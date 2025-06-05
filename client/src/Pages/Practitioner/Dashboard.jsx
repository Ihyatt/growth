// Practitioner Layout and Pages
import { Link, Outlet } from 'react-router-dom';


export function Practitioner() {
    return (
      <div>
        <h1>Practitioner Dashboard</h1>
        <nav>
          <Link to="create-form">Create Form</Link>
          <Link to="forms">View Forms</Link>
          <Link to="patients">View Patients</Link>
          <Link to="reports">View Reports</Link>
        </nav>
        <Outlet />
      </div>
    );
  }

export default Practitioner;
  