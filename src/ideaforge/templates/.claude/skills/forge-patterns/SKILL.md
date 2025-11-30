# IdeaForge Patterns Skill

> **Language-agnostic** development patterns for IdeaForge workflow.
> Modular structure for efficient token usage.

---

## Quick Reference

| Pattern | Module | When to Use |
|---------|--------|-------------|
| TDD Workflow | [modules/tdd.md](modules/tdd.md) | RED-GREEN-REFACTOR cycle |
| API Design | [modules/api.md](modules/api.md) | REST API, OpenAPI 3.0 |
| Database Schema | [modules/database.md](modules/database.md) | Entity modeling, migrations |
| Testing | [modules/testing.md](modules/testing.md) | Test patterns, coverage |
| Error Handling | [modules/errors.md](modules/errors.md) | Error types, responses |
| Architecture Diagrams | [modules/diagrams.md](modules/diagrams.md) | PlantUML diagrams |

---

## Module Overview

### TDD Workflow (`modules/tdd.md`)
- RED Phase - Write failing tests
- GREEN Phase - Minimal implementation
- REFACTOR Phase - Improve quality
- Checkpoint patterns
- Status indicators (🔴🟢🔵)

### API Design (`modules/api.md`)
- RESTful 2.0 conventions
- OpenAPI 3.0 specification
- CRUD patterns
- Authentication endpoints
- WebSocket events (AsyncAPI)

### Database Schema (`modules/database.md`)
- Entity definition pattern
- Relationship types (1:N, N:M)
- Migration pattern
- Soft delete, audit log
- Index guidelines

### Testing (`modules/testing.md`)
- AAA pattern (Arrange-Act-Assert)
- Test categories (Unit, Integration, E2E)
- Factory pattern
- Mock patterns
- Coverage guidelines

### Error Handling (`modules/errors.md`)
- Standard error types
- HTTP status codes
- Error response format
- Retry patterns
- Circuit breaker

### Architecture Diagrams (`modules/diagrams.md`)
- System Architecture
- Class Diagram
- Sequence Diagram
- Package Diagram
- ER Diagram
- State Diagram
- Activity Diagram

---

## IdeaForge Workflow Integration

```
/forge:idea     → PRD Generation
/forge:analyze  → Agent/Task Generation
/forge:design   → Architecture Diagrams (modules/diagrams.md)
/forge:build    → TDD Implementation (modules/tdd.md)
/forge:verify   → Verification
```

---

## Project Structure

```
project/
├── src/                # Source code
│   ├── api/            # API layer (modules/api.md)
│   ├── core/           # Business logic
│   ├── models/         # Data models (modules/database.md)
│   ├── services/       # Services
│   └── utils/          # Utilities
├── tests/              # Tests (modules/testing.md)
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docs/               # Documentation
└── .forge/             # IdeaForge artifacts
    ├── prds/           # PRD documents
    ├── tasks/          # Task decomposition
    ├── design/         # Diagrams (modules/diagrams.md)
    └── progress/       # Checkpoints
```

---

## Code Quality Checklist

### Before Commit
- [ ] All tests pass
- [ ] No linting errors
- [ ] Type checking passes
- [ ] Code coverage maintained
- [ ] Documentation updated

### Code Review Criteria
| Aspect | Check |
|--------|-------|
| Correctness | Does it work as intended? |
| Readability | Is it easy to understand? |
| Maintainability | Is it easy to modify? |
| Performance | Are there obvious bottlenecks? |
| Security | Are there vulnerabilities? |
| Tests | Are edge cases covered? |

---

## Loading Modules

When working on specific patterns, load the relevant module:

```
# For TDD workflow
Read modules/tdd.md

# For API design
Read modules/api.md

# For database modeling
Read modules/database.md

# For architecture diagrams
Read modules/diagrams.md
```

This modular approach saves tokens by loading only what's needed.
