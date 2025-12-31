.PHONY: help install dev build lint format typecheck quality clean

# Default target
help:
	@echo "CMatrix Frontend - Development Commands"
	@echo "========================================"
	@echo ""
	@echo "Setup:"
	@echo "  make install        Install dependencies"
	@echo "  make dev            Start development server"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint           Run ESLint"
	@echo "  make lint-fix       Run ESLint with auto-fix"
	@echo "  make format         Format code with Prettier"
	@echo "  make format-check   Check formatting without changes"
	@echo "  make typecheck      Run TypeScript type checker"
	@echo "  make quality        Run all quality checks (lint + format + typecheck)"
	@echo ""
	@echo "Build:"
	@echo "  make build          Build for production"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          Remove build artifacts and cache"

# Installation
install:
	npm install

# Development
dev:
	npm run dev

# Build
build:
	npm run build

# Code quality
lint:
	npm run lint

lint-fix:
	npm run lint:fix

format:
	npm run format

format-check:
	npm run format:check

typecheck:
	npm run typecheck

quality: lint-fix format typecheck
	@echo "✅ All quality checks passed!"

# Cleanup
clean:
	@echo "🧹 Cleaning up..."
	rm -rf .next
	rm -rf out
	rm -rf node_modules/.cache
	rm -rf tsconfig.tsbuildinfo
	@echo "✅ Cleanup complete!"
