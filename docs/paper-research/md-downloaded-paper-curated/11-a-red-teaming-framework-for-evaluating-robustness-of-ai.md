# **A Red Teaming Framework for Evaluating Robustness of AI-enabled Security Orchestration, Automation, and Response Systems**

## Table of Contents

  - [Abstract](#abstract)
- [1 INTRODUCTION](#1-introduction)
- [2 LITERATURE REVIEW](#2-literature-review)
  - [2.1 Cyber Operations Simulation Environments](#2-1-cyber-operations-simulation-environments)
  - [2.2 Large Language Models for Cybersecurity](#2-2-large-language-models-for-cybersecurity)
  - [2.3 Reinforcement Learning for Cyber Operations](#2-3-reinforcement-learning-for-cyber-operations)
  - [2.4 Hybrid Architectures and Research Gap](#2-4-hybrid-architectures-and-research-gap)
- [3 Methodology](#3-methodology)
  - [3.1 Problem Formulation](#3-1-problem-formulation)
  - [3.2 Hierarchical LLM–RL Architecture](#3-2-hierarchical-llm-rl-architecture)
  - [3.3 State and Intent Representation](#3-3-state-and-intent-representation)
  - [3.4 Hierarchical Reward Shaping](#3-4-hierarchical-reward-shaping)
  - [3.5 Policy Learning](#3-5-policy-learning)
  - [3.6 Memory and Adaptation](#3-6-memory-and-adaptation)
- [4 Experiments](#4-experiments)
  - [4.1 Environment](#4-1-environment)
  - [4.2 Red Agent Configurations](#4-2-red-agent-configurations)
  - [4.3 Training Details](#4-3-training-details)
  - [4.4 Evaluation Protocol and Metrics](#4-4-evaluation-protocol-and-metrics)
  - [4.5 Experimental Design](#4-5-experimental-design)
  - [4.6 Implementation Details](#4-6-implementation-details)
- [5 Results](#5-results)
  - [5.1 Evaluation of the Hierarchical LLM-RL Red Teaming Framework](#5-1-evaluation-of-the-hierarchical-llm-rl-red-teaming-framework)
  - [5.2 Comparison with Standalone LLM Agents](#5-2-comparison-with-standalone-llm-agents)
  - [5.3 Comparison with RL-only Agents](#5-3-comparison-with-rl-only-agents)
  - [5.4 Key Insights](#5-4-key-insights)
- [6 CONCLUSION](#6-conclusion)
- [Acknowledgments](#acknowledgments)
- [References](#references)

---

Ayan Javeed Shaikh<sup>a</sup> , Nathaniel D. Bastian<sup>b</sup> , and Ankit Shah<sup>∗a</sup>

> aIndiana University, Bloomington, IN, United States

> bUnited States Military Academy, West Point, NY, United States

### **Abstract**

> AI-enabled Security Orchestration, Automation, and Response (SOAR) systems increasingly employ autonomous agents for cyber defense, yet their resilience to adaptive adversaries is underexplored. We introduce an autonomous red teaming framework that integrates large language models (LLMs) with reinforcement learning (RL) to generate adaptive, multi-stage attack campaigns against autonomous defenders in enterprise networks. A hierarchical design combines an LLM-based planner for strategic intent with an RL controller for tactical execution, supported by reward shaping aligned with kill-chain progression. Evaluation in a high-fidelity enterprise simulation demonstrates the effectiveness of the proposed approach, while also showing that standalone LLM agents fail to sustain multi-stage attack campaigns and that domain-specific cybersecurity models achieve only limited levels of compromise, highlighting the necessity for hybrid LLM-RL approaches to red teaming.

> **Keywords:** Red Teaming, Large Language Models, Reinforcement Learning, Cybersecurity, SOAR System

---

## **1 INTRODUCTION**

Cyber threats targeting enterprise networks continue to increase in both frequency and sophistication, with recent industry telemetry reporting on the order of approximately two thousand weekly attacks per organization globally in 2025, reflecting a sustained upward trend in adversarial activity [1]. In response, enterprises are increasingly adopting Security Orchestration, Automation, and Response (SOAR) systems that leverage artificial intelligence (AI) to enable autonomous threat detection, incident response, and policy enforcement at machine speed [2]. However, despite their growing deployment, these AI-enabled SOAR systems are not yet rigorously stress-tested against adaptive and strategic adversaries. Traditional penetration testing and rule-based red team scripts fail to capture the dynamic, multi-step nature of real-world attack campaigns, leaving a critical gap in evaluating the robustness of AI-enabled cyber defense systems [3]. Autonomous red teaming, where an AI agent emulates an attacker following structured kill-chain behaviors such as reconnaissance, initial access, privilege escalation, lateral movement, and impact [4], offers a principled approach to closing this gap.

Recent advances in large language models (LLMs) have demonstrated strong capabilities for autonomous offensive cybersecurity tasks, including vulnerability discovery, threat reasoning, and multi-step attack plan-

> ∗Corresponding author: ankit@iu.edu

A Red Teaming Framework for Evaluating Robustness of AI-enabled Security Orchestration, Automation, and Response Systems A Prepprint

A Prepprint

ning [3, 5]. Domain-specific models such as Cisco’s Foundation-Sec-8B [6] and DeepHat-7B, formerly WhiteRabbitNeo [7], further improve structured reasoning in adversarial settings through security-focused finetuning. In parallel, reinforcement learning (RL) enables red teaming via interaction-driven policy optimization, learning sequential attack strategies that maximize long-horizon objectives in dynamic environments [8]. However, both paradigms exhibit fundamental limitations when applied independently to autonomous red teaming. LLM-based agents struggle with long-horizon state tracking, action consistency, and adaptation through environment feedback, while RL-based agents are constrained by sample inefficiency, limited interpretability, and poor generalization across heterogeneous cyber environments [9].

To address these limitations, we propose a hierarchical hybrid framework that integrates LLM-based strategic planning with RL-based tactical execution for red team operations. The LLM acts as a high-level planner that generates attack objectives, selects strategies, and modulates risk posture, while an RL controller executes low-level actions conditioned on environment state and planner directives. The LLM is kept frozen during training to preserve external knowledge, while RL optimizes execution policies through interaction. Optionally, a Reflexion mechanism [10] enables iterative strategic refinement via episodic memory without parameter updates.

We evaluate our approach in the Cyber Operations Research Gym (CybORG) CAGE Challenge 4 environment [11, 12], a U.S. government–sponsored evaluation setting. CAGE 4 is a high-fidelity enterprise network simulation featuring partial observability, long-horizon decision-making, and adaptive defensive responses. The environment includes five coordinated blue team defenders powered by the Hierarchical Multi-Agent Reinforcement Learning (H-MARL) Expert policy,[13] the strongest published autonomous defender for this setting, making it a rigorous benchmark for evaluating robustness under realistic adversarial conditions.

The key contributions of our work are as follows. We present a hierarchical LLM–RL architecture for autonomous red teaming that decouples strategic planning (LLM) from tactical execution (RL), enabling structured interaction between high-level intent generation and low-level environment-grounded control. We further introduce a kill-chain-aligned RL framework that incorporates structured reward shaping to guide long-horizon adversarial behavior consistent with MITRE ATT&CK stages. In addition, we provide a comprehensive empirical study of LLMs across multiple families, including Qwen3, Llama, reasoning specialists such as DeepSeek-R1, and domain-specialized cybersecurity models such as Foundation-Sec and DeepHat, and across a wide parameter range (0.6B to 70B), revealing systematic limitations of standalone LLM agents in sustaining long-horizon cyber operations against adaptive autonomous defenders. Finally, we conduct an extensive evaluation in the CAGE 4 environment demonstrating the effectiveness of the proposed hybrid architecture under partial observability and multi-agent defender dynamics.

The remainder of this paper is organized as follows. Section 2 reviews related work in autonomous cyber operations, LLMs for cybersecurity, and hybrid LLM–RL architectures. Section 3 presents the proposed red teaming framework. Section 4 describes the experimental setup. Section 5 reports the results and compares the proposed approach with standalone LLM and RL baselines. Section 6 concludes with a discussion of limitations and directions for future work.

---

## **2 LITERATURE REVIEW**

This section reviews three bodies of literature that converge on the problem of autonomous red teaming: simulation environments for cyber operations, LLM applications in cybersecurity, and reinforcement learning for cyber agents. We then identify the gap that motivates our hierarchical architecture.

### **2.1 Cyber Operations Simulation Environments**

Evaluating autonomous cyber agents requires simulation environments that model realistic network topologies, multi-agent interaction, and partial observability. Several platforms have been developed to address this need. Microsoft’s CyberBattleSim[14] provides a high-level abstraction of enterprise networks focused on post-breach lateral movement, using an OpenAI Gym interface to train RL agents; however, its abstract nature limits the fidelity of defensive responses. FARLAND[15] (Framework for Advanced Reinforcement Learning for Autonomous Network Defense), a MITRE–NSA collaboration, supports progressive complexity scaling and software-defined network reconfiguration for blue agent training, but focuses exclusively on defensive operations. CybORG[11] introduced a dual-mode research gym, combining low-fidelity simulation for rapid training with high-fidelity emulation on real virtual machines supporting both red and blue team agents through an OpenAI Gym-compatible interface. Early experiments with Deep Double Q-Network


A Red Teaming Framework for Evaluating Robustness of AI-enabled Security Orchestration, Automation, and Response Systems A Prepprint

A Prepprint

(DDQN) agents demonstrated that RL could learn effective policies for simplified capture-the-flag scenarios within CybORG’s simulation mode, but these experiments were limited to small networks with a single subnet and few hosts.

The CAGE Challenge series, built on CybORG, has progressively increased scenario complexity from single-subnet defense (CAGE 1) through enterprise-scale multi-agent operations (CAGE 4)[12]. CAGE 4 represents the most demanding configuration in the series: a multi-subnet enterprise network with coordinated blue team defenders operating across 500-step episodes under partial observability. Each episode features active defensive responses including host restoration, network isolation, and deception deployment that require the red agent to adapt its strategy in real time. CybORG has emerged as the standard benchmark for autonomous cyber agent research,[2, 9] and we adopt CAGE 4 as the primary evaluation environment for this work.

### **2.2 Large Language Models for Cybersecurity**

The application of LLMs to cybersecurity has expanded rapidly across multiple domains. On the offensive side, LLM-driven penetration testing tools have demonstrated that language models can assist with vulnerability discovery and exploitation. PentestGPT[16] introduced a three-module architecture (Reasoning, Generation, and Parsing) that decomposes penetration testing into subtasks, achieving a 228.6% task-completion improvement over GPT-3.5 baselines and earning the Distinguished Artifact Award at USENIX Security 2024. Another representative line of work includes WhiteRabbitNeo, a family of cybersecurity-focused generative models designed for offensive and defensive security tasks, which has evolved into the more recent DeepHat system, extending its capability toward uncensored red-team automation and improved inference efficiency in practical security operations [7]. HackSynth[17] proposed a dual-module Planner-Summarizer architecture for autonomous CTF challenges, demonstrating that iterative command generation and feedback processing can solve challenges across diverse domains. Rigaki et al.[18] evaluated pre-trained LLMs as attacking agents in the NetSecGame environment using ReACT-style prompting, finding that zero-shot LLM agents achieve comparable or superior performance to RL agents trained for thousands of episodes in most scenarios. However, these systems rely on LLM reasoning alone without learned tactical policies, limiting their effectiveness in environments that require precise multi-step execution under active defense.

Domain-specialized security models have shown that targeted fine-tuning can close the performance gap with much larger general-purpose models. Foundation-Sec-8B[6] was trained on cybersecurity corpora including MITRE ATT&CK mappings and threat intelligence datasets, achieving strong performance on security reasoning tasks at the 8B-parameter scale. Levi et al.[19] introduced CyberPal 2.0, a family of cybersecurityexpert small language models (4B–20B parameters) that match or exceed GPT-4o on vulnerability-weakness correlation benchmarks, demonstrating that domain specialization at modest model sizes is viable for security applications. A notable finding from their work is that fine-tuning a base model yields 2.7 _×_ larger performance gains compared to fine-tuning an already instruction-tuned model, with direct implications for domain-specific LLM adaptation strategies. Yang et al.[5] proposed a dual-model collaborative architecture for Advanced Persistent Threat (APT) detection that iteratively refines threat assessments through multi-LLM reasoning aligned with MITRE ATT&CK tactics, achieving F1 scores exceeding up to 99.20% on standard APT detection datasets.

Despite these advances, LLMs face fundamental limitations as standalone autonomous cyber agents. Castro et al.[9] evaluated LLM-based blue team agents in CAGE 4 and found that all-LLM teams achieved mean rewards approximately five times worse than all-RL teams ( _−_ 2 _,_ 547 vs. _−_ 493) while operating at roughly 1 _/_ 104th the decision-making speed. LLMs struggle with precise state tracking over hundreds of sequential decisions, exhibit action-repetition loops when operating in interactive environments, and cannot learn from trial-and-error interaction within a specific operational context. These findings motivate the search for architectures that preserve LLM reasoning capabilities while addressing their tactical execution limitations.

### **2.3 Reinforcement Learning for Cyber Operations**

Reinforcement learning has been applied to both offensive and defensive cyber operations, leveraging its ability to learn optimal sequential decision-making policies through environment interaction. The CAGE Challenge series has driven the development of increasingly sophisticated RL approaches. The Cybermonic KEEP submission[20] employed graph convolutional networks (GCNs) with self-attention to process network


A Red Teaming Framework for Evaluating Robustness of AI-enabled Security Orchestration, Automation, and Response Systems A Prepprint

A Prepprint

topology as graph states, optimizing independent actor-critic agents per zone using PPO. Singh et al.[13] proposed a hierarchical PPO architecture for CAGE 4 that decomposes the cyber defense task into specialized sub-policies for network investigation and host recovery, achieving top convergence speed and episodic return among CAGE 4 blue team submissions while enabling policy transfer across adversarial behavior shifts. We adopt their H-MARL Expert policy as the blue team defender in our evaluation, ensuring our red team agent is tested against the strongest published autonomous defense.

However, RL for cyber operations faces persistent challenges. Pure RL agents require extensive training episodes to explore the large state-action space of realistic network environments, exhibit limited transferability across different network configurations, and produce opaque policies that resist human interpretation [9]. The sparse reward structure of cyber operations where meaningful outcomes such as host compromise or service degradation occur only after long sequences of prerequisite actions exacerbates sample inefficiency and makes credit assignment difficult. Reward shaping aligned with domain knowledge (e.g., MITRE ATT&CK kill chain progression) has been shown to improve RL training stability, but introduces the risk of reward hacking if not carefully constrained.[3]

On the offensive side, RL based red team agents remain significantly underexplored compared to defensive applications. The agentic security survey by Shahriar et al.[2] found that only eight of over 160 surveyed papers employed RL or preference-based learning in security agent systems, and the vast majority of existing work focuses on defense rather than attack. This asymmetry is notable because robust evaluation of autonomous defenses requires equally capable autonomous adversaries precisely the capability our framework aims to provide.

### **2.4 Hybrid Architectures and Research Gap**

The complementary strengths and weaknesses of LLMs and RL have motivated growing interest in hybrid architectures across AI research. LLMs provide rich domain knowledge, strategic reasoning, and natural language explainability, but cannot learn from environment interaction. RL agents learn effective policies through trial and error, but require extensive training, produce opaque decisions, and struggle with longhorizon planning in the absence of domain priors.

Several works have begun exploring combinations of these paradigms in the cybersecurity domain. Castro et al.[9] evaluated mixed teams of LLM and RL agents for blue team defense in CAGE 4, finding that heterogeneous teams, one LLM agent coordinating with four RL agents, could leverage both the reasoning capabilities of LLMs and the execution speed of RL. However, their approach combines agents at the _team level_ , assigning LLM and RL roles to different agents, rather than integrating both paradigms within a single agent’s decision-making pipeline. Tholl et al.[21] investigated LLM integration with RL for autonomous cyber operations using the CAGE Challenge environment, finding that LLM-augmented reward shaping and action feedback can accelerate RL training and improve initial policy quality. Their work provides early evidence that LLMs can enhance RL-based cyber agents, though their integration operates at the reward and feedback level rather than through a structured planning hierarchy.

In the broader AI agent literature, hierarchical architectures that separate high-level planning from low-level control have shown success across robotics, game playing, and navigation tasks. The Reflexion framework[10] demonstrated that LLM agents can improve their performance through verbal self-reflection and episodic memory without requiring weight updates, establishing the viability of learning-without-training paradigms for language model agents. The planner-executor pattern identified as the most common architecture in security agents[2] typically uses LLMs for both planning and execution layers, missing the opportunity to leverage RL for adaptive tactical execution.

To the best of our knowledge, no prior work has proposed a hierarchical architecture that uses a frozen LLM as a strategic planner providing structured intent to a trainable RL controller for autonomous red team operations on AI-enabled cyber defense systems. While Singh et al.[13] employ a hierarchical decomposition for RL-based defense, and Castro et al.[9] combine LLMs and RL at the team level for defense, neither integrates LLM strategic reasoning with RL tactical learning within a single offensive agent. Existing LLMbased security agents lack the ability to improve through environment interaction; existing RL-based cyber agents lack strategic reasoning and domain knowledge priors. Our framework bridges this gap by decoupling strategic planning (LLM) from tactical execution (RL), allowing each component to operate in its area of strength: the LLM contributes knowledge of attack tactics and strategic reasoning about target selection, while the RL controller learns environment-specific tactical execution through thousands of training episodes


A Red Teaming Framework for Evaluating Robustness of AI-enabled Security Orchestration, Automation, and Response Systems A Prepprint

A Prepprint

guided by the planner’s intent.

---

## **3 Methodology**

> **Section Summary:** We propose a hierarchical framework for autonomous red teaming that integrates LLMs with RL to address long-horizon decision-making in adversarial environments.


We propose a hierarchical framework for autonomous red teaming that integrates LLMs with RL to address long-horizon decision-making in adversarial environments. The framework decomposes the problem into two levels: (i) high-level strategic planning and (ii) low-level tactical execution, enabling complementary strengths of reasoning and learning to be combined within a unified agent.

### **3.1 Problem Formulation**

We model autonomous red teaming as a partially observable Markov decision process (POMDP) defined by ( _S, A, O, T , r, γ_ ), where _st ∈S_ is the latent environment state, _ot ∈O_ is the observation, _at ∈A_ is the action, and _rt_ is the reward at time _t_ . The agent interacts with the environment over long horizons, with the objective of maximizing cumulative reward while progressing through multi-stage adversarial objectives. Due to partial observability and delayed rewards, effective policies must reason over long temporal dependencies and maintain consistency across multi-step attack sequences.

### **3.2 Hierarchical LLM–RL Architecture**

Our approach introduces a two-level hierarchy consisting of an LLM-based strategic planner and an RL-based tactical controller (see Figure 1).

**Strategic Planner (LLM):** The LLM operates at a coarse temporal resolution and produces a structured _intent_ conditioned on the current observation and auxiliary context. The intent encodes high-level decisions such as action type, MITRE ATT&CK tactic, target selection, and risk posture. Formally, the planner defines:


![](images/11-a-red-teaming-framework-for-evaluating-robustness-of-ai.pdf-0005-10.png)


where _zt_ is the structured intent and _mt_ represents optional memory or contextual inputs. The LLM parameters remain fixed during training.

**Tactical Controller (RL):** The RL controller executes actions at every timestep, conditioned on both the current observation and the LLM-generated intent:


![](images/11-a-red-teaming-framework-for-evaluating-robustness-of-ai.pdf-0005-13.png)


This allows the controller to learn environment-grounded policies while following high-level strategic guidance.

To integrate both inputs, we encode observations into a latent representation _ht_ and map the intent into a compatible embedding space. The combined representation is used by an actor-critic policy optimized via policy gradient methods. Notably, the planner operates at a lower frequency than the controller, generating intents every _h_ steps or when replanning is triggered. This reduces computational overhead while maintaining responsiveness to environment changes.

### **3.3 State and Intent Representation**

Observations are transformed into two complementary representations:

- A structured natural language summary used by the LLM planner.

- A numeric feature vector used by the RL controller.

The LLM outputs a structured intent object containing discrete and continuous attributes (e.g., action category, target, confidence), which is encoded into a fixed-dimensional embedding before being consumed by the RL controller.


A Red Teaming Framework for Evaluating Robustness of AI-enabled Security Orchestration, Automation, and Response Systems A Prepprint

A Prepprint

Table 1: Hierarchical reward shaping components used for training the RL controller.

|**Layer**|**Component**|**Reward**|
|---|---|---|
|L1: Environment|Negated defender reward|_renv_ =_−r_blue|
||Discover new host|+0_._2|
||Scan host|+0_._5|
||Compromise (user access)|+5_._0|
|L2: Milestone|Privilege escalation (root)|+3_._0|
||Impact host|+5_._0|
||Discover new subnet|+1_._0|
||First compromise (defended subnet)|+8_._0|
||Impact without root|_−_0_._1|
|L3: Constraint|Exploit without scanning|_−_0_._05|
||Escalate without user access|_−_0_._05|
|L4IntntAlinmnt|Match LLM intent|+1_._0|
|: e ge|Diverge from intent|_−_0_._3|


### **3.4 Hierarchical Reward Shaping**

To address sparse and delayed rewards, we introduce a novel reward function composed of multiple components:


![](images/11-a-red-teaming-framework-for-evaluating-robustness-of-ai.pdf-0006-06.png)


where _r_ env is the environment reward that provides task-level feedback, _r_ progress is the progress reward that encourages advancement through multi-stage objectives, _r_ constraint represents constraint penalties that discourage invalid or out-of-order actions, and _r_ alignment is the alignment reward that incentivizes consistency between RL actions and LLM intent. This decomposition is aimed towards improving credit assignment and stabilizes learning in long-horizon settings. Table 1 summarizes the reward components used to guide learning across different stages of the task.

### **3.5 Policy Learning**

The RL controller is trained using an actor-critic method, Proximal Policy Optimization (PPO)[22], to maximize expected return:


![](images/11-a-red-teaming-framework-for-evaluating-robustness-of-ai.pdf-0006-10.png)


where _γ_ is the discount factor and _T_ is the maximum number of timesteps. The controller receives both state and intent information, enabling it to learn when to follow or deviate from the planner based on environment feedback.

### **3.6 Memory and Adaptation**

To enhance long-horizon reasoning, the planner can optionally maintain a bounded memory of prior interactions. In addition to short-term contextual inputs, our approach incorporates the Reflexion framework[10], wherein the planner generates a natural language self-reflection at the end of each episode. These reflections summarize successes, failures, and observed environmental patterns, capturing high-level strategic feedback such as ineffective actions, missed opportunities, and defender behaviors.

Reflections are stored in a bounded first-in, first-out (FIFO) buffer and incorporated into the planner’s input at the start of subsequent episodes. This provides cross-episode strategic context without modifying model parameters, enabling the frozen LLM to adapt its planning behavior through natural language feedback rather than gradient updates. This mechanism complements the RL controller’s weight-based learning. While policy optimization encodes tactical improvements through interaction data, the Reflexion framework enables rapid, explicit adjustments to high-level strategy, allowing the agent to improve both action selection and temporal decision-making across episodes.


A Red Teaming Framework for Evaluating Robustness of AI-enabled Security Orchestration, Automation, and Response Systems A Prepprint

A Prepprint

---

## **4 Experiments**

We evaluate the proposed hierarchical LLM–RL framework in a high-fidelity cyber defense simulation to assess its effectiveness in generating long-horizon, multi-stage attack strategies against adaptive defenders. Figure 1 illustrates the proposed red teaming architecture within a simulation-based testbed. Our experiments are designed to answer a key research question: whether integrating LLM-based strategic planning with RL-based execution improves autonomous red team performance against AI-enabled SOAR systems.


![](images/11-a-red-teaming-framework-for-evaluating-robustness-of-ai.pdf-0007-04.png)


Figure 1: Hierarchical LLM-RL red teaming framework architecture implemented in the CybORG CAGE 4 environment. The LLM planner provides strategic intent every 20 environment steps, while the RL controller selects tactical actions at every step. LLM weights remain fixed; only the RL controller is trained via PPO. The 4-layer reward shaping aligns policy optimization with kill-chain progression and strategic intent following.

### **4.1 Environment**

We conduct all experiments in the CAGE 4 environment.[11, 12] This environment simulates an enterprise network with multiple hosts, services, and subnets, and includes coordinated blue team defenders. The environment is partially observable and requires the red agent to perform multi-step operations such as reconnaissance, exploitation, privilege escalation, and impact over long horizons. Figure 2 shows a schematic of the kill chain progression in this environment. Each episode spans up to 500 timesteps. The blue team is controlled by an H-MARL policy [13] representing a strong autonomous defender.

### **4.2 Red Agent Configurations**

For our proposed hybrid configuration, the LLM planner operates at a planning horizon of _h_ = 20 steps and is also triggered upon action failure. At each timestep _t_ , the environment provides an observation _ot_ describing the current network state, including discovered hosts, available services, access levels, and active sessions. A perception layer (the CybORG adapter) converts this raw observation into a shared state representation consumed by both levels of the hierarchy: a text summary ( _≤_ 600 tokens) for the LLM planner, and a 445-dimensional feature vector for the RL controller.

The RL controller maps the shared state vector and the encoded LLM intent to a discrete action drawn from a 10-action space aligned with MITRE ATT&CK tactics (see Table 2). A state encoder compresses the observation into a 128-dimensional embedding via a two-layer residual network with layer normalization.


A Red Teaming Framework for Evaluating Robustness of AI-enabled Security Orchestration, Automation, and Response Systems A Prepprint

A Prepprint


![](images/11-a-red-teaming-framework-for-evaluating-robustness-of-ai.pdf-0008-02.png)


Figure 2: MITRE ATT&CK kill chain progression in CAGE 4. Each stage requires completion of the previous stage on the same host. The minimum path from discovery to impact requires 10 environment steps (12 with stealth scanning). Blue team defenders detect indicator files created during exploitation and escalation, triggering host restoration that removes all red team access.

When an LLM planner is present, an intent encoder maps the structured intent into a 128-dimensional vector, yielding a combined 256-dimensional input to the policy and value networks. A prerequisite-aware action mask constrains the RL controller to only select actions that have valid targets in the current state, preventing wasted actions while preserving autonomous decision-making (the RL chooses _which_ valid action to take, not a hand-coded rule).

The selected action index is translated into a CybORG-compatible action parameterized by the intent’s target host and the current belief state in the execution layer. The environment returns the next observation, a reward signal, and a termination flag. A reward shaping module augments the sparse environment reward with kill-chain-aligned bonuses and penalties.

Table 2: Discrete action space aligned with MITRE ATT&CK tactics. Actions 0–3 perform reconnaissance at different stealth levels, actions 4–5 advance the kill chain through exploitation and privilege escalation, actions 6–7 achieve operational impact, and actions 8–9 <u>provide</u> evasive maneuvers.

|**Index**|**Action**|**MITRE ATT&CK Tactic**|
|---|---|---|
|0|DiscoverRemoteSystems|Discovery|
|1|AggressiveServiceDiscovery|Discovery|
|2|StealthServiceDiscovery|Discovery|
|3|DiscoverDeception|Discovery|
|4|ExploitRemoteService|Initial Access|
|5|PrivilegeEscalate|Privilege Escalation|
|6|Impact|Impact|
|7|DegradeServices|Impact|
|8|Withdraw|Defense Evasion|
|9|Sleep|Defense Evasion|


We evaluate our approach by comparing with two other agent configurations to isolate the contribution of each component in our framework:


A Red Teaming Framework for Evaluating Robustness of AI-enabled Security Orchestration, Automation, and Response Systems A Prepprint

A Prepprint

- **LLM-only (zero-shot):** The LLM directly selects actions at each timestep without learning, establishing a baseline for purely reasoning-based agents. We evaluate 14 open-weight LLMs spanning four families and a wide range of parameter scales:

   - **General-purpose models:** Qwen3 (0.6B, 1.7B, 4B, 8B, 14B, 32B), a family of instruction-tuned models with native chain-of-thought reasoning capabilities; and Llama (Llama-3.1-8B-Instruct, Llama-3.3-70B-Instruct), widely adopted open-weight instruction-tuned models.

   - **Reasoning-specialized models:** DeepSeek-R1 (14B) and QwQ (32B), optimized for extended chain-of-thought reasoning through distillation and specialized training.

   - **Domain-specialized models:** Foundation-Sec-8B, DeepHat-7B, and RedSage-8B, fine-tuned on cybersecurity-specific corpora including MITRE ATT&CK mappings, vulnerability analysis, and attack simulation data.

- **RL-only:** A PPO-based controller operates without LLM guidance, learning a policy solely from environment interaction.

### **4.3 Training Details**

The RL controller is trained using PPO with Generalized Advantage Estimation (GAE) [22, 23]. Training proceeds for up to 48 hours per run, with early stopping based on convergence of evaluation reward. In particular, training terminates when the evaluation reward improves by less than 0.5% across five consecutive evaluation windows (checked every 1,000 episodes), subject to a minimum of 20,000 episodes to ensure sufficient exploration. We employ curriculum learning by gradually increasing environment difficulty and episode length. Table 3 summarizes the hyperparameters, which were tuned through preliminary experiments in the CAGE 4 environment.

Table 3: PPO hyperparameters for RL controller training.

|**Parameter**|**Value**|
|---|---|
|Learning rate|3_×_10<sup>_−_4</sup> _→_3_×_10<sup>_−_5</sup> (linear decay)|
|Clip ratio _ϵ_|0.2|
|Discount factor _γ_|0.99|
|GAE parameter _λ_|0.95|
|Mini-batch size|64|
|PPO epochs per rollout|8|
|Episodes per rollout|10|
|Max gradient norm|0.5|
|Entropy coefcient|0.05 (Qwen3) / 0.10 (Foundation-Sec-8B)|
|Learning rate schedule|Cosine decay|


### **4.4 Evaluation Protocol and Metrics**

All experiments employ the H-MARL Expert policy [13] as the blue team defender. This policy comprises five coordinated AI agents that operate across network zones to perform investigation and recovery tasks. The expert master policy uses an Indicators of Compromise (IOC)-driven deterministic dispatch mechanism: upon detecting malicious files on a host, the corresponding agent transitions from investigation to recovery (i.e., host restoration).

We evaluate red team performance over 200 episodes using environment-native metrics that capture different stages of adversarial progress, which enable consistent comparison across different agent configurations and training regimes:

- **Episode compromise rate (ECR)** : the fraction of episodes in which the agent achieves at least one host compromise through its own exploitation actions. This is our primary comparison metric, as it directly measures whether the agent can execute the attack kill chain.


A Red Teaming Framework for Evaluating Robustness of AI-enabled Security Orchestration, Automation, and Response Systems A Prepprint

A Prepprint

- **Attack action count (AAC)** : the total number of exploit, escalation, and impact actions attempted across all episodes. This behavioral metric distinguishes agents that actively generate attack campaigns from those that remain passive.

- **Average host discovery (AHD)** : for each episode, we record the maximum number of hosts the agent has discovered at any point during the episode; AHD is the mean of these per-episode maxima. This measures the agent’s reconnaissance reach across the network.

### **4.5 Experimental Design**

We design a set of controlled studies to isolate the contribution of key system components, focusing on three main axes: (i) language model choice, (ii) memory augmentation, and (iii) LLM–RL integration. We evaluate the following dimensions:

- **LLM type:** General-purpose vs. domain-specialized models

- **Memory:** Reflexion-enabled vs. disabled variants

- **LLM–RL coupling:** RL with vs. without LLM-guided intent conditioning

These controlled variations allow us to quantify the impact of strategic reasoning (LLMs), episodic selfimprovement (memory), and hybrid decision-making (LLM+RL).

Table 4 summarizes all evaluated configurations, grouped into three agent types: LLM-only, RL-only, and LLM+RL. Each configuration is evaluated under identical environmental conditions using stochastic action sampling against a fixed 5-agent H-MARL Expert blue team defender.

Table 4: Overview of experimental configurations across LLM-only, RL-only, and LLM+RL agent classes.

|**Agent Type**|**Confguration**|**Purpose**|**Compute**|
|---|---|---|---|
||Qwen3 (0.6B–32B, 6 models)|LLM scaling|1–2_×_H100|
|LLMl|Llama-3.1-8B, 3.3-70B|General|1–4_×_H100|
|-ony|QwQ-32B, R1-14B|Reasoning|1–2_×_H100|
||Cybersecurity models (Foundation-Sec, DeepHat, RedSage)|Domain|1_×_H100|
|RL-only|PPO (RL only, no LLM)|RL baseline|1_×_H100|
||Qwen3-1.7B + PPO|General + RL|2_×_H100|
|LLMRL|Qwen3-1.7B + PPO + Refexion|+ Refection|2_×_H100|
|+|Foundation-Sec-8B + PPO|Domain + RL|2_×_H100|
||Foundation-Sec-8B + PPO + Refexion|+ Refection|2_×_H100|


### **4.6 Implementation Details**

The LLM planner is served using `vLLM` [24] or `HuggingFace Transformers` , selected based on model compatibility and serving efficiency. The RL controller is implemented as a standard actor–critic architecture with shared encoders that jointly process environment state and LLM-derived intent representations.

All experiments are executed on a GPU cluster with NVIDIA H100 (80 GB) GPUs. Each training run is allocated a fixed compute budget of up to 48 hours of wall-clock time to ensure consistent comparison across configurations. The framework is implemented in Python 3.11, using PyTorch 2.6 for RL training and vLLM 0.8.5 for high-throughput LLM inference.

For LLM-integrated configurations, the LLM is deployed as a local vLLM server on GPU 0, while RL training runs on GPU 1 within the same node, avoiding cross-node communication overhead. Both FoundationSec-8B-Reasoning and Qwen3-1.7B fit comfortably within a single H100 GPU under this setup. The LLM server operates asynchronously alongside training and is accessed through an OpenAI-compatible REST API over localhost. Ports are assigned dynamically to support multiple concurrent experiments without conflicts.

---

## **5 Results**

> **Section Summary:** We first evaluate the proposed hierarchical LLM-RL framework and then compare it against standalone LLM and RL baselines.


We first evaluate the proposed hierarchical LLM-RL framework and then compare it against standalone LLM and RL baselines.


A Red Teaming Framework for Evaluating Robustness of AI-enabled Security Orchestration, Automation, and Response Systems A Prepprint

A Prepprint

### **5.1 Evaluation of the Hierarchical LLM-RL Red Teaming Framework**

Table 5 summarizes the performance of the proposed framework across the top performing LLM backbones and memory configurations. The results demonstrate strong and consistent end-to-end attack capability across all configurations. In particular, the hybrid agents achieve near-perfect episode compromise rates, with Qwen3+RL attaining a 100% success rate (200/200 episodes) and Foundation-Sec+RL achieving 94%. These agents reliably progress through multiple stages of the attack sequence, including privilege escalation and impact, indicating effective long-horizon coordination between planning and execution.

Table 5: LLM+RL results <u>(200</u> episodes).

|**Confguration**|**AHD**|**ECR**|**AAC**|
|---|---|---|---|
|Qwen3 + RL|10.01|**200 (100%)**|3,559|
|Qwen3 + RL + Refexion|10.01|199 (99.99%)|541|
|Foundation-Sec + RL|9.86|188 (94%)|2,322|
|Foundation-Sec + RL + Refexion|9.97|182 (91%)|3,765|


The addition of the Reflexion framework maintains high success rates while altering behavioral efficiency, as reflected in differences in action counts. This suggests that reflection primarily influences strategic adaptation rather than raw success probability. Overall, the results show that the hierarchical decomposition enables stable and repeatable execution of multi-stage attack strategies in the presence of adaptive defenders.

### **5.2 Comparison with Standalone LLM Agents**

Table 6 presents the performance of the top performing standalone LLM agents. In contrast to the hybrid approach, LLM-only agents exhibit limited end-to-end capability. Only six of 14 models achieve any compromise beyond the initial foothold, and the strongest model (QwQ-32B) succeeds in only 30% of episodes. Moreover, successful behaviors are largely confined to early-stage reconnaissance and isolated exploitation attempts, without sustained progression through the attack chain.

Table 6: LLM-only results <u>(200</u> episodes). Models with zero success are not shown.

|**Model**|**Category**|**AHD**|**ECR**|**AAC**|
|---|---|---|---|---|
|QwQ-32B|Reasoning-specialized|6.67|**60 (30%)**|266|
|DeepSeek-R1-14B|Reasoning-specialized|10.17|26 (13%)|290|
|Foundation-Sec-8B|Domain-specialized|10.13|13 (6.5%)|21,746|
|DeepHat-7B|Domain-specialized|10.01|8 (4%)|9,741|
|Qwen3-0.6B|General-purpose|3.74|7 (3.5%)|2,490|
|Qwen3-1.7B|General-purpose|10.09|2 (1%)|1,103|


Reasoning-specialized models outperform general-purpose and domain-specific models, achieving higher compromise rates. However, this advantage is confounded by model scale, as these models are also among the largest evaluated. Within the Qwen3 family, performance is non-monotonic with respect to model size: smaller models (e.g., 0.6B) achieve limited success, while larger variants fail to attempt exploitation altogether despite effective exploration (see Figure 3).

Domain-specific models are not competitive despite generating substantially higher action volumes. For instance, Foundation-Sec-8B produces extremely large action counts in the LLM-only setting (21,746 actions) yet achieves only a 6.5% ECR. This indicates that high domain-specific activity alone does not translate into meaningful attack progression, and that strategic reasoning plays a more critical role than domain specialization. These results indicate that while LLMs can provide useful strategic signals, they struggle with consistent multi-step execution and state tracking in interactive environments.

### **5.3 Comparison with RL-only Agents**

The RL-only agent exhibits a degenerate policy collapse, selecting a single reconnaissance action ( _DiscoverRemoteSystems_ ) in nearly all timesteps. Across 200 evaluation episodes, it fails to achieve any successful compromise (0% success rate). This behavior reflects a failure of reward-driven exploration to discover the structured sequence of actions required for multi-stage attacks, instead converging to a local optimum that maximizes immediate reward through repeated discovery actions.


A Red Teaming Framework for Evaluating Robustness of AI-enabled Security Orchestration, Automation, and Response Systems A Prepprint

A Prepprint


![](images/11-a-red-teaming-framework-for-evaluating-robustness-of-ai.pdf-0012-02.png)


Figure 3: Non-monotonic scaling in the Qwen3 model family. Left axis: episodes achieving compromise (out of 200). Right axis: average peak hosts discovered. Only the two smallest models achieve any compromise, while models at 4B+ never attempt exploitation.

We note that this outcome is influenced by the reward formulation used in our framework, which is designed to support the hierarchical LLM-RL setting. We do not perform additional reward tuning for the RL-only baseline in order to maintain a consistent and controlled comparison across agent configurations. As such, the observed collapse highlights the difficulty of learning effective multi-stage strategies under this reward structure without high-level guidance, rather than representing the best achievable performance of standalone RL under task-specific reward optimization.

### **5.4 Key Insights**

These results highlight the complementary limitations of LLMs and RL when used in isolation. Standalone LLM agents provide high-level reasoning but fail to sustain coherent long-horizon behavior, while RL agents can optimize actions through interaction but fail to discover meaningful attack strategies due to sparse rewards and exploration challenges. Our proposed hybrid framework overcomes these limitations by combining strategic guidance from LLMs with environment-grounded learning in RL, resulting in substantial improvements in multi-stage attack success and robustness against adaptive defenses.

---

## **6 CONCLUSION**

> **Section Summary:** We present a hierarchical LLM-RL framework for evaluating the robustness of AI-enabled cyber defense systems in high-fidelity simulation.


We present a hierarchical LLM-RL framework for evaluating the robustness of AI-enabled cyber defense systems in high-fidelity simulation. Across extensive experiments in the CybORG CAGE Challenge 4 environment, we demonstrate that autonomous red teaming requires the tight coupling of strategic reasoning and learned execution. Our principal findings from this study are as follows. First, standalone approaches are fundamentally insufficient. Across 14 LLMs, we observe limited end-to-end attack capability, with most models failing to sustain multi-step compromises. Similarly, RL alone collapses to a degenerate policy, unable to discover meaningful attack progression under sparse rewards. These results highlight the inability of either reasoning- or learning-only systems to execute full kill-chain behavior.

Second, integrating LLM planning with RL execution yields a multiplicative improvement. The hierarchical system achieves near-universal episode-level compromise and substantially higher root access rates than either component alone. The LLM provides high-level strategic intent over kill-chain progression, while


A Red Teaming Framework for Evaluating Robustness of AI-enabled Security Orchestration, Automation, and Response Systems A Prepprint

A Prepprint

the RL controller learns robust low-level execution, enabling sustained multi-step attack behavior under adaptive defense.

Third, we find that reliable structured planning is more critical than domain specialization. Generalpurpose models consistently outperform larger cybersecurity-specialized models, despite the latter producing significantly higher action volumes. This discrepancy is primarily driven by improved output reliability and fewer planning failures in general-purpose models, suggesting that structured controllability is a key requirement for LLMs in hierarchical decision systems.

Our study is constrained by several factors. First, evaluation is conducted in a single high-fidelity simulation environment (CAGE 4), and generalization to other network settings and real-world systems remains untested. Second, the framework uses a single red team agent, limiting analysis of coordination effects in multi-agent adversarial settings. Third, only a small subset of LLMs is integrated into the full hierarchical system due to computational constraints, leaving open the question of how stronger or larger models would affect performance. Finally, the environment introduces partial observability constraints that prevent full network topology awareness prior to host compromise, which may influence exploration dynamics.

Future directions include extending the framework to multi-agent red team coordination, improving topology inference through structured exploration strategies, and evaluating scalability across diverse environments and defender policies. We also plan to investigate larger and more capable LLM planners to better understand scaling behavior within hierarchical RL systems.

---

## **Acknowledgments**

> **Section Summary:** This work was supported in part by the U.S.


This work was supported in part by the U.S. Military Academy (USMA) under Cooperative Agreement No. W911NF-25-2-0008 and the Defense Advanced Research Projects Agency (DARPA) under Cooperative Agreement No. HR0011-24-2-0004. The views and conclusions expressed in this paper are those of the authors and do not reflect the official policy or position of USMA, U.S. Army, U.S. Department of War, or U.S. Government.

Computational resources for this study were in part provided by Indiana University’s Big Red 200 supercomputer.

Distribution statement: Approved for public release; distribution is unlimited.

---

## **References**

> **Section Summary:** - [1] Check Point Software Technologies Ltd.


- [1] Check Point Software Technologies Ltd. Cyber security report 2026, 2026. URL `https://www. checkpoint.com/security-report/` . Accessed: 2026-03-11.

- [2] Asif Shahriar, Md Nafiu Rahman, Sadif Ahmed, Farig Sadeque, and Md Rizwan Parvez. A survey on agentic security: Applications, threats and defenses. _arXiv preprint arXiv:2510.06445_ , 2025.

- [3] HanXiang Xu, ShenAo Wang, Ningke Li, Kailong Wang, Yanjie Zhao, Kai Chen, Ting Yu, Yang Liu, and HaoYu Wang. Large language models for cyber security: A systematic literature review. _ACM Transactions on Software Engineering and Methodology_ .

- [4] The MITRE Corporation. MITRE ATT&CK: Adversarial tactics, techniques, and common knowledge. `https://attack.mitre.org/` , 2024.

- [5] Longjing Yang, Ayong Ye, Yuanhuang Liu, Wenting Lu, and Chuang Huang. Llm-aptds: A highprecision advanced persistent threat detection system for imbalanced data based on large language models with strong interpretabilit. _Future Generation Computer Systems_ , page 108315, 2025.

- [6] Paul Kassianik, Baturay Saglam, Alexander Chen, Blaine Nelson, Anu Vellore, Massimo Aufiero, Fraser Burch, Dhruv Kedia, Avi Zohary, Sajana Weerawardhena, et al. Llama-3.1-foundationai-securityllmbase-8b technical report. _

- [7] Cameron Thomas Stark. Generative artificial intelligence tools for red teams. Technical report, Sandia National Laboratories (SNL-NM), Albuquerque, NM (United States), 2024.


A Red Teaming Framework for Evaluating Robustness of AI-enabled Security Orchestration, Automation, and Response Systems A Prepprint

A Prepprint

- [8] Soumyadeep Hore, Jalal Ghadermazi, Diwas Paudel, Ankit Shah, Tapas Das, and Nathaniel Bastian. Deep packgen: A deep reinforcement learning framework for adversarial network packet generation. _ACM Transactions on Privacy and Security_ , 28(2):1–33, 2025.

- [9] Sebasti´an R Castro, Roberto Campbell, Nancy Lau, Octavio Villalobos, Jiaqi Duan, and Alvaro A Cardenas. Large language models are autonomous cyber defenders. In _2025 IEEE Conference on Artificial Intelligence (CAI)_ , pages 1125–1132. IEEE, 2025.

- [10] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion: Language agents with verbal reinforcement learning. _Advances in neural information processing systems_ , 36:8634–8652, 2023.

- [11] Callum Baillie, Maxwell Standen, Jonathon Schwartz, Michael Docking, David Bowman, and Junae Kim. Cyborg: An autonomous cyber operations research gym. _

- [12] Mitchell Kiely, Metin Ahiskali, Etienne Borde, Benjamin Bowman, David Bowman, Dirk Van Bruggen, KC Cowan, Prithviraj Dasgupta, Erich Devendorf, Ben Edwards, et al. Exploring the efficacy of multi-agent reinforcement learning for autonomous cyber defence: A cage challenge 4 perspective. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 39, pages 28907–28913, 2025.

- [13] Aditya Vikram Singh, Ethan Rathbun, Emma Graham, Lisa Oakley, Simona Boboila, Peter Chin, and Alina Oprea. Hierarchical multi-agent reinforcement learning for cyber network defense. In _Proceedings of the 24th International Conference on Autonomous Agents and Multiagent Systems_ , pages 2747–2749, 2025.

- [14] Microsoft Defender Research Team. CyberBattleSim: An experimentation and research platform for autonomous cyber agents. `https://github.com/microsoft/CyberBattleSim` , 2021.

- [15] Andres Molina-Markham, Cory Miniter, Becky Powell, and Ahmad Ridley. Network environment design for autonomous cyberdefense. _

- [16] Gelei Deng, Yi Liu, V´ıctor Mayoral-Vilches, Peng Liu, Yuekang Li, Yuan Xu, Tianwei Zhang, Yang Liu, Martin Pinzger, and Stefan Rass. _{_ PentestGPT _}_ : Evaluating and harnessing large language models for automated penetration testing. In _33rd USENIX Security Symposium (USENIX Security 24)_ , pages 847–864, 2024.

- [17] Lajos Muzsai, David Imolai, and Andr´as Luk´acs. Hacksynth: Llm agent and evaluation framework for autonomous penetration testing. _

- [18] Maria Rigaki, Ondˇrej Luk´aˇs, Carlos A Catania, and Sebastian Garcia. Out of the cage: How stochastic parrots win in cyber security environments. _

- [19] Matan Levi, Daniel Ohayon, Ariel Blobstein, Ravid Sagi, Ian Molloy, and Yair Allouche. Toward cybersecurity-expert small language models. _

- [20] Isaiah J King, Benjamin Bowman, and H Howie Huang. Automated cyber defense with generalizable graph-based reinforcement learning agents. _

- [21] Konur Tholl, Fran¸cois Rivest, Mariam El Mezouar, Adrian Taylor, and Ranwa Al Mallah. Large language model integration with reinforcement learning to augment decision-making in autonomous cyber operations. _

- [22] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _

- [23] John Schulman, Philipp Moritz, Sergey Levine, Michael Jordan, and Pieter Abbeel. High-dimensional continuous control using generalized advantage estimation. In _Proc. Int. Conf. Learning Representations (ICLR)_ , 2016. arXiv:1506.02438.


A Red Teaming Framework for Evaluating Robustness of AI-enabled Security Orchestration, Automation, and Response Systems A Preprint

- [24] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gonzalez, Hao Zhang, and Ion Stoica. Efficient memory management for large language model serving with pagedattention. In _Proceedings of the 29th symposium on operating systems principles_ , pages 611–626, 2023.
