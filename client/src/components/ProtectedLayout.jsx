import React from 'react';
import { Navigate } from 'react-router-dom';

import useAuthStore from '../stores/auth';

function ProtectedLayout(Component) {
    const { isAuthenticated } = useAuthStore();
    
    const isAdmin = useAuthStore(state => state.isAdmin);
    const isPractitioner = useAuthStore(state => state.isAdmin);
    const isPatient = useAuthStore(state => state.isAdmin);
    
    return isAuthenticated ? (
      <Component />
    ) : (
      <Navigate to="/login" replace />
    );
  }

export default ProtectedLayout;