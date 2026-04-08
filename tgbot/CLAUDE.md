# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Telegram bot for military group (milgroup) commanders. The primary workflow is daily absence reporting: a commander selects their personnel, marks each student's status (present / late / leave / illness), and submits the report.

Secondary function: receives uniform-change notifications from the back-end via an internal HTTP webhook and broadcasts them to relevant commanders.

## Entry Point & Launch (`src/bot.py`)

The bot runs two concurrent tasks:
1. **Telegram polling** — `dp.start_polling()` (aiogram 2.x long-poll)
2. **aiohttp web server** — listens on `TGBOT_PORT` for the `POST /uniforms/` webhook

Both are started with `asyncio.gather()`. On startup: `dp.skip_updates()` discards stale messages.

## Project Structure

```
src/
├── bot.py              # Entry point, dispatcher setup, asyncio.gather
├── config.py           # Env vars (TOKEN, DEBUG, TGBOT_PORT, BACK_END_PORT, etc.)
├── handlers/
│   ├── __init__.py     # Registers all handlers on the dispatcher
│   ├── auth.py         # Contact sharing → authorization
│   ├── menu.py         # /start, main menu
│   └── absence.py      # List personnel, toggle status, submit report
├── middleware/
│   └── auth.py         # AuthMiddleware — blocks unauthenticated users
├── api/
│   ├── client.py       # HTTP client with Bearer token + auto-refresh
│   ├── auth.py         # Session CRUD + authorization logic
│   ├── student.py      # Student/milgroup fetching, Student dataclass
│   └── absence.py      # Absence CRUD, report formatting
├── keyboards/
│   ├── reply.py        # Main menu keyboard
│   └── inline.py       # Per-student absence status buttons
├── messages/           # Message text constants
├── routes/
│   └── uniforms.py     # aiohttp route handler for POST /uniforms/
├── utils/
│   └── time.py         # Timezone helpers, absence time-window validation
└── proto/
    └── uniforms.py     # Uniform dataclass (headdress, outerwear, milfaculty)
```

## Authentication Flow

1. User sends `/start` → bot checks if a `Session` exists in back-end
2. If no session: bot asks user to share contact (phone number)
3. Phone is sent to `auth/authorize()` which calls back-end to verify the user is a milgroup commander (`post == "GC"` or `"SC"`)
4. On success: session is persisted in back-end (`tgbot/session/` endpoint), linking `chat_id` ↔ `phone`
5. `AuthMiddleware` checks session existence on every subsequent message; unauthenticated messages are dropped with `CancelHandler()`

## Absence Reporting Flow

1. Commander taps "Личный состав" → bot fetches students via `lms/students/` filtered by milgroup
2. Bot shows inline keyboard per student with status buttons (present / late / leave / illness)
3. Each button tap triggers a callback → `toggle_student_absence_status()` → immediately POSTs/DELETEs to `lms/absences/`; state is kept in FSM via `await state.set_data(students_by_id)`
4. Commander taps "Доложить расход" → `report_absence()` submits a formatted summary
5. Reports can only be sent within the time window from `lms/absence-time/` (Moscow timezone)

## API Client (`src/api/client.py`)

- Single `Client` class with a persistent `aiohttp.ClientSession`
- Authenticates once with `TGBOT_EMAIL`/`TGBOT_PASSWORD` to obtain a Bearer token
- On 401 response: automatically re-authenticates and retries the original request
- Base URL: `http://back-end:{BACK_END_PORT}/api`

## aiogram Patterns

- **Version**: aiogram 2.12.x — uses old-style `Dispatcher`, not the 3.x `Router`
- **FSM**: `MemoryStorage` — state is lost on bot restart; stores `dict[student_id → Student]`
- **Handler registration**: explicit `dp.register_message_handler()` / `dp.register_callback_query_handler()` calls in `handlers/__init__.py`
- **Middleware**: registered via `dp.middleware.setup(AuthMiddleware())`

## Key Env Vars

`TOKEN`, `TGBOT_PORT`, `TGBOT_EMAIL`, `TGBOT_PASSWORD`, `BACK_END_PORT`, `DEBUG`
