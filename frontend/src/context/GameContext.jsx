import { createContext, useContext, useState, useCallback } from 'react';
import { getGameState } from '../api/gameApi';

const GameContext = createContext(null);

export function GameProvider({ children }) {
  const [userId, setUserId] = useState(
    () => Number(localStorage.getItem('user_id') || 1)
  );
  const [stats, setStats] = useState({
    speech: 40, dev: 5, planning: 20, stamina: 30,
  });
  const [scene, setScene] = useState(1);

  const applyStatDelta = useCallback((delta) => {
    setStats(prev => ({
      speech:   prev.speech   + (delta.stat_speech   || 0),
      dev:      prev.dev      + (delta.stat_dev       || 0),
      planning: prev.planning + (delta.stat_planning  || 0),
      stamina:  prev.stamina  + (delta.stat_stamina   || 0),
    }));
  }, []);

  const refreshFromServer = useCallback(async () => {
    try {
      const data = await getGameState(userId);
      setStats({
        speech:   data.stat_speech,
        dev:      data.stat_dev,
        planning: data.stat_planning,
        stamina:  data.stat_stamina,
      });
      setScene(data.current_scene);
    } catch {
      // 서버 미연결 시 로컬 상태 유지
    }
  }, [userId]);

  return (
    <GameContext.Provider value={{ userId, setUserId, stats, scene, applyStatDelta, refreshFromServer }}>
      {children}
    </GameContext.Provider>
  );
}

export function useGame() {
  return useContext(GameContext);
}
