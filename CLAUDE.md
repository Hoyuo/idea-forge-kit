# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

IdeaForge는 아이디어에서 구현까지 자동화하는 AI 개발 킷입니다. 아이디어 하나로 PRD 생성 → 에이전트 자동 생성 → TDD 구현 → 완료까지의 워크플로우를 지원합니다.

## 빌드 및 개발 명령어

```bash
# 개발 환경 설정
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# 린트
ruff check src/

# 타입 체크
mypy src/

# 테스트 실행
pytest

# 단일 테스트 실행
pytest tests/test_specific.py::test_function -v

# CLI 실행
forge init my-project
forge doctor
forge status
forge list
```

## 아키텍처

### 핵심 구조

```
src/ideaforge/
├── cli/main.py              # Click 기반 CLI (forge 명령어)
└── templates/               # 프로젝트 초기화 시 복사되는 템플릿
    ├── .claude/
    │   ├── agents/          # 9개 기본 에이전트 (orchestrator, prd-writer, analyzer, tdd-runner 등)
    │   ├── commands/forge/  # 12개 슬래시 명령어 (idea, analyze, build, verify 등)
    │   ├── hooks/lib/       # 공유 Python 모듈 (agent_generator, prd_analyzer 등)
    │   └── skills/          # 코딩 패턴 스킬
    ├── .forge/              # IdeaForge 작업 디렉토리 템플릿
    ├── .mcp.json            # MCP 서버 설정 (Context7, Sequential-Thinking)
    └── CLAUDE.md            # 생성된 프로젝트용 지시문
```

### 워크플로우

```
/forge:idea "아이디어" → PRD 생성 (.forge/prds/)
/forge:analyze {ID}   → 에이전트 자동 생성 (.forge/agents/{ID}/)
/forge:build {ID}     → TDD 구현 (RED → GREEN → REFACTOR)
/forge:verify {ID}    → 요구사항 검증 (.forge/reports/)
```

### 동적 에이전트 시스템 (v2.0)

PRD 분석 후 8개 도메인에서 필요한 에이전트만 자동 생성:
- `expert-backend`, `expert-frontend`, `expert-database`, `expert-security`
- `expert-devops`, `expert-testing`, `expert-mobile`, `expert-ai`

에이전트 생성 로직: `templates/.claude/hooks/lib/agent_generator.py`

### CLI 진입점

`pyproject.toml`에서 정의: `forge` 및 `ideaforge` → `ideaforge.cli.main:cli`

### 템플릿 복사 방식

`forge init` 실행 시 `src/ideaforge/templates/` 디렉토리 전체가 대상 프로젝트로 복사됨.

## 주요 의존성

- `click`: CLI 프레임워크
- `rich`: 터미널 UI
- `pydantic`: 데이터 검증
- `jinja2`: 템플릿 엔진
- `pyyaml`: YAML 처리

## 테스트

테스트 경로: `tests/`
커버리지 포함 실행: `pytest -v --cov=ideaforge`

## Git 커밋 컨벤션

[gitmoji](https://gitmoji.dev/) 사용:

| 이모지 | 코드 | 용도 |
|--------|------|------|
| 🎉 | `:tada:` | 초기 커밋 |
| ✨ | `:sparkles:` | 새 기능 |
| 🐛 | `:bug:` | 버그 수정 |
| 📝 | `:memo:` | 문서 추가/수정 |
| ♻️ | `:recycle:` | 리팩토링 |
| 🔧 | `:wrench:` | 설정 파일 |
| ✅ | `:white_check_mark:` | 테스트 추가/수정 |
| 🚀 | `:rocket:` | 배포 |
| 🔥 | `:fire:` | 코드/파일 삭제 |
| 💄 | `:lipstick:` | UI/스타일 |

**커밋 메시지 형식:**
```
<gitmoji> <제목>

<본문 (선택)>
```

**예시:**
```
✨ PRD 생성 시 복잡도 자동 판단 기능 추가

- simple/medium/complex 3단계 분류
- FR 개수와 도메인 수 기준으로 판단
```
