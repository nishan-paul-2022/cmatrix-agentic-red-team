# [STEP 4a] — Section Structure

## Summary
Defined the full 12–16 page section and subsection structure for the **VulnRAG** manuscript. The structure is optimized for IEEE S&P standards, moving from theoretical problem formulation to deep technical methodology and comprehensive empirical evaluation.

## Full Output

### 1. Abstract (0.25 pages)
- **Core Claim**: VulnRAG is a first-of-its-kind agentic RAG system that overcomes the "Retrieval Gap" in autonomous VAPT via graph-aware discovery and self-correcting reasoning.
- **Key Metrics**: 97%+ reasoning success, [X]% cost reduction.

### 2. Section I: Introduction (1.5 pages)
- **A. The Shift to Autonomous Security**: LLMs as "reasoning engines" in pentesting.
- **B. The Retrieval Gap**: Why keyword and naive vector search fail to capture "Operational Context."
- **C. Contributions**:
    - VulnRAG Structural-Semantic Architecture.
    - Multi-Factor Semantic Reranking (MFSR).
    - Zero-Shot Agentic Self-Correction.
    - Complexity-Aware Multi-Tier Routing.

### 3. Section II: Background and Related Work (1.5 pages)
- **A. Retrieval-Augmented Generation**: Foundations (Lewis et al.), REALM.
- **B. Agentic Workflows**: LangGraph, Self-RAG, Reflexion.
- **C. Autonomous Pentesting SOTA**: PentestGPT, RAVEN, AutoAttacker.
- **D. Graph-based IR**: RAPTOR, KG-RAG comparisons.

### 4. Section III: Threat Model and Problem Formulation (1.0 page)
- **A. System Model**: Enterprise VAPT context.
- **B. Attacker Goals and Constraints**: Information overload vs. exploit accuracy.
- **C. Research Questions (RQ1-4)**: Formal statement of the 4 RQs defined in 3c.

### 5. Section IV: VulnRAG: System Design (1.5 pages)
- **A. Modular Agentic Architecture**: The Master-Worker orchestration logic.
- **B. Continuous Knowledge Synchronization**: `nvd_sync_service.py` and real-time NVD API 2.0 integration.
- **C. Vector Storage and Embeddings**: Qdrant indexing, BGE-large embeddings, and payload-based metadata filtering.

### 6. Section V: Agentic Retrieval Optimization (2.5 pages)
- **A. Query Reformulation Engine**: Technical detail on `query_reformulator.py`. CPE extraction and security synonym mapping.
- **B. Zero-Shot Self-Correction Loop**: The Evaluator-Reformulator feedback logic in `self_correction.py`.
- **C. Structural Discovery via CVE Relationship Graphs**: The core novelty of `cve_graph.py`. Traversing URL references to find related vulnerabilities.

### 7. Section VI: Multi-Factor Semantic Reranking (MFSR) (1.5 pages)
- **A. Cross-Encoder Semantic Scoping**: Using `BGE-reranker-large` to mitigate "Lost in the Middle."
- **B. Operational Relevance Scoring**: Formal mathematical definition of $S_{OR}$ (from 3c).
- **C. Ranking Strategies**: Deep dive into Balanced, Security-First, and Recency-First weighting configurations.

### 8. Section VII: Complexity-Aware Multi-Tier Routing (1.0 page)
- **A. Tier Classification Logic**: How the `SmartCVESearchService` classifies tasks into Flash, Pro, and Reasoning tiers.
- **B. Escalation Thresholds**: Criteria for escalating failed searches to higher-reasoning models.

### 9. Section VIII: Experimental Evaluation (3.0 pages)
- **A. Experimental Setup**: Benchmarks, hardware, and baseline descriptions.
- **B. RQ1 Results (Structural vs. Semantic)**: Recall and NDCG metrics for graph traversal.
- **C. RQ2 Results (Self-Correction)**: Precision-Recall curves showing the impact of reformulation.
- **D. RQ3 Results (Reranking)**: Expert vs. automated relevance ratings.
- **E. RQ4 Results (Economics)**: Cost/Token vs. Reasoning Accuracy tradeoff plots.

### 10. Section IX: Discussion and Limitations (1.5 pages)
- **A. Operational Resilience**: Handling provider outages and API rate limits.
- **B. Ethical Considerations**: Dual-use mitigation and CIDR-restricted tool execution.
- **C. Limitations**: Latency of multi-agent loops and graph depth constraints.

### 11. Section X: Conclusion and Future Work (0.25 pages)
- **Summary**: Synthesis of findings.
- **Future Directions**: Real-time exploit-ability verification (HITL integration).

### 12. References (1.5 pages)
- 30–40 high-quality citations.

## Key Decisions Made
- **Depth**: Section V (Agentic Optimization) is given the most space (2.5 pages) as it contains the primary research novelties (Reformulation, Self-Correction, Graph).
- **Evaluation Weight**: Section VIII is given 3.0 pages to accommodate detailed charts and comparative tables.

## Open Questions
- Should we include a separate "Case Study" section, or integrate cases into the Evaluation section? (Decision: Integrate into Evaluation to save space for technical depth).

## Checklist Results
- [PASS] `artifacts/step-3a/b/c` read first
- [PASS] Full section and subsection structure defined
- [PASS] Title, core argument, and key details documented for each
- [PASS] Target length for each section documented
- [PASS] Total length within 12–16 page range
- [PASS] Artifact saved as `artifacts/step-4a-section-structure.md`

## Input for Next Step
The skeleton of the paper is now ready. We will use this structure in 4b to plan the specific **Figures** that will illustrate the technical concepts in each section.
