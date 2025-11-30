# /forge:verify - Requirements Verification

## Usage

```
/forge:verify AUTH-001
```

## Input

`$ARGUMENTS` - PRD ID to verify

## Language Configuration

Read from `.forge/config.json`:
- Use `language.conversation` for verification responses
- Use `language.output_documents` for verification reports

## Workflow

### 1. Verification Preparation

```
IdeaForge Verify: {PRD_ID}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

1. Load PRD: `.forge/prds/{PRD_ID}.md`
2. Task status: `.forge/tasks/{PRD_ID}/tasks.json`
3. Progress: `.forge/progress/{PRD_ID}/checkpoint.json`

### 2. Requirements Checklist Verification

For each requirement in PRD:

```
Functional Requirements Verification
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ FR-001: Email/Password Login
   ├── Implementation: src/auth/login.py ✓
   ├── Tests: tests/test_auth.py::test_login ✓
   └── Coverage: 92% ✓

✓ FR-002: OAuth Social Login
   ├── Implementation: src/auth/oauth.py ✓
   ├── Tests: tests/test_oauth.py ✓
   └── Coverage: 88% ✓

⚠ FR-003: Password Reset
   ├── Implementation: src/auth/password.py ✓
   ├── Tests: tests/test_password.py ✓
   └── Coverage: 65% ⚠ (target: 80%)

Non-Functional Requirements Verification
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ NFR-001: Response Time < 200ms
   └── Measured: avg 145ms ✓

✓ NFR-002: Security Standards Compliance
   └── OWASP Top 10 Check ✓
```

### 3. Test Execution

Run full test suite (command determined by project's tech stack):

```
# Test command is auto-detected from project configuration
# Examples by language:
#   Python:     pytest tests/ -v --cov
#   TypeScript: npm test -- --coverage
#   Go:         go test ./... -cover
#   Rust:       cargo test
#   Java:       mvn test / gradle test
```

Result:
```
Test Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Tests: 24
├── Passed:  24 ✓
├── Failed:  0
├── Skipped: 0
└── Errors:  0

Coverage: 87%
├── src/auth/login.*      92%
├── src/auth/oauth.*      88%
├── src/auth/password.*   65% ⚠
└── src/auth/session.*    95%
```

### 4. Code Quality Check

```
Code Quality
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Linting:
├── Errors: 0 ✓
├── Warnings: 2 ⚠
└── Style: 98/100

Type Checking:
├── Errors: 0 ✓
└── Coverage: 85%

Complexity:
├── Avg Cyclomatic: 4.2 (good)
└── Max Cyclomatic: 8 (acceptable)
```

### 5. Final Report Generation

`.forge/reports/{PRD_ID}-final.md`:

```markdown
# {PRD_ID} Verification Report

## Summary
- Status: ✓ Pass / ⚠ Partial Pass / ✗ Fail
- Verified: {ISO-DATE}
- Duration: {BUILD_DURATION}

## Requirements Fulfillment
- Functional Requirements: 5/5 (100%)
- Non-Functional Requirements: 2/2 (100%)

## Test Results
- Total: 24 tests
- Passed: 24 (100%)
- Coverage: 87%

## Code Quality
- Linting: Pass
- Type Check: Pass
- Complexity: Good

## Improvement Recommendations
1. Improve password.py coverage (65% → 80%)
2. Resolve 2 warnings

## Generated Files
{File list}
```

### 6. Completion Message

**On Success**:
```
Verification Complete: {PRD_ID}

Result: PASSED

Requirements: 7/7 fulfilled (100%)
Tests: 24/24 passed
Coverage: 87%

Report: .forge/reports/{PRD_ID}-final.md

Next Steps:
   - Git commit recommended
   - Check other PRDs with /forge:list
```

**On Partial Pass**:
```
Verification Complete: {PRD_ID}

Result: PARTIAL PASS

Requirements: 6/7 fulfilled (86%)
Tests: 22/24 passed
Coverage: 72% (target: 80%)

Unfulfilled Items:
   - FR-003: Coverage insufficient
   - NFR-002: Performance not met

Report: .forge/reports/{PRD_ID}-final.md

Recommended Actions:
   /forge:build {PRD_ID} --task FR-003
```
