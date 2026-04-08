# API 스펙

## Base URL
`http://localhost:8000`

## 엔드포인트 목록

| Method | Path | 설명 |
|--------|------|------|
| GET | / | 헬스체크 |
| POST | /auth/register | 회원가입 |
| POST | /auth/login | 로그인 |
| POST | /chat | 캐릭터 채팅 |
| GET | /game-state | 게임 상태 조회 |
| POST | /game-state/event | 이벤트 기록 |
| POST | /game-state/save | 게임 저장 |
| GET | /game-state/load | 저장 불러오기 |

---

## POST /auth/register

**Request**
```json
{ "username": "jiyoon", "password": "1234" }
```
**Response**
```json
{ "ok": true, "user_id": 1, "username": "jiyoon" }
```

---

## POST /auth/login

**Request**
```json
{ "username": "jiyoon", "password": "1234" }
```
**Response**
```json
{ "ok": true, "user_id": 1, "username": "jiyoon" }
```

---

## POST /chat

**Request**
```json
{
  "user_id": 1,
  "character_id": "이민준",
  "message": "오늘 알고리즘 너무 어렵지 않아요?",
  "scene": 2
}
```
**Response**
```json
{
  "reply": "코드는 일단 동작하게 만들고, 예쁘게는 나중에 해요.",
  "stat_delta": { "stat_dev": 3 },
  "choices": ["더 물어본다", "고맙다고 한다", "화제를 돌린다"]
}
```

---

## GET /game-state?user_id=1

**Response**
```json
{
  "id": 1,
  "user_id": 1,
  "stat_speech": 42,
  "stat_dev": 8,
  "stat_planning": 21,
  "stat_stamina": 30,
  "absences": 0,
  "tardiness": 0,
  "subject_eval_pass": 0,
  "subject_eval_fail": 0,
  "monthly_eval_pass": 0,
  "monthly_eval_fail": 0,
  "sw_test_grade": "",
  "current_scene": 2,
  "ending": ""
}
```

---

## POST /game-state/event

**event_type 목록**

| 값 | 설명 |
|----|------|
| `subject_eval_pass` | 과목 평가 통과 |
| `subject_eval_fail` | 과목 평가 실패 |
| `monthly_eval_pass` | 월말 평가 통과 |
| `monthly_eval_fail` | 월말 평가 실패 |
| `tardiness` | 지각/조퇴 (3회 누적 = 결석 1회) |
| `absence` | 결석 직접 기록 |
| `sw_test` | SW 역량 테스트 (value에 등급) |
| `advance_scene` | 씬 진행 |

**Request**
```json
{ "user_id": 1, "event_type": "tardiness", "value": "" }
```
**Response**
```json
{ "ok": true, "state": { ...GameState } }
```
