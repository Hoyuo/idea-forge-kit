# /forge:resume - 중단된 작업 재개

## 사용법

```
/forge:resume AUTH-001
```

## 입력

`$ARGUMENTS` - 재개할 PRD ID

## 워크플로우

### 1. 체크포인트 확인

```
🔄 Resuming: AUTH-001
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 Checkpoint found!
```

체크포인트 파일 로드: `.forge/progress/{PRD_ID}/checkpoint.json`

### 2. 상태 복원

```
📋 Previous State:
   ├── Last Task: FR-003 (비밀번호 재설정)
   ├── Last Phase: GREEN
   ├── Completed: FR-001, FR-002
   ├── Pending: FR-004, NFR-001
   └── Last Updated: 2024-11-30 15:30

📊 Progress: ████████████░░░░░░░░░░░░░░░░ 45%
```

### 3. 재개 확인

AskUserQuestion으로 확인:

```
❓ 작업을 재개하시겠습니까?

Options:
1. 중단점에서 계속 (FR-003 GREEN phase)
2. 현재 태스크 처음부터 (FR-003 RED phase)
3. 다음 태스크로 건너뛰기 (FR-004)
4. 취소
```

### 4. 작업 재개

선택에 따라 `/forge:build` 호출:

**Option 1: 중단점에서 계속**
```
🔄 Resuming from checkpoint...

Task: FR-003 비밀번호 재설정
Phase: GREEN (continue)

[GREEN phase 계속 진행]
```

**Option 2: 태스크 처음부터**
```
🔄 Restarting task FR-003...

Task: FR-003 비밀번호 재설정
Phase: RED (restart)

[TDD 사이클 처음부터]
```

**Option 3: 다음 태스크로**
```
⏭️ Skipping to next task...

Skipped: FR-003 (marked as skipped)
Next: FR-004 세션 관리

[FR-004부터 시작]
```

### 5. 체크포인트가 없을 때

```
⚠️ No checkpoint found for AUTH-001

가능한 조치:
1. /forge:build AUTH-001    - 처음부터 빌드
2. /forge:status AUTH-001   - 상태 확인
```

### 6. 에러 복구

이전 실패로 중단된 경우:

```
❌ Previous Error Detected:

Task: FR-003
Phase: GREEN
Error: pytest failed - 2 tests failing

📄 Error Log: .forge/progress/AUTH-001/error.log

Options:
1. 에러 로그 확인 후 재시도
2. 수동으로 수정 후 재개
3. 태스크 건너뛰기
```

### 7. 완료 후 상태 저장

재개 후 정상적으로 진행되면 체크포인트 업데이트:

```json
{
  "prd_id": "AUTH-001",
  "resumed_at": "2024-11-30T16:00:00Z",
  "resumed_from": {
    "task": "FR-003",
    "phase": "GREEN"
  },
  "current_task": "FR-003",
  "current_phase": "REFACTOR",
  ...
}
```
