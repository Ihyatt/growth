import { BrowserRouter as Router, Routes, Route, Navigate, useParams } from 'react-router-dom';


import useAuthStore from './stores/auth';

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
import PractitionerViewForm from './pages/Practitioner/ViewForm';
import PractitionerEditForm from './pages/Practitioner/EditForm';
import PractitionerViewPatientsForms from './pages/Practitioner/ViewPatientsForms';
import PractitionerViewPatientForm from './pages/Practitioner/ViewPatientForm';
import PractitionerViewPatients from './pages/Practitioner/ViewPatients';
import PractitionerViewPatient from './pages/Practitioner/ViewPatient';
import PractitionerViewReports from './Pages/Practitioner/ViewPatientsReports';
import PractitionerViewReport from './Pages/Practitioner/ViewPatientsReport';
import ProtectedLayout from './components/ProtectedLayout';


function App() {
  const { username } = useAuthStore();



  return (
    <Router>
      <Routes>
        {/* Auth */}
        <Route
          path="/login"
          element={<Login/>}
        />
        <Route
          path="/register"
          element={<Register/>}
        />

               {/* Admin */}
              <Route path="/admin" element={ <ProtectedLayout currPermission={'ADMIN'}/>}>
               <Route path="users" element={<AdminViewAllUsers />} />
               <Route path=":id" element={<AdminViewUser />} />
              </Route>

              {/* Patient */}
              <Route path="/patients/:username" element={ <ProtectedLayout currPermission={'PATIENT'}/> }>
                <Route path="forms" element={<PatientFormsToComplete />} >
                  <Route path="list" element={<PatientFormToComplete />} />
                  <Route path=":id" element={<PatientFormToComplete />} />
                </Route>
                <Route path="reports" element={<PatientReports />} >
                  <Route path="list" element={<PatientFormToComplete />} />
                  <Route path=":id" element={<PatientReport />} />
                </Route>
              </Route>
    
             {/* Practitioner */}
                <Route path='/practitioners/:username' element={<ProtectedLayout currPermission={'PRACTITIONER'}/>}>
                  <Route path="forms" element={<PractitionerViewForms />} >
                    <Route path="add" element={<PractitionerCreateForm />}/>
                    <Route path="list" element={<PractitionerViewForm/>}/>
                    <Route path=":id" element={<PractitionerViewForm/>}>
                      <Route path="edit" element={<PractitionerEditForm />} />
                      <Route path="assign" element={<PractitionerEditForm />} />
                    </Route>
                  </Route>

                  <Route path="patients" element={<PractitionerViewPatients />}>
                    <Route path=":id" element={<PractitionerViewPatient />}>
                      <Route path="comment" element={<PractitionerEditForm />} />
                    </Route>
                  </Route> 

                  <Route path="reports" element={<PractitionerViewReports />}>
                    <Route path="list" element={<PractitionerViewReport />} />
                    <Route path=":id" element={<PractitionerViewReport />} />
                  </Route>
               </Route> 
     
             {/* Default Redirect */}
             <Route path="/" element={<ProtectedLayout currPermission = {''}/>} />
      </Routes>
    </Router>
  );
}

export default App;