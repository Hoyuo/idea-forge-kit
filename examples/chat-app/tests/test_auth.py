"""인증 API 테스트"""

import pytest
from httpx import AsyncClient


class TestAuthRegister:
    """회원가입 테스트"""

    async def test_register_success(self, client: AsyncClient):
        """회원가입 성공 테스트"""
        response = await client.post(
            "/api/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "securepassword123",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "password" not in data
        assert "id" in data

    async def test_register_duplicate_username(self, client: AsyncClient):
        """중복 사용자명 회원가입 실패 테스트"""
        # 첫 번째 사용자 등록
        await client.post(
            "/api/auth/register",
            json={
                "username": "duplicate",
                "email": "first@example.com",
                "password": "password123",
            },
        )

        # 같은 사용자명으로 등록 시도
        response = await client.post(
            "/api/auth/register",
            json={
                "username": "duplicate",
                "email": "second@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 400
        assert "username" in response.json()["detail"].lower()

    async def test_register_invalid_email(self, client: AsyncClient):
        """잘못된 이메일 형식 테스트"""
        response = await client.post(
            "/api/auth/register",
            json={
                "username": "validuser",
                "email": "invalid-email",
                "password": "password123",
            },
        )
        assert response.status_code == 422  # Validation error

    async def test_register_short_password(self, client: AsyncClient):
        """짧은 비밀번호 테스트"""
        response = await client.post(
            "/api/auth/register",
            json={
                "username": "validuser",
                "email": "valid@example.com",
                "password": "short",
            },
        )
        assert response.status_code == 422


class TestAuthLogin:
    """로그인 테스트"""

    async def test_login_success(self, client: AsyncClient):
        """로그인 성공 테스트"""
        # 먼저 회원가입
        await client.post(
            "/api/auth/register",
            json={
                "username": "loginuser",
                "email": "login@example.com",
                "password": "password123",
            },
        )

        # 로그인 시도
        response = await client.post(
            "/api/auth/login",
            json={"username": "loginuser", "password": "password123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_wrong_password(self, client: AsyncClient):
        """잘못된 비밀번호 로그인 실패 테스트"""
        # 먼저 회원가입
        await client.post(
            "/api/auth/register",
            json={
                "username": "wrongpwuser",
                "email": "wrongpw@example.com",
                "password": "correctpassword",
            },
        )

        # 잘못된 비밀번호로 로그인
        response = await client.post(
            "/api/auth/login",
            json={"username": "wrongpwuser", "password": "wrongpassword"},
        )
        assert response.status_code == 401

    async def test_login_nonexistent_user(self, client: AsyncClient):
        """존재하지 않는 사용자 로그인 실패 테스트"""
        response = await client.post(
            "/api/auth/login",
            json={"username": "nonexistent", "password": "password123"},
        )
        assert response.status_code == 401


class TestPasswordHashing:
    """비밀번호 해시화 테스트"""

    def test_password_hashing(self):
        """비밀번호 해시화 및 검증 테스트"""
        from src.core.security import hash_password, verify_password

        password = "mysecretpassword"
        hashed = hash_password(password)

        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False
