import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

// Layouts
import { Patient } from './Pages/Patient/Dashboard';
import { Practitioner } from './Pages/Practitioner/Dashboard';
import { Admin } from './Pages/Admin/Dashboard';

// Auth Pages
import Login from './pages/Login';
import Register from './pages/Register';

// Admin Pages
import AdminViewAllUsers from './pages/Admin/ViewAllUsers';
import AdminViewUser from './pages/Admin/ViewUser';

// Patient Pages
import PatientFormsToComplete from './pages/Patient/FormsToComplete';
import PatientFormToComplete from './pages/Patient/FormToComplete';
import PatientReports from './pages/Patient/Reports';
import PatientReport from './pages/Patient/Report';

// Practitioner Pages
import PractitionerCreateForm from './pages/Practitioner/CreateForm';
import PractitionerViewForms from './pages/Practitioner/ViewForms';
import PractitionerEditForm from './pages/Practitioner/EditForm';
import PractitionerViewPatientsForms from './pages/Practitioner/ViewPatientsForms';
import PractitionerViewPatientForm from './pages/Practitioner/ViewPatientForm';
import PractitionerViewPatients from './pages/Practitioner/ViewPatients';
import PractitionerViewPatient from './pages/Practitioner/ViewPatient';
import PractitionerViewReports from './Pages/Practitioner/ViewPatientsReports';
import PractitionerViewReport from './Pages/Practitioner/ViewPatientsReport';


function App() {
  const isAuthenticated = true; // Replace with actual auth logic

  return (
    <Router>
      <Routes>
        {/* Auth */}
        <Route
          path="/login"
          element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <Login />}
        />
        <Route
          path="/register"
          element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <Register />}
        />

        {/* Admin */}
        <Route path="/admin" element={<Admin />}>
          <Route path="users" element={<AdminViewAllUsers />} />
          <Route path="users/:userId" element={<AdminViewUser />} />
        </Route>

        {/* Patient */}
        <Route path="/patients/:patientUsername" element={<Patient />}>
          <Route path="forms" element={<PatientFormsToComplete />} />
          <Route path="forms/:formId" element={<PatientFormToComplete />} />
          <Route path="reports" element={<PatientReports />} />
          <Route path="reports/:reportId" element={<PatientReport />} />
        </Route>

        {/* Practitioner */}
        <Route path="/practitioners/:practitionerUsername" element={<Practitioner />}>
          <Route path="create-form" element={<PractitionerCreateForm />} />
          <Route path="forms" element={<PractitionerViewForms />} />
          <Route path="forms/:formId/edit" element={<PractitionerEditForm />} />
          <Route path="patients/forms" element={<PractitionerViewPatientsForms />} />
          <Route path="patients/forms/:formId" element={<PractitionerViewPatientForm />} />
          <Route path="patients" element={<PractitionerViewPatients />} />
          <Route path="patients/:patientId" element={<PractitionerViewPatient />} />
          <Route path="reports" element={<PractitionerViewReports />} />
          <Route path="reports/:reportId" element={<PractitionerViewReport />} />
        </Route>

        {/* Default Redirect */}
        <Route path="/" element={<Navigate to={isAuthenticated ? "/practitioner" : "/login"} replace />} />
      </Routes>
    </Router>
  );
}

export default App;