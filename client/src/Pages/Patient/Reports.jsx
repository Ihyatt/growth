import { Link, Outlet } from 'react-router-dom';


export function PatientReports() {
    return (
      <div>
        <h2>Past Reports</h2>
        <Link to="/reports/2">View Report 456</Link>
      </div>
    );
  }

export default PatientReports;