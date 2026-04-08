from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import create_db
from backend.routers import chat, game_state, auth

app = FastAPI(title="김지윤 키우기 API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(game_state.router, prefix="/game-state", tags=["game-state"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.on_event("startup")
def on_startup():
    create_db()


@app.get("/")
def root():
    return {"status": "ok", "message": "김지윤 키우기 API"}
