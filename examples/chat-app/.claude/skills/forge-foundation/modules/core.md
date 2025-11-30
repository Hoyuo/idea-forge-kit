# IdeaForge Core Module

> Core workflow rules and execution patterns.

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    IdeaForge Workflow                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  /forge:idea "idea"                                         │
│       ↓                                                     │
│  ┌─────────────────┐                                        │
│  │   PRD Document  │  .forge/prds/{ID}.md                   │
│  └────────┬────────┘                                        │
│           ↓                                                 │
│  /forge:analyze {ID}                                        │
│       ↓                                                     │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │  Task Breakdown │  │ Dynamic Agents  │                   │
│  └────────┬────────┘  └────────┬────────┘                   │
│           ↓                    ↓                            │
│  /forge:design {ID}                                         │
│       ↓                                                     │
│  ┌─────────────────┐                                        │
│  │   Diagrams      │  .forge/design/{ID}/                   │
│  └────────┬────────┘                                        │
│           ↓                                                 │
│  /forge:build {ID}                                          │
│       ↓                                                     │
│  ┌─────────────────────────────────────────┐                │
│  │  TDD Cycle (per task)                   │                │
│  │  🔴 RED → 🟢 GREEN → 🔵 REFACTOR        │                │
│  └────────┬────────────────────────────────┘                │
│           ↓                                                 │
│  /forge:verify {ID}                                         │
│       ↓                                                     │
│  ┌─────────────────┐                                        │
│  │ Quality Report  │  .forge/reports/{ID}-*.md              │
│  └────────┬────────┘                                        │
│           ↓                                                 │
│  /forge:sync {ID}                                           │
│       ↓                                                     │
│  ┌─────────────────┐                                        │
│  │  Documentation  │  README, CHANGELOG, docs/              │
│  └─────────────────┘                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Command Reference

| Command | Input | Output | Agent |
|---------|-------|--------|-------|
| `/forge:idea` | "idea description" | PRD document | forge-prd-writer |
| `/forge:analyze` | PRD_ID | Tasks + Agents | forge-analyzer |
| `/forge:design` | PRD_ID | PlantUML diagrams | forge-designer |
| `/forge:build` | PRD_ID | Implementation | forge-tdd-runner |
| `/forge:verify` | PRD_ID | Quality report | forge-quality |
| `/forge:sync` | PRD_ID | Documentation | forge-sync |
| `/forge:dashboard` | - | Web server | - |
| `/forge:status` | - | Current state | - |
| `/forge:list` | - | All PRDs | - |
| `/forge:resume` | PRD_ID | Continue work | - |
| `/forge:help` | - | Help text | - |

---

## Directory Structure

```
project/
├── .forge/
│   ├── prds/                    # PRD documents
│   │   └── {ID}.md
│   ├── tasks/                   # Task breakdown
│   │   └── {ID}/
│   │       └── tasks.json
│   ├── agents/                  # Dynamic agents
│   │   └── {ID}/
│   │       └── {agent}.md
│   ├── progress/                # Checkpoints
│   │   └── {ID}/
│   │       └── checkpoint.json
│   ├── design/                  # Diagrams
│   │   └── {ID}/
│   │       ├── diagrams/
│   │       └── DESIGN.md
│   ├── reports/                 # Quality reports
│   │   └── {ID}-*.md
│   ├── logs/                    # Execution logs
│   ├── dashboard/               # Web server
│   └── config.json              # Configuration
│
├── .claude/
│   ├── agents/forge/            # Base agents
│   ├── commands/forge/          # Slash commands
│   ├── skills/                  # Skills
│   │   ├── forge-foundation/    # This skill
│   │   └── forge-patterns/      # Development patterns
│   └── settings.json            # Permissions
│
├── src/                         # Source code
├── tests/                       # Test files
└── CLAUDE.md                    # Project instructions
```

---

## Configuration Reference

`.forge/config.json` structure:

```json
{
  "version": "0.2.0",
  "project": {
    "name": "project-name",
    "description": "description",
    "language": "python|typescript|go|...",
    "framework": "fastapi|nextjs|gin|..."
  },
  "language": {
    "conversation": "ko|en|ja|zh",
    "output_documents": "ko|en|ja|zh"
  },
  "workflow": {
    "auto_agent_generation": true,
    "tdd_enabled": true,
    "checkpoint_enabled": true,
    "test_coverage_target": 80
  },
  "git_strategy": {
    "mode": "manual|personal|team"
  },
  "document_management": {
    "enabled": true,
    "auto_sync": false
  },
  "dashboard": {
    "enabled": true,
    "port": 20555
  }
}
```

---

## Execution Rules

### Rule 1: Config First
Always read `.forge/config.json` before any operation.

### Rule 2: Sequential Workflow
Follow the workflow order. Don't skip steps.

### Rule 3: Checkpoint Always
Save checkpoint after every significant operation.

### Rule 4: Quality Gates
All code must pass quality gates before completion.

### Rule 5: Documentation Sync
Run `/forge:sync` after implementation to update docs.

---

## Error Handling

| Error | Action |
|-------|--------|
| PRD not found | Check `.forge/prds/` directory |
| Checkpoint missing | Start from beginning or last known state |
| Test failure | Continue TDD cycle (GREEN phase) |
| Coverage below target | Add more tests |
| Git conflict | Resolve manually, then continue |
