export default function ChoiceButtons({ choices, onChoose }) {
  return (
    <div className="choices-container">
      {choices.map((text, i) => (
        <button key={i} className="choice-btn" onClick={() => onChoose(text)}>
          {text}
        </button>
      ))}
    </div>
  );
}
