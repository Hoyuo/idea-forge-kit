"""Template synchronization for IdeaForge upgrade system."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import NamedTuple


class SyncResult(NamedTuple):
    """템플릿 동기화 결과."""

    success: bool
    files_updated: int
    message: str


class TemplateSync:
    """IdeaForge 템플릿 동기화 관리자.

    패키지에 포함된 템플릿을 프로젝트에 동기화합니다.
    .forge/ 디렉토리의 사용자 데이터는 보존합니다.
    """

    # 템플릿 디렉토리 (패키지 내부)
    TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"

    # 동기화 대상
    SYNC_TARGETS = [
        ".claude",      # 에이전트, 명령어, 훅, 스킬
        "CLAUDE.md",    # 프로젝트 지시문
        ".mcp.json",    # MCP 서버 설정
    ]

    # .forge/ 내에서 보존해야 할 사용자 데이터
    PRESERVE_IN_FORGE = [
        "prds",         # PRD 문서
        "tasks",        # 태스크 분해 결과
        "agents",       # 동적 생성 에이전트
        "progress",     # 진행 상황
        "reports",      # 검증 리포트
    ]

    def __init__(self, project_path: Path):
        """초기화.

        Args:
            project_path: 프로젝트 루트 디렉토리 경로
        """
        self.project_path = project_path

    def sync(self) -> SyncResult:
        """템플릿 동기화 수행.

        Returns:
            SyncResult: 동기화 결과
        """
        if not self.TEMPLATES_DIR.exists():
            return SyncResult(
                success=False,
                files_updated=0,
                message=f"템플릿 디렉토리 없음: {self.TEMPLATES_DIR}",
            )

        files_updated = 0

        try:
            # .claude 디렉토리 동기화
            files_updated += self._sync_claude_directory()

            # CLAUDE.md 동기화
            files_updated += self._sync_file("CLAUDE.md")

            # .mcp.json 동기화
            files_updated += self._sync_file(".mcp.json")

            # .forge 디렉토리 구조 보장 (사용자 데이터 보존)
            self._ensure_forge_structure()

            return SyncResult(
                success=True,
                files_updated=files_updated,
                message="템플릿 동기화 완료",
            )

        except Exception as e:
            return SyncResult(
                success=False,
                files_updated=files_updated,
                message=f"템플릿 동기화 실패: {e}",
            )

    def _sync_claude_directory(self) -> int:
        """`.claude` 디렉토리 동기화.

        Returns:
            업데이트된 파일 수
        """
        src = self.TEMPLATES_DIR / ".claude"
        dst = self.project_path / ".claude"

        if not src.exists():
            return 0

        # 기존 .claude 디렉토리 삭제 후 복사
        if dst.exists():
            shutil.rmtree(dst)

        shutil.copytree(src, dst)

        # 파일 수 계산
        return sum(1 for _ in dst.rglob("*") if _.is_file())

    def _sync_file(self, filename: str) -> int:
        """단일 파일 동기화.

        Args:
            filename: 파일명

        Returns:
            1 (업데이트됨) 또는 0 (스킵)
        """
        src = self.TEMPLATES_DIR / filename
        dst = self.project_path / filename

        if not src.exists():
            return 0

        shutil.copy2(src, dst)
        return 1

    def _ensure_forge_structure(self) -> None:
        """.forge 디렉토리 구조 보장.

        템플릿에서 .forge 기본 구조를 복사하되,
        기존 사용자 데이터는 보존합니다.
        """
        src_forge = self.TEMPLATES_DIR / ".forge"
        dst_forge = self.project_path / ".forge"

        # .forge 디렉토리가 없으면 전체 복사
        if not dst_forge.exists():
            if src_forge.exists():
                shutil.copytree(src_forge, dst_forge)
            else:
                # 기본 구조 생성
                for subdir in self.PRESERVE_IN_FORGE:
                    (dst_forge / subdir).mkdir(parents=True, exist_ok=True)
            return

        # 기존 .forge가 있으면 config.json만 업데이트
        src_config = src_forge / "config.json"
        dst_config = dst_forge / "config.json"

        if src_config.exists() and not dst_config.exists():
            shutil.copy2(src_config, dst_config)

    def get_sync_preview(self) -> dict[str, list[str]]:
        """동기화될 파일 미리보기.

        Returns:
            카테고리별 파일 목록
        """
        preview: dict[str, list[str]] = {
            "update": [],
            "add": [],
            "preserve": [],
        }

        # .claude 내 파일들
        src_claude = self.TEMPLATES_DIR / ".claude"
        dst_claude = self.project_path / ".claude"

        if src_claude.exists():
            for src_file in src_claude.rglob("*"):
                if src_file.is_file():
                    rel_path = src_file.relative_to(self.TEMPLATES_DIR)
                    dst_file = self.project_path / rel_path

                    if dst_file.exists():
                        preview["update"].append(str(rel_path))
                    else:
                        preview["add"].append(str(rel_path))

        # .forge 내 보존 대상
        dst_forge = self.project_path / ".forge"
        if dst_forge.exists():
            for subdir in self.PRESERVE_IN_FORGE:
                subdir_path = dst_forge / subdir
                if subdir_path.exists():
                    for f in subdir_path.rglob("*"):
                        if f.is_file():
                            preview["preserve"].append(
                                str(f.relative_to(self.project_path))
                            )

        return preview
