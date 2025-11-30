#!/usr/bin/env python3
"""
IdeaForge Session End Hook

Executes when Claude Code session ends.
- Saves session metrics
- Checks for uncommitted changes
- Cleans up temporary files
- Displays session summary
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

try:
    from config import ConfigManager
    from checkpoint import CheckpointManager
    from paths import PathUtils
except ImportError:
    # Fallback if lib not available
    ConfigManager = None
    CheckpointManager = None
    PathUtils = None


def get_project_dir() -> Path:
    """Get project directory from environment or current directory."""
    return Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))


def get_git_status() -> dict:
    """Get Git repository status."""
    try:
        # Check if git repo
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            check=True,
            cwd=get_project_dir(),
        )

        # Get uncommitted changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=get_project_dir(),
        )

        changes = result.stdout.strip().split("\n") if result.stdout.strip() else []

        return {
            "is_repo": True,
            "uncommitted_count": len(changes),
            "uncommitted_files": changes[:10],  # Limit to 10
        }
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {"is_repo": False, "uncommitted_count": 0, "uncommitted_files": []}


def cleanup_temp_files(project_dir: Path, config: dict) -> int:
    """Clean up temporary files based on config.

    Returns:
        Number of files cleaned up
    """
    cleanup_config = config.get("document_management", {}).get("cleanup", {})

    if not cleanup_config.get("enabled", False):
        return 0

    targets = cleanup_config.get("targets", [".forge/logs/*", ".forge/reports/*.tmp"])
    cleaned = 0

    for pattern in targets:
        full_pattern = project_dir / pattern
        for file_path in full_pattern.parent.glob(full_pattern.name):
            if file_path.is_file():
                try:
                    file_path.unlink()
                    cleaned += 1
                except OSError:
                    pass

    return cleaned


def save_session_metrics(project_dir: Path, metrics: dict) -> None:
    """Save session metrics to logs directory."""
    logs_dir = project_dir / ".forge" / "logs" / "sessions"
    logs_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    metrics_file = logs_dir / f"session_{timestamp}.json"

    with open(metrics_file, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)


def get_session_summary(project_dir: Path) -> dict:
    """Get session summary from checkpoints."""
    if CheckpointManager:
        checkpoint_mgr = CheckpointManager(str(project_dir))
        return checkpoint_mgr.get_summary()

    # Fallback if lib not available
    return {
        "total_prds": 0,
        "completed": 0,
        "in_progress": 0,
        "pending": 0,
        "total_tests": 0,
        "passed_tests": 0,
        "test_pass_rate": 0,
    }


def main():
    """Main entry point for session end hook."""
    project_dir = get_project_dir()
    forge_dir = project_dir / ".forge"

    # Check if IdeaForge project
    if not forge_dir.exists():
        return

    # Load config
    config = {}
    config_path = forge_dir / "config.json"
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    # Get language
    lang = config.get("language", {}).get("conversation", "ko")

    # Gather metrics
    git_status = get_git_status()
    summary = get_session_summary(project_dir)
    cleaned_files = cleanup_temp_files(project_dir, config)

    # Build session metrics
    session_metrics = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "project": config.get("project", {}).get("name", ""),
        "summary": summary,
        "git": git_status,
        "cleanup": {"files_removed": cleaned_files},
    }

    # Save metrics
    save_session_metrics(project_dir, session_metrics)

    # Display summary
    print()
    print("━" * 50)

    if lang == "ko":
        print("🔥 IdeaForge 세션 종료")
        print("━" * 50)
        print()
        print(f"📊 세션 요약")
        print(f"   PRD: {summary['total_prds']}개 (완료: {summary['completed']}, 진행중: {summary['in_progress']})")
        print(f"   테스트: {summary['passed_tests']}/{summary['total_tests']} 통과")

        if git_status["is_repo"] and git_status["uncommitted_count"] > 0:
            print()
            print(f"⚠️  커밋되지 않은 변경사항: {git_status['uncommitted_count']}개")
            print("   git add . && git commit -m 'message' 로 커밋하세요")

        if cleaned_files > 0:
            print()
            print(f"🧹 정리된 임시 파일: {cleaned_files}개")
    else:
        print("🔥 IdeaForge Session End")
        print("━" * 50)
        print()
        print(f"📊 Session Summary")
        print(f"   PRDs: {summary['total_prds']} (Done: {summary['completed']}, Active: {summary['in_progress']})")
        print(f"   Tests: {summary['passed_tests']}/{summary['total_tests']} passed")

        if git_status["is_repo"] and git_status["uncommitted_count"] > 0:
            print()
            print(f"⚠️  Uncommitted changes: {git_status['uncommitted_count']}")
            print("   Run: git add . && git commit -m 'message'")

        if cleaned_files > 0:
            print()
            print(f"🧹 Temp files cleaned: {cleaned_files}")

    print()
    print("━" * 50)


if __name__ == "__main__":
    main()
