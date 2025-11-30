"""Version checking utilities for IdeaForge upgrade system."""

from __future__ import annotations

import json
from pathlib import Path
from typing import NamedTuple

from ideaforge import __version__


class VersionInfo(NamedTuple):
    """Version comparison result."""

    current: str  # 프로젝트에 설치된 템플릿 버전
    package: str  # 패키지에 포함된 템플릿 버전
    needs_upgrade: bool  # 업그레이드 필요 여부


class VersionChecker:
    """IdeaForge 프로젝트의 버전 체크 유틸리티.

    config.json의 template_version과 패키지 버전을 비교하여
    업그레이드 필요 여부를 판단합니다.
    """

    def __init__(self, project_path: Path):
        """초기화.

        Args:
            project_path: 프로젝트 루트 디렉토리 경로
        """
        self.project_path = project_path
        self.config_path = project_path / ".forge" / "config.json"

    def get_package_version(self) -> str:
        """패키지에 포함된 템플릿 버전 반환.

        Returns:
            현재 설치된 ideaforge 패키지 버전
        """
        return __version__

    def get_project_version(self) -> str:
        """프로젝트에 설치된 템플릿 버전 반환.

        Returns:
            config.json의 template_version, 없으면 "0.0.0"
        """
        if not self.config_path.exists():
            return "0.0.0"

        try:
            config = json.loads(self.config_path.read_text(encoding="utf-8"))
            return config.get("template_version", config.get("version", "0.0.0"))
        except (json.JSONDecodeError, KeyError):
            return "0.0.0"

    def compare_versions(self, v1: str, v2: str) -> int:
        """시맨틱 버전 비교.

        Args:
            v1: 첫 번째 버전
            v2: 두 번째 버전

        Returns:
            -1: v1 < v2
             0: v1 == v2
             1: v1 > v2
        """
        def parse_version(v: str) -> tuple[int, ...]:
            """버전 문자열을 튜플로 변환."""
            # v 접두어 제거
            v = v.lstrip("v")
            # 숫자만 추출
            parts = []
            for part in v.split("."):
                try:
                    parts.append(int(part.split("-")[0].split("+")[0]))
                except ValueError:
                    parts.append(0)
            # 최소 3개 요소 보장
            while len(parts) < 3:
                parts.append(0)
            return tuple(parts)

        v1_tuple = parse_version(v1)
        v2_tuple = parse_version(v2)

        if v1_tuple < v2_tuple:
            return -1
        elif v1_tuple > v2_tuple:
            return 1
        return 0

    def check(self) -> VersionInfo:
        """버전 체크 수행.

        Returns:
            VersionInfo: 현재 버전, 패키지 버전, 업그레이드 필요 여부
        """
        current = self.get_project_version()
        package = self.get_package_version()
        needs_upgrade = self.compare_versions(current, package) < 0

        return VersionInfo(
            current=current,
            package=package,
            needs_upgrade=needs_upgrade,
        )

    def update_project_version(self, version: str | None = None) -> None:
        """프로젝트 config.json의 template_version 업데이트.

        Args:
            version: 설정할 버전 (None이면 패키지 버전 사용)
        """
        if version is None:
            version = self.get_package_version()

        if not self.config_path.exists():
            return

        try:
            config = json.loads(self.config_path.read_text(encoding="utf-8"))
            config["template_version"] = version
            config["version"] = version  # 호환성을 위해 둘 다 업데이트
            self.config_path.write_text(
                json.dumps(config, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        except (json.JSONDecodeError, OSError):
            pass
