# /forge:verify - 요구사항 검증

## 사용법

```
/forge:verify AUTH-001
```

## 입력

`$ARGUMENTS` - 검증할 PRD ID

## 워크플로우

### 1. 검증 준비

```
✔️ IdeaForge Verify: {PRD_ID}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

1. PRD 로드: `.forge/prds/{PRD_ID}.md`
2. 태스크 현황: `.forge/tasks/{PRD_ID}/tasks.json`
3. 진행 상황: `.forge/progress/{PRD_ID}/checkpoint.json`

### 2. 요구사항 체크리스트 검증

PRD의 각 요구사항에 대해:

```
📋 기능 요구사항 검증
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ FR-001: 이메일/비밀번호 로그인
   ├── 구현: src/auth/login.py ✓
   ├── 테스트: tests/test_auth.py::test_login ✓
   └── 커버리지: 92% ✓

✅ FR-002: OAuth 소셜 로그인
   ├── 구현: src/auth/oauth.py ✓
   ├── 테스트: tests/test_oauth.py ✓
   └── 커버리지: 88% ✓

⚠️ FR-003: 비밀번호 재설정
   ├── 구현: src/auth/password.py ✓
   ├── 테스트: tests/test_password.py ✓
   └── 커버리지: 65% ⚠️ (목표: 80%)

📋 비기능 요구사항 검증
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ NFR-001: 응답시간 < 200ms
   └── 측정값: 평균 145ms ✓

✅ NFR-002: 보안 표준 준수
   └── OWASP Top 10 체크 ✓
```

### 3. 테스트 실행

전체 테스트 스위트 실행:

```bash
pytest tests/ -v --cov=src --cov-report=html
```

결과:
```
📊 테스트 결과
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Tests: 24
├── Passed:  24 ✅
├── Failed:  0
├── Skipped: 0
└── Errors:  0

Coverage: 87%
├── src/auth/login.py     92%
├── src/auth/oauth.py     88%
├── src/auth/password.py  65% ⚠️
└── src/auth/session.py   95%
```

### 4. 코드 품질 검사

```
🔍 코드 품질
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Linting (ruff):
├── Errors: 0 ✅
├── Warnings: 2 ⚠️
└── Style: 98/100

Type Checking (mypy):
├── Errors: 0 ✅
└── Coverage: 85%

Complexity:
├── Avg Cyclomatic: 4.2 (good)
└── Max Cyclomatic: 8 (acceptable)
```

### 5. 최종 리포트 생성

`.forge/reports/{PRD_ID}-final.md`:

```markdown
# {PRD_ID} 검증 리포트

## 요약
- 상태: ✅ 통과 / ⚠️ 부분 통과 / ❌ 실패
- 검증일: {ISO-DATE}
- 소요시간: {BUILD_DURATION}

## 요구사항 충족률
- 기능 요구사항: 5/5 (100%)
- 비기능 요구사항: 2/2 (100%)

## 테스트 결과
- 전체: 24 tests
- 통과: 24 (100%)
- 커버리지: 87%

## 코드 품질
- Linting: Pass
- Type Check: Pass
- Complexity: Good

## 개선 권장사항
1. password.py 커버리지 향상 필요 (65% → 80%)
2. 경고 2건 해결 권장

## 생성된 파일
{파일 목록}
```

### 6. 완료 메시지

**성공 시**:
```
✅ 검증 완료: {PRD_ID}

📊 결과: PASSED

요구사항: 7/7 충족 (100%)
테스트: 24/24 통과
커버리지: 87%

📄 리포트: .forge/reports/{PRD_ID}-final.md

👉 다음 단계:
   - Git commit 권장
   - /forge:list 로 다른 PRD 확인
```

**부분 통과 시**:
```
⚠️ 검증 완료: {PRD_ID}

📊 결과: PARTIAL PASS

요구사항: 6/7 충족 (86%)
테스트: 22/24 통과
커버리지: 72% (목표: 80%)

❌ 미충족 항목:
   - FR-003: 커버리지 부족
   - NFR-002: 성능 미달

📄 리포트: .forge/reports/{PRD_ID}-final.md

🔧 권장 조치:
   /forge:build {PRD_ID} --task FR-003
```
