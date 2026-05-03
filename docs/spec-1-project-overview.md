# CMatrix - Multi-Agent Security Orchestration Platform

**AI-powered security assessment with real command execution**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](.)
[![License](https://img.shields.io/badge/license-Educational-green.svg)](.)

CMatrix combines multi-agent AI orchestration with real security tool execution for comprehensive vulnerability assessments through natural language commands, maintaining strict authorization and audit trails.

---

## Table of Contents

- [🚀 Quick Start](#quick-start)
- [🛠️ Features](#features)
- [📚 Architecture](#architecture)
- [🎯 Usage Examples](#usage-examples)
- [🔒 Security & Authorization](#security--authorization)
- [🔐 Authentication](#authentication)
- [🧠 Knowledge Base](#knowledge-base)
- [📁 Project Structure](#project-structure)
- [🔧 Configuration](#configuration)
- [📞 API Reference](#api-reference)
- [🐛 Troubleshooting](#troubleshooting)
- [📋 Project Vision & Roadmap](#project-vision--roadmap)

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# 1. Setup (First time only)
./docker.sh setup    # Creates .env file
nano .env            # Add your SECRET_KEY

# 2. Run
./docker.sh start    # Starts everything in background

# 3. Access
# App: http://localhost:3011
# API Docs: http://localhost:3012/docs
```

**First Run:** Redirected to `/setup` to create admin credentials
**Subsequent Runs:** Redirected to `/login`

### Option 2: Manual Setup

```bash
# 1. Start Backend
cd app-backend && ./dev.sh

# 2. Start Frontend (new terminal)
cd app-frontend && pnpm dev

# 3. Open http://localhost:3011
```

### Common Docker Commands

| Action | Command | Description |
|--------|---------|-------------|
| **Start** | `./docker.sh start` | Run in production mode |
| **Dev** | `./docker.sh dev` | Run with hot-reload |
| **Stop** | `./docker.sh stop` | Stop all services |
| **Logs** | `./docker.sh logs` | View server logs |
| **Clean** | `./docker.sh clean` | Wipe containers & volumes |
| **Shell** | `./docker.sh shell-backend` | Open backend terminal |

---

## 🛠️ Features

### 7 Specialized Agents
- **Network Agent** - Port scanning, vulnerability assessment
- **Web Security Agent** - HTTP headers, HTTPS/HSTS validation
- **Authentication Agent** - Login forms, sessions, rate limiting
- **Configuration Agent** - Cloud config, system hardening, compliance
- **Vulnerability Intelligence Agent** - CVE search, threat intelligence
- **API Security Agent** - REST/GraphQL testing
- **Command Execution Agent** - Terminal command execution

### 22 Security Tools
All tools execute real commands (nmap, curl, etc.) with full audit logging.

### Key Capabilities
- ✅ Real command execution in terminal
- ✅ Multi-agent orchestration
- ✅ Long-term knowledge base (Qdrant vector store)
- ✅ Authorization & audit logging
- ✅ Web-based interface
- ✅ CVE database integration
- ✅ Compliance checking (CIS, PCI-DSS, HIPAA, SOC2)

---

## 📚 Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                         │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP/WebSocket + JWT Token
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    Next.js Frontend (Port 3011)              │
│  - Receives user messages                                    │
│  - Forwards to Python backend                                │
│  - Streams responses back to user                            │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP POST /chat/stream
                             │ Authorization: Bearer <token>
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                  Python Backend (Port 3012)                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  FastAPI Server                                      │   │
│  │  - Authenticates Request (JWT)                       │   │
│  │  - Manages agent execution                           │   │
│  │  - Streams responses                                 │   │
│  └────────────────────┬──────────────┬──────────────────┘   │
│                       │              │                       │
│                       ▼              ▼                       │
│  ┌─────────────────────────┐    ┌─────────────────────────┐ │
│  │  LangGraph Agent        │    │  Auth Service           │ │
│  │  - Agent Orchestration  │    │  - Login/Setup          │ │
│  │  - Tool Execution       │    │  - Token Validation     │ │
│  └─────────────────────────┘    └─────────────────────────┘ │
└────────────────────────────┬────────────────┬────────────────┘
                             │                │
                             │ HTTPS API      │ SQL (Async)
                             ▼                ▼
┌────────────────────────────────┐   ┌────────────────────────────────┐
│      HuggingFace Router API    │   │   PostgreSQL Database (5432)   │
│  Model: DeepHat/DeepHat-V1-7B  │   │   - Users Table                │
│                                │   │   - Persistent Storage         │
└────────────────────────────────┘   └────────────────────────────────┘
```

### Data Flow

1. **User → Frontend** → `/api/chat` (POST)
2. **Frontend → Backend** → `/chat/stream` (POST) with `{ message, history }`
3. **Backend → Agent** → Analyzes, executes tools, calls LLM, returns response
4. **Backend → Frontend → User** via Server-Sent Events (SSE)

### Key Components

**Frontend (Next.js)**
- Location: `app-frontend/`, Port: 3011
- Key File: `app-frontend/app/api/chat/route.ts`

**Backend (Python)**
- Location: `app-backend/`, Port: 3012
- Key Files: `app-backend/app.py`, `app-backend/agent.py`

### Benefits
✅ Security: API keys never exposed to frontend
✅ Flexibility: Easy to add new tools
✅ Scalability: Backend deployed independently
✅ Monitoring: Centralized logging

---

## 🎯 Usage Examples

### Web UI (http://localhost:3011)

**Structured Commands:**
```
scan_network(target=localhost, ports=1-10000)
search_cve(keyword="apache", limit=5)
check_compliance(standard="CIS")
```

**Natural Language:**
```
Scan localhost for open ports
Search for Apache vulnerabilities
Check CIS compliance requirements
What are the PCI-DSS requirements?
```

---

## 🔒 Security & Authorization

### Authorization
- Target whitelist system
- API key authentication
- Scope-based permissions

### Audit Logging
- All commands logged to `app-backend/audit_logs/`
- JSON format for compliance
- Daily log rotation

### Command Whitelist
Only approved commands execute:
- nmap, curl, wget, dig, ping
- systemctl, ps, top
- sudo (for privileged scans)
- 40+ security tools

---

## 🔐 Authentication

### Features
- **Single-User Setup**: First user sets admin credentials
- **JWT Tokens**: Secure, stateless authentication (7-day expiry)
- **PostgreSQL Storage**: Credentials hashed with Bcrypt
- **Protected Routes**: All API endpoints require valid token

### Setup Flow
1. **First Access**: Redirects to `/setup` - create username/password
2. **Login**: Subsequent access redirects to `/login`
3. **Logout**: Use logout button in header

---

## 🧠 Knowledge Base

Persistent knowledge base powered by Qdrant vector database.

### Features
- 💾 **Persistent Storage**: Scan results, findings, decisions stored permanently
- 🔍 **Semantic Search**: Natural language queries
- 🎯 **Context-Aware**: Better responses based on history
- 👤 **User Isolation**: Private knowledge base per user

### Usage

**Saving Information:**
```
"Scan ports on 192.168.1.100 and save the results"
"Save this finding to the knowledge base"
```

**Searching Past Information:**
```
"What ports did we find on 192.168.1.100?"
"Show me past SSL vulnerabilities"
"What have we discovered about the target network?"
```

### Technical Details
- **Vector Database**: Qdrant (http://localhost:6333)
- **Embedding Model**: all-MiniLM-L6-v2 (384 dimensions)
- **Collection**: `cmatrix_memory`
- **Dashboard**: http://localhost:6333/dashboard

### Management

```bash
# Health Check
./health_check.sh

# Test Knowledge Base
./test_knowledge_base.sh

# View Stored Memories
curl http://localhost:6333/collections/cmatrix_memory | jq '.result.points_count'
```

For detailed documentation, see [docs/KNOWLEDGE_BASE.md](docs/KNOWLEDGE_BASE.md)

---

## 📁 Project Structure

```
cmatrix/
├── app-frontend/              # Next.js app
│   ├── app/              # Pages and API routes
│   └── components/       # React components
├── app-backend/              # Python backend
│   ├── orchestrator.py   # Multi-agent orchestrator
│   ├── agents/          # 7 worker agents
│   ├── authorization.py  # Auth system
│   ├── audit_logger.py   # Audit logging
│   └── command_executor.py # Command execution
└── docs/                # Documentation
```

---

## 🔧 Configuration

### Backend (.env)
```env
PORT=3012
DATABASE_URL=postgresql+asyncpg://cmatrix:cmatrix@postgres:5432/cmatrix
SECRET_KEY=your_secret_key_here
```

### Frontend (.env)
```env
PYTHON_BACKEND_URL=http://localhost:3012
```

### LLM Provider Management

#### Available Providers

1. **HuggingFace** - Router API (default)
   - Models: DeepHat/DeepHat-V1-7B, custom models
   - Best for: Cybersecurity-focused responses

2. **Ollama** - Local model inference
   - Models: gemma3:4b, llama3, mistral, etc.
   - Best for: Local deployment, privacy, no API costs

3. **OpenRouter** - Multi-provider API
   - Models: x-ai/grok-4-fast:free, GPT-4, Claude, etc.
   - Best for: Access to multiple models through single API

4. **Kilo Code** - Custom xAI Grok Code models
   - Models: x-ai/grok-code-fast-1
   - Best for: Code generation and technical tasks

5. **Gemini (Google)** - Google's Gemini models
   - Models: gemini-2.5-pro, gemini-pro, gemini-pro-vision
   - Best for: Multimodal tasks, Google's ecosystem

6. **Cerebras** - High-performance inference
   - Models: gpt-oss-120b, qwen-3-coder-480b, llama3.1-70b
   - Best for: Fast inference, large context windows

#### Provider Switching

```bash
# Get available providers
curl -X GET "http://localhost:3012/api/v1/chat/providers" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Switch to a different provider
curl -X POST "http://localhost:3012/api/v1/chat/providers/switch" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '"ollama"'
```

---

## 📞 API Reference

### Core Endpoints
- `GET /health` - Health check
- `POST /api/v1/chat` - Non-streaming chat
- `POST /api/v1/chat/stream` - Streaming chat (SSE)

### LLM Provider Management
- `GET /api/v1/chat/providers` - List available LLM providers
- `POST /api/v1/chat/providers/switch` - Switch default LLM provider
- `GET /api/v1/chat/providers/{provider_name}` - Get provider details

### Documentation
- `GET /docs` - Interactive API documentation (Swagger UI)

---

## 🐛 Troubleshooting

**Backend won't start:**
```bash
cd app-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Port already in use:**
```bash
lsof -ti:3012 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

**Database connection failed:**
```bash
# Check if postgres is running
docker compose ps postgres
# Restart postgres
docker compose restart postgres
```

**nmap not found:**
```bash
sudo apt install nmap  # Ubuntu/Debian
sudo yum install nmap  # CentOS/RHEL
```

---

## 📋 Project Vision & Roadmap

### The Core Idea

An AI-orchestrated vulnerability assessment platform using a master-worker agent architecture where a central "Red Agent" coordinates specialized worker agents, each focused on specific security assessment domains.

### Legitimate Scope
- Vulnerability Discovery: Identifying weaknesses through passive and active scanning
- Configuration Analysis: Detecting misconfigurations and weak security postures
- Compliance Testing: Automated security compliance verification
- Simulated Attack Scenarios: Controlled proof-of-concept demonstrations in authorized environments

### Feasibility & Growth Potential

**Feasibility: MEDIUM**

**Positive Factors:**
- Existing agent frameworks (LangChain, AutoGen, CrewAI) make multi-agent systems accessible
- Security testing APIs and tools are available (Nmap, OWASP ZAP, etc.)
- Growing demand for automated security solutions
- Cloud infrastructure makes deployment scalable

**Critical Challenges:**
- Legal & Compliance: Requires robust authorization systems, audit trails, and legal frameworks
- Technical Complexity: Integrating diverse security tools reliably
- False Positives: AI agents may generate unreliable results requiring human verification
- Liability: Significant legal exposure if the system causes unintended damage
- Authorization Controls: Must prevent unauthorized use

**Growth Potential: MODERATE-HIGH**

**Market Opportunity:**
- Global cybersecurity market: $200B+ and growing 12% annually
- Penetration testing market: ~$2B with 15%+ CAGR
- Enterprise spending on security automation increasing rapidly

**Growth Drivers:**
- Cybersecurity talent shortage (3.5M+ unfilled positions globally)
- Increasing regulatory requirements (GDPR, SOC2, ISO 27001)
- Rising attack frequency and sophistication
- Shift toward continuous security testing (DevSecOps)

### Development Roadmap

#### Phase 1: Foundation (Months 1-4) ✅ COMPLETE
- Core architecture design and authorization framework
- Master agent orchestration engine
- Basic worker agents: Network discovery, Web scanning
- Authorization and audit logging system
- MVP with CLI interface

#### Phase 2: Core Platform (Months 5-9)
- Complete all 6+ worker agent modules
- Web-based dashboard and reporting
- Scan scheduling and automation
- Integration with common CI/CD pipelines
- Enhanced authorization controls

#### Phase 3: Intelligence & Automation (Months 10-14)
- AI-driven vulnerability prioritization
- Automated remediation suggestions
- Threat intelligence integration
- Custom agent creation framework
- API for third-party integrations

#### Phase 4: Enterprise Features (Months 15-18)
- Multi-tenancy and role-based access control (RBAC)
- Compliance reporting (SOC2, ISO 27001, PCI-DSS)
- Integration marketplace
- Advanced analytics and trend analysis
- Enterprise support infrastructure

#### Phase 5: Scale & Expansion (Months 19-24)
- Cloud-native agent deployment
- Real-time continuous monitoring
- Collaborative features for security teams
- AI model fine-tuning on customer data (with permission)
- International compliance (GDPR, regional requirements)

### Projected Impact

**People's Lives Touched: 10M-100M+ (Indirect)**

**Direct Users (Conservative 3-Year Projection):**
- Year 1: 50-100 organizations (500-2,000 security professionals)
- Year 2: 500-1,000 organizations (5,000-20,000 security professionals)
- Year 3: 2,000-5,000 organizations (20,000-100,000 security professionals)

**Industry Impact:**

1. **Security Team Productivity** ⭐⭐⭐⭐
   - Time Savings: 60-80% reduction in manual testing time
   - Coverage Increase: 3-5x more assets tested regularly

2. **Vulnerability Remediation Speed** ⭐⭐⭐⭐⭐
   - Current Average: 60-120 days from discovery to patch
   - With Automation: Reduce to 7-30 days

3. **Cost Reduction** ⭐⭐⭐⭐
   - Manual VAPT: $15,000-$100,000 per engagement
   - Automated Solution: $10,000-$50,000 annually for continuous testing
   - ROI: 200-500% for medium-large enterprises

4. **Breach Prevention** ⭐⭐⭐⭐⭐
   - Average breach costs $4.45M (IBM 2023)
   - If preventing just 1% of breaches: Billions saved globally

5. **Democratization of Security** ⭐⭐⭐⭐
   - Makes enterprise-grade security testing accessible to startups and SMBs
   - Levels the playing field between large and small organizations

### Critical Success Factors
1. **Authorization System**: Bulletproof controls preventing misuse
2. **Accuracy**: Low false positive rate (<5%)
3. **Compliance**: SOC2 Type II, ISO 27001 certified from day one
4. **Trust Building**: Strong brand, transparent practices, security researcher endorsements
5. **Integration**: Seamless fit into existing security workflows
6. **Support**: White-glove enterprise support and incident response

---

**Built with:** LangGraph, FastAPI, Next.js, nmap, and ❤️
