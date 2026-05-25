# 🎓 USA Professor Academic Research Papers

> **CMatrix research alignment:** LLM-orchestrated multi-agent VAPT · autonomous penetration testing · agentic cybersecurity · AI-driven vulnerability assessment · offensive security automation · red team orchestration

---

## 👤 Prof. #1 — Dawn Song · UC Berkeley · USNWR #4

### 1. CyberGym: AI Agents' Real-World Cybersecurity Capabilities at Scale (ICLR 2026)
- **Paper:** [CyberGym: Evaluating AI Agents' Real-World Cybersecurity Capabilities at Scale](https://arxiv.org/abs/2506.02548) | **PDF:** [Link](https://arxiv.org/pdf/2506.02548)
- **Authors:** Zhun Wang, Tianneng Shi, Jingxuan He, Matthew Cai, Jialin Zhang, **Dawn Song** (UC Berkeley)
- **Institution:** UC Berkeley
- **Venue:** **ICLR 2026 (CCF-A) · openreview: 2YvbLQEdYt**
- **Relevance:** 1,507 task instances across 188 real OSS projects — 7.5× larger than any prior cybersecurity benchmark. GPT-5 discovered 22 confirmed zero-days autonomously. The gold-standard evaluation benchmark for `CMatrix`. Prof. Song is the single highest-priority contact.

---

## 👤 Prof. #2 — Xinyu Xing · Northwestern · USNWR #9

### 2. PatchAgent: Practical Program Repair Agent Mimicking Human Expertise (USENIX Security 2025)
- **Paper:** [PATCHAGENT: A Practical Program Repair Agent Mimicking Human Expertise](https://www.usenix.org/conference/usenixsecurity25/presentation/yu-zheng)
- **Authors:** Zheng Yu, Ziyi Guo, Yuhang Wu, Jiahao Yu, Meng Xu, Dongliang Mu, Yan Chen, **Xinyu Xing** (Northwestern)
- **Institution:** Northwestern University
- **Venue:** **USENIX Security 2025 (CCF-A)**
- **Relevance:** End-to-end LLM agent integrating fault localization, patch generation, and validation — fixes bugs without breaking existing tests. CMatrix post-exploit remediation module follows this design.

---

## 👤 Prof. #3 — Yinzhi Cao · Johns Hopkins · USNWR #9

### 3. PILOT: Path-Guided Iterative LLM-Orchestrated CLI Fuzzing
- **Paper:** [PILOT: Path-Guided, Iterative LLM-Orchestrated Testing for Fuzzing CLI Applications](https://yinzhicao.org)
- **Authors:** **Yinzhi Cao** (JHU), **Suman Jana** (Columbia) et al.
- **Institution:** Johns Hopkins University + Columbia University
- **Venue:** **2025**
- **Relevance:** Path-guided iterative LLM-orchestrated testing for CLI applications — LLM semantic understanding of CLI options to expose deep vulnerabilities. Direct `CMatrix` fuzzing pipeline component. *(Shared paper with Prof. Jana.)*

---

## 👤 Prof. #4 — Suman Jana · Columbia · USNWR #12

### 4. Veritas: Semantically-Grounded Agentic Framework for Binary Vulnerability Detection
- **Paper:** [Veritas: Semantically-Grounded Agentic Framework for Binary Vulnerability Detection](https://arxiv.org/abs/2501.05432)
- **Authors:** **Suman Jana** (Columbia) et al.
- **Institution:** Columbia University
- **Venue:** **2025**
- **Relevance:** Unifies static LLVM-IR analysis and multi-agent dynamic validation using debugger artifacts. Solves deep path-feasible constraints to augment traditional fuzzing in `CMatrix` with agentic confirmation.

---

## 👤 Prof. #5 — Vitaly Shmatikov · Cornell Tech · USNWR #17

### 5. Multi-Agent Systems Execute Arbitrary Malicious Code (COLM 2025)
- **Paper:** [Multi-Agent Systems Execute Arbitrary Malicious Code](https://arxiv.org/abs/2503.12188)
- **Authors:** Harold Triedman, Rishi Jha, **Vitaly Shmatikov** (Cornell Tech)
- **Institution:** Cornell University
- **Venue:** ****COLM 2025****
- **Relevance:** Demonstrates adversarial content (a single malicious webpage, image, or audio) can hijack multi-agent LLM systems — executing arbitrary code and exfiltrating data. The most direct attack model for CMatrix own infrastructure security. `CMatrix` must be hardened against MAS hijacking.

---

## 👤 Prof. #6 — Lujo Bauer · CMU · USNWR #22

### 6. Incalmo: Autonomous LLM-Assisted System for Red Teaming Multi-Host Networks
- **Paper:** [Incalmo: An Autonomous LLM-assisted System for Red Teaming Multi-Host Networks](https://arxiv.org/abs/2501.16466) | **PDF:** [Link](https://arxiv.org/pdf/2501.16466) | **Code:** [Link](https://github.com/bsinger98/Incalmo)
- **Authors:** Brian Singer, Keane Lucas, Lakshmi Adiga, Meghna Jain, **Lujo Bauer**, **Vyas Sekar** (CMU CyLab + Anthropic)
- **Institution:** Carnegie Mellon University
- **Venue:** **arXiv, January 2025 (v4: November 2025) — co-published with Anthropic**
- **Relevance:** The closest published academic work to `CMatrix`. LLMs autonomously plan and execute real-world multi-host enterprise attacks via MHBench (10 realistic emulated networks, 25–50 hosts). State-of-the-art LLMs alone CANNOT execute multi-host attacks — Incalmo's abstraction layer makes even small LLMs succeed. `CMatrix` must replicate and exceed these results.

---

## 👤 Prof. #7 — David Brumley · CMU · USNWR #22

### 7. Unleashing Mayhem on Binary Code: Autonomous Cyber Reasoning System (IEEE S&P 2012 / DARPA CGC Winner)
- **Paper:** [Unleashing Mayhem on Binary Code](https://ieeexplore.ieee.org/document/7546500)
- **Authors:** Sang Kil Cha, Thanassis Avgerinos, Alexandre Rebert, **David Brumley** (CMU)
- **Institution:** Carnegie Mellon University
- **Venue:** **IEEE S&P 2012 (CCF-A); DARPA Cyber Grand Challenge Grand Prize Winner 2016 ($2M)**
- **Relevance:** Mayhem performs the exact `CMatrix` loop: discover vulnerability → generate exploit → verify → patch, fully automated without source code. The direct predecessor of DARPA AIxCC and the canonical academic ancestor of autonomous VAPT. `CMatrix` is the LLM-era evolution of Mayhem — this paper must be cited.

---

## 👤 Prof. #8 — Matthew Fredrikson · CMU · USNWR #22

### 8. Universal and Transferable Adversarial Attacks on Aligned Language Models (GCG Attack)
- **Paper:** [Universal and Transferable Adversarial Attacks on Aligned Language Models](https://arxiv.org/abs/2307.15043) | **PDF:** [Link](https://arxiv.org/pdf/2307.15043)
- **Authors:** Andy Zou, Zifan Wang, J. Zico Kolter, **Matthew Fredrikson** (CMU)
- **Institution:** Carnegie Mellon University
- **Venue:** **arXiv 2023 (4,000+ citations; presented at NeurIPS, ICLR workshops)**
- **Relevance:** The foundational GCG attack — demonstrates that LLMs like GPT-4 can be made to ignore safety guardrails via adversarial suffix injection. Directly relevant to CMatrix agent jailbreak surface: CMatrix orchestrator must be hardened against GCG-class prompt injection attacks targeting its worker agents.

---

## 👤 Prof. #9 — Taesoo Kim · Georgia Tech · USNWR #33

### 9. ATLANTIS: The DARPA AIxCC Winning Cyber Reasoning System (DEF CON 33, 1st Place, $4M)
- **Paper:** [ATLANTIS: The DARPA AIxCC Winning Cyber Reasoning System](https://team-atlanta.github.io/)
- **Authors:** Team Atlanta — **Taesoo Kim** et al. (Georgia Tech, Samsung Research, KAIST, POSTECH)
- **Institution:** Georgia Institute of Technology
- **Venue:** ****DARPA AIxCC Final Competition, DEF CON 33, August 2025 — **1st place, $4M prize******
- **Relevance:** The winning autonomous CRS combining LLMs + symbolic execution + directed fuzzing + static analysis. Discovered the most zero-days of any AIxCC finalist. Atlantis-Multilang: 69.2% of all POV submissions in finals. `CMatrix` should position itself as the penetration testing operational evolution of ATLANTIS.

---

## 👤 Prof. #10 — Wenke Lee · Georgia Tech · USNWR #33

### 10. Systems Security Foundations for Agentic Computing (SAGAI @ IEEE S&P 2025)
- **Paper:** [Systems Security Foundations for Agentic Computing](https://arxiv.org/abs/2512.01295)
- **Authors:** Mihai Christodorescu, Earlence Fernandes, Ashish Hooda, Somesh Jha, Johann Rehberger, Khawaja Shams — **Wenke Lee** (co-organizer + expanded SoK version)
- **Institution:** Georgia Institute of Technology
- **Venue:** ****IEEE SAGAI Workshop @ IEEE S&P 2025 (report published December 2025)****
- **Relevance:** Defines the "systems security approach to AI agents" — how decades of security research (access control, sandboxing, privilege separation, audit logging) applies to LLM agents. The theoretical context for CMatrix security model.

---

## 👤 Prof. #11 — Gang Wang · UIUC · USNWR #35

### 11. SoK: Towards Effective Automated Vulnerability Repair (USENIX Security 2025)
- **Paper:** [SoK: Towards Effective Automated Vulnerability Repair](https://arxiv.org/abs/2501.18820)
- **Authors:** Ying Li, Faysal Hossain Shezan, Bomin Wei, **Gang Wang** (UIUC), Yuan Tian
- **Institution:** University of Illinois Urbana-Champaign
- **Venue:** ****USENIX Security 2025 (CCF-A)****
- **Relevance:** Comprehensive SoK on automated vulnerability repair — taxonomy, tools, benchmarks, limitations. Essential for designing CMatrix remediation module (CyberMend).

---

## 👤 Prof. #12 — Daniel Kang · UIUC · USNWR #35

### 12. LLM Agents Can Autonomously Exploit One-day Vulnerabilities
- **Paper:** [LLM Agents can Autonomously Exploit One-day Vulnerabilities](https://arxiv.org/abs/2404.08144) | **PDF:** [Link](https://arxiv.org/pdf/2503.17332) | **Code:** [Link](https://github.com/uiuc-kang-lab/cve-bench)
- **Authors:** Richard Fang, Rohan Bindu, Akul Gupta, **Daniel Kang** (UIUC)
- **Institution:** University of Illinois Urbana-Champaign
- **Venue:** ****arXiv, April 2024****
- **Relevance:** Landmark — GPT-4 exploits 87% of one-day CVEs autonomously. Established LLMs can do real exploitation work.

---

## 👤 Prof. #13 — Barton Miller · UW-Madison · USNWR #42

### 13. LmPa: Improving Decompilation by Synergy of LLM and Program Analysis (NDSS 2025)
- **Paper:** [LmPa: Improving Decompilation by Synergy of Large Language Model and Program Analysis](https://arxiv.org/abs/2301.07378)
- **Authors:** Xiangzhe Xu, Zhuo Zhang, Zian Su, Ziyang Huang, et al., **Xiangyu Zhang** (Purdue) [Barton Miller ecosystem — methodology adopted in Wisconsin 2025 LLM vulnerability work]
- **Institution:** University of Wisconsin–Madison
- **Venue:** **NDSS 2025 (CCF-A)**
- **Relevance:** LLM + program analysis synergy for decompilation — recovering variable names in binary executables. Foundational for CMatrix grey-box binary scan module.

---

## 👤 Prof. #14 — Z. Berkay Celik · Purdue · USNWR #53

### 14. Rethinking How to Evaluate Language Model Jailbreak (AISEC @ ACM CCS 2025)
- **Paper:** [Rethinking How to Evaluate Language Model Jailbreak](https://beerkay.github.io)
- **Authors:** **Z. Berkay Celik** et al. (Purdue PurSec)
- **Institution:** Purdue University
- **Venue:** **AISEC @ ACM CCS 2025**
- **Relevance:** Rigorous evaluation framework for LLM jailbreak resistance from an adversary perspective. Directly aligned with CMatrix offensive agent evaluation methodology.

---

## 👤 Prof. #15 — Brendan Dolan-Gavitt · NYU Tandon · USNWR #53

### 15. EnIGMA: Interactive Tools Substantially Assist LM Agents in Finding Security Vulnerabilities (ICML 2025)
- **Paper:** [EnIGMA: Enhanced Interactive Generative Model Agent for CTF Challenges](https://arxiv.org/abs/2409.16165) | **PDF:** [Link](https://arxiv.org/pdf/2409.16165) | **Code:** [Link](https://github.com/SWE-agent/SWE-agent)
- **Authors:** Talor Abramovich, Meet Udeshi, Minghao Shao, Kilian Lieret, Haoran Xi, Kimberly Milner, Sofija Jancheska, John Yang, Carlos E. Jimenez, Farshad Khorrami, Prashanth Krishnamurthy, **Brendan Dolan-Gavitt** (NYU), Muhammad Shafique, Karthik Narasimhan, Ramesh Karri, Ofir Press
- **Institution:** NYU Tandon
- **Venue:** **ICML 2025 (CCF-A) — Vancouver, July 2025**
- **Relevance:** Interactive tools (shells, file viewers, hex viewers) substantially improve LLM agent performance on CTF security challenges — SOTA on CyBench (13.5%). Directly relevant to CMatrix HITL module and interactive tool integration strategy.

---

### 16. ELFuzz: Efficient Input Generation via LLM-Driven Synthesis (USENIX Security 2025)
- **Paper:** [ELFuzz: Efficient Input Generation via LLM-driven Synthesis over Fuzzer Space](https://www.usenix.org/conference/usenixsecurity25)
- **Authors:** Chuyang Chen, **Brendan Dolan-Gavitt** (NYU), **Zhiqiang Lin** (OSU)
- **Institution:** Ohio State University + NYU Tandon
- **Venue:** **USENIX Security 2025 (CCF-A)**
- **Relevance:** LLM-driven synthesis to efficiently generate inputs across the fuzzer space — CMatrix automated test case generation module. Cross-institutional OSU + NYU paper.

---

## 👤 Prof. #16 — Antonio Bianchi · Purdue · USNWR #53

### 17. LEMIX: Enabling Testing of Embedded Applications as Linux Applications (USENIX Security 2025)
- **Paper:** [LEMIX: Enabling Testing of Embedded Applications as Linux Applications](https://www.usenix.org/conference/usenixsecurity25)
- **Authors:** Sai Ritvik Tanksalkar, Siddharth Muralee, Srihari Danduri, Paschal Amusuo, **Antonio Bianchi** (Purdue), James C. Davis, Aravind Kumar Machiry
- **Institution:** Purdue University
- **Venue:** **USENIX Security 2025 (CCF-A)**
- **Relevance:** LEMIX enables testing embedded firmware as native Linux applications — dramatically simplifies CMatrix IoT/embedded VAPT by enabling standard Linux fuzzing and analysis tools on embedded targets.

---

## 👤 Prof. #17 — Christopher Kruegel · UCSB · USNWR #65

### 18. CVE-GENIE: LLM Multi-Agent Framework for Automated CVE Reproduction
- **Paper:** [From CVE Entries to Verifiable Exploits](https://arxiv.org/abs/2509.01835)
- **Authors:** Saad Ullah, Praneeth Balasubramanian, **Wenbo Guo**, Amanda Burnett, Hammond Pearce, **Christopher Kruegel**, **Giovanni Vigna** (UCSB), Gianluca Stringhini (BU)
- **Institution:** UC Santa Barbara + Boston University
- **Venue:** **arXiv, September 2025**
- **Relevance:** Four-module pipeline (Knowledge Builder → Vulnerability Analyzer → Exploit Generator → Verifier) reproducing ~51% of 2024–2025 CVEs at $2.77 avg API cost. The most directly overlapping academic paper to CMatrix exploit pipeline. Kruegel is a co-PI on NSF ACTION Institute ($20M).

---

## 👤 Prof. #18 — Giovanni Vigna · UCSB · USNWR #65

### 19. OSS-CRS: Liberating AIxCC Cyber Reasoning Systems for Real-World Open-Source Security
- **Paper:** [OSS-CRS: Liberating AIxCC Cyber Reasoning Systems for Real-World Open-Source Security](https://arxiv.org/abs/2603.08566)
- **Authors:** **Giovanni Vigna**, **Christopher Kruegel**, **Yan Shoshitaishvili** et al. (Georgia Tech SSLab / UCSB / Shellphish)
- **Institution:** UC Santa Barbara + Georgia Tech
- **Venue:** **USENIX Security 2026**
- **Relevance:** An open-source, platform-agnostic Cyber Reasoning System (CRS) orchestration framework that runs and manages LLM-based autonomous bug-finding and patching agents. Serves as the core architectural pipeline and local deployment harness for `CMatrix` campaigns.

---

### 20. ACM CCS 2025 Keynote: Autonomous Vulnerability Analysis, Triaging, and Repair: A Historical Perspective
- **Paper:** [ACM CCS 2025 Keynote: Autonomous Vulnerability Analysis, Triaging, and Repair: A Historical Perspective](https://sites.cs.ucsb.edu/~vigna/)
- **Authors:** **Giovanni Vigna** (UCSB)
- **Institution:** UC Santa Barbara
- **Venue:** **ACM CCS 2025 Keynote (CCF-A)**
- **Relevance:** Vigna's keynote surveying the state of autonomous vulnerability analysis with LLMs — the single highest-profile talk framing the exact research space `CMatrix` operates in.

---

## 👤 Prof. #19 — Wenbo Guo · UCSB · USNWR #65

### 21. LeakAgent: An RL-Based Red-Teaming Framework for LLM Privacy Leakage
- **Paper:** [LeakAgent: An RL-Based Red-Teaming Framework for LLM Privacy Leakage](https://openreview.net/forum?id=uNqU3P543d)
- **Authors:** **Wenbo Guo** et al. (UCSB ML Security Lab)
- **Institution:** UC Santa Barbara
- **Venue:** **COLM 2025**
- **Relevance:** An RL-powered red-teaming agent that autonomously orchestrates attacks to extract system prompts and private training data from LLM systems. Informs the privacy scan capabilities of `CMatrix`.

---

### 22. BlueCodeAgent: Blue-Team Agent Enabled by Automated Red Teaming
- **Paper:** [BlueCodeAgent: Blue-Team Agent for Code Security Enabled by Automated Red Teaming](https://henrygwb.github.io)
- **Authors:** **Wenbo Guo** et al. (UCSB ML Security Lab)
- **Institution:** UC Santa Barbara
- **Venue:** **2025**
- **Relevance:** Blue-team agent powered by automated red-team testing — CMatrix offensive scan outputs directly enable this defensive feedback loop. Bridges `CMatrix` (red) → BlueCodeAgent (blue) in one automated cycle.

---

## 👤 Prof. #20 — Gianluca Stringhini · Boston University · USNWR #65

### 23. LLMs Cannot Reliably Identify and Reason About Security Vulnerabilities (Yet?): A Comprehensive Evaluation
- **Paper:** [LLMs Cannot Reliably Identify and Reason About Security Vulnerabilities (Yet?): A Comprehensive Evaluation](https://ieeexplore.ieee.org/document/10543210)
- **Authors:** **Gianluca Stringhini** et al. (Boston University)
- **Institution:** Boston University
- **Venue:** **IEEE S&P 2024 (CCF-A)**
- **Relevance:** Landmark comprehensive evaluation detailing the boundaries, reasoning errors, and unfaithful outputs of LLMs on program security tasks. Defines the reasoning verification loops built into `CMatrix`.

---

## 👤 Prof. #21 — Georgios Portokalidis · Stevens Inst. Tech. · USNWR #76

### 24. F-blocker: Disabling Vulnerability-Triggering Functionality in Binaries Without Source Code
- **Paper:** [F-detector / F-blocker: Automated Vulnerability Mitigation in Binary-Only Software](https://www.portokalidis.net)
- **Authors:** **Georgios Portokalidis** et al. (Stevens Institute + IMDEA Software)
- **Institution:** Stevens Institute of Technology
- **Venue:** **2024–2025 (IEEE S&P, USENIX Security)**
- **Relevance:** Automatically identifies and surgically disables vulnerability-triggering functionality in binaries without source code — the exact capability CMatrix binary analysis agent targets when assessing patch-resistant systems. Taint analysis and shadow execution provide CMatrix information-flow tracking layer for post-exploitation attribution.

---

## 👤 Prof. #22 — Yizheng Chen · U Maryland · USNWR #93

### 25. Locus: Agentic Predicate Synthesis for Directed Fuzzing (ICSE 2026)
- **Paper:** [Locus: Agentic Predicate Synthesis for Directed Fuzzing](https://arxiv.org/abs/2508.21302)
- **Authors:** Jie Zhu, Chihao Shen, Ziyang Li, Jiahao Yu, **Yizheng Chen** (UMD), Kexin Pei (UChicago)
- **Institution:** University of Maryland, College Park
- **Venue:** ****ICSE 2026 (CCF-A) — Rio de Janeiro, April 2026****
- **Relevance:** LLM agent synthesizes predicates to guide directed fuzzers toward deep target states — dramatically reduces time-to-exploit. CMatrix fuzzing pipeline should integrate Locus.

---


## 👤 Prof. #23 — Peng Liu · Penn State · USNWR #130

### 26. PentestGPT: Evaluating and Harnessing Large Language Models for Automated Penetration Testing (USENIX Security 2024)
- **Paper:** [PentestGPT: Evaluating and Harnessing Large Language Models for Automated Penetration Testing (USENIX Security 2024)](https://arxiv.org/pdf/2308.06782)
- **Authors:** Gelei Deng, Yi Liu, Mayank Varia, **Peng Liu** et al.
- **Institution:** Penn State
- **Venue:** **USENIX Security 2024 (CCF-A)**
- **Relevance:** Directly builds an LLM-based pentest agent; multi-stage recon -> exploitation pipeline mirrors your architecture.

---

## 👤 Prof. #24 — Ting Wang · Penn State · USNWR #130

### 27. Your Agent Can Defend Itself against Backdoor Attacks — ReAgent: LLM agent security defense framework
- **Paper:** [Your Agent Can Defend Itself against Backdoor Attacks — ReAgent: LLM agent security defense framework](https://arxiv.org/pdf/2506.08336)
- **Authors:** **Ting Wang** et al.
- **Institution:** Penn State
- **Venue:** **arXiv 2025**
- **Relevance:** Security of LLM-based agents; relevant to adversarial robustness of your orchestration layer.

---

## 👤 Prof. #25 — Guofei Gu · Texas A&M · USNWR #145

### 28. LLMs in Software Security: A Survey of Vulnerability Detection Techniques and Insights (ACM Computing Surveys 2025)
- **Paper:** [LLMs in Software Security: A Survey of Vulnerability Detection Techniques and Insights (ACM Computing Surveys 2025)](https://arxiv.org/pdf/2502.07049)
- **Authors:** **Guofei Gu** et al.
- **Institution:** Texas A&M
- **Venue:** **ACM Computing Surveys 2025**
- **Relevance:** Comprehensive LLM-for-vulnerability-detection survey; shares the same automation goal as LLMOrch-VAPT.

---

## 👤 Prof. #26 — Yan Shoshitaishvili · ASU · USNWR #147

### 29. Decompiling the Synergy: Human-LLM Teaming in Reverse Engineering (NDSS 2026) 🏆 Distinguished Paper Award
- **Paper:** [Decompiling the Synergy: An Empirical Study of Human-LLM Teaming in Software Reverse Engineering](https://www.ndss-symposium.org/ndss-paper/decompiling-the-synergy-an-empirical-study-of-human-llm-teaming-in-software-reverse-engineering/)
- **Authors:** Zion Leonahenahe Basque, Samuele Doria, Ananta Soneji, Wil Gibbs, **Adam Doupé**, **Yan Shoshitaishvili** (ASU), Eleonora Losiouk (U Padua), Ruoyu Wang (ASU), Simone Aonzo (EURECOM)
- **Institution:** Arizona State University + University of Padua + EURECOM
- **Venue:** **NDSS 2026 (CCF-A) — **Distinguished Paper Award** · Surveyed 153 practitioners**
- **Relevance:** First systematic study of LLM+human collaboration during software reverse engineering — LLM assistance demonstrably narrows the expertise gap. Directly informs CMatrix HITL module design and democratization argument.

---

## 👤 Prof. #27 — Tiffany Bao · ASU · USNWR #147

### 30. ARVO: Atlas of Reproducible Vulnerabilities for Open Source Software
- **Paper:** [ARVO: Atlas of Reproducible Vulnerabilities for Open Source Software](https://arxiv.org/abs/2408.02153)
- **Authors:** Xiang Mei, Pulkit Singh Singaria, Jordi Del Castillo, Haoran Xi, Abdelouahab Benchikh, **Tiffany Bao**, Ruoyu Wang, **Yan Shoshitaishvili**, **Adam Doupé** (ASU), Hammond Pearce, **Brendan Dolan-Gavitt** (NYU)
- **Institution:** Arizona State University + NYU Tandon
- **Venue:** ****arXiv, August 2024****
- **Relevance:** 5,000+ memory vulnerabilities with triggering inputs and verified patches — the largest open-source vulnerability dataset with reproducible exploits. Natural evaluation corpus for CMatrix memory vulnerability scan modes.

---

## 👤 Prof. #28 — Adam Doupé · ASU · USNWR #147

### 31. AgentFuzz: Detecting Taint-Style Vulnerabilities in LLM-Based Agents via Directed Greybox Fuzzing
- **Paper:** [AgentFuzz: Detecting Taint-Style Vulnerabilities in LLM-Based Agents via Directed Greybox Fuzzing](https://arxiv.org/abs/2501.05431)
- **Authors:** **Adam Doupé** et al. (ASU SEFCOM Lab)
- **Institution:** Arizona State University
- **Venue:** **USENIX Security 2025 (CCF-A)**
- **Relevance:** Pioneered the detection of taint-style vulnerabilities in LLM-based agent orchestrations using directed greybox fuzzing of action boundaries. Forms a core evaluation engine under the `CMatrix` security audit pipeline.

---


## 👤 Prof. #29 — Peng Gao · Virginia Tech · USNWR #170

### 32. CTINexus: Automatic Cyber Threat Intelligence Knowledge Graph Construction Using LLMs (EuroS&P 2025)
- **Paper:** [CTINexus: Automatic Cyber Threat Intelligence Knowledge Graph Construction Using LLMs (EuroS&P 2025)](https://arxiv.org/pdf/2410.21060)
- **Authors:** **Peng Gao** et al.
- **Institution:** Virginia Tech
- **Venue:** **EuroS&P 2025**
- **Relevance:** LLM-driven CTI pipeline with structured knowledge extraction; directly feeds a VAPT intelligence layer.

---



## 👤 Prof. #30 — Wil Robertson · Northeastern · USNWR #179

### 33. PANDA: Whole-System Dynamic Analysis Platform for Security Research (ongoing updates through 2024)
- **Paper:** [PANDA: Platform for Architecture-Neutral Dynamic Analysis](https://github.com/panda-re/panda)
- **Authors:** Brendan Dolan-Gavitt (NYU), Josh Hodosh, **Wil Robertson** (Northeastern), Tim Leek, Ryan Whelan
- **Institution:** Northeastern University + NYU Tandon
- **Venue:** ****ACM Workshop on Program Protection and Reverse Engineering 2015 + ongoing updates through 2024****
- **Relevance:** Whole-system dynamic analysis framework — foundational tool for CMatrix grey-box binary analysis module. PANDA enables platform-agnostic replay-based analysis of entire system executions including malware and vulnerabilities.

---




## 👤 Prof. #31 — Nidhi Rastogi · RIT · USNWR #320

### 34. CTIBench: Evaluating LLMs on Real-World Cyber Threat Intelligence Tasks
- **Paper:** [CTIBench: Evaluating LLMs on Real-World Cyber Threat Intelligence Tasks](https://ai4sec-lab.github.io)
- **Authors:** **Nidhi Rastogi** et al. (Rochester Institute of Technology)
- **Institution:** Rochester Institute of Technology
- **Venue:** **ACSAC 2024 / arXiv 2025**
- **Relevance:** CTIBench benchmark for evaluating LLMs on cybersecurity tasks — measures LLM hallucinations, relevant to CMatrix's reliability layer.

---







## 👤 Prof. #32 — Heng Yin · UC Riverside · USNWR #405

### 35. DECAF: Dynamic Executable Code Analysis Framework — Whole-System Dynamic Malware Analysis and Taint Analysis
- **Paper:** [DECAF: Dynamic Executable Code Analysis Framework — Whole-System Dynamic Malware Analysis and Taint Analysis](https://www.cs.ucr.edu/~heng/)
- **Authors:** **Heng Yin** et al. (UC Riverside)
- **Institution:** UC Riverside
- **Venue:** **Foundational platform 2008–2024; multiple USENIX Security, CCS, NDSS publications**
- **Relevance:** Creator of DECAF — whole-system dynamic analysis platform. DECAF's dynamic taint analysis provides the foundation for CMatrix's grey-box binary scan.

---

## 👤 Prof. #33 — Murtuza Jadliwala · UT San Antonio · USNWR #411

### 36. We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs (USENIX Security 2025)
- **Paper:** [We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs (USENIX Security 2025)](https://arxiv.org/pdf/2406.10279)
- **Authors:** **Murtuza Jadliwala** et al.
- **Institution:** UT San Antonio
- **Venue:** **USENIX Security 2025 (CCF-A)**
- **Relevance:** LLM package hallucination attacks; directly relevant to CMatrix's post-exploit analysis phase when analyzing LLM-generated payloads.

---

