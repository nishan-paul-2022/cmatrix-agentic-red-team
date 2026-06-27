# Module 03 — The Agent Architecture (Who Does What)

---

## 🎯 One-Line Summary

CMatrix has **one brain** (the Commander) and **six specialist hands** (agents). Each agent is born fresh for its task, does only what it's authorized to do, and dies when it's done — leaving only structured knowledge behind.

---

## 🎭 Think of a Surgical Team

Imagine a complex surgical operation. There's:
- A **lead surgeon** who directs the operation, makes all major decisions, and coordinates the team.
- A **scrub nurse** who handles instruments.
- An **anesthesiologist** who manages sedation.
- A **resident** who handles specific tasks assigned by the lead.

Each person has a specific role. The scrub nurse doesn't decide whether to operate. The anesthesiologist doesn't wield the scalpel. The lead surgeon doesn't administer sedation. **Clear separation of roles makes the system reliable.**

CMatrix's agent architecture follows the same logic. One orchestrating intelligence (the Commander) directs specialists who each handle exactly one domain of responsibility.

---

## 👑 The Commander Agent — The Orchestrating Brain

The Commander is the intelligence center of CMatrix. It is the *only* agent that:
- Reads the complete state of both the ASG and APG
- Makes decisions about what to do next
- Spawns other agents and assigns their tasks
- **Writes to the APG** (creates and updates AttackChains)
- Approves or rejects High-risk tool calls from the mailbox

The Commander never runs tools directly. It never touches a vulnerability scanner or an exploit framework. Its job is purely **reasoning and orchestration** — reading the dual graph, figuring out what's most important, and delegating to specialists.

This might sound like a limitation, but it's actually a strength. A surgeon who focuses entirely on decision-making and delegates execution to trusted specialists produces better outcomes than one who tries to do everything themselves.

**Key decisions the Commander makes at each cycle:**
- Which ASG nodes are unexplored? What should be investigated next?
- Which Vulnerability nodes should seed new APG AttackChains?
- Which AttackChain has the highest risk score and deserves validation first?
- Has a chain been fully validated end-to-end?
- Is it time to terminate the mission?
- Should a High-risk tool call be approved?

The Commander is guided by the **VAPT Protocol Prompt** — a structured document that encodes the assessment methodology (which phases come first, when to re-plan, when to terminate). This is covered in Module 06.

---

## 🕵️ The Recon Agent — The Explorer

**Mission:** Map the external attack surface. Discover what exists.

The Recon Agent is spawned at the beginning of an assessment and given one job: find everything that's out there. It doesn't analyze. It doesn't assess vulnerabilities. It just discovers.

**Tools it uses:**
- **Amass** — finds all subdomains through DNS brute-forcing, certificate transparency logs, and passive OSINT sources
- **httpx** — checks which discovered hosts are actually alive and responding
- **Nmap** — scans live hosts for open ports, running services, OS information

**What it writes to the ASG:**
- Domain nodes (root domain + all subdomains discovered)
- Host nodes (IP addresses, OS, liveness status)
- Port nodes (open ports with protocol)
- Service nodes (software names, versions, banners)

When done, the Recon Agent returns its **structured ASG delta** (the set of new nodes and edges it created) to the Commander. Its working context is then discarded — completely. The Commander uses the ASG to understand what was found; it doesn't need the Recon Agent's conversation history.

---

## 🔬 The Analysis Agent — The Deep Investigator

**Mission:** Take the discovered surface and find vulnerabilities. Make the unknown known.

The Analysis Agent is spawned after Recon has populated the ASG with hosts, ports, and services. Now the question shifts from "what exists?" to "what weaknesses exist in what was found?"

**Tools it uses:**
- **WhatWeb** — fingerprints the technology stack (CMS, frameworks, JavaScript libraries, version numbers)
- **Gobuster** — brute-forces directories to find hidden paths, admin panels, backup files, exposed resources
- **ffuf** — fuzzes APIs and parameters to find undocumented endpoints and injection points
- **Nuclei** — template-based scanner that checks services against thousands of known CVE and misconfiguration signatures
- **OWASP ZAP** — active web application scanner that crawls and probes for OWASP Top 10 vulnerabilities

**What it writes to the ASG:**
- Technology nodes (CMS, framework, library versions)
- Endpoint nodes (discovered URL paths and API routes)
- Parameter nodes (input fields, query parameters)
- Vulnerability nodes (CVEs, misconfigurations, weaknesses)

The Analysis Agent transforms raw infrastructure into a map of security weaknesses. When it finds, say, WordPress 5.9.3 — it doesn't just write "WordPress found." It triggers the Research Agent to find what CVEs affect that version and writes enriched Vulnerability nodes.

---

## 🔍 The Research Agent — The Intelligence Officer

**Mission:** Ground vulnerability findings in real-world intelligence. Close the knowledge gap between what was found and what is known about it.

This agent is spawned on-demand — whenever the Commander or Analysis Agent encounters a vulnerability, technology version, or CVE that needs enrichment. It never runs VAPT tools. It connects to external intelligence sources.

**Authorized sources:**
- **NVD (National Vulnerability Database)** — CVE technical details, CVSS scores, affected version ranges
- **Exploit-DB** — publicly available proof-of-concept (PoC) exploits, classified by type
- **GitHub** — security advisories, PoC repositories, vendor patch information
- **Vendor security advisories** — sourced from ASG Technology node metadata

**What it writes to the ASG:**
- Enriched attributes on Vulnerability nodes: CVE severity, CVSS vector, exploitability assessment (PoC exists / no public PoC / actively exploited in the wild), recommended validation approach

**The most important rule about the Research Agent:** It is the *only* agent authorized to make outbound requests to external networks. Every other agent operates exclusively on the target environment. This boundary is a hard design constraint — it prevents agents from accidentally leaking target information to external services or conducting unauthorized external queries.

> No raw web content ever enters the LLM context — only the structured intelligence record extracted from the response.

This ensures Research Agent output is consistent with the same principle applied to tool outputs: structured findings only, never noisy raw data.

---

## 🎯 The Validation Agent — The Proof-Maker

**Mission:** Prove that discovered vulnerabilities are real and exploitable. Not discover — prove.

This is the most critical and sensitive agent in the system. It receives a specific APG AttackChain from the Commander and executes controlled exploitation to validate each ChainStep in sequence.

**Tools it uses:**
- **SQLMap** — automated SQL injection detection and exploitation
- **Metasploit** — exploitation framework for running known exploits against identified vulnerabilities

**What happens when a step succeeds:**
The ChainStep status advances toward `VALIDATED`. Evidence is written to the ASG.

**What happens when a step fails:**
This is where the Validation Agent gets interesting. Instead of immediately giving up and marking the step `RULED_OUT`, it enters a **structured self-debugging loop**:

### The Self-Debugging Loop

```
ATTEMPT → DIAGNOSE → CONTEXTUALIZE → ADAPT → retry (up to cap)
                                                    ↓ (if cap reached)
                                              RULED_OUT + write failure reason to ASG
```

1. **ATTEMPT** — Execute the tool against the target.
2. **DIAGNOSE** — Analyze *why* it failed. Wrong parameter? Authentication required? Version mismatch? Payload encoding issue? Tool flag error?
3. **CONTEXTUALIZE** — Query the ASG for additional information that might resolve the diagnosis. (E.g., "Let me check if the Service node has more version details" or "Was a credential captured in a prior Evidence node?")
4. **ADAPT** — Modify the tool invocation based on diagnosis and new context. Retry with the corrected approach.
5. **CAP** — After a configurable maximum retry count (default: 3 attempts), mark the ChainStep `RULED_OUT` and write the failure reason as a structured annotation on the Vulnerability node in the ASG.

Why is this loop valuable? Because most exploit failures in real penetration testing aren't fundamental — they're parameter issues, timing issues, encoding issues, version mismatches. A skilled human tester would diagnose and adapt. The self-debugging loop gives CMatrix's Validation Agent the same capability. The cap prevents infinite loops; the loop prevents premature abandonment.

### Vulnerability-Class Knowledge Injection

The Validation Agent doesn't go into its task empty-handed. At spawn time, it receives **curated offline expert knowledge** matched to the vulnerability class it's working on:

| What it's validating | What knowledge it receives |
|---------------------|--------------------------|
| SQL injection chains | SQL injection technique taxonomy; SQLMap flag reference; blind/time-based detection patterns |
| XSS chains | XSS payload patterns; CSP bypass techniques; DOM vs reflected vs stored distinction |
| Exploit chains | Metasploit module selection heuristics; payload/encoder selection guide |

These documents are pre-loaded, version-controlled expert knowledge. They encode practitioner wisdom that would otherwise be implicit in the model's training — and they're re-injected at spawn time every time, so they never get lost to context compaction.

---

## 📸 The Evidence Agent — The Documentarian

**Mission:** Capture proof of everything. Make findings impossible to dispute.

After the Validation Agent confirms a ChainStep, the Evidence Agent is spawned to create visual proof artifacts.

**Tool it uses:**
- **EyeWitness** — headless screenshot capture of web pages, exposed panels, and API responses

**What it writes to the ASG:**
- Evidence nodes (screenshot files, response captures, exploitation outputs)
- `validated_by` edges linking Evidence to the corresponding ASG Vulnerability nodes
- `supported_by` edges linking Evidence to the corresponding APG ChainStep nodes

This creates the traceability chain: every claimed vulnerability in the final report has a corresponding Evidence node in the ASG, linked directly to the proof artifact.

---

## 📝 The Report Agent — The Writer

**Mission:** Translate the dual-graph world model into a professional human-readable report.

The Report Agent is the last agent spawned in a mission. It reads the complete ASG and APG and produces the final penetration test report. It does not run tools. It makes no security decisions. It is purely a reader and writer.

**Report structure it produces:**
- **Executive Summary** — business impact, derived from APG Impact nodes
- **Technical Findings** — every vulnerability with severity, sourced from ASG Vulnerability nodes
- **Attack Surface Map** — complete discovered environment from the ASG
- **Validated Attack Chains** — step-by-step chains from the APG with linked Evidence at each step
- **Remediation Guidance** — prioritized by APG risk scores

---

## 🧊 Context Isolation — The Most Underappreciated Design Choice

Here's the design principle that ties all agents together: **every agent is spawned fresh and dies when done.**

Agents are not persistent processes that accumulate history. Each agent spawn:
- Receives only the **ASG slice** relevant to its task (not the full graph)
- Receives only the **APG slice** relevant to its task (if applicable)
- Receives only the **tool set** it's authorized to use (not all tools)
- Receives a specific **task specification** from the Commander

When the agent completes, it returns only **structured output** — new ASG nodes and edges. Its entire working context (conversation history, tool outputs, intermediate reasoning) is discarded.

Why is this so important?

1. **The Commander's context stays clean.** It never sees raw tool outputs, verbose scan results, or intermediate reasoning from agents. It only sees ASG/APG state changes. This keeps the Commander sharp and focused.

2. **Agents can't contaminate each other.** If Agent A runs a massive directory brute-force and generates thousands of lines of output, none of that leaks into Agent B's context when it's spawned later.

3. **Rejected High-risk calls vanish.** If the Commander rejects a dangerous tool call, that rejection never appears in the Commander's own context — preventing the refusal from subtly biasing future planning decisions.

---

## 🗺️ Who Does What — Quick Reference

| Agent | Role | Tools | Writes to |
|-------|------|-------|-----------|
| **Commander** | Orchestration, reasoning, APG management | None | APG only |
| **Recon** | External discovery | Amass, httpx, Nmap | ASG (Domain, Host, Port, Service) |
| **Analysis** | Deep enumeration, vuln discovery | WhatWeb, Gobuster, ffuf, Nuclei, OWASP ZAP | ASG (Technology, Endpoint, Parameter, Vulnerability) |
| **Research** | Live CVE intelligence | NVD, Exploit-DB, GitHub APIs | ASG (Vulnerability node enrichment) |
| **Validation** | Controlled exploitation | SQLMap, Metasploit | ASG (Evidence nodes), APG (chain status) |
| **Evidence** | Proof capture | EyeWitness | ASG (Evidence nodes) |
| **Report** | Final report generation | None | Report document (reads full ASG + APG) |

---

## ✅ What You Should Remember From This Module

| Concept | Plain English |
|---------|---------------|
| Commander | The brain — reads everything, plans everything, writes only to APG, never runs tools |
| Specialist agents | Spawn fresh, do one job, return structured output, then vanish |
| Context isolation | No agent's raw history pollutes any other agent or the Commander |
| Self-debugging loop | Validation Agent diagnoses and adapts on failure before giving up |
| Knowledge injection | Validation Agent gets expert documents pre-loaded at spawn time |

---

*Next: Module 04 — The Tool Adapter Layer and Risk Gate*
