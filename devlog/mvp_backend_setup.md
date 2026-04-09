# MVP 백엔드 + 프론트엔드 기반 구조 세팅

## 왜 이 작업을 했나

김지윤 키우기 게임의 첫 번째 작업. 채팅 → LLM 응답 → 능력치 변화 흐름이 동작하는 최소한의 뼈대가 필요했다. 실제 LLM 연동 전에 Mock으로 전체 흐름을 먼저 검증하기로 했다.

## 무엇을 만들었나

### 백엔드 (FastAPI)
- `backend/main.py` — 앱 진입점, 라우터 3개 포함
- `backend/models.py` — 게임 데이터 스키마 (능력치, 게임 상태)
- `backend/database.py` — DB 연결 설정
- `backend/routers/chat.py` — POST /chat
- `backend/routers/game_state.py` — GET /game-state, POST /game-state/event
- `backend/routers/auth.py` — 회원가입 / 로그인
- `backend/llm/mock.py` — Mock LLM (하드코딩된 응답)
- `backend/llm/interface.py` — LLM_BACKEND 환경변수로 구현체 교체 가능한 인터페이스
- `backend/requirements.txt`

### 프론트엔드 (React + Vite)
- `frontend/src/App.jsx` — 라우팅
- `frontend/src/context/GameContext.jsx` — 능력치 전역 상태
- `frontend/src/api/gameApi.js` — API 호출 함수
- `frontend/src/components/Chat/` — ChatScreen, MessageBubble, ChatInput, ChoiceButtons
- `frontend/src/components/Main/MainScreen.jsx` — 메인 화면

### 콘텐츠
- `charactor/김지윤.md` — 주인공 (초기 능력치: 언변 40, 개발 5, 기획 20, 체력 30)
- `charactor/이민준.md` — 개발 고수 동기 NPC

### 문서
- `_workspace/api-spec.md` — API 엔드포인트 스펙 문서

## 핵심 결정 사항

**LLM을 Mock으로 시작한 이유**: 실제 HuggingFace 모델 연동 전에 API 구조와 프론트-백 통신을 먼저 완성해두면, 나중에 LLM만 교체하면 된다. `llm/interface.py`에 환경변수(`LLM_BACKEND`)로 구현체를 바꿀 수 있게 설계했다.

**FastAPI 선택 이유**: Python 기반이라 나중에 HuggingFace 모델 코드와 같은 언어로 통합하기 쉽다. 자동 API 문서(Swagger)도 개발 중 편리하다.

## 막혔던 점 / 해결 방법

- Node.js 미설치 → 프론트엔드 `npm install` 불가. 백엔드 먼저 완성하고 프론트는 구조만 작성.
- 백엔드 실행 테스트 미완료 (uvicorn 기동 확인 필요)

## Claude Code 활용

`게임 오케스트레이터` 에이전트로 Day 1 작업을 킥오프했다. 오케스트레이터가 `plan.md`를 먼저 작성하고 Phase 1 작업을 세 에이전트에게 분배했다.

**병렬 실행한 에이전트 3개:**
- `백엔드 개발자` (`game-api-builder` 스킬) — FastAPI 프로젝트 전체 구조 생성
- `프론트엔드 개발자` (`chat-ui-builder` 스킬) — React + Vite 프로젝트 구조 생성
- `콘텐츠 작가` (`character-writer` 스킬) — 김지윤, 이민준 캐릭터 파일 작성

세 에이전트가 동시에 실행되어 하루 만에 백엔드 + 프론트엔드 + 콘텐츠 뼈대가 모두 완성됐다. 에이전트 간 데이터 전달은 `_workspace/api-spec.md`를 통했다 — 백엔드 개발자가 API 스펙을 문서화하면 프론트엔드 개발자가 읽어서 `gameApi.js`를 구현하는 구조.

작업 종료 후 `handoff.md`에 완료된 것, 남은 이슈, 다음 단계를 기록해 다음 세션에 컨텍스트를 전달했다.

## 다음 연결 작업

- `scene_based_refactor` — NPC 1:1 채팅 방식을 씬 기반으로 전환
- Node.js 설치 후 프론트엔드 실행 확인
