import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './RegisterPage.css';

const API_BASE_URL = import.meta.env.VITE_API_URL;

const RegisterPage = ({ onRegister }) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [userType, setUserType] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!username || !email || !password || !confirmPassword || !userType) {
      setError('Please fill in all fields and select your user type.');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    try {
      const body = { username, email, password, userType };

      const response = await fetch(`${API_BASE_URL}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data?.message || 'Registration failed.');
      }

      setSuccess('Registration successful! Redirecting to login...');
      setTimeout(() => {
        onRegister();
        navigate('/login');
      }, 1500);
    } catch (err) {
      setError(err.message || 'An unexpected error occurred during registration.');
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