# CMatrix Presentation Audit — 06: Workflow Consistency

> Cross-check of every workflow diagram against module-08-visual-walkthrough.md. Checks step correctness, sequence, and transition accuracy.

---

## Workflow 1 — shopvault.io Mission Timeline (Slide 10 vs. Module 07 Figure 1A)

### Phase 1 — Reconnaissance

| Step | module-08 Says | Slide 10 Says | Verdict |
|---|---|---|---|
| Tool order | Amass → httpx → Nmap | Amass → httpx → Nmap | ✅ Correct |
| Amass output | 14 subdomains | 14 subdomains | ✅ Correct |
| httpx output | 11 live hosts; staging unexpected 200 | 11 live hosts; staging unexpected 200 | ✅ Correct |
| Nmap output | 28 open ports; pay.shopvault.io expired TLS | Ports 80/443/8080/8443; pay.shopvault.io expired TLS | ✅ Correct |
| ASG delta | 37 new nodes | 37 new nodes | ✅ Correct |

Phase 1 is perfectly reproduced.

---

### Phase 2 — Analysis + Intelligence

| Step | module-08 Says | Slide 10 Says | Verdict |
|---|---|---|---|
| Tool order | WhatWeb → Research Agent → Gobuster → ffuf → Nuclei → ZAP | WhatWeb → Gobuster → ffuf → ZAP (Research shown separately) | ⚠️ Nuclei missing from slide summary |
| WhatWeb | WordPress 5.9.3, Django 4.1.2 | WordPress 5.9.3, Django API | ✅ Correct |
| Research Agent trigger | Commander spawns after WordPress 5.9.3 Technology node | Shown as "Research: CVE-2022-21661 (CVSS 8.8)" | ✅ Correct |
| Gobuster | /backup/db_export_2023.sql, /admin/login, /admin/users | /backup/db_export_2023.sql EXPOSED, /admin/login, /admin/users | ✅ Correct |
| ffuf | IDOR user_id param, internal API endpoints | IDOR user_id param, /api/v1/internal/users | ✅ Correct |
| Nuclei | CVE-2022-21661 template match, phpinfo.php, default creds | Mentioned "Nuclei" under tools but not in phase narrative | ⚠️ Nuclei output absent from walkthrough |
| ZAP | XSS /search?q=, SQL error staging login | XSS on /search?q=, SQL error on staging login | ✅ Correct |
| ASG delta | 61 nodes | 61 nodes | ✅ Correct |
| APG delta | 3 chains seeded | 3 chains seeded | ✅ Correct |

**Minor gap:** Nuclei's findings are listed in the tool catalogue but not shown in the Phase 2 narrative. The module-08 walkthrough explicitly states Nuclei fires on `pay.shopvault.io` (expired TLS), `staging.shopvault.io` (default creds template), and WordPress (WooCommerce plugin). Slide 10 omits this. This is a simplification, not an error, but the supervisor may notice that Nuclei appears in the tool catalogue but produces no visible output in the walkthrough.

---

### Phase 3 — Validation

| Step | module-08 Says | Slide 10 Says | Verdict |
|---|---|---|---|
| Chain pursuit order | Chain-01 (8.8) → Chain-03 (8.1) → Chain-02 (7.5) | Chain-01 → Chain-03 → Chain-02 | ✅ Correct order |
| Chain-01 Step 1 | SQLMap on WP_Query → SQLi confirmed | SQLMap → SQLi confirmed | ✅ Correct |
| Chain-01 Step 2 | SQLMap --dump users table → admin:Summer2023! | Admin hash cracked | ✅ Correct |
| Chain-01 Step 3 | Metasploit wp_admin_shell_upload → HIGH risk → Commander Mailbox → APPROVED → RCE | HIGH risk → Commander Mailbox → Metasploit → RCE | ✅ Correct |
| Chain-01 risk escalation | 8.8 → 9.1 after RCE | 8.8 → 9.1 escalated | ✅ Correct |
| Chain-03 | Blind SQLi staging login → staging DB creds → credential reuse flagged | Blind SQLi → DB creds, reuse risk flagged | ✅ Correct |
| Chain-02 | SQLMap user_id → IDOR confirmed | SQLMap user_id → IDOR confirmed | ✅ Correct |
| **Chain-04** | Module-08: Phase 4 ASG Exhaustion — Commander reads ASG, discovers /backup not accessed, seeds Chain-04, validates trivially via HTTP GET | **Slide 10: Listed in Phase 3 column alongside Chains 01–03** | ❌ Wrong phase |
| Phase 3 Evidence Agent | EyeWitness runs after each chain validation | "EyeWitness" listed under Phase 3 tools | ✅ Correct (present) |

**Critical error:** Chain-04 is in Phase 3 on slide 10. Module-08 Figure 1A places Chain-04 unambiguously in Phase 4 under "ASG Exhaustion Check" — after all three Phase 3 chains are validated and the Commander performs the exhaustion check.

---

### Phase 4 — Report

| Step | module-08 Says | Slide 10 Says | Verdict |
|---|---|---|---|
| Termination trigger | 111 ASG nodes explored, all 4 chains VALIDATED | 111 nodes — appears in stats box | ✅ Correct |
| Report Agent reads full ASG + APG | Explicit | ✅ | ✅ Correct |
| Report contents: 4 chains, executive summary, evidence at each ChainStep, 11 vulns | module-08 Fig 1A RPT node | Slide 10 Phase 4 box matches | ✅ Correct |

---

## Workflow 2 — Commander Decision Log (Slide 10 / vs Module 07 Figure 1B)

Module-08 Figure 1B shows a 14-step timeline of Commander decisions. Slide 10 condenses this into a phase-based summary. The phase summary is accurate, though the Commander decision detail is only visible across slides 10, 11, and 12 combined.

No inconsistencies found in the condensed version.

---

## Workflow 3 — Chain-01 Traceability (Slide 11 vs. Module 07 Figure 1D)

| Element | module-08 Says | Slide 11 Says | Verdict |
|---|---|---|---|
| Starting node | ASG Vulnerability: CVE-2022-21661, CVSS 8.8 | ASG VULNERABILITY: CVE-2022-21661, CVSS 8.8, PoC Exploit-DB ✓ | ✅ Correct |
| Chain node | APG AttackChain: Chain-01, risk 9.1, VALIDATED | APG ATTACKCHAIN: Chain-01, risk 9.1, VALIDATED | ✅ Correct |
| Edge CVE → Chain | starts_at | starts_at | ✅ Correct |
| ChainStep 1 | SQLMap → WP_Query SQLi | SQLMap → WP_Query SQLi | ✅ Correct |
| ChainStep 2 | SQLMap dump → hash cracked | SQLMap dump → hash cracked | ✅ Correct |
| ChainStep 3 | Metasploit → Web shell | Metasploit → Web shell | ✅ Correct |
| Edges between steps | next_step | next_step | ✅ Correct |
| Final edge | achieves → Impact | achieves | ✅ Correct |
| Evidence 1 | sqli-extraction.txt | sqli-extraction.txt | ✅ Correct |
| Evidence 2 | user-table-dump.png | user-table-dump.png | ✅ Correct |
| Evidence 3 | webshell-rce.png | webshell-rce.png | ✅ Correct |
| Evidence edges | supported_by | supported_by | ✅ Correct |

Slide 11 is a perfect reproduction of module-08 Figure 1D.

---

## Workflow 4 — Agent Spawn Lifecycle (Slide 7 vs. Module 03 Figure 2A)

| Step | module-08 Says | Slide 7 Says | Verdict |
|---|---|---|---|
| Commander reads ASG before spawn | Yes | Yes | ✅ Correct |
| Spawn with scoped context | ASG slice + task spec + toolset | ASG slice + task + toolset | ✅ Correct |
| WhatWeb call → LOW → execute | Yes | Yes | ✅ Correct |
| Gobuster → MED → LLM Classifier | Yes | LLM Classifier → EXECUTE | ✅ Correct |
| SQLMap → HIGH → Commander Mailbox | Yes | Commander Mailbox | ✅ Correct |
| Agent writes delta to ASG | Yes — [Tech][Endpoint][Vuln] nodes | [Tech node][Endpoint node][Vuln node] | ✅ Correct |
| Working context discarded | Explicit "DISCARDED" note | Explicit "DISCARDED" note | ✅ Correct |
| Commander reads new Vuln nodes → seeds Chain-01 | Yes | Yes | ✅ Correct |

No errors. Slide 7 faithfully reproduces module-08 Figure 2A.

---

## Workflow 5 — Risk Gate Decision Tree (Slide 9 vs. Module 04 Figure 1A)

| Step | module-08 Says | Slide 9 Says | Verdict |
|---|---|---|---|
| PreToolUse hook fires first | Yes — before scope check | Shown correctly first | ✅ Correct |
| Scope check before classification | Yes | Yes | ✅ Correct |
| LOW path: execute immediately | Yes | Yes | ✅ Correct |
| MED path: LLM Classifier | Fast filter → CoT pass | Fast Filter → CoT pass | ✅ Correct |
| HIGH path: Commander Mailbox | Yes | Yes | ✅ Correct |
| ESCALATE from MED → Mailbox | Yes (Classifier can escalate) | ESCALATE → Commander Mailbox | ✅ Correct |
| PostToolUse hook after ASG write | Yes | Shown after adapter | ✅ Correct |
| Agent gets compact summary only | Yes | "Agent receives compact summary only" | ✅ Correct |
| **6 lifecycle hooks shown** | 6 hooks defined in §8 | Only 2 shown (PreToolUse, PostToolUse) | ⚠️ 4 hooks absent |

Minor gap: 4 of 6 lifecycle hooks (PreAgentSpawn, PostAgentReturn, PreAPGUpdate, PostMissionTerminate) are not shown. Given slide space constraints, this is acceptable as a simplification.

---

## Workflow 6 — Planning Cycle (Slide 13 vs. Module 06 Figure 1A)

| Step | module-08 Says | Slide 13 Says | Verdict |
|---|---|---|---|
| OBSERVE ASG → OBSERVE APG → REASON → DECIDE | Yes | Yes | ✅ Correct |
| DECIDE branches: EXPLORE / VALIDATE / BOTH | Yes | ASG gaps / both / APG chains | ✅ Correct |
| Cycle Guard check after agent executes | Yes | After AGENT EXECUTES | ✅ Correct |
| Cycle Guard → Reflector OR Force Re-Plan | Yes | → REFLECTOR or FORCE RE-PLAN | ✅ Correct |
| UPDATE ASG → UPDATE APG → TERM CHECK | Yes | UPDATE ASG → UPDATE APG → TERM CHECK | ✅ Correct |
| Term check: both conditions must be true | Yes | "ASG exhausted AND APG resolved" | ✅ Correct |
| Report Agent spawned on term | Yes | Not explicitly shown on slide 13 (shown on slide 14) | ✅ Acceptable (slide 14 covers it) |

No errors. The planning cycle is correctly and completely reproduced.

---

## Workflow Consistency Summary

| Workflow | Errors Found |
|---|---|
| shopvault.io Mission Timeline | Chain-04 in wrong phase |
| Chain-01 Traceability | None |
| Agent Spawn Lifecycle | None |
| Risk Gate Decision Tree | 4 lifecycle hooks not shown (minor) |
| Planning Cycle | None |
| Commander Decision Log | None |

**Total workflow errors:** 1 critical (Chain-04 phase placement)  
**Total minor gaps:** 2 (Nuclei output absent from narrative; 4 hooks not shown)
