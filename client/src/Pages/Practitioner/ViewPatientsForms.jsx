import { Link, Outlet } from 'react-router-dom';


export function PractitionerViewPatientsForms() {
    return (
      <div>
        <h2>Patients' Forms</h2>
        <Link to="/practitioner/patients/forms/2">View Form 101</Link>
      </div>
    );
  }


export default PractitionerViewPatientsForms;
  