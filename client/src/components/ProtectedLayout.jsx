import { Navigate,Outlet } from 'react-router-dom';
import PropTypes from 'prop-types'; // Import PropTypes

import useAuthStore from '../stores/auth';
import { Patient } from '../Pages/Patient/Dashboard';
import { Practitioner } from '../Pages/Practitioner/Dashboard';
import { Admin } from '../Pages/Admin/Dashboard';
import Login from '../pages/Login';


function ProtectedLayout({currPermission}) {

  
    const { isAuthenticated, permission, userName } = useAuthStore();
  
    console.log(currPermission)
    if (!isAuthenticated) {
      return <Navigate to="/login" replace />;
    }
    console.log(userName)
    const isPatient = permission == 'PATIENT'
    const isPractitioner = permission == 'PRACTITIONER'
    const isAdmin =  permission == 'ADMIN'

    if (isPatient && permission != currPermission) {
      return <Navigate to={`/patients/${userName}`} replace />;
    }
    
    if (isPractitioner && permission != currPermission) {
      console.log(`/practitioners/${userName}`)
      return <Navigate to={`/practitioners/${userName}`} replace />;
    }

    if (isAdmin && permission != currPermission) {
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

ProtectedLayout.propTypes = {
  currPermission: PropTypes.string.isRequired, // Expecting a string like 'ADMIN', 'PATIENT', 'PRACTITIONER'
                                              // and it's required for this component
};
export default ProtectedLayout;