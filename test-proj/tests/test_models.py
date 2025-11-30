"""데이터베이스 모델 테스트"""

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.models.room import ChatRoom, ChatRoomMember
from src.models.message import Message


class TestUserModel:
    """User 모델 테스트"""

    async def test_create_user(self, async_session: AsyncSession):
        """사용자 생성 테스트"""
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password",
        )
        async_session.add(user)
        await async_session.commit()

        result = await async_session.execute(select(User).where(User.username == "testuser"))
        saved_user = result.scalar_one()

        assert saved_user.username == "testuser"
        assert saved_user.email == "test@example.com"
        assert saved_user.is_active is True
        assert saved_user.id is not None

    async def test_user_unique_username(self, async_session: AsyncSession):
        """사용자명 중복 방지 테스트"""
        user1 = User(username="duplicate", email="user1@example.com", password_hash="hash1")
        user2 = User(username="duplicate", email="user2@example.com", password_hash="hash2")

        async_session.add(user1)
        await async_session.commit()

        async_session.add(user2)
        with pytest.raises(Exception):  # IntegrityError
            await async_session.commit()


class TestChatRoomModel:
    """ChatRoom 모델 테스트"""

    async def test_create_chat_room(self, async_session: AsyncSession):
        """채팅방 생성 테스트"""
        room = ChatRoom()
        async_session.add(room)
        await async_session.commit()

        assert room.id is not None
        assert room.created_at is not None

    async def test_add_members_to_room(self, async_session: AsyncSession):
        """채팅방 멤버 추가 테스트"""
        # 사용자 생성
        user1 = User(username="user1", email="user1@example.com", password_hash="hash1")
        user2 = User(username="user2", email="user2@example.com", password_hash="hash2")
        async_session.add_all([user1, user2])
        await async_session.commit()

        # 채팅방 생성
        room = ChatRoom()
        async_session.add(room)
        await async_session.commit()

        # 멤버 추가
        member1 = ChatRoomMember(room_id=room.id, user_id=user1.id)
        member2 = ChatRoomMember(room_id=room.id, user_id=user2.id)
        async_session.add_all([member1, member2])
        await async_session.commit()

        # 검증
        result = await async_session.execute(
            select(ChatRoomMember).where(ChatRoomMember.room_id == room.id)
        )
        members = result.scalars().all()
        assert len(members) == 2


class TestMessageModel:
    """Message 모델 테스트"""

    async def test_create_message(self, async_session: AsyncSession):
        """메시지 생성 테스트"""
        # 사용자 및 채팅방 생성
        user = User(username="sender", email="sender@example.com", password_hash="hash")
        room = ChatRoom()
        async_session.add_all([user, room])
        await async_session.commit()

        # 메시지 생성
        message = Message(room_id=room.id, sender_id=user.id, content="Hello, World!")
        async_session.add(message)
        await async_session.commit()

        assert message.id is not None
        assert message.content == "Hello, World!"
        assert message.created_at is not None

    async def test_message_ordering(self, async_session: AsyncSession):
        """메시지 시간순 정렬 테스트"""
        user = User(username="sender2", email="sender2@example.com", password_hash="hash")
        room = ChatRoom()
        async_session.add_all([user, room])
        await async_session.commit()

        # 여러 메시지 생성
        messages = [
            Message(room_id=room.id, sender_id=user.id, content=f"Message {i}")
            for i in range(3)
        ]
        async_session.add_all(messages)
        await async_session.commit()

        # 시간순 조회
        result = await async_session.execute(
            select(Message)
            .where(Message.room_id == room.id)
            .order_by(Message.created_at.asc())
        )
        saved_messages = result.scalars().all()

        assert len(saved_messages) == 3
        assert saved_messages[0].content == "Message 0"
