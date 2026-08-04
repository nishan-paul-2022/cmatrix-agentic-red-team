# xOffense: An Autonomous Multi-Agent Framework for Penetration Testing with Domain-Adapted Large Language Models 

Phung Duc Luong a,b, Le Tran Gia Bao a,b, Nguyen Vu Khai Tam a,b, Dong Huu Nguyen Khoa a,b, Nguyen Huu Quyen a,b, Van-Hau Pham a,b, Phan The Duy a,b,∗ 

_aInformation Security Lab, University of Information Technology, Ho Chi Minh City, Vietnam bVietnam National University Ho Chi Minh City, Ho Chi Minh City, Vietnam_ 

## **Abstract** 

Penetration testing plays a critical role in assessing the security of modern information systems; however, existing automated approaches based on machine learning, deep learning, or reinforcement learning remain constrained by simplified action spaces, high computational overhead, and limited reasoning across multi-stage workflows such as reconnaissance, vulnerability analysis, and exploitation. Recent large language model (LLM)-based systems have shown promise in addressing these challenges, yet they often rely on large-scale or proprietary models, resulting in high cost, limited scalability, and suboptimal adaptability in complex environments. This paper introduces xOffense, an AI-driven multi-agent framework for autonomous penetration testing that transforms traditional expert-driven processes into fully automated and scalable workflows. The proposed system leverages a fine-tuned mid-scale open-source LLM to perform structured reasoning and decision-making, while decomposing the pentesting pipeline into specialized agents responsible for reconnaissance, vulnerability scanning, and exploitation. An orchestration mechanism coordinates inter-agent collaboration to ensure coherent multi-phase execution. In addition, domain-specific fine-tuning with chainof-thought penetration testing data enables accurate command generation and consistent multi-step reasoning across tasks. The effectiveness of xOffense is validated on two representative benchmarks, AutoPenBench and AI-Pentest-Benchmark. Experimental results demonstrate that the proposed framework consistently outperforms existing LLM-based approaches, achieving a sub-task completion rate of 79.17% and surpassing state-of-the-art systems in both effectiveness and reliability. These results highlight that integrating domain-adapted mid-scale LLMs within a structured multi-agent architecture can provide a cost-efficient, scalable, and reproducible solution for autonomous penetration testing, offering a practical direction for deploying intelligent cybersecurity systems in real-world settings. 

_Keywords:_ Autonomous penetration testing, Large language models, Multi-agent systems, Intelligent decision-making, Cybersecurity automation, Domain-adapted learning 

## **1. Introduction** 

Pentest remains one of the most effective ways to assess the real-world security posture of modern information systems. Unfortunately, the prevailing approach manual testing conducted by small teams of human experts cannot keep pace with today’s rapidly expanding attack surface. In 2024 alone, the National Vulnerability Database listed more than 29,000 new CVEs, a 38% year-over-year increase [1] [2]. As networks grow in scale and complexity, the gap between the appearance of new vulnerabilities and the ability of security professionals to detect and remediate them is widening. This growing imbalance underscores the urgent necessity for automated and intelligent pentest solutions. 

∗Corresponding author 

_Email addresses:_ `21522312@gm.uit.edu.vn` (Phung Duc Luong ), `22520105@gm.uit.edu.vn` (Le Tran Gia Bao ), `22521293@gm.uit.edu.vn` (Nguyen Vu Khai Tam ), `23520734@gm.uit.edu.vn` (Dong Huu Nguyen Khoa ), `quyennh@uit.edu.vn` (Nguyen Huu Quyen ), `haupv@uit.edu.vn` (Van-Hau Pham ), `duypt@uit.edu.vn` (Phan The Duy ) 

Early attempts to narrow this gap focused on fully _deterministic_ or _heuristic_ automation. Notable examples include DeepExploit [3], and Metasploit-based scripting frameworks [4] that chain banner grabbing, version mapping, and exploit invocation. Despite their efficiency, these systems rely on rigid expert rules and struggle with unseen configurations or incomplete information. 

A second, more adaptive line of work leverages _RL_ . Systems like IAPTS [5] and HA-DRL [6] model pentest as a sequential decision-making problem in partially observable environments, enabling agents to autonomously explore and learn effective attack strategies through interaction and reward-based learning. RL agents can, in principle, discover novel attack paths, yet in practice they face two key obstacles: (i) their action space must be heavily simplified such as “scan port”, “exploit CVE-xxx”, and (ii) training requires a large number of environment interactions that are expensive to obtain and seldom transfer between real networks. Consequently, even state-of-the-art RL-based pentesters achieve modest coverage and require significant engineering to integrate new tools or protocols. 

These limitations illustrate that purely DL or RL-based au- 

_April 28, 2026_ 

_Preprint submitted to Elsevier_ 

tomation is insufficient for the inherently multi-phase and dynamic nature of pentest. To overcome this, recent works have turned toward AI agent-based paradigms, in which multiple specialized agents collaborate to emulate the workflow of human red teams. In such systems, each agent assumes a distinct role: a _Reconnaissance Agent_ focuses on host and service discovery, a _Vulnerability Analysis Agent_ correlates findings with CVE and CWE knowledge bases, and an _Exploitation Agent_ generates and tests candidate payloads. This agentoriented decomposition enables modularity, context retention across phases, and the possibility of scaling to complex attack paths that traditional ML/DL/RL pipelines cannot handle. 

Recent advancements in LLMs have opened new possibilities for automating modern pentest. Leveraging their strong reasoning and code generation capabilities, LLMs have been adopted in several research prototypes such as PentestGPT [7], PentestAgent [8], and VulnBot [9], where models assist or autonomously conduct reconnaissance, scanning, and exploitation. In particular, VulnBot represents a major step forward: it frames pentest as a collaborative workflow between specialized LLM agents guided by a Penetration Task Graph (PTG), enabling the simulation of expert-level pentesting with limited or no human intervention. Empirical results from benchmarks like AutoPenBench [10] and AI-Pentest-Benchmark [11] have validated VulnBot’s capacity to outperform other automated methods in structured testing environments. 

However, most of these systems rely heavily on extremely large or commercial LLMs, such as GPT-4o, LLaMA3-70B, or DeepSeek-V3. Despite their capabilities, these models present significant operational hurdles including high resource consumption, costly API dependencies, and limited adaptability to domainspecific fine-tuning. Additionally, their general-purpose nature often leads to hallucinations, loss of context across phases, or poor command translation in complex penetration workflows. As such, there is a pressing need to explore whether smaller, fine-tuned open-source models can serve as more efficient, specialized alternatives, which offers better controllability, lower cost, and targeted reasoning. 

This work is motivated by two core observations. First, while large LLMs have demonstrated strong potential in security domains, scale alone does not guarantee effectiveness, particularly when models are deployed in structured, multi-step tasks like pentest. Despite their size, large-scale LLMs still suffer from context loss across phases, generate incorrect tool usage, and require significant human supervision. Second, most current systems adopt LLMs as black-box assistants or instruction followers, without integrating deeper task-specific guidance or domain adaptation. To address these limitations, we explore an alternative paradigm: leveraging a mid-sized, domainadapted LLM that is explicitly trained for pentest tasks. We present xOffense, a refined evolution of the VulnBot framework that substitutes its dependence on large, general-purpose models with a fine-tuned Qwen3-32B [12], a 32-billion-parameter open-source language model. Through dedicated training on pentest workflows, including vulnerability scanning, exploit crafting, and security tool interaction, xOffense achieves sharper task alignment, enhanced operational fidelity, and greater adapt- 

ability in nuanced or low-visibility environments. 

Beyond simply replacing the core language model, xOffense also incorporates a context-aware prompting scheme we refer to as grey-box prompting. In this setup, agents are equipped with partial system insights, such as protocol hints, observed services, or prior scan summaries, enabling them to make more informed decisions without relying on full system disclosure. This strategy preserves the operational constraints of black-box testing while offering minimal structured guidance, striking a balance between realism and agent effectiveness. By preserving VulnBot’s three-phase pipeline reconnaissance, scanning, and exploitation xOffense ensures compatibility with existing workflows, facilitates direct benchmarking, and provides a robust foundation for comparative evaluation. 

In this paper, we present the design, implementation, and evaluation of xOffense, a lightweight, domain-adaptive, and highly effective autonomous pentest system. Our key contributions are as follows: 

- **An AI-driven multi-agent pentest system.** We propose a novel agent-based framework in which specialized agents collaborate to cover all critical phases of pentest reconnaissance, vulnerability analysis, and exploitation. This design emulates the workflow of human red teams, ensures modularity across tasks, and enables coherent orchestration of complex attack paths in an autonomous manner. 

- **A domain-adapted mid-scale LLM.** At the core of our system lies Qwen3-32B, a 32B-parameter open-source model fine-tuned with Chain-of-Thought (CoT) pentest data. This adaptation empowers the model with precise multi-phase reasoning, accurate tool command generation, and strong adaptability in complex exploitation workflows. 

- **Grey-box phase prompting.** We introduce a contextaware prompting mechanism that selectively integrates environmental cues such as observed protocols, discovered services, and prior scan outputs into the agent reasoning process. This strategy strikes a balance between black-box and white-box testing, reducing context loss and improving continuity across phases. 

- **Extensive empirical validation.** We conduct rigorous evaluations of xOffense on AutoPenBench and AI-PentestBenchmark, demonstrating state-of-the-art performance in both synthetic and real-world pentest scenarios. The system achieves superior task and sub-task completion rates compared to prior methods, confirming the effectiveness of multi-agent orchestration and domain-adapted LLMs. 

The remainder of this paper is organized as follows. Section 2 reviews prior studies on pentest and automation approaches, while Section 3 introduces the fundamental concepts that underpin automated systems. Section 4 describes the architecture of the proposed xOffense framework, including its fine-tuned 

2 

Qwen3-32B model, grey-box prompting strategy, and multiagent orchestration. We describe the experimental settings and benchmark datasets, evaluation metrics in Section 5. In Section 6 empirical results on two benchmarks and real-world exploitation scenarios are reported and analyzed. Section 7 discusses potential threats to validity and their implications for generalizability. In Section 8, we discuss ethical considerations and responsible use of the proposed framework, including potential misuse risks, deployment constraints, and implications for defensive cybersecurity research. Finally, Section 9 concludes the paper and outlines directions for future research. 

## **2. Related work** 

## _2.1. Pre-LLM automation and RL_ 

Deterministic orchestrators, such as DeepExploit, integrate scanners and exploit frameworks, including Metasploit, Nmap, Nikto, and WPScan, but rely on rigid rules and shallow evidence fusion, limiting adaptability to dynamic attack scenarios [3, 4, 13, 14, 15]. RL-based agents formulate pentesting as a Partially Observable Markov Decision Process (POMDP) with reward shaping, providing a principled approach to automating attack strategies [5, 6, 16]. Notably, the Raiju framework has made significant strides in automating post-exploitation tasks by leveraging RL algorithms, specifically Advantage Actor-Critic (A2C) and Proximal Policy Optimization (PPO) [17]. Integrated with Metasploit, Raiju trains specialized agents to perform tasks such as privilege escalation, hashdump gathering, and lateral movement in real-world environments, achieving a success rate exceeding 84% across diverse attack types in four tested environments. However, RL-based approaches, including Raiju, face two primary challenges: (i) the need for extensive state and action space engineering, and (ii) limited crosstarget transferability without costly retraining. These limitations highlight the need for more adaptive methods, such as LLMs, to enhance efficiency and generalization in pentest. 

## _2.2. LLM single-few-agent pipelines_ 

PentestGPT demonstrates a modular, self-interacting scaffold where an LLM plans, parses tool outputs, and synthesizes commands; this closes the perception↔action loop while mitigating context loss via summarization [7]. AutoAttacker focuses on _post-breach_ realism with shell/Metasploit control across Windows/Linux, executing multi-step attacks [18]. Both highlight that language-grounded synthesis and disciplined tool use can automate substantial portions of a Cyber Kill Chain, yet often rely on large backbones and ad-hoc grounding. 

## _2.3. LLM multi-agent orchestration_ 

PentestAgent adopts RAG-grounded, role-based collaboration (reconnaissance, triage, exploitation) to reduce hallucinations and improve next step selection [8]. Additionally, VulnBot 

structures collaboration via a PTG to preserve phase order (recon → scanning → exploitation) and constrain branching; reported results include 30.3% overall and 69.05% sub-task completion on AutoPenBench and strong performance on AI-PentestBenchmark [9, 10, 11]. RefPentester [19] introduces knowledgeinformed self-reflection tied to stage recognition, improving recovery from failed operations on Hack The Box targets. RapidPen targets the _initial foothold_ (IP-to-shell) with a ReAct-style loop and retrieval of exploit knowledge, demonstrating fully autonomous compromises on HTB within minutes at modest cost [20]. The work of Weber et al. [21] presents Perses, a notable effort to enable small language models (SLMs) to perform automated privilege escalation through an extensible, role-specialized multi-LLM architecture. Perses shows that heterogeneity, which assigns lightweight models to Planner, Commander, Summariser and domain-specific Overseers, can substantially improve exploitation of simple misconfigurations. Importantly, the evaluation in Perses is narrowly scoped: experiments are conducted primarily on FreeBSD targets, employ a limited and largely handcrafted set of privilege escalation vulnerabilities, and use a threat model tailored to configuration errors rather than broad end-to-end attacks. As a result, Perses demonstrates the viability of SLM heterogeneity in constrained environments but leaves open questions about transferability to full penetration pipelines (reconnaissance, scanning, multistage exploitation), complex real-world services, and heterogeneous network topologies. 

## _2.4. Focused exploit studies (one-day, zero-day) and CTF-style agents._ 

Fang et al. [22] show that, given CVE descriptions, GPT-4 can exploit 87% of a 15 one-day vulnerability set, whereas other LLMs and scanners achieve 0%; without the description, success drops markedly (7%). Zhu et al. [23] further extend this to teams of agents ( _HPTSA_ ) for _zero-day_ web vulnerabilities, reporting up to 42% pass@5 and 18% pass@1 on 14 real-world cases with GPT-4. For broader skill evaluation, HackSynth proposes a two-module agent and two CTF-based benchmarks (PicoCTF/OverTheWire; 200 tasks) [24], while NYU CTF Bench (NeurIPS D&B) contributes a scalable open-source dataset and automation framework (200 CSAW CTF tasks) [25]. 

## _2.5. Benchmarks and methodology_ 

The emergence of AI-driven pentest has been accompanied by a rapid proliferation of evaluation suites designed to measure autonomy, tool integration, and end-to-end performance under controlled conditions. While the space remains nascent, a few benchmarks have begun to dominate experimental protocols. Notably, _AutoPenBench_ and _AI-Pentest-Benchmark_ appear most frequently in recent studies, reflecting their alignment with realistic, multi-phase pentesting workflows and their ability to grade performance across autonomy levels and subtasks. Conversely, more specialized testbeds such as _CVE-Bench_ target specific exploitability dimensions, such as real-world CVEs in web contexts, and thus see adoption in works focusing on vulnerability exploitation rather than full-cycle orchestration. 

3 

Capture The Flag resources such as _NYU CTF Bench_ and the datasets introduced by _HackSynth_ have also gained traction, particularly for skill-granular or task-decomposed evaluations, though their scenarios often differ from operational pentests in scope and realism. 

Within this landscape, AutoPenBench offers open and standardized graded tasks spanning web, network, and cryptographic targets, with configurable autonomy modes to support comparisons between orchestration strategies and model backbones [10]. AI-Pentest-Benchmark provides VM-based targets, enabling reproducible end-to-end penetration tests [11], thereby supporting performance attribution across discovery, exploitation, and post-exploitation phases. CVE-Bench grounds evaluation in real-world web CVEs, reporting typical success rates in the low teens even for state-of-the-art agents, highlighting the gap between research prototypes and robust autonomy [26]. Methodological recommendations across these works increasingly emphasize standardizing budget constraints, clearly labeling autonomy levels, and reporting detailed error modes to prevent overestimation of capabilities [27]. 

## _2.6. Positioning of our work_ 

Relative to single-agent _PentestGPT_ [7] and post-breach _AutoAttacker_ [18], we retain a multi-agent/PTG discipline akin to _PentestAgent_ / _VulnBot_ [8, 9] but differ in three ways: (i) prioritizing mid-scale, open backbones for cost-effective, on-prem deployment; (ii) employing _grey-box phase prompting_ to maintain phase continuity while effectively limiting drift; and (iii) aligning evaluation with open substrates (AutoPenBench, AIPentest-Benchmark, and where applicable CVE-Bench) under fixed budgets and sub-task breakdowns [10, 11, 26, 27]. 

## _2.7. Takeaways._ 

Outcomes hinge on (i) _grounding quality_ (RAG/summaries/validators) and (ii) _orchestration discipline_ (roles/PTG/reflection). Single-agent pipelines set baselines; role-structured multiagent systems consistently improve reliability; reflective and IP-to-shell variants further push autonomy at kill-chain ends; one-day/zero-day studies quantify limits of discovery vs. exploitation [22, 23]. Our approach emphasizes cost-effective, reproducible deployment with mid-scale open models, PTG structure, and grey-box prompts under open, reproducible protocols [10, 11, 26, 27]. 

## **3. Background** 

## _3.1. Automated Pentest_ 

Pentest aims to evaluate the security of a target system by simulating adversarial behavior across phases such as reconnaissance, vulnerability enumeration, exploitation, and privilege escalation. Manual execution is effective but limited by human resources and scalability. Automated Pentest (APT) addresses these limitations by orchestrating these phases through intelligent agents and machine learning models. 

Formally, let _T_ denote a target system with configuration space C and attack surface S. An automated pentesting operation can be represented as a pipeline: 


![](images/27-xoffense-an-ai-driven-autonomous-penetration-testing.pdf-0004-10.png)


where _R_ are the reconnaissance results (asset discovery, service mapping), _V_ are detected vulnerabilities, _E_ denotes the exploit simulation results, _P_ represents the privilege escalation attempts and _O_ is the structured output (reports, risk scores, or attack paths). 

Such pipelines resemble MLOps workflows, where data collection, model inference, and result verification are continuously orchestrated. In this analogy, reconnaissance and vulnerability scanning serve as data ingestion, exploitation is model inference, and reporting acts as the ’evaluation’ stage. By automating this operation, APT enables repeatability, scalability, and integration into CI/CD security pipelines. 

## _3.2. Multi-Agent AI Systems_ 

Multi-Agent Systems (MAS) provide a natural architecture for automated pentest by assigning each pentest phase to a specialized agent. For example: 

- Reconnaissance Agent: enumerates hosts, ports, and services (similar to VulnBot’s ’Recon Agent’ [9]). 

- Vulnerability Analysis Agent: correlated scan data with CVE / CWE knowledge bases. 

- Exploitation Agent: generates and tests candidate payloads 

- Reporting Agent: summarizes results, attack graphs, and remediation advice. 

Agents communicate through a task manager or memory module, allowing modularity and fault tolerance. Frameworks like _CAMEL_ [29] show that role-conditioned LLM agents can collaborate effectively on complex objectives. In our system _xO_ ff _ense_ , MAS design ensures that each offensive task is handled by a role-specialized model while maintaining global coordination. 

## _3.3. LLM-based O_ ff _ensive Agents_ 

Within MAS, LLMs provide reasoning, contextual understanding, and code synthesis capabilities that align well with pentest workflows. The central problem is, given an attack context _C_ (system description, logs, CVEs), generate actionable steps or payloads _A_ that maximize the likelihood of successful exploitation: 

## _g_ : _C_ �→ _A_ 

Although proprietary LLMs, such as GPT-4 and Claude, offer strong performance, they introduce limitations in cost, reproducibility, and security control. Therefore, we adopt opensource models such as **Qwen3** , which support local deployment, fine-tuning, and quantization (AWQ/INT4), making them 

4 

Table 1: Comparison of representative automated pentesting systems and benchmarks (grid-lined). Criteria emphasize architecture, scope, grounding, tools, autonomy, and evaluation. 

|**Work**|**Architecture**<br>**(Arch.)**|**Scope**/**Phase**|**Grounding**/<br>**Memory**|**Tool Use**|**Evaluation**<br>**& Highlights**|
|---|---|---|---|---|---|
|PentestGPT [7]|SA|Web+Net (multi-phase)|SUM (module summaries)|Parse scans→cmd synth.|USENIX’24 cases/bench; modularpipeline|
|AutoAttacker [18]|SA (post)|Post-breach, OpSec realism|CTX (in-session)|Shell, Metasploit|Simulated org(Win/Linux); multi-stepattacks|
|PentestAgent [8]|MA|Web focus (ext. assess.)|RAG+MEM|Scanners, PoCs|Bench+HTB; reduced hallucinations via RAG|
|VulnBot [9]|MA+PTG|Full cycle (recon→exp.)|Phase SUM (PTG state)|Nmap, Nikto, Metasploit|AutoPenBench (30.3% overall; 69.05% sub-task), AIPB best-of-six|
|RefPentester [19]|MA+RFL|Stage-aware triage/exp.|Refection+knowledge|Std. toolchain|HTB “Sau”: +16.7% vs GPT-4o baseline|
|Perses [21]|MA (multi-LLM)|Privilege escalation|**HET**(heterogeneous model/task)|Tool-grounded (details inpaper)|FreeBSD systems; small-LLM focus|
|RapidPen [20]|SA|**IP**→**Shell**(initial foothold)|MEM+exploit retrieval|Scan→exploit loop|HTB: autonomous shells in minutes; low cost|
|One-DayAgent [22]|SA|Web (one-dayCVEs)|CVE-guided CTX|Browser, tools|87% (GPT-4, with CVE desc.); 7% w/o desc.|
|HPTSA (Teams) [23]|MA (hier./team)|Web (zero-day)|Planner+experts|Browser, task agents|42%pass@5; 18%pass@1 on 14 real vulns|
|HackSynth [24]|SA (2-mod.)|CTF (200 tasks)|Planner+summarizer|Sandbox tools|PicoCTF/OTW benchmarks; GPT-4o best|
|AutoPentest [28]|MA (LangChain)|Black-box (enum→exp.)|Prompting+MEM|Std. scans/exploits|GPT-4o-basedprototype; open code|
|CVE-Bench [26]|Bench|Real web CVEs|–|–|Upto 13% s-rates for SOTA agents|
|AutoPenBench [10]|Bench|Mixed (Web/Net/CRPT)|–|–|33 tasks; autonomyand milestone scoring|
|NYU CTF Bench [25]|Bench|CTF (CSAW; 200)|–|Tool-integrated|NeurIPS D&B; open dataset+automation|
|**Our work**|MA+PTG|Full cycle (Web+Net)|**GBP**+MEM|Broad scan/exploit|APB, AIPB, (opt.) CVEB; mid-scale open LLM|



**Legend:** SA=Single-agent; MA=Multi-agent; PTG=Penetration Task Graph; RFL=Reflection; SUM=Summaries; RAG=Retrieval-Augmented Generation; MEM=Explicit memory; CTX=In-session context; **HET** =Heterogeneity (multi-LLM model/task selection); GBP=Grey-box phase prompting; APB=AutoPenBench [10]; AIPB=AI-Pentest-Benchmark [11]; CVEB=CVE-Bench [26]. “s-rate” denotes success rate. 

suitable for offensive research environments where sensitive data cannot leave the infrastructure. 

To mitigate risks such as hallucination or unsafe outputs, LLM agents are sandboxed and validated against controlled execution environments before results are accepted. 

## _3.4. Fine-tuning Methods for O_ ff _ensive LLMs_ 

Adapting LLMs to offensive security tasks requires taskspecific specialization beyond general pre-trained knowledge, and several parameter-efficient fine-tuning approaches have been explored, including Prefix-Tuning, Adapter-based methods, LowRank Adaptation (LoRA) and its extension QLoRA. 

Prefix-Tuning or P-Tuning v2 appends task-specific continuous vectors or tokens to the input prompt. Its advantages lie in simplicity and a very low memory footprint, since only the prefix embeddings are optimized. However, this method often struggles to capture deeper structural knowledge, and its effectiveness diminishes when reasoning requires multi-step tool interaction or long-context planning, both of which are essential in pentest. 

Adapter-based methods insert small trainable modules within transformer layers, enabling modular adaptation to new tasks. They provide good task isolation and make it possible to reuse the same backbone across different domains with minimal additional parameters. Nonetheless, these methods introduce extra inference latency due to the added modules, and their limited capacity makes them less effective for embedding highly domain-specific procedural knowledge such as exploit reasoning or vulnerability chaining. 

LoRA and its extension QLoRA decompose weight updates into low-rank matrices, significantly reducing the number of trainable parameters while retaining the expressive power of the base model. LoRA achieves a balance between efficiency and performance: it requires far fewer resources than full finetuning, adds negligible inference overhead, and can effectively embed specialized knowledge without erasing the general reasoning ability of the original model. Conceptually, weight up- 

dates ∆ _W_ lie in a low-rank subspace: 

∆ _W_ = _AB_ , _A_ ∈ R<sup>_d_×</sup><sup>_r_</sup> , _B_ ∈ R<sup>_r_×</sup><sup>_k_</sup> , _r_ ≪ min( _d_ , _k_ ) 

and the effective weight during inference is 


![](images/27-xoffense-an-ai-driven-autonomous-penetration-testing.pdf-0005-13.png)


where α is a scaling factor controlling the magnitude of the adaptation. 

Considering the need to adapt a 32B-parameter model such as Qwen3 under realistic hardware constraints, this work adopts LoRA fine-tuning. This approach makes it possible to embed offensive knowledge, including vulnerability patterns, exploit reasoning, and payload generation, efficiently while preserving the base model’s general-purpose capabilities. Detailed dataset construction and the training procedure are described in Section 4. 

## **4. Methodology** 

## _4.1. Overview of the proposed framework_ 

xOffense is an innovative, lightweight framework for autonomous pentest, engineered to replicate the collaborative dynamics of human security teams while operating within resourceconstrained environments. By harnessing compact LLMs with approximately 32 billion parameters, xOffense eliminates dependency on commercial APIs, enabling deployment on standard hardware. The framework decomposes the intricate process of pentest into three meticulously designed phases reconnaissance, scanning, and exploitation coordinated through a sophisticated multi-agent architecture. Comprising five core components Task Orchestrator, Knowledge Repository, Command Synthesizer, Action Executor, and Information Aggregator. xOffense ensures seamless task progression, robust information management, and precise execution. This section elucidates the system’s architecture, role delineation, task coordination, interagent communication, and execution mechanisms, underscoring its efficacy in addressing cybersecurity challenges with minimal computational overhead. 

5 

The operational workflow of _xO_ ff _ense_ , illustrated in Figure 1, initiates when a user submits a pentest objective, such as “Identify vulnerabilities on IP 192.168.X.X and retrieve rootlevel flags.” This task description serves as the Initial Context, which is passed to the _Task Orchestrator_ for comprehensive plan generation. The orchestrator constructs a Task Coordination Graph (TCG), decomposing the penetration objective into a structured sequence of tasks with clearly defined dependencies. To enhance contextual accuracy, it queries the _Knowledge Repository_ a vector-based database via a Retrieval-Augmented Generation (RAG) mechanism, which is taken from LangchainChatchat [30], retrieving relevant penetration knowledge based on inputs such as the initial task description, the current task’s instruction, or recent task results. 

Each task within the TCG is processed through an iterative and adaptive loop involving Command Synthesis, Execution, Feedback Analysis, and Dynamic Plan Update. The _Command Synthesizer_ , fine-tuned using lightweight LoRA techniques, translates task directives into precise, tool-specific commands, which are executed by the _Action Executor_ utilizing a MemAgentenhanced context management system to handle verbose outputs effectively. Post-execution, task outcomes are evaluated and relayed back to the orchestrator, which marks tasks as completed or triggers reflection and re-planning in case of failures. Upon completing all tasks within a phase, such as _Reconnaissance_ , the _Information Aggregator_ consolidates outputs into concise directives for the subsequent phase, such as _Scanning_ , ensuring contextual coherence and minimizing token overhead. This orchestration-execution-feedback loop is consistently applied across all three phases, with each phase iteratively refining the attack path based on task outcomes and environmental feedback. The overall workflow, including execution and re-planning, is later formalized in Algorithm 1. The workflow terminates upon successfully achieving the defined success criteria, such as privilege escalation or flag retrieval. 

## _4.2. Role Specialization_ 

To navigate the complexity of pentest, xOffense employs a role specialization strategy, mitigating the risk of information overload and ensuring contextual coherence across phases. By assigning agents to distinct roles, the framework optimizes resource utilization and maintains precision in task execution, addressing the challenge of dynamic reasoning across testing stages. 

- **Reconnaissance Phase** : Agents focus on comprehensive intelligence gathering, cataloging network configurations, open ports, and service details. Tools such as _Nmap_ [13] for network scanning, _Dirb_ [31] for directory enumeration, _Gobuster_ [32] for brute-forcing hidden directories, and _Amass_ [33] for subdomain discovery are integrated. For instance, a task might execute `nmap -sV -p- <target-ip>` to map all open ports and services, providing a robust foundation for subsequent phases. 

- **Scanning Phase** : Building on reconnaissance insights, scanning agents identify vulnerabilities and misconfigurations using tools like _Nikto_ [14] for web server analysis, 

- _WPScan_ [15] for WordPress vulnerabilities, _sqlmap_ [34] for SQL injection testing for comprehensive vulnerability scanning. This phase prioritizes exploitable weaknesses to streamline progression. 

- **Exploitation Phase** : Agents exploit identified vulnerabilities to gain unauthorized access or escalate privileges, employing tools such as _Metasploit_ [4] for exploit development, _Hydra_ [35] for credential brute-forcing, _John the Ripper_ [36] for password cracking, and _ExploitDB_ [37] for sourcing exploit scripts. For example, a task might deploy a Metasploit module to exploit a known CVE, followed by privilege escalation via a custom script. 

This structured delineation ensures that each phase leverages prior findings, fostering a cohesive testing process and mitigating the risk of fragmented analyses. 

## _4.3. Task Coordination and Reflection_ 

The TCG and its integrated _Check and Reflection Mechanism_ form the cornerstone of xOffense’s penetration path planning, enabling systematic task execution and adaptive plan refinement. These components address the challenges of limited context windows and inadequate error handling, ensuring robust and dynamic testing workflows. Their operational logic is illustrated in Algorithm 1, Algorithm 2, and Algorithm 3. 

## _4.3.1. Task Coordination Graph_ 

The TCG is a structured acyclic digraph, defined as _G_ = ( _V_ , _E_ ), where _V_ represents individual tasks and _E_ denotes dependencies, ensuring logical and conflict-free execution. Each task node _v_ ∈ _V_ encapsulates attributes such as: 

- Directive: A clear instruction, such as _”enumerate services on port 80 of 192.168.X.X.”_ 

- Operation Type: Specifies whether the task involves automated shell commands, such as `nmap` , or manual intervention. 

- Prerequisites: Lists tasks that must be completed prior to execution, ensuring sequential integrity. 

- Command: The tool-specific instruction generated by the _Command Synthesizer_ . 

- Outcome: The execution result, capturing tool outputs or errors. 

- Completion Status: Indicates whether the task is completed or pending. 

- Success Status: Records whether the task was successful. 

The _Task Orchestrator_ generates the TCG in a JSON, which is compliant format, dynamically updating it based on execution outcomes. For instance, a task designed to perform user 

6 


![](images/27-xoffense-an-ai-driven-autonomous-penetration-testing.pdf-0007-00.png)


Figure 1: The Overall Architecture of the xOffense Framework. 

authentication by initiating an SSH connection attempt, targeting a specific service endpoint associated with remote shell access protocols, on port 22 of 192.168.X.X depends on the successful completion of a preceding port scanning task. Subsequent tasks, such as performing an exhaustive enumeration of writable directories for privilege escalation through misconfigured permissions or publicly writable paths ( `find / -writable 2>/dev/null` ) or listing running processes ( `ps aux` ), are contingent on this authentication. 

Figure 2 illustrates a sample TCG, with a JSON task list on the left detailing directives, dependencies, and commands, and a dependency graph on the right showing task sequences with arrows indicating prerequisites. This formalism provides the structural foundation later used in Algorithm 1 for iterative execution and feedback handling. 

The TCG operates through two sessions: 

- **Planning Session** : The _Task Orchestrator_ constructs an initial action plan tailored to the target system’s characteristics and user requirements. It decomposes the plan into structured task lists, ensuring logical sequencing and dependency alignment. The plan is dynamically refined based on execution feedback, addressing the challenge of maintaining coherent context across phases. 

_Executor_ for execution. It also evaluates execution outcomes, updating the TCG’s completion and success statuses, as shown in Algorithm 1. 

This structured approach ensures systematic progression, mitigating the risk of out-of-sequence execution and enhancing efficiency in resource-constrained environments. 

## _4.3.2. Check and Reflection Mechanism_ 

The generation of erroneous commands and the lack of effective error-handling mechanisms pose significant challenges to LLM-based pentest. xOffense addresses these issues through a _Check and Reflection Mechanism_ integrated into the _Task Orchestrator_ , enabling continuous self-assessment and plan optimization. The full workflow is detailed in Algorithm 1. 

During the _Task Session_ , the _Action Executor_ evaluates task outcomes and updates the _TCG_ with success or failure statuses. The _Planning Session_ then reflects on these outcomes, revising task directives and updating the TCG accordingly. Successful tasks are retained, while failed tasks trigger a reanalysis process, wherein the LLM regenerates commands with corrected parameters or alternative strategies. The updated plan is merged with previously completed tasks to preserve execution continuity, as demonstrated in Algorithm 2 and Algorithm 3. 

- **Task Session** : This session generates detailed instructions for each task, which are passed to the _Command Synthesizer_ for command generation and to the _Action_ 

7 


![](images/27-xoffense-an-ai-driven-autonomous-penetration-testing.pdf-0008-00.png)


Figure 2: **TCG** illustrating task dependencies and execution status. Completed tasks are shown in dark, the current task in orange, and pending tasks in light blue. 

**Algorithm 1** Check and Reflection Procedure 

**Require:** TCG, Knowledge Repository _KR_ 1: **while** not all tasks completed **do** 

2: _t_ ← `NextTask` (TCG) 3: _r_ ← `Execute` (t) 4: **if** `CheckSuccess` ( _r_ ) **then** 5: `MarkCompleted` ( _t_ ) 6: `StoreEmbedding` ( _t_ , _r_ , _KR_ ) 7: **else** 8: _K_ ← `RetrieveSimilar` (t, _KR_ ) 9: _t_<sup>′</sup> ← `RegenerateTask` (t, _K_ ) 10: `MergeTasks` (t’, TCG) 11: **end if** 12: `UpdatePlan` (TCG) 13: **end while** 

The _Knowledge Repository_ supports this mechanism indirectly by assisting the _Task Orchestrator_ during plan updates. It stores embeddings of previously successful tasks and curated pentest knowledge, including exploitation techniques, privilege escalation methods, and tool usage tutorials from sources such as HackTricks [38] and HackingArticles [39]. When re-planning, the _Task Orchestrator_ queries this repository to retrieve the top- _k_ most relevant past cases using vector similarity search. Retrieved results are re-ranked and integrated into the revised TCG, ensuring that updates benefit from prior successes. This integration enhances resilience against hallucinated commands, improves error recovery, and maintains efficiency across iterative pentest phases. 

**Algorithm 3** `MergeTasks` : Success-Preserving Integration 

**Require:** Old plan _P_ old, new plan _P_ new 

1: C ← completed-success tasks from _P_ old 

**Algorithm 2** `UpdatePlan` : LLM-driven Plan Revision 

**Require:** Current plan _P_ , failed task _t_ , result _r_ 1: _S_ ← list of completed-success tasks from _P_ 2: _F_ ← list of failed tasks from _P_ 3: _P_ new ← LLMUpdatePlan( _t_ , _r_ , _S_ , _F_ ) 4: _P_<sup>⋆</sup> ← `MergeTasks` ( _P_ , _P_ new) 5: **return** _P_<sup>⋆</sup> 

_Plan Update and Merge Algorithms.._ The `UpdatePlan` and `MergeTasks` procedures are key to preserving execution continuity. Upon task failure, the system calls the LLM to propose an updated plan, then merges it with the existing TCG such that all successfully completed tasks are retained, sequence numbers are adjusted, and only pending or failed tasks are revised. Their formal pseudocode is shown in Algorithm 2 and Algorithm 3. 

- 2: M ← empty list 

- 3: **for all** τ ∈C **do** 4: **if** τ not in _P_ new by instruction **then** 5: append τ to M with reset dependencies 6: **end if** 7: **end for** 8: **for all** τˆ ∈ _P_ new **do** 9: **if** instruction matches a task in C **then** 

- 10: reuse completed task with updated dependencies 11: **else** 12: append τˆ as a new task 13: **end if** 14: **end for** 

- 15: update sequence numbers in M 

16: **return** merged plan with tasks M 

8 

**Algorithm 4** Inter-Agent Communication via PlannerSummary 

|1:|**Input:** Phase sequence_P_={_p_1,_p_2, . . . ,_pn_}, Shell State Log_S_|
|---|---|
|2:|**for**_i_=1 to_n_−1**do**|
|3:|// **Step 1: Collect and summarize results from previous**|
||**phase**|
|4:|`history`<br>`ids`←`GetPlannerIDs`(_pi_)|
|5:|**if** |`history`<br>`ids`|=0**then**|
|6:|_context_←””|
|7:|**else**|
|8:|_summary_←`"Previous Phase:`\`n"`|
|9:|**for**each_id_in`history`<br>`ids`**do**|
|10:|_plan_←`get`<br>~~`p`~~`lanner`<br>~~`b`~~`y`<br>~~`i`~~`d`(_id_)|
|11:|**for**each_task_in _plan_.`finished`<br>`tasks`**do**|
|12:|_summary_ ←_summary_<br>`|| "Instruction:`<br>`"`|
||+_task_.`instruction`<br><br><br>|
||+<br>`|| "Code:`<br>`"`+_task_.`code`|
||+<br>`|| "Result:`<br>`"`+_task_.`result`|
||+ `"`\`n` \`n"`|
|13:|**end for**|
|14:|**end for**|
|15:|_context_,<br>←<br>`callLLM`(`query`<br>=<br>`write`<br>~~`s`~~`ummary` +|
||_summary_, `summary`=`False`)<br>|
|16:|**end if**|
|17:|//**Step 2: Send summarized context to next phase planner**|
|18:<br>19:|`InitPlanner`(_pi_+1,`context`=_context_,`state`=_S_)<br> **end for**|



## _4.4. Inter-Agent Communication Mechanism_ 

Seamless coordination among agents is critical for maintaining contextual coherence across the reconnaissance, scanning, and exploitation phases, particularly given the limited context window of compact LLMs. xOffense employs the _Information Aggregator_ to facilitate efficient communication, consolidating verbose outputs into concise, actionable summaries to optimize token usage and prevent information overload. The entire communication pipeline is operationalized in Algorithm 4. 

For example, reconnaissance outputs, such as open ports (such as 22, 80, and 443), service versions, and system fingerprints, are synthesized into a compact directive for the scanning phase, enabling targeted vulnerability detection with tools like _Nikto_ or _sqlmap_ . Similarly, scanning outputs, such as a SQL injection vulnerability identified by _sqlmap_ or a misconfiguration detected by _Nuclei_ , are summarized to guide the exploitation phase in prioritizing relevant exploits. 

The _Information Aggregator_ maintains a persistent shell state log, tracking access levels, such as a low-privileged user account gained via SSH, and system context, such as operating system type. This log ensures continuity across phases, mitigating the risk of context loss and enabling dynamic integration of findings. By filtering outputs from preceding phases to focus on critical insights, the mechanism minimizes computational overhead, ensuring efficient operation on a 32B-parameter LLM. This streamlined communication fosters a cohesive testing process, addressing the challenge of synthesizing information across multiple stages. 

## _4.5. Generative Behavior and Execution_ 

xOffense supports three operational modes, specifically automatic, semi-automatic, and manual, with the automatic mode 

enabling fully autonomous testing. The _Command Synthesizer_ transforms TCG directives into precise, tool-specific instructions tailored to the target system and phase, addressing the challenge of accurate command generation. 

`-` For instance, a reconnaissance directive might yield `nmap sS -p 22,80,443 <target-ip>` for stealth scanning, while a scanning task might produce `sqlmap -u http://<target -ip>/login --batch` to test for SQL injection vulnerabilities or `nikto -h http://<target-ip>` for web server analysis. In the exploitation phase, commands like `use exploit/ windows/smb/ms17_010_eternalblue` in _Metasploit_ . 

The _Action Executor_ runs these commands via a Python _Paramiko_ -based interactive shell on a Kali Linux environment, simulating human interactions with high fidelity. This component seamlessly processes tool-specific instructions generated by the _Command Synthesizer_ , enabling robust interaction with the target system through simulated keyboard operations. The _Action Executor_ is optimized for the **Qwen3-32B** model, which, despite its constrained 16,384-token context window, integrates the innovative _MemAgent_ [40] framework to handle extended contexts effectively. Drawing on MemAgent’s segment-based processing and reinforcement learning (RL)optimized memory mechanism, as described in the referenced study, the Action Executor processes arbitrarily long outputs by iteratively reading command results in chunks and updating a fixed-length memory. This approach ensures linear computational complexity, allowing xOffense to manage verbose tool outputs without performance degradation, even beyond the Qwen3-32B’s native context limit. To address the challenge of excessive or redundant output, a sophisticated filtering mechanism employs the MemAgent-enhanced LLM to extract critical information when results exceed 8,000 characters, preserving only actionable insights for analysis. These insights are relayed to the _Task Orchestrator_ for further processing, ensuring contextual coherence and minimizing computational overhead. By incorporating MemAgent’s ability to selectively retain relevant data while discarding distractors, the _Action Executor_ enhances the system’s efficiency and scalability, enabling robust pentest in resource-constrained environments and contributing to xOffense’s capability to handle complex, long-context workflows with precision. 

## **5. Implementation, Benchmark Dataset and Metrics** 

To thoroughly assess the effectiveness and practicality of _xO_ ff _ense_ , we designed a comprehensive experimental setup that evaluates not only task completion rates but also the scalability, adaptability, and efficiency of the system under realistic pentest conditions. This section details the experimental settings, models, fine-tuning method, benchmark datasets, evaluation metrics and presents an in-depth analysis of the empirical results. 

## _5.1. Experimental Setup_ 

## _5.1.1. Attacker Environment_ 

All pentest experiments are executed from a dedicated attacker machine configured as a VMware virtual workstation 

9 

running Kali Linux 2025 [41]. Kali is chosen for its comprehensive pentest toolkit and compatibility with industry-standard workflows. This virtualized attacker host is provisioned with 8 vCPUs, 16 GB RAM, and 120 GB storage, ensuring stable execution of both offensive tools and the _xO_ ff _ense_ multi-agent framework within a single environment. 

## _5.1.2. Victim Environment_ 

Two types of target environments are deployed corresponding to the benchmark datasets: 

- **AUTOPENBENCH** [10]: Tasks are instantiated as Docker containers, which are hosted on a separate virtual machine to avoid resource contention with the attacker host. This victim VM is configured with 4 vCPUs, 8 GB RAM, and 80 GB storage, and placed in the same NAT network as the attacker machine to ensure direct connectivity. 

- **AI-Pentest-Benchmark** [11]: Vulnerable machines are directly imported from official VulnHub distributions and executed as VMware virtual machines without modification to their default specifications, in order to preserve the original exploitation conditions. All machines are assigned to the same NAT network as the attacker host to guarantee consistent communication. 

## _5.1.3. Evaluation Protocol_ 

Within the unified environment described in Section 5.1.1, xOffense utilizes a core toolchain with specific versions detailed in Table 2. These industry-standard utilities maintain stable command-line interfaces (CLI) and operational syntaxes, ensuring that the agent’s reasoning logic remains functionally compatible with prior benchmark studies despite minor version iterations. 

Table 2: Operational toolchain and versions (Kali Linux 2025) 

|**Tool**|**Version**|
|---|---|
|Nmap|7.95|
|Nikto|2.5.0|
|WPScan|3.8.28|
|sqlmap|1.9.2#stable|
|Metasploit Framework|6.4.50|
|Hydra|9.5|
|Enum4linux|0.9.1|
|Gobuster|3.8.2|
|Dirb|2.22|



The evaluation itself follows a standardized protocol designed to guarantee fair and reproducible comparisons across all evaluated methods. Each agent is executed under identical constraints, including a maximum interaction budget of 5 steps per task, a timeout of 60 minutes per run, and a fixed token budget per model invocation. All methods are restricted to the same set of tools and environment configurations, without access to external resources beyond those explicitly defined. 

Each experimental scenario is repeated for 5 independent runs with different random seeds to account for stochasticity in 

LLM outputs. Reported results are averaged across runs, and we additionally report standard deviations where applicable. 

The evaluation follows a goal-oriented setting, where an episode is considered successful if the agent achieves the predefined exploitation objective within the allowed budget. Intermediate actions, such as reconnaissance and vulnerability identification, are not independently scored but contribute to overall task completion. 

To prevent potential bias, all models are evaluated on the same subset of benchmark environments, and no task-specific tuning is performed during evaluation. Furthermore, we ensure that training data used for fine-tuning does not overlap with evaluation benchmarks to mitigate data leakage. This protocol is consistently applied to both the proposed framework and all baselines to ensure comparability and reliability of the reported results. 

## _5.2. LLM models_ 

The fine-tuned model, namely Qwen3-32B-finetune is hosted on a dedicated compute node equipped with an NVIDIA A100 GPU having 80 GB VRAM. The same hardware is also used during the fine-tuning process to accelerate training efficiency. For inference, the model is exposed via an API endpoint tunneled through `ngrok` , allowing the attacker machine to interact with the model as an external service. This separation ensured that LLM inference did not compete with pentest tasks for system resources, while also replicating realistic deployment conditions where models are often served remotely. 

## _5.2.1. Evaluated Baseline Models_ 

The experimental evaluation utilizes a broad spectrum of large language models to establish a rigorous comparative baseline. This selection encompasses leading proprietary models such as GPT-4o, alongside high-performance open-source architectures including Llama3.3-70B, Llama3.1-405B, and DeepSeek-V3. For the mid-scale category, Qwen3-32B-base serves as the foundational open-source representative, which is subsequently optimized into Qwen3-32B-finetune for specialized penetration testing tasks. 

Empirical consistency is maintained by enforcing a standardized decoding strategy across all tested models. The inference process is configured with a temperature of 0.5 and a top-p value of 0.9. This specific combination strikes a deliberate balance between the deterministic accuracy required for security tool command synthesis and the generative flexibility necessary for exploring complex attack paths. Furthermore, the topk parameter is set to 40, allowing for a diverse yet controlled vocabulary selection that prevents the model from generating highly improbable tokens. Each model interaction is allocated a maximum budget of 4096 tokens. This extended context window is essential for processing verbose security logs and generating comprehensive multi-stage exploit scripts without the risk of mid-sentence truncation. This universal hyperparameter setup isolates the architectural design and multi-agent orchestration of each framework as the primary variables driving the observed performance results. 

10 

## _5.2.2. Fine-Tuning Methodology_ 

Unlike conventional large-scale model adaptations, which demand significant computational overhead, _xO_ ff _ense_ leverages LoRA to achieve domain specialization. LoRA reduces the parameter footprint by freezing the base model’s weights and training only a compact set of adapter matrices. This approach dramatically lowers the number of trainable parameters by over 99%, enabling efficient fine-tuning even on standard GPU infrastructures. 

To further address the memory bottlenecks of handling a 32B-parameter model, we employ DeepSpeed ZeRO-3 [42] optimization. ZeRO-3 partitions model states, which includes optimizer, gradients, and parameters across multiple GPUs, achieving linear scalability. Additionally, FlashAttention v2 [43] is integrated to optimize attention computation, reducing memory usage and accelerating training by up to 3x compared to standard attention implementations. These combined techniques allow us to efficiently fine-tune Qwen3-32B for pentest workloads with a significant reduction in hardware demands. And the fine-tuning dataset comprised two main corpora as follows: 

- **PentestData** : This dataset is meticulously curated to encompass domain-specific question-answer pairs, each enriched with synthetically generated CoT reasoning traces. The reasoning steps are encapsulated within `<think>` tags, enabling the model to learn structured, step-by-step logical deduction processes tailored for pentest scenarios. To construct PentestData, we aggregate and standardize write-ups from over **1,000 machines** across leading cybersecurity platforms, including TryHackMe [44], HackTheBox [45], and VulnHub [46]. These write-ups are systematically processed to extract task-specific reasoning paths, exploit procedures, and decision-making sequences relevant to offensive security operations. In addition, we incorporate supplementary pentest datasets from HuggingFace Datasets Hub [47], focusing on cybersecurity knowledge bases, pentest techniques, and practical guides for commonly used security tools. This comprehensive integration ensures that PentestData serves as a robust and diverse resource for training models in autonomous pentest workflows. 

- **WhiteRabbitNeo** : A high-quality JSONL-formatted dataset comprising instruction-response pairs, specifically curated for cybersecurity tasks. Although the original dataset lacked explicit CoT reasoning annotations, it is standardized during preprocessing by appending empty `<think>` tags to each sample. This structural unification ensures compatibility with CoT-augmented training pipelines and facilitates subsequent fine-tuning for stepby-step reasoning abilities. The dataset draws from realworld offensive and defensive cybersecurity scenarios, encompassing exploitation techniques, payload crafting, and red-team/blue-team interactions, sourced from the WhiteRabbitNeo community contributions [48]. 

## _5.2.3. Prompt Setting_ 

To ensure methodological transparency and reproducibility, _xO_ ff _ense_ adopts a **single system-wide initialization prompt** ( _init prompt_ ) that governs the full penetration workflow, rather than using distinct prompt policies for individual agents. This unified prompt defines the global objective, operational boundaries, execution environment assumptions, output contracts, and cross-phase memory usage, thereby enforcing consistent reasoning behavior throughout reconnaissance, scanning, and exploitation. 

Concretely, the init prompt specifies four mandatory control dimensions: (i) **mission context** (target objective and scope constraints), (ii) **state continuity** (reuse of prior successful actions and shell status), (iii) **actionability requirements** (toolcompatible and directly executable commands), and (iv) **structured output formatting** . The unified design reduces promptpolicy drift across phases and improves execution stability when the planner performs iterative update and reflection. 

To reduce parsing ambiguity, the init prompt enforces strict output contracts: planning outputs must be serialized within `<json></json>` tags, while executable commands must be enclosed in `<execute></execute>` tags. This explicit interface is essential because downstream modules parse model outputs programmatically. In addition, long execution logs are summarized before being re-injected into context, which mitigates context dilution and helps maintain coherent decision-making over multi-step attack trajectories. 

The prompt follows a grey-box principle: it does not expose implementation internals, but injects selective operational state, including prior successful or failed tasks, shell continuity indicators, and compressed history summaries. This strategy preserves cross-step coherence without overwhelming the model with raw terminal traces. 

For all experiments, prompt execution used a unified inference policy to isolate the effect of architecture and prompting from decoding variance. Specifically, we use temperature = 0.5, top- _p_ = 0.9, top- _k_ = 40, and a maximum generation budget of 4096 tokens per interaction, consistent across compared models. In the deployed _xO_ ff _ense_ implementation, hidden chain-of-thought traces (when produced inside `<think>` tags) are removed before downstream processing, ensuring evaluation is based only on actionable outputs while retaining stable external behavior. 

For reproducibility, a representative structured output schema governed by the init prompt is shown below: 

Listing 1: Representative structured planning output used in xOffense prompts. 

```
<json >
[
```

```
{
```

- `"id": "1",` 

- `" dependent_task_ids ": [],` 

- `"instruction ": "Enumerate open services on 10.10.10.5 with version detection .",` 

- `"action ": "Shell"` 

```
},
```

11 

```
{
```

```
"id":"2",
" dependent_task_ids ":["1"] ,
"instruction ":"AssessHTTP
serviceon10.10.10.5:80for
commonwebvulnerabilities
.",
"action ":"Web"
}
]
</json >
```

## _5.3. Benchmark Datasets_ 

To ensure a rigorous and practically relevant evaluation, we selected two complementary benchmarks that cover both synthetic vulnerabilities and realistic multi-stage exploitation scenarios. Together, these benchmarks provide a balanced testbed for assessing the adaptability and robustness of automated pentest systems. 

_AutoPenBench._ This benchmark defines a total of 33 pentest tasks, spanning both instructional “in-vitro” exercises and real-world CVEs. The in-vitro set (22 tasks) reflects fundamental vulnerability classes frequently highlighted in industry rankings such as the OWASP Top 10, including weak access control (such as misconfigured sudo, world-writable shadow files), web application flaws (such as path traversal, SQL injection, file upload RCE), and insecure network configurations (such as SNMP misconfiguration, ARP spoofing). In addition, four cryptography tasks evaluate resilience against improper or weak cryptographic implementations, such as bruteforcing Diffie–Hellman keys. Beyond these educational tasks, the benchmark incorporates 11 real-world CVEs ranging from 2014 to 2024 with CVSS scores between 7.5 and 10.0. These include critical vulnerabilities widely recognized for their impact and prevalence, such as Log4Shell (CVE-2021-44228), Heartbleed (CVE-2014-0160), SambaCry (CVE-2017-7494), and Spring4Shell (CVE-2022-22965). By combining foundational categories with critical CVEs, AutoPenBench provides a structured yet realistic environment to evaluate whether agents can transition from basic exploitation to handling high-severity vulnerabilities that have historically dominated real-world attack campaigns. 

_AI-Pentest-Benchmark.._ While AutoPenBench focuses on containerized vulnerabilities, the AI-Pentest-Benchmark evaluates AI agents on complete end-to-end exploitation workflows across 13 real-world vulnerable machines drawn from VulnHub. These machines are categorized by difficulty into easy (such as Victim1, Library2, Funbox, WestWild), medium (such as Cengbox2, Devguru, Symfonos2), and hard (such as Insanity, TempusFugit). Each machine defines a structured set of reconnaissance, exploitation, privilege escalation, and general technique subtasks, amounting to 152 tasks in total. The vulnerabilities embedded within these machines reflect common pentest scenarios, including web application 

flaws (SQL injection, XSS, CSRF/SSRF), network service weaknesses (FTP/AD enumeration, brute-force authentication), code-level issues (deserialization, command injection), and post-exploitation techniques (cronjob analysis, misconfigured system files, privilege escalation via user access exploitation). Notably, many of these tasks map directly to recurring weakness categories in the CWE Top 25 and OWASP Top 10, ensuring that success on this benchmark corresponds to capabilities relevant in practical offensive security operations. The benchmark is particularly challenging because the ultimate goal is to achieve root access on each machine, requiring coherent reasoning across reconnaissance, exploitation, and privilege escalation stages. Previous studies have shown that even largescale proprietary models such as GPT-4o and Llama3.1-405B are unable to achieve root-level compromise without human assistance, underscoring the difficulty and realism of this benchmark. 

## _5.4. Evaluation Metrics_ 

To evaluate the performance of _xO_ ff _ense_ , we employ three complementary metrics that capture both high-level task success and fine-grained sub-task robustness. 

## _5.4.1. Overall Task Completion Rate_ 

This metric measures the percentage of target machines successfully compromised like the obtained flag within the allowed interaction budget. Formally: 


![](images/27-xoffense-an-ai-driven-autonomous-penetration-testing.pdf-0012-11.png)


This provides a coarse-grained view of whether an agent can achieve end-to-end exploitation across categories such as Access Control (AC), Web Security (WS), Network Security (NS), Cryptography (CRPT), and Real-world tasks. 

## _5.4.2. Sub-task Completion Rate (1 Experiment)_ 

To gain insight into intermediate stages of pentest, we evaluate sub-task success rates, including service enumeration and vulnerability detection. Each benchmark defines a set of subtasks _S_ . A sub-task is considered successful if it is completed in at least one of the five independent runs: 


![](images/27-xoffense-an-ai-driven-autonomous-penetration-testing.pdf-0012-15.png)


This metric highlights the agent’s ability to eventually solve a sub-task, even if not consistently across all runs. 

## _5.4.3. Sub-task Completion Rate (5 Experiments)_ 

To measure robustness and consistency, we also compute the cumulative completion rate across all five runs. In this case, we count the total number of successful sub-tasks over all experiments and normalize by the maximum possible number of successes: 


![](images/27-xoffense-an-ai-driven-autonomous-penetration-testing.pdf-0012-19.png)


12 

This stricter metric rewards agents that not only succeed once but can repeatedly complete subtasks across independent executions. 

Together, these three metrics provide a balanced view: (i) overall penetration capability, (ii) eventual solvability of subtasks, and (iii) robustness of performance under repeated trials. 

## **6. Evaluation and results** 

## _6.1. Experiment Scenarios_ 

We design five experimental scenarios to comprehensively evaluate _xO_ ff _ense_ across synthetic and real-world settings: 

- **Scenario 1:** Overall task completion on AutoPenBench, measuring full machine compromise across AC, WS, NS, and CRPT categories. 

- **Scenario 2:** Sub-task completion on AutoPenBench (1 Experiment), where a sub-task is successful if solved in at least one of five runs. 

- **Scenario 3:** Sub-task completion on AutoPenBench (5 Experiments), aggregating successful subtasks across all five runs to capture consistency. 

- **Scenario 4:** Real-world exploitation on AI-PentestBenchmark without RAG, using six representative VulnHub machines. 

- **Scenario 5:** Real-world exploitation on AI-PentestBenchmark with RAG, highlighting the contribution of retrieval to complex exploitation chains. 

## _6.2. Task Completion Performance Across pentest Categories_ 

## _6.2.1. Overall Task Completion Performance_ 

Table 3 presents the overall task completion rates across all evaluated models on the AutoPenBench dataset. The fine-tuned **Qwen3-32B-finetune** model achieved a remarkable **72.72%** completion rate, substantially outperforming both its base variant, **Qwen3-32B-base** (30.30%), and other state-ofthe-art models, including GPT-4o (21.21%), Llama3.1-405B (Paper) (30.30%), and PentestGPT (9.09%). 

The performance disparity between **Qwen3-32B-finetune** and its base version is particularly noteworthy. Despite having identical model architecture and parameter size (32 billion parameters), the domain-specific fine-tuning enabled a **2.4x improvement** in task completion. This validates the effectiveness of our lightweight LoRA fine-tuning pipeline in adapting general-purpose models to specialized pentest workflows. 

In the **AC** category, **Qwen3-32B-finetune** achieved a **100% success rate** , a stark contrast to the 40.00% of Qwen3-32Bbase and the 60.00% of Llama3.1-405B (Paper). Similarly, in **NS** , our model achieved **83.33%** completion, surpassing all baselines, including Llama3.3-70B (33.33%) and Qwen332B-base (50.00%). Notably, even in the complex **Realworld** category, **Qwen3-32B-finetune** attained a **54.54%** success rate, outperforming Qwen3-32B-base (27.27%) and PentestGPT (0.00%). 

These findings demonstrate that fine-tuning on domainrelevant CoT data and incorporating robust task orchestration mechanisms can enable a quantized, resource-efficient model to match and even surpass the capabilities of larger, generalpurpose LLMs in specialized scenarios. The consistent outperformance across categories further validates the robustness of our fine-tuning strategy, especially given the compute-efficient AWQ quantization. 

## _6.2.2. Sub-task Completion Performance (1 Experiment)_ 

To assess finer-grained capabilities, we evaluated sub-task completion in a single-run experiment (Table 4). The term ”1 Experiment” refers to the overall sub-task completion rate across five experiments, where a sub-task is considered successful if it succeeds in at least one experiment. **Qwen3-32Bfinetune** achieved a **79.17%** sub-task completion rate, outperforming Llama3.1-405B (Paper) (69.05%) by a margin of **10.12%** . This margin is significant, particularly when considering that Llama3.1-405B is a much larger model (405B parameters) operating in its native configuration. 

In the **Real-world** category, **Qwen3-32B-finetune** achieved a **35.96%** sub-task completion rate, more than doubling that of Qwen3-32B-base (24.92%) and outperforming Llama3.1405B (Paper) (26.19%). Similarly, in the CRPT category, the fine-tuned model demonstrated a **3.41%** improvement over Llama3.1-405B (Paper). 

Interestingly, while Qwen3-32B-base achieved moderate results (52.36%), its performance gap to Qwen3-32B-finetune (79.17%) illustrates the critical role of domain adaptation. The base model, though capable of handling general security tasks, struggled with multi-step reasoning and contextual coherence, particularly in chained exploit scenarios. The finetuned model’s superior performance confirms that its CoTdriven prompt alignment and RAG-assisted knowledge retrieval mechanisms provide a tangible advantage in executing complex task sequences. 

## _6.2.3. Sub-task Completion Performance (5 Experiments)_ 

To evaluate robustness and stability, we conducted aggregated experiments over five runs (Table 5). The term ”5 Experiments” denotes the number of subtasks completed in all five experiments. **Qwen3-32B-finetune** maintained its lead with a **60.94%** sub-task completion rate, significantly outperforming Llama3.1-405B (Paper) (49.90%) and Qwen3-32Bbase (23.03%). This robustness is critical in practical pentesting workflows, where variance due to environmental noise and complex task dependencies often degrades model performance. 

In the **AC** category, **Qwen3-32B-finetune** achieved a remarkable **14.51%** , which is **4.32% higher** than Llama3.1405B (Paper). For **WS** , our model reached **10.91%** , outperforming all baselines by a significant margin. Notably, even in categories where task chains are inherently volatile, such as **Real-world** , the fine-tuned model achieved **21.07%** , compared to 17.71% for Llama3.1-405B (Paper) and only 9.78% for Qwen3-32B-base. 

While a performance drop of approximately **18%** from the single-experiment run to the aggregated runs was observed, this 

13 

Table 3: Overall Task Completion Rate on Target Machines. Our fine-tuned model demonstrates superior performance, especially in AC, NS, and Real-world categories. 

|**Category**|**GPT-4o**|**Llama3.3-70B**<br>**(VulnBot)**|**Llama3.1-405B**<br>**(VulnBot)**|**Llama3.1-405B**<br>**(PentestGPT)**|**Qwen3-32B**<br>**(Base)**|**Qwen3-32B-fnetune**<br>**(Ours)**|
|---|---|---|---|---|---|---|
|AC|1(20.00%)|1(20.00%)|3(60.00%)|1(20.00%)|2(40.00%)|**5(100.00%)**|
|WS|2(28.57%)|1(14.29%)|2(28.57%)|0(0.00%)|2(28.57%)|**5(71.42%)**|
|NS|3(50.00%)|2(33.33%)|2(33.33%)|2(33.33%)|3(50.00%)|**5(83.33%)**|
|CRPT|0(0.00%)|0(0.00%)|0(0.00%)|0(0.00%)|0(0.00%)|**3(75.00%)**|
|Real-world|1(9.09%)|2(18.18%)|3(27.27%)|0(0.00%)|3(27.27%)|**6(54.54%)**|
|**ALL**|7(21.21%)|6(18.18%)|10(30.30%)|3(9.09%)|10(30.30%)|**24(72.72%)**|



Table 4: Sub-task Completion Rate (1 Experiment) . Qwen3-32B-finetune shows the highest completion rate across all categories. 

|**Category**|**Llama3.3-70B**<br>**(VulnBot)**|**Llama3.1-405B**<br>**(VulnBot)**|**Llama3.3-70B**<br>**(Base)**|**Llama3.1-405B**<br>**(Base)**|**Llama3.1-405B**<br>**(PentestGPT)**|**Qwen3-32B**<br>**(Base)**|**Qwen3-32B-fnetune**<br>**(Ours)**|
|---|---|---|---|---|---|---|---|
|AC|25(11.90%)|31(14.76%)|16(7.62%)|21(10.00%)|20(9.52%)|26(8.20%)|**46(14.51%)**|
|WS|24(11.43%)|30(14.29%)|22(10.48%)|26(12.38%)|18(8.57%)|28(8.83%)|**38(11.98%)**|
|NS|12(5.71%)|11(5.24%)|10(4.76%)|9(4.29%)|6(2.86%)|11(3.47%)|**15(4.73%)**|
|CRPT|15(7.14%)|18(8.57%)|17(8.10%)|18(8.57%)|12(5.71%)|22(6.94%)|**38(11.98%)**|
|Real-world|49(23.33%)|55(26.19%)|29(13.81%)|29(13.81%)|28(13.33%)|79(24.92%)|**114(35.96%)**|
|**ALL**|125(59.52%)|145(69.05%)|94(44.76%)|103(49.05%)|84(40.00%)|166(52.36%)|**251(79.17%)**|



Table 5: Sub-task Completion Rate (5 Experiments) . Our model maintains a significant lead, demonstrating robustness and consistency. 

|**Category**|**Llama3.3-70B**<br>**(VulnBot)**|**Llama3.1-405B**<br>**(VulnBot)**|**Llama3.3-70B**<br>**(Base)**|**Llama3.1-405B**<br>**(Base)**|**Llama3.1-405B**<br>**(PentestGPT)**|**Qwen3-32B**<br>**(Base)**|**Qwen3-32B-fnetune**<br>**(Ours)**|
|---|---|---|---|---|---|---|---|
|AC|87(8.29%)|107(10.19%)|46(4.38%)|61(5.81%)|27(2.57%)|60(3.78%)|**212(14.51%)**|
|WS|106(10.10%)|116(11.05%)|83(7.90%)|66(6.29%)|40(3.81%)|70(4.42%)|**173(10.91%)**|
|NS|41(3.90%)|40(3.81%)|36(3.43%)|22(2.10%)|15(1.43%)|10(0.63%)|**71(4.67%)**|
|CRPT|65(6.19%)|75(7.14%)|68(6.48%)|44(4.19%)|43(4.10%)|70(4.42%)|**176(11.10%)**|
|Real-world|166(15.81%)|186(17.71%)|99(9.43%)|67(6.38%)|56(5.33%)|155(9.78%)|**334(21.07%)**|
|**ALL**|465(44.29%)|524(49.90%)|332(31.62%)|260(24.76%)|181(17.24%)|365(23.03%)|**966(60.94%)**|



is expected due to increased task complexity and stochastic failures inherent in autonomous pentesting. Nevertheless, the finetuned model’s consistency across these iterations underscores its robustness, particularly when contrasted with PentestGPT’s 17.24% sub-task completion in the same setting. 

## _6.2.4. Comparative Insights_ 

A critical observation from these experiments is the disproportionate performance leap achieved through fine-tuning relative to model size. Despite being a 32B parameter model, **Qwen3-32B-finetune** consistently outperformed larger counterparts like Llama3.1-405B (405B parameters) across every evaluation metric. This validates our hypothesis that task orchestration, RAG-driven context augmentation, and parameterefficient tuning techniques (LoRA + ZeRO-3 + FlashAttention) can bridge, and in specialized scenarios, exceed the performance gap traditionally associated with sheer model size. 

Furthermore, the disparity between Qwen3-32B-base and Qwen3-32B-finetune exemplifies the inadequacy of using general-purpose LLMs in specialized pentesting workflows without domain adaptation. The base model, though architecturally identical, lacked the reasoning depth and contextcoherence required for intricate attack path planning, resulting in lower task and sub-task completion rates. 

## _6.3. Evaluation on Complex Real-World Exploitation Chains_ 

## _6.3.1. Performance without RAG (No-RAG)_ 

To assess the baseline capabilities of our proposed system _xO_ ff _ense_ in realistic offensive security scenarios, we conducted experiments on the same set of six real-world vulnerable machines as utilized in the VulnBot [9] evaluation: **Victim1** , **Library2** , **Sar** , **WestWild** , **Symfonos2** , and **Funbox** . This machine set, originally derived from the AI-Pentest-Benchmark, covers a diverse range of exploitation challenges, including misconfigurations, weak authentication, remote code execution, privilege escalation, and multi-step attack chains. By adopting this identical set, we ensure methodological consistency and enable a direct, fair comparison with prior work. 

The experiments were conducted in a fully autonomous mode, without any human intervention or RAG support. Each target machine was tested in five independent runs, and the reported performance represents the best sub-task completion rate per machine, following the AI-Pentest-Benchmark scoring methodology. Figure 3 presents the comparative results across multiple models, including **VulnBot-Llama3.1-405B** , **VulnBot-DeepSeek-v3** , their respective base models, and our proposed **Qwen3-32B** variants (base and finetuned). 

The results reveal several noteworthy patterns. First, **Qwen3-32B-finetune** consistently surpasses its base counterpart across all six machines, with particularly significant im- 

14 

provements on _Victim1_ (+0.55), _Library2_ (+0.30), and _WestWild_ (+0.63). These gains highlight the effectiveness of domain-specific fine-tuning in strengthening the model’s exploitation reasoning and procedural robustness. Second, while VulnBot-DeepSeek-v3 remains highly competitive, achieving the highest score on _Victim1_ (0.83) and _WestWild_ (0.71), our fine-tuned Qwen3-32B achieves comparable or superior performance on most other machines, including leading results on _Sar_ (0.58) and _Funbox_ (0.54). 

Notably, performance disparities are strongly correlated with the complexity of exploitation chains. Targets such as _Symfonos2_ and _Funbox_ , which demand multi-stage privilege escalation and exploitation of non-trivial service configurations, clearly benefit from the enhanced contextual reasoning introduced via fine-tuning. This observation underscores the critical role of model specialization in addressing the inherent unpredictability and diversity of real-world pentest environments. In summary, the No-RAG evaluation confirms that **xO** ff **enseQwen3-32B-finetune** can autonomously achieve competitive, and in some cases state-of-the-art, performance in realistic offensive security scenarios, even without external retrieval augmentation. This establishes a robust performance baseline for subsequent RAG-enhanced evaluations. 

## _6.3.2. Performance with RAG (RAG)_ 

When augmenting the evaluation with the Knowledge Repository module, a substantial shift in performance trends emerges across the six real-world exploitation targets _(see Fig. 4)_ . Compared to the baseline (No-RAG), the Qwen3-32BFinetune model demonstrates marked improvement, achieving perfect completion scores on Victim1 and WestWild (1.00) and notable gains on Library2 (+0.20) and Symfonos2 (+0.16). Similarly, moderate increases are observed for Sar and Funbox, reflecting the model’s enhanced capability to navigate multistep attack chains when supported by targeted, contextually relevant prior knowledge. 

The gains are less pronounced for Qwen3-32B-Base, with performance remaining comparatively low on challenging targets such as Symfonos2 (0.13) and WestWild (0.25). This disparity underscores the role of fine-tuning in maximizing the benefits of retrieval augmentation, as without alignment to domain-specific exploitation strategies, the retrieved information alone is insufficient to ensure consistent execution success. When compared against VulnBot baselines, Qwen3-32BFinetune with RAG achieves competitive or superior results in four out of six targets, matching the best baseline performance on Library2 (0.80) and surpassing it on Victim1 and WestWild. This suggests that RAG integration not only mitigates the limitations of the base model but also allows the fine-tuned variant to close the gap, or in certain scenarios, outperform humanassisted frameworks. 

These improvements can be attributed to three key factors: (1) the retriever’s ability to surface high-relevance exploitation procedures from a curated cybersecurity corpus, (2) the fine-tuned model’s capacity to integrate external information into coherent multi-step reasoning, and (3) the reduction 

of hallucination-driven dead ends, which are particularly detrimental in constrained exploitation environments. Collectively, these findings reinforce the notion that RAG is a critical enabler for scalable, high-fidelity automated pentest in complex real-world settings. 

## **7. Threats to Validity** 

## _7.1. Internal validity_ 

The fine-tuning of Qwen3-32B on a CoT-enriched pentest dataset introduces potential internal threats. Certain vulnerability classes and exploitation strategies are disproportionately represented, which may bias the model toward specific attack vectors while limiting its capacity to generalize to underrepresented scenarios. Moreover, the integration of prompting strategies and toolchains may embed implicit task-specific heuristics, raising the possibility that reported improvements partly reflect dataset artifacts rather than genuine reasoning ability. Such factors must be considered when interpreting performance gains on structured benchmarks. 

## _7.2. External validity_ 

The evaluation settings of AutoPenBench and AI-PentestBenchmark, which approximate realistic penetration workflows, yet cannot fully capture the heterogeneity of productionscale environments. Operational networks often exhibit greater variability in topology, non-standard configurations, active defenses, and deception mechanisms that remain absent from current benchmarks. In addition, adversarial tactics evolve over time, whereas benchmarks are necessarily static. Consequently, the generalizability of results to enterprise systems, heterogeneous infrastructures, or zero-day exploitation scenarios should be regarded with caution. 

## _7.3. Construct validity_ 

Task completion rate and exploitation success were employed as primary evaluation metrics. While suitable for quantifying functional effectiveness, these measures neglect other dimensions that are central to pentest practice. Attributes such as stealth, efficiency of resource utilization, time-to-compromise, and resilience against detection are critical to operational realism yet remain unaccounted for in the adopted benchmarks. Furthermore, binary success measures fail to capture partial progress or incremental compromise, potentially obscuring nuances in agent behavior across complex exploitation chains. 

## _7.4. Reliability_ 

The reproducibility of results may be affected by stochastic factors inherent in both large language model inference and auxiliary system tools. Hardware variation, runtime conditions, network latency, and nondeterministic outputs from scanning utilities can yield divergent agent behaviors even under identical inputs. Standardized configurations and repeated trials mitigate these effects but do not eliminate them entirely, implying that replications across platforms or over extended periods may observe non-negligible variance. 

15 


![](images/27-xoffense-an-ai-driven-autonomous-penetration-testing.pdf-0016-00.png)


Figure 3: Comparison of sub-task completion rates across six real-world vulnerable machines in a No-RAG setting. 


![](images/27-xoffense-an-ai-driven-autonomous-penetration-testing.pdf-0016-02.png)


Figure 4: Comparison of sub-task completion rates across six real-world vulnerable machines with RAG setting. 

In sum, although the reported findings provide strong evidence of the capabilities of xOffense, these validity concerns underscore the need for broader empirical validation. Expanding evaluations to encompass more diverse infrastructures, adversarially adaptive defenses, and richer performance metrics would strengthen the robustness, scalability, and practical applicability of autonomous pentest systems. 

## **8. Ethical Considerations and Responsible Use** 

This work addresses autonomous penetration testing, a domain with inherent dual-use implications. While the proposed xOffense framework is intended to support defensive cybersecurity practices, it may also be subject to misuse if deployed without appropriate safeguards. The system is designed strictly for authorized security assessment, research, and training pur- 

16 

poses in controlled environments, such as benchmark platforms and laboratory settings, and must only be used with explicit legal authorization from system owners. It is not intended for unauthorized exploitation of real-world systems. 

Due to its capability to automate multi-stage penetration testing workflows, the framework may lower the barrier for conducting offensive operations, including large-scale vulnerability discovery and exploitation. This highlights the importance of responsible usage and user awareness when interacting with such systems. Users are expected to adhere to applicable legal frameworks, institutional policies, and professional ethical standards when deploying or extending the proposed approach. 

To mitigate potential risks, all experiments in this study are conducted strictly within sandboxed and publicly available benchmark environments, including AutoPenBench and AI-Pentest-Benchmark, without interaction with live production systems or undisclosed vulnerabilities. In practical deployments, additional safeguards are necessary, including restricting execution to authorized and monitored environments, enforcing logging and auditing of system actions, limiting tool usage and external network access, and incorporating human-in-theloop validation for high-impact decisions. Future implementations should further integrate policy-based constraints and access control mechanisms to prevent unintended or malicious usage. 

Beyond its offensive capabilities, this line of research also motivates the development of more robust defensive mechanisms. Understanding how autonomous agents identify and exploit vulnerabilities can inform the design of improved intrusion detection systems, adaptive defenses, and secure system architectures. As such, this work contributes not only to offensive security automation but also to advancing defensive cybersecurity research. 

This research adheres to responsible cybersecurity and AI research practices. The study does not involve zero-day exploitation or unauthorized system access, and all evaluations are conducted on simulated or explicitly permitted targets. Future extensions should follow coordinated disclosure principles and comply with relevant legal and ethical standards, in line with established guidelines for responsible AI and cybersecurity research. 

## **9. Conclusion and Future Work** 

This work presented xOffense, an independent, fully autonomous multi-agent framework for pentest, designed to address persistent limitations in existing systems such as context loss, limited reasoning continuity, and dependence on large proprietary models. By integrating a fine-tuned, midscale open-source LLM (Qwen3-32B) with a novel grey-box phase prompting mechanism and a purpose-built orchestration architecture, xOffense achieves accurate multi-stage decisionmaking and robust tool integration across the entire pentest lifecycle. 

Our evaluation on _AutoPenBench_ and _AI-PentestBenchmark_ demonstrated that xOffense consistently out- 

performs both larger commercial LLMs, such as GPT-4o and LLaMA3-70B, and leading open-source baselines, such as PentestGPT and VulnBot-LLaMA3-405B. The framework attained an overall task completion rate of 72.72% and a sub-task completion rate of up to 79.17%, while successfully exploiting complex real-world targets. These results highlight that a domain-specialized, mid-scale model, when paired with targeted reasoning guidance, can match or exceed the capabilities of state-of-the-art large-scale systems, offering a cost-effective and reproducible solution for autonomous offensive security operations. 

Future work will explore three main directions. First, we aim to optimize the command generation module, potentially through structured function calling, to further improve execution precision. Second, we plan to enhance the robustness of long-running process handling and strengthen the retrieval-augmented generation mechanism with automated updates from vulnerability intelligence sources such as ExploitDB and GitIngest. Third, we intend to extend xOffense’s capabilities to support advanced web and GUI interactions via browser automation, enabling it to tackle a broader range of pentest scenarios. 

## **References** 

- [1] Infosecurity Magazine. Nvd revamps operations amid cve surge. `https://www.infosecurity-magazine.com/news/ nvd-revamps-operations-cve-surge/` , 2024. Accessed: 2025-0730. 

- [2] GBHackers. Nist facing challenges in managing cve backlog. `https://gbhackers.com/ nist-facing-challenges-in-managing-cve-backlog/` , 2024. Accessed: 2025-07-30. 

- [3] Isao Takaesu and Daisuke Chikamori. Deep exploit. `https: //www.blackhat.com/us-18/arsenal/schedule/index.html# deep-exploit-11908` , 2018. Presented at Black Hat USA 2018 Arsenal, Las Vegas. Accessed: 2025-07-30. 

- [4] Rapid7. Metasploit — penetration testing software, pen testing security. `https://www.metasploit.com/` , 2024. Accessed: July 27, 2024. 

- [5] Abdul Samad, Saad Altaf, and M Junaid Arshad. Advancements in automated penetration testing for iot security by leveraging reinforcement learning. _evaluation_ , 8:9, 2024. 

- [6] Khuong Tran, Ashlesha Akella, Maxwell Standen, Junae Kim, David Bowman, Toby Richer, and Chin-Teng Lin. Deep hierarchical reinforcement agents for automated penetration testing. _arXiv preprint arXiv:2109.06449_ , 2021. 

- [7] Gelei Deng, Yi Liu, V´ıctor Mayoral-Vilches, Peng Liu, Yuekang Li, Yuan Xu, Tianwei Zhang, Yang Liu, Martin Pinzger, and Stefan Rass. PentestGPT: Evaluating and harnessing large language models for automated penetration testing. In _33rd USENIX Security Symposium (USENIX Security 24)_ , pages 847–864, Philadelphia, PA, 2024. USENIX Association. 

- [8] Xiangmin Shen, Lingzhi Wang, Zhenyuan Li, Yan Chen, Wencheng Zhao, Dawei Sun, Jiashui Wang, and Wei Ruan. Pentestagent: Incorporating llm agents to automated penetration testing. In _Proceedings of the 20th ACM Asia Conference on Computer and Communications Security_ , pages 375–391, 2025. 

- [9] He Kong, Die Hu, Jingguo Ge, Liangxiong Li, Tong Li, and Bingzhen Wu. VulnBot: Autonomous penetration testing for a multi-agent collaborative framework. _arXiv preprint arXiv:2501.13411_ , Jan 2025. 

- [10] Luca Gioacchini, Marco Mellia, Idilio Drago, Alexander Delsanto, Giuseppe Siracusano, and Roberto Bifulco. Autopenbench: Benchmarking generative agents for penetration testing, 2024. 

- [11] Isamu Isozaki. Ai-pentest-benchmark: A benchmark for automated penetration testing. `https://github.com/isamu-isozaki/` 

17 

`AI-Pentest-Benchmark` , 2024. GitHub repository. Accessed: 202507-30. 

- [12] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. _arXiv preprint arXiv:2505.09388_ , 2025. 

- [13] Gordon Lyon. Nmap: The network mapper - free security scanner. `https://nmap.org/` , 2024. Accessed: July 27, 2024. 

- [14] Chris Sullo. Nikto web server scanner. `https://github.com/sullo/ nikto` , 2024. Accessed: July 27, 2024. 

- [15] WPScan Team. Wpscan wordpress security scanner. `https://github. com/wpscanteam/wpscan` , 2024. Accessed: July 27, 2024. 

- [16] Ryusei Maeda and Mamoru Mimura. Automating post-exploitation with deep reinforcement learning. _Computers_ & _Security_ , 100:102108, 2021. 

- [17] Van-Hau Pham, Hien Do Hoang, Phan Thanh Trung, Van Dinh Quoc, Trong-Nghia To, and Phan The Duy. Raiju: Reinforcement learningguided post-exploitation for automating security assessment of network systems. _Computer Networks_ , 253:110706, 2024. 

- [18] Jiacen Xu, Jack W Stokes, Geoff McDonald, Xuesong Bai, David Marshall, Siyue Wang, Adith Swaminathan, and Zhou Li. AutoAttacker: A large language model guided system to implement automatic cyberattacks. _arXiv preprint arXiv:2403.01038_ , 2024. 

- [19] Hanzheng Dai, Yuanliang Li, Zhibo Zhang, and Jun Yan. Refpentester: A knowledge-informed self-reflective penetration testing framework based on large language models. _arXiv preprint arXiv:2505.07089_ , 2025. 

- [20] Sho Nakatani. Rapidpen: Fully automated ip-to-shell penetration testing with llm-based agents. _arXiv preprint arXiv:2502.16730_ , 2025. 

- [21] Dominik M. Weber, Ioannis Tzachristas, and Aifen Sui. Perses: Unlocking privilege escalation for small llms via extensible heterogeneity. In _Proceedings of the 20th ACM Asia Conference on Computer and Communications Security (ASIA CCS ’25)_ . ACM, 2025. 

- [22] Richard Fang, Rohan Bindu, Akul Gupta, and Daniel Kang. Llm agents can autonomously exploit one-day vulnerabilities. _arXiv preprint arXiv:2404.08144_ , 2024. 

- [23] Yuxuan Zhu, Antony Kellermann, Akul Gupta, Philip Li, Richard Fang, Rohan Bindu, and Daniel Kang. Teams of llm agents can exploit zero-day vulnerabilities. _arXiv preprint arXiv:2406.01637_ , Mar 2025. 

- [24] Lajos Muzsai, David Imolai, and Andr´as Luk´acs. Hacksynth: Llm agent and evaluation framework for autonomous penetration testing. _arXiv preprint arXiv:2412.01778_ , 2024. 

- [25] Minghao Shao, Sofija Jancheska, Meet Udeshi, Brendan Dolan-Gavitt, Haoran Xi, Kimberly Milner, Boyuan Chen, Max Yin, Siddharth Garg, Ramesh Karri, Prashanth Krishnamurthy, Farshad Khorrami, and Muhammad Shafique. Nyu ctf bench: A scalable open-source benchmark dataset for evaluating llms in offensive security. In _NeurIPS 2024 Datasets and Benchmarks Track_ , 2024. 

written in go. `https://github.com/OJ/gobuster` , 2025. 

   - [33] OWASP Amass Project. Owasp amass - in-depth attack surface mapping and asset discovery. `https://github.com/owasp-amass/amass` , 2025. 

   - [34] sqlmap Developers. sqlmap - automatic sql injection and database takeover tool. `https://github.com/sqlmapproject/sqlmap` , 2025. 

   - [35] THC Hydra Team. Thc-hydra - network logon cracker. `https:// github.com/vanhauser-thc/thc-hydra` , 2025. 

   - [36] Openwall Project. John the ripper - password cracker. `https:// github.com/openwall/john` , 2025. 

   - [37] Offensive Security. Exploit database (exploit-db). `https://www. exploit-db.com/` , 2025. 

   - [38] Carlos Polop. Hacktricks: Hacking techniques & privilege escalation encyclopedia. `https://book.hacktricks.xyz/` , 2025. 

   - [39] Raj Chandel and Hacking Articles Team. Hacking articles: A cyber security community blog. `https://www.hackingarticles.in/` , 2025. 

   - [40] Hongli Yu, Tinghong Chen, Jiangtao Feng, Jiangjie Chen, Weinan Dai, Qiying Yu, Ya-Qin Zhang, Wei-Ying Ma, Jingjing Liu, Mingxuan Wang, et al. Memagent: Reshaping long-context llm with multi-conv rl-based memory agent. _arXiv preprint arXiv:2507.02259_ , 2025. 

   - [41] Offensive Security. Kali linux: Penetration testing and ethical hacking linux distribution. `https://www.kali.org/` , 2025. 

   - [42] Samyam Rajbhandari, Jeff Rasley, Olatunji Ruwase, and Yuxiong He. Zero: Memory optimizations toward training trillion parameter models. In _SC20: International Conference for High Performance Computing, Networking, Storage and Analysis_ , pages 1–16. IEEE, 2020. 

   - [43] Tri Dao, Dan Fu, Stefano Ermon, Atri Rudra, and Christopher R´e. Flashattention: Fast and memory-efficient exact attention with io-awareness. _Advances in neural information processing systems_ , 35:16344–16359, 2022. 

   - [44] TryHackMe Team. Tryhackme: Hands-on cybersecurity training platform. `https://tryhackme.com` , 2024. 

   - [45] HackTheBox Team. Hack the box: Cybersecurity labs and challenges. `https://www.hackthebox.com` , 2024. 

   - [46] VulnHub Community. Vulnhub: Vulnerable machines for penetration testing practice. `https://www.vulnhub.com` , 2024. 

   - [47] HuggingFace Team. Huggingface datasets hub: Open-source datasets for machine learning. `https://huggingface.co/datasets` , 2024. 

   - [48] Migel Tissera and WhiteRabbitNeo Team. Whiterabbitneo cybersecurity dataset (wrn-chapter-1, wrn-chapter-2). `https://huggingface. co/datasets/WhiteRabbitNeo/WRN-Chapter-1` , 2024. 

- [26] Yuxuan Zhu, Antony Kellermann, Dylan Bowman, Philip Li, Akul Gupta, Adarsh Danda, Richard Fang, Conner Jensen, Eric Ihli, Jason Benn, Jet Geronimo, Avi Dhir, Sudhit Rao, Kaicheng Yu, Twm Stone, and Daniel Kang. Cve-bench: A benchmark for ai agents’ ability to exploit realworld web application vulnerabilities. _arXiv preprint arXiv:2503.17332_ , Mar 2025. 

- [27] Isamu Isozaki, Manil Shrestha, Rick Console, and Edward Kim. Towards automated penetration testing: Introducing LLM benchmark, analysis, and improvements. In _Proceedings of the 2025 ACM Conference (companion_ / _adjunct) on Computer and Communications Security_ , 2025. Accessed: 2025-08-06. 

- [28] Julius Henke. Autopentest: Enhancing vulnerability management with autonomous llm agents. _arXiv preprint arXiv:2505.10321_ , 2025. 

- [29] Guohao Li, Hasan Hammoud, Hani Itani, Dmitrii Khizbullin, and Bernard Ghanem. Camel: Communicative agents for ”mind” exploration of large language model society. In A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt, and S. Levine, editors, _Advances in Neural Information Processing Systems_ , volume 36, pages 51991–52008. Curran Associates, Inc., 2023. 

- [30] Qian Liu, Jinke Song, Zhiguo Huang, Yuxuan Zhang, glide-the, and liunux4odoo. Langchain-Chatchat. `https://github.com/ chatchat-space/Langchain-Chatchat` , 2024. Accessed: 2026-0427. 

- [31] DirB Project. Dirb web content scanner. `https://gitlab.com/ kalilinux/packages/dirb` , 2025. 

- [32] Gobuster Project. Gobuster - directory/file, dns and vhost busting tool 

18 

