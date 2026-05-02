# Research Area 3: Advanced Reasoning Patterns in Security Agents (ToT + ReWOO + Self-Reflection)

## [A] Research Area Overview

### What is this research area?

Imagine you're a general planning a military campaign. A naive approach is to react moment-to-moment: encounter an obstacle, decide what to do, move, repeat. But a good general thinks ahead: "I'll consider three different approaches, evaluate their tradeoffs, pick the best one, then plan the full sequence of maneuvers before moving a single soldier." This is exactly what advanced reasoning patterns bring to AI agents.

**Tree of Thoughts (ToT)** says: before committing to an approach, generate N candidate strategies and pick the best one. **ReWOO (Reasoning Without Observation)** says: generate a complete execution plan upfront so you don't waste LLM calls re-reasoning between every step. **Self-Reflection** says: after you execute, critique your own work and automatically fix gaps.

In security assessment, these patterns translate to:
- ToT: Should I do a fast scan, a stealth scan, or a comprehensive scan? (Choose before acting)
- ReWOO: Plan all 6 steps of a full pentest before running any of them
- Self-Reflection: I ran a port scan but missed the vulnerability check — let me auto-correct

### Why does it matter RIGHT NOW in 2025–2026?

- **LLM API costs are significant**: Every chain-of-thought loop costs money. ReWOO's claim of 40%+ reduction in LLM calls is an enormous economic incentive for real deployments.
- **Security assessment quality is high-stakes**: Unlike a chatbot giving a wrong movie recommendation, a security agent that misses a critical CVE can result in a breach. Self-reflection addresses this directly.
- **Complexity of security tasks requires planning**: Modern penetration tests involve dozens of sequential steps where order matters (you can't exploit a service you haven't discovered). ReWOO's dependency-aware planning is architecturally suited for this.
- **The research community is actively seeking domain-specific applications**: ToT and ReWOO papers exist, but their application to cybersecurity workflows is entirely unpublished.

### What is the core open problem?

**How do advanced reasoning patterns (designed for general-purpose LLM tasks) perform when applied to the specific constraints of cybersecurity assessment workflows — where steps have real side effects, ordering is critical, tools have authorization requirements, and quality metrics are domain-specific?**

---

## [B] Related Research Papers

### Paper 1: Tree of Thoughts: Deliberate Problem Solving with Large Language Models

- **Link**: [https://arxiv.org/abs/2305.10601](https://arxiv.org/abs/2305.10601)
- **Lead Author**: Shunyu Yao (Princeton) — [Google Scholar](https://scholar.google.com/citations?user=GfR-YZ4AAAAJ)
- **Summary**: Introduces ToT as a framework where LLMs maintain a tree of intermediate "thoughts" and can explore multiple reasoning paths simultaneously before committing to a solution. On the Game of 24 puzzle, ToT achieves 74% vs. 4% for standard chain-of-thought, showing the dramatic benefit of multi-path exploration before commitment.
- **Similarity to CMatrix**: CMatrix's `tree_of_thoughts.py` directly implements ToT for security strategy selection. The `evaluate_strategies()` method generates 3–5 candidate strategies (FAST_SCAN, STEALTH, COMPREHENSIVE, TARGETED, BALANCED), scores each against 5 evaluation criteria (speed, thoroughness, stealth, resource usage, success probability), and selects the optimal strategy before any tool execution begins.
- **Gap**: The original ToT paper applies to mathematical puzzles and creative writing. CMatrix applies ToT to **security assessment strategy selection** — a domain with real-world costs (slow comprehensive scans vs. fast partial scans) and adversarial constraints (stealth requirements). This is a novel application with security-specific evaluation criteria.

### Paper 2: ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models

- **Link**: [https://arxiv.org/abs/2305.18323](https://arxiv.org/abs/2305.18323)
- **Lead Author**: Binfeng Xu — [arXiv](https://arxiv.org/search/?searchtype=author&query=Xu+Binfeng)
- **Summary**: ReWOO decouples planning from execution by having the LLM generate a complete plan with explicit inter-step dependencies (e.g., "#E2 depends on #E1") before any tool is called. The key finding: ReWOO reduces LLM calls by 40%+ and reduces token usage significantly compared to ReAct. The pre-generated plan also enables parallel execution of independent steps.
- **Similarity to CMatrix**: CMatrix's `rewoo.py` (677 LOC) implements the full ReWOO pattern with: `generate_plan()` → `_try_template_planning()` → `_llm_generate_plan()` → `_validate_plan()`. The `PlanStep.dependencies` field implements exactly the "#E1, #E2" reference system from the paper. Redis caching of plans for similar tasks is an additional optimization not in the original paper.
- **Gap**: The original ReWOO paper applies to Wikipedia QA and HotpotQA. CMatrix applies it to **sequential security assessment workflows** where plan steps have real side effects, inter-step data dependencies are security-meaningful (e.g., CVE search depends on service enumeration output), and plan templates for common attack patterns (network_scan, web_assessment, cve_research) can dramatically accelerate planning.

### Paper 3: Reflexion: Language Agents with Verbal Reinforcement Learning

- **Link**: [https://arxiv.org/abs/2303.11366](https://arxiv.org/abs/2303.11366)
- **Lead Author**: Noah Shinn — [arXiv](https://arxiv.org/search/?searchtype=author&query=Shinn+Noah)
- **Summary**: Reflexion enables LLM agents to learn from failure by verbally critiquing their own performance and using that critique to improve future attempts. Agents maintain an "episodic memory" of past reflections and use it to avoid repeating mistakes. On HotpotQA, Reflexion improves from 73% to 80% accuracy.
- **Similarity to CMatrix**: CMatrix's `reflection.py` (604 LOC) implements a direct port of Reflexion, but specialized for security assessment. The `_assess_quality()`, `_detect_gaps()`, and `_generate_improvements()` methods implement the Reflexion critique loop with security-specific gap categories (`missed_ports`, `missing_service_info`, `no_vulnerability_check`, `inconsistent_results`). The `MAX_REFLECTIONS = 2` limit prevents infinite loops.
- **Gap**: Reflexion was developed for text-based tasks. CMatrix adapts it for **structured security scan output critique** — where "gaps" are formally defined (missed CRITICAL_PORTS list, missing CVE search, inconsistent open_ports vs. services counts) and improvement actions are concrete tool re-invocations (`scan_network`, `search_cve`, `check_service_version`), not just rephrased prompts.

### Paper 4: Self-Refine: Iterative Refinement with Self-Feedback

- **Link**: [https://arxiv.org/abs/2303.17651](https://arxiv.org/abs/2303.17651)
- **Lead Author**: Aman Madaan — [Google Scholar](https://scholar.google.com/citations?user=0d5KfFkAAAAJ)
- **Summary**: Self-Refine shows that LLMs can iteratively improve their outputs by generating feedback on their own outputs and then refining based on that feedback. Without additional training, this achieves 20% average improvement across 7 diverse tasks (code, sentiment, dialogue, etc.).
- **Similarity to CMatrix**: CMatrix's `_llm_reflect()` in `reflection.py` invokes the LLM to generate natural-language reasoning about gaps and improvements, which is then converted into concrete tool calls in `_generate_improvements()`. This combines Self-Refine's natural language critique with executable improvement actions.
- **Gap**: Self-Refine produces refined *text output*. CMatrix produces refined *tool execution plans* — the reflection output drives new TOOL: calls that actually execute in the real world. This is a fundamentally more complex and more impactful application of the self-refine concept.

---

## [C] Our Codebase's Unique Contribution

### Relevant Modules

| Module | Role |
|--------|------|
| `app/services/reasoning/tree_of_thoughts.py` (693 LOC) | Strategy selection with 5 criteria × 5 strategy types |
| `app/services/reasoning/rewoo.py` (677 LOC) | Upfront planning with dependency tracking + Redis caching |
| `app/services/reasoning/reflection.py` (604 LOC) | Post-execution quality assessment + auto-correction |
| `app/services/orchestrator.py` L750–937 | Integration: strategy_selection → planning → agent → reflection |
| `app/services/orchestrator.py` L1064–1161 | Workflow graph: ToT → ReWOO → ReAct → Reflection |

### Abstract Draft

> We present the first empirical study of advanced LLM reasoning patterns — Tree of Thoughts (ToT), ReWOO, and Self-Reflection — applied to multi-step cybersecurity assessment workflows. While these patterns have been validated on academic benchmarks (Game of 24, HotpotQA, MBPP), their application to security tasks introduces novel challenges: tool execution has real-world side effects, inter-step dependencies carry security-meaningful data flows (CVE lookup depends on service version from port scan), and quality metrics must be domain-specific (missed critical ports, absent vulnerability checks). In CMatrix, we compose all three patterns into a sequential reasoning pipeline: ToT selects an assessment strategy before execution (fast/stealth/comprehensive/targeted/balanced), ReWOO generates a complete dependency-aware plan with Redis-cached templates for common attack patterns, and Self-Reflection critiques execution results and auto-generates corrective tool calls. We measure the combined effect on (1) LLM API call efficiency vs. pure ReAct, (2) security assessment completeness (rate of critical port coverage, CVE search inclusion), and (3) self-correction accuracy (rate at which auto-generated fixes address real gaps). Our results demonstrate that the combined reasoning pipeline reduces LLM calls by X% while improving assessment completeness by Y%, validating the transfer of these academic reasoning patterns to applied security workflows.

### Experiments We Can Run

1. **ReWOO call efficiency study**: Measure total LLM API calls for identical security targets using pure ReAct vs. ReWOO + ReAct. Use the `plan.confidence` and `plan.cached` fields as metrics.
2. **ToT strategy quality study**: For a given target, run all 5 strategy types and measure actual security findings against the ToT-predicted `success_probability` score. Does ToT's strategy selection correlate with actual outcomes?
3. **Reflection correction accuracy**: Track `reflection_count`, `quality_score`, `gaps`, and whether auto-corrective tool calls (`ImprovementAction.tool_name`) actually close the detected gaps.
4. **Plan template vs. LLM planning**: Measure plan generation latency and quality for `_try_template_planning()` vs. `_llm_generate_plan()`. Do templates produce equally good plans at much lower cost?
5. **Combined pipeline vs. ablations**: Compare assessment quality for: (a) pure ReAct, (b) ReWOO only, (c) Reflection only, (d) ToT + ReWOO + Reflection. Ablation studies are the standard way to prove individual contributions in ML papers.

---

## [D] Research Gaps We Can Fill

1. **Gap: No application of ToT to security strategy selection** — All ToT papers focus on text tasks. **We fill it** by applying ToT with security-specific strategy types (stealth, comprehensive, targeted) and evaluation criteria (stealth score, success probability, resource usage) derived from real pentesting practice.

2. **Gap: ReWOO not validated in agentic tool-use workflows with side effects** — ReWOO was validated on QA tasks where "observations" are text lookups. **We fill it** by applying ReWOO to security workflows where "observations" are real network scan outputs, CVE database queries, and authentication probes — with actual dependencies between steps.

3. **Gap: Self-reflection in security not producing executable corrections** — Reflexion produces refined text. **We fill it** by converting reflection output into structured `ImprovementAction` objects with specific `tool_name`, `parameters`, and `priority` fields that drive actual tool re-execution — closing the loop from critique to corrective action.

4. **Gap: No unified benchmark for combined reasoning patterns on security tasks** — Papers evaluate ToT, ReWOO, and Reflection separately. **We fill it** by running ablation studies of all three patterns and their combinations on standardized security assessment tasks.

5. **Gap: No Redis-cached plan reuse for recurring security scenarios** — **We fill it** with CMatrix's ReWOO plan caching: identical or similar tasks retrieve cached plans, dramatically reducing planning overhead for repeat assessments of similar infrastructure. This is a novel efficiency optimization not in any published ReWOO work.

---

## [E] Target Publication Venues

| Venue | Type | Tier | Relevance |
|-------|------|------|-----------|
| **NeurIPS** | Conference | A* | Advanced reasoning, LLM agents |
| **ICML** | Conference | A* | Machine learning, agents |
| **ACM CCS** | Conference | A* | Security + ML |
| **ICLR** | Conference | A* | Representation learning, agents |
| **EMNLP** | Conference | A | NLP, LLM reasoning |

### **Recommended Venue: ACM CCS 2026**

ACM CCS is uniquely positioned to receive a paper that combines ML reasoning advances with a security application. The conference explicitly covers "AI and ML for security" as a track. The paper's combined contribution — novel security application of ToT+ReWOO+Reflection with empirical ablations — fits CCS's expectation for technical depth and practical impact. The ablation study format is exactly what CCS reviewers look for in ML+security papers.

---

## [F] Quick-Reference Summary Box

| Item | Detail |
|------|--------|
| **Research area** | Advanced reasoning patterns (ToT, ReWOO, Reflexion) applied to security assessment |
| **Our codebase support** | **Strong** — all three patterns fully implemented and integrated into the workflow |
| **Novelty level** | **High** — first paper combining all three patterns in a security-domain agent |
| **Recommended venue** | ACM CCS 2026 |
| **Estimated effort to publish** | 4–5 months (ablation experiments + evaluation metrics + writing) |
| **Key differentiator** | Redis-cached ReWOO plans + security-specific gap taxonomy + executable correction actions |
