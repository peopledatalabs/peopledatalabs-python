.PHONY: install test lint format clean help

help:
	@echo "Available commands:"
	@echo "  install    : Install dependencies"
	@echo "  test       : Run tests"
	@echo "  lint       : Run linting (Ruff)"
	@echo "  format     : Run formatting (Ruff)"
	@echo "  clean      : Remove temporary files"

install:
	poetry install
	poetry run pre-commit install

test:
	poetry run pytest

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

clean:
	rm -rf .pytest_cache .ruff_cache .venv build dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
