import React from 'react';
import { useNavigate } from 'react-router-dom';

const Dashboard = ({ onLogout }) => {
    const navigate = useNavigate();

    const handleLogoutClick = () => {
        onLogout(); // Call the onLogout function passed from App.jsx
        navigate('/login'); // Redirect to login page
    };

    return (
        <div style={styles.container}>
            <h2 style={styles.heading}>Welcome to the Dashboard!</h2>
            <p style={styles.paragraph}>You are logged in.</p>
            <button onClick={handleLogoutClick} style={styles.button}>Logout</button>
        </div>
    );
};

// Basic inline styles
const styles = {
    container: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        backgroundColor: '#e6f7ff',
        fontFamily: 'Arial, sans-serif',
        textAlign: 'center',
        padding: '20px',
    },
    heading: {
        color: '#2c3e50',
        marginBottom: '15px',
    },
    paragraph: {
        color: '#34495e',
        fontSize: '18px',
        marginBottom: '30px',
    },
    button: {
        padding: '10px 20px',
        backgroundColor: '#dc3545',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '16px',
        transition: 'background-color 0.3s ease',
    },
};

export default Dashboard;