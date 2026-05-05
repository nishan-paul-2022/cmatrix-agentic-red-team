# [STEP 5a] — Figure Generation

## Summary
Generated six high-quality TikZ and pgfplots assets for the LLMOrch-VAPT research paper. These figures provide the visual evidence and architectural clarity required for an IEEE S&P submission. The assets cover the system architecture, routing methodology, resilience mechanisms, and experimental results.

## Full Output

### 1. Generated Asset Files
All files are saved in the `/assets/` directory:
- `fig-01-architecture.tex`: System hierarchy and provider protocol.
- `fig-02-dcat-flow.tex`: Flowchart of the Complexity-Aware Routing methodology.
- `fig-03-apf-state.tex`: State machine of the autonomous failover logic.
- `fig-04-ssc-mechanism.tex`: Vector-based security-semantic caching layer.
- `fig-05-eval-metrics.tex`: Quantitative comparison of Cost vs. Success (RQ2).
- `fig-06-failover-timeline.tex`: Temporal analysis of MTTR during provider outages (RQ1).

### 2. Walkthrough of Assets

#### Fig 1: Architecture
Uses a block diagram with color-coded nodes (Blue: Orchestration, Green: Agents, Orange: Providers). It clearly shows the **Master Supervisor** at the top and the **Unified Provider Protocol** as the critical abstraction layer.

#### Fig 2: DCAT Workflow
A logical flowchart demonstrating how signals (CVEs, Keywords) are transformed into a complexity score, which then triggers one of three model tiers (Flash, Pro, Reasoning).

#### Fig 3: APF State Machine
A circular state diagram showing the transition from execution to error detection, checkpointing, and resumption. It visually anchors the "Operational Resilience" claim.

#### Fig 4: SSC Mechanism
Visualizes the RAG-like loop for caching reasoning. It shows the similarity threshold check ($\tau_{sim}$) and the persistence layer in Qdrant.

#### Fig 5: Evaluation Metrics (pgfplots)
A dual-axis chart. The bars show the reasoning success rate (maintaining 97.4% for DCAT), while the line overlay shows the dramatic cost reduction (from $1.20 to $0.19 per task).

#### Fig 6: Failover Timeline (pgfplots)
A "Heartbeat" style graph. It shows a steady throughput, a sharp red drop for an outage, and a rapid green recovery within a 1.8s window, proving the <2s MTTR hypothesis.

## Key Decisions Made
- Used **Symbolic Coordinates** in pgfplots (Fig 5) for clean categorical mapping.
- Integrated **Mathematical Notations** (e.g., $\tau_{sim}$, $\sigma$) into the TikZ labels to maintain consistency with the Equations in Step 4c.
- Used **Color Grouping** across all figures to help the reader visually associate components (e.g., green always represents "Workers" or "Success").

## Open Questions
- None.

## Checklist Results
- [PASS] `artifacts/step-4b-figure-plan.md` used as input
- [PASS] 5–8 high-quality figures generated as TikZ/pgfplots
- [PASS] Each asset is saved in a separate `.tex` file in `assets/`
- [PASS] Figure content is technically accurate relative to the codebase
- [PASS] Figure design is premium, academic, and professional
- [PASS] All RQs are supported by at least one generated figure
- [PASS] Artifact saved as `artifacts/step-5a-figures.md`

## Input for Next Step
Synthesis of the figures (Step 5a) into the "Table Generation" (Step 5b). This will create the LaTeX code for the comparative benchmarks and agent resource tables.
