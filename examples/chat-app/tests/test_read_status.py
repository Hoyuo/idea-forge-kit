"""읽음 표시 기능 테스트"""

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.message import MessageRead


async def create_user_and_login(client: AsyncClient, username: str, email: str):
    """테스트 유틸"""
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


class TestMessageReadStatus:
    """메시지 읽음 표시 테스트"""

    async def test_mark_message_as_read(self, client: AsyncClient):
        """메시지 읽음 표시 테스트"""
        token1, user1_id = await create_user_and_login(client, "readuser1", "read1@example.com")
        token2, user2_id = await create_user_and_login(client, "readuser2", "read2@example.com")

        # 채팅방 생성
        room_response = await client.post(
            "/api/rooms",
            json={"other_user_id": user2_id},
            headers={"Authorization": f"Bearer {token1}"},
        )
        room_id = room_response.json()["id"]

        # user1이 메시지 전송
        msg_response = await client.post(
            f"/api/rooms/{room_id}/messages",
            json={"content": "Hello!"},
            headers={"Authorization": f"Bearer {token1}"},
        )
        message_id = msg_response.json()["id"]

        # user2가 메시지 읽음 표시
        response = await client.post(
            f"/api/messages/{message_id}/read",
            headers={"Authorization": f"Bearer {token2}"},
        )
        assert response.status_code == 200
        assert response.json()["read"] is True

    async def test_get_unread_count(self, client: AsyncClient):
        """안 읽은 메시지 수 조회 테스트"""
        token1, user1_id = await create_user_and_login(client, "unreaduser1", "unread1@example.com")
        token2, user2_id = await create_user_and_login(client, "unreaduser2", "unread2@example.com")

        # 채팅방 생성
        room_response = await client.post(
            "/api/rooms",
            json={"other_user_id": user2_id},
            headers={"Authorization": f"Bearer {token1}"},
        )
        room_id = room_response.json()["id"]

        # user1이 3개 메시지 전송
        for i in range(3):
            await client.post(
                f"/api/rooms/{room_id}/messages",
                json={"content": f"Message {i}"},
                headers={"Authorization": f"Bearer {token1}"},
            )

        # user2가 안 읽은 메시지 수 확인
        response = await client.get(
            f"/api/rooms/{room_id}/unread",
            headers={"Authorization": f"Bearer {token2}"},
        )
        assert response.status_code == 200
        assert response.json()["unread_count"] == 3

    async def test_mark_all_as_read(self, client: AsyncClient):
        """채팅방 전체 읽음 처리 테스트"""
        token1, user1_id = await create_user_and_login(client, "allreaduser1", "allread1@example.com")
        token2, user2_id = await create_user_and_login(client, "allreaduser2", "allread2@example.com")

        # 채팅방 생성
        room_response = await client.post(
            "/api/rooms",
            json={"other_user_id": user2_id},
            headers={"Authorization": f"Bearer {token1}"},
        )
        room_id = room_response.json()["id"]

        # user1이 메시지 전송
        for i in range(5):
            await client.post(
                f"/api/rooms/{room_id}/messages",
                json={"content": f"Message {i}"},
                headers={"Authorization": f"Bearer {token1}"},
            )

        # user2가 전체 읽음 처리
        response = await client.post(
            f"/api/rooms/{room_id}/read-all",
            headers={"Authorization": f"Bearer {token2}"},
        )
        assert response.status_code == 200
        assert response.json()["marked_count"] == 5

        # 안 읽은 메시지 수 확인
        unread_response = await client.get(
            f"/api/rooms/{room_id}/unread",
            headers={"Authorization": f"Bearer {token2}"},
        )
        assert unread_response.json()["unread_count"] == 0
