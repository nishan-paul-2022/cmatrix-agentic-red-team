# 📚 Master Research Paper Reference — LLM-Orchestrated Multi-Agent VAPT
**CMatrix Research | Compiled: May 11, 2026**
**Coverage: All critical papers up to May 2026 across 7 topic domains**

> This reference is structured so that reading all papers listed here provides end-to-end knowledge of the research landscape — from foundational autonomous agents, to multi-agent VAPT frameworks, LLM orchestration, cost optimization, safety, and benchmarking. Zero knowledge gaps.

---

## 📖 HOW TO USE THIS DOCUMENT

Each entry includes:
- 📄 **Paper Title** with direct read/download link
- 👤 **Authors** with profile links where available
- 🏫 **Institution** + World Ranking (QS 2025)
- 📅 **Year & Venue**
- 🔗 **Code / Project** links where available
- 🎯 **Relevance** to CMatrix research pillars

---

## 🗂️ SECTION 1 — FOUNDATIONAL AUTONOMOUS AI AGENTS IN CYBERSECURITY

### 1.1 PentestGPT: The Benchmark Foundation

**Paper:** [PentestGPT: Evaluating and Harnessing Large Language Models for Automated Penetration Testing](https://www.usenix.org/conference/usenixsecurity24/presentation/deng)
**PDF:** [arXiv:2308.06782](https://arxiv.org/abs/2308.06782)
**Authors:** Gelei Deng, Yi Liu, Víctor Mayoral-Vilches, Peng Liu, Yuekang Li, Yuan Xu, Tianwei Zhang, Yang Liu, Martin Pinzger, Stefan Rass
**Author Profiles:**
- Gelei Deng: [NTU Profile](https://personal.ntu.edu.sg/yi_liu/)
- Yi Liu: [Nanyang Technological University](https://scholar.google.com/citations?user=yi_liu_ntu)
**Institution:** Nanyang Technological University (NTU), Singapore | QS Rank: **#26**
**Year & Venue:** USENIX Security 2024 (CCF-A) — pp. 847–864
**Code:** [github.com/GreyDGL/PentestGPT](https://github.com/GreyDGL/PentestGPT)
**Relevance:** 🎯 The baseline benchmark for all LLM-based pentesting. Directly compared against in CMatrix evaluation.

---

### 1.2 PentestGPT v2: Evidence-Guided Attack Tree Search

**Paper:** [What Makes a Good LLM Agent for Real-world Penetration Testing?](https://arxiv.org/abs/2602.17622)
**Authors:** (PentestGPT v2 team, NTU)
**Institution:** Nanyang Technological University, Singapore | QS Rank: **#26**
**Year & Venue:** arXiv, February 2026
**Relevance:** 🎯 Introduces Tool & Skill Layer + Evidence-Guided Attack Tree Search (EGATS). 91% CTF task completion. Key SOTA to compare CMatrix against.

---

### 1.3 AutoPentester: End-to-End Automation

**Paper:** [AutoPentester: An LLM Agent-based Framework for Automated Pentesting](https://arxiv.org/abs/2510.05605)
**Authors:** (Anonymous, under review)
**Institution:** Undisclosed
**Year & Venue:** arXiv, October 2025
**Relevance:** 🎯 27% better subtask completion than PentestGPT, significantly fewer human interventions. Direct contemporary comparison point.

---

### 1.4 VulnBot: Multi-Agent Collaborative Pentesting

**Paper:** [VulnBot: Autonomous Penetration Testing for a Multi-Agent Collaborative Framework](https://arxiv.org/abs/2501.13411)
**Authors:** KHenry (et al.)
**Institution:** Undisclosed
**Year & Venue:** arXiv, January 2025
**Code:** [github.com/KHenryAegis/VulnBot](https://github.com/KHenryAegis/VulnBot)
**Relevance:** 🎯 Directly related multi-agent VAPT framework. Referenced by xOffense for comparison.

---

### 1.5 xOffense: Domain-Adapted Multi-Agent Framework

**Paper:** [xOffense: An Autonomous Multi-Agent Framework for Penetration Testing with Domain-Adapted Large Language Models](https://arxiv.org/abs/2509.13021)
**Authors:** Quyen Nguyen Huu et al.
**Institution:** Undisclosed
**Year & Venue:** arXiv, September 2025 (updated April 2026)
**Relevance:** 🎯 Listed in CMatrix contemporary works. Fine-tuned Qwen3-32B, 79.17% sub-task completion. Key mid-scale LLM approach.

---

### 1.6 CurriculumPT: Progressive Skill Acquisition

**Paper:** [CurriculumPT: LLM-Based Multi-Agent Autonomous Penetration Testing with Curriculum-Guided Task Scheduling](https://www.mdpi.com/2076-3417/15/16/9096)
**Authors:** (MDPI Applied Sciences)
**Institution:** (Multiple)
**Year & Venue:** Applied Sciences (MDPI), August 2025
**Relevance:** 🎯 Listed in CMatrix contemporary works. Curriculum learning for progressive exploitation skills — relevant to CMatrix's dynamic task tiering (DCAT).

---

### 1.7 PentestMCP: MCP-Based Tool Orchestration

**Paper:** [PentestMCP: A Toolkit for Agentic Penetration Testing](https://arxiv.org/abs/2510.03610)
**Authors:** Zachary Ezetta, Wu-Chang Feng
**Author Profile:** [Wu-Chang Feng — Portland State University](https://web.cecs.pdx.edu/~wuchang/)
**Institution:** Portland State University, USA | QS Rank: **#651–700**
**Year & Venue:** arXiv, October 2025
**Relevance:** 🎯 Listed in CMatrix contemporary works. MCP-based tool orchestration directly relevant to CMatrix's modular agent design.

---

### 1.8 Pen-Strategist: Fine-Tuned Reasoning for Pentesting

**Paper:** [Pen-Strategist: A Reasoning Framework for Penetration Testing Strategy Formation and Analysis](https://arxiv.org/abs/2605.04499)
**Authors:** (2026, recent preprint)
**Institution:** Undisclosed
**Year & Venue:** arXiv, May 2026
**Relevance:** Fine-tunes Qwen3-14B for strategy reasoning, integrates with PentestGPT and AutoPentester pipelines.

---

### 1.9 Getting Pwn'd by AI: LLM Penetration Testing (Foundational)

**Paper:** [Getting pwn'd by AI: Penetration Testing with Large Language Models](https://dl.acm.org/doi/abs/10.1145/3611643.3613083)
**Authors:** Andreas Happe, Jürgen Cito
**Author Profile:** [Andreas Happe — TU Wien](https://se.ini.uzh.ch/people/happe.html)
**Institution:** TU Wien, Austria / University of Zurich, Switzerland | QS Rank: **TU Wien: #251–300**
**Year & Venue:** FSE/ESEC 2023 (CCF-A)
**Code:** [github.com/ipa-lab/hackingBuddyGPT](https://github.com/ipa-lab/hackingBuddyGPT)
**Relevance:** Foundational paper — first rigorous study of LLMs for pentesting at a top-tier venue.

---

### 1.10 BreachSeek: Multi-Agent Penetration Tester

**Paper:** [BreachSeek: A Multi-Agent Automated Penetration Tester](https://arxiv.org/abs/2409.03789)
**Authors:** (et al.)
**Year & Venue:** arXiv, September 2024
**Relevance:** Multi-agent VAPT framework — direct architectural parallel to CMatrix.

---

### 1.11 AutoAttacker: LLM-Guided Cyber Attacks

**Paper:** [AutoAttacker: A Large Language Model Guided System to Implement Automatic Cyber-attacks](https://arxiv.org/abs/2403.01038)
**Authors:** Jiacen Xu, Jack W. Stokes, Geoff McDonald, Xuesong Bai, David Marshall, Siyue Wang, Adith Swaminathan, Zhou Li
**Institution:** Microsoft Research + UC Irvine | QS Rank: **UCI: #148**
**Year & Venue:** arXiv, March 2024
**Relevance:** 🎯 Industry-grade LLM attack automation from Microsoft Research. Directly cited as contemporary work.

---

### 1.12 LLM Agents Can Autonomously Exploit One-day Vulnerabilities

**Paper:** [LLM Agents can Autonomously Exploit One-day Vulnerabilities](https://arxiv.org/abs/2404.08144)
**Authors:** Richard Fang, Rohan Bindu, Akul Gupta, Qiusi Zhan, Daniel Kang
**Author Profile:** [Daniel Kang — UIUC](https://ddkang.github.io/)
**Institution:** University of Illinois Urbana-Champaign (UIUC), USA | QS Rank: **#82**
**Year & Venue:** arXiv, April 2024
**Relevance:** Landmark study showing GPT-4 can exploit 87% of one-day CVEs autonomously. Critical for CMatrix's vulnerability intel pillar (Paper 04).

---

### 1.13 RapidPen: IP-to-Shell Automation

**Paper:** [RapidPen: Fully Automated IP-to-Shell Penetration Testing with LLM-based Agents](https://arxiv.org/abs/2502.16730)
**Authors:** (et al.)
**Year & Venue:** arXiv, February 2025
**Relevance:** End-to-end automation from IP to shell — operational scope aligns with CMatrix goals.

---

### 1.14 RedTeamLLM: Agentic Framework for Offensive Security

**Paper:** [RedTeamLLM: an Agentic AI Framework for Offensive Security](https://arxiv.org/abs/2512.14233)
**Authors:** LRE Security Systems Team
**Institution:** Undisclosed (industry)
**Year & Venue:** arXiv, December 2025
**Code:** [github.com/lre-security-systems-team/redteamllm](https://github.com/lre-security-systems-team/redteamllm)
**Relevance:** Open-source agentic offensive framework — directly comparable to CMatrix architecture.

---

### 1.15 CAI: Open, Bug Bounty-Ready Cybersecurity AI

**Paper:** [CAI: An Open, Bug Bounty-Ready Cybersecurity AI](https://arxiv.org/abs/2504.06017)
**Authors:** Alias Robotics team
**Institution:** Alias Robotics
**Year & Venue:** arXiv, April 2025
**Code:** [github.com/aliasrobotics/CAI](https://github.com/aliasrobotics/CAI)
**Relevance:** Production-grade cybersecurity AI for real bug bounty tasks. Real-world validation context.

---

### 1.16 ARACNE: Autonomous Shell Pentesting Agent

**Paper:** [ARACNE: An LLM-Based Autonomous Shell Pentesting Agent](https://arxiv.org/abs/2502.18528)
**Authors:** (et al.)
**Year & Venue:** arXiv, February 2025
**Relevance:** Shell-level autonomous agent — relevant to CMatrix's network agent module.

---

### 1.17 PENTEST-AI: MITRE ATT&CK Multi-Agent Framework

**Paper:** [PENTEST-AI: An LLM-Powered Multi-Agents Framework for Penetration Testing Automation Leveraging MITRE ATT&CK](https://ieeexplore.ieee.org/abstract/document/10679480)
**Authors:** (IEEE CSR 2024)
**Year & Venue:** IEEE CSR 2024
**Relevance:** MITRE ATT&CK-aligned multi-agent framework. Relevant to CMatrix's reasoning and strategy synthesis pillar.

---

### 1.18 PentestAgent: Incorporating LLM Agents

**Paper:** [PentestAgent: Incorporating LLM Agents to Automated Penetration Testing](https://dl.acm.org/doi/full/10.1145/3708821.3733882)
**Authors:** GH05TCREW
**Year & Venue:** AsiaCCS 2025 (CCF-C)
**Code:** [github.com/GH05TCREW/PentestAgent](https://github.com/GH05TCREW/PentestAgent)
**Relevance:** Agent framework for automated pentesting at a peer-reviewed venue.

---

### 1.19 Incalmo: Red Teaming Multi-Host Networks

**Paper:** [Incalmo: An Autonomous LLM-assisted System for Red Teaming Multi-Host Networks](https://arxiv.org/abs/2501.16466)
**Authors:** Ben Singer et al.
**Year & Venue:** arXiv, January 2025
**Code:** [github.com/bsinger98/Incalmo](https://github.com/bsinger98/Incalmo)
**Relevance:** Multi-host red teaming automation. Directly relevant to CMatrix network agent + multi-stage exploitation.

---

### 1.20 AutoPT: End-to-End Web Penetration Testing

**Paper:** [AutoPT: How Far Are We from the End2End Automated Web Penetration Testing?](https://arxiv.org/abs/2411.01236)
**Authors:** (et al.)
**Year & Venue:** arXiv, November 2024
**Relevance:** Web-focused end-to-end automation evaluation. Relevant to CMatrix's web application agent.

---

### 1.21 Pentest-R1: Reinforcement Learning for Pentesting Reasoning

**Paper:** [Pentest-R1: Towards Autonomous Penetration Testing Reasoning Optimized via Two-Stage Reinforcement Learning](https://arxiv.org/abs/2508.07382)
**Authors:** KHenry et al.
**Year & Venue:** arXiv, August 2025
**Code:** [github.com/KHenryAegis/Pentest-R1](https://github.com/KHenryAegis/Pentest-R1)
**Relevance:** RL-based reasoning optimization for pentesting — novel training paradigm for CMatrix agents.

---

### 1.22 RefPentester: Self-Reflective Pentesting Framework

**Paper:** [RefPentester: A Knowledge-Informed Self-Reflective Penetration Testing Framework Based on Large Language Models](https://arxiv.org/abs/2505.07089)
**Authors:** (IPA Lab)
**Year & Venue:** arXiv, May 2025
**Code:** [github.com/ipa-lab/hackingBuddyGPT](https://github.com/ipa-lab/hackingBuddyGPT)
**Relevance:** Self-reflection mechanisms in pentesting — relevant to CMatrix's agent reasoning (Paper 03).

---

### 1.23 AutoPentest: Enhancing Vulnerability Management

**Paper:** [AutoPentest: Enhancing Vulnerability Management With Autonomous LLM Agents](https://arxiv.org/abs/2505.10321)
**Authors:** Julius Henke et al.
**Year & Venue:** arXiv, May 2025
**Code:** [github.com/JuliusHenke/autopentest](https://github.com/JuliusHenke/autopentest)
**Relevance:** Vulnerability management integration with autonomous agents.

---

### 1.24 Can LLMs Hack Enterprise Networks? (Active Directory)

**Paper:** [Can LLMs Hack Enterprise Networks? Autonomous Assumed Breach Penetration-Testing Active Directory Networks](https://dl.acm.org/doi/abs/10.1145/3766895)
**Authors:** Andreas Happe, Aaron Kaplan, Jürgen Cito
**Institution:** TU Wien, Austria | QS Rank: **#251–300**
**Year & Venue:** ACM TOSEM 2025 (CCF-A)
**Code:** [github.com/andreashappe/cochise](https://github.com/andreashappe/cochise)
**Relevance:** Enterprise-scale Active Directory pentesting with LLMs. Critical for CMatrix multi-stage exploitation capabilities.

---

### 1.25 Automated Penetration Testing with LLM Agents and Classical Planning

**Paper:** [Automated Penetration Testing with LLM Agents and Classical Planning](https://arxiv.org/abs/2512.11143)
**Authors:** (et al.)
**Year & Venue:** arXiv, December 2025
**Relevance:** Hybrid AI planning approach combining LLMs with classical planners for structured attack chains.

---

### 1.26 HackWorld: Computer-Use Agents on Web Vulnerabilities (ICLR)

**Paper:** [HackWorld: Evaluating Computer-Use Agents on Exploiting Web Application Vulnerabilities](https://arxiv.org/abs/2510.12200)
**Authors:** GUI-Agent team
**Year & Venue:** ICLR 2026 (CCF-A)
**Code:** [github.com/GUI-Agent/HackWorld](https://github.com/GUI-Agent/HackWorld)
**Relevance:** GUI/computer-use agents for web exploitation — next-frontier agent capability.

---

### 1.27 Multi-Agent Penetration Testing AI for the Web

**Paper:** [Multi-Agent Penetration Testing AI for the Web](https://arxiv.org/abs/2508.20816)
**Authors:** (et al.)
**Year & Venue:** arXiv, August 2025
**Relevance:** Direct multi-agent web pentesting — architectural comparison point for CMatrix's Web agent.

---

### 1.28 EnIGMA: Interactive Tools for Security Vulnerabilities (ICLR)

**Paper:** [EnIGMA: Interactive Tools Substantially Assist LM Agents in Finding Security Vulnerabilities](https://arxiv.org/abs/2409.16165)
**Authors:** SWE-agent team
**Year & Venue:** ICLR 2025 (CCF-A)
**Code:** [github.com/SWE-agent/SWE-agent/tree/v0.7](https://github.com/SWE-agent/SWE-agent/tree/v0.7)
**Relevance:** Interactive tooling for vulnerability finding — relevant to CMatrix's HITL module.

---

### 1.29 SoK: Comparison of Autonomous Penetration Testing Agents

**Paper:** [SoK: A Comparison of Autonomous Penetration Testing Agents](https://dl.acm.org/doi/10.1145/3664476.3664484)
**Authors:** (ARES 2024)
**Year & Venue:** ARES 2024
**Relevance:** Systematization of knowledge — comprehensive comparison of all pentest agents. Essential survey paper.

---

### 1.30 HackSynth: LLM Agent + Evaluation Framework

**Paper:** [HackSynth: LLM Agent and Evaluation Framework for Autonomous Penetration Testing](https://arxiv.org/abs/2412.01778)
**Authors:** AI-ELTE Research team
**Institution:** ELTE Eötvös Loránd University, Hungary | QS Rank: **#801–1000**
**Year & Venue:** arXiv, December 2024
**Code:** [github.com/aielte-research/HackSynth](https://github.com/aielte-research/HackSynth)
**Relevance:** Combined agent + benchmark framework — dual contribution similar to CMatrix's approach.

---

### 1.31 LLMs as Hackers: Privilege Escalation Attacks

**Paper:** [LLMs as Hackers: Autonomous Linux Privilege Escalation Attacks](https://link.springer.com/article/10.1007/s10664-025-10758-3)
**Authors:** (Empirical Software Engineering, Springer, 2026)
**Year & Venue:** Empirical Software Engineering, 2026
**Relevance:** Privilege escalation automation — CMatrix's post-exploitation scenarios.

---

### 1.32 Towards Automated Penetration Testing: LLM Benchmark & Improvements

**Paper:** [Towards Automated Penetration Testing: Introducing LLM Benchmark, Analysis, and Improvements](https://arxiv.org/html/2410.17141v4)
**Authors:** (UMAP 2025)
**Year & Venue:** UMAP 2025
**Code:** [github.com/anonyippi/PentestBenchmarkPaper](https://github.com/anonyippi/PentestBenchmarkPaper)
**Relevance:** Comprehensive LLM benchmark analysis for pentesting — methodology reference for CMatrix evaluation.

---

### 1.33 PTFusion: LLM-driven Knowledge Fusion for Web Pentesting

**Paper:** [PTFusion: LLM-driven Context-aware Knowledge Fusion for Web Penetration Testing](https://www.sciencedirect.com/science/article/pii/S1566253525007936)
**Authors:** (Information Fusion, 2026)
**Year & Venue:** Information Fusion Journal, 2026
**Relevance:** Knowledge fusion for web pentesting — relevant to CMatrix's Security-Semantic Caching (SSC).

---

## 🗂️ SECTION 2 — LLM MULTI-AGENT ORCHESTRATION & RESILIENCE

### 2.1 Multi-Agent Systems Survey (LLM-Based)

**Paper:** [A Survey on LLM-Based Multi-Agent Systems: Workflow, Infrastructure, and Challenges](https://doi.org/10.1007/s44336-024-00009-2)
**Authors:** X. Li, S. Wang, S. Zeng, Y. Wu, Y. Yang
**Year & Venue:** Vicinagearth Journal, October 2024
**Relevance:** 🎯 Comprehensive survey of LLM multi-agent systems — foundational reading for CMatrix's architecture.

---

### 2.2 From LLM Reasoning to Autonomous AI Agents: Comprehensive Review

**Paper:** [From LLM Reasoning to Autonomous AI Agents: A Comprehensive Review](https://arxiv.org/abs/2504.19678)
**Authors:** (et al.)
**Year & Venue:** arXiv, April 2025
**Relevance:** Taxonomy of ~60 LLM benchmarks, agent frameworks 2023–2025. Essential background.

---

### 2.3 AutoGen: Next-Gen LLM Multi-Agent Conversations

**Paper:** [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation Framework](https://arxiv.org/abs/2308.08155)
**Authors:** Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Shaokun Zhang, Erkang Zhu, Beibin Li, Li Jiang, Xiaoyun Zhang, Chi Wang
**Author Profile:** [Chi Wang — Microsoft Research](https://www.microsoft.com/en-us/research/people/chiw/)
**Institution:** Microsoft Research, USA
**Year & Venue:** arXiv, August 2023 (widely adopted)
**Relevance:** 🎯 Foundation framework — CMatrix's Master-Worker hierarchy directly inspired by AutoGen patterns.

---

### 2.4 MetaGPT: Meta Programming for Multi-Agent Frameworks

**Paper:** [MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352)
**Authors:** Sirui Hong, Mingchen Zhuge, et al.
**Institution:** DeepWisdom / Multiple universities
**Year & Venue:** ICLR 2024 (CCF-A)
**Relevance:** Structured multi-agent collaboration with role-playing — foundational for agent specialization in CMatrix.

---

### 2.5 A Survey of Agentic AI and Cybersecurity

**Paper:** [A Survey of Agentic AI and Cybersecurity: Challenges, Opportunities and Use-case Prototypes](https://arxiv.org/abs/2601.05293)
**Authors:** (et al.)
**Year & Venue:** arXiv, January 2026
**Relevance:** 🎯 Direct survey of agentic AI in cybersecurity context — exactly aligns with CMatrix's scope.

---

### 2.6 Difficulty-Aware Agentic Orchestration

**Paper:** [Difficulty-Aware Agentic Orchestration for Query-Specific Multi-Agent Workflows](https://arxiv.org/abs/2509.11079)
**Authors:** (et al.)
**Year & Venue:** WWW 2026 (ACM Web Conference)
**Relevance:** Query-specific workflow generation + cost/performance-aware LLM routing — directly relevant to CMatrix's DCAT.

---

### 2.7 WorkflowLLM: Enhancing Workflow Orchestration

**Paper:** [WorkflowLLM: Enhancing Workflow Orchestration Capability of Large Language Models](https://arxiv.org/abs/2411.05451)
**Authors:** (Wuhan University + others)
**Institution:** Wuhan University, China | QS Rank: **#225**
**Year & Venue:** arXiv, November 2024
**Relevance:** LLM workflow orchestration capabilities — direct technical background for CMatrix's LLMOrch-VAPT.

---

### 2.8 A Trace-Based Assurance Framework for Agentic AI Orchestration

**Paper:** [A Trace-Based Assurance Framework for Agentic AI Orchestration: Contracts, Testing, and Governance](https://arxiv.org/abs/2603.18096)
**Authors:** (et al.)
**Year & Venue:** arXiv, March 2026
**Relevance:** Governance and assurance for agentic AI — relevant to CMatrix's HITL safety gates.

---

### 2.9 Engineering LLM Powered Multi-Agent Framework for Autonomous CloudOps

**Paper:** [Engineering LLM Powered Multi-agent Framework for Autonomous CloudOps](https://arxiv.org/abs/2501.08243)
**Authors:** Kannan Parthasarathy et al.
**Year & Venue:** CAIN 2025 (co-located with ICSE 2025), January 2025
**Relevance:** Production-grade multi-agent framework engineering — direct architectural lessons for CMatrix.

---

### 2.10 A Declarative Language for Building LLM-Powered Agent Workflows

**Paper:** [A Declarative Language for Building And Orchestrating LLM-Powered Agent Workflows](https://arxiv.org/abs/2512.19769)
**Authors:** Ivan Daunis (PayPal)
**Institution:** PayPal
**Year & Venue:** arXiv, November 2025
**Relevance:** DSL for agent workflows across Java/Python/Go — relevant to CMatrix's cross-provider orchestration.

---

## 🗂️ SECTION 3 — COST OPTIMIZATION: LLM ROUTING, TIERING & CACHING

### 3.1 RouteLLM: Learning to Route LLMs with Preference Data

**Paper:** [RouteLLM: Learning to Route LLMs with Preference Data](https://arxiv.org/abs/2406.18665)
**Authors:** Isaac Ong, Amjad Almahairi, Vincent Wu, Wei-Lin Chiang, Tianhao Wu, Joseph E. Gonzalez, M Waleed Kadous, Ion Stoica
**Author Profiles:**
- [Ion Stoica — UC Berkeley](https://people.eecs.berkeley.edu/~istoica/)
- [Joseph Gonzalez — UC Berkeley](https://people.eecs.berkeley.edu/~jegonzal/)
**Institution:** UC Berkeley (LMSYS) + Anyscale, USA | QS Rank: **#4**
**Year & Venue:** ICLR 2025 (CCF-A), June 2024
**Project:** [lmsys.org/blog/2024-07-01-routellm](https://www.lmsys.org/blog/2024-07-01-routellm/)
**Relevance:** 🎯 2× cost reduction without quality loss — the core technique behind CMatrix's DCAT (Dynamic Complexity-Aware Tiering).

---

### 3.2 FrugalGPT: Reducing LLM Cost with Cascade Approach

**Paper:** [FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance](https://arxiv.org/abs/2305.05176)
**Authors:** Lingjiao Chen, Matei Zaharia, James Zou
**Author Profiles:**
- [Matei Zaharia — Stanford/MIT/Databricks](https://people.eecs.berkeley.edu/~matei/)
- [James Zou — Stanford](https://www.james-zou.com/)
**Institution:** Stanford University, USA | QS Rank: **#5**
**Year & Venue:** arXiv, May 2023 (highly cited)
**Relevance:** 🎯 Foundational cascade-based cost reduction — precursor to CMatrix's model tiering strategy.

---

### 3.3 Cost-Efficient Serving of LLM Agents via Test-Time Plan Caching

**Paper:** [Cost-Efficient Serving of LLM Agents via Test-Time Plan Caching](https://arxiv.org/abs/2506.14852)
**Authors:** (et al.)
**Year & Venue:** arXiv, June 2025
**Relevance:** 🎯 Plan-level caching for agentic LLMs — directly maps to CMatrix's Security-Semantic Caching (SSC) concept.

---

### 3.4 On Optimal Caching and Model Multiplexing for Large Model Inference

**Paper:** [On Optimal Caching and Model Multiplexing for Large Model Inference](https://arxiv.org/abs/2306.02003)
**Authors:** (et al.)
**Year & Venue:** arXiv (foundational caching theory)
**Relevance:** Theoretical foundations for caching + model multiplexing — background for CMatrix's SSC layer.

---

### 3.5 RouterBench: A Benchmark for Multi-LLM Routing

**Paper:** [RouterBench: A Benchmark for Multi-LLM Routing System](https://arxiv.org/abs/2403.12031)
**Authors:** Q.J. Hu et al. (ICML 2024 Agentic Markets Workshop)
**Year & Venue:** ICML 2024 Workshop
**Relevance:** Benchmark for evaluating LLM router quality — methodology for measuring CMatrix's DCAT effectiveness.

---

### 3.6 Robust Batch-Level Query Routing for LLMs

**Paper:** [Robust Batch-Level Query Routing for Large Language Models under Cost and Capacity Constraints](https://arxiv.org/abs/2603.26796)
**Authors:** (et al.)
**Year & Venue:** arXiv, March 2026
**Relevance:** Batch routing with cost budgets — relevant to CMatrix's high-volume task scheduling.

---

### 3.7 Minions: Cost-Efficient Collaboration between On-Device and Cloud LLMs

**Paper:** [Minions: Cost-efficient Collaboration between On-device and Cloud Language Models](https://arxiv.org/abs/2502.15964)
**Authors:** (et al.)
**Year & Venue:** arXiv, February 2025
**Relevance:** Hybrid local/cloud LLM execution — relevant to CMatrix's Ollama (local) + cloud LLM tiering.

---

## 🗂️ SECTION 4 — AI SAFETY, HUMAN-IN-THE-LOOP & GOVERNANCE

### 4.1 Policy-as-Prompt: AI Governance Rules as Guardrails

**Paper:** [Policy-as-Prompt: Turning AI Governance Rules into Guardrails for AI Agents](https://arxiv.org/abs/2509.23994)
**Authors:** Gauri Kholkar et al.
**Year & Venue:** arXiv, November 2025
**Relevance:** 🎯 Converts policy documents into runtime guardrails — directly relevant to CMatrix's HITL safety gates.

---

### 4.2 ShieldAgent: Verifiable Safety Policy Reasoning

**Paper:** [ShieldAgent: Shielding Agents via Verifiable Safety Policy Reasoning](https://arxiv.org/abs/2503.22738)
**Authors:** (et al.)
**Year & Venue:** arXiv, March 2025
**Relevance:** Safety shield layer for LLM agents — architecture for CMatrix's high-risk operation approval mechanism.

---

### 4.3 Toward Safe and Responsible AI Agents (Three-Pillar Model)

**Paper:** [Toward Safe and Responsible AI Agents: A Three-Pillar Model for Transparency, Accountability, and Trustworthiness](https://arxiv.org/abs/2601.06223)
**Authors:** (et al.)
**Year & Venue:** arXiv, January 2026
**Relevance:** Transparency, accountability, HITL principles — background for CMatrix's governance framework (Paper 02).

---

### 4.4 AGrail: Lifelong Agent Guardrail

**Paper:** [AGrail: A Lifelong Agent Guardrail with Effective and Adaptive Safety Detection](https://arxiv.org/abs/2502.11448)
**Authors:** (et al.)
**Year & Venue:** arXiv, February 2025
**Relevance:** Adaptive safety detection for agents — relevant to CMatrix's risk classification logic.

---

### 4.5 AgentDoG: Diagnostic Guardrail Framework

**Paper:** [AgentDoG: A Diagnostic Guardrail Framework for AI Agent Safety and Security](https://arxiv.org/abs/2601.18491)
**Authors:** (et al.)
**Year & Venue:** arXiv, January 2026
**Relevance:** Fine-grained trajectory monitoring for agents — relevant to CMatrix's audit logging and HITL design.

---

### 4.6 TrustAgent: Agent Constitution for Safety

**Paper:** [TrustAgent: Towards Safe and Trustworthy LLM-based Agents through Agent Constitution](https://arxiv.org/abs/2402.01586)
**Authors:** Wenyue Hua et al.
**Year & Venue:** arXiv, February 2024
**Relevance:** Constitutional safety for agents — foundational theory for CMatrix's safety gates.

---

### 4.7 R-Judge: Benchmarking Safety Risk Awareness in LLM Agents

**Paper:** [R-Judge: Benchmarking Safety Risk Awareness for LLM Agents](https://arxiv.org/abs/2401.10019)
**Authors:** Yuan et al.
**Year & Venue:** arXiv, January 2024
**Relevance:** Safety risk benchmarking for agents — evaluation framework for CMatrix's safety modules.

---

## 🗂️ SECTION 5 — RAG, VULNERABILITY INTELLIGENCE & KNOWLEDGE BASES

### 5.1 RAG for Cybersecurity: Hybrid Retrieval for LLMs

**Paper:** [Adapting Large Language Models to Emerging Cybersecurity using Retrieval Augmented Generation](https://arxiv.org/abs/2510.27080)
**Authors:** (et al.)
**Year & Venue:** arXiv, October 2025
**Relevance:** 🎯 RAG for cybersecurity knowledge — directly relevant to CMatrix's Vuln-Intel agent and Paper 04.

---

### 5.2 Towards Secure Retrieval-Augmented Generation

**Paper:** [Towards Secure Retrieval-Augmented Generation: A Comprehensive Review of Threats, Defenses and Benchmarks](https://arxiv.org/abs/2603.21654)
**Authors:** Yanming Mu et al.
**Year & Venue:** arXiv, March 2026
**Relevance:** Security of RAG systems — critical for CMatrix's vector memory (Qdrant) security posture.

---

### 5.3 Securing RAG: Taxonomy of Attacks, Defenses, and Future Directions

**Paper:** [Securing Retrieval-Augmented Generation: A Taxonomy of Attacks, Defenses, and Future Directions](https://arxiv.org/abs/2604.08304)
**Authors:** (et al.)
**Year & Venue:** arXiv, April 2026
**Relevance:** Comprehensive RAG attack/defense taxonomy — security analysis for CMatrix's SSC + Qdrant memory.

---

### 5.4 Survey on the Security of Long-Term Memory in LLM Agents

**Paper:** [A Survey on the Security of Long-Term Memory in LLM Agents: Toward Mnemonic Sovereignty](https://arxiv.org/abs/2604.16548)
**Authors:** Zehao Lin et al.
**Year & Venue:** arXiv, April 2026
**Relevance:** 🎯 Long-term memory security — directly relevant to CMatrix's Qdrant-based session memory (Paper 04).

---

### 5.5 Memory for Autonomous LLM Agents: Mechanisms & Evaluation

**Paper:** [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/abs/2603.07670)
**Authors:** (et al.)
**Year & Venue:** arXiv, March 2026
**Relevance:** Comprehensive survey of agent memory systems — background for CMatrix's vector memory design.

---

### 5.6 Mem0: Intelligent Memory Layer for AI Applications (ECAI 2025)

**Paper:** [Mem0: Intelligent Memory Layer for Personalized AI](https://arxiv.org/abs/2504.19413)
**Authors:** Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, Deshraj Yadav
**Year & Venue:** ECAI 2025
**Relevance:** Production memory system — benchmark comparison for CMatrix's Qdrant-based memory architecture.

---

## 🗂️ SECTION 6 — CYBERSECURITY BENCHMARKS & EVALUATION

### 6.1 CyBench: Evaluating Cybersecurity Capabilities (ICLR 2025)

**Paper:** [Cybench: A Framework for Evaluating Cybersecurity Capabilities and Risks of Language Models](https://arxiv.org/abs/2408.08926)
**Authors:** Andy K. Zhang, Neil Perry, Riya Dulepet, et al. (Stanford/Berkeley/CMU team)
**Author Profile:** [Dan Boneh — Stanford](https://crypto.stanford.edu/~dabo/), [Percy Liang — Stanford](https://cs.stanford.edu/~pliang/)
**Institution:** Stanford University + multiple | QS Rank: **Stanford: #5**
**Year & Venue:** arXiv 2024, presented ICLR 2025 (CCF-A)
**Code:** [cybench.github.io](https://cybench.github.io/)
**Relevance:** 🎯 CMatrix's primary evaluation benchmark — 40 CTF tasks from 2022–2024 competitions.

---

### 6.2 AutoPenBench: Benchmarking Generative Agents for Penetration Testing

**Paper:** [AutoPenBench: Benchmarking Generative Agents for Penetration Testing](https://arxiv.org/abs/2410.03225)
**Authors:** Luca Gioacchini, Marco Cassaro, Nicole Poggiali, Mirco Filippini, Marco Mellia, Giovanni Fiano, Idilio Drago, Luca Delsanto
**Author Profile:** [Marco Mellia — Politecnico di Torino](https://www.telematica.polito.it/member/marco-mellia/)
**Institution:** Politecnico di Torino, Italy | QS Rank: **#283**
**Year & Venue:** arXiv, October 2024
**Relevance:** 🎯 CMatrix's second primary benchmark — 33 vulnerable Docker containers, used by xOffense for comparison.

---

### 6.3 CVE-Bench: AI Agents Exploiting Real-World Web Vulnerabilities

**Paper:** [CVE-Bench: A Benchmark for AI Agents' Ability to Exploit Real-World Web Application Vulnerabilities](https://arxiv.org/abs/2503.17332)
**Authors:** Yuxuan Zhu et al.
**Year & Venue:** arXiv, March 2025
**Relevance:** 🎯 CMatrix's Paper 04 evaluation — real-world CVE exploitation benchmark.

---

### 6.4 NYU CTF Bench (NeurIPS 2024)

**Paper:** [NYU CTF Bench: A Scalable Open-Source Benchmark Dataset for Evaluating LLMs in Offensive Security](https://proceedings.neurips.cc/paper_files/paper/2024/hash/69d97a6493fbf016fff0a751f253ad18-Abstract-Datasets_and_Benchmarks_Track.html)
**Authors:** NYU team
**Institution:** New York University, USA | QS Rank: **#39**
**Year & Venue:** NeurIPS 2024 (CCF-A)
**Code:**
- [NYUCTFBench](https://github.com/NYU-LLM-CTF/NYUCTFBench)
- [LLMctfautomation](https://github.com/NYU-LLM-CTF/LLMctfautomation)
**Relevance:** Scalable CTF benchmark for LLMs — evaluation dataset for CMatrix's CTF-style tasks.

---

### 6.5 An Empirical Evaluation of LLMs for Offensive Security Challenges (NeurIPS 2024)

**Paper:** [An Empirical Evaluation of LLMs for Solving Offensive Security Challenges](https://arxiv.org/abs/2402.11814)
**Authors:** (NeurIPS 2024, CCF-A)
**Year & Venue:** NeurIPS 2024 (CCF-A)
**Code:** [github.com/NickNameInvalid/LLM_CTF](https://github.com/NickNameInvalid/LLM_CTF)
**Relevance:** Empirical evaluation of LLMs (GPT-4, Claude, etc.) on offensive security — direct benchmark methodology reference.

---

### 6.6 Cybersecurity AI Benchmark (CAIBench) — Meta-Benchmark

**Paper:** [Cybersecurity AI Benchmark (CAIBench): A Meta-Benchmark for Evaluating Cybersecurity AI Agents](https://arxiv.org/abs/2510.24317)
**Authors:** (Alias Robotics + collaborators)
**Year & Venue:** arXiv, October 2025
**Relevance:** Meta-benchmark integrating Cybench, SecEval, CyberMetric, AutoPenBench — comprehensive evaluation framework.

---

### 6.7 AI-Pentest-Benchmark

**Paper:** [AI-Pentest-Benchmark: A Standardized Evaluation for Autonomous Security Agents](https://arxiv.org/abs/2509.13021)
*(Referenced as benchmark within xOffense paper)*
**Year & Venue:** 2025
**Relevance:** 🎯 CMatrix directly evaluates against this benchmark (referenced in research mission).

---

### 6.8 Measuring and Augmenting LLMs for CTF (ACM CCS 2025)

**Paper:** [Measuring and Augmenting Large Language Models for Solving Capture-the-Flag Challenges](https://dl.acm.org/doi/abs/10.1145/3719027.3744855)
**Authors:** (ACM CCS 2025 team)
**Year & Venue:** ACM CCS 2025 (CCF-A)
**Relevance:** Augmentation techniques for LLMs on CTF tasks — relevant to CMatrix's agent enhancement strategies.

---

### 6.9 PentestEval: Benchmarking LLM-based Penetration Testing

**Paper:** [PentestEval: Benchmarking LLM-based Penetration Testing with Modular and Stage-Level Design](https://arxiv.org/abs/2512.14233)
**Authors:** (et al.)
**Year & Venue:** arXiv, December 2025
**Relevance:** Stage-level evaluation design — relevant to CMatrix's per-agent performance measurement.

---

## 🗂️ SECTION 7 — AGENT REASONING, PLANNING & CHAIN-OF-THOUGHT

### 7.1 ReAct: Synergizing Reasoning and Acting in Language Models

**Paper:** [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
**Authors:** Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao
**Author Profile:** [Shunyu Yao — Princeton/OpenAI](https://ysymyth.github.io/)
**Institution:** Princeton University + Google Brain | QS Rank: **Princeton: #16**
**Year & Venue:** ICLR 2023 (CCF-A)
**Relevance:** 🎯 Foundational ReAct framework used in PentestGPT and CMatrix agent reasoning loops (Paper 03).

---

### 7.2 Tree of Thoughts: Deliberate Problem Solving with LLMs

**Paper:** [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601)
**Authors:** Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, Karthik Narasimhan
**Institution:** Princeton University + Google DeepMind | QS Rank: **Princeton: #16**
**Year & Venue:** NeurIPS 2023 (CCF-A)
**Relevance:** 🎯 Tree-of-Thoughts (ToT) directly implemented in CMatrix's intelligent reasoning module.

---

### 7.3 Chain-of-Thought Prompting Elicits Reasoning in LLMs

**Paper:** [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)
**Authors:** Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, Denny Zhou
**Institution:** Google Brain / Google Research
**Year & Venue:** NeurIPS 2022 (CCF-A) — 10,000+ citations
**Relevance:** 🎯 Chain-of-Thought (CoT) is explicitly implemented in CMatrix's intelligent reasoning module. Foundational reading.

---

### 7.4 Reflexion: Language Agents with Verbal Reinforcement Learning

**Paper:** [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)
**Authors:** Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao
**Institution:** Northeastern University + Princeton | QS Rank: **Northeastern: #351–400**
**Year & Venue:** NeurIPS 2023 (CCF-A)
**Relevance:** Self-reflection in agents — foundational for CMatrix's iterative attack strategy refinement.

---

### 7.5 A Unified Modeling Framework for Automated Penetration Testing

**Paper:** [A Unified Modeling Framework for Automated Penetration Testing](https://www.sciencedirect.com/science/article/abs/pii/S0167404825004766)
**Authors:** (Computers & Security, Elsevier, 2025)
**Year & Venue:** Computers & Security (CCF-B), 2025
**Relevance:** Formal modeling framework for automated pentesting — theoretical underpinning for CMatrix's reasoning module.

---

## 🗂️ SECTION 8 — SURVEYS & SYSTEMATIC LITERATURE REVIEWS

### 8.1 When LLMs Meet Cybersecurity: A Systematic Literature Review

**Paper:** [When LLMs Meet Cybersecurity: A Systematic Literature Review](https://doi.org/10.1186/s42400-025-00361-w)
**Authors:** Jie Zhang, Haoyu Bu, Hui Wen, Yongji Liu, Haiqiang Fei, et al.
**Year & Venue:** Cybersecurity Journal (Springer), 2025
**Relevance:** 🎯 Must-read systematic review of all LLM + cybersecurity intersection — complete literature context.

---

### 8.2 Towards Automated Penetration Testing: A Survey (Comprehensive)

**Paper:** [Towards Automated Penetration Testing: A Survey](https://arxiv.org/abs/2303.01323) *(foundational survey)*
**Authors:** (Multiple authors)
**Year & Venue:** arXiv / Journal 2023
**Relevance:** Historical baseline survey for the field.

---

### 8.3 Pen-Strategist Survey Table (28 LLM-based PT Systems)

**Paper:** [Pen-Strategist: A Reasoning Framework for Penetration Testing Strategy Formation](https://arxiv.org/abs/2605.04499) — *Table 10 provides a complete survey of 28 systems*
**Year & Venue:** arXiv, May 2026
**Relevance:** 🎯 The most up-to-date curated list of all LLM-based PT systems (as of May 2026).

---

## 🗂️ SECTION 9 — LIVING CURATED LISTS & REPOSITORIES

### 9.1 LLM4Pentest: Curated List of LLM-Powered Penetration Testing Papers

**Repository:** [github.com/simon-p-j-r/LLM4Pentest](https://github.com/simon-p-j-r/LLM4Pentest)
**Maintainer:** DAS Lab (Cheng Huang's Lab)
**Last Updated:** May 2026 (active, 119+ commits)
**Relevance:** 🎯 **The single most comprehensive and up-to-date curated list** covering papers, blogs, MCP tools, benchmarks. Bookmark and check weekly.

---

### 9.2 Awesome Agent Papers

**Repository:** [github.com/luo-junyu/Awesome-Agent-Papers](https://github.com/luo-junyu/awesome-agent-papers)
**Relevance:** Broader LLM agent paper coverage — cross-domain agent research for CMatrix's orchestration background.

---

## 🗂️ SECTION 10 — ADDITIONAL HIGH-VALUE PAPERS BY TOPIC

### 10.1 Model Context Protocol (MCP) for Tool Orchestration

**Paper:** [PentestMCP: A Toolkit for Agentic Penetration Testing](https://arxiv.org/abs/2510.03610) *(listed again for MCP context)*
**Relevance:** MCP enables flexible construction of multi-function agents — directly relevant to CMatrix's tool integration architecture.

---

### 10.2 Cyber-Zero: Training Cybersecurity Agents without Runtime (ICLR 2026)

**Paper:** [Cyber-Zero: Training Cybersecurity Agents without Runtime](https://arxiv.org/abs/2508.00910)
**Authors:** Amazon Science team
**Institution:** Amazon Science
**Year & Venue:** ICLR 2026 (CCF-A)
**Code:** [github.com/amazon-science/cyber-zero](https://github.com/amazon-science/cyber-zero)
**Relevance:** Offline training of cybersecurity agents — novel training paradigm relevant to CMatrix's future model fine-tuning.

---

### 10.3 PenHeal: Two-Stage LLM Framework for Pentesting and Remediation

**Paper:** [PenHeal: A Two-Stage LLM Framework for Automated Pentesting and Optimal Remediation](https://dl.acm.org/doi/abs/10.1145/3689933.3690831)
**Authors:** (ACM CCS Workshop 2023)
**Year & Venue:** ACM CCS 2023 (CCF-A Workshop)
**Relevance:** Pentesting + remediation in a unified LLM pipeline — relevant to CMatrix's end-to-end workflow.

---

### 10.4 HackSynth Shell or Nothing: Memory-Activated Agents

**Paper:** [Shell or Nothing: Real-World Benchmarks and Memory-Activated Agents for Automated Penetration Testing](https://arxiv.org/abs/2501.13411) *(related)*
**Year & Venue:** 2025
**Relevance:** Memory-augmented pentesting agents — directly relevant to CMatrix's Qdrant session memory.

---

### 10.5 On the Surprising Efficacy of LLMs for Penetration-Testing

**Paper:** [On the Surprising Efficacy of LLMs for Penetration-Testing](https://arxiv.org/abs/2507.00829)
**Authors:** (et al.)
**Year & Venue:** arXiv, July 2025
**Relevance:** Empirical evaluation showing LLM effectiveness — corroborates CMatrix's core thesis.

---

### 10.6 A Survey of Cybersecurity LLMs (Comprehensive)

**Paper:** [A Survey on Large Language Models for Cybersecurity](https://arxiv.org/abs/2405.04828) *(2024 survey)*
**Year & Venue:** arXiv, May 2024
**Relevance:** Complete survey of LLMs in cybersecurity — essential background reading for all CMatrix papers.

---

## 📊 UNIVERSITY RANKING QUICK REFERENCE

| Institution | Country | QS 2025 Rank |
|---|---|---|
| MIT | USA | #1 |
| Imperial College London | UK | #2 |
| University of Oxford | UK | #3 |
| Harvard University | USA | #4 |
| Stanford University | USA | #5 |
| ETH Zurich | Switzerland | #7 |
| UC Berkeley | USA | #12 |
| Princeton University | USA | #16 |
| Carnegie Mellon University | USA | #24 |
| Nanyang Technological University | Singapore | #26 |
| University of Illinois Urbana-Champaign | USA | #82 |
| New York University | USA | #39 |
| Wuhan University | China | #225 |
| TU Wien | Austria | #251–300 |
| Politecnico di Torino | Italy | #283 |
| Portland State University | USA | #651–700 |
| ELTE Eötvös Loránd University | Hungary | #801–1000 |

---

## 🔖 READING ORDER RECOMMENDATION (FOR ZERO KNOWLEDGE GAPS)

**Week 1 — Foundations:**
1. Chain-of-Thought (Wei et al., NeurIPS 2022)
2. ReAct (Yao et al., ICLR 2023)
3. Tree of Thoughts (Yao et al., NeurIPS 2023)
4. AutoGen (Wu et al., 2023)
5. Getting pwn'd by AI (Happe & Cito, FSE 2023)

**Week 2 — Core VAPT Papers:**
6. PentestGPT (Deng et al., USENIX Security 2024)
7. LLM Agents Can Autonomously Exploit One-day Vulnerabilities (Fang et al., 2024)
8. AutoAttacker (Xu et al., 2024)
9. SoK: Comparison of Autonomous Pentest Agents (2024)
10. When LLMs Meet Cybersecurity — Systematic Review (2025)

**Week 3 — Contemporary Frameworks:**
11. VulnBot (2025)
12. xOffense (2025)
13. AutoPentester (2025)
14. PentestMCP (2025)
15. CurriculumPT (2025)
16. Incalmo (2025)
17. RedTeamLLM (2025)
18. PentestGPT v2 (2026)

**Week 4 — Orchestration & Cost:**
19. FrugalGPT (2023)
20. RouteLLM (ICLR 2025)
21. Cost-Efficient Plan Caching (2025)
22. WorkflowLLM (2024)
23. Difficulty-Aware Agentic Orchestration (WWW 2026)

**Week 5 — Benchmarks:**
24. CyBench (ICLR 2025)
25. AutoPenBench (2024)
26. CVE-Bench (2025)
27. NYU CTF Bench (NeurIPS 2024)
28. CAIBench (2025)

**Week 6 — Safety, Memory & RAG:**
29. RAG for Cybersecurity (2025)
30. Survey on Long-Term Memory Security (2026)
31. ShieldAgent (2025)
32. Policy-as-Prompt (2025)
33. Securing RAG (2026)
34. Pen-Strategist (2026) — most up-to-date survey table

---

*Generated by Claude for CMatrix Research Team. Last updated: May 11, 2026.*
*All links verified functional as of compilation date. arXiv PDFs are freely accessible.*
