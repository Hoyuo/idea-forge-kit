# /forge:status - Check Project Status

## Usage

```
/forge:status
/forge:status AUTH-001
```

## Input

`$ARGUMENTS` - (Optional) Specific PRD ID. If omitted, shows overall project status

## Language Configuration

Read from `.forge/config.json`:
- Use `language.conversation` for status display language

## Workflow

### 1. Overall Project Status (No PRD ID)

```
IdeaForge Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project: {PROJECT_NAME}
Location: {CWD}

┌─ PRD Overview ────────────────────────────────┐
│                                               │
│  ID        Title              Status    Prog  │
│  ────────  ─────────────────  ────────  ────  │
│  AUTH-001  User Auth System   🔨 build  45%   │
│  CHAT-002  Real-time Chat     📝 draft   0%   │
│  API-003   REST API Design    ✓ done   100%   │
│                                               │
└───────────────────────────────────────────────┘

Summary:
   Total PRDs: 3
   ├── Draft: 1
   ├── Analyzed: 0
   ├── Building: 1
   └── Done: 1

Quick Actions:
   /forge:idea "new idea"      - Create new PRD
   /forge:build AUTH-001       - Continue build
   /forge:status AUTH-001      - Detailed status
```

### 2. Specific PRD Status (With PRD ID)

```
IdeaForge Status: AUTH-001
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRD: User Authentication System
Status: Building (45%)
Created: 2024-11-30
Active: 2h 15m

┌─ Phase Progress ──────────────────────────────┐
│                                               │
│  [✓] Idea    → PRD created                    │
│  [✓] Analyze → 3 agents generated             │
│  [~] Build   → 2/5 tasks completed            │
│  [ ] Verify  → Pending                        │
│                                               │
└───────────────────────────────────────────────┘

┌─ Task Breakdown ──────────────────────────────┐
│                                               │
│  ✓ FR-001  Email login         [backend]  Done│
│  ✓ FR-002  OAuth integration   [backend]  Done│
│  ~ FR-003  Password reset      [backend]  50% │
│  ◯ FR-004  Session management  [backend]  -   │
│  ◯ NFR-001 Response time opt   [devops]   -   │
│                                               │
└───────────────────────────────────────────────┘

┌─ Active Agents ───────────────────────────────┐
│                                               │
│  🤖 expert-backend    Working on FR-003       │
│  💤 expert-security   Waiting                 │
│  💤 expert-devops     Waiting                 │
│                                               │
└───────────────────────────────────────────────┘

┌─ Test Summary ────────────────────────────────┐
│                                               │
│  Tests:    12 passed, 0 failed                │
│  Coverage: 78%                                │
│  Files:    4 created, 2 modified              │
│                                               │
└───────────────────────────────────────────────┘

Actions:
   /forge:build AUTH-001    - Continue build
   /forge:resume AUTH-001   - Resume from checkpoint
   /forge:verify AUTH-001   - Run verification
```

### 3. Information Sources

Status information collected from:

- `.forge/prds/{ID}.md` - PRD metadata
- `.forge/tasks/{ID}/tasks.json` - Task status
- `.forge/progress/{ID}/checkpoint.json` - Progress
- `.forge/agents/{ID}/` - Generated agents

### 4. Status Codes

| Status | Icon | Description |
|--------|------|-------------|
| draft | 📝 | PRD created, not analyzed |
| analyzed | 🔍 | Analysis complete, not built |
| building | 🔨 | TDD implementation in progress |
| paused | ⏸️ | Paused |
| failed | ✗ | Failed (retry needed) |
| done | ✓ | Complete |
