# Module 08 — Visual Walkthrough: CMatrix Architecture in Diagrams

> **How to read this module:** Every diagram here is a visual translation of a concept already explained in Modules 01–07. If a box or arrow is unfamiliar, refer back to the relevant module. This file adds *no new concepts* — it only makes existing ones visible.

---

## Diagram 1 — System Architecture: The Three-Tier Overview

This is the master view of CMatrix. Everything fits into three tiers:

- **Tier 1 (top):** Orchestration — the operator configures, the Commander reasons
- **Tier 2 (middle):** The dual-graph world model — the two living knowledge stores
- **Tier 3 (bottom):** The six specialist agents and the tool layer they operate through

```mermaid
flowchart TD
    %% ── TIER 1: ORCHESTRATION ──────────────────────────────────────
    subgraph T1["① ORCHESTRATION TIER"]
        direction LR
        OP["🧑 OPERATOR\n─────────────\nDefines: Target domain\nScope boundaries\nAssessment mode\n(Black-Box / Grey-Box)"]
        CMD["👑 COMMANDER AGENT\n─────────────────────────────\n• Reads full ASG + APG state\n• Plans and delegates tasks\n• Seeds APG AttackChains\n• Approves High-risk tool calls\n• Writes ONLY to APG\n• Determines termination"]
        VPP["📄 VAPT PROTOCOL PROMPT\n──────────────────────────\nMethodology-as-Config:\n• Phase sequencing rules\n• Re-plan triggers\n• Termination conditions\n• Tool selection heuristics"]

        OP -- "mission config\n(target + scope)" --> CMD
        CMD <-- "guides\nplanning policy" --> VPP
    end

    %% ── TIER 2: DUAL-GRAPH WORLD MODEL ─────────────────────────────
    subgraph T2["② DUAL-GRAPH WORLD MODEL TIER"]
        direction LR
        subgraph ASG["🟢 ATTACK SURFACE GRAPH (ASG)\n── Discovered Reality ──\nFacts ONLY. Never contains hypotheses."]
            A1["Domain · Host · Port\nService · Technology"]
            A2["Endpoint · Parameter\nVulnerability · Evidence"]
        end
        SEP["⬛ STRICT\nSEPARATION\n────────\nNo agent\ncrosses this\nboundary"]
        subgraph APG["🟡 ATTACK PATH GRAPH (APG)\n── Inferred Opportunity ──\nReasoning ONLY. Never contains raw scan data."]
            P1["AttackChain\nrisk_score · priority"]
            P2["ChainStep\nvalidation_status"]
            P3["Impact\n(demonstrated)"]
        end
    end

    %% ── TIER 3: AGENTS + TOOLS ──────────────────────────────────────
    subgraph T3["③ SPECIALIZED AGENTS + TOOL ADAPTER TIER"]
        direction LR
        AGR["🕵️ Recon\nAmass·httpx·Nmap"]
        AGA["🔬 Analysis\nWhatWeb·Gobuster\nffuf·Nuclei·ZAP"]
        AGI["🔍 Research\nNVD·Exploit-DB\nGitHub"]
        AGV["🎯 Validation\nSQLMap·Metasploit"]
        AGE["📸 Evidence\nEyeWitness"]
        AGRP["📝 Report\nReads ASG+APG"]

        subgraph TAL["TOOL ADAPTER LAYER + RISK GATE"]
            RG1["🟢 LOW\nExecute immediately"]
            RG2["🟡 MED\nLLM Classifier"]
            RG3["🔴 HIGH\nCommander Mailbox"]
        end
    end

    %% ── CROSS-TIER ARROWS ───────────────────────────────────────────
    CMD -- "reads state" --> ASG
    APG -- "status feedback" --> CMD
    CMD -- "derives chains\nfrom new Vulnerability nodes" --> APG
    CMD -- "spawns with\nscoped context" --> AGR
    CMD -- "spawns with\nscoped context" --> AGA
    CMD -- "spawns with\nscoped context" --> AGI
    CMD -- "spawns with\nscoped context" --> AGV
    CMD -- "spawns with\nscoped context" --> AGE
    CMD -- "spawns at\nmission end" --> AGRP

    AGR -- "writes Domain\nHost·Port·Service" --> ASG
    AGA -- "writes Technology\nEndpoint·Vulnerability" --> ASG
    AGI -- "enriches Vulnerability\nnodes (CVE+PoC)" --> ASG
    AGV -- "writes Evidence\nadvances ChainStep" --> ASG
    AGE -- "writes Evidence\nscreenshots" --> ASG

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

*Diagram 2 below: Dual-Graph Model (ASG node tree + APG attack chain, visualised)*

---

## Diagram 2 — The Dual-Graph Model: ASG + APG Visualised

This diagram shows both graphs side-by-side using the `shopvault.io` mission as a concrete example. Left side = ASG (what was discovered). Right side = APG (what can be done with it). The vertical barrier in the middle = the strict separation boundary.

### 2A — ASG: The Attack Surface Graph (Discovered Reality)

Every node here represents something **confirmed by a tool**. Every edge represents a **confirmed relationship**. No guesses. No hypotheses.

```mermaid
graph TD
    %% ── ASG ROOT ──────────────────────────────────────────────
    DOM["🌐 Domain\nshopvault.io"]

    %% ── HOSTS ─────────────────────────────────────────────────
    H1["🖥️ Host\n10.0.0.1\nOS: Ubuntu 22.04"]
    H2["🖥️ Host\n10.0.0.2\nOS: Debian 11"]
    H3["🖥️ Host\napi.shopvault.io\n10.0.0.5"]

    %% ── PORTS ─────────────────────────────────────────────────
    P443["🔌 Port :443\ntcp · open"]
    P8080["🔌 Port :8080\ntcp · open · unencrypted"]
    P80["🔌 Port :80\ntcp · open"]
    P22["🔌 Port :22\ntcp · open"]

    %% ── SERVICES ──────────────────────────────────────────────
    SVC1["⚙️ Service\nNginx 1.18.0"]
    SVC2["⚙️ Service\nHTTP unencrypted"]
    SVC3["⚙️ Service\nOpenSSH 8.9p1"]

    %% ── TECHNOLOGIES ──────────────────────────────────────────
    TECH1["📦 Technology\nWordPress 5.9.3"]
    TECH2["📦 Technology\nWooCommerce 6.1"]
    TECH3["📦 Technology\nDjango 4.1.2"]

    %% ── ENDPOINTS ─────────────────────────────────────────────
    EP1["🔗 Endpoint\n/wp-admin/login\nsensitivity: HIGH"]
    EP2["🔗 Endpoint\n/backup/db_export.sql\nsensitivity: CRITICAL"]
    EP3["🔗 Endpoint\n/api/v1/orders"]
    EP4["🔗 Endpoint\n/api/v1/internal/users\nundocumented!"]

    %% ── PARAMETERS ────────────────────────────────────────────
    PARAM1["⚙️ Parameter\nuser_id=?\ninjectable: TRUE"]

    %% ── VULNERABILITIES ───────────────────────────────────────
    VULN1["🚨 Vulnerability\nCVE-2022-21661\nCVSS: 8.8 · SQLi\nPoC: Exploit-DB ✓\nMetasploit module ✓"]
    VULN2["🚨 Vulnerability\nIDOR on /api/v1/orders\nSeverity: HIGH"]
    VULN3["🚨 Vulnerability\nExposed DB backup\nSeverity: CRITICAL"]

    %% ── EVIDENCE ──────────────────────────────────────────────
    EV1["📎 Evidence\nsqli-extraction.txt"]
    EV2["📎 Evidence\nadmin-panel.png"]
    EV3["📎 Evidence\nwebshell-rce.png"]

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

### 2B — APG: The Attack Path Graph (Inferred Opportunity)

The Commander reads the ASG and reasons: *"These vulnerabilities can chain together into complete attack paths."* Those chains live here — in the APG.

```mermaid
flowchart TD
    %% ── CHAIN 01 ──────────────────────────────────────────────────
    subgraph C1["AttackChain: Chain-01 · risk_score: 9.1 · VALIDATED"]
        direction TB
        C1S["starts_at → ASG: CVE-2022-21661\n(WordPress SQLi, CVSS 8.8)"]

        STEP1["ChainStep 1\n─────────────\nTool: SQLMap\nTarget: /wp-admin/admin-ajax.php\nAction: Confirm WP_Query SQLi\nStatus: ✅ VALIDATED\n↗ supported_by: sqli-extraction.txt"]

        STEP2["ChainStep 2\n─────────────\nTool: SQLMap --dump\nAction: Extract WordPress users table\nGet admin password hash\nStatus: ✅ VALIDATED\n↗ supported_by: users-table-dump.png"]

        STEP3["ChainStep 3\n─────────────\nTool: Metasploit\nModule: wp_admin_shell_upload\nAction: Deploy webshell → RCE\nStatus: ✅ VALIDATED\n↗ supported_by: webshell-rce.png"]

        IMP1["💀 IMPACT\n─────────────\nFull RCE on shopvault.io web server\nCustomer PII database accessible\nClassification: CRITICAL"]

        C1S --> STEP1
        STEP1 -->|next_step| STEP2
        STEP2 -->|next_step| STEP3
        STEP3 -->|achieves| IMP1
    end

    %% ── CHAIN 02 ──────────────────────────────────────────────────
    subgraph C2["AttackChain: Chain-02 · risk_score: 7.5 · VALIDATED"]
        direction TB
        C2S["starts_at → ASG: IDOR on /api/v1/orders\n(user_id parameter unsanitised)"]

        STEP21["ChainStep 1\n─────────────\nTool: SQLMap / ffuf\nAction: Confirm IDOR\nAny user_id returns that user's orders\nStatus: ✅ VALIDATED"]

        IMP2["💀 IMPACT\n─────────────\nAll customer order history exposed\nName · address · payment method visible\nClassification: HIGH"]

        C2S --> STEP21
        STEP21 -->|achieves| IMP2
    end

    %% ── CHAIN 03 (RULED OUT) ──────────────────────────────────────
    subgraph C3["AttackChain: Chain-03 · risk_score: 6.2 · RULED_OUT"]
        direction TB
        C3S["starts_at → ASG: Exposed /backup/db_export.sql"]

        STEP31["ChainStep 1\n─────────────\nAction: Direct HTTP GET of .sql file\nStatus: ❌ RULED_OUT\nReason: File returns 403 after\nfirst access (WAF blocked)\nFailure written to ASG Vuln node"]

        C3S --> STEP31
    end

    %% ── PRIORITY RANKING ──────────────────────────────────────────
    PRIO["📊 APG Priority Queue\n──────────────────────\n#1 Chain-01 · 9.1 ← validated first\n#2 Chain-02 · 7.5 ← validated second\n#3 Chain-03 · 6.2 ← ruled out\n\nCommander re-ranks on every status change"]

    %% Styles
    style C1 fill:#1E1004,stroke:#FFC107,color:#FFC107
    style C2 fill:#1E1004,stroke:#FFC107,color:#FFC107
    style C3 fill:#1A0606,stroke:#FF5252,color:#FF5252
    style STEP1 fill:#0E0C02,stroke:#7FFF00,color:#7FFF00
    style STEP2 fill:#0E0C02,stroke:#7FFF00,color:#7FFF00
    style STEP3 fill:#0E0C02,stroke:#7FFF00,color:#7FFF00
    style IMP1 fill:#200818,stroke:#9C27B0,color:#CE93D8
    style STEP21 fill:#0E0C02,stroke:#7FFF00,color:#7FFF00
    style IMP2 fill:#200818,stroke:#9C27B0,color:#CE93D8
    style STEP31 fill:#200606,stroke:#FF5252,color:#FF5252
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

*Diagram 3 below: Agent Spawn Lifecycle*

---

## Diagram 3 — Agent Spawn Lifecycle: Born Fresh, Die Clean

This is the most important architectural insight that separates CMatrix from other multi-agent systems. Every agent is born fresh, does exactly one job with a scoped context, and vanishes — leaving only structured graph state behind.

### 3A — The Spawn Lifecycle (single agent)

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

### 3B — What Each Agent Receives at Spawn (Scoped Context)

```mermaid
flowchart LR
    CMD["👑 COMMANDER\nDecides next action"]

    subgraph SPAWN["Agent Spawn Package"]
        direction TB
        S1["📊 ASG SLICE\nOnly nodes relevant to this task\nNot the full graph"]
        S2["🔗 APG SLICE\nRelevant AttackChains only\n(if this is a Validation task)"]
        S3["🔧 TOOL SET\nAuthorized tools only\nNo others available"]
        S4["📋 TASK SPEC\nCommander's current plan item\nExact objective for this spawn"]
        S5["📚 KNOWLEDGE DOCS\n(Validation Agent only)\nVulnerability-class expert docs\ninjected at spawn time"]
    end

    subgraph AGENT["🤖 Isolated Agent Context\n(fresh per task — no prior history)"]
        WORK["Works autonomously\nwithin bounded context\nAll tool calls → Risk Gate"]
    end

    subgraph RETURN["Agent Returns"]
        R1["✅ Structured ASG Delta\nNew nodes + edges only"]
        R2["🗑️ Working context DISCARDED\nRaw tool output → gone\nConversation history → gone\nIntermediate reasoning → gone"]
    end

    CMD -->|"spawn with\nscoped package"| SPAWN
    SPAWN --> AGENT
    AGENT --> RETURN
    RETURN -->|"delta written\nto ASG"| ASG_ICON["🟢 ASG"]
    RETURN -->|"Commander reads\nnew nodes"| CMD

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

### 3C — Why Context Isolation Produces Three Critical Properties

```mermaid
flowchart TD
    CI["🔒 CONTEXT ISOLATION\nEvery agent spawns fresh\nEvery agent dies clean"]

    P1["✅ Property 1\nCOMMANDER STAYS CLEAN\n─────────────────────\nCommander only ever sees\nASG/APG state — never\nthousands of lines of\nraw tool output.\nIts reasoning context stays\nsurgically focused."]

    P2["✅ Property 2\nAGENTS CANNOT CONTAMINATE\n─────────────────────────\nAgent A's verbose history\nnever appears in Agent B's\ncontext. Knowledge passes\nonly through the ASG.\nNo shared memory. No\naccidental cross-pollution."]

    P3["✅ Property 3\nREJECTIONS DON'T BIAS PLANNING\n────────────────────────────────\nWhen Commander rejects a\nHigh-risk tool call, that\nrejection never appears in\nthe Commander's own context.\nRefusals don't accumulate\nand skew future decisions."]

    RESULT["🎯 RESULT\nLong missions with many agents\nproduce the same quality of\nreasoning as single-agent tasks.\nContext quality does not degrade\nwith mission complexity."]

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

### Reading Key for Diagram 3

| Concept | What to Notice |
|---------|---------------|
| Spawn package | 5 components — each scoped, none is the full system state |
| Tool Set boundary | Agent can ONLY use tools it was authorized for at spawn |
| Knowledge Docs | Only Validation + Analysis agents receive these — matched to their vulnerability class |
| Return = delta only | The ASG grows by addition — agents don't rewrite existing nodes |
| Context discarded | The working session is gone — the ASG persists forever |

---

*Diagram 4 coming next: Tool Risk Gate Flow*
