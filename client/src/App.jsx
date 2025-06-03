import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './components/LoginPage/LoginPage';
import RegisterPage from './components/RegisterPage/RegisterPage';
import Dashboard from './components/Dashboard/Dashboard';
import AdminDashboardPage from './pages/AdminDashboardPage';
import { USER_ROLES } from './constants/enums';

const AUTH_KEY = 'isAuthenticated';
const TOKEN_KEY = 'jwtToken';
const PERMISSION = 'permission';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return localStorage.getItem(AUTH_KEY) === 'true';
  });

  const [userPermission, setUserPermission] = useState(() => {
    return localStorage.getItem(PERMISSION) || null;
  });

  useEffect(() => {
    localStorage.setItem(AUTH_KEY, isAuthenticated);
  }, [isAuthenticated]);


  useEffect(() => {
    localStorage.setItem(PERMISSION, userPermission);
  }, [userPermission]);


  const handleLogin = (jwtToken, permission) => {
    setIsAuthenticated(true);
    setUserPermission(permission)
    localStorage.setItem(TOKEN_KEY, jwtToken);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    localStorage.removeItem(AUTH_KEY);
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(PERMISSION);
  };
  console.log(isAuthenticated, userPermission, USER_ROLES)
  return (
    <Router>
      <Routes>
        <Route
          path="/admin"
          element={
            isAuthenticated && userPermission === USER_ROLES.ADMIN
              ? <AdminDashboardPage onLogout={handleLogout} />
              : <Navigate to="/dashboard" replace />
            }
        />
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