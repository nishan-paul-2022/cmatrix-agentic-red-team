.PHONY: help install dev build quality clean pre-commit

# Default target
help:
	@echo "CMatrix - Full Stack Development Commands"
	@echo "=========================================="
	@echo ""
	@echo "🚀 Quick Start:"
	@echo "  make install        Install all dependencies (frontend + backend)"
	@echo "  make dev            Start both frontend and backend dev servers"
	@echo "  make quality        Run all quality checks (frontend + backend)"
	@echo ""
	@echo "📦 Setup:"
	@echo "  make install-frontend   Install frontend dependencies"
	@echo "  make install-backend    Install backend dependencies"
	@echo "  make pre-commit         Install pre-commit hooks"
	@echo ""
	@echo "🔧 Development:"
	@echo "  make dev-frontend       Start frontend dev server"
	@echo "  make dev-backend        Start backend dev server"
	@echo ""
	@echo "✨ Code Quality:"
	@echo "  make quality-frontend   Run frontend quality checks"
	@echo "  make quality-backend    Run backend quality checks"
	@echo "  make lint               Run linters (frontend + backend)"
	@echo "  make format             Format code (frontend + backend)"
	@echo "  make typecheck          Run type checkers (frontend + backend)"
	@echo ""
	@echo "🏗️  Build:"
	@echo "  make build-frontend     Build frontend for production"
	@echo "  make build-backend      Build backend (if applicable)"
	@echo ""
	@echo "🧹 Cleanup:"
	@echo "  make clean              Clean all build artifacts and caches"
	@echo "  make clean-frontend     Clean frontend artifacts"
	@echo "  make clean-backend      Clean backend artifacts"

# Installation
install: install-frontend install-backend pre-commit
	@echo "✅ All dependencies installed!"

install-frontend:
	@echo "📦 Installing frontend dependencies..."
	cd frontend && npm install

install-backend:
	@echo "📦 Installing backend dependencies..."
	cd backend && pip install -r requirements.txt

# Pre-commit hooks
pre-commit:
	@echo "🪝 Installing pre-commit hooks..."
	cd backend && source venv/bin/activate && pre-commit install

# Development servers
dev:
	@echo "🚀 Starting development servers..."
	@echo "Run 'make dev-frontend' and 'make dev-backend' in separate terminals"

dev-frontend:
	@echo "🚀 Starting frontend dev server..."
	cd frontend && npm run dev

dev-backend:
	@echo "🚀 Starting backend dev server..."
	cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Code quality
quality: quality-frontend quality-backend
	@echo "✅ All quality checks passed!"

quality-frontend:
	@echo "✨ Running frontend quality checks..."
	cd frontend && npm run quality

quality-backend:
	@echo "✨ Running backend quality checks..."
	cd backend && make quality

lint:
	@echo "🔍 Running linters..."
	cd frontend && npm run lint:fix
	cd backend && make lint-fix

format:
	@echo "✨ Formatting code..."
	cd frontend && npm run format
	cd backend && make format

typecheck:
	@echo "🔎 Running type checkers..."
	cd frontend && npm run typecheck
	cd backend && make typecheck

# Build
build: build-frontend
	@echo "✅ Build complete!"

build-frontend:
	@echo "🏗️  Building frontend..."
	cd frontend && npm run build

build-backend:
	@echo "🏗️  Backend doesn't require build step"

# Cleanup
clean: clean-frontend clean-backend
	@echo "✅ Cleanup complete!"

clean-frontend:
	@echo "🧹 Cleaning frontend..."
	cd frontend && make clean

clean-backend:
	@echo "🧹 Cleaning backend..."
	cd backend && make clean

# Testing
test:
	@echo "🧪 Running tests..."
	cd backend && make test

test-frontend:
	@echo "🧪 Frontend tests not configured yet"

test-backend:
	@echo "🧪 Running backend tests..."
	cd backend && make test
