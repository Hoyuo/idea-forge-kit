"""실시간 메시지 송수신 테스트"""

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.message import Message


async def create_user_and_login(client: AsyncClient, username: str, email: str):
    """테스트 유틸: 사용자 생성 및 로그인"""
    reg_response = await client.post(
        "/api/auth/register",
        json={"username": username, "email": email, "password": "password123"},
    )
    user_id = reg_response.json()["id"]

    login_response = await client.post(
        "/api/auth/login",
        json={"username": username, "password": "password123"},
    )
    return login_response.json()["access_token"], user_id


class TestMessageSend:
    """메시지 전송 테스트 (REST API)"""

    async def test_send_message(self, client: AsyncClient, async_session: AsyncSession):
        """메시지 전송 테스트"""
        token1, user1_id = await create_user_and_login(client, "msguser1", "msg1@example.com")
        _, user2_id = await create_user_and_login(client, "msguser2", "msg2@example.com")

        # 채팅방 생성
        room_response = await client.post(
            "/api/rooms",
            json={"other_user_id": user2_id},
            headers={"Authorization": f"Bearer {token1}"},
        )
        room_id = room_response.json()["id"]

        # 메시지 전송
        response = await client.post(
            f"/api/rooms/{room_id}/messages",
            json={"content": "Hello, World!"},
            headers={"Authorization": f"Bearer {token1}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["content"] == "Hello, World!"
        assert data["sender_id"] == user1_id
        assert data["room_id"] == room_id

    async def test_send_message_to_nonmember_room(self, client: AsyncClient):
        """멤버가 아닌 채팅방에 메시지 전송 실패 테스트"""
        token1, user1_id = await create_user_and_login(client, "nonmember1", "nonmember1@example.com")
        token2, user2_id = await create_user_and_login(client, "nonmember2", "nonmember2@example.com")
        token3, user3_id = await create_user_and_login(client, "nonmember3", "nonmember3@example.com")

        # user1과 user2의 채팅방 생성
        room_response = await client.post(
            "/api/rooms",
            json={"other_user_id": user2_id},
            headers={"Authorization": f"Bearer {token1}"},
        )
        room_id = room_response.json()["id"]

        # user3가 해당 채팅방에 메시지 전송 시도
        response = await client.post(
            f"/api/rooms/{room_id}/messages",
            json={"content": "I shouldn't be here!"},
            headers={"Authorization": f"Bearer {token3}"},
        )
        assert response.status_code == 403

    async def test_send_empty_message(self, client: AsyncClient):
        """빈 메시지 전송 실패 테스트"""
        token1, user1_id = await create_user_and_login(client, "emptyuser1", "empty1@example.com")
        _, user2_id = await create_user_and_login(client, "emptyuser2", "empty2@example.com")

        room_response = await client.post(
            "/api/rooms",
            json={"other_user_id": user2_id},
            headers={"Authorization": f"Bearer {token1}"},
        )
        room_id = room_response.json()["id"]

        response = await client.post(
            f"/api/rooms/{room_id}/messages",
            json={"content": ""},
            headers={"Authorization": f"Bearer {token1}"},
        )
        assert response.status_code == 422


class TestMessagePersistence:
    """메시지 저장 테스트"""

    async def test_message_saved_to_db(self, client: AsyncClient, async_session: AsyncSession):
        """메시지가 DB에 저장되는지 테스트"""
        token1, user1_id = await create_user_and_login(client, "dbuser1", "db1@example.com")
        _, user2_id = await create_user_and_login(client, "dbuser2", "db2@example.com")

        room_response = await client.post(
            "/api/rooms",
            json={"other_user_id": user2_id},
            headers={"Authorization": f"Bearer {token1}"},
        )
        room_id = room_response.json()["id"]

        # 메시지 전송
        await client.post(
            f"/api/rooms/{room_id}/messages",
            json={"content": "Persistent message"},
            headers={"Authorization": f"Bearer {token1}"},
        )

        # DB에서 직접 확인
        result = await async_session.execute(
            select(Message).where(Message.room_id == room_id)
        )
        messages = result.scalars().all()
        assert len(messages) == 1
        assert messages[0].content == "Persistent message"
