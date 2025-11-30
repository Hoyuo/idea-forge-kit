# IdeaForge Git Module

> Git workflow patterns and 3-Mode system.

---

## 3-Mode System

### Mode Overview

| Mode | Environment | Use Case |
|------|-------------|----------|
| `manual` | Local | Solo development, learning |
| `personal` | GitHub | Individual projects |
| `team` | GitHub | Team collaboration |

---

## Manual Mode

**Configuration**:
```json
{
  "git_strategy": {
    "mode": "manual",
    "manual": {
      "environment": "local",
      "auto_branch": false,
      "auto_commit": true,
      "auto_pr": false,
      "auto_push": false
    }
  }
}
```

**Workflow**:
```
1. Work on main/develop branch (manual branch creation)
2. Auto-commit after TDD phases
3. Manual push when ready
4. No PR (local only)
```

**Auto-Commit Pattern**:
```bash
# After RED phase
git add tests/
git commit -m "test(CHAT-001): RED - Add failing tests for login"

# After GREEN phase
git add src/
git commit -m "feat(CHAT-001): GREEN - Implement login functionality"

# After REFACTOR phase
git add src/ tests/
git commit -m "refactor(CHAT-001): REFACTOR - Clean up login code"
```

---

## Personal Mode

**Configuration**:
```json
{
  "git_strategy": {
    "mode": "personal",
    "personal": {
      "environment": "github",
      "auto_branch": true,
      "auto_commit": true,
      "auto_pr": false,
      "auto_push": true,
      "branch_prefix": "feature/",
      "main_branch": "main"
    }
  }
}
```

**Workflow**:
```
1. Auto-create feature branch: feature/CHAT-001
2. Auto-commit after TDD phases
3. Auto-push to remote
4. Suggest PR creation (not auto)
```

**Branch Flow**:
```
main
  │
  └── feature/CHAT-001  (auto-created)
        │
        ├── commit: test(CHAT-001): RED - ...
        ├── commit: feat(CHAT-001): GREEN - ...
        ├── commit: refactor(CHAT-001): REFACTOR - ...
        │
        └── (suggest PR when complete)
```

---

## Team Mode

**Configuration**:
```json
{
  "git_strategy": {
    "mode": "team",
    "team": {
      "environment": "github",
      "auto_branch": true,
      "auto_commit": true,
      "auto_pr": true,
      "auto_push": true,
      "draft_pr": true,
      "required_reviews": 1,
      "branch_protection": true,
      "branch_prefix": "feature/",
      "main_branch": "main"
    }
  }
}
```

**Workflow**:
```
1. Auto-create feature branch: feature/CHAT-001
2. Auto-commit after TDD phases
3. Auto-push to remote
4. Auto-create draft PR when first push
5. Mark PR ready when complete
```

**PR Template**:
```markdown
## Summary

Implements CHAT-001: Real-time Chat Feature

### Changes
- Added WebSocket connection management
- Implemented message broadcasting
- Added message persistence

## Test Plan

- [x] Unit tests for connection manager
- [x] Integration tests for messaging
- [x] WebSocket endpoint tests

## Checklist

- [x] Tests passing (49/49)
- [x] Coverage: 85%
- [x] Lint: 0 errors
- [x] Type check: 0 errors

## Related

- PRD: .forge/prds/CHAT-001.md
- Tasks: .forge/tasks/CHAT-001/tasks.json
```

---

## Conventional Commits

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(auth): Add OAuth2 login` |
| `fix` | Bug fix | `fix(chat): Resolve message ordering` |
| `test` | Test changes | `test(auth): Add login unit tests` |
| `docs` | Documentation | `docs(api): Update endpoint docs` |
| `refactor` | Code refactoring | `refactor(chat): Extract message handler` |
| `style` | Formatting | `style: Apply black formatting` |
| `chore` | Maintenance | `chore: Update dependencies` |

### TDD Commit Pattern

```bash
# RED phase
test({PRD_ID}): RED - Add failing tests for {feature}

# GREEN phase
feat({PRD_ID}): GREEN - Implement {feature}

# REFACTOR phase
refactor({PRD_ID}): REFACTOR - Clean up {feature}
```

---

## Branch Naming

### Pattern

```
{prefix}/{PRD_ID}[-optional-description]
```

### Examples

```
feature/CHAT-001
feature/CHAT-001-websocket
feature/AUTH-002-oauth
fix/CHAT-001-message-order
```

---

## Git Commands Reference

### Branch Operations

```bash
# Create and switch
git checkout -b feature/{PRD_ID}

# Push with upstream
git push -u origin feature/{PRD_ID}

# Delete local
git branch -d feature/{PRD_ID}

# Delete remote
git push origin --delete feature/{PRD_ID}
```

### Commit Operations

```bash
# Stage and commit
git add .
git commit -m "feat({PRD_ID}): Description"

# Amend last commit (before push)
git commit --amend -m "New message"

# View log
git log --oneline -10
```

### PR Operations (GitHub CLI)

```bash
# Create PR
gh pr create --title "feat({PRD_ID}): Title" --body "Description" --draft

# Mark ready for review
gh pr ready

# View PR
gh pr view

# Merge PR
gh pr merge --squash
```

---

## Safety Rules

### Never Do

- ❌ Force push to main/master
- ❌ Commit credentials or secrets
- ❌ Commit without testing
- ❌ Merge without review (team mode)

### Always Do

- ✅ Pull before starting work
- ✅ Run tests before commit
- ✅ Use meaningful commit messages
- ✅ Create draft PR first (team mode)

---

## Conflict Resolution

### When Conflicts Occur

1. **Pull latest changes**:
   ```bash
   git pull origin main
   ```

2. **Resolve conflicts**:
   - Edit conflicted files
   - Remove conflict markers
   - Keep correct code

3. **Mark resolved**:
   ```bash
   git add <resolved-files>
   git commit -m "chore: Resolve merge conflicts"
   ```

4. **Run tests**:
   ```bash
   # Ensure nothing broke
   pytest tests/ -v
   ```

5. **Continue work**:
   ```bash
   git push
   ```
