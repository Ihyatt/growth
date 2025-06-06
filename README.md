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
