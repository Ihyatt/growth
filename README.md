# Growth: Mental Wellness Companion

## Project Overview
Growth is a full-stack web application designed to connect patients with mental health practitioners, foster self-awareness through trend tracking, and streamline medication management. This platform aims to empower patients by visualizing their mental health journey, while providing practitioners with essential tools for patient oversight and engagement.

## Key Features
Growth provides a robust set of features tailored for various user roles:

### Patient Functionality
- **Form Completion**: Patients can complete various mental health forms (e.g., mood trackers, symptom checklists).
- **Trend Visualization**: Intuitive charts and graphs display personal mental health trends over time, based on submitted forms.
- **Medication Tracking**: Patients can log current medications, track practitioner-suggested trials (with dosage and reason), and set up refill reminders.
- **Weekly Reports**: Access to compiled weekly reports summarizing their form data and trends.

### Practitioner Functionality
- **Patient Management**: View and manage a list of assigned patients.
- **Form Review & Interaction**: Access individual completed patient forms, add comments for feedback, and "pin" important forms for quick reference.
- **Medication Suggestions**: Suggest new medications to patients, including dosage and rationale.
- **Weekly Reports**: View compiled weekly reports for their patients' form data and trends.

### Admin Functionality
- **Patient Approval**: Administer and approve new patient registrations.
- **Practitioner Audit Tracking**: Maintain detailed audit logs of practitioner approvals and system interactions.

## Core System Features
- **JWT Authentication**: Secure stateless authentication using JSON Web Tokens for all API endpoints.
- **Modular API Design**: Flask Blueprints architecture for clean separation of API routes and business logic.
- **Role-Based Access Control (RBAC)**: Secure user login and authorization system ensuring appropriate access for patients, practitioners, and administrators.
- **Automated Reporting**: Weekly compilation of all completed forms into comprehensive reports accessible to both patients and practitioners.
- **Rate Limiting**: Implemented to protect API endpoints from abuse and ensure fair usage.
- **Comprehensive Audit Logs**: Detailed records of significant system actions for security, compliance, and debugging.

## Technical Stack
- **Frontend**: React, Vite, JavaScript
- **Backend**: 
  - Python (Flask)
  - Flask Blueprints for API architecture
  - JWT (PyJWT) for authentication
- **Database**: PostgreSQL (PSQL)
- **ORM**: SQLAlchemy
- **Task Queue**: Celery (for background tasks like report generation and reminders)
- **Message Broker**: Redis (with Celery)

## To-Do List
This is a high-level overview of the development plan. Items will be updated as the project progresses.

### Phase 1: Core Backend & Database Setup
- [ ] Initialize Flask project with Blueprints for modular API architecture.
- [ ] Implement JWT token generation and validation middleware.
- [ ] Set up PostgreSQL database and configure SQLAlchemy.
- [ ] Design and implement core database schemas (Users, Forms, CompletedForms, Medications, AuditLogs).
- [ ] Implement basic user authentication (registration, login) with JWT tokens.
- [ ] Develop initial API endpoints using Blueprints for user management and form creation.
- [ ] Develop initial API endpoints for user management and form creation.

### Phase 2: Frontend Foundation & Core Features
- [ ] Set up React project with Vite.
- [ ] Implement user authentication on the frontend (login, logout, protected routes).
- [ ] Build basic dashboard views for Patients, Practitioners, and Admins.
- [ ] Develop the "Create Form" interface for patients.
- [ ] Implement "View Completed Forms" for patients.

### Phase 3: Practitioner & Admin Features
- [ ] Implement "View Patient List" and "View Individual Completed Forms" for practitioners.
- [ ] Add "Add Comment" and "Pin Form" functionality for practitioners.
- [ ] Develop API endpoints and frontend for Admin patient approval.
- [ ] Implement audit logging for practitioner approvals and other key admin actions.

### Phase 4: Medication Management & Advanced Features
- [ ] Develop medication tracking (current medications, practitioner-suggested) for patients.
- [ ] Implement medication refill reminders (using Celery/Redis for scheduling).
- [ ] Build API endpoints for practitioner medication suggestions.
- [ ] Implement rate limiting for critical API routes.

### Phase 5: Reporting & Trends
- [ ] Implement data aggregation logic for trend visualization.
- [ ] Integrate a charting library (e.g., Chart.js) into the React frontend.
- [ ] Develop logic for weekly report generation (using Celery).
- [ ] Build interfaces for patients and practitioners to view weekly reports.

### Phase 6: Refinement, Testing & Deployment
- [ ] Implement comprehensive error handling.
- [ ] Write unit and integration tests for both frontend and backend.
- [ ] Improve UI/UX based on feedback.
- [ ] Prepare for deployment (Dockerization, CI/CD pipeline).
- [ ] Deploy the application to a cloud platform.