# 에이전트 팀 하네스 구성

## 왜 이 작업을 했나

코드가 전혀 없는 상태에서 MVP 마감이 5일 후였다. 혼자 백엔드, 프론트엔드, 캐릭터 콘텐츠, AI 연동을 순서대로 만들면 마감 안에 끝낼 수 없다. 처음부터 Claude Code 에이전트 팀을 구성해서 병렬로 작업하는 구조를 만들기로 했다.

## 무엇을 만들었나

### 에이전트 5인팀 (`Chat_Game/.claude/agents/`)
- `orchestrator.md` — 게임 오케스트레이터 (전체 Phase 조율, 팀원 작업 할당)
- `content-writer.md` — 콘텐츠 작가 (캐릭터 파일, 시나리오 작성)
- `frontend-dev.md` — 프론트엔드 개발자 (KakaoTalk 스타일 채팅 UI)
- `backend-dev.md` — 백엔드 개발자 (FastAPI API, 게임 상태 관리)
- `ai-integrator.md` — AI 통합 전문가 (HuggingFace 모델 연동, 캐릭터 프롬프트)

### 스킬 6개 (`Chat_Game/.claude/skills/`)
- `character-writer` — 캐릭터 `.md` 파일 작성 패턴
- `scenario-writer` — `scene_{N}.md` 시나리오 작성 패턴
- `chat-ui-builder` — KakaoTalk 스타일 채팅 UI 구축 패턴
- `game-api-builder` — FastAPI 게임 API 구축 패턴
- `llm-integrator` — HuggingFace 모델 연동 패턴
- `game-orchestrator` — 전체 개발 워크플로우 정의

## 핵심 결정 사항

**에이전트 패턴: 감독자(Supervisor) + 팬아웃/팬인 혼합**

오케스트레이터 한 명이 전체 Phase를 관리하고, Phase 내 독립적인 작업은 팬아웃으로 병렬 실행한다. Phase 간 의존성(예: 백엔드 완료 전에 AI 통합 불가)만 순서를 지킨다.

```
[오케스트레이터]
  ├── [콘텐츠_작가]       ← 캐릭터 파일 + 시나리오 (Phase 1, 병렬)
  ├── [프론트엔드_개발자] ← 채팅 UI (Phase 1, 병렬)
  ├── [백엔드_개발자]     ← API + 게임 상태 (Phase 1, 병렬)
  └── [AI_통합_전문가]    ← HuggingFace 연동 (Phase 2, 백엔드 완료 후)
```

**에이전트 간 데이터 전달은 파일 기반**

에이전트끼리 직접 통신하는 대신, `_workspace/` 폴더에 산출물 파일을 남기는 방식으로 전달한다. 예: 백엔드 개발자가 `_workspace/api-spec.md`를 작성하면 프론트엔드 개발자가 읽어서 API를 연동한다.

**FastAPI 선택 이유**: Python 기반이라 HuggingFace 모델 코드와 같은 생태계에서 통합하기 쉽다.

## Claude Code 활용

`/harness` 메타스킬 한 번 실행으로 에이전트 팀 전체를 설계하고 파일을 생성했다. 직접 에이전트 `.md` 파일 형식이나 스킬 frontmatter를 알 필요 없이, "이런 팀이 필요하다"는 요구사항만 전달하면 하네스 구성부터 `settings.json` 업데이트까지 자동으로 처리됐다.

에이전트 정의 파일의 핵심은 **트리거 조건**이다. "캐릭터 만들어줘"라고 말하면 자동으로 `character-writer` 스킬이 호출되도록 각 에이전트의 `description`에 트리거 문구를 명시해두었다.

## 막혔던 점 / 해결 방법

특별한 트러블슈팅 없음. 하네스 설계 자체는 `/harness` 스킬이 처리했고, 이후 실제 개발에서 문제가 발생했다.

## 다음 연결 작업

- `mvp_backend_setup` — 에이전트 팀을 실제로 가동해 코드 생성
