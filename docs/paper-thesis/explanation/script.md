# 🎯 CMatrix — Presentation Script
### *Complete · All 19 Slides · Defense Ready*

---

> ### 🗣️ How to Deliver This Script
>
> This is **not** a document to read word-for-word. It's a script to *internalize*.
> Know it so well that you can say any sentence in it without looking at the page.
>
> - 🎭 **Pause** after strong statements — let them breathe.
> - 👁️ **Make eye contact** when you say the big claims.
> - 💪 **Own the material completely.** You built this. Speak like you built it.

---

## 🎤 Slide 01 — Title Slide

> 🎬 *Pause 2–3 seconds. Let the room settle. Make eye contact before speaking.*

Good morning, Professor. Today we're presenting **CMatrix** — a *Dual-Graph-Guided, LLM-Orchestrated Multi-Agent Framework* for Autonomous Vulnerability Assessment and Penetration Testing.

That title is intentionally precise. **Every word in it earns its place.** And by the time we finish this presentation, you'll understand exactly what each word means and why we chose it.

Let me start with the question that drove this entire research: can a machine truly ***reason*** about security — not just execute tools, not just flag findings, but actually think through an attack the way a skilled human penetration tester does?

Answering that question is what **CMatrix** is built to do. *Let's get into it.*

---

## 🎤 Slide 02 — The Problem

Before we explain what CMatrix *is*, we need to understand the precise problem it was designed to solve.

Automated security testing has existed for decades. And in recent years, LLM-based systems have begun entering this space — using large language models to coordinate tools and produce security findings. These systems are impressive. But they all share **one fundamental, structural flaw.**

> ⚠️ ***They have no model of the target.***

Think about what that means in practice. When a modern automated VAPT system finishes a scan, it has a log of what it did: *"ran Nmap, found port 443, ran Nuclei, found CVE-2022-21661."* But that information lives in flat conversation history — or a task queue — with no structure, no relationships, no graph. The system knows *what it did* — but it cannot represent ***what the target is*** or ***what can be done to it***.

**This one design gap produces four cascading failures:**

| # | Failure | What It Means |
|---|---------|---------------|
| 🔴 **First** | **No structured world model** | The system can't build a connected, queryable picture of the target environment. There's no concept of *"this host runs this service which has this vulnerability which is linked to this endpoint."* |
| 🔴 **Second** | **No attack path reasoning** | A professional penetration tester doesn't just collect weaknesses — they figure out how Vulnerability A connects to Endpoint B to achieve Impact C. Existing systems can't do this. They log findings, not attack chains. |
| 🔴 **Third** | **Fragile re-planning** | When something new is discovered mid-mission, there's no principled way to decide what to do next. Re-planning is ad-hoc — a guess, not a graph-grounded decision. |
| 🔴 **Fourth** | **Arbitrary termination** | This is the most damaging failure. When is a penetration test *done*? Existing systems stop when a timer expires or a task queue goes empty — not because the attack surface is genuinely exhausted and every opportunity has been tested. That's not completeness. That's convenience. |

> 🧠 The root cause of all four problems is the same: **no structured world model.**
> CMatrix's solution is the *dual-graph architecture* — and everything we present today builds from that foundation.

---

## 🎤 Slide 03 — Foundations and Inspirations

CMatrix was not designed in isolation. Before we wrote a single line of architecture, we conducted a deep review of the state of the art — **five academic papers** and **three production open-source repositories**. This slide maps exactly what we learned from each one and where it lives in our design.

> 🎓 We believe research credit should be precise. So let me walk through these quickly.

---

#### 📚 Academic Papers

| Source | Venue | What We Took | How We Extended It |
|--------|-------|--------------|-------------------|
| **PentestGPT** | USENIX Security 2024 | Parsing raw tool output *before* it enters the reasoning context | Parsed output becomes *permanent graph state* in the ASG — not just a summary |
| **AutoAttacker** | — | Experience manager reusing successful attack subtasks *within* a mission | Generalized to *across* missions → the **Cross-Mission Experience Store** |
| **HPTSA** | Teams of LLM Agents | Task-specific document injection at agent spawn time improves zero-day exploitation by up to **2.1×** | Foundation of **Vulnerability-Class Knowledge Injection** |
| **PentestAgent** | AsiaCCS 2025 | Self-debugging loop pattern — diagnose, contextualize, adapt, retry | Applied directly to the **Validation Agent** failure recovery sequence |
| **VulnBot** | — | Agents hand off *structured summaries*, not raw history | Foundation of the **context-isolated agent design** |

---

#### 🛠️ Open-Source Repositories

| Source | What We Took |
|--------|-------------|
| **PentAGI** | Cycle Guard and Reflector for detecting agent fixation |
| **Claude Code** | Two-stage LLM permission classifier + named lifecycle hook architecture |
| **Hermes Agent** | Skill crystallization mechanism + trajectory export concept |

---

> 🏗️ For each of these, we know exactly **what we took**, **what we adapted**, and **what we added.**
> This is the intellectual foundation **CMatrix** is built on.

---

## 🎤 Slide 04 — Scope

Before diving into the architecture, let's be clear about the **boundaries** of what CMatrix assesses — and what it deliberately does not.

---

#### 🔁 Assessment Modes

| Mode | Description |
|------|-------------|
| 🖤 **Black-Box** | Operator provides only a root domain and scope declaration. The system discovers everything from zero. |
| 🩶 **Grey-Box** | Partial knowledge (known IP ranges or credentials) is provided upfront, pre-seeding the ASG with Host nodes before assessment begins. |

---

#### ✅ In Scope — Target Categories

- 🌐 **Network Infrastructure** — hosts, ports, services
- 🖥️ **Web Applications** — HTTP/HTTPS services, CMSes
- 🔌 **REST APIs** — endpoints, parameters, authentication surface

> 🔒 Every single tool execution is gated against the declared scope *before* it fires. **Nothing runs out-of-scope.** The Risk Gate enforces this unconditionally.

---

#### ❌ Explicitly Out of Scope

*These are not limitations we're hiding — they're intentional boundaries that keep the thesis focused and the evaluation clean.*

`White-box source code analysis` · `Mobile applications` · `Cloud and IoT infrastructure` · `Wireless networks` · `Active Directory` · `Physical or social engineering`

---

> 🚀 **The key point:** the operator configures CMatrix once — *target, scope, mode* — presses start, and **does not touch it again.** Everything that follows is fully autonomous.

---

## 🎤 Slide 05 — System Architecture

Now let's look at how CMatrix is actually structured. The architecture has **three tiers** — orchestration, the dual-graph world model, and the specialized agents with tool execution layer.

---

### 🏛️ Tier One — Orchestration

At the top sits the **Operator**, who configures the mission: target, scope, assessment mode. This configuration flows directly to the **Commander Agent**.

The Commander is the brain of the entire system. It reads both graphs. It plans. It delegates. It approves high-risk operations. And here is the most important thing to understand about the Commander:

> 🧠 ***It never runs tools.*** Not once. Its job is **pure reasoning and orchestration.**

The Commander is governed by the **VAPT Protocol Prompt** — a structured, versioned natural-language document that encodes the entire assessment methodology. Phase sequencing, re-planning triggers, termination conditions, tool selection heuristics — all defined in this document. This means you can swap out the methodology — OWASP Testing Guide, PTES, custom red-team workflow — without changing a single line of orchestration code. That's research contribution **C7: methodology-as-configuration**.

---

### 🗺️ Tier Two — The Dual-Graph World Model

This is the **heart of the architecture.** Two strictly separated knowledge layers:

| Graph | Role | Contains |
|-------|------|----------|
| 🔵 **Attack Surface Graph (ASG)** | *Discovered reality* | Every confirmed fact about the target: domains, hosts, ports, services, technologies, endpoints, parameters, vulnerabilities, evidence artifacts. **Only confirmed facts. Never hypotheses.** |
| 🔴 **Attack Path Graph (APG)** | *Inferred opportunity* | Attack chains built by the Commander through active reasoning over ASG state. Risk scores, chain priorities, validation status. **Only attack reasoning. Never raw scan data.** |

> 🔐 **Strict separation. Enforced write ownership. No agent crosses this boundary.**

---

### ⚙️ Tier Three — Specialized Agents and the Tool Adapter Layer

Six specialized agents each own a specific domain of responsibility. Every tool invocation — without exception — passes through the **Tool Adapter Layer** and the **Risk Gate**.

| Risk Level | Tools | Execution |
|------------|-------|-----------|
| 🟢 **Low-risk** | Passive discovery | Execute immediately |
| 🟡 **Medium-risk** | Active enumeration | Require LLM classifier evaluation |
| 🔴 **High-risk** | Exploit tools | Require Commander's explicit mailbox approval |

> 🔗 That mailbox is also the architectural insertion point for **human-in-the-loop supervision** — no code change required.

---

## 🎤 Slide 06 — Dual-Graph World Model

Let's go deeper on the dual-graph, because this is the architectural foundation everything else is built on.

Let's go deeper on the dual-graph, because this is the **architectural foundation** everything else is built on.

---

### 🔵 Left — Attack Surface Graph (ASG)

Ask yourself: what does a human penetration tester *know* about a target as they work? They know what hosts exist. What ports are open. What services are running. What technologies are in use. What endpoints are exposed. What parameters those endpoints accept. What vulnerabilities are present. And what evidence exists to prove each finding.

The ASG encodes exactly that knowledge as a **living, queryable graph.** On this slide you can trace a real example from our `shopvault.io` assessment:

```
Domain: shopvault.io
  └── Host: 192.168.1.10
        └── Port 443 → Service: Nginx 1.18
              └── Technology: WordPress 5.9.3
                    └── Endpoint: /wp-admin
                          └── Vulnerability: CVE-2022-21661 (CVSS 8.8)
                                └── Evidence: sqli-extract.txt ✅
```

> 📌 **The ASG is not a log. It is not a task list. It is a structural model of the target environment.**
> Every node is a *confirmed discovered fact*. Every edge is a *confirmed relationship*. **Hypotheses are never written here.**

---

### 🔴 Right — Attack Path Graph (APG)

This is where the Commander ***reasons***. When the Commander reads a Vulnerability node in the ASG, it asks: *can this be exploited? Does it chain with other vulnerabilities? What's the likely business impact?* The answers become AttackChain nodes in the APG.

You can see the **four chains from `shopvault.io`** on this slide:

| Chain | Risk Score | Path |
|-------|-----------|------|
| 🥇 **Chain-01** | **9.1** | Full SQLi-to-RCE through WordPress |
| 🥈 **Chain-03** | 8.1 | Blind SQLi on staging login |
| 🥉 **Chain-02** | 7.5 | IDOR via `user_id` parameter |
| **Chain-04** | 4.2 | Exposed database backup |

The Commander **re-ranks this priority queue every time any chain's status changes.**

---

### ⚖️ The Separation Principle

> 🔐 ***Discovery agents write only to the ASG and never reason about attack chains.***
> ***The Commander writes only to the APG and never runs tools.***
>
> Each layer is authoritative for exactly one type of knowledge. This eliminates the class of errors that plague flat-memory systems: conflating facts with hypotheses, or letting attack reasoning contaminate environmental observation.

---

## 🎤 Slide 07 — Agent Architecture

CMatrix has **seven agents** — the Commander plus six specialists. Each specialist is ***context-isolated***: spawned fresh for its task, given only the slice of the dual graph it actually needs, and returning only structured graph output when it's done. Its working context is then discarded completely.

---

#### 🤖 The Agent Registry

| Agent | Role | Tools | ASG Writes |
|-------|------|-------|-----------|
| 🧠 **Commander** | Orchestrating brain. Reads dual graph, plans, delegates, approves high-risk ops. *Only agent that writes to APG. Never runs tools.* | — | APG only |
| 🔍 **Recon Agent** | External reconnaissance. Discovers subdomains, validates live hosts, identifies open ports and services. | `Amass`, `httpx`, `Nmap` | Domain, Host, Port, Service nodes |
| 🔬 **Analysis Agent** | Deep enumeration and vulnerability discovery. Fingerprints stacks, finds hidden endpoints, fuzzes API parameters, runs CVE template checks. | `WhatWeb`, `Gobuster`, `ffuf`, `Nuclei`, `OWASP ZAP` | Technology, Endpoint, Parameter, Vulnerability nodes |
| 🌐 **Research Agent** | Intelligence specialist. *Only* agent authorized to make outbound requests. Retrieves live CVE/exploit data from NVD, Exploit-DB, GitHub. | External APIs | Enriched Vulnerability node attributes |
| ✅ **Validation Agent** | Proves vulnerabilities are real. Receives a specific APG AttackChain and confirms each ChainStep — runs self-debugging loop on failures. | `SQLMap`, `Metasploit` | Chain status updates |
| 📸 **Evidence Agent** | Captures screenshots and response artifacts for every validated finding. Links Evidence nodes via `validated_by` edges. | `EyeWitness` | Evidence nodes |
| 📄 **Report Agent** | Reads the complete dual graph at mission end. *No tools. No decisions.* Pure translation of graph state to human-readable output. | — | — |

---

#### 🔒 Context Isolation Model

When the Commander spawns a specialist, it provides **exactly five things** and nothing else:

1. 📊 ASG slice relevant to the task
2. 🗺️ APG slice *(if applicable)*
3. 🛠️ Authorized tool set
4. 📋 Task specification
5. 📚 Vulnerability-class knowledge documents *(for Analysis and Validation agents)*

When the agent returns, it provides **one thing**: a structured ASG delta — *new nodes and edges only.*

---

#### ⚡ Three Critical Properties Produced

| Property | What It Means |
|----------|---------------|
| 🧹 **Commander context stays clean** | It never sees thousands of lines of raw tool output |
| 🚫 **Agents can't contaminate each other** | Agent A's verbose execution history never appears in Agent B's context; knowledge passes only through the ASG |
| 🎯 **Rejections don't bias planning** | When the Commander rejects a high-risk tool call, that rejection never appears in the Commander's own reasoning context and cannot skew future decisions |

> 🏆 **The result:** long missions with many agents produce the same reasoning quality as single-agent tasks. *Context quality does not degrade with mission complexity.*

---

## 🎤 Slide 08 — Context-Isolated Agent Spawn Lifecycle

This slide shows the **exact sequence** of a single agent spawn — from Commander decision to ASG write to context discard. Let me trace through it.

The Commander reads the dual graph, decides the next action, and issues a `spawn` call to a specialist agent, delivering the scoped context package we just described.

---

#### 🔄 Tool Call Trace — Step by Step

**Step 1 — 🟢 WhatWeb** *(Low-risk)*

The agent calls WhatWeb. The Risk Gate checks scope: target is in declared scope, tool is authorized. **Executes immediately.** The Tool Adapter runs WhatWeb, parses the raw output, extracts structured findings — *"WordPress 5.9.3, WooCommerce, Nginx 1.18"* — and returns only that structured record. Raw output is discarded.

**Step 2 — 🟡 Gobuster** *(Medium-risk)*

The Risk Gate routes this to the **LLM Permission Classifier**. The classifier evaluates three axes:
- Is the target in scope?
- Is this call consistent with the active APG chain?
- Are there any parameter anomalies suggesting scope drift or injection?

Classifier returns `EXECUTE`. Gobuster runs. The endpoint `/backup/db_export_2023.sql` is discovered and written as a node to the ASG.

**Step 3 — 🔴 SQLMap** *(High-risk)*

The Risk Gate routes this to the **Commander Mailbox**. The Commander receives the full approval request: tool, target, parameters, rationale, active chain context.

> The Commander evaluates: *target is in scope, CVE is confirmed, chain priority is highest, parameters look clean.* **It approves.** SQLMap executes.

---

#### 📤 Agent Returns

When the agent finishes its full task, it writes the complete ASG delta — Technology node, Endpoint node, Vulnerability node — and returns it to the Commander. The Commander reads the new Vulnerability node and seeds **APG Chain-01**.

The agent's working context — every line of tool output, every intermediate reasoning step, every failed attempt — is ***discarded***. It is gone. **The only thing that persists is the structured ASG delta.**

---

> 📈 **This is what makes CMatrix scalable.**
> *Intelligence accumulates in the graph. Context bloat doesn't accumulate anywhere.*

---

## 🎤 Slide 09 — Offensive Tool Catalogue

CMatrix integrates **eleven industry-standard offensive security tools**. These aren't toys or simulations — they are the exact tools professional penetration testers use in real engagements. The difference is that CMatrix operates them autonomously through the Tool Adapter Layer, so agents reason about *targets*, not command syntax.

---

#### 🗓️ Phase 1 — Reconnaissance *(3 tools)*

| Tool | Purpose |
|------|---------|
| **Amass** | Subdomain enumeration — DNS brute-forcing, certificate transparency logs, passive OSINT |
| **httpx** | Live host probing — validates which discovered hosts actually respond, identifies web server headers and TLS details |
| **Nmap** | Port and service scanning — fingerprints services, detects OS, can run NSE scripts for vulnerability detection on open services |

---

#### 🔎 Phase 2 — Analysis *(5 tools)*

| Tool | Purpose |
|------|---------|
| **WhatWeb** | Fingerprints technology stacks — CMS versions, frameworks, JavaScript libraries — seeds the ASG with Technology nodes that trigger Research Agent queries |
| **Gobuster** | Wordlist-based directory brute-forcing to find hidden paths, admin panels, and exposed files |
| **ffuf** | Fast fuzzer for API route discovery, parameter fuzzing, and virtual host enumeration |
| **Nuclei** | Template-based scanning, matching discovered technologies against thousands of CVE and misconfiguration templates |
| **OWASP ZAP** | Actively crawls and tests for the OWASP Top 10 — XSS, CSRF, injection flaws, authentication weaknesses |

---

#### 💣 Phase 3 — Validation *(2 tools)*

| Tool | Purpose |
|------|---------|
| **SQLMap** | Automated SQL injection detection and exploitation — confirms injection points, extracts data, tests for OS-level access |
| **Metasploit** | Exploit execution — validates APG ChainSteps, demonstrates impact, achieves proof of exploitation |

---

#### 📷 Phase 3 — Evidence *(1 tool)*

| Tool | Purpose |
|------|---------|
| **EyeWitness** | Headless screenshot capture — visual proof artifacts linked to ASG Evidence nodes |

---

> 🔩 **Key architectural point:** Every tool is **wrapped in a Tool Adapter**. Agents never call tools directly. This means tools can be swapped, updated, or replaced without touching any agent logic. And no irreversible offensive operation runs without Commander-level scope validation.

---

## 🎤 Slide 10 — Tool Adapter Layer

The **Tool Risk Gate** is one of CMatrix's most important safety and control mechanisms. Let me walk through the full lifecycle of a tool call.

---

#### 🔁 Full Tool Call Lifecycle

An agent requests a tool call — say, Gobuster against `shopvault.io`.

**① Pre-execution → PreToolUse Hook**
Before anything executes, the **PreToolUse hook** fires. This is an operator-registered interception point. The operator can block, modify, or let it continue.

**② Scope Check**
Is the target in declared assessment scope? Is this tool authorized for the current agent? If either check fails, the call is **blocked here.**

**③ Risk Classification**
The gate assigns the call to one of three tiers:

| Tier | Tools | Path |
|------|-------|------|
| 🟢 **Low-risk** — passive discovery | `Amass`, `httpx`, `WhatWeb`, `EyeWitness` | Execute immediately after scope check. No further evaluation required. |
| 🟡 **Medium-risk** — active enumeration | `Nmap`, `Gobuster`, `ffuf`, `Nuclei`, `ZAP` | → **LLM Permission Classifier** |
| 🔴 **High-risk** — exploit tools | `SQLMap`, `Metasploit` | → **Commander Mailbox** (always) |

---

#### 🟡 LLM Permission Classifier — Three Evaluation Axes

A fast-filter pass checks obvious cases instantly. If it's not obvious, a chain-of-thought reasoning pass evaluates:

1. **Scope Alignment** — is the exact target node within declared scope?
2. **Chain Intent** — is this call consistent with the active APG AttackChain being pursued?
3. **Parameter Safety** — do the parameters exhibit any prompt injection patterns or scope drift?

Classifier outputs a binary: `EXECUTE` or `ESCALATE`. If escalate, the call routes to the Commander Mailbox as if it were High-risk.

---

#### 🔴 Commander Mailbox — Decision Options

The Commander receives the full approval request and returns one of three decisions:

- ✅ **Approve** → proceeds to execution
- ❌ **Reject** → annotated to the APG
- ✏️ **Modify** → adjusts parameters before the tool runs

---

#### 📬 Post-Execution

After execution: the **Tool Adapter** runs the tool, parses raw output into structured JSON, and discards the raw output. Then the **PostToolUse hook** fires — logging, alerting, validating the write. The ASG receives the new nodes and edges. The agent receives only a compact summary of the result.

---

> 🛡️ **Critical safety property:** No irreversible offensive operation executes without Commander-level scope validation. No medium-tier call executes without LLM classifier approval. **This is not a soft constraint — it is enforced by architecture.**

---

## 🎤 Slide 11 — Autonomous Planning Cycle

Now let's look at how the Commander actually operates. This is the **cognitive engine of CMatrix** — the loop it runs every single iteration.

---

#### 👁️ Step 1 — Observe

Every cycle begins with two observations:

- 🔵 **Read the ASG:** Are there unexplored nodes? New vulnerability or technology discoveries? Unprobed endpoints?
- 🔴 **Read the APG:** Are there hypothesized chains waiting to be validated? Have chain statuses changed? Does the priority queue need re-ranking?

---

#### 🧠 Step 2 — Reason

With both observations in hand, the Commander **reasons**: *given the full dual-graph state, what is the best next action?*

| Condition | Action |
|-----------|--------|
| ASG has gaps — unexplored hosts, unchecked endpoints | Spawns a **Discovery Agent** to explore them |
| APG has high-priority chains awaiting validation | Spawns a **Validation Agent** against the top-ranked chain |
| Both are pressing | Dispatches **in parallel**, weighing priority across both paths simultaneously |

---

#### 🔄 Step 3 — Execute & Guard

Every action routes through the Risk Gate. The agent executes, writes its ASG delta, and returns. The Commander updates both graphs. Then it runs the **Cycle Guard**:

- *Has the same tool call been repeated 3+ times?* → That's **fixation** — force a re-plan.
- *Are there repeated distinct failures?* → The **Reflector** provides corrective guidance rather than letting the agent burn its budget blind.

Then: **Termination Check** — both conditions must be true simultaneously. *(Covered in Slide 12.)*

---

#### ⚡ Re-plan Triggers — Every One a Graph Event

| Graph | Trigger | Re-plan Action |
|-------|---------|----------------|
| 🔵 **ASG** | New **Vulnerability** node | Might seed an APG chain |
| 🔵 **ASG** | New **Technology** node | Warrants a Research Agent spawn |
| 🔵 **ASG** | New **Endpoint** node | Needs probing |
| 🔴 **APG** | Chain → `PARTIALLY_VALIDATED` | Re-rank all chains |
| 🔴 **APG** | Chain → `VALIDATED` | Move on to the next |
| 🔴 **APG** | Chain → `RULED_OUT` | Remove and re-prioritize |

> 🎯 **The key claim:** Every Commander decision traces to a graph event. Every re-plan is triggered by a node write. ***The system doesn't guess. It responds to structured evidence.***

---

## 🎤 Slide 12 — Dual Termination and Context Compaction

This slide covers **two of the most technically distinctive properties** of CMatrix. Let's take them in turn.

---

### 🛑 Part 1 — Dual Termination

> *When is a penetration test **done**? This is not a trivial question.*
> And the answer that prior systems give — *"when the timer expires"* or *"when the task queue is empty"* — is **the wrong answer.**

CMatrix requires **both** of the following to be simultaneously true before a mission terminates:

| Condition | Definition |
|-----------|-----------|
| ✅ **Condition 1: ASG Exhausted** | Every node in the ASG — every Domain, Host, Port, Service, Technology, Endpoint, and Parameter — has been investigated by the appropriate specialist agent. **No unexplored surface remains.** |
| ✅ **Condition 2: APG Resolved** | Every AttackChain in the APG sits in a terminal state — either `VALIDATED` or `RULED_OUT`. **No chain is left `HYPOTHESIZED` or `PARTIALLY_VALIDATED`.** |

**You need both.** Here's why each alone is insufficient:

| ASG State | APG State | Status |
|-----------|-----------|--------|
| ✅ Exhausted | ❌ Open chains | **Not done** — attack reasoning is unfinished |
| ❌ New nodes written | ✅ Resolved | **Not done** — new nodes might seed new chains |
| ❌ Not exhausted | ❌ Open chains | **Obviously not done** |
| ✅ Exhausted | ✅ Resolved | ✅ **Mission complete** → Spawn Report Agent |

> 🏆 No other autonomous VAPT system in the literature can express both conditions simultaneously. Timer-based systems stop mid-chain. Task-queue systems have no concept of APG resolution at all. This is **research contribution C8** — and it's not an incremental improvement. *It's a categorically different definition of completeness.*

---

### 🗜️ Part 2 — Context Compaction

VAPT missions are long. Raw tool outputs are enormous. Without active management, LLM context windows overflow — and when they do, *the system loses intelligence.*

> 💡 **Core insight:** The ASG is a lossless persistent store of all discoveries. **Conversation history is expendable. The ASG is not.**

CMatrix uses a **three-layer compaction scheme:**

| Layer | Trigger | Action |
|-------|---------|--------|
| **Layer 1 — MicroCompact** | *Every tool call* | Raw tool output parsed at the Tool Adapter. Structured findings go to the ASG. Only a 3-line compact summary enters the agent's working context. Raw output is gone. |
| **Layer 2 — AutoCompact** | *60% context usage* | Older conversation turns are summarized by a scoped LLM call. Summary replaces the raw turns. Agent continues without interruption. |
| **Layer 3 — FullCompact** | *85% context* | Entire conversation history is replaced. Context reconstructed from scratch: current ASG snapshot, current APG priority chains, last N tool results. |

> 🔒 **FullCompact loses zero intelligence** — because no intelligence ever lived exclusively in the conversation. It was all written to the ASG the moment it was discovered. That's what makes this compaction scheme **lossless.** No general-purpose agent can claim this property.

---

## 🎤 Slide 13 — Attack Chain Lifecycle

This slide details the **APG chain state machine** — how attack chains are born, evolve, and terminate — and the Validation Agent's self-debugging mechanism.

---

#### 🔗 Chain State Machine

| State | How It's Reached | Meaning |
|-------|-----------------|---------|
| 🟣 `HYPOTHESIZED` | Commander reads a Vulnerability node in ASG, infers a plausible exploitation path | Not tested yet. An *informed hypothesis*, not a confirmed attack. |
| 🟡 `PARTIALLY VALIDATED` | Validation Agent confirms individual steps | Steps are proven. Chain not yet complete end-to-end. |
| 🟢 `VALIDATED` | Every ChainStep confirmed with linked Evidence and Impact demonstrated | ***Mission success for that chain.*** |
| ⛔ `RULED OUT` | Required step fails after maximum retries | Not exploitable as hypothesized. Failure reason written back to ASG as a structured annotation on the Vulnerability node. Commander re-prioritizes and moves on. |

---

#### 🔧 Validation Agent Self-Debugging Loop

> *When a ChainStep fails, the Validation Agent does **not** immediately give up.*
> It enters a structured **four-stage recovery sequence:**

1. 🔍 **Diagnose** — Analyze *why* it failed. Wrong parameter format? Authentication required? Version mismatch? Payload encoding issue? *The diagnosis is specific, not generic.*

2. 🗂️ **Contextualize** — Query the ASG for additional node attributes that might resolve the diagnosis. If authentication is required, is there a captured credential Evidence node? If the version is wrong, what does the Service node actually say?

3. ✏️ **Adapt** — Modify the tool invocation based on the diagnosis and additional context. New parameters, different payload, corrected module selection.

4. 🔁 **Retry** — Up to a configurable cap, defaulting to **3 attempts**. If the cap is reached, the step is marked `RULED_OUT` and the Commander re-plans.

*This bounded loop balances two real failure modes: giving up too early on a legitimate vulnerability due to a transient error, versus burning infinite time on an exploit that will simply never work. Three attempts is enough to overcome transient failures while preventing runaway loops.*

---

#### 📊 Live Priority Queue — `shopvault.io`

| Rank | Chain | Risk Score | Type |
|------|-------|-----------|------|
| 🥇 1 | **Chain-01** | 9.1 | Full SQLi-to-RCE through WordPress |
| 🥈 2 | **Chain-03** | 8.1 | Blind SQLi on staging login |
| 🥉 3 | **Chain-02** | 7.5 | IDOR via `user_id` |
| 4 | **Chain-04** | low | Trivial misconfiguration |

The Commander pursues them in this exact order and **re-ranks after every status change.**

---

## 🎤 Slide 14 — Cross-Mission Learning

This slide presents **one of CMatrix's most distinctive capabilities.** And I want to frame it with a simple observation first.

> 🧠 Every autonomous VAPT system in the prior literature — PentestGPT, AutoAttacker, PentestAgent, VulnBot — starts from *zero knowledge* on every new mission. Whatever was learned in Mission 1 is completely gone by Mission 2.
> **The system is amnesiac by design.** That seems like an obvious limitation. CMatrix addresses it.

---

### 💾 The Cross-Mission Experience Store *(C10)*

When a CMatrix mission terminates, the Report Agent writes a structured record for every validated attack chain into a **persistent, RAG-backed knowledge base** that survives across missions. Each record contains:
- Target technology fingerprint
- The specific CVE
- Successful tool parameters
- ChainStep sequence that achieved validation
- Final mission outcome

When the *next* mission starts — immediately after the Recon Agent writes its first Technology nodes to the ASG, before Analysis even begins — the Commander queries this store. It retrieves records from past missions on similar technology stacks.

Those records become **candidate chain hypotheses** — pre-validated patterns that inform APG seeding. Instead of starting from zero, the Commander starts from a *library of things that have already worked on similar targets.*

> 🔄 This generalizes AutoAttacker's within-mission experience reuse mechanism to **cross-mission scope**. AutoAttacker reuses subtasks within one session. CMatrix accumulates across *every mission ever run*. That generalization is the contribution.

---

### 📚 The Attack Strategy Library *(C11)*

This goes a level further. When the same technology fingerprint produces a validated AttackChain across two or more independent missions, the Commander triggers **crystallization**.

A scoped LLM call generalizes the specific chain parameters from those missions into a named, parameterized attack procedure with a **confidence score**.

> 💡 **Example:** `STRAT-WP-SQLI-001` — *"WordPress 5.x SQL injection via WP_Query, confirmed across four independent missions, Metasploit module available, parameters template provided."*

This strategy is retrieved at mission start whenever WordPress 5.x is fingerprinted, and injected as a **pre-ranked APG AttackChain seed**. It's prioritized above zero-prior chains because it carries a *validated track record*, not just CVE severity.

---

> 📈 **The measurable claim:** CMatrix becomes demonstrably more efficient on repeat target-type engagements. The fourth time it assesses a WordPress deployment, it doesn't rediscover the same chains from scratch — it begins from a library of validated attack patterns with known confidence scores. **No other autonomous VAPT system in the literature does this.**

---

## 🎤 Slide 15 — Real-World Scenario

Everything we've described architecturally comes together in this slide. Let me walk you through a complete end-to-end mission: a black-box assessment of `shopvault.io`, a fictional e-commerce platform. The operator provides the root domain and scope. Then presses start. Zero manual commands from this point forward.

Everything we've described architecturally comes together in this slide. Let me walk you through a **complete end-to-end mission**: a black-box assessment of `shopvault.io`, a fictional e-commerce platform.

> The operator provides the root domain and scope. Then presses start. **Zero manual commands from this point forward.**

---

#### 🗓️ Phase 1 — Reconnaissance

The Commander reads the initial ASG: one seed node, the Domain `shopvault.io`. It spawns the **Recon Agent**.

- **Amass** runs subdomain enumeration and discovers 14 subdomains — including `api`, `admin`, `staging`, and `pay`.
- **httpx** probes all 14 and confirms 11 are live. Notably, `staging.shopvault.io` returns an unexpected `200 OK` rather than being gated.
- **Nmap** scans all 11 hosts and finds ports 80, 443, 8080, and 8443 open. `pay.shopvault.io` has an expired TLS certificate.

> 📥 *The Recon Agent returns 37 new ASG nodes. Working context discarded.*

---

#### 🔎 Phase 2 — Analysis and Intelligence

The Commander spawns the **Analysis Agent**. WhatWeb fingerprints the stack: WordPress 5.9.3 on the main site, Django API on api.shopvault, Nginx 1.18 as the reverse proxy.

The Commander reads the WordPress Technology node and immediately spawns the **Research Agent**: *"WordPress 5.9.3 known CVEs."*
- NVD returns **CVE-2022-21661** — SQL injection via WP_Query, CVSS 8.8, public PoC on Exploit-DB, Metasploit module available.
- The Commander seeds **Chain-01** in the APG. Status: `HYPOTHESIZED`. Risk score: **8.8**.

**Meanwhile, Analysis continues:**
- **Gobuster** discovers `/backup/db_export_2023.sql` — an exposed database dump file.
- **ffuf** fuzzes the API and finds the `user_id` parameter accepts unsanitized input. **Chain-02 seeded:** IDOR, risk **7.5**.
- **OWASP ZAP** finds SQL error messages on the staging login form. **Chain-03 seeded:** blind SQLi, risk **8.1**.

> 📥 *61 new ASG nodes. 3 chains in the APG, all `HYPOTHESIZED`.*

---

#### 💣 Phase 3 — Validation

The Commander reads the APG. Chain-01 leads at 8.8. It spawns the **Validation Agent**.

- 🥇 **Chain-01:** SQLMap targets the WP_Query injection — *High-risk call, Commander Mailbox.* **Approved.** Injection confirmed, admin hash extracted. Metasploit cracks the hash, authenticates to WordPress admin, deploys a web shell via the theme editor. Full remote code execution. `VALIDATED`. Risk score escalated to **9.1**. Evidence Agent captures four screenshots.
- 🥈 **Chain-02:** SQLMap on the `user_id` parameter confirms IDOR — any customer's orders are accessible without authentication. `VALIDATED`.
- 🥉 **Chain-03:** Blind SQLi on staging login extracts database credentials. The Commander notices credential overlap with production and flags additional impact: credential reuse risk. `VALIDATED`.
- 🏅 **Chain-04:** The exposed database backup file is simply retrieved via HTTP GET. Trivially `VALIDATED`.

---

#### 📄 Phase 4 — Report

The Commander confirms: **all 11 hosts explored, all 4 chains in terminal state.** Dual-graph termination condition met. **Report Agent** spawned. It reads the complete ASG and APG and produces a full penetration test report.

> 🏆 **Final Mission Statistics:**
> `14 subdomains` · `11 live hosts` · `28 open ports` · `19 endpoints` · `11 vulnerabilities` · `4 validated chains` · **`0 manual commands`**

---

## 🎤 Slide 16 — Chain-01 Traceability

This slide demonstrates **one of the most rigorous properties of CMatrix:** every claim in the final penetration test report is *fully traceable through the dual graph, end to end.*

Let me walk you through the trace for **Chain-01**.

---

#### 📍 The Anchor Point (ASG Discovery Layer)

The chain begins in the ASG:
- Recon Agent discovered Domain `shopvault.io`
- Resolves to Host `192.168.1.10`
- Exposes Port `443`
- Runs Service `Nginx 1.18.0`
- Serves Technology `WordPress 5.9.3`
- Affected by Vulnerability `CVE-2022-21661` (CVSS 8.8)

That Vulnerability node in the ASG is the anchor point. The Commander reads it and creates **Chain-01** in the APG — the `starts_at` edge linking the Vulnerability to the AttackChain.

---

#### ⛓️ The Attack Chain (APG Validation Layer)

From the AttackChain, three `ChainSteps` follow in sequence via `next_step` edges:

| Step | Action | Status | 📄 Evidence Node Link |
|------|--------|--------|----------------------|
| **1** | SQLMap confirms WP_Query SQL injection | `VALIDATED` | `sqli-extraction.txt` (Database dump output) |
| **2** | SQLMap extracts users table; admin hash cracked | `VALIDATED` | `user-table-dump.png` (Extracted table screenshot) |
| **3** | Metasploit deploys web shell via admin panel | `VALIDATED` | `webshell-rce.png` (Shell with command output) |

---

#### 🎯 The Impact

The chain achieves its **Impact node**: full RCE on `shopvault.io`. Customer PII accessible. That Impact node is also supported by `pii-sample.json` — a captured sample of the accessible data.

> 🔍 **Read the diagram bottom-up as a verification chain:**
> Claim of RCE → ChainStep 3 → Evidence `webshell-rce.png` → **Real.**
> Claim of SQLi → ChainStep 1 → Evidence `sqli-extraction.txt` → **Real.**
> *Every assertion traces back to a file.*

---

> ⚖️ **The Rigor Claim**
> No existing autonomous VAPT system produces evidence-traceable, graph-grounded attack chains at this level of rigor. When a professional penetration tester produces a report, they can say *"here is the evidence for every claim."* **CMatrix produces reports where you can say the same.**

---

## 🎤 Slide 17 — Novel Contributions

This slide presents all **twelve research contributions — C1 through C12.** We've seen most of them in context throughout the presentation. Let me highlight the ones that define CMatrix as a *research contribution*, not just an engineering project.

---

#### 🌟 Core Architectural Innovations

| ID | Contribution | Significance |
|----|-------------|--------------|
| **C1** | **Dual-Graph World Model** | The foundation. Two strictly separated graph structures: ASG for discovered reality, APG for inferred opportunity. No prior system maintains these distinct boundaries. |
| **C2** | **Graph-State-Driven Dynamic Re-Planning** | Re-planning fires on explicit, inspectable graph triggers (new Vulnerability node, chain status change) — not on arbitrary schedules. *Every re-plan has a formal, traceable cause.* |
| **C3** | **APG Attack Chain Lifecycle** | Attack chains are first-class entities with risk scores, lifecycle tracking, and end-to-end evidence linkage via `supported_by` edges. |
| **C5** | **Tool Risk Gate** | Every tool call classified before execution. High-risk calls require Commander-Mailbox approval — *zero code change required to activate supervised mode.* |
| **C6** | **ASG-Backed Context Compaction** | Three-layer compaction reduces conversation history to near-zero without losing findings — because intelligence lives in the graph, not the LLM context window. |
| **C8** | **Dual-Graph Termination Semantics** | Mission completion defined as the conjunction of ASG exhaustion and APG resolution. No prior system can express both simultaneously. |

---

#### 🧠 Cross-Mission & Reproducibility Contributions

| ID | Contribution | Significance |
|----|-------------|--------------|
| **C10 / C11** | **Experience Store & Strategy Library** | Persistent, RAG-backed accumulation of validated exploitation outcomes. Crystallization of repeated successes into named, confidence-scored strategies. *CMatrix gets smarter every mission it runs.* |
| **C12** | **Structured Engagement Trajectory Export** | Every mission produces a machine-readable decision log. Yields a publicly releasable, labeled dataset of autonomous VAPT reasoning sequences — *a dataset type that does not currently exist in the literature.* |

---

> 🎓 **The Bottom Line**
> **Twelve contributions.** Every one of them is fully specified at the architecture level. Every one has a direct experimental evaluation path.

---

## 🎤 Slide 18 — Evaluation Plan

We know CMatrix makes strong claims. Here is exactly how we plan to validate each one empirically.

---

#### 🧪 1. Evaluation Platforms *(3 Environments)*

- 💻 **HackTheBox (Retired Machines)** — Linux and Windows targets with known ground-truth vulnerabilities. Standard benchmark for autonomous pentesting research (PentestGPT, VulnBot). *Used for direct comparison.*
- 🚩 **TryHackMe (CTF Environments)** — Guided vulnerable web applications and APIs. *Used for testing specific chain types in controlled settings.*
- 🏢 **Custom Lab VMs** — A controlled WordPress + Django stack mirroring `shopvault.io` exactly. *Used for clean, repeatable A/B comparisons and ablation studies without network variability.*

---

#### ❓ 2. Research Questions *(4 Core Claims)*

- **RQ1:** Does the dual-graph architecture improve vulnerability coverage compared to a flat-memory baseline?
- **RQ2:** Does formal dual termination reduce false-early-stops compared to timer-based termination?
- **RQ3:** Does cross-mission learning measurably reduce time-to-finding on repeat target-type engagements?
- **RQ4:** Does the Risk Gate reduce unintended offensive actions without significantly reducing coverage?

---

#### 📊 3. Metrics *(5 Measurements per Mission)*

1. **Vulnerability Coverage %** against ground truth
2. **Chain Precision** (% of APG chains achieving `VALIDATED` status)
3. **Time-to-First-Finding** (wall-clock time)
4. **False Early-Stop Rate**
5. **Mean Tool Calls** to first `VALIDATED` chain

---

#### 🆚 4. Baselines & Ablation Study

**Direct Comparisons:**
- `PentestGPT` → Tests **RQ1** (world-model gap)
- `VulnBot` → Tests **RQ1** (graph separation)
- `PentestAgent` → Tests **RQ3** (cross-mission learning gap)

**Ablation Study (Isolating architectural components):**
- ❌ *No dual-graph* (flat history only)
- ❌ *ASG only* (no APG reasoning)
- ❌ *No compaction* (unlimited raw history)
- ❌ *No learning* (no cross-mission experience or strategy library)

> *Each ablation proves the contribution of its removed component.*

---

## 🎤 Slide 19 — Summary

We've covered a lot of ground. Let me close by being very precise about what we've built, what we claim, and what we're asking from you today.

---

### 🛠️ What CMatrix Is

A **dual-graph-guided, LLM-orchestrated multi-agent framework** for autonomous Vulnerability Assessment and Penetration Testing.

It maintains two strictly separated graph structures — the **ASG** for what the target *is*, and the **APG** for what can be *done* to it — and uses both to plan, dispatch, validate, and formally terminate a complete VAPT engagement. **No human intervention required after mission start.**

---

### 🛡️ What We Claim

1. **New Architectural Paradigm:** CMatrix is the first autonomous VAPT system to maintain two strictly separated, continuously evolving graph structures for simultaneous discovery and attack reasoning. It is not a refinement of prior approaches.
2. **Theoretically Sound Completion:** Formal dual termination provides a verifiable completion criterion that prior systems cannot express. *"The mission is done because both graphs say so"* is categorically more rigorous than *"the mission is done because the timer fired."*
3. **Cross-Mission Learning:** Accumulates validated exploitation outcomes across all missions. CMatrix is the first system that gets measurably better as it runs more missions.
4. **Reproducibility & Dataset Generation:** The architecture produces a machine-readable decision trace usable for training security-specialized LLMs — a secondary contribution that doesn't exist elsewhere in the literature.

---

### 🗣️ What We're Asking For

We're currently at the **architecture proposal phase**. All twelve contributions are fully specified. No implementation has begun. We're here for your guidance on four things:

- 📐 Are the twelve contributions appropriately scoped for a thesis, or should some be scaled back or consolidated?
- 🧪 Is our HTB/THM ablation plan sufficient to prove the core claims — particularly RQ1 and RQ3?
- 🏗️ Which contributions are most load-bearing and should be fully implemented, versus which can be validated primarily at the architectural level?
- 📍 Based on the contribution level, which publication venue do you think this work is targeting — **USENIX Security**, **IEEE S&P**, or **ACSAC**?

> **Your feedback today determines where we point our implementation effort. We're ready for your questions.**

---

*[End of presentation script]*

---

> **If the supervisor asks a question you don't have a perfect answer for:**
> Don't panic. Say: *"That's a good question. In the current architecture, [your best answer]. This is something we'd want to address more rigorously during implementation — and it's the kind of thing the ablation study would help us characterize precisely."*
>
> Confidence is not about knowing everything. It's about owning what you know and being clear about what you don't. You built this architecture. You understand it. Show that.
