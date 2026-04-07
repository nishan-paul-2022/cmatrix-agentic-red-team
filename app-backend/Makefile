.PHONY: help install dev test lint format typecheck quality clean pre-commit check

# Define tool paths
VENV ?= ./venv
ifneq ($(VENV),)
    BIN := $(VENV)/bin/
else
    BIN :=
endif

RUFF := $(BIN)ruff
MYPY := $(BIN)mypy
BANDIT := $(BIN)bandit
PYTEST := $(BIN)pytest

# Default target
help:
	@echo "CMatrix Backend - Development Commands"
	@echo "======================================"
	@echo ""
	@echo "Setup:"
	@echo "  make install        Install production dependencies"
	@echo "  make dev            Install development dependencies"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint           Run linter (ruff check)"
	@echo "  make format         Format code (ruff format)"
	@echo "  make typecheck      Run type checker (mypy)"
	@echo "  make quality        Run all quality checks (lint + format + typecheck + bandit)"
	@echo ""
	@echo "Testing:"
	@echo "  make test           Run tests"
	@echo "  make check          Run quality + test"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          Remove cache files"

# Installation
install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"

# Code quality
lint:
	@echo "🔍 Running Ruff linter..."
	$(RUFF) check .

lint-fix:
	@echo "🔧 Running Ruff linter with auto-fix..."
	$(RUFF) check --fix .

format:
	@echo "✨ Formatting code with Ruff..."
	$(RUFF) format .

format-check:
	@echo "🔍 Checking code formatting..."
	$(RUFF) format --check .

typecheck:
	@echo "🔎 Running mypy type checker..."
	$(MYPY) app/

bandit:
	@echo "🛡️  Running bandit security scan..."
	$(BANDIT) -r app/ -c pyproject.toml

quality: lint-fix format typecheck bandit
	@echo "✅ All quality checks passed!"

check: quality test
	@echo "✅ Backend check complete!"

# Testing
test:
	@echo "🧪 Running tests..."
	cd $(CURDIR) && export PYTHONPATH=. && $(VENV)/bin/pytest tests app/tests

test-cov:
	@echo "🧪 Running tests with coverage..."
	$(PYTEST) --cov=app tests/ --cov-report=term-missing

# Pre-commit
pre-commit:
	@echo "🪝 Installing pre-commit hooks..."
	pre-commit install

pre-commit-run:
	@echo "🪝 Running pre-commit on all files..."
	pre-commit run --all-files

# Cleanup
clean:
	@echo "🧹 Cleaning up cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete!"

# Development server
run:
	@echo "🚀 Starting development server with auto-migrations..."
	./scripts/migrate.sh --host 0.0.0.0 --port 3012 --reload

run-prod:
	@echo "🚀 Starting production server with auto-migrations..."
	./scripts/migrate.sh --host 0.0.0.0 --port 3012 --workers 4
