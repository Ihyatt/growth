import { Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';

// Layout Components
import DashboardLayout from './layouts/DashboardLayout';
import AdminLayout from './layouts/AdminLayout';
import PractitionerLayout from './layouts/PractitionerLayout';
import PatientLayout from './layouts/PatientLayout';

// Page Components
import Login from './pages/Login';

import AdminViewAllUsers from './pages/Admin/ViewAllUsers';
import AdminViewUser from './pages/Admin/ViewUser';

import PatientFormsToComplete from './pages/Patient/FormsToComplete';
import PatientFormToComplete from './pages/Patient/FormToComplete';
import PatientReports from './pages/Patient/Reports';
import PatientReport from './pages/Patient/Report';

import PractitionerCreateForm from './pages/Practitioner/CreateForm';
import PractitionerViewForms from './pages/Practitioner/ViewForms';
import PractitionerEditForm from './Pages/Practitioner/EditForm';
import PractitionerViewPatientsForms from './pages/Practitioner/ViewPatientsForms';
import PractitionerViewPatientForm from './pages/Practitioner/ViewPatientForm';
import PractitionerViewPatients from './pages/Practitioner/ViewPatients';
import PractitionerViewPatient from './pages/Practitioner/ViewPatient';
import PractitionerViewReports from './Pages/Practitioner/ViewReports';
import PractitionerViewReport from './pages/Practitioner/ViewHistoricReports/ViewReport';


function AppRoutes() {
  const { user, isLoading } = useAuth();

  if (isLoading) return <div>Loading...</div>;

  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/login" element={<Login />} />

      {/* Protected Routes */}
      <Route element={<ProtectedRoute user={user} />}>
        <Route element={<DashboardLayout />}>
          {/* Default redirect based on role */}
          <Route index element={<Navigate to={getDefaultRoute(user?.role)} replace />} />

          {/* Admin Routes */}
          <Route element={<RoleRoute allowedRoles={['admin']} user={user} />}>
            <Route element={<AdminLayout />}>
              <Route path="admin/users" element={<AdminViewAllUsers />} />
              <Route path="admin/users/:userId" element={<AdminViewUser />} />
            </Route>
          </Route>

          {/* Patient Routes */}
          <Route element={<RoleRoute allowedRoles={['patient']} user={user} />}>
            <Route element={<PatientLayout />}>
              <Route path="patient/forms" element={<PatientFormsToComplete />} />
              <Route path="patient/forms/:formId" element={<PatientFormToComplete />} />
              <Route path="patient/reports" element={<PatientReports />} />
              <Route path="patient/reports/:reportId" element={<PatientReport />} />
            </Route>
          </Route>

          {/* Practitioner Routes */}
          <Route element={<RoleRoute allowedRoles={['practitioner']} user={user} />}>
            <Route element={<PractitionerLayout />}>
              <Route path="practitioner/create-form" element={<PractitionerCreateForm />} />
              <Route path="practitioner/forms" element={<PractitionerViewForms />} />
              <Route path="practitioner/forms/:formId/edit" element={<PractitionerEditForm />} />
              
              <Route path="practitioner/patient-forms" element={<PractitionerViewPatientsForms />}>
                <Route path=":formId" element={<PractitionerViewPatientForm />} />
              </Route>
              
              <Route path="practitioner/patients" element={<PractitionerViewPatients />} />
              <Route path="practitioner/patients/:patientId" element={<PractitionerViewPatient />} />
              
              <Route path="practitioner/reports" element={<PractitionerViewReports />} />
              <Route path="practitioner/reports/:reportId" element={<PractitionerViewReport />} />
            </Route>
          </Route>
        </Route>
      </Route>

      {/* Fallback Routes */}
      <Route path="/unauthorized" element={<div>You don't have permission</div>} />
      <Route path="*" element={<div>Page not found</div>} />
    </Routes>
  );
}

// Auth Protection Components
function ProtectedRoute({ user, children }) {
  return user ? <Outlet /> : <Navigate to="/login" replace />;
}

function RoleRoute({ allowedRoles, user, children }) {
  return allowedRoles.includes(user?.role) ? <Outlet /> : <Navigate to="/unauthorized" replace />;
}

function getDefaultRoute(role) {
  switch(role) {
    case 'admin': return '/admin/users';
    case 'practitioner': return '/practitioner/patient-forms';
    case 'patient': return '/patient/forms';
    default: return '/login';
  }
}

export default AppRoutes;