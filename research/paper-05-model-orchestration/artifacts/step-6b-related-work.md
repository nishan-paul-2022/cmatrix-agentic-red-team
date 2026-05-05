# [STEP 6b] — Background & Related Work

## Summary
Completed the formal drafting of the Background and Related Work section for the LLMOrch-VAPT research paper. The section provides a critical synthesis of the literature across three clusters: LLM Routing, Autonomous Security Agents, and Stateful Orchestration. It explicitly identifies the "Operational Gap" in current SOTA and positions LLMOrch-VAPT as the infrastructure-first solution to these problems.

## Full Output

### 1. Key Syntheses
- **Routing**: Contrasted generic routing (FrugalGPT/RouteLLM) with our security-domain-specific logic (**DCAT**).
- **Security Agents**: Contrasted current "Attack Intelligence" focus (PentestGPT/PentestMCP) with our focus on **Operational Infrastructure and Resilience**.
- **Orchestration**: Showed how we synthesize ReWOO and ToT patterns into a resilient master-worker hierarchy.

### 2. LaTeX Source
The content has been saved to: `sections/02-related-work.tex`.

### 3. Highlights from the Section
- **The "Operational Gap"**: Dedicated a separate sub-section (§II-D) to explicitly define the research void that LLMOrch-VAPT fills.
- **2025 SOTA Inclusion**: Integrated the latest research found in Step 2b (PentestMCP, PentestAgent, UniRoute) to ensure the paper is cutting-edge.
- **Resilience Narrative**: Framed the **APF (Failover)** engine as the primary differentiator against all existing security agents.
- **Efficiency Narrative**: Framed **SSC (Caching)** as an extension of the ReWOO reasoning pattern for redundant tasks.

## Key Decisions Made
- Used a **"Synthesis-over-List"** approach to ensure the reviewer understands the evolution and the niche.
- Highlighted the **"Provider Volatility"** problem as the primary motivator for our architectural decisions.
- Ensured all citations from `references.bib` are properly mapped to the technical narrative.

## Open Questions
- None.

## Checklist Results
- [PASS] Step 2c (Related Work Map) used as input
- [PASS] Section is structured into logical clusters (Routing, Security, Orchestration)
- [PASS] Narrative is critical and synthesised (not just a list of papers)
- [PASS] Latest 2024-2025 research is integrated
- [PASS] Research gap is clearly identified and emphasized
- [PASS] LaTeX saved in `sections/02-related-work.tex`
- [PASS] Artifact saved as `artifacts/step-6b-related-work.md`

## Input for Next Step
Synthesis of the threat model and RQs (Step 3c) into the formal "Threat Model" section (Step 6c). This will define the security assumptions and adversary capabilities.
