export default function MessageBubble({ role, content, speakerName }) {
  const isMine = role === 'user';
  return (
    <div className={`bubble-wrapper ${isMine ? 'mine' : 'other'}`}>
      {!isMine && (
        <div className="bubble-avatar" title={speakerName}>
          {speakerName?.[0] ?? '?'}
        </div>
      )}
      <div className="bubble-content">
        {!isMine && speakerName && (
          <span className="bubble-speaker-name">{speakerName}</span>
        )}
        <div className={`bubble ${isMine ? 'mine' : 'other'}`}>
          {content}
        </div>
      </div>
    </div>
  );
}
