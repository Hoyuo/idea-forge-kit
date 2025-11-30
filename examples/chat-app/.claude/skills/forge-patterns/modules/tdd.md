# TDD Workflow Patterns

> RED → GREEN → REFACTOR cycle for test-driven development.

---

## 1. RED Phase - Write Failing Tests First

```
1. Create test file in tests/ directory
2. Write test cases based on requirements
3. Run tests → Verify they FAIL
4. Proceed to GREEN phase only after tests fail
```

**Test Structure (AAA Pattern):**
```
test_function_name_scenario():
    // Arrange - Setup test data
    input = create_test_data()
    expected = define_expected_result()

    // Act - Execute the function
    result = function_under_test(input)

    // Assert - Verify the result
    assert result == expected
```

**Test Naming Convention:**
```
test_<unit>_<scenario>_<expected>

Examples:
- test_login_valid_credentials_returns_token
- test_login_invalid_password_throws_error
- test_create_user_duplicate_email_returns_conflict
```

---

## 2. GREEN Phase - Minimal Implementation

```
1. Write MINIMUM code to pass the failing test
2. Do NOT add extra features
3. Do NOT optimize yet
4. Run tests → Verify they PASS
5. Proceed to REFACTOR phase
```

**Guidelines:**
- Focus only on making the test pass
- Hardcode values if necessary (will refactor later)
- Avoid premature optimization
- One test at a time

---

## 3. REFACTOR Phase - Improve Code Quality

**Checklist:**
- [ ] Remove duplicate code (DRY)
- [ ] Rename for clarity (meaningful names)
- [ ] Extract functions (single responsibility)
- [ ] Add type annotations/hints
- [ ] Write documentation/comments
- [ ] **Re-run ALL tests → Must still pass**

**Refactoring Techniques:**

| Technique | Description |
|-----------|-------------|
| Extract Method | Move code block to separate function |
| Rename | Improve variable/function names |
| Inline | Replace variable with its value |
| Replace Magic Number | Use named constants |
| Introduce Parameter Object | Group related parameters |

---

## IdeaForge TDD Integration

### PRD to Implementation Flow

```
PRD Analysis → Task Decomposition → TDD Cycle → Verification

For each task:
  1. RED: Write failing test from PRD requirement
  2. GREEN: Implement minimum code to pass
  3. REFACTOR: Improve code quality
  4. Verify: Check against PRD acceptance criteria
```

### Checkpoint Pattern

```
Checkpoint: {PRD_ID}
─────────────────────────────────────
current_task  : {TASK_ID}
current_phase : RED | GREEN | REFACTOR
completed     : [{TASK_IDs}]
pending       : [{TASK_IDs}]
test_summary:
  total       : {count}
  passed      : {count}
  failed      : {count}
  coverage    : {percent}
```

### Status Indicators

| Phase | Indicator | Meaning |
|-------|-----------|---------|
| RED | 🔴 | Writing/running failing tests |
| GREEN | 🟢 | Implementing to pass tests |
| REFACTOR | 🔵 | Improving code quality |
| Complete | ✅ | Task finished |
| Pending | ⏳ | Waiting to start |
