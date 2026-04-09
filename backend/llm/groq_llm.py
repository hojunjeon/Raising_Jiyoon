"""
Groq API LLM 구현체.
환경변수 GROQ_API_KEY, GROQ_MODEL로 제어.
무료 한도: 14,400 req/day (llama-3.1-8b-instant 기준)
"""
import os
import random
from groq import AsyncGroq
from backend.llm.mock import LLMResponse, DEFAULT_CHOICES

# 씬 → NPC 매핑
SCENE_SPEAKER: dict[int, str] = {
    1: "이민준",
    2: "이민준",
    3: "이민준",
}

# 이민준 캐릭터 시스템 프롬프트
SYSTEM_PROMPTS: dict[str, str] = {
    "이민준": """당신은 이민준입니다. SSAFY 15기 서울 6반 수강생, 27세 남성.

성격:
- 자신감 있고 직설적. 모르는 건 모른다고, 아는 건 바로 말한다.
- 가르치기 좋아함. 아는 걸 공유하는 걸 즐기지만 상대가 이미 알면 바로 멈춘다.
- 효율주의자. "더 빠른 방법 있어요"가 입버릇.
- 속으로는 은근히 외로움. 대화할 상대를 찾고 있다.

말투:
- 빠르고 간결. 핵심만 말한다.
- 가끔 기술 용어를 자연스럽게 섞는다.
- 반말과 존댓말 사이 (아직 많이 친하지 않으므로 존댓말 위주).

상대방은 김지윤 (29세, 전직 초등학교 국어선생님, SSAFY에서 개발자로 전환 중).
김지윤의 대사에 이민준으로서 자연스럽게 짧게 응답하세요. 2~3문장 이내로. 반드시 한국어로만 답하세요.""",
}


class GroqLLM:
    def __init__(self):
        self._client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        self._model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    def _build_messages(
        self,
        speaker: str,
        protagonist_line: str,
        history: list[dict],
    ) -> list[dict]:
        system_prompt = SYSTEM_PROMPTS.get(speaker, SYSTEM_PROMPTS["이민준"])
        messages = [{"role": "system", "content": system_prompt}]

        for h in history:
            role = "user" if h.get("role") == "user" else "assistant"
            messages.append({"role": role, "content": h.get("content", "")})

        messages.append({"role": "user", "content": protagonist_line})
        return messages

    async def chat(
        self,
        scene_id: int,
        protagonist_line: str,
        history: list[dict],
    ) -> LLMResponse:
        speaker = SCENE_SPEAKER.get(scene_id, "이민준")
        messages = self._build_messages(speaker, protagonist_line, history)

        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                max_tokens=150,
                temperature=0.7,
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"(응답 오류: {e})"

        choices = random.choice(DEFAULT_CHOICES)
        return LLMResponse(speaker=speaker, reply=reply, choices=choices)
