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

*Diagram 4 below: Tool Risk Gate Flow*

---

## Diagram 4 — Tool Risk Gate: Every Tool Call's Journey

No tool in CMatrix executes without passing through this gate. This diagram shows the complete decision path — from an agent requesting a tool call, through all three risk tiers, to either execution or rejection.

### 4A — The Full Risk Gate Decision Tree

```mermaid
flowchart TD
    START["🤖 Agent requests tool call\n───────────────────────────\nTool: Gobuster\nTarget: shopvault.io\nParams: -w big.txt -x php,sql"]

    HOOK1["🪝 PreToolUse Hook fires\n───────────────────────\nExternal observers notified.\nHook returns: CONTINUE / BLOCK / MODIFY"]

    HOOK1_CHECK{Hook returns?}
    HOOK_BLOCK["❌ BLOCKED\nAction cancelled.\nReason logged."]
    HOOK_MODIFY["🔄 MODIFIED\nPayload updated.\nProceeds with\nmodified params."]

    SCOPE["🔍 Scope Check\n──────────────────\nIs target in declared scope?\nIs this tool authorized\nfor this agent type?"]

    SCOPE_FAIL["❌ OUT OF SCOPE\nTool call rejected.\nAgent notified.\nNo execution."]

    CLASSIFY["🎯 Risk Classification\n──────────────────────\nWhich tier does this call belong to?"]

    LOW{"🟢 LOW RISK?\nPassive tools:\nAmass · httpx\nWhatWeb"}
    MED{"🟡 MEDIUM RISK?\nActive tools:\nNmap · Gobuster · ffuf\nNuclei · OWASP ZAP"}
    HIGH{"🔴 HIGH RISK?\nExploitation tools:\nSQLMap · Metasploit"}

    EXEC_LOW["✅ Execute immediately\nNo further approval needed"]

    CLASSIFIER["🧠 LLM Permission Classifier\n────────────────────────────\nFast filter pass:\n  → Clearly safe? → EXECUTE\n  → Clearly risky? → ESCALATE\n\nChain-of-thought pass (ambiguous):\n  Axis 1: Scope alignment\n  Axis 2: Chain intent\n  Axis 3: Parameter safety\n  → Checks for prompt injection"]

    CLF_RESULT{Classifier verdict?}
    CLF_EXEC["✅ EXECUTE\nProceeds to\nTool Adapter"]
    CLF_ESC["⬆️ ESCALATE\nRouted to\nCommander Mailbox"]

    MAILBOX["📬 Commander Mailbox\n──────────────────────\nApproval request queued:\n  • Tool + module\n  • Target ASG node\n  • Chain context\n  • Rationale\n\n(Human inserted here\nin supervised mode)"]

    CMD_REVIEW{Commander decides?}
    CMD_APPROVE["✅ APPROVED\nProceeds to\nTool Adapter"]
    CMD_REJECT["❌ REJECTED\nCancelled.\nReason annotated\nto APG chain."]
    CMD_MODIFY["🔄 MODIFIED\nCommander adjusts\nparams, then approves"]

    ADAPTER["⚙️ Tool Adapter executes\n────────────────────────\n1. Translate request → CLI command\n2. Run tool\n3. Parse raw output → structured JSON\n4. Discard raw output"]

    HOOK2["🪝 PostToolUse Hook fires\n─────────────────────────\nStructured findings available.\nHook can: log · alert · validate · block write"]

    ASG_WRITE["🟢 Structured findings\nwritten to ASG as\nnodes + edges"]

    AG_SUMMARY["🤖 Agent receives\ncompact summary only\n(NOT raw output)"]

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

### 4B — What the LLM Permission Classifier Actually Checks

```mermaid
flowchart LR
    INPUT["🟡 Medium-Risk\nTool Call\n─────────────\nTool: Gobuster\nTarget: staging.shopvault.io\nParams: -w big.txt"]

    subgraph FAST["Fast Filter (instant)"]
        F1{"Obviously safe?\n(passive, in-scope,\nstandard params)"}
        F2{"Obviously risky?\n(out-of-scope target,\nsuspicious params)"}
    end

    subgraph COT["Chain-of-Thought Pass (ambiguous cases)"]
        AX1["Axis 1: SCOPE ALIGNMENT\n──────────────────────\nIs staging.shopvault.io\nin the declared scope?\nWas it explicitly excluded?"]
        AX2["Axis 2: CHAIN INTENT\n───────────────────\nDoes Gobuster on this host\nmake sense for the current\nAPG AttackChain being pursued?"]
        AX3["Axis 3: PARAMETER SAFETY\n────────────────────────\nDo params match current\nASG state? Or do they look\nlike they were injected from\ncrawled web content?\n(Prompt injection check)"]
    end

    VERDICT{"Final verdict"}
    EXEC["✅ EXECUTE"]
    ESC["⬆️ ESCALATE\nto Commander\nMailbox"]

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

### 4C — The 6 Lifecycle Hooks: Where Operators Can Intervene

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

*Diagram 5 below: Autonomous Planning Cycle Loop*

---

## Diagram 5 — The Autonomous Planning Cycle

The Commander runs this loop continuously — from mission start until the dual-graph termination condition fires. Every iteration is grounded in graph state. Every decision is traceable to a specific graph event.

### 5A — The Core Planning Loop

```mermaid
flowchart TD
    START(["🚀 MISSION START\nOperator provides: root domain + scope + mode\nASG seeded: [Domain: shopvault.io]\nAPG: empty"])

    OBS_ASG["👁️ OBSERVE ASG\n─────────────────────────────────\n• Which nodes are unexplored?\n• Which Vulnerability nodes are new?\n• Which Technology nodes need Research?"]

    OBS_APG["👁️ OBSERVE APG\n─────────────────────────────────\n• Which chains are HYPOTHESIZED?\n• Which are PARTIALLY_VALIDATED?\n• Which just went VALIDATED or RULED_OUT?"]

    REASON["🧠 REASON\n─────────────────────────────────\nGiven ASG + APG state:\nWhat is the single best\nnext action right now?"]

    DECIDE{What does\nreasoning\nproduce?}

    EXPLORE["🗺️ EXPLORE\nASG gap detected\n─────────────────\nSpawn discovery agent:\n• Recon → unscanned hosts\n• Analysis → untested tech\n• Research → unenriched CVE"]

    VALIDATE["🎯 VALIDATE\nHigh-priority chain waiting\n─────────────────────────\nSpawn Validation Agent\nfor highest-priority\nHYPOTHESIZED chain"]

    BOTH["↕️ PARALLEL\nBoth ASG gaps AND\nunvalidated chains exist\n─────────────────────\nCommander weighs priority:\nHigh-risk chain beats\nlow-value exploration"]

    AGENT_RUNS["⚡ AGENT EXECUTES\n(tools → Risk Gate → ASG writes)"]

    UPDATE_ASG["📥 UPDATE ASG\nNew nodes + edges written\nby returning agent"]

    UPDATE_APG["📥 UPDATE APG (Commander)\n─────────────────────────\nNew Vuln nodes → seed chains?\nChainStep advanced → update status?\nRULED_OUT chain → re-prioritize?"]

    CYCLE_GUARD{Cycle Guard:\nRepeated\nidentical calls?}
    REFLECTOR["🪞 REFLECTOR\nRepeated failures?\n→ Issue corrective guidance\n→ Agent adapts approach"]
    FORCE_REPLAN["🔄 FORCE RE-PLAN\nStop current approach\nCommander reassigns"]

    TERM{Termination\ncondition met?}
    TERM_CHECK["✅ ASG exhausted?\n(no unexplored nodes)\nAND\n✅ APG resolved?\n(all chains VALIDATED\nor RULED_OUT)"]

    REPORT["📝 Spawn Report Agent\nReads full ASG + APG\nGenerates professional\npenetration test report"]

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
    CYCLE_GUARD -->|"yes — fixation\ndetected"| FORCE_REPLAN
    CYCLE_GUARD -->|"repeated different\nfailures"| REFLECTOR
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

### 5B — What Triggers a Re-Plan (Graph-Grounded Events)

```mermaid
flowchart LR
    subgraph ASG_EVENTS["ASG Trigger Events"]
        E1["🆕 New Vulnerability node written\n→ Should this seed a new APG chain?"]
        E2["🆕 New Technology node written\n→ Spawn Research Agent for CVE lookup"]
        E3["🆕 New Endpoint node written\n→ Analysis Agent needs to probe it"]
    end

    subgraph APG_EVENTS["APG Trigger Events"]
        E4["📈 Chain → PARTIALLY_VALIDATED\n→ Re-rank all chain priorities"]
        E5["✅ Chain → VALIDATED\n→ Mark complete, pursue next"]
        E6["❌ Chain → RULED_OUT\n→ Remove from queue, re-prioritize"]
    end

    subgraph GUARD_EVENTS["Cycle Guard Events"]
        E7["🔁 Same tool call repeated ×3\n→ Force re-plan immediately"]
        E8["💥 Repeated different failures\n→ Reflector issues guidance"]
    end

    CMD["👑 Commander\nRe-plans on\nany of these\nevents"]

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

### 5C — The Dual Termination Condition (Why Both Must Be True)

```mermaid
flowchart TD
    Q["❓ Is the mission complete?"]

    C1{"ASG exhausted?\n────────────────\nEvery Domain, Host, Port,\nService, Technology,\nEndpoint, Parameter node\nhas been investigated\nby the appropriate agent"}

    C2{"APG resolved?\n──────────────────\nEvery AttackChain is in\na terminal state:\nVALIDATED or RULED_OUT\n\nNo chain is still\nHYPOTHESIZED or\nPARTIALLY_VALIDATED"}

    ONLY1["❌ NOT DONE\nASG explored but\nchains still open.\nAttack reasoning\nis unfinished."]

    ONLY2["❌ NOT DONE\nAll chains resolved\nbut new ASG nodes\njust written.\nMight seed new chains."]

    NEITHER["❌ NOT DONE\nBoth incomplete.\nContinue mission."]

    BOTH_TRUE["✅ MISSION COMPLETE\nASG is fully mapped.\nAll attack opportunities\nproven or disproven.\nReport Agent spawned."]

    CONTRAST["⚠️ Why existing systems fail:\n─────────────────────────────\nTimer-based: stops mid-chain\nTask-queue-based: can't express APG resolution\nOnly CMatrix defines both\nconditions simultaneously"]

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

### 5D — Context Compaction: How Long Missions Stay Sharp

```mermaid
flowchart LR
    subgraph NORMAL["Normal Operation"]
        T1["Tool runs\n→ MicroCompact\nRaw output discarded\nAgent sees 3-line summary"]
    end

    subgraph AUTO["AutoCompact @ 60% context"]
        T2["Older conversation turns\nsummarized by scoped LLM call\nSummary replaces raw turns\nAgent continues uninterrupted"]
    end

    subgraph FULL["FullCompact @ 85% context"]
        T3["Entire history replaced\nfrom scratch using:\n• Current ASG snapshot\n• Current APG priorities\n• Last N tool results\n\nZERO intelligence lost\n(everything important\nis in the graph)"]
    end

    T1 -->|context grows| AUTO
    AUTO -->|context grows| FULL
    FULL -->|fresh context| T1

    ASG_KEY["🟢 ASG is the key\n────────────────\nConversation history\nis expendable because\nall discoveries live\nin the graph permanently.\nFullCompact = safe."]

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

*Diagram 6 below: shopvault.io Full Mission Walkthrough*

---

## Diagram 6 — Real-World Scenario: shopvault.io End-to-End

This is the complete picture. One real mission. Zero manual commands. Watch every tool, every graph write, every Commander decision, from the moment the operator presses start to the final professional report.

**Target:** `shopvault.io` — an e-commerce platform  
**Mode:** Black-Box (zero prior knowledge)  
**Scope:** All subdomains, web apps, REST APIs  
**Operator action:** Provide domain + scope → press start

---

### 6A — Mission Timeline: Phase by Phase

```mermaid
flowchart TD
    OP(["🧑 OPERATOR\nTarget: shopvault.io\nScope: all subdomains\nMode: Black-Box\n→ PRESS START"])

    subgraph P1["🟢 PHASE 1 — RECONNAISSANCE\nRecon Agent spawned"]
        A1["Tool: Amass\n────────────────────────\n14 subdomains discovered:\napi · admin · staging\npay · mail · static · ..."]
        A2["Tool: httpx\n────────────────────────\n11 live hosts confirmed\nstaging → unexpected 200 OK\npay → TLS certificate EXPIRED"]
        A3["Tool: Nmap\n────────────────────────\n28 open ports mapped\nPorts: 80, 443, 8080, 8443, 22\nServices: Nginx 1.18 · OpenSSH 8.9\nUnencrypted HTTP on port 8080"]
        D1["📥 ASG DELTA\n37 new nodes written:\n14 Domain · 11 Host\n28 Port · 15 Service"]
    end

    subgraph P2["🔵 PHASE 2 — ANALYSIS + INTELLIGENCE\nAnalysis Agent + Research Agent spawned"]
        B1["Tool: WhatWeb\n────────────────────────\nWordPress 5.9.3 on shopvault.io\nWooCommerce 6.1 detected\nDjango 4.1.2 on api.shopvault.io\n→ Commander spawns Research Agent"]
        B2["Research Agent: NVD + Exploit-DB\n────────────────────────────────\nCVE-2022-21661 found (CVSS 8.8)\nPoC on Exploit-DB ✓\nMetasploit module available ✓"]
        B3["Tool: Gobuster\n────────────────────────\n/backup/db_export_2023.sql → 200!\n/wp-admin/login → 200\n/wp-admin/users → 403\n/api/v1/internal/users → 200"]
        B4["Tool: ffuf\n────────────────────────\nIDOR: user_id param unsanitised\n/api/v2 routes discovered\nVirtual host: internal.shopvault.io"]
        B5["Tool: Nuclei\n────────────────────────\nCVE-2022-21661 template → MATCH\nExposed phpinfo.php on staging\nDefault creds check: admin/admin → fail"]
        B6["Tool: OWASP ZAP\n────────────────────────\nXSS on /search?q= (reflected)\nSQL error on staging login form\nMissing security headers on API"]
        D2["📥 ASG DELTA: 61 new nodes\nTechnology(3) · Endpoint(19)\nParameter(8) · Vulnerability(9)\n\n📥 APG DELTA: 3 chains seeded\nChain-01: CVE SQLi→RCE (8.8)\nChain-02: IDOR orders API (7.5)\nChain-03: Exposed DB backup (6.2)"]
    end

    subgraph P3["🔴 PHASE 3 — VALIDATION + EVIDENCE\nValidation Agent + Evidence Agent spawned"]
        C1["Chain-01 (highest priority: 8.8)\n────────────────────────────────\nStep 1: SQLMap on WP_Query\n→ SQLi confirmed ✅\n→ Evidence: sqli-extraction.txt"]
        C2["Step 2: SQLMap --dump users table\n────────────────────────────────\n→ Admin hash extracted ✅\n→ Offline crack: password123\n→ Evidence: user-table-dump.png"]
        C3["Step 3: Metasploit wp_admin_shell_upload\n────────────────────────────────\n⚠️ HIGH RISK → Commander Mailbox\n→ Commander APPROVES\n→ Web shell deployed ✅\n→ RCE confirmed!\n→ risk_score escalated: 8.8 → 9.1\n→ Evidence: webshell-rce.png"]
        C4["Chain-02 (risk: 7.5)\n────────────────────────────────\nffuf: user_id=456 returns user 456 orders\n→ IDOR confirmed ✅\n→ All customer PII accessible\n→ Evidence: idor-orders-dump.png"]
        C5["Chain-03 (risk: 6.2)\n────────────────────────────────\nGET /backup/db_export_2023.sql\n→ Attempt 1: 403 (WAF blocked)\n→ Diagnose: WAF active\n→ Attempt 2: header bypass → 403\n→ Attempt 3: path variation → 403\n→ CAP REACHED → RULED_OUT\n→ Failure written to ASG Vuln node"]
        D3["📥 APG DELTA\nChain-01: VALIDATED (9.1)\nChain-02: VALIDATED (7.5)\nChain-03: RULED_OUT (6.2)\n\n📥 ASG DELTA\n4 Evidence nodes + edges added"]
    end

    subgraph P4["🟣 PHASE 4 — REPORT\nReport Agent spawned — reads full ASG + APG"]
        RPT["📋 PROFESSIONAL PENETRATION TEST REPORT\n─────────────────────────────────────────\n• Executive Summary\n• 2 Validated Attack Chains (RCE + IDOR)\n• 1 Ruled-Out Chain (DB backup WAF-protected)\n• Full attack surface map (14 subdomains · 11 hosts)\n• 9 vulnerabilities with CVSS scores\n• Remediation guidance ordered by risk_score\n• Screenshot evidence at every ChainStep\n• ZERO manual commands issued"]
    end

    TERM["✅ TERMINATION CONDITION MET\nASG: all 98 nodes explored\nAPG: all 3 chains in terminal state\n→ Report Agent spawned"]

    OP --> P1
    A1 --> A2 --> A3 --> D1
    D1 --> P2
    B1 --> B2 --> B3 --> B4 --> B5 --> B6 --> D2
    D2 --> P3
    C1 --> C2 --> C3
    C3 --> C4 --> C5 --> D3
    D3 --> TERM
    TERM --> P4
    P4 --> RPT

    style OP fill:#041A08,stroke:#7FFF00,color:#7FFF00
    style P1 fill:#062210,stroke:#7FFF00,color:#7FFF00
    style P2 fill:#04162E,stroke:#00D4FF,color:#00D4FF
    style P3 fill:#1A0606,stroke:#FF5252,color:#FF5252
    style P4 fill:#10081E,stroke:#9C27B0,color:#CE93D8
    style D1 fill:#041A08,stroke:#7FFF00,color:#7FFF00
    style D2 fill:#041A08,stroke:#7FFF00,color:#7FFF00
    style D3 fill:#1E1004,stroke:#FFC107,color:#FFC107
    style TERM fill:#041A08,stroke:#7FFF00,color:#7FFF00
    style RPT fill:#10081E,stroke:#9C27B0,color:#CE93D8
```

---

### 6B — The Commander's Decision Log (Key Moments)

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
        Step 5  : Trigger: IDOR Vuln node written by ZAP
                : Action: Seed Chain-02 in APG — HYPOTHESIZED — priority 2
        Step 6  : Trigger: Exposed DB backup Vuln node written
                : Action: Seed Chain-03 in APG — HYPOTHESIZED — priority 3
    section Validation
        Step 7  : Trigger: Chain-01 is highest priority
                : Action: Spawn Validation Agent for Chain-01
        Step 8  : Trigger: SQLMap HIGH-risk call arrives at mailbox
                : Decision: APPROVE — target confirmed in scope — chain context valid
        Step 9  : Trigger: Metasploit HIGH-risk call arrives at mailbox
                : Decision: APPROVE — Steps 1+2 already VALIDATED — RCE is the goal
        Step 10 : Trigger: Chain-01 → VALIDATED — risk escalated to 9.1
                : Action: Spawn Validation Agent for Chain-02
        Step 11 : Trigger: Chain-02 → VALIDATED
                : Action: Spawn Validation Agent for Chain-03
        Step 12 : Trigger: Chain-03 → RULED_OUT after 3 retries
                : Note: Failure reason written to ASG Vuln node
    section Termination
        Step 13 : Trigger: ASG exhausted (98 nodes explored) AND APG resolved (3/3 terminal)
                : Action: Dual-graph termination condition met — spawn Report Agent
```

---

### 6C — Final Mission Stats

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
        CH1["Chain-01: VALIDATED ✅\nrisk: 9.1 (escalated)\nSQLi → Admin → RCE"]
        CH2["Chain-02: VALIDATED ✅\nrisk: 7.5\nIDOR → Customer PII"]
        CH3["Chain-03: RULED_OUT ❌\nrisk: 6.2\nDB backup WAF-protected"]
    end

    subgraph REPORT_FINAL["📝 Report Output"]
        direction TB
        R1["2 validated attack chains\nwith step-by-step reproduction"]
        R2["4 screenshot evidence artifacts\nlinked at each ChainStep"]
        R3["9 vulnerabilities\nordered by risk_score"]
        R4["Remediation guidance\nprioritized by business risk"]
        R5["0 manual commands issued\nduring entire assessment"]
    end

    ASG_FINAL --> REPORT_FINAL
    APG_FINAL --> REPORT_FINAL

    style ASG_FINAL fill:#062210,stroke:#7FFF00,color:#7FFF00
    style APG_FINAL fill:#1E1004,stroke:#FFC107,color:#FFC107
    style REPORT_FINAL fill:#10081E,stroke:#9C27B0,color:#CE93D8
```

---

### 6D — Chain-01 Full Traceability: From CVE to Evidence

This is the most important chain in the mission. Every arrow here is a relationship that exists in the dual graph — followable from the report all the way back to the raw evidence file.

```mermaid
flowchart LR
    CVE["🚨 ASG\nVulnerability node\nCVE-2022-21661\nCVSS: 8.8\nPoC: Exploit-DB ✓"]

    CH["🟡 APG\nAttackChain: Chain-01\nrisk_score: 9.1\nstatus: VALIDATED\nstarts_at → CVE-2022-21661"]

    S1["🟡 APG\nChainStep 1\nSQLMap → WP_Query SQLi\nstatus: VALIDATED"]
    S2["🟡 APG\nChainStep 2\nSQLMap dump → hash cracked\nstatus: VALIDATED"]
    S3["🟡 APG\nChainStep 3\nMetasploit → Web shell\nstatus: VALIDATED"]
    IMP["🟣 APG\nImpact\nRCE on shopvault.io\nCustomer PII accessible"]

    EV1["📎 ASG\nEvidence\nsqli-extraction.txt"]
    EV2["📎 ASG\nEvidence\nuser-table-dump.png"]
    EV3["📎 ASG\nEvidence\nwebshell-rce.png"]

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
| **All tool calls gated** | SQLMap and Metasploit both went through Commander Mailbox — no exploitation without approval |
| **Chain-03 RULED_OUT** | The system correctly diagnosed WAF protection and stopped after 3 retries — not an infinite loop |
| **risk_score escalated** | Chain-01 started at 8.8 (CVSS); after RCE was confirmed, Commander escalated to 9.1 |
| **Traceability** | Every Impact claim links through ChainSteps back to Evidence files in the ASG |
| **Dual termination** | Mission ended because 98 nodes explored AND 3/3 chains terminal — not because a timer fired |

---

## Module 08 — Complete ✅

All 6 diagrams are now in this file:

| # | Diagram | What It Shows |
|---|---------|---------------|
| 1 | System Architecture | 3-tier swim-lane: Orchestration → Dual-Graph → Agents+Tools |
| 2 | Dual-Graph Model | ASG node tree (9 types) + APG chain lifecycle (3 chains) |
| 3 | Agent Spawn Lifecycle | Sequence diagram + spawn package + 3 isolation properties |
| 4 | Tool Risk Gate | Full decision tree + LLM classifier internals + 6 hooks timeline |
| 5 | Planning Cycle | Core loop + re-plan triggers + dual termination + compaction |
| 6 | shopvault.io Walkthrough | Phase-by-phase timeline + Commander log + traceability chain |
