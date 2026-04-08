# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Async FastAPI service for managing tests (quizzes), questions, answer options, and student attempts. Has its own PostgreSQL database and delegates authentication to the main back-end.

## Project Structure

```
app/
├── main.py       # All FastAPI endpoints (no separate routers)
├── models.py     # SQLAlchemy ORM models
├── schemas.py    # Pydantic request/response schemas
├── crud.py       # Database operations (async)
├── auth.py       # Bearer token verification via back-end
├── db.py         # Async SQLAlchemy engine + session
└── settings.py   # Env-based config (pydantic-settings)
migrations/       # Alembic migrations
```

## Data Model

```
Test
 └── Question (ordered, type: single | multiple | numeric)
      └── Option (is_correct flag)

Attempt (one per user per test, enforced by unique constraint)
 └── AttemptAnswer (one per question: option_id or numeric_answer + is_correct)
```

All PKs are UUIDs. `Attempt.user_id` is an Integer matching the Django user ID.

## Question Types & Scoring

- **single** — exactly one option must be selected; must match the correct option
- **multiple** — any subset of correct options is accepted (partial selection scores a point)
- **numeric** — exact match against `Question.correct_number` (Float)

Score = number of correct answers. `max_score` = total number of questions.

## Authentication

`auth.py` implements a Bearer token dependency. On each request it calls:
```
GET {AUTH_BASE_URL}/api/auth/user/
Authorization: Bearer <token>
```
Returns a `Principal` with `user_id`, `permissions` list, and `is_superuser`. Superusers bypass all permission checks.

Required env var: `AUTH_BASE_URL` (must point to the Django back-end).

## Endpoints

All endpoints defined directly in `main.py` (no router modules):

| Resource    | Endpoints                                                    |
|-------------|--------------------------------------------------------------|
| Tests       | CRUD at `/tests` and `/tests/{id}`                           |
| Questions   | CRUD at `/tests/{id}/questions` and `/tests/{id}/questions/{id}` |
| Attempts    | `POST /tests/{id}/attempts/start`, `GET .../attempts/me`, `GET .../attempts` |
| Submission  | `POST /tests/{id}/submit` — scores the attempt, prevents double submission |
| Health      | `GET /health`                                                |

Write endpoints require `marks.post.milfaculty` permission. Read endpoints are open to any authenticated user.

## Database & Migrations

- Async SQLAlchemy with `asyncpg` driver
- Alembic for migrations (`migrations/`)
- Separate PostgreSQL instance (port 5433 by default, configured via `QUIZZES_DB_*` env vars)

To create a new migration after changing models:
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Key Env Vars

`AUTH_BASE_URL`, `QUIZZES_DB_HOST`, `QUIZZES_DB_PORT`, `QUIZZES_DB_NAME`, `QUIZZES_DB_USER`, `QUIZZES_DB_PASSWORD`, `QUIZZES_HOST`, `QUIZZES_PORT`
