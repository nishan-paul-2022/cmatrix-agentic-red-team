# 🤖 Getting pwn'd by AI: Penetration Testing with Large Language Models

> 📜 **Paper Information**
> * **Authors:** **Andreas Happe** *(TU Wien, Austria)* — `andreas.happe@tuwien.ac.at`, **Jürgen Cito** *(TU Wien, Austria)* — `juergen.cito@tuwien.ac.at`
> * **Published:** ACM ESEC/FSE '23, December 3–9, 2023, San Francisco, CA, USA
> * **arXiv:** `2308.00121v3 [cs.CL]` (17 Aug 2023)
> * **ACM Reference:** Andreas Happe and Jürgen Cito. 2023. *Getting pwn'd by AI: Penetration Testing with Large Language Models*. In Proceedings of ESEC/FSE '23, pages 1–5. DOI: `10.1145/3611643.3613083`

---

## 📑 Table of Contents
- [📌 Abstract](#-abstract)
- [🚀 1. Introduction](#-1-introduction)
- [📖 2. Background](#-2-background)
- [🛡️ 3. LLM-Based Penetration Testing](#️-3-llm-based-penetration-testing)
  - [3.1 High-Level: Task-Planning Systems](#31-high-level-task-planning-systems)
  - [3.2 Low-Level: Attack-Execution System](#32-low-level-attack-execution-system)
- [💬 4. Discussion](#-4-discussion)
  - [4.1 Grounding of Results and Hallucinations](#41-grounding-of-results-and-hallucinations)
  - [4.2 Stability and Reproducibility](#42-stability-and-reproducibility)
  - [4.3 Ethical Moderation in LLMs](#43-ethical-moderation-in-llms)
- [🔮 5. A Vision of AI-Augmented Pen-Testing](#-5-a-vision-of-ai-augmented-pen-testing)
  - [5.1 Integration of High- and Low-Level](#51-integration-of-high--and-low-level)
  - [5.2 Investigation of Model Options](#52-investigation-of-model-options)
  - [5.3 Memory, Verification, and Reflection](#53-memory-verification-and-reflection)
  - [5.4 Prompts for Asking Better Questions](#54-prompts-for-asking-better-questions)
- [⚖️ 6. Final Ethical Considerations](#️-6-final-ethical-considerations)
- [🔗 References](#-references)

---

## 📌 Abstract

The field of software security testing, more specifically **penetration testing**, requires high levels of expertise and involves many manual testing and analysis steps. This paper explores the potential use of large language models (LLMs), such as **GPT-3.5**, to augment penetration testers with **AI sparring partners**. We explore two distinct use cases:
1. **High-level task planning** for security testing assignments.
2. **Low-level vulnerability hunting** within a vulnerable virtual machine.

For the latter, we implemented a closed-feedback loop connecting LLM-generated low-level actions via SSH with a vulnerable Linux virtual machine (`lin.security`). The LLM analyzes machine state outputs, identifies vulnerabilities, and suggests concrete attack vectors which are automatically executed. We discuss promising initial results, avenues for technical improvement, and deliberate on the ethics of AI sparring partners.

```
CCS CONCEPTS: Security and privacy -> Systems security
KEYWORDS: security testing, penetration testing, large language models
```

---

## 🚀 1. Introduction

Large language models (LLMs), such as ChatGPT or GPT-3.5, have become a hot topic in computer science and cybersecurity [12]. The field of cybersecurity suffers from a chronic workforce deficit [19]. According to the *(ISC)² Cybersecurity Workforce Study 2022* [18], while the global cybersecurity workforce grew by 11.1% YoY, the supply gap expanded by **26.2% YoY**.

Recent empirical research with penetration testers highlights the urgent need for **human sparring partners**—colleagues who brainstorm alternative attack vectors when a tester gets stuck [16]. Furthermore, intuition plays a significant role in flaw discovery, often honed through Capture-the-Flag (CTF)[^1] events. Augmenting human operators with AI-based agents creates powerful new capabilities, counteracts skill shortages, and accelerates on-the-job training for novice penetration testers [7]. Keeping a human operator in the loop additionally mitigates key ethical risks [6].

> 🎯 **Research Question (RQ)**
> **To what extent can we automate security testing with LLMs?**
>
> To evaluate whether LLMs can serve as effective sparring partners, we leverage the **MITRE ATT&CK** framework as a guiding structure. A capable sparring partner must cover the full spectrum of tactics, techniques, and procedures (TTPs).

### 🔍 Scope & Ethical Boundaries
We recognize other security areas where generative AI excels (e.g., crafting spear-phishing or vishing messages). For ethical reasons, attacks designed to deceive humans were excluded from this study. Conversely, tedious administrative workflows like automated penetration test report generation represent promising non-malicious use cases.

---

## 📖 2. Background

```
                              ┌─────────────────────────────────────────┐
                              │            MITRE ATT&CK TTP             │
                              └────────────────────┬────────────────────┘
                                                   │
                   ┌───────────────────────────────┼───────────────────────────────┐
                   ▼                               ▼                               ▼
       ┌───────────────────────┐       ┌───────────────────────┐       ┌───────────────────────┐
       │     Tactics (T)       │       │    Techniques (T)     │       │    Procedures (P)     │
       │  High-level Goal      │  ──►  │ Specific Method Used  │  ──►  │ Concrete CLI Exec     │
       │  (e.g., PrivEsc)      │       │ (e.g., Sudo Caching) │       │ (e.g., sudo -l execution)
       └───────────────────────┘       └───────────────────────┘       └───────────────────────┘
```

### 1. MITRE ATT&CK Framework
MITRE ATT&CK [37] is a knowledge base of adversary tactics, techniques, and procedures (TTPs):
* **Tactics (T):** High-level adversary objectives (e.g., Reconnaissance, Privilege Escalation, Collection).
* **Techniques (T):** Methods used to achieve a tactic (e.g., *Abuse Elevation Control Mechanism: Sudo and Sudo Caching* [3]).
* **Procedures (P):** Specific execution details and technical commands used to implement a technique.

An AI sparring partner must span the complete TTP spectrum: deriving appropriate tactics at a macro level, and proposing actionable procedures at a micro level.

### 2. Large Language Models & Prompt Engineering
LLMs are deep neural networks trained via self-supervised learning on massive text corpora. Model capability correlates strongly with parameter scale (ranging from 7B in base LLaMA models up to hundreds of billions / trillions in GPT-4). Prompt engineering [10, 22, 36, 40] has emerged as the core discipline for structuring text queries to elicit accurate model behavior. Local inference engines like `llama.cpp` [14] enable 13B-parameter models to run on consumer hardware without API fees or server-side moderation.

### 3. Pre-trained Autonomous AI Agents
* **AutoGPT [15]:** Generates autonomous task sequences by querying LLMs to refine their own prompts. Incorporates external web search and human feedback to minimize hallucinations [29].
* **BabyAGI [25, 26, 27]:** Splits high-level goals into subtasks managed via a task queue. Uses specialized execution, task-creation, context, and prioritization agents powered by GPT-4.
* **Jarvis / HuggingGPT [33]:** Connects LLMs with multimodal models to execute multi-step workflows.

---

## 🛡️ 3. LLM-Based Penetration Testing

We evaluate two distinct operational levels:
1. **High-Level (Task Planning):** "What is an effective attack methodology against Active Directory?"
2. **Low-Level (Attack Execution):** "I have local shell access; how can I escalate privileges on this specific Linux VM?"

---

### 3.1 High-Level: Task-Planning Systems

To evaluate macro-level planning:

#### Scenario A: Active Directory Exploitation
We tasked **AgentGPT** to *"Become domain admin in an Active Directory"*. The agent generated highly realistic attack vectors:
* Password spraying
* Kerberoasting & AS-REP roasting
* Exploiting Active Directory Certificate Services (AD CS)
* Abusing unconstrained delegation
* Exploiting Group Policy Objects (GPOs)

#### Scenario B: External Penetration Test Plan
With target authorization, we tasked **AutoGPT** to devise an external penetration testing plan for a target company. AutoGPT synthesized a standard methodology:
1. Network vulnerability scanning
2. OSINT & user enumeration
3. Phishing campaign against identified targets

When instructed further, AutoGPT successfully crawled the target website to discover email addresses, but halted real security scans and phishing due to built-in ethical guardrails.

---

### 3.2 Low-Level: Attack-Execution System

To evaluate micro-level attack execution, we developed an autonomous SSH feedback loop against a vulnerable Linux VM (`lin.security` [21]). The prototype source code is publicly available at **[hackingBuddyGPT](https://github.com/ipa-lab/hackingBuddyGPT)**.

#### 📌 Figure 1: High-Level Architecture Overview

```mermaid
flowchart LR
    User(("Low-Privilege User\n(Human Operator)"))
    LLM["LLM Agent\n(GPT-3.5-turbo)"]
    VM["Vulnerable VM\n(lin.security)"]
    TermOutput[/"Executed CLI Output:<br>$ sudo -l<br>$ sudo /usr/bin/perl -e 'exec \"/bin/sh\";'"/]

    User -->|"1. Initial Prompt"| LLM
    LLM -->|"2. Shell Command (SSH)"| VM
    VM -->|"3. Terminal Output"| LLM
    LLM -->|"4. Analysis & Refinement"| LLM
    LLM -->|"5. Root Shell Achieved"| User
    VM -.- TermOutput
```
*Figure 1: Closed-loop architecture connecting GPT-3.5 to an SSH target VM.*

#### Execution Loop Mechanics
1. **Instruction:** The Python script prompts GPT-3.5, assigning the persona of a low-privileged user aiming to obtain `root` privileges.
2. **Execution:** The LLM returns a single Linux shell command, which the script executes over SSH on the target VM.
3. **Feedback:** Terminal output is returned back to the LLM context for the next iteration.
4. **Vulnerability Analysis:** Concurrently, GPT-3.5 is asked to analyze terminal output and suggest "verification commands" (exploitation commands) for identified flaws.

> 🏆 **Exploitation Success**
> The prototype routinely escalated privileges to **`root`** on the `lin.security` VM. 
> * **Primary Path:** Checking `sudo -l`, followed by invoking `sudo` with permitted binary shells or leveraging **GTFObins** (benign binaries executable as root).
> * **Secondary Path:** Inspecting `/etc/passwd` to spot accounts lacking shadow password hashes[^2].
> * **Reverse Shells:** When instructed to spawn a reverse shell to a specified remote IP, the agent successfully executed a payload and dropped a root shell.

---

## 💬 4. Discussion

### 4.1 Grounding of Results and Hallucinations

Because all SSH interactions were logged, we verified whether LLM command choices stemmed from real terminal feedback or prior training data (analogous to human CTF intuition):

```
                        ┌─────────────────────────────────────────┐
                        │          LLM Command Decisions          │
                        └────────────────────┬────────────────────┘
                                             │
                   ┌─────────────────────────┴─────────────────────────┐
                   ▼                                                   ▼
       ┌───────────────────────┐                           ┌───────────────────────┐
       │  System-Grounded      │                           │  Prior Knowledge      │
       │  Causal Reasoning     │                           │  (CTF / Heuristics)   │
       ├───────────────────────┤                           ├───────────────────────┤
       │ • sudo -l -> GTFObins │                           │ • DirtyCOW attempts   │
       │ • /etc/passwd -> hash │                           │ • General Linux OS    │
       │   cracking            │                           │   enumeration         │
       └───────────────────────┘                           └───────────────────────┘
```

* **Causal Reasoning:** GPT-3.5 demonstrated clear multi-step reasoning. Inspecting `sudo -l` immediately triggered attempts to exploit listed binaries. Parsing `/etc/passwd` triggered targeted password attacks.
* **Prior Knowledge / Heuristics:** Unprompted suggestions (e.g., checking for `dirty_cow` exploits) occurred based on general OS knowledge prior to specific enumeration.
* **Hallucinations:** Pure hallucinations were rare. The most frequent hallucination was requesting execution of `exploit.sh` (a generic script name frequent in online CTF writeups).

---

### 4.2 Stability and Reproducibility

* **Single-Run Variance:** Individual runs exhibited variance in command choices. The agent occasionally focused too long on single aspects ("going down a rabbit hole"), a phenomenon common among novice human penetration testers [16].
* **Statistical Convergence:** When aggregated over tens of runs, performance converged reliably on successful privilege escalation paths.
* **Comparison to Deterministic Tools:** Tools like `linpeas.sh` [30] follow strict, hardcoded rule trees. LLMs are non-deterministic. Interestingly, during one run, GPT-3.5 attempted to download and execute `linpeas.sh` directly (failing only due to an invalid URL).

---

### 4.3 Ethical Moderation in LLMs

During experiments with `GPT-3.5-turbo`:
* **Bypassing Filters:** Standard safety filters were infrequently triggered during SSH command generation. Framing prompts with *"do not ask questions or provide judgments"* effectively bypassed denials.
* **Reframing Attack Terms:** Replacing security terms like *"exploit"* with *"verification command"* completely eliminated safety filter rejections.
* **Local Models:** Transitioning from commercial cloud APIs to uncensored local models (e.g., LLaMA derivatives) bypasses all server-side ethical moderation layers.

---

## 🔮 5. A Vision of AI-Augmented Pen-Testing

```
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                 Unified AI Sparring Assistant Architecture                 │
  └──────────────────────────────────────┬──────────────────────────────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
     ┌───────────────────────┐                       ┌───────────────────────┐
     │  High-Level Planner   │                       │  Low-Level Executor   │
     │  (Macro Strategy)     │  ◄── Shared Memory ──►│  (SSH / CLI Actions)  │
     └───────────────────────┘                       └───────────────────────┘
```

### 5.1 Integration of High- and Low-Level
Future architectures should unify high-level strategy planning and low-level CLI execution into a single agent framework. Testers can alternate seamlessly between macro queries (*"What AD attack should I try next?"*) and micro actions (*"Escalate privilege on this host"*), creating synergy across the engagement lifecycle.

### 5.2 Investigation of Model Options
Evaluating cloud APIs against open-weight local models (**LLaMA** [39], **StableLM** [35], **Dolly 2.0** [9], **Koala** [13]):
* **Data Privacy:** Local models prevent corporate data leaks to third-party APIs.
* **Domain Fine-Tuning:** Local models allow continuous fine-tuning on organization-specific pentest reports and target environment patterns over time.

### 5.3 Memory, Verification, and Reflection
Current context windows (e.g., 4k tokens in early GPT-3.5) limit execution history. Enhancements include:
* **Reflected Memory [28]:** Summarizing past terminal outputs to retain essential system state findings while discarding raw CLI noise.
* **Multi-Stream Memory:** Maintaining separate memory queues for (1) executed CLI history, (2) discovered vulnerabilities, and (3) inferred target system models to prevent hallucinations.

### 5.4 Prompts for Asking Better Questions
Meta-prompting (using LLMs to optimize execution prompts) can enhance effectiveness. Studying empirical human pentester workflows [16] will inform better prompt structures and user-agent collaboration models.

---

## ⚖️ 6. Final Ethical Considerations

Dual-use security research presents unavoidable dilemmas:
* **Accessibility of Exploitation:** Local open-source foundation models can be fine-tuned for malicious activity for less than **$1,000 USD** in cloud compute costs [5].
* **Democratization:** Prompt engineering removes traditional barriers to entry, enabling non-technical actors to deploy automated attack pipelines.
* **The Red Queen's Race:** Defensive capabilities must evolve rapidly [8, 17]. Because malicious actors will inevitably employ autonomous LLM agents [1], security defenders must harness LLMs to keep pace.

---

## 🔗 References

1. AIAAIC. 2023. *Repository of incidents and controversies related to AI, algorithms and automation*. `https://www.aiaaic.org/`
2. The Wassenaar Arrangement. 1982. *Export Controls for Dual-Use Goods and Technologies*. `https://www.wassenaar.org/`
3. MITRE ATT&CK. 2020. *Abuse Elevation Control Mechanism: Sudo and Sudo Caching (T1548.003)*. `https://attack.mitre.org/techniques/T1548/003/`
4. MITRE ATT&CK. 2020. *Steal or Forge Kerberos Tickets: Kerberoasting (T1558.003)*. `https://attack.mitre.org/techniques/T1558/003/`
5. Edward Beeching et al. 2023. *StackLLaMA: An RL Fine-tuned LLaMA Model*. DOI: `10.57967/hf/0513`
6. Erik Brynjolfsson. 2023. *The Turing Trap: Promise & Peril of Human-Like AI*. Routledge.
7. Erik Brynjolfsson et al. 2023. *Generative AI at Work*. NBER Working Paper No. 31161.
8. Vit Bukac et al. 2014. *Red Queen's Race: APT Win-Win Game*. Springer.
9. Mike Conover et al. 2023. *Free Dolly: Open Instruction-Tuned LLM*. Databricks.
10. Paul Denny et al. 2023. *Conversing with Copilot: Prompt Engineering for CS1*. ACM SIGCSE.
11. The Economist. 2022. *Huge foundation models are turbo-charging AI progress*.
12. The Economist. 2023. *Large, creative AI models will transform lives and labour markets*.
13. Xinyang Geng et al. 2023. *Koala: A Dialogue Model for Academic Research*. BAIR.
14. Georgi Gerganov. 2023. *llama.cpp: Inference of LLaMA model in pure C/C++*. `https://github.com/ggerganov/llama.cpp`
15. Significant Gravitas. 2023. *Auto-GPT: An Autonomous GPT-4 Experiment*. `https://github.com/Significant-Gravitas/Auto-GPT`
16. Andreas Happe and Jürgen Cito. 2023. *Understanding Hackers' Work: An Empirical Study of Offensive Security Practitioners*. ESEC/FSE '23. ACM.
17. Richard Harang and Felipe N Ducau. 2018. *Measuring the speed of the Red Queen's Race*. BlackHat USA.
18. (ISC)². 2022. *(ISC)² Cybersecurity Workforce Study 2022*. `https://www.isc2.org/`
19. Sydney Lake. 2022. *The cybersecurity industry is short 3.4 million workers*. Fortune.
20. Selena Larson and Daniel Blackford. 2021. *Cobalt Strike: Favorite Tool from APT to Crimeware*. Proofpoint.
21. lin.security. 2018. *Lin.Security Vulnerable Virtual Machine*. VulnHub. `https://www.vulnhub.com/entry/linsecurity-1,244/`
22. Vivian Liu and Lydia B Chilton. 2022. *Design guidelines for prompt engineering*. ACM CHI.
23. Nestor Maslej et al. 2023. *The AI Index 2023 Annual Report*. Stanford HAI.
24. Ron Miller. 2023. *Sam Altman: Size of LLMs won't matter as much moving forward*. TechCrunch.
25. Yohei Nakajima. 2023. *BabyAGI*. `https://github.com/yoheinakajima/babyagi`
26. Yohei Nakajima. 2023. *Introducing Task-driven Autonomous Agent*. Twitter post.
27. Yohei Nakajima. 2023. *Task-driven Autonomous Agent Utilizing GPT-4, Pinecone, and LangChain*.
28. Joon Sung Park et al. 2023. *Generative Agents: Interactive Simulacra of Human Behavior*. arXiv:2304.03442.
29. Baolin Peng et al. 2023. *Check Your Facts and Try Again*. arXiv:2302.12813.
30. Carlos Polop. 2023. *LinPEAS - Linux Privilege Escalation Awesome Script*. `https://github.com/carlospolop/PEASS-ng`
31. Katyanna Quach. 2023. *LLaMA drama as Meta's mega language model leaks*. The Register.
32. Kevin Schaul et al. 2023. *Inside the secret list of websites that make AI like ChatGPT sound smart*. Washington Post.
33. Yongliang Shen et al. 2023. *HuggingGPT: Solving AI Tasks with ChatGPT and its Friends*. arXiv:2303.17580.
34. Cybereason Global SOC. 2023. *Sliver C2 Leveraged by Many Threat Actors*.
35. Stability AI. 2023. *Stability AI Launches StableLM Suite*.
36. Hendrik Strobelt et al. 2022. *Interactive and Visual Prompt Engineering*. IEEE TVCG.
37. Blake E Strom et al. 2018. *MITRE ATT&CK: Design and Philosophy*. Technical Report, MITRE.
38. Jason Wei et al. 2022. *Emergent Abilities of Large Language Models*. arXiv:2206.07682.
39. Renrui Zhang et al. 2023. *LLaMA-Adapter: Efficient Fine-Tuning of Language Models*. arXiv:2303.16199.
40. Kaiyang Zhou et al. 2022. *Learning to Prompt for Vision-Language Models*. IJCV.

---

## 📌 Footnotes

[^1]: CTFs (Capture-The-Flag) are gamified penetration-testing exercises.
[^2]: If your Linux system is not using shadow passwords by now, ChatGPT is the least of your worries.
