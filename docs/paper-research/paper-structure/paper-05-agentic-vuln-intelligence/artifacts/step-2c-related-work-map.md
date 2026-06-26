# [STEP 2c] — Related Work Map

## Summary
Created a comprehensive comparison map between VulnRAG and current state-of-the-art (SOTA) systems. This visualization clearly identifies our "Checkmark Sweep" and the unique research niche we occupy.

## Full Output

### SOTA Comparison Table

| Feature | PentestGPT (2024) | RAVEN (2026) | Self-RAG (2024) | ActiveRAG (2024) | Multi-Level RAG (2025) | **VulnRAG (Ours)** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Agentic reasoning loop** | ✅ | ✅ | ✅ | ✅ | ❌ | **✅** |
| **Autonomous self-correction** | ❌ | ✅ | ✅ | ✅ | ❌ | **✅** |
| **Security-specific (CVE/NVD)** | ✅ | ✅ | ❌ | ❌ | ✅ | **✅** |
| **Graph-aware retrieval** | ❌ | ❌ | ❌ | ❌ | ❌ | **✅** |
| **Training-free (Zero-shot)** | ✅ | ✅ | ❌ | ✅ | ✅ | **✅** |
| **Cost-optimized routing** | ❌ | ❌ | ❌ | ❌ | ❌ | **✅** |

### The "Unoccupied Space"
Our project occupies the unique intersection of **Structural Retrieval (Graphs)** and **Operational Optimization (Routing)** within the Agentic RAG paradigm. 

Specifically, while RAVEN and Multi-Level RAG address the security domain, they treat retrieval as a flat or hierarchical search over text. **VulnRAG** is the first to:
1.  **Traverse structural relationships** (CVE graphs) to discover related attack vectors.
2.  **Apply tiered model routing** to the RAG pipeline itself, ensuring that expensive reasoning is only used for complex intelligence synthesis while routine lookups use cheaper tiers.

### Visualization of Positioning
- **Structural Novelty**: Move from "Text Search" -> "Graph Discovery".
- **Operational Novelty**: Move from "Always-Flagship" -> "Complexity-Aware Tiering".
- **Implementation Novelty**: Move from "Fine-tuned models" -> "Modular Agentic Orchestration".

## Key Decisions Made
- **Claim of First**: We will cautiously claim to be the first **Graph-Aware Agentic RAG system specifically optimized for Vulnerability Intelligence**.
- **Related Work Structure**: The "Related Work" section of the paper will be structured around these three pillars: Agentic RAG, Security Intelligence Systems, and Graph-based Retrieval.

## Open Questions
- Should we include a comparison with **RAPTOR**'s document trees, or is the distinction between "Document Summaries" and "CVE Relationships" clear enough?
- Are there any "Agentic RAG" papers that use **Reinforcement Learning** that we should distinguish ourselves from?

## Checklist Results
- [PASS] `artifacts/step-2a-cited-papers-research.md` read first
- [PASS] `artifacts/step-2b-state-of-the-art-search.md` read first
- [PASS] Comparison table between ours and 5+ competitors created
- [PASS] 6+ criteria for comparison used
- [PASS] "Checkmark Sweep" visualized
- [PASS] "Unoccupied Space" identified
- [PASS] Artifact saved as `artifacts/step-2c-related-work-map.md`

## Input for Next Step
A clear and defensible novelty argument. We are now ready to enter **STEP 3 — Novelty & Contribution Crystallization**, where we will formally define our unique research contributions based on this gap analysis.
