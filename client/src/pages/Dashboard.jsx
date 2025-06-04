import React from 'react';
import { useNavigate } from 'react-router-dom';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import {USER_ROLES} from '../utils/constants'
import useAuthStore from '../stores/auth';
import Practitioner from '../components/Dashboard/Practitioner';
import Admin from '../components/Dashboard/Admin/Admin';
import Patient from '../components/Dashboard/Patient';


function Dashboard() {
  const { logout, permission, isAuthenticated } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  let content;

  if (isAuthenticated &&  permission === USER_ROLES.ADMIN) {
    content = <Admin />;
  } else if (isAuthenticated &&  permission=== USER_ROLES.PRACTITIONER) {
    content = <Practitioner />;
  } else {
    content = <Patient />;
  }

  console.log('hello i am isAuthenticad',isAuthenticated)

  return (
    <div>
      <h1>Dashboard ({permission})</h1>
      <button onClick={handleLogout}>Logout</button>
      {content}
    </div>
  );

}

export default Dashboard;