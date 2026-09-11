# Waimea User API

REST API for user registration built with FastAPI, PostgreSQL and SQLAlchemy.

## Tech Stack

- Python 3.14
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pytest
- Ruff
- uv
- Docker Compose

## Running

Create the environment file:

cp .env.example .env

Start PostgreSQL:

docker compose up -d postgres

Run migrations:

uv run alembic upgrade head

Start the API:

uv run uvicorn waimea_user_api.main:app --reload

API: http://localhost:8000

Swagger: http://localhost:8000/docs

## Tests

uv run pytest

## Code Quality

uv run ruff check .
uv run ruff format .