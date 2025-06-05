import React from 'react';


import { Link, Outlet ,useNavigate} from 'react-router-dom';
import useAuthStore from '../../stores/auth';


export function Admin() {
  const { logout, permission, isAuthenticated } = useAuthStore();
  const navigate = useNavigate();
  const handleLogout = () => {
    logout();
    navigate('/login');
  };

    return (
      <div>
        <h1>Admin Dashboard</h1>
        <nav>
          <Link to="users">View Users</Link>
          <Link to="users/2">View User 2</Link>

        </nav>
        <Outlet />
        <div>
        <h1>Dashboard ({permission})</h1>
        <button onClick={handleLogout}>Logout</button>

      </div>
    
      </div>
    );
  }

export default Admin;


