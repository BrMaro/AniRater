import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Profile from './pages/Profile';
import GameSession from './pages/GameSession';
import BaseLayout from './components/BaseLayout';
import Login from './pages/Login';
import Register from './pages/Register';
import './styles/App.css'


const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <Router>
      <BaseLayout isAuthenticated={isAuthenticated}>        



      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/profile" element={isAuthenticated ? <Profile /> : <Login />} />
        <Route path="/game-session" element={isAuthenticated ? <GameSession /> : <Login />} />
      </Routes>
      </BaseLayout>
    </Router>
  );
};

export default App;
