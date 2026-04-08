# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run all tests
docker compose -f ../dev-dc.yaml run back-end scripts/test.sh

# Run a specific test file or directory
docker compose -f ../dev-dc.yaml run back-end pytest src/lms/tests/test_lessons.py

# Format code (black)
docker compose -f ../dev-dc.yaml run back-end scripts/format.sh
docker compose -f ../dev-dc.yaml run back-end scripts/format.sh --check

# Django management
docker compose -f ../dev-dc.yaml run back-end python manage.py migrate
docker compose -f ../dev-dc.yaml run back-end python manage.py register_permissions
docker compose -f ../dev-dc.yaml run back-end python manage.py populate   # seed test data
```

## App Structure (`src/`)

| App      | Responsibility                                                           |
|----------|--------------------------------------------------------------------------|
| `conf/`  | Settings, root URL routing, WSGI                                         |
| `auth/`  | Custom User model, JWT tokens, groups, custom permission system          |
| `common/`| Shared models (Campus, Faculty, Program, BirthInfo, Photo, Subject, etc.)|
| `ams/`   | Applicant Management — applications, physical tests, admission pipeline  |
| `lms/`   | Learning Management — students, teachers, lessons, marks, absences, etc. |
| `dms/`   | Document Management — books, papers, videos, class materials             |
| `tgbot/` | Telegram session model + endpoint (chat_id ↔ phone mapping)             |

URL prefix per app: `/api/auth/`, `/api/ams/`, `/api/dms/`, `/api/lms/`, `/api/tgbot/`.

## Authentication & Permissions

### JWT Auth
- simplejwt: access token 50 min, refresh token 1 day
- `BearerTokenMiddleware` pulls token from cookie as fallback
- Bot/service accounts authenticate with email+password and store the token

### Custom Permission System
Django's built-in permissions are **not used**. The project has its own:

- `Permission` model: `viewset` + `method` + `scope` → `codename` (e.g. `students.get.milfaculty`)
- `scope` levels: `ALL(0)` → `MILFACULTY(10)` → `MILGROUP(20)` → `SELF(30)`
- Users have permissions directly or via `Group`
- New permissions are auto-discovered and registered via:
  ```bash
  python manage.py register_permissions
  ```
  This command scans all `BasePermission` subclasses — add new permissions there, then run the command.

### QuerySet Scoping
`QuerySetScopingMixin` (in `lms/utils/mixins.py`) automatically filters querysets based on the authenticated user's scope. Override `handle_scope_milfaculty()` / `handle_scope_milgroup()` / `handle_scope_self()` in a ViewSet to customize filtering per scope level.

`StudentTeacherQuerySetScopingMixin` handles the common pattern of filtering marks, absences, and similar resources by the student/teacher's organizational unit.

## Key Patterns

### Action-based serializers
ViewSets pick a serializer based on the current action:
```python
MUTATE_ACTIONS = ["create", "update", "partial_update"]

def get_serializer_class(self):
    if self.action in MUTATE_ACTIONS:
        return MyWriteSerializer
    return MyReadSerializer
```

### Signal-based file cleanup
`Photo`, `Video`, and `File` models use `post_delete` / `pre_save` signals to delete files from disk automatically. Always delete model instances (not just files) to avoid orphaned media.

### Ordered models
`Section` and `Topic` in DMS use `django-ordered-model`. Use `.to(order)` to reposition; don't set `order` manually.

### Mark history
`Mark` uses both an `ArrayField` (multiple values for retakes) and `django-simple-history` for full change tracking.

### Personnel type union
`lms/utils/types.py` defines `Personnel = Student | Teacher` (Python 3.10 syntax). Scope-filtering logic uses this union to determine access level uniformly.

## Testing

- Fixtures in `src/conftest.py`: `superuser`, `su_client`, `test_user`, `test_client`, `permission_data`
- `remove_permissions` fixture auto-clears test user permissions after each test
- Each app has `tests/conftest.py` with model factories specific to that domain
- Tests use `pytest-django` with a real PostgreSQL database — no mocking the DB
