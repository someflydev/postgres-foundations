.PHONY: install fmt lint test cli

install:
	uv sync

fmt:
	uv run ruff format .

lint:
	uv run ruff check .

test:
	uv run pytest

cli:
	uv run pgfound
