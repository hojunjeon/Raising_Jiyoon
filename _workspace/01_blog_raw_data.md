# 블로그 원본 데이터 — 2026-04-09

## 메타 정보
- 수집 날짜: 2026-04-09
- 개발 일차: Day 3
- 최근 커밋: `7a7533b first`
- 포함된 devlog: harness_setup.md, mvp_backend_setup.md, scene_based_refactor.md
- **블로그 앵글: "Claude Code 에이전트 팀으로 5일 만에 게임 MVP 개발"**

---

## 완료된 작업

### Day 0 — 에이전트 팀 하네스 구성
코드 한 줄 없는 상태. MVP 마감 5일 전. `/harness` 메타스킬로 에이전트 5인팀과 스킬 6개를 설계/생성.

**에이전트 팀:**
- 게임 오케스트레이터 (감독자 — 전체 Phase 조율)
- 콘텐츠 작가 (`character-writer`, `scenario-writer` 스킬)
- 프론트엔드 개발자 (`chat-ui-builder` 스킬)
- 백엔드 개발자 (`game-api-builder` 스킬)
- AI 통합 전문가 (`llm-integrator` 스킬)

에이전트 간 데이터 전달은 `_workspace/` 폴더 파일 기반. 예: 백엔드 개발자가 `api-spec.md` 작성 → 프론트엔드 개발자가 읽어 API 연동.

### Day 1 — MVP 기반 구조 (병렬 개발)
`게임 오케스트레이터`가 `plan.md`를 작성하고 세 에이전트를 병렬 실행.

- `콘텐츠 작가`: `charactor/김지윤.md`, `charactor/이민준.md` 생성
- `백엔드 개발자`: FastAPI 전체 구조 생성 (main, models, routers 3개, llm/mock, llm/interface)
- `프론트엔드 개발자`: React + Vite 구조 생성 (ChatScreen, MainScreen, GameContext 등)

**하루 만에 FE + BE + 콘텐츠 뼈대 완성.**

### Day 2 — 씬 기반 방식으로 전환
Plan mode로 변경 범위 확정(15개 파일) → 승인 → 에이전트 실행.

| 항목 | 변경 전 | 변경 후 |
|------|---------|---------|
| URL | /chat/:characterId | /scene/:sceneId |
| 입력 의미 | "내가" 하는 말 | "김지윤이" 하는 말 |
| API 요청 | character_id + message | scene_id + protagonist_line |
| API 응답 | reply + stat_delta | **speaker** + reply + stat_delta + choices |

시나리오 3개 신규 작성: scene_1(입과식), scene_2(알고리즘 수업), scene_3(팀 프로젝트)

### Day 3 (오늘) — 실행 테스트 완료
- 프론트엔드: `npm run dev` → http://localhost:5173 정상 기동 ✅
- 백엔드: `uvicorn backend.main:app --reload` (루트에서) 정상 기동 ✅
- 트러블슈팅: `backend/` 디렉토리 내부 실행 시 `ModuleNotFoundError: No module named 'backend'` → 루트에서 실행으로 해결

---

## 핵심 기술 결정

### 1. 하네스 먼저 짓기 — 코딩 전에 팀을 구성하라
혼자 FE/BE/콘텐츠/AI를 순서대로 만들면 5일 MVP 불가. `/harness` 메타스킬로 팀을 먼저 구성하고 이후 모든 개발을 에이전트에 위임. 감독자+팬아웃 패턴으로 독립 작업은 병렬, 의존 작업은 순서 보장.

### 2. Mock LLM으로 시작 — 교체 가능한 인터페이스
실제 HuggingFace 연동 전에 API 구조와 프론트-백 통신을 먼저 완성. `LLM_BACKEND` 환경변수 하나로 mock/claude/huggingface를 교체 가능하게 설계. MVP 단계에서는 Mock, 이후 실제 모델로 교체.

### 3. Plan mode — 코드 전에 범위 확정
여러 파일을 동시에 바꾸는 작업은 Plan mode를 먼저 사용. "변경하지 않는 것"을 명시적으로 확정해서 불필요한 리팩토링 방지. 씬 기반 전환 시 변경 15개 파일, 유지 6개 모듈을 plan 파일에 정리.

### 4. plan.md + handoff.md 워크플로우
매 작업 시작 시 `handoff.md` 읽어 이전 상태 파악, 완료 후 업데이트. 에이전트가 세션 간 컨텍스트를 잃지 않는다. `plan.md`는 작업 전 목표/완료기준/단계 정의.

### 5. 씬 기반 방식 선택 이유
"플레이어 = 김지윤의 대리인" 구조. 플레이어가 상황을 읽고 김지윤의 말을 써주면 NPC들이 반응. 단순 NPC 채팅보다 몰입감이 높고 "김지윤을 키운다"는 게임 테마에 맞다.

---

## 현재 이슈
- LLM Mock 상태 → 실제 AI 응답 없음 (다음 작업: llm-integrator)
- 설정 화면, 엔딩 화면, 저장/불러오기 UI 미구현

---

## 코드 구조

### 백엔드
```
backend/
├── main.py          # FastAPI 앱, CORS, 라우터 등록
├── models.py        # GameState, ChatHistory 스키마
├── database.py      # SQLite 연결
├── routers/
│   ├── chat.py      # POST /chat (씬 기반)
│   ├── game_state.py
│   └── auth.py
└── llm/
    ├── interface.py  # LLM_BACKEND 환경변수로 구현체 교체
    └── mock.py       # Mock LLM (씬별 하드코딩 응답)
```

### 프론트엔드
```
frontend/src/
├── App.jsx                    # 라우팅 (/, /scene/:sceneId)
├── context/GameContext.jsx    # 능력치 전역 상태
├── api/gameApi.js             # sendMessage(userId, sceneId, protagonistLine)
└── components/
    ├── Main/MainScreen.jsx    # 씬 목록 + 능력치 바
    └── Chat/
        ├── ChatScreen.jsx     # 씬 기반 채팅 메인
        ├── MessageBubble.jsx  # speakerName 레이블 포함
        ├── ChatInput.jsx
        └── ChoiceButtons.jsx
```

### 콘텐츠
- `charactor/김지윤.md` — 주인공 (29세, 전직 국어교사, 언변 40 / 개발 5 / 기획 20 / 체력 30)
- `charactor/이민준.md` — NPC (27세, 스타트업 퇴사 개발자)
- `scenario/scene_1.md` ~ `scene_3.md`

---

## 코드 스니펫

### 스니펫 1: LLM 교체 가능한 인터페이스
```python
# backend/llm/interface.py
def get_llm():
    backend = os.getenv("LLM_BACKEND", "mock")
    if backend == "mock":
        return MockLLM()
    # 이후 claude / huggingface 추가
    raise ValueError(f"Unknown LLM_BACKEND: {backend}")
```

### 스니펫 2: 씬 기반 채팅 API 스키마
```python
# backend/routers/chat.py
class ChatRequest(BaseModel):
    user_id: int = 1
    scene_id: int = 1
    protagonist_line: str  # 플레이어가 입력한 김지윤의 대사

class ChatResponse(BaseModel):
    speaker: str           # 응답 NPC 이름 (다중 NPC 대응)
    reply: str
    stat_delta: dict[str, int]
    choices: list[str]
```

### 스니펫 3: 씬별 능력치 가중치 매핑
```python
SCENE_STAT_MAP = {
    1: {"stat_speech": 2, "stat_dev": 0, "stat_planning": 1},   # 입과식
    2: {"stat_speech": 0, "stat_dev": 3, "stat_planning": 0},   # 알고리즘 수업
    3: {"stat_speech": 1, "stat_dev": 1, "stat_planning": 2},   # 팀 프로젝트
}
```

---

## 다음 계획
1. LLM 실제 연동 (HuggingFace Inference API 또는 Claude API)
2. 설정 화면, 엔딩 화면, 저장/불러오기 UI
