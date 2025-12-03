# CMatrix Backend

AI-powered cybersecurity agent system built with **FastAPI**, **LangGraph**, and **HuggingFace**.

## 🏗️ Architecture

The backend follows a clean, layered architecture designed for scalability and maintainability.

```
backend/
├── app/
│   ├── api/            # HTTP endpoints (v1)
│   ├── core/           # Config, logging, security
│   ├── services/       # Business logic (LLM, Orchestrator)
│   ├── agents/         # Specialized agents (Network, Web, etc.)
│   ├── tools/          # Tool implementations & registry
│   ├── models/         # Pydantic data models
│   └── utils/          # Helpers & audit logging
├── data/               # Data files (demos.json, auth_config.json)
├── logs/               # Application & audit logs
├── scripts/            # Management scripts
├── tests/              # Pytest suite
└── .old_structure_backup/ # Backup of pre-refactor files
```

## 🚀 Quick Start

### 1. Setup
Run the automated setup script to create the virtual environment and install dependencies:
```bash
./setup.sh
```

### 2. Configuration
Copy the example environment file and add your API keys:
```bash
cp .env.example .env
nano .env
# Set HUGGINGFACE_API_KEY=your_key_here
```

### 3. Run Application
**Development (Hot Reload):**
```bash
./scripts/dev.sh
# OR: uvicorn app.main:app --reload
```

**Production:**
```bash
./scripts/start.sh
# OR: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Docker:**
```bash
docker build -t cmatrix-backend .
docker run -p 8000:8000 --env-file .env cmatrix-backend
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/health` | System health check |
| `POST` | `/api/v1/chat` | Standard chat interface |
| `POST` | `/api/v1/chat/stream` | Streaming chat interface |
| `GET` | `/docs` | Swagger UI documentation |
| `GET` | `/redoc` | ReDoc documentation |

## 🛠️ Development

**Testing:**
```bash
pytest                  # Run all tests
pytest --cov=app tests/ # Run with coverage
```

**Code Quality:**
```bash
# Linting and formatting (Ruff replaces black, flake8, isort)
ruff check .            # Check for issues
ruff check --fix .      # Auto-fix issues
ruff format .           # Format code

# Type checking
mypy app/               # Check types

# Run all checks (recommended before commit)
ruff check --fix . && ruff format . && mypy app/
```

**Pre-commit Hooks (Automated):**
```bash
# Install hooks (one-time setup)
pre-commit install

# Hooks will run automatically on git commit
# To run manually on all files:
pre-commit run --all-files

# Update hooks to latest versions:
pre-commit autoupdate
```

## 🔐 Security Features
- **Environment Config**: No hardcoded secrets.
- **Input Validation**: Strict Pydantic models.
- **Command Whitelisting**: Restricted execution environment.
- **Audit Logging**: Comprehensive operation tracking in `logs/audit_logs/`.

## 📚 Documentation

For comprehensive code quality, linting, and development workflows, see:
- **[Code Quality Guide](../docs/CODE_QUALITY_GUIDE.md)** - Complete guide to linting, formatting, and development workflows
- **[Makefile Commands](Makefile)** - Run `make help` for available commands
