#!/usr/bin/env python3
"""IdeaForge statusline hook - shows real-time build status."""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

TOOL_NAME = "IdeaForge"
TOOL_VERSION = "0.1.0"
TOOL_ICON = "🔥"

# TDD Phase icons
PHASE_ICONS = {
    "RED": "🔴",
    "GREEN": "🟢",
    "REFACTOR": "🔵",
    "completed": "✅",
    "pending": "⏳",
}


def read_session_context() -> dict:
    """Read JSON context from Claude Code via stdin."""
    try:
        if not sys.stdin.isatty():
            input_data = sys.stdin.read()
            if input_data:
                return json.loads(input_data)
        return {}
    except (json.JSONDecodeError, EOFError, ValueError):
        return {}


def get_git_branch() -> str:
    """Get current git branch name."""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=2,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return ""


def get_forge_status() -> dict:
    """Get detailed IdeaForge build status."""
    status = {
        "prd_id": "",
        "current_task": "",
        "task_title": "",
        "phase": "",
        "progress": 0,
        "completed": 0,
        "total": 0,
        "status": "idle",
    }

    progress_dir = Path.cwd() / ".forge" / "progress"
    if not progress_dir.exists():
        return status

    # Find active checkpoint
    for checkpoint_file in progress_dir.glob("*/checkpoint.json"):
        try:
            data = json.loads(checkpoint_file.read_text())
            prd_id = data.get("prd_id", "")

            completed_tasks = data.get("completed_tasks", [])
            pending_tasks = data.get("pending_tasks", [])
            current_task = data.get("current_task")
            current_phase = data.get("current_phase", "")

            total = len(completed_tasks) + len(pending_tasks)
            if current_task:
                total += 1

            status["prd_id"] = prd_id
            status["completed"] = len(completed_tasks)
            status["total"] = total
            status["progress"] = (len(completed_tasks) / max(total, 1)) * 100
            status["status"] = data.get("status", "building")

            if current_task:
                status["current_task"] = current_task
                status["phase"] = current_phase

                # Try to get task title from tasks.json
                tasks_file = Path.cwd() / ".forge" / "tasks" / prd_id / "tasks.json"
                if tasks_file.exists():
                    try:
                        tasks_data = json.loads(tasks_file.read_text())
                        for task in tasks_data.get("tasks", []):
                            if task.get("id") == current_task:
                                status["task_title"] = task.get("title", "")[:20]
                                break
                    except (json.JSONDecodeError, IOError):
                        pass

            # Return first active checkpoint found
            if current_task or status["status"] != "idle":
                return status

        except (json.JSONDecodeError, IOError):
            pass

    return status


def format_forge_status(status: dict) -> str:
    """Format forge status for statusline display."""
    if not status["prd_id"]:
        return ""

    parts = []

    # PRD ID
    parts.append(status["prd_id"])

    # Current task and phase
    if status["current_task"]:
        phase_icon = PHASE_ICONS.get(status["phase"], "⏳")
        task_display = status["current_task"]
        if status["task_title"]:
            task_display += f" {status['task_title']}"
        parts.append(f"{phase_icon} {task_display}")
    elif status["status"] == "core_features_complete":
        parts.append("✅ Core Complete")
    elif status["status"] == "completed":
        parts.append("✅ Done")

    # Progress
    parts.append(f"{status['completed']}/{status['total']} ({status['progress']:.0f}%)")

    return " | ".join(parts)


def main():
    """Generate statusline output."""
    context = read_session_context()

    # Model info from context
    model_info = context.get("model", {})
    model_name = model_info.get("display_name") or model_info.get("name") or "Claude"

    # Current time
    current_time = datetime.now().strftime("%H:%M")

    # Git branch
    branch = get_git_branch()

    # Forge status (detailed)
    forge_status = get_forge_status()
    forge_display = format_forge_status(forge_status)

    # Build status line
    parts = []

    # Tool icon and version
    parts.append(f"{TOOL_ICON} {TOOL_NAME}")

    # Forge build status (most important - show prominently)
    if forge_display:
        parts.append(f"📋 {forge_display}")
    else:
        parts.append("💤 No active build")

    # Branch
    if branch:
        parts.append(f"🔀 {branch}")

    # Time
    parts.append(f"⏰ {current_time}")

    print(" | ".join(parts))


if __name__ == "__main__":
    main()
