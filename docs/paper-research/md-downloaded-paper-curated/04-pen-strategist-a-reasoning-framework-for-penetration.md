# **Pen-Strategist: A Reasoning Framework for Penetration Testing Strategy Formation and Analysis** 

Yasod Ginige*, Pasindu Marasinghe*, Sajal Jain<sup>†</sup> , Suranga Seneviratne* 

* _The University of Sydney, NSW, Australia_ 

> † _Catharsis.net.au, Australia_ Email: {yasod.ginige, pasindu.marasinghe, suranga.seneviratne}@sydney.edu.au, sajal@catharsis.net.au 

## **Abstract** 

Cyber threats are rapidly increasing, expanding their impact from large-scale enterprises to government services and individual users, making robust security systems increasingly essential. However, a significant shortage of skilled cybersecurity professionals exacerbates this challenge. While recent research has explored automating tasks such as penetration testing using LLM-based agents, existing frameworks often perform poorly due to limited capability in strategy formulation, domain-specific reasoning, and accurate action and tool selection. To overcome these limitations, we propose _Pen-Strategist_ framework, consisting of a novel domain-specific reasoning model that derives pentesting strategies via logical reasoning and a classifier that converts the strategies into actionable steps. First, we construct a reasoning dataset containing logical explanations for both strategy derivation and step selection in pentesting scenarios. We then fine-tune a Qwen-3-14B model for strategy generation using reinforcement learning. Evaluation on the test split of the dataset demonstrates a 87% improvement in strategy derivation performance compared to the baseline. Furthermore, we integrate the fine-tuned Pen-Strategist model into existing automated pentesting frameworks, such as PentestGPT, and evaluate its performance on vulnerable machines, achieving a 47.5% improvement in subtask completion while surpassing the baseline GPT-5. Further experiments on the CTFKnow benchmark show an 18% performance gain over the base model. For step prediction, we train a semantic-based CNN classifier, which outperforms commercial LLMs by 28% and enhances execution stability. Finally, we conduct a user study to qualitatively assess the generated strategies, and Pen-Strategist demonstrates superior performance compared to the Claude-4.6-Sonnet. 

## **CCS Concepts** 

• **Security and privacy** → **Software and application security, Systems security** ; • **Computing methodologies** → _Artificial intelligence_ . 

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org. _Conference acronym ’XX, Woodstock, NY_ 

> © 2018 Copyright held by the owner/author(s). Publication rights licensed to ACM. ACM ISBN 978-1-4503-XXXX-X/2018/06 https://doi.org/XXXXXXX.XXXXXXX 

## **Keywords** 

Network Security, Software Security, Penetration Testing, Reasoning Models, LLM, LLM Agents 

#### **ACM Reference Format:** 

Yasod Ginige*, Pasindu Marasinghe*, Sajal Jain<sup>†</sup> , Suranga Seneviratne*, * _The University of Sydney, NSW, Australia_ ,<sup>†</sup> _Catharsis.net.au, Australia_ , Email: {yasod.ginige, pasindu.marasinghe, suranga.seneviratne}@sydney.edu.au, sajal@catharsis.net.au. 2018. Pen-Strategist: A Reasoning Framework for Penetration Testing Strategy Formation and Analysis. In _Proceedings of Make sure to enter the correct conference title from your rights confirmation email (Conference acronym ’XX)._ ACM, New York, NY, USA, 16 pages. https: //doi.org/XXXXXXX.XXXXXXX 

## **1 Introduction** 

Cyber incidents and attacks are increasing rapidly worldwide. While attackers have traditionally focused on large enterprises, they now also target small and medium-sized enterprises (SMEs), public sector organizations, and critical services such as hospitals and emergency response systems. This expanded threat landscape requires systems of all sizes to maintain a robust and continuously evolving security posture. Penetration testing (pentesting) and vulnerability and threat assessment are standard practices for securing software and networked systems. Pentesting simulates real-world attacks to uncover exploitable weaknesses, while vulnerability and threat assessment systematically identifies, analyzes, and prioritizes risks to enable proactive mitigation. Their frequency is often driven by regulatory requirements that vary across industries and government sectors [13]. However, these processes are time-consuming and resource-intensive, and the cybersecurity workforce cannot keep pace with demand due to the persistent skills shortage [1]. Consequently, automating these processes has become essential. 

Recent studies have explored the use of LLMs and LLM-based agents to automate security tasks such as penetration testing [12, 14, 33]. However, these approaches face several fundamental limitations: **(i)** they often fail to select effective strategies across different stages of the pentesting process, leading to poor vulnerability exploitation and limited attack surface coverage, and consequently require expert human guidance, undermining full automation [12, 21, 37]; **(ii)** they rely on external commercial LLM APIs, which necessitate transmitting sensitive information such as network structure and potential vulnerabilities to third-party servers, raising security and privacy concerns, while also introducing non-trivial operational costs and limiting deployment in environments requiring strict data locality or low-latency, tightly 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Trovato et al. 

coupled command execution [12, 14, 33]; and **(iii)** they exhibit unstable execution behavior, including hallucinations and invocation of incorrect or unavailable tools due to insufficient guidance in tool selection and orchestration [21, 33], during multi-step attack execution. 

To this end, we propose Pen-Strategist, a framework that consists of two models; (i) Strategy model: a domain-specific reasoning model to logically derive strategies for pentesting stages by evaluating prior findings, and (ii) Step model: a step classifier that converts generated strategies into actionable steps and tool selections. The two models can be used locally to generate strategies for Penetration testing tasks, while protecting data privacy. Furthermore, they can be integrated with agentic frameworks such as PentestGPT [12] for automated pentesting to achieve better results. First, we construct a novel reasoning-centric dataset tailored for penetration testing, comprising structured inputs along with logical explanations for both strategy derivation and step-level decision making. This dataset enables logically consistent reasoning while jointly supporting action and tool prediction, thereby reducing hallucinations and ensuring adherence to constraints in the execution environment. Subsequently, we train two models using this dataset. As the Strategy model, we finetune an open source Qwen-3-14B model, using Group Relative Policy Optimization (GRPO) [32], to improve its ability to generate logically grounded strategies across different stages of penetration testing. As the step model, we train a convolution-based classifier on top of frozen language model embeddings, which improves execution reliability and reduces invalid tool usage. We evaluate the Pen-Strategist framework on pentesting tasks and demonstrate significant performance improvements compared to commercial LLMs, driven by accurate strategy derivation and tool selection. Furthermore, we extend the evaluation to generalized red-teaming tasks, including CTF-style challenges, to assess the robustness beyond the training distribution. We also conduct ablation studies to analyze the contribution of different fine-tuning strategies and pipeline components. Finally, we conduct a survey with security professionals to qualitatively evaluate the practicality and effectiveness of the generated strategies. 

More specifically, we make the following contributions. 

- We propose Pen-Strategist, a novel framework for pentesting strategy derivation and the next action prediction, consisting of two models: the Strategy model and the Step model. 

- We create a new dataset to finetune LLMs for strategy derivation and step prediction in pentesting tasks. The dataset contains reasoning data for both strategy derivation and step prediction, covering 240 Hack-The-Box and VulnHub machines. To the best of our knowledge, the dataset is the first of its kind. 

- We fine-tune the Strategy model, built on an open-source LLM using reinforcement learning, achieving an 87% performance improvement over the baseline. We also train a semantics-based dual-head CNN model (Step model) for action classification, which attains 82.8% accuracy in step prediction and outperforms commercial LLMs. 

- We conduct extensive experiments by integrating Pen-Strategist into agentic pentesting frameworks (PentestGPT, AutoPentester, and VulnBot), achieving a 47.5% improvement in subtask completion, in Hack-The-Box machines. We further evaluate generalizability on CTF challenges, where PenStrategist improves performance by 28% over the base model. 

- Finally, we conduct a user survey among security professionals to qualitatively evaluate Pen-Strategist’s strategies in comparison with GPT-5 and Claude-4.6-Sonnet. We show that our strategy analyzer stands as the first choice in 52.4% of the cases, surpassing the other two models. 

We provide our dataset and code in our GitHub repository.<sup>1</sup> 

## **2 Related Work** 

## **2.1 Automated Penetration Testing** 

Early approaches to automated penetration testing relied on traditional reinforcement learning methods. For instance, Hu et al. [19] proposed a two-stage Deep Q-learning approach that first constructs an attack tree from network topology information and enumerates possible attack paths, then applies a Deep Q-Learning Network (DQN) to select the most easily exploitable path. However, their work focuses solely on recommending attack vectors rather than exploiting software vulnerabilities. 

Recent advancements in large language models (LLMs), including GPT [8], Claude [5], and Gemini [34], have enabled new approaches to automating cybersecurity tasks through LLM-based agents. PentestGPT [12] represents one of the first major efforts toward LLM-driven penetration testing, employing a summarizeranalyzer-generator pipeline. However, it remains semi-automated, requiring security professionals to manually execute strategies and provide feedback to guide the analyzer toward correct approaches. AutoAttacker [37] automated command generation and execution but was restricted to the Metasploit framework. The AutoPentester framework [14] addressed this limitation by supporting a broader range of tools; nevertheless, despite its multi-agent architecture, subtask completion rates on Hack-The-Box [16] challenges remain low, primarily due to strategy identification failures. Similarly, PentestAgent [33] and VulnBot [21] employ multi-agent architectures with specialized agents for planning, execution, and summarization, yet they too suffer from low subtask completion rates. The fundamental limitation underlying these frameworks is that commercial LLMs lack specialized capabilities for analyzing penetration testing strategies, as they are not specifically fine-tuned for such tasks. Additionally, existing frameworks frequently fail during action execution due to incorrect or unavailable tool selection [12, 21]. 

## **2.2 Cybersecurity Datasets for LLM Evaluation** 

Multiple datasets have been released to assess LLMs’ capabilities in various cybersecurity tasks. For example, the ExCyTIn-Bench dataset [36] is designed to evaluate LLM agents on their capabilities for cyber incident assessment, framed as multi-step questionanswering over security logs. It is constructed from a controlled Azure environment, simulating eight real-world attack scenarios. The final dataset consists of 589 question–answer pairs; however, 

1https://github.com/YasodGinige/Pentest-Strategist.git 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Pen-Strategist: A Reasoning Framework for Penetration Testing Strategy Formation and Analysis 

it does not provide any opportunity for strategic reasoning-based training, rather acts as a benchmark for existing LLMs. The CTFKnow dataset [20] is designed for evaluating LLMs on automated vulnerability discovery and exploitation tasks, where models must identify and reason about potential attack vectors. It contains multiple choice questions; therefore cannot be used to fine-tune a model for strategy derivations. The CyberSecEval dataset [7] is designed to evaluate LLMs on cybersecurity tasks such as vulnerability identification, exploit generation, and CVE score prediction. The dataset is constructed by combining real-world security benchmarks, including CVEs, CTF challenges, and code samples. However, none of the above datasets provides the platform to fine-tune a model for strategy analysis in the pentesting. CyberLLaMA [38] introduces a named entity recognition (NER) framework aimed at extracting structured security information, such as threats, vulnerabilities, and malware, from unstructured text. It fine-tunes a LLaMA-3.2-3B model on a large, carefully curated corpus of cybersecurity articles annotated with 4,788 unique entities, improving sequence labeling performance. Similarly, TrafficLLM [15] explores the fine-tuning of large language models for network traffic analysis to detect potential security threats. However, neither of these approaches addresses the need for a reasoning-oriented model capable of deriving penetration testing strategies. 

## **2.3 Finetuning LLMs with Reinforcement Learning** 

Reinforcement learning-based fine-tuning enables LLMs to develop advanced reasoning and strategic decision-making capabilities, essential for domains requiring sequential, goal-oriented problemsolving. Group Relative Policy Optimization (GRPO) [32] demonstrated the scalability of this approach, establishing it as a viable method for creating specialized reasoning models. GRPO and its variants [24, 30] extend preference-based finetuning such as Direct Preference Optimization (DPO) [31] by sampling multiple candidate outputs for the same prompt and ranking them within a group, allowing the model to learn from relative quality signals rather than absolute rewards. 

Generalized Direct Preference Optimization (GDPO) [24] builds on direct preference learning by incorporating more flexible formulations of preference comparisons, enabling the model to better align with nuanced or structured feedback beyond simple pairwise rankings. It typically improves sample efficiency and reduces reliance on explicit reward modeling while maintaining stable optimization. Reinforcement Learning with Verifiable Rewards (RLVR) [35] focuses on tasks where the correctness of the responses generated can be automatically checked, using deterministic reward signals derived from verifiers instead of learned reward models or human annotations. This approach reduces ambiguity in supervision and enables scalable training with reliable feedback. Together, these methods represent a shift toward more stable, scalable, and automation-friendly alignment techniques that reduce dependence on human labeling and complex reward modeling. 

Fine-tuning LLMs using reinforcement learning, in particular GRPO, for reasoning has shown promising results beyond typical scenarios such as coding and mathematics. For instance, [10, 30] 


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0003-07.png)


<!-- Start of picture text -->
Pen-Strategist<br>PTT  - summary of the Strategy model Step model<br>attack environment Analyze the previous step GPT2 - semantic<br>+ and results embedding extraction<br>Previous Step Reason out the next strategy<br>based on the previous Next step prediction<br>+ findings (PTT)<br>Previous Step Result Derived strategy with MCP server prediction<br>reasoning<br>Agent setup<br>1. Better strategy derivation.<br>Plug into other<br>frameworks<br>2. Correct next step (action) prediction.<br>Execution<br><!-- End of picture text -->


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0003-08.png)


**Figure 1: System overview of the Pen-Strategist. The framework is designed to be modular, allowing integration with other agent-based architectures.** 

reported that RL improves clinical reasoning and diagnostic generation under data scarcity. Similarly, Dai et al. [11] found that RL can be used to improve structured reasoning in legal applications. Similar improvements have been shown in finance for tasks such as credit assessment and risk pricing [26]. However, to the best of our knowledge, no existing work has fine-tuned a reasoning model specifically for penetration testing tasks. 

## **3 System Overview** 

As illustrated in Figure 1, Pen-Strategist is a modular framework comprising two models for strategy generation and step (i.e., action) classification in the pentesting. The _Strategy model_ acts as a domain-specific reasoning component that derives logical strategies for different pentesting stages based on prior findings, while the _Step model_ functions as a classifier that translates these strategies into executable steps and tool selections, guiding the automated execution. Pen-Strategist is designed to integrate with existing agentic penetration testing frameworks (e.g., PentestGPT [12], AutoPentester [14]), improving overall task performance. 

The Strategy model is fine-tuned to generate logically consistent strategies based on a summary of the target environment, including previously executed steps and their corresponding findings. To this end, we fine-tune a Qwen-3-14B model with Low-Rank Adaptation (LoRA) [18], as detailed in Section 4.2. 

The Step model is a multi-label classifier designed to predict the next action from a given strategy, along with the MCP servers required to execute it. The strategy is first encoded into a contextaware semantic embedding using a GPT-2 model. This embedding is then fed into a dual-head CNN, where one head predicts the next step (action) and the other identifies the relevant MCP servers. As a result, a follow-up LLM can be guided to decompose the main step into substeps to execute the strategy using the selected MCP servers. Having a separate step model reduces the hallucinations and execution failures due to incorrect tool usage. For instance, if the execution environment does not support the _Gobuster_ tool but does support _Dirbuster_ , only the _Dirbuster_ MCP tool will be included in the classification. This allows a downstream LLM to be explicitly guided to use Dirbuster, which would not be reliably ensured if it were simply asked to generate commands for the chosen steps—potentially leading to execution errors. Furthermore, 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Trovato et al. 


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0004-02.png)



![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0004-03.png)


<!-- Start of picture text -->
Walkthroughs<br><!-- End of picture text -->


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0004-04.png)



![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0004-05.png)



![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0004-06.png)



![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0004-07.png)



![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0004-08.png)


<!-- Start of picture text -->
Human Summarizer<br>interaction<br>Summarize the<br>results<br>Command<br>execution<br><!-- End of picture text -->


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0004-09.png)


<!-- Start of picture text -->
Target machine<br><!-- End of picture text -->


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0004-10.png)



![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0004-11.png)



![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0004-12.png)



![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0004-13.png)



![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0004-14.png)


<!-- Start of picture text -->
Generator<br>SubtaskGenerator<br>breakdown<br>MCP tool selection for<br>each subtask<br><!-- End of picture text -->


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0004-15.png)


<!-- Start of picture text -->
PTT  - summary of the attack Next strategy  - best<br>environment strategy for the current state<br>1. Reconnaissance - done Do a vulnerability analysis on theimagemagick 7.1.0-49<br>{findings: <>}<br>2.Vulnerability scan Explanation<br>       2.1. Port 22 - {findings: < >} The discovery of the 'magick' binary<br>       2.2. Port 80 - {findings: < >} is significant as ImageMagick has<br>.... been known to havevulnerabilities...<br>Next step  - next action MCP tools  - MCP tools Results summary  -<br>to execute the strategy that can be used to results summary of the<br>Do a google search for more execute subtasks commands executed<br>information<br>Explanation To find vulnerabilities of {'Google search': 'Search forknown vulnerabilities andexploits for ImageMagick ImageMagick version 7.1.0 hastwo significant vulnerabilities:CVE-2022-44268 and CVE-<br>ImageMagick 7.1.0-49, do a version 7.1.0-49'} 2022-44267....<br>google search...<br><!-- End of picture text -->


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0004-16.png)


<!-- Start of picture text -->
- Human action<br><!-- End of picture text -->


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0004-17.png)


**Figure 2: Dataset collection steps (a) and a sample data point (b).** 

the Step Model gives access to widely used security MCP servers and enables individual pentesters to use their preferred subset of tools (from a large and diverse ecosystem ) with existing frameworks by simply finetuning the classifier. The MCP servers can also be replaced using recently developed Claude Skills [4], which will be discussed in the Discussion. Overall, the Pen-Strategist framework manages the full planning pipeline, from deriving a logical strategy to its high-level execution. The significance of these components is discussed in the ablation study (Section 6.4). 

## **4 Methodology** 

In this section, we discuss curation of the training dataset, followed by Pen-Strategist model training. 

## **4.1 Dataset Curation** 

Our dataset is collected to accomplish two tasks: fine-tuning and training models for (i) pentest strategy derivation through reasoning and (ii) predicting the next step to execute a given strategy. It contains data points collected using 240 HTB and VulnHub machines in total, under two main parts based on the data curation process: **(i) Manual collection:** We collected data for 40 HTB machines using human supervision to input the strategy, next steps, and the logical reasoning for each decision using the write-ups (further explained in Section 4.1.1). Here, the human annotator breaks into HTB machines following walkthroughs and records the steps with logical reasoning for each decision, (ii) **Automated collection:** Since it is not practical to complete all the machines manually, and the fact that a large number of data points are required to fine-tune a reasoning model, we also designed an automated data curation workflow using Claude Code as detailed in Section 4.1.2. Our complete dataset contains 2,165 data points. 

_4.1.1_ **Manual data collection workflow** _._ As illustrated in Figure 2-(a), in the manual data collection workflow, we employ a modified PentestGPT framework and systematically log the required 

data fields while iteratively following the penetration testing workflow based on the corresponding machine write-ups. PentestGPT is modified in two key ways. First, instead of Analyzer automatically generating the next optimal strategy and steps, a human annotator provides the strategy, action, and their associated logical explanations by consulting the write-ups. Second, during execution, we record a set of structured data points at each iteration. Specifically, we capture the _PenTest Tree (PTT)_ , which summarizes the current state of the target environment, including prior actions and their outcomes. We also log the _Previous step_ and _Previous step result_ , representing the most recent action and its observed outcome. Furthermore, the _New strategy_ and _Strategy explanation_ describe the next optimal strategy and its underlying rationale, derived from the PTT and preceding results. The _New step_ and _Step explanation_ detail the concrete action to be executed, including the tools or MCP servers involved and their usage. Finally, the _Results_ field records the outputs obtained from executing the proposed step. A detailed discussion about the data fields and formats is given in Section 4.1.3. 

_4.1.2_ **Automated data collection workflow** _._ In the automated data collection workflow, we use Claude Code to extend the dataset using an additional 200 machines from HTB and VulnHub. Initially, we compile a list of target machines from both platforms and collect their corresponding write-up files. Next, we provide Claude Code with a subset of manually curated dataset samples along with their associated write-ups, enabling it to infer the desired data structure and formatting. Subsequently, guided by explicit instructions and formatting specifications, Claude Code is used to transform the information contained in the write-ups into the required dataset format. Importantly, this process is purely a data conversion and structuring task, where Claude Code extracts and reformats information from existing write-ups, rather than executing any live commands or performing autonomous penetration testing. As the source write-ups are already validated and the manually collected samples serve as reliable references, the generated dataset is consistently well-structured. To further ensure data quality, we perform 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Pen-Strategist: A Reasoning Framework for Penetration Testing Strategy Formation and Analysis 

##### **Strategy:** 

Enumerate the web application to understand its functionality and identify potential attack vectors. 

##### **Step:** 

Further enumerate the website by identifying hidden directories, links, and underlying technologies. 

|**MCP Servers:**|
|---|
|- Web Page Interaction: Browsehttp://10.10.11.12to identify application<br>purpose and functionality.|
|- Dirbuster: Enumerate directories and fles to discover hidden content.|
|- Interactive CLI: Examine HTTP headers and page source for technology indi-<br>cators.|



**Figure 3: A sample strategy decomposition illustrating the use of MCP servers for web application enumeration.** 

a manual review of the entire dataset to validate formatting consistency, along with an additional inspection of 10% randomly sampled entries to verify their content correctness against the original writeups. This process did not reveal any significant errors, indicating the dataset’s overall reliability. 

_4.1.3_ **Dataset format** _._ Figure 2-(b) illustrates a sample data instance comprising: _PTT_ , which represents the pentesting process as an attack tree enriched with summarized findings; _New strategy_ and _Strategy explanation_ , which provide the ground truth strategy and its derivation for a given pentest instance; _Next step_ and _Step explanation_ , which specify the action to be taken along with its rationale; _MCP tools_ , which gives suitable tools to execute the selected step; and _Results_ , which summarize the tool outputs from executed commands. 

The _Next step_ is restricted to a predefined set of high-level actions as listed in the first column of Table 1. This constraint helps stabilize the automated execution phase by reducing hallucinations and variability in command generation and tool usage. As illustrated in Figure 3, when executing a strategy, the step model classifies it into one of these steps and predicts the MCP server to be used to execute the step. We define 11 _MCP servers_<sup>2</sup> that commonly used in pentesting: Nmap, Metasploit, Netcat, Dirbuster, SQLmap, SMB client, Hydra, John-the-ripper, Google search, Interactive CLI, and Web page interaction. This facilitates training a model to accurately produce the New step and its explanation, while also selecting the appropriate MCP servers needed to execute the commands for that step. 

_4.1.4_ **Dataset summary** _._ Next, we present summary statistics of the dataset. First, we examine the dataset by analyzing how strategies as classified by an LLM are distributed across pentesting stages (e.g., reconnaissance, vulnerability scanning, and others), as shown in Figure 4. In this stage-wise breakdown, reconnaissance (33.0%) and exploitation (28.4%) represent the largest portions of the data, followed by vulnerability scanning (20.8%). Other stages, including privilege escalation, lateral movement, and maintaining access, are less frequently observed. This distribution is advantageous for 

> 2An MCP server is a standardized, secure bridge that connects AI models to external tools and data sources. Example security-specific MCP servers can be found here: https://github.com/cyproxio/mcp-for-security. 

|33.0%<br>(714)<br>28.4%<br>(615)<br>Stage-wise Distribution|20.8%<br>(450)<br>11.4%<br>(247)<br>(Total: 2,165 entries)|
|---|---|
|0%<br>20%<br>40%<br>Percentage|60%<br>80%<br>100%<br>(%)|
|Reconnaissance  (33.0%, 714)|Privilege escalation  (11.4%, 247)|
|Exploitation  (28.4%, 615)|Lateral movement  (3.5%, 76)|
|Vulnerability scanning  (20.8%, 450)|Maintaining Access  (2.9%, 63)|



**Figure 4: Distribution of the strategies in different stages of the pentesting process.** 

**Table 1: Distribution of the items of** **_Next Step_** 

|Next step|Count|%|
|---|---|---|
|Exploit the selected exploitations|628|35.64|
|Enumerate further on the X service to fnd software|357|20.26|
|versions, hidden directories and fle.|||
|Explore the suspicious fles, commands and create a<br>summary of the fndings.|176|9.99|
|End task and ask permission to generate the report|174|9.88|
|Further enumerate the website (hidden directories, links,<br>software)|165|9.36|
|Do a Google search for more information|108|6.13|
|Analyze the outcomes of the previous step and fnd an<br>attack path|93|5.28|
|Enumerate the domain|31|1.76|
|Explore the source code for vulnerabilities|29|1.65|



model fine-tuning, as it reflects realistic operational patterns and allows the model to focus on the most critical and commonly occurring stages, particularly reconnaissance and exploitation. At the same time, the inclusion of 76 lateral movement and 63 maintaining access instances ensures that even these less frequent stages are adequately represented, enabling the model to learn a more complete spectrum of pentesting tasks. 

Table 1 lists the distribution of the _Next Steps_ in the dataset. In particular, exploiting identified vulnerabilities (35.64%) and further enumeration of services (20.26%) appear most frequently, followed by activities such as analyzing findings and reporting-related steps. Other actions, such as domain enumeration and source code analysis, occur less frequently due to their lower prevalence in the HTB environment. 

## **4.2 Pen-Strategist Model Training** 

As mentioned before, the Pen-Strategist framework consists of two key components: _strategy prediction_ and _step prediction_ , capturing the logical (what to do) and methodological (how to do it) aspects of pentesting, respectively. To this end, we develop two specialized models. The strategy model derives the most appropriate next strategy based on prior steps and observed findings, while the step model predicts the next action along with the corresponding MCP servers required for execution. We fine-tune a Qwen3-14B [2] model with LoRA [18] on a single H200 GPU for strategy prediction, and train a semantics-based dual-head CNN model for step classification. 

_4.2.1_ **Strategy Model** _._ As illustrated in Figure 5, we fine-tune the Qwen3-14B model using LoRA with GRPO [32], where only the LoRA parameters are updated during training. The objective is to enable the model to infer the next strategy in a pentesting workflow by emulating human reasoning, analyzing prior findings to determine subsequent actions. To provide sufficient context, the 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Trovato et al. 


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0006-02.png)


<!-- Start of picture text -->
Update ({G}, {A}, πθ)<br>User prompt<br><PTT> {ptt} </PTT> Qwen3-14B LoRA<br> <PS> {prev_step} (frozen) G11 A11<br></PS> (r=8, alpha=16) G22 A22<br> <PSR> {prev_res}<br></PSR> Reward functions<br> Derive a Newstrategy for thenext step in thepentesting process Generation 1 (GGeneration 1 (G1)Generation 1 (G1)Generation n (G1) n) (G ) R i i with the GTsimilarityStrategy Responseformatformat<br>based on theprevious step and {R , R ,1 2 ....., R }n Language Responselengthlength<br>the findings.....  {A1 , A2 ,....., A n }<br>...<br><!-- End of picture text -->


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0006-03.png)


<!-- Start of picture text -->
G11 A11<br>G22 A22<br>Reward functions<br>similarityStrategyStrategy Responseformatformat<br>with the GTsimilarityStrategy<br>Language<br>Responselengthlength<br><!-- End of picture text -->

**Figure 5: Strategy model training steps.** 

user prompt includes the PTT, which summarizes the attack environment up to the current stage and includes executed steps and their outcomes, along with the immediate previous step and its result. Based on this information, the model is guided to generate the next strategy through logical reasoning followed by a concise explanation. The detailed prompts used are provided in Appendix C. 

### **GRPO fine-tuning** 

In GRPO, the model produces multiple candidate outputs ( _𝑦𝑖_ ) for each input prompt instead of a single response; in our setup, four responses are sampled from the current policy to form a comparison group. These candidates are evaluated using a set of reward functions, and the higher-quality outputs are selected based on their relative reward scores within the group. Learning is then driven by optimizing the model to increase the likelihood of these betterperforming responses. This relative comparison-based optimization encourages the model to favor higher-quality outputs while improving training stability and reducing variance. The reward functions used are as follows: 

**i) Semantic and logical similarity reward (** _𝑅𝑠_ **):** We quantify the semantic and logical alignment between the generated _New strategy_ and _Strategy explanation_ and their ground-truth counterparts using the G-Eval [25] - an LLM as a judge framework, which employs an LLM to evaluate two texts under a fixed rubric. We use GPT-4o as the evaluator with four criteria ( _𝐺𝐸𝑣𝑎𝑙𝑘_ ) based evaluation in the GEval framework; logical alignment with the groundtruth rationale, reference to similar evidence and primary task, consistency of the final decision for the given context, and usage of similar tools and techniques. Each criterion is independently scored by the evaluator, and the final similarity reward is computed by averaging the scores given to each criterion, as denoted by _𝑅_ s ( _𝑔,𝑦_ ) =<sup><u>1</u></sup> 4 � _𝑘_ 4=1<sup>GEval</sup><sup>_𝑘_(</sup><sup>_𝑔,𝑦_).</sup> 

This reward captures the overall logical and semantic agreement between the generated strategy (y) content and the ground truth (g). The prompt used is provided in Figure 12 in Appendix C. 

ii) **Pattern reward (** _𝑅𝑝_ **)** forces the model to generate the output in the following pattern. _<think> logical derivation </think> New strategy <explanation> Strategy explanation </explanation>_ . This is a hard reward where the exact match gets a 1, otherwise 0. 

iii) **Generation length reward (** _𝑅𝑙_ **)** the model to keep the generation length below the maximum token count 1,024. Otherwise, 

the reasoning tends to explode as training progresses. The reward function is defined according to the Equations 1 and 2. 


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0006-13.png)



![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0006-14.png)


iv) **Language reward (** _𝑅𝑒_ **)** forces the model to stick to the English language without mixing with other languages during the reasoning. This ensures the generated rationale is directly applicable to the similarity reward without any complexities. The language reward is defined as 1.0 if the output is in English, 0.0 if it is in any other language, and -1.0 if the output is empty. 

Finally, we sum up all reward components into a single total reward, denoted as _𝑅_ total. Since four strategies are generated for each prompt, we obtain four corresponding _𝑅_ total values, each reflecting the quality of the respective strategy. Rtotal = { _𝑅_ total ( _𝑦_ 1) _, 𝑅_ total ( _𝑦_ 2) _, 𝑅_ total ( _𝑦_ 3) _, 𝑅_ total ( _𝑦_ 4)}. 


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0006-17.png)


To encourage higher-quality strategies while discouraging weaker ones, GRPO assigns each sampled completion an advantage score based on its relative performance within the group using the Equation 3. For a given prompt, we sample _𝑁_ = 4 candidate completions { _𝑦𝑖_ } _𝑖_<sup>_𝑁_</sup> =1<sup>, each of which is evaluated using a set of reward functions.</sup> The advantage _𝐴𝑖_ is computed as the normalized deviation of the total reward of _𝑦𝑖_ from the group mean, where positive values indicate above-average performance and negative values indicate below-average quality. 


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0006-19.png)


The policy is then optimized using an advantage-weighted objective, as defined in Equation 4, which increases the likelihood of higher-advantage completions while reducing that of loweradvantage ones. In parallel, a Kullback–Leibler (KL) divergence [22] penalty is applied to constrain the learned policy _𝜋𝜃_ from deviating excessively from a fixed reference policy _𝜋_ ref, which corresponds to the base pretrained model. This regularization term improves training stability and prevents overfitting to high-reward samples by maintaining proximity to the reference distribution. 

We set the optimization learning rate to 5<sup>−5</sup> , a common value for finetuning LLMs. The model was trained with the AdamW optimizer and a weight decay of 0.01 to regularize the parameters. A linear learning rate schedule was applied, in which the learning rate was gradually increased over the first 10% of training steps (warmup ratio of 0.1) and then linearly decreased for the rest of the training. 

_4.2.2_ **Step Model** _._ We train a dual-task architecture consisting of a frozen GPT-2 encoder and two independent convolution-based classification heads to predict (i) the next step class and (ii) the set 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Pen-Strategist: A Reasoning Framework for Penetration Testing Strategy Formation and Analysis 

of MCP servers, conditioned on the _New strategy_ and its _Strategy explanation_ . The objective is to discourage invalid or unavailable tool selection and reduce overly generic or unfocused tool usage, thereby improving the stability and consistency of strategy execution. 

Given the input formed by concatenating the strategy and its explanation, we extract contextual token-level embeddings using a pretrained GPT-2 model. Since GPT-2 does not provide a dedicated classification token, we retain full sequence representations and do not perform CLS pooling. The encoder is kept frozen and used solely as a feature extractor. On top of these embeddings, we apply two separate convolutional encoders with multiple kernel sizes to capture local semantic patterns. Each encoder performs temporal convolution followed by global max pooling to produce a fixeddimensional representation. One representation is used for step classification, and the other for MCP server prediction. 

We formulate the learning problem as a two-task multi-label classification setting, where a shared representation is used to jointly predict (i) the next step label and (ii) the MCP server set. For each training instance, we compute a cross-entropy loss for step prediction and a binary cross-entropy loss for MCP prediction using the ground-truth labels _𝑦_ step ∈ _𝐴_ and multi-hot vector _𝑦_ mcp ∈{0 _,_ 1}<sup>|</sup><sup>_𝑀_|</sup> , respectively: 


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0007-05.png)


where _𝑧 𝑗_<sup>(mcp)</sup> denotes the logit corresponding to the _𝑗_ -th MCP class and _𝜎_ (·) is the sigmoid activation. The final objective is a 

**Algorithm 1** Dual-Task Training for step and MCP prediction with Frozen GPT-2 and <u>dual head CNN model.</u> 

**Require:** Dataset D with inputs _𝑥_ , step labels _𝑦_<sup>(</sup><sup>_𝑠_)</sup> , and MCP labels _𝑦_<sup>(</sup><sup>_𝑚_)</sup> **Require:** Frozen GPT-2 encoder _𝑓𝜃_ , dual CNN heads _𝑔𝜙𝑠_ and _𝑔𝜙𝑚_ **Require:** Learning rate _𝜂𝑡_ , batch size _𝐵_ , epochs _𝐸_ , weight decay _𝑤𝑑_ , and loss weights _𝜆𝑠, 𝜆𝑚_ 


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0007-09.png)


weighted combination of both losses, calculated as L = _𝜆_ stepLstep + _𝜆_ mcpLmcp. 

where we set _𝜆_ step = 1 and _𝜆_ mcp = 1 _._ 5 based on empirical performance. Optimization is performed using AdamW with a linear warmup followed by linear decay, where _𝜂𝑡_ denotes the timedependent learning rate and _𝑤𝑑_ is the weight decay coefficient. The overall training procedure is summarized in Algorithm 1. 

## **5 Experimental Setup** 

We divide the experiments into several setups for easier analysis. 

## **5.1 Test Set Evaluation** 

We evaluate the fine-tuned strategy and step models using the heldout test set of the dataset. It contains 10 machines from the manual collection and 30 from the automated collection. The goal is to measure how well the fine-tuned model performs in strategy derivation and step prediction compared to other commercial models such as GPT, Gemini, and Claude (The exact model versions are listed in the result Table 2). For strategy derivation, we use two metrics: final strategy similarity and the explanation similarities measured by G-Eval scores, following the same criteria as the similarity reward (Section 4.2.1). 

For step prediction and MCP server prediction, we use accuracy and Micro F1 score as evaluation metrics, respectively. Accuracy measures the model’s ability to correctly predict the exact next step as the ground truth. In contrast, MCP server prediction is a multi-label task, as a single step may involve multiple servers. Therefore, in addition to accuracy, which captures the correctness of the entire predicted set, we use the Micro F1 score to evaluate element-wise prediction performance. The F1 score is computed at the per-sample level and then averaged across all samples to obtain the final Micro F1 score. For each sample _𝑛_ , the true positives ( _𝑇𝑃𝑛_ ), false positives ( _𝐹𝑃𝑛_ ), and false negatives ( _𝐹𝑁𝑛_ ) are computed as: 


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0007-17.png)


Here, _𝑁_ denotes the total number of samples in the evaluation set and _𝐾_ denotes the number of MCP server labels in the multilabel prediction space. For each sample _𝑛_ ∈{1 _, . . . , 𝑁_ } and label _𝑗_ ∈{1 _, . . . , 𝐾_ }, the ground-truth indicator _𝑦𝑛,𝑗_ ∈{0 _,_ 1} specifies whether MCP label _𝑗_ is actually present, while the predicted indicator _𝑦_ ˆ _𝑛,𝑗_ ∈{0 _,_ 1} specifies whether the model predicts that label. The corresponding results are presented in Section 6.1. 

## **5.2 Evaluation by Integrating to Existing Frameworks** 

In this experiment, we replace the strategy analysis/planning module of existing pentesting frameworks with the fine-tuned strategy model. Specifically, we evaluate this integration within the PentestGPT [12], AutoPentester [14], and VulnBot [21] frameworks. As the evaluation benchmark, we use six HTB machines (Sau, Pilgrimage, Authority, Jupiter, Jarvis, and Bank), none of which were included in the training data of the fine-tuned model. The objective is to assess the performance improvement of these frameworks when employing the fine-tuned LLM in place of commercial LLMs within the strategy analysis component. For comparison, GPT-5 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Trovato et al. 

is used as the baseline commercial LLM under the default settings of each framework. As the evaluation metric, we use the subtask completion rate, a widely adopted metric in agent evaluations on pentesting tasks [12, 14, 33], where each machine’s attack vector is divided into subtasks. We calculate the percentage of subtasks completed out of the total number of subtasks as the completion rate. For each machine, we conduct three runs and report the average subtask completion rate to minimize the variability of results. 

Recent updates of Claud Code demonstrate enhanced skills in task automation. Therefore, we evaluate the Claude Code in pentesting tasks by giving the six HTB machines to solve autonomously. The corresponding results are presented in Section 6.2. 

## **5.3 Cross-Task Generalization** 

To assess generalizability, we evaluate Pen-Strategist on additional security tasks that require logical reasoning, such as CTF challenges. In particular, we use the PicoCTF challenges [12] and the CTFKnow [20] dataset to determine whether fine-tuning improves performance in task completion. 

For the PicoCTF evaluation, we adapt the experiment setup in PentestGPT [12], which contains 20 challenges. PentestGPT uses GPT-5 as the backend for the strategy analyzer agent to solve the challenges; we replace it with the base Qwen-3-14B model and the fine-tuned strategy model, enabling us to assess the impact of fine-tuning on CTF problem-solving performance, which is measured using the challenge completion rate. For each challenge, we perform five independent runs and record the number of successful completions. 

In the CTFKnow dataset, we run the benchmark experiments using the fine-tuned strategy model directly. The dataset consists of multiple-choice questions based on security incidents, where the agent is required to analyze each scenario and select the most appropriate answer. We evaluate the task success rate, the original metric used in the benchmark. The corresponding results are presented in Section 6.3. 

## **5.4 Ablation Study** 

We conduct an ablation study using the AutoPentester [14] and integrate the fine-tuned strategy model as the backend of its analyzer agent. The Step model is used to predict the next step and tools that guide the command generator in the execution phase. Unlike PentestGPT, which requires manual command execution, AutoPentester is a fully automated framework. Therefore, it enables us to assess the effectiveness of the Step model by measuring reductions in command execution failures in an automated setting. 

For evaluation, we use three HTB machines—Sau, Authority, and Jarvis—as the test bench. We compare three configurations: (i) the original AutoPentester, (ii) AutoPentester with the fine-tuned strategy model, and (iii) AutoPentester with both the fine-tuned strategy model and the additional step prediction stage. This setup allows us to analyze the contribution of individual components, namely the strategy model and the step model, to overall system performance. The evaluation metric used is subtask completion rate. The corresponding results are presented in Section 6.4. 

**Table 2: Model performance on Strategy and Explanation. Here, we use the GEval score as the evaluation criterion.** 

|**Model Name**|**Strategy**|**Explanation**|
|---|---|---|
|Claude 3 Haiku|0.54|0.58|
|Claude 4.5 Sonnet|0.65|**0.72**|
|Gemini 2.0 Flash|0.40|0.53|
|Gemini 2.5 Flash|0.45|0.56|
|GPT-3.5-turbo|0.36|0.47|
|GPT 4.1|0.60|0.66|
|GPT-4o-mini|0.52|0.64|
|GPT-5|0.62|0.63|
|LLaMA-3.1-8B|0.40|0.51|
|Qwen-3-14B|0.39|0.45|
|**Qwen-3-14B-GRPO (ours)**|**0.73**|0.71|



## **5.5 Human Expert Evaluation** 

We conducted a user study with 12 security experts to qualitatively evaluate the reasoning quality and practical usefulness of the generated pentesting strategies. The study was approved by our institution’s Human Research Ethics Committee, and the participants were recruited based on their expressed interest in a LinkedIn post promoting the survey. We used 15 pentesting scenarios, each outlining the sequence of steps performed and the corresponding findings describing a specific stage of an ongoing penetration testing process. These scenarios were organized into three sets, each consisting of five scenarios. For each scenario, we give three strategy outputs to rank generated by different LLMs: our fine-tuned Strategy model, GPT-5, and Claude-4.6-Sonnet. To avoid bias, model identities were anonymized. A sample scenario is given in Figure 13 in the Appendix C. 

Each participant was presented with one set containing five scenarios. For each scenario, they were asked to rank the strategies generated by three models based on logical correctness and alignment with the given task, assigning a rank of 1 to the bestperforming strategy and 3 to the least effective. In addition, participants reported their confidence in each ranking decision using a three-level scale (very confident, somewhat confident, not at all confident) to account for potential ambiguity in judgment. Finally, free-text feedback was collected to better understand the reasoning behind participant rankings, and participants were also encouraged to provide qualitative comments on the strengths and weaknesses of the generated strategies. 

As evaluation metrics, we report: (i) the percentage of a particular model being selected as the first choice, and (ii) Kendall’s W statistic [23] to assess the level of agreement among participants’ rankings. To incorporate participant confidence into the evaluation, we filter a subset of scenarios where the participant was highly confident and recalculate the metrics. The corresponding results are presented in Section 6.5 

## **6 Results** 

In this section, we report results from the experiments described in Section 5. 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Pen-Strategist: A Reasoning Framework for Penetration Testing Strategy Formation and Analysis 

**Table 3: Step and MCP server prediction performance.** 

##### **Scenario:** 

|**Model**|**Step**<br>**Acc.(%)**|**Step**<br>**Micro F1**|**MCP**<br>**Acc.(%)**|**MCP**<br>**Micro F1**|
|---|---|---|---|---|
|Claude 3 Haiku|55.43|0.53|16.13|0.39|
|Claude 4.5 sonnet|63.44|0.66|24.73|0.60|
|Gemini 2.0 Flash|61.29|0.67|24.17|0.59|
|Gemini 2.5 Flash|64.52|0.68|30.11|0.62|
|GPT-3.5-turbo|41.76|0.45|18.52|0.40|
|GPT 4.1|62.78|0.65|28.41|0.58|
|GPT-4o-mini|54.83|0.54|28.69|0.56|
|GPT-5-mini|59.66|0.65|33.81|0.50|
|LLaMA-3.1-8B|51.09|0.54|13.98|0.38|
|**Step Model(ours)**|**82.87**|**0.80**|**48.88**|**0.64**|



## **6.1 Test Set Evaluation** 

_6.1.1_ **Strategy Model:** Table 2 shows the results of Pen-Strategist evaluated on the test set using the setup described in Section 5.1. As observed, predicting pentesting strategies remains challenging for current large language models, as reflected in consistently low GEval scores, mostly below 0.6. The strongest baseline, Claude4.5-Sonnet, achieves 0.65 for strategy and 0.72 for explanation, yet still falls short of the proposed approach. It is also notable that more recent commercial model versions generally outperform their earlier counterparts (e.g., Claude 4.5 Sonnet vs. Claude 3 Haiku), suggesting incremental improvements with model evolution. 

GRPO fine-tuning significantly enhances the performance of Qwen-3-14B on both strategy and explanation similarity, with scores increasing from 0.39 to 0.73 and from 0.45 to 0.71, respectively. The fine-tuned model outperforms all evaluated commercial models in strategy prediction, achieving an improvement of approximately 87% over its base version. Notably, it surpasses Claude 4.5 Sonnet, the strongest commercial baseline, by 8 percentage points in strategy similarity, despite being considerably smaller in scale. In Figure 6, we present an example illustrating how GRPO training has improved the base model. The base model provides a high-level answer, whereas the fine-tuned model offers a more specific and actionable strategy by leveraging the SQL injection to achieve direct code execution through a webshell. 

The explanation similarity of the Strategy model is on par with Claude-4.5-sonnet. Since the reasoning involves a step-by-step process with dense security-related terminology, an area where Claude models are typically stronger, the GEval score is slightly higher than that of the Strategy model. 

_6.1.2_ **Step Model:** Next, we evaluate the trained Step model on the test dataset. As shown in Table 3, the Step model achieves the best performance across all evaluation metrics, clearly outperforming all baseline LLMs for both step and MCP prediction. Among the baselines, Gemini 2.5 Flash emerges as the strongest overall competitor, although it still lags behind the trained model by a noticeable margin (18% in Step F1-score and 5% in MCP F1-score). This consistent gap indicates that, while general-purpose LLMs can provide reasonable performance, they are not yet reliable for precise step and MCP server prediction in this setting. Overall, the results demonstrate that task-specific supervised training with a dedicated classifier is substantially more effective than prompting generalpurpose LLMs, leading to more reliable structured predictions for automated execution. 

Reconnaissance identified key findings supporting SQL injection exploitation: an Apache web server hosting the “Stark Hotel” application and a dynamic parameter (cod) in the booking feature, which was confirmed to be vulnerable to union-based SQL injection. Exploitation of this vulnerability already demonstrates significant database interaction capabilities, including retrieval of the database version and user (DBadmin@localhost). More importantly, the ability to read system files confirms that the database has elevated privileges and supports file operations. Further inspection of the Apache configuration reveals the DocumentRoot (/var/www/html), and the environment indicates that MySQL file-writing functionality (e.g., INTO OUTFILE) is likely available. 

##### **Base Model:** 

Use the confirmed SQL injection to extract more database information, look for user credentials, exploit file writing capability to gain persistent access or execute commands, check for other vulnerabilities, and consider privilege escalation. 

##### **Fine-tuned Model:** 

The next strategy involves exploiting the confirmed SQL injection vulnerability to write a PHP webshell into the server’s DocumentRoot using the INTO OUTFILE clause. This will allow us to execute arbitrary commands on the server. The SQL injection payload will be crafted to write a reverse shell or webshell into /var/www/html, which is the DocumentRoot. Once the shell is uploaded, it can be accessed via the web browser, granting a shell session on the target system. 

**Figure 6: A sample strategy derived by Qwen-3-14B base model and the fine-tuned model (i.e., Pen-Strategist-Strategy model) for a pentesting scenario.** 

## **6.2 Evaluate on Pentesting Frameworks** 

As outlined in Section 5.2, we assess the Strategy model by integrating it as the backend of strategy analyzer agents within automated pentesting frameworks. Figure 7 shows the performance of these frameworks across six HTB machines, using GPT-5 and the Strategy model as backends. The higher patterned bars show that our model consistently outperforms GPT-5, achieving higher subtask completion rates across all machines and frameworks. Overall, the finetuned model improved the subtask completion rate of PentestGPT by 46.5% and AutoPentester by 43.4%, VulnBot by 52.5%, across all the test machines. These findings indicate that RL-augmented frameworks demonstrate clear performance gains, indicating that 


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0009-18.png)


<!-- Start of picture text -->
Subtask Completion Rate of HTB Machines<br>P-GPT A-GPT V-GPT Claude code<br>100 P-RL A-RL V-RL<br>80<br>60<br>40<br>20<br>0<br>HTB Machines<br>Sau Pilgrimage Authority Jupiter Jarvis Bank<br>Subtask Completion Rate (%)<br><!-- End of picture text -->

**Figure 7: Subtask completion rates for HTB machines. P, A, and V denote PentestGPT, AutoPentester, and VulnBot, respectively. X-GPT uses the GPT-5 as the backend for the strategy analyzer, and X-RL uses the Strategy model.** 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Trovato et al. 

**Table 4: Performance of different LLMs on CTF-Known benchmark. Note that finetuning has significantly improved the Qwen model’s performance.** 

|**Model/Human**|**Web (218)**|**Pwn (459)**|**Misc (332)**|**Crypto (638)**|**Reverse (128)**|**Forensics (221)**|**Total (1996)**|
|---|---|---|---|---|---|---|---|
|GPT-3.5-Turbo|72.02|79.08|82.23|81.03|79.69|76.47|79.21|
|GPT-4-Turbo|80.73|85.40|87.95|86.21|90.62|85.07|85.87|
|GPT-4o|83.03|88.02|89.46|88.56|89.84|86.43|87.83|
|GPT-5-mini|88.26|91.21|92.41|93.88|93.43|91.67|92.26|
|Llama-3-70B|83.03|86.06|88.86|85.89|89.84|87.33|86.52|
|Gemini-2.5-Flash|79.58|79.20|86.22|81.50|82.41|78.49|81.23|
|Claude-4.5-Sonnet|85.71|75.40|89.19|69.64|76.19|72.22|76.10|
|Qwen-3-14B|67.69|76.03|74.87|78.60|72.59|64.37|72.38|
|Qwen-3-14B-GRPO (Our)|81.31|85.19|81.96|87.37|89.47|89.29|85.71|



the fine-tuned model significantly enhances subtask completion by enabling more accurate next strategy derivation. 

For completeness, we repeat the experiment using the Claude Code as the agentic pentester. We observed that Claude Code falls short compared to AutoPentester and PentestGPT with the Strategy model backend, achieving 45.83% on average across machines. However, it is worth noting that Claude Code performs marginally better than VulnBot version with the fine-tuned model. 

## **6.3 Cross-Task Generalization** 

As outlined in Section 5.3, we assess the performance of the Strategy model on CTF challenges. The results in Table 4 on the CTFKnown benchmark show that GRPO finetuning substantially enhances the Strategy model’s reasoning and problem-solving performance across all task categories. The Qwen-3-14B base model achieves a total success rate of 72.38%, which is substantially lower than GPT-4o and GPT-4-Turbo. This performance gap is expected, as commercial models benefit from significantly larger parameter scales and are trained on extensive proprietary datasets comparable to those 

**Table 5: PicoCTF challenge results using different LLMs as the strategy analyzer in PentestGPT. We conduct 5 runs for each challenge and report the number of successful completions. The Qwen model used is Qwen-3-14B.** 

|**Challenge**|**Category**|**GPT-5**|**Qwen**<br>**Base**|**Qwen-**<br>**RL**|
|---|---|---|---|---|
|login|web|3|1|3|
|advance-potion-making|forensics|2|1|2|
|spelling-quiz|crypto|1|1|2|
|caas|web|2|0|1|
|XtrOrdinary|crypto|2|1|1|
|tripplesecure|crypto|1|1|2|
|clutteroverfow|binary|1|0|1|
|not|crypto|0|0|1|
|scrambled-bytes|forensics|0|0|0|
|breadth|reverse|0|0|0|
|notepad|web|0|0|0|
|college-rowing-team|crypto|1|0|2|
|fermat-strings|binary|0|0|1|
|corrupt-key-1|crypto|0|0|1|
|SaaS|binary|0|0|0|
|riscy business|reverse|0|0|0|
|homework|binary|0|0|0|
|lockdown-horses|binary|0|0|0|
|corrupt-key-2|crypto|0|0|0|
|vr-school|binary|0|0|0|
|Total||13|5|17|



used in the experiment. However, after GRPO fine-tuning, Qwen3-14B-GRPO improves to 85.71%, narrowing the gap with GPT-4o to just 2.12 percentage points and outperforming several strong baselines such as Llama-3-70B. Importantly, this gain was achieved with a much smaller 14B parameter model, and it can be deployed and hosted locally, offering a practical advantage in terms of cost and data privacy. Overall, fine-tuning consistently boosts performance across all domains, with the largest improvements observed in reasoning-heavy tasks such as reverse engineering and forensics. 

Furthermore, Table 5 presents the results of the PicoCTF challenges conducted using the PentestGPT framework and different LLMs as the strategy analyzer. The results show a clear improvement in the Qwen model after fine-tuning. The base Qwen-3-14B achieves only 5 total successful cases, whereas the fine-tuned QwenRL reaches 17. Notably, Qwen-RL slightly outperforms GPT-5 in total successful attempts, indicating that fine-tuning improves the model’s ability to generalize reasoning across CTF challenges. 

## **6.4 Ablation Study** 

Our ablation study consists of evaluating the impact of the two newly introduced models, namely the strategy and step models, on pentesting tasks, with the results reported in Table 6. In addition, we analyze the failure cases observed in the ablation study and present them in Table 7. The AutoPentester with the Strategy model (RL-A-Strategy) consistently improves subtask completion over the baseline AutoPentester (A) across all the machines, gaining 21.8%. This is further supported by Table 7, where “incorrect strategy selected” errors are reduced from 4 to 2, indicating that the Strategy model improves reasoning at the planning level. With the addition of the step prediction module (RL-A-Strategy + Step), performance further increases by 11.5% on average, due to stable strategy execution. Table 7 shows that tool-related errors are fully eliminated, indicating that the step model effectively guides correct tool selection. Overall, the Strategy model improves correct strategy selection, while the step model reduces tool-selection errors and strengthens execution reliability, leading to the best overall performance as measured by subtask completion rate. 

## **6.5 Survey Analysis** 

As described in Section 5.5, we conducted a user study with 12 cybersecurity experts to qualitatively evaluate the Pen-Strategist. As illustrated in Figure 8, across the full response set, the Strategy 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Pen-Strategist: A Reasoning Framework for Penetration Testing Strategy Formation and Analysis 

**Table 6: Ablation study based on subtask completion (%) on HTB machines to measure the impact of fine-tuned models.** 

|**Machine**|**Method**|**Subtask Completion (%)**|
|---|---|---|
||A|44.44|
|Sau (6 subtasks)|RL-A-Strategy|55.58|
||RL-A-Strategy + Step|**61.11**|
||A|52.38|
|Authority (7 subtasks)|RL-A-Strategy|61.90|
||RL-A-Strategy + Step|**71.42**|
||A|50.00|
|Jarvis (6 subtasks)|RL-A-Strategy|61.11|
||RL-A-Strategy + Step|**66.67**|



**Table 7: Error analysis in the ablation study.** 

|**Error Type**|**A**|**RL-A-Strategy**|**RL-A-Str + Step**|
|---|---|---|---|
|Try tools which are not installed|1|1|0|
|Try GUI-based tools (not supported)|1|2|0|
|Incorrect strategy selected|4|2|2|
|Cannot craft the valid exploit|2|1|3|
|Other|1|3|4|



model attains a higher first-choice rate than Claude-4.6-Sonnet, exceeding it by 3.4 percentage points, and inter-participant agreement is moderately strong, with a Kendall’s W of 0.6. When focusing on the high-confidence subset, the Strategy model’s advantage becomes more pronounced, achieving a 4.8 percentage point lead in first-choice rate. In this subset, agreement also rises to 0.85, suggesting a clear and confident preference for the Strategy model over commercial LLMs. Notably, GPT-5 performs significantly worse under both settings. Overall, the findings consistently show that the Strategy model is the most preferred by experts, with Claude performing competitively. 

Below we show some example free text comments we received from the participants. Here, Options 1, 2, and 3 refer to Strategy, Claude-4.6-sonnet, and GPT-5 models, respectively. 

**Comment 1:** _"Option 2 includes several redundant checks that can be avoided, such as SUID/SGID bit checking, since we have already identified the execution behavior and privilege context of test.py and test.txt. Option 3 lacks confidence in its explanation and is less precise. It also suggests gaining script manager privileges, even though we already have access to that user. Option 1 correctly understands the key observation that test.py can be modified and is likely executed with root privileges (e.g., via a cron job). Therefore, it provides a clear and effective path to escalate privileges by modifying the script."_ 

**Comment 2:** _Option 2 identifies a strong strategy, however focuses predominantly on the enumeration of the API. Option 1 expands upon Option 2, and provides context about the importance of researching CVEs relevant to the current stack._ 

Both the comments favor our model for its clarity and stronger strategic reasoning. In Comment 1, our model is credited with correctly identifying the key exploitation path, modifying a writable script likely executed with elevated privileges, while Claude-4.6sonnet is criticized for redundant checks and GPT-5 for less confident and imprecise reasoning. In Comment 2, Claude-4.6-sonnet demonstrates a valid approach; however, it is viewed as overly 


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0011-11.png)


<!-- Start of picture text -->
Full response set High-confidence subset<br>GPT-5 GPT-5<br>5.1% 0.0%<br>Claude StrategyModel Claude47.6% StrategyModel<br>45.8% 49.2% 52.4%<br>Kendall's W = 0.6 Kendall's W = 0.85<br><!-- End of picture text -->

**Figure 8: Survey results analysis.** 

focused on enumeration, whereas our model extends this by incorporating broader contextual awareness, such as the importance of CVE research. Overall, participants emphasize our model’s ability to combine accurate technical insight with actionable, context-aware strategy compared to the other two models. 

## **6.6 Extended Experiments** 

To further evaluate the Pen-Strategist, we conduct extended experiments. 

_6.6.1_ **Evaluating Different Fine-tuning Techniques:** Here, we assess how different training strategies affect the quality of generated pentesting strategies and their explanations. As shown in Figure 9, reinforcement learning–based methods consistently outperform supervised fine-tuning (SFT) across both metrics. Among the reinforcement learning techniques, GRPO achieves the best performance, reaching 0.73 for strategy generation and 0.71 for explanation quality compared to GDPO and RLVR. SFT marginally improves the performance of the base model, indicating that naive supervised fine-tuning is insufficient for this task. This can be attributed to SFT shifting the model weights too far from their pretrained initialization, which may lead to overfitting to the training set, reduced output diversity, and diminished generalization ability for the test set [6, 17]. Overall, these results demonstrate the effectiveness of reinforcement learning approaches, with GRPO in particular providing the most substantial improvements in both strategic reasoning and explanation quality. 

_6.6.2_ **Fine-tuning Different Open-source Models:** To generalize the effectiveness of the GRPO training using the collected 


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0011-18.png)


<!-- Start of picture text -->
0.8 Strategy Explanation<br>0.6<br>0.4<br>0.2<br>0.0<br>Base SFT GDPO RLVR GRPO Base SFT GDPO RLVR GRPO<br>GEval Similarity Score<br><!-- End of picture text -->

**Figure 9: Evaluation of different training approaches for strategy generation compared to Qwen-3-14B base model, measured using GEval similarity scores.** 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Trovato et al. 

**Table 8: Performance comparison of base and fine-tuned models for strategy generation.** 

|**Model**|**Bas**|**e**|**Fine-tu**|**ned**|
|---|---|---|---|---|
||**Strategy**|**Expl.**|**Strategy**|**Expl.**|
|Qwen-3-8B-GRPO|0.16|0.32|0.33|0.50|
|Nemotron-cascade-14B|0.45|0.45|0.64|0.56|
|Mistral-3-14B|0.47|0.45|0.63|0.75|
|Qwen-3-14B-GRPO|0.39|0.45|0.74|0.72|



**Table 9: Performance comparison across models using Pass@k metrics. Here, Str. and Exp. represents GEval scores for strategy and the explanation.** 

|**Model**|**Pas**|**s@1**|**Pas**|**s@3**|**Pas**|**s@5**|
|---|---|---|---|---|---|---|
||**Str.**|**Exp.**|**Str.**|**Exp.**|**Str.**|**Exp.**|
|Claude 4.5 Sonnet|0.65|0.72|0.73|0.74|0.75|0.74|
|Gemini 2.5 Flash|0.45|0.56|0.50|0.60|0.55|0.63|
|GPT-5|0.62|0.63|0.72|0.70|0.73|0.72|
|Qwen-3-14B-GRPO (ours)|**0.73**|**0.71**|**0.75**|**0.74**|**0.77**|**0.76**|



dataset, we compare the performance of fine-tuned Qwen-3-8B [3], Nemotron-cascade-14B [28], and Mistral-3-14B-reasoning [27] models with their respective base models (similar to the experiment setup in Section 5.1). As presented in Table 8, all models benefit from fine-tuning, with Qwen-3-14B demonstrating superior overall performance across both strategy generation and explanation quality. Other models also show consistent gains, averaging 60.7% in strategy generation and 49.6% in explanation quality. Overall, GRPO fine-tuning substantially improves performance across architectures. 

_6.6.3_ **Pass@k Evaluation:** Finally, we evaluate the strategy generation performance of different models on the test set of the dataset using Pass@k metrics, where _𝑘_ represents the number of strategies generated for a sample. For instance, Pass@3 refers to generating 3 strategies and selecting the best one for GEval calculations. Table 9 shows that our Strategy consistently outperforms strong commercial baselines across all _𝑘_ values. Overall, performance increases across all models with _𝑘_ , as generating more candidate strategies increases the likelihood of including a correct solution. The superior performance of the Strategy model across all the k- cases demonstrates consistency in generating correct strategies and explanations compared to other models. Furthermore, unlike other models, the Strategy model achieves a higher Pass@1 rate, indicating its ability to generate the correct strategy in a single attempt. 

## **7 Discussion and Concluding Remarks** 

We propose Pen-Strategist, a framework to derive strategies through logical reasoning for penetration testing scenarios and predict the actions and MCP servers to execute the selected strategy. To achieve that, we collect a reasoning dataset using HTB and Vulnhub machines and fine-tune an open-source Qwen-3-14B model for strategy derivation using GRPO. Furthermore, we train a semantic-based dual-head CNN classifier to predict the next step and the MCP servers. The extensive experiments conducted demonstrate that 

fine-tuning improves the strategy derivation performance of the open-source model by 87%. Furthermore, the step model achieves 82.8% accuracy in step prediction, outperforming commercial LLMs. When integrated into frameworks such as PentestGPT, the combined strategy and step models improve subtask completion rates on HTB machines, highlighting their practical effectiveness. We further demonstrate that fine-tuning also boosts performance in related red teaming tasks, including CTF challenges, indicating strong generalization. Finally, a user study reveals that security professionals prefer the strategies generated by our model over Claude-4.6-Sonnet by a margin of 4.8%. Next, we discuss the general comments, limitations, and future work. 

**Local Models for Data Privacy:** The Pen-Strategist framework can be locally deployed and enables on-premise pentesting strategy and step formulation without exposing sensitive system information or vulnerabilities to third-party LLMs. This significantly enhances data privacy for enterprises, addressing a key concern in automated pentesting. More specifically, the Qwen-3-14B model we finetuned can be deployed on a single GPU with 80GB VRAM, representing a substantially lower hardware requirement compared to larger models. However, results from HTB experiments indicate that even fine-tuned LLMs continue to struggle with identifying correct strategies in certain pentesting tasks, primarily due to limited model scale and insufficient training on relevant data and scenarios. Scaling to larger open-source models, such as Qwen-3-235B [9], and fine-tuning them on more comprehensive datasets is likely to yield improved performance. In such cases, however, local deployment will require more compute. 

**MCP Classifier and Recent Developments:** In our approach, the step model functions as both an action predictor and an MCP server classifier, helping to minimize incorrect tool usage. Alternatively, one could define Claude Code skills [4] that guide an LLM to execute the chosen steps directly, removing the need for a separate MCP selection classifier. However, this shifts full responsibility to the LLM’s decision-making, which may introduce errors, as reflected by the relatively low F1 scores of other LLMs in Table 3. Furthermore, it may hallucinate the use of unavailable tools or may try to install them, and therefore requires guardrails to ensure safe execution and protect privacy within the environment. A similar behavior was observed in the recent OpenClaw [29] agent, where the system incurs substantial token costs due to looping in incorrect strategies and attempting to use unavailable tools. In contrast, our approach provides a more constrained and structured environment covering the most commonly used pentesting tools, while still allowing flexibility to add more based on the specific needs of the pentester. **Dataset Extension:** Our dataset currently includes samples from only 240 vulnerable machines, primarily due to constraints in time and human effort. However, by releasing it publicly, we enable others to expand it with additional human-curated entries following the same format, thereby improving its scale and utility for training further reasoning models for security. Moreover, this approach can be extended to develop more general red and blue teaming models by incorporating reasoning data from related tasks such as log analysis, digital forensics, and software security analysis. 

In conclusion, although much of the existing work emphasizes agentic systems for automating security tasks, a major limitation is the model’s ability to reason logically and systematically about 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Pen-Strategist: A Reasoning Framework for Penetration Testing Strategy Formation and Analysis 

current findings to determine the next strategy. Another challenge lies in executing these strategies while respecting the constraints of the execution environment. To this end, we proposed Pen-Strategist, consisting of two models, strategy and step, which together lead to significant performance improvements in pretesting strategy formation and across a range of security tasks. 

## **References** 

- [1] Hessa Mohammed Zaher Al Shebli and Babak D Beheshti. 2018. A study on penetration testing process and tools. In _2018 IEEE Long Island Systems, Applications and Technology Conference_ . 1–7. 

- [2] Alibaba Cloud. 2025. Qwen3-14B. https://huggingface.co/Qwen/Qwen3-14B. 

- [3] Alibaba Cloud. 2025. Qwen3-8B. https://huggingface.co/Qwen/Qwen3-8B. 

- [4] Anthropic. 2025. Agent Skills Overview. https://platform.claude.com/docs/en/ agents-and-tools/agent-skills/overview. 

- [5] Anthropic. 2026. Claude Code. https://code.claude.com/docs/en/quickstart. 

- [6] Gregor Bachmann and Vaishnavh Nagarajan. 2024. The pitfalls of next-token prediction. _arXiv preprint arXiv:2403.06963_ (2024). 

- [7] Dipkamal Bhusal, Md Tanvirul Alam, Le Nguyen, Ashim Mahara, Zachary Lightcap, Rodney Frazier, Romy Fieblinger, Grace Long Torales, Benjamin A Blakely, and Nidhi Rastogi. 2024. SECURE: Benchmarking large language models for cybersecurity. In _2024 Annual Computer Security Applications Conference (ACSAC)_ . IEEE, 15–30. 

- [8] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, et al. 2020. Language models are few-shot learners. _Advances in Neural Information Processing Systems_ 33 (2020), 1877–1901. 

- [9] Alibaba Cloud. 2025. Qwen/Qwen3-235B-A22B · Hugging Face. https:// huggingface.co/Qwen/Qwen3-235B-A22B 

- [10] Wei Dai, Peilin Chen, Chanakya Ekbote, and Paul Pu Liang. 2025. QoQ-Med: Building multimodal clinical foundation models with domain-aware GRPO training. _arXiv preprint arXiv:2506.00711_ (2025). 

- [11] Xin Dai, Buqiang Xu, Zhenghao Liu, Yukun Yan, Huiyuan Xie, Xiaoyuan Yi, Shuo Wang, and Ge Yu. 2025. Legal Δ: Enhancing legal reasoning in LLMs via reinforcement learning with chain-of-thought guided information gain. _arXiv preprint arXiv:2508.12281_ (2025). 

- [12] Gelei Deng, Yi Liu, Víctor Mayoral-Vilches, Peng Liu, Yuekang Li, Yuan Xu, Tianwei Zhang, Yang Liu, Martin Pinzger, and Stefan Rass. 2024. PentestGPT: Evaluating and harnessing large language models for automated penetration testing. In _33rd USENIX Security Symposium (USENIX Security 24)_ . 847–864. 

- [13] FedRAMP. 2024. FedRAMP Penetration Test Guidance. https: //www.fedramp.gov/assets/resources/documents/CSP_Penetration_Test_ Guidance_public_comment.pdf. 

- [14] Yasod Ginige, Akila Niroshan, Sajal Jain, and Suranga Seneviratne. 2025. Autopentester: An LLM agent-based framework for automated pentesting. In _2025 IEEE 24th International Conference on Trust, Security and Privacy in Computing and Communications (TrustCom)_ . IEEE, 163–174. 

   - [25] Yang Liu, Dan Iter, Yichong Xu, Shuohang Wang, Ruochen Xu, and Chenguang Zhu. 2023. G-Eval: NLG evaluation using GPT-4 with better human alignment. In _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing_ . 2511–2522. 

   - [26] Zhaowei Liu, Xin Guo, Zhi Yang, Fangqi Lou, Lingfeng Zeng, Jinyi Niu, Mengping Li, Qi Qi, Zhiqiang Liu, Yiyang Han, et al. 2025. Fin-R1: A large language model for financial reasoning through reinforcement learning. _arXiv preprint arXiv:2503.16252_ (2025). 

   - [27] Mistral AI. 2025. Ministral-3-14B-Reasoning-2512. https://huggingface.co/ mistralai/Ministral-3-14B-Reasoning-2512. 

   - [28] NVIDIA. 2026. Nemotron-Cascade-14B-Thinking. https://huggingface.co/nvidia/ Nemotron-Cascade-14B-Thinking. 

   - [29] openclaw. 2025. GitHub - openclaw/openclaw: Your own personal AI assistant. Any OS. Any Platform. The lobster way. https://github.com/openclaw/openclaw 

   - [30] Zhongxi Qiu, Zhang Zhang, Yan Hu, Heng Li, and Jiang Liu. 2025. Open-MedicalR1: How to choose data for RLVR training at medicine domain. _arXiv preprint arXiv:2504.13950_ (2025). 

   - [31] Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D Manning, Stefano Ermon, and Chelsea Finn. 2023. Direct preference optimization: Your language model is secretly a reward model. _Advances in Neural Information Processing Systems_ 36 (2023), 53728–53741. 

   - [32] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al. 2024. DeepSeekMath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ (2024). 

   - [33] Xiangmin Shen, Lingzhi Wang, Zhenyuan Li, Yan Chen, Wencheng Zhao, Dawei Sun, Jiashui Wang, and Wei Ruan. 2025. Pentestagent: Incorporating LLM agents to automated penetration testing. In _Proceedings of the 20th ACM Asia Conference on Computer and Communications Security_ . 375–391. 

   - [34] Gemini Team, Rohan Anil, Sebastian Borgeaud, Jean-Baptiste Alayrac, et al. 2023. Gemini: A family of highly capable multimodal models. _arXiv preprint arXiv:2312.11805_ (2023). 

   - [35] Xumeng Wen, Zihan Liu, Shun Zheng, Shengyu Ye, Zhirong Wu, Yang Wang, Zhijian Xu, Xiao Liang, Junjie Li, Ziming Miao, et al. 2025. Reinforcement learning with verifiable rewards implicitly incentivizes correct reasoning in base LLMs. _arXiv preprint arXiv:2506.14245_ (2025). 

   - [36] Yiran Wu, Mauricio Velazco, Andrew Zhao, Manuel Raúl Meléndez Luján, Srisuma Movva, Yogesh K Roy, Quang Nguyen, Roberto Rodriguez, Qingyun Wu, Michael Albada, et al. 2025. ExCyTIn-Bench: Evaluating LLM agents on cyber threat investigation. _arXiv preprint arXiv:2507.14201_ (2025). 

   - [37] Jiacen Xu, Jack W Stokes, Geoff McDonald, Xuesong Bai, David Marshall, Siyue Wang, Adith Swaminathan, and Zhou Li. 2024. AutoAttacker: A large language model guided system to implement automatic cyber-attacks. _arXiv preprint arXiv:2403.01038_ (2024). 

   - [38] Hao Zhang, Tingmin Wu, Tianqing Zhu, Sheng Wen, and Yang Xiang. 2025. CyberLlama: A fine-tuned large language model for cybersecurity named entity recognition. _Knowledge-Based Systems_ (2025), 114183. 

- [15] Yasod Ginige, Bhanuka Silva, Thilini Dahanayaka, and Suranga Seneviratne. 2025. TrafficLLM: LLMs for improved open-set encrypted traffic analysis. _Computer Networks_ (2025), 111847. 

- [16] Hack The Box. 2024. Hack The Box. https://www.hackthebox.com/. 

- [17] Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, and Yejin Choi. 2020. The Curious Case of Neural Text Degeneration. In _International Conference on Learning Representations_ . 

- [18] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Liang Wang, and Weizhu Chen. 2022. LoRA: Low-rank adaptation of large language models. In _International Conference on Learning Representations_ . 

- [19] Zhenguo Hu, Razvan Beuran, and Yasuo Tan. 2020. Automated penetration testing using deep reinforcement learning. In _IEEE European Symposium on Security and Privacy Workshops (EuroS&PW)_ . 2–10. 

- [20] Zimo Ji, Daoyuan Wu, Wenyuan Jiang, Pingchuan Ma, Zongjie Li, and Shuai Wang. 2025. Measuring and augmenting large language models for solving capture-the-flag challenges. In _Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security_ . 603–617. 

- [21] He Kong, Die Hu, Jingguo Ge, Liangxiong Li, Tong Li, and Bingzhen Wu. 2025. Vulnbot: Autonomous penetration testing for a multi-agent collaborative framework. _arXiv preprint arXiv:2501.13411_ (2025). 

- [22] Solomon Kullback. 1951. Kullback–Leibler divergence. _Encyclopedia of Machine Learning_ (1951), 581–583. 

- [23] Gordon H Lewis and Richard G Johnson. 1971. Kendall’s Coefficient of Concordance for sociometric rankings with self excluded. _Sociometry_ (1971), 496–503. 

- [24] Shih-Yang Liu, Xin Dong, Ximing Lu, Shizhe Diao, Peter Belcak, Mingjie Liu, Min-Hung Chen, Hongxu Yin, Yu-Chiang Frank Wang, Kwang-Ting Cheng, et al. 2026. GDPO: Group reward-decoupled normalization policy optimization for multi-reward RL optimization. _arXiv preprint arXiv:2601.05242_ (2026). 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Trovato et al. 

## **A Open Science** 

We published our dataset and codes in an anonymous GitHub repository (https://anonymous.4open.science/r/Pentest-Strategist-B783/). More specifically, it contains the following components. 

- The dataset 

- Automated dataset collection code 

- Training code for the strategy and the step models 

- Codes for the experiments 

- Anonymised survey results and analysis code. 

The repository contains README files for each section, which guide users to set up the Python environment and run the experiments. Please follow those steps to execute the code successfully. 

## **B Ethical Considerations** 

The survey received formal approval from our University’s Ethics Committee following a comprehensive review process. Additionally, all responses were collected anonymously (without any personal details), and informed consent was obtained from participants via a dedicated form. As a result, the study fully complies with the University’s ethical guidelines, which are designed to international standards. 

As this work presents a framework for strategy generation in penetration testing, supported by a dataset collected from simulated public platforms such as Hack-The-Box and VulnHub, we do not identify any potential risks to society arising from this research. 

## **C Prompts** 

This section presents the complete prompts used during model fine-tuning and evaluation of the Pen-Strategist framework. 

## **System Prompt** 


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0014-16.png)


**Figure 10: System prompt used for the Strategy model finetuning.** 

Figure 10 presents the system prompt used during both finetuning and inference of the Strategy model. As described in Section 4.2.1, the model is fine-tuned to act as a domain-specific penetration testing strategist. The system prompt instructs the model to derive a new strategy for the next pentesting step based on the current attack environment state, and specifies the required output format: a brief chain-of-thought reasoning enclosed in <think> tags followed by the final strategy. The reasoning phase is capped at 512 tokens, consistent with the generation length reward _𝑅𝑙_ defined in Section 4.2.1, which penalizes outputs exceeding the maximum token count to prevent reasoning explosion during training. 

## **User Prompt** 


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0014-20.png)


**Figure 11: User prompt used for the Strategy model finetuning.** 

Figure 11 presents the user prompt, which provides the structured input context for each training instance, as described in Section 4.1.3. Specifically, it supplies three input fields drawn from the dataset: the PenTest Tree (PTT), which summarizes the current attack state including previously executed steps and their findings; the Previous Step, representing the most recent action performed; and the Previous Step Result, containing the observed output of that action. 

## **Reward Model Prompt** 

Figure 12 presents the reward model prompt used during GRPO finetuning to compute the semantic and logical similarity reward _𝑅𝑠_ , as defined in Section 4.2.1. It instructs GPT-4o, acting as the evaluator in the G-Eval framework [25], to score a generated strategy against the ground-truth strategy along four independent criteria: (i) logical alignment with the ground-truth rationale, (ii) coverage of essential technical terms and entities, (iii) consistency of the final decision given the context, and (iv) use of equivalent tools or techniques. Each criterion is scored on a scale from −2 to +2, and the final reward is computed as the average across all four criteria. 

## **Survey Scenario** 

Figure 13 presents a representative scenario from the user study described in Section 5.5. Each scenario consists of a pentesting context summarizing the findings at the current exploitation state, followed by three anonymized strategy outputs generated by the Strategy model, Claude-4.6-Sonnet, and GPT-5, respectively. Participants were asked to rank the three strategies from best to worst based on logical correctness and alignment with the given task, as described in Section 5.5. In this example, Option 1 (Strategy model) correctly identifies that test.py is executed by root via a scheduled task and 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Pen-Strategist: A Reasoning Framework for Penetration Testing Strategy Formation and Analysis 


![](images/04-pen-strategist-a-reasoning-framework-for-penetration.pdf-0015-02.png)


derives a precise privilege escalation path through script modification, while Option 2 (Calude-4.6-Sonnet) includes redundant checks such as SUID/SGID bit verification that are unnecessary given the established execution context, and Option 3 (GPT-5) lacks precision in identifying the exploitation vector. 

Received 20 February 2007; revised 12 March 2009; accepted 5 June 2009 

**Figure 12: Reward model prompt used to evaluate the derived strategy by comparing generated and ground-truth strategies in the strategy model finetuning.** 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Trovato et al. 

|**Reconnaissance Phase Completed:**<br>- Conducted passive and active information gather<br>latency of 0.70s.<br>- Performed a port scan revealing Port 80/tcp as o<br>**HTTP Service Enumeration:**<br>- Enumerated directories using a wordlist, discover<br>`/dev`, and `/js`.<br>- Explored the `/dev` directory, finding two PHP file<br>- Successfully exploited the PHP files to gain shell<br>connection.<br>**Privilege Escalation Phase Initiated:**<br>- Checked user privileges for `www-data`, revealin<br>password.<br>- Explored server files, identifying a notable `scripts<br>**Current Exploration:**<br>- Attempted to switch to the `scriptmanager` user a<br>as the directory was not found in the current path.<br>- Found two files in the `scripts` directory: `test.py`<br>(containing "testing 123!"), with permissions indicatin<br>by root.<br>**Option 1**<br>**Strategy derivation:**<br>Looking at the previous step results, there's a critical<br>observation: test.py is owned by scriptmanager but test.txt is<br>owned by root. This suggests that test.py is being executed<br>by root (likely via a cron job or scheduled task), which is why<br>the output file test.txt has root ownership.<br>This is a classic privilege escalation vector:<br>1. We have sudo privileges to run commands as<br>scriptmanager (no password required)<br>2. We can modify test.py (owned by scriptmanager with rw<br>permissions)<br>3. test.py appears to be executed automatically by root<br>(evidenced by root-owned output)<br>The strategy should be to:<br>1. First, switch to scriptmanager user using our sudo<br>privileges<br>2. Modify test.py to include a reverse shell or privilege<br>escalation payload<br>3. Wait for the automated execution (likely a cron job) to run<br>the script as root<br>4. Gain root access<br>**Final strategy:**<br>1.4.4 Exploit automated script execution for privilege<br>escalation<br>Since test.py is owned by scriptmanager but creates files<br>owned by root, this indicates the script is being executed by<br>root automatically (likely via cron). Exploit this by:<br>1. Switch to scriptmanager user: `sudo -u scriptmanager<br>/bin/bash`<br>2. Modify test.py to include a reverse shell payload that will<br>execute as root<br>3. Set up a new netcat listener on the attacking machine<br>(different port, e.g., 5555)<br>4. Replace test.py content with a Python reverse shell<br>connecting to attacker IP<br>5. Wait for the automated execution (monitor for incoming<br>connection)|**Pentest Scenario**<br>ing, identifying the target IP (10.129.237.16) as active with a<br>pen, running Apache HTTPD 2.4.18 (Ubuntu).<br>ing several paths including `/images`, `/uploads`, `/php`, `/css`,<br>s: `phpbash.min.php` and `phpbash.php`.<br>access as the `www-data` user, establishing a reverse shell<br>g the ability to run commands as `scriptmanager` without a<br>` directory owned by `scriptmanager` with specific permissions<br>nd navigate to the `scripts` directory but encountered an issue<br>(a script writing "testing 123!" to `test.txt`) and `test.txt`<br>g `test.py` is writable by `scriptmanager` and `test.txt` is owned<br>**Option 2**<br>**Strategy:**<br>Exploit potential vulnerabilities within the `test.py` script or<br>use it as a stepping stone to escalate privileges from the<br>compromised `www-data` user.<br>**Steps:**<br>1. Analyze `test.py`:<br>- Inspect the code of `test.py` to identify if it contains any<br>insecure functionalities, such as hardcoded credentials,<br>misconfigured logging, or unintended side effects when<br>executed with elevated privileges.<br>2. Check for SUID/SGID Bits:<br>- Verify if any files in `/scripts` have the setuid/setgid bits<br>enabled, which could allow execution with higher privileges.<br>3. Test Execution of `test.py`:<br>- Execute `test.py` under different contexts (e.g., as `root`,<br>via cron jobs, or through web access) to observe its behavior<br>and check if it leads to privilege escalation.<br>4. Look for Path Manipulation or Environment Variables:<br>- Search for environment variables that might be<br>manipulated to execute arbitrary code when `test.py` runs.<br>5. Consider Web Context:<br>- If the target has exposed web endpoints related to<br>`/scripts`, attempt to trigger `test.py` via a crafted request to<br>see if it behaves differently than locally.<br>6. Escalate Privileges via Sudo Rights:<br>- Since `www-data` has sudo rights, focus on escalating<br>from there first before moving into other users.<br>7. Review System Logs:<br>- Look for clues in system logs (if accessible) regarding<br>failed login attempts or processes that might indicate<br>misconfigurations.|.<br> <br>**Option 3**<br>The previous reconnaissance and privilege escalation steps<br>provided key insights. We have accessed the 'scripts'<br>directory intended for the 'scriptmanager' user, revealing files<br>with varied permissions. 'test.py' is an interesting target<br>because itâ��s owned by 'scriptmanager' and reveals an<br>execution purpose (writing to 'test.txt'). Privilege escalation<br>can be approached by leveraging the library and execution<br>environment for this Python script.<br>Given the file 'test.py' is writable but executed potentially by a<br>more privileged user, modifying it to execute commands as<br>the 'scriptmanager' user might allow us to gain higher<br>privilege access. The presence of a command that writes to a<br>root-owned file (â��test.txtâ��) suggests execution under<br>different privilege contexts, potentially with the desired higher<br>privileges by 'scriptmanager'.<br>Preparation for this next step includes:<br>1. Verifying execution contexts or triggering conditions.<br>2. Preparing a backdoor or alternative command within<br>'test.py' to escalate privileges or explore further.<br>3. Managing access to quickly test modifications in 'test.py'.<br>4. Checking periodic execution schedules (cron jobs) that<br>might allow leveraging the modified script.<br>Focus on gaining 'scriptmanager' privileges to increase<br>system control, permitting further system exploration or<br>access.<br>**Final strategy:**Modify 'test.py' within /scripts to include a<br>command that provides a backdoor (e.g., spawn a reverse<br>shell) or logs 'scriptmanager' credentials. Check for<br>automated execution (potential cron jobs) or manually trigger<br>execution if possible, leveraging its writable status to gain<br>'scriptmanager' privileges, facilitating further exploration and<br>potential root access|
|---|---|---|



**Figure 13: A sample scenario given in the survey. Here Option 1,2, and 3 are generated using our strategy model, Claude-4.6Sonnet, and GPT-5 respectively.** 

