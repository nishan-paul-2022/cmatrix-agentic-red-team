# [STEP 2a] — Cited Papers Research

## Summary
Conducted a deep-dive research into the current bibliography and foundational literature. Mapped 10 critical papers to the CMatrix-VulnRAG project, identifying their core contributions and, more importantly, the specific research gaps that our project fills.

## Full Output

### 1. RouteLLM (ICML 2024)
- **Summary**: A framework for dynamic routing between strong (expensive) and weak (cheap) LLMs using human preference data.
- **Core Contribution**: Optimized performance-to-cost trade-off via intelligent query routing.
- **Why Cited**: Foundation for our "Complexity-Aware Routing" (Flash, Pro, Reasoning tiers).
- **The Gap**: RouteLLM is general-purpose and primarily binary (strong vs. weak). **VulnRAG** applies this to the security domain using domain-specific complexity signals (CVE presence, exploit complexity) across a multi-tier hierarchy.

### 2. PentestGPT (USENIX Security 2024)
- **Summary**: An LLM-empowered framework with Reasoning, Generation, and Parsing modules for automated pentesting.
- **Core Contribution**: The "Pentesting Task Tree" (PTT) for maintaining long-term context in multi-step attacks.
- **Why Cited**: Primary state-of-the-art (SOTA) for autonomous red teaming.
- **The Gap**: PentestGPT focuses on task orchestration and command execution. It treats vulnerability intelligence as a simple tool output. **VulnRAG** deep-dives into the *retrieval* phase, implementing a sophisticated agentic loop for intelligence gathering that PentestGPT lacks.

### 3. Self-RAG (ICLR 2024)
- **Summary**: A model trained to adaptively retrieve, generate, and critique via special "reflection tokens."
- **Core Contribution**: End-to-end self-reflective RAG pipeline.
- **Why Cited**: Inspiration for our `self_correction.py` and `query_reformulator.py`.
- **The Gap**: Self-RAG requires specialized model fine-tuning. **VulnRAG** implements self-reflective behavior **zero-shot** using a modular agentic architecture (Evaluator + Reformulator), making it provider-agnostic and easier to integrate into enterprise systems.

### 4. RAPTOR (ICLR 2024)
- **Summary**: Recursive abstractive processing that builds a tree of summaries for multi-level document retrieval.
- **Core Contribution**: Hierarchical retrieval that overcomes the limitations of flat chunking.
- **Why Cited**: Theoretical basis for our graph-based retrieval.
- **The Gap**: RAPTOR builds trees over generic text. **VulnRAG** builds **CVE Relationship Graphs** using security-specific semantics (e.g., URL references, shared CWEs), enabling the discovery of actual attack chains rather than just thematic summaries.

### 5. Lost in the Middle (TACL 2023)
- **Summary**: Identifies that LLM performance degrades significantly when relevant information is in the middle of a long context.
- **Core Contribution**: Empirical proof of the "U-shaped" performance curve in long-context models.
- **Why Cited**: Rationale for our `cve_reranker.py` module.
- **The Gap**: Liu et al. identify the problem and suggest reranking as a potential fix. **VulnRAG** provides a concrete implementation and study of **Cross-Encoder reranking** specifically for security-critical CVE data to ensure high-priority vulnerabilities are never "lost."

### 6. ReWOO (NeurIPS 2023)
- **Summary**: Decouples reasoning from observation by planning tool calls in advance to reduce cost and latency.
- **Core Contribution**: Evidence that structured planning improves efficiency in augmented language models.
- **Why Cited**: Supports our goal of cost-efficient security reasoning.
- **The Gap**: ReWOO is a general-purpose execution pattern. **VulnRAG** applies it to the "Intelligence Discovery" phase, allowing the agent to plan a series of NVD/Graph queries before executing them, minimizing redundant LLM calls.

### 7. Reflexion (NeurIPS 2023)
- **Summary**: An agentic pattern where the model critiques its own outputs and maintains a "memory" of past failures to improve.
- **Core Contribution**: Verbal reinforcement learning as a training-free improvement mechanism.
- **Why Cited**: Theoretical foundation for the `SelfCorrectionService`.
- **The Gap**: Reflexion focuses on generic reasoning tasks (coding, QA). **VulnRAG** applies self-reflection specifically to **Retrieval Quality**, allowing the agent to "realize" when a search result is poor and reformulate its query.

### 8. Tree of Thoughts (ToT) (NeurIPS 2023)
- **Summary**: A framework where LLMs explore multiple reasoning branches (thoughts) and evaluate them to find a solution.
- **Core Contribution**: Generalization of Chain of Thought for non-linear problem solving.
- **Why Cited**: Used in our "Reasoning Suite" for complex attack path exploration.
- **The Gap**: ToT is a search algorithm for reasoning. **VulnRAG** uses ToT to explore **vulnerability chains** discovered via graph traversal, turning structural CVE data into strategic attack paths.

### 9. REALM (Guu et al. 2020)
- **Summary**: Integrates retrieval into pre-training, emphasizing that external knowledge is more updateable than model parameters.
- **Core Contribution**: The foundational argument for RAG: "Knowledge as Retrieval."
- **Why Cited**: Justifies our use of a continuous `nvd_sync_service.py` to keep the knowledge base current.
- **The Gap**: REALM uses a static Wikipedia dump. **VulnRAG** operates on a **dynamically updated security knowledge base** where new "facts" (CVEs) appear daily.

### 10. RAG (Lewis et al. 2020)
- **Summary**: The original Retrieval-Augmented Generation paper combining a retriever and a generator.
- **Core Contribution**: Established the "Retrieve-then-Generate" paradigm.
- **Why Cited**: The fundamental baseline for our work.
- **The Gap**: Original RAG is a static, one-shot process. **VulnRAG** is **Agentic RAG**, where the retrieval is iterative, self-correcting, and graph-aware.

## Key Decisions Made
- **Venues**: Confirmed **ACM SIGIR 2026** as the primary target, as the paper's core innovations (reranking, graph retrieval, query reformulation) are classic IR problems applied to a high-value security domain.
- **Positioning**: We will position VulnRAG as the **"Intelligence Layer"** that SOTA systems like PentestGPT are missing.

## Open Questions
- Are there any other specific "Security RAG" papers published in the last 6 months (late 2025) that we should include?
- How much of the "Model Cascading" (FrugalGPT) logic is actually implemented in the `SmartCVESearchService`?

## Checklist Results
- [PASS] `artifacts/research-area.md` read first
- [PASS] `artifacts/step-1c-gap-analysis.md` read first
- [PASS] Bibliography (`references.bib`) deep-dived
- [PASS] Every paper currently cited (top 10) analyzed
- [PASS] Summary, core contribution, and reason for citation documented
- [PASS] The "Gap" for every cited paper identified
- [PASS] Accuracy ensured (via internal knowledge or `search_web`)
- [PASS] Artifact saved as `artifacts/step-2a-cited-papers-research.md`

## Input for Next Step
A comprehensive map of the current literature landscape. This will be used in 2b to find *even newer* papers and in 2c to create the "Related Work Map" that visualizes our positioning.
