"""채팅방 API 테스트"""

import pytest
from httpx import AsyncClient


async def create_user_and_login(client: AsyncClient, username: str, email: str):
    """테스트 유틸: 사용자 생성 및 로그인 후 토큰과 사용자 ID 반환"""
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


class TestChatRoom:
    """채팅방 테스트"""

    async def test_create_room(self, client: AsyncClient):
        """1:1 채팅방 생성 테스트"""
        token1, user1_id = await create_user_and_login(client, "roomuser1", "room1@example.com")
        token2, user2_id = await create_user_and_login(client, "roomuser2", "room2@example.com")

        # 채팅방 생성
        response = await client.post(
            "/api/rooms",
            json={"other_user_id": user2_id},
            headers={"Authorization": f"Bearer {token1}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert len(data["members"]) == 2

    async def test_create_room_with_self(self, client: AsyncClient):
        """자기 자신과 채팅방 생성 실패 테스트"""
        token, user_id = await create_user_and_login(client, "selfchat", "self@example.com")

        response = await client.post(
            "/api/rooms",
            json={"other_user_id": user_id},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 400

    async def test_get_existing_room(self, client: AsyncClient):
        """기존 채팅방 반환 테스트 (중복 생성 방지)"""
        token1, user1_id = await create_user_and_login(client, "existuser1", "exist1@example.com")
        _, user2_id = await create_user_and_login(client, "existuser2", "exist2@example.com")

        # 첫 번째 채팅방 생성
        response1 = await client.post(
            "/api/rooms",
            json={"other_user_id": user2_id},
            headers={"Authorization": f"Bearer {token1}"},
        )
        room_id_1 = response1.json()["id"]

        # 같은 사용자와 다시 채팅방 생성 시도
        response2 = await client.post(
            "/api/rooms",
            json={"other_user_id": user2_id},
            headers={"Authorization": f"Bearer {token1}"},
        )
        room_id_2 = response2.json()["id"]

        # 같은 채팅방이 반환되어야 함
        assert room_id_1 == room_id_2

    async def test_list_my_rooms(self, client: AsyncClient):
        """내 채팅방 목록 조회 테스트"""
        token1, user1_id = await create_user_and_login(client, "listuser1", "list1@example.com")
        _, user2_id = await create_user_and_login(client, "listuser2", "list2@example.com")
        _, user3_id = await create_user_and_login(client, "listuser3", "list3@example.com")

        # 두 개의 채팅방 생성
        await client.post(
            "/api/rooms",
            json={"other_user_id": user2_id},
            headers={"Authorization": f"Bearer {token1}"},
        )
        await client.post(
            "/api/rooms",
            json={"other_user_id": user3_id},
            headers={"Authorization": f"Bearer {token1}"},
        )

        # 목록 조회
        response = await client.get(
            "/api/rooms", headers={"Authorization": f"Bearer {token1}"}
        )
        assert response.status_code == 200
        rooms = response.json()
        assert len(rooms) == 2

    async def test_create_room_unauthorized(self, client: AsyncClient):
        """인증 없이 채팅방 생성 실패 테스트"""
        response = await client.post(
            "/api/rooms",
            json={"other_user_id": "some-user-id"},
        )
        assert response.status_code == 401
