// src/components/LoginPage/LoginPage.jsx
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './LoginPage.css'; // Import the component's specific CSS

const LoginPage = ({ onLogin }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(''); // Clear previous errors


        if (username && password) {
        try {
            const API_BASE_URL = import.meta.env.VITE_API_URL;
            const body = {
                username: username,
                password: password,
            };
            console.log(API_BASE_URL); // Log to ensure VITE_API_URL is correctly loaded

            const response = await fetch(`${API_BASE_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            

            const data = await response.json();
            localStorage.setItem("jwtToken", data.jwtToken);
            localStorage.setItem("permission", data.permission);
            if (!response.ok) {
                // If response is not OK, throw an error with the message from the backend
                throw new Error(data.message || 'Login failed');
            }


            onLogin(); // Call the onLogin function from App.jsx
            navigate('/dashboard'); // Redirect to dashboard

        } catch (err) {
            // Catch any network errors or errors thrown from the response
            setError(err.message || 'An unexpected error occurred during login.');
        }
    } else {
        setError('Please fill in all fields and select your user type.');
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