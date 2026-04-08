---
name: chat-ui-builder
description: 김지윤 키우기 게임의 KakaoTalk 스타일 채팅 UI를 React로 구축한다. 채팅 화면, 메인 화면, 설정 화면, 능력치 표시, 선택지 버튼 UI를 포함. "채팅 UI 만들어줘", "프론트엔드 구현해줘", "채팅 화면 개발해줘", "React 앱 만들어줘" 요청 시 반드시 이 스킬을 사용할 것.
---

# 채팅 UI 빌더 가이드

## 프로젝트 세팅

```bash
cd Chat_Game
npm create vite@latest frontend -- --template react
cd frontend
npm install react-router-dom
npm install
```

## 핵심 컴포넌트 구조

```
frontend/src/
├── App.jsx                      # 라우팅 (/, /chat/:characterId, /settings)
├── context/
│   └── GameContext.jsx          # 게임 상태 전역 관리
├── api/
│   └── gameApi.js               # 백엔드 API 호출 함수
├── components/
│   ├── Main/
│   │   ├── MainScreen.jsx       # 캐릭터 선택 + 능력치 대시보드
│   │   └── CharacterCard.jsx    # 개별 캐릭터 카드
│   ├── Chat/
│   │   ├── ChatScreen.jsx       # 채팅 화면 컨테이너
│   │   ├── MessageBubble.jsx    # 말풍선 컴포넌트
│   │   ├── ChatInput.jsx        # 텍스트 입력 + 전송
│   │   └── ChoiceButtons.jsx    # 이벤트 선택지 버튼
│   └── Settings/
│       └── SettingsScreen.jsx   # 저장/불러오기/초기화
└── styles/
    ├── global.css
    └── variables.css            # 색상 변수 (카카오 감성)
```

## KakaoTalk 스타일 CSS 가이드

```css
/* variables.css */
:root {
  --kakao-yellow: #FEE500;
  --chat-bg: #B2C7DA;        /* 카카오 채팅 배경 */
  --bubble-mine: #FEE500;    /* 내 말풍선 */
  --bubble-other: #FFFFFF;   /* 상대 말풍선 */
  --header-bg: #1E1E1E;
  --font-main: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
}
```

```css
/* 채팅 화면 레이아웃 */
.chat-screen {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 480px;    /* 모바일 퍼스트 */
  margin: 0 auto;
}

.chat-header {
  background: var(--header-bg);
  color: white;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: var(--chat-bg);
}

/* 말풍선 */
.bubble-wrapper {
  display: flex;
  margin-bottom: 8px;
}
.bubble-wrapper.mine { justify-content: flex-end; }
.bubble-wrapper.other { justify-content: flex-start; }

.bubble {
  max-width: 70%;
  padding: 8px 12px;
  border-radius: 16px;
  font-size: 14px;
  line-height: 1.5;
}
.bubble.mine { background: var(--bubble-mine); border-radius: 16px 4px 16px 16px; }
.bubble.other { background: var(--bubble-other); border-radius: 4px 16px 16px 16px; }
```

## 핵심 컴포넌트 구현 패턴

### GameContext.jsx
```jsx
const GameContext = createContext();

export function GameProvider({ children }) {
  const [gameState, setGameState] = useState({
    stats: { speech: 0, dev: 0, planning: 0 },
    currentScene: 1,
    absences: 0,
  });
  
  const updateStats = (delta) => {
    setGameState(prev => ({
      ...prev,
      stats: {
        speech: prev.stats.speech + (delta.speech || 0),
        dev: prev.stats.dev + (delta.dev || 0),
        planning: prev.stats.planning + (delta.planning || 0),
      }
    }));
  };
  
  return (
    <GameContext.Provider value={{ gameState, updateStats }}>
      {children}
    </GameContext.Provider>
  );
}
```

### ChatInput + ChoiceButtons
```jsx
// 이벤트 씬: 선택지 모드 / 일반 씬: 텍스트 입력 모드
function ChatInput({ onSend, choices }) {
  if (choices?.length > 0) {
    return (
      <div className="choices-container">
        {choices.map((choice, i) => (
          <button key={i} onClick={() => onSend(choice.text)} className="choice-btn">
            {choice.text}
          </button>
        ))}
      </div>
    );
  }
  return <TextInput onSend={onSend} />;
}
```

### gameApi.js
```js
const BASE_URL = 'http://localhost:8000';

export async function sendMessage(characterId, message) {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ character_id: characterId, message }),
  });
  return res.json();  // { reply, stat_delta, choices }
}

export async function getGameState() {
  const res = await fetch(`${BASE_URL}/game-state`);
  return res.json();
}
```

## 구현 우선순위

1. **채팅 화면 + 기본 말풍선** (MVP 필수)
2. **백엔드 API 연동** (sendMessage)
3. **능력치 표시** (헤더 또는 사이드)
4. **선택지 버튼 UI**
5. **메인 화면** (캐릭터 목록)
6. **설정/저장** (저장 화면)

## 에러 상태 처리

- 로딩 중: 말풍선 자리에 "..." 애니메이션
- API 오류: 토스트 메시지 + 재시도 버튼
- 오프라인: 로컬스토리지 캐시 사용
