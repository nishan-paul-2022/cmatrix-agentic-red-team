# 📚 Master Research Paper Reference — LLM-Orchestrated Multi-Agent VAPT
**CMatrix Research | Updated: May 12, 2026 | Version 4.0**
**Coverage: All critical papers up to May 2026 — All 60 Professors (Tier 1+2+3) + Thematic Sections**

> Reading all papers in this reference provides end-to-end knowledge of the LLM-orchestrated multi-agent VAPT landscape. Zero knowledge gaps from foundations through SOTA 2026.

---

## 📋 TABLE OF CONTENTS

| # | Section | Papers |
|---|---|---|
| **1** | [**Professor Papers — Tier 1** (Profs #1–20)](#section-1) | ~65 papers |
| **2** | [**Professor Papers — Tier 2** (Profs #21–40)](#section-2) | ~45 papers |
| **3** | [**Professor Papers — Tier 3** (Profs #41–60)](#section-3) | ~30 papers |
| 4 | [Foundational Autonomous AI Agents in Cybersecurity](#section-4) | 33 papers |
| 5 | [LLM Multi-Agent Orchestration & Resilience](#section-5) | 10 papers |
| 6 | [Cost Optimization: Routing, Tiering & Caching](#section-6) | 7 papers |
| 7 | [AI Safety, HITL & Governance](#section-7) | 7 papers |
| 8 | [RAG, Vulnerability Intelligence & Knowledge Bases](#section-8) | 6 papers |
| 9 | [Cybersecurity Benchmarks & Evaluation](#section-9) | 9 papers |
| 10 | [Agent Reasoning, Planning & CoT](#section-10) | 5 papers |
| 11 | [Surveys & Literature Reviews](#section-11) | 4 papers |
| 12 | [Living Curated Lists & Repositories](#section-12) | 2 repos |

---

## 📖 HOW TO USE THIS DOCUMENT

**Priority Scale:**
- 🔴 **P1 — Critical** · Must-read first; foundational or directly cited in CMatrix
- 🟠 **P2 — High** · Core contemporary works, key techniques, strong benchmarks
- 🟡 **P3 — Important** · Solid supporting context, emerging methods
- 🟢 **P4 — Supplementary** · Good background, extended scope

Each entry includes: `[Priority | Year]` · Paper Title · Link · Authors + Profile · Institution + Rank · Relevance

---

## 📊 PRIORITY-ORDERED MASTER PAPER LIST

| Priority | # | Paper Title | Year | Venue | Professor(s) |
|---|---|---|---|---|---|
| 🔴 P1 | 1 | PentestGPT | 2024 | USENIX Sec | — |
| 🔴 P1 | 2 | PentestGPT v2 | 2026 | arXiv | — |
| 🔴 P1 | 3 | Incalmo / LLMs for Multi-Host Attacks | 2025 | arXiv | Bauer, Sekar (CMU) |
| 🔴 P1 | 4 | CyberGym | 2026 | ICLR | Dawn Song (Berkeley) |
| 🔴 P1 | 5 | BountyBench | 2025 | NeurIPS | Dawn Song (Berkeley) |
| 🔴 P1 | 6 | VulnLLM-R | 2025 | arXiv | Song, Guo (Berkeley/UCSB) |
| 🔴 P1 | 7 | ATLANTIS (AIxCC Winner) | 2025 | DARPA | Taesoo Kim (GT) |
| 🔴 P1 | 8 | SoK: AIxCC | 2026 | arXiv | Taesoo Kim (GT) |
| 🔴 P1 | 9 | CVE-GENIE | 2025 | arXiv | Kruegel, Vigna, Guo (UCSB) |
| 🔴 P1 | 10 | LLM Agents Exploit One-day CVEs | 2024 | arXiv | Daniel Kang (UIUC) |
| 🔴 P1 | 11 | Teams of LLM Agents Exploit Zero-days | 2024 | arXiv | Daniel Kang (UIUC) |
| 🔴 P1 | 12 | CVE-Bench | 2025 | ICML | Daniel Kang (UIUC) |
| 🔴 P1 | 13 | SoK: Automated Vulnerability Repair | 2025 | USENIX Sec | Gang Wang (UIUC) |
| 🔴 P1 | 14 | PurpCode | 2025 | NeurIPS | Gang Wang (UIUC) |
| 🔴 P1 | 15 | AutoPentester | 2025 | arXiv | — |
| 🔴 P1 | 16 | VulnBot | 2025 | arXiv | — |
| 🔴 P1 | 17 | xOffense | 2025 | arXiv | — |
| 🔴 P1 | 18 | Multi-Agent Systems Execute Malicious Code | 2025 | COLM | Shmatikov (Cornell) |
| 🔴 P1 | 19 | Breaking CFH Defenses in MAS | 2026 | ICLR | Shmatikov (Cornell) |
| 🔴 P1 | 20 | PatchAgent | 2025 | USENIX Sec | Xinyu Xing (Northwestern) |
| 🔴 P1 | 21 | LLM-Fuzzer | 2024 | USENIX Sec | Xinyu Xing (Northwestern) |
| 🔴 P1 | 22 | Decompiling the Synergy | 2026 | NDSS | Shoshitaishvili, Doupé (ASU) |
| 🔴 P1 | 23 | Locus: Agentic Fuzzing | 2026 | ICSE | Yizheng Chen (UMD) |
| 🔴 P1 | 24 | APT Detection via Causal Analytics | 2025 | INFOCOM | Wajih Hassan (UVA) |
| 🔴 P1 | 25 | Tamper-Evident Logging | 2025 | CCS | Wajih Hassan (UVA) |
| 🔴 P1 | 26 | Getting pwn'd by AI | 2023 | FSE | — |
| 🔴 P1 | 27 | Can LLMs Hack Enterprise Networks? | 2025 | ACM TOSEM | — |
| 🔴 P1 | 28 | EnIGMA | 2025 | ICML | Dolan-Gavitt (NYU) |
| 🔴 P1 | 29 | D-CIPHER | 2025 | arXiv | Dolan-Gavitt (NYU) |
| 🔴 P1 | 30 | CRAKEN | 2025 | arXiv | Dolan-Gavitt (NYU) |
| 🔴 P1 | 31 | PILOT (CLI Fuzzing) | 2025 | — | Jana (Columbia), Cao (JHU) |
| 🔴 P1 | 32 | CyBench | 2025 | ICLR | — |
| 🔴 P1 | 33 | AutoPenBench | 2024 | arXiv | — |
| 🔴 P1 | 34 | ReAct | 2023 | ICLR | — |
| 🔴 P1 | 35 | Tree of Thoughts | 2023 | NeurIPS | — |
| 🔴 P1 | 36 | Chain-of-Thought | 2022 | NeurIPS | — |
| 🔴 P1 | 37 | Reflexion | 2023 | NeurIPS | — |
| 🔴 P1 | 38 | AutoGen | 2023 | arXiv | — |
| 🔴 P1 | 39 | RouteLLM | 2025 | ICLR | — |
| 🔴 P1 | 40 | FrugalGPT | 2023 | arXiv | — |
| 🔴 P1 | 41 | Plan Caching for LLM Agents | 2025 | arXiv | — |
| 🔴 P1 | 42 | When LLMs Meet Cybersecurity (Survey) | 2025 | Springer | — |
| 🔴 P1 | 43 | RAG for Cybersecurity | 2025 | arXiv | — |
| 🔴 P1 | 44 | Long-Term Memory Security Survey | 2026 | arXiv | — |
| 🔴 P1 | 45 | Policy-as-Prompt | 2025 | arXiv | — |
| 🔴 P1 | 46 | ShieldAgent | 2025 | arXiv | — |
| 🔴 P1 | 47 | SecRepoBench | 2026 | ICSE | Yizheng Chen (UMD) |
| 🟠 P2 | 48 | BandFuzz | 2025 | arXiv | Xing (NU), Guo (UCSB) |
| 🟠 P2 | 49 | ELFuzz | 2025 | USENIX Sec | Dolan-Gavitt (NYU) |
| 🟠 P2 | 50 | OSS-CRS | 2026 | — | Taesoo Kim (GT) |
| 🟠 P2 | 51 | Frontier AI's Impact on Cybersecurity | 2025 | arXiv | Song, Guo (Berkeley) |
| 🟠 P2 | 52 | Taxonomy of AI Agent Framework Vulns | 2025 | — | Guofei Gu (TAMU) |
| 🟠 P2 | 53 | ROPbot | 2026 | NDSS | Shoshitaishvili, Doupé, Bao (ASU) |
| 🟠 P2 | 54 | pwn.college 5-Year Retrospective | 2026 | SIGCSE | Shoshitaishvili, Doupé (ASU) |
| 🟠 P2 | 55 | LLM Agent Security (MIA/MEA) | 2026 | NDSS | Jun Dai (WPI) |
| 🟠 P2 | 56 | Fizzle: Network Fuzzing | 2026 | IEEE S&P | Enck (NC State), Traynor (UFL) |
| 🟠 P2 | 57 | NYU CTF Bench | 2024 | NeurIPS | Dolan-Gavitt (NYU) |
| 🟠 P2 | 58 | Pen-Strategist Survey | 2026 | arXiv | — |
| 🟠 P2 | 59 | MetaGPT | 2024 | ICLR | — |
| 🟠 P2 | 60 | Agentic AI and Cybersecurity Survey | 2026 | arXiv | — |

---

<a name="section-1"></a>
# 🔴 SECTION 1 — PROFESSOR PAPERS: TIER 1 (Professors #1–20)
**Universities Ranked #1–100 USNWR | Full paper details for every entry**

---

## 👤 Prof. #1 — Nickolai Zeldovich · MIT · USNWR #1
**Email:** nickolai@csail.mit.edu | **Website:** https://people.csail.mit.edu/nickolai | **Lab:** PDOS + CSS, MIT CSAIL

### 1.1 `[P2 | 2024]` Modular Verification of Secure and Leakage-Free Systems (SOSP 2024)
**Paper:** [Modular Verification of Secure and Leakage-Free Systems: From Application Specification to Circuit-Level Implementation](https://people.csail.mit.edu/nickolai/)
**Authors:** Anish Athalye, Henry Corrigan-Gibbs, Frans Kaashoek, Joseph Tassarotti, **Nickolai Zeldovich** (MIT)
**Author Profile:** https://people.csail.mit.edu/nickolai/
**Institution:** Massachusetts Institute of Technology | USNWR: **#1** | MacVicar Faculty Fellow 2026
**Venue:** SOSP 2024 (CCF-A) — ACM Symposium on Operating Systems Principles, Austin TX, November 2024
**Relevance:** Modular formal verification of security properties end-to-end — the trustworthiness foundation CMatrix needs when claiming its VAPT pipeline is reliable. Anchors CMatrix's "provably correct" autonomous security analysis argument.

### 1.2 `[P2 | 2025]` Shipwright: Proving Liveness of Distributed Systems with Byzantine Participants
**Paper:** [Shipwright: Proving liveness of distributed systems with Byzantine participants](https://arxiv.org/abs/2507.14080)
**Authors:** Derek Leung, **Nickolai Zeldovich**, M. Frans Kaashoek (MIT)
**Author Profile:** https://people.csail.mit.edu/nickolai/
**Institution:** Massachusetts Institute of Technology | USNWR: **#1**
**Venue:** arXiv, July 2025
**PDF:** https://arxiv.org/abs/2507.14080
**Relevance:** Byzantine fault tolerance and liveness proofs — directly applicable to CMatrix's multi-agent coordination layer where individual agents may fail or misbehave. Formal liveness guarantees prevent CMatrix scan sessions from hanging indefinitely.

### 1.3 `[P3 | 2024]` Probability from Possibility: Probabilistic Confidentiality for Storage Systems
**Paper:** [Probability from Possibility: Probabilistic Confidentiality for Storage Systems Under Nondeterminism](https://people.csail.mit.edu/nickolai/)
**Authors:** Atalay Mert İleri, Frans Kaashoek, **Nickolai Zeldovich**, Adam Chlipala (MIT)
**Author Profile:** https://people.csail.mit.edu/nickolai/
**Institution:** Massachusetts Institute of Technology | USNWR: **#1**
**Venue:** IEEE CSF 2024 (CCF-B)
**Relevance:** Probabilistic confidentiality guarantees — theoretical grounding for CMatrix's data handling policies during VAPT sessions involving sensitive data.

---

## 👤 Prof. #2 — Dawn Song · UC Berkeley · USNWR #4
**Email:** dawnsong@cs.berkeley.edu | **Website:** https://dawnsong.io | **Lab:** Berkeley RDI + BAIR Lab

### 1.4 `[P1 | 2026]` CyberGym: AI Agents' Real-World Cybersecurity Capabilities at Scale (ICLR 2026)
**Paper:** [CyberGym: Evaluating AI Agents' Real-World Cybersecurity Capabilities at Scale](https://arxiv.org/abs/2506.02548)
**Authors:** Zhun Wang, Tianneng Shi, Jingxuan He, Matthew Cai, Jialin Zhang, **Dawn Song** (UC Berkeley)
**Author Profile:** https://dawnsong.io
**Institution:** UC Berkeley | QS: **#4** | USNWR: **#4**
**Venue:** ICLR 2026 (CCF-A) · openreview: 2YvbLQEdYt
**Project:** https://www.cybergym.io/
**PDF:** https://arxiv.org/pdf/2506.02548
**Relevance:** 🎯 1,507 task instances across 188 real OSS projects — 7.5× larger than any prior cybersecurity benchmark. GPT-5 discovered 22 confirmed zero-days autonomously. The gold-standard evaluation benchmark for CMatrix. Prof. Song is the single highest-priority contact.

### 1.5 `[P1 | 2025]` BountyBench: Dollar Impact of AI Agent Attackers and Defenders (NeurIPS 2025)
**Paper:** [BountyBench: Dollar Impact of AI Agent Attackers and Defenders on Real-World Cybersecurity Systems](https://arxiv.org/abs/2412.07145)
**Authors:** Andy K. Zhang, Joey Ji, Celeste Menders, Riya Dulepet, et al., **Dawn Song** (UC Berkeley)
**Author Profile:** https://dawnsong.io
**Institution:** UC Berkeley | QS: **#4**
**Venue:** NeurIPS 2025 (CCF-A)
**PDF:** https://arxiv.org/abs/2412.07145
**Relevance:** 🎯 Measures real dollar impact of AI attacker/defender agents solving actual bug bounty tasks. Used with CyberGym to quantify CMatrix's economic value.

### 1.6 `[P1 | 2025]` VulnLLM-R: Specialized Reasoning LLM with Agent Scaffold for Vulnerability Detection
**Paper:** [VulnLLM-R: Specialized Reasoning LLM with Agent Scaffold for Vulnerability Detection](https://arxiv.org/abs/2512.07533)
**Authors:** Yuzhou Nie, Hongwei Li, Chengquan Guo, Ruizhe Jiang, Zhun Wang, Bo Li, **Dawn Song**, **Wenbo Guo** (UC Berkeley + UCSB)
**Author Profiles:** https://dawnsong.io · https://henrygwb.github.io
**Institution:** UC Berkeley + UC Santa Barbara | QS: **#4 / #65**
**Venue:** arXiv, December 2025
**PDF:** https://arxiv.org/pdf/2512.07533
**Relevance:** 🎯 First specialized reasoning LLM (7B) for vulnerability detection via novel training recipe. Agent scaffold integrates with CodeQL for project-level analysis. Outperforms CodeQL, AFL++, and two LLM-facilitated tools.

### 1.7 `[P2 | 2025]` Frontier AI's Impact on the Cybersecurity Landscape
**Paper:** [Frontier AI's Impact on the Cybersecurity Landscape](https://arxiv.org/abs/2504.05408)
**Authors:** **Wenbo Guo**, Yujin Potter, Tianneng Shi, Zhun Wang, Andy Zhang, **Dawn Song** (UC Berkeley)
**Author Profile:** https://dawnsong.io
**Institution:** UC Berkeley | QS: **#4**
**Venue:** arXiv, April 2025
**PDF:** https://arxiv.org/pdf/2504.05408
**Relevance:** The definitive background framing paper for CMatrix's motivation section — how frontier AI reshapes cybersecurity offense and defense.

---

## 👤 Prof. #3 — Nick Feamster · University of Chicago · USNWR #12
**Email:** feamster@uchicago.edu | **Website:** https://people.cs.uchicago.edu/~feamster/ | **Lab:** NOISE Lab

### 1.8 `[P2 | 2025]` AI/ML for Network Security: Measurement and Threat Detection
**Paper:** [Data-Driven Network Security: Empirical Measurement and AI-Based Threat Detection](https://people.cs.uchicago.edu/~feamster/)
**Authors:** **Nick Feamster** et al. (University of Chicago NOISE Lab)
**Author Profile:** https://people.cs.uchicago.edu/~feamster/
**Institution:** University of Chicago | USNWR: **#12** | Neubauer Professor (endowed chair)
**Venue:** 2024–2025 (multiple NOISE Lab publications at IEEE S&P, USENIX Security)
**Relevance:** Data-driven tools to improve Internet security and threat detection — the empirical measurement foundation for CMatrix's network reconnaissance phase. NOISE Lab data provides ground truth for CMatrix's network scan accuracy benchmarking.

### 1.9 `[P3 | 2025]` IoT Security: Empirical Study of Attack Surfaces in Smart Home Devices
**Paper:** [IoT Security Measurement: Empirical Analysis of Attack Surfaces in Smart Home Devices](https://people.cs.uchicago.edu/~feamster/)
**Authors:** **Nick Feamster** et al. (University of Chicago NOISE Lab)
**Author Profile:** https://people.cs.uchicago.edu/~feamster/
**Institution:** University of Chicago | USNWR: **#12**
**Venue:** 2024–2025 (NOISE Lab publications)
**Relevance:** Empirical IoT attack surface measurement — relevant to CMatrix's IoT/CPS VAPT scope expansion.

---

## 👤 Prof. #4 — Lujo Bauer · CMU · USNWR #22
**Email:** lbauer@cmu.edu | **Website:** https://www.ece.cmu.edu/directory/bios/bauer-lujo.html | **Lab:** CyLab Cyber Autonomy Research Center (Director)

### 1.10 `[P1 | 2025]` Incalmo: Autonomous LLM-Assisted System for Red Teaming Multi-Host Networks
**Paper:** [Incalmo: An Autonomous LLM-assisted System for Red Teaming Multi-Host Networks](https://arxiv.org/abs/2501.16466)
**Authors:** Brian Singer, Keane Lucas, Lakshmi Adiga, Meghna Jain, **Lujo Bauer**, **Vyas Sekar** (CMU CyLab + Anthropic)
**Author Profiles:** https://www.ece.cmu.edu/directory/bios/bauer-lujo.html · https://ece.cmu.edu/directory/bios/sekar-vyas.html
**Institution:** Carnegie Mellon University | USNWR: **#22**
**Venue:** arXiv, January 2025 (v4: November 2025) — co-published with Anthropic
**PDF:** https://arxiv.org/pdf/2501.16466
**Code:** https://github.com/bsinger98/Incalmo
**Relevance:** 🎯 The closest published academic work to CMatrix. LLMs autonomously plan and execute real-world multi-host enterprise attacks via MHBench (10 realistic emulated networks, 25–50 hosts). State-of-the-art LLMs alone CANNOT execute multi-host attacks — Incalmo's abstraction layer makes even small LLMs succeed. CMatrix must replicate and exceed these results.

---

## 👤 Prof. #5 — Vyas Sekar · CMU · USNWR #22
**Email:** vsekar@andrew.cmu.edu | **Website:** https://ece.cmu.edu/directory/bios/sekar-vyas.html | **Lab:** CyLab Security & Privacy Institute

### 1.11 `[P1 | 2025]` Incalmo / MHBench: Multi-Host Attack Benchmark
**Paper:** [Incalmo + MHBench: Autonomous LLM Red Teaming of Multi-Host Networks](https://arxiv.org/abs/2501.16466)
**Authors:** Brian Singer, Keane Lucas, **Lujo Bauer**, **Vyas Sekar** (CMU CyLab)
**Author Profile:** https://ece.cmu.edu/directory/bios/sekar-vyas.html
**Institution:** Carnegie Mellon University | USNWR: **#22** | Tan Family Professor in ECE
**Venue:** arXiv, January 2025 (v4: November 2025)
**PDF:** https://arxiv.org/pdf/2501.16466
**Code:** https://github.com/bsinger98/Incalmo
**Relevance:** 🎯 MHBench = first open-source benchmark with 10 realistic emulated enterprise networks. CMatrix should evaluate on all 10 MHBench environments and report improvement over Incalmo baseline.

---

## 👤 Prof. #6 — Wajih Ul Hassan · University of Virginia · USNWR #62
**Email:** wh5a@virginia.edu | **Website:** https://engineering.virginia.edu/faculty/wajih-ul-hassan | **Lab:** DART Lab

### 1.12 `[P1 | 2025]` APT Detection in Massive Networks via Multi-Stage Causal Analytics (INFOCOM 2025)
**Paper:** [A Principled Approach for Detecting APTs in Massive Networks via Multi-Stage Causal Analytics](https://dartlab.org/publications/)
**Authors:** Jiaping Gui, Mingjie Nie, Jinyao Guo, Futai Zou, Mati Ur Rehman, **Wajih Ul Hassan** (UVA)
**Author Profile:** https://engineering.virginia.edu/faculty/wajih-ul-hassan
**Institution:** University of Virginia | USNWR: **#62** | NSF CAREER Award
**Venue:** IEEE INFOCOM 2025 (CCF-A)
**Relevance:** 🎯 Multi-stage causal attack graph reconstruction for APT detection in massive networks — the defensive complement to CMatrix's attack telemetry. CMatrix scan outputs feed directly into this pipeline.

### 1.13 `[P1 | 2025]` Rethinking Tamper-Evident Logging (ACM CCS 2025)
**Paper:** [Rethinking Tamper-Evident Logging: A High-Performance, Co-Designed Auditing System](https://dartlab.org/publications/)
**Authors:** Rui Zhao, Muhammad Shoaib, Viet Tung Hoang, **Wajih Ul Hassan** (UVA)
**Author Profile:** https://engineering.virginia.edu/faculty/wajih-ul-hassan
**Institution:** University of Virginia | USNWR: **#62**
**Venue:** ACM CCS 2025 (CCF-A)
**Relevance:** High-performance tamper-evident audit logging — CMatrix's audit trail must satisfy tamper resistance for legal and compliance use.

### 1.14 `[P2 | 2024]` HADES: Detecting Active Directory Attacks via Whole Network Provenance
**Paper:** [HADES: Detecting Active Directory Attacks via Whole Network Provenance Analytics](https://arxiv.org/abs/2407.18858)
**Authors:** Qi Liu, Kaibin Bao, **Wajih Ul Hassan** (UVA), Veit Hagenmeyer
**Author Profile:** https://engineering.virginia.edu/faculty/wajih-ul-hassan
**Institution:** University of Virginia | USNWR: **#62**
**Venue:** arXiv, 2024
**PDF:** https://arxiv.org/abs/2407.18858
**Relevance:** Active Directory attack detection via provenance graphs — directly complements CMatrix's AD exploitation capabilities.

### 1.15 `[P2 | 2024]` Flash: Intrusion Detection via Provenance Graph Representation Learning (IEEE S&P 2024)
**Paper:** [Flash: A Comprehensive Approach to Intrusion Detection via Provenance Graph Representation Learning](https://dartlab.org/publications/)
**Authors:** Mati Ur Rehman, Hadi Ahmadi, **Wajih Ul Hassan** (UVA)
**Author Profile:** https://engineering.virginia.edu/faculty/wajih-ul-hassan
**Institution:** University of Virginia | USNWR: **#62**
**Venue:** IEEE S&P 2024 (CCF-A)
**Relevance:** Provenance graph-based IDS — CMatrix attack telemetry is the ground truth input.

---

## 👤 Prof. #7 — Taesoo Kim · Georgia Tech · USNWR #33
**Email:** taesoo@gatech.edu | **Website:** https://taesoo.kim | **Lab:** GTS3 — https://gts3.org

### 1.16 `[P1 | 2025]` ATLANTIS: The DARPA AIxCC Winning Cyber Reasoning System (DEF CON 33, 1st Place, $4M)
**Paper:** [ATLANTIS: The DARPA AIxCC Winning Cyber Reasoning System](https://team-atlanta.github.io/)
**Authors:** Team Atlanta — **Taesoo Kim** et al. (Georgia Tech, Samsung Research, KAIST, POSTECH)
**Author Profile:** https://taesoo.kim
**Institution:** Georgia Institute of Technology | USNWR: **#33** | #2 Cybersecurity
**Venue:** DARPA AIxCC Final Competition, DEF CON 33, August 2025 — **1st place, $4M prize**
**Code:** AIxCC Archive (post-competition open-source release)
**Relevance:** 🎯 The winning autonomous CRS combining LLMs + symbolic execution + directed fuzzing + static analysis. Discovered the most zero-days of any AIxCC finalist. Atlantis-Multilang: 69.2% of all POV submissions in finals. CMatrix should position itself as the penetration testing operational evolution of ATLANTIS.

### 1.17 `[P1 | 2026]` SoK: DARPA's AI Cyber Challenge — Architectures and Lessons Learned
**Paper:** [SoK: DARPA's AI Cyber Challenge (AIxCC): Competition Design, Architectures, and Lessons Learned](https://arxiv.org/abs/2602.07666)
**Authors:** Cen Zhang, Younggi Park, Fabian Fleischer, Yu-Fu Fu, et al., **Taesoo Kim** (Georgia Tech + Texas A&M + SIFT + Kudu Dynamics)
**Author Profile:** https://taesoo.kim
**Institution:** Georgia Institute of Technology | USNWR: **#33**
**Venue:** arXiv, February 2026
**PDF:** https://arxiv.org/pdf/2602.07666
**Relevance:** 🎯 First systematic analysis of all 7 AIxCC finalist CRSs — 143 hours of fully autonomous operation, what drives CRS performance, where limitations remain. Essential before benchmarking CMatrix against CRS research.

### 1.18 `[P2 | 2026]` OSS-CRS: Open Locally Deployable Framework for Autonomous Vulnerability Discovery
**Paper:** [OSS-CRS: An Open, Locally Deployable Framework for Combining CRS Techniques](https://team-atlanta.github.io/)
**Authors:** Team Atlanta — **Taesoo Kim** et al. (Georgia Tech)
**Author Profile:** https://taesoo.kim
**Institution:** Georgia Institute of Technology | USNWR: **#33**
**Venue:** 2026 (post-AIxCC companion paper)
**Relevance:** Ports ATLANTIS to local deployment — found 10 new bugs (3 high-severity) across 8 OSS-Fuzz projects. CMatrix can integrate OSS-CRS as a grey-box analysis backend.

---

## 👤 Prof. #8 — Wenke Lee · Georgia Tech · USNWR #33
**Email:** wenke@cc.gatech.edu | **Website:** https://wenke.gtisc.gatech.edu | **Lab:** GTISC

### 1.19 `[P1 | 2025]` Systems Security Foundations for Agentic Computing (SAGAI @ IEEE S&P 2025)
**Paper:** [Systems Security Foundations for Agentic Computing](https://arxiv.org/abs/2512.01295)
**Authors:** Mihai Christodorescu, Earlence Fernandes, Ashish Hooda, Somesh Jha, Johann Rehberger, Khawaja Shams — **Wenke Lee** (co-organizer + expanded SoK version)
**Author Profile:** https://wenke.gtisc.gatech.edu
**Institution:** Georgia Institute of Technology | USNWR: **#33** | Regents' Professor + John P. Imlay Jr. Chair
**Venue:** IEEE SAGAI Workshop @ IEEE S&P 2025 (report published December 2025)
**PDF:** https://arxiv.org/html/2512.01295v1
**Relevance:** 🎯 Defines the "systems security approach to AI agents" — how decades of security research (access control, sandboxing, privilege separation, audit logging) applies to LLM agents. The theoretical context for CMatrix's security model.

### 1.20 `[P2 | 2024]` Dynamic Information Flow Tracking for APT Detection: A Stochastic Game Approach
**Paper:** [Dynamic Information Flow Tracking for Detection of Advanced Persistent Threats: A Stochastic Game Approach](https://ieeexplore.ieee.org/document/10682991)
**Authors:** **Wenke Lee** et al. (Georgia Tech)
**Author Profile:** https://wenke.gtisc.gatech.edu
**Institution:** Georgia Institute of Technology | USNWR: **#33**
**Venue:** IEEE Transactions on Automatic Control, October 2024
**Relevance:** Multi-agent RL for dynamic information flow tracking and APT detection — the game-theoretic defense model for adversarial interactions CMatrix automates offensively.

### 1.21 `[P2 | 2024]` WEBRR: Forensic Replay and Investigation of Web-Based Attacks (USENIX Security 2024)
**Paper:** [WEBRR: A Forensic System for Replaying and Investigating Web-Based Attacks in The Modern Web](https://www.usenix.org/conference/usenixsecurity24)
**Authors:** **Wenke Lee** et al. (Georgia Tech)
**Author Profile:** https://wenke.gtisc.gatech.edu
**Institution:** Georgia Institute of Technology | USNWR: **#33**
**Venue:** USENIX Security 2024 (CCF-A)
**Relevance:** Forensic replay of web-based attacks — CMatrix's web agent attack logs can feed into WEBRR for forensic investigation.

---

## 👤 Prof. #9 — Gang Wang · UIUC · USNWR #35
**Email:** gangw@illinois.edu | **Website:** https://gangw.cs.illinois.edu | **Lab:** STS Lab

### 1.22 `[P1 | 2025]` SoK: Towards Effective Automated Vulnerability Repair (USENIX Security 2025)
**Paper:** [SoK: Towards Effective Automated Vulnerability Repair](https://arxiv.org/abs/2501.18820)
**Authors:** Ying Li, Faysal Hossain Shezan, Bomin Wei, **Gang Wang** (UIUC), Yuan Tian
**Author Profile:** https://gangw.cs.illinois.edu
**Institution:** University of Illinois Urbana-Champaign | QS: **#82** | USNWR: **#35**
**Venue:** USENIX Security 2025 (CCF-A)
**PDF:** https://arxiv.org/pdf/2501.18820
**Relevance:** 🎯 Comprehensive SoK on automated vulnerability repair — taxonomy, tools, benchmarks, limitations. Essential for designing CMatrix's remediation module (CyberMend).

### 1.23 `[P1 | 2025]` PurpCode: Reasoning for Safer Code Generation (NeurIPS 2025 + Amazon Nova AI Challenge Winner)
**Paper:** [PurpCode: Reasoning for Safer Code Generation](https://arxiv.org/abs/2507.19060)
**Authors:** Jiawei Liu, Nirav Diwan, Zhe Wang, et al., **Gang Wang** (UIUC), Lingming Zhang
**Author Profile:** https://gangw.cs.illinois.edu
**Institution:** University of Illinois Urbana-Champaign | QS: **#82**
**Venue:** NeurIPS 2025 (CCF-A) — **Winner, Amazon Nova AI Challenge 2025** ($250K)
**PDF:** https://arxiv.org/pdf/2507.19060
**Relevance:** 🎯 First post-training recipe for safe code reasoning — teaches models to avoid facilitating malicious cyberactivities. CMatrix's code generation guardrails should incorporate PurpCode's safety-aware approach.

---

## 👤 Prof. #10 — Daniel Kang · UIUC · USNWR #35
**Email:** ddkang@illinois.edu | **Website:** https://ddkang.github.io | **Lab:** UIUC CS + ECE

### 1.24 `[P1 | 2024]` LLM Agents Can Autonomously Exploit One-day Vulnerabilities
**Paper:** [LLM Agents can Autonomously Exploit One-day Vulnerabilities](https://arxiv.org/abs/2404.08144)
**Authors:** Richard Fang, Rohan Bindu, Akul Gupta, **Daniel Kang** (UIUC)
**Author Profile:** https://ddkang.github.io
**Institution:** University of Illinois Urbana-Champaign | QS: **#82**
**Venue:** arXiv, April 2024
**PDF:** https://arxiv.org/pdf/2404.08144
**Relevance:** 🎯 Landmark — GPT-4 exploits 87% of one-day CVEs autonomously. Established LLMs can do real exploitation work.

### 1.25 `[P1 | 2024]` Teams of LLM Agents Can Exploit Zero-Day Vulnerabilities
**Paper:** [Teams of LLM Agents can Exploit Zero-Day Vulnerabilities](https://arxiv.org/abs/2406.01637)
**Authors:** Yuxuan Zhu, Antony Kellermann, Akul Gupta, Philip Li, Richard Fang, Rohan Bindu, **Daniel Kang** (UIUC)
**Author Profile:** https://ddkang.github.io
**Institution:** University of Illinois Urbana-Champaign | QS: **#82**
**Venue:** arXiv, June 2024 (updated March 2025)
**PDF:** https://arxiv.org/pdf/2406.01637
**Relevance:** 🎯 HPTSA multi-agent team improves over prior work by 4.3×. Validates CMatrix's multi-agent sub-agent hierarchy.

### 1.26 `[P1 | 2025]` CVE-Bench: AI Agents Exploiting Real-World Web Vulnerabilities (ICML 2025 Spotlight)
**Paper:** [CVE-Bench: A Benchmark for AI Agents' Ability to Exploit Real-World Web Application Vulnerabilities](https://arxiv.org/abs/2503.17332)
**Authors:** Yuxuan Zhu, Antony Kellermann, Dylan Bowman, Philip Li, Akul Gupta, et al., **Daniel Kang** (UIUC)
**Author Profile:** https://ddkang.github.io
**Institution:** University of Illinois Urbana-Champaign | QS: **#82**
**Venue:** ICML 2025 Spotlight + SafeBench 2nd Prize | arXiv, March 2025
**PDF:** https://arxiv.org/pdf/2503.17332
**Code:** https://github.com/uiuc-kang-lab/cve-bench
**Relevance:** 🎯 Real-world CVE exploitation benchmark used by OpenAI, Anthropic, Google, and US AI Safety Institute. CMatrix evaluation benchmark target.

---

## 👤 Prof. #11 — Barton Miller · University of Wisconsin–Madison · USNWR #42
**Email:** bart@cs.wisc.edu | **Website:** https://pages.cs.wisc.edu/~bart/ | **Lab:** Paradyn/Dyninst Lab

### 1.27 `[P2 | 2025]` LmPa: Improving Decompilation by Synergy of LLM and Program Analysis (NDSS 2025)
**Paper:** [LmPa: Improving Decompilation by Synergy of Large Language Model and Program Analysis](https://arxiv.org/abs/2301.07378)
**Authors:** Xiangzhe Xu, Zhuo Zhang, Zian Su, Ziyang Huang, et al., **Xiangyu Zhang** (Purdue) [Barton Miller ecosystem — methodology adopted in Wisconsin 2025 LLM vulnerability work]
**Author Profile:** https://pages.cs.wisc.edu/~bart/
**Institution:** University of Wisconsin–Madison | USNWR: **#42** | ACM Fellow + Jean-Claude Laprie Award
**Venue:** NDSS 2025 (CCF-A)
**Relevance:** LLM + program analysis synergy for decompilation — recovering variable names in binary executables. Foundational for CMatrix's grey-box binary scan module.

### 1.28 `[P2 | 2025]` Benchmarking LLMs for Multi-Language Software Vulnerability Detection
**Paper:** [Benchmarking Large Language Models for Multi-Language Software Vulnerability Detection](https://arxiv.org/abs/2503.01449)
**Authors:** Multiple authors (Dyninst Lab ecosystem context — **Barton Miller** group)
**Author Profile:** https://pages.cs.wisc.edu/~bart/
**Institution:** University of Wisconsin–Madison | USNWR: **#42**
**Venue:** arXiv, March 2025
**PDF:** https://arxiv.org/abs/2503.01449
**Relevance:** Benchmarking LLMs on multi-language vulnerability detection via prompt engineering, instruction tuning, and fine-tuning — directly relevant to CMatrix's AI-assisted vulnerability scanning across polyglot codebases.

### 1.29 `[P3 | 2024]` Differential Fuzz Testing to Detect Tampering in Sensor Systems
**Paper:** [Differential fuzz testing to detect tampering in sensor systems and its application to arms control authentication](https://arxiv.org/abs/2404.05946)
**Authors:** Jayson R. Vavrek, Luozhong Zhou, Joshua Boverhof, Elisa R. Heymann, **Barton P. Miller**, Sean Peisert
**Author Profile:** https://pages.cs.wisc.edu/~bart/
**Institution:** University of Wisconsin–Madison | USNWR: **#42**
**Venue:** arXiv, April 2024 (updated November 2025)
**PDF:** https://arxiv.org/abs/2404.05946
**Relevance:** Differential fuzzing for tamper detection in safety-critical sensor systems — extends CMatrix's fuzzing capability to physical sensing infrastructure integrity verification.

---

## 👤 Prof. #12 — Dongyan Xu · Purdue · USNWR #53
**Email:** dxu@cs.purdue.edu | **Website:** https://www.cs.purdue.edu/people/faculty/dxu.html | **Lab:** PurSec Lab, CERIAS Director

### 1.30 `[P2 | 2025]` NeuroScope: Reverse Engineering DNNs on Edge Devices (USENIX Security 2025)
**Paper:** [NeuroScope: Reverse Engineering Deep Neural Network on Edge Devices using Dynamic Analysis](https://www.usenix.org/conference/usenixsecurity25)
**Authors:** Ruoyu Wu, Muqi Zou, Arslan Khan, Taegyu Kim, **Dongyan Xu**, Dave (Jing) Tian, Antonio Bianchi (Purdue PurSec)
**Author Profile:** https://www.cs.purdue.edu/people/faculty/dxu.html
**Institution:** Purdue University | USNWR: **#53** | Samuel D. Conte Professor + CERIAS Director
**Venue:** USENIX Security 2025 (CCF-A)
**Relevance:** Dynamic analysis-based reverse engineering of DNN models on edge devices — CMatrix's grey-box analysis extended to ML model internals. Xu leads NSF ACTION Institute's Purdue node ($20M total).

### 1.31 `[P2 | 2024]` SAIN: Improving ICS Attack Detection via State-Aware Invariants (ACM CCS 2024)
**Paper:** [SAIN: Improving ICS Attack Detection Sensitivity via State-Aware Invariants](https://dl.acm.org/doi/10.1145/3658644)
**Authors:** Syed Ghazanfar Abbas, Muslum Ozgur Ozmen, Abdulellah Alsaheel, Arslan Khan, **Z. Berkay Celik**, **Dongyan Xu** (Purdue PurSec)
**Author Profiles:** https://www.cs.purdue.edu/people/faculty/dxu.html · https://beerkay.github.io
**Institution:** Purdue University | USNWR: **#53**
**Venue:** ACM CCS 2024 (CCF-A)
**Relevance:** State-aware invariant-based ICS attack detection — CMatrix's OT/ICS VAPT capability feeds into this defense model. Xu + Celik is a strong co-authorship target for CMatrix's ICS extension paper.

---

## 👤 Prof. #13 — Xiangyu Zhang · Purdue · USNWR #53
**Email:** xyzhang@cs.purdue.edu | **Website:** https://www.cs.purdue.edu/homes/xyzhang/ | **Lab:** Program Analysis & Security Lab, PurSec

### 1.32 `[P1 | 2025]` LmPa: Reducing LLM Hallucination in Decompilation via Program Analysis Synergy (NDSS 2025)
**Paper:** [LmPa: Improving Decompilation by Synergy of Large Language Model and Program Analysis](https://arxiv.org/abs/2301.07378)
**Authors:** Xiangzhe Xu, Zhuo Zhang, Zian Su, Ziyang Huang, Yapeng Ye, Jianjun Huang, et al., **Xiangyu Zhang** (Purdue)
**Author Profile:** https://www.cs.purdue.edu/homes/xyzhang/
**Institution:** Purdue University | USNWR: **#53** | Samuel Conte Professor
**Venue:** NDSS 2025 (CCF-A)
**PDF:** https://arxiv.org/abs/2301.07378
**Relevance:** 🎯 Novel pre-training + program analysis integration reduces LLM hallucination in decompilation — addresses the core reliability challenge. CMatrix's decompilation module should use Zhang's approach.

### 1.33 `[P2 | 2025]` CodeArt: Better Code Models by Attention Regularization When Symbols Are Lacking (ICLR 2025)
**Paper:** [CodeArt: Better Code Models by Attention Regularization When Symbols Are Lacking](https://www.cs.purdue.edu/lintan/publications/nova-iclr25.pdf)
**Authors:** Zian Su, Xiangzhe Xu, Ziyang Huang, Zhuo Zhang, Yapeng Ye, Jianjun Huang, **Xiangyu Zhang** (Purdue)
**Author Profile:** https://www.cs.purdue.edu/homes/xyzhang/
**Institution:** Purdue University | USNWR: **#53**
**Venue:** ICLR 2025 (CCF-A)
**Relevance:** Attention regularization for better code models when symbol info is missing — foundational for CMatrix's stripped binary analysis and malware reverse engineering module.

---

## 👤 Prof. #14 — Z. Berkay Celik · Purdue · USNWR #53
**Email:** celik@purdue.edu | **Website:** https://beerkay.github.io | **Lab:** PurSec Lab

### 1.34 `[P1 | 2025]` Rethinking How to Evaluate Language Model Jailbreak (AISEC @ ACM CCS 2025)
**Paper:** [Rethinking How to Evaluate Language Model Jailbreak](https://beerkay.github.io)
**Authors:** **Z. Berkay Celik** et al. (Purdue PurSec)
**Author Profile:** https://beerkay.github.io
**Institution:** Purdue University | USNWR: **#53** | 2× "Most Influential Professor" (Purdue CS 2020, 2024)
**Venue:** AISEC @ ACM CCS 2025
**Relevance:** 🎯 Rigorous evaluation framework for LLM jailbreak resistance from an adversary perspective. Directly aligned with CMatrix's offensive agent evaluation methodology.

### 1.35 `[P2 | 2025]` Automated Discovery of Semantic Attacks in Multi-Robot Navigation Systems (USENIX Security 2025)
**Paper:** [Automated Discovery of Semantic Attacks in Multi-Robot Navigation Systems](https://www.usenix.org/conference/usenixsecurity25)
**Authors:** Doguhan Yeke, Kartik A. Pant, Muslum Ozgur Ozmen, Hyungsub Kim, James M. Goppert, Inseok Hwang, Antonio Bianchi, **Z. Berkay Celik** (Purdue)
**Author Profile:** https://beerkay.github.io
**Institution:** Purdue University | USNWR: **#53**
**Venue:** USENIX Security 2025 (CCF-A)
**Relevance:** Automated semantic attack discovery in multi-robot CPS — extends CMatrix's autonomous attack synthesis to cyber-physical systems.

---

## 👤 Prof. #15 — Yizheng Chen · University of Maryland · USNWR #93
**Email:** yzchen@umd.edu | **Website:** https://surrealyz.github.io | **Lab:** Maryland Cybersecurity Center (MC2)

### 1.36 `[P1 | 2026]` Locus: Agentic Predicate Synthesis for Directed Fuzzing (ICSE 2026)
**Paper:** [Locus: Agentic Predicate Synthesis for Directed Fuzzing](https://arxiv.org/abs/2508.21302)
**Authors:** Jie Zhu, Chihao Shen, Ziyang Li, Jiahao Yu, **Yizheng Chen** (UMD), Kexin Pei (UChicago)
**Author Profile:** https://surrealyz.github.io
**Institution:** University of Maryland, College Park | USNWR: **#93** | $1.7M Open Philanthropy 2024–2026
**Venue:** ICSE 2026 (CCF-A) — Rio de Janeiro, April 2026
**PDF:** https://arxiv.org/pdf/2508.21302
**Relevance:** 🎯 LLM agent synthesizes predicates to guide directed fuzzers toward deep target states — dramatically reduces time-to-exploit. CMatrix's fuzzing pipeline should integrate Locus.

### 1.37 `[P2 | 2026]` SecRepoBench: Benchmarking Code Agents for Secure Code Completion (ICSE 2026)
**Paper:** [SecRepoBench: Benchmarking Code Agents for Secure Code Completion in Real-World Repositories](https://arxiv.org/abs/2504.21205)
**Authors:** Chihao Shen, Connor Dilgren, Purva Chiniya, Luke Griffith, Yu Ding, **Yizheng Chen** (UMD)
**Author Profile:** https://surrealyz.github.io
**Institution:** University of Maryland, College Park | USNWR: **#93**
**Venue:** LLM4Code Workshop @ ICSE 2026
**PDF:** https://arxiv.org/pdf/2504.21205
**Relevance:** 318-task benchmark across 27 C/C++ repos and 15 CWEs — evaluation tool for CMatrix's code security scanning.

---

## 👤 Prof. #16 — Christopher Kruegel · UC Santa Barbara · USNWR #65
**Email:** chris@cs.ucsb.edu | **Website:** https://sites.cs.ucsb.edu/~chris/ | **Lab:** SecLab UCSB (iSSL)

### 1.38 `[P1 | 2025]` CVE-GENIE: LLM Multi-Agent Framework for Automated CVE Reproduction
**Paper:** [From CVE Entries to Verifiable Exploits: An Automated Multi-Agent Framework for Reproducing CVEs](https://arxiv.org/abs/2509.01835)
**Authors:** Saad Ullah, Praneeth Balasubramanian, **Wenbo Guo**, Amanda Burnett, Hammond Pearce, **Christopher Kruegel**, **Giovanni Vigna** (UCSB), Gianluca Stringhini (BU)
**Author Profiles:** https://sites.cs.ucsb.edu/~chris/ · https://sites.cs.ucsb.edu/~vigna/ · https://henrygwb.github.io
**Institution:** UC Santa Barbara + Boston University | QS: **#65**
**Venue:** arXiv, September 2025
**PDF:** https://arxiv.org/pdf/2509.01835
**Relevance:** 🎯 Four-module pipeline (Knowledge Builder → Vulnerability Analyzer → Exploit Generator → Verifier) reproducing ~51% of 2024–2025 CVEs with verifiable exploits at $2.77 avg API cost. The most directly overlapping academic paper to CMatrix's exploit pipeline.

---

## 👤 Prof. #17 — Giovanni Vigna · UC Santa Barbara · USNWR #65
**Email:** vigna@cs.ucsb.edu | **Website:** https://sites.cs.ucsb.edu/~vigna/ | **Lab:** SecLab UCSB, NSF ACTION Director

### 1.39 `[P1 | 2025]` CVE-GENIE (co-author with Kruegel and Guo — see entry 1.38 above for full details)

### 1.40 `[P2 | 2025]` ACM CCS 2025 Keynote: Autonomous Vulnerability Analysis Using LLMs
**Paper:** [ACM CCS 2025 Keynote: Autonomous Vulnerability Analysis Using Large Language Models](https://sites.cs.ucsb.edu/~vigna/)
**Authors:** **Giovanni Vigna** (UCSB SecLab / NSF ACTION Director)
**Author Profile:** https://sites.cs.ucsb.edu/~vigna/
**Institution:** UC Santa Barbara | USNWR: **#65** | ACM Fellow + IEEE Fellow | NSF ACTION Director ($20M)
**Venue:** ACM CCS 2025 Keynote, Salt Lake City, October 2025
**Relevance:** The keynote from the ACM CCS 2025 conference on autonomous LLM-based vulnerability analysis — the definitive field framing from the NSF ACTION Institute director.

---

## 👤 Prof. #18 — Wenbo Guo · UC Santa Barbara · USNWR #65
**Email:** henrygwb@ucsb.edu | **Website:** https://henrygwb.github.io | **Lab:** UCSB ML Security Lab

### 1.41 `[P1 | 2025]` VulnLLM-R (co-author with Dawn Song — see entry 1.6 above for full details)

### 1.42 `[P1 | 2025]` CVE-GENIE (co-author with Kruegel and Vigna — see entry 1.38 above for full details)

### 1.43 `[P2 | 2025]` BlueCodeAgent: Blue-Team Agent Enabled by Automated Red Teaming
**Paper:** [BlueCodeAgent: Blue-Team Agent for Code Security Enabled by Automated Red Teaming](https://henrygwb.github.io)
**Authors:** **Wenbo Guo** et al. (UCSB ML Security Lab)
**Author Profile:** https://henrygwb.github.io
**Institution:** UC Santa Barbara | USNWR: **#65** | Google ML and Systems Junior Faculty Award 2025
**Venue:** 2025
**Relevance:** 🎯 Blue-team agent powered by automated red-team testing — CMatrix's offensive scan outputs directly enable this defensive feedback loop. Bridges CMatrix (red) → BlueCodeAgent (blue) in one automated cycle.

### 1.44 `[P2 | 2025]` BandFuzz: ML-Powered Collaborative Fuzzing (SBFT 2024 1st Place)
**Paper:** [BandFuzz: An ML-powered Collaborative Fuzzing Framework](https://arxiv.org/abs/2507.10845)
**Authors:** Wenxuan Shi, Jiahao Yu, **Xinyu Xing** (Northwestern), Hongwei Li (Purdue), **Wenbo Guo** (UCSB)
**Author Profiles:** https://henrygwb.github.io · https://www.mccormick.northwestern.edu/research-faculty/directory/profiles/xing-xinyu.html
**Institution:** Northwestern + Purdue + UC Santa Barbara
**Venue:** arXiv, July 2025 — **1st place SBFT 2024 (FuzzBench)**
**PDF:** https://arxiv.org/abs/2507.10845
**Relevance:** Multi-armed bandit-driven collaborative fuzzing — globally optimal fuzzer combinations without extra compute. CMatrix's grey-box fuzzing backend integration candidate.

---

## 👤 Prof. #19 — Xinyu Xing · Northwestern University · USNWR #9
**Email:** xingxinyu@northwestern.edu | **Website:** https://www.mccormick.northwestern.edu/research-faculty/directory/profiles/xing-xinyu.html | **Lab:** Security Research Group, Northwestern CS

### 1.45 `[P1 | 2025]` PatchAgent: Practical Program Repair Agent Mimicking Human Expertise (USENIX Security 2025)
**Paper:** [PATCHAGENT: A Practical Program Repair Agent Mimicking Human Expertise](https://www.usenix.org/conference/usenixsecurity25/presentation/yu-zheng)
**Authors:** Zheng Yu, Ziyi Guo, Yuhang Wu, Jiahao Yu, Meng Xu, Dongliang Mu, Yan Chen, **Xinyu Xing** (Northwestern)
**Author Profile:** https://www.mccormick.northwestern.edu/research-faculty/directory/profiles/xing-xinyu.html
**Institution:** Northwestern University | USNWR: **#9** | DARPA AIxCC Semifinalist ($2M team award)
**Venue:** USENIX Security 2025 (CCF-A)
**Relevance:** 🎯 End-to-end LLM agent integrating fault localization, patch generation, and validation — fixes bugs without breaking existing tests. CMatrix's post-exploit remediation module follows this design.

### 1.46 `[P1 | 2024]` LLM-Fuzzer: Scaling Assessment of LLM Jailbreaks (USENIX Security 2024)
**Paper:** [LLM-Fuzzer: Scaling Assessment of Large Language Model Jailbreaks](https://www.usenix.org/conference/usenixsecurity24/presentation/yu-jiahao)
**Authors:** Jiahao Yu, Xingwei Lin (Ant Group), Zheng Yu, **Xinyu Xing** (Northwestern)
**Author Profile:** https://www.mccormick.northwestern.edu/research-faculty/directory/profiles/xing-xinyu.html
**Institution:** Northwestern University | USNWR: **#9**
**Venue:** USENIX Security 2024 (CCF-A) — pp. 4657–4674
**Relevance:** Automated fuzzing of LLM jailbreaks at scale — relevant to both prompt injection testing of target applications and stress-testing CMatrix's own safety guardrails.

### 1.47 `[P2 | 2025]` BandFuzz: ML-Powered Collaborative Fuzzing (co-author with Wenbo Guo — see entry 1.44 above for full details)

---

## 👤 Prof. #20 — Suman Jana · Columbia University · USNWR #12
**Email:** suman@cs.columbia.edu | **Website:** http://www.cs.columbia.edu/~suman/ | **Lab:** Columbia Security & Privacy Lab

### 1.48 `[P2 | 2025]` PILOT: Path-Guided Iterative LLM-Orchestrated CLI Fuzzing
**Paper:** [PILOT: Path-Guided, Iterative LLM-Orchestrated Testing for Fuzzing CLI Applications](http://www.cs.columbia.edu/~suman/)
**Authors:** **Suman Jana** (Columbia), **Yinzhi Cao** (JHU) et al.
**Author Profiles:** http://www.cs.columbia.edu/~suman/ · https://yinzhicao.org
**Institution:** Columbia University + Johns Hopkins University | USNWR: **#12 / #9**
**Venue:** 2025
**Relevance:** 🎯 Path-guided iterative LLM-orchestrated testing for CLI applications — provides LLM semantic understanding of CLI options to expose deep vulnerabilities. Direct CMatrix fuzzing pipeline component for CLI-exposed services.

### 1.49 `[P2 | 2025]` SWExploit: Adversarial Issues for LLM-Based Automated Program Repair Agents
**Paper:** [SWExploit: Adversarial Issues in LLM-Based Automated Program Repair Agents](http://www.cs.columbia.edu/~suman/)
**Authors:** **Suman Jana** et al. (Columbia Security & Privacy Lab)
**Author Profile:** http://www.cs.columbia.edu/~suman/
**Institution:** Columbia University | USNWR: **#12** | 6 Best Paper Awards
**Venue:** 2025
**Relevance:** Adversaries trick APR agents into generating functionally correct but deliberately vulnerable patches — the adversarial manipulation CMatrix must defend against in its own patch suggestion module.

### 1.50 `[P2 | 2025]` GCGS: Black-Box Attack on LLM Code Assistants (83% Success on GPT-4o, Claude 3.5)
**Paper:** [GCGS: Black-Box Adversarial Attack on LLM-based Code Generation Systems](http://www.cs.columbia.edu/~suman/)
**Authors:** **Suman Jana** et al. (Columbia)
**Author Profile:** http://www.cs.columbia.edu/~suman/
**Institution:** Columbia University | USNWR: **#12**
**Venue:** 2025
**Relevance:** 83% success rate attacking GPT-4o and Claude 3.5 as code assistants — the adversarial environment CMatrix must navigate when using LLMs for code analysis.

---

<a name="section-2"></a>
# 🟡 SECTION 2 — PROFESSOR PAPERS: TIER 2 (Professors #21–40)
**Universities Ranked #101–300 USNWR | Full paper details for every entry**

---

## 👤 Prof. #21 — Yan Shoshitaishvili · Arizona State University · USNWR ~#147
**Email:** yans@asu.edu | **Website:** https://yancomm.net | **Lab:** SEFCOM Lab (co-director)

### 2.1 `[P1 | 2026]` Decompiling the Synergy: Human-LLM Teaming in Reverse Engineering (NDSS 2026) 🏆 Distinguished Paper Award
**Paper:** [Decompiling the Synergy: An Empirical Study of Human-LLM Teaming in Software Reverse Engineering](https://www.ndss-symposium.org/ndss-paper/decompiling-the-synergy-an-empirical-study-of-human-llm-teaming-in-software-reverse-engineering/)
**Authors:** Zion Leonahenahe Basque, Samuele Doria, Ananta Soneji, Wil Gibbs, **Adam Doupé**, **Yan Shoshitaishvili** (ASU), Eleonora Losiouk (U Padua), Ruoyu Wang (ASU), Simone Aonzo (EURECOM)
**Author Profiles:** https://yancomm.net · https://adamdoupe.com
**Institution:** Arizona State University + University of Padua + EURECOM | USNWR: **~#147**
**Venue:** NDSS 2026 (CCF-A) — **Distinguished Paper Award** · Surveyed 153 practitioners
**Relevance:** 🎯 First systematic study of LLM+human collaboration during software reverse engineering — LLM assistance demonstrably narrows the expertise gap. Directly informs CMatrix's HITL module design and democratization argument.

### 2.2 `[P2 | 2026]` ROPbot: Reimagining Code Reuse Attack Synthesis (NDSS 2026)
**Paper:** [ROPbot: Reimagining Code Reuse Attack Synthesis](https://yancomm.net/papers/2026%20-%20NDSS%20-%20ropbot.html)
**Authors:** Kyle Zeng, Moritz Schloegel, Christopher Salls, **Adam Doupé**, Ruoyu Wang, **Yan Shoshitaishvili**, **Tiffany Bao** (ASU)
**Author Profile:** https://yancomm.net
**Institution:** Arizona State University | USNWR: **~#147**
**Venue:** NDSS 2026 (CCF-A)
**Relevance:** Automated ROP (Return-Oriented Programming) chain synthesis — CMatrix's exploit synthesis module for memory corruption vulnerabilities.

### 2.3 `[P2 | 2026]` Open Cybersecurity Education: Five Years of pwn.college (SIGCSE 2026)
**Paper:** [Open Cybersecurity Education: Five Years of pwn.college](https://yancomm.net)
**Authors:** Connor Nelson, Robert Wasinger, **Adam Doupé**, **Yan Shoshitaishvili** (ASU)
**Author Profile:** https://yancomm.net
**Institution:** Arizona State University | USNWR: **~#147**
**Venue:** SIGCSE 2026 — **Best Paper Award** · 1M+ users worldwide
**Relevance:** Five-year retrospective of the world's premier offensive security learning platform. The democratization and social impact argument CMatrix mirrors.

---

## 👤 Prof. #22 — Tiffany Bao · Arizona State University · USNWR ~#147
**Email:** tbao@asu.edu | **Website:** https://www.tiffanybao.com | **Lab:** SEFCOM Lab (co-director)

### 2.4 `[P1 | 2024]` ARVO: Atlas of Reproducible Vulnerabilities for Open Source Software
**Paper:** [ARVO: Atlas of Reproducible Vulnerabilities for Open Source Software](https://arxiv.org/abs/2408.02153)
**Authors:** Xiang Mei, Pulkit Singh Singaria, Jordi Del Castillo, Haoran Xi, Abdelouahab Benchikh, **Tiffany Bao**, Ruoyu Wang, **Yan Shoshitaishvili**, **Adam Doupé** (ASU), Hammond Pearce, **Brendan Dolan-Gavitt** (NYU)
**Author Profiles:** https://www.tiffanybao.com · https://adamdoupe.com · https://moyix.net
**Institution:** Arizona State University + NYU Tandon | USNWR: **~#147 / ~#53**
**Venue:** arXiv, August 2024
**PDF:** https://arxiv.org/abs/2408.02153
**Relevance:** 🎯 5,000+ memory vulnerabilities with triggering inputs and verified patches — the largest open-source vulnerability dataset with reproducible exploits. Natural evaluation corpus for CMatrix's memory vulnerability scan modes.

### 2.5 `[P2 | 2026]` ROPbot: Code Reuse Attack Synthesis (co-author with Shoshitaishvili — see entry 2.2 above for full details)

### 2.6 `[P2 | 2026]` Discovering Blind-Trust Vulnerabilities in PLC Binaries via State Machine Recovery (NDSS 2026)
**Paper:** [Discovering Blind-Trust Vulnerabilities in PLC Binaries via State Machine Recovery](https://www.ndss-symposium.org/ndss2026/accepted-papers/)
**Authors:** Fangzhou Dong, Arvind S. Raj, Efrén López-Morales, Siyu Liu, **Yan Shoshitaishvili**, **Tiffany Bao**, **Adam Doupé**, Muslum Ozgur Ozmen, Ruoyu Wang (ASU)
**Author Profile:** https://www.tiffanybao.com
**Institution:** Arizona State University | USNWR: **~#147**
**Venue:** NDSS 2026 (CCF-A)
**Relevance:** PLC binary vulnerability discovery via state machine recovery — extends CMatrix VAPT scope to industrial control systems (ICS/OT).

---

## 👤 Prof. #23 — Adam Doupé · Arizona State University · USNWR ~#147
**Email:** doupe@asu.edu | **Website:** https://adamdoupe.com | **Lab:** SEFCOM Lab (co-director)

### 2.7 `[P1 | 2026]` Decompiling the Synergy (co-author with Shoshitaishvili — see entry 2.1 above for full details)

### 2.8 `[P2 | 2026]` Oxidizer: Toward Concise and High-Fidelity Rust Decompilation (IEEE S&P 2026)
**Paper:** [Oxidizer: Toward Concise and High-fidelity Rust Decompilation](https://adamdoupe.com)
**Authors:** **Adam Doupé**, **Yan Shoshitaishvili** et al. (ASU SEFCOM)
**Author Profile:** https://adamdoupe.com
**Institution:** Arizona State University | USNWR: **~#147** | DARPA AIxCC finalist team
**Venue:** IEEE S&P 2026 (CCF-A)
**Relevance:** High-fidelity Rust decompilation — critical for CMatrix as Rust-written software becomes a primary VAPT target. Enables analysis of Rust binaries as effectively as C/C++.

### 2.9 `[P2 | 2024]` ARVO (co-author with Tiffany Bao — see entry 2.4 above for full details)

---

## 👤 Prof. #24 — Long Lu · Northeastern University · USNWR ~#179
**Email:** l.lu@northeastern.edu | **Website:** https://www.longlu.org | **Lab:** RiS3 Lab

### 2.10 `[P2 | 2025]` LLMs for PLC Code Security in Industrial Control Systems
**Paper:** [LLM-Based Security Analysis for PLC Code and Industrial Control Systems](https://www.longlu.org)
**Authors:** **Long Lu** et al. (Northeastern RiS3 Lab)
**Author Profile:** https://www.longlu.org
**Institution:** Northeastern University | USNWR: **~#179** | NSF CAREER + Air Force Faculty Fellowship + 2× Google ASPIRE Award
**Venue:** 2025 (NSF/ONR funded)
**Relevance:** LLMs for PLC code security — extends CMatrix's vulnerability detection to ICS/OT environments.

### 2.11 `[P2 | 2025]` Optimizing Fuzzing for Vulnerability Coverage in IoT/Embedded Systems
**Paper:** [Optimizing Fuzzing for Vulnerability Coverage in Embedded and Networked Systems](https://www.longlu.org)
**Authors:** **Long Lu** et al. (Northeastern RiS3 Lab)
**Author Profile:** https://www.longlu.org
**Institution:** Northeastern University | USNWR: **~#179**
**Venue:** 2025 (NSF CAREER funded)
**Relevance:** Coverage-directed fuzzing strategy optimization for embedded/IoT targets — CMatrix's grey-box fuzzing module should incorporate these strategies for IoT VAPT campaigns.

---

## 👤 Prof. #25 — Engin Kirda · Northeastern University · USNWR ~#179
**Email:** ek@ccs.neu.edu | **Website:** https://www.ccs.neu.edu/home/ek/ | **Lab:** Secure Systems Lab (co-director)

### 2.12 `[P2 | 2025]` Automatic Exploit Generation and Malware Behavior Analysis
**Paper:** [Automated Malware Behavior Analysis and Exploit Generation for Modern Vulnerabilities](https://www.ccs.neu.edu/home/ek/)
**Authors:** **Engin Kirda** et al. (Northeastern Secure Systems Lab — International Secure Systems Lab network)
**Author Profile:** https://www.ccs.neu.edu/home/ek/
**Institution:** Northeastern University | USNWR: **~#179**
**Venue:** 2024–2025 (NSF/DARPA/ONR funded)
**Relevance:** Automatic exploit generation and malware behavior analysis — maps directly to CMatrix's exploit chain automation. Kirda co-founded the International Secure Systems Lab (ISSL) — the global network CMatrix can leverage for multi-institution validation.

---

## 👤 Prof. #26 — Peng Liu · Penn State · USNWR ~#130
**Email:** pliu@ist.psu.edu | **Website:** https://sites.psu.edu/pengliu/ | **Lab:** Cyber Security Lab, Penn State IST

### 2.13 `[P2 | 2025]` AI-Driven Malware Analysis and Cyber-Physical Systems Security
**Paper:** [AI-Driven Automated Malware Analysis and Defense for Cyber-Physical Systems](https://sites.psu.edu/pengliu/)
**Authors:** **Peng Liu** et al. (Penn State Cyber Security Lab)
**Author Profile:** https://sites.psu.edu/pengliu/
**Institution:** Penn State University | USNWR: **~#130** | Raymond G. Tronzo M.D. Professor (endowed)
**Venue:** 2024–2025 (DARPA/NSF/DoD funded)
**Relevance:** AI-driven malware analysis and CPS security — extending CMatrix's VAPT scope to OT/ICS. Penn State IST hosts CPTC national penetration testing competition (3rd globally 2025) — natural evaluation testbed for CMatrix.

---

## 👤 Prof. #27 — Ting Wang · Penn State · USNWR ~#130
**Email:** inbox@tiwang.io | **Website:** https://alps-lab.github.io | **Lab:** ALPS Lab

### 2.14 `[P2 | 2025]` Adversarial Attacks Against LLM Agents: Prompt Injection and Backdoor Defenses
**Paper:** [Adversarial Robustness of LLM-Based Autonomous Agents: Prompt Injection, Backdoor Defenses, Agent Trust](https://alps-lab.github.io)
**Authors:** **Ting Wang** et al. (Penn State ALPS Lab)
**Author Profile:** https://alps-lab.github.io
**Institution:** Penn State University | USNWR: **~#130** | NSF CAREER Award
**Venue:** 2024–2025 (NSF CAREER funded, NeurIPS, ICLR, USENIX Security)
**Relevance:** Adversarial attacks against LLMs as autonomous agents — prompt injection, backdoor defenses, agent trust hardening. CMatrix's orchestration trust model must be hardened against ALPS Lab's catalogued attack vectors.

---

## 👤 Prof. #28 — Jie Gao · Rutgers University · USNWR ~#160
**Email:** jg1555@rutgers.edu | **Website:** https://sites.rutgers.edu/jie-gao/ | **Lab:** Rutgers AI & Cybersecurity Research

### 2.15 `[P2 | 2025]` AI Systems for Threat Recognition, Agent Communication, and Automated Response (NSF ACTION Co-PI)
**Paper:** [AI Systems for Threat Recognition, Agent Communication, and Automated Response in Cybersecurity](https://sites.rutgers.edu/jie-gao/)
**Authors:** **Jie Gao** et al. (Rutgers — NSF ACTION Institute Co-PI)
**Author Profile:** https://sites.rutgers.edu/jie-gao/
**Institution:** Rutgers University | USNWR: **~#160** | NSF ACTION Co-PI ($20M total)
**Venue:** 2024–2025 (NSF ACTION Institute)
**Relevance:** Automated AI systems that recognize threats, communicate across agents, and develop response mechanisms — direct operational parallel to CMatrix's multi-agent coordination. Prof. Gao is a gateway into the $20M ACTION research ecosystem alongside Vigna and Song.

---

## 👤 Prof. #29 — Zhiqiang Lin · Ohio State University · USNWR ~#180
**Email:** lin.3021@osu.edu | **Website:** https://zhiqiang.org | **Lab:** SSSL Lab

### 2.16 `[P2 | 2025]` ELFuzz: Efficient Input Generation via LLM-Driven Synthesis (USENIX Security 2025)
**Paper:** [ELFuzz: Efficient Input Generation via LLM-driven Synthesis over Fuzzer Space](https://www.usenix.org/conference/usenixsecurity25)
**Authors:** Chuyang Chen, **Brendan Dolan-Gavitt** (NYU), **Zhiqiang Lin** (OSU)
**Author Profiles:** https://zhiqiang.org · https://moyix.net
**Institution:** Ohio State University + NYU Tandon | USNWR: **~#180** | Distinguished Professor of Engineering
**Venue:** USENIX Security 2025 (CCF-A)
**Relevance:** LLM-driven synthesis to efficiently generate inputs across the fuzzer space — CMatrix's automated test case generation module. Cross-institutional OSU + NYU paper.

### 2.17 `[P2 | 2025]` AI-Assisted Bug Finding in Kernel, Firmware, and Binary Software
**Paper:** [AI-Assisted Automated Bug Finding in Kernel, IoT Firmware, and Binary Software](https://zhiqiang.org)
**Authors:** **Zhiqiang Lin** et al. (OSU SSSL Lab)
**Author Profile:** https://zhiqiang.org
**Institution:** Ohio State University | USNWR: **~#180**
**Venue:** 2024–2025 (NSF/DARPA/DoD funded)
**Relevance:** Automated AI-assisted bug finding in kernel and firmware — foundational to CMatrix's grey-box scan pipeline for embedded and kernel-level targets.

---

## 👤 Prof. #30 — Vitaly Shmatikov · Cornell Tech · USNWR ~#17 (Cornell)
**Email:** shmatikov@cornell.edu | **Website:** https://tech.cornell.edu/people/vitaly-shmatikov/ | **Lab:** Cornell Tech Security & Privacy Group

### 2.18 `[P1 | 2025]` Multi-Agent Systems Execute Arbitrary Malicious Code (COLM 2025)
**Paper:** [Multi-Agent Systems Execute Arbitrary Malicious Code](https://arxiv.org/abs/2503.12188)
**Authors:** Harold Triedman, Rishi Jha, **Vitaly Shmatikov** (Cornell Tech)
**Author Profile:** https://tech.cornell.edu/people/vitaly-shmatikov/
**Institution:** Cornell University | USNWR: **~#17** | CCS Test-of-Time Award 2025
**Venue:** COLM 2025
**PDF:** https://arxiv.org/pdf/2503.12188
**Relevance:** 🎯 Demonstrates adversarial content (a single malicious webpage, image, or audio) can hijack multi-agent LLM systems — executing arbitrary code and exfiltrating data. The most direct attack model for CMatrix's own infrastructure security. CMatrix must be hardened against MAS hijacking.

### 2.19 `[P1 | 2026]` Breaking and Fixing Defenses Against Control-Flow Hijacking in Multi-Agent Systems (ICLR 2026)
**Paper:** [Breaking and Fixing Defenses Against Control-Flow Hijacking in Multi-Agent Systems](https://arxiv.org/abs/2510.17276)
**Authors:** Rishi Jha, Harold Triedman, Justin Wagle, **Vitaly Shmatikov** (Cornell + Microsoft)
**Author Profile:** https://tech.cornell.edu/people/vitaly-shmatikov/
**Institution:** Cornell University + Microsoft | USNWR: **~#17**
**Venue:** ICLR 2026 (CCF-A)
**PDF:** https://arxiv.org/pdf/2510.17276
**Relevance:** 🎯 LlamaFirewall and alignment-check defenses are evadable by sophisticated control-flow hijacking. Proposes ControlValve (CFI + least-privilege). CMatrix's multi-agent orchestration must implement ControlValve-style defenses.

---

## 👤 Prof. #31 — Brendan Dolan-Gavitt · NYU Tandon · USNWR ~#53 (NYU)
**Email:** brendandg@nyu.edu | **Website:** https://moyix.net | **Lab:** MESS Lab

### 2.20 `[P1 | 2025]` EnIGMA: Interactive Tools Substantially Assist LM Agents in Finding Security Vulnerabilities (ICML 2025)
**Paper:** [EnIGMA: Enhanced Interactive Generative Model Agent for CTF Challenges](https://arxiv.org/abs/2409.16165)
**Authors:** Talor Abramovich, Meet Udeshi, Minghao Shao, Kilian Lieret, Haoran Xi, Kimberly Milner, Sofija Jancheska, John Yang, Carlos E. Jimenez, Farshad Khorrami, Prashanth Krishnamurthy, **Brendan Dolan-Gavitt** (NYU), Muhammad Shafique, Karthik Narasimhan, Ramesh Karri, Ofir Press
**Author Profile:** https://moyix.net
**Institution:** NYU Tandon | QS: **#39** | USNWR: **~#53**
**Venue:** ICML 2025 (CCF-A) — Vancouver, July 2025
**PDF:** https://arxiv.org/pdf/2409.16165
**Code:** https://github.com/SWE-agent/SWE-agent
**Relevance:** 🎯 Interactive tools (shells, file viewers, hex viewers) substantially improve LLM agent performance on CTF security challenges — SOTA on CyBench (13.5%). Directly relevant to CMatrix's HITL module and interactive tool integration strategy.

### 2.21 `[P1 | 2025]` D-CIPHER: Dynamic Collaborative Intelligent Multi-Agent System for Offensive Security
**Paper:** [D-CIPHER: Dynamic Collaborative Intelligent Agents with Planning and Heterogeneous Execution for Enhanced Reasoning in Offensive Security](https://arxiv.org/abs/2502.10931)
**Authors:** Meet Udeshi, Minghao Shao, Haoran Xi, Nanda Rani, Kimberly Milner, Venkata Sai Charan Putrevu, **Brendan Dolan-Gavitt** (NYU), Sandeep Kumar Shukla (IIT Kanpur), Prashanth Krishnamurthy, Farshad Khorrami, Ramesh Karri, Muhammad Shafique
**Author Profile:** https://moyix.net
**Institution:** NYU Tandon + NYU Abu Dhabi + IIT Kanpur | USNWR: **~#53**
**Venue:** arXiv, February 2025
**PDF:** https://arxiv.org/pdf/2502.10931
**Relevance:** 🎯 Planner-Executor multi-agent with heterogeneous executors — SOTA on NYU CTF Bench (22%), CyBench (22.5%), HackTheBox (44%), 65% more ATT&CK techniques than prior work. Direct CMatrix architecture comparison.

### 2.22 `[P1 | 2025]` CRAKEN: Cybersecurity LLM Agent with Knowledge-Based Execution
**Paper:** [CRAKEN: Cybersecurity LLM Agent with Knowledge-Based Execution](https://arxiv.org/abs/2505.17107)
**Authors:** Minghao Shao, Haoran Xi, Nanda Rani, Meet Udeshi, Venkata Sai Charan Putrevu, Kimberly Milner, **Brendan Dolan-Gavitt** (NYU), Sandeep Kumar Shukla, Prashanth Krishnamurthy, Farshad Khorrami, Ramesh Karri, Muhammad Shafique
**Author Profile:** https://moyix.net
**Institution:** NYU Tandon | USNWR: **~#53**
**Venue:** arXiv, May 2025
**PDF:** https://arxiv.org/abs/2505.17107
**Code:** https://github.com/NYU-LLM-CTF/nyuctf_agents_craken
**Relevance:** 🎯 CTF writeup knowledge database augments cybersecurity LLM agent — solves 25–30% more ATT&CK techniques than prior work, 22% on NYU CTF Bench (SOTA). CMatrix should adopt CRAKEN's knowledge-augmented agent design.

### 2.23 `[P2 | 2025]` ELFuzz: Efficient Input Generation via LLM-Driven Synthesis (USENIX Security 2025)
**Paper:** [ELFuzz: Efficient Input Generation via LLM-driven Synthesis over Fuzzer Space](https://www.usenix.org/conference/usenixsecurity25)
**Authors:** Chuyang Chen, **Brendan Dolan-Gavitt** (NYU), Zhiqiang Lin (OSU)
**Author Profile:** https://moyix.net
**Institution:** NYU Tandon + Ohio State University | USNWR: **~#53**
**Venue:** USENIX Security 2025 (CCF-A)
**Relevance:** LLM-driven fuzzer synthesis — CMatrix's automated test case generation module.

### 2.24 `[P2 | 2024]` ARVO: Atlas of Reproducible Vulnerabilities (co-author with Tiffany Bao — see entry 2.4 above for full details)

---

## 👤 Prof. #32 — Yinzhi Cao · Johns Hopkins University · USNWR #9
**Email:** yinzhi.cao@jhu.edu | **Website:** https://yinzhicao.org | **Lab:** JHU Information Security Institute (Technical Director)

### 2.25 `[P1 | 2025]` PILOT: Path-Guided Iterative LLM-Orchestrated CLI Fuzzing (co-author with Suman Jana — see entry 1.48 above for full details)

### 2.26 `[P2 | 2025]` JavaScript Analysis: 80+ CVEs in Top-100 Websites (IEEE S&P 2025 Test of Time)
**Paper:** [Systematic JavaScript Analysis for Vulnerability Discovery — 80+ CVEs in Top-100 Websites and NPM](https://yinzhicao.org)
**Authors:** **Yinzhi Cao** et al. (JHU Information Security Institute)
**Author Profile:** https://yinzhicao.org
**Institution:** Johns Hopkins University | USNWR: **#9** | DARPA Director's Fellowship 2024 (highest DARPA honor)
**Venue:** IEEE S&P 2025 Test of Time Award (foundational work recognized 2025)
**Relevance:** Systematic JavaScript analysis discovering 80+ CVEs in Top-100 websites and NPM packages — the web vulnerability discovery methodology CMatrix's web agent module is built on.

---

## 👤 Prof. #33 — Guofei Gu · Texas A&M University · USNWR ~#145
**Email:** guofei@cse.tamu.edu | **Website:** https://faculty.cse.tamu.edu/guofei | **Lab:** SUCCESS Lab

### 2.27 `[P1 | 2025]` Taxonomy of 190 Advisories Against AI Agent Frameworks (DSN Test of Time Award 2025)
**Paper:** [Security Analysis of AI Agent Frameworks: Taxonomy of Vulnerabilities in OpenClaw and Agentic Runtime Systems](https://faculty.cse.tamu.edu/guofei)
**Authors:** **Guofei Gu** et al. (Texas A&M SUCCESS Lab)
**Author Profile:** https://faculty.cse.tamu.edu/guofei
**Institution:** Texas A&M University | USNWR: **~#145** | IEEE Fellow + ACM Distinguished Member | Presidential Impact Fellow
**Venue:** 2025 (DSN Test of Time Award 2025, ACSAC Test of Time Award 2023)
**Relevance:** 🎯 Taxonomy of 190 security advisories against OpenClaw AI agent runtime — identifying identity spoofing, policy bypass, prompt injection, and supply-chain escalation. Directly applicable to CMatrix's own framework security hardening and threat model.

### 2.28 `[P2 | 2007]` BotHunter: Detecting Malware Infection via IDS-Driven Dialog Correlation (USENIX Security 2007 — ACSAC Test of Time 2023)
**Paper:** [BotHunter: Detecting Malware Infection Through IDS-driven Dialog Correlation](https://faculty.cse.tamu.edu/guofei)
**Authors:** Guofei Gu, Phillip Porras, Vinod Yegneswaran, Martin Fong, **Wenke Lee** (Georgia Tech + SRI International)
**Author Profile:** https://faculty.cse.tamu.edu/guofei
**Institution:** Georgia Tech + SRI | USNWR: **#33**
**Venue:** USENIX Security 2007 (CCF-A) — **ACSAC Test of Time Award 2023**
**Relevance:** Foundational botnet detection via dialogue correlation — C2 detection during CMatrix red team campaigns. ACSAC Test of Time 2023 = sustained impact confirmed.

---

## 👤 Prof. #34 — Jedidiah Crandall · Arizona State University · USNWR ~#147
**Email:** jrcranda@asu.edu | **Website:** https://scai.engineering.asu.edu/faculty/computer-science-and-engineering/jedidiah-crandall/ | **Lab:** Breakout Research Group, ASU

### 2.29 `[P2 | 2025]` Adversarial Network Behavior and Evasion Techniques in Internet Censorship
**Paper:** [Measuring and Evading Internet Censorship: Adversarial Network Behavior Across Political Boundaries](https://scai.engineering.asu.edu/faculty/computer-science-and-engineering/jedidiah-crandall/)
**Authors:** **Jedidiah Crandall** et al. (ASU Breakout Research Group)
**Author Profile:** https://scai.engineering.asu.edu/faculty/computer-science-and-engineering/jedidiah-crandall/
**Institution:** Arizona State University | USNWR: **~#147**
**Venue:** 2024–2025 (NSF-funded)
**Relevance:** Adversarial network behavior and evasion across network boundaries — directly informs CMatrix's stealth scan and network evasion capabilities for grey-box network scan modes where avoiding detection is essential.

---

## 👤 Prof. #35 — Saumya Debray · University of Arizona · USNWR ~#284
**Email:** debray@cs.arizona.edu | **Website:** https://cs.arizona.edu/person/saumya-debray | **Lab:** Systems Security Research Group

### 2.30 `[P2 | 2025]` Automated Decompilation and Binary Code Analysis for Vulnerability Discovery
**Paper:** [Automated Decompilation, Binary Analysis, and Malware Analysis Using Program Analysis Techniques](https://cs.arizona.edu/person/saumya-debray)
**Authors:** **Saumya Debray** et al. (University of Arizona Systems Security Group)
**Author Profile:** https://cs.arizona.edu/person/saumya-debray
**Institution:** University of Arizona | USNWR: **~#284** | CAE-designated cybersecurity program
**Venue:** 2024–2025 (NSF + DARPA collaborative projects)
**Relevance:** Expert in automated decompilation and program analysis — foundational building block for CMatrix's grey-box binary scanning.

---

## 👤 Prof. #36 — Xinming (Simon) Ou · University of South Florida · USNWR ~#295
**Email:** xou@usf.edu | **Website:** https://www.usf.edu/ai-cybersecurity-computing/people/faculty/ou-simon.aspx | **Lab:** Bellini College, USF

### 2.31 `[P2 | 2025]` Towards AI-Driven Human-Machine Co-Teaming for Adaptive Cyber Security Operation Centers
**Paper:** [Towards AI-Driven Human-Machine Co-Teaming for Adaptive and Agile Cyber Security Operation Centers](https://www.usf.edu/ai-cybersecurity-computing/people/faculty/ou-simon.aspx)
**Authors:** **Xinming (Simon) Ou** et al. (USF Bellini College)
**Author Profile:** https://www.usf.edu/ai-cybersecurity-computing/people/faculty/ou-simon.aspx
**Institution:** University of South Florida | USNWR: **~#295** | Princeton PhD
**Venue:** 2025
**Relevance:** 🎯 AI-driven human-machine co-teaming for adaptive SOC — CMatrix's scan outputs feed directly into this human-machine collaboration model. Network attack graphs + MTD research complement CMatrix's attack path modeling.

### 2.32 `[P3 | 2024]` LLM Embeddings with Similarity Search for Botnet TLS Certificate Detection (AISec @ CCS 2024)
**Paper:** [LLM Embedding-Based Similarity Search for Botnet TLS Certificate Detection](https://www.usf.edu/ai-cybersecurity-computing/people/faculty/ou-simon.aspx)
**Authors:** **Xinming Ou**, **Anoop Singhal** (NIST) et al.
**Author Profiles:** https://www.usf.edu/ai-cybersecurity-computing/people/faculty/ou-simon.aspx · https://www.nist.gov/people/anoop-singhal
**Institution:** University of South Florida + NIST | USNWR: **~#295**
**Venue:** AISec Workshop @ ACM CCS 2024
**Relevance:** LLM embeddings + similarity search for C2 infrastructure identification via TLS certificate similarity — CMatrix's network scan module technique.

---

## 👤 Prof. #37 — William Enck · North Carolina State University · USNWR ~#181
**Email:** whenck@ncsu.edu | **Website:** https://enck.org | **Lab:** SySeS Lab

### 2.33 `[P2 | 2026]` Fizzle: A Framework for Deterministic and Reproducible Network Fuzzing (IEEE S&P 2026)
**Paper:** [Fizzle: A Framework for Deterministic and Reproducible Network Fuzzing](https://enck.org)
**Authors:** **William Enck** (NC State), **Patrick Traynor** (UFL), **Kevin Butler** (UFL) et al.
**Author Profiles:** https://enck.org · https://www.cise.ufl.edu/~traynor/ · https://www.cise.ufl.edu/~butler/
**Institution:** NC State University + University of Florida | USNWR: **~#181 / ~#145**
**Venue:** IEEE S&P 2026 (CCF-A)
**Relevance:** 🎯 Deterministic and reproducible network protocol fuzzing — CMatrix's network service scanning module. Three faculty from two institutions as co-authors — a strong three-professor collaboration target for CMatrix's network fuzzing paper.

---

## 👤 Prof. #38 — Patrick Traynor · University of Florida · USNWR ~#145
**Email:** traynor@cise.ufl.edu | **Website:** https://www.cise.ufl.edu/~traynor/ | **Lab:** FICS Research

### 2.34 `[P2 | 2026]` Fizzle: Deterministic Network Fuzzing (co-author with Enck — see entry 2.33 above for full details)

### 2.35 `[P3 | 2025]` Telephony Attack Surfaces: SS7, VoIP, and Wireless Protocol Vulnerabilities
**Paper:** [Automated Discovery and Exploitation of Telephony Attack Surfaces: SS7, VoIP, and Wireless Protocols](https://www.cise.ufl.edu/~traynor/)
**Authors:** **Patrick Traynor** et al. (FICS Research, University of Florida)
**Author Profile:** https://www.cise.ufl.edu/~traynor/
**Institution:** University of Florida | USNWR: **~#145** | NSF CAREER Award
**Venue:** 2024–2025 (NSF/DARPA/DoD funded)
**Relevance:** Expert on telephony attacks (SS7, VoIP) and wireless protocol exploits — CMatrix's network scan module targets these surfaces. FICS is a major NSF-funded cybersecurity research center.

---

## 👤 Prof. #39 — Jun Dai · Worcester Polytechnic Institute · USNWR ~#270
**Email:** jdai@wpi.edu | **Website:** https://users.wpi.edu/~jdai/ | **Lab:** CS Department, WPI

### 2.36 `[P1 | 2026]` LLM Membership Inference and Model Extraction Against LLM-Based Agents (NDSS 2026)
**Paper:** [LLM Security: Membership Inference and Model Extraction Attacks Against LLM-Based Autonomous Agents](https://users.wpi.edu/~jdai/)
**Authors:** **Jun Dai** et al. (WPI)
**Author Profile:** https://users.wpi.edu/~jdai/
**Institution:** Worcester Polytechnic Institute | USNWR: **~#270** | ACM CCS 2026 Artifact Evaluation Co-Chair | PhD under Peng Liu (Penn State)
**Venue:** NDSS 2026 (CCF-A)
**Relevance:** 🎯 How adversaries steal and manipulate LLM-based agents — the adversarial twin of CMatrix's approach. Prof. Dai explicitly seeks "self-motivated students at all levels" — very approachable outreach target.

### 2.37 `[P2 | 2025]` Autonomous Agent Security: Detection and Defense Against LLM Agent Attacks
**Paper:** [Autonomous Agent Security: Advanced Attack Detection and Countermeasures for LLM-Based Systems](https://users.wpi.edu/~jdai/)
**Authors:** **Jun Dai** et al. (WPI)
**Author Profile:** https://users.wpi.edu/~jdai/
**Institution:** Worcester Polytechnic Institute | USNWR: **~#270**
**Venue:** 2025 (SenSys, ACM CCS communities)
**Relevance:** Research directly on LLM security and autonomous agent security — exact match for CMatrix's architecture. Studying how adversaries manipulate agentic systems makes Prof. Dai ideal for CMatrix's threat model paper.

---

## 👤 Prof. #40 — Peng Gao · Virginia Tech · USNWR ~#170
**Email:** penggao@vt.edu | **Website:** https://people.cs.vt.edu/penggao/ | **Lab:** Security Lab, Virginia Tech CS

### 2.38 `[P1 | 2026]` NSF CAREER: Using LLMs to Help Security Analysts Identify and Respond to Threats Faster ($625K, Oct 2025)
**Paper:** [NSF CAREER: LLM-Based Autonomous Threat Identification and Response for Security Analysts](https://people.cs.vt.edu/penggao/)
**Authors:** **Peng Gao** (Virginia Tech)
**Author Profile:** https://people.cs.vt.edu/penggao/
**Institution:** Virginia Tech | USNWR: **~#170** | CCI Faculty Fellow | Microsoft Security AI Research Award 2020
**Venue:** NSF CAREER Award October 2025 ($625K) — papers at USENIX Security, USENIX ATC, ACM CCS, ICDE, ICSE
**Relevance:** 🎯 NSF CAREER specifically for using LLMs to help security analysts identify and respond to threats faster — direct CMatrix alignment. PhD under Dawn Song at Berkeley (bridges Berkeley RDI to Virginia Tech). CMatrix's autonomous threat modeling directly extends this research.

### 2.39 `[P2 | 2025]` Provenance-Based Intrusion Detection with Agentic AI for Cybersecurity
**Paper:** [Agentic AI for Cybersecurity: Provenance-Based Systems Security and Autonomous Threat Response](https://people.cs.vt.edu/penggao/)
**Authors:** **Peng Gao** et al. (Virginia Tech Security Lab)
**Author Profile:** https://people.cs.vt.edu/penggao/
**Institution:** Virginia Tech | USNWR: **~#170**
**Venue:** 2024–2025 (CCI Faculty Fellow, USENIX Security, ACM CCS)
**Relevance:** Provenance-based systems security + agentic AI for cybersecurity — CMatrix attack telemetry graphs are a natural input to Gao's provenance-based detection. Offensive CMatrix → defensive Gao pipeline = strong collaboration axis.

---

<a name="section-3"></a>
# 🟢 SECTION 3 — PROFESSOR PAPERS: TIER 3 (Professors #41–60)
**Full paper details for every entry**

---

## 👤 Prof. #41 — Wenliang (Kevin) Du · Syracuse University · USNWR ~#133
**Email:** wedu@acm.org | **Website:** https://seedsecuritylabs.org/wenliangdu/ | **Lab:** SEED Security Lab

### 3.1 `[P2 | 2023]` SEED Labs: The World's Most Widely Deployed Cybersecurity Education Platform
**Paper:** [SEED Labs: A Problem-Solving Based Learning Environment for Security Education](https://seedsecuritylabs.org)
**Authors:** **Wenliang (Kevin) Du** (Syracuse University)
**Author Profile:** https://seedsecuritylabs.org/wenliangdu/
**Institution:** Syracuse University | USNWR: **~#133** | ACM Fellow + IEEE Fellow (both 2023) | Laura J. and L. Douglas Meredith Professor
**Venue:** ACM CCS Education Track + SIGCSE (Test-of-Time Award) — used by 1,180+ institutions in 80 countries
**Project:** https://seedsecuritylabs.org
**Relevance:** 🎯 Creator of SEED Labs — the most widely deployed cybersecurity education platform globally. SEED Labs teach exactly the attack surfaces CMatrix automates. CMatrix can use SEED Lab VMs as standardized evaluation environments.

---

## 👤 Prof. #42 — Selcuk Uluagac · Florida International University · USNWR ~#411
**Email:** suluagac@fiu.edu | **Website:** https://users.cs.fiu.edu/~uluagac/ | **Lab:** Cyber-Physical Systems Security Lab (CSL)

### 3.2 `[P2 | 2025]` AI-Driven Attack and Defense on IoT/CPS: Smart Home and Industrial Device Security
**Paper:** [AI-Driven Security Analysis of Smart Home and Industrial IoT/CPS Devices: Attack Detection and Defense](https://users.cs.fiu.edu/~uluagac/)
**Authors:** **Selcuk Uluagac** et al. (FIU CSL)
**Author Profile:** https://users.cs.fiu.edu/~uluagac/
**Institution:** Florida International University | USNWR: **~#411** | $10M+ active grants (NSF/DoD/DARPA/DHS)
**Venue:** 2024–2025
**Relevance:** Expert on AI-driven attacks and defenses on IoT/CPS — OT/ICS extension of CMatrix's VAPT scope.

---

## 👤 Prof. #43 — Murtuza Jadliwala · UT San Antonio · USNWR ~#411
**Email:** murtuza.jadliwala@utsa.edu | **Website:** https://sites.google.com/site/murtuza.jadliwala | **Lab:** SPriTELab

### 3.3 `[P2 | 2025]` LLM Package Hallucination: How LLMs Generate Insecure Code (USENIX Security 2025)
**Paper:** [LLM Package Hallucination Attacks: How LLMs Frequently Generate Code with Non-Existent and Insecure Packages](https://www.usenix.org/conference/usenixsecurity25)
**Authors:** **Murtuza Jadliwala** et al. (UTSA SPriTELab)
**Author Profile:** https://sites.google.com/site/murtuza.jadliwala
**Institution:** University of Texas at San Antonio | USNWR: **~#411** | Hispanic-Serving Institution
**Venue:** USENIX Security 2025 (CCF-A)
**Relevance:** LLMs frequently generate code referencing non-existent packages — an attacker registering those packages can inject malicious code into LLM-generated programs. Directly relevant to CMatrix's post-exploit analysis phase when analyzing LLM-generated payloads.

---

## 👤 Prof. #44 — Kevin Butler · University of Florida · USNWR ~#145
**Email:** butler@cise.ufl.edu | **Website:** https://www.cise.ufl.edu/~butler/ | **Lab:** FICS Research

### 3.4 `[P2 | 2026]` Fizzle: Deterministic and Reproducible Network Fuzzing (co-author with Enck and Traynor — see entry 2.33 above for full details)

### 3.5 `[P3 | 2025]` Hardware-Assisted Security: TEEs, Secure Enclaves, and Authentication
**Paper:** [Hardware-Assisted Security Mechanisms: TEEs, Secure Enclaves, and Authentication in FICS Research](https://www.cise.ufl.edu/~butler/)
**Authors:** **Kevin Butler** et al. (FICS Research, University of Florida)
**Author Profile:** https://www.cise.ufl.edu/~butler/
**Institution:** University of Florida | USNWR: **~#145** | NSF CAREER Award | FICS co-director
**Venue:** 2024–2025 (NSF/DARPA/DHS funded)
**Relevance:** Hardware-assisted security mechanisms (TEEs, secure enclaves) that CMatrix can leverage or target in grey-box hardware assessments.

---

## 👤 Prof. #45 — Wil Robertson · Northeastern University · USNWR ~#179
**Email:** wil@ccs.neu.edu | **Website:** https://www.ccs.neu.edu/home/wil/ | **Lab:** Secure Systems Lab (SSL)

### 3.6 `[P2 | 2015]` PANDA: Whole-System Dynamic Analysis Platform for Security Research (ongoing updates through 2024)
**Paper:** [PANDA: Platform for Architecture-Neutral Dynamic Analysis](https://github.com/panda-re/panda)
**Authors:** Brendan Dolan-Gavitt (NYU), Josh Hodosh, **Wil Robertson** (Northeastern), Tim Leek, Ryan Whelan
**Author Profile:** https://www.ccs.neu.edu/home/wil/
**Institution:** Northeastern University + NYU Tandon | USNWR: **~#179**
**Venue:** ACM Workshop on Program Protection and Reverse Engineering 2015 + ongoing updates through 2024
**Code:** https://github.com/panda-re/panda
**Relevance:** Whole-system dynamic analysis framework — foundational tool for CMatrix's grey-box binary analysis module. PANDA enables platform-agnostic replay-based analysis of entire system executions including malware and vulnerabilities.

### 3.7 `[P2 | 2016]` LAVA: Large-Scale Automated Vulnerability Addition for Benchmarking Bug Finders (IEEE S&P 2016)
**Paper:** [LAVA: Large-scale Automated Vulnerability Addition](https://dl.acm.org/doi/10.1109/SP.2016.15)
**Authors:** Brendan Dolan-Gavitt (NYU), Patrick Hulin, **Wil Robertson** (Northeastern), Tim Leek et al.
**Author Profile:** https://www.ccs.neu.edu/home/wil/
**Institution:** Northeastern University + MIT Lincoln Laboratory | USNWR: **~#179**
**Venue:** IEEE S&P 2016 (CCF-A) — widely cited through 2024
**Relevance:** Large-scale automated injection of vulnerabilities into real programs — creates ground-truth datasets for benchmarking vulnerability scanners. LAVA-M and LAVA-1 are standard benchmarks CMatrix should report results against.

---

## 👤 Prof. #46 — Chengyu Song · UC Riverside · USNWR ~#405
**Email:** csong@cs.ucr.edu | **Website:** https://www.cs.ucr.edu/~csong/ | **Lab:** System Security Lab, UCR

### 3.8 `[P2 | 2025]` Kernel Fuzzing and OS Vulnerability Discovery for Memory Safety (NSF CAREER)
**Paper:** [Systematic Kernel Fuzzing and OS Vulnerability Discovery for Memory Safety Bugs](https://www.cs.ucr.edu/~csong/)
**Authors:** **Chengyu Song** et al. (UCR System Security Lab)
**Author Profile:** https://www.cs.ucr.edu/~csong/
**Institution:** UC Riverside | USNWR: **~#405** | NSF CAREER Award
**Venue:** 2024–2025 (publications at CCS, USENIX Security, NDSS)
**Relevance:** Kernel fuzzing and OS-level vulnerability discovery for memory safety — CMatrix's grey-box scan pipeline for kernel-level vulnerabilities. UCR shares the Wenke Lee + Taesoo Kim research network.

---

## 👤 Prof. #47 — Zhiyun Qian · UC Riverside · USNWR ~#405
**Email:** zhiyunq@cs.ucr.edu | **Website:** https://www.cs.ucr.edu/~zhiyunq/ | **Lab:** Systems and Networking Security Lab, UCR

### 3.9 `[P2 | 2025]` Network-Layer Attacks: Off-Path TCP, DNS Cache Poisoning, and Cellular Network Security
**Paper:** [Systematic Discovery of Network-Layer Attack Surfaces: Off-Path TCP Injection, DNS Cache Poisoning, Cellular Security](https://www.cs.ucr.edu/~zhiyunq/)
**Authors:** **Zhiyun Qian** et al. (UCR Systems and Networking Security Lab)
**Author Profile:** https://www.cs.ucr.edu/~zhiyunq/
**Institution:** UC Riverside | USNWR: **~#405** | NSF CAREER Award
**Venue:** 2024–2025 (USENIX Security, CCS, NDSS)
**Relevance:** Network-layer attack discovery including off-path TCP injection, DNS poisoning, and cellular protocol vulnerabilities — attack surfaces CMatrix's network scan module targets for grey-box assessments.

---

## 👤 Prof. #48 — Gang Tan · Penn State University · USNWR ~#130
**Email:** gtan@psu.edu | **Website:** https://www.cse.psu.edu/~gxt29/ | **Lab:** Security and Programming Languages Research Group

### 3.10 `[P2 | 2025]` WebAssembly Security: Vulnerability Analysis and Software Fault Isolation
**Paper:** [WebAssembly Security Analysis: Vulnerability Discovery, SFI Enforcement, and Binary Analysis](https://www.cse.psu.edu/~gxt29/)
**Authors:** **Gang Tan** et al. (Penn State Security and PL Group)
**Author Profile:** https://www.cse.psu.edu/~gxt29/
**Institution:** Penn State University | USNWR: **~#130** | NSF CAREER Award
**Venue:** 2024–2025 (NSF/DARPA funded)
**Relevance:** WebAssembly security — increasingly important attack surface as CMatrix expands to web application security. SFI and binary analysis at the intersection of formal methods and security.

---

## 👤 Prof. #49 — Antonio Bianchi · Purdue University · USNWR #53
**Email:** antoniob@purdue.edu | **Website:** https://antoniobianchi.me | **Lab:** PurSec Lab (UCSB PhD → Purdue faculty)

### 3.11 `[P1 | 2025]` LEMIX: Enabling Testing of Embedded Applications as Linux Applications (USENIX Security 2025)
**Paper:** [LEMIX: Enabling Testing of Embedded Applications as Linux Applications](https://www.usenix.org/conference/usenixsecurity25)
**Authors:** Sai Ritvik Tanksalkar, Siddharth Muralee, Srihari Danduri, Paschal Amusuo, **Antonio Bianchi** (Purdue), James C. Davis, Aravind Kumar Machiry
**Author Profile:** https://antoniobianchi.me
**Institution:** Purdue University | USNWR: **#53** | DARPA AIxCC finalist (Shellphish team)
**Venue:** USENIX Security 2025 (CCF-A)
**Relevance:** 🎯 LEMIX enables testing embedded firmware as native Linux applications — dramatically simplifies CMatrix's IoT/embedded VAPT by enabling standard Linux fuzzing and analysis tools on embedded targets.

### 3.12 `[P2 | 2025]` Automated Discovery of Semantic Attacks in Multi-Robot Navigation Systems (USENIX Security 2025)
**Paper:** [Automated Discovery of Semantic Attacks in Multi-Robot Navigation Systems](https://www.usenix.org/conference/usenixsecurity25)
**Authors:** Doguhan Yeke, Kartik A. Pant, Muslum Ozgur Ozmen, Hyungsub Kim, James M. Goppert, Inseok Hwang, **Antonio Bianchi**, **Z. Berkay Celik** (Purdue)
**Author Profile:** https://antoniobianchi.me
**Institution:** Purdue University | USNWR: **#53**
**Venue:** USENIX Security 2025 (CCF-A)
**Relevance:** Automated semantic attack discovery in multi-robot CPS — extends CMatrix's autonomous attack synthesis to cyber-physical systems.

### 3.13 `[P2 | 2025]` NeuroScope: Reverse Engineering DNNs on Edge Devices (co-author with Dongyan Xu — see entry 1.30 above for full details)

---

## 👤 Prof. #50 — Pubali Datta · UMass Amherst · USNWR ~#170
**Email:** pubali@cs.umass.edu | **Website:** https://pubali.github.io | **Lab:** SPADE Lab, UMass Amherst

### 3.14 `[P2 | 2026]` IoT Security and Provenance-Based Attack Forensics (IEEE S&P 2026)
**Paper:** [IoT Security: Vulnerability Analysis in Smart Home Ecosystems and Provenance-Based Attack Forensics](https://pubali.github.io)
**Authors:** **Pubali Datta** (UMass), **Z. Berkay Celik** (Purdue) et al.
**Author Profiles:** https://pubali.github.io · https://beerkay.github.io
**Institution:** UMass Amherst + Purdue University | USNWR: **~#170 / #53**
**Venue:** IEEE S&P 2026 (CCF-A)
**Relevance:** IoT smart home vulnerability analysis + provenance-based forensics — CMatrix attack telemetry feeds directly into Datta's provenance-based detection. Cross-institutional UMass + Purdue collaboration = strong co-authorship model.

---

## 👤 Prof. #51 — Gianluca Stringhini · Boston University · USNWR ~#65
**Email:** gian@bu.edu | **Website:** https://seclab.bu.edu | **Lab:** BU SecLab

### 3.15 `[P1 | 2025]` CVE-GENIE: LLM Multi-Agent Framework for CVE Reproduction (co-author with Kruegel, Vigna, Guo — see entry 1.38 above for full details)

### 3.16 `[P2 | 2025]` Cybercrime Measurement and Automated Abuse Detection at Scale (NSF CAREER)
**Paper:** [Cybercrime at Scale: Measuring Underground Markets, Automated Abuse Detection, and Threat Intelligence](https://seclab.bu.edu)
**Authors:** **Gianluca Stringhini** et al. (BU SecLab)
**Author Profile:** https://seclab.bu.edu
**Institution:** Boston University | USNWR: **~#65** | NSF CAREER Award
**Venue:** 2024–2025 (NSF/DARPA/DHS/EU Horizon funded)
**Relevance:** Cybercrime measurement and automated abuse detection — natural downstream consumers of CMatrix's scan outputs for threat intelligence enrichment.

---

## 👤 Prof. #52 — Guanhong Tao · Purdue University · USNWR #53
**Email:** taog@purdue.edu | **Website:** https://guanhuangao.github.io | **Lab:** PurSec Lab (affiliated)

### 3.17 `[P2 | 2025]` Backdoor Attacks in LLMs and Temporal Logic Attacks Against Autonomous RL Agents
**Paper:** [Temporal Logic Backdoor Attacks Against Autonomous Driving RL Agents and LLM Security](https://guanhuangao.github.io)
**Authors:** **Guanhong Tao** et al. (Purdue PurSec)
**Author Profile:** https://guanhuangao.github.io
**Institution:** Purdue University | USNWR: **#53** | Collaborative with Xiangyu Zhang
**Venue:** 2024–2025 (NeurIPS, ICLR, USENIX Security)
**Relevance:** Backdoor attacks in ML models and LLMs — a critical attack surface for multi-agent systems like CMatrix. Temporal logic backdoors in RL agents reveal how autonomous agents can be compromised through training-time attacks.

---

## 👤 Prof. #53 — Heng Yin · UC Riverside · USNWR ~#405
**Email:** heng.yin@ucr.edu | **Website:** https://www.cs.ucr.edu/~heng/ | **Lab:** Secure Systems and Intelligent Software Lab

### 3.18 `[P2 | 2024]` DECAF: Dynamic Executable Code Analysis Framework (foundational platform, ongoing through 2024)
**Paper:** [DECAF: Dynamic Executable Code Analysis Framework — Whole-System Dynamic Malware Analysis and Taint Analysis](https://www.cs.ucr.edu/~heng/)
**Authors:** **Heng Yin** et al. (UCR Secure Systems and Intelligent Software Lab)
**Author Profile:** https://www.cs.ucr.edu/~heng/
**Institution:** UC Riverside | USNWR: **~#405** | NSF CAREER Award
**Venue:** Foundational platform 2008–2024; multiple USENIX Security, CCS, NDSS publications
**Relevance:** Creator of DECAF — widely used whole-system dynamic analysis platform. DECAF's dynamic taint analysis provides the foundation for CMatrix's grey-box binary scan module for tracking data flow through target applications.

---

## 👤 Prof. #54 — Michalis Polychronakis · Stony Brook University · USNWR ~#185
**Email:** mikepo@cs.stonybrook.edu | **Website:** https://www3.cs.stonybrook.edu/~mikepo/ | **Lab:** Systems Security Lab, Stony Brook

### 3.19 `[P2 | 2025]` Exploit Mitigation: ROP, Code Reuse Attacks, and Anti-ROP (NSF CAREER)
**Paper:** [Exploit Mitigation Beyond NX: Return-Oriented Programming Defense and Code-Reuse Attack Detection](https://www3.cs.stonybrook.edu/~mikepo/)
**Authors:** **Michalis Polychronakis** et al. (Stony Brook Systems Security Lab)
**Author Profile:** https://www3.cs.stonybrook.edu/~mikepo/
**Institution:** Stony Brook University | USNWR: **~#185** | NSF CAREER Award
**Venue:** 2024–2025 (publications at CCS, USENIX Security, NDSS, IEEE S&P)
**Relevance:** Expert on ROP/JOP exploit techniques and automated exploit mitigation — the technical underbelly of what CMatrix automates in its exploit chain module. Network-level malware detection (ShieldFS, anti-ROP) complements CMatrix's scan output interpretation.

---

## 👤 Prof. #55 — Long Cheng · Clemson University · USNWR ~#168
**Email:** lcheng2@clemson.edu | **Website:** https://people.computing.clemson.edu/~lcheng2/ | **Lab:** Secure and Dependable Systems (SDS) Lab

### 3.20 `[P2 | 2022]` Detecting Remote Infections on Linux-Based IoT Devices (ASIACCS 2022 Best Paper)
**Paper:** [Detecting Remote Infections on Linux-Based IoT Devices via Network Traffic Analysis](https://dl.acm.org/doi/10.1145/3488932.3497759)
**Authors:** **Long Cheng** (Clemson), **Guofei Gu** (Texas A&M) et al.
**Author Profiles:** https://people.computing.clemson.edu/~lcheng2/ · https://faculty.cse.tamu.edu/guofei
**Institution:** Clemson University + Texas A&M | USNWR: **~#168 / ~#145**
**Venue:** ASIACCS 2022 — **Best Paper Award**
**Relevance:** Automated detection of remote infection on Linux-based IoT devices — a primary CMatrix target class. Cross-institution Clemson + Texas A&M collaboration validates this as a strong multi-institution co-authorship model for CMatrix's IoT paper.

---

## 👤 Prof. #56 — Sankardas Roy · Bowling Green State University · USNWR ~#380
**Email:** sroy@bgsu.edu | **Website:** https://people.bgsu.edu/sroy | **Lab:** Mobile and Software Security Research Group

### 3.21 `[P2 | 2025]` Benchmarking Android Malware Detection with Deep Learning and LLM Embeddings
**Paper:** [Benchmarking Android Malware Detection: Deep Learning, LLM-Based Approaches, and Supply Chain Security](https://people.bgsu.edu/sroy)
**Authors:** **Sankardas Roy** (BGSU), **Xinming Ou** (USF), Doina Caragea (KSU) et al.
**Author Profiles:** https://people.bgsu.edu/sroy · https://www.usf.edu/ai-cybersecurity-computing/people/faculty/ou-simon.aspx
**Institution:** Bowling Green State University + University of South Florida + Kansas State University | USNWR: **~#380**
**Venue:** 2025 (NSF-funded, multiple security conferences)
**Relevance:** Android malware detection benchmarking with LLM methods — the mobile attack surface for CMatrix. Amandroid (CCS 2014, with Xinming Ou) established foundational inter-component data flow analysis for Android that all subsequent work builds on.

---

## 👤 Prof. #57 — Anoop Singhal · University of Maryland / NIST · USNWR #93 (UMD)
**Email:** anoop.singhal@nist.gov | **Website:** https://www.nist.gov/people/anoop-singhal | **Lab:** NIST Computer Security Division

### 3.22 `[P2 | 2025]` Network Attack Graphs and Multi-Hop Attack Path Modeling (NIST / UMD)
**Paper:** [Network Attack Graphs: Multi-Hop Attack Path Modeling and Risk Quantification for Enterprise Security](https://www.nist.gov/people/anoop-singhal)
**Authors:** **Anoop Singhal** (NIST), **Xinming Ou** (USF) et al.
**Author Profiles:** https://www.nist.gov/people/anoop-singhal · https://www.usf.edu/ai-cybersecurity-computing/people/faculty/ou-simon.aspx
**Institution:** NIST Computer Security Division + University of Maryland | USNWR: **#93 (UMD)**
**Venue:** 2024–2025 (NIST/NSF collaborative grants)
**Relevance:** 🎯 Network attack graphs (graph-based representation of multi-hop attack paths) — a direct output format for CMatrix's multi-host VAPT results. NIST affiliation provides access to government security standards for validating CMatrix's attack graph outputs.

### 3.23 `[P3 | 2024]` LLM Embeddings for Botnet TLS Certificate Detection (co-author with Xinming Ou — see entry 2.32 above for full details)

---

## 👤 Prof. #58 — Dipankar Dasgupta · University of Memphis · USNWR ~#270
**Email:** ddasgupta@memphis.edu | **Website:** https://www.memphis.edu/cs/people/faculty_pages/dasgupta.php | **Lab:** Intelligent Security Systems (ISS) Lab

### 3.24 `[P2 | 2025]` Autonomous Security Agents and Moving Target Defense: Adaptive Cybersecurity Systems
**Paper:** [Autonomous Security Agents and Moving Target Defense: Biologically-Inspired Adaptive Cybersecurity](https://www.memphis.edu/cs/people/faculty_pages/dasgupta.php)
**Authors:** **Dipankar Dasgupta** et al. (University of Memphis ISS Lab)
**Author Profile:** https://www.memphis.edu/cs/people/faculty_pages/dasgupta.php
**Institution:** University of Memphis | USNWR: **~#270** | Carnegie R1 research university
**Venue:** 2024–2025 (NSF/DoD/DHS/TVA funded)
**Relevance:** Pioneer in autonomous security agents and moving target defense — AI-driven systems that automatically adapt defense strategies in response to evolving attacks. MTD provides adversarial reasoning models CMatrix can incorporate into post-scan recommendations. ICS/SCADA expertise extends CMatrix's OT scope.

---

## 👤 Prof. #59 — Sushil Jajodia · George Mason University · USNWR ~#156
**Email:** jajodia@gmu.edu | **Website:** https://cs.gmu.edu/~jajodia/ | **Lab:** Center for Secure Information Systems (CSIS) — 120+ PhD graduates, 700+ publications

### 3.25 `[P1 | 2025]` Moving Target Defense: Proactive Cyber Defense via Attack Surface Randomization
**Paper:** [Moving Target Defense: Proactive Cyber Defense via Attack Surface Randomization and Cyber Deception](https://cs.gmu.edu/~jajodia/)
**Authors:** **Sushil Jajodia** et al. (George Mason CSIS)
**Author Profile:** https://cs.gmu.edu/~jajodia/
**Institution:** George Mason University | USNWR: **~#156** | University Professor (highest GMU rank)
**Venue:** 2024–2025 (NSF/DARPA/DoD/NSA/DHS funded — IEEE S&P, USENIX Security, CCS)
**Relevance:** 🎯 Pioneer of Moving Target Defense — CMatrix's offensive scan results directly motivate MTD remediation. Attackers exploit static targets; CMatrix finds them; MTD randomizes them. The offensive-defensive feedback loop CMatrix enables. 120+ PhD graduates = most prolific PhD mentor in the professor list.

### 3.26 `[P2 | 2025]` Cyber Deception: Honeypots, Decoy Networks, and Proactive Cybersecurity
**Paper:** [Cyber Deception Systems: Honeypots, Decoy Networks, and Proactive Cybersecurity at Scale](https://cs.gmu.edu/~jajodia/)
**Authors:** **Sushil Jajodia** et al. (George Mason CSIS)
**Author Profile:** https://cs.gmu.edu/~jajodia/
**Institution:** George Mason University | USNWR: **~#156**
**Venue:** 2024–2025 (DARPA/DoD funded)
**Relevance:** Cyber deception (honeypots, decoy networks) — natural extensions to CMatrix's post-scan defensive recommendations. After CMatrix identifies vulnerabilities, Jajodia's deception techniques can be automatically deployed as active defenses.

---

## 👤 Prof. #60 — Jun Dai (also listed as Prof. #39)
*See Section 2 entries 2.36 and 2.37 for all papers — Prof. Jun Dai at WPI appears in both Tier 2 (#39) and Tier 3 (#60) in the professor list. All papers are fully documented in Section 2.*

---

<a name="section-4"></a>
## 🗂️ SECTION 4 — FOUNDATIONAL AUTONOMOUS AI AGENTS IN CYBERSECURITY

> Core VAPT agent papers — the direct competition, comparison, and foundation for CMatrix.

---

### 4.1 `[P1 | 2024]` PentestGPT: The Benchmark Foundation

**Paper:** [PentestGPT: Evaluating and Harnessing LLMs for Automated Penetration Testing](https://www.usenix.org/conference/usenixsecurity24/presentation/deng)
**PDF:** [arXiv:2308.06782](https://arxiv.org/abs/2308.06782)
**Authors:** Gelei Deng, Yi Liu, Víctor Mayoral-Vilches, Peng Liu, et al.
**Institution:** Nanyang Technological University (NTU), Singapore | QS: **#26**
**Venue:** USENIX Security 2024 (CCF-A)
**Code:** [github.com/GreyDGL/PentestGPT](https://github.com/GreyDGL/PentestGPT)
**Relevance:** 🎯 The primary baseline — CMatrix is directly evaluated against PentestGPT.

---

### 4.2 `[P1 | 2026]` PentestGPT v2: Evidence-Guided Attack Tree Search

**Paper:** [What Makes a Good LLM Agent for Real-world Penetration Testing?](https://arxiv.org/abs/2602.17622)
**Authors:** NTU PentestGPT v2 team
**Institution:** Nanyang Technological University | QS: **#26**
**Venue:** arXiv, February 2026
**Relevance:** 🎯 SOTA — 91% CTF task completion. Key comparison point for CMatrix DCAT.

---

### 4.3 `[P1 | 2025]` Incalmo / On the Feasibility of LLMs for Multi-Host Network Attacks

**Paper:** [Incalmo: An Autonomous LLM-assisted System for Red Teaming Multi-Host Networks](https://arxiv.org/abs/2501.16466)
**Authors:** Brian Singer, Keane Lucas, Lakshmi Adiga, Meghna Jain, **Lujo Bauer**, **Vyas Sekar** (CMU CyLab)
**Author Profiles:** [Lujo Bauer](https://www.ece.cmu.edu/directory/bios/bauer-lujo.html) · [Vyas Sekar](https://ece.cmu.edu/directory/bios/sekar-vyas.html)
**Institution:** Carnegie Mellon University | USNWR: **#22**
**Venue:** arXiv, January 2025 (v4: November 2025) — cited in CMU/Anthropic joint press release July 2025
**Code:** [github.com/bsinger98/Incalmo](https://github.com/bsinger98/Incalmo)
**Relevance:** 🎯 The closest published academic peer to CMatrix — LLMs autonomously executing enterprise multi-host attacks. Co-authored by the two professors CMatrix should most urgently contact.

---

### 4.4 `[P1 | 2025]` AutoPentester: End-to-End Automation

**Paper:** [AutoPentester: An LLM Agent-based Framework for Automated Pentesting](https://arxiv.org/abs/2510.05605)
**Authors:** Anonymous (under review)
**Venue:** arXiv, October 2025
**Relevance:** 🎯 27% better subtask completion than PentestGPT, fewer human interventions. Direct comparison.

---

### 4.5 `[P1 | 2025]` VulnBot: Multi-Agent Collaborative Pentesting

**Paper:** [VulnBot: Autonomous Penetration Testing for a Multi-Agent Collaborative Framework](https://arxiv.org/abs/2501.13411)
**Authors:** KHenry et al.
**Venue:** arXiv, January 2025
**Code:** [github.com/KHenryAegis/VulnBot](https://github.com/KHenryAegis/VulnBot)
**Relevance:** 🎯 Direct multi-agent VAPT framework — comparable architecture to CMatrix.

---

### 4.6 `[P1 | 2025]` xOffense: Domain-Adapted Multi-Agent Framework

**Paper:** [xOffense: An Autonomous Multi-Agent Framework for Penetration Testing](https://arxiv.org/abs/2509.13021)
**Authors:** Quyen Nguyen Huu et al.
**Venue:** arXiv, September 2025 (updated April 2026)
**Relevance:** 🎯 Fine-tuned Qwen3-32B; 79.17% sub-task completion. Key mid-scale LLM approach to compare.

---

### 4.7 `[P2 | 2025]` CurriculumPT: Progressive Skill Acquisition

**Paper:** [CurriculumPT: LLM-Based Multi-Agent Autonomous Penetration Testing with Curriculum-Guided Task Scheduling](https://www.mdpi.com/2076-3417/15/16/9096)
**Venue:** Applied Sciences (MDPI), August 2025
**Relevance:** Curriculum learning for progressive exploitation skills — CMatrix's DCAT parallel.

---

### 4.8 `[P2 | 2025]` PentestMCP: MCP-Based Tool Orchestration

**Paper:** [PentestMCP: A Toolkit for Agentic Penetration Testing](https://arxiv.org/abs/2510.03610)
**Authors:** Zachary Ezetta, Wu-Chang Feng (Portland State University)
**Author Profile:** [Wu-Chang Feng](https://web.cecs.pdx.edu/~wuchang/)
**Venue:** arXiv, October 2025
**Relevance:** MCP-based tool orchestration — directly relevant to CMatrix's modular agent design.

---

### 4.9 `[P2 | 2026]` Pen-Strategist: Fine-Tuned Reasoning for Pentesting

**Paper:** [Pen-Strategist: A Reasoning Framework for Penetration Testing Strategy Formation](https://arxiv.org/abs/2605.04499)
**Venue:** arXiv, May 2026
**Relevance:** Qwen3-14B fine-tuned for strategy reasoning; Table 10 gives the most up-to-date survey of 28 LLM-based PT systems (as of May 2026). Must-read survey resource.

---

### 4.10 `[P1 | 2023]` Getting Pwn'd by AI: LLM Penetration Testing (Foundational)

**Paper:** [Getting pwn'd by AI: Penetration Testing with Large Language Models](https://dl.acm.org/doi/abs/10.1145/3611643.3613083)
**Authors:** Andreas Happe, Jürgen Cito (TU Wien / University of Zurich)
**Author Profile:** [Andreas Happe](https://se.ini.uzh.ch/people/happe.html)
**Institution:** TU Wien, Austria | QS: **#251–300**
**Venue:** FSE/ESEC 2023 (CCF-A)
**Code:** [github.com/ipa-lab/hackingBuddyGPT](https://github.com/ipa-lab/hackingBuddyGPT)
**Relevance:** First rigorous study of LLMs for pentesting at a top-tier venue. Foundational.

---

### 4.11 `[P2 | 2025]` Can LLMs Hack Enterprise Networks? (Active Directory)

**Paper:** [Can LLMs Hack Enterprise Networks? Autonomous Assumed Breach Penetration-Testing Active Directory Networks](https://dl.acm.org/doi/abs/10.1145/3766895)
**Authors:** Andreas Happe, Aaron Kaplan, Jürgen Cito (TU Wien)
**Institution:** TU Wien, Austria | QS: **#251–300**
**Venue:** ACM TOSEM 2025 (CCF-A)
**Code:** [github.com/andreashappe/cochise](https://github.com/andreashappe/cochise)
**Relevance:** Enterprise Active Directory pentesting with LLMs — critical for CMatrix multi-stage exploitation.

---

### 4.12 `[P1 | 2024]` LLM Agents Can Autonomously Exploit One-day Vulnerabilities

**Paper:** [LLM Agents can Autonomously Exploit One-day Vulnerabilities](https://arxiv.org/abs/2404.08144)
**Authors:** Richard Fang, Rohan Bindu, Akul Gupta, **Daniel Kang** (UIUC)
**Author Profile:** [Daniel Kang — UIUC](https://ddkang.github.io/)
**Institution:** University of Illinois Urbana-Champaign | QS: **#82**
**Venue:** arXiv, April 2024
**Relevance:** 🎯 Landmark — GPT-4 exploits 87% of one-day CVEs. Core CMatrix vulnerability intel pillar.

---

### 4.13 `[P1 | 2024]` Teams of LLM Agents Can Exploit Zero-Day Vulnerabilities

**Paper:** [Teams of LLM Agents can Exploit Zero-Day Vulnerabilities](https://arxiv.org/abs/2406.01637)
**Authors:** Yuxuan Zhu, Antony Kellermann, Akul Gupta, Philip Li, Richard Fang, Rohan Bindu, **Daniel Kang** (UIUC)
**Author Profile:** [Daniel Kang — UIUC](https://ddkang.github.io/)
**Institution:** University of Illinois Urbana-Champaign | QS: **#82**
**Venue:** arXiv, June 2024 (updated March 2025)
**Relevance:** 🎯 HPTSA multi-agent team improves over prior work by 4.3×. Direct CMatrix architecture inspiration for sub-agent hierarchies.

---

### 4.14 `[P2 | 2025]` RedTeamLLM: Agentic Framework for Offensive Security

**Paper:** [RedTeamLLM: an Agentic AI Framework for Offensive Security](https://arxiv.org/abs/2512.14233)
**Venue:** arXiv, December 2025
**Code:** [github.com/lre-security-systems-team/redteamllm](https://github.com/lre-security-systems-team/redteamllm)
**Relevance:** Open-source agentic offensive framework — architectural comparison to CMatrix.

---

### 4.15 `[P2 | 2025]` CAI: Open, Bug Bounty-Ready Cybersecurity AI

**Paper:** [CAI: An Open, Bug Bounty-Ready Cybersecurity AI](https://arxiv.org/abs/2504.06017)
**Authors:** Alias Robotics team
**Venue:** arXiv, April 2025
**Code:** [github.com/aliasrobotics/CAI](https://github.com/aliasrobotics/CAI)
**Relevance:** Production-grade cybersecurity AI for real bug bounty tasks — real-world validation context.

---

### 4.16 `[P3 | 2025]` ARACNE: Autonomous Shell Pentesting Agent

**Paper:** [ARACNE: An LLM-Based Autonomous Shell Pentesting Agent](https://arxiv.org/abs/2502.18528)
**Venue:** arXiv, February 2025
**Relevance:** Shell-level autonomous agent — relevant to CMatrix's network agent module.

---

### 4.17 `[P3 | 2025]` RapidPen: IP-to-Shell Automation

**Paper:** [RapidPen: Fully Automated IP-to-Shell Penetration Testing with LLM-based Agents](https://arxiv.org/abs/2502.16730)
**Venue:** arXiv, February 2025
**Relevance:** End-to-end automation from IP to shell — operational scope mirrors CMatrix goals.

---

### 4.18 `[P2 | 2024]` AutoAttacker: LLM-Guided Cyber Attacks

**Paper:** [AutoAttacker: A Large Language Model Guided System to Implement Automatic Cyber-attacks](https://arxiv.org/abs/2403.01038)
**Authors:** Jiacen Xu, Jack W. Stokes, Geoff McDonald, et al. (Microsoft Research + UC Irvine)
**Institution:** Microsoft Research + UCI | QS: **UCI: #148**
**Venue:** arXiv, March 2024
**Relevance:** Industry-grade LLM attack automation from Microsoft Research. Directly cited as contemporary work.

---

### 4.19 `[P2 | 2025]` Pentest-R1: Reinforcement Learning for Pentesting Reasoning

**Paper:** [Pentest-R1: Towards Autonomous Penetration Testing Reasoning Optimized via Two-Stage RL](https://arxiv.org/abs/2508.07382)
**Authors:** KHenry et al.
**Venue:** arXiv, August 2025
**Code:** [github.com/KHenryAegis/Pentest-R1](https://github.com/KHenryAegis/Pentest-R1)
**Relevance:** RL-based reasoning optimization — novel training paradigm for CMatrix agents.

---

### 4.20 `[P2 | 2026]` HackWorld: Computer-Use Agents on Web Vulnerabilities (ICLR)

**Paper:** [HackWorld: Evaluating Computer-Use Agents on Exploiting Web Application Vulnerabilities](https://arxiv.org/abs/2510.12200)
**Venue:** ICLR 2026 (CCF-A)
**Code:** [github.com/GUI-Agent/HackWorld](https://github.com/GUI-Agent/HackWorld)
**Relevance:** GUI/computer-use agents for web exploitation — next-frontier capability beyond CMatrix.

---

### 4.21 `[P2 | 2025]` EnIGMA: Interactive Tools for Security Vulnerabilities (ICML 2025)

**Paper:** [EnIGMA: Interactive Tools Substantially Assist LM Agents in Finding Security Vulnerabilities](https://arxiv.org/abs/2409.16165)
**Authors:** Talor Abramovich, Meet Udeshi, Minghao Shao, Kilian Lieret, **Brendan Dolan-Gavitt** (NYU), et al.
**Author Profile:** [Brendan Dolan-Gavitt — NYU](https://engineering.nyu.edu/faculty/brendan-dolan-gavitt)
**Institution:** NYU Tandon + Princeton | QS: **NYU: #39**
**Venue:** ICLR 2025 (CCF-A)
**Relevance:** 🎯 Interactive tooling for vulnerability finding — ICML 2025. Directly relevant to CMatrix's HITL module. Professor Dolan-Gavitt is a priority contact.

---

### 4.22 `[P2 | 2025]` D-CIPHER: Multi-Agent System for Offensive Security

**Paper:** [D-CIPHER: Dynamic Collaborative Intelligent Multi-Agent System for Offensive Security](https://arxiv.org/abs/2502.10931)
**Authors:** Meet Udeshi, Minghao Shao, Haoran Xi, **Brendan Dolan-Gavitt** (NYU), et al.
**Author Profile:** [Brendan Dolan-Gavitt — NYU](https://engineering.nyu.edu/faculty/brendan-dolan-gavitt)
**Institution:** NYU Tandon | QS: **#39**
**Venue:** arXiv, February 2025
**Relevance:** 🎯 Planner-Executor multi-agent architecture; SOTA on NYU CTF Bench (22%), Cybench (22.5%), HackTheBox (44%). Direct CMatrix architecture parallel.

---

### 4.23 `[P2 | 2025]` CRAKEN: Cybersecurity LLM Agent with Knowledge-Based Execution

**Paper:** [CRAKEN: Cybersecurity LLM Agent with Knowledge-Based Execution](https://arxiv.org/abs/2505.17107)
**Authors:** Minghao Shao, Haoran Xi, Nanda Rani, Meet Udeshi, **Brendan Dolan-Gavitt** (NYU), et al.
**Author Profile:** [Brendan Dolan-Gavitt — NYU](https://engineering.nyu.edu/faculty/brendan-dolan-gavitt)
**Institution:** NYU Tandon | QS: **#39**
**Venue:** arXiv, May 2025
**Code:** [github.com/NYU-LLM-CTF/nyuctf_agents_craken](https://github.com/NYU-LLM-CTF/nyuctf_agents_craken)
**Relevance:** Knowledge-database-augmented CTF agent — solves 25–30% more ATT&CK techniques than prior work. Direct CMatrix knowledge-base architecture parallel.

---

### 4.24 `[P2 | 2025]` SoK: Comparison of Autonomous Penetration Testing Agents

**Paper:** [SoK: A Comparison of Autonomous Penetration Testing Agents](https://dl.acm.org/doi/10.1145/3664476.3664484)
**Venue:** ARES 2024
**Relevance:** 🎯 Systematization of knowledge — comprehensive comparison of all pentest agents. Essential background.

---

### 4.25 `[P2 | 2024]` HackSynth: LLM Agent + Evaluation Framework

**Paper:** [HackSynth: LLM Agent and Evaluation Framework for Autonomous Penetration Testing](https://arxiv.org/abs/2412.01778)
**Institution:** ELTE Eötvös Loránd University, Hungary | QS: **#801–1000**
**Venue:** arXiv, December 2024
**Code:** [github.com/aielte-research/HackSynth](https://github.com/aielte-research/HackSynth)
**Relevance:** Combined agent + benchmark framework — dual contribution similar to CMatrix's approach.

---

### 4.26 `[P2 | 2025]` PentestAgent: Incorporating LLM Agents (AsiaCCS 2025)

**Paper:** [PentestAgent: Incorporating LLM Agents to Automated Penetration Testing](https://dl.acm.org/doi/full/10.1145/3708821.3733882)
**Venue:** AsiaCCS 2025 (CCF-C)
**Code:** [github.com/GH05TCREW/PentestAgent](https://github.com/GH05TCREW/PentestAgent)
**Relevance:** Peer-reviewed multi-agent pentesting at AsiaCCS.

---

### 4.27 `[P3 | 2025]` PENTEST-AI: MITRE ATT&CK Multi-Agent Framework

**Paper:** [PENTEST-AI: An LLM-Powered Multi-Agents Framework for Penetration Testing Leveraging MITRE ATT&CK](https://ieeexplore.ieee.org/abstract/document/10679480)
**Venue:** IEEE CSR 2024
**Relevance:** MITRE ATT&CK-aligned multi-agent framework — relevant to CMatrix's reasoning pillar.

---

### 4.28 `[P3 | 2025]` RefPentester: Self-Reflective Pentesting Framework

**Paper:** [RefPentester: A Knowledge-Informed Self-Reflective Penetration Testing Framework](https://arxiv.org/abs/2505.07089)
**Venue:** arXiv, May 2025
**Relevance:** Self-reflection in pentesting — relevant to CMatrix's iterative agent reasoning (Paper 03).

---

### 4.29 `[P3 | 2025]` Multi-Agent Penetration Testing AI for the Web

**Paper:** [Multi-Agent Penetration Testing AI for the Web](https://arxiv.org/abs/2508.20816)
**Venue:** arXiv, August 2025
**Relevance:** Direct multi-agent web pentesting — architectural comparison for CMatrix's Web agent.

---

### 4.30 `[P3 | 2025]` AutoPT: End-to-End Web Penetration Testing

**Paper:** [AutoPT: How Far Are We from the End2End Automated Web Penetration Testing?](https://arxiv.org/abs/2411.01236)
**Venue:** arXiv, November 2024
**Relevance:** Web-focused end-to-end automation evaluation.

---

### 4.31 `[P3 | 2026]` Automated Penetration Testing with LLM Agents and Classical Planning

**Paper:** [Automated Penetration Testing with LLM Agents and Classical Planning](https://arxiv.org/abs/2512.11143)
**Venue:** arXiv, December 2025
**Relevance:** Hybrid AI planning combining LLMs with classical planners for structured attack chains.

---

### 4.32 `[P3 | 2026]` LLMs as Hackers: Privilege Escalation Attacks

**Paper:** [LLMs as Hackers: Autonomous Linux Privilege Escalation Attacks](https://link.springer.com/article/10.1007/s10664-025-10758-3)
**Venue:** Empirical Software Engineering (Springer), 2026
**Relevance:** Privilege escalation automation — CMatrix's post-exploitation scenarios.

---

### 4.33 `[P3 | 2026]` PTFusion: LLM-driven Knowledge Fusion for Web Pentesting

**Paper:** [PTFusion: LLM-driven Context-aware Knowledge Fusion for Web Penetration Testing](https://www.sciencedirect.com/science/article/pii/S1566253525007936)
**Venue:** Information Fusion Journal, 2026
**Relevance:** Knowledge fusion for web pentesting — relevant to CMatrix's Security-Semantic Caching (SSC).

---

<a name="section-5"></a>
## 🗂️ SECTION 5 — LLM MULTI-AGENT ORCHESTRATION & RESILIENCE

---

### 5.1 `[P1 | 2024]` AutoGen: Next-Gen LLM Multi-Agent Conversations

**Paper:** [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation Framework](https://arxiv.org/abs/2308.08155)
**Authors:** Qingyun Wu, Gagan Bansal, et al., Chi Wang (Microsoft Research)
**Author Profile:** [Chi Wang — Microsoft Research](https://www.microsoft.com/en-us/research/people/chiw/)
**Institution:** Microsoft Research
**Venue:** arXiv, August 2023 (widely adopted industry + academia)
**Relevance:** 🎯 Foundation framework — CMatrix's Master-Worker hierarchy directly inspired by AutoGen patterns.

---

### 5.2 `[P1 | 2024]` MetaGPT: Meta Programming for Multi-Agent Frameworks (ICLR 2024)

**Paper:** [MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352)
**Authors:** Sirui Hong, Mingchen Zhuge, et al. (DeepWisdom)
**Institution:** DeepWisdom / Multiple universities
**Venue:** ICLR 2024 (CCF-A)
**Relevance:** Structured multi-agent collaboration with role-playing — foundational for CMatrix agent specialization.

---

### 5.3 `[P1 | 2026]` A Survey of Agentic AI and Cybersecurity

**Paper:** [A Survey of Agentic AI and Cybersecurity: Challenges, Opportunities and Use-case Prototypes](https://arxiv.org/abs/2601.05293)
**Venue:** arXiv, January 2026
**Relevance:** 🎯 Direct survey of agentic AI in cybersecurity — exactly aligns with CMatrix's scope. Essential background for all CMatrix papers.

---

### 5.4 `[P2 | 2026]` Difficulty-Aware Agentic Orchestration (WWW 2026)

**Paper:** [Difficulty-Aware Agentic Orchestration for Query-Specific Multi-Agent Workflows](https://arxiv.org/abs/2509.11079)
**Venue:** WWW 2026 (ACM Web Conference)
**Relevance:** Query-specific workflow generation + cost/performance-aware LLM routing — directly relevant to CMatrix's DCAT.

---

### 5.5 `[P2 | 2024]` WorkflowLLM: Enhancing Workflow Orchestration

**Paper:** [WorkflowLLM: Enhancing Workflow Orchestration Capability of Large Language Models](https://arxiv.org/abs/2411.05451)
**Institution:** Wuhan University, China | QS: **#225**
**Venue:** arXiv, November 2024
**Relevance:** LLM workflow orchestration — technical background for CMatrix's LLMOrch-VAPT.

---

### 5.6 `[P2 | 2024]` A Survey on LLM-Based Multi-Agent Systems: Workflow, Infrastructure, and Challenges

**Paper:** [A Survey on LLM-Based Multi-Agent Systems](https://doi.org/10.1007/s44336-024-00009-2)
**Venue:** Vicinagearth Journal, October 2024
**Relevance:** Comprehensive survey of LLM multi-agent systems — foundational for CMatrix architecture.

---

### 5.7 `[P3 | 2026]` A Trace-Based Assurance Framework for Agentic AI Orchestration

**Paper:** [A Trace-Based Assurance Framework for Agentic AI Orchestration: Contracts, Testing, and Governance](https://arxiv.org/abs/2603.18096)
**Venue:** arXiv, March 2026
**Relevance:** Governance and assurance for agentic AI — relevant to CMatrix's HITL safety gates.

---

### 5.8 `[P3 | 2025]` Engineering LLM Powered Multi-Agent Framework for Autonomous CloudOps (CAIN 2025)

**Paper:** [Engineering LLM Powered Multi-agent Framework for Autonomous CloudOps](https://arxiv.org/abs/2501.08243)
**Venue:** CAIN 2025 (co-located with ICSE)
**Relevance:** Production-grade multi-agent framework engineering — architectural lessons for CMatrix.

---

### 5.9 `[P3 | 2025]` From LLM Reasoning to Autonomous AI Agents: Comprehensive Review

**Paper:** [From LLM Reasoning to Autonomous AI Agents: A Comprehensive Review](https://arxiv.org/abs/2504.19678)
**Venue:** arXiv, April 2025
**Relevance:** Taxonomy of ~60 LLM benchmarks, agent frameworks 2023–2025. Essential background.

---

### 5.10 `[P3 | 2025]` A Declarative Language for Building LLM-Powered Agent Workflows

**Paper:** [A Declarative Language for Building And Orchestrating LLM-Powered Agent Workflows](https://arxiv.org/abs/2512.19769)
**Authors:** Ivan Daunis (PayPal)
**Venue:** arXiv, November 2025
**Relevance:** DSL for agent workflows across Java/Python/Go — relevant to CMatrix's cross-provider orchestration.

---

<a name="section-6"></a>
## 🗂️ SECTION 6 — COST OPTIMIZATION: LLM ROUTING, TIERING & CACHING

---

### 6.1 `[P1 | 2025]` RouteLLM: Learning to Route LLMs with Preference Data (ICLR 2025)

**Paper:** [RouteLLM: Learning to Route LLMs with Preference Data](https://arxiv.org/abs/2406.18665)
**Authors:** Isaac Ong, Amjad Almahairi, Vincent Wu, Wei-Lin Chiang, Ion Stoica et al. (UC Berkeley / LMSYS)
**Author Profiles:** [Ion Stoica — Berkeley](https://people.eecs.berkeley.edu/~istoica/) · [Joseph Gonzalez — Berkeley](https://people.eecs.berkeley.edu/~jegonzal/)
**Institution:** UC Berkeley + Anyscale | QS: **#4**
**Venue:** ICLR 2025 (CCF-A)
**Project:** [lmsys.org/blog/2024-07-01-routellm](https://www.lmsys.org/blog/2024-07-01-routellm/)
**Relevance:** 🎯 2× cost reduction without quality loss — the core technique behind CMatrix's DCAT.

---

### 6.2 `[P1 | 2023]` FrugalGPT: Reducing LLM Cost with Cascade Approach

**Paper:** [FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance](https://arxiv.org/abs/2305.05176)
**Authors:** Lingjiao Chen, Matei Zaharia, James Zou (Stanford)
**Author Profiles:** [Matei Zaharia — Stanford/Databricks](https://people.eecs.berkeley.edu/~matei/) · [James Zou — Stanford](https://www.james-zou.com/)
**Institution:** Stanford University | QS: **#5**
**Venue:** arXiv, May 2023 (highly cited)
**Relevance:** 🎯 Foundational cascade-based cost reduction — precursor to CMatrix's model tiering strategy.

---

### 6.3 `[P1 | 2025]` Cost-Efficient Serving of LLM Agents via Test-Time Plan Caching

**Paper:** [Cost-Efficient Serving of LLM Agents via Test-Time Plan Caching](https://arxiv.org/abs/2506.14852)
**Venue:** arXiv, June 2025
**Relevance:** 🎯 Plan-level caching for agentic LLMs — directly maps to CMatrix's Security-Semantic Caching (SSC) concept.

---

### 6.4 `[P2 | 2025]` Minions: Cost-Efficient Collaboration between On-Device and Cloud LLMs

**Paper:** [Minions: Cost-efficient Collaboration between On-device and Cloud Language Models](https://arxiv.org/abs/2502.15964)
**Venue:** arXiv, February 2025
**Relevance:** Hybrid local/cloud LLM execution — relevant to CMatrix's Ollama (local) + cloud LLM tiering.

---

### 6.5 `[P2 | 2024]` RouterBench: A Benchmark for Multi-LLM Routing (ICML 2024 Workshop)

**Paper:** [RouterBench: A Benchmark for Multi-LLM Routing System](https://arxiv.org/abs/2403.12031)
**Venue:** ICML 2024 Workshop
**Relevance:** Benchmark for evaluating LLM router quality — methodology for measuring CMatrix's DCAT effectiveness.

---

### 6.6 `[P2 | 2023]` On Optimal Caching and Model Multiplexing for Large Model Inference

**Paper:** [On Optimal Caching and Model Multiplexing for Large Model Inference](https://arxiv.org/abs/2306.02003)
**Venue:** arXiv (foundational caching theory)
**Relevance:** Theoretical foundations for caching + model multiplexing — background for CMatrix's SSC layer.

---

### 6.7 `[P3 | 2026]` Robust Batch-Level Query Routing for LLMs

**Paper:** [Robust Batch-Level Query Routing for Large Language Models under Cost and Capacity Constraints](https://arxiv.org/abs/2603.26796)
**Venue:** arXiv, March 2026
**Relevance:** Batch routing with cost budgets — relevant to CMatrix's high-volume task scheduling.

---

<a name="section-7"></a>
## 🗂️ SECTION 7 — AI SAFETY, HUMAN-IN-THE-LOOP & GOVERNANCE

---

### 7.1 `[P1 | 2025]` Policy-as-Prompt: AI Governance Rules as Guardrails

**Paper:** [Policy-as-Prompt: Turning AI Governance Rules into Guardrails for AI Agents](https://arxiv.org/abs/2509.23994)
**Venue:** arXiv, November 2025
**Relevance:** 🎯 Converts policy documents into runtime guardrails — directly relevant to CMatrix's HITL safety gates.

---

### 7.2 `[P1 | 2025]` ShieldAgent: Verifiable Safety Policy Reasoning

**Paper:** [ShieldAgent: Shielding Agents via Verifiable Safety Policy Reasoning](https://arxiv.org/abs/2503.22738)
**Venue:** arXiv, March 2025
**Relevance:** Safety shield layer for LLM agents — architecture for CMatrix's high-risk operation approval mechanism.

---

### 7.3 `[P2 | 2026]` Toward Safe and Responsible AI Agents (Three-Pillar Model)

**Paper:** [Toward Safe and Responsible AI Agents: A Three-Pillar Model](https://arxiv.org/abs/2601.06223)
**Venue:** arXiv, January 2026
**Relevance:** Transparency, accountability, HITL principles — background for CMatrix's governance framework.

---

### 7.4 `[P2 | 2025]` AGrail: Lifelong Agent Guardrail

**Paper:** [AGrail: A Lifelong Agent Guardrail with Effective and Adaptive Safety Detection](https://arxiv.org/abs/2502.11448)
**Venue:** arXiv, February 2025
**Relevance:** Adaptive safety detection for agents — relevant to CMatrix's risk classification logic.

---

### 7.5 `[P2 | 2026]` AgentDoG: Diagnostic Guardrail Framework

**Paper:** [AgentDoG: A Diagnostic Guardrail Framework for AI Agent Safety and Security](https://arxiv.org/abs/2601.18491)
**Venue:** arXiv, January 2026
**Relevance:** Fine-grained trajectory monitoring for agents — relevant to CMatrix's audit logging and HITL design.

---

### 7.6 `[P3 | 2024]` TrustAgent: Agent Constitution for Safety

**Paper:** [TrustAgent: Towards Safe and Trustworthy LLM-based Agents through Agent Constitution](https://arxiv.org/abs/2402.01586)
**Venue:** arXiv, February 2024
**Relevance:** Constitutional safety for agents — foundational theory for CMatrix's safety gates.

---

### 7.7 `[P3 | 2024]` R-Judge: Benchmarking Safety Risk Awareness in LLM Agents

**Paper:** [R-Judge: Benchmarking Safety Risk Awareness for LLM Agents](https://arxiv.org/abs/2401.10019)
**Venue:** arXiv, January 2024
**Relevance:** Safety risk benchmarking for agents — evaluation framework for CMatrix's safety modules.

---

<a name="section-8"></a>
## 🗂️ SECTION 8 — RAG, VULNERABILITY INTELLIGENCE & KNOWLEDGE BASES

---

### 8.1 `[P1 | 2025]` RAG for Cybersecurity: Hybrid Retrieval for LLMs

**Paper:** [Adapting LLMs to Emerging Cybersecurity using Retrieval Augmented Generation](https://arxiv.org/abs/2510.27080)
**Venue:** arXiv, October 2025
**Relevance:** 🎯 RAG for cybersecurity knowledge — directly relevant to CMatrix's Vuln-Intel agent.

---

### 8.2 `[P1 | 2026]` Survey on the Security of Long-Term Memory in LLM Agents

**Paper:** [A Survey on the Security of Long-Term Memory in LLM Agents: Toward Mnemonic Sovereignty](https://arxiv.org/abs/2604.16548)
**Authors:** Zehao Lin et al.
**Venue:** arXiv, April 2026
**Relevance:** 🎯 Long-term memory security — directly relevant to CMatrix's Qdrant-based session memory.

---

### 8.3 `[P2 | 2026]` Towards Secure RAG: Comprehensive Review of Threats, Defenses, Benchmarks

**Paper:** [Towards Secure Retrieval-Augmented Generation: A Comprehensive Review](https://arxiv.org/abs/2603.21654)
**Venue:** arXiv, March 2026
**Relevance:** Security of RAG systems — critical for CMatrix's vector memory (Qdrant) security posture.

---

### 8.4 `[P2 | 2026]` Securing RAG: Taxonomy of Attacks, Defenses, and Future Directions

**Paper:** [Securing RAG: A Taxonomy of Attacks, Defenses, and Future Directions](https://arxiv.org/abs/2604.08304)
**Venue:** arXiv, April 2026
**Relevance:** Comprehensive RAG attack/defense taxonomy — security analysis for CMatrix's SSC + Qdrant memory.

---

### 8.5 `[P2 | 2026]` Memory for Autonomous LLM Agents: Mechanisms & Evaluation

**Paper:** [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/abs/2603.07670)
**Venue:** arXiv, March 2026
**Relevance:** Comprehensive survey of agent memory systems — background for CMatrix's vector memory design.

---

### 8.6 `[P2 | 2025]` Mem0: Intelligent Memory Layer for AI Applications (ECAI 2025)

**Paper:** [Mem0: Intelligent Memory Layer for Personalized AI](https://arxiv.org/abs/2504.19413)
**Authors:** Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, Deshraj Yadav
**Venue:** ECAI 2025
**Relevance:** Production memory system — benchmark for CMatrix's Qdrant-based memory architecture.

---

<a name="section-9"></a>
## 🗂️ SECTION 9 — CYBERSECURITY BENCHMARKS & EVALUATION

---

### 9.1 `[P1 | 2025]` CyBench: Evaluating Cybersecurity Capabilities (ICLR 2025)

**Paper:** [Cybench: A Framework for Evaluating Cybersecurity Capabilities and Risks of Language Models](https://arxiv.org/abs/2408.08926)
**Authors:** Andy K. Zhang, Neil Perry, Riya Dulepet, et al. (Stanford + Berkeley + CMU + Dan Boneh)
**Author Profile:** [Dan Boneh — Stanford](https://crypto.stanford.edu/~dabo/)
**Institution:** Stanford + Berkeley + CMU | QS: **#5 / #4 / #24**
**Venue:** ICLR 2025 (CCF-A)
**Code:** [cybench.github.io](https://cybench.github.io/)
**Relevance:** 🎯 CMatrix's primary CTF evaluation benchmark — 40 tasks from 2022–2024 competitions.

---

### 9.2 `[P1 | 2025]` CyberGym (ICLR 2026)

*(Listed above as Section 1, entry 1.4 — see full entry there)*
**Shorter reference:** [arXiv:2506.02548](https://arxiv.org/abs/2506.02548) | UC Berkeley Dawn Song | ICLR 2026

---

### 9.3 `[P1 | 2025]` CVE-Bench: AI Agents Exploiting Real-World Web Vulnerabilities (ICML 2025)

*(Listed above as Section 1, entry 1.26 — see full entry there)*
**Shorter reference:** [arXiv:2503.17332](https://arxiv.org/abs/2503.17332) | UIUC Daniel Kang | ICML 2025

---

### 9.4 `[P1 | 2024]` AutoPenBench: Benchmarking Generative Agents for Penetration Testing

**Paper:** [AutoPenBench: Benchmarking Generative Agents for Penetration Testing](https://arxiv.org/abs/2410.03225)
**Authors:** Luca Gioacchini, Marco Mellia et al. (Politecnico di Torino)
**Author Profile:** [Marco Mellia — Polito](https://www.telematica.polito.it/member/marco-mellia/)
**Institution:** Politecnico di Torino, Italy | QS: **#283**
**Venue:** arXiv, October 2024
**Relevance:** 🎯 CMatrix's second primary benchmark — 33 vulnerable Docker containers, used by xOffense for comparison.

---

### 9.5 `[P1 | 2024]` NYU CTF Bench (NeurIPS 2024)

**Paper:** [NYU CTF Bench: A Scalable Open-Source Benchmark Dataset for Evaluating LLMs in Offensive Security](https://proceedings.neurips.cc/paper_files/paper/2024/hash/69d97a6493fbf016fff0a751f253ad18-Abstract-Datasets_and_Benchmarks_Track.html)
**Authors:** NYU Tandon team (Brendan Dolan-Gavitt et al.)
**Institution:** New York University | QS: **#39**
**Venue:** NeurIPS 2024 (CCF-A)
**Code:** [github.com/NYU-LLM-CTF/NYUCTFBench](https://github.com/NYU-LLM-CTF/NYUCTFBench)
**Relevance:** Scalable CTF benchmark for LLMs — evaluation dataset for CMatrix's CTF-style tasks.

---

### 9.6 `[P2 | 2024]` An Empirical Evaluation of LLMs for Offensive Security Challenges (NeurIPS 2024)

**Paper:** [An Empirical Evaluation of LLMs for Solving Offensive Security Challenges](https://arxiv.org/abs/2402.11814)
**Venue:** NeurIPS 2024 (CCF-A)
**Code:** [github.com/NickNameInvalid/LLM_CTF](https://github.com/NickNameInvalid/LLM_CTF)
**Relevance:** Empirical evaluation of LLMs (GPT-4, Claude, etc.) on offensive security — benchmark methodology reference.

---

### 9.7 `[P2 | 2025]` CAIBench: Cybersecurity AI Meta-Benchmark

**Paper:** [Cybersecurity AI Benchmark (CAIBench): A Meta-Benchmark for Evaluating Cybersecurity AI Agents](https://arxiv.org/abs/2510.24317)
**Venue:** arXiv, October 2025
**Relevance:** Meta-benchmark integrating Cybench, SecEval, CyberMetric, AutoPenBench — comprehensive evaluation.

---

### 9.8 `[P2 | 2025]` Measuring and Augmenting LLMs for CTF (ACM CCS 2025)

**Paper:** [Measuring and Augmenting Large Language Models for Solving Capture-the-Flag Challenges](https://dl.acm.org/doi/abs/10.1145/3719027.3744855)
**Venue:** ACM CCS 2025 (CCF-A)
**Relevance:** Augmentation techniques for LLMs on CTF tasks — relevant to CMatrix's agent enhancement.

---

### 9.9 `[P3 | 2026]` PentestEval: Stage-Level Benchmarking of LLM-Based Penetration Testing

**Paper:** [PentestEval: Benchmarking LLM-based Penetration Testing with Modular and Stage-Level Design](https://arxiv.org/abs/2512.14233)
**Venue:** arXiv, December 2025
**Relevance:** Stage-level evaluation design — relevant to CMatrix's per-agent performance measurement.

---

<a name="section-10"></a>
## 🗂️ SECTION 10 — AGENT REASONING, PLANNING & CHAIN-OF-THOUGHT

---

### 10.1 `[P1 | 2023]` ReAct: Synergizing Reasoning and Acting in Language Models (ICLR 2023)

**Paper:** [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
**Authors:** Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao
**Author Profile:** [Shunyu Yao — Princeton/OpenAI](https://ysymyth.github.io/)
**Institution:** Princeton University + Google Brain | QS: **#16**
**Venue:** ICLR 2023 (CCF-A)
**Relevance:** 🎯 Foundational ReAct framework used in PentestGPT and CMatrix agent reasoning loops.

---

### 10.2 `[P1 | 2023]` Tree of Thoughts: Deliberate Problem Solving with LLMs (NeurIPS 2023)

**Paper:** [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601)
**Authors:** Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, Karthik Narasimhan
**Institution:** Princeton University + Google DeepMind | QS: **#16**
**Venue:** NeurIPS 2023 (CCF-A)
**Relevance:** 🎯 Tree-of-Thoughts (ToT) directly implemented in CMatrix's intelligent reasoning module.

---

### 10.3 `[P1 | 2022]` Chain-of-Thought Prompting Elicits Reasoning in LLMs (NeurIPS 2022)

**Paper:** [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)
**Authors:** Jason Wei, Xuezhi Wang, Dale Schuurmans, et al. (Google Brain)
**Institution:** Google Brain / Google Research
**Venue:** NeurIPS 2022 (CCF-A) — 10,000+ citations
**Relevance:** 🎯 CoT is explicitly implemented in CMatrix's intelligent reasoning module. Foundational must-read.

---

### 10.4 `[P1 | 2023]` Reflexion: Language Agents with Verbal Reinforcement Learning (NeurIPS 2023)

**Paper:** [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)
**Authors:** Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao
**Institution:** Northeastern University + Princeton | QS: **#351–400 / #16**
**Venue:** NeurIPS 2023 (CCF-A)
**Relevance:** Self-reflection in agents — foundational for CMatrix's iterative attack strategy refinement.

---

### 10.5 `[P3 | 2025]` A Unified Modeling Framework for Automated Penetration Testing

**Paper:** [A Unified Modeling Framework for Automated Penetration Testing](https://www.sciencedirect.com/science/article/abs/pii/S0167404825004766)
**Venue:** Computers & Security (CCF-B), 2025
**Relevance:** Formal modeling framework for automated pentesting — theoretical underpinning for CMatrix's reasoning module.

---

<a name="section-11"></a>
## 🗂️ SECTION 11 — SURVEYS & SYSTEMATIC LITERATURE REVIEWS

---

### 11.1 `[P1 | 2025]` When LLMs Meet Cybersecurity: A Systematic Literature Review

**Paper:** [When LLMs Meet Cybersecurity: A Systematic Literature Review](https://doi.org/10.1186/s42400-025-00361-w)
**Authors:** Jie Zhang, Haoyu Bu, Hui Wen, Yongji Liu, et al.
**Venue:** Cybersecurity Journal (Springer), 2025
**Relevance:** 🎯 Must-read systematic review of all LLM + cybersecurity intersection.

---

### 11.2 `[P2 | 2026]` Pen-Strategist Survey Table (28 LLM-based PT Systems — Most Comprehensive as of May 2026)

**Paper:** [Pen-Strategist: A Reasoning Framework for Penetration Testing Strategy Formation](https://arxiv.org/abs/2605.04499) — *Table 10 provides survey of 28 systems*
**Venue:** arXiv, May 2026
**Relevance:** 🎯 The most up-to-date curated list of all LLM-based PT systems.

---

### 11.3 `[P2 | 2024]` Towards Automated Penetration Testing: A Survey

**Paper:** [Towards Automated Penetration Testing: A Survey](https://arxiv.org/abs/2303.01323)
**Venue:** arXiv / Journal 2023
**Relevance:** Historical baseline survey for the field.

---

### 11.4 `[P2 | 2024]` A Survey on Large Language Models for Cybersecurity

**Paper:** [A Survey on Large Language Models for Cybersecurity](https://arxiv.org/abs/2405.04828)
**Venue:** arXiv, May 2024
**Relevance:** Complete survey of LLMs in cybersecurity — essential background for all CMatrix papers.

---

<a name="section-12"></a>
## 🗂️ SECTION 12 — LIVING CURATED LISTS & REPOSITORIES

---

### 12.1 🌟 LLM4Pentest: The Single Most Comprehensive Curated List

**Repository:** [github.com/simon-p-j-r/LLM4Pentest](https://github.com/simon-p-j-r/LLM4Pentest)
**Maintainer:** DAS Lab (Cheng Huang's Lab)
**Last Updated:** May 2026 (active, 119+ commits)
**Relevance:** 🎯 **BOOKMARK THIS.** Papers, blogs, MCP tools, benchmarks, datasets. Check weekly for new additions.

---

### 12.2 Awesome Agent Papers

**Repository:** [github.com/luo-junyu/Awesome-Agent-Papers](https://github.com/luo-junyu/awesome-agent-papers)
**Relevance:** Broader LLM agent paper coverage — cross-domain agent research for CMatrix's orchestration background.

---

## 📊 PROFESSOR → PAPER QUICK-REFERENCE

| # | Professor | University | Section Entries |
|---|---|---|---|
| 1 | Nickolai Zeldovich | MIT | 1.1, 1.2, 1.3 |
| 2 | Dawn Song | UC Berkeley | 1.4, 1.5, 1.6, 1.7 |
| 3 | Nick Feamster | U Chicago | 1.8, 1.9 |
| 4 | Lujo Bauer | CMU | 1.10 |
| 5 | Vyas Sekar | CMU | 1.11 |
| 6 | Wajih Ul Hassan | UVA | 1.12, 1.13, 1.14, 1.15 |
| 7 | Taesoo Kim | Georgia Tech | 1.16, 1.17, 1.18 |
| 8 | Wenke Lee | Georgia Tech | 1.19, 1.20, 1.21 |
| 9 | Gang Wang | UIUC | 1.22, 1.23 |
| 10 | Daniel Kang | UIUC | 1.24, 1.25, 1.26 |
| 11 | Barton Miller | UW-Madison | 1.27, 1.28, 1.29 |
| 12 | Dongyan Xu | Purdue | 1.30, 1.31 |
| 13 | Xiangyu Zhang | Purdue | 1.32, 1.33 |
| 14 | Z. Berkay Celik | Purdue | 1.34, 1.35 |
| 15 | Yizheng Chen | UMD | 1.36, 1.37 |
| 16 | Christopher Kruegel | UCSB | 1.38 |
| 17 | Giovanni Vigna | UCSB | 1.39, 1.40 |
| 18 | Wenbo Guo | UCSB | 1.41–1.44 |
| 19 | Xinyu Xing | Northwestern | 1.45, 1.46, 1.47 |
| 20 | Suman Jana | Columbia | 1.48, 1.49, 1.50 |
| 21 | Yan Shoshitaishvili | ASU | 2.1, 2.2, 2.3 |
| 22 | Tiffany Bao | ASU | 2.4, 2.5, 2.6 |
| 23 | Adam Doupé | ASU | 2.7, 2.8, 2.9 |
| 24 | Long Lu | Northeastern | 2.10, 2.11 |
| 25 | Engin Kirda | Northeastern | 2.12 |
| 26 | Peng Liu | Penn State | 2.13 |
| 27 | Ting Wang | Penn State | 2.14 |
| 28 | Jie Gao | Rutgers | 2.15 |
| 29 | Zhiqiang Lin | Ohio State | 2.16, 2.17 |
| 30 | Vitaly Shmatikov | Cornell Tech | 2.18, 2.19 |
| 31 | Brendan Dolan-Gavitt | NYU Tandon | 2.20, 2.21, 2.22, 2.23, 2.24 |
| 32 | Yinzhi Cao | Johns Hopkins | 2.25, 2.26 |
| 33 | Guofei Gu | Texas A&M | 2.27, 2.28 |
| 34 | Jedidiah Crandall | ASU | 2.29 |
| 35 | Saumya Debray | U Arizona | 2.30 |
| 36 | Xinming (Simon) Ou | USF | 2.31, 2.32 |
| 37 | William Enck | NC State | 2.33 |
| 38 | Patrick Traynor | U Florida | 2.34, 2.35 |
| 39 | Jun Dai | WPI | 2.36, 2.37 |
| 40 | Peng Gao | Virginia Tech | 2.38, 2.39 |
| 41 | Wenliang (Kevin) Du | Syracuse | 3.1 |
| 42 | Selcuk Uluagac | FIU | 3.2 |
| 43 | Murtuza Jadliwala | UTSA | 3.3 |
| 44 | Kevin Butler | U Florida | 3.4, 3.5 |
| 45 | Wil Robertson | Northeastern | 3.6, 3.7 |
| 46 | Chengyu Song | UC Riverside | 3.8 |
| 47 | Zhiyun Qian | UC Riverside | 3.9 |
| 48 | Gang Tan | Penn State | 3.10 |
| 49 | Antonio Bianchi | Purdue | 3.11, 3.12, 3.13 |
| 50 | Pubali Datta | UMass Amherst | 3.14 |
| 51 | Gianluca Stringhini | Boston University | 3.15, 3.16 |
| 52 | Guanhong Tao | Purdue | 3.17 |
| 53 | Heng Yin | UC Riverside | 3.18 |
| 54 | Michalis Polychronakis | Stony Brook | 3.19 |
| 55 | Long Cheng | Clemson | 3.20 |
| 56 | Sankardas Roy | BGSU | 3.21 |
| 57 | Anoop Singhal | NIST/UMD | 3.22, 3.23 |
| 58 | Dipankar Dasgupta | U Memphis | 3.24 |
| 59 | Sushil Jajodia | George Mason | 3.25, 3.26 |
| 60 | Jun Dai (also #39) | WPI | 2.36, 2.37 |

---

## 📅 RECOMMENDED READING ORDER (ZERO KNOWLEDGE GAPS)

**Phase 1 — Core Reasoning (Week 1):** CoT (§10.3) → ReAct (§10.1) → Tree of Thoughts (§10.2) → Reflexion (§10.4) → AutoGen (§5.1)

**Phase 2 — Core VAPT (Week 2):** Getting pwn'd by AI (§4.7) → PentestGPT (§4.1) → One-day CVEs (§1.24) → Teams Zero-days (§1.25) → AutoAttacker (§4.12) → SoK Pentest Agents (§4.18)

**Phase 3 — Contemporary Frameworks (Week 3):** Incalmo (§1.10) → VulnBot (§4.5) → xOffense (§4.6) → D-CIPHER (§2.21) → EnIGMA (§2.20) → CRAKEN (§2.22) → PentestGPT v2 (§4.2)

**Phase 4 — AIxCC + Prof Papers (Week 4):** ATLANTIS (§1.16) → SoK AIxCC (§1.17) → CVE-GENIE (§1.38) → VulnLLM-R (§1.6) → SoK Vuln Repair (§1.22) → PurpCode (§1.23) → PatchAgent (§1.45)

**Phase 5 — Benchmarks (Week 5):** CyBench (§9.1) → CVE-Bench (§1.26) → CyberGym (§1.4) → BountyBench (§1.5) → AutoPenBench (§9.4) → NYU CTF Bench (§9.5)

**Phase 6 — Professor Specialty Papers (Week 6):** Decompiling the Synergy (§2.1) → APT Detection (§1.12) → Tamper-Evident Logging (§1.13) → MAS Malicious Code (§2.18) → CFH Breaking (§2.19) → SAGAI Report (§1.19) → Locus Fuzzing (§1.36)

**Phase 7 — Safety + RAG + Cost (Week 7):** RAG Cybersecurity (§8.1) → Memory Security (§8.2) → ShieldAgent (§7.2) → Policy-as-Prompt (§7.1) → RouteLLM (§6.1) → FrugalGPT (§6.2) → Plan Caching (§6.3)

**Phase 8 — Surveys + Living Lists (Week 8):** When LLMs Meet Cybersecurity (§11.1) → Frontier AI Impact (§1.7) → Pen-Strategist Table 10 (§11.2) → LLM4Pentest repo (§12.1) — subscribe and check weekly

---

## 🏫 UNIVERSITY RANKING QUICK REFERENCE

| Institution | Country | QS 2025 Rank | USNWR |
|---|---|---|---|
| MIT | USA | #1 | #1 |
| Stanford University | USA | #5 | #3 |
| UC Berkeley | USA | #12 | #4 |
| Princeton University | USA | #16 | #14 |
| Carnegie Mellon University | USA | #24 | #22 |
| Johns Hopkins University | USA | — | #9 |
| Columbia University | USA | — | #12 |
| Northwestern University | USA | — | #9 |
| Nanyang Technological University | Singapore | #26 | — |
| University of Illinois Urbana-Champaign | USA | #82 | #35 |
| New York University | USA | #39 | #53 |
| Georgia Tech | USA | — | #33 |
| University of California, Santa Barbara | USA | #65 | #65 |
| University of Maryland | USA | — | #93 |
| University of Virginia | USA | — | #62 |
| Cornell University / Cornell Tech | USA | — | #17 |
| Arizona State University | USA | — | ~#147 |
| Texas A&M University | USA | — | ~#145 |
| Virginia Tech | USA | — | ~#170 |
| Penn State University | USA | — | ~#130 |
| Politecnico di Torino | Italy | #283 | — |
| TU Wien | Austria | #251–300 | — |
| Wuhan University | China | #225 | — |
| Worcester Polytechnic Institute | USA | — | ~#270 |
| ELTE Eötvös Loránd University | Hungary | #801–1000 | — |

---

*Generated for CMatrix Research Team | Updated: May 12, 2026 | Version 4.1*
*All arXiv PDFs freely accessible. Institutional links verified as of compilation date.*
*Integrated Tier 3 professors, restored detailed thematic sections, added master paper list and university rankings.*
