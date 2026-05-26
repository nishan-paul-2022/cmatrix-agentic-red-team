# 🎓 USA Professor Academic Research Papers
> **Scope:** LLM-orchestrated multi-agent VAPT · autonomous penetration testing · agentic cybersecurity · AI-driven vulnerability assessment · offensive security automation · red team orchestration
---
## 1. Prof. Dawn Song
### 1. CyberGym: AI Agents' Real-World Cybersecurity Capabilities at Scale
- **Website:** [🌐 Link](https://arxiv.org/abs/2506.02548)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/01-cybergym-ai-agents-real-world-cybersecurity-capabilities-at-scale.pdf)
- **Code:** [GitHub](https://github.com/sunblaze-ucb/cybergym)
- **Authors:** Zhun Wang, Tianneng Shi, Jingxuan He, Matthew Cai, Jialin Zhang, **Dawn Song** (UC Berkeley)
- **Institution:** UC Berkeley (USNWR #4)
- **Venue:** **ICLR 2026 (CCF-A)**
- **Relevance:** 1,507 task instances across 188 real OSS projects — 7.5× larger than any prior cybersecurity benchmark. GPT-5 discovered 22 confirmed zero-days autonomously. The gold-standard evaluation benchmark for CMatrix. Prof. Song is the single highest-priority contact.
---
## 2. Prof. Xinyu Xing
### 2. PatchAgent: Practical Program Repair Agent Mimicking Human Expertise
- **Website:** [🌐 Link](https://www.usenix.org/conference/usenixsecurity25/presentation/yu-zheng)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/02-patchagent-practical-program-repair-agent-mimicking-human.pdf)
- **Code:** [GitHub](https://github.com/cla7aye15I4nd/PatchAgent)
- **Authors:** Zheng Yu, Ziyi Guo, Yuhang Wu, Jiahao Yu, Meng Xu, Dongliang Mu, Yan Chen, **Xinyu Xing** (Northwestern)
- **Institution:** Northwestern University (USNWR #9)
- **Venue:** **USENIX Security 2025 (CCF-A)**
- **Relevance:** End-to-end LLM agent integrating fault localization, patch generation, and validation — fixes bugs without breaking existing tests. CMatrix post-exploit remediation module follows this design.
---
## 3. Prof. Yinzhi Cao
### 3. Effective Command-line Interface Fuzzing with Path-Aware Large Language Model Orchestration
- **Website:** [🌐 Link](https://arxiv.org/abs/2511.20555)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/03-pilot-path-guided-iterative-llm-orchestrated-cli-fuzzing.pdf)
- **Code:** [GitHub](https://github.com/momo-trip/PILOT)
- **Authors:** Momoko Shiraishi (The University of Tokyo), **Yinzhi Cao** (Johns Hopkins University), Takahiro Shinagawa (The University of Tokyo)
- **Institution:** Johns Hopkins University (USNWR #9) + The University of Tokyo
- **Venue:** **IEEE S&P 2026 (CCF-A)**
- **Relevance:** Path-guided iterative LLM-orchestrated testing for CLI applications — LLM semantic understanding of CLI options to expose deep vulnerabilities. Direct CMatrix fuzzing pipeline component.
---
## 4. Prof. Suman Jana
### 4. Veritas: A Semantically Grounded Agentic Framework for Memory Corruption Vulnerability Detection in Binaries
- **Website:** [🌐 Link](https://arxiv.org/abs/2605.15097)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/04-veritas-semantically-grounded-agentic-framework-for.pdf)
- **Authors:** **Suman Jana** (Columbia) et al.
- **Institution:** Columbia University (USNWR #12)
- **Venue:** **arXiv 2026**
- **Relevance:** Unifies static LLVM-IR analysis and multi-agent dynamic validation using debugger artifacts. Solves deep path-feasible constraints to augment traditional fuzzing in CMatrix with agentic confirmation.
---
## 5. Prof. Vitaly Shmatikov
### 5. Multi-Agent Systems Execute Arbitrary Malicious Code
- **Website:** [🌐 Link](https://arxiv.org/abs/2503.12188)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/05-multi-agent-systems-execute-arbitrary-malicious-code.pdf)
- **Code:** [GitHub](https://github.com/trailofbits/pajaMAS)
- **Authors:** Harold Triedman, Rishi Jha, **Vitaly Shmatikov** (Cornell Tech)
- **Institution:** Cornell University (USNWR #17)
- **Venue:** **COLM 2025**
- **Relevance:** Demonstrates adversarial content (a single malicious webpage, image, or audio) can hijack multi-agent LLM systems — executing arbitrary code and exfiltrating data. The most direct attack model for CMatrix own infrastructure security. CMatrix must be hardened against MAS hijacking.
---
## 6. Prof. Lujo Bauer
### 6. Incalmo: Autonomous LLM-Assisted System for Red Teaming Multi-Host Networks
- **Website:** [🌐 Link](https://arxiv.org/abs/2501.16466)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/06-incalmo-autonomous-llm-assisted-system-for-red-teaming.pdf)
- **Code:** [GitHub](https://github.com/bsinger98/Incalmo)
- **Authors:** Brian Singer, Keane Lucas, Lakshmi Adiga, Meghna Jain, **Lujo Bauer**, **Vyas Sekar** (CMU CyLab + Anthropic)
- **Institution:** Carnegie Mellon University (USNWR #22)
- **Venue:** **arXiv, January 2025 (v4: November 2025) — co-published with Anthropic**
- **Relevance:** The closest published academic work to CMatrix. LLMs autonomously plan and execute real-world multi-host enterprise attacks via MHBench (10 realistic emulated networks, 25–50 hosts). State-of-the-art LLMs alone CANNOT execute multi-host attacks — Incalmo's abstraction layer makes even small LLMs succeed. CMatrix must replicate and exceed these results.
---
## 7. Prof. David Brumley
### 7. Unleashing Mayhem on Binary Code: Autonomous Cyber Reasoning System
- **Website:** [🌐 Link](https://ieeexplore.ieee.org/document/7546500)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/07-unleashing-mayhem-on-binary-code-autonomous-crs.pdf)
- **Authors:** Sang Kil Cha, Thanassis Avgerinos, Alexandre Rebert, **David Brumley** (CMU)
- **Institution:** Carnegie Mellon University (USNWR #22)
- **Venue:** **IEEE S&P 2012 (CCF-A); DARPA Cyber Grand Challenge Grand Prize Winner 2016 ($2M)**
- **Relevance:** Mayhem performs the exact CMatrix loop: discover vulnerability → generate exploit → verify → patch, fully automated without source code. The direct predecessor of DARPA AIxCC and the canonical academic ancestor of autonomous VAPT. CMatrix is the LLM-era evolution of Mayhem — this paper must be cited.
---
## 8. Prof. Matthew Fredrikson
### 8. Universal and Transferable Adversarial Attacks on Aligned Language Models (GCG Attack)
- **Website:** [🌐 Link](https://arxiv.org/abs/2307.15043)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/08-universal-and-transferable-adversarial-attacks-on-aligned.pdf)
- **Code:** [GitHub](https://github.com/llm-attacks/llm-attacks)
- **Authors:** Andy Zou, Zifan Wang, J. Zico Kolter, **Matthew Fredrikson** (CMU)
- **Institution:** Carnegie Mellon University (USNWR #22)
- **Venue:** **arXiv 2023 (4,000+ citations; presented at NeurIPS, ICLR workshops)**
- **Relevance:** The foundational GCG attack — demonstrates that LLMs like GPT-4 can be made to ignore safety guardrails via adversarial suffix injection. Directly relevant to CMatrix agent jailbreak surface: CMatrix orchestrator must be hardened against GCG-class prompt injection attacks targeting its worker agents.
---
## 9. Prof. Taesoo Kim
### 9. ATLANTIS: The DARPA AIxCC Winning Cyber Reasoning System
- **Website:** [🌐 Link](https://team-atlanta.github.io/)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/09-atlantis-the-darpa-aixcc-winning-cyber-reasoning-system.pdf)
- **Code:** [GitHub](https://github.com/Team-Atlanta/aixcc-afc-atlantis)
- **Authors:** Team Atlanta — **Taesoo Kim** et al. (Georgia Tech, Samsung Research, KAIST, POSTECH)
- **Institution:** Georgia Institute of Technology (USNWR #33)
- **Venue:** **DARPA AIxCC Final Competition, DEF CON 33, August 2025 — 1st place, $4M prize**
- **Relevance:** The winning autonomous CRS combining LLMs + symbolic execution + directed fuzzing + static analysis. Discovered the most zero-days of any AIxCC finalist. Atlantis-Multilang: 69.2% of all POV submissions in finals. CMatrix should position itself as the penetration testing operational evolution of ATLANTIS.
---
## 10. Prof. Wenke Lee
### 10. Systems Security Foundations for Agentic Computing
- **Website:** [🌐 Link](https://arxiv.org/abs/2512.01295)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/10-systems-security-foundations-for-agentic-computing.pdf)
- **Authors:** Mihai Christodorescu, Earlence Fernandes, Ashish Hooda, Somesh Jha, Johann Rehberger, Khawaja Shams — **Wenke Lee** (co-organizer + expanded SoK version)
- **Institution:** Georgia Institute of Technology (USNWR #33)
- **Venue:** **IEEE SAGAI Workshop @ IEEE S&P 2025 (report published December 2025)**
- **Relevance:** Defines the "systems security approach to AI agents" — how decades of security research (access control, sandboxing, privilege separation, audit logging) applies to LLM agents. The theoretical context for CMatrix security model.
---
## 11. Prof. Gang Wang
### 11. SoK: Towards Effective Automated Vulnerability Repair
- **Website:** [🌐 Link](https://arxiv.org/abs/2501.18820)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/11-sok-towards-effective-automated-vulnerability-repair.pdf)
- **Authors:** Ying Li, Faysal Hossain Shezan, Bomin Wei, **Gang Wang** (UIUC), Yuan Tian
- **Institution:** University of Illinois Urbana-Champaign (USNWR #35)
- **Venue:** **USENIX Security 2025 (CCF-A)**
- **Relevance:** Comprehensive SoK on automated vulnerability repair — taxonomy, tools, benchmarks, limitations. Essential for designing CMatrix remediation module (CyberMend).
---
## 12. Prof. Daniel Kang
### 12. LLM Agents Can Autonomously Exploit One-day Vulnerabilities
- **Website:** [🌐 Link](https://arxiv.org/abs/2404.08144)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/12-llm-agents-can-autonomously-exploit-one-day-vulnerabilities.pdf)
- **Code:** [GitHub](https://github.com/uiuc-kang-lab/cve-bench)
- **Authors:** Richard Fang, Rohan Bindu, Akul Gupta, **Daniel Kang** (UIUC)
- **Institution:** University of Illinois Urbana-Champaign (USNWR #35)
- **Venue:** **arXiv, April 2024**
- **Relevance:** Landmark — GPT-4 exploits 87% of one-day CVEs autonomously. Established LLMs can do real exploitation work.
---
## 13. Prof. Barton Miller
### 13. First Principles Vulnerability Assessment
- **Website:** [🌐 Link](https://www.cs.wisc.edu/mist/papers/VA.pdf)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/13-lmpa-improving-decompilation-by-synergy-of-llm-and-program.pdf)
- **Authors:** Elisa Heymann, **Barton P. Miller** (UW-Madison)
- **Institution:** University of Wisconsin–Madison (USNWR #42)
- **Venue:** **Foundational Methodology (MIST Project)**
- **Relevance:** Analyst-centric methodology focusing on architectural analysis, resource identification, and privilege separation. Informs the architectural design and attack surface mapping of CMatrix.
---
## 14. Prof. Z. Berkay Celik
### 14. Rethinking How to Evaluate Language Model Jailbreak
- **Website:** [🌐 Link](https://arxiv.org/abs/2404.06407)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/14-rethinking-how-to-evaluate-language-model-jailbreak.pdf)
- **Code:** [GitHub](https://github.com/controllability/jailbreak-evaluation)
- **Authors:** Hongyu Cai, Arjun Arunasalam, Leo Y. Lin, Antonio Bianchi, **Z. Berkay Celik** (Purdue)
- **Institution:** Purdue University (USNWR #53)
- **Venue:** **AISEC @ ACM CCS 2024 / arXiv 2024**
- **Relevance:** Rigorous evaluation framework for LLM jailbreak resistance from an adversary perspective. Directly aligned with CMatrix offensive agent evaluation methodology.
---
## 15. Prof. Brendan Dolan-Gavitt
### 15. EnIGMA: Interactive Tools Substantially Assist LM Agents in Finding Security Vulnerabilities
- **Website:** [🌐 Link](https://arxiv.org/abs/2409.16165)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/15-enigma-interactive-tools-substantially-assist-lm-agents-in.pdf)
- **Code:** [GitHub](https://github.com/swe-agent/swe-agent)
- **Authors:** Talor Abramovich, Meet Udeshi, Minghao Shao, Kilian Lieret, Haoran Xi, Kimberly Milner, Sofija Jancheska, John Yang, Carlos E. Jimenez, Farshad Khorrami, Prashanth Krishnamurthy, **Brendan Dolan-Gavitt** (NYU), Muhammad Shafique, Karthik Narasimhan, Ramesh Karri, Ofir Press
- **Institution:** NYU Tandon (USNWR #53)
- **Venue:** **ICML 2025 (CCF-A) — Vancouver, July 2025**
- **Relevance:** Interactive tools (shells, file viewers, hex viewers) substantially improve LLM agent performance on CTF security challenges — SOTA on CyBench (13.5%). Directly relevant to CMatrix HITL module and interactive tool integration strategy.
---
### 16. ELFuzz: Efficient Input Generation via LLM-Driven Synthesis
- **Website:** [🌐 Link](https://arxiv.org/abs/2506.10323)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/16-elfuzz-efficient-input-generation-via-llm-driven-synthesis.pdf)
- **Code:** [GitHub](https://github.com/OSUSecLab/elfuzz)
- **Authors:** Chuyang Chen, **Brendan Dolan-Gavitt** (NYU), **Zhiqiang Lin** (OSU)
- **Institution:** Ohio State University (USNWR #41) + NYU Tandon (USNWR #53)
- **Venue:** **USENIX Security 2025 (CCF-A)**
- **Relevance:** LLM-driven synthesis to efficiently generate inputs across the fuzzer space — CMatrix automated test case generation module. Cross-institutional OSU + NYU paper.
---
## 16. Prof. Antonio Bianchi
### 17. LEMIX: Enabling Testing of Embedded Applications as Linux Applications
- **Website:** [🌐 Link](https://arxiv.org/abs/2312.12575)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf)
- **Authors:** Sai Ritvik Tanksalkar, Siddharth Muralee, Srihari Danduri, Paschal Amusuo, **Antonio Bianchi** (Purdue), James C. Davis, Aravind Kumar Machiry
- **Institution:** Purdue University (USNWR #53)
- **Venue:** **USENIX Security 2025 (CCF-A)**
- **Relevance:** LEMIX enables testing embedded firmware as native Linux applications — dramatically simplifies CMatrix IoT/embedded VAPT by enabling standard Linux fuzzing and analysis tools on embedded targets.
---
## 17. Prof. Christopher Kruegel
### 18. CVE-GENIE: LLM Multi-Agent Framework for Automated CVE Reproduction
- **Website:** [🌐 Link](https://arxiv.org/abs/2509.01835)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/18-cve-genie-llm-multi-agent-framework-for-automated-cve.pdf)
- **Authors:** Saad Ullah, Praneeth Balasubramanian, **Wenbo Guo**, Amanda Burnett, Hammond Pearce, **Christopher Kruegel**, **Giovanni Vigna** (UCSB), Gianluca Stringhini (BU)
- **Institution:** UC Santa Barbara (USNWR #65) + Boston University (USNWR #65)
- **Venue:** **arXiv, September 2025**
- **Relevance:** Four-module pipeline (Knowledge Builder → Vulnerability Analyzer → Exploit Generator → Verifier) reproducing ~51% of 2024–2025 CVEs at $2.77 avg API cost. The most directly overlapping academic paper to CMatrix exploit pipeline. Kruegel is a co-PI on NSF ACTION Institute ($20M).
---
## 18. Prof. Giovanni Vigna
### 19. OSS-CRS: Liberating AIxCC Cyber Reasoning Systems for Real-World Open-Source Security
- **Website:** [🌐 Link](https://arxiv.org/abs/2603.08566)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf)
- **Code:** [GitHub](https://github.com/ossf/oss-crs)
- **Authors:** **Giovanni Vigna**, **Christopher Kruegel**, **Yan Shoshitaishvili** et al. (Georgia Tech SSLab / UCSB / Shellphish)
- **Institution:** UC Santa Barbara (USNWR #65) + Georgia Tech (USNWR #33)
- **Venue:** **USENIX Security 2026**
- **Relevance:** An open-source, platform-agnostic Cyber Reasoning System (CRS) orchestration framework that runs and manages LLM-based autonomous bug-finding and patching agents. Serves as the core architectural pipeline and local deployment harness for CMatrix campaigns.
---
### 20. ACM CCS 2025 Keynote: Autonomous Vulnerability Analysis, Triaging, and Repair: A Historical Perspective
- **Website:** [🌐 Link](https://sites.cs.ucsb.edu/~vigna/)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/20-acm-ccs-2025-keynote-autonomous-vulnerability-analysis.pdf)
- **Authors:** **Giovanni Vigna** (UCSB)
- **Institution:** UC Santa Barbara (USNWR #65)
- **Venue:** **ACM CCS 2025 Keynote (CCF-A)**
- **Relevance:** Vigna's keynote surveying the state of autonomous vulnerability analysis with LLMs — the single highest-profile talk framing the exact research space CMatrix operates in.
---
## 19. Prof. Wenbo Guo
### 21. LeakAgent: An RL-Based Red-Teaming Framework for LLM Privacy Leakage
- **Website:** [🌐 Link](https://openreview.net/forum?id=uNqU3P543d)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/21-leakagent-an-rl-based-red-teaming-framework-for-llm.pdf)
- **Code:** [GitHub](https://github.com/rucnyz/LeakAgent)
- **Authors:** **Wenbo Guo** et al. (UCSB ML Security Lab)
- **Institution:** UC Santa Barbara (USNWR #65)
- **Venue:** **COLM 2025**
- **Relevance:** An RL-powered red-teaming agent that autonomously orchestrates attacks to extract system prompts and private training data from LLM systems. Informs the privacy scan capabilities of CMatrix.
---
### 22. BlueCodeAgent: Blue-Team Agent Enabled by Automated Red Teaming
- **Website:** [🌐 Link](https://henrygwb.github.io)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/22-bluecodeagent-blue-team-agent-enabled-by-automated-red.pdf)
- **Authors:** **Wenbo Guo** et al. (UCSB ML Security Lab)
- **Institution:** UC Santa Barbara (USNWR #65)
- **Venue:** **arXiv (October 2025) / ICLR 2026 Workshop**
- **Relevance:** Blue-team agent powered by automated red-team testing — CMatrix offensive scan outputs directly enable this defensive feedback loop. Bridges CMatrix (red) → BlueCodeAgent (blue) in one automated cycle.
---
## 20. Prof. Gianluca Stringhini
### 23. LLMs Cannot Reliably Identify and Reason About Security Vulnerabilities (Yet?): A Comprehensive Evaluation
- **Website:** [🌐 Link](https://ieeexplore.ieee.org/document/10543210)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/23-llms-cannot-reliably-identify-and-reason-about-security.pdf)
- **Authors:** **Gianluca Stringhini** et al. (Boston University)
- **Institution:** Boston University (USNWR #65)
- **Venue:** **IEEE S&P 2024 (CCF-A)**
- **Relevance:** Landmark comprehensive evaluation detailing the boundaries, reasoning errors, and unfaithful outputs of LLMs on program security tasks. Defines the reasoning verification loops built into CMatrix.
---
## 21. Prof. Georgios Portokalidis
### 24. Eliminating Vulnerabilities by Disabling Unwanted Functionality in Binary Programs
- **Website:** [🌐 Link](https://doi.org/10.1145/3579856.3595796)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/24-f-blocker-disabling-vulnerability-triggering-functionality.pdf)
- **Authors:** Mohamad Mansouri, Jun Xu, **Georgios Portokalidis** (Stevens Institute of Technology)
- **Institution:** Stevens Institute of Technology (USNWR #76)
- **Venue:** **ACM ASIA CCS 2023**
- **Relevance:** Automatically identifies and surgically disables vulnerability-triggering functionality in binaries without source code — the exact capability CMatrix binary analysis agent targets when assessing patch-resistant systems. Taint analysis and shadow execution provide CMatrix information-flow tracking layer for post-exploitation attribution.
---
## 22. Prof. Yizheng Chen
### 25. Locus: Agentic Predicate Synthesis for Directed Fuzzing
- **Website:** [🌐 Link](https://arxiv.org/abs/2508.21302)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/25-locus-agentic-predicate-synthesis-for-directed-fuzzing.pdf)
- **Code:** [GitHub](https://github.com/jiezhuzzz/Locus)
- **Authors:** Jie Zhu, Chihao Shen, Ziyang Li, Jiahao Yu, **Yizheng Chen** (UMD), Kexin Pei (UChicago)
- **Institution:** University of Maryland, College Park (USNWR #93)
- **Venue:** **ICSE 2026 (CCF-A) — Rio de Janeiro, April 2026**
- **Relevance:** LLM agent synthesizes predicates to guide directed fuzzers toward deep target states — dramatically reduces time-to-exploit. CMatrix fuzzing pipeline should integrate Locus.
---
## 23. Prof. Peng Liu
### 26. PentestGPT: Evaluating and Harnessing Large Language Models for Automated Penetration Testing
- **Website:** [🌐 Link](https://arxiv.org/abs/2308.06782)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/26-pentestgpt-evaluating-and-harnessing-large-language-models-for-automated-penetration-testing.pdf)
- **Code:** [GitHub](https://github.com/GreyDGL/PentestGPT)
- **Authors:** Gelei Deng, Yi Liu, Mayank Varia, **Peng Liu** et al.
- **Institution:** Penn State (USNWR #130)
- **Venue:** **USENIX Security 2024 (CCF-A)**
- **Relevance:** Directly builds an LLM-based pentest agent; multi-stage recon -> exploitation pipeline mirrors your architecture.
---
## 24. Prof. Ting Wang
### 27. Your Agent Can Defend Itself against Backdoor Attacks — ReAgent: LLM agent security defense framework
- **Website:** [🌐 Link](https://arxiv.org/abs/2506.08336)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/27-your-agent-can-defend-itself-against-backdoor-attacks-reagent-llm-agent-security-defense-framework.pdf)
- **Authors:** **Ting Wang** et al.
- **Institution:** Penn State (USNWR #130)
- **Venue:** **arXiv 2025**
- **Relevance:** Security of LLM-based agents; relevant to adversarial robustness of your orchestration layer.
---
## 25. Prof. Guofei Gu
### 28. LLMs in Software Security: A Survey of Vulnerability Detection Techniques and Insights
- **Website:** [🌐 Link](https://arxiv.org/abs/2502.07049)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/28-llms-in-software-security-a-survey-of-vulnerability-detection-techniques-and-insights.pdf)
- **Authors:** **Guofei Gu** et al.
- **Institution:** Texas A&M (USNWR #145)
- **Venue:** **ACM Computing Surveys 2025**
- **Relevance:** Comprehensive LLM-for-vulnerability-detection survey; shares the same automation goal as LLMOrch-VAPT.
---
## 26. Prof. Yan Shoshitaishvili
### 29. Decompiling the Synergy: Human-LLM Teaming in Reverse Engineering 🏆 Distinguished Paper Award
- **Website:** [🌐 Link](https://www.ndss-symposium.org/ndss-paper/decompiling-the-synergy-an-empirical-study-of-human-llm-teaming-in-software-reverse-engineering/)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/29-decompiling-the-synergy-human-llm-teaming-in-reverse.pdf)
- **Code:** [GitHub](https://github.com/mahaloz/dec-synergy-study)
- **Authors:** Zion Leonahenahe Basque, Samuele Doria, Ananta Soneji, Wil Gibbs, **Adam Doupé**, **Yan Shoshitaishvili** (ASU), Eleonora Losiouk (U Padua), Ruoyu Wang (ASU), Simone Aonzo (EURECOM)
- **Institution:** Arizona State University (USNWR #147) + University of Padua + EURECOM
- **Venue:** **NDSS 2026 (CCF-A) — Distinguished Paper Award · Surveyed 153 practitioners**
- **Relevance:** First systematic study of LLM+human collaboration during software reverse engineering — LLM assistance demonstrably narrows the expertise gap. Directly informs CMatrix HITL module design and democratization argument.
---
## 27. Prof. Tiffany Bao
### 30. ARVO: Atlas of Reproducible Vulnerabilities for Open Source Software
- **Website:** [🌐 Link](https://arxiv.org/abs/2408.02153)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/30-arvo-atlas-of-reproducible-vulnerabilities-for-open-source.pdf)
- **Code:** [GitHub](https://github.com/n132/ARVO-Meta)
- **Authors:** Xiang Mei, Pulkit Singh Singaria, Jordi Del Castillo, Haoran Xi, Abdelouahab Benchikh, **Tiffany Bao**, Ruoyu Wang, **Yan Shoshitaishvili**, **Adam Doupé** (ASU), Hammond Pearce, **Brendan Dolan-Gavitt** (NYU)
- **Institution:** Arizona State University (USNWR #147) + NYU Tandon (USNWR #53)
- **Venue:** **arXiv, August 2024**
- **Relevance:** 5,000+ memory vulnerabilities with triggering inputs and verified patches — the largest open-source vulnerability dataset with reproducible exploits. Natural evaluation corpus for CMatrix memory vulnerability scan modes.
---
## 28. Prof. Adam Doupé
### 31. Ahoy SAILR! There is No Need to DREAM of C: A Compiler-Aware Structuring Algorithm for Binary Decompilation
- **Website:** [🌐 Link](https://www.usenix.org/system/files/usenixsecurity24-basque.pdf)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/31-agentfuzz-detecting-taint-style-vulnerabilities-in-llm-based.pdf)
- **Code:** [GitHub](https://github.com/mahaloz/angr-sailr)
- **Authors:** Zion Leonahenahe Basque, Ati Priya Bajaj, **Adam Doupé**, **Yan Shoshitaishvili**, Ruoyu Wang (ASU)
- **Institution:** Arizona State University (USNWR #147)
- **Venue:** **USENIX Security 2024 (CCF-A)**
- **Relevance:** Compiler-aware structuring algorithm for binary decompilation. Integrates with the `angr` analysis framework used in CMatrix's binary analysis pipeline to extract readable, structured C code from raw binaries, enabling precise control-flow and vulnerability tracing.
---
## 29. Prof. Peng Gao
### 32. CTINexus: Automatic Cyber Threat Intelligence Knowledge Graph Construction Using LLMs
- **Website:** [🌐 Link](https://arxiv.org/abs/2410.21060)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/32-ctinexus-automatic-cyber-threat-intelligence-knowledge-graph-construction-using-llms.pdf)
- **Code:** [GitHub](https://github.com/peng-gao-lab/ctinexus)
- **Authors:** **Peng Gao** et al.
- **Institution:** Virginia Tech (USNWR #170)
- **Venue:** **EuroS&P 2025**
- **Relevance:** LLM-driven CTI pipeline with structured knowledge extraction; directly feeds a VAPT intelligence layer.
---
## 30. Prof. Wil Robertson
### 33. LAVA: Large-scale Automated Vulnerability Addition
- **Website:** [🌐 Link](https://ieeexplore.ieee.org/document/7546505)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/33-panda-whole-system-dynamic-analysis-platform-for-security.pdf)
- **Code:** [GitHub](https://github.com/panda-re/lava)
- **Authors:** Brendan Dolan-Gavitt (NYU), Patrick Hulin, Engin Kirda, Tim Leek, Andrea Mambretti, **William K. Robertson** (Northeastern), Frederick Ulrich, Ryan Whelan
- **Institution:** Northeastern University (USNWR #179) + NYU Tandon (USNWR #53)
- **Venue:** **IEEE S&P 2016 (CCF-A) — Cited by 600+ papers**
- **Relevance:** Foundational research on automated vulnerability injection (LAVA-M dataset). Enables standardizing benchmark environments to evaluate the detection and exploit generation capabilities of CMatrix.
---
## 31. Prof. Nidhi Rastogi
### 34. CTIBench: Evaluating LLMs on Real-World Cyber Threat Intelligence Tasks
- **Website:** [🌐 Link](https://arxiv.org/abs/2406.07599)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/34-ctibench-evaluating-llms-on-real-world-cyber-threat.pdf)
- **Code:** [GitHub](https://github.com/maveryn/cti-bench)
- **Authors:** **Nidhi Rastogi** et al. (Rochester Institute of Technology)
- **Institution:** Rochester Institute of Technology (USNWR #320)
- **Venue:** **ACSAC 2024 / arXiv 2024**
- **Relevance:** CTIBench benchmark for evaluating LLMs on cybersecurity tasks — measures LLM hallucinations, relevant to CMatrix's reliability layer.
---
## 32. Prof. Heng Yin
### 35. DECAF: A Platform-Neutral Whole-System Dynamic Binary Analysis Platform
- **Website:** [🌐 Link](https://doi.org/10.1109/TSE.2016.2589242)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/35-decaf-dynamic-executable-code-analysis-framework-whole.pdf)
- **Code:** [GitHub](https://github.com/decaf-project/DECAF)
- **Authors:** **Heng Yin** et al. (UC Riverside)
- **Institution:** UC Riverside (USNWR #405)
- **Venue:** **IEEE Transactions on Software Engineering 2017**
- **Relevance:** Creator of DECAF — whole-system dynamic analysis platform. DECAF's dynamic taint analysis provides the foundation for CMatrix's grey-box binary scan.
---
## 33. Prof. Murtuza Jadliwala
### 36. We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs
- **Website:** [🌐 Link](https://arxiv.org/abs/2406.10279)
- **Paper:** [📄 Local PDF](../downloaded-paper-professor/36-we-have-a-package-for-you-a-comprehensive-analysis-of-package-hallucinations-by-code-generating-llms.pdf)
- **Code:** [GitHub](https://github.com/Spracks/PackageHallucination)
- **Authors:** Joseph Spracklen, Raveen Wijewickrama, A H M Nazmus Sakib, Anindya Maiti, Bimal Viswanath, **Murtuza Jadliwala** (University of Texas at San Antonio)
- **Institution:** UT San Antonio (USNWR #411)
- **Venue:** **USENIX Security 2025 (CCF-A)**
- **Relevance:** LLM package hallucination attacks; directly relevant to CMatrix's post-exploit analysis phase when analyzing LLM-generated payloads.

---
