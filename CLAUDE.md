# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DAL is an educational platform for HSE (Higher School of Economics) combining Document Management, Learning Management, and Applicant Management. The system serves military education units with support for students, teachers, applicants, quizzes, documents, and a Telegram bot for commanders.

## Services

| Service    | Technology        | Port  | Description                               |
|------------|-------------------|-------|-------------------------------------------|
| back-end   | Django REST        | 1112  | Main API — auth, LMS, AMS, DMS            |
| front-end  | Vue.js 2           | 1116  | Single-page application                   |
| watchdoc   | FastAPI            | 1113  | DOCX document generation + Yandex Disk    |
| tgbot      | aiogram (Python)   | 1115  | Telegram bot for milgroup commanders      |
| quizzes    | FastAPI (async)    | 5050  | Quiz management with own PostgreSQL DB    |
| nginx      | Nginx              | 80/443| Reverse proxy + static files              |

## Service Interactions

```
[front-end] ──HTTP──► [back-end :1112] ──► [PostgreSQL]
                            │
                            ├──► [watchdoc :1113]  (POST /applicants/)
                            │         └──► Yandex Disk + Email
                            │
                            └──► [quizzes :5050]   (auth verification)
                                      └──► [PostgreSQL (separate DB)]

[tgbot] ──HTTP──► [back-end :1112]   (sessions, students, absences)
       ◄──webhook── [back-end]        (uniform change notifications)

[Ofelia] ──docker labels──► scheduled tasks on containers
```

`front-end` proxies `/api/*` and `/media/*` to `back-end`. The `quizzes` service calls back-end to verify Bearer tokens.

## Docker Compose

```bash
# Development (hot-reload, volume mounts)
docker compose -f dev-dc.yaml up

# Production
docker compose -f prod-dc.yaml up
```

## Environment Setup

Copy `.env.example` → `.env`. Each service also has its own `.env.example`:
- `back-end/.env.example` — Django SECRET_KEY, DB, SMTP
- `watchdoc/.env.example` — Yadisk token, SMTP
- `tgbot/.env.example` — Telegram TOKEN, back-end credentials
- `quizzes/.env.example` — separate DB connection, auth_base_url

## Per-Service Documentation

Detailed architecture and development commands for each service live in their own CLAUDE.md:

- [back-end/CLAUDE.md](back-end/CLAUDE.md)
- [front-end/CLAUDE.md](front-end/CLAUDE.md)
- [watchdoc/CLAUDE.md](watchdoc/CLAUDE.md)
- [tgbot/CLAUDE.md](tgbot/CLAUDE.md)
- [quizzes/CLAUDE.md](quizzes/CLAUDE.md)
