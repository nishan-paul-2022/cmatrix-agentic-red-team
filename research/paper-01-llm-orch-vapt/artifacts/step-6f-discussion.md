# [STEP 6f] — Discussion & Limitations

## Summary
Completed the formal drafting of the Discussion and Limitations section for the LLMOrch-VAPT research paper. This section addresses the broader implications of autonomous VAPT, including ethical governance, dual-use mitigation, and the technical bottlenecks inherent in current LLM technologies. It reinforces the framework's commitment to "Safety-First" automation while acknowledging the challenges of business logic exploitation and context management.

## Full Output

### 1. Key Discussion Points
- **SOC Integration**: Framed the provider-agnosticism as a "Fleet Management" advantage for enterprise SOCs.
- **Ethics & Dual-Use**: Proactively addressed the dual-use risk, highlighting the **HITL Safety Gates** as a critical mitigation.
- **Democratizing Defense**: Argued that open-sourcing the platform balances the asymmetric advantage of adversaries.
- **Technical Gaps**: Identified **Context Windows** and **Business Logic** as the primary current limitations of agentic VAPT.

### 2. LaTeX Source
The content has been saved to: `sections/06-discussion.tex`.

### 3. Highlights from the Section
- **Resilience Narrative**: Re-emphasized that the stateful checkpointing is not just for outages, but for **operational continuity** (shift changes, etc.).
- **Signal Spoofing**: Introduced the novel concept of "signal spoofing" as a limitation, where defenders could bait the DCAT engine into using expensive models.
- **Future Directions**: Mapped out **Experience-based RAG** and **Prompt Injection Protection** as the next logical steps for the project.

## Key Decisions Made
- Used a **"Responsible Research"** tone to satisfy the ethical review requirements of top-tier conferences (IEEE S&P, USENIX).
- Explicitly listed the **Limitations** to provide a balanced and credible academic perspective.
- Focused the Future Work on **technical extensions** (RAG/Security) rather than generic "more data" or "better models."

## Open Questions
- None.

## Checklist Results
- [PASS] Step 4a structure used as input
- [PASS] Covers Ethics, Dual-use, Operational continuity, and Technical limitations
- [PASS] Narrative is professional, balanced, and world-class
- [PASS] Identifies at least 3 concrete technical limitations
- [PASS] Proposes clear future research directions
- [PASS] LaTeX saved in `sections/06-discussion.tex`
- [PASS] Artifact saved as `artifacts/step-6f-discussion.md`

## Input for Next Step
Synthesis of the entire narrative (Steps 6a-6f) into the "Conclusion" (Step 6g). This will provide the final summary and parting impact statement.
