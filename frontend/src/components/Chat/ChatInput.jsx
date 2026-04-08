import { useState } from 'react';
import ChoiceButtons from './ChoiceButtons';

export default function ChatInput({ onSend, choices, disabled }) {
  const [text, setText] = useState('');

  if (choices?.length > 0) {
    return (
      <div className="chat-input-area">
        <ChoiceButtons choices={choices} onChoose={(c) => { onSend(c); }} />
      </div>
    );
  }

  const handleSend = () => {
    if (!text.trim() || disabled) return;
    onSend(text.trim());
    setText('');
  };

  return (
    <div className="chat-input-area">
      <div className="text-input-row">
        <input
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSend()}
          placeholder="김지윤의 대사를 입력하세요..."
          disabled={disabled}
        />
        <button className="send-btn" onClick={handleSend} disabled={disabled}>
          전송
        </button>
      </div>
    </div>
  );
}
