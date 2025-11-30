# /forge:dashboard - Real-time Progress Dashboard

## Usage

```
/forge:dashboard
/forge:dashboard --port 20555
```

## Description

Starts a local web server to visualize IdeaForge progress in real-time.

## Features

- **PRD Overview**: All PRDs with status and progress
- **TDD Visualization**: RED/GREEN/REFACTOR phase tracking
- **Test Results**: Pass/fail counts, coverage percentage
- **Diagram Preview**: PlantUML diagrams rendered in browser
- **Real-time Updates**: Auto-refresh every 5 seconds

## Workflow

### 1. Start Server

```
Starting IdeaForge Dashboard...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Server running at: http://localhost:20555

Dashboard Features:
   ├── PRD List & Status
   ├── TDD Phase Visualization
   ├── Test Results & Coverage
   └── Diagram Preview

Press Ctrl+C to stop the server.
```

### 2. Dashboard Views

#### Home - PRD Overview
```
┌─────────────────────────────────────────────────────────┐
│  🔥 IdeaForge Dashboard                                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  PRD List                                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │ AUTH-001  │ Building │ ████████░░ 80% │ 🟢 GREEN │   │
│  │ CHAT-002  │ Complete │ ██████████ 100% │ ✅ Done │   │
│  │ API-003   │ Pending  │ ░░░░░░░░░░ 0%  │ ⏳ Wait │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### PRD Detail View
```
┌─────────────────────────────────────────────────────────┐
│  AUTH-001: User Authentication                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Progress: ████████████░░░░░░░░ 60%                     │
│                                                         │
│  Tasks                                                  │
│  ├── FR-001: Email Login      ✅ Complete               │
│  ├── FR-002: OAuth Login      🟢 GREEN (implementing)   │
│  ├── FR-003: Password Reset   🔴 RED (testing)          │
│  └── FR-004: Session Mgmt     ⏳ Pending                │
│                                                         │
│  Test Summary                                           │
│  ├── Total: 24                                          │
│  ├── Passed: 20 ✓                                       │
│  ├── Failed: 4 ✗                                        │
│  └── Coverage: 78%                                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### Diagram View
```
┌─────────────────────────────────────────────────────────┐
│  Diagrams: AUTH-001                                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [System Architecture] [Class Diagram] [Sequences]      │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │                                                   │   │
│  │     [PlantUML Rendered Diagram]                  │   │
│  │                                                   │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Source: .forge/design/AUTH-001/diagrams/               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 3. API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Dashboard home page |
| `GET /api/prds` | List all PRDs with status |
| `GET /api/prds/:id` | Get PRD details |
| `GET /api/prds/:id/tasks` | Get tasks for PRD |
| `GET /api/prds/:id/progress` | Get progress/checkpoint |
| `GET /api/prds/:id/diagrams` | List diagrams |
| `GET /api/prds/:id/diagrams/:name` | Get diagram source |
| `GET /api/render-plantuml` | Render PlantUML to SVG |

### 4. File Monitoring

The server monitors these directories:
- `.forge/prds/` - PRD documents
- `.forge/tasks/` - Task decomposition
- `.forge/progress/` - Checkpoints
- `.forge/design/` - Diagrams

### 5. Stop Server

```
Stopping IdeaForge Dashboard...

Server stopped.
```

## Options

- `--port {number}`: Server port (default: 20555)
- `--open`: Auto-open browser
- `--watch`: Enable file watching for auto-refresh

## Requirements

- Node.js 18+ installed
- npm or npx available

## Installation

The dashboard is included in the IdeaForge template. On first run, dependencies are installed automatically:

```bash
cd .forge/dashboard
npm install
```

Or run directly with npx (no install needed).
