# SecureCorp Lab — Build Specification
**Target URL:** `http://lab.kaiofficial.xyz`
**Host:** Hetzner VPS — `[HETZNER_VPS_IP]` (EU region)
**Purpose:** Intentionally vulnerable demo target for CMatrix red team engagement
**Stack:** Node.js + Express, Dockerized, behind Nginx reverse proxy

---

## 1. Overview

SecureCorp Portal is a fake corporate web application with six deliberately planted vulnerabilities — one for each CMatrix agent. The vulnerabilities are realistic (not contrived) and map exactly to the demo narrative. The app must be stable, isolated from the VPS host, and safe to scan repeatedly.

### Vulnerability Matrix

| CMatrix Agent | Vulnerability | Location | CVE / Class |
|---|---|---|---|
| Network Agent | Open FTP port with vsftpd 2.3.4 banner | Port 21 | CVE-2011-2523 |
| Auth Agent | SQL injection on login | `POST /login` | CWE-89 |
| Web Agent | Reflected XSS on search | `GET /search?q=` | CWE-79 |
| Web Agent | Exposed `.env` file | `GET /config/.env` | CWE-538 |
| Vuln Intel Agent | node-serialize 0.0.4 in use | `POST /api/upload` | CVE-2017-5941 |
| API Security Agent | IDOR on user profile | `GET /api/user/:id` | CWE-639 |
| Config Agent | No security headers | All responses | CWE-693 |

---

## 2. Repository Structure

```
redteam-lab/
├── docker-compose.yml
├── nginx.conf
├── app/
│   ├── Dockerfile
│   ├── package.json
│   ├── server.js
│   ├── config/
│   │   └── .env                  ← intentionally exposed
│   └── views/
│       ├── index.html
│       ├── login.html
│       └── dashboard.html
└── ftp-mock/
    └── Dockerfile                ← mock FTP with vsftpd banner
```

---

## 3. Application Code

### 3.1 `package.json`

```json
{
  "name": "securecorp-portal",
  "version": "1.0.0",
  "description": "SecureCorp internal portal",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "node-serialize": "0.0.4",
    "sqlite3": "^5.1.6",
    "body-parser": "^1.20.2"
  }
}
```

> `node-serialize@0.0.4` is intentionally pinned — this is the vulnerable version (CVE-2017-5941).

---

### 3.2 `server.js`

```javascript
const express = require('express');
const bodyParser = require('body-parser');
const serialize = require('node-serialize');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3000;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// ─── DATABASE SETUP ──────────────────────────────────────────────────────────
// Using in-memory SQLite for portability
const db = new sqlite3.Database(':memory:');

db.serialize(() => {
  db.run(`CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    email TEXT,
    role TEXT
  )`);
  db.run(`INSERT INTO users VALUES (1, 'admin', 'admin123', 'admin@securecorp.local', 'admin')`);
  db.run(`INSERT INTO users VALUES (2, 'alice', 'password1', 'alice@securecorp.local', 'user')`);
  db.run(`INSERT INTO users VALUES (3, 'bob', 'letmein', 'bob@securecorp.local', 'user')`);
});

// ─── HOMEPAGE ────────────────────────────────────────────────────────────────
app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>SecureCorp Portal</title>
      <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 0 20px; }
        h1 { color: #2c3e50; }
        nav a { margin-right: 20px; color: #3498db; text-decoration: none; }
        .banner { background: #2c3e50; color: white; padding: 15px 20px; border-radius: 4px; margin-bottom: 20px; }
      </style>
    </head>
    <body>
      <div class="banner"><h2>SecureCorp Internal Portal</h2><p>Employee access only. All activity is monitored.</p></div>
      <nav>
        <a href="/login">Login</a>
        <a href="/search">Search</a>
        <a href="/api/user/1">My Profile</a>
      </nav>
      <hr>
      <p>Welcome to the SecureCorp employee portal. Please log in to access your dashboard.</p>
    </body>
    </html>
  `);
});

// ─── VULN 1: SQL INJECTION ────────────────────────────────────────────────────
// Auth Agent target
// Vulnerable: directly interpolates user input into SQL query — no parameterization
app.get('/login', (req, res) => {
  res.send(`
    <!DOCTYPE html><html><head><title>Login — SecureCorp</title>
    <style>body{font-family:Arial,sans-serif;max-width:400px;margin:80px auto;padding:0 20px}
    input{width:100%;padding:8px;margin:8px 0;box-sizing:border-box}
    button{background:#3498db;color:white;padding:10px 20px;border:none;cursor:pointer;width:100%}</style>
    </head><body>
    <h2>SecureCorp Login</h2>
    <form method="POST" action="/login">
      <input type="text" name="username" placeholder="Username" />
      <input type="password" name="password" placeholder="Password" />
      <button type="submit">Sign In</button>
    </form>
    </body></html>
  `);
});

app.post('/login', (req, res) => {
  const { username, password } = req.body;
  // VULNERABILITY: SQL Injection — raw string interpolation
  const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
  db.get(query, (err, row) => {
    if (err) {
      return res.status(500).send(`<h3>DB Error: ${err.message}</h3>`);
    }
    if (row) {
      res.send(`<h2>Welcome, ${row.username}!</h2><p>Role: ${row.role}</p><a href="/">Home</a>`);
    } else {
      res.status(401).send(`<h2>Invalid credentials</h2><a href="/login">Try again</a>`);
    }
  });
});

// ─── VULN 2: REFLECTED XSS ────────────────────────────────────────────────────
// Web Agent target
// Vulnerable: reflects URL param directly into HTML without escaping
app.get('/search', (req, res) => {
  const query = req.query.q || '';
  // VULNERABILITY: Reflected XSS — no HTML encoding on output
  res.send(`
    <!DOCTYPE html><html><head><title>Search — SecureCorp</title>
    <style>body{font-family:Arial,sans-serif;max-width:700px;margin:50px auto;padding:0 20px}
    input{padding:8px;width:300px}button{padding:8px 16px;background:#3498db;color:white;border:none}</style>
    </head><body>
    <h2>Employee Search</h2>
    <form method="GET">
      <input type="text" name="q" value="${query}" placeholder="Search employees..." />
      <button type="submit">Search</button>
    </form>
    <p>Search results for: <strong>${query}</strong></p>
    </body></html>
  `);
});

// ─── VULN 3: EXPOSED .env FILE ────────────────────────────────────────────────
// Config Agent target
// Vulnerable: serves sensitive config file over HTTP
app.get('/config/.env', (req, res) => {
  res.type('text/plain');
  res.send(`
# SecureCorp Portal — Environment Configuration
# DO NOT COMMIT THIS FILE

NODE_ENV=production
PORT=3000

# Database
DB_HOST=postgres.securecorp.internal
DB_PORT=5432
DB_NAME=securecorp_prod
DB_USER=sc_admin
DB_PASSWORD=Sup3rS3cr3tP@ssw0rd!

# AWS
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=ap-southeast-1

# JWT
JWT_SECRET=my_jwt_secret_key_do_not_share

# Internal APIs
INTERNAL_API_KEY=sk-internal-v2-abcdef1234567890
ADMIN_WEBHOOK=https://hooks.securecorp.internal/alerts
  `.trim());
});

// ─── VULN 4: IDOR ─────────────────────────────────────────────────────────────
// API Security Agent target
// Vulnerable: returns any user record by ID without authentication check
app.get('/api/user/:id', (req, res) => {
  const { id } = req.params;
  // VULNERABILITY: IDOR — no token verification, no ownership check
  db.get(`SELECT id, username, email, role FROM users WHERE id = ?`, [id], (err, row) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!row) return res.status(404).json({ error: 'User not found' });
    res.json(row);
  });
});

// ─── VULN 5: node-serialize DESERIALIZATION ───────────────────────────────────
// Vuln Intel Agent target (CVE-2017-5941)
// Vulnerable: deserializes untrusted user input — allows RCE via IIFE in serialized function
app.post('/api/upload', (req, res) => {
  try {
    const { data } = req.body;
    // VULNERABILITY: CVE-2017-5941 — node-serialize unserialize() on user-supplied input
    const result = serialize.unserialize(data);
    res.json({ status: 'processed', result: JSON.stringify(result) });
  } catch (e) {
    res.status(400).json({ error: 'Invalid data format' });
  }
});

// ─── VULN 6: MISSING SECURITY HEADERS ────────────────────────────────────────
// Config Agent target
// No X-Frame-Options, no Content-Security-Policy, no X-Content-Type-Options etc.
// These are intentionally absent — Express default has no security headers

// ─── START SERVER ─────────────────────────────────────────────────────────────
app.listen(PORT, '0.0.0.0', () => {
  console.log(`SecureCorp Portal running on port ${PORT}`);
});
```

---

### 3.3 `Dockerfile` (app)

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package.json .
RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
```

---

### 3.4 `ftp-mock/Dockerfile` (mock FTP banner)

This container doesn't serve real FTP — it opens port 21 and responds with the vsftpd 2.3.4 banner string so nmap fingerprinting picks it up correctly.

```dockerfile
FROM alpine:3.18

RUN apk add --no-cache ncat

EXPOSE 21

# Serve the vsftpd 2.3.4 banner on TCP port 21
CMD ["sh", "-c", "while true; do echo -e '220 (vsFTPd 2.3.4)' | ncat -l -p 21 -q 1; done"]
```

---

### 3.5 `docker-compose.yml`

```yaml
version: '3.8'

services:
  securecorp-app:
    build: ./app
    container_name: securecorp-app
    restart: unless-stopped
    networks:
      - lab-net
    expose:
      - "3000"

  securecorp-ftp:
    build: ./ftp-mock
    container_name: securecorp-ftp
    restart: unless-stopped
    networks:
      - lab-net
    ports:
      - "21:21"

networks:
  lab-net:
    driver: bridge
```

> The app container is NOT directly exposed to the internet — only Nginx talks to it. The FTP mock exposes port 21 directly since nmap needs to reach it.

---

### 3.6 `nginx.conf`

```nginx
server {
    listen 80;
    server_name lab.kaiofficial.xyz;

    location / {
        proxy_pass http://securecorp-app:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Add this as a new site config on the Hetzner VPS Nginx instance:

```bash
sudo nano /etc/nginx/sites-available/lab.kaiofficial.xyz
# paste the config above
sudo ln -s /etc/nginx/sites-available/lab.kaiofficial.xyz /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 4. DNS Configuration

Point `lab.kaiofficial.xyz` to your Hetzner VPS:

| Type | Name | Value | TTL |
|---|---|---|---|
| A | `lab` | `[HETZNER_VPS_IP]` | 300 |

Set TTL to 300 (5 min) for fast propagation. Verify with:

```bash
dig lab.kaiofficial.xyz
# Expected: [HETZNER_VPS_IP]
```

---

## 5. Deployment Commands (Run on Hetzner VPS)

```bash
# 1. SSH into VPS
ssh root@[HETZNER_VPS_IP]

# 2. Create lab directory
mkdir -p ~/redteam-lab/app
mkdir -p ~/redteam-lab/ftp-mock

# 3. Copy all files (from local machine)
# scp -r ./redteam-lab/ root@[HETZNER_VPS_IP]:~/

# 4. Build and start
cd ~/redteam-lab
docker compose up -d --build

# 5. Verify containers are running
docker compose ps
# Expected: securecorp-app (running), securecorp-ftp (running)

# 6. Test app directly (before DNS)
curl http://[HETZNER_VPS_IP]
# Expected: SecureCorp Portal HTML

# 7. Test via domain (after DNS propagates)
curl http://lab.kaiofficial.xyz
# Expected: SecureCorp Portal HTML

# 8. Test FTP banner
nmap -sV -p 21 lab.kaiofficial.xyz
# Expected: vsftpd 2.3.4
```

---

## 6. Verification Checklist

Run these manually before the demo to confirm every vulnerability is reachable:

```bash
# SQLi — should return admin user data
curl -X POST http://lab.kaiofficial.xyz/login \
  -d "username=' OR 1=1 --&password=x" \
  -H "Content-Type: application/x-www-form-urlencoded"

# XSS — should reflect the script tag in page source
curl "http://lab.kaiofficial.xyz/search?q=<script>alert(1)</script>"

# Exposed .env — should return plaintext credentials
curl http://lab.kaiofficial.xyz/config/.env

# IDOR — should return user 2 without any auth token
curl http://lab.kaiofficial.xyz/api/user/2

# node-serialize endpoint — should be reachable
curl -X POST http://lab.kaiofficial.xyz/api/upload \
  -H "Content-Type: application/json" \
  -d '{"data": "{\"name\": \"test\"}"}'

# FTP banner (requires nmap)
nmap -sV -p 21 lab.kaiofficial.xyz
```

All six should return expected results. If any fails, debug before the demo.

---

## 7. Safety & Isolation

This configuration is safe to run on the Hetzner VPS without violating ToS:

- The app runs in a Docker bridge network (`lab-net`) — it cannot access VPS host filesystem
- Only ports 80 and 21 are exposed to the internet (not 5432, 6379, or any internal services)
- Payloads used in the demo are non-destructive (`' OR 1=1`, `alert(1)`, etc.)
- The SQLite database is in-memory — it resets on container restart, no persistent data loss
- The FTP mock serves only a banner string — there is no actual FTP daemon running

**Nmap scan settings in CMatrix should be `-T3` (polite) for the demo, not `-T5` (aggressive).**

---

## 8. Resetting the Lab

If anything breaks during setup or the demo, reset cleanly:

```bash
cd ~/redteam-lab

# Full reset
docker compose down --volumes
docker compose up -d --build

# Verify
curl http://lab.kaiofficial.xyz
```

Takes about 30 seconds. The in-memory SQLite database reinitializes on startup.

---

## 9. Optional Enhancements (if time permits)

These are not required for the demo but strengthen the visual impact:

### 9.1 Dashboard Page (post-login)
After SQL injection succeeds, redirect to a fake dashboard showing "sensitive" internal data — employee records, server statuses, financial numbers. Makes the SQLi finding visually impactful.

### 9.2 Real vsftpd (alternative to mock)
If the mock banner isn't detected reliably by nmap service fingerprinting, install actual vsftpd in a container and configure it to respond with the 2.3.4 version string. The mock approach is faster to set up and sufficient for the demo.

### 9.3 HTTPS on the lab
Not recommended — adding TLS adds complexity and the demo doesn't benefit from it. HTTP is fine for an intentionally vulnerable lab.

---

## 10. File Creation Order

Build in this exact order to avoid dependency issues:

1. Create `redteam-lab/` directory structure
2. Write `app/package.json`
3. Write `app/server.js`
4. Write `app/Dockerfile`
5. Write `ftp-mock/Dockerfile`
6. Write `docker-compose.yml`
7. Write `nginx.conf` and configure on VPS
8. Update DNS
9. Deploy with `docker compose up -d --build`
10. Run verification checklist

Estimated total setup time: **1–2 hours** on a clean VPS with Docker already installed.
