"""온라인 상태 관리 모듈"""


class OnlineStatusManager:
    """사용자 온라인 상태를 관리하는 클래스"""

    def __init__(self):
        self._online_users: set[str] = set()

    def set_online(self, user_id: str) -> None:
        """사용자를 온라인 상태로 설정"""
        self._online_users.add(user_id)

    def set_offline(self, user_id: str) -> None:
        """사용자를 오프라인 상태로 설정"""
        self._online_users.discard(user_id)

    def is_online(self, user_id: str) -> bool:
        """사용자의 온라인 여부 확인"""
        return user_id in self._online_users

    def get_online_users(self) -> list[str]:
        """현재 온라인인 모든 사용자 목록 반환"""
        return list(self._online_users)

    def get_online_from_list(self, user_ids: list[str]) -> list[str]:
        """주어진 사용자 목록 중 온라인인 사용자만 반환"""
        return [uid for uid in user_ids if uid in self._online_users]


# 전역 인스턴스
status_manager = OnlineStatusManager()
