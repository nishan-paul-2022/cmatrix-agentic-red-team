IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 


# A Unified Modeling Framework for Automated Penetration Testing 

## Table of Contents

- [I. INTRODUCTION](#i-introduction)
- [II. THEORETICAL FOUNDATIONS OF AUTOPT SIMULATION MODELING](#ii-theoretical-foundations-of-autopt-simulation-modeling)
- [A. Control Theory Perspective](#a-control-theory-perspective)
- [B. AutoPT as a Dynamic Nonlinear System](#b-autopt-as-a-dynamic-nonlinear-system)
- [C. Core Modeling Elements](#c-core-modeling-elements)
- [III. THE MULTI-DIMENSIONAL CLASSIFICATION SYSTEM FOR PENETRATION TESTING MODELING: MDCPM](#iii-the-multi-dimensional-classification-system-for-penetration-testing-modeling-mdcpm)
- [A. Dimensionality of MDCPM](#a-dimensionality-of-mdcpm)
- [B. Case Study](#b-case-study)
- [IV. AUTOPT-SIM: A UNIFIED SIMULATION MODELING FRAMEWORK FOR AUTOMATED PENETRATION TESTING](#iv-autopt-sim-a-unified-simulation-modeling-framework-for-automated-penetration-testing)
- [A. AutoPT Simulation Modeling Framework](#a-autopt-simulation-modeling-framework)
- [B. Network Simulation Dataset and Network Generator](#b-network-simulation-dataset-and-network-generator)
- [V. CONCLUSION](#v-conclusion)
- [REFERENCES](#references)

---

Yunfei Wang*, Shixuan Liu*, Wenhao Wang*, Changling Zhou, Chao Zhang, _Member, IEEE_ , Jiandong Jin, Cheng Zhu 

**_Abstract_ —The integration of artificial intelligence into automated penetration testing (AutoPT) has highlighted the necessity of simulation modeling for the training of intelligent agents, due to its cost-efficiency and swift feedback capabilities. Despite the proliferation of AutoPT research, there is a recognized gap in the availability of a unified framework for simulation modeling methods. This paper presents a systematic review and synthesis of existing techniques, introducing MDCPM to categorize studies based on literature objectives, network simulation complexity, dependency of technical and tactical operations, and scenario feedback and variation. To bridge the gap in unified method for multi-dimensional and multi-level simulation modeling, dynamic environment modeling, and the scarcity of public datasets, we introduce AutoPT-Sim, a novel modeling framework that based on policy automation and encompasses the combination of all sub dimensions. AutoPT-Sim offers a comprehensive approach to modeling network environments, attackers, and defenders, transcending the constraints of static modeling and accommodating networks of diverse scales. We publicly release a generated standard network environment dataset and the code of Network Generator. By integrating publicly available datasets flexibly, support is offered for various simulation modeling levels focused on policy automation in MDCPM and the network generator help researchers output customized target network data by adjusting parameters or fine-tuning the network generator.** 

**_Index Terms_ —Automated Penetration Testing, Simulation Modeling, Penetration Testing Modeling** 

---

## I. INTRODUCTION 

HE Internet is crucial for modern life and social advance- **T** ment, significantly impacting government, finance, energy, and military sectors, yet cybersecurity remains a critical concern despite enhanced convenience and services [1, 2, 3]. Penetration testing, which simulates hacker attacks to assess vulnerabilities and overall security [4, 5], is vital for improving cybersecurity, but is complex and time consuming, relying on the expertise of the tester [6]. As a solution, automated penetration testing (AutoPT) has emerged to replace human efforts and accelerate evaluations [7]. 

Yunfei Wang and Cheng Zhu are with the National Key Laboratory of Information Systems Engineering, National University of Defense Technology, Hunan, China. E-mail: _{_ wangyunfei, zhucheng _}_ @nudt.edu.cn 

Shixuan Liu is with the Department of Intelligent Data Science, College of Computer Science and Technology, National University of Defense Technology, Hunan, China. E-mail: liushixuan@nudt.edu.cn 

Wenhao Wang is with the National University of Defense Technology, Hunan, China. E-mail: wangwenhao11@nudt.edu.cn 

Chao Zhang is with the Tsinghua University, Beijing, China. E-mail: chaoz@tsinghua.edu.cn 

Jiandong Jin and Changling Zhou are with the Computer Center, Peking University, Beijing, China. E-mail: _{_ jiandong.jin, zclfly _}_ @pku.edu.cn *These authors contributed equally. 

(Corresponding author: Cheng Zhu.) 

AutoPT involves two main processes: intelligent decisionmaking and automatic execution. The intelligent decisionmaking phase is critical, encompassing target identification, attack path selection, and method determination, effectively replacing manual judgments. Current approaches to intelligent decision-making can be classified into three categories: 

- 1) _Fixed Script Execution Methods_ employs predetermined rules, which limits adaptability and flexibility when working with other penetration tools [8]. 

- 2) _PDDL with Planner Methods_ leverage the PDDL language to define penetration actions, with classical planners facilitating the process [9, 10]. While PDDL enables detailed definition of penetration parameters and easy integration with tools, manually crafting these definitions is labor-intensive, requiring diverse approaches for various tools and tactics. 

- 3) _Artificial Intelligence Methods_ adopt attack trees [5], attack graphs [11], reinforcement learning [12, 13], and large language models [14, 15] to guide decision-making in penetration testing, representing a leading trend in current research. 

For all of the above categories, it is important to model target scenarios, technical and tactical elements, and decision parameters. AI methods, in particular, require extensive training in diverse scenarios to reveal hidden patterns and improve generalizability. 

On the other hand, the automatic execution phase utilizes various penetration tools to implement predetermined actions, automating tasks typically performed by human experts. Integrating intelligent decision-making with automatic execution seeks to help experts in network penetration, improve efficiency, reduce costs, and improve security outcomes [16]. 

As shown in Figure 1, training within real network environments or cyber ranges demands significant resources, making it impractical due to high time and financial costs, as well as the complexities involved. The inherent unpredictability and lack of reproducibility of real-world scenarios pose significant challenges for agents to in conducting repetitive training and recognizing patterns. By contrast, simulation environments provide a cost-effective and straightforward solution, with flexibility that allows for diverse scenarios and rapid feedback—key to improving the AutoPT decision-making process. 

The quality and fidelity of simulation modeling is crucial for effective algorithm training in AutoPT. Real-world application demands algorithms that are both capable of learning and refining their performance from data and reflective of essential real-world features. Despite advances in AutoPT research, 

IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 



![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0002-02.png)


<!-- Start of picture text -->
Real Network or Cyber Range<br>• High Temporal Expenditure<br>• Significant Economic Expenditure<br>• Substantial Complexity and Challenge<br>× • Limited Variability Simulation Modeling Challenge<br>• Inability to Capture Dynamic and  • Simulation Quality<br>Stochastic Characteristics Effectively . • Real-world Abstraction<br>• Lack of Systematic Simulation Model-<br>Simulation Environment ing Approaches<br>• Low Cost • Lack of Dynamic Scenario Modeling<br>• Simple and Flexible • Lack of Public Datasets<br>• Diverse Scenarios<br>Intelligent Automatic Execution • Rapid Feedback<br>Decision-making √<br>Automated Penetration Testing Training or Testing Environment<br><!-- End of picture text -->


![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0002-03.png)


Figure 1: The Necessity and Challenges of Simulation Environments Modeling in AutoPT 

there is a lack of systematic analysis of simulation modeling methodologies. Current methods are diverse and fragmented, lacking a unified framework for modeling characteristics, elements, granularity, and procedures. This hampers the development of efficient simulation models. A public dataset is essential for a rigorous and unbiased evaluation of penetration testing algorithms. Yet, concerns over security and privacy often result in a scarcity of public datasets for simulated networks, hindering a comprehensive assessment of AutoPT’s efficacy. 

Creating a unified framework presents several challenges. Firstly, the complexity of real-world systems demands models capable of encompassing diverse behaviors and interactions. Secondly, rapid technological advancements and evolving cyber threats require models that can be quickly updated. Thirdly, diverse research goals and stakeholder needs in AutoPT complicate the creation of a universally applicable framework. Lastly, privacy and security concerns must be prioritized, ensuring that models and datasets adhere to ethical standards while accurately depicting real-world attack scenarios and ensuring availability and reproducibility. 

This paper comprehensively reviews academic literature on AutoPT Modeling from the 1990s to today, focusing on key terms including AutoPT, network attack-defense games, automated red teams, and related areas. We offer an in-depth analysis and interpretation of simulation modeling methods used in various AutoPT studies. Our contributions include: 

- We are the first to analyze and classify simulation modeling methods in AutoPT. Through an extensive review of the literature on AutoPT, we decompose the elements in AutoPT’s simulation modeling and propose the **M** ulti- **D** imensional **C** lassification System for **P** enetration Testing **M** odeling (MDCPM) to systematically organize current simulation modeling methods within AutoPT. 

- To address the absence of a unified approach for multidimensional and multi-level simulation modeling, dynamic environment modeling, and the lack of public datasets, we introduce the AutoPT Simulation Modeling Framework (AutoPT-Sim), a novel framework that leverages policy automation and integrates all sub-dimensions 

across the other three dimensions. 

- We present a publicly available network simulation dataset along with the Network Generator code. This dataset can be flexibly combined to support various simulation modeling levels focused on policy automation within MDCPM. The Network Generator enables customizable network data generation by adjusting parameters or fine-tuning the settings, facilitating future research in AutoPT. 

The paper is organized as follows: Section 2 examines the theoretical foundations and core modeling elements in simulation modeling for AutoPT. Section 3 presents our proposed Multi-Dimensional Penetration Testing Modeling Classification System (MDCPM), discussing typical cases and current research trends. Section 4 introduces AutoPT Simulation Modeling Framework (AutoPT-Sim), along with the open-source network simulation dataset and Network Generator. Section 5 concludes with a summary of our contributions and future work. 

---

## II. THEORETICAL FOUNDATIONS OF AUTOPT SIMULATION MODELING 

---

## _A. Control Theory Perspective_ 

In AutoPT, simulation modeling not only involves the abstraction and modeling of the target cyberspace but also encompasses the modeling of interactive entities within the network—attackers and defenders. We draw upon nonlinear system theory from Modern Control Theory to understand and categorize simulation modeling in AutoPT. 

Modern control theory represents a significant domain within automatic control, dedicated to the analysis and design of complex systems, encompassing multiple-input-multipleoutput, nonlinear, and time-varying configurations. This theoretical framework utilizes state variables and state space equations to depict the dynamic behavior of systems, thereby elucidating their internal states. Such an approach conceptualizes a system as a unified entity, highlighting the interdependence of its components, feedback mechanisms, hierarchical structures, and open systems characteristics. In the context of AutoPT, this perspective facilitates a thorough understanding 

IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 


and simulation of cybersecurity dynamics by conceptualizing the target network, attackers, and defenders as an integrated system. Control theory quantifies the status of the system through assignment of a state and formally describe the progression of AutoPT. It adopts a state-based approach to define cost structures that balance security and availability. The _information state_ in control theory compresses attackerdefender information to a level sufficient for optimal decisionmaking, converting determining the optimal defense policy into a sequential optimization problem [17]. 

The complexity and variability of network activities, coupled with the multifactorial nature of penetration and defense strategies, means that identical actions on the same system can yield divergent outcomes, indicating that the penetration testing system is inherently dynamic. It implies that the same action combinations may produce different outputs, rendering linear differential equations inadequate for describing the system’s behavior. The superposition principle is inapplicable, thus classifying such systems as a dynamic nonlinear system. Traditional research often models penetration testing as a discrete system based on the actions of attackers and defenders, treating these actions as discrete events. The system’s output is influenced not only by its structural parameters but also by the inputs and initial conditions. 

---

## _B. AutoPT as a Dynamic Nonlinear System_ 

_1) System Components:_ The modeling framework in AutoPT incorporates both the abstract representation of network environments and the simulation of adversarial interactions between attackers and defenders. Environmental modeling directly shapes the objectives, action spaces, and strategic decision-making processes of both agents. Concurrently, their adversarial interactions induce environmental modifications, establishing a dynamic feedback loop that subsequently shapes their adaptive strategic responses. 

- Network environment: The target network environment, encompassing its architecture and assets, serves as the foundational framework for attack-defense interactions, shaping the dynamics, realism, and reliability of simulated engagements. Accurate modeling of network architecture and assets is critical for achieving realistic simulations, as it captures the fluidity and complexity of real-world network conditions. This precision enables a more robust assessment of vulnerabilities and the efficacy of defensive measures. 

- Attackers and defenders: AutoPT simulates adversarial tactics, techniques, and procedures to identify security vulnerabilities in target networks by modeling attacker and defender behaviors [16]. The attacker model requires explicit specification of objectives and permissible actions for simulated agents, while defender modeling accommodates greater flexibility, incorporating both static strategies (e.g., firewall policies, intrusion-detection system configurations [18]) and dynamic defense mechanisms [6]. Observations for both parties are characterized by incomplete information and noise, including missed detections and false alarms [17]. We assume an information structure adhering to the _perfect recall_ assumption, 

- wherein attackers and defenders retain complete historical records of past observations and decisions. Consequently, defenders at time _t_ maintain access to all prior historical data for decision-making. 

In partially observable environments involving attackers and defenders, two primary approaches exist for modeling their interactions [17]: probabilistic uncertainty and nondeterministic uncertainty. 

_2) System Dynamics:_ In the AutoPT system, randomness and dynamic behavior arise from three interdependent factors: adversarial interactions between attackers and defenders, fluctuations in network environments, and stochastic events. System dynamism is thus inherently tied to these interdependent factors. 

- Input-Output. Attacker and defender actions exhibit bidirectional coupling: their interdependent decisions act as both system inputs and state-dependent outputs, driving iterative state evolution. 

- State Transitions. The state _S_ ( _t_ +1) evolves stochastically based on _S_ ( _t_ ), concurrent actions _A_<sup>_A_</sup> ( _t_ ) (attacker) and _A_<sup>_D_</sup> ( _t_ ) (defender), and exogenous stochastic events _W_ ( _t_ ). 

- Feedback Mechanisms. The utility function _U_ ( _t_ ) = ( _U_<sup>_A_</sup> ( _t_ ) _, U_<sup>_D_</sup> ( _t_ )) critically shapes system dynamics by providing post-action feedback to both agents. This function serves dual roles: predefined reward signals or emergent behavioral outputs. 

_3) Formal expression:_ As illustrated in Figure 2, the AutoPT system comprises a target network environment, adversarial agents (attackers/defenders), and a state vector _S_ ( _t_ ) = [ _S_<sup>_E_</sup> ( _t_ ) _, S_<sup>_A_</sup> ( _t_ ) _, S_<sup>_D_</sup> ( _t_ )], where _S_<sup>_E_</sup> ( _t_ ), _S_<sup>_A_</sup> ( _t_ ) and _S_<sup>_D_</sup> ( _t_ ) denote the network, attacker, and defender states, respectively. Stochastic disturbances _W_ ( _t_ ), representing exogenous factors (e.g., hardware failures, user errors, or action success probabilities), introduce uncertainty into state transitions. These disturbances induce non-deterministic critical outputs even under identical inputs. For _t ≥ t_ 0, the system’s trajectory depends on the initial state _S_ ( _t_ 0), input vector _A_ ( _t_ ), and the probabilistic disturbance terms _W_ ( _t_ ). 

Attacker and defender actions exhibit dual input-output roles within the system. At time _t_ , the input _A_ ( _t_ ) = [ _A_<sup>_A_</sup> ( _t_ ) _, A_<sup>_D_</sup> ( _t_ )] comprises the attacker’s action vector _A_<sup>_a_</sup> ( _t_ ) = [ _a_<sup>_a_</sup> 1<sup>_, aa_</sup> 2<sup>_, . . . , aa_</sup> _p_<sup>]</sup> and the defender’s action vector _A_<sup>_D_</sup> ( _t_ ) = [ _a_<sup>_d_</sup> 1<sup>_, ad_</sup> 2<sup>_, . . . , ad_</sup> _q_<sup>]. The</sup> system output _Y_ ( _t_ ) = [ _Y_<sup>_A_</sup> ( _t_ ) _, Y_<sup>_D_</sup> ( _t_ )] mirrors this structure, with _Y_<sup>_a_</sup> ( _t_ ) = [ _y_ 1<sup>_a, y_</sup> 2<sup>_a, . . . , y_</sup> _p_<sup>_a_]and</sup><sup>_YD_(</sup><sup>_t_)=[</sup><sup>_y_</sup> 1<sup>_d, y_</sup> 2<sup>_d, . . . , y_</sup> _q_<sup>_d_].</sup> While _p_ = _q_ (distinct input-output dimensions for attackers and defenders), these can be standardized via zero-padding to a unified dimension _p_<sup>_′_</sup> , where _p_<sup>_′_</sup> = max( _p, q_ ), without loss of generality. We therefore understand the AutoPT simulation system as a discrete-time system, and its state equation can be represented as a stochastic difference equation: 


![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0003-16.png)


The system’s output equation is given as follows: 


![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0003-18.png)


IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 



![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0004-02.png)


<!-- Start of picture text -->
Attacker Action input output Defender Action<br>Target Network Environment<br>𝐴(𝑡𝑘) = 𝐴 𝐴 (𝑡𝑘), 𝐴 𝐷 (𝑡𝑘) Attackers and Defenders 𝑌(𝑡) = [𝑌 𝐴 (𝑡), 𝑌 𝐷 (𝑡)<br>𝑆(𝑡) = [𝑆 𝐸 (𝑡), 𝑆 𝐴 (𝑡), 𝑆 𝐷 (𝑡)]<br>Defender Action Attacker Action<br>input output<br>Nonlinear System<br>𝑆(𝑡𝑘+1) = 𝑓[𝑆(𝑡𝑘), 𝐴(𝑡𝑘), 𝑊 𝑡𝑘 , 𝑡𝑘]<br><!-- End of picture text -->

Figure 2: The Dynamic Nonlinear System Framework of AutoPT Simulation Modeling 

where, _tk_ represents the _k_ -th sampling instant within a discrete-time framework, and _k_ serves as the corresponding state index. 

Traditional penetration testing research often frames the process as a discrete system driven by isolated attacker and defender actions, modeled as discrete, isolated events [9, 19, 20]. However, system outputs are contingent upon structural parameters, system inputs, and initial conditions. This interdependence necessitates a holistic framework that accounts for inherent feedback dynamics, integrating interdependent variables to accurately capture penetration testing environments. 

---

## _C. Core Modeling Elements_ 

> **Section Summary:** In this section, we will introduce every core element in detail.


In this section, we will introduce every core element in detail. 

_1) Network Architecture and Target Assets:_ The target network environment involves both the network architecture and target assets. Primarily, network architecture refers to the structural design and configuration of an organization’s network systems, which are fundamental in shaping the design of attack vectors and defense strategies during penetration testing. This architecture can be delineated into two levels: 

- **Physical Connections:** Physical media, comprising guided media such as cables and optical fibers, and unguided media like wireless signals, facilitate data transmission between network devices. These connections are supported by infrastructure components such as routers, switches, fiber optic systems, network cables, and Bluetooth technology. 

- **Logical Topology:** Logical topology describes the structural relationships and data flow between network devices, such as routers and switches, irrespective of their physical locations or connection methods. It focuses on the interactions and communication pathways within the network, illustrating the interconnection patterns of network assets. Configurations may include star, ring, tree, or hybrid topologies [21]. 

Conversely, target assets represent all resources within penetration testing, including hardware, software, data, and personnel. These assets represent the primary objectives that attackers seek to access, manipulate, or compromise, including: 

- **Physical Resources:** Servers, workstations, desktops, laptops, mobile devices, external storage, network infrastructure, and security appliances. 

- **Virtual Resources:** Operating systems, software applications, open services, databases, and account credentials. 

The configuration and security posture of these assets determine their value, access policies, and defensive capabilities [22]. Moreover, the modeling of network architecture and target assets can be classified as either static or dynamic. Static modeling assumes that network architecture and configurations remain constant throughout the simulation, whereas dynamic modeling accommodates changes in the target environment due to actions by attackers or defenders, thereby replicating real-world conditions such as: 

- Variations in the status of enterprise hardware due to employee commuting. 

- Proactive network changes resulting from dynamic defense strategies like Cyber Mimic Defense [23] or Moving Target Defense [24]. 

- Randomness and uncertainty in network scenarios, such as the unpredictable failure of network devices and the non-deterministic outcomes of attack actions. 

_2) Attacker Models:_ The attacker model in AutoPT closely resembles real-world penetration testing methodologies, explicitly delineating identities, targets, and other relevant factors to inform strategic planning, resource allocation, and the selection of attack methods. 

- **Identity:** The identity of an attacker may vary from an individual, such as a script kiddie, to a collective, such as a state-sponsored hacking group. This identity could render varying attack methods and available resources. However, in practical testing scenarios, specifying this characteristic is often optional. 

- **Objectives:** An attacker’s objectives, influenced by their identity and the specific testing requirements, shape their actions within the network. Rapid access to sensitive areas prompts the use of direct paths and potent techniques [12]. If the objective is to achieve rapid access to sensitive areas, the attacker must employ the shortest attack path and most effective techniques to minimize the steps required. In contrast, if the objective is to identify numerous hidden security vulnerabilities within the network, the attacker should utilize diverse attack methods and carry out a broad spectrum of attacks. If the objective is to maintain a prolonged covert presence, the attacker must implement high-concealment strategies, such as Advanced Persistent Threat, advancing stealthily 


IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 

within the network while meticulously eliminating traces of their movements. 

- **Actions:** Attacker could exploit vulnerabilities, escalate privileges, conduct scans, and facilitate lateral movement. The Cyber Kill Chain model, developed by Lockheed Martin, offers a systematic approach to penetration testing [25]. Meanwhile, the MITRE ATT&CK framework [26] catalogs relevant TTPs (Techniques, Tactics, and Procedures) for AutoPT research. Due to the impracticality of incorporating all TTPs, researchers typically abstract an attack action library based on network architecture, target assets, and attacker-defender models. Each action is defined with specific preconditions, execution steps, and outcomes to optimize the penetration process. 

- **Network Visibility:** The type of penetration testing—black box, grey box, and white box—influences network visibility. During white box testing, the tester has full visibility and comprehensive knowledge of the system, including access to source code, architectural designs, and network topologies, enabling an in-depth evaluation of internal security measures [27, 28, 29, 30]. Grey box testing involves partial knowledge and access to internal data structures, log files, and application APIs, enhancing testing effectiveness [29, 31, 32]. Conversely, black box testing restricts testers to external observations, simulating real-world attack scenarios [27, 28, 29, 31, 33]. 

In AutoPT, the modeling of attackers, particularly their objectives and actions, is essential. The specification of objectives influences agents’ tactical decisions and the formulation of evaluation metrics, such as reward functions. Meanwhile, the modeling of actions must capture the variations in attackers’ capabilities and realistic impacts while preserving an appropriate level of abstraction. Failure to achieve this balance can complicate the training process and hinder the development of effective strategies. 

_3) Defender Models:_ Defenders are the security personnel responsible for safeguarding the network. They manage network connections through LANs, VLANs, firewalls, and various security measures [18, 34]. Their responsibilities include deploying intrusion detection systems, analyzing logs for anomalies [35], implementing antivirus software, and performing system updates to mitigate vulnerabilities. Additionally, they conduct security awareness programs through lectures and training to achieve protective objectives [36]. 

Despite their comprehensive visibility of the network, defenders typically lack awareness of the attacker’s presence and actions. While they actively monitor network conditions, they may not immediately correlate changes with potential attacks. Based on the level of proactive measures employed, defenders can be categorized into two distinct types: 

- **Static Defense:** Static defense is a predefined cybersecurity strategy that operates without adapting to evolving attack policy. This approach is characterized by its fixed nature, activating automatically under specific conditions in response to detected attacker activity or changes in network status. Examples include implementing firewall rules via established logical connections between de- 

- vices [37] and ensuring intrusion detection mechanisms via periodic reconnaissance. Within static defense, the success rates of attacker actions can represent defender ability. Despite its limitations in immediate response capabilities to new threats and attack techniques, static defense is considered an important auxiliary security measure. Its simplicity and reliability make it a popular choice for AutoPT, as much of the research in this area does not account for defender dynamics. 

- **Dynamic Defense:** Dynamic defense involves the definition of defense agents and an action library, encompassing preconditions, actions, and expected outcomes to enable real-time adjustments to defensive measures based on network conditions. This proactive strategy enhances security by disrupting communications and modifying network information to simulate an active defense [38, 39]. Furthermore, it complements active defense through methodologies such as Zero Trust Networks, Moving Target Defense, and honeypots. The flexibility inherent in dynamic defense modeling is essential for addressing the evolving landscape of cyber threats, ensuring effective protection by considering both attacker behavior and changes in network environments. 

Upon establishing the core elements, penetration testing can be understood as a dynamic interaction between attackers and defenders or as a series of unidirectional offensive maneuvers by attackers. The target network’s state evolves based on predefined logical relationships that dictate the outcomes of various actions. Furthermore, routine user activities may also alter the network’s assets and topology [9]. These changes collectively influence the decision-making for subsequent attack and defense actions. The penetration test is conducted through the iterative application of these strategies throughout the simulation. Our modeling classification method is constructed based on three perspectives: the overall aim of the research literature, the key elements presented in this section, and the interactions between these elements. We will first present the overall contributions of the paper, followed by an analysis on the core modeling factors. 

---

## III. THE MULTI-DIMENSIONAL CLASSIFICATION SYSTEM FOR PENETRATION TESTING MODELING: MDCPM 

In this section, we present the **M** ulti- **D** imensional **C** lassification System for **P** enetration Testing **M** odeling (MDCPM), an innovative approach for classifying target network scenarios modeling method in penetration testing. This system categorizes scenario modeling based on four principal dimensions: (1) Literature Objectives, (2) Network Simulation Complexity, (3) Dependency of Technical and Tactical Operations, and (4) Scenario Feedback and Variation. Each dimension comprises sub-dimensions for a nuanced classification of attack scenarios, as illustrated in Figure 3. This paper begins with an explanation of our classification criteria, followed by illustrative examples, and concludes with an analysis of the reviewed literature. 


IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 


![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0006-02.png)


<!-- Start of picture text -->
Automated Penetration Testing<br>Components<br>Intelligent  Jointly Decide Automatic<br>Decision-making Execution<br>Dimension 1:<br>Literature Objectives<br>Core Elements<br>Network Architecture Interact<br>Attacker and Defender<br>& Target Assets<br>Dimension  3:<br>Dimension  2:<br>Dependency of Technical and<br>Network Simulation Complexity<br>Tactical Operations<br>Dimension 4:<br>Scenario Feedback and Variation<br><!-- End of picture text -->

Figure 3: The Multi-Dimensional Classification System for Penetration Testing Modeling 

---

## _A. Dimensionality of MDCPM_ 

> **Section Summary:** In this section, we define and introduce the four primary dimensions characterizing the MDCPM, along with their associated sub-dimensions.


In this section, we define and introduce the four primary dimensions characterizing the MDCPM, along with their associated sub-dimensions. 

_1) Literature Objectives:_ The Literature Objectives analyze the aims and outcomes of various AutoPT studies, including tool development, policy proposals, and platform introductions. Based on the two phases of AutoPT—intelligent decision-making and automatic execution—we categorize this dimension into three sub-dimensions: . Specifically, technical automation pertains to automatic execution, while policy automation refers to intelligent decision-making; when a study simultaneously addresses both aspects, we classify it as complete automation. By organizing the research background, objectives, and significance of each study, we identify the literature’s goals and gain insights into each paper’s contributions, innovations, and applications. 

**Technical Automation:** This dimension emphasizes the direct implementation of specific technical and tactical procedures without strategic planning. It represents the earliest stage of automation, characterized by a lower level of intelligence in AutoPt. It automates predefined testing technicals such as identifying live hosts, open ports, services, and conducting vulnerability scans. Tools are central to this process. Nmap [40], Fscan [41], and Webshell [42] facilitate the identification of live hosts and services. Nessus and AWVS conduct automated vulnerability scans. Metasploit automates vulnerability verification and exploitation. These tools are essential for the autonomous execution phase of AutoPT, enabling the efficient performance of repetitive tasks and minimizing manual errors and time expenditure. 

**Policy Automation:** This aspect focuses on automated generation of attack policy without real-world execution, crucial 

for intelligent decision-making in AutoPT. It involves the automated planning of attack paths and technical actions, representing a key focus in contemporary AI research for AutoPT [43, 44, 45]. For instance, Hu et al. use Multi-host Multi-stage Vulnerability Analysis to construct an attack tree for network topologies, applying Deep Q-Networks (DQN) to identify the most exploitable attack paths [12]. Zhou et al. [46] frame penetration testing as a Markov Decision Process and used an improved deep q-network to decouple actions and learn attack strategies. However, their methodologies remain limited to policy generation in theoretical network environments, lacking integration with actual penetration tools or execution of attack payloads in real-world scenarios. 

**Complete Automation:** While the two aforementioned aspects are crucial, they both represent only singular aspects of penetration testing. A comprehensive security assessment requires the integration of automatic execution and intelligent decision-making to effectively identify and mitigate potential security threats. Complete automation encompasses automation of the entire attack lifecycle, from decision-making to execution. This includes the automatic planning of attack paths and the integration of execution tools with actual payloads to perform real-world penetration tests in either simulated or live network environments, entirely without human intervention [5, 47, 48]. 

Literature objectives deepen our understanding of research trends in AutoPT, providing insights into theoretical advancements and practical implications while clarifying the current landscape and future directions. Moreover, these objectives could also facilitate the classification of network simulation complexity, modeling dependencies between technical and tactical operations, as well as scenario feedback and variation. 

_2) Network Simulation Complexity:_ This dimension focuses on network architecture and target assets-the first element 

IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 


of AutoPT simulation modeling. This dimension is further divided into two sub-dimensions based on the abstraction level and construction methods of network attributes: hypothetical and authentic attributes. 

**Simulation of Hypothetical Attributes:** Numerous studies utilize numerical, rule-based, or conceptual methods to abstractly model assets and architectures. For instance, Hammar et al. utilize numerical attributes to characterize nodes in a four-node network, with each node represented by multidimensional metrics of defensive and detection capabilities [20]. 

**Simulation of Authentic Attributes:** Certain studies employ real-world systems, software, services, account passwords, vulnerabilities, and other real information to model target assets and attributes. These works utilize complex network topologies to accurately replicate real-life environments, reflecting both node attributes and their interrelationships. For example, Microsoft’s CyberBattleSim defines the operating systems, software, vulnerabilities, and node reward for each node while establishing diverse connection relationships across multiple small scenarios involving fewer than 20 nodes [49]. 

_3) Dependency of Technical and Tactical Operations:_ This dimension analyzes attacker and defender models to assess whether their defined actions incorporate interdependencies, specifically determining if the outcome of one action serves as a prerequisite for subsequent actions. 

**Isolated Technical and Tactical Actions:** Many technical and tactical actions are independent, lacking defined prerequisites. This category includes executing single tactics, such as using Nmap for scanning, or multiple unrestricted actions. For example, Sarraute et al. [50] defined only scanning and vulnerability exploitation actions in a penetration scenario. Although agents may implicitly learn that scanning before exploitation improves the success rate of vulnerability selection, the action definitions do not specify prerequisites, allowing actions to be performed independently. 

**Coordinated Technical and Tactical Actions:** Many technical and tactical actions are interdependent, forming an integrated kill chain. This coordination is evident in stages such as privilege escalation and lateral movement, where initial actions like vulnerability exploitation or phishing attacks precede subsequent activities such as credential theft and malware implantation. Defining the preconditions and post-effects of actions is essential. For example, Filiol et al. [29] modeled attacker behavior by specifying logical relationships among actions, including domain name acquisition, IP scanning, service version collection, attack list generation, and attack configuration. 

Dependency of Technical and Tactical Operations investigates the explicit interrelationships between sequential actions essential for precise simulation modeling. In real-world penetration testing scenarios, actions are constrained by execution limitations, and their variability hinders standardization efforts. Many studies overlook these dependencies, thereby simplifying execution constraints and standardizing decision parameters, which increases abstraction and reduces alignment with real-world conditions. Addressing this gap is crucial for the effective transition of simulation models to practical environments. 

In existing research, isolated and coordinated technical and tactical operations are frequently combined. For example, CALDERA [6] employs coordinated technical and tactical actions to simulate an attacker’s lateral movement, privilege escalation, and data theft by imposing action dependencies. Meanwhile, it also utilizes isolated technical and tactical actions to represent a passive defender unaware of the attacker, limited to independent actions such as random reboots and logins. Although classified as a continuous tactic scenario, CALDERA incorporates isolated tactics in its modeling. 

_4) Scenario Feedback and Variation:_ This dimension classifies modifications to the target network’s architecture and assets, including changes in host connectivity, installed systems and software, account credentials, and vulnerabilities. It does not account for attributes related to attackers and defenders, such as an attacker’s privilege level or newly acquired credentials. This dimension involves two types of changes: scenario feedback and scenario variation. 

**Scenario Feedback** refers to passive changes arising from interactions between attackers and defenders that affect the target network’s architecture and assets. This includes attacker actions such as establishing connections, deploying phishing emails or malware, and causing network disruptions, as well as defender responses like system shutdowns, credential remediation, and software updates. These alterations occur only when attackers and defenders engage, characterizing them as passive changes. In contrast, **Scenario Variation** involves predefined modifications within simulation models designed to emulate real-world user operations or dynamic network configurations. Examples include simulating user behavior, scheduling power operations to reflect work routines, conducting traffic simulations for behavioral drills, periodically updating IP addresses and systems, and implementing defense strategies such as Moving Target Defense (MTD), Cyber Mimic Defense (CMD), load balancing, and Endogenous Safety and Security (ESS). These changes are integrated into the scenario and execute according to predetermined schedules or conditions, independent of the immediate actions of attackers or defenders, thus qualifying them as active changes. Figure 4 illustrates the Scenario Feedback and Variation dimension. 

Based on these two aspects in AutoPT modeling, scenario feedback and variation are categorized into three subdimensions: 

**Completely Static Scenario:** A scenario with no passive modifications from attack-defense interactions and no active alterations to the target environment. 

**Semi-Dynamic Scenario:** A scenario that incorporates passive changes resulting from attack-defense interactions but does not include active modifications to the target environment. 

**Completely Dynamic Scenario:** A scenario that encompasses both passive changes from attack-defense interactions and active alterations to the target environment. 

---

## _B. Case Study_ 

> **Section Summary:** To clarify MDCPM, we present and analyze four representative cases, including:


To clarify MDCPM, we present and analyze four representative cases, including: 

IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 



![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0008-02.png)


<!-- Start of picture text -->
Scenario Feedback and Variability<br>Primary Target<br>Target Scenario: Network Architecture and Target Assets<br>Two Types of Changes<br>Passive:  Active :<br>Scenario Feedback Scenario Variability<br>Caused by Caused by<br>Interactions between  User Operations or<br>Attackers and Defenders Dynamic Network Design<br>×<br> × ×<br>Completely  Semi- Completely<br>Static  Dynamic  Dynamic<br>Scenario Scenario Scenario<br><!-- End of picture text -->

Figure 4: The connotation and sub-dimensions of the Scenario Feedback and Variation 

- Penetration Testing Tools: These tools automate key security tactics and techniques, essential for conducting AutoPT in real-world scenarios. 

- Numerical Simulation Networks [20]: Although highly abstract and detached from real-world conditions, these networks provide a theoretical framework for exploring cybersecurity complexities. 

- CyberBattleSim [49]: Developed by Microsoft, this simulation platform is employed in various studies for both simulation and emulation purposes. 

- Network Attack Simulator [37]: Released by Harvard University, this popular simulator specializes in network attack simulations, enhancing the understanding of penetration testing behaviors. 

These cases are widely cited and diverse, encompassing a broad spectrum of classifications in existing research. Analyzing them provides deeper insights into the classification principles and applications of MDCPM. 

_1) Penetration Testing Tools:_ Penetration testing tools typically incorporate technical automation, simulate authentic attributes, execute isolated technical and tactical actions, and utilize either entirely static scenarios or impose no scenario restrictions. These AutoPT tools are essential for network security, enabling professionals to identify and evaluate vulnerabilities within networks, applications, and systems. The following are some widely used automated tools: 

- Nmap (Network Mapper) [40]: A multifunctional security and port scanner designed to efficiently evaluate individual hosts or large networks. It offers features such as host discovery, port scanning, service identification, operating system detection, version scanning, and script scanning. 

- Nessus [51]: A comprehensive vulnerability scanner developed by Tenable, designed to identify security vulnerabilities in systems, networks, and applications. It scans targets such as IP addresses and domains, and generates detailed reports that include vulnerability descriptions, severity ratings, and recommended remediation actions. 

- Metasploit [52]: Metasploit is a collaborative framework designed for vulnerability validation and security 

assessments, operating through distinct modules. Auxiliary Modules perform scanning, fingerprinting, e.t.c, to support penetration testing. Exploit Modules utilize identified vulnerabilities to infiltrate systems. Payload Modules execute post-exploitation tasks, enabling arbitrary command execution on targets. Post-Exploitation Modules secure further access and gather additional data from compromised systems. Encoder Modules obfuscate payloads to bypass security mechanisms. 

Many AutoPT tools automate specific penetration testing steps but often require manual input for targets and parameters, making it difficult to conduct the entire process without human involvement. These tools fall under Technical Automation and simulate authentic attributes based on realworld network. Their technical and tactical measures can be executed in isolation, categorizing them as Isolated Technical and Tactical Actions. Although applicable to various scenarios, they are typically confined to secure environments due to legal and ethical considerations and operate within static scenarios without active user interaction. 

_2) Numerical Simulation Networks:_ Numerical simulation networks encompass policy automation, simulation of hypothetical attributes, execution of isolated technical and tactical actions, and semi-dynamic scenarios. 

Hammer et al. investigated attack–defense interactions in penetration testing using a four-node numerical simulation network [20]. Figure 5 presents the network architecture, its graphical representation and attribute model. In the left diagram, _Nstart_ represents the attacker’s computer, while the other nodes correspond to defender components. The attacker’s objective is to compromise _Ndata_ . The middle diagram formalizes the network as a graph, with nodes representing components and edges indicating connections. Each node _k_ is characterized by attributes _Sk_ = _{Sk_<sup>_A, S_</sup> _k_<sup>_D}_,whichinclude</sup> both attack and defense values. The attack attributes _Sk_<sup>_A_=</sup> _{Sk,_<sup>_A_</sup> 1<sup>_, S_</sup> _k,_<sup>_A_</sup> 2<sup>_, . . . , S_</sup> _k,m_<sup>_A}_represent the strength of</sup><sup>_m_attack types</sup> and are visible only to the attacker. The defense attributes _Sk_<sup>_D_</sup> = _{Sk,_<sup>_D_</sup> 1<sup>_, S_</sup> _k,_<sup>_D_</sup> 2<sup>_, . . . , S_</sup> _k,m_<sup>_D_</sup> +1<sup>_}_arevisibleonlytothede-</sup> fender, where the first _m_ attributes correspond to the respective attack types and the ( _m_ + 1)-th attribute indicates detection capability. This study simulates hypothetical attributes, and the target network remains static. 

The attacker can perform two actions on a node _k_ : (1) reconnaissance to reveal the defense state _Sk_<sup>_D_, and (2) execute</sup> an attack of type _j ∈{_ 1 _,_ 2 _, · · · , m}_ , increasing the attack state _Sk,j_<sup>_A_by one. The defender can take two actions on node</sup><sup>_k_: (1)</sup> monitoring operations to enhance the node’s detection ability _Sk_<sup>_D_</sup> :
- _m_ +1<sup>,and(2)defensiveoperationstostrengthendefenses</sup> against attack type _j ∈{_ 1 _,_ 2 _, · · · , m}_ , thereby increasing _Sk,j_<sup>_D_.</sup> The attacker and defender alternate actions. If _Sk,j_<sup>_A> S_</sup> _k,j_<sup>_D_for</sup> any attack type _j_ , the attacker compromises node _k_ , making its neighbors visible. If the attack does not compromise the node, the defender detects it with probability _p_ = _Skw_<sup>_D_</sup> <u>
- </u> _m_ +1+1<sup>,basedon</sup> the node’s detection ability _Sk_<sup>_D_</sup>
- _m_ +1<sup>.</sup>

From the attacker and defender models, it is evident that both can execute actions without constraints, allowing them to act independently. This categorizes their actions as Isolated 

IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 



![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0009-02.png)


<!-- Start of picture text -->
𝑆0𝐴 = 0,0,0,0<br>𝑁𝑠𝑡𝑎𝑟𝑡 𝑁𝑠𝑡𝑎𝑟𝑡 𝑆0𝐷 = [0,0,0,0,0]<br>𝑆𝑆1𝐷1𝐴= [9,1,7,8,1]= 0,0,0,0 𝑆𝑆0𝐷0𝐴= [9,7,1,8,1]= 0,0,0,0<br>𝑁𝑑𝑎𝑡𝑎 𝑁𝑑𝑎𝑡𝑎 𝑆𝑆0𝐷0𝐴= [5,9,8,1,1]= 0,0,0,0<br>Network Model Graph Model Attribute Model<br><!-- End of picture text -->


![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0009-03.png)


Figure 5: A numerical simulation network with four nodes [20]. The left, middle, right diagram shows the network model, graph model and attribute model, respectively. 

Technical and Tactical Actions. The defender’s actions modify the network’s defense attributes and enhance its monitoring capabilities, resulting in passive changes to the network. Since there are no active alterations, the scenario is classified as Semi-Dynamic. The game aims to determine optimal strategies without involving real-world tactical executions or attack payloads, classifying it as Policy Automation. 

In summary, Hammer et al.’s approach is characterized by Policy Automation, Simulation of Hypothetical Attributes, Isolated Technical and Tactical Actions, and a Semi-Dynamic Scenario. 

_3) CyberBattleSim:_ CyberBattleSim is an open-source research project initiated by Microsoft in 2021 that uses highlevel abstractions of computer networks and cybersecurity concepts to study how autonomous agents operate within simulated corporate environments [49]. Numerous studies have used it for AutoPT research [34, 53, 54, 55]. With our classification system, CyberBattleSim is categorized under policy automation, simulation of authentic attributes, coordinated technical and tactical actions, and semi-dynamic scenarios. 

CyberBattleSim focuses on threat modeling during the postcompromise lateral movement phase of network attacks. It simulates a fixed network topology with parameterized vulnerabilities, allowing attackers to exploit these weaknesses for lateral movement. A target network scenario, illustrated in Figure 6, consists of nodes running various operating systems and software. Each computer has specific attributes, values, and pre-assigned vulnerabilities. Communication between nodes is depicted by black edges labeled with communication protocols. The target network is constructed using realistic attribute simulations, and the scenario remains static without active changes. 

The attacker aims to gain network control by exploiting vulnerabilities and maximizing rewards through three actions: performing a local attack, performing a remote attack, and connecting to other nodes. Actions are parameterized by the source node where the underlying operation should take place, and they are only permitted on nodes owned by the agent. As illustrated in Figure 6, the attacker starts from a Windows 7 node, exploits vulnerabilities, and uses cached credentials to move laterally, ultimately accessing an SQL database. Defenders monitor activities to detect and mitigate attacks by reimaging infected nodes. Attack success also depends on predefined probabilities. 


![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0009-10.png)



![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0009-11.png)



![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0009-12.png)


<!-- Start of picture text -->
Windows 2019<br>SQL Server 12<br><!-- End of picture text -->


![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0009-13.png)


<!-- Start of picture text -->
Vulnerability X.Y.Z<br>SQL SQL<br>Initial agentWindows 7node SMB SMB hack Windows 2008SQL ServerTesting Windows 2019 IIS websiteconnectionSQL usingLeakedstring<br>SQL Linqpad CredsLeak<br>IIS IIS vulnerability<br>… vulnerability<br>RDP  using HTTP HTTP HTTP<br>credentials<br><!-- End of picture text -->

Figure 6: Schematic Diagram of CyberBattleSim Network [49] 


![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0009-15.png)


<!-- Start of picture text -->
Subnet_1<br>(1, 0)<br><!-- End of picture text -->


![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0009-16.png)



![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0009-17.png)



![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0009-18.png)



![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0009-19.png)


<!-- Start of picture text -->
(3, 0) (3, 1) (3, 2)<br><!-- End of picture text -->


![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0009-20.png)



![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0009-21.png)



![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0009-22.png)



![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0009-23.png)


<!-- Start of picture text -->
Subnet_4<br>(5, 0) (5, 1) (5, 2)<br><!-- End of picture text -->


![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0009-24.png)


<!-- Start of picture text -->
Subnet_5<br>(5, 0) (5, 1) (5, 2)<br><!-- End of picture text -->


![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0009-25.png)


<!-- Start of picture text -->
Subnet_2<br>(2, 0)<br><!-- End of picture text -->

Figure 7: Network Architecture Diagram of Network Attack Simulator [37] 

The attacker modifies network communication and architecture, while defenders reimage systems, patch vulnerabilities, and alter node attributes. Consequently, the target network undergoes passive changes from both attacker and defender actions without active alterations, classifying it as a semidynamic scenario. CyberBattleSim conducts abstract simulations without executing real attack code, emphasizing agent interactions. It is designed for small to medium networks (10–20 nodes) and does not support fully dynamic scenarios. 

_4) Network Attack Simulator:_ The Network Attack Simulator [37], a lightweight, open-source tool developed by Schwartz et al. in 2019, is a groundbreaking application of reinforcement learning in AutoPT research. The simulator constructs a network environment of multiple subnets with firewall-controlled access, each containing machines running various services. As shown in Figure 7 [37], the architecture includes node attributes such as address (subnet <u>ID,</u> machine ID), machine value, and parameters (open services, success rate, exploitation cost). The network architecture and asset modeling utilize real-world data for the simulation of authentic attributes, remaining static throughout the process. 

Focusing solely on attacker modeling, the simulator allows for individual scanning actions and vulnerability exploitation targeting services on each machine. Scanning identifies services on ports, which are then exploited based on the machine’s configuration. The attacker’s actions are independent; one does not depend on the completion of another. Although scanning can guide vulnerability selection, traversing execution vulnerabilities can also grant access to the target machine. Importantly, these actions do not alter the target network, 

IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 


reinforcing the classification of the scenario as completely static. 

_C. Research on Existing Penetration Testing Scenario Modeling Methods_ 

In summary, Network Attack Simulator combines policy automation, authentic attribute simulation, isolated technical and tactical actions, and a completely static scenario. While it implicitly represents static defenders through subnet and machine connections and vulnerability success rates, the tool’s simplicity limits its scalability for larger networks and lacks explicit defender modeling or a dynamically changing network environment. 

We conducted a systematic literature review of AutoPT studies using Web of Science, Scopus, and IEEE Xplore (1990s-present). A two-stage screening process filtered out irrelevant and low-quality papers. Inclusion criteria consisted of thematic relevance, methodological rigor, academic impact, and research recency. After applying these criteria, 65 representative documents were selected for analysis, with 33 from 2020-2024. Each study was cross-reviewed by at least two 

Table I: Classification Table of Simulation Modeling Methods in Typical Literature on Automated Penetration Testing 

|||Literature Obje|ctives|Network Simula|tion Complexity|Dependenc|y of T&T Operations|Scenar|io Feedback and|Variation|
|---|---|---|---|---|---|---|---|---|---|---|
|Year|Paper|Technical<br>Policy|Complete|Hypothetical|Authentic|Isolated|Coordinated|Static|Semi-Dynamic|Dynamic|
|1997|Haeni et al. [56]<br>Nma[57]|✓<br>✓|||✓<br>✓|✓<br>✓||—<br>—|—<br>—|—<br>—|
|1998|p <br>Nessus [51]|✓|||✓|✓||—|—|—|
|2001<br>2002|McDermott et al. [58]<br>Skl59|✓<br>✓||✓|✓|✓|✓|✓<br>✓|||
|2003|aggs et a. []<br>Metasploit [52]|✓|||✓|✓||—|—|—|
|2005|Liu et al. [60]|✓|||✓|✓||✓|||
||Kosuga et al. [61]<br>Fl62|✓<br>✓|||✓<br>✓|✓<br>✓||✓<br>✓|||
|2007|onseca et a. []<br>Shen et al. [63]|✓|||✓||✓||✓||
||Cone et al. [64]|✓||✓||✓||✓|||
|2009|Lyon et al. [40]|✓|||✓|✓||—|—|—|
||Greenwaldetal.[65]|✓|||✓|✓||✓|||
|2011|<br>Sarraute et al. [66]|✓|||✓||✓||✓||
||Sarraute et al. [50]<br>|✓|||✓<br>|✓||✓|||
|2013|Sarraute et al. [47]||✓||✓||✓||✓||
||Van Dijk et al. [67]|✓||✓||✓||✓|||
|2014|Chapman et al. [68]|✓||✓||✓||✓|||
|2016|Applebaum et al. [6]<br>Chapman et al. [69]|✓<br>✓||✓<br>✓||✓<br>✓||✓|✓||
||Elderman et al. [39]|✓||✓||✓|||✓||
|2017|Applebaum et al. [9]<br>Ficco et al. [70]|✓<br>✓|||✓<br>✓|✓|✓|✓||✓|
|2018|Miller et al. [19]<br>Ghanem et al. [7]|✓<br>✓|||✓<br>✓||✓<br>✓|✓<br>✓|||
||Casolaetal[71]|✓|||✓||✓|✓|||
||. <br>Ghanem et al. [72]||✓||✓||✓||✓||
||Paul et al. [38]|✓|||✓||✓||✓||
||Shttl37|✓|||✓||✓|✓|||
||cwarz e a. []<br>Paul et al. [73]|✓||✓||✓|||✓||
|2019|Zhou et al. [74]<br>|✓<br>|||✓<br>||✓<br>|✓|||
||Zang et al. [10]|✓|||✓||✓||✓||
||Huetal[12]|✓|||✓||✓|✓|||
||. <br>Hammar et al. [20]|✓||✓||✓|||✓||
||Valea et al. [75]|✓|||✓|✓||✓|||
||Bhattacharya et al. [76]<br>|✓<br>|||✓<br>||✓||✓||
||Nguyen et al. [77]<br>Cttl78|✓<br>✓|||✓<br>✓|✓<br>✓||✓<br>✓|||
|2020|osa e a. []<br>||||||||||
||Chowdhary et al. [13]|✓|||✓||✓|✓|||
||Bland et al. [79]<br>|✓<br>|||✓<br>||✓||✓||
||Hu et al. [80]|✓|||✓|✓||✓|||
||Enochetal.[43]|✓|||✓||✓|✓|||
||<br>Schwartz et al. [44]|✓|||✓|✓|||✓||
||Dorchuck et al. [5]||✓||✓||✓|✓|||
||Qian et al. [81]<br>|✓<br>|||✓<br>||✓<br>|✓<br>|||
|2021|Filiol et al. [29]<br>Zhouetal[46]|✓<br>✓|||✓<br>✓||✓<br>✓|✓<br>✓|||
||. <br>Hacks et al. [8]|✓|||✓||✓||✓||
||Erd˝odietal[82]|✓|||✓||✓|✓|||
||. <br>Ji et al. [83]|✓|||✓|✓|||✓||
||Dillon et al. [36]|✓||✓|||✓||✓||
||Yamin et al. [84]<br>||✓||✓<br>||✓<br>||✓<br>||
|2022|Confdo et al. [85]<br>Ttl86|✓<br>✓|||✓<br>✓||✓<br>✓||✓<br>✓||
||ran e a. []<br>Hance et al. [87]|✓|||✓||✓|✓|||
||Færøetal[88]|✓|||✓|✓||✓|||
|2023|y  . <br>Li et al. [89]|✓|||✓||✓|✓|||
||Xu et al. [48]<br>||✓||✓<br>||✓<br>|✓<br>|||
||Becker et al. [45]<br>Li et al. [53]|✓<br>✓|||✓<br>✓||✓<br>✓|✓|✓||
|2024|Alshehri et al. [90]<br>|✓<br>|||✓<br>||✓<br>|✓<br>|||
||Deng et al. [15]|✓|||✓||✓|✓|||
||Wang et al. [91]<br>|✓<br>|||✓<br>||✓|✓|||
||Li et al. [92]<br>Wang et al. [93]|✓<br>✓|||✓<br>✓|✓<br>✓||✓||✓|



IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 


Table II: Classification Statistics of Simulation Modeling Methods in Automated Penetration Testing Literature 


![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0011-03.png)


<!-- Start of picture text -->
Types TechnicalLiteraturePolicObyjectivesComplete NetworkHypotheticalSimulationAuthenticComplexity DeIsolatedpendency of CoordinatedT&T Operations Completely StaticScenarioSemi-DFeedbackynamicand VariationCompletely Dynamic<br>Quantity 17 43 5 10 55 29 36 43 20 2<br>Literature Objectives Trends Over Time Network Simulation Complexity Trends Over Time<br>35 100 35 100<br>Technical Hypothetical 31<br>30 Policy 80 30 Authentic 80<br>Complete<br>25 23 25<br>20 'Technical' Percentage 60 20 'Hypothetical' Percentage 60<br>15 'Policy' Percentage'Complete' Percentage 15 40 15 'Authentic' Percentage 13 40<br>10 5 5 7 20 10 8 6 20<br>5 3 2 2 3 5 3 2 2<br>0 0 0 0<br>0 0 0 0<br>before 2000 2000-2009 2010-2019 2020-2024 before 2000 2000-2009 2010-2019 2020-2024<br>Dependency of Technical and Tactical Operations Trends Over Time Scenario Feedback and Variation Trends Over Time<br>35 100 35 100<br>Isolated  Completely Static<br>30 Coordinated 80 30 Semi-Dynamic 80<br> Completely Dynamic<br>25 23 25<br>21<br>20 'Isolated' Percentage 60 20 'Completely Static' Percentage 60<br>'Semi-Dynamic' Percentage<br>15 'Coordinated' Percentage 40 15 'Completely Dynamic' Percentage 40<br>11 10 10 11<br>10 8 8 10 7 8<br>20 20<br>5 3 0 2 5 3 2 0 1 0 1 1<br>0 0 0 0<br>before 2000 2000-2009 2010-2019 2020-2024 before 2000 2000-2009 2010-2019 2020-2024<br>Percentage Percentage<br>Articles Number Articles Number<br>Percentage Percentage<br>Articles Number Articles Number<br><!-- End of picture text -->

Figure 8: Temporal Variations in Article Volume Across Dimensions 

researchers to ensure accuracy and reliability. We categorized AutoPT modeling methods according to their characteristics (Table I) and examined the research background, objectives, and significance of each article. 

We summarized the article count across four dimensions in Table II. Notably, some automated execution tools like Nessus, Metasploit, and nmap have unrestricted application scenarios (therefore denoted by dash notation). Generally, their use requires consideration of legal and ethical constraints, typically in isolated network environments, categorized as Completely Static Scenarios. 

Policy automation and intelligent decision-making are prominent research areas, attracting significant academic attention. Most studies focus on simulating authentic attributes and continuous technical actions, closely mirroring practical scenarios. However, research on dynamic environments remains limited. For example, Applebaum et al. [9] introduce active network changes using gray agents, but initiate only one connection set per round, resulting in minimal alterations within small to medium networks (11–21 hosts). Similarly, Li et al. [92] carefully define network changes but do not quantify them or test scalability in larger networks. Their experiments are confined to a 10-node network and overlook dynamic simulation and emulation for larger systems. Additionally, their simplistic action settings focus on vulnerability exploitation without addressing the logical relationships among multiple penetration tactics. 

Table II summarizes literature classifications over time, 

while Figure 8 shows trends in article volumes across dimensions. Initially, AutoPT research focused on Technical Automation, emphasizing the automation of specific tactics and steps. Over time, Policy Automation became more prominent, evolving from simulating hypothetical attributes and isolated actions to simulating authentic attributes and coordinated technical and tactical actions. This shift reflects reduced abstraction in simulation modeling and a closer alignment between models and reality, paving the way for integrating intelligent decision-making algorithms with automated tools for Complete Automation. Ongoing research in Complete Automation typically streamlines the AutoPT process by targeting specific components, incorporating one or more automated tools—such as rules, planners, or basic reinforcement learning models—to develop action-guiding strategies with a greater emphasis on engineering implementation and lower intelligence levels. Notably, Ghanem et al. [72] focus on automating strategy generation using tools like MSF for execution. Although Complete Automation is not fully achieved, their work is practically significant and classified under Complete Automation, demonstrating the flexibility of our criteria. 

Besides, most studies focus on static or semi-dynamic scenarios, neglecting active network changes and dynamic information. Approaches like Cyber Mimic Defense [23] and Moving Target Defense [24] signal a shift toward dynamic network security strategies. Future research should integrate both active and passive network changes to enable intelligent decision-making and automated execution in fully dynamic 

IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 



![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0012-02.png)


<!-- Start of picture text -->
Sensitive<br>Business<br>…… Area<br>General<br>Switch_0 Switch_i Business<br>Area<br>Server_ 0<br>…… DMZ<br>Lan_1 Lan_2 Lan_i<br>Full Mesh<br>(a) Partitioned and Layered Topology Network<br>(b) Tree Topology Network<br>Core<br>Layer<br>Pod 0<br>Convergence<br>Layer<br>Switch_0<br>Access<br>Layer<br>Server_0<br>(c) FatTree Topology Network<br>Server Switch edge LAN Pod<br><!-- End of picture text -->

Figure 9: Three Types of Network Topology in AutoPT-Sim 

environments. Additionally, existing studies typically simulate only small to medium-sized networks [9, 49, 92], overlooking large-scale network modeling and the impact of diverse network architectures on penetration testing. Furthermore, current simulation methods lack flexibility, focusing on limited combinations without providing a unified approach for multidimensional and multi-level simulation modeling. 

---

## IV. AUTOPT-SIM: A UNIFIED SIMULATION MODELING FRAMEWORK FOR AUTOMATED PENETRATION TESTING 

> **Section Summary:** Current scenario modeling methods are often incomplete, exhibit low variability, lack fully dynamic capabilities, and are hindered by the absence of public datasets.


Current scenario modeling methods are often incomplete, exhibit low variability, lack fully dynamic capabilities, and are hindered by the absence of public datasets. To address these limitations, we introduce the AutoPT Simulation Modeling Framework (AutoPT-Sim), which leverages policy automation to integrate all sub-dimensions of the MDCPM framework across its three primary dimensions. Additionally, we provide 

a comprehensive and publicly accessible dataset on GitHub<sup>1</sup> to support future research endeavors. We welcome constructive feedback to refine our standards and dataset further. Furthermore, we have developed a suite of interfaces to underpin future extensions in tactical and full-process automation. 

---

## _A. AutoPT Simulation Modeling Framework_ 

Our model enables AutoPT research within internal networks by automating policy scenarios and simulating all penetration testing phases, including information gathering, foothold establishment, privilege escalation, lateral movement, and persistence. We provide diverse network architectures and asset modeling techniques to support dynamic network construction. Additionally, attacker and defender actions are comprehensively modeled, allowing for customizable configurations. 

1www.github.com/feifei-feifei-hub/Simulation-Modeling-for-AutomatedPenetration-Testing 

IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 


_1) Network Architecture and Target Asset Modeling:_ We model the target network by combining its architecture and assets into a graph _G_ = ( _V, E, X_ ), where nodes _V_ represent network devices, edges _E_ denote their connections, and _X_ captures attributes for both nodes and edges. Computer networks naturally form graph structures [94]. Each node _V_ = _{_ 1 _,_ 2 _,_ 3 _, . . . , N }_ corresponds to a device, with attributes _Xi_ detailing systems, services, and credentials. Edges _E_ represent both wired and wireless communications. An edge _eij_ exists if node _i_ can communicate with node _j_ , with link attributes _Xij_ specifying protocols, traffic size, and more. All nodes have a type attribute distinguishing categories like server or switch, effectively capturing configurations and functionalities through attributes such as software and services. 

To emulate attackers’ extensive maneuverability in internal networks, all connections are bidirectional. Our penetration testing framework emphasizes lateral movement by focusing on node configurations and attributes rather than simulating traffic. We incorporate various network topologies to reflect real-world diversity, and our network generator allows for the expansion of directed links and link attributes to represent data flow characteristics. The specific methods for network architecture and target asset modeling are detailed below. 

**Network Architecture Modeling.** Our simulated network model assumes direct connections between nodes on the same LAN and switch-mediated communication between nodes on different LANs. The network graph features undirected edges, enabling bidirectional communication between nodes. To capture the diversity of real-world network topologies, our framework incorporates multiple classic topologies, as well as partitioned and layered topologies informed by expert insights. These topologies are illustrated in Figure 9. 

- **Partitioned and Layered Topology Network** : We employ a customized network topology, initially introduced by Sarraute et al. [95] and subsequently refined through expert consultation with cybersecurity professionals. The PLTN architecture is specifically designed for performance testing and comprises three distinct regions: (1) the Demilitarized Zone (DMZ), (2) the General Business Area, and (3) the Sensitive Business Area. 

- 1) **DMZ** connects the external internet to the general business area. It features interconnected nodes with minimal defenses, lenient firewall rules, and lower account privileges, making it a potential entry point but less likely to contain sensitive information. 

- 2) **General Business Area** acts as a bridge between the DMZ and the sensitive business area. It includes multiple subnets with enhanced defenses, some sensitive data, and high-level accounts. Connections between subnets are managed by devices like firewalls and routers. 

- 3) **Sensitive Business Area** connects only to the general business area and consists of 1-3 subnets with the strongest defenses and strict access controls. It has fewer nodes but is more likely to contain sensitive information, with connectivity managed similarly to the general business area. 

Backup switches enhance network robustness by demonstrating variability in node connections across different layers and LANs. This setup reflects the network’s inherent randomness and adaptability. 

- **Tree Topology Network** [21]: A classic network architecture where nodes are arranged in layers, typically consisting of a root, branch, and leaf nodes. Each node has a unique data transmission path, simplifying traffic control and management. The failure of a node or link affects only its subtree. Common in broadband networks like Ethernet, the central node is usually a switch or hub, with branches and leaves as workstations or computers. While easy to manage, a central node failure can jeopardize the entire network. 

- **FatTree Topology Network** [96]: This scalable data center network architecture addresses traditional topology limitations, offering improved scale and bandwidth. By employing multiple low-cost units, it builds a large-scale structure ideal for high-performance computing and big data tasks. The FatTree is a _k_ -ary tree with _k_ ports per switch, ( _k/_ 2)<sup>2</sup> core switches, and _k_ pods. Each pod contains two layers: the aggregation layer and the access layer (or edge layer), each with _k/_ 2 switches. Aggregation layer ports connect to core switches and access layer switches. In the access layer, ports connect to the aggregation layer and hosts. This design enhances network performance with scalable bandwidth and hierarchical connectivity. 

We use the topology type as input for the network generator, enabling researchers to easily create diverse network topologies and utilize implicit information within them. 

**Target Asset Modeling.** Our framework models nodes in a network graph using hypothetical and authentic attribute simulations. 

**Simulation of Hypothetical Attributes** : We follow Hammar et al. [20] to assign node attributes, creating networks with hypothetical attributes. Each node is assigned _m_ +1 values: the first _m_ reflect its defensive capabilities, and the last indicates its anomaly detection capability. If a node has a vulnerability in the _i_ -th defense, the _i_ -th attribute value is set to _xi ≤_ 1. 

**Simulation of Authentic Attributes** : Leveraging expert insights, we identify critical attributes for penetration testing, setting unique attributes for each node to simulate authentic target assets: 

- **IP** ( _ip_ ): The IP address of the node. 

- **Node Type** ( _type_ ): Nodes are classified as either switch for data transmission or server for processing and storage. Customizable types are supported. 

- **Local Area Network ID** ( _lan id_ ): Identifies the node’s LAN, reflecting our partitioned network design. Nodes in the same LAN are assumed connected, despite possible internal firewalls. 

- **Operating System** ( _system_ ): Categorized as _windows_ , _linux_ , or _other_ . 

- **Open Ports and Services** ( _port server_ _<u>version</u>_ ): Lists the node’s open ports and associated services, including service versions. Scans may omit this information, par- 

IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 


ticularly versions, so we simulate potential data loss with a predefined probability. 

- **Installed Software and Versions** ( _software_ _<u>version</u>_ ): Details additional software on the node that doesn’t provide external services and their versions, which might have vulnerabilities or sensitive data like passwords, accessible through specific methods. 

- **Saved Account Passwords and Levels** ( _account_ ): Encompasses standard, administrative, and domain administrator accounts. 

- **Vulnerabilities and Vulnerability Exploit Success Rate** ( _cve_ ): Indicates vulnerabilities related to the node’s OS, services, software and weak passwords, alongside the likelihood of successful exploitation. We collected more than 500 vulnerabilities across various systems and services. CVSS scores assess severity based on factors like attack vector and complexity, while EPSS scores, from the latest EPSS v3 model, estimate exploitation likelihood in the wild, with higher scores indicating greater risk. The EPSS score from 2024.10, and CVSS scores are used to determine exploitation success probability. 

For example, the attributes _Xi_ can be set as follows: 


![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0014-07.png)



![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0014-08.png)


To enhance network attribute generation, we incorporate an underlying pattern based on expert knowledge. Nodes within the same LAN often exhibit similarities, particularly concerning operating systems and installed software, such as Windows and Office. This suggests they may share common system and software vulnerabilities, mirroring real-world scenarios where nodes in the same department have similarities. However, due to varying user habits, some vulnerabilities may be addressed through system patches or software updates, and this aspect is also simulated in our network model. Link attributes can be configured based on research needs and decision-making methods. The selection of node and link attributes for intelligent decision-making should align with the specific method and scenario. 

_2) Attacker and Defender Modeling:_ In this section, we model attacker and defender actions by integrating established methods from literature and expert insights. For hypothetical attribute networks, we follow the settings by Hammar et al. [20]. Attackers increment a node’s attack value by 1 in a specific dimension. An attack succeeds when this value 

exceeds the node’s defense value. Defenders can add a defense value of 1 to a node or detect attackers probabilistically. For real attribute networks, we employ a more complex and realistic modeling approach for attackers. 

**Attacker Modeling.** Our attacker modeling is based on the MITRE ATT&CK framework, which outlines 14 tactic and technique phases. Below are the methods applicable at each phase, the necessary execution details, and the results obtained. 

- **Reconnaissance:** Input the target node IP and return its attack surface attributes. Ports and services are paired, and service software versions have a 50% chance of being returned. 

- **Resource Development:** Establish resources like fingerprint vulnerabilities, weak password libraries, and payloads collected before penetration testing. This is a preparatory phase rather than a decision-making stage in intelligent decision processes. During penetration, experts choose suitable resources and tools from what’s available. The thoroughness of this preparation dictates the range of potential actions. 

- **Initial Access:** Achieved via actions such as exploiting vulnerabilities, phishing, cracking weak passwords, and using credentials. 

- **Execution:** Indicates that the attacker has gained initial access to a target network node and is running attackrelated code. This is typically accomplished by exploiting vulnerabilities to subsequently gather system information, sensitive data, and additional node content. 

- **Persistence:** Determine which nodes to maintain access to for ongoing exploitation. 

- **Privilege Escalation:** Decide where to escalate privileges using vulnerabilities, password cracking, or credential login. 

- **Defense Evasion:** Erase traces of actions on a node to reduce detection chances. 

- **Credential Access:** Use credentials such as passwords, cookies, tokens, tickets, and cryptographic elements including hashes, keys, certificates, fingerprints, and biometric data to obtain node access permissions. In modeling, we use the ’Credential Access’ action to encompass these various attack methods. 

- **Discovery:** Internal network reconnaissance by gathering system and network info through techniques like discovery of account, address space, URL, and system, aiding in mapping environments of compromised hosts. 

- **Lateral Movement:** Select a host to move to, decide on the target node and the access method.. 

- **Collection:** Attackers collect valuable information, such as drive types, browsers, audio, video, email, and file contents. In modeling, we use ”Obtain Sensitive Information” action to encompass all techniques at this stage and restrict the information gathered to the internal data of the controlled host, distinguishing it from the externally exposed surface data collected via active scanning during the Renaissance or Discovery phases. 

- **Command and Control:** Remotely control the host to execute commands and operations, potentially leading 


IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 

Table III: Attacker Action Modeling 

|**Action**|**ATT&CK Phase**|**Precondition**|**Decision**<br>**Parameters**|**Expected Outcomes**|**Unexpected**<br>**Outcomes**|**Time**<br>**Cost**|**Network**<br>**Changed**|**Note**|
|---|---|---|---|---|---|---|---|---|
|Scanning|Reconnaissance,<br>Discov-<br>ery|Target IP known|Target IP|Obtain<br>partial<br>information<br>of<br>the target IP,including<br>type,<br>LAN<br>ID,<br>system,<br>and<br>(port,<br>service,<br>version)<br>attributes.||2|No|Version<br>data<br>is<br>often<br>re-<br>turned probabilistically, simu-<br>lating randomness and poten-<br>tial pairing errors. Similarly,<br>exposure surface information<br>is provided in a probabilis-<br>tic manner, mirroring the chal-<br>lenges of incomplete data in<br>real-world scanning tools.|
|Vulnerability<br>Exploitation|Initial Access, Execution,<br>Persistence, Privilege Es-<br>calation,<br>Lateral<br>Move-<br>ment, Command and Con-<br>trol|Target IP known|Target<br>IP,<br>specifc vul-<br>nerability|Obtain<br>control<br>per-<br>missions of the target<br>IP node|If the vulnerabil-<br>ity does not exist,<br>exploitation fails|1|No|Success judged by CVSS and<br>EPSS scores; user-set success<br>probability supported.|
|Persistence|Persistence|Administrative<br>user permissions<br>for target IP|Target IP|Obtain persist session|Persistent session<br>not retrieved|1|No|Node maintains session post-<br>restart.|
|Credential<br>Access|Initial<br>Access,<br>Privilege<br>Escalation, Credential Ac-<br>cess, Lateral Movement|Target IP known|Target IP|Obtain<br>different<br>permissions based on<br>(account,<br>password)<br>level|Login fails if cre-<br>dentials<br>do<br>not<br>match|3|No|Success based on target IP’s<br>credentials in repository.|
|Weak<br>Pass-<br>word Crack-<br>ing|Initial<br>Access,<br>Privilege<br>Escalation, Lateral Move-<br>ment|Target IP known|Target IP|Gain<br>administrative<br>privileges|Login<br>fails<br>if<br>password<br>does not match<br>weak<br>password<br>database|3|No|Success based on weak pass-<br>word vulnerability.|
|Obtain Sen-<br>sitive<br>Infor-<br>mation|Collection, Command and<br>Control, Discovery|Permissions<br>for<br>target IP|Target IP|Obtain all attributes<br>and sensitive informa-<br>tion; add host creden-<br>tials to database||2|No|Support partial information re-<br>turn to demonstrate attacker<br>capabilities.|
|Phishing<br>Email|Privilege Escalation, Lat-<br>eral Movement, Initial Ac-<br>cess|Target IP known|Target IP|Obtain different priv-<br>ileges||2|No|Success judged by target IP<br>node attributes and success<br>rate.|
|Information<br>Leakage|Command<br>and<br>Control,<br>Exfltration, Impact|Sensitive<br>information<br>for target IP|Target IP|Leak sensitive infor-<br>mation||2|No|Based on researcher’s objec-<br>tives.|
|Establish<br>or<br>Disconnect<br>Connection|Command<br>and<br>Control,<br>Lateral Movement|Permissions<br>for<br>target IP|Initial<br>IP,<br>Target IP|Create or disconnect<br>connections||1|Yes||
|Force<br>Host<br>Of-<br>fine/online|Command<br>and<br>Control,<br>Impact|Permissions<br>for<br>target IP|Target IP|Target node goes of-<br>fine or online||1|Yes|Causes network paralysis, af-<br>fecting services.|
|Defense<br>Evasion|Defense Evasion|Permissions<br>for<br>target IP|Target IP|Clean up action traces<br>to reduce discovery<br>probability||2|No||



to information leakage and connection manipulation by exploiting vulnerabilities. 

- **Exfiltration:** Decide on transmitting sensitive information externally after collection. 

- **Impact:** Aim to manipulate, disrupt, or interfere with systems and data. 

Based on our analysis of intelligent decision-making needs, decision content, methods, common attack actions in research, and real-life penetration parameters, we provide a detailed list of attacker actions in Table III. 

**Defender Modeling.** Defender modeling integrates research and practical defense strategies. Network administrators enhance detection and defense by patching vulnerabilities, deploying intrusion detection systems (IDS), and monitoring traffic. They terminate attacker sessions by taking nodes offline, blocking IPs, and clearing login credentials to protect compromised nodes. Detailed actions are in Table IV. 

In real-world scenarios, the network is visible to defenders, but attackers’ actions are concealed. Traditional AutoPT research models defender awareness through detection. Our approach enhances defense capabilities and detection, incorporating proactive measures like IP blacklisting, honeypots, and countermeasures to capture attacker traces. We have also integrated social engineering defense by providing exten- 

sive security education to reduce phishing success rates and strengthen network security. 

In addition to measures shown in Table IV, some implicit defenses can be strengthened by defining communication relationships between nodes. Dynamic target defense and network mimicry can be implemented through adaptive network changes. In zero trust environments, this contemporary approach enhances defense capabilities via continuous and dynamic verification processes. Our framework simulates continuous authentication by regularly updating node credentials, limiting attackers to credential-logging for session persistence. By adjusting inter-node communication and simulating granular access controls, we can effectively model zero trust scenarios. 

Certain attacker and defender actions can passively modify the network architecture and target assets, as shown in Tables III and IV. During modeling, not all actions are essential for a complete penetration phase. It is preferable to select actions relevant to the specific application phase and research method. Simplifying decision parameters enhances the effective use of independent and continuous tactics and techniques. 


IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 

Table IV: Defender Action Modeling 

|Action|Decision Parameters|Expected Outcomes|Time<br>Cost|Network<br>Changed|Note|
|---|---|---|---|---|---|
|Patch Vulnerability|Target IP|Patch a specifc vulnerability|1|Yes|One vulnerability of the target IP is randomly<br>patched at a time. This invalidates sessions estab-<br>lished through that vulnerability, causing the attacker<br>to lose control of the host.|
|Traffc Monitoring|Target IP|Monitor node traffc and invalidate<br>suspicious sessions|2|No|Attackers may cause suspicious traffc changes when<br>using information leakage.|
|Detect Attack|Target IP|If the detected target IP is n=2 time<br>steps behind the attack’s vulnera-<br>bility exploitation, the foothold is<br>invalidated|1|No||
|Proactively Take Host<br>Offine|Target IP|Take a specifc host offine|1|Yes|Target IP will come back online after a fve time<br>steps interval. Upon reconnection, the attacker will<br>lose control of the host, and all established sessions<br>will be terminated.|
|IP Blacklisting|Target IP|Randomly disconnect one connec-<br>tion of the target IP node|1|Yes||
|Clear/Add<br>Active<br>Credentials|Target IP, Clear/Add<br>Active Credentials|Clear/Add active credentials for the<br>target IP|1|Yes||
|Honeypot|Target IP|Confgure the target IP as a honey-<br>pot; an alarm message will trigger<br>upon a successful attacker penetra-<br>tion of the node.|1|No|One of the conditions for penetration failure can<br>be defned as an attacker successfully infltrating a<br>honeypot.|
|Countermeasure|Target IP|Obtain the attacker’s IP and related<br>information|2|No|Upon honeypot infltration, the defender implements<br>countermeasures to pinpoint the attacker’s IP address<br>andrelated information, which can be designed as an<br>ending condition.|
|Network<br>security<br>training|None|Randomly reduce the success rate<br>of attack methods such as phishing<br>emails, weak passwords, and cre-<br>dential login.|10|No|The degree of success rate reduction varies for each<br>node.|



---

## _B. Network Simulation Dataset and Network Generator_ 

> **Section Summary:** We developed a network generator using the AutoPTSim framework, enabling the creation of dynamic and static networks with diverse architectures, attributes, and scales.


We developed a network generator using the AutoPTSim framework, enabling the creation of dynamic and static networks with diverse architectures, attributes, and scales. The open-source code allows researchers to generate custom network data through parameter adjustments, thereby advancing AutoPT research. We offer a pre-generated network simulation dataset, which includes hypothetical numerical attributes, authentic attributes, and their continuous-time counterparts. 

- Static Hypothetical Numerical Attributes Simulation Networks: These are based on numerical simulations with hypothetical attributes, with no active changes in network scenarios. 

- Static Authentic Attributes Simulation Networks: These use authentic attributes without active changes in network scenarios. 

- Dynamic Hypothetical Numerical Simulation Networks: These incorporate hypothetical attributes alongside dynamic scenario alterations. Nodes may be added or modified randomly, affecting connections and attributes according to a specified change proportion, _p_ change. 

- Dynamic Authentic Attribute Simulation Networks: Here, authentic attributes are used with dynamic scenario changes, governed by _p_ change. 

Based on the aforementioned configurations, we include three types of networks with scales of 10, 100, and 1,000 nodes in our dataset. These scales can also be expanded by modifying the scale parameter. For dynamic networks, we produce network graphs at various time points, providing snapshots that represent the network’s evolution. Researchers can switch 

between these snapshots to effectively capture network dynamics. 

**Usage Example.** To construct a simulation scenario with policy automation, authentic attributes, coordinated technical and tactical actions, and a semi-dynamic context, start by using datasets from static authentic attribute networks. Then, select actions from the attacker and defender sets while ensuring they meet preconditions, and incorporate at least one action to induce passive changes in the network structure. 

To advance simulation modeling in policy automation within MDCPM, we integrate publicly available datasets flexibly. We have also released network generator code, enabling researchers to customize network data by adjusting parameters or fine-tuning the generator. AutoPT-Sim addresses the limitations of existing scene modeling methods, which often focus on small to medium-sized networks and lack support for large networks and varied architectures. Current methods fall short in dynamic scene modeling, offering limited flexibility and lacking a unified approach for multidimensional and multilayer simulations. 

---

## V. CONCLUSION 

> **Section Summary:** This paper reviews the literature on AutoPT and introduces an innovative classification framework, MDCPM, for scenario modeling methods.


This paper reviews the literature on AutoPT and introduces an innovative classification framework, MDCPM, for scenario modeling methods. Our framework categorizes existing research distinctly, addressing the limited scope, fragmented scenarios, and lack of unified standards and public datasets in current AutoPT modeling. We propose AutoPT-Sim, a method that emphasizes strategy automation while supporting tactic and technique automation, as well as full-process integration. Our public release includes a network scenario dataset and 

IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 


network generator code, facilitating flexible scenario modeling across all levels and enabling researchers to customize network data by adjusting generator parameters. Our construction method and dataset aim to guide simulation modeling in AutoPT and serve as a standard data benchmark for fair comparisons of intelligent decision-making methods. To our knowledge, this is the first work to analyze and classify simulation modeling in AutoPT, while offering guidance and standard datasets for model construction. 

Ethical considerations are crucial in AutoPT. Our modeling framework, AutoPT-Sim, uses real-world data while abstracting it to protect privacy and excludes actual penetration tools and payloads, ensuring no direct real-world application. Our research focuses on developing penetration strategies without full automation, thereby avoiding potential harm to systems or users. 

In our current modeling framework, we detail the modeling of attacker and defender actions and plan to release the attacker-defender action dataset and state transition functions in a future phase. We will enhance our characterization of attacker capabilities post-intrusion. Recognizing that information gathering significantly depends on the attacker’s expertise, we will examine network visibility disparities between attackers and defenders, as well as defenders’ delayed response times to attacker actions. Another significant challenge in AutoPT is the lack of a unified evaluation method. Current evaluations often emphasize convergence speed and cumulative rewards in specific network settings, with varying reward configurations complicating comparisons. There is no widely accepted set of metrics for assessing the effectiveness of intelligent decision-making. We advocate for future research to develop standardized evaluation metrics to enhance comparison and advance AutoPT methodologies. 

---

## REFERENCES 

- [1] Z. Chen, “Research on internet security situation awareness prediction technology based on improved rbf neural network algorithm,” _Journal of Computational and Cognitive Engineering_ , vol. 1, no. 3, pp. 103–108, 2022. 

- [2] A. Wani, R. S, and R. Khaliq, “Sdn-based intrusion detection system for iot using deep learning classifier (idsiot-sdl),” _CAAI Transactions on Intelligence Technology_ , vol. 6, no. 3, pp. 281–290, 2021. 

- [3] R. Verma, A. Kumari, A. Anand, and V. Yadavalli, “Revisiting shift cipher technique for amplified data security,” _Journal of Computational and Cognitive Engineering_ , vol. 3, no. 1, pp. 8–14, 2024. 

- [4] F. Abu-Dabaseh and E. Alshammari, “Automated penetration testing: An overview,” in _The 4th international conference on natural language computing, Copenhagen, Denmark_ , pp. 121–129, 2018. 

- [5] S. J. Dorchuck, _Goal-Directed Systems Testing: Automated Execution of Intelligently Generated Cyber Attack Plans_ . PhD thesis, Massachusetts Institute of Technology, 2021. 

- [6] A. Applebaum, D. Miller, B. Strom, C. Korban, and R. Wolf, “Intelligent, automated red team emulation,” in 

   - _Proceedings of the 32nd Annual Conference on Computer Security Applications_ , pp. 363–373, 2016. 

- [7] M. C. Ghanem and T. M. Chen, “Reinforcement learning for intelligent penetration testing,” in _2018 second world conference on smart trends in systems, security and sustainability (WorldS4)_ , pp. 185–192, IEEE, 2018. 

- [8] S. Hacks, R. Lagerstr”om,<sup>¨</sup> and D. Ritter, “Towards automated attack simulations of bpmn-based processes,” in _2021 IEEE 25th International Enterprise Distributed Object Computing Conference (EDOC)_ , pp. 182–191, IEEE, 2021. 

- [9] A. Applebaum, D. Miller, B. Strom, H. Foster, and C. Thomas, “Analysis of automated adversary emulation techniques,” in _Proceedings of the summer simulation multi-conference_ , pp. 1–12, 2017. 

- [10] Z. Yichao, Z. Tianyang, G. Xiaoyue, and W. Qingxian, “An improved attack path discovery algorithm through compact graph planning,” _IEEE Access_ , vol. 7, pp. 59346–59356, 2019. 

- [11] J. L. Obes, C. Sarraute, and G. Richarte, “Attack planning in the real world,” _arXiv preprint arXiv:1306.4044_ , 2013. 

- [12] Z. Hu, R. Beuran, and Y. Tan, “Automated penetration testing using deep reinforcement learning,” in _2020 IEEE European Symposium on Security and Privacy Workshops (EuroS&PW)_ , pp. 2–10, IEEE, 2020. 

- [13] A. Chowdhary, D. Huang, J. S. Mahendran, D. Romo, Y. Deng, and A. Sabur, “Autonomous security analysis and penetration testing,” in _2020 16th International Conference on Mobility, Sensing and Networking (MSN)_ , pp. 508–515, IEEE, 2020. 

- [14] S. G. Bianou and R. G. Batogna, “Pentest-ai, an llmpowered multi-agents framework for penetration testing automation leveraging mitre attack,” in _2024 IEEE International Conference on Cyber Security and Resilience (CSR)_ , pp. 763–770, IEEE, 2024. 

- [15] G. Deng, Y. Liu, V. Mayoral-Vilches, P. Liu, Y. Li, Y. Xu, T. Zhang, Y. Liu, M. Pinzger, and S. Rass, “Pentestgpt: Evaluating and harnessing large language models for automated penetration testing,” in _33rd USENIX Security Symposium (USENIX Security 24)_ , pp. 847–864, 2024. 

- [16] k. Chen, H. Lu, B. Fang, Y. Sun, s. Su, and Z. Tian, “Survey on automated penetration testing technology research,” _Journal of Software_ , pp. 1–21, 2023. 

- [17] ErikMiehling, MohammadRasouli, DemosthenisTeneketzis, ErikMiehling, MohammadRasouli, DemosthenisTeneketzis, ErikMiehling, MohammadRasouli, DemosthenisTeneketzis, and E. and, “Control-theoretic approaches to cyber-security,” 2019. 

- [18] A. Furfaro, L. Argento, A. Parise, and A. Piccolo, “Using virtual environments for the assessment of cybersecurity issues in iot scenarios,” _Simulation Modelling Practice and Theory_ , vol. 73, pp. 43–54, 2017. 

- [19] D. Miller, R. Alford, A. Applebaum, H. Foster, C. Little, and B. Strom, “Automated adversary emulation: A case for planning and acting with unknowns,” _MITRE CORP MCLEAN VA MCLEAN_ , 2018. 

- [20] K. Hammar and R. Stadler, “Finding effective security strategies through reinforcement learning and self-play,” 

IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 


2020. 

- [21] M. Brede, “Networks—an introduction. mark e. j. newman. (2010, oxford university press.) $65.38, £35.96 (hardcover), 772 pages. isbn-978-0-19-920665-0.,” _Artificial Life_ , vol. 18, pp. 241–242, 2012. 

- [22] L. Guo, Y. Cao, M. Su, Y. Shang, Y. Zhu, P. Zhang, and C. Zhou, “Cyberspace resource mapping: Concepts and techniques,” _Journal of Information Security_ , vol. 3, no. 4, p. 14, 2018. 

- [23] W. U. Jiangxing, “Research on cyber mimic defense,” _Journal of Cyber Security_ , 2016. 

- [24] S. Jajodia, A. K. Ghosh, V. Swarup, C. Wang, and X. S. Wang, _Moving Target Defense: Creating Asymmetric Uncertainty for Cyber Threats_ . Moving Target Defense: Creating Asymmetric Uncertainty for Cyber Threats, 2011. 

- [25] E. M. Hutchins, M. J. Cloppert, R. M. Amin, _et al._ , “Intelligence-driven computer network defense informed by analysis of adversary campaigns and intrusion kill chains,” _Leading Issues in Information Warfare & Security Research_ , vol. 1, no. 1, p. 80, 2011. 

- [26] B. E. Strom, A. Applebaum, D. Miller, K. C. Nickels, A. G. Pennington, and C. Thomas, “Mitre att&ck : Design and philosophy,” 2018. 

- [27] P. Midian, “Perspectives on penetration testing — black box vs. white box.,” _Network Security_ , p. 10, 2002. 

- [28] H. M. Z. Al Shebli and B. D. Beheshti, “A study on penetration testing process and tools,” in _2018 IEEE Long Island Systems, Applications and Technology Conference (LISAT)_ , pp. 1–7, IEEE, 2018. 

- [29] E. Filiol, F. Mercaldo, and A. Santone, “A method for automatic penetration testing and mitigation: A red hat approach,” _Procedia Computer Science_ , vol. 192, pp. 2039–2046, 2021. 

- [30] K. Shravan, B. Neha, and B. Pawan, “Penetration testing: A review,” _Compusoft_ , vol. 3, no. 4, p. 752, 2014. 

- [31] J. N. Goel and B. M. Mehtre, “Vulnerability assessment & penetration testing as a cyber defence technology,” _Procedia Computer Science_ , vol. 57, pp. 710–715, 2015. 

- [32] J. DeMott, R. Enbody, and W. F. Punch, “Revolutionizing the field of grey-box attack surface testing with evolutionary fuzzing,” _BlackHat and Defcon_ , 2007. 

- [33] N. F. Awang and A. A. Manaf, “Detecting vulnerabilities in web applications using automated black box and manual penetration testing,” in _International Conference on Security of Information and Communication Networks_ , pp. 230–239, Springer, 2013. 

- [34] F. Terranova, A. Lahmadi, and I. Chrisment, “Leveraging deep reinforcement learning for cyber-attack paths prediction: Formulation, generalization, and evaluation,” in _The 27th International Symposium on Research in Attacks, Intrusions and Defenses (RAID 2024)_ , 2024. 

- [35] M. C. Ghanem, _Towards an efficient automation of network penetration testing using model-based reinforcement learning_ . PhD thesis, City, University of London, 2022. 

- [36] R. Dillon _et al._ , ““perihack”: Designing a serious game for cybersecurity awareness,” in _2022 IEEE International_ 

_Conference on Teaching, Assessment and Learning for Engineering (TALE)_ , pp. 630–634, IEEE, 2022. 

- [37] J. Schwartz and H. Kurniawati, “Autonomous penetration testing using reinforcement learning,” _arXiv preprint arXiv:1905.05965_ , 2019. 

- [38] S. Paul, Z. Ni, and C. Mu, “A learning-based solution for an adversarial repeated game in cyber–physical power systems,” _IEEE Transactions on Neural Networks and Learning Systems_ , vol. 31, no. 11, pp. 4512–4523, 2019. 

- [39] R. Elderman, L. J. Pater, A. S. Thie, M. M. Drugan, and M. A. Wiering, “Adversarial reinforcement learning in a cyber security simulation,” in _9th International Conference on Agents and Artificial Intelligence (ICAART 2017)_ , pp. 559–566, SciTePress Digital Library, 2017. 

- [40] G. F. Lyon, _Nmap network scanning: The official Nmap project guide to network discovery and security scanning_ . Insecure, 2009. 

- [41] 2020. https://github.com/shadow1ng/fscan/blob/main/ README EN.md. 

- [42] X. Long, Y. Fang, C. Huang, and L. Liu, “Webshell research overview: The game between detection and evasion,” _Cyberspace Security_ , vol. 9, no. 1, pp. 62–68, 2018. 

- [43] S. Y. Enoch, Z. Huang, C. Y. Moon, D. Lee, M. K. Ahn, and D. S. Kim, “Harmer: Cyber-attacks automation and evaluation,” _IEEE Access_ , vol. 8, pp. 129397–129414, 2020. 

- [44] J. Schwartz, H. Kurniawati, and E. El-Mahassni, “Pomdp+ information-decay: Incorporating defender’s behaviour in autonomous penetration testing,” in _Proceedings of the International Conference on Automated Planning and Scheduling_ , vol. 30, pp. 235–243, 2020. 

- [45] N. Becker, D. Reti, E. V. Ntagiou, M. Wallum, and H. D. Schotten, “Evaluation of reinforcement learning for autonomous penetration testing using a3c, q-learning and dqn,” _arXiv preprint arXiv:2407.15656_ , 2024. 

- [46] S. Zhou, J. Liu, D. Hou, X. Zhong, and Y. Zhang, “Autonomous penetration testing based on improved deep q-network,” _Applied Sciences_ , vol. 11, no. 19, p. 8823, 2021. 

- [47] C. Sarraute, “Automated attack planning,” _arXiv preprint arXiv:1307.7808_ , 2013. 

- [48] J. Xu, J. W. Stokes, G. McDonald, X. Bai, D. Marshall, S. Wang, A. Swaminathan, and Z. Li, “Autoattacker: A large language model guided system to implement automatic cyber-attacks,” _arXiv preprint arXiv:2403.01038_ , 2024. 

- [49] W. Blum, “Gamifying machine learning for stronger security and ai models,” _Microsoft Res., Redmond, WA, USA_ , 2021. 

- [50] C. Sarraute, O. Buffet, and J. Hoffmann, “Penetration testing== pomdp solving?,” _arXiv preprint arXiv:1306.4714_ , 2013. 

- [51] Tenable, “Nessus vulnerability scanner: Network security solution.” https://www.tenable.com/products/nessus, 2024. Accessed: 2024-10-04. 

- 

- [52] Rapid7, “Metasploit penetration testing software, pen testing security.” https://www.metasploit.com/, 2024. Ac- 

IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 


cessed: 2024-10-04. 

- [53] Y. Li, H. Dai, and J. Yan, “Knowledge-informed autopenetration testing based on reinforcement learning with reward machine,” _arXiv preprint arXiv:2405.15908_ , 2024. 

- [54] Y. Zhang, J. Liu, S. Zhou, D. Hou, X. Zhong, and C. Lu, “Improved deep recurrent q-network of pomdps for automated penetration testing,” _Applied Sciences_ , vol. 12, no. 20, p. 10339, 2022. 

- [55] X. Guo, J. Ren, J. Zheng, J. Liao, C. Sun, H. Zhu, T. Song, S. Wang, and W. Wang, “Automated penetration testing with fine-grained control through deep reinforcement learning,” _Journal of Communications and Information Networks_ , vol. 8, no. 3, pp. 212–220, 2023. 

- [56] R. E. Haeni, “Firewall penetration testing,” tech. rep., Technical report, The George Washington University Cyberspace Policy ..., 1997. 

- [57] “Nmap: the network mapper - free security scanner.” https://nmap.org/. Accessed: 2024-12-16. 

- [58] J. P. McDermott, “Attack net penetration testing,” in _Proceedings of the 2000 workshop on New security paradigms_ , pp. 15–21, 2001. 

- [59] B. Skaggs, B. Blackburn, G. Manes, and S. Shenoi, “Network vulnerability analysis,” in _The 2002 45th Midwest Symposium on Circuits and Systems, 2002. MWSCAS2002._ , vol. 3, pp. III–493, IEEE, 2002. 

- [60] P. Liu, “A game theoretic approach to cyber attack prediction,” tech. rep., Pennsylvania State Univ., University Park, PA (United States), 2005. 

- [61] Y. Kosuga, K. Kono, M. Hanaoka, M. Hishiyama, and Y. Takahama, “Sania: Syntactic and semantic analysis for automated testing against sql injection,” in _Twentythird annual computer security applications conference (ACSAC 2007)_ , pp. 107–117, IEEE, 2007. 

- [62] J. Fonseca, M. Vieira, and H. Madeira, “Testing and comparing web vulnerability scanning tools for sql injection and xss attacks,” in _13th Pacific Rim international symposium on dependable computing (PRDC 2007)_ , pp. 365– 372, IEEE, 2007. 

- [63] D. Shen, G. Chen, L. Haynes, and E. Blasch, “Strategies comparison for game theoretic cyber situational awareness and impact assessment,” in _2007 10th International Conference on Information Fusion_ , pp. 1–8, IEEE, 2007. 

- [64] B. D. Cone, C. E. Irvine, M. F. Thompson, and T. D. Nguyen, “A video game for cyber security training and awareness,” _computers & security_ , vol. 26, no. 1, pp. 63– 72, 2007. 

- [65] L. Greenwald and R. Shanley, “Automated planning for remote penetration testing,” in _MILCOM 2009-2009 IEEE Military Communications Conference_ , pp. 1–7, IEEE, 2009. 

- [66] C. Sarraute, G. Richarte, and J. Luc´angeli Obes, “An algorithm to find optimal attack paths in nondeterministic scenarios,” in _Proceedings of the 4th ACM workshop on Security and artificial intelligence_ , pp. 71–80, 2011. 

- [67] M. Van Dijk, A. Juels, A. Oprea, and R. L. Rivest, “Flipit: The game of “stealthy takeover”,” _Journal of Cryptology_ , vol. 26, pp. 655–713, 2013. 

- [68] M. Chapman, G. Tyson, P. McBurney, M. Luck, and S. Parsons, “Playing hide-and-seek: an abstract game for cyber security,” in _Proceedings of the 1st International Workshop on Agents and CyberSecurity_ , pp. 1–8, 2014. 

- [69] Chapman and M. David, “Cyber hide-and-seek,” 2016. 

- [70] M. Ficco, M. Chora´s, and R. Kozik, “Simulation platform for cyber-security and vulnerability analysis of critical infrastructures,” _Journal of computational science_ , vol. 22, pp. 179–186, 2017. 

- [71] V. Casola, A. De Benedictis, M. Rak, and U. Villano, “Towards automated penetration testing for cloud applications,” in _2018 IEEE 27th International Conference on Enabling Technologies: Infrastructure for Collaborative Enterprises (WETICE)_ , pp. 24–29, IEEE, 2018. 

- [72] M. C. Ghanem and T. M. Chen, “Reinforcement learning for efficient network penetration testing,” _Information_ , vol. 11, no. 1, p. 6, 2019. 

- [73] S. Paul and Z. Ni, “A strategic analysis of attackerdefender repeated game in smart grid security,” in _2019 IEEE Power & Energy Society Innovative Smart Grid Technologies Conference (ISGT)_ , pp. 1–5, IEEE, 2019. 

- [74] T. Y. Zhou, Y. C. Zang, J. H. Zhu, and Q. X. Wang, “Nig-ap: a new method for automated penetration testing,” _Frontiers of Information Technology & Electronic Engineering_ , vol. 20, no. 9, pp. 1277–1288, 2019. 

- [75] O. Valea and C. Opris¸a, “Towards pentesting automation using the metasploit framework,” in _2020 IEEE 16th International Conference on Intelligent Computer Communication and Processing (ICCP)_ , pp. 171–178, IEEE, 2020. 

- [76] A. Bhattacharya, T. Ramachandran, S. Banik, C. P. Dowling, and S. D. Bopardikar, “Automated adversary emulation for cyber-physical systems via reinforcement learning,” in _2020 IEEE International Conference on Intelligence and Security Informatics (ISI)_ , pp. 1–6, IEEE, 2020. 

- [77] H. V. Nguyen, H. N. Nguyen, and T. Uehara, “Multiple level action embedding for penetration testing,” in _Proceedings of the 4th International Conference on Future Networks and Distributed Systems_ , pp. 1–9, 2020. 

- [78] G. Costa and A. Valenza, “Why charles can pen-test: an evolutionary approach to vulnerability testing,” _arXiv preprint arXiv:2011.13213_ , 2020. 

- [79] J. A. Bland, M. D. Petty, T. S. Whitaker, K. P. Maxwell, and W. A. Cantrell, “Machine learning cyberattack and defense strategies,” _Computers & security_ , vol. 92, p. 101738, 2020. 

- [80] T. Hu, T. Zhou, Y. Zang, Q. Wang, and H. Li, “Apud* lite: Attack planning under uncertainty based on d* lite,” _CMC-COMPUTERS MATERIALS & CONTINUA_ , vol. 65, no. 2, pp. 1795–1807, 2020. 

- [81] K. Qian, D. Zhang, P. Zhang, Z. Zhou, X. Chen, and S. Duan, “Ontology and reinforcement learning based intelligent agent automatic penetration test,” in _2021 IEEE International Conference on Artificial Intelligence and Computer Applications (ICAICA)_ , pp. 556–561, IEEE, 2021. 

- [82] L. Erd˝odi, A.<sup>˚</sup> A.<sup>˚</sup> Sommervoll, and F. M. Zennaro, “Sim- 

IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 


ulating sql injection vulnerability exploitation using q- learning reinforcement learning agents,” _Journal of Information Security and Applications_ , vol. 61, p. 102903, 2021. 

   - [96] M. Al-Fares, A. Loukissas, and A. Vahdat, “A scalable, commodity data center network architecture,” _ACM SIGCOMM computer communication review_ , vol. 38, no. 4, pp. 63–74, 2008. 

- [83] X.-P. Ji, W. Tian, W. Liu, and G. Liu, “Optimal attack strategy selection of an autonomous cyber-physical micro-grid based on attack-defense game model,” _Journal of Ambient Intelligence and Humanized Computing_ , vol. 12, pp. 8859–8866, 2021. 

- [84] M. M. Yamin and B. Katt, “Use of cyber attack and defense agents in cyber ranges: A case study,” _Computers & Security_ , vol. 122, p. 102892, 2022. 

- [85] A. Confido, E. V. Ntagiou, and M. Wallum, “Reinforcing penetration testing using ai,” in _2022 IEEE Aerospace Conference (AERO)_ , pp. 1–15, IEEE, 2022. 

- [86] K. Tran, M. Standen, J. Kim, D. Bowman, T. Richer, A. Akella, and C.-T. Lin, “Cascaded reinforcement learning agents for large action spaces in autonomous penetration testing,” _Applied Sciences_ , vol. 12, no. 21, p. 11265, 2022. 

- [87] J. Hance, J. Milbrath, N. Ross, and J. Straub, “Distributed attack deployment capability for modern automated penetration testing,” _Computers_ , vol. 11, no. 3, p. 33, 2022. 

- [88] F. L. Færøy, M. M. Yamin, A. Shukla, and B. Katt, “Automatic verification and execution of cyber attack on iot devices,” _Sensors_ , vol. 23, no. 2, p. 733, 2023. 

- [89] Q. Li, M. Hu, H. Hao, M. Zhang, and Y. Li, “Innes: An intelligent network penetration testing model based on deep reinforcement learning,” _Applied Intelligence_ , vol. 53, no. 22, pp. 27110–27127, 2023. 


![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0020-11.png)



![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0020-12.png)


**Yunfei Wang** received the B.S. degree in civil engineering from the Hunan University, Changsha, China, in 2020. She is now pursuing the Ph.D degree at the National University of Defense Technology, Changsha, China. She is also a visiting scholar at Tsinghua University. Her research interests include auto penetration test, reinforcement learning and cyber-security. 

**Shixuan Liu** received his B.S. and Ph.D. degrees from the National University of Defense Technology, Changsha, China, in 2019 and 2024, respectively. He is also a visiting scholar in the Department of Computer Science and Technology at Tsinghua University, where he has spent two years. He has published over 10 papers in prestigious journals and conferences, including T-PAMI, T-KDE, T-CYB, and ICDM, focusing on knowledge reasoning and data mining. 

- [90] I. Alshehri, A. Alshehri, A. Almalki, M. Bamardouf, and A. Akbar, “Breachseek: A multi-agent automated penetration tester,” _arXiv preprint arXiv:2409.03789_ , 2024. 

- [91] Z. Wang, S. Li, L. Zhang, C. Hu, and L. Yan, “A red team automated testing modeling and online planning method for post-penetration,” _Computers & Security_ , p. 103945, 2024. 

- [92] Q. Li, R. Wang, D. Li, F. Shi, M. Zhang, and A. Chattopadhyay, “Dynpen: Automated penetration testing in dynamic network scenarios using deep reinforcement learning,” _IEEE Transactions on Information Forensics and Security_ , 2024. 

- [93] Y. Wang, S. Liu, W. Wang, C. Zhu, C. Fan, K. Huang, and C. Chen, “Pentraformer: Learning agents for automated penetration testing via sequence modeling,” in _2024 IEEE International Conferences on Internet of Things (iThings) and IEEE Green Computing & Communications (GreenCom) and IEEE Cyber, Physical & Social Computing (CPSCom) and IEEE Smart Data (SmartData) and IEEE Congress on Cybermatics_ , pp. 551–558, IEEE, 2024. 

- [94] Y. Wang, S. Liu, C. Zhang, W. Wang, J. Jin, C. Zhu, and C. Zhou, “Graph pre-training for reconnaissance perception in automated penetration testing,” in _International Conference on Intelligent Computing_ , 2024. 

- [95] C. Sarraute, O. Buffet, and J. Hoffmann, “Pomdps make better hackers: Accounting for uncertainty in penetration testing,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 26, pp. 1816–1824, 2012. 


![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0020-21.png)



![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0020-22.png)


**Wenhao Wang** received the Ph.D. degrees from the National University of Defense Technology, Changsha, China. He is now a lecturer at the National University of Defense Technology. His research interests include auto penetration test, reinforcement learning and cyber-security. 

**Changling Zhou** received the B.S., M.S. and Ph.D. degrees from Peking University. He is a Professor with Peking University. His research interest include cyber-security, auto penetration test and LLM. 

IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY 



![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0021-02.png)



![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0021-03.png)


**Chao Zhang** (Member, IEEE) received the B.S. and Ph.D. degrees from Peking University. He did Postdoctoral Research at UC Berkeley. He is an Associate Professor at Tsinghua University. His research interest lie in software and system security, including AI for security and security for AI. 

**Jiandong Jin** received the M.S. and Ph.D. degrees from Peking University. He is an engineer in the Computer Center from Peking University. His research interest include system security, including AI for security and security for AI. 


![](images/20-a-unified-modeling-framework-for-automated-penetration.pdf-0021-06.png)


**Cheng Zhu** received the Ph.D. degree in management science and engineering from the National University of Defense Technology, China, in 2005. He is currently a Professor with the National Key Laboratory of Information Systems Engineering, National University of Defense Technology. His current research interest is computer network data mining, command and control, and cyber security. 

