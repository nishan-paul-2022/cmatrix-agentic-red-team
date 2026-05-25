# [STEP 4c] — Equation & Table Plan

## Summary
Planned 4 mathematical equations and 5 data tables to provide the technical rigor and empirical evidence required for an IEEE S&P manuscript. These elements formalize the **VulnRAG** logic and the metrics used to answer the Research Questions (RQs).

## Full Output

### 1. Equation Plan

#### Equation 1: Operational Relevance Score ($S_{OR}$)
- **LaTeX**: $S_{OR}(q, c) = w_{sem} S_{sem}(q, c) + w_{cvss} V_{cvss}(c) + w_{exp} E_{exp}(c) + w_{rec} R_{rec}(c)$
- **Section**: VI. Multi-Factor Semantic Reranking
- **Description**: The core weighted scoring function used by `cve_reranker.py` to reorder retrieved CVEs.
- **Variables**: 
    - $S_{sem}$: Semantic affinity score (Cross-Encoder output).
    - $V_{cvss}$: Normalized CVSS v3.1 base score $[0, 1]$.
    - $E_{exp}$: Binary exploit availability $[0, 1]$.
    - $R_{rec}$: Disclosure recency score.
    - $w_i$: Relative importance weights where $\sum w_i = 1$.

#### Equation 2: Recency Decay Function ($R_{rec}$)
- **LaTeX**: $R_{rec}(c, t) = \frac{1}{1 + \ln(1 + \Delta t)}$
- **Section**: VI. Multi-Factor Semantic Reranking
- **Description**: Logarithmic time-decay function ensuring that recently disclosed vulnerabilities are prioritized without completely masking historical data.
- **Variables**: $\Delta t$ is the time delta in days since the CVE disclosure date.

#### Equation 3: Complexity-Aware Routing Objective
- **LaTeX**: $T^* = \arg \max_{T \in \{F, P, R\}} (Q(T) - \lambda_C C(T) - \lambda_L L(T))$
- **Section**: VII. Multi-Tier Routing
- **Description**: The optimization objective for selecting the LLM tier (Flash, Pro, Reasoning) for a given sub-task.
- **Variables**: 
    - $T$: Tier selection.
    - $Q(T)$: Estimated reasoning quality of the tier.
    - $C(T)$: Unit inference cost.
    - $L(T)$: Latency penalty.
    - $\lambda$: Constraint coefficients.

#### Equation 4: Discovery Yield Metric ($Y_G$)
- **LaTeX**: $Y_G = \frac{|C_G \setminus C_V|}{|C_V|}$
- **Section**: VIII. Experimental Evaluation
- **Description**: A novel metric to quantify the unique discovery value of graph traversal over standard vector search.
- **Variables**: 
    - $C_G$: Set of relevant CVEs discovered via relationship graph traversal.
    - $C_V$: Set of relevant CVEs discovered via standard top-K vector search.

---

### 2. Table Plan

#### Table I: LLM Tier Characteristics and Routing Indicators
- **Section**: VII. Multi-Tier Routing
- **Columns**: Tier | Representative Models | Typical Tasks | Cost/1M (Avg) | Latency
- **Purpose**: Defines the operational environment for the complexity-aware routing experiments.

#### Table II: Reranking Strategy Configuration Matrix
- **Section**: VI. Multi-Factor Semantic Reranking
- **Columns**: Strategy | $w_{sem}$ | $w_{cvss}$ | $w_{exp}$ | $w_{rec}$ | Use Case
- **Purpose**: Details the specific weighting profiles evaluated in the reranking study (e.g., Balanced vs. Security-First).

#### Table III: Retrieval Performance: Baseline vs. VulnRAG
- **Section**: VIII. Experimental Evaluation
- **Columns**: Method | Recall@5 | Precision@5 | NDCG@5 | Avg. Relevant Found
- **Purpose**: Primary empirical proof for RQ1 and RQ3, comparing NVD keyword search, Naive Vector search, and VulnRAG.

#### Table IV: Impact of Agentic Self-Correction Loop
- **Section**: VIII. Experimental Evaluation
- **Columns**: Metric | Baseline (Raw) | 1-Pass Ref. | 2-Pass Ref. | Net Gain (%)
- **Purpose**: Empirical proof for RQ2, showing how iterative query reformulation overcomes initial search failures.

#### Table V: Graph Discovery Yield by CVE Severity
- **Section**: VIII. Experimental Evaluation
- **Columns**: Severity (CVSS) | Sample Size | Uniq. Found (D=1) | Uniq. Found (D=2) | Chain Rate
- **Purpose**: Deep-dive into the structural discovery novelty, proving that graph traversal finds critical related vulnerabilities that are semantically distinct.

## Key Decisions Made
- **Naming**: The reranking function will be consistently referred to as **MFSR** (Multi-Factor Semantic Reranking).
- **Metric Selection**: Chose NDCG (Normalized Discounted Cumulative Gain) as the primary ranking metric to highlight the effectiveness of reranking.

## Open Questions
- Should we provide the specific model versions used for the "Flash/Pro/Reasoning" tiers in Table I? (Decision: Yes, using Gemini 1.5 Flash, Gemini 1.5 Pro, and Claude 3.5 Sonnet as the reference set).

## Checklist Results
- [PASS] `artifacts/step-4a-section-structure.md` read first
- [PASS] `artifacts/step-3c-threat-model-research-questions.md` read first
- [PASS] 3–5 equations planned with LaTeX and variable definitions
- [PASS] 3–5 tables planned with columns and purpose
- [PASS] Each element linked to a section and Research Question
- [PASS] Artifact saved as `artifacts/step-4c-equation-table-plan.md`

## Input for Next Step
The technical blueprint of the manuscript is now complete. We have the section structure, the figure plan, and the mathematical/tabular plan. We are ready to move to **STEP 5 — Figure, Table & Equation Generation**, where we will start implementing these components in LaTeX.
