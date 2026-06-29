# Module 08 — Visual Walkthrough: CMatrix Architecture in Diagrams

> **How to read this module:** Every diagram here is a visual translation of a concept already explained in Modules 01–07. If a box or arrow is unfamiliar, refer back to the relevant module. This file adds *no new concepts* — it only makes existing ones visible.

---

*Module 02, Figure 1 below: Dual-Graph Model (ASG node tree + APG attack chain, visualised)*

---

## Module 02, Figure 1 — The Dual-Graph Model: ASG + APG Visualised

This diagram shows both graphs side-by-side using the `shopvault.io` mission as a concrete example. Left side = ASG (what was discovered). Right side = APG (what can be done with it). The vertical barrier in the middle = the strict separation boundary.

### Figure 1A — ASG: The Attack Surface Graph (Discovered Reality)

Every node here represents something **confirmed by a tool**. Every edge represents a **confirmed relationship**. No guesses. No hypotheses.

```mermaid
graph TD
    %% ── ASG ROOT ──────────────────────────────────────────────
    DOM["🌐 Domain<br/>shopvault.io"]

    %% ── HOSTS ─────────────────────────────────────────────────
    H1["🖥️ Host<br/>10.0.0.1<br/>OS: Ubuntu 22.04"]
    H2["🖥️ Host<br/>10.0.0.2<br/>OS: Debian 11"]
    H3["🖥️ Host<br/>api.shopvault.io<br/>10.0.0.5"]

    %% ── PORTS ─────────────────────────────────────────────────
    P443["🔌 Port :443<br/>tcp · open"]
    P8080["🔌 Port :8080<br/>tcp · open · unencrypted"]
    P80["🔌 Port :80<br/>tcp · open"]
    P22["🔌 Port :22<br/>tcp · open"]

    %% ── SERVICES ──────────────────────────────────────────────
    SVC1["⚙️ Service<br/>Nginx 1.18.0"]
    SVC2["⚙️ Service<br/>HTTP unencrypted"]
    SVC3["⚙️ Service<br/>OpenSSH 8.9p1"]

    %% ── TECHNOLOGIES ──────────────────────────────────────────
    TECH1["📦 Technology<br/>WordPress 5.9.3"]
    TECH2["📦 Technology<br/>WooCommerce 6.1"]
    TECH3["📦 Technology<br/>Django 4.1.2"]

    %% ── ENDPOINTS ─────────────────────────────────────────────
    EP1["🔗 Endpoint<br/>/wp-admin/login<br/>sensitivity: HIGH"]
    EP2["🔗 Endpoint<br/>/backup/db_export.sql<br/>sensitivity: CRITICAL"]
    EP3["🔗 Endpoint<br/>/api/v1/orders"]
    EP4["🔗 Endpoint<br/>/api/v1/internal/users<br/>undocumented!"]

    %% ── PARAMETERS ────────────────────────────────────────────
    PARAM1["⚙️ Parameter<br/>user_id=?<br/>injectable: TRUE"]

    %% ── VULNERABILITIES ───────────────────────────────────────
    VULN1["🚨 Vulnerability<br/>CVE-2022-21661<br/>CVSS: 8.8 · SQLi<br/>PoC: Exploit-DB ✓<br/>Metasploit module ✓"]
    VULN2["🚨 Vulnerability<br/>IDOR on /api/v1/orders<br/>Severity: HIGH"]
    VULN3["🚨 Vulnerability<br/>Exposed DB backup<br/>Severity: CRITICAL"]

    %% ── EVIDENCE ──────────────────────────────────────────────
    EV1["📎 Evidence<br/>sqli-extraction.txt"]
    EV2["📎 Evidence<br/>admin-panel.png"]
    EV3["📎 Evidence<br/>webshell-rce.png"]

    %% ── EDGES ─────────────────────────────────────────────────
    DOM -->|has_host| H1
    DOM -->|has_host| H2
    DOM -->|has_host| H3

    H1 -->|has_port| P443
    H1 -->|has_port| P22
    H2 -->|has_port| P8080
    H3 -->|has_port| P80

    P443 -->|runs| SVC1
    P8080 -->|runs| SVC2
    P22 -->|runs| SVC3

    H1 -->|uses| TECH1
    H1 -->|uses| TECH2
    H3 -->|uses| TECH3

    TECH1 -->|affected_by| VULN1

    SVC1 -->|has_endpoint| EP1
    SVC1 -->|has_endpoint| EP2
    H3 -->|has_endpoint| EP3
    H3 -->|has_endpoint| EP4

    EP3 -->|has_parameter| PARAM1
    PARAM1 -->|affected_by| VULN2
    EP2 -->|affected_by| VULN3

    VULN1 -->|validated_by| EV1
    VULN1 -->|validated_by| EV2
    VULN1 -->|validated_by| EV3

    %% ── STYLES ────────────────────────────────────────────────
    style DOM fill:#062210,stroke:#7FFF00,color:#7FFF00
    style H1 fill:#062210,stroke:#7FFF00,color:#7FFF00
    style H2 fill:#062210,stroke:#7FFF00,color:#7FFF00
    style H3 fill:#062210,stroke:#7FFF00,color:#7FFF00
    style P443 fill:#062210,stroke:#7FFF00,color:#7FFF00
    style P8080 fill:#062210,stroke:#7FFF00,color:#7FFF00
    style P80 fill:#062210,stroke:#7FFF00,color:#7FFF00
    style P22 fill:#062210,stroke:#7FFF00,color:#7FFF00
    style SVC1 fill:#062210,stroke:#7FFF00,color:#7FFF00
    style SVC2 fill:#062210,stroke:#7FFF00,color:#7FFF00
    style SVC3 fill:#062210,stroke:#7FFF00,color:#7FFF00
    style TECH1 fill:#082018,stroke:#00D4FF,color:#00D4FF
    style TECH2 fill:#082018,stroke:#00D4FF,color:#00D4FF
    style TECH3 fill:#082018,stroke:#00D4FF,color:#00D4FF
    style EP1 fill:#082018,stroke:#00D4FF,color:#00D4FF
    style EP2 fill:#1A0404,stroke:#FF5252,color:#FF5252
    style EP3 fill:#082018,stroke:#00D4FF,color:#00D4FF
    style EP4 fill:#082018,stroke:#00D4FF,color:#00D4FF
    style PARAM1 fill:#082018,stroke:#00D4FF,color:#00D4FF
    style VULN1 fill:#220606,stroke:#FF5252,color:#FF5252
    style VULN2 fill:#220606,stroke:#FF5252,color:#FF5252
    style VULN3 fill:#220606,stroke:#FF5252,color:#FF5252
    style EV1 fill:#120820,stroke:#9C27B0,color:#CE93D8
    style EV2 fill:#120820,stroke:#9C27B0,color:#CE93D8
    style EV3 fill:#120820,stroke:#9C27B0,color:#CE93D8
```

**Node colour key:**
- 🟢 **Lime** — Domain, Host, Port, Service (infrastructure layer)
- 🔵 **Cyan** — Technology, Endpoint, Parameter (application layer)
- 🔴 **Red** — Vulnerability (weakness layer)
- 🟣 **Purple** — Evidence (proof layer)

---

### Figure 1B — APG: The Attack Path Graph (Inferred Opportunity)

The Commander reads the ASG and reasons: *"These vulnerabilities can chain together into complete attack paths."* Those chains live here — in the APG.

```mermaid
flowchart TD
    %% ── CHAIN 01 ──────────────────────────────────────────────────
    subgraph C1["AttackChain: Chain-01 · risk_score: 9.1 · VALIDATED"]
        direction TB
        C1S["starts_at → ASG: CVE-2022-21661<br/>(WordPress SQLi, CVSS 8.8)"]

        STEP1["ChainStep 1<br/>─────────────<br/>Tool: SQLMap<br/>Target: /wp-admin/admin-ajax.php<br/>Action: Confirm WP_Query SQLi<br/>Status: ✅ VALIDATED<br/>↗ supported_by: sqli-extraction.txt"]

        STEP2["ChainStep 2<br/>─────────────<br/>Tool: SQLMap --dump<br/>Action: Extract WordPress users table<br/>Hash cracked offline → admin:Summer2023!<br/>Status: ✅ VALIDATED<br/>↗ supported_by: users-table-dump.png"]

        STEP3["ChainStep 3<br/>─────────────<br/>Tool: Metasploit<br/>Module: wp_admin_shell_upload<br/>Action: Deploy webshell → RCE<br/>Status: ✅ VALIDATED<br/>↗ supported_by: webshell-rce.png"]

        IMP1["💀 IMPACT<br/>─────────────<br/>Full RCE on shopvault.io web server<br/>Customer PII database accessible<br/>Classification: CRITICAL"]

        C1S --> STEP1
        STEP1 -->|next_step| STEP2
        STEP2 -->|next_step| STEP3
        STEP3 -->|achieves| IMP1
    end

    %% ── CHAIN 02 ──────────────────────────────────────────────────
    subgraph C2["AttackChain: Chain-02 · risk_score: 7.5 · VALIDATED"]
        direction TB
        C2S["starts_at → ASG: IDOR on /api/v1/orders<br/>(user_id parameter unsanitised)"]

        STEP21["ChainStep 1<br/>─────────────<br/>Tool: SQLMap<br/>Action: Confirm IDOR — user_id param injectable<br/>API returns any user's orders without auth check<br/>Status: ✅ VALIDATED<br/>↗ supported_by: idor-orders-dump.png"]

        IMP2["💀 IMPACT<br/>─────────────<br/>All customer order history exposed<br/>Name · address · payment method visible<br/>Classification: HIGH"]

        C2S --> STEP21
        STEP21 -->|achieves| IMP2
    end

    %% ── CHAIN 03 ─────────────────────────────────────────────────
    subgraph C3["AttackChain: Chain-03 · risk_score: 8.1 · VALIDATED"]
        direction TB
        C3S["starts_at → ASG: SQL error on staging.shopvault.io/login<br/>(blind SQLi entry point)"]

        STEP31["ChainStep 1<br/>─────────────<br/>Tool: SQLMap<br/>Target: staging.shopvault.io/login<br/>Action: Confirm blind SQLi<br/>Extract staging database credentials table<br/>Status: ✅ VALIDATED<br/>↗ supported_by: staging-db-dump.png"]

        IMP3["💀 IMPACT<br/>─────────────<br/>Staging DB credentials extracted<br/>Credential reuse risk flagged:<br/>staging creds partially overlap production<br/>Classification: HIGH"]

        C3S --> STEP31
        STEP31 -->|achieves| IMP3
    end

    %% ── CHAIN 04 ─────────────────────────────────────────────────
    subgraph C4["AttackChain: Chain-04 · risk_score: 7.0 · VALIDATED"]
        direction TB
        C4S["starts_at → ASG: Exposed /backup/db_export_2023.sql<br/>(Information Disclosure misconfiguration)"]

        STEP41["ChainStep 1<br/>─────────────<br/>Action: Direct HTTP GET of .sql file<br/>File publicly accessible — no auth required<br/>Status: ✅ VALIDATED immediately<br/>↗ supported_by: db-backup-download.png"]

        IMP4["💀 IMPACT<br/>─────────────<br/>Full customer PII database exposed<br/>Direct download — no exploitation needed<br/>Classification: CRITICAL"]

        C4S --> STEP41
        STEP41 -->|achieves| IMP4
    end

    %% ── PRIORITY RANKING ──────────────────────────────────────────
    PRIO["📊 APG Priority Queue<br/>──────────────────────<br/>#1 Chain-01 · 9.1 (escalated after RCE) ← validated first<br/>#2 Chain-03 · 8.1 ← validated second<br/>#3 Chain-02 · 7.5 ← validated third<br/>#4 Chain-04 · 7.0 ← trivially validated in Phase 4<br/><br/>Commander re-ranks on every status change"]

    %% Styles
    style C1 fill:#1E1004,stroke:#FFC107,color:#FFC107
    style C2 fill:#1E1004,stroke:#FFC107,color:#FFC107
    style C3 fill:#1E1004,stroke:#FFC107,color:#FFC107
    style C4 fill:#1E1004,stroke:#FFC107,color:#FFC107
    style STEP1 fill:#0E0C02,stroke:#7FFF00,color:#7FFF00
    style STEP2 fill:#0E0C02,stroke:#7FFF00,color:#7FFF00
    style STEP3 fill:#0E0C02,stroke:#7FFF00,color:#7FFF00
    style IMP1 fill:#200818,stroke:#9C27B0,color:#CE93D8
    style STEP21 fill:#0E0C02,stroke:#7FFF00,color:#7FFF00
    style IMP2 fill:#200818,stroke:#9C27B0,color:#CE93D8
    style STEP31 fill:#0E0C02,stroke:#7FFF00,color:#7FFF00
    style IMP3 fill:#200818,stroke:#9C27B0,color:#CE93D8
    style STEP41 fill:#0E0C02,stroke:#7FFF00,color:#7FFF00
    style IMP4 fill:#200818,stroke:#9C27B0,color:#CE93D8
    style PRIO fill:#06101E,stroke:#00D4FF,color:#00D4FF
```

### What the Two Graphs Together Tell You

| Question | Answered By |
|----------|------------|
| "What hosts exist on shopvault.io?" | ASG → Domain → Host nodes |
| "What software is running on port 443?" | ASG → Port → Service → Technology nodes |
| "Which vulnerabilities were found?" | ASG → Vulnerability nodes (with CVSS, PoC status) |
| "What are the complete attack paths?" | APG → AttackChain nodes (with ChainSteps) |
| "Which attack is most dangerous?" | APG → risk_score ranking |
| "Is each attack actually proven?" | APG → validation_status + supported_by → ASG Evidence |
| "What is the proof?" | ASG → Evidence nodes (screenshots, tool outputs) |

---

## Module 03, Figure 1 — System Architecture: The Three-Tier Overview

This is the master view of CMatrix. Everything fits into three tiers:

- **Tier 1 (top):** Orchestration — the operator configures, the Commander reasons
- **Tier 2 (middle):** The dual-graph world model — the two living knowledge stores
- **Tier 3 (bottom):** The six specialist agents and the tool layer they operate through

```mermaid
flowchart TD
    %% ── TIER 1: ORCHESTRATION ──────────────────────────────────────
    subgraph T1["① ORCHESTRATION TIER"]
        direction LR
        OP["🧑 OPERATOR<br/>─────────────<br/>Defines: Target domain<br/>Scope boundaries<br/>Assessment mode<br/>(Black-Box / Grey-Box)"]
        CMD["👑 COMMANDER AGENT<br/>─────────────────────────────<br/>• Reads full ASG + APG state<br/>• Plans and delegates tasks<br/>• Seeds APG AttackChains<br/>• Approves High-risk tool calls<br/>• Writes ONLY to APG<br/>• Determines termination"]
        VPP["📄 VAPT PROTOCOL PROMPT<br/>──────────────────────────<br/>Methodology-as-Config:<br/>• Phase sequencing rules<br/>• Re-plan triggers<br/>• Termination conditions<br/>• Tool selection heuristics"]

        OP -- "mission config<br/>(target + scope)" --> CMD
        CMD <-- "guides<br/>planning policy" --> VPP
    end

    %% ── TIER 2: DUAL-GRAPH WORLD MODEL ─────────────────────────────
    subgraph T2["② DUAL-GRAPH WORLD MODEL TIER"]
        direction LR
        subgraph ASG["🟢 ATTACK SURFACE GRAPH (ASG)<br/>── Discovered Reality ──<br/>Facts ONLY. Never contains hypotheses."]
            A1["Domain · Host · Port<br/>Service · Technology"]
            A2["Endpoint · Parameter<br/>Vulnerability · Evidence"]
        end
        SEP["⬛ STRICT<br/>SEPARATION<br/>────────<br/>No agent<br/>crosses this<br/>boundary"]
        subgraph APG["🟡 ATTACK PATH GRAPH (APG)<br/>── Inferred Opportunity ──<br/>Reasoning ONLY. Never contains raw scan data."]
            P1["AttackChain<br/>risk_score · priority"]
            P2["ChainStep<br/>validation_status"]
            P3["Impact<br/>(demonstrated)"]
        end
    end

    %% ── TIER 3: AGENTS + TOOLS ──────────────────────────────────────
    subgraph T3["③ SPECIALIZED AGENTS + TOOL ADAPTER TIER"]
        direction LR
        AGR["🕵️ Recon<br/>Amass·httpx·Nmap"]
        AGA["🔬 Analysis<br/>WhatWeb·Gobuster<br/>ffuf·Nuclei·ZAP"]
        AGI["🔍 Research<br/>NVD·Exploit-DB<br/>GitHub"]
        AGV["🎯 Validation<br/>SQLMap·Metasploit"]
        AGE["📸 Evidence<br/>EyeWitness"]
        AGRP["📝 Report<br/>Reads ASG+APG"]

        subgraph TAL["TOOL ADAPTER LAYER + RISK GATE"]
            RG1["🟢 LOW<br/>Execute immediately"]
            RG2["🟡 MED<br/>LLM Classifier"]
            RG3["🔴 HIGH<br/>Commander Mailbox"]
        end
    end

    %% ── CROSS-TIER ARROWS ───────────────────────────────────────────
    CMD -- "reads state" --> ASG
    APG -- "status feedback" --> CMD
    CMD -- "derives chains<br/>from new Vulnerability nodes" --> APG
    CMD -- "spawns with<br/>scoped context" --> AGR
    CMD -- "spawns with<br/>scoped context" --> AGA
    CMD -- "spawns with<br/>scoped context" --> AGI
    CMD -- "spawns with<br/>scoped context" --> AGV
    CMD -- "spawns with<br/>scoped context" --> AGE
    CMD -- "spawns at<br/>mission end" --> AGRP

    AGR -- "writes Domain<br/>Host·Port·Service" --> ASG
    AGA -- "writes Technology<br/>Endpoint·Vulnerability" --> ASG
    AGI -- "enriches Vulnerability<br/>nodes (CVE+PoC)" --> ASG
    AGV -- "writes Evidence<br/>advances ChainStep" --> ASG
    AGE -- "writes Evidence<br/>screenshots" --> ASG

    AGR --> TAL
    AGA --> TAL
    AGV --> TAL

    %% Styling
    classDef tier1 fill:#061020,stroke:#00D4FF,color:#fff
    classDef tier2asg fill:#04180C,stroke:#7FFF00,color:#fff
    classDef tier2apg fill:#1E1004,stroke:#FFC107,color:#fff
    classDef tier3 fill:#0A081C,stroke:#9C27B0,color:#fff
    classDef gate_low fill:#0A1A08,stroke:#7FFF00,color:#7FFF00
    classDef gate_med fill:#1A1000,stroke:#FFC107,color:#FFC107
    classDef gate_hi fill:#1A0606,stroke:#FF5252,color:#FF5252
    classDef sep fill:#081018,stroke:#444,color:#888

    class T1 tier1
    class ASG tier2asg
    class APG tier2apg
    class T3 tier3
    class RG1 gate_low
    class RG2 gate_med
    class RG3 gate_hi
    class SEP sep
```

### Reading Key

| Colour | Meaning |
|--------|---------|
| 🟢 Cyan border | Commander — orchestration layer |
| 🟢 Lime/Green border | ASG — discovery facts |
| 🟡 Gold border | APG — attack reasoning |
| 🟣 Purple border | Agent tier + tool adapter |
| Solid arrow | Data flow / write |
| Dashed arrow | Read / feedback |

### Three Things to Notice

1. **The Commander never touches tools.** Every arrow from the Commander goes to agents — never to the Tool Adapter Layer directly.
2. **Only the Commander writes to the APG.** All six specialist agents write only to the ASG (or read from it). The APG is exclusively the Commander's domain.
3. **All tool calls go through the Tool Adapter Layer.** There is no path from an agent directly to a tool. The Risk Gate sits in that layer.

---

*Module 03, Figure 2 below: Agent Spawn Lifecycle*

---

## Module 03, Figure 2 — Agent Spawn Lifecycle: Born Fresh, Die Clean

This is the most important architectural insight that separates CMatrix from other multi-agent systems. Every agent is born fresh, does exactly one job with a scoped context, and vanishes — leaving only structured graph state behind.

### Figure 2A — The Spawn Lifecycle (single agent)

```mermaid
sequenceDiagram
    participant CMD as 👑 Commander
    participant GATE as 🚦 Risk Gate
    participant TAL as ⚙️ Tool Adapter
    participant AG as 🤖 Specialist Agent
    participant ASG as 🟢 ASG
    participant APG as 🟡 APG

    Note over CMD: Reads full ASG + APG state
    Note over CMD: Decides: spawn Analysis Agent<br/>for WordPress 5.9.3 host

    CMD->>AG: spawn(ASG slice + task spec + authorized toolset)
    Note over AG: Fresh context — no prior history<br/>Knows only: its ASG slice + task

    AG->>GATE: tool_call(WhatWeb, target=shopvault.io)
    GATE-->>AG: LOW risk → execute immediately

    AG->>TAL: execute(WhatWeb)
    TAL-->>AG: structured findings<br/>{technology: WordPress, version: 5.9.3}
    Note over AG: Raw output discarded<br/>Agent sees only compact summary

    AG->>GATE: tool_call(Gobuster, target=shopvault.io)
    GATE->>CMD: MEDIUM risk → LLM Classifier check
    CMD-->>GATE: EXECUTE approved
    GATE->>TAL: execute(Gobuster)
    TAL-->>AG: structured findings<br/>{endpoint: /backup/db_export.sql, status: 200}

    AG->>GATE: tool_call(SQLMap, target=shopvault.io)
    GATE->>CMD: HIGH risk → Commander Mailbox
    Note over CMD: Reviews: target in scope?<br/>Chain context valid? Params safe?
    CMD-->>AG: APPROVED (or REJECTED/MODIFIED)

    AG->>ASG: write delta<br/>[Technology: WP 5.9.3]<br/>[Endpoint: /backup/db_export.sql]<br/>[Vulnerability: CVE-2022-21661]

    AG->>CMD: return structured ASG delta
    Note over AG: Working context DISCARDED<br/>All raw tool output gone<br/>All intermediate reasoning gone

    CMD->>APG: read new Vulnerability nodes
    Note over CMD: Reasons: CVE-2022-21661 → seed Chain-01
    CMD->>APG: write AttackChain(Chain-01, risk=8.8, HYPOTHESIZED)
```

---

### Figure 2B — What Each Agent Receives at Spawn (Scoped Context)

```mermaid
flowchart LR
    CMD["👑 COMMANDER<br/>Decides next action"]

    subgraph SPAWN["Agent Spawn Package"]
        direction TB
        S1["📊 ASG SLICE<br/>Only nodes relevant to this task<br/>Not the full graph"]
        S2["🔗 APG SLICE<br/>Relevant AttackChains only<br/>(if this is a Validation task)"]
        S3["🔧 TOOL SET<br/>Authorized tools only<br/>No others available"]
        S4["📋 TASK SPEC<br/>Commander's current plan item<br/>Exact objective for this spawn"]
        S5["📚 KNOWLEDGE DOCS<br/>(Validation Agent + Analysis Agent)<br/>Vulnerability-class expert docs<br/>injected at spawn time"]
    end

    subgraph AGENT["🤖 Isolated Agent Context<br/>(fresh per task — no prior history)"]
        WORK["Works autonomously<br/>within bounded context<br/>All tool calls → Risk Gate"]
    end

    subgraph RETURN["Agent Returns"]
        R1["✅ Structured ASG Delta<br/>New nodes + edges only"]
        R2["🗑️ Working context DISCARDED<br/>Raw tool output → gone<br/>Conversation history → gone<br/>Intermediate reasoning → gone"]
    end

    CMD -->|"spawn with<br/>scoped package"| SPAWN
    SPAWN --> AGENT
    AGENT --> RETURN
    RETURN -->|"delta written<br/>to ASG"| ASG_ICON["🟢 ASG"]
    RETURN -->|"Commander reads<br/>new nodes"| CMD

    style CMD fill:#04162E,stroke:#00D4FF,color:#00D4FF
    style SPAWN fill:#0A0C1E,stroke:#9C27B0,color:#9C27B0
    style AGENT fill:#0A0C1E,stroke:#9C27B0,color:#fff
    style RETURN fill:#041808,stroke:#7FFF00,color:#7FFF00
    style ASG_ICON fill:#062210,stroke:#7FFF00,color:#7FFF00
    style S1 fill:#04180A,stroke:#7FFF00,color:#7FFF00
    style S2 fill:#1A1002,stroke:#FFC107,color:#FFC107
    style S3 fill:#180404,stroke:#FF5252,color:#FF5252
    style S4 fill:#041420,stroke:#00D4FF,color:#00D4FF
    style S5 fill:#100820,stroke:#9C27B0,color:#CE93D8
```

---

### Figure 2C — Why Context Isolation Produces Three Critical Properties

```mermaid
flowchart TD
    CI["🔒 CONTEXT ISOLATION<br/>Every agent spawns fresh<br/>Every agent dies clean"]

    P1["✅ Property 1<br/>COMMANDER STAYS CLEAN<br/>─────────────────────<br/>Commander only ever sees<br/>ASG/APG state — never<br/>thousands of lines of<br/>raw tool output.<br/>Its reasoning context stays<br/>surgically focused."]

    P2["✅ Property 2<br/>AGENTS CANNOT CONTAMINATE<br/>─────────────────────────<br/>Agent A's verbose history<br/>never appears in Agent B's<br/>context. Knowledge passes<br/>only through the ASG.<br/>No shared memory. No<br/>accidental cross-pollution."]

    P3["✅ Property 3<br/>REJECTIONS DON'T BIAS PLANNING<br/>────────────────────────────────<br/>When Commander rejects a<br/>High-risk tool call, that<br/>rejection never appears in<br/>the Commander's own context.<br/>Refusals don't accumulate<br/>and skew future decisions."]

    RESULT["🎯 RESULT<br/>Long missions with many agents<br/>produce the same quality of<br/>reasoning as single-agent tasks.<br/>Context quality does not degrade<br/>with mission complexity."]

    CI --> P1
    CI --> P2
    CI --> P3
    P1 --> RESULT
    P2 --> RESULT
    P3 --> RESULT

    style CI fill:#04162E,stroke:#00D4FF,color:#00D4FF
    style P1 fill:#041A08,stroke:#7FFF00,color:#7FFF00
    style P2 fill:#10081E,stroke:#9C27B0,color:#CE93D8
    style P3 fill:#1A0606,stroke:#FF5252,color:#FF5252
    style RESULT fill:#1A1002,stroke:#FFC107,color:#FFC107
```

### Reading Key for Figure 2

| Concept | What to Notice |
|---------|---------------|
| Spawn package | 5 components — each scoped, none is the full system state |
| Tool Set boundary | Agent can ONLY use tools it was authorized for at spawn |
| Knowledge Docs | Validation Agent + Analysis Agent receive these — matched to their vulnerability class |
| Return = delta only | The ASG grows by addition — agents don't rewrite existing nodes |
| Context discarded | The working session is gone — the ASG persists forever |

---

*Module 04, Figure 1 below: Tool Risk Gate Flow*

---

## Module 04, Figure 1 — Tool Risk Gate: Every Tool Call's Journey

No tool in CMatrix executes without passing through this gate. This diagram shows the complete decision path — from an agent requesting a tool call, through all three risk tiers, to either execution or rejection.

### Figure 1A — The Full Risk Gate Decision Tree

```mermaid
flowchart TD
    START["🤖 Agent requests tool call<br/>───────────────────────────<br/>Tool: Gobuster<br/>Target: shopvault.io<br/>Params: -w big.txt -x php,sql"]

    HOOK1["🪝 PreToolUse Hook fires<br/>───────────────────────<br/>External observers notified.<br/>Hook returns: CONTINUE / BLOCK / MODIFY"]

    HOOK1_CHECK{Hook returns?}
    HOOK_BLOCK["❌ BLOCKED<br/>Action cancelled.<br/>Reason logged."]
    HOOK_MODIFY["🔄 MODIFIED<br/>Payload updated.<br/>Proceeds with<br/>modified params."]

    SCOPE["🔍 Scope Check<br/>──────────────────<br/>Is target in declared scope?<br/>Is this tool authorized<br/>for this agent type?"]

    SCOPE_FAIL["❌ OUT OF SCOPE<br/>Tool call rejected.<br/>Agent notified.<br/>No execution."]

    CLASSIFY["🎯 Risk Classification<br/>──────────────────────<br/>Which tier does this call belong to?"]

    LOW{"🟢 LOW RISK?<br/>Passive tools:<br/>Amass · httpx<br/>WhatWeb"}
    MED{"🟡 MEDIUM RISK?<br/>Active tools:<br/>Nmap · Gobuster · ffuf<br/>Nuclei · OWASP ZAP"}
    HIGH{"🔴 HIGH RISK?<br/>Exploitation tools:<br/>SQLMap · Metasploit"}

    EXEC_LOW["✅ Execute immediately<br/>No further approval needed"]

    CLASSIFIER["🧠 LLM Permission Classifier<br/>────────────────────────────<br/>Fast filter pass:<br/>  → Clearly safe? → EXECUTE<br/>  → Clearly risky? → ESCALATE<br/><br/>Chain-of-thought pass (ambiguous):<br/>  Axis 1: Scope alignment<br/>  Axis 2: Chain intent<br/>  Axis 3: Parameter safety<br/>  → Checks for prompt injection"]

    CLF_RESULT{Classifier verdict?}
    CLF_EXEC["✅ EXECUTE<br/>Proceeds to<br/>Tool Adapter"]
    CLF_ESC["⬆️ ESCALATE<br/>Routed to<br/>Commander Mailbox"]

    MAILBOX["📬 Commander Mailbox<br/>──────────────────────<br/>Approval request queued:<br/>  • Tool + module<br/>  • Target ASG node<br/>  • Chain context<br/>  • Rationale<br/><br/>(Human inserted here<br/>in supervised mode)"]

    CMD_REVIEW{Commander decides?}
    CMD_APPROVE["✅ APPROVED<br/>Proceeds to<br/>Tool Adapter"]
    CMD_REJECT["❌ REJECTED<br/>Cancelled.<br/>Reason annotated<br/>to APG chain."]
    CMD_MODIFY["🔄 MODIFIED<br/>Commander adjusts<br/>params, then approves"]

    ADAPTER["⚙️ Tool Adapter executes<br/>────────────────────────<br/>1. Translate request → CLI command<br/>2. Run tool<br/>3. Parse raw output → structured JSON<br/>4. Discard raw output"]

    HOOK2["🪝 PostToolUse Hook fires<br/>─────────────────────────<br/>Structured findings available.<br/>Hook can: log · alert · validate · block write"]

    ASG_WRITE["🟢 Structured findings<br/>written to ASG as<br/>nodes + edges"]

    AG_SUMMARY["🤖 Agent receives<br/>compact summary only<br/>(NOT raw output)"]

    START --> HOOK1
    HOOK1 --> HOOK1_CHECK
    HOOK1_CHECK -->|BLOCK| HOOK_BLOCK
    HOOK1_CHECK -->|MODIFY| HOOK_MODIFY
    HOOK1_CHECK -->|CONTINUE| SCOPE
    HOOK_MODIFY --> SCOPE

    SCOPE -->|fail| SCOPE_FAIL
    SCOPE -->|pass| CLASSIFY

    CLASSIFY --> LOW
    CLASSIFY --> MED
    CLASSIFY --> HIGH

    LOW -->|yes| EXEC_LOW
    MED -->|yes| CLASSIFIER
    HIGH -->|yes| MAILBOX

    CLASSIFIER --> CLF_RESULT
    CLF_RESULT -->|EXECUTE| CLF_EXEC
    CLF_RESULT -->|ESCALATE| MAILBOX

    MAILBOX --> CMD_REVIEW
    CMD_REVIEW -->|APPROVE| CMD_APPROVE
    CMD_REVIEW -->|REJECT| CMD_REJECT
    CMD_REVIEW -->|MODIFY| CMD_MODIFY

    EXEC_LOW --> ADAPTER
    CLF_EXEC --> ADAPTER
    CMD_APPROVE --> ADAPTER
    CMD_MODIFY --> ADAPTER

    ADAPTER --> HOOK2
    HOOK2 --> ASG_WRITE
    HOOK2 --> AG_SUMMARY

    style START fill:#04162E,stroke:#00D4FF,color:#fff
    style HOOK1 fill:#0C0820,stroke:#9C27B0,color:#CE93D8
    style HOOK2 fill:#0C0820,stroke:#9C27B0,color:#CE93D8
    style HOOK_BLOCK fill:#1A0606,stroke:#FF5252,color:#FF5252
    style HOOK_MODIFY fill:#1A1002,stroke:#FFC107,color:#FFC107
    style SCOPE fill:#0A0C1E,stroke:#888,color:#aaa
    style SCOPE_FAIL fill:#1A0606,stroke:#FF5252,color:#FF5252
    style CLASSIFY fill:#0A0C1E,stroke:#888,color:#aaa
    style LOW fill:#041A08,stroke:#7FFF00,color:#7FFF00
    style MED fill:#1A1002,stroke:#FFC107,color:#FFC107
    style HIGH fill:#1A0606,stroke:#FF5252,color:#FF5252
    style EXEC_LOW fill:#041A08,stroke:#7FFF00,color:#7FFF00
    style CLASSIFIER fill:#04162E,stroke:#00D4FF,color:#00D4FF
    style CLF_EXEC fill:#041A08,stroke:#7FFF00,color:#7FFF00
    style CLF_ESC fill:#1A1002,stroke:#FFC107,color:#FFC107
    style MAILBOX fill:#04162E,stroke:#00D4FF,color:#00D4FF
    style CMD_APPROVE fill:#041A08,stroke:#7FFF00,color:#7FFF00
    style CMD_REJECT fill:#1A0606,stroke:#FF5252,color:#FF5252
    style CMD_MODIFY fill:#1A1002,stroke:#FFC107,color:#FFC107
    style ADAPTER fill:#0A0C1E,stroke:#9C27B0,color:#CE93D8
    style ASG_WRITE fill:#062210,stroke:#7FFF00,color:#7FFF00
    style AG_SUMMARY fill:#04162E,stroke:#00D4FF,color:#00D4FF
```

---

### Figure 1B — What the LLM Permission Classifier Actually Checks

```mermaid
flowchart LR
    INPUT["🟡 Medium-Risk<br/>Tool Call<br/>─────────────<br/>Tool: Gobuster<br/>Target: staging.shopvault.io<br/>Params: -w big.txt"]

    subgraph FAST["Fast Filter (instant)"]
        F1{"Obviously safe?<br/>(passive, in-scope,<br/>standard params)"}
        F2{"Obviously risky?<br/>(out-of-scope target,<br/>suspicious params)"}
    end

    subgraph COT["Chain-of-Thought Pass (ambiguous cases)"]
        AX1["Axis 1: SCOPE ALIGNMENT<br/>──────────────────────<br/>Is staging.shopvault.io<br/>in the declared scope?<br/>Was it explicitly excluded?"]
        AX2["Axis 2: CHAIN INTENT<br/>───────────────────<br/>Does Gobuster on this host<br/>make sense for the current<br/>APG AttackChain being pursued?"]
        AX3["Axis 3: PARAMETER SAFETY<br/>────────────────────────<br/>Do params match current<br/>ASG state? Or do they look<br/>like they were injected from<br/>crawled web content?<br/>(Prompt injection check)"]
    end

    VERDICT{"Final verdict"}
    EXEC["✅ EXECUTE"]
    ESC["⬆️ ESCALATE<br/>to Commander<br/>Mailbox"]

    INPUT --> FAST
    F1 -->|yes| EXEC
    F2 -->|yes| ESC
    F1 -->|no| COT
    F2 -->|no| COT
    AX1 --> VERDICT
    AX2 --> VERDICT
    AX3 --> VERDICT
    VERDICT -->|all clear| EXEC
    VERDICT -->|concern| ESC

    style INPUT fill:#1A1002,stroke:#FFC107,color:#FFC107
    style FAST fill:#04100C,stroke:#7FFF00,color:#7FFF00
    style COT fill:#04162E,stroke:#00D4FF,color:#00D4FF
    style AX1 fill:#041420,stroke:#00D4FF,color:#00D4FF
    style AX2 fill:#041420,stroke:#00D4FF,color:#00D4FF
    style AX3 fill:#041420,stroke:#00D4FF,color:#00D4FF
    style EXEC fill:#041A08,stroke:#7FFF00,color:#7FFF00
    style ESC fill:#1A1002,stroke:#FFC107,color:#FFC107
```

---

### Figure 1C — The 6 Lifecycle Hooks: Where Operators Can Intervene

```mermaid
timeline
    title CMatrix Agent Lifecycle Hook Points
    section Before Tool
        PreToolUse : Fires before Risk Gate
                   : CONTINUE / BLOCK / MODIFY
                   : Use for: extra scope checks
    section After Tool
        PostToolUse : Fires after ASG write
                    : Log to SIEM · Alert SOC
                    : Use for: audit trails
    section Agent Events
        PreAgentSpawn : Fires before Commander spawns agent
                      : Override context · extra auth
        PostAgentReturn : Fires after agent returns delta
                        : Validate schema · notify systems
    section APG Events
        PreAPGUpdate : Fires before new AttackChain written
                     : External approval gate · compliance
    section Mission Events
        PostMissionTerminate : Fires at dual-graph termination
                             : Push to vuln management platform
                             : Trigger report delivery
```

### Risk Gate Summary Table

| Tool | Tier | Gate | Rationale |
|------|------|------|-----------|
| Amass | 🟢 LOW | Scope check only | Passive DNS — no target traffic |
| httpx | 🟢 LOW | Scope check only | Read-only HTTP probing |
| WhatWeb | 🟢 LOW | Scope check only | Read-only fingerprinting |
| Nmap | 🟡 MED | LLM Classifier | Active scan — may trigger IDS |
| Gobuster | 🟡 MED | LLM Classifier | Active — unusual traffic patterns |
| ffuf | 🟡 MED | LLM Classifier | Active fuzzing — parameter injection risk |
| Nuclei | 🟡 MED | LLM Classifier | Template matching — active probes |
| OWASP ZAP | 🟡 MED | LLM Classifier | Active web scan — touches all endpoints |
| EyeWitness | 🟢 LOW | Scope check only | Screenshot only — no exploitation |
| SQLMap | 🔴 HIGH | Commander Mailbox | Destructive — extracts data |
| Metasploit | 🔴 HIGH | Commander Mailbox | Irreversible — achieves code execution |

---

*Module 06, Figure 1 below: Autonomous Planning Cycle Loop*

---

## Module 06, Figure 1 — The Autonomous Planning Cycle

The Commander runs this loop continuously — from mission start until the dual-graph termination condition fires. Every iteration is grounded in graph state. Every decision is traceable to a specific graph event.

### Figure 1A — The Core Planning Loop

```mermaid
flowchart TD
    START(["🚀 MISSION START<br/>Operator provides: root domain + scope + mode<br/>ASG seeded: [Domain: shopvault.io]<br/>APG: empty"])

    OBS_ASG["👁️ OBSERVE ASG<br/>─────────────────────────────────<br/>• Which nodes are unexplored?<br/>• Which Vulnerability nodes are new?<br/>• Which Technology nodes need Research?"]

    OBS_APG["👁️ OBSERVE APG<br/>─────────────────────────────────<br/>• Which chains are HYPOTHESIZED?<br/>• Which are PARTIALLY_VALIDATED?<br/>• Which just went VALIDATED or RULED_OUT?"]

    REASON["🧠 REASON<br/>─────────────────────────────────<br/>Given ASG + APG state:<br/>What is the single best<br/>next action right now?"]

    DECIDE{What does<br/>reasoning<br/>produce?}

    EXPLORE["🗺️ EXPLORE<br/>ASG gap detected<br/>─────────────────<br/>Spawn discovery agent:<br/>• Recon → unscanned hosts<br/>• Analysis → untested tech<br/>• Research → unenriched CVE"]

    VALIDATE["🎯 VALIDATE<br/>High-priority chain waiting<br/>─────────────────────────<br/>Spawn Validation Agent<br/>for highest-priority<br/>HYPOTHESIZED chain"]

    BOTH["↕️ PARALLEL<br/>Both ASG gaps AND<br/>unvalidated chains exist<br/>─────────────────────<br/>Commander weighs priority:<br/>High-risk chain beats<br/>low-value exploration"]

    AGENT_RUNS["⚡ AGENT EXECUTES<br/>(tools → Risk Gate → ASG writes)"]

    UPDATE_ASG["📥 UPDATE ASG<br/>New nodes + edges written<br/>by returning agent"]

    UPDATE_APG["📥 UPDATE APG (Commander)<br/>─────────────────────────<br/>New Vuln nodes → seed chains?<br/>ChainStep advanced → update status?<br/>RULED_OUT chain → re-prioritize?"]

    CYCLE_GUARD{Cycle Guard:<br/>Repeated<br/>identical calls?}
    REFLECTOR["🪞 REFLECTOR<br/>Repeated failures?<br/>→ Issue corrective guidance<br/>→ Agent adapts approach"]
    FORCE_REPLAN["🔄 FORCE RE-PLAN<br/>Stop current approach<br/>Commander reassigns"]

    TERM{Termination<br/>condition met?}
    TERM_CHECK["✅ ASG exhausted?<br/>(no unexplored nodes)<br/>AND<br/>✅ APG resolved?<br/>(all chains VALIDATED<br/>or RULED_OUT)"]

    REPORT["📝 Spawn Report Agent<br/>Reads full ASG + APG<br/>Generates professional<br/>penetration test report"]

    DONE(["🏁 MISSION COMPLETE"])

    START --> OBS_ASG
    OBS_ASG --> OBS_APG
    OBS_APG --> REASON
    REASON --> DECIDE
    DECIDE -->|"ASG gaps only"| EXPLORE
    DECIDE -->|"APG chains waiting"| VALIDATE
    DECIDE -->|"Both present"| BOTH
    EXPLORE --> AGENT_RUNS
    VALIDATE --> AGENT_RUNS
    BOTH --> AGENT_RUNS
    AGENT_RUNS --> CYCLE_GUARD
    CYCLE_GUARD -->|"yes — fixation<br/>detected"| FORCE_REPLAN
    CYCLE_GUARD -->|"repeated different<br/>failures"| REFLECTOR
    REFLECTOR --> AGENT_RUNS
    FORCE_REPLAN --> OBS_ASG
    CYCLE_GUARD -->|"no — normal"| UPDATE_ASG
    UPDATE_ASG --> UPDATE_APG
    UPDATE_APG --> TERM
    TERM --> TERM_CHECK
    TERM_CHECK -->|"no — continue"| OBS_ASG
    TERM_CHECK -->|"yes — both\nconditions true"| REPORT
    REPORT --> DONE

    style START fill:#041A08,stroke:#7FFF00,color:#7FFF00
    style OBS_ASG fill:#062210,stroke:#7FFF00,color:#7FFF00
    style OBS_APG fill:#1E1004,stroke:#FFC107,color:#FFC107
    style REASON fill:#04162E,stroke:#00D4FF,color:#00D4FF
    style DECIDE fill:#04162E,stroke:#00D4FF,color:#fff
    style EXPLORE fill:#062210,stroke:#7FFF00,color:#7FFF00
    style VALIDATE fill:#1A0606,stroke:#FF5252,color:#FF5252
    style BOTH fill:#1A1002,stroke:#FFC107,color:#FFC107
    style AGENT_RUNS fill:#0A0C1E,stroke:#9C27B0,color:#CE93D8
    style UPDATE_ASG fill:#062210,stroke:#7FFF00,color:#7FFF00
    style UPDATE_APG fill:#1E1004,stroke:#FFC107,color:#FFC107
    style CYCLE_GUARD fill:#1A0606,stroke:#FF5252,color:#fff
    style REFLECTOR fill:#1A1002,stroke:#FFC107,color:#FFC107
    style FORCE_REPLAN fill:#1A0606,stroke:#FF5252,color:#FF5252
    style TERM fill:#04162E,stroke:#00D4FF,color:#fff
    style TERM_CHECK fill:#04162E,stroke:#00D4FF,color:#00D4FF
    style REPORT fill:#10081E,stroke:#9C27B0,color:#CE93D8
    style DONE fill:#041A08,stroke:#7FFF00,color:#7FFF00
```

---

### Figure 1B — What Triggers a Re-Plan (Graph-Grounded Events)

```mermaid
flowchart LR
    subgraph ASG_EVENTS["ASG Trigger Events"]
        E1["🆕 New Vulnerability node written<br/>→ Should this seed a new APG chain?"]
        E2["🆕 New Technology node written<br/>→ Spawn Research Agent for CVE lookup"]
        E3["🆕 New Endpoint node written<br/>→ Analysis Agent needs to probe it"]
    end

    subgraph APG_EVENTS["APG Trigger Events"]
        E4["📈 Chain → PARTIALLY_VALIDATED<br/>→ Re-rank all chain priorities"]
        E5["✅ Chain → VALIDATED<br/>→ Mark complete, pursue next"]
        E6["❌ Chain → RULED_OUT<br/>→ Remove from queue, re-prioritize"]
    end

    subgraph GUARD_EVENTS["Cycle Guard Events"]
        E7["🔁 Same tool call repeated ×3<br/>→ Force re-plan immediately"]
        E8["💥 Repeated different failures<br/>→ Reflector issues guidance"]
    end

    CMD["👑 Commander<br/>Re-plans on<br/>any of these<br/>events"]

    E1 --> CMD
    E2 --> CMD
    E3 --> CMD
    E4 --> CMD
    E5 --> CMD
    E6 --> CMD
    E7 --> CMD
    E8 --> CMD

    style ASG_EVENTS fill:#062210,stroke:#7FFF00,color:#7FFF00
    style APG_EVENTS fill:#1E1004,stroke:#FFC107,color:#FFC107
    style GUARD_EVENTS fill:#1A0606,stroke:#FF5252,color:#FF5252
    style CMD fill:#04162E,stroke:#00D4FF,color:#00D4FF
```

---

### Figure 1C — The Dual Termination Condition (Why Both Must Be True)

```mermaid
flowchart TD
    Q["❓ Is the mission complete?"]

    C1{"ASG exhausted?<br/>────────────────<br/>Every Domain, Host, Port,<br/>Service, Technology,<br/>Endpoint, Parameter node<br/>has been investigated<br/>by the appropriate agent"}

    C2{"APG resolved?<br/>──────────────────<br/>Every AttackChain is in<br/>a terminal state:<br/>VALIDATED or RULED_OUT<br/><br/>No chain is still<br/>HYPOTHESIZED or<br/>PARTIALLY_VALIDATED"}

    ONLY1["❌ NOT DONE<br/>ASG explored but<br/>chains still open.<br/>Attack reasoning<br/>is unfinished."]

    ONLY2["❌ NOT DONE<br/>All chains resolved<br/>but new ASG nodes<br/>just written.<br/>Might seed new chains."]

    NEITHER["❌ NOT DONE<br/>Both incomplete.<br/>Continue mission."]

    BOTH_TRUE["✅ MISSION COMPLETE<br/>ASG is fully mapped.<br/>All attack opportunities<br/>proven or disproven.<br/>Report Agent spawned."]

    CONTRAST["⚠️ Why existing systems fail:<br/>─────────────────────────────<br/>Timer-based: stops mid-chain<br/>Task-queue-based: can't express APG resolution<br/>Only CMatrix defines both<br/>conditions simultaneously"]

    Q --> C1
    Q --> C2
    C1 -->|"yes, C2 no"| ONLY1
    C2 -->|"yes, C1 no"| ONLY2
    C1 & C2 -->|"neither"| NEITHER
    C1 & C2 -->|"BOTH true"| BOTH_TRUE
    BOTH_TRUE --> CONTRAST

    style Q fill:#04162E,stroke:#00D4FF,color:#00D4FF
    style C1 fill:#062210,stroke:#7FFF00,color:#7FFF00
    style C2 fill:#1E1004,stroke:#FFC107,color:#FFC107
    style ONLY1 fill:#1A0606,stroke:#FF5252,color:#FF5252
    style ONLY2 fill:#1A0606,stroke:#FF5252,color:#FF5252
    style NEITHER fill:#1A0606,stroke:#FF5252,color:#FF5252
    style BOTH_TRUE fill:#041A08,stroke:#7FFF00,color:#7FFF00
    style CONTRAST fill:#10081E,stroke:#9C27B0,color:#CE93D8
```

---

### Figure 1D — Context Compaction: How Long Missions Stay Sharp

```mermaid
flowchart LR
    subgraph NORMAL["Normal Operation"]
        T1["Tool runs<br/>→ MicroCompact<br/>Raw output discarded<br/>Agent sees 3-line summary"]
    end

    subgraph AUTO["AutoCompact @ 60% context"]
        T2["Older conversation turns<br/>summarized by scoped LLM call<br/>Summary replaces raw turns<br/>Agent continues uninterrupted"]
    end

    subgraph FULL["FullCompact @ 85% context"]
        T3["Entire history replaced<br/>from scratch using:<br/>• Current ASG snapshot<br/>• Current APG priorities<br/>• Last N tool results<br/><br/>ZERO intelligence lost<br/>(everything important<br/>is in the graph)"]
    end

    T1 -->|context grows| AUTO
    AUTO -->|context grows| FULL
    FULL -->|fresh context| T1

    ASG_KEY["🟢 ASG is the key<br/>────────────────<br/>Conversation history<br/>is expendable because<br/>all discoveries live<br/>in the graph permanently.<br/>FullCompact = safe."]

    FULL --> ASG_KEY

    style NORMAL fill:#062210,stroke:#7FFF00,color:#7FFF00
    style AUTO fill:#1A1002,stroke:#FFC107,color:#FFC107
    style FULL fill:#04162E,stroke:#00D4FF,color:#00D4FF
    style ASG_KEY fill:#041A08,stroke:#7FFF00,color:#7FFF00
```

### Planning Cycle — Key Insights

| Question | Answer |
|----------|--------|
| What drives re-planning? | Explicit graph events — never timers or empty queues |
| How does the Commander know what to do next? | Reads ASG (unexplored nodes) + APG (chain priorities) |
| What prevents infinite loops? | Cycle Guard (identical calls) + Reflector (repeated failures) |
| When does the mission end? | ASG exhausted AND all APG chains terminal — both simultaneously |
| How does context stay manageable? | 3-layer compaction — history is expendable, graph is permanent |

---

*Module 07, Figure 1 below: shopvault.io Full Mission Walkthrough*

---

## Module 07, Figure 1 — Real-World Scenario: shopvault.io End-to-End

This is the complete picture. One real mission. Zero manual commands. Watch every tool, every graph write, every Commander decision, from the moment the operator presses start to the final professional report.

**Target:** `shopvault.io` — an e-commerce platform  
**Mode:** Black-Box (zero prior knowledge)  
**Scope:** All subdomains, web apps, REST APIs  
**Operator action:** Provide domain + scope → press start

---

### Figure 1A — Mission Timeline: Phase by Phase

```mermaid
flowchart TD
    OP(["🧑 OPERATOR<br/>Target: shopvault.io<br/>Scope: all subdomains<br/>Mode: Black-Box<br/>→ PRESS START"])

    subgraph P1["🟢 PHASE 1 — RECONNAISSANCE<br/>Recon Agent spawned"]
        A1["Tool: Amass<br/>────────────────────────<br/>14 subdomains discovered:<br/>api · admin · staging<br/>pay · mail · static · ..."]
        A2["Tool: httpx<br/>────────────────────────<br/>11 live hosts confirmed<br/>staging → unexpected 200 OK<br/>pay → TLS certificate EXPIRED"]
        A3["Tool: Nmap<br/>────────────────────────<br/>28 open ports mapped<br/>Ports: 80, 443, 8080, 8443, 22<br/>Services: Nginx 1.18 · OpenSSH 8.9<br/>Unencrypted HTTP on port 8080"]
        D1["📥 ASG DELTA<br/>37 new nodes written:<br/>14 Domain · 11 Host<br/>28 Port · 15 Service"]
    end

    subgraph P2["🔵 PHASE 2 — ANALYSIS + INTELLIGENCE<br/>Analysis Agent + Research Agent spawned"]
        B1["Tool: WhatWeb<br/>────────────────────────<br/>WordPress 5.9.3 on shopvault.io<br/>WooCommerce 6.1 detected<br/>Django 4.1.2 on api.shopvault.io<br/>→ Commander spawns Research Agent"]
        B2["Research Agent: NVD + Exploit-DB<br/>────────────────────────────────<br/>CVE-2022-21661 found (CVSS 8.8)<br/>PoC on Exploit-DB ✓<br/>Metasploit module available ✓"]
        B3["Tool: Gobuster<br/>────────────────────────<br/>/backup/db_export_2023.sql → 200!<br/>/wp-admin/login → 200<br/>/wp-admin/users → 403<br/>/api/v1/internal/users → 200"]
        B4["Tool: ffuf<br/>────────────────────────<br/>IDOR: user_id param unsanitised<br/>/api/v2 routes discovered<br/>Virtual host: internal.shopvault.io"]
        B5["Tool: Nuclei<br/>────────────────────────<br/>CVE-2022-21661 template → MATCH<br/>Exposed phpinfo.php on staging<br/>Default creds check: admin/admin → fail"]
        B6["Tool: OWASP ZAP<br/>────────────────────────<br/>XSS on /search?q= (reflected)<br/>SQL error on staging login form<br/>Missing security headers on API"]
        D2["📥 ASG DELTA: 61 new nodes<br/>Technology(3) · Endpoint(19)<br/>Parameter(8) · Vulnerability(9)<br/><br/>📥 APG DELTA: 3 chains seeded<br/>Chain-01: CVE-2022-21661 SQLi→RCE (8.8)<br/>Chain-02: IDOR orders API (7.5)<br/>Chain-03: Staging login blind SQLi (8.1)"]
    end

    subgraph P3["🔴 PHASE 3 — VALIDATION + EVIDENCE<br/>Validation Agent + Evidence Agent spawned"]
        C1["Chain-01 (highest priority: 8.8)<br/>────────────────────────────────<br/>Step 1: SQLMap on WP_Query<br/>→ SQLi confirmed ✅<br/>→ Evidence: sqli-extraction.txt"]
        C2["Step 2: SQLMap --dump users table<br/>────────────────────────────────<br/>→ Admin hash extracted ✅<br/>→ Offline crack: admin:Summer2023!<br/>→ Evidence: user-table-dump.png"]
        C3["Step 3: Metasploit wp_admin_shell_upload<br/>────────────────────────────────<br/>⚠️ HIGH RISK → Commander Mailbox<br/>→ Commander APPROVES<br/>→ Web shell deployed ✅<br/>→ RCE confirmed!<br/>→ risk_score escalated: 8.8 → 9.1<br/>→ Evidence: webshell-rce.png"]
        C4["Chain-03 (next by risk: 8.1)<br/>────────────────────────────────<br/>SQLMap on staging.shopvault.io/login<br/>→ Blind SQLi confirmed ✅<br/>→ Staging DB credentials extracted ✅<br/>→ Commander flags: staging creds overlap production<br/>→ Additional Impact node: credential reuse risk<br/>→ Evidence: staging-db-dump.png"]
        C5["Chain-02 (risk: 7.5)<br/>────────────────────────────────<br/>SQLMap on user_id parameter<br/>→ IDOR confirmed ✅<br/>→ Any customer's orders accessible without auth<br/>→ Evidence: idor-orders-dump.png"]
        D3["📥 APG DELTA<br/>Chain-01: VALIDATED (9.1)<br/>Chain-03: VALIDATED (8.1)<br/>Chain-02: VALIDATED (7.5)<br/><br/>📥 ASG DELTA<br/>Evidence nodes + edges added"]
    end

    subgraph P4["🟣 PHASE 4 — ASG EXHAUSTION + CHAIN-04 + REPORT"]
        C6["ASG Exhaustion Check<br/>────────────────────────────────<br/>Commander reads ASG: all 11 hosts mapped<br/>→ /backup/db_export_2023.sql still unvalidated<br/>→ Seed Chain-04: Direct DB backup download<br/>→ HTTP GET → 200 OK → VALIDATED immediately<br/>→ Evidence: db-backup-download.png"]
        RPT["📋 PROFESSIONAL PENETRATION TEST REPORT<br/>─────────────────────────────────────────<br/>• Executive Summary<br/>• 4 Validated Attack Chains<br/>• Full attack surface map (14 subdomains · 11 hosts)<br/>• 11 vulnerabilities with CVSS scores<br/>• Remediation guidance ordered by risk_score<br/>• Evidence at every ChainStep<br/>• ZERO manual commands issued"]
    end

    TERM["✅ TERMINATION CONDITION MET<br/>ASG: all 111 nodes explored<br/>APG: all 4 chains VALIDATED<br/>→ Report Agent spawned"]

    OP --> P1
    A1 --> A2 --> A3 --> D1
    D1 --> P2
    B1 --> B2 --> B3 --> B4 --> B5 --> B6 --> D2
    D2 --> P3
    C1 --> C2 --> C3
    C3 --> C4 --> C5 --> D3
    D3 --> TERM
    TERM --> P4
    C6 --> RPT

    style OP fill:#041A08,stroke:#7FFF00,color:#7FFF00
    style P1 fill:#062210,stroke:#7FFF00,color:#7FFF00
    style P2 fill:#04162E,stroke:#00D4FF,color:#00D4FF
    style P3 fill:#1A0606,stroke:#FF5252,color:#FF5252
    style P4 fill:#10081E,stroke:#9C27B0,color:#CE93D8
    style D1 fill:#041A08,stroke:#7FFF00,color:#7FFF00
    style D2 fill:#041A08,stroke:#7FFF00,color:#7FFF00
    style D3 fill:#1E1004,stroke:#FFC107,color:#FFC107
    style TERM fill:#041A08,stroke:#7FFF00,color:#7FFF00
    style C6 fill:#1E1004,stroke:#FFC107,color:#FFC107
    style RPT fill:#10081E,stroke:#9C27B0,color:#CE93D8
```

---

### Figure 1B — The Commander's Decision Log (Key Moments)

```mermaid
timeline
    title Commander Decisions — shopvault.io Mission
    section Mission Start
        Step 1  : Seed: Domain node shopvault.io
                : Action: Spawn Recon Agent
    section After Phase 1
        Step 2  : Trigger: 11 live hosts written to ASG
                : Action: Spawn Analysis Agent (all hosts)
        Step 3  : Trigger: WordPress 5.9.3 Technology node written
                : Action: Spawn Research Agent (CVE lookup)
    section After Research
        Step 4  : Trigger: CVE-2022-21661 Vuln node written (CVSS 8.8, PoC confirmed)
                : Action: Seed Chain-01 in APG — HYPOTHESIZED — priority 1
        Step 5  : Trigger: IDOR Parameter node written (user_id unsanitised)
                : Action: Seed Chain-02 in APG — HYPOTHESIZED — priority 3
        Step 6  : Trigger: SQL error Vuln node on staging login written by ZAP
                : Action: Seed Chain-03 in APG — HYPOTHESIZED — priority 2 (risk 8.1)
    section Phase 4 — ASG Exhaustion
        Step 6b : Trigger: Exposed /backup/db_export_2023.sql Endpoint node
                : Action: Seed Chain-04 in APG — trivially validated via HTTP GET
    section Validation
        Step 7  : Trigger: Chain-01 is highest priority (8.8)
                : Action: Spawn Validation Agent for Chain-01
        Step 8  : Trigger: SQLMap HIGH-risk call arrives at mailbox
                : Decision: APPROVE — target confirmed in scope — chain context valid
        Step 9  : Trigger: Metasploit HIGH-risk call arrives at mailbox
                : Decision: APPROVE — Steps 1+2 already VALIDATED — RCE is the goal
        Step 10 : Trigger: Chain-01 → VALIDATED — risk escalated to 9.1
                : Action: Spawn Validation Agent for Chain-03 (next by risk score 8.1)
        Step 11 : Trigger: Chain-03 → VALIDATED — staging credentials extracted
                : Note: Commander flags credential reuse risk as additional Impact node
        Step 12 : Trigger: Chain-02 next (risk 7.5)
                : Action: Spawn Validation Agent for Chain-02 — VALIDATED
        Step 13 : Trigger: Chain-04 — trivial validation (public HTTP GET)
                : Action: VALIDATED immediately
    section Termination
        Step 14 : Trigger: ASG exhausted (111 nodes) AND APG resolved (4/4 chains VALIDATED)
                : Action: Dual-graph termination condition met — spawn Report Agent
```

---

### Figure 1C — Final Mission Stats

```mermaid
flowchart LR
    subgraph ASG_FINAL["🟢 ASG — Final State"]
        direction TB
        N1["14 Domain nodes"]
        N2["11 Host nodes"]
        N3["28 Port nodes"]
        N4["15 Service nodes"]
        N5["3 Technology nodes"]
        N6["19 Endpoint nodes"]
        N7["8 Parameter nodes"]
        N8["9 Vulnerability nodes"]
        N9["4 Evidence nodes"]
        NT["= 111 total nodes"]
    end

    subgraph APG_FINAL["🟡 APG — Final State"]
        direction TB
        CH1["Chain-01: VALIDATED ✅<br/>risk: 9.1 (escalated after RCE)<br/>WordPress SQLi → Admin auth → RCE"]
        CH2["Chain-02: VALIDATED ✅<br/>risk: 7.5<br/>IDOR → Customer order PII"]
        CH3["Chain-03: VALIDATED ✅<br/>risk: 8.1<br/>Staging blind SQLi → Credential extraction"]
        CH4["Chain-04: VALIDATED ✅<br/>risk: 7.0<br/>Exposed DB backup → Full PII download"]
    end

    subgraph REPORT_FINAL["📝 Report Output"]
        direction TB
        R1["4 validated attack chains<br/>with step-by-step reproduction"]
        R2["Evidence artifacts linked<br/>at every ChainStep"]
        R3["11 vulnerabilities<br/>ordered by risk_score"]
        R4["Remediation guidance<br/>prioritized by business risk"]
        R5["0 manual commands issued<br/>during entire assessment"]
    end

    ASG_FINAL --> REPORT_FINAL
    APG_FINAL --> REPORT_FINAL

    style ASG_FINAL fill:#062210,stroke:#7FFF00,color:#7FFF00
    style APG_FINAL fill:#1E1004,stroke:#FFC107,color:#FFC107
    style REPORT_FINAL fill:#10081E,stroke:#9C27B0,color:#CE93D8
```

---

### Figure 1D — Chain-01 Full Traceability: From CVE to Evidence

This is the most important chain in the mission. Every arrow here is a relationship that exists in the dual graph — followable from the report all the way back to the raw evidence file.

```mermaid
flowchart LR
    CVE["🚨 ASG<br/>Vulnerability node<br/>CVE-2022-21661<br/>CVSS: 8.8<br/>PoC: Exploit-DB ✓"]

    CH["🟡 APG<br/>AttackChain: Chain-01<br/>risk_score: 9.1<br/>status: VALIDATED<br/>starts_at → CVE-2022-21661"]

    S1["🟡 APG<br/>ChainStep 1<br/>SQLMap → WP_Query SQLi<br/>status: VALIDATED"]
    S2["🟡 APG<br/>ChainStep 2<br/>SQLMap dump → hash cracked<br/>status: VALIDATED"]
    S3["🟡 APG<br/>ChainStep 3<br/>Metasploit → Web shell<br/>status: VALIDATED"]
    IMP["🟣 APG<br/>Impact<br/>RCE on shopvault.io<br/>Customer PII accessible"]

    EV1["📎 ASG<br/>Evidence<br/>sqli-extraction.txt"]
    EV2["📎 ASG<br/>Evidence<br/>user-table-dump.png"]
    EV3["📎 ASG<br/>Evidence<br/>webshell-rce.png"]

    CVE -->|"starts_at"| CH
    CH --> S1
    S1 -->|next_step| S2
    S2 -->|next_step| S3
    S3 -->|achieves| IMP
    S1 -->|supported_by| EV1
    S2 -->|supported_by| EV2
    S3 -->|supported_by| EV3

    style CVE fill:#220606,stroke:#FF5252,color:#FF5252
    style CH fill:#1E1004,stroke:#FFC107,color:#FFC107
    style S1 fill:#0E0C02,stroke:#7FFF00,color:#7FFF00
    style S2 fill:#0E0C02,stroke:#7FFF00,color:#7FFF00
    style S3 fill:#0E0C02,stroke:#7FFF00,color:#7FFF00
    style IMP fill:#200818,stroke:#9C27B0,color:#CE93D8
    style EV1 fill:#120820,stroke:#9C27B0,color:#CE93D8
    style EV2 fill:#120820,stroke:#9C27B0,color:#CE93D8
    style EV3 fill:#120820,stroke:#9C27B0,color:#CE93D8
```

**Reading this diagram:** Start at the red CVE node (ASG fact) → follow `starts_at` to the gold Chain (APG reasoning) → follow ChainSteps in order → arrive at the purple Impact (what was demonstrated) → follow `supported_by` back to the purple Evidence nodes (ASG proof). Every claim in the final report has this complete path. Nothing is asserted without evidence.

---

### Summary: What Makes This Remarkable

| Fact | Significance |
|------|-------------|
| **Zero manual commands** | The operator configured scope and pressed start. Everything else was autonomous. |
| **All exploitation gated** | SQLMap and Metasploit both went through Commander Mailbox — no exploitation without explicit approval |
| **4 chains, all VALIDATED** | Every seeded AttackChain reached a terminal VALIDATED state — including the trivially validated DB backup chain |
| **risk_score escalated** | Chain-01 started at 8.8 (CVSS); after RCE was confirmed, Commander escalated to 9.1 |
| **Credential reuse discovered** | Chain-03 validation uncovered staging-to-production credential overlap — flagged as an additional APG Impact node |
| **Traceability** | Every Impact claim links through ChainSteps back to Evidence files in the ASG |
| **Dual termination** | Mission ended because 111 nodes explored AND 4/4 chains VALIDATED — not because a timer fired |

---

## Module 06, Figure 5 — Cross-Mission Experience Store: The Persistent Learning Layer

The ASG and APG are reset fresh for every mission. The Cross-Mission Experience Store is the only structure that survives across missions. This diagram shows its two-direction lifecycle: how it is written at mission close, and how it is queried at mission start.

```mermaid
flowchart TD
    subgraph MISSION_A["🟢 Mission A — shopvault.io (completed)"]
        direction LR
        A1["APG: Chain-01 VALIDATED<br/>WordPress 5.9.3 + WooCommerce<br/>SQLi → Admin → RCE"]
        A2["APG: Chain-03 VALIDATED<br/>Django API + staging SQLi<br/>Blind SQLi → Credential extraction"]
    end

    subgraph WRITE["📥 WRITE TRIGGER<br/>Report Agent — at mission close<br/>For every VALIDATED chain"]
        W1["Store Entry Written:<br/>──────────────────────────<br/>Target fingerprint: WordPress 5.9.3 · WooCommerce 6.1 · Nginx 1.18<br/>Vuln class: SQLi (CVE-2022-21661)<br/>Tool sequence: SQLMap → SQLMap dump → Metasploit<br/>ChainStep params: WP_Query endpoint · wp_admin_shell_upload<br/>Outcome: RCE achieved · admin hash cracked · Summer2023!<br/>Mission ID: MIS-001"]
    end

    subgraph STORE["🗄️ CROSS-MISSION EXPERIENCE STORE<br/>(Persistent · RAG-backed · Survives across missions)"]
        S1["Entry: MIS-001 · WordPress SQLi → RCE"]
        S2["Entry: MIS-001 · Django staging blind SQLi"]
        S3["Entry: MIS-002 · ... (prior missions)"]
        S4["Entry: MIS-00N · ..."]
    end

    subgraph QUERY["📤 QUERY TRIGGER<br/>Commander — at mission start<br/>After first Technology nodes written to ASG"]
        Q1["Query: WordPress 5.x + WooCommerce<br/>──────────────────────────<br/>Retrieves: MIS-001 entry<br/>Injects into Commander context as:<br/>Candidate chain hypotheses —<br/>pre-validated patterns from analogous past engagements"]
    end

    subgraph MISSION_B["🔵 Mission B — new target with WordPress 5.8"]
        direction LR
        B1["Commander seeds APG Chain-01<br/>Front-loaded: SQLi hypothesis<br/>already validated on similar stack<br/>→ Skips zero-prior reasoning<br/>→ Validation pursued immediately"]
    end

    MISSION_A --> WRITE
    WRITE --> STORE
    STORE --> QUERY
    QUERY --> MISSION_B

    style MISSION_A fill:#062210,stroke:#7FFF00,color:#7FFF00
    style WRITE fill:#1E1004,stroke:#FFC107,color:#FFC107
    style STORE fill:#04162E,stroke:#00D4FF,color:#00D4FF
    style QUERY fill:#1E1004,stroke:#FFC107,color:#FFC107
    style MISSION_B fill:#10081E,stroke:#9C27B0,color:#CE93D8
```

**Key properties:**
- The store is queried **immediately after the first Technology node batch** is written — before Analysis Agent begins enumeration. This front-loads high-probability chains.
- Only `VALIDATED` chains are written. `RULED_OUT` chains are not stored (they represent dead ends on specific parameters, not reusable patterns).
- Retrieval returns **candidate hypotheses** — the Commander still evaluates them against the current ASG before seeding APG chains. The store accelerates, it does not override.

---

## Module 06, Figure 6 — Attack Strategy Library: Cross-Mission Procedural Learning

The Cross-Mission Experience Store records raw per-mission outcomes. The Attack Strategy Library is a higher-order abstraction: generalized, named, parameterized attack strategies crystallized from multiple missions that produced the same result on the same technology fingerprint.

```mermaid
flowchart TD
    subgraph RAW["🗄️ Cross-Mission Experience Store<br/>(Raw per-mission records)"]
        R1["MIS-001: WordPress 5.9.3 + WooCommerce<br/>→ CVE-2022-21661 SQLi → RCE ✅"]
        R2["MIS-007: WordPress 5.8.2 + WooCommerce 6.0<br/>→ CVE-2022-21661 SQLi → RCE ✅"]
        R3["MIS-012: WordPress 5.9.1 + WooCommerce 6.1<br/>→ CVE-2022-21661 SQLi → RCE ✅"]
    end

    subgraph THRESHOLD["⚖️ Crystallization Threshold Check<br/>Commander evaluates after each mission close<br/>Same fingerprint pattern → VALIDATED<br/>across ≥ 2 independent missions?"]
        T1{"≥ 2 missions<br/>with same fingerprint<br/>→ same VALIDATED<br/>outcome?"}
    end

    subgraph CRYSTALLIZE["🔬 Crystallization<br/>Scoped LLM call — generalizes specific params<br/>into a technology-class procedure"]
        CR1["Input: 3 raw mission entries<br/>Output: Generalized strategy<br/>─────────────────────────────<br/>Strategy ID: STRAT-WP-SQLI-001<br/>Name: WordPress WP_Query SQLi → Admin RCE<br/>Fingerprint: WordPress 5.x + WooCommerce + Nginx<br/>Vuln class: SQLi · CVE range: CVE-2022-21661<br/>Tool sequence: SQLMap (WP_Query endpoint)<br/>  → SQLMap --dump (users table)<br/>  → Metasploit (wp_admin_shell_upload)<br/>Confidence: 3/3 missions (100%)<br/>Last validated: MIS-012"]
    end

    subgraph LIBRARY["📚 ATTACK STRATEGY LIBRARY<br/>(Named · Parameterized · Confidence-scored)"]
        L1["STRAT-WP-SQLI-001<br/>WordPress SQLi → RCE<br/>Confidence: 100% (3 missions)"]
        L2["STRAT-DJANGO-IDOR-001<br/>Django API IDOR<br/>Confidence: 67% (2/3 missions)"]
        L3["STRAT-... (growing library)"]
    end

    subgraph INJECT["🚀 Mission Start — Strategy Retrieval<br/>Commander queries Library AFTER<br/>Cross-Mission Experience Store query"]
        I1["Match: new target has WordPress 5.7<br/>→ Retrieves STRAT-WP-SQLI-001<br/>→ Injected as pre-ranked APG AttackChain seed<br/>→ Prioritized ABOVE zero-prior chains<br/>   (carries validated track record, not just CVSS)"]
    end

    RAW --> THRESHOLD
    T1 -->|"yes"| CRYSTALLIZE
    T1 -->|"no — keep accumulating"| RAW
    CRYSTALLIZE --> LIBRARY
    LIBRARY --> INJECT

    style RAW fill:#04162E,stroke:#00D4FF,color:#00D4FF
    style THRESHOLD fill:#1E1004,stroke:#FFC107,color:#FFC107
    style CRYSTALLIZE fill:#062210,stroke:#7FFF00,color:#7FFF00
    style LIBRARY fill:#10081E,stroke:#9C27B0,color:#CE93D8
    style INJECT fill:#1E1004,stroke:#FFC107,color:#FFC107
```

**Distinction from Cross-Mission Experience Store:**

| | Experience Store | Strategy Library |
|---|---|---|
| Granularity | Per-mission, per-chain raw records | Generalized across ≥2 missions |
| Content | Specific tool params, exact chain outcomes | Parameterized procedures + confidence scores |
| Query trigger | After first Technology nodes written | After Experience Store query — same mission start window |
| Write trigger | Every VALIDATED chain at mission close | Crystallization threshold: ≥2 matching missions |

---

## Module 06, Figure 2 — Validation Agent Self-Debug Loop

When a ChainStep fails, the Validation Agent does not immediately mark it `RULED_OUT`. It enters a bounded 4-step self-debugging loop before giving up.

```mermaid
flowchart TD
    START["🎯 Validation Agent<br/>Executes ChainStep attempt<br/>(tool call → result)"]

    RESULT{Result?}

    SUCCESS["✅ ChainStep → VALIDATED<br/>Evidence written to ASG<br/>Commander advances chain"]

    DIAGNOSE["🔍 Step 1: DIAGNOSE<br/>─────────────────────────<br/>Analyze why the attempt failed:<br/>• Wrong parameter / encoding?<br/>• Authentication required?<br/>• Version mismatch?<br/>• Tool flag error?<br/>• Payload detection / filtering?"]

    CONTEXTUALIZE["📊 Step 2: CONTEXTUALIZE<br/>─────────────────────────<br/>Query ASG for additional node attributes:<br/>• Re-read Service version from ASG Service node<br/>• Check if auth credential captured in prior Evidence node<br/>• Retrieve any Parameter annotations added since spawn<br/>• Cross-check APG chain intent vs actual target state"]

    ADAPT["🔧 Step 3: ADAPT<br/>─────────────────────────<br/>Modify tool invocation based on<br/>diagnosis + additional ASG context:<br/>• Adjust payload / encoding<br/>• Add auth credential from Evidence node<br/>• Change tool flags / timing<br/>• Switch exploitation approach"]

    CAP{"Retry cap<br/>reached?<br/>(default: 3)"}

    RETRY["🔄 Retry<br/>Execute adapted tool call"]

    RULED_OUT["❌ ChainStep → RULED_OUT<br/>─────────────────────────<br/>Failure reason written as structured<br/>annotation to ASG Vulnerability node<br/>Commander re-reads APG<br/>Re-prioritizes remaining chains"]

    START --> RESULT
    RESULT -->|"success"| SUCCESS
    RESULT -->|"failure"| DIAGNOSE
    DIAGNOSE --> CONTEXTUALIZE
    CONTEXTUALIZE --> ADAPT
    ADAPT --> CAP
    CAP -->|"no — retry"| RETRY
    RETRY --> RESULT
    CAP -->|"yes — give up"| RULED_OUT

    style START fill:#04162E,stroke:#00D4FF,color:#00D4FF
    style RESULT fill:#1E1004,stroke:#FFC107,color:#fff
    style SUCCESS fill:#041A08,stroke:#7FFF00,color:#7FFF00
    style DIAGNOSE fill:#1A0606,stroke:#FF5252,color:#FF5252
    style CONTEXTUALIZE fill:#04162E,stroke:#00D4FF,color:#00D4FF
    style ADAPT fill:#1E1004,stroke:#FFC107,color:#FFC107
    style CAP fill:#1A0606,stroke:#FF5252,color:#fff
    style RETRY fill:#1E1004,stroke:#FFC107,color:#FFC107
    style RULED_OUT fill:#220606,stroke:#FF5252,color:#FF5252
```

**Why this matters:**
- The cap (default 3) prevents infinite loops while giving the agent a real chance to recover from transient errors
- `RULED_OUT` is a **structured, annotated outcome** — the failure reason is written back to the ASG Vulnerability node so future missions or the Report Agent can read it
- The Commander re-prioritizes immediately on any `RULED_OUT` — the next-highest chain is pursued without delay

---

## Module 06, Figure 3 — Single LLM API: All Call Types, One Integration Point

CMatrix issues every LLM call through a single configured API. What varies between calls is not the model — it is the scope of the prompt. This diagram makes that explicit.

```mermaid
flowchart LR
    API["☁️ SINGLE CONFIGURED<br/>LLM API<br/>─────────────<br/>One model.<br/>One integration point.<br/>All behavioral differences<br/>explained by prompt scope<br/>— not routing logic."]

    subgraph CALLS["All LLM Call Types in CMatrix"]
        direction TB

        CALL1["👑 Commander Reasoning<br/>─────────────────────────<br/>Scope: FULL<br/>Receives: complete ASG snapshot<br/>+ APG chain priorities + chain status<br/>Produces: next planned action<br/>Frequency: every planning cycle iteration"]

        CALL2["🗜️ MicroCompact<br/>─────────────────────────<br/>Scope: NARROW<br/>Receives: single raw tool output<br/>Instruction: normalize to ASG schema fields<br/>Produces: structured JSON → written to ASG<br/>Raw output: discarded after write<br/>Frequency: every tool call"]

        CALL3["🗜️ AutoCompact<br/>─────────────────────────<br/>Scope: NARROW<br/>Receives: older conversation turns<br/>(at 60% context threshold)<br/>Instruction: summarize losslessly<br/>Produces: summary replaces old turns<br/>Frequency: triggered at 60% context"]

        CALL4["🔍 Research Agent Normalization<br/>─────────────────────────<br/>Scope: NARROW<br/>Receives: raw NVD / Exploit-DB response<br/>Instruction: extract to ASG Vulnerability schema<br/>Produces: enriched Vulnerability node attributes<br/>Frequency: per Research Agent invocation"]

        CALL5["🚦 Permission Classifier<br/>─────────────────────────<br/>Scope: NARROW<br/>Receives: tool call + target ASG node<br/>+ current APG chain context<br/>Instruction: evaluate 3 axes → binary verdict<br/>Produces: EXECUTE or ESCALATE<br/>Frequency: every Medium-risk tool call"]
    end

    CALL1 --> API
    CALL2 --> API
    CALL3 --> API
    CALL4 --> API
    CALL5 --> API

    style API fill:#04162E,stroke:#00D4FF,color:#00D4FF
    style CALL1 fill:#1E1004,stroke:#FFC107,color:#FFC107
    style CALL2 fill:#062210,stroke:#7FFF00,color:#7FFF00
    style CALL3 fill:#062210,stroke:#7FFF00,color:#7FFF00
    style CALL4 fill:#10081E,stroke:#9C27B0,color:#CE93D8
    style CALL5 fill:#1A0606,stroke:#FF5252,color:#FF5252
```

**Why single-API matters for research:** Every result CMatrix produces is attributable to one model under one configuration. There is no hidden quality/cost trade-off from silently routing some calls to a cheaper model. Evaluation is honest.

---

## Module 06, Figure 4 — Vulnerability-Class Knowledge Injection

At agent spawn time, Validation Agent and Analysis Agent receive curated offline expert documents matched to their assigned vulnerability class. These are injected once at spawn — not accumulated in conversation history — so they survive context compaction automatically.

```mermaid
flowchart TD
    CMD["👑 Commander<br/>Spawns specialist agent<br/>with assigned vulnerability class"]

    subgraph INJECT["📚 Knowledge Injection at Spawn"]
        direction TB

        K1["Analysis Agent — Web Targets<br/>────────────────────────────────<br/>• OWASP Testing Guide checklist<br/>  (per applicable OWASP category)<br/>• Common web misconfiguration patterns"]

        K2["Analysis Agent — API Targets<br/>────────────────────────────────<br/>• REST API attack surface checklist<br/>• IDOR patterns<br/>• Parameter pollution techniques"]

        K3["Validation Agent — SQLi Chains<br/>────────────────────────────────<br/>• SQL injection technique taxonomy<br/>• SQLMap flag reference guide<br/>• Blind / time-based detection patterns"]

        K4["Validation Agent — XSS Chains<br/>────────────────────────────────<br/>• XSS payload pattern library<br/>• CSP bypass techniques<br/>• DOM vs reflected vs stored distinction"]

        K5["Validation Agent — Exploit Chains<br/>────────────────────────────────<br/>• Metasploit module selection heuristics<br/>• Payload / encoder selection guide<br/>• Post-exploitation evidence collection"]
    end

    subgraph PROP["Key Properties"]
        direction TB
        P1["Static · curated · version-controlled<br/>Encodes practitioner knowledge<br/>implicit in LLM pre-training"]
        P2["Re-injected at every spawn<br/>Never accumulated in history<br/>→ Survives FullCompact automatically"]
        P3["No internet access required<br/>Separate from Research Agent<br/>live CVE intelligence"]
    end

    CMD --> INJECT
    INJECT --> PROP

    style CMD fill:#04162E,stroke:#00D4FF,color:#00D4FF
    style INJECT fill:#10081E,stroke:#9C27B0,color:#CE93D8
    style K1 fill:#082018,stroke:#00D4FF,color:#00D4FF
    style K2 fill:#082018,stroke:#00D4FF,color:#00D4FF
    style K3 fill:#1A0606,stroke:#FF5252,color:#FF5252
    style K4 fill:#1A0606,stroke:#FF5252,color:#FF5252
    style K5 fill:#1A0606,stroke:#FF5252,color:#FF5252
    style PROP fill:#041A08,stroke:#7FFF00,color:#7FFF00
```

> **Distinction from Research Agent:** Research Agent retrieves **live CVE data** for specific discovered versions during a mission. Knowledge injection provides **evergreen offensive technique reasoning** that does not depend on external network access and is re-used across all missions.

---

## Module 08 — Complete ✅

The diagrams have been migrated to their contextually appropriate modules. Here is the new mapping:

| Location | Figure | What It Shows |
|---|---------|---------------|
| Module 03 | Figure 1: System Architecture | 3-tier swim-lane: Orchestration → Dual-Graph → Agents+Tools |
| Module 02 | Figure 1: Dual-Graph Model | ASG node tree (9 types) + APG chain lifecycle (4 chains) |
| Module 03 | Figure 2: Agent Spawn Lifecycle | Sequence diagram + spawn package + 3 isolation properties |
| Module 04 | Figure 1: Tool Risk Gate | Full decision tree + LLM classifier internals + 6 hooks timeline |
| Module 06 | Figure 1: Planning Cycle | Core loop + re-plan triggers + dual termination + compaction |
| Module 06 | Figure 2: Validation Agent Self-Debug Loop | 4-step diagnose→contextualize→adapt→cap loop |
| Module 06 | Figure 3: Single LLM API / Scoped Calls | All call types routed to one API, differentiated by prompt scope |
| Module 06 | Figure 4: Vulnerability-Class Knowledge Injection | Agent-to-document injection mapping |
| Module 07 | Figure 1: shopvault.io Walkthrough | Phase-by-phase timeline + Commander log + traceability chain |
| Module 06 | Figure 5: Cross-Mission Experience Store | Mission-start query + mission-end write lifecycle |
| Module 06 | Figure 6: Attack Strategy Library Crystallization | Fingerprint → multi-mission → crystallized strategy flow |
