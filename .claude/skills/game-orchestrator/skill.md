---
name: game-orchestrator
description: 김지윤 키우기 게임 개발 전체 워크플로우를 오케스트레이션한다. 콘텐츠 작가, 프론트엔드, 백엔드, AI 통합 에이전트 팀을 조율하여 MVP(4월 13일)를 목표로 개발을 진행. "게임 개발 시작해줘", "팀 전체 작업 지시해줘", "게임 만들어줘", "개발 시작" 요청 시 반드시 이 스킬을 사용할 것.
---

# 게임 오케스트레이터 스킬

## 에이전트 팀 구성

```
[오케스트레이터] ← 이 스킬을 실행하는 주체
  ├── content-writer   (콘텐츠 작가)
  ├── frontend-dev     (프론트엔드 개발자)
  ├── backend-dev      (백엔드 개발자)
  └── ai-integrator    (AI 통합 전문가)
```

## 실행 순서

### Phase 0: 준비 (시작 시)
1. `제작_의뢰서.md`와 `CLAUDE.md` 읽기
2. `handoff.md` 읽어 이전 작업 상태 파악
3. `plan.md` 업데이트 (이번 세션 목표/단계 기록)
2. 빈 디렉토리 확인 (`charactor/`, `scenario/`, `frontend/`, `backend/`)
3. `_workspace/` 폴더 생성
4. Phase 1 팀원 병렬 호출

### Phase 1: 기반 구축 (병렬)

3개 에이전트를 동시에 호출:

```
Agent(content-writer): "김지윤, 교수자, 동기 3명 캐릭터 파일 작성. scene_1~3 시나리오 작성."
Agent(backend-dev): "FastAPI 프로젝트 세팅. 데이터 스키마 정의. _workspace/api-spec.md 작성."
Agent(frontend-dev): "Vite+React 프로젝트 세팅. 채팅 화면 컴포넌트 골격 작성."
```

**완료 조건**:
- `charactor/` 파일 5개 이상
- `scenario/scene_1.md` ~ `scene_3.md` 존재
- `backend/main.py`, `backend/models.py` 존재
- `_workspace/api-spec.md` 존재
- `frontend/src/` 구조 존재

### Phase 2: 핵심 기능 개발 (병렬)

3개 에이전트를 동시에 호출:

```
Agent(backend-dev): "chat, game-state, save, load API 구현. Mock LLM 포함."
Agent(frontend-dev): "채팅 화면 완성. 메인 화면. _workspace/api-spec.md 기반 연동."
Agent(ai-integrator): "charactor/*.md 읽고 시스템 프롬프트 생성. HF Inference API 연결."
```

**완료 조건**:
- `http://localhost:8000/docs` 접근 가능
- `http://localhost:5173` 채팅 화면 표시
- `backend/llm/prompts/*.txt` 캐릭터 프롬프트 존재

### Phase 3: 통합 (순차)

```
1. Agent(ai-integrator): "backend/llm/hf_client.py와 main.py 연결. 엔드투엔드 테스트."
2. Agent(frontend-dev): "백엔드 실제 API 연동. Mock 제거."
3. Agent(content-writer): "scene_4~8 추가 시나리오 작성."
```

### Phase 4: MVP 완성

```
통합 테스트 체크리스트:
- [ ] 캐릭터 선택 → 채팅 시작
- [ ] 메시지 전송 → LLM 응답
- [ ] 능력치 변화 표시
- [ ] 저장/불러오기
- [ ] 이벤트 선택지 동작
```

## 데이터 전달 프로토콜

| 산출물 | 경로 | 생성자 | 소비자 |
|--------|------|--------|--------|
| 캐릭터 파일 | `charactor/*.md` | 콘텐츠 작가 | AI 통합 |
| 시나리오 | `scenario/scene_*.md` | 콘텐츠 작가 | 프론트엔드 |
| API 스펙 | `_workspace/api-spec.md` | 백엔드 | 프론트엔드, AI 통합 |
| React 앱 | `frontend/` | 프론트엔드 | — |
| FastAPI 서버 | `backend/` | 백엔드 | AI 통합 |
| LLM 모듈 | `backend/llm/` | AI 통합 | — |

## 에러 핸들링

| 에러 상황 | 대응 |
|---------|------|
| Phase 1 팀원 실패 | 1회 재시도, 재실패 시 해당 기능 없이 Phase 2 진행 |
| HF API 키 없음 | USE_MOCK=true로 계속 진행, 키 설정 안내 출력 |
| 프론트-백엔드 스키마 불일치 | backend-dev와 frontend-dev SendMessage로 즉시 조율 |
| 일정 지연 | MVP 범위 조정: 저장/불러오기 → 나중으로, 채팅 기능 우선 |

## 테스트 시나리오

### 정상 흐름
1. `_workspace/` 생성 확인
2. Phase 1 에이전트 3개 병렬 호출
3. 완료 조건 체크
4. Phase 2 진행
5. `localhost:8000/docs`에서 API 문서 확인
6. `localhost:5173`에서 채팅 UI 확인
7. 채팅 테스트: "안녕하세요" → LLM 응답 확인

### 에러 흐름
1. HF_TOKEN 없음 → Mock LLM으로 자동 전환 확인
2. 백엔드 다운 시 → 프론트엔드 에러 메시지 표시 확인

## 세션 종료 시

`handoff.md`를 업데이트한다:
- 완료된 Phase와 산출물 파일 목록
- 미완료 항목 및 블로커
- 다음 세션 시작 지점

## 진행 상황 보고

각 Phase 완료 시 다음 형식으로 사용자에게 보고:

```
## Phase {N} 완료

완성된 파일:
- {파일 목록}

다음 Phase: {설명}
예상 완료: {날짜}
```
