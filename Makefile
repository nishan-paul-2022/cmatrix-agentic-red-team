.PHONY: help install dev build quality clean pre-commit check paper clean-paper

# Global Environment Variables
VENV ?= ./venv
ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
LATEXMK := latexmk -f -cd -pdf -pdflatex="pdflatex -interaction=nonstopmode -halt-on-error %O %S"

# Default target
help:
	@echo "CMatrix - Full Stack Development Commands"
	@echo "=========================================="
	@echo ""
	@echo "🚀 Quick Start:"
	@echo "  make install        Install all dependencies (app-frontend + app-backend)"
	@echo "  make dev            Start both app-frontend and app-backend dev servers"
	@echo "  make quality        Run all quality checks (app-frontend + app-backend)"
	@echo ""
	@echo "📦 Setup:"
	@echo "  make install-app-frontend   Install app-frontend dependencies"
	@echo "  make install-app-backend    Install app-backend dependencies"
	@echo "  make pre-commit         Install pre-commit hooks"
	@echo ""
	@echo "🔧 Development:"
	@echo "  make dev-app-frontend       Start app-frontend dev server"
	@echo "  make dev-app-backend        Start app-backend dev server"
	@echo ""
	@echo "✨ Code Quality:"
	@echo "  make quality-app-frontend   Run app-frontend quality checks"
	@echo "  make quality-app-backend    Run app-backend quality checks"
	@echo "  make lint               Run linters (app-frontend + app-backend)"
	@echo "  make format             Format code (app-frontend + app-backend)"
	@echo "  make typecheck          Run type checkers (app-frontend + app-backend)"
	@echo ""
	@echo "🏗️  Build:"
	@echo "  make build-app-frontend     Build app-frontend for production"
	@echo "  make build-app-backend      Build app-backend (if applicable)"
	@echo "  make paper              Build the Research Paper PDF"
	@echo ""
	@echo "🧹 Cleanup:"
	@echo "  make clean              Clean all build artifacts and caches"
	@echo "  make clean-app-frontend     Clean app-frontend artifacts"
	@echo "  make clean-app-backend      Clean app-backend artifacts"

# Installation
install: install-app-frontend install-app-backend pre-commit
	@echo "✅ All dependencies installed!"

install-app-frontend:
	@echo "📦 Installing app-frontend dependencies..."
	cd app-frontend && npm install

install-app-backend:
	@echo "📦 Installing app-backend dependencies..."
	cd app-backend && pip install -r requirements.txt

# Pre-commit hooks
pre-commit:
	@echo "🪝 Installing husky pre-commit hooks..."
	npm run prepare

# Development servers
dev:
	@echo "🚀 Starting development servers..."
	@echo "Run 'make dev-app-frontend' and 'make dev-app-backend' in separate terminals"

dev-app-frontend:
	@echo "🚀 Starting app-frontend dev server..."
	cd app-frontend && npm run dev

dev-app-backend:
	@echo "🚀 Starting app-backend dev server..."
	cd app-backend && source venv/bin/activate && uvicorn app.main:app --port $${BACKEND_PORT} --reload

# Code quality
quality: quality-app-frontend quality-app-backend
	@echo "✅ All quality checks passed!"

quality-app-frontend:
	@echo "✨ Running app-frontend quality checks..."
	cd app-frontend && npm run quality

quality-app-backend:
	@echo "✨ Running app-backend quality checks..."
	cd app-backend && $(MAKE) quality VENV=$(VENV)

lint:
	@echo "🔍 Running linters..."
	cd app-frontend && npm run lint:fix
	cd app-backend && $(MAKE) lint-fix VENV=$(VENV)

format:
	@echo "✨ Formatting code..."
	cd app-frontend && npm run format
	cd app-backend && $(MAKE) format VENV=$(VENV)

typecheck:
	@echo "🔎 Running type checkers..."
	cd app-frontend && npm run typecheck
	cd app-backend && $(MAKE) typecheck VENV=$(VENV)

# Build
build: build-app-frontend
	@echo "✅ Build complete!"

build-app-frontend:
	@echo "🏗️  Building app-frontend..."
	cd app-frontend && npm run build

build-app-backend:
	@echo "🏗️  Backend doesn't require build step"

# Paper Build Directories
PAPER_DIR_01 := research/paper-01-red-teaming
PAPER_DIR_02 := research/paper-02-hitl-safety
PAPER_DIR_03 := research/paper-03-agent-reasoning
PAPER_DIR_04 := research/paper-04-vulnerability-intelligence
PAPER_DIR_05 := research/paper-05-model-orchestration

paper: paper-01 paper-02 paper-03 paper-04 paper-05
	@echo "✅ All papers built successfully!"

paper-01:
	@echo "🏗️  Building Research Paper: 01-red-teaming..."
	$(LATEXMK) -jobname=main -outdir="." -auxdir="build" $(PAPER_DIR_01)/content/main.tex
	mv $(PAPER_DIR_01)/content/main.pdf $(PAPER_DIR_01)/paper.pdf
	rm -rf $(PAPER_DIR_01)/content/build

paper-02:
	@echo "🏗️  Building Research Paper: 02-hitl-safety..."
	$(LATEXMK) -jobname=main -outdir="." -auxdir="build" $(PAPER_DIR_02)/content/main.tex
	mv $(PAPER_DIR_02)/content/main.pdf $(PAPER_DIR_02)/paper.pdf
	rm -rf $(PAPER_DIR_02)/content/build

paper-03:
	@echo "🏗️  Building Research Paper: 03-agent-reasoning..."
	$(LATEXMK) -jobname=main -outdir="." -auxdir="build" $(PAPER_DIR_03)/content/main.tex
	mv $(PAPER_DIR_03)/content/main.pdf $(PAPER_DIR_03)/paper.pdf
	rm -rf $(PAPER_DIR_03)/content/build

paper-04:
	@echo "🏗️  Building Research Paper: 04-vulnerability-intelligence..."
	$(LATEXMK) -jobname=main -outdir="." -auxdir="build" $(PAPER_DIR_04)/content/main.tex
	mv $(PAPER_DIR_04)/content/main.pdf $(PAPER_DIR_04)/paper.pdf
	rm -rf $(PAPER_DIR_04)/content/build

paper-05:
	@echo "🏗️  Building Research Paper: 05-model-orchestration..."
	$(LATEXMK) -jobname=main -outdir="." -auxdir="build" $(PAPER_DIR_05)/content/main.tex
	mv $(PAPER_DIR_05)/content/main.pdf $(PAPER_DIR_05)/paper.pdf
	rm -rf $(PAPER_DIR_05)/content/build

# Cleanup
clean: clean-app-frontend clean-app-backend clean-paper
	@echo "✅ Cleanup complete!"

clean-app-frontend:
	@echo "🧹 Cleaning app-frontend..."
	cd app-frontend && make clean

clean-app-backend:
	@echo "🧹 Cleaning app-backend..."
	cd app-backend && make clean

clean-paper:
	@echo "🧹 Cleaning Research Paper artifacts..."
	rm -rf research/paper-*/*.pdf research/paper-*/content/build

# Testing
test:
	@echo "🧪 Running tests..."
	cd app-backend && $(MAKE) test VENV=$(VENV)

test-app-frontend:
	@echo "🧪 Frontend tests not configured yet"

test-app-backend:
	@echo "🧪 Running app-backend tests..."
	cd app-backend && $(MAKE) test VENV=$(VENV)

# Unified Check (One-Click Verification)
check: quality test-app-backend
	@echo "✅ All quality checks and tests passed! You are ready to commit."
