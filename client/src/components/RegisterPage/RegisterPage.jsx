// src/components/RegisterPage/RegisterPage.jsx
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './RegisterPage.css'; // Import the component's specific CSS

const RegisterPage = ({ onRegister }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [userType, setUserType] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        if (password !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        if (!userType) {
            setError('Please select if you are a Patient or a Practitioner');
            return;
        }

        if (username && password && userType && email) {
            console.log(`Attempting to register: Username: ${username}, UserType: ${userType}`);
            try {
                const API_BASE_URL = import.meta.env.VITE_API_URL;
                const body = {
                    username: username,
                    email: email,
                    password: password,
                    userType: userType
                };
                console.log(API_BASE_URL); // Log to ensure VITE_API_URL is correctly loaded

                const response = await fetch(`${API_BASE_URL}/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(body)
                });

                const data = await response.json();
                if (!response.ok) {
                    // If response is not OK, throw an error with the message from the backend
                    throw new Error(data.message || 'Registration failed');
                }

                setSuccess('Registration successful! Redirecting to login...');

                setTimeout(() => {
                    onRegister(); // This function often just signals completion, not necessarily logs in
                    navigate('/login');
                }, 1500); // Redirect after 1.5 seconds

            } catch (err) {
                // Catch any network errors or errors thrown from the response
                setError(err.message || 'An unexpected error occurred during registration.');
            }
        } else {
            setError('Please fill in all fields and select your user type.');
        }
    };

    return (
        <div className="register-container">
            <h2 className="register-heading">Register</h2>
            <form onSubmit={handleSubmit} className="register-form">
                <div className="register-form-group">
                    <label htmlFor="username" className="register-label">Username:</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className="register-input"
                        required
                    />
                </div>
                <div className="register-form-group">
                    <label htmlFor="email" className="register-label">Email:</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="register-input"
                        required
                    />
                </div>
                <div className="register-form-group">
                    <label htmlFor="password" className="register-label">Password:</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="register-input"
                        required
                    />
                </div>
                <div className="register-form-group">
                    <label htmlFor="confirmPassword" className="register-label">Confirm Password:</label>
                    <input
                        type="password"
                        id="confirmPassword"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        className="register-input"
                        required
                    />
                </div>

                <div className="register-form-group">
                    <label className="register-label">Are you a:</label>
                    <div className="register-radio-group">
                        <label className="register-radio-label">
                            <input
                                type="radio"
                                name="userType"
                                value="patient"
                                checked={userType === 'patient'}
                                onChange={() => setUserType('patient')}
                                className="register-radio-input"
                            /> Patient
                        </label>
                        <label className="register-radio-label">
                            <input
                                type="radio"
                                name="userType"
                                value="practitioner"
                                checked={userType === 'practitioner'}
                                onChange={() => setUserType('practitioner')}
                                className="register-radio-input"
                            /> Practitioner
                        </label>
                    </div>
                </div>

                {error && <p className="register-error">{error}</p>}
                {success && <p className="register-success">{success}</p>}
                <button type="submit" className="register-button">Register</button>
            </form>
            <p className="register-switch-link">
                Already have an account? <Link to="/login" className="register-link">Login here</Link>
            </p>
        </div>
    );
};

export default RegisterPage;