// Patient Layout and Pages
export function Patient() {
    return (
      <div>
        <h1>Patient Dashboard</h1>
        <nav>
          <Link to="forms">Forms To Complete</Link>
          <Link to="reports">Past Reports</Link>
        </nav>
        <Outlet />
      </div>
    );
  }

export default Patient;