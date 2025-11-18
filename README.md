# CMatrix - Multi-Agent Security Orchestration Platform

**AI-powered security assessment with real command execution**

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Setup environment
./docker.sh setup
# Edit .env and add your HUGGINGFACE_API_KEY

# Start all services
./docker.sh start

# Or for development with hot reload
./docker.sh dev
```

**Web UI:** http://localhost:3000  
**API Docs:** http://localhost:8000/docs

See [DOCKER.md](./DOCKER.md) for detailed Docker documentation.

### Option 2: Manual Setup

#### 1. Start Backend
```bash
cd backend && ./dev.sh
```

#### 2. Start Frontend
```bash
cd frontend && pnpm dev
```

#### 3. Open Web Interface

**Web UI:** http://localhost:3000

Type commands like:
```
scan_network(target=localhost, ports=1-10000)
search_cve(keyword="apache", limit=5)
check_compliance(standard="CIS")
```

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

### Key Features
- ✅ Real command execution in terminal
- ✅ Multi-agent orchestration
- ✅ Authorization & audit logging
- ✅ Web-based interface
- ✅ CVE database integration
- ✅ Compliance checking (CIS, PCI-DSS, HIPAA, SOC2)

---

## 📚 Architecture

```
User → Next.js Frontend (3000) → FastAPI Backend (8000) → Orchestrator
                                                              ↓
                                                    7 Specialized Agents
                                                              ↓
                                                    22 Security Tools
                                                              ↓
                                                    Real Command Execution
```

**Tech Stack:**
- Frontend: Next.js 16, React 19, TypeScript
- Backend: FastAPI, Python 3.11
- AI: LangGraph (Multi-Agent), LangChain
- Security Tools: nmap, curl, requests, BeautifulSoup4
- Database: JSON-based (auth config, audit logs)

---

## 🎯 Usage Examples

### Web UI (http://localhost:3000)

Type commands directly:
```
scan_network(target=localhost, ports=1-10000)
search_cve(keyword="apache", limit=5)
check_compliance(standard="CIS")
```

Or use natural language:
```
Scan localhost for open ports
Search for Apache vulnerabilities
Check CIS compliance requirements
What are the PCI-DSS requirements?
```

---

## 🔒 Security

### Authorization
- Target whitelist system
- API key authentication
- Scope-based permissions

### Audit Logging
- All commands logged to `backend/audit_logs/`
- JSON format for compliance
- Daily log rotation

### Command Whitelist
Only approved commands can execute:
- nmap, curl, wget, dig, ping
- systemctl, ps, top
- sudo (for privileged scans)
- 40+ security tools

---

## 📁 Project Structure

```
cmatrix/
├── frontend/              # Next.js app
│   ├── app/              # Pages and API routes
│   └── components/       # React components
├── backend/              # Python backend
│   ├── orchestrator.py   # Multi-agent orchestrator
│   ├── agents/          # 7 worker agents
│   ├── authorization.py  # Auth system
│   ├── audit_logger.py   # Audit logging
│   └── command_executor.py # Command execution
└── README.md           # This file
```

---

## 🧪 Testing

```bash
# Integration tests
./test-integration.sh

# System tests
./test-system.sh

# Command execution test
./test-command-execution.sh
```

---

## 📊 Status

**Phase 1: 100% Complete** ✅

- ✅ 7 specialized agents
- ✅ 22 security tools
- ✅ Real command execution
- ✅ Authorization system
- ✅ Audit logging
- ✅ Web interface
- ✅ CVE integration
- ✅ Compliance checking

---

## 🔧 Configuration

### Backend (.env)
```env
HUGGINGFACE_API_KEY=your_key_here
PORT=8000
```

### Frontend (.env)
```env
PYTHON_BACKEND_URL=http://localhost:8000
```

---

## 📝 Documentation

- **README.md** - This file (quick start & overview)
- **DOCKER.md** - Docker deployment guide
- **ARCHITECTURE.md** - Detailed architecture
- **project-proposal.md** - Original vision

---

## 🐛 Troubleshooting

**Backend won't start:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Port already in use:**
```bash
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

**nmap not found:**
```bash
sudo apt install nmap  # Ubuntu/Debian
sudo yum install nmap  # CentOS/RHEL
```

---

## 🌟 Key Capabilities

1. **Real Command Execution** - Actually runs nmap, curl, etc.
2. **Multi-Agent Orchestration** - 7 specialized security agents
3. **CVE Intelligence** - Real-time NVD database queries
4. **Compliance Checking** - CIS, PCI-DSS, HIPAA, SOC2
5. **Audit Trail** - Complete logging for compliance
6. **Authorization** - Target and API key management

---

## 📞 API Endpoints

- `GET /health` - Health check
- `POST /chat` - Non-streaming chat
- `POST /chat/stream` - Streaming chat (SSE)
- `GET /docs` - Interactive API documentation

---

## 🎊 Summary

CMatrix is a production-ready multi-agent security orchestration platform that performs real security assessments with proper authorization and comprehensive audit logging.

**Built with:** LangGraph, FastAPI, Next.js, nmap, and ❤️

---

**License:** Educational and development purposes

**Version:** 1.0.0 (Phase 1 Complete)
