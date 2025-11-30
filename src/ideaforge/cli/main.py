"""Main CLI entry point for IdeaForge commands."""

import shutil
import subprocess
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from ideaforge import __version__

console = Console()

# Templates directory (installed with package)
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


def print_banner():
    """Print welcome banner."""
    console.print(Panel.fit(
        f"[bold white]Idea → Implement → Test → Done[/bold white]",
        title=f"[bold cyan]🔥 IdeaForge v{__version__}[/bold cyan]",
        border_style="cyan",
    ))


@click.group()
@click.version_option(version=__version__, prog_name="ideaforge")
def cli():
    """IdeaForge - AI-powered development kit.

    Transform ideas into implementation with auto-generated agents and TDD workflow.

    Commands:
      init     Initialize a new project with IdeaForge setup
      doctor   Check system requirements
      status   Show project status and active PRDs
    """
    pass


@cli.command()
@click.argument("path", type=click.Path(), default=".")
@click.option("--force", "-f", is_flag=True, help="Overwrite existing files")
def init(path: str, force: bool):
    """Initialize a new project with IdeaForge setup.

    Examples:
        forge init my-project
        forge init .
        forge init existing-project --force
    """
    print_banner()

    target_path = Path(path).resolve()

    # Create directory if it doesn't exist
    if not target_path.exists():
        target_path.mkdir(parents=True)
        console.print(f"[green]✓[/green] Created directory: {target_path.name}")

    # Check if already initialized
    forge_dir = target_path / ".forge"
    if forge_dir.exists() and not force:
        console.print(f"[yellow]⚠[/yellow] Project already initialized at {target_path}")
        console.print("  Use [bold]--force[/bold] to overwrite")
        return

    console.print(f"\n[bold]Initializing IdeaForge project:[/bold] {target_path.name}\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        # Step 1: Copy .claude directory
        task1 = progress.add_task("Setting up .claude/ directory...", total=1)
        src_claude = TEMPLATES_DIR / ".claude"
        dst_claude = target_path / ".claude"

        if dst_claude.exists() and force:
            shutil.rmtree(dst_claude)

        if src_claude.exists():
            shutil.copytree(src_claude, dst_claude, dirs_exist_ok=True)
        progress.update(task1, completed=1)

        # Step 2: Copy .forge directory
        task2 = progress.add_task("Setting up .forge/ directory...", total=1)
        src_forge = TEMPLATES_DIR / ".forge"
        dst_forge = target_path / ".forge"

        if dst_forge.exists() and force:
            shutil.rmtree(dst_forge)

        if src_forge.exists():
            shutil.copytree(src_forge, dst_forge, dirs_exist_ok=True)
        else:
            # Create basic structure if template doesn't exist
            (dst_forge / "prds").mkdir(parents=True, exist_ok=True)
            (dst_forge / "tasks").mkdir(parents=True, exist_ok=True)
            (dst_forge / "agents").mkdir(parents=True, exist_ok=True)
            (dst_forge / "progress").mkdir(parents=True, exist_ok=True)
            (dst_forge / "reports").mkdir(parents=True, exist_ok=True)
        progress.update(task2, completed=1)

        # Step 3: Copy CLAUDE.md
        task3 = progress.add_task("Copying CLAUDE.md...", total=1)
        src_claude_md = TEMPLATES_DIR / "CLAUDE.md"
        dst_claude_md = target_path / "CLAUDE.md"

        if src_claude_md.exists():
            shutil.copy2(src_claude_md, dst_claude_md)
        progress.update(task3, completed=1)

        # Step 4: Copy .mcp.json
        task4 = progress.add_task("Copying .mcp.json...", total=1)
        src_mcp = TEMPLATES_DIR / ".mcp.json"
        dst_mcp = target_path / ".mcp.json"

        if src_mcp.exists():
            shutil.copy2(src_mcp, dst_mcp)
        progress.update(task4, completed=1)

        # Step 5: Create .forge/config.json
        task5 = progress.add_task("Creating config...", total=1)
        config_path = dst_forge / "config.json"
        if not config_path.exists():
            config_content = f"""{{
  "version": "{__version__}",
  "template_version": "{__version__}",
  "project_name": "",
  "language": "ko",
  "auto_agent_generation": true,
  "tdd_enabled": true,
  "checkpoint_enabled": true
}}
"""
            config_path.write_text(config_content)
        progress.update(task5, completed=1)

    # Success message
    console.print("\n[bold green]✓ IdeaForge initialized successfully![/bold green]\n")

    # Show what was created
    table = Table(title="Created Files & Directories", show_header=True)
    table.add_column("Path", style="cyan")
    table.add_column("Description", style="white")

    table.add_row(".claude/agents/", "4 base agents (orchestrator, prd-writer, analyzer, tdd-runner)")
    table.add_row(".claude/commands/forge/", "7 commands (idea, analyze, build, verify, status, list, resume)")
    table.add_row(".claude/skills/", "1 skill (forge-patterns)")
    table.add_row(".claude/settings.json", "Permissions & hooks config")
    table.add_row(".forge/", "PRDs, tasks, agents, progress tracking")
    table.add_row(".mcp.json", "MCP servers (Context7, Sequential-Thinking)")
    table.add_row("CLAUDE.md", "Project instructions for Claude")

    console.print(table)

    # Next steps
    console.print("\n[bold]Next steps:[/bold]")
    console.print(f"  1. cd {target_path.name}")
    console.print("  2. claude")
    console.print("  3. /forge:idea \"your idea here\"\n")


@cli.command()
def doctor():
    """Check system requirements and configuration.

    Verifies:
      - Python version
      - Claude Code installation
      - Git installation
      - Node.js (for MCP servers)
    """
    print_banner()
    console.print("[bold]System Check[/bold]\n")

    checks = []

    # Python version
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    py_ok = sys.version_info >= (3, 10)
    checks.append(("Python", py_version, py_ok, ">=3.10 required"))

    # Claude Code
    try:
        result = subprocess.run(
            ["claude", "--version"], capture_output=True, text=True, timeout=5
        )
        claude_version = result.stdout.strip().split()[0] if result.returncode == 0 else "Not found"
        claude_ok = result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        claude_version = "Not found"
        claude_ok = False
    checks.append(("Claude Code", claude_version, claude_ok, "npm install -g @anthropic-ai/claude-code"))

    # Git
    try:
        result = subprocess.run(
            ["git", "--version"], capture_output=True, text=True, timeout=5
        )
        git_version = result.stdout.strip().replace("git version ", "") if result.returncode == 0 else "Not found"
        git_ok = result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        git_version = "Not found"
        git_ok = False
    checks.append(("Git", git_version, git_ok, "https://git-scm.com"))

    # Node.js (for MCP servers)
    try:
        result = subprocess.run(
            ["node", "--version"], capture_output=True, text=True, timeout=5
        )
        node_version = result.stdout.strip() if result.returncode == 0 else "Not found"
        node_ok = result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        node_version = "Not found"
        node_ok = False
    checks.append(("Node.js", node_version, node_ok, "Required for MCP servers"))

    # Display results
    table = Table(show_header=True)
    table.add_column("Component", style="cyan")
    table.add_column("Version", style="white")
    table.add_column("Status", style="white")

    all_ok = True
    for name, version, ok, hint in checks:
        status = "[green]✓[/green]" if ok else "[red]✗[/red]"
        if not ok:
            all_ok = False
            version = f"{version} ({hint})"
        table.add_row(name, version, status)

    console.print(table)

    if all_ok:
        console.print("\n[bold green]✓ All checks passed![/bold green]")
    else:
        console.print("\n[bold yellow]⚠ Some checks failed. Please install missing components.[/bold yellow]")


@cli.command()
def status():
    """Show current project status and active PRDs.

    Displays:
      - Active PRDs and their status
      - Current progress
      - Generated agents
    """
    print_banner()

    cwd = Path.cwd()
    forge_dir = cwd / ".forge"

    if not forge_dir.exists():
        console.print("[yellow]⚠ Not an IdeaForge project[/yellow]")
        console.print(f"  Run: [bold]forge init .[/bold] to initialize")
        return

    console.print(f"[bold]Project:[/bold] {cwd.name}\n")

    # Count PRDs
    prds_dir = forge_dir / "prds"
    prds = list(prds_dir.glob("*.md")) if prds_dir.exists() else []

    # Count generated agents
    agents_dir = forge_dir / "agents"
    agent_folders = [d for d in agents_dir.iterdir() if d.is_dir()] if agents_dir.exists() else []

    # Show PRD status
    table = Table(title="PRD Status", show_header=True)
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Status", style="white")
    table.add_column("Progress", style="white")

    if prds:
        for prd in prds:
            # Parse PRD frontmatter (simplified)
            content = prd.read_text()
            prd_id = prd.stem
            title = prd_id  # Simplified, would parse from content
            status_emoji = "📝"
            progress = "0%"
            table.add_row(prd_id, title, status_emoji, progress)
    else:
        table.add_row("-", "No PRDs yet", "-", "-")

    console.print(table)

    # Show summary
    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"  PRDs: {len(prds)}")
    console.print(f"  Generated Agent Sets: {len(agent_folders)}")

    # Show commands
    console.print("\n[bold]Commands:[/bold]")
    console.print("  /forge:idea <idea>     - Create new PRD from idea")
    console.print("  /forge:analyze <id>    - Analyze PRD and generate agents")
    console.print("  /forge:build <id>      - Start TDD implementation")
    console.print("  /forge:list            - List all PRDs\n")


@cli.command(name="list")
def list_prds():
    """List all PRDs in the project."""
    print_banner()

    cwd = Path.cwd()
    prds_dir = cwd / ".forge" / "prds"

    if not prds_dir.exists():
        console.print("[yellow]⚠ No PRDs found[/yellow]")
        console.print("  Run: [bold]/forge:idea \"your idea\"[/bold] to create one")
        return

    prds = list(prds_dir.glob("*.md"))

    if not prds:
        console.print("[yellow]⚠ No PRDs found[/yellow]")
        console.print("  Run: [bold]/forge:idea \"your idea\"[/bold] to create one")
        return

    table = Table(title="All PRDs", show_header=True)
    table.add_column("ID", style="cyan")
    table.add_column("Created", style="white")
    table.add_column("Size", style="dim")

    for prd in sorted(prds):
        stat = prd.stat()
        created = stat.st_mtime
        from datetime import datetime
        created_str = datetime.fromtimestamp(created).strftime("%Y-%m-%d %H:%M")
        size = f"{stat.st_size / 1024:.1f} KB"
        table.add_row(prd.stem, created_str, size)

    console.print(table)


@cli.command()
@click.option("--force", "-f", is_flag=True, help="강제 업그레이드 (버전 체크 무시)")
@click.option("--rollback", is_flag=True, help="마지막 백업으로 롤백")
def upgrade(force: bool, rollback: bool):
    """IdeaForge 템플릿을 최신 버전으로 업그레이드.

    3-Stage Workflow:
      Stage 1: 버전 체크 - 업그레이드 필요 여부 확인
      Stage 2: 백업 생성 - 롤백 지원
      Stage 3: 템플릿 동기화 - .claude/, CLAUDE.md, .mcp.json 업데이트

    사용자 데이터 보존:
      - .forge/prds/      PRD 문서
      - .forge/tasks/     태스크 분해 결과
      - .forge/agents/    동적 생성 에이전트
      - .forge/progress/  진행 상황
      - .forge/reports/   검증 리포트

    Examples:
        forge upgrade           # 일반 업그레이드
        forge upgrade --force   # 강제 업그레이드
        forge upgrade --rollback  # 마지막 백업으로 롤백
    """
    from ideaforge.core.upgrade import VersionChecker, BackupManager, TemplateSync

    print_banner()

    cwd = Path.cwd()
    forge_dir = cwd / ".forge"

    # 프로젝트 확인
    if not forge_dir.exists():
        console.print("[red]✗ IdeaForge 프로젝트가 아닙니다[/red]")
        console.print("  실행: [bold]forge init .[/bold]")
        return

    # 롤백 모드
    if rollback:
        _handle_rollback(cwd)
        return

    # Stage 1: 버전 체크
    console.print("[bold cyan]Stage 1:[/bold cyan] 버전 체크\n")

    checker = VersionChecker(cwd)
    version_info = checker.check()

    console.print(f"  현재 버전: [yellow]{version_info.current}[/yellow]")
    console.print(f"  패키지 버전: [green]{version_info.package}[/green]\n")

    if not version_info.needs_upgrade and not force:
        console.print("[green]✓ 이미 최신 버전입니다![/green]")
        return

    if not version_info.needs_upgrade and force:
        console.print("[yellow]⚠ 최신 버전이지만 --force로 강제 업그레이드합니다[/yellow]\n")

    # Stage 2: 백업
    console.print("[bold cyan]Stage 2:[/bold cyan] 백업 생성\n")

    backup_manager = BackupManager(cwd)
    backup_result = backup_manager.create_backup()

    if not backup_result.success:
        console.print(f"[red]✗ 백업 실패: {backup_result.message}[/red]")
        return

    if backup_result.backup_path:
        console.print(f"  [green]✓[/green] {backup_result.message}")
        console.print(f"  [dim]위치: {backup_result.backup_path.relative_to(cwd)}[/dim]\n")
    else:
        console.print(f"  [dim]{backup_result.message}[/dim]\n")

    # Stage 3: 템플릿 동기화
    console.print("[bold cyan]Stage 3:[/bold cyan] 템플릿 동기화\n")

    sync = TemplateSync(cwd)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("템플릿 동기화 중...", total=1)
        sync_result = sync.sync()
        progress.update(task, completed=1)

    if not sync_result.success:
        console.print(f"[red]✗ 동기화 실패: {sync_result.message}[/red]")

        # 롤백 시도
        if backup_result.backup_path:
            console.print("[yellow]⚠ 백업에서 복원 중...[/yellow]")
            restore_result = backup_manager.restore_backup(backup_result.backup_path)
            if restore_result.success:
                console.print("[green]✓ 복원 완료[/green]")
            else:
                console.print(f"[red]✗ 복원 실패: {restore_result.message}[/red]")
        return

    # 버전 업데이트
    checker.update_project_version()

    # 오래된 백업 정리
    deleted = backup_manager.cleanup_old_backups(keep_count=5)
    if deleted > 0:
        console.print(f"  [dim]오래된 백업 {deleted}개 정리됨[/dim]")

    # 성공 메시지
    console.print(f"\n[bold green]✓ v{version_info.package}으로 업그레이드 완료![/bold green]\n")

    console.print(f"  [dim]업데이트된 파일: {sync_result.files_updated}개[/dim]")
    if backup_result.backup_path:
        console.print(f"  [dim]백업 위치: {backup_result.backup_path.relative_to(cwd)}[/dim]")

    console.print("\n[bold]보존된 사용자 데이터:[/bold]")
    console.print("  • .forge/prds/      PRD 문서")
    console.print("  • .forge/tasks/     태스크 분해")
    console.print("  • .forge/agents/    동적 에이전트")
    console.print("  • .forge/progress/  진행 상황")

    console.print("\n[bold]다음 단계:[/bold]")
    console.print("  1. claude 실행")
    console.print("  2. /forge:status로 상태 확인")


def _handle_rollback(project_path: Path):
    """백업에서 롤백 처리."""
    from ideaforge.core.upgrade import BackupManager

    backup_manager = BackupManager(project_path)
    backups = backup_manager.list_backups()

    if not backups:
        console.print("[yellow]⚠ 사용 가능한 백업이 없습니다[/yellow]")
        return

    # 최신 백업으로 롤백
    latest_backup = backups[0]
    console.print(f"[bold]롤백 대상:[/bold] {latest_backup.name}\n")

    restore_result = backup_manager.restore_backup(latest_backup)

    if restore_result.success:
        console.print("[bold green]✓ 롤백 완료![/bold green]")
    else:
        console.print(f"[red]✗ 롤백 실패: {restore_result.message}[/red]")


if __name__ == "__main__":
    cli()
