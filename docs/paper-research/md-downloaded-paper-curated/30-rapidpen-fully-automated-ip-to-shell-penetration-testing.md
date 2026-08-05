# **RapidPen: Fully Automated IP-to-Shell Penetration Testing with LLM-based Agents** 

## Table of Contents

- [Abstract](#abstract)
- [1 Introduction](#1-introduction)
- [Research Questions (RQs)](#research-questions-rqs)
- [Contributions and Scope](#contributions-and-scope)
- [2 Background and Motivation](#2-background-and-motivation)
- [2.1 Overview of Penetration Testing](#2-1-overview-of-penetration-testing)
- [2.2 LLM-Driven Automation in General](#2-2-llm-driven-automation-in-general)
- [2.3 Existing Research and Opportunities for Improvement](#2-3-existing-research-and-opportunities-for-improvement)
- [3 Threat Model and Problem Definition](#3-threat-model-and-problem-definition)
- [3.1 Threat Model](#3-1-threat-model)
- [3.2 Assumptions](#3-2-assumptions)
- [3.3 Scope and Limitations](#3-3-scope-and-limitations)
- [4 Design Overview of RapidPen](#4-design-overview-of-rapidpen)
- [4.2 PTT as a Core Data Model in the Re Module](#4-2-ptt-as-a-core-data-model-in-the-re-module)
- [4.1 System Architecture](#4-1-system-architecture)
- [4.3 Layered ReAct Modules in RapidPen](#4-3-layered-react-modules-in-rapidpen)
- [4.4 RAG for Offensive Security](#4-4-rag-for-offensive-security)
- [4.5 Feedback Cycle in Act Module](#4-5-feedback-cycle-in-act-module)
- [5 Implementation](#5-implementation)
- [5.1 Prototype Setup and LLM Usage](#5-1-prototype-setup-and-llm-usage)
- [5.2 RapidPen-vis](#5-2-rapidpen-vis)
- [5.3 Custom Dify-Sandbox](#5-3-custom-dify-sandbox)
  - [6.2.1 Testing Two Configurations](#6-2-1-testing-two-configurations)
- [6 Evaluation](#6-evaluation)
- [6.1 Objectives and Questions](#6-1-objectives-and-questions)
- [6.3 Results](#6-3-results)
  - [6.3.1 Overall Success Rates and Timings](#6-3-1-overall-success-rates-and-timings)
- [6.2 Experimental Setup](#6-2-experimental-setup)
  - [6.3.2 Observations and Discussion](#6-3-2-observations-and-discussion)
  - [• Failure Causes:](#failure-causes)
- [6.4 Module-Wise Time and Cost Breakdown](#6-4-module-wise-time-and-cost-breakdown)
- [6.5 Behavioral Insights](#6-5-behavioral-insights)
- [6.6 Summary of Findings](#6-6-summary-of-findings)
- [7 Discussion](#7-discussion)
- [7.1 Benefits and Future Directions of the Act Feedback Mechanism](#7-1-benefits-and-future-directions-of-the-act-feedback-mechanism)
- [7.2 Advantages and Limitations of Using Success Cases](#7-2-advantages-and-limitations-of-using-success-cases)
- [7.3 Expanding the Attack Surface](#7-3-expanding-the-attack-surface)
- [7.4 Ethical and Safety Considerations](#7-4-ethical-and-safety-considerations)
- [8 Related Work](#8-related-work)
- [8.1 LLM-Based Penetration Testing](#8-1-llm-based-penetration-testing)
  - [8.1.1 PentestGPT – Task Tree-Driven AI Pentesting](#8-1-1-pentestgpt-task-tree-driven-ai-pentesting)
  - [8.1.2 Other LLM-Driven Pentesting Tools](#8-1-2-other-llm-driven-pentesting-tools)
  - [Tools that Automate Initial Access but Focus on Broad Vulnerability Scanning Rather than Speed](#tools-that-automate-initial-access-but-focus-on-broad-vulnerability-scanning-rather-than-speed)
  - [Tools That Focus on Post-Exploitation and Are Complementary to RapidPen](#tools-that-focus-on-post-exploitation-and-are-complementary-to-rapidpen)
- [8.2 Reinforcement Learning-Based Penetration Testing Approaches](#8-2-reinforcement-learning-based-penetration-testing-approaches)
- [8.3 Comparison with RapidPen](#8-3-comparison-with-rapidpen)
- [9 Conclusion and Future Work](#9-conclusion-and-future-work)
- [9.1 Summary of Contributions](#9-1-summary-of-contributions)
- [9.2 Future Directions](#9-2-future-directions)
- [9.3 Closing Remarks](#9-3-closing-remarks)
- [References](#references)

---

Sho Nakatani _SecDevLab Inc._ 

## **Abstract** 

> **Section Summary:** We present **RapidPen** , a fully automated penetration testing (pentesting) framework that addresses the challenge of achieving an initial foothold ( _IP-to-Shell_ ) without human intervention.


We present **RapidPen** , a fully automated penetration testing (pentesting) framework that addresses the challenge of achieving an initial foothold ( _IP-to-Shell_ ) without human intervention. Unlike prior approaches that focus primarily on post-exploitation or require a _human-in-the-loop_ , RapidPen leverages large language models (LLMs) to autonomously discover and exploit vulnerabilities, starting from a single IP address. By integrating advanced ReAct-style task planning ( _Re_ ) with retrieval-augmented knowledge bases of successful exploits, along with a command-generation and direct execution feedback loop ( _Act_ ), RapidPen systematically scans services, identifies viable attack vectors, and executes targeted exploits in a fully automated manner. 

In our evaluation against a vulnerable target from the Hack The Box platform, RapidPen achieved shell access within 200–400 seconds at a per-run cost of approximately $0.3– $0.6, demonstrating a **60% success rate** when reusing prior “success-case” data. These results underscore the potential of truly autonomous pentesting for both security novices and seasoned professionals. Organizations without dedicated security teams can leverage RapidPen to quickly identify critical vulnerabilities, while expert pentesters can offload repetitive tasks and focus on complex challenges. Ultimately, our work aims to make penetration testing more accessible and costefficient, thereby enhancing the overall security posture of modern software ecosystems. 

---

## **1 Introduction** 

> **Section Summary:** Penetration testing (pentesting) typically begins with its most critical and challenging phase: _initial infiltration_ of a target system.


Penetration testing (pentesting) typically begins with its most critical and challenging phase: _initial infiltration_ of a target system. Once an attacker—or in this case, a testing platform—gains an initial foothold, subsequent _post-exploitation_ tasks such as privilege escalation, credential theft, lateral movement, and data exfiltration become significantly more feasible. Although the initial foothold phase in penetration testing is challenging, preventing _all_ infiltration attempts is 

equally daunting, especially given the risks posed by zero-day exploits and social engineering. Consequently, it is essential to assess post-exploitation risks under the realistic assumption that a compromise may occur. The faster a testing process can confirm initial access, the more effectively it can allocate time to deeper post-exploitation stages before “running out of clock.” 

Despite advances in automation, fully autonomous solutions for identifying initial compromise vectors remain elusive. In many cases, sophisticated pentesting still demands substantial human expertise, time, and cost. Recent advancements in large language models (LLMs) have driven progress in automating pentesting tasks, such as vulnerability scanning and post-exploitation. However, the _initial-access_ phase has received comparatively less attention. Existing approaches that incorporate LLMs often rely on a _human-in-the-loop_ to validate generated scans and exploits or to guide testing when ambiguities arise [6]. While this approach may suit seasoned pentesters, it presents a significant barrier for software developers and system operators with limited security expertise, who may struggle to evaluate or refine the LLM’s recommendations. Moreover, prior research has identified two key challenges to full automation [26]: the vast search space of potential entry points and the highly target-specific nature of exploits. 

In this work, we focus on _IP-to-Shell_ testing: given only a target IP address, an autonomous system must obtain a shell without human intervention. Our goal is to develop a high-speed, low-cost solution that significantly simplifies penetration testing for both security professionals and nonspecialists alike. 

---

## **Research Questions (RQs)** 

Comparing highly skilled human penetration testers with existing _human-in-the-loop_ systems [6], we hypothesize that two key design choices can facilitate autonomous, robust, and efficient initial infiltration: 

**RQ1:** _Can reusing “success cases” (i.e., past experiences_ 


_with successful scans and exploit paths) enhance the speed and reliability of initial-access automation?_ 

- **RQ2:** _Does iterative command refinement—where the system analyzes failures and regenerates commands until successful—result in a higher probability of exploitation success?_ 

Building on these ideas, we propose an LLM-based pentesting agent, _RapidPen_ , which requires no human intervention beyond specifying a single target IP [15]. We further broaden the scope of our investigation by posing the following research questions: 

- **RQ3:** _How does the time-to-compromise achieved by RapidPen compare to that of a skilled human pentester?_ 

- **RQ4:** _How do the automation costs (in dollars per test) compare to manual penetration testing? Are they low enough to make automated solutions widely practical?_ 

---

## **Contributions and Scope** 

> **Section Summary:** While our system is still in the early stages of development, we validate the feasibility of fully automated IP-to-Shell exploitation on a vulnerable target from the Hack The Box (HTB) platform [1].


While our system is still in the early stages of development, we validate the feasibility of fully automated IP-to-Shell exploitation on a vulnerable target from the Hack The Box (HTB) platform [1]. Specifically, we achieve: 

- A **60% success rate** when leveraging past “success-case” data for the same class of vulnerability; 

- Typical end-to-end compromise in **200–400 seconds** ; 

- A per-run cost of only **$0.3–$0.6** to conduct a fully automated test. 

These promising results support our hypotheses regarding the benefits of success-case knowledge ( **RQ1** ) and iterative command refinement ( **RQ2** ). We also provide a preliminary analysis relevant to **RQ3** and **RQ4** , comparing automated testing speed and cost with expert-driven testing. 

While RapidPen is designed to support organizations with limited security expertise, it is not exclusively intended for teams without dedicated security staff. We also envision its adoption by security teams and professional penetration testers, enabling them to offload straightforward assessments to RapidPen and focus their efforts on more complex, highvalue testing scenarios. Like many other LLM-based penetration testing automation tools, RapidPen primarily achieves its objectives by flexibly leveraging existing knowledge. However, human expertise remains crucial for identifying novel vulnerabilities that are not yet documented or well understood. 

By providing a solution that benefits security-conscious organizations and industries with minimal prior expertise in penetration testing, we aim to enhance the overall security posture of modern software ecosystems. 

**Paper Outline.** This paper is structured as follows: Section 2 reviews the fundamentals of penetration testing and the evolving landscape of AI-driven automation. Section 3 defines our threat model, scope, and assumptions, clarifying RapidPen’s operational boundaries. Section 4 presents the high-level architecture of RapidPen, including its ReActbased modules and retrieval-augmented workflow. Next, Section 5 details our prototype implementation and core technical choices. Section 6 describes our experimental setup and discusses the results of testing RapidPen on a vulnerable target. Finally, Section 9 summarizes the key findings and outlines future directions for enhancing RapidPen’s capabilities and impact. 

---

## **2 Background and Motivation** 

---

## **2.1 Overview of Penetration Testing** 

> **Section Summary:** Penetration testing (pentesting) is a structured process for identifying and validating vulnerabilities in systems and networks before malicious actors can exploit them.


Penetration testing (pentesting) is a structured process for identifying and validating vulnerabilities in systems and networks before malicious actors can exploit them. It typically involves multiple phases, which align with well-known frameworks such as the Penetration Testing Execution Standard (PTES) [21] or the MITRE ATT&CK model [5]. Although different organizations may use slightly varying terminology, a common workflow includes: 

- **Reconnaissance (Recon)** – Gathering preliminary information about the target, such as domain names, IP address ranges, and publicly available data. Effective reconnaissance can guide subsequent actions by identifying potential entry points. 

- **Scanning (Enumeration)** – Conducting deeper, often automated probes on discovered services, ports, and configurations. Tools like nmap can identify vulnerabilities or anomalies. 

- **Exploitation (Initial Access)** – Leveraging discovered weaknesses to gain unauthorized access. This phase is often the most challenging and high-stakes, as it determines whether an attacker can _successfully_ compromise the system. 

- **Post-Exploitation** – Once an initial foothold is obtained, security testers (or adversaries) may escalate privileges, move laterally, and explore deeper layers of the environment to assess the impact of a breach. 

Penetration testing plays a crucial role in cybersecurity: rigorous simulated attacks can expose complex weaknesses that static code analysis or automated scanners might overlook. By emulating real-world threats, pentesters help organizations prioritize remediation efforts and improve their overall security posture. overall security posture of modern software ecosystems. 


---

## **2.2 LLM-Driven Automation in General** 

In recent years, large language models (LLMs) have rapidly advanced in both capability and scope, enabling significant progress in automating a wide range of tasks, including natural language processing, programming assistance, and more. Early breakthroughs include transformer-based architectures such as **BERT** [7], **GPT-2/3** [18, 2], and **T5** [19], which collectively demonstrated how pre-trained models could perform text classification, summarization, and translation with minimal fine-tuning. Subsequent models like **LaMDA** [25] and **GPT-4** [16] have further increased parameter counts and the sophistication of emergent behaviors, allowing for more complex and context-aware interactions. 

These advances have driven adoption across various application domains: 

- **Text Summarization and Translation.** LLMs trained on large corpora can generate concise summaries of lengthy documents and translate text between multiple languages, often surpassing traditional systems [2, 19]. 

- **Code Generation and Debugging.** Models such as Codex [3] can generate scaffolding code, unit tests, or entire functions from natural language descriptions, accelerating software development and improving productivity. Research also explores the use of LLMs for debugging and static analysis to identify potential software vulnerabilities. 

- **Task Planning and Reasoning.** Recent advancements integrate symbolic and factual reasoning with language models, facilitating tasks such as chain-of-thought prompting [12] and multi-step planning [29]. These improvements enable structured decision-making in scenarios requiring multi-step execution and complex logic. 

Since LLMs essentially learn a broad “prior” from largescale text corpora, they can be adapted for novel tasks through well-crafted prompts. This _prompt engineering_ paradigm significantly lowers the barrier to automating domain-specific workflows, including cybersecurity-related tasks. Notably, LLMs can parse tool outputs, synthesize commands, and adjust actions based on prior responses, making them particularly well-suited for penetration testing scenarios requiring multi-step, context-aware orchestration. 

---

## **2.3 Existing Research and Opportunities for Improvement** 

> **Section Summary:** Recent research has explored the application of LLMs to automate various penetration testing tasks, from initial access to remediation.


Recent research has explored the application of LLMs to automate various penetration testing tasks, from initial access to remediation. For example, **PentestGPT** [6] introduces an LLM-based framework for guided exploitation using a task-tree architecture, while **PenHeal** [11] focuses on vulnerability discovery and mitigation strategies. Tools such 

as **BLADE** [24] and **AutoAttacker** [28] extend automation into post-exploitation, and **Wintermute** [9] highlights autonomous Linux privilege escalation. 

Despite these advancements, a key gap remains in achieving _fast, fully automated initial infiltration_ . To date, most approaches still rely on _human-in-the-loop_ validation or focus primarily on post-exploitation rather than providing a highspeed, end-to-end framework for breaching a target. From a software development and operations perspective, the critical questions are often, “Can my system be infiltrated, and how quickly can that happen?” Delivering an _IP-to-Shell_ workflow at practical speed and cost could provide significant value to a broader audience, including security-conscious organizations and industries lacking dedicated security teams. 

In the following sections, we introduce an approach to address this need. By focusing on the initial-access phase and aiming for fully automated, low-cost, high-speed penetration testing, our work seeks to enhance overall cybersecurity and enable a wider range of users to incorporate real-world adversarial testing into their development processes. 

---

## **3 Threat Model and Problem Definition** 

---

## **3.1 Threat Model** 

> **Section Summary:** The RapidPen agent is assumed to have minimal prior knowledge of the target system:


The RapidPen agent is assumed to have minimal prior knowledge of the target system: 

- **Target IP Only.** The attacker (i.e., RapidPen) is provided only with the IP address of the machine under test, without additional configuration details or vulnerability disclosures. 

- **Shell Acquisition.** In its current prototype, RapidPen exploits vulnerabilities using the Metasploit Framework [20] (msfconsole) and considers a shell “obtained” once logs confirm that a reverse shell has been successfully established. 

---

## **3.2 Assumptions** 

> **Section Summary:** RapidPen operates under the assumption that it can establish TCP connections to the target system’s IP address.


RapidPen operates under the assumption that it can establish TCP connections to the target system’s IP address. If necessary, an OpenVPN configuration file can be deployed within the RapidPen environment to enable VPN-based connectivity. Beyond these basic networking requirements, no additional external services or credentials are assumed. 

---

## **3.3 Scope and Limitations** 

> **Section Summary:** - **Pre-Scanning Recon Excluded.** Passive reconnaissance steps, such as searching domain records or metadata leaks, are beyond the scope of this study.


- **Pre-Scanning Recon Excluded.** Passive reconnaissance steps, such as searching domain records or metadata leaks, are beyond the scope of this study. Instead, we focus on active port scanning as the starting point. 


- **No Post-Exploitation.** RapidPen does not attempt privilege escalation or lateral movement once a shell is acquired. 

- **No Web-Based Attacks.** Although web vulnerabilities can serve as entry points, the current system does not address them. Future work will explore extending RapidPen to support web exploits. 

- **No UDP-Based Attacks.** This implementation is limited to TCP-based targeting. UDP-based exploits and scans are not considered in this study. 

---

## **4 Design Overview of RapidPen** 

> **Section Summary:** In this section, we describe the overall architecture of our fully automated penetration testing framework, referred to as RapidPen.


In this section, we describe the overall architecture of our fully automated penetration testing framework, referred to as RapidPen. We adopt the _ReAct_ [29] paradigm, which consists of a _Re_ (task planning) module and an _Act_ (command execution) module, both supported by specialized _retrievalaugmented generation (RAG)_ [13] repositories. Below, we detail the system architecture, how each module interacts, and how failures are handled. 

---

## **4.2 PTT as a Core Data Model in the** **_Re_ Module** 

In prior work on **PentestGPT** [6], the concept of a _Pentesting Task Tree_ (PTT) was introduced to structure the entire penetration testing process as an _attributed tree_ , where each node represents a task (e.g., port scanning, vulnerability testing, exploitation), and edges define the flow of reasoning or dependencies between tasks. The tree evolves dynamically as new tasks are generated, completed, or require backtracking due to partial failures. 

**PTT Definition (from PentestGPT).** A PTT is essentially a labeled tree (or attributed polytree) with the following key elements: 

1. **Nodes (tasks)** with unique identifiers and optional child nodes. 

2. **Attributes** assigned to each node, such as task descriptions, current statuses, and relevant parameters. 

3. **Edges** representing parent-child relationships (e.g., subtask expansions) that structure the penetration testing workflow at multiple levels of detail. 

---

## **4.1 System Architecture** 

> **Section Summary:** Figure 1 provides a high-level overview of RapidPen’s core components.


Figure 1 provides a high-level overview of RapidPen’s core components. 

- **Input** : The user provides the _target IP address_ . 

- **Output** : RapidPen-vis displays penetration test progress (e.g., logs, discovered vulnerabilities) and generates the final reports, including the command used to obtain a shell. 

- **Re and Act Modules** : These modules jointly implement the ReAct loop, coordinating tasks and executing commands. 

- **RapidPen-vis** : A separate visualization tool for monitoring intermediate processes and final reports. [15] 





**Our Extensions.** We integrate the PTT as the _core data model_ in the _Re_ (reasoning) module to structure and coordinate tasks. In addition to the standard PentestGPT functionality, we introduce the following enhancements: 

1. **Environment Metadata.** Our PTT includes a dedicated metadata block capturing details about the penetration testing environment (e.g., attacker and target IP addresses, time stamps, test status). 

2. **Act Results in Nodes.** Each task node maintains a history of command executions, including the executed command string, exit_code, exit_class, and a brief log summary. This allows for a clearer interplay between the _Act_ module outputs and the _Re_ module’s reasoning state. 

3. **JSON-based I/O.** We consistently store and exchange the PTT in JSON format, ensuring that the LLM operates within a strict schema. This prevents ambiguity or “hallucination” when the LLM appends new tasks or updates existing nodes. A simplified JSON schema is provided in Listing 1. 

Listing 1: Simplified PTT snippet with environment metadata, subtask structure, and Act results. 

Figure 1: The high-level architecture of RapidPen, illustrating user inputs and outputs, the _Re_ and _Act_ modules, and RapidPen-vis, a visualization tool for monitoring intermediate processes and final reports. 

1 { 2 "version": "2" , 3 "metadata": { 4 "started_at": "2025-02-13T22:01:52Z" , 


5 "finished_at": "2025-02-13T22:08:00Z" , 6 "status": "SUCCESS" , 7 "attacker": { "LHOST": "10.10.14.22" } , 8 "target": { 9 "description": "HTB Blue machine" , 10 "RHOST": "10.10.10.40" 11 } 12 } , 13 "root": { 14 "id": "1" , 15 "title": "Reconnaissance" , 16 "act_results": [{ 17 "command": "(omit)" , 18 "timeout_sec": 60 , 19 "exit_code": 0 , 20 "exit_class": "SUCCESS" , 21 "log_summary": "(omit)" 22 }] , 23 "subtasks": [ 24 ... 25 ] 26 } 27 } 

---

## **4.3 Layered ReAct Modules in RapidPen** 

> **Section Summary:** RapidPen’s execution logic follows the _ReAct_ [29] paradigm, where:


RapidPen’s execution logic follows the _ReAct_ [29] paradigm, where: 

1. **Re (Task Planning):** Monitors current logs, prior task outcomes, and “success-case” data to propose new tasks or exploit paths. 

2. **Act (Command Execution):** Issues commands to gather information or launch attacks. Upon receiving logs, the system refines or regenerates commands before feeding outcomes back to _Re_ . 

Figures 2–4 illustrate how the _Re_ module is divided into submodules, while Figure 5 details the _Act_ module’s workflow. 


*(Image omitted: Refer to paper)*



*(Image omitted: Refer to paper)*


Figure 2: The _Re_ module in RapidPen consists of the _Re (L1) PTT Planner_ and _Re (L1) PTT Prioritizer_ submodules. The PTT Planner is responsible for expanding and maintaining the PTT tree, while the PTT Prioritizer determines the next task to execute. 


*(Image omitted: Refer to paper)*



*(Image omitted: Refer to paper)*



*(Image omitted: Refer to paper)*


Figure 3: The _Re (L1) PTT Planner_ processes the command results from the last executed task to generate new tasks at Level 2 (L2) in the PTT. These tasks are deduplicated using an LLM-based approach before being merged into the PTT, updating it from an old to a new state. 


*(Image omitted: Refer to paper)*



*(Image omitted: Refer to paper)*



*(Image omitted: Refer to paper)*


Figure 4: The _Re (L2) New Task Generation_ module generates new tasks based on historical success cases. The process begins by extracting command results from the last executed task. An LLM queries relevant historical success cases, which are then analyzed to extract key insights. Based on this analysis, new tasks are generated and integrated into the planning process. 


*(Image omitted: Refer to paper)*


Figure 5: The _Act (L1)_ module processes runnable tasks through three key stages: command generation, execution, and log analysis. It leverages offensive security expertise to generate commands, automates execution, and applies selfcorrecting mechanisms when necessary. Successful executions produce a command result, while failed executions trigger a feedback loop for improvement. 

---

## **4.4 RAG for Offensive Security** 

While _ReAct_ provides a general “reasoning–acting” pattern, RapidPen enhances this approach with two specialized _Retrieval-Augmented Generation (RAG)_ repositories for domain-specific commands and proven exploit steps: 


1. **Act (L1) Command Generation RAG:** A curated collection of 148 Markdown files from **HackTricks** [4], primarily focused on “Network Services Pentesting” (e.g., SMB, FTP, SSH). These documents provide typical scan commands, exploit techniques, and enumeration strategies relevant to the initial-access phase. The Command Generation module references these documents to generate commands via the LLM. 

2. **Re (L2) New Tasks (Success Cases) RAG:** PTTs in JSON format capturing successful pentesting sequences. Currently, this dataset includes two PTTs for the Blue machine in Hack The Box [1]. Each file outlines step-bystep instructions, from scanning to obtaining a shell. The New Tasks (Success Cases) module generates a search query for the RAG based on the results of the most recent task execution. It then analyzes the retrieved PTT output to generate effective subtasks. 

---

## **4.5 Feedback Cycle in Act Module** 

> **Section Summary:** Figure 5 illustrates the feedback loop within the _Act_ module, where command generation and execution are tightly coupled with log analysis and error handling.


Figure 5 illustrates the feedback loop within the _Act_ module, where command generation and execution are tightly coupled with log analysis and error handling. After executing each command, the system interprets the outcome (e.g., SUCCESS, TIMEOUT, COMMAND_NOT_FOUND) and determines whether to retry or escalate. The feedback loop follows these key policies: 

1. **Three-Strike Retry Limit.** When commands are generated and executed in a cycle, the Log Analysis module evaluates the logs to determine if the result is conclusive. If the command fails or does not produce sufficient evidence for further progress, the _Act_ module refines or regenerates the command and re-executes it. This cycle repeats up to three times. If no success is achieved after three attempts, RapidPen marks the corresponding task as _failed_ and reports this outcome to the _Re_ module. 

2. **Handling Timeouts.** In some cases, command execution may hang indefinitely if the target server is unresponsive. To prevent this, each command is assigned an initial timeout (e.g., 30 seconds). When a TIMEOUT occurs, the next execution cycle begins with _Act (L1) Command Generation_ searching for a faster alternative command. For example, it may replace an nmap port scan command with rustscan for quicker execution. If no faster alternative exists, the system doubles the timeout threshold to allow more time for execution. 

3. **Handling Missing Commands or Files.** Since _Act (L1) Command Generation_ references HackTricks and other sources, it may propose commands or reference files that are not available in the _Act (L1) Command Executor_ environment. In such scenarios, COMMAND_NOT_FOUND 

or FILE_NOT_FOUND errors occur. Upon detecting these, RapidPen employs a _fail-fast_ strategy: it terminates the current penetration test session and notifies the developer. The rationale is that an external installation or environment fix is required before continuing, and automated retries would be ineffective. 

---

## **5 Implementation** 

> **Section Summary:** This section describes the prototype implementation of RapidPen.


This section describes the prototype implementation of RapidPen. While Chapter 4 presented the overall design, here we focus on the specific tools, infrastructure, and configurations used to realize our fully automated pentesting workflow. 

---

## **5.1 Prototype Setup and LLM Usage** 

> **Section Summary:** Currently, RapidPen exists as a **prototype** implementation built on top of Dify<sup>1</sup> .


Currently, RapidPen exists as a **prototype** implementation built on top of Dify<sup>1</sup> . We run Dify locally to manage interactions with multiple Large Language Model (LLM) endpoints. Additionally, we integrate LangSmith<sup>2</sup> with Dify to precisely measure and monitor LLM invocation costs. This setup enables tracking of API calls, token usage, and associated costs under realistic testing conditions. 

Our system exclusively employs OpenAI’s gpt-4o [17] as the underlying language model. Internally, we maintain **10 LLM instances** dedicated to the _Re_ module (task planning and reasoning) and **8 LLM instances** for the _Act_ module (command generation and log analysis). Initially, some prompts were adapted from **PentestGPT** [6]; however, all prompts have since been replaced with original designs. 

---

## **5.2 RapidPen-vis** 

> **Section Summary:** For visualization and reporting, we provide _RapidPen-vis_ , consisting of:


For visualization and reporting, we provide _RapidPen-vis_ , consisting of: 

- **Server-Side:** A Python Flask application responsible for rendering real-time test logs and final pentest summaries. 

- **Client-Side:** A lightweight **vanilla JavaScript** frontend that communicates with the Flask API to fetch and display pentesting progress graphically. 

This interface allows operators to observe the automated exploit process, review execution logs, and track the overall state of penetration testing tasks. 

---

## **5.3 Custom Dify-Sandbox** 

> **Section Summary:** Dify provides a secure Python execution environment called _Dify-Sandbox_ , which restricts system calls and external network access within a controlled Docker container.


Dify provides a secure Python execution environment called _Dify-Sandbox_ , which restricts system calls and external network access within a controlled Docker container. However, 


*(Image omitted: Refer to paper)*


> 2https://smith.langchain.com/ 


our _Act (L1) Command Executor_ requires broader system access to execute real-world pentesting commands. To address this limitation, we implemented a custom Docker image that maintains the same REST API interface as _Dify-Sandbox_ , but without restrictive sandbox policies. This customized container is integrated into our docker compose setup as a direct replacement for the official Dify-Sandbox. It processes the same API calls for command execution while permitting the necessary system calls and network interactions required for pentesting. 

By leveraging this custom sandbox implementation, we maintain compatibility with Dify’s workflow and Python execution mechanism while removing constraints that would otherwise prevent valid pentesting operations. This dual approach ensures that our local environment remains modular and extensible, allowing for future experiments and improvements in pentest automation. 

**Attacker Environment.** We executed the RapidPen orchestrator and _RapidPen-vis_ on a local MacBook Pro (13-inch M2, 24 GB RAM, macOS Sequoia 15.3.1). The _Dify_ -based RapidPen orchestration runs in Docker containers, including our custom sandbox for actual command execution. 

### **6.2.1 Testing Two Configurations** 

To evaluate the impact of _Re (L2) New Tasks (Success Cases) RAG_ , we conducted two sets of experiments: 

- **With Success Cases Enabled (Runs #1–10):** The system had access to a stored PTT reflecting successful exploitation steps on HTB “Blue” (which shares the MS17-010 vulnerability). 

- **Without Success Cases (Runs #11–20):** The system relied solely on scanning and standard exploit references, without leveraging pre-recorded successful sequences. 

---

## **6 Evaluation** 

This section presents preliminary experiments on the _Legacy_ machine from Hack The Box [1], designed to validate RapidPen’s ability to establish an initial foothold (IP-to-Shell) in an early-stage prototype. Future work will extend these experiments to a broader set of targets. 

---

## **6.1 Objectives and Questions** 

> **Section Summary:** Our evaluation seeks to answer the following key questions:


Our evaluation seeks to answer the following key questions: 

1. **Success Rate:** How often does RapidPen successfully achieve initial access (shell) on a known vulnerable machine? 

For each run, we reset the environment, then launched RapidPen with a single target IP. We recorded the following metrics: 

- **Outcome:** _Success_ (obtained a shell) or _Failure_ . 

- **#Steps:** Number of PTT expansions initiated by the _Re (L1) PTT Planner_ , from start to success/failure. 

- **Elapsed Time:** Total wall-clock time from test initiation to termination. 

---

## **6.3 Results** 

### **6.3.1 Overall Success Rates and Timings** 

2. **Time and Bottlenecks:** How long does an average run take, and which modules in RapidPen consume the most time? 

3. **LLM Cost:** What is the cost of an automated penetration test in terms of LLM usage? 

4. **Behavioral Insights:** How does the feedback mechanism in the _Act_ module (cf. Section 4.5) function in practice, and what role does the _Re (L2) New Tasks (Success Cases) RAG_ (cf. Section 4.4) play in generating effective exploit paths? 

---

## **6.2 Experimental Setup** 

> **Section Summary:** **Target Machine (HTB Legacy).** We selected the Hack The Box “Legacy” machine as our primary target.


**Target Machine (HTB Legacy).** We selected the Hack The Box “Legacy” machine as our primary target. This machine features an older SMB server exposed on tcp/445 with the MS17-010 (EternalBlue) vulnerability, enabling remote code execution (RCE). 

**With Success Cases (#1–10).** In the left column of Figure 6, we observe that **6 out of 10** runs successfully achieved a shell on the Legacy machine. Runs that failed tended to get stuck in repeated enumerations or timed out when nmap scanning did not produce conclusive results quickly. When the test succeeded, execution time ranged from 200–400 seconds, with a moderate correlation between the number of steps and elapsed time. 

**Without Success Cases (#11–20).** In contrast, the right column of Figure 6 presents a less favorable outcome. The system succeeded in only **3 out of 10** runs. We also observed more outlier runs that either timed out after multiple scanning attempts or executed redundant exploit attempts. For instance, Run #13 followed an excessively long sequence of unsuccessful attack vectors. Consequently, the average failure time was significantly higher, occasionally exceeding 400 seconds. When an exploit succeeded, execution time was typically below 350 seconds. 



*(Image omitted: Refer to paper)*



*(Image omitted: Refer to paper)*



*(Image omitted: Refer to paper)*



*(Image omitted: Refer to paper)*


Figure 6: Impact of _Re (L2) New Tasks (Success Cases)_ on Penetration Testing Efficiency. The left column (yellow) represents runs with **Success Cases enabled** , while the right column (green) represents runs **without Success Cases** . **Top Row:** Elapsed time (in seconds) per run. Runs with Success Cases tend to complete faster, while runs without them exhibit greater variance and some failures exceeding 1200 seconds (forcefully terminated). **Bottom Row:** Number of steps taken (PTT expansions) before success or failure. Runs without Success Cases often require more steps, indicating inefficient task selection. The vertical dashed line separates **successful** and **failed runs** , highlighting that the **failure rate is higher without Success Cases (3/10 success) compared to with Success Cases (6/10 success)** . 

### **6.3.2 Observations and Discussion** 

The presence of _Success Cases_ significantly improved the success rate, as the Legacy machine shares the same SMBv1 vulnerability exploited by HTB “Blue.” Although the exact environment differs slightly, the fundamental MS17-010 exploit steps stored in the PTT closely align with the real target’s requirements. For more diverse vulnerabilities, we expect a lower direct transferability of RAG data; however, we anticipate that it will still accelerate the identification of effective enumeration and exploitation paths. 

- **Task Steps vs. Time:** Runs with fewer steps generally completed faster. 

### • **Failure Causes:** 

1. Runs #1, #16, #18, and #20: _Act (L1) Command Generation_ produced smbclient commands with incorrect parameters, resulting in COMMAND_NOT_FOUND, FILE_NOT_FOUND, and OTHERS errors. 

   2. Runs #4, #6, and #17: _Act (L1) Command Generation_ generated inappropriate commands for the given tasks, leading to OTHERS, FILE_NOT_FOUND, and COMMAND_NOT_FOUND errors. 

   3. Run #9: _Act (L1) Command Execution_ failed to execute the enum4linux command on port 139. _Act (L1) Log Analysis_ classified it as an OTHERS error, triggering the fail-fast mechanism. 

   4. Run #13: The system continuously attempted to exploit port 139. After exceeding 1200 seconds, execution in Dify stalled. 

   5. Run #14: _Re (L1) PTT Prioritizer_ generated a hallucinated non-leaf task in the PTT, causing a validation error in the _Act_ module. 

- **Future Generalization:** We plan to extend testing to machines with partially overlapping but not identical vulnerabilities to assess how well the success-case RAG generalizes. 



*(Image omitted: Refer to paper)*


Figure 7: Module-wise breakdown of elapsed time per run with _Re (L2) New Tasks (Success Cases)_ enabled. Each bar represents the total execution time for a single run, with different colors indicating each module’s contribution. _Re (L1) PTT Planner_ (red) accounts for a significant portion of the total time, followed by _Act (L1) Command Execution_ (blue). 


*(Image omitted: Refer to paper)*


Figure 8: Module-wise breakdown of LLM cost per run with _Re (L2) New Tasks (Success Cases)_ enabled. Each bar represents the total LLM cost (in USD) for a single run, with different colors indicating the cost contribution of each module. _Re (L1) PTT Planner_ (red) incurs the highest cost, followed by _Act (L1) Command Execution_ (blue) and _Act (L1) Log Analysis_ (purple). 

---

## **6.4 Module-Wise Time and Cost Breakdown** 

> **Section Summary:** Listing 2: Input to _Re (L2) New Tasks (Success Cases)_ in Legacy <u>(last executed task)</u>


Listing 2: Input to _Re (L2) New Tasks (Success Cases)_ in Legacy <u>(last executed task)</u> 

To gain deeper insights, we instrumented the runs (particularly in the _with Success Cases_ scenario) to measure each module’s contribution to the total runtime and LLM costs. 

1 { 2 "id": "1.3.1.4" , 3 "title": "Enumerate services on port 445" , 4 "detail": "Use Nmap to enumerate the _�→_ service running on port 445 on _�→_ 10.10.10.4. Check for SMB _�→_ vulnerabilities such as _�→_ EternalBlue." , 5 "status": "completed" , 6 "act_results": [ 7 { 8 "command": "nmap -p 445 -vv -Pn _�→_ --script= _�→_ smb -vuln -cve2009 -3103.nse , _�→_ smb -vuln -ms06 -025.nse , _�→_ smb -vuln -ms07 -029.nse , _�→_ smb -vuln -ms08 -067.nse , _�→_ smb -vuln -ms10 -054.nse , _�→_ smb -vuln -ms10 -061.nse , _�→_ smb -vuln -ms17 -010.nse _�→_ 10.10.10.4" , 9 "timeout_sec": 30 , "exit_code": 0 , "exit_class": "SUCCESS" , "log_summary": "TCP port 445 on 

The runtime breakdown (see Figure 7) indicates that _Act (L1) Command Execution_ contributes the most to total execution time, followed by _Re (L1) PTT Planner_ . 

Next, we analyze the LLM cost distribution (see Figure 8). _Re (L1) PTT Planner_ dominates the cost due to frequent PTT expansions and the overhead of merging newly generated subtasks from _Re (L2) New Tasks (Success Cases)_ . 

The current cost and execution time are practical for targeted penetration testing scenarios. However, further optimization is possible by reducing large PTT inputs (which can sometimes exceed 14KB) to the LLM and improving error-handling mechanisms. 

---

## **6.5 Behavioral Insights** 

> **Section Summary:** **Act Feedback Examples.** As described in Section 4.5, the _Act_ module attempts to recover from command failures by either adjusting parameters or switching to alternative tools.


**Act Feedback Examples.** As described in Section 4.5, the _Act_ module attempts to recover from command failures by either adjusting parameters or switching to alternative tools. In 9 multiple runs, we observed that when an nmap scan timed out, 10 it was immediately replaced with rustscan. Additionally, 11 when an exploit attempt using msfconsole timed out, the 12 system generally did not find an alternative command and instead increased the timeout from 30 to 60 seconds before re-executing the command. 

- _�→_ 10.10.10.4 is open , and the _�→_ following vulnerabilities have _�→_ been detected: MS08 -067 _�→_ (CVE -2008 -4250), MS17 -010 _�→_ (CVE -2017 -0143)." 

**Role of Re (L2) New Tasks (Success Cases).** Section 4.4 13 introduced the _New Tasks (Success Cases) RAG_ , where Rapid14 Pen references a stored success PTT from HTB “Blue.” 15 

} ] , ... 




16 } 36 "detail": "Attempt to exploit the _�→_ identified MS17 -010 When the last executed task from Listing 2 is passed to _�→_ vulnerability on port 445 _Re (L2) New Tasks (Success Cases)_ , a query is generated _�→_ of 10.10.10.40 using for the _New Tasks (Success Cases) RAG_ : "Metasploit SMB _�→_ Metasploit. Set RHOST to exploit port 445 empty credentials". This retrieves _�→_ 10.10.10.40 , RPORT to 445, the stored success-case PTT from the HTB Blue machine _�→_ and LHOST to 10.10.14.22." , (Listing 3). 37 "status": "completed" , 38 "act_results": [{ Listing 3: Success Case (PTT JSON) from the Blue machine 39 "command": "msfconsole -q -x 1 { _�→_ 'use exploit/ windows/ 2 "version": "2" , _�→_ smb/ 3 "metadata": { _�→_ ms17_010_eternalblue:
- set 4 "started_at": "2025-02-13T22:17:00Z" , _�→_ RHOST 10.10.10.40
- set 5 "finished_at": "2025-02-13T21:23:00Z" , _�→_ RPORT 445
- set LHOST 6 "status": "SUCCESS" , _�→_ 10.10.14.22
- exploit '" , 7 "attacker": { 40 "timeout_sec": 60 , 8 "LHOST": "10.10.14.22" 41 "exit_code": 0 , 9 } , 42 "exit_class": "SUCCESS" , 10 "target": { 43 "log_summary": "Port 445 on 11 "description": "HTB Blue machine" , _�→_ 10.10.10.40 is vulnerable 12 "RHOST": "10.10.10.40" _�→_ to MS17 -010. Windows 7 13 } _�→_ Professional 7601 Service 14 } , _�→_ Pack 1 x64 was 15 "root": { _�→_ identified , and a 16 ... _�→_ Meterpreter session was 17 { _�→_ established." 18 "id": "1.3.1.3" , 44 }] , 19 "title": "Enumerate services on port 45 "subtasks": [] _�→_ 445" , 46 } 20 "detail": "Use Nmap to enumerate the 47 ] _�→_ service running on port 445 on 48 ... _�→_ 10.10.10.40. Check for SMB 49 } _�→_ vulnerabilities such as 21 "status" _�→_ EternalBlue.": "failed" , , _Tasks (Success Cases)_ Based on the success case from HTB Blue, the LLM generated the following output: LLM generated the following output: _Re (L2) New_ 22 "act_results": [ 23 { Listing 4: Generated new tasks from Success Cases PTT. 24 "command": "nmap -p 445 -vv -Pn 1 { _�→_ --script= 2 "Thought process (Step1)": "First , check _�→_ smb -vuln -ms17 -010.nse _�→_ whether a success -case task tree _�→_ 10.10.10.40" , _�→_ exists. The provided data contains 25 "timeout_sec": 30 , _�→_ a success -case task tree , so 26 "exit_code": 0 , _�→_ proceed to the next step." , 27 "exit_class": "SUCCESS" , 3 "Thought process (Step2)": "Find a task 28 "log_summary": "Port 445 on _�→_ in the success -case task tree _�→_ 10.10.10.40 is open , and _�→_ similar to the most recent executed _�→_ the Microsoft SMBv1 server _�→_ task. In this case , the latest task _�→_ has a remote code execution _�→_ involves port 445, and the _�→_ vulnerability (MS17 -010, _�→_ success -case task tree also _�→_ CVE -2017 -0143)." _�→_ contains detailed information about 29 } , _�→_ port 445. Specifically , task ID 30 ... _�→_ '1.3.1.3 ' and its subtasks are 31 ] , _�→_ related to port 445. Based on 32 "subtasks": [ _�→_ these , generate new tasks." , 33 { 4 "newTasks": [ 34 "id": "1.3.1.3.1" , 5 { 35 "title": "Exploit SMBv1 6 "title": "Exploit SMBv1 Vulnerability _�→_ Vulnerability MS17 -010" , _�→_ MS17 -010" ,

_Re (L2) New Tasks (Success Cases)_ Based on the success case from HTB Blue, the LLM generated the following output: LLM generated the following output: 



*(Image omitted: Refer to paper)*


<!-- Start of picture text -->
7 "detail": "Attempt to exploit the<br>�→ identified MS17 -010<br>�→ vulnerability on port 445 of<br>�→ 10.10.10.4 using Metasploit.<br>�→ Set RHOST to 10.10.10.4 , RPORT<br>�→ to 445, and LHOST to<br>�→ 10.10.14.22." ,<br>8 "origin": {<br>9 "reason": "The previous check<br>�→ confirmed the presence of<br>�→ MS17 -010 vulnerability on<br>�→ port 445, enabling an exploit<br>�→ attempt."<br>10 }<br>11 } ,<br>12 {<br>13 "title": "Verify System Access" ,<br>14 "detail": "After exploiting the SMBv1<br>�→ vulnerability , verify access to<br>�→ 10.10.10.4 by checking for a<br>�→ shell or other indicators of<br>�→ successful exploitation." ,<br>15 "origin": {<br>16 "reason": "Verification is<br>�→ necessary to ensure that the<br>�→ exploit successfully provided<br>�→ access to the target system."<br>17 }<br>18 }<br>19 ]<br>20 }<br><!-- End of picture text -->

By leveraging the success case from the HTB Blue machine, which shares the same vulnerability, the system was able to generate appropriate tasks, demonstrating the effectiveness of using prior success cases for guided penetration testing. 

---

## **6.6 Summary of Findings** 

> **Section Summary:** Our preliminary evaluation indicates that RapidPen can achieve consistent IP-to-Shell exploits on a known vulnerable target:


Our preliminary evaluation indicates that RapidPen can achieve consistent IP-to-Shell exploits on a known vulnerable target: 

- **Success Rate:** 60% with success-case RAG vs. 30% without, across 10 trials each. 

- **Time-to-Shell:** On average, 200–400 seconds for successful runs. 

- **LLM Cost:** Typically under $0.60 per run, with the _Re (L1) PTT Planner_ module contributing the most. 

Though limited to a single machine and vulnerability type, these results demonstrate the _Re (L2) New Tasks (Success Cases)_ approach’s potential and highlight the _Act_ module’s self-correcting behavior. We plan to broaden our scope with additional targets, diverse vulnerabilities, and larger user studies in future work. 

---

## **7 Discussion** 

---

## **7.1 Benefits and Future Directions of the Act Feedback Mechanism** 

> **Section Summary:** The self-reliant feedback cycle implemented in the _Act_ module (Section 4.5) significantly reduces the need for human intervention.


The self-reliant feedback cycle implemented in the _Act_ module (Section 4.5) significantly reduces the need for human intervention. As long as the tasks assigned by the _Re_ module are appropriate, the _Act_ module persistently re-generates and refines commands, interprets resulting logs, and explores alternative strategies when errors occur. This design choice allows RapidPen to continue progressing without manual oversight, enhancing its ability to achieve fully automated penetration testing. 

However, the current fail-fast mechanism employed by the _Act_ module causes the entire process to terminate upon encountering specific errors, such as COMMAND_NOT_FOUND, FILE_NOT_FOUND, and OTHERS. While this approach prevents unnecessary retries and repeated failures, it can also abruptly halt the penetration test in cases where partial remediation—such as installing missing packages or updating outdated command syntax—would suffice. 

Future improvements should modify both _Command Generation_ and _Command Execution_ to address these errors dynamically. A more nuanced error-handling strategy should categorize failures, apply targeted retries or fixes, and reserve immediate termination for cases where it is strictly necessary. Such refinements would further enhance the system’s robustness and adaptability in real-world scenarios. 

---

## **7.2 Advantages and Limitations of Using Success Cases** 

> **Section Summary:** Our experiments indicate that RapidPen’s use of Success Cases accelerates exploit discovery when the target vulnerability closely matches those in previously recorded penetration tests.


Our experiments indicate that RapidPen’s use of Success Cases accelerates exploit discovery when the target vulnerability closely matches those in previously recorded penetration tests. For example, referencing the MS17-010 exploit path from the “Blue” machine on Hack The Box (HTB) was effective against the “Legacy” machine, which shares a similarly vulnerable SMBv1 service. This demonstrates that reusing existing exploit sequences can streamline scanning and exploitation, leading to faster and more reliable outcomes. 

However, handling scenarios where no relevant Success Cases exist remains an open problem. Zero-day vulnerabilities or configurations that have never been encountered may require more advanced reasoning beyond merely “copying” from past success. While our current approach leverages the LLM’s internal knowledge and a RAG-based repository, a more powerful framework for abstracting exploit techniques—enabling RapidPen to discover novel attack strategies—will be essential for addressing unknown threats. Designing and evaluating such a next-generation system is a critical step toward making automated pentesting broadly effective against new or rare vulnerabilities. 


---

## **7.3 Expanding the Attack Surface** 

> **Section Summary:** Although RapidPen currently achieves fully automated IPto-Shell compromises, it does not yet address the postexploitation phase.


Although RapidPen currently achieves fully automated IPto-Shell compromises, it does not yet address the postexploitation phase. Privilege escalation, lateral movement, and deeper analysis of the compromised environment represent logical extensions for future work. In particular, tools like BLADE [24] and AUTOATTACKER [28] already explore AI-assisted post-exploitation. Extending RapidPen to integrate with such frameworks could broaden its applicability, enabling more comprehensive, end-to-end assessments. 

Another important direction involves web exploits, which are currently absent from the system. Web-based vulnerabilities often require specialized knowledge—ranging from injection techniques to authentication bypass methods—and may involve GUI-based testing beyond simple command-line interactions. Incorporating these capabilities would likely require RAG expansions to include relevant web exploitation knowledge bases and potentially adapt the _Act_ module to handle browser automation. Achieving the same degree of autonomy for web exploits poses additional research and engineering challenges. 

---

## **7.4 Ethical and Safety Considerations** 

> **Section Summary:** Although the user explicitly provides a target IP address to RapidPen, reducing the risk of scanning unrelated systems, the possibility of misuse cannot be ignored.


Although the user explicitly provides a target IP address to RapidPen, reducing the risk of scanning unrelated systems, the possibility of misuse cannot be ignored. Any automated exploit tool can be leveraged for malicious purposes if placed in the wrong hands or configured improperly. Future developments should focus on access control, rate-limiting, and formal usage policies—especially if the system transitions from a research prototype to a commercial or open-source deployment. Additionally, practical safeguards like monitoring logs, validating the legitimacy of the target environment, and enforcing strict network boundaries are pivotal for preventing inadvertent attacks against unauthorized hosts. 

Overall, while RapidPen lowers the barrier for automated security testing, it underscores the need for responsible deployment practices. Addressing legal and ethical ramifications is essential to ensuring that the benefits of fully automated pentesting do not come at the expense of broader cybersecurity risks. 

---

## **8 Related Work** 

---

## **8.1 LLM-Based Penetration Testing** 

### **8.1.1 PentestGPT – Task Tree-Driven AI Pentesting** 

Recent research has explored using large language models (LLMs) to automate penetration testing. **PentestGPT** [6] is a notable example: it leverages an LLM (GPT-3.5/GPT-4) to guide the pentest process via a _Pentesting Task Tree (PTT)_ 

structure. Inspired by attack trees, the PTT decomposes engagements into sub-tasks (e.g., port scanning, service enumeration, exploitation), allowing the LLM to maintain context throughout testing. PentestGPT operates using three coordinated modules: a _Reasoning_ module (the "lead tester") that updates the task tree and determines next steps, a _Generation_ module (the "junior tester") that proposes specific commands, and a _Parsing_ module to summarize tool output. 

While PentestGPT automates attack planning, it requires a human-in-the-loop to execute suggested commands and correct errors. Users must review and refine commands before execution, limiting its autonomy. Thus, PentestGPT functions more as a guided assistant rather than a fully autonomous pentesting tool. 

### **8.1.2 Other LLM-Driven Pentesting Tools** 

Beyond PentestGPT, several emerging tools utilize LLMs for penetration testing, each focusing on different aspects of the workflow. These tools can be categorized as follows: 

### **Tools that Automate Initial Access but Focus on Broad Vulnerability Scanning Rather than Speed** 

- **PenHeal** [11] – an AI agent that operates without direct human involvement, designed to identify a broad range of vulnerabilities and propose mitigation strategies. Although the paper does not explicitly confirm automation of initial foothold attacks, it is possible that PenHeal’s capabilities overlap with RapidPen in terms of initial access. However, no evaluation is provided regarding the time and cost required to achieve initial access. In contrast, RapidPen focuses on demonstrating the most immediate security risk—namely, gaining unauthorized shell access as quickly as possible—before handing over control to established tools designed for post-exploitation. While RapidPen does not yet provide broad vulnerability coverage or automated remediation, incorporating such features remains an area for future exploration. 

### **Tools That Focus on Post-Exploitation and Are Complementary to RapidPen** 

- **BLADE** [24] – **B** reaking **L** imits, **A** utomate **D** eep **E** xploitation – an AI-driven pentesting agent built on an autonomous agent framework (Microsoft’s AutoGen [27]). BLADE autonomously orchestrates exploitation tasks by leveraging external tools and dynamic script generation. For example, it uses pre-configured tools like LinPEAS for privilege escalation and John the Ripper for credential cracking to achieve deeper system compromise. Additionally, it includes agents for network scanning and lateral movement, showcasing how multi-agent AI systems can enhance penetration testing workflows. 


- **AutoAttacker** [28] – an LLM-guided system designed to implement automated “hands-on-keyboard” cyberattacks in post-breach scenarios. 

- **Wintermute** [9] – an LLM-driven Linux privilege escalation tool that evaluates model performance in fully automated exploit scenarios. It highlights strengths and weaknesses in autonomous security workflows, focusing on post-exploitation. 

---

## **8.2 Reinforcement Learning-Based Penetration Testing Approaches** 

> **Section Summary:** _Deep reinforcement learning (RL)_ has also been explored for autonomous pentesting.


_Deep reinforcement learning (RL)_ has also been explored for autonomous pentesting. RL-based systems learn attack sequences by interacting with an environment and optimizing for successful exploits. Key contributions include: 

- **Hu et al.** [10] developed a deep RL framework for automated penetration testing, modeling scanning, exploitation, and lateral movement as a reinforcement learning problem. 

- **Garrad and Unnikrishnan** [8] applied RL to vehicular ad-hoc network (VANET) penetration testing, demonstrating AI-driven attack sequence learning. 

- **Liu et al.** [14] proposed a hierarchical RL agent for large-scale network penetration, improving efficiency by splitting attack planning into multiple levels. 

- **DeepExploit** [22, 23], an early RL-powered pentesting tool integrated with Metasploit, demonstrated full automation of initial access but suffered from overfitting to training environments. 

While RL-based pentesting can autonomously uncover attack paths, its major drawback is **poor generalization** beyond training data, requiring extensive retraining for new environments. 

---

## **8.3 Comparison with RapidPen** 

> **Section Summary:** **Degree of Automation:** RapidPen is designed for full automation of initial access, requiring no human intervention once launched.


**Degree of Automation:** RapidPen is designed for full automation of initial access, requiring no human intervention once launched. This sets it apart from PentestGPT, which requires users to review and execute commands manually. In contrast, RL-based systems like DeepExploit require extensive training and tuning before deployment, making RapidPen a more practical choice for real-world pentesting with minimal setup overhead. 

**Scope of Initial Access Techniques:** RapidPen focuses on achieving unauthorized shell access as quickly as possible, covering a broad range of network and system-level exploitation techniques. Unlike PentestGPT, which primarily provides recommendations, RapidPen directly executes exploits. 

Meanwhile, tools like BLADE and AutoAttacker specialize in post-exploitation rather than initial access, making them complementary rather than competing solutions. 

**Usability for Non-Experts:** RapidPen is explicitly designed for usability by non-experts, enabling security assessments without deep penetration testing expertise. Unlike PentestGPT, which still requires expert validation of generated commands, RapidPen autonomously performs the entire attack process. Additionally, tools like Autonomous Web Exploitation target a different domain (web applications), leaving gaps in usability for broader infrastructure pentesting. 

Overall, RapidPen distinguishes itself by combining **full automation, speed, and accessibility** . It provides a **highly practical and deployable solution** for automated initial access testing, making it a valuable tool for security practitioners and organizations looking to assess their exposure to realworld attack scenarios. 

---

## **9 Conclusion and Future Work** 

> **Section Summary:** In this paper, we introduced **RapidPen** , a fully automated penetration testing framework aimed at achieving an _IP-toShell_ compromise without human intervention.


In this paper, we introduced **RapidPen** , a fully automated penetration testing framework aimed at achieving an _IP-toShell_ compromise without human intervention. By combining ReAct-style task planning with retrieval-augmented exploit knowledge and iterative command generation/execution loops, RapidPen systematically scans for vulnerabilities and exploits them, demonstrating promising results on a vulnerable Hack The Box target. Our evaluation shows that RapidPen can achieve shell access within minutes at a modest cost, even in its current prototype form. 

---

## **9.1 Summary of Contributions** 

> **Section Summary:** - **Proposal and Implementation.** We described the design of RapidPen’s modular _Re_ and _Act_ subsystems, highlighting how each leverages large language models and curated knowledge repositories.


- **Proposal and Implementation.** We described the design of RapidPen’s modular _Re_ and _Act_ subsystems, highlighting how each leverages large language models and curated knowledge repositories. 

- **Empirical Evaluation.** Preliminary experiments on a known vulnerable target demonstrated up to a **60% success rate** for shell acquisition within **200–400 seconds** , with a per-run cost of approximately **$0.3–$0.6** . 

- **Key Insights.** Our results highlight how reusing “success cases” and employing self-correcting command loops significantly enhance the reliability and efficiency of automated pentesting. 

---

## **9.2 Future Directions** 

> **Section Summary:** **Expanding the Scope.** Although RapidPen is currently designed for TCP-based initial access, we plan to extend its capabilities in several areas:


**Expanding the Scope.** Although RapidPen is currently designed for TCP-based initial access, we plan to extend its capabilities in several areas: 


- **Web and UDP Attacks.** Expanding support for webbased exploits, including injection and authentication bypass techniques, and exploring UDP-based vulnerabilities as logical next steps. 

- **Beyond Initial Access.** Integrating passive reconnaissance and post-exploitation workflows (e.g., lateral movement, privilege escalation) by interfacing RapidPen with complementary automated or manual tools. 

**Refining the Current Implementation.** Our short-term development focuses on improving reliability and performance within RapidPen’s existing scope: 

- **Robust Error Handling.** Strengthening the _Act (L1) Command Execution_ and _Act (L1) Log Analysis_ pipeline to prevent premature termination from unexpected failures and clarify when retries or alternative commands are appropriate. 

- **Optimized PTT Input to LLM.** Pruning irrelevant fields or tasks when feeding _Pentesting Task Tree_ (PTT) JSON data to the LLM to reduce context size, thereby increasing speed and lowering costs, particularly in _Re (L1) PTT Planner_ . 

**Execution Modes and Trade-offs.** To improve success rates, we plan to introduce an “auto-retry” mode, where RapidPen automatically re-runs failed test attempts. This feature will be user-configurable, allowing for a balance between execution time, cost, and a higher probability of success. 

**Towards Real-World Deployment.** We aim to make RapidPen accessible to a broader audience—whether through commercial offerings or as an open-source project—so that software teams and security professionals alike can benefit from automated initial-access testing. At the same time, we must design appropriate safeguards to minimize the risk of misuse and ensure that RapidPen is deployed exclusively in legitimate, authorized environments. 

---

## **9.3 Closing Remarks** 

> **Section Summary:** By focusing on _IP-to-Shell_ automation, our work provides both security novices and experts with a powerful tool for quickly identifying critical exposures.


By focusing on _IP-to-Shell_ automation, our work provides both security novices and experts with a powerful tool for quickly identifying critical exposures. We envision that RapidPen’s foundation in LLM-driven planning and execution can serve as a stepping stone toward a new class of intelligent, extensible offensive security tools. As RapidPen matures, we hope it will stimulate further research into collaborative workflows between humans and AI agents, ultimately strengthening the security posture of modern software ecosystems. 

---

## **References** 

- [1] Hack The Box. _Hack The Box: The #1 Cybersecurity Performance Center_ . Accessed: 2025-02-21. 2025. URL: https://www.hackthebox.com/. 

- [2] Tom Brown et al. “Language Models are FewShot Learners”. In: _Advances in Neural Information Processing Systems_ . Ed. by H. Larochelle et al. Vol. 33. Curran Associates, Inc., 2020, pp. 1877– 1901. URL: https : / / proceedings . neurips . cc / paper _ files / paper / 2020 / file / 1457c0d6bfcb4967418bfb8ac142f64a - Paper . pdf. 

- [3] Mark Chen et al. _Evaluating Large Language Models Trained on Code_ . 2021. arXiv: 2107.03374 [cs.LG]. URL: https://arxiv.org/abs/2107.03374. 

- [4] HackTricks Contributors. _HackTricks_ . Accessed: 202502-21. 2025. URL: https : / / github . com / HackTricks-wiki/hacktricks. 

- [5] The MITRE Corporation. _MITRE ATT&CK_ . Accessed: 2025-02-21. 2025. URL: https://attack.mitre. org/. 

- [6] Gelei Deng et al. “PentestGPT: Evaluating and harnessing large language models for automated penetration testing”. In: _33rd USENIX Security Symposium (USENIX Security 24)_ . 2024. 

- [7] Jacob Devlin et al. _BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding_ . 2019. arXiv: 1810.04805 [cs.CL]. URL: https:// arxiv.org/abs/1810.04805. 

- [8] Phillip Garrad and Saritha Unnikrishnan. “Reinforcement learning in VANET penetration testing”. In: _Results in Engineering_ 17 (2023), p. 100970. ISSN: 25901230. DOI: https://doi.org/10.1016/j.rineng. 2023.100970. URL: https://www.sciencedirect. com/science/article/pii/S259012302300097X. 

- [9] Andreas Happe and Jürgen Cito. “Getting pwn’d by AI: Penetration Testing with Large Language Models”. In: _Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering_ . ESEC/FSE 2023. San Francisco, CA, USA: Association for Computing Machinery, 2023, pp. 2082–2086. ISBN: 9798400703270. DOI: 10.1145/3611643.3613083. URL: https:// doi.org/10.1145/3611643.3613083. 

- [10] Zhenguo Hu, Razvan Beuran, and Yasuo Tan. “Automated Penetration Testing Using Deep Reinforcement Learning”. In: _2020 IEEE European Symposium on Security and Privacy Workshops (EuroS&PW)_ . 2020, pp. 2–10. DOI: 10 . 1109 / EuroSPW51379 . 2020 . 00010. 


- [11] J. Huang and Q. Zhu. “PenHeal: A Two-Stage LLM Framework for Automated Pentesting and Optimal Remediation”. In: _Proceedings of the Workshop on Autonomous Cybersecurity_ . ACM, 2023, pp. 11–22. 

- [12] Takeshi Kojima et al. _Large Language Models are ZeroShot Reasoners_ . 2023. arXiv: 2205.11916 [cs.CL]. URL: https://arxiv.org/abs/2205.11916. 

- [13] Patrick Lewis et al. “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks”. In: _Advances in Neural Information Processing Systems_ . Ed. by H. Larochelle et al. Vol. 33. Curran Associates, Inc., 2020, pp. 9459–9474. URL: https://proceedings. neurips.cc/paper_files/paper/2020/file/ 6b493230205f780e1bc26945df7481e5 - Paper . pdf. 

- [14] Hongri Liu et al. “An Automated Penetration Testing Framework Based on Hierarchical Reinforcement Learning”. In: _Electronics_ 13.21 (2024). ISSN: 20799292. DOI: 10.3390/electronics13214311. URL: https://www.mdpi.com/2079-9292/13/21/4311. 

- [15] Sho Nakatani. _[Demo] RapidPen Automatically Gains a Shell (HTB Blue Machine)_ . Feb. 2025. DOI: 10 . 5281/zenodo.14908250. 

   - [24] Isao Takaesu and Daiki Ichinose. “BLADE: A study on automated penetration testing using autonomous AI agents”. In: _AVTOKYO 2024_ . 2024. 

   - [25] Romal Thoppilan et al. _LaMDA: Language Models for Dialog Applications_ . 2022. arXiv: 2201.08239 [cs.CL]. URL: https://arxiv.org/abs/2201. 08239. 

   - [26] Yunfei Wang et al. _A Unified Modeling Framework for Automated Penetration Testing_ . 2025. arXiv: 2502. 11588 [cs.AI]. URL: https://arxiv.org/abs/ 2502.11588. 

   - [27] Qingyun Wu et al. _AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation_ . 2023. arXiv: 2308.08155 [cs.AI]. URL: https://arxiv. org/abs/2308.08155. 

   - [28] Jiacen Xu et al. _AutoAttacker: A Large Language Model Guided System to Implement Automatic Cyberattacks_ . 2024. arXiv: 2403 . 01038 [cs.CR]. URL: https://arxiv.org/abs/2403.01038. 

   - [29] Shunyu Yao et al. “ReAct: Synergizing reasoning and acting in language models”. In: _arXiv preprint arXiv:2210.03629_ (2022). 

- [16] OpenAI et al. _GPT-4 Technical Report_ . 2024. arXiv: 2303.08774 [cs.CL]. URL: https://arxiv.org/ abs/2303.08774. 

- [17] OpenAI et al. _GPT-4o System Card_ . 2024. arXiv: 2410. 21276 [cs.CL]. URL: https://arxiv.org/abs/ 2410.21276. 

- [18] Alec Radford et al. “Language Models are Unsupervised Multitask Learners”. In: _OpenAI_ (2019). Accessed: 2024-11-15. URL: https://cdn.openai. com / better - language - models / language _ models _ are _ unsupervised _ multitask _ learners.pdf. 

- [19] Colin Raffel et al. “Exploring the limits of transfer learning with a unified text-to-text transformer”. In: _J. Mach. Learn. Res._ 21.1 (Jan. 2020). ISSN: 1532-4435. 

- [20] Rapid7. _Metasploit Framework_ . Accessed: 2025-0221. 2025. URL: https : / / github . com / rapid7 / metasploit-framework. 

- [21] The Penetration Testing Execution Standard. _PTES Technical Guidelines_ . Accessed: 2025-02-21. 2025. URL: http://www.pentest-standard.org/index. php. 

- [22] Isao Takaesu. “Deep Exploit”. In: _DEF CON 26_ . 2018. 

- [23] Isao Takaesu. “DeepExploit: Fully Automated Penetration Testing Using Reinforcement Learning”. In: _CODE BLUE_ . 2019. 


