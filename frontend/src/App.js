import React, { useEffect, useReducer, useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import Profile from './components/Profile';
import GameSession from './components/GameSession';
import BaseLayout from './components/BaseLayout';
import Login from './Auth/Login';
import Register from './Auth/Register';
import './styles/App.css'


const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState({"authenticated":false, username: ''});

  // Authentication
  useEffect(()=>{
    const checkAuth = async () =>{
      try {
        const response = await axios.get('http://localhost:8000/check-auth/',{withCredentials:true});
        setIsAuthenticated(response.data);
      } catch (error) {
        console.error("Error checking authentication: ", error);
      }
    };

    checkAuth();
  }, 2000);


  return (
    <Router>
      <BaseLayout isAuthenticated={isAuthenticated}>        
      {/* 
       IF i click animguess, it should reload homepage,
       IF i click on login and is sucessfull, reload homepage
       IF i click on login and is succesfull, reload homepage
      */}

      <Routes>
        {/* <Route path='/home' element={<Home/>}/> */}
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
