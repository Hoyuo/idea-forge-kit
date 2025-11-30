# IdeaForge Foundation Skill

> **Core knowledge base** for IdeaForge workflow execution.
> Modular structure for efficient token usage.

---

## Quick Reference

| Module | Content | When to Load |
|--------|---------|--------------|
| [core.md](modules/core.md) | Workflow rules, agent catalog | Always (first load) |
| [tdd.md](modules/tdd.md) | TDD patterns, RED-GREEN-REFACTOR | During `/forge:build` |
| [quality.md](modules/quality.md) | Quality gates, testing standards | During `/forge:verify` |
| [git.md](modules/git.md) | Git 3-Mode, commit conventions | Git operations |
| [agents.md](modules/agents.md) | Full agent reference | Agent selection |

---

## Module Overview

### Core (`modules/core.md`)
- IdeaForge workflow overview
- Command reference
- Execution rules
- Configuration guide

### TDD (`modules/tdd.md`)
- RED-GREEN-REFACTOR cycle
- Test writing patterns
- Checkpoint management
- Phase transitions

### Quality (`modules/quality.md`)
- Quality gates (80% coverage)
- Lint and type checking
- Security scanning
- Report generation

### Git (`modules/git.md`)
- 3-Mode System (manual/personal/team)
- Conventional Commits
- Branch management
- PR creation

### Agents (`modules/agents.md`)
- Core agents (4)
- Manager agents (4)
- Dynamic agents (5)
- Agent selection guide

---

## IdeaForge Workflow

```
/forge:idea     → PRD Generation
/forge:analyze  → Agent + Task Generation
/forge:design   → Architecture Diagrams
/forge:build    → TDD Implementation
/forge:verify   → Quality Verification
/forge:sync     → Documentation Sync
```

---

## Loading Modules

Load only what you need:

```
# For TDD implementation
Read modules/tdd.md

# For quality checks
Read modules/quality.md

# For Git operations
Read modules/git.md

# For agent selection
Read modules/agents.md
```

This modular approach saves tokens by loading only what's needed.

---

## Essential Rules

### Rule 1: Always Use Checkpoint
Save progress after each TDD phase to `.forge/progress/{ID}/checkpoint.json`.

### Rule 2: Follow TDD Strictly
Never skip phases: RED → GREEN → REFACTOR

### Rule 3: Meet Quality Gates
- Test coverage: ≥80%
- Lint errors: 0
- Type errors: 0

### Rule 4: Use Config
Read settings from `.forge/config.json` before operations.

### Rule 5: Language Awareness
Respect `language.conversation` and `language.output_documents` settings.
