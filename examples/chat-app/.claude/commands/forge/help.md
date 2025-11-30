# /forge:help - IdeaForge 도움말

이 명령어는 IdeaForge의 모든 기능을 안내합니다.

---

## 출력 내용

아래 내용을 보기 좋게 표시해주세요:

```
🔥 IdeaForge - 아이디어에서 구현까지 자동화

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 워크플로우
   💡 아이디어 → 📄 PRD → 🤖 에이전트 → 🔨 TDD → ✅ 완료

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎮 명령어

   /forge:idea "아이디어"    아이디어를 PRD로 변환
   /forge:analyze {ID}      PRD 분석, 에이전트/태스크 자동 생성
   /forge:build {ID}        TDD 구현 시작 (RED-GREEN-REFACTOR)
   /forge:verify {ID}       요구사항 검증 및 리포트 생성

   /forge:status            현재 상태 확인
   /forge:list              모든 PRD 목록
   /forge:resume {ID}       중단된 작업 재개
   /forge:help              이 도움말

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 에이전트

   기본 에이전트 (항상 포함):
   ├── forge-orchestrator   메인 오케스트레이터
   ├── forge-prd-writer     PRD 작성 전문가
   ├── forge-analyzer       PRD 분석가
   └── forge-tdd-runner     TDD 실행자

   동적 생성 (PRD 분석 후):
   ├── expert-backend       API, 서버, 인증
   ├── expert-frontend      UI, 컴포넌트
   ├── expert-database      스키마, 쿼리
   ├── expert-security      보안, 암호화
   └── expert-devops        배포, CI/CD

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧪 TDD 워크플로우

   🔴 RED      테스트 작성 → 실패 확인
   🟢 GREEN    최소 구현 → 테스트 통과
   🔵 REFACTOR 코드 개선 → 테스트 유지

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 디렉토리 구조

   .forge/
   ├── prds/       PRD 문서
   ├── tasks/      태스크 분해
   ├── agents/     동적 생성 에이전트
   ├── progress/   체크포인트
   └── reports/    검증 리포트

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 빠른 시작

   1. /forge:idea "실시간 채팅 기능"
   2. /forge:analyze CHAT-001
   3. /forge:build CHAT-001
   4. /forge:verify CHAT-001

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
