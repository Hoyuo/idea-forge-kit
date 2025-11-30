# Testing Best Practices

> Universal testing patterns for all languages.

---

## Core Principles

1. **Arrange-Act-Assert (AAA)** - Structure every test
2. **One assertion per test** - Focus on single behavior
3. **Descriptive test names** - `test_<function>_<scenario>_<expected>`
4. **Use fixtures/factories** - Reduce repetition
5. **Mock external dependencies** - Isolate unit under test
6. **Target 80%+ coverage** - Balance coverage with value

---

## Test Categories

| Type | Scope | Speed | Dependencies |
|------|-------|-------|--------------|
| Unit | Function/Method | Fast | Mocked |
| Integration | Module/Service | Medium | Real (some) |
| E2E | Full System | Slow | Real (all) |

---

## Test Directory Structure

```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # Service integration tests
├── e2e/            # End-to-end tests
├── fixtures/       # Shared test data
└── config.*        # Test configuration
```

---

## Test Data Factory Pattern

```
Factory: {EntityName}Factory
─────────────────────────────────────
create(overrides):
  return merge(defaults, overrides)

defaults:
  id        : auto_generate()
  email     : "test_{random}@example.com"
  username  : "user_{random}"
  createdAt : now()

build():
  return create() without persistence

create_batch(count, overrides):
  return [create(overrides) for _ in range(count)]
```

---

## Test Naming Conventions

```
# Pattern
test_<unit>_<scenario>_<expected>

# Examples
test_login_valid_credentials_returns_token
test_login_invalid_password_throws_auth_error
test_create_user_duplicate_email_returns_conflict
test_get_users_with_pagination_returns_correct_page
test_delete_user_not_found_returns_404
```

---

## Mock Patterns

### External Service Mock

```
MockExternalAPI:
  - Define expected requests
  - Return predefined responses
  - Verify call count and parameters
```

### Database Mock

```
MockRepository:
  - In-memory data store
  - Implement same interface as real repository
  - Reset between tests
```

### Time Mock

```
MockClock:
  - Freeze time for consistent tests
  - Advance time for timeout tests
  - Reset after each test
```

---

## Coverage Guidelines

| Type | Target | Priority |
|------|--------|----------|
| Unit | 80%+ | High |
| Integration | 60%+ | Medium |
| E2E | Critical paths | High |

### What to Cover

- ✅ Business logic
- ✅ Edge cases
- ✅ Error handling
- ✅ API contracts

### What to Skip

- ❌ Third-party library code
- ❌ Simple getters/setters
- ❌ Configuration files
- ❌ Generated code

---

## Test Isolation Rules

1. **No shared state** - Each test is independent
2. **Clean up after** - Reset database, mocks, files
3. **Deterministic** - Same input = same output
4. **No external calls** - Mock all network requests
5. **Fast execution** - Unit tests < 100ms each

---

## Integration Test Patterns

### API Integration Test

```
test_api_flow:
  1. Setup test database
  2. Create test data via factories
  3. Make HTTP request to endpoint
  4. Assert response status and body
  5. Assert database state
  6. Cleanup test data
```

### Service Integration Test

```
test_service_integration:
  1. Setup real dependencies (DB, cache)
  2. Mock external services
  3. Call service method
  4. Assert result and side effects
  5. Verify mock interactions
```

---

## E2E Test Guidelines

```
test_user_journey:
  1. Start with clean state
  2. Simulate real user actions
  3. Wait for async operations
  4. Assert visible outcomes
  5. Capture screenshots on failure
  6. Full cleanup
```

### E2E Best Practices

- Use realistic test data
- Test critical user flows only
- Run in CI/CD pipeline
- Retry flaky tests (max 2)
- Parallel execution when possible
