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
                  <Link to="forms">Forms To Complete</Link>
                  <Link to="reports">Past Reports</Link>
                  <Link to="patients">Past Reports</Link>
                </nav>
        <div>
        <h1>Dashboard ({permission})</h1>
        <button onClick={handleLogout}>Logout</button>

      </div>
      <Outlet />
      </div>
    );
  }

export default Practitioner;
  
