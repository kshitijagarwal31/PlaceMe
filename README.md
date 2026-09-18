# PlaceMe — College Placement Portal

A full-stack college placement portal that helps admins, companies, and students manage the placement process in one place.

---

## Problem Statement

In many colleges, placement activities are managed through spreadsheets, emails, and messages. This can make it difficult to keep track of companies, placement drives, and student applications.

I built PlaceMe to make this process easier and more organized.

---

## Features

### Admin
- Pre-existing admin account — no registration required
- Approve or reject company registration requests
- Approve or reject placement drive requests
- Blacklist students or companies
- View all students, companies, drives, and applications

### Company
- Register and wait for admin approval
- Receive email notification when approved
- Complete company profile before creating a drive
- Create placement drives
- View all applications for their drives
- Update application status — Shortlisted / Interview Scheduled / Selected / Rejected
- Add interview details (date, mode, location) and feedback
- Export all placement drives as CSV via email

### Student
- Register and log in directly
- Must complete profile (CGPA, skills, resume, bio) before applying
- View all active placement drives
- Apply to placement drives
- Track application status in real time
- Receive email notifications on every status update
- Export all applications as CSV via email

---

## Tech Stack

- Frontend: Vue.js — Single Page Application
- Backend: Python, Flask — REST API
- Authentication & RBAC: Flask-Security — Login and Roles
- Database: PostgreSQL — Data Storage
- ORM: SQLAlchemy — Database
- Caching: Redis — API Response Caching
- Async Tasks: Celery — Background Jobs, Email Notifications
- Containerization: Docker & Docker Compose — Multi-container Deployment

---

## Project Structure

```
PlaceMe/
├── backend/
├── frontend/
├── .env.example
├── .gitignore
├── README.md
└── docker-compose.yml
```

---

## How to Run

### Requirements
- Docker
- Docker Compose

### 1. Clone the repository
```bash
git clone https://github.com/kshitijagarwal31/PlaceMe.git
cd PlaceMe
```

### 2. Setup environment variables
```bash
cp .env.example .env
```
Add the required values to the `.env` file

### 3. Run the application
```bash
docker-compose up --build
```

---

## Application Flow

```
1. Company registers and waits for admin approval
2. Admin approves the company
3. Company completes its profile and creates a placement drive
4. Admin approves the drive
5. Student completes their profile and applies to the drive
6. Company reviews applications and updates their status
7. Student receives email notifications about status changes
```

---

## Environment Variables

- `SECRET_KEY`              - Flask secret key 
- `SECURITY_PASSWORD_SALT`  - Password hashing salt
- `DATABASE_URL`            - PostgreSQL connection URL
- `DATABASE_USER`           - PostgreSQL username
- `DATABASE_PASSWORD`       - PostgreSQL password 
- `DATABASE_NAME`           - PostgreSQL database name
- `REDIS_URL`               - Redis connection URL
- `CELERY_BROKER_URL`       - Celery broker (Redis)
- `CELERY_RESULT_BACKEND`   - Celery result backend (Redis)
- `SENDER_ADDRESS`          - Gmail address for sending emails
- `SENDER_PASSWORD`         - Gmail app password

---

## Author

**Kshitij Agarwal**  
[GitHub](https://github.com/kshitijagarwal31) • [LinkedIn](https://www.linkedin.com/in/kshitij-agarwal-b80759370)
