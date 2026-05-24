# [STEP 3c] — Threat Model & Research Questions

## Summary
Defined the formal **Threat Model** and **Research Questions (RQs)** for the VulnRAG paper. This step also provides the mathematical formalization for the Multi-Factor Semantic Reranking (MFSR) scoring function, providing the "academic rigor" required for IEEE S&P.

## Full Output

### 1. Threat Model
- **System Model**: We consider an autonomous security assessment system operating within a complex enterprise network. The system must process thousands of potential service/version indicators and correlate them with a vast, dynamically updated knowledge base (NVD).
- **The Information Overload Challenge**: With >30,000 CVEs published annually, the primary bottleneck for autonomous agents is not "access" to data, but the "precision of retrieval."
- **Retrieval Gap**: We define the core threat to autonomous reliability as the **Retrieval Gap**—the failure of standard keyword or naive vector search to identify operationally linked vulnerabilities (e.g., shared libraries, transitive dependencies) or prioritize actionable exploits over theoretical vulnerabilities.
- **Adversarial Context**: While our primary focus is defense/assessment, the threat model acknowledges that attackers can use similar automated retrieval to discover attack paths faster than human defenders can patch them.

### 2. Research Questions (RQs)
- **RQ1: Structural Retrieval Effectiveness** — To what extent does graph-based traversal of CVE relationship metadata improve the recall of operationally linked vulnerabilities compared to standard semantic vector search? (Tests Novelty 1).
- **RQ2: Zero-Shot Agentic Resilience** — Can a decoupled, training-free agentic feedback loop (Evaluator-Reformulator) achieve search precision and coverage metrics comparable to fine-tuned self-reflective RAG models? (Tests Novelty 2).
- **RQ3: Domain-Aware Reranking** — How does the integration of security-specific domain metrics (CVSS, exploitability, recency) into the reranking function influence the "Intelligence Density" of the top-K results provided to the LLM context? (Tests Novelty 4).
- **RQ4: Operational Economics** — What are the quantitative trade-offs between reasoning success rates and inference costs when implementing complexity-aware multi-tier routing for vulnerability intelligence tasks? (Tests Novelty 3).

### 3. Mathematical Formalization: Operational Relevance Score ($S_{OR}$)
To address RQ3, we formalize the **Multi-Factor Semantic Reranking (MFSR)** scoring function. For a given query $q$ and a retrieved CVE $c$, the final relevance score $S_{OR}$ is defined as:

$$S_{OR}(q, c) = w_{sem} \cdot S_{sem}(q, c) + w_{cvss} \cdot V_{cvss}(c) + w_{exp} \cdot E_{exp}(c) + w_{rec} \cdot R_{rec}(c)$$

Where:
- $S_{sem}(q, c)$: Semantic similarity score from the Cross-Encoder model.
- $V_{cvss}(c)$: Normalized CVSS v3.1 base score $[0, 1]$.
- $E_{exp}(c)$: Binary exploit availability score (1 if exploit exists in public databases, 0 otherwise).
- $R_{rec}(c)$: Recency score, calculated as $1 / (1 + \ln(1 + \Delta t))$, where $\Delta t$ is the days since disclosure.
- $w_i$: Configurable weights such that $\sum w_i = 1$.

### 4. Logic Table: Mapping RQs to Contributions

| Research Question | Associated Contribution | Implementation Module |
| :--- | :--- | :--- |
| **RQ1** | Structural-Semantic Architecture | `cve_graph.py` |
| **RQ2** | Agentic Self-Correction Loop | `self_correction.py` |
| **RQ3** | MFSR Reranking Function | `cve_reranker.py` |
| **RQ4** | Multi-Tier Routing | `cve_search.py` |

## Key Decisions Made
- **Weights**: The paper will evaluate three specific weighting configurations ($w_i$):
    1.  **Balanced**: Equal emphasis on all factors.
    2.  **Security-First**: High weight on CVSS ($w_{cvss}$) and Exploitability ($w_{exp}$).
    3.  **Recency-First**: High weight on disclosure date ($w_{rec}$).
- **RQ Focus**: The RQs are designed to move from "Retrieval Quality" (RQ1-3) to "Operational Efficiency" (RQ4).

## Open Questions
- Should we include **EPSS** (Exploit Prediction Scoring System) as a separate factor or keep it merged with "Exploit Availability"? (Decision: Keep merged for simplicity, but mention in the text).

## Checklist Results
- [PASS] `artifacts/step-3a-novelty-identification.md` read first
- [PASS] `artifacts/step-3b-core-contributions.md` read first
- [PASS] Formal "Threat Model" defined
- [PASS] 3–4 "Research Questions" (RQs) defined
- [PASS] Each RQ is clear, answerable, and linked to a novelty
- [PASS] Mathematical definition of $S_{OR}$ provided
- [PASS] Artifact saved as `artifacts/step-3c-threat-model-research-questions.md`

## Input for Next Step
The theoretical framework of the paper is now complete. We have the "Why" (Threat Model), the "What" (Novelties/Contributions), and the "How to measure it" (RQs). We are now ready to move to **STEP 4 — Paper Architecture**, where we will define the section structure and plan the figures/tables.
