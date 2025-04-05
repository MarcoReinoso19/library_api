# Library Management System - Backend

## 📚 Project Description

Backend application for a library management system built with:

- **FastAPI** (API Framework)
- **Pydantic** (Python Data Validation)
- **SqlAlchemy** (Object Relational Mapping)
- **Alembic** (Database Migrations in case of changing db)
- **SqlLite** (Database Management)

The system consists of two services:

1. **library-app** (separate frontend service)
2. **library-api** (this project - backend)

## 🚀 Prerequisites

- Python v3.12+
- uv (pip install uv)

## Installation

1. Clone repository:

   ```Powershell
   git clone https://github.com/MarcoReinoso19/library_api
   ```

2. Install dependencies in library-api:

   ```Powershell
   uv sync
   ```

3. This project needs to run in:
   <http://localhost:8000>

## Running the App

Start development server:

```Powershell
uv run uvicorn main:app --reload
```

- Access application at:
<http://localhost:8000>

- Access docs at:
<http://localhost:8000/docs>

---

## Project Structure

```md
app/
├── models/
├── routers/
├── schemas/
├── services/
├── pages/
config/
db/
shared/
    └── utils/
```
# library_api
