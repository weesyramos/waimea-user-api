# Waimea User API

REST API for user registration built with Python 3.14, FastAPI, PostgreSQL and SQLAlchemy.

The project follows a Clean Architecture-oriented structure and includes password hashing with Argon2, transaction management, automated tests and Docker support.

## Tech Stack

- Python 3.14
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- pwdlib + Argon2
- Pytest
- Ruff
- uv
- Docker Compose

## Running the Project

### 1. Clone the repository

git clone <repository-url>
cd waimea-user-api

### 2. Configure environment

cp .env.example .env

### 3. Start PostgreSQL

docker compose up -d postgres

### 4. Run migrations

uv run alembic upgrade head

The initial migration creates the database tables and an admin role for testing.

### 5. Start the API

uv run uvicorn waimea_user_api.main:app --reload

API: http://localhost:8000

Swagger: http://localhost:8000/docs

## Tests

uv run pytest

## Code Quality

uv run ruff check .
uv run ruff format .

## Project Structure

src/
└── waimea_user_api/
    ├── application/
    ├── domain/
    ├── infrastructure/
    └── presentation/

## Main Endpoint

### Create User

POST /users

Example request:

{
  "name": "John Doe",
  "email": "john@example.com",
  "role_id": 1
}

When the password is not provided, the API generates one automatically.