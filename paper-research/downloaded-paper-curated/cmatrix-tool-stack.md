# CMatrix Tool Stack Documentation

> **Project:** CMatrix — LLM-Orchestrated Multi-Agent VAPT Framework  
> **Scope:** Web + API + Network (Black Box + Grey Box)  
> **Version:** v1  
> **Total Tools:** 11  

---

## Pipeline Overview

```
Target
  │
  ▼
Amass           ← Subdomain + OSINT recon
  │
  ▼
httpx           ← Live host validation
  │
  ▼
Nmap            ← Port scan + service detection
  │
  ▼
WhatWeb         ← Tech stack fingerprinting
  │
  ▼
Gobuster        ← Directory + file enumeration
  │
  ▼
ffuf            ← Parameter + endpoint + vhost fuzzing
  │
  ▼
Nuclei          ← CVE + misconfig vulnerability scan
  │
  ▼
OWASP ZAP       ← Active web + API scan
  │
  ▼
SQLMap          ← SQL injection validation
  │
  ▼
Metasploit      ← Exploit execution
  │
  ▼
EyeWitness      ← Screenshot + evidence collection
```

---

## Tool Reference

---

### 1. Amass
**Category:** Recon  
**Phase:** 1 — Initial reconnaissance  

**Purpose:**  
Amass performs external attack surface mapping through passive and active subdomain enumeration using OSINT sources, DNS brute-forcing, and graph-based relationship mapping.

**Why Amass over Subfinder:**  
Subfinder is fast but passive-only. Amass goes deeper — it supports active DNS brute-force, OSINT integration (Shodan, Censys, VirusTotal, etc.), and outputs a relationship graph, which is more useful for agent reasoning.

**Key Capabilities:**
- Passive subdomain discovery via 50+ data sources
- Active DNS brute-force enumeration
- ASN, IP range, and CIDR mapping
- Graph database output (supports Neo4j)
- OSINT integration (Shodan, Censys, VirusTotal, etc.)

**Agent Integration:**
```bash
# Passive recon
amass enum -passive -d target.com -o amass_out.txt -json amass_out.json

# Active recon (grey-box)
amass enum -active -d target.com -brute -o amass_out.txt -json amass_out.json
```

**Output Format:** JSON, TXT, Graph  
**LangGraph Node Input:** `{ target_domain }`  
**LangGraph Node Output:** `{ subdomains[], ip_ranges[], asn_info }`

---

### 2. httpx
**Category:** Host Validation  
**Phase:** 2 — Live host filtering  

**Purpose:**  
httpx probes discovered hosts/subdomains to filter live ones before passing them downstream. Prevents wasting tool cycles on dead hosts.

**Why it matters:**  
Amass may return hundreds of subdomains. Without httpx, every subsequent tool wastes time on dead hosts. The `Amass → httpx → WhatWeb` flow is the modern standard in recon pipelines.

**Key Capabilities:**
- HTTP/HTTPS probing at scale
- Status code, title, content-length extraction
- TLS certificate information
- Technology hints (basic)
- Response time and redirect tracking
- JSON output natively

**Agent Integration:**
```bash
# Probe all discovered subdomains
cat amass_out.txt | httpx -status-code -title -tech-detect -json -o httpx_out.json

# With TLS info
cat amass_out.txt | httpx -status-code -tls-grab -json -o httpx_out.json
```

**Output Format:** JSON  
**LangGraph Node Input:** `{ subdomains[] }`  
**LangGraph Node Output:** `{ live_hosts[], status_codes{}, titles{}, tls_info{} }`

---

### 3. Nmap
**Category:** Network  
**Phase:** 3 — Port scan and service detection  

**Purpose:**  
Nmap maps open ports, running services, service versions, and OS fingerprints across live hosts. Foundation of all network-layer attack surface understanding.

**Key Capabilities:**
- TCP/UDP port scanning
- Service version detection (`-sV`)
- OS fingerprinting (`-O`)
- NSE scripting engine for targeted checks
- Firewall/IDS evasion techniques
- XML output for structured parsing

**Agent Integration:**
```bash
# Standard service scan
nmap -sV -sC -oX nmap_out.xml -oJ nmap_out.json target.com

# Full port scan
nmap -p- -sV -T4 -oX nmap_full.xml target.com

# UDP scan (grey-box)
nmap -sU -top-ports 200 -oX nmap_udp.xml target.com
```

**Output Format:** XML, JSON (via `-oJ`), grepable  
**LangGraph Node Input:** `{ live_hosts[] }`  
**LangGraph Node Output:** `{ open_ports[], services{}, os_hints{}, nse_findings[] }`

---

### 4. WhatWeb
**Category:** Fingerprinting  
**Phase:** 4 — Technology stack detection  

**Purpose:**  
WhatWeb identifies web technologies — CMS, frameworks, server software, JavaScript libraries, analytics platforms, and more. Informs which vulnerability templates to run next.

**Key Capabilities:**
- 1800+ plugin detection rules
- CMS detection (WordPress, Drupal, Joomla, etc.)
- Framework detection (Laravel, Django, Rails, etc.)
- Server software detection (Apache, Nginx, IIS, etc.)
- Version extraction where exposed
- Aggression levels (1–4) for depth control

**Agent Integration:**
```bash
# Standard fingerprint
whatweb -a 3 --log-json=whatweb_out.json target.com

# Bulk scan from httpx output
cat live_hosts.txt | whatweb -a 3 --log-json=whatweb_out.json --input-file=-
```

**Output Format:** JSON, XML, TXT  
**LangGraph Node Input:** `{ live_hosts[] }`  
**LangGraph Node Output:** `{ technologies{}, cms, server, frameworks[], versions{} }`

**Agent Decision Point:**  
WhatWeb output should feed the agent's tool selection logic — e.g., if WordPress is detected, trigger WordPress-specific Nuclei templates next.

---

### 5. Gobuster
**Category:** Enumeration  
**Phase:** 5 — Directory and file brute-force  

**Purpose:**  
Gobuster brute-forces directories, files, and DNS subdomains. Uncovers hidden paths, admin panels, backup files, and exposed endpoints not linked from the application surface.

**Gobuster vs ffuf distinction:**  
Gobuster excels at directory/file discovery. ffuf handles parameter fuzzing, vhost discovery, and API endpoint fuzzing. They are complementary, not redundant.

**Key Capabilities:**
- Directory and file brute-force (`dir` mode)
- DNS subdomain brute-force (`dns` mode)
- Virtual host discovery (`vhost` mode)
- Custom wordlists
- Extension support (`.php`, `.bak`, `.env`, `.json`, etc.)
- Status code filtering

**Agent Integration:**
```bash
# Directory enumeration
gobuster dir -u https://target.com -w /usr/share/wordlists/dirb/common.txt \
  -x php,html,js,json,bak,env -o gobuster_out.txt --no-error -q

# JSON-friendly output via flag
gobuster dir -u https://target.com -w wordlist.txt -o gobuster_out.json -q
```

**Recommended Wordlists:**
- `SecLists/Discovery/Web-Content/common.txt`
- `SecLists/Discovery/Web-Content/api/api-endpoints.txt`
- `SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt`

**Output Format:** TXT (structured, parseable)  
**LangGraph Node Input:** `{ live_hosts[], extensions[] }`  
**LangGraph Node Output:** `{ discovered_paths[], interesting_files[] }`

---

### 6. ffuf
**Category:** Fuzzing  
**Phase:** 6 — Parameter, endpoint, and vhost fuzzing  

**Purpose:**  
ffuf (Fuzz Faster U Fool) performs high-speed web fuzzing — parameter discovery, hidden API endpoint enumeration, virtual host brute-forcing, and custom payload injection. Fills the gap Gobuster leaves on the API and parameter surface.

**Why ffuf matters for CMatrix specifically:**  
When the agent discovers `/api/users`, it needs to explore `/api/admin`, `/api/debug`, `/api/internal` etc. ffuf is built for exactly this — iterative API surface expansion driven by agent reasoning.

**Key Capabilities:**
- GET/POST parameter fuzzing
- API endpoint discovery
- Virtual host fuzzing
- Header fuzzing
- JSON body fuzzing
- Custom matchers (status code, size, regex, word count)
- Native JSON output

**Agent Integration:**
```bash
# API endpoint fuzzing
ffuf -u https://target.com/api/FUZZ -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt \
  -mc 200,201,301,302,401,403 -of json -o ffuf_api.json

# Parameter fuzzing
ffuf -u https://target.com/endpoint?FUZZ=test -w params_wordlist.txt \
  -mc 200 -of json -o ffuf_params.json

# Vhost fuzzing
ffuf -u https://target.com -H "Host: FUZZ.target.com" \
  -w subdomains.txt -mc 200 -of json -o ffuf_vhost.json
```

**Output Format:** JSON (native, clean)  
**LangGraph Node Input:** `{ base_url, discovered_paths[], fuzz_mode }`  
**LangGraph Node Output:** `{ discovered_endpoints[], parameters[], vhosts[] }`

---

### 7. Nuclei
**Category:** Vulnerability Scan  
**Phase:** 7 — Template-based vulnerability detection  

**Purpose:**  
Nuclei runs community-maintained YAML templates against targets to detect CVEs, misconfigurations, exposed panels, default credentials, and security header issues. Most automation-friendly scanner in the stack.

**Why Nuclei is the best fit for AI agent:**  
Templates are structured, tagged, and severity-rated. The agent can select which template categories to run based on WhatWeb fingerprint output — e.g., run `wordpress` templates only on WordPress targets. This makes Nuclei uniquely suited to intelligent agent-driven scanning.

**Key Capabilities:**
- 9000+ community templates (CVEs, misconfigs, exposures, etc.)
- Tag-based template filtering (`-tags cve,wordpress,api,auth`)
- Severity filtering (`-severity critical,high`)
- Rate limiting and concurrency control
- SARIF and JSON output
- Custom template support

**Agent Integration:**
```bash
# Run based on detected tech stack
nuclei -u https://target.com -tags wordpress,cve -severity critical,high \
  -json -o nuclei_out.json

# Full scan
nuclei -u https://target.com -json -o nuclei_full.json

# Network templates
nuclei -u target.com:port -tags network -json -o nuclei_network.json
```

**Output Format:** JSON, SARIF  
**LangGraph Node Input:** `{ target_url, detected_technologies[], severity_filter }`  
**LangGraph Node Output:** `{ vulnerabilities[], severity{}, cve_ids[], template_ids[] }`

**Agent Decision Point:**  
Nuclei findings should feed the agent's exploitation planning — confirmed CVEs get passed to Metasploit, SQLi hints get passed to SQLMap.

---

### 8. OWASP ZAP
**Category:** Web/API Scan  
**Phase:** 8 — Active web and API vulnerability scanning  

**Purpose:**  
ZAP performs active web application scanning — crawling, spidering, active attack, and API schema-based scanning. Covers OWASP Top 10 vulnerabilities including XSS, CSRF, IDOR, auth issues, and injection flaws.

**Key Capabilities:**
- Authenticated scanning (session, JWT, cookie, API key)
- OpenAPI/Swagger/GraphQL schema import for API scanning
- Active and passive scan modes
- Ajax Spider for JS-heavy SPAs
- REST API for full programmatic control
- SARIF, JSON, XML, HTML report output

**Agent Integration (via REST API):**
```python
# ZAP runs as a daemon; agent controls via REST API
import requests

ZAP_API = "http://localhost:8080"
API_KEY = "your-api-key"

# Start spider
requests.get(f"{ZAP_API}/JSON/spider/action/scan/",
    params={"apikey": API_KEY, "url": "https://target.com"})

# Start active scan
requests.get(f"{ZAP_API}/JSON/ascan/action/scan/",
    params={"apikey": API_KEY, "url": "https://target.com"})

# Get alerts
alerts = requests.get(f"{ZAP_API}/JSON/core/view/alerts/",
    params={"apikey": API_KEY}).json()
```

**Output Format:** JSON, XML, SARIF, HTML  
**LangGraph Node Input:** `{ target_url, auth_context, api_schema_path }`  
**LangGraph Node Output:** `{ alerts[], risk_levels{}, affected_endpoints[] }`

> **Note:** ZAP requires an **auth context manager** in CMatrix to fully leverage grey-box scanning. See Authentication Architecture section below.

---

### 9. SQLMap
**Category:** Validation  
**Phase:** 9 — SQL injection confirmation and exploitation  

**Purpose:**  
SQLMap automates detection and exploitation of SQL injection vulnerabilities. Used as a **validation step** after Nuclei or ZAP flags potential SQLi — not as a blind scanner.

**Key Capabilities:**
- 6 SQLi detection techniques (boolean, error, time, union, stacked, out-of-band)
- Database fingerprinting
- Data extraction (schema, tables, columns, dump)
- Authentication bypass testing
- WAF detection and evasion
- Batch/non-interactive mode for agent use

**Agent Integration:**
```bash
# Validate a suspected SQLi endpoint
sqlmap -u "https://target.com/api/users?id=1" \
  --batch --level=3 --risk=2 \
  --output-dir=./sqlmap_out \
  --forms --json-errors

# With authentication (grey-box)
sqlmap -u "https://target.com/api/users?id=1" \
  --cookie="session=abc123; token=xyz" \
  --batch --level=3 --output-dir=./sqlmap_out
```

**Output Format:** TXT logs, structured output directory  
**LangGraph Node Input:** `{ endpoint_url, parameters[], auth_cookies }`  
**LangGraph Node Output:** `{ injectable_params[], db_type, extracted_data[], severity }`

---

### 10. Metasploit
**Category:** Exploitation  
**Phase:** 10 — Exploit execution  

**Purpose:**  
Metasploit provides a framework for executing confirmed exploits against validated vulnerabilities. In CMatrix, it acts as the final offensive step — triggered only when upstream tools confirm exploitable conditions.

**Agent Integration approach:**  
Metasploit exposes an **RPC API** (`msfrpcd`) that the agent can call programmatically. In a research context (controlled lab / CTF / intentionally vulnerable VMs), full autonomous exploitation is acceptable.

**Key Capabilities:**
- 2000+ exploit modules
- Auxiliary modules (scanners, fuzzers, etc.)
- Post-exploitation modules
- RPC API for programmatic control (`msfrpcd`)
- Meterpreter payload support
- Session management

**Agent Integration (via RPC):**
```python
from metasploit.msfrpc import MsfRpcClient

client = MsfRpcClient('password', port=55553)

# Select and configure exploit
exploit = client.modules.use('exploit', 'multi/handler')
exploit['PAYLOAD'] = 'linux/x64/meterpreter/reverse_tcp'
exploit['LHOST'] = '0.0.0.0'
exploit['LPORT'] = 4444

# Execute
exploit.execute(payload=exploit['PAYLOAD'])
```

**Output Format:** RPC response objects, session data  
**LangGraph Node Input:** `{ cve_id, target_host, target_port, exploit_module }`  
**LangGraph Node Output:** `{ session_opened, shell_access, post_exploit_data }`

> **Research Note:** In CMatrix, Metasploit should be triggered by confirmed CVE IDs from Nuclei output — not blindly. The agent maps `cve_id → metasploit_module` using a lookup or an LLM reasoning step.

---

### 11. EyeWitness
**Category:** Evidence  
**Phase:** 11 — Screenshot and evidence collection  

**Purpose:**  
EyeWitness takes screenshots of discovered web services, captures HTTP headers, and generates an HTML report. Provides visual evidence of findings for research documentation and paper figures.

**Key Capabilities:**
- Headless screenshot of web services
- HTTP header capture
- Default credential checking
- RDP and VNC screenshot support
- Organized HTML report output

**Agent Integration:**
```bash
# Screenshot all live hosts
eyewitness --web -f live_hosts.txt --no-prompt -d ./eyewitness_out

# From Nmap XML
eyewitness --web --xml nmap_out.xml --no-prompt -d ./eyewitness_out
```

**Output Format:** HTML report + PNG screenshots  
**LangGraph Node Input:** `{ live_hosts[] }`  
**LangGraph Node Output:** `{ screenshots_dir, report_path, interesting_services[] }`

---

## Authentication Architecture (Grey-Box)

This is a **first-class CMatrix concern**, not a tool concern. All tools above support authentication — but CMatrix must manage and distribute auth context across them.

### Auth Context Manager (Required Component)

```python
# Conceptual structure
class AuthContext:
    session_cookies: dict
    jwt_token: str
    api_key: str
    csrf_token: str
    basic_auth: tuple  # (username, password)
    
    def to_zap_config(self) -> dict: ...
    def to_sqlmap_flags(self) -> list: ...
    def to_ffuf_headers(self) -> dict: ...
    def to_nuclei_headers(self) -> dict: ...
```

### Auth flow per tool

| Tool | Auth Method |
|---|---|
| ZAP | Session management via REST API config |
| SQLMap | `--cookie`, `--auth-type`, `--auth-cred` flags |
| ffuf | `-H "Authorization: Bearer ..."` header flag |
| Nuclei | `-H` header flag or template variable |
| Gobuster | `-c` cookie flag, `-H` header flag |
| httpx | `-H` header flag |

---

## LangGraph Node Map

```
[amass_node]
    └→ [httpx_node]
           └→ [nmap_node]
           └→ [whatweb_node]
                  └→ [gobuster_node]
                  └→ [ffuf_node]
                  └→ [nuclei_node]  ← tech-aware template selection
                         └→ [zap_node]
                         └→ [sqlmap_node]  ← triggered by SQLi hints
                         └→ [metasploit_node]  ← triggered by confirmed CVEs
                                └→ [eyewitness_node]
```

Each node:
- Receives structured JSON input
- Executes tool via subprocess or API
- Parses output into structured JSON
- Passes findings to next node(s) via LangGraph state

---

## Output Schema (Unified)

Every tool node should emit findings in this unified format for evidence correlation:

```json
{
  "tool": "nuclei",
  "phase": "vulnerability_scan",
  "target": "https://target.com",
  "timestamp": "2026-06-25T10:00:00Z",
  "findings": [
    {
      "id": "CVE-2021-44228",
      "severity": "critical",
      "description": "...",
      "endpoint": "/api/log",
      "evidence": "...",
      "raw_output": "..."
    }
  ]
}
```

This schema feeds both the **agent reasoning layer** (next tool selection) and the **final report generation**.

---

## Scan Mode Matrix

| Tool | Black Box | Grey Box | Notes |
|---|---|---|---|
| Amass | ✅ | ✅ | Passive vs active mode |
| httpx | ✅ | ✅ | Add auth headers in grey-box |
| Nmap | ✅ | ✅ | More aggressive timing in grey-box |
| WhatWeb | ✅ | ✅ | Higher aggression level in grey-box |
| Gobuster | ✅ | ✅ | Add auth cookies in grey-box |
| ffuf | ✅ | ✅ | Add auth headers in grey-box |
| Nuclei | ✅ | ✅ | More template categories in grey-box |
| ZAP | ✅ | ✅ | Full session auth in grey-box |
| SQLMap | ✅ | ✅ | Cookie/token auth in grey-box |
| Metasploit | ✅ | ✅ | Same; more post-exploit in grey-box |
| EyeWitness | ✅ | ✅ | Auth not relevant |

---

## Research Targets (Recommended)

For CMatrix v1 evaluation, test against:

| Target Type | Examples |
|---|---|
| Intentionally Vulnerable VMs | DVWA, Metasploitable, VulnHub machines |
| CTF Platforms | HackTheBox, TryHackMe retired machines |
| API Labs | OWASP crAPI, VAmPI, dvAPI |
| Cloud Labs | PentesterLab, PortSwigger Web Academy |

> Never run CMatrix against targets without explicit written authorization.

---

*CMatrix Tool Stack Documentation — v1*  
*Last updated: June 2026*
