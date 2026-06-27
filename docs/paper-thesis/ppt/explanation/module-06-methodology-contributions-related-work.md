# Module 06 — Methodology-as-Configuration, Research Contributions, and Related Work

---

## 🎯 One-Line Summary

CMatrix encodes its entire assessment methodology as a swappable configuration document, has 12 distinct research contributions, and stands on the shoulders of 8 prior works — each with a specific, traceable influence.

---

## 📜 Methodology-as-Configuration — The VAPT Protocol Prompt

In traditional security tooling, the assessment methodology is hardcoded into the software. Want to follow OWASP Testing Guide instead of PTES? You need a new tool, or at minimum a new codebase.

CMatrix takes a radically different approach: **the methodology itself is a configuration document.**

The **VAPT Protocol Prompt** is a structured, versioned natural language document injected into the Commander's reasoning context. It defines everything about how the Commander plans and makes decisions:

- **Phase sequencing rules** — which activities come first, in what order
- **Transition conditions** — when is Phase 1 complete? When does Phase 2 begin?
- **Re-planning triggers** — which ASG state changes force a new plan?
- **Termination conditions** — when has the assessment achieved its goals?
- **Tool selection heuristics** — which tools are appropriate for which ASG node types?
- **Risk escalation rules** — when does something need Commander-level approval?

Different Protocol Prompt versions implement different methodologies:
- **OWASP Testing Guide** — systematic coverage of OWASP Top 10 and Web Testing Guide
- **PTES (Penetration Testing Execution Standard)** — full-lifecycle methodology
- **Custom red-team workflow** — client-specific scope and priority rules

**Swapping methodologies requires only swapping the Protocol Prompt document.** Zero changes to orchestration code, agent logic, or tool adapters.

### Why This Is a Research Contribution

This creates a unique research capability: you can **benchmark the effect of methodology choice on assessment outcomes** as an independent variable. Run CMatrix against the same target under OWASP Testing Guide and under PTES. Compare the results. The architecture is identical; only the methodology document differs. This kind of controlled comparison has never been possible before with automated VAPT systems.

---

## 🔬 The 12 Research Contributions (C1–C12)

These are the specific, novel claims CMatrix makes about what it contributes to the field. You should know what each one is and be able to explain it.

---

### C1 — Dual-Graph World Model with Strict Write Ownership

**What it is:** Two strictly separated graph structures — ASG for discovered reality, APG for inferred opportunity — with enforced write boundaries. Discovery agents write only to ASG. Commander writes only to APG. No agent conflates fact-collection with attack-chain inference.

**Why it matters:** Existing systems mix facts and hypotheses in shared memory. This creates a class of errors CMatrix eliminates entirely.

---

### C2 — Graph-State-Driven Dynamic Re-Planning

**What it is:** The Commander re-plans on explicit, graph-grounded triggers (new Vulnerability node seeds a chain; chain validation status changes; chain is ruled out) — not on fixed schedules or task completion.

**Why it matters:** Every re-plan has a formal, inspectable cause. Re-planning is predictable and auditable, not arbitrary.

---

### C3 — APG Attack Chain Lifecycle with Evidence Traceability

**What it is:** Attack chains are first-class entities with risk scoring, prioritization, and lifecycle-tracked validation (`HYPOTHESIZED` → `PARTIALLY_VALIDATED` → `VALIDATED` / `RULED_OUT`). Every ChainStep is linked to proof via `supported_by` edges to ASG Evidence nodes.

**Why it matters:** Every validated attack chain is fully traceable end-to-end from discovery to proof. No black boxes.

---

### C4 — ASG-Aware Parallel Tool Dispatch

**What it is:** Dependency-safe concurrent tool execution using the ASG itself as the dependency graph — not a separately maintained task scheduler.

**Why it matters:** The ASG already encodes what depends on what (you can't scan a Service before you discover its Port). Using the ASG as the scheduler eliminates an entire category of scheduling logic and keeps everything consistent with the world model.

---

### C5 — Tool Risk Gate with Commander-Mailbox Approval

**What it is:** Every tool call is classified into a risk tier before execution. High-risk calls require explicit Commander approval through a mailbox mechanism. The mailbox doubles as a zero-code insertion point for human-in-the-loop supervision.

**Why it matters:** No irreversible offensive operation can execute without Commander-level validation. Human oversight is a configuration, not an architectural redesign.

---

### C6 — ASG-Backed Lossless Context Compaction

**What it is:** A three-layer compaction scheme (MicroCompact → AutoCompact → FullCompact) in which FullCompact reduces conversation history to near-zero without losing any findings, because every discovery already lives in the ASG.

**Why it matters:** CMatrix can run indefinitely on large targets without context degradation. No other general-purpose agent can claim lossless compression because their findings only exist in conversation history.

---

### C7 — Methodology-as-Configuration via the VAPT Protocol Prompt

**What it is:** The Commander's planning policy is encoded as a versioned natural-language document. Different methodologies (OWASP Testing Guide, PTES, custom) can be benchmarked as independent research variables.

**Why it matters:** First time assessment methodology itself becomes a controlled, independently evaluable experimental variable.

---

### C8 — Dual-Graph Termination Semantics

**What it is:** Mission completion is formally defined as the conjunction of ASG exhaustion (no unexplored nodes) AND APG resolution (all chains in terminal state). Neither condition alone is sufficient.

**Why it matters:** The first formally grounded termination condition in autonomous VAPT literature. Neither pure task-queue systems nor pure graph-traversal systems can express both simultaneously.

---

### C9 — Live Vulnerability Intelligence Grounding via Scoped Research Agent

**What it is:** Real-time CVE enrichment, PoC availability assessment, and exploit feasibility research from authoritative sources (NVD, Exploit-DB, GitHub) during active assessment, written back to the ASG as structured Vulnerability node attributes.

**Why it matters:** Closes the stale-knowledge gap. Systems that reason only from pre-trained LLM knowledge may have outdated CVE information. CMatrix grounds every vulnerability finding in current intelligence.

---

### C10 — Cross-Mission Experience Store

**What it is:** A persistent, RAG-backed knowledge base of validated exploitation outcomes accumulated across missions. Queried by Commander at mission start to seed candidate AttackChains from prior validated patterns on analogous target stacks.

**Why it matters:** Generalizes AutoAttacker's within-mission experience-reuse mechanism to cross-mission scope. Every completed mission makes future missions on similar targets faster and more accurate. *(Note: the cross-mission accumulation is the contribution; the reuse concept originates with AutoAttacker.)*

---

### C11 — Attack Strategy Library with Technology-Fingerprint-Indexed Crystallization

**What it is:** When the same technology fingerprint produces validated AttackChains across two or more independent missions, the Commander crystallizes those outcomes into a named, parameterized attack strategy with a confidence score. Strategies are retrieved at mission start and injected as pre-ranked APG AttackChain seeds.

**Why it matters:** No existing autonomous VAPT system accumulates and generalizes validated exploitation procedures across sessions. Every prior system resets to zero knowledge on each mission. CMatrix becomes measurably more efficient on repeat target-type engagements — with a direct experimental evaluation path on HTB/THM machine families sharing technology fingerprints.

---

### C12 — Structured Engagement Trajectory Export

**What it is:** Every mission produces a complete machine-readable decision log capturing, for each planning cycle step: the ASG/APG trigger, Commander reasoning rationale, action taken, agent output summary, and strategy library hit status.

**Why it matters:** Serves three simultaneous purposes — full reproducibility of all benchmark claims; ablation study support (measure strategy library hit rate and planning-step reduction with/without C11); and a publicly releasable labeled dataset of autonomous VAPT reasoning sequences. This dataset type does not currently exist in the literature.

---

## 📚 Related Work — What CMatrix Learned From

CMatrix was designed with reference to five academic papers and three open-source systems. Here is each one with the specific mechanism it contributed.

---

### 1. PentestGPT (USENIX Security '24)

**Key idea:** Split the pipeline into Reasoning / Generation / Parsing modules. The Parsing module condenses raw tool output *before* it re-enters the reasoning context — keeping noisy terminal output from polluting strategic memory. Memory is maintained via a Pentesting Task Tree.

**CMatrix adaptation:** The "parse before you reason" instinct underlies the **Tool Adapter Layer**. Every tool's raw output is normalized into structured findings at the adapter boundary before anything reaches an agent's context. CMatrix extends this further: parsed results become **permanent ASG graph state** — surviving long after the conversation that produced them is gone.

---

### 2. AutoAttacker (arXiv '24, Xu et al.)

**Key idea:** Modular planner / summarizer / code-generator pipeline with an **experience manager** that stores executed attack subtasks and reuses them when constructing later, more complex attack chains — all within one mission.

**CMatrix adaptation:** The **Cross-Mission Experience Store (C10)** generalizes this from within one mission to across every mission ever run. The reuse concept originates with AutoAttacker; the cross-mission scope is CMatrix's addition.

---

### 3. Teams of LLM Agents / HPTSA (arXiv '24, Zhu et al.)

**Key idea:** Hierarchical planner that delegates to task-specific sub-agents. Central finding: injecting **task-specific documentation** directly into a sub-agent's context (rather than relying on pre-trained knowledge alone) improves zero-day exploitation performance by up to 2.1× over undocumented agents.

**CMatrix adaptation:** **Vulnerability-Class Knowledge Injection (§7)**. CMatrix injects curated offline expert documents (SQLi taxonomies, XSS payload patterns, OWASP checklists, Metasploit selection guides) into specialist agents at spawn time, matched to the vulnerability class they're assigned. Same pattern, applied to VAPT.

---

### 4. PentestAgent (AsiaCCS '25, Shen et al.)

**Key idea:** Planning agent paired with RAG-backed shared memory, plus an execution agent that on failure **self-diagnoses** the cause and corrects its approach before abandoning the attack path.

**CMatrix adaptation:** The **Validation Agent's self-debugging loop** (Diagnose → Contextualize → Adapt → Cap). CMatrix's Validation Agent follows the same sequence on a failed ChainStep — with the cap preventing infinite loops and the failure reason written to the ASG when the cap is reached.

---

### 5. VulnBot (arXiv '25, Kong et al.)

**Key idea:** Five-module pipeline (Planner, Memory Retriever, Generator, Executor, Summarizer) where the Summarizer condenses each phase's outcome before passing to the next role — preventing raw execution history from leaking between agents.

**CMatrix adaptation:** **Context-Isolated Agent Spawning (§7)**. Every CMatrix specialist agent returns only a structured ASG/APG delta to the Commander; its raw working context is discarded on completion. Agents hand off structured summaries, never raw history.

---

### 6. PentAGI (vxcontrol/pentagi)

**Key idea:** Production multi-agent pentesting platform with execution-pattern monitoring — an Adviser agent that detects repeated identical tool calls, and a Reflector that nudges stuck agents toward completion rather than letting them burn their budget.

**CMatrix adaptation:** **Cycle Guard and Reflector (§10)**. CMatrix detects fixation the same way: repeated identical or unproductive actions force re-planning; the Reflector provides corrective guidance on repeated tool-call failures.

---

### 7. Claude Code (Anthropic pattern)

**Key idea:** Two-stage fast-filter → chain-of-thought classifier (`yoloClassifier.ts`) for tool-call auto-approval. Plus a 27-event hook architecture giving operators named interception points throughout the agent loop.

**CMatrix adaptation — two distinct concepts:**
- **LLM Permission Classifier** — CMatrix's Medium-tier Risk Gate uses the same fast-filter + brief chain-of-thought pattern, evaluating scope alignment, chain intent, and parameter safety before returning `EXECUTE` or `ESCALATE`.
- **Agent Lifecycle Hook System** — CMatrix's six named hooks follow the same named-interception-point philosophy, scaled to CMatrix's dual-graph decision boundaries.

---

### 8. Hermes Agent (NousResearch/hermes-agent)

**Key idea:** Self-improving autonomous agent with closed learning loop — skill crystallization from completed tasks, stored and reused when contextually relevant. Plus structured trajectory export for SFT fine-tuning and RL training.

**CMatrix adaptation — two distinct concepts:**
- **Attack Strategy Library (C11)** — domain-constrained counterpart to Hermes's skill crystallization. CMatrix crystallizes validated attack chains into named, technology-fingerprint-indexed attack strategies. The generalization mechanism and confidence-scoring model both originate with Hermes's skill system.
- **Engagement Trajectory Export (C12)** — domain-adapted counterpart to Hermes's trajectory export. CMatrix logs every planning-cycle step as a structured trajectory entry adapted to the dual-graph event structure. The concept of deliberately structuring agent execution logs as training-data artifacts originates with Hermes.

---

## ✅ What You Should Remember From This Module

| Concept | Plain English |
|---------|---------------|
| VAPT Protocol Prompt | Methodology encoded as a swappable document — OWASP vs PTES vs custom, no code changes |
| C1–C12 | 12 specific novel contributions, each addressing a gap in prior work |
| Related work | 8 prior systems, each with a specific, traceable contribution to CMatrix's design |
| Provenance principle | CMatrix always credits where each idea came from and what exactly CMatrix added |

---

*End of explanation modules. See script.md for the presentation speaking script.*
