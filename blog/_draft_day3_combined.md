---
title: Claude Code 에이전트 팀으로 5일 만에 LLM 게임 MVP 개발하기
date: 2026-04-09
tags: [개발일지, 게임개발, FastAPI, React, LLM, Claude Code]
series: 김지윤 키우기 개발기
---

# Claude Code 에이전트 팀으로 5일 만에 LLM 게임 MVP 개발하기

## TL;DR

- **만든 것**: 에이전트 5명, 스킬 6개로 구성한 LLM 게임 하네스. Day 1에 FE+BE+콘텐츠 뼈대, Day 2에 씬 기반 아키텍처 완성
- **핵심 결정**: 코드 전에 팀을 먼저 짓고, Plan mode로 범위를 확정한 뒤, 병렬 개발로 5일 MVP 가능
- **다음 단계**: LLM 실제 연동 및 UI 완성

---

## 배경

SSAFY 15기 서울 6반의 이야기를 게임으로 만드는 프로젝트다. LLM과 상호작용하는 키우기 게임인데, MVP 마감이 5일 남은 상황에서 시작했다. 한 명의 개발자가 프론트엔드, 백엔드, 콘텐츠, AI를 모두 순서대로 진행하면 절대 불가능한 일정이었다. 그래서 Claude Code의 에이전트 팀 기능을 활용했다.

---

## 무엇을 만들었나

### Day 0 — 에이전트 하네스 구성
- **에이전트 5명**: 게임 오케스트레이터(감독), 콘텐츠 작가, 프론트엔드 개발자, 백엔드 개발자, AI 통합 전문가
- **스킬 6개**: `character-writer`, `scenario-writer`, `chat-ui-builder`, `game-api-builder`, `llm-integrator`, `blog-writer`
- 에이전트 간 데이터 공유: `_workspace/` 폴더의 파일 기반 (API 스펙 → 프론트엔드 구현)

### Day 1 — MVP 기반 구조 (병렬 개발 완성)
- **백엔드**: FastAPI 전체 구조 (`main.py`, `models.py`, `routers/` 3개, `llm/` 모듈)
- **프론트엔드**: React + Vite 구조 (`ChatScreen.jsx`, `MainScreen.jsx`, `GameContext.jsx` 등)
- **콘텐츠**: 캐릭터 2명 + 시나리오 뼈대

### Day 2 — 씬 기반 아키텍처로 전환
- API URL 변경: `/chat/:characterId` → `/scene/:sceneId`
- 입력 의미 변경: "내가" 하는 말 → "**김지윤이**" 하는 말
- 응답 포맷 확장: `speaker` 필드 추가 (다중 NPC 대응)
- 시나리오 3개 신규 작성: 입과식, 알고리즘 수업, 팀 프로젝트

### Day 3 (오늘) — 통합 테스트 완료
- 프론트엔드: `npm run dev` → http://localhost:5173 정상 기동
- 백엔드: `uvicorn backend.main:app --reload` 정상 기동
- 트러블슈팅 완료: `ModuleNotFoundError` 해결

---

## 핵심 기술 결정

### 1. 하네스 먼저, 코딩은 나중

처음 생각은 "FE 먼저 만들고 BE 만들고 콘텐츠 통합하자"였다. 그런데 그렇게 하면 5일 안에 끝날 리가 없다. 대신 `/harness` 메타스킬로 **팀을 먼저 구성**했다.

에이전트별 스킬 정의로 누가 뭘 할 건지 명확히 하고, `_workspace/` 폴더로 에이전트 간 커뮤니케이션 채널을 만들었다. 병렬/순서 작업을 분류해서 FE+BE는 동시에, 통합은 이후에 진행했다.

그 결과 독립 작업들은 **동시에 진행**되고, 의존 작업만 순서를 지킬 수 있었다. "혼자 5일"이 아니라 "5명이 1일씩"이 된 셈이다.

### 2. Plan mode로 "변경하지 않는 것"을 명시하기

Day 2 씬 기반 전환 시 백엔드 15개 파일, 프론트엔드 여러 컴포넌트를 동시에 수정해야 했다. 이런 대규모 리팩토링은 에이전트가 실수하기 좋은 상황이다.

Claude Code의 **Plan mode**를 사용해서 변경할 15개 파일을 나열하고, **유지할 6개 모듈을 명시적으로 확정**했다(이쪽은 건드리지 말 것). 완료 기준 3가지도 정의했다.

Plan을 작성하고 검토(승인)한 후 에이전트를 실행했다. 덕분에 불필요한 파일 수정은 일어나지 않았다.

### 3. Mock LLM으로 교체 가능한 인터페이스 설계

실제 HuggingFace 모델을 처음부터 연동하지 않았다. 대신 **Mock LLM**으로 시작해서 API 구조를 먼저 완성했다.

```python
# backend/llm/interface.py
def get_llm():
    backend = os.getenv("LLM_BACKEND", "mock")
    if backend == "mock":
        return MockLLM()
    # Day 4에 claude / huggingface 구현 추가 예정
    raise ValueError(f"Unknown LLM_BACKEND: {backend}")
```

환경변수 하나만 바꾸면 mock/claude/huggingface를 교체할 수 있다. MVP 단계에서는 mock으로 빠르게 테스트하고, 나중에 실제 모델로 교체한다.

### 4. 씬 기반 게임플레이의 몰입감

처음 설계는 "NPC별 채팅방" 구조였다. 플레이어가 NPC를 선택하고 말을 건다.

```
플레이어: "안녕하세요"
NPC (이민준): "안녕. 뭐할 거야?"
```

근데 이건 역할극의 감정이입이 떨어졌다. 게임은 "김지윤을 **키우는** 게임"인데, 플레이어가 여전히 **제3자**처럼 느껴졌다.

**씬 기반으로 바꾸니 완전 달라졌다.**

```
[입과식 씬]
이민준: "에이, 너 뭐라고 할 거야?"
[플레이어가 입력] "저 어제 국어선생님이었어요"

NPC들이 플레이어가 입력한 김지윤의 대사에 반응한다.
```

플레이어가 **김지윤의 대리인**이 되는 느낌이 생긴다. "여기서 김지윤이라면 뭐라고 할까?"라고 생각하면서 플레이한다.

API 레벨에서도:
- Request: `scene_id` + `protagonist_line` (김지윤이 할 말)
- Response: `speaker` + `reply` + `choices` (누가 뭐라고 했고, 다음에 선택할 것)

---

## 코드로 보는 구현

### 씬 기반 채팅 API 스키마

```python
# backend/routers/chat.py
class ChatRequest(BaseModel):
    user_id: int = 1
    scene_id: int = 1
    protagonist_line: str  # 플레이어가 입력한 김지윤의 대사

class ChatResponse(BaseModel):
    speaker: str           # 응답 NPC 이름 (여러 NPC 가능)
    reply: str
    stat_delta: dict[str, int]  # {"stat_speech": 2, "stat_dev": 0}
    choices: list[str]     # 다음 선택지
```

요청에서 `protagonist_line`을 받으면, 응답에서 `speaker` 필드로 "누가" 대답하는지 명시한다. 같은 씬에 여러 NPC가 있을 때 대화 흐름을 표현할 수 있다.

### 씬별 능력치 가중치 매핑

```python
# backend/routers/chat.py
SCENE_STAT_MAP = {
    1: {"stat_speech": 2, "stat_dev": 0, "stat_planning": 1},   # 입과식: 언변 중심
    2: {"stat_speech": 0, "stat_dev": 3, "stat_planning": 0},   # 알고리즘: 개발 중심
    3: {"stat_speech": 1, "stat_dev": 1, "stat_planning": 2},   # 팀프로젝트: 기획 중심
}
```

각 씬마다 강조되는 능력치가 다르다. 입과식 씬에서는 언변이 중요하고, 알고리즘 수업에서는 개발 능력이 올라간다. 이 매핑으로 플레이어의 선택이 게임 엔딩(능력치 최고치)에 영향을 미친다.

---

## 아직 남은 과제

### LLM 모델 연동 없는 상태

현재 백엔드는 Mock LLM으로 하드코딩된 응답만 한다. 실제로 플레이어 입력에 따라 NPC가 다르게 응답하려면 HuggingFace API 또는 Claude API를 연동해야 한다. Day 4에서 `llm-integrator` 에이전트가 이를 처리할 예정이다.

### UI 미완성

현재는 채팅 화면(`ChatScreen.jsx`)과 메인 화면(`MainScreen.jsx`)만 있다. 설정 화면, 엔딩 화면, 게임 저장/불러오기 UI는 아직 미구현 상태다. Day 5에서 `chat-ui-builder` 에이전트가 마무리할 것이다.

---

## 배운 점

이번 작업의 가장 큰 교훈은 **"코드를 먼저 짜지 말고 구조를 먼저 설계하라"**는 것이다. 5명의 에이전트를 세팅하는 데 반나절이 걸렸지만, 그 덕분에 남은 4일 반 동안 병렬로 개발할 수 있었다. 혼자라면 3주는 걸릴 프로젝트를 5일 안에 끝낼 수 있었던 이유다.

다음 포스트에서는 실제로 LLM을 붙이면서 캐릭터별 시스템 프롬프트를 어떻게 설계했는지, 그리고 **Plan mode에서 예상치 못한 버그를 찾아낸 과정**을 공유할 예정이다.

---

**다음 포스트:** "HuggingFace 한국어 모델로 NPC 캐릭터성 만들기" (예정)
