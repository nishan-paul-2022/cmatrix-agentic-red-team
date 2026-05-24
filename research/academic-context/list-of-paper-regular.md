# Regular Research Papers (LLM-Orch VAPT)

> **Scope:** Foundational and thematic research papers cited in the `CMatrix` context,
> covering multi-agent framework architectures, dynamic task delegation, RAG/vulnerability
> intelligence, agent reasoning patterns, and security benchmarks. Ordered from **most recent → oldest**.
> Quality filter: CCF-A/B venues, major arXiv preprints, or direct architectural equivalents. No fluff.

---

## `2026 Papers`

### 1. Pen-Strategist: A Reasoning Framework for Penetration Testing Strategy Formation and Analysis
- **Venue:** arXiv (May 2026)
- **arXiv:** [2605.04499](https://arxiv.org/abs/2605.04499)
- **Why it matters for CMatrix:** Two-model framework: domain-specific Strategy Model (logical reasoning over prior findings) + Step Classifier (converts strategies → tool selections). Runs fully locally for data privacy — same design philosophy as CMatrix's local deployment. Table 10 contains a survey of 28 LLM-based PT systems — mandatory reference for CMatrix's related work section.

---

## `2025 Papers`

### 2. AGrail: Lifelong Agent Guardrail with Effective and Adaptive Safety Detection
- **Venue:** arXiv (Feb 2025)
- **arXiv:** [2502.11448](https://arxiv.org/abs/2502.11448)
- **Why it matters for CMatrix:** Adaptive safety detection and lifelong command execution guardrails (e.g., intercepting malicious CLI commands). Relevant to CMatrix's execution sandbox and tool safety logic.

---

### 3. RAG for Cybersecurity: Hybrid Retrieval for LLMs
- **Venue:** arXiv (Oct 2025)
- **arXiv:** [2510.27080](https://arxiv.org/abs/2510.27080)
- **Why it matters for CMatrix:** Adapting LLMs to emerging cybersecurity using retrieval augmented generation. Directly relevant to CMatrix's Vuln-Intel agent architecture for CVE and threat intelligence lookup.

---

### 4. CAIBench: Cybersecurity AI Meta-Benchmark
- **Venue:** arXiv (Oct 2025)
- **arXiv:** [2510.24317](https://arxiv.org/abs/2510.24317)
- **Why it matters for CMatrix:** Evaluates agent capabilities by meta-benchmarking across Cybench, SecEval, and AutoPenBench, establishing a robust framework for comparing CMatrix's overall capabilities.

---

### 5. When LLMs Meet Cybersecurity: A Systematic Literature Review
- **Venue:** Cybersecurity Journal (Springer) 2025
- **DOI:** [10.1186/s42400-025-00361-w](https://doi.org/10.1186/s42400-025-00361-w)
- **Why it matters for CMatrix:** Must-read systematic review of the entire LLM + cybersecurity intersection, providing technical taxonomy for offensive and defensive agent behaviors.

---

## `2024 Papers`

### 6. AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation
- **Venue:** arXiv (Aug 2023 / 2024)
- **arXiv:** [2308.08155](https://arxiv.org/abs/2308.08155)
- **Why it matters for CMatrix:** Foundational multi-agent conversation framework. CMatrix's Master-Worker hierarchy is directly inspired by AutoGen agent orchestration and cooperation patterns.

---

### 7. MetaGPT: Meta Programming for Multi-Agent Frameworks
- **Venue:** ICLR 2024
- **arXiv:** [2308.00352](https://arxiv.org/abs/2308.00352)
- **Why it matters for CMatrix:** Role-playing multi-agent architecture. Establishes SOPs for agent collaborations, which maps directly to specialized VAPT agent roles (Recon, Scan, Exploit) in CMatrix.

---

### 8. AutoPenBench: Benchmarking Generative Agents for Penetration Testing
- **Venue:** arXiv (Oct 2024)
- **arXiv:** [2410.03225](https://arxiv.org/abs/2410.03225)
- **Why it matters for CMatrix:** Standard evaluation benchmark utilizing 33 vulnerable Docker containers. Used to measure and optimize CMatrix's execution-layer exploit success rate.

---

### 9. Towards Automated Penetration Testing: Introducing LLM Benchmark, Analysis, and Improvements
- **Venue:** arXiv (Oct 2024)
- **arXiv:** [2410.17141](https://arxiv.org/abs/2410.17141)
- **Why it matters for CMatrix:** Introduces an open benchmark for evaluating LLM agents on end-to-end penetration testing. Helpful reference for our evaluation setup.

---

## `2023 Papers`

### 10. ReAct: Synergizing Reasoning and Acting in LLMs
- **Venue:** ICLR 2023
- **arXiv:** [2210.03629](https://arxiv.org/abs/2210.03629)
- **Why it matters for CMatrix:** The standard action-reasoning loop. Informs CMatrix's core terminal and execution agents on command generation and response evaluation.

---

### 11. Tree of Thoughts: Deliberate Problem Solving with LLMs
- **Venue:** NeurIPS 2023
- **arXiv:** [2305.10601](https://arxiv.org/abs/2305.10601)
- **Why it matters for CMatrix:** Advanced tree search and backtracking over planning nodes. Highly relevant for multi-step penetration testing campaign planning and vulnerability exploration.

---

### 12. Reflexion: Language Agents with Verbal RL
- **Venue:** NeurIPS 2023
- **arXiv:** [2303.11366](https://arxiv.org/abs/2303.11366)
- **Why it matters for CMatrix:** Self-reflection loops allowing agents to evaluate exploit execution failures and iteratively refine payloads.

---

## `2022 Papers`

### 13. Chain-of-Thought Prompting Elicits Reasoning in LLMs
- **Venue:** NeurIPS 2022
- **arXiv:** [2201.11903](https://arxiv.org/abs/2201.11903)
- **Why it matters for CMatrix:** Elicits complex reasoning by generating intermediate steps. Essential base planning logic for all CMatrix agents.

---
