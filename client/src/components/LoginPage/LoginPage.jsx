// src/components/LoginPage/LoginPage.jsx
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './LoginPage.css'; // Import the component's specific CSS

const LoginPage = ({ onLogin }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();
        setError(''); // Clear previous errors

        // Mock authentication: replace with actual API call
        if (username === 'user' && password === 'password') {
            onLogin(); // Call the onLogin function from App.jsx
            navigate('/dashboard'); // Redirect to dashboard
        } else {
            setError('Invalid username or password');
        }
    };

    return (
        <div className="login-container">
            <h2 className="login-heading">Login</h2>
            <form onSubmit={handleSubmit} className="login-form">
                <div className="login-form-group">
                    <label htmlFor="username" className="login-label">Username:</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className="login-input"
                        required
                    />
                </div>
                <div className="login-form-group">
                    <label htmlFor="password" className="login-label">Password:</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="login-input"
                        required
                    />
                </div>
                {error && <p className="login-error">{error}</p>}
                <button type="submit" className="login-button">Login</button>
            </form>
            <p className="login-switch-link">
                Don't have an account? <Link to="/register" className="login-link">Register here</Link>
            </p>
        </div>
    );
};

export default LoginPage;