import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Login = ({ setIsAuthenticated }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!username || !password) {
            setMessage('Please fill in all fields');
            return;
        }

        setIsLoading(true);
        setMessage('');
        
        try {
            const response = await axios.post(
                'http://localhost:8000/login/', 
                { username, password },
                { withCredentials: true }  // Important for cookies
            );

            if (response.status === 200) {
                // Update authentication state
                setIsAuthenticated({
                    authenticated: true,
                    username: username
                });
                setMessage('Login successful');
                navigate('/', { replace: true });
            }
        } catch (error) {
            if (error.response && error.response.data) {
                setMessage(error.response.data.error || 'Login failed. Please try again.');
            } else {
                setMessage('Network error. Please try again.');
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="login-container">
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        disabled={isLoading}
                    />
                </div>
                <div className="form-group">
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        disabled={isLoading}
                    />
                </div>
                <button type="submit" disabled={isLoading}>
                    {isLoading ? 'Logging in...' : 'Login'}
                </button>
            </form>
            {message && <p className="message">{message}</p>}
        </div>
    );
};

export default Login;