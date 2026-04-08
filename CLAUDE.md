# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

**김지윤 키우기** — LLM 기반 인터랙티브 캐릭터 챗 시뮬레이션 게임.

전직 초등학교 국어선생님 29세 김지윤이 SSAFY 15기 서울 6반에서 SW 개발자로 성장하는 이야기. 플레이어는 AI 캐릭터들과 자유 대화하며 스토리를 진행한다.

## 콘텐츠 구조 규칙

- 캐릭터 설정: `charactor/{캐릭터이름}.md` — 성격, 말투, 세계관, 배경 등
- 시나리오: `scenario/scene_{N}.md` — 순번 순서대로 진행
- 트러블슈팅 기록: `trouble_shooting/trouble_shoot_{N}.md`
- 기획 문서: `제작_의뢰서.md` — 기능 명세 원본 (미완성 항목은 `[]` 표시)

## 게임 시스템 설계

### 엔딩 조건 (능력치 기반)
- 언변 능력치 최고 → 강사 취직
- 개발 능력치 최고 → 개발자 취직
- 기획 능력치 최고 → 기획자 취직
- 히든 엔딩: SSAFY 수료 기준 미달 퇴소
  - 과목 평가 10회 중 6회 이상 pass
  - 월말 평가 6회 중 3회 이상 pass
  - SW 역량 테스트 IM 등급
  - 결석 4회 미만 (월별 지각/조퇴 3회 누적 = 결석 1회, 누적 초기화 없음)

### 이벤트 트리거
- 과목 평가 / 월말 평가 시행 시점
- 추가 조건은 `제작_의뢰서.md` 3.2절에 채워나갈 예정

### AI 모델
- Hugging Face 한국어 지원 chat 모델 사용 예정

## 기술 스택 (확정 전)

- 플랫폼: 웹
- 프론트엔드: 미결정 (`제작_의뢰서.md` 5.3절)
- AI: Hugging Face 한국어 chat 모델
- 필수 화면: 메인 / 채팅 / 설정

## 작업 관리 규칙

모든 작업 시 프로젝트 루트의 두 파일로 계획과 상태를 관리한다.

- **`plan.md`** — 작업 시작 전 목표, 완료 기준, 단계를 작성
- **`handoff.md`** — 작업 종료 후 완료된 것, 남은 이슈, 다음 단계를 기록

직접 작업이든 에이전트 팀 작업이든 동일하게 적용한다. 에이전트는 작업 시작 시 `handoff.md`를 읽어 이전 상태를 파악하고, 완료 후 업데이트한다.

## devlog 규칙

`devlog/` 폴더는 작업 단위로 개발 기록을 남기는 곳이다. 블로그 포스팅의 원본 자료이자, 에이전트가 맥락을 파악하는 소스다.

- **파일명**: `{작업_슬러그}.md` (예: `scene_based_refactor.md`, `llm_integration.md`)
- **작성 시점**: 작업이 완료되거나 의미 있는 결정이 내려졌을 때
- **템플릿**: `devlog/_template.md` 참조
- **필수 섹션**: 왜 이 작업을 했나 / 무엇을 만들었나 / 핵심 결정 사항 / 막혔던 점 / 다음 연결 작업
- **핵심 원칙**: "왜"를 반드시 기록한다. 무엇을 만들었는지보다 왜 그 방식을 선택했는지가 더 중요하다.
- 에이전트는 새 작업 시작 시 관련 devlog 파일을 읽어 맥락을 파악한다.

## 워크스페이스 대시보드

`claude-workspace-dashboard-template/` — `~/.claude/` 디렉토리를 시각화하는 읽기 전용 로컬 도구. 게임 코드와 무관.

```bash
cd claude-workspace-dashboard-template
python3 server.py   # http://localhost:8080
```

서버 검증: `python3 -c "import server"`

JS 수정 후 검증: `node -c dist/assets/index-DYwNDC3K.js`

**주의**: `server.py`는 read-only mock — PUT/POST/DELETE는 실제 파일 변경 없음. `dist/` 파일 통째로 덮어쓰지 말 것.
