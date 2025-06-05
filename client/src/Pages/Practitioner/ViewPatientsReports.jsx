import { Link, Outlet } from 'react-router-dom';


export function PractitionerViewReports() {
    return (
      <div>
        <h2>Reports</h2>
        <Link to="/practitioner/reports/2">View Report 303</Link>
      </div>
    );
  }

export default PractitionerViewReports;