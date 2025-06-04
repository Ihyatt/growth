import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import useAuthStore from './stores/auth';
import Dashboard from './pages/Dashboard/Dashboard';
import Login from './pages/Login';
import Register from './pages/Register';

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
        <Route path="/patients/:patient_username" element={<Blogs />}>
          <Route path="forms" element={<Blogs />}>
            <Route path=":form_id" element={<Blogs />} />
          </Route>
          <Route path="reports" element={<Blogs />}>
            <Route path=":report_id" element={<Blogs />} />
          </Route>
        </Route>

        {/* Practitioner Routes */}
        <Route path="/practitioners/:practitioner_username" element={<Blogs />}>
          <Route path="forms" element={<Blogs />}>
            <Route path=":form_id" element={<Blogs />} />
          </Route>
          <Route path="reports" element={<Blogs />}>
            <Route path=":report_id" element={<Blogs />} />
          </Route>
          <Route path="patients" element={<Blogs />}>
            <Route path=":patient_username" element={<Blogs />} />
          </Route>
        </Route>

        {/* Admin Routes */}
        <Route path="/admins/:admin_id" element={<Blogs />}>
          <Route path="users" element={<Blogs />}>
            <Route path=":user_name" element={<Blogs />} />
          </Route>
          <Route path="reports" element={<Blogs />}>
            <Route path=":report_id" element={<Blogs />} />
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