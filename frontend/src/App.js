import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Profile from './components/Profile';
import GameSession from './components/GameSession';
import BaseLayout from './components/BaseLayout';
import Login from './Auth/Login';
import Register from './Auth/Register';
import Home from './components/Home'; // Add this import
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
        console.error("Error checking authentication: ", error);
        setIsAuthenticated({ authenticated: false, username: '' });
      }
    };

    checkAuth();
  }, []); // Empty dependency array for initial load only

  return (
    <Router>
      <BaseLayout isAuthenticated={isAuthenticated}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route 
            path="/login" 
            element={
              isAuthenticated.authenticated ? 
              <Navigate to="/" replace /> : 
              <Login setIsAuthenticated={setIsAuthenticated} />
            } 
          />
          <Route 
            path="/register" 
            element={
              isAuthenticated.authenticated ? 
              <Navigate to="/" replace /> : 
              <Register />
            } 
          />
          <Route 
            path="/profile" 
            element={
              isAuthenticated.authenticated ? 
              <Profile /> : 
              <Navigate to="/login" replace />
            } 
          />
          <Route 
            path="/game-session" 
            element={
              isAuthenticated.authenticated ? 
              <GameSession /> : 
              <Navigate to="/login" replace />
            } 
          />
        </Routes>
      </BaseLayout>
    </Router>
  );
};

export default App;