# PlaceMe — College Placement Portal

> A full-stack placement management system that streamlines the entire campus recruitment process — from company registration to student selection.

## Live Demo
🔗 **Frontend:** https://place-me-one.vercel.app
🔗 **Backend API:** https://placeme-api.up.railway.app

## Demo Credentials

| Role | Email | Password |
|---|---|---|
| Admin | admin@gmail.com | admin@123 |
| Company | company@demo.com | company@123 |
| Student | student@demo.com | student@123 |

> **Note:** Register as a new company or student to experience the full flow from scratch.

---

## Problem Statement

College placement processes are often managed manually — through spreadsheets, emails, and WhatsApp messages. This leads to miscommunication, missed deadlines, and a lack of transparency for students and companies alike.

**PlaceMe solves this** by providing a centralized platform where admins, companies, and students can manage the entire placement lifecycle in one place.

---

## Features

### Admin
- Pre-existing admin account — no registration required
- Approve or reject company registration requests
- Approve or reject placement drive requests
- Blacklist students or companies
- View all students, companies, drives, and applications
- Full visibility across the entire placement process

### Company
- Register and await admin approval
- Receive email notification upon approval
- Complete company profile before creating drives
- Create placement drives (pending admin approval)
- View all applications for their drives
- Update application status — Shortlisted / Interview Scheduled / Selected / Rejected
- Add interview details (date, mode, location) and feedback
- Export all placement drives as CSV via email

### Student
- Register and log in directly
- Must complete profile (CGPA, skills, resume, bio) before applying
- View all active placement drives
- Apply to drives with one click
- Track application status in real time
- Receive email notifications on every status update
- Export all applications as CSV via email

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Vue.js | Single Page Application |
| **Backend** | Python, Flask | REST API |
| **Authentication & RBAC** | Flask-Security | Token Auth · Admin / Company / Student Roles |
| **Database** | PostgreSQL | Relational Data Storage |
| **ORM** | SQLAlchemy | Database Abstraction Layer |
| **Caching** | Redis | API Response Caching |
| **Async Tasks** | Celery | Background Jobs · Email Notifications |
| **Containerization** | Docker & Docker Compose | Multi-container Deployment |

---

## Project Structure

```
PlaceMe/
├── backend/
├── frontend/
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```
---

## Getting Started

### Prerequisites
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
Open `.env` and fill in your values.

### 3. Run the application
```bash
docker-compose up --build
```

### 4. Open in browser
```
Frontend  →  https://place-me-one.vercel.app
Backend   →  https://placeme-api.up.railway.app
```

---

## Application Flow

```
1. Company registers → Admin approves → Company gets email
2. Company completes profile → Creates placement drive
3. Admin approves drive → Drive goes live
4. Student completes profile → Applies to drive
5. Company reviews applications → Updates status with feedback
6. Student receives email on every status update
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Flask secret key |
| `SECURITY_PASSWORD_SALT` | Password hashing salt |
| `DATABASE_URL` | PostgreSQL connection URL |
| `DATABASE_USER` | PostgreSQL username |
| `DATABASE_PASSWORD` | PostgreSQL password |
| `DATABASE_NAME` | PostgreSQL database name |
| `REDIS_URL` | Redis connection URL |
| `CELERY_BROKER_URL` | Celery broker (Redis) |
| `CELERY_RESULT_BACKEND` | Celery result backend (Redis) |
| `SENDER_ADDRESS` | Gmail address for sending emails |
| `SENDER_PASSWORD` | Gmail app password |

---

## Author

**Kshitij Agarwal**  
[GitHub](https://github.com/kshitijagarwal31) • [LinkedIn](https://www.linkedin.com/in/kshitij-agarwal-b80759370)