import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Login = () => {
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

        setIsLoading(true); // Show loading state
        setMessage(''); // Clear any previous message
        try {
            const response = await axios.post('http://localhost:8000/login/', { username, password });

            // Assuming response contains success message and possibly a token
            if (response.status === 200) {
                setMessage('Login successful');
                navigate("/")
                // localStorage.setItem('token', response.data.token); // Store JWT token (if applicable)
                // Redirect or update UI as needed (e.g., go to profile page)
            } else {
                setMessage('Login failed. Please check your credentials.');
            }
        } catch (error) {
            // Display specific error messages if available
            if (error.response && error.response.data) {
                setMessage(error.response.data.error || 'Login failed. Please try again.');
            } else {
                setMessage('Network error. Please try again.');
            }
        }
        setIsLoading(false);
    };

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    disabled={isLoading} // Disable input while loading
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    disabled={isLoading} // Disable input while loading
                />
                <button type="submit" disabled={isLoading}>
                    {isLoading ? 'Logging in...' : 'Login'} {/* Show loading state in button */}
                </button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default Login;
