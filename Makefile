.PHONY: install fmt lint test test-integration test-all cli lab-up lab-down lab-nuke lab-psql lab-logs lab-sandbox-up

COMPOSE := docker compose -f docker/docker-compose.yml

install:
	uv sync

fmt:
	uv run ruff format .

lint:
	uv run ruff check .
	scripts/readme-lint.sh

test:
	uv run pytest

test-integration:
	uv run pytest tests/integration

test-all:
	uv run pytest

cli:
	uv run pgfound

lab-up:
	$(COMPOSE) up -d pg

lab-down:
	$(COMPOSE) down

lab-nuke:
	$(COMPOSE) down -v

lab-psql:
	$(COMPOSE) exec pg psql -U pgfound

lab-logs:
	$(COMPOSE) logs -f pg

lab-sandbox-up:
	$(COMPOSE) --profile sandbox up -d
