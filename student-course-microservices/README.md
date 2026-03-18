# ITSAR2 Laboratory Activity Student Course System — Microservices

## Architecture

```
student-course-microservices/
├── services/
│   ├── student-service/        → port 8001
│   │   ├── app.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── config.py
│   │   ├── requirements.txt
│   │   └── .env
│   ├── course-service/         → port 8002
│   │   ├── app.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── config.py
│   │   ├── requirements.txt
│   │   └── .env
│   └── enrollment-service/     → port 8003
│       ├── app.py
│       ├── models.py
│       ├── routes.py
│       ├── config.py
│       ├── requirements.txt
│       └── .env
├── frontend/                   → port 5500
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── tests/
│   └── test.bat
├── start.ps1
├── .env.example
├── .gitignore
└── README.md
```

### How Services Communicate

```
Browser (port 5500)
    │
    ├──► Student Service    (port 8001) ──► students.db
    ├──► Course Service     (port 8002) ──► courses.db
    └──► Enrollment Service (port 8003) ──► enrollments.db
              │
              ├──► calls Student Service to validate student
              └──► calls Course Service to validate course
```

---

## Prerequisites

- [Python 3.9+](https://python.org/downloads/)
- pip
- Git

---

## Getting Started

### 1. Clone the repository

```powershell
git clone -b Lab2 https://github.com/raubendee-bit/ITSAR-Laboratory.git
cd ITSAR-Laboratory\student-courses-microservices
```

### 2. Install dependencies

```powershell
pip install flask flask-sqlalchemy flask-cors python-dotenv requests
```

### 3. Start all services

```powershell
.\start.ps1
```

### 4. Open the app

```
http://localhost:5500
```

---

## Stopping Services

```powershell
Get-Job | Stop-Job
Get-Job | Remove-Job
```

---

## API Endpoints

### Student Service — `http://localhost:8001`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/students` | Get all students |
| POST | `/students` | Add a new student |
| GET | `/students/{id}` | Get student by ID |
| DELETE | `/students/{id}` | Delete a student |

### Course Service — `http://localhost:8002`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/courses` | Get all courses |
| POST | `/courses` | Add a new course |
| GET | `/courses/{id}` | Get course by ID |
| DELETE | `/courses/{id}` | Delete a course |

### Enrollment Service — `http://localhost:8003`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/enrollments` | Get all enrollments |
| POST | `/enrollments` | Enroll a student in a course |
| GET | `/enrollments/{id}` | Get enrollment by ID |

---
