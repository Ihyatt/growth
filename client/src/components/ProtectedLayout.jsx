import { Navigate,Outlet } from 'react-router-dom';

import useAuthStore from '../stores/auth';
import { Patient } from '../Pages/Patient/Dashboard';
import { Practitioner } from '../Pages/Practitioner/Dashboard';
import { Admin } from '../Pages/Admin/Dashboard';
import Login from '../pages/Login';


function ProtectedLayout() {
    const { isAuthenticated, permission, userName } = useAuthStore();
  
    console.log('herrre')
    if (!isAuthenticated) {
      return <Navigate to="/login" replace />;
    }
  
    const isPatient = permission == 'PATIENT'
    const isPractitioner = permission == 'PRACTITIONER'
    const isAdmin =  permission == 'ADMIN'

    if (isPatient) {
      return <Navigate to={`/patients/${userName}`} replace />;
    }

    if (isPractitioner) {
      return <Navigate to={`/practitioners/${userName}`} replace />;
    }

    if (isAdmin) {
      return <Navigate to='/admin' replace />;
    }
    return (
      <div>
      {!isAuthenticated && <Login/>}
      {isPatient && <Patient/>}
      {isPractitioner && <Practitioner/>}
      {isAdmin && <Admin/>}

      </div>
    );

  }

export default ProtectedLayout;