# CMatrix Presentation Audit — 05: Architecture & Technical Accuracy

> Cross-check of every architecture claim against architecture.md. Technical accuracy issues catalogued with exact source references.

---

## Architecture Consistency Audit

### 5.1 — System Architecture (Slide 4)

| Claim in Slide | architecture.md Reference | Verdict |
|---|---|---|
| Commander reads ASG + APG state | §6 "Reads the dual graph" | ✅ Correct |
| Commander plans & delegates tasks | §6 "Plans. Delegates." | ✅ Correct |
| Commander approves High-risk ops | §8 "High-risk calls route to the Commander's mailbox" | ✅ Correct |
| Commander writes to APG only | §5c "The Commander that reasons writes only to the APG" | ✅ Correct |
| VAPT Protocol Prompt: phase sequencing, re-plan triggers, termination | §9 exact match | ✅ Correct |
| **Commander "Seeds APG AttackChains" NOT listed** | §6 "Which Vulnerability nodes seed new APG AttackChains?" | ❌ Missing |

**Deficit:** The most operationally unique Commander function — seeding APG AttackChains from Vulnerability nodes — is absent from its responsibility list.

---

### 5.2 — Dual-Graph World Model (Slide 5)

| Claim in Slide | architecture.md Reference | Verdict |
|---|---|---|
| ASG node types: Domain, Host, Port, Service, Technology, Endpoint, Parameter, Vulnerability, Evidence | §5a exact match | ✅ Correct (all 9) |
| APG node types: AttackChain, ChainStep, Impact | §5b exact match | ✅ Correct |
| APG carries risk_score, validation_status, priority | §5b exact match | ✅ Correct |
| Edge labels: has_host, runs, uses, has_endpoint, has_parameter, affected_by, validated_by | §5a exact match | ✅ Correct |
| Separation principle: discovery agents write only to ASG; Commander writes only to APG | §5c | ✅ Correct |
| APG "supported_by" edges to Evidence nodes | §5b | ✅ Correct |
| Chain-01 risk: 9.1 (escalated) | §13 + module-08 Fig 1B | ✅ Correct |
| Chain-02 risk: 7.5 | §13 + module-08 Fig 1B | ✅ Correct |
| Chain-03 risk: 8.1 | §13 + module-08 Fig 1B | ✅ Correct |
| Chain-04 risk: 7.0 | §13 + module-08 Fig 1B | ✅ Correct (slide 5) |

No errors on slide 5. This is the most technically accurate slide in the deck.

---

### 5.3 — Agent Architecture (Slide 6)

| Claim in Slide | architecture.md Reference | Verdict |
|---|---|---|
| Recon: Amass · httpx · Nmap | §4 tool-to-agent mapping | ✅ Correct |
| Analysis: WhatWeb · Gobuster · ffuf · Nuclei · ZAP | §4 tool-to-agent mapping | ✅ Correct |
| Research: NVD · Exploit-DB · GitHub · Vendor Advisories | §6 Research Agent | ✅ Correct |
| Validation: SQLMap · Metasploit | §4 tool-to-agent mapping | ✅ Correct |
| Evidence: EyeWitness | §4 tool-to-agent mapping | ✅ Correct |
| Validation self-debug: Diagnose → Contextualize → Adapt → Cap (×3) | §6 Validation Agent | ✅ Correct |
| Research is only agent with outbound internet access | §6 "only agent authorized to make outbound requests" | ✅ Correct |
| **Report Agent absent from roster** | §6 Report Agent section | ❌ Missing |

---

### 5.4 — Agent Spawn Lifecycle (Slide 7)

| Claim in Slide | architecture.md Reference | Verdict |
|---|---|---|
| Spawn package: ASG Slice + APG Slice + Tool Set + Task Spec + Knowledge Docs | §7 exact match (5 components) | ✅ Correct |
| Working context discarded after return | §7 "When the agent completes its task, it returns only structured output — new ASG nodes and edges. Its working context is discarded." | ✅ Correct |
| Three isolation properties | §7 three properties listed | ✅ Correct |
| WhatWeb = LOW risk, Gobuster = MED risk, SQLMap = HIGH risk | §8 Tool Risk Gate table | ✅ Correct |
| MED goes to LLM Classifier | §8 | ✅ Correct |
| HIGH goes to Commander Mailbox | §8 | ✅ Correct |

No errors.

---

### 5.5 — Tool Catalogue (Slide 8)

All 11 tools verified against architecture.md §4:

| Tool | Slide Agent | Spec Agent | Phase | Verdict |
|---|---|---|---|---|
| Amass | Recon Agent | Recon Agent | Reconnaissance | ✅ |
| httpx | Recon Agent | Recon Agent | Reconnaissance | ✅ |
| Nmap | Recon Agent | Recon Agent | Reconnaissance | ✅ |
| WhatWeb | Analysis Agent | Analysis Agent | Analysis | ✅ |
| Gobuster | Analysis Agent | Analysis Agent | Analysis | ✅ |
| ffuf | Analysis Agent | Analysis Agent | Analysis | ✅ |
| Nuclei | Analysis Agent | Analysis Agent | Analysis | ✅ |
| OWASP ZAP | Analysis Agent | Analysis Agent | Analysis | ✅ |
| SQLMap | Validation Agent | Validation Agent | Validation | ✅ |
| Metasploit | Validation Agent | Validation Agent | Validation | ✅ |
| EyeWitness | Evidence Agent | Evidence Agent | Evidence | ✅ |

100% accurate.

---

### 5.6 — Tool Risk Gate (Slide 9)

| Claim in Slide | architecture.md Reference | Verdict |
|---|---|---|
| Scope check before classification | §8 "target is in declared scope, tool is authorized" | ✅ Correct |
| LOW = execute immediately | §8 | ✅ Correct |
| MED = LLM Classifier | §8 | ✅ Correct |
| HIGH = Commander Mailbox | §8 | ✅ Correct |
| Classifier evaluates 3 axes: Scope Alignment, Chain Intent, Parameter Safety | §8 exact match | ✅ Correct |
| Classifier is a fast-filter + CoT two-stage design | §8 "fast-filter pass followed by brief chain-of-thought reasoning" | ✅ Correct |
| Commander can APPROVE / REJECT / MODIFY | §8 | ✅ Correct |
| Rejection annotated to APG chain | §8 "reason annotated to APG chain" | ✅ Correct |
| PostToolUse hook fires after ASG write | §8 Agent Lifecycle Hook System | ✅ Correct |
| Agent receives compact summary only | §8 + §12 MicroCompact | ✅ Correct |
| Amass/httpx/WhatWeb/EyeWitness = LOW | §8 table | ✅ Correct |
| Nmap/Gobuster/ffuf/Nuclei/ZAP = MED | §8 table | ✅ Correct |
| SQLMap/Metasploit = HIGH | §8 table | ✅ Correct |

No errors. Slide 9 is fully accurate.

---

### 5.7 — Attack Chain Lifecycle (Slide 12)

| Claim in Slide | architecture.md Reference | Verdict |
|---|---|---|
| States: HYPOTHESIZED → PARTIALLY_VALIDATED → VALIDATED / RULED_OUT | §11 exact match | ✅ Correct |
| Self-debug: ATTEMPT → DIAGNOSE → CONTEXTUALIZE → ADAPT → CAP × 3 | §6 Validation Agent | ✅ Correct |
| RULED_OUT writes failure to ASG Vulnerability node | §6 "failure reason is written to the ASG as a structured annotation" | ✅ Correct |
| **risk_score = CVSS × Exploitability × Impact** | §5b: "derived from vulnerability severity, exploitability, and impact classification" — **no formula given** | ❌ Invented |
| **Chain-04 risk: N/A** | module-08 Fig 1B: Chain-04 risk_score: 7.0 | ❌ Wrong |
| Chain-01 = 9.1 | §13 + module-08 | ✅ Correct |
| Chain-02 = 7.5 | §13 + module-08 | ✅ Correct |
| Chain-03 = 8.1 | §13 + module-08 | ✅ Correct |

Two errors on slide 12.

---

### 5.8 — Planning Cycle (Slide 13)

| Claim in Slide | architecture.md Reference | Verdict |
|---|---|---|
| OBSERVE ASG → OBSERVE APG → REASON → DECIDE loop | §10 Observe→Reason→Plan→Execute | ✅ Correct |
| EXPLORE / VALIDATE / PARALLEL decision branches | §10 | ✅ Correct |
| Cycle Guard: same call ×3 → force re-plan | §10 "if an agent issues the same tool call... more than a configurable number of times" | ✅ Correct |
| Reflector: repeated different failures → corrective guidance | §10 | ✅ Correct |
| Re-plan trigger: New Vulnerability node → seed APG chain | §10 + module-08 Fig 1B | ✅ Correct |
| Re-plan trigger: New Technology node → spawn Research Agent | §10 + module-08 Fig 1B | ✅ Correct |
| Chain RULED_OUT → remove, re-prioritize | §6 Validation Agent + §10 | ✅ Correct |

No errors.

---

### 5.9 — Dual Termination + Compaction (Slide 14)

| Claim in Slide | architecture.md Reference | Verdict |
|---|---|---|
| ASG exhausted = every node investigated by appropriate agent | §10 "No unexplored nodes remain" | ✅ Correct |
| APG resolved = all chains VALIDATED or RULED_OUT | §10 "All APG AttackChains are in a terminal state" | ✅ Correct |
| Both conditions must be true simultaneously | §10 "formally grounded dual termination condition" | ✅ Correct |
| Timer-based systems fail this test | §10 "a condition neither pure task-queue systems nor pure graph-traversal systems can express" | ✅ Correct |
| MicroCompact @ every tool call | §12 Layer 1 | ✅ Correct |
| AutoCompact @ 60% context | §12 Layer 2 | ✅ Correct |
| FullCompact @ 85% context | §12 Layer 3 | ✅ Correct |
| FullCompact reconstructs from ASG snapshot + APG priorities + last N tool results | §12 exact match | ✅ Correct |
| No intelligence lost because all discoveries live in ASG | §12 "FullCompact loses no intelligence" | ✅ Correct |

No errors.

---

### 5.10 — Cross-Mission Learning (Slide 15)

| Claim in Slide | architecture.md Reference | Verdict |
|---|---|---|
| Report Agent writes VALIDATED chains at mission close | §6 Cross-Mission Experience Store "Write trigger" | ✅ Correct |
| Commander queries after first Technology nodes written, before Analysis begins | §6 "Retrieval trigger" exact match | ✅ Correct |
| Store entries become "candidate chain hypotheses" | §6 exact wording | ✅ Correct |
| Crystallization threshold: ≥2 missions with same fingerprint | §6 Attack Strategy Library | ✅ Correct |
| Named strategies e.g. STRAT-WP-SQLI-001 | §6 exact example | ✅ Correct |
| Strategies prioritized above zero-prior chains | §6 "prioritized above zero-prior chains because they carry a validated track record" | ✅ Correct |
| AutoAttacker origin for C10 | §15 Related Work exact match | ✅ Correct |
| **C12 (Trajectory Export) not covered** | §12 + §14 C12 definition | ❌ Missing |

---

### 5.11 — References (Slide 16)

| Claim in Slide | architecture.md Reference | Verdict |
|---|---|---|
| PentestGPT → Tool Adapter + MicroCompact | §15 PentestGPT section | ✅ Correct |
| AutoAttacker → Cross-Mission Experience Store (C10) | §15 AutoAttacker section | ✅ Correct |
| HPTSA → Knowledge Injection **(C3 / §7)** | §15 "Incorporated — Vulnerability-Class Knowledge Injection (§7)" — **C3 is APG Chain Lifecycle** | ❌ Wrong C-number |
| PentestAgent → Validation self-debug loop | §15 PentestAgent section | ✅ Correct |
| VulnBot → Context-Isolated Agent Spawning | §15 VulnBot section | ✅ Correct |
| PentAGI → Cycle Guard + Reflector | §15 PentAGI section | ✅ Correct |
| Claude Code → LLM Classifier + 6-hook system | §15 Claude Code section | ✅ Correct |
| Hermes Agent → Attack Strategy Library (C11) + Trajectory Export (C12) | §15 Hermes section | ✅ Correct |

One error: C3 mislabeled for Knowledge Injection.

---

## Technical Accuracy Summary

| Slide | Technical Errors Found |
|---|---|
| 4 | Commander seeding role missing |
| 6 | Report Agent missing |
| 10 | Chain-04 placed in wrong phase |
| 12 | risk_score formula invented; Chain-04 N/A |
| 15 | C12 absent |
| 16 | C3 mislabeled |
| All others | ✅ No errors |

**Total technical errors:** 6  
**Slides with errors:** 6 of 16  
**Slides fully accurate:** 10 of 16
