// Practitioner Layout and Pages
import { Link, Outlet } from 'react-router-dom';


export function Practitioner() {
    return (
      <div>
        <h1>Practitioner Dashboard</h1>
        <nav>
          <Link to="create-form">Create Form</Link>
          <Link to="forms">View Forms</Link>
          <Link to="forms/2">View Forms</Link>
          <Link to="forms/2/edit">View Patients</Link>
          <Link to="patients">View Reports</Link>
          <Link to="patients/2">View Reports</Link>
          <Link to="patients/forms">View Reports</Link>
          <Link to="patients/forms/2">View Reports</Link>
          <Link to="patients/reports">View Reports</Link>
          <Link to="patients/reports/2">View Reports</Link>
        </nav>
        <Outlet />
      </div>
    );
  }

export default Practitioner;
  