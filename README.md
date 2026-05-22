# Shortcuts App

A keyboard shortcuts reference app. Add applications, organize shortcuts by category, and browse them from a searchable main page.

## Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: SvelteKit, Tailwind CSS, DaisyUI
- **Infrastructure**: Docker, nginx (reverse proxy)
- **Package managers**: uv (Python), pnpm (Node)

---

## Running with Docker (production)

Copy the example env file and fill in the values:

```
cp .env.example .env
```

Required variables:

| Variable            | Description                        |
|---------------------|------------------------------------|
| `POSTGRES_PASSWORD` | Password for the PostgreSQL user   |
| `SECRET_KEY`        | Secret used to sign JWT tokens     |

Then bring everything up:

```
make up
```

The app is served at `http://localhost:8080` via nginx. The first time you run it, create an admin user:

```
make create-admin
```

Optionally seed the database with example shortcut data:

```
make seed
```

---

## Local development

### Backend

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```
cd backend
uv sync
uv run uvicorn src.main:app --reload
```

The API runs at `http://localhost:8000`. Interactive docs are at `/docs`.

The backend reads `DATABASE_URL` and `SECRET_KEY` from a `.env` file in the `backend/` directory when running locally.

### Frontend

Requires Node.js and [pnpm](https://pnpm.io/).

```
cd frontend
pnpm install
pnpm dev
```

The dev server runs at `http://localhost:5173` and proxies `/api/` to the backend.

---

## Commands

All commands can be run from the project root via `make`.

### Docker

| Command          | Description                        |
|------------------|------------------------------------|
| `make up`        | Start all services in the background |
| `make down`      | Stop and remove containers         |
| `make build`     | Rebuild Docker images              |
| `make logs`      | Tail logs from all services        |
| `make restart`   | Restart all services               |

### Data

| Command              | Description                                |
|----------------------|--------------------------------------------|
| `make create-admin`  | Interactive prompt to create an admin user |
| `make seed`          | Seed the database with example shortcuts   |

### Development

| Command              | Description                              |
|----------------------|------------------------------------------|
| `make dev-backend`   | Run the backend with hot reload          |
| `make dev-frontend`  | Run the frontend dev server              |
| `make gen-types`     | Regenerate TypeScript types from the backend OpenAPI spec (requires backend running) |
| `make check`         | Run SvelteKit type checker               |
| `make lint`          | Lint both frontend and backend           |
| `make lint-frontend` | Run ESLint on the frontend               |
| `make lint-backend`  | Run Ruff on the backend                  |

---

## Project structure

```
.
+-- backend/
|   +-- src/
|   |   +-- admin/          # Auth logic and login route
|   |   +-- database/       # SQLAlchemy schema, session, and repositories
|   |   +-- scripts/        # One-off scripts (create_admin_user, seed)
|   |   +-- shortcuts/      # Applications, categories, and shortcuts routes
|   |   +-- main.py
|   +-- config.py           # Settings loaded from environment
|   +-- pyproject.toml
+-- frontend/
|   +-- src/
|   |   +-- lib/
|   |   |   +-- api.ts              # API client
|   |   |   +-- api.types.ts        # Auto-generated from OpenAPI spec (do not edit)
|   |   |   +-- components/         # Shared components
|   |   +-- routes/
|   |       +-- +page.svelte        # Main shortcuts browser
|   |       +-- admin/
|   |           +-- +page.svelte    # Login page
|   |           +-- panel/
|   |               +-- +page.svelte  # Admin panel (apps, categories, shortcuts)
|   +-- package.json
+-- docker-compose.yml
+-- nginx.conf
+-- Makefile
```

---

## Type sync

The frontend types in `src/lib/api.types.ts` are generated from the FastAPI OpenAPI spec. They are committed to the repo. After changing any backend Pydantic model, regenerate them:

```
make gen-types
```

TypeScript will then flag any frontend code that is out of sync with the backend.

---

## Admin panel

Navigate to `/admin` to log in. From the panel you can:

- Create and delete applications (name + accent color)
- Create and delete shortcut categories within an application
- Create and delete shortcuts within a category, recording keystrokes directly from the keyboard
