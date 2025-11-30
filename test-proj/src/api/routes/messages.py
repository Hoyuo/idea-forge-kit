from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.database import get_db
from src.models.message import Message, MessageRead
from src.models.room import ChatRoomMember
from src.models.user import User
from src.schemas.message import MessageCreate, MessageResponse
from src.websocket.manager import manager

router = APIRouter(prefix="/api/rooms", tags=["messages"])
read_router = APIRouter(prefix="/api/messages", tags=["read-status"])


async def check_room_membership(db: AsyncSession, room_id: str, user_id: str) -> bool:
    """사용자가 채팅방 멤버인지 확인"""
    result = await db.execute(
        select(ChatRoomMember).where(
            ChatRoomMember.room_id == room_id, ChatRoomMember.user_id == user_id
        )
    )
    return result.scalar_one_or_none() is not None


async def get_room_member_ids(db: AsyncSession, room_id: str) -> list[str]:
    """채팅방 멤버 ID 목록 조회"""
    result = await db.execute(
        select(ChatRoomMember.user_id).where(ChatRoomMember.room_id == room_id)
    )
    return [r for r in result.scalars().all()]


@router.get("/{room_id}/messages", response_model=list[MessageResponse])
async def get_messages(
    room_id: str,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """채팅방 메시지 히스토리 조회"""
    # 채팅방 멤버 확인
    if not await check_room_membership(db, room_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this room",
        )

    result = await db.execute(
        select(Message)
        .where(Message.room_id == room_id)
        .order_by(Message.created_at.asc())
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()


@router.post(
    "/{room_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED
)
async def send_message(
    room_id: str,
    message_data: MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 채팅방 멤버 확인
    if not await check_room_membership(db, room_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this room",
        )

    # 메시지 저장
    message = Message(
        room_id=room_id,
        sender_id=current_user.id,
        content=message_data.content,
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)

    # WebSocket으로 실시간 전송
    member_ids = await get_room_member_ids(db, room_id)
    await manager.broadcast_to_room(
        member_ids,
        {
            "type": "message",
            "room_id": room_id,
            "message": MessageResponse.model_validate(message).model_dump(mode="json"),
        },
    )

    return message


@read_router.post("/{message_id}/read")
async def mark_as_read(
    message_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """메시지 읽음 표시"""
    # 메시지 존재 확인
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalar_one_or_none()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    # 채팅방 멤버 확인
    if not await check_room_membership(db, message.room_id, current_user.id):
        raise HTTPException(status_code=403, detail="You are not a member of this room")

    # 이미 읽음 표시 확인
    existing = await db.execute(
        select(MessageRead).where(
            MessageRead.message_id == message_id, MessageRead.user_id == current_user.id
        )
    )
    if existing.scalar_one_or_none():
        return {"read": True, "message_id": message_id}

    # 읽음 표시 저장
    read_status = MessageRead(message_id=message_id, user_id=current_user.id)
    db.add(read_status)
    await db.commit()

    return {"read": True, "message_id": message_id}


@router.get("/{room_id}/unread")
async def get_unread_count(
    room_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """안 읽은 메시지 수 조회"""
    if not await check_room_membership(db, room_id, current_user.id):
        raise HTTPException(status_code=403, detail="You are not a member of this room")

    # 채팅방 내 전체 메시지 중 내가 보내지 않은 메시지
    all_messages = select(Message.id).where(
        Message.room_id == room_id, Message.sender_id != current_user.id
    )

    # 내가 읽은 메시지
    read_messages = select(MessageRead.message_id).where(
        MessageRead.user_id == current_user.id
    )

    # 안 읽은 메시지 수
    result = await db.execute(
        select(func.count()).select_from(
            all_messages.except_(read_messages).subquery()
        )
    )
    unread_count = result.scalar() or 0

    return {"room_id": room_id, "unread_count": unread_count}


@router.post("/{room_id}/read-all")
async def mark_all_as_read(
    room_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """채팅방 전체 메시지 읽음 처리"""
    if not await check_room_membership(db, room_id, current_user.id):
        raise HTTPException(status_code=403, detail="You are not a member of this room")

    # 내가 보내지 않은 안 읽은 메시지 조회
    result = await db.execute(
        select(Message.id).where(
            Message.room_id == room_id,
            Message.sender_id != current_user.id,
            ~Message.id.in_(
                select(MessageRead.message_id).where(MessageRead.user_id == current_user.id)
            ),
        )
    )
    unread_message_ids = result.scalars().all()

    # 읽음 표시 일괄 저장
    for msg_id in unread_message_ids:
        read_status = MessageRead(message_id=msg_id, user_id=current_user.id)
        db.add(read_status)

    await db.commit()

    return {"room_id": room_id, "marked_count": len(unread_message_ids)}
