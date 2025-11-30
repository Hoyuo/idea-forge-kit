"""Upgrade system for IdeaForge projects.

3-Stage Upgrade Workflow:
  Stage 1: Version Check - Compare current vs package template_version
  Stage 2: Backup - Create timestamped backup of existing files
  Stage 3: Template Sync - Copy new templates with rollback support
"""

from .version_checker import VersionChecker
from .backup_manager import BackupManager
from .template_sync import TemplateSync

__all__ = ["VersionChecker", "BackupManager", "TemplateSync"]
