# IdeaForge Project Instructions

> **IdeaForge**: AI development kit that automates from idea to implementation

---

## Core Workflow

```
Idea → PRD → Design → Agents → TDD → Verify → Sync → Done

/forge:idea     → Generate PRD
/forge:analyze  → Auto-generate agents + task breakdown (Dynamic Agent System)
/forge:design   → Architecture diagrams (PlantUML)
/forge:build    → TDD implementation (RED-GREEN-REFACTOR)
/forge:verify   → Requirements verification
/forge:sync     → Documentation synchronization
/forge:dashboard → Real-time progress visualization
```

---

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/forge:idea "idea"` | Transform idea into PRD |
| `/forge:analyze {ID}` | Analyze PRD, auto-generate agents/tasks |
| `/forge:design {ID}` | Generate architecture diagrams |
| `/forge:build {ID}` | Start TDD implementation |
| `/forge:verify {ID}` | Verify requirements |
| `/forge:sync {ID}` | Synchronize documentation |
| `/forge:dashboard` | Start progress dashboard (port 20555) |
| `/forge:status` | Check current status |
| `/forge:list` | List all PRDs |
| `/forge:resume {ID}` | Resume interrupted work |
| `/forge:feedback "msg"` | Submit feedback or report issues |
| `/forge:help` | Show help |

---

## Directory Structure

```
.forge/
├── prds/           # PRD documents
├── tasks/          # Task breakdown results
├── agents/         # Dynamically generated agents (per PRD)
│   └── {PRD_ID}/   # Agent set for specific PRD
├── progress/       # Progress and checkpoints
├── design/         # Architecture diagrams (PlantUML)
├── reports/        # Verification reports
├── logs/           # Execution logs
├── feedback/       # User feedback
├── dashboard/      # Web dashboard server
└── config.json     # Configuration

.claude/
├── agents/forge/   # Base agents (9)
├── commands/forge/ # Slash commands (12)
├── hooks/          # Session hooks + lib/
│   └── lib/        # Shared Python modules
├── skills/         # Skills (forge-foundation)
└── settings.json   # Permission settings
```

---

## Agent System

### Base Agents (Core)

| Agent | Role |
|-------|------|
| `forge-orchestrator` | Main orchestrator, workflow coordination |
| `forge-prd-writer` | PRD writing specialist |
| `forge-analyzer` | PRD analysis, dynamic agent generation (v2.0) |
| `forge-tdd-runner` | TDD cycle execution |

### Manager Agents (Workflow)

| Agent | Role |
|-------|------|
| `forge-designer` | Architecture diagram generation |
| `forge-sync` | Documentation synchronization |
| `forge-quality` | Test coverage and code quality |
| `forge-git` | Git workflow management |
| `forge-feedback` | Feedback collection and categorization |

### Dynamic Agents (8 Domains)

Generated automatically by `/forge:analyze` based on PRD content:

| Agent | Domain | Keywords |
|-------|--------|----------|
| `expert-backend` | API, server | api, server, endpoint, rest, graphql |
| `expert-frontend` | UI, components | ui, component, page, react, vue |
| `expert-database` | Schema, queries | database, schema, table, sql, prisma |
| `expert-security` | Security | auth, oauth, jwt, token, encryption |
| `expert-devops` | Deployment | deploy, docker, kubernetes, ci/cd |
| `expert-testing` | Testing | test, unit, integration, e2e |
| `expert-mobile` | Mobile apps | mobile, ios, android, flutter |
| `expert-ai` | AI/ML | ai, ml, llm, gpt, embedding |

---

## Dynamic Agent System (v2.0)

### How It Works

1. **Domain Detection**: Analyze PRD for keywords
2. **Confidence Scoring**: Calculate match confidence (0.0-1.0)
3. **Agent Generation**: Create specialized agents per domain
4. **Requirement Assignment**: Map FR-XXX to appropriate agents

### Output Structure

```
.forge/agents/{PRD_ID}/
├── index.json           # Agent registry with analysis
├── expert-backend.md    # Backend specialist
├── expert-frontend.md   # Frontend specialist
└── expert-{domain}.md   # Other domain specialists
```

### Python Modules

```python
from lib.agent_generator import AgentGenerator
from lib.prd_analyzer import PRDAnalyzer
```

---

## TDD Workflow

```
🔴 RED      → Write tests, verify failure
🟢 GREEN   → Minimal implementation, pass tests
🔵 REFACTOR → Improve code, maintain tests
```

This cycle repeats for each task.

---

## Git Strategy (3-Mode System)

Configure in `.forge/config.json` → `git_strategy.mode`:

| Mode | Environment | Auto Branch | Auto Commit | Auto Push | Auto PR |
|------|-------------|-------------|-------------|-----------|---------|
| `manual` | Local | ❌ | ✅ | ❌ | ❌ |
| `personal` | GitHub | ✅ | ✅ | ✅ | ❌ |
| `team` | GitHub | ✅ | ✅ | ✅ | ✅ (draft) |

---

## Document Management

Configure in `.forge/config.json` → `document_management`:

- **auto_sync**: Auto-run `/forge:sync` after build
- **sections**: readme, api, diagrams, tests, changelog
- **cleanup**: Auto-cleanup old logs/reports

---

## Dashboard

Real-time progress visualization server:

```bash
cd .forge/dashboard
npm install
npm start
# → http://localhost:20555
```

Features:
- PRD list & progress
- TDD phase visualization (🔴🟢🔵)
- Test results & coverage
- PlantUML diagram preview

---

## Hooks System

### Session Hooks

| Hook | Purpose |
|------|---------|
| `SessionStart` | Initialize session, show project info |
| `SessionEnd` | Save metrics, cleanup, show summary |

### Hook Library (`.claude/hooks/lib/`)

| Module | Purpose |
|--------|---------|
| `config.py` | Configuration management |
| `checkpoint.py` | Progress checkpoints |
| `paths.py` | Path utilities |
| `agent_generator.py` | Dynamic agent generation |
| `prd_analyzer.py` | PRD analysis utilities |

---

## Checkpoint System

Work state is saved to `.forge/progress/{ID}/checkpoint.json` whenever interrupted.

Use `/forge:resume {ID}` to continue from where you left off.

---

## MCP Servers

- **Context7**: Latest library documentation reference (hallucination prevention)
- **Sequential-Thinking**: Complex analysis and design

---

## Language Configuration

Read from `.forge/config.json`:
- `language.conversation`: AI response language
- `language.output_documents`: PRD/report language

Supported languages: en, ko, ja, zh

---

## Quality Standards

- Test coverage target: 80% (configurable)
- Lint: No errors
- Type check: No errors
- Security: No vulnerabilities

---

## Version

IdeaForge v0.1.0
