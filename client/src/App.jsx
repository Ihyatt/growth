import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import useAuthStore from './stores/auth';
import Dashboard from './pages/Dashboard/Dashboard';
import Login from './pages/Login';
import Register from './pages/Register';
import {ProtectedLayout} from './components/ProtectedLayout';
import {Patient} from './pages/Dashboard/Patient/Dashboard';
import {Practitioner} from './pages/Dashboard/Practitioner/Dashboard';
import {Admin} from './pages/Dashboard/Admin/Dashboard';
import { AdminViewUser } from './pages/Dashboard/Admin/Pages/User'

// client/src/App.jsx



function App() {
  const { isAuthenticated } = useAuthStore();


  return (
    <Router>
      <Routes>
        {/* Auth Routes */}
        <Route
          path="/login"
          element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <Login />}
        />
        <Route
          path="/register"
          element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <Register />}
        />

        {/* Main Dashboard */}
        <Route
          path="/dashboard"
          element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" replace />}
        />

        {/* Patient Routes */}
        <Route path="/patients/:patient_username" element={ProtectedLayout(Patient)}>
          <Route path="/forms" element={ProtectedLayout()}>
            <Route path="/:form_id" element={ProtectedLayout()} />
          </Route>
          <Route path="/reports" element={ProtectedLayout()}>
            <Route path="/:report_id" element={ProtectedLayout()} />
          </Route>
        </Route>

        {/* Practitioner Routes */}
        <Route path="/practitioners/:practitioner_username" element={ProtectedLayout(Practitioner)}>
          <Route path="/forms" element={ProtectedLayout()}>
            <Route path="/:form_id" element={ProtectedLayout()} />
          </Route>
          <Route path="/reports" element={ProtectedLayout()}>
            <Route path="/:report_id" element={ProtectedLayout()} />
          </Route>
          <Route path="/patients" element={ProtectedLayout()}>
            <Route path="/:patient_username" element={ProtectedLayout} />
          </Route>
        </Route>

        {/* Admin Routes */}
        <Route path="/admins/:admin_id" element={ProtectedLayout(Admin)}>
          <Route path="/users" element={ProtectedLayout()}>
            <Route path="/:user_name" element={ProtectedLayout(AdminViewUser)} />
          </Route>
          <Route path="/reports" element={ProtectedLayout()}>
            <Route path="/:report_id" element={ProtectedLayout()} />
          </Route>
        </Route>

        {/* Default Route */}
        <Route
          path="/"
          element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />}
        />
      </Routes>
    </Router>
  );
}

export default App;