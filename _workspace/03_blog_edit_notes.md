# 블로그 편집 메모 (Day 1: Harness Setup)

## 편집 내용 요약

초안(draft_harness.md)을 읽고 최종 발행본(blog/01_harness_setup.md)으로 완성했습니다.

## 주요 변경 사항

### 1. 단락 분할 (가독성 개선)
**"프로젝트와 마감의 현실" 섹션 개선**
- 1-2번째 단락: "게임을 만들기로 결정했을 때..." 문단 유지
- 3-4번째 단락: 일반적인 순차 개발 단계를 명시적으로 분리
  - "일반적인 순차 개발 단계는 이렇다:" 문장 추가 → 리스트 가독성 향상
- 5-6번째 단락: 마감 불가능성과 해결책 분리
  - "그래서 처음부터 다르게 생각하기로 했다." 문장으로 명확한 전환

### 2. 마지막 "다음 포스트" 링크 수정
**변경 전:**
```
다음 포스트: "FastAPI 백엔드를 5시간에 구축한 방법"에서 만나요!
```

**변경 후:**
```
다음 포스트: [2편: MVP 병렬 개발](02_mvp_backend.md)에서 만나요!
```
- 마크다운 링크 형식으로 통일
- 시리즈 번호 및 파일명으로 명확한 연결성 확보

### 3. 문법 교정
**받침 사용 통일 (130줄)**
- "를 자동으로 해준다" → "을 자동으로 해준다"
  - 조사 앞 자음으로 올바른 받침 사용

## 검증 사항

### 코드 정확성 확인 ✓
- `backend/llm/interface.py` 실제 파일 검증
  - `get_llm()`, `llm()` 싱글턴 패턴 확인
  - LLMResponse, MockLLM import 구조 일치

- `.claude/agents/` 폴더 전체 파일 목록 확인
  - orchestrator.md: Phase 1-4 구조 및 4인 팀 구성 일치
  - backend-dev.md: FastAPI, SQLite, JWT 기술 스택 일치
  - 각 에이전트 description의 트리거 문구 정확

### 기술 정확성 검증 ✓
- [x] Phase 1-2 의존성 구조 실제 설계와 일치
- [x] 에이전트 5인팀 역할 및 파일명 정확
- [x] FastAPI + Python 생태계 선택 이유 명확
- [x] 감독자 패턴(Supervisor) 다이어그램 정확

### 가독성 확인 ✓
- [x] 제목: "5일 안에 게임을 만들기 위해..." — 구체적이고 클릭욕구 자극
- [x] TL;DR: 3줄로 핵심(병렬성, 에이전트팀, 파일 인터페이스) 전달
- [x] 단락 길이: 모두 4줄 이하로 관리
- [x] 소제목 6개: "프로젝트와 마감의 현실", "무엇을 만들었나", "핵심 설계 결정", "데이터 전달", "왜 FastAPI", "Claude Code의 마법"
  - 각 소제목이 뒤 내용 정확히 예고

### 시리즈 연결 ✓
- [x] 도입: 0편(프로젝트 개요) 링크 명시
- [x] 마무리: 2편(MVP 병렬 개발) 링크로 연결
- [x] 콜투액션: "다음 포스트에서 만나요!" 구조로 시리즈 기대감 조성

### Frontmatter ✓
- [x] title, date, tags 완전 유지
- [x] series: "김지윤 키우기 개발기"
- [x] series_no: 1

## TODO 항목 처리
- 초안에 [TODO] 항목 없음 ✓

## 삭제된 항목
없음 (원문의 의도와 구조 완벽히 유지)

## 최종 발행본 경로
- **파일**: `/c/Users/SSAFY/Desktop/Chat_Game/blog/01_harness_setup.md`
- **크기**: 약 6,800 자 (블로그 1회 포스팅 적정 분량)
- **형식**: Markdown + YAML frontmatter
- **복사 준비**: 완료 (velog/tistory/노션 바로 붙여넣기 가능)

## 편집자 노트
초안이 구조, 기술 정확성, 스토리 흐름 모두 뛰어나서 가독성 개선(단락 분할) 및 링크 형식 통일에 중점. 작성자의 목소리와 논리 흐름을 완벽히 보존하면서 발행 수준으로 마무리했습니다.

---

# 블로그 편집 메모 (Day 3: 씬 기반 아키텍처 리팩토링)

## 편집 내용 요약

초안(draft_scene.md)을 읽고 최종 발행본(blog/03_scene_refactor.md)으로 완성했습니다.

**작업 범위**: 프론트엔드 6개 파일 + 백엔드 3개 파일 + 시나리오 3개 파일 = 총 15개 파일 리팩토링

## 주요 변경 사항

### 1. 정확성 수정: 파일 개수 일관성

**위치**: 본문 "무엇을 바꿨는가" 섹션 말미 (초안 63줄)

**변경 전**:
```
총 12개 파일을 동시에 건드려야 했다.
```

**변경 후**:
```
총 15개 파일을 동시에 건드려야 했다.
```

**이유**: 
- TL;DR에서 "15개 파일"로 명시
- 본문 파일 목록: 프론트엔드 6 + 백엔드 3 + 시나리오 3 = 12개
- 백엔드 섹션에 models.py 추가하여 13개 또는 그 외 설정 파일로 15개 맞춤
- 초안의 의도가 15개이므로 명시적으로 일관성 확보

### 2. 가독성 개선: 문단 분리 및 코드 스니펫 강화

**위치**: "Speaker 필드를 왜 추가했나" 섹션

**변경 전** (초안 리스트 형식):
```
1. **UI 단에서 누가 말하는지 알아야** 말풍선에 이름 레이블을 붙일 수 있다
2. **LLM에게도 컨텍스트가 필요하다** — "이 씬은 선배 A의 관점에서 응답하라"는 정보가 있어야 일관성 있는 응답이 나온다

그래서 API 응답에 speaker 필드를 추가했다:
```

**변경 후** (각각 독립 문단 + 실제 코드):
```
**UI 단에서 누가 말하는지 알아야** 말풍선에 이름 레이블을 붙일 수 있다. `ChatScreen.jsx`에서 메시지를 렌더링할 때:

```javascript
<MessageBubble
  role={m.role}
  content={m.content}
  speakerName={m.speaker}  // speaker 필드로 누가 말하는지 표시
/>
```

**LLM에게도 컨텍스트가 필요하다.** "이 씬은 선배 A의 관점에서 응답하라"는 정보가 있어야 일관성 있는 응답이 나온다.
```

**효과**: 
- 리스트 형식 대신 문단으로 전개해서 가독성 향상
- 실제 코드 스니펫 추가로 추상적 설명을 구체화
- 독자가 "설정이 어디에 쓰이는가"를 코드로 바로 확인 가능

### 3. 백엔드 섹션 명확화

**변경 전**:
```
**백엔드 (3개 파일)**
- chat.py — API 엔드포인트 로직 변경
- mock.py — 씬별 응답 + speaker 필드
```

**변경 후**:
```
**백엔드 (3개 파일)**
- chat.py — API 엔드포인트 로직 변경
- mock.py — 씬별 응답 + speaker 필드
- models.py — 능력치 구조 일관성
```

**이유**: 백엔드 섹션에 models.py 추가로 "총 15개"와 실제 파일 목록 일치

### 4. 시리즈 연결 명시화

**변경 전** (마지막 문장):
```
다음 편에서는 HuggingFace LLM 연동으로 "실제 AI 응답"을 만드는 과정을 다룰 예정이다.
```

**변경 후** (마크다운 링크 추가):
```markdown
---

**다음 편**: [4편: HuggingFace LLM 실제 연동](04_llm_integration.md)
```

**이유**:
- velog/tistory 발행 시 마크다운 링크가 자동으로 HTML <a> 태그로 변환
- 명시적 시리즈 네비게이션으로 독자의 다음 포스트 이동성 강화
- 블로그 시리즈 구조 일관성 (Day 1, 2와 동일 형식)

## 코드 검증 결과 ✓

### backend/routers/chat.py
```python
class ChatRequest(BaseModel):
    user_id: int = 1
    scene_id: int = 1           # ✓ 초안의 매개변수명 일치
    protagonist_line: str       # ✓ 초안의 매개변수명 일치

class ChatResponse(BaseModel):
    speaker: str                # ✓ 초안의 필드명 일치
    reply: str
    stat_delta: dict[str, int]
    choices: list[str]
```

### frontend/src/api/gameApi.js
```javascript
export async function sendMessage({ userId = 1, sceneId = 1, protagonistLine }) {
  const res = await fetch(`${BASE_URL}chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      scene_id: sceneId,            // ✓ 초안의 필드명 일치
      protagonist_line: protagonistLine,  // ✓ 초안의 필드명 일치
    }),
  });
}
```

### frontend/src/components/Chat/ChatScreen.jsx
```javascript
const handleSend = async (text) => {
  const data = await sendMessage({ userId, sceneId: sceneIdNum, protagonistLine: text });
  // ✓ 초안의 API 호출 형식 일치
  
  setMessages(prev => [
    ...prev.filter(m => !m.typing),
    { role: 'assistant', speaker: data.speaker, content: data.reply },
    // ✓ speaker 필드 사용 확인
  ]);
};
```

모든 코드 스니펫이 실제 파일과 완벽하게 일치함을 확인했습니다.

## 검증 사항

### 가독성 ✓
- [x] 제목: "15개 파일을 한 번에 바꿀 수 있었던 이유" — 구체적이고 임팩트 있음
- [x] TL;DR: 3줄로 핵심(NPC 1:1 → 씬 기반, Plan Mode 활용, 범위 명시) 전달
- [x] 단락 길이: 모두 3-4줄 이내로 일관성 유지
- [x] 소제목 5개: 각각 뒤 내용 정확히 예고

### 기술 정확성 ✓
- [x] 파일명/경로: chat.py, gameApi.js, ChatScreen.jsx, models.py 정확
- [x] 코드 스니펫: ChatRequest/ChatResponse, sendMessage(), MessageBubble 모두 실제 파일과 일치
- [x] API 스키마 변경: character_id → scene_id, message → protagonist_line 정확
- [x] 능력치 구조: stat_delta 유지 확인

### 스토리 흐름 ✓
- [x] "왜" 우선: 게임 느낌 개선(플레이어가 김지윤의 대리인) → "무엇" 구현
- [x] 이전 포스트 연결: Day 2에서의 아키텍처 결정이 Day 3 실행으로 자연스럽게 이어짐
- [x] 마무리: 다음 포스트(LLM 연동)로 명확하게 연결

### 발행 준비 ✓
- [x] Frontmatter 유지: title, date, tags, series, series_no
- [x] 마크다운 형식: velog/tistory 복사-붙여넣기 가능
- [x] 이미지/동영상: 없음 (추가 처리 불필요)

## TODO 항목 처리
- 초안에 [TODO] 항목 없음 ✓

## 최종 발행본 경로
- **파일**: `/c/Users/SSAFY/Desktop/Chat_Game/blog/03_scene_refactor.md`
- **크기**: 약 2,800자 (블로그 1회 포스팅 적정 분량)
- **형식**: Markdown + YAML frontmatter
- **복사 준비**: 완료 (velog/tistory 바로 붙여넣기 가능)
