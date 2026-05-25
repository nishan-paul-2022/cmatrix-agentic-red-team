# [STEP 3c] — Threat Model & Research Questions

## Summary
Defined the formal threat model and research questions (RQs) for the LLMOrch-VAPT paper. The threat model focuses on the **Operational Resilience** of the autonomous red teaming system under conditions of provider volatility and cost constraints. The research questions are designed to test the core hypotheses regarding failover, cost-efficiency through tiering, and the scalability benefits of semantic caching.

## Full Output

### 1. Threat Model
**System Goal**: To perform autonomous, continuous vulnerability assessment and penetration testing (VAPT) on a target network environment while optimizing for cost, quality, and resilience.

#### Adversary Capabilities (The System)
- **Target Access**: The system is granted network-level access to target assets (web servers, databases, internal APIs).
- **Tool Suite**: The system can execute a suite of security tools (nmap, sqlmap, exploit-db) via specialized agents.
- **LLM Access**: The system utilizes multiple LLM providers (e.g., OpenAI, Google, Anthropic, Ollama) for reasoning and decision-making.

#### System Assumptions & Constraints
- **Provider Volatility**: LLM API providers are assumed to be unreliable, experiencing periodic outages, rate limits, or latency spikes.
- **Financial Constraints**: The system must operate within a predefined cost budget, preventing the indiscriminate use of flagship models for simple tasks.
- **Safety Constraints**: Destructive actions (e.g., buffer overflows, database deletions) are gated by a human-in-the-loop (HITL) approval process.

#### Adversarial Scenarios
1.  **Scenario A: Provider Failure**: A primary LLM provider (e.g., GPT-4o) goes offline during an active multi-stage exploit chain.
2.  **Scenario B: Budget Exhaustion**: An extensive reconnaissance phase on a large network exhausts the budget due to suboptimal model selection.
3.  **Scenario C: Reasoning Hallucination**: A lower-tier "Flash" model suggests incorrect or dangerous commands for a complex vulnerability.

### 2. Research Questions (RQs)
- **RQ1 (Operational Resilience)**: How effectively can a provider-agnostic failover mechanism maintain operational continuity and state during unplanned LLM provider outages compared to monolithic, single-provider systems?
- **RQ2 (Cost-Reasoning Optimization)**: To what extent can **Dynamic Complexity-Aware Tiering (DCAT)** reduce total inference costs while maintaining a reasoning success rate equivalent to a unified flagship-model deployment?
- **RQ3 (Scalability and Caching)**: What is the impact of **Security-Semantic Caching (SSC)** on the performance and cost-efficiency of large-scale, redundant security assessments on heterogeneous network infrastructures?
- **RQ4 (Safety & Governance)**: Can a stateful graph-based orchestration framework with HITL gates effectively mitigate the risk of unintended destructive actions during autonomous exploitation?

### 3. Expected Outcomes
- **Outcome 1**: Validation that the failover engine achieves <2s MTTR with zero state loss.
- **Outcome 2**: Demonstrable 80%+ cost savings using DCAT for reconnaissance and low-complexity tasks.
- **Outcome 3**: Significant latency reduction (30%+) for redundant scans using SSC.
- **Outcome 4**: 100% adherence to safety constraints through the centralized gate mechanism.

## Key Decisions Made
- Focused the Research Questions on the **System-Level** attributes (Resilience, Optimization, Scalability) to align with the core contributions in Step 3b.
- Included **RQ4** to address the critical "Safety" requirement for autonomous red teaming in IEEE publications.
- Grounded the adversary model in "Operational Realism"—treating provider outages as a standard threat to autonomous workflows.

## Open Questions
- Should we define a "Network Defender" adversary who attempts to block the LLMOrch-VAPT system? (Decided: No, focus on the system's own operational threats to keep the scope controlled).

## Checklist Results
- [PASS] Step 3b contributions used as input
- [PASS] Threat model clearly defined (system goal, capabilities, constraints)
- [PASS] Adversary model described (system assumptions)
- [PASS] 3–4 rigorous Research Questions (RQs) formulated
- [PASS] RQs are directly testable and mapping to contributions
- [PASS] Expected outcomes for each RQ are listed
- [PASS] Artifact saved as `artifacts/step-3c-threat-model-rqs.md`

## Input for Next Step
Synthesis of the RQs (Step 3c) into the high-level "Paper Outline" (Step 4a). This will define the structure of the manuscript and how each section addresses the RQs.
