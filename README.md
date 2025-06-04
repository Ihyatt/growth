# Growth: Mental Wellness Companion

## Project Overview
Growth is a full-stack web application designed to connect patients with mental health practitioners, foster self-awareness through trend tracking, and streamline medication management. This platform aims to empower patients by visualizing their mental health journey, while providing practitioners with essential tools for patient oversight and engagement.

## Current Progress
I've laid down the foundational architecture for the "Growth" application. Here's what's currently implemented:

### Frontend
- ✅ Initialized with React and Vite
- ✅ Core authentication pages (login/registration)
- ✅ Admin practitioner list view

### Backend
- ✅ PostgreSQL database setup
- ✅ SQLAlchemy ORM configuration
- ✅ Flask Blueprints for modular APIs
- ✅ JWT authentication system
- ✅ User table implementation

## Technical Stack
| Category        | Technologies                          |
|-----------------|---------------------------------------|
| **Frontend**    | React, Vite, JavaScript               |
| **Backend**     | Python (Flask), Flask Blueprints      |
| **Database**    | PostgreSQL (PSQL)                     |
| **ORM**         | SQLAlchemy                            |
| **Auth**        | JWT (JSON Web Tokens)                 |
| **Planned**     | Celery (async tasks), Redis (broker)  |

## Future Enhancements

### Core Features
- [ ] Custom form builder for practitioners
- [ ] Patient form completion interface
- [ ] Dynamic trend visualization charts
- [ ] Medication tracking system
  - [ ] Patient medication logs
  - [ ] Practitioner suggestions
  - [ ] Refill reminders

### Automation & Reporting
- [ ] Weekly report generation
- [ ] Email reminder system for forms

### Admin & Security
- [ ] Practitioner approval workflow
- [ ] Audit tracking middleware
- [ ] API rate limiting
- [ ] Comprehensive activity logs

## Development Roadmap

```mermaid
graph TD
    A[Current Foundation] --> B[Form Management]
    B --> C[Data Visualization]
    C --> D[Medication System]
    D --> E[Automation Features]
    E --> F[Admin Security]
    