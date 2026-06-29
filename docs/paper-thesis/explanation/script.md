# CMatrix — Presentation Script (Complete, All 19 Slides)

> **How to deliver this script:**
> This is not a document to read word-for-word. It's a script to internalize. Know it so well that you can say any sentence in it without looking at the page. Pause after strong statements — let them breathe. Make eye contact when you say the big claims. Own the material completely. You built this. Speak like you built it.

---

## 🎤 Slide 01 — Title Slide

*[Pause 2–3 seconds. Let the room settle. Make eye contact before speaking.]*

Good morning, Professor. Today we're presenting **CMatrix** — a Dual-Graph-Guided, LLM-Orchestrated Multi-Agent Framework for Autonomous Vulnerability Assessment and Penetration Testing.

That title is intentionally precise. Every word in it earns its place. And by the time we finish this presentation, you'll understand exactly what each word means and why we chose it.

Let me start with the question that drove this entire research: can a machine truly *reason* about security — not just execute tools, not just flag findings, but actually think through an attack the way a skilled human penetration tester does?

Answering that question is what CMatrix is built to do. Let's get into it.

---

## 🎤 Slide 02 — The Problem

Before we explain what CMatrix *is*, we need to understand the precise problem it was designed to solve.

Automated security testing has existed for decades. And in recent years, LLM-based systems have begun entering this space — using large language models to coordinate tools and produce security findings. These systems are impressive. But they all share one fundamental, structural flaw.

**They have no model of the target.**

Think about what that means in practice. When a modern automated VAPT system finishes a scan, it has a log of what it did: "ran Nmap, found port 443, ran Nuclei, found CVE-2022-21661." But that information lives in flat conversation history — or a task queue — with no structure, no relationships, no graph. The system knows *what it did* — but it cannot represent *what the target is* or *what can be done to it*.

This one design gap produces four cascading failures.

**First: no structured world model.** The system can't build a connected, queryable picture of the target environment. There's no concept of "this host runs this service which has this vulnerability which is linked to this endpoint."

**Second: no attack path reasoning.** A professional penetration tester doesn't just collect weaknesses — they figure out how Vulnerability A connects to Endpoint B to achieve Impact C. Existing systems can't do this. They log findings, not attack chains.

**Third: fragile re-planning.** When something new is discovered mid-mission, there's no principled way to decide what to do next. Re-planning is ad-hoc — a guess, not a graph-grounded decision.

**Fourth: arbitrary termination.** This is the most damaging failure. When is a penetration test *done*? Existing systems stop when a timer expires or a task queue goes empty — not because the attack surface is genuinely exhausted and every opportunity has been tested. That's not completeness. That's convenience.

The root cause of all four problems is the same: **no structured world model**. CMatrix's solution is the dual-graph architecture — and everything we present today builds from that foundation.

---

## 🎤 Slide 03 — Foundations and Inspirations

CMatrix was not designed in isolation. Before we wrote a single line of architecture, we conducted a deep review of the state of the art — five academic papers and three production open-source repositories. This slide maps exactly what we learned from each one and where it lives in our design.

We believe research credit should be precise. So let me walk through these quickly.

**PentestGPT**, from USENIX Security 2024, introduced the principle of parsing raw tool output *before* it enters the reasoning context. We took this and extended it — in CMatrix, parsed output doesn't just become a summary, it becomes permanent graph state in the ASG.

**AutoAttacker** showed that an experience manager can reuse successful attack subtasks *within* a mission. We generalized this to *across* missions — that's the Cross-Mission Experience Store you'll see later.

**HPTSA**, the Teams of LLM Agents paper, demonstrated that injecting task-specific documents at agent spawn time improves zero-day exploitation by up to 2.1×. CMatrix's Vulnerability-Class Knowledge Injection is directly based on this finding.

**PentestAgent** from AsiaCCS 2025 gave us the self-debugging loop pattern — the idea that when a Validation Agent fails, it should diagnose, contextualize, adapt, and retry rather than immediately giving up.

**VulnBot** showed that agents should hand off structured summaries, not raw history. That's the foundation of our context-isolated agent design.

From the open-source side: **PentAGI** gave us the Cycle Guard and Reflector for detecting agent fixation. **Claude Code** gave us the two-stage LLM permission classifier and the named lifecycle hook architecture. And **Hermes Agent** gave us both the skill crystallization mechanism and the trajectory export concept.

For each of these, we know exactly what we took, what we adapted, and what we added. This is the intellectual foundation CMatrix is built on.

---

## 🎤 Slide 04 — Scope

Before diving into the architecture, let's be clear about the boundaries of what CMatrix assesses — and what it deliberately does not.

CMatrix operates in two modes. **Black-Box** — where the operator provides only a root domain and scope declaration, and the system discovers everything from zero. And **Grey-Box** — where partial knowledge like known IP ranges or credentials is provided upfront, pre-seeding the ASG with Host nodes before assessment begins.

Within those modes, CMatrix covers three target categories: **network infrastructure** — hosts, ports, services; **web applications** — HTTP/HTTPS services, CMSes; and **REST APIs** — endpoints, parameters, authentication surface.

And critically: every single tool execution is gated against the declared scope *before* it fires. Nothing runs out-of-scope. The Risk Gate enforces this unconditionally.

What's explicitly out of scope: white-box source code analysis, mobile applications, cloud and IoT infrastructure, wireless networks, Active Directory, and physical or social engineering. These are not limitations we're hiding — they're intentional boundaries that keep the thesis focused and the evaluation clean.

The key point: the operator configures CMatrix once — target, scope, mode — presses start, and does not touch it again. Everything that follows is fully autonomous.

---

## 🎤 Slide 05 — System Architecture

Now let's look at how CMatrix is actually structured. The architecture has three tiers — orchestration, the dual-graph world model, and the specialized agents with tool execution layer.

**Tier One — Orchestration.**

At the top sits the Operator, who configures the mission: target, scope, assessment mode. This configuration flows directly to the **Commander Agent**.

The Commander is the brain of the entire system. It reads both graphs. It plans. It delegates. It approves high-risk operations. And here is the most important thing to understand about the Commander: **it never runs tools**. Not once. Its job is pure reasoning and orchestration.

The Commander is governed by the **VAPT Protocol Prompt** — a structured, versioned natural-language document that encodes the entire assessment methodology. Phase sequencing, re-planning triggers, termination conditions, tool selection heuristics — all defined in this document. This means you can swap out the methodology — OWASP Testing Guide, PTES, custom red-team workflow — without changing a single line of orchestration code. That's research contribution C7: methodology-as-configuration.

**Tier Two — The Dual-Graph World Model.**

This is the heart of the architecture. Two strictly separated knowledge layers:

The **Attack Surface Graph** — discovered reality. Every confirmed fact about the target: domains, hosts, ports, services, technologies, endpoints, parameters, vulnerabilities, evidence artifacts. It contains only confirmed facts. Never hypotheses.

The **Attack Path Graph** — inferred opportunity. Attack chains built by the Commander through active reasoning over ASG state. Risk scores, chain priorities, validation status. It contains only attack reasoning. Never raw scan data.

Strict separation. Enforced write ownership. No agent crosses this boundary.

**Tier Three — Specialized Agents and the Tool Adapter Layer.**

Six specialized agents each own a specific domain of responsibility. Every tool invocation — without exception — passes through the Tool Adapter Layer and the Risk Gate. Low-risk passive tools execute immediately. Medium-risk active tools require LLM classifier evaluation. High-risk exploit tools require the Commander's explicit mailbox approval. That mailbox is also the architectural insertion point for human-in-the-loop supervision — no code change required.

---

## 🎤 Slide 06 — Dual-Graph World Model

Let's go deeper on the dual-graph, because this is the architectural foundation everything else is built on.

On the left, the **Attack Surface Graph**. Ask yourself: what does a human penetration tester *know* about a target as they work? They know what hosts exist. What ports are open. What services are running. What technologies are in use. What endpoints are exposed. What parameters those endpoints accept. What vulnerabilities are present. And what evidence exists to prove each finding.

The ASG encodes exactly that knowledge as a living, queryable graph. On this slide you can trace a real example from our shopvault.io assessment. The domain resolves to three hosts. One host exposes port 443 running Nginx 1.18. That service hosts WordPress 5.9.3. The endpoint `/wp-admin` is affected by CVE-2022-21661, a SQL injection vulnerability with CVSS 8.8. That vulnerability is validated by `sqli-extract.txt`. Every relationship is an explicit, typed edge in the graph.

**The ASG is not a log. It is not a task list. It is a structural model of the target environment.** Every node is a confirmed discovered fact. Every edge is a confirmed relationship. Hypotheses are never written here.

On the right, the **Attack Path Graph**. This is where the Commander *reasons*. When the Commander reads a Vulnerability node in the ASG, it asks: can this be exploited? Does it chain with other vulnerabilities? What's the likely business impact? The answers become AttackChain nodes in the APG.

You can see the four chains from shopvault.io on this slide. Chain-01, the highest priority at risk score 9.1, represents the full SQLi-to-RCE path through WordPress. Each chain has a risk score, a validation status, and a priority ranking. The Commander re-ranks this priority queue every time any chain's status changes.

**The Separation Principle** — and this is what makes the architecture sound — is this: discovery agents write only to the ASG and never reason about attack chains. The Commander writes only to the APG and never runs tools. Each layer is authoritative for exactly one type of knowledge. This eliminates the class of errors that plague flat-memory systems: conflating facts with hypotheses, or letting attack reasoning contaminate environmental observation.

---

## 🎤 Slide 07 — Agent Architecture

CMatrix has seven agents — the Commander plus six specialists. Each specialist is **context-isolated**: spawned fresh for its task, given only the slice of the dual graph it actually needs, and returning only structured graph output when it's done. Its working context is then discarded completely.

Let me walk through each agent.

**The Commander** — orchestrating brain. Reads the dual graph, plans, delegates, approves high-risk operations. It is the only agent that writes to the APG. It never runs tools.

**The Recon Agent** — external reconnaissance. Amass, httpx, Nmap. Discovers subdomains, validates live hosts, identifies open ports and services. Writes Domain, Host, Port, and Service nodes to the ASG.

**The Analysis Agent** — deep enumeration and vulnerability discovery. WhatWeb, Gobuster, ffuf, Nuclei, OWASP ZAP. Fingerprints technology stacks, finds hidden endpoints, fuzzes API parameters, runs template-based vulnerability checks. Writes Technology, Endpoint, Parameter, and Vulnerability nodes.

**The Research Agent** — the intelligence specialist. It is the *only* agent authorized to make outbound requests to external sources. When the Commander encounters an unknown CVE or an unrecognized technology version, it spawns the Research Agent with a specific query — a CVE ID, a technology-version string — and the Research Agent retrieves live intelligence from NVD, Exploit-DB, and GitHub. The result is written back as enriched Vulnerability node attributes. No raw web content ever enters the LLM context — only the structured intelligence record.

**The Validation Agent** — proves vulnerabilities are real. SQLMap, Metasploit. It doesn't discover — it *confirms*. Receives a specific APG AttackChain and executes controlled exploitation to validate each ChainStep in sequence, running a structured self-debugging loop on failures.

**The Evidence Agent** — EyeWitness. Captures screenshots and response artifacts for every validated finding. Links Evidence nodes to the ASG via `validated_by` edges.

**The Report Agent** — reads the complete dual graph at mission end and produces the final penetration test report. No tools. No decisions. Pure translation of graph state to human-readable output.

Now let's talk about the **Context Isolation Model** on the left. When the Commander spawns a specialist, it provides exactly five things and nothing else: the ASG slice relevant to the task, the APG slice if applicable, the authorized tool set, the task specification, and vulnerability-class knowledge documents for Analysis and Validation agents. When the agent returns, it provides one thing: a structured ASG delta — new nodes and edges only.

This produces three critical properties. Commander context stays clean — it never sees thousands of lines of raw tool output. Agents can't contaminate each other — Agent A's verbose execution history never appears in Agent B's context; knowledge passes only through the ASG. And rejections don't bias planning — when the Commander rejects a high-risk tool call, that rejection never appears in the Commander's own reasoning context and cannot skew future decisions.

The result: long missions with many agents produce the same reasoning quality as single-agent tasks. Context quality does not degrade with mission complexity.

---

## 🎤 Slide 08 — Context-Isolated Agent Spawn Lifecycle

This slide shows the exact sequence diagram of a single agent spawn — from Commander decision to ASG write to context discard. Let me trace through it.

The Commander reads the dual graph, decides the next action, and issues a `spawn` call to a specialist agent, delivering the scoped context package we just described.

The agent begins executing. It calls WhatWeb — a **Low-risk** tool. The Risk Gate checks scope: target is in declared scope, tool is authorized. It executes immediately. The Tool Adapter runs WhatWeb, parses the raw output, extracts structured findings — "WordPress 5.9.3, WooCommerce, Nginx 1.18" — and returns only that structured record. Raw output is discarded.

The agent then calls Gobuster — a **Medium-risk** tool. The Risk Gate routes this to the LLM Permission Classifier. The classifier evaluates three axes: is the target in scope? Is this call consistent with the active APG chain? Are there any parameter anomalies suggesting scope drift or injection? The classifier returns `EXECUTE`. Gobuster runs. Structured findings returned. The endpoint `/backup/db_export_2023.sql` is discovered and written as a node to the ASG.

The agent then calls SQLMap — a **High-risk** tool. The Risk Gate routes this to the **Commander Mailbox**. The Commander receives an approval request: tool, target, parameters, rationale, active chain context. The Commander evaluates: target is in scope, CVE is confirmed, chain priority is highest, parameters look clean. It approves. SQLMap executes.

When the agent finishes its full task, it writes the complete ASG delta — Technology node, Endpoint node, Vulnerability node — and returns it to the Commander. The Commander reads the new Vulnerability node and seeds APG Chain-01.

The agent's working context — every line of tool output, every intermediate reasoning step, every failed attempt — is **discarded**. It is gone. The only thing that persists is the structured ASG delta.

This is what makes CMatrix scalable. Intelligence accumulates in the graph. Context bloat doesn't accumulate anywhere.

---

## 🎤 Slide 09 — Offensive Tool Catalogue

CMatrix integrates eleven industry-standard offensive security tools. These aren't toys or simulations — they are the exact tools professional penetration testers use in real engagements. The difference is that CMatrix operates them autonomously through the Tool Adapter Layer, so agents reason about *targets*, not command syntax.

**Phase 1 — Reconnaissance** uses three tools. **Amass** for subdomain enumeration — DNS brute-forcing, certificate transparency logs, passive OSINT. **httpx** for live host probing — validates which discovered hosts actually respond, identifies web server headers and TLS details. **Nmap** for port and service scanning — fingerprints services, detects OS, can run NSE scripts for vulnerability detection on open services.

**Phase 2 — Analysis** uses five tools. **WhatWeb** fingerprints technology stacks — CMS versions, frameworks, JavaScript libraries — and seeds the ASG with Technology nodes that trigger Research Agent queries. **Gobuster** runs wordlist-based directory brute-forcing to find hidden paths, admin panels, and exposed files. **ffuf** is a fast fuzzer for API route discovery, parameter fuzzing, and virtual host enumeration. **Nuclei** runs template-based scanning, matching discovered technologies against thousands of CVE and misconfiguration templates. **OWASP ZAP** actively crawls and tests for the OWASP Top 10 — XSS, CSRF, injection flaws, authentication weaknesses.

**Phase 3 — Validation** uses two exploit tools. **SQLMap** for automated SQL injection detection and exploitation — confirms injection points, extracts data, tests for OS-level access. **Metasploit** for exploit execution — validates APG ChainSteps, demonstrates impact, achieves proof of exploitation.

**Phase 3 — Evidence** uses one tool. **EyeWitness** for headless screenshot capture — visual proof artifacts linked to ASG Evidence nodes.

The key architectural point: **every tool is wrapped in a Tool Adapter**. Agents never call tools directly. This means tools can be swapped, updated, or replaced without touching any agent logic. And no irreversible offensive operation runs without Commander-level scope validation.

---

## 🎤 Slide 10 — Tool Adapter Layer

The Tool Risk Gate is one of CMatrix's most important safety and control mechanisms. Let me walk through the full lifecycle of a tool call.

An agent requests a tool call — say, Gobuster against `shopvault.io`. Before anything executes, the **PreToolUse hook** fires. This is an operator-registered interception point. The operator can block, modify, or let it continue.

Next: **Scope Check**. Is the target in declared assessment scope? Is this tool authorized for the current agent? If either check fails, the call is blocked here.

Then: **Risk Classification**. The gate assigns the call to one of three tiers.

**Low-risk** — passive discovery tools: Amass, httpx, WhatWeb, EyeWitness. These execute immediately after the scope check. No further evaluation required.

**Medium-risk** — active enumeration tools: Nmap, Gobuster, ffuf, Nuclei, ZAP. These go to the **LLM Permission Classifier**. A fast-filter pass checks obvious cases instantly. If it's not obvious, a brief chain-of-thought reasoning pass evaluates three axes: Scope Alignment — is the exact target node within declared scope? Chain Intent — is this call consistent with the active APG AttackChain being pursued? Parameter Safety — do the parameters exhibit any prompt injection patterns or scope drift? The classifier outputs a binary: `EXECUTE` or `ESCALATE`. If escalate, the call routes to the Commander Mailbox as if it were High-risk.

**High-risk** — exploit tools: SQLMap, Metasploit. These always go directly to the **Commander Mailbox**. The Commander receives the full approval request and returns one of three decisions: Approve, Reject, or Modify. A rejection is annotated to the APG. A modification adjusts parameters before the tool runs. An approval proceeds to execution.

After execution: the **Tool Adapter** runs the tool, parses raw output into structured JSON, and discards the raw output. Then the **PostToolUse hook** fires — logging, alerting, validating the write. The ASG receives the new nodes and edges. The agent receives only a compact summary of the result.

**Critical safety property**: no irreversible offensive operation executes without Commander-level scope validation. No medium-tier call executes without LLM classifier approval. This is not a soft constraint — it is enforced by architecture.

---

## 🎤 Slide 11 — Autonomous Planning Cycle

Now let's look at how the Commander actually operates. This is the cognitive engine of CMatrix — the loop it runs every single iteration.

Every cycle begins with two observations. The Commander reads the **ASG**: are there unexplored nodes? New vulnerability or technology discoveries? Unprobed endpoints? Then it reads the **APG**: are there hypothesized chains waiting to be validated? Have chain statuses changed? Does the priority queue need re-ranking?

With both observations in hand, the Commander **reasons**: given the full dual-graph state, what is the best next action?

If the ASG has gaps — unexplored hosts, unchecked endpoints — it spawns a Discovery Agent to explore them.
If the APG has high-priority chains awaiting validation — it spawns a Validation Agent against the top-ranked chain.
If both are pressing — it can dispatch **in parallel**, weighing priority across both paths simultaneously.

Every action routes through the Risk Gate. The agent executes, writes its ASG delta, and returns. The Commander updates both graphs. Then it runs the **Cycle Guard**: has the same tool call been repeated three or more times? That's fixation — force a re-plan. Are there repeated distinct failures? The Reflector provides corrective guidance rather than letting the agent burn its budget blind.

Then: **Termination Check**. Both conditions must be true simultaneously. We'll cover this properly in a moment.

On the right side of this slide, you see what triggers a re-plan. Every trigger is a specific, inspectable graph event:

ASG triggers: a new Vulnerability node that might seed an APG chain. A new Technology node that warrants a Research Agent spawn. A new Endpoint node that needs probing.

APG triggers: a chain advancing to PARTIALLY_VALIDATED — re-rank all chains. A chain reaching VALIDATED — move on to the next. A chain reaching RULED_OUT — remove it and re-prioritize.

This is the key claim: **every Commander decision traces to a graph event. Every re-plan is triggered by a node write. The system doesn't guess. It responds to structured evidence.**

---

## 🎤 Slide 12 — Dual Termination and Context Compaction

This slide covers two of the most technically distinctive properties of CMatrix. Let's take them in turn.

**Dual Termination.**

When is a penetration test *done*? This is not a trivial question. And the answer that prior systems give — "when the timer expires" or "when the task queue is empty" — is the wrong answer.

CMatrix requires both of the following to be simultaneously true before a mission terminates.

**Condition 1: ASG Exhausted.** Every node in the ASG — every Domain, Host, Port, Service, Technology, Endpoint, and Parameter — has been investigated by the appropriate specialist agent. No unexplored surface remains.

**Condition 2: APG Resolved.** Every AttackChain in the APG sits in a terminal state — either VALIDATED or RULED_OUT. No chain is left HYPOTHESIZED or PARTIALLY_VALIDATED.

You need both. Here's why each alone is insufficient:

ASG exhausted but APG has open chains? The attack surface is fully mapped, but chains are still in progress. Attack reasoning is unfinished. Not done.

APG resolved but new ASG nodes were just written? All chains are resolved, but new nodes might seed new chains. Not done.

Neither true? Obviously not done.

Only when *both* conditions are simultaneously satisfied does the Commander spawn the Report Agent. Only then is the mission complete.

No other autonomous VAPT system in the literature can express both conditions simultaneously. Timer-based systems stop mid-chain. Task-queue systems have no concept of APG resolution at all. This is research contribution C8 — and it's not an incremental improvement. It's a categorically different definition of completeness.

**Context Compaction.**

VAPT missions are long. Raw tool outputs are enormous. Without active management, LLM context windows overflow — and when they do, the system loses intelligence.

CMatrix's solution is a three-layer compaction scheme grounded in one insight: **the ASG is a lossless persistent store of all discoveries. Conversation history is expendable. The ASG is not.**

**Layer 1 — MicroCompact**, running on every tool call. Raw tool output is parsed at the Tool Adapter. Structured findings go to the ASG. Only a 3-line compact summary enters the agent's working context. Raw output is gone.

**Layer 2 — AutoCompact**, triggering at 60% context usage. Older conversation turns are summarized by a scoped LLM call. The summary replaces the raw turns. The agent continues without interruption.

**Layer 3 — FullCompact**, triggering at 85% context. The entire conversation history is replaced. The agent's context is reconstructed from scratch: current ASG snapshot, current APG priority chains, last N tool results. That's all that's needed. Nothing else matters. Because everything important already lives in the graph.

**FullCompact loses zero intelligence** — because no intelligence ever lived exclusively in the conversation. It was all written to the ASG the moment it was discovered. That's what makes this compaction scheme lossless. No general-purpose agent can claim this property.

---

## 🎤 Slide 13 — Attack Chain Lifecycle

This slide details the APG chain state machine — how attack chains are born, evolve, and terminate — and the Validation Agent's self-debugging mechanism.

Every chain begins as **HYPOTHESIZED**. The Commander reads a Vulnerability node in the ASG, infers a plausible exploitation path, and creates an AttackChain in the APG. It hasn't been tested. It's an informed hypothesis, not a confirmed attack.

As the Validation Agent confirms individual steps, the chain advances to **PARTIALLY VALIDATED**. Steps are proven. The chain is not yet complete end-to-end.

When every ChainStep has been confirmed with linked Evidence and the Impact is demonstrated, the chain reaches **VALIDATED** — mission success for that chain.

If a required step fails after maximum retries, the chain is **RULED OUT** — not exploitable as hypothesized. The failure reason is written back to the ASG as a structured annotation on the Vulnerability node. The Commander re-prioritizes and moves on.

Now — the **Validation Agent Self-Debugging Loop**. This is critical. When a ChainStep fails, the Validation Agent does not immediately give up. It enters a structured four-stage recovery sequence.

**Diagnose**: analyze *why* it failed. Wrong parameter format? Authentication required? Version mismatch? Payload encoding issue? The diagnosis is specific, not generic.

**Contextualize**: query the ASG for additional node attributes that might resolve the diagnosis. If authentication is required, is there a captured credential Evidence node? If the version is wrong, what does the Service node actually say?

**Adapt**: modify the tool invocation based on the diagnosis and additional context. New parameters, different payload, corrected module selection.

**Retry** — up to a configurable cap, defaulting to 3 attempts. If the cap is reached, the step is marked RULED_OUT and the Commander re-plans.

This bounded loop balances two real failure modes: giving up too early on a legitimate vulnerability due to a transient error, versus burning infinite time on an exploit that will simply never work. Three attempts is enough to overcome transient failures while preventing runaway loops.

The priority queue shown at the bottom right reflects the real shopvault.io mission: Chain-01 at 9.1, Chain-03 at 8.1, Chain-02 at 7.5, Chain-04 a trivial misconfiguration. The Commander pursues them in this exact order and re-ranks after every status change.

---

## 🎤 Slide 14 — Cross-Mission Learning

This slide presents one of CMatrix's most distinctive capabilities. And I want to frame it with a simple observation first.

Every autonomous VAPT system in the prior literature — PentestGPT, AutoAttacker, PentestAgent, VulnBot — starts from zero knowledge on every new mission. Whatever was learned in Mission 1 is completely gone by Mission 2. The system is amnesiac by design. That seems like an obvious limitation. CMatrix addresses it.

**The Cross-Mission Experience Store** — research contribution C10.

When a CMatrix mission terminates, the Report Agent writes a structured record for every validated attack chain into a persistent, RAG-backed knowledge base that survives across missions. Each record contains: the target technology fingerprint, the CVE, the successful tool parameters, the ChainStep sequence that achieved validation, and the mission outcome.

When the *next* mission starts — immediately after the Recon Agent writes its first Technology nodes to the ASG, before Analysis even begins — the Commander queries this store. It retrieves records from past missions on similar technology stacks. Those records become **candidate chain hypotheses** — pre-validated patterns that inform APG seeding. Instead of starting from zero, the Commander starts from a library of things that have already worked on similar targets.

This generalizes AutoAttacker's within-mission experience reuse mechanism to cross-mission scope. AutoAttacker reuses subtasks within one session. CMatrix accumulates across every mission ever run. That generalization — that cross-mission accumulation — is the contribution.

**The Attack Strategy Library** — research contribution C11 — goes a level further.

When the same technology fingerprint produces a validated AttackChain across two or more independent missions, the Commander triggers crystallization. A scoped LLM call generalizes the specific chain parameters from those missions into a named, parameterized attack procedure with a confidence score.

For example: `STRAT-WP-SQLI-001` — "WordPress 5.x SQL injection via WP_Query, confirmed across four independent missions, Metasploit module available, parameters template provided." This strategy is retrieved at mission start whenever WordPress 5.x is fingerprinted, and injected as a pre-ranked APG AttackChain seed. It's prioritized above zero-prior chains because it carries a validated track record, not just CVE severity.

The measurable claim: CMatrix becomes demonstrably more efficient on repeat target-type engagements. The fourth time it assesses a WordPress deployment, it doesn't rediscover the same chains from scratch — it begins from a library of validated attack patterns with known confidence scores. No other autonomous VAPT system in the literature does this.

---

## 🎤 Slide 15 — Real-World Scenario

Everything we've described architecturally comes together in this slide. Let me walk you through a complete end-to-end mission: a black-box assessment of `shopvault.io`, a fictional e-commerce platform. The operator provides the root domain and scope. Then presses start. Zero manual commands from this point forward.

**Phase 1 — Reconnaissance.**

The Commander reads the initial ASG: one seed node, the Domain `shopvault.io`. It spawns the Recon Agent.

Amass runs subdomain enumeration and discovers 14 subdomains — including api, admin, staging, and pay. httpx probes all 14 and confirms 11 are live. Notably, `staging.shopvault.io` returns an unexpected 200 response rather than being gated. Nmap scans all 11 hosts and finds ports 80, 443, 8080, and 8443 open. `pay.shopvault.io` has an expired TLS certificate.

The Recon Agent returns 37 new ASG nodes. Working context discarded.

**Phase 2 — Analysis and Intelligence.**

The Commander spawns the Analysis Agent. WhatWeb fingerprints the stack: WordPress 5.9.3 on the main site, Django API on api.shopvault, Nginx 1.18 as the reverse proxy.

The Commander reads the WordPress Technology node and immediately spawns the Research Agent: "WordPress 5.9.3 known CVEs." NVD returns CVE-2022-21661 — SQL injection via WP_Query, CVSS 8.8, public PoC on Exploit-DB, Metasploit module available. The Commander seeds Chain-01 in the APG. Status: HYPOTHESIZED. Risk score: 8.8.

Gobuster discovers `/backup/db_export_2023.sql` — an exposed database dump file — sitting publicly accessible. ffuf fuzzes the API and finds the `user_id` parameter accepts unsanitized input. Chain-02 seeded: IDOR, risk 7.5. OWASP ZAP finds SQL error messages on the staging login form. Chain-03 seeded: blind SQLi, risk 8.1.

61 new ASG nodes. 3 chains in the APG, all HYPOTHESIZED.

**Phase 3 — Validation.**

The Commander reads the APG. Chain-01 leads at 8.8. It spawns the Validation Agent.

SQLMap targets the WP_Query injection — High-risk call, Commander Mailbox. Approved. Injection confirmed, admin hash extracted. Metasploit cracks the hash, authenticates to WordPress admin, deploys a web shell via the theme editor. Full remote code execution. Chain-01: VALIDATED. Risk score escalated to 9.1 after RCE demonstrated. Evidence Agent captures four screenshots — database dump, admin panel, web shell, PII sample.

Chain-02: SQLMap on the `user_id` parameter confirms IDOR — any customer's orders are accessible without authentication. VALIDATED.

Chain-03: Blind SQLi on staging login extracts database credentials. The Commander notices credential overlap with production and flags additional impact: credential reuse risk. VALIDATED.

Chain-04: The exposed database backup file is simply retrieved via HTTP GET. Trivially VALIDATED.

**Phase 4 — Report.**

The Commander confirms: all 11 hosts explored, all 4 chains in terminal state. Dual-graph termination condition met. Report Agent spawned. It reads the complete ASG and APG and produces a full penetration test report.

The numbers on this slide: **14 subdomains. 11 live hosts. 28 open ports. 19 endpoints. 11 vulnerabilities. 4 validated chains. Zero manual commands.**

---

## 🎤 Slide 16 — Chain-01 Traceability

This slide demonstrates one of the most rigorous properties of CMatrix: **every claim in the final penetration test report is fully traceable through the dual graph, end to end.**

Let me walk you through the trace for Chain-01.

The chain begins in the ASG, in the discovery layer. The Recon Agent discovered the Domain `shopvault.io`. That resolved to Host `192.168.1.10`. That host exposed Port 443. Port 443 ran Service Nginx 1.18.0. Nginx served Technology WordPress 5.9.3. WordPress 5.9.3 is affected by Vulnerability CVE-2022-21661, CVSS 8.8.

That Vulnerability node in the ASG is the anchor point. The Commander reads it and creates Chain-01 in the APG — the `starts_at` edge linking the Vulnerability to the AttackChain.

From the AttackChain, three ChainSteps follow in sequence via `next_step` edges.

**ChainStep 1**: SQLMap confirms the WP_Query SQL injection. Status: VALIDATED. Supported by ASG Evidence node `sqli-extraction.txt` — the actual database dump output proving the injection.

**ChainStep 2**: SQLMap extracts the users table and the admin password hash is cracked. Status: VALIDATED. Supported by ASG Evidence node `user-table-dump.png` — a screenshot of the extracted table.

**ChainStep 3**: Metasploit deploys a web shell via the authenticated admin panel. Full remote code execution achieved. Status: VALIDATED. Supported by ASG Evidence node `webshell-rce.png` — the shell with command output.

The chain achieves its **Impact node**: full RCE on `shopvault.io`. Customer PII accessible. That Impact node is also supported by `pii-sample.json` — a captured sample of the accessible data.

Read the diagram bottom-up as a verification chain: claim of RCE → ChainStep 3 → Evidence `webshell-rce.png` → real. Claim of SQLi → ChainStep 1 → Evidence `sqli-extraction.txt` → real. Every assertion traces back to a file.

This is the key numbers on this slide: **6 recon-to-CVE hops traced. 3 VALIDATED ChainSteps. 4 Evidence artifacts. 0 manual commands.**

No existing autonomous VAPT system produces evidence-traceable, graph-grounded attack chains at this level of rigor. When a professional penetration tester produces a report, they can say "here is the evidence for every claim." CMatrix produces reports where you can say the same.

---

## 🎤 Slide 17 — Novel Contributions

This slide presents all twelve research contributions — C1 through C12. We've seen most of them in context throughout the presentation. Let me highlight the ones that define CMatrix as a research contribution, not just an engineering project.

**C1 — Dual-Graph World Model with strict write ownership.** This is the foundation. Two strictly separated graph structures: ASG for discovered reality, APG for inferred attack opportunity. No prior VAPT system maintains these as distinct structures with enforced boundaries. This is the architectural innovation from which every other contribution derives.

**C2 — Graph-State-Driven Dynamic Re-Planning.** Re-planning fires on explicit, inspectable graph triggers — a new Vulnerability node, a chain status change — not on arbitrary schedules. Every re-plan has a formal, traceable cause.

**C3 — APG Attack Chain Lifecycle with Evidence Traceability.** Attack chains are first-class entities with risk scores, lifecycle tracking, and end-to-end evidence linkage via `supported_by` edges. You saw this in action in the Chain-01 slide.

**C5 — Tool Risk Gate with Commander-Mailbox Approval.** Every tool call is classified before execution. High-risk calls require human-in-the-loop approval — zero code change required to activate supervised mode.

**C6 — ASG-Backed Lossless Context Compaction.** Three-layer compaction that reduces conversation history to near-zero without losing any findings — because everything lives in the graph, not the context window.

**C8 — Dual-Graph Termination Semantics.** Formally defined mission completion as the conjunction of ASG exhaustion and APG resolution. Neither condition alone is sufficient. No prior system can express both simultaneously.

**C10 and C11 — Cross-Mission Experience Store and Attack Strategy Library.** Persistent, RAG-backed accumulation of validated exploitation outcomes across missions. Crystallization of repeated successes into named, confidence-scored attack strategies. CMatrix gets smarter every mission it runs.

**C12 — Structured Engagement Trajectory Export.** Every mission produces a machine-readable decision log capturing ASG/APG triggers, Commander reasoning, and actions taken. Serves reproducibility, ablation studies, and — as a secondary contribution — a publicly releasable labeled dataset of autonomous VAPT reasoning sequences. This dataset type does not currently exist in the literature.

Twelve contributions. Every one of them is fully specified at the architecture level. Every one has a direct experimental evaluation path.

---

## 🎤 Slide 18 — Evaluation Plan

We know CMatrix makes strong claims. Here is exactly how we plan to validate each one empirically.

**Evaluation Platforms.** Three environments.

**HackTheBox retired machines** — Linux and Windows targets with known ground-truth vulnerabilities. These are the standard benchmark for autonomous pentesting research — PentestGPT and VulnBot both use them. We use them too, for direct comparison.

**TryHackMe CTF environments** — guided vulnerable web applications and APIs. Good for testing specific chain types in controlled settings.

**Custom Lab VMs** — a controlled WordPress plus Django stack that mirrors shopvault.io exactly. This is where we run clean, repeatable A/B comparisons and ablation studies without network variability.

**Research Questions.** Four core claims to test.

RQ1: Does the dual-graph architecture improve vulnerability coverage compared to a flat-memory baseline?
RQ2: Does formal dual termination reduce false-early-stops compared to timer-based termination?
RQ3: Does cross-mission learning measurably reduce time-to-finding on repeat target-type engagements?
RQ4: Does the Risk Gate reduce unintended offensive actions without significantly reducing coverage?

**Metrics.** Five measurements per mission: vulnerability coverage percentage against ground truth, chain precision — what percentage of APG chains achieve VALIDATED status, time-to-first-finding wall-clock, false early-stop rate, and mean tool calls to first VALIDATED chain.

**Baselines.** Three direct comparisons — PentestGPT tests RQ1 on world-model gap, VulnBot tests RQ1 on graph separation, PentestAgent tests RQ3 on cross-mission learning gap.

**Ablation Study.** Four ablations that isolate each architectural component: no dual-graph — flat history only. ASG only — no APG reasoning. No compaction — unlimited raw history. No learning — no cross-mission experience or strategy library. Each ablation proves the contribution of its removed component.

---

## 🎤 Slide 19 — Summary

We've covered a lot of ground. Let me close by being very precise about what we've built, what we claim, and what we're asking from you today.

**What CMatrix is.**

A dual-graph-guided, LLM-orchestrated multi-agent framework for autonomous Vulnerability Assessment and Penetration Testing. It maintains two strictly separated graph structures — the ASG for what the target is, and the APG for what can be done to it — and uses both to plan, dispatch, validate, and formally terminate a complete VAPT engagement. No human intervention required after mission start.

**What we claim.**

First: CMatrix is the first autonomous VAPT system to maintain two strictly separated, continuously evolving graph structures for simultaneous discovery and attack reasoning. The dual-graph is not a refinement of prior approaches — it is a new architectural paradigm for autonomous security assessment.

Second: Formal dual termination provides a theoretically sound, verifiable completion criterion that prior systems cannot express. "The mission is done because both graphs say so" is categorically more rigorous than "the mission is done because the timer fired."

Third: Cross-mission learning accumulates validated exploitation outcomes across all missions — a capability no prior published VAPT system demonstrates. CMatrix is the first system that gets measurably better as it runs more missions.

Fourth: The architecture produces a machine-readable decision trace usable for training security-specialized LLMs — a secondary contribution that doesn't exist elsewhere in the literature.

**What we're asking for.**

We're currently at the architecture proposal phase. All twelve contributions are fully specified. No implementation has begun. We're here for your guidance on four things:

Are the twelve contributions appropriately scoped for a thesis, or should some be scaled back or consolidated?

Is our HTB/THM ablation plan sufficient to prove the core claims — particularly RQ1 and RQ3?

Which contributions are most load-bearing and should be fully implemented, versus which can be validated primarily at the architectural level?

And finally: based on the contribution level, which publication venue do you think this work is targeting — USENIX Security, IEEE S&P, or ACSAC?

Your feedback today determines where we point our implementation effort. We're ready for your questions.

---

*[End of presentation script]*

---

> **If the supervisor asks a question you don't have a perfect answer for:**
> Don't panic. Say: *"That's a good question. In the current architecture, [your best answer]. This is something we'd want to address more rigorously during implementation — and it's the kind of thing the ablation study would help us characterize precisely."*
>
> Confidence is not about knowing everything. It's about owning what you know and being clear about what you don't. You built this architecture. You understand it. Show that.
