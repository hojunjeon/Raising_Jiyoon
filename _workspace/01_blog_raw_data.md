# 블로그 원본 데이터 — 2026-04-08

## 메타 정보
- 수집 날짜: 2026-04-08
- 개발 일차: Day 2
- 최근 커밋 수: 4개 (전체)
- 포함된 devlog: `devlog/mvp_backend_setup.md`, `devlog/scene_based_refactor.md`

## 완료된 작업

### Day 1: MVP 백엔드 + 프론트엔드 기반 구조 세팅
- FastAPI 백엔드 전체 구조 완성 (main.py, models.py, database.py, 라우터 3개, Mock LLM)
- React + Vite 프론트엔드 구조 완성 (ChatScreen, MainScreen, GameContext)
- 캐릭터 파일 2개 작성 (김지윤: 주인공, 이민준: NPC)
- API 스펙 문서 작성 (`_workspace/api-spec.md`)

### Day 2: NPC 1:1 채팅 → 씬 기반 방식 전환
- 게임 방식 전면 변경: NPC별 채팅방 → 씬 기반 주인공 대사 입력 방식
- URL: `/chat/:characterId` → `/scene/:sceneId`
- 메인화면: 캐릭터 카드 → 씬 카드 (입과식/알고리즘/팀프로젝트)
- 입력 의미: "내가" 하는 말 → "김지윤이" 하는 말
- API: `character_id + message` → `scene_id + protagonist_line`
- 응답에 `speaker` 필드 추가 (NPC 이름 표시)
- 시나리오 3개 작성 (scene_1: 입과식, scene_2: 알고리즘 수업, scene_3: 팀 프로젝트)

## 핵심 기술 결정

### 1. LLM을 Mock으로 시작한 이유
실제 HuggingFace 모델 연동 전에 API 구조와 프론트-백 통신을 먼저 완성해두면, 나중에 LLM만 교체하면 된다. `llm/interface.py`에 환경변수(`LLM_BACKEND`)로 구현체를 바꿀 수 있게 설계했다.

### 2. FastAPI 선택 이유
Python 기반이라 나중에 HuggingFace 모델 코드와 같은 언어로 통합하기 쉽다. 자동 API 문서(Swagger)도 개발 중 편리하다.

### 3. 씬 기반으로 전환한 이유 (가장 중요한 결정)
초기 설계는 NPC별로 채팅방을 만드는 방식이었다. 플레이어가 NPC에게 말을 걸면 NPC가 응답하는 구조. 이 방식은 플레이어가 항상 먼저 말을 걸어야 해서 "내가 왜 이 NPC한테 말 걸어야 하지?" 하는 수동적인 느낌이 있었다.

씬 기반으로 바꾸면 플레이어가 **김지윤의 대사를 직접 입력**하는 방식이 된다. "이 상황에서 김지윤이라면 뭐라고 할까?"를 고민하게 되어 몰입감이 생긴다. 게임의 핵심인 "김지윤을 키운다"는 느낌도 더 잘 산다.

### 4. speaker 필드 추가 이유
한 씬에 NPC가 여러 명 등장할 수 있다. 누가 말하는지 알아야 말풍선에 이름을 표시할 수 있고, LLM에게도 "이 NPC의 캐릭터로 응답하라"는 컨텍스트를 줄 수 있다.

## 현재 이슈
- Node.js 미설치 → 프론트엔드 `npm install` 안 됨 (사용자가 직접 설치 필요)
- LLM이 Mock 상태 → 실제 AI 응답 없음
- 백엔드 실행/프론트엔드 실행 테스트 미완료

## 아직 안 된 것
- LLM 실제 연동 (`llm-integrator` 스킬)
- 설정 화면 (`SettingsScreen.jsx`)
- 엔딩 화면
- 저장/불러오기 UI

## 코드 구조

### 백엔드 (FastAPI)
```
backend/
├── main.py              # 앱 진입점, 라우터 3개 include
├── models.py            # 게임 데이터 스키마
├── database.py          # DB 연결 설정
├── routers/
│   ├── chat.py          # POST /chat (씬 기반)
│   ├── game_state.py    # GET /game-state, POST /game-state/event
│   └── auth.py          # 회원가입/로그인
└── llm/
    ├── mock.py          # Mock LLM (씬별 NPC 응답)
    └── interface.py     # LLM_BACKEND 환경변수로 구현체 교체
```

### 프론트엔드 (React + Vite)
```
frontend/src/
├── App.jsx                    # 라우팅 (/, /scene/:sceneId)
├── context/GameContext.jsx    # 능력치 전역 상태 관리
├── api/gameApi.js             # sendMessage(userId, sceneId, protagonistLine)
└── components/
    ├── Chat/
    │   ├── ChatScreen.jsx     # 씬 기반 채팅 화면
    │   ├── MessageBubble.jsx  # speakerName 레이블 포함
    │   ├── ChatInput.jsx
    │   └── ChoiceButtons.jsx
    └── Main/
        └── MainScreen.jsx     # 씬 목록 + 능력치 바
```

### 콘텐츠
- `charactor/김지윤.md` — 주인공 (29세, 전직 국어교사, 초기 능력치: 언변 40, 개발 5, 기획 20, 체력 30)
- `charactor/이민준.md` — NPC (27세, 스타트업 퇴사 개발자)
- `scenario/scene_1.md` — 입과식
- `scenario/scene_2.md` — 알고리즘 수업
- `scenario/scene_3.md` — 팀 프로젝트

## 코드 스니펫

### 스니펫 1: LLM 인터페이스 — 환경변수로 구현체 교체
```python
# backend/llm/interface.py
import os
from backend.llm.mock import MockLLM

def get_llm():
    backend = os.getenv("LLM_BACKEND", "mock")
    if backend == "mock":
        return MockLLM()
    raise ValueError(f"Unknown LLM_BACKEND: {backend}")

_llm = None
def llm():
    global _llm
    if _llm is None:
        _llm = get_llm()
    return _llm
```

### 스니펫 2: 씬별 능력치 변화 로직
```python
# backend/routers/chat.py
SCENE_STAT_MAP = {
    1: {"stat_speech": 2, "stat_dev": 0, "stat_planning": 1},   # 입과식
    2: {"stat_speech": 0, "stat_dev": 3, "stat_planning": 0},   # 알고리즘 수업
    3: {"stat_speech": 1, "stat_dev": 1, "stat_planning": 2},   # 팀 프로젝트
}
```

### 스니펫 3: React 능력치 전역 상태
```jsx
// frontend/src/context/GameContext.jsx
const applyStatDelta = useCallback((delta) => {
    setStats(prev => ({
      speech:   prev.speech   + (delta.stat_speech   || 0),
      dev:      prev.dev      + (delta.stat_dev       || 0),
      planning: prev.planning + (delta.stat_planning  || 0),
      stamina:  prev.stamina  + (delta.stat_stamina   || 0),
    }));
}, []);
```

## 다음 계획
1. Node.js 설치 후 `cd frontend && npm install && npm run dev` 실행 확인
2. `cd backend && pip install -r requirements.txt && uvicorn backend.main:app --reload` 실행 확인
3. 채팅 흐름 통합 테스트
4. LLM 실제 연동 (HuggingFace) — `llm-integrator` 스킬 사용
5. 설정 화면, 엔딩 화면, 저장/불러오기 UI 구현
