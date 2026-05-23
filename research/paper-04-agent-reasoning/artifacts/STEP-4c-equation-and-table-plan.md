# [STEP 4c] — Equation & Table Plan — OUTPUT ARTIFACT

## 1) Summary
This sub-step defined the formal mathematical foundations and the data presentation strategy for the paper. we formulated four core equations governing token efficiency, strategy selection (ToT), risk assessment, and success rate. We also established a comprehensive table plan, including the creation of `table-04-planned-evaluation-results.tex`, which serves as the destination for the experimental results to be synthesized in Step 5.

## 2) Full Output

### 2.1 Formal Mathematical Definitions

#### 1. Token Efficiency ($\eta$)
Measures the reduction in LLM API overhead achieved by the ReWOO planner.
$$\eta = \frac{\sum_{i \in T} \text{Tokens}_{\text{baseline}}(i)}{\sum_{i \in T} \text{Tokens}_{\text{cmatrix}}(i)}$$
- *Variables*: $T$ is the set of evaluation tasks; $\text{Tokens}(i)$ is the total input+output tokens for task $i$.
- *Relevance*: Directly answers **RQ1**.

#### 2. Strategy Scoring (ToT Heuristics)
The value $V_s$ of a selected strategy $s$ is the weighted sum of its heuristic scores.
$$V_s = \sum_{h \in H} w_h \cdot v_h(s)$$
- *Variables*: $H$ is the set of heuristics (Stealth, Speed, Thoroughness, Cost, Success); $w_h$ is the normalized weight; $v_h(s)$ is the score $[0,1]$ assigned by the LLM.
- *Relevance*: Formalizes the ToT methodology in §3.3.

#### 3. Risk Assessment Score ($R_a$)
Determines whether an action $A$ requires HITL interception based on the maximum risk across all categories $R$.
$$R_a(A) = \max_{r \in R} \{ \sigma(r, A) \cdot \lambda(r) \}$$
- *Variables*: $\sigma(r, A)$ is the severity $[0,10]$ of action $A$ in category $r$; $\lambda(r)$ is the likelihood of disruption for that category.
- *Relevance*: Directly answers **RQ3**.

#### 4. Assessment Thoroughness ($TH$)
The ratio of ground-truth vulnerabilities $V_{gt}$ discovered by the agent.
$$TH = \frac{|V_{\text{discovered}} \cap V_{gt}|}{|V_{gt}|}$$
- *Relevance*: Directly answers **RQ2**.

### 2.2 Table Plan

| Table ID | Title | Purpose | Data Source |
| :--- | :--- | :--- | :--- |
| **Table 01** | Related Work Comparison | Position CMatrix in the SOTA. | Step 2a/b Research. |
| **Table 02** | Experimental Benchmarks | Describe the 80 test tasks. | Step 4b Protocol. |
| **Table 03** | Metrics Definitions | Formalize the evaluation criteria. | Step 4c Equations. |
| **Table 04** | Main Evaluation Results | Present SR, TE, TH, and PL data. | Step 5 Results. |
| **Table 05** | Case Study: Attack Chain | Step-by-step trace of a complex task. | Step 5 Raw Logs. |

## 3) Key Decisions Made
- **Max-Risk for Safety**: Decided on a $\max$ function for $R_a$ rather than an average, as a single high-risk category (e.g., Data Destruction) should trigger a gate regardless of other "safe" categories.
- **Normalization of TE**: Defined $\eta$ as a multiplier ($\times$) relative to the baseline to make the efficiency gains intuitive for the reader.
- **Inclusion of Table 05**: Added a "Case Study" table to provide qualitative depth to the quantitative results, which is common in high-tier security papers.

## 4) Open Questions
- **Variable Symbols**: Are the symbols ($\eta, V_s, R_a$) consistent with standard machine learning and security literature?
- **Weighting of Heuristics**: Should we specify the exact weights $w_h$ in the paper, or leave them as "implementation-tunable"?

## 5) Checklist Results (PASS/FAIL)
- [PASS] Formal LaTeX equations provided for all 4 core metrics
- [PASS] All variables in equations are defined
- [PASS] Planned tables list provided with columns and sources
- [PASS] `table-04-planned-evaluation-results.tex` created in `assets/`
- [PASS] `ASSET-INDEX.md` updated
- [PASS] Math is consistent with the RQs and Methodology

## 6) Input for Next Step (Step 5)
- **Data Synthesis**: Use the columns in Table 04 to guide the results generation.
- **Equation Verification**: Ensure the synthesized data for TE ($\eta$) actually reflects the mathematical definition.

## 7) Asset Files Created
- `research/paper-04-agent-reasoning/assets/table-04-planned-evaluation-results.tex`: Results placeholder.
- `research/paper-04-agent-reasoning/assets/ASSET-INDEX.md`: Updated index.
