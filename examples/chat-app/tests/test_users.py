"""사용자 목록 API 테스트"""

import pytest
from httpx import AsyncClient


async def create_user_and_login(client: AsyncClient, username: str, email: str):
    """테스트 유틸: 사용자 생성 및 로그인 후 토큰 반환"""
    await client.post(
        "/api/auth/register",
        json={"username": username, "email": email, "password": "password123"},
    )
    response = await client.post(
        "/api/auth/login",
        json={"username": username, "password": "password123"},
    )
    return response.json()["access_token"]


class TestUserList:
    """사용자 목록 테스트"""

    async def test_list_users(self, client: AsyncClient):
        """사용자 목록 조회 테스트"""
        # 여러 사용자 생성
        token = await create_user_and_login(client, "user1", "user1@example.com")
        await create_user_and_login(client, "user2", "user2@example.com")
        await create_user_and_login(client, "user3", "user3@example.com")

        # 목록 조회
        response = await client.get(
            "/api/users", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        users = response.json()
        assert len(users) == 3

    async def test_search_users(self, client: AsyncClient):
        """사용자 검색 테스트"""
        token = await create_user_and_login(client, "searchuser", "search@example.com")
        await create_user_and_login(client, "anotheruser", "another@example.com")
        await create_user_and_login(client, "searchme", "searchme@example.com")

        # 'search' 키워드로 검색
        response = await client.get(
            "/api/users/search?q=search", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        users = response.json()
        assert len(users) == 2  # searchuser, searchme

    async def test_list_users_unauthorized(self, client: AsyncClient):
        """인증 없이 사용자 목록 조회 실패 테스트"""
        response = await client.get("/api/users")
        assert response.status_code == 401
