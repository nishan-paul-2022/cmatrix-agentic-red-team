# CMatrix — Presentation Script

> **How to use this script:**
> Each section corresponds to one slide. Read the script naturally — don't rush, don't read robotically. Pause after key points. Make eye contact. Own the material.

---

## 🎤 Slide 01 — Title Slide

*[Pause for 2 seconds after displaying the slide. Let the title land.]*

Good morning, everyone. Today we're presenting our research project: **CMatrix** — a Dual-Graph-Guided, LLM-Orchestrated Multi-Agent Framework for Autonomous Vulnerability Assessment and Penetration Testing.

That's a dense title — but by the end of this presentation, every single word in it will make perfect sense.

The core question driving this work is: *can we build a system that doesn't just run security tools automatically, but actually reasons about security — the way a skilled human penetration tester does?*

What we've built is our attempt to answer that question. Let's get into it.

---

## 🎤 Slide 02 — The Problem

Before we explain what CMatrix is, we need to understand *why* it needed to exist in the first place. What's wrong with how things are done today?

Automated security testing isn't new. There are plenty of tools that scan systems, flag vulnerabilities, and produce reports. And recently, LLM-based systems have started entering this space. But they all share a fundamental limitation — and it's subtle.

**They have no structured model of the target.**

Think about what that means. When an existing system finishes a scan, it has a list of findings — "port 443 open," "WordPress 5.9.3 detected," "CVE-2022-21661 found." But it stores all of this in flat conversation history or a task queue. It has no graph, no structure, no relationships. It knows *what it did* — but not *what the target is* or *what can be done to it*.

This creates four specific failures, which you see on this slide:

**No structured world model** — they can't represent the target as a connected, living knowledge graph.

**No attack path reasoning** — they can't figure out which vulnerabilities chain together into a real attack. A skilled pentester doesn't just list weaknesses — they figure out how weakness A connects to weakness B to achieve impact C.

**Fragile re-planning** — because there's no formal model of the target, when something new is discovered, the system has no principled way to decide what to do next. Re-planning is ad-hoc.

**Arbitrary termination** — and perhaps most critically: when is the mission *done*? Existing systems stop when a timer expires or a task queue empties — not because the attack surface is genuinely exhausted.

The root cause of all four problems is the same: no structured model. CMatrix's solution is the dual-graph world model — which we'll see in a moment.

---

## 🎤 Slide 03 — Novel Contributions

This slide gives you a bird's-eye view of what's actually new in CMatrix. There are twelve research contributions — labeled C1 through C12.

I won't go through all twelve right now — we'll see most of them in context as we explain the system. But I want to highlight the ones that really define what CMatrix is.

**C1 — the dual-graph world model** — this is the foundational innovation. Two strictly separated graph structures, one for what was discovered, one for what can be done with those discoveries. No prior VAPT system maintains these as distinct structures with enforced ownership boundaries.

**C2 — graph-state-driven re-planning** — every re-plan fires on a formal, inspectable graph event. Not a timer. Not a guess. A specific change in the world model.

**C3 — APG attack chain lifecycle** — attack chains are first-class entities in our system. They have risk scores, they go through a lifecycle, and every step is linked to real evidence. We can prove every claim we make.

**C8 — dual-graph termination** — the mission ends precisely when the attack surface is exhausted AND all attack chains are in a terminal state. No other autonomous VAPT system can express both conditions simultaneously.

**C10 and C11** — cross-mission learning. CMatrix accumulates validated exploitation knowledge across every mission it runs. It gets smarter. No prior system in the literature does this — every existing system resets to zero knowledge on each new engagement.

These contributions aren't incremental tweaks. They represent a fundamentally different way of thinking about autonomous security assessment.

---

## 🎤 Slide 04 — System Architecture

Now let's look at how the system is actually structured. CMatrix has three tiers — you can see them on this slide.

**Tier One — Orchestration.**

At the top is the Operator, who configures the mission: the target, the scope, the assessment mode. This configuration flows to the Commander Agent.

The Commander is the brain of the entire system. It reads both graphs. It plans. It delegates. It approves high-risk operations. And critically — **it never runs tools itself**. Its job is pure reasoning and orchestration.

The Commander is governed by the VAPT Protocol Prompt — a structured document encoding the entire assessment methodology. Phase sequencing, re-planning rules, termination conditions — all in a versioned, swappable document. Different methodologies like OWASP Testing Guide or PTES can be switched in without touching any code.

**Tier Two — The Dual-Graph World Model.**

This is the heart of the architecture. Two separate knowledge layers:

The **Attack Surface Graph** — discovered reality. Everything confirmed about the target: domains, hosts, ports, services, technologies, endpoints, parameters, vulnerabilities, evidence. Contains only facts. Never hypotheses.

The **Attack Path Graph** — inferred opportunity. Attack chains built by the Commander from ASG facts. Risk scores, priorities, validation status. Contains only reasoning. Never raw scan data.

These two graphs are strictly separated. No agent crosses the boundary. And that separation is what makes the architecture sound.

**Tier Three — Specialized Agents and the Tool Adapter Layer.**

Six specialized agents each handle a specific domain of responsibility. Every tool invocation passes through the Tool Adapter Layer and the Tool Risk Gate. Low-risk tools execute immediately. Medium-risk tools need LLM classifier approval. High-risk tools — exploits, destructive operations — need the Commander's explicit approval through a mailbox mechanism. That mailbox is also where a human operator can be inserted for supervised assessments.

---

## 🎤 Slide 05 — Dual-Graph World Model

Let's go deeper on the dual-graph world model, because this is the architectural foundation everything else is built on.

On the left you see the **ASG — the Attack Surface Graph**. This answers one question: *what does the target look like?* It's a living knowledge graph of everything discovered. On this slide, you can actually trace a real example from our shopvault.io assessment — a domain resolving to a host, with ports, services, a technology stack, endpoints, parameters, vulnerabilities, and finally evidence artifacts.

The ASG grows continuously as agents discover things. Nodes are connected by typed edges: `has_host`, `has_port`, `runs`, `uses`, `has_endpoint`, `has_parameter`, `affected_by`, `validated_by`. Every relationship is explicit.

The golden rule of the ASG: **it contains only confirmed discovered facts. Never hypotheses.**

On the right is the **APG — the Attack Path Graph**. This answers a different question: *what can be done to the target?* It's built entirely by the Commander through active reasoning over ASG state. Looking at the example on this slide — Chain-01, risk score 9.1, status VALIDATED — you can see a complete attack chain: Step 1 uses SQLMap to confirm SQL injection, Step 2 extracts admin credentials, Step 3 uses Metasploit to achieve full remote code execution, and the Impact node confirms full server access and customer PII exposure. Each step has a `supported_by` edge pointing to an ASG Evidence node — a real screenshot proving the step succeeded.

Between them: **strict separation**. Discovery agents write only to the ASG — they never reason about chains. The Commander writes only to the APG — it never runs tools. No agent crosses this boundary.

This separation eliminates a whole class of errors: confusing facts with hypotheses, letting attack reasoning contaminate environmental observation. It's a simple principle with profound consequences for system reliability.

---

## 🎤 Slide 06 — Agent Architecture

CMatrix uses six specialized agents, all coordinated by the Commander. The key design principle for all of them is **context isolation**.

Every agent is spawned fresh for its task. It receives only what it needs: the slice of the ASG relevant to its assignment, the relevant APG slice if applicable, the restricted set of tools it's authorized to use, and a specific task specification from the Commander's current plan.

When the agent completes its task, it returns only structured output — new ASG nodes and edges. Its entire working context is then discarded. Nothing raw passes back to the Commander.

Why does this matter? Three reasons. The Commander's context stays clean — it never sees raw tool output or verbose agent reasoning. Agents can't contaminate each other — Agent A's massive scan output can't leak into Agent B's context. And rejected high-risk tool calls vanish — they don't bias the Commander's future planning.

Let me walk you through the agents quickly.

The **Recon Agent** maps the external attack surface. It uses Amass for subdomain discovery, httpx to confirm live hosts, and Nmap for port and service scanning. It writes Domain, Host, Port, and Service nodes to the ASG.

The **Analysis Agent** goes deeper — it fingerprints technologies with WhatWeb, discovers hidden resources with Gobuster, fuzzes APIs with ffuf, runs CVE templates with Nuclei, and actively scans web applications with OWASP ZAP. It writes Technology, Endpoint, Parameter, and Vulnerability nodes.

The **Research Agent** is on-demand intelligence — it queries NVD, Exploit-DB, and GitHub to enrich vulnerability findings with real-time CVE data, CVSS scores, and PoC availability. Crucially, it's the only agent authorized to make outbound requests to external networks.

The **Validation Agent** proves that vulnerabilities are real. It runs controlled exploitation using SQLMap and Metasploit. When a step fails, it doesn't give up — it enters a structured self-debugging loop: diagnose why it failed, contextualize by querying the ASG for more information, adapt the approach, and retry — up to a configurable cap.

The **Evidence Agent** captures proof: screenshots, response captures, exploitation outputs. It links everything back to the ASG with `validated_by` edges.

And the **Report Agent** reads the complete dual graph and produces the final professional penetration test report — findings, attack chains, evidence, remediation guidance, all in one.

---

## 🎤 Slide 07 — Offensive Tool Catalogue

This slide shows the 11 offensive security tools CMatrix integrates. These are all industry-standard tools used by professional penetration testers — CMatrix doesn't reinvent any of them. What it does is orchestrate them intelligently.

Notice the structure: tools are grouped by phase and by the agent that operates them.

**Amass, httpx, and Nmap** belong to the Recon Agent — they handle external discovery, live host validation, and port scanning respectively.

**WhatWeb, Gobuster, ffuf, Nuclei, and OWASP ZAP** belong to the Analysis Agent — they handle technology fingerprinting, directory brute-forcing, API fuzzing, template-based vulnerability scanning, and active web application testing.

**SQLMap and Metasploit** belong to the Validation Agent — these are the exploitation tools. They require the highest level of authorization and go through the High-risk tier of the Tool Risk Gate.

**EyeWitness** belongs to the Evidence Agent — it captures visual proof of everything the Validation Agent confirmed.

The critical design constraint: every single one of these tools is wrapped in a Tool Adapter. Agents never invoke tools directly. The adapter handles command syntax, parses raw output, and returns structured ASG-ready data. This means agents reason about *targets and goals* — not command flags and output formats. And it means tools can be replaced without touching agent logic.

The line at the bottom of this slide captures the safety philosophy: *no irreversible offensive operation executes without Commander-level scope validation.*

---

## 🎤 Slide 08 — Real-World Scenario

Now let's see the whole system in action. This is a real walkthrough of CMatrix assessing `shopvault.io` — a mid-sized e-commerce company's external infrastructure — in black-box mode. Zero prior knowledge. The operator configures the root domain and scope, presses start. Everything else is autonomous.

**Phase 1 — Reconnaissance.**

The Commander reads the initial ASG: just one seed node — the root domain `shopvault.io`. It spawns the Recon Agent.

Amass discovers 14 subdomains including api, admin, staging, and pay. httpx probes all 14 and confirms 11 are live — notably, staging returns an unexpected 200 response, which is already suspicious. Nmap scans all 11 hosts and finds ports 80, 443, 8080, and 8443, plus an expired TLS certificate on pay.shopvault.io.

The Recon Agent writes 37 new nodes to the ASG and returns. Its context is discarded.

**Phase 2 — Analysis and Intelligence.**

The Commander re-reads the ASG and spawns the Analysis Agent. WhatWeb identifies WordPress 5.9.3 on the main site and a Django API. The Commander immediately spawns the Research Agent to look up WordPress 5.9.3 CVEs. NVD returns CVE-2022-21661 — SQL injection via WP_Query, CVSS 8.8, public PoC confirmed. The Commander seeds its first APG chain: Chain-01.

Gobuster then discovers something alarming: `/backup/db_export_2023.sql` — an exposed database dump — sitting publicly accessible on the admin subdomain. ffuf fuzzes the Django API and finds the user_id parameter accepts unsanitized input. The Commander seeds Chain-02: IDOR on the orders endpoint. OWASP ZAP finds SQL error messages on staging login. Chain-03 is seeded.

At the end of Phase 2: 61 new ASG nodes and 3 attack chains in the APG, all in HYPOTHESIZED state.

**Phase 3 — Validation.**

The Commander reads the APG. Chain-01 has the highest risk score at 8.8 — it goes first.

The Validation Agent is spawned with Chain-01. SQLMap targets the WordPress WP_Query injection — this is a High-risk call. The Commander receives it in its mailbox, evaluates, and approves. SQLMap confirms the injection and extracts the admin password hash. Metasploit uses the cracked hash to authenticate and deploys a web shell. Full remote code execution achieved. Chain-01 is VALIDATED — risk score escalated to 9.1 after RCE is demonstrated. Evidence Agent captures screenshots.

Chain-02: SQLMap on the user_id parameter confirms IDOR — any customer's orders are accessible without authentication. VALIDATED.

Chain-03: Blind SQLi on staging login extracts database credentials. The Commander notices credential overlap with production and flags an additional Impact node. VALIDATED.

Chain-04: The exposed database backup file is simply downloaded via HTTP GET. Trivially VALIDATED.

**Phase 4 — Reporting.**

The Commander confirms the termination condition: all 11 ASG hosts explored, all 4 APG chains in terminal state. The Report Agent is spawned. It reads the complete dual graph and produces a professional penetration test report.

The numbers on this slide tell the story: 14 subdomains, 11 live hosts, 28 open ports, 19 endpoints, 11 vulnerabilities, 4 validated chains. Zero manual commands.

---

## 🎤 Slide 09 — Attack Chain Lifecycle

This slide goes deeper on how attack chains work in the APG — the lifecycle and the self-debugging mechanism.

Every attack chain begins life as **HYPOTHESIZED** — the Commander infers it's possible from ASG Vulnerability nodes. It hasn't been tested yet.

As the Validation Agent confirms individual steps, the chain advances to **PARTIALLY VALIDATED** — some steps confirmed, not complete yet.

When every step has evidence and the impact is demonstrated, the chain reaches **VALIDATED** — mission success for that chain.

If a required step fails after the maximum retries, the chain is **RULED OUT** — not exploitable as hypothesized. The Commander re-prioritizes and moves on.

On the right side of this slide you see the self-debugging loop in detail. When a ChainStep fails, the Validation Agent doesn't immediately give up. It cycles through Attempt → Diagnose → Contextualize → Adapt → retry. The Diagnose step analyzes *why* it failed: wrong parameter, authentication required, version mismatch, payload encoding issue. The Contextualize step queries the ASG for additional attributes that might resolve the issue. Adapt modifies the tool invocation accordingly. Then it retries — up to 3 times by default. If the cap is reached, the step is marked RULED_OUT and the failure reason is written back to the ASG as a structured annotation on the Vulnerability node.

This bounded retry loop is the balance between two failure modes: giving up too early on a legitimate vulnerability due to a transient error, and burning infinite time on an exploit that will never work.

The bottom of this slide shows the actual chain priority order from the shopvault.io mission: Chain-01 at 9.1, Chain-03 at 8.1, Chain-02 at 7.5, Chain-04 trivial. The Commander pursues them in this exact order and re-ranks after every status change.

---

## 🎤 Slide 10 — Cross-Mission Learning

One of CMatrix's most distinctive properties is that it learns across missions. This slide explains how.

Most autonomous systems — in pentesting and in other domains — start from zero knowledge on every run. They have no memory that persists across sessions. Whatever was learned in Mission 1 is gone by Mission 2.

CMatrix breaks this pattern with two mechanisms.

**The Cross-Mission Experience Store** — C10 — is a persistent, RAG-backed knowledge base that survives across missions. When a mission ends, the Report Agent writes a structured record of every validated attack chain into the store: the target technology fingerprint, the vulnerability, the tool parameters that worked, the chain sequence, the outcome.

When the next mission starts, immediately after the Recon Agent writes the first Technology nodes to the ASG, the Commander queries this store. It retrieves records from past missions on similar technology stacks and injects them as candidate chain hypotheses — pre-validated patterns that inform APG seeding before deep enumeration even begins.

**The Attack Strategy Library** — C11 — goes a level higher. It's not raw records; it's generalized procedures. When the same technology fingerprint produces a validated attack chain across two or more independent missions, the Commander triggers crystallization: a scoped LLM call generalizes the specific chain parameters into a named, parameterized strategy with a confidence score.

For example: `STRAT-WP-SQLI-001` — "WordPress 5.x SQL injection via WP_Query, confirmed across 4 independent missions, Metasploit module available." This strategy is retrieved at the start of any mission that fingerprints WordPress 5.x and injected as a pre-ranked APG AttackChain seed — prioritized above zero-prior chains because it carries a validated track record.

The table on the right side of this slide shows the distinction: the Experience Store holds granular, per-mission records; the Strategy Library holds generalized, confidence-scored procedures.

Why does this matter? Because CMatrix becomes measurably more efficient on repeat target-type engagements. The fourth time it assesses a WordPress deployment, it doesn't start from scratch. It starts from a library of validated attack patterns with known confidence scores. No other autonomous VAPT system in the literature does this.

---

## 🎤 Slide 11 — Inspirations and References

CMatrix didn't emerge in isolation. It was designed with close reference to five academic papers and three open-source repositories from the autonomous security space. This slide maps each one to its specific contribution to CMatrix's architecture.

We believe in crediting our intellectual sources precisely. So let me walk through them.

**PentestGPT** from USENIX Security '24 taught us the "parse before you reason" principle — condense noisy tool output before it enters the LLM's reasoning context. CMatrix extends this: parsed output becomes permanent ASG graph state, not just a context summary.

**AutoAttacker** introduced within-mission experience reuse — storing successful attack subtasks and retrieving them later in the same engagement. CMatrix generalizes this concept to cross-mission scope in C10.

**Teams of LLM Agents (HPTSA)** showed that injecting task-specific documents into sub-agent contexts at spawn time improves performance by up to 2.1 times. CMatrix's Vulnerability-Class Knowledge Injection does exactly this — giving specialist agents curated offline expert knowledge matched to their assigned vulnerability class.

**PentestAgent** demonstrated an execution agent that self-diagnoses failed exploit attempts and corrects its approach. CMatrix's Validation Agent self-debugging loop comes directly from this pattern.

**VulnBot** showed that agents should hand off structured summaries, not raw history. CMatrix's context-isolated agents return only ASG deltas — never their verbose execution traces.

From the open-source side: **PentAGI** gave us the Cycle Guard and Reflector pattern for detecting and correcting agent fixation.

**Claude Code** gave us two things: the two-stage fast-filter plus chain-of-thought classifier for medium-risk tool approval, and the named lifecycle hook architecture for operator intervention.

And **Hermes Agent** gave us both the crystallization mechanism underlying the Attack Strategy Library and the trajectory export concept underlying C12.

For each of these, we know exactly what we took, what we adapted, and what we added. That's the standard we hold ourselves to.

---

*[End of presentation script]*

---

> **Closing note:** If the supervisor asks a question you don't immediately know the answer to, that's fine. Say: "That's a good point — in the current design, [best available answer]. This is something we'd want to address more rigorously in the implementation phase." Confidence is not about knowing everything. It's about owning what you know and being clear about what you don't.
