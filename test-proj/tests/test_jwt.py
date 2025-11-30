"""JWT 토큰 테스트"""

import pytest
from httpx import AsyncClient


class TestJWTMiddleware:
    """JWT 미들웨어 테스트"""

    async def test_protected_route_without_token(self, client: AsyncClient):
        """토큰 없이 보호된 경로 접근 테스트"""
        response = await client.get("/api/auth/me")
        assert response.status_code == 401

    async def test_protected_route_with_invalid_token(self, client: AsyncClient):
        """잘못된 토큰으로 보호된 경로 접근 테스트"""
        response = await client.get(
            "/api/auth/me", headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401

    async def test_protected_route_with_valid_token(self, client: AsyncClient):
        """유효한 토큰으로 보호된 경로 접근 테스트"""
        # 회원가입
        await client.post(
            "/api/auth/register",
            json={
                "username": "tokenuser",
                "email": "token@example.com",
                "password": "password123",
            },
        )

        # 로그인하여 토큰 획득
        login_response = await client.post(
            "/api/auth/login",
            json={"username": "tokenuser", "password": "password123"},
        )
        access_token = login_response.json()["access_token"]

        # 보호된 경로 접근
        response = await client.get(
            "/api/auth/me", headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "tokenuser"
        assert data["email"] == "token@example.com"

    async def test_token_refresh(self, client: AsyncClient):
        """토큰 갱신 테스트"""
        # 회원가입 및 로그인
        await client.post(
            "/api/auth/register",
            json={
                "username": "refreshuser",
                "email": "refresh@example.com",
                "password": "password123",
            },
        )
        login_response = await client.post(
            "/api/auth/login",
            json={"username": "refreshuser", "password": "password123"},
        )
        refresh_token = login_response.json()["refresh_token"]

        # 토큰 갱신
        response = await client.post(
            "/api/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    async def test_expired_token(self, client: AsyncClient):
        """만료된 토큰 테스트"""
        from datetime import datetime, timedelta, timezone

        from jose import jwt

        from src.core.config import settings

        # 이미 만료된 토큰 생성
        expired_token = jwt.encode(
            {
                "sub": "test-user-id",
                "username": "testuser",
                "exp": datetime.now(timezone.utc) - timedelta(hours=1),
                "type": "access",
            },
            settings.secret_key,
            algorithm=settings.algorithm,
        )

        response = await client.get(
            "/api/auth/me", headers={"Authorization": f"Bearer {expired_token}"}
        )
        assert response.status_code == 401
