# Curated Research Papers — 27 Papers (Final Selection)

> **Scope:** Papers directly relevant to our work — LLM-based agentic pentesting,
> multi-agent red-team orchestration, autonomous vulnerability exploitation, offensive security
> benchmarks, and agentic cybersecurity systems. Ordered from **most recent → oldest**.
> Quality filter: CCF-A/B venues, major arXiv preprints with 50+ citations, or direct architectural
> equivalents.

---

## `2026 Papers`

### 1. HackWorld: Evaluating Computer-Use Agents on Exploiting Web Application Vulnerabilities
- **Website:** [🌐 Link](https://arxiv.org/abs/2510.12200)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/01-hackworld-evaluating-computer-use-agents-on-exploiting-web.pdf)
- **Code:** [GitHub](https://github.com/GUI-Agent/HackWorld)
- **Authors:** **Xiaoxue Ren**, Penghao Jiang, Kaixin Li, Zhiyong Huang, Xiaoning Du, Jiaojiao Jiang, Zhenchang Xing, Jiamou Sun, Terry Yue Zhuo
- **Institution:** Zhejiang University (USNWR #45)
- **Venue:** **ICLR 2026**
- **Relevance:** Evaluates GUI/computer-use LLM agents autonomously attacking real web application vulnerabilities — directly maps to CMatrix's black-box scan mode and web vuln pipeline. Uses the same agent-environment loop that CMatrix's VS Code-style terminal UI embodies.

---

### 2. What Makes a Good LLM Agent for Real-world Penetration Testing?
- **Website:** [🌐 Link](https://arxiv.org/abs/2602.17622)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/02-what-makes-a-good-llm-agent-for-real-world-penetration.pdf)
- **Authors:** **Gelei Deng**, Yi Liu, Yuekang Li, Ruozhao Yang, Xiaofei Xie, Jie Zhang, Han Qiu, Tianwei Zhang
- **Institution:** Nanyang Technological University (USNWR #28)
- **Venue:** **arXiv (Feb 2026)**
- **Relevance:** PentestGPT V2 paper — empirically identifies what agent properties (planning, memory, tool use) matter most for real-world pentest. Achieves 76.9% (10/13 machines) on HackTheBox. Directly comparable to CMatrix's evaluation framework design.

---

### 3. Co-RedTeam: Orchestrated Security Discovery and Exploitation with LLM Agents
- **Website:** [🌐 Link](https://arxiv.org/abs/2602.02164)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/03-co-redteam-orchestrated-security-discovery-and-exploitation.pdf)
- **Authors:** **Pengfei He**, Ash Fox, Lesly Miculicich, Stefan Friedli, Daniel Fabian, Burak Gokturk, Jiliang Tang, Chen-Yu Lee, Tomas Pfister, Long T. Le
- **Institution:** Google Cloud AI Research
- **Venue:** **arXiv (Feb 2026) — Google Cloud AI Research**
- **Relevance:** Multi-agent red team with specialized roles (discovery agent, exploitation agent, critic agent) and structured interaction — architecturally almost identical to CMatrix's reconnaissance-scan-exploit pipeline. Google-authored.

---

### 4. AWE: Adaptive Agents for Dynamic Web Penetration Testing
- **Website:** [🌐 Link](https://www.ndss-symposium.org/ndss-paper/auto-draft-680/)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/04-awe-adaptive-agents-for-dynamic-web-penetration-testing.pdf)
- **Code:** [GitHub](https://github.com/stuxlabs/AWE)
- **Authors:** **Akshat Singh Jaswal**, Ashish Baghel
- **Institution:** Stux Labs
- **Venue:** **NDSS 2026**
- **Relevance:** Adaptive agents designed specifically for dynamic web penetration testing — highly relevant to CMatrix's web agent architecture.

---

### 5. Can LLMs Hack Enterprise Networks? Autonomous Assumed Breach Penetration-Testing Active Directory Networks
- **Website:** [🌐 Link](https://dl.acm.org/doi/abs/10.1145/3766895)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/05-can-llms-hack-enterprise-networks-autonomous-assumed-breach.pdf)
- **Code:** [GitHub](https://github.com/andreashappe/cochise)
- **Authors:** **Andreas Happe**, Jürgen Cito
- **Institution:** TU Wien (USNWR #334)
- **Venue:** **TOSEM 2025 (ACM Transactions on Software Engineering and Methodology)**
- **Relevance:** Enterprise AD network pentest — closest to CMatrix's grey-box scan mode and multi-host lateral movement scenarios. Top journal publication.

---

### 6. PentestAgent: Incorporating LLM Agents to Automated Penetration Testing
- **Website:** [🌐 Link](https://arxiv.org/abs/2411.05185)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/06-pentestagent-incorporating-llm-agents-to-automated.pdf)
- **Code:** [GitHub](https://github.com/GH05TCREW/PentestAgent)
- **Authors:** **Xiangmin Shen**, Lingzhi Wang, Zhenyuan Li, Yan Chen, Wencheng Zhao, Dawei Sun, Jiashui Wang
- **Institution:** Northwestern University (USNWR #9)
- **Venue:** **AsiaCCS 2025**
- **Relevance:** Fully autonomous multi-agent pentesting, competes directly with CMatrix. Evaluated against VulHub + HackTheBox. Strongest direct architectural competitor.

---

### 7. PentestGPT: Evaluating and Harnessing Large Language Models for Automated Penetration Testing
- **Website:** [🌐 Link](https://arxiv.org/abs/2308.06782)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/09-pentestgpt-evaluating-and-harnessing-large-language-models-for-automated-penetration-testing.pdf)
- **Authors:** **Gelei Deng**, Yi Liu, Víctor Mayoral-Vilches, Peng Liu, Yuekang Li, Yuan Xu, Tianwei Zhang, Yang Liu, Martin Ochoa, Stefan Savage
- **Institution:** Nanyang Technological University (USNWR #28)
- **Venue:** **USENIX Security 2024**
- **Relevance:** Defines the canonical three-module (Reasoning · Generation · Parsing) LLM pentesting architecture. The highest-impact published paper in the field; every subsequent network pentesting agent cites or differentiates from it. CMatrix's Commander-Specialist pattern is a direct evolution of this decomposition.

---

### 8. VulnBot: Autonomous Penetration Testing for a Multi-Agent Collaborative Framework
- **Website:** [🌐 Link](https://arxiv.org/abs/2501.13411)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/07-vulnbot-autonomous-penetration-testing-for-a-multi-agent.pdf)
- **Code:** [GitHub](https://github.com/KHenryAegis/VulnBot)
- **Authors:** **He Kong**, Die Hu, Jingguo Ge, Liangxiong Li, Tong Li, Bingzhen Wu
- **Institution:** Institute of Information Engineering, Chinese Academy of Sciences
- **Venue:** **arXiv (Jan 2025)**
- **Relevance:** Role-specialized multi-agent framework (recon, scan, exploit) with penetration task graph (PTG) for logical execution — the closest existing architectural match to CMatrix's LangGraph pipeline design.

---

### 9. Incalmo: An Autonomous LLM-assisted System for Red Teaming Multi-Host Networks
- **Website:** [🌐 Link](https://arxiv.org/abs/2501.16466)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/08-incalmo-an-autonomous-llm-assisted-system-for-red-teaming.pdf)
- **Code:** [GitHub](https://github.com/bsinger98/Incalmo)
- **Authors:** **Brian Singer**, Keane Lucas, Lakshmi Adiga, Meghna Jain, Lujo Bauer, Vyas Sekar
- **Institution:** Carnegie Mellon University (USNWR #22)
- **Venue:** **arXiv (Jan 2025, multiple revisions through Nov 2025)**
- **Relevance:** Multi-host red teaming with abstract action layer — compromised 9/10 mobile-core testbeds (25–50 hosts). Directly comparable to CMatrix's multi-target scan mode.

---

### 10. D-CIPHER: Dynamic Collaborative Intelligent Multi-Agent System with Planner and Heterogeneous Executors for Offensive Security
- **Website:** [🌐 Link](https://arxiv.org/abs/2502.10931)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/10-d-cipher-dynamic-collaborative-intelligent-multi-agent.pdf)
- **Authors:** **Meet Udeshi**, Minghao Shao, Haoran Xi, Kimberly Milner, Venkata Sai Charan Putrevu, Brendan Dolan-Gavitt, Prashanth Krishnamurthy, Farshad Khorrami, Ramesh Karri, Muhammad Shafique, Nanda Rani, Sandeep K. Shukla
- **Institution:** NYU Tandon (USNWR #53)
- **Venue:** **arXiv (Feb 2025)**
- **Relevance:** Planner-executor multi-agent system with heterogeneous specialized agents for CTF — directly informs CMatrix's agent role decomposition and inter-agent communication protocol.

---

### 11. Automated Penetration Testing with LLM Agents and Classical Planning
- **Website:** [🌐 Link](https://arxiv.org/abs/2512.11143)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/11-automated-penetration-testing-with-llm-agents-and-classical.pdf)
- **Authors:** **Lingzhi Wang**, Xinyi Shi, Ziyu Li, Yi Jiang, Shiyu Tan, Yuhao Jiang, Junjie Cheng, Wenyuan Chen, Xiangmin Shen, Zhenyuan Li, Yan Chen
- **Institution:** Northwestern University (USNWR #9)
- **Venue:** **arXiv (Dec 2025)**
- **Relevance:** Combines classical planning (symbolic AI) with LLM agents for structured pentest execution — hybrid approach that CMatrix could adopt to reduce hallucination in multi-step exploit chains.

---

### 12. Multi-Agent Penetration Testing AI for the Web
- **Website:** [🌐 Link](https://arxiv.org/abs/2508.20816)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/12-multi-agent-penetration-testing-ai-for-the-web.pdf)
- **Authors:** **Isaac David**, Arthur Gervais
- **Institution:** University College London (USNWR #7)
- **Venue:** **arXiv (Aug 2025)**
- **Relevance:** Web-specific multi-agent pentest — CMatrix's primary initial attack surface. Detailed agent decomposition for web recon, injection, exploitation.

---

### 13. Forewarned is Forearmed: A Survey on LLM-based Agents in Autonomous Cyberattacks
- **Website:** [🌐 Link](https://arxiv.org/abs/2505.12786)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/13-forewarned-is-forearmed-a-survey-on-llm-based-agents-in.pdf)
- **Authors:** **Minrui Xu**, Jiani Fan, Xinyu Huang, Conghao Zhou, Jiawen Kang, Dusit Niyato, Shiwen Mao, Zhu Han, Xuemin (Sherman) Shen, Kwok-Yan Lam
- **Institution:** Nanyang Technological University (USNWR #28)
- **Venue:** **arXiv (May 2025)**
- **Relevance:** Comprehensive survey on offensive LLM agent capabilities across all attack stages. The reference survey most aligned with CMatrix's scope. Covers recon, exploitation, lateral movement, persistence.

---

### 14. BountyBench: Dollar Impact of AI Agent Attackers and Defenders on Real-World Cybersecurity Systems
- **Website:** [🌐 Link](https://arxiv.org/abs/2505.15216)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/14-bountybench-dollar-impact-of-ai-agent-attackers-and.pdf)
- **Code:** [bountybench.github.io](https://bountybench.github.io)
- **Authors:** **Andy K. Zhang**, Joey Ji, Celeste Menders, Riya Dulepet, Thomas Qin, Ron Y. Wang, Junrong Wu, Kyleen Liao, Jiliang Li, Jinghan Hu, Sara Hong, Nardos Demilew, Shivatmica Murgai, Jason Tran, Nishka Kacheria, Ethan Ho, Denis Liu, Lauren McLane, Olivia Bruvik, Dai-Rong Han, Seungwoo Kim, Akhil Vyas, Cuiyuanxiu Chen, Ryan Li, Weiran Xu, Jonathan Z. Ye, Prerit Choudhary, Siddharth M. Bhatia, Vikram Sivashankar, Yuxuan Bao, Dawn Song, Dan Boneh, Daniel E. Ho, Percy Liang
- **Institution:** Stanford University (USNWR #3)
- **Venue:** **NeurIPS 2025 (Datasets and Benchmarks Track) — Stanford / UC Berkeley**
- **Relevance:** First benchmark to quantify AI agent cyber-capability in real dollar terms. 25 production systems, 40 bounties ($10–$30,485), covering 9 OWASP Top 10 risks. Defines Detect/Exploit/Patch task taxonomy — precisely the three phases CMatrix automates. Evaluated DeepSeek-R1 among 10 agents, giving CMatrix a direct reference point for its backbone model.

---

### 15. PentestEval: Benchmarking LLM-based Penetration Testing with Modular and Stage-Level Design
- **Website:** [🌐 Link](https://arxiv.org/abs/2512.14233)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/15-pentesteval-benchmarking-llm-based-penetration-testing.pdf)
- **Authors:** **Ruozhao Yang**, Mingfei Cheng, Gelei Deng, Tianwei Zhang, Junjie Wang, Xiaofei Xie
- **Institution:** Singapore Management University (USNWR #616)
- **Venue:** **arXiv (Dec 2025)**
- **Relevance:** Benchmarking platform designed to evaluate stage-level and modular penetration testing behaviors in LLM agents.

---

### 16. Teams of LLM Agents Can Exploit Zero-Day Vulnerabilities
- **Website:** [🌐 Link](https://arxiv.org/abs/2406.01637)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/16-teams-of-llm-agents-can-exploit-zero-day-vulnerabilities.pdf)
- **Authors:** **Yuxuan Zhu**, Antony Kellermann, Akul Gupta, Philip Li, Richard Fang, Rohan Bindu, Daniel Kang
- **Institution:** University of Illinois Urbana-Champaign (USNWR #35)
- **Venue:** **arXiv (Jun 2024) — University of Illinois**
- **Relevance:** **Critical paper** — first proof that multi-agent LLM teams can exploit zero-day vulnerabilities with no prior knowledge. Hierarchical Planning and Task-Specific Agents (HPTSA) architecture is a direct ancestor of CMatrix's multi-agent design.

---

### 17. LLM Agents Can Autonomously Exploit One-Day Vulnerabilities
- **Website:** [🌐 Link](https://arxiv.org/abs/2404.08144)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/17-llm-agents-can-autonomously-exploit-one-day-vulnerabilities.pdf)
- **Authors:** **Richard Fang**, Rohan Bindu, Akul Gupta, Daniel Kang
- **Institution:** University of Illinois Urbana-Champaign (USNWR #35)
- **Venue:** **arXiv (Apr 2024) — University of Illinois**
- **Relevance:** The landmark paper proving GPT-4 agents can exploit 87% of real CVEs. Zero-shot capability on real-world vulnerabilities. CMatrix's core use case validated here first.

---

### 18. Cybench: A Framework for Evaluating Cybersecurity Capabilities and Risks of Language Models
- **Website:** [🌐 Link](https://arxiv.org/abs/2408.08926)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/18-cybench-a-framework-for-evaluating-cybersecurity.pdf)
- **Code:** [cybench.github.io](https://cybench.github.io/)
- **Authors:** **Andy K. Zhang**, Neil Perry, Riya Dulepet, Joey Ji, Celeste Menders, Justin W. Lin, Eliot Jones, Gashon Hussein, Samantha Liu, Donovan Jasper, Pura Peetathawatchai, Ari Glenn, Vikram Sivashankar, Daniel Zamoshchin, Leo Glikbarg, Derek Askaryar, Mike Yang, Teddy Zhang, Rishi Alluri, Nathan Tran, Rinnara Sangpisit, Polycarpos Yiorkadjis, Kenny Osele, Gautham Raghupathi, Dan Boneh, Daniel E. Ho, Percy Liang
- **Institution:** Stanford University (USNWR #3)
- **Venue:** **arXiv (Aug 2024)**
- **Relevance:** 40-challenge CTF benchmark with step-by-step subtasks — the de facto evaluation framework. CMatrix must report Cybench numbers in any published evaluation.

---

### 19. AutoPT: How Far Are We from the End2End Automated Web Penetration Testing?
- **Website:** [🌐 Link](https://arxiv.org/abs/2411.01236)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/20-autopt-how-far-are-we-from-the-end2end-automated-web.pdf)
- **Authors:** **Benlong Wu**, Guoqiang Chen, Kejiang Chen, Xiuwei Shang, Jiapeng Han, Yanru He, Weiming Zhang, Nenghai Yu
- **Institution:** University of Science and Technology of China (USNWR #71)
- **Venue:** **arXiv (Nov 2024)**
- **Relevance:** Defines the gap between current LLM-based approaches and true end-to-end web pentest automation. Direct roadmap for what CMatrix aims to close.

---

### 20. AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation
- **Website:** [🌐 Link](https://arxiv.org/abs/2308.08155)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/21-autogen-next-gen-llm-multi-agent-conversations.pdf)
- **Authors:** **Qingyun Wu**, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shaokun Zhang, Jiale Liu, Ahmed Awadallah, Ryen W. White, Doug Burger, Chi Wang
- **Institution:** Penn State University (USNWR #130)
- **Venue:** **arXiv (Aug 2023 / 2024)**
- **Relevance:** Foundational multi-agent conversation framework. CMatrix's Master-Worker hierarchy is directly inspired by AutoGen agent orchestration and cooperation patterns.

---

### 21. MetaGPT: Meta Programming for Multi-Agent Frameworks
- **Website:** [🌐 Link](https://arxiv.org/abs/2308.00352)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/22-metagpt-meta-programming-for-multi-agent-frameworks.pdf)
- **Authors:** **Sirui Hong**, Mingchen Zhuge, Jiaqi Chen, Xiawu Zheng, Yuheng Cheng, Ceyao Zhang, Jinlin Wang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin Wu, Jürgen Schmidhuber
- **Institution:** DeepWisdom
- **Venue:** **ICLR 2024**
- **Relevance:** Role-playing multi-agent architecture. Establishes SOPs for agent collaborations, which maps directly to specialized VAPT agent roles (Recon, Scan, Exploit) in CMatrix.

---

### 22. Getting pwn'd by AI: Penetration Testing with Large Language Models
- **Website:** [🌐 Link](https://dl.acm.org/doi/abs/10.1145/3611643.3613083)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/23-getting-pwnd-by-ai-penetration-testing-with-large-language.pdf)
- **Code:** [GitHub](https://github.com/ipa-lab/hackingBuddyGPT)
- **Authors:** **Andreas Happe**, Jürgen Cito
- **Institution:** TU Wien (USNWR #334)
- **Venue:** **ESEC/FSE 2023**
- **Relevance:** One of the earliest serious academic treatments of LLM-based pentesting. Establishes the foundational argument and methodology that all later work (including PentestGPT) builds upon. FSE is CCF-A.

---

### 23. Reflexion: Language Agents with Verbal RL
- **Website:** [🌐 Link](https://arxiv.org/abs/2303.11366)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/24-reflexion-language-agents-with-verbal-rl.pdf)
- **Authors:** **Noah Shinn**, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao
- **Institution:** Northeastern University (USNWR #179)
- **Venue:** **NeurIPS 2023**
- **Relevance:** Self-reflection loops allowing agents to evaluate exploit execution failures and iteratively refine payloads.

---


### 24. Voyager: An Open-Ended Embodied Agent with Large Language Models
- **Website:** [🌐 Link](https://arxiv.org/abs/2305.16291)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/25-voyager-an-open-ended-embodied-agent.pdf)
- **Authors:** **Guanzhi Wang**, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, Anima Anandkumar
- **Institution:** NVIDIA / Caltech / Stanford
- **Venue:** **NeurIPS 2023**
- **Relevance:** Attack Strategy Library: Voyager's persistent, ever-growing skill library — where completed tasks are crystallized into reusable code skills stored in a vector DB and retrieved at task-start — is the direct conceptual ancestor of CMatrix's technology-fingerprint-indexed attack strategy crystallization.

---

### 25. A Survey on Large Language Model based Autonomous Agents
- **Website:** [🌐 Link](https://arxiv.org/abs/2308.11432)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/26-a-survey-on-large-language-model-based-autonomous-agents.pdf)
- **Authors:** **Lei Wang**, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang, Xu Chen, Yankai Lin, Wayne Xin Zhao, Zhewei Wei, Ji-Rong Wen
- **Institution:** Renmin University of China
- **Venue:** **Frontiers of Computer Science 2024**
- **Relevance:** General agent architecture: Establishes the canonical 4-module agent taxonomy (Profile · Memory · Planning · Action) used as background vocabulary in every agent paper.

---

### 26. PrediQL: Automated Testing of GraphQL APIs with LLMs
- **Website:** [🌐 Link](https://arxiv.org/abs/2510.10407)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/27-prediql-automated-testing-of-graphql-apis-with-llms.pdf)
- **Authors:** **Zhenyu Cheng**, Linxi Fan, Anima Anandkumar
- **Institution:** Chinese Academy of Sciences
- **Venue:** **WWW 2026**
- **Relevance:** GraphQL LLM Fuzzing: Essential API testing foundation for CMatrix's API scanning capabilities.

---

### 27. RESTler: Stateful REST API Fuzzing
- **Website:** [🌐 Link](https://doi.org/10.1145/3213846.3213851)
- **Paper:** [📄 Local PDF](../downloaded-paper-curated/28-restler-stateful-rest-api-fuzzing.pdf)
- **Authors:** **Vaggelis Atlidakis**, Patrice Godefroid, Marina Polishchuk
- **Institution:** Columbia University / Microsoft
- **Venue:** **ICSE 2019**
- **Relevance:** Stateful REST API Fuzzing: Provides baseline methodology and strategies for the REST API module in CMatrix's API penetration testing capabilities.

---

## `2022 Papers`
