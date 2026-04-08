---
name: blog-orchestrator
description: 김지윤 키우기 개발 과정을 블로그 포스트로 자동 생성하는 오케스트레이터. blog-collector → blog-writer → blog-editor 3단계 파이프라인을 실행하여 blog/ 폴더에 최종 발행 가능한 포스트를 생성한다. "블로그 써줘", "개발 일지 만들어줘", "이번 작업 블로그로 정리해줘", "블로그 포스트 생성해줘", "blog post 작성" 요청 시 반드시 이 스킬을 사용할 것.
---

# 블로그 오케스트레이터

김지윤 키우기 개발 과정을 블로그 포스트로 자동 생성하는 파이프라인.

## 실행 모드: 서브 에이전트 (파이프라인)

각 단계가 이전 단계의 파일 출력에 의존하므로 순차 실행한다.

## 에이전트 구성

| 단계 | 에이전트 | 역할 | 입력 | 출력 |
|------|---------|------|------|------|
| Phase 1 | `blog-collector` | 개발 데이터 수집 | 프로젝트 파일들 | `_workspace/01_blog_raw_data.md` |
| Phase 2 | `blog-writer` | 초안 작성 | `01_blog_raw_data.md` | `_workspace/02_blog_draft.md` |
| Phase 3 | `blog-editor` | 편집 및 완성 | `02_blog_draft.md` | `blog/day{N}_{slug}.md` |

## 워크플로우

### Phase 0: 사전 준비

1. `handoff.md`를 읽어 현재 개발 일차(Day N) 확인
2. `blog/` 폴더 유무 확인 — 없으면 생성
3. `_workspace/` 폴더 유무 확인 — 없으면 생성
4. 이미 같은 Day의 블로그가 있는지 확인 (`blog/day{N}_*.md`)
   - 있으면 사용자에게 덮어쓸지 확인 후 진행

### Phase 1: 데이터 수집

`blog-collector` 에이전트를 서브 에이전트로 호출:

```
Agent(
  subagent_type: "Explore",
  model: "opus",
  prompt: """
  .claude/agents/blog-collector.md와 .claude/skills/blog-collector/skill.md를 읽고,
  그 지침에 따라 프로젝트 개발 데이터를 수집하라.
  
  프로젝트 루트: C:\Users\SSAFY\Desktop\Chat_Game
  
  수집 완료 후 _workspace/01_blog_raw_data.md에 저장하라.
  """
)
```

완료 확인: `_workspace/01_blog_raw_data.md` 존재 여부

### Phase 2: 초안 작성

`blog-writer` 에이전트를 서브 에이전트로 호출:

```
Agent(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
  .claude/agents/blog-writer.md와 .claude/skills/blog-writer/skill.md를 읽고,
  그 지침에 따라 블로그 초안을 작성하라.
  
  입력: _workspace/01_blog_raw_data.md
  출력: _workspace/02_blog_draft.md
  
  프로젝트 루트: C:\Users\SSAFY\Desktop\Chat_Game
  """
)
```

완료 확인: `_workspace/02_blog_draft.md` 존재 여부

### Phase 3: 편집 및 완성

`blog-editor` 에이전트를 서브 에이전트로 호출:

```
Agent(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
  .claude/agents/blog-editor.md를 읽고, 그 지침에 따라 블로그 초안을 편집하라.
  
  입력: _workspace/02_blog_draft.md
  최종 출력: blog/day{N}_{slug}.md (N은 handoff.md의 Day 번호)
  편집 메모: _workspace/03_blog_edit_notes.md
  
  프로젝트 루트: C:\Users\SSAFY\Desktop\Chat_Game
  
  편집 시 실제 코드 파일을 Read로 확인하여 코드 스니펫 정확성을 검증하라.
  """
)
```

### Phase 4: 완료 보고

최종 출력:
```
블로그 포스트 생성 완료
- 최종 파일: blog/day{N}_{slug}.md
- 제목: {포스트 제목}
- 분량: {글자 수}자
- 편집 메모: _workspace/03_blog_edit_notes.md
```

## 에러 핸들링

| 상황 | 대응 |
|------|------|
| `handoff.md` 없음 | 사용자에게 "handoff.md가 없습니다. 먼저 개발 작업을 진행해 주세요." 안내 후 중단 |
| Phase 1 실패 (수집 데이터 없음) | Phase 1 재시도 1회. 재실패 시 "데이터 수집에 실패했습니다." 보고 후 중단 |
| Phase 2 실패 (초안 없음) | Phase 2 재시도 1회. 재실패 시 수집 데이터만으로 임시 초안 생성 |
| Phase 3 실패 | 편집 없이 초안을 최종본으로 사용 (`_workspace/02_blog_draft.md` → `blog/` 복사) |

## 테스트 시나리오

### 정상 흐름
```
사용자: "이번 작업 블로그로 써줘"
→ Phase 0: Day 2 확인, 폴더 준비
→ Phase 1: handoff.md + plan.md + git log → 01_blog_raw_data.md
→ Phase 2: raw data → 02_blog_draft.md (초안)
→ Phase 3: draft → blog/day2_scene_based_chat.md (최종본)
→ 완료 보고
```

### 에러 흐름
```
Phase 1에서 handoff.md 없음
→ 사용자에게 handoff.md 작성 요청 안내
→ 중단
```
