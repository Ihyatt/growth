import React from 'react';
import { useNavigate } from 'react-router-dom';
import useAuthStore from '../stores/authStore';

function Dashboard() {
  const { logout, permission } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div>
      <h1>Dashboard ({permission})</h1>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}

export default Dashboard;