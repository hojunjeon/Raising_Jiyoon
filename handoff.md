# 인수인계 메모 — 2026-04-08 (Day 2)

## 끝난 것
- `charactor/김지윤.md` — 주인공 캐릭터 (초기 능력치: 언변 40, 개발 5, 기획 20, 체력 30)
- `charactor/이민준.md` — 개발 고수 동기 NPC
- `backend/` — FastAPI 백엔드 전체 구조
  - `main.py`, `models.py`, `database.py`
  - `routers/chat.py` — POST /chat (씬 기반으로 변경 완료)
  - `routers/game_state.py` — GET /game-state, POST /game-state/event
  - `routers/auth.py` — 회원가입/로그인
  - `llm/mock.py` — 씬별 NPC 응답 Mock LLM (speaker 필드 포함)
  - `llm/interface.py` — LLM_BACKEND 환경변수로 구현체 교체 가능
  - `requirements.txt`
- `frontend/` — React + Vite 프론트엔드 구조
  - `src/App.jsx` — 라우팅 (/, /scene/:sceneId)
  - `src/context/GameContext.jsx` — 능력치 전역 상태
  - `src/api/gameApi.js` — sendMessage(userId, sceneId, protagonistLine)
  - `src/components/Chat/` — ChatScreen(씬 기반), MessageBubble(speakerName), ChatInput, ChoiceButtons
  - `src/components/Main/MainScreen.jsx` — 씬 목록 + 능력치 바
  - `src/styles/global.css` — bubble-content, bubble-speaker-name 스타일 추가
- `scenario/scene_1.md` — 입과식
- `scenario/scene_2.md` — 알고리즘 수업
- `scenario/scene_3.md` — 팀 프로젝트
- `_workspace/api-spec.md` — API 엔드포인트 문서

## 주요 구조 변경 (Day 2)

**게임 방식 변경**: NPC 1:1 채팅 → 씬 기반 주인공 대사 입력 방식

| 항목 | 변경 전 | 변경 후 |
|------|---------|---------|
| URL | /chat/:characterId | /scene/:sceneId |
| 메인화면 | 캐릭터 카드 | 씬 카드 (입과식/알고리즘/팀프로젝트) |
| 입력 의미 | "내가" 하는 말 | "김지윤이" 하는 말 |
| API 요청 | character_id + message | scene_id + protagonist_line |
| API 응답 | reply + stat_delta + choices | speaker + reply + stat_delta + choices |
| 말풍선 | NPC 이름 없음 | NPC 이름 레이블 표시 |

## 남은 이슈
- Node.js 미설치 → 프론트엔드 `npm install` 안 됨 (사용자가 직접 설치 필요)
- LLM이 Mock 상태 → 실제 AI 응답 없음
- 백엔드 실행/프론트엔드 실행 테스트 미완료

## 아직 안 된 것
- LLM 실제 연동 (`llm-integrator` 스킬)
- 설정 화면 (`SettingsScreen.jsx`)
- 엔딩 화면
- 저장/불러오기 UI

## 다음 단계
1. Node.js 설치 후 `cd frontend && npm install && npm run dev` 실행 확인
2. `cd backend && pip install -r requirements.txt && uvicorn backend.main:app --reload` 실행 확인
3. 채팅 흐름 통합 테스트: 씬 선택 → 김지윤 대사 입력 → NPC 이름 붙은 응답 확인
4. LLM 실제 연동 (Claude API 또는 HuggingFace)
