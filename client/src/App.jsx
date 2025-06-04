import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import useAuthStore from './stores/auth';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Register from './pages/Register';

function App() {
  const { isAuthenticated, permission } = useAuthStore();

  return (
    <Router>
      <Routes>
        <Route
          path="/login"
          element={
            isAuthenticated
              ? <Navigate to="/dashboard" replace />
              : <Login />
          }
        />
        <Route
          path="/register"
          element={
            isAuthenticated
              ? <Navigate to="/dashboard" replace />
              : <Register />
          }
        />
        <Route
          path="/dashboard"
          element={
            isAuthenticated
              ? <Dashboard />
              : <Navigate to="/login" replace />
          }
        />
        <Route
          path="/"
          element={
            <Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />
          }
        />
      </Routes>
    </Router>
  );
}

export default App;










// import React, { useState, useEffect } from 'react';
// import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

// import Dashboard from './pages/Dashboard';
// import Login from './pages/Login';
// import Register from './pages/Register';


// const AUTH_KEY = 'isAuthenticated';
// const TOKEN_KEY = 'jwtToken';
// const PERMISSION = 'permission';

// function App() {
//   const [isAuthenticated, setIsAuthenticated] = useState(() => {
//     return localStorage.getItem(AUTH_KEY) === 'true';
//   });

//   const [userPermission, setUserPermission] = useState(() => {
//     return localStorage.getItem(PERMISSION) || null;
//   });

//   useEffect(() => {
//     localStorage.setItem(AUTH_KEY, isAuthenticated);
//   }, [isAuthenticated]);


//   useEffect(() => {
//     localStorage.setItem(PERMISSION, userPermission);
//   }, [userPermission]);


//   const handleLogin = (jwtToken, permission) => {
//     setIsAuthenticated(true);
//     setUserPermission(permission)
//     localStorage.setItem(TOKEN_KEY, jwtToken);
//   };

//   const handleLogout = () => {
//     setIsAuthenticated(false);
//     localStorage.removeItem(AUTH_KEY);
//     localStorage.removeItem(TOKEN_KEY);
//     localStorage.removeItem(PERMISSION);
//   };
//   return (
//     <Router>
//       <Routes>
//         <Route
//           path="/login"
//           element={
//             isAuthenticated
//               ? <Navigate to="/dashboard" replace />
//               : <Login onLogin={handleLogin} />
//           }
//         />
//         <Route
//           path="/register"
//           element={
//             isAuthenticated
//               ? <Navigate to="/dashboard" replace />
//               : <Register />
//           }
//         />
//         <Route
//           path="/dashboard"
//           element={
//             isAuthenticated
//               ? <Dashboard onLogout={handleLogout} />
//               : <Navigate to="/login" replace />
//           }
//         />
//         <Route
//           path="/"
//           element={
//             isAuthenticated
//               ? <Navigate to="/dashboard" replace />
//               : <Navigate to="/login" replace />
//           }
//         />
//       </Routes>
//     </Router>
//   );
// }

// export default App;