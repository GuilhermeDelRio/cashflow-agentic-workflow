.PHONY: help install install-dev sync clean test lint format type-check run dev graph-ui telegram all

help:
	@echo "Cashflow Agentic Workflow - Available Commands"
	@echo "=============================================="
	@echo "Setup:"
	@echo "  make install      - Install dependencies"
	@echo "  make install-dev  - Install dev dependencies"
	@echo "  make sync         - Sync all dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make run          - Run the main application"
	@echo "  make dev          - Run LangGraph dev UI"
	@echo "  make graph-ui     - Alias for 'make dev'"
	@echo "  make telegram     - Run Telegram bot"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint         - Run linter (ruff check)"
	@echo "  make format       - Format code (ruff format)"
	@echo "  make type-check   - Run type checker (mypy)"
	@echo "  make test         - Run tests (pytest)"
	@echo "  make all          - Run format, lint, type-check, and test"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean        - Remove cache files and __pycache__"
	@echo ""

install:
	@echo "Installing dependencies..."
	uv sync

install-dev:
	@echo "Installing dev dependencies..."
	uv sync --group dev

sync:
	@echo "Syncing all dependencies..."
	uv sync --all-groups

clean:
	@echo "Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cache files removed!"

test:
	@echo "Running tests..."
	uv run pytest

lint:
	@echo "Running linter..."
	uv run ruff check .

format:
	@echo "Formatting code..."
	uv run ruff format .

type-check:
	@echo "Running type checker..."
	uv run mypy .

run:
	@echo "Running main application..."
	uv run python main.py

dev:
	@echo "Starting LangGraph dev UI..."
	uv run langgraph dev

graph-ui: dev

telegram:
	@echo "Starting Telegram bot..."
	uv run python telegram_main.py

all: format lint type-check test
	@echo "All checks passed!"
