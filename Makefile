.PHONY: up down build logs shell test migrate makemigrations superuser lint format fix check pre-commit schema

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose up --build -d

logs:
	docker compose logs -f

shell:
	docker compose exec web sh

test:
	docker compose exec web uv run pytest

migrate:
	docker compose exec web uv run python manage.py migrate

makemigrations:
	docker compose exec web uv run python manage.py makemigrations

superuser:
	docker compose exec web uv run python manage.py createsuperuser

lint:
	uv run ruff check .

format:
	uv run ruff format .

fix:
	uv run ruff check . --fix

check:
	uv run ruff check .
	uv run ruff format . --check

pre-commit:
	uv run pre-commit run --all-files

schema:
	uv run python manage.py spectacular --file schema.yml
