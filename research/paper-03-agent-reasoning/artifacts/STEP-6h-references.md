# [STEP 6h] — References — OUTPUT ARTIFACT

## 1) Summary
This final sub-step performed a comprehensive bibliography audit and finalized the `references.bib` file. We extracted all citation keys used across the modular manuscript sections and ensured they were correctly mapped to high-quality BibTeX entries. We added the most recent SOTA security defense citations (AgentSentinel and Cloak, Honey, Trap) to support our novelty positioning. The resulting bibliography is IEEE-compliant and ready for camera-ready compilation.

## 2) Full Output

### 2.1 Finalized Bibliography Keys
The following keys are actively referenced in the manuscript:
- **Reasoning**: `tot`, `rewoo`, `reflexion`, `selfrefine`, `react`.
- **VAPT Agents**: `pentestgpt`, `autoattacker`.
- **Security Defenses**: `agentsentinel`, `cloak`.
- **Orchestration**: `langgraph`, `routellm`, `frugalgpt`.
- **Models**: `gpt4`, `gemini`, `claude`, `llama2`.
- **Standards**: `nvd`.

### 2.2 Added Citations
- **AgentSentinel**: Haitao Hu et al., arXiv 2025.
- **Cloak, Honey, Trap**: Daniel Ayzenshteyn et al., USENIX Security 2025.

## 3) Key Decisions Made
- **2025 Inclusion**: Prioritized adding 2025 citations (AgentSentinel, Cloak) to ensure the paper feels current and addresses the very latest competitive work.
- **BibTeX Normalization**: Ensured consistent author name formatting and protected capital letters (e.g., `{LLM}`, `{AgentSentinel}`) to prevent LaTeX from lowercasing them in the final PDF.

## 4) Open Questions
- **None**: The bibliography is complete and verified against the manuscript text.

## 5) Checklist Results (PASS/FAIL)
- [PASS] Complete IEEE-formatted reference list
- [PASS] Every citation used in the paper (`tot`, `rewoo`, `cloak`, etc.) included in the BibTeX file
- [PASS] No citation included that doesn't appear in the paper (Audit performed)
- [PASS] BibTeX entries for newest 2025 papers added
- [PASS] Capitalization protection (`{...}`) applied to technical terms
- [PASS] `references.bib` updated in the `content/` directory

## 6) Input for Next Step (Final Validation)
- **PDF Compilation**: The next logical step is to run `make paper-03` to verify that all cross-references, figures, and citations render perfectly.

## 7) Asset Files Updated
- `research/paper-03-agent-reasoning/content/references.bib`: Finalized BibTeX source.
- `research/paper-03-agent-reasoning/assets/ASSET-INDEX.md`: Updated.
