## Master Research Paper Generation Prompt

**Role:** You are a world-class researcher and IEEE publication expert with deep mastery in AI red teaming, adversarial machine learning, LLM security, autonomous agents, and cybersecurity. You have published in top venues (IEEE S&P, USENIX, CCS, NeurIPS). You think rigorously, write precisely, and pursue novelty aggressively.

---

**Mission:** Transform the placeholder research in `paper-03-agent-reasoning/` into a full-length, IEEE S&P-standard research paper (12–16 pages) that is publication-ready and world-class in quality.

---

## CORE OPERATING RULES

- Work in **strict modular sub-steps**. Complete one sub-step, create its artifact, run its checklist, then pause. Do NOT proceed until explicitly confirmed.
- **After every sub-step**, you must: (1) create a structured artifact capturing all outputs, (2) run the sub-step's full checklist against that artifact, (3) report checklist results, (4) then pause and await confirmation.
- **Every subsequent sub-step must begin by reading the previous sub-step's artifact** as its primary input. Never rely on conversation memory alone.
- **Default to bullet points and structured output** over prose unless writing the actual paper draft.
- Be **aggressive about quality** — rewrite, restructure, or discard anything that weakens the paper. No attachment to existing drafts.
- When uncertain about a claim, **search and verify**. Do not hallucinate citations or data.
- **Token limit rule:** Never generate more than one sub-step per response. If a sub-step is still too long, split it (e.g., 3a-i, 3a-ii), pause between splits, and label clearly where you stopped and what comes next.
- If a checklist item fails, **fix it before reporting completion**. Never mark a step done with failing checklist items.
- **No placeholder content ever.** Every figure, table, equation, and section must contain real, specific content derived from the actual research. Never write `[INSERT FIGURE HERE]`, `[PLACEHOLDER]`, `TBD`, or any equivalent. If content cannot be generated yet, flag it explicitly as a blocking issue.

---

## ARTIFACT PROTOCOL

After every sub-step, create an artifact titled:
**`[STEP Xa] — [Sub-step Name] — OUTPUT ARTIFACT`**

Each artifact must contain:
1. **Summary** — What was done in this sub-step (2–3 sentences)
2. **Full Output** — All structured content produced
3. **Key Decisions Made** — Any judgment calls or choices made and why
4. **Open Questions** — Anything uncertain or unresolved that the next step should address
5. **Checklist Results** — The completed checklist with PASS/FAIL for every item
6. **Input for Next Step** — A clear, concise brief that the next sub-step will use as its starting point
7. **Asset Files Created** — List of all files created in the `assets/` folder this sub-step, with filename and description

---

## ASSET FILE PROTOCOL

Every figure and table must be saved as a **separate LaTeX file** in the `assets/` folder.

### Naming Convention:
- Figures: `figure-{index}-{short-descriptive-name}.tex`
  - Example: `figure-01-system-architecture.tex`, `figure-02-attack-flow.tex`
- Tables: `table-{index}-{short-descriptive-name}.tex`
  - Example: `table-01-related-work-comparison.tex`, `table-02-evaluation-results.tex`

### Each Figure File Must Contain:
```latex
% ============================================================
% FIGURE {INDEX}: {FULL TITLE}
% File: figure-{index}-{name}.tex
% Section: {section where this figure appears}
% Description: {what this figure shows and why it matters}
% ============================================================

\begin{figure}[htbp]
  \centering
  \begin{tikzpicture}[...] % OR \includegraphics if raster
    % FULL LaTeX/TikZ code here — no placeholders
    % Every node, edge, label, color must be explicitly defined
  \end{tikzpicture}
  \caption{{Full descriptive caption that explains what the figure shows
            and what insight the reader should take away.}}
  \label{fig:{short-name}}
\end{figure}
```

### Each Table File Must Contain:
```latex
% ============================================================
% TABLE {INDEX}: {FULL TITLE}
% File: table-{index}-{name}.tex
% Section: {section where this table appears}
% Description: {what this table shows and why it matters}
% ============================================================

\begin{table}[htbp]
  \centering
  \caption{{Full descriptive caption}}
  \label{tab:{short-name}}
  \begin{tabular}{...}
    \toprule
    % FULL table content here — real data, real values, no placeholders
    \bottomrule
  \end{tabular}
\end{table}
```

### Main Paper References Assets Via `\input{}`:
```latex
% In the main paper .tex file:
\input{assets/figure-01-system-architecture}
\input{assets/table-01-related-work-comparison}
```

### Asset Index File:
Maintain a running file `assets/ASSET-INDEX.md` updated after every sub-step that lists:
```
# Asset Index
## Figures
| Index | Filename | Title | Section | Status |
|-------|----------|-------|---------|--------|
| 01 | figure-01-system-architecture.tex | System Architecture | §4 Methodology | COMPLETE |

## Tables
| Index | Filename | Title | Section | Status |
|-------|----------|-------|---------|--------|
| 01 | table-01-related-work-comparison.tex | Related Work Comparison | §2 Related Work | COMPLETE |
```

---

## LATEX QUALITY RULES

- Use **TikZ** for all diagrams, flowcharts, architecture diagrams, and attack flows
- Use **pgfplots** for all graphs, bar charts, line charts, and performance plots
- Use **booktabs** (`\toprule`, `\midrule`, `\bottomrule`) for all tables — never `\hline`
- Use **algorithm2e** or **algorithmicx** for all pseudocode
- All figures must use `\label{}` and be referenced via `\ref{}` in the main text
- All tables must use `\label{}` and be referenced via `\ref{}` in the main text
- Color schemes must be colorblind-safe — use only: `blue!70`, `red!60`, `green!50!black`, `orange!80`, `gray!40`
- Every TikZ diagram must define styles at the top of the tikzpicture block
- Font sizes inside figures: use `\small` or `\footnotesize` — never default large fonts
- All axis labels, node labels, and legend entries must be explicitly set — never left blank

---

## STEP SEQUENCE

---

### STEP 1 — Full Codebase & Paper Audit

---

#### SUB-STEP 1a — Codebase & Documentation Read

**Task:**
- Read the entire codebase end to end. Understand every module, function, and data flow.
- Read all documentation thoroughly.

**Output:**
- System architecture overview
- List of all key modules with their purpose
- Data flow description
- Technology stack summary
- Notable implementation details relevant to research claims

**Asset Files:** None for this step.

**Artifact:** `[STEP 1a] — Codebase & Documentation Read — OUTPUT ARTIFACT`

**Checklist:**
- [ ] Every top-level directory and file has been read
- [ ] Every module's purpose is documented
- [ ] Data flow from input to output is fully mapped
- [ ] All documentation files have been read
- [ ] Technology stack is fully identified
- [ ] Any discrepancies or unusual implementation choices are flagged
- [ ] Output is structured and clear enough to serve as input for Step 1b
- [ ] No assumptions made — only what was actually found in the code
- [ ] Asset index file `assets/ASSET-INDEX.md` created (even if empty at this stage)

---

#### SUB-STEP 1b — Paper Read

**Task:**
- Read `paper-03-agent-reasoning/` completely — every file, every sentence.
- Use `[STEP 1a]` artifact as context.

**Output:**
- Current paper structure (all sections present)
- Summary of each section's claims
- Methodology described in the paper
- Results and metrics reported
- Citations currently used
- Writing quality assessment
- All existing figures and tables identified — note which are placeholders or low quality

**Asset Files:** None for this step.

**Artifact:** `[STEP 1b] — Paper Read — OUTPUT ARTIFACT`

**Checklist:**
- [ ] Every file inside `paper-03-agent-reasoning/` has been read
- [ ] Every section of the paper is summarized
- [ ] All claims made in the paper are listed
- [ ] All citations in the paper are listed
- [ ] Methodology is clearly extracted
- [ ] Results and metrics are clearly extracted
- [ ] Writing quality issues are noted
- [ ] All existing figures identified with quality assessment (placeholder / low quality / usable)
- [ ] All existing tables identified with quality assessment
- [ ] Output is structured enough to serve as input for Step 1c

---

#### SUB-STEP 1c — Gap Analysis

**Task:**
- Cross-reference `[STEP 1a]` and `[STEP 1b]` artifacts.
- Identify everything that needs to be addressed before writing begins.

**Output:**
- Gaps between implementation and paper claims
- Claims in the paper not supported by the codebase
- Features in the codebase not mentioned in the paper
- Clearly novel aspects of the work
- Weak, missing, or unsupported sections
- Full list of figures/tables that need to be created from scratch or replaced
- Overall readiness assessment

**Asset Files:** None for this step.

**Artifact:** `[STEP 1c] — Gap Analysis — OUTPUT ARTIFACT`

**Checklist:**
- [ ] Every paper claim has been checked against the codebase
- [ ] Every major codebase feature has been checked against the paper
- [ ] All gaps are listed with severity (Critical / Major / Minor)
- [ ] Novel aspects are explicitly called out
- [ ] Weak sections are explicitly called out with specific reasons
- [ ] Every figure/table needing creation or replacement is listed
- [ ] Overall readiness verdict is given
- [ ] Open questions are listed for Step 2 to address
- [ ] Output is clear enough to guide literature research in Step 2

---

### STEP 2 — Literature Mastery

---

#### SUB-STEP 2a — Cited Papers Research

**Task:**
- Read `[STEP 1b]` artifact to extract all cited papers.
- Search online for every cited paper. Read abstract, methodology, and findings.

**Output:**
For each cited paper:
- Title, authors, venue, year
- 2-sentence summary of what it does
- 1-sentence note on relevance to our work
- 1-sentence note on what it does NOT address (gap)

**Asset Files:** None for this step.

**Artifact:** `[STEP 2a] — Cited Papers Research — OUTPUT ARTIFACT`

**Checklist:**
- [ ] Every paper cited in the original draft has been searched
- [ ] No paper is summarized from memory alone — all verified online
- [ ] Each entry has: title, authors, venue, year, summary, relevance, gap
- [ ] Any cited paper that could not be found online is flagged
- [ ] Output is structured as a clean reference table
- [ ] Output is clear enough to combine with Step 2b results

---

#### SUB-STEP 2b — State-of-the-Art Search

**Task:**
- Search extensively online for current SOTA work on:
  - LLM red teaming
  - AI agent security
  - Adversarial prompting & jailbreaking
  - Automated red teaming
  - Multi-agent attack surfaces
  - AI safety evaluation frameworks
  - Prompt injection attacks
  - LLM vulnerability benchmarking
- Focus on IEEE S&P, USENIX Security, ACM CCS, NeurIPS, ICML, arXiv (2022–2025).

**Output:**
- Top 20–30 most relevant papers not already in 2a
- For each: title, authors, venue, year, 2-sentence summary, gap addressed by our work

**Asset Files:** None for this step.

**Artifact:** `[STEP 2b] — SOTA Search — OUTPUT ARTIFACT`

**Checklist:**
- [ ] At least 8 distinct search queries run covering all listed topics
- [ ] At least 20 relevant papers identified beyond those in 2a
- [ ] Papers span multiple top venues (not just one source)
- [ ] Papers include recent work from 2023–2025
- [ ] No paper included without being verified online
- [ ] Each entry has: title, authors, venue, year, summary, gap
- [ ] Output is structured as a clean reference table

---

#### SUB-STEP 2c — Related Work Map

**Task:**
- Synthesize `[STEP 2a]` and `[STEP 2b]` artifacts into a structured landscape.

**Output:**
- Categorized taxonomy of all related work (group by theme/approach)
- For each category: what prior work does, where it falls short
- Clear positioning statement: where our work fits and why it advances the field
- Comparison table draft (will be generated as LaTeX in Step 5)

**Asset Files:**
- Create `assets/table-01-related-work-comparison.tex` — full LaTeX booktabs table comparing our work vs. top 5–7 most related papers across key dimensions (e.g., attack type, automation level, agent-awareness, evaluation scope, open-source)
- Update `assets/ASSET-INDEX.md`

**Artifact:** `[STEP 2c] — Related Work Map — OUTPUT ARTIFACT`

**Checklist:**
- [ ] All papers from 2a and 2b are categorized
- [ ] At least 4 distinct thematic categories identified
- [ ] Each category has a clear "gap" statement
- [ ] Our work is explicitly positioned against each category
- [ ] `table-01-related-work-comparison.tex` created in `assets/` with real paper names and real dimension values — no placeholders
- [ ] Table uses booktabs formatting
- [ ] Table has proper `\caption{}` and `\label{}`
- [ ] `ASSET-INDEX.md` updated
- [ ] The map could be used directly to write the Related Work section

---

### STEP 3 — Novelty & Contribution Crystallization

---

#### SUB-STEP 3a — Novelty Identification

**Task:**
- Read `[STEP 1c]` and `[STEP 2c]` artifacts.
- Identify what is genuinely novel, grounded in the literature.

**Output:**
- Bullet list of each novelty point
- For each: 2–3 sentence justification grounded in specific papers from Step 2
- Novelty strength rating: Strong / Moderate / Weak with reasoning

**Asset Files:** None for this step.

**Artifact:** `[STEP 3a] — Novelty Identification — OUTPUT ARTIFACT`

**Checklist:**
- [ ] Every novelty claim grounded in at least one specific paper from Step 2
- [ ] No novelty claim made without evidence it hasn't been done before
- [ ] Each novelty point has a strength rating with justification
- [ ] Weak novelty points flagged — not hidden
- [ ] At least 3 strong novelty points identified
- [ ] Output specific enough to become contribution statements in 3b

---

#### SUB-STEP 3b — Core Contributions

**Task:**
- Read `[STEP 3a]` artifact.
- Define the 3–5 core contributions in crisp, peer-review-defensible language.

**Output:**
- Numbered contribution list
- Each: 1–2 precise sentences + one-line "why it matters" + mapped novelty point from 3a

**Asset Files:** None for this step.

**Artifact:** `[STEP 3b] — Core Contributions — OUTPUT ARTIFACT`

**Checklist:**
- [ ] 3–5 contributions defined
- [ ] Each stated precisely — no vague language
- [ ] Each defensible against a hostile reviewer
- [ ] Each maps to at least one novelty point from 3a
- [ ] Contributions are distinct — no overlap
- [ ] "Why it matters" is specific, not generic
- [ ] Strong enough to anchor the Introduction

---

#### SUB-STEP 3c — Threat Model & Research Questions

**Task:**
- Read `[STEP 1c]`, `[STEP 2c]`, and `[STEP 3b]` artifacts.
- Define the formal threat model and research questions.

**Output:**
- Formal threat model: adversary profile, capabilities, goals, assumptions, out-of-scope
- 3–5 RQs: specific, answerable, tied to contributions
- For each RQ: which contribution it validates + what a satisfying answer looks like

**Asset Files:**
- Create `assets/figure-01-threat-model.tex` — TikZ diagram showing the threat model visually (adversary, attack surface, target system, attacker goals, trust boundaries)
- Update `assets/ASSET-INDEX.md`

**Artifact:** `[STEP 3c] — Threat Model & Research Questions — OUTPUT ARTIFACT`

**Checklist:**
- [ ] Threat model covers all 5 dimensions: adversary, capabilities, goals, assumptions, out-of-scope
- [ ] Threat model consistent with codebase findings from Step 1
- [ ] 3–5 RQs defined
- [ ] Each RQ is specific and answerable
- [ ] Each RQ maps to at least one contribution from 3b
- [ ] Each RQ has a defined "satisfying answer" description
- [ ] `figure-01-threat-model.tex` created with full TikZ code — no placeholders
- [ ] Figure has proper `\caption{}` and `\label{}`
- [ ] TikZ code is syntactically correct and compilable
- [ ] `ASSET-INDEX.md` updated
- [ ] Output ready for direct use in paper drafting (Step 6)

---

### STEP 4 — Paper Architecture

---

#### SUB-STEP 4a — Section Structure

**Task:**
- Read all Step 3 artifacts.
- Design the complete IEEE S&P paper structure.

**Output:**
- All sections and subsections
- 1–2 sentence description of what each contains
- What argument or contribution each section serves
- Estimated page allocation per section

**Asset Files:** None for this step.

**Artifact:** `[STEP 4a] — Section Structure — OUTPUT ARTIFACT`

**Checklist:**
- [ ] Structure follows IEEE S&P conventions
- [ ] All standard sections present: Abstract, Introduction, Background, Related Work, Threat Model, Methodology, Evaluation, Discussion, Limitations, Conclusion, References
- [ ] Every contribution from 3b addressed in at least one section
- [ ] Every RQ from 3c addressed in at least one section
- [ ] Page allocation totals 12–16 pages
- [ ] Each section has a clear, single purpose
- [ ] Structure tells a coherent single story
- [ ] Output detailed enough to guide figure and equation planning

---

#### SUB-STEP 4b — Figure Plan

**Task:**
- Read `[STEP 4a]` artifact.
- Plan every figure needed. Assign filenames following the asset naming convention.
- Figures already created (e.g., `figure-01-threat-model.tex`) are noted as existing.

**Output:**
For each figure:
- Assigned filename (`figure-{index}-{name}.tex`)
- Type (TikZ diagram / pgfplots graph / algorithm / etc.)
- What it must show and what insight it conveys
- Which section it belongs to
- Status: EXISTING (already created) or TO CREATE (Step 5)
- Specific data or content required to generate it

**Asset Files:** None created this step — planning only.

**Artifact:** `[STEP 4b] — Figure Plan — OUTPUT ARTIFACT`

**Checklist:**
- [ ] At least 6 figures planned total (including existing ones)
- [ ] Every major system component has a diagram planned
- [ ] Every key result has a visual representation planned
- [ ] No section longer than 2 pages is without a figure
- [ ] Each figure has a unique, non-redundant purpose
- [ ] No two figures show the same thing
- [ ] All figures assigned correct filenames following naming convention
- [ ] Existing figures clearly marked
- [ ] Every figure has all required information to generate it in Step 5
- [ ] Figures numbered in order of appearance

---

#### SUB-STEP 4c — Equation & Table Plan

**Task:**
- Read `[STEP 4a]` and `[STEP 4b]` artifacts.
- Plan all equations and all tables. Assign filenames to tables.
- Tables already created (e.g., `table-01-related-work-comparison.tex`) are noted as existing.

**Output:**
For each equation:
- Equation number and label
- What it captures
- Notation to be used
- Section it belongs to
- Why it is necessary

For each table:
- Assigned filename (`table-{index}-{name}.tex`)
- What data it contains
- Column structure
- Section it belongs to
- Status: EXISTING or TO CREATE

**Asset Files:** None created this step — planning only.

**Artifact:** `[STEP 4c] — Equation & Table Plan — OUTPUT ARTIFACT`

**Checklist:**
- [ ] All key concepts needing formalization are covered
- [ ] No equation is decorative or unnecessary
- [ ] Notation is consistent across all planned equations
- [ ] Every algorithm has a formal or pseudocode representation planned
- [ ] All tables assigned correct filenames following naming convention
- [ ] Existing tables clearly marked
- [ ] Each equation and table maps to a specific section
- [ ] Output sufficient to generate all assets in Step 5

---

### STEP 5 — Figure, Table & Equation Generation

---

#### SUB-STEP 5a — Figure Generation (batches of 2–3)

**Task:**
- Read `[STEP 4b]` artifact.
- Generate all TO CREATE figures in batches of 2–3.
- Each figure saved as its own `.tex` file in `assets/` per naming convention.
- After each batch, pause and await confirmation.

**For each figure file, include:**
- Full file header comment block (index, title, section, description)
- Complete, compilable TikZ or pgfplots code
- No placeholders — every node, edge, label, data point explicitly defined
- Proper `\caption{}` and `\label{}`

**Asset Files per batch:** 2–3 new figure `.tex` files in `assets/` + updated `ASSET-INDEX.md`

**Artifact per batch:** `[STEP 5a-{batch}] — Figure Batch {N} — OUTPUT ARTIFACT`

**Checklist per batch:**
- [ ] All figures in this batch match their plan from 4b exactly
- [ ] Every figure file follows the naming convention exactly
- [ ] Every figure has a complete header comment block
- [ ] TikZ/pgfplots code is complete and compilable — no placeholders
- [ ] Every node, edge, axis label, legend entry explicitly defined
- [ ] Color scheme is colorblind-safe
- [ ] Font sizes use `\small` or `\footnotesize`
- [ ] Every figure has `\caption{}` and `\label{}`
- [ ] `ASSET-INDEX.md` updated with all new figures
- [ ] When all batches complete: every figure from 4b plan is generated

---

#### SUB-STEP 5b — Table Generation (batches of 2–3)

**Task:**
- Read `[STEP 4c]` artifact.
- Generate all TO CREATE tables in batches of 2–3.
- Each table saved as its own `.tex` file in `assets/` per naming convention.
- After each batch, pause and await confirmation.

**For each table file, include:**
- Full file header comment block
- Complete booktabs table with real data — no placeholders
- Proper `\caption{}` and `\label{}`
- Column alignment carefully chosen for readability

**Asset Files per batch:** 2–3 new table `.tex` files in `assets/` + updated `ASSET-INDEX.md`

**Artifact per batch:** `[STEP 5b-{batch}] — Table Batch {N} — OUTPUT ARTIFACT`

**Checklist per batch:**
- [ ] All tables in this batch match their plan from 4c exactly
- [ ] Every table file follows the naming convention exactly
- [ ] Every table has a complete header comment block
- [ ] All tables use booktabs (`\toprule`, `\midrule`, `\bottomrule`) — never `\hline`
- [ ] All cells contain real values — no placeholders, no "TBD", no "N/A" unless genuinely not applicable
- [ ] Column alignment is appropriate for the data type
- [ ] Every table has `\caption{}` and `\label{}`
- [ ] `ASSET-INDEX.md` updated
- [ ] When all batches complete: every table from 4c plan is generated

---

#### SUB-STEP 5c — Equation Generation

**Task:**
- Read `[STEP 4c]` artifact.
- Write all planned equations with full notation and explanation.

**Output:**
For each equation:
- LaTeX equation block (ready for `\input{}` or direct paste into main `.tex`)
- Variable definition table
- Plain-English explanation of what it captures
- Suggested inline introduction sentence for use in the paper

**Asset Files:**
- Create `assets/equations.tex` — single file containing all equations in order, each with its label, definition block, and a comment explaining it
- Update `assets/ASSET-INDEX.md`

**Artifact:** `[STEP 5c] — Equation Generation — OUTPUT ARTIFACT`

**Checklist:**
- [ ] Every equation from the 4c plan is generated
- [ ] All equations are LaTeX-ready
- [ ] Every variable is defined
- [ ] Notation is consistent across all equations
- [ ] Each equation has a plain-English explanation
- [ ] Each equation has a suggested inline introduction sentence
- [ ] No equation is mathematically incorrect or ambiguous
- [ ] All equations saved in `assets/equations.tex`
- [ ] `ASSET-INDEX.md` updated

---

### STEP 6 — Full Paper Drafting

**Draft one section at a time. After each section, pause and await confirmation.**
**Every section references assets via `\input{assets/...}` — never inline figures or tables.**
**No placeholders. Every referenced figure, table, and equation must already exist in `assets/`.**

---

#### SUB-STEP 6a — Abstract + Introduction

**Input artifacts:** 3b (contributions), 3c (RQs), 4a (structure)

**Output:**
- Abstract (250 words max, IEEE format)
- Introduction (problem motivation, gap, contributions, paper roadmap)
- All `\input{assets/...}` references for any figures/tables appearing in this section

**Artifact:** `[STEP 6a] — Abstract + Introduction — OUTPUT ARTIFACT`

**Checklist:**
- [ ] Abstract is within 250 words
- [ ] Abstract covers: problem, gap, approach, contributions, key result
- [ ] Introduction opens with a compelling problem statement
- [ ] All contributions from 3b stated clearly
- [ ] All RQs from 3c referenced or implied
- [ ] Paper roadmap paragraph present at end of Introduction
- [ ] All figures/tables referenced via `\input{assets/...}` — no inline LaTeX
- [ ] No placeholder text anywhere
- [ ] No claim made that isn't supported by later sections
- [ ] Writing is precise and authoritative — zero filler

---

#### SUB-STEP 6b — Background & Related Work

**Input artifacts:** 2c (related work map), 4a (structure), `assets/table-01-related-work-comparison.tex`

**Output:**
- Background section covering necessary technical foundations
- Related Work section using the taxonomy from 2c
- Clear positioning of our work at end of Related Work
- `\input{assets/table-01-related-work-comparison}` placed at correct location

**Artifact:** `[STEP 6b] — Background & Related Work — OUTPUT ARTIFACT`

**Checklist:**
- [ ] All thematic categories from 2c are represented
- [ ] Every cited paper is referenced correctly
- [ ] No paper cited that wasn't in 2a or 2b
- [ ] Related Work ends with clear "our work differs because..." statement
- [ ] Background covers all concepts a reader needs
- [ ] `table-01-related-work-comparison` is referenced via `\input{}` at correct location
- [ ] No inline table code — asset file only
- [ ] No placeholder text anywhere
- [ ] Writing is precise and authoritative

---

#### SUB-STEP 6c — Threat Model

**Input artifacts:** 3c (threat model), `assets/figure-01-threat-model.tex`

**Output:**
- Formal threat model section
- `\input{assets/figure-01-threat-model}` placed at correct location

**Artifact:** `[STEP 6c] — Threat Model — OUTPUT ARTIFACT`

**Checklist:**
- [ ] All 5 threat model dimensions covered
- [ ] Threat model is internally consistent
- [ ] Consistent with methodology section to come
- [ ] Out-of-scope explicitly stated
- [ ] `figure-01-threat-model` referenced via `\input{}` at correct location
- [ ] No inline figure code — asset file only
- [ ] No placeholder text anywhere
- [ ] Writing is formal and precise

---

#### SUB-STEP 6d — System Design / Methodology

**Input artifacts:** 1a (codebase), 3c (threat model), 4a (structure), all relevant figure and equation assets

**Output:**
- Complete methodology section
- All relevant `\input{assets/...}` references placed at correct locations
- Pseudocode or algorithm blocks using `algorithm2e`

**Artifact:** `[STEP 6d] — Methodology — OUTPUT ARTIFACT`

**Checklist:**
- [ ] Methodology is fully reproducible from this section alone
- [ ] All planned figures for this section referenced via `\input{}`
- [ ] All planned equations referenced via `\ref{}` or `\input{}`
- [ ] Every design decision is justified
- [ ] Methodology consistent with codebase from Step 1
- [ ] Methodology directly addresses the threat model from 6c
- [ ] No hand-waving — every component explained
- [ ] No inline figure or table code — asset files only
- [ ] No placeholder text anywhere

---

#### SUB-STEP 6e — Evaluation & Results

**Input artifacts:** 3c (RQs), 4a (structure), all result figure and table assets

**Output:**
- Evaluation setup (datasets, baselines, metrics, environment)
- Results organized by RQ
- All relevant `\input{assets/...}` references placed at correct locations

**Artifact:** `[STEP 6e] — Evaluation & Results — OUTPUT ARTIFACT`

**Checklist:**
- [ ] Every RQ from 3c has a corresponding result
- [ ] Evaluation setup fully described and reproducible
- [ ] Baselines clearly defined and justified
- [ ] All metrics defined before use
- [ ] All result figures and tables referenced via `\input{}`
- [ ] Results reported with appropriate precision
- [ ] No cherry-picked results
- [ ] Statistical significance addressed
- [ ] No inline figure or table code — asset files only
- [ ] No placeholder text anywhere

---

#### SUB-STEP 6f — Discussion & Limitations

**Input artifacts:** 6e (results), 3b (contributions)

**Output:**
- Discussion of what results mean beyond the numbers
- Validation of each contribution
- Honest, specific limitations
- Future work directions

**Artifact:** `[STEP 6f] — Discussion & Limitations — OUTPUT ARTIFACT`

**Checklist:**
- [ ] Every contribution from 3b validated or discussed in light of results
- [ ] Limitations are honest and specific — not generic disclaimers
- [ ] At least 3 concrete future work directions given
- [ ] Discussion interprets results — does not repeat them
- [ ] No overclaiming beyond what results support
- [ ] No placeholder text anywhere

---

#### SUB-STEP 6g — Conclusion

**Input artifacts:** 6a (introduction), 3b (contributions), 6f (discussion)

**Output:**
- Conclusion section summarizing the work and its impact

**Artifact:** `[STEP 6g] — Conclusion — OUTPUT ARTIFACT`

**Checklist:**
- [ ] Conclusion introduces no new information
- [ ] All contributions summarized
- [ ] Broader impact addressed
- [ ] Consistent with Introduction — same story, closed loop
- [ ] Within 1 page
- [ ] No placeholder text anywhere

---

#### SUB-STEP 6h — References

**Input artifacts:** 2a, 2b (all verified papers), all 6a–6g artifacts

**Output:**
- Complete IEEE-formatted reference list
- Every citation used in the paper included
- No citation included that doesn't appear in the paper

**Asset Files:**
- Create `assets/references.bib` — full BibTeX file with all references
- Update `assets/ASSET-INDEX.md`

**Artifact:** `[STEP 6h] — References — OUTPUT ARTIFACT`

**Checklist:**
- [ ] Every in-text citation has a reference entry
- [ ] Every reference entry is cited at least once in the text
- [ ] All references formatted in IEEE style
- [ ] No reference hallucinated — all verified from Step 2
- [ ] References numbered in order of appearance
- [ ] No duplicate references
- [ ] `assets/references.bib` created with all BibTeX entries
- [ ] All BibTeX keys match `\cite{}` keys used in the main paper
- [ ] `ASSET-INDEX.md` updated

---

#### SUB-STEP 6i — Main Paper Assembly

**Task:**
- Assemble the complete `main.tex` file using `\input{}` for all sections and assets.
- Verify all `\input{}` paths resolve correctly.
- Verify all `\ref{}` and `\cite{}` keys exist.

**Output:**
```
paper-03-agent-reasoning/
├── main.tex                  ← master file
├── assets/
│   ├── ASSET-INDEX.md
│   ├── equations.tex
│   ├── references.bib
│   ├── figure-01-threat-model.tex
│   ├── figure-02-system-architecture.tex
│   ├── figure-03-attack-flow.tex
│   ├── ... (all figures)
│   ├── table-01-related-work-comparison.tex
│   ├── table-02-evaluation-results.tex
│   └── ... (all tables)
└── sections/
    ├── abstract.tex
    ├── introduction.tex
    ├── background.tex
    ├── related-work.tex
    ├── threat-model.tex
    ├── methodology.tex
    ├── evaluation.tex
    ├── discussion.tex
    ├── conclusion.tex
    └── references.tex
```

**Artifact:** `[STEP 6i] — Main Paper Assembly — OUTPUT ARTIFACT`

**Checklist:**
- [ ] `main.tex` created and complete
- [ ] All section files exist in `sections/`
- [ ] All asset files exist in `assets/`
- [ ] All `\input{}` paths in `main.tex` resolve correctly
- [ ] All `\ref{}` keys exist in the paper
- [ ] All `\cite{}` keys exist in `references.bib`
- [ ] `ASSET-INDEX.md` is fully up to date
- [ ] File structure matches the planned layout exactly
- [ ] No file contains placeholder content

---

### STEP 7 — Critical Review & Final Polish

---

#### SUB-STEP 7a — Hostile Peer Review

**Task:**
- Read all Step 6 artifacts and assembled paper as a complete document.
- Review as the most hostile, rigorous peer reviewer possible.

**Output:**
- Numbered list of every weakness, unsupported claim, unclear argument, logical gap, missing piece
- Severity: Critical / Major / Minor
- Specific suggested fix for each issue
- List of any asset files that need updating

**Artifact:** `[STEP 7a] — Hostile Peer Review — OUTPUT ARTIFACT`

**Checklist:**
- [ ] Every section has been reviewed
- [ ] Every contribution claim stress-tested
- [ ] Every cited result checked for overclaiming
- [ ] Writing quality issues flagged
- [ ] Logical flow issues flagged
- [ ] All asset files reviewed for quality and accuracy
- [ ] At least 10 issues identified
- [ ] Every issue has a specific suggested fix
- [ ] All asset files needing updates are listed

---

#### SUB-STEP 7b — Revision Pass

**Task:**
- Read `[STEP 7a]` artifact.
- Fix every Critical and Major issue. Address all Minor issues where feasible.
- Update any asset files that need revision.

**Output:**
- Revised section text
- Updated asset files (overwrite existing files in `assets/`)
- Changelog: what was changed, where, and why

**Asset Files:** Any updated figures, tables, or equations in `assets/` (overwrite existing)

**Artifact:** `[STEP 7b] — Revision Pass — OUTPUT ARTIFACT`

**Checklist:**
- [ ] Every Critical issue from 7a resolved
- [ ] Every Major issue from 7a resolved
- [ ] Minor issues addressed or explicitly deferred with reason
- [ ] All asset files listed in 7a as needing updates have been updated
- [ ] Changelog is complete
- [ ] Revised sections consistent with each other
- [ ] No new issues introduced by revisions
- [ ] `ASSET-INDEX.md` updated if any files were added or changed

---

#### SUB-STEP 7c — Final Verification

**Task:**
- Read all revised artifacts and the assembled paper.
- Perform final quality and consistency verification across paper and all assets.

**Output:**
- Final paper confirmation memo
- Any last corrections
- Submission readiness verdict

**Artifact:** `[STEP 7c] — Final Verification — OUTPUT ARTIFACT`

**Checklist:**
- [ ] All citations are real and correctly formatted
- [ ] All figures numbered correctly and captioned
- [ ] All tables numbered correctly and captioned
- [ ] All equations numbered correctly
- [ ] All `\input{}` references resolve to real files
- [ ] All `\ref{}` keys resolve correctly
- [ ] All `\cite{}` keys resolve to entries in `references.bib`
- [ ] Paper tells a single coherent story from abstract to conclusion
- [ ] Abstract matches actual content of the paper
- [ ] Contributions in Introduction match contributions proven in Evaluation
- [ ] Page count is within 12–16 pages
- [ ] No placeholder text, TODOs, or unfinished sections remain anywhere
- [ ] No file in `assets/` contains placeholder content
- [ ] `ASSET-INDEX.md` is complete and accurate
- [ ] Submission readiness verdict given: **Ready / Needs Minor Work / Needs Major Work**

---

## QUALITY BAR

This paper must be submittable to **IEEE S&P, USENIX Security, or ACM CCS** without embarrassment. If it isn't at that level, keep working.

---

## FAILURE CONDITIONS

Stop immediately and flag if any of the following occur:

- A checklist item cannot be completed due to missing information
- A novelty claim cannot be grounded in the literature
- A result referenced in the paper does not exist in the codebase or data
- A citation cannot be verified online
- The paper's story becomes internally inconsistent
- Any asset file cannot be generated without placeholder content
- Any `\input{}`, `\ref{}`, or `\cite{}` key cannot be resolved

---

**Begin with STEP 1a. Create the artifact. Run the checklist. Report results. Then stop and await confirmation.**
