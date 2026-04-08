import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import MessageBubble from './MessageBubble';
import ChatInput from './ChatInput';
import { sendMessage } from '../../api/gameApi';
import { useGame } from '../../context/GameContext';

const SCENE_INFO = {
  1: { emoji: '🎉', name: '입과식' },
  2: { emoji: '💻', name: '알고리즘 수업' },
  3: { emoji: '🤝', name: '팀 프로젝트' },
};

function StatToast({ delta }) {
  const lines = Object.entries(delta)
    .filter(([, v]) => v !== 0)
    .map(([k, v]) => {
      const labels = { stat_speech: '언변', stat_dev: '개발', stat_planning: '기획', stat_stamina: '체력' };
      return `${labels[k] ?? k} ${v > 0 ? '+' : ''}${v}`;
    });
  if (lines.length === 0) return null;
  return <div className="stat-toast">{lines.join('  ')}</div>;
}

export default function ChatScreen() {
  const { sceneId } = useParams();
  const sceneIdNum = Number(sceneId);
  const navigate = useNavigate();
  const { userId, stats, applyStatDelta } = useGame();
  const [messages, setMessages] = useState([]);
  const [choices, setChoices] = useState([]);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState(null);
  const bottomRef = useRef(null);

  const sceneInfo = SCENE_INFO[sceneIdNum] ?? { emoji: '📖', name: `씬 ${sceneId}` };

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (text) => {
    setMessages(prev => [...prev, { role: 'user', speaker: '김지윤', content: text }]);
    setChoices([]);
    setLoading(true);
    setMessages(prev => [...prev, { role: 'assistant', speaker: '...', content: '...', typing: true }]);

    try {
      const data = await sendMessage({ userId, sceneId: sceneIdNum, protagonistLine: text });
      setMessages(prev => [
        ...prev.filter(m => !m.typing),
        { role: 'assistant', speaker: data.speaker, content: data.reply },
      ]);
      if (data.choices?.length > 0) setChoices(data.choices);
      if (data.stat_delta) {
        applyStatDelta(data.stat_delta);
        setToast(data.stat_delta);
        setTimeout(() => setToast(null), 2200);
      }
    } catch {
      setMessages(prev => [
        ...prev.filter(m => !m.typing),
        { role: 'assistant', speaker: '시스템', content: '(연결 오류. 백엔드가 실행 중인지 확인하세요.)' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-screen">
      {toast && <StatToast delta={toast} />}

      <div className="chat-header">
        <button className="back-btn" onClick={() => navigate('/')}>←</button>
        <div className="char-name">{sceneInfo.emoji} {sceneInfo.name}</div>
        <div className="stat-mini">
          <span><span className="val">{stats.speech}</span>언변</span>
          <span><span className="val">{stats.dev}</span>개발</span>
          <span><span className="val">{stats.planning}</span>기획</span>
        </div>
      </div>

      <div className="messages-container">
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', color: '#555', marginTop: 40, fontSize: 14 }}>
            김지윤의 대사를 입력해 이야기를 이어가세요.
          </div>
        )}
        {messages.map((m, i) => (
          <MessageBubble
            key={i}
            role={m.role}
            content={m.content}
            speakerName={m.speaker}
          />
        ))}
        <div ref={bottomRef} />
      </div>

      <ChatInput onSend={handleSend} choices={choices} disabled={loading} />
    </div>
  );
}
