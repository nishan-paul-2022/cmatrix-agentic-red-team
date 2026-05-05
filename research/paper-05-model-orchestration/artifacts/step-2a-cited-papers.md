# [STEP 2a] — Cited Papers Research

## Summary
Performed a deep-dive research into the top 6 foundational papers cited in the LLMOrch-VAPT draft. This research covers LLM routing strategies (FrugalGPT, RouteLLM), autonomous security agents (PentestGPT, AutoAttacker), and advanced reasoning frameworks (ReWOO, Tree of Thoughts). The findings provide the baseline metrics and methodologies that LLMOrch-VAPT aims to extend.

## Full Output

### 1. FrugalGPT (TMLR 2024 / NeurIPS 2023)
- **Core Methodology**: Implements an **LLM Cascade** strategy where queries are sent to models in increasing order of cost. A fine-tuned "Judger" model (e.g., DistilBERT) evaluates the quality of each output and decides whether to stop or proceed to a stronger model.
- **Key Metrics**: Achieved up to **98% cost reduction** compared to GPT-4 while matching performance. Improved accuracy by 4% at equal cost.
- **Relation to LLMOrch-VAPT**: Provides the theoretical foundation for the "Complexity-Aware Routing Engine" claimed in §IV. LLMOrch-VAPT seeks to adapt this to the security domain using technical signals (CVE-IDs) instead of generic judgers.

### 2. RouteLLM (ICML 2024)
- **Core Methodology**: Learns routing functions based on human preference data (e.g., Chatbot Arena). Explores Matrix Factorization (MF), BERT-based classifiers, and Similarity-Weighted ranking.
- **Key Metrics**: Maintained high performance (MT-Bench) while achieving **2x+ cost reduction**. Demonstrated strong transfer learning (routers work for model pairs not seen during training).
- **Relation to LLMOrch-VAPT**: Suggests that preference-based routing is robust. LLMOrch-VAPT can incorporate "Security Expert Preference" data to refine its routing logic.

### 3. PentestGPT (USENIX Security 2024)
- **Core Methodology**: A tripartite modular architecture consisting of a **Reasoning Module** (using a Pentesting Task Tree), a **Generation Module** (creating commands), and a **Parsing Module** (processing tool output).
- **Key Metrics**: **228.6% increase in task completion** over GPT-3.5 and **58.6% over GPT-4**. Won the Distinguished Artifact Award.
- **Relation to LLMOrch-VAPT**: Provides the state-of-the-art baseline for autonomous VAPT. LLMOrch-VAPT's "Master-Worker" hierarchy in §III directly mirrors and extends the Reasoning/Generation/Parsing split.

### 4. AutoAttacker (NeurIPS 2024)
- **Core Methodology**: Modular agent architecture (Summarizer, Planner, Navigator, Experience Manager) targeting post-breach "hands-on-keyboard" attacks using MITRE ATT&CK and Metasploit.
- **Key Metrics**: GPT-4 achieved 100% success on tested tasks, while smaller models struggled with hallucinations.
- **Relation to LLMOrch-VAPT**: Grounding for the "Case Study" in §VI. AutoAttacker's use of an "Experience Manager" (RAG-based) informs LLMOrch-VAPT's vector-store memory management in the Appendix.

### 5. ReWOO (NeurIPS 2023)
- **Core Methodology**: Decouples reasoning from observations. A **Planner** generates a complete blueprint of tool calls first; a **Worker** executes them in parallel; a **Solver** synthesizes the final answer.
- **Key Metrics**: **64% reduction in token consumption** compared to ReAct. 4% accuracy gain on HotpotQA.
- **Relation to LLMOrch-VAPT**: Integrated into the "Reasoning Suite" in §II. LLMOrch-VAPT uses the ReWOO pattern to minimize latency in multi-tool security scans.

### 6. Tree of Thoughts (NeurIPS 2023)
- **Core Methodology**: Generalizes Chain-of-Thought by allowing BFS/DFS exploration of multiple "thought" branches. Includes a "State Evaluator" to prune dead-ends.
- **Key Metrics**: Achieved **74% success** on the Game of 24 (vs. 4% for GPT-4 with CoT).
- **Relation to LLMOrch-VAPT**: Used for "Exploitation" tasks in §VI, where multiple attack vectors must be explored and evaluated before execution.

## Key Decisions Made
- Identified FrugalGPT and RouteLLM as the primary competitors/inspirations for the Routing Engine.
- Identified PentestGPT as the "system-level" SOTA baseline.
- Decided to focus on "Token Efficiency" (ReWOO) and "Search Accuracy" (ToT) as the two primary technical benchmarks for the LLMOrch-VAPT reasoning layer.

## Open Questions
- How does FrugalGPT's "Judger" approach compare to the "Keyword-based Complexity" approach currently in the CMatrix code?
- Can we adapt RouteLLM's Matrix Factorization approach to security task embeddings?

## Checklist Results
- [PASS] `references.bib` has been read
- [PASS] Top 5–10 papers selected for research
- [PASS] Each paper's methodology and results are summarized
- [PASS] Relationship to LLMOrch-VAPT is clearly defined
- [PASS] Artifact saved as `artifacts/step-2a-cited-papers.md`
- [PASS] No Wikipedia or low-quality sources used

## Input for Next Step
Deep research on the core literature provides the "known landscape." The next step (2b) will perform a broader search for *new* SOTA papers (late 2024–2025) to ensure the paper is truly cutting-edge and identifies a clear research gap.
