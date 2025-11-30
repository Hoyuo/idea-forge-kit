#!/usr/bin/env python3
"""IdeaForge session start hook - shows project info."""

import json
from pathlib import Path


def main():
    """Display project information at session start."""
    cwd = Path.cwd()
    forge_dir = cwd / ".forge"

    # Check if IdeaForge project
    if not forge_dir.exists():
        return

    # Count PRDs
    prds_dir = forge_dir / "prds"
    prds = list(prds_dir.glob("*.md")) if prds_dir.exists() else []

    # Check for active builds
    progress_dir = forge_dir / "progress"
    active_builds = []
    if progress_dir.exists():
        for checkpoint_file in progress_dir.glob("*/checkpoint.json"):
            try:
                data = json.loads(checkpoint_file.read_text())
                if data.get("current_task"):
                    active_builds.append(data.get("prd_id", "Unknown"))
            except (json.JSONDecodeError, IOError):
                pass

    # Output info (goes to Claude's context)
    print(f"IdeaForge Project: {cwd.name}")
    print(f"PRDs: {len(prds)}")
    if active_builds:
        print(f"Active Builds: {', '.join(active_builds)}")


if __name__ == "__main__":
    main()
