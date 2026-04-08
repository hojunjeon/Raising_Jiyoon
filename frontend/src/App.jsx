import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { GameProvider } from './context/GameContext';
import MainScreen from './components/Main/MainScreen';
import ChatScreen from './components/Chat/ChatScreen';
import './styles/global.css';

export default function App() {
  return (
    <GameProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<MainScreen />} />
          <Route path="/scene/:sceneId" element={<ChatScreen />} />
        </Routes>
      </BrowserRouter>
    </GameProvider>
  );
}
