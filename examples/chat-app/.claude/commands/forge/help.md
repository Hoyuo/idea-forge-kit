# /forge:help - IdeaForge Help

This command displays all IdeaForge features.

---

## Output Content

Display the following content in a well-formatted manner:

```
IdeaForge - Automation from Idea to Implementation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Workflow
   Idea → PRD → Agents → TDD → Done

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Commands

   /forge:idea "idea"       Transform idea into PRD
   /forge:analyze {ID}      Analyze PRD, auto-generate agents/tasks
   /forge:build {ID}        Start TDD implementation (RED-GREEN-REFACTOR)
   /forge:verify {ID}       Verify requirements and generate report

   /forge:status            Check current status
   /forge:list              List all PRDs
   /forge:resume {ID}       Resume interrupted work
   /forge:help              This help

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Agents

   Base Agents (always included):
   ├── forge-orchestrator   Main orchestrator
   ├── forge-prd-writer     PRD writing specialist
   ├── forge-analyzer       PRD analyst
   └── forge-tdd-runner     TDD executor

   Dynamic Generation (after PRD analysis):
   ├── expert-backend       API, server, auth
   ├── expert-frontend      UI, components
   ├── expert-database      Schema, queries
   ├── expert-security      Security, encryption
   └── expert-devops        Deployment, CI/CD

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TDD Workflow

   RED      Write tests → Verify failure
   GREEN    Minimal implementation → Tests pass
   REFACTOR Improve code → Maintain tests

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Directory Structure

   .forge/
   ├── prds/       PRD documents
   ├── tasks/      Task breakdown
   ├── agents/     Dynamically generated agents
   ├── progress/   Checkpoints
   └── reports/    Verification reports

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Quick Start

   1. /forge:idea "real-time chat feature"
   2. /forge:analyze CHAT-001
   3. /forge:build CHAT-001
   4. /forge:verify CHAT-001

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
