# IdeaForge TDD Module

> Test-Driven Development patterns and execution rules.

---

## TDD Cycle Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     TDD Cycle                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│    🔴 RED Phase                                             │
│    ┌─────────────────────────────────────────┐              │
│    │ 1. Write test for new feature           │              │
│    │ 2. Run test → MUST FAIL                 │              │
│    │ 3. Verify failure is expected           │              │
│    └─────────────────┬───────────────────────┘              │
│                      ↓                                      │
│    🟢 GREEN Phase                                           │
│    ┌─────────────────────────────────────────┐              │
│    │ 1. Write MINIMAL code to pass           │              │
│    │ 2. Run test → MUST PASS                 │              │
│    │ 3. All existing tests must pass         │              │
│    └─────────────────┬───────────────────────┘              │
│                      ↓                                      │
│    🔵 REFACTOR Phase                                        │
│    ┌─────────────────────────────────────────┐              │
│    │ 1. Improve code quality                 │              │
│    │ 2. Remove duplication                   │              │
│    │ 3. Run tests → ALL MUST PASS            │              │
│    └─────────────────┬───────────────────────┘              │
│                      ↓                                      │
│    ✅ COMPLETE → Next Task                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase Details

### 🔴 RED Phase

**Goal**: Write a failing test that defines expected behavior.

**Steps**:
1. Understand the requirement from task description
2. Write test code (unit/integration as appropriate)
3. Run test and verify it FAILS
4. Failure should be for the RIGHT reason (not syntax error)

**Checkpoint**:
```json
{
  "current_task": "TASK-001",
  "current_phase": "red",
  "test_file": "tests/test_feature.py",
  "test_status": "failing"
}
```

**Output**:
```
🔴 RED Phase: TASK-001
━━━━━━━━━━━━━━━━━━━━━━━━

Test written: tests/test_feature.py::test_login_success

Running test...
FAILED (expected)

Failure reason: Function not implemented
→ Proceeding to GREEN phase
```

---

### 🟢 GREEN Phase

**Goal**: Write minimal code to make the test pass.

**Rules**:
- Write ONLY enough code to pass the test
- Don't optimize or clean up yet
- Don't add features not tested
- Keep it simple

**Steps**:
1. Implement minimal code
2. Run the new test → MUST PASS
3. Run ALL tests → ALL MUST PASS
4. If any test fails, fix before proceeding

**Checkpoint**:
```json
{
  "current_task": "TASK-001",
  "current_phase": "green",
  "implementation_file": "src/feature.py",
  "test_status": "passing"
}
```

**Output**:
```
🟢 GREEN Phase: TASK-001
━━━━━━━━━━━━━━━━━━━━━━━━

Implementation: src/auth/login.py

Running tests...
✅ test_login_success PASSED
✅ All 15 tests PASSED

→ Proceeding to REFACTOR phase
```

---

### 🔵 REFACTOR Phase

**Goal**: Improve code quality while keeping tests passing.

**Activities**:
- Remove code duplication
- Improve naming
- Extract functions/classes
- Optimize performance
- Add docstrings/comments

**Rules**:
- Run tests after EVERY change
- If test fails, undo last change
- Don't add new features

**Checkpoint**:
```json
{
  "current_task": "TASK-001",
  "current_phase": "refactor",
  "refactored": true,
  "test_status": "passing"
}
```

**Output**:
```
🔵 REFACTOR Phase: TASK-001
━━━━━━━━━━━━━━━━━━━━━━━━━━

Refactoring: src/auth/login.py

Changes:
├── Extracted validate_credentials()
├── Added type hints
└── Improved error messages

Running tests...
✅ All 15 tests PASSED

→ Task TASK-001 COMPLETE
```

---

## Test Patterns

### Unit Test Template

```python
# tests/test_{module}.py

import pytest
from src.{module} import {function}

class Test{Feature}:
    """Tests for {feature} functionality."""

    def test_{action}_success(self):
        """Test successful {action}."""
        # Arrange
        input_data = {...}
        expected = {...}

        # Act
        result = {function}(input_data)

        # Assert
        assert result == expected

    def test_{action}_failure(self):
        """Test {action} with invalid input."""
        # Arrange
        invalid_input = {...}

        # Act & Assert
        with pytest.raises(ValueError):
            {function}(invalid_input)

    def test_{action}_edge_case(self):
        """Test {action} edge case."""
        # Test boundary conditions
        pass
```

### Integration Test Template

```python
# tests/integration/test_{feature}.py

import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

class Test{Feature}Integration:
    """Integration tests for {feature}."""

    def test_{endpoint}_success(self):
        """Test {endpoint} returns expected response."""
        response = client.post(
            "/api/{endpoint}",
            json={...}
        )

        assert response.status_code == 200
        assert response.json()["success"] == True
```

---

## Checkpoint Management

### Checkpoint Structure

```json
{
  "prd_id": "CHAT-001",
  "started_at": "2025-11-30T00:00:00Z",
  "current_task": "TASK-003",
  "current_phase": "green",
  "completed_tasks": ["TASK-001", "TASK-002"],
  "pending_tasks": ["TASK-003", "TASK-004", "TASK-005"],
  "test_summary": {
    "total": 25,
    "passed": 25,
    "failed": 0,
    "coverage": 85
  },
  "last_updated": "2025-11-30T01:30:00Z",
  "can_resume": true
}
```

### Save Checkpoint

Save after:
- Completing RED phase (test written)
- Completing GREEN phase (implementation done)
- Completing REFACTOR phase (task done)
- Any interruption

### Resume from Checkpoint

```
/forge:resume CHAT-001

Reading checkpoint...
━━━━━━━━━━━━━━━━━━━━━━━━

Last State:
├── Task: TASK-003
├── Phase: green
├── Completed: 2/5 tasks
└── Tests: 25 passing

Resuming from GREEN phase...
```

---

## Common Issues

### Test Won't Fail (RED Phase)

- Check if function already exists
- Verify test is actually calling the code
- Ensure assertions are correct

### Test Won't Pass (GREEN Phase)

- Check error message carefully
- Verify implementation matches test expectation
- Check for missing imports/dependencies

### Tests Break (REFACTOR Phase)

- Undo last change immediately
- Make smaller changes
- Run tests more frequently
