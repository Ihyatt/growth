# Growth - Mental Health Platform

*A platform connecting therapists and clients for better mental health outcomes*

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Development](#development)
- [License](#license)

## ✨ Features

### For Therapists
- **Form Management**
  - Create custom assessment forms
  - Assign forms to specific patients
  - View form completion progress
- **Patient Management**
  - Follow/unfollow patients
  - View patient medication dashboards
  - Comment on patient medications and reports
- **Reporting**
  - Automatic weekly report generation
  - Historical report analysis

### For Patients
- **Form Completion**
  - Fill out assigned forms
  - View form history
- **Medication Tracking** 💊
  - Dashboard of current medications
  - Add/edit medication details
  - Comment on medications (visible to therapist)
- **Communication**
  - Comment on generated reports
  - Follow/unfollow therapists

### For Admins
- **Therapist Approval**
  - Review and approve new therapist accounts
  - Manage platform users
- **Content Moderation**
  - Monitor comments and interactions
  - Handle reports

## 🛠 Tech Stack

### Frontend
- React.js
- React Router v6
- Chart.js (for reports)
- Tailwind CSS

### Backend
- Flask (Python)
- PostgreSQL
- SQLAlchemy
- JWT Authentication

### DevOps
- Docker
- AWS EC2
- GitHub Actions CI/CD

## 🚀 Installation

```bash
# Clone repository
git clone https://github.com/yourusername/growth.git

# Backend setup
cd server
python -m venv venv
source venv/bin/activate 
pip3 install -r requirements.txt
rm -rf migrations
psql -U <Username> -d growth_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
psql -U <username> -d growth_db -c 'GRANT ALL ON SCHEMA public TO "Inashyatt1";'
psql -U <username>-d growth_db -c "\dn+ public"
flask db init
flask db migrate -m "Initial schema creation"
flask db upgrade
python seed.py
python3 run.py

# Frontend setup
cd ../client
npm install


TODO:
add a cron job to expire expired forms that havent been completed after a week


API ROUTE PAGES

AUTH
/login
/register

ADMIN
/admins/search
/admins/approve/user_id
/admins/reject/user_id


THERAPIST
therapists/therapist_username/search-patients?
therapists/therapist_username/search-form-templates?
therapists/therapist_username/create-form-template

THERAPIST/THERAPIST_USERNAME/PATIENTS/PATIENT_USERNAME
therapists/therapist_id/patients/patient_username 
therapists/therapist_username/patients/patient_username/medications
therapists/therapist_username/patients/patient_username/medications/add
therapists/therapist_id/patients/patient_username/reports
therapists/therapist_id/patients/patient_username/assigned_forms


THERAPIST/THERAPIST_USERNAME/PATIENTS/PATIENT_USERNAME/MEDICATIONS/MEDICATION_ID
therapists/therapist_username/patients/patient_username/medications/medication_id/delete
therapists/therapist_username/patients/patient_username/medications/medication_id/edit
therapists/therapist_username/patients/patient_username/medications/medication_id/comment


THERAPIST/THERAPIST_USERNAME/PATIENTS/PATIENT_USERNAME/MEDICATIONS/MEDICATION_ID/MEDICATION_COMMENTS/MEDICATION_COMMENT_ID
therapists/therapist_username/patients/patient_username/medications/medication_id/comments/medication_comment_id/edit
therapists/therapist_username/patients/patient_username/medications/medication_id/comments/medication_comment_id/delete



THERAPIST/THERAPIST_USERNAME/FORM_TEMPLATE/FORM_TEMPLATE_ID
therapists/therapist_username/form_template/form_template_id/assign
therapists/therapist_username/form_template/form_template_id/un_assign
therapists/therapist_username/form_template/form_template_id/archive


therapists/therapist_username/patients/care_team/connect
therapists/therapist_username/patients/care_team/disconnect



patients/patient_username
patients/patient_username/assigned_forms
patients/patient_username/reports
patients/patient_username/medications


patients/patient_username/assigned_forms/assigned_form_id
patients/patient_username/assigned_forms/assigned_form_id/submit


patients/patient_username/medications/medication_id
patients/patient_username/medications/medications_id/comments/create


patients/patient_username/reports/reports_id
patients/patient_username/reports/reports_id/comments/create


create cron job that expires forms that are a week old, cron job can be run every night