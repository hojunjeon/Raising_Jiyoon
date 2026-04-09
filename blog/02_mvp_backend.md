---
title: 3개 에이전트로 하루 만에 게임 뼈대 완성하기
date: 2026-04-09
tags: [개발일지, SSAFY, 게임개발, FastAPI, React, Claude Code]
series: 김지윤 키우기 개발기
series_no: 2
---

이 글은 '김지윤 키우기' 개발기 시리즈 2편입니다. [1편(프로젝트 개요)](01_project_overview.md)을 먼저 읽으시면 맥락 이해에 도움이 됩니다.

## TL;DR

- Claude Code 병렬 에이전트 3개(백엔드 개발자, 프론트엔드 개발자, 콘텐츠 작가)를 동시에 실행해 24시간 안에 FastAPI 서버 + React 앱 + 캐릭터 파일 완성
- 에이전트 간 데이터 전달은 `_workspace/` 공유 파일(API 스펙 문서)로 핸드오프
- LLM을 Mock으로 시작해 나중에 실제 모델만 교체하는 구조

---

## 배경: 뼈대가 필요했다

프로젝트 초기 단계에서 핵심 흐름의 동작 가능성을 검증해야 했다: "플레이어 메시지 → LLM 응답 → 능력치 변화 → 화면 업데이트"

기술 스택(FastAPI, React, HuggingFace)은 결정했지만, 실제 LLM을 붙이기 전에 프론트-백 통신 구조가 먼저 완성되어야 했다. 동시에 백엔드, 프론트엔드, 콘텐츠 작가가 병렬로 진행되어야 했고, 4월 13일 내에 MVP를 완성해야 한다는 데드라인이 있었다.

이런 상황에서 **Claude Code 에이전트 3개를 동시에 실행**하는 것이 최적이었다.

---

## 무엇을 만들었나

### 백엔드 (FastAPI)

```
backend/
├── main.py                 # 앱 진입점 + 라우터 3개
├── models.py               # 능력치, 게임 상태 스키마
├── database.py             # DB 설정
├── routers/
│   ├── chat.py             # POST /chat
│   ├── game_state.py       # GET /game-state, POST /game-state/event
│   └── auth.py             # 회원가입/로그인
├── llm/
│   ├── interface.py        # LLM 추상 인터페이스
│   └── mock.py             # 하드코딩된 Mock 응답
└── requirements.txt
```

핵심은 `/chat` 엔드포인트다. 플레이어가 메시지를 보내면:
1. 게임 상태를 로드
2. LLM 인터페이스를 통해 응답 생성 (현재는 Mock)
3. 응답 결과에 따라 능력치 업데이트
4. 변경된 상태를 응답

### 프론트엔드 (React + Vite)

```
frontend/src/
├── App.jsx
├── context/
│   └── GameContext.jsx     # 능력치 전역 상태
├── api/
│   └── gameApi.js          # API 호출 함수들
├── components/
│   ├── Chat/               # ChatScreen, MessageBubble, ChatInput, ChoiceButtons
│   └── Main/               # MainScreen
```

React Context로 능력치(`언변`, `개발`, `기획`, `체력`)를 전역 상태로 관리했다. 게임 화면은 두 가지:
- **메인 화면**: 능력치 표시 + 게임 시작
- **채팅 화면**: KakaoTalk 스타일 메시지 + 선택지 버튼

### 콘텐츠

- `charactor/김지윤.md` — 주인공 (초기 능력치: 언변 40, 개발 5, 기획 20, 체력 30)
- `charactor/이민준.md` — 개발 고수 동기 NPC

### 문서

- `_workspace/api-spec.md` — API 엔드포인트, 요청/응답 스키마, 능력치 변화 로직

---

## 핵심 기술 결정: 왜 이렇게 설계했나

### 1. LLM을 Mock으로 시작한 이유

실제 HuggingFace 모델을 바로 붙이지 않았다. 이유는:

1. **불확실성 제거** — 어떤 모델을 쓸지, 응답 시간이 얼마나 걸릴지 아직 모른다. 그동안 프론트-백 통신 구조를 먼저 완성하면 나중에 LLM 구현체만 교체하면 된다.
2. **병렬 개발 가능** — Mock 응답이 있으니 프론트엔드 팀이 API를 바로 테스트할 수 있다. LLM 준비를 기다릴 필요 없다.
3. **환경변수 기반 전환** — `interface.py`에서 `LLM_BACKEND` 환경변수로 구현체를 동적으로 로드한다.

```python
# backend/llm/interface.py
def get_llm():
    backend = os.getenv("LLM_BACKEND", "mock")
    if backend == "mock":
        return MockLLM()
    raise ValueError(f"Unknown LLM_BACKEND: {backend}")
```

환경변수 `LLM_BACKEND`를 `"huggingface"` 같은 값으로 바꾸면 나중에 실제 모델 구현체를 로드한다. 현재는 `"mock"` 기본값이라 MockLLM만 반환한다.

### 2. FastAPI 선택 이유

프로젝트 전체가 Python 생태계(HuggingFace도 Python)라서 일관성 있다. 그리고 자동 API 문서(Swagger UI)가 기본으로 생성되어 개발 중 편리하다. 프론트엔드 팀이 `http://localhost:8000/docs`에서 실시간으로 스키마를 확인할 수 있다.

### 3. 에이전트 병렬 실행 — _workspace/ 파일 핸드오프

가장 흥미로운 부분은 **에이전트 간 협업 방식**이다.

```
게임 오케스트레이터
  ├─→ 백엔드 개발자 에이전트
  │   ├─ FastAPI 프로젝트 생성
  │   └─ _workspace/api-spec.md 작성
  │
  ├─→ 프론트엔드 개발자 에이전트
  │   ├─ React 프로젝트 생성
  │   ├─ _workspace/api-spec.md 읽음
  │   └─ gameApi.js 구현
  │
  └─→ 콘텐츠 작가 에이전트
      └─ charactor/*.md 작성
```

**핸드오프 방식:**

1. **게임 오케스트레이터**가 `plan.md`를 먼저 작성하고 세 에이전트에게 작업 분배
2. **백엔드 개발자**가 API 스펙을 `_workspace/api-spec.md`에 문서화
3. **프론트엔드 개발자**가 그 파일을 읽어서 자신의 `gameApi.js`를 구현
4. 세 에이전트가 동시에 실행 → 24시간 안에 완성

이 방식의 장점:

- **의존성 명확** — "API 스펙이 먼저 결정되면 프론트엔드는 그 스펙에 맞춰 구현"이 자명해진다.
- **재현 가능** — 무엇을 했는지가 아니라, 어떤 파일을 읽고 어디에 썼는지가 기록된다.
- **다음 세션 컨텍스트** — `handoff.md`에 "완료된 것 / 남은 이슈 / 다음 단계"를 기록하면 다음 팀이 바로 이어받을 수 있다.

---

## 남은 과제

### 현재 상태
- 백엔드: 구조 완성, 실행 테스트 미완료
- 프론트엔드: 구조 작성만 완료, `npm install` 불가 (Node.js 미설치)
- 콘텐츠: 2명 캐릭터만 작성

### 다음 작업
- Node.js 설치 후 프론트엔드 구동 확인
- NPC 1:1 채팅 방식을 **씬 기반**으로 전환 (기획 단계에서 발견한 게임플레이 개선)
- HuggingFace 모델 통합

---

## 마무리: 배운 점

"게임 하나를 혼자 만드는 게" 아니라 "여러 역할을 분담하되 **각 역할이 작성한 아티팩트(문서, 코드, 파일)를 통해 협업**하는 것"이 얼마나 강력한지 느낀 작업이었다.

Claude Code 에이전트 3개를 하루 동안 병렬로 실행할 때:
1. 각 에이전트가 자신의 영역에 집중 → 코드 품질 향상
2. 에이전트 간 "누가 어떻게 결정했는가"가 `_workspace/` 파일로 명확 → 나중에 마이그레이션/변경이 쉬움
3. `handoff.md`로 다음 팀에 컨텍스트 전달 → 세션 연속성 확보

---

## 다음 포스트

[3편: 씬 기반 리팩토링 — NPC와의 관계도 시스템](03_scene_refactor.md)에서는 현재의 "자유 대화" 방식을 벗어나, 시나리오 분기와 캐릭터 관계도를 추가하는 과정을 다룬다.
