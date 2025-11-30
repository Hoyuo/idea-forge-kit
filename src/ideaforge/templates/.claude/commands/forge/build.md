# /forge:build - TDD Implementation Execution

## Usage

```
/forge:build AUTH-001
/forge:build CHAT-002 --task FR-003
```

## Input

`$ARGUMENTS` - PRD ID (optionally specify a specific task)

## Language Configuration

Read from `.forge/config.json`:
- Use `language.conversation` for progress messages and interaction

## Workflow

### 1. Preparation Phase

```
IdeaForge Build: {PRD_ID}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

1. Load `.forge/tasks/{PRD_ID}/tasks.json`
2. Check `.forge/progress/{PRD_ID}/checkpoint.json` (for resume)
3. Verify generated agents list

### 2. TDD Cycle

Execute RED-GREEN-REFACTOR for each task:

```
┌─────────────────────────────────────────────────┐
│  Task 1/5: FR-001 Email/Password Login          │
├─────────────────────────────────────────────────┤
│                                                 │
│  RED Phase                                      │
│  ├── Create test file: tests/test_auth.*       │
│  ├── Write test cases                          │
│  │   └── test_login_with_valid_credentials     │
│  │   └── test_login_with_invalid_password      │
│  │   └── test_login_with_nonexistent_user      │
│  └── Run tests → 3 failed ✓                    │
│                                                 │
│  GREEN Phase                                    │
│  ├── Create impl file: src/auth/login.*        │
│  ├── Write minimal implementation              │
│  └── Run tests → 3 passed ✓                    │
│                                                 │
│  REFACTOR Phase                                 │
│  ├── Code review and improvement               │
│  ├── Remove duplication                        │
│  └── Run tests → 3 passed ✓                    │
│                                                 │
│  Task Complete!                                 │
└─────────────────────────────────────────────────┘
```

### 3. Agent Delegation

Delegate to domain-appropriate agent for each task:

```
# Backend task delegation (language-agnostic)
Task(subagent_type="expert-backend", prompt="""
PRD: {PRD_ID}
Task: {TASK_ID} - {TASK_TITLE}

## TDD Phase: RED
1. Create test file in tests/ directory
2. Write test cases for requirements
3. Run tests to verify failure

## Requirements
{Requirements extracted from PRD}

## Tech Stack
{Tech stack from PRD - determines test runner}
""")
```

### 4. Checkpoint Saving

Auto-save on each task/phase completion:

`.forge/progress/{PRD_ID}/checkpoint.json`:
```json
{
  "prd_id": "AUTH-001",
  "started_at": "2024-11-30T10:00:00Z",
  "current_task": "FR-002",
  "current_phase": "GREEN",
  "completed_tasks": ["FR-001"],
  "pending_tasks": ["FR-003", "FR-004"],
  "test_summary": {
    "total": 8,
    "passed": 8,
    "failed": 0,
    "coverage": 85
  },
  "last_updated": "2024-11-30T11:30:00Z",
  "can_resume": true
}
```

### 5. Progress Display

Real-time progress:

```
Building: AUTH-001
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Progress: ████████████░░░░░░░░░░░░░░░░ 45%

Completed (2/5):
   ├── FR-001: Email login ✓
   └── FR-002: OAuth integration ✓

In Progress:
   └── FR-003: Password reset [GREEN phase]

Pending (2):
   ├── FR-004: Session management
   └── NFR-001: Response time optimization

Test Summary:
   Tests: 12 passed, 0 failed
   Coverage: 78%

Elapsed: 1h 23m
Est. Remaining: 1h 45m
```

### 6. Completion Message

```
Build Complete: {PRD_ID}

Summary:
   ├── Tasks: 5/5 completed
   ├── Tests: 24 passed, 0 failed
   ├── Coverage: 87%
   └── Duration: 3h 15m

Generated Files:
   ├── src/auth/login.py
   ├── src/auth/oauth.py
   ├── src/auth/password.py
   ├── tests/test_auth.py
   └── tests/test_oauth.py

Next Steps:
   /forge:verify {PRD_ID}  - Verify requirements
   /forge:status           - Check status
```

## Failure Handling

On test failure or error:

```
Build Interrupted: {PRD_ID}

Failure Location:
   Task: FR-003
   Phase: GREEN
   Error: Tests failed (2 tests)

Checkpoint Saved:
   .forge/progress/{PRD_ID}/checkpoint.json

Resolution Options:
   1. Check error log: .forge/progress/{PRD_ID}/error.log
   2. Fix manually and resume: /forge:resume {PRD_ID}
   3. Retry specific task: /forge:build {PRD_ID} --task FR-003
```

## Options

- `--task {TASK_ID}`: Execute specific task only
- `--skip-tests`: Skip tests (not recommended)
- `--verbose`: Detailed log output
