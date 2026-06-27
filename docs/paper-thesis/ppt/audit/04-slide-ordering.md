# CMatrix Presentation Audit — 04: Slide Ordering

> Evaluation of the current slide sequence, swap recommendations, and the proposed corrected order.

---

## Current Slide Order (with problems annotated)

```
01  Title
02  The Problem                     ← Correct position
03  Novel Contribution (C1–C12)     ← ⚠️ TOO EARLY — terms undefined
04  System Architecture             ← Correct
05  Dual-Graph World Model          ← Correct
06  Agent Architecture              ← Correct
07  Agent Spawn Lifecycle           ← Correct
08  Offensive Tool Catalogue        ← ⚠️ Could move earlier (before agents)
09  Tool Adapter Layer / Risk Gate  ← Correct (after tools)
10  Real-World Scenario             ← Correct position (after all architecture)
11  Chain-01 Traceability           ← Correct (follows walkthrough)
12  Attack Chain Lifecycle          ← ⚠️ Should come BEFORE the walkthrough
13  Autonomous Planning Cycle       ← ⚠️ Should come BEFORE the walkthrough
14  Dual Termination + Compaction   ← ⚠️ Should come BEFORE the walkthrough
15  Cross-Mission Learning          ← ⚠️ Should come BEFORE the walkthrough
16  References                      ← Correct
```

---

## Core Ordering Problem: Architecture After Scenario

The most significant ordering defect is that slides 12–15 (attack chain lifecycle, planning cycle, termination, cross-mission learning) appear **after** the scenario walkthrough (slides 10–11).

This means the audience watches a detailed mission execution without having been shown:
- How the planning loop works (slide 13)
- What HYPOTHESIZED/VALIDATED/RULED_OUT means (slide 12)
- How the mission knows when to stop (slide 14)
- How the experience store is populated (slide 15)

All four of these concepts are *prerequisites* for understanding the walkthrough, not consequences of it.

---

## Secondary Problem: Contributions Before Architecture

Slide 3 presents C1–C12 before the audience has seen the ASG, the APG, the Commander, or any agent. Contributions like "C4: ASG-Aware Parallel Dispatch" and "C8: Dual-Graph Termination Semantics" are incomprehensible without the architectural context established in slides 4–14.

The contributions slide should appear **after** the audience understands what they are contributions to.

---

## Proposed Corrected Order

```
01  Title
02  The Problem                     ← Identifies gaps in existing systems
03  [NEW] Scope                     ← Defines what CMatrix targets and what it doesn't
04  System Architecture             ← Three-tier overview — establishes vocabulary
05  Dual-Graph World Model          ← ASG + APG — establishes core structures
06  Agent Architecture              ← Commander + 6 agents + context isolation
07  Agent Spawn Lifecycle           ← How agents are born, die, and pass state
08  Offensive Tool Catalogue        ← 11 tools — what agents operate
09  Tool Adapter Layer / Risk Gate  ← How tool calls are governed
10  Autonomous Planning Cycle       ← How the Commander loops
11  Attack Chain Lifecycle          ← Chain state machine + self-debug
12  Dual Termination + Compaction   ← When the mission ends + long-session stability
13  Cross-Mission Learning          ← Experience Store + Strategy Library + C12
14  Real-World Scenario             ← NOW the audience can follow the walkthrough
15  Chain-01 Traceability           ← Deepens the walkthrough with trace path
16  Novel Contribution (C1–C12)     ← NOW the audience understands each contribution
17  [NEW] Evaluation Plan           ← Benchmarking, metrics, ablation design
18  Inspirations & References       ← Related work acknowledgement
```

**Total slides in proposed order:** 18 (adds Scope and Evaluation Plan; all other slides retained)

---

## Rationale for Each Change

| Change | Reason |
|---|---|
| Scope slide inserted at position 3 | First thing a supervisor asks: "what's in scope?" |
| Architecture (slide 4) before Dual-Graph (slide 5) | 3-tier overview must precede deep-dive into one tier |
| Planning Cycle moved to position 10 | Required to understand the walkthrough at position 14 |
| Attack Chain Lifecycle moved to position 11 | Chain states (HYPOTHESIZED etc.) needed before walkthrough |
| Termination/Compaction moved to position 12 | Audience needs to know how mission ends before watching one end |
| Cross-Mission Learning moved to position 13 | Belongs with architecture, not after walkthrough |
| Scenario moved to position 14 | Now the audience has all prerequisites |
| Contributions moved to position 16 | Now functions as a synthesis/summary, not a teaser |
| Evaluation Plan inserted at position 17 | Required for any thesis presentation |
| References remain last | Correct academic convention |

---

## Slide Swap Analysis

| Swap | Benefit |
|---|---|
| Swap slides 3 (Contributions) ↔ end position | Transforms contributions from meaningless labels into earned conclusions |
| Swap slides 12–14 (Lifecycle/Cycle/Termination) before slide 10 (Scenario) | Makes the scenario comprehensible on first reading |
| Swap slides 13 (Planning) and 12 (Chain Lifecycle) | Planning cycle logically precedes chain state machine |

---

## What Must Not Change

| Slide | Current Position | Keep Because |
|---|---|---|
| Title | 1 | Correct |
| The Problem | 2 | Sets up motivation perfectly |
| System Architecture | 4 → 4 | Correct placement |
| Dual-Graph World Model | 5 → 5 | Correct after architecture overview |
| Agent Architecture | 6 → 6 | Correct tier-3 deep dive |
| Agent Spawn Lifecycle | 7 → 7 | Correct follow-on |
| Tool Catalogue | 8 → 8 | Correct after agents are established |
| Risk Gate | 9 → 9 | Correct after tool catalogue |
| References | 16 → 18 | Correct last position |
