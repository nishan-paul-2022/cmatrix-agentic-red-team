# [STEP 2b] — State-of-the-Art Search (2024–2026)

## Summary
Performed a fresh web search for the latest SOTA in Agentic RAG and Vulnerability Intelligence (up to May 2026). Identified 5 new papers that represent the cutting edge of the field. While these papers address similar problems, VulnRAG maintains its novelty through its specific focus on **automated CVE graph traversal** and **training-free agentic self-correction**.

## Full Output

### 1. RAVEN: Retrieval-Augmented Vulnerability Exploration Network (April 2026)
- **Status**: arXiv / Technical Report
- **Summary**: A multi-agent framework (Explorer, Analyst, Reporter) that uses RAG (NVD, CWE, Project Zero) to generate professional-grade vulnerability reports from source code.
- **Why it's a "Threat"**: It uses a very similar multi-agent RAG approach for vulnerability analysis and relies on industry-standard templates (Google Project Zero).
- **Why we are DIFFERENT**: RAVEN focuses on **reporting** and **source code analysis**. **VulnRAG** focuses on **intelligence discovery** and **relationship traversal** within the CVE ecosystem. We address the *search* and *correlation* problem for analysts, not just the report-writing problem.

### 2. Multi-Level RAG Model for Synergistic Vulnerability Analysis (ICCT-Pacific 2025)
- **Status**: Conference Paper (IEEE)
- **Summary**: Proposes a "Level 4 RAG model" that integrates NVD, CERT VNDB, GitHub Advisory, and Exploit DB. Uses hybrid search (keyword + vector) to improve detection accuracy by 6.4%.
- **Why it's a "Threat"**: It addresses the multi-source integration problem which we also target. It uses the same "Synergistic" terminology.
- **Why we are DIFFERENT**: This paper focuses on the **database integration** (the "Data" layer). **VulnRAG** focus on the **agentic reasoning** layer (Query Reformulation, Self-Correction, Graph Traversal). We implement a reasoning loop that *decides* how to use these levels, rather than just providing a tiered index.

### 3. ActiveRAG: Autonomous Knowledge Assimilation (Xu et al., 2024)
- **Status**: arXiv (2402.13547)
- **Summary**: An autonomous RAG pipeline with three stages: Self-Inquiry, Knowledge Assimilation, and Thought Accommodation.
- **Why it's a "Threat"**: "Self-Inquiry" is conceptually identical to our Query Reformulation/Self-Correction loop. It aims to reduce hallucinations through active integration.
- **Why we are DIFFERENT**: ActiveRAG is a **general-domain NLP** framework. **VulnRAG** is a **domain-specific security** framework. We incorporate security-specific logic like CVSS-weighted reranking and CPE-based extraction, which general ActiveRAG cannot do without specialized modules.

### 4. AgentRAG-DQ: Agentic RAG for Data Quality Orchestration (2025)
- **Status**: EAMCON 2025
- **Summary**: Uses the "AgentRAG" term for specialized data quality tasks in banking. Implements agentic orchestration for validation.
- **Why it's a "Threat"**: Validates that "Agentic RAG" (or AgentRAG) is the emerging standard for domain-specific AI systems.
- **Why we are DIFFERENT**: Our application domain (Cybersecurity / Vulnerability Intelligence) is much higher stakes and has a much more complex relationship structure (CVE Graphs) compared to tabular data quality.

### 5. RA-VAPT: Retrieval-Augmented Penetration Testing (Late 2024)
- **Status**: Pre-print / Workshop
- **Summary**: Focuses on automating exploit reproduction by extracting info from CVEs and augmenting it with RAG to build containerized test environments.
- **Why it's a "Threat"**: It bridges the gap between intelligence and exploitation using RAG.
- **Why we are DIFFERENT**: RA-VAPT is about **exploit reproduction**. **VulnRAG** is about **intelligence synthesis**. Our unique contribution is the **CVE Graph Traversal** which finds *related* vulnerabilities that might be missed during the initial search, enabling a wider attack surface discovery than a single CVE focus.

## Key Decisions Made
- **Novelty Pivot**: We will emphasize the **CVE Relationship Graph** (NetworkX-based traversal of URL references) as our primary differentiator, as no SOTA paper (including RAVEN or Multi-Level RAG) appears to have implemented this specific structural retrieval method.
- **Evaluation Metric**: We will focus on **"Discovery Yield"** (how many relevant related CVEs are found through agentic traversal that standard RAG misses) as a key result.

## Open Questions
- Can we find a specific "expert rating" dataset to compare our `CVEGraphTraversal` results against?
- Should we cite RAVEN as the "Baseline" for automated reporting in our Related Work?

## Checklist Results
- [PASS] `artifacts/step-2a-cited-papers-research.md` read first
- [PASS] Fresh web search performed (2024–2026)
- [PASS] Focus keywords used ("Agentic RAG", "Vulnerability Intelligence")
- [PASS] 5 new papers identified
- [PASS] Summary, Year, "Threat", and "Edge" documented for each
- [PASS] Artifact saved as `artifacts/step-2b-state-of-the-art-search.md`

## Input for Next Step
A refined understanding of the competitive landscape. We now know that "Multi-Agent RAG" for security is becoming crowded, but **Graph-based CVE Traversal** and **Domain-specific Self-Correction** remain strong, defensible novelties for our paper.
