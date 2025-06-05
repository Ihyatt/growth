import { Link, Outlet } from 'react-router-dom';


export function PatientFormsToComplete() {
    return (
      <div>
        <h2>Forms To Complete</h2>
        <Link to="/patients/forms/2">Go to Form 123</Link>
      </div>
    );
  }

export default PatientFormsToComplete;