# /forge:idea - 아이디어를 PRD로 변환

## 사용법

```
/forge:idea "사용자 인증 시스템 with OAuth"
/forge:idea "실시간 채팅 기능"
```

## 입력

`$ARGUMENTS` - 사용자의 아이디어 (자연어)

## 워크플로우

### 1. 아이디어 분석

사용자 아이디어: `$ARGUMENTS`

이 아이디어를 분석하여 핵심 요소를 파악합니다:
- 주요 기능
- 예상 기술 스택
- 복잡도 수준

### 2. 소크라테스식 질문

아이디어를 명확히 하기 위해 AskUserQuestion을 사용하여 질문합니다:

1. **목적**: 이 기능의 주요 목적은 무엇인가요?
2. **사용자**: 주요 사용자는 누구인가요?
3. **기존 시스템**: 기존 시스템과 연동이 필요한가요?
4. **기술 스택**: 선호하는 기술 스택이 있나요?
5. **규모**: 예상 사용량/규모는 어떻게 되나요?

### 3. PRD 생성

수집된 정보를 바탕으로 구조화된 PRD를 생성합니다.

**PRD ID 생성 규칙**:
- 아이디어 키워드에서 PREFIX 추출 (AUTH, CHAT, API 등)
- 기존 PRD 확인하여 다음 번호 부여
- 형식: `{PREFIX}-{001~999}`

**저장 위치**: `.forge/prds/{ID}.md`

### 4. PRD 템플릿

```markdown
---
id: {ID}
title: "{TITLE}"
status: draft
created: {ISO-DATE}
priority: medium
---

# {ID}: {TITLE}

## 1. 개요
{프로젝트 개요}

## 2. 기능 요구사항 (Functional Requirements)
- [ ] FR-001: {기능 1}
- [ ] FR-002: {기능 2}

## 3. 비기능 요구사항 (Non-Functional Requirements)
- [ ] NFR-001: {성능/보안 요구사항}

## 4. 기술 스택 제안
- Language:
- Framework:
- Database:

## 5. 예상 에이전트
{/forge:analyze 후 업데이트}

## 6. 태스크 분해
{/forge:analyze 후 업데이트}

## 7. 성공 기준
- {성공 기준}
```

### 5. 완료 메시지

```
✅ PRD 생성 완료!

📋 ID: {ID}
📄 Title: {TITLE}
📁 Location: .forge/prds/{ID}.md

📊 Summary:
   - 기능 요구사항: {N}개
   - 비기능 요구사항: {M}개
   - 예상 복잡도: {low|medium|high}

👉 다음 단계:
   /forge:analyze {ID}  - PRD 분석 및 에이전트 생성
   /forge:status        - 프로젝트 상태 확인
```

## 주의사항

- Planning Mode: 이 명령어는 PRD 생성만 수행하며 코드를 작성하지 않습니다
- PRD 파일을 Write 도구로 저장합니다
- 기존 같은 ID의 PRD가 있으면 덮어쓰기 전 확인합니다
