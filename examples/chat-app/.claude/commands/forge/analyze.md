# /forge:analyze - PRD 분석 및 에이전트 자동 생성

## 사용법

```
/forge:analyze AUTH-001
/forge:analyze CHAT-002
```

## 입력

`$ARGUMENTS` - 분석할 PRD ID

## 워크플로우

### 1. PRD 로드

```
📄 Loading: .forge/prds/{PRD_ID}.md
```

PRD 파일을 읽어 요구사항을 파싱합니다.

### 2. 도메인 분석

PRD의 요구사항에서 도메인 키워드를 추출합니다:

| 키워드 | 도메인 | 에이전트 |
|--------|--------|----------|
| api, server, endpoint | Backend | expert-backend |
| ui, component, page | Frontend | expert-frontend |
| database, schema, query | Database | expert-database |
| auth, oauth, jwt | Security | expert-security |
| docker, deploy, ci/cd | DevOps | expert-devops |

### 3. 에이전트 자동 생성

식별된 도메인별로 전문 에이전트를 생성합니다.

**저장 위치**: `.forge/agents/{PRD_ID}/expert-{domain}.md`

**에이전트 템플릿**:
```markdown
---
name: expert-{domain}
description: {PRD_ID} {domain} 구현 전문가
model: sonnet
context:
  prd: {PRD_ID}
  focus: [{할당된 FR 목록}]
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# {PRD_ID} {Domain} Expert

## 담당 요구사항
{PRD에서 할당된 요구사항}

## 기술 스택
{PRD의 기술 스택}

## TDD 규칙
1. 테스트 먼저 작성 (tests/ 디렉토리)
2. 최소한의 코드로 통과
3. 리팩토링
```

### 4. 태스크 분해

각 요구사항을 실행 가능한 태스크로 분해합니다.

**저장 위치**: `.forge/tasks/{PRD_ID}/tasks.json`

```json
{
  "prd_id": "{PRD_ID}",
  "created": "{ISO-DATE}",
  "total_tasks": {N},
  "tasks": [
    {
      "id": "FR-001",
      "title": "{태스크 제목}",
      "agent": "expert-{domain}",
      "dependencies": [],
      "complexity": "medium",
      "status": "pending"
    }
  ]
}
```

### 5. PRD 업데이트

분석 결과를 원본 PRD에 업데이트합니다:
- Section 5: 예상 에이전트 → 실제 생성된 에이전트
- Section 6: 태스크 분해 → 실제 태스크 목록
- status: draft → analyzed

### 6. 완료 메시지

```
✅ PRD 분석 완료: {PRD_ID}

🤖 생성된 에이전트 ({N}개):
   📁 .forge/agents/{PRD_ID}/
   ├── expert-backend.md    (FR-001, FR-002)
   ├── expert-frontend.md   (FR-003)
   └── expert-database.md   (FR-004)

📋 태스크 분해 ({M}개):
   1. [backend]  FR-001: 로그인 API 구현
   2. [backend]  FR-002: OAuth 연동
   3. [frontend] FR-003: 로그인 페이지 UI
   4. [database] FR-004: 사용자 테이블 설계

📊 복잡도 분석:
   - Simple: 2개
   - Medium: 1개
   - Complex: 1개

👉 다음 단계:
   /forge:build {PRD_ID}  - TDD 구현 시작
   /forge:status          - 상태 확인
```

## 주의사항

- Sequential-Thinking MCP를 사용하여 복잡한 분석 수행
- Context7 MCP로 기술 스택의 최신 문서 참조
- 에이전트 생성 전 사용자 확인 (AskUserQuestion)
