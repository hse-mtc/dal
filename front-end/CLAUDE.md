# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm run dev            # dev server on :9528
npm run build:production
npm run test:unit      # Jest unit tests
npm run lint           # ESLint check only
npm run lint:fix       # ESLint fix in-place
npm run test:ci        # lint + test:unit (used in CI)
```

Dev server proxies `/api/*` and `/media/*` to the back-end (configured in `vue.config.js` via env vars `VUE_APP_BACK_END_HOST` / `VUE_APP_BACK_END_PORT`, defaulting to `localhost:9090`).

## Architecture

### Routing (`src/router.js`)
Routes are grouped by domain. Top-level groups:
- **Auth routes** — login, registration, password recovery, applicant flow (no sidebar layout)
- **Core layout routes** — everything under the `Layout` shell with sidebar:
  - `/discipline-control/` — subjects, schedule, marks, quizzes
  - `/personnel/` — students, teachers, uniforms
  - `/absence/`, `/discipline/` — attendance and disciplinary actions
  - `/apanel/` — admin panel (user/role management, approvals, dictionaries)
  - `/applications/` — applicant document tracking

Routes use `meta.permissions` to control visibility. History mode is enabled — server must support it.

### Vuex Store (`src/store/`)
Class-based modules via `vuex-module-decorators`. Import modules like:
```js
import { UserModule, ChoicesModule } from "@/store";
```

| Module       | What it holds                                                         |
|--------------|-----------------------------------------------------------------------|
| `user`       | JWT tokens, user ID, permissions, campuses, person info (lazy-loaded) |
| `app`        | Sidebar state, device type                                            |
| `choices`    | Enum dictionaries (absence statuses, student posts, teacher ranks…)  |
| `reference`  | Reference data (milgroups, milfaculties, milspecialties, rooms…)     |
| `subjects`   | Subject list + current subject + sections                             |
| `papers`     | Publishers, authors, categories                                       |
| `settings`   | UI settings (fixed header, sidebar logo)                              |

**Lazy-load pattern**: getters auto-trigger a fetch on first access if data isn't loaded yet. Components just read `UserModule.permissions` — no manual fetch needed.

### API Layer (`src/api/` + `src/utils/request.js`)
- Axios instance with base URL `/`, 10 s timeout
- Request interceptor: attaches Bearer token
- Response interceptor: on 401 auto-refreshes token via `updateAccess()` and retries; on failed refresh clears tokens and redirects to `/login/`
- Each file in `src/api/` exports named functions for one domain (`students.js`, `marks.js`, `books.js`, etc.)
- All endpoint URL fragments live in `src/constants/api.js` — always add new endpoints there

### Component Structure
```
src/
├── views/          # Thin page wrappers — one per route, import from components/
├── components/     # Feature components grouped by domain
│   ├── Personnel/  # Students, Teachers, Student profile tabs
│   ├── @Subjects/  # Subject and section/topic navigation
│   ├── Apanel/     # Admin panel components
│   └── ...
├── common/         # Shared UI: Form builder, input components, SearchBar, PageHeader
└── layout/         # App shell: Sidebar, Navbar, AppMain
```

Views are intentionally thin — they just render the matching component. Business logic lives in components and the store.

### Permissions
- `src/utils/permissions.js` — `hasPermission(permissions)` checks multiple scope variants
- Permission names follow back-end codenames: e.g. `students.get.all`, `students.get.milfaculty`, `students.get.milgroup`
- Used both in router meta and in component `v-if` guards

## Key Patterns

### Generic store action factories (`src/utils/mutators.js`)
`getFetchRequest`, `getAddRequest`, `getEditRequest`, `getDeleteRequest` return async action functions that handle the common fetch → mutate → notify flow. Use these instead of writing boilerplate actions.

### Reusable inputs (`src/common/inputs/`)
All custom input components extend `InputsBase.vue` and `inputsMixin.js` for consistent `v-model` binding and error handling.

### Token lifecycle (`src/utils/tokenService.js`)
Singleton reading/writing tokens in `localStorage`. Decodes JWT to extract `userId`. Use `tokenService` directly for token access outside the store.
