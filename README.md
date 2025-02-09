# Books Project

A full-stack web application designed to manage and display a collection of books, with separate frontend and backend components for modular development.

## 📋 Table of Contents

- [Books Project](#books-project)
  - [📋 Table of Contents](#-table-of-contents)
  - [📚 Project Overview](#-project-overview)
  - [🛠 Technologies Used](#-technologies-used)
    - [Backend](#backend)
    - [Frontend](#frontend)
  - [🏗 Project Structure](#-project-structure)
  - [🚀 Getting Started](#-getting-started)
    - [Prerequisites](#prerequisites)
    - [Quick Start](#quick-start)
  - [📂 Related Repositories](#-related-repositories)

## 📚 Project Overview

This project provides a platform to manage book data and book reservations with a Django-based backend and a React-based frontend. The backend handles API requests, data storage, and asynchronous tasks, while the frontend offers a modern user interface for managing and browsing books.

## 🛠 Technologies Used

### Backend

- **Django 4.2**: Web framework for building the backend API
- **Django REST Framework**: Tools for building robust RESTful APIs
- **PostgreSQL**: Relational database management
- **Docker & Docker Compose**: Containerization for consistent development environments
- **Celery & Redis**: Asynchronous task management

### Frontend

- **React**: JavaScript library for building user interfaces
- **TypeScript**: Static typing for JavaScript
- **Axios**: Promise-based HTTP client for API requests

## 🏗 Project Structure

```
books-project/
├── backend/         # Django backend
│   └── README.md    # Backend-specific instructions
├── frontend/        # React frontend
│   └── README.md    # Frontend-specific instructions
├── docker-compose.yml
└── README.md        # General project overview
```

## 🚀 Getting Started

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

### Quick Start

1. **Clone the repository:**

```bash
git clone https://github.com/JosePedro90/books-project.git
cd books-project
```

2. **Start Services:**

- For backend

```bash
cd backend
docker-compose up -d
```

- For frontend

```bash
cd frontend
npm run dev
```

3. **Access the application:**
   Start

- Backend API: `http://localhost:8000`
- Frontend UI: `http://localhost:5173`

- The default administrator username is `admin`, and the initial password is `your_strong_password`."

For detailed setup instructions, refer to the [backend](./backend/README.md) and [frontend](./frontend/README.md) READMEs.

## 📂 Related Repositories

- [Backend README](./backend/README.md): Configuration and setup instructions for the Django backend.
- [Frontend README](./frontend/README.md): Configuration and setup instructions for the React frontend.
