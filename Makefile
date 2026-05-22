.PHONY: up down build logs restart \
        create-admin seed \
        dev-backend dev-frontend \
        gen-types check lint lint-backend lint-frontend

# Docker

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

restart:
	docker compose restart

# First-time / data setup

create-admin:
	cd backend && uv run python src/scripts/create_admin_user.py

seed:
	cd backend && uv run python src/scripts/seed.py

# Local development

dev-backend:
	cd backend && uv run uvicorn src.main:app --reload

dev-frontend:
	cd frontend && pnpm dev

# Frontend tooling

gen-types:
	cd frontend && pnpm gen:types

check:
	cd frontend && pnpm check

lint-frontend:
	cd frontend && pnpm lint

lint-backend:
	cd backend && uv run ruff check src/

lint: lint-frontend lint-backend
