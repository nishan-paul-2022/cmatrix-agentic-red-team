# [STEP 4b] — Figure Plan

## Summary
Defined the visual asset strategy for the LLMOrch-VAPT paper. Planned six high-impact figures to support the core technical claims and experimental results. All figures are designed to be implemented using TikZ or pgfplots to ensure perfect resolution and compliance with IEEE S&P standards.

## Full Output

### Figure List

#### Fig. 1: LLMOrch-VAPT System Architecture
- **Section**: §IV System Architecture
- **Type**: TikZ Block Diagram
- **Content**: A hierarchical view showing the **Master Supervisor** at the top, delegating tasks to **Worker Agents** (Network, Web, Intel, Auth, Config). Shows the **Unified Provider Protocol** as the abstraction layer between the agents and multiple heterogeneous backends (Gemini, GPT-4, Ollama, Groq).
- **Goal**: Visualize the "Master-Worker" hierarchy and the provider-agnostic decoupling.

#### Fig. 2: Dynamic Complexity-Aware Routing (DCAT) Workflow
- **Section**: §V Methodology
- **Type**: TikZ Flowchart
- **Content**: Input Task → **Complexity Analysis Engine** (Keyword/Signal extraction) → **Tier Logic** (Flash vs. Pro vs. Reasoning) → **Dynamic Model Selection** → Execution → Metadata Feedback Loop.
- **Goal**: Explain the methodology for cost-reasoning optimization.

#### Fig. 3: Autonomous Provider Failover (APF) State Machine
- **Section**: §IV System Architecture
- **Type**: TikZ State Diagram
- **Content**: States: [Initial Execution] → [Error Detected] → [State Checkpointing] → [Failover Triggered] → [Backend Swapping] → [Execution Resumed].
- **Goal**: Demonstrate the resilience mechanism and the <2s MTTR claim.

#### Fig. 4: Security-Semantic Caching (SSC) Mechanism
- **Section**: §V Methodology
- **Type**: TikZ Architectural Diagram
- **Content**: Security Query → **Embedding Generator** → **Vector Store (Qdrant)** → Similarity Check (Threshold $\tau$) → [Cache HIT: Return Cached Reason] / [Cache MISS: LLM Reasoning → Update Cache].
- **Goal**: Visualize the scalability and cost-saving contribution.

#### Fig. 5: Evaluation: Cost vs. Reasoning Success (RQ2)
- **Section**: §VII Experimental Evaluation
- **Type**: pgfplots Bar Chart (Double Y-Axis)
- **Content**: X-axis: Model Tiers (Flash, Pro, DCAT-Ours). Y1-axis: Success Rate (%). Y2-axis: Cost ($). 
- **Goal**: Provide the core evidence for the "84.2% cost reduction" and "97.4% success" claims.

#### Fig. 6: Operational Resilience: MTTR Analysis (RQ1)
- **Section**: §VII Experimental Evaluation
- **Type**: pgfplots Line Chart
- **Content**: A timeline of a simulated provider outage. Shows the performance drop at $T_0$ and the rapid recovery/failover to a backup provider by $T_{0+2s}$.
- **Goal**: Ground the MTTR claims in a clear temporal visualization.

### Asset Inventory Updates
The following entries will be added to `assets/ASSET-INDEX.md` in Step 5:
- `fig-01-architecture.tex`
- `fig-02-dcat-flow.tex`
- `fig-03-apf-state.tex`
- `fig-04-ssc-mechanism.tex`
- `fig-05-eval-metrics.tex`
- `fig-06-failover-timeline.tex`

## Key Decisions Made
- Prioritized **TikZ** for all architectural and logic diagrams to maintain a professional, academic look.
- Decided to use a **Double Y-axis** for Fig. 5 to clearly show the relationship between cost savings and performance maintenance.
- Grouped the figures to ensure at least one visual asset per primary Research Question.

## Open Questions
- Should we include a figure for the "Safety Gate" (RQ4)? (Decided: Subsume this into the Architecture diagram or use a small sidebar/caption in Section VI).

## Checklist Results
- [PASS] Step 4a structure used as input
- [PASS] 5–8 high-quality figures planned
- [PASS] Each figure has a title, section placement, and type
- [PASS] Each figure has a detailed description of content and goals
- [PASS] TikZ/pgfplots types are specified for all figures
- [PASS] All RQs are supported by at least one figure
- [PASS] Artifact saved as `artifacts/step-4b-figure-plan.md`

## Input for Next Step
Synthesis of the figure plan (Step 4b) into the "Equation & Table Plan" (Step 4c). This will complete the paper's non-textual architecture.
