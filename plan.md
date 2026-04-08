# 작업 계획 — MVP Day 1

## 목표
김지윤 키우기 MVP의 기반 구조 구축.
캐릭터 파일, FastAPI 백엔드, React 프론트엔드를 완성하여 "채팅 → 응답 → 능력치 변화" 흐름이 동작하게 한다.

## 완료 기준
- [x] 캐릭터 파일 2개 (김지윤, 이민준) 작성 완료
- [x] FastAPI 백엔드 구조 완성 (`POST /chat`, `GET /game-state`, auth)
- [x] Mock LLM으로 채팅 API 동작
- [x] React + Vite 프론트엔드 구조 완성 (채팅 화면, 메인 화면)
- [x] API 스펙 문서 작성 (`_workspace/api-spec.md`)
- [ ] 백엔드 실행 확인 (`uvicorn` 정상 기동)
- [ ] 프론트엔드 실행 확인 (`npm run dev` 정상 기동)
- [ ] 채팅 전송 → Mock 응답 → 능력치 토스트 표시 확인

## 단계
1. ~~캐릭터 파일 작성 (김지윤, 이민준)~~ ✅
2. ~~FastAPI 백엔드 생성 (models, routers, mock LLM)~~ ✅
3. ~~React 프론트엔드 생성 (ChatScreen, MainScreen, GameContext)~~ ✅
4. 백엔드 pip install + uvicorn 실행 확인 (사용자 직접)
5. 프론트엔드 npm install + npm run dev 확인 (사용자 직접, Node.js 필요)
6. Day 2: LLM 연동 (`/llm-integrator` 스킬)

## 참고 자료
- `charactor/김지윤.md`, `charactor/이민준.md`
- `backend/main.py`, `backend/routers/`
- `frontend/src/`
- `_workspace/api-spec.md`
