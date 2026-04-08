from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from pydantic import BaseModel

from backend.database import get_db
from backend.models import ChatHistory, GameState
from backend.llm.interface import llm

router = APIRouter()

# 씬별 능력치 변화 가중치
SCENE_STAT_MAP: dict[int, dict[str, int]] = {
    1: {"stat_speech": 2, "stat_dev": 0, "stat_planning": 1},   # 입과식
    2: {"stat_speech": 0, "stat_dev": 3, "stat_planning": 0},   # 알고리즘 수업
    3: {"stat_speech": 1, "stat_dev": 1, "stat_planning": 2},   # 팀 프로젝트
}


class ChatRequest(BaseModel):
    user_id: int = 1
    scene_id: int = 1           # 씬 번호
    protagonist_line: str       # 플레이어가 입력한 김지윤의 대사


class ChatResponse(BaseModel):
    speaker: str                # 응답 NPC 이름
    reply: str
    stat_delta: dict[str, int]
    choices: list[str]


def get_recent_history(db: Session, user_id: int, scene_id: int, limit: int = 10):
    rows = db.exec(
        select(ChatHistory)
        .where(ChatHistory.user_id == user_id)
        .where(ChatHistory.scene == scene_id)
        .order_by(ChatHistory.id.desc())
        .limit(limit)
    ).all()
    rows.reverse()
    return [{"role": r.role, "content": r.content, "speaker": r.character_id} for r in rows]


def apply_stat_delta(db: Session, user_id: int, scene_id: int):
    delta = SCENE_STAT_MAP.get(scene_id, {})
    state = db.exec(select(GameState).where(GameState.user_id == user_id)).first()
    if state:
        for key, val in delta.items():
            current = getattr(state, key, 0)
            setattr(state, key, current + val)
        db.add(state)
        db.commit()
    return delta


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest, db: Session = Depends(get_db)):
    history = get_recent_history(db, req.user_id, req.scene_id)

    result = await llm().chat(req.scene_id, req.protagonist_line, history)

    # 김지윤의 대사 저장
    db.add(ChatHistory(user_id=req.user_id, character_id="김지윤",
                       role="user", content=req.protagonist_line, scene=req.scene_id))
    # NPC 응답 저장
    db.add(ChatHistory(user_id=req.user_id, character_id=result.speaker,
                       role="assistant", content=result.reply, scene=req.scene_id))
    db.commit()

    stat_delta = apply_stat_delta(db, req.user_id, req.scene_id)

    return ChatResponse(speaker=result.speaker, reply=result.reply,
                        stat_delta=stat_delta, choices=result.choices)
