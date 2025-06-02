// src/App.jsx
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './components/LoginPage/LoginPage';
import RegisterPage from './components/RegisterPage/RegisterPage';
import Dashboard from './components/Dashboard/Dashboard';

function App() {
    // Initialize isAuthenticated from localStorage, or false if not found
    const [isAuthenticated, setIsAuthenticated] = useState(() => {
        const storedAuth = localStorage.getItem('isAuthenticated');
        return storedAuth === 'true'; // localStorage stores strings, convert to boolean
    });

    // Effect to update localStorage whenever isAuthenticated changes
    useEffect(() => {
        localStorage.setItem('isAuthenticated', isAuthenticated);
    }, [isAuthenticated]);
   
    const handleLogin = (jwtToken, permission) => {
        setIsAuthenticated(true);
        localStorage.setItem("jwtToken", jwtToken);
        localStorage.setItem("permission", permission);
    };


    const handleLogout = () => {
        setIsAuthenticated(false);
        // Clear any stored tokens or user data
        localStorage.removeItem('isAuthenticated');
        localStorage.removeItem('jwtToken'); // If you were storing a token
    };

    return (
        <Router>
            <Routes>
                {/* Public Routes */}
                <Route
                    path="/login"
                    element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <LoginPage onLogin={handleLogin} />}
                />
                <Route
                    path="/register"
                    element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <RegisterPage />}
                />

                {/* Protected Route */}
                <Route
                    path="/dashboard"
                    element={isAuthenticated ? <Dashboard onLogout={handleLogout} /> : <Navigate to="/login" replace />}
                />

                {/* Default Route: Redirect to dashboard if authenticated, otherwise to login */}
                <Route
                    path="/"
                    element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />}
                />
            </Routes>
        </Router>
    );
}

export default App;