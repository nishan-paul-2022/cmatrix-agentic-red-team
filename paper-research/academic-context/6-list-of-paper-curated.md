# Curated Research Papers

> **Scope:** Papers directly relevant to our work — LLM-based agentic pentesting,
> multi-agent red-team orchestration, autonomous vulnerability exploitation, offensive security
> benchmarks, and agentic cybersecurity systems. Ordered from **most recent → oldest**.
> Quality filter: CCF-A/B venues, major arXiv preprints with 50+ citations, or direct architectural
> equivalents.

---

## `2026 Papers`

### 1. [HackWorld: Evaluating Computer-Use Agents on Exploiting Web Application Vulnerabilities](https://arxiv.org/abs/2510.12200)
- **Authors:** **Xiaoxue Ren**, Penghao Jiang, Kaixin Li, Zhiyong Huang, Xiaoning Du, Jiaojiao Jiang, Zhenchang Xing, Jiamou Sun, Terry Yue Zhuo
- **Institution:** Zhejiang University (USNWR #45)
- **Venue:** **ICLR 2026**
- **Code:** [GitHub](https://github.com/GUI-Agent/HackWorld)
- **Relevance:** Evaluates GUI/computer-use LLM agents autonomously attacking real web application vulnerabilities — directly maps to CMatrix's black-box scan mode and web vuln pipeline. Uses the same agent-environment loop that CMatrix's VS Code-style terminal UI embodies.

---

### 2. [Cyber-Zero: Training Cybersecurity Agents without Runtime](https://arxiv.org/abs/2508.00910)
- **Authors:** **Terry Yue Zhuo**, Dingmin Wang, Hantian Ding, Varun Kumar, Zijian Wang
- **Institution:** Monash University (USNWR #38)
- **Venue:** **ICLR 2026**
- **Code:** [GitHub](https://github.com/amazon-science/cyber-zero)
- **Relevance:** Trains offensive security agents *without runtime environment access* — directly relevant to CMatrix's offline/local model strategy and the question of pre-training vs. fine-tuning for pentest tasks. Amazon research.

---

### 3. [What Makes a Good LLM Agent for Real-world Penetration Testing?](https://arxiv.org/abs/2602.17622)
- **Authors:** **Gelei Deng**, Yi Liu, Yuekang Li, Ruozhao Yang, Xiaofei Xie, Jie Zhang, Han Qiu, Tianwei Zhang
- **Institution:** Nanyang Technological University (USNWR #28)
- **Venue:** **arXiv (Feb 2026)**
- **Relevance:** PentestGPT V2 paper — empirically identifies what agent properties (planning, memory, tool use) matter most for real-world pentest. Achieves 76.9% (10/13 machines) on HackTheBox. Directly comparable to CMatrix's evaluation framework design.

---

### 4. [Pen-Strategist: A Reasoning Framework for Penetration Testing Strategy Formation and Analysis](https://arxiv.org/abs/2605.04499)
- **Authors:** **Yasod Ginige**, Pasindu Marasinghe, Sajal Jain, Suranga Seneviratne
- **Institution:** University of Sydney (USNWR #29)
- **Venue:** **arXiv (May 2026)**
- **Relevance:** Two-model framework: a fine-tuned domain-specific **Strategy Model** (logical reasoning over prior findings) + a **Step Classifier** (converts strategies → tool selections). Runs fully locally for data privacy — same design philosophy as CMatrix's local Vast.ai deployment. Table 10 contains the most comprehensive survey of 28 LLM-based PT systems as of May 2026 — mandatory reference for CMatrix's related work section. Same author group as AutoPentester (#28), forming a coherent Sydney research lineage CMatrix must engage with.

---

### 5. [Co-RedTeam: Orchestrated Security Discovery and Exploitation with LLM Agents](https://arxiv.org/abs/2602.02164)
- **Authors:** **Pengfei He**, Ash Fox, Lesly Miculicich, Stefan Friedli, Daniel Fabian, Burak Gokturk, Jiliang Tang, Chen-Yu Lee, Tomas Pfister, Long T. Le
- **Institution:** Google Cloud AI Research
- **Venue:** **arXiv (Feb 2026) — Google Cloud AI Research**
- **Relevance:** Multi-agent red team with specialized roles (discovery agent, exploitation agent, critic agent) and structured interaction — architecturally almost identical to CMatrix's reconnaissance-scan-exploit pipeline. Google-authored.

---

### 6. [CyberExplorer: Benchmarking LLM Offensive Security Capabilities in a Real-World Attacking Simulation](https://arxiv.org/abs/2602.08023)
- **Authors:** **Nanda Rani**, Kimberly Milner, Minghao Shao, Meet Udeshi, Haoran Xi, Venkata Sai Charan Putrevu, Saksham Aggarwal, Sandeep K. Shukla, Prashanth Krishnamurthy, Farshad Khorrami, Muhammad Shafique, Ramesh Karri
- **Institution:** CISPA - Helmholtz Center for Information Security
- **Venue:** **arXiv (Feb 2026)**
- **Relevance:** Open-environment benchmark with 40 vulnerable web services, multi-target scenarios, autonomous reconnaissance without prior knowledge — perfectly mirrors CMatrix's black-box scan scenario. Defines evaluation metrics CMatrix should adopt.

---

### 7. [To Defend Against Cyber Attacks, We Must Teach AI Agents to Hack](https://arxiv.org/abs/2602.02595)
- **Authors:** **Terry Yue Zhuo**, Yangruibo Ding, Wenbo Guo, Ruijie Meng
- **Institution:** Monash University (USNWR #38)
- **Venue:** **arXiv (Feb 2026)**
- **Relevance:** Argues for and demonstrates offensive-security-first agent training — the philosophical and technical grounding for CMatrix's approach of using unrestricted models (DeepSeek-R1) for red-team tasks.

---

### 8. [LLMs as Hackers: Autonomous Linux Privilege Escalation Attacks](https://link.springer.com/article/10.1007/s10664-025-10758-3)
- **Authors:** **Andreas Happe**, Aaron Kaplan, Jürgen Cito
- **Institution:** TU Wien (USNWR #334)
- **Venue:** **Empirical Software Engineering 2026 (Springer)**
- **Relevance:** End-to-end autonomous privilege escalation — a concrete pentest sub-task CMatrix's exploitation agent must handle. Real-system evaluation on Linux.

---

### 9. [Towards Cybersecurity Superintelligence: from AI-guided humans to human-guided AI](https://arxiv.org/abs/2601.14614)
- **Authors:** **Víctor Mayoral-Vilches**, Stefan Rass, Martin Pinzger, Endika Gil-Uriarte, Unai Ayucar-Carbajo, Jon Ander Ruiz-Alcalde, Maite del Mundo de Torres, María Sanz-Gómez, Francesco Balassone, Cristóbal R. J. Veas Chavez, Vanesa Turiel, Alfonso Glera-Picón, Daniel Sánchez-Prieto, Yuri Salvatierra, Paul Zabalegui-Landa, Ruffino Reydel Cabrera-Álvarez, Patxi Mayoral-Pizarroso
- **Institution:** Alias Robotics
- **Venue:** **arXiv (Jan 2026) — Alias Robotics**
- **Relevance:** Documents the full progression PentestGPT → CAI → G-CTR. The most comprehensive single paper tracking the evolution of the field CMatrix operates in. Directly cites game-theoretic agent reasoning as the frontier.

---

### 10. [A Survey of Agentic AI and Cybersecurity: Challenges, Opportunities and Use-case Prototypes](https://arxiv.org/abs/2601.05293)
- **Authors:** **Sahaya Jestus Lazer**, Kshitiz Aryal, Maanak Gupta, Elisa Bertino
- **Institution:** Tennessee Tech University (USNWR #232)
- **Venue:** **arXiv (Jan 2026)**
- **Relevance:** Comprehensive dual-use analysis of agentic AI in cybersecurity — planning, memory, tool orchestration, multi-agent interaction. Positions exactly where CMatrix sits in the landscape.

---

### 11. [A Red Teaming Framework for Evaluating Robustness of AI-enabled Security Orchestration, Automation, and Response (SOAR) Systems](https://arxiv.org/abs/2605.17075)
- **Authors:** **Ayan Javeed Shaikh**, Nathaniel D. Bastian, Ankit Shah
- **Institution:** Indiana University (USNWR #73)
- **Venue:** **arXiv (May 2026)**
- **Relevance:** Hybrid LLM-RL red teaming against enterprise SOAR systems — multi-stage attack campaigns, shows standalone LLM agents failing, justifying CMatrix's multi-agent design.

---

### 12. [ExploitGym: Can AI Agents Turn Security Vulnerabilities into Real Attacks?](https://arxiv.org/abs/2605.11086)
- **Authors:** **Zhun Wang**, Nico Schiller, Hongwei Li, Srijiith Sesha Narayana, Milad Nasr, Nicholas Carlini, Xiangyu Qi, Eric Wallace, Elie Bursztein, Luca Invernizzi, Kurt Thomas, Yan Shoshitaishvili, Wenbo Guo, Jingxuan He, Thorsten Holz, Dawn Song
- **Institution:** UC Berkeley (USNWR #4)
- **Venue:** **arXiv (May 2026)**
- **Relevance:** Evaluates defensive security agents using automated exploits and reinforcement learning to turn vulnerabilities into verified attacks.

---

### 13. [AWE: Adaptive Agents for Dynamic Web Penetration Testing](https://www.ndss-symposium.org/ndss-paper/auto-draft-680/)
- **Authors:** **Akshat Singh Jaswal**, Ashish Baghel
- **Institution:** Stux Labs
- **Venue:** **NDSS 2026**
- **Code:** [GitHub](https://github.com/stuxlabs/AWE)
- **Relevance:** Adaptive agents designed specifically for dynamic web penetration testing — highly relevant to CMatrix's web agent architecture.

---

### 14. [PACEbench: A Framework for Evaluating Practical AI Cyber-Exploitation Capabilities](https://openreview.net/pdf?id=kGEuZXaXU6)
- **Authors:** **Zicheng Liu**, Lige Huang, Jie Zhang, Dongrui Liu, Yuan Tian, Jing Shao
- **Institution:** Shanghai Artificial Intelligence Laboratory
- **Venue:** **ICLR 2026**
- **Code:** [GitHub](https://github.com/RyuKosei/PACEbench)
- **Relevance:** Evaluates practical AI cyber-exploitation capabilities on diverse benchmarks — validates offensive agent evaluation standards.

---

## `2025 Papers`

### 15. [EnIGMA: Interactive Tools Substantially Assist LM Agents in Finding Security Vulnerabilities](https://arxiv.org/abs/2409.16165)
- **Authors:** **Talor Abramovich**, Meet Udeshi, Minghao Shao, Kilian Lieret, Haoran Xi, Kimberly Milner, Sofija Jancheska, John Yang, Carlos E. Jimenez, Farshad Khorrami, Prashanth Krishnamurthy, Brendan Dolan-Gavitt, Muhammad Shafique, Karthik Narasimhan, Ramesh Karri, Ofir Press
- **Institution:** NYU Tandon (USNWR #53)
- **Venue:** **ICLR 2025**
- **Code:** [GitHub](https://github.com/SWE-agent/SWE-agent/tree/v0.7)
- **Relevance:** Shows interactive tooling dramatically improves LLM agent security performance. Directly validates CMatrix's xterm.js terminal integration and interactive tool design (vs. static script execution).

---

### 16. [Can LLMs Hack Enterprise Networks? Autonomous Assumed Breach Penetration-Testing Active Directory Networks](https://dl.acm.org/doi/abs/10.1145/3766895)
- **Authors:** **Andreas Happe**, Jürgen Cito
- **Institution:** TU Wien (USNWR #334)
- **Venue:** **TOSEM 2025 (ACM Transactions on Software Engineering and Methodology)**
- **Code:** [GitHub](https://github.com/andreashappe/cochise)
- **Relevance:** Enterprise AD network pentest — closest to CMatrix's grey-box scan mode and multi-host lateral movement scenarios. Top journal publication.

---

### 17. [Measuring and Augmenting Large Language Models for Solving Capture-the-Flag Challenges](https://dl.acm.org/doi/abs/10.1145/3719027.3744855)
- **Authors:** **Zimo Ji**, Daoyuan Wu, Wenyuan Jiang, Pingchuan Ma, Zongjie Li, Shuai Wang
- **Institution:** Hong Kong University of Science and Technology (USNWR #109)
- **Venue:** **ACM CCS 2025**
- **Relevance:** CTF is the primary evaluation playground for offensive LLM agents. Top-tier CCS paper on systematically augmenting LLMs for this task — directly informs CMatrix's benchmark design.

---

### 18. [PentestAgent: Incorporating LLM Agents to Automated Penetration Testing](https://arxiv.org/abs/2411.05185)
- **Authors:** **Xiangmin Shen**, Lingzhi Wang, Zhenyuan Li, Yan Chen, Wencheng Zhao, Dawei Sun, Jiashui Wang
- **Institution:** Northwestern University (USNWR #9)
- **Venue:** **AsiaCCS 2025**
- **Code:** [GitHub](https://github.com/GH05TCREW/PentestAgent)
- **Relevance:** Fully autonomous multi-agent pentesting, competes directly with CMatrix. Evaluated against VulHub + HackTheBox. Strongest direct architectural competitor.

---

### 19. [From Capabilities to Performance: Evaluating Key Functional Properties of LLM Architectures in Penetration Testing](https://arxiv.org/abs/2509.14289)
- **Authors:** **Lanxiao Huang**, Daksh Dave, Tyler Cody, Peter Beling, Ming Jin
- **Institution:** Virginia Tech (USNWR #170)
- **Venue:** **ACL 2025**
- **Relevance:** Systematic evaluation of how specific LLM architectural properties (chain-of-thought, tool use, context window) affect pentest performance. Directly informs CMatrix's model selection (DeepSeek-R1-Distill reasoning).

---

### 20. [A Unified Modeling Framework for Automated Penetration Testing](https://www.sciencedirect.com/science/article/abs/pii/S0167404825004766)
- **Authors:** **Yunfei Wang**, Shixuan Liu, Wenhao Wang, Changling Zhou, Chao Zhang, Jiandong Jin, Cheng Zhu
- **Institution:** National University of Defense Technology
- **Venue:** **Computers & Security 2025 (Elsevier — CCF-B)**
- **Relevance:** Unified formal framework covering all phases of automated pentesting — directly maps to CMatrix's black/grey/white-box unified LangGraph pipeline. Published in CMatrix's target journal.

---

### 21. [VulnBot: Autonomous Penetration Testing for a Multi-Agent Collaborative Framework](https://arxiv.org/abs/2501.13411)
- **Authors:** **He Kong**, Die Hu, Jingguo Ge, Liangxiong Li, Tong Li, Bingzhen Wu
- **Institution:** Institute of Information Engineering, Chinese Academy of Sciences
- **Venue:** **arXiv (Jan 2025)**
- **Code:** [GitHub](https://github.com/KHenryAegis/VulnBot)
- **Relevance:** Role-specialized multi-agent framework (recon, scan, exploit) with penetration task graph (PTG) for logical execution — the closest existing architectural match to CMatrix's LangGraph pipeline design.

---

### 22. [Incalmo: An Autonomous LLM-assisted System for Red Teaming Multi-Host Networks](https://arxiv.org/abs/2501.16466)
- **Authors:** **Brian Singer**, Keane Lucas, Lakshmi Adiga, Meghna Jain, Lujo Bauer, Vyas Sekar
- **Institution:** Carnegie Mellon University (USNWR #22)
- **Venue:** **arXiv (Jan 2025, multiple revisions through Nov 2025)**
- **Code:** [GitHub](https://github.com/bsinger98/Incalmo)
- **Relevance:** Multi-host red teaming with abstract action layer — compromised 9/10 mobile-core testbeds (25–50 hosts). Directly comparable to CMatrix's multi-target scan mode.

---

### 23. [CAI: An Open, Bug Bounty-Ready Cybersecurity AI](https://arxiv.org/abs/2504.06017)
- **Authors:** **Víctor Mayoral-Vilches**, Luis Javier Navarrete-Lozano, María Sanz-Gómez, Lidia Salas Espejo, Martiño Crespo-Álvarez, Francisco Oca-Gonzalez, Francesco Balassone, Alfonso Glera-Picón, Unai Ayucar-Carbajo, Jon Ander Ruiz-Alcalde, Stefan Rass, Martin Pinzger, Endika Gil-Uriarte
- **Institution:** Alias Robotics
- **Venue:** **arXiv (Apr 2025) — Alias Robotics**
- **Code:** [GitHub](https://github.com/aliasrobotics/CAI)
- **Relevance:** The most production-proven autonomous pentest agent in existence (Rank #1 at 5 major CTF competitions, $50K Neurogrid prize). Direct competitor. Architectural reference for what CMatrix aspires to become.

---

### 24. [Cybersecurity AI: The World's Top AI Agent for Security CTF](https://arxiv.org/abs/2512.02654)
- **Authors:** **Víctor Mayoral-Vilches**, Luis Javier Navarrete-Lozano, Francesco Balassone, María Sanz-Gómez, Cristóbal R. J. Veas Chavez, Maite del Mundo de Torres, Vanesa Turiel
- **Institution:** Alias Robotics
- **Venue:** **arXiv (Dec 2025) — Alias Robotics**
- **Relevance:** Documents CAI's dominance across 5 international CTF competitions. Establishes the current state-of-the-art benchmark CMatrix must measure against.

---

### 25. [Pentest-R1: Towards Autonomous Penetration Testing Reasoning Optimized via Two-Stage Reinforcement Learning](https://arxiv.org/abs/2508.07382)
- **Authors:** **He Kong**, Die Hu, Jingguo Ge, Liangxiong Li, Hui Li, Tong Li
- **Institution:** Institute of Information Engineering, Chinese Academy of Sciences
- **Venue:** **arXiv (Aug 2025)**
- **Code:** [GitHub](https://github.com/KHenryAegis/Pentest-R1)
- **Relevance:** Applies two-stage RL (offline on 500+ walkthroughs → online CTF environment) to optimize pentest reasoning. Achieves 24.2% on AutoPenBench and 15.0% on Cybench for open-source models. Directly validates CMatrix's choice of DeepSeek-R1 (chain-of-thought reasoning model) and informs the planned fine-tuning strategy.

---

### 26. [RedTeamLLM: an Agentic AI Framework for Offensive Security](https://arxiv.org/abs/2505.06913)
- **Authors:** **Brian Challita**, Pierre Parrend
- **Institution:** Laboratoire de Recherche de l'EPITA, France
- **Venue:** **arXiv (May 2025)**
- **Code:** [GitHub](https://github.com/lre-security-systems-team/redteamllm)
- **Relevance:** Direct autonomous agentic VAPT framework designed to solve open challenges in planning, memory, and tool integration. Useful architectural reference.

---

### 27. [xOffense: An AI-driven Autonomous Penetration Testing Framework with Offensive Knowledge-enhanced LLMs and Multi-Agent Systems](https://arxiv.org/abs/2509.13021)
- **Authors:** **Phung Duc Luong**, Le Tran Gia Bao, Nguyen Vu Khai Tam, Dong Huu Nguyen Khoa, Van-Hau Pham, Phan The Duy, Nguyen Huu Quyen
- **Institution:** University of Information Technology, Vietnam
- **Venue:** **arXiv (Sep 2025) — submitted to Elsevier**
- **Relevance:** Uses fine-tuned Qwen3-32B as reasoning backbone with specialized recon/scan/exploit agents — mirrors CMatrix's open-source LLM + multi-agent approach. Even the model scale (~32B) is identical to CMatrix's DeepSeek-R1-Distill-Qwen-32B choice.

---

### 28. [D-CIPHER: Dynamic Collaborative Intelligent Multi-Agent System with Planner and Heterogeneous Executors for Offensive Security](https://arxiv.org/abs/2502.10931)
- **Authors:** **Meet Udeshi**, Minghao Shao, Haoran Xi, Kimberly Milner, Venkata Sai Charan Putrevu, Brendan Dolan-Gavitt, Prashanth Krishnamurthy, Farshad Khorrami, Ramesh Karri, Muhammad Shafique, Nanda Rani, Sandeep K. Shukla
- **Institution:** NYU Tandon (USNWR #53)
- **Venue:** **arXiv (Feb 2025)**
- **Relevance:** Planner-executor multi-agent system with heterogeneous specialized agents for CTF — directly informs CMatrix's agent role decomposition and inter-agent communication protocol.

---

### 29. [AutoPentester: An LLM Agent-based Framework for Automated Penetration Testing](https://arxiv.org/abs/2510.05605)
- **Authors:** **Yasod Ginige**, Asitha Niroshan, Sajal Jain, Suranga Seneviratne
- **Institution:** University of Sydney (USNWR #29)
- **Venue:** **IEEE (also arXiv Oct 2025)**
- **Relevance:** Five-module architecture (Strategy Analyzer → RAG Summarizer → Generator → Results Verifier → Repetition Identifier) with CoT-based dynamic attack strategy generation — the closest single-paper analogue to CMatrix's LangGraph conditional branching design. Hard numbers: 27.0% better subtask completion, 39.5% more vulnerability coverage, 19.8% higher user score vs PentestGPT. Evaluated on HackTheBox + custom VMs. Primary direct comparison baseline for any CMatrix publication. Same author group as Pen-Strategist (#4).

---

### 30. [RapidPen: Fully Automated IP-to-Shell Penetration Testing with LLM-based Agents](https://arxiv.org/abs/2502.16730)
- **Authors:** **Sho Nakatani**
- **Institution:** SecDevLab Inc.
- **Venue:** **arXiv (Feb 2025)**
- **Relevance:** End-to-end IP→shell automation via ReAct agent in 200–400 seconds, $0.30–$0.60/run. Establishes cost/speed benchmarks for autonomous pentest that CMatrix should target.

---

### 31. [ARACNE: An LLM-Based Autonomous Shell Pentesting Agent](https://arxiv.org/abs/2502.18528)
- **Authors:** **Tomas Nieponice**, Veronica Valeros, Sebastian Garcia
- **Institution:** Colegio Nacional de Buenos Aires
- **Venue:** **arXiv (Feb 2025)**
- **Relevance:** Shell-level autonomous pentest agent — the execution-layer component CMatrix's exploit agent must replicate. Evaluates on realistic network environments.

---

### 32. [AutoPentest: Enhancing Vulnerability Management With Autonomous LLM Agents](https://arxiv.org/abs/2505.10321)
- **Authors:** **Julius Henke**
- **Institution:** University of Amsterdam (USNWR #33)
- **Venue:** **arXiv (May 2025)**
- **Code:** [GitHub](https://github.com/JuliusHenke/autopentest)
- **Relevance:** Integrates GPT-4o with LangChain for enumeration-to-exploitation — the exact same stack (LangChain/LangGraph + LLM) as CMatrix. Direct implementation comparison.

---

### 33. [RefPentester: A Knowledge-Informed Self-Reflective Penetration Testing Framework Based on Large Language Models](https://arxiv.org/abs/2505.07089)
- **Authors:** **Hanzheng Dai**, Yuanliang Li, Jun Yan, Zhibo Zhang
- **Institution:** Concordia University (USNWR #755)
- **Venue:** **arXiv (May 2025)**
- **Code:** [GitHub](https://github.com/ipa-lab/hackingBuddyGPT)
- **Relevance:** Self-reflective reasoning in pentesting — directly maps to CMatrix's agent feedback loops and critique mechanisms. Knowledge-augmented approach aligns with Qdrant memory design.

---

### 34. [CurriculumPT: LLM-Based Multi-Agent Autonomous Penetration Testing with Curriculum-Guided Task Scheduling](https://www.mdpi.com/2076-3417/15/16/9096)
- **Authors:** **Xingyu Wu**, Yunzhe Tian, Yuanwan Chen, Ping Ye, Xiaoshu Cui, Jingqi Jia, Shouyang Li, Jiqiang Liu, Wenjia Niu
- **Institution:** Beijing Jiaotong University (USNWR #542)
- **Venue:** **Applied Sciences (MDPI) — Aug 2025**
- **Relevance:** Curriculum learning for progressive skill acquisition in multi-agent pentest — relevant to CMatrix's planned fine-tuning pipeline (easy → hard exploits, progressive task complexity).

---

### 35. [Automated Penetration Testing with LLM Agents and Classical Planning](https://arxiv.org/abs/2512.11143)
- **Authors:** **Lingzhi Wang**, Xinyi Shi, Ziyu Li, Yi Jiang, Shiyu Tan, Yuhao Jiang, Junjie Cheng, Wenyuan Chen, Xiangmin Shen, Zhenyuan Li, Yan Chen
- **Institution:** Northwestern University (USNWR #9)
- **Venue:** **arXiv (Dec 2025)**
- **Relevance:** Combines classical planning (symbolic AI) with LLM agents for structured pentest execution — hybrid approach that CMatrix could adopt to reduce hallucination in multi-step exploit chains.

---

### 36. [PentestMCP: LLM and MCP Based Multi-Agent Framework for Automated Penetration Testing](https://sciety.org/articles/activity/10.21203/rs.3.rs-7582841/v1)
- **Authors:** **Jiqiang Zhai**, Xinyi Zhou, Hong Miao, Zekun Li, Zhe Li, Hailu Yang
- **Institution:** Harbin University of Science and Technology (USNWR #773)
- **Venue:** **Preprint (Nov 2025)**
- **Relevance:** MCP-based multi-agent pentest — this is *exactly* what CMatrix identified as a key future-proofing upgrade. Validates the MCP-first architecture CMatrix plans to adopt.

---

### 37. [On the Surprising Efficacy of LLMs for Penetration-Testing](https://arxiv.org/abs/2507.00829)
- **Authors:** **Andreas Happe**, Jürgen Cito
- **Institution:** TU Wien (USNWR #334)
- **Venue:** **arXiv (Jul 2025)**
- **Relevance:** Provides empirical evidence for what LLMs can and can't do natively in pentesting — baseline capability study essential for CMatrix's model selection and agent design decisions.

---

### 38. [Multi-Agent Penetration Testing AI for the Web](https://arxiv.org/abs/2508.20816)
- **Authors:** **Isaac David**, Arthur Gervais
- **Institution:** University College London (USNWR #7)
- **Venue:** **arXiv (Aug 2025)**
- **Relevance:** Web-specific multi-agent pentest — CMatrix's primary initial attack surface. Detailed agent decomposition for web recon, injection, exploitation.

---

### 39. [Forewarned is Forearmed: A Survey on LLM-based Agents in Autonomous Cyberattacks](https://arxiv.org/abs/2505.12786)
- **Authors:** **Minrui Xu**, Jiani Fan, Xinyu Huang, Conghao Zhou, Jiawen Kang, Dusit Niyato, Shiwen Mao, Zhu Han, Xuemin (Sherman) Shen, Kwok-Yan Lam
- **Institution:** Nanyang Technological University (USNWR #28)
- **Venue:** **arXiv (May 2025)**
- **Relevance:** Comprehensive survey on offensive LLM agent capabilities across all attack stages. The reference survey most aligned with CMatrix's scope. Covers recon, exploitation, lateral movement, persistence.

---

### 40. [Towards Automated Penetration Testing: Introducing LLM Benchmark, Analysis, and Improvements](https://dl.acm.org/doi/full/10.1145/3708319.3733804)
- **Authors:** **Isamu Isozaki**, Manil Shrestha, Rick Console, Edward Kim
- **Institution:** Drexel University (USNWR #80)
- **Venue:** **UMAP 2025**
- **Code:** [GitHub](https://github.com/anonyippi/PentestBenchmarkPaper)
- **Relevance:** Standardized pentest benchmark + LLM comparison — baseline metrics CMatrix should report against.

---

### 41. [Cybersecurity AI: A Game-Theoretic AI for Guiding Attack and Defense](https://arxiv.org/abs/2601.05887)
- **Authors:** **Víctor Mayoral-Vilches**, María Sanz-Gómez, Francesco Balassone, Stefan Rass, Lidia Salas-Espejo, Benjamin Jablonski, Luis Javier Navarrete-Lozano, Maite del Mundo de Torres, Cristóbal R. J. Veas Chavez
- **Institution:** Alias Robotics
- **Venue:** **arXiv (Jan 2026)**
- **Relevance:** Game-theoretic reasoning layer on top of LLM agents — reduces hallucination and improves strategic multi-step exploit planning. Future direction for CMatrix.

---

### 42. [BountyBench: Dollar Impact of AI Agent Attackers and Defenders on Real-World Cybersecurity Systems](https://arxiv.org/abs/2505.15216)
- **Authors:** **Andy K. Zhang**, Joey Ji, Celeste Menders, Riya Dulepet, Thomas Qin, Ron Y. Wang, Junrong Wu, Kyleen Liao, Jiliang Li, Jinghan Hu, Sara Hong, Nardos Demilew, Shivatmica Murgai, Jason Tran, Nishka Kacheria, Ethan Ho, Denis Liu, Lauren McLane, Olivia Bruvik, Dai-Rong Han, Seungwoo Kim, Akhil Vyas, Cuiyuanxiu Chen, Ryan Li, Weiran Xu, Jonathan Z. Ye, Prerit Choudhary, Siddharth M. Bhatia, Vikram Sivashankar, Yuxuan Bao, Dawn Song, Dan Boneh, Daniel E. Ho, Percy Liang
- **Institution:** Stanford University (USNWR #3)
- **Venue:** **NeurIPS 2025 (Datasets and Benchmarks Track) — Stanford / UC Berkeley**
- **Code:** [bountybench.github.io](https://bountybench.github.io)
- **Relevance:** First benchmark to quantify AI agent cyber-capability in real dollar terms. 25 production systems, 40 bounties ($10–$30,485), covering 9 OWASP Top 10 risks. Defines Detect/Exploit/Patch task taxonomy — precisely the three phases CMatrix automates. Evaluated DeepSeek-R1 among 10 agents, giving CMatrix a direct reference point for its backbone model.

---

### 43. [CRAKEN: Cybersecurity LLM Agent with Knowledge-Based Execution](https://arxiv.org/abs/2505.17107)
- **Authors:** **Minghao Shao**, Haoran Xi, Nanda Rani, Meet Udeshi, Venkata Sai Charan Putrevu, Kimberly Milner, Brendan Dolan-Gavitt, Sandeep Kumar Shukla, Prashanth Krishnamurthy, Farshad Khorrami, Ramesh Karri, Muhammad Shafique
- **Institution:** New York University (USNWR #53)
- **Venue:** **arXiv (May 2025) — NYU**
- **Code:** [GitHub](https://github.com/NYU-LLM-CTF/nyuctf_agents_craken)
- **Relevance:** Knowledge-based RAG (Self-RAG + Graph-RAG) injected into a planner-executor multi-agent CTF system — 22% on NYU CTF Bench. Directly validates CMatrix's Qdrant + knowledge-graph approach for CVE/exploit retrieval. Built on top of D-CIPHER architecture.

---

### 44. [CyberGym: Evaluating AI Agents' Real-World Cybersecurity Capabilities at Scale](https://arxiv.org/abs/2506.02548)
- **Authors:** **Zhun Wang**, Tianneng Shi, Jingxuan He, Matthew Cai, Jialin Zhang, Dawn Song
- **Institution:** UC Berkeley (USNWR #4)
- **Venue:** **arXiv (Jun 2025, v2 Oct 2025) — UC Berkeley (Dawn Song group)**
- **Code:** [cybergym.io](https://cybergym.io)
- **Relevance:** The largest cybersecurity benchmark in existence — 1,507 real-world vulnerabilities across 188 software projects, 7.5× larger than any prior benchmark. Led to discovery of 35 zero-day vulnerabilities and 17 incomplete patches in production software. The definitive scale benchmark CMatrix must eventually target.

---

### 45. [An Empirical Evaluation of LLMs for Solving Offensive Security Challenges](https://arxiv.org/abs/2402.11814)
- **Authors:** **Minghao Shao**, Boyuan Chen, Siddharth Garg, Ramesh Karri
- **Institution:** New York University (USNWR #53)
- **Venue:** **NeurIPS 2024**
- **Code:** [GitHub](https://github.com/NickNameInvalid/LLM_CTF)
- **Relevance:** Gold-standard empirical evaluation of multiple LLMs on offensive security — establishes which models work, which fail. Directly informs CMatrix's LLM selection.

---

### 46. [Shell or Nothing: Real-World Benchmarks and Memory-Activated Agents for Automated Penetration Testing](https://dspace.bracu.ac.bd/xmlui/handle/10361/27423)
- **Authors:** **Wuyuao Mai**, Jinsong Chen, Geng Hong, Qi Liu, Jiarun Dai, Xudong Pan, Min Yang, Yuan Zhang
- **Institution:** Fudan University (USNWR #70)
- **Venue:** **arXiv (2025)**
- **Relevance:** Introduces memory-activated agents for automated penetration testing and real-world system benchmarks.

---

### 47. [PentestEval: Benchmarking LLM-based Penetration Testing with Modular and Stage-Level Design](https://arxiv.org/abs/2512.14233)
- **Authors:** **Ruozhao Yang**, Mingfei Cheng, Gelei Deng, Tianwei Zhang, Junjie Wang, Xiaofei Xie
- **Institution:** Singapore Management University (USNWR #616)
- **Venue:** **arXiv (Dec 2025)**
- **Relevance:** Benchmarking platform designed to evaluate stage-level and modular penetration testing behaviors in LLM agents.

---

### 48. [AGrail: Lifelong Agent Guardrail with Effective and Adaptive Safety Detection](https://arxiv.org/abs/2502.11448)
- **Authors:** **Weidi Luo**, Shenghong Dai, Xiaogeng Liu, Suman Banerjee, Huan Sun, Muhao Chen, Chaowei Xiao
- **Institution:** The Ohio State University (USNWR #41)
- **Venue:** **arXiv (Feb 2025)**
- **Relevance:** Adaptive safety detection and lifelong command execution guardrails (e.g., intercepting malicious CLI commands). Relevant to CMatrix's execution sandbox and tool safety logic.

---

### 49. [RAG for Cybersecurity: Hybrid Retrieval for LLMs](https://arxiv.org/abs/2510.27080)
- **Authors:** **Arnabh Borah**, Md Tanvirul Alam, Nidhi Rastogi
- **Institution:** Rochester Institute of Technology (USNWR #320)
- **Venue:** **arXiv (Oct 2025)**
- **Relevance:** Adapting LLMs to emerging cybersecurity using retrieval augmented generation. Directly relevant to CMatrix's Vuln-Intel agent architecture for CVE and threat intelligence lookup.

---

### 50. [CAIBench: Cybersecurity AI Meta-Benchmark](https://arxiv.org/abs/2510.24317)
- **Authors:** **María Sanz-Gómez**, Víctor Mayoral-Vilches, Francesco Balassone, Luis Javier Navarrete-Lozano, Cristóbal R. J. Veas Chavez, Maite del Mundo de Torres
- **Institution:** Alias Robotics
- **Venue:** **arXiv (Oct 2025)**
- **Relevance:** Evaluates agent capabilities by meta-benchmarking across Cybench, SecEval, and AutoPenBench, establishing a robust framework for comparing CMatrix's overall capabilities.

---

### 51. [When LLMs Meet Cybersecurity: A Systematic Literature Review](https://doi.org/10.1186/s42400-025-00361-w)
- **Authors:** **Jie Zhang**, Haoyu Bu, Hui Wen, Yongji Liu, Haiqiang Fei, Rongrong Xi, Lun Li, Yun Yang, Hongsong Zhu, Dan Meng
- **Institution:** Institute of Information Engineering, Chinese Academy of Sciences
- **Venue:** **Cybersecurity Journal (Springer) 2025**
- **Relevance:** Must-read systematic review of the entire LLM + cybersecurity intersection, providing technical taxonomy for offensive and defensive agent behaviors.

---

## `2024 Papers`

### 52. [NYU CTF Bench: A Scalable Open-Source Benchmark Dataset for Evaluating LLMs in Offensive Security](https://proceedings.neurips.cc/paper_files/paper/2024/hash/69d97a6493fbf016fff0a751f253ad18-Abstract-Datasets_and_Benchmarks_Track.html)
- **Authors:** **Minghao Shao**, Sofija Jancheska, Meet Udeshi, Brendan Dolan-Gavitt, Haoran Xi, Kimberly Milner, Boyuan Chen, Max Yin, Siddharth Garg, Prashanth Krishnamurthy, Farshad Khorrami, Ramesh Karri, Muhammad Shafique
- **Institution:** New York University (USNWR #53)
- **Venue:** **NeurIPS 2024**
- **Code:** [GitHub](https://github.com/NYU-LLM-CTF/NYUCTFBench)
- **Relevance:** The standard CTF benchmark for LLM evaluation. CMatrix's lab environment (lab.kaiofficial.xyz) should be evaluated against this dataset.

---

### 53. [Teams of LLM Agents Can Exploit Zero-Day Vulnerabilities](https://arxiv.org/abs/2406.01637)
- **Authors:** **Yuxuan Zhu**, Antony Kellermann, Akul Gupta, Philip Li, Richard Fang, Rohan Bindu, Daniel Kang
- **Institution:** University of Illinois Urbana-Champaign (USNWR #35)
- **Venue:** **arXiv (Jun 2024) — University of Illinois**
- **Relevance:** **Critical paper** — first proof that multi-agent LLM teams can exploit zero-day vulnerabilities with no prior knowledge. Hierarchical Planning and Task-Specific Agents (HPTSA) architecture is a direct ancestor of CMatrix's multi-agent design.

---

### 54. [LLM Agents Can Autonomously Exploit One-Day Vulnerabilities](https://arxiv.org/abs/2404.08144)
- **Authors:** **Richard Fang**, Rohan Bindu, Akul Gupta, Daniel Kang
- **Institution:** University of Illinois Urbana-Champaign (USNWR #35)
- **Venue:** **arXiv (Apr 2024) — University of Illinois**
- **Relevance:** The landmark paper proving GPT-4 agents can exploit 87% of real CVEs. Zero-shot capability on real-world vulnerabilities. CMatrix's core use case validated here first.

---

### 55. [AutoAttacker: A Large Language Model Guided System to Implement Automatic Cyber-attacks](https://arxiv.org/abs/2403.01038)
- **Authors:** **Jiacen Xu**, Jack W. Stokes, Geoff McDonald, Xuesong Bai, David Marshall, Siyue Wang, Adith Swaminathan, Zhou Li
- **Institution:** University of California, Irvine (USNWR #32)
- **Venue:** **arXiv (Mar 2024)**
- **Relevance:** Post-exploitation automation (keyboard-operated attacks) — the execution phase CMatrix's exploitation agent handles. AutoAttacker is an early direct ancestor.

---

### 56. [BreachSeek: A Multi-Agent Automated Penetration Tester](https://arxiv.org/abs/2409.03789)
- **Authors:** **Ibrahim AlShehri**, Adnan AlShehri, Abdulrahman AlMalki, Majed Bamardouf, Alaqsa Akbar
- **Institution:** King Fahd University of Petroleum and Minerals (USNWR #314)
- **Venue:** **arXiv (Sep 2024)**
- **Relevance:** Multi-agent pentest system, one of the first to use specialized agents for each phase — directly comparable architecture to CMatrix.

---

### 57. [Cybench: A Framework for Evaluating Cybersecurity Capabilities and Risks of Language Models](https://arxiv.org/abs/2408.08926)
- **Authors:** **Andy K. Zhang**, Neil Perry, Riya Dulepet, Joey Ji, Celeste Menders, Justin W. Lin, Eliot Jones, Gashon Hussein, Samantha Liu, Donovan Jasper, Pura Peetathawatchai, Ari Glenn, Vikram Sivashankar, Daniel Zamoshchin, Leo Glikbarg, Derek Askaryar, Mike Yang, Teddy Zhang, Rishi Alluri, Nathan Tran, Rinnara Sangpisit, Polycarpos Yiorkadjis, Kenny Osele, Gautham Raghupathi, Dan Boneh, Daniel E. Ho, Percy Liang
- **Institution:** Stanford University (USNWR #3)
- **Venue:** **arXiv (Aug 2024)**
- **Code:** [cybench.github.io](https://cybench.github.io/)
- **Relevance:** 40-challenge CTF benchmark with step-by-step subtasks — the de facto evaluation framework. CMatrix must report Cybench numbers in any published evaluation.

---

### 58. [HackSynth: LLM Agent and Evaluation Framework for Autonomous Penetration Testing](https://arxiv.org/abs/2412.01778)
- **Authors:** **Lajos Muzsai**, David Imolai, András Lukács
- **Institution:** Eötvös Loránd University (USNWR #485)
- **Venue:** **arXiv (Dec 2024)**
- **Code:** [GitHub](https://github.com/aielte-paper-research/HackSynth)
- **Relevance:** Single-agent pentest with iterative planning + feedback summarization loop — shows even a single well-designed agent can outperform complex systems. Baseline comparison for CMatrix.

---

### 59. [SoK: A Comparison of Autonomous Penetration Testing Agents](https://dl.acm.org/doi/10.1145/3664476.3664484)
- **Authors:** **Raphael Simon**, Wim Mees
- **Institution:** Royal Military Academy, Brussels
- **Venue:** **ARES 2024**
- **Relevance:** Systematization of knowledge paper — side-by-side comparison of all major autonomous pentest agents as of 2024. Essential for CMatrix's related work section.

---

### 60. [AutoPT: How Far Are We from the End2End Automated Web Penetration Testing?](https://arxiv.org/abs/2411.01236)
- **Authors:** **Benlong Wu**, Guoqiang Chen, Kejiang Chen, Xiuwei Shang, Jiapeng Han, Yanru He, Weiming Zhang, Nenghai Yu
- **Institution:** University of Science and Technology of China (USNWR #71)
- **Venue:** **arXiv (Nov 2024)**
- **Relevance:** Defines the gap between current LLM-based approaches and true end-to-end web pentest automation. Direct roadmap for what CMatrix aims to close.

---

### 61. [PENTEST-AI: An LLM-Powered Multi-Agents Framework for Penetration Testing Automation Leveraging MITRE ATT&CK](https://ieeexplore.ieee.org/abstract/document/10679480)
- **Authors:** **Stanislas G. Bianou**, Rodrigue G. Batogna
- **Institution:** Independent Researcher
- **Venue:** **IEEE CSR 2024**
- **Relevance:** MITRE ATT&CK-aligned multi-agent pentest system — directly validates CMatrix's planned ATT&CK integration for structured attack path planning.

---

### 62. [NYU CTF Bench: A Scalable Open-Source Benchmark Dataset for Evaluating LLMs in Offensive Security](https://proceedings.neurips.cc/paper_files/paper/2024/hash/69d97a6493fbf016fff0a751f253ad18-Abstract-Datasets_and_Benchmarks_Track.html)
- **Authors:** **Minghao Shao**, Sofija Jancheska, Meet Udeshi, Brendan Dolan-Gavitt, Haoran Xi, Kimberly Milner, Boyuan Chen, Max Yin, Siddharth Garg, Prashanth Krishnamurthy, Farshad Khorrami, Ramesh Karri, Muhammad Shafique
- **Institution:** New York University (USNWR #53)
- **Venue:** **NeurIPS 2024**
- **Code:** [GitHub](https://github.com/NYU-LLM-CTF/NYUCTFBench)
- **Relevance:** Standard dataset and runner evaluating offensive security CTF solving capabilities.

---

### 63. [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://arxiv.org/abs/2308.08155)
- **Authors:** **Qingyun Wu**, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shaokun Zhang, Jiale Liu, Ahmed Awadallah, Ryen W. White, Doug Burger, Chi Wang
- **Institution:** Penn State University (USNWR #130)
- **Venue:** **arXiv (Aug 2023 / 2024)**
- **Relevance:** Foundational multi-agent conversation framework. CMatrix's Master-Worker hierarchy is directly inspired by AutoGen agent orchestration and cooperation patterns.

---

### 64. [MetaGPT: Meta Programming for Multi-Agent Frameworks](https://arxiv.org/abs/2308.00352)
- **Authors:** **Sirui Hong**, Mingchen Zhuge, Jiaqi Chen, Xiawu Zheng, Yuheng Cheng, Ceyao Zhang, Jinlin Wang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin Wu, Jürgen Schmidhuber
- **Institution:** DeepWisdom
- **Venue:** **ICLR 2024**
- **Relevance:** Role-playing multi-agent architecture. Establishes SOPs for agent collaborations, which maps directly to specialized VAPT agent roles (Recon, Scan, Exploit) in CMatrix.

---

### 65. [AutoPenBench: Benchmarking Generative Agents for Penetration Testing](https://arxiv.org/abs/2410.03225)
- **Authors:** **Luca Gioacchini**, Marco Mellia, Idilio Drago, Alexander Delsanto, Giuseppe Siracusano, Roberto Bifulco
- **Institution:** Politecnico di Torino (USNWR #527)
- **Venue:** **arXiv (Oct 2024)**
- **Relevance:** Standard evaluation benchmark utilizing 33 vulnerable Docker containers. Used to measure and optimize CMatrix's execution-layer exploit success rate.

---

## `2023 Papers`

### 66. [PenHeal: A Two-Stage LLM Framework for Automated Pentesting and Optimal Remediation](https://arxiv.org/abs/2407.17788)
- **Authors:** **Junjie Huang**, Quanyan Zhu
- **Institution:** New York University Shanghai (USNWR #53)
- **Venue:** **ACM CCS 2023 (Workshop on Autonomous Cybersecurity)**
- **Relevance:** First CCS paper combining automated pentesting + remediation recommendation — defines the detect-then-fix loop CMatrix's reporting module should implement.

---

### 67. [Getting pwn'd by AI: Penetration Testing with Large Language Models](https://dl.acm.org/doi/abs/10.1145/3611643.3613083)
- **Authors:** **Andreas Happe**, Jürgen Cito
- **Institution:** TU Wien (USNWR #334)
- **Venue:** **ESEC/FSE 2023**
- **Code:** [GitHub](https://github.com/ipa-lab/hackingBuddyGPT)
- **Relevance:** One of the earliest serious academic treatments of LLM-based pentesting. Establishes the foundational argument and methodology that all later work (including PentestGPT) builds upon. FSE is CCF-A.

---

### 68. [Language Agents as Hackers: Evaluating Cybersecurity Skills with Capture the Flag](https://arxiv.org/abs/2308.10443)
- **Authors:** **Wesley Tann**, Yuancheng Liu, Jun Heng Sim, Choon Meng Seah, Ee-Chien Chang
- **Institution:** National University of Singapore (USNWR #22)
- **Venue:** **MASEC Workshop @ NeurIPS 2023**
- **Relevance:** First serious CTF evaluation of LLM agents as offensive security actors — the origin paper for the CTF-as-benchmark paradigm that CMatrix's evaluation will use.

---

### 69. [ReAct: Synergizing Reasoning and Acting in LLMs](https://arxiv.org/abs/2210.03629)
- **Authors:** **Shunyu Yao**, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao
- **Institution:** Princeton University (USNWR #1)
- **Venue:** **ICLR 2023**
- **Relevance:** The standard action-reasoning loop. Informs CMatrix's core terminal and execution agents on command generation and response evaluation.

---

### 70. [Tree of Thoughts: Deliberate Problem Solving with LLMs](https://arxiv.org/abs/2305.10601)
- **Authors:** **Shunyu Yao**, Dian Yu, Thomas L. Griffiths, Jeffrey Zhao, Yuan Cao, Izhak Shafran, Karthik Narasimhan
- **Institution:** Princeton University (USNWR #1)
- **Venue:** **NeurIPS 2023**
- **Relevance:** Advanced tree search and backtracking over planning nodes. Highly relevant for multi-step penetration testing campaign planning and vulnerability exploration.

---

### 71. [Reflexion: Language Agents with Verbal RL](https://arxiv.org/abs/2303.11366)
- **Authors:** **Noah Shinn**, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao
- **Institution:** Northeastern University (USNWR #179)
- **Venue:** **NeurIPS 2023**
- **Relevance:** Self-reflection loops allowing agents to evaluate exploit execution failures and iteratively refine payloads.

---

## `2022 Papers`

### 72. [Chain-of-Thought Prompting Elicits Reasoning in LLMs](https://arxiv.org/abs/2201.11903)
- **Authors:** **Jason Wei**, Brian Ichter, Xuezhi Wang, Fei Xia, Dale Schuurmans, Ed H. Chi, Quoc V. Le, Maarten Bosma, Denny Zhou
- **Institution:** Google Research
- **Venue:** **NeurIPS 2022**
- **Relevance:** Elicits complex reasoning by generating intermediate steps. Essential base planning logic for all CMatrix agents.

---
