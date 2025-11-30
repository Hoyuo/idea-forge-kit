from fastapi import WebSocket


class ConnectionManager:
    """WebSocket 연결 관리자"""

    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    def connect(self, user_id: str, websocket: WebSocket):
        """사용자 연결 추가"""
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        """사용자 연결 해제"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    def is_connected(self, user_id: str) -> bool:
        """사용자 연결 상태 확인"""
        return user_id in self.active_connections

    async def send_personal_message(self, user_id: str, message: dict):
        """특정 사용자에게 메시지 전송"""
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message)

    async def broadcast_to_room(self, member_ids: list[str], message: dict):
        """채팅방 멤버들에게 메시지 브로드캐스트"""
        for user_id in member_ids:
            if user_id in self.active_connections:
                await self.active_connections[user_id].send_json(message)

    def get_connection_count(self) -> int:
        """현재 연결 수 반환"""
        return len(self.active_connections)


# 전역 연결 관리자 인스턴스
manager = ConnectionManager()
