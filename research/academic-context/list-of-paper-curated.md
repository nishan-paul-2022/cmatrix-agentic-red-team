# Curated Research Papers (LLM-Orch VAPT)

> **Scope:** Papers directly relevant to CMatrix's core pillars — LLM-based agentic pentesting,
> multi-agent red-team orchestration, autonomous vulnerability exploitation, offensive security
> benchmarks, and agentic cybersecurity systems. Ordered from **most recent → oldest**.
> Quality filter: CCF-A/B venues, major arXiv preprints with 50+ citations, or direct architectural
> equivalents. No fluff, no tangential references.

---

## Legend

| Badge | Meaning |
|---|---|
| 🔴 CCF-A | Top-tier venue (USENIX, CCS, IEEE S&P, NeurIPS, ICLR, ACL, TOSEM, FSE) |
| 🟡 CCF-B | Strong venue (Computers & Security, AsiaCCS, JNCA, ESE) |
| 🟠 arXiv | High-quality preprint (architecturally direct match) |
| 🔵 Workshop | Major workshop at top venue |

---

## `2026 Papers`

### 1. HackWorld: Evaluating Computer-Use Agents on Exploiting Web Application Vulnerabilities
- **Venue:** 🔴 ICLR 2026
- **arXiv:** [2510.12200](https://arxiv.org/abs/2510.12200)
- **Code:** [GitHub](https://github.com/GUI-Agent/HackWorld)
- **Why it matters for CMatrix:** Evaluates GUI/computer-use LLM agents autonomously attacking real web application vulnerabilities — directly maps to CMatrix's black-box scan mode and web vuln pipeline. Uses the same agent-environment loop that CMatrix's VS Code-style terminal UI embodies.

---

### 2. Cyber-Zero: Training Cybersecurity Agents without Runtime
- **Venue:** 🔴 ICLR 2026
- **arXiv:** [2508.00910](https://arxiv.org/abs/2508.00910)
- **Code:** [GitHub](https://github.com/amazon-science/cyber-zero)
- **Why it matters for CMatrix:** Trains offensive security agents *without runtime environment access* — directly relevant to CMatrix's offline/local model strategy and the question of pre-training vs. fine-tuning for pentest tasks. Amazon research.

---

### 3. What Makes a Good LLM Agent for Real-world Penetration Testing?
- **Venue:** 🟠 arXiv (Feb 2026)
- **arXiv:** [2602.17622](https://arxiv.org/abs/2602.17622)
- **Why it matters for CMatrix:** PentestGPT V2 paper — empirically identifies what agent properties (planning, memory, tool use) matter most for real-world pentest. Achieves 76.9% (10/13 machines) on HackTheBox. Directly comparable to CMatrix's evaluation framework design.

---

### 4. Pen-Strategist: A Reasoning Framework for Penetration Testing Strategy Formation and Analysis
- **Venue:** 🟠 arXiv (May 2026)
- **arXiv:** [2605.04499](https://arxiv.org/abs/2605.04499)
- **Authors:** Yasod Ginige, Pasindu Marasinghe, Sajal Jain, Suranga Seneviratne — University of Sydney
- **Why it matters for CMatrix:** Two-model framework: a fine-tuned domain-specific **Strategy Model** (logical reasoning over prior findings) + a **Step Classifier** (converts strategies → tool selections). Runs fully locally for data privacy — same design philosophy as CMatrix's local Vast.ai deployment. Table 10 contains the most comprehensive survey of 28 LLM-based PT systems as of May 2026 — mandatory reference for CMatrix's related work section. Same author group as AutoPentester (#28), forming a coherent Sydney research lineage CMatrix must engage with.

---

### 5. Co-RedTeam: Orchestrated Security Discovery and Exploitation with LLM Agents
- **Venue:** 🟠 arXiv (Feb 2026) — Google Cloud AI Research
- **arXiv:** [2602.02164](https://arxiv.org/abs/2602.02164)
- **Why it matters for CMatrix:** Multi-agent red team with specialized roles (discovery agent, exploitation agent, critic agent) and structured interaction — architecturally almost identical to CMatrix's reconnaissance-scan-exploit pipeline. Google-authored.

---

### 6. CyberExplorer: Benchmarking LLM Offensive Security Capabilities in a Real-World Attacking Simulation
- **Venue:** 🟠 arXiv (Feb 2026)
- **arXiv:** [2602.08023](https://arxiv.org/abs/2602.08023)
- **Why it matters for CMatrix:** Open-environment benchmark with 40 vulnerable web services, multi-target scenarios, autonomous reconnaissance without prior knowledge — perfectly mirrors CMatrix's black-box scan scenario. Defines evaluation metrics CMatrix should adopt.

---

### 7. To Defend Against Cyber Attacks, We Must Teach AI Agents to Hack
- **Venue:** 🟠 arXiv (Feb 2026)
- **arXiv:** [2602.02595](https://arxiv.org/abs/2602.02595)
- **Why it matters for CMatrix:** Argues for and demonstrates offensive-security-first agent training — the philosophical and technical grounding for CMatrix's approach of using unrestricted models (DeepSeek-R1) for red-team tasks.

---

### 8. LLMs as Hackers: Autonomous Linux Privilege Escalation Attacks
- **Venue:** 🟡 Empirical Software Engineering 2026 (Springer)
- **URL:** [Springer](https://link.springer.com/article/10.1007/s10664-025-10758-3)
- **Why it matters for CMatrix:** End-to-end autonomous privilege escalation — a concrete pentest sub-task CMatrix's exploitation agent must handle. Real-system evaluation on Linux.

---

### 9. Towards Cybersecurity Superintelligence: from AI-guided humans to human-guided AI
- **Venue:** 🟠 arXiv (Jan 2026) — Alias Robotics
- **arXiv:** [2601.14614](https://arxiv.org/abs/2601.14614)
- **Why it matters for CMatrix:** Documents the full progression PentestGPT → CAI → G-CTR. The most comprehensive single paper tracking the evolution of the field CMatrix operates in. Directly cites game-theoretic agent reasoning as the frontier.

---

### 10. A Survey of Agentic AI and Cybersecurity: Challenges, Opportunities and Use-case Prototypes
- **Venue:** 🟠 arXiv (Jan 2026)
- **arXiv:** [2601.05293](https://arxiv.org/abs/2601.05293)
- **Why it matters for CMatrix:** Comprehensive dual-use analysis of agentic AI in cybersecurity — planning, memory, tool orchestration, multi-agent interaction. Positions exactly where CMatrix sits in the landscape.

---

### 11. A Red Teaming Framework for Evaluating Robustness of AI-enabled Security Orchestration, Automation, and Response (SOAR) Systems
- **Venue:** 🟠 arXiv (May 2026)
- **arXiv:** [2605.17075](https://arxiv.org/abs/2605.17075)
- **Why it matters for CMatrix:** Hybrid LLM-RL red teaming against enterprise SOAR systems — multi-stage attack campaigns, shows standalone LLM agents failing, justifying CMatrix's multi-agent design.

---

### 12. ExploitGym: Can AI Agents Turn Security Vulnerabilities into Real Attacks?
- **Venue:** 🟠 arXiv (May 2026)
- **arXiv:** [2605.11086](https://arxiv.org/abs/2605.11086)
- **Why it matters for CMatrix:** Evaluates defensive security agents using automated exploits and reinforcement learning to turn vulnerabilities into verified attacks.

---

### 13. AWE: Adaptive Agents for Dynamic Web Penetration Testing
- **Venue:** 🔴 NDSS 2026
- **URL:** [NDSS](https://www.ndss-symposium.org/ndss-paper/auto-draft-680/)
- **Code:** [GitHub](https://github.com/stuxlabs/AWE)
- **Why it matters for CMatrix:** Adaptive agents designed specifically for dynamic web penetration testing — highly relevant to CMatrix's web agent architecture.

---

### 14. PACEbench: A Framework for Evaluating Practical AI Cyber-Exploitation Capabilities
- **Venue:** 🔴 ICLR 2026
- **URL:** [OpenReview](https://openreview.net/pdf?id=kGEuZXaXU6)
- **Code:** [GitHub](https://github.com/RyuKosei/PACEbench)
- **Why it matters for CMatrix:** Evaluates practical AI cyber-exploitation capabilities on diverse benchmarks — validates offensive agent evaluation standards.

---

## `2025 Papers`

### 15. EnIGMA: Interactive Tools Substantially Assist LM Agents in Finding Security Vulnerabilities
- **Venue:** 🔴 ICLR 2025
- **arXiv:** [2409.16165](https://arxiv.org/abs/2409.16165)
- **Code:** [GitHub](https://github.com/SWE-agent/SWE-agent/tree/v0.7)
- **Why it matters for CMatrix:** Shows interactive tooling dramatically improves LLM agent security performance. Directly validates CMatrix's xterm.js terminal integration and interactive tool design (vs. static script execution).

---

### 16. Can LLMs Hack Enterprise Networks? Autonomous Assumed Breach Penetration-Testing Active Directory Networks
- **Venue:** 🔴 TOSEM 2025 (ACM Transactions on Software Engineering and Methodology)
- **DOI:** [10.1145/3766895](https://dl.acm.org/doi/abs/10.1145/3766895)
- **Code:** [GitHub](https://github.com/andreashappe/cochise)
- **Why it matters for CMatrix:** Enterprise AD network pentest — closest to CMatrix's grey-box scan mode and multi-host lateral movement scenarios. Top journal publication.

---

### 17. Measuring and Augmenting Large Language Models for Solving Capture-the-Flag Challenges
- **Venue:** 🔴 ACM CCS 2025
- **DOI:** [10.1145/3719027.3744855](https://dl.acm.org/doi/abs/10.1145/3719027.3744855)
- **Why it matters for CMatrix:** CTF is the primary evaluation playground for offensive LLM agents. Top-tier CCS paper on systematically augmenting LLMs for this task — directly informs CMatrix's benchmark design.

---

### 18. PentestAgent: Incorporating LLM Agents to Automated Penetration Testing
- **Venue:** 🟡 AsiaCCS 2025
- **arXiv:** [2411.05185](https://arxiv.org/abs/2411.05185)
- **DOI:** [10.1145/3708821.3733882](https://dl.acm.org/doi/full/10.1145/3708821.3733882)
- **Code:** [GitHub](https://github.com/GH05TCREW/PentestAgent)
- **Why it matters for CMatrix:** Fully autonomous multi-agent pentesting, competes directly with CMatrix. Evaluated against VulHub + HackTheBox. Strongest direct architectural competitor.

---

### 19. From Capabilities to Performance: Evaluating Key Functional Properties of LLM Architectures in Penetration Testing
- **Venue:** 🔴 ACL 2025
- **Why it matters for CMatrix:** Systematic evaluation of how specific LLM architectural properties (chain-of-thought, tool use, context window) affect pentest performance. Directly informs CMatrix's model selection (DeepSeek-R1-Distill reasoning).

---

### 20. Cloak, Honey, Trap: Proactive Defenses Against LLM Agents
- **Venue:** 🔴 USENIX Security 2025
- **Why it matters for CMatrix:** Studies defenses deployed against offensive LLM agents — essential for CMatrix to understand adversarial constraints and evasion scenarios its agents will face.

---

### 21. A Unified Modeling Framework for Automated Penetration Testing
- **Venue:** 🟡 Computers & Security 2025 (Elsevier — CCF-B)
- **DOI:** [10.1016/j.cose.2025.004766](https://www.sciencedirect.com/science/article/abs/pii/S0167404825004766)
- **Why it matters for CMatrix:** Unified formal framework covering all phases of automated pentesting — directly maps to CMatrix's black/grey/white-box unified LangGraph pipeline. Published in CMatrix's target journal.

---

### 22. VulnBot: Autonomous Penetration Testing for a Multi-Agent Collaborative Framework
- **Venue:** 🟠 arXiv (Jan 2025)
- **arXiv:** [2501.13411](https://arxiv.org/abs/2501.13411)
- **Code:** [GitHub](https://github.com/KHenryAegis/VulnBot)
- **Why it matters for CMatrix:** Role-specialized multi-agent framework (recon, scan, exploit) with penetration task graph (PTG) for logical execution — the closest existing architectural match to CMatrix's LangGraph pipeline design.

---

### 23. Incalmo: An Autonomous LLM-assisted System for Red Teaming Multi-Host Networks
- **Venue:** 🟠 arXiv (Jan 2025, multiple revisions through Nov 2025)
- **arXiv:** [2501.16466](https://arxiv.org/abs/2501.16466)
- **Code:** [GitHub](https://github.com/bsinger98/Incalmo)
- **Why it matters for CMatrix:** Multi-host red teaming with abstract action layer — compromised 9/10 mobile-core testbeds (25–50 hosts). Directly comparable to CMatrix's multi-target scan mode.

---

### 24. CAI: An Open, Bug Bounty-Ready Cybersecurity AI
- **Venue:** 🟠 arXiv (Apr 2025) — Alias Robotics
- **arXiv:** [2504.06017](https://arxiv.org/abs/2504.06017)
- **Code:** [GitHub](https://github.com/aliasrobotics/CAI)
- **Why it matters for CMatrix:** The most production-proven autonomous pentest agent in existence (Rank #1 at 5 major CTF competitions, $50K Neurogrid prize). Direct competitor. Architectural reference for what CMatrix aspires to become.

---

### 25. Cybersecurity AI: The World's Top AI Agent for Security CTF
- **Venue:** 🟠 arXiv (Dec 2025) — Alias Robotics
- **arXiv:** [2512.02654](https://arxiv.org/abs/2512.02654)
- **Why it matters for CMatrix:** Documents CAI's dominance across 5 international CTF competitions. Establishes the current state-of-the-art benchmark CMatrix must measure against.

---

### 26. Pentest-R1: Towards Autonomous Penetration Testing Reasoning Optimized via Two-Stage Reinforcement Learning
- **Venue:** 🟠 arXiv (Aug 2025)
- **arXiv:** [2508.07382](https://arxiv.org/abs/2508.07382)
- **Code:** [GitHub](https://github.com/KHenryAegis/Pentest-R1)
- **Why it matters for CMatrix:** Applies two-stage RL (offline on 500+ walkthroughs → online CTF environment) to optimize pentest reasoning. Achieves 24.2% on AutoPenBench and 15.0% on Cybench for open-source models. Directly validates CMatrix's choice of DeepSeek-R1 (chain-of-thought reasoning model) and informs the planned fine-tuning strategy.

---

### 27. RedTeamLLM: an Agentic AI Framework for Offensive Security
- **Venue:** 🟠 arXiv (Dec 2025)
- **arXiv:** [2512.14233](https://arxiv.org/abs/2512.14233)
- **Code:** [GitHub](https://github.com/lre-security-systems-team/redteamllm)
- **Why it matters for CMatrix:** Explicit offensive security agentic framework — reconnaissance, exploitation, reporting phases. Direct architectural comparison.

---

### 28. xOffense: An AI-driven Autonomous Penetration Testing Framework with Offensive Knowledge-enhanced LLMs and Multi-Agent Systems
- **Venue:** 🟠 arXiv (Sep 2025) — submitted to Elsevier
- **arXiv:** [2509.13021](https://arxiv.org/abs/2509.13021)
- **Why it matters for CMatrix:** Uses fine-tuned Qwen3-32B as reasoning backbone with specialized recon/scan/exploit agents — mirrors CMatrix's open-source LLM + multi-agent approach. Even the model scale (~32B) is identical to CMatrix's DeepSeek-R1-Distill-Qwen-32B choice.

---

### 29. D-CIPHER: Dynamic Collaborative Intelligent Multi-Agent System with Planner and Heterogeneous Executors for Offensive Security
- **Venue:** 🟠 arXiv (Feb 2025)
- **arXiv:** [2502.10931](https://arxiv.org/abs/2502.10931)
- **Why it matters for CMatrix:** Planner-executor multi-agent system with heterogeneous specialized agents for CTF — directly informs CMatrix's agent role decomposition and inter-agent communication protocol.

---

### 30. AutoPentester: An LLM Agent-based Framework for Automated Penetration Testing
- **Venue:** 🟡 IEEE (also arXiv Oct 2025)
- **arXiv:** [2510.05605](https://arxiv.org/abs/2510.05605)
- **Authors:** Yasod Ginige, Asitha Niroshan, Sajal Jain, Suranga Seneviratne — University of Sydney
- **Why it matters for CMatrix:** Five-module architecture (Strategy Analyzer → RAG Summarizer → Generator → Results Verifier → Repetition Identifier) with CoT-based dynamic attack strategy generation — the closest single-paper analogue to CMatrix's LangGraph conditional branching design. Hard numbers: 27.0% better subtask completion, 39.5% more vulnerability coverage, 19.8% higher user score vs PentestGPT. Evaluated on HackTheBox + custom VMs. Primary direct comparison baseline for any CMatrix publication. Same author group as Pen-Strategist (#4).

---

### 31. RapidPen: Fully Automated IP-to-Shell Penetration Testing with LLM-based Agents
- **Venue:** 🟠 arXiv (Feb 2025)
- **arXiv:** [2502.16730](https://arxiv.org/abs/2502.16730)
- **Why it matters for CMatrix:** End-to-end IP→shell automation via ReAct agent in 200–400 seconds, $0.30–$0.60/run. Establishes cost/speed benchmarks for autonomous pentest that CMatrix should target.

---

### 32. ARACNE: An LLM-Based Autonomous Shell Pentesting Agent
- **Venue:** 🟠 arXiv (Feb 2025)
- **arXiv:** [2502.18528](https://arxiv.org/abs/2502.18528)
- **Why it matters for CMatrix:** Shell-level autonomous pentest agent — the execution-layer component CMatrix's exploit agent must replicate. Evaluates on realistic network environments.

---

### 33. AutoPentest: Enhancing Vulnerability Management With Autonomous LLM Agents
- **Venue:** 🟠 arXiv (May 2025)
- **arXiv:** [2505.10321](https://arxiv.org/abs/2505.10321)
- **Code:** [GitHub](https://github.com/JuliusHenke/autopentest)
- **Why it matters for CMatrix:** Integrates GPT-4o with LangChain for enumeration-to-exploitation — the exact same stack (LangChain/LangGraph + LLM) as CMatrix. Direct implementation comparison.

---

### 34. RefPentester: A Knowledge-Informed Self-Reflective Penetration Testing Framework Based on Large Language Models
- **Venue:** 🟠 arXiv (May 2025)
- **arXiv:** [2505.07089](https://arxiv.org/abs/2505.07089)
- **Code:** [GitHub](https://github.com/ipa-lab/hackingBuddyGPT)
- **Why it matters for CMatrix:** Self-reflective reasoning in pentesting — directly maps to CMatrix's agent feedback loops and critique mechanisms. Knowledge-augmented approach aligns with Qdrant memory design.

---

### 35. CurriculumPT: LLM-Based Multi-Agent Autonomous Penetration Testing with Curriculum-Guided Task Scheduling
- **Venue:** 🟠 Applied Sciences (MDPI) — Aug 2025
- **DOI:** [10.3390/app15169096](https://www.mdpi.com/2076-3417/15/16/9096)
- **Why it matters for CMatrix:** Curriculum learning for progressive skill acquisition in multi-agent pentest — relevant to CMatrix's planned fine-tuning pipeline (easy → hard exploits, progressive task complexity).

---

### 36. Automated Penetration Testing with LLM Agents and Classical Planning
- **Venue:** 🟠 arXiv (Dec 2025)
- **arXiv:** [2512.11143](https://arxiv.org/abs/2512.11143)
- **Why it matters for CMatrix:** Combines classical planning (symbolic AI) with LLM agents for structured pentest execution — hybrid approach that CMatrix could adopt to reduce hallucination in multi-step exploit chains.

---

### 37. PentestMCP: LLM and MCP Based Multi-Agent Framework for Automated Penetration Testing
- **Venue:** 🟠 Preprint (Nov 2025)
- **DOI:** [10.21203/rs.3.rs-7582841/v1](https://sciety.org/articles/activity/10.21203/rs.3.rs-7582841/v1)
- **Why it matters for CMatrix:** MCP-based multi-agent pentest — this is *exactly* what CMatrix identified as a key future-proofing upgrade. Validates the MCP-first architecture CMatrix plans to adopt.

---

### 38. On the Surprising Efficacy of LLMs for Penetration-Testing
- **Venue:** 🟠 arXiv (Jul 2025)
- **arXiv:** [2507.00829](https://arxiv.org/abs/2507.00829)
- **Why it matters for CMatrix:** Provides empirical evidence for what LLMs can and can't do natively in pentesting — baseline capability study essential for CMatrix's model selection and agent design decisions.

---

### 39. Multi-Agent Penetration Testing AI for the Web
- **Venue:** 🟠 arXiv (Aug 2025)
- **arXiv:** [2508.20816](https://arxiv.org/abs/2508.20816)
- **Why it matters for CMatrix:** Web-specific multi-agent pentest — CMatrix's primary initial attack surface. Detailed agent decomposition for web recon, injection, exploitation.

---

### 40. Forewarned is Forearmed: A Survey on LLM-based Agents in Autonomous Cyberattacks
- **Venue:** 🟠 arXiv (May 2025)
- **arXiv:** [2505.12786](https://arxiv.org/abs/2505.12786)
- **Why it matters for CMatrix:** Comprehensive survey on offensive LLM agent capabilities across all attack stages. The reference survey most aligned with CMatrix's scope. Covers recon, exploitation, lateral movement, persistence.

---

### 41. AI-Augmented SOC: A Survey of LLMs and Agents for Security Automation
- **Venue:** 🟡 Journal of Cybersecurity & Privacy (MDPI) — Nov 2025
- **DOI:** [10.3390/jcp5040095](https://www.mdpi.com/2624-800X/5/4/95)
- **Why it matters for CMatrix:** Defines the SOC automation landscape CMatrix operates within. Published in CMatrix's primary target journal. Taxonomy of LLM agent roles in security pipelines.

---

### 42. Towards Automated Penetration Testing: Introducing LLM Benchmark, Analysis, and Improvements
- **Venue:** 🟠 UMAP 2025
- **DOI:** [10.1145/3708319.3733804](https://dl.acm.org/doi/full/10.1145/3708319.3733804)
- **Code:** [GitHub](https://github.com/anonyippi/PentestBenchmarkPaper)
- **Why it matters for CMatrix:** Standardized pentest benchmark + LLM comparison — baseline metrics CMatrix should report against.

---

### 43. Cybersecurity AI: A Game-Theoretic AI for Guiding Attack and Defense
- **Venue:** 🟠 arXiv (Jan 2026)
- **arXiv:** [2601.05887](https://arxiv.org/abs/2601.05887)
- **Why it matters for CMatrix:** Game-theoretic reasoning layer on top of LLM agents — reduces hallucination and improves strategic multi-step exploit planning. Future direction for CMatrix.

---

### 44. BountyBench: Dollar Impact of AI Agent Attackers and Defenders on Real-World Cybersecurity Systems
- **Venue:** 🔴 NeurIPS 2025 (Datasets and Benchmarks Track) — Stanford / UC Berkeley
- **arXiv:** [2505.15216](https://arxiv.org/abs/2505.15216)
- **Code:** [bountybench.github.io](https://bountybench.github.io)
- **Why it matters for CMatrix:** First benchmark to quantify AI agent cyber-capability in real dollar terms. 25 production systems, 40 bounties ($10–$30,485), covering 9 OWASP Top 10 risks. Defines Detect/Exploit/Patch task taxonomy — precisely the three phases CMatrix automates. Evaluated DeepSeek-R1 among 10 agents, giving CMatrix a direct reference point for its backbone model.

---

### 45. CRAKEN: Cybersecurity LLM Agent with Knowledge-Based Execution
- **Venue:** 🟠 arXiv (May 2025) — NYU
- **arXiv:** [2505.17107](https://arxiv.org/abs/2505.17107)
- **Code:** [GitHub](https://github.com/NYU-LLM-CTF/nyuctf_agents_craken)
- **Why it matters for CMatrix:** Knowledge-based RAG (Self-RAG + Graph-RAG) injected into a planner-executor multi-agent CTF system — 22% on NYU CTF Bench. Directly validates CMatrix's Qdrant + knowledge-graph approach for CVE/exploit retrieval. Built on top of D-CIPHER architecture.

---

### 46. CyberGym: Evaluating AI Agents' Real-World Cybersecurity Capabilities at Scale
- **Venue:** 🟠 arXiv (Jun 2025, v2 Oct 2025) — UC Berkeley (Dawn Song group)
- **arXiv:** [2506.02548](https://arxiv.org/abs/2506.02548)
- **Code:** [cybergym.io](https://cybergym.io)
- **Why it matters for CMatrix:** The largest cybersecurity benchmark in existence — 1,507 real-world vulnerabilities across 188 software projects, 7.5× larger than any prior benchmark. Led to discovery of 35 zero-day vulnerabilities and 17 incomplete patches in production software. The definitive scale benchmark CMatrix must eventually target.

---

### 47. An Empirical Evaluation of LLMs for Solving Offensive Security Challenges
- **Venue:** 🔴 NeurIPS 2024
- **arXiv:** [2402.11814](https://arxiv.org/abs/2402.11814)
- **Code:** [GitHub](https://github.com/NickNameInvalid/LLM_CTF)
- **Why it matters for CMatrix:** Gold-standard empirical evaluation of multiple LLMs on offensive security — establishes which models work, which fail. Directly informs CMatrix's LLM selection.

---

### 48. Shell or Nothing: Real-World Benchmarks and Memory-Activated Agents for Automated Penetration Testing
- **Venue:** 🟠 arXiv (2025)
- **URL:** [BRACU](https://dspace.bracu.ac.bd/xmlui/handle/10361/27423)
- **Why it matters for CMatrix:** Introduces memory-activated agents for automated penetration testing and real-world system benchmarks.

---

### 49. Perry: A High-level Framework for Accelerating Cyber Deception Experimentation
- **Venue:** 🟠 arXiv (Jun 2025)
- **arXiv:** [2506.20770](https://arxiv.org/abs/2506.20770)
- **Code:** [GitHub](https://github.com/bsinger98/Perry)
- **Why it matters for CMatrix:** High-level framework that accelerates cyber deception experimentation — crucial for simulating adversarial defenses against red-team agents.

---

### 50. PentestEval: Benchmarking LLM-based Penetration Testing with Modular and Stage-Level Design
- **Venue:** 🟠 arXiv (Dec 2025)
- **arXiv:** [2512.14233](https://arxiv.org/abs/2512.14233)
- **Why it matters for CMatrix:** Benchmarking platform designed to evaluate stage-level and modular penetration testing behaviors in LLM agents.

---

## `2024 Papers`

### 51. NYU CTF Bench: A Scalable Open-Source Benchmark Dataset for Evaluating LLMs in Offensive Security
- **Venue:** 🔴 NeurIPS 2024
- **URL:** [NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2024/hash/69d97a6493fbf016fff0a751f253ad18-Abstract-Datasets_and_Benchmarks_Track.html)
- **Code:** [GitHub](https://github.com/NYU-LLM-CTF/NYUCTFBench)
- **Why it matters for CMatrix:** The standard CTF benchmark for LLM evaluation. CMatrix's lab environment (lab.kaiofficial.xyz) should be evaluated against this dataset.

---

### 52. Teams of LLM Agents Can Exploit Zero-Day Vulnerabilities
- **Venue:** 🟠 arXiv (Jun 2024) — University of Illinois
- **arXiv:** [2406.01637](https://arxiv.org/abs/2406.01637)
- **Why it matters for CMatrix:** **Critical paper** — first proof that multi-agent LLM teams can exploit zero-day vulnerabilities with no prior knowledge. Hierarchical Planning and Task-Specific Agents (HPTSA) architecture is a direct ancestor of CMatrix's multi-agent design.

---

### 53. LLM Agents Can Autonomously Exploit One-Day Vulnerabilities
- **Venue:** 🟠 arXiv (Apr 2024) — University of Illinois
- **arXiv:** [2404.08144](https://arxiv.org/abs/2404.08144)
- **Why it matters for CMatrix:** The landmark paper proving GPT-4 agents can exploit 87% of real CVEs. Zero-shot capability on real-world vulnerabilities. CMatrix's core use case validated here first.

---

### 54. AutoAttacker: A Large Language Model Guided System to Implement Automatic Cyber-attacks
- **Venue:** 🟠 arXiv (Mar 2024)
- **arXiv:** [2403.01038](https://arxiv.org/abs/2403.01038)
- **Why it matters for CMatrix:** Post-exploitation automation (keyboard-operated attacks) — the execution phase CMatrix's exploitation agent handles. AutoAttacker is an early direct ancestor.

---

### 55. BreachSeek: A Multi-Agent Automated Penetration Tester
- **Venue:** 🟠 arXiv (Sep 2024)
- **arXiv:** [2409.03789](https://arxiv.org/abs/2409.03789)
- **Why it matters for CMatrix:** Multi-agent pentest system, one of the first to use specialized agents for each phase — directly comparable architecture to CMatrix.

---

### 56. Cybench: A Framework for Evaluating Cybersecurity Capabilities and Risks of Language Models
- **Venue:** 🟠 arXiv (Aug 2024)
- **arXiv:** [2408.08926](https://arxiv.org/abs/2408.08926)
- **Code:** [cybench.github.io](https://cybench.github.io/)
- **Why it matters for CMatrix:** 40-challenge CTF benchmark with step-by-step subtasks — the de facto evaluation framework. CMatrix must report Cybench numbers in any published evaluation.

---

### 57. HackSynth: LLM Agent and Evaluation Framework for Autonomous Penetration Testing
- **Venue:** 🟠 arXiv (Dec 2024)
- **arXiv:** [2412.01778](https://arxiv.org/abs/2412.01778)
- **Code:** [GitHub](https://github.com/aielte-research/HackSynth)
- **Why it matters for CMatrix:** Single-agent pentest with iterative planning + feedback summarization loop — shows even a single well-designed agent can outperform complex systems. Baseline comparison for CMatrix.

---

### 58. SoK: A Comparison of Autonomous Penetration Testing Agents
- **Venue:** 🟡 ARES 2024
- **DOI:** [10.1145/3664476.3664484](https://dl.acm.org/doi/10.1145/3664476.3664484)
- **Why it matters for CMatrix:** Systematization of knowledge paper — side-by-side comparison of all major autonomous pentest agents as of 2024. Essential for CMatrix's related work section.

---

### 59. AutoPT: How Far Are We from the End2End Automated Web Penetration Testing?
- **Venue:** 🟠 arXiv (Nov 2024)
- **arXiv:** [2411.01236](https://arxiv.org/abs/2411.01236)
- **Why it matters for CMatrix:** Defines the gap between current LLM-based approaches and true end-to-end web pentest automation. Direct roadmap for what CMatrix aims to close.

---

### 60. PENTEST-AI: An LLM-Powered Multi-Agents Framework for Penetration Testing Automation Leveraging MITRE ATT&CK
- **Venue:** 🟡 IEEE CSR 2024
- **DOI:** [10.1109/CSR.2024.10679480](https://ieeexplore.ieee.org/abstract/document/10679480)
- **Why it matters for CMatrix:** MITRE ATT&CK-aligned multi-agent pentest system — directly validates CMatrix's planned ATT&CK integration for structured attack path planning.

---

### 61. NYU CTF Bench: A Scalable Open-Source Benchmark Dataset for Evaluating LLMs in Offensive Security
- **Venue:** 🔴 NeurIPS 2024
- **URL:** [NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2024/hash/69d97a6493fbf016fff0a751f253ad18-Abstract-Datasets_and_Benchmarks_Track.html)
- **Code:** [GitHub](https://github.com/NYU-LLM-CTF/NYUCTFBench)
- **Why it matters for CMatrix:** Standard dataset and runner evaluating offensive security CTF solving capabilities.

---

## `2023 Papers`

### 62. PenHeal: A Two-Stage LLM Framework for Automated Pentesting and Optimal Remediation
- **Venue:** 🔴 ACM CCS 2023 (Workshop on Autonomous Cybersecurity)
- **arXiv:** [2407.17788](https://arxiv.org/abs/2407.17788)
- **DOI:** [10.1145/3689933.3690831](https://dl.acm.org/doi/abs/10.1145/3689933.3690831)
- **Why it matters for CMatrix:** First CCS paper combining automated pentesting + remediation recommendation — defines the detect-then-fix loop CMatrix's reporting module should implement.

---

### 63. Getting pwn'd by AI: Penetration Testing with Large Language Models
- **Venue:** 🔴 ESEC/FSE 2023
- **DOI:** [10.1145/3611643.3613083](https://dl.acm.org/doi/abs/10.1145/3611643.3613083)
- **Code:** [GitHub](https://github.com/ipa-lab/hackingBuddyGPT)
- **Why it matters for CMatrix:** One of the earliest serious academic treatments of LLM-based pentesting. Establishes the foundational argument and methodology that all later work (including PentestGPT) builds upon. FSE is CCF-A.

---

### 64. Language Agents as Hackers: Evaluating Cybersecurity Skills with Capture the Flag
- **Venue:** 🔴 MASEC Workshop @ NeurIPS 2023
- **arXiv:** [2308.10443](https://arxiv.org/abs/2308.10443)
- **Why it matters for CMatrix:** First serious CTF evaluation of LLM agents as offensive security actors — the origin paper for the CTF-as-benchmark paradigm that CMatrix's evaluation will use.

---

### 65. Using Large Language Models for Cybersecurity Capture-The-Flag Challenges and Certification Questions
- **Venue:** 🟠 arXiv (Aug 2023)
- **arXiv:** [2308.10443](https://arxiv.org/abs/2308.10443)
- **Why it matters for CMatrix:** Explores the early baseline performance of LLMs on cybersecurity capture-the-flag challenges.

---

# 🔗 LLM4Pentest: The Single Most Comprehensive Curated List
> 📢 **Active community repositories and curated datasets for continuous monitoring.**

---

**Repository:** [github.com/simon-p-j-r/LLM4Pentest](https://github.com/simon-p-j-r/LLM4Pentest)  
**Maintainer:** DAS Lab (Cheng Huang's Lab)   
**Relevance:** 🎯 Papers, blogs, MCP tools, benchmarks, datasets

---
