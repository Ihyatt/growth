
import React, { useState, useRef } from 'react';
import { Link, Routes, Route } from 'react-router-dom';
import AddForm from './Pages/AddForms/Form';
import ViewForms from './Pages/ViewForms/Forms';
import ViewPatients from './Pages/ViewPatients/Patients';
import ViewReports from './Pages/ViewReports/Reports';

function Practitioner() {

    return (
        <div className="dashboard">
            <nav>
                <div>
                    <Link to="add-form">Add Form</Link>
                </div>
                <div>
                    <Link to="view-forms">View Forms</Link>
                </div>
                <div>
                    <Link to="view-patients">View Patients</Link>
                </div>
                <div>
                    <Link to="view-reports">View Reports</Link>
                </div>
            </nav>
        <main>
          <Routes>
            <Route path="add-form" element={<AddForm />} />
            <Route path="view-forms" element={<ViewForms />} />
            <Route path="view-patients" element={<ViewPatients />} />
            <Route path="view-reports" element={<ViewReports />} />
          </Routes>
        </main>
      </div>
    );
}

export default Practitioner;