import { BrowserRouter as Router, Routes, Route, Navigate, useParams } from 'react-router-dom';


import useAuthStore from './stores/auth';

// Auth Pages
import Login from './pages/Login';
import Register from './pages/Register';


// Patient Pages
import PatientForms from './pages/Patient/Forms';
import PatientReports from './pages/Patient/Reports';

// Practitioner Pages
import PractitionerForms from './pages/Practitioner/Forms';
import PractitionerPatients from './pages/Practitioner/Patients';
import PractitionerReports from './pages/Practitioner/Patients';

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
              <Route path="/admin" element={ <ProtectedLayout currPermission={'ADMIN'}/>} />

              {/* Patient */}
              <Route path="/patients/:username" element={ <ProtectedLayout currPermission={'PATIENT'}/> }>
                <Route path="forms" element={<PatientForms />} />
                <Route path="reports" element={<PatientReports />} />
              </Route>
    
             {/* Practitioner */}
                <Route path='/practitioners/:username' element={<ProtectedLayout currPermission={'PRACTITIONER'}/>}>
                  <Route path="forms" element={<PractitionerForms />} />
                  <Route path="patients" element={<PractitionerPatients />}/>
                  <Route path="reports" element={<PractitionerReports />}>
                  </Route>
               </Route> 
     
             {/* Default Redirect */}
             <Route path="/" element={<ProtectedLayout currPermission = {''}/>} />
      </Routes>
    </Router>
  );
}

export default App;