# Module 04 — The Tool Adapter Layer and Risk Gate

---

## 🎯 One-Line Summary

Every tool call in CMatrix goes through a **safety checkpoint** before it runs. Dangerous operations need the Commander's explicit approval — and in supervised mode, a human's too.

---

## 🏛️ Why Tools Need a Middleman

Imagine giving a junior analyst direct access to every weapon in the arsenal — SQL injection tools, exploit frameworks, network scanners — with no oversight. They could accidentally run a destructive exploit on a production server. They could scan systems outside the agreed scope. They could trigger an irreversible action based on a misread finding.

This is not hypothetical. These are real failure modes that happen in automated security tooling.

CMatrix solves this with a mandatory intermediary layer: the **Tool Adapter Layer**. Every single tool invocation — from a passive DNS lookup to a full Metasploit exploit — flows through this layer. Agents cannot invoke tools directly. Period.

---

## ⚙️ What a Tool Adapter Does

A Tool Adapter is a standardized wrapper around each security tool. It has three jobs:

1. **Execute** the tool with the parameters provided by the agent.
2. **Parse** the raw output (which can be thousands of lines of messy terminal text).
3. **Return** structured, normalized findings ready for ASG ingestion.

This single design decision has a cascading positive effect:

- **Agents reason about targets, not command syntax.** An agent doesn't need to know the exact command-line flags for Nmap version 7.94. It just requests a port scan on a given host. The adapter handles translation.

- **Tools can be swapped without touching agent logic.** If a better tool replaces Gobuster tomorrow, you update the adapter — not every agent that uses directory enumeration.

- **Raw tool output never reaches an agent's context.** Nmap can produce thousands of lines. ZAP can produce enormous XML reports. None of this noise enters the agent's reasoning context. Only the clean, structured extract does.

This is the same "parse before you reason" principle identified in PentestGPT (USENIX Security '24) — one of the key academic inspirations for CMatrix. The difference is that CMatrix extends it further: parsed output becomes **permanent graph state in the ASG**, not just a context summary.

---

## 🚦 The Tool Risk Gate — Three Tiers of Oversight

Every tool call, before it is passed to the Tool Adapter for execution, is classified into one of three risk tiers by the **Tool Risk Gate**. This is where safety happens.

### Tier 1 — Low Risk: Execute Immediately

**What falls here:** Passive discovery operations.
- Subdomain enumeration (Amass)
- Live host probing (httpx)
- Passive reconnaissance

**Handling:** Execute immediately after a lightweight scope check — is the target in declared scope? Is the tool authorized for this agent? If yes, proceed.

No additional approval needed. These operations don't modify the target, can't cause harm, and are reversible by nature.

---

### Tier 2 — Medium Risk: LLM Permission Classifier

**What falls here:** Active enumeration that probes the target but doesn't exploit it.
- Port scanning (Nmap)
- Directory brute-forcing (Gobuster, ffuf)
- Vulnerability template scanning (Nuclei)
- Active web application scanning (OWASP ZAP)

**Handling:** Before execution, the call is sent to an **LLM Permission Classifier** — a fast, narrowly-scoped call to the same configured LLM API, issued with a constrained classification-only prompt.

The classifier evaluates three things:

| Axis | Question |
|------|---------|
| **Scope alignment** | Does the target ASG node fall within the declared assessment scope? |
| **Chain intent** | Is this call consistent with the current APG AttackChain being pursued? |
| **Parameter safety** | Do the tool parameters show any patterns inconsistent with the authorized assessment mode? |

The classifier uses a fast-filter pass first (obvious safe/unsafe), then brief chain-of-thought reasoning for ambiguous cases. Its output is strictly binary: **`EXECUTE`** or **`ESCALATE`**.

If `EXECUTE` → the call proceeds to the Tool Adapter.
If `ESCALATE` → the call is routed to the Commander mailbox, treated as if it were High-risk.

**Why use an LLM classifier here instead of static rules?**

Static rules can't catch context-dependent problems. For example:
- A directory brute-force on `api.shopvault.io` might be in scope — or it might not be if only the main domain was authorized.
- An aggressive timing parameter in a Nmap scan might be fine in black-box mode — but might be out of bounds in a grey-box assessment where stealth was agreed upon.
- An attacker might try to manipulate a tool's parameters through a discovered web page (prompt injection via tool output) — the classifier catches this by evaluating whether the parameter set is consistent with the current chain intent.

The classifier is the layer that catches **adversarial prompt injection in tool parameters** and **scope drift in enumeration calls** — failure modes that static tier rules simply cannot detect.

---

### Tier 3 — High Risk: Commander Mailbox Approval

**What falls here:** Destructive, irreversible, or high-impact operations.
- SQL injection exploitation (SQLMap with data extraction)
- Exploit execution (Metasploit)
- Any operation that modifies the target or achieves code execution

**Handling:** The agent does not execute the tool. Instead, it deposits an **approval request** in the **Commander's mailbox**. The request contains:
- The tool name and full parameters
- The target ASG node
- The chain context (which APG AttackChain this serves)
- The rationale for this call

The Commander then evaluates the request:
- Is the target in scope?
- Is the CVE confirmed with sufficient evidence?
- Is this chain the highest priority one worth pursuing?
- Do the parameters look correct?

The Commander either: **approves** (call proceeds), **rejects** (call is cancelled, failure reason written to APG), or **modifies** (Commander adjusts parameters, then approves).

### The Human-in-the-Loop Insertion Point

Here's the elegant part. For supervised missions, a human operator can be **inserted at the Commander's mailbox**. Approval requests that would normally be auto-processed by the Commander's reasoning can instead be surfaced to a human for review and sign-off.

This enables human oversight without any change to agent logic. The agents don't know or care whether it's the Commander's LLM or a human analyst reading the mailbox. The interface is the same. The workflow is the same. Human-in-the-loop is a configuration, not a redesign.

---

## 🔒 The Non-Negotiable Safety Property

> **No irreversible offensive operation executes without Commander-level scope validation.**
> **No Medium-tier call executes without LLM classifier approval.**

This property is architectural, not policy. It cannot be bypassed by an agent — the Tool Adapter Layer is the only path to tool execution. If a call hasn't passed through the appropriate gate, it doesn't run.

---

## 🪝 The Agent Lifecycle Hook System

Beyond the Risk Gate, CMatrix exposes a set of **named lifecycle hooks** — formal interception points throughout the agent loop where external observers and operators can observe or modify system behavior without touching any agent or Commander logic.

Think of hooks like built-in power outlets in a wall. The wall doesn't change based on what you plug in. But you can plug in a lamp, a phone charger, or a sophisticated monitoring system — all without modifying the wall.

### The Six Hooks

| Hook | Fires When | What Operators Can Do |
|------|-----------|----------------------|
| `PreToolUse` | Before any tool call enters the Risk Gate | Inject additional scope checks; block specific tool+target combinations |
| `PostToolUse` | After tool output is written to ASG | Log raw outputs; trigger external alerts on specific findings |
| `PreAgentSpawn` | Before Commander spawns a specialist agent | Override agent context; inject additional ASG attributes |
| `PostAgentReturn` | After specialist agent returns its ASG delta | Validate returned nodes; reject malformed graph writes |
| `PreAPGUpdate` | Before Commander writes a new AttackChain to APG | External approval gate for autonomous chain creation |
| `PostMissionTerminate` | When dual-graph termination condition is met | Trigger report delivery; write to Cross-Mission Experience Store |

### How Hooks Work

Each hook receives a **structured event payload** and returns an **action directive**:
- `CONTINUE` — proceed normally
- `BLOCK` — stop the triggering action cleanly
- `MODIFY(payload)` — replace the payload before the action proceeds

Hook execution is synchronous — a `BLOCK` stops the action immediately; a `MODIFY` changes it before it continues.

**Real-world use cases for hooks:**
- A compliance team wants every High-risk tool approval logged to their SIEM → `PostToolUse` hook writes to external system.
- A CI/CD pipeline wants CMatrix to run on every release but require human approval for any chain that achieves RCE → `PreAPGUpdate` hook gates chain creation on external approval.
- An enterprise SOC wants real-time notifications when a new vulnerability is written to the ASG → `PostToolUse` hook triggers alerts.

The hook system is how CMatrix integrates into enterprise security operations pipelines — not through custom code, but through a standard event interface.

---

## ✅ What You Should Remember From This Module

| Concept | Plain English |
|---------|---------------|
| Tool Adapter | Mandatory intermediary — agents never touch tools directly; adapters parse raw output into structured ASG-ready data |
| Low risk | Passive tools — run immediately after scope check |
| Medium risk | Active tools — need LLM classifier to approve (catches scope drift and parameter injection) |
| High risk | Exploitation tools — need Commander mailbox approval; human can be inserted here |
| Lifecycle hooks | Named event points where operators can observe, block, or modify any significant system action |

---

*Next: Module 05 — The Autonomous Planning Cycle and Termination*
