"""메시지 히스토리 API 테스트"""

import pytest
from httpx import AsyncClient


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


class TestMessageHistory:
    """메시지 히스토리 테스트"""

    async def test_get_message_history(self, client: AsyncClient):
        """메시지 히스토리 조회 테스트"""
        token1, user1_id = await create_user_and_login(client, "histuser1", "hist1@example.com")
        _, user2_id = await create_user_and_login(client, "histuser2", "hist2@example.com")

        # 채팅방 생성
        room_response = await client.post(
            "/api/rooms",
            json={"other_user_id": user2_id},
            headers={"Authorization": f"Bearer {token1}"},
        )
        room_id = room_response.json()["id"]

        # 메시지 전송
        for i in range(5):
            await client.post(
                f"/api/rooms/{room_id}/messages",
                json={"content": f"Message {i}"},
                headers={"Authorization": f"Bearer {token1}"},
            )

        # 히스토리 조회
        response = await client.get(
            f"/api/rooms/{room_id}/messages",
            headers={"Authorization": f"Bearer {token1}"},
        )
        assert response.status_code == 200
        messages = response.json()
        assert len(messages) == 5
        # 시간순 정렬 확인 (오래된 것 먼저)
        assert messages[0]["content"] == "Message 0"
        assert messages[4]["content"] == "Message 4"

    async def test_get_message_history_with_pagination(self, client: AsyncClient):
        """페이지네이션 테스트"""
        token1, user1_id = await create_user_and_login(client, "pageuser1", "page1@example.com")
        _, user2_id = await create_user_and_login(client, "pageuser2", "page2@example.com")

        room_response = await client.post(
            "/api/rooms",
            json={"other_user_id": user2_id},
            headers={"Authorization": f"Bearer {token1}"},
        )
        room_id = room_response.json()["id"]

        # 15개 메시지 전송
        for i in range(15):
            await client.post(
                f"/api/rooms/{room_id}/messages",
                json={"content": f"Message {i}"},
                headers={"Authorization": f"Bearer {token1}"},
            )

        # 첫 페이지 (10개)
        response = await client.get(
            f"/api/rooms/{room_id}/messages?limit=10",
            headers={"Authorization": f"Bearer {token1}"},
        )
        messages = response.json()
        assert len(messages) == 10

        # 두 번째 페이지 (offset 사용)
        response = await client.get(
            f"/api/rooms/{room_id}/messages?limit=10&offset=10",
            headers={"Authorization": f"Bearer {token1}"},
        )
        messages = response.json()
        assert len(messages) == 5

    async def test_get_history_nonmember(self, client: AsyncClient):
        """멤버가 아닌 채팅방 히스토리 조회 실패 테스트"""
        token1, user1_id = await create_user_and_login(client, "nonhist1", "nonhist1@example.com")
        token2, user2_id = await create_user_and_login(client, "nonhist2", "nonhist2@example.com")
        token3, _ = await create_user_and_login(client, "nonhist3", "nonhist3@example.com")

        room_response = await client.post(
            "/api/rooms",
            json={"other_user_id": user2_id},
            headers={"Authorization": f"Bearer {token1}"},
        )
        room_id = room_response.json()["id"]

        # user3가 조회 시도
        response = await client.get(
            f"/api/rooms/{room_id}/messages",
            headers={"Authorization": f"Bearer {token3}"},
        )
        assert response.status_code == 403
