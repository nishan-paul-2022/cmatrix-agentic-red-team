# CMatrix Red Team: World-Class End-to-End Demo Plan
**Date**: April 4th, 2026 | **Target**: lab.kaiofficial.xyz

---

## 🎭 The Narrative Flow (5-Act Story)

### **Act 1: The Sovereign Instruction (30s)**
*   **Action**: Type a single natural language command: `"Perform a full security audit of lab.kaiofficial.xyz. Identify critical vulnerabilities and generate a report."`
*   **Impression**: Total autonomy. No complex flags or scripts. The teacher sees a "Human-to-Agent" interaction.

### **Act 2: Autonomous Recon & The Approval Gate (2m)**
*   **Action**: The **Network Agent** spawns. Logs stream in live: `[📡] Scanning lab.kaiofficial.xyz...`.
*   **The Moment**: The **HITL Gate** triggers for the Nmap scan (Red/Orange badge).
*   **Narrative**: Pause and explain: *"The system is autonomous, but I stay in control for high-risk network operations. This is responsible AI in action."* -> Click **Approve**.

### **Act 3: Parallel Deep Dive (3-4m)**
*   **Action**: The **Supervisor Agent** analyzes the initial findings and delegates tasks in parallel.
*   **Visual**: Show the **Animated Diagram** with three branches firing at once:
    1.  **Web Agent**: Crawling for XSS and `.env` leaks.
    2.  **Auth Agent**: Testing SQL Injection on the login form.
    3.  **API Security Agent**: Checking `/api/user/1` for IDOR.
*   **Impression**: Massive efficiency. One human doing the work of three specialized researchers simultaneously.

### **Act 4: The Intelligence Layer (Agentic RAG) (2m)**
*   **Action**: Once `node-serialize@0.0.4` is found, the **VulnIntel Agent** triggers.
*   **Technical Highlight**: Show the **Query Reformulator** log:
    *   `Original: "node-serialize bugs"`
    *   `Reformulated: "CVE-2017-5941 Node.js deserialization RCE exploit details"`
*   **Correction Loop**: If the first vector search is broad, show the agent automatically narrowing the search to find the specific CVSS 9.8 critical vulnerability.

### **Act 5: Actionable Synthesis (1m)**
*   **Action**: The system collapses its findings into a **Structured JSON/Markdown Report**.
*   **Impression**: High-quality artifact. Ranking by CVSS severity shows that the agent isn't just "finding things"; it is **prioritizing risk**.

---

## 🛠️ The 6 Key Functionalities (What to Highlight)

1.  **Autonomous Multi-Agent Orchestration**: Highlight the `Supervisor.py` logic that manages the life cycle of sub-agents without human hand-holding.
2.  **HITL (Human-in-the-Loop) Gate**: Demonstrate the `checkpoint.py` state persistence that allows the scan to "wait" for you safely.
3.  **Agentic RAG (Query Reformulation)**: Explain how `query_reformulator.py` uses an LLM to "think" about search terms before hitting the CVE database.
4.  **Self-Correcting Search**: Mention the `self_correction.py` service that retries failed logic automatically—the system doesn't give up.
5.  **CVSS-Ranked Reporting**: Show the final output ranking findings by impact, demonstrating technical depth.
6.  **Real Internet Target**: Emphasize that `lab.kaiofficial.xyz` is a live VPS on Contabo, proving the system works across real network boundaries.

---

## 🏁 Deployment Checklist (Contabo VPS)

| Vulnerability | Port/Endpoint | Purpose |
| :--- | :--- | :--- |
| **vsftpd 2.3.4** | Port 21 | Port scan + specific version trigger |
| **SQL Injection** | `/login` | Auth bypass demo |
| **Exposed .env** | `/.env` | Config leakage demo |
| **CVE-2017-5941** | Header/Cookie | Agentic RAG / RCE demo |
| **IDOR** | `/api/user/:id` | API vulnerability demo |
