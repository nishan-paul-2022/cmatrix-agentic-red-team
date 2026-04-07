# CMatrix

<div align="center">

![CMatrix Logo](app-frontend/public/icon.svg)

**AI-Powered Multi-Agent Security Orchestration Platform**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/next.js-16.0-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2.45-purple)](https://github.com/langchain-ai/langgraph)

[Features](#features) • [Quick Start](#quick-start) • [Documentation](#documentation) • [Contributing](#contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Docker Setup (Recommended)](#docker-setup-recommended)
  - [Manual Setup](#manual-setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## 🎯 Overview

**CMatrix** is an advanced AI-powered security orchestration platform that leverages multi-agent architecture to automate security assessments, vulnerability scanning, and threat intelligence gathering. Built with LangGraph and FastAPI, CMatrix provides intelligent, autonomous security operations through specialized AI agents.

### What Makes CMatrix Different?

- 🤖 **Agentic AI Architecture**: Powered by LangGraph for sophisticated reasoning and tool orchestration
- 🔄 **Persistent Workflows**: Background job processing with state checkpointing for long-running security scans
- 🧠 **Vector Memory**: Qdrant-powered knowledge base for contextual awareness across sessions
- 🛡️ **Security-First**: Human-in-the-loop approvals for dangerous operations
- 📊 **Real-Time Streaming**: Server-Sent Events (SSE) for live scan updates
- 🎨 **Modern UI**: Beautiful Next.js frontend with real-time chat interface

---

## ✨ Features

### Core Capabilities

- **🔍 Network Security Scanning**
  - Port scanning and service detection
  - Network topology discovery
  - SSL/TLS certificate validation

- **🌐 Web Application Security**
  - HTTP/HTTPS endpoint validation
  - Security header analysis
  - Authentication mechanism testing

- **🔐 Vulnerability Intelligence**
  - CVE database search and analysis
  - Threat intelligence gathering
  - Security advisory tracking

- **⚙️ Configuration Compliance**
  - Security configuration auditing
  - Compliance checking
  - Best practice validation

- **🔧 Command Execution**
  - Secure terminal command execution
  - Approval-based dangerous operations
  - Command output streaming

### AI Agent Features

- **Reasoning & Planning**: ReAct (Reasoning + Acting) pattern for intelligent decision-making
- **Tool Orchestration**: 22+ specialized security tools across 7 agent categories
- **Memory Management**: Short-term conversation memory + long-term vector storage
- **State Persistence**: Checkpoint-based workflow resumption
- **Background Processing**: Celery-based job queue for long-running tasks

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                      │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   Chat UI   │  │  Job Status  │  │  Approval Gates  │  │
│  └─────────────┘  └──────────────┘  └──────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ SSE Streaming / REST API
┌────────────────────────┴────────────────────────────────────┐
│                   Backend (FastAPI)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           LangGraph Orchestrator                     │  │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐    │  │
│  │  │Network │  │  Web   │  │ Vuln   │  │Command │    │  │
│  │  │ Agent  │  │ Agent  │  │ Agent  │  │ Agent  │    │  │
│  │  └────────┘  └────────┘  └────────┘  └────────┘    │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼──────┐  ┌──────▼──────┐  ┌─────▼──────┐
│  PostgreSQL  │  │    Redis    │  │   Qdrant   │
│  (State +    │  │  (Jobs +    │  │  (Vector   │
│   Users)     │  │   Cache)    │  │   Memory)  │
└──────────────┘  └─────────────┘  └────────────┘
```

### Technology Stack

**Backend:**
- Python 3.12+
- FastAPI 0.115 (async web framework)
- LangChain 0.3.7 + LangGraph 0.2.45 (AI orchestration)
- SQLAlchemy 2.0 (ORM)
- Celery 5.4 (background jobs)
- Alembic (database migrations)

**Frontend:**
- Next.js 16.0 (React framework)
- TypeScript 5+
- Tailwind CSS 4.1
- Radix UI components
- React Markdown

**Databases:**
- PostgreSQL 16 (primary database + checkpointing)
- Redis 7 (job queue + caching)
- Qdrant (vector database for embeddings)

---

## 📦 Prerequisites

### Local Environment Configuration

When running the backend locally (e.g., using `make run`) while using Docker for infrastructure services (Postgres, Redis, Qdrant), you must ensure your local system can resolve the unified service hostnames.

Run the following command on your local machine:

```bash
echo "127.0.0.1 cmatrix-postgres cmatrix-redis cmatrix-qdrant" | sudo tee -a /etc/hosts
```

This ensures that `DATABASE_URL`, `CELERY_BROKER_URL`, and other service links in your `.env` file work identically both locally and in the Docker-based production environment.

### API Keys (Optional)

CMatrix supports multiple LLM providers. Once you've signed in, you can configure these keys in **Settings > LLM Profiles**.

- **Google Gemini API** (recommended for free tier)
- **OpenAI API** (GPT-4, GPT-3.5)
- **Anthropic API** (Claude)
- **Ollama** (local LLMs)

---

## 🚀 Installation

### Docker Setup (Recommended)

This is the easiest way to get started with CMatrix.

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/cmatrix.git
cd cmatrix
```

#### 2. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your preferred editor
nano .env
```

**Minimum required configuration:**

```env
# Database (auto-configured in Docker)
DATABASE_URL=postgresql+asyncpg://cmatrix:cmatrix@postgres:5432/cmatrix

# Security - CHANGE THIS!
SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars

# LLM Configuration (Set up in UI)
# After signing in, go to Settings -> LLM Profiles to add your API keys.
# Supports: Google Gemini, OpenAI, Claude, Ollama.

# Option 2: OpenAI
# OPENAI_API_KEY=your_openai_api_key_here

# Option 3: Ollama (local)
# OLLAMA_BASE_URL=http://localhost:11434
```

#### 3. Start All Services

```bash
# Start all services in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Check service health
docker-compose ps
```

#### 4. Initialize the Database

```bash
# Run database migrations
docker-compose exec backend alembic upgrade head

# (Optional) Initialize knowledge base
docker-compose exec backend python init_knowledge_base.py
```

#### 5. Access the Application

- **Frontend**: http://localhost:3011
- **Backend API**: http://localhost:3012
- **API Documentation**: http://localhost:3012/docs
- **Qdrant Dashboard**: http://localhost:6333/dashboard

#### 6. Create Your First User

Visit http://localhost:3011 and click "Sign Up" to create an account.

---

### Manual Setup

For development or if you prefer not to use Docker.

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit with your settings

# Start PostgreSQL (if not using Docker)
# Install PostgreSQL 16 from https://www.postgresql.org/download/

# Create database
createdb cmatrix

# Run migrations
alembic upgrade head

# Start Redis (required for Celery)
redis-server

# Start Qdrant (in another terminal)
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage \
    qdrant/qdrant

# Initialize knowledge base
python init_knowledge_base.py

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 3012

# In a new terminal, start Celery worker
celery -A app.worker worker --loglevel=info
```

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Configure environment
echo "NEXT_PUBLIC_API_URL=http://localhost:3012" > .env.local

# Start development server
npm run dev
```

Access the application at http://localhost:3011

---

## ⚙️ Configuration

### Environment Variables

#### Application Settings

```env
APP_NAME=CMatrix
APP_VERSION=0.0.1
DEBUG=false
LOG_LEVEL=INFO
```

#### Database Configuration

```env
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database
```

#### Security Settings

```env
SECRET_KEY=your-secret-key-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days
```

#### Vector Database (Qdrant)

```env
QDRANT_URL=http://localhost:6333
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=cmatrix_memory
```

#### Embeddings

```env
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DEVICE=cpu  # or 'cuda' for GPU
```

#### Command Execution

```env
COMMAND_TIMEOUT=30
ENABLE_SUDO=false  # Set to true only if needed
```

#### Celery (Background Jobs)

```env
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
```

### LLM Configuration

Create `llm_config.json` in the backend directory:

```json
{
  "provider": "google",
  "model": "gemini-2.0-flash-exp",
  "temperature": 0.7,
  "max_tokens": 8192,
  "streaming": true
}
```

Supported providers: `google`, `openai`, `anthropic`, `ollama`

---

## 💻 Usage

### Basic Workflow

1. **Sign Up / Login**: Create an account or login at http://localhost:3000

2. **Start a Conversation**: Click "New Chat" to start interacting with the AI agent

3. **Security Scanning Examples**:

   ```
   User: Scan 192.168.1.1 for open ports

   User: Check if example.com has proper SSL configuration

   User: Search for CVEs related to Apache 2.4

   User: Analyze the security headers of https://example.com
   ```

4. **Approve Dangerous Operations**: When the agent requests to execute potentially dangerous commands, you'll see an approval dialog

5. **View Job Status**: Long-running scans run in the background. Monitor progress in real-time

### Advanced Features

#### Using the Knowledge Base

```
User: Remember that server-01 is our production database server

User: What do you know about server-01?
```

#### Multi-Step Security Assessment

```
User: Perform a comprehensive security assessment of 10.0.0.5:
1. Scan for open ports
2. Identify running services
3. Check for known vulnerabilities
4. Provide a security report
```

---

## 🛠️ Development

### Project Structure

```
cmatrix/
├── backend/
│   ├── app/
│   │   ├── agents/           # AI agent definitions
│   │   │   └── specialized/  # Network, Web, Vuln agents
│   │   ├── api/              # FastAPI routes
│   │   ├── core/             # Config, security, database
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   ├── tools/            # LangChain tools
│   │   └── worker.py         # Celery worker
│   ├── migrations/           # Alembic migrations
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js app router
│   │   ├── components/       # React components
│   │   ├── hooks/            # Custom React hooks
│   │   ├── lib/              # Utilities
│   │   └── types/            # TypeScript types
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml        # Docker orchestration
├── .env.example              # Environment template
└── README.md
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# With coverage
pytest --cov=app --cov-report=html

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting
cd backend
black .                    # Format code
flake8 .                   # Lint
mypy app/                  # Type checking

# Frontend linting
cd frontend
npm run lint
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

### Adding New Tools

1. Create tool function in `backend/app/tools/`
2. Register in appropriate agent file in `backend/app/agents/specialized/`
3. Update agent prompts to include new tool
4. Test tool execution

Example:

```python
# backend/app/tools/my_tool.py
from langchain.tools import StructuredTool

def my_security_tool(target: str) -> str:
    """
    Description of what this tool does.

    Args:
        target: The target to scan

    Returns:
        Scan results as string
    """
    # Implementation
    return "Results"

# Register in agent
MY_TOOL = StructuredTool.from_function(
    func=my_security_tool,
    name="my_security_tool",
    description="Tool description for LLM"
)
```

---

## 🧪 Testing

### Health Checks

```bash
# Check all services
./health_check.sh

# Check specific service
curl http://localhost:3012/api/v1/health
```

### Test Scripts

```bash
# Test knowledge base
./test_knowledge_base.sh

# Test memory functionality
./test_memory_demo.sh

# Test backend API
python backend/test_backend.py
```

---

## 🚢 Deployment

### Production Deployment

#### Using Docker Compose (Production)

```bash
# Use production compose file
docker-compose -f docker-compose.release.yml up -d

# Or use the deployment script
./docker.sh release
```

#### Environment Hardening

1. **Change default credentials**:
   ```env
   SECRET_KEY=<generate-strong-random-key>
   POSTGRES_PASSWORD=<strong-password>
   ```

2. **Disable debug mode**:
   ```env
   DEBUG=false
   LOG_LEVEL=WARNING
   ```

3. **Enable HTTPS**: Configure reverse proxy (nginx/Caddy)

4. **Restrict command execution**:
   ```env
   ENABLE_SUDO=false
   COMMAND_TIMEOUT=30
   ```

#### Scaling

```bash
# Scale Celery workers
docker-compose up -d --scale worker=4

# Scale backend instances (with load balancer)
docker-compose up -d --scale backend=3
```

### Monitoring

- **Logs**: `docker-compose logs -f [service]`
- **Metrics**: Backend logs in `backend/logs/`
- **Health**: http://localhost:3012/api/v1/health

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Getting Started

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Run tests**:
   ```bash
   pytest
   npm test
   ```
5. **Commit with conventional commits**:
   ```bash
   git commit -m "feat: add amazing feature"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Contribution Guidelines

- **Code Style**: Follow PEP 8 (Python) and ESLint rules (TypeScript)
- **Tests**: Add tests for new features
- **Documentation**: Update README and code comments
- **Commits**: Use [Conventional Commits](https://www.conventionalcommits.org/)
- **Issues**: Check existing issues before creating new ones

### Development Workflow

1. **Pick an issue** or create one describing your feature
2. **Discuss approach** in the issue before major changes
3. **Write tests** alongside your code
4. **Update documentation** if needed
5. **Request review** from maintainers

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

---

## 🐛 Troubleshooting

### Common Issues

#### Docker Issues

**Problem**: Services won't start
```bash
# Check logs
docker-compose logs

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**Problem**: Port already in use
```bash
# Find process using port
lsof -i :3011  # or :3012, :6379, etc.

# Kill process or change port in docker-compose.yml
```

#### Database Issues

**Problem**: Migration errors
```bash
# Reset database (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d postgres
docker-compose exec backend alembic upgrade head
```

**Problem**: Connection refused
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check connection string in .env
# Ensure DATABASE_URL matches docker-compose.yml
```

#### Celery Worker Issues

**Problem**: Jobs not processing
```bash
# Check worker logs
docker-compose logs worker

# Restart worker
docker-compose restart worker

# Check Redis connection
docker-compose exec backend python check_redis.py
```

#### Frontend Issues

**Problem**: API connection errors
```bash
# Check NEXT_PUBLIC_API_URL in .env.local
# Ensure backend is running on correct port
curl http://localhost:3012/api/v1/health
```

**Problem**: Build errors
```bash
# Clear Next.js cache
cd frontend
rm -rf .next
npm run build
```

#### LLM Issues

**Problem**: Agent not responding
```bash
# Check LLM configuration
cat backend/llm_config.json

# Verify API key is set in the UI / Database
# Profiles can be checked at http://localhost:3012/api/v1/profiles

# Test LLM setup
docker-compose exec backend python setup_llm.py
```

### Getting Help

- **Documentation**: Check this README and code comments
- **Issues**: Search [existing issues](https://github.com/yourusername/cmatrix/issues)
- **Discussions**: Join [GitHub Discussions](https://github.com/yourusername/cmatrix/discussions)
- **Logs**: Always include relevant logs when reporting issues

---

## 📚 Additional Resources

### Documentation

- [Architecture Overview](docs/architecture.md)
- [API Documentation](http://localhost:3012/docs) (when running)
- [Agentic Implementation Roadmap](AGENTIC_IMPLEMENTATION_ROADMAP.md)

### Related Projects

- [LangChain](https://github.com/langchain-ai/langchain)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/)

### Learning Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Next.js Learn](https://nextjs.org/learn)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [LangChain](https://github.com/langchain-ai/langchain) and [LangGraph](https://github.com/langchain-ai/langgraph)
- UI components from [Radix UI](https://www.radix-ui.com/)
- Inspired by modern AI agent architectures and security automation tools

---

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/cmatrix/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/cmatrix/discussions)
- **Email**: your.email@example.com

---

<div align="center">

**Made with ❤️ by the CMatrix Team**

[⬆ Back to Top](#cmatrix)

</div>
