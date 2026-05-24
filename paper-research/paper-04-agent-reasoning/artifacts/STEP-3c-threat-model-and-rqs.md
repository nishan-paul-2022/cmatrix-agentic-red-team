# [STEP 3c] — Threat Model & RQs — OUTPUT ARTIFACT

## 1) Summary
This sub-step defined the formal threat model and research questions (RQs) that structure the remainder of the paper. We established a trust boundary between the autonomous orchestrator and the target infrastructure, enforced by a risk-aware HITL safety gate. We also formulated four RQs that directly validate the core contributions defined in [STEP 3b], focusing on efficiency, thoroughness, safety, and model-agnostic performance. Finally, we created the visual representation of this model in `figure-01-threat-model.tex`.

## 2) Full Output

### 2.1 Formal Threat Model

| Dimension | Definition |
| :--- | :--- |
| **Adversary Profile** | An AI-augmented red team or autonomous security agent tasked with proactive vulnerability assessment. |
| **Adversary Goals** | Identify technical vulnerabilities (CVEs, misconfigurations) and validate attack paths in a target infrastructure without causing system disruption. |
| **Capabilities** | Access to standard security tooling (Nmap, Metasploit, etc.), long-horizon reasoning capabilities (LLMs), and network-level connectivity to the target. |
| **Assumptions** | The agent operates within a containerized "execution spine"; the HITL gate has absolute veto power over any tool call deemed "high-risk." |
| **Trust Boundary** | A critical boundary exists between the Reasoning Suite (internal) and the Target Infrastructure (external), mediated by the HITL Safety Gate. |
| **Out-of-Scope** | Physical intrusion, social engineering, 0-day exploitation, and attacks on the LLM provider itself (e.g., model extraction). |

### 2.2 Research Questions (RQs)

1.  **RQ1 (Efficiency):** Does the composition of ToT and ReWOO reasoning patterns significantly reduce LLM API overhead and token consumption compared to standard interleaved (ReAct) security agents?
    - *Validates Contribution 1 & 4.*
    - *Target Answer*: Quantitative evidence of >30% reduction in API calls for multi-step attack chains.

2.  **RQ2 (Thoroughness):** To what extent does "executable reflection" improve the completeness of security assessments by identifying and correcting missed attack vectors?
    - *Validates Contribution 2.*
    - *Target Answer*: Qualitative and quantitative comparison showing reflection loops identifying at least 20% more vulnerabilities than one-shot plans.

3.  **RQ3 (Safety):** Can a risk-aware HITL safety gate effectively prevent the execution of disruptive commands while maintaining autonomous operation for low-risk tasks?
    - *Validates Contribution 3.*
    - *Target Answer*: Zero "disruptive" tool calls reaching the target infrastructure during testing, with high throughput for "safe" tools (e.g., info gathering).

4.  **RQ4 (Generalization):** How does the performance of the composite reasoning suite vary across different LLM backends (e.g., GPT-4 vs. Llama-3), and do our reasoning patterns bridge the performance gap for smaller models?
    - *Validates Contribution 4.*
    - *Target Answer*: Proof that ReWOO/ToT enables a 70B model to approach the performance of a 1T+ model on complex security planning.

## 3) Key Decisions Made
- **Strict Scope Definition**: Explicitly placed "0-day discovery" out of scope to avoid reviewer criticism about current LLM reasoning limits.
- **Visual trust boundary**: Used TikZ to explicitly draw the "Trust Boundary" around the Orchestrator + HITL Gate, emphasizing the safety-first architecture.
- **Answerability**: Ensured each RQ has a clear "Target Answer" that can be mapped to an experiment in Step 4.

## 4) Open Questions
- **Baseline for RQ1**: Which specific open-source agent should we use as the "ReAct" baseline? (Likely a standard LangChain ReAct agent).
- **Risk Taxonomy**: Is the "disruptive" vs. "safe" binary sufficient, or do we need a more granular 4-tier risk model (e.g., Informational, Low, Medium, High)?

## 5) Checklist Results (PASS/FAIL)
- [PASS] Formal threat model includes adversary goals, capabilities, and assumptions
- [PASS] 3–5 specific RQs defined
- [PASS] Each RQ maps to at least one contribution from 3b
- [PASS] Each RQ is stated in answerable, scientific terms
- [PASS] `figure-01-threat-model.tex` created in `assets/`
- [PASS] Figure uses TikZ and follows the specified visual elements
- [PASS] `ASSET-INDEX.md` updated
- [PASS] Threat model is grounded in the findings of Step 1 and Step 2

## 6) Input for Next Step (Step 4a)
- **Experimental Design**: Step 4a must design four distinct experiments, one to answer each of the four RQs.
- **Tool Mapping**: Map the "Security Tool Registry" from the figure to the actual tools implemented in CMatrix (Nmap, etc.).

## 7) Asset Files Created
- `paper-research/paper-04-agent-reasoning/assets/figure-01-threat-model.tex`: Threat model diagram.
- `paper-research/paper-04-agent-reasoning/assets/ASSET-INDEX.md`: Updated index.
