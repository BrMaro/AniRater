import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Profile from './components/Profile';
import GameSession from './components/GameSession';
import BaseLayout from './components/BaseLayout';
import Login from './Auth/Login';
import Register from './Auth/Register';
import Home from './components/Home'; 

import './styles/App.css'

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState({ authenticated: false, username: '' });

  // Authentication check
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await axios.get('http://localhost:8000/check-auth/', { withCredentials: true });
        setIsAuthenticated(response.data);
      } catch (error) {
        console.error("Erro\r checking authentication: ", error);
        setIsAuthenticated({ authenticated: false, username: '' });
      }
    };

    checkAuth();
  }, []); 

  return (
    <Router>
      <BaseLayout isAuthenticated={isAuthenticated}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={isAuthenticated.authenticated ? <Navigate to="/" replace /> : 
              <Login setIsAuthenticated={setIsAuthenticated} />
            } 
          />
          <Route path="/register" element={isAuthenticated.authenticated ? <Navigate to="/" replace /> : 
              <Register />
            } 
          />
          <Route path="/profile" element={isAuthenticated.authenticated ? <Profile /> : 
              <Navigate to="/login" replace />
            } 
          />
          <Route path="/game-session" element={<GameSession isAuthenticated={isAuthenticated.authenticated}username={isAuthenticated.username}/>
            }
          />
        </Routes>
      </BaseLayout>
    </Router>
  );
};

export default App;