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
    stat_speech: int = 40     # 언변 (교사 경력으로 초기값 높음)
    stat_dev: int = 5         # 개발
    stat_planning: int = 20   # 기획
    stat_stamina: int = 30    # 체력
    # 출석
    absences: int = 0         # 결석 횟수 (4 이상 = 히든 엔딩)
    tardiness: int = 0        # 지각/조퇴 누적 (3회 = 결석 1회, 초기화 없음)
    # 평가
    subject_eval_pass: int = 0    # 과목 평가 pass (10회 중 6회 필요)
    subject_eval_fail: int = 0
    monthly_eval_pass: int = 0    # 월말 평가 pass (6회 중 3회 필요)
    monthly_eval_fail: int = 0
    sw_test_grade: str = ""       # "", "IM", "A" (비어있으면 아직 안 봄)
    # 진행
    current_scene: int = 1
    ending: str = ""              # "", "instructor", "developer", "planner", "hidden_dropout"


class ChatHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    character_id: str             # speaker: "김지윤"(user) 또는 "이민준" 등(NPC)
    role: str                     # "user" or "assistant"
    content: str
    scene: int = 1
