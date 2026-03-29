# CMatrix Red Team: End-to-End Demonstration Plan

> **Project Name**: SecureCorp Portal (Artificial Vulnerable Environment)
> **Target URL**: `http://lab.kaiofficial.xyz`
> **Objective**: Demonstrate the autonomous reconnaissance, vulnerability analysis, and exploitation capabilities of the CMatrix multi-agent system.

---

## 1. Project Overview

The objective is to deploy a standalone "Black Box" target application on a remote **Contabo VPS** and perform an automated red teaming audit from the **CMatrix** platform. This demonstrates real-world capabilities across the public internet.

### Network Architecture
- **Control Plane (CMatrix)**: Running locally or on a separate management VPS.
- **Target Plane (SecureCorp)**: Running in an isolated Docker container on the Contabo VPS.
- **Connection**: External scanning via Public IP/Domain (`lab.kaiofficial.xyz`).

---

## 2. Target Application: "SecureCorp Portal"

A Node.js/Express application designed with "hidden" vulnerabilities that map specifically to the CMatrix agent toolsets.

### Vulnerability Matrix

| CMatrix Agent | Target Vulnerability | Implementation Logic |
| :--- | :--- | :--- |
| **Network Agent** | **Open Port 21** | A mock FTP listener with an old `vsftpd 2.3.4` banner. |
| **Auth Agent** | **SQL Injection** | `SELECT * FROM users WHERE username = '${req.body.user}'` on login. |
| **Web Agent** | **Reflected XSS** | A search bar reflecting URL params without HTML escaping. |
| **Vuln Intel Agent** | **Known RCE Library** | Uses `node-serialize@0.0.4` (CVE-2017-5941). |
| **Config Agent** | **Exposed .env** | Sensitive database credentials accessible at `/config/.env`. |
| **API Sec Agent** | **IDOR** | `/api/user/:id` endpoint returns any profile without token verification. |

---

## 3. High-Level Demo Workflow

### Phase 1: Setup
1. **Target Subdomain**: Point `lab.kaiofficial.xyz` to your Contabo VPS IP.
2. **Dockerization**: Deploy the target container on the VPS.
3. **Nginx Proxy**: Configure Nginx to route traffic from the subdomain to the container.

### Phase 2: Autonomous Audit
1. **Instruction**: User tells CMatrix: *"Our target is http://lab.kaiofficial.xyz. Start a full audit."*
2. **Recon**: The **Network Agent** scans the domain and identifies open ports (80, 21).
3. **Exploration**: **Auth Agent** attempts a login bypass and succeeds via SQLi.
4. **Leakage**: **Config Agent** crawls the site and finds the exposed `.env` file.
5. **Synthesis**: **Vuln Intel Agent** explains the RCE risk in the serialized headers.

---

## 4. Safety & Isolation Protocol (Contabo Compliance)

To ensure your server remains safe and your account isn't flagged by Contabo:

1. **Strict Containerization**: The target app is isolated in a Docker bridge network. It cannot access the VPS host filesystem.
2. **Gentle Probing**: CMatrix tools will be configured for "Low Aggression" (e.g., `nmap -T3`).
3. **Non-Destructive Payloads**: Payloads like `alert(1)` or `' OR 1=1` are used instead of destructive commands.
4. **Port Restriction**: Only specific demo ports (80, 21, 8080) will be exposed to the internet.

---

## 5. Deployment Checklist (Commands)

### On Contabo VPS:
```bash
mkdir -p ~/redteam-lab
cd ~/redteam-lab
# (Files: server.js, Dockerfile, docker-compose.yml)
docker-compose up -d
```

### On Local CMatrix:
```bash
# Verify connection to target
curl http://lab.kaiofficial.xyz
# Start Agentic Scan in UI
```
