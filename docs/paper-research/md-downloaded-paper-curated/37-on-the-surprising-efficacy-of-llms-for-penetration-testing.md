# **On the Surprising Efficacy of LLMs for Penetration-Testing** 

## Table of Contents

- [ABSTRACT](#abstract)
- [CCS CONCEPTS](#ccs-concepts)
- [KEYWORDS](#keywords)
- [1 INTRODUCTION](#1-introduction)
- [2 BACKGROUND](#2-background)
- [2.1 Penetration-Testing](#2-1-penetration-testing)
- [2.2 Pre-LLM Usage of AI for Offensive Security](#2-2-pre-llm-usage-of-ai-for-offensive-security)
- [2.3 Evolution of LLMs](#2-3-evolution-of-llms)
- [3 A SHORT HISTORY OF USING LLMS FOR PENETRATION-TESTING](#3-a-short-history-of-using-llms-for-penetration-testing)
- [3.1 Academic Research](#3-1-academic-research)
- [3.2 Industry Adoption](#3-2-industry-adoption)
- [4 ON THE SURPRISING EFFICACY OF LLMS FOR PENETRATION-TESTING](#4-on-the-surprising-efficacy-of-llms-for-penetration-testing)
- [4.1 Penetration-Testing Resembles Pattern-Matching](#4-1-penetration-testing-resembles-pattern-matching)
- [4.2 LLMs Inherently Cope With Uncertainty](#4-2-llms-inherently-cope-with-uncertainty)
- [4.3 The Costs of Using LLMs](#4-3-the-costs-of-using-llms)
- [4.4 Additional Beneficial Capabilities](#4-4-additional-beneficial-capabilities)
- [5.2 Towards Autonomous Hacking](#5-2-towards-autonomous-hacking)
- [6 OBSTACLES TO OVERCOME](#6-obstacles-to-overcome)
- [5 STATUS-QUO: VIBE-HACKING AND AUTONOMOUS AGENTS](#5-status-quo-vibe-hacking-and-autonomous-agents)
- [5.1 Vibe-Hacking](#5-1-vibe-hacking)
- [6.1 Model Features and Stability](#6-1-model-features-and-stability)
- [6.2 Safety and Security Concerns](#6-2-safety-and-security-concerns)
- [6.3 Costs and Efficiency Concerns](#6-3-costs-and-efficiency-concerns)
- [6.4 Privacy and Digital Sovereignty Concerns](#6-4-privacy-and-digital-sovereignty-concerns)
- [6.5 Accountability Concerns](#6-5-accountability-concerns)
- [6.6 Capability vs. Reliability](#6-6-capability-vs-reliability)
- [6.7 Concerns About Ethics](#6-7-concerns-about-ethics)
- [7 THE WAY FORWARD?](#7-the-way-forward)
- [7.1 Costs and Features](#7-1-costs-and-features)
- [7.2 The Need for Better Safeguards](#7-2-the-need-for-better-safeguards)
- [7.3 Capabilities and Reliability](#7-3-capabilities-and-reliability)
- [7.4 Decision Time for Individuals and Society](#7-4-decision-time-for-individuals-and-society)
- [8 CONCLUSION](#8-conclusion)
- [REFERENCES](#references)

---

Andreas Happe andreas.happe@tuwien.ac.at TU Wien Vienna, Austria 

## **ABSTRACT** 

> **Section Summary:** This paper presents a critical examination of the surprising efficacy of Large Language Models (LLMs) in penetration testing.


This paper presents a critical examination of the surprising efficacy of Large Language Models (LLMs) in penetration testing. The paper thoroughly reviews the evolution of LLMs and their rapidly expanding capabilities which render them increasingly suitable for complex penetration testing operations. It systematically details the historical adoption of LLMs in both academic research and industry, showcasing their application across various offensive security tasks and covering broader phases of the cyber kill chain. Crucially, the analysis also extends to the observed adoption of LLMs by malicious actors, underscoring the inherent dual-use challenge of this technology within the security landscape. 

The unexpected effectiveness of LLMs in this context is elucidated by several key factors: the strong alignment between penetration testing’s reliance on pattern-matching and LLMs’ core strengths, their inherent capacity to manage uncertainty in dynamic environments, and cost-effective access to competent pre-trained models through LLM providers. 

The current landscape of LLM-aided penetration testing is categorized into interactive ’vibe-hacking’ and the emergence of fully autonomous systems. The paper identifies and discusses significant obstacles impeding wider adoption and safe deployment. These include critical issues concerning model reliability and stability, paramount safety and security concerns, substantial monetary and ecological costs, implications for privacy and digital sovereignty, complex questions of accountability, and profound ethical dilemmas. This comprehensive review and analysis provides a foundation for discussion on future research directions and the development of robust safeguards at the intersection of AI and security. 

---

## **CCS CONCEPTS** 

> **Section Summary:** • **Security and privacy** → **Systems security** ; **Network security** ;


• **Security and privacy** → **Systems security** ; **Network security** ; 

- **Computing methodologies** → **Artificial intelligence** . 

---

## **KEYWORDS** 

> **Section Summary:** Penetration-Testing, Security Testing, Large Language Models, LLM, Offensive Security


Penetration-Testing, Security Testing, Large Language Models, LLM, Offensive Security 

---

## **1 INTRODUCTION** 

> **Section Summary:** Upholding an organization’s IT security has been problematic since the rise of enterprise networks in the early 2000s.


Upholding an organization’s IT security has been problematic since the rise of enterprise networks in the early 2000s. One of the most publicly visible type of security incidents are ransomware attacks. Current estimates indicate that 72% of business were affected by ransomware between 2018–2023 [81]. Related losses are estimated to reach $57 billion for 2025 or $6.5 million per hour [73]. The trend indicates a worsening of this situation with estimates of ransomware incidents happening every 2 seconds in 2031, up from 11 seconds in 2021 [73]. 

Jürgen Cito juergen.cito@tuwien.ac.at TU Wien Vienna, Austria 

A common way of preventing security incidents is to test one’s own defenses through penetration-testing. The capability of performing sufficient penetration-testing is severely limited by the amount of available offensive personnel, i.e. ISC2 estimates that currently 4.7 million cybersecurity experts are missing from the workforce. The year-over-year change indicates that this gap is still increasing, e.g., by 19.1% [46] in 2025, this indicates a massive need to make existing security penetration-testers more effective, or even to automate time-consuming parts of penetration-testing, reducing the need for manual work by human specialists. As will be shown in Section 3, Large Language Models (LLMs) have been increasingly investigated by both industry and academia to fulfill this need. 

In this paper, we reflect on the first two years (2023–2025) of LLM-aided penetration-testing. We use the Background Section (Section 2) to create a common understanding of penetration-testing and highlight important milestones within the evolution of LLMs. In Section 3, we give a short history of how LLMs were used for penetration-testing, separated into academic research and adoption by industry. After we have shown their clear and present interest in LLMs, we discuss why LLMs are a good fit for penetration-testing and summarize the current status-quo (Sections 4 and 5). Subsequently, we highlight obstacles that prevent further adoption of LLMs before we conclude with a final section highlighting potential remediation means, also known as research opportunities, for the mentioned obstacles. 

---

## **2 BACKGROUND** 

> **Section Summary:** We introduce penetration-testing, show how pre-LLM AI systems were used by adversaries, and conclude with a high-level overview of the evolution of LLMs.


We introduce penetration-testing, show how pre-LLM AI systems were used by adversaries, and conclude with a high-level overview of the evolution of LLMs. 

---

## **2.1 Penetration-Testing** 

> **Section Summary:** During penetration-testing highly-skilled professionals try to break systems to uncover vulnerabilities so that those can be mitigated by defensive personnel before malicious actors can exploit them.


During penetration-testing highly-skilled professionals try to break systems to uncover vulnerabilities so that those can be mitigated by defensive personnel before malicious actors can exploit them. We focus on the practitioners’ daily work [34], not on security researchers that seek to find new vulnerabilities and attack vectors that practitioners will subsequently exploit. 

Enterprise networks are typically comprised of Microsoft Active Directory, with industry studies indicating that over 90% of Global Fortune 1000 companies are using it as their primary means of authenticating and authorizing users [55]. Having this common technology stack, or mono-culture, for enterprise network architectures allows penetration-testers to apply knowledge learned during prior penetration-tests to new assignments by matching common problems and insecure configurations. Practitioners also describe that they can apply knowledge learned during educational attacking of simulated systems (CTFs) to real-world systems [34], further 

Andreas Happe and Jürgen Cito 

enforcing the idea that **penetration-testing is often based on pattern-matching** . 

---

## **2.2 Pre-LLM Usage of AI for Offensive Security** 

> **Section Summary:** Interest into applying machine-learning techniques to offensive security tasks precedes the rise of LLMs.


Interest into applying machine-learning techniques to offensive security tasks precedes the rise of LLMs. Mirsky et al. [72] performed a literature review and surveyed experts from academia, industry, and government on the potential threat of offensive AI to organizations. The initial version of the paper was released to arXiv in July 2021, a revised version was published in January 2023. As ChatGPT went public in late November 2022, this publication describes the state-of-the-art pre-LLM. 

The authors identify 33 AI offensive capabilities and group them into _Automation_ , _Campaign Resilience_ , _Credential Theft_ , _Exploit Development_ , _Information Gathering_ , and _Stealth_ . Of these categories, the top 3 identified capabilities were _Exploit Development_ , _Social Engineering_ , and _Information Gathering_ . Their survey indicated that, overall, academia and industry felt that impersonation (and thus social engineering) was the biggest threat, mirroring another user study of professional penetration-testers [34] that highlighted the potential of machine-learning for phishing, a subtask of social engineering. 

They conclude that offensive AI primarily impacts the initial steps of the cyber kill chain, focusing on reconnaissance, resource development, and initial access as “ **AI technologies are not mature enough to create agents able to carry on attacks that proceed without human supervision and aid** ”. In 2021, their outlook on the near future was that “ **we aren’t likely to see botnets that can autonomously and dynamically interact with a diverse set of complex systems (like an organization’s network) in the near future** ”. 

We will show in this paper that the rise of LLMs has accelerated the adoption of machine-learning for offensive security and has fulfilled some of the paper’s predictions. While we focus upon penetration-testing (roughly comprising the _automation_ and _campaign resilience_ categories of their study), our section on malicious industrial use of LLMs (Section 3.2.2) will show that their predictions about social engineering, exploit development, and information gathering became reality. Furthermore, while not employed by industry yet, LLMs enabled academic prototypes (Section 3.1) to cover more phases of the cyber kill chain, including privilege escalation and lateral movement. Dwelling deeper on their list of identified offensive AI capabilities, we see the following _Automation_ capabilities well-covered by research: _Attack Adaption_ , _Attack Coordination_ , _Next Hop Targeting_ , _Point of Entry Detection_ . Of _Campaign Resilience_ ’s capabilities, we see _Campaign Planning_ covered; of the other techniques some are implicitly covered by the prototypes highlighted in Section 3.1, e.g., _Virtualization Detection_ and _Password Guessing_ . 

---

## **2.3 Evolution of LLMs** 

> **Section Summary:** In November 2022, OpenAI made ChatGPT publicly available [78] and thus sparkled public interest into LLMs.


In November 2022, OpenAI made ChatGPT publicly available [78] and thus sparkled public interest into LLMs. Their API allowed integration of LLMs into existing tools and workflows. 

Over time, LLMs gained advanced capabilities [50] such as _toolcalling_ or _structured-output_ . The former allows LLMs to call usersupplied functions, typically used to interact with their environment. Structured output allows easier integration of LLM’s output into the caller’s system. Both of them have lead to _agentic AI_ , systems in which agents issue commands to interact with their environment to solve their given tasks, often autonomously. _Retrieval Augmented Generation_ (RAG) and using the ever-increasing LLM context size for _In-Context Learning_ allowed LLMs to integrate additional background knowledge [59] without having to expensively retrain models. It became feasible to operate smaller models on commodity hardware on-edge [97]. Prompt-Engineering used techniques such as _Chain-of-Thought_ [103] (CoT) to improve the efficacy of LLMs in complex tasks. 

Another big step forward was the introduction of reasoning LLMs, e.g., by OpenAI introducing the o1 model in 2024 [79]. Reasoning models are pre-trained to incorporate CoT during inference, reducing the dependence on prior prompt-engineering techniques for solving complex tasks. Recent contested research [82, 90] indicates that reasoning models do not perform reasoning similar to humans, but that LLMs are “merely” **getting even better at pattern-matching** than they were before. Concurrent research indicates that reasoning LLMs can introduce problems with _toolcalling_ and _instruction-following_ [61]. 

Latest advancements further improve the ability of LLMs to interact with their environment or with each other. The _Model Context Protocol_ (MCP), originally proposed by Anthropic in 2024 [4], standardized integration of tools into LLMs, leading to an explosion of available tool-integrations. Recent interest into _Multi-Agent Systems_ , e.g. Google’s A2A [93], uses multiple collaborating LLMs to solve complex tasks [51]. 

---

## **3 A SHORT HISTORY OF USING LLMS FOR PENETRATION-TESTING** 

> **Section Summary:** Give the rapid evolution for LLMs, we want to highlight their impact on security with a focus on penetration-testing.


Give the rapid evolution for LLMs, we want to highlight their impact on security with a focus on penetration-testing. We differentiate between academic research and industry adoption. 

For academic research, we used Google Scholar to identify survey papers on offensive use of LLMs [7, 20, 39, 48, 69, 74, 87, 107, 113– 115]. We included papers from these surveys if they were using LLMs to perform penetration-testing, and analyzed them in chronological order for their novelty. The analysis of industrial use of LLMs is based on articles posted on security-specific news-sites<sup>1</sup> mentioning the use of LLMs, as well as on abuse reports provided by LLM providers. 

---

## **3.1 Academic Research** 

> **Section Summary:** We group academic research based on the initial publication year of the respective publication, typically using the date of their initial upload to arXiv.


We group academic research based on the initial publication year of the respective publication, typically using the date of their initial upload to arXiv. 

_3.1.1 Initial Forays (2023)._ Given our described methodology, the first paper that used LLMs for penetration-testing was _Getting pwn’d by AI_ by Happe et al. [33] in July 2023. They differentiated between two use-cases. On a strategic level, they used chatGPT to devise an 

1https://www.bleepingcomputer.com/ and https://www.darkreading.com/ 

On the Surprising Efficacy of LLMs for Penetration-Testing 

attack plan and gather information about a target organization. On an operational level, they introduced an autonomous penetrationtesting prototype capable of performing privilege-escalation attacks against a vulnerable Linux virtual machine. 

Deng et al. [16] published _pentestGPT_ in August 2023. Their prototype integrates human operators with an LLM to interactively hack CTF boxes. They were the first paper to explicitly state that LLMs have sufficient inherent capabilities for hacking but have problems with context-management, manifesting in missing longterm memory, recency bias, and hallucinations. They propose the Pentest-Task-Tree, a hierarchical todo list, to alleviate these problems. 

In October 2023, Happe et al. [38] published _LLM as Hackers_ . While still focusing on Linux privilege-escalation attacks, they exchanged the single vulnerable VM with a benchmark comprised of different privilege-escalation vulnerability classes to further analyze the capabilities of LLMs. They focus on context-management, summarization capabilities, in-context learning for providing background knowledge, the impact of high-level guidance, and included small language models in their evaluation. Their results indicate that small language models were not feasible for penetration-testing, highlight LLMs’ problems with complex multi-step attacks, and the importance of high-level strategy/guidance mechanisms for the overall performance of LLMs. 

_3.1.2 Broadening Domains and Embracing Newer LLM Capabilities (2024)._ In 2024, LLM-capabilities improved through the introduction of function-calling and structured-output. Supported context sizes increased from typical 4–16 kTokens in 2023 to typically 64–128 kTokens, with some models allowing for even larger context sizes, e.g., Google’s Gemini-1.5 model allowed for a context size of up to one million tokens in February 2024. 

In February 2024, Fang et al. [24] published _LLM Agents can Autonomously Hack Websites_ , extending targets to web sites and showing that LLMs were able to autonomously find vulnerabilities within them. They incorporated both in-context learning and were the first to use function-calling in their prototype. Also in February, Shao et al. [88] published _An Empirical Evaluation of LLMs for Solving Offensive Security Challenges_ . They analyze the capacity of LLMs for solving CTF challenges in interactive and autonomous settings. Similar to Fang et al., their prototype incorporated function-calling. They conclude that LLM-driven prototypes produced similar results compared to human penetration-testers. 

In March, Xu et al. [108] introduced _AutoAttacker_ focusing on post-breach attacks using the Metasploit attack framework. They explicitly mention the use of RAG for background knowledge storage. They are also the only paper within our analysis that explicitly mentioned the need for jailbreaks, i.e., being caught by LLM provider’s safety filters and needed to bypass these filters by utilizing roleplay prompting [49]. 

Fang et al. analyzed the capability of LLMs for exploit development, i.e., their capability to create exploits for both one-day<sup>2</sup> [23] and zero-day vulnerabilities [25]. In their initial paper, they used a 

> 2A zero-day vulnerability is unknown to the vendor, and thus there is no patch, mitigation, or fix available to address it. One-day vulnerabilities are known vulnerabilities for which a patch or mitigation is available but hasn’t yet been applied. 

GPT-4 based ReAct-agent and highlighted the need for better planning and improved exploration capabilities. In their latter paper, they implemented a hierarchical planning system using multiple task-specific agents that were provided background knowledge through in-context learning. Their results indicate that hierarchical planning improved penetration-testing results by a factor of 6, while task-specific agents and in-context learning both doubled the performance. 

Finally, in October 2024, Gioacchini et al. [28] introduced _AutoPenBench_ . They use function-calling and structured-output to autonomously solve CTF challenges. Their results indicate that LLMs were able to solve challenges if similar tasks were well documented publicly through blog posts and walk-throughs. 

_3.1.3 Breaching Out (2025)._ In January 2025, Kong et al. [52] introduced _VulnBot_ , a multi-agent autonomous prototype using a penetration-testing task graph as internal storage mechanism for creating high-level strategies. They also incorporated RAG for providing background knowledge to the agent. Also in February, Singer et al. [91] published _On the Feasibility of Using LLMs to Execute Multistage Network Attacks_ , switching from the single-host attacks performed by previous papers to attacking complex multi-stage networks. They introduce a tool abstraction layer that simplifies tool usage for LLMs, indicating that this abstraction enables smaller LLMs to successfully perform penetration-testing, while improving the hacking results of larger models. 

In February 2025, Happe et al. [37] published _Can LLMs Hack Enterprise Networks?_ , replacing single targets with a real-life Microsoft Active Directory enterprise network. Their prototype consists of a high-level strategy component using a penetration task tree, and a low-level ReAct-based task execution agent. They use tool-calling and structured-output and analyze the capabilities offered by reasoning LLMs. Their results indicate that modern models contain enough penetration-testing knowledge to perform autonomous hacking without providing background-knowledge through RAG. Their results indicate that LLMs have sufficient hacking capabilities but that results lack consistency, i.e., vary between testruns. They highlight models’ auto-repair capabilities and conclude that the costs of using LLMs for penetration-testing compares favorable to human penetration-testers. 

_3.1.4 Specialized LLMs for Security Tasks._ In parallel, LLMs were fine-tuned for security-tasks [83, 104]. As their makers typically do not publish these models, or, if published, they lack capabilities such as tool-calling, these specialized models were not used within the reviewed publications. 

---

## **3.2 Industry Adoption** 

> **Section Summary:** We differentiate between white-hats trying to improve security, and black-hats trying to use LLMs to exploit security vulnerabilities.


We differentiate between white-hats trying to improve security, and black-hats trying to use LLMs to exploit security vulnerabilities. 

_3.2.1 Benign White-Hats._ There has been interest in using LLMs to either accelerate tedious tasks during vulnerability research, to increase test coverage within analyzed projects, and to cover more projects with vulnerability research. 

Andreas Happe and Jürgen Cito 

Google operates OSS-Fuzz<sup>3</sup> which provides continuous fuzzing for open-source projects. In order to fuzz a project, complex fuzzing harnesses have to be created. OSS-Fuzz started to use AI for creating and testing these fuzz harnesses using AI [63] in August 2023, and reported 26 vulnerabilities detected with help of AI in November 2024 [11]. Their blog post highlights how LLMs were used to create and debug fuzz harnesses, leading to increased fuzzing coverage. In addition, LLMs were used to analyze the traces gathered by the fuzzing process. 

We will use the cooperation between Google’s Project Zero, a team of security-analysts tasked with finding zero days, and Google DeepMind as an example study for using LLM agents in security research. In June 2024, Project Zero detailed _Project Naptime_ [29], a LLM-powered vulnerability research framework. They utilized Chain-of-Thought, an interactive environment, specialized tools for debugging, and provide an external verification environment to validate found vulnerabilities. To explore multiple vulnerability hypotheses, instead of implementing a high-level strategizing loop, they advocate for a sampling strategy that explores multiple hypotheses through independent trajectories. In November 2024, they were able to disclose the first real-world vulnerability found through their agent, now called _Big Sleep_ : an exploitable stack buffer underflow in SQLite [95]. 

LLM-use is not limited to large-scale companies such as Google. Sean Heelan used OpenAI’s o3 model to find CVE-2025-37899 [41], a remote zero-day in the Linux kernel’s SMB implementation (a commonly used network file-system). They provided only a subset of the SMB code to o3 as including the full kernel code would exceed o3’s context size. They instructed the LLM to specifically search for use-after-free vulnerabilities [110], gave a high-level overview of the SMB module, and provided a threat model. They then ran the resulting prompt 100 times, resulting in 8 trajectories correctly identifying the vulnerability, indicating that LLMs have sufficient capabilities for finding zero-days, but lack reliability. 

LLMs are also used for non-exploitation purposes. Matt Adams released _StrideGPT_<sup>4</sup> , a LLM-powered automated threat-modeling tool. Daniel Miessler, a well-known security professional, provides _fabric_<sup>5</sup> , an open-source framework for augmenting humans with AI. In his opinion, “ _AI doesn’t have a capabilities problem—it has an integration problem_ ”. 

This list does not include indirect industry use, i.e., security professionals using LLMs instead of dedicated search systems for security-specific information-retrieval. Anecdotally, LLM systems are also used during reporting. 

_3.2.2 Malicious Black-Hats._ Academic research indicated early uptake of LLMs by malicious actors, often facilitated within the Darknet [26, 62]. Specialized LLMs employing neither ethical guardrails nor safety filters were offered to help with exploit development, social engineering, and information gathering. Monitoring this malicious use of LLMs is complicated by their provider’s inherent covert and illegal operation. 

Public cloud-backed LLM providers have started to periodically publish abuse reports. We analyze malicious tasks included in 

the reports provided by OpenAI [75–77, 80], Anthropic [5], and Google [30]. Overall, they show a similar theme: threat actors use LLMs to accelerate and optimize their work, but they do not use them to create novel methods of attack. Threat actors use LLMs for information gathering similar to using search engines, employ them for developing and debugging malicious software, and use them to generate content for social engineering and phishing attacks. 

Presumed state-level actors use LLMs for covert _Influence Operations_ (IO) trying to perform election tinkering, sway public opinion especially in and around conflict zones, discredit political activists and parties, attack independent media, sow discontent within populations, and polarize existing population sub-groups. They use LLMs to rewrite articles from genuine news sources with a particular political perspective or tone. Anthropic highlighted an _Influenceas-a-Service_ operation in their March 2025 report [5, 58], detailing a semi-autonomous LLM-driven system that used approximately 100 fake social-media puppet accounts to influence opinion. AI was used to make both strategic and tactical decisions when and how to employ these social accounts and incorporated LLM-powered image generators. 

Advanced Persistent Threats (APTs) use LLMs to aid development of malware and backdoors, analyze defensive capabilities and perform deceptive employment schemes.<sup>6</sup> As Anthropic states [5], LLMs “ _flatten the learning curve for malicious actors_ ”. OpenAI’ highlighted in its June 2025 report [76] that threat actors start to research into LLM-driven penetration-testing. 

---

## **4 ON THE SURPRISING EFFICACY OF LLMS FOR PENETRATION-TESTING** 

> **Section Summary:** In this section we speculate why LLMs have become a part of the vanguard for automated penetration-testing.


In this section we speculate why LLMs have become a part of the vanguard for automated penetration-testing. 

There are few empirical studies on the work practices of penetrationtesters and their decision making processes [34]. Thus, we include our own experiences (one of the authors has been a professional penetration-tester for 13 years and taught penetration-testing both in academic and industrial settings). We encourage further empirical research into hackers’ work and expect that future findings will support our hypotheses. 

---

## **4.1 Penetration-Testing Resembles Pattern-Matching** 

> **Section Summary:** We focus on security practitioners within this work: they are the professionals that perform daily penetration-tests to find vulnerabilities in enterprise networks and web-applications.


We focus on security practitioners within this work: they are the professionals that perform daily penetration-tests to find vulnerabilities in enterprise networks and web-applications. 

_4.1.1 Pattern-Matching is a Substantial Part of Penetration-Testing._ Empirical studies with security professionals [34] list examples of practitioners applying pattern-matching, e.g., identifying vulnerable areas or operations through knowledge gained from CTF exercises, applying knowledge learned as software developer, using knowledge from prior interactions with the customer and their systems, and using vulnerabilities that the penetration-tester has exploited before. 

3https://github.com/google/oss-fuzz 

> 4https://github.com/mrwadams/stride-gpt 

> 5https://github.com/danielmiessler/fabric 

6These are a form of social engineering attack in which the attacker applies for a job interview to gain access to the target organization. 

On the Surprising Efficacy of LLMs for Penetration-Testing 

One example of pattern-matching in penetration testing are _Vulnerability Assessments_ . During those, software version numbers, detected from service banners or application errors messages, are compared against well-known vulnerabilities. If a match occurred, a potentially available exploit is prepared, i.e., its options are filled with data gathered from the target environment, and execute to exploit the expected vulnerability. Pattern matching occurs at multiple levels: detecting error messages, matching them to the vulnerability catalog, matching the right configuration options, and matching the exploit’s output to the expected behavior. 

Another low-level occurrence of pattern-matching happens during analyzing of web-application responses containing error messages. For example, LLMs can match error messages that indicate database issues (SQL injection attacks) to knowledge in their training data, and subsequently successfully exploit these vulnerabilities [24]. 

On a higher level, creating an attack-strategy is also grounded in patterns seen during security testing. Interviews with professional penetration-testers indicate that they encounter similar insecure configurations during assignments, create a hypothesis about the network’s security, and select attacks based upon that [34]. For example, if penetration-testers encounter unsigned NTLMv2-Hashes during an enterprise network security test, they assume that the overall target network matches security bad-practices from 10 years ago and attempt matching attacks such as pass-the-hash attacks. 

_4.1.2 The Target System Landscape is Homogeneous._ Pattern-matching is only feasible if penetration-testing targets exhibit similarities— otherwise there would be insufficient features to base the patternmatching on. Fortunately, when looking at enterprise networks, over 90% of Global Fortune 1000 companies use the same underlying technology stack (Section 2.1). Security practitioners note that they encounter the same security vulnerabilities and insecure configurations during assignments [34]. When looking at web penetration-testing, the landscape is more diverse. Applications utilizing the same technology stack, e.g., the same web framework, are similar implementation-wise and often exhibit similar vulnerabilities. Architectures between different technology stacks also show similarity through common architecture design patterns. 

_4.1.3 LLMs exceed in Pattern-Matching._ One side-effect of the ongoing discussion about LLMs’ reasoning capabilities is that researchers agree that LLMs exceed at pattern-matching [71, 86, 90]. Given the previous section, this implies that they are well-suited for penetration-testing. 

Research implies that LLMs are able to solve tasks if examples in their training data resemble those tasks [28]. Given the described semi-monocultures, target IT environments should resemble each other. Furthermore, there is ample publicly available penetrationtesting background knowledge available from technical blog posts, incident reports, and CTF walk-throughs and thus included in common training data sets. We further note that common walkthrough formats, i.e., providing step-by-step instructions including reasoning steps and tool usage examples, structurally resembles trajectories used to train LLMs and thus are well-suited to train LLMs. 

---

## **4.2 LLMs Inherently Cope With Uncertainty** 

> **Section Summary:** _4.2.1 Uncertainty During Penetration-Testing._ Security practitioners routinely deal with uncertainty [34, 43].


_4.2.1 Uncertainty During Penetration-Testing._ Security practitioners routinely deal with uncertainty [34, 43]. Examples given for sources of uncertainty include interpreting misleading tool outputs and target system responses, negative side-effects like target systems becoming unresponsive due to exploits, incomplete information about the target environment, and invalid but not falsified assumptions about the target system’s behavior and security. 

_4.2.2 LLMs’ Pattern-Matching Copes with Uncertainty._ Patternmatching is inherently capable of dealing with uncertainty. During a penetration-test, a LLM-driven hacking prototype will sample the target environment and create a representation of its view of the target world, typically as a text-based representation. This world view is typically included in subsequent LLM invocations. Compared to deterministic rule-based systems, LLMs are able to ignore parts of their world-view through the pattern-matching process. This is beneficial during penetration-testing in realistic network scenarios where actions influence the state of the network, e.g., where a failed attack might lead to locked accounts or crashed network servers, changing the ground truth. While traditional systems need to manually invalidate their world view, LLMs implicitly do this through their pattern-matching approach. 

---

## **4.3 The Costs of Using LLMs** 

> **Section Summary:** When adopting machine learning, there’s always the question of costs for creating and operating the system, as well as for creating a training data-set and utilizing it for training.


When adopting machine learning, there’s always the question of costs for creating and operating the system, as well as for creating a training data-set and utilizing it for training. 

_4.3.1 LLM-Makers are Front-Loading Creation Costs._ As shown through-out our review of academic research (Section 3.1), off-theshelf LLMs already contain sufficient background knowledge to perform penetration-testing, alleviating the need to costly train new security-specific LLMs. Even if specific additional knowledge is needed, In-Context Learning and RAG (Section 2.3) offer costeffective alternatives to training a model from scratch. 

A model alone does not make a penetration-testing prototype— integration with its environment is also required. The LLM ecosystem provides easy access to development libraries/frameworks. Technologies, such as function-calling or MCP, make integration efficient from a development perspective. 

_4.3.2 LLM-Providers Enable Cost-Effective Inference._ Running LLMs using cloud-based LLM-providers is cost efficient, e.g., Happe et al. [37] listed operational costs for their penetration-testing prototype running from $0.10 to $11.64 depending on the used LLM. 

Given the sensitive nature of using LLMs for hacking, LLM providers imposing stricter safety guards would negate this benefit. Of the reviewed academic publications, a single paper mentioned problems with safe-guards [108]—and those were easily bypassed by simple techniques such as roleplay-prompting [49, 108]. 

_4.3.3 Costs of Running to Stand Still._ In evolutionary biology, the Red Queen’s hypothesis proposes that species must continuously adopt and evolve to survive while pitted against ever-evolving opposing species [98]. In penetration-testing, we have active adversaries (defensive blue teams) that adapt to our attacks and evolve 

Andreas Happe and Jürgen Cito 

their defenses based on our activities, e.g., develop new intrusiondetection (IDS/IPS) or endpoint detection and response (EDR) capabilities. 

Security tooling, esp. in case of covert C2 frameworks or vulnerability scanners, impose a high maintenance cost as they have to be adopted to new vulnerabilities, current trends, and evolved adversary measures. Penetration-testers also have to continuously improve, e.g., learn new attack vectors or how to circumvent novel counter-measures. Delegating parts of these costs to the LLM-maker, as newer training data will inherently incorporate these new techniques, is thus tempting to time-poor penetration-testers. 

---

## **4.4 Additional Beneficial Capabilities** 

> **Section Summary:** We want to high-light additional LLM capabilities that, while not required for successful penetration-testing, are beneficial.


We want to high-light additional LLM capabilities that, while not required for successful penetration-testing, are beneficial. 

_4.4.1 Inter-Context Attacks._ Compared to traditional tooling, LLMs provide multi-modal or inter-context capabilities [37]. For example, if a LLM detects a web-server during an enterprise network penetration-test, it will switch to a web-testing context and perform a web penetration-test. They are able to detect passwords in text files [37] and utilize them during subsequent penetration-testing steps. This is a time-consuming task, typically performed by human penetration-testers [34]. 

_4.4.2 Hallucinations often not deemed catastrophic._ LLMs are prone to hallucinations, e.g., they invent untrue facts. In small amounts, this can be beneficial during penetration-tests as it is similar to human penetration-testers trying out hypotheses about the security of their target systems. Thus, limited hallucinations are not as problematic for the penetration-testing use-case compared to other software-engineering use-cases. 

The former highlights the potential for developer burnout, catastrophic failures, ethical problems, and increased maintenance costs [60]; while the latter highlight developer efficiency gains and reduction of tedious work. While our use-case, penetration-testing, does not include high-maintenance overheads, safety concerns are paramount [84]. 

We foresee that, over time, more and more complex tasks will be delegated to LLM agents, culminating in LLMs autonomously performing complex multi-step tasks. This is already established in academic research (Section 3.1) and first forays can be seen in industrial adoption (Section 3.2). 

---

## **5.2 Towards Autonomous Hacking** 

> **Section Summary:** We see two research directions leading towards autonomous hacking.


We see two research directions leading towards autonomous hacking. The first paper using LLMs for penetration-testing already used autonomous LLM agents [33]. In addition, with increasing delegated task complexity, interactive LLM-systems resemble autonomous hacking systems. When the task becomes “hack system x”, both approaches converge. 

Capability evaluations show that LLMs contain sufficient penetrationtesting capabilities to successfully exploit systems, but their reliability is lacking, i.e., the same LLM-driven prototype will find different attack chains within the same testbed during multiple runs (Section 3.1). 

Autonomous systems often try to minimize the amount of keeping humans in the loop for efficiency reasons, increasing safety concerns (Section 6.2) when deploying autonomous prototypes. 

We find it concerning that malicious actors already have started to investigate using LLMs for autonomous penetration-testing and influence-operations (Section 3.2.2), increasing the need for security tooling with which defenders can test and improve their defenses. 

---

## **6 OBSTACLES TO OVERCOME** 

---

## **5 STATUS-QUO: VIBE-HACKING AND AUTONOMOUS AGENTS** 

> **Section Summary:** We want to highlight the current status-quo of LLM-driven penetrationtesting.


We want to highlight the current status-quo of LLM-driven penetrationtesting. We structure this into interactive use of LLMs ( _vibe-hacking_ ) and in prototypes that use LLMs to autonomously hack systems. 

---

## **5.1 Vibe-Hacking** 

> **Section Summary:** As Section 3.2 has shown, industrial interactive uptake of LLMs is already occurring.


As Section 3.2 has shown, industrial interactive uptake of LLMs is already occurring. Borrowing from _vibe-coding_ , this interactive delegating of tedious tasks has become known as _vibe-hacking_ . Levels of autonomy are diverse, ranging from chat-based LLMs for information-retrieval and exploit-code generation, over co-pilot inspired augmenting agents, to systems influenced by pentestGPT [16] where humans are responsible for oversight. CTF challenges are often created by the same authors, exhibiting patterns in their structure. Anecdotally, CTF players use OpenAI’s custom GPTs support to create LLMs trained with previous challenges created by well-known authors and use that knowledge for future challenges. Compared to other automation approaches, currently vibe-hacking keeps the human in the loop and thus incorporating an important safety feature. 

While _vibe-hacking_ is not often discussed online, _vibe-coding_ is, current opinions range from AI Angst to AI enthusiasm [8]. 

We highlight obstacles that prevent further adaption of LLMs for penetration-testing. We focus on autonomous use as this includes obstacles relevant to vibe-hacking too. 

---

## **6.1 Model Features and Stability** 

_6.1.1 Impact of Feature Selection._ Agentic AI (Section 2) is highly dependent on LLM features such as function-calling and structuredoutput, limiting model selection to LLMs supporting these features. Empirical research [61] has shown that model support for these features is not homogeneous and, even if features are supported, using these features can impact the overall quality of LLM responses. During our research using LLMs-as-Judges, we saw that switching to structured-output changed the LLM judge’s result. 

_6.1.2 Minuscule Changes Impact Outcomes._ LLMs can be unstable and exhibit chaotic behavior: minimal changes to prompts or switching model versions can substantially impact created trajectories. Capability differences between model families are expected, but there can be unexpected differences between versions of the same model family, e.g., there is an ongoing discussion if OpenAI’s o1preview model’s capabilities were significantly reduced compared to the final o1 model [2, 3]. Obviously, prompt engineering has a large impact upon the LLM’s results and their consistency [101]. Unobvious, formatting changes orthogonal to the prompt’s content 

On the Surprising Efficacy of LLMs for Penetration-Testing 

impact results: He et al. [40] investigated the impact of using different formats (such as plain text, Markdown, JSON, and YAML) for providing context information and detected a variance of 40% when using OpenAI GPT-3.5-turbo. Another problem is that even when using deterministic settings, an LLM’s output can still be nondeterministic [6]. 

These instabilities are problematic as seemingly unrelated prompt adaptions occurring during empirical experiments can potentially impact and taint the experiment’s measurements. 

---

## **6.2 Safety and Security Concerns** 

> **Section Summary:** _6.2.1 Safety._ As LLMs are autonomously interacting with their environment in potentially destructive ways, safety is of the highest concern.


_6.2.1 Safety._ As LLMs are autonomously interacting with their environment in potentially destructive ways, safety is of the highest concern. Typically, prototypes embed safety instructions into their prompts, e.g., limit valid targets that the LLM prototype is allowed to attack. If LLMs do not heed those safety instructions, outcomes can be catastrophic. Concurrent research investigates potential catastrophic fallout when LLMs are used in National Security Applications [10] or CBRN [109] domains.<sup>7</sup> Safety instructions are also employed during penetration-testing. Happe et al. [37] describe while they instructed LLMs to only target their lab network range, some of their evaluated LLMs ignored those instructions and attacked systems explicitly forbidden form being targeted. 

_6.2.2 Alignment Concerns._ Happe et al. [37] highlight another case in which the LLM diverged from the user’s original intent by discarding the assigned task and starting to solve an unrelated security task, thus breaking the model’s alignment with the user’s goals. Similar problems can occur unintentionally, e.g., through changes in the model’s deployment infrastructure [27], or can be maliciously precipitated [66]. 

_6.2.3 Security._ Safety and security are intertwined. While we are investigating the offensive use of LLMs, offensive prototypes can also become the target of adversaries, e.g., became victims to active or forward defenses. Offensive AI agents are high-value targets for attackers as they sit at the intersection of private data, untrusted content, powerful actions, and external communication [106]. An adversary, that is able to take over an offensive AI agent, e.g., through using a prompt injection, gains powerful means of attacking the agent’s owner or an unrelated third-party system, further complicating attribution. 

---

## **6.3 Costs and Efficiency Concerns** 

> **Section Summary:** _6.3.1 Monetary Costs._ Running a LLM depends upon a costly runtime environment: either they run on expensive local AI accelerators or are hosted within on-demand clouds occurring a per-minute cost.


_6.3.1 Monetary Costs._ Running a LLM depends upon a costly runtime environment: either they run on expensive local AI accelerators or are hosted within on-demand clouds occurring a per-minute cost. Especially newer reasoning models can incur unexpected costs when using their maker’s cloud offerings: spending thousands of US$ for running a single prototype for few hours is not unheard of; using a non-reasoning LLM with the same prototype can cost 1–2 orders of magnitude less. 

_6.3.2 Ecological Costs._ Concerns about non-monetary cost are becoming more prominent [96]. Energy-usage of LLMs imposes a ecological burden that needs to be answered for by their utility. 

7Chemical, Biological, Radiological and Nuclear (CBRN) 

Analysis of the energy and water usage of different model families indicates that reasoning models, such as OpenAI o3 or DeepSeekR1, consume 70 times the energy compared to a small LLM such as OpenAI GPT-4.1-nano, making conscious model selection an important goal for sustainability [47]. 

_6.3.3 Effectiveness of Using LLMs._ Given the mentioned monetary and ecological costs, usage of LLMs should show cost-effectiveness. The common internet saying of “ _go away or I will replace you with a small shell script_ ” encapsulates the difference between the two extremes: writing a shell script can be tedious and resourceintensive, but operating it is light on resources. Creating a LLMdriven hacking prototype is comparatively cheap, but running it is resource-intensive. Coming back to Sommer and Paxson [92], machine-learning might not be an end in itself, but rather an underappreciated means to an end, used to illuminating the problem space. 

---

## **6.4 Privacy and Digital Sovereignty Concerns** 

> **Section Summary:** LLMs do not exist in emptiness but within the real-world with its geo-political tensions.


LLMs do not exist in emptiness but within the real-world with its geo-political tensions. 

_6.4.1 Privacy._ When LLM-driven penetration-testing prototypes interact with enterprise networks, there’s a high chance of them ingesting sensitive data. If using cloud-provided LLMs, this sensitive data is transported to the cloud of the respective LLM provider—a potential violation of digital sovereignty. If an LLM-driven prototype is able to detect and exploit a vulnerability, knowledge of this vulnerability is also transported to the LLM cloud; this means that knowledge of an exploitable vulnerability is thus stored outside of the security perimeter and control of the affected company—both a security and privacy risk. 

_6.4.2 Digital Sovereignty._ LLMs are currently only provided by a limited amount of countries, making LLM users dependent upon those countries. 

Another problem is the opaque nature of LLMs. Due to their missing explainability, both closed- and open-weight models can contain backdoors that can result in adversary-planted behavior when triggered by a predefined interaction with the environment. Kutosov et al. [56] tasked frontier LLMs to compete a main task while they should also covertly execute a side-task, emulating industrial espionage, sabotage, and insider threats. Complex models such as Claude 3.7 Sonnet and Gemini 2.5 Pro performed “best”, resulting in 27% and 15% successful covert task execution. 

---

## **6.5 Accountability Concerns** 

_6.5.1 Who is accountable if a LLM makes a faulty decision?_ A famous quote from a 1970’s IBM manual has become surprisingly relevant again: “ _A computer can never be accountable therefore a computer must never make a management decision_ ” [45]. There has been legal precedent of a company being made liable for advice given by a LLM-powered chat bot [111]. 

Given the potential catastrophic impact of a security LLM-prototype interacting with their target environment, who is liable for direct and collateral damages? Imagine, that a company’s operation is disrupted due to a LLM-operated penetration-test that executed a destructive command unrelated to the penetration-testing task 

Andreas Happe and Jürgen Cito 

at hand. Who is liable for damages? What if this happens not to a “normal” company but to a power plant? 

_6.5.2 Overlap with Explainability._ Regulatory and legal requirements often imply explainability. The European Union’s AI Act mandates that organizations operating high-risk AI systems must provide meaningful explanations of AI decisions to individuals. In the United States of America, _the FDA’s proposed framework for medical devices empathizes the importance of explainable AI for patient safety and clinical decision making_ [18]. 

---

## **6.6 Capability vs. Reliability** 

_6.6.1 Missing Reliability._ As mentioned in Sections 3.1.3 and 3.2.2, experiments indicate that LLMs exhibit capabilities for penetrationtesting but lack reliability, i.e., multiple runs of the same prototype against the same testbed yield different vulnerabilities. The obvious solution of repeatedly calling the prototype is problematic due to the higher time- and resource usage (Section 6.3). In addition, if a security-test should be covert, repeatedly calling the prototype might trigger detection. Better approaches to raise consistency and reliability are needed. 

_6.6.2 The Problem with Capability Evaluations._ Capability Evaluations are used to measure LLM’s abilities throughout diverse fields, typically using testbeds and benchmarks. Benchmark test-cases have multiple desired properties, e.g., atomicity of test-cases and reproducibility, that can conflict with real-world use-cases which are often “messy” and not reproducible [35]. There are concerns [64, 92] that synthetic test-beds often do not measure real-world impact and thus not provide meaningful guidance for LLM development. 

---

## **6.7 Concerns About Ethics** 

> **Section Summary:** While usage of LLMs might be technically feasible, the question arises if it is ethical, or wise, to advance this research.


While usage of LLMs might be technically feasible, the question arises if it is ethical, or wise, to advance this research. Machinelearning ethics is a diverse field; we only cover the subset of using LLMs for penetration-testing purposes and refer to existing publications for areas not covered in this publication, such as bias [14, 94, 100] or potential problems with training data [13, 19, 67]. 

_6.7.1 Democratizing Access to Penetration-Testing._ Mirsky et al. [72] noted that **AI is a Double-Edged Sword** . Security researchers with noble intentions see the potential of AI democratizing access to security testing, i.e., providing access to security testing to parties that currently lack means of testing to improve their security posture. Examples typically given include small- and medium businesses (SMEs), non-governmental, and non-profit organizations (NGOs and NPOs). As shown in our review of blackhat activities (Section 3.2.2), malicious actors also see the potential of AI, although with less benign intentions. This problematic situation results from the inherent dual-purpose nature of security tooling [65]. Recent research into how security researcher express their ethical considerations indicates that they are aware of this ethical dilemma [36]. 

_6.7.2 Impact Upon Workforce._ In economics, Schumpeter’s _Creative Destruction_ describes a process in which new innovations replace and make obsolete older innovations [17]. The impact of LLMs, especially their potential for automating tasks, on the workforce is currently subject of academic discussions [22, 42, 54, 85, 89, 102] 

with the hopeful expectation that LLMs will be beneficial for novice and lower-skill workers [9]. 

Experience indicates that successful use of autonomous LLMagents depends on oversight by highly-skilled human workers with domain knowledge [105]. Recent research shows that (premature) use of LLMs during education, e.g., through delegating informationretrieval tasks, has negative impact on brain neural connectivity, leading to measurable negative impact on learning skills [53]. Do we bite the hand that feeds us? 

---

## **7 THE WAY FORWARD?** 

> **Section Summary:** Academic (Section 3.1) and industrial (Section 3.2) uptake of LLMs suggest that they will play an increasing role for cybersecurity in the near future.


Academic (Section 3.1) and industrial (Section 3.2) uptake of LLMs suggest that they will play an increasing role for cybersecurity in the near future. As Section 5 showed, vibe-hacking is already here, and real-world use of LLMs for autonomous hacking is currently investigated by both white- and blackhats. Based on the issues mentioned in Section 6, we now turn to potential remediations and research opportunities to enable and ease adaption of LLMs for offensive security tasks. 

---

## **7.1 Costs and Features** 

> **Section Summary:** While LLM-based experiments can impose substantial costs (Section 6.3), the overall trajectory indicates continuously decreasing costs per token.


While LLM-based experiments can impose substantial costs (Section 6.3), the overall trajectory indicates continuously decreasing costs per token. For example, during January 2025, one million output/reasoning tokens using OpenAI’s o1 model would cost $60. Five months later, using the new o3 model, the costs would have been reduced from $60 to $8 per million output/reasoning tokens. 

Newer model releases typically also improve their feature support, e.g., function-calling and structured-output. Currently, reasoning models seem to struggle with function calling [112]. While this problem is something that researchers should be aware of, this situation should resolve itself quickly. 

While costs per token decreases, overall volume of token consumption is rising and thus impacts global energy use and ecology. To reduce this impact, careful selection of models is essential, e.g., only using reasoning models if their capabilities are needed. Unfortunately, one of the most resource-intensive areas of using LLMs, image- and video-creation [68], is used by blackhats for influence operations (Section 3.2.2)—we assume that these malicious operators are not that ecology-conscious. Ultimately, the decision about the ecological impact of LLMs if for each individual, and societies at large, to decide (Section 7.4). 

---

## **7.2 The Need for Better Safeguards** 

> **Section Summary:** LLMs become further integrated into security workflows and thus gain more potential to interact with their environment, making their security and safety parameter (Section 6.2).


LLMs become further integrated into security workflows and thus gain more potential to interact with their environment, making their security and safety parameter (Section 6.2). If security or safety incidents occur, Accountability (Section 6.5) becomes important. 

Google identified multiple features needed for operating secure LLM-based systems [21]. Prominent features were, e.g., protection from malicious inputs, limitation of agents’ interaction capabilities, and clear human oversight being enforced. 

Prototypes can use LlamaGuard [44] to analyze user input for unsafe content, e.g., if a user might follow criminal intentions. The similarly named Llama PromptGuard [70] can be used to detect malicious inputs used for prompt-injection or jailbreak attacks. 

On the Surprising Efficacy of LLMs for Penetration-Testing 

Google CaMeL [15] applies _Control Flow Integrity_ [1], a traditional defensive mechanism, to LLM prompting and uses it to separate data from control flow. Meta’s CodeShield [12] uses source-code analysis to prevent malicious program generation through agentic AI. Agent AlignmentChecks [12] continuously compares a LLM’s reasoning trace with the user’s stated goal to detect misalignment. 

Still, using agentic AI for penetration-testing imposes the problem that we cannot differentiate ethical hacking (whitehats) from unethical hacking (blackhats) as the utilized mechanisms and techniques are identical. In the case of red-teaming, there is not even a difference in the target’s awareness of being attacked. Ultimately, the only difference is the potential impact of a penetration-testing campaign on the target, but as this is orthogonal to the penetrationtesting operations that were performed before, this cannot be used to differentiate ethical from unethical behavior. 

Please note that concerns for safety and security should not be abused as reason to put ethical penetration-testing prototypes inside walled-gardens to prepare later commercialization. 

---

## **7.3 Capabilities and Reliability** 

> **Section Summary:** As seen in Section 6.6.1, there is currently a lack of reliability and reproducibility when using LLMs for penetration-testing.


As seen in Section 6.6.1, there is currently a lack of reliability and reproducibility when using LLMs for penetration-testing. Improvements can be categorized in single-agent and multi-agent solutions. The former try to improve reliability within a single agent’s trajectory, while the latter combine multiple agents to increase reliability while typically imposing higher token costs due to more agents being run. 

Single-LLM solutions currently explore the impact of self-discussion or self-challenging [116], investigate better state management [57], or implement auto-correction mechanisms [37]. Multi-LLM solutions typically combine output of multiple agents using techniques such as LLM-as-judge [31] to integrate the results of singular agents. As Anthropic notes [32], multi-agent systems improve the actinspace search breadth but incur substantial higher token costs (they note that their multi-agent system consumes 3 _._ 75 times the tokens of a similar single-agent system) introducing an overlap with monetary and economic cost concerns (Section 6.3). 

If a multi-agent system uses multiple different LLMs, concerns about LLM stability in face of minuscule changes altering the trajectory substantially (Section 6.1.2 should be alleviated as each individual model should have a reduced overall impact on the system’s result. 

Regardless of the chosen approach, more empirical data about model behavior is needed. Improving the explainability of models would make analysis of models’ decisions more impactful and also more efficient. 

---

## **7.4 Decision Time for Individuals and Society** 

> **Section Summary:** While we try to propose technological improvements, some of the imposed problems of LLMs are for society to decide, i.e., are a socio-economical problem, not a technological one.


While we try to propose technological improvements, some of the imposed problems of LLMs are for society to decide, i.e., are a socio-economical problem, not a technological one. We need consensus on how to handle privacy, ecological impact, ethical issues, accountability, and digital sovereignty concerns (Section 6.7). While technology solutions for parts of the problems exists, e.g., running small language models locally to keep data private, individuals will 

often have to ultimately decide if they value, e.g., privacy, over LLM-provided features. 

Andy Masley compared resource-consumption of using LLMs with other lifestyle-decisions [96] and calculated the equivalent of “going vegan” with 400 _._ 000 chatGPT text queries a year, concluding with that his becoming vegan will offset his chatGPT use. When measuring the average query counts of the two best-performing LLMs for hacking enterprise networks [37], we arrive at 165 _._ 75 queries per hours, or _._ 145 million queries a year if the autonomous penetration-testing prototype is running 24/7. Given their preliminary results, this could prevent dozens or hundreds of ransomware incidents saving resource-intesive recovery costs. How would this balance out? 

---

## **8 CONCLUSION** 

> **Section Summary:** Using LLMs for offensive security is evolving at a fast pace.


Using LLMs for offensive security is evolving at a fast pace. Vibehacking has already been established; autonomous penetrationtesting is currently investigated within Academia while both blackand whitehat hackers are deploying first systems in production. Given the scarcity of professional penetration-testers, a reduction in interest is hard to believe in. 

Due to the high-risk environment, keeping humans in the loop is essential for production environments’ safety. We hope that the proliferation of using LLMs during in or during education will not reduce human capabilities [53] needed for performing this oversight. 

Security tooling always had an dual-edged nature, especially if it is deployable in an autonomous manner as this reduces the skills needed to perform security audits. We have reports of initial adversarial use (Section 3.2.2), we are already within a weapons race. Fittingly, Vernor Vinge [99] used the Red Queen’s paradox to illustrate the struggle between encouraging technological advancement and protecting the world if technology is abused. While originally this was written as part of a science fiction story-line, we are living it out right now. 

---

## **REFERENCES** 

> **Section Summary:** - [1] Martín Abadi, Mihai Budiu, Ulfar Erlingsson, and Jay Ligatti.


- [1] Martín Abadi, Mihai Budiu, Ulfar Erlingsson, and Jay Ligatti. Control-flow integrity principles, implementations, and applications. _ACM Transactions on Information and System Security (TISSEC)_ , 13(1):1–40, 2009. 

- [2] Anonymous. O1 is less powerful than o1-preview due to the less time it spends on thinking (compute time). https://www.reddit.com/r/OpenAI/comments/ 1h7qtaf/o1_is_less_powerful_than_o1preview_due_to_the/, December 2024. Accessed: 2025-06-29. 

- [3] Anonymous. Performance of o1 vs. o1-preview. https://community.openai. com/t/performance-o1-vs-o1-preview/1046831/1, December 2024. Accessed: 2025-06-29. 

- [4] Anthropic. Introducing the model context protocol. https://www.anthropic. com/news/model-context-protocol, November 2024. Accessed: 2025-06-02. 

- [5] Anthropic. Detecting and countering malicious uses of claude: March 2025. https://www.anthropic.com/news/detecting-and-countering-malicioususes-of-claude-march-2025, April 2025. Accessed: 2025-06-19. 

- [6] Berk Atil, Sarp Aykent, Alexa Chittams, Lisheng Fu, Rebecca J. Passonneau, Evan Radcliffe, Guru Rajan Rajagopal, Adam Sloan, Tomasz Tudrej, Ferhan Ture, Zhe Wu, Lixinyu Xu, and Breck Baldwin. Non-determinism of "deterministic" llm settings, 2025. URL https://arxiv.org/abs/2408.04667. 

- [7] Mohamed Boukhlif, Nassim Kharmoum, and Mohamed Hanine. Llms for intelligent software testing: A comparative study. In _Proceedings of the 7th International Conference on Networking, Intelligent Systems and Security_ , NISS ’24, New York, NY, USA, 2024. Association for Computing Machinery. ISBN 9798400709296. doi: 10.1145/3659677.3659749. URL https://doi.org/10.1145/ 3659677.3659749. 

- [8] Tim Bray. Ai angst. https://www.tbray.org/ongoing/When/202x/2025/06/06/ My-AI-Angst, June 2025. Accessed: 2025-06-29. 

Andreas Happe and Jürgen Cito 

- [9] Erik Brynjolfsson, Danielle Li, and Lindsey Raymond. Generative ai at work. _The Quarterly Journal of Economics_ , page qjae044, 2025. 

- [10] William N Caballero and Phillip R Jenkins. On large language models in national security applications. _Stat_ , 14(2):e70057, 2025. 

- [11] Oliver Chang, Dongge Liu, and Jonathan Metzman. Leveling up fuzzing: Finding more vulnerabilities with ai. https://security.googleblog.com/2024/11/levelingup-fuzzing-finding-more.html, November 2024. Accessed: 2025-06-19. 

- [12] Sahana Chennabasappa, Cyrus Nikolaidis, Daniel Song, David Molnar, Stephanie Ding, Shengye Wan, Spencer Whitman, Lauren Deason, Nicholas Doucette, Abraham Montilla, et al. Llamafirewall: An open source guardrail system for building secure ai agents. _arXiv preprint arXiv:2505.03574_ , 2025. 

- [13] A. Feder Cooper, Aaron Gokaslan, Amy B. Cyphert, Christopher De Sa, Mark A. Lemley, Daniel E. Ho, and Percy Liang. Extracting memorized pieces of (copyrighted) books from open-weight language models, 2025. URL https: //arxiv.org/abs/2505.12546. 

- [14] Sunhao Dai, Chen Xu, Shicheng Xu, Liang Pang, Zhenhua Dong, and Jun Xu. Bias and unfairness in information retrieval systems: New challenges in the llm era. In _Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ , pages 6437–6447, 2024. 

- [15] Edoardo Debenedetti, Ilia Shumailov, Tianqi Fan, Jamie Hayes, Nicholas Carlini, Daniel Fabian, Christoph Kern, Chongyang Shi, Andreas Terzis, and Florian Tramèr. Defeating prompt injections by design. _arXiv preprint arXiv:2503.18813_ , 2025. 

- [16] Gelei Deng, Yi Liu, Víctor Mayoral-Vilches, Peng Liu, Yuekang Li, Yuan Xu, Tianwei Zhang, Yang Liu, Martin Pinzger, and Stefan Rass. {PentestGPT}: Evaluating and harnessing large language models for automated penetration testing. In _33rd USENIX Security Symposium (USENIX Security 24)_ , pages 847– 864, 2024. 

- [17] Arthur M Diamond Jr. Schumpeter’s creative destruction: A review of the evidence. _Journal of Private Enterprise_ , 22(1):120, 2006. 

- [18] Lee Dittmar. The explainability challenge of generative ai and llms. https://www. oceg.org/the-explainability-challenge-of-generative-ai-and-llms/, November 2024. Accessed: 2025-06-21. 

- [19] Chris Draper and Nicky Gillibrand. The potential for jurisdictional challenges to ai or llm training datasets. In _AI4AJ@ ICAIL_ , 2023. 

- [20] Rohit Dube. Large language models in information security research: A january 2024 survey. _ResearchGate preprint RG_ , 2(20107.26404), 2024. 

- [21] Santiago (Sal) Díaz, Christoph Kern, and Kara Olive. Google’s approach for secure ai agents. Technical report, 2025. 

- [22] Tyna Eloundou, Sam Manning, Pamela Mishkin, and Daniel Rock. Gpts are gpts: Labor market impact potential of llms. _Science_ , 384(6702):1306–1308, 2024. 

- [23] Richard Fang, Rohan Bindu, Akul Gupta, and Daniel Kang. Llm agents can autonomously exploit one-day vulnerabilities, 2024. URL https://arxiv.org/abs/ 2404.08144. 

- [24] Richard Fang, Rohan Bindu, Akul Gupta, Qiusi Zhan, and Daniel Kang. Llm agents can autonomously hack websites, 2024. URL https://arxiv.org/abs/2402. 06664. 

- [25] Richard Fang, Rohan Bindu, Akul Gupta, Qiusi Zhan, and Daniel Kang. Teams of llm agents can exploit zero-day vulnerabilities, 2024. URL https://arxiv.org/ abs/2406.01637. 

- [26] Mohamed Fazil Mohamed Firdhous, Walid Elbreiki, Ibrahim Abdullahi, BH Sudantha, and Rahmat Budiarto. Wormgpt: a large language model chatbot for criminals. In _2023 24th International Arab Conference on Information Technology (ACIT)_ , pages 1–6. IEEE, 2023. 

- [27] Asma Ghandeharioun, Ann Yuan, Marius Guerard, Emily Reif, Michael Lepori, and Lucas Dixon. Who’s asking? user personas and the mechanics of latent misalignment. _Advances in Neural Information Processing Systems_ , 37:125967– 126003, 2024. 

- [28] Luca Gioacchini, Marco Mellia, Idilio Drago, Alexander Delsanto, Giuseppe Siracusano, and Roberto Bifulco. Autopenbench: Benchmarking generative agents for penetration testing, 2024. URL https://arxiv.org/abs/2410.03225. 

- [29] Sergei Glazunov and Mark Brand. Project naptime: Evaluating offensive security capabilities of large language models. https://googleprojectzero.blogspot.com/ 2024/06/project-naptime.html, June 2024. Accessed: 2025-06-19. 

- [30] Google Threat Intelligence Group. Adversarial misuse of generative ai. https://cloud.google.com/blog/topics/threat-intelligence/adversarial-misusegenerative-ai, January 2025. Accessed: 2025-06-19. 

- [31] Jiawei Gu, Xuhui Jiang, Zhichao Shi, Hexiang Tan, Xuehao Zhai, Chengjin Xu, Wei Li, Yinghan Shen, Shengjie Ma, Honghao Liu, et al. A survey on llm-as-a-judge. _arXiv preprint arXiv:2411.15594_ , 2024. 

- [32] Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jerem Fox, and Daniel Ford. How we built our multi-agent research system. https://www. anthropic.com/engineering/built-multi-agent-research-system, June 2025. Accessed: 2025-06-21. 

- [33] Andreas Happe and Jürgen Cito. Getting pwn’d by ai: Penetration testing with large language models. In _Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering_ , pages 2082–2086, 2023. 

- [34] Andreas Happe and Jürgen Cito. Understanding hackers’ work: An empirical study of offensive security practitioners. In _Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering_ , ESEC/FSE ’23, page 1669–1680. ACM, November 2023. doi: 10.1145/3611643.3613900. URL http://dx.doi.org/10.1145/3611643.3613900. 

- [35] Andreas Happe and Jürgen Cito. Benchmarking practices in llm-driven offensive security: Testbeds, metrics, and experiment design, 2025. URL https://arxiv.org/ abs/2504.10112. 

- [36] Andreas Happe and Jürgen Cito. On the ethics of using llms for offensive security, 2025. URL https://arxiv.org/abs/2506.08693. 

- [37] Andreas Happe and Jürgen Cito. Can llms hack enterprise networks? autonomous assumed breach penetration-testing active directory networks, 2025. URL https://arxiv.org/abs/2502.04227. 

- [38] Andreas Happe, Aaron Kaplan, and Juergen Cito. Llms as hackers: Autonomous linux privilege escalation attacks. _arXiv preprint arXiv:2310.11409_ , 2024. 

- [39] Mohammed Hassanin and Nour Moustafa. A comprehensive overview of large language models (llms) for cyber defences: Opportunities and directions, 2024. URL https://arxiv.org/abs/2405.14487. 

- [40] Jia He, Mukund Rungta, David Koleczek, Arshdeep Sekhon, Franklin X Wang, and Sadid Hasan. Does prompt formatting have any impact on llm performance?, 2024. URL https://arxiv.org/abs/2411.10541. 

- [41] Sean Heelan. How i used o3 to find cve-2025-37899, a remote zeroday vulnerability in the linux kernel’s smb implementation. https://sean.heelan.io/2025/05/22/how-i-used-o3-to-find-cve-2025-37899-aremote-zeroday-vulnerability-in-the-linux-kernels-smb-implementation/, May 2025. Accessed: 2025-06-19. 

- [42] Oliver Azuara Herrera, Laura Ripani, and Eric Torres Ramirez. Ai and the increase of productivity and labor inequality in latin america: Potential impact of large language models on latin american workforce. 2024. 

- [43] Zhiyuan Hu, Chumin Liu, Xidong Feng, Yilun Zhao, See-Kiong Ng, Anh Tuan Luu, Junxian He, Pang Wei W Koh, and Bryan Hooi. Uncertainty of thoughts: Uncertainty-aware planning enhances information seeking in llms. _Advances in Neural Information Processing Systems_ , 37:24181–24215, 2024. 

- [44] Hakan Inan, Kartikeya Upasani, Jianfeng Chi, Rashi Rungta, Krithika Iyer, Yuning Mao, Michael Tontchev, Qing Hu, Brian Fuller, Davide Testuggine, et al. Llama guard: Llm-based input-output safeguard for human-ai conversations. _arXiv preprint arXiv:2312.06674_ , 2023. 

- [45] Civic Innovations. Ethics and algorithms. https://civic.io/2022/12/14/ethicsand-algorithms/, December 2022. Accessed: 2025-06-02. 

- [46] ISC2. 2024 isc2 cybersecurity workforce study. https://www.isc2.org/Insights/ 2024/10/ISC2-2024-Cybersecurity-Workforce-Study, October 2024. Accessed: 2025-06-13. 

- [47] Nidhal Jegham, Marwen Abdelatti, Lassad Elmoubarki, and Abdeltawab Hendawi. How hungry is ai? benchmarking energy, water, and carbon footprint of llm inference, 2025. URL https://arxiv.org/abs/2505.09598. 

- [48] Haolin Jin, Linghan Huang, Haipeng Cai, Jun Yan, Bo Li, and Huaming Chen. From llms to llm-based agents for software engineering: A survey of current, challenges and future, 2024. URL https://arxiv.org/abs/2408.02479. 

- [49] Zachary D Johnson. _Generation, Detection, and Evaluation of Role-play based Jailbreak attacks in Large Language Models_ . PhD thesis, Massachusetts Institute of Technology, 2024. 

- [50] Muhammad Zaeem Khan, Saleha Jamshed, Sadia Ahmad, Aleesha Zainab, Kaynat Khatib, Faria Bibi, Abdul Rehman, et al. Advances in llms with focus on reasoning, adaptability, efficiency and ethics. _arXiv preprint arXiv:2506.12365_ , 2025. 

- [51] Dezhang Kong, Shi Lin, Zhenhua Xu, Zhebo Wang, Minghao Li, Yufeng Li, Yilun Zhang, Zeyang Sha, Yuyuan Li, Changting Lin, Xun Wang, Xuan Liu, Muhammad Khurram Khan, Ningyu Zhang, Chaochao Chen, and Meng Han. A survey of llm-driven ai agent communication: Protocols, security risks, and defense countermeasures, 2025. URL https://arxiv.org/abs/2506.19676. 

- [52] He Kong, Die Hu, Jingguo Ge, Liangxiong Li, Tong Li, and Bingzhen Wu. Vulnbot: Autonomous penetration testing for a multi-agent collaborative framework. _arXiv preprint arXiv:2501.13411_ , 2025. 

- [53] Nataliya Kosmyna, Eugene Hauptmann, Ye Tong Yuan, Jessica Situ, Xian-Hao Liao, Ashly Vivian Beresnitzky, Iris Braunstein, and Pattie Maes. Your brain on chatgpt: Accumulation of cognitive debt when using an ai assistant for essay writing task, 2025. URL https://arxiv.org/abs/2506.08872. 

- [54] Elizabeth Koumpan<sup>1</sup> and Lynda McOwen. Revolutionizing talent: the path in 21st century workforce transformation. _Human Factors, Business Management and Society_ , 33(16):74, 2024. 

- [55] Swetha Krishnamoorthi and Jarad Carleton. Active directory holds the keys to your kingdom, but is it secure? https://www.frost.com/growth-opportunitynews/active-directory-holds-the-keys-to-your-kingdom-but-is-it-secure, March 2020. Accessed: 2025-06-02. 

- [56] Jonathan Kutasov, Yuqi Sun, Paul Colognese, Teun van der Weij, Linda Petrini, Chen Bo Calvin Zhang, AI Scale, John Hughes, Xiang Deng, Henry Sleight, et al. Shade-arena: Evaluating sabotage and monitoring in llm agents. 

On the Surprising Efficacy of LLMs for Penetration-Testing 

- [57] Philippe Laban, Hiroaki Hayashi, Yingbo Zhou, and Jennifer Neville. Llms get lost in multi-turn conversation. _arXiv preprint arXiv:2505.06120_ , 2025. 

- [58] Ken Lebedev, Alex Moix, and Jacob Klein. Operating multi-client influence networks across platforms. https://cdn.sanity.io/files/4zrzovbb/website/ 45bc6adf039848841ed9e47051fb1209d6bb2b26.pdf, April 2025. Accessed: 202506-19. 

- [59] Jinhyuk Lee, Anthony Chen, Zhuyun Dai, Dheeru Dua, Devendra Singh Sachan, Michael Boratko, Yi Luan, Sébastien M. R. Arnold, Vincent Perot, Siddharth Dalmia, Hexiang Hu, Xudong Lin, Panupong Pasupat, Aida Amini, Jeremy R. Cole, Sebastian Riedel, Iftekhar Naim, Ming-Wei Chang, and Kelvin Guu. Can long-context language models subsume retrieval, rag, sql, and more?, 2024. URL https://arxiv.org/abs/2406.13121. 

- [60] Glyph Lefkowitz. I think i’m done thinking about genai for now. https://blog. glyph.im/2025/06/i-think-im-done-thinking-about-genai-for-now.html, June 2025. Accessed: 2025-06-29. 

- [61] Xiaomin Li, Zhou Yu, Zhiwei Zhang, Xupeng Chen, Ziji Zhang, Yingying Zhuang, Narayanan Sadagopan, and Anurag Beniwal. When thinking fails: The pitfalls of reasoning for instruction-following in llms. _arXiv preprint arXiv:2505.11423_ , 2025. 

- [62] Zilong Lin, Jian Cui, Xiaojing Liao, and XiaoFeng Wang. Malla: Demystifying real-world large language model integrated malicious services. In _33rd USENIX Security Symposium (USENIX Security 24)_ , pages 4693–4710, 2024. 

- [63] Dongge Liu, Jonathan Metzman, and Oliver Chang. Ai-powered fuzzing: Breaking the bug hunting barrier. https://security.googleblog.com/2023/08/aipowered-fuzzing-breaking-bug-hunting.html, August 2023. Accessed: 2025-0619. 

- [64] Kamile˙ Lukošiut¯ e˙ and Adam Swanda. Llm cyber evaluations don’t capture real-world risk, 2025. URL https://arxiv.org/abs/2502.00072. 

- [65] Amir Lupovici. The dual-use security dilemma and the social construction of insecurity. _Contemporary Security Policy_ , 42(3):257–285, 2021. 

- [66] Aengus Lynch, Benjamin Wright, Caleb Larson, Kevin K. Troy, Stuart J. Ritchie, Sören Mindermann, Ethan Perez, and Evan Hubinger. Agentic misalignment: How llms could be an insider threat. _Anthropic Research_ , 2025. https://www.anthropic.com/research/agentic-misalignment. 

- [67] Pratyush Maini, Hengrui Jia, Nicolas Papernot, and Adam Dziedzic. Llm dataset inference: Did you train on my dataset? _Advances in Neural Information Processing Systems_ , 37:124069–124092, 2024. 

- [68] Andy Masley. Why using chatgpt is not bad for the environment - a cheat sheet. https://andymasley.substack.com/p/a-cheat-sheet-for-conversationsabout, April 2025. Accessed: 2025-06-23. 

- [69] Harindra S. Mavikumbure, Victor Cobilean, Chathurika S. Wickramasinghe, Devin Drake, and Milos Manic. Generative ai in cyber security of cyber physical systems: Benefits and threats. In _2024 16th International Conference on Human System Interaction (HSI)_ , pages 1–8, 2024. doi: 10.1109/HSI61632.2024.10613562. 

- [70] Meta. Llama prompt guard 2. https://www.llama.com/docs/model-cards-andprompt-formats/prompt-guard/, January 2025. Accessed: 2025-06-21. 

- [71] Suvir Mirchandani, Fei Xia, Pete Florence, Brian Ichter, Danny Driess, Montserrat Gonzalez Arenas, Kanishka Rao, Dorsa Sadigh, and Andy Zeng. Large language models as general pattern machines, 2023. URL https://arxiv.org/abs/ 2307.04721. 

- [72] Yisroel Mirsky, Ambra Demontis, Jaidip Kotak, Ram Shankar, Deng Gelei, Liu Yang, Xiangyu Zhang, Maura Pintor, Wenke Lee, Yuval Elovici, et al. The threat of offensive ai to organizations. _Computers & Security_ , 124:103006, 2023. 

- [73] Steve Morgan. Global ransomware damage costs predicted to exceed $275 billion by 2031. https://cybersecurityventures.com/global-ransomware-damage-costspredicted-to-reach-250-billion-usd-by-2031/, April 2025. Accessed: 2025-06-02. 

- [74] Farzad Nourmohammadzadeh Motlagh, Mehrdad Hajizadeh, Mehryar Majd, Pejman Najafi, Feng Cheng, and Christoph Meinel. Large language models in cybersecurity: State-of-the-art, 2024. URL https://arxiv.org/abs/2402.00891. 

- [75] Ben Nimmo and Michael Flossman. Influence and cyber operations: an update. https://cdn.openai.com/threat-intelligence-reports/influence-and-cyberoperations-an-update_October-2024.pdf, October 2024. Accessed: 2025-06-13. 

- [76] Ben Nimmo, Albert Zhang, Sophia Farquhar, and Kimo Murphy, Max Bumanglag. Disrupting malicious uses of ai: June 2025. https://openai.com/globalaffairs/disrupting-malicious-uses-of-ai-june-2025/, June 2025. Accessed: 202506-13. 

- [77] Ben Nimmo, Albert Zhang, Matthew Richard, and Nathaniel Hartley. Disrupting malicious uses of ai: February 2025. https://cdn.openai.com/threat-intelligencereports/disrupting-malicious-uses-of-our-models-february-2025-update.pdf, February 2025. Accessed: 2025-06-18. 

- [78] OpenAI. Introducting chatgpt. https://openai.com/index/chatgpt/, November 2022. Accessed: 2025-06-02. 

- [79] OpenAI. Introducing openai o1. https://openai.com/o1/, September 2024. Accessed: 2025-06-02. 

- [80] OpenAI. Disrupting malicious uses of ai by state-affiliated threat actors. https://openai.com/index/disrupting-malicious-uses-of-ai-by-stateaffiliated-threat-actors/, February 2024. Accessed: 2025-06-19. 

- [81] Ani Petrosyan. Annual share of organizations affected by ransomware attacks worldwide from 2018 to 2023. https://www.statista.com/statistics/204457/ businesses-ransomware-attack-rate/, November 2024. Accessed: 2025-06-13. 

- [82] Ivo Petrov, Jasper Dekoninck, Lyuben Baltadzhiev, Maria Drencheva, Kristian Minchev, Mislav Balunović, Nikola Jovanović, and Martin Vechev. Proof or bluff? evaluating llms on 2025 usa math olympiad. _arXiv preprint arXiv:2503.21934_ , 2025. 

- [83] Derry Pratama, Naufal Suryanto, Andro Aprila Adiputra, Thi-Thu-Huong Le, Ahmada Yusril Kadiptya, Muhammad Iqbal, and Howon Kim. Cipher: Cybersecurity intelligent penetration-testing helper for ethical researcher. _Sensors_ , 24 (21):6878, 2024. 

- [84] Thomas Ptacek. My ai skeptic friends are all nuts. https://fly.io/blog/youre-allnuts/, June 2025. Accessed: 2025-06-29. 

- [85] William G. Resh, Yi Ming, Xinyao Xia, Michael Overton, Gul Nisa Gürbüz, and Brandon De Breuhl. Complementarity, augmentation, or substitutivity? the impact of generative artificial intelligence on the u.s. federal workforce, 2025. URL https://arxiv.org/abs/2503.09637. 

- [86] Christian Schindler and Andreas Rausch. Llm-based design pattern detection, 2025. URL https://arxiv.org/abs/2502.18458. 

- [87] Saskia Laura Schröer, Giovanni Apruzzese, Soheil Human, Pavel Laskov, Hyrum S. Anderson, Edward W. N. Bernroider, Aurore Fass, Ben Nassi, Vera Rimmer, Fabio Roli, Samer Salam, Chi En Ashley Shen, Ali Sunyaev, Tim WadhwaBrown, Isabel Wagner, and Gang Wang. Sok: On the offensive potential of ai. In _2025 IEEE Conference on Secure and Trustworthy Machine Learning (SaTML)_ , pages 247–280, 2025. doi: 10.1109/SaTML64287.2025.00021. 

- [88] Minghao Shao, Boyuan Chen, Sofija Jancheska, Brendan Dolan-Gavitt, Siddharth Garg, Ramesh Karri, and Muhammad Shafique. An empirical evaluation of llms for solving offensive security challenges, 2024. URL https: //arxiv.org/abs/2402.11814. 

- [89] Yijia Shao, Humishka Zope, Yucheng Jiang, Jiaxin Pei, David Nguyen, Erik Brynjolfsson, and Diyi Yang. Future of work with ai agents: Auditing automation and augmentation potential across the u.s. workforce, 2025. URL https://arxiv. org/abs/2506.06576. 

- [90] Parshin Shojaee, Iman Mirzadeh, Keivan Alizadeh, Maxwell Horton, Samy Bengio, and Mehrdad Farajtabar. The illusion of thinking: Understanding the strengths and limitations of reasoning models via the lens of problem complexity. _arXiv preprint arXiv:2506.06941_ , 2025. 

- [91] Brian Singer, Keane Lucas, Lakshmi Adiga, Meghna Jain, Lujo Bauer, and Vyas Sekar. On the feasibility of using llms to execute multistage network attacks. _arXiv preprint arXiv:2501.16466_ , 2025. 

- [92] Robin Sommer and Vern Paxson. Outside the closed world: On using machine learning for network intrusion detection. In _2010 IEEE symposium on security and privacy_ , pages 305–316. IEEE, 2010. 

- [93] Rao Surapaneni, Miku Jha, Michael Vakoc, and Todd Segal. Announcing the agent2agent protocol (a2a). https://developers.googleblog.com/en/a2a-a-newera-of-agent-interoperability/, April 2025. Accessed: 2025-06-02. 

- [94] Amir Taubenfeld, Yaniv Dover, Roi Reichart, and Ariel Goldstein. Systematic biases in llm simulations of debates. _arXiv preprint arXiv:2402.04049_ , 2024. 

- [95] Big Sleep Team. From naptime to big sleep: Using large language models to catch vulnerabilities in real-world code. https://googleprojectzero.blogspot.com/2024/ 10/from-naptime-to-big-sleep.html, November 2024. Accessed: 2025-06-19. 

- [96] The New York Times. Can you choose an a.i. model that harms the planet less? https://www.nytimes.com/2025/06/19/climate/ai-emissions-chatbotaccuracy.html, June 2025. Accessed: 2025-06-21. 

- [97] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. Llama: Open and efficient foundation language models. _arXiv preprint arXiv:2302.13971_ , 2023. 

- [98] Valen Van. A new evolutionary law. _Evolutionary theory_ , 1:1, 1973. 

- [99] Vernor Vinge. _Rainbows End: A Novel With One Foot In The Future_ . Tor Books, 2007. 

- [100] Yixin Wan, George Pu, Jiao Sun, Aparna Garimella, Kai-Wei Chang, and Nanyun Peng. " kelly is a warm person, joseph is a role model": Gender biases in llmgenerated reference letters. _arXiv preprint arXiv:2310.09219_ , 2023. 

- [101] Li Wang, Xi Chen, XiangWen Deng, Hao Wen, MingKe You, WeiZhi Liu, Qi Li, and Jian Li. Prompt engineering in consistency and reliability with the evidencebased guideline for llms. _NPJ digital medicine_ , 7(1):41, 2024. 

- [102] Yifei Wang. The large language model (llm) paradox: Job creation and loss in the age of advanced ai. _Authorea Preprints_ , 2023. 

- [103] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. _Advances in neural information processing systems_ , 35:24824–24837, 2022. 

- [104] WhiteRabbitNeo. Whiterabbitneo. https://huggingface.co/WhiteRabbitNeo, February 2024. Accessed: 2025-06-02. 

- [105] Simon Willison. Coding agents. https://simonwillison.net/2025/Jun/18/codingagents/, June 2025. Accessed: 2025-06-21. 

Andreas Happe and Jürgen Cito 

- [106] Simon Willison. The lethal trifecta for ai agents: private data, untrusted content, and external communication. https://simonwillison.net/2025/Jun/16/the-lethaltrifecta/, June 2025. Accessed: 2025-06-21. 

- [107] Hanxiang Xu, Shenao Wang, Ningke Li, Kailong Wang, Yanjie Zhao, Kai Chen, Ting Yu, Yang Liu, and Haoyu Wang. Large language models for cyber security: A systematic literature review, 2024. URL https://arxiv.org/abs/2405.04760. 

- [108] Jiacen Xu, Jack W Stokes, Geoff McDonald, Xuesong Bai, David Marshall, Siyue Wang, Adith Swaminathan, and Zhou Li. Autoattacker: A large language model guided system to implement automatic cyber-attacks. _arXiv preprint arXiv:2403.01038_ , 2024. 

- [109] Rongwu Xu, Xiaojian Li, Shuo Chen, and Wei Xu. Nuclear deployed: Analyzing catastrophic risks in decision-making of autonomous llm agents, 2025. URL https://arxiv.org/abs/2502.11355. 

- [110] Wen Xu, Juanru Li, Junliang Shu, Wenbo Yang, Tianyi Xie, Yuanyuan Zhang, and Dawu Gu. From collision to exploitation: Unleashing use-after-free vulnerabilities in linux kernel. In _Proceedings of the 22nd ACM SIGSAC Conference on Computer and Communications Security_ , pages 414–425, 2015. 

- [111] Maria Yagoda. Airline held liable for its chatbot giving passenger bad advice - what this means for travellers. https://www.bbc.com/travel/article/20240222- 

air-canada-chatbot-misinformation-what-travellers-should-know, February 2024. Accessed: 2025-06-21. 

- [112] Fanjia Yan, Huanzhi Mao, Charlie Cheng-Jie Ji, Tianjun Zhang, Shishir G. Patil, Ion Stoica, and Joseph E. Gonzalez. Berkeley function calling leaderboard. https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_ leaderboard.html, 2024. 

- [113] Yifan Yao, Jinhao Duan, Kaidi Xu, Yuanfang Cai, Zhibo Sun, and Yue Zhang. A survey on large language model (llm) security and privacy: The good, the bad, and the ugly. _High-Confidence Computing_ , 4(2):100211, 2024. ISSN 2667-2952. doi: https://doi.org/10.1016/j.hcc.2024.100211. URL https://www.sciencedirect. com/science/article/pii/S266729522400014X. 

- [114] Yagmur Yigit, William J Buchanan, Madjid G Tehrani, and Leandros Maglaras. Review of generative ai methods in cybersecurity, 2024. URL https://arxiv.org/ abs/2403.08701. 

- [115] Jie Zhang, Haoyu Bu, Hui Wen, Yu Chen, Lun Li, and Hongsong Zhu. When llms meet cybersecurity: A systematic literature review, 2024. URL https: //arxiv.org/abs/2405.03644. 

- [116] Yifei Zhou, Sergey Levine, Jason Weston, Xian Li, and Sainbayar Sukhbaatar. Self-challenging language model agents. _arXiv preprint arXiv:2506.01716_ , 2025. 

