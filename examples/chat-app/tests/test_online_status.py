"""온라인 상태 관리 테스트"""

import pytest
from unittest.mock import MagicMock


class TestOnlineStatusManager:
    """온라인 상태 관리자 테스트"""

    def test_set_online(self):
        """온라인 상태 설정 테스트"""
        from src.websocket.status import OnlineStatusManager

        manager = OnlineStatusManager()
        manager.set_online("user-123")

        assert manager.is_online("user-123") is True

    def test_set_offline(self):
        """오프라인 상태 설정 테스트"""
        from src.websocket.status import OnlineStatusManager

        manager = OnlineStatusManager()
        manager.set_online("user-123")
        manager.set_offline("user-123")

        assert manager.is_online("user-123") is False

    def test_get_online_users(self):
        """온라인 사용자 목록 조회 테스트"""
        from src.websocket.status import OnlineStatusManager

        manager = OnlineStatusManager()
        manager.set_online("user-1")
        manager.set_online("user-2")
        manager.set_online("user-3")

        online_users = manager.get_online_users()
        assert len(online_users) == 3
        assert "user-1" in online_users
        assert "user-2" in online_users

    def test_get_online_users_from_list(self):
        """특정 사용자 목록 중 온라인인 사용자 조회"""
        from src.websocket.status import OnlineStatusManager

        manager = OnlineStatusManager()
        manager.set_online("user-1")
        manager.set_online("user-3")

        user_ids = ["user-1", "user-2", "user-3", "user-4"]
        online = manager.get_online_from_list(user_ids)

        assert len(online) == 2
        assert "user-1" in online
        assert "user-3" in online
        assert "user-2" not in online


class TestOnlineStatusAPI:
    """온라인 상태 API 테스트"""

    async def test_get_user_status(self, client):
        """사용자 온라인 상태 조회 테스트"""
        from httpx import AsyncClient

        # 회원가입
        reg_response = await client.post(
            "/api/auth/register",
            json={"username": "statususer", "email": "status@example.com", "password": "password123"},
        )
        user_id = reg_response.json()["id"]

        login_response = await client.post(
            "/api/auth/login",
            json={"username": "statususer", "password": "password123"},
        )
        token = login_response.json()["access_token"]

        # 상태 조회 (WebSocket 미연결 상태이므로 offline)
        response = await client.get(
            f"/api/users/{user_id}/status",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == user_id
        assert data["is_online"] is False

    async def test_get_room_members_status(self, client):
        """채팅방 멤버 온라인 상태 조회 테스트"""
        from httpx import AsyncClient

        # 두 사용자 생성
        reg1 = await client.post(
            "/api/auth/register",
            json={"username": "roomstatus1", "email": "roomstatus1@example.com", "password": "password123"},
        )
        user1_id = reg1.json()["id"]

        reg2 = await client.post(
            "/api/auth/register",
            json={"username": "roomstatus2", "email": "roomstatus2@example.com", "password": "password123"},
        )
        user2_id = reg2.json()["id"]

        login1 = await client.post(
            "/api/auth/login",
            json={"username": "roomstatus1", "password": "password123"},
        )
        token1 = login1.json()["access_token"]

        # 채팅방 생성
        room_response = await client.post(
            "/api/rooms",
            json={"other_user_id": user2_id},
            headers={"Authorization": f"Bearer {token1}"},
        )
        room_id = room_response.json()["id"]

        # 채팅방 멤버 상태 조회
        response = await client.get(
            f"/api/rooms/{room_id}/status",
            headers={"Authorization": f"Bearer {token1}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["members"]) == 2
