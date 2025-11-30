"""WebSocket 연결 관리자 테스트"""

import pytest
from unittest.mock import AsyncMock, MagicMock


class TestConnectionManager:
    """ConnectionManager 테스트"""

    def test_connect(self):
        """연결 추가 테스트"""
        from src.websocket.manager import ConnectionManager

        manager = ConnectionManager()
        websocket = MagicMock()
        user_id = "user-123"

        manager.connect(user_id, websocket)

        assert user_id in manager.active_connections
        assert manager.active_connections[user_id] == websocket

    def test_disconnect(self):
        """연결 해제 테스트"""
        from src.websocket.manager import ConnectionManager

        manager = ConnectionManager()
        websocket = MagicMock()
        user_id = "user-123"

        manager.connect(user_id, websocket)
        manager.disconnect(user_id)

        assert user_id not in manager.active_connections

    def test_is_connected(self):
        """연결 상태 확인 테스트"""
        from src.websocket.manager import ConnectionManager

        manager = ConnectionManager()
        websocket = MagicMock()
        user_id = "user-123"

        assert manager.is_connected(user_id) is False
        manager.connect(user_id, websocket)
        assert manager.is_connected(user_id) is True

    async def test_send_personal_message(self):
        """개인 메시지 전송 테스트"""
        from src.websocket.manager import ConnectionManager

        manager = ConnectionManager()
        websocket = AsyncMock()
        user_id = "user-123"
        message = {"type": "message", "content": "Hello!"}

        manager.connect(user_id, websocket)
        await manager.send_personal_message(user_id, message)

        websocket.send_json.assert_called_once_with(message)

    async def test_broadcast_to_room(self):
        """채팅방 브로드캐스트 테스트"""
        from src.websocket.manager import ConnectionManager

        manager = ConnectionManager()
        ws1 = AsyncMock()
        ws2 = AsyncMock()
        ws3 = AsyncMock()

        manager.connect("user1", ws1)
        manager.connect("user2", ws2)
        manager.connect("user3", ws3)  # 채팅방에 없는 사용자

        room_member_ids = ["user1", "user2"]
        message = {"type": "message", "content": "Hello room!"}

        await manager.broadcast_to_room(room_member_ids, message)

        ws1.send_json.assert_called_once_with(message)
        ws2.send_json.assert_called_once_with(message)
        ws3.send_json.assert_not_called()

    def test_get_connection_count(self):
        """연결 수 확인 테스트"""
        from src.websocket.manager import ConnectionManager

        manager = ConnectionManager()
        assert manager.get_connection_count() == 0

        manager.connect("user1", MagicMock())
        manager.connect("user2", MagicMock())
        assert manager.get_connection_count() == 2

        manager.disconnect("user1")
        assert manager.get_connection_count() == 1
