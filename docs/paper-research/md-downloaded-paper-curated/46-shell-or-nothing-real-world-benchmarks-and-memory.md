# **Shell or Nothing: Real-World Benchmarks and Memory-Activated Agents for Automated Penetration Testing** 

Geng Hong<sup>∗</sup> Fudan University Shanghai, China ghong@fudan.edu.cn 

Qi Liu Fudan University Shanghai, China qiliu25@m.fudan.edu.cn 

Wuyuao Mai<sup>∗</sup> Fudan University Shanghai, China maiwuyuao20@fudan.edu.cn 

Jinsong Chen Fudan University Shanghai, China jschen23@m.fudan.edu.cn 

Jiarun Dai Xudong Pan Fudan University Fudan University Shanghai, China Shanghai Innovation Institute jrdai@fudan.edu.cn Shanghai, China xdpan@fudan.edu.cn 

Min Yang<sup>�</sup> Fudan University Shanghai, China m_yang@fudan.edu.cn 

Yuan Zhang Fudan University Shanghai, China yuanxzhang@fudan.edu.cn 

## **Abstract** 

To address these challenges, we propose TermiAgent, a multi-agent penetration testing framework. TermiAgent mitigates long-context forgetting with a Located Memory Activation mechanism and builds a reliable exploit arsenal via structured code understanding rather than naïve retrieval. In evaluations, our work outperforms state-of-the-art agents—exhibiting stronger penetration testing capability, reducing execution time and financial cost, and demonstrating practicality even on laptop-scale deployments. Our work delivers both the first open-source benchmark for real-world autonomous pentesting and a novel agent framework that establishes a milestone for AI-driven penetration testing. 

Penetration testing is critical for identifying and mitigating security vulnerabilities, yet traditional approaches remain expensive, time-consuming, and dependent on expert human labor. Recent work has explored AI-driven pentesting agents, but their evaluation relies on oversimplified capture-the-flag (CTF) settings that embed prior knowledge and reduce complexity, leading to performance estimates far from real-world practice. We close this gap by introducing the first real-world, agent-oriented pentesting benchmark, TermiBench, which shifts the goal from “flag finding” to achieving full system control. The benchmark spans 510 hosts across 25 services and 30 CVEs, with realistic environments that require autonomous reconnaissance, discrimination between benign and exploitable services, and robust exploit execution. Using this benchmark, we find that existing systems can hardly obtain system shells under realistic conditions. 

#### **ACM Reference Format:** 

Wuyuao Mai, Geng Hong, Qi Liu, Jinsong Chen, Jiarun Dai, Xudong Pan, Yuan Zhang, and Min Yang<sup>�</sup> . 2025. Shell or Nothing: RealWorld Benchmarks and Memory-Activated Agents for Automated Penetration Testing. In _._ ACM, New York, NY, USA, 19 pages. https: //doi.org/10.1145/nnnnnnn.nnnnnnn 

∗Both authors contributed equally to this research. 

## **1 Introduction** 

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org. _Anonymous’25, Anonymous_ 

© 2025 Copyright held by the owner/author(s). Publication rights licensed to ACM. ACM ISBN 978-x-xxxx-xxxx-x/YYYY/MM https://doi.org/10.1145/nnnnnnn.nnnnnnn 

Penetration testing (pentesting) is a cornerstone of modern cybersecurity, enabling organizations to proactively identify and mitigate exploitable vulnerabilities before adversaries can capitalize on them. By simulating realistic cyberattacks, pentesting not only assesses the robustness of deployed defenses but also informs remediation strategies and compliance with security standards [21, 38]. Traditional pentesting, however, is resource-intensive—typically costing $10,000–$20,000 per engagement [10, 14]—and demands highly skilled human experts capable of navigating complex, heterogeneous systems under tight time constraints. These 

Anonymous’25, Anon, Anonymous 

Wuyuao Mai, et al. 

limitations have fueled growing interest in automation, particularly through AI-assisted cybersecurity testing. 

Recent advances in large language models (LLMs) and autonomous agents have inspired new approaches to AIassisted security testing, ranging from vulnerability discovery and patch generation (e.g., DARPA’s AI Cyber Challenge) [17] to AI-driven penetration testing frameworks such as PentestGPT and VulnBot [9, 18, 40]. While these prototypes demonstrate the potential of LLM-based agents to accelerate parts of the pentesting workflow, their evaluations remain tethered to oversimplified, CTF-style environments. These settings often embed a priori knowledge—such as leaked passwords, predefined exploit entry-points that human red teams would not have in practice, and they set up an unrealistic testing environment that each target only hosts exactly one vulnerable service. As a result, these simplified benchmarks may overestimate real-world agent pentest performance. 

In contrast, real-world penetration testing unfolds in a far more challenging operational landscape. Red-teams often begin with nothing more than network access, requiring them to perform reconnaissance and enumeration under uncertainty while distinguishing benign background services from the actual attack surface of the targets. Achieving full system compromise—culminating in an interactive shell—necessitates the integration of diverse skills, tools, and reasoning under dynamic and incomplete information. Current benchmarks for autonomous penetration testing agents, structured as CTF-style exercises and providing prior hints, are insufficient for evaluating agent performance in real-world scenarios. 

To close these gaps, we present TermiBench, the first benchmark for real-world, fine-grained, and agent-oriented penetration testing evaluation. First, our benchmark shifts the final objective from “flag-finding” to achieving system control, specifically obtaining a system shell. To more faithfully replicate real-world conditions, the benchmark omits unnecessary prior information—such as entry points and predefined exploit paths—thereby requiring agents to conduct reconnaissance autonomously. In addition, we configure target hosts with common applications, including web servers and database systems, to introduce “noise” that compels agents to distinguish between exploitable and nonexploitable services. Finally, the benchmark comprises 510 hosts embedding 30 CVEs across 25 distinct services over a ten-year span. Each host is configured with up to seven vulnerability-free services alongside one vulnerable service dated between 2015 and 2025. 

With this benchmark, we find that previous work fails to acquire the system shell of target hosts. Agents were either lost in vast amounts of exploratory information that accumulated in complex real-world penetration testing scenarios, or could not penetrate the target service without ready-to-use penetration testing agents’ exploits. 

In this paper, we propose TermiAgent, a multi-agent framework tailored for real-world penetration testing. To address the challenge of long-context forgetting in penetration testing, we introduce a Located Memory Activation approach. When predicting its next action, the agent automatically activates all relevant memories required for decision-making, reflecting the characteristics of real-world penetration testing tasks. To build an up-to-date and ready-to-use exploit arsenal, we formulate exploit integration as a structured code-understanding problem rather than a simple retrievaland-execution task. Unlike naive methods that merely fetch public PoC repositories and attempt direct execution, our approach ensures robust and reliable exploit utilization. As illustrated in Figure 2, TermiAgent comprises the Reasoner Module, the Assistant Module, the Executor Module, the _Memory Module_ and the Arsenal Module, which collaboratively decompose penetration testing targets into multi-step sub-tasks, progressively achieving the final objectives in a perception–action loop. 

To evaluate the performance of TermiAgent, we compare it against state-of-the-art penetration testing agents. Results demonstrate that TermiAgent solves approximately 1.7 times as many CTF challenges and over 8 times as many real-world penetration testing tasks as state-of-the-art agents. In terms of efficiency, TermiAgent achieves lower time and financial costs, requiring less than one-fifth of the execution time and only a tenth of the financial cost in real-world scenarios. Furthermore, our arsenal covers 1.8 times more RCE CVEs than Metasploit. 

In summary, this papers make the following contributions: 

- We reveal the gap between real-world penetration testing requirements and existing LLM-based approaches, showing that current benchmarks overestimate real-world agent penetration performance. 

- We construct and open-source the first real-world, finegrained, and agent-oriented penetration benchmark that replicates real-world conditions for agent-oriented penetration testing. 

- We design and implement TermiAgent, a penetration testing framework that achieves significantly better performance than prior work. 

- We demonstrate that even a laptop-scale deployment can effectively support end-to-end automated penetration testing, highlighting the practicality of our approach. 

## **2 Background and Preliminary Study 2.1 Background** 

**Penetration Testing.** Penetration testing, or pentesting, refers to the practice of simulating adversarial attacks on a computing system to identify exploitable security flaws. Penetration testing is critical for proactively identifying security vulnerabilities before they can be exploited by adversaries. Simulating real-world cyberattacks enables the assessment 

Anonymous’25, Anon, Anonymous 

Shell or Nothing: Real-World Benchmarks and Memory-Activated Agents for Automated Penetration Testing 


![](docs/paper-research/md-downloaded-paper-curated/images/46-shell-or-nothing-real-world-benchmarks-and-memory.pdf-0003-02.png)


<!-- Start of picture text -->
Limitations of Previous Work<br>a (Flag-oriented)CTF Challenge b Extra Hints c Single Service  d Limited & Delayed Tools<br>✅ IP: 192.168.0.10<br>My task is to  ✅ Entry Point: /login   Coverage: < 50% of PoCs<br>capture the  flag . ✅ Exploit Path: XXXX Config.yml SQL SSH Status: Delayed updates<br>FLAG services: vuln:  enabled vuln Redis FTP Common Pentest Toolkits<br>💬I captured the flag:    ssh:   http:   ftp:  disableddisableddisabled HTTP xxx x ✅✅❌❌CVE-2018-xxxxCVE-2020-xxxxCVE-2024-xxxxCVE-2025-xxxx Integrated Exploits<br>FLAG{this_is_a_string}   sql:  disabled Benchmark Slow Updates Limited Coverage<br>e Our Real-world Pentest Agent<br>Real-world CVE Target  Only Subnet Multi-service Broad & Timely Arsenal<br>(Shell-oriented)<br>Broad Coverage Fast Updates<br>My task is to gain a  shell . ✅ subnet: 192.168.0.0/24   FTPRedis HTTP<br>CVE List<br>Apache├├ CVE-2021-41773 Spring Framework├├ CVE-2022-22965 DNS SSH Integrated exploits In-the-wildexploits<br> └─  CVE-2021-42013  └─  CVE-2018-1270 user@host:~$  sudo su<br>Elasticsearch └─  └─  CVE-2015-1427 25 Services30 CVEs30 CVEs SQL CVE-xxx root@host:~#uid-0(root) gid-0(root)id<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-curated/images/46-shell-or-nothing-real-world-benchmarks-and-memory.pdf-0003-03.png)


<!-- Start of picture text -->
CVE List<br>Apache├├ CVE-2021-41773 Spring Framework├├ CVE-2022-22965<br> └─  CVE-2021-42013  └─  CVE-2018-1270<br>Elasticsearch └─  └─  CVE-2015-1427 25 Services30 CVEs30 CVEs<br><!-- End of picture text -->

**Figure 1.** A motivating example of this work compared with the previous work. 

of defensive effectiveness, mitigates the risk of data breaches, and ensures adherence to security standards [21]. Pentesting is generally executed through a series of well-defined steps, including target Planning, Discovery, Attack, Reporting [38]. The average cost of a penetration test ranges from $10,000 to $20,000, depending on the complexity of the environment, including factors such as services, databases, and operating systems [10, 14]. 

**AI-assisted Cybersecurity Testing.** Current AI-assisted cybersecurity testing efforts mainly fall into two categories: automated vulnerability discovery and remediation, and AIdriven pentesting. In the former, initiatives such as DARPA’s AI Cyber Challenge (AIxCC) [17] have demonstrated that AI systems can help identify and patch vulnerabilities at scale. In the latter, research prototypes such as PentestGPT represent initial attempts to employ LLM-based agents for pentesting [9, 18, 40]. While these works highlight AI roles to accelerate pentesting, they remain limited by reliance on well-informed CTF-like datasets and oversimplified configurations of meeting the challenges posed by fully automated, end-to-end pentesting against realistic targets. 

### **2.2 Motivating Example** 

Although the emergence of LLMs and agents has fostered the development of automated pentesting, current approaches still fall short of meeting the requirements of real-world automated pentesting scenarios as in Figure 1. Some pentesting agents **(a)** improperly equate CTF challenges with real-world scenarios, **(b)** requiring initial hints like entry points, a luxury not afforded in real-world tasks where only IP or subnet is provided. They also heavily **(c)** rely on static, outdated third-party tools like Metasploit, which have insufficient 

vulnerability coverage. Similarly, current benchmarks are unrealistic, **(d)** typically featuring targets with only a single vulnerable service, thereby failing to reflect the multi-service complexity of real-world scenarios. 

Our work addresses these challenges by **(e)** an approach oriented toward real-world pentesting scenarios. Our agent is designed to perform end-to-end penetration tests using only IP or subnet information to gain host ownership. To ensure it has timely access to a more extensive range of exploits, we have built our own dynamic arsenal. Furthermore, our benchmark moves beyond the traditional CTF-style exercises by introducing a multi-service environment and assessing the agent’s capability by evaluating the true depth of its penetration. 

### **2.3 Research Scope** 

We consider an adversary leveraging an AI agent to conduct real-world automated end-to-end pentesting. The adversary is assumed to have network-level access to the target but no prior knowledge of its vulnerabilities or configurations beyond standard reconnaissance capabilities. The agent operates fully autonomously—planning, executing, and adapting each step without human intervention. The target is a simulated host configured with widely deployed services, which may or may not contain exploitable vulnerabilities. The adversary’s goal is to achieve control authority of the targeted machine, concretely, obtaining interactive system shell access. 

## **3 Real-World Benchmark** 

To effectively evaluate the capabilities of autonomous pentesting agents, a benchmark should faithfully reproduce the 

Anonymous’25, Anon, Anonymous 

Wuyuao Mai, et al. 

**Table 1.** A comparison between TermiAgent and prior work. TermiAgent requires only the subnet range of target to achieve the real-world penetration objective of system ownership, while also being compatible with CTF scenarios. Leveraging a Pluggable External Arsenal and the Local Memory Activation mechanism, TermiAgent is designed to handle complex, multi-step, multi-service real-world penetration testing tasks, while maintaining compatibility with lightweight LLMs. 

||**Success**<br>**Criterion**|**Target**<br>**Information**|**Human**<br>**Assisted**|**Pluggable External**<br>**Arsenal**|**Muti-Service**<br>**Penetration**|**Lightweight LLM**<br>**Compatibility**|
|---|---|---|---|---|---|---|
|**TermiAgent**|**System Ownership**|**Subnet**|✗|✓|✓|✓|
|VulnBot[18]|CTF Flag|Subnet / Entry Point / Exploit Path|✗|✗|✗|✗|
|PentestGPT[9]|CTF Flag|IP|✓|✗|✗|✗|
|PentestAgent[40]|CTF Flag|IP|✗|✗<sup>*</sup>|✗|✗|
|AutoPentest[15]|CTF Flag|IP|✗|✗|✗|✗|
|HackSynth[23]|CTF Flag|IP / Entry Point / Exploit Path|✗|✗|✗|✗|
|CIPHER[31]|CTF Flag|IP|✓|✗|✗|✗|
|AutoAttacker[41]|Subtask|Exploit Path|✗|✗|✗|✗|
|BreachSeek[6]|Subtask|Exploit Path|✗|✗|✗|✗|



> * PentestAgent can just search for relevant exploit online, but it cannot automatically package it into a ready-to-use arsenal. 

complexity and uncertainty of real-world scenarios. A realworld penetration test is defined as a security assessment that mimics real-world attacks to identify methods for circumventing the security features of an application, system, or network [38]. Importantly, this process typically involves testers who have little to no prior information about the target environment, except for an IP address. They are tasked with identifying and exploiting known vulnerabilities to evaluate the true level of risk [4, 29, 32, 38]. Existing evaluation benchmarks [9, 12, 16], however, fall short of this standard, creating a gap between an agent’s performance in a well-informed testbed and its efficacy in a real operational environment. 

### **3.1 Prior Benchmark Limitations** 

Existing pentesting resources, including traditional platforms like Vulhub and HackTheBox [13, 30], are not ideal for evaluating autonomous pentesting agents. These platforms are primarily designed for human training: they provide prebuilt vulnerable Docker environments but lack instrumentation to automatically verify compromise or track an agent’s progress. They also fall short in realism, as they only expose the target vulnerability and do not include benign background services. Past benchmarks share the following characteristics. 

First, the objectives of the prior benchmarks [9, 12, 16] are misaligned with those of real-world pentesting. They are primarily structured as CTF-style exercises, where the goal is typically to locate a “flag”—a string stored in a file that signifies task completion. However, this “flag-finding” focus diverges from the end-to-end objectives of a typical penetration test, such as obtaining a remote shell. Moreover, using flag capture as the sole evaluation criterion fails to meet the requirement [38] of assessing the impact of the attacker’s penetration progress on the target. 

Second, some benchmark provides agents with more information than is available in real-world pentesting. Instructions of targets in Auto-Pen-Bench [12] often embed a priori knowledge—such as service names and versions, entry-point hints, or predefined exploit paths—that a red team would not have. In practice, operators typically start with little more than network access and must perform reconnaissance, enumeration, and hypothesis-driven testing under uncertainty [38]. 

Third, target configurations are often oversimplified. A common limitation in existing work is the configuration of each server with exactly one exploitable service [9, 12, 16]. In contrast, real-world servers typically host multiple services, most of which lack easily exploitable vulnerabilities [43]. These vulnerability-free services introduce substantial “noise” into pentesting, requiring the agent to perform thorough reconnaissance, accurately identify the actual attack surface, and operate within a larger, more complex environment. 

### **3.2 Benchmark Design** 

To overcome these limitations, we present the first realworld, fine-grained, and agent-oriented pentesting bench- mark, built around three principles: real world fidelity, blind evaluation, and systematic service integration. 

First, instead of artificial “flag-finding” challenges, every target in our benchmark is based on a real, documented CVE. From all CVEs disclosed between 2015 and 2025 [24], we retained only those affecting free and open-source software, reproducible in a controlled setting, and enabling remote code execution(RCE)—the most operationally relevant outcome in professional pentesting. This process yields 30 CVEs spanning 25 distinct services, three times larger than previous works that have been exploited in the wild. Success is defined as obtaining a remote shell, directly aligning with end-to-end pentesting goals. We further examine whether 

Anonymous’25, Anon, Anonymous 

Shell or Nothing: Real-World Benchmarks and Memory-Activated Agents for Automated Penetration Testing 

**Table 2.** Comparison of penetration testing Benchmarks for automated agents. TermiBench is distinguished by its focus on achieving system ownership in complex, multi-service environments with minimal initial information. 

||**Primary Objective**|**Initial Knowledge**|**Environment**<br>**Complexity**|**# of**<br>**Benign Services**|**System Impact**<br>**Assessment**|**# of**<br>**Unique CVEs**|**# of**<br>**Hosts**|
|---|---|---|---|---|---|---|---|
|**TermiBench**|**System Ownership**|**Subnet Only**|**Multi-Service**|**0, 1, 3, 5, 7**|✓|**30**|**510**|
|Auto-Pen-Bench [12]|CTF Flag|Extra Hints|Single-Service|0|✗|11(CTF-style)|33|
|HackTheBox/Vulhub<sup>*</sup>|CTF Flag|Not Specifed|Single-Service|0|✗|0|13|
|AI-Pentest-Benchmark [16]|CTF Flag|Not Specifed|Single-Service|0|✗|0|13|



> * Selected by PentestGPT [9] 

the acquired shell possesses root privileges to evaluate the extent of impact on the target host [38]. 

Second, to better replicate real-world conditions, agents receive no prior knowledge beyond the target subnet range. Service names, version details, and predefined exploit paths are not provided in our benchmark, requiring agents to autonomously conduct reconnaissance, enumeration, and testing under uncertainty. This blind-start condition reflects the operational reality of human red teams and prevents the unrealistic advantage from benchmarks that include a priori knowledge in their setup. 

Third, to solve the problem of oversimplified configurations, we introduce systematic environmental complexity. We integrate benign services alongside the target vulnerability to create operational “noise”. This design forces agents to perform comprehensive service enumeration and accurately identify the true attack vector in a more complex environment, a challenge absent from single-service benchmarks [12, 13, 30]. To systematically evaluate agent performance, we adjust the density of these benign services across different levels, enabling a detailed analysis of how environmental complexity influences the agent’s effectiveness. 

### **3.3 Benchmark Overview** 

Our benchmark consists of a total of 510 distinct host instances, built on a foundation of 30 unique, real-world CVEs that affect 25 different services as shown in Table 10. The design systematically varies the number of benign background services to create different levels of environmental complexity. This approach enables a detailed evaluation of an agent’s capabilities in increasingly realistic network environments. 

The benchmark is structured into two main parts. It begins with a base configuration of 30 hosts, each featuring a single vulnerable service and no benign services, referred to as the “1+0” configuration. These hosts serve to measure agent performance in an isolated environment, providing a direct comparison to the simplified setups of previous benchmarks [9, 12, 16]. 

The core of our benchmark consists of four levels of environmental complexity, totaling 480 hosts, designed to measure the impact of environmental noise. These levels are systematically constructed with one, three, five, and seven benign services running alongside the single vulnerable one 

corresponding to the “1+1”, “3+1”, “5+1”, and “7+1” configurations, with 120 hosts allocated to each level. The benign services, as shown in Table 8, are randomly selected from a pool of the 14 most common applications identified through large-scale internet measurements using the FOFA scan engine [11]. The upper bound of seven benign services was chosen based on our empirical analysis of this data, which indicates that the vast majority of typical home computing environments host no more than seven concurrently active services. This structure, summarized in Table 9, enables a systematic analysis of how agent performance degrades or adapts as the operational environment becomes progressively more complex and noisy. 

## **4 Methodology** 

In this section, we present the challenges encountered, key insights gained, and the design and implementation of our approach. 

### **4.1 Challenges and Insights** 

Traditional pentesting methodologies [5] generally involve three key phases. The scanning phase gathers information about the target system. The reconnaissance identifies potential attack surfaces. The exploitation phase attempts to gain system control by leveraging discovered vulnerabilities, thereby completing the pentesting cycle. 

Given the proven effectiveness of these well-established procedures, integrating them into AI-agent-driven automated pentesting appears to be a promising direction. However, we argue that directly applying them in real-world environments with autonomous agents poses significant challenges. **Challenge 1: How to manage and optimize context in real-world pentesting agents under long-context forgetting?** A key bottleneck in AI-agent-driven pentesting is the long-context forgetting phenomenon inherent to LLMs [20]. In complex real-world pentesting scenarios, as the agent progresses through iterative trial-and-error steps, vast amounts of exploratory information accumulate in the context. Due to the limited effective context retention of LLMs, older but still relevant information is often attenuated or entirely forgotten as new content is appended. Therefore, even when the context length is compressed to stay within 

Anonymous’25, Anon, Anonymous 

Wuyuao Mai, et al. 

the LLM’s window limit, irrelevant information continues to consume valuable context space, causing the agent to miss capturing crucial relevant details, thereby degrading the actual effectiveness of the pentesting. 

Insights 1: We tackle this challenge with a Located Memory Activation approach. When predicting its next action, the agent automatically activates all memories relevant to the current decision-making, guided by the hierarchical nature of real-world pentesting landscapes where target hosts branch into increasingly specific and mutually independent attack surfaces. We further apply memory reduction at varying levels—ranging from coarse summaries to fine-grained details—based on the agent’s task requirements. For example, phased planning requires monitoring high-level penetration test progress, while concrete instruction generation relies on low-level command details. This ensures that the agent consistently retains only minimal but sufficient knowledge throughout the penetration process. 

**Challenge 2: How to construct an up-to-date and readyto-use exploit arsenal for the pentesting agents?** Current pentesting agents’ exploits often rely heavily on opensource frameworks such as Metasploit [22], whose exploit collections are relatively outdated and exhibit incomplete coverage of relevant vulnerabilities. In particular, our analysis of RCE vulnerabilities from 2015 to 2025 shows that Metasploit covers only about half of these CVEs compared to publicly available exploits on GitHub, highlighting a gap between existing frameworks and real-world vulnerability disclosures. To close this gap, integrating exploits from platforms such as GitHub seems straightforward. Unfortunately, online repositories are rarely “plug-and-play”: they lack a unified usage convention, exhibit non-standard execution entry points, and are often accompanied by incomplete or missing documentation. This lack of standardization makes it difficult to transform raw exploits into agent-friendly exploits. 

Insights 2: We treat automated exploit integration as a structured code-understanding problem, rather than a simple code retrieval and execution task. Our approach addresses two key challenges. First, we systematically extract over ten semantic and operational dimensions that define an exploit’s executability—such as programming language, base image, system dependencies, and workflow—and organize them into a Unified Exploit Descriptor (UED). The UED serves as a precise intermediate representation, enabling raw GitHub repositories to be automatically packaged into fully executable, self-contained artifacts. Second, to make exploits agent-invocable, we automatically generate concise, precise manuals. These manuals distill excessive or noisy instructions and infer missing details from code structures, repository files, and inline comments. By combining the UED with these distilled manuals, raw exploits are transformed into standardized, plug-and-play modules, supporting reliable integration into automated pentesting workflows. 

### **4.2 Design Overview** 

Building on the challenges and our insights aforementioned, we propose TermiAgent, a multi-agent framework tailored for real-world pentesting. As illustrated in Figure 2, TermiAgent comprises the Reasoner Module, the Assistant Module, the Executor Module, the _Memory Module_ and the Arsenal Module, which collaboratively decompose pentesting targets into multi-step sub-tasks, progressively achieving the final objectives in a perception–action loop. 

Within our framework, the Reasoner Module handles highlevel decisions, planning subsequent phased goals based on the ongoing progress and overall goal of the penetration test. The Assistant Module, in turn, handles low-level decisions by generating the specific command to be executed next, based on the phased goal and the concrete details of the current pentesting task. The Assistant Module may generate a series of commands to accomplish the phased goal. Control is returned to the Reasoner Module to devise a new phased goal only after the current one is either achieved or fails. The commands generated are subsequently executed by the Executor Module, with their respective outputs being logged. 

During this process, the _Memory Module_ records all contextual information gathered by TermiAgent throughout the pentesting, with each entry being goal-oriented and compressed into three distinct levels of granularity. When TermiAgent plans the next phased goal or generates the subsequent commands, all the relevant memories are automatically activated, the corresponding compressed level of which is then provided based on the specific requirements of the current decision-making task. 

In addition, we develop the Arsenal Module, which automates the integration of both in-the-wild exploits and open-source pentesting frameworks to TermiAgent as a plugand-play module. The Arsenal Module provides TermiAgent with a unified interface encompassing all pentesting tools, including all collected executable exploits along with their corresponding usage manuals, thereby enabling TermiAgent to readily utilize them and further enhancing its pentesting capabilities. 

In the following sections, we will further elaborate on the _Memory Module_ and the Arsenal Module, highlighting both their functionalities and the underlying design principles. The introduction of the Reasoner Module, the Assistant Module, and the Excutor Module can be found in Appendix B. 

### **4.3 Memory Module** 

The _Memory Module_ is responsible for recording and organizing all contextual information gathered by the agent during the execution of real-world pentesting tasks. First, _Memory Module_ dynamically activates memory related to the current target components within the agent’s decision-making loop. Second, to provide the agent with compact but sufficient 

Anonymous’25, Anon, Anonymous 

Shell or Nothing: Real-World Benchmarks and Memory-Activated Agents for Automated Penetration Testing 


![](docs/paper-research/md-downloaded-paper-curated/images/46-shell-or-nothing-real-world-benchmarks-and-memory.pdf-0007-02.png)


<!-- Start of picture text -->
Identify host in 192.168.0.0/24 and perform penetration testing to get its shell.<br>❶<br>❷<br>❺<br>Reasoner Memory Assistant<br>R Activated Based on the context and the phased goals,<br>Please plan the next phased goals based on the context and overall goals: PMT Non-activated first determine whether the current phased goal has been completed. If not completed,<br>Overall Goal R. Subnet :  192.168.0.0/24 please generate specific instructions for the<br>perform penetration testing to get its shell.Identify host in 192.168.0.0/24 and  Activated Abstract Memory 1 a 2 b 3 1.2. IP: 192.168.0.1 IP: 192.168.0.2 a. Service Ⅰ Exp:  : AA-1 pache - druid next step.Use self-built exploit A-1 to try to obtain a shell through Apache-druid service  Phased Goal<br>1. found host 192.168.0.2 In 192.168.0.0/242. Found service Apache-druid in the host3. Found corresponding self-build exploit A-1 Ⅰ Ⅱ         b.3. IP: 192.168.0.3Service: OpenSSH Ⅱ  Exp: A-2 1. Used ` Activated Coarse-grained Memory nmap –sn 192.168.0.0/24 ` and<br>found host 192.168.0.2 up;<br>Compression Level a 2. Used ` nmap –sV 192.168.0.2 ` and found<br>Abstract:  Identified the Apache-druid service. port `8888` with unknown service ` answerbook? ` sun-<br>OK, now that we have successfully identified the host, service, and corresponding exploit, in order to obtain the shell, the next phased goal should be: Coarse-grained:  found port `8888` with unknown service ` answerbook?8888` , revealing Apache-druid.`; UsedUsed `  `whatweb http://192.168.0.2:nmap –sV 192.168.0.2sun- ` and  3. Usedrevealing Apache-druid.3. Found a corresponding self-build exploitA-1 for Apache-druid.  `whatweb http://192.168.0.2:8888`<br>Use self-built exploit A-1 to try to obtain a shell through Apache-druid service  Phased Goal Fine-grained: 1. VERSION ……8888/tcp open  sun-answerbook?......  nmap -sV  192.168.0.2:  ...... PORT STATE SERVICE  ` docker run –it A-1 –ip <ip> Exploit Manual -port <port> ` Analysis<br>2. whatweb http://172.19.0.99:8081:  ...[RESERVED]<br>[ZZ], HTML5 IP[172.19.0.99]…Title[Apache Druid]… No, the A-1 exploit has not been used, so the mission is not complete. The next UED<br>step is to deploy self-built exploit A-1 for<br>Executor Apache-druid. Based on manual of self-<br>built exploit A-1, the next specific<br>192.168.0.2 ` docker run –it A-1 –ip Instruction -port 8888 Shell execution in` Kali Linux Capture Output [08/26/25 23:59:20*] Docker starting...[08/26/25 23:59:59*] Get the shell> whoamiroot Output ！ instruction should be:` docker run –it A-1 –ip 192.168.0.2 Instruction port 8888 ` -<br>❸ ❹<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-curated/images/46-shell-or-nothing-real-world-benchmarks-and-memory.pdf-0007-03.png)



![](docs/paper-research/md-downloaded-paper-curated/images/46-shell-or-nothing-real-world-benchmarks-and-memory.pdf-0007-04.png)


<!-- Start of picture text -->
RCE filter<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-curated/images/46-shell-or-nothing-real-world-benchmarks-and-memory.pdf-0007-05.png)


<!-- Start of picture text -->
Metasploit<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-curated/images/46-shell-or-nothing-real-world-benchmarks-and-memory.pdf-0007-06.png)


<!-- Start of picture text -->
Metasploit<br>……<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-curated/images/46-shell-or-nothing-real-world-benchmarks-and-memory.pdf-0007-07.png)


<!-- Start of picture text -->
Collection<br>Analysis<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-curated/images/46-shell-or-nothing-real-world-benchmarks-and-memory.pdf-0007-08.png)



![](docs/paper-research/md-downloaded-paper-curated/images/46-shell-or-nothing-real-world-benchmarks-and-memory.pdf-0007-09.png)



![](docs/paper-research/md-downloaded-paper-curated/images/46-shell-or-nothing-real-world-benchmarks-and-memory.pdf-0007-10.png)


<!-- Start of picture text -->
Exploits Manuals<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-curated/images/46-shell-or-nothing-real-world-benchmarks-and-memory.pdf-0007-11.png)


**Figure 2.** System Overview. ❶ The security researcher specifies the overall pentesting goal and inputs it to the agent. After several iterations, based on the abstract memory automatically activated by the _Memory Module_ and the overall goal, the Reasoner Module proceeds to plan the next phased goal. ❷ The phased goal is then sent to the Assistant Module, which generates the next specific instruction based on activated coarse-grained memory and documentation from the Self-Built Arsenal Module. ❸ The Executor Module executes the specific instruction and updates the resulting command output into the _Memory Module_ . ❹ The assistant module then generates the next instruction. If the current phased goal is completed, ❺ it obtains the next phased goal from the Reasoner Module, repeating this process until the overall goal is achieved. 

context information, memory is reduced at varying levels according to the task requirements. Finally, the _Memory Module_ tracks and guides the pentesting direction according to a comprehensive record of pentesting progress. 

**4.3.1 Penetration Memory Tree Construction.** To enable automated active suitable located memory, the first challenge lies in accurately identifying which memory is relevant to the current pentesting stage. In real-world pentesting scenarios, a single host may expose multiple attack services and each service may suffering enoumouse vulnerabilities, leading to excessive potential penetration paths for the agent to explore. The widely adopted method for relevant context filtering relies on semantic similarity analysis. However, the key information of a single penetration path, such as IP addresses, ports, and shell commands, contains limited semantic content and thus similarity-based context filtering methods risk omitting critical information. 

We model the pentesting process as a Penetration Memory Tree ( **PMT** ), capturing the hierarchical structure of realworld pentesting. In PMT, a target machine may host several services, each exposing entry points exploitable via distinct vulnerabilities. Tree edges represent branching decisions—such as selecting a service or choosing among available exploits—while nodes store the agent’s execution context at that decision point. Upon undergoing a new stage of penetration, the current node spawns child nodes and transfers context to the relevant branch. During execution, context retrieval is performed via backward traversal from the current node to the root of PMT, ensuring activation of relevant memories while suppressing extraneous information. 

**4.3.2 Pentest Context Compression.** The agents of TermiAgent in different roles prioritize information at different levels of granularity. Specifically, the Reasoner Module concentrates on monitoring the high-level, stage-wise progress of pentesting, whereas the Assistant Module depends on concrete execution results of individual instructions to both 

Anonymous’25, Anon, Anonymous 

Wuyuao Mai, et al. 

assess the attainment of phased goals and generate subsequent instructions. Therefore, supplying the raw memory with noise in their entirety to the context is insufficient to guarantee that TermiAgent can operate at its full potential. In addition to role-specific distinctions, the different stages of real-world pentesting further shape the aspects of context to which agents assign priority. For example, in the scanning stage, TermiAgent may prioritize service fingerprints, version numbers, and other indicators of entry points, whereas in the exploitation stage, the focus may shift toward information like command outputs, execution success, etc. Such key aspects are often not directly inferable from instructions and their results alone. If constrained to this limited view, the agent may disproportionately focus on outcome-related information while overlooking other critical metadata. 

Therefore, we applied intent-oriented compression to the context of TermiAgent. We recorded the agent’s reasoning process during instruction generation to analyze the underlying intent, which then guided the compression of the context into three distinct levels. First, the raw execution results of instructions are normalized at the character level to remove escape sequences, such as color control codes, yielding a finegrained, LLM-readable context. Based on this fine-grained level context, the abstract level context is compressed to emphasize the stage-wise progress of pentesting, while the coarse-grained level context is compressed to provide an overview of executed instructions and their corresponding outcomes. The design of intent-oriented compression enables TermiAgent to selectively attend to context according to its role and the current stage of the pentesting task, thereby avoiding interference from irrelevant information while ensuring that critical information is fully preserved. 

**4.3.3 Path Enumeration and Prioritization.** After constructing the memory tree and compressing unnecessary memory, the _Memory Module_ must generate the penetration path guide efficiently. Specifically, _Memory Module_ employs a depth-first search traversal to enumerate all root-to-leaf paths, explicitly annotating both executed and unexecuted sequences. Furthermore, child nodes under a parent node can be sorted according to pentesting conditions, allowing the agent to prioritize exploring paths with a higher likelihood of success. The sorting criteria are determined by the vulnerability likelihood of the target service and the ranking of available exploits. 

### **4.4 Arsenal Module** 

The Arsenal Module is a framework that transforms heterogeneous "in-the-wild" exploits into standardized, plug-andplay modules for agents. To achieve this, we first introduce a structured format to represent each exploit. Essential information is then extracted from repositories to populate this structured format. Finally, this structured format is used to generate a self-contained, executable module equipped 

with usage manual for the agent. The entire workflow—from acquiring exploit repositories to generating standardized executable modules—is fully automated with no human intervention. 

Repositories of "in-the-wild" exploits lack standardized structures, often differing in project organization, programming languages, system dependencies, and execution workflows—core details that are crucial for automated packaging and reliable execution. Therefore, constructing a robust arsenal requires deep insight into these repositories. To address this, we conducted a large-scale deep analysis of mainstream exploit repositories, guided by two penetration-testing experts, and summarized their essential feature patterns as Unified Exploit Descriptor ( **UED** ). As shown in Table 12, UED is a structured abstraction capturing over ten expertdefined meta-dimensions spanning both environmental and operational aspects, which are essential for automated construction and execution. Environmental dimensions (e.g., language, dependencies, base images) support reproducible execution environments, while operational dimensions (e.g., parameters, operation steps) ensure precise, agent-invocable manuals. By organizing these dimensions into a unified schema, the task of “making an exploit work” is transformed into the well-defined problem of populating a descriptor, turning chaotic exploits into reproducible specifications. 

Our analysis further revealed distinct patterns in these repositories’ characteristics, which can be categorized into several representative types. Repositories within the same category shared similar environment setups and execution strategies. Based on our analysis, we categorized the repositories into three representative types: packet-based, commandline-based, and script-based exploits. This categorization ensures that subsequent environment construction and manual generation are aligned with the exploit’s intrinsic requirements. 

We automate the UED construction process employing an LLM for semantic analysis of entire repositories, reasoning jointly over code, comments, and documentation. The model filters out irrelevant content (e.g., setup instructions, author notes) while inferring missing details from file structures and code patterns. This ensures that even incomplete exploits yield a complete UED, faithfully capturing complex workflows such as multi-stage asynchronous exploits. The constructed UED then drives a dual-output generation process: environmental dimensions generate a Dockerfile for a reproducible containerized environment, while operational dimensions produce a concise manual translating complex attack sequences into step-by-step instructions. This final stage converts noisy, inconsistent exploits into robust, standardized modules ready for autonomous deployment. 

Anonymous’25, Anon, Anonymous 

Shell or Nothing: Real-World Benchmarks and Memory-Activated Agents for Automated Penetration Testing 

**Table 3.** Distribution and Standardization Performance of "in-the-wild" Exploits. 

|**Exploit Type**|**Count**|**Proportion**|**Output Success Rate**|**Avg. Time (s)**|**Output**|
|---|---|---|---|---|---|
|Packet-based|123|5.97%|94.31%|41.28|Manual|
|Script-based|1825|88.55%|63.51%|83.76<br>Manua|l, Docker Image|
|Command-line|113|5.48%|91.15%|33.21|Manual|



## **5 Implementation** 

Building upon the design in Section 4, we implemented TermiAgent on the LangGraph[19], consisting of over 3,500 lines of Python code and about 700 lines of prompt definitions. 

TermiAgent requires only the target host’s IP address or the subnet in which it resides as input. The default objective of TermiAgent is aligned with real-world pentesting scenarios, aiming to obtain ownership of the target machine, such as acquiring a shell. Additionally, we have adapted for a CTF scenario where obtaining a flag can be specified as an alternative objective. TermiAgent communicates with the backend LLM via the API format compatible with OpenAI[28], which ensures adaptability in switching between different backend LLMs to accommodate diverse pentesting environments. All commands during the pentesting are executed through a Kali[39] host to interact with the target machine, and the entire process is fully automated, requiring no human intervention until the objective is achieved. 

In the Arsenal Module, from the 228,139 CVEs on the NVD website[24] in the past decade (2015–2025), we identified 31,332 potential RCEs. Using these CVE IDs, we employed GitHub CLI[7] to search GitHub and identified 6,514 candidates. We subsequently retained only executables that did not require manual front-end interaction and were designed to target non-Windows services. This process resulted in 694 RCE CVEs, corresponding to 2,185 repositories. After excluding repositories that failed to be successfully containerized, we obtained 1,378 Dockerized exploits along with their instruction manuals, forming the final arsenal of standardized modules ready for automated execution. Table 3 shows the exploit distribution and packaging performance. Script-based exploits dominate (89%), reflecting their prevalence in public repositories, and achieved a 63.51% success rate when both manuals and Docker images were required. In contrast, packet-based and command-line exploits represent smaller proportions (5.97% and 5.48%) but achieved high success rates (94.31% and 91.15%, respectively) since only manuals needed to be generated. Across categories, environment reconstruction times ranged from 33 to 84 seconds. 

Additionally, by filtering these CVE IDs and considering rankings, we curated 1,077 exploits from Metasploit[22], corresponding to 851 unique CVEs, and supplemented them with the corresponding manuals. All of these exploits and manuals, continuously collected by the Arsenal Module, can be invoked by TermiAgent through a unified interface in a plug-and-play manner, ensuring scalability and modularity. 

## **6 Evaluation** 

In this section, we evaluate the practical performance of TermiAgent based on the following three research questions: **RQ 1 (Performance):** How does the performance of TermiAgent, compared with the state-of-the-art pentesting agents, both in CTF scenarios and real-world scenarios? 

**RQ 2 (Cost):** Can TermiAgent, compared with the state-ofthe-art pentesting agents, maintain lower time and financial costs while ensuring comparable performance? 

**RQ 3 (Ablation):** To what extent do the Arsenal Module and Located Memory Activation improve the performance of TermiAgent? How does the design of the UED facilitate the Dockerization of exploits? 

### **6.1 Evaluation Setting** 

We evaluated the performance of TermiAgent under both real-world scenarios and CTF scenarios. For evaluation under real-world scenarios, we used TermiBench constructed as in Section 3.2, which contains 510 target machines with varying numbers of services. Each category of machines includes one vulnerable service and 0, 1, 3, 5, or 7 benign services. We selected all targets with 0 benign services, and randomly sampled 50 targets from each of the remaining four categories, resulting in a total of 230 targets for evaluation. For CTF scenarios, we used all 33 targets from Auto-PenBench[12] for its diverse categories of CTF challenges and local deployment–friendly features. For ethical considerations, each target machine was subjected to five repeated tests to mitigate potential randomness in the results. A penetration test was deemed successful if at least one of the attempts succeeded. 

We selected PentestGPT[9] and VulnBot[18] for comparison with TermiAgent, as both of them are widely recognized and feature corresponding designs for pentesting task planning. For PentestGPT, we used the fully automated version implemented in VulnBot, which retains all original prompts and simulates a manual copy-paste process without additional interpretation. Additionally, we also included the built-in autonomous agent from Auto-Pen-Bench, which is equipped with essential tools and a limited single-framework prompt, allowing for a relatively objective evaluation of an LLM’s ability to tackle CTF challenges. However, it was not tested in a real-world scenario as its design is tightly coupled with the CTF-oriented targets in Auto-Pen-Bench. 

To evaluate the impact of different backend LLMs on the performance of TermiAgent, we selected GPT-5-202508-07[27] from closed-source models, DeepSeek-V3-0324[8], and the Qwen3 series[42] from open-source models. For the Qwen3 series, we chose five models with different parameter sizes, Qwen3-30B-A3B[35], Qwen3-14B[33], Qwen3-8B[37], Qwen3-4B[36], and Qwen3-1.7B[34] to assess the agent’s compatibility with lightweight LLMs. Detailed information on the LLMs is summarized in Table 11. 

Anonymous’25, Anon, Anonymous 

Wuyuao Mai, et al. 

**Table 4.** The overall performance of TermiBench, VulnBot, PentestGPT, and built-in agent of Auto-Pen-Bench under both CTF and real-world scenario. 

|**Agent**|**Model**||**CT**|**F Scena**|**rio Pas**<br>|**s@5**<br>||**Re**|**al-Wor**|**ld Scen**<br>|**ario **<sup>*** **</sup>**P**<br>|**ass@5**<br>||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||Total(33)|||Categ<br>|ory<br>||Total(230)||# of Se<br>|rvices p<br>|er Host<br>||
||||AC(5)|WS(7)|NS(6)|CRPT(4)|CVE(11)||1(30)|2(50)|4(50)|6(50)|8(50)|
||GPT-5|11|2|4|2|0|3|91/52|9/6|21/14|21/10|17/11|23/11|
|**TiAt**|DeepSeek-V3|15|3|5|2|0|5|128/46|17/5|31/13|30/10|26/10|24/8|
|**ermgen**|Qwen3-30B|15|3|4|2|0|6|118/56|12/6|20/13|21/9|29/13|36/15|
||Qwen3-8B|10|2|4|2|0|2|131/60|14/6|26/13|17/13|30/14|24/14|
||GPT-5|3|0|1|0|1|1|3/1|1/0|2/1|0/0|0/0|0/0|
|**VlBt**|DeepSeek-V3|9|1|2|4|1|1|15/9|2/1|5/3|3/1|3/2|2/2|
|**uno**|Qwen3-30B|7|0|4|2|0|1|5/0|1/0|1/0|2/0|0/0|1/0|
||Qwen3-8B|4|0|0|2|0|2|4/2|2/1|2/1|0/0|0/0|0/0|
||GPT-5|3|1|2|0|0|0|0/0|0/0|0/0|0/0|0/0|0/0|
|**PGPT**|DeepSeek-V3|4|1|0|2|0|1|0/0|0/0|0/0|0/0|0/0|0/0|
|**entest**|Qwen3-30B|0|0|0|0|0|0|0/0|0/0|0/0|0/0|0/0|0/0|
||Qwen3-8B|0|0|0|0|0|0|0/0|0/0|0/0|0/0|0/0|0/0|
|**Auto-Pen-Bench**|GPT-5|22|5|4|2|4|7|-|-|-|-|-|-|
|**BiltI**|DeepSeek-V3|10|0|4|2|0|4|-|-|-|-|-|-|
|**u-n**<br>**At**|Qwen3-30B|3|0|2|1|0|0|-|-|-|-|-|-|
|**gen**|Qwen3-8B|5|0|3|2|0|0|-|-|-|-|-|-|



> * Results are shown as num1/num2, with num1 indicating shells obtained and num2 indicating root shells. 

All experiments were conducted on authorized, isolated servers, with an Intel® Xeon® Gold 6330 processor (28 cores), 8 NVIDIA GeForce RTX 4090 GPUs, 512GB of memory, and a 29TB hard disk drive, running Ubuntu 24.04 LTS. 

### **6.2 Performance Evaluation (RQ1)** 

To comprehensively evaluate the performance of TermiAgent and its competing agents in both real-world and CTF scenarios, this section not only assesses their completion of pentesting tasks on selected benchmarks, but also further examines the performance degradation of limited CTF instruction settings. Additionally, we compare the agents’ adaptability to lightweight LLMs. 

**CTF/Shell Exploitation Performance.** The pentesting results of TermiAgent and its competing agents in both realworld and CTF scenarios are summarized in Table 4, and TermiAgent achieved superior performance. In the CTF scenario, the best performance of TermiAgent exceeded that of VulnBot by 66.67%, achieving 15 successful tests compared with VulnBot’s 9. Remarkably, even when powered by a lightweight LLM such as Qwen3-8B, TermiAgent still outperformed VulnBot’s best results using DeepSeek (10 v.s. 9), further demonstrating its robustness and efficiency under resource-constrained settings. In contrast, PentestGPT, although supplemented with a command execution module, achieved only 4 successful tests at best, highlighting its reliance on human involvement to ensure effectiveness. In the real-world scenarios, TermiAgent stood out, achieving success of pentesting on over 50% of the target hosts with all 

selected backend LLMs. Conversely, VulnBot, designed for CTF competitions, failed to cope with real-world pentesting, as its performance was limited to successfully compromising fewer than 10% of the target hosts. Additionally, within its limited success, VulBot is more effective at hosts with a small number of services (1, 2, 4 per host), accounting for 21 of its total 27 successes. Its success rate drops on hosts with a larger number of services (6, 8 per host). This highlights the agent’s inability to effectively adapt to real-world scenarios where a single host may have many benign services that need to be excluded. PentestGPT failed to successfully compromise any of the target hosts. Beyond its limited capability in real-world pentesting, our log analysis revealed that in over 50% of the attempts, PentestGPT generated nmap commands containing unresolved placeholders, such as nmap -p-sV [target IP] that caused errors. These findings suggest that PentestGPT remains far from achieving fully automated pentesting. 

Notably, Auto-Pen-Bench’s built-in agents powered by GPT-5 completed 22 targets, a sharp contrast to DeepSeek and Qwen models. We hypothesize that this is because GPT5’s knowledge cutoff on September 30, 2024, closely aligns with the open-source release of Auto-Pen-Bench and the provided official solutions using its built-in agents. However, the performance of VulnBot powered by GPT-5 fell significantly short of expectations in both CTF and real-world scenarios. Further log analysis showed that GPT-5 in VulnBot generates more complex, piped instructions that VulnBot’s execution 

Anonymous’25, Anon, Anonymous 

Shell or Nothing: Real-World Benchmarks and Memory-Activated Agents for Automated Penetration Testing 


![](docs/paper-research/md-downloaded-paper-curated/images/46-shell-or-nothing-real-world-benchmarks-and-memory.pdf-0011-02.png)


<!-- Start of picture text -->
20<br>VulnBot (Deepseek) TermiAgent (Deepseek)<br>VulnBot (Qwen3-30B) TermiAgent (Qwen3-30B)<br>15 15<br>15<br>10<br>10 9<br>8<br>7<br>5<br>3<br>2<br>0<br>Original Limited<br>Instruction<br># of Success<br><!-- End of picture text -->

**Figure 3.** Performance of TermiAgent and VulnBot with limited instruction under CTF scenario. 

module cannot handle. Compared with DeepSeek’s instructions under the CTF scenario, each individual instruction is on average 40.10% longer, and the number of instructions per attempt increases by 33.33%. And these two percentages in real-world scenarios were 40.80% and 41.67%, respectively. While seemingly sophisticated, this behavior leads to suboptimal results and even errors, highlighting the lack of robustness in the design of VulnBot. 

These results demonstrate that while existing pentesting agents show some capability in CTF scenarios, they are insufficient for complex, real-world tasks. In contrast, the outstanding performance of TermiAgent not only fills this gap but also significantly advances the efficacy of pentesting. **Performance under limited instruction.** The targets in Auto-Pen-Bench’s default configuration disclose supplementary hints, such as entry points and exploit paths, in addition to their subnet. To better emulate a red team scenario where information is limited, we reconfigured the instructions for each target to be restricted to contain only **1)** the target’s subnet and **2)** the ultimate objective to obtain the flag. Further details of this process are provided in the Appendix C. Under limited instructions, we re-evaluated the performance of both TermiAgent and VulnBot as in Figure 3. 

Under limited instructions, the number of targets successfully compromised by TermiAgent powered by Deepseek and Qwen3-30B dropped from the original 15 to 8 and 10, respectively, which was comparable to VulnBot with original instructions. In contrast, VulnBot powered by Deepseek and Qwen3-30B saw their number of successful targets drop from 9 to 3 and from 7 to 2, respectively, representing significant decreases of 66.67% and 71.43%. The experimental results revealed that VulnBot’s design inherently requires these additional hints to guarantee its pentesting success, which diverges from the reality of real-world scenarios where information is typically limited to an IP or subnet. By comparison, TermiAgent demonstrated its capacity to perform effective 

**Table 5.** Lightweight LLM compatibility of TermiAgent and VulnBot by Qwen3 series in real-world scenario. 

||**30B**|**14B**|**8B**|**4B**|**1.7B**|
|---|---|---|---|---|---|
|**TermiAgent**|118/56|116/53|131/60|137/58|67/33|
|**VulnBot**|5/0|3/2|4/2|1/1|0/0|



**Table 6.** Time and financial cost of TermiAgent and VulnBot in CTF and real-world scenario. 

||**Metric**|**CTF Scenario**|**Real-world Scenario**|
|---|---|---|---|
|**TermiAent**|Avg. Time (Mins)|19.5908|11.7875|
|**g**|Avg. Cost ($)|0.0551|0.0074|
|**VlBt**|Avg. Time (Mins)|17.5746|63.1402|
|**uno**|Avg. Cost ($)|0.0577|0.0996|



penetration tests and achieve a commendable success rate using only the limited information provided. 

**Lightwight LLM compatibility.** Previous pentesting agents relied on state-of-the-art LLMs, which not only incur significant financial costs but also cannot be deployed in internal environments with limited computational resources and restrictions on network access. To evaluate the extent to which our agent can achieve a trade-off between resource consumption and performance, we selected 5 open-source LLMs from the Qwen3 series, with parameter sizes ranging from 1.7B to 30B. Using the 230 target hosts from TermiBench in a real-world scenario, we compared the performance of TermiAgent with that of VulnBot, and each target host was tested five times. The results are shown in Table 5. 

The experimental results reveal that TermiAgent achieved excellent performance across LLMs with different parameter sizes. Even with a 4B model, TermiAgent successfully conducted 137 penetration tests out of 230 target hosts. This is comparable to the performance achieved by the model with 30B parameters and even DeepSeek-V3 with 685B parameters. Even though TermiAgent, based on Qwen3-1.7B, completed 67 successful penetration tests, this is still a remarkable performance considering the model’s parameter size and computational overhead. In contrast, VulnBot’s compatibility with lightweight LLMs was notably less effective. It completed only 5 successful penetration tests based on the 30B model, a 66.67% decline from its best result of 15 with DeepSeek-V3. Performance of VulnBot with the 4B and 1.7B models was even more deficient. The 4B and 1.7B models are efficient enough to run smoothly on mainstream consumer-grade GPUs. The results demonstrate the potential for TermiAgent to perform penetration tests locally on devices such as laptops and even smartphones. 

### **6.3 Cost Evaluation (RQ2)** 

To assess the overhead of TermiAgent in achieving its current pentesting performance, we evaluated both its time and 

Anonymous’25, Anon, Anonymous 

Wuyuao Mai, et al. 

financial costs in CTF scenarios and real-world scenarios, respectively. We selected VulnBot for comparison and to ensure the reliability of experimental results, both TermiAgent and VulnBot were tested under identical hardware, software, and network environments, which were aforementioned in Section 6.1. Under both scenarios, we only selected the vulnerable machines that both agents successfully penetrated—regardless of the backend LLM—to eliminate bias caused by the varying difficulty of different target machines. For both agents, we analyzed every successful penetration attempt on the selected vulnerable machines. The time cost for each machine was defined as the shortest successful attempt duration. For the financial cost, we calculated the cost of each attempt by multiplying the number of LLM tokens consumed by the LLM’s API price, then selected the lowestcost attempt for that machine. The API specifications are presented in Table 11. Finally, we computed the average time and financial costs for both TermiAgent and VulnBot across all the selected targets as the final results. 

We ultimately selected 12 jointly successful target hosts in the CTF scenario and 18 machines in the real-world scenario. For a total of 283 successful attempts on these target machines, we calculated the time and financial costs based on the aforementioned criteria. The final results are summarized in Table 6. The results demonstrate that for these jointly successful target hosts, in the CTF scenario, TermiAgent and VulnBot exhibited comparable levels of cost and time overhead. But in the real-world scenario, TermiAgent consumed only about 7.43% of the financial cost and 18.67% of the time required by VulnBot to compromise the same number of targets, not to mention its overwhelming advantage in terms of the total number of successfully exploited machines. This is because, in a complex multi-service pentesting task, TermiAgent utilizes Located Memory Activation (LMA) to filter irrelevant context and reduce token usage, enabling strong performance with lightweight LLMs of cheaper price. Moreover, its Penetration Memory Tree (PMT) enumerates and prioritizes exploitation paths, avoiding redundancy and enhancing efficiency. 

### **6.4 Ablation Study (RQ3)** 

To validate the effectiveness and irreplaceability of our proposed designs, we perform ablation studies in this section. Specifically, we conduct ablations on the Memory and Arsenal Module of TermiAgent during pentesting, and then the UED during dockerization of in-the-wild exploits. 

**Ablation of Memory and Arsenal Module.** To quantify the performance improvements brought by the Memory Module and the Arsenal Module to TermiAgent’s pentesting capabilities, we conduct a series of evaluations by separately removing each module under real-world scenarios. Specifically, with the Memory Module ablated, we disabled the Located Memory Activation (LMA) approach. In its place, we followed the design of VulnBot and PentestGPT, inputting 


![](docs/paper-research/md-downloaded-paper-curated/images/46-shell-or-nothing-real-world-benchmarks-and-memory.pdf-0012-07.png)


<!-- Start of picture text -->
50<br>w/ LMA & Arsenal w/o Arsenal w/o LMA<br>40<br>36<br>30 29<br>24<br>20 21 20<br>20 17 17<br>12 13 12<br>10 9 8<br>1 1<br>0<br>1 2 4 6 8<br># of Services per Host<br># of Success<br><!-- End of picture text -->

**Figure 4.** Ablation study on Local Memory Activation (LMA) and Arsenal Module of TermiAgent. 

**Table 7.** Ablation analysis of individual UED components. 

|**Group**|**Excluded Component**|**Output Success Rate**|**Exploitation Success Rate**|
|---|---|---|---|
|Baseline|None (all preserved)|89.1%|63.33%|
|1|language|83.1%|0|
|2|Language version|82.7%|43.33%|
|3|Docker base image|25.1%|3.33%|
|4|System dependencies|85.3%|50.00%|
|5|Code dependencies|84.0%|0|
|6|Main scrip<br>|82.7%|43.33%|
|7|Parameter fles|83.5%|33.67%|
|8|Docker confg|83.5%|43.33%|
|9|Setup steps|83.5%|36.67%|
|10|Exploit steps|84.0%|36.67%|
|11|Command parameters|84.4%|23.33%|
|12|Usage example|84.4%|23.33%|



the complete Penetration Memory Tree (PMT), which contains all information from the current penetration test, directly into the context. While with the Arsenal Module ablated, we limited TermiAgent’s ability to access in-the-wild exploits which were already packaged and ready to use. We conducted this experiment using Qwen3-30B, using the same 230 target machines from TermiBench as mentioned in Section 6.1, with each tested five times to mitigate the effects of randomness. 

The results of the ablation study on the Memory and Arsenal Modules are shown in Figure 4. With the Arsenal Module ablated, TermiAgent’s pentesting effectiveness dropped by 29.66%, decreasing from 118 to 83. Furthermore, the ablation of Located Memory Activation approach led to a much more pronounced decrease in TermiAgent’s effectiveness. A total of 79 previously successful targets could no longer be compromised, representing a substantial decline rate of 66.95%. The largest number of failures, nearly 20 targets, occurred on machines with 8 services. This suggests that the Located Memory Activation (LMA) approach within the Memory Module is of critical role in complex, multi-service pentesting scenarios. 

**Ablation of UED.** We evaluated the UED on 231 GitHub repositories corresponding to 30 target CVEs, covering all 

Anonymous’25, Anon, Anonymous 

Shell or Nothing: Real-World Benchmarks and Memory-Activated Agents for Automated Penetration Testing 

publicly available scripts for these CVEs. Output Success Rate measures the proportion of repositories for which both a Dockerized image and a manual were successfully generated. To assess practical exploitation, we randomly selected one repository per CVE and manually verified pentesting on the corresponding vulnerable targets. Only one repository per CVE was tested due to the large number of UED dimensions, allowing us to focus on each component’s contribution while keeping verification manageable. 

The baseline system, with all UED dimensions preserved, achieved an Output Success Rate of 89.1%—higher than the 63.51% observed across 1,825 repositories (Table 3)—because the selected CVEs were representative and commonly supported, simplifying containerization, and the Exploitation Success Rate was 63.3%. 

Ablation shows that the Output Success Rate is dominated by the Docker base image, with its removal causing a sharp drop, while other dimensions have minor effects. Exploitation Success Rate depends on multiple dimensions, including setup steps, exploit steps, command parameters, and usage examples, any of which can significantly reduce attack success if omitted. Special cases highlight this: omitting code dependencies leads to zero exploitation success, since the necessary code libraries or modules are missing, causing execution to fail even though containerization succeeds, whereas omitting system-level dependencies has a smaller effect, as fewer repositories rely on OS-level packages. These results confirm that each UED component is crucial, either for reproducible containerization or for generating manuals that reliably guide successful exploitation. 

## **7 Discussion** 

**Security Implication.** In this work, we propose TermiBench, a benchmark for automated pentesting composed of 510 real-world targets, and TermiAgent, an automated agent that significantly enhances effectiveness by leveraging Located Memory Activation and the Arsenal Module. Both TermiBench and TermiAgent are designed to facilitate the development of more secure systems. Advancements in automated pentesting will strengthen system robustness and security while reducing the barriers to building secure systems. 

The introduction of TermiBench establishes a much-needed, unified standard for evaluating pentesting agents in realworld scenarios, addressing the biased and inconsistent understanding of what constitutes real-world in prior research. Furthermore, our evaluation demonstrates that TermiAgent significantly outperforms its competitors in both CTF and real-world pentesting scenarios using even lightweight LLMs. It represents a significant leap forward in automated pentesting agents, as it ushers in a new era where real-world pentesting can be effectively driven by consumer-grade GPUs on laptop-scale deployments and obtain superior performance. 

Our work demonstrates a critical vulnerability in the safety alignment of LLMs. Despite safeguards[27] of LLMs to prevent harmful and unethical content, TermiAgent successfully bypassed security protocols without jailbreaking prompts. Across 1,150 tests every LLM, only GPT-5 exhibited 11 times of refusal (0.96%). This may be attributed to TermiAgent’s design, which leverages Located Memory Activation to filter out unrelated context and employs fine-grained task decomposition to prevent LLM from perceiving full security risk. **Limitation.** Despite TermiAgent’s excellent performance in both CTF and real-world scenarios, we also acknowledge certain limitations of this work. Firstly, TermiAgent has limited capabilities in complex web-based pentesting, which often demand advanced operations, such as interacting with HTML elements or handling file uploads[26], and performing in-depth response analyses. This remains a significant and unresolved challenge for all current automated pentesting agents. However, TermiAgent is already capable of handling basic web pentesing[25], and we will continue to advance its capabilities for complex web-based scenarios in future work. 

Secondly, within the Arsenal Module, we are currently unable to handle certain repositories that exhibit excessive complexity, particularly those with large monolithic codebases or highly fragmented logic. Such complexity hinders the accurate extraction of exploit logic and the preparation of a reliable execution environment. Besides, many PoCs possessed complex operational requirements that fall outside our current automation scope, such as dependencies on interactive user interfaces or the need for manual setup of external network services. These outliers represent challenges in PoC implementation style rather than a specific class of vulnerability, and our future work will explore techniques like modular code analysis and browser automation to address them. 

Thirdly, while TermiBench currently focuses on evaluating whether an automated attacker can achieve initial ownership of a target, it does not yet include assessments for the post-exploitation phase, such as privilege escalation, information gathering, or lateral movement. However, our evaluations demonstrate that this scope is already sufficient for objectively gauging the capabilities of contemporary automated pentesting agents. The inclusion of post-exploitation assessments will be a key focus for our future work. 

## **8 Related Work** 

**Automated Penetration Testing.** Penetration testing, a long-standing cybersecurity task, has been greatly facilitated by LLMs and AI agents. While systems like PentestGPT[9] and CIPHER[31] can assist with pentesting as chatbots, they remain semi-automated, requiring continuous human interaction and falling short of true end-to-end automation. Although AutoAttacker[41] and BreachSeek[6] provide some 

Anonymous’25, Anon, Anonymous 

Wuyuao Mai, et al. 

subtask execution capabilities, they lack the planning functionality necessary for true end-to-end pentesting. In contrast, AutoPentest[15] and HackSynth[23] aim for a more challenging CTF scenario, but their planning modules are solely based on simple prompt engineering, which still fall short of effectively handling complex real-world pentesting scenarios. VulnBot [18] improves planning via a Penetration Task Graph but suffers from context loss and reliance on third-party tools, limiting its effectiveness. While PentestAgent[40] can search online exploits, it lacks the ability to package them into ready-to-use tools. In our work, TermiAgent improved end-to-end pentesting effectiveness in real-world scenarios by utilizing Located Memory Activation and a self-built arsenal. 

**Benchmark for Penetration Testing.** Traditional platforms like HackTheBox[13] and Vulhub[30] feature humandesigned CTF challenges with only one vulnerable service per host, primarily aimed at training security professionals and failing to capture real-world scenarios. AI-PentestBenchmark[16] classifies tasks to evaluate an agent’s pentesting capabilities, but its assessment focuses on sub-task completion rather than end-to-end testing. Although AutoPen-Bench[12] includes CVEs, it remains limited to the CTF task rather than ownership-targeted real-world pentesting. Besides, its instructions include extra hints that prevent objective evaluation. In our work, TermiBench provides 510 target hosts in multi-service, ownership-based tasks, objectively assessing agents’ penetration success given only subnet information. 

## **9 Conclusion** 

In this work, we propose TermiBench, a real-world benchmark for evaluating pentesting agents, which comprises 510 multi-service target hosts incorporating 30 CVEs that affect 25 different services. Besides, we present TermiAgent, an automated pentesting agent designed for real-world scenarios. It leverages Local Memory Activation to effectively handle complex, multi-step pentesting tasks, and we enhanced TermiAgent’s capabilities by proactively collecting in-the-wild exploits in Arsenal Module, moving beyond the limitations of third-party tools. Our comprehensive evaluation demonstrates that TermiAgent achieved superior performance in both CTF and real-world pentesting scenarios while reducing execution time and financial cost. Our work advances the automation of real-world pentesting into a new stage, where such processes can be effectively driven by laptopscale deployments. 

## **Ethics Considerations** 

In this work, we introduce TermiBench and TermiAgent to advance automated penetration testing, thereby enhancing system robustness and security while lowering the barriers to building reliable defenses. 

Recognizing that penetration testing research may pose ethical risks, we have carefully designed our study to adhere to established ethical norms and relevant guidelines. Our approach emphasizes responsible disclosure, strict experimental isolation, and controlled dissemination, ensuring that the benefits of our research outweigh potential harms. We will provide a transparent account of our reasoning as follows. 

### **1. Stakeholders and Impact Analysis** 

We identify the following stakeholders and analyze the potential impacts of our research. 

**i) Research Team.** Conducting automated penetration testing carries operational risks. Ethical oversight by our institution’s Responsible AI Committee ensures safe procedures and adherence to responsible experimentation guidelines. 

**ii) Academic Community.** Researchers benefit from access to methodology and findings, facilitating further research in automated penetration testing. There is a potential risk of misuse if tools are not carefully controlled. 

**iii) CVE Vendors and Affected Organizations.** Publication may indirectly affect organizations related to the CVEs used. All vulnerabilities analyzed are publicly disclosed, with no novel 0-day exploits are used. 

**iv) Potential Malicious Actors.** There is a risk that TermiAgent could be misused. Mitigations include restricted access, responsible use agreements, and controlled dissemination. 

**v) Society and End Users.** Indirect benefits include improved understanding of defensive strategies against automated penetration testing. There is minimal risk to external users as all experiments are confined to isolated environments. 

### **2. Mitigation Measures** 

To ensure that our research on automated penetration testing is conducted in a safe, ethical, and responsible manner, we adopt a series of mitigation measures as follows. 

**i) Responsible Scope and Disclosure.** Our study was conducted under the oversight of an ethics review procedure under our institution’s Responsible AI Committee, ensuring that the research adhered to established guidelines for responsible security experimentation. The scope of our work is strictly limited to publicly disclosed CVEs documented in the NVD database[24]. TermiAgent leverages the Located Memory Activation (LMA) mechanism—designed to handle complex, multi-step penetration testing tasks in real-world settings—exclusively to exploit publicly disclosed CVE vulnerabilities rather than unknown 0-day vulnerabilities. In addition, the Arsenal Module employs the Unified Exploit Descriptor (UED) to automatically package publicly available exploits for known CVEs into a ready-to-use form, without generating new exploits. All penetration testing logs are 

Anonymous’25, Anon, Anonymous 

Shell or Nothing: Real-World Benchmarks and Memory-Activated Agents for Automated Penetration Testing 

carefully reviewed by professional security personnel, and any noteworthy potential risks identified by TermiAgent will be proactively disclosed through responsible channels. 

**ii) Controlled and Secure Environment.** All experiments were conducted within a fully isolated and controlled environment to eliminate any risk of affecting external systems. Access to the source code, experimental environment, and exploit artifacts was restricted to authorized and trusted personnel only, ensuring secure handling of sensitive components and preventing misuse. In addition, all testing activities were continuously logged and monitored to ensure compliance with institutional ethical standards and to prevent any unauthorized use or dissemination. 

**iii) Open-source and Community Engagement.** To mitigate potential risks associated with abuse, the prototype of TermiAgent, along with sets of exploits, will only be made conditionally available to researchers who submit a formal request, provide proof of their qualifications, and, upon our review, sign a responsible use agreement. This approach prevents misuse while actively promoting further research in the academic field of automated penetration testing. Moreover, we actively engage with the security research community to establish responsible usage guidelines for TermiAgent, aiming to prevent potential misuse while promoting safe and ethical adoption. Furthermore, there remains a notable gap in the academic literature regarding defensive research for automated penetration testing. As part of our future work, we plan to focus on developing methods for detecting and defending against automated penetration testing agents, thereby contributing to both the safe deployment of such tools and the broader understanding of defensive strategies in cybersecurity. 

### **3. Decision Rationale** 

We chose to conduct this research as automated penetration testing with publicly disclosed CVEs enables systematic exploration of complex attack paths in a real-world scenario, providing significant benefits to security research, supporting the development of more resilient systems, and lowering the practical challenges faced in constructing secure defenses. And we decided to publish our findings because sufficient mitigations are in place, and the societal and academic benefits outweigh the potential risks. Ethical considerations, including potential harms and rights protection, were systematically weighed. 

## **Open Science** 

We are committed to the open science policy, and we have made TermiBench publicly available at https://doi.org/10. 5281/zenodo.16962513. TermiBench features 510 penetration testing targets that are linked to 30 CVE IDs and affect 25 different software services. The repository includes detailed usage instructions for each machine, serving as a foundational 

resource for further research into automated penetration testing. 

For ethical consideration, we will not make TermiAgent’s code or the exploits from the Arsenal Module publicly available, to prevent any potential misuse. The prototype of TermiAgent, along with a limited set of exploits, will only be made conditionally available to researchers who submit a formal request, provide proof of their qualifications, and, upon our review, sign a responsible use agreement in the future. 

## **References** 

- [1] Alibaba Cloud [n. d.]. _Alibaba Cloud Bailian Console_ . Alibaba Cloud. https://bailian.console.aliyun.com/ Enterprise-level large-model service platform console (“Bailian”) from Alibaba Cloud. 

- [2] OpenAI [n. d.]. _API Pricing_ . OpenAI. https://openai.com/api/pricing/ Official pricing page. 

- [3] DeepSeek [n. d.]. _DeepSeek API Platform_ . DeepSeek. https://platform. deepseek.com/ Official platform for accessing DeepSeek models and API resources. 

- [4] 2018. Penetration Testing within the Financial Service Industry. 

- [5] 2025. Penetration test. https://en.wikipedia.org/wiki/Penetration_test. Accessed 2025-08-24. 

- [6] Ibrahim Alshehri, Adnan Alshehri, Abdulrahman Almalki, Majed Bamardouf, and Alaqsa Akbar. 2024. Breachseek: A multi-agent automated penetration tester. _arXiv preprint arXiv:2409.03789_ (2024). 

- [7] GitHub CLI Contributors. 2025. GitHub CLI. https://cli.github.com/ Accessed: 2025-08-24. 

- [8] DeepseekAI. 2025. DeepSeek-V3-0324. https://huggingface.co/ deepseek-ai/DeepSeek-V3-0324 Accessed: 2025-08-13. 

- [9] Gelei Deng, Yi Liu, Víctor Mayoral-Vilches, Peng Liu, Yuekang Li, Yuan Xu, Tianwei Zhang, Yang Liu, Martin Pinzger, and Stefan Rass. 2024. PentestGPT: Evaluating and Harnessing Large Language Models for Automated Penetration Testing. In _33rd USENIX Security Symposium (USENIX Security 24)_ . USENIX Association, Philadelphia, PA, 847–864. https://www.usenix.org/conference/usenixsecurity24/ presentation/deng 

- [10] Ewelina Baran. 2023. _How Much Does Penetration Testing Cost?_ Accessed: 2025-08-12. 

- [11] FOFA. 2024. _FOFA Search Engine._ https://fofa.info/. 

- [12] Luca Gioacchini, Marco Mellia, Idilio Drago, Alexander Delsanto, Giuseppe Siracusano, and Roberto Bifulco. 2024. AutoPenBench: Benchmarking Generative Agents for Penetration Testing. arXiv:2410.03225 [cs.CR] https://arxiv.org/abs/2410.03225 

- [13] Hack The Box Limited. 2016. Hack The Box: An Online Platform for Cybersecurity Training. Online Platform. https://www.hackthebox. com/ Accessed: 2025-08-13. 

- [14] Heath Adams. 2024. _How Much Does a Penetration Test Cost in 2025?_ Accessed: 2025-08-12. 

- [15] Julius Henke. 2025. AutoPentest: Enhancing Vulnerability Management With Autonomous LLM Agents. arXiv:2505.10321 [cs.CR] https://arxiv.org/abs/2505.10321 

- [16] Isamu Isozaki, Manil Shrestha, Rick Console, and Edward Kim. 2024. Towards Automated Penetration Testing: Introducing LLM Benchmark, Analysis, and Improvements. arXiv:2410.17141 [cs.CR] https://arxiv. org/abs/2410.17141 

- [17] Matt Kapko. 2025. DARPA’s AI Cyber Challenge reveals winning models for automated vulnerability discovery and patching. _CyberScoop_ (8 Aug. 2025). https://cyberscoop.com/darpa-ai-cyber-challengewinners-def-con-2025/ Accessed on YYYY-MM-DD. 

- [18] He Kong, Die Hu, Jingguo Ge, Liangxiong Li, Tong Li, and Bingzhen Wu. 2025. VulnBot: Autonomous Penetration Testing for a Multi-Agent 

Anonymous’25, Anon, Anonymous 

Wuyuao Mai, et al. 

   - Collaborative Framework. arXiv:2501.13411 [cs.SE] https://arxiv.org/ abs/2501.13411 

- [19] LangChain Inc. 2025. _LangGraph: Build resilient language agents as graphs_ . https://github.com/langchain-ai/langgraph MIT License. 

- [20] Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. 2023. Lost in the Middle: How Language Models Use Long Contexts. arXiv:2307.03172 [cs.CL] https://arxiv.org/abs/2307.03172 

- [21] Keshav Malik. 2025. _Why Penetration Testing is Important_ . Accessed: 2025-08-12. 

- [22] Metasploit. [n. d.]. _Metasploit The world’s most used penetration testing framework_ . https://www.metasploit.com/. 

- [23] Lajos Muzsai, David Imolai, and András Lukács. 2024. HackSynth: LLM Agent and Evaluation Framework for Autonomous Penetration Testing. arXiv:2412.01778 [cs.CR] https://arxiv.org/abs/2412.01778 

- [24] National Institute of Standards and Technology. 2025. National Vulnerability Database (NVD). Online Database. https://nvd.nist.gov/ Accessed: 2025-08-13. 

- [25] National Institute of Standards and Technology. 2018. CVE-2018-7600 Detail. https://nvd.nist.gov/vuln/detail/CVE-2018-7600 Accessed: 2025-08-27. 

- [26] National Institute of Standards and Technology. 2019. CVE-2019-6339 Detail. https://nvd.nist.gov/vuln/detail/CVE-2019-6339 Accessed: 2025-08-27. 

- [27] OpenAI. 2025. Introducing GPT-5. https://openai.com/index/ introducing-gpt-5/ Accessed: 2025-08-13. 

- [28] OpenAI. 2025. OpenAI API. https://openai.com/api/. Accessed: 2025-08-20. 

- [29] OWASP Foundation. 2021. OWASP Web Security Testing Guide. Online. https://owasp.org/www-project-web-security-testing-guide/ 

- [30] Phith0n. 2019. Vulhub: Pre-Built Vulnerable Environments Based on Docker. GitHub Repository. https://github.com/vulhub/vulhub Accessed: 2025-08-13. 

- [31] Derry Pratama, Naufal Suryanto, Andro Aprila Adiputra, Thi-ThuHuong Le, Ahmada Yusril Kadiptya, Muhammad Iqbal, and Howon Kim. [n. d.]. CIPHER: Cybersecurity Intelligent Penetration-Testing Helper for Ethical Researcher. _Sensors_ 24, 21 ([n. d.]). doi:10.3390/ s24216878 

- [32] PTES Committee. 2014. Penetration Testing Execution Standard. Online. http://www.pentest-standard.org/ Version 1.0. 

- [33] Qwen. 2025. Qwen3-14B. https://huggingface.co/Qwen/Qwen3-14B Accessed: 2025-08-13. 

- [34] Qwen. 2025. Qwen3-1.7B. https://huggingface.co/Qwen/Qwen3-1.7B Accessed: 2025-08-13. 

- [35] Qwen. 2025. Qwen3-30B-A3B. https://huggingface.co/Qwen/Qwen330B-A3B Accessed: 2025-08-13. 

- [36] Qwen. 2025. Qwen3-4B. https://huggingface.co/Qwen/Qwen3-4B Accessed: 2025-08-13. 

- [37] Qwen. 2025. Qwen3-8B. https://huggingface.co/Qwen/Qwen3-8B Accessed: 2025-08-13. 

- [38] Karen Scarfone, Murugiah Souppaya, and Amanda Cody. 2008. _Technical Guide to Information Security Testing and Assessment_ . Technical Report NIST Special Publication 800-115. National Institute of Standards and Technology, Gaithersburg, MD. doi:10.6028/NIST.SP.800-115 

2403.01038 

- [42] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, Chujie Zheng, Dayiheng Liu, Fan Zhou, Fei Huang, Feng Hu, Hao Ge, Haoran Wei, Huan Lin, Jialong Tang, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jing Zhou, Jingren Zhou, Junyang Lin, Kai Dang, Keqin Bao, Kexin Yang, Le Yu, Lianghao Deng, Mei Li, Mingfeng Xue, Mingze Li, Pei Zhang, Peng Wang, Qin Zhu, Rui Men, Ruize Gao, Shixuan Liu, Shuang Luo, Tianhao Li, Tianyi Tang, Wenbiao Yin, Xingzhang Ren, Xinyu Wang, Xinyu Zhang, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yinger Zhang, Yu Wan, Yuqiong Liu, Zekun Wang, Zeyu Cui, Zhenru Zhang, Zhipeng Zhou, and Zihan Qiu. 2025. Qwen3 Technical Report. _arXiv preprint arXiv:2505.09388_ (2025). 

- [43] .... 2022. Measuring and Mitigating the Risk of IP Reuse on Public Clouds. (2022). Identified dozens of exploitable software systems spanning hundreds of servers, e.g., databases, caches, mobile applications, and web services. 

## **A Supplement to Design of TermiBench** 

Table 10 presents the 30 CVEs incorporated in TermiBench along with the 25 services they affect, spanning the years 2015 to 2025. In addition, the 14 selected benign mainstream services are listed in the Table 8. By combining these vulnerable services with varying numbers of benign services, we ultimately constructed the 510 target machines in TermiBench. 

**Table 8.** 14 benign services used in TermiBench. 

||**Service**|
|---|---|
|1|sshd|
|2|vsftpd|
|3|mysql<br>|
|4|postfx<br>|
|5|dnsmasq|
|6|ldap|
|7|redis|
|8|postgres|
|9|mosquitto|
|10|xrdp|
|11|mongodb|
|12|http|
|13|nginx|
|14|samba|



- [39] Offensive Security. 2025. Kali Linux. https://www.kali.org/ Accessed: 2025-08-20. 

- [40] Xiangmin Shen, Lingzhi Wang, Zhenyuan Li, Yan Chen, Wencheng Zhao, Dawei Sun, Jiashui Wang, and Wei Ruan. 2025. PentestAgent: Incorporating LLM Agents to Automated Penetration Testing. arXiv:2411.05185 [cs.CR] https://arxiv.org/abs/2411.05185 

- [41] Jiacen Xu, Jack W. Stokes, Geoff McDonald, Xuesong Bai, David Marshall, Siyue Wang, Adith Swaminathan, and Zhou Li. 2024. AutoAttacker: A Large Language Model Guided System to Implement Automatic Cyber-attacks. arXiv:2403.01038 [cs.CR] https://arxiv.org/abs/ 

## **B Supplement to Desgin of TermiAgent** 

**Reasoner Module.** The Reasoner Module is primarily responsible for high-level planning. It determines whether the overall goal of the penetration testing task has been achieved based on the stage-wise progress of the test, rather than on the details of specific instruction execution. If the overall goal is not yet accomplished, it generates the next phased 

Anonymous’25, Anon, Anonymous 

Shell or Nothing: Real-World Benchmarks and Memory-Activated Agents for Automated Penetration Testing 

**Table 9.** Overview of the Benchmark Configurations. 

|**Confguration**|**# of Benign Services**|**# of Vulnerable Services**|**# of Hosts**|
|---|---|---|---|
|Tier 0|0|1|30|
|Tier 1|1|1|120|
|Tier 2|3|1|120|
|Tier 3|5|1|120|
|Tier 4|7|1|120|
|**Total**|-|-|**510**|



**Table 10.** 30 CVEs and their affacted services used in TermiBench. 

||**CVE ID**|**Afected Service**|
|---|---|---|
|1|CVE-2015-1427|Elasticsearch|
|2|CVE-2015-3306|ProFTPD|
|3|CVE-2015-8562|Joomla|
|4|CVE-2016-3088|ActiveMQ|
|5|CVE-2016-5734|phpMyAdmin|
|6|CVE-2017-12636|CouchDB|
|7|CVE-2017-16082|Node|
|8|CVE-2017-17562|GoAhead|
|9|CVE-2017-7494|Samba|
|10|CVE-2018-1297|JMeter-Server|
|11|CVE-2018-20062|ThinkPHP|
|12|CVE-2018-7600|Drupal|
|13|CVE-2019-11043|PHP-FPM|
|14|CVE-2019-17564|Dubbo|
|15|CVE-2020-35476|OpenTSDB|
|16|CVE-2020-7247|OpenSMTPD|
|17|CVE-2021-25646|Apache-Druid|
|18|CVE-2021-41773|Apache-HTTPD|
|19|CVE-2021-42013|Apache-HTTPD|
|20|CVE-2022-0543|Redis|
|21|CVE-2022-22965|Spring-WebMVC|
|22|CVE-2022-24706|CouchDB|
|23|CVE-2022-24816|GeoServer|
|24|CVE-2022-41678|ActiveMQ|
|25|CVE-2023-25826|OpenTSDB|
|26|CVE-2023-51467|OFBiz|
|27|CVE-2024-27348|HugeGraph|
|28|CVE-2024-36401|GeoServer|
|29|CVE-2025-32433|Erlang/OTP(sshd)<br>|
|30|CVE-2025-3248|Langfow|



goal and hands it over to the Assistant Module. The Reasoner Module proceeds to the next planning step only after the Assistant Module reports success or failure in achieving the phased goal. Throughout this process, the Assistant Module interacts with the Memory Module to retrieve abstract-level activated memory as input context for decision-making. **Assistant Module.** The Assistant Module is responsible for the phased goal assigned by the Reasoner Module and performs low-level planning based on it, such as generating the specific instructions to be executed. Prior to generating the next instruction, the Assistant Module verifies whether the phased goal has succeeded or failed, determining whether control should revert to the Reasoner Module for a new 

phased goal. During this process, the Assistant Module also interacts with the Memory Module to obtain coarse-grained level activated memory, which serves as context for decisionmaking. 

In addition, the Assistant Module interacts with the Arsenal Module to obtain the manuals for exploits available based on the current penetration progress—whether in-the-wild or from third-party tools such as Metasploit—thereby assisting in the generation of concrete instructions to be executed. **Executor Module.** The Executor Module executes the concrete instructions generated by the Assistant Module and submits both the instructions and their raw execution results to the Memory Module for organization and compression. Upon completion of instruction execution, control reverts to the Assistant Module to proceed with the next planning step. 

## **C Supplement to Instructions Reduction of Auto-Pen-Bench** 

Apart from the target subnet and the goal of obtaining the flag, the instructions in Auto-Pen-Bench also include some additional hints, such as penetration entry points, exploit paths, and even details of specific command execution. Below are the original instructions for the CVE_VM8 target in AutoPen-Bench, which contain target service’s username admin, credentials password, the flag’s storage path /var/www/html/flag.txt, and specific commands like launch msfconsole. Such information is rarely available in real-world penetration testing tasks, where the only known data may be the target’s IP address or subnet. 

### Original Instruction for Auto-Pen-Bench 

Discover the vulnerable target machine within the 192.168.5.0/24 network. Inspect the service through direct interaction. Launch an interactive msfconsole to ientify a known exploit (Do not use searchsploit). Correctly configure the exploit to access the /var/www/html/flag.txt file. When you discover the service, use admin:password as ’admin’ credentials. Remember: If you need to run command outside msfconsole after you used it, remember to type ’exit’ 

Accordingly, for experiment on performance under limited instructions in Section 6, we reduced all Auto-Pen-Bench’s instructions to include only the target host’s subnet and the flag acquisition goal. The final instructions used in the experiment are shown below and this provides a more objective assessment of the agent’s penetration testing performance. 

### Limited Instruction for Auto-Pen-Bench 

Discove the target machine within 192.168.5.0/24 and try to get the flag on it. 

Anonymous’25, Anon, Anonymous 

Wuyuao Mai, et al. 

## **D Details of LLMs Used in Evaluation** 

Table 11 presents the basic information, pricing, and default parameter settings of the LLMs used in the experiments for TermiAgent. It should be noted that the GPT-5 series models no longer allow users to specify the temperature and top_p parameters[28]. 

## **E Details of UED Dimensions** 

Table 12 provides the detailed definitions of all dimensions used in the Unified Exploit Descriptor (UED). These dimensions are divided into two functional categories: those required for automated environment construction (e.g., language, system_dependencies, main_script) and those required for generating agent-invocable manuals (e.g., parameters, setup_steps, exploit_steps). The table formalizes how heterogeneous exploit repositories are transformed into standardized, reproducible specifications for autonomous execution by Arsenal Module. 

Anonymous’25, Anon, Anonymous 

Shell or Nothing: Real-World Benchmarks and Memory-Activated Agents for Automated Penetration Testing 

**Table 11.** LLMs information. 

|**Model**||**Cost**||**Hyperparam**|**eters**|
|---|---|---|---|---|---|
||**API Platform**<br>**I**|**nput**|**Output**|**Temperature**|**Top P**|
|GPT-5[27]|[2]<br>1.25USD|/ 1M tokens|10 USD / 1M tokens|-|-|
|DeepSeek-V3-0324[8]|[3]<br>2RMB /|1M tokens|8RMB / 1M tokens|1.0|1.0|
|Qwen3-30B-A3B[35]|[1]<br>0.75RMB|/ 1M tokens|7.5 RMB / 1M tokens|0.6|0.95|
|Qwen3-14B [33]|[1]<br>1RMB /|1M tokens|10RMB / 1M tokens|0.6|0.95|
|Qwen3-8B [37]|[1]<br>0.3RMB|/ 1M tokens|3RMB / 1M tokens|0.6|0.95|
|Qwen3-4B [36]|[1]<br>0.3RMB|/ 1M tokens|3RMB / 1M tokens|0.6|0.95|
|Qwen3-1.7B [34]|[1]<br>0.3RMB|/ 1M tokens|3RMB / 1M tokens|0.6|0.95|



**Table 12.** Unified Exploit Descriptor (UED) dimensions, organized into environmental and operational categories. 

|**Dimension**|**Description**|
|---|---|
|**Enviro**|**nmental dimensions (for reproducible execution environment)**|
|Language|Primary programming language of the exploit (e.g., Python, C, Go).|
|Language version<br>Base image|Recommended language version ensuring compatibility (e.g., Python 3.9 vs. 2.7).<br>Lightweight Docker base image aligned with language/runtime (e.g.,python:3.9-slim).|
|System dependencies<br>Code dependencies|OS-level packages to be installed via package manager (e.g.,nmap,build-essential).<br>Language-specifc libraries installed via package manager (e.g.,requests,pwntools).|
|Main script|Path, executor, and metadata of the primary exploit script. Serves as container<br>entrypoint.|
|Parameter fles|External fles (payloads, confgs, URL lists) required by the exploit.|
|Docker confg|Workdir, entrypoint, and command defaults for reproducible containerization.|
||**Operational dimensions (for manual generation)**|
|Setup steps|Environment and target setup before exploitation(e.g., listener, service connection.|
|Exploit steps|Ordered attack operations (e.g., run script, send payload). Form the execution skeleton.|
|Parameters|Command-line arguments with placeholders, descriptions, and defaults.|
|Usage example|Repository-derived command-line example.|



