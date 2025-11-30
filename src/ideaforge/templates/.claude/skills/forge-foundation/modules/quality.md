# IdeaForge Quality Module

> Quality gates, testing standards, and verification patterns.

---

## Quality Gates

### Mandatory Gates

| Gate | Threshold | Action if Fail |
|------|-----------|----------------|
| Test Pass Rate | 100% | Fix failing tests |
| Code Coverage | ≥80% | Add more tests |
| Lint Errors | 0 | Fix lint issues |
| Type Errors | 0 | Fix type annotations |
| Security Issues | 0 | Fix vulnerabilities |

### Gate Execution Order

```
1. Run Tests         → All must pass
2. Check Coverage    → Must meet target
3. Run Linter        → No errors allowed
4. Run Type Checker  → No errors allowed
5. Security Scan     → No issues allowed
```

---

## Test Coverage

### Coverage Target

Default: **80%** (configurable in `.forge/config.json`)

```json
{
  "workflow": {
    "test_coverage_target": 80
  }
}
```

### Coverage Commands

**Python**:
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

**TypeScript**:
```bash
npm test -- --coverage
```

**Go**:
```bash
go test ./... -cover -coverprofile=coverage.out
go tool cover -func=coverage.out
```

### Coverage Report

```
Coverage Report: CHAT-001
━━━━━━━━━━━━━━━━━━━━━━━━━

Overall: 85%

File Coverage:
├── src/auth/login.py      92%
├── src/auth/token.py      88%
├── src/chat/room.py       85%
├── src/chat/message.py    78% ⚠️
└── src/db/models.py       82%

Uncovered Lines:
├── src/chat/message.py:45-52 (error handling)
└── src/chat/message.py:78-82 (edge case)

Status: ✅ PASS (85% ≥ 80%)
```

---

## Lint Standards

### Python (Ruff)

```bash
ruff check src/ tests/
```

Rules enforced:
- E: pycodestyle errors
- F: Pyflakes
- I: isort
- N: pep8-naming
- UP: pyupgrade

### TypeScript (ESLint)

```bash
npx eslint src/ --ext .ts,.tsx
```

### Go (golint)

```bash
golint ./...
```

---

## Type Checking

### Python (mypy)

```bash
mypy src/ --strict
```

Configuration (pyproject.toml):
```toml
[tool.mypy]
strict = true
ignore_missing_imports = true
```

### TypeScript (tsc)

```bash
npx tsc --noEmit
```

---

## Security Scanning

### Python (Bandit)

```bash
bandit -r src/
```

### Node.js (npm audit)

```bash
npm audit
```

### Dependency Check

```bash
# Python
pip-audit

# Node.js
npm audit --audit-level=high
```

---

## Quality Report

### Report Structure

`.forge/reports/{PRD_ID}-quality-report.md`:

```markdown
# Quality Report: {PRD_ID}

Generated: {timestamp}

## Summary

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Test Pass Rate | 100% | 100% | ✅ PASS |
| Code Coverage | 85% | 80% | ✅ PASS |
| Lint Errors | 0 | 0 | ✅ PASS |
| Type Errors | 0 | 0 | ✅ PASS |
| Security Issues | 0 | 0 | ✅ PASS |

## Test Results

Total: 49
Passed: 49
Failed: 0
Skipped: 0

### Test Breakdown

| Module | Tests | Passed | Coverage |
|--------|-------|--------|----------|
| auth | 15 | 15 | 92% |
| chat | 20 | 20 | 85% |
| db | 14 | 14 | 82% |

## Coverage Details

{detailed coverage by file}

## Lint Report

No issues found.

## Type Check Report

No errors found.

## Security Report

No vulnerabilities found.

## Recommendations

1. Increase coverage in src/chat/message.py (78%)
2. Consider adding integration tests for WebSocket
```

---

## Verification Checklist

### Before `/forge:verify`

- [ ] All TDD cycles completed
- [ ] No pending tasks
- [ ] All tests written and passing

### During `/forge:verify`

- [ ] Run full test suite
- [ ] Generate coverage report
- [ ] Run linter
- [ ] Run type checker
- [ ] Run security scanner
- [ ] Generate quality report

### After `/forge:verify`

- [ ] All gates pass → proceed to `/forge:sync`
- [ ] Any gate fails → fix issues and re-verify

---

## Quality Improvement Tips

### Increase Coverage

1. **Test edge cases**: null, empty, boundary values
2. **Test error paths**: exceptions, failures
3. **Test async code**: properly await and handle
4. **Mock external services**: isolate unit tests

### Fix Lint Issues

1. **Auto-fix**: `ruff check --fix src/`
2. **Format**: `ruff format src/`
3. **Review disabled rules**: ensure valid reasons

### Fix Type Errors

1. **Add annotations**: function params and returns
2. **Use generics**: for collections
3. **Handle None**: use Optional[] or | None
4. **Type guards**: narrow types with isinstance()

### Fix Security Issues

1. **Update dependencies**: patch vulnerabilities
2. **Sanitize input**: prevent injection
3. **Use secrets properly**: environment variables
4. **Review hardcoded values**: no credentials in code
