import { Navigate,Outlet } from 'react-router-dom';

import useAuthStore from '../stores/auth';
import { Patient } from '../Pages/Patient/Dashboard';
import { Practitioner } from '../Pages/Practitioner/Dashboard';
import { Admin } from '../Pages/Admin/Dashboard';

function ProtectedLayout() {
    const { isAuthenticated, permission } = useAuthStore();
  
    if (!isAuthenticated) {
      return <Navigate to="/login" replace />;
    }

    const isPatient = permission == 'PATIENT'
    const isPractitioner = permission == 'PRACTITIONER'
    const isAdmin =  permission == 'ADMIN'
  
    return (
      <>
        {isPatient && <Patient />}
        {isPractitioner && <Practitioner />}
        {isAdmin && <Admin />}
      </>
    );

  }

export default ProtectedLayout;