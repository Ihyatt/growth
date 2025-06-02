// src/components/Dashboard/Dashboard.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css'; // Import the component's specific CSS

const Dashboard = ({ onLogout }) => {
    const navigate = useNavigate();

    const handleLogoutClick = () => {
        onLogout(); // Call the onLogout function passed from App.jsx
        navigate('/login'); // Redirect to login page
    };
    
    return (
        <div className="dashboard-container">
            <h2 className="dashboard-heading">Welcome to the Dashboard!</h2>
            <p className="dashboard-paragraph">You are logged in.</p>
            <button onClick={handleLogoutClick} className="dashboard-logout-button">Logout</button>
        </div>
    );
};

export default Dashboard;