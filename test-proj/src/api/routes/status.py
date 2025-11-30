"""온라인 상태 API 라우터"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.database import get_db
from src.models.room import ChatRoomMember
from src.models.user import User
from src.websocket.status import status_manager

router = APIRouter(prefix="/api", tags=["status"])


@router.get("/users/{user_id}/status")
async def get_user_status(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """사용자 온라인 상태 조회"""
    # 사용자 존재 확인
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "user_id": user_id,
        "is_online": status_manager.is_online(user_id),
    }


@router.get("/rooms/{room_id}/status")
async def get_room_members_status(
    room_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """채팅방 멤버 온라인 상태 조회"""
    # 채팅방 멤버 확인
    result = await db.execute(
        select(ChatRoomMember).where(ChatRoomMember.room_id == room_id)
    )
    members = result.scalars().all()

    if not members:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    # 현재 사용자가 멤버인지 확인
    member_ids = [m.user_id for m in members]
    if current_user.id not in member_ids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this room",
        )

    return {
        "room_id": room_id,
        "members": [
            {"user_id": uid, "is_online": status_manager.is_online(uid)}
            for uid in member_ids
        ],
    }
