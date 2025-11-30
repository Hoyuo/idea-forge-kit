# IdeaForge Project Instructions

> **IdeaForge**: 아이디어에서 구현까지 자동화하는 AI 개발 킷

---

## 핵심 워크플로우

```
💡 아이디어 → 📋 PRD → 🤖 에이전트 → 🔨 TDD → ✅ 완료

/forge:idea     → PRD 생성
/forge:analyze  → 에이전트 자동 생성 + 태스크 분해
/forge:build    → TDD 구현 (RED-GREEN-REFACTOR)
/forge:verify   → 요구사항 검증
```

---

## 슬래시 명령어

| 명령어 | 용도 |
|--------|------|
| `/forge:idea "아이디어"` | 아이디어를 PRD로 변환 |
| `/forge:analyze {ID}` | PRD 분석, 에이전트/태스크 자동 생성 |
| `/forge:build {ID}` | TDD 구현 시작 |
| `/forge:verify {ID}` | 요구사항 검증 |
| `/forge:status` | 현재 상태 확인 |
| `/forge:list` | 모든 PRD 목록 |
| `/forge:resume {ID}` | 중단된 작업 재개 |

---

## 디렉토리 구조

```
.forge/
├── prds/           # PRD 문서들
├── tasks/          # 태스크 분해 결과
├── agents/         # 동적 생성된 에이전트
├── progress/       # 진행 상황 및 체크포인트
├── reports/        # 검증 리포트
└── config.json     # 설정

.claude/
├── agents/         # 기본 에이전트 (4개)
├── commands/forge/ # 슬래시 명령어 (7개)
├── skills/         # 스킬
└── settings.json   # 권한 설정
```

---

## 에이전트 체계

### 기본 에이전트 (항상 포함)

| 에이전트 | 역할 |
|----------|------|
| `forge-orchestrator` | 메인 오케스트레이터, 워크플로우 조율 |
| `forge-prd-writer` | PRD 작성 전문가 |
| `forge-analyzer` | PRD 분석, 에이전트/태스크 생성 |
| `forge-tdd-runner` | TDD 사이클 실행 |

### 동적 생성 에이전트 (PRD 분석 후)

| 에이전트 | 도메인 |
|----------|--------|
| `expert-backend` | API, 서버, 인증 |
| `expert-frontend` | UI, 컴포넌트 |
| `expert-database` | 스키마, 쿼리 |
| `expert-security` | 보안, 암호화 |
| `expert-devops` | 배포, CI/CD |

---

## TDD 워크플로우

```
🔴 RED      → 테스트 작성, 실패 확인
🟢 GREEN   → 최소 구현, 테스트 통과
🔵 REFACTOR → 코드 개선, 테스트 유지
```

각 태스크마다 이 사이클을 반복합니다.

---

## 체크포인트 시스템

작업 중 언제든 중단해도 `.forge/progress/{ID}/checkpoint.json`에 상태가 저장됩니다.

`/forge:resume {ID}`로 중단된 지점에서 재개할 수 있습니다.

---

## MCP 서버

- **Context7**: 최신 라이브러리 문서 참조 (할루시네이션 방지)
- **Sequential-Thinking**: 복잡한 분석 및 설계

---

## 언어 설정

기본 응답 언어: 한국어
코드 주석: 영어/한국어 혼용 가능
