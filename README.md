# Rajasthan Internship & E-Governance Portal

Flask + MySQL web application.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up MySQL
mysql -u root -p < schema.sql

# 3. Configure DB (optional — edit app.py or set env vars)
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=yourpassword
export MYSQL_DB=rajasthan_portal

# 4. Run
python app.py
# → http://127.0.0.1:5000
```

> **Without MySQL**: the app runs in demo mode with sample data.

## Pages & Routes

| Route             | Page                    |
|-------------------|-------------------------|
| `/`               | Dashboard               |
| `/students`       | Student Registration    |
| `/employers`      | Employer Portal         |
| `/placement`      | Placement Analytics     |
| `/egov`           | E-Governance Module     |
| `/internconnect`  | InternConnect Platform  |
| `/notifications`  | Notifications           |
| `/settings`       | Settings                |

## REST API

| Method | Endpoint                         | Description            |
|--------|----------------------------------|------------------------|
| GET    | `/api/students`                  | List all students      |
| GET    | `/api/students/<id>`             | Student detail         |
| GET    | `/api/internships`               | Open internships       |
| GET    | `/api/applications`              | All applications       |
| POST   | `/api/applications`              | Submit application     |
| PUT    | `/api/applications/<id>`         | Update app status      |
| GET    | `/api/stats`                     | Dashboard statistics   |

## Project Structure

```
rajasthan_portal/
├── app.py              ← Flask application (all routes)
├── schema.sql          ← MySQL schema + seed data
├── requirements.txt
├── README.md
└── templates/
    ├── base.html           ← Layout shell (navbar, sidebar, CSS)
    ├── dashboard.html
    ├── students.html
    ├── employers.html
    ├── placement.html
    ├── egov.html
    ├── internconnect.html
    ├── notifications.html
    └── settings.html
```
