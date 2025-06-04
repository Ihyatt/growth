import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import useAuthStore from '../stores/auth';
import { userLogin } from '../services/auth';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const { login } = useAuthStore();


  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(username, password)
    try {
      const response = await userLogin(username, password);
      login(response.data.jwtToken, response.data.permission);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed');
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
      Don&apos;t have an account? <Link to="/register" className="login-link">Register here</Link>
    </p>
  </div>
  );
}

export default Login;