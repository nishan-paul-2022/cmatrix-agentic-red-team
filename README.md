<div align="center">
  <img src="app-frontend/public/icon.svg" alt="CMatrix Logo" width="120" height="120" />
  <h1>CMatrix</h1>
  <p>AI-Powered Multi-Agent Security Orchestration & VAPT Platform</p>

  <a href="https://cmatrix.kaiofficial.xyz" target="_blank">
    <img src="https://img.shields.io/badge/Live_App-cmatrix.kaiofficial.xyz-0070f3?style=for-the-badge&logo=next.js&logoColor=white" alt="Live App" />
  </a>
</div>

CMatrix is an advanced, AI-powered security orchestration platform utilizing a multi-agent architecture to automate security assessments, vulnerability scanning, and threat intelligence. Powered by **LangGraph** and **FastAPI** with a **Next.js** frontend, CMatrix acts as an autonomous security operations center.

---

## ✨ Core Features

- 🤖 **Agentic AI Architecture**: Powered by LangGraph for sophisticated tool orchestration and reasoning.
- 🔍 **Network & Web Scanning**: In-depth port scanning, topology discovery, and web vulnerability analysis.
- 🧠 **Vector Memory**: Qdrant-powered long-term contextual memory across scanning sessions.
- 🛡️ **Human-in-the-Loop**: Approval gates for safe execution of dangerous operations and terminal commands.
- 🔄 **Stateful Workflows**: Checkpoint-based workflow resumption and Celery background task processing.
- 🎨 **Modern Interface**: A stunning Next.js frontend with real-time SSE streaming for live updates.
- 🔐 **LLM Agnostic**: Seamlessly integrate with Gemini, OpenAI, Claude, or local Ollama models.
- 🐳 **Docker Ready**: Fully containerized setup for rapid and reliable deployment.
- 📜 **Academic Tooling**: Integrated LaTeX build system for generating IEEE-formatted research papers.


---

## 📸 Application Preview

<div align="center">
  <img src="assets/preview.gif" alt="CMatrix Overview" width="100%" />
</div>

---

## 🛠️ Technology Stack

| Category | Technology Stack |
| :--- | :--- |
| **AI Agents & Orchestration** | <a href="https://github.com/langchain-ai/langgraph"><img src="https://img.shields.io/badge/LangGraph-000000?style=for-the-badge&logo=langchain&logoColor=white" alt="LangGraph" /></a> <a href="https://github.com/langchain-ai/langchain"><img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain" /></a> <img src="https://img.shields.io/badge/Multi--Agent-blue?style=for-the-badge" alt="Multi-Agent" /> <img src="https://img.shields.io/badge/ReWOO-orange?style=for-the-badge" alt="ReWOO" /> <img src="https://img.shields.io/badge/Self--Reflection-purple?style=for-the-badge" alt="Self-Reflection" /> <img src="https://img.shields.io/badge/Tree--of--Thoughts-green?style=for-the-badge" alt="Tree-of-Thoughts" /> <img src="https://img.shields.io/badge/Supervisor--Pattern-red?style=for-the-badge" alt="Supervisor Pattern" /> <img src="https://img.shields.io/badge/Agentic--RAG-cyan?style=for-the-badge" alt="Agentic RAG" /> |
| **Frontend & UI** | <a href="https://nextjs.org/"><img src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js" /></a> |
| **Backend & API** | <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" /></a> |
| **Knowledge Base & Memory** | <a href="https://qdrant.tech/"><img src="https://img.shields.io/badge/Qdrant-7B3F00?style=for-the-badge&logo=qdrant&logoColor=white" alt="Qdrant" /></a> <img src="https://img.shields.io/badge/Vector--Database-black?style=for-the-badge" alt="Vector Database" /> <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" /></a> <a href="https://www.sqlalchemy.org/"><img src="https://img.shields.io/badge/SQLAlchemy-D71100?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy" /></a> |
| **Infrastructure & Queue** | <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" /></a> <a href="https://redis.io/"><img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis" /></a> <a href="https://docs.celeryq.dev/"><img src="https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white" alt="Celery" /></a> |


---

## 🚀 Installation & Setup

CMatrix supports both local development workflows and a fully containerized Docker approach. 

### 1. Prerequisites

Ensure you have the following installed:
- **Docker** and **Docker Compose**
- **Git**
- **Python 3.12+** and **Node.js** for local native development.

### 2. Clone the Repository

```bash
git clone https://github.com/nishan-paul-2022/cmatrix-agentic-red-team.git
cd cmatrix-agentic-red-team
```

### 3. Configuration

Set up your environment variables by copying the example files:

```bash
cp .env.example .env
```

#### 3.1 ⚙️ Core Configuration
Essential settings for the backend API and database. Edit `.env` to define:
- `SECRET_KEY`: Security key for standard app operation.
- `DATABASE_URL`: Postgres connection string (defaults mapped to Docker setup).

#### 3.2 🤖 LLM Configuration
API keys for AI models (e.g., Google Gemini, OpenAI, Anthropic) are configured directly via the **UI Settings > LLM Profiles** once the app is running. Alternatively, provide configuration explicitly via a `app-backend/llm_config.json` configuration file.

### 4. Running the Application

Choose the deployment method that fits your needs:

#### Option A: Full Docker Environment (Recommended)
This runs the entire system (Frontend, Backend API, Celery Worker, PostgreSQL, Redis, Qdrant) in isolated containers.

```bash
# Bring up all services
docker-compose up -d

# Check live logs
docker-compose logs -f
```

*Don't forget to run initial database migrations!*
```bash
docker-compose exec app-backend alembic upgrade head
```

#### Option B: Hybrid Local Development
Allows you to run infrastructure (DBs/Redis) in Docker, while running the Frontend and Backend natively for absolute speed in development. 

**Pre-requisite mapping:** Map local host to Docker containers to mock networking:
```bash
echo "127.0.0.1 cmatrix-postgres cmatrix-redis cmatrix-qdrant" | sudo tee -a /etc/hosts
```

**Terminal 1 — Core Infrastructure**:
```bash
docker-compose up -d postgres redis qdrant
```

**Terminal 2 — Backend API & Worker**:
```bash
cd app-backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 3012
# Note: You will also need to start Celery in another pane `celery -A app.worker worker`
```

**Terminal 3 — Frontend UI**:
```bash
cd app-frontend
npm install
npm run dev
```

> **Access Points:**
> - **Frontend Interface**: [http://localhost:3011](http://localhost:3011)
> - **Backend API & Swagger**: [http://localhost:3012/docs](http://localhost:3012/docs)
> - **Qdrant Vector Dashboard**: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

---

## 🔄 Development & CI/CD Workflow

CMatrix architecture treats AI agents as modular functions. Adding new tools involves drafting robust agent tools under `app-backend/app/tools` and plugging them directly into the ReAct LangGraph logic. 

**Testing**: 
- Backend: Run `pytest` inside the `app-backend` application scope.
- Frontend: Use standard `npm test` scripts within `app-frontend`.

*Code merges trigger Github Actions ensuring full functional and integration tests across container images.*

---

## 📜 Research & Documentation

CMatrix includes a professional, independent LaTeX build system for documenting research findings. We have five specialized research papers (formatted for **IEEE S&P**) covering different aspects of agentic security.

### 📚 Available Research Papers

| Index | Paper Topic | Build Command | Output Path |
| :--- | :--- | :--- | :--- |
| 01 | **Red Teaming** | `make paper-01` | `paper-01-red-teaming/paper/research-paper.pdf` |
| 02 | **HITL Safety** | `make paper-02` | `paper-02-hitl-safety/paper/research-paper.pdf` |
| 03 | **Agent Reasoning** | `make paper-03` | `paper-03-agent-reasoning/paper/research-paper.pdf` |
| 04 | **Vulnerability Intelligence** | `make paper-04` | `paper-04-vulnerability-intelligence/paper/research-paper.pdf` |
| 05 | **Model Orchestration** | `make paper-05` | `paper-05-model-orchestration/paper/research-paper.pdf` |

### 🏗️ Building the Papers

To build a specific paper, use its corresponding command listed above. To build **all** papers at once, run:

```bash
make paper
```

> **Note:** This requires `latexmk` and a standard LaTeX distribution (like TeX Live) installed on your system.

---


## 🌐 Contemporary Works & Inspiration

A curated list of state-of-the-art autonomous AI security agents and frameworks that share a similar vision of agentic red teaming and automated VAPT.

### 🛡️ Autonomous Penetration Testing

- **PentAGI**
    - 🌐 **Website**: [pentagi.com](https://pentagi.com/)
    - 📂 **GitHub**: [vxcontrol/pentagi](https://github.com/vxcontrol/pentagi)
    - 🎥 **Demo**: [Watch on YouTube](https://www.youtube.com/watch?v=R70x5Ddzs1o)
    > *A self-hosted, multi-agent AI system designed for autonomous end-to-end penetration testing using sandboxed tools.*

- **Shannon**
    - 🌐 **Website**: [keygraph.io](https://keygraph.io/)
    - 📂 **GitHub**: [KeygraphHQ/shannon](https://github.com/KeygraphHQ/shannon)
    - 🎥 **Demo**: [Watch on YouTube](https://www.youtube.com/watch?v=H7Xh-x_TVdQ)
    > *An AI-powered "proof-by-exploitation" security agent that validates vulnerabilities through real-world attack simulations.*

### ⚔️ Frameworks & MCP Servers

- **HexStrike AI**
    - 🌐 **Website**: [hexstrike.com](https://www.hexstrike.com/)
    - 📂 **GitHub**: [0x4m4/hexstrike-ai](https://github.com/0x4m4/hexstrike-ai)
    - 🎥 **Demo**: [Watch on YouTube](https://www.youtube.com/watch?v=PQOwpjZXzMo)
    > *A Model Context Protocol (MCP) server that empowers LLMs with 150+ professional security tools for autonomous offensive workflows.*

### 💻 General Agentic CLI & Tooling

- **Claude Code**
    - 🌐 **Website**: [claude.ai/code](https://claude.com/product/claude-code)
    > *Anthropic's official agentic CLI for terminal-based coding, shell execution, and autonomous repository management.*

- **OpenClaw**
    - 🌐 **Website**: [openclaw.ai](https://openclaw.ai/)
    - 📂 **GitHub**: [openclaw/openclaw](https://github.com/openclaw/openclaw)
    > *A viral, open-source autonomous AI assistant designed to run locally with direct OS and tool access.*

---

<div align="center">
  <img src="assets/company-logo.svg" alt="Author Logo" width="80" height="80" />
  <p>Built with ❤️ by <b><a href="https://kaiofficial.xyz/">KAI</a></b></p>
</div>
