# /forge:analyze - PRD Analysis and Dynamic Agent Generation

## Usage

```
/forge:analyze AUTH-001
/forge:analyze CHAT-002
```

## Input

`$ARGUMENTS` - PRD ID to analyze

## Description

Analyzes PRD to automatically:
1. **Detect domains** from requirements
2. **Generate specialized agents** for each domain
3. **Decompose tasks** with dependencies
4. **Estimate complexity** and timeline

## Language Configuration

Read from `.forge/config.json`:
- `language.conversation` for analysis responses
- `language.output_documents` for generated files

## Workflow

### Phase 1: Load PRD

```
Loading: .forge/prds/{PRD_ID}.md
```

Uses `lib.prd_analyzer.PRDAnalyzer` to parse PRD.

### Phase 2: Domain Analysis

**Domain Detection** (8 domains supported):

| Domain | Keywords | Agent |
|--------|----------|-------|
| Backend | api, server, endpoint, rest, graphql | expert-backend |
| Frontend | ui, component, page, form, react | expert-frontend |
| Database | database, schema, table, query, sql | expert-database |
| Security | auth, oauth, jwt, token, encryption | expert-security |
| DevOps | deploy, docker, kubernetes, ci/cd | expert-devops |
| Testing | test, unit, integration, e2e, coverage | expert-testing |
| Mobile | mobile, ios, android, app, flutter | expert-mobile |
| AI/ML | ai, ml, llm, gpt, embedding | expert-ai |

**Confidence Scoring**:
- 3+ keyword matches = High confidence (0.8-1.0)
- 2 keyword matches = Medium confidence (0.5-0.7)
- 1 keyword match = Low confidence (0.3-0.4)

### Phase 3: User Confirmation

Before generating agents, ask user:

```
📋 Agent Generation Plan for {PRD_ID}

Detected Domains:
  1. backend (confidence: 0.85) → expert-backend
     Requirements: FR-001, FR-002, FR-005

  2. frontend (confidence: 0.72) → expert-frontend
     Requirements: FR-003, FR-004

  3. database (confidence: 0.65) → expert-database
     Requirements: FR-006

Total: 3 agents, 6 requirements

Generate these agents? [Y/n]
```

### Phase 4: Dynamic Agent Generation

Uses `lib.agent_generator.AgentGenerator`:

```python
from lib.agent_generator import AgentGenerator

generator = AgentGenerator(project_dir)
result = generator.generate_agents_for_prd(prd_id, prd_content)
```

**Output Structure**:

```
.forge/agents/{PRD_ID}/
├── index.json              # Agent registry
├── expert-backend.md       # Backend specialist
├── expert-frontend.md      # Frontend specialist
├── expert-database.md      # Database specialist
└── expert-{domain}.md      # Other domains
```

**Generated Agent Template**:

```markdown
---
name: expert-{domain}
description: {PRD_ID} {domain} implementation specialist
model: sonnet
context:
  prd: {PRD_ID}
  domain: {domain}
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
skills:
  - forge-foundation
---

# {PRD_ID} {Domain} Expert

## Assigned Requirements
{Requirements from PRD for this domain}

## Tech Stack
{Relevant tech from PRD}

## TDD Rules
1. Write tests first (RED)
2. Minimal code to pass (GREEN)
3. Refactor (BLUE)
```

### Phase 5: Task Decomposition

**Output**: `.forge/tasks/{PRD_ID}/tasks.json`

```json
{
  "prd_id": "AUTH-001",
  "created": "2025-11-30T12:00:00Z",
  "total_tasks": 6,
  "by_domain": {
    "backend": 3,
    "frontend": 2,
    "database": 1
  },
  "by_complexity": {
    "simple": 2,
    "medium": 3,
    "complex": 1
  },
  "estimated_hours": 12,
  "tasks": [
    {
      "id": "FR-001",
      "title": "Login API endpoint",
      "agent": "expert-backend",
      "domain": "backend",
      "dependencies": ["FR-006"],
      "complexity": "medium",
      "status": "pending"
    }
  ]
}
```

### Phase 6: Update PRD Status

Add analysis metadata to PRD:

```markdown
---
status: analyzed
analyzed_at: 2025-11-30T12:00:00Z
generated_agents:
  - expert-backend
  - expert-frontend
  - expert-database
total_tasks: 6
estimated_hours: 12
---
```

### Phase 7: Completion Report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRD Analysis Complete: {PRD_ID}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Domain Analysis:
   Primary: backend (confidence: 0.85)
   Secondary: frontend (0.72), database (0.65)

🤖 Generated Agents (3):
   .forge/agents/{PRD_ID}/
   ├── expert-backend.md    → FR-001, FR-002, FR-005
   ├── expert-frontend.md   → FR-003, FR-004
   └── expert-database.md   → FR-006

📋 Task Breakdown (6 tasks):
   [backend]  FR-001: Login API (medium)
   [backend]  FR-002: OAuth integration (complex)
   [backend]  FR-005: Token validation (simple)
   [frontend] FR-003: Login page UI (simple)
   [frontend] FR-004: Dashboard (medium)
   [database] FR-006: User schema (medium)

📈 Complexity Summary:
   Simple: 2  |  Medium: 3  |  Complex: 1

⏱️ Estimated Time: ~12 hours

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Steps:
  /forge:design {PRD_ID}  - Generate architecture diagrams
  /forge:build {PRD_ID}   - Start TDD implementation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## MCP Integration

- **Sequential-Thinking**: Complex domain analysis and dependency mapping
- **Context7**: Latest library docs for tech stack decisions

## Quality Checks

- [ ] All requirements assigned to agents
- [ ] No orphan requirements
- [ ] Dependencies are acyclic (no circular deps)
- [ ] Each domain has appropriate tools
- [ ] Tech stack is compatible

## Error Handling

| Error | Resolution |
|-------|------------|
| PRD not found | Check `.forge/prds/{ID}.md` exists |
| No requirements | Ensure PRD has FR-XXX format requirements |
| Unknown domain | Assign to `expert-general` |
| Circular deps | Report warning, suggest resolution |

## Examples

### Example 1: Simple PRD

```
/forge:analyze LOGIN-001

→ Detected: backend, frontend
→ Generated: 2 agents
→ Tasks: 4
```

### Example 2: Complex PRD

```
/forge:analyze ECOMMERCE-001

→ Detected: backend, frontend, database, security, devops
→ Generated: 5 agents
→ Tasks: 15
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/forge:idea` | Create PRD first |
| `/forge:design` | Generate architecture diagrams |
| `/forge:build` | Start TDD implementation |
| `/forge:status` | Check analysis status |
