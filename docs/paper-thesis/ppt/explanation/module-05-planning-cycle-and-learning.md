# Module 05 — The Planning Cycle, Context Management, and Cross-Mission Learning

---

## 🎯 One-Line Summary

CMatrix runs a continuous observe → reason → plan → execute loop, manages memory intelligently across long sessions, and gets smarter across every mission it completes.

---

## 🔄 The Autonomous Planning Cycle

Every CMatrix mission runs on a single continuous loop. There's no fixed script, no predetermined sequence of tasks. The Commander reads the current state of the world (the dual graph), reasons about what's most important, acts on that reasoning, and repeats.

Here's the full cycle:

```
Observe ASG    → Read current ASG state — what has been discovered?
Observe APG    → Read AttackChain priorities and validation status — what's in progress?
Reason         → Identify unexplored ASG gaps; derive/update APG chains from new vulnerability nodes
Plan           → Decide: explore a new ASG gap OR validate the highest-priority APG chain
Spawn          → Spawn the appropriate context-isolated agent with a scoped ASG/APG slice
Gate           → Route any High-risk calls through the Tool Risk Gate for Commander approval
Execute        → Agent runs approved tools; structured output flows to ASG
Update ASG     → Agent writes discovered nodes and edges to the ASG
Update APG     → Commander derives new chains or advances existing chain validation status
Return         → Agent returns its structured delta; its working context is discarded
Re-Plan        → Commander re-reads the dual graph and decides the next action
```

Then repeat.

### What triggers a re-plan?

Not arbitrary schedules. Not timers. The re-plan is **graph-grounded** — it fires on explicit changes to the dual graph:

- A new ASG Vulnerability node appears → Commander evaluates whether it seeds a new APG chain
- An APG chain's `validation_status` changes (e.g., `PARTIALLY_VALIDATED`) → Commander re-prioritizes
- An APG chain is marked `RULED_OUT` → Commander moves to the next highest-priority chain
- A High-risk tool call is rejected → Commander adapts the plan

Every re-plan has a **formal, inspectable cause** — a specific graph event. This is what makes CMatrix's re-planning reliable and auditable, unlike systems that re-plan based on conversational state or arbitrary timeouts.

---

## 🏁 The Termination Condition — When Is the Mission Done?

This is one of CMatrix's most important contributions. How does an autonomous system know when it's actually finished?

Most existing systems use blunt criteria:
- Timer expired → stop
- Task queue empty → stop

These are poor proxies. A timer might expire before every attack path is explored. A task queue might empty even though new vulnerabilities are being discovered that weren't in the original queue.

CMatrix uses a **formally grounded dual termination condition**:

> **The mission terminates when AND ONLY WHEN:**
> 1. **ASG exhaustion:** No unexplored nodes remain in the ASG. Every discovered entity has been investigated.
> 2. **APG resolution:** All APG AttackChains are in a terminal state — either `VALIDATED` or `RULED_OUT`. No chain is still in `HYPOTHESIZED` or `PARTIALLY_VALIDATED` state.

Both conditions must be true simultaneously. This is the only mission-complete state.

Why is this dual condition significant? Because:
- A pure task-queue system can't express APG resolution — it has no concept of attack chains.
- A pure graph-traversal system can't express both simultaneously — it would exhaust the ASG graph but have no notion of attack path completeness.

CMatrix's termination is the first in the autonomous VAPT literature to be grounded in both dimensions at once.

A third, optional termination trigger: user-defined constraints (time limits, scope boundaries). But the *natural* termination is always the dual-graph condition.

---

## 🛡️ Cycle Guard and Reflector — Preventing Fixation

Long autonomous sessions can get stuck. An agent might repeat the same tool call over and over. A Validation Agent might keep retrying an exploit that was never going to work. Without guards, this burns time and budget with no progress.

CMatrix has two lightweight protective mechanisms:

### Cycle Guard

Monitors each agent's recent action history. If an agent issues the **same tool call** (same tool + same target + same parameters) more than a configurable number of times within a phase, the Commander forces a re-plan.

The key insight: repeated identical tool calls are a signal of **fixation**, not progress. Something is wrong. Better to re-plan than to let the agent spin in place.

### Reflector

Handles a different failure mode: when tool calls fail repeatedly but *differently* (distinct failures, not the exact same call). The Reflector issues **corrective guidance** to the agent on its next attempt — pointing at the specific failure pattern observed — rather than letting the agent retry blind.

Think of the Reflector as a coach who steps in and says: "Your last three attempts all failed because of authentication. Have you checked whether the target requires a token?"

Both mechanisms are evaluated against the agent's own recent action history — not the ASG/APG. This means they add no graph-write surface and cannot contaminate the graphs with diagnostic state.

---

## 🧠 ASG-Backed Context Management — Never Running Out of Memory

VAPT sessions are long. A thorough assessment of a large target might involve thousands of tool invocations, hundreds of findings, and many hours of continuous operation. LLM context windows have limits. Without active management, the context fills up and the system degrades or fails.

CMatrix's solution is grounded in a key architectural insight:

> **The ASG is a lossless persistent store of all discoveries. Conversation history is expendable. The ASG is not.**

Everything that matters — every discovered node, every vulnerability, every evidence artifact — is permanently stored in the ASG. The conversation history (tool call outputs, intermediate reasoning, agent exchanges) is scaffolding. Once findings are in the graph, the scaffolding can be compressed without losing anything.

CMatrix implements a **three-layer compaction system**:

### Layer 1 — MicroCompact (runs on every tool call)

When a tool's raw output is parsed by the Tool Adapter, only a compact summary enters the agent's working context. The full raw output is never stored in the context — only in the ASG.

*"We got 2,847 lines of Nmap output. What goes into context: a structured summary of 11 live hosts, 28 open ports, and detected services. The rest is discarded."*

### Layer 2 — AutoCompact (triggers at 60% context capacity)

When the conversation history reaches 60% of the context window, older turns are summarized via a separate, scoped LLM call. The summary replaces the stale history. The agent's primary reasoning thread continues without interruption.

*"We've accumulated a lot of history. Summarize turns 1-50 into a compact state snapshot, then discard them."*

### Layer 3 — FullCompact (triggers at 85% context capacity)

The entire conversation history is replaced. The agent's context is reconstructed from:
- The current ASG snapshot (all discovered nodes and edges)
- Current APG priority chains and their statuses
- The last N tool results

Nothing else is needed. Everything important is in the graph.

**The critical property:** Because all discoveries live in the ASG, FullCompact loses **zero intelligence** — only the conversational scaffolding that produced it.

No general-purpose agent can claim this property. CMatrix can compress conversation history to near-zero and lose nothing, because the dual graph is the source of truth — not the context window.

### Single LLM API — One Model, Many Scopes

CMatrix never routes calls to different models for different tasks. Everything — Commander reasoning, agent execution, MicroCompact summarization, Research Agent output normalization, Permission Classifier evaluation — goes through **the same configured LLM API**.

What changes between calls is the **scope of the prompt**, not the model:

| Task | Call type |
|------|-----------|
| Commander reasoning, chain scoring | Full-context call against the dual graph |
| AutoCompact/MicroCompact summarization | Narrow-scope call, constrained to summarization |
| Research Agent output normalization | Narrow-scope call constrained to the ASG Vulnerability schema |
| Permission Classifier evaluation | Narrow-scope call constrained to `EXECUTE` / `ESCALATE` |

This design keeps evaluation honest: every result is attributable to one model under one configuration. No hidden quality trade-offs from silently routing some calls to cheaper models.

---

## 🌐 Cross-Mission Experience Store — The System Remembers

The ASG and APG are per-mission structures. When a mission ends, they're closed. The next mission starts fresh. This is by design — different targets need different graphs.

But this creates a waste: all the valuable intelligence from successful exploitations just... disappears. The next mission against a similar target (say, another WordPress 5.9.x deployment) has to rediscover everything from scratch.

The **Cross-Mission Experience Store** solves this. It is a persistent, RAG-backed knowledge base that **survives across missions**.

### What Gets Written to It

At mission close, the Report Agent writes a structured summary of every validated APG AttackChain:
- Target technology fingerprint (CMS, framework, version, service)
- Vulnerability class and CVE
- Successful tool invocations and exact parameters
- ChainStep sequence that achieved validation
- Mission outcome summary

### When Is It Read

At mission start, **immediately after the Recon Agent writes the first batch of Technology nodes to the ASG** (and before the Analysis Agent begins deep enumeration), the Commander queries the store.

It retrieves exploitation records from past missions on similar technology stacks and injects them as **candidate chain hypotheses** — pre-validated patterns — into the Commander's reasoning context.

The Commander then evaluates these against the current ASG before seeding new APG AttackChains. Instead of starting from zero, it can front-load high-probability chains that have worked before.

**Analogous inspiration:** AutoAttacker (arXiv '24) introduced an experience manager that stores and reuses attack subtasks *within one mission*. CMatrix generalizes this to a *cross-mission* scope — the reuse concept comes from AutoAttacker, but the cross-mission accumulation is CMatrix's contribution.

---

## 🏆 Attack Strategy Library — Wisdom, Not Just Memory

The Cross-Mission Experience Store is raw memory — specific tool parameters, exact chain outcomes, per-mission records. Useful, but granular.

The **Attack Strategy Library** is a higher-order abstraction: **generalized, named, reusable attack procedures** distilled from patterns across multiple missions.

### How Crystallization Works

When the same target fingerprint (e.g., `WordPress 5.x + WooCommerce + Nginx`) produces a validated AttackChain across **two or more independent missions**, the Commander triggers crystallization.

A scoped LLM call generalizes the specific parameters of those chains into a **named attack strategy**:
- A parameterized procedure with known entry conditions
- The tool sequence that works
- Expected evidence artifacts
- A confidence score based on how many missions contributed

Example: `STRAT-WP-SQLI-001` — "WordPress SQL injection via WP_Query, confirmed across 4 missions with CVSS 8.8, exploit available in Metasploit."

### How It's Used

At mission start, after querying the Cross-Mission Experience Store, the Commander also retrieves matching Attack Strategies for discovered technology fingerprints. Strategies are injected as **pre-ranked APG AttackChain seeds** — prioritized *above* zero-prior chains because they carry a validated track record, not just CVE severity scores.

### The Distinction

| | Cross-Mission Experience Store | Attack Strategy Library |
|---|---|---|
| Granularity | Per-mission, per-chain raw records | Generalized across multiple missions |
| Content | Specific tool parameters, exact outcomes | Parameterized procedures, confidence scores |
| Query trigger | After Recon writes Technology nodes | Same time as Experience Store |
| Write trigger | Every validated chain at mission close | When ≥2 missions share same fingerprint |

### Why This Matters

> No existing autonomous VAPT system accumulates and generalizes validated exploitation procedures across sessions. Every system in the prior literature resets to zero knowledge on each mission.

CMatrix's Attack Strategy Library makes the system **measurably more efficient on repeat target-type engagements**. If it has exploited WordPress SQL injection three times before, the fourth time starts with a pre-validated strategy at high confidence — not a blank page.

This is the autonomous VAPT equivalent of a human pentester who gets better at their job with every engagement they complete.

---

## 📊 Engagement Trajectory Export — Every Mission Documented

Every CMatrix mission produces a **structured engagement trajectory** — a complete, machine-readable log of every decision step from mission start to termination.

Each log entry records:
- The ASG node or APG chain that triggered this decision
- What the ASG and APG looked like at this moment (deltas)
- The Commander's reasoning rationale
- The action taken (spawn agent, approve tool, re-plan, terminate)
- The agent's output summary
- Whether a strategy from the Attack Strategy Library was used

**Why this matters:**

| Use | How the trajectory supports it |
|-----|-------------------------------|
| **Reproducibility** | Any mission can be re-run deterministically; reviewers can verify every claim |
| **Ablation studies** | Compare trajectories with/without Attack Strategy Library — measure exactly how much it helps |
| **Failure analysis** | Steps where Commander re-plans after `RULED_OUT` expose recovery behavior precisely |
| **Dataset generation** | Trajectories are labeled VAPT reasoning sequences usable as SFT training data |
| **Benchmark auditing** | HTB/THM benchmark results are fully auditable, not just final outcome metrics |

The trajectory export runs as a side-effect hook registered on `PostMissionTerminate` and `PostAPGUpdate` — it adds no overhead to the critical path.

The corpus of trajectories across all benchmark missions is itself a research contribution: a publicly releasable, labeled dataset of autonomous VAPT reasoning sequences. **No such dataset currently exists in the literature.**

---

## ✅ What You Should Remember From This Module

| Concept | Plain English |
|---------|---------------|
| Planning cycle | Observe → Reason → Plan → Execute → Re-Plan, continuously, driven by graph events |
| Termination | Ends ONLY when ASG is exhausted AND all APG chains are in terminal states |
| Cycle Guard / Reflector | Detect fixation and correct stuck agents before they burn their budget |
| Context compaction | 3-layer system lets CMatrix run indefinitely — ASG is the lossless memory store |
| Cross-Mission Experience Store | Persistent RAG store of validated exploitation outcomes across missions |
| Attack Strategy Library | Crystallized, generalized attack procedures indexed by target technology fingerprint |
| Trajectory export | Machine-readable decision log — enables reproducibility, ablation, and dataset generation |

---

*Next: Module 06 — Methodology-as-Configuration and Research Contributions*
