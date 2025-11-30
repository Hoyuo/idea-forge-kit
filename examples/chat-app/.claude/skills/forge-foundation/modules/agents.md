# IdeaForge Agents Module

> Complete agent catalog and selection guide.

---

## Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Hierarchy                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Core Agents (Always Loaded)            │    │
│  │                                                     │    │
│  │  forge-orchestrator  │  Main workflow coordinator   │    │
│  │  forge-prd-writer    │  PRD document creation       │    │
│  │  forge-analyzer      │  PRD analysis, task gen      │    │
│  │  forge-tdd-runner    │  TDD cycle execution         │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │            Manager Agents (Workflow)                │    │
│  │                                                     │    │
│  │  forge-designer      │  Architecture diagrams       │    │
│  │  forge-sync          │  Documentation sync          │    │
│  │  forge-quality       │  Quality verification        │    │
│  │  forge-git           │  Git workflow management     │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │          Dynamic Agents (Generated per PRD)         │    │
│  │                                                     │    │
│  │  expert-backend      │  API, server, auth           │    │
│  │  expert-frontend     │  UI, components              │    │
│  │  expert-database     │  Schema, queries             │    │
│  │  expert-security     │  Security, encryption        │    │
│  │  expert-devops       │  Deployment, CI/CD           │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Agents

### forge-orchestrator

**Role**: Main workflow coordinator

**Responsibilities**:
- Route commands to appropriate agents
- Manage workflow state
- Handle errors and recovery
- Coordinate between agents

**When Used**: Every command invocation

---

### forge-prd-writer

**Role**: PRD document creation

**Responsibilities**:
- Transform ideas into structured PRDs
- Define functional requirements (FR)
- Define non-functional requirements (NFR)
- Create acceptance criteria

**When Used**: `/forge:idea`

**Output**: `.forge/prds/{ID}.md`

---

### forge-analyzer

**Role**: PRD analysis and task generation

**Responsibilities**:
- Analyze PRD requirements
- Generate task breakdown
- Select required expert agents
- Estimate complexity

**When Used**: `/forge:analyze`

**Output**:
- `.forge/tasks/{ID}/tasks.json`
- `.forge/agents/{ID}/`

---

### forge-tdd-runner

**Role**: TDD cycle execution

**Responsibilities**:
- Execute RED-GREEN-REFACTOR cycle
- Manage checkpoints
- Run tests
- Track progress

**When Used**: `/forge:build`

**Output**: Implementation in `src/`, tests in `tests/`

---

## Manager Agents

### forge-designer

**Role**: Architecture diagram generation

**Responsibilities**:
- Analyze PRD for entities and flows
- Generate PlantUML diagrams
- Create design documentation

**When Used**: `/forge:design`

**Output**: `.forge/design/{ID}/`

**Diagrams Generated**:
- System Architecture
- Class Diagram
- Sequence Diagrams
- ER Diagram
- State Diagrams

---

### forge-sync

**Role**: Documentation synchronization

**Responsibilities**:
- Analyze implementation
- Update README
- Generate API documentation
- Update CHANGELOG

**When Used**: `/forge:sync`

**Output**: `README.md`, `docs/`, `CHANGELOG.md`

---

### forge-quality

**Role**: Quality verification

**Responsibilities**:
- Run test suite
- Check coverage
- Run linter
- Run type checker
- Security scanning
- Generate quality report

**When Used**: `/forge:verify`

**Output**: `.forge/reports/{ID}-quality-report.md`

---

### forge-git

**Role**: Git workflow management

**Responsibilities**:
- Create branches (personal/team mode)
- Auto-commit TDD progress
- Push to remote
- Create PRs (team mode)

**When Used**: During TDD, after sync

**Modes**: manual, personal, team

---

## Dynamic Agents

Generated by `forge-analyzer` based on PRD analysis.

### expert-backend

**Domain**: API, Server, Authentication

**Technologies**:
- FastAPI, Django, Flask (Python)
- Express, NestJS (Node.js)
- Gin, Echo (Go)

**Tasks**:
- REST API endpoints
- Authentication/Authorization
- Business logic
- Data validation

---

### expert-frontend

**Domain**: UI, Components, State

**Technologies**:
- React, Next.js
- Vue, Nuxt
- Svelte, SvelteKit

**Tasks**:
- UI components
- State management
- API integration
- Routing

---

### expert-database

**Domain**: Schema, Queries, Migrations

**Technologies**:
- PostgreSQL, MySQL, SQLite
- MongoDB, Redis
- SQLAlchemy, Prisma, GORM

**Tasks**:
- Schema design
- Query optimization
- Migrations
- Data modeling

---

### expert-security

**Domain**: Security, Encryption, Auth

**Tasks**:
- Authentication implementation
- Authorization (RBAC, ABAC)
- Encryption/Hashing
- Security best practices
- Vulnerability prevention

---

### expert-devops

**Domain**: Deployment, CI/CD, Infrastructure

**Technologies**:
- Docker, Kubernetes
- GitHub Actions, GitLab CI
- AWS, GCP, Azure

**Tasks**:
- Containerization
- CI/CD pipelines
- Infrastructure setup
- Monitoring

---

## Agent Selection Guide

### By Task Type

| Task Type | Primary Agent | Support Agent |
|-----------|---------------|---------------|
| API Development | expert-backend | expert-database |
| UI Development | expert-frontend | - |
| Database Design | expert-database | expert-backend |
| Authentication | expert-security | expert-backend |
| Deployment | expert-devops | - |
| Documentation | forge-sync | - |
| Quality Check | forge-quality | - |
| Diagrams | forge-designer | - |

### By PRD Type

| PRD Type | Agents Generated |
|----------|------------------|
| Web App | backend, frontend, database |
| API Only | backend, database, security |
| CLI Tool | backend |
| Full Stack | All expert agents |

---

## Agent Communication

### Flow Example

```
User: /forge:build CHAT-001

forge-orchestrator
    │
    ├── Read checkpoint
    │
    ├── Select agent: expert-backend (TASK-003)
    │       │
    │       └── forge-tdd-runner
    │               │
    │               ├── 🔴 RED: Write test
    │               ├── 🟢 GREEN: Implement
    │               └── 🔵 REFACTOR: Clean up
    │
    ├── Save checkpoint
    │
    └── forge-git (if auto_commit)
            │
            └── Commit changes
```

---

## Adding Custom Agents

### Agent File Structure

```markdown
---
name: custom-agent
description: Agent description
tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Custom Agent

You are a specialist for {domain}.

## Mission

{Agent's primary goal}

## Capabilities

{List of what this agent can do}

## Workflow

{Step-by-step process}

## Output Format

{Expected output structure}
```

### Registration

Place in `.claude/agents/forge/` directory.

Update CLAUDE.md to reference new agent.
