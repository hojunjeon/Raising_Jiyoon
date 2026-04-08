from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from pydantic import BaseModel

from backend.database import get_db
from backend.models import GameState

router = APIRouter()


def check_ending(state: GameState) -> str:
    """현재 능력치/평가/출석 기반 엔딩 판정."""
    # 히든 엔딩: 수료 기준 미달
    if state.current_scene >= 20:
        dropout = (
            state.subject_eval_pass < 6
            or state.monthly_eval_pass < 3
            or (state.sw_test_grade not in ("", "IM", "A"))
            or state.absences >= 4
        )
        if dropout:
            return "hidden_dropout"

    max_stat = max(state.stat_speech, state.stat_dev, state.stat_planning)
    if max_stat == 0:
        return ""
    if max_stat == state.stat_speech:
        return "instructor"
    elif max_stat == state.stat_dev:
        return "developer"
    else:
        return "planner"


class EventRequest(BaseModel):
    user_id: int = 1
    event_type: str   # "subject_eval_pass", "subject_eval_fail", "monthly_eval_pass",
                      # "monthly_eval_fail", "tardiness", "absence", "sw_test"
    value: str = ""   # sw_test 때 등급 ("IM", "A", ...)


@router.get("")
def get_game_state(user_id: int = 1, db: Session = Depends(get_db)):
    state = db.exec(select(GameState).where(GameState.user_id == user_id)).first()
    if not state:
        # 최초 조회 시 초기 상태 생성
        state = GameState(user_id=user_id)
        db.add(state)
        db.commit()
        db.refresh(state)
    ending = check_ending(state)
    return {**state.model_dump(), "ending": ending}


@router.post("/event")
def record_event(req: EventRequest, db: Session = Depends(get_db)):
    state = db.exec(select(GameState).where(GameState.user_id == req.user_id)).first()
    if not state:
        state = GameState(user_id=req.user_id)
        db.add(state)
        db.commit()
        db.refresh(state)

    match req.event_type:
        case "subject_eval_pass":
            state.subject_eval_pass += 1
        case "subject_eval_fail":
            state.subject_eval_fail += 1
        case "monthly_eval_pass":
            state.monthly_eval_pass += 1
        case "monthly_eval_fail":
            state.monthly_eval_fail += 1
        case "tardiness":
            state.tardiness += 1
            if state.tardiness % 3 == 0:
                state.absences += 1
        case "absence":
            state.absences += 1
        case "sw_test":
            state.sw_test_grade = req.value
        case "advance_scene":
            state.current_scene += 1

    db.add(state)
    db.commit()
    db.refresh(state)
    return {"ok": True, "state": state.model_dump()}


@router.post("/save")
def save_game(user_id: int = 1, db: Session = Depends(get_db)):
    state = db.exec(select(GameState).where(GameState.user_id == user_id)).first()
    if not state:
        return {"ok": False, "error": "state not found"}
    return {"ok": True, "data": state.model_dump()}


@router.get("/load")
def load_game(user_id: int = 1, db: Session = Depends(get_db)):
    return get_game_state(user_id=user_id, db=db)
