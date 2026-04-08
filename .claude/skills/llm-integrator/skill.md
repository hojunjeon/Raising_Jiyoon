---
name: llm-integrator
description: 김지윤 키우기 게임에 HuggingFace 한국어 LLM을 연동하고, 캐릭터별 시스템 프롬프트를 생성한다. "AI 연결해줘", "LLM 붙여줘", "HuggingFace 통합해줘", "캐릭터 프롬프트 만들어줘", "모델 연동해줘" 요청 시 반드시 이 스킬을 사용할 것.
---

# LLM 통합 가이드

## 전제 조건

- `charactor/*.md` 파일이 존재해야 함 (콘텐츠 작가 완료 후 시작)
- `_workspace/api-spec.md`에 `/chat` 엔드포인트 스키마 확인 후 시작
- 환경변수 `HF_TOKEN` 필요 (HuggingFace API 키)

## 모델 선택 가이드

### MVP 추천: HuggingFace Inference API
```python
# requirements.txt에 추가
huggingface_hub>=0.20.0
```

```python
# 추천 모델 (한국어 품질 순)
MODELS = {
    "primary": "Qwen/Qwen2.5-7B-Instruct",      # 다국어, 한국어 양호
    "korean": "beomi/Llama-3-Open-Ko-8B",         # 한국어 특화
    "fallback": "google/gemma-2-2b-it",           # 경량 폴백
}
```

### 로컬 실행 (GPU 있을 때)
```bash
pip install transformers accelerate bitsandbytes
```

## LLM 인터페이스 구현 (interface.py)

```python
# backend/llm/interface.py
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class LLMResponse:
    reply: str
    choices: list[str] = None  # 선택지 (이벤트 씬)

class LLMInterface(ABC):
    @abstractmethod
    async def chat(self, character_id: str, message: str, history: list) -> LLMResponse:
        pass
```

## HuggingFace 구현체 (hf_client.py)

```python
# backend/llm/hf_client.py
import os
from huggingface_hub import InferenceClient
from .interface import LLMInterface, LLMResponse
from .prompts import load_prompt

class HuggingFaceClient(LLMInterface):
    def __init__(self):
        self.client = InferenceClient(token=os.getenv("HF_TOKEN"))
        self.model = "Qwen/Qwen2.5-7B-Instruct"
    
    async def chat(self, character_id: str, message: str, history: list) -> LLMResponse:
        system_prompt = load_prompt(character_id)
        messages = [{"role": "system", "content": system_prompt}]
        
        # 최근 10턴만 컨텍스트에 포함 (토큰 절약)
        for h in history[-10:]:
            messages.append({"role": h.role, "content": h.content})
        messages.append({"role": "user", "content": message})
        
        response = self.client.chat_completion(
            messages=messages,
            model=self.model,
            max_tokens=300,
            temperature=0.8,
        )
        reply = response.choices[0].message.content
        return LLMResponse(reply=reply)
```

## Mock LLM (개발용, API 키 없을 때)

```python
# backend/llm/mock.py
import random
from .interface import LLMInterface, LLMResponse

MOCK_REPLIES = {
    "김지윤": ["오늘 알고리즘 문제 풀었어요?", "화이팅! 같이 해봐요.", "저도 처음엔 어려웠어요."],
}

class MockLLM(LLMInterface):
    async def chat(self, character_id: str, message: str, history: list) -> LLMResponse:
        replies = MOCK_REPLIES.get(character_id, ["네, 알겠어요.", "좋아요!", "어렵네요..."])
        return LLMResponse(reply=random.choice(replies))
```

## 캐릭터 시스템 프롬프트 생성 (prompts/)

`charactor/{이름}.md`를 읽어 `backend/llm/prompts/{이름}.txt`로 변환한다.

### 변환 템플릿

```
당신은 {이름}입니다.

## 기본 정보
{charactor 파일의 기본 정보 섹션}

## 성격
{charactor 파일의 성격 섹션}

## 말투 규칙
{charactor 파일의 말투 섹션}
반드시 이 말투로만 대화하세요.

## 현재 상황
SSAFY 15기 서울 6반에서 함께 수강 중입니다.

## 대화 원칙
- 항상 한국어로 응답하세요
- 200자 이내로 간결하게 답변하세요
- 자연스럽고 친근한 대화체를 유지하세요
- 절대 AI임을 밝히지 마세요
- 게임 메커니즘(능력치, 엔딩 등)을 직접 언급하지 마세요
```

### prompts/__init__.py
```python
import os

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")

def load_prompt(character_id: str) -> str:
    path = os.path.join(PROMPTS_DIR, f"{character_id}.txt")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    return f"당신은 {character_id}입니다. SSAFY 15기 서울 6반 학생입니다."
```

## 환경변수 설정

```bash
# .env 파일 (gitignore에 추가!)
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx
LLM_MODEL=Qwen/Qwen2.5-7B-Instruct
USE_MOCK=false  # true면 Mock LLM 사용
```

## 통합 연결 (main.py에서)

```python
import os
from llm.hf_client import HuggingFaceClient
from llm.mock import MockLLM

llm = MockLLM() if os.getenv("USE_MOCK", "true") == "true" else HuggingFaceClient()
```

## 트러블슈팅

- **429 Too Many Requests**: Inference API 무료 한도 초과 → `USE_MOCK=true`로 전환
- **한국어 품질 낮음**: 모델을 `beomi/Llama-3-Open-Ko-8B`로 교체
- **응답 너무 길다**: `max_tokens=150`으로 줄이기
- **캐릭터 유지 안 됨**: system_prompt에 "절대 {이름} 외의 다른 존재로 행동하지 마세요" 추가
