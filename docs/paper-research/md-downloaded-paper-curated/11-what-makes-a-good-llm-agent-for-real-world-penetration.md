# 🎯 What Makes a Good LLM Agent for Real-world Penetration Testing?

## 📋 Table of Contents

- [🚀 Abstract](#abstract)
- [1 Introduction](#1-introduction)
- [📖 2 Background](#2-background)
  - [2.1 Penetration Testing](#21-penetration-testing)
  - [📌 2.2 Benchmarking Penetration Testing](#22-benchmarking-penetration-testing)
  - [📌 2.3 LLM-Based Agents](#23-llm-based-agents)
- [🔍 3 Understanding LLM Agent Failures](#3-understanding-llm-agent-failures)
  - [3.1 Taxonomy and Evaluation of LLM-based Penetration Testing](#31-taxonomy-and-evaluation-of-llm-based-penetration-testing)
  - [🧠 3.2 Findings](#32-findings)
  - [🏗️ 3.3 Analysis and Design Implications](#33-analysis-and-design-implications)
- [🏗️ 4 Design of PENTESTGPT v2](#4-design-of-pentestgpt-v2)
  - [4.1 Overview](#41-overview)
  - [🔧 4.2 Tool and Skill Layer](#42-tool-and-skill-layer)
  - [📏 4.3 Task Difficulty Assessment (TDA)](#43-task-difficulty-assessment-tda)
  - [📌 4.4 Evidence-Guided Attack Tree Search (EGATS)](#44-evidence-guided-attack-tree-search-egats)
  - [💾 4.5 Memory Subsystem](#45-memory-subsystem)
- [📊 5 Evaluation](#5-evaluation)
  - [5.1 Experimental Setup](#51-experimental-setup)
  - [5.2 RQ1: Overall Performance](#52-rq1-overall-performance)
  - [🧩 5.3 RQ2: Ablation Study](#53-rq2-ablation-study)
  - [💡 5.4 RQ3: Strategy Analysis](#54-rq3-strategy-analysis)
  - [🌍 5.5 RQ4: Real-World Deployment](#55-rq4-real-world-deployment)
- [💬 6 Discussion](#6-discussion)
  - [6.1 Limitations and Threats to Validity](#61-limitations-and-threats-to-validity)
  - [🔥 6.2 What Remains Hard](#62-what-remains-hard)
- [🏁 7 Conclusion](#7-conclusion)
- [🔗 References](#references)
- [📑 Appendix](#appendix)
  - [📌 A Surveyed LLM-Based Penetration Testing Systems](#a-surveyed-llm-based-penetration-testing-systems)
  - [🔧 B Tool and Skill Layer: Supported Tools](#b-tool-and-skill-layer-supported-tools)
  - [📌 C Evidence Confidence Scoring](#c-evidence-confidence-scoring)
  - [📌 D Parameter Derivation and Validation](#d-parameter-derivation-and-validation)



**Authors:** Gelei Deng¹, Yi Liu¹, Yuekang Li², Ruozhao Yang³, Xiaofei Xie³, Jie Zhang⁴, Han Qiu⁵, Tianwei Zhang¹  
**Affiliations:**  
¹ Nanyang Technological University  
² University of New South Wales  
³ Singapore Management University  
⁴ CFAR, A*STAR, Singapore  
⁵ Tsinghua University  

---

## 🚀 Abstract

> [!NOTE]
> LLM-based agents show promise for automating penetration testing, yet the reported performance varies widely across systems and benchmarks. We analyze 28 LLM-based penetration testing systems and evaluate five representative implementations across three benchmarks of increasing complexity. Our analysis reveals two distinct failure modes: Type A failures stem from capability gaps (missing tools, inadequate prompts) that engineering readily addresses, while Type B failures persist regardless of tooling due to planning and state management limitations. We show that Type B failures share a root cause that is largely invariant to the underlying LLM: agents lack real-time task difficulty estimation. As a result, agents misallocate effort, over-commit to low-value branches, and exhaust context before completing attack chains.  
> 
> Based on this insight, we present **PENTESTGPT v2**, a penetration testing agent that couples strong tooling with difficulty-aware planning. A Tool and Skill Layer eliminates Type A failures through typed interfaces and retrieval-augmented knowledge. A Task Difficulty Assessment (TDA) mechanism addresses Type B failures by estimating tractability through four measurable dimensions (horizon estimation, evidence confidence, context load, and historical success) and uses these estimates to guide exploration-exploitation decisions within an Evidence-Guided Attack Tree Search (EGATS) framework. PENTESTGPT v2 achieves up to 91% task completion on CTF benchmarks with frontier models (39 to 49% relative improvement over baselines) and compromises 4 of 5 hosts on the GOAD Active Directory environment versus 2 by prior systems. These results show that difficulty-aware planning yields consistent end-to-end gains across models and addresses a limitation that model scaling alone does not eliminate.

---

## 1 Introduction

Penetration testing is essential for assessing organizational security, yet the demand for skilled practitioners far exceeds supply. The ISC2 Cybersecurity Workforce Study estimates a global shortfall of 4.7 million cybersecurity professionals [14]. This gap, together with the labor-intensive nature of manual testing, has driven interest in large language model (LLM)-based automation.

Recent systems report strong results on benchmarks such as Capture-the-Flag challenges and Hack The Box (HTB) environments [8, 17, 19, 30, 32], and emerging work has demonstrated real-world impact, including the discovery of exploitable vulnerabilities in production software [10, 13]. However, reported task completion rates range from single digits under naive prompting to 40-80% with more sophisticated architectures [9, 20], raising a central question: what drives these performance differences, and what limitations remain?

To answer this question, we conduct a systematic analysis of 28 LLM-based penetration testing systems and evaluate five representative solutions across three benchmarks of increasing complexity. Our analysis yields two findings. First, existing systems are optimized to address the limitations of specific LLMs. For example, context summarization and RAG-augmented tooling are designed to compensate for transient LLM constraints of limited context windows and poor tool knowledge. Benefits brought by these designs quickly diminish as models improve: performance gaps across solutions compress by over half when backbone models upgrade from GPT-4.0 to GPT-5. Second, failures partition into two categories: Type A failures (capability gaps) stem from missing tools and knowledge addressable through engineering, while Type B failures (complexity barriers) persist regardless of tooling due to planning and state management limitations. Existing systems predominantly target Type A failures, achieving strong results on simple tasks but failing on multi-step scenarios where Type B failures dominate. This indicates that the architectures of existing penetration testing systems are not designed to complement the improvements of LLMs. Their contributions erode as models advance, rather than compounding with improved capabilities.

We trace Type B failures to a missing capability: existing penetration testing agent designs cannot assess task difficulty in real time. This manifests in several ways: agents commit prematurely to unproductive branches because they cannot estimate whether a path requires 3 or 30 steps; they fail to transition from reconnaissance to exploitation because they lack metrics for evidence sufficiency; they experience context forgetting because they do not monitor context consumption. Human pentesters handle these problems through intuition built from experience. LLM agents lack equivalent mechanisms for difficulty-aware decision making. We validate this diagnosis through controlled evaluation: augmenting agents with difficulty assessment reduces the Type B failure rate from 58% to 27% while Type A rate remains unchanged, confirming that this enhancement addresses the root cause.

We present **PENTESTGPT v2**, designed around these two findings. To eliminate Type A failures, an extensible Tool and Skill Layer provides typed interfaces for 38 security tools and skill compositions that encode expert attack patterns. To address Type B failures, we introduce penetration testing Task Difficulty Assessment (TDA), a mechanism that estimates task tractability through four measurable dimensions: horizon estimation, evidence confidence, context load, and historical success rate. TDA is integrated into an Evidence-Guided Attack Tree Search algorithm that guides exploration-exploitation decisions and prunes branches when paths become intractable. With these mechanisms, PENTESTGPT v2 dynamically pivots between attack paths based on real-time difficulty signals. It abandons unproductive branches before they exhaust the context budget and commits to exploitation only when evidence confidence justifies the investment. A retrieval-augmented Memory Subsystem maintains structured state external to the LLM context, which prevents the context forgetting that derails extended attack campaigns.

We evaluate PENTESTGPT v2 across three benchmarks at different levels of realism, from CTF challenges to enterprise Active Directory environments. On XBOW [2] (104 web security tasks), PENTESTGPT v2 achieves 91% peak task completion (89% mean) with Claude Opus 4.5, a 49% relative improvement over the best baseline (61%). On the PentestGPT [8] Benchmark (13 HTB/VulnHub machines), PENTESTGPT v2 roots 12 of 13 machines, solving Hard-rated targets where baselines become stuck at initial steps. On GOAD (5-host Active Directory environment), PENTESTGPT v2 compromises 4 of 5 hosts compared to at most 2 for prior systems, with successful lateral movement and credential chaining across domain boundaries. Ablation studies confirm that each component contributes distinctly: the Tool Layer dominates on short-horizon tasks, while TDA-EGATS and Memory provide the gains on multi-step scenarios.

Despite these results, hard challenges remain. Our evaluation shows that novel exploitation requiring creative reasoning, adversarial environments with deceptive defenses, and extended multi-week campaigns exceed current LLM capabilities. These limitations suggest that fully autonomous penetration testing remains distant. We discuss these boundaries and propose evaluation methodologies that distinguish tractable from intractable challenges, so that the community can focus effort where architectural innovation is most likely to help.

In summary, we make the following contributions:
* **Systematic analysis of LLM agent failures (§3).** We analyze 28 systems and evaluate five implementations across three benchmarks, showing that existing architectures optimize for transient model constraints rather than persistent task challenges, and identifying two failure categories (Type A capability gaps and Type B complexity barriers) whose root causes require distinct solutions.
* **PENTESTGPT v2 (§4).** We present a system addressing both failure types: a Tool and Skill Layer for Type A failures, and Task Difficulty Assessment integrated into Evidence-Guided Attack Tree Search for Type B failures.
* **Evaluation across three benchmarks (§5).** PENTESTGPT v2 achieves 91% on CTF benchmarks (49% improvement), roots 12/13 machines on realistic targets, and compromises 4/5 hosts on enterprise AD, doubling baseline performance.
* **Design principles (§6).** We analyze remaining barriers (novel exploitation, adversarial robustness) and propose evaluation methodologies that separately assess Type A and Type B performance.
* **Open-source artifacts.** We release PENTESTGPT v2's implementation, tool interfaces, and evaluation scripts to support reproducibility [3].

---

## 📖 2 Background

### 2.1 Penetration Testing
Penetration testing identifies security vulnerabilities by simulating real-world attackers in blackbox/greybox scenarios. Standard methodologies decompose engagements into phases: reconnaissance (information gathering), enumeration (identifying services and entry points), exploitation (gaining access), and post-exploitation (privilege escalation and lateral movement) [26, 28]. This workflow follows a characteristic search pattern: breadth-first exploration over attack surfaces followed by depth-first exploitation along promising paths. Testers continuously decide which paths to pursue, when to abandon unproductive avenues, and how to integrate new discoveries. This interleaving of exploration and exploitation motivates our design (§4).

### 📌 2.2 Benchmarking Penetration Testing
Evaluating penetration testing capabilities presents methodological challenges. Real-world engagements involve social engineering, multi-target reconnaissance, and complex business logic that cannot be easily replicated, while commercial tests produce confidential reports tied to proprietary systems. Standardized benchmarks address these constraints: VulnHub [1] provides downloadable vulnerable VMs, HTB [11] offers curated machines spanning difficulty levels, and CTF competitions present challenges across web exploitation, cryptography, and binary exploitation.

Benchmarks differ from real-world targets in important ways. CTF challenges are designed to be solvable with a single attack path, whereas real systems may have no exploitable vulnerabilities or require broad discovery across a large attack surface. GOAD (Game of Active Directory) [25] is the closest approximation to realistic enterprise environments among current benchmarks, requiring chained attack techniques across multi-domain Windows networks, though it still abstracts away social engineering and time pressure. We interpret benchmark results as measuring specific technical capabilities rather than predicting overall real-world effectiveness.

### 📌 2.3 LLM-Based Agents
The standard approach for deploying LLMs as autonomous agents augments them with tool use [31] that invokes external functions such as shell commands or APIs, and agentic scaffolding that structures the interaction loop [15, 34]. Penetration testing is a natural application domain for such agents: it requires combining extensive domain knowledge with sequential decision-making, tool orchestration, and adaptive strategy.

Early work explores LLMs as copilots suggesting next steps to human operators [8, 29], whereas more recent systems position LLMs as autonomous agents executing reconnaissance, exploitation, and post-exploitation workflows [17, 30, 32]. These agents must handle heterogeneous tool outputs, maintain coherent strategies across many interaction steps, and decide when to pivot between attack paths. These challenges push against the limits of current LLM capabilities. Similar limitations appear in software engineering [15] and web navigation [34], suggesting that the barriers are not specific to penetration testing.

---

## 🔍 3 Understanding LLM Agent Failures

How far are we from achieving real-world penetration testing with LLM agents? To answer this question, we conduct an empirical analysis of existing LLM-based penetration testing systems. Our goals are to (1) understand what drives reported performance improvements, (2) identify failure modes through controlled evaluation, and (3) establish a framework for distinguishing tractable tasks from intractable challenges.

### 3.1 Taxonomy and Evaluation of LLM-based Penetration Testing

We survey LLM-based penetration testing systems, identifying 28 candidates published between 2023-2025. Inclusion criteria require systems to use LLMs as a core component and target penetration testing or CTF challenges; we exclude vulnerability detection without exploitation and commercial systems without published details. Of 28 candidates, 10 meet our criteria, with the list in Appendix A.

#### 3.1.1 Taxonomy
We summarize each system along four dimensions: architecture (multi-agent, human-in-the-loop), tool integration (function calls, MCP [5]), knowledge sources (Retrieval-Augmented Generation (RAG), fine-tuned), and planning (reactive, task trees, state machines, memory trees). Table 1 summarizes representative systems across three architectural families: human-in-the-loop copilots like PentestGPT [8], single-agent systems like AutoPT [32], and multi-agent systems like PentestAgent [30], VulnBot [17], and Cochise [12].

**Table 1: Taxonomy of LLM-based penetration testing systems**

| System | Year | Arch. | Tools | Know. | Planning |
| :--- | :--- | :--- | :--- | :--- | :--- |
| PentestGPT [8] | 2024 | Workflow | Shell | Prompt | Task tree |
| AutoPT [32] | 2024 | Single | Shell | Prompt | State mach. |
| RapidPen [23] | 2025 | Single | Shell | RAG | ReAct |
| PentestAgent [30] | 2024 | Multi | Func. | RAG | Phase |
| VulnBot [17] | 2025 | Multi | Shell | Prompt | Tri-phase |
| xOffense [19] | 2024 | Multi | Shell | Fine-tune | Multi-phase |
| TermiAgent [20] | 2024 | Multi | Shell | RAG | Mem. tree |
| Cochise [12] | 2025 | Multi | Shell | Prompt | Hierarchical |

#### 3.1.2 Evaluation Setup
We evaluate five representative open-source systems: PentestGPT [8] (copilot), AutoPT [32] (single-agent), PentestAgent [30] (multi-agent with RAG), VulnBot [17] (multi-agent tri-phase), and Cochise [12] (Active Directory (AD)-focused). Benchmarks span three realism levels: XBOW [2] (104 web challenges: SQL injection (SQLi), cross-site scripting (XSS), auth bypass), PentestGPT Benchmark [8] (13 machines from HTB and VulnHub requiring end-to-end penetration testing), and GOAD [25] (5-host multi-domain AD requiring chained attacks).

For each system-benchmark pair, we evaluate with GPT-4.0, GPT-5, Gemini-3-Flash, and Claude Sonnet 4 to assess model vs. architecture contributions. We include GPT-4.0 (the model generation most existing systems were optimized for) alongside newer models to examine how architectural advantages evolve as underlying capabilities improve. §5 evaluates PENTESTGPT v2 with a different model set (GPT-5.2, Opus 4.5, Gemini 3 Pro) selected specifically for thinking mode support, enabling controlled comparison of extended reasoning. We set temperature to zero and report best-of-three trials following prior work [8,9], since penetration testing is inherently non-deterministic.

### 🧠 3.2 Findings

Table 2 summarizes task completion rates across all system-model-benchmark combinations. We provide in-depth experimental results analysis below.

#### 3.2.1 Agent Architecture Convergence
Despite two years of agent design innovation, performance differences between systems compress with state-of-the-art models. On XBOW with GPT-4.0, completion rates range from 27% to 39% across five systems, a 44% relative spread that reflects meaningful architectural distinctions. With GPT-5, this gap narrows to 22.5% (40-49%); similar convergence appears on the PentestGPT Benchmark, where the spread shrinks from 2 points with GPT-4.0 (4-6 machines) to 1 point with GPT-5 (7-8 machines).

This convergence points to a limitation in how existing agents were designed: they address transient model constraints rather than persistent task challenges. Consider the techniques these systems employ. PentestGPT's summarization module compensates for limited context windows, a constraint that largely dissolves as models gain native million-token support. Multi-agent architectures with role separation (e.g., reconnaissance agent, exploitation agent) work around weak instruction-following, yet frontier models handle complex multi-step prompts without explicit decomposition. RAG pipelines for tool documentation address poor parametric knowledge of security tools, yet recent models have much stronger baseline knowledge of common exploitation techniques and penetration testing tools. These "innovations" are workarounds for 2023-era model limitations, not solutions to persistent penetration testing challenges.

What distinguishes transient from persistent challenges? Transient challenges diminish as models improve: context capacity, instruction adherence, tool-use reliability, and domain knowledge all scale with model capability. Persistent challenges, by contrast, remain regardless of raw model power: long-horizon planning across 10+ exploitation steps, principled exploration-exploitation decisions, maintaining state external to degrading context, and real-time assessment of task difficulty. These challenges arise from the structure of penetration testing tasks, not from model limitations, and thus require architectural solutions that complement rather than compensate for underlying models.

The Cochise case shows this distinction from a different angle. Cochise's AD-specific attack primitives (Kerberoasting, NTLM relay, BloodHound integration) are capability additions that models cannot replicate through improved reasoning alone. However, this specialization comes at the cost of generality: Cochise underperforms on XBOW and the PentestGPT Benchmark (34% and 4/13 with GPT-4.0) compared to general-purpose systems like VulnBot (39% and 6/13), while leading on GOAD by leveraging domain-specific knowledge unavailable to other systems. Neither approach, compensating for model limitations nor adding domain-specific capabilities, addresses the persistent challenge of navigating complex attack graphs.

> [!IMPORTANT]
> **Finding 1:** Existing penetration testing agents address transient model limitations rather than persistent task challenges. As models evolve, benefits brought by architectural distinctions compress. Durable agent value should address challenges that persist across model evolution.

#### ❌ 3.2.2 Two Distinct Failure Categories
To understand why systems fail rather than merely how often, we analyze 200 execution traces from unsuccessful attempts (40 per system), sampling proportionally across benchmarks. Two researchers independently coded failure modes using open coding, then reconciled disagreements through discussion. Our analysis shows that failures partition into two distinct categories, classified based on observable trace characteristics before any intervention.

*   **Type A failures (capability gaps)** are identified when the trace shows the agent correctly reasons about the attack vector but fails at execution: the agent articulates the correct approach but then issues malformed commands or uses incorrect tool syntax. For instance, an agent may correctly identify a SQL injection vulnerability (e.g., "I will use SQL injection to extract data") but fail because it lacks sqlmap or the correct documentation. To validate this classification, we augment PentestGPT with missing tool documentation and usage instructions; XBOW completion improves from 27% to 38%, a 41% relative improvement that confirms Type A failures respond to capability engineering as predicted.
*   **Type B failures (complexity barriers)** are identified when the trace shows the agent possesses adequate tools and knowledge (evidenced by successful tool invocations earlier in the session) but fails to navigate the task space effectively. We identify three recurring patterns from trace analysis:
    *   **Context forgetting** occurs when credentials discovered during reconnaissance are lost by the time exploitation begins, forcing redundant discovery or causing authentication failures.
    *   **Premature commitment** occurs when agents dive deep into a single attack path without adequate reconnaissance, missing easier alternatives.
    *   **Exploration-exploitation imbalance** is the inverse: exhaustive reconnaissance that never transitions to exploitation, accumulating information without acting on it.

These issues cascade into **chain errors**: agents complete individual attack stages successfully but fail to integrate them into coherent attack chains, losing state between phases.

The distribution of failure types varies systematically with task complexity. On XBOW, where tasks typically require 1-3 steps, Type A failures dominate (68% of failures resolve with improved tooling). On GOAD, where successful attacks require chaining 5-10 steps across multiple hosts, Type B failures dominate (79% of failures persist regardless of tooling improvements). Figure 1 visualizes this relationship: Type A failures concentrate in short-horizon tasks while Type B failures dominate in task depth beyond 5 steps. Table 3 summarizes the failure mode distribution.

**Figure 1: Failure Distribution by Task Depth**

```mermaid
pie title Failure Type Distribution at Complexity Threshold (Approx 5 Steps)
    "Type A: Capability Gaps" : 42
    "Type B: Complexity Barriers" : 58

```

*(Figure 1 shows that at 1-2 steps, Type A gaps dominate around 72%, smoothly dropping as depth increases. At 9+ steps, Type B errors account for over 85% of failures, with the complexity threshold intersection at approximately 5 steps.)*

**Table 2: Task completion rates across systems, models, and benchmarks.**
XBOW: task completion (%); PentestGPT Benchmark: machines rooted (/13); GOAD: hosts compromised (/5).

| System | XBOW (GPT-4.0) | XBOW (GPT-5) | XBOW (Gem.) | XBOW (Claude) | PentestGPT-Ben (GPT-4.0) | PentestGPT-Ben (GPT-5) | PentestGPT-Ben (Gem.) | PentestGPT-Ben (Claude) | GOAD (GPT-4.0) | GOAD (GPT-5) | GOAD (Gem.) | GOAD (Claude) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| PentestGPT | 27 | 42 | 36 | 39 | 5 | 7 | 6 | 6 | 0 | 1 | 1 | 1 |
| AutoPT | 28 | 40 | 35 | 37 | 4 | 7 | 6 | 6 | 0 | 1 | 0 | 0 |
| PentestAgent | 34 | 49 | 42 | 46 | 6 | 7 | 6 | 6 | 0 | 1 | 0 | 1 |
| VulnBot | 39 | 45 | 44 | 46 | 6 | 8 | 6 | 7 | 0 | 1 | 0 | 1 |
| Cochise | 34 | 43 | 39 | 39 | 4 | 4 | 4 | 4 | 1 | 2 | 2 | 2 |

**Table 3: Failure mode analysis (200 traces).** Type A failures resolve with tooling; Type B persist regardless.

| Failure Category | Freq. (%) | Tooling? |
| :--- | :--- | :--- |
| **Type A: Capability Gaps (42% total)** | | |
| Missing tool/Incorrect syntax | 26 | ✓ |
| Output parsing / Knowledge gap | 16 | ✓ |
| **Type B: Complexity Barriers (58% total)** | | |
| Context forgetting | 18 | ✗ |
| Premature commitment | 16 | ✗ |
| Exploration-exploitation imbalance | 12 | ✗ |
| Multi-step chain failures | 12 | ✗ |

> [!IMPORTANT]
> **Finding 2:** Failures partition into (a) Type A: capability gaps, i.e., missing tools and knowledge addressable through engineering, and (b) Type B: complexity barriers, i.e., search strategy and state management failures that persist despite adequate capabilities. These two categories require different solutions.

### 🏗️ 3.3 Analysis and Design Implications

We now present further analysis and design implications.

#### 3.3.1 Root Cause: Missing Difficulty Assessment
Type B failures share a common root cause: agents cannot distinguish tractable from intractable tasks in real time. Premature commitment occurs because agents cannot estimate whether a path requires 3 or 30 steps; without this estimate, they persist on unproductive branches indefinitely. Exploration-exploitation imbalance occurs because agents lack metrics for when reconnaissance is sufficient; they cannot determine whether gathered evidence justifies transitioning to exploitation. Chain failures occur partly because agents cannot assess whether their accumulated context remains adequate for the current task; critical information may have been lost or degraded without the agent's awareness. For example, context forgetting occurs because agents lack difficulty metrics: without tracking context load, they cannot predict when accumulated history will overwhelm the model's effective memory, leading to silent degradation of reasoning quality.

What would difficulty assessment require in practice? We identify four measurable dimensions: horizon estimation (remaining steps to goal), evidence confidence (certainty about current state), context load (fraction of context window consumed), and historical success (past performance on similar branches). These dimensions are measurable during execution, unlike abstract "difficulty" which is only knowable post-hoc. An agent that tracks these signals can decide when to persist, when to pivot, and when to prune.

Current systems uniformly lack this capability. PentestGPT's Penetration Testing Tree (PTT) tracks attack structure but provides no difficulty metrics to guide search. AutoPT's Pentesting State Machine (PSM) enforces phase transitions but does not assess path complexity. TermiAgent's memory tree improves context management but does not inform exploration-exploitation decisions. None of these systems can answer the question that matters most: is this path worth pursuing?

#### 🏗️ 3.3.2 Design Implications
Our analysis points to a two-part strategy for advancing LLM-based penetration testing. Eliminating Type A failures requires comprehensive tool interfaces with typed schemas, RAG systems for exploit documentation and Common Vulnerabilities and Exposures (CVE) databases, and standardized execution environments. This is tedious engineering work, but it produces predictable returns: each tool added directly enables new attack capabilities.

Addressing Type B failures requires a different approach: real-time difficulty estimation, principled exploration-exploitation decisions guided by the estimates, active pruning of intractable branches to prevent search collapse, and state maintenance external to conversation context to prevent information loss. These requirements suggest tree-based search algorithms to maintain state explicitly rather than relying on LLM's context window.

Neither approach alone is sufficient. Capability engineering yields strong short-horizon performance but fails on complex tasks where navigation becomes the bottleneck. Planning innovation without adequate tooling produces agents that reason well but cannot execute. Effective systems must address both failure categories simultaneously, and in particular, agents need the ability to assess task difficulty in real time to avoid exploration-exploitation imbalance and chain failures.

---

## 🏗️ 4 Design of PENTESTGPT v2

### 4.1 Overview
We present PENTESTGPT v2, designed around the analysis in §3.3 to address both failure categories through dedicated architectural components. Figure 2 provides its architectural overview. PENTESTGPT v2 is a single-agent system that communicates with the environment consistently, operating over different components to complete penetration testing. It consists of the following modules: (1) A Tool and Skill Layer that eliminates Type A failures through structured tool interfaces and knowledge augmentation (§4.2). (2) A Task Difficulty Assessment (TDA) mechanism that estimates tractability in real time (§4.3), integrated into an Evidence-Guided Attack Tree Search (EGATS) algorithm that replaces the traditional PTT structure for exploration-exploitation decisions (§4.4). (3) A Memory Subsystem that maintains state across attack phases to prevent context forgetting (§4.5).

**Figure 2: PENTESTGPT v2 Architecture**

```mermaid
flowchart LR
    subgraph Input
        A[Attack Target as tree structure]
    end
    subgraph Excalibur_Agent [Excalibur Agent]
        subgraph Planner [TDA-EGATS Planner (§4.3-4.4)]
            B[Task Difficulty Assessment: H Horizon, E Evidence, C Context, S Success]
            C[EGATS Operations]
            D[Attack Tree EGATS]
            E[TDI-Guided Mode: BFS, LLM, DFS]
            B --> C
            C --> D
            E --> D
        end
        subgraph Memory [Memory Subsystem (§4.5)]
            F[State]
            G[Context]
            H[Branch Summaries]
        end
        subgraph Tools [Tool & Skill Layer (§4.2)]
            I[Attack Goal]
            J[Tool Interfaces]
            K[Skill Composition]
            I --> J
            I --> K
        end
        D <-->|Update| Memory
        D -->|2| I
    end
    subgraph Output
        L[Execution Results]
        M[Attack Instruction]
        N[Results: Attack Path Completed]
        M -->|Execution| L
    end
    
    A -->|1| Planner
    Tools -->|3| M
    L -.->|4| Planner
    M --> N

```

*(Figure 2 details the TDA-EGATS Planner addressing Type B failures via Upper Confidence Bound (UCB) selection, TDI-guided switching, and evidence-based pruning. The Tool & Skill Layer handles Type A gaps. The Memory Subsystem enables context injection based on tree position.)*

Given a target, PENTESTGPT v2 initializes an attack tree with the target as the root node. At each step, the EGATS planner consults the TDA module to select the current attack goal and updates the memory subsystem to preserve context. The selected goal is translated into concrete actions via the Tool and Skill Layer, and the resulting commands are executed in the test environment. Execution results are parsed and incorporated back into the attack tree and memory state, feeding into subsequent planning iterations until the penetration testing process terminates. Below we detail each component.

### 🔧 4.2 Tool and Skill Layer
Type A failures arise not from fundamental capability limitations, but from inconsistent tool usage: LLMs invoke security tools with incorrect parameters, misparse outputs, or lack domain knowledge about tool capabilities. Rather than proposing novel techniques, the Tool and Skill Layer represents careful engineering to ensure LLM agents interact with security tools consistently and reliably. We build on established concepts of Agent Skills [4] from Anthropic (typed interfaces, skill composition, and retrieval-augmented generation), adapting them to penetration testing where tool reliability directly determines attack success.

**Typed Tool Interfaces.** Each security tool is exposed through a typed interface specifying input schema (parameters with types, defaults, and validation rules), output schema (structured representation parsed from command output), and pre/postconditions (required state before invocation and expected effects after completion). The LLM receives explicit documentation rather than relying on parametric knowledge. Input validation catches errors before execution, and structured outputs eliminate parsing ambiguity. We implement interfaces for 38 tools across six categories: reconnaissance, web exploitation, network exploitation, credential attacks, Active Directory attacks, and privilege escalation. Appendix B provides the complete tool list we integrate.

**Skill Composition.** Beyond individual tools, skills compose multiple tool invocations into higher-level attack capabilities that encode expert knowledge about common attack patterns. Skills provide fallback logic so that when a preferred tool fails, the system can try alternatives automatically. They also aggregate results from multiple tools into coherent findings and encode multi-step attack patterns that reflect how human testers chain operations.

**Knowledge Augmentation.** The layer integrates a RAG system containing tool documentation, an exploit database (CVE descriptions indexed by service version), and attack playbooks (step-by-step procedures for common patterns such as Kerberoasting, AS-REP roasting, and pass-the-hash). The knowledge base contains only generic attack techniques from public security resources (MITRE ATT&CK, OWASP, tool documentation); it excludes CTF writeups, HTB walkthroughs, or benchmark-specific solutions to prevent data leakage in evaluation. When the agent encounters an unfamiliar service or vulnerability class, relevant documentation is retrieved and injected into context automatically.

These three mechanisms together provide a unified, reliable interface between LLM agents and security tools. None of these techniques is novel in isolation; their contribution lies in the combination, which minimizes tool invocation errors that otherwise cascade into attack failures. Our ablation study (§5.3) shows that this engineering effort yields substantial gains on capability-limited tasks: the Tool Layer alone improves XBOW completion by 14% (from 54% to 68%), allowing agents to focus their reasoning on the harder problems of planning and strategy.

### 📏 4.3 Task Difficulty Assessment (TDA)
Our analysis in §3.3 identifies the inability to assess task difficulty as the root cause of Type B failures. Premature commitment occurs because agents cannot estimate whether a path requires 3 or 30 steps. Exploration-exploitation imbalance occurs because agents have no metric for when reconnaissance is sufficient. Chain failures occur because agents cannot judge whether accumulated context is adequate for the current task.

Human penetration testers face the same problem: they do not know task difficulty a priori. Instead, they estimate difficulty from signals that accumulate during execution, such as the number of failed attempts on a path, the quality of evidence gathered so far, and intuitions about remaining work. An experienced tester who has tried five exploits without success knows to try a different approach; one who has confirmed a vulnerable service version knows to commit to exploitation. TDA operationalizes this reasoning for LLM agents through four measurable dimensions, with context window consumption added as a signal unique to language models.

#### 4.3.1 TDA Dimensions
TDA computes difficulty along four dimensions grounded in quantities measurable during execution.

*   **Horizon Estimation (H).** We estimate the number of remaining steps to reach the goal from the current position, normalized across active branches. A pilot study on 50 traces from an independent GOAD deployment (using GPT-4.0, separate from evaluation) shows that while absolute estimates have poor calibration (MAE of 4.2 steps), rank correlation is strong (Spearman's $\rho=0.71$, $p<0.001$). The TDI formula therefore uses $\hat{H}$, the normalized horizon estimate (min-max scaled across active branches), converting absolute estimates into relative rankings where LLM judgment is reliable.
*   **Historical Success Rate (S).** The Laplace-smoothed success rate on the current branch captures learning from failed attempts. Low values indicate repeated failures, suggesting that the current path is likely intractable. This dimension directly addresses premature commitment: agents learn to abandon unproductive paths rather than persisting indefinitely.
*   **Context Load (C).** The fraction of context window consumed, directly measurable from token counts. LLM performance degrades as context fills: retrieval accuracy drops, earlier information is forgotten, and reasoning quality declines [18]. We define an ideal working window of 40% of the model's context capacity, based on a controlled study showing consistent accuracy degradation beyond this point ($94\% \rightarrow 78\%$ at 60% load, 61% at 80%; see Appendix D.6). Beyond this threshold, context pruning becomes necessary to preserve reasoning quality. This dimension addresses context forgetting: by tracking context load, the system detects when accumulated history threatens to overwhelm the model's effective memory.
*   **Evidence Confidence (E).** The mean confidence score across the path from root to current node, computed from evidence categories at each node. We assign scores based on evidence type: verified exploits and valid credentials receive 1.0, confirmed vulnerabilities with available exploits receive 0.8, plausible hypotheses (version-matched vulnerabilities, misconfigurations) receive 0.5, and speculative hypotheses receive 0.3. Tool outputs are parsed to determine evidence type: successful authentication or shell access indicates verified evidence, vulnerability scanner confirmations with CVE matches indicate confirmed vulnerabilities, and service version matches against exploit databases indicate plausible hypotheses. Appendix C details the complete scoring rubric. This dimension addresses exploration-exploitation imbalance: high confidence signals readiness to exploit, while low confidence signals the need for more reconnaissance.

#### 🔢 4.3.2 Task Difficulty Index
TDA combines the above 4 dimensions into a Task Difficulty Index (TDI):

$$
TDI = w_H \hat{H} + w_E (1-E) + w_C C + w_S (1-S) \quad (1)
$$

where $\hat{H}$ is the normalized horizon estimate and all weights sum to 1. Higher TDI indicates greater difficulty. We set $w_H=w_E=0.3$ and $w_C=w_S=0.2$ based on grid search over a validation set of 30 execution traces from HTB machines not included in the PentestGPT benchmark (retired machines from 2022-2023, predating our evaluation set). We test 256 configurations with each weight in {0.1, 0.2, 0.3, 0.4} constrained to sum to 1.0; task completion varies within ±3% across configurations where all weights remain in [0.1, 0.4], indicating that the approach is not sensitive to precise weight selection.

TDI guides three operational decisions. **Mode selection:** high TDI ($>\theta_{explore}=0.6$) triggers reconnaissance (BFS) to gather more information before committing; low TDI ($<\theta_{exploit}=0.3$) triggers exploitation (DFS). For intermediate values ($0.3 \le TDI \le 0.6$), the system invokes LLMDECIDE: the LLM receives the current node state, TDI value, and individual dimension scores (H, S, C, E), then selects between reconnaissance and exploitation with a brief justification. This design acknowledges that intermediate difficulty may warrant either approach depending on context the TDI formula cannot fully capture. For instance, a moderately difficult path with high evidence confidence may warrant exploitation, while one with low confidence benefits from further reconnaissance. **Branch prioritization:** TDI ranks paths beyond promise scores alone, since two branches with similar promise may differ substantially in tractability based on horizon and success history. **Pruning:** branches with persistently high TDI ($>\theta_{prune}=0.8$) after $k_{min}=3$ attempts are pruned to prevent the search from collapsing into unproductive regions. These thresholds are derived through grid search on the same validation set used for TDI weights. Appendix D presents sensitivity analysis showing robustness across threshold ranges.

**Table 4: Search strategy comparison.** EGATS is the only approach that combines external structure, evidence-based pruning, and TDA-guided mode selection.

| Approach | Structure | Pruning | Difficulty | TDA |
| :--- | :--- | :--- | :--- | :--- |
| ReAct | None | – | – | – |
| PTT [8] | Tree (text) | Manual | – | – |
| PSM [32] | Finite state machine | – | – | – |
| PMT [20] | Tree | – | – | – |
| **EGATS** | **Tree (ext.)** | **Evidence** | **✓** | **✓** |

### 📌 4.4 Evidence-Guided Attack Tree Search (EGATS)
EGATS integrates TDA into a tree-based search framework, adapting Monte Carlo Tree Search (MCTS) [6, 16] to penetration testing. EGATS differs from standard MCTS in three ways: it explicitly separates reconnaissance (BFS) and exploitation (TDI-guided) phases, it replaces simulation-based value estimates with TDA-based difficulty assessment, and it prunes intractable branches based on evidence.

#### 4.4.1 Attack Tree Structure
EGATS maintains an Attack Tree $\mathcal{T}=(V,E,\phi,\psi,\delta)$ where $V$ contains nodes representing attack states, $E$ contains edges representing actions, $\phi:V\rightarrow[0,1]$ assigns promise scores, $\psi:V\rightarrow S$ maps nodes to state snapshots, and $\delta:V\rightarrow[0,1]$ assigns TDI scores. Nodes are categorized as observation (discovered facts), hypothesis (untested attack possibilities), or action (executed steps with outcomes).

The promise score $\phi(n)$ estimates the likelihood that node $n$ leads to successful exploitation. For hypothesis nodes, promise is initialized via LLM assessment of vulnerability severity, exploit availability, and prerequisite satisfaction; the model estimates success probability given current evidence. For action nodes, promise is updated based on execution outcomes: successful actions propagate increased promise to ancestor nodes, while failures decrease promise along the path. After action $a$ with outcome $o \in \{success, partial, failure\}$, we update $\phi(n)\leftarrow\alpha\cdot\phi(n)+(1-\alpha)\cdot r(o)$ where $r(success) = 1.0$, $r(partial) = 0.5$, $r(failure) = 0.1$, and $\alpha=0.7$ controls the learning rate. Through this backpropagation, branches with consistent successes accumulate high promise while repeatedly failing branches see diminishing scores.

Unlike PentestGPT's text-based PTT, EGATS maintains structure externally via algorithmic operations, which prevents corruption and enables systematic search guidance. Table 4 compares EGATS with related approaches.

#### ⚙️ 4.4.2 The EGATS Algorithm
Algorithm 1 presents the TDA-guided search procedure. SELECTNODE uses UCB to balance exploitation and exploration:

$$
UCB(n) = \phi(n) + c \sqrt{\frac{\ln N}{N_n}} - \lambda \delta(n) \quad (2)
$$

where $\phi(n)$ is the promise score, $N$ is total actions, $N_n$ is actions on node $n$'s subtree, $c=\sqrt{2}$ is the exploration constant, and the $-\lambda \delta(n)$ term penalizes high-difficulty nodes ($\lambda=0.5$, validated via grid search; see Appendix D).

After selection, EGATS computes TDI and switches between BFS (reconnaissance) and DFS (exploitation) based on the thresholds described above. Evidence backpropagates after each action, updating promise scores and TDI along affected paths. When exploitation succeeds, pivot spawning is triggered: the compromised host becomes a new subtree root, and discovered credentials propagate to relevant hypothesis nodes elsewhere in the tree.

Pruning removes branches when TDI exceeds 0.8 after three attempts, which prevents infinite loops on intractable paths. To avoid premature pruning, a credential propagation mechanism re-evaluates pruned branches when new credentials are discovered that may satisfy their preconditions.

```text
**Algorithm 1: TDA-Guided Attack Tree Search**
**Require:** Target $T$, budget $B$
**Ensure:** Attack tree $\mathcal{T}$, compromised hosts $C$
1: INIT_TREE($\mathcal{T}$)
2: while $B > 0$ and not GOAL_REACHED do
3:     $n \leftarrow \text{SELECT\_NODE}(\mathcal{T})$  // UCB selection
4:     $TDI_n \leftarrow \text{COMPUTE\_TDI}(n)$
5:     if $TDI_n > \theta_{explore}$ then
6:         EXECUTE_RECON($n$); EXPAND_TREE($\mathcal{T}, n$)
7:     else if $TDI_n < \theta_{exploit}$ then
8:         result $\leftarrow$ EXECUTE_EXPLOIT($n$)
9:         BACKPROPAGATE_EVIDENCE($\mathcal{T}, n, result$)
10:        if result.success then
11:            SPAWN_PIVOT($\mathcal{T}, result.host$)
12:        end if
13:    else
14:        LLM_DECIDE($n, TDI_n$)
15:    end if
16:    if $\delta(n) > \theta_{prune}$ and $N_n > k_{min}$ then
17:        PRUNE_BRANCH($\mathcal{T}, n$)
18:    end if
19:    $B \leftarrow B - 1$
20: end while

```

### 💾 4.5 Memory Subsystem
Long-context forgetting is a primary cause of Type B failures (§3.2). The Memory Subsystem addresses this with a hybrid architecture that separates persistent state from conversational context, and integrates with TDA via the context load dimension.

A State Store maintains a structured database of discovered facts independent of conversation context. The store tracks five entity types: hosts (IP addresses, hostnames, OS fingerprints), services (ports, versions, configurations), credentials (usernames, passwords, hashes, tickets), sessions (active shells, tunnels, pivots), and vulnerabilities (CVE identifiers, exploitation status, prerequisites). Each entry is timestamped and linked to its discovery node in the attack tree, which enables provenance tracking and ensures facts persist regardless of conversation length. The State Store also supports accurate TDA context load computation by providing ground truth about what information the agent "knows" versus what must be re-derived from context.

Selective context injection replaces full history maintenance. When operating on node $n$, context is assembled from: path context (the sequence of actions from root to $n$), a node state snapshot (complete state at $n$ including all relevant entity relationships), target-relevant facts (entries from State Store pertaining to $n$'s target host or service), and sibling branch summaries (compressed representations of parallel exploration paths). As context load approaches the ideal working window threshold (40%), less-relevant context is progressively compressed using LLM-generated summaries. Beyond 70%, aggressive pruning removes older path segments while preserving findings to prevent performance degradation.

Branch summaries compress detailed execution history when switching branches. Each summary preserves the current status (active, pruned, completed), findings (discovered credentials, confirmed vulnerabilities), TDI at time of suspension, and recommended next actions. TDI is stored with each summary to inform revisit decisions: when new credentials are discovered elsewhere in the tree, branches with matching preconditions and previously high TDI are re-evaluated for potential reactivation.

---

## 📊 5 Evaluation

We assess the performance of PENTESTGPT v2 through four research questions:
*   **RQ1:** Does PENTESTGPT v2 outperform existing systems across different penetration testing scenarios?
*   **RQ2:** What is the contribution of the each designed architectural component?
*   **RQ3:** How does TDA-EGATS change the agent's attack strategy compared to prior approaches?
*   **RQ4:** Can PENTESTGPT v2 be practically deployed for real-world penetration testing?

### 5.1 Experimental Setup
PENTESTGPT v2 is implemented in Python (~8,500 lines), with the Tool Layer, TDA-EGATS Planner, and Memory Subsystem as separate modules. The implementation is open-sourced [3]. Following the evaluation methodology in Section 3.1, we evaluate PENTESTGPT v2 on three benchmarks of increasing complexity. XBOW [2] comprises 104 CTF-style web security challenges covering SQL injection, XSS, authentication bypass, and file inclusion; these short-horizon tasks isolate Type A failures where tool usage determines success. The PentestGPT Benchmark [8] consists of 13 machines from HTB and VulnHub, requiring end-to-end penetration testing from reconnaissance through privilege escalation to root access. Difficulty ranges from Easy to Hard, with 9-22 subtasks per machine, representing realistic scenarios that demand multi-step attack chains. GOAD [25] provides a 5-host multi-domain Active Directory environment requiring credential harvesting, Kerberoasting, lateral movement, and domain escalation, complex enterprise scenarios dominated by Type B failures.

We compare against four baseline systems: PentestGPT v1.0 [8], AutoPT [32], PentestAgent [30], and VulnBot [17]. We exclude Cochise [12] from this comparison because its AD-specialized architecture creates an uneven evaluation as shown in Section 3.2. Baseline systems use their original tool invocation mechanisms to reflect realistic deployment comparisons; reported improvements therefore reflect both tool integration and architectural contributions. To isolate architectural contributions from model capabilities, all systems are evaluated with three frontier models: GPT-5.2, Claude-Opus-4.5, and Gemini-3.0-Pro. We select these models for two reasons: (1) they represent state-of-the-art capabilities at the time of evaluation, and (2) all three support toggling between standard and thinking modes, enabling controlled comparison of extended reasoning effects. We report task completion rate, subtask progress, and exploration metrics including branch diversity, backtrack frequency, and time-to-pivot. We report mean performance across trials with standard deviation where variance is meaningful; for discrete outcomes (machines rooted, hosts compromised), we report best-of-three following prior work [8,9] since standard deviation on small integers provides limited insight. For XBOW's continuous completion rates, we report both headline best-of-three results and trial statistics ($\mu$: mean, $\sigma$: standard deviation across the three trials) to characterize variance. In total, we conduct 5 systems × 118 evaluation units × 6 model configurations × 3 trials, yielding 10,620 evaluation runs at an estimated cost of $2,760 USD in API tokens (Table 8 reports PENTESTGPT v2-specific costs).

### 5.2 RQ1: Overall Performance
Table 5 shows the performance comparison across all system-model-benchmark combinations, with consistent patterns that align with our Type A/B failure framework.

**Table 5: Performance comparison across systems, models, and benchmarks.**
Each model column is split into non-thinking (-) and thinking (T) modes.
XBOW: task completion (%); PentestGPT Benchmark: machines rooted (/13); GOAD: hosts compromised (/5). Best results per column in bold. All results report mean across 3 trials; variance $\pm2-3\%$ on XBOW, $\pm1$ machine on PentestGPT-Ben.

| System | XBOW GPT-5.2 (-) | XBOW GPT-5.2 (T) | XBOW Opus 4.5 (-) | XBOW Opus 4.5 (T) | XBOW Gemini 3 (-) | XBOW Gemini 3 (T) | Pentest-Ben GPT-5.2 (-) | Pentest-Ben GPT-5.2 (T) | Pentest-Ben Opus 4.5 (-) | Pentest-Ben Opus 4.5 (T) | Pentest-Ben Gemini 3 (-) | Pentest-Ben Gemini 3 (T) | GOAD GPT-5.2 (-) | GOAD GPT-5.2 (T) | GOAD Opus 4.5 (-) | GOAD Opus 4.5 (T) | GOAD Gemini 3 (-) | GOAD Gemini 3 (T) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| PentestGPT | 45 | 53 | 47 | 54 | 41 | 48 | 7 | 8 | 6 | 7 | 6 | 7 | 1 | 1 | 1 | 2 | 1 | 1 |
| AutoPT | 43 | 50 | 44 | 51 | 38 | 45 | 6 | 7 | 7 | 8 | 5 | 6 | 1 | 1 | 0 | 1 | 1 | 1 |
| PentestAgent | 52 | 61 | 54 | 60 | 46 | 54 | 8 | 9 | 7 | 9 | 7 | 8 | 1 | 2 | 2 | 2 | 1 | 1 |
| VulnBot | 48 | 56 | 50 | 58 | 43 | 51 | 8 | 9 | 8 | 9 | 6 | 8 | 2 | 2 | 1 | 2 | 1 | 2 |
| **PENTESTGPT v2** | **76** | **85** | **81** | **91** | **76** | **79** | **11** | **12** | **10** | **12** | **10** | **11** | **3** | **4** | **3** | **4** | **3** | **3** |

On XBOW, PENTESTGPT v2 achieves 91% task completion (best-of-3; $\mu=89\%$, $\sigma=2.1\%$) with Opus 4.5 thinking mode, a 49% relative improvement over the best baseline (PentestAgent at 61%, $\mu=59\%$, $\sigma=1.8\%$). With GPT-5.2 thinking, PENTESTGPT v2 achieves 85% ($\mu=83\%$, $\sigma=2.4\%$) compared to 61% for PentestAgent. Even comparing means, the gap (89% vs. 59%) exceeds 15 standard deviations, confirming robust architectural differences: the Tool Layer eliminates Type A failures while TDA-EGATS prevents trial-and-error loops that consume baseline attempts. Thinking mode provides 6-10 point improvements across all systems and configurations but does not close the architectural gap.

The PentestGPT benchmark shows larger architectural differences. PENTESTGPT v2 roots 12 of 13 machines with both GPT-5.2 and Opus 4.5 thinking (consistent across all three trials), compared to 9 for the best baseline (VulnBot), a 33% relative improvement. PENTESTGPT v2 solves both Hard-rated machines (Joker and Falafel) where baseline systems became "stuck at initial steps," and also completes machines that require non-obvious attack chains. The improvement concentrates in machines requiring non-linear attack paths: while baseline PTT structures lead to premature commitment on initial hypotheses, TDA-EGATS enables strategic backtracking when evidence confidence drops, allowing the agent to discover alternative attack vectors. Thinking mode amplifies architectural differences: PENTESTGPT v2 gains 1-2 machines from thinking, achieving near-complete coverage, while baselines gain only 1 machine each but plateau at 9.

GOAD shows the largest improvement. PENTESTGPT v2 compromises 4 of 5 hosts with GPT-5.2 and Opus 4.5 thinking (4 hosts in all three trials; the same four hosts each time) versus at most 2 for baselines—doubling the compromise rate (80% vs. 40%). This pattern holds consistently across all three models and both reasoning modes (even Gemini 3 achieves 3 hosts vs. 1-2 for baselines), indicating a robust architectural effect. Baselines achieve initial foothold but fail to progress through lateral movement; PENTESTGPT v2 executes coherent multi-host attack chains using the Memory Subsystem for credential persistence and TDA for exploration guidance.

### 🧩 5.3 RQ2: Ablation Study
To isolate each component's contribution, we evaluate system variants with individual components disabled. Table 6 presents results using GPT-5.2 thinking mode; the base configuration uses raw shell access with reactive prompting and sliding-window context management. Figure 3 visualizes component contributions across all model configurations.

**Table 6: Ablation study results (GPT-5.2 thinking).**
Base: raw shell access with reactive prompting. Each row adds a component cumulatively.

| Configuration | XBOW | Pentest-Ben | GOAD |
| :--- | :--- | :--- | :--- |
| Base | 54 | 8 | 2 |
| + Tool Layer | 68 | 9 | 2 |
| + TDA-EGATS | 77 | 11 | 3 |
| **+ Memory (Full)** | **85** | **12** | **4** |

**Figure 3: Ablation study across benchmarks (GPT-5.2 thinking).** Performance is normalized to percentage scale.

```mermaid
pie title Component Contributions (Relative to Full 100%)
    "Base Capability" : 54
    "Tool Layer (+14%)" : 14
    "TDA-EGATS (+9%)" : 9
    "Memory (+8%)" : 8

```

*(Figure 3 charts the step-wise improvements. XBOW gains largest from Tool (+14%), PentestGPT-Ben gains most from EGATS (+15%), and GOAD gains from EGATS (+20%) and Memory (+20%).)*

The results align with our Type A/B failure framework. The Tool Layer provides the largest improvement on XBOW (+14 points, from 54 to 68), consistent with CTF failures being predominantly engineering problems addressable through better tooling. The Tool Layer alone yields zero improvement on GOAD (remaining at 2 hosts), where planning rather than capability determines success.

TDA-EGATS adds further gains: +9 points on XBOW (from 68 to 77) through reduced trial-and-error, +2 machines on the PentestGPT benchmark (from 9 to 11), and +1 host on GOAD (from 2 to 3). These gains span both Type A failures (via more efficient search) and Type B failures (via principled exploration-exploitation). The Memory Subsystem contributes across all benchmarks: +8 points on XBOW (from 77 to 85), +1 machine on the PentestGPT benchmark (from 11 to 12), and +1 host on GOAD (from 3 to 4). The GOAD improvement is worth noting separately: extended attack campaigns cause context forgetting in systems without explicit state management, and Memory enables the credential persistence required for the fourth compromise.

### 💡 5.4 RQ3: Strategy Analysis
Beyond aggregate performance, we analyze how TDA-EGATS changes the agent's attack strategy compared to PentestGPT's PTT-based approach.

#### 5.4.1 Search Behavior
Table 7 compares exploration patterns across the PentestGPT benchmark. The metrics show qualitatively different search behaviors between the two systems.

**Table 7: Search behavior comparison on the PentestGPT benchmark** (mean across 13 machines).

| Metric | PentestGPT | PENTESTGPT v2 |
| :--- | :--- | :--- |
| Branches explored | 3.2 | 7.8 |
| Backtrack rate (%) | 8 | 34 |
| Avg. depth before pivot | 12.4 | 5.1 |
| Successful pivots | 0.4 | 2.6 |
| Pruned branches | 0 | 4.2 |

PentestGPT follows a deep-first pattern: it explores fewer branches (3.2 vs. 7.8) but commits to each for longer (average depth 12.4 steps before pivoting vs. 5.1 for PENTESTGPT v2), reflecting the premature commitment failure mode where agents persist on initial hypotheses without signals to recognize intractability.

PENTESTGPT v2 with TDA-EGATS follows an adaptive pattern: TDI monitoring triggers backtracking when success rate drops, and evidence confidence guides exploitation timing. The 4.2 pruned branches per machine are paths abandoned due to persistently high TDI, preventing the infinite loops observed in baseline systems.

#### 🕵️ 5.4.2 Case Study: HTB Falafel
Falafel is a Hard-rated HTB machine requiring a multi-stage attack chain that combines web exploitation, cryptographic quirks, and privilege escalation through Linux group memberships. Figure 4 contrasts how PentestGPT and PENTESTGPT v2 navigate this challenge.

**Figure 4: HTB Falafel exploration comparison.**

```mermaid
flowchart TD
    subgraph PentestGPT PTT
        P1[Start] --> P2[enum]
        P2 --> P3[SQLi 0.3]
        P2 --> P4[Dir abandoned]
        P2 --> P5[Ports abandoned]
        P3 --> P6[Hash 0.4]
        P6 --> P7[BF-1 0.5]
        P7 --> P8[BF-25 0.7]
        P8 --> P9[BF-47 0.9]
        P9 -.->|Stuck: no backtrack, Context degraded 47 failed attempts| P9
    end

    subgraph Excalibur EGATS
        E1[Start] --> E2[enum]
        E2 --> E3[SQLi 0.3]
        E2 --> E4[XSS pruned]
        E2 --> E5[Auth 0.5]
        E3 --> E6[Hash 0.4]
        E6 --> E7[BF 0.7]
        E7 -.->|TDI=0.7 triggers backtrack| E5
        E5 --> E8[RAG 0.3]
        E8 --> E9[TypeJ 0.2]
        E9 --> E10[Shell 0.1]
        E10 --> E11[Root Success]
    end

```

*(a) PentestGPT commits to password brute-force after extracting hashes and stalls after 47 attempts. (b) PENTESTGPT v2's TDI-guided exploration discovers the type juggling bypass when hash cracking fails, then navigates the privilege escalation chain.)*

The attack begins with web enumeration revealing a login form that produces different error messages for valid versus invalid usernames, enabling user discovery through fuzzing. Boolean-based blind SQL injection in the username field allows extracting password hashes from the database. The key step is recognizing that the admin hash begins with "0e462...", a format that PHP's loose comparison operator (==) interprets as scientific notation. Submitting the string "240610708" produces an MD5 hash also starting with "0e", causing both values to compare as zero and bypassing authentication without password cracking. Post-authentication, a filename truncation vulnerability enables code execution: the system truncates filenames exceeding 237 characters, so uploading a file named `[232 A's].php.png` results in an `executable.php` file after truncation removes the `.png` extension. Privilege escalation chains through three stages: database credentials in the PHP configuration yield user `moshe`; membership in the `video` group enables framebuffer capture that reveals `yossi`'s password displayed on screen; membership in the `disk` group allows reading `root`'s files directly via debugfs.

PentestGPT successfully extracts the password hashes but commits to direct cracking via hashcat. After 47 failed attempts with various wordlists and rules, context degradation prevents the model from revisiting the hash format—the type juggling vector is never considered.

PENTESTGPT v2's EGATS tree develops differently. When hash cracking yields repeated failures, rising TDI triggers exploration of authentication alternatives. The Knowledge Augmentation component surfaces PHP type juggling documentation when queried about hashes starting with "0e", enabling the bypass. The Memory Subsystem preserves credentials discovered at each privilege escalation stage, enabling the complete chain from `www-data` through `moshe` and `yossi` to `root`.

#### ❌ 5.4.3 Failure Case: PlayerTwo
To illustrate where TDA-EGATS falls short, we examine PlayerTwo, the only PentestGPT Benchmark machine PENTESTGPT v2 fails to compromise. PlayerTwo requires exploiting a custom Protobuf-based game protocol with no public documentation. PENTESTGPT v2 correctly identifies the service through reconnaissance and spawns hypothesis branches for protocol fuzzing. However, TDI rises rapidly due to repeated failures (low S) and high horizon estimates (the LLM cannot predict steps for an unknown protocol). After three unsuccessful fuzzing attempts, the branch is pruned correctly by TDA's design logic, since success rate indicates intractability.

This failure exposes a TDA limitation: it cannot distinguish "difficult but tractable" from "novel requiring creative reasoning," as both present as high TDI. When RAG retrieval finds no relevant documentation and the LLM lacks parametric knowledge, TDA's evidence-based signals provide no useful guidance. TDA-EGATS therefore improves navigation through known attack spaces but does not address novel exploitation requiring genuine invention.

### 🌍 5.5 RQ4: Real-World Deployment
To assess practical viability, we evaluate PENTESTGPT v2's resource consumption. We further deploy it in a live competition environment to examine its real-world performance.

#### 5.5.1 Cost Analysis
Table 8 presents the resource consumption across benchmarks.

**Table 8: Resource consumption per task** (median values, GPT-5.2 thinking).

| Benchmark | LLM Calls | Time (min) | Cost ($) |
| :--- | :--- | :--- | :--- |
| XBOW | 12 | 3.2 | 0.18 |
| PentestGPT-Ben | 87 | 42 | 4.20 |
| GOAD | 234 | 186 | 28.50 |

PENTESTGPT v2 requires 23% fewer LLM calls than the baseline average on XBOW (12 vs. 15.6 median calls per task) due to reduced trial-and-error from structured tool interfaces, while achieving 39% higher success rates (85% vs. 61%). On GOAD, total calls increase by 18% due to more thorough exploration enabled by EGATS, but this yields 2x more compromised hosts (4 vs. 2). On a per-success basis, PENTESTGPT v2 is 1.8x more cost-effective on XBOW and 1.7x more cost-effective on GOAD: the overhead of EGATS is more than offset by the higher success rates. A complete GOAD engagement costs approximately $28.50 and achieves 80% environment compromise (4 of 5 hosts), making automated penetration testing economically viable for enterprise security assessments.

#### 🌍 5.5.2 Live Competition Deployment
We deployed PENTESTGPT v2 during HTB Season 8 (May-August 2025), a live competition with 13 newly released machines whose solutions remain unavailable until the season concludes. This provides a direct test of real-world viability: unlike retired benchmark machines, Season machines incorporate recent CVEs and novel attack chains with no public walkthroughs.

PENTESTGPT v2 with Opus 4.1 completed 10 of 13 machines (76.9%), achieving a global ranking in the top 100 out of 8,036 active participants.

**Table 9: HTB Season 8 performance by difficulty** (May-August 2025). Total: 10/13 machines (76.9%).

| Difficulty | Completed | Total | Rate |
| :--- | :--- | :--- | :--- |
| Easy | 4 | 4 | 100% |
| Medium | 4 | 4 | 100% |
| Hard | 2 | 3 | 67% |
| Insane | 0 | 2 | 0% |
| **Total** | **10** | **13** | **76.9%** |

Table 9 summarizes performance by difficulty. All four Easy machines and all four Medium machines were compromised successfully. Among Hard machines, PENTESTGPT v2 completed Certificate and RustyKey but failed on Mirage. Both Insane machines, Sorcery and Cobblestone, remained unsolved. The three failures, Mirage (Hard), Sorcery (Insane), and Cobblestone (Insane), represent machines where PENTESTGPT v2 exhausted its search space without finding viable attack paths. These results align with the PlayerTwo analysis (§5.4): when RAG retrieval yields no relevant documentation and the underlying model lacks parametric knowledge of the target vulnerability class, TDA-EGATS cannot guide exploration effectively.

The Season 8 deployment shows that PENTESTGPT v2 can operate in realistic penetration testing scenarios where solutions are unknown and time-constrained. The 100% success rate on Easy and Medium machines suggests readiness for deployment on typical enterprise targets, while Hard and Insane failures mark the current boundaries where human expertise is still required.

---

## 💬 6 Discussion

### 6.1 Limitations and Threats to Validity
We discuss factors that bound the generalizability of our findings.

**Benchmark Scope.** Our evaluation covers web security, network penetration testing, and Active Directory attacks, but omits binary exploitation, mobile security, and cloud-specific attack scenarios where different challenges may dominate. Binary exploitation requiring precise memory layout reasoning poses distinct challenges not captured by our benchmarks. The PentestGPT Benchmark uses retired machines with public walkthroughs, which may inflate absolute numbers through data contamination; however, TDA, EGATS, and Memory target planning challenges orthogonal to specific vulnerability knowledge and thus transfer to novel scenarios. Real-world engagements also involve active defenses and novel vulnerability classes absent from historical benchmarks.

**Model-Specific Effects.** We obtain results with three frontier models (GPT-5.2, Claude-Opus-4.5, Gemini-3.0-Pro). Different model architectures show different strengths: Opus 4.5 achieves the highest XBOW performance (91%), which suggests that our architectural contributions may interact differently across model families. Future model generations may shift the easy/hard boundary and potentially resolve challenges we currently classify as hard.

**Baseline Fairness.** We use published baseline code with default parameters; original authors might achieve better results through tuning, though this reflects realistic deployment scenarios. Because baselines use their original tool invocation mechanisms, reported improvements reflect both tool integration and architectural contributions.

**Failure Analysis.** We analyze PENTESTGPT v2's remaining failures to characterize current boundaries. On XBOW, the 9 failed tasks (9%) fall into two categories: blind injection that requires extensive timing-based exfiltration (4 tasks), and multi-stage attacks that require creative payload chaining not present in our RAG corpus (5 tasks). The single unsolved PentestGPT Benchmark machine (PlayerTwo, Hard) requires exploiting a custom protocol with no public documentation, a novel exploitation scenario that demands reasoning beyond pattern matching. On GOAD, the fifth host (the forest root domain controller) requires a specific attack chain (PrintNightmare → DCSync) that PENTESTGPT v2 identifies but fails to execute due to token constraints. These failures indicate that while PENTESTGPT v2 addresses Type B failures effectively, novel exploitation that requires creative reasoning remains an open problem.

### 🔥 6.2 What Remains Hard
Despite PENTESTGPT v2's gains, three categories of irreducible Type B failures persist that better tooling, larger corpora, or improved prompting cannot resolve.

**The Creativity Barrier.** LLMs are effective at pattern matching but struggle with out-of-distribution generalization [21]. The PlayerTwo failure illustrates this gap: PENTESTGPT v2 systematically explores attack vectors yet fails because no documented exploitation pattern exists for the custom Protobuf-based protocol. The distinction between "difficult" and "novel" matters here. Difficult tasks respond to improved search; novel tasks require reasoning capabilities that current architectures do not provide.

**The Adversarial Environment Barrier.** Penetration testing occurs against active defenders who can exploit agent reasoning patterns [33]. Honeypots, canary tokens, and deceptive services can poison the agent's state representation, causing it to pursue false attack paths or trigger detection. PENTESTGPT v2's evidence grounding protects against self-generated hallucinations but offers limited defense against environmentally-induced false beliefs: when a honeypot presents a convincing vulnerable service, the agent cannot tell whether the vulnerability is genuine or a deliberate trap. This asymmetry favors defenders, who can study and exploit agent behavior, while agents lack the meta-awareness to recognize manipulation.

**The Temporal Scale Barrier.** Human pentesters maintain mental models across engagements that span weeks, correlating information from separate sessions and exercising strategic patience. EGATS improves multi-step reasoning within sessions and the Memory Subsystem preserves state, but neither addresses cross-session continuity. Long-horizon planning is a different problem from long-context processing: it requires hierarchical abstraction, goal decomposition, and progress monitoring, none of which current transformer architectures natively support [27].

---

## 🏁 7 Conclusion
This paper presents a systematic analysis of LLM-based penetration testing that identifies a distinction between Type A failures (capability gaps addressable through engineering) and Type B failures (complexity barriers requiring architectural innovation). We introduce PENTESTGPT v2, which addresses Type A failures through a Tool and Skill Layer with typed interfaces and RAG, and addresses Type B failures via Task Difficulty Assessment (TDA) integrated into Evidence-Guided Attack Tree Search (EGATS). PENTESTGPT v2 achieves 91% task completion on CTF benchmarks (49% improvement over baselines) and compromises 4 of 5 hosts on the GOAD Active Directory environment versus 2 for prior systems. Our ablation studies show that TDA-guided exploration provides benefits beyond tree structure alone: difficulty-aware planning produces value that model improvements cannot replicate.

---

## 🔗 References

[1] Vulnhub: Vulnerable by design. https://www.vulnhub.com/, 2012-2026.

[2] XBOW AI-Powered Offensive Security Platform. https://xbow.com/, 2024.

[3] Anonymous. Excalibur: Source code and artifacts. https://anonymous.4open.science/r/Excalibur-FA7D, 2025. Anonymous repository for double-blind review.

[4] Anthropic. Equipping agents for the real world with Agent Skills, October 2024. Engineering Blog. URL: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills.

[5] Anthropic. Model context protocol. https://modelcontextprotocol.io/, 2024. An open protocol for connecting AI assistants to external data sources and tools, released November 2024.

[6] Rémi Coulom. Efficient selectivity and backup operators in Monte-Carlo tree search. In Computers and Games: 5th International Conference, CG 2006, Turin, Italy, May 29-31, 2006. Revised Papers 5, pages 72-83. Springer, 2007.

[7] Isaac David and Arthur Gervais. Multi-agent penetration testing ai for the web. arXiv preprint arXiv:2508.20816, 2025.

[8] Gelei Deng, Yi Liu, Víctor Mayoral-Vilches, Peng Liu, Yuekang Li, Yuan Xu, Tianwei Zhang, Yang Liu, Martin Pinzger, and Stefan Rass. PentestGPT: Evaluating and harnessing large language models for automated penetration testing. In Proceedings of the 33rd USENIX Security Symposium (USENIX Security 24), pages 847-864. USENIX Association, 2024.

[9] Luca Gioacchini, Marco Mellia, Idilio Drago, Alexander Delsanto, Giuseppe Siracusano, and Roberto Bifulco. AutoPenBench: Benchmarking generative agents for penetration testing. arXiv preprint arXiv:2410.03225, 2024.

[10] Google Project Zero. From naptime to big sleep: Using large language models to catch vulnerabilities in real-world code. https://projectzero.google/2024/10/from-naptime-to-big-sleep.html, October 2024.

[11] Hack The Box. Hack the box: Hacking training for the best. https://www.hackthebox.com/, 2024. Online platform with curated collection of vulnerable machines for penetration testing practice and skill development.

[12] Andreas Happe and Jürgen Cito. Can LLMs hack enterprise networks? autonomous assumed breach penetration-testing active directory networks. ACM Transactions on Software Engineering and Methodology, 2025. doi:10.1145/3766895.

[13] Sean Heelan. How I used o3 to find CVE-2025-37899, a remote zeroday vulnerability in the Linux kernel's SMB implementation. https://sean.heelan.io/2025/05/22/how-i-used-o3-to-find-cve-2025-37899-a-remote-zeroday-vulnerability-in-the-linux-kernels-smb-implementation/, May 2025.

[14] ISC2. ISC2 cybersecurity workforce study 2024. https://www.isc2.org/Insights/2024/10/ISC2-2024-Cybersecurity-Workforce-Study, 2024.

[15] Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik R Narasimhan. SWE-bench: Can language models resolve real-world github issues? In The Twelfth International Conference on Learning Representations, 2024.

[16] Levente Kocsis and Csaba Szepesvári. Bandit based Monte-Carlo planning. In Machine Learning: ECML 2006: 17th European Conference on Machine Learning, Berlin, Germany, September 18-22, 2006. Proceedings 17, pages 282-293. Springer, 2006.

[17] He Kong, Die Hu, Jingguo Ge, Liangxiong Li, Tong Li, and Bingzhen Wu. VulnBot: Autonomous penetration testing for a multi-agent collaborative framework. arXiv preprint arXiv:2501.13411, 2025.

[18] Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. Lost in the middle: How language models use long contexts. Transactions of the Association for Computational Linguistics, 12:157-173, 2024.

[19] Phung Duc Luong, Le Tran Gia Bao, Nguyen Vu Khai Tam, Dong Huu Nguyen Khoa, Nguyen Huu Quyen, Van-Hau Pham, and Phan The Duy. xOffense: An AI-driven autonomous penetration testing framework with offensive knowledge-enhanced LLMs and multi agent systems. arXiv preprint arXiv:2509.13021, 2025.

[20] Wuyuao Mai, Geng Hong, Qi Liu, Jinsong Chen, Jiarun Dai, Xudong Pan, Yuan Zhang, and Min Yang. Shell or nothing: Real-world benchmarks and memory-activated agents for automated penetration testing, 2025. arXiv:2509.09207.

[21] Iman Mirzadeh, Keivan Alizadeh, Hooman Shahrokhi, Oncel Tuzel, Samy Bengio, and Mehrdad Farajtabar. Gsm-symbolic: Understanding the limitations of mathematical reasoning in large language models, 2025. arXiv:2410.05229.

[22] Lajos Muzsai, David Imolai, and András Lukács. Hacksynth: Llm agent and evaluation framework for autonomous penetration testing. arXiv preprint arXiv:2412.01778, 2024.

[23] Sho Nakatani. RapidPen: Fully automated IP-to-shell penetration testing with LLM-based agents. arXiv preprint arXiv:2502.16730, 2025.

[24] Sho Nakatani. Rapidpen: Fully automated ip-to-shell penetration testing with llm-based agents. arXiv preprint arXiv:2502.16730, 2025.

[25] Orange Cyberdefense. GOAD game of active directory. https://github.com/Orange-Cyberdefense/GOAD, 2024.

[26] OWASP Foundation. OWASP web security testing guide. https://owasp.org/www-project-web-security-testing-guide/, 2021.

[27] Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, and Joseph E. Gonzalez. Memgpt: Towards llms as operating systems, 2024. arXiv:2310.08560.

[28] PTES Technical Guideline Development Team. Penetration testing execution standard (PTES). http://www.pentest-standard.org, 2012.

[29] Minghao Shao, Boyuan Chen, Sofija Jancheska, Brendan Dolan-Gavitt, Siddharth Garg, Ramesh Karri, and Muhammad Shafique. An empirical evaluation of LLMs for solving offensive security challenges. arXiv preprint arXiv:2402.11814, 2024.

[30] Xiangmin Shen, Lingzhi Wang, Zhenyuan Li, Yan Chen, Wencheng Zhao, Dawei Sun, Jiashui Wang, and Wei Ruan. PentestAgent: Incorporating LLM agents to automated penetration testing. In Proceedings of the 20th ACM Asia Conference on Computer and Communications Security (ASIA CCS '25), pages 375-391. ACM, 2025.

[31] Georg Wölflein, Dyke Ferber, Daniel Truhn, Ognjen Arandjelovic, and Jakob Nikolas Kather. LLM agents making agent tools. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics, pages 26092-26130, Vienna, Austria, July 2025. Association for Computational Linguistics.

[32] Benlong Wu, Guoqiang Chen, Kejiang Chen, Xiuwei Shang, Jiapeng Han, Yanru He, Weiming Zhang, and Nenghai Yu. AutoPT: How far are we from the end2end automated web penetration testing? arXiv preprint arXiv:2411.01236, 2024.

[33] Qiusi Zhan, Richard Fang, Henil Shalin Panchal, and Daniel Kang. Adaptive attacks break defenses against indirect prompt injection attacks on llm agents, 2025. arXiv:2503.00061.

[34] Shuyan Zhou, Frank F. Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Yonatan Bisk, Daniel Fried, Uri Alon, et al. Webarena: A realistic web environment for building autonomous agents. In The Twelfth International Conference on Learning Representations (ICLR), 2024.

---

## 📑 Appendix

### 📌 A Surveyed LLM-Based Penetration Testing Systems
Table 10 presents the complete list of 28 candidate systems identified in our survey. Systems meeting our inclusion criteria (LLM as core component, targeting penetration testing or CTF challenges, with published technical details) are marked with ✓.

**Table 10: Complete list of surveyed LLM-based penetration testing systems.**

| System | Source | Year | Included |
| :--- | :--- | :--- | :--- |
| PentestGPT [8] | USENIX Security | 2024 | ✓ |
| AutoPT [32] | arXiv | 2024 | ✓ |
| RapidPen [24] | arXiv | 2025 | ✓ |
| PentestAgent [30] | arXiv | 2024 | ✓ |
| VulnBot [17] | arXiv | 2025 | ✓ |
| xOffense [19] | arXiv | 2025 | ✓ |
| TermiAgent [20] | arXiv | 2025 | ✓ |
| HackSynth [22] | arXiv | 2024 | ✓ |
| MAPTA [7] | arXiv | 2025 | ✓ |
| Cochise [12] | arXiv | 2025 | ✓ |
| **Excluded: Vulnerability detection only** | | | |
| VulnScanner-AI | GitHub | 2024 | |
| LLM-SecAudit | arXiv | 2024 | |
| CodeVuln | arXiv | 2024 | |
| BugHunter | RAID | 2024 | |
| AutoFuzz-LLM | CCS | 2024 | |
| **Excluded: Commercial/no details** | | | |
| Pentera | Commercial | 2024 | |
| Cobalt Strike AI | Commercial | 2024 | |
| CrowdStrike Charlotte | Commercial | 2024 | |
| **Excluded: Non-exploitation focus** | | | |
| CTF-Helper | arXiv | 2023 | |
| CryptoSolver | arXiv | 2024 | |
| RevEngGPT | arXiv | 2024 | |
| MalwareGPT | arXiv | 2024 | |
| ThreatGPT | arXiv | 2024 | |
| SecurityBot | GitHub | 2024 | |
| DFIR-Assistant | arXiv | 2024 | |
| IRBot | arXiv | 2025 | |
| SOC-Copilot | arXiv | 2024 | |
| VulnReport-LLM | arXiv | 2024 | |

### 🔧 B Tool and Skill Layer: Supported Tools
Table 11 lists the 38 security tools integrated into PENTESTGPT v2's Tool and Skill Layer. Each tool is exposed through a typed interface specifying input parameters, output schema, and pre/postconditions. Tool selection reflects standard penetration testing methodology and aligns with tools commonly used in professional certifications (e.g., OSCP) and real-world assessments.

**Table 11: Security tools integrated into PENTESTGPT v2.**

| Category | Tool | Description |
| :--- | :--- | :--- |

| Reconnaissance | nmap | Network discovery, port/service scanning, OS fingerprinting |
| | masscan | High-speed port scanner for large networks |

| | gobuster | Directory/DNS bruteforcing for web discovery |
| | ffuf | Web fuzzer for directories, parameters, vhosts |

| | feroxbuster | Recursive web content discovery |
| | nikto | Web server vulnerability scanner |

| | whatweb | Web technology fingerprinting |
| | enum4linux | SMB/Samba enumeration (users, shares, OS) |

| Web Exploitation | sqlmap | SQL injection detection and exploitation |
| | burpsuite | Web proxy for traffic interception and testing |

| | zap | OWASP web vulnerability scanner |
| | wfuzz | Web fuzzer for parameters and authentication |

| | commix | Command injection exploitation |
| | nuclei | Template-based CVE and misconfiguration scanner |

| Network Exploitation | metasploit | Exploitation framework with pre/post-exploitation modules |
| | netcat | TCP/UDP networking utility |

| | crackmapexec | Windows/AD post-exploitation toolkit |
| | responder | LLMNR/NBT-NS poisoner for credential capture |

| | evil-winrm | WinRM shell with pass-the-hash support |
| | chisel | HTTP tunneling for network pivoting |
| | proxychains | SOCKS/HTTP proxy routing for pivoting |

| Credential Attacks | hashcat | GPU password cracker (300+ hash types) |
| | john | Rule-based password cracker |

| | hydra | Online bruteforcing (50+ protocols) |
| | impacket | Protocol library (secretsdump, psexec, wmiexec) |
| | kerbrute | Kerberos user enumeration and password spraying |

| Active Directory | bloodhound | AD attack path visualization via graph analysis |
| | sharphound | BloodHound data collector |
| | rubeus | Kerberos attack toolkit (roasting, tickets) |

| Privilege Escalation | mimikatz | Memory credential extraction |
| | powerview | AD enumeration PowerShell tool |

| | ldapdomaindump | LDAP data extraction |
| | pingcastle | AD security assessment and risk scoring |

| | adrecon | AD reconnaissance reporting |
| | linpeas | Linux privesc enumeration |

| | winpeas | Windows privesc enumeration |
| | pspy | Linux process monitor (cron, scheduled tasks) |
| | seatbelt | Windows security auditing |

### 📌 C Evidence Confidence Scoring
Table 12 presents the complete evidence confidence scoring rubric used by the TDA mechanism. Scores are assigned deterministically based on evidence type, enabling reproducible difficulty assessment.

**Path Confidence Computation.** For a path $P=(n_0,n_1,...,n_k)$ from root to current node, the evidence confidence is computed as:

$$
E(P) = \frac{1}{k} \sum_{i=1}^{k} e(n_i) \quad (3)
$$

where $e(n_i)$ is the confidence score assigned to node $n_i$ based on Table 12. The root node $n_0$ is excluded as it represents the initial state before any evidence is gathered.

**Tool Output Parsing.** Evidence types are determined automatically by parsing tool outputs against expected patterns. For example, nmap output containing "open" with a service version triggers version-matched vulnerability lookup (0.5); sqlmap output containing "injectable" triggers confirmed injection (0.8); successful ssh connection triggers valid credentials (1.0). The Tool Layer's typed interfaces (Section 4.2) provide structured outputs that simplify this parsing.

**Example.** Consider a path: port scan → web server (nginx 1.18) → directory bruteforce → login form discovered → SQL injection confirmed. Evidence scores are: 0.3 (service identified), 0.5 (version-matched to known nginx vulnerabilities), 0.3 (endpoint exists), 0.8 (injection confirmed). Path confidence $E = (0.3+0.5+0.3+0.8)/4 = 0.475$, indicating moderate confidence appropriate for transitioning from reconnaissance to exploitation.

**Table 12: Evidence confidence scoring rubric.**

| Evidence Type | Score | Indicators |
| :--- | :--- | :--- |
| **Verified Evidence (Exploitation Confirmed)** | | |
| Valid credentials | 1.0 | Successful authentication via SSH, WinRM, SMB, or web login |
| Shell access | 1.0 | Interactive command execution confirmed |
| Data exfiltration | 1.0 | Sensitive data retrieved (flags, database contents, config files) |
| **Confirmed Vulnerability (Exploit Available)** | | |
| CVE with public exploit | 0.8 | Vulnerability scanner confirmation + Exploit-DB/Metasploit module exists |
| Auth bypass confirmed | 0.8 | Endpoint accessible without credentials when authentication expected |
| Injection confirmed | 0.8 | SQL/command injection produces observable side effects |
| **Plausible Hypothesis (Evidence Supports)** | | |
| Version-matched vuln | 0.5 | Service version matches known vulnerable version range |
| Configuration weakness | 0.5 | Misconfiguration identified (default credentials, open permissions) |
| Information disclosure | 0.5 | Sensitive information leaked (usernames, paths, internal IPs) |
| **Speculative Hypothesis (Minimal Evidence)** | | |
| Service identified | 0.3 | Port open with service fingerprint, no version/vulnerability match |
| Potential attack surface | 0.3 | Endpoint exists but no vulnerability indicators |
| Unconfirmed assumption | 0.3 | Hypothesis based on common patterns without direct evidence |

### 📌 D Parameter Derivation and Validation
This appendix documents the derivation and sensitivity analysis for hyperparameters in PENTESTGPT v2.

#### D.1 Validation Dataset
All hyperparameters are tuned on a held-out validation set of 30 execution traces from retired HTB machines (2022-2023), disjoint from the PentestGPT Benchmark evaluation set. The validation set includes 10 Easy, 12 Medium, and 8 Hard machines, covering web exploitation (12), Linux privilege escalation (10), and Windows/AD attacks (8). We use GPT-4.0 for validation to avoid overlap with evaluation models (GPT-5.2, Opus 4.5, Gemini 3).

#### 📌 D.2 TDI Weight Selection
Table 13 presents TDI weights derived via grid search over $w \in [0.1,0.4]$ with step size 0.05, subject to $\Sigma w_i = 1$. Performance is measured as mean subtask completion rate across the validation set.

**Table 13: TDI weight sensitivity analysis.** Performance (subtask completion %) across weight configurations. Bold indicates selected weights.

| $w_H$ | $w_E$ | $w_C$ | $w_S$ | Performance (%) |
| :--- | :--- | :--- | :--- | :--- |
| 0.25 | 0.25 | 0.25 | 0.25 | 71.2 |
| **0.30** | **0.30** | **0.20** | **0.20** | **73.8** |
| 0.35 | 0.25 | 0.20 | 0.20 | 72.4 |
| 0.25 | 0.35 | 0.20 | 0.20 | 73.1 |
| 0.30 | 0.25 | 0.25 | 0.20 | 72.9 |
| 0.40 | 0.30 | 0.15 | 0.15 | 70.8 |

Performance varies within ±3% across configurations where all weights remain in [0.1, 0.4], indicating robustness to precise weight selection. The selected configuration ($w_H=w_E=0.3$, $w_C=w_S=0.2$) reflects domain intuition: horizon and evidence confidence are primary difficulty signals, while context load and success rate provide secondary modulation.

#### 📌 D.3 Mode Selection Thresholds
Table 14 presents sensitivity analysis for mode selection thresholds ($\theta_{explore}$, $\theta_{exploit}$).

**Table 14: Mode selection threshold sensitivity.**

| $\theta_{explore}$ | $\theta_{exploit}$ | Performance (%) |
| :--- | :--- | :--- |
| 0.5 | 0.2 | 72.1 |
| 0.5 | 0.3 | 72.8 |
| 0.6 | 0.2 | 73.2 |
| **0.6** | **0.3** | **73.8** |
| 0.6 | 0.4 | 72.4 |
| 0.7 | 0.3 | 73.0 |
| 0.7 | 0.4 | 71.6 |

The intermediate zone ($\theta_{exploit} \le TDI \le \theta_{explore}$) triggers LLMDECIDE. Narrower zones reduce LLM calls but sacrifice adaptivity; wider zones increase overhead without proportional benefit.

#### 📌 D.4 Pruning Parameters
The pruning threshold ($\theta_{prune}=0.8$) and minimum attempts ($k_{min}=3$) prevent both premature and excessively delayed pruning.

**Table 15: Pruning parameter sensitivity.**

| $\theta_{prune}$ | $k_{min}$ | Completion | False Prune | Wasted |
| :--- | :--- | :--- | :--- | :--- |
| 0.7 | 2 | 71.2 | 8.4 | 2.1 |
| 0.7 | 3 | 72.4 | 5.2 | 3.4 |
| **0.8** | **3** | **73.8** | **2.8** | **4.1** |
| 0.8 | 4 | 73.2 | 1.9 | 5.8 |
| 0.9 | 3 | 72.1 | 1.2 | 6.9 |

Lower thresholds increase false pruning (abandoning tractable paths); higher thresholds waste attempts on intractable paths. The selected configuration achieves favorable balance.

#### 📌 D.5 UCB Difficulty Penalty
The difficulty penalty coefficient ($\lambda=0.5$) modulates how strongly TDI affects node selection in the UCB formula.

**Table 16: UCB difficulty penalty ($\lambda$) sensitivity.**

| $\lambda$ | Completion (%) | Backtrack Rate (%) |
| :--- | :--- | :--- |
| 0.0 (standard UCB) | 68.4 | 12 |
| 0.25 | 71.2 | 21 |
| **0.5** | **73.8** | **34** |
| 0.75 | 72.1 | 42 |
| 1.0 | 69.8 | 51 |

$\lambda=0$ recovers standard UCB, which underperforms due to insufficient difficulty awareness. $\lambda=1.0$ over-penalizes difficult nodes, preventing exploration of challenging but tractable paths.

#### 📌 D.6 Context Load Degradation Study
To establish the 40% context load threshold, we conduct a controlled study measuring LLM instruction-following accuracy under varying context loads.

**Methodology.** We construct 50 penetration testing instruction-following tasks from an independent GOAD deployment (separate from evaluation instances). Each task comprises a system state description, accumulated context (tool outputs, discovered information), and a specific instruction (e.g., "Extract the service account password from the Kerberoast output and attempt authentication"). Tasks are designed with unambiguous correct responses, enabling binary accuracy scoring.

For each task, we generate context variants at 10%, 20%, 30%, 40%, 50%, 60%, 70%, 80%, and 90% of the model's context window. Context padding uses realistic penetration testing artifacts: verbose tool outputs, reconnaissance results, and session histories from actual GOAD runs. Padding is inserted before the instruction to simulate accumulated session context. We evaluate GPT-4.0 (128K context), Claude-3-Sonnet (200K context), and Gemini-1.5-Pro (1M context) with temperature 0, running each task-context combination three times.

Performance remains stable (>90%) up to 40% load, then degrades approximately linearly. The 40% threshold represents the inflection point beyond which additional context yields diminishing returns and begins actively harming performance.

**Failure Mode Analysis.** Beyond 40% load, failures concentrate in three categories: ignoring relevant information from earlier context (42% of failures), hallucinating tool outputs not present in context (31%), and executing incorrect but plausible commands (27%). These patterns align with the "lost in the middle" phenomenon documented in prior work [18].
