import React, { useState } from 'react';

function AuthForm() {
  const [authState, setAuthState] = useState({
    email: '',
    password: '',
    name: '', // For registration
    error: null,
    loading: false,
    successMessage: null
  });

  const [isLogin, setIsLogin] = useState(true); // Toggle between login/register

  const API_BASE_URL = 'http://localhost:5000/api';

  const handleChange = (e) => {
    const { name, value } = e.target;
    setAuthState(prev => ({
      ...prev,
      [name]: value,
      error: null // Clear error when user types
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setAuthState(prev => ({ ...prev, loading: true, error: null }));

    try {
      const endpoint = isLogin ? '/login' : '/register';
      const body = isLogin 
        ? { email: authState.email, password: authState.password }
        : { name: authState.name, email: authState.email, password: authState.password };
      

      
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });


      const data = await response.json();

      console.log(data.message)

      if (!response.ok) {
        throw new Error(data.message || 'Authentication failed');
      }

      setAuthState(prev => ({
        ...prev,
        loading: false,
        successMessage: data.message,
        password: '' // Clear password after successful auth
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
    <div style={containerStyle}>
      <h1 style={headerStyle}>{isLogin ? 'Login' : 'Register'}</h1>
      
      <form onSubmit={handleSubmit} style={formStyle}>
        {!isLogin && (
          <div style={inputGroupStyle}>
            <label htmlFor="name" style={labelStyle}>Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={authState.name}
              onChange={handleChange}
              style={inputStyle}
              required
            />
          </div>
        )}

        <div style={inputGroupStyle}>
          <label htmlFor="email" style={labelStyle}>Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={authState.email}
            onChange={handleChange}
            style={inputStyle}
            required
          />
        </div>

        <div style={inputGroupStyle}>
          <label htmlFor="password" style={labelStyle}>Password</label>
          <input
            type="password"
            id="password"
            name="password"
            value={authState.password}
            onChange={handleChange}
            style={inputStyle}
            minLength="6"
            required
          />
        </div>

        <button 
          type="submit" 
          disabled={authState.loading}
          style={buttonStyle}
        >
          {authState.loading ? 'Processing...' : isLogin ? 'Login' : 'Register'}
        </button>

        <button 
          type="button"
          onClick={() => setIsLogin(!isLogin)}
          style={toggleButtonStyle}
        >
          {isLogin ? 'Need an account? Register' : 'Already have an account? Login'}
        </button>
      </form>

      {authState.error && (
        <div style={errorStyle}>
          {authState.error}
        </div>
      )}

      {authState.successMessage && (
        <div style={successStyle}>
          {authState.successMessage}
        </div>
      )}
    </div>
  );
}

// Styles
const containerStyle = {
  maxWidth: '400px',
  margin: '2rem auto',
  padding: '2rem',
  borderRadius: '8px',
  boxShadow: '0 0 10px rgba(0,0,0,0.1)'
};

const headerStyle = {
  textAlign: 'center',
  color: '#333',
  marginBottom: '1.5rem'
};

const formStyle = {
  display: 'flex',
  flexDirection: 'column',
  gap: '1rem'
};

const inputGroupStyle = {
  display: 'flex',
  flexDirection: 'column',
  gap: '0.5rem'
};

const labelStyle = {
  fontSize: '0.9rem',
  color: '#555'
};

const inputStyle = {
  padding: '0.8rem',
  border: '1px solid #ddd',
  borderRadius: '4px',
  fontSize: '1rem'
};

const buttonStyle = {
  padding: '0.8rem',
  backgroundColor: '#2196F3',
  color: 'white',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer',
  fontSize: '1rem',
  marginTop: '1rem',
  transition: 'background-color 0.3s',
  ':hover': {
    backgroundColor: '#0b7dda'
  }
};

const toggleButtonStyle = {
  ...buttonStyle,
  backgroundColor: 'transparent',
  color: '#2196F3',
  border: '1px solid #2196F3',
  marginTop: '0.5rem'
};

const errorStyle = {
  color: '#f44336',
  padding: '1rem',
  marginTop: '1rem',
  backgroundColor: '#ffebee',
  borderRadius: '4px'
};

const successStyle = {
  color: '#4CAF50',
  padding: '1rem',
  marginTop: '1rem',
  backgroundColor: '#e8f5e9',
  borderRadius: '4px'
};

export default AuthForm;