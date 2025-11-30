# /forge:feedback - Submit Feedback

## Usage

```
/forge:feedback "description"
/forge:feedback --type issue "bug description"
/forge:feedback --type suggestion "improvement idea"
/forge:feedback --type question "question about usage"
```

## Description

Submit feedback, report issues, or suggest improvements for IdeaForge.

Feedback is saved to `.forge/feedback/` for review and tracking.

## Types

| Type | Description | Example |
|------|-------------|---------|
| `issue` | Bug reports, errors | "TDD cycle doesn't save checkpoint" |
| `suggestion` | Feature requests, improvements | "Add support for Rust projects" |
| `question` | Usage questions, clarifications | "How to configure custom test commands" |

## Workflow

### 1. Submit Feedback

```
/forge:feedback "The /forge:design command doesn't generate ER diagrams"

Processing feedback...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type: suggestion (auto-detected)
Category: command

Feedback saved: .forge/feedback/FB-001.md
```

### 2. Review Feedback

Feedback is saved as markdown with metadata:

```markdown
---
id: FB-001
type: suggestion
category: command
status: open
created: 2025-11-30T12:00:00Z
---

# Feedback: FB-001

## Description

The /forge:design command doesn't generate ER diagrams

## Context

- PRD: CHAT-001 (if applicable)
- Command: /forge:design
- Phase: design

## Analysis

{Auto-generated analysis}

## Suggested Resolution

{Proposed solution}
```

### 3. Feedback Categories

| Category | Related To |
|----------|------------|
| `command` | Slash commands |
| `agent` | Agent behavior |
| `workflow` | Overall workflow |
| `config` | Configuration |
| `docs` | Documentation |
| `dashboard` | Dashboard UI |
| `other` | General |

## Options

- `--type {issue|suggestion|question}`: Feedback type (auto-detected if not specified)
- `--category {category}`: Feedback category
- `--prd {PRD_ID}`: Related PRD
- `--priority {low|medium|high}`: Priority level

## Output Structure

```
.forge/feedback/
├── FB-001.md
├── FB-002.md
└── index.json      # Feedback index
```

## Examples

### Report a Bug

```
/forge:feedback --type issue "Build fails when test file has spaces in name"
```

### Suggest Improvement

```
/forge:feedback --type suggestion "Add support for monorepo projects"
```

### Ask Question

```
/forge:feedback --type question "How to skip certain tests during TDD?"
```

## Integration

Feedback can be:
1. Reviewed locally in `.forge/feedback/`
2. Exported to GitHub Issues (future feature)
3. Used to improve IdeaForge

## Best Practices

1. **Be specific**: Include exact error messages or steps to reproduce
2. **Provide context**: Mention related PRD, command, or phase
3. **One item per feedback**: Don't combine multiple issues
4. **Check existing**: Review existing feedback before submitting duplicates
