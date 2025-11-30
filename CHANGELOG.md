# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-11-30

### Added

- **CLI 명령어**: `forge init`, `forge doctor`, `forge status`, `forge list`
- **슬래시 명령어**: 12개 (`/forge:idea`, `/forge:analyze`, `/forge:build`, `/forge:verify` 등)
- **기본 에이전트**: 4개 (orchestrator, prd-writer, analyzer, tdd-runner)
- **동적 에이전트 시스템**: PRD 분석 기반 8개 도메인 에이전트 자동 생성
- **TDD 워크플로우**: RED-GREEN-REFACTOR 사이클 자동화
- **체크포인트 시스템**: 작업 중단/재개 지원
- **MCP 서버 통합**: Context7, Sequential-Thinking
- **소크라테스식 질문**: AskUserQuestion 기반 PRD 구체화

### Technical

- Python 3.10+ 지원
- Click 기반 CLI
- Rich 터미널 UI
- Jinja2 템플릿 엔진

[Unreleased]: https://github.com/Hoyuo/idea-forge-kit/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Hoyuo/idea-forge-kit/releases/tag/v0.1.0
