# NPC 1:1 채팅 → 씬 기반 방식 전환

## 왜 이 작업을 했나

초기 설계는 NPC별로 채팅방을 만드는 방식이었다. 플레이어가 NPC에게 말을 걸면 NPC가 응답하는 구조. 그런데 이 방식은 플레이어가 항상 먼저 말을 걸어야 해서 "내가 왜 이 NPC한테 말 걸어야 하지?" 하는 수동적인 느낌이 있었다.

씬 기반으로 바꾸면 플레이어가 **김지윤의 대사를 직접 입력**하는 방식이 된다. "이 상황에서 김지윤이라면 뭐라고 할까?"를 고민하게 되어 몰입감이 생긴다. 게임의 핵심인 "김지윤을 키운다"는 느낌도 더 잘 산다.

## 무엇을 만들었나

### 씬 기반 구조로 전환된 파일들

| 항목 | 변경 전 | 변경 후 |
|------|---------|---------|
| URL | `/chat/:characterId` | `/scene/:sceneId` |
| 메인화면 | 캐릭터 카드 | 씬 카드 (입과식/알고리즘/팀프로젝트) |
| 입력 의미 | "내가" 하는 말 | "김지윤이" 하는 말 |
| API 요청 | `character_id + message` | `scene_id + protagonist_line` |
| API 응답 | `reply + stat_delta + choices` | `speaker + reply + stat_delta + choices` |
| 말풍선 | NPC 이름 없음 | NPC 이름 레이블 표시 |

### 새로 추가/변경된 파일
- `backend/routers/chat.py` — 씬 기반으로 로직 변경
- `backend/llm/mock.py` — 씬별 NPC 응답 + speaker 필드 포함
- `frontend/src/App.jsx` — `/scene/:sceneId` 라우트로 변경
- `frontend/src/api/gameApi.js` — `sendMessage(userId, sceneId, protagonistLine)`
- `frontend/src/components/Chat/ChatScreen.jsx` — 씬 기반 채팅 화면
- `frontend/src/components/Chat/MessageBubble.jsx` — speakerName 레이블 추가
- `frontend/src/components/Main/MainScreen.jsx` — 씬 목록 + 능력치 바
- `frontend/src/styles/global.css` — `bubble-speaker-name` 스타일 추가
- `scenario/scene_1.md` — 입과식
- `scenario/scene_2.md` — 알고리즘 수업
- `scenario/scene_3.md` — 팀 프로젝트

## 핵심 결정 사항

**씬 기반 선택의 핵심**: "플레이어 = 김지윤의 대리인" 구조. 플레이어가 상황을 읽고 김지윤의 말을 써주면, NPC들이 그 말에 반응한다. 능력치 변화는 김지윤이 어떻게 말했느냐에 따라 달라진다.

**speaker 필드 추가 이유**: 한 씬에 NPC가 여러 명 등장할 수 있다. 누가 말하는지 알아야 말풍선에 이름을 표시할 수 있고, LLM에게도 "이 NPC의 캐릭터로 응답하라"는 컨텍스트를 줄 수 있다.

## 막혔던 점 / 해결 방법

- Mock LLM이라 실제 AI 응답 없음 — 씬별로 하드코딩된 응답으로 흐름만 검증
- 프론트엔드 Node.js 미설치로 실제 실행 테스트 불가

## 다음 연결 작업

- `llm_integration` — HuggingFace 실제 모델 연동
- 설정 화면 (`SettingsScreen.jsx`) 구현
- 엔딩 화면 구현
- 저장/불러오기 UI 구현
- Node.js 설치 후 채팅 전체 흐름 통합 테스트
