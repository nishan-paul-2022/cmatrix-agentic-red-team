# **Incalmo: An Autonomous LLM-assisted System for Red Teaming Multi-Host Networks** 

Brian Singer<sup>_∗_</sup> , Keane Lucas<sup>_†_</sup> , Lakshmi Adiga<sup>_∗_</sup> , Meghna Jain<sup>_∗_</sup> , Lujo Bauer<sup>_∗_</sup> , Vyas Sekar<sup>_∗_</sup> , _∗Carnegie Mellon University †Anthropic_ 

**_Abstract_ —Security operators use red teams to simulate real attackers and proactively find defense gaps. In realistic enterprise settings, this involves executing multi-host network attacks spanning many “stepping stone” hosts. Unfortunately, red teams are expensive and entail significant expertise and effort. Given the promise of LLMs in CTF challenges, we first analyze if LLMs can autonomously execute multi-host red team exercises. We find that state-of-the-art LLM-assisted offense systems (e.g., PentestGPT, CyberSecEval3) with leading LLMs (e.g., Sonnet 4, Gemini 2.5 Pro) are unable to do so.** 

**Building on our observations in understanding the failure modes of state-of-the-art systems, we argue the need to improve the abstractions and interfaces for LLM-assisted red teaming. Based on this insight, we present the design and implementation of Incalmo**<sup>1</sup> **, an LLM-assisted system for autonomously red teaming multi-host networks. Incalmo uses LLMs to plan red team exercises in terms of high-level declarative tasks that are executed by domain-specific task agents. Incalmo also uses auxiliary services to manage context and acquired assets.** 

**For our evaluation, we develop MHBench, a novel multihost attack benchmark with 40 realistic emulated networks (from 22 to 50 hosts). We find that Incalmo successfully acquires critical assets (i.e., key hosts or data) in 37 out of 40 MHBench environments. In contrast, state-of-the-art LLMassisted systems succeed in only 3 out of 40 environments. We show that Incalmo is efficient—successful attacks took 12–54 minutes and cost** _≤_ $15 **in LLM credits.** 

## **1. Introduction** 

Defenders often use red teams to proactively test and discover gaps in their network defenses. Here, red teams execute operations across many hosts to achieve their attack goals (e.g., compromising a key host), emulating real attackers [43], [46]. Red-team exercises help defenders prioritize vulnerabilities to patch, evaluate detection rules, and test their response strategy. Unfortunately, red-team exercises are expensive and require significant expertise and effort. 

Given the promise of autonomous LLM-based cyber offense capabilities (e.g., [14], [72], [49], [80], [71], [77], [61], [76], [17]), we explore whether LLMs can autonomously execute red-team exercises. Autonomous red teams could 

1. All code is publicly available: https://github.com/bsinger98/Incalmo 


![](docs/paper-research/md-downloaded-paper-professor/images/06-incalmo-autonomous-llm-assisted-system-for-red-teaming.pdf-0001-10.png)


Figure 1. Incalmo is a system for executing multi-host red teams. Unlike prior systems, Incalmo explicitly decouples the red teaming into two layers: a planning layer and an execution layer. Instead of LLMs interacting with low-level tools, Incalmo has an LLM plan red teams with high-level declarative tasks that are executed by expert red team agents. 

reduce the cost and effort for enterprises and help defenders proactively block attack paths [55]. Such a capability could also further our understanding of the cybersecurity capabilities of frontier models [72], [71], [49]. 

With this objective in mind, we first create MHBench, a red-teaming benchmark of 40 multi-host environments. MHBench is based on a mix of public reports of real-world attacks [43], [33], reference topologies [2], [3], and prior work [36], [69], [18], [2], [40]. We use MHBench to evaluate state-of-the-art LLM-based offense systems (e.g., PentestGPT [14], CyberSecEval3 [72], CAI [44]) using frontier models (e.g., GPT4o, Sonnet 4, Gemini 2.5 Pro). We find that the state-of-the-art offense systems achieve very limited success in red-team challenges. To our knowledge, this is the first systematic assessment of the red-teaming capability of LLM-assisted cyber offense in multi-host scenarios. 

Next, we analyze how state-of-the-art systems failed at 

multi-host red-team challenges. At a high level, we find that existing systems waste effort in _irrelevant_ tasks unrelated to the challenge, _incorrectly execute_ tasks, or use _brittle postexploitation techniques_ . Additionally, all of these systems suffer from significant _context bloat_ as they proceed in the complex challenge, which impacts effectiveness in longhorizon challenges, as seen in other domains [11]. 

Rather than try to improve LLMs’ effectiveness in executing correct low-level commands (e.g., adding better prompts [14], [72], self-reflection [29], [14], [62]), we draw inspiration from how expert human red teams work and argue that we need to _raise the level of abstraction_ to build effective autonomous LLM-assisted red teams. More specifically, expert red teams do not try to run low-level shell commands or use brittle shell commands across stepping stone hosts. Instead, they think in terms of _high-level “cyber kill-chain” tasks_ [30] such as reconnaissance [47], exploitation [12], command and control [55], and goalcentric actions. Furthermore, they use best practice _tools_ in the security domain to ensure each stage in the kill chain can be effective [55], [47], [12]. 

Building on this insight—that raising the level of abstraction is the key—we present the design, implementation, and evaluation of Incalmo. Incalmo explicitly _decouples redteam planning from execution_ (Figure 1). Incalmo uses the LLM primarily as a _planning_ module that decides _what_ task to perform in terms of _high-level declarative tasks_ modeling cyber kill-chain steps, rather than low-level shell commands. Incalmo delegates the execution of these tasks to reliable expert task agents using domain-specific best practices. To avoid prompt bloat and reliably manage acquired assets, we introduce auxiliary environment-state, attack-graph, and command-and-control services for the planning LLM and task agents to retrieve information, reason about the environment, and execute tasks. Taken together, these ideas allow Incalmo to both (a) leverage the broad world knowledge in the LLM used as a planner to respond and plan next steps and (b) use domain-specific expertise to execute the plan. 

We show that Incalmo can handle unforeseen multihost scenarios (i.e., previously unseen topologies and attack paths) that involve known or public vulnerabilities. This setting is representative of many real-world red teams that often chain together known techniques to achieve attack goals in multi-host settings [43], [46], [9]. The design of Incalmo is also extensible to include new capabilities (e.g., creating 0-day exploits [70], [73]). 

In some sense, Incalmo’s design represents a redteam–specific synthesis of best practices in using LLMs for complex and long-horizon tasks—decoupling planning from execution [78], scoped agents [11], and offloading solution steps [21], [41], [58]. Our key contributions are in identifying the right tasks, a suitable functional split between LLMs and domain-specific agents, and interfaces to share knowledge and capabilities between the planner and agents. 

To evaluate Incalmo, we leverage MHBench and use three metrics to capture success: (1) _Success_ , indicates whether an attacker has successfully acquired _any_ critical asset in an environment; (2) _TotalAcquisition_ , to measure 


![](docs/paper-research/md-downloaded-paper-professor/images/06-incalmo-autonomous-llm-assisted-system-for-red-teaming.pdf-0002-06.png)


Figure 2. Comparing Reliability across environments between Incalmo and ExpertPromptShell with Sonnet 4, the LLM-based system with the best performance on MHBench. Incalmo succeeded in 37 out of 40 environments while ExpertPromptShell only succeeded in 3 out of 40 environments. 

_the proportion_ of critical assets captured across multiple attempts; and (3) _Reliability_ , to measure the likelihood that any given red-team exercise will succeed at Success. 

As an illustrative finding, Fig. 2 compares the _Success_ and _Reliability_ of Incalmo against ExpertPromptShell, the best baseline LLM-based tool<sup>2</sup> , with both systems using Sonnet 4. In terms of _Success_ , Incalmo succeeded in 37 out of 40 environments while ExpertPromptShell only succeeded in 3. In terms of _TotalAcquisition_ , we find that Incalmo obtained more critical assets than ExpertPromptShell in 37 of the environments, with them achieving parity in the remaining 3. We find that Incalmo is cheap and fast— successful attacks took 12–54 minutes and cost _≤_ $15 in LLM credits. 

We conduct an ablation study to understand which key factors impact Incalmo’s success. We show that the choice of LLM used by Incalmo is not critical and Incalmo can successfully red-team networks using a variety of LLMs. Additionally, we find that Incalmo’s abstractions play a larger role than model size: Incalmo using smaller LLMs (e.g., Haiku 3.5) can successfully execute attacks in most environments. 

_Contributions._ 

- We identify a key gap in existing cyber offense work and motivate the need for LLM-assisted red teaming in multi-host networks in unforeseen environments. 

- We develop MHBench, an extensible benchmark with 40 networks for evaluating LLMs at autonomously executing multi-host red team challenges. 

- We show that leading LLMs with state-of-the-art techniques are largely unable to autonomously execute multi-host red team challenges. We analyze the failure patterns and find that the systems output irrelevant tasks, execute incorrect commands, use brittle asset management, and have context bloat. 

- We present Incalmo, building on the idea of raising the level of abstraction at which the LLM plans, delegating execution of high-level tasks to domain-specific expert agents, and introducing auxiliary services to tackle 

2. ExpertPromptShell with Sonnet 4 is the best-performing prior system among various baselines, as we show in Sec. 2. 


![](docs/paper-research/md-downloaded-paper-professor/images/06-incalmo-autonomous-llm-assisted-system-for-red-teaming.pdf-0003-00.png)


Figure 3. The attacker during 2017 Equifax breach executed a multi-host attack. The attacker exploited, infected, and exfiltrated data on multiple hosts across two networks. 

context bloat and to manage acquired assets. We show that Incalmo can autonomously obtain critical assets in 37 out of the 40 environments. 

_Ethics and reproducible research._ We acknowledge that Incalmo is a dual-use technology that could be leveraged by real attackers. However, systems like Incalmo can also help defenders proactively test their networks. As prior work has also noted [80], [14], there is a long history of dual-use systems (e.g., bug finding [73], [26], exploit generation [14], [8], [54]) helping defenders more than attackers [64] and we believe the same will be true for autonomous red teams. Additionally, the use of LLMs by real attackers has already been documented [6], [52], and we hope our work will help defenders also benefit from the capabilities that LLMs offer. Following the precedent of previous work [14], [80], [8], [75], [28], [54], [35], [73], we are open-sourcing Incalmo, the benchmarks, and all of the code related to this study to enable defenders and researchers to use and build on our findings. We have also disclosed our results to leading LLM vendors to enable them to monitor for and, if desired, build safeguards against, the kinds of LLM uses that we explore. We discuss research ethics in more detail in the Ethics considerations section. 

## **2. Motivation and background** 

We start with a motivating example highlighting the importance of running red team exercises in multi-host networks. Then, we give a brief overview of related work in cyber-offense systems. We address a key gap in prior work [59]—understanding how existing LLM-based systems perform in _multi-host red team exercises_ . 

### **2.1. Motivating example: Red teaming Equifax** 

We begin by highlighting the importance of red teams in multi-host settings using the 2017 Equifax data breach as an illustrative example [43], shown in Fig. 3. Attackers infected two external web servers by exploiting CVE-2017-5638, a known vulnerability publicly disclosed two months prior to the attack. Attackers then found plain text credentials on one of the web servers, used the credentials to compromise 

database servers, and then exfiltrated sensitive user data from 48 databases. This example illustrates the _multi-host_ and “stepping stones” nature of a real-world attack spanning multiple network segments and different vulnerabilities to acquire the critical asset(s). 

If the network operators were able to “red team” or pentest the entire network to proactively uncover the possibility of a multi-host attack, then they could have implemented protective measures. For instance, it may have flagged that data exfiltration monitoring rules were not being actively monitored [20]. Or it may have highlighted how unpatched vulnerabilities and plaintext credentials could be chained together to exfiltrate critical data [20], to help prioritize these problems to operators. 

Doing such red team exercises today, unfortunately, is easier said than done. Such exercises require manual effort from specialized and expensive teams of experts [55]. 

In this context, we see a potential opportunity for AIassisted automation in red teams. Such a mechanism, if feasible, can lower the cost and effort for continuous redteaming, and serve as a basis to proactively uncover and mitigate such multi-host attacks. 

### **2.2. Approaches to offense systems** 

We categorize existing cyber-offense approaches along three dimensions: (1) type of attack challenge (e.g., single host, multi-host), (2) type of vulnerabilities, and (3) execution model (e.g., LLM vs. non-LLM). Our focus is on red teaming involving _multi-host_ challenges executed _autonomously_ by _LLM-based_ systems [59]. 

_Type of attack challenge._ Prior studies evaluate LLMs for solving CTF-style challenges [14], [72], [49], [80], [71], [29], [23], [77], [61], [76], [7], [17], [60]. Many problems do not involve infecting a host (e.g., solving a cryptography challenge [80], [14], [49]). Some challenges involve a single action to infect a single host [23], [77], [76], [17], [60]. More difficult challenges are single-host attacks that involve completing a series of steps [14], [80], [61], [72], [49], [71], [24]. While these may require multiple stages, they do not involve multiple hosts and subnetworks. 

We refer to challenges that involve multiple hosts and subnetworks as _multi-host network attacks_ . A multi-host network attack is complex and involves multiple intermediate subgoals, strategic planning, and coordinated actions at each step toward the final target(s). 

_Type of vulnerabilities._ Some prior offense systems assume vulnerabilities are known [72], [80], [14], [8], while others focus on 0-day vulnerabilities [73], [62]. As a first step in the multi-host setting, we focus on attacks using known vulnerabilities which is a serious concern in realworld attacks [43], [33], [9]. 

3. The MITRE OCCULT is a framework to understand the cyber security risks of LLMs. In one evaluation, they have a preliminary case study on using an LLM-based system to attack a proprietary multi-host network. Later, we evaluate Incalmo-WHT, a similar approach to the case study, on MHBench and show that LLMs fail to even partially succeed in any environment. 

TABLE 1. SUMMARY OF EXISTING CYBER-OFFENSE TOOLS AND THEIR EVALUATION ENVIRONMENT 

|**Evaluation**<br>**environment**<br>**Non-LLM**|**LL**|**M**|
|---|---|---|
|Manual<br>Automated|Semi-auto|Automated|
|Single-stage<br>Single-host<br>MSF[54]<br>NM[42] HC[66]<br>–|PT[14] CB[80]|GP[23] YL[77]<br>IC[76] FT[17]<br>SH[60]|
|Multistage<br>Single-host<br>MSF[54]<br>CD[8]|PT[14] CB[80]<br>AA[75] AP[5]|NY[61] CA[44]<br>CS[72] O1[49]<br>|
|||CB[80] AT[71]<br>VB[34]|
|Multistage<br>Multi-host<br>MSF[54]<br>CD[8] LR[26]<br>HR[16] CY[79]<br>AJ[4] SV[27]<br>HP[28] DE[67]|–|Incalmo<br>OC[35]<sup>3</sup>|
|Legend|||



We summarize prior work as seen in Table 1: (1) LLMbased systems and (2) Non-LLM-based systems. 

_LLM-based systems._ LLM-based autonomous offense systems [23], [77], [76], [17], [60], [61], [72], [49], [80], [71], [44] entail instructing LLMs to attack the environment. The LLM outputs shell commands, which a second entity (e.g., human, MCP server) executes on a computer with access to the environment, shown in Fig. 1. The output of the command is optionally processed [14], [44] and appended to the context. Then the LLM (and/or human) will use this context to decide the next command to execute. 

_Non-LLM-based systems._ There is also work on multihost attacks that do not rely on LLMs—some fully autonomous [8], [26], [16], [79], [27]. There are rule-based and state-machine-based systems (e.g., [26], [27], [16], [79], [4]). However, the focus in this paper is to explore and design LLM-assisted techniques at automating red teams. 

In summary, existing autonomous and human-assisted use of LLMs has shown preliminary promise for small CTF-style single host security challenges. However, our understanding of if, and how, LLM-assisted systems can autonomously red team multi-host networks is limited. 

### **2.3. Existing LLM-based systems are ineffective in multi-host red team challenges** 

To address the gap in evaluating state-of-the-art LLMbased systems, we create a novel _multi-host network attack_ benchmark called MHBench. We describe MHBench in more detail in Sec. 5 and Appendix B. In this section, we select 10 illustrative multi-host attack challenges from MHBench and evaluate the red team effectiveness of the aforementioned baseline systems. 

_Success criteria._ In real-world multi-host environments, there are often multiple key assets (e.g., Equifax had multiple sensitive databases in Fig. 3). Similar to human red teams [47], we consider an attack successful if an attacker 


![](docs/paper-research/md-downloaded-paper-professor/images/06-incalmo-autonomous-llm-assisted-system-for-red-teaming.pdf-0004-09.png)


Figure 4. The Success and TotalAcquisition metrics of LLM offense systems across 10 environments. The systems were largely unable to realize multi-host attacks. 

is able to compromise at least one key asset (e.g., exfiltrated SSNs from at least one database). For the experiments in this section, we consider two kinds of metrics: _Success_ indicates if _any_ critical asset was acquired; and _TotalAcquisition_ to measure _how many_ critical assets were captured (formal definitions in Sec. 6). 

_Baselines._ In terms of autonomous LLM systems, we consider three baselines: (1) CyberSecEval3 [72], (2) ExpertPromptShell, a shell system with a prompt we created in collaboration with a domain expert at a leading LLM provider, and (3) CAI [44], a popular open-source system.<sup>4</sup> We choose these systems because they use a variety of the techniques (e.g., chain-of-thought [72], [74], ReAct [78], and self-reflection [72], [14]) and were reproducible with open-source prompts and systems. For the semi-autonomous or human-in-the-loop systems, we evaluate PentestGPT [14] because it encompasses many “reasoning” strategies in other work (e.g., [14], [80]). Since PentestGPT requires a human operator, we evaluate PentestGPT by manually entering the commands recommended at each step by PentestGPT into the attacker’s Kali Linux host. For ExpertPromptShell and CyberSecEval3, we consider 3 state-of-the-art LLMs: Sonnet 4, GPT 4o, Gemini 2.5 Pro.<sup>5</sup> 

The baseline systems are evaluated on the 10 environments with 5 independent trial runs.<sup>6</sup> We also evaluate a SOTA non-LLM attack system, MITRE’s Caldera [8], a popular open-source tool for red teaming multi-host networks. Caldera has a library of over 1,000 actions and various non-LLM strategies found in prior work (e.g., RL [36], weighted decisions [22]). We execute Caldera with a variety of strategies (we only show the results of the most exhaustive strategy because the others do not make progress). 

_Findings._ Across all evaluated LLMs and environments, we find that existing state-of-the-art LLM-assisted and nonLLM-based systems are largely unable to realize multi-host 

4. All prompts are in our open-source repository. 

5. We were unable to evaluate OpenAI’s “o” or “GPT-5” models because the public API has a safeguard that prevents them from executing attacks. 

6. Since PentestGPT requires manual effort, we only execute 3 trials with GPT4o, the recommended LLM. 


![](docs/paper-research/md-downloaded-paper-professor/images/06-incalmo-autonomous-llm-assisted-system-for-red-teaming.pdf-0005-00.png)


Figure 5. A mental model of how red teams execute multi-host attacks. Red teams start with a goal (e.g., exfiltrate important data). Then, they follow a loop of deciding a task (e.g., infect a server), executing the task (e.g., launching an exploit), and updating their knowledge/capabilities. 

attacks w.r.t both Success and TotalAcquisition, shown in Fig. 4. Only ExpertPromptShell with Sonnet 4 was able to succeed even partially, by managing to exfiltrate data from one of the database servers in the Equifax-inspired environment. ExpertPromptShell with Gemini 2.5 Pro and Sonnet 4 were able to exfiltrate some of the data in the 4-layer chain environment. We find that PentestGPT, even with its state-of-the-art prompting strategies is ineffective in this multi-host setting.<sup>7</sup> 

## **3. Failure analysis** 

In this section, we analyze _how_ existing state-of-the-art LLM-assisted systems fail at multi-host red team exercises. These insights help inform our design of Incalmo. 

### **3.1. Methodology** 

We begin by describing our methodology to understand how prior systems fail at multi-host challenges. Specifically, we use a combination of an abstract model of how expert human red teams operate in practice, reference solutions for the challenges, and execution logs from existing systems to understand their failure modes. We describe each next. 

_Abstract mental model._ Red-team operations operate through an iterative loop shown in Fig. 5. Starting from their initial _knowledge_ (e.g., known vulnerabilities) and what _assets_ they can control (e.g., command execution on a host), the red team _plans and decides_ a next logical _task_ to implement (e.g., infect a host) [55]. The red team will then attempt to _execute_ the task (e.g., launch an exploit). A successful task either obtains new assets (e.g., access to a new host) or discovers new _knowledge_ (e.g., finding sensitive data). Then, the red team updates their knowledge/asset base 

7. We have tested other models such as DeepSeek and Llama 3 but do not show these results for brevity. In our experiments, these models do not follow instructions and are unable to execute shell commands correctly. As models get released, we plan to update our benchmark “scorecard” (Fig. 4). 


![](docs/paper-research/md-downloaded-paper-professor/images/06-incalmo-autonomous-llm-assisted-system-for-red-teaming.pdf-0005-09.png)


Figure 6. Percentage of tasks successfully implemented by ExpertPromptShell with different LLMs. Across all environments, ExpertPromptShell was only able to execute 1–30% of the tasks. 

and decides the next task. The red team repeats this loop until they either achieve all goals or runs out of time [47]. 

_Reference solutions._ With this mental model, we create reference solutions for how a red team would successfully attack the environments in Sec. 2. For each environment, we create a reference solution based on an attack graph model [63]. We define a _task_ as a sequence of commands to reach a state in the attack graph (e.g., found the correct vulnerability, gained access to a server). For each task, we manually create a correct implementation to achieve the task (e.g., the correct command to find a vulnerability) to reach the next logical state in the attack graph. For completeness, we provide the details of the attack graph model in Appendix A. 

_Log analysis._ Using the reference solutions, we manually analyze the logs from the execution runs of the baseline systems from Sec. 2. This helps us shed light on common failure modes. Given the manual effort of this analysis, we do a qualitative inspection across baselines and a deeper dive on the best performing system, ExpertPromptShell. For ExpertPromptShell, we first categorize tasks by the LLMbased systems as either relevant or irrelevant. We define a relevant task as a task required for successfully executing a multi-host attack (e.g., found the correct exploit). Then, for relevant tasks, we use the reference solution and manual review to determine if the tasks are correctly implemented. The details of this analysis are in Appendix A. 

### **3.2. Observations** 

We now describe our key observations about how existing systems fail in our multi-host red team exercises from Sec. 2. 

**Observation 1: Pursuing irrelevant red team tasks** We observe that both the LLM-based (and non-LLM-based) red-team systems evaluated in Sec. 2 struggle to correctly decide a task in Fig. 5. Across the LLMs and environments, 47–90% of ExpertPromptShell’s commands are irrelevant, shown in Fig. 7. For instance, the ExpertPromptShell tried brute forcing SSH credentials, finding misconfigured files, or exploiting non-exploitable services. Or in the case of PentestGPT, we often found it trying to “cover its tracks” (e.g., deleting command history) on the attacker’s Kali host. 


![](docs/paper-research/md-downloaded-paper-professor/images/06-incalmo-autonomous-llm-assisted-system-for-red-teaming.pdf-0006-00.png)


Figure 7. In the Equifax-inspired and chain environments, 47–90% of ExpertPromptShell’s tasks are irrelevant. Furthermore, 6–41% of ExpertPromptShell’s tasks are implemented incorrectly. 

Caldera, a non-LLM based system also executed irrelevant tasks; e.g., frequently attacking the attacker’s own Kali host, rather than use the attacker’s host for red teaming. 

**Observation 2: Incorrectly executing tasks** Even when LLM-based systems pursued relevant red teaming tasks, we observed that they struggled to correctly execute these tasks in Fig. 5. For instance, across the LLMs and environments, 6–41% of ExpertPromptShell’s relevant tasks are implemented with incorrect commands (Fig. 7). Incorrect implementations are a critical failure mode: they can produce cascading failures and mask otherwise viable attack chains. An incorrectly implemented exploit will not only fail to compromise one host, it also prevents the discovery of downstream vulnerabilities. 

In our manual review of the logs, we found that the systems consistently struggled to correctly implement exploits and network scans. For example, in one case we see that ExpertPromptShell with Sonnet 4 tried to create a complex exploit for the Apache Struts vulnerability, but the implementation is wrong and fails: 

curl -H "Content-Type: % (#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS). (#_memberAccess?(#_memberAccess=#dm): ((#container=#context[’com.opensymphony.xwork2. ActionContext.container’]). (#ognlUtil=#container.getInstance(@com.opensymphony. xwork2.ognl.OgnlUtil@class)). (#ognlUtil.getExcludedPackageNames().clear()). (#ognlUtil.getExcludedClasses().clear()). (#context.setMemberAccess(#dm)))).(#cmd=’id’). (#iswin=(@java.lang.System@getProperty(’os.name’). toLowerCase().contains(’win’))). (#cmds=(#iswin?{’cmd.exe’,’/c’,#cmd}: {’/bin/bash’,’-c’,#cmd})). (#p=new java.lang.ProcessBuilder(#cmds)). (#p.redirectErrorStream(true)).(#process=#p.start()). (#ros=(@org.apache.struts2.ServletActionContext@ getResponse().getOutputStream())). (@org.apache.commons.io.IOUtils@copy (#process.getInputStream(),#ros))% http://192.168.200.10:8080/showcase.jsp 

Or in the case of network scanning, PentestGPT and CAI were able to discover external services (e.g., a web server) through scanning tools such as nmap. However, these systems struggled to find remote code execution vulnerabilities on these services. In one case, CAI w/ Sonnet 4 executed 9 shell commands to discover external web servers. Then, rather than searching for a vulnerability, CAI executed 3 

unrelated exploits and gave up. Or in another case, after PentestGPT discovered a web server, it said “the favorable next step is to find vulnerabilities” without any suggestions or commands on how to discover such vulnerabilities. 

**Observation 3: Using brittle post-exploitation techniques to command hosts** In the few times ExpertPromptShell successfully executed exploits, the system used brittle post-exploitation techniques to control assets. We only observe this in ExpertPromptShell because none of the other systems were able to make substantial progress. ExpertPromptShell w/ Sonnet 4 often used exploits to execute commands on vulnerable hosts, rather than establishing an agent connected to a command and control server. Exploits are often not a reliable method of executing commands [55], but more importantly the unreliability cascades in multihost environments. As the chain grows, chaining together exploits becomes increasingly complex and unreliable.<sup>8</sup> 

We also found that ExpertPromptShell w/ Sonnet 4 used ssh and reverse shells to execute commands on vulnerable hosts. This technique was sufficient for the 4-layer chain challenge, but fails in the other challenges. These approaches do not work because of common firewall configurations (e.g., a web server does not have ssh configured). 

**Observation 4: Knowledge has context bloat** All of the prior LLM-systems store all knowledge by adding observations (e.g., command outputs) to the context. We found this especially in ExpertPromptShell (the best performing system) and CyberSecEval3, where the context grew with many low-level implementation details clogging the red team’s knowledge in Fig. 5. For instance, in one case ExpertPromptShell with Sonnet 4 on the Enterprise A environment executed 108 shell commands with a final context of 54K tokens (157,760 characters). One of these commands resulted in over 30K characters consisting of file paths. These long contexts likely cause the LLM systems to struggle to maintain a high-level plan [11], [14].<sup>9</sup> 

## **4. Incalmo: An LLM-based system for autonomously executing multi-host red teams** 

In this section, we begin by describing the high-level idea underlying Incalmo before presenting the detailed design. 

### **4.1. High-level idea** 

Our design of Incalmo draws from both our mental model of expert red teams and the failure modes we observed in existing LLM-assisted systems. At a high level, we observe that existing LLM-based systems: (1) operate at 

8. In real-world attacks and red team exercises, attackers primarily use exploits to install malware agents that communicate with a C&C server [20], [33], [55] 

9. Interestingly, the authors of PentestGPT [14] noted this same problem when solving CTF challenges and introduced a token compression module to limit the context. However, we did not observe context rot in PentestGPT as it only executed 6 commands at most before giving up in this multi-host challenge. 


![](docs/paper-research/md-downloaded-paper-professor/images/06-incalmo-autonomous-llm-assisted-system-for-red-teaming.pdf-0007-00.png)


Figure 8. Incalmo uses LLMs to plan multi-host attacks with high-level tasks. The orchestrator implements the tasks with expert agents and services. 

a low level, trying to output shell commands, and creating complex, brittle exploits and managing acquired hosts; and (2) continuously bloat the LLM context over the course of a multi-host red-team exercise. 

Building on these lessons, we argue for an approach that _raises the level of abstraction_ at which an LLM-assisted red team operates. To this end, we explicitly _decouple planning from execution_ by separating Incalmo into an LLM-assisted planning layer that decides _what_ tasks to perform and an execution layer that decides _how_ to execute tasks. 

This is in contrast to how prior systems use LLMs to both plan and execute tasks, shown in Fig. 8. Rather than have the planner output low-level commands as done in the baseline systems, we reformulate it to output high-level declarative tasks inspired by the cyber kill chain framework [30], [12]. We delegate the execution of these tasks to bespoke red-team agents that use reliable best practices (e.g., a C&C server service). This is in contrast to how prior systems used a variety of heuristics (e.g., fine-tuned system prompts [14], [72], [80], command self-reflection [14], [44], [29], summarizers [14], [29]) to improve the ability of a single LLM to combine planning and execution. Finally, to tackle the context bloat, we introduce auxiliary environmentstate and attack-graph services that can be queried (akin to RAG [39]) by the planner and expert agents. This allows the majority of accumulated knowledge to be off-loaded from the LLM, in contrast to prior systems storing all knowledge in the LLM’s context. 

_Scope and limitations._ We scope our design in this paper with two known limitations. First, our design does not take into account defender capabilities (e.g., detection, blocking), similar to prior work in LLM-based offense evaluations [14], [72], [80]. Second, similar to many real-world settings, we assume the red team exercise only considers known vulnerabilities and do not consider zero-day exploits [62]. We do note, however, that Incalmo is extensible and could include these considerations in future work. 

### **4.2. Detailed design** 

Having described the high-level idea above, next we describe our concrete realization of the: (1) planning abstraction and declarative tasks; (2) library of red team agents to implement the specific tasks; and (3) auxiliary services that enable the planner LLM and the task agents to reliably manage knowledge and assets they have gained during the red team exercise. 

_Planning abstraction._ Prior systems plan and execute red teams in terms of low-level shell commands and tools. In contrast, we raise the level of abstraction and explicitly instruct the LLM’s plan to be expressed in terms of highlevel declarative tasks. More specifically, our abstraction for these declarative tasks follows the logical stages specified by the MITRE ATT&CK [12] and cyber kill chain [30] frameworks: scan a network, laterally move, escalate privileges, discover local information, and exfiltrate data. Concretely, LLMs specify and compose these declarative tasks using Python functions. The functions can use the standard Python library and Incalmo’s API. A function can either (1) output a series of high-level tasks (e.g., scan a network), or (2) output a series of queries for environment context (e.g., find hosts on a public network). This functional specification allows the LLM to use the Incalmo services to specify red team plans. For instance, an LLM can output a function that queries for all external networks, then has a loop to execute a scan on each of the networks. We see in practice that LLMs can generate complex functions that infect multiple hosts at once or exfiltrate all data in a network. 

_Task agents._ We design task agents to translate the above set of declarative tasks into low-level commands, as described briefly in Table 2. Prior LLM-based offense systems used a variety of techniques to improve command accuracy such as adding LLM inference methods: self-reflection to correct wrong commands [14], [44], [29], increasing the library of low-level MCP tools [44], and even creating a library of system prompts tuned to specific security tasks [14]. However, in Sec. 2 and Sec. 3, we observe that these techniques are insufficient in fixing implementation problems for multi-host environments. 

In contrast, we create task agents that can reliably execute each of these tasks based on security domain best practices.<sup>10</sup> For instance, the lateral movement agent queries the attack graph service to identify possible vulnerable paths to the target server. Then, the agent searches an exploit database (e.g., Metasploit) for exploits matching these vulnerabilities and executes them. We address two key challenges when designing these agents: (1) the agents need to be environment-agnostic; and (2) the agent library needs to be extensible to support new attacker capabilities. 

To ensure these tasks are generalizable across environments, the agents use the APIs exposed by the attack graph service and environment state service (described below). For instance, agents select the source and target hosts for the lateral movement task with the environment state service. 

10. Later in Sec. 6, we also explore the use of LLM-based agents and find that they do not perform well at executing tasks. 

TABLE 2. HOW INCALMO NON-LLM TASK AGENTS TRANSLATE TASKS 

|**High-level tasks**|**Incalmo agent translation**|
|---|---|
|FindInformation|Searches common directories for key data and<br>credentials.|
|Scan|Runs nmap/nikto to fnd vulnerable services.<br>|
|LateralMove|Searches for and executes exploits from an in-<br>ternal library or Metasploit’s library.|
|EscalatePrivilege|Searches for and executes exploits from an in-<br>ternal library or Metasploit’s library|
|ExfiltrateData|Finds shortest path to attacker’s host and then<br>exfltrates the data.|



We design Incalmo to be extensible and note that both the set of abstract tasks and their specific implementations are extensible. Since we decouple the task API from the realization, tasks can accommodate multiple execution agents. For instance, in Sec. 6.2, we add LLM-based agents as alternative implementations. We also enable developers to add new high-level tasks. For instance, users can add a “stealth data exfiltration” task (examples in the open-source repository). 

_Auxiliary services._ Next, we detail the design of the three auxiliary services that help LLMs retrieve relevant context and enable reliable execution of red team tasks: (1) an environment state service to maintain environment knowledge, (2) an attack graph service to reason about potential attack paths, and (3) a C&C server service to reliably maintain and execute commands on assets. 

_(1) Environment state service:_ To tackle context bloat, PentestGPT and CAI use several heuristics such as using LLMs to summarize prior context (e.g., command outputs, chain-of-thought, etc). However, relevant information can still get buried in the context: a crucial clue could be discovered on a host, but it only becomes meaningful after several commands on a different host are executed. While this may not have been a critical flaw in single-host CTF challenges, this stale context quickly becomes a bottleneck in long-horizon, multi-host exercises. 

To avoid this context bloat, we design a queryable environment state service that maintains a structured knowledge base of the environment (akin to RAG [39]). LLMs can output high-level code that queries the service. The idea is that planning LLMs (and agents) query the environment state service for information when it becomes relevant for the attack. There are two challenges when designing an environment state service: (1) our knowledge of the network changes as attackers run tasks (e.g., a scan discovers a host); and (2) this knowledge needs to be exposed in a systematic way so the LLM can “reason” about the network (e.g., what services does a host have). To address these challenges, the environment state service maintains a structured database of Python objects that represent the environment, similar to Lore [26].<sup>11</sup> The database is updated as red team agents execute tasks. For instance, if an agent discovers hosts 

11. Lore uses traditional state-space exploration tools and algorithms for attack exploration, and is not designed to be exposed to LLMs as such. 

with a scan, the database will update and contain objects representing the new hosts. 

_(2) Attack graph service:_ We also introduce an attack graph service that helps Incalmo’s planning LLMs and agents correctly decide what tasks to execute [63]. Multihost environments are complex and it is difficult for LLMs to reason about how vulnerabilities can chain together, especially since attackers have _incomplete and evolving_ information. We design a dynamic attack graph service to help both the planning LLM and the agents reason about environments. Existing attack graph tools are often developed from a static defense perspective and assume complete and prior knowledge of the network [51], [50]. Our attack graph service dynamically retrieves the current best knowledge from the environment state service and can recommend the next best course(s) of action for the red team exercise. For instance, Incalmo’s lateral move agent queries the attack graph service to identify tasks to infect a host with the following query: 

<mark>attack_graph_service.get_possible_attack_paths( target_host)</mark> 

When calling this endpoint, the attack graph service will query the environment state service to obtain the current world view about host vulnerabilities and host reachability criteria to suggest next hosts to exploit. Our current implementation uses a simple brute-force search to discover these candidate paths, which we have found to be sufficiently scalable for environments on the order of 100s of nodes. 

_(3) C&C server service_ We design a high-level C&C server service to help task agents reliably execute commands and manage their assets. Instead of using low-level shell commands to manage assets, we abstract a C&C server as a service that (A) executes commands on an arbitrary infected user on a host, and (B) has an API endpoint to download and execute malware to infect additional hosts. Our current implementation handles all low-level communication techniques (e.g., proxying [54], beaconing [8]) internally. However, the C&C server service API can be extended to include options to configure these. 

### **4.3. Illustrative case study** 

In this section, we show a concrete end-to-end example of Incalmo using Sonnet 4 running in an interactive loop to run a red team exercise in the Equifax-inspired environment. In this example, Incalmo w/ Sonnet 4 is following similar steps as the real Equifax attacker in Fig. 3. In Fig. 9, we both show a timeline of the steps Incalmo took to red team the network and map key events to the real attack in Fig. 3. The full prompt and logs of this case study are in our opensource repository (see Open science section). 

_Onboarding._ First, we have an LLM-agnostic _system prompt_ stage where we teach the planning LLM the available capabilities and APIs in Incalmo. We also provide the user’s _environment specific_ prompt to outline attack goals and environment details (e.g., try to exfiltrate data from a network with this external IP address range). 


![](docs/paper-research/md-downloaded-paper-professor/images/06-incalmo-autonomous-llm-assisted-system-for-red-teaming.pdf-0009-00.png)


Figure 9. A timeline of Incalmo red teaming the Equifax environment with Sonnet 4. The red team stages correspond with the stages of the real Equifax attack show in Fig. 3. Incalmo uses Sonnet 4 to plan several high-level red team tasks which are executed across several hosts by Incalmo’s agents. 

_Execution._ Incalmo then uses a Sonnet-4-assisted workflow to plan and execute the red team exercise, shown in Fig. 9. Sonnet 4 outputs tasks, Incalmo agents execute them, the agents return any results or errors, and then Sonnet 4 reacts and decides the subsequent task(s), as shown in Fig. 9. 

Sonnet 4 first decided to scan Equifax’s external network. The Incalmo scanning agent discovered web servers and identified that they have remote code execution vulnerabilities ( **1** , Fig. 9). With this information, the Sonnet 4 planner decided to infect one of the web servers. Incalmo was able to infect the web server (through the lateral movement agent executing an exploit and installing malware). However, this turned out to be a dead end because Incalmo cannot use this web server to obtain further network access. 

After exploring this futile path, the Sonnet 4 planner decides to infect the other web server ( **2** , Fig. 9). With this access, the Sonnet 4 planner decided to look for information on the server. The find information agent used the C&C server connection to reliably execute commands and found plain-text SSH credentials ( **3** , Fig. 9). With these credentials, Sonnet 4 decided to infect all of the databases, again using the lateral movement agent ( **4** , Fig. 9). Finally, Sonnet 4 decided to exfiltrate the data from the database. The data exfiltration agent used the environment and attack graph services to identify an exfiltration path out of the network: copy the data to a web server, and then download the data to the attacker’s computer over HTTP ( **5** , Fig. 9). Incalmo then proceeds to use this workflow in a loop to infect and exfiltrate data from each of the 48 databases in 

the network (not shown in Fig. 9 for brevity). 

## **5. Implementation** 

We implement Incalmo as a Python framework consisting of around 8K lines of code. We implement a custom C&C server and use open-source malware capabilities (from the Caldera project [8]) to infect and send shell commands to hosts.<sup>12</sup> We implement Incalmo with custom Python modules. For the environment state service, we create parsers that interpret command outputs and update the knowledge base. 

For each of the five high-level tasks in Sec. 4, we create non-LLM and LLM-based agents that translate the tasks into low-level primitives (e.g., Python scripts, shell commands). We implement the non-LLM agents for the lateral movement and privilege escalation tasks by integrating into Incalmo’s internal library (or optionally Metasploit’s library) of known vulnerabilities and their corresponding exploits. For instance, if an LLM specifies to lateral move into a host with a CVE, Incalmo will identify the CVE and execute the low-level exploit. 

We use LangChain [37] to iteratively prompt LLMs. We first create a prompt with the onboarding process outlined in Sec. 4. During the execution phase, we extract the Python function between the <task></task> or <query></query> tags. Then Incalmo executes the function to get a list of tasks for the orchestrator to execute. Incalmo will execute attacks until an LLM specifies a <finished> tag or reaches a time limit. 

_MHBench._ To systematically evaluate Incalmo, we design and implement MHBench, a multi-host red teaming benchmark with 40 environments. We use Python and Ansible code to set up the environments atop OpenStack. The red team goal in 10 environments is to exfiltrate key data files and the goal in the remaining 30 environments is to gain root access to key hosts. We design MHBench to be diverse along key dimensions: (1) network size and topology, (2) type of vulnerabilities, and (3) red teaming complexity. 

In terms of network size, MHBench currently includes many small enterprise environments ranging from 22 to 50 hosts. For 30 of the environments, we algorithmically generate different topology structures that are similar to real-world environments [2], [3]. In addition, we manually design the topology of 10 environments based on topologies from prior work such as “Star”, “Chain”, and “Dumbbell” [36], [69], [18], [2], [40] and topologies from public reports of realworld attacks [43], [33]. The manually designed topologies are named based on the environment they were adapted from (e.g., Equifax environment). The algorithmically generated topologies are named based on the topology structure: “N4H41-G7” has four (sub)networks, 41 hosts and 7 critical assets (i.e., goals). 

In terms of vulnerabilities, MHBench includes diverse vulnerabilities such as common misconfigurations (e.g., 

12. We picked Caldera given our familiarity. Other C&C servers such as Cobalt Strike [19] or Merlin [45] could also be used. 

plain text credentials), remote code execution vulnerabilities (e.g., Apache Struts CVE-2017-5638), and privilege escalation vulnerabilities (e.g., sudo CVE-2021-3156). Several of these vulnerabilities have been used in real-world attacks [20], [33]. 

In terms of red teaming complexity, we vary the number of critical assets as well as the attack graph complexity. Across the environments, red team success spans a spectrum ranging from 2 to 48 assets and from 5 to 104 tasks. More details on the specifics of each environment are in Appendix B. 


![](docs/paper-research/md-downloaded-paper-professor/images/06-incalmo-autonomous-llm-assisted-system-for-red-teaming.pdf-0010-02.png)


## **6. Evaluation** 

In this section, we first show end-to-end experiments evaluating the success of Incalmo at autonomously conducting red team exercises in multi-host environments and compare it to baseline solutions. Then, we conduct an ablation study to understand the key factors that impact Incalmo’s success. 

_Setup._ We evaluate systems on MHBench by executing 5 trials with a time limit of 75 minutes per trial. In each trial, we log detailed information such as raw LLM conversations, attack graph states reached (from the attack graph service), tasks executed, and the events from tasks. We also use these logs to calculate MHBench metrics. 

_Baselines._ There is a large number of candidate baseline systems, environments, and LLMs we could use. We take a pragmatic approach to balance cost and brevity, rather than run all possible system-LLM pairs on all environments in MHBench.<sup>13</sup> We identify the best system-LLM combination from Sec. 2: ExpertPromptShell with Sonnet 4. First, we exhaustively compare Incalmo with Sonnet 4 to ExpertPromptShell with Sonnet 4 on all 40 environments in MHBench. Later, for the factor analysis, we use the 10 environments from Sec. 2, but evaluate many system-LLM combinations. 

_Metrics of success._ Consider an environment _e_ having a set of critical assets _Ce_ (e.g., a set of critical hosts or sensitive datasets). Each red team system, _a_ (i.e., the baselines and Incalmo described above) is evaluated across 5 trials _t_ 1 _, . . . t_ 5. Let _Ga,e,t ⊆_ 2<sup>_Ce_</sup> be the set of critical assets that _a_ managed to acquire in a given trial _t_ in environment _e_ . Let _Sa,e,t_ denote a binary success metric if _a_ was able to acquire _some_ critical asset _c_ in trial _t_ : _Sa,e,t_ = 1 `if` _|Ga,e,t | ≥_ 1; 0 `otherwise` . 

With this setup, we define three metrics of success: 

- _Success:_ For each red team system _a_ on _e_ , we consider it successful if _a_ is able to obtain at least one critical asset in at least one trial, similar to how red teams are measured today: _Successa,e_ = 1 _if ∃t s.t.|Ga,e,t | ≥_ 1; 0 _otherwise_ 

- _Reliability:_ We measure the reliability of a red team system _a_ in environment _e_ by counting the number 

13. A trial takes up to 75 minutes and costs up to $15. 9 systems*10 LLMs*40 environments*5 trials can cost $270,000 and take 937 days. 

Figure 10. The TotalAcquisition of Incalmo and ExpertPromptShell with Sonnet 4. We find that Incalmo obtained all of the critical assets in 9 out of 40 environments. 

- of trials the system is successful in terms of acquiring some critical asset: _Ra,e_ =<sup>�</sup> _t_<sup>_Sa,e,t_</sup> 

- _TotalAcquisition:_ We measure how comprehensive a red team system _a_ is in _e_ by counting the number of unique critical assets obtained across trials and dividing by the total number of possible critical assets: _Ca,e_ = _|_<sup>�</sup><sup>_T_</sup> _t_ =1<sup>_Ga,e,t|/|Ce|_</sup> 

### **6.1. Red team success evaluation** 

First, we evaluate Incalmo against ExpertPromptShell, the best performing prior system in Sec. 2, on all 40 environments in MHBench. We use Sonnet 4 for both systems because it had the highest performance with ExpertPromptShell in Sec. 2. We explore other LLMs in Sec. 6.2. 

**Finding 1.A** : In terms of the Success metric, Incalmo-Sonnet 4 succeeds in 37 out of 40 environments in MHBench while ExpertPromptShell with Sonnet 4 only succeeds in 3 out of 40 environments. (Fig. 2). 

We already saw in Fig. 2, that Incalmo-Sonnet4 succeeds in 37 out of 40 environments, while ExpertPromptShell-Sonnet-4 only succeeds in 3 out of 40 environments. From Fig. 2 we can also infer that w.r.t Reliability, Incalmo outperforms ExpertPromptShell. Specifically, Incalmo achieved perfect (i.e., 5 out of 5 trials) Reliability in 28 out of 40 environments but ExpertPromptShell is not perfect in any. 

**Finding 1.B** : In terms of the TotalAcquisition metric, Incalmo-Sonnet 4 succeeded in acquiring at least 50% of assets in 21 out of 40 environments. In contrast, ExpertPromptShell with Sonnet 4 never went above 24% in any environment (Fig. 10). 

With respect to TotalAcquisition, in 9 of the environments Incalmo was able to obtain 100% of critical as- 


![](docs/paper-research/md-downloaded-paper-professor/images/06-incalmo-autonomous-llm-assisted-system-for-red-teaming.pdf-0011-00.png)


Figure 11. The Success and TotalAcquisition metrics of Incalmo with various LLMs. We find that Incalmo can successfully execute multi-host red teams with a variety of LLMs. 

sets, whereas the maximum achieved by ExpertPromptShell was 24%. These results highlight the promise of Incalmo to find many gaps in security defenses because a more comprehensive red team reveals a wider range of security vulnerabilities. In Sec. 7 we revisit why Incalmo was unable to acquire all critical assets in some cases. 

### **6.2. Factor analysis** 

Next, we conduct experiments varying: (1) type of LLM executing the plan, and (2) disabling modules in Incalmo. For brevity and cost constraints, we execute these experiments on the 10 illustrative environments used in Sec. 2. 

_Impact of LLM choice._ We explore the impact of Incalmo using different LLMs to plan the red team. We evaluate Incalmo with 10 different LLMs: Haiku 3.5; Sonnet 3.5, 3.7, and 4; GPT4o and GPT4o Mini; Gemini Flash 1.5 and 2; and Gemini Pro 1.5 and 2.5. 

**Finding 2.A** : Incalmo successfully executes red teams with a variety of LLMs. Across all 10 LLMs, Incalmo successfully red teams 6—9 out of 10 representative environments w.r.t the Success metric (Fig. 11). 

In terms of the Success metric, across various LLMs, Incalmo is able to succeed in 9 out of 10 environments. In terms of the TotalAcquisition metric, Incalmo was able to obtain all critical assets in 5 out of 10 environments as seen in Fig. 11. For instance, in the Dumbbell A environment, Incalmo with all 10 LLMs is able to obtain at least one critical asset while none of the systems in Sec. 2 were able to. 

We also compare the Success and TotalAcquisition metrics of Incalmo with smaller LLMs to ExpertPromptShell with bigger LLMs. From each vendor, we evaluate a small and big LLM (e.g., GPT4o vs GPT4o mini). 


![](docs/paper-research/md-downloaded-paper-professor/images/06-incalmo-autonomous-llm-assisted-system-for-red-teaming.pdf-0011-09.png)


Figure 12. In terms of the Success metric, Incalmo with smaller LLMs succeeded in 9 out of 10 environments while larger LLMs with ExpertPromptShell only succeeded in 2. 

**Finding 2.B** : Incalmo using small LLMs obtained all critical assets in 5 out of 10 environments, while ExpertPromptShell with larger LLMs was unable to obtain all critical assets in any environment (Fig. 12) 

In Fig. 12, we show that in 9 out of 10 of the environments, Incalmo using smaller LLMs to plan red teams has better Success metrics than ExpertPromptShell with larger LLMs. For instance, in the Equifax environment, ExpertPromptShell with Sonnet 4 was able to exfiltrate a single file, but Incalmo with Haiku 3.5 was able to exfiltrate all 25 databases in the environment. In contrast to the sentiment that larger model sizes are more critical for performance [10], [32], in the red team domain, we see Incalmo’s abstractions are more critical than model size. 

_Impact of high-level tasks._ First, we create a version of Incalmo without high-level tasks, Incalmo-WHT, where LLMs do not have access to the five high-level tasks, but can use the environment and attack graph services. Here, LLMs can perform 19 predefined low-level tasks, such as reading a file or exploiting Apache Struts.<sup>14</sup> These low-level tasks mirror the library that Incalmo uses to translate high-level tasks. 

**Finding 3.A** : Incalmo-WHT was unable to succeed across all 10 environments and 10 LLMs, suggesting that the high-level task abstraction is an important factor for red team success (not shown for brevity). 

_Impact of Incalmo services._ Next, we create a variant of Incalmo without the environment and attack graph services called Incalmo-WS, but LLMs still have access to the five high-level tasks. Incalmo-WS’s agents still use the environment and attack graph services to be environment- 

14. We require the system to use predefined tasks to enable the environment and attack graph services. 


![](docs/paper-research/md-downloaded-paper-professor/images/06-incalmo-autonomous-llm-assisted-system-for-red-teaming.pdf-0012-00.png)


Figure 13. Success and TotalAcquisition metrics of Incalmo and IncalmoWS. Incalmo was able to succeed in 1–5 more environments than IncalmoWS. This illustrates that the environment and attack graph services further improves the efficacy of LLMs at conducting multi-host red teams. 


![](docs/paper-research/md-downloaded-paper-professor/images/06-incalmo-autonomous-llm-assisted-system-for-red-teaming.pdf-0012-02.png)


Figure 14. Minutes taken for Incalmo to obtain all critical assets. Incalmo red teams range from taking 14 to 70 minutes. 

agnostic, but the services are not accessible to the LLM (unlike Incalmo). 

In Fig. 13, we compare Incalmo-WS to Incalmo across a variety of LLMs. Unlike Incalmo-WHT, Incalmo-WS was sometimes able to obtain critical assets. However, in terms of Success, Incalmo was able to succeed in 1 to 5 more environments. 

**Finding 3.B** : In terms of the Success metric, Incalmo was able to succeed in 1 to 5 more environments than Incalmo-WS, suggesting that Incalmo services can further improve red team success (Fig. 13). 

For instance, Incalmo-WS with GPT4o mini only obtained critical assets in three environments. In contrast, Incalmo with GPT4o obtained critical assets in eight environments. 


![](docs/paper-research/md-downloaded-paper-professor/images/06-incalmo-autonomous-llm-assisted-system-for-red-teaming.pdf-0012-08.png)


Figure 15. The Success and TotalAcquisition metrics of Incalmo with Sonnet 3.5 task agents in three environments. Sonnet 3.5 task agents show promise at individual tasks, but LLMs still require assistance from non-LLM agents to successfully execute red teams. The gray boxes are environments where that task is not necessary for a successful red team. 

### **6.3. Cost and speed** 

Next, we measure the speed and cost of Incalmo. In terms of speed, Incalmo can rapidly run red team exercises. For instance, in the Enterprise C environment, Incalmo is able to successfully gain root access on all 15 critical hosts in 12 to 18 minutes (Fig. 14). Similarly, Incalmo can exfiltrate data from all 48 databases in the Equifax-inspired environment in just 54 minutes. 

However, some LLMs were inefficient in the red team exercise. For instance, in one trial of Dumbbell A, IncalmoHaiku 3.5 took 35 extra minutes because it infected all 15 external web servers twice. Incalmo-Haiku 3.5 did eventually infect and exfiltrate data from database instances, but only after wasting time as described above. 

Overall, running autonomous red team exercises on multi-host networks with Incalmo is relatively inexpensive. For instance, the Incalmo-Gemini 2 Flash usage is within the free tier. The most expensive Incalmo experiment used Sonnet 3.5 with 5,750K input tokens and 60K output tokens; or around $15. A breakdown of tokens used by Incalmo is in Appendix C. 

Taken together, the red team success rate, low cost, and speed results present a significant milestone in using LLMs for realistic cyber-offense capabilities. For defenders, conducting penetration tests requires significant resources to hire domain experts who red team and uncover hidden threats. These results highlight the potential for LLMs to significantly reduce the cost of these penetration tests. 

### **6.4. Extensibility case study** 

Next, we demonstrate how Incalmo is extensible to support new task-specific agents. In the prior evaluations, tasks are executed by deterministic agents. In this case study, we explore adding LLM-based task agents to Incalmo. For example, when the planning LLM initiates a lateral movement task, instead of using the predefined Incalmo agent, we consider introducing a new LLM-based agent to dynamically execute the task with low-level commands, but still has access to helpful services like the C&C server service. For the case study, we design an LLM-based agent for each of the five tasks. 

As an illustration, we show the setting of Incalmo with Sonnet 3.5 to both plan the red team and have the LLMbased task agents use Sonnet 3.5 in three environments: Equifax-inspired, Enterprise C, and 6-layer star. (We see similar results for Sonnet 4, the top performing model.) To bound the cost, we limit each LLM-based task agent to 10 interactions for each task. We consider two experimental setups: (1) _all_ task agents use Sonnet 3.5 instead of Incalmo and (2) replace Incalmo task agents _one at a time_ . 

**Finding 4** : Sonnet 3.5-based task agents show promise at executing lateral movement, network scanning, privilege escalation, and data exfiltration. But LLM planners still require assistance from nonLLM agents to succeed (Fig. 15). 

In the “all” setup, Sonnet 3.5 as the planner only using Sonnet 3.5 task agents was unable to succeed in any of the 3 evaluated environments, as seen in Fig. 15. However, when replacing a single Incalmo agent for LLM-based agents, Sonnet 3.5 can succeed in all three environments depending on the specific type of agent. For instance, Sonnet 3.5 with a Sonnet 3.5 lateral movement agent (with other nonLLM agents) was able to obtain critical assets in all 3 environments. 

This study also serves two other purposes. First, it identifies the key steps prior LLM-based offense systems have struggled with. Second, it suggests a roadmap to tackle 0-day vulnerabilities via novel AI-based agents when the existing agents lack coverage [73]. 

## **7. Discussion and limitations** 

Next, we briefly discuss limitations and directions for improving the capabilities in Incalmo. 

_Improve TotalAcquisition._ We saw that Incalmo was unable to obtain _all_ critical assets in some exercises. In some cases, the LLM planner obtained a single critical asset and then stopped. In many trials, we observed the LLM planner could have queried the Incalmo attack graph service to identify that there were additional paths to explore, but did not do so. We speculate this could be because LLMs may not have much training data for red teaming multi-host networks using attack graphs. An interesting direction for future work is to improve coverage (e.g., further train and fine-tune LLMs to better leverage the attack graph service). 

_Reducing failure scenarios._ We saw Incalmo was unable to succeed in 3 environments. On further analysis, we found that these settings required both external scans (e.g., to identify vulnerable web servers) and internal scans (e.g., to identify a vulnerable database management server). At a high level, the current LLM-assisted workflow seems to lack an understanding that scanning from different network locations could have different results. We hypothesize that this can be addressed by improving the Incalmo attack graph service to reason about network segments and access control (e.g., need to be on same subnet to access a host because 

of inter-segment firewalls). We believe that extending the attack graph service to reason about fine-grained access control could further improve Success and also help improve TotalAcquisition. 

_Extending Incalmo to handle 0-days._ In this paper, we scoped our exploration to consider exercises with known vulnerabilities. Since Incalmo is extensible, future versions could support advanced 0-day specific task agents to further improve red team effectiveness [73]. 

_Environment realism._ In general, enterprise network details are considered sensitive and there is little public information. MHBench is our best effort attempt using a variety of public sources and prior reports to design realistic environments [43], [33], [2], [18]. An interesting direction of future work is to extend MHBench and use Incalmo on a broader range of real (possibly proprietary) enterprise settings at scale. 

_Adding defenders in the loop._ As a first step toward understanding the feasibility of LLM-assisted red teaming in multi-host network settings, we evaluate Incalmo in environments without defenders. An interesting direction for future work is to extend this to settings with realistic (and possibly autonomous) defenses in place and also add features to Incalmo to evade detection. 

_Memorization._ A concern with LLMs is the memorization of training data. Given that the prior LLM-offense systems failed in MHBench, they may have not been exposed to multi-host network challenges. In contrast, LLMs’ success with CTF challenges [80], [14], [71], [49] may be due to publicly available solutions in training data. However, as MHBench will be released, LLM providers may incorporate MHBench in the training data. Similar to other efforts [1], we envision MHBench as evolving and using “holdout” tests in the future. 

## **8. Other related work** 

We discussed most of the closely related work on LLMassisted cyber offense capabilities in Sec. 2. Before we conclude, we briefly discuss other related work. 

_LLM security benchmarks._ As mentioned in Sec. 2, there are many benchmarks for evaluating LLMs in CTF challenges (e.g., [61], [76], [72], [72], [7], [56]). However, they are challenge problems and single host attacks. Other non-CTF benchmarks evaluate general security knowledge (e.g., [68]). 

_Other research in LLMs for security._ In addition, there is work to create LLM-based systems for other security tasks. For instance, there is work evaluating LLMs ability to find vulnerable code (e.g., [72]), using LLMs to summarize defender security logs (e.g., [13]), and using LLMs for anomaly detection (e.g., [15]). Other work has shown how LLMs can be used for social engineering tasks like phishing [57], [25]. These are orthogonal to our focus on multi-host red teams. 

## **9. Conclusions** 

We identify a key gap in existing LLM-based offense capabilities: autonomously executing red teaming exercises in multi-host environments. We showed that state-of-theart LLM-assisted cyber offense systems struggle in this setting and shed light on the key failure modes of existing solutions. By raising the level of abstraction via decoupling of planning and execution and introducing domain-specific task agents, Incalmo demonstrates the feasibility of LLMassisted red teaming in complex multi-host settings. Across a majority of the diverse environments in MHBench, Incalmo can autonomously find vulnerable services, execute exploits, gain access to networks, discover configurations and vulnerabilities to laterally move, exploit vulnerabilities to escalate privileges, and exfiltrate data. 

We believe Incalmo and MHBench represent a significant advance in our understanding of LLM-assisted red teaming capabilities in realistic multi-host settings. We believe that by lowering the barrier for defenders to run red teaming exercises quickly, cheaply, and often, we can better enable them to proactively protect their networks against future attacks (both human and AI-based). We hope our work spurs further advances in the “science of security” in the use of AI-assisted autonomous cyber defense and offense capabilities. 

## **Ethics considerations** 

In computer security, there is a history of developing dual-use technologies [64], [53]. For example: fuzzing can find bugs for defenders to patch or attacker to exploit, malware research can help defenders detect malware or attackers evade malware detection, and adversarial ML techniques can help defenders train better models or help attackers trick existing models. In many cases, such dual-use technologies benefit defenders more than attackers [64], [53]. 

We acknowledge that Incalmo follows this trend as a dual-use technology: defenders can use Incalmo to proactively test their networks to discover security gaps or real attackers can use Incalmo to attack networks. Incalmo poses similar risks as other tools in this space such as prior LLMbased attack systems [80], [14], [44], [73] and non-LLM attack systems [8], [19], [16], [45]. 

However, understanding the limits of AI-assisted autonomous attacks can benefit red teams as shown in this paper. It will also help defenders guard against future AIassisted attackers by helping them play on a level footing by proactively assessing vulnerabilities and security gaps in their networks. Finally, we believe that understanding the limits and capabilities of LLM-assisted offense capabilities whether for red teaming or attacks, is valuable to advance the science of AI-meets-security for key stakeholders across academia, industry, governments, and policymakers. 

Next, we primarily discuss the ethical principle of beneficence with respect to several key stakeholders because it is the most relevant: 

- **LLM providers** LLM providers could both benefit and face harm from this research. LLM providers could benefit by profiting off of future Incalmo-like tools that use LLMs to find security gaps in networks. This research could also harm the reputation of providers if bad actors utilize LLMs to maliciously hack networks using LLMs. Furthermore, the research could impact the profits of providers if policymakers decide to regulate the usage of LLMs based on our findings. 

- **Companies** Similar to LLM providers, companies could both benefit and face harm from this research. Companies already use non-LLM autonomous attack tools [19], [8] to find gaps in their security. Similarly, companies could use the results of this research for the same purpose. However, similar to other autonomous attack tools, bad actors could use these tools to cause harm against companies such as a cyber attack. 

- **Policymakers** There is great interest in regulating AI technology by government organizations and policymakers. Incalmo and MHBench can assist policymakers in measuring the red teaming capability of LLMs. Many government agencies and frontier labs are already evaluating other cybersecurity capabilities of LLMs [71], [80], [49] to help inform their policies and our research further sheds light on these capabilities. 

- **Security vendors** Security vendors could benefit from Incalmo helping them assess networks for security gaps. Their customers could benefit from dramatically lowered cost, time, and effort needed to launch complex red teaming exercises. 

- **Society at large** As society becomes more dependent on technology, the security risks increase. Autonomous attack tools can both help prevent these security risks and lower the bar for bad actors to execute attacks. 

_Decision._ We decided to proceed with this research because we believe the benefits of autonomous red teaming outweigh the potential harms. Our belief is consistent with similar prior systems [14], [80], [8], [75], [28], [54], [35], [73] and the analysis of that practice in computer security research [64]. Furthermore, we also mitigated the risks to LLM providers by preemptively notifying the providers to add guardrails if they choose to do so. 

_Open Science._ In addition, reproducibility and transparency are key tenets to scientific research [48]. Open source code both assists researchers to reproduce this work and accelerates scientific progress. As a result, similar to other prior offensive systems [14], [80], [8], [54], [44], MHBench, our tools to reproduce prior work, and Incalmo will be open source and publicly available to the research community: https://github.com/bsinger98/Incalmo. 

## **LLM usage considerations** 

_Originality:_ LLMs were used for editorial purposes in this manuscript, and all outputs were inspected by the authors to ensure accuracy and originality. 

_Transparency:_ We evaluated Incalmo with both openand closed-source LLMs, but we only observed meaningful 

results with the closed-source models. We acknowledge that closed-source LLMs may make some of the results harder to reproduce. However, we mitigate this limitation by open-sourcing MHBench, prompts, model numbers, and Incalmo’s code. We also show in Sec. 6 that Incalmo performs well across a diverse range of LLMs. As open-source LLMs increase in capabilities, we envision these models could be used instead of closed-source LLMs. 

_Responsibility:_ We are unable to calculate exact carbon footprints for our experiments [31]. Experiments cost at most $15 of credits and in total we spent around $3,000 of LLM credits across providers. We also took care to design and debug Incalmo on smaller LLMs before executing thorough evaluations to minimize the environmental impact. Furthermore, cyberattacks are extraordinarily costly (in terms of money, energy, human harm, etc) for society [20], [33]. As a result, we conclude that the potential benefits of reducing the cost of red teaming networks to proactively find security gaps outweigh the environmental impact of the research. 

## **References** 

- [1] Humanity’s Last Exam. https://agi.safe.ai/, accessed: Apr 23, 2025. 

- [2] Enterprise Campus 3.0 Architecture: Overview and Framework. Technical report, Cisco, April 2008. 

- [3] Hierarchical Tree Topology. Technical report, IBM, January 2024. 

- [4] A. B. Ajmal, M. A. Shah, C. Maple, M. N. Asghar, and S. U. Islam. Offensive security: Towards proactive threat hunting via adversary emulation. _IEEE Access_ , 2021. 

- [5] H. S. Al-Sinani and C. J. Mitchell. Pentest++: Elevating ethical hacking with ai and automation. _arXiv:2502.09484_ , 2025. 

- [6] Anthropic. Threat intelligence report: August 2025. Technical report, Anthropic, San Francisco, CA, USA, Aug. 2025. Available at https://www-cdn.anthropic.com/ b2a76c6f6992465c09a6f2fce282f6c0cea8c200.pdf. 

- [7] A. Anurin, J. Ng, K. Schaffer, J. Schreiber, and E. Kran. Catastrophic cyber capabilities benchmark (3cb): Robustly evaluating llm agent cyber offense capabilities. _arXiv:2410.09114_ , 2024. 

- [8] A. Applebaum, D. Miller, B. Strom, C. Korban, and R. Wolf. Intelligent, Automated Red Team Emulation. In _Proceedings of the 32nd Annual Conference on Computer Security Applications_ , 2016. 

- [9] L. Bilge and T. Dumitras¸. Before we knew it: an empirical study of zero-day attacks in the real world. In _ACM CCS_ , 2012. 

- [10] T. B. Brown. Language models are few-shot learners. _arXiv:2005.14165_ , 2020. 

- [11] M. Cemri, M. Z. Pan, S. Yang, L. A. Agrawal, B. Chopra, R. Tiwari, K. Keutzer, A. Parameswaran, D. Klein, K. Ramchandran, et al. Why do multi-agent llm systems fail? _arXiv:2503.13657_ , 2025. 

- [12] M. Corporation. MITRE ATT&CK® Framework. https://attack.mitre. org/. 

- [13] M. Corporation. Microsoft Security Copilot, 2023. 

- [14] G. Deng, Y. Liu, V. Mayoral-Vilches, P. Liu, Y. Li, Y. Xu, T. Zhang, Y. Liu, M. Pinzger, and S. Rass. PentestGPT: Evaluating and Harnessing Large Language Models for Automated Penetration Testing. In _USENIX_ , 2024. 

- [15] A. Elhafsi, R. Sinha, C. Agia, E. Schmerling, I. A. Nesnas, and M. Pavone. Semantic anomaly detection with large language models. _Autonomous Robots_ , 47(8):1035–1055, 2023. 

- [16] S. Y. Enoch, Z. Huang, C. Y. Moon, D. Lee, M. K. Ahn, and D. S. Kim. Harmer: Cyber-attacks automation and evaluation. _IEEE Access_ , 8:129397–129414, 2020. 

- [17] R. Fang, R. Bindu, A. Gupta, Q. Zhan, and D. Kang. Teams of llm agents can exploit zero-day vulnerabilities. _arXiv:2406.01637_ , 2024. 

- [18] K. J. Ferguson-Walter, M. M. Major, C. K. Johnson, and D. H. Muhleman. Examining the efficacy of decoy-based and psychological cyber deception. In _USENIX_ , 2021. 

- [19] Fortra. Cobalt Strike. https://www.cobaltstrike.com/. 

- [20] FTC. Equifax Data Breach Settlement. Technical report, December 2022. 

- [21] L. Gao, A. Madaan, S. Zhou, U. Alon, P. Liu, Y. Yang, J. Callan, and G. Neubig. Pal: Program-aided language models. In _International Conference on Machine Learning_ . PMLR, 2023. 

- [22] L. Hackl¨ander-Jansen. Emulating complete, realistic cyber attack chains with the new caldera bounty hunter plugin, 2024. Medium (MITRE Caldera). Accessed: 2025-11-11. 

- [23] A. Happe and J. Cito. Getting pwn’d by ai: Penetration testing with large language models. In _ACM ESEC_ , 2023. 

- [24] A. Happe and J. Cito. Can llms hack enterprise networks? autonomous assumed breach penetration-testing active directory networks. _ACM TOSEM_ , 2025. 

- [25] F. Heiding, S. Lermen, A. Kao, B. Schneier, and A. Vishwanath. Evaluating Large Language Models’ Capability to Launch Fully Automated Spear Phishing Campaigns: Validated on Human Subjects. _arXiv:2412.00586_ , 2024. 

- [26] H. Holm. Lore a red team emulation tool. _IEEE Transactions on Dependable and Secure Computing_ , 2022. 

- [27] H. Holm and T. Sommestad. SVED: Scanning, vulnerabilities, exploits and detection. In _MILCOM 2016 IEEE Military Communications Conference_ . IEEE, 2016. 

- [28] Z. Hu, R. Beuran, and Y. Tan. Automated penetration testing using deep reinforcement learning. In _IEEE EuroS&PW_ . https://github. com/crond-jaist/AutoPentest-DRL. 

- [29] J. Huang and Q. Zhu. PenHeal: A Two-Stage LLM Framework for Automated Pentesting and Optimal Remediation. In _Proceedings of the Workshop on Autonomous Cybersecurity_ . Association for Computing Machinery, 2024. 

- [30] E. M. Hutchins, M. J. Cloppert, R. M. Amin, et al. Intelligencedriven computer network defense informed by analysis of adversary campaigns and intrusion kill chains. _Leading Issues in Information Warfare & Security Research_ , 2011. 

- [31] N. Jegham, M. Abdelatti, L. Elmoubarki, and A. Hendawi. How hungry is ai? benchmarking energy, water, and carbon footprint of llm inference. _arXiv:2505.09598_ , 2025. 

- [32] J. Kaplan, S. McCandlish, T. Henighan, T. B. Brown, B. Chess, R. Child, S. Gray, A. Radford, J. Wu, and D. Amodei. Scaling laws for neural language models. _arXiv:2001.08361_ , 2020. 

- [33] S. M. Kerner. Colonial Pipeline hack explained: Everything you need to know. _TechTarget_ , 2022. 

- [34] H. Kong, D. Hu, J. Ge, L. Li, T. Li, and B. Wu. Vulnbot: Autonomous penetration testing for a multi-agent collaborative framework. _arXiv:2501.13411_ , 2025. 

- [35] M. Kouremetis, M. Dotter, A. Byrne, D. Martin, E. Michalak, G. Russo, M. Threet, and G. Zarrella. Occult: Evaluating large language models for offensive cyber operation capabilities. _arXiv:2502.15797_ , 2025. 

- [36] M. Kouremetis, D. Lawrence, R. Alford, Z. Cheuvront, D. Davila, B. Geyer, T. Haigh, E. Michalak, R. Murphy, and G. Russo. Mirage: cyber deception against autonomous cyber attacks in emulation and simulation. _Annals of Telecommunications_ , 2024. 

- [37] LangChain. Langchain: Building applications with llms through composability. https://github.com/langchain-ai/langchain, 2025. 

- [38] R. M. Lee, M. Assante, and T. Conway. CRASHOVERRIDE: Analysis of the threat to electric grid operations. 2017. 

- [39] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. K¨uttler, M. Lewis, W.-t. Yih, T. Rockt¨aschel, et al. Retrievalaugmented generation for knowledge-intensive nlp tasks. _NeurIPS_ , 2020. 

- [40] J. Li, Y. Luan, X. Wu, and J.-a. Lu. Synchronizability of double-layer dumbbell networks. _Chaos: An Interdisciplinary Journal of Nonlinear Science_ , 2021. 

- [41] P. Lu, B. Peng, H. Cheng, M. Galley, K.-W. Chang, Y. N. Wu, S.-C. Zhu, and J. Gao. Chameleon: Plug-and-play compositional reasoning with large language models. _NeurIPS_ , 2024. 

- [42] G. F. Lyon. _Nmap network scanning: The official Nmap project guide to network discovery and security scanning_ . Insecure, 2009. 

- [43] Majority Staff Report 115th Congress. The Equifax Data Breach. Technical report, December 2018. 

- [44] V. Mayoral-Vilches, L. J. Navarrete-Lozano, M. Sanz-G´omez, L. S. Espejo, M. Crespo- Alvarez, F. Oca-Gonzalez, F. Balassone, A. Glera-<sup>´</sup> Pic´on, U. Ayucar-Carbajo, J. A. Ruiz-Alcalde, et al. Cai: An open, bug bounty-ready cybersecurity ai. _arXiv:2504.06017_ , 2025. 

- [45] Ne0nd0g. Merlin. https://github.com/Ne0nd0g/merlin. 

- [46] J. Nuce, J. Kennelly, K. Goody, A. Moore, A. Rahman, M. Williams, B. McKeague, and J. Wilson. Shining a light on darkside ransomware operations. _FireEye Blogs_ , 2021. 

- [47] J. G. Oakley. _Professional red teaming: conducting successful cybersecurity engagements_ . Apress, 2019. 

- [48] N. A. of Sciences, Medicine, Policy, G. Affairs, B. on Research Data, D. on Engineering, P. Sciences, C. on Applied, T. Statistics, B. on Mathematical Sciences, et al. _Reproducibility and replicability in science_ . National Academies Press, 2019. 

- [49] OpenAI. OpenAI o1 System Card. https://openai.com/index/ openai-o1-system-card/, 2024. 

- [50] X. Ou, W. F. Boyer, and M. A. McQueen. A scalable approach to attack graph generation. In _ACM CCS_ , 2006. 

- [51] X. Ou, S. Govindavajhala, A. W. Appel, et al. Mulval: A logic-based network security analyzer. In _USENIX_ . Baltimore, MD, 2005. 

- [52] A. PBC. Disrupting the first reported ai-orchestrated cyber espionage campaign. Technical report, November 2025. 

- [53] T. S. Rad. The sword and the shield: Hacking tools as offensive weapons and defensive tools. _Geo. J. Int’l Aff._ , 16:123, 2015. 

- [54] Rapid7. Metasploit. https://www.metasploit.com/. 

- [55] J. Rehberger. _Cybersecurity Attacks–Red Team Strategies: A practical guide to building a penetration testing program having homefield advantage_ . Packt Publishing Ltd, 2020. 

- [56] M. Rodriguez, R. A. Popa, F. Flynn, L. Liang, A. Dafoe, and A. Wang. A framework for evaluating emerging cyberattack capabilities of ai. _arXiv:2503.11917_ , 2025. 

- [57] S. S. Roy, P. Thota, K. V. Naragam, and S. Nilizadeh. From Chatbots to Phishbots?: Phishing Scam Generation in Commercial Large Language Models. In _IEEE S&P_ , 2024. 

- [58] T. Schick, J. Dwivedi-Yu, R. Dess`ı, R. Raileanu, M. Lomeli, E. Hambro, L. Zettlemoyer, N. Cancedda, and T. Scialom. Toolformer: Language models can teach themselves to use tools. _NeurIPS_ , 2024. 

- [59] S. L. Schraker, G. Apruzzese, S. Human, P. Laskov, H. S. Anderson, E. W. Bernroider, A. Fass, B. Nassi, V. Rimmer, F. Roli, et al. SoK: On the offensive potential of AI. _arXiv:2412.18442_ , 2024. 

- [60] M. Shao, B. Chen, S. Jancheska, B. Dolan-Gavitt, S. Garg, R. Karri, and M. Shafique. An empirical evaluation of llms for solving offensive security challenges. _arXiv:2402.11814_ , 2024. 

- [61] M. Shao, S. Jancheska, M. Udeshi, B. Dolan-Gavitt, H. Xi, K. Milner, B. Chen, M. Yin, S. Garg, P. Krishnamurthy, et al. Nyu ctf dataset: A scalable open-source benchmark dataset for evaluating llms in offensive security. _arXiv:2406.05590_ , 2024. 

- [62] M. Shao, H. Xi, N. Rani, M. Udeshi, V. S. C. Putrevu, K. Milner, B. Dolan-Gavitt, S. K. Shukla, P. Krishnamurthy, F. Khorrami, et al. CRAKEN: Cybersecurity LLM Agent with Knowledge-Based Execution. _arXiv:2505.17107_ , 2025. 

- [63] O. Sheyner, J. Haines, S. Jha, R. Lippmann, and J. M. Wing. Automated generation and analysis of attack graphs. In _IEEE S&P_ , 2002. 

- [64] M. Silic. Dual-use open source security software in organizations– dilemma: help or hinder? _Computers & Security_ , 39:386–395, 2013. 

- [65] B. Singer, A. Pandey, S. Li, L. Bauer, C. Miller, L. Pileggi, and V. Sekar. Shedding light on inconsistencies in grid cybersecurity: Disconnects and recommendations. In _IEEE S&P_ , 2023. 

- [66] J. Steube. Hashcat: Advanced Password Recovery. https://hashcat. net/hashcat/, 2025. 

- [67] I. Takaesu. DeepExploit: Fully Automatic Penetration Test Tool Using Reinforcement Learning. https://github.com/13o-bbr-bbq/machine learning <u>security,</u> 2018. 

- [68] N. Tihanyi, M. A. Ferrag, R. Jain, and M.-o. Debbah. Cybermetric: A benchmark dataset for evaluating large language models knowledge in cybersecurity. _arXiv:2402.07688_ , 2024. 

- [69] S. T. Trassare, R. Beverly, and D. Alderson. A technique for network topology deception. In _MILCOM IEEE Military Communications Conference_ . IEEE, 2013. 

- [70] S. Ullah, P. Balasubramanian, W. Guo, A. Burnett, H. Pearce, C. Kruegel, G. Vigna, and G. Stringhini. From cve entries to verifiable exploits: An automated multi-agent framework for reproducing cves. _arXiv:2509.01835_ , 2025. 

- [71] US AI Safety Institute and UK AI Safety Institute. US AISI and UK AISI Joint Pre-Deployment Test: Anthropic’s Claude 3.5 Sonnet. Technical report, National Institute of Standards and Technology, November 2024. 

- [72] S. Wan, C. Nikolaidis, D. Song, D. Molnar, J. Crnkovich, J. Grace, M. Bhatt, S. Chennabasappa, S. Whitman, S. Ding, et al. Cyberseceval 3: Advancing the evaluation of cybersecurity risks and capabilities in large language models. _arXiv:2408.01605_ , 2024. 

- [73] Z. Wang, T. Shi, J. He, M. Cai, J. Zhang, and D. Song. Cybergym: Evaluating ai agents’ cybersecurity capabilities with real-world vulnerabilities at scale. _arXiv:2506.02548_ , 2025. 

- [74] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, D. Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. _NeurIPS_ , 2022. 

- [75] J. Xu, J. W. Stokes, G. McDonald, X. Bai, D. Marshall, S. Wang, A. Swaminathan, and Z. Li. Autoattacker: A large language model guided system to implement automatic cyber-attacks. _arXiv:2403.01038_ , 2024. 

- [76] J. Yang, A. Prabhakar, K. Narasimhan, and S. Yao. InterCode: Standardizing and Benchmarking Interactive Coding with Execution Feedback. In _NeurIPS_ , 2023. 

- [77] J. Yang, A. Prabhakar, S. Yao, K. Pei, and K. R. Narasimhan. Language agents as hackers: Evaluating cybersecurity skills with capture the flag. In _Multi-Agent Security Workshop NeurIPS_ , 2023. 

- [78] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao. React: Synergizing reasoning and acting in language models. In _ICLR_ , 2023. 

- [79] J. D. Yoo, E. Park, G. Lee, M. K. Ahn, D. Kim, S. Seo, and H. K. Kim. Cyber attack and defense emulation agents. _Applied Sciences_ , 10(6):2140, 2020. 

- [80] A. K. Zhang, N. Perry, R. Dulepet, J. Ji, J. W. Lin, E. Jones, C. Menders, G. Hussein, S. Liu, D. Jasper, et al. Cybench: A Framework for Evaluating Cybersecurity Capabilities and Risks of Language Models. _arXiv:2408.08926_ , 2024. 

TABLE 3. TOKEN COST OF MULTI-HOST ATTACKS IN 1,000S OF TOKENS 

|LLM|I|nput Tok|ens|Out|put Toke|ns|
|---|---|---|---|---|---|---|
||Min|Mean|Max|Min|Mean|Max|
|GPT4o mini<br>|4.1<br>|104.4<br>|1474.3<br>|0.2<br>|0.2<br>|15.6<br>|
|GPT4o|9.4|106.5|1005.7|0.9|3.2|11.9|
|Gemini 1.5 Flash|3.5|9.8|26.1|0.2|0.2|0.7|
|Gemini 2 Flash<br>|12.2<br>|137.2|1189.1|1.0|3.0|10.9|
|Gemini 1.5 Pro<br>|6.7|29.1|243.2|0.3|1.0|4.4|
|Gemini 2.5 Pro|7.4|672.4|2022|0.9|9.7|19.8|
|Haiku 3.5<br>|14.6<br>|799.2|4241.7<br>|1.4<br>|12.5|50.9|
|Sonnet 3.5|57.5|862.8|5897.1|5.0|19.3|60.1|
|Sonnet 3.7<br>|61.0<br>|279.3<br>|997.8<br>|2.5<br>|6.0<br>|19.6<br>|
|Sonnet 4|2.5|268.7|1515.3|0.8|7.2|15.6|



## **Appendix A. Attack Graph Formalism and Log analysis** 

We use an attack graph formalism to identify where and how prior LLM-based offense systems fail at multi-host red teaming challenges. We then describe the log analysis we conduct with this formalism. 

_Attack graph formalism._ Formally, an attack graph is defined as _G_ = ( _S, A, So, Sg_ ) where _S_ is a set of states, _A ⊆ S ×S_ is the set of actions (directed edges) representing transitions between these states, _Sg ⊆ S_ is the set of goal states, and _So ⊆ S_ is the set of initial states [63]. Intuitively, the nodes are attacker states (e.g., gained access to web server) and the edges are attack actions (e.g., exfiltrate data). We define a successful attack path, where an attacker reaches all of their goals, as _π_ = ( _s_ 0 _, s_ 1 _, . . . , sn_ ) such that _Sg ⊆ {s_ 0 _, s_ 1 _, . . . , sn}_ . 

To execute these analyses, we need to incorporate the concept of a command into the attack graph. Each action _a ∈ A_ is composed of a _sequence of commands_ . A single command is defined as a function _c_ : ( _h, n, p_ ) _�→ o_ where _h_ is the host on which the command is run, _n_ is the name of the command, _p_ are the parameters of the command, and _o_ is the output of the command. 

For each environment, we manually create a reference attack graph and a minimal sequence of commands for an attack: _C_ man = ( _c_ 1 _, c_ 2 _, . . . , cm_ ).<sup>15</sup> Here, a single command is defined as a function _c_ : ( _h, n, p_ ) _�→ o_ where _h_ is the host on which the command is run, _n_ is the name of the command, _p_ are the parameters of the command, and _o_ is the output of the command. 

_Log analysis._ Similar to prior work, we break down our multi-host challenges into tasks [80] (e.g., find a CVE). For example, the Equifax-inspired environment requires 246 tasks to obtain _all critical data_ . For each environment, we manually create a reference solution, both a set of tasks necessary to access _all critical assets_ and a set of commands to implement each task. 

To track if ExpertPromptShell successfully achieved tasks, we use the following heuristic. For each command in 

15. For most of the environments, there is only one successful attack path. 

the reference solution, we store the command’s output. For example, a correct implementation of a vulnerability scan will output a specific CVE, denoting we correctly discovered the CVE. Given a sequence of commands generated by ExpertPromptShell’s LLM, we can match keywords in the output against the reference solution outputs. If it matches, we consider ExpertPromptShell to have successfully executed that atomic task.<sup>16</sup> 

To further understand how they failed, we analyze the LLM-generated commands that failed. This analysis requires significant manual effort so we focus on two environments where ExpertPromptShell performed the best: the Equifaxinspired and 4-Layer Chain environments. 

_Irrelevant tasks._ For each task, we tag the task as irrelevant if the task’s command’s name and command’s host do not appear in _any_ command in the reference solution. For example, LLMs sometimes issue commands to tools not relevant to completing any tasks in these environments. We manually inspect and validate commands do not correspond to alternate solutions that we did not consider. 

_Incorrectly implemented commands._ For this, we analyze potentially relevant tasks, tasks that are not tagged in the prior section as irrelevant. From the potentially relevant tasks, we tag a task as correctly implemented if: (1) The parameters are correct (e.g., an nmap scan has the correct flags); and (2) command has no syntax errors. 

## **Appendix B. Environments** 

In this section, we give detailed descriptions of each environment. We algorithmically generate 30 environments in MHBench. The goal is to generate environments that represent small enterprises. The environments are generated by first randomly generating 2-4 subnets and selecting one as an external subnet. Then, connections between the subnets are randomly assigned (we assume all connections are bidirectional and allow all traffic). For each subnet, we randomly generate between 7 and 15 hosts. Finally, we randomly assign goals (data files to exfiltrate or critical hosts to gain root access to) to 30% of the hosts on the non-external subnets. 

Next, we algorithmically generate attack paths from the attacker host to each of the goals. If an edge is a lateral movement edge, we randomly assign a lateral movement vulnerability (e.g., vulnerable Apache Struts service) or a misconfiguration (e.g., plaintext credentials). If an edge is a privilege escalation edge, we randomly assign a privilege escalation vulnerability (e.g., vulnerable sudo version). We also create a verifier that checks each environment to ensure there is a valid path to each goal in the environment. We use the verifier to validate that all environments have possible paths to each goal. 

16. We acknowledge that there could be alternative ways to achieve a state that do not contain these keywords. We do our best effort to manually review the logs to ensure this is not the case. 

TABLE 4. OVERVIEW OF ENVIRONMENTS IN MHBENCH 

|_Environment_|_Description_|Goal|Hosts|
|---|---|---|---|
|Equifax-<br>inspired|A replica of Equifax network (same topology, services, and vulnerabilities) based on public<br>report of the breach [43].|Exfltrate data from 48<br>databases.|50|
|Enterprise A|A tree topology, sometimes used in enterprise networks [3], [2], with three networks. One<br>network has webservers, another has employee hosts, and the last has databases.|Exfltrate data from 10<br>databases.|30|
|Enterprise B|A similar topology as Enterprise A but has four networks. One network has webservers,<br>two networks have employee hosts and the last network has databases.|Exfltrate data from 9<br>databases.|40|
|Enterprise C|An environment inspired by the Colonial Pipeline breach [33] and other ICS attacks [38],<br>[65]. The environment models three IT networks. One of the networks manages critical<br>actuators with a management host.|Gain access to 15<br>critical actuators.|45|
|4-Layer chain|Each host has credentials to another host in the network [36], [69]. Each host has critical<br>data.|Exfltrate data from 25<br>databases.|25|
|6-Layer chain|Same topology and goal as 4-layer chain, but the data on each host requires privileged<br>access. Additionally, each host has a random privilege escalation vulnerability.|Exfltrate data from 25<br>databases.|25|
|4-Layer star|A single network where all hosts have a variety of remote code execution vulnerabilities.<br>Each host has critical data. [18].|Exfltrate data from 25<br>databases.|25|
|6-Layer star|Same topology and goal as 4-layer star, but the data on each host requires privileged<br>access. Each host has a random privilege escalation vulnerability.|Exfltrate data from 25<br>databases.|25|
|Dumbbell A|The topology contains two networks, one with external webservers and another with<br>databases [40]. Each web server has credentials to a unique database.|Exfltrate data from 15<br>databases.|30|
|Dumbbell B|Has the same topology as Dumbbell A. Each web server’s credentials and the data on each<br>database requires privileged access.|Exfltrate data from 15<br>databases.|30|



In Table 4, we detail how we manually created 10 environments based on real attacks and network topologies. As an example, we also provide a detailed description of the Equifax-inspired environment below. Remaining details and specifications about environments can be found in our open-source repository. 

_Equifax-inspired environment._ The Equifax-inspired environment has two web servers running a vulnerable version of Apache Struts with CVE-2017-5638, the same as the real environment [43]. During the Equifax breach, the attacker discovered a plaintext file on one of the web servers that included credentials to 48 different database hosts on a separate network [43].<sup>17</sup> 

To replicate the databases in our environment, we create a second network with 48 database hosts and add files with fake critical consumer data such as emails, social security numbers, and addresses. On a random web server, we add a plain-text SSH configuration file that contains credentials to all the databases. 

## **Appendix C. Token usage** 

We break down the token usage of Incalmo in Table 3. Incalmo used between 3.5K-5897.1K input tokens and 0.2K-60.1K output tokens for the planning LLMs. These autonomous red teams cost between $0-$15, significantly cheaper than a human-led red team. 

17. From public information, it is unclear how many additional nondatabase credentials were in the file, but we assume that the credential file only contained database credentials. 

