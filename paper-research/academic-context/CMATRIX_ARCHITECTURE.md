# 🛡️ CMatrix Architecture
> **Dual-Graph-Guided LLM-Orchestrated Multi-Agent Framework for Autonomous VAPT**

---

## 🎯 1. What CMatrix Is

CMatrix is a web-based autonomous Vulnerability Assessment and Penetration Testing (VAPT) platform.

It combines two continuously evolving graph structures — the **Attack Surface Graph (ASG)** and the **Attack Path Graph (APG)** — with specialized AI agents, an LLM orchestration layer, and industry-standard offensive security tools to perform end-to-end penetration testing without human intervention.

> 💡 **Core Philosophy**
> The ASG models discovered reality: what the target is. The APG models inferred opportunity: what can be done to it. Together they form the dual-graph world model that drives all agent decisions.

*The goal is not to automate tools.*
*The goal is to automate the reasoning process of a professional penetration tester.*

---

## 📦 2. Deployment Model

CMatrix is distributed as a Docker Compose package.

A user runs a single command on their local machine. All components start inside Docker containers. The user accesses the platform through a browser at `localhost`.

The VAPT tools (Nmap, Metasploit, SQLMap, etc.) run inside the same Docker environment as the backend. The backend communicates with them directly via subprocess and internal APIs. No external infrastructure is required.

### 🏗️ **Deployment topology:**

```text
User's Machine
│
└── 🐳 Docker Compose
    ├── 🖥️ Frontend Container       → Next.js (localhost:3000)
    ├── ⚙️ Backend Container        → FastAPI + LangGraph + Tool Adapters
    ├── 🧠 LLM Container            → Primary LLM via Ollama (OpenAI-compatible)
    ├── 🤖 Auxiliary LLM Container  → Lightweight LLM for summarization/reporting
    ├── 🗄️ Database Container       → PostgreSQL
    ├── 🔀 Queue Container          → Redis + Celery
    ├── 📊 Vector DB Container      → Qdrant
    └── 🧰 Tools Container          → All 11 VAPT tools installed
```

---

## 🔭 3. Scope

### ✅ Included

**🔍 Assessment Modes**
- **Black-Box Testing** — no prior knowledge of target
- **Grey-Box Testing** — partial knowledge (credentials, network ranges)

**🎯 Target Categories**
- Network Infrastructure
- Web Applications
- REST APIs

**🛡️ Security Activities**
- Reconnaissance
- Host and Service Discovery
- Technology Fingerprinting
- Resource and API Enumeration
- Vulnerability Discovery
- Vulnerability Validation
- Exploitation
- Attack Path Validation
- Evidence Collection
- Reporting

### ❌ Excluded

- White-Box Testing and Source Code Analysis
- Mobile, Cloud, IoT, and Wireless Security
- Malware Development
- Lateral Movement and Post-Exploitation Research
- Active Directory Attacks

---

## 🗺️ 4. System Architecture — Birds Eye View

```text
┌─────────────────────────────────────────────────────────────┐
│                        🌐 Browser UI                        │
│         Mission Config · Live Dashboard · Reports           │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP / WebSocket
┌────────────────────────▼────────────────────────────────────┐
│                      ⚙️ FastAPI Backend                     │
│              Session Management · REST API                  │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                  🧠 LangGraph Orchestrator                   │
│         State Machine · Conditional Routing · Planning       │
│                                                              │
│   ┌──────────────────────────────┐  ┌─────────────────────┐  │
│   │ 🕸️ Attack Surface Graph (ASG)│  │🛣️ Attack Path Graph │  │
│   │  Discovered Reality          │  │ (APG)               │  │
│   │  Hosts·Ports·Services        │  │ Inferred Chains     │  │
│   │  Endpoints·Vulns·Evidence    │  │ Risk Scores         │  │
│   └──────────────┬───────────────┘  │ Validation Status   │  │
│                  │ feeds            └────────┬────────────┘  │
│   ┌──────────────▼──────────────────────────▼───────────┐    │
│   │       👑 Commander Agent                            │    │
│   │  [Tiered Prompt · VAPT Protocol · Phase Budget]     │    │
│   │  [Tool Risk Gate Mailbox · reads ASG · writes APG]  │    │
│   └──────────────────────┬──────────────────────────────┘    │
│                          │ spawns (context-isolated)         │
│   ┌──────────────────────▼───────────────────────────────┐   │
│   │     🤖 Specialized Agents  [Phase Budget · ASG Slice]│   │
│   │     Recon · Analysis · Validation · Evidence         │   │
│   │     Report     returns structured ASG/APG output ▲   │   │
│   └──────────────────────┬───────────────────────────────┘   │
│                          │ calls (risk-gated)                │
│   ┌──────────────────────▼──────────────────────────────┐    │
│   │               🔌 Tool Adapter Layer                 │    │
│   │  Tool Risk Gate · InterruptibleToolRunner           │    │
│   │  Parallel Tool Dispatch · MicroCompact              │    │
│   └──────────────────────┬──────────────────────────────┘    │
└──────────────────────────┼───────────────────────────────────┘
                           │ subprocess / REST API / MSFRPC
┌──────────────────────────▼──────────────────────────────────┐
│                    🧰 VAPT Tool Layer                       │
│  Amass · httpx · Nmap · WhatWeb · Gobuster · ffuf           │
│  Nuclei · OWASP ZAP · SQLMap · Metasploit · EyeWitness      │
└─────────────────────────────────────────────────────────────┘
```

---

## ☯️ 5. The Dual-Graph World Model

CMatrix maintains two complementary graph structures as its shared world model. They are kept strictly separate by design — each answers a different question.

> **ASG**  →  *What does the target look like?*   (discovered reality)
> **APG**  →  *What can be done to it?*           (inferred opportunity)

Agents write to the ASG as they discover facts. The Commander reads the ASG and derives the APG as it reasons about attack strategy. The APG feeds back into the Commander's planning, driving prioritization, validation sequencing, and termination decisions.

---

### 🕸️ 5a. Attack Surface Graph (ASG)

The ASG is the **discovered-reality** layer of CMatrix.

It is a continuously evolving knowledge graph that represents the complete discovered state of the target environment. Every tool execution updates it. It is the single shared truth about what the target is at any point in time.

*It is not a task list. It is not a log. It is a living structural model of the target.*

**🗂️ Node types:**

| Node | Represents |
|------|-----------|
| **Domain** | Root domain and discovered subdomains |
| **Host** | IP address, OS, liveness status |
| **Port** | Open port with protocol |
| **Service** | Service name, version, banner |
| **Technology** | Framework, CMS, server software |
| **Endpoint** | Web or API route |
| **Parameter** | Request parameter, header, or input field |
| **Vulnerability** | CVE, misconfiguration, or weakness |
| **Evidence** | Screenshot, response capture, artifact |

**🔗 Edge types:**

| Edge | Meaning |
|------|---------|
| `has_host` | Domain resolves to Host |
| `has_port` | Host exposes Port |
| `runs` | Port runs Service |
| `uses` | Host or Endpoint uses Technology |
| `has_endpoint` | Host or Service has Endpoint |
| `has_parameter` | Endpoint has Parameter |
| `affected_by` | Host or Endpoint affected by Vulnerability |
| `validated_by` | Vulnerability validated by Evidence |

---

### 🛣️ 5b. Attack Path Graph (APG)

The APG is the **inferred-opportunity** layer of CMatrix.

While the ASG records what was discovered, the APG records what can be done with those discoveries. It is populated by the Commander Agent through reasoning over ASG state, and updated continuously as new vulnerabilities are discovered, validated, or ruled out.

The APG is not derived automatically from the ASG. It requires active reasoning: which vulnerabilities chain together, which entry points lead to which impacts, which paths are worth pursuing given current evidence. This reasoning is the Commander's primary intellectual task.

**🗂️ Node types:**

| Node | Represents |
|------|-----------|
| **AttackChain** | An ordered sequence of exploitation steps from entry to impact |
| **ChainStep** | A single step in an attack chain — a specific action on a specific ASG node |
| **Impact** | The business or technical consequence at the end of a chain |

**🔗 Edge types:**

| Edge | Meaning |
|------|---------|
| `starts_at` | AttackChain begins at an ASG Vulnerability or Endpoint node |
| `next_step` | ChainStep leads to the next ChainStep in the chain |
| `achieves` | Final ChainStep achieves an Impact |
| `supported_by` | ChainStep is supported by an ASG Evidence node |

**🏷️ APG node attributes:**

Each AttackChain carries:
- `risk_score` — composite score derived from CVSS severity, exploitability, and impact classification
- `validation_status` — one of `HYPOTHESIZED`, `PARTIALLY_VALIDATED`, `VALIDATED`, `RULED_OUT`
- `priority` — Commander-assigned pursuit priority based on risk score and current mission phase

**⚙️ How the APG is populated:**

1. When the Analysis Agent writes a new Vulnerability node to the ASG, the Commander evaluates whether it extends any existing AttackChain or seeds a new one.
2. When the Validation Agent confirms a vulnerability, the relevant ChainStep's validation_status advances to `VALIDATED` and the chain's risk_score is updated.
3. When a validation attempt fails, the ChainStep is marked `RULED_OUT` and the Commander re-prioritizes remaining chains.
4. When an entire AttackChain reaches `VALIDATED` status from entry to impact, it is linked to its Evidence nodes and flagged for the Report Agent.

> ⚖️ **The separation principle:**
> 
> The ASG never contains hypotheses. It contains only confirmed discovered facts.
> The APG never contains raw scan data. It contains only inferred attack reasoning.
> 
> *This separation is what makes the dual-graph architecture stronger than a single unified graph: agents that write to the ASG (Recon, Analysis, Evidence) never need to reason about attack chains. The Commander that writes to the APG never needs to run tools. Each layer is authoritative for exactly one type of knowledge.*

---

## 🤖 6. Agent Architecture

### 👑 Commander Agent

*The orchestrating brain of CMatrix.*

Reads the current state of the ASG and decides what happens next. Decomposes the mission into objectives. Assigns tasks to specialized agents. Tracks progress. Re-plans dynamically when new findings change the picture.

> 🚫 **The Commander never runs tools directly. It reasons, plans, and delegates.**

**🧠 Key decisions the Commander makes:**
- Which ASG nodes are unexplored and what should be explored next?
- Which Vulnerability nodes in the ASG seed new APG AttackChains?
- Which APG AttackChain has the highest risk score and should be validated first?
- Which agent should act next?
- Has an AttackChain been fully validated end-to-end?
- Is the mission complete — no unexplored ASG nodes and all high-priority APG chains resolved?
- Should a High-risk tool call be approved, rejected, or modified?

### 🧩 Context-Isolated Agent Spawning

Specialized agents in CMatrix are not persistent processes sharing a common context window with the Commander. Each agent is spawned fresh for its assigned task with a precisely scoped context.

At spawn time, the Commander constructs the agent's initial context containing exactly:
- The **ASG slice** relevant to the current task — not the full graph. A Recon Agent working on a single subdomain receives only the Domain and Host nodes for that subdomain, not the full ASG.
- The **APG slice** relevant to the current task, if applicable — a Validation Agent receives the specific AttackChain it is being asked to validate, not the full APG.
- The **restricted tool set** the agent is authorized to call for this task — not the full tool catalog.
- The **task specification** derived from the Commander's current plan.
- The agent's **Phase Budget** for this invocation.

When the agent completes its task (or exhausts its Phase Budget), it does not return its full working context to the Commander. It returns only **structured output** — the set of new ASG nodes and edges it produced. The working context is discarded.

**✨ This design has three direct benefits:**
1. **🪙 Token efficiency** — the Commander's context is never polluted by the raw working history of each specialized agent. Hundreds of tool outputs stay isolated to the agent that produced them.
2. **🛡️ Context integrity** — parallel agents running simultaneously cannot contaminate each other's reasoning context.
3. **🔒 Security boundary** — a High-risk tool call that is rejected at the Tool Risk Gate never appears in the Commander's context at all, preventing the refusal from influencing subsequent Commander planning decisions.

### 🥞 Tiered Prompt Architecture

The Commander Agent assembles its system prompt in three stable tiers to minimize token consumption and enable prefix caching:

| Tier | Contents | Change Frequency |
|------|----------|-----------------|
| **Stable** | Mission parameters, agent identity, tool catalog, assessment mode, VAPT Protocol Prompt | Never changes mid-session |
| **Context** | Current ASG summary + top-priority APG chains — updated at phase boundaries | Changes at phase boundaries |
| **Volatile** | Current task, immediate tool result, timestamp | Changes every turn |

The stable tier is eligible for Anthropic prompt caching — it is sent once and cached. Only the volatile tier burns fresh tokens on each turn. As VAPT sessions grow to hundreds of nodes and tool outputs, this architecture prevents the system prompt from inflating context costs linearly with session length.

### 📜 VAPT Protocol Prompt

The Commander Agent's planning and decision-making policy is defined as a structured, versioned natural language document injected into the stable prompt tier — the **VAPT Protocol Prompt**.

Rather than encoding the Commander's methodology in conditional branching logic inside the LangGraph orchestrator, the protocol is expressed as a first-class artifact. It defines:

- **🔄 Phase sequencing rules** — the order in which assessment phases are executed and the conditions under which phase transitions occur
- **⚡ Re-planning triggers** — specific ASG state changes that cause the Commander to abandon the current plan and re-derive objectives (e.g., discovery of a critical vulnerability mid-enumeration, scope expansion from a newly discovered subdomain)
- **🏁 Termination conditions** — explicit criteria under which the mission is considered complete or exhausted
- **🧰 Tool selection heuristics** — which tools are appropriate for which ASG node types and assessment modes
- **⚠️ Risk escalation rules** — the conditions under which a tool call is classified as High-risk and routed to the Tool Risk Gate

The VAPT Protocol Prompt is versioned alongside the codebase. Different versions implement different methodologies — OWASP Testing Guide, PTES, a custom red-team workflow — without any change to orchestration code. The methodology itself becomes a configurable, swappable, and independently evaluable research variable.

> 🔬 **This separation enables a direct research contribution:** **methodology-as-configuration** — the same agent architecture can be benchmarked under different protocol versions, and the effect of methodology choice on assessment outcomes can be measured and published independently of agent implementation.

---

### 🕵️‍♂️ Recon Agent

*Responsible for all external reconnaissance and host discovery.*

Runs Amass to discover subdomains and enumerate the external attack surface. Runs httpx to validate which discovered hosts are live. Runs Nmap to identify open ports, running services, and operating systems.

All findings are written to the ASG as Domain, Host, Port, and Service nodes.

**⏳ Phase Budget:** 30 iterations. On exhaustion, the Recon Agent writes a structured partial recon result to the ASG, flags the phase as `PARTIAL`, and returns control to the Commander. The Commander re-plans with the partial information.

**🧰 Tools:** Amass · httpx · Nmap

---

### 🔬 Analysis Agent

*Responsible for deep enumeration and vulnerability discovery.*

Once the Recon Agent maps the infrastructure, the Analysis Agent goes deeper. It fingerprints technologies, discovers hidden resources, finds API routes and parameters, and runs automated vulnerability checks.

All findings are written to the ASG as Technology, Endpoint, Parameter, and Vulnerability nodes.

**⏳ Phase Budget:** 50 iterations. On exhaustion, the Analysis Agent writes a structured partial analysis to the ASG, flags the phase as `PARTIAL`, and returns control to the Commander.

**🧰 Tools:** WhatWeb · Gobuster · ffuf · Nuclei · OWASP ZAP

---

### 🎯 Validation Agent

*Responsible for confirming that discovered vulnerabilities are real and exploitable, and for advancing APG AttackChain validation status.*

Does not discover vulnerabilities — it proves them. Receives a specific APG AttackChain from the Commander and executes controlled exploitation to validate each ChainStep in sequence. Confirms impact and traces the complete attack path from entry point to demonstrated impact.

Confirmed ChainSteps are written back to the APG with `validation_status: VALIDATED`. Failed attempts update the relevant ChainStep to `RULED_OUT` and the Commander re-prioritizes. All exploitation evidence is written to the ASG as Evidence nodes and linked to the corresponding APG ChainStep via `supported_by` edges.

**⏳ Phase Budget:** 40 iterations. On exhaustion, the Validation Agent writes confirmed ChainSteps so far, flags remaining steps as `PENDING_VALIDATION`, and returns control to the Commander.

**🧰 Tools:** SQLMap · Metasploit

---

### 📸 Evidence Agent

*Responsible for capturing proof of every significant finding.*

Takes screenshots of exposed admin panels, application pages, and API responses. Captures exploitation results. Links all evidence artifacts to the corresponding ASG nodes so the Report Agent can reference them.

**🧰 Tool:** EyeWitness

---

### 📝 Report Agent

*Responsible for producing the final deliverable.*

Reads the complete ASG and APG and generates a structured penetration test report. Does not run tools. Does not make security decisions. It translates the dual-graph world model into human-readable output.

**📋 Report contains:**
- *Executive Summary* — business impact in plain language, derived from APG Impact nodes
- *Technical Findings* — all vulnerabilities with severity ratings, sourced from ASG Vulnerability nodes
- *Attack Surface Map* — complete discovered environment from ASG
- *Validated Attack Chains* — step-by-step chains from APG with Evidence nodes linked at each step
- *Remediation Guidance* — prioritized fix recommendations ordered by APG risk scores

---

## 🔌 7. Tool Adapter Layer

> 🛑 **Agents never interact with tools directly.**

Every tool is wrapped in a **Tool Adapter** — a standardized interface that accepts structured parameters from an agent, executes the tool (via `subprocess`, `REST API`, or `MSFRPC`), parses the raw output, and returns a structured result ready for ASG ingestion.

**✨ This abstraction means:**
- Agents reason about targets, not command syntax
- Tools can be swapped or upgraded without touching agent logic
- All tool outputs are normalized before reaching the ASG
- Errors and timeouts are handled consistently

### 🚦 Tool Risk Gate

Not all tool executions carry the same risk. Some are read-only and reversible. Others are destructive, scope-sensitive, or irreversible. The **Tool Risk Gate** enforces a mandatory approval checkpoint between an agent's decision to call a tool and the actual execution of that call.

**📊 Every tool adapter is classified with a risk tier:**

| Risk Tier | Examples | Handling |
|-----------|----------|---------|
| 🟢 **Low** | Amass, httpx, WhatWeb, Nmap (discovery) | Execute immediately, log to ASG |
| 🟡 **Medium** | Gobuster, ffuf, Nuclei, OWASP ZAP | Log decision to ASG, execute after brief scope check |
| 🔴 **High** | SQLMap (--dump, --os-shell), Metasploit (exploit execution), Nmap (--script vuln on new scope) | Route to Commander mailbox for approval before execution |

When a High-risk tool call is dispatched, the calling agent does not execute. Instead it deposits an **approval request** into the Commander's mailbox — a structured message containing the tool name, parameters, target ASG node, and the agent's rationale. The Commander evaluates the request against the current mission scope, ASG state, and VAPT Protocol Prompt risk escalation rules, then either approves, rejects, or modifies the call.

An **atomic claim mechanism** ensures that if multiple agents simultaneously deposit approval requests (possible during parallel tool dispatch), each request is claimed and evaluated independently. No two approval evaluations can race on the same request.

> 🔒 **This architecture provides a critical safety property:** **no irreversible offensive operation executes without Commander-level scope validation**. It also provides a structured audit trail — every High-risk execution has a logged approval decision with rationale, making the report fully traceable to authorized actions.

For fully autonomous missions, the Commander approves automatically based on protocol rules. For supervised missions, a human operator can be inserted at the mailbox evaluation step — enabling a human-in-the-loop mode without any change to agent logic.

### 🛑 InterruptibleToolRunner

Every tool execution runs inside a cancellable thread or process managed by the `InterruptibleToolRunner`. The main orchestration loop monitors for interrupt signals while the tool runs in the background.

**⚡ An interrupt is triggered when:**
- The Cycle Guard fires (agent fixation detected)
- The LLM context approaches the window limit
- An agent's Phase Budget is exhausted
- The user explicitly stops a mission

When interrupted, the tool thread is abandoned cleanly and no partial output is injected into the ASG or conversation history. This is distinct from the Cycle Guard — the Cycle Guard detects fixation and forces a re-plan; the `InterruptibleToolRunner` is the hard kill switch that enforces it.

### ⚡ Parallel Tool Dispatch

When a Commander or Analysis Agent dispatches multiple tools in a single planning step, the Tool Adapter Layer identifies non-dependent tool calls from ASG state and executes them concurrently via `ThreadPoolExecutor`.

Non-dependency is determined by checking whether the inputs of each tool call reference the same ASG nodes. Tools operating on independent nodes (e.g., Gobuster on `/admin` and ffuf on `/api`) are safe to parallelize. Results are reassembled in the original dispatch order before being written to the ASG, preserving deterministic graph update semantics.

> 🛠️ **This is a core engineering contribution:** **ASG-aware parallel tool dispatch** — the ASG provides the dependency information that makes safe parallelization possible without hardcoded tool ordering rules.

**🧰 Tool integration methods:**

| Tool | Integration |
|------|------------|
| **Amass** | subprocess |
| **httpx** | subprocess |
| **Nmap** | subprocess |
| **WhatWeb** | subprocess |
| **Gobuster** | subprocess |
| **ffuf** | subprocess |
| **Nuclei** | subprocess |
| **OWASP ZAP** | REST API via python-owasp-zap-v2.4 |
| **SQLMap** | subprocess |
| **Metasploit** | MSFRPC via pymetasploit3 |
| **EyeWitness** | subprocess |

---

## 🏢 8. Shared Infrastructure

### 🕹️ LangGraph Orchestrator

Manages the agent execution graph as a stateful state machine. Each node in the graph is an agent. Edges represent conditional transitions based on ASG state and Commander decisions. Handles agent sequencing, parallel execution where safe, and loop detection.

### 🗜️ Three-Layer ASG-Backed Context Compaction

VAPT sessions are long-running. A single Nmap scan on a large subnet produces tens of thousands of lines of raw output. A full Nuclei run can return hundreds of findings. Without active compaction, LLM context windows overflow within hours.

CMatrix uses a three-layer compaction system. The key architectural insight is that the ASG makes aggressive compaction safe: all discovered facts are persisted in the graph. Conversation history is expendable. The ASG is not.

> **🟢 Layer 1 — MicroCompact (zero API cost)**
> 
> Raw tool output is compacted at the Tool Adapter boundary before it enters the conversation at all. Each tool adapter's parser extracts the structured findings, writes them to the ASG, and injects only a compact summary into the agent's working context. The full raw output is stored in PostgreSQL but never enters the LLM conversation history. This is the first and cheapest compaction layer — it runs on every single tool call.

> **🟡 Layer 2 — AutoCompact (Auxiliary LLM, triggered at 60% context)**
> 
> When the agent's conversation history reaches 60% of the primary model's context window, AutoCompact triggers. The Auxiliary LLM summarizes older conversation turns into a compact structured summary while preserving the last N turns intact. Tool call / ASG update pairs are always kept together and never split. The summary is injected in place of the compressed turns. The primary model continues without interruption.

> **🔴 Layer 3 — FullCompact (triggered at 85% context)**
> 
> When conversation history reaches 85% of the context window, FullCompact triggers. The entire conversation history is compressed. The agent's working context is reconstructed from: the current ASG snapshot (freshly rendered), the current APG priority chains, the current VAPT Protocol state, and the last N tool results. Nothing else is needed — all findings are in the ASG and all attack reasoning is in the APG. History beyond the last N turns is archived to PostgreSQL and dropped from the active context.

**Because the dual graph is a lossless persistent store of all discoveries and all attack reasoning, FullCompact loses no intelligence — only the conversational scaffolding that produced those discoveries.**
*This is the property that no general-purpose agent can claim:* **CMatrix can compress conversation history to near-zero without losing any findings or attack chain state, because everything lives in the graph, not the context window.**


### 🔄 Cycle Guard

A micro-level loop detector embedded in the Commander Agent. If any agent calls the same tool with identical parameters more than N consecutive times without producing new ASG nodes or edges, the Cycle Guard flags the execution as stuck and forces a re-plan. This complements the ASG-driven macro termination condition (no unexplored paths remain) with a safety net against agent fixation on a single approach.

### 🪞 Reflector

A failure recovery component invoked when an agent fails to produce a valid tool call after repeated attempts. The Reflector analyzes the failure context and provides corrective guidance — redirecting the agent toward an alternative tool, a different strategy, or a graceful task completion. Prevents silent agent failures from stalling the pipeline.

### 🔀 Celery + Redis (Task Queue)

VAPT tool runs are long-running and asynchronous. Celery manages the task queue. Redis acts as the message broker. The frontend receives live updates via WebSocket as tasks complete and the ASG evolves.

### 🐘 PostgreSQL

Persistent storage for all session data — missions, agent decisions, task history, and raw tool outputs. The ASG is reconstructable from PostgreSQL at any time.

### 🗃️ Qdrant (Vector Database)

Stores CVE descriptions, exploit patterns, and historical scan knowledge as vector embeddings. The Commander and Analysis agents query Qdrant for context-relevant vulnerability intelligence during planning and analysis.

### 🧠 LLM Layer

All agents use a locally hosted LLM via an OpenAI-compatible endpoint (served by Ollama). The LLM is model-agnostic — any capable model can be configured. The default recommended model is DeepSeek-R1-Distill-Qwen-32B at Q4_K_M quantization.

The LLM receives ASG context, current objectives, and tool outputs as structured prompts. It returns decisions, plans, and analysis in structured formats that the orchestrator can act on.

### 🤖 Auxiliary LLM Client

A separate lightweight LLM client handles side tasks that do not require primary model reasoning capacity:

- **Context summarization** — feeds the Context Summarizer with compressed representations of older conversation turns
- **ASG-to-text rendering** — translates the full ASG into structured prose for the Report Agent
- **Evidence description generation** — produces human-readable descriptions of EyeWitness screenshot captures

The Auxiliary LLM Client uses a smaller, cheaper model than the primary reasoning model. This preserves primary model context window capacity for agent planning and decision-making. The primary model handles all agent reasoning; the Auxiliary handles all synthesis, compression, and reporting workloads.

---

## 🖥️ 9. Frontend

Browser-based interface accessible at `localhost:3000`.

**⚙️ Mission Configuration Panel**
- Define target scope, assessment mode (Black-Box / Grey-Box), and constraints
- Start, pause, and stop missions

**📈 Live Dashboard**
- Real-time ASG visualization as an interactive graph — structural view of the target environment
- Real-time APG visualization — active AttackChains with validation status and risk scores
- Agent activity feed — what each agent is doing right now
- Tool execution log — live terminal output from running tools
- Finding stream — vulnerabilities and nodes as they are discovered

**📄 Report Panel**
- View, export, and download the final penetration test report

---

## 🏎️ 10. Autonomous Planning Cycle

CMatrix operates on a continuous **Observe–Reason–Plan–Execute** loop driven by the Commander Agent.

```text
Observe ASG    → Read current ASG state (scoped slice per task)
Observe APG    → Read current AttackChain priorities and validation status
Reason         → Identify ASG gaps + derive / update APG chains from new Vulnerability nodes
Plan           → Decompose next objective (per VAPT Protocol Prompt): explore ASG gaps  OR  validate highest-priority APG chain
Spawn          → Spawn context-isolated agent with scoped ASG + APG slice + restricted toolset
Gate           → Route High-risk tool calls through Tool Risk Gate mailbox
Execute        → Run approved tool via adapter (MicroCompact raw output → ASG)
Update ASG     → Agent writes discovered nodes and edges to ASG
Update APG     → Commander derives new chains or advances chain validation status
Return         → Agent returns structured ASG/APG delta; working context discarded
Re-Plan        → Commander re-reads dual graph, decides next action
Compact        → AutoCompact at 60% context; FullCompact at 85% context
```

**🏁 The cycle terminates when:**
- No unexplored nodes remain in the ASG
- All APG AttackChains are in a terminal state (`VALIDATED` or `RULED_OUT`)
- User-defined constraints (time limit, scope boundary) are reached

---

## ⚔️ 11. Exploitation Philosophy

CMatrix treats exploitation as a **reasoning activity**, not a shell-collection exercise.

> 🏆 **Success is defined as validated APG AttackChains with evidence, not obtained shells.**

**✅ A penetration test is considered complete when:**
- The attack surface is fully mapped in the ASG
- Vulnerabilities are discovered, classified, and seeded into APG AttackChains
- APG AttackChains are prioritized by risk score and pursued in order
- Each ChainStep is validated through controlled exploitation
- Complete chains from entry to impact are confirmed with linked Evidence
- A professional report is generated from the dual-graph state

*A shell alone does not constitute success.*
*A validated, evidenced, documented AttackChain does.*

**🏷️ APG Chain validation levels:**

| Status | Meaning |
|--------|---------|
| ⚪ `HYPOTHESIZED` | Commander has inferred a possible chain from ASG Vulnerability nodes — not yet tested |
| 🟡 `PARTIALLY_VALIDATED` | One or more ChainSteps confirmed; chain not yet complete end-to-end |
| 🟢 `VALIDATED` | All ChainSteps confirmed with Evidence; Impact demonstrated |
| 🔴 `RULED_OUT` | A required ChainStep failed validation; chain is not exploitable as hypothesized |

---

## 🔬 12. Research Contributions

| # | Contribution |
|---|-------------|
| **C1** | **Dual-graph world model for autonomous VAPT** — Attack Surface Graph (ASG) capturing discovered reality and Attack Path Graph (APG) capturing inferred opportunity, maintained as strictly separate structures with a clean separation of concerns: ASG contains only confirmed facts, APG contains only attack reasoning |
| **C2** | **LLM-orchestrated multi-agent architecture** for end-to-end autonomous VAPT without human intervention |
| **C3** | **Dual-graph shared state** — agents that discover write to the ASG; the Commander that reasons writes to the APG; no agent conflates fact-collection with attack-chain inference |
| **C4** | **Dynamic planning driven by dual-graph state** — Commander re-plans when new ASG Vulnerability nodes seed new APG AttackChains, when chain validation status changes, or when chains are ruled out; planning is always grounded in current graph state |
| **C5** | **Autonomous tool selection and execution** through a unified Tool Adapter Layer with typed parsers feeding the ASG |
| **C6** | **Unified assessment** across Network, Web, and API targets with black-box and grey-box routing in a single pipeline |
| **C7** | **Evidence-driven vulnerability validation** with evidence artifacts linked to APG ChainStep nodes via `supported_by` edges, making every validated chain fully traceable to its proof |
| **C8** | **APG-guided attack chain generation**, risk scoring, prioritization, and end-to-end validation — attack chains are first-class APG entities with explicit validation lifecycle: `HYPOTHESIZED` → `PARTIALLY_VALIDATED` → `VALIDATED` / `RULED_OUT` |
| **C9** | **ASG-aware parallel tool dispatch** — dependency-safe concurrent tool execution using the ASG as the dependency graph, with ordered result reassembly before graph update |
| **C10** | **Tiered prompt architecture** with prompt caching — stable/context/volatile prompt split enabling prefix caching on the stable tier, reducing token cost for long VAPT sessions |
| **C11** | **Phase Budget with graceful degradation** — per-agent iteration caps with structured partial result handoff, enabling the Commander to re-plan under real-world time constraints |
| **C12** | **Tool Risk Gate with Commander mailbox approval** — mandatory scope validation checkpoint for High-risk offensive operations, with atomic claim mechanism preventing concurrent approval races; enables human-in-the-loop insertion without architectural change |
| **C13** | **ASG-backed lossless context compaction** — three-layer compaction (MicroCompact / AutoCompact / FullCompact) where FullCompact can reduce conversation history to near-zero without losing any findings, because all discoveries are persisted in the ASG |
| **C14** | **Context-isolated agent spawning** — each specialized agent receives only a scoped ASG/APG slice and restricted tool set at spawn time; returns only structured graph output to the Commander, eliminating cross-agent context contamination |
| **C15** | **Methodology-as-configuration via VAPT Protocol Prompt** — Commander planning policy encoded as a versioned natural language document, enabling different assessment methodologies (OWASP, PTES, custom) to be benchmarked as independent research variables without code changes |
| **C16** | **Dual-graph termination semantics** — mission completion is defined by both ASG exhaustion (no unexplored nodes) and APG resolution (all chains in terminal state), providing a formally grounded termination condition that neither pure task-queue nor pure graph-traversal systems can express |

---

## 🆚 13. Differentiation from Related Work

| System | What it does | What CMatrix adds |
|--------|-------------|-------------------|
| [**PentestGPT: Evaluating and Harnessing Large Language Models for Automated Penetration Testing**](7-list-of-paper-professor.md#26-pentestgpt-evaluating-and-harnessing-large-language-models-for-automated-penetration-testing) (USENIX '24) | LLM guidance with human-in-the-loop | Fully autonomous; no human required during execution |
| [**AutoAttacker: A Large Language Model Guided System to Implement Automatic Cyber-attacks**](6-list-of-paper-curated.md#56-autoattacker-a-large-language-model-guided-system-to-implement-automatic-cyber-attacks) (arXiv '24) | LLM-guided post-breach automation | Full VAPT pipeline from recon to reporting |
| [**Teams of LLM Agents Can Exploit Zero-Day Vulnerabilities**](6-list-of-paper-curated.md#54-teams-of-llm-agents-can-exploit-zero-day-vulnerabilities) (arXiv '24) | Multi-agent web exploitation | Network + Web + API scope; ASG world model |
| [**PentestAgent: Incorporating LLM Agents to Automated Penetration Testing**](6-list-of-paper-curated.md#18-pentestagent-incorporating-llm-agents-to-automated-penetration-testing) (AsiaCCS '25) | Multi-agent with RAG and shared memory | ASG replaces flat memory; structured attack path generation |
| [**VulnBot: Autonomous Penetration Testing for a Multi-Agent Collaborative Framework**](6-list-of-paper-curated.md#21-vulnbot-autonomous-penetration-testing-for-a-multi-agent-collaborative-framework) (arXiv '25) | Penetration Task Graph for task planning | ASG models the target environment, not just task dependencies |
| **PentAGI** (GitHub, production) | General-purpose autonomous agent framework with pentest prompts and 20+ tools in Kali container | Purpose-built VAPT with typed ASG world model, attack path generation, black/grey-box routing, evidence linked to ASG nodes, Tool Risk Gate for offensive operation safety — not a generic framework retargeted at security |

> 🌉 **The gap CMatrix fills:**
> 
> No published system uses a dual-graph world model — a continuously evolving Attack Surface Graph (discovered reality) paired with an Attack Path Graph (inferred opportunity) — as the shared foundation driving all agent decisions across a unified Network + Web + API assessment pipeline with explicit attack chain generation, risk scoring, and lifecycle-tracked validation.

**🥊 CMatrix vs PentAGI — specific technical distinctions:**

PentAGI is a capable system (15k+ GitHub stars, production deployments) but it is architecturally a generic agent framework. Its agents reason from flat task history and vector memory. It has no model of the target environment — only a model of its own past actions. When PentAGI finishes a task, it knows what it did. It does not know what the target looks like, and it has no representation of what attack chains are possible.

CMatrix maintains two complementary models: the ASG knows what the target is; the APG knows what can be done to it. Agents write only facts to the ASG. The Commander derives attack reasoning into the APG. No other published VAPT system separates these two concerns into distinct structures.

**Additional distinctions:**
- PentAGI has no black-box / grey-box assessment mode concept. CMatrix routes agent behavior and tool selection based on declared assessment mode.
- PentAGI stores evidence as flat artifacts. CMatrix links evidence to APG ChainStep nodes via `supported_by` edges, making every validated chain directly traceable to its proof.
- PentAGI generates no explicit attack paths. CMatrix generates, scores, prioritizes, and tracks the full validation lifecycle of APG AttackChains.
- PentAGI terminates when the task queue is empty. CMatrix terminates when the ASG has no unexplored nodes AND all APG chains are in a terminal state — a formally grounded dual termination condition.

---

## ⚖️ 14. Source of Truth Statement

> 📜 **This document is the authoritative architecture, scope, and design specification for CMatrix.**

All implementation, experimentation, benchmarking, publication, and extension of CMatrix **must remain consistent** with the principles defined here.

*When implementation details conflict with this document, this document governs.*
