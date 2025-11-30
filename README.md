# 🔥 IdeaForge

[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](https://github.com/Hoyuo/idea-forge-kit)
[![Python](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

> 아이디어에서 구현까지 자동화하는 AI 개발 킷

**아이디어 하나로 PRD 생성 → 에이전트 자동 생성 → TDD 구현 → 완료**

## 특징

- 🎯 **Zero-to-Code**: 아이디어만 입력하면 동작하는 코드까지
- 🤖 **Agent-on-Demand**: PRD 분석해서 필요한 에이전트만 자동 생성
- 🧪 **TDD-First**: 항상 테스트 먼저, 품질 보장
- 📊 **Progress Tracking**: 모든 단계의 진행 상황 실시간 추적
- 💾 **Checkpoint System**: 언제든 중단하고 재개 가능

## 설치

```bash
# GitHub에서 직접 설치
uv pip install git+https://github.com/Hoyuo/idea-forge-kit.git

# 또는 로컬 클론 후 설치
git clone https://github.com/Hoyuo/idea-forge-kit.git
cd idea-forge-kit
uv pip install -e .

# uv tool로 전역 설치 (권장)
uv tool install git+https://github.com/Hoyuo/idea-forge-kit.git
```

> **Note**: PyPI 배포 예정. 배포 후에는 `uv pip install ideaforge`로 설치 가능.

## 빠른 시작

### 1. 프로젝트 초기화

```bash
# 새 프로젝트
forge init my-project
cd my-project

# 또는 기존 프로젝트에
cd existing-project
forge init .
```

### 2. Claude Code 실행

```bash
claude
```

### 3. 워크플로우 시작

```
# 아이디어를 PRD로
/forge:idea "사용자 인증 시스템 with OAuth"

# PRD 분석 및 에이전트 생성
/forge:analyze AUTH-001

# TDD 구현
/forge:build AUTH-001

# 검증
/forge:verify AUTH-001
```

## 워크플로우

```
💡 Idea          📋 PRD           🤖 Agents        🔨 Build         ✅ Done
    │               │                │                │               │
    ▼               ▼                ▼                ▼               ▼
/forge:idea  →  /forge:analyze  →  /forge:build  →  /forge:verify
```

## 명령어

### CLI 명령어

| 명령어 | 설명 |
|--------|------|
| `forge init [path]` | 프로젝트 초기화 |
| `forge upgrade` | 최신 버전으로 업그레이드 |
| `forge doctor` | 시스템 요구사항 확인 |
| `forge status` | 프로젝트 상태 |
| `forge list` | PRD 목록 |

### 슬래시 명령어 (Claude Code 내)

| 명령어 | 설명 |
|--------|------|
| `/forge:idea "아이디어"` | 아이디어를 PRD로 변환 |
| `/forge:analyze {ID}` | PRD 분석, 에이전트/태스크 자동 생성 |
| `/forge:build {ID}` | TDD 구현 시작 |
| `/forge:verify {ID}` | 요구사항 검증 |
| `/forge:status` | 현재 상태 확인 |
| `/forge:list` | 모든 PRD 목록 |
| `/forge:resume {ID}` | 중단된 작업 재개 |

## 디렉토리 구조

```
project/
├── .claude/
│   ├── agents/           # 기본 에이전트 (4개)
│   ├── commands/forge/   # 슬래시 명령어 (7개)
│   ├── skills/           # 코딩 패턴 스킬
│   ├── hooks/            # 훅 (statusline, session_start)
│   └── settings.json     # 권한 설정
│
├── .forge/
│   ├── prds/             # PRD 문서들
│   ├── tasks/            # 태스크 분해 결과
│   ├── agents/           # 동적 생성된 에이전트
│   ├── progress/         # 진행 상황 및 체크포인트
│   ├── reports/          # 검증 리포트
│   └── config.json       # IdeaForge 설정
│
├── .mcp.json             # MCP 서버 설정
├── CLAUDE.md             # 프로젝트 지시문
└── README.md
```

## 에이전트

### 기본 에이전트

| 에이전트 | 역할 |
|----------|------|
| `forge-orchestrator` | 메인 오케스트레이터 |
| `forge-prd-writer` | PRD 작성 전문가 |
| `forge-analyzer` | PRD 분석, 에이전트/태스크 생성 |
| `forge-tdd-runner` | TDD 사이클 실행 |

### 동적 생성 에이전트

PRD 분석 후 필요에 따라 자동 생성:

- `expert-backend`: API, 서버, 인증
- `expert-frontend`: UI, 컴포넌트
- `expert-database`: 스키마, 쿼리
- `expert-security`: 보안, 암호화
- `expert-devops`: 배포, CI/CD

## TDD 워크플로우

```
🔴 RED      → 테스트 작성, 실패 확인
🟢 GREEN   → 최소 구현, 테스트 통과
🔵 REFACTOR → 코드 개선, 테스트 유지
```

## 요구사항

- Python >= 3.10
- Claude Code
- Node.js >= 18 (MCP 서버용)
- Git

## MCP 서버

기본 포함:
- **Context7**: 최신 라이브러리 문서 참조
- **Sequential-Thinking**: 복잡한 분석 및 설계

## 예제

### 실시간 채팅 앱

`examples/chat-app/` - IdeaForge 워크플로우로 생성된 실시간 채팅 애플리케이션

```bash
cd examples/chat-app
uv venv && source .venv/bin/activate
uv pip install -e .
pytest  # 테스트 실행
```

**생성 과정:**
```
/forge:idea "실시간 채팅 기능"     → CHAT-001.md 생성
/forge:analyze CHAT-001           → 에이전트 3개 자동 생성
/forge:build CHAT-001             → TDD로 구현
/forge:verify CHAT-001            → 검증 완료
```

## 라이선스

[MIT](LICENSE)

## 기여

기여를 환영합니다! [Issue](https://github.com/Hoyuo/idea-forge-kit/issues)나 [PR](https://github.com/Hoyuo/idea-forge-kit/pulls)을 자유롭게 제출해주세요.
