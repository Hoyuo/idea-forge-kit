from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.database import get_db
from src.models.room import ChatRoom, ChatRoomMember
from src.models.user import User
from src.schemas.room import RoomCreate, RoomMemberResponse, RoomResponse

router = APIRouter(prefix="/api/rooms", tags=["rooms"])


async def find_existing_room(
    db: AsyncSession, user1_id: str, user2_id: str
) -> ChatRoom | None:
    """두 사용자 간 기존 채팅방 찾기"""
    # user1이 속한 채팅방 중 user2도 속한 채팅방 찾기
    subquery = (
        select(ChatRoomMember.room_id)
        .where(ChatRoomMember.user_id == user1_id)
        .subquery()
    )
    result = await db.execute(
        select(ChatRoomMember.room_id)
        .where(
            ChatRoomMember.user_id == user2_id,
            ChatRoomMember.room_id.in_(select(subquery.c.room_id)),
        )
    )
    room_id = result.scalar_one_or_none()

    if room_id:
        result = await db.execute(select(ChatRoom).where(ChatRoom.id == room_id))
        return result.scalar_one_or_none()
    return None


@router.post("", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create_room(
    room_data: RoomCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 자기 자신과 채팅방 생성 불가
    if room_data.other_user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create room with yourself",
        )

    # 상대방 사용자 존재 확인
    result = await db.execute(select(User).where(User.id == room_data.other_user_id))
    other_user = result.scalar_one_or_none()
    if not other_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # 기존 채팅방 확인
    existing_room = await find_existing_room(db, current_user.id, room_data.other_user_id)
    if existing_room:
        # 기존 채팅방의 멤버 조회
        result = await db.execute(
            select(ChatRoomMember).where(ChatRoomMember.room_id == existing_room.id)
        )
        members = result.scalars().all()
        return RoomResponse(
            id=existing_room.id,
            created_at=existing_room.created_at,
            members=[RoomMemberResponse.model_validate(m) for m in members],
        )

    # 새 채팅방 생성
    room = ChatRoom()
    db.add(room)
    await db.flush()

    # 멤버 추가
    member1 = ChatRoomMember(room_id=room.id, user_id=current_user.id)
    member2 = ChatRoomMember(room_id=room.id, user_id=room_data.other_user_id)
    db.add_all([member1, member2])
    await db.commit()

    return RoomResponse(
        id=room.id,
        created_at=room.created_at,
        members=[
            RoomMemberResponse.model_validate(member1),
            RoomMemberResponse.model_validate(member2),
        ],
    )


@router.get("", response_model=list[RoomResponse])
async def list_rooms(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 현재 사용자가 속한 채팅방 ID 조회
    result = await db.execute(
        select(ChatRoomMember.room_id).where(ChatRoomMember.user_id == current_user.id)
    )
    room_ids = [r for r in result.scalars().all()]

    if not room_ids:
        return []

    # 채팅방 정보 및 멤버 조회
    rooms_result = await db.execute(select(ChatRoom).where(ChatRoom.id.in_(room_ids)))
    rooms = rooms_result.scalars().all()

    response = []
    for room in rooms:
        members_result = await db.execute(
            select(ChatRoomMember).where(ChatRoomMember.room_id == room.id)
        )
        members = members_result.scalars().all()
        response.append(
            RoomResponse(
                id=room.id,
                created_at=room.created_at,
                members=[RoomMemberResponse.model_validate(m) for m in members],
            )
        )

    return response
