# CMatrix — Final Definitive Paper List
**Research:** LLM-Orchestrated Multi-Agent Framework for Autonomous VAPT  
**Attack Surfaces:** Web · API · Network  
**Total: 27 papers**

> **Legend:**  
> ✅ **IN LIBRARY** = already in `docs/paper-research/md-downloaded-paper-curated/`  
> 🗑️ **DROPPED** = in library but excluded (see drop table at end)

---

## SECTION 1 — NETWORK PENTESTING
*The VAPT agent papers focused on network infrastructure: reconnaissance, service exploitation, CVE chaining, lateral movement, shell acquisition. This is where all prior LLM-agent VAPT research has concentrated — CMatrix builds on and differentiates from all of these.*

| # | Status | File | Paper | Surface | Unique Contribution |
|---|---|---|---|---|---|
| 1 | ✅ | [📄 `22-getting-pwnd-by-ai-penetration-testing-with-large-language.pdf`](paper-research/downloaded-paper-curated/22-getting-pwnd-by-ai-penetration-testing-with-large-language.pdf) | **Getting pwn'd by AI** — Happe & Cito, ESEC/FSE 2023 | 🕸️ Network | First closed-loop LLM→shell agent. Foundational baseline. Every paper cites this. |
| 2 | ✅ | [📄 `09-pentestgpt-evaluating-and-harnessing-large-language-models-for-automated-penetration-testing.pdf`](paper-research/downloaded-paper-curated/09-pentestgpt-evaluating-and-harnessing-large-language-models-for-automated-penetration-testing.pdf) | **PentestGPT** — Deng et al., USENIX Security 2024 | 🕸️ Network | Three-module Reasoning/Generation/Parsing architecture. USENIX — highest impact published paper in field. |
| 3 | ✅ | [📄 `02-what-makes-a-good-llm-agent-for-real-world-penetration.pdf`](paper-research/downloaded-paper-curated/02-what-makes-a-good-llm-agent-for-real-world-penetration.pdf) | **PentestGPT V2 / What Makes a Good LLM Agent** — Deng et al., NTU 2025 | 🕸️ Network | Evidence-Guided Attack Tree Search (EGATS) + Task Difficulty Assessment (TDA). 91% CTF completion. Best analysis of failure modes (Type A vs Type B). The evolution of PentestGPT you cannot ignore. |
| 4 | ✅ | [📄 `07-vulnbot-autonomous-penetration-testing-for-a-multi-agent.pdf`](paper-research/downloaded-paper-curated/07-vulnbot-autonomous-penetration-testing-for-a-multi-agent.pdf) | **VulnBot** — He et al., 2025 | 🕸️ Network | Penetration task graph driving role-specific agents. Best task-graph-driven multi-agent for network. |
| 5 | ✅ | [📄 `06-pentestagent-incorporating-llm-agents-to-automated.pdf`](paper-research/downloaded-paper-curated/06-pentestagent-incorporating-llm-agents-to-automated.pdf) | **PentestAgent** — Zhang et al., 2024 | 🕸️ Network + 🌐 Web (partial) | First to integrate knowledge retrieval (RAG) + specialized agents end-to-end. |
| 6 | ✅ | [📄 `11-automated-penetration-testing-with-llm-agents-and-classical.pdf`](paper-research/downloaded-paper-curated/11-automated-penetration-testing-with-llm-agents-and-classical.pdf) | **CHECKMATE** — Wang et al. (Northwestern/Zhejiang), 2025 | 🕸️ Network | PEP (Planner-Executor-Perceptor) paradigm. +20% over Claude Code. Best current SotA for structured planning + LLM. |
| 7 | ✅ | [📄 `10-d-cipher-dynamic-collaborative-intelligent-multi-agent.pdf`](paper-research/downloaded-paper-curated/10-d-cipher-dynamic-collaborative-intelligent-multi-agent.pdf) | **D-CIPHER** — Udeshi et al. (NYU), 2025 | 🕸️ Network | Heterogeneous executors + auto-prompter. SotA: Cybench 22.5%, HackTheBox 44%. MITRE ATT&CK mapped. |
| 8 | ✅ | [📄 `08-incalmo-an-autonomous-llm-assisted-system-for-red-teaming.pdf`](paper-research/downloaded-paper-curated/08-incalmo-an-autonomous-llm-assisted-system-for-red-teaming.pdf) | **Incalmo** — Singer et al. (CMU), 2025 | 🕸️ Network (Enterprise Multi-Host) | Only paper on autonomous enterprise multi-host red teaming. MHBench (40 real networks). 37/40 success. |
| 9 | ✅ | [📄 `05-can-llms-hack-enterprise-networks-autonomous-assumed-breach.pdf`](paper-research/downloaded-paper-curated/05-can-llms-hack-enterprise-networks-autonomous-assumed-breach.pdf) | **Can LLMs Hack Enterprise Networks?** — Happe & Cito, ACM 2025 | 🕸️ Network (Enterprise) | Empirical Planner-Executor on real enterprise testbed. LLM comparison: GPT-4o, Gemini, o1, Qwen3. |
| 10 | ✅ | [📄 `03-co-redteam-orchestrated-security-discovery-and-exploitation.pdf`](paper-research/downloaded-paper-curated/03-co-redteam-orchestrated-security-discovery-and-exploitation.pdf) | **Co-RedTeam** — He et al. (Google), 2025 | 🌐 Web + 🕸️ Network | **Google's multi-agent red-teaming framework.** OWASP/CWE-grounded agents, execution-driven reasoning, long-term memory. 60%+ exploitation on BountyBench + CyberGym. Strongest framework covering BOTH Web and Network with a unified pipeline. |

---

## SECTION 2 — WEB APPLICATION PENTESTING
*These specifically address OWASP-class web vulnerabilities with LLM agents.*

| # | Status | File | Paper | Surface | Unique Contribution |
|---|---|---|---|---|---|
| 11 | ✅ | [📄 `17-llm-agents-can-autonomously-exploit-one-day-vulnerabilities.pdf`](paper-research/downloaded-paper-curated/17-llm-agents-can-autonomously-exploit-one-day-vulnerabilities.pdf) | **LLM Agents can Autonomously Exploit One-Day Vulnerabilities** — Fang et al. (UIUC), 2024 | 🌐 Web | The seminal web hacking paper. GPT-4 exploiting real web CVEs (SQLi, RCE, auth bypass). 87% on 15 CVEs. Academic foundation for your Web surface claim. |
| 12 | ✅ | [📄 `16-teams-of-llm-agents-can-exploit-zero-day-vulnerabilities.pdf`](paper-research/downloaded-paper-curated/16-teams-of-llm-agents-can-exploit-zero-day-vulnerabilities.pdf) | **Teams of LLM Agents can Exploit Zero-Day Vulnerabilities** — Fang et al. (UIUC), 2024 | 🌐 Web | Zero-day web multi-agent (HPTSA). Extends #11 to zero-day. First multi-agent web zero-day system. |
| 13 | ✅ | [📄 `12-multi-agent-penetration-testing-ai-for-the-web.pdf`](paper-research/downloaded-paper-curated/12-multi-agent-penetration-testing-ai-for-the-web.pdf) | **MAPTA: Multi-Agent Penetration Testing AI for the Web** — David & Gervais (UCL), arXiv Aug 2025 | 🌐 Web + 🔌 API (REST partial) | Most complete open-source web pentesting framework. XBOW 104-challenge benchmark: 76.9% overall. Covers SQLi, XSS, SSRF, broken auth, SSTI. Includes REST/API fuzzing section. |
| 14 | ✅ | [📄 `04-awe-adaptive-agents-for-dynamic-web-penetration-testing.pdf`](paper-research/downloaded-paper-curated/04-awe-adaptive-agents-for-dynamic-web-penetration-testing.pdf) | **AWE: Adaptive Agents for Dynamic Web Penetration Testing** — Jaswal & Baghel (Stux Labs), **NDSS Workshop (LAST-X) 2026** | 🌐 Web | Memory-augmented, vuln-specific pipelines. 87% XSS (+30.5% over MAPTA), 66.7% blind SQLi (+33.3%). Best injection-class depth. |
| 15 | ✅ | [📄 `19-autopt-how-far-are-we-from-the-end2end-automated-web.pdf`](paper-research/downloaded-paper-curated/19-autopt-how-far-are-we-from-the-end2end-automated-web.pdf) | **AutoPT: End2End Automated Web Penetration Testing** — Wu et al. (USTC/ACM), 2024 | 🌐 Web | First end-to-end web pentest benchmark. Penetration State Machine (PSM) — FSM-driven LLM. 22%→41% on GPT-4o mini. ACM published. |
| 16 | ✅ | [📄 `01-hackworld-evaluating-computer-use-agents-on-exploiting-web.pdf`](paper-research/downloaded-paper-curated/01-hackworld-evaluating-computer-use-agents-on-exploiting-web.pdf) | **HackWorld: Evaluating Computer-Use Agents on Web Vulnerabilities** — Ren et al. (Zhejiang/NUS/Monash/CSIRO), **under review ICLR 2026** | 🌐 Web | 36-app web benchmark, 11 frameworks, 7 languages. Tests visual/GUI exploitation (CUAs). Injection flaws, auth bypasses. |

---

## SECTION 3 — API SECURITY

| # | Status | File | Paper | arXiv / Venue | Surface | Unique Contribution |
|---|---|---|---|---|---|---|
| 17 | ✅ | [📄 `26-prediql-automated-testing-of-graphql-apis-with-llms.pdf`](paper-research/downloaded-paper-curated/26-prediql-automated-testing-of-graphql-apis-with-llms.pdf) | **PrediQL: Automated Testing of GraphQL APIs with LLMs** — Liu et al., **The Web Conference (WWW) 2026** | WWW 2026 | 🔌 API (GraphQL) | **Only peer-reviewed paper targeting GraphQL API security with LLMs.** LLM + RAG + multi-armed bandit for adaptive fuzzing. Access-control bypass, injection, info disclosure in GraphQL. |
| 18 | ✅ | [📄 `27-restler-stateful-rest-api-fuzzing.pdf`](paper-research/downloaded-paper-curated/27-restler-stateful-rest-api-fuzzing.pdf) | **RESTler: Stateful REST API Fuzzing** — Atlidakis et al. (Microsoft), ICSE 2019 | ICSE 2019 (ACM) | 🔌 API (REST) | **The foundational REST API fuzzing baseline.** Producer-consumer dependency inference from OpenAPI spec. Bugs found in Azure, Office 365, GitLab. Cite as the pre-LLM baseline that CMatrix supersedes. |




---

## SECTION 4 — MULTI-AGENT ARCHITECTURE FOUNDATIONS
*Justify your orchestration design choices.*

| # | Status | File | Paper | Unique Contribution |
|---|---|---|---|---|
| 21 | ✅ | [📄 `20-autogen-next-gen-llm-multi-agent-conversations.pdf`](paper-research/downloaded-paper-curated/20-autogen-next-gen-llm-multi-agent-conversations.pdf) | **AutoGen** — Wu et al. (Microsoft Research), 2023 | Most cited multi-agent conversation framework. Direct predecessor/comparator to your orchestrator. |
| 22 | ✅ | [📄 `21-metagpt-meta-programming-for-multi-agent-frameworks.pdf`](paper-research/downloaded-paper-curated/21-metagpt-meta-programming-for-multi-agent-frameworks.pdf) | **MetaGPT: Meta Programming for Multi-Agent Frameworks** — ICLR 2024 | Role-based agents with structured SOP communication. Directly justifies your role assignment design (Recon, Web, API, Network, Orchestrator agents). |

---

## SECTION 5 — AGENT REASONING FOUNDATIONS
*Papers whose mechanisms are directly implemented inside CMatrix's agent architecture.*

| # | Status | File | Paper | Venue | Maps To CMatrix |
|---|---|---|---|---|---|
| 19 | ✅ | [📄 `24-voyager-an-open-ended-embodied-agent.pdf`](paper-research/downloaded-paper-curated/24-voyager-an-open-ended-embodied-agent.pdf) | **Voyager: An Open-Ended Embodied Agent with Large Language Models** — Wang et al. (NVIDIA/Stanford/UT Austin), 2023 | **NeurIPS 2023** | **Attack Strategy Library** (§6, C11): Voyager's persistent, ever-growing skill library — where completed tasks are crystallized into reusable code skills stored in a vector DB and retrieved at task-start — is the direct conceptual ancestor of CMatrix's technology-fingerprint-indexed attack strategy crystallization. CMatrix domain-constrains the mechanism to security exploitation procedures with confidence scoring. |
| 20 | ✅ | [📄 `23-reflexion-language-agents-with-verbal-rl.pdf`](paper-research/downloaded-paper-curated/23-reflexion-language-agents-with-verbal-rl.pdf) | **Reflexion: Language Agents with Verbal Reinforcement Learning** — Shinn et al. (Northeastern/Princeton), 2023 | **NeurIPS 2023** | **Validation Agent self-debugging loop** (§6: diagnose→contextualize→adapt→retry→cap) + **Cycle Guard/Reflector** (§10): both are direct implementations of Reflexion's verbal reinforcement pattern — the agent critiques its own failed attempts, stores the reflection, and adapts before retrying. Every agent paper cites this; not listing it as primary when two contributions implement it looks like an oversight. |

---


## SECTION 6 — BENCHMARK PAPERS

| # | Status | File | Paper | Surface | Why Essential |
|---|---|---|---|---|---|
| 23 | ✅ | [📄 `18-cybench-a-framework-for-evaluating-cybersecurity.pdf`](paper-research/downloaded-paper-curated/18-cybench-a-framework-for-evaluating-cybersecurity.pdf) | **Cybench** — Zhang et al., 2024 | All | Largest recognized cybersecurity agent benchmark. 40 professional CTF tasks. Standard baseline — CHECKMATE, D-CIPHER, and all SotA systems report here. You MUST report here too. |
| 24 | ✅ | [📄 `15-pentesteval-benchmarking-llm-based-penetration-testing.pdf`](paper-research/downloaded-paper-curated/15-pentesteval-benchmarking-llm-based-penetration-testing.pdf) | **PentestEval** — Yang et al. (SMU/NTU), 2025 | Network + partial Web | 346-task benchmark across 6 decomposed pentest stages (NIST/PTES-aligned). Covers OWASP Top 10 + CWE Top 25 in 12 vulnerable scenarios. Only benchmark with expert-annotated stage-level ground truth. Tests PentestGPT, PentestAgent, VulnBot — directly comparable to your system. **Replaces AutoPenBench as primary network evaluation benchmark.** |
| 25 | ✅ | [📄 `14-bountybench-dollar-impact-of-ai-agent-attackers-and.pdf`](paper-research/downloaded-paper-curated/14-bountybench-dollar-impact-of-ai-agent-attackers-and.pdf) | **BountyBench** — Zhang et al. (Stanford / UC Berkeley), arXiv 2025 | Web (Bug Bounty) | Real-world web vulnerability impact in dollar terms. Bug bounty CVEs. Authors include Percy Liang, Dan Boneh, Dawn Song. Only benchmark measuring business impact of AI web agents. |



---

## SECTION 7 — SURVEY PAPERS

| # | Status | File | Paper | Scope | Why This One |
|---|---|---|---|---|---|
| 26 | ✅ | [📄 `13-forewarned-is-forearmed-a-survey-on-llm-based-agents-in.pdf`](paper-research/downloaded-paper-curated/13-forewarned-is-forearmed-a-survey-on-llm-based-agents-in.pdf) | **"Forewarned is Forearmed": Survey on LLM-Based Agents in Autonomous Cyberattacks** — Xu et al. (NTU/Waterloo), IEEE 2025 | **VAPT-specific** | 150+ papers on LLM agents for offensive cybersecurity. Covers network, web, enterprise, multi-agent, defensive implications. NTU/Waterloo/IEEE authorship. The canonical reference for positioning CMatrix in the security literature. |
| 27 | ✅ | [📄 `25-a-survey-on-large-language-model-based-autonomous-agents.pdf`](paper-research/downloaded-paper-curated/25-a-survey-on-large-language-model-based-autonomous-agents.pdf) | **A Survey on Large Language Model based Autonomous Agents** — Wang et al., Frontiers of Computer Science 2024 | **General agent architecture** | 3,200+ citations. Establishes the canonical 4-module agent taxonomy (Profile · Memory · Planning · Action) used as background vocabulary in every agent paper. Needed once in your Background section to ground the agent architecture framework your Commander/Agent design implements. No agent paper skips this citation. |

---

## FINAL COUNT

| Category | Papers | Source |
|---|---|---|
| Network Pentesting | 10 | ✅ All in library |
| Web Pentesting | 6 | ✅ All in library |
| API Security | 2 | ✅ All in library |
| Multi-Agent Architecture | 2 | ✅ All in library |
| Agent Reasoning Foundations | 2 | ✅ All in library |
| Benchmarks | 3 | ✅ All in library |
| Surveys | 2 | ✅ All in library |
| **TOTAL** | **27** | **✅ All 27 papers in library** |

---

## Complete Drop Table (73 → 25 papers)

Everything in your library that is excluded, with exact reasons:

| File # | Paper | Drop Reason |
|---|---|---|
| 02 | Cyber-Zero | LLM fine-tuning for CTF. No VAPT framework. Irrelevant to your scope. |
| 04 | Pen-Strategist | Fine-tuning Qwen for pentest strategy. Interesting but a model paper, not a multi-agent framework paper. |
| 06 | CTFExplorer | Multi-target CTF benchmark only. CTF ≠ VAPT. |
| 07 | To Defend Against Cyber Attacks | Opinion/position paper. No framework, no evaluation. |
| 08 | LLMs as Hackers (Linux PrivEsc) | Linux privilege escalation only. Very narrow. Fully covered by Network section. |
| 09 | Towards Cybersecurity Superintelligence | Short position paper summarizing PentestGPT→CAI→G-CTR evolution. Not a framework paper. |
| 10 | Survey of Agentic AI and Cybersecurity | Broader survey, less focused than Forewarned is Forearmed. One survey is enough. |
| 11 | Red Teaming Framework for AI Robustness | AI model robustness red-teaming, not VAPT. Wrong domain. |
| 12 | ExploitGym | RL-based exploit generation gym. Not LLM agent, not VAPT. |
| 14 | PaceBench | Evaluates "practical AI cybersecurity capability" but CTF-focused. |
| 15 | ENIGMA | Interactive tool assistance for CTF. CTF-only. |
| 17 | Measuring and Augmenting LLMs for CTF | CTF solving capability paper. Not VAPT. |
| 19 | From Capabilities to Performance | Evaluation taxonomy paper. Informative but not a foundational framework. |
| 20 | Unified Modeling Framework (AutoPT-Sim) | Network simulation modeling. Too theoretical/academic for a working framework paper. |
| 23 | CAI | Bug bounty + CTF focused. Network-centric. Covered by BountyBench + Incalmo. |
| 24 | Cybersecurity AI (CAI CTF #1) | CTF competition paper. Not VAPT. |
| 25 | Pentest-R1 | Reasoning-first pentesting — interesting but a model tuning paper, not a framework. |
| 26 | RedTeamLLM | General agentic offensive framework. No surface-specific evaluation. Superseded by Co-RedTeam and CHECKMATE. |
| 27 | XOffense | Superseded by CHECKMATE and D-CIPHER. No web/API coverage. |
| 29 | AutoPentester | Thin. Superseded by CHECKMATE. |
| 30 | RapidPen | IP-to-shell only. Covered by CHECKMATE + Incalmo. |
| 31 | Aracne | Shell agent only. Zero Web/API. |
| 32 | AutoPentest (#32) | Vulnerability management framing only. Thin. |
| 33 | RefPentester | HTB/network-only. Self-reflection covered by D-CIPHER + Co-RedTeam. |
| 34 | CurriculumPT | CVE exploitation, curriculum scheduling. No web/API. |
| 36 | PentestMCP | Tool integration using MCP. Useful for implementation, not a primary research paper. Cite inline. |
| 37 | On the Surprising Efficacy of LLMs | Evaluation study. Informative, not primary. |
| 40 | Towards Automated Penetration Testing | Early conceptual paper. Superseded by everything else. |
| 41 | Cybersecurity AI Game-Theoretic | Game-theoretic AI for CTF. CTF-only. |
| 43 | CRAKEN | Knowledge-based tool selection. Interesting but CTF-only, covered by D-CIPHER. |
| 44 | CyberGym | Benchmark for vulnerability PoC generation from code. Not VAPT agent testing. |
| 45 | Empirical Evaluation of LLMs for CTF | CTF-only, older paper. |
| 46 | Shell or Nothing (TermiAgent/TermiBench) | Strong network benchmark, but PentestEval is more rigorous and targeted. |
| 48 | AGrail | Agent guardrail/safety paper. Defensive. Not relevant to your framework. |
| 49 | RAG for Cybersecurity | RAG retrieval technique paper. Cite inline only. |
| 50 | CAIBench | Meta-benchmark for CTF + A&D. Interesting but CTF-centric. |
| 51 | When LLMs Meet Cybersecurity | Broad survey, less focused. Forewarned is Forearmed is better for this scope. |
| 52 | PentestMCP Toolkit | Tool companion to #36. Same reason. |
| 53 | NYU CTF Bench (v1) | CTF-only. Covered by Cybench. |
| 56 | AutoAttacker | Superseded by CHECKMATE + D-CIPHER. |
| 57 | BreachSeek | Redundant with VulnBot and PentestAgent. |
| 59 | HackSynth | CTF solving agent + eval. CTF-only. |
| 62 | Pentest-AI (MITRE ATT&CK) | MITRE mapping only, no novel architecture. |
| 63 | NYU CTF Bench (v2) | CTF-only. Covered by Cybench. |
| 66 | AutoPenBench | Good but PentestEval is more rigorous. Retain as secondary benchmark only. |
| 67 | PenHeal | Pentest + remediation. Interesting but remediation is out of your scope. |
| 69 | Language Agents as Hackers (CTF) | CTF-only, early paper. |
| 70 | ReAct | Cite inline in Methods. Not a primary paper. |
| 71 | Tree of Thoughts | Cite inline in Methods. Not a primary paper. |
| 73 | Chain-of-Thought | Cite inline in Methods. Not a primary paper. |

---

## Attack Surface Coverage Map

| Surface | Papers | Verdict |
|---|---|---|
| 🌐 **Web (OWASP Top 10)** | Fang One-Day (#11), Fang Zero-Day (#12), MAPTA (#13), AWE (#14), AutoPT (#15), HackWorld (#16), Co-RedTeam (#10), BountyBench (#25) | ✅ **Strong** |
| 🔌 **API (REST + GraphQL)** | MAPTA (#13 partial), RESTler (#18 baseline), PrediQL (#17 GraphQL) | 🟡 **Covered with CMatrix as novel extension** |
| 🕸️ **Network (recon, CVE, privesc, lateral)** | Getting pwnd (#1), PentestGPT (#2), PentestGPT V2 (#3), VulnBot (#4), PentestAgent (#5), CHECKMATE (#6), D-CIPHER (#7), Incalmo (#8), Enterprise Networks (#9), Co-RedTeam (#10) | ✅ **Very Strong** |
| 🤖 **Multi-Agent Orchestration** | AutoGen (#21), MetaGPT (#22), D-CIPHER (#7), Incalmo (#8), CHECKMATE (#6), VulnBot (#4), Co-RedTeam (#10) | ✅ **Strong** |
| 🧠 **Agent Reasoning (planning, memory, self-correction)** | Voyager (#19) — skill crystallization, Reflexion (#20) — verbal reinforcement / self-debug, MemGPT — context paging (inline cite) | ✅ **Strong** |
| 📊 **Benchmarks** | Cybench (#23), PentestEval (#24), BountyBench (#25), AutoPT (#15 web), HackWorld (#16 web) | ✅ **Strong** |
| 📖 **Survey** | Forewarned is Forearmed (#26) | ✅ **One authoritative survey** |
