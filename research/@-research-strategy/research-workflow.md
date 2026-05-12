# Research Workflow for CMatrix (Beginner-Friendly)

This is one of the most common bottlenecks for engineering-background researchers — you're used to *building*, not *reading*. Here's a practical workflow designed for your situation.

---

## The Core Mindset Shift

You don't read research papers the way you read documentation. **Papers are mined, not read.** Your goal is to extract what's useful for CMatrix and move on.

---

## Phase 1 — Triage Your 200 Papers First

Before reading anything deeply, **sort your 200 papers into 3 buckets**:

| Bucket | Criteria | Approx Count |
|--------|----------|--------------|
| 🔴 Core | Directly about your system (LLM agents for pentesting, agentic security tools) | ~20–30 |
| 🟡 Supporting | Related concepts (RAG, LangGraph patterns, CVE analysis, tool-use in LLMs) | ~60–80 |
| 🟢 Background | Survey/overview papers, foundational work | ~remaining |

Read 🔴 papers deeply. Skim 🟡. Use 🟢 only for citations and background understanding.

**How to triage without reading:** Just use the title + abstract + conclusion. That's enough to bucket a paper in under 3 minutes.

---

## Phase 2 — The 3-Pass Reading Method (per paper)

This is a well-known academic technique, adapted for your context.

### Pass 1 — Reconnaissance (5–10 min)

Read only:
- Title + Abstract
- Introduction (first and last paragraph only)
- All headings and subheadings
- All figures, tables, diagrams
- Conclusion

**Goal:** Answer — *"Does this paper give me something I can use in CMatrix right now?"*

### Pass 2 — Extraction (30–60 min, Core papers only)

Now read the full paper but with a highlighter mindset. You're looking for:
- Their **architecture/system design** → compare with yours
- Their **evaluation metrics** → steal these for your own paper
- Their **limitations section** → this is your differentiation opportunity
- Their **references** → find 2–3 more papers worth triaging

### Pass 3 — Deep Dive (only for 5–10 papers max)

Full line-by-line understanding. Only for papers that are either:
- The closest competitor to CMatrix (PentAGI, Shannon papers)
- Introducing a concept you're actually implementing

---

## Phase 3 — The Parallel Coding-Reading Loop

This is key. **Don't read in isolation.** Tie every reading session to a concrete CMatrix task.

```
Reading Session → Coding Task → Note → Repeat
```

Concretely:

| Paper Topic | CMatrix Task to Code Immediately After |
|-------------|----------------------------------------|
| LangGraph agentic loop patterns | Refine your scan pipeline's conditional branching |
| RAG + CVE retrieval paper | Hook Qdrant to your NVD feed ingestion |
| Tool-use benchmarking paper | Define your own eval harness structure |
| Prompt injection in agents | Add a guardrail node to your LangGraph flow |

The reading session gives you the *idea*, the coding session makes it *stick*. You won't forget a paper you built something from.

---

## Phase 4 — Your Note-Taking System

For each paper you do Pass 2 on, maintain a single structured note. Keep it simple:

```markdown
## [Paper Title] — [Year]
**1-line summary:** What they built/proved
**Relevance to CMatrix:** High / Medium / Low
**Key idea I can use:** [specific thing]
**Their metrics/benchmarks:** [list them]
**Their limitations:** [this is your gap to exploit]
**Citation key:** author2024_keyword
```

Use Obsidian or even a single markdown file in your CMatrix repo (`/research/notes/`). Don't overthink the tooling.

---

## Weekly Workflow (Realistic)

Given your MSc + job hunting + active development:

```
Monday–Tuesday:    Read 3–5 papers (Pass 1 all, Pass 2 on 1 core paper)
Wednesday–Thursday: Code the feature/idea extracted from that core paper
Friday:            Update your notes, update your literature review draft
Weekend:           Rest or light reading only
```

This gives you ~50 Pass-1 triages and ~8 deep papers per month — enough to write a solid related works section in 3 months.

---

## The Biggest Mistake to Avoid

> ❌ "Let me fully understand this paper before I start coding."

This leads to paralysis. You're an engineer. **Your codebase is your research instrument.** The moment CMatrix can run a scan and produce output, you have something to *compare against* the papers — which is exactly how you generate your own research contribution.

Read enough to know what to build. Build it. Then read more.
