# /forge:resume - Resume Interrupted Work

## Usage

```
/forge:resume AUTH-001
```

## Input

`$ARGUMENTS` - PRD ID to resume

## Language Configuration

Read from `.forge/config.json`:
- Use `language.conversation` for resume messages and interactions

## Workflow

### 1. Checkpoint Check

```
Resuming: AUTH-001
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Checkpoint found!
```

Load checkpoint file: `.forge/progress/{PRD_ID}/checkpoint.json`

### 2. State Recovery

```
Previous State:
   ├── Last Task: FR-003 (Password Reset)
   ├── Last Phase: GREEN
   ├── Completed: FR-001, FR-002
   ├── Pending: FR-004, NFR-001
   └── Last Updated: 2024-11-30 15:30

Progress: ████████████░░░░░░░░░░░░░░░░ 45%
```

### 3. Resume Confirmation

Confirm with AskUserQuestion:

```
Resume work?

Options:
1. Continue from checkpoint (FR-003 GREEN phase)
2. Restart current task (FR-003 RED phase)
3. Skip to next task (FR-004)
4. Cancel
```

### 4. Resume Work

Based on selection, call `/forge:build`:

**Option 1: Continue from checkpoint**
```
Resuming from checkpoint...

Task: FR-003 Password Reset
Phase: GREEN (continue)

[Continue GREEN phase]
```

**Option 2: Restart task**
```
Restarting task FR-003...

Task: FR-003 Password Reset
Phase: RED (restart)

[TDD cycle from beginning]
```

**Option 3: Skip to next task**
```
Skipping to next task...

Skipped: FR-003 (marked as skipped)
Next: FR-004 Session Management

[Start from FR-004]
```

### 5. No Checkpoint Found

```
No checkpoint found for AUTH-001

Available Actions:
1. /forge:build AUTH-001    - Build from start
2. /forge:status AUTH-001   - Check status
```

### 6. Error Recovery

If interrupted due to previous failure:

```
Previous Error Detected:

Task: FR-003
Phase: GREEN
Error: Tests failed - 2 tests failing

Error Log: .forge/progress/AUTH-001/error.log

Options:
1. Review error log and retry
2. Fix manually and resume
3. Skip task
```

### 7. Save State After Resume

Update checkpoint after successful resume:

```json
{
  "prd_id": "AUTH-001",
  "resumed_at": "2024-11-30T16:00:00Z",
  "resumed_from": {
    "task": "FR-003",
    "phase": "GREEN"
  },
  "current_task": "FR-003",
  "current_phase": "REFACTOR",
  ...
}
```
