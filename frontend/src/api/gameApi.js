const BASE_URL = '/';  // vite proxy 사용

export async function sendMessage({ userId = 1, sceneId = 1, protagonistLine }) {
  const res = await fetch(`${BASE_URL}chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      scene_id: sceneId,
      protagonist_line: protagonistLine,
    }),
  });
  if (!res.ok) throw new Error('채팅 API 오류');
  return res.json(); // { speaker, reply, stat_delta, choices }
}

export async function getGameState(userId = 1) {
  const res = await fetch(`${BASE_URL}game-state?user_id=${userId}`);
  if (!res.ok) throw new Error('게임 상태 API 오류');
  return res.json();
}

export async function recordEvent({ userId = 1, eventType, value = '' }) {
  const res = await fetch(`${BASE_URL}game-state/event`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, event_type: eventType, value }),
  });
  if (!res.ok) throw new Error('이벤트 API 오류');
  return res.json();
}

export async function login({ username, password }) {
  const res = await fetch(`${BASE_URL}auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) throw new Error('로그인 실패');
  return res.json(); // { ok, user_id, username }
}

export async function register({ username, password }) {
  const res = await fetch(`${BASE_URL}auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) throw new Error('회원가입 실패');
  return res.json();
}
