# Module 07 — The 11 VAPT Tools: Real World vs. CMatrix

---

## 🎯 One-Line Summary

CMatrix autonomously operates **11 industry-standard security tools** — the same tools professional penetration testers use every day. The difference: an AI orchestrates them with graph-grounded reasoning instead of human intuition.

---

## 🗺️ Tools by Phase — Quick Map

```
PHASE 1 — RECONNAISSANCE
  Tool 01: Amass        → Subdomain enumeration
  Tool 02: httpx        → Live host probing
  Tool 03: Nmap         → Port + service fingerprinting

PHASE 2 — ANALYSIS + INTELLIGENCE
  Tool 04: WhatWeb      → Technology fingerprinting
  Tool 05: Gobuster     → Directory + file brute-force
  Tool 06: ffuf         → API route + parameter fuzzing
  Tool 07: Nuclei       → Template-based vulnerability scanning
  Tool 08: OWASP ZAP    → Active web application scanning

PHASE 3 — VALIDATION
  Tool 09: SQLMap       → SQL injection exploitation
  Tool 10: Metasploit   → Exploit execution + RCE demonstration

PHASE 3 — EVIDENCE
  Tool 11: EyeWitness   → Screenshot + proof capture
```

Every tool is wrapped in a **Tool Adapter** — agents never touch tools directly. Raw output is parsed into structured ASG nodes. Nothing unparsed ever enters an agent's reasoning context.

---

## PHASE 1 — RECONNAISSANCE

### 🔭 Tool 01: Amass — Subdomain Enumeration

**What it is:** Amass is the industry gold-standard for discovering all subdomains belonging to a root domain. A company might own `shopvault.io` but also run `api.shopvault.io`, `admin.shopvault.io`, `staging.shopvault.io`, `pay.shopvault.io` — often without documenting all of them publicly. Amass finds them all.

**How it works (three methods simultaneously):**
1. **DNS brute-forcing** — tries thousands of possible subdomain names (`api`, `admin`, `dev`, `staging`, `mail`, `vpn`, `internal`, etc.) and checks if the DNS server responds
2. **Certificate Transparency (CT) logs** — every SSL/TLS certificate issued publicly is logged. These logs contain all domain names the certificate covers. Amass queries these logs to find subdomains that were issued certificates.
3. **Passive OSINT** — queries third-party databases (Shodan, VirusTotal, AlienVault, etc.) that have indexed domain information over time

**How a real pentester uses it:**
```bash
amass enum -passive -d shopvault.io -o subdomains.txt
amass enum -active -brute -d shopvault.io -w wordlist.txt -o active_results.txt
```
The pentester runs passive first (no traffic to the target — just querying public databases), then active brute-force. They then manually review the list, looking for anything unexpected: staging servers, backup servers, admin panels, internal tools accidentally exposed externally.

**How CMatrix uses it:**
The Recon Agent invokes Amass via the Tool Adapter. The adapter parses the output text into structured `Domain` nodes — one per discovered subdomain — with attributes: `domain_name`, `discovery_method` (passive/active), `resolved_ip`. These are written directly to the ASG. The Recon Agent sees only: *"Amass complete. 14 subdomains discovered."* — not the raw text.

**What the ASG gets:**
```
[Domain: shopvault.io]
[Domain: api.shopvault.io]
[Domain: admin.shopvault.io]
[Domain: staging.shopvault.io]
[Domain: pay.shopvault.io]
... (14 total)
```

---

### 🌐 Tool 02: httpx — Live Host Probing

**What it is:** Given a list of domains or IP addresses, httpx rapidly checks which ones are actually alive and responding to HTTP/HTTPS requests. It's the filter between "domains that exist in DNS" and "domains with live web servers."

**Why it's needed:** Amass might discover 50 subdomains. Not all of them have web servers. Some might be mail servers, some might be parked domains, some might redirect. httpx makes HTTP/HTTPS requests to each discovered host and reports back: status code, server software banner, page title, TLS certificate details, redirect chain, response time.

**Key finding httpx surfaces:** An unexpected 200 OK on `staging.shopvault.io` when you expected it to be internal-only. Or a `403 Forbidden` on `admin.shopvault.io` — which tells you there IS a server there, even if it's blocking you. Both are valuable intelligence.

**How a real pentester uses it:**
```bash
cat subdomains.txt | httpx -status-code -title -server -tech-detect -o live_hosts.txt
```
They pipe Amass output directly into httpx. They scan the output for anomalies: unexpected status codes, old server software versions, misconfigured redirects, hosts on non-standard ports.

**How CMatrix uses it:**
The Recon Agent pipes Amass output into httpx. The Tool Adapter parses: status code, server banner (e.g., `Nginx 1.18.0`), title, TLS validity. Each live host becomes a `Host` node in the ASG with a `status: alive` attribute and HTTP metadata. Dead hosts are noted but not explored further (no wasted effort).

**What the ASG gets:**
```
[Host: 10.0.0.1] status=alive, server=Nginx 1.18.0, tls=valid
[Host: 10.0.0.2] status=alive, server=Apache 2.4.51, tls=EXPIRED ← flagged
```

---

### 🔌 Tool 03: Nmap — Port Scanner + Service Fingerprinter

**What it is:** The world's most-used network scanner. Nmap (Network Mapper) connects to every port on every host and determines: is this port open? What software is running on it? What version? What operating system is this machine running? Does this service have any known vulnerabilities (via NSE scripts)?

**Background — What are ports?** Every server communicates on numbered ports (0–65535). Port 80 = HTTP. Port 443 = HTTPS. Port 22 = SSH (remote access). Port 3306 = MySQL database. Port 8080 = alternative HTTP. An open port means: "there is a service running here, accepting connections." Nmap finds all of them.

**How a real pentester uses it:**
```bash
# Full port scan on all 65535 ports (slow but thorough)
nmap -sS -sV -O -p- --min-rate 5000 10.0.0.1 -oN nmap_full.txt

# Targeted script scan on found ports
nmap -sV --script=vuln -p 80,443,8080,22 10.0.0.1 -oN nmap_vuln.txt
```
They look for: non-standard ports running sensitive services (SSH on port 2222 — weaker security?), outdated software versions (Apache 2.4.49 — CVE-2021-41773!), unexpected services (a Redis database port open externally?).

**NSE Scripts:** Nmap has a library of scripts (NSE = Nmap Scripting Engine) that can check for specific vulnerabilities. `--script=vuln` runs hundreds of these automatically.

**How CMatrix uses it:**
The Recon Agent runs Nmap on all live hosts discovered by httpx. The Tool Adapter parses the Nmap XML output (which can be thousands of lines) into clean `Port` and `Service` nodes per host. If NSE scripts detect vulnerabilities, those are flagged as candidate Vulnerability nodes (to be enriched by the Research Agent).

**What the ASG gets:**
```
[Host: 10.0.0.1]
  --has_port--> [Port: 80, protocol=tcp, state=open]
  --has_port--> [Port: 443, protocol=tcp, state=open]
  --has_port--> [Port: 8080, protocol=tcp, state=open]
    [Port: 80] --runs--> [Service: Nginx 1.18.0]
    [Port: 443] --runs--> [Service: Nginx 1.18.0, tls=valid]
    [Port: 8080] --runs--> [Service: HTTP unencrypted]
```

---

## PHASE 2 — ANALYSIS + INTELLIGENCE

### 🔍 Tool 04: WhatWeb — Technology Fingerprinter

**What it is:** WhatWeb analyzes HTTP responses — headers, HTML source code, cookies, URL patterns, JavaScript files — and identifies exactly what software is powering a website. CMS (WordPress, Drupal, Joomla), frameworks (Django, Laravel, Express), server-side languages (PHP, Python, Ruby), JavaScript libraries (jQuery 1.x vs 3.x), e-commerce platforms (WooCommerce, Magento), and their version numbers.

**Why version numbers matter:** A web application running "WordPress 5.9.3" is not just a CMS — it's a precisely identified software artifact with a known CVE list. WhatWeb's output is what makes the Research Agent's work possible.

**How a real pentester uses it:**
```bash
whatweb -a 3 https://shopvault.io --log-json whatweb_results.json
```
Aggression level 3 = active testing (sends real requests). They review the results looking for: old plugin versions, outdated CMS, server headers leaking software info (e.g., `X-Powered-By: PHP/7.4.3` — which version?), JavaScript libraries with known XSS vulnerabilities.

**How CMatrix uses it:**
The Analysis Agent runs WhatWeb on all live hosts. The Tool Adapter parses JSON output into `Technology` nodes: `{name: "WordPress", version: "5.9.3", confidence: 100}`. Each Technology node gets a `uses` edge from its host. Then the Commander spots new Technology nodes and spawns the Research Agent to enrich them with CVE data.

**What the ASG gets:**
```
[Host: shopvault.io] --uses--> [Technology: WordPress 5.9.3]
[Host: shopvault.io] --uses--> [Technology: WooCommerce 6.1.0]
[Host: api.shopvault.io] --uses--> [Technology: Django 4.1.2]
```

---

### 📁 Tool 05: Gobuster — Directory + File Brute-Forcer

**What it is:** Gobuster tries thousands of known URL paths against a web server and identifies which ones return valid responses. The goal: find pages, files, and directories that exist on the server but aren't linked from the main website — backup files, admin panels, configuration files, database exports left accidentally exposed.

**How it works:** Gobuster takes a wordlist (a list of common path names like `admin`, `backup`, `config.php`, `wp-admin`, `db_export.sql`, `.env`, `test`, `dashboard`, etc.) and sends an HTTP request for each one. If the server returns 200 (found) or 301/302 (redirect), it's reported.

**What a pentester finds with it:** The most dangerous findings are often "low hanging fruit" — a `backup/db_export_2023.sql` that is a complete database dump left on a public web server. Or `/admin/users` that's accessible without authentication. Or `.env` files containing API keys and database passwords.

**How a real pentester uses it:**
```bash
gobuster dir -u https://shopvault.io -w /usr/share/wordlists/dirb/big.txt \
  -x php,html,bak,sql,zip -t 50 -o gobuster_results.txt
```
The `-x` flag adds file extensions to try. `-t 50` = 50 concurrent threads (faster). They review 200s and 301s carefully, especially anything with "backup", "admin", "config", "export", "sql", "env" in the name.

**How CMatrix uses it:**
The Analysis Agent runs Gobuster on all live hosts. The Tool Adapter parses: URL path, HTTP status code, response size. Each discovered path becomes an `Endpoint` node in the ASG. High-value endpoints (admin panels, backup files, `.env`) are flagged with a `sensitivity: HIGH` attribute that influences Commander chain prioritization.

**What the ASG gets:**
```
[Host: shopvault.io]
  --has_endpoint--> [Endpoint: /wp-admin/login, status=200, sensitivity=HIGH]
  --has_endpoint--> [Endpoint: /backup/db_export_2023.sql, status=200, sensitivity=CRITICAL]
  --has_endpoint--> [Endpoint: /api/v1/orders, status=200]
```

---

### ⚡ Tool 06: ffuf — Fast Web Fuzzer

**What it is:** ffuf (Fuzz Faster U Fool) is a highly flexible HTTP fuzzer. Where Gobuster finds directories with a fixed wordlist, ffuf goes further: it discovers undocumented API endpoints, finds injectable parameters, identifies virtual hosts, and reveals hidden API versions.

**Three main use cases for pentesters:**

1. **API route discovery** — `ffuf -u https://api.shopvault.io/api/FUZZ -w api_wordlist.txt` — tries thousands of route names to find undocumented API endpoints
2. **Parameter fuzzing** — `ffuf -u https://shopvault.io/search?FUZZ=test -w params.txt` — discovers which query parameters the application accepts
3. **IDOR testing** — `ffuf -u https://shopvault.io/api/orders?user_id=FUZZ -w numbers.txt` — tries numeric IDs to find insecure direct object references

**IDOR background:** Insecure Direct Object Reference — if the API returns user 456's orders when you request `?user_id=456` and you're logged in as user 123, that's a critical vulnerability. ffuf automates testing this at scale.

**How a real pentester uses it:**
```bash
# API enumeration
ffuf -u https://api.shopvault.io/api/v1/FUZZ -w api_routes.txt -mc 200,301,403

# IDOR test on order endpoint
ffuf -u https://api.shopvault.io/api/v1/orders?user_id=FUZZ \
  -w numbers_1_to_1000.txt -H "Authorization: Bearer <token>" -mc 200
```

**How CMatrix uses it:**
The Analysis Agent targets each discovered API Service node and Endpoint node with ffuf. The Tool Adapter parses discovered routes into new `Endpoint` nodes and discovered parameters into `Parameter` nodes. IDOR indicators (endpoints that return different user data on different IDs) are flagged as candidate Vulnerability nodes.

**What the ASG gets:**
```
[Service: api.shopvault.io]
  --has_endpoint--> [Endpoint: /api/v1/internal/users, status=200]  ← undocumented!
  --has_endpoint--> [Endpoint: /api/v2/admin/orders, status=403]
[Endpoint: /api/v1/orders]
  --has_parameter--> [Parameter: user_id, type=integer, injectable=TRUE]  ← IDOR candidate
```

---

### 🎯 Tool 07: Nuclei — Template-Based Vulnerability Scanner

**What it is:** Nuclei scans discovered services and endpoints against a continuously updated library of templates — each template is a precise definition of how to detect a specific vulnerability, CVE, misconfiguration, or exposed sensitive file. Nuclei has thousands of templates covering CVEs, default credentials, exposed configuration files, misconfigurations, and OWASP vulnerabilities.

**How templates work:** A Nuclei template defines:
- What to send (HTTP request, specific payload, specific URL path)
- What to look for in the response (status code, specific text, header value)
- How confident the match is

Example: A template for CVE-2022-21661 sends a crafted request to the WordPress `admin-ajax.php` endpoint and looks for database error text in the response. If found → confirmed vulnerable.

**How a real pentester uses it:**
```bash
# Run all CVE templates against discovered hosts
nuclei -l live_hosts.txt -t cves/ -o nuclei_cve_results.txt

# Run specific technology templates
nuclei -l live_hosts.txt -t technologies/wordpress/ -o nuclei_wp_results.txt

# Run misconfiguration templates
nuclei -l live_hosts.txt -t misconfigurations/ -o nuclei_misc_results.txt
```
A pentester reviews Nuclei output to find confirmed-vulnerable services. High-confidence matches go straight into the report. Lower-confidence matches need manual verification.

**How CMatrix uses it:**
The Analysis Agent runs Nuclei after WhatWeb identifies Technology nodes (so the right technology-specific templates are chosen). The Tool Adapter parses: template ID, CVE reference, severity, target, match evidence. Each confirmed match becomes a `Vulnerability` node in the ASG — linked via `affected_by` to the relevant Technology or Endpoint node. The Commander then evaluates whether to spawn the Research Agent for enrichment.

**What the ASG gets:**
```
[Technology: WordPress 5.9.3]
  --affected_by--> [Vulnerability: CVE-2022-21661, severity=HIGH, source=Nuclei-template]
[Endpoint: /wp-admin/login]
  --affected_by--> [Vulnerability: DefaultCredentials-WordPress-Admin, severity=MEDIUM]
```

---

### 🕷️ Tool 08: OWASP ZAP — Active Web Application Scanner

**What it is:** OWASP ZAP (Zed Attack Proxy) is a full-featured web application security scanner. It first spiders (crawls) the entire web application to discover every page and form, then actively probes each discovered element for OWASP Top 10 vulnerabilities: SQL injection, XSS (Cross-Site Scripting), CSRF, path traversal, broken authentication, IDOR, security misconfiguration, and more.

**Background — OWASP Top 10:** The Open Web Application Security Project publishes the 10 most critical web application vulnerability categories. These represent the highest-risk, most commonly exploited classes of web vulnerabilities. ZAP systematically checks for all of them.

**Key vulnerability classes ZAP finds:**
- **XSS (Cross-Site Scripting):** Malicious JavaScript injected into pages that runs in other users' browsers — can steal cookies, hijack sessions
- **CSRF (Cross-Site Request Forgery):** Tricks authenticated users into performing actions they didn't intend
- **SQL Injection:** Database query manipulation through user input (if not already found by Nuclei)
- **Path Traversal:** Accessing files outside the web root using `../../../etc/passwd`
- **Broken Authentication:** Weak session tokens, credential exposure in URLs, insecure remember-me cookies

**How a real pentester uses it:**
```bash
# Headless (no browser window) spider + active scan
zap-cli spider https://shopvault.io
zap-cli active-scan --scanners all https://shopvault.io
zap-cli report -o zap_report.html -f html
```
A pentester reviews the ZAP report, triaging by risk level. High-risk findings (SQL injection, XSS with proof-of-concept) go into immediate investigation. Medium findings are noted for the report.

**How CMatrix uses it:**
The Analysis Agent runs ZAP on all live web hosts. The Tool Adapter parses the ZAP JSON report: each finding becomes a Vulnerability node in the ASG with attributes (vulnerability class, URL, parameter, evidence, risk level). XSS and injection findings on `Parameter` nodes update those nodes with an `injectable: TRUE` attribute — making them candidates for APG AttackChain entry points.

**What the ASG gets:**
```
[Endpoint: /search]
  --has_parameter--> [Parameter: q, injectable=XSS]
  --affected_by--> [Vulnerability: XSS-Reflected-on-search-q, severity=MEDIUM]
[Endpoint: /staging/login]
  --affected_by--> [Vulnerability: SQLError-on-login-form, severity=HIGH]
```

---

## PHASE 3 — VALIDATION

### 💉 Tool 09: SQLMap — SQL Injection Validator + Exploiter

**What it is:** SQLMap is the definitive automated SQL injection tool. It takes a URL with a parameter, automatically detects if that parameter is injectable, identifies the injection technique, and then exploits it: dumping database contents, extracting credentials, testing for OS-level command execution.

**Background — SQL Injection types SQLMap handles:**
- **Error-based:** Database errors are returned visibly in the response — SQLMap reads the error messages to extract data
- **Boolean-based blind:** No visible data returned, but responses differ for true vs. false conditions — SQLMap infers data character by character
- **Time-based blind:** No visible difference in response, but a `SLEEP(5)` in the payload causes a time delay — SQLMap times responses to infer data
- **UNION-based:** Appends a `UNION SELECT` to the query to retrieve additional data in the response
- **Out-of-band:** Data is exfiltrated via DNS or HTTP requests to an external server

**How a real pentester uses it:**
```bash
# Test specific parameter for SQLi
sqlmap -u "https://shopvault.io/wp-admin/admin-ajax.php" \
  --data "action=query_vars&query_vars=test" \
  --dbms=mysql --level=3 --risk=2 --batch

# If injectable: dump specific table
sqlmap -u "https://shopvault.io/wp-admin/admin-ajax.php" \
  --data "action=query_vars&query_vars=test" \
  --dbms=mysql -D wordpress -T users --dump
```
The `--batch` flag means no prompts — fully automated. The pentester reviews the extracted data. If admin credentials are found, they test them on the admin panel.

**How CMatrix uses it:**
The Validation Agent receives the specific APG AttackChain ChainStep: "Confirm SQL injection via CVE-2022-21661 on the WP_Query endpoint." It invokes SQLMap through the Tool Adapter with parameters derived from the ASG (the exact endpoint URL, the injectable parameter name, the detected DBMS type from the Service node). This is a **HIGH risk** tool call — it goes through the Commander Mailbox before executing.

The Tool Adapter parses: injection type confirmed, DBMS version, extracted data (table names, row counts, sample data). The result: an Evidence node is created and linked to the ChainStep via `supported_by`. The ChainStep status advances toward `VALIDATED`.

**The self-debugging loop in action:** If SQLMap fails on the first attempt (wrong parameter, WAF blocking), the Validation Agent diagnoses the failure, queries the ASG for additional context (e.g., any WAF-related nodes?), and retries with adapted parameters (e.g., adding `--tamper=randomcase --delay=2` to bypass the WAF). Up to 3 retries before `RULED_OUT`.

**What the ASG gets:**
```
[Vulnerability: CVE-2022-21661]
  --validated_by--> [Evidence: sqlmap-extraction-output.txt]
  --validated_by--> [Evidence: wordpress-users-table-dump.txt]
```

---

### 💣 Tool 10: Metasploit — Exploit Framework + RCE Demonstrator

**What it is:** Metasploit is the world's most widely used penetration testing framework. It has thousands of modules — each one a ready-to-run exploit for a specific CVE or vulnerability class. Given a target and a vulnerability, Metasploit handles the exploit execution, payload delivery, and post-exploitation session management.

**Key concepts:**
- **Module:** A specific exploit (e.g., `exploit/multi/http/wp_admin_shell_upload`)
- **Payload:** What runs on the target after exploitation (e.g., a Meterpreter shell, a reverse shell, a command executor)
- **Meterpreter:** A powerful interactive shell that gives the attacker read/write filesystem access, process listing, privilege escalation commands, network pivoting — all over an encrypted channel
- **Session:** An active connection to a compromised system

**How a real pentester uses it:**
```bash
msfconsole
use exploit/multi/http/wp_admin_shell_upload
set RHOSTS shopvault.io
set USERNAME admin
set PASSWORD cracked_password_from_sqlmap
set TARGETURI /
run
# If successful: Meterpreter session opens
# > sysinfo      → shows OS, hostname, user
# > getuid       → shows current user (www-data? root?)
# > ls /home     → lists user directories
# > cat /etc/passwd → shows system users
```
The pentester uses the session to demonstrate impact: what data is accessible? Can they escalate to root? Can they reach internal network resources?

**In CMatrix — ChainStep 3 context:**
After SQLMap confirms injection (ChainStep 1) and credentials are extracted (ChainStep 2), the Validation Agent invokes Metasploit for ChainStep 3: "Deploy web shell to demonstrate RCE." This is the highest-risk call in the entire assessment — it goes through Commander Mailbox approval with full chain context provided.

If Metasploit achieves RCE, the Evidence Agent immediately captures screenshots. The AttackChain risk_score is escalated (from 8.8 CVSS to 9.1 post-validation, because impact is confirmed worse than theoretical). The chain status advances to `VALIDATED`.

**What the ASG gets:**
```
[Vulnerability: CVE-2022-21661]
  --validated_by--> [Evidence: webshell-running-screenshot.png]
  --validated_by--> [Evidence: meterpreter-session-sysinfo.txt]
```

---

## PHASE 3 — EVIDENCE

### 📸 Tool 11: EyeWitness — Screenshot Capture

**What it is:** EyeWitness is a headless browser tool that visits web pages, renders them in a real (non-visible) browser, captures a screenshot, and returns the image file. It handles authentication prompts, JavaScript-rendered pages, and web application login panels — anything a regular browser can display.

**Why screenshots matter in pentesting:** A penetration test report without visual evidence is less credible and less actionable. A screenshot of an admin panel you accessed, a database dump displayed in the browser, or a web shell execution prompt is **proof** — undeniable, timestamped, unambiguous evidence that the vulnerability is real and exploitable. Clients and management understand screenshots. They don't understand raw SQLMap output.

**How a real pentester uses it:**
```bash
# Screenshot a list of discovered endpoints
eyewitness --web -f live_hosts.txt --no-prompt -d screenshots/

# Screenshot specific high-value pages
eyewitness --web --single https://shopvault.io/wp-admin/ -d screenshots/

# Screenshot API responses
eyewitness --web --single https://api.shopvault.io/api/v1/internal/users -d screenshots/
```
A pentester runs EyeWitness at the end of an engagement to bulk-capture screenshots of all validated findings. They attach the most impactful ones to the executive summary: "Here is proof we accessed your admin panel. Here is proof we extracted your customer database."

**How CMatrix uses it:**
After every ChainStep is validated by the Validation Agent, the Evidence Agent is spawned. It receives the specific ASG Evidence node references — the exact URLs, panel addresses, or API endpoints that need to be captured. It invokes EyeWitness via the Tool Adapter. The Tool Adapter receives the screenshot file path, creates a permanent `Evidence` node in the ASG, and links it to the validated ChainStep via a `supported_by` edge and to the Vulnerability node via a `validated_by` edge.

**What the ASG gets:**
```
[Evidence: admin-panel-access-screenshot.png]
  ← supported_by -- [APG ChainStep 3: Metasploit → RCE]
  ← validated_by -- [Vulnerability: CVE-2022-21661]

[Evidence: customer-pii-database-screenshot.png]
  ← supported_by -- [APG ChainStep 2: Admin hash extracted]
  ← validated_by -- [Vulnerability: CVE-2022-21661]
```

The Report Agent later reads all `Evidence` nodes and embeds the screenshot references into the final penetration test report — one screenshot per validated finding, traceable back to the exact ChainStep it proves.

---

## 🔒 The Safety Boundary That Governs All 11 Tools

Every single tool above — from the passive Amass query to the destructive Metasploit exploit — flows through the same mandatory path:

```
Agent Request → Risk Gate → Tool Adapter → Tool Execution → Parse → ASG Write
```

| Tool | Risk Tier | Gate |
|------|-----------|------|
| Amass | LOW | Scope check only → immediate execution |
| httpx | LOW | Scope check only → immediate execution |
| WhatWeb | LOW | Scope check only → immediate execution |
| Nmap | MEDIUM | LLM Permission Classifier (scope + parameter safety) |
| Gobuster | MEDIUM | LLM Permission Classifier |
| ffuf | MEDIUM | LLM Permission Classifier |
| Nuclei | MEDIUM | LLM Permission Classifier |
| OWASP ZAP | MEDIUM | LLM Permission Classifier |
| SQLMap | HIGH | Commander Mailbox approval required |
| Metasploit | HIGH | Commander Mailbox approval required |
| EyeWitness | LOW | Scope check only (read-only, no exploitation) |

> **No raw tool output ever enters an agent's reasoning context. No exploitation tool executes without Commander-level approval. No tool operates outside the declared scope.**

---

## ✅ Summary Table — All 11 Tools at a Glance

| # | Tool | Phase | Agent | Real Purpose | CMatrix Purpose |
|---|------|-------|-------|-------------|-----------------|
| 1 | Amass | Recon | Recon | Find all subdomains | Populate Domain nodes in ASG |
| 2 | httpx | Recon | Recon | Identify live web servers | Populate Host nodes in ASG |
| 3 | Nmap | Recon | Recon | Map ports + services | Populate Port + Service nodes in ASG |
| 4 | WhatWeb | Analysis | Analysis | Identify technology versions | Populate Technology nodes → trigger Research Agent |
| 5 | Gobuster | Analysis | Analysis | Find hidden files + admin panels | Populate Endpoint nodes (incl. high-sensitivity) |
| 6 | ffuf | Analysis | Analysis | Discover API routes + IDOR params | Populate Endpoint + Parameter nodes |
| 7 | Nuclei | Analysis | Analysis | Detect known CVEs via templates | Populate Vulnerability nodes from template matches |
| 8 | OWASP ZAP | Analysis | Analysis | OWASP Top 10 active web scan | Populate Vulnerability nodes (XSS, SQLi, CSRF) |
| 9 | SQLMap | Validation | Validation | Prove SQL injection is exploitable | Validate APG ChainSteps; write Evidence nodes |
| 10 | Metasploit | Validation | Validation | Execute exploits, demonstrate RCE | Validate final ChainSteps; demonstrate impact |
| 11 | EyeWitness | Evidence | Evidence | Capture visual proof screenshots | Write Evidence nodes; link via supported_by edges |

---

*Next: Module 08 — Real-World Scenario Walkthrough (shopvault.io, visualized step by step)*
