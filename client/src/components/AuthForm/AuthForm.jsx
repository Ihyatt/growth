import React, { useState } from 'react';
import './AuthForm.css';

function AuthForm() {
  const [authState, setAuthState] = useState({
    email: '',
    password: '',
    name: '',
    userType: 'patient',
    error: null,
    loading: false,
    successMessage: null
  });

  const [isLogin, setIsLogin] = useState(true);
  const API_BASE_URL = 'http://localhost:5000/api';

  const handleChange = (e) => {
    const { name, value } = e.target;
    setAuthState(prev => ({
      ...prev,
      [name]: value,
      error: null
    }));
  };

  const handleUserTypeChange = (type) => {
    setAuthState(prev => ({
      ...prev,
      userType: type,
      error: null
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setAuthState(prev => ({ ...prev, loading: true, error: null }));

    try {
      const endpoint = isLogin ? '/login' : '/register';
      const body = isLogin
        ? { email: authState.email, password: authState.password }
        : {
            name: authState.name,
            email: authState.email,
            password: authState.password,
            userType: authState.userType
          };

      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });

      const data = await response.json();

      if (!response.ok) throw new Error(data.message || 'Authentication failed');

      setAuthState(prev => ({
        ...prev,
        loading: false,
        successMessage: data.message,
        password: ''
      }));

    } catch (error) {
      setAuthState(prev => ({
        ...prev,
        loading: false,
        error: error.message
      }));
    }
  };

  return (
    <div className="container">
      <h1 className="header">{isLogin ? 'Login' : 'Register'}</h1>
      <form onSubmit={handleSubmit} className="form">
        {!isLogin && (
          <>
            <div className="input-group">
              <label htmlFor="name" className="label">Name</label>
              <input
                type="text"
                id="name"
                name="name"
                value={authState.name}
                onChange={handleChange}
                className="input"
                required
              />
            </div>

            <div className="input-group">
              <label className="label">I am a:</label>
              <div className="user-type-container">
                <button
                  type="button"
                  className={`user-type-button ${authState.userType === 'patient' ? 'selected' : ''}`}
                  onClick={() => handleUserTypeChange('patient')}
                >
                  Patient
                </button>
                <button
                  type="button"
                  className={`user-type-button ${authState.userType === 'practitioner' ? 'selected' : ''}`}
                  onClick={() => handleUserTypeChange('practitioner')}
                >
                  Medical Practitioner
                </button>
              </div>
            </div>
          </>
        )}

        <div className="input-group">
          <label htmlFor="email" className="label">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={authState.email}
            onChange={handleChange}
            className="input"
            required
          />
        </div>

        <div className="input-group">
          <label htmlFor="password" className="label">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            value={authState.password}
            onChange={handleChange}
            className="input"
            minLength="6"
            required
          />
        </div>

        <button type="submit" disabled={authState.loading} className="submit-button">
          {authState.loading ? 'Processing...' : isLogin ? 'Login' : 'Register'}
        </button>

        <button
          type="button"
          onClick={() => setIsLogin(!isLogin)}
          className="toggle-button"
        >
          {isLogin ? 'Need an account? Register' : 'Already have an account? Login'}
        </button>
      </form>

      {authState.error && <div className="error">{authState.error}</div>}
      {authState.successMessage && <div className="success">{authState.successMessage}</div>}
    </div>
  );
}

export default AuthForm;