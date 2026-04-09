"""
LLM 추상 인터페이스.
환경 변수 LLM_BACKEND에 따라 mock / claude / huggingface 중 선택.

chat(scene_id: int, protagonist_line: str, history: list[dict]) -> LLMResponse
  - scene_id: 현재 씬 번호
  - protagonist_line: 플레이어가 입력한 김지윤의 대사
  - history: 이전 대화 기록
"""
import os
from backend.llm.mock import MockLLM, LLMResponse


def get_llm():
    backend = os.getenv("LLM_BACKEND", "mock")
    if backend == "mock":
        return MockLLM()
    if backend == "huggingface":
        from backend.llm.huggingface import HuggingFaceLLM
        return HuggingFaceLLM()
    if backend == "groq":
        from backend.llm.groq_llm import GroqLLM
        return GroqLLM()
    raise ValueError(f"Unknown LLM_BACKEND: {backend}")


# 싱글턴
_llm = None


def llm():
    global _llm
    if _llm is None:
        _llm = get_llm()
    return _llm
