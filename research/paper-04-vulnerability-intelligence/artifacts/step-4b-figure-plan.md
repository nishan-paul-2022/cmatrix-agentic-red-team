# [STEP 4b] — Figure Plan

## Summary
Planned 7 high-quality, technically dense figures to illustrate the **VulnRAG** framework and its empirical performance. These figures are designed to meet the aesthetic and scientific standards of IEEE S&P, utilizing TikZ and PGFPlots for professional rendering.

## Full Output

### Figure 1: VulnRAG System Architecture
- **ID**: Fig 1
- **Section**: IV. System Design
- **Title**: The VulnRAG Modular Agentic Architecture.
- **Type**: TikZ Block Diagram.
- **Description**: A high-level overview showing the flow from **Continuous Knowledge Sync** (NVD API 2.0) to the **Agentic Retrieval Loop** (Query Reformulator -> Vector Store -> Multi-Factor Reranker -> Evaluator).
- **The Message**: VulnRAG is a stateful, modular system that replaces the linear "Retrieve-then-Generate" paradigm with an iterative, agentic cycle.

### Figure 2: CVE Relationship Graph Traversal
- **ID**: Fig 2
- **Section**: V. Agentic Retrieval Optimization
- **Title**: Attack Chain Discovery via Structural CVE Relationship Graphs.
- **Type**: Network Graph Visualization (TikZ `shapes.geometric`).
- **Description**: Visualizes a "seed" CVE node (e.g., CVE-2021-44228) connected to related vulnerabilities through various edge types: `referenced_in_url`, `shared_exploit_id`, and `cpe_cluster`.
- **The Message**: Structural retrieval enables the discovery of functionally linked vulnerabilities that lack semantic similarity.

### Figure 3: Zero-Shot Self-Correction Flow
- **ID**: Fig 3
- **Section**: V. Agentic Retrieval Optimization
- **Title**: The Evaluator-Reformulator Feedback Logic.
- **Type**: Logic Flowchart.
- **Description**: Details the conditional logic of the **Evaluator agent**: analyzing result counts, score distributions, and metadata relevance to trigger a **Reformulator** pass with specific instructions (e.g., "broaden product scope").
- **The Message**: Agentic self-correction ensures high-precision retrieval in zero-shot environments.

### Figure 4: Multi-Factor Reranking (MFSR) Radar
- **ID**: Fig 4
- **Section**: VI. Multi-Factor Semantic Reranking
- **Title**: Comparative Profiling of Ranking Strategy Weights.
- **Type**: Radar Chart.
- **Description**: Compares three ranking strategies (**Balanced**, **Security-First**, **Recency-First**) across four dimensions: Semantic Similarity, CVSS Severity, Exploit Availability, and Disclosure Recency.
- **The Message**: MFSR provides a flexible framework for aligning RAG outputs with specific operational requirements.

### Figure 5: Precision-Recall Frontier Improvement
- **ID**: Fig 5
- **Section**: VIII. Experimental Evaluation
- **Title**: Impact of Agentic Query Reformulation on Retrieval Frontier.
- **Type**: PGFPlots Line Chart (P-R Curve).
- **Description**: Contrasts the Precision-Recall curves of **Baseline (Raw Queries)** against **VulnRAG (Reformulated Queries)** across 200 benchmark tasks.
- **The Message**: Agentic expansion significantly improves both recall and precision by disambiguating security terminology.

### Figure 6: Discovery Yield Analysis
- **ID**: Fig 6
- **Section**: VIII. Experimental Evaluation
- **Title**: Discovery Yield: Structural Graph Traversal vs. Semantic Vector Search.
- **Type**: Grouped Bar Chart.
- **Description**: Measures the number of uniquely identified relevant CVEs found at depth 1, 2, and 3 using graph traversal compared to a fixed-K semantic retrieval baseline.
- **The Message**: Graph-aware retrieval provides a unique "Discovery Yield" that text-based RAG cannot achieve.

### Figure 7: Economic Performance Trade-off
- **ID**: Fig 7
- **Section**: VIII. Experimental Evaluation
- **Title**: Success Rate vs. Operational Inference Cost.
- **Type**: PGFPlots Scatter Plot with Pareto Frontier.
- **Description**: Plots the performance-to-cost ratio for three configurations: **Flagship-Only** (High cost/High quality), **Flash-Only** (Low cost/Low quality), and **VulnRAG Tiered Routing** (Optimized).
- **The Message**: Complexity-aware routing achieves near-flagship success rates at a fraction of the operational cost.

## Key Decisions Made
- **Tooling**: All figures will be implemented in native LaTeX (TikZ/PGFPlots) to ensure perfect integration with IEEE S&P fonts and layout.
- **Aesthetics**: Use a consistent color palette (Blues for Architecture, Greens for Logic, Oranges for Results) as established in the design system.

## Open Questions
- Do we have enough data points to plot a smooth P-R curve for Fig 5? (Decision: Use the 200-query benchmark results from the evaluation scripts).

## Checklist Results
- [PASS] `artifacts/step-4a-section-structure.md` read first
- [PASS] 5–8 high-quality figures planned
- [PASS] ID, Section, Title, and Type documented for each
- [PASS] Detailed description and "Message" documented for each
- [PASS] Artifact saved as `artifacts/step-4b-figure-plan.md`

## Input for Next Step
A visual roadmap for the technical and empirical claims. We will now move to **Sub-step 4c: Equation & Table Plan**, completing the technical architecture of the manuscript.
