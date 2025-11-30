"""Backup management for IdeaForge upgrade system."""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import NamedTuple


class BackupResult(NamedTuple):
    """백업 결과."""

    success: bool
    backup_path: Path | None
    message: str


class BackupManager:
    """IdeaForge 프로젝트 백업 관리자.

    업그레이드 전 .claude 디렉토리를 백업하고,
    실패 시 롤백할 수 있습니다.
    """

    def __init__(self, project_path: Path):
        """초기화.

        Args:
            project_path: 프로젝트 루트 디렉토리 경로
        """
        self.project_path = project_path
        self.claude_dir = project_path / ".claude"
        self.forge_dir = project_path / ".forge"
        self.backup_base = project_path / ".forge-backups"

    def _generate_backup_name(self) -> str:
        """타임스탬프 기반 백업 디렉토리 이름 생성."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"backup_{timestamp}"

    def has_existing_files(self) -> bool:
        """백업할 파일이 있는지 확인.

        Returns:
            .claude 디렉토리가 존재하면 True
        """
        return self.claude_dir.exists()

    def create_backup(self) -> BackupResult:
        """백업 생성.

        .claude 디렉토리를 .forge-backups/ 아래에 복사합니다.

        Returns:
            BackupResult: 백업 결과
        """
        if not self.has_existing_files():
            return BackupResult(
                success=True,
                backup_path=None,
                message="백업할 파일 없음",
            )

        try:
            # 백업 디렉토리 생성
            backup_name = self._generate_backup_name()
            backup_path = self.backup_base / backup_name
            backup_path.mkdir(parents=True, exist_ok=True)

            # .claude 디렉토리 백업
            if self.claude_dir.exists():
                shutil.copytree(
                    self.claude_dir,
                    backup_path / ".claude",
                    dirs_exist_ok=True,
                )

            # CLAUDE.md 백업
            claude_md = self.project_path / "CLAUDE.md"
            if claude_md.exists():
                shutil.copy2(claude_md, backup_path / "CLAUDE.md")

            # .mcp.json 백업
            mcp_json = self.project_path / ".mcp.json"
            if mcp_json.exists():
                shutil.copy2(mcp_json, backup_path / ".mcp.json")

            return BackupResult(
                success=True,
                backup_path=backup_path,
                message=f"백업 완료: {backup_path.name}",
            )

        except Exception as e:
            return BackupResult(
                success=False,
                backup_path=None,
                message=f"백업 실패: {e}",
            )

    def restore_backup(self, backup_path: Path) -> BackupResult:
        """백업에서 복원.

        Args:
            backup_path: 복원할 백업 디렉토리 경로

        Returns:
            BackupResult: 복원 결과
        """
        if not backup_path.exists():
            return BackupResult(
                success=False,
                backup_path=backup_path,
                message=f"백업 디렉토리 없음: {backup_path}",
            )

        try:
            # .claude 디렉토리 복원
            backup_claude = backup_path / ".claude"
            if backup_claude.exists():
                if self.claude_dir.exists():
                    shutil.rmtree(self.claude_dir)
                shutil.copytree(backup_claude, self.claude_dir)

            # CLAUDE.md 복원
            backup_claude_md = backup_path / "CLAUDE.md"
            if backup_claude_md.exists():
                shutil.copy2(backup_claude_md, self.project_path / "CLAUDE.md")

            # .mcp.json 복원
            backup_mcp = backup_path / ".mcp.json"
            if backup_mcp.exists():
                shutil.copy2(backup_mcp, self.project_path / ".mcp.json")

            return BackupResult(
                success=True,
                backup_path=backup_path,
                message="복원 완료",
            )

        except Exception as e:
            return BackupResult(
                success=False,
                backup_path=backup_path,
                message=f"복원 실패: {e}",
            )

    def list_backups(self) -> list[Path]:
        """사용 가능한 백업 목록 반환.

        Returns:
            백업 디렉토리 경로 목록 (최신순)
        """
        if not self.backup_base.exists():
            return []

        backups = [
            d for d in self.backup_base.iterdir()
            if d.is_dir() and d.name.startswith("backup_")
        ]
        return sorted(backups, reverse=True)

    def cleanup_old_backups(self, keep_count: int = 5) -> int:
        """오래된 백업 정리.

        Args:
            keep_count: 유지할 백업 개수

        Returns:
            삭제된 백업 개수
        """
        backups = self.list_backups()
        if len(backups) <= keep_count:
            return 0

        to_delete = backups[keep_count:]
        deleted = 0

        for backup in to_delete:
            try:
                shutil.rmtree(backup)
                deleted += 1
            except Exception:
                pass

        return deleted
