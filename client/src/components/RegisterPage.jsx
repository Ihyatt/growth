// src/components/RegisterPage.jsx
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

const RegisterPage = ({ onRegister }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [userType, setUserType] = useState(''); // New state for user type
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
            console.log(API_BASE_URL)
            const response = await fetch(`${API_BASE_URL}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.message || 'Authentication failed');

            setSuccess('Registration successful! Redirecting to login...');

            setTimeout(() => {
                onRegister();
                navigate('/login');
            }, 1500); // Redirect after 1.5 seconds
            
    } catch (error) {
        setError( error.message);

      }
        } else {
            setError('Please fill in all fields and select your user type.');
        }
    };

    return (
        <div style={styles.container}>
            <h2 style={styles.heading}>Register</h2>
            <form onSubmit={handleSubmit} style={styles.form}>
                <div style={styles.formGroup}>
                    <label htmlFor="username" style={styles.label}>Username:</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        style={styles.input}
                        required
                    />
                </div>
                <div style={styles.formGroup}>
                <label htmlFor="email" style={styles.label}>Email:</label>
                <input
                    type="email"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    style={styles.input}
                    required
                />
            </div>
                <div style={styles.formGroup}>
                    <label htmlFor="password" style={styles.label}>Password:</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        style={styles.input}
                        required
                    />
                </div>
                <div style={styles.formGroup}>
                    <label htmlFor="confirmPassword" style={styles.label}>Confirm Password:</label>
                    <input
                        type="password"
                        id="confirmPassword"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        style={styles.input}
                        required
                    />
                </div>

                {/* NEW: User Type Selection */}
                <div style={styles.formGroup}>
                    <label style={styles.label}>Are you a:</label>
                    <div style={styles.radioGroup}>
                        <label style={styles.radioLabel}>
                            <input
                                type="radio"
                                name="userType"
                                value="patient"
                                checked={userType === 'patient'}
                                onChange={() => setUserType('patient')}
                                style={styles.radioInput}
                            /> Patient
                        </label>
                        <label style={styles.radioLabel}>
                            <input
                                type="radio"
                                name="userType"
                                value="practitioner"
                                checked={userType === 'practitioner'}
                                onChange={() => setUserType('practitioner')}
                                style={styles.radioInput}
                            /> Practitioner
                        </label>
                    </div>
                </div>

                {error && <p style={styles.error}>{error}</p>}
                {success && <p style={styles.success}>{success}</p>}
                <button type="submit" style={styles.button}>Register</button>
            </form>
            <p style={styles.switchLink}>
                Already have an account? <Link to="/login" style={styles.link}>Login here</Link>
            </p>
        </div>
    );
};

// Basic inline styles (reusing from LoginPage, move to a CSS file for production)
const styles = {
    container: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        backgroundColor: '#f0f2f5',
        fontFamily: 'Arial, sans-serif',
        padding: '20px',
    },
    heading: {
        color: '#333',
        marginBottom: '20px',
    },
    form: {
        backgroundColor: '#fff',
        padding: '30px',
        borderRadius: '8px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
        width: '100%',
        maxWidth: '350px',
        boxSizing: 'border-box',
    },
    formGroup: {
        marginBottom: '15px',
    },
    label: {
        display: 'block',
        marginBottom: '5px',
        color: '#555',
        fontWeight: 'bold',
    },
    input: {
        width: '100%',
        padding: '10px',
        border: '1px solid #ddd',
        borderRadius: '4px',
        boxSizing: 'border-box',
    },
    radioGroup: { // New style for radio buttons
        display: 'flex',
        gap: '20px',
        marginTop: '10px',
    },
    radioLabel: { // New style for radio button labels
        display: 'flex',
        alignItems: 'center',
        cursor: 'pointer',
    },
    radioInput: { // New style for radio button input
        marginRight: '8px',
        transform: 'scale(1.2)', // Slightly enlarge for better clickability
    },
    error: {
        color: 'red',
        marginBottom: '10px',
        textAlign: 'center',
    },
    success: {
        color: 'green',
        marginBottom: '10px',
        textAlign: 'center',
    },
    button: {
        width: '100%',
        padding: '10px',
        backgroundColor: '#28a745', // Green for register
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '16px',
        transition: 'background-color 0.3s ease',
    },
    switchLink: {
        marginTop: '20px',
        color: '#555',
    },
    link: {
        color: '#007bff',
        textDecoration: 'none',
        fontWeight: 'bold',
    },
};

export default RegisterPage;