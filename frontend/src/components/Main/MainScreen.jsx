import { Link } from 'react-router-dom';
import { useGame } from '../../context/GameContext';
import { useEffect } from 'react';

const SCENES = [
  { id: 1, emoji: '🎉', name: '입과식', desc: '드디어 SSAFY 15기 서울 6반이 시작된다.' },
  { id: 2, emoji: '💻', name: '알고리즘 수업', desc: '첫 번째 알고리즘 강의. 개발 경험이 거의 없는 지윤에겐 낯선 세계.' },
  { id: 3, emoji: '🤝', name: '팀 프로젝트', desc: '팀이 꾸려졌다. 의견 충돌도, 협력도 시작된다.' },
];

function StatBar({ label, value }) {
  const pct = Math.min(100, Math.max(0, value));
  return (
    <div className="stat-row">
      <span className="stat-label">{label}</span>
      <div className="stat-bar-bg">
        <div className="stat-bar-fill" style={{ width: `${pct}%` }} />
      </div>
      <span className="stat-value">{value}</span>
    </div>
  );
}

export default function MainScreen() {
  const { stats, refreshFromServer } = useGame();

  useEffect(() => {
    refreshFromServer();
  }, []);

  return (
    <div className="main-screen">
      <h1>김지윤 키우기</h1>

      <div className="stats-panel">
        <h2>현재 능력치</h2>
        <StatBar label="언변" value={stats.speech} />
        <StatBar label="개발" value={stats.dev} />
        <StatBar label="기획" value={stats.planning} />
        <StatBar label="체력" value={stats.stamina} />
      </div>

      <div className="character-list">
        {SCENES.map(s => (
          <Link key={s.id} to={`/scene/${s.id}`} className="character-card">
            <div className="avatar">{s.emoji}</div>
            <div className="info">
              <h3>{s.name}</h3>
              <p>{s.desc}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
