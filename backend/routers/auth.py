"""MVP 인증 — 단순 유저 생성/조회 (JWT 없이)."""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from passlib.context import CryptContext

from backend.database import get_db
from backend.models import User, GameState

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.exec(select(User).where(User.username == req.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 존재하는 유저명입니다.")
    user = User(username=req.username, hashed_password=pwd_context.hash(req.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    # 초기 게임 상태 생성
    state = GameState(user_id=user.id)
    db.add(state)
    db.commit()
    return {"ok": True, "user_id": user.id, "username": user.username}


@router.post("/login")
def login(req: RegisterRequest, db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.username == req.username)).first()
    if not user or not pwd_context.verify(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="유저명 또는 비밀번호가 틀렸습니다.")
    return {"ok": True, "user_id": user.id, "username": user.username}
