# /forge:list - List All PRDs

## Usage

```
/forge:list
/forge:list --status building
/forge:list --sort date
```

## Language Configuration

Read from `.forge/config.json`:
- Use `language.conversation` for list display language

## Workflow

### 1. Display PRD List

Scan all PRDs in `.forge/prds/` directory.

```
IdeaForge PRD List
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌────────────────────────────────────────────────────────────┐
│  ID        Title                Status      Progress  Date │
├────────────────────────────────────────────────────────────┤
│  AUTH-001  User Auth System     🔨 building    45%   11/30 │
│  CHAT-002  Real-time Chat       📝 draft        0%   11/29 │
│  API-003   REST API Design      ✓ done        100%   11/28 │
│  UI-004    Dashboard UI         🔍 analyzed     0%   11/27 │
└────────────────────────────────────────────────────────────┘

Total: 4 PRDs
├── 📝 Draft: 1
├── 🔍 Analyzed: 1
├── 🔨 Building: 1
└── ✓ Done: 1

Actions:
   /forge:status {ID}    - Detailed status
   /forge:build {ID}     - Start/continue build
   /forge:idea "..."     - Create new PRD
```

### 2. Filter Options

**Filter by status**:
```
/forge:list --status draft
/forge:list --status building
/forge:list --status done
```

**Sort**:
```
/forge:list --sort date     # By date (default)
/forge:list --sort name     # By name
/forge:list --sort progress # By progress
```

### 3. PRD Metadata Parsing

Extract information from each PRD file's frontmatter:

```yaml
---
id: AUTH-001
title: "User Authentication System"
status: building
created: 2024-11-30
priority: high
---
```

### 4. Progress Calculation

From `.forge/tasks/{ID}/tasks.json`:
- Completed tasks / Total tasks × 100%

### 5. Empty List

```
IdeaForge PRD List
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(No PRDs found)

Get Started:
   /forge:idea "your idea"
```
