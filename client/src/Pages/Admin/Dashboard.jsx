import { Link, Outlet } from 'react-router-dom';


export function Admin() {
    return (
      <div>
        <h1>Practitioner Dashboard</h1>
        <nav>
          <Link to="users">View Users</Link>
          <Link to="users/2">View User 2</Link>

        </nav>
        <Outlet />
      </div>
    );
  }

export default Admin;


