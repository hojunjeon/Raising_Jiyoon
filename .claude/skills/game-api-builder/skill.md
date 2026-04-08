---
name: game-api-builder
description: 김지윤 키우기 게임의 FastAPI 백엔드 서버를 구축한다. 채팅 API, 게임 상태(능력치/출석/평가), 저장/불러오기, 인증을 구현. "API 서버 만들어줘", "백엔드 구현해줘", "FastAPI 세팅해줘", "게임 상태 API 만들어줘" 요청 시 반드시 이 스킬을 사용할 것.
---

# 게임 API 빌더 가이드

## 프로젝트 세팅

```bash
cd Chat_Game
mkdir backend && cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install fastapi uvicorn sqlmodel python-jose[cryptography] python-multipart
```

## 디렉토리 구조

```
backend/
├── main.py                  # FastAPI 앱 진입점
├── models.py                # SQLModel 데이터 모델
├── routers/
│   ├── chat.py             # /chat 엔드포인트
│   ├── game_state.py       # /game-state 엔드포인트
│   └── auth.py             # /auth 엔드포인트
├── llm/
│   ├── interface.py        # LLM 추상 인터페이스 (AI팀이 구현)
│   └── mock.py             # MVP용 Mock LLM
├── database.py              # SQLite 연결
└── requirements.txt
```

## 핵심 데이터 모델 (models.py)

```python
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    hashed_password: str

class GameState(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    # 능력치
    stat_speech: int = 0      # 언변
    stat_dev: int = 0         # 개발
    stat_planning: int = 0    # 기획
    # 출석
    absences: int = 0         # 결석 횟수 (4 이상 = 히든 엔딩)
    tardiness: int = 0        # 지각/조퇴 누적 (3회 = 결석 1회)
    # 평가
    subject_eval_pass: int = 0   # 과목 평가 pass (10회 중 6회 필요)
    subject_eval_fail: int = 0
    monthly_eval_pass: int = 0   # 월말 평가 pass (6회 중 3회 필요)
    sw_test_grade: str = ""      # IM/A
    # 진행
    current_scene: int = 1
    ending: str = ""

class ChatHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    character_id: str
    role: str                 # "user" or "assistant"
    content: str
    scene: int
```

## 핵심 API 엔드포인트

### POST /chat
```python
@router.post("/chat")
async def chat(req: ChatRequest, db: Session = Depends(get_db)):
    """
    Request: { character_id, message, scene }
    Response: { reply, stat_delta, choices, next_scene }
    """
    # 1. 대화 기록 최근 10턴 조회
    history = get_recent_history(db, req.character_id, limit=10)
    # 2. LLM 호출 (llm/interface.py)
    result = await llm_interface.chat(req.character_id, req.message, history)
    # 3. 대화 기록 저장
    save_history(db, req.character_id, req.message, result.reply)
    # 4. 능력치 변화 계산 (씬 로직)
    stat_delta = compute_stat_delta(req.scene, result)
    return { "reply": result.reply, "stat_delta": stat_delta, "choices": result.choices }
```

### GET /game-state
```python
@router.get("/game-state")
async def get_game_state(db: Session = Depends(get_db)):
    state = db.get(GameState, current_user_id)
    ending = check_ending(state)
    return { **state.dict(), "ending": ending }
```

### 엔딩 판정 로직
```python
def check_ending(state: GameState) -> str:
    dropout = (
        state.subject_eval_pass < 6 or
        state.monthly_eval_pass < 3 or
        state.sw_test_grade not in ["IM", "A", ""] or  # 아직 안 봤으면 패스
        state.absences >= 4
    )
    if dropout and state.current_scene >= 20:  # 충분히 진행 후 판정
        return "hidden_dropout"
    
    max_stat = max(state.stat_speech, state.stat_dev, state.stat_planning)
    if max_stat == state.stat_speech:
        return "instructor"
    elif max_stat == state.stat_dev:
        return "developer"
    else:
        return "planner"
```

## main.py 기본 설정

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="김지윤 키우기 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite 개발 서버
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/chat")
app.include_router(game_state_router, prefix="/game-state")
app.include_router(auth_router, prefix="/auth")
```

## API 스펙 문서 작성

작업 완료 후 `_workspace/api-spec.md`에 다음을 작성한다:

```markdown
# API 스펙

## Base URL
http://localhost:8000

## 엔드포인트 목록
| Method | Path | 설명 |
|--------|------|------|
| POST | /chat | 캐릭터 채팅 |
| GET | /game-state | 게임 상태 조회 |
| POST | /game-state/event | 이벤트 기록 |
| POST | /save | 게임 저장 |
| GET | /load | 저장 불러오기 |

## /chat Request/Response 스키마
[상세 JSON 스키마]
```

## 실행

```bash
uvicorn main:app --reload --port 8000
# 문서: http://localhost:8000/docs
```
