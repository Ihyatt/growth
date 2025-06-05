// Practitioner Layout and Pages
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
  