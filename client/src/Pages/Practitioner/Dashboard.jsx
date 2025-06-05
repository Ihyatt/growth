import React from 'react';


import { Link, Outlet ,useNavigate} from 'react-router-dom';
import useAuthStore from '../../stores/auth';


export function Practitioner() {


const { logout, permission, isAuthenticated } = useAuthStore();
const navigate = useNavigate();
const handleLogout = () => {
  logout();
  navigate('/login');
};
    return (
      <div>
        <h1>Practitioner Dashboard</h1>
        <nav>
          <Link to="create-form">Create Form</Link>
          <Link to="forms">View Forms</Link>
          <Link to="forms/2">View Forms</Link>
          <Link to="forms/2/edit">View Form</Link>
          <Link to="patients">View patients</Link>
          <Link to="patients/2">View patient</Link>
          <Link to="patients/forms">View patients forms</Link>
          <Link to="patients/forms/2">View patients form</Link>
          <Link to="reports">View Patients Reports</Link>
          <Link to="reports/2">View Patients Report</Link>
        </nav>
        <Outlet />
        <div>
        <h1>Dashboard ({permission})</h1>
        <button onClick={handleLogout}>Logout</button>

      </div>
      </div>
    );
  }

export default Practitioner;
  
