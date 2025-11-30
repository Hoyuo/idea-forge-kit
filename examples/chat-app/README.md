# 실시간 채팅 앱 예제

> 이 프로젝트는 **IdeaForge v0.1.0**으로 생성되었습니다.

## 개요

IdeaForge 워크플로우를 통해 생성된 실시간 1:1 채팅 애플리케이션입니다.

## 생성 과정

```bash
/forge:idea "실시간 채팅 기능"     # → CHAT-001.md 생성
/forge:analyze CHAT-001           # → 에이전트 3개 자동 생성
/forge:build CHAT-001             # → TDD로 구현
/forge:verify CHAT-001            # → 검증 완료
```

## 생성된 에이전트

| 에이전트 | 역할 |
|----------|------|
| `expert-backend` | API, WebSocket 핸들러 |
| `expert-database` | 스키마 설계, 쿼리 |
| `expert-security` | JWT 인증, 보안 |

## 실행 방법

```bash
cd examples/chat-app
uv venv && source .venv/bin/activate
uv pip install -e .
pytest  # 테스트 실행
```

## 기술 스택

- Python 3.11+
- FastAPI
- SQLite
- WebSocket

## 구조

```
src/
├── api/routes/     # API 엔드포인트
├── core/           # 설정, 보안
├── models/         # SQLAlchemy 모델
├── schemas/        # Pydantic 스키마
└── websocket/      # WebSocket 매니저

tests/              # 테스트 코드 (12개 파일)
```

## 최신 버전으로 새로 생성하기

```bash
forge init my-chat-app
cd my-chat-app
claude
/forge:idea "실시간 채팅 기능"
```
