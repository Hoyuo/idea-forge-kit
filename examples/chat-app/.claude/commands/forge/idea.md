# /forge:idea - 아이디어를 PRD로 변환

## 사용법

```
/forge:idea "OAuth 기반 사용자 인증 시스템"
/forge:idea "실시간 채팅 기능"
/forge:idea "상품 결제 및 주문 관리"
```

## 입력

`$ARGUMENTS` - 사용자의 아이디어 (자연어)

## 언어 설정

`.forge/config.json`에서 읽기:
- `language.conversation`: 질문/응답 언어
- `language.output_documents`: PRD 문서 언어

---

## 워크플로우

### Phase 1: 아이디어 초기 분석

사용자 아이디어: `$ARGUMENTS`

아이디어에서 핵심 요소 추출:
- 주요 기능 키워드
- 예상 도메인 (backend, frontend, database, security 등)
- 초기 복잡도 예측

### Phase 2: 소크라테스식 질문

**AskUserQuestion 도구**를 사용하여 아이디어를 구체화합니다.

#### 질문 세트 1: 기본 정보

```
AskUserQuestion([
  {
    "question": "이 기능의 주요 목적은 무엇인가요?",
    "header": "목적",
    "options": [
      {"label": "신규 기능", "description": "완전히 새로운 기능 개발"},
      {"label": "기존 개선", "description": "기존 기능 개선 또는 리팩토링"},
      {"label": "버그 수정", "description": "기존 문제 해결"},
      {"label": "PoC/프로토타입", "description": "개념 검증용 빠른 구현"}
    ],
    "multiSelect": false
  },
  {
    "question": "예상 사용자 규모는 어느 정도인가요?",
    "header": "규모",
    "options": [
      {"label": "소규모", "description": "100명 이하, 개인/팀 프로젝트"},
      {"label": "중규모", "description": "100~1,000명, 스타트업/중소기업"},
      {"label": "대규모", "description": "1,000명 이상, 엔터프라이즈"},
      {"label": "미정", "description": "아직 결정되지 않음"}
    ],
    "multiSelect": false
  }
])
```

#### 질문 세트 2: 기술 요구사항

```
AskUserQuestion([
  {
    "question": "선호하는 기술 스택이 있나요?",
    "header": "기술스택",
    "options": [
      {"label": "Python", "description": "FastAPI, Django, Flask 등"},
      {"label": "JavaScript/TS", "description": "Node.js, Next.js, React 등"},
      {"label": "Go", "description": "Gin, Echo, Fiber 등"},
      {"label": "자동 선택", "description": "요구사항에 맞게 AI가 추천"}
    ],
    "multiSelect": false
  },
  {
    "question": "기존 시스템과 연동이 필요한가요?",
    "header": "연동",
    "options": [
      {"label": "신규 프로젝트", "description": "처음부터 새로 구축"},
      {"label": "기존 연동", "description": "기존 API/DB와 연동 필요"},
      {"label": "마이그레이션", "description": "기존 시스템 교체"}
    ],
    "multiSelect": false
  }
])
```

#### 질문 세트 3: 비기능 요구사항 (선택적)

복잡도가 medium 이상으로 예측되면 추가 질문:

```
AskUserQuestion([
  {
    "question": "중요하게 고려할 비기능 요구사항은?",
    "header": "NFR",
    "options": [
      {"label": "성능", "description": "응답시간, 처리량 중요"},
      {"label": "보안", "description": "인증, 암호화, 감사 로그"},
      {"label": "확장성", "description": "수평 확장, 마이크로서비스"},
      {"label": "기본값", "description": "일반적인 수준으로 충분"}
    ],
    "multiSelect": true
  }
])
```

### Phase 3: PRD ID 생성

**ID 생성 규칙:**

| 키워드 | PREFIX | 예시 |
|--------|--------|------|
| auth, login, oauth, jwt | AUTH | AUTH-001 |
| chat, message, realtime | CHAT | CHAT-001 |
| payment, order, cart | PAY | PAY-001 |
| user, profile, account | USER | USER-001 |
| api, endpoint, rest | API | API-001 |
| admin, dashboard, manage | ADMIN | ADMIN-001 |
| search, filter, query | SEARCH | SEARCH-001 |
| file, upload, storage | FILE | FILE-001 |
| notification, alert, push | NOTI | NOTI-001 |
| 기타 | FEAT | FEAT-001 |

**번호 할당:**
1. `.forge/prds/` 디렉토리 확인
2. 동일 PREFIX의 기존 PRD 검색
3. 다음 번호 할당 (001, 002, ...)

### Phase 4: 복잡도 판단

| 복잡도 | 기준 | 예상 시간 |
|--------|------|-----------|
| **simple** | FR 3개 이하, 단일 도메인 | 2-4시간 |
| **medium** | FR 4-7개, 2-3개 도메인 | 4-12시간 |
| **complex** | FR 8개 이상, 4개+ 도메인, 외부 연동 | 12시간+ |

### Phase 5: PRD 생성

**저장 위치**: `.forge/prds/{ID}.md`

```markdown
---
id: {ID}
title: "{TITLE}"
status: draft
created: {ISO-DATE}
priority: {low|medium|high}
complexity: {simple|medium|complex}
---

# {ID}: {TITLE}

## 1. 개요

### 목표
{사용자 답변 기반으로 작성}

### 대상 사용자
{규모 및 특성}

### 제약사항
{기술 스택, 연동 요구사항 등}

## 2. 기능 요구사항 (Functional Requirements)

### 핵심 기능
- [ ] FR-001: {핵심 기능 1}
- [ ] FR-002: {핵심 기능 2}
- [ ] FR-003: {핵심 기능 3}

### 부가 기능
- [ ] FR-004: {부가 기능 1}

## 3. 비기능 요구사항 (Non-Functional Requirements)

- [ ] NFR-001: {성능/보안/확장성 요구사항}
- [ ] NFR-002: {추가 NFR}

## 4. 기술 스택 제안

- **Language**: {언어}
- **Framework**: {프레임워크}
- **Database**: {데이터베이스}
- **기타**: {필요시}

### 선택 이유
{기술 스택 선택 근거}

## 5. 예상 에이전트

> `/forge:analyze` 실행 후 자동 업데이트

## 6. 태스크 분해

> `/forge:analyze` 실행 후 자동 업데이트

## 7. 성공 기준

- [ ] {측정 가능한 성공 기준 1}
- [ ] {측정 가능한 성공 기준 2}

## 8. 참고 자료

- {관련 문서/API 링크}
```

### Phase 6: 완료 메시지

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ PRD 생성 완료!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 PRD 정보:
   ID: {ID}
   제목: {TITLE}
   위치: .forge/prds/{ID}.md

📊 분석 결과:
   기능 요구사항: {N}개
   비기능 요구사항: {M}개
   예상 복잡도: {simple|medium|complex}
   예상 도메인: {backend, frontend, ...}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
다음 단계:
   /forge:analyze {ID}  → 에이전트 자동 생성 및 태스크 분해
   /forge:status        → 프로젝트 상태 확인
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 도메인별 예시

### 예시 1: 인증 시스템

```
/forge:idea "OAuth 소셜 로그인이 포함된 사용자 인증"

→ ID: AUTH-001
→ 도메인: backend, security, database
→ FR: 회원가입, 로그인, OAuth, 토큰 관리, 비밀번호 재설정
→ 복잡도: medium
```

### 예시 2: 실시간 채팅

```
/forge:idea "1:1 실시간 채팅 기능"

→ ID: CHAT-001
→ 도메인: backend, frontend, database
→ FR: 채팅방 생성, 메시지 송수신, 히스토리, 읽음 표시
→ 복잡도: medium
```

### 예시 3: 결제 시스템

```
/forge:idea "상품 결제 및 주문 관리 시스템"

→ ID: PAY-001
→ 도메인: backend, database, security
→ FR: 장바구니, 결제 연동, 주문 관리, 환불 처리
→ 복잡도: complex
```

### 예시 4: 간단한 API

```
/forge:idea "할 일 목록 REST API"

→ ID: API-001
→ 도메인: backend, database
→ FR: CRUD 엔드포인트, 필터링, 페이지네이션
→ 복잡도: simple
```

---

## 주의사항

1. **계획 모드**: 이 명령은 PRD만 생성하며 코드를 작성하지 않음
2. **중복 확인**: 동일 ID의 PRD가 있으면 덮어쓰기 전 확인
3. **최소 질문**: 간단한 아이디어는 질문 세트 1만 사용
4. **Write 도구 사용**: PRD 파일 저장 시 Write 도구 사용

## 관련 명령어

| 명령어 | 용도 |
|--------|------|
| `/forge:analyze {ID}` | PRD 분석, 에이전트/태스크 생성 |
| `/forge:list` | 모든 PRD 목록 확인 |
| `/forge:status` | 프로젝트 상태 확인 |
