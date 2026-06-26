# [STEP 5c] — Equation Generation

## Summary
Generated four rigorous LaTeX equations for the LLMOrch-VAPT research paper. these mathematical formulations provide the theoretical underpinning for the framework's core methodologies: Complexity-Aware Routing (DCAT), Cost-Reasoning Optimization, Semantic Caching (SSC), and Operational Resilience (MTTR). All assets are saved as modular `.tex` files in the `assets/` directory.

## Full Output

### 1. Generated Asset Files
All files are saved in the `/assets/` directory:
- `eq-01-complexity.tex`: Task Complexity Signal formula.
- `eq-02-optimization.tex`: Cost-Reasoning Optimization Objective with constraints.
- `eq-03-cache-similarity.tex`: Semantic Cache Similarity and Decision function.
- `eq-04-mttr.tex`: Decomposition of the Mean Time To Recovery metric.

### 2. Walkthrough of Assets

#### Eq 1: Complexity Signal ($C_t$)
Formalizes the "Complexity Signal" as a weighted sum of keyword indicators, vulnerability presence (CVEs), and network depth. This provides the mathematical basis for the DCAT routing engine.

#### Eq 2: Optimization Objective ($\mathcal{J}$)
Defines the core problem as a constrained maximization of reasoning quality. It introduces the `SecurityTier(m)` constraint, which ensures that the selected model $m$ meets or exceeds the complexity requirement $C(t)$ of the task.

#### Eq 3: Cache Similarity ($\sigma$)
Utilizes cosine similarity between vector embeddings to define the cache-hit condition. It explicitly includes the decision logic for returning cached reasoning vs. invoking the LLM.

#### Eq 4: MTTR Metric
Decomposes the recovery time into detection, checkpointing, and switching phases. This provides a rigorous metric for evaluating the "Operational Resilience" claim in the evaluation section.

## Key Decisions Made
- Used `\arg \max` in Eq 2 to emphasize the system's decision-making nature.
- Defined variables using standard academic notation (e.g., $\mathbb{I}$ for indicators, $\mathbb{E}$ for expectation) to ensure compatibility with top-tier AI and security venues.
- Grouped the variables and definitions within the `.tex` files to make them ready for `\input{}` into the main manuscript.

## Open Questions
- None.

## Checklist Results
- [PASS] `artifacts/step-4c-equations-tables.md` used as input
- [PASS] 3–5 rigorous equations generated in LaTeX
- [PASS] Each asset is saved as a separate `.tex` file in `assets/`
- [PASS] Mathematical symbols and variables are clearly defined
- [PASS] Formulas are technically sound and map to the framework's logic
- [PASS] Equations support the Research Questions (RQs)
- [PASS] Artifact saved as `artifacts/step-5c-equations.md`

## Input for Next Step
Synthesis of all generated assets (Figures, Tables, Equations) into the "Full Paper Drafting" (Step 6). We will begin with the Abstract and Introduction (Step 6a).
