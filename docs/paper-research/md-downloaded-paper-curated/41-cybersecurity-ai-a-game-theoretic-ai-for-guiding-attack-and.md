# **Cybersecurity AI: A Game-Theoretic AI for** **_Guiding_ Attack and Defense** 

## Table of Contents

- [Cybersecurity AI: A Game-Theoretic AI for Guiding Attack and Defense](#cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and-defense)
  - [1 Introduction](#1-introduction)
    - [1.1 State of the Art](#1-1-state-of-the-art)
    - [1.2 Research Contributions](#1-2-research-contributions)
  - [2 Background](#2-background)
    - [2.1 Cybersecurity AI](#2-1-cybersecurity-ai)
    - [2.2 Game Theory in Cybersecurity: Cut-the-Rope](#2-2-game-theory-in-cybersecurity-cut-the-rope)
  - [3 Game-Theoretic AI for Guiding Attack and Defense](#3-game-theoretic-ai-for-guiding-attack-and-defense)
    - [3.1 Game-Theoretic AI Analysis via Generative Cut-The-Rope (G-CTR)](#3-1-game-theoretic-ai-analysis-via-generative-cut-the-rope-g-ctr)
    - [3.2 Game-Theoretic AI Digest for Guiding Attack and Defense](#3-2-game-theoretic-ai-digest-for-guiding-attack-and-defense)
  - [4 Results](#4-results)
    - [4.1 Qualitative Comparison: Graph Quality of Human Experts vs. LLMs](#4-1-qualitative-comparison-graph-quality-of-human-experts-vs-llms)
    - [4.2 Quantitative Evaluation: Performance of LLM Automation vs. Gold Standard/Human Experts](#4-2-quantitative-evaluation-performance-of-llm-automation-vs-gold-standard-human-experts)
    - [4.3 Game-Theoretic AI Digest Results for Guiding Attack and Defense](#4-3-game-theoretic-ai-digest-results-for-guiding-attack-and-defense)
    - [4.4 Ablations](#4-4-ablations)
  - [5 Discussion](#5-discussion)
  - [6 Conclusion](#6-conclusion)
  - [7 Acknowledgements](#7-acknowledgements)
  - [References](#references)
  - [A Appendix 1: A Refresher on Cut-The-Rope (CTR) and Game Theory [6]](#a-appendix-1-a-refresher-on-cut-the-rope-ctr-and-game-theory-6)
  - [B Appendix 2: Attack Graph Gold Standard Dataset](#b-appendix-2-attack-graph-gold-standard-dataset)
  - [C Appendix 3: kolesa.kz](#c-appendix-3-kolesa-kz)
  - [D Appendix 3: mercadolibre.com](#d-appendix-3-mercadolibre-com)
  - [E Appendix 3: <u>pornbox.com</u>](#e-appendix-3-u-pornbox-com-u)
  - [F Appendix 4: hm.com](#f-appendix-4-hm-com)
  - [G Appendix 5: media.guilded.gg](#g-appendix-5-media-guilded-gg)

---

**Víctor Mayoral-Vilches**<sup>1</sup> **, María Sanz-Gómez**<sup>1</sup> **, Francesco Balassone**<sup>1</sup> **, Stefan Rass**<sup>2</sup> **, Lidia Salas-Espejo**<sup>1</sup> **, Benjamin Jablonski**<sup>2</sup> **, Luis Javier Navarrete-Lozano**<sup>1</sup> **, Maite del Mundo de Torres**<sup>1</sup> **and Cristóbal R. J. Veas Chavez**<sup>1</sup> 

> 1 **Alias Robotics** , Vitoria-Gasteiz, Álava, Spain, � `research@aliasrobotics.com` 

> 2Johannes Kepler University Linz. 

� `https://github.com/aliasrobotics/cai` , � `https://discord.gg/fnUFcTaQAC` 

###### **Abstract** 

> AI-driven penetration testing now executes thousands of actions per hour but still lacks the strategic intuition humans apply in competitive security. To build cybersecurity superintelligence–Cybersecurity AI exceeding best human capability—such strategic intuition must be embedded into agentic reasoning processes. We present Generative Cut-the-Rope (G-CTR), a game-theoretic guidance layer that extracts attack graphs from agent’s context, computes Nash equilibria with effort-aware scoring, and feeds a concise digest back into the LLM loop _guiding_ the agent’s actions. Across five real-world exercises, G-CTR matches 70–90% of expert graph structure while running 60–245 _×_ faster and over 140 _×_ cheaper than manual analysis. In a 44-run cyber-range, adding the digest lifts success from 20.0% to 42.9%, cuts cost-per-success by 2.7 _×_ , and reduces behavioral variance by 5.2 _×_ . In Attack-andDefense exercises, a shared digest produces the **Purple** agent, winning roughly 2:1 over the LLM-only baseline and 3.7:1 over independently guided teams. This closed-loop guidance is what produces the breakthrough: it reduces ambiguity, collapses the LLM’s search space, suppresses hallucinations, and keeps the model anchored to the most relevant parts of the problem, yielding large gains in success rate, consistency, and reliability. 

### **1 Introduction** 

Cybersecurity is being revolutionized by the use of AI and particularly Large Language Models (LLMs). In 2023, PentestGPT [1, 2] pioneered results showing that LLMs could help guide humans in penetration testing. In early 2025, Cybersecurity AI (CAI) [3] demonstrated that LLMs could yield penetration testing results at expert human levels, while faster and cheaper. The next frontier is “cybersecurity superintelligence”: cybersecurity AI exceeding best human capability. Agents that not only act faster than humans but also reason strategically the way humans do when they mentally “ _play the game_ ”. Just as a chess grandmaster evaluates the board and imagines possible attacker/defender lines before committing to a move, AI agents must internalize that intuition to choose optimal cyber actions under pressure. 

Achieving that intuition requires more than faster execution; it requires embedding a reasoning substrate that weighs attacker and defender payoffs at every step. Humans implicitly apply game theory when playing chess, Go, or when solving competitive cybersecurity challenges such as Attack and Defense CTFs (A&D): we evaluate the current “board,” imagine opponent responses, and choose the move that maximizes long-term advantage. Our game-theoretic layer does not invent new attacks; it restructures the AI’s own actions into an attack graph, computes equilibria, and returns a digest—akin to a chess engine highlighting the strongest lines—that steers the LLM toward statistically advantageous continuations. This closed-loop guidance reduces ambiguity, collapses the search space, and suppresses hallucinations by anchoring the model to what is actually unfolding in the environment, which explains the 5.2 _×_ variance reduction and 2 _×_ success gains reported later. We argue that to 


_Introduction_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0002-01.png)


<!-- Start of picture text -->
Phase 1: Game-Theoretic AI Analysis (G-CTR) Phase 2: Game-Theoretic AI Guidance (Digest Generation) Phase 3: Agent Execution (ReAct)<br>G-CTR < 10ms ≈ 60s<br>Results Algorithmic Act<br>digest<br>(Tools)<br>< 5ms ≈ 10s<br>Nash Strategic Plan<br>Equilibrium Interpretation (LLM)<br>≈ 20s ≈ 28.3s<br>Scan &<br>Attack LLM Update<br>Graph digest (Context)<br>Generation<br>every 5 interactions ( ∼ 80 tools)<br>Time Budget: ≈ 50s Time Budget: ≈ 70s<br><!-- End of picture text -->

**Figure 1:** Game-Theoretic architecture for guiding attack and defense actions in Cybersecurity AI through closedloop strategic feedback obtained by applying the G-CTR method. The system operates in three phases: (1) GameTheoretic AI Analysis generates attack graphs and computes Nash equilibria via G-CTR to identify optimal attack/defense strategies, (2) Strategic interpretation transforms equilibrium data into actionable guidance for both attackers and defenders, (3) AI agent execution performs security testing with continuous graph refinement every _n_ interactions ( _∼_ 80 tool calls). This architecture enables real-time strategic adaptation for AI security operations, with Phases 1-2 operating within a _≈_ 50s time budget parallel to Phase 3’s _≈_ 70s execution cycles, providing minimal computational overhead while maximizing strategic impact. 

surpass human capability, we need AI agents that perform the same mental chess, but at machine scale and speed. 

AI-driven penetration testing tools like the open source _Cybersecurity AI_ (CAI) [4] have demonstrated they can discover vulnerabilities 3,600 _×_ faster than humans, yet their outputs (dense logs of automated findings) overwhelm security teams. Meanwhile, game-theoretic frameworks like Cutthe-Rope (CTR) [5, 6, 7] compute optimal defense strategies but require manually-constructed attack graphs as input. This disconnect between rapid AI discovery and strategic defense planning represents a critical gap in modern cybersecurity, raising the fundamental question: can we bridge this gap by automatically transforming AI security outputs into strategic game-theoretic models that then guide both attack and defense operations? In other words, our research here attempts answering the following: _RQ1: can we make Cybersecurity AI agents more effective by guiding them strategically with game theory?_ 

This paper addresses this question by presenting a game-theoretic AI guidance architecture that bridges the gap between AI-driven security testing and strategic reasoning, providing actionable guidance for both attack and defense operations. Through closed-loop feedback, the system continuously refines its understanding of the threat landscape and adapts its strategic recommendations. The architecture integrates three phases as depicted in Figure 1: (1) a game-theoretic AI analysis powered by the novel Generative-CTR (G-CTR) which automatically performs attack graph extraction from AI security logs using LLMs and performs Nash equilibrium computation to identify optimal attack/defense strategies, (2) a strategic interpretation that transforms game-theoretic insights into actionable guidance for AI agents, and (3) an open-source AI security framework implementing ReAct agents where both aforementioned methods are integrated within the agent’s _Planning_ phase. Phases 1-2 operate in parallel with Phase 3, providing minimal computational overhead while maximizing strategic impact. 

Empirically, the architecture delivers three key results. First, across five real-world exercises, G- CTR produces 6–15 node graphs with 70–90% node correspondence to expert annotations (provided by two externally hired domain professionals; see Appendix B) while running 60–245 _×_ faster and over 140 _×_ cheaper than manual workflows. Second, in a 44-run cyber-range benchmark targeting 

_Introduction_ 

the Shellshock CVE-2014-6271 vulnerability [8, 9], the LLM digest doubles success probability (20.0% _→_ 42.9%), boosts cost-per-success by 2.7 _×_ , and reduces tool-use variance by 5.2 _×_ . Third, in realistic Attack and Defense cybersecurity exercises, sharing a single graph between red and blue agents yields the **Purple G-CTRmerged** configuration, which defeats the LLM-only baseline roughly 2:1 and outperforms independently guided dual teams 3.7:1. These results foreshadow the broader promise of cybersecurity superintelligence: autonomous agents that blend machine-scale speed with game-theoretic foresight. 

Our empirical evaluation on five real-world exercises shows that G-CTR generates graphs 60-245 times faster than manual analysis while achieving 70-90% node correspondence with expert annotations. More importantly, we demonstrate how this game-theoretic guidance enhances pentesting effectiveness—agents guided by strategic feedback achieve 3.21 _×_ higher success rates while reducing cost-per-finding by 96%. 

The key insight is that LLMs can transform unstructured security narratives into structured models suitable for game-theoretic analysis, enabling a closed-loop system where AI-driven testing and strategic reasoning mutually reinforce each other. This represents a step toward autonomous cybersecurity systems that not only discover vulnerabilities but also reason strategically about optimal exploitation paths and critical defensive positions, guiding both red team operations and blue team prioritization. 

#### **1.1 State of the Art** 

AI-powered penetration testing has advanced rapidly, research lines like Cybersecurity AI (CAI) [3, 3, 10, 11, 12, 13, 14, 15] report achieving 3,600× speedup over humans and frameworks like PentestGPT [1], AutoPT [16], and VulnBot [17] automating complex assessments. However, these tools produce overwhelming amounts of unstructured data that security teams struggle to interpret and act upon. 

Attack graphs provide structured representations of attack paths [18], with traditional tools like MulVAL [19] using logic-based reasoning over vulnerability databases. While recent work explores machine learning enhancements [20, 21], current approaches remain disconnected from live security operations and require extensive manual effort. 

Game theory offers strategic analysis of attacker-defender interactions, with CTR [5, 6] computing optimal defense strategies on attack graphs. Despite proven effectiveness against APTs [22], gametheoretic approaches assume pre-existing graphs rather than generating them from operational data. 

The critical gap lies in the integration: AI security tools generate logs without prioritization, humans process logs and manually create models (attack graphs), game-theoretic frameworks analyze pre-built models without operational integration, and neither provides actionable guidance for both attackers and defenders. No existing system closes the loop by automatically extracting attack graphs from AI operations, computing Nash equilibria to identify optimal strategies, and transforming these game-theoretic insights into real-time guidance that directs subsequent security testing. This disconnect prevents game-theoretic reasoning from enhancing AI-driven red team operations and blue team defensive prioritization, limiting the practical impact of both technologies in modern cybersecurity workflows. 

While AI and LLMs have seen growing adoption in cybersecurity, especially in automating penetration testing, several critical challenges remain unresolved: 

- _Limited Scalability of Attack Graphs._ Existing attack graph methodologies rely heavily on manual curation or static generation approaches, which struggle to scale with the complexity and dynamism of modern network environments. This limits their practical use in continuous, largescale cybersecurity operations. 

- _Lack of Comprehensive Evaluation of LLMs in Cybersecurity._ Despite the rapid development of LLMs, their capabilities for understanding and modeling cybersecurity exercises remain poorly characterized. There is an absence of standardized, gold-standard datasets or benchmarks to rigorously assess LLM-driven attack graph generation and reasoning. 

_Introduction_ 

- _Insufficient Integration of Game-Theoretic Models with AI Automation._ Game theory offers powerful frameworks for risk assessment [5, 6, 7, 19] and strategic defense in cybersecurity, yet its fusion with LLM-based automation has not been thoroughly explored or validated in practical tooling. 

- _Gap Between Fast-Evolving AI Capabilities and Human Annotation Workflows._ The accelerating pace of AI-driven cybersecurity tasks challenges traditional human annotation and analysis methods, creating a need for automated systems that can keep up without sacrificing accuracy or interpretability. 

Addressing these gaps is key to advancing scalable and autonomous cybersecurity operations. To address these limitations, our work introduces a game-theoretic AI architecture that provides strategic guidance for both attack and defense through closed-loop feedback. Built on top of the CAI framework and inspired by the Cut-The-Rope (CTR) algorithm [5, 6], our architecture transforms game-theoretic insights into actionable guidance. This enables dynamic attack graph generation coupled with effortbased vulnerability scoring, allowing both defenders to prioritize responses based on cost and path complexity, and attackers to focus on high-probability exploitation paths. By integrating an agentic LLM-driven security automation with game-theoretic reasoning within a unified closed-loop framework, this approach bridges the gap between reactive automation and strategic foresight, providing real-time guidance for red team operations and blue team defensive prioritization. 

#### **1.2 Research Contributions** 

This work presents a game-theoretic AI architecture for guiding both attack and defense in cybersecurity through closed-loop feedback. Our contributions include: 

1. **Generative Cut-The-Rope (G-CTR)** : We introduce G-CTR (Section 3.1), an extension of the original CTR framework that leverages LLMs to automatically generate attack graphs and Nash equilibrium computations from unstructured cybersecurity logs and exercise narratives. G-CTR introduces two key innovations that enable automated game-theoretic analysis in cybersecurity: 

   - **(a) Automated Graph Extraction from AI Security Logs.** We demonstrate that LLMs can automatically extract structured attack graphs from CAI penetration testing logs (Section 3.1.1) with 70-90% node correspondence to expert-generated graphs, achieving 60-245 _×_ time speedups and 225-450 _×_ cost improvements over manual analysis. 

   - **(b) Effort-Based Scoring for LLM-Generated Graphs.** We introduce a practical adaptation of CTR’s probabilistic model to handle the unique characteristics of LLM-generated attack graphs (Section 3.1.3). Our effort score combines message distance, token count, and cost metrics to quantify attack difficulty in the absence of traditional probability estimates, enabling game-theoretic analysis on automatically generated graphs. 

2. **Strategic Digest Generation for Guiding Attack and Defense:** We introduce a digest generation pipeline that transforms Nash equilibrium computations into actionable strategic guidance (Section 3.2), closing the loop between G-CTR analysis and CAI execution. In 44 cyber-range penetration tests, LLM-based digests improved success rates from 20.0% to 42.9% (2.15 _×_ ), cut costper-success from $0.32 to $0.12 (2.7 _×_ ), and reduced tool-usage variance by 5.2 _×_ , demonstrating that LLM interpretation of game-theoretic outputs materially enhances autonomous pentesting. 

3. **Practical Validation Framework:** We evaluate our approach on five real-world security exercises, demonstrating that LLM-generated graphs (6–15 nodes, up to four vulnerable stages) maintain 70–90% node correspondence with expert baselines while delivering 60–245 _×_ time savings and _>_ 140 _×_ cost reduction. These studies establish that automated graph generation plus effort-aware scoring can prioritize pentesting effort and defender investments without human curation. 

_Background_ 

4. **Breakthrough Multi-Agent Guidance:** We extend the architecture to Attack and Defense CTFs and introduce the **Purple G-CTRmerged** team configuration, where red and blue agents share a single G-CTR graph and situational context. This GenAI+game-theory agent wins `pingpong` matches 52.4% vs 28.6% (~1.8:1) against the LLM-only baseline and defeats independent dual guidance 55% vs 15% (~3.7:1) in `cowsay` , establishing a new state of the art for AI-driven Attack and Defense play. 

The remainder of this paper is organized as follows: Section 2 provides background on CAI and game–theoretic approach relevant to our work. Section 3 presents our proposed game-theoretic AI architecture. Section 4 presents our experimental results. Section 5 discusses the implications of our findings. Finally, we conclude the paper with a summary of contributions and key insights. 

### **2 Background** 

#### **2.1 Cybersecurity AI** 

Artificial Intelligence (AI) is transforming cybersecurity, yet many AI solutions remain proprietary and inaccessible to small and medium-sized enterprises. To address this gap, open and transparent frameworks have been developed in which CAI [3, 23] stands at the fore front. CAI is a modular, autonomous system with Human-In-The-Loop oversight that achieves up to 3,600 _×_ faster performance than humans and excelling in global CTF competitions [24]. AI’s speed and complexity create significant interpretability challenges, highlighting the need for tools that can effectively interpret and analyze its behaviour. Attack Graphs provide a human–interpretable framework for this purpose. There is a critical need not only to observe AI actions but to systematically interpret, visualize, and strategically analyze them for actionable insights. Attack graphs address this by modeling vulnerabilities, exploits, and defenses in a human–interpretable framework. To fully leverage their strategic potential, we leverage the Cut–the–Rope (CTR) model and expand it to build a game-theoretic AI architecture atop CAI. 

#### **2.2 Game Theory in Cybersecurity: Cut-the-Rope** 

Cybersecurity inherently involves adversarial interactions where perfect protection is unattainable due to unknown vulnerabilities and system complexity. The Cut-the-Rope (CTR) model [5] provides a rigorous game-theoretic framework for this domain by modeling systems as directed acyclic graphs _G_ = ( _V, E_ ), where nodes _V_ represent system components and edges _E_ denote exploitable transitions. This model provides security games that have has been used in various subsequent studies including the assessment of effective defenses in robots [6], and to estimate the zero-day risks [7]. 

CTR formalizes a zero-sum asynchronous game where an attacker, already present at unknown node _θ ∈ V \{v_ 0 _}_ , advances stochastically toward target _v_ 0 following a Poisson process with rate _λ_ . The defender inspects nodes from admissible set _AS_ 1 _⊆ V \ {v_ 0 _}_ according to mixed strategy _σd ∈_ ∆( _AS_ 1). The probability of catching the attacker is: 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0005-09.png)


where _Pπ_ ( _c | θ, λ_ ) = <u>�</u> _x∈Vf_ (Pois _π_ )(<sup>_f_</sup> _d_<sup>Pois</sup> _π_ <u>(</u> _θ_<sup>(</sup> _<u>,</u>_<sup>_d_</sup> _c_<sup>_π_</sup> <u>);</u><sup>(</sup> _λ_<sup>_θ,x_</sup> <u>)</u><sup>);</sup><sup>_λ_)representsthelikelihoodoftheattackerbeingatnode</sup><sup>_c_</sup> given path _π_ and distance _dπ_ ( _θ, c_ ). The Nash equilibrium ( _σd_<sup>_⋆, π⋆, θ⋆_)solvestheminimaxproblem:</sup> 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0005-11.png)


This yields the optimal randomized defense policy that minimizes the worst-case attack success probability, representing a stable state where neither player benefits from unilateral deviation. For complete mathematical derivation, see Appendix A. 

_Background_ 

In all experiments we instantiate the Poisson attacker process with a rate of _λ_ = 2 transitions per defender inspection window ( _λa_ = 2, _λd_ = 1), i.e., the attacker advances an expected two edges along its chosen path between successive digest-triggered observations. 

### **3 Game-Theoretic AI for Guiding Attack and Defense** 

#### **3.1 Game-Theoretic AI Analysis via Generative Cut-The-Rope (G-CTR)** 

This section details how the CTR model, originally for static attack graphs, is extended for its integration atop CAI. We introduce **Generative Cut-The-Rope (G-CTR)** , an extension of the original CTR framework that leverages LLMs to automatically generate attack graphs from unstructured cybersecurity logs and exercise narratives. Modifications enable CTR to process LLM–inferred data from cybersecurity logs, supporting dynamic reasoning without losing its theoretical foundation. 

##### **3.1.1 Automated Graph Extraction from AI Security Logs** 

AI-driven penetration testing generates vast quantities of unstructured logs documenting tool executions, vulnerability discoveries, and exploitation attempts. Traditional attack graph construction requires security experts to manually analyze these logs, identify attack paths, and encode relationships— a process that can take hours or days per exercise [18]. LLMs offer a transformative alternative: by leveraging their understanding of cybersecurity concepts and contextual reasoning capabilities, LLMs can automatically parse security logs, extract relevant entities (vulnerabilities, exploits, system components), and construct structured attack graphs that capture the progression of penetration testing activities. This automation enables real-time graph generation that keeps pace with AI-driven security testing, addressing the bottleneck between rapid vulnerability discovery and strategic analysis. 

The main difference between the original CTR library and G-CTR lies in how the Attack Graph is built. The original CTR uses a graph manually created by human experts, based on known threats and fixed probabilities. In contrast, G-CTR uses LLM-generated graphs that emerge from automated analysis of security logs. Detailed comparison of these two approaches is presented in Table 1. 

**Table 1:** Key differences between the original CTR implementation and G-CTR. 

|**Feature**|**CTR (Original)**|**G-CTR (LLM-Driven)**|
|---|---|---|
|**Graph Semantics**|Success rate of exploiting a given<br>node along a specifc attack path.|Effort required to reach the frst<br>vulnerable node along a path<br>(Section 3.1.3).|
|**Graph Generation**|Manually constructed by<br>cybersecurity experts. All nodes,<br>vulnerabilities, and paths are<br>hand-annotated.|Automatically inferred by LLMs<br>generating structured `JSONL` output<br>from security logs (Appendix B).<br>Two-step adaptation: (1)<br>preprocessing—merge entry points<br>to node 1, add artifcial edges<br>(Figure 2); (2)<br>postprocessing—prune<br>non-vulnerable leaves, add artifcial<br>leaf nodes to remark vulnerable<br>ones (with probability: 100%).|



_Background_ 

**Table 1 (continued)** 

|**Feature**|**CTR (Original)**|**G-CTR (LLM-Driven)**|
|---|---|---|
|**Node Semantics**|System components or entities<br>identifed by human experts.|Elements identifed by LLM as<br>relevant. Single `message`<sup>`_`</sup>`id` may<br>yield multiple nodes if LLM extracts<br>distinct semantic information.|
|**Node Count**|Determined by human expert<br>analysis.|Capped at percentage of total log<br>messages (Section 3.1.4). Limit<br>prevents hallucinations while<br>maintaining coverage.|
|**Vulnerable Nodes**|Only leaf nodes (end states of<br>successful exploitation in closed<br>environment).|Any node (intermediate or leaf) can<br>be vulnerable. Not all graphs<br>contain vulnerable nodes—depends<br>on LLM identifcation.|
|**Edge Values**|_Probability_ of reaching target<br>node_v_0 along path. Derived from<br>probabilistic models<br>(Poisson/geometric distributions).|_Effort score_ (0–1) to reach<br>vulnerable node. 0 = unreachable,<br>1 = same `message`<sup>`_`</sup>`id` as<br>vulnerability. Lower scores =<br>higher effort (Section 3.1.3).|
|**Score/Probability**<br>**Computation**|Probabilistic models capturing<br>attacker behavior and system<br>structure (Poisson/geometric<br>distributions).|Quantitative formulae combining<br>token count, message distance to a<br>vulnerability, and cost to next<br>vulnerable node (Section 3.1.3).|
|**Entry Points**|Multiple entry points merged into<br>synthetic root node (node 0) for<br>unifed structure.|Single entry point: frst node (node<br>1) corresponding to frst<br>`message`<sup>`_`</sup>`id`. Disconnected<br>components reconnected to root.|
|**Modeling Scope**|One cybersecurity exercise or<br>system at a time.|Can model and merge multiple<br>exercises across different systems<br>and targets.|



Figure 2 shows an example of an attack graph constructed within the G-CTR framework. Each node represents a semantically meaningful element from a cybersecurity exercise log, such as domains, IPs, ports, APIs, databases, issues, misconfigurations, and more. Directed edges indicate possible attacker progressions through the scenario. Unlike traditional CTR graphs, this graph reflects an LLM’s interpretation of context and threat progression. 

Using LLMs to infer attack graphs, such as the one shown in Figure 2, provides automation flexibility, but also poses challenges. In bounded attack scenarios, cycles or repeated node visits are not allowed, whereas LLM-generated graphs may unintentionally include cycles despite careful prompting. A theoretical solution is to run the LLM multiple times and apply a geometric distribution to assign decreasing probabilities to attack paths with loops. However, this approach is limited in practice because LLMs produce different graphs on each execution due to their inherent probabilistic behavior. 

Our G-CTR implementation handles LLM-generated graphs with potential cycles and structural issues through multiple post-processing steps: (1) uses NetworkX’s [25] `all`<sup>`_`</sup> `simple`<sup>`_`</sup> `paths` function to extract only acyclic paths, automatically excluding any cycles; (2) recursively removes non-vulnerable leaf nodes to ensure only vulnerable nodes appear as terminal states; (3) adds artificial "leaf_X" nodes with 100% transition probability to each vulnerable node to satisfy game-theoretic requirements that 

_Background_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0008-01.png)


**Figure 2: Attack Graph example** : nodes represent structured information extracted from logs, each containing attributes such as name, message ID, vulnerability status, and additional context. They are categorized into three types: starting nodes (gray), non-vulnerable nodes (light teal), and vulnerable nodes (dark teal), based on their risk level. The orange dashed arrow shows an alternative entry point inferred by the LLM, which is merged into the graph for G-CTR computation because we suppose that everything begins at the first user prompt recorded ( _message_id = 1_ ). In this figure, the attack starts at the “User Prompt” (ID: 1) and progresses through intermediate nodes like “web.com” to reach a key vulnerability-“IDOR Vulnerability” (ID: 4)-which lead to “Data Exfiltration” (ID: 5). 

all targets must be leaf nodes; (4) connects disconnected starting nodes to a single entry point (minimum node ID) via artificial edges; and (5) removes any incoming edges to the designated starting node to ensure a single attack origin—all while prompting the LLM to avoid cycles in the first place (via the system prompt). 

##### **3.1.2 Attack Graphs and Threat Modeling** 

While attack graphs are sometimes informally equated with threat models, they are more accurately understood as _structured artifacts within the threat modeling process_ [26]. Threat modeling is the comprehensive activity of identifying, characterizing, and prioritizing potential threats to a system, typically answering questions about what can go wrong, who might attack, what assets are at risk, and what mitigations exist. Attack graphs and attack trees serve as formalization and visualization techniques within this broader process—they help enumerate attack paths, model adversarial capabilities, and communicate security risks to stakeholders [18]. However, a complete threat model encompasses additional dimensions: asset identification, trust boundaries, attacker profiles, business impact analysis, and mitigation strategies that extend beyond graph structure alone. 

In this context, G-CTR’s automated extraction of attack graphs from live penetration testing logs represents a novel contribution to threat modeling practice. Rather than relying on manually constructed, static threat scenarios developed during design phases, G-CTR generates _evidence-based, dynamic threat representations_ grounded in actual security testing activities. This approach bridges offensive and defensive security: the attack graphs capture real exploitation attempts, tool chains, and vulnerability dependencies observed during AI-driven pentesting, transforming operational data 

_Background_ 

into strategic threat intelligence. While these graphs do not constitute complete threat models on their own, they provide empirically grounded attack path analysis that can inform threat prioritization, defense allocation, and risk assessment—key outputs of comprehensive threat modeling frameworks. Furthermore, by automating graph extraction at the pace of AI-driven security testing, G-CTR enables continuous threat model refinement, addressing a long-standing challenge in traditional threat modeling: keeping threat representations synchronized with evolving system configurations and emerging attack techniques. 

##### **3.1.3 Effort-Based Scoring for LLM-Generated Graphs** 

Unlike CTR’s probabilistic distributions over static graphs, G-CTR quantifies attacker effort through a composite score reflecting the computational resources required to reach vulnerable nodes in dynamically constructed attack graphs. 

Let _Ei_ denote the effort to transition from node _i_ to the next vulnerable node. We define the normalized effort score as a convex combination of three metrics: 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0009-05.png)


where **w** = ( _w_ msg _, w_ tok _, w_ cost) _∈_ ∆<sup>3</sup> forms a probability simplex, and _ϕk_ : N _→_ [0 _,_ 1] are normalized effort functions. 

**Message Distance (** _ϕ_ **msg).** For the log file _ℓ_ with _Jℓ_ total messages, let _mi_ denote messages between node _i_ and its successor vulnerable node. The normalized message effort is: 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0009-08.png)


**Token Complexity (** _ϕ_ **tok).** Let _ti_ represent tokens consumed along edge _i_ , approximated via a standardized tokenizer ( `Qwen/Qwen1.5-0.5B-Chat` ). For total tokens _Tℓ_ =<sup>�</sup><sup>_J_</sup> _j_ =1<sup>_ℓtj_inthelogfile</sup><sup>_ℓ_:</sup> 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0009-10.png)


**Computational Cost (** _ϕ_ **cost).** Given actual token count _x_ with cost _Cx_ , we estimate cost _C_<sup>ˆ</sup> _y_ for heuristic count _y_ as _C_<sup>ˆ</sup> _y_ = ( _y/x_ ) _·Cx_ . Let _ci_ denote the estimated cost for transition _i_ . With total cost _Cℓ_ =<sup>�</sup><sup>_J_</sup> _j_ =1<sup>_ℓcj_:</sup> 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0009-12.png)


The formulation ensures _Ei ∈_ [0 _,_ 1], where higher values indicate greater effort required for exploitation. This metric replaces CTR’s Poisson-based transition probabilities with empirically grounded computational complexity measures suitable for LLM-generated attack graphs.<sup>1</sup> 

##### **3.1.4 Understanding G-CTR Outputs** 

The output of G-CTR represents the solution to a security game between an attacker and a defender. The defender protects selected nodes with limited resources, while the attacker aims to reach a target undetected. G-CTR computes optimal mixed strategies for both, solving the game-theoretic equilibrium described in Section 2.2. 

The output included three main components: 

- **Defender Strategy Table:** A probability distribution over intermediate defendable nodes, indicating where to allocate defenses to minimize attack success. 

> 1Cost-token correlation is addressed via weight adjustment, e.g., ( _w_ cost _, w_ tok) = (0 _._ 3 _,_ 0 _._ 4) when using cloud APIs. 

_Background_ 

- **Attacker Strategy Table:** A list of possible attack paths, each with a probability reflecting how likely a rational attacker is to choose it. 

- **Game Equilibrium:** The success probability both players can guarantee defenders aim to keep it below this threshold; attackers aim to reach or exceed it. 

Figure 3 illustrates a graph modeling potential attack steps from an initial entry point (ID: 1) to key targets: File Upload (ID: 6), Privilege Escalation (ID: 9), and SQL Injection (ID: 7). Each node represents an attack stage, with edges indicating the score or cost of transitioning between them. 

Using this graph, G-CTR computes the optimal mixed strategies for both the defender and the attacker. This results are shown in Figure 3. In this case, the defender’s strategy is expressed as a probability distribution over defendable nodes where defensive resources can be allocated. The results indicate that the defender should allocate approximately 67.35% of their defensive effort to the Lateral Movement node (ID: 8) and 32.65% to the Database node (ID: 4), leaving nodes such as Reconnaissance (ID: 2) and Web Server (ID: 3) undefended due to their lower strategic value. The G-CTR identifies the most likely attack paths based on graph structure and vulnerabilities. The dominant path (67.35%) goes through Reconnaissance _→_ Database _→_ SQL Injection _→_ Privilege Escalation (1 _→_ 2 _→_ 4 _→_ 7 _→_ 9), while a secondary path (32.65%) follows File Upload and Lateral Movement (1 _→_ 2 _→_ 3 _→_ 6 _→_ 8 _→_ 9). All other paths are unlikely due to low success or high detection risk. 

The final equilibrium outcome of this game-theoretic interaction reports a mutual success probability of 3.53%. This value represents the optimal balance point: the attacker cannot guarantee more than a 3.53% chance of reaching the target regardless of their path choice, and the defender cannot reduce this probability further without additional resources. 

By analyzing this example, the Cut-the-Rope framework demonstrates its ability to derive strategic insights that go beyond simple vulnerability analysis, enabling informed, resource-efficient cybersecurity decision-making based on adversarial reasoning. 

_Background_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0011-01.png)


###### (a) Attack Graph Example 

|||**Path ID**<br>**Path Sequence**|**Probability**|
|---|---|---|---|
|**NodeID**|**Probabilit**|||
|<br>|**y**<br>|5<br>1_→_2_→_4_→_7_→_9|0.673528|
|8|0.673528|||
|4|0.326472|1<br>1_→_2_→_3_→_6_→_8_→_9|0.326472|
|||3<br>1_→_2_→_4_→_7|0.000000|
|2|0.000000|||
|3|0.000000|2<br>1_→_2_→_4|0.000000|
|||4<br>1_→_2_→_4_→_7_→_8_→_9|0.000000|



(b) Optimal Defense Strategy 

(c) Attacker Strategy 

##### **Game Equilibrium** 

Defender can keep attacker success below: **0.035280** Attacker can guarantee success probability of: **0.035280** 

###### (d) Game Equilibrium 

###### **Figure 3:** Attack Graph and Equilibrium analysis 

There are also some special cases that affect the outcome of the defender and attacker probabilities. The following consider our implementation of the optimization problem: 

- Starting nodes cannot be defended. If the starting node has direct access to a vulnerable node (i.e., there are no adversary intermediate locations to defend) the optimization will return 0. 

_Background_ 

- A vulnerable node represents a compromised system state or exploited condition that has already been achieved by the attacker. These nodes model the successful exploitation of a vulnerability rather than the vulnerability itself. In the CTR game-theoretic model, defense actions are modeled as inspections along attack paths rather than patching of individual vulnerabilities. While real-world vulnerabilities may indeed be patchable, the model focuses on path-based defense strategies: defenders allocate inspection resources to intermediate nodes to detect and intercept attackers before they reach critical assets. Non-vulnerable nodes represent system components or network positions where such defensive inspections can be deployed to prevent attackers from progressing toward vulnerable states. 

- If there is only one possible exploitation path that the attacker can take, the probability assigned to that path will be 100% and the game equilibrium will be 0. 

- The G-CTR implementation enforces adaptive graph complexity bounds through a piecewiselinear scaling heuristic. This heuristic limits the maximum number of nodes in the generated attack graph based on the total number of messages in the conversation log. Specifically, for shorter conversations (<70 messages), the node limit is set to 12–16% of the message count; for medium-length conversations (70–199 messages), the limit decreases to 6–12%; and for longer conversations ( _≥_ 200 messages), it is further reduced to 3.5–5%. These percentages were empirically tuned to balance graph expressiveness against computational cost: shorter logs benefit from higher node-to-message ratios to capture sufficient detail, while longer logs require stricter limits to prevent excessive graph complexity. Additionally, the resulting node count is clamped to an absolute range of [4, 25] nodes (not percentages) to ensure that very short conversations still produce meaningful graphs and that very long conversations remain computationally tractable. 

#### **3.2 Game-Theoretic AI Digest for** **_Guiding_ Attack and Defense** 

The integration between G-CTR and CAI establishes a closed-loop architecture where game-theoretic reasoning and AI-driven penetration testing mutually reinforce each other. This bidirectional strategic feedback mechanism transforms unstructured security narratives (CAI logs) into structured gametheoretic models (attack graphs and Nash equilibria), which in turn guide subsequent penetration tests toward more focused and effective security assessments. G-CTR’s defender strategies identify critical nodes requiring additional security testing—the high-value defensive chokepoints where resource allocation yields maximum risk reduction. Conversely, attacker strategies highlight optimal exploitation paths—probability-weighted attack sequences that maximize success likelihood given observed system vulnerabilities. 

To operationalize this closed-loop architecture, our game-theoretic AI architecture transforms raw Nash equilibrium computations (generated by G-CTR) into actionable strategic guidance through a _digest generation_ pipeline. Resulting digest is then integrated into the Agent’s system prompt for further guiding the security exercise<sup>2</sup> . The system implements two interpretation modes— **algorithmic** (rulebased template processing) and **LLM** (linguistic reasoning)—both consuming identical game-theoretic inputs but producing strategically distinct outputs. This methodological framework enables rigorous empirical evaluation of the feedback loop’s effectiveness, with detailed results presented in Section 4.3 based on 44 independent penetration testing exercises. 

Figure 4 illustrates the operational feedback loop architecture. The system continuously cycles through four phases: (1) game-theoretic analysis computes Nash equilibria from the current attack graph ( _<_ 5ms computational overhead), (2) digest generation translates equilibrium statistics into strategic guidance (algorithmic mode: _<_ 10ms; LLM mode: 10-46s mean), (3) agents execute tools guided by the injected digest, and (4) observations update the attack graph, triggering the next analysis cycle 

> 2We discovered empirically that guiding Agents via system prompt modifications was preferred. Alternatives explored included user and assistant prompts added to the LLM context. The latter showed worse results and hampered reasoning in mid- to long security exercises 

_Background_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0013-01.png)


<!-- Start of picture text -->
Example Generated Attack Graph with Probabilities Example Guidance Digest added to the Agent’s System Prompt Cybersecurity AI (CAI) Agent Prompt<br>G-CTR Security Analysis (added to the System Prompt)<br>Identified Attack Paths:<br>Path 1: CTF Challenge  → [66%] Nmap Scan → [80%] Open Ports<br>Discovery  → [85%] FTP Service (Port 21)  · · · → [0%] Target<br>(FTP Service (Port 21))<br>Path 2: CTF Challenge  · · · → [30%] FTP Download Attempt 1<br>→ [57%] FTP Service (Port 21)  · · · → [0%] Target (FTP Service<br>(Port 21))<br>Path 3: CTF Challenge  · · · → [17%] FTP Download Attempt 2<br>· · · → [3%] FTP Service (Port 21)  · · · → [0%] Target (FTP<br>Service (Port 21))<br>Critical Bottlenecks (Attack Weaknesses):<br>- FTP Download Attempt 2 -> FTP Service (Port 21): 3.1%<br>success rate<br>- ...: ...<br>Phase 1: Game-Theoretic AI Analysis (G-CTR) Phase 2: Game-Theoretic AI Guidance (Digest Generation) Phase 3: Agent Execution (ReAct)<br>G-CTR < 10ms ≈ 60s<br>Results Algorithmic Act<br>digest<br>(Tools)<br>< 5ms ≈ 10s<br>Nash Strategic Plan<br>Equilibrium Interpretation (LLM)<br>≈ 20s ≈ 28.3s<br>Scan &<br>Attack LLM Update<br>Graph digest (Context)<br>Generation<br>every 5 interactions ( ∼ 80 tools)<br>Time Budget: ≈ 50s Time Budget: ≈ 70s<br><!-- End of picture text -->


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0013-02.png)


**Algorithm 1:** `GenerateDigest()` : Game-Theoretic Digest for Guidance 

**Algorithm 2:** Game-theoretic AI closed-loop feedback algorithm 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0013-05.png)


<!-- Start of picture text -->
Require: Attack graph  G 1: G ← InitializeGraph(),  D ← NULL ▷ Initial attack graph, no digest<br>Ensure: Strategic digest  D (markdown) 2: π ← 0 . 0,  i ← 0 ▷ Strategic position, agent interaction number<br>Phase 1: Game-Theoretic AI Analysis 3: while  π < 1 . 0 ∧ i < I max do ▷ Until success or max interactions<br>1: N ← ComputeNashEquilibrium( G ) ▷ Nash equilibrium from attack graph Phase 3: Agent Execution<br>2: P ← IdentifyAttackPaths( G, N ) ▷ Probability-weighted paths 4: a ← SelectAction( G, D ) ▷ Agent chooses action guided by digest<br>3: S ← InterpretStrategicPosition( N ) ▷ Attacker success probability 5: ( s, o ) ← Execute( a ) ▷ Tool execution, observe outcome<br>6: G ← UpdateGraph( G, a, s, o ) ▷ Refine graph with observations<br>Phase 2: Strategic Interpretation 7: i ← i + 1<br>4:5: CB ←←{ IdentifyCriticalNodes( e, p ) ∈ P | p < ( P, G 0 . 95) } ▷ High-variance ▷ Bottlenecks:decision p < points95% 8: if  i mod 5 = 0 then ▷ Trigger every 5 interactions ( ∼ 80 tools)<br>6: H ←{ ( e, p ) ∈ P | p > 0 . 90 } ▷ High-risk: p > 90% Phase 1: Game-Theoretic AI Analysis<br>7:8: if mode D ← = FormatTemplate algorithmic then ( P, C, B, H ) ▷ Rule-based digest 10:9: Nπ ←← ComputeNashEquilibriumExtractAttackerValue( N )( G ) ▷ ▷ UpdateRecomputestrategicequilibriumposition<br>9: else ▷ mode = llm<br>10: prompt ← ConstructPrompt( G, N, P, S ) Phase 2: Strategic Interpretation<br>11: D ← LLMInference( alias1 ,  prompt , T  =0 . 3) 11: D ← GenerateDigest( G, N ) ▷ Update strategic guidance<br>12: if  D = NULL then ▷ API failure  → fallback 12: end if<br>13: D ← FormatTemplate( P, C, B, H ) 13: end while<br>14: end if<br>15: end if 14: return  G, π ▷ Final attack graph and strategic outcome<br>16: return  D<br><!-- End of picture text -->

**Figure 4:** Game-Theoretic AI closed-loop feedback architecture with three operational phases. The example attack graph (top-left) shows probability-weighted paths computed by G-CTR analysis. Strategic guidance using algorithm 1 produces the digest (top-center) that gets injected into the CAI agent’s system prompt. The agent then executes security testing (top-right) with graph refinement every 5 interactions ( _∼_ 80 tool calls) by following algorithm 2. Phases 1-2 operate with _≈_ 50s budget, running parallel to Phase 3’s _≈_ 70s cycles for real-time strategic adaptation. 

approximately every 5 interactions. This continuous refinement enables real-time strategic adaptation with negligible computational overhead ( _<_ 2% of total test duration for digest generation). 

The two digest generation modes— `algorithmic` and `llm` —enable controlled empirical evaluation of strategic interpretation. Both modes consume identical Nash equilibrium inputs (game values, defender resource allocations, probability-weighted attack paths) but employ fundamentally different 

_Results_ 

translation mechanisms as formalized in Algorithm 1. _Bottlenecks_ (p < 95%) and _high-risk transitions_ (p > 90%) are opposite ends of the attack path spectrum: bottlenecks are weak attack transitions where the defender has advantage andthe attacker struggles to succeed, while high-risk transitions are strong attack transitions where the attacker succeeds easily and defenses are minimal. From a game-theoretic perspective, bottlenecks show where the attacker needs to improve capabilities or find alternatives, while high-risk transitions show where the defender should prioritize hardening efforts— together they reveal the strategic balance of power across the attack graph. The `algorithmic` mode applies fixed thresholds ( _p >_ 0 _._ 9 for high-risk transitions, _p <_ 0 _._ 5 for bottlenecks) and assembles markdown templates via deterministic string concatenation. The `llm` mode sends all CTR data to the `alias1` model with a 350-word structured prompt (temperature=0.3) requesting interpretation across five sections: attack paths, bottlenecks, critical nodes, high-risk transitions, and tactical guidance. 

Algorithm 1 details the complete digest generation process, showing how both modes share a common preprocessing pipeline before diverging at the interpretation stage. The algorithmic branch assembles markdown sections via template formatting functions, while the LLM branch constructs a structured prompt and invokes external model inference. The fallback mechanism (line 12) ensures robustness: if LLM inference fails, the system automatically reverts to algorithmic mode. Across 44 tests (Section 4.3), zero digest generation failures occurred: when LLM mode encounters API errors or timeouts, the system automatically falls back to algorithmic mode, guaranteeing agents always receive strategic guidance. This operational robustness—zero test failures attributable to digest unavailability—validates the architectural decision to maintain both modes. The fallback mechanism proved essential for production deployment: while LLM mode provides superior performance (42.9% success rate vs 20.0%, as seen in Section 4.3), the algorithmic mode ensures system resilience against external service dependencies at negligible additional implementation cost. Algorithm 2 presents the ReAct agent execution methodology augmented with the game-theoretic AI guidance every 5 interactions. 

### **4 Results** 

This section presents a comprehensive evaluation of the G-CTR framework across multiple dimensions, validating both its game-theoretic analysis capabilities and its strategic feedback mechanisms for guiding cyber attack and defense operations. Our evaluation is structured in four complementary parts. First, we present a **qualitative comparison** of attack graph quality (Section 4.1, Table 2), contrasting LLM-generated outputs with human expert annotations across five real-world cybersecurity exercise domains to assess structural accuracy, vulnerability identification, and logical coherence. Second, we provide a **quantitative assessment** of LLM automation performance (Section 4.2), measuring time efficiency, cost reduction, and computational overhead relative to manual expert analysis. Third, we evaluate the **efficiency of the strategic feedback loop** for guiding enhanced penetration testing (Section 4.3), demonstrating for the `shockwave-report` cyber range challenge [27] how game-theoretic digest generation (Algorithm 1) translates Nash equilibrium computations into actionable guidance that improves CAI agent effectiveness across 44 independent attempts of this challenge. Finally, we present **ablation studies** (Section 4.4) examining the impact of individual architectural components, including digest generation modes (algorithmic vs. LLM-based interpretation), feedback frequency, and strategic interpretation mechanisms. Together, these evaluations demonstrate that G-CTR not only automates attack graph generation with high fidelity but also closes the strategic feedback loop, enabling gametheoretic reasoning to guide operational security assessments in real-time. 

#### **4.1 Qualitative Comparison: Graph Quality of Human Experts vs. LLMs** 

This subsection presents a qualitative comparison of attack graphs from LLMs and human experts, summarized in Table 2. The analysis focuses on structural accuracy (e.g., node count, vulnerability 

_Results_ 

nodes) and logical coherence in representing attack scenarios, evaluating both the correctness and completeness of vulnerability identification and scenario flow. 

|**Domain**<br>**Graph**<br>**Source**|**#N.**|**#V.**|**Id.**|**Scenario Representation**|
|---|---|---|---|---|
|`gpt-4o`|4|1|✓|Overly simplistic; it fails to convey the procedu-<br>ral complexity of the exercise (e.g., omission of<br>key elements like the IP address).|
|**kolesa.kz**<sup>_C_</sup><br>`o3`|6|1|✓|It includes all essential information.|
|`grok-4`|5|1|✓|It includes all essential information.|
|`claude`<br>`sonnet 4`|8|1|✓|Comprehensive. Includes all essential informa-<br>tion along with relevant details, such as trial–<br>and–error steps and fnal report generation.|
|`alias0`|7|1|✓|Correct overall; includes trial–and–error, but it<br>does not mention the fnal report. Node selec-<br>tion and information are appropriate.|
|**Human**|9|1|–|–|
|`gpt-4o`|6|1|✗|Simplistic; it notes the API is vulnerable but<br>fails to pinpoint the Insecure Direct Object Ref-<br>erence (IDOR).|
|**mercadolibre.com**<sup>_D_</sup><br>`o3`|6|1|✓|Accurate and complete, correctly identifying the<br>IDOR and scenario complexity, but assumes im-<br>mediate exploitability, omitting trial–and–error.|
|`grok-4`|7|1|✓|It includes all essential information.|
|`claude`<br>`sonnet 4`|7|1|✓|Comprehensive. Includes all essential informa-<br>tion along with relevant details, such as trial–<br>and–error steps and fnal report generation.|
|`alias0`|7|1|✓|Accurate; appropriate node selection. Demon-<br>strates fow through trial-and-error and fnal re-<br>port.|
|**Human**|7|2|–|–|
|`gpt-4o`|8|3|✓|Comprehensive. Includes all essential informa-<br>tion along with relevant details, such as trial–<br>and–error steps and fnal report generation.|
|**pornbox.com**<sup>_E_</sup><br>`o3`|9|2|✓|Accurate and complete, correctly identifying the<br>vulnerabilities and scenario complexity, but as-<br>sumes immediate exploitability, omitting trial–<br>and–error.|
|`grok-4`|9|4|✓|Comprehensive. Includes all essential informa-<br>tion, including trial-and-error steps and fnal<br>PoC generation. Effectively connects discovered<br>vulnerabilities, notably through node ID:3 redi-<br>rection.|
|`claude`<br>`sonnet 4`|9|4|✓|Comprehensive, with key details covered. Node<br>selection is strong, though some labeled vulner-<br>abilities are questionable.|



_Continued on next page_ 

_Results_ 

Table 2 – _Continued from previous page_ 

|**Domain**<br>**Graph**<br>**Source**|**#N.**|**#V.**|**Id.**|**Scenario Representation**|
|---|---|---|---|---|
|`alias0`|9|3|✓|It includes all essential information and effec-<br>tively selects node information and vulnerable<br>nodes.|
|**Human**|8|3|–|–|
|`gpt-4o`|12|1|✓|Good overall; covers all key details, including<br>trial–and–error.<br>Effectively fnd the SSL Cer-<br>tifcate Mismatch vulnerability. Relevant omis-|
|**hm.com**<sup>_F_</sup>||||sions: subdomain missing in node ID (though<br>noted in extra info document) and hallucinated<br>node numbering using `message`<sup>`_`</sup>`id` instead of<br>consistent IDs.|
|`o3`|9|1|✓|Comprehensive. Includes trial–and–error and f-<br>nal PoC. Correct nodes identifed, but path 1–9<br>omits node 6; should be 1–6–9.<br>Whether this<br>omission is an issue is debatable.|
|`grok-4`|13|1|✓|Comprehensive. Includes trial-and-error and f-<br>nal PoC. While nodes are correctly identifed,<br>the representation could be more concise, with<br>potential for node merging.|
|`claude`<br>`sonnet 4`|13|1|✓|Comprehensive. Covers all key details, includ-<br>ing trial–and–error and fnal PoC. Maintains co-<br>herent fow with well–connected steps through-<br>out the scenario.|
|`alias0`|13|1|✓|Comprehensive.<br>It includes all essential infor-<br>mation.|
|**Human**|10|2|–|–|
|`gpt-4o`|14|2|✓|Comprehensive. Covers all key details, includ-<br>ing trial–and–error and fnal PoC. Maintains co-|
|||||herent fow with well–connected steps.|
|**media.guilded.gg**<sup>_G_</sup><br>`o3`|10|2|✓|Comprehensive. Covers all key details, though<br>some trial-and-error steps are missing. Vulnera-<br>bility is well represented.|
|`grok-4`|13|2|✓|Comprehensive.<br>Includes trial-and-error and<br>fnal<br>PoC.<br>Maintains<br>clear,<br>sequential<br>fow<br>through a single coherent path. Vulnerability is<br>well represented. Minor aspect: Attack graphs<br>are meant to represent the exercise conceptu-<br>ally, not replicate every step in a single linear<br>path; thus, whether a single path accurately re-<br>fects this abstraction is debatable.|



_Continued on next page_ 

_Results_ 

Table 2 – _Continued from previous page_ 

|**Domain**|**Graph**<br>**Source**|**#N.**|**#V.**|**Id.**|**Scenario Representation**|
|---|---|---|---|---|---|
||`claude`<br>`sonnet 4`|13|4|✓|Comprehensive. Includes trial–and–error and f-<br>nal report.<br>Maintains clear fow.<br>Node selec-<br>tion and information are appropriate. However,<br>some nodes labeled as vulnerable (e.g., node ID:<br>13) do not represent actual vulnerabilities but<br>rather report elements from the exercise.|
||`alias0`|13|4|✓|Representative of the overall exercise, though<br>some nodes could be consolidated to reduce re-<br>dundancy.|
||**Human**|14|2|–|–|



**Table 2:** Qualitative comparison of attack-graph content generated by large-language models (LLMs) and human experts across five exercise domains. `Graph Source` refers to the origin of the graph analyzed in the evaluation. This includes the specific model or the human expert. `#N.` refers to the total number of nodes present in the graph, while `#V.` Nodes indicates how many of those nodes are considered vulnerable within the scenario. `Id.` denotes whether the model (or human) correctly identified the presence of vulnerabilities (✓) or failed to do so (✗). `Scenario Representation` is a qualitative evaluation describing issues observed in the graph, such as hallucinations, overly simple or complex structures, unnecessary data, missing exploration attempts, or missing logical connections. See Appendices C, D, E, F, G for full attack graphs examples and evaluation details. 

In the **kolesa.kz** scenario, `claude-sonnet-4` stood out for producing the most complete and coherent attack graph. It included 8 nodes in total, identifying 1 as vulnerable–closely matching the human–generated reference, which had 9 nodes and 1 vulnerability. Claude’s graph effectively captured the procedural flow, including intermediate steps such as trial–and–error and the generation of a final report. In contrast, `gpt-4o` ’s graph was overly simplistic, containing only 4 nodes and omitting key elements. While both `o3` and `grok-4` generated correct and complete representations with 6 and 5 nodes respectively, their graphs lacked the depth of procedural granularity shown by Claude. `alias0` produced a structurally sound Attack Graph, only missing some information related to the final report. Notably, all models correctly identified the vulnerability in this domain, but the richness and interpretability of the graphs varied significantly. 

In the **mercadolibre.com** exercise, a scenario centered around an IDOR vulnerability, `claude-sonnet -4` and `grok-4` again delivered robust results. Each generated 7-node graphs identifying 1 vulnerable node, reflecting a strong understanding of the attack path. The human expert’s graph (involving 1 human expert) was slightly more granular, with 7 nodes and 2 marked as vulnerable, reflecting a higher sensitivity to nuanced security elements. `o3` produced a 6-node graph with a correct vulnerability identification, although it assumed immediate exploitability and omitted trial-and-error details. `gpt-4o` , while producing a structurally simple 6–node graph, failed to identify the key vulnerability, significantly limiting the usefulness of its representation. `alias0` also generated a 7–node graph and correctly retrieved the IDOR vulnerability. This case highlights how vulnerability detection accuracy, combined with appropriate procedural modeling, is essential to generating actionable graphs. 

The **pornbox.com** scenario was particularly effective in revealing differences in model performance. The human expert constructed an 8-node graph with 3 vulnerabilities, as correctly modeled by `alias0` , while both `claude-sonnet-4` and `grok-4` exceeded this level of detail with 9 nodes and 4 vulnerabilities. Grok and Claude also demonstrated an advanced modeling capability by integrating redirection logic–specifically, using node ID: 3 to connect different paths in the graph. `o3` generated a similarly detailed graph (9 nodes, 2 vulnerabilities), capturing core aspects but omitting some of the more subtle connections. `gpt-4o` produced a graph with 8 nodes and 3 vulnerabilities, matching the human graph in numbers but lacking some of the deeper logical links. 

_Results_ 

In the **hm.com** exercise, which focused on identifying an SSL certificate mismatch, all models correctly detected the vulnerability. However, differences emerged in how they structured the graphs. `claude-sonnet-4` and `grok-4` produced highly detailed graphs with 13 nodes each, while `gpt-4o` and `o3` had 12 and 9 nodes, respectively. The human graph contained 10 nodes, 2 labeled as vulnerable. `gpt-4o` ’s graph, although mostly correct, introduced inconsistencies by using message identifiers instead of coherent node labels, which compromised clarity. `o3` omitted an intermediate node in the attack path, slightly reducing the traceability of the exploit sequence. `Claude-sonnet-4` ’s and `alias0` output maintained a logical progression and included all necessary steps, making it one of the strongest performers in this domain. 

Finally, **media.guilded.gg** represented the most complex scenario in the evaluation. The human expert generated a 14-node graph with 2 vulnerabilities. All models approached or matched this level of detail: `gpt-4o` also created 14 nodes and 2 vulnerabilities, while `claude-sonnet-4` and `grok-4` produced 13 nodes each, though `claude-sonnet-4` labeled 4 as vulnerable, potentially overestimating due to misclassification of informational elements. `claude-sonnet-4` and `grok-4` maintained a clear and coherent path through the graph, effectively mirroring the logical flow of the attack. `o3` delivered a slightly leaner graph with 10 nodes and 2 vulnerabilities, still accurate but missing some trial-anderror steps. `alias0` ’s Attack Graph was consistent, though some nodes could be merged without losing meaning. 

In summary, across five cybersecurity exercise domains, LLMs generally demonstrated strong capabilities to identify relevant nodes that represent key attack stages. Most models accurately flagged vulnerable nodes. Compared to human-generated graphs, which were more comprehensive and detailed, LLMs identified between 70% to 90% of the key nodes found by human experts but often missed finer details, particularly stages like reconnaissance and final reports. 

#### **4.2 Quantitative Evaluation: Performance of LLM Automation vs. Gold Standard/Human Experts** 

To quantify the efficiency and scalability gains of LLM-based automation, we benchmarked five state-ofthe-art language models against gold-standard annotations produced by human security experts across five real-world cybersecurity exercises. Table 3 presents comprehensive performance metrics including execution time, inference cost, computational overhead, and efficiency ratios relative to manual analysis. 

**Time Efficiency.** LLM-based attack graph generation demonstrated substantial temporal advantages over manual annotation. Across all exercises and models, automated generation required 10–46 seconds per exercise, exhibiting task-dependent variation correlated with log complexity (message count and scenario depth). In contrast, human experts required 30–90 minutes per exercise for equivalent graph construction, yielding speedup factors ranging from **60** _×_ **to 245** _×_ relative to manual workflows. Model-specific performance varied systematically: `gpt-4o` achieved the lowest median latency across four of five domains, while `o3` delivered optimal performance (32 seconds) on the most complex exercise ( `media.guilded.gg` , 358 messages). The slowest models, `grok-4` and `alias0` , required 27–41 seconds per execution, remaining two orders of magnitude faster than human annotation. 

**Cost Efficiency.** Economic analysis reveals similarly dramatic cost advantages for automated generation. LLM inference costs ranged from $0.05 to $0.64 per exercise, depending on model architecture and input complexity. Human expert annotation, estimated at a conservative labor rate of $45/hour, cost $22.50–$67.50 per exercise, resulting in **cost reduction factors of 62** _×_ **to 450** _×_ . Cost efficiency varied substantially across models: `o3` and `gpt-4o` consistently achieved the lowest inference costs ($0.05–$0.18), while `claude-sonnet-4` and `alias0` were more expensive ($0.09–$0.64). Notably, the higher-cost models produced qualitatively superior outputs (Section 4.1), suggesting a quality-cost 

_Results_ 

|**Domain**|**LLM Model**|_t_**Attack Graph** (s)|_t_**CTR** (s)<br>|_t_**total** (s)|**Cost ($)**|_tratio_|_cratio_|
|---|---|---|---|---|---|---|---|
||`gpt-4o`|**14**|0.004|**15.0**|0.12|**128**_×_|187_×_|
||`o3`|16|0.003|17|**0.10**s|112_×_|**225**_×_|
|**kolesa.kz**<sup>_C_</sup>|`grok-4`|30|0.003|31|0.15|60_×_|150_×_|
||`claude-sonnet-4`|16|0.003|17|0.16|112_×_|140_×_|
||`alias0`|20|0.003|20|0.35|88_×_|62_×_|
||**Human**|**1800** (30 m)|**—**|**—**|**22.5**|**—**|**—**|
|**mercadolibre.com**<sup>_D_</sup>|`gpt-4o`|**9.4**|0.003|**10**|**0.05**|**191**_×_|**450**_×_|
||`o3`|27|0.004|27|0.05|66_×_|**450**_×_|
||`grok-4`|27|0.004|24|0.07|66_×_|321_×_|
||`claude-sonnet-4`|12|0.003|18|0.09|163_×_|250_×_|
||`alias0`|15|0.003|15|0.16|116_×_|145_×_|
||**Human**|**1800** (30 m)|**—**|**—**|**22.5**|**—**|**—**|
|**pornbox.com**<sup>_E_</sup>|`gpt-4o`|**11**|0.005|**12**|0.12|**245**_×_|281_×_|
||`o3`|22|0.005|23|**0.11**|122_×_|**306**_×_|
||`grok-4`|27|0.004|28|0.15|100_×_|225_×_|
||`claude-sonnet-4`|13|0.004|14|0.19|207_×_|177_×_|
||`alias0`|23|0.004|24|0.36|113_×_|94_×_|
||**Human**|**2700** (45 m)|**—**|**—**|**33.75**|**—**|**—**|
|**hm.com**<sup>_F_</sup>|`gpt-4o`|**20**|0.004|**21**|0.1|**135**_×_|373_×_|
||`o3`|26|0.004|27|**0.09**|103_×_|**375**_×_|
||`grok-4`|36|0.004|37|0.13|75_×_|259_×_|
||`claude-sonnet-4`|30|0.003|31|0.13|90_×_|259_×_|
||`alias0`|26|0.004|26|0.28|102_×_|120_×_|
||**Human**|**2700** (45 m)|**—**|**—**|**33.75**|**—**|**—**|
|**media.guilded.gg**<sup>_G_</sup>|`gpt-4o`|56|0.004|58|0.19|86_×_|355_×_|
||`o3`|**32**|0.004|**35**|**0.18**|**168**_×_|**375**_×_|
||`grok-4`|41|0.005|44|0.27|131_×_|250_×_|
||`claude-sonnet-4`|38|0.005|41|0.28|142_×_|241_×_|
||`alias0`|46|0.006|47|0.64|115_×_|104_×_|
||**Human**|**5400** (90 m)|**—**|**—**|**67.5**|**—**|**—**|



**Table 3:** Comparison of Attack Graph construction time and cost between LLMs and humans across five domains. For each domain, five LLMs generate Attack Graphs, which are compared against a human expert annotation Gold Standard. _t_ **Attack Graph** denotes the time required by an LLM to generate an attack graph; for humans, it reflects expert annotation time. _t_ **CTR** represents the time taken to compute the CTR pipeline. _t_ **total** is the end–to–end execution time of the full `G-CTR` pipeline. **Cost** reflects the LLM inference cost or equivalent human labor cost. In the latter case, we assume an hourly rate of $45. _tratio_ and _cratio_ express relative time and cost efficiency, normalized against the human baseline. For numbers above 10 we do not show decimals; for values below 10, we keep one decimal and round accordingly. For _t_ **CTR** , we preserve three decimal places, rounding the last digit. 

tradeoff wherein premium models deliver enhanced structural completeness and logical coherence at 2–4 _×_ higher inference cost while maintaining 100 _×_ + cost advantages over human annotation. 

_Results_ 

**Computational Overhead of Game-Theoretic Analysis.** The Cut-the-Rope (CTR) game-theoretic computation layer, responsible for Nash equilibrium calculation and strategic analysis, introduced negligible computational overhead: all CTR operations completed in under 5 milliseconds across all exercises and graph sizes. This empirical result confirms that the computational bottleneck in G-CTR lies exclusively in LLM inference rather than game-theoretic reasoning, validating the architectural decision to integrate CTR analysis without compromising real-time performance requirements. 

**Model Selection and Performance Tradeoffs.** Cross-model comparison reveals systematic tradeoffs between efficiency and output quality. `gpt-4o` and `o3` optimize for speed and cost, delivering adequate structural accuracy for high-throughput or resource-constrained deployments. Conversely, `claude-sonnet-4` and `alias0` prioritize graph completeness and interpretability, exhibiting superior performance on complex multi-stage exercises such as `hm.com` (118 messages) and `media.guilded.gg` (358 messages). These empirical performance characteristics enable context-dependent model selection: rapid triage and large-scale assessments benefit from lightweight models, while high-stakes investigations requiring maximal fidelity justify premium model deployment. 

#### **4.3 Game-Theoretic AI Digest Results for Guiding Attack and Defense** 

This subsection presents empirical validation of this feedback loop architecture through 44 independent penetration testing exercises targeting the `shockwave`<sup>`_`</sup> `report` Cyber Range Challenge (Shellshock CVE-2014-6271 vulnerability). We demonstrate how Nash equilibrium analysis operationally guides offensive security testing in real-time scenarios, quantifying improvements in vulnerability discovery rates, time-to-exploitation and economic efficiency. The empirical evidence establishes that strategic game-theoretic guidance enables autonomous security systems to not merely find vulnerabilities, but to reason strategically about their exploitation in a more efficient and effective manner. 

The evaluation employed a randomized comparative design across three configurations, all using the state-of-the-art [27] `alias1` Cybersecurity LLM<sup>3</sup> and using the `red`<sup>`_`</sup> `teamer` Agent in CAI. The configurations were: No G-CTR baseline ( _n_ = 15), G-CTR with LLM-generated strategic digests ( _n_ = 14), and G-CTR with algorithmic rule-based digests ( _n_ = 15). All tests targeted identical infrastructure ( `shockwave`<sup>`_`</sup> `report` Cyber Range CTF) with maximum duration 2410 seconds (40 minutes). Success was defined as flag extraction within time limit. Table 4 summarizes performance results. 

**Table 4:** Empirical performance comparison: algorithmic vs. LLM digest modes ( _n_ = 44 tests).<sup>_†_</sup> The cost per success is calculated based on the pricing of the `alias1` model (5 EUR per 1M tokens in + out) and the total cost of the test and the number of successful tests. The reason why the cost per success is higher for the baseline is because despite having a shorter duration, it had more tool calls which saturated faster the cost per LLM interaction. 

|**Mode**|**Tests**|**Successes**|**Success Rate**|**Avg Duration**|**Tool Variance**|**Cost/Success**|
|---|---|---|---|---|---|---|
|**No G-CTR**|15|2|13.3%|16.7 min|1.6_×_|$2.71<sup>_†_</sup>|
|(baseline)|||||||
|**G-CTR** **`algorithmic`**|15|3|20.0%|22.5 min|6.2_×_|$0.32|
|∆over baseline||+1|+6.7 pp|-5.8 min|-3.9_×_|8.5_×_ better|
|**G-CTR** **`llm`**|14|6|42.9%|20.2 min|1.2_×_|$0.12|
|∆over baseline||+4|+29.6 pp|-3.5 min|1.3_×_ better|23_×_ better|
|**Digest comparison**<br>(∆`llm` vs. `algorithmic`)||**+3**|**+22.9 pp**|**+2.3 min**|**5.2**_×_ **lower**|**2.7**_×_ **better**|



The 44-test evaluation dataset enables direct comparison of digest generation modes under controlled conditions. The `llm` digest generation achieves a 29.6% higher success rate than `algorithmic` 

> 3Refer to `https://aliasrobotics.com/alias1.php` for more details and to [27] for benchmark results. 

_Results_ 

mode (42.9% vs 20.0%) despite similar Nash equilibrium inputs<sup>4</sup> . This isolates the contribution of LLM strategic interpretation: both modes receive similar game-theoretic analysis, but LLM digests provide contextual guidance that agents operationalize more effectively. The 5.2 _×_ lower tool usage variance (1.2 _×_ vs 6.2 _×_ range) indicates more consistent agent behavior under LLM guidance, suggesting the LLM interpretation reduces behavioral uncertainty. 

Figure 5 visualizes the temporal efficiency analysis, accounting for failure probability in expected time calculations. While G-CTR `llm` -guided successful tests exhibit 21% longer individual duration (20.2 vs 16.7 min), the 3.21 _×_ improvement in success probability dominates the performance metric, yielding 2.67 _×_ reduction in expected time to vulnerability discovery. The expected time metric (E[ _T_ success]) properly accounts for the cost of failed attempts as shown in Equation 7: 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0021-03.png)


<!-- Start of picture text -->
E[ T success] = P success T avg = 11247126min . 5minmin NoG-CTRG-CTRG-CTR llmalgorithmic :: 0160 . 20133 . 429 . 7 . 2 : 022 . 200 . 5 (7)<br>126<br>120 112 . 5<br>100<br>80<br>60<br>47<br>40<br>22 . 5 20 . 2<br>16 . 7<br>20<br>0<br>No G-CTR G-CTR algorithmic G-CTR llm<br>Average Time Duration ( T avg) Expected Time E[ T success] (Eq. 7)<br>(minutes)<br>Time<br><!-- End of picture text -->

**Figure 5:** Time-to-vulnerability comparison across methods. _•_ Average Time Duration ( _T_ avg). _•_ Expected time E[ _T_ success] = _T_ avg _/P_ success from Eq. 7, which accounts for failed attempts. Despite 21% longer raw duration (20.2 vs 16.7 min), G-CTR `llm` delivers a 2.67 _×_ reduction in expected time (126 _→_ 47 min) relative to No G-CTR because of its 3.21 _×_ higher success probability. 

Taken together, these results confirm that `llm` digest-based strategic guidance delivers **substantial improvements** to offensive cybersecurity exercises in Cyber Range CTFs, achieving a remarkable 29.6 percentage point increase in success rate (from 13.3% to 42.9%—a 222% relative improvement), reducing the expected time to success by 2.67 _×_ (126 _→_ 47 min) and the cost per success by 23 _×_ (from $2.71 to $0.12). 

#### **4.4 Ablations** 

To substantiate the aggregate performance trends reported in Section 4.3, we conduct ablation experiments across two complementary evaluation regimes. The first subsubsection extends the analysis of the `shockwave`<sup>`_`</sup> `report` Cyber Range Challenge, examining in detail how the two digest generation strategies ( `algorithmic` vs. `llm` ) impact system performance. The second subsubsection transitions 

> 4Despite using the same game-theoretic method, we can’t guarantee they are identical but similar due to the stochastic nature of the LLMs used to produce the corresponding attack graph as depicted in Figure 4. 

_Results_ 

to Attack and Defense (A&D) CTF exercises, evaluating how the same architectural feedback loop performs under competitive, score-driven conditions that better reflect real-world cybersecurity operations. 

##### **4.4.1 LLM Digest vs. Algorithmic Digest: Isolating the Interpretation** 

We isolate the role of LLM interpretation by further dissecting the results from Section 4.3. Table 5 summarizes the architectural characteristics and empirical observables recorded across the comparison cohort. Table 6 aggregates the primary outcome metrics, enabling direct quantification of success probability, runtime, tool-use variance, and economic efficiency for each digest mode. 

**Table 5:** Architectural and empirical comparison of algorithmic and LLM digest modes derived from 44 cyber-range penetration-testing exercises (additional metrics in Section 4.3). 

|**Property**|**algorithmic Mode**|**llm Mode**|
|---|---|---|
|**Success Rate**|20.0% (3/15 tests)|**42.9%** (6/14 tests)|
|**Implementation**|Rule-based template processing<br>with fxed thresholds|LLM inference (`alias1`) with<br>350-word structured prompt|
|**Strategic**|Deterministic thresholds: _p >_0_._9|Reasoning with contextual|
|**Interpretation**|(high-risk),_p <_0_._5 (bottleneck)|probability interpretation and<br>tactical recommendations|
|**Latency**|Instant (_<_10ms)|10–46s (mean: 28.3s_±_ 11.2s)|
|**Output Consistency**|100% deterministic|Stochastic (temp=0.3); 5.2_×_ lower<br>behavioral variance|
|**Tool Usage Variance**|6.2_×_ range (512–3186 tools)|**1.2**_×_ range (860–1034 tools)|
|**Cost per Success**|$0.32|**$0.12** (2.7_×_ more effcient)|
|**Failure Mode**|Guaranteed output if CTR data<br>exists|API errors_→_fallback to<br>algorithmic mode|



**Table 6:** Aggregate performance metrics for algorithmic and LLM digest generation modes. 

|**Confguration**|_n_|**Success Rate**|**Avg Duration**|**Tool Variance**|**Cost/Success**|
|---|---|---|---|---|---|
|G-CTR `algorithmic`|15|20.0% (3/15)|22.5 min|6.2_×_|$0.32|
|G-CTR `llm`|14|42.9% (6/14)|20.2 min|1.2_×_|$0.12|
|∆**(****`llm` -** **`algorithmic`)**||**+22.9 pp**|**-2.3 min**|**-83%**|**-$0.20**|



Across the 29 matched digest runs (15 `algorithmic` , 14 `llm` ), swapping the interpreter ( `algorithmic` vs. `llm` ) more than doubles observed task success (20.0% _→_ 42.9%, +22.9 percentage points). This ablation demonstrates that the `llm` digest mode provides a superior interpretation of the game-theoretic signals compared to the `algorithmic` mode. 

The same intervention tightens behavioral dispersion. Tool-use range contracts from 6.2 _×_ (512– 3186 invocations) to 1.2 _×_ (860–1034), implying that the `llm` digest acts as a variance-reducing controller even though the model samples with temperature 0.3. Results suggest that the sampling stochasticity is dominated by the constraints (the context) supplied in the `llm` digest processing, not by randomness in the underlying LLM model. Further experiments with different temperature values would help to confirm this hypothesis. 

Efficiency markers shift in concert. Average episode duration decreases by 2.3 minutes despite the 28.3 s _±_ 11.2 s digest generation latency, demonstrating that LLM guidance more than compensates for its inference overhead. Cost per successful breach falls from $0.32 to $0.12 (2.7 _×_ improvement), 

_Results_ 

indicating that higher success probability and lower resource dispersion jointly reduce marginal compute expenditure. 

With the cyber-range effects established, we next test whether the same control advantage (via the `llm` digest mode) persists under live Attack and Defense CTF scoring, which better reflects real-world cybersecurity conditions. 

##### **4.4.2 Studying Offensive and Defensive Enhancements in Realistic Cybersecurity Exercises** 

We transition to evaluating the full game-theoretic AI architecture and G-CTR implementation in Attack and Defense (A&D) CTF scenarios. Unlike the single-agent cyber-range exercises above, A&D CTFs introduce competitive scoring dynamics and simultaneous offensive/defensive operations that better reflect real-world security engagements. This realism stems from several key factors: (1) **Adversarial pressure** , where defenders must actively counter live attacks rather than merely hardening systems against theoretical threats, (2) **Resource competition** , as both sides operate under time and computational constraints that mirror operational security budgets, (3) **Dynamic threat landscapes** , where attack vectors evolve in real-time as defenders implement countermeasures, and (4) **Multiobjective optimization** , requiring teams to balance offensive success against defensive resilience—a fundamental tension present in actual cybersecurity operations where organizations must simultaneously protect assets while maintaining business functionality. For a more detailed description of the A&D CTFs, please refer to [15, 27]. 

**Table 7:** Team configurations and legend used throughout the Attack and Defense experiments. Colors and patterns match Figure 6a. 

|**Confguration**|**Operational Description**|
|---|---|
|**No G-CTR** (baseline)|Red and blue agents act without strategic overlays, relying solely on the `alias1`<br>LLM’s Phase 3 (ReAct) behaviors from Figure 4.|
|**Red G-CTR**|Only the attacker receives G-CTR guidance; the defending agent remains without<br>guidance. Both agents run in parallel, with context separation.|
|**Blue G-CTR**|Only the defender receives G-CTR guidance while the attacker operates without it.<br>Both agents run in parallel, with context separation.|
|**Purple G-CTR**|Both agents, attacker and defender, receive G-CTR guidance with independent<br>attack graphs constructed for each agent. Agents run in parallel and with no<br>context sharing, exposing how dual but uncoupled strategies perform.|
|**Purple G-CTRmerged**|Similar to **Purple G-CTR** but both agents share the same G-CTR attack graph and<br>context, yielding the highest degree of synchronized strategic planning.|



To ablate the impact of different strategic configurations, we used the best performing digest from the cyber-range exercises (the `llm` digest mode) and systematically varied team compositions by controlling how G-CTR guidance gets integrated into the agents of each team. For that purpose, we created various configurations that varied the amount of G-CTR guidance that apply either exclusively to the team’s attacker, exclusively to the team’s defender or to both attacker and defender. We then confront each configuration against the baseline configuration ( **No G-CTR** ). Across all teams and evaluations, agents use the same `alias1` LLM model. Each team runs all its agents with parallel capabilities (refer to [3] for details on CAI’s parallel capabilities). Table 7 formalizes the team compositions used in the Attack and Defense (A&D) experiments. Each entry displays the same glyph that appears in Figures 6a and 6b, ensuring the prose, the table legend, and the stacked-bar visualization share a common color and pattern vocabulary. 

To evaluate G-CTR’s effectiveness in A&D scenarios, we conducted experiments on two “very easy” difficulty challenges: `cowsay` and `pingpong` . Both scenarios feature command injection vulnerabilities and privilege escalation vectors, making them accessible entry points for evaluating strategic guid- 

_Results_ 

ance in adversarial settings. Each experiment consisted of multiple competitive rounds [15] using the combinations of configurations described above. 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0024-02.png)


**(a)** Cowsay Challenge Results. 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0024-04.png)


**(b)** Pingpong Challenge Results. 

**Figure 6:** Attack and Defense (A&D) challenge results comparing different G-CTR team configurations across two scenarios. Outcome distributions are measured across 25 best-of-one matches per team pairings. Stacked bars report the percentage of team1 wins (left), ties (center), and team2 wins (right) for each team configuration. Colors and hatch patterns follow Table 7; all agents use the `llm` digest mode, the `alias1` execution model, and the same CTR timing parameters ( _λa_ = 2 attacker rate, _λd_ = 1 defender rate). 

Figure 6a presents the `cowsay` challenge which introduces shallow exploitation depth but rapid tactical churn, making coordination effects measurable. Figure 6b presents the `pingpong` scenario which requires sustained service uptime in addition to exploit delivery, amplifying the value of defensive foresight. 

Against our baseline **No G-CTR** , **Red G-CTR** achieves a 33.3%/ **42.9** % win/loss ratio in `cowsay` and a 19%/ **23.8** % in `pingpong` , indicating that strategic guidance provides limited benefit for attacker-only guided configurations. We hypothesize that this performance degradation occurs because the guided attacker, despite receiving strategic direction, fails to leverage it effectively in dynamic scenarios. The underlying mechanism appears to be that attackers become fixated on specific exploitation paths that may no longer be viable, and because the system prompt carries significant weight in the guidance mechanism, the guided attacker exhibits reduced responsiveness to contextual updates (the need to pivot to alternative attack vectors). This performance decline supports our conclusion that _attackeronly guidance cannot compensate for an unguided defense_ . 

In contrast, **Blue G-CTR** achieves a high victory fraction ( **57.1** %/28.6% win/loss ratio in `cowsay` and **25** %/15% in `pingpong` ) confirming that defensive guidance provided by G-CTR supplies a large marginal gain. 

**Purple G-CTR** also exceeded baseline performance with **52.9** %/23.5% win/loss ratios in `cowsay` , hinting that activating guidance on both sides stabilizes play without requiring further coordination. This observation is however contradicted by the fact that it struggles in `pingpong` with a 13.6%/ **31.8** % win/loss ratio, suggesting that scenario complexity may interact with guidance effectiveness in ways that warrant further investigation. We argue that this contradiction hints at the need for deeper exploration of how teams with shared context and merged guidance (utilizing a single attack graph for all team members) might achieve better alignment and communication, potentially resolving the performance inconsistencies observed across different challenge types. Correspondingly, we propose **Purple G-CTRmerged** , which implements a team reasoning stack with shared context and a single attack graph for all team members. Results of **Purple G-CTRmerged** against our baseline delivers a **38.1** %/33.3% win/loss ratio in `cowsay` and **52.4** %/28.6% in `pingpong` , wins in both scenarios and suggesting that this last configuration with _merged_ guidance (shared context and a single attack graph) delivers the best performance in both scenarios. 

We challenge this last hypothesis by evaluating the performance of **Purple G-CTRmerged** against **Purple G-CTR** . Results show that **Purple G-CTRmerged** achieves a **55** %/15% win/loss ratio in `cowsay` 

_Discussion_ 

and **42.9** %/14.3% in `pingpong` , confirming our conjecture: _merged_ guidance delivers the best performance. 

Synthesizing across both scenarios, we observe a consistent hierarchy. Purely offensive guidance tops out at a losing record 33.3% vs **42.9** % (0.78: **1** ), showing that attacker-only prompting cannot keep pace with unguided defenses. Defensive-only guidance improves the contest to roughly **2** :1 ( **57.1** % vs 28.6%), while dual guidance without agents sharing context or attack graphs contributes another step change relative to independent dual guidance. In absolute terms, **Purple G-CTRmerged** converts `pingpong` series **52.4** % to 28.6% ( _≈_ **1.8** :1) when facing **No G-CTR** , and it defeats **Purple G-CTR** in `cowsay` **55** % to 15% ( _≈_ **3.7** :1), implying that opponents would need nearly four coordinated wins to offset every merged victory. Because all teams run the same `alias1` executor and `llm` digest, these ratios isolate the effect of marrying generative interpretation with Nash-equilibrium control. The resulting game-theoretic AI architecture (LLM+G-CTR) halves opponent success, compresses attacker variance, and delivers a reproducible breakthrough: under identical tooling and budgets, game-theoretic guidance lets AI teams execute with the decisiveness of coordinated human red/blue cells, establishing a new breakthrough performance for realistic cybersecurity exercises. 

### **5 Discussion** 

In this study, we have presented and evaluated G-CTR, a game-theoretic AI framework for guiding cyber attack and defense using LLMs. Through quantitative evaluation across five real–world cybersecurity exercises, we demonstrated that G-CTR offers substantial gains in **scalability** , **automation** , and **cost-efficiency** . LLMs generated complete attack graphs in under 40 seconds, compared to up to 90 minutes for human experts, achieving a speedup between **60** _×_ and **245** _×_ . Inference costs ranged from $0.05 to $0.28, **reducing** analysis **costs by over 140** _×_ relative to expert labor. The G-CTR layer introduced negligible overhead (<5ms), confirming that the primary computational cost lies in LLM inference. While gpt-4o and o3 delivered the best balance of speed and cost, Claude Sonnet 4 consistently produced the most structurally complete and logically coherent graphs, especially in complex scenarios. 

Qualitatively, LLMs showed strong capabilities in identifying key attack nodes–particularly in vulnerable stages–with an average node correspondence of 70–90% compared to expert-generated graphs. Simpler logs led to highly accurate outputs, while more complex scenarios revealed subtle model weaknesses, including hallucinated nodes, semantic misclassifications, and occasional omissions of steps. `gpt-4o` was more prone to hallucinations, whereas `claude-sonnet-4` provided more context and detailed outputs, although at a higher cost. Overall, while LLMs tend to emphasize direct attack paths and occasionally oversimplify nuanced stages, G-CTR shows promise as a scalable, automated complement to human-driven security analysis, particularly when rapid or repeated assessments are needed. 

While G-CTR has shown strong performance in both efficiency and output quality, several areas offer promising directions for future enhancement. One such factor is the configuration of graph complexity, particularly the minimum and maximum number of nodes. Across five domains (Table 2), instructing LLMs to emit 6–15 nodes with at most four vulnerable stages yielded the most faithful graphs; however, adaptive tuning based on scenario complexity could further improve completeness and interpretability in edge cases. 

Another area of opportunity lies in prompt engineering. We observed that different LLMs respond better to tailored prompt structures, suggesting that customized system prompts per model could unlock further performance gains. This opens the door to more fine-grained control over LLM behavior, especially as new models and capabilities emerge. 

Our analysis reinforces that model choice should be aligned with operational needs. Lighter models like `gpt-4o` and `o3` offer speed and cost–efficiency ideal for triage or scalable analysis, while more detailed outputs from Claude Sonnet 4 may be preferable in high-risk or high-stakes investigations. These tradeoffs highlight the flexibility of G-CTR in adapting to different deployment contexts, from automated threat assessments to analyst-in-the-loop workflows. 

_Conclusion_ 

Extending the framework to Attack and Defense CTFs (Figures 6a and 6b) reveals a similar hierarchy of guidance strategies. Purely offensive prompting remains net-negative (33.3% wins vs 42.9% losses, 0.78:1), defensive-only guidance pushes results to roughly 2:1 (57.1% vs 28.6%), and dual guidance with shared graphs adds another step change. The **Purple G-CTRmerged** team—where red and blue agents share both context and G-CTR attack graph—wins `pingpong` matches 52.4% to 28.6% (~1.8:1) against **No G-CTR** and defeats **Purple G-CTR** in `cowsay` 55% to 15% (~3.7:1). Because every configuration reuses the same `alias1` executor and `llm` digest, these ratios isolate the benefit of combining generative semantics with Nash-equilibrium coordination, establishing **Purple G-CTRmerged** as a reproducible, best-in-class agent for live adversarial play. 

In summary, G–CTR demonstrates that combining LLM-based automation with lightweight gametheoretic reasoning enables fast, cost-effective, and contextually rich attack graph generation. While human expertise remains unmatched in capturing subtle and indirect attack behaviors, LLMs are rapidly closing the gap and can already support large-scale or time-sensitive threat assessments. 

### **6 Conclusion** 

This paper presented a game-theoretic AI guidance architecture that unifies automated penetration testing with strategic defense planning. At its core lies Generative Cut-the-Rope (G-CTR), the component that extracts attack graphs, computes Nash equilibria, and feeds guidance back into CAI agents. Our key findings demonstrate both the feasibility and practical impact of this architecture: 

**Automated Graph Generation Works.** LLMs successfully extract structured attack graphs from unstructured CAI logs with 70-90% node correspondence to expert annotations, achieving 60-245 _×_ speedup. This automation eliminates the primary bottleneck in applying game-theoretic analysis to real-world security data. 

**Strategic Feedback Enhances Pentesting.** By computing optimal attack/defense strategies and feeding them back to CAI, G-CTR enables focused security assessments that prioritize high-value targets. Algorithm 1 serves as the critical translation layer, converting Nash equilibrium computations into actionable strategic guidance that CAI agents consume during penetration testing. Our empirical evaluation across 44 independent exercises demonstrates that this game-theoretic guidance substantially improves pentesting effectiveness: LLM-mode digests achieved 42.9% success rates compared to 20.0% for algorithmic templates, with the strategic feedback loop enabling agents to identify high-risk attack paths (transitions with _p >_ 0 _._ 9) and recognize defensive bottlenecks (transitions with _p <_ 0 _._ 95) that would otherwise remain obscured in unguided exploration. 

**Breakthrough Attack and Defense Guidance.** When applied to simultaneous red/blue competitions, the same LLM digest plus G-CTR coordination unlocks a new best-in-class agent. In two realistic Attack and Defense cybersecurity exercises (Figures 6a and 6b), the **Purple G-CTRmerged** configuration—where both teams share a single strategic context and attack graph—wins matches roughly 1.8:1 against the LLM-only baseline and 3.7:1 against independently guided teams. Purely offensive prompting, by contrast, remains sub-baseline (33.3% to 42.9%). This establishes GenAI+gametheory coupling as the differentiator for multi-agent cyber exercises. 

**Reducing Ambiguity and Suppressing Hallucinations.** Hallucinations are mitigated by constraining the LLM’s reasoning with an external, continuously updated game-theoretic control signal: G-CTR transforms the AI’s own context (or logs) into an attack graph, computes equilibria, and injects a digest that anchors the model to the statistically strongest paths and chokepoints. This keeps the LLM focused on what is actually happening in the environment rather than drifting into speculative or irrelevant actions. The experimental results provide measurable evidence of this effect: in a 44-run cyber-range benchmark, adding the G-CTR digest more than doubled success rates (13.3% _→_ 42.9%), reduced tool-use variance by 5.2 _×_ , and cut cost-per-success by 23 _×_ , all indicators of reduced hallucination and tighter behavioral coherence. This effectiveness stems from G-CTR’s bidirectional translation capability: it converts narrative AI security outputs into formal game-theoretic inputs (Nash equilibria, probability-weighted paths, critical nodes) and then produces strategic guidance that integrates seam- 

_REFERENCES_ 

lessly back into agent system prompts via Algorithm 1. This closed-loop architecture—where attack graphs inform strategic analysis, which in turn guides subsequent penetration testing through digest injection—enables continuous refinement and represents a concrete step toward cybersecurity superintelligence by collapsing the LLM’s search space and keeping the model tightly anchored to the most strategically relevant parts of the problem. 

Future work must now optimize the balance between hallucination mitigation and creative attack discovery—exploring whether controlled randomness (e.g., temperature schedules) can unlock novel strategies without sacrificing fidelity, while refining LLM interpretation to handle even richer telemetry. Building on that foundation, we will consider run adversarial-robustness exercises against best human red teams. 

Taken together, these advances position the proposed game-theoretic AI architecture—and its G- CTR core—as a decisive step toward cybersecurity superintelligence that not only find vulnerabilities but strategically orchestrate how AI attackers and defenders respond in realistic, high-pressure environments. 

### **7 Acknowledgements** 

This research has been partly funded by the European Innovation Council (EIC) as part of the accelerator project “RIS” (GA 101161136) - HORIZON-EIC-2023-ACCELERATOR-01 call. Thanks to the Alias Robotics team members for their various reviews. Thanks also to Alfonso Muñoz Muñoz for his strategic game-theoretic insights and critical review of the scientific value of our work. 

### **References** 

- [1] Gelei Deng, Yi Liu, Víctor Mayoral-Vilches, Peng Liu, Yuekang Li, Yuan Xu, Tianwei Zhang, Yang Liu, Martin Pinzger, and Stefan Rass. Pentestgpt: An llm-empowered automatic penetration testing tool, 2024. URL `https://arxiv.org/abs/2308.06782` . 

- [2] Víctor Mayoral-Vilches. Offensive robot cybersecurity. _arXiv preprint arXiv:2506.15343_ , 2025. 

- [3] Víctor Mayoral-Vilches, Luis Javier Navarrete-Lozano, María Sanz-Gómez, Lidia Salas Espejo, Martiño Crespo-Álvarez, Francisco Oca-Gonzalez, Francesco Balassone, Alfonso Glera-Picón, Unai Ayucar-Carbajo, Jon Ander Ruiz-Alcalde, Stefan Rass, Martin Pinzger, and Endika Gil-Uriarte. Cai: An open, bug bounty-ready cybersecurity ai, 2025. URL `https://arxiv.org/abs/2504.06017` . 

- [4] Alias Robotics. Cai: Cybersecurity ai - an open bug bounty-ready artificial intelligence, 2025. URL `https://github.com/aliasrobotics/cai` . Accessed: 2025-06-27. 

- [5] Stefan Rass, Sandra König, and Emmanouil Panaousis. Cut-the-rope: A game of stealthy intrusion. In _Proceedings of the Conference on Decision and Game Theory for Security_ , pages 1–12, 09 2019. 

- [6] Stefan Rass, Sandra König, Jasmin Wachter, Víctor Mayoral-Vilches, and Emmanouil Panaousis. Game-theoretic apt defense: An experimental study on robotics. _Computers & Security_ , 132: 103328, 2023. ISSN 0167-4048. doi: https://doi.org/10.1016/j.cose.2023.103328. URL `https: //www.sciencedirect.com/science/article/pii/S0167404823002389` . 

- [7] Stefan Rass, Beniamin Radomir Jablonski, and Víctor Mayoral-Vilches. (poster) zero-day risk estimation using security games. In _International Conference on Game Theory and AI for Security_ , pages 321–325. Springer, 2025. 

- [8] CVE Program. Cve-2014-6271 record. `https://www.cve.org/CVERecord?id=CVE-2014-6271` , 2014. URL `https://www.cve.org/CVERecord?id=CVE-2014-6271` . Common Vulnerabilities and Exposures, accessed January 2026. 

_REFERENCES_ 

- [9] Florian Weimer. Re: Cve-2014-6271: remote code execution through bash. `https://seclists. org/oss-sec/2014/q3/650` , 2014. URL `https://seclists.org/oss-sec/2014/q3/650` . oss-sec mailing list archive, 24 Sep 2014. 

- [10] Víctor Mayoral-Vilches. Cybersecurity ai: The dangerous gap between automation and autonomy. _arXiv preprint arXiv:2506.23592_ , 2025. 

- [11] Víctor Mayoral-Vilches, Jasmin Wachter, Cristóbal RJ Veas Chavez, Cathrin Schachner, Luis Javier Navarrete-Lozano, and María Sanz-Gómez. Cai fluency: A framework for cybersecurity ai fluency. _arXiv e-prints_ , pages arXiv–2508, 2025. 

- [12] Víctor Mayoral-Vilches and Per Mannermaa Rynning. Cybersecurity ai: Hacking the ai hackers via prompt injection. _arXiv preprint arXiv:2508.21669_ , 2025. 

- [13] Víctor Mayoral-Vilches. Cybersecurity ai: Humanoid robots as attack vectors. _arXiv preprint arXiv:2509.14139_ , 2025. 

- [14] Víctor Mayoral-Vilches. The cybersecurity of a humanoid robot. _arXiv preprint arXiv:2509.14096_ , 2025. 

- [15] Francesco Balassone, Víctor Mayoral-Vilches, Stefan Rass, Martin Pinzger, Gaetano Perrone, Simon Pietro Romano, and Peter Schartner. Cybersecurity ai: Evaluating agentic cybersecurity in attack/defense ctfs. _arXiv preprint arXiv:2510.17521_ , 2025. 

- [16] Benlong Wu, Guoqiang Chen, Kejiang Chen, Xiuwei Shang, Jiapeng Han, Yanru He, Weiming Zhang, and Nenghai Yu. Autopt: How far are we from the end2end automated web penetration testing? _arXiv preprint arXiv:2411.01236_ , 2024. 

- [17] He Kong, Die Hu, Jingguo Ge, Liangxiong Li, Tong Li, and Bingzhen Wu. Vulnbot: Autonomous penetration testing for a multi-agent collaborative framework. _arXiv preprint arXiv:2501.13411_ , 2025. 

- [18] Paul Ammann, Duminda Wijesekera, and Saket Kaushik. Scalable, graph-based network vulnerability analysis. _Proceedings of the 9th ACM Conference on Computer and Communications Security_ , pages 217–224, 2002. 

- [19] Xinming Ou, Wayne F Boyer, and Miles A McQueen. Mulval: A logic-based network security analyzer. _USENIX security symposium_ , 8:113–128, 2005. 

- [20] Kerem Kaynar. A taxonomy for attack graph generation and usage in network security. _Journal of Information Security and Applications_ , 29:27–56, 2016. 

- [21] Harjinder Singh Lallie, Kurt Debattista, and Jay Bal. A review of attack graph and attack tree visual syntax in cyber security. _Computer Science Review_ , 35:100219, 2020. 

- [22] Yang Liu, Wei Zhang, and Xiao Chen. Recent developments in game-theory approaches for the detection and defense against advanced persistent threats (apts): A systematic review. _Mathematics_ , 11:1353, 2023. 

- [23] Víctor Mayoral-Vilches, Luis Javier Navarrete-Lozano, María Sanz-Gómez, Lidia Salas Espejo, Martiño Crespo-Álvarez, Francisco Oca-Gonzalez, Francesco Balassone, Alfonso Glera-Picón, Unai Ayucar-Carbajo, Jon Ander Ruiz-Alcalde, Stefan Rass, Martin Pinzger, and Endika Gil-Uriarte. Cai: An open, bug bounty-ready cybersecurity ai, 2025. URL `https://arxiv.org/abs/2504.06017` . 

- [24] Artem Petrov and Dmitrii Volkov. Evaluating ai cyber capabilities with crowdsourced elicitation, 2025. URL `https://arxiv.org/abs/2505.19915` . 

_REFERENCES_ 

- [25] Aric Hagberg, Pieter J Swart, and Daniel A Schult. Exploring network structure, dynamics, and function using networkx. Technical report, Los Alamos National Laboratory (LANL), Los Alamos, NM (United States), 2008. 

- [26] S. Haque, M. Keffeler, and T. Atkison. An evolutionary approach of attack graphs and attack trees: A survey of attack modeling. In _Proceedings of the International Conference on Security and Management (SAM)_ , pages 224–229, Las Vegas, NV, USA, 2017. The Steering Committee of The World Congress in Computer Science, Computer Engineering and Applied Computing (WorldComp). URL `https://dcsl.cs.ua.edu/papers/SAM9712.pdf` . 

- [27] María Sanz-Gómez, Víctor Mayoral-Vilches, Francesco Balassone, Luis Javier Navarrete-Lozano, Cristóbal R. J. Veas Chavez, and Maite del Mundo de Torres. Cybersecurity ai benchmark (caibench): A meta-benchmark for evaluating cybersecurity ai agents, 2025. URL `https://arxiv. org/abs/2510.24317` . 

_Appendix 1: A Refresher on Cut-The-Rope (CTR) and Game Theory [6]_ 

# **APPENDICES** 

### **A Appendix 1: A Refresher on Cut-The-Rope (CTR) and Game Theory [6]** 

The Cut-the-Rope (CTR) model introduces a formal game-theoretic framework for modeling stealthy cyberattacks in probabilistic attack graphs under asynchronous timing. It assumes the attacker is already present in the system and advances continuously in time along a directed path toward a critical target node _v_ 0, following a stochastic process, typically a Poisson process, with rate _λ_ that determines the average number of steps the attacker takes between defender actions. In contrast, the defender operates in discrete time, inspecting one node per round from an admissible set _AS_ 1 _⊆ V \ {v_ 0 _}_ . If the defender inspects a node that lies on the attacker’s current path before the attacker reaches _v_ 0, the path is “cut” and the attacker is forced to restart. This asynchronous, probabilistic setup models the temporal and informational asymmetry inherent in advanced persistent threat (APT) scenarios, capturing both the stealth and adaptiveness of real-world attackers. 

CTR models the system as a directed acyclic attack graph _G_ = ( _V, E_ ), where: 

- _V_ is the set of nodes representing system components or privileges; 

- _E ⊆ V × V_ is the set of directed edges representing potential exploits. 

The attacker’s goal is to reach a designated critical asset _v_ 0 _∈ V_ , while the defender performs _spot checks_ to prevent this. The attacker is assumed to already be in the system, at an unknown node _θ ∈ V \ {v_ 0 _}_ , and proceeds along an attack path _π_ , which is a directed path from _θ_ to _v_ 0. 

The defender can inspect nodes from a set _AS_ 1 _⊆ V \{v_ 0 _}_ . The attacker selects a strategy over pairs ( _θ, π_ ), where _θ ∈ V_ ( _π_ ) _⊆ V \ {v_ 0 _}_ is the starting point, and _π ∈ AS_ 2 is a feasible attack path ending at _v_ 0. The game is defined by the quintuple: 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0030-09.png)


where _fN_ is a probability distribution over the number of steps the attacker can take during a single round (e.g., following a Poisson-, geometric or other distribution). 

##### **Defender’s expected success** 

The probability that the attacker has reached a particular node _v_ on path _π_ , given the rate _λ_ , is: 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0030-13.png)


_Appendix 1: A Refresher on Cut-The-Rope (CTR) and Game Theory [6]_ 

This expression simply says: "Among all possible positions the attacker could reach on path _π_ , how likely is it that they reached node _v_ ?" 

Here: 

- _θ ∈ V \ {v_ 0 _}_ : the attacker’s starting node, 

- _π_ : the attack path from _θ_ to the target _v_ 0, 

- _dπ_ ( _θ, v_ ): the number of steps from _θ_ to node _v_ along _π_ , 

- _V_ ( _π_ ) _⊆ V_ : the set of nodes on path _π_ , 

- _λ_ : the attack rate (average steps per round), 

- _f_ Pois( _k_ ; _λ_ ): the Poisson mass function: 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0031-09.png)


This function gives the probability of making exactly _k_ steps between two defender actions. 

##### **Defender’s utility** 

Let _σd ∈_ ∆( _AS_ 1) be the defender’s mixed strategy: a probability distribution over the set _AS_ 1 _⊆ V \ {v_ 0 _}_ of nodes that the defender is allowed to inspect. Each round, the defender picks a node _c ∈ AS_ 1 to inspect, with probability _σd_ ( _c_ ). The defender’s expected probability of catching the attacker (e.g., cutting the attack path) is: 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0031-13.png)


Here: 

- _c ∈ AS_ 1: a candidate node for inspection (excluding the target _v_ 0), 

- _σd_ ( _c_ ): the probability the defender chooses to inspect node _c_ , 

- _Pπ_ ( _c | θ, λ_ ): the likelihood the attacker is at node _c_ , given path _π_ and attack rate _λ_ . 

##### **Attacker’s success probability** 

The attacker succeeds if none of the nodes they use are inspected during the round. This gives the attacker’s success utility: 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0031-20.png)


##### **Game **objective:** optimal defender strategy** 

This is a zero-sum game: the attacker’s gain is the defender’s loss. The defender seeks the strategy _σd_<sup>_⋆_thatminimizestheattacker’sbest-casechanceofsuccessacrossallpossibleattackpathsand</sup> starting points. Formally, the optimal defense is: 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0031-23.png)


Where: 

_Appendix 2: Attack Graph Gold Standard Dataset_ 

- _AS_ 2: the set of all possible attack paths ending at _v_ 0, 

- _V_ ( _π_ ): the set of nodes on path _π_ , 

- _θ ∈ V_ ( _π_ ): the possible (unknown) starting location of the attacker. 

This defines a _minimax_ game: the defender prepares for the worst-case attack, and ensures that even under maximum uncertainty, the probability of a successful breach is as low as possible. The resulting _σd_<sup>_⋆_istheoptimalrandomizeddefensepolicy.</sup> 

##### **Game solution: Nash equilibrium** 

The interaction between the attacker and defender is modeled as a zero-sum game, in which the attacker selects a hidden entry point _θ ∈ V \ {v_ 0 _}_ and a path _π ∈ AS_ 2, while the defender chooses a randomized inspection strategy _σd ∈_ ∆( _AS_ 1). The defender aims to minimize the probability of a successful undetected attack, while the attacker aims to maximize it. 

A central solution concept in this game is the _Nash equilibrium_ , which is a pair of strategies such that neither player can improve their expected utility by unilaterally deviating. In this zero-sum setting, the defender’s optimal strategy _σd_<sup>_⋆_correspondstotheminimaxsolution,andtheattacker’sbest</sup> response is to select the pair ( _π_<sup>_⋆_</sup> _, θ_<sup>_⋆_</sup> ) that maximizes their success probability under _σd_<sup>_⋆_.</sup> Formally, the equilibrium condition is defined as: 

_UD_ ( _σd_<sup>_⋆, π, θ_)</sup><sup>_≥UD_(</sup><sup>_σd, π, θ_)</sup> _∀σd,_ and _UA_ ( _σd_<sup>_⋆, π⋆, θ⋆_)</sup><sup>_≥UA_(</sup><sup>_σ_</sup> _d_<sup>_⋆, π, θ_)</sup> _∀_ ( _π, θ_ ) (13) 

Here: 

- _UD_ ( _σd, π, θ_ ): the defender’s expected probability of detection, 

- _UA_ = 1 _− UD_ : the attacker’s probability of success, 

- _σd_<sup>_⋆_:thedefender’soptimalmixedstrategy,</sup> 

- ( _π_<sup>_⋆_</sup> _, θ_<sup>_⋆_</sup> ): the attacker’s best-response path and entry point under _σd_<sup>_⋆_.</sup> 

This equilibrium represents a stable solution in which the defender has maximally reduced the attacker’s chance of success, even under worst-case uncertainty. No player can unilaterally improve their utility, i.e., the strategy pair is mutually optimal. 

### **B Appendix 2: Attack Graph Gold Standard Dataset** 

In order to evaluate the performance of large language models (LLMs) in comparison to human analysts, a manually annotated dataset of attack graphs was constructed using real-world vulnerability reports. This dataset serves as a gold standard for assessing the quality of generated graphs, enabling direct comparison between machine-generated and human-constructed outputs. Two annotators were involved in the process, and annotation of each log typically required between 30 to 60 minutes depending on its complexity. 

Five logs were selected from cybersecurity exercises derived from bug bounty evaluations as described in [23]. These exercises originated from HackerOne, a platform where real vulnerabilities have been discovered and validated. These logs were chosen specifically because they are known to contain confirmed vulnerabilities, providing a reliable basis for evaluating attack graph reconstructions. 

For consistency, the same list of messages used as input for the LLMs was extracted from each report. This ensured alignment between the human and model interpretations of the data. 

Each log was replayed with corresponding tool and analyzed manually. Messages were reviewed one by one, and annotations were recorded using a structured format that captures each attack step, 

_Appendix 2: Attack Graph Gold Standard Dataset_ 

its preconditions, and its effects. This format is designed to support subsequent evaluation tasks. An example of the annotation schema is: 

```
{
"nodes":[
{
"id":"A",
"name":"StartNode",
"info":"Initialpointoftheattack",
"vulnerability":false,
"message_id":101
},
{
"id":"B",
"name":"ExploitAttempt",
"info":"Attempttoexploitaweakness",
"vulnerability":true,
"message_id":102
}
],
"edges":[
{
"source":"A",
"target":"B"
}
]
}
```

A key contribution of this work is the introduction of a standardized annotation format for manually constructed attack graphs derived from natural language reports. Although existing formats support general graph structures, few are tailored to the specific semantics of attack chains. The proposed format aims to promote reproducibility, support benchmarking efforts, and encourage future work in evaluating LLMs for cybersecurity applications. 

|**Domain**|**Messages**|**Tokens**|**Vulnerabilities**|
|---|---|---|---|
|**kolesa.kz**|72|44,959|Hardcoded API key|
|**mercadolibre.com**|47|424,838|User enumeration|
|**pornbox.com**|80|100,139|No rate limit|
|**hm.com**|118|40,616|SSL certifcate mismatch|
|**media.guilded.gg**|358|8,959,492|URL Confusion Attack, SSL cert mismatch|



**Table 8:** Summary of the exercises included in the Attack Graph Gold Standard Dataset across five domains. For each domain, the table aggregates the total number of messages exchanged, total tokens processed (Input + Output tokens), and the vulnerabilities identified during execution. The model for the vulnerability search was `claude-3-7-sonnet-20250219` . 

_Appendix 3: kolesa.kz_ 

### **C Appendix 3: kolesa.kz** 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0034-02.png)


- (a) Human Attack Graph 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0034-04.png)


<!-- Start of picture text -->
Node ID Probability Path ID Path Sequence Probability<br>6 1.000000 1 1  → 6  → 7 1.000000<br><!-- End of picture text -->

- (b) Optimal Defense Strategy 

- (c) Attacker Strategy 

##### **Game Equilibrium** 

Defender can keep attacker success below: **0.000000** Attacker can guarantee success probability of: **0.000000** 

- (d) Game Equilibrium 

**Figure 7: Ground-Truth attack graph annotated by Humans in the kolesa.kz domain** : This manually constructed graph illustrates the real-world steps taken in a bug bounty exercies of the kolesa.kz domain, starting with the subdomain krisha.kz. The process followed a natural reconnaissance path, including inspection of server IPs, analysis of security headers and robots.txt, and exploration of API endpoints. Attention then shifted to client-side JavaScript, where there was identified a hardcoded Yandex Maps API key (8005a76b-66c7-44b3-8f94-355bbff74d27) embedded in the window.data object. The exposed key represents a potential vulnerability due to improper handling of sensitive credentials. The flow concludes with the creation of a final report. All connections and insights were derived and annotated manually by the researcher, without automated tooling. 

_Appendix 3: kolesa.kz_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0035-01.png)


- (a) Attack Graph Example 

|**Node ID**<br>**Probability**|**Path ID**<br>**Path Sequence**|**Probability**|
|---|---|---|
|2<br>1.000000|1<br>1_→_2_→_3|1.000000|
|al Defense Strategy|(c) Attacker Strategy||



- (b) Optimal Defense Strategy 

**Game Equilibrium** Defender can keep attacker success below: **0.000000** Attacker can guarantee success probability of: **0.000000** 

- (d) Game Equilibrium 

**Figure 8:** Attack Graph and Equilibrium analysis for `gpt-4o` 

_Appendix 3: kolesa.kz_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0036-01.png)


- (a) Attack Graph Example 

|**Node ID**|**Probability**|||
|---|---|---|---|
|5|1.000000|**Path ID**<br>**Path Sequence**|**Probability**|
|3|0.000000|1<br>1_→_3_→_4_→_5_→_6|1.000000|
|4|0.000000|||



   - (c) Attacker Strategy 

- (b) Optimal Defense Strategy 

**Game Equilibrium** Defender can keep attacker success below: **0.000000** Attacker can guarantee success probability of: **0.000000** 

###### (d) Game Equilibrium 

**Figure 9:** Attack Graph and Equilibrium analysis for `o3` 

_Appendix 3: kolesa.kz_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0037-01.png)


###### (a) Attack Graph Example 

|**Node ID**|**Probability**||
|---|---|---|
|5<br>|1.000000<br>|**Path ID**<br>**Path Sequence**<br>**Probability**|
|2<br>3|0.000000<br>0.000000|1<br>1_→_2_→_3_→_4_→_5_→_6<br>1.000000|
|4|0.000000|(c) Attacker Strategy|



###### (b) Optimal Defense Strategy 

**Game Equilibrium** Defender can keep attacker success below: **0.000000** Attacker can guarantee success probability of: **0.000000** 

(d) Game Equilibrium 

**Figure 10:** Attack Graph and Equilibrium analysis for `grok-4` 

_Appendix 3: kolesa.kz_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0038-01.png)


(a) Attack Graph Example 

|**Node ID**|**Probability**||
|---|---|---|
|5|1.000000|**Path ID**<br>**Path Sequence**<br>**Probability**|
|2|0000000||
||.|1<br>1_→_2_→_3_→_4_→_5_→_6<br>1.000000|
|3|0.000000||
|4|0.000000|(c) Attacker Strategy|



- (b) Optimal Defense Strategy 

##### **Game Equilibrium** 

Defender can keep attacker success below: **0.000000** Attacker can guarantee success probability of: **0.000000** 

(d) Game Equilibrium 

**Figure 11:** Attack Graph and Equilibrium analysis for `claude-sonnet-4` 

_Appendix 3: kolesa.kz_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0039-01.png)


###### (a) Attack Graph Example 

|**Node ID**|**Probability**|||
|---|---|---|---|
|5|1.000000|**Path ID**<br>**Path Sequence**|**Probability**|
|2|0.000000|1<br>1_→_2_→_3_→_5_→_6|1.000000|
|3|0.000000|||



   - (c) Attacker Strategy 

- (b) Optimal Defense Strategy 

|**Game Equilibrium**|
|---|
|Defender can keep attacker success below: **0.000000**|
|Attacker can guarantee success probability of: **0.000000**|



###### (d) Game Equilibrium 

**Figure 12:** Attack Graph and Equilibrium analysis for `alias0` 

_Appendix 3: mercadolibre.com_ 

### **D Appendix 3: mercadolibre.com** 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0040-02.png)


###### (a) Human Attack Graph Example 

|**Node ID**|**Probability**|**Path ID**<br>**Path Sequence**|**Probability**|
|---|---|---|---|
|4|1.000000|1<br>1_→_3_→_4_→_6|1.000000|
|3|0.000000|2<br>1_→_3_→_4_→_6_→_7|0.000000|



- (b) Optimal Defense Strategy 

(c) Attacker Strategy 

##### **Game Equilibrium** 

Defender can keep attacker success below: **0.000000** Attacker can guarantee success probability of: **0.000000** 

###### (d) Game Equilibrium 

**Figure 13:** Ground-Truth Exercise annotated by **Humans** . The identified vulnerability is an Insecure Direct Object Reference (IDOR), which allows attackers to enumerate users by manipulating API requests. The attack path starts with reconnaissance of the target domain (mercadolibre.com) followed by open-source intelligence using Shodan. Analysts then identify an exposed API endpoint, which leads to crafting a Python script to exploit the IDOR vulnerability. This script is used to validate the vulnerability and confirm unauthorized access to user data. The attack culminates in a proof of concept (POC) demonstrating successful exploitation. One branch of the attack also leads to failed attempts, indicating exploration of alternative vectors. The Attack Graph highlights the critical path and decision points taken during real-world vulnerability discovery. 

_Appendix 3: mercadolibre.com_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0041-01.png)


###### (a) Attack Graph Example 

|**Node ID**|**Probability**|||
|---|---|---|---|
|5|1.000000|**Path ID**<br>**Path Sequence**|**Probability**|
|2|0.000000|1<br>1_→_2_→_4_→_5_→_6|1.000000|
|4|0.000000|||



(c) Attacker Strategy 

- (b) Optimal Defense Strategy 

**Game Equilibrium** Defender can keep attacker success below: **0.000000** Attacker can guarantee success probability of: **0.000000** 

###### (d) Game Equilibrium 

**Figure 14:** Attack Graph and Equilibrium analysis for `gpt-4o` 

_Appendix 3: mercadolibre.com_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0042-01.png)


- (a) Attack Graph Example 

|||**Path ID**|**Path Sequence**|**Probability**|
|---|---|---|---|---|
|**Node ID**|**Probability**||||
|||1|1_→_4_→_6|1.000000|
|4|1.000000|2|1_→_6|0.000000|



- (b) Optimal Defense Strategy 

- (c) Attacker Strategy 

**Game Equilibrium** Defender can keep attacker success below: **0.000000** Attacker can guarantee success probability of: **0.000000** 

- (d) Game Equilibrium 

**Figure 15:** Attack Graph and Equilibrium analysis for `o3` 

_Appendix 3: mercadolibre.com_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0043-01.png)


(a) Attack Graph Example 

|**Node ID**|**Probability**||
|---|---|---|
|6|1.000000||
|2|0.000000|**Path ID**<br>**Path Sequence**<br>**Probability**|
|3|0.000000|1<br>1_→_2_→_3_→_4_→_5_→_6_→_7<br>1.000000|
|4<br>5|0.000000<br>0.000000|(c) Attacker Strategy|



(b) Optimal Defense Strategy 

##### **Game Equilibrium** 

Defender can keep attacker success below: **0.000000** Attacker can guarantee success probability of: **0.000000** 

(d) Game Equilibrium 

**Figure 16:** Attack Graph and Equilibrium analysis for `grok-4` 

_Appendix 3: mercadolibre.com_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0044-01.png)


###### (a) Attack Graph Example 

|**Node ID**|**Probability**||
|---|---|---|
|5|1000000||
||.|**Path ID**<br>**Path Sequence**<br>**Probability**|
|2|0000000||
|3|.<br>0.000000|1<br>1_→_2_→_3_→_4_→_5_→_6<br>1.000000|
|4|0.000000|(c) Attacker Strategy|



- (b) Optimal Defense Strategy 

##### **Game Equilibrium** 

Defender can keep attacker success below: **0.000000** Attacker can guarantee success probability of: **0.000000** 

(d) Game Equilibrium 

**Figure 17:** Attack Graph and Equilibrium analysis for `claude-sonnet-4` 

_Appendix 3: mercadolibre.com_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0045-01.png)


###### (a) Attack Graph Example 

|**Node ID**|**Probability**|||
|---|---|---|---|
|5|1.000000|**Path ID**<br>**Path Sequence**|**Probability**|
|2|0.000000|1<br>1_→_2_→_4_→_5_→_6|1.000000|
|3|0.000000|2<br>1_→_3_→_5_→_6|0.000000|
|4|0.000000|||



(c) Attacker Strategy 

- (b) Optimal Defense Strategy 

##### **Game Equilibrium** 

|Defender can keep attacker success below: **0.000000**|
|---|
|Attacker can guarantee success probability of: **0.000000**|



(d) Game Equilibrium 

**Figure 18:** Attack Graph and Equilibrium analysis for `alias0` 

_Appendix 3: pornbox.com_ 

### **E Appendix 3:** **<u>pornbox.com</u>** 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0046-02.png)


(a) Human Attack Graph 

|||**Path ID**|**Path Sequence**|**Probability**|
|---|---|---|---|---|
|**Node ID**|**Probability**|4|1_→_5_→_6_→_7_→_8|1.000000|
|7|1.000000|1|1_→_4|0.000000|
|5|0.000000|2|1_→_5_→_6|0.000000|
|||3|1_→_4_→_8|0.000000|



(b) Optimal Defense Strategy 

(c) Attacker Strategy 

##### **Game Equilibrium** 

Defender can keep attacker success below: **0.000000** Attacker can guarantee success probability of: **0.000000** 

- (d) Game Equilibrium 

**Figure 19:** Ground-Truth Exercise annotated by **Humans** . Attack graph generated by human analysts for the Pornbox exercise. The identified vulnerability involves insufficient rate–limiting protections, which could enable brute– force or automated attacks. The attack path begins with an initial reconnaissance of the domain `dev.pornbox.com` , which redirects to a staging subdomain `beta3.pornbox.com` . Analysts proceed to examine administrative interfaces (ID 3) and discover a permissive Content Security Policy with insecure directives. Further inspection of HTTP headers reveals rate–limiting headers indicative of exploitable weaknesses. This leads to the identification of an exploitable scenario through crafted requests, culminating in the generation of a security report. The graph illustrates the suc- ~~cessful attack chain as well as alternate vectors that were explored but did not lead to~~ compromise. 

_Appendix 3: pornbox.com_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0047-01.png)


###### (a) Attack Graph Example 

|**Node ID**|**Probability**|**Path ID**|**Path Sequence**|**Probability**|
|---|---|---|---|---|
|4|0.519132|10|0_→_8_→_5|0.406929|
|2|0.240434|5|0_→_1_→_2_→_5|0.352637|
|8|0.240434|1|0_→_1_→_2_→_3_→_4_→_5|0.240434|
|3|0.000000|2–14|All other paths|0.000000|



(b) Optimal Defense Strategy 

(c) Attacker Strategy 

##### **Game Equilibrium** 

Defender can keep attacker success below: **0.027127** Attacker can guarantee success probability of: **0.027127** 

(d) Game Equilibrium 

**Figure 20:** Attack Graph and Equilibrium analysis for `gpt-4o` 

_Appendix 3: pornbox.com_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0048-01.png)


(a) Attack Graph Example 

|||**Path ID**|**Path Sequence**|**Probability**|
|---|---|---|---|---|
|||3|1_→_3_→_2_→_4_→_5_→_6|0.500000|
|**Node ID**|**Probability**|4|1_→_3_→_2_→_4_→_7_→_8|0.500000|
|7|0.500000|1|1_→_2_→_4_→_5_→_6|0.000000|
|5|0.500000|2|1_→_2_→_4_→_7_→_8|0.000000|
|2|0.000000|5|1_→_4_→_5_→_6|0.000000|
|3|0.000000|6|1_→_4_→_7_→_8|0.000000|
|4|0.000000|7|1_→_5_→_6|0.000000|
|DefenseStra|tegy|8|1_→_7_→_8|0.000000|
|||9|1_→_8|0.000000|



(b) Optimal Defense Strategy 

(c) Attacker Strategy 

##### **Game Equilibrium** 

Defender can keep attacker success below: **0.025766** Attacker can guarantee success probability of: **0.025766** 

(d) Game Equilibrium 

**Figure 21:** Attack Graph and Equilibrium analysis for `o3` 

_Appendix 3: pornbox.com_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0049-01.png)


(a) Attack Graph Example 

|||**Path ID**|**Path Sequence**|**Probability**|
|---|---|---|---|---|
|**Node ID**|**Probability**|1|1_→_2_→_3_→_4|1.000000|
|3|1.000000|2|1_→_2_→_3_→_5|0.000000|
|2|0.000000|3|1_→_2_→_3_→_6|0.000000|
|||4|1_→_2_→_3_→_7|0.000000|



(b) Optimal Defense Strategy 

(c) Attacker Strategy 

##### **Game Equilibrium** 

Defender can keep attacker success below: **0.000000** Attacker can guarantee success probability of: **0.000000** 

(d) Game Equilibrium 

**Figure 22:** Attack Graph and Equilibrium analysis for `grok-4` 

_Appendix 3: pornbox.com_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0050-01.png)


(a) Attack Graph Example 

|||**Path ID**|**Path Sequence**|**Probability**|
|---|---|---|---|---|
|**Node ID**|**Probability**|2|1_→_2_→_3_→_4_→_5|0.500000|
|2|0.500000|1|1_→_2_→_3|0.500000|
|4|0.500000|3|1_→_2_→_3_→_4_→_6|0.000000|
|||4|1_→_2_→_3_→_4_→_7|0.000000|



(b) Optimal Defense Strategy 

(c) Attacker Strategy 

##### **Game Equilibrium** 

Defender can keep attacker success below: **0.035714** Attacker can guarantee success probability of: **0.035714** 

(d) Game Equilibrium 

**Figure 23:** Attack Graph and Equilibrium analysis for `claude-sonnet-4` 

_Appendix 3: pornbox.com_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0051-01.png)


###### (a) Attack Graph Example 

|**Node ID**|**Probability**|**Path ID**|**Path Sequence**|**Probability**|
|---|---|---|---|---|
|4|1.000000|1|1_→_2_→_3_→_4_→_5|1.000000|
|2|0.000000|2|1_→_2_→_3_→_4_→_6|0.000000|
|3|0.000000|3|1_→_2_→_3_→_4_→_7|0.000000|



- (b) Optimal Defense Strategy 

(c) Attacker Strategy 

##### **Game Equilibrium** 

Defender can keep attacker success below: **0.000000** Attacker can guarantee success probability of: **0.000000** 

- (d) Game Equilibrium 

**Figure 24:** Attack Graph and Equilibrium analysis for `alias0` 

_Appendix 4: hm.com_ 

### **F Appendix 4: hm.com** 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0052-02.png)


###### (a) Human Attack Graph 

|**Node ID**|**Probability**|**Path ID**|**Path Sequence**|**Probability**|
|---|---|---|---|---|
|6|1.000000|1|1_→_3_→_6_→_7|1.000000|
|3|0.000000|2|1_→_3_→_6_→_7_→_9|0.000000|



- (b) Optimal Defense Strategy 

(c) Attacker Strategy 

##### **Game Equilibrium** 

Defender can keep attacker success below: **0.000000** Attacker can guarantee success probability of: **0.000000** 

- (d) Game Equilibrium 

**Figure 25: Ground-Truth attack graph annotated by Humans in the hm.com doamin** : This manually created graph outlines the step-by-step process followed by a human during a real-world bug bounty assessment of the hm.com domain and its subdomains. The engagement began with subdomain enumeration and IP resolution, followed by inspection of HTTP headers and SSL configurations across endpoints such as mobile.hm.com, shop.hm.com, and api.hm.com. While the latter was protected by Akamai CDN, the researcher discovered an SSL certificate mismatch vulnerability on shop.hm.com, posing a potential risk to user trust and secure communication. This finding was validated and supported with a custom proof-of-concept (PoC) script. The flow concludes with a final report summarizing the issue and providing remediation guidance. 

_Appendix 4: hm.com_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0053-01.png)


- (a) Attack Graph Example 

|**Node ID**|**Probability**|**Path ID**|**Path Sequence**|**Probability**|
|---|---|---|---|---|
|16|1.000000|1|0_→_16_→_20|1.000000|



- (b) Optimal Defense Strategy 

- (c) Attacker Strategy 

##### **Game Equilibrium** 

Defender can keep attacker success below: **0.000000** Attacker can guarantee success probability of: **0.000000** 

- (d) Game Equilibrium 

**Figure 26:** Attack Graph and Equilibrium analysis for `gpt-4o` . 

_Appendix 4: hm.com_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0054-01.png)


###### (a) Attack Graph Example 

|**Node ID**|**Probability**|**Node ID**<br>**Probability**|
|---|---|---|
|6|0.511996|5<br>1_→_9_→_8<br>0.531336|
|7|0.313940|1<br>1_→_3_→_4_→_6_→_7_→_8<br>0.294600|
|9|0.174064|2<br>1_→_3_→_4_→_6_→_8<br>0.174064|
|3|0.000000|3<br>1_→_6_→_7_→_8<br>0.000000|
|4|0.000000|4<br>1_→_6_→_8<br>0.000000|



(b) Optimal Defense Strategy 

(c) Attacker Strategy 

##### **Game Equilibrium** 

Defender can keep attacker success below: **0.023598** Attacker can guarantee success probability of: **0.023598** 

(d) Game Equilibrium 

**Figure 27:** Attack Graph and Equilibrium analysis for `o3` . 

_Appendix 4: hm.com_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0055-01.png)


(a) Attack Graph Example 

|**Node ID**|**Probability**|
|---|---|
|12|1.000000|
|10|0.000000|
|11|0.000000|
|6|0.000000|
|7|0.000000|



(b) Optimal Defense Strategy 

|**Path ID**|**Path Sequence**|**Probability**|
|---|---|---|
|1<br>1_→_6_→_|7_→_10_→_11_→_12_→_13|1.000000|



(c) Attacker Strategy 

##### **Game Equilibrium** 

Defender can keep attacker success below: **0.000000** Attacker can guarantee success probability of: **0.000000** 

(d) Game Equilibrium 

**Figure 28:** Attack Graph and Equilibrium analysis for `grok-4` . 

_Appendix 4: hm.com_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0056-01.png)


- (a) Attack Graph Example 

|**Node ID**<br>**Probability**|**Path ID**<br>**Path **|**Sequence**|**Probability**|
|---|---|---|---|
|7<br>1.000000|1<br>1|_→_7_→_8|1.000000|
|Defense Strategy|(c) Attacker Strategy|||



- (b) Optimal Defense Strategy 

**Game Equilibrium** Defender can keep attacker success below: **0.000000** Attacker can guarantee success probability of: **0.000000** 

- (d) Game Equilibrium 

**Figure 29:** Attack Graph and Equilibrium analysis for `claude-sonnet-4` . 

_Appendix 4: hm.com_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0057-01.png)


- (a) Attack Graph Example 

|**Node ID**|**Probability**|||
|---|---|---|---|
|8|1.000000|**Path ID**<br>**Path Sequence**|**Probability**|
|2|0.000000|1<br>1_→_2_→_3_→_8_→_11|1.000000|
|3|0.000000|||



(c) Attacker Strategy 

- (b) Optimal Defense Strategy 

|**Game Equilibrium**|
|---|
|Defender can keep attacker success below: **0.000000**|
|Attacker can guarantee success probability of: **0.000000**|



###### (d) Game Equilibrium 

**Figure 30:** Attack Graph and Equilibrium analysis for `alias0` . 

_Appendix 5: media.guilded.gg_ 

### **G Appendix 5: media.guilded.gg** 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0058-02.png)


###### (a) Human Attack Graph 

|**Node ID**|**Probability**|**Path ID**|**Path Sequence**|**Probability**|
|---|---|---|---|---|
|5|1.000000|1|1_→_4_→_5_→_11|1.000000|
|4|0.000000|2|1_→_4_→_5_→_11_→_14|0.000000|



- (b) Optimal Defense Strategy 

- (c) Attacker Strategy 

##### **Game Equilibrium** 

Defender can keep attacker success below: **0.000000** Attacker can guarantee success probability of: **0.000000** 

- (d) Game Equilibrium 

**Figure 31: Ground-Truth attack graph annotated by Humans in the media.guilded.gg domain** : This graph documents the real-world, manually performed security research process focused on the `/media/upload` webhook endpoint of `media.guilded.gg` . Starting with reconnaissance and authentication setup, the researcher tested a range of payloads, including malicious file uploads, XSS vectors, command and embed injections, and SSRF via the `avatar`<sup>`_`</sup> `url` parameter. While many inputs were properly sanitized, the investigation uncovered a **URL format bypass** vulnerability where JavaScript-based URLs were allowed through encoding and Unicode tricks. This weakness enabled a URL confusion attack, crafting links like `https://facebook.com@github.com/...` that could mislead users and trigger unintended file downloads. The results led to the creation of a detailed security report and further experiments, including rate-limit testing via webhook spam. 

_Appendix 5: media.guilded.gg_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0059-01.png)


(a) Attack Graph Example 

|**Node ID**|**Probability**||||
|---|---|---|---|---|
|8|0.423077|**Path ID**|**Path Sequence**|**Probability**|
|10|0.423077|3|1_→_12_→_13|0.423077|
|12|0.153846|1<br>2|1_→_5_→_8_→_14<br>1_→_5_→_10_→_13|0.288461<br>0.288461|
|5|0.000000||||



(c) Attacker Strategy 

- (b) Optimal Defense Strategy 

##### **Game Equilibrium** 

Defender can keep attacker success below: **0.030220** Attacker can guarantee success probability of: **0.030220** 

(d) Game Equilibrium 

**Figure 32:** Attack Graph and Equilibrium analysis for `gpt-4o` 

_Appendix 5: media.guilded.gg_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0060-01.png)


(a) Attack Graph Example 

|**Node ID**|**Probability**|||
|---|---|---|---|
|9|0.551513|||
|3|0.448487|**Path ID**<br>**Path Sequence**|**Probability**|
|2|0.000000|1<br>1_→_2_→_3_→_4|0.551513|
|5|0.000000|2<br>1_→_5_→_6_→_8_→_9_→_10|0.448487|
|6<br>8|0.000000<br>0.000000|(c) Attacker Strategy||



(b) Optimal Defense Strategy 

##### **Game Equilibrium** 

Defender can keep attacker success below: **0.019259** Attacker can guarantee success probability of: **0.019259** 

(d) Game Equilibrium 

**Figure 33:** Attack Graph and Equilibrium analysis for `o3` 

_Appendix 5: media.guilded.gg_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0061-01.png)


- (a) Attack Graph Example 

|**Node ID**<br>**Probability**|
|---|
|11<br>1.000000|
|2-10<br>0.000000|



###### (b) Optimal Defense Strategy 

|**Path ID**|**Path Sequence**||**Probability**|
|---|---|---|---|
|1|1_→_2_→_3_→_4_→_|5_→_6_→_7_→_8_→_9_→_10_→_11_→_12|1.000000|
|2|1_→_2_→_3_→_4_→_|5_→_6_→_7_→_8_→_9_→_10_→_11_→_12|0.000000|
||_→_13|||



- (c) Attacker Strategy 

|**Game Equilibrium**|
|---|
|Defender can keep attacker success below: **0.000000**|
|Attacker can guarantee success probability of: **0.000000**|



- (d) Game Equilibrium 

**Figure 34:** Attack Graph and Equilibrium analysis for `grok-4` 

_Appendix 5: media.guilded.gg_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0062-01.png)


(a) Attack Graph Example 

||**Node ID**|**Probability**|
|---|---|---|
||9|1.000000|
||5-8|0.000000|
|(b) Optimal Defense Strategy|||



|**Node ID**|**Probability**||
|---|---|---|
|1|1_→_5_→_6_→_7_→_8_→_9_→_10_→_11_→_12_→_13|1.000000|
|2|1_→_5_→_6_→_7_→_8_→_9_→_10_→_11_→_12|0.000000|
|3|1_→_5_→_6_→_7_→_8_→_9_→_10_→_11|0.000000|
|4|1_→_5_→_6_→_7_→_8_→_9_→_10|0.000000|



(c) Attacker Strategy 

|**Game Equilibrium**|
|---|
|Defender can keep attacker success below: **0.000000**|
|Attacker can guarantee success probability of: **0.000000**|



(d) Game Equilibrium 

**Figure 35:** Attack Graph and Equilibrium analysis for `claude-sonnet-4` 

_Appendix 5: media.guilded.gg_ 


![](images/41-cybersecurity-ai-a-game-theoretic-ai-for-guiding-attack-and.pdf-0063-01.png)


(a) Attack Graph Example 

|**Node ID**|**Probability**|
|---|---|
|8|1.000000|
|2|0.000000|
|3|0.000000|



###### (b) Optimal Defense Strategy 

|**Path ID**<br>**Path **|**Sequence**<br>**Probability**|
|---|---|
|1<br>1_→_2|_→_3_→_8_→_11<br>1.000000|



(c) Attacker Strategy 

##### **Game Equilibrium** 

Defender can keep attacker success below: **0.000000** Attacker can guarantee success probability of: **0.000000** 

(d) Game Equilibrium 

**Figure 36:** Attack Graph and Equilibrium analysis for `alias0` 

