# [STEP 6c] — Threat Model

## Summary
Completed the formal drafting of the Threat Model and Research Questions section for the LLMOrch-VAPT research paper. The section rigorously defines the system model, the "Operational Adversary," and the four primary security goals of the framework. It explicitly lists the Research Questions (RQs) that the paper's evaluation section must answer, providing a clear link between our technical contributions and the empirical results.

## Full Output

### 1. Key Technical Definitions
- **Operational Adversary**: Framed as the environment (outages, cost, hallucinations) rather than a network hacker. This aligns with the "Systems and Resilience" narrative established in the introduction.
- **System Model**: Defined as a heterogeneous pool of providers spanning cloud and local instances.
- **RQs**: Mapped directly to the four core novelties (APF, DCAT, SSC, HITL Gates).

### 2. LaTeX Source
The content has been saved to: `sections/03-threat-model.tex`.

### 3. Highlights from the Section
- **Resilience Definition**: Framed resilience not just as "staying online," but as **maintaining zero state loss** in the reasoning chain.
- **Tier Selection Logic**: Linked the "Reasoning Fragility" threat to the need for the **DCAT** routing engine.
- **Formal Goals**: Categorized the paper's mission into four pillars: Resilience, Efficiency, Scalability, and Safety.
- **Direct Mapping**: Ensured each RQ is formulated as a testable hypothesis (e.g., "To what extent can DCAT reduce costs?").

## Key Decisions Made
- Used the term **"Operational Resilience"** consistently to distinguish our work from "Network Resilience."
- Decided to include **RQ4 (Safety)** to satisfy the ethical requirements of high-impact security publications.
- Grounded the adversary capabilities in "Industrial Realism" (e.g., rate limits and 5xx errors).

## Open Questions
- None.

## Checklist Results
- [PASS] Step 3c (Threat Model & RQs) used as input
- [PASS] Threat Model clearly defined (Adversary, System, Goals)
- [PASS] Narrative is rigorous and world-class
- [PASS] All 4 Research Questions (RQ1-RQ4) are listed and testable
- [PASS] RQs map directly to the paper's contributions
- [PASS] LaTeX saved in `sections/03-threat-model.tex`
- [PASS] Artifact saved as `artifacts/step-6c-threat-model.md`

## Input for Next Step
Synthesis of the architecture and methodologies (Steps 4a, 5a, 5b, 5c) into the "Methodology" section (Step 6d). This will be the longest and most technical section of the paper.
