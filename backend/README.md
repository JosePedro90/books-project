# Books Project Backend

[![Django](https://img.shields.io/badge/Django-4.2-brightgreen)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue)](https://docs.docker.com/compose/)
[![Celery](https://img.shields.io/badge/Celery-5.3%20|%20Redis-green)](https://docs.celeryq.dev/)

A Django-based backend for managing books and reservations.

## 📋 Table of Contents

- [Books Project Backend](#books-project-backend)
  - [📋 Table of Contents](#-table-of-contents)
  - [🎨 Design Choices](#-design-choices)
    - [Architecture](#architecture)
  - [📦 Prerequisites](#-prerequisites)
  - [✨ Key Features](#-key-features)
  - [🚀 Running the Application](#-running-the-application)
  - [💡 Future Enhancements](#-future-enhancements)

## 🎨 Design Choices

### Architecture

- **Dockerized Services**: Containerized using Docker Compose for environment consistency.
- **PostgreSQL**: Relational database for structured book data storage and reservations.
- **Redis + Celery**: Asynchronous task processing for CSV injection and other background tasks.
- **RESTful API:** API endpoints are designed following RESTful principles.
- **JWT Authentication:** JSON Web Tokens are used for secure authentication and authorization.

## 📦 Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Python 3.11

## ✨ Key Features

- **Book Management:** CRUD operations for books, including author linking.
- **Reservation Management:** Handles book reservations, linking books to users.
- **CSV Import:** Functionality to import book data from CSV files.
- **Email Notifications:** Email notifications are currently mocked for demonstration purposes.
- **Security:** Sensitive data (database credentials, secret key) is managed via environment variables.
- **JWT Authentication:** Secure API access via JWT (access and refresh tokens).

## 🚀 Running the Application

This application can be run using either Docker Compose for containerized deployment or standard Django commands for local development.

**Option 1: Docker Compose (Recommended)**

1. **Clone:** `git clone <your_repository_url>` and `cd <your_project_directory>`.

2. **.env:** Create a `.env` file (same directory as `docker-compose.yml`) with:

```
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=db
DATABASE_PORT=5432
SECRET_KEY=a_strong_secret_key
DJANGO_SUPERUSER_PASSWORD=your_admin_password
DJANGO_SUPERUSER_EMAIL=admin@example.com
CELERY_BROKER_URL=redis://redis:6379/0
```

1. **Run:** `docker-compose up -d --build`

2. **Access:** `http://localhost:8000` (app), `http://localhost:8000/admin` (admin).

3. **Logs:** `docker-compose logs web`, `docker-compose logs db`, `docker-compose logs redis`.

4. **Stop:** `docker-compose down`

**Option 2: Local Development (Django Commands)**

1. **.env:** Create `.env` file as above.

2. **Install with Poetry:**

   `poetry install`

3. **Migrate:** `python manage.py migrate`

4. **Superuser:** `python manage.py createsuperuser --username=admin --email=your_email --noinput && echo "$DJANGO_SUPERUSER_PASSWORD" | python manage.py changepassword admin`

5. **Run:** `python manage.py runserver 0.0.0.0:8000`

## 💡 Future Enhancements

- **API Documentation:** Adding API documentation (e.g., using Swagger or DRF-yasg) would be beneficial.
- **More Robust CSV Handling:** The CSV import could be made more robust with better error handling and data validation.
- **Bulk Update on CSV Injection:** Implementing bulk update functionality during CSV injection to improve performance and efficiency.
- **Robust Testing:** Expanding the test suite to include more comprehensive test coverage, including edge cases, integration tests, and performance tests, would further enhance the application's reliability.
- **Celery Task Tracking:** Implementing Celery task tracking would provide visibility into the status and results of asynchronous tasks.
