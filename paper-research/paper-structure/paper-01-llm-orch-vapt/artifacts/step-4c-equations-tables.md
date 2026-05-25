# [STEP 4c] — Equation & Table Plan

## Summary
Completed the final layer of the paper architecture by defining the required mathematical equations and technical tables. These assets provide the quantitative rigor and comparative data needed for an IEEE S&P publication. The plan includes formalizing the **DCAT Optimization Objective** and the **SSC Similarity Threshold**, along with comparative benchmarks against state-of-the-art frameworks.

## Full Output

### 1. Table List

#### Table I: LLM Provider Performance Benchmarks
- **Section**: §VII Experimental Evaluation
- **Type**: LaTeX Table (Booktabs)
- **Content**: Comparison of 6–8 LLM backends (e.g., Gemini 1.5 Pro/Flash, GPT-4o, Claude 3.5, Llama-3-70B, Groq-Mixtral) across:
  - Reasoning Success Rate (%)
  - Average Latency (s)
  - Cost per 1M Input/Output Tokens ($)
  - Complexity Suitability (Flash/Pro/Reasoning)
- **Goal**: Provide the baseline data for the routing tier selection.

#### Table II: Agent Specialization and Resource Allocation
- **Section**: §IV System Architecture
- **Type**: LaTeX Table (Booktabs)
- **Content**: Breakdown of the 7 implemented agents (Network Security, Web Security, Vulnerability Intel, Auth, Config, API, Command Exec):
  - Primary Domain
  - Integrated Tools
  - Default Reasoning Tier
  - Context Management Strategy
- **Goal**: Detail the multi-agent hierarchy and agent specialization.

#### Table III: Comparative Framework Analysis
- **Section**: §II Background / §VIII Discussion
- **Type**: LaTeX Table (Booktabs)
- **Content**: Comparison of LLMOrch-VAPT against PentestGPT, AutoAttacker, and PentestMCP across:
  - Provider-Agnosticism
  - Autonomous Failover (APF)
  - Cost-Complexity Tiering (DCAT)
  - Semantic Caching (SSC)
  - HITL Safety Governance
- **Goal**: Explicitly demonstrate the novelty and technical superiority.

### 2. Equation List

#### Eq. 1: Task Complexity Signal ($C_t$)
- **Context**: Used in §V-A for Tier Selection.
- **Formulation**: $C_t = \sum (w_i \cdot k_i) + \delta_{cve} + \delta_{exp}$, where $w_i$ are keyword weights and $\delta$ are binary indicators for CVE-IDs or Exploit-DB entries.
- **Goal**: Mathematically define the "Complexity Signal" used for routing.

#### Eq. 2: Cost-Reasoning Optimization Objective ($\mathcal{J}$)
- **Context**: Used in §V-C for Methodology.
- **Formulation**: 
  $$\mathcal{J} = \arg \max_{m \in \mathcal{M}} \{ Q(m, t) \} \text{ subject to: } \text{Cost}(m) \leq B, \text{Latency}(m) \leq \mathcal{L}_{max}$$
  where $Q$ is predicted quality, $B$ is budget, and $\mathcal{L}$ is latency limit.
- **Goal**: Formalize the core optimization problem solved by LLMOrch-VAPT.

#### Eq. 3: Semantic Cache Similarity Function ($\sigma$)
- **Context**: Used in §V-B for Security-Semantic Caching.
- **Formulation**: $\sigma(q_{new}, q_{cached}) = \frac{\mathbf{e}_{new} \cdot \mathbf{e}_{cached}}{\|\mathbf{e}_{new}\| \|\mathbf{e}_{cached}\|} \geq \tau_{sim}$
- **Goal**: Define the threshold-based retrieval for SSC.

#### Eq. 4: MTTR Resilience Metric
- **Context**: Used in §VII-B for Failover Results.
- **Formulation**: $T_{recovery} = T_{resume} - T_{failure} \approx \Delta t_{detect} + \Delta t_{checkpoint} + \Delta t_{switch}$
- **Goal**: Provide a formal metric for the "Operational Resilience" contribution.

## Key Decisions Made
- Opted for a **Multi-Constraint Optimization** formula for Eq. 2 to highlight the complexity of the routing task.
- Decided to include a **Complexity Suitability** column in Table I to directly link the benchmark data to the DCAT methodology.
- Standardized all tables to use the `booktabs` package for a premium, academic appearance.

## Open Questions
- Should we include a table of the 1,500 evaluation tasks by category? (Decided: Place this in the Appendix to save space in the main body).

## Checklist Results
- [PASS] Step 4b figure plan used as input
- [PASS] 2–4 high-impact tables planned
- [PASS] 3–5 rigorous equations planned
- [PASS] All tables have titles, placement, and content descriptions
- [PASS] All equations have contexts and variable definitions
- [PASS] All RQs are supported by at least one table or equation
- [PASS] Artifact saved as `artifacts/step-4c-equations-tables.md`

## Input for Next Step
Synthesis of all architecture plans (4a, 4b, 4c) into the actual generation of assets (Step 5). This marks the transition from planning to creative implementation.
