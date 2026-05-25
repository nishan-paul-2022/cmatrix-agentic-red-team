# [STEP 2c] — Related Work Map — OUTPUT ARTIFACT

## 1) Summary
This sub-step synthesized the research findings from [STEP 2a] and [STEP 2b] into a structured taxonomy of the current LLM security landscape. We categorized the research into four thematic pillars: Autonomous VAPT Agents, Advanced Reasoning Patterns, Adversarial Benchmarking, and Agentic Defensive Frameworks. We created the first LaTeX asset, `table-01-related-work-comparison.tex`, which positions CMatrix as the first system to integrate composite reasoning (ToT + ReWOO + Reflexion) with a formal HITL safety gate for end-to-end security assessment.

## 2) Full Output

### 2.1 Categorized Taxonomy of Related Work

#### Category 1: Autonomous VAPT & Red Teaming Agents
- **Prior Work:** *PentestGPT (USENIX '24)*, *AutoAttacker (NeurIPS '24)*, *HackingBuddy (ESEC/FSE '23)*.
- **What they do:** Use LLMs to automate penetration testing by maintaining a task tree (PentestGPT) or using experience management (AutoAttacker).
- **Shortcomings:** They largely rely on simple ReAct or CoT reasoning, which is inefficient for long-horizon planning and lacks deliberate strategy selection.

#### Category 2: Advanced LLM Reasoning Patterns
- **Prior Work:** *Tree of Thoughts (NeurIPS '23)*, *ReWOO (NeurIPS '23)*, *Reflexion (NeurIPS '23)*.
- **What they do:** Introduce multi-path exploration (ToT), decoupled planning (ReWOO), and verbal reinforcement learning (Reflexion) for general-purpose LLM tasks.
- **Shortcomings:** These patterns have not been empirically validated or composed in the context of operational cybersecurity assessment with real-world side effects.

#### Category 3: Adversarial Robustness & Jailbreak Benchmarking
- **Prior Work:** *JailbreakBench (2024)*, *HarmBench (2024)*, *Jailbreak-Zero (NeurIPS '25)*.
- **What they do:** Provide standardized datasets and metrics to evaluate model robustness against "harmful" prompts and jailbreak attempts.
- **Shortcomings:** They focus on "saying no" to harmful requests rather than "doing safely" in a technical, tool-enabled environment.

#### Category 4: Agentic Security & Defensive Frameworks
- **Prior Work:** *AgentSentinel (ACM CCS '25)*, *Cloak, Honey, Trap (USENIX '25)*.
- **What they do:** Propose real-time monitors and deceptive environments to neutralize malicious agents.
- **Shortcomings:** They treat agents as potential threats to be trapped rather than as internal tools to be formally governed via risk-based authorization.

### 2.2 Clear Positioning Statement
CMatrix occupies the intersection of **Autonomous VAPT** and **Advanced Reasoning**. While prior VAPT tools focus on context maintenance, CMatrix is the first to apply a **composite reasoning suite** (ToT + ReWOO + Reflexion) specifically to security attack chains. Furthermore, we bridge the gap between "Red Teaming" and "Safety" by integrating a **formal risk-based HITL safety gate** directly into the stateful orchestration loop, a feature currently absent in all identified autonomous attack frameworks.

### 2.3 Comparison Table Draft (LaTeX Asset)
The comparison table compares CMatrix against 5 top competitors across 6 dimensions:
- **Autonomy**: Level of human intervention required.
- **Planning**: Mechanism for multi-step task decomposition (ReWOO vs. Static vs. None).
- **Reasoning**: Specific pattern used (ToT vs. ReAct vs. CoT).
- **Safety Gate**: Presence of a formal HITL or risk-based authorization mechanism.
- **VAPT Scope**: Target domain (Web, Post-Breach, OS, End-to-End).
- **Repo**: Availability of open-source code for verification.

## 3) Key Decisions Made
- **Ablation Focus**: Decided that the positioning statement must emphasize the *composition* of the three reasoning patterns as our primary technical novelty.
- **Baseline Selection**: Chose *PentestGPT* as the primary competitor due to its USENIX '24 prestige and similar modular architecture.
- **Table Formatting**: Used `booktabs` (`\toprule`, `\midrule`, `\bottomrule`) to ensure submission-ready LaTeX quality from the start.

## 4) Open Questions
- **Benchmark Realism**: How should we justify the "End-to-End" scope of CMatrix in the evaluation section compared to the narrower scopes of competitors?
- **Safety Metric**: Is there a published metric for "safety gate effectiveness" that we can use to compare against AgentSentinel?

## 5) Checklist Results (PASS/FAIL)
- [PASS] All papers from 2a and 2b are categorized
- [PASS] At least 4 distinct thematic categories identified
- [PASS] Each category has a clear "gap" statement
- [PASS] Our work is explicitly positioned against each category
- [PASS] `table-01-related-work-comparison.tex` created in `assets/` with real data
- [PASS] Table uses booktabs formatting
- [PASS] Table has proper `\caption{}` and `\label{}`
- [PASS] `ASSET-INDEX.md` updated
- [PASS] The map is ready to serve as the basis for the Related Work section (Step 6b)

## 6) Input for Next Step (Step 3a)
- **Novelty Extraction**: Use the "Shortcomings" listed in 2.1 to define the "Strong" novelty points in 3a.
- **Threat Model Context**: Use Category 4 (Defensive Frameworks) to define the adversarial assumptions for the threat model in 3c.

## 7) Asset Files Created
- `paper-research/paper-04-agent-reasoning/assets/table-01-related-work-comparison.tex`: Comparison table.
- `paper-research/paper-04-agent-reasoning/assets/ASSET-INDEX.md`: Updated index.
