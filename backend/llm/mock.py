"""
MVP용 Mock LLM — 실제 LLM 연동 전 테스트용.
씬별 등장 NPC와 고정 응답 풀에서 랜덤 선택.
"""
import random
from dataclasses import dataclass, field


@dataclass
class LLMResponse:
    speaker: str
    reply: str
    choices: list[str] = field(default_factory=list)


# 씬별 NPC 응답 풀: { scene_id: [{"speaker": ..., "reply": ...}, ...] }
SCENE_MOCK_RESPONSES: dict[int, list[dict]] = {
    1: [  # 입과식
        {"speaker": "이민준", "reply": "어, 저도 처음엔 많이 떨렸어요. 지윤 씨는 발표 잘 하실 것 같던데."},
        {"speaker": "이민준", "reply": "교사 경력이 있으시면 발표는 걱정 없겠다, 솔직히 부럽네요."},
        {"speaker": "이민준", "reply": "입과식이 생각보다 길었죠. 저는 벌써 알고리즘 공부 시작하고 싶은데."},
    ],
    2: [  # 알고리즘 수업
        {"speaker": "이민준", "reply": "그거 O(n²)인데, 정렬 먼저 하면 O(n log n)으로 줄일 수 있어요."},
        {"speaker": "이민준", "reply": "코드는 일단 동작하게 만들고, 예쁘게는 나중에 해요."},
        {"speaker": "이민준", "reply": "오늘 알고리즘 풀었어요? 저는 두 문제 했는데 하나는 틀렸어요."},
    ],
    3: [  # 팀 프로젝트
        {"speaker": "이민준", "reply": "지윤 씨 아이디어 괜찮은데요. 기획이 탄탄하니까 개발이 편할 것 같아요."},
        {"speaker": "이민준", "reply": "팀 분위기가 중요하죠. 저는 그냥 묵묵히 코딩하는 스타일이긴 한데."},
        {"speaker": "이민준", "reply": "발표는 지윤 씨가 맡는 게 낫지 않을까요? 설명을 진짜 잘 하시더라고."},
    ],
}

DEFAULT_CHOICES = [
    ["더 자세히 물어본다", "고맙다고 한다", "화제를 돌린다"],
    ["같이 해보자고 제안한다", "혼자 해보겠다고 한다"],
    ["공감한다", "다른 이야기를 꺼낸다"],
]


class MockLLM:
    async def chat(
        self,
        scene_id: int,
        protagonist_line: str,
        history: list[dict],
    ) -> LLMResponse:
        pool = SCENE_MOCK_RESPONSES.get(scene_id, SCENE_MOCK_RESPONSES[1])
        picked = random.choice(pool)
        choices = random.choice(DEFAULT_CHOICES)
        return LLMResponse(speaker=picked["speaker"], reply=picked["reply"], choices=choices)
