.PHONY: help install dev test lint format typecheck quality clean pre-commit

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
	@echo "  make quality        Run all quality checks (lint + format + typecheck)"
	@echo ""
	@echo "Testing:"
	@echo "  make test           Run tests"
	@echo "  make test-cov       Run tests with coverage"
	@echo ""
	@echo "Pre-commit:"
	@echo "  make pre-commit     Install pre-commit hooks"
	@echo "  make pre-commit-run Run pre-commit on all files"
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
	ruff check .

lint-fix:
	@echo "🔧 Running Ruff linter with auto-fix..."
	ruff check --fix .

format:
	@echo "✨ Formatting code with Ruff..."
	ruff format .

format-check:
	@echo "🔍 Checking code formatting..."
	ruff format --check .

typecheck:
	@echo "🔎 Running mypy type checker..."
	mypy app/

quality: lint-fix format typecheck
	@echo "✅ All quality checks passed!"

# Testing
test:
	@echo "🧪 Running tests..."
	pytest

test-cov:
	@echo "🧪 Running tests with coverage..."
	pytest --cov=app tests/ --cov-report=term-missing

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
	@echo "🚀 Starting development server..."
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

run-prod:
	@echo "🚀 Starting production server..."
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
