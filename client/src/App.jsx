import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './components/LoginPage/LoginPage';
import RegisterPage from './components/RegisterPage/RegisterPage';
import Dashboard from './components/Dashboard/Dashboard';

const AUTH_KEY = 'isAuthenticated';
const TOKEN_KEY = 'jwtToken';
const PERMISSION_KEY = 'permission';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return localStorage.getItem(AUTH_KEY) === 'true';
  });

  useEffect(() => {
    localStorage.setItem(AUTH_KEY, isAuthenticated);
  }, [isAuthenticated]);

  const handleLogin = (jwtToken, permission) => {
    setIsAuthenticated(true);
    localStorage.setItem(TOKEN_KEY, jwtToken);
    localStorage.setItem(PERMISSION_KEY, permission);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    localStorage.removeItem(AUTH_KEY);
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(PERMISSION_KEY);
  };

  return (
    <Router>
      <Routes>
        <Route
          path="/login"
          element={
            isAuthenticated
              ? <Navigate to="/dashboard" replace />
              : <LoginPage onLogin={handleLogin} />
          }
        />
        <Route
          path="/register"
          element={
            isAuthenticated
              ? <Navigate to="/dashboard" replace />
              : <RegisterPage />
          }
        />

        <Route
          path="/dashboard"
          element={
            isAuthenticated
              ? <Dashboard onLogout={handleLogout} />
              : <Navigate to="/login" replace />
          }
        />
        <Route
          path="/"
          element={
            isAuthenticated
              ? <Navigate to="/dashboard" replace />
              : <Navigate to="/login" replace />
          }
        />
      </Routes>
    </Router>
  );
}

export default App;