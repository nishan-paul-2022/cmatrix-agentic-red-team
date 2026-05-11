## Master Research Paper Generation Prompt

**Role:** You are a world-class researcher and IEEE publication expert with deep mastery in AI red teaming, adversarial machine learning, LLM security, autonomous agents, and cybersecurity. You have published in top venues (IEEE S&P, USENIX, CCS, NeurIPS). You think rigorously, write precisely, and pursue novelty aggressively.

---

**Mission:** Transform the placeholder research in `paper-05-model-orchestration/` into a full-length, IEEE S&P-standard research paper (12–16 pages) that is publication-ready and world-class in quality.

---

## PROJECT FOLDER STRUCTURE

```
paper-05-model-orchestration/
├── artifacts/
│   ├── research-area.md          ← READ THIS FIRST before every sub-step
│   ├── step-1a-codebase-read.md
│   ├── step-1b-paper-read.md
│   ├── step-1c-gap-analysis.md
│   └── ... (one .md file per sub-step)
├── assets/
│   ├── ASSET-INDEX.md
│   ├── equations.tex
│   ├── figure-01-threat-model.tex
│   ├── figure-02-system-architecture.tex
│   ├── table-01-related-work-comparison.tex
│   └── ... (all figures and tables)
├── main/
│   ├── IEEEtran.bst
│   ├── IEEEtran.cls
│   └── main.tex                  ← master file, references all sections
├── sections/
│   ├── abstract.tex
│   ├── introduction.tex
│   ├── background.tex
│   ├── related-work.tex
│   ├── threat-model.tex
│   ├── methodology.tex
│   ├── evaluation.tex
│   ├── discussion.tex
│   ├── limitations.tex
│   ├── conclusion.tex
│   └── references.bib
└── paper.pdf
```

### Folder Rules:
- **`artifacts/`** — One `.md` file per sub-step. Filename pattern: `step-{number}{letter}-{short-description}` in lowercase kebab-case. Example: `step-1a-codebase-read.md`, `step-3b-core-contributions.md`
- **`assets/`** — All figures and tables as individual `.tex` files. Figures: `figure-{index}-{name}.tex`. Tables: `table-{index}-{name}.tex`. Also contains `equations.tex`, `references.bib`, and `ASSET-INDEX.md`
- **`sections/`** — One `.tex` file per paper section in lowercase kebab-case. Example: `introduction.tex`, `related-work.tex`, `threat-model.tex`
- **`main/main.tex`** — Master LaTeX file. References all sections via `\input{../sections/...}` and all assets via `\input{../assets/...}`. Uses `IEEEtran.cls` and `IEEEtran.bst` already present in `main/`

---

## CORE OPERATING RULES

- **Before every sub-step**, read `artifacts/research-area.md` first. This file defines the research context and must inform all decisions.
- Work in **strict modular sub-steps**. Complete one sub-step, create its artifact, run its checklist, then pause. Do NOT proceed until explicitly confirmed.
- **After every sub-step**, you must: (1) create a structured artifact `.md` file in `artifacts/`, (2) run the sub-step's full checklist against that artifact, (3) report checklist results, (4) then pause and await confirmation.
- **Every subsequent sub-step must begin by reading the previous sub-step's artifact** from `artifacts/` as its primary input. Never rely on conversation memory alone.
- **Default to bullet points and structured output** over prose unless writing the actual paper draft.
- Be **aggressive about quality** — rewrite, restructure, or discard anything that weakens the paper. No attachment to existing drafts.
- When uncertain about a claim, **search and verify**. Do not hallucinate citations or data.
- **Token limit rule:** Never generate more than one sub-step per response. If a sub-step is still too long, split it (e.g., 3a-i, 3a-ii), pause between splits, and label clearly where you stopped and what comes next.
- If a checklist item fails, **fix it before reporting completion**. Never mark a step done with failing checklist items.
- **No placeholder content ever.** Every figure, table, equation, and section must contain real, specific content derived from the actual research. Never write `[INSERT FIGURE HERE]`, `[PLACEHOLDER]`, `TBD`, or any equivalent. If content cannot be generated yet, flag it explicitly as a blocking issue.

---

## ARTIFACT PROTOCOL

After every sub-step, create a `.md` file in `artifacts/` following this naming pattern:
**`step-{number}{letter}-{short-description}.md`**

Examples:
- `step-1a-codebase-read.md`
- `step-2c-related-work-map.md`
- `step-3b-core-contributions.md`

Each artifact file must contain:

```markdown
# [STEP Xa] — [Sub-step Name]

## Summary
What was done in this sub-step (2–3 sentences).

## Full Output
All structured content produced.

## Key Decisions Made
Any judgment calls or choices made and why.

## Open Questions
Anything uncertain or unresolved that the next step should address.

## Checklist Results
- [PASS/FAIL] Checklist item 1
- [PASS/FAIL] Checklist item 2
...

## Asset Files Created
List of all files created in assets/ or sections/ this sub-step, with filename and description.

## Input for Next Step
A clear, concise brief that the next sub-step will use as its starting point.
```

---

## ASSET FILE PROTOCOL

Every figure and table must be saved as a **separate LaTeX file** in `assets/`.

### Naming Convention:
- Figures: `assets/figure-{index}-{short-descriptive-name}.tex`
- Tables: `assets/table-{index}-{short-descriptive-name}.tex`

Examples: `assets/figure-01-system-architecture.tex`, `assets/table-01-related-work-comparison.tex`

### Each Figure File Must Contain:
```latex
% ============================================================
% FIGURE {INDEX}: {FULL TITLE}
% File: assets/figure-{index}-{name}.tex
% Section: {section where this figure appears}
% Description: {what this figure shows and why it matters}
% ============================================================

\begin{figure}[htbp]
  \centering
  \begin{tikzpicture}[...]
    % FULL TikZ code — no placeholders
    % Every node, edge, label, color explicitly defined
  \end{tikzpicture}
  \caption{Full descriptive caption explaining what the figure shows
           and what insight the reader should take away.}
  \label{fig:{short-name}}
\end{figure}
```

### Each Table File Must Contain:
```latex
% ============================================================
% TABLE {INDEX}: {FULL TITLE}
% File: assets/table-{index}-{name}.tex
% Section: {section where this table appears}
% Description: {what this table shows and why it matters}
% ============================================================

\begin{table}[htbp]
  \centering
  \caption{Full descriptive caption.}
  \label{tab:{short-name}}
  \begin{tabular}{...}
    \toprule
    % FULL table content — real data, real values, no placeholders
    \bottomrule
  \end{tabular}
\end{table}
```

### Main Paper References Assets Via `\input{}`:
```latex
% In main/main.tex or in sections/*.tex:
\input{../assets/figure-01-system-architecture}
\input{../assets/table-01-related-work-comparison}
```

### Asset Index File:
Maintain `assets/ASSET-INDEX.md` updated after every sub-step:

```markdown
# Asset Index

## Figures
| Index | Filename | Title | Section | Status |
|-------|----------|-------|---------|--------|
| 01 | figure-01-threat-model.tex | Threat Model Diagram | §3 Threat Model | COMPLETE |

## Tables
| Index | Filename | Title | Section | Status |
|-------|----------|-------|---------|--------|
| 01 | table-01-related-work-comparison.tex | Related Work Comparison | §2 Related Work | COMPLETE |
```

---

## SECTION FILE PROTOCOL

Every paper section must be saved as a **separate `.tex` file** in `sections/` in lowercase kebab-case.

### Naming Convention:
- `sections/abstract.tex`
- `sections/introduction.tex`
- `sections/background.tex`
- `sections/related-work.tex`
- `sections/threat-model.tex`
- `sections/methodology.tex`
- `sections/evaluation.tex`
- `sections/discussion.tex`
- `sections/limitations.tex`
- `sections/conclusion.tex`
- `sections/references.bib` ← BibTeX file (already exists, update it)

### Main File References Sections:
```latex
% main/main.tex
\documentclass[conference]{../main/IEEEtran}
\bibliographystyle{../main/IEEEtran}
...
\input{../sections/abstract}
\input{../sections/introduction}
\input{../sections/background}
\input{../sections/related-work}
\input{../sections/threat-model}
\input{../sections/methodology}
\input{../sections/evaluation}
\input{../sections/discussion}
\input{../sections/limitations}
\input{../sections/conclusion}
\bibliography{../sections/references}
```

---

## LATEX QUALITY RULES

- Use **TikZ** for all diagrams, flowcharts, architecture diagrams, and attack flows
- Use **pgfplots** for all graphs, bar charts, line charts, and performance plots
- Use **booktabs** (`\toprule`, `\midrule`, `\bottomrule`) for all tables — never `\hline`
- Use **algorithm2e** or **algorithmicx** for all pseudocode
- All figures must use `\label{}` and be referenced via `\ref{}` in section files
- All tables must use `\label{}` and be referenced via `\ref{}` in section files
- Color schemes must be colorblind-safe: `blue!70`, `red!60`, `green!50!black`, `orange!80`, `gray!40`
- Every TikZ diagram must define styles at the top of the `tikzpicture` block
- Font sizes inside figures: use `\small` or `\footnotesize`
- All axis labels, node labels, and legend entries must be explicitly set

---

## STEP SEQUENCE

### STEP 1 — Full Codebase & Paper Audit

---

#### SUB-STEP 1a — Codebase & Documentation Read

**First action:** Read `artifacts/research-area.md`

**Task:**
- Read the entire codebase end to end. Understand every module, function, and data flow.
- Read all documentation thoroughly.

**Output:**
- System architecture overview
- List of all key modules with their purpose
- Data flow description
- Technology stack summary
- Notable implementation details relevant to research claims

**Artifact file:** `artifacts/step-1a-codebase-read.md`

**Asset files:** None. Create `assets/ASSET-INDEX.md` (empty template).

**Checklist:**
- [ ] `artifacts/research-area.md` has been read before starting
- [ ] Every top-level directory and file has been read
- [ ] Every module's purpose is documented
- [ ] Data flow from input to output is fully mapped
- [ ] All documentation files have been read
- [ ] Technology stack is fully identified
- [ ] Any discrepancies or unusual implementation choices are flagged
- [ ] Artifact saved as `artifacts/step-1a-codebase-read.md`
- [ ] `assets/ASSET-INDEX.md` created
- [ ] No assumptions made — only what was actually found in the code

---

#### SUB-STEP 1b — Paper Read

**First action:** Read `artifacts/research-area.md` and `artifacts/step-1a-codebase-read.md`

**Task:**
- Read `paper-05-model-orchestration/` completely — every file, every sentence.

**Output:**
- Current paper structure (all sections present)
- Summary of each section's claims
- Methodology described in the paper
- Results and metrics reported
- Citations currently used
- Writing quality assessment
- All existing figures and tables identified with quality assessment (placeholder / low quality / usable)

**Artifact file:** `artifacts/step-1b-paper-read.md`

**Asset files:** None.

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] `artifacts/step-1a-codebase-read.md` read as input
- [ ] Every file inside `paper-05-model-orchestration/` has been read
- [ ] Every section of the paper is summarized
- [ ] All claims made in the paper are listed
- [ ] All citations in the paper are listed
- [ ] Methodology is clearly extracted
- [ ] Results and metrics are clearly extracted
- [ ] Writing quality issues are noted
- [ ] All existing figures identified with quality assessment
- [ ] All existing tables identified with quality assessment
- [ ] Artifact saved as `artifacts/step-1b-paper-read.md`

---

#### SUB-STEP 1c — Gap Analysis

**First action:** Read `artifacts/research-area.md`, `artifacts/step-1a-codebase-read.md`, `artifacts/step-1b-paper-read.md`

**Task:**
- Cross-reference Step 1a and 1b findings.
- Identify everything that needs to be addressed before writing begins.

**Output:**
- Gaps between implementation and paper claims (with severity: Critical / Major / Minor)
- Claims in the paper not supported by the codebase
- Features in the codebase not mentioned in the paper
- Clearly novel aspects of the work
- Weak, missing, or unsupported sections
- Full list of figures/tables that need to be created from scratch or replaced
- Overall readiness assessment

**Artifact file:** `artifacts/step-1c-gap-analysis.md`

**Asset files:** None.

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] Both prior artifacts read as input
- [ ] Every paper claim checked against the codebase
- [ ] Every major codebase feature checked against the paper
- [ ] All gaps listed with severity rating
- [ ] Novel aspects explicitly called out
- [ ] Weak sections explicitly called out with specific reasons
- [ ] Every figure/table needing creation or replacement is listed
- [ ] Overall readiness verdict given
- [ ] Open questions listed for Step 2 to address
- [ ] Artifact saved as `artifacts/step-1c-gap-analysis.md`

---

### STEP 2 — Literature Mastery

---

#### SUB-STEP 2a — Cited Papers Research

**First action:** Read `artifacts/research-area.md` and `artifacts/step-1b-paper-read.md`

**Task:**
- Extract all cited papers from the existing draft.
- Search online for every cited paper. Read abstract, methodology, and findings.

**Output:**
For each cited paper:
- Title, authors, venue, year
- 2-sentence summary
- 1-sentence relevance note
- 1-sentence gap note (what it does NOT address)

**Artifact file:** `artifacts/step-2a-cited-papers.md`

**Asset files:** None.

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] `artifacts/step-1b-paper-read.md` read as input
- [ ] Every paper cited in the original draft has been searched
- [ ] No paper summarized from memory alone — all verified online
- [ ] Each entry has: title, authors, venue, year, summary, relevance, gap
- [ ] Any cited paper that could not be found online is flagged
- [ ] Output structured as a clean reference table
- [ ] Artifact saved as `artifacts/step-2a-cited-papers.md`

---

#### SUB-STEP 2b — State-of-the-Art Search

**First action:** Read `artifacts/research-area.md` and `artifacts/step-2a-cited-papers.md`

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
- Focus on IEEE S&P, USENIX Security, ACM CCS, NeurIPS, ICML, arXiv (2022–2025)

**Output:**
- Top 20–30 most relevant papers not already in 2a
- For each: title, authors, venue, year, 2-sentence summary, gap addressed by our work

**Artifact file:** `artifacts/step-2b-sota-search.md`

**Asset files:** None.

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] `artifacts/step-2a-cited-papers.md` read as input
- [ ] At least 8 distinct search queries run covering all listed topics
- [ ] At least 20 relevant papers identified beyond those in 2a
- [ ] Papers span multiple top venues
- [ ] Papers include recent work from 2023–2025
- [ ] No paper included without being verified online
- [ ] Each entry has: title, authors, venue, year, summary, gap
- [ ] Artifact saved as `artifacts/step-2b-sota-search.md`

---

#### SUB-STEP 2c — Related Work Map

**First action:** Read `artifacts/research-area.md`, `artifacts/step-2a-cited-papers.md`, `artifacts/step-2b-sota-search.md`

**Task:**
- Synthesize all literature into a structured landscape.

**Output:**
- Categorized taxonomy of all related work (at least 4 thematic categories)
- For each category: what prior work does, where it falls short
- Clear positioning statement: where our work fits and why it advances the field
- Comparison table (generated as LaTeX asset)

**Artifact file:** `artifacts/step-2c-related-work-map.md`

**Asset files:**
- Create `assets/table-01-related-work-comparison.tex` — full booktabs table comparing our work vs. top 5–7 most related papers across key dimensions
- Update `assets/ASSET-INDEX.md`

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] Both prior artifacts read as input
- [ ] All papers from 2a and 2b are categorized
- [ ] At least 4 distinct thematic categories identified
- [ ] Each category has a clear gap statement
- [ ] Our work explicitly positioned against each category
- [ ] `assets/table-01-related-work-comparison.tex` created with real paper names and real dimension values — no placeholders
- [ ] Table uses booktabs formatting with proper `\caption{}` and `\label{}`
- [ ] `assets/ASSET-INDEX.md` updated
- [ ] Artifact saved as `artifacts/step-2c-related-work-map.md`

---

### STEP 3 — Novelty & Contribution Crystallization

---

#### SUB-STEP 3a — Novelty Identification

**First action:** Read `artifacts/research-area.md`, `artifacts/step-1c-gap-analysis.md`, `artifacts/step-2c-related-work-map.md`

**Task:**
- Identify what is genuinely novel, grounded in the literature.

**Output:**
- Bullet list of each novelty point
- For each: 2–3 sentence justification citing specific papers from Step 2
- Novelty strength rating: Strong / Moderate / Weak with reasoning

**Artifact file:** `artifacts/step-3a-novelty-identification.md`

**Asset files:** None.

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] Both prior artifacts read as input
- [ ] Every novelty claim grounded in at least one specific paper from Step 2
- [ ] No novelty claim made without evidence it hasn't been done before
- [ ] Each novelty point has a strength rating with justification
- [ ] Weak novelty points flagged — not hidden
- [ ] At least 3 strong novelty points identified
- [ ] Artifact saved as `artifacts/step-3a-novelty-identification.md`

---

#### SUB-STEP 3b — Core Contributions

**First action:** Read `artifacts/research-area.md` and `artifacts/step-3a-novelty-identification.md`

**Task:**
- Define the 3–5 core contributions in crisp, peer-review-defensible language.

**Output:**
- Numbered contribution list
- Each: 1–2 precise sentences + one-line "why it matters" + mapped novelty point from 3a

**Artifact file:** `artifacts/step-3b-core-contributions.md`

**Asset files:** None.

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] `artifacts/step-3a-novelty-identification.md` read as input
- [ ] 3–5 contributions defined
- [ ] Each stated precisely — no vague language
- [ ] Each defensible against a hostile reviewer
- [ ] Each maps to at least one novelty point from 3a
- [ ] Contributions are distinct — no overlap
- [ ] "Why it matters" is specific, not generic
- [ ] Artifact saved as `artifacts/step-3b-core-contributions.md`

---

#### SUB-STEP 3c — Threat Model & Research Questions

**First action:** Read `artifacts/research-area.md`, `artifacts/step-1c-gap-analysis.md`, `artifacts/step-2c-related-work-map.md`, `artifacts/step-3b-core-contributions.md`

**Task:**
- Define the formal threat model and research questions.

**Output:**
- Formal threat model: adversary profile, capabilities, goals, assumptions, out-of-scope
- 3–5 RQs: specific, answerable, tied to contributions
- For each RQ: which contribution it validates + what a satisfying answer looks like

**Artifact file:** `artifacts/step-3c-threat-model-rqs.md`

**Asset files:**
- Create `assets/figure-01-threat-model.tex` — full TikZ diagram of the threat model (adversary, attack surface, target system, attacker goals, trust boundaries)
- Update `assets/ASSET-INDEX.md`

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] All prior relevant artifacts read as input
- [ ] Threat model covers all 5 dimensions: adversary, capabilities, goals, assumptions, out-of-scope
- [ ] Threat model consistent with codebase findings from Step 1
- [ ] 3–5 RQs defined, each specific and answerable
- [ ] Each RQ maps to at least one contribution from 3b
- [ ] Each RQ has a defined "satisfying answer" description
- [ ] `assets/figure-01-threat-model.tex` created with full TikZ code — no placeholders
- [ ] Figure has proper `\caption{}` and `\label{}`
- [ ] TikZ code is syntactically correct and compilable
- [ ] `assets/ASSET-INDEX.md` updated
- [ ] Artifact saved as `artifacts/step-3c-threat-model-rqs.md`

---

### STEP 4 — Paper Architecture

---

#### SUB-STEP 4a — Section Structure

**First action:** Read `artifacts/research-area.md` and all Step 3 artifacts

**Task:**
- Design the complete IEEE S&P paper section structure.

**Output:**
- All sections and subsections with 1–2 sentence description of each
- What argument or contribution each section serves
- Estimated page allocation per section
- Confirmed list of section filenames for `sections/`

**Artifact file:** `artifacts/step-4a-section-structure.md`

**Asset files:** None.

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] All Step 3 artifacts read as input
- [ ] Structure follows IEEE S&P conventions
- [ ] All standard sections present: Abstract, Introduction, Background, Related Work, Threat Model, Methodology, Evaluation, Discussion, Limitations, Conclusion, References
- [ ] Every contribution from 3b addressed in at least one section
- [ ] Every RQ from 3c addressed in at least one section
- [ ] Page allocation totals 12–16 pages
- [ ] Each section has a clear, single purpose
- [ ] Section filenames listed in lowercase kebab-case
- [ ] Structure tells a coherent single story
- [ ] Artifact saved as `artifacts/step-4a-section-structure.md`

---

#### SUB-STEP 4b — Figure Plan

**First action:** Read `artifacts/research-area.md` and `artifacts/step-4a-section-structure.md`

**Task:**
- Plan every figure needed. Assign filenames. Mark already-created figures.

**Output:**
For each figure:
- Assigned filename (`assets/figure-{index}-{name}.tex`)
- Type (TikZ diagram / pgfplots graph / algorithm / etc.)
- What it must show and what insight it conveys
- Which section file it belongs to
- Status: EXISTING or TO CREATE
- Specific data or content required

**Artifact file:** `artifacts/step-4b-figure-plan.md`

**Asset files:** None created — planning only.

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] `artifacts/step-4a-section-structure.md` read as input
- [ ] At least 6 figures planned total
- [ ] Every major system component has a diagram planned
- [ ] Every key result has a visual representation planned
- [ ] No section longer than 2 pages is without a figure
- [ ] Each figure has a unique, non-redundant purpose
- [ ] All figures assigned correct filenames following naming convention
- [ ] Existing figures clearly marked
- [ ] Figures numbered in order of appearance
- [ ] Artifact saved as `artifacts/step-4b-figure-plan.md`

---

#### SUB-STEP 4c — Equation & Table Plan

**First action:** Read `artifacts/research-area.md`, `artifacts/step-4a-section-structure.md`, `artifacts/step-4b-figure-plan.md`

**Task:**
- Plan all equations and tables. Assign filenames to tables. Mark already-created tables.

**Output:**
For each equation:
- Equation number and label
- What it captures, notation to be used, section it belongs to, why it is necessary

For each table:
- Assigned filename (`assets/table-{index}-{name}.tex`)
- What data it contains, column structure, section it belongs to
- Status: EXISTING or TO CREATE

**Artifact file:** `artifacts/step-4c-equation-table-plan.md`

**Asset files:** None created — planning only.

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] Both prior artifacts read as input
- [ ] All key concepts needing formalization are covered
- [ ] No equation is decorative or unnecessary
- [ ] Notation is consistent across all planned equations
- [ ] Every algorithm has a pseudocode representation planned
- [ ] All tables assigned correct filenames
- [ ] Existing tables clearly marked
- [ ] Each equation and table maps to a specific section file
- [ ] Artifact saved as `artifacts/step-4c-equation-table-plan.md`

---

### STEP 5 — Figure, Table & Equation Generation

---

#### SUB-STEP 5a — Figure Generation (batches of 2–3)

**First action:** Read `artifacts/research-area.md` and `artifacts/step-4b-figure-plan.md`

**Task:**
- Generate all TO CREATE figures in batches of 2–3.
- Each figure saved as its own `.tex` file in `assets/`.
- After each batch, pause and await confirmation.

**Each figure file must include:**
- Full header comment block
- Complete compilable TikZ or pgfplots code — no placeholders
- Every node, edge, label, data point explicitly defined
- Colorblind-safe colors, `\small` or `\footnotesize` fonts
- Proper `\caption{}` and `\label{}`

**Artifact file per batch:** `artifacts/step-5a-{batch-number}-figures.md`

**Asset files per batch:** 2–3 new figure `.tex` files in `assets/` + updated `assets/ASSET-INDEX.md`

**Checklist per batch:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] `artifacts/step-4b-figure-plan.md` read as input
- [ ] All figures in this batch match their plan from 4b exactly
- [ ] Every figure file follows the naming convention exactly
- [ ] Every figure has a complete header comment block
- [ ] TikZ/pgfplots code is complete and compilable — no placeholders
- [ ] Every node, edge, axis label, legend entry explicitly defined
- [ ] Color scheme is colorblind-safe
- [ ] Font sizes use `\small` or `\footnotesize`
- [ ] Every figure has `\caption{}` and `\label{}`
- [ ] `assets/ASSET-INDEX.md` updated
- [ ] Artifact saved as `artifacts/step-5a-{batch}-figures.md`
- [ ] When all batches done: every figure from 4b plan is generated

---

#### SUB-STEP 5b — Table Generation (batches of 2–3)

**First action:** Read `artifacts/research-area.md` and `artifacts/step-4c-equation-table-plan.md`

**Task:**
- Generate all TO CREATE tables in batches of 2–3.
- Each table saved as its own `.tex` file in `assets/`.
- After each batch, pause and await confirmation.

**Each table file must include:**
- Full header comment block
- Complete booktabs table with real data — no placeholders
- Proper `\caption{}` and `\label{}`

**Artifact file per batch:** `artifacts/step-5b-{batch-number}-tables.md`

**Asset files per batch:** 2–3 new table `.tex` files in `assets/` + updated `assets/ASSET-INDEX.md`

**Checklist per batch:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] `artifacts/step-4c-equation-table-plan.md` read as input
- [ ] All tables in this batch match their plan from 4c exactly
- [ ] Every table file follows naming convention exactly
- [ ] Every table has a complete header comment block
- [ ] All tables use booktabs — never `\hline`
- [ ] All cells contain real values — no placeholders
- [ ] Column alignment appropriate for data type
- [ ] Every table has `\caption{}` and `\label{}`
- [ ] `assets/ASSET-INDEX.md` updated
- [ ] Artifact saved as `artifacts/step-5b-{batch}-tables.md`

---

#### SUB-STEP 5c — Equation Generation

**First action:** Read `artifacts/research-area.md` and `artifacts/step-4c-equation-table-plan.md`

**Task:**
- Write all planned equations with full notation, variable definitions, and explanation.

**Output:**
For each equation:
- LaTeX equation block with label
- Variable definition table
- Plain-English explanation
- Suggested inline introduction sentence for use in the section file

**Artifact file:** `artifacts/step-5c-equations.md`

**Asset files:**
- Create `assets/equations.tex` — all equations in order, each with label, definition block, and explanatory comment
- Update `assets/ASSET-INDEX.md`

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] `artifacts/step-4c-equation-table-plan.md` read as input
- [ ] Every equation from the 4c plan is generated
- [ ] All equations are LaTeX-ready
- [ ] Every variable is defined
- [ ] Notation is consistent across all equations
- [ ] Each equation has a plain-English explanation
- [ ] Each equation has a suggested inline introduction sentence
- [ ] No equation is mathematically incorrect or ambiguous
- [ ] All equations saved in `assets/equations.tex`
- [ ] `assets/ASSET-INDEX.md` updated
- [ ] Artifact saved as `artifacts/step-5c-equations.md`

---

### STEP 6 — Full Paper Drafting

**Draft one section at a time. After each section, pause and await confirmation.**
**Every section file in `sections/` references assets via `\input{../assets/...}` — never inline figures or tables.**
**No placeholders. Every referenced figure, table, and equation must already exist in `assets/`.**

---

#### SUB-STEP 6a — Abstract + Introduction

**First action:** Read `artifacts/research-area.md`, `artifacts/step-3b-core-contributions.md`, `artifacts/step-3c-threat-model-rqs.md`, `artifacts/step-4a-section-structure.md`

**Output:**
- `sections/abstract.tex` — Abstract (250 words max, IEEE format)
- `sections/introduction.tex` — Problem motivation, gap, contributions, paper roadmap
- All `\input{../assets/...}` references placed at correct locations

**Artifact file:** `artifacts/step-6a-abstract-introduction.md`

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] All relevant prior artifacts read as input
- [ ] `sections/abstract.tex` created
- [ ] `sections/introduction.tex` created
- [ ] Abstract is within 250 words
- [ ] Abstract covers: problem, gap, approach, contributions, key result
- [ ] Introduction opens with a compelling problem statement
- [ ] All contributions from 3b stated clearly in Introduction
- [ ] All RQs from 3c referenced or implied
- [ ] Paper roadmap paragraph present at end of Introduction
- [ ] All figures/tables referenced via `\input{../assets/...}` — no inline LaTeX
- [ ] No placeholder text anywhere in either file
- [ ] Writing is precise and authoritative — zero filler
- [ ] `main/main.tex` updated to `\input{../sections/abstract}` and `\input{../sections/introduction}`
- [ ] Artifact saved as `artifacts/step-6a-abstract-introduction.md`

---

#### SUB-STEP 6b — Background & Related Work

**First action:** Read `artifacts/research-area.md`, `artifacts/step-2c-related-work-map.md`, `artifacts/step-4a-section-structure.md`

**Output:**
- `sections/background.tex`
- `sections/related-work.tex`
- `\input{../assets/table-01-related-work-comparison}` placed at correct location in `related-work.tex`

**Artifact file:** `artifacts/step-6b-background-related-work.md`

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] All relevant prior artifacts read as input
- [ ] `sections/background.tex` created
- [ ] `sections/related-work.tex` created
- [ ] All thematic categories from 2c are represented
- [ ] Every cited paper is referenced correctly
- [ ] No paper cited that wasn't in 2a or 2b
- [ ] Related Work ends with clear "our work differs because..." statement
- [ ] Background covers all concepts a reader needs
- [ ] `table-01-related-work-comparison` referenced via `\input{../assets/...}`
- [ ] No inline table code — asset file only
- [ ] No placeholder text anywhere
- [ ] `main/main.tex` updated with both new section `\input{}` references
- [ ] Artifact saved as `artifacts/step-6b-background-related-work.md`

---

#### SUB-STEP 6c — Threat Model

**First action:** Read `artifacts/research-area.md` and `artifacts/step-3c-threat-model-rqs.md`

**Output:**
- `sections/threat-model.tex`
- `\input{../assets/figure-01-threat-model}` placed at correct location

**Artifact file:** `artifacts/step-6c-threat-model.md`

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] `artifacts/step-3c-threat-model-rqs.md` read as input
- [ ] `sections/threat-model.tex` created
- [ ] All 5 threat model dimensions covered
- [ ] Threat model is internally consistent
- [ ] Out-of-scope explicitly stated
- [ ] `figure-01-threat-model` referenced via `\input{../assets/...}`
- [ ] No inline figure code — asset file only
- [ ] No placeholder text anywhere
- [ ] `main/main.tex` updated
- [ ] Artifact saved as `artifacts/step-6c-threat-model.md`

---

#### SUB-STEP 6d — Methodology

**First action:** Read `artifacts/research-area.md`, `artifacts/step-1a-codebase-read.md`, `artifacts/step-3c-threat-model-rqs.md`, `artifacts/step-4a-section-structure.md`, `artifacts/step-4b-figure-plan.md`

**Output:**
- `sections/methodology.tex`
- All relevant `\input{../assets/...}` references placed at correct locations
- Algorithm blocks using `algorithm2e`

**Artifact file:** `artifacts/step-6d-methodology.md`

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] All relevant prior artifacts read as input
- [ ] `sections/methodology.tex` created
- [ ] Methodology is fully reproducible from this section alone
- [ ] All planned figures for this section referenced via `\input{../assets/...}`
- [ ] All planned equations referenced via `\ref{}` or pulled from `assets/equations.tex`
- [ ] Every design decision is justified
- [ ] Methodology consistent with codebase from Step 1
- [ ] Methodology directly addresses the threat model from 6c
- [ ] No hand-waving — every component explained
- [ ] No inline figure or table code — asset files only
- [ ] No placeholder text anywhere
- [ ] `main/main.tex` updated
- [ ] Artifact saved as `artifacts/step-6d-methodology.md`

---

#### SUB-STEP 6e — Evaluation & Results

**First action:** Read `artifacts/research-area.md`, `artifacts/step-3c-threat-model-rqs.md`, `artifacts/step-4a-section-structure.md`, `artifacts/step-4b-figure-plan.md`, `artifacts/step-4c-equation-table-plan.md`

**Output:**
- `sections/evaluation.tex`
- All relevant `\input{../assets/...}` references placed at correct locations

**Artifact file:** `artifacts/step-6e-evaluation.md`

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] All relevant prior artifacts read as input
- [ ] `sections/evaluation.tex` created
- [ ] Every RQ from 3c has a corresponding result
- [ ] Evaluation setup fully described and reproducible
- [ ] Baselines clearly defined and justified
- [ ] All metrics defined before use
- [ ] All result figures and tables referenced via `\input{../assets/...}`
- [ ] Results reported with appropriate precision
- [ ] No cherry-picked results
- [ ] Statistical significance addressed
- [ ] No inline figure or table code — asset files only
- [ ] No placeholder text anywhere
- [ ] `main/main.tex` updated
- [ ] Artifact saved as `artifacts/step-6e-evaluation.md`

---

#### SUB-STEP 6f — Discussion & Limitations

**First action:** Read `artifacts/research-area.md`, `artifacts/step-6e-evaluation.md`, `artifacts/step-3b-core-contributions.md`

**Output:**
- `sections/discussion.tex`
- `sections/limitations.tex`

**Artifact file:** `artifacts/step-6f-discussion-limitations.md`

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] All relevant prior artifacts read as input
- [ ] `sections/discussion.tex` created
- [ ] `sections/limitations.tex` created
- [ ] Every contribution from 3b validated or discussed in light of results
- [ ] Limitations are honest and specific — not generic disclaimers
- [ ] At least 3 concrete future work directions given
- [ ] Discussion interprets results — does not repeat them
- [ ] No overclaiming beyond what results support
- [ ] No placeholder text anywhere
- [ ] `main/main.tex` updated with both new section `\input{}` references
- [ ] Artifact saved as `artifacts/step-6f-discussion-limitations.md`

---

#### SUB-STEP 6g — Conclusion

**First action:** Read `artifacts/research-area.md`, `artifacts/step-6a-abstract-introduction.md`, `artifacts/step-3b-core-contributions.md`, `artifacts/step-6f-discussion-limitations.md`

**Output:**
- `sections/conclusion.tex`

**Artifact file:** `artifacts/step-6g-conclusion.md`

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] All relevant prior artifacts read as input
- [ ] `sections/conclusion.tex` created
- [ ] Conclusion introduces no new information
- [ ] All contributions summarized
- [ ] Broader impact addressed
- [ ] Consistent with Introduction — same story, closed loop
- [ ] Within 1 page
- [ ] No placeholder text anywhere
- [ ] `main/main.tex` updated
- [ ] Artifact saved as `artifacts/step-6g-conclusion.md`

---

#### SUB-STEP 6h — References

**First action:** Read `artifacts/research-area.md`, `artifacts/step-2a-cited-papers.md`, `artifacts/step-2b-sota-search.md` and all 6a–6g artifacts

**Task:**
- Update `sections/references.bib` with all citations used across all section files.
- Verify every `\cite{}` key in every section file has a corresponding BibTeX entry.

**Output:**
- Updated `sections/references.bib` — complete, IEEE-formatted BibTeX entries

**Artifact file:** `artifacts/step-6h-references.md`

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] All prior artifacts read as input
- [ ] Every in-text `\cite{}` key has a BibTeX entry in `sections/references.bib`
- [ ] Every BibTeX entry is cited at least once in the paper
- [ ] All references formatted correctly for IEEE / IEEEtran
- [ ] No reference hallucinated — all verified from Step 2
- [ ] No duplicate BibTeX keys
- [ ] `main/main.tex` uses `\bibliography{../sections/references}`
- [ ] Artifact saved as `artifacts/step-6h-references.md`

---

#### SUB-STEP 6i — Main File Assembly

**First action:** Read `artifacts/research-area.md` and all Step 6 artifacts

**Task:**
- Finalize `main/main.tex` to correctly reference all sections and assets.
- Verify all `\input{}`, `\ref{}`, and `\cite{}` paths resolve correctly.
- Confirm final folder structure is complete and clean.

**Output:**
- Finalized `main/main.tex`
- Confirmed complete folder structure:

```
paper-05-model-orchestration/
├── artifacts/
│   ├── research-area.md
│   ├── step-1a-codebase-read.md
│   ├── step-1b-paper-read.md
│   ├── step-1c-gap-analysis.md
│   ├── step-2a-cited-papers.md
│   ├── step-2b-sota-search.md
│   ├── step-2c-related-work-map.md
│   ├── step-3a-novelty-identification.md
│   ├── step-3b-core-contributions.md
│   ├── step-3c-threat-model-rqs.md
│   ├── step-4a-section-structure.md
│   ├── step-4b-figure-plan.md
│   ├── step-4c-equation-table-plan.md
│   ├── step-5a-{batch}-figures.md
│   ├── step-5b-{batch}-tables.md
│   ├── step-5c-equations.md
│   ├── step-6a-abstract-introduction.md
│   ├── step-6b-background-related-work.md
│   ├── step-6c-threat-model.md
│   ├── step-6d-methodology.md
│   ├── step-6e-evaluation.md
│   ├── step-6f-discussion-limitations.md
│   ├── step-6g-conclusion.md
│   ├── step-6h-references.md
│   └── step-6i-main-assembly.md
├── assets/
│   ├── ASSET-INDEX.md
│   ├── equations.tex
│   ├── figure-01-threat-model.tex
│   ├── figure-02-system-architecture.tex
│   ├── ... (all figures)
│   ├── table-01-related-work-comparison.tex
│   └── ... (all tables)
├── main/
│   ├── IEEEtran.bst
│   ├── IEEEtran.cls
│   └── main.tex
├── sections/
│   ├── abstract.tex
│   ├── introduction.tex
│   ├── background.tex
│   ├── related-work.tex
│   ├── threat-model.tex
│   ├── methodology.tex
│   ├── evaluation.tex
│   ├── discussion.tex
│   ├── limitations.tex
│   ├── conclusion.tex
│   └── references.bib
└── paper.pdf
```

**Artifact file:** `artifacts/step-6i-main-assembly.md`

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] All Step 6 artifacts read as input
- [ ] `main/main.tex` is complete and finalized
- [ ] `main/main.tex` uses `\documentclass[conference]{IEEEtran}`
- [ ] `main/main.tex` uses `\bibliographystyle{IEEEtran}`
- [ ] All sections referenced via `\input{../sections/...}` in correct order
- [ ] All `\input{}` paths resolve to real files
- [ ] All `\ref{}` keys resolve correctly
- [ ] All `\cite{}` keys resolve to entries in `sections/references.bib`
- [ ] All section files exist in `sections/`
- [ ] All asset files exist in `assets/`
- [ ] `assets/ASSET-INDEX.md` is complete and accurate
- [ ] No file in any folder contains placeholder content
- [ ] Artifact saved as `artifacts/step-6i-main-assembly.md`

---

### STEP 7 — Critical Review & Final Polish

---

#### SUB-STEP 7a — Hostile Peer Review

**First action:** Read `artifacts/research-area.md` and all Step 6 artifacts

**Task:**
- Read the assembled paper as a complete document.
- Review as the most hostile, rigorous peer reviewer possible.

**Output:**
- Numbered list of every weakness, unsupported claim, unclear argument, logical gap, missing piece
- Severity: Critical / Major / Minor
- Specific suggested fix for each issue
- List of asset files or section files that need updating

**Artifact file:** `artifacts/step-7a-peer-review.md`

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] All Step 6 artifacts read as input
- [ ] Every section has been reviewed
- [ ] Every contribution claim stress-tested
- [ ] Every cited result checked for overclaiming
- [ ] Writing quality issues flagged
- [ ] Logical flow issues flagged
- [ ] All asset files reviewed for quality and accuracy
- [ ] At least 10 issues identified (if fewer, review again more carefully)
- [ ] Every issue has a specific suggested fix
- [ ] All files needing updates are explicitly listed
- [ ] Artifact saved as `artifacts/step-7a-peer-review.md`

---

#### SUB-STEP 7b — Revision Pass

**First action:** Read `artifacts/research-area.md` and `artifacts/step-7a-peer-review.md`

**Task:**
- Fix every Critical and Major issue. Address all Minor issues where feasible.
- Update affected section files in `sections/` and asset files in `assets/`.

**Output:**
- Updated `sections/*.tex` files for all affected sections
- Updated `assets/*.tex` files for all affected figures/tables
- Changelog

**Artifact file:** `artifacts/step-7b-revision-pass.md`

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] `artifacts/step-7a-peer-review.md` read as input
- [ ] Every Critical issue from 7a resolved
- [ ] Every Major issue from 7a resolved
- [ ] Minor issues addressed or explicitly deferred with reason
- [ ] All section files listed in 7a as needing updates have been updated
- [ ] All asset files listed in 7a as needing updates have been updated
- [ ] Changelog is complete with what changed, where, and why
- [ ] Revised files are consistent with each other
- [ ] No new issues introduced by revisions
- [ ] `assets/ASSET-INDEX.md` updated if any files were added or changed
- [ ] Artifact saved as `artifacts/step-7b-revision-pass.md`

---

#### SUB-STEP 7c — Final Verification

**First action:** Read `artifacts/research-area.md` and all revised artifacts

**Task:**
- Perform final quality and consistency verification across all files.

**Output:**
- Final verification memo
- Any last corrections applied directly to files
- Submission readiness verdict

**Artifact file:** `artifacts/step-7c-final-verification.md`

**Checklist:**
- [ ] `artifacts/research-area.md` read before starting
- [ ] All revised artifacts read as input
- [ ] All citations are real and correctly formatted in `sections/references.bib`
- [ ] All figures numbered correctly and captioned in `assets/`
- [ ] All tables numbered correctly and captioned in `assets/`
- [ ] All equations numbered correctly in `assets/equations.tex`
- [ ] All `\input{}` references in `main/main.tex` and `sections/` resolve to real files
- [ ] All `\ref{}` keys resolve correctly
- [ ] All `\cite{}` keys resolve to entries in `sections/references.bib`
- [ ] Paper tells a single coherent story from abstract to conclusion
- [ ] Abstract matches actual content of the paper
- [ ] Contributions in Introduction match contributions proven in Evaluation
- [ ] Page count is within 12–16 pages
- [ ] No placeholder text, TODOs, or unfinished content in any file
- [ ] `assets/ASSET-INDEX.md` is complete and accurate
- [ ] `artifacts/` contains one `.md` file per completed sub-step
- [ ] Submission readiness verdict given: **Ready / Needs Minor Work / Needs Major Work**
- [ ] Artifact saved as `artifacts/step-7c-final-verification.md`

---

## QUALITY BAR

This paper must be submittable to **IEEE S&P, USENIX Security, or ACM CCS** without embarrassment. If it isn't at that level, keep working.

---

## FAILURE CONDITIONS

Stop immediately and flag if any of the following occur:

- `artifacts/research-area.md` cannot be read at the start of a sub-step
- A checklist item cannot be completed due to missing information
- A novelty claim cannot be grounded in the literature
- A result referenced in the paper does not exist in the codebase or data
- A citation cannot be verified online
- The paper's story becomes internally inconsistent
- Any asset file cannot be generated without placeholder content
- Any `\input{}`, `\ref{}`, or `\cite{}` key cannot be resolved
- A section file or asset file cannot be written to its correct folder location

---

> - Begin with STEP 1a. Read `artifacts/research-area.md` first. Create `artifacts/step-1a-codebase-read.md`. Run the checklist. Report results.  
> - Put ✅ at the right side of substep in @research/context/steps-of-prompt.md that u have completed now.  
> - Stop and await for confirmation.  
