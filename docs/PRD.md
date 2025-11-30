# IdeaForge PRD (Product Requirements Document)

> **프로젝트명**: IdeaForge - 아이디어에서 구현까지 자동화하는 AI 개발 킷
> **버전**: 0.1.0 (Draft)
> **작성일**: 2024-11-30
> **목표**: Clavix의 PRD 워크플로우 + MoAI-ADK의 에이전트 오케스트레이션 결합

---

## 1. 개요

### 1.1 비전

**"아이디어 하나로 PRD 생성 → 에이전트 자동 생성 → TDD 구현 → 완료"**

개발자가 아이디어만 입력하면, AI가 자동으로:
1. PRD(제품 요구사항 문서) 생성
2. 필요한 전문 에이전트 분석 및 생성
3. TDD 워크플로우로 구현
4. 진행 상황 실시간 추적

### 1.2 핵심 가치

| 가치 | 설명 |
|------|------|
| **Zero-to-Code** | 아이디어 → 동작하는 코드까지 자동화 |
| **Agent-on-Demand** | PRD 분석해서 필요한 에이전트만 동적 생성 |
| **TDD-First** | 항상 테스트 먼저, 품질 보장 |
| **Progress Visibility** | 모든 단계의 진행 상황 시각화 |

---

## 2. 사용자 스토리

### 2.1 기본 워크플로우

```
사용자: "실시간 채팅 기능을 만들고 싶어"

[Phase 1: Ideate] /forge:idea
├── 아이디어 분석 및 질문
├── PRD 자동 생성
└── PRD 저장 (.forge/prds/CHAT-001.md)

[Phase 2: Analyze] /forge:analyze CHAT-001
├── PRD 분석
├── 필요한 에이전트 식별:
│   ├── expert-backend (WebSocket 서버)
│   ├── expert-frontend (채팅 UI)
│   └── expert-database (메시지 저장)
├── 에이전트 자동 생성 (.claude/agents/)
└── 태스크 분해 (.forge/tasks/CHAT-001/)

[Phase 3: Build] /forge:build CHAT-001
├── TDD 사이클 (RED → GREEN → REFACTOR)
├── 각 태스크별 진행 상황 추적
├── 체크포인트 자동 저장
└── 완료 시 리포트 생성

[Phase 4: Verify] /forge:verify CHAT-001
├── 모든 테스트 통과 확인
├── PRD 요구사항 체크리스트 검증
├── 코드 품질 검사
└── 최종 리포트
```

### 2.2 상세 사용 시나리오

**시나리오 1: 새 아이디어에서 시작**
```bash
# 1. 아이디어 입력
/forge:idea "사용자 인증 시스템 with OAuth"

# AI가 질문하고 PRD 생성
# → .forge/prds/AUTH-001.md 생성

# 2. PRD 분석 및 에이전트 생성
/forge:analyze AUTH-001

# → 필요한 에이전트 자동 식별 및 생성
# → 태스크 분해

# 3. TDD 구현
/forge:build AUTH-001

# → RED-GREEN-REFACTOR 자동화
# → 실시간 진행 상황

# 4. 검증
/forge:verify AUTH-001
```

**시나리오 2: 기존 PRD에서 계속**
```bash
# 저장된 PRD 목록 확인
/forge:list

# 특정 PRD의 상태 확인
/forge:status AUTH-001

# 중단된 지점에서 계속
/forge:resume AUTH-001
```

---

## 3. 시스템 아키텍처

### 3.1 전체 구조

```
ideaforge/
├── src/ideaforge/
│   ├── cli/                    # CLI 명령어 (init, doctor, status)
│   │   └── main.py
│   │
│   ├── core/                   # 핵심 로직
│   │   ├── prd_generator.py    # PRD 생성 엔진
│   │   ├── agent_analyzer.py   # 에이전트 분석기
│   │   ├── task_decomposer.py  # 태스크 분해기
│   │   └── progress_tracker.py # 진행 상황 추적
│   │
│   ├── templates/              # 프로젝트 초기화 템플릿
│   │   ├── .claude/
│   │   │   ├── agents/         # 기본 에이전트
│   │   │   ├── commands/forge/ # 슬래시 명령어
│   │   │   ├── skills/         # 스킬
│   │   │   └── settings.json
│   │   ├── .forge/             # IdeaForge 작업 디렉토리
│   │   │   ├── prds/           # PRD 문서들
│   │   │   ├── tasks/          # 태스크 분해 결과
│   │   │   ├── agents/         # 동적 생성된 에이전트
│   │   │   ├── progress/       # 진행 상황 로그
│   │   │   └── config.json
│   │   ├── .mcp.json           # MCP 서버 설정
│   │   └── CLAUDE.md
│   │
│   └── __init__.py
│
├── pyproject.toml
└── README.md
```

### 3.2 명령어 체계

| 명령어 | 용도 | 모드 |
|--------|------|------|
| `/forge:idea` | 아이디어 → PRD 생성 | Planning |
| `/forge:analyze` | PRD 분석 → 에이전트/태스크 생성 | Planning |
| `/forge:build` | TDD 구현 실행 | Implementation |
| `/forge:verify` | 요구사항 검증 | Verification |
| `/forge:status` | 현재 진행 상황 확인 | Info |
| `/forge:list` | 모든 PRD 목록 | Info |
| `/forge:resume` | 중단된 작업 재개 | Implementation |

### 3.3 에이전트 체계

**기본 에이전트 (항상 포함)**:
```
.claude/agents/
├── forge-orchestrator.md    # 메인 오케스트레이터
├── forge-prd-writer.md      # PRD 작성 전문가
├── forge-analyzer.md        # 요구사항 분석가
└── forge-tdd-runner.md      # TDD 실행자
```

**동적 생성 에이전트 (PRD 분석 후 생성)**:
```
.forge/agents/{PRD-ID}/
├── expert-backend.md        # 백엔드 전문가 (필요시)
├── expert-frontend.md       # 프론트엔드 전문가 (필요시)
├── expert-database.md       # 데이터베이스 전문가 (필요시)
└── expert-{domain}.md       # 기타 도메인 전문가
```

---

## 4. 핵심 기능 상세

### 4.1 PRD 생성 (/forge:idea)

**입력**: 자연어 아이디어
**출력**: 구조화된 PRD 문서

**PRD 템플릿 구조**:
```markdown
---
id: AUTH-001
title: "사용자 인증 시스템"
status: draft | analyzing | building | complete
created: 2024-11-30
priority: high | medium | low
---

# AUTH-001: 사용자 인증 시스템

## 1. 개요
[AI가 아이디어를 분석하여 작성]

## 2. 기능 요구사항
- [ ] FR-001: 이메일/비밀번호 로그인
- [ ] FR-002: OAuth 소셜 로그인
- [ ] FR-003: 비밀번호 재설정

## 3. 비기능 요구사항
- [ ] NFR-001: 응답시간 < 200ms
- [ ] NFR-002: 보안 표준 준수

## 4. 기술 스택 제안
[AI가 분석하여 제안]

## 5. 예상 에이전트
[/forge:analyze 후 자동 업데이트]

## 6. 태스크 분해
[/forge:analyze 후 자동 업데이트]
```

**소크라테스식 질문 프로세스**:
```
1. "이 기능의 주요 사용자는 누구인가요?"
2. "기존 시스템과 연동이 필요한가요?"
3. "보안 수준은 어느 정도가 필요한가요?"
4. "예상 사용량/규모는 어떻게 되나요?"
5. "기술 스택 선호도가 있나요?"
```

### 4.2 에이전트 자동 생성 (/forge:analyze)

**입력**: PRD 문서
**출력**: 필요한 에이전트 + 태스크 분해

**에이전트 분석 로직**:
```python
# PRD 분석 → 도메인 식별 → 에이전트 매핑
domain_agent_map = {
    "authentication": ["expert-backend", "expert-security"],
    "database": ["expert-database"],
    "ui": ["expert-frontend", "expert-uiux"],
    "api": ["expert-backend"],
    "realtime": ["expert-backend", "expert-frontend"],
    "deployment": ["expert-devops"],
}
```

**생성되는 에이전트 템플릿**:
```markdown
---
name: expert-backend
description: AUTH-001 백엔드 구현 전문가
model: sonnet
tools: [Read, Write, Edit, Bash, Grep, Glob]
context:
  prd: AUTH-001
  focus: [FR-001, FR-002, FR-003]
---

# AUTH-001 백엔드 전문가

## 역할
이 PRD의 백엔드 관련 요구사항을 구현합니다.

## 담당 요구사항
- FR-001: 이메일/비밀번호 로그인
- FR-002: OAuth 소셜 로그인
- FR-003: 비밀번호 재설정

## 기술 스택
{PRD에서 정의된 기술 스택 - 언어/프레임워크 무관}

## TDD 규칙
1. 테스트 먼저 작성
2. 최소한의 코드로 통과
3. 리팩토링
```

### 4.3 TDD 구현 (/forge:build)

**워크플로우**:
```
┌─────────────────────────────────────────────────────────┐
│                    /forge:build AUTH-001                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Task 1/5: FR-001 이메일 로그인                          │
│  ├── [RED] 테스트 작성 → 실패 확인                       │
│  ├── [GREEN] 최소 구현 → 테스트 통과                     │
│  ├── [REFACTOR] 코드 개선                               │
│  └── ✅ 완료                                            │
│                                                         │
│  Task 2/5: FR-002 OAuth 로그인                          │
│  ├── [RED] 테스트 작성 중...                            │
│  │   └── 🔄 진행 중 (35%)                               │
│  ├── [ ] GREEN                                          │
│  └── [ ] REFACTOR                                       │
│                                                         │
│  Task 3-5: 대기 중                                      │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  전체 진행률: ████████░░░░░░░░░░░░ 40%                   │
│  예상 남은 시간: ~45분                                   │
└─────────────────────────────────────────────────────────┘
```

**체크포인트 자동 저장**:
```json
// .forge/progress/AUTH-001/checkpoint.json
{
  "prd_id": "AUTH-001",
  "current_task": "FR-002",
  "current_phase": "RED",
  "completed_tasks": ["FR-001"],
  "pending_tasks": ["FR-003", "NFR-001", "NFR-002"],
  "last_updated": "2024-11-30T15:30:00Z",
  "can_resume": true
}
```

### 4.4 진행 상황 추적 (/forge:status)

**실시간 상태 표시**:
```
┌─────────────────────────────────────────────────────────┐
│  🔨 IdeaForge Status: AUTH-001                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📋 PRD: 사용자 인증 시스템                              │
│  📊 Phase: Building                                     │
│  ⏱️  Started: 2시간 전                                  │
│                                                         │
│  ┌─ Progress ─────────────────────────────────────────┐ │
│  │                                                     │ │
│  │  Requirements: ████████████░░░░░░░░ 60% (3/5)      │ │
│  │  Tests:        ███████████████░░░░░ 75% (15/20)    │ │
│  │  Coverage:     ████████████████░░░░ 82%            │ │
│  │                                                     │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                         │
│  🤖 Active Agent: expert-backend                        │
│  📝 Current Task: FR-002 OAuth 로그인                   │
│  🔄 TDD Phase: GREEN (구현 중)                          │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  Commands:                                              │
│  • /forge:resume - 작업 계속                            │
│  • /forge:verify - 검증 실행                            │
│  • /forge:pause  - 작업 일시 중지                       │
└─────────────────────────────────────────────────────────┘
```

---

## 5. IdeaForge 개발 환경

> **참고**: 이 섹션은 IdeaForge CLI 도구 자체의 개발 환경입니다.
> IdeaForge로 생성되는 프로젝트는 **어떤 언어/프레임워크**든 사용 가능합니다.

### 5.1 IdeaForge CLI 개발 언어: Python

**선택 이유**:
- MoAI-ADK 스타일로 일관성 유지
- Claude Code와의 통합 용이
- 풍부한 AI/NLP 라이브러리 생태계
- uv를 통한 빠른 패키지 관리

### 5.2 의존성

```toml
[project]
name = "ideaforge"
version = "0.1.0"
dependencies = [
    "click>=8.0.0",      # CLI 프레임워크
    "rich>=13.0.0",      # 터미널 UI
    "pydantic>=2.0.0",   # 데이터 검증
    "jinja2>=3.0.0",     # 템플릿 엔진
    "pyyaml>=6.0.0",     # YAML 처리
]
```

### 5.3 MCP 서버 통합

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking@latest"]
    }
  }
}
```

---

## 6. 구현 로드맵

### Phase 1: 기반 구축 (Week 1-2)
- [ ] 프로젝트 구조 설정
- [ ] CLI 기본 명령어 (init, doctor, status)
- [ ] 템플릿 시스템 구축
- [ ] 기본 설정 파일 구조

### Phase 2: PRD 시스템 (Week 3-4)
- [ ] /forge:idea 명령어
- [ ] 소크라테스식 질문 로직
- [ ] PRD 템플릿 및 생성기
- [ ] PRD 저장/로드 시스템

### Phase 3: 에이전트 시스템 (Week 5-6)
- [ ] /forge:analyze 명령어
- [ ] 도메인 분석 로직
- [ ] 에이전트 자동 생성기
- [ ] 태스크 분해 로직

### Phase 4: TDD 워크플로우 (Week 7-8)
- [ ] /forge:build 명령어
- [ ] TDD 사이클 자동화
- [ ] 체크포인트 시스템
- [ ] 진행 상황 추적

### Phase 5: 검증 및 완성 (Week 9-10)
- [ ] /forge:verify 명령어
- [ ] 종합 리포트 생성
- [ ] 문서화
- [ ] 오픈소스 배포 준비

---

## 7. 성공 지표

| 지표 | 목표 |
|------|------|
| 아이디어 → PRD 생성 시간 | < 5분 |
| PRD → 에이전트 생성 시간 | < 2분 |
| TDD 사이클 자동화율 | > 80% |
| 요구사항 추적률 | 100% |
| 테스트 커버리지 | > 85% |

---

## 8. 경쟁 우위

### vs Clavix
- PRD뿐만 아니라 **에이전트 자동 생성**
- **TDD 워크플로우** 내장
- **진행 상황 실시간 추적**

### vs MoAI-ADK
- 더 **간단한 시작점** (아이디어 한 줄)
- **동적 에이전트 생성** (미리 정의 불필요)
- 더 **가벼운 설치** (핵심 기능만)

### 차별화 포인트
```
Clavix:      아이디어 → PRD → (수동 구현)
MoAI-ADK:    SPEC → (수동 에이전트 선택) → TDD
IdeaForge:   아이디어 → PRD → 자동 에이전트 → TDD → 완료
```

---

## 9. 리스크 및 대응

| 리스크 | 확률 | 대응 |
|--------|------|------|
| 에이전트 자동 생성 정확도 | 중 | 사용자 확인 단계 추가 |
| TDD 자동화 한계 | 중 | 수동 개입 옵션 제공 |
| 복잡한 PRD 처리 | 중 | 단계적 분해 지원 |

---

## 10. 다음 단계

1. **이 PRD 승인** 후 프로젝트 시작
2. **Phase 1** 기반 구축부터 시작
3. 각 Phase 완료 시 리뷰 및 조정

---

**프로젝트명 후보**:
- IdeaForge (아이디어 + 대장간)
- AutoDev (자동 개발)
- FlowKit (워크플로우 킷)
- BuildPilot (빌드 파일럿)

어떤 이름이 좋으신가요?
