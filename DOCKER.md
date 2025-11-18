# 🐳 CMatrix Docker Guide

## 🚀 Quick Start

**1. Setup** (First time only)
```bash
./docker.sh setup    # Creates .env file
nano .env            # Add your HUGGINGFACE_API_KEY
```

**2. Run**
```bash
./docker.sh start    # Starts everything in background
```

**3. Access**
- **App:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs

---

## 🛠️ Common Commands

| Action | Command | Description |
|--------|---------|-------------|
| **Start** | `./docker.sh start` | Run in production mode (background) |
| **Dev** | `./docker.sh dev` | Run with hot-reload (live editing) |
| **Stop** | `./docker.sh stop` | Stop all services |
| **Logs** | `./docker.sh logs` | View server logs (Ctrl+C to exit) |
| **Clean** | `./docker.sh clean` | Wipe all containers & volumes |
| **Shell** | `./docker.sh shell-backend` | Open terminal inside backend |

---

## ⚙️ Configuration

**Environment Variables (`.env`)**
```env
HUGGINGFACE_API_KEY=your_key_here  # Required
PORT=8000                          # Backend port
```

**Project Structure**
- `docker-compose.yml` - Production config
- `docker-compose.dev.yml` - Development config (hot-reload)
- `backend/Dockerfile` - Python/FastAPI image
- `frontend/Dockerfile` - Next.js image

---

## 🐛 Troubleshooting

**Port already in use?**
```bash
./docker.sh clean
./docker.sh start
```

**Build failing?**
```bash
./docker.sh rebuild
```

**Check Health**
```bash
./docker.sh health
```
