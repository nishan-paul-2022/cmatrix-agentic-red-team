# **What Makes a Good LLM Agent for Real-world Penetration Testing?**

## Table of Contents

- [Abstract](#abstract)
- [1 Introduction](#1-introduction)
- [2 Background](#2-background)
- [2.1 Penetration Testing](#2-1-penetration-testing)
- [2.2 Benchmarking Penetration Testing](#2-2-benchmarking-penetration-testing)
- [2.3 LLM-Based Agents](#2-3-llm-based-agents)
- [3 Understanding LLM Agent Failures](#3-understanding-llm-agent-failures)
- [3.1 Taxonomy and Evaluation of LLM-based Penetration Testing](#3-1-taxonomy-and-evaluation-of-llm-based-penetration-testing)
  - [3.1.1 Taxonomy](#3-1-1-taxonomy)
  - [3.1.2 Evaluation Setup](#3-1-2-evaluation-setup)
- [3.2 Findings](#3-2-findings)
  - [3.2.1 Agent Architecture Convergence](#3-2-1-agent-architecture-convergence)
  - [3.2.2 Two Distinct Failure Categories](#3-2-2-two-distinct-failure-categories)
- [3.3 Analysis and Design Implications](#3-3-analysis-and-design-implications)
  - [3.3.1 Root Cause: Missing Difficulty Assessment](#3-3-1-root-cause-missing-difficulty-assessment)
  - [3.3.2 Design Implications](#3-3-2-design-implications)
- [4 Design of PENTESTGPT V2](#4-design-of-pentestgpt-v2)
- [4.1 Overview](#4-1-overview)
- [4.2 Tool and Skill Layer](#4-2-tool-and-skill-layer)
- [4.3 Task Difficulty Assessment (TDA)](#4-3-task-difficulty-assessment-tda)
  - [4.3.1 TDA Dimensions](#4-3-1-tda-dimensions)
- [4.4 Evidence-Guided Attack Tree Search (EGATS)](#4-4-evidence-guided-attack-tree-search-egats)
  - [4.3.2 Task Difficulty Index](#4-3-2-task-difficulty-index)
  - [4.4.1 Attack Tree Structure](#4-4-1-attack-tree-structure)
  - [4.4.2 The EGATS Algorithm](#4-4-2-the-egats-algorithm)
- [4.5 Memory Subsystem](#4-5-memory-subsystem)
- [5 Evaluation](#5-evaluation)
- [5.1 Experimental Setup](#5-1-experimental-setup)
- [5.2 RQ1: Overall Performance](#5-2-rq1-overall-performance)
- [5.3 RQ2: Ablation Study](#5-3-rq2-ablation-study)
- [5.4 RQ3: Strategy Analysis](#5-4-rq3-strategy-analysis)
  - [5.4.1 Search Behavior](#5-4-1-search-behavior)
  - [5.4.2 Case Study: HTB Falafel](#5-4-2-case-study-htb-falafel)
  - [5.4.3 Failure Case: PlayerTwo](#5-4-3-failure-case-playertwo)
- [5.5 RQ4: Real-World Deployment](#5-5-rq4-real-world-deployment)
  - [5.5.1 Cost Analysis](#5-5-1-cost-analysis)
  - [5.5.2 Live Competition Deployment](#5-5-2-live-competition-deployment)
- [6 Discussion](#6-discussion)
- [6.1 Limitations and Threats to Validity](#6-1-limitations-and-threats-to-validity)
- [6.2 What Remains Hard](#6-2-what-remains-hard)
- [7 Conclusion](#7-conclusion)
- [References](#references)
- [A Surveyed LLM-Based Penetration Testing Systems](#a-surveyed-llm-based-penetration-testing-systems)
- [B Tool and Skill Layer: Supported Tools](#b-tool-and-skill-layer-supported-tools)
- [C Evidence Confidence Scoring](#c-evidence-confidence-scoring)
- [D Parameter Derivation and Validation](#d-parameter-derivation-and-validation)
- [D.1 Validation Dataset](#d-1-validation-dataset)
- [D.2 TDI Weight Selection](#d-2-tdi-weight-selection)
- [D.3 Mode Selection Thresholds](#d-3-mode-selection-thresholds)
- [D.4 Pruning Parameters](#d-4-pruning-parameters)
- [D.5 UCB Difficulty Penalty](#d-5-ucb-difficulty-penalty)
- [D.6 Context Load Degradation Study](#d-6-context-load-degradation-study)

---

Gelei Deng<sup>1</sup> , Yi Liu<sup>1</sup> , Yuekang Li<sup>2</sup> , Ruozhao Yang<sup>3</sup> , Xiaofei Xie<sup>3</sup> , Jie Zhang<sup>4</sup> , Han Qiu<sup>5</sup> , Tianwei Zhang<sup>1</sup>

> 1 _Nanyang Technological University,_ 2 _University of New South Wales,_ 3 _Singapore Management University,_

> 4 _CFAR, A*STAR, Singapore,_ 5 _Tsinghua University_

## **Abstract**

> **Section Summary:** LLM-based agents show promise for automating penetration testing, yet the reported performance varies widely across systems and benchmarks.


LLM-based agents show promise for automating penetration testing, yet the reported performance varies widely across systems and benchmarks. We analyze 28 LLM-based penetration testing systems and evaluate five representative implementations across three benchmarks of increasing complexity. Our analysis reveals two distinct failure modes: _Type A failures_ stem from capability gaps (missing tools, inadequate prompts) that engineering readily addresses, while _Type B failures_ persist regardless of tooling due to planning and state management limitations. We show that Type B failures share a root cause that is largely invariant to the underlying LLM: agents lack real-time task difficulty estimation. As a result, agents misallocate effort, over-commit to low-value branches, and exhaust context before completing attack chains.

Based on this insight, we present PENTESTGPT V2, a penetration testing agent that couples strong tooling with difficultyaware planning. A Tool and Skill Layer eliminates Type A failures through typed interfaces and retrieval-augmented knowledge. A Task Difficulty Assessment (TDA) mechanism addresses Type B failures by estimating tractability through four measurable dimensions (horizon estimation, evidence confidence, context load, and historical success) and uses these estimates to guide exploration-exploitation decisions within an Evidence-Guided Attack Tree Search (EGATS) framework. PENTESTGPT V2 achieves up to 91% task completion on CTF benchmarks with frontier models (39 to 49% relative improvement over baselines) and compromises 4 of 5 hosts on the GOAD Active Directory environment versus 2 by prior systems. These results show that difficulty-aware planning yields consistent end-to-end gains across models and addresses a limitation that model scaling alone does not eliminate.

---

## **1 Introduction**

> **Section Summary:** Penetration testing is essential for assessing organizational security, yet the demand for skilled practitioners far exceeds


Penetration testing is essential for assessing organizational security, yet the demand for skilled practitioners far exceeds

supply. The ISC2 Cybersecurity Workforce Study estimates a global shortfall of 4.7 million cybersecurity professionals [14]. This gap, together with the labor-intensive nature of manual testing, has driven interest in large language model (LLM)–based automation.

Recent systems report strong results on benchmarks such as Capture-the-Flag challenges and Hack The Box (HTB) environments [8, 17, 19, 30, 32], and emerging work has demonstrated real-world impact, including the discovery of exploitable vulnerabilities in production software [10, 13]. However, reported task completion rates range from single digits under naive prompting to 40–80% with more sophisticated architectures [9, 20], raising a central question: _what drives these performance differences, and what limitations remain?_

To answer this question, we conduct a systematic analysis of 28 LLM-based penetration testing systems and evaluate five representative solutions across three benchmarks of increasing complexity. Our analysis yields two findings. First, existing systems are optimized to address the limitations of specific LLMs. For example, context summarization and RAG-augmented tooling are designed to compensate for transient LLM constraints of limited context windows and poor tool knowledge. Benefits brought by these designs quickly diminish as models improve: performance gaps across solutions compress by over half when backbone models upgrade from GPT-4o to GPT-5. Second, failures partition into two categories: _Type A failures_ (capability gaps) stem from missing tools and knowledge addressable through engineering, while _Type B failures_ (complexity barriers) persist regardless of tooling due to planning and state management limitations. Existing systems predominantly target Type A failures, achieving strong results on simple tasks but failing on multi-step scenarios where Type B failures dominate. This indicates that the architectures of existing penetration testing systems are not designed to complement the improvements of LLMs. Their contributions erode as models advance, rather than compounding with improved capabilities.

We trace Type B failures to a missing capability: _existing_


_penetration testing agent designs cannot assess task difficulty in real time_ . This manifests in several ways: agents commit prematurely to unproductive branches because they cannot estimate whether a path requires 3 or 30 steps; they fail to transition from reconnaissance to exploitation because they lack metrics for evidence sufficiency; they experience context forgetting because they do not monitor context consumption. Human pentesters handle these problems through intuition built from experience. LLM agents lack equivalent mechanisms for difficulty-aware decision making. We validate this diagnosis through controlled evaluation: augmenting agents with difficulty assessment reduces the Type B failure rate from 58% to 27% while Type A rate remains unchanged, confirming that this enhancement addresses the root cause.

We present PENTESTGPT V2, designed around these two findings. To eliminate Type A failures, an extensible _Tool and Skill Layer_ provides typed interfaces for 38 security tools and skill compositions that encode expert attack patterns. To address Type B failures, we introduce penetration testing _Task Difficulty Assessment_ (TDA), a mechanism that estimates task tractability through four measurable dimensions: horizon estimation, evidence confidence, context load, and historical success rate. TDA is integrated into an _EvidenceGuided Attack Tree Search_ algorithm that guides explorationexploitation decisions and prunes branches when paths become intractable. With these mechanisms, PENTESTGPT V2 dynamically pivots between attack paths based on real-time difficulty signals. It abandons unproductive branches before they exhaust the context budget and commits to exploitation only when evidence confidence justifies the investment. A retrieval-augmented _Memory Subsystem_ maintains structured state external to the LLM context, which prevents the context forgetting that derails extended attack campaigns.

We evaluate PENTESTGPT V2 across three benchmarks at different levels of realism, from CTF challenges to enterprise Active Directory environments. On XBOW [2] (104 web security tasks), PENTESTGPT V2 achieves 91% peak task completion (89% mean) with Claude Opus 4.5, a 49% relative improvement over the best baseline (61%). On the PentestGPT [8] Benchmark (13 HTB/VulnHub machines), PENTESTGPT V2 roots 12 of 13 machines, solving Hardrated targets where baselines become stuck at initial steps. On GOAD (5-host Active Directory environment), PENTESTGPT V2 compromises 4 of 5 hosts compared to at most 2 for prior systems, with successful lateral movement and credential chaining across domain boundaries. Ablation studies confirm that each component contributes distinctly: the Tool Layer dominates on short-horizon tasks, while TDA-EGATS and Memory provide the gains on multi-step scenarios.

Despite these results, hard challenges remain. Our evaluation shows that novel exploitation requiring creative reasoning, adversarial environments with deceptive defenses, and extended multi-week campaigns exceed current LLM capabilities. These limitations suggest that fully autonomous penetra-

tion testing remains distant. We discuss these boundaries and propose evaluation methodologies that distinguish tractable from intractable challenges, so that the community can focus effort where architectural innovation is most likely to help. In summary, we make the following contributions:

- **Systematic analysis of LLM agent failures** (§3). We analyze 28 systems and evaluate five implementations across three benchmarks, showing that existing architectures optimize for transient model constraints rather than persistent task challenges, and identifying two failure categories (Type A capability gaps and Type B complexity barriers) whose root causes require distinct solutions.

- **PENTESTGPT V2** (§4). We present a system addressing both failure types: a Tool and Skill Layer for Type A failures, and Task Difficulty Assessment integrated into EvidenceGuided Attack Tree Search for Type B failures.

- **Evaluation across three benchmarks** (§5). PENTESTGPT V2 achieves 91% on CTF benchmarks (49% improvement), roots 12/13 machines on realistic targets, and compromises 4/5 hosts on enterprise AD, doubling baseline performance.

- **Design principles** (§6). We analyze remaining barriers (novel exploitation, adversarial robustness) and propose evaluation methodologies that separately assess Type A and Type B performance.

- **Open-source artifacts** . We release PENTESTGPT V2’s implementation, tool interfaces, and evaluation scripts to support reproducibility [3].

---

## **2 Background**

---

## **2.1 Penetration Testing**

> **Section Summary:** Penetration testing identifies security vulnerabilities by simulating real-world attackers in blackbox/greybox scenarios.


Penetration testing identifies security vulnerabilities by simulating real-world attackers in blackbox/greybox scenarios. Standard methodologies decompose engagements into phases: _reconnaissance_ (information gathering), _enumeration_ (identifying services and entry points), _exploitation_ (gaining access), and _post-exploitation_ (privilege escalation and lateral movement) [26, 28]. This workflow follows a characteristic search pattern: _breadth-first exploration_ over attack surfaces followed by _depth-first exploitation_ along promising paths. Testers continuously decide which paths to pursue, when to abandon unproductive avenues, and how to integrate new discoveries. This interleaving of exploration and exploitation motivates our design (§4).

---

## **2.2 Benchmarking Penetration Testing**

> **Section Summary:** Evaluating penetration testing capabilities presents methodological challenges.


Evaluating penetration testing capabilities presents methodological challenges. Real-world engagements involve social engineering, multi-target reconnaissance, and complex business logic that cannot be easily replicated, while commercial tests produce confidential reports tied to proprietary systems. Standardized benchmarks address these con-


straints: _VulnHub_ [1] provides downloadable vulnerable VMs, _HTB_ [11] offers curated machines spanning difficulty levels, and _CTF_ competitions present challenges across web exploitation, cryptography, and binary exploitation.

Benchmarks differ from real-world targets in important ways. CTF challenges are designed to be solvable with a single attack path, whereas real systems may have no exploitable vulnerabilities or require broad discovery across a large attack surface. GOAD (Game of Active Directory) [25] is the closest approximation to realistic enterprise environments among current benchmarks, requiring chained attack techniques across multi-domain Windows networks, though it still abstracts away social engineering and time pressure. We interpret benchmark results as measuring specific technical capabilities rather than predicting overall real-world effectiveness.

---

## **2.3 LLM-Based Agents**

The standard approach for deploying LLMs as autonomous agents augments them with _tool use_ [31] that invokes external functions such as shell commands or APIs, and _agentic scaffolding_ that structures the interaction loop [15, 34]. Penetration testing is a natural application domain for such agents: it requires combining extensive domain knowledge with sequential decision-making, tool orchestration, and adaptive strategy. Early work explores LLMs as copilots suggesting next steps to human operators [8, 29], whereas more recent systems position LLMs as autonomous agents executing reconnaissance, exploitation, and post-exploitation workflows [17, 30, 32]. These agents must handle heterogeneous tool outputs, maintain coherent strategies across many interaction steps, and decide when to pivot between attack paths. These challenges push against the limits of current LLM capabilities. Similar limitations appear in software engineering [15] and web navigation [34], suggesting that the barriers are not specific to penetration testing.

---

## **3 Understanding LLM Agent Failures**

> **Section Summary:** _How far are we from achieving real-world penetration testing with LLM agents?_ To answer this question, we conduct an empirical analysis of existing LLM-based penetration testing systems.


_How far are we from achieving real-world penetration testing with LLM agents?_ To answer this question, we conduct an empirical analysis of existing LLM-based penetration testing systems. Our goals are to (1) understand what drives reported performance improvements, (2) identify failure modes through controlled evaluation, and (3) establish a framework for distinguishing tractable tasks from intractable challenges.

---

## **3.1 Taxonomy and Evaluation of LLM-based Penetration Testing**

> **Section Summary:** We survey LLM-based penetration testing systems, identifying 28 candidates published between 2023–2025.


We survey LLM-based penetration testing systems, identifying 28 candidates published between 2023–2025. Inclusion criteria require systems to use LLMs as a core component

Table 1: Taxonomy of LLM-based penetration testing systems

|**System**|**Year**|**Arch.**|**Tools**|**Know.**|**Planning**|
|---|---|---|---|---|---|
|PentestGPT [8]|2024|Workfow|Shell|Prompt|Task tree|
|AutoPT [32]|2024|Single|Shell|Prompt|State mach.|
|RapidPen [23]|2025|Single|Shell|RAG|ReAct|
|PentestAgent [30]|2024|Multi|Func.|RAG|Phase|
|VulnBot [17]|2025|Multi|Shell|Prompt|Tri-phase|
|xOffense [19]|2024|Multi|Shell|Fine-tune|Multi-phase|
|TermiAgent [20]|2024|Multi|Shell|RAG|Mem. tree|
|Cochise [12]|2025|Multi|Shell|Prompt|Hierarchical|


and target penetration testing or CTF challenges; we exclude vulnerability detection without exploitation and commercial systems without published details. Of 28 candidates, 10 meet our criteria, with the list in Appendix A.

### **3.1.1 Taxonomy**

We summarize each system along four dimensions: _architecture_ (multi-agent, human-in-the-loop), _tool integration_ (function calls, MCP [5]), _knowledge sources_ (RetrievalAugmented Generation (RAG), fine-tuned), and _planning_ (reactive, task trees, state machines, memory trees). Table 1 summarizes representative systems across three architectural families: human-in-the-loop copilots like PentestGPT [8], singleagent systems like AutoPT [32], and multi-agent systems like PentestAgent [30], VulnBot [17], and Cochise [12].

### **3.1.2 Evaluation Setup**

We evaluate five representative open-source systems: **PentestGPT** [8] (copilot), **AutoPT** [32] (single-agent), **PentestAgent** [30] (multi-agent with RAG), **VulnBot** [17] (multi-agent tri-phase), and **Cochise** [12] (Active Directory (AD)-focused). Benchmarks span three realism levels: **XBOW** [2] (104 web challenges: SQL injection (SQLi), cross-site scripting (XSS), auth bypass), **PentestGPT Benchmark** [8] (13 machines from HTB and VulnHub requiring end-to-end penetration testing), and **GOAD** [25] (5-host multi-domain AD requiring chained attacks).

For each system-benchmark pair, we evaluate with GPT4o, GPT-5, Gemini-3-Flash, and Claude Sonnet 4 to assess model vs. architecture contributions. We include GPT-4o (the model generation most existing systems were optimized for) alongside newer models to examine how architectural advantages evolve as underlying capabilities improve. §5 evaluates PENTESTGPT V2 with a different model set (GPT5.2, Opus 4.5, Gemini 3 Pro) selected specifically for thinking mode support, enabling controlled comparison of extended reasoning. We set temperature to zero and report best-of-three trials following prior work [8, 9], since penetration testing is inherently non-deterministic.


---

## **3.2 Findings**

> **Section Summary:** Table 2 summarizes task completion rates across all systemmodel-benchmark combinations.


Table 2 summarizes task completion rates across all systemmodel-benchmark combinations. We provide in-depth experimental results analysis below.

### **3.2.1 Agent Architecture Convergence**

Despite two years of agent design innovation, performance differences between systems compress with state-of-the-art models. On XBOW with GPT-4o, completion rates range from 27% to 39% across five systems, a 44% relative spread that reflects meaningful architectural distinctions. With GPT5, this gap narrows to 22.5% (40–49%); similar convergence appears on the PentestGPT Benchmark, where the spread shrinks from 2 points with GPT-4o (4–6 machines) to 1 point with GPT-5 (7–8 machines).

This convergence points to a limitation in how existing agents were designed: they address _transient_ model constraints rather than _persistent_ task challenges. Consider the techniques these systems employ. PentestGPT’s summarization module compensates for limited context windows, a constraint that largely dissolves as models gain native milliontoken support. Multi-agent architectures with role separation (e.g., reconnaissance agent, exploitation agent) work around weak instruction-following, yet frontier models handle complex multi-step prompts without explicit decomposition. RAG pipelines for tool documentation address poor parametric knowledge of security tools, yet recent models have much stronger baseline knowledge of common exploitation techniques and penetration testing tools. These “innovations” are workarounds for 2023-era model limitations, not solutions to persistent penetration testing challenges.

What distinguishes transient from persistent challenges? Transient challenges diminish as models improve: context capacity, instruction adherence, tool-use reliability, and domain knowledge all scale with model capability. Persistent challenges, by contrast, remain regardless of raw model power: long-horizon planning across 10+ exploitation steps, principled exploration-exploitation decisions, maintaining state external to degrading context, and real-time assessment of task difficulty. These challenges arise from the _structure of penetration testing tasks_ , not from model limitations, and thus require architectural solutions that _complement_ rather than _compensate for_ underlying models.

The Cochise case shows this distinction from a different angle. Cochise’s AD-specific attack primitives (Kerberoasting, NTLM relay, BloodHound integration) are capability additions that models cannot replicate through improved reasoning alone. However, this specialization comes at the cost of generality: Cochise underperforms on XBOW and the PentestGPT Benchmark (34% and 4/13 with GPT-4o) compared to general-purpose systems like VulnBot (39% and 6/13), while leading on GOAD by leveraging domain-specific knowledge unavailable to other systems. Neither approach, compensating


```mermaid
xychart-beta
    title "Failure Distribution vs Task Depth (Type A vs Type B)"
    x-axis "Task Depth (steps)" ["1-2", "3-4", "5-6", "7-8", "9+"]
    y-axis "Failure Distribution (%)" 0 --> 100
    line [72, 58, 41, 28, 15]
    %% Note: Area below line represents Type A: Capability Gaps
    %% Area above line represents Type B: Complexity Barriers
```


<!-- Start of picture text -->
Type A: Capability Gaps Type B: Complexity Barriers<br>100<br>75<br>85%<br>50 ComThresholdplexity<br>72%<br>25<br>0<br>1-2 3-4 5-6 7-8 9+<br>Task Depth (steps)<br>Failure Distribution (%)<br><!-- End of picture text -->

Figure 1: Failure type distribution by the task depth, measured as the number of distinct exploitation steps required for task completion.

for model limitations nor adding domain-specific capabilities, addresses the persistent challenge of navigating complex attack graphs.

**Finding 1:** Existing penetration testing agents address transient model limitations rather than persistent task challenges. As models evolves, benefits brought by architectural distinctions compress. Durable agent value should address challenges that persist across model evolution.

### **3.2.2 Two Distinct Failure Categories**

To understand _why_ systems fail rather than merely _how often_ , we analyze 200 execution traces from unsuccessful attempts (40 per system), sampling proportionally across benchmarks. Two researchers independently coded failure modes using open coding, then reconciled disagreements through discussion. Our analysis shows that failures partition into two distinct categories, classified based on observable trace characteristics _before_ any intervention.

_Type A failures_ (capability gaps) are identified when the trace shows the agent correctly reasons about the attack vector but fails at execution: the agent articulates the correct approach but then issues malformed commands or uses incorrect tool syntax. For instance, an agent may correctly identify a SQL injection vulnerability (e.g., “I will use SQL injection to extract data”) but fail because it lacks sqlmap or the correct documentation. To validate this classification, we augment PentestGPT with missing tool documentation and usage instructions; XBOW completion improves from 27% to 38%, a 41% relative improvement that confirms Type A failures respond to capability engineering as predicted.

_Type B failures_ (complexity barriers) are identified when the trace shows the agent possesses adequate tools and knowledge (evidenced by successful tool invocations earlier in the session) but fails to navigate the task space effectively. We


Table 2: Task completion rates across systems, models, and benchmarks. XBOW: task completion (%); PentestGPT Benchmark: machines rooted (/13); GOAD: hosts compromised (/5).

||**X**|**BOW (1**|**04 tasks)**||**Pentest**|**GPT-Ben**|**(13 ma**|**chines)**||**GOAD (**|**5 targets)**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**System**|GPT-4o|GPT-5|Gem.|Claude|GPT-4o|GPT-5|Gem.|Claude|GPT-4o|GPT-5|Gem.|Claude|
|PentestGPT|27|42|36|39|5|7|6|6|0|1|1|1|
|AutoPT|28|40|35|37|4|7|6|6|0|1|0|0|
|PentestAgent|34|**49**|42|**46**|**6**|7|6|6|0|1|0|1|
|VulnBot|**39**|45|**44**|**46**|**6**|**8**|6|**7**|0|1|0|1|
|Cochise|34|43|39|39|4|4|4|4|**1**|**2**|**2**|**2**|


Table 3: Failure mode analysis (200 traces). Type A failures resolve with tooling; Type B persist regardless.

|**Failure Category**<br>**F**|**req. (%)**|**Tooling?**|
|---|---|---|
|_Type A: Capability Gaps (42% total)_|||
|Missing tool / Incorrect syntax|26|✓|
|Output parsing / Knowledge gap|16|✓|
|_Type B: Complexity Barriers (58% total)_|||
|Context forgetting|18|–|
|Premature commitment|16|–|
|Exploration-exploitation imbalance|12|–|
|Multi-step chain failures|12|–|


identify three recurring patterns from trace analysis. _Context forgetting_ occurs when credentials discovered during reconnaissance are lost by the time exploitation begins, forcing redundant discovery or causing authentication failures. _Premature commitment_ occurs when agents dive deep into a single attack path without adequate reconnaissance, missing easier alternatives. _Exploration-exploitation imbalance_ is the inverse: exhaustive reconnaissance that never transitions to exploitation, accumulating information without acting on it. These issues cascade into chain errors: agents complete individual attack stages successfully but fail to integrate them into coherent attack chains, losing state between phases.

The distribution of failure types varies systematically with task complexity. On XBOW, where tasks typically require 1–3 steps, Type A failures dominate (68% of failures resolve with improved tooling). On GOAD, where successful attacks require chaining 5–10 steps across multiple hosts, Type B failures dominate (79% of failures persist regardless of tooling improvements). Figure 1 visualizes this relationship: Type A failures concentrate in short-horizon tasks while Type B failures dominate in task depth beyond 5 steps. Table 3 summarizes the failure mode distribution.

**Finding 2:** Failures partition into (a) _Type A: capability gaps_ , i.e., missing tools and knowledge addressable through engineering, and (b) _Type B: complexity barriers_ , i.e., search strategy and state management failures that persist despite adequate capabilities. These two categories require different solutions.

---

## **3.3 Analysis and Design Implications**

> **Section Summary:** We now present further analysis and design implications.


We now present further analysis and design implications.

### **3.3.1 Root Cause: Missing Difficulty Assessment**

Type B failures share a common root cause: agents cannot distinguish tractable from intractable tasks in real time. _Premature commitment_ occurs because agents cannot estimate whether a path requires 3 or 30 steps:
- without this estimate, they persist on unproductive branches indefinitely. _Exploration-exploitation imbalance_ occurs because agents lack metrics for when reconnaissance is sufficient
- they cannot determine whether gathered evidence justifies transitioning to exploitation. _Chain failures_ occur partly because agents cannot assess whether their accumulated context remains adequate for the current task
- critical information may have been lost or degraded without the agent’s awareness. For example, context forgetting occurs because agents lack difficulty metrics: without tracking context load, they cannot predict when accumulated history will overwhelm the model’s effective memory, leading to silent degradation of reasoning quality.

What would difficulty assessment require in practice? We identify four measurable dimensions: _horizon estimation_ (remaining steps to goal), _evidence confidence_ (certainty about current state), _context load_ (fraction of context window consumed), and _historical success_ (past performance on similar branches). These dimensions are measurable during execution, unlike abstract “difficulty” which is only knowable posthoc. An agent that tracks these signals can decide when to persist, when to pivot, and when to prune.

Current systems uniformly lack this capability. PentestGPT’s Penetration Testing Tree (PTT) tracks attack structure but provides no difficulty metrics to guide search. AutoPT’s Pentesting State Machine (PSM) enforces phase transitions


```mermaid
flowchart LR
    subgraph Input["Input"]
        Target["Attack Target<br/>(tree structure)"]
    end

    subgraph Excalibur["Excalibur Agent"]
        subgraph Planner["§4.3-4.4 TDA-EGATS Planner"]
            TDA["Task Difficulty Assessment<br/>H, E, C, S"]
            Mode["TDI-Guided Mode<br/>BFS / LLM / DFS"]
            TDA --> Mode
            Mode --> Ops["EGATS Operations"]
            Ops --> Tree["Attack Tree (EGATS)"]
        end

        Goal["Attack Goal"]

        subgraph Memory["§4.5 Memory Subsystem"]
            State["State"]
            Context["Context"]
            Branch["Branch Summaries"]
        end

        subgraph Tool["§4.2 Tool & Skill Layer"]
            Interfaces["Tool Interfaces"]
            Skill["Skill Composition"]
        end

        Planner <-->|Update| Memory
        Tree -->|2| Goal
        Goal --> Tool
    end

    subgraph Execution["Execution"]
        Network(("fa:fa-globe"))
        Inst["Attack Instruction"]
        Res["Execution Results"]
        Inst --> Network --> Res
    end

    subgraph Output["Output"]
        OutTree["Results<br/>Attack Path Completed"]
    end

    Target -->|1| Planner
    Tool -->|3| Inst
    Res -->|4| OutTree
    OutTree -.->|Feedback| Target
```


<!-- Start of picture text -->
Attack Target §4.3-4.4 TDA-EGATS Planner §4.5 Memory Subsystem Execution Results<br>structure)(as tree Task Difficulty Assessment EGATS Operations Update State Context Branch Summaries Results Attack Path<br>1 H  Horizon E  Evidence 4<br>C  Context S  Success Attack Tree (EGATS) §4.2 Tool & Skill Layer<br>TDI-Guided Mode R 2 Attack Skill 3 Attack ✓ Completed ✓ ✓<br>BFS LLM DFS ✓ ✗ P Goal Tool Interfaces Composition Instruction<br>Input Excalibur Agent Output<br><!-- End of picture text -->

Figure 2: PENTESTGPT V2 architecture. The TDA-EGATS Planner addresses Type B failures through difficulty-aware tree search with Upper Confidence Bound (UCB) selection, TDI-guided mode switching, and evidence-based pruning. The Tool & Skill Layer addresses Type A failures through typed tool interfaces and RAG-augmented knowledge. The Memory Subsystem maintains structured state and enables selective context injection based on tree position.

but does not assess path complexity. TermiAgent’s memory tree improves context management but does not inform exploration-exploitation decisions. None of these systems can answer the question that matters most: _is this path worth pursuing?_

### **3.3.2 Design Implications**

Our analysis points to a two-part strategy for advancing LLMbased penetration testing. _Eliminating Type A failures_ requires comprehensive tool interfaces with typed schemas, RAG systems for exploit documentation and Common Vulnerabilities and Exposures (CVE) databases, and standardized execution environments. This is tedious engineering work, but it produces predictable returns: each tool added directly enables new attack capabilities.

_Addressing Type B failures_ requires a different approach: real-time difficulty estimation, principled explorationexploitation decisions guided by the estimates, active pruning of intractable branches to prevent search collapse, and state maintenance external to conversation context to prevent information loss. These requirements suggest tree-based search algorithms to maintain state explicitly rather than relying on LLM’s context window.

Neither approach alone is sufficient. Capability engineering yields strong short-horizon performance but fails on complex tasks where navigation becomes the bottleneck. Planning innovation without adequate tooling produces agents that reason well but cannot execute. Effective systems must address both failure categories simultaneously, and in particular, agents need the ability to assess task difficulty in real time to avoid exploration-exploitation imbalance and chain failures.

---

## **4 Design of PENTESTGPT V2**

---

## **4.1 Overview**

> **Section Summary:** We present PENTESTGPT V2, designed around the analysis in §3.3 to address both failure categories through dedicated architectural components.


We present PENTESTGPT V2, designed around the analysis in §3.3 to address both failure categories through dedicated architectural components. Figure 2 provides its architectural overview. PENTESTGPT V2 is a _single-agent_ system that communicates with the environment consistently, operating over different components to complete penetration testing. It consists of the following modules: (1) A _Tool and Skill Layer_ that eliminates Type A failures through structured tool interfaces and knowledge augmentation (§4.2). (2) A _Task Difficulty Assessment_ (TDA) mechanism that estimates tractability in real time (§4.3), integrated into an _Evidence-Guided Attack Tree Search_ (EGATS) algorithm that replaces the traditional PTT structure for exploration-exploitation decisions (§4.4). (3) A _Memory Subsystem_ that maintains state across attack phases to prevent context forgetting (§4.5).

Given a target, PENTESTGPT V2 ❶ initializes an attack tree with the target as the root node. At each step, the EGATS planner consults the TDA module to select the current attack goal and updates the memory subsystem to preserve context. ❷ The selected goal is translated into concrete actions via the Tool and Skill Layer, and ❸ the resulting commands are executed in the test environment. ❹ Execution results are parsed and incorporated back into the attack tree and memory state, feeding into subsequent planning iterations until the penetration testing process terminates. Below we detail each component.

---

## **4.2 Tool and Skill Layer**

Type A failures arise not from fundamental capability limitations, but from inconsistent tool usage: LLMs invoke security tools with incorrect parameters, misparse outputs, or lack domain knowledge about tool capabilities. Rather than proposing novel techniques, the Tool and Skill Layer represents


careful engineering to ensure LLM agents interact with security tools consistently and reliably. We build on established concepts of Agent Skills [4] from Anthropic (typed interfaces, skill composition, and retrieval-augmented generation), adapting them to penetration testing where tool reliability directly determines attack success.

**Typed Tool Interfaces.** Each security tool is exposed through a typed interface specifying input schema (parameters with types, defaults, and validation rules), output schema (structured representation parsed from command output), and pre/postconditions (required state before invocation and expected effects after completion). The LLM receives explicit documentation rather than relying on parametric knowledge. Input validation catches errors before execution, and structured outputs eliminate parsing ambiguity. We implement interfaces for 38 tools across six categories: reconnaissance, web exploitation, network exploitation, credential attacks, Active Directory attacks, and privilege escalation. Appendix B provides the complete tool list we integrate.

**Skill Composition.** Beyond individual tools, _skills_ compose multiple tool invocations into higher-level attack capabilities that encode expert knowledge about common attack patterns. Skills provide fallback logic so that when a preferred tool fails, the system can try alternatives automatically. They also aggregate results from multiple tools into coherent findings and encode multi-step attack patterns that reflect how human testers chain operations.

**Knowledge Augmentation.** The layer integrates a RAG system containing tool documentation, an exploit database (CVE descriptions indexed by service version), and attack playbooks (step-by-step procedures for common patterns such as Kerberoasting, AS-REP roasting, and pass-the-hash). The knowledge base contains only generic attack techniques from public security resources (MITRE ATT&CK, OWASP, tool documentation); it excludes CTF writeups, HTB walkthroughs, or benchmark-specific solutions to prevent data leakage in evaluation. When the agent encounters an unfamiliar service or vulnerability class, relevant documentation is retrieved and injected into context automatically.

These three mechanisms together provide a unified, reliable interface between LLM agents and security tools. None of these techniques is novel in isolation; their contribution lies in the combination, which minimizes tool invocation errors that otherwise cascade into attack failures. Our ablation study (§5.3) shows that this engineering effort yields substantial gains on capability-limited tasks: the Tool Layer alone improves XBOW completion by 14% (from 54% to 68%), allowing agents to focus their reasoning on the harder problems of planning and strategy.

---

## **4.3 Task Difficulty Assessment (TDA)**

> **Section Summary:** Our analysis in §3.3 identifies the inability to assess task difficulty as the root cause of Type B failures.


Our analysis in §3.3 identifies the inability to assess task difficulty as the root cause of Type B failures. Premature commit-

ment occurs because agents cannot estimate whether a path requires 3 or 30 steps. Exploration-exploitation imbalance occurs because agents have no metric for when reconnaissance is sufficient. Chain failures occur because agents cannot judge whether accumulated context is adequate for the current task.

Human penetration testers face the same problem: they do not know task difficulty _a priori_ . Instead, they estimate difficulty from signals that accumulate during execution, such as the number of failed attempts on a path, the quality of evidence gathered so far, and intuitions about remaining work. An experienced tester who has tried five exploits without success knows to try a different approach; one who has confirmed a vulnerable service version knows to commit to exploitation. TDA operationalizes this reasoning for LLM agents through four measurable dimensions, with context window consumption added as a signal unique to language models.

### **4.3.1 TDA Dimensions**

TDA computes difficulty along four dimensions grounded in quantities measurable during execution.

**Horizon Estimation (** _H_ **).** We estimate the number of remaining steps to reach the goal from the current position, normalized across active branches. A pilot study on 50 traces from an independent GOAD deployment (using GPT-4o, separate from evaluation) shows that while absolute estimates have poor calibration (MAE of 4.2 steps), rank correlation is strong (Spearman’s ρ = 0 _._ 71, _p <_ 0 _._ 001). The TDI formula therefore uses _H_<sup>ˆ</sup> , the _normalized_ horizon estimate (min-max scaled across active branches), converting absolute estimates into relative rankings where LLM judgment is reliable. **Historical Success Rate (** _S_ **).** The Laplace-smoothed success rate on the current branch captures learning from failed attempts. Low values indicate repeated failures, suggesting that the current path is likely intractable. This dimension directly addresses _premature commitment_ : agents learn to abandon unproductive paths rather than persisting indefinitely. **Context Load (** _C_ **).** The fraction of context window consumed, directly measurable from token counts. LLM performance degrades as context fills: retrieval accuracy drops, earlier information is forgotten, and reasoning quality declines [18]. We define an _ideal working window_ of 40% of the model’s context capacity, based on a controlled study showing consistent accuracy degradation beyond this point (94% _→_ 78% at 60% load, 61% at 80%; see Appendix D.6). Beyond this threshold, context pruning becomes necessary to preserve reasoning quality. This dimension addresses _context forgetting_ : by tracking context load, the system detects when accumulated history threatens to overwhelm the model’s effective memory.

**Evidence Confidence (** _E_ **).** The mean confidence score across the path from root to current node, computed from evidence categories at each node. We assign scores based on evidence type: verified exploits and valid credentials receive 1.0, con-


firmed vulnerabilities with available exploits receive 0.8, plausible hypotheses (version-matched vulnerabilities, misconfigurations) receive 0.5, and speculative hypotheses receive 0.3. Tool outputs are parsed to determine evidence type: successful authentication or shell access indicates verified evidence, vulnerability scanner confirmations with CVE matches indicate confirmed vulnerabilities, and service version matches against exploit databases indicate plausible hypotheses. Appendix C details the complete scoring rubric. This dimension addresses _exploration-exploitation imbalance_ : high confidence signals readiness to exploit, while low confidence signals the need for more reconnaissance.

Table 4: Search strategy comparison. EGATS is the only approach that combines external structure, evidence-based pruning, and TDA-guided mode selection.

|**Approach**|**Structure**|**Pruning**|**Diffculty**|**TDA**|
|---|---|---|---|---|
|ReAct|None|–|–|–|
|PTT [8]|Tree (text)|Manual|–|–|
|PSM [32]|Finite state machine|–|–|–|
|PMT [20]|Tree|–|–|–|
|**EGATS**|Tree (ext.)|Evidence|✓|✓|


---

## **4.4 Evidence-Guided Attack Tree Search (EGATS)**

### **4.3.2 Task Difficulty Index**

TDA combines the above 4 dimensions into a Task Difficulty Index (TDI):


```mermaid
flowchart TD
    Eq["<b>Equation 1: Task Difficulty Index (TDI)</b><br/><br/>TDI = w_H * H&#770; + w_E * (1 - E) + w_C * C + w_S * (1 - S)"]
    style Eq fill:#fff,stroke:#333,stroke-width:1px,font-family:serif,font-size:16px
```


where _H_<sup>ˆ</sup> is the normalized horizon estimate and all weights sum to 1. Higher TDI indicates greater difficulty. We set _wH_ = _wE_ = 0 _._ 3 and _wC_ = _wS_ = 0 _._ 2 based on grid search over a validation set of 30 execution traces from HTB machines not included in the PentestGPT benchmark (retired machines from 2022–2023, predating our evaluation set). We test 256 configurations with each weight in _{_ 0 _._ 1 _,_ 0 _._ 2 _,_ 0 _._ 3 _,_ 0 _._ 4 _}_ constrained to sum to 1.0; task completion varies within _±_ 3% across configurations where all weights remain in [0 _._ 1 _,_ 0 _._ 4], indicating that the approach is not sensitive to precise weight selection.

TDI guides three operational decisions. _Mode selection:_ high TDI ( _>_ θexplore = 0 _._ 6) triggers reconnaissance (BFS) to gather more information before committing; low TDI ( _<_ θexploit = 0 _._ 3) triggers exploitation (DFS). For intermediate values (0 _._ 3 _≤_ TDI _≤_ 0 _._ 6), the system invokes LLMDECIDE: the LLM receives the current node state, TDI value, and individual dimension scores ( _H_ , _S_ , _C_ , _E_ ), then selects between reconnaissance and exploitation with a brief justification. This design acknowledges that intermediate difficulty may warrant either approach depending on context the TDI formula cannot fully capture. For instance, a moderately difficult path with high evidence confidence may warrant exploitation, while one with low confidence benefits from further reconnaissance. _Branch prioritization:_ TDI ranks paths beyond promise scores alone, since two branches with similar promise may differ substantially in tractability based on horizon and success history. _Pruning:_ branches with persistently high TDI ( _>_ θprune = 0 _._ 8) after _k_ min = 3 attempts are pruned to prevent the search from collapsing into unproductive regions. These thresholds are derived through grid search on the same validation set used for TDI weights. Appendix D presents sensitivity analysis showing robustness across threshold ranges.

EGATS integrates TDA into a tree-based search framework, adapting Monte Carlo Tree Search (MCTS) [6, 16] to penetration testing. EGATS differs from standard MCTS in three ways: it explicitly separates reconnaissance (BFS) and exploitation (TDI-guided) phases, it replaces simulation-based value estimates with TDA-based difficulty assessment, and it prunes intractable branches based on evidence.

### **4.4.1 Attack Tree Structure**

EGATS maintains an Attack Tree _T_ = ( _V, E,_ φ _,_ ψ _,_ δ) where _V_ contains nodes representing attack states, _E_ contains edges representing actions, φ : _V →_ [0 _,_ 1] assigns promise scores, ψ : _V →S_ maps nodes to state snapshots, and δ : _V →_ [0 _,_ 1] assigns TDI scores. Nodes are categorized as _observation_ (discovered facts), _hypothesis_ (untested attack possibilities), or _action_ (executed steps with outcomes).

The _promise score_ φ( _n_ ) estimates the likelihood that node _n_ leads to successful exploitation. For hypothesis nodes, promise is initialized via LLM assessment of vulnerability severity, exploit availability, and prerequisite satisfaction; the model estimates success probability given current evidence. For action nodes, promise is updated based on execution outcomes: successful actions propagate increased promise to ancestor nodes, while failures decrease promise along the path. After action _a_ with outcome _o ∈{success, partial, failure}_ , we update φ( _n_ ) _←_ α _·_ φ( _n_ )+(1 _−_ α) _·r_ ( _o_ ) where _r_ ( _success_ ) = 1 _._ 0, _r_ ( _partial_ ) = 0 _._ 5, _r_ ( _failure_ ) = 0 _._ 1, and α = 0 _._ 7 controls the learning rate. Through this backpropagation, branches with consistent successes accumulate high promise while repeatedly failing branches see diminishing scores.

Unlike PentestGPT’s text-based PTT, EGATS maintains structure externally via algorithmic operations, which prevents corruption and enables systematic search guidance. Table 4 compares EGATS with related approaches.

### **4.4.2 The EGATS Algorithm**

Algorithm 1 presents the TDA-guided search procedure. SELECTNODE uses UCB to balance exploitation and explo-


**Algorithm 1** TDA-Guided Attack Tree Search

**Require:** Target _T_ , budget _B_ **Ensure:** Attack tree _T_ , compromised hosts _C_ 1: _T ←_ INITTREE( _T_ )

- 2: **while** _B >_ 0 **and not** GOALREACHED **do**

3: _n ←_ SELECTNODE( _T_ ) _▷_ UCB selection 4: TDI _n ←_ COMPUTETDI( _n_ ) 5: **if** TDI _n >_ θexplore **then** 6: EXECUTERECON( _n_ ); EXPANDTREE( _T_ , _n_ ) 7: **else if** TDI _n <_ θexploit **then** 8: _result ←_ EXECUTEEXPLOIT( _n_ ) 9: BACKPROPAGATEEVIDENCE( _T_ , _n_ , _result_ ) 10: **if** _result.success_ **then** SPAWNPIVOT( _T_ , _result.host_ ) 11: **end if** 12: **else** 13: LLMDECIDE( _n_ , TDI _n_ ) 14: **end if** 15: **if** δ( _n_ ) _>_ θprune **and** _Nn > k_ min **then** 16: PRUNEBRANCH( _T_ , _n_ ) 17: **end if** 18: _B ← B −_ 1 19: **end while**

ration:


```mermaid
flowchart TD
    Eq["<b>Equation 2: Upper Confidence Bound (UCB)</b><br/><br/>UCB(n) = &phi;(n) + c * &radic;(ln N / N_n) - &lambda; * &delta;(n)"]
    style Eq fill:#fff,stroke:#333,stroke-width:1px,font-family:serif,font-size:16px
```


where φ( _n_ ) is the promise score, _N_ is total actions, _Nn_ is actions on node _n_ ’s subtree, _c_ = _√_ 2 is the exploration constant, and the _−_ λ _·_ δ( _n_ ) term penalizes high-difficulty nodes (λ = 0 _._ 5, validated via grid search; see Appendix D).

After selection, EGATS computes TDI and switches between BFS (reconnaissance) and DFS (exploitation) based on the thresholds described above. Evidence backpropagates after each action, updating promise scores and TDI along affected paths. When exploitation succeeds, _pivot spawning_ is triggered: the compromised host becomes a new subtree root, and discovered credentials propagate to relevant hypothesis nodes elsewhere in the tree.

Pruning removes branches when TDI exceeds 0.8 after three attempts, which prevents infinite loops on intractable paths. To avoid premature pruning, a credential propagation mechanism re-evaluates pruned branches when new credentials are discovered that may satisfy their preconditions.

---

## **4.5 Memory Subsystem**

> **Section Summary:** Long-context forgetting is a primary cause of Type B failures (§3.2).


Long-context forgetting is a primary cause of Type B failures (§3.2). The Memory Subsystem addresses this with a hybrid architecture that separates persistent state from conversational context, and integrates with TDA via the context load dimension.

A _State Store_ maintains a structured database of discovered facts independent of conversation context. The store tracks five entity types: hosts (IP addresses, hostnames, OS fingerprints), services (ports, versions, configurations), credentials (usernames, passwords, hashes, tickets), sessions (active shells, tunnels, pivots), and vulnerabilities (CVE identifiers, exploitation status, prerequisites). Each entry is timestamped and linked to its discovery node in the attack tree, which enables provenance tracking and ensures facts persist regardless of conversation length. The State Store also supports accurate TDA context load computation by providing ground truth about what information the agent “knows” versus what must be re-derived from context.

_Selective context injection_ replaces full history maintenance. When operating on node _n_ , context is assembled from: path context (the sequence of actions from root to _n_ ), a node state snapshot (complete state at _n_ including all relevant entity relationships), target-relevant facts (entries from State Store pertaining to _n_ ’s target host or service), and sibling branch summaries (compressed representations of parallel exploration paths). As context load approaches the ideal working window threshold (40%), less-relevant context is progressively compressed using LLM-generated summaries. Beyond 70%, aggressive pruning removes older path segments while preserving findings to prevent performance degradation.

_Branch summaries_ compress detailed execution history when switching branches. Each summary preserves the current status (active, pruned, completed), findings (discovered credentials, confirmed vulnerabilities), TDI at time of suspension, and recommended next actions. TDI is stored with each summary to inform revisit decisions: when new credentials are discovered elsewhere in the tree, branches with matching preconditions and previously high TDI are re-evaluated for potential reactivation.

---

## **5 Evaluation**

> **Section Summary:** We assess the performance of PENTESTGPT V2 through four research questions:


We assess the performance of PENTESTGPT V2 through four research questions:

- **RQ1** : Does PENTESTGPT V2 outperform existing systems across different penetration testing scenarios?

- **RQ2** : What is the contribution of the each designed architectural component?

- **RQ3** : How does TDA-EGATS change the agent’s attack strategy compared to prior approaches?

- **RQ4** : Can PENTESTGPT V2 be practically deployed for real-world penetration testing?

---

## **5.1 Experimental Setup**

> **Section Summary:** PENTESTGPT V2 is implemented in Python ( _∼_ 8,500 lines), with the Tool Layer, TDA-EGATS Planner, and Memory Subsystem as separate modules.


PENTESTGPT V2 is implemented in Python ( _∼_ 8,500 lines), with the Tool Layer, TDA-EGATS Planner, and Memory Subsystem as separate modules. The implementation is open-


Table 5: Performance comparison across systems, models, and benchmarks. Each model column is split into non-thinking (–) and thinking (T) modes. XBOW: task completion (%); PentestGPT Benchmark: machines rooted (/13); GOAD: hosts compromised (/5). Best results per column in **bold** . All results report mean across 3 trials; variance _±_ 2–3% on XBOW, _±_ 1 machine on PentestGPT-Ben.

|GPT<br>**System**<br>–|**XB**<br>-5.2<br>T|**OW**<br>Opu<br>–|**(104 t**<br>s 4.5<br>T|**asks)**<br>Gem<br>–|ini 3<br>T|**Pen**<br>GPT<br>–|**testG**<br>-5.2<br>T|**PT-**<br>Opu<br>–|**Ben (1**<br>s 4.5<br>T|**3 ma**<br>Ge<br>–|**chines)**<br>mini 3<br>T|GP<br>–|**G**<br>T-5.2<br>T|**OAD**<br>Op<br>–|**(5 ho**<br>us 4.5<br>T|**sts)**<br>Ge<br>–|mini 3<br>T|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|PentestGPT<br>45|53|47|54|41|48|7|8|6|7|6|7|1|1|1|2|1|1|
|AutoPT<br>43|50|44|51|38|45|6|7|7|8|5|6|1|1|0|1|1|1|
|PentestAgent<br>52|61|54|60|46|54|8|9|7|9|7|8|1|2|2|2|1|1|
|VulnBot<br>48|56|50|58|43|51|8|9|8|9|6|8|2|2|1|2|1|2|
|**PENTESTGPT V2**<br>**76**|**85**|**81**|**91**|**76**|**79**|**11**|**12**|**10**|**12**|**10**|**11**|**3**|**4**|**3**|**4**|**3**|**3**|


sourced [3]. Following the evaluation methodology in Section 3.1, we evaluate PENTESTGPT V2 on three benchmarks of increasing complexity. **XBOW** [2] comprises 104 CTFstyle web security challenges covering SQL injection, XSS, authentication bypass, and file inclusion; these short-horizon tasks isolate Type A failures where tool usage determines success. The **PentestGPT Benchmark** [8] consists of 13 machines from HTB and VulnHub, requiring end-to-end penetration testing from reconnaissance through privilege escalation to root access. Difficulty ranges from Easy to Hard, with 9–22 subtasks per machine, representing realistic scenarios that demand multi-step attack chains. **GOAD** [25] provides a 5-host multi-domain Active Directory environment requiring credential harvesting, Kerberoasting, lateral movement, and domain escalation, complex enterprise scenarios dominated by Type B failures.

We compare against four baseline systems: PentestGPT v1.0 [8], AutoPT [32], PentestAgent [30], and VulnBot [17]. We exclude Cochise [12] from this comparison because its AD-specialized architecture creates an uneven evaluation as shown in Section 3.2. Baseline systems use their original tool invocation mechanisms to reflect realistic deployment comparisons; reported improvements therefore reflect both tool integration and architectural contributions. To isolate architectural contributions from model capabilities, all systems are evaluated with three frontier models: GPT-5.2, Claude-Opus4.5, and Gemini-3.0-Pro. We select these models for two reasons: (1) they represent state-of-the-art capabilities at the time of evaluation, and (2) all three support toggling between standard and thinking modes, enabling controlled comparison of extended reasoning effects. We report task completion rate, subtask progress, and exploration metrics including branch diversity, backtrack frequency, and time-to-pivot. We report mean performance across trials with standard deviation where variance is meaningful; for discrete outcomes (machines rooted, hosts compromised), we report best-of-three following prior work [8, 9] since standard deviation on small integers provides limited insight. For XBOW’s continuous completion rates, we report both headline best-of-three results

and trial statistics ( _µ_ : mean, σ: standard deviation across the three trials) to characterize variance. In total, we conduct 5 systems _×_ 118 evaluation units _×_ 6 model configurations _×_ 3 trials, yielding 10,620 evaluation runs at an estimated cost of $2,760 USD in API tokens (Table 8 reports PENTESTGPT V2-specific costs).

---

## **5.2 RQ1: Overall Performance**

> **Section Summary:** Table 5 shows the performance comparison across all systemmodel-benchmark combinations, with consistent patterns that align with our Type A/B failure framework.


Table 5 shows the performance comparison across all systemmodel-benchmark combinations, with consistent patterns that align with our Type A/B failure framework.

On XBOW, PENTESTGPT V2 achieves 91% task completion (best-of-3; _µ_ =89%, σ=2.1%) with Opus 4.5 thinking mode, a 49% relative improvement over the best baseline (PentestAgent at 61%, _µ_ =59%, σ=1.8%). With GPT-5.2 thinking, PENTESTGPT V2 achieves 85% ( _µ_ =83%, σ=2.4%) compared to 61% for PentestAgent. Even comparing means, the gap (89% vs. 59%) exceeds 15 standard deviations, confirming robust architectural differences: the Tool Layer eliminates Type A failures while TDA-EGATS prevents trial-and-error loops that consume baseline attempts. Thinking mode provides 6– 10 point improvements across all systems and configurations but does not close the architectural gap.

The PentestGPT benchmark shows larger architectural differences. PENTESTGPT V2 roots 12 of 13 machines with both GPT-5.2 and Opus 4.5 thinking (consistent across all three trials), compared to 9 for the best baseline (VulnBot), a 33% relative improvement. PENTESTGPT V2 solves both Hardrated machines (Joker and Falafel) where baseline systems became “stuck at initial steps,” and also completes machines that require non-obvious attack chains. The improvement concentrates in machines requiring non-linear attack paths: while baseline PTT structures lead to premature commitment on initial hypotheses, TDA-EGATS enables strategic backtracking when evidence confidence drops, allowing the agent to discover alternative attack vectors. Thinking mode amplifies architectural differences: PENTESTGPT V2 gains 1–2 machines from thinking, achieving near-complete coverage,


Table 6: Ablation study results (GPT-5.2 thinking). Base: raw shell access with reactive prompting. Each row adds a component cumulatively.


```mermaid
xychart-beta
    title "Performance by Configuration (XBOW %)"
    x-axis ["Base", "+Tool", "+EGATS", "Full (Memory)"]
    y-axis "Performance (%)" 0 --> 100
    bar [54, 68, 77, 85]
```


<!-- Start of picture text -->
Configuration XBOW Pentest-Ben GOAD<br>Base 54 8 2<br>+ Tool Layer 68 9 2<br>+ TDA-EGATS 77 11 3<br>+ Memory (Full) 85 12 4<br>XBOW PentestGPT-Ben GOAD<br>Largest gain: +Tool (+14%) Largest gain: +EGATS (+15%) Largest gain: +EGATS (+20%)<br>100 100 92% 100<br>85%<br>80%<br>80 80 80<br>60 60 60<br>40 40 40<br>20 20 20<br>0 0 0<br>Base +Tool +EGATS +Memory Full<br>Base+Tool+EGATS+Memory Full Base+Tool+EGATS+Memory Full Base+Tool+EGATS+Memory Full<br>Performance (%)<br><!-- End of picture text -->

Figure 3: Ablation study across benchmarks (GPT-5.2 thinking). Performance is normalized to percentage scale.

Table 7: Search behavior comparison on the PentestGPT benchmark (mean across 13 machines).

|**Metric**|**PentestGPT**|**PENTESTGPT V2**|
|---|---|---|
|Branches explored|3.2|7.8|
|Backtrack rate (%)|8|34|
|Avg. depth before pivot|12.4|5.1|
|Successful pivots|0.4|2.6|
|Pruned branches|–|4.2|


TDA-EGATS adds further gains: +9 points on XBOW (from 68 to 77) through reduced trial-and-error, +2 machines on the PentestGPT benchmark (from 9 to 11), and +1 host on GOAD (from 2 to 3). These gains span both Type A failures (via more efficient search) and Type B failures (via principled exploration-exploitation). The Memory Subsystem contributes across all benchmarks: +8 points on XBOW (from 77 to 85), +1 machine on the PentestGPT benchmark (from 11 to 12), and +1 host on GOAD (from 3 to 4). The GOAD improvement is worth noting separately: extended attack campaigns cause context forgetting in systems without explicit state management, and Memory enables the credential persistence required for the fourth compromise.

while baselines gain only 1 machine each but plateau at 9.

GOAD shows the largest improvement. PENTESTGPT V2 compromises 4 of 5 hosts with GPT-5.2 and Opus 4.5 thinking (4 hosts in all three trials; the same four hosts each time) versus at most 2 for baselines—doubling the compromise rate (80% vs. 40%). This pattern holds consistently across all three models and both reasoning modes (even Gemini 3 achieves 3 hosts vs. 1–2 for baselines), indicating a robust architectural effect. Baselines achieve initial foothold but fail to progress through lateral movement; PENTESTGPT V2 executes coherent multi-host attack chains using the Memory Subsystem for credential persistence and TDA for exploration guidance.

---

## **5.3 RQ2: Ablation Study**

> **Section Summary:** To isolate each component’s contribution, we evaluate system variants with individual components disabled.


To isolate each component’s contribution, we evaluate system variants with individual components disabled. Table 6 presents results using GPT-5.2 thinking mode; the base configuration uses raw shell access with reactive prompting and sliding-window context management. Figure 3 visualizes component contributions across all model configurations.

The results align with our Type A/B failure framework. The Tool Layer provides the largest improvement on XBOW (+14 points, from 54 to 68), consistent with CTF failures being predominantly engineering problems addressable through better tooling. The Tool Layer alone yields zero improvement on GOAD (remaining at 2 hosts), where planning rather than capability determines success.

---

## **5.4 RQ3: Strategy Analysis**

> **Section Summary:** Beyond aggregate performance, we analyze how TDAEGATS changes the agent’s attack strategy compared to PentestGPT’s PTT-based approach.


Beyond aggregate performance, we analyze how TDAEGATS changes the agent’s attack strategy compared to PentestGPT’s PTT-based approach.

### **5.4.1 Search Behavior**

Table 7 compares exploration patterns across the PentestGPT benchmark. The metrics show qualitatively different search behaviors between the two systems.

PentestGPT follows a deep-first pattern: it explores fewer branches (3.2 vs. 7.8) but commits to each for longer (average depth 12.4 steps before pivoting vs. 5.1 for PENTESTGPT V2), reflecting the premature commitment failure mode where agents persist on initial hypotheses without signals to recognize intractability.

PENTESTGPT V2 with TDA-EGATS follows an adaptive pattern: TDI monitoring triggers backtracking when success rate drops, and evidence confidence guides exploitation timing. The 4.2 pruned branches per machine are paths abandoned due to persistently high TDI, preventing the infinite loops observed in baseline systems.

### **5.4.2 Case Study: HTB Falafel**

Falafel is a Hard-rated HTB machine requiring a multi-stage attack chain that combines web exploitation, cryptographic


quirks, and privilege escalation through Linux group memberships. Figure 4 contrasts how PentestGPT and PENTESTGPT V2 navigate this challenge.

The attack begins with web enumeration revealing a login form that produces different error messages for valid versus invalid usernames, enabling user discovery through fuzzing. Boolean-based blind SQL injection in the username field allows extracting password hashes from the database. The key step is recognizing that the admin hash begins with “0e462...”, == a format that PHP’s loose comparison operator ( ) interprets as scientific notation. Submitting the string “240610708” produces an MD5 hash also starting with “0e”, causing both values to compare as zero and bypassing authentication without password cracking. Post-authentication, a filename truncation vulnerability enables code execution: the system truncates filenames exceeding 237 characters, so uploading a file named [232 A’s].php.png results in an executable .php file after truncation removes the .png extension. Privilege escalation chains through three stages: database credentials in the PHP configuration yield user moshe; membership in the video group enables framebuffer capture that reveals yossi’s password displayed on screen; membership in the disk group allows reading root’s files directly via debugfs.

PentestGPT successfully extracts the password hashes but commits to direct cracking via hashcat. After 47 failed attempts with various wordlists and rules, context degradation prevents the model from revisiting the hash format—the type juggling vector is never considered.

PENTESTGPT V2’s EGATS tree develops differently. When hash cracking yields repeated failures, rising TDI triggers exploration of authentication alternatives. The Knowledge Augmentation component surfaces PHP type juggling documentation when queried about hashes starting with “0e”, enabling the bypass. The Memory Subsystem preserves credentials discovered at each privilege escalation stage, enabling the complete chain from www-data through moshe and yossi to root.

### **5.4.3 Failure Case: PlayerTwo**

To illustrate where TDA-EGATS falls short, we examine PlayerTwo, the only PentestGPT Benchmark machine PENTESTGPT V2 fails to compromise. PlayerTwo requires exploiting a custom Protobuf-based game protocol with no public documentation. PENTESTGPT V2 correctly identifies the service through reconnaissance and spawns hypothesis branches for protocol fuzzing. However, TDI rises rapidly due to repeated failures (low _S_ ) and high horizon estimates (the LLM cannot predict steps for an unknown protocol). After three unsuccessful fuzzing attempts, the branch is pruned correctly by TDA’s design logic, since success rate indicates intractability.

This failure exposes a TDA limitation: it cannot distinguish “difficult but tractable” from “novel requiring creative reasoning,” as both present as high TDI. When RAG retrieval


```mermaid
flowchart TD
    subgraph PTT["(a) PentestGPT (PTT)"]
        S1["Start"] --> E1["Enum"]
        E1 --> SQL1["SQLi (0.3)"]
        E1 -.-> Dir1["Dir (abandoned)"]
        E1 -.-> Ports1["Ports (abandoned)"]
        SQL1 --> Hash1["Hash (0.4)"]
        Hash1 --> BF1["BF-1 (0.5)"]
        BF1 -.-> BF25["BF-25 (0.7)<br/>Stuck: no backtrack"]
        BF25 -.-> BF47["BF-47 (0.9)<br/>Context degraded"]
    end

    subgraph EGATS["(b) Excalibur (EGATS)"]
        S2["Start"] --> E2["Enum"]
        E2 --> SQL2["SQLi (0.3)"]
        E2 -.-> XSS2["XSS (pruned)"]
        E2 --> Auth2["Auth (0.5)"]
        SQL2 --> Hash2["Hash (0.4)"]
        Hash2 --> BF2_1["BF (0.7)"]
        BF2_1 -.->|TDI pivot<br/>triggers backtrack| Auth2
        Auth2 --> RAG["RAG (0.3)"]
        RAG --> TypeJ["TypeJ (0.2)"]
        TypeJ --> Shell["Shell (0.1)"]
        Shell --> Root["Root Success"]
    end
```


<!-- Start of picture text -->
(a) PentestGPT (PTT) (b) Excalibur (EGATS)<br>Start Start<br>Enum Enum<br>SQLi 0.3 Dir Ports SQLi 0.3 XSS Auth 0.5<br>abandoned abandoned prunedTDI pivot<br>Hash 0.4 TDI Hash 0.4 RAG 0.3<br>BF-1 0.5 BF 0.7 TypeJ 0.2<br>BF-25 0.7 Stuck:no backtrack (TDI=0.7 triggers backtrack) Shell 0.1<br>BF-47 0.9 Context degraded(47 failed attempts) SuccessRoot<br>Success Failed Exploring Pruned TDI Pivot<br><!-- End of picture text -->

Figure 4: HTB Falafel exploration comparison. (a) PentestGPT commits to password brute-force after extracting hashes and stalls after 47 attempts. (b) PENTESTGPT V2’s TDIguided exploration discovers the type juggling bypass when hash cracking fails, then navigates the privilege escalation chain.

Table 8: Resource consumption per task (median values, GPT5.2 thinking).

|**Benchmark**|**LLM Calls**|**Time (min)**|**Cost ($)**|
|---|---|---|---|
|XBOW|12|3.2|0.18|
|PentestGPT-Ben|87|42|4.20|
|GOAD|234|186|28.50|


finds no relevant documentation and the LLM lacks parametric knowledge, TDA’s evidence-based signals provide no useful guidance. TDA-EGATS therefore improves navigation through _known_ attack spaces but does not address _novel_ exploitation requiring genuine invention.

---

## **5.5 RQ4: Real-World Deployment**

> **Section Summary:** To assess practical viability, we evaluate PENTESTGPT V2’s resource consumption.


To assess practical viability, we evaluate PENTESTGPT V2’s resource consumption. We further deploy it in a live competition environment to examine its real-world performance.

### **5.5.1 Cost Analysis**

Table 8 presents the resource consumption across benchmarks. PENTESTGPT V2 requires 23% fewer LLM calls than the baseline average on XBOW (12 vs. 15.6 median calls per task) due to reduced trial-and-error from structured tool interfaces, while achieving 39% higher success rates (85% vs. 61%). On GOAD, total calls increase by 18% due to more thorough exploration enabled by EGATS, but this yields 2 _×_ more compromised hosts (4 vs. 2). On a per-success basis, PENTESTGPT V2 is 1.8 _×_ more cost-effective on XBOW and 1.7 _×_ more cost-effective on GOAD: the overhead of EGATS is more than offset by the higher success rates. A complete GOAD engagement costs approximately $28.50 and achieves 80% environment compromise (4 of 5 hosts), making automated penetration testing economically viable for enterprise


Table 9: HTB Season 8 performance by difficulty (May– August 2025). Total: 10/13 machines (76.9%).

|**Diffculty**|**Completed**|**Total**|**Rate**|
|---|---|---|---|
|Easy|4|4|100%|
|Medium|4|4|100%|
|Hard|2|3|67%|
|Insane|0|2|0%|
|**Total**|**10**|**13**|**76.9%**|


security assessments.

### **5.5.2 Live Competition Deployment**

We deployed PENTESTGPT V2 during HTB Season 8 (May– August 2025), a live competition with 13 newly released machines whose solutions remain unavailable until the season concludes. This provides a direct test of real-world viability: unlike retired benchmark machines, Season machines incorporate recent CVEs and novel attack chains with no public walkthroughs.

PENTESTGPT V2 with Opus 4.1 completed 10 of 13 machines (76.9%), achieving a global ranking in the top 100 out of 8,036 active participants.

Table 9 summarizes performance by difficulty. All four Easy machines and all four Medium machines were compromised successfully. Among Hard machines, PENTESTGPT V2 completed Certificate and RustyKey but failed on Mirage. Both Insane machines, _Sorcery_ and _Cobblestone_ , remained unsolved. The three failures, Mirage (Hard), Sorcery (Insane), and Cobblestone (Insane), represent machines where PENTESTGPT V2 exhausted its search space without finding viable attack paths. These results align with the PlayerTwo analysis (§5.4): when RAG retrieval yields no relevant documentation and the underlying model lacks parametric knowledge of the target vulnerability class, TDA-EGATS cannot guide exploration effectively.

The Season 8 deployment shows that PENTESTGPT V2 can operate in realistic penetration testing scenarios where solutions are unknown and time-constrained. The 100% success rate on Easy and Medium machines suggests readiness for deployment on typical enterprise targets, while Hard and Insane failures mark the current boundaries where human expertise is still required.

---

## **6 Discussion**

---

## **6.1 Limitations and Threats to Validity**

> **Section Summary:** We discuss factors that bound the generalizability of our findings.


We discuss factors that bound the generalizability of our findings.

**Benchmark Scope.** Our evaluation covers web security, network penetration testing, and Active Directory attacks, but

omits binary exploitation, mobile security, and cloud-specific attack scenarios where different challenges may dominate. Binary exploitation requiring precise memory layout reasoning poses distinct challenges not captured by our benchmarks. The PentestGPT Benchmark uses retired machines with public walkthroughs, which may inflate absolute numbers through data contamination; however, TDA, EGATS, and Memory target planning challenges orthogonal to specific vulnerability knowledge and thus transfer to novel scenarios. Real-world engagements also involve active defenses and novel vulnerability classes absent from historical benchmarks.

**Model-Specific Effects.** We obtain results with three frontier models (GPT-5.2, Claude-Opus-4.5, Gemini-3.0-Pro). Different model architectures show different strengths: Opus 4.5 achieves the highest XBOW performance (91%), which suggests that our architectural contributions may interact differently across model families. Future model generations may shift the easy/hard boundary and potentially resolve challenges we currently classify as hard.

**Baseline Fairness.** We use published baseline code with default parameters; original authors might achieve better results through tuning, though this reflects realistic deployment scenarios. Because baselines use their original tool invocation mechanisms, reported improvements reflect both tool integration and architectural contributions.

**Failure Analysis.** We analyze PENTESTGPT V2’s remaining failures to characterize current boundaries. On XBOW, the 9 failed tasks (9%) fall into two categories: blind injection that requires extensive timing-based exfiltration (4 tasks), and multi-stage attacks that require creative payload chaining not present in our RAG corpus (5 tasks). The single unsolved PentestGPT Benchmark machine (PlayerTwo, Hard) requires exploiting a custom protocol with no public documentation, a novel exploitation scenario that demands reasoning beyond pattern matching. On GOAD, the fifth host (the forest root domain controller) requires a specific attack chain (PrintNightmare _→_ DCSync) that PENTESTGPT V2 identifies but fails to execute due to token constraints. These failures indicate that while PENTESTGPT V2 addresses Type B failures effectively, novel exploitation that requires creative reasoning remains an open problem.

---

## **6.2 What Remains Hard**

> **Section Summary:** Despite PENTESTGPT V2’s gains, three categories of irreducible Type B failures persist that better tooling, larger corpora, or improved prompting cannot resolve.


Despite PENTESTGPT V2’s gains, three categories of irreducible Type B failures persist that better tooling, larger corpora, or improved prompting cannot resolve.

**The Creativity Barrier.** LLMs are effective at pattern matching but struggle with out-of-distribution generalization [21]. The PlayerTwo failure illustrates this gap: PENTESTGPT V2 systematically explores attack vectors yet fails because no documented exploitation pattern exists for the custom Protobuf-based protocol. The distinction between “difficult” and “novel” matters here. Difficult tasks respond to improved


search; novel tasks require reasoning capabilities that current architectures do not provide.

**The Adversarial Environment Barrier.** Penetration testing occurs against active defenders who can exploit agent reasoning patterns [33]. Honeypots, canary tokens, and deceptive services can poison the agent’s state representation, causing it to pursue false attack paths or trigger detection. PENTESTGPT V2’s evidence grounding protects against self-generated hallucinations but offers limited defense against environmentallyinduced false beliefs: when a honeypot presents a convincing vulnerable service, the agent cannot tell whether the vulnerability is genuine or a deliberate trap. This asymmetry favors defenders, who can study and exploit agent behavior, while agents lack the meta-awareness to recognize manipulation. **The Temporal Scale Barrier.** Human pentesters maintain mental models across engagements that span weeks, correlating information from separate sessions and exercising strategic patience. EGATS improves multi-step reasoning within sessions and the Memory Subsystem preserves state, but neither addresses cross-session continuity. Long-horizon planning is a different problem from long-context processing: it requires hierarchical abstraction, goal decomposition, and progress monitoring, none of which current transformer architectures natively support [27].

---

## **7 Conclusion**

This paper presents a systematic analysis of LLM-based penetration testing that identifies a distinction between Type A failures (capability gaps addressable through engineering) and Type B failures (complexity barriers requiring architectural innovation). We introduce PENTESTGPT V2, which addresses Type A failures through a Tool and Skill Layer with typed interfaces and RAG, and addresses Type B failures via Task Difficulty Assessment (TDA) integrated into Evidence-Guided Attack Tree Search (EGATS). PENTESTGPT V2 achieves 91% task completion on CTF benchmarks (49% improvement over baselines) and compromises 4 of 5 hosts on the GOAD Active Directory environment versus 2 for prior systems. Our ablation studies show that TDAguided exploration provides benefits beyond tree structure alone: difficulty-aware planning produces value that model improvements cannot replicate.


---

## **References**

> **Section Summary:** - [1] Vulnhub: Vulnerable by design.


- [1] Vulnhub: Vulnerable by design. https://www. vulnhub.com/, 2012–2026.

- [2] XBOW — AI-Powered Offensive Security Platform. https://xbow.com/, 2024.

- [3] Anonymous. Excalibur: Source code and artifacts. https://anonymous.4open.science/r/ Excalibur-FA7D, 2025. Anonymous repository for double-blind review.

- [4] Anthropic. Equipping agents for the real world with Agent Skills, October 2024. Engineering Blog. URL: https://www.anthropic.com/engineering/ equipping-agents-for-the-real-world-withagent-skills.

- [5] Anthropic. Model context protocol. https:// modelcontextprotocol.io/, 2024. An open protocol for connecting AI assistants to external data sources and tools, released November 2024.

- [6] Rémi Coulom. Efficient selectivity and backup operators in Monte-Carlo tree search. In _Computers and Games: 5th International Conference, CG 2006, Turin, Italy, May 29-31, 2006. Revised Papers 5_ , pages 72–83. Springer, 2007. URL: https://link.springer.com/ chapter/10.1007/978-3-540-75538-8_7, doi:10. 1007/978-3-540-75538-8_7.

- [7] Isaac David and Arthur Gervais. Multi-agent penetration testing ai for the web. _arXiv preprint arXiv:2508.20816_ , 2025.

- [8] Gelei Deng, Yi Liu, Víctor Mayoral-Vilches, Peng Liu, Yuekang Li, Yuan Xu, Tianwei Zhang, Yang Liu, Martin Pinzger, and Stefan Rass. PentestGPT: Evaluating and harnessing large language models for automated penetration testing. In _Proceedings of the 33rd USENIX Security Symposium (USENIX Security 24)_ , pages 847– 864. USENIX Association, 2024.

- [9] Luca Gioacchini, Marco Mellia, Idilio Drago, Alexander Delsanto, Giuseppe Siracusano, and Roberto Bifulco. AutoPenBench: Benchmarking generative agents for penetration testing. _

- [10] Google Project Zero. From naptime to big sleep: Using large language models to catch vulnerabilities in realworld code. https://projectzero.google/2024/ 10/from-naptime-to-big-sleep.html, October 2024.

- [11] Hack The Box. Hack the box: Hacking training for the best. https://www.hackthebox.com/, 2024. Online platform with curated collection of vulnerable machines for penetration testing practice and skill development.

- [12] Andreas Happe and Jürgen Cito. Can LLMs hack enterprise networks? autonomous assumed breach penetration-testing active directory networks. _ACM Transactions on Software Engineering and Methodology_ , 2025. doi:10.1145/3766895.

- [13] Sean Heelan. How I used o3 to find CVE-2025-37899, a remote zeroday vulnerability in the Linux kernel’s SMB implementation. https://sean.heelan.io/ 2025/05/22/how-i-used-o3-to-find-cve-202537899-a-remote-zeroday-vulnerability-inthe-linux-kernels-smb-implementation/, May 2025.

- [14] ISC2. ISC2 cybersecurity workforce study 2024. https://www.isc2.org/Insights/2024/10/ISC22024-Cybersecurity-Workforce-Study, 2024.

- [15] Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik R Narasimhan. SWE-bench: Can language models resolve real-world github issues? In _The Twelfth International Conference on Learning Representations_ , 2024.

- [16] Levente Kocsis and Csaba Szepesvári. Bandit based Monte-Carlo planning. In _Machine Learning: ECML 2006: 17th European Conference on Machine Learning, Berlin, Germany, September 18-22, 2006. Proceedings 17_ , pages 282–293. Springer, 2006. URL: https://link.springer.com/chapter/10.1007/ 11871842_29, doi:10.1007/11871842_29.

- [17] He Kong, Die Hu, Jingguo Ge, Liangxiong Li, Tong Li, and Bingzhen Wu. VulnBot: Autonomous penetration testing for a multi-agent collaborative framework. _

- [18] Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. Lost in the middle: How language models use long contexts. _Transactions of the Association for Computational Linguistics_ , 12:157–173, 2024. doi: 10.1162/tacl_a_00638.

- [19] Phung Duc Luong, Le Tran Gia Bao, Nguyen Vu Khai Tam, Dong Huu Nguyen Khoa, Nguyen Huu Quyen, Van-Hau Pham, and Phan The Duy. xOffense: An AIdriven autonomous penetration testing framework with offensive knowledge-enhanced LLMs and multi agent systems. _

- [20] Wuyuao Mai, Geng Hong, Qi Liu, Jinsong Chen, Jiarun Dai, Xudong Pan, Yuan Zhang, and Min Yang. Shell or nothing: Real-world benchmarks and memoryactivated agents for automated penetration testing, 2025. URL: https://arxiv.org/abs/2509.09207, arXiv:2509.09207.

- [21] Iman Mirzadeh, Keivan Alizadeh, Hooman Shahrokhi, Oncel Tuzel, Samy Bengio, and Mehrdad Farajtabar. Gsm-symbolic: Understanding the limitations of mathematical reasoning in large language models, 2025. URL: https://arxiv.org/abs/2410.05229, arXiv:2410.05229.

- [22] Lajos Muzsai, David Imolai, and András Lukács. Hacksynth: Llm agent and evaluation framework for autonomous penetration testing. _

- [23] Sho Nakatani. RapidPen: Fully automated IP-to-shell penetration testing with LLM-based agents. _

- [24] Sho Nakatani. Rapidpen: Fully automated ip-to-shell penetration testing with llm-based agents. _

- [25] Orange Cyberdefense. GOAD - game of active directory. https://github.com/Orange-Cyberdefense/ GOAD, 2024. A pentest Active Directory LAB project providing vulnerable AD environments for practicing attack techniques.

- [26] OWASP Foundation. OWASP web security testing guide. https://owasp.org/www-project-websecurity-testing-guide/, 2021. Version 4.2. Comprehensive guide to testing the security of web applications and web services.

- [27] Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, and Joseph E. Gonzalez. Memgpt: Towards llms as operating systems, 2024. URL: https://arxiv.org/abs/2310.08560, arXiv:2310.08560.

- [28] PTES Technical Guideline Development Team. Penetration testing execution standard (PTES). http: //www.pentest-standard.org, 2012. A comprehensive standard for conducting penetration tests, defining seven main phases from pre-engagement to reporting.

- [29] Minghao Shao, Boyuan Chen, Sofija Jancheska, Brendan Dolan-Gavitt, Siddharth Garg, Ramesh Karri, and Muhammad Shafique. An empirical evaluation of LLMs for solving offensive security challenges. _

- [30] Xiangmin Shen, Lingzhi Wang, Zhenyuan Li, Yan Chen, Wencheng Zhao, Dawei Sun, Jiashui Wang, and Wei Ruan. PentestAgent: Incorporating LLM agents to automated penetration testing. In _Proceedings of the 20th ACM Asia Conference on Computer and Communications Security (ASIA CCS ’25)_ , pages 375–391. ACM, 2025.

- [31] Georg Wölflein, Dyke Ferber, Daniel Truhn, Ognjen Arandjelovic, and Jakob Nikolas Kather. LLM agents making agent tools. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics_ , pages 26092–26130, Vienna, Austria, July 2025. Association for Computational Linguistics. URL: https: //aclanthology.org/2025.acl-long.1266/, doi: 10.18653/v1/2025.acl-long.1266.

- [32] Benlong Wu, Guoqiang Chen, Kejiang Chen, Xiuwei Shang, Jiapeng Han, Yanru He, Weiming Zhang, and Nenghai Yu. AutoPT: How far are we from the end2end automated web penetration testing? _

- [33] Qiusi Zhan, Richard Fang, Henil Shalin Panchal, and Daniel Kang. Adaptive attacks break defenses against indirect prompt injection attacks on llm agents, 2025. URL: https://arxiv.org/abs/2503.00061, arXiv:2503.00061.

- [34] Shuyan Zhou, Frank F. Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Yonatan Bisk, Daniel Fried, Uri Alon, et al. Webarena: A realistic web environment for building autonomous agents. In _The Twelfth International Conference on Learning Representations (ICLR)_ , 2024.

---

## **A Surveyed LLM-Based Penetration Testing Systems**

> **Section Summary:** Table 10 presents the complete list of 28 candidate systems identified in our survey.


Table 10 presents the complete list of 28 candidate systems identified in our survey. Systems meeting our inclusion criteria (LLM as core component, targeting penetration testing or CTF challenges, with published technical details) are marked with ✓.

---

## **B Tool and Skill Layer: Supported Tools**

> **Section Summary:** Table 11 lists the 38 security tools integrated into PENTESTGPT V2’s Tool and Skill Layer.


Table 11 lists the 38 security tools integrated into PENTESTGPT V2’s Tool and Skill Layer. Each tool is exposed through a typed interface specifying input parameters, output schema, and pre/postconditions. Tool selection reflects standard penetration testing methodology and aligns with tools commonly used in professional certifications (e.g., OSCP) and real-world assessments.


Table 10: Complete list of surveyed LLM-based penetration testing systems. Systems marked with ✓meet our inclusion criteria and are analyzed in Section 3.

|**System**|**Source**|**Year**|**Included**|
|---|---|---|---|
|PentestGPT [8]|USENIX Security|2024|✓|
|AutoPT [32]|arXiv|2024|✓|
|RapidPen [24]|arXiv|2025|✓|
|PentestAgent [30]|arXiv|2024|✓|
|VulnBot [17]|arXiv|2025|✓|
|xOffense [19]|arXiv|2025|✓|
|TermiAgent [20]|arXiv|2025|✓|
|HackSynth [22]|arXiv|2024|✓|
|MAPTA [7]|arXiv|2025|✓|
|Cochise [12]|arXiv|2025|✓|
|_Excluded: Vulnerability_|_detection only_|||
|VulnScanner-AI|GitHub|2024||
|LLM-SecAudit|arXiv|2024||
|CodeVuln|arXiv|2024||
|BugHunter|RAID|2024||
|AutoFuzz-LLM|CCS|2024||
|_Excluded: Commercial/n_|_o details_|||
|Pentera|Commercial|2024||
|Cobalt Strike AI|Commercial|2024||
|CrowdStrike Charlotte|Commercial|2024||
|_Excluded: Non-exploitat_|_ion focus_|||
|CTF-Helper|arXiv|2023||
|CryptoSolver|arXiv|2024||
|RevEngGPT|arXiv|2024||
|MalwareGPT|arXiv|2024||
|ThreatGPT|arXiv|2024||
|SecurityBot|GitHub|2024||
|DFIR-Assistant|arXiv|2024||
|IRBot|arXiv|2025||
|SOC-Copilot|arXiv|2024||
|VulnReport-LLM|arXiv|2024||


---

## **C Evidence Confidence Scoring**

> **Section Summary:** Table 12 presents the complete evidence confidence scoring rubric used by the TDA mechanism.


Table 12 presents the complete evidence confidence scoring rubric used by the TDA mechanism. Scores are assigned deterministically based on evidence type, enabling reproducible difficulty assessment.

**Path Confidence Computation.** For a path _P_ = ( _n_ 0 _, n_ 1 _,..., nk_ ) from root to current node, the evidence confidence is computed as:


```mermaid
flowchart TD
    Eq["<b>Equation 3: Average Path Evidence E(P)</b><br/><br/>E(P) = (1/k) * &Sigma; e(n_i)"]
    style Eq fill:#fff,stroke:#333,stroke-width:1px,font-family:serif,font-size:16px
```


where _e_ ( _ni_ ) is the confidence score assigned to node _ni_ based on Table 12. The root node _n_ 0 is excluded as it represents the initial state before any evidence is gathered.

**Tool Output Parsing.** Evidence types are determined automatically by parsing tool outputs against expected patterns.

For example, nmap output containing “open” with a service version triggers version-matched vulnerability lookup (0.5); sqlmap output containing “injectable” triggers confirmed injection (0.8); successful ssh connection triggers valid credentials (1.0). The Tool Layer’s typed interfaces (Section 4.2) provide structured outputs that simplify this parsing.

**Example.** Consider a path: _port scan → web server (nginx 1.18) → directory bruteforce → login form discovered → SQL injection confirmed_ . Evidence scores are: 0.3 (service identified), 0.5 (version-matched to known nginx vulnerabilities), 0.3 (endpoint exists), 0.8 (injection confirmed). Path confidence _E_ = (0 _._ 3 + 0 _._ 5 + 0 _._ 3 + 0 _._ 8) _/_ 4 = 0 _._ 475, indicating moderate confidence appropriate for transitioning from reconnaissance to exploitation.

---

## **D Parameter Derivation and Validation**

> **Section Summary:** This appendix documents the derivation and sensitivity analysis for hyperparameters in PENTESTGPT V2.


This appendix documents the derivation and sensitivity analysis for hyperparameters in PENTESTGPT V2.

---

## **D.1 Validation Dataset**

> **Section Summary:** All hyperparameters are tuned on a held-out validation set of 30 execution traces from retired HTB machines (2022– 2023), disjoint from the PentestGPT Benchmark evaluation set.


All hyperparameters are tuned on a held-out validation set of 30 execution traces from retired HTB machines (2022– 2023), disjoint from the PentestGPT Benchmark evaluation set. The validation set includes 10 Easy, 12 Medium, and 8 Hard machines, covering web exploitation (12), Linux privilege escalation (10), and Windows/AD attacks (8). We use GPT-4o for validation to avoid overlap with evaluation models (GPT-5.2, Opus 4.5, Gemini 3).

---

## **D.2 TDI Weight Selection**

> **Section Summary:** Table 13 presents TDI weights derived via grid search over _w ∈_ [0 _._ 1 _,_ 0 _._ 4] with step size 0.05, subject to ∑ _wi_ = 1.


Table 13 presents TDI weights derived via grid search over _w ∈_ [0 _._ 1 _,_ 0 _._ 4] with step size 0.05, subject to ∑ _wi_ = 1. Performance is measured as mean subtask completion rate across the validation set.

Performance varies within _±_ 3% across configurations where all weights remain in [0 _._ 1 _,_ 0 _._ 4], indicating robustness to precise weight selection. The selected configuration ( _wH_ = _wE_ = 0 _._ 3, _wC_ = _wS_ = 0 _._ 2) reflects domain intuition: horizon and evidence confidence are primary difficulty signals, while context load and success rate provide secondary modulation.

---

## **D.3 Mode Selection Thresholds**

> **Section Summary:** Table 14 presents sensitivity analysis for mode selection thresholds (θexplore, θexploit).


Table 14 presents sensitivity analysis for mode selection thresholds (θexplore, θexploit).

The intermediate zone (θexploit _≤_ TDI _≤_ θexplore) triggers LLMDECIDE. Narrower zones reduce LLM calls but sacrifice adaptivity; wider zones increase overhead without proportional benefit.


---

## **D.4 Pruning Parameters**

> **Section Summary:** The pruning threshold (θprune = 0 _._ 8) and minimum attempts ( _k_ min = 3) prevent both premature and excessively delayed pruning.


The pruning threshold (θprune = 0 _._ 8) and minimum attempts ( _k_ min = 3) prevent both premature and excessively delayed pruning.

Lower thresholds increase false pruning (abandoning tractable paths); higher thresholds waste attempts on intractable paths. The selected configuration achieves favorable balance.

---

## **D.5 UCB Difficulty Penalty**

> **Section Summary:** The difficulty penalty coefficient (λ = 0 _._ 5) modulates how strongly TDI affects node selection in the UCB formula.


The difficulty penalty coefficient (λ = 0 _._ 5) modulates how strongly TDI affects node selection in the UCB formula.

λ = 0 recovers standard UCB, which underperforms due to insufficient difficulty awareness. λ = 1 _._ 0 over-penalizes difficult nodes, preventing exploration of challenging but tractable paths.

---

## **D.6 Context Load Degradation Study**

> **Section Summary:** To establish the 40% context load threshold, we conduct a controlled study measuring LLM instruction-following accuracy under varying context loads.


To establish the 40% context load threshold, we conduct a controlled study measuring LLM instruction-following accuracy under varying context loads.

**Methodology.** We construct 50 penetration testing instructionfollowing tasks from an independent GOAD deployment (separate from evaluation instances). Each task comprises a system state description, accumulated context (tool outputs, discovered information), and a specific instruction (e.g., “Extract the service account password from the Kerberoast output and attempt authentication”). Tasks are designed with unambiguous correct responses, enabling binary accuracy scoring.

For each task, we generate context variants at 10%, 20%, 30%, 40%, 50%, 60%, 70%, 80%, and 90% of the model’s context window. Context padding uses realistic penetration testing artifacts: verbose tool outputs, reconnaissance results, and session histories from actual GOAD runs. Padding is inserted before the instruction to simulate accumulated session context. We evaluate GPT-4o (128K context), Claude3-Sonnet (200K context), and Gemini-1.5-Pro (1M context) with temperature 0, running each task-context combination three times.

Performance remains stable ( _>_ 90%) up to 40% load, then degrades approximately linearly. The 40% threshold represents the inflection point beyond which additional context yields diminishing returns and begins actively harming performance.

**Failure Mode Analysis.** Beyond 40% load, failures concentrate in three categories: ignoring relevant information from earlier context (42% of failures), hallucinating tool outputs not present in context (31%), and executing incorrect but plausible commands (27%). These patterns align with the “lost in the middle” phenomenon documented in prior work [18].


Table 11: Security tools integrated into PENTESTGPT V2. Each tool has a typed interface specifying input schema, output parsing, and execution constraints.

|**Category**|**Tool**|**Description**|
|---|---|---|
||nmap<br>masscan<br>gobuster|Network discovery, port/service scanning, OS fngerprinting<br>High-speed port scanner for large networks<br>Directory/DNS bruteforcing for web discovery|
|Reconnaissance|ffuf|Web fuzzer for directories, parameters, vhosts|
||feroxbuster<br>nikto<br>whatweb|Recursive web content discovery<br>Web server vulnerability scanner<br>Web technology fngerprinting|
||enum4linux|SMB/Samba enumeration (users, shares, OS)|
||sqlmap|SQL injection detection and exploitation|
||burpsuite|Web proxy for traffc interception and testing|
|Web Exploitation|zap<br>wfuzz<br>commix|OWASP web vulnerability scanner<br>Web fuzzer for parameters and authentication<br>Command injection exploitation|
||nuclei|Template-based CVE and misconfguration scanner|
||metasploit<br>netcat|Exploitation framework with pre/post-exploitation modules<br>TCP/UDP networking utility|
||crackmapexec|Windows/AD post-exploitation toolkit|
|Network Exploitation|responder<br>evil-winrm<br>chisel<br>proxychains|LLMNR/NBT-NS poisoner for credential capture<br>WinRM shell with pass-the-hash support<br>HTTP tunneling for network pivoting<br>SOCKS/HTTP proxy routing for pivoting|
||hashcat|GPU password cracker (300+ hash types)|
||john|Rule-based password cracker|
|Credential Attacks|hydra<br>impacket<br>kerbrute|Online bruteforcing (50+ protocols)<br>Protocol library (secretsdump, psexec, wmiexec)<br>Kerberos user enumeration and password spraying|
||bloodhound<br>sharphound<br>rubeus|AD attack path visualization via graph analysis<br>BloodHound data collector<br>Kerberos attack toolkit (roasting, tickets)|
|Active Directory|mimikatz<br>powerview<br>ldapdomaindump|Memory credential extraction<br>AD enumeration PowerShell tool<br>LDAP data extraction|
||pingcastle<br>adrecon|AD security assessment and risk scoring<br>AD reconnaissance reporting|
||linpeas|Linux privesc enumeration|
|Privilee Escalation|winpeas|Windows privesc enumeration|
|g|pspy<br>seatbelt|Linux process monitor (cron, scheduled tasks)<br>Windows security auditing|


Table 12: Evidence confidence scoring rubric. Scores are assigned based on the strongest evidence type at each node; when multiple evidence types are present, the highest applicable score is used.

|**Evidence Type**|**Score**|**Indicators**|
|---|---|---|
|_Verifed Evidence (Exploita_|_tion Con_|_frmed)_|
|Valid credentials|1.0|Successful authentication via SSH, WinRM, SMB, or web login|
|Shell access|1.0|Interactive command execution confrmed|
|Data exfltration|1.0|Sensitive data retrieved (fags, database contents, confg fles)|
|_Confrmed Vulnerability (E_|_xploit Av_|_ailable)_|
|CVE with public exploit|0.8|Vulnerability scanner confrmation + Exploit-DB/Metasploit<br>module exists|
|Auth bypass confrmed|0.8|Endpoint accessible without credentials when authentication<br>expected|
|Injection confrmed|0.8|SQL/command injection produces observable side effects|
|_Plausible Hypothesis (Evid_|_ence Sup_|_ports)_|
|Version-matched vuln|0.5|Service version matches known vulnerable version range|
|Confguration weakness|0.5|Misconfguration identifed (default credentials, open permis-<br>sions)|
|Information disclosure|0.5|Sensitive information leaked (usernames, paths, internal IPs)|
|_Speculative Hypothesis (Mi_|_nimal Ev_|_idence)_|
|Service identifed|0.3|Port open with service fngerprint, no version/vulnerability match|
|Potential attack surface|0.3|Endpoint exists but no vulnerability indicators|
|Unconfrmed assumption|0.3|Hypothesis based on common patterns without direct evidence|


Table 13: TDI weight sensitivity analysis. Performance (subtask completion %) across weight configurations. Bold indicates selected weights.

|_wH_|_wE_|_wC_|_wS_|Performance (%)|
|---|---|---|---|---|
|0.25|0.25|0.25|0.25|71.2|
|**0.30**|**0.30**|**0.20**|**0.20**|**73.8**|
|0.35|0.25|0.20|0.20|72.4|
|0.25|0.35|0.20|0.20|73.1|
|0.30|0.25|0.25|0.20|72.9|
|0.40|0.30|0.15|0.15|70.8|


Table 14: Mode selection threshold sensitivity. Performance (subtask completion %) across threshold configurations.

|θexplore|θexploit|Performance (%)|
|---|---|---|
|0.5|0.2|72.1|
|0.5|0.3|72.8|
|0.6|0.2|73.2|
|**0.6**|**0.3**|**73.8**|
|0.6|0.4|72.4|
|0.7|0.3|73.0|
|0.7|0.4|71.6|


Table 15: Pruning parameter sensitivity. Metrics: subtask completion (%), branches incorrectly pruned (%), wasted attempts on intractable branches (mean count).

|θprune|_k_min|Completion|False Prune|Wasted|
|---|---|---|---|---|
|0.7|2|71.2|8.4|2.1|
|0.7|3|72.4|5.2|3.4|
|**0.8**|**3**|**73.8**|**2.8**|**4.1**|
|0.8|4|73.2|1.9|5.8|
|0.9|3|72.1|1.2|6.9|


Table 16: UCB difficulty penalty (λ) sensitivity.

|λ|Completion (%)|Backtrack Rate (%)|
|---|---|---|
|0.0 (standard UCB)|68.4|12|
|0.25|71.2|21|
|**0.5**|**73.8**|**34**|
|0.75|72.1|42|
|1.0|69.8|51|
