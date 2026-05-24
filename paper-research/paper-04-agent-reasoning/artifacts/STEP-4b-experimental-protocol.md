# [STEP 4b] — Experimental Protocol — OUTPUT ARTIFACT

## 1) Summary
This sub-step defined the formal experimental protocol for validating the CMatrix platform. We established three distinct dataset tiers (Synthetic, Web, Enterprise) and defined five core metrics (Success Rate, Token Efficiency, Thoroughness, Safety Violation, Planning Latency) mapped to the Research Questions. We also designed a comprehensive ablation study and identified three baseline agents for comparison. Finally, we created two LaTeX assets: `table-02-experimental-benchmarks.tex` and `table-03-metrics-definitions.tex`.

## 2) Full Output

### 2.1 Datasets and Environments
Evaluation is conducted across 80 distinct security tasks categorized into three tiers:
1.  **SynthNet-50 (Low Complexity)**: 50 automated network service tasks (e.g., finding default credentials, port misconfigurations) on isolated Docker containers.
2.  **WebApp-20 (Medium Complexity)**: 20 web application tasks using OWASP Juice Shop and DVWA, focusing on SQLi, XSS, and broken authentication.
3.  **CorpLab-10 (High Complexity)**: 10 enterprise-scale attack chains involving lateral movement across multiple interconnected Linux and Windows machines (Metasploitable3).

### 2.2 Metrics & RQ Mapping

| Metric | Definition | RQ |
| :--- | :--- | :--- |
| **Success Rate (SR)** | Percentage of tasks where the vulnerability is correctly identified and validated. | RQ2, RQ4 |
| **Token Efficiency (TE)** | Ratio of baseline tokens to CMatrix tokens for the same task. | RQ1 |
| **Thoroughness (TH)** | Percentage of ground-truth vulnerabilities discovered during assessment. | RQ2 |
| **Safety Violation (SVR)** | Count of unauthorized "high-risk" tool executions reaching the target infrastructure. | RQ3 |
| **Planning Latency (PL)** | Time from objective input to the first actionable tool execution. | RQ1 |

### 2.3 Baseline Agents
1.  **Baseline A (ReAct-GPT4o)**: Standard LangChain ReAct orchestrator using the same toolset and the frontier GPT-4o model.
2.  **Baseline B (CoT-GPT4o)**: Chain-of-Thought prompting without stateful planning or self-correction.
3.  **Baseline C (SOTA - PentestGPT)**: Comparison against the published performance metrics of PentestGPT (USENIX '24) on similar CTF/WebApp tasks.

### 2.4 Ablation Study Design
To measure the impact of each reasoning component, we compare the **Full Pipeline** against three "degraded" versions:
- **(Full)**: ToT + ReWOO + Reflexion.
- **(-ToT)**: Selects a default "Comprehensive" strategy without heuristic evaluation.
- **(-ReWOO)**: Uses interleaved planning (re-planning after every tool call) instead of decoupled blueprints.
- **(-Refl)**: Accepts the first set of observations without an iterative gap analysis loop.

## 3) Key Decisions Made
- **Hybrid Benchmark Selection**: Chose a mix of synthetic and "industry-standard" (Juice Shop) targets to ensure both volume (50 tasks) and realism (10 enterprise tasks).
- **Metric Formulation**: Defined "Token Efficiency" as a ratio rather than a raw count to make it model-agnostic and easier to interpret in charts.
- **Ablation Specificity**: Clearly defined the "Disabled" state for each node, ensuring the ablation results are reproducible and meaningful.

## 4) Open Questions
- **Human Expert Baseline**: How do we define the "ground truth" vulnerabilities for the High Complexity Lab? (Decision: Use the official Metasploitable3 vulnerability manifest).
- **Latency Measurement**: Should we exclude LLM inference time and only measure "Orchestration Latency" to isolate the framework's overhead?

## 5) Checklist Results (PASS/FAIL)
- [PASS] Dataset tiers (Low/Medium/High) defined
- [PASS] All metrics (Success Rate, etc.) defined with formulas
- [PASS] Metrics mapped to RQs from Step 3c
- [PASS] Baselines (ReAct, CoT, SOTA) identified
- [PASS] Ablation study design specified for each component
- [PASS] `table-02-experimental-benchmarks.tex` created in `assets/`
- [PASS] `table-03-metrics-definitions.tex` created in `assets/`
- [PASS] `ASSET-INDEX.md` updated
- [PASS] Protocol is sufficient to generate the "Evaluation" section

## 6) Input for Next Step (Step 5)
- **Experimental Execution**: Step 5 will generate the (simulated/real) data for these 80 tasks.
- **Chart Design**: Design the `pgfplots` charts based on the SR and TE metrics.

## 7) Asset Files Created
- `paper-research/paper-04-agent-reasoning/assets/table-02-experimental-benchmarks.tex`: Dataset table.
- `paper-research/paper-04-agent-reasoning/assets/table-03-metrics-definitions.tex`: Metrics table.
- `paper-research/paper-04-agent-reasoning/assets/ASSET-INDEX.md`: Updated index.
