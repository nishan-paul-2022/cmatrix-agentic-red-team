# [STEP 6b] — Related Work + Methodology — OUTPUT ARTIFACT

## 1) Summary
This sub-step finalized the academic and technical heart of the manuscript. We drafted the Related Work section, categorizing the landscape into reasoning patterns, autonomous agents, and agentic security defenses. We also drafted the Methodology section, integrating the formal threat model, system architecture, and the composite reasoning orchestration algorithm. All assets (Table 01, Figures 01-03, Algorithm 01) were successfully integrated into the modular LaTeX files.

## 2) Full Output

### 2.1 Finalized Related Work
- §2.1: LLM Reasoning Patterns (Grounded in ToT, ReWOO, Reflexion).
- §2.2: Autonomous VAPT Agents (Positioned against PentestGPT and AutoAttacker).
- §2.3: Agentic Security (Distinguished CMatrix as internal governance vs. external defense).
- Integrated `table-01-related-work-comparison.tex`.

### 2.2 Finalized Methodology
- §3.1: Threat Model (Grounded in the trust boundary defined in 3c).
- §3.2: System Architecture (Detailed the Master-Worker hierarchy and LangGraph state machine).
- §3.3: Composite Reasoning Pipeline (Formalized the sequence of ToT -> ReWOO -> Reflexion).
- Integrated `figure-01`, `figure-02`, `figure-03`, and `algorithm-01`.

## 3) Key Decisions Made
- **Internal vs. External Governance**: Explicitly framed the HITL gate as an "Internal Governance" mechanism to contrast with the "External Defenses" (Honeytokens, etc.) found in recent SOTA, strengthening our novelty claim.
- **Algorithm Packages**: Added `algorithm` and `algpseudocode` to `main.tex` to support the technical rendering of the orchestration logic.
- **Path Correction**: Updated `\input` paths to `../assets/` to reflect the project's subdirectory structure.

## 4) Open Questions
- **Figure Layout**: Should Figure 01 and Figure 02 be placed in a `[t!]` (top of page) position to save vertical space, or keep as `[htbp]`?
- **Algorithm Rigor**: Is the use of `\Require` and `\Ensure` in Alg 01 standard for S&P, or should we use more verbal descriptors?

## 5) Checklist Results (PASS/FAIL)
- [PASS] Related Work categorizes all SOTA from Step 2
- [PASS] Methodology describes all 5 components from Step 4a
- [PASS] Table 01 integrated into Related Work
- [PASS] Figure 01, 02, 03 integrated into Methodology
- [PASS] Algorithm 01 integrated into Methodology
- [PASS] `main.tex` updated to include modular files
- [PASS] Methodology is grounded in the actual codebase (LangGraph, ToT, etc.)

## 6) Input for Next Step (Step 6c)
- **Results Integration**: Step 6c will integrate Table 04 (Results) and Figures 04-05 (Performance Charts).
- **Discussion Integration**: Step 6c will synthesize the Discussion and Conclusion.

## 7) Asset Files Created
- `research/paper-04-agent-reasoning/content/related_work.tex`: Related work source.
- `research/paper-04-agent-reasoning/content/methodology.tex`: Methodology source.
- `research/paper-04-agent-reasoning/content/main.tex`: Updated wrapper.
