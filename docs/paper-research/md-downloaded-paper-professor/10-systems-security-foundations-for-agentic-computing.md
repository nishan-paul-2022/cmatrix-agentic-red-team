# Systems Security Foundations for Agentic Computing 

Mihai Christodorescu<sup>1</sup> Earlence Fernandes<sup>2</sup> Ashish Hooda<sup>1</sup> Somesh Jha<sup>1</sup><sup>_,_3</sup> Johann Rehberger<sup>4</sup> Kamalika Chaudhuri<sup>5</sup> Xiaohan Fu<sup>2</sup><sup>_,_6</sup> Khawaja Shams<sup>1</sup> Guy Amir<sup>7</sup> Jihye Choi<sup>3</sup> Sarthak Choudhary<sup>3</sup> Nils Palumbo<sup>3</sup> Andrey Labunets<sup>2</sup> Nishit V. Pandya<sup>2</sup> 

1Google 2University of California San Diego 3University of Wisconsin–Madison 4EmbraceTheRed 5FAIR at Meta 6Gray Swan AI 7Cornell University 

#### **Abstract** 

In recent years, _agentic artificial intelligence (AI)_ systems are becoming increasingly widespread. 

These systems allow agents to use various _tools_ , such as web browsers, compilers, and more. However, despite their popularity, agentic AI systems also introduce a myriad of security concerns, due to their constant interaction with third-party servers. For example, a malicious adversary can cause data exfiltration by executing prompt injection attacks, as well as other unwarranted behavior. These security concerns have recently motivated researchers to improve the safety and reliability of agentic systems. However, most of the literature on this topic is from the AI standpoint and lacks the system-security perspective and guarantees. In this work, we begin bridging this gap and present an analysis through the lens of classic cybersecurity research. Specifically, motivated by decades of progress in this domain, we identify short- and long-term research problems in agentic AI safety by examining end-to-end security properties of _entire systems_ , rather than standalone AI models running in isolation. Our key goal is to examine where research challenges arise when applying traditional security principles in the context of AI agents and, as a secondary goal, distill these ideas for AI practitioners. Furthermore, we extensively cover 11 case studies of real-world attacks on agentic systems, as well as define a series of new research problems that are specific to this important domain. 

## **1 Introduction** 

Agentic AI systems have become widespread: by being given access to tools such as web browsers, compilers, and more, AI agents, and especially those based on large language models (LLM), are becoming increasingly powerful. However, this comes at a cost: access to third party tools and external servers introduces a wide range of security challenges that must be addressed in order to safely and reliably deploy such systems in a trustworthy manner. Previous literature has raised the important topic of agentic AI security, however, most of the this literature is written from an AI perspective, and does not leverage the extensive research accumulating through dozens of years of classic security studies. In this Systematization of Knowledge (SoK) paper, we begin bridging this gap, and explore how to build upon well-studied concepts and practices in computer-security research to advance the security of agentic computing. We focus on key similarities and differences between both domains, and distill lessons, open research problems and recommendations on how the two fields can co-operate to build a foundation for secure agentic computing. 

_Agentic computing_ refers to AI models that interact with computer systems and services on behalf of human users by repeatedly calling tools in a loop [100]. The user specifies a task in natural language, and the AI model (typically a large language or vision model) completes it by iteratively invoking tools, such as desktop UIs, web browsers, or mobile operating systems. For instance, a user might ask an agent to _find mentions of a particular event in recent emails, summarize what happened, and save the summary to a text file_ . Such a request can trigger tools calls including email search, retrieval, and writes to local storage. Recently, 

1 

there is also a trend in promoting uniform standards and protocols for defining various agentic tool calls, e.g., REST or Model Context Protocol (MCP) [58]. 

Current efforts to secure agentic systems span multiple layers of defense [8], including model-level, systemlevel, and user-level approaches. At the _model level_ , various methods aim to make the agent more resilient to attacks by hardening approaches, often described as alignment techniques [18, 96, 62]. At the _system level_ , an increasingly prominent line of work treats the model as an untrusted (or at best, probabilistic) component and instead enforces invariants through isolation and mediation: restricting the agent’s action space, sandboxing tool execution, structuring tool interfaces, and separating untrusted data from control flow via explicit trust boundaries and guardrails [8, 110]. Finally, at the _user level_ , practical deployments commonly incorporate governance mechanisms such as explicit approvals/confirmations for sensitive actions, permission scoping, and audit/monitoring to reduce the blast radius of failures and support incident response [8]. 

From a computer-security perspective, this emerging taxonomy mirrors a classic _defense-in-depth_ lesson: hardening a component is valuable, but is rarely sufficient on its own. Robust systems rely on _deterministic_ enforcement points (e.g., access control, isolation, and provenance boundaries) placed at multiple layers of abstraction (hardware, hypervisors, operating systems, user-space frameworks, applications, and networks), to increase the attacker’s burden while preserving performance and functionality [82, 4]. In agentic settings, however, deciding _where_ to place such enforcement points is less straightforward, because the model simultaneously (i) processes untrusted content and (ii) synthesizes actions and tool calls on the fly. 

This tension is aggravated further due to modern agents being vulnerable to inference-time attacks that can steer behavior in arbitrary ways [115, 31, 91, 39]. As with earlier waves of adversarial ML, purely behavioral defenses that rely on the model to reliably identify and ignore malicious instructions can remain brittle under adaptive attackers [60, 7, 65]. Moreover, in the LLM era, attackers often need not have deep system expertise: simple prompting can be enough to induce harmful tool use or policy violations in real-world deployments [39, 70, 79, 74, 80]. Therefore, to make foundational and practical progress, the fields of computer security and AI agent security need to co-operate: combining model-level robustness with principled system-level and user-level guardrails grounded in decades of security research. 

**Summary of Findings.** Computer security makes progress by articulating clear security invariants and then enforcing them via layered, largely deterministic mechanisms and design principles (e.g., least privilege, complete mediation, separation of privilege) [82, 4]. When we attempt to apply these ideas to agentic systems, we encounter several challenges that arise. We use these frictions to organize the report and to surface concrete research questions. Furthermore, each of these challenges also poses interesting research avenues for long-term future work. 

_<u>(1)</u> Probabilistic and Opaque TCB._ A classic systems-security move is to minimize a _trusted computing base (TCB)_ that deterministically enforces an invariant (e.g., preventing execution from non-executable memory regions to reduce the impact of memory-corruption bugs). In many _AI-based_ systems, including agentic ones, the model itself becomes a central part of the TCB, yet its behavior is fundamentally probabilistic and often not fully interpretable. If we “ _train the model to never do X_ ”, that guarantee is inherently conditional and statistical: it holds with some probability that depends on the input distribution and the surrounding context rather than as an absolute property of the system. The resulting challenge is to build defenses with meaningful assurance guarantees despite relying on a probabilistic/opaque component in the TCB. 

_<u>(2)</u> Dynamic Security Policies._ A security policy specifies what an untrusted program is allowed to do and is typically authored by a developer or inferred from code analysis. However, in agentic settings, both these assumptions break down: (i) there may be no developer intent beyond the end-user’s natural-language request, and (ii) there is no fixed program to analyze, since the agent effectively synthesizes many programs on the fly. Inferring or synthesizing a policy from a task description is difficult because tasks are often underspecified, and using the agent’s full context window for precise policy inference is nontrivial due to untrusted external content. 

_<u>(3)</u> Fuzzy Security Boundary._ Deterministic guardrails are most effective when enforced at an interface that exposes the right semantic information (e.g., Android permissions at the boundary between apps and protected services). In many agentic stacks, however, the boundary between “decision” and “action” is blurry: the model may directly emit tool calls (sometimes via low-level UI actions) without stable abstraction layers that cleanly separate intent from mechanism. As a result, policies written at too low a level (clicks/keystrokes) 

2 

become brittle, while policies written at too high a level may lack enforceable grounding. This can also be viewed as a manifestation of the classic _semantic gap_ problem [44, 29, 89]. 

_<u>(4)</u> Dynamic Instruction Following._ Prompt injections are a key security problem to solve in agentic systems, but the underlying mechanism of dynamically updating agentic instructions is oftentimes necessary for functionality and thus not necessarily malicious. For example, tool documentation does affect an agent’s behavior (by definition because the agent has to learn how to use the tool!). The challenge here is defining when prompt injections are harmful [26] and when they are useful and then distinguishing the two. The analog in computer security is dynamic code loading–a very challenging problem that remains difficult to address today. 

**Scope and organization of this report.** There has been a range of recent and contemporaneous writings on the general theme of applying computer security ideas to agentic computing [8, 110]. The key distinction of this report is that we take a deep-dive on the technical challenges that arise when applying concrete security principles and articulate open research problems based on those technical challenges. The paper starts out with a discussion of security principles applied to agentic settings and the challenges that arise forthwith (Section 2). Section 3 presents 11 case studies of real attacks on agentic systems with three goals in mind: (1) to showcase how real attacks are carried out by adversaries without the need for sophisticated technical tools to execute them; (2) to highlight the corresponding security principle(s) that were violated; and (3) to outline concrete security mechanisms needed to stop each such attack. We discuss the current practices for mitigating these threats in Section 4 and summarize the open research problems in Section 5. 

## **2 Challenges in Applying Security Engineering to Agentic Computing** 

### **2.1 The TCB is Probabilistic** 

The _Trusted Computing Base (TCB)_ is a component or assumption that cannot be influenced by the attacker. TCB is an invariant which is basis of security, such as the no-execute or NX bit in hardware (e.g. data put in region with NX bit set can never be executed or interpreted as instruction). 

In traditional systems, the TCB consists of deterministic components such as hardware, OS kernels, reference monitors that behave predictably. This determinism enables security guarantees: W _⊕_ X memory protection consistently prevents execution of writable memory, and Content Security Policy deterministically blocks unauthorized scripts. 

In contrast, the TCB in agentic systems is built on LLMs that do not guarantee predictable, or even deterministic behavior—the same prompt can yield different outputs due to sampling randomness. Thus a fundamental challenge in realizing this traditional security principle in agentic systems is the TCB being probabilistic or non-deterministic (e.g. imagine whether we could build a memory safety defense on top of a probabilistic NX bit). This probabilistic nature undermines traditional security principles in three ways. First, a probabilistic reference monitor might correctly deny unauthorized access 99% of the time, but the remaining 1% can be exploited. Second, unlike traditional systems where security properties can be formally verified, we cannot prove an LLM will always enforce policies correctly. Third, LLMs operate in continuous representation spaces, making them vulnerable to adversarial examples. Unlike traditional systems that have discrete instruction sets with clear boundaries, attackers can use various search and optimization techniques to efficiently find inputs that appear benign but cause policy violations. 

To build secure systems on probabilistic LLMs, we must leverage external deterministic information to disambiguate LLM decisions. An example of a system takes this approach is SkillFence [41]. It uses deterministic signals from the user’s browsing history and installed apps to correct any mistakes made by a voice assistant’s language understanding. However, we believe that building provable defenses on probabilistic and non-deterministic TCB is a challenging—perhaps impossible—task. 

### **2.2 The Security Policy Is Dynamic and Task-Specific** 

In traditional computer security, a security policy governs the privilege of a piece of code. For example, in Android, the OS developers provide a set of permissions that an app developer can select from. The key aspect 

3 

is that the app is generally single-purpose, built to perform a fixed set of tasks, and thus, the app developer can create a security policy and present it to the user at the time of installation. Furthermore, one can analyze the app’s code to determine why certain permissions are needed and whether they are necessary for the app’s stated functionality (thus allowing for analyzing compliance with the principle of Least Privilege). 

In agentic systems, there is no app developer and there is no app. Rather, there is only a natural language task specification that can change over time. Thus, the privilege of the agent is dynamic and needs to be predicted from the task description in a secure manner. For example, consider a simple developer task assigned to a browser agent: 

#### comment on GitLab issue 745 that we’re done 

From this task description, the security policy would need to incorporate the following components: 

   1. The agent can navigate to GitLab issue 745; 

   2. The agent should have write access to the comment box; 

   3. The agent should not have access to anything else in GitLab or the user’s session in the browser. 

- This least-privilege security policy is task-specific and only known once the task is specified. Continuing this example, let’s say that the user specifies a follow-up task for the agent: 

summarize issue 745 for me 

Now, how should the privilege of the agent change to solve the new task description? One option is to reset the agent’s context and redo the policy prediction. This approach is secure but can result in lost utility because the agent’s context is erased. Thus, how can we evolve the security policy in a secure manner while there is untrusted data in the context? An additional problem for AI agents is that privacy consent is fundamentally at odds with agency [93], as finding and enforcing the right policy for an AI agent each time requires resolving the trade-off between providing more access for better task performance and restricting access as per least-privilege principle. We believe that the key lies in creating policy languages that are amenable to formalized reasoning so that when new policies are predicted and added to the existing set, we can reason about how the new policies change the overall privilege level of the agent. 

Extrapolating from this example, we posit the following research challenges: (1) _domain-specific policy languages_ for different types of agents that are amenable to formal analysis and reasoning; (2) _dynamic policy prediction_ in these DSLs given natural language tasks, from trusted and untrusted context. 

### **2.3 The Security Boundary Is Fuzzy** 

Identifying the right abstraction at which security policies are enforced is crucial to upholding the complete mediation design principle. In traditional computer systems, we have layered architectures (Hardware— Operating System (OS) Kernel—Process—Network) that offer different levels of abstraction for enforcing security policies. For example, the process-kernel interface allows for SELinux-style MAC policies and the App-Runtime interface allows for higher-level permissions that we see in systems like Android. Agentic systems lack these layers. Rather, they directly use tools given a natural language prompt. There are no layers in between. Thus, enforcing a security policy at the final layer of tool-calls can lead to incomplete or ineffective mediation (i.e., there can be gaps). The key research challenge in applying the complete mediation principle is identifying or creating the right abstraction at which a security policy can be enforced. 

We discuss two recent efforts that have started investigating these challenges along two dimensions: (1) creating an abstraction over which security can be enforced; (2) finding the right level of abstraction in an existing agent design. 

_CaMeL_ [25] and _FIDES_ [23] introduce an agent design that exemplifies the “solution as code” approach. To solve a task, the agent first generates code that, when executed, would solve the task specified in natural language. Notice that this introduces a new layer of abstraction: the code needed to solve the task. At that point, one can analyze the code using standard security analysis methods (control and data flows) to 

4 

determine whether the agent’s plan is aligned with the user’s goal. A key assumption in this design is that the agent has access to a set of semantically-meaningful tools. One of the key future research questions here is creating an appropriate intermediate representation for agent plans that is amenable to static and dynamic analysis. 

_ceLLMate_ [54] introduces a sandboxing framework for browser agents. The key challenge is identifying the right abstraction to enforce security policies within existing infrastructure. Browser agents, as currently built, have access to low-level UI manipulation tools (e.g., clicks and keystrokes), and thus, it is non-sensical to write policies at that level. The key insight to address this semantic gap is realizing that no matter what UI manipulations the agents perform, HTTP-level messages capture those actions in semantically meaningful ways. Therefore, ceLLMate policies are specified and enforced at the HTTP level, in co-operation with information supplied by webserver developers. One of the key future research challenges here is automatically predicting policies at the level of HTTP messages using natural language task descriptions as input. 

### **2.4 Dynamic Instruction Following** 

Prompt injection, more specifically indirect prompt injection, is often seen as a vulnerability of current AI-based systems. But more generally, prompt injection can be seen as a manifestation of a new class of functionality in AI, where the agent can adjust its task based on _new instructions_ in its context. For example, using the GitLab task in Section 2.2, the agent may start with the aforementioned summarization request prompt, subsequently visit the GitLab page for that issue, identify that it depends on another issue, and decide to summarize both to give the user a comprehensive answer. The distinction between (undesirable) prompt injection and (desirable) contextual task adjustment rests on the provenance of the input that triggered the change and the scope of the change. 

From the security perspective, dynamic instruction following, which can be realized as prompt injection (benign or malicious), has a parallel in non-AI systems in the form of dynamic code loading. This is common among applications that support plugins or extensions (e.g., OS kernels, IDEs, web browsers) and has long posed significant challenges in terms of security. The typical solution is to introduce another security boundary between the main TCB and the dynamically loaded code and to use permissions or sandboxing to limit the access afforded to the new code. For example, web pages (probably the most popular platform for dynamic code loading, as each page load and subsequent interaction can potentially load additional Javascript code as web-page scripts) are secured through a number of sandboxes and associated security policies: Content Security Policy determines which third-party scripts can be loaded, Same-Origin Policy restricts the web page data accessible to a third-party script, <iframe> sandboxing isolates third-party content, and Subresource Integrity ensures that third-party scripts have not been modified from the time it was approved by the developer. Other systems, such as Android, actively discourage dynamic code loading [34]. 

In the agentic space, dynamic instruction following is a key feature to steer task execution. For example, MCP descriptions are instructions brought in externally, as are Anthropic’s Claude Skills [6] and OpenClaw’s ClawHub add-ons [64]. Yet current agentic systems lack both of the components that provide security in web page dynamic code loading. First, information about the source (or provenance) of an instruction given to the agent is hard to assess (in contrast to the source of web-page scripts, most commonly loaded through explicit URLs over HTTPS). Second, sandboxing in the agent context is unavailable or probabilistic at best via mechanisms such as Instruction Hierarchy [96]. An additional challenge to further drive the contrast with the web-page security model is that web pages are designed by a website owner, who is in charge of determining which code to include on the page and indirectly which code to dynamically load at some later time on the page. Agents are often given underspecified instructions and are expected to refine them with additional instructions discovered while working on the task at hand. This is a highly desirable functionality of agentic systems (not having to fully specify the task completely in the first prompt), but one for which security mechanisms are not readily available. 

## **3 Attacks on Agentic Systems: Case Studies** 

We present here 11 attacks against agentic systems to illustrate the variety of types of vulnerabilities that occur in practice. For each attack we also highlight the security principle(s) that were violated and the 

5 

Table 1: Attacks of Section 3 and violated security principles. 

|**Attack**|**Least Privilege**|**TCB Tamper Resistance**|**Complete Mediation**|**Secure Information Flow**|**Human Weak Link**|
|---|---|---|---|---|---|
|Microsoft Copilot Exfltration|✓|–|✓|✓|–|
|Devin AI Exposed Ports|✓|–|–|✓|–|
|ChatGPT Long-Term Memory SpAIware|–|✓|–|✓|–|
|Amp AI Code Arbitrary Command Execution|–|✓|–|✓|–|
|DeepSeek AI Account Takeover|–|–|✓|✓|–|
|Terminal DiLLMa|–|–|✓|✓|–|
|ChatGPT Operator Prompt Injection|–|–|–|✓|✓|
|Devin AI Secret Leaks|✓|–|–|✓|–|
|Cursor AgentFlayer|✓|–|–|✓|–|
|Claude Code Exfltration|✓|–|–|✓|–|
|AI ClickFix|✓|–|–|✓|✓|



potential defenses. For a refresher on the security principles we reference here, please see Appendix B. A summary of these attacks and corresponding violated security principles is shown in Table 1. 

**Microsoft Copilot Exfiltration.** A vulnerability in Microsoft 365 Copilot allowed attackers to steal private user data, such as emails, by sending a malicious message containing a hidden prompt [73]. When a user interacted with this message (asking, for example, for a summary) via Copilot, a prompt-injection attack was triggered, letting the attacker take control of the agent. The compromised Copilot was then instructed to find sensitive information, encode it using “ASCII smuggling,” and embed it into a seemingly harmless hyperlink. When the user clicked this link, their data was secretly sent to the attacker. 

<u>Violation:</u> This attack violates the security principles of _Least Privilege_ , _Complete Mediation_ , and _Secure Information Flow_ , as Copilot automatically performed unexpected actions sourced from a document of unknown origin (like searching for and exfiltrating data) without verifying each step with the user, failing to check that the AI’s operations were fully authorized. This vulnerability is similar to that of traditional code injection after a buffer overflow, where an adversarially crafted input allows the attacker to run code of their choice inside the victim process, coupled with insufficient access control. 

<u>Defense:</u> Implement strict output sanitization to detect and block data ex-filtration channels like “ASCII smuggling” in generated hyperlinks. Require human approval whenever the agent accesses sensitive data. Because the TCB is probabilistic (the CoPilot LLM is part of the TCB, Section 2.1) and the security boundary for Internet access is fuzzy (the set of safe URLs cannot be practically enumerated in full, Section 2.3), these defenses provide only incomplete security guarantees and will need to be supplemented with mechanisms for separating instructions and data (Section 5.1) and for least-privilege access control (Section 5.2). 

6 

**Devin AI Exposed Ports.** The AI agent Devin comes with tool called expose_port, meant for testing, that was abused through an indirect prompt injection attack [80]. An attacker hosted a malicious prompt on a website that, when visited by Devin, hijacked the agent. The compromised AI then started a local web server, exposing its entire file system, and used the expose_port tool to make this server publicly accessible online. The resulting URL was then sent to the attacker, granting them full access to Devin’s files. 

<u>Violation:</u> This vulnerability violates the principles of Least Privilege (as the expose_port tool had excessive permissions, allowing it to expose any port, including one with access to the entire file system, rather than being restricted to only what was necessary for its intended function) and of Security Information Flow (as the agent accepted instructions received from an unknown origin). This vulnerability is similar to that of traditional code injection after a buffer overflow. 

<u>Defense:</u> A potential solution is to restrict the expose_port tool to a predefined safe range of ports by default and configurable only from outside the agent’s sandbox. However, such a safe list might be prompt specific and thus presents the challenge of a dynamic, task-specific security policy (Section 2.2). A strong defense will need controls that guarantee minimum-privilege access, an open problem for agentic systems (see Section 5.2). 

**ChatGPT Long-Term Memory SpAIware.** A vulnerability in the ChatGPT macOS app allowed for persistent data exfiltration by injecting malicious instructions into the app’s “Memories” feature [74]. This was accomplished through a prompt injection in an untrusted document or website, which caused the application to continuously send all of the user’s conversations to an attacker-controlled server. The data was exfiltrated by rendering an invisible image that included the user’s data as a parameter in the image URL. 

<u>Violation:</u> This attack violates the principles of _Trusted Computing Base (TCB) Tamper Resistance_ and Secure Information Flow because it stores data from an untrusted origin into the Memories storage (presumably trusted by the agent) and creates an unauthorized channel for sensitive information to be leaked from the application to an external, malicious server. In addition to the similarity with code injection after buffer overflow, this vulnerability also allows the attacker to achieve persistent control, which is one of the fundamental issues with dynamic code loading (Section 2.4). 

<u>Defense:</u> All data entering “Memories” should be sanitized before storage or, at a minimum, passed through a human-in-the-loop check (as other agents do by _suggesting_ memories to the user instead of automatically persisting them). Additionally, the app’s rendering layer should prevent automatic loading of remote sources from untrusted origins. The deployed fix performs an additional check via a url_safe tool to control which URLs ChatGPT will connect to, in turn making exfiltration more difficult.. We note that sanitization for untyped data (such as natural-language text) and determining the trust level of a remote Internet resource (such as a web page) both often rely on classifiers, raising concerns of building on a probabilistic TCB (Section 2.1). 

**Amp AI Code Arbitrary Command Execution.** Sourcegraph’s Amp AI coding agent allowed for arbitrary command execution by exploiting the agent’s ability to modify its own configuration file [77]. Through a prompt injection attack, an adversary instructed the AI to alter its settings.json file, either by adding malicious commands to an allowlist for automatic execution or by adding an attacker-controlled server to the configuration, both of which led to running unauthorized code on the developer’s machine. 

<u>Violation:</u> This attack fundamentally violates the principles of TCB Tamper Resistance (as the AI agent, a component of the trusted system, was able to modify its own security-critical configuration files, thereby 

7 


![](docs/paper-research/md-downloaded-paper-professor/images/10-systems-security-foundations-for-agentic-computing.pdf-0008-00.png)


<!-- Start of picture text -->
Figure 1: OpenAI Operator exploit flow: a prompt-injected GitHub issues page can steer the<br><!-- End of picture text -->

Figure 1: OpenAI Operator exploit flow: a prompt-injected GitHub issues page can steer the agent into an authenticated session (e.g., Gmail) and onward to an attacker-controlled site, resulting in personally identifiable information (PII) exfiltration. 

compromising the integrity of the system’s security policies) and Secure Information Flow. In addition to the similarity with code injection after buffer overflow, this vulnerability has parallels with privilege escalation, where the attacker can modify the security configuration of their environment to gain higher access. 

<u>Defense:</u> Such systems should enforce immutability on security-critical configuration files (like settings. json) so the agent cannot modify its own execution environment. Any changes to these configurations should require human approval. These defenses highlight the challenges of fuzzy security boundaries (Section 2.3) and dynamic code loading (Section 2.4), for which agentic systems have no guaranteed solutions (see Sections 5.2 and 5.3 for further discussion on these open problems). 

**DeepSeek AI Account Takeover.** A vulnerability in the DeepSeek AI platform led to a full account takeover by chaining a prompt injection with a Cross-Site Scripting (XSS) exploit [71]. An attacker uploaded a malicious text file containing a base64 encoded JavaScript payload, which, when processed by a victim’s account, instructed the AI to decode and execute the script in the victim’s browser, stealing the userToken from localStorage and sending it to the attacker. 

<u>Violation:</u> This attack violates the principles of Secure Information Flow (as it established an unauthorized covert channel to leak a sensitive session token from the user’s browser to an external, malicious endpoint, completely bypassing the platform’s intended data handling and security boundaries) and _Complete Mediation_ (as the agent processed encoded data meant to bypass input filtering). Chained code injections are often used in traditional exploits to complete an attack. 

<u>Defense:</u> Ensure a strict separation between data (uploaded text files) and executable web code. The fuzzy security boundary (Section 2.3) coupled with the need to allow for some flexibility in using external data as prompts (a form of dynamic code loading, Section 2.4) makes it challenging to secure the agentic system end-to-end when no good mechanisms for separating instruction and data are available (see Section 5.1). 

**Terminal DiLLMa.** The “Terminal DiLLMa” attack hijacked a user’s terminal through LLM-powered command-line tools by using prompt injection to generate malicious ANSI escape sequences [75]. When a compromised tool, such as the proof-of-concept dillma.py, processed a malicious prompt, it output specially crafted ANSI codes that the terminal emulator executes, leading to unauthorized actions like clipboard 

8 

manipulation or data exfiltration via DNS requests. 

<u>Violation:</u> This attack highlights a violation of the Complete Mediation and Secure Information Flow principles. Insufficient or incorrect input validation and sanitization result in incompletely validated inputs which then trigger unwanted software behaviors, as occurred here. 

<u>Defense:</u> Implement a sanitization layer for agent output for dangerous ANSI escape sequences before they reach the terminal emulator. This becomes challenging as highlighted in Section 2.3 when different types of outputs can be created (e.g., with ANSI escape codes, with Markdown formatting, with HTML tag and Javascript) and can be displayed in various settings (e.g., terminals, browsers, text viewers). 

**ChatGPT Operator Prompt Injection.** A prompt injection attack on the ChatGPT Operator led to the exfiltration of a user’s personally identifiable information (PII) by manipulating the agent through a malicious GitHub issue [78]. The attack began when the operator was prompted to investigate a GitHub issue containing a malicious combine tool, which, when clicked, redirected the agent to an attacker-controlled webpage. The compromised operator was then instructed to navigate to a settings page on another website (where the operator was already authenticated), to copy sensitive PII, and to paste it into a textbox on the attacker’s page, where it was immediately captured (see Figure 1). 

<u>Violation:</u> This exploit is a clear violation of Secure Information Flow, as the system fails to validate the origin of the request to perform various actions (navigating, clicking, copying, pasting) to ensure they are authorized by the user after the initial, legitimate prompt was given. 

<u>Defense:</u> We note that human confirmation on every navigation event is not a desirable mechanism, since it shifts the burden to the user who may not have the expertise or the patience to reason through a fuzzy security boundary (Section 2.3). A better approach is to employ sandboxing or information-flow controls but as we point in Section 5.3 building such a mechanism for ML models remains an open problem. 

**Devin AI Secret Leaks.** The Devin AI agent was manipulated via indirect prompt injection to leak sensitive environment variables and secrets [81]. An attacker hosted a malicious prompt on a platform like GitHub, and when Devin was instructed to interact with it, the agent was tricked into using its native tools, such as the shell tool or the browsing tool, to exfiltrate data by sending it to an attacker-controlled server via commands like curl or by embedding it in a URL. 

<u>Violation:</u> This vulnerability represents a failure of Secure Information Flow and Least Privilege principles, as it creates multiple unauthorized channels by unexpectedly executing tools (shell commands, browser navigation, markdown image rendering) for confidential data to be transmitted out of the agent’s secure environment. 

<u>Defense:</u> Sandbox the agent to prevent tools like curl from contacting arbitrary, attacker-controlled servers. Additionally, enforce a default-deny policy for reading sensitive environment files (e.g., .env) unless specifically authorized for the current task. Defining a precise, least-privilege security policy for each task is an open challenge (Section 5.2). 

**Cursor AgentFlayer.** A malicious Jira ticket was used to trick the AI-powered code editor, Cursor, into exfiltrating sensitive information [85]. The attack created a Jira ticket with a prompt that, while seemingly harmless, caused Cursor to leak repository secrets or even personal files, like Amazon Web Services (AWS) credentials, from the user’s local system. The author shows how simple changes in wording bypassed the AI’s built-in security measures. This exploit required, as a prerequisite, that a developer disabled the 

9 

human-in-the-loop validation for the Jira MCP server or entirely enabled Cursor’s Auto Run mode (a form of YOLO mode for agents where confirmation prompts are minimized, often used in order to give the agents more freedom without involving the developer). 

<u>Violation:</u> This exploit violates the Secure Information Flow, Least Privilege, Complete Mediation, and TCB Tamper Resistance principles. 

<u>Defense:</u> Implement fine-grained file system permissions, restricting the agent to only the specific repositories or directories it is currently working on. However, the set of required permissions might depend on the prompt as overly restrictive permissions could impact utility. Similar to the preceding attack, a defense that guarantees least-privilege access as defined in Section 5.2 is desirable but hard to realize practically. 

**Claude Code Exfiltration.** Claude Code enabled data exfiltration via DNS requests [79] (Figure 2 in Appendix A). The attack leveraged indirect prompt injection, where a malicious prompt hidden in a code file instructed Claude Code to read sensitive information, such as API keys from a .env file, and then used an allow-listed command like ping to send that data to an attacker-controlled server as part of a DNS query (via the inherent nslookup that occurs). The result was the leakage of sensitive information from the developer’s machine without consent. Claude code had implemented human approval for many shell commands that could send data to unknown domains, but mistakenly allowed ping to execute without human approval. 

<u>Violation:</u> This violates secure information flow because the environment file contents leaked to an unknown domain. It also violated least privilege because the agent may not necessarily need uniform access to all shell commands with the ability to supply unrestricted arguments at all points in time. 

<u>Defense:</u> The input arguments to tools such as ping and nslookup should be restricted to trusted or user-approved domains. Information-flow control for ML models (Section 5.3) and model architectures with built-in security controls (Section 5.5) could address such attacks that chain multiple exploits. 

**AI ClickFix.** Traditional social-engineering techniques were adapted to use against computer-use agents, in an attack called “AI ClickFix” [76]. The attack involved tricking an AI agent into executing malicious code by presenting it with a series of instructions on a webpage. For instance, the agent was prompted to click a button which secretly copied a malicious command to the clipboard; then, the agent was instructed to open a terminal and paste the command from the clipboard into the terminal. This resulted in the AI system being hijacked to execute arbitrary commands from untrusted web content. 

<u>Violation:</u> This attack demonstrates that AI agents can be “socially engineered,” violating the principles of Human Weak Link, Least Privilege, and Secure Information Flow. 

<u>Defense:</u> Introduce a hard security boundary between untrusted web content and privileged system tools. The agent should not be allowed to copy data from a browser clipboard directly into a system terminal without user consent. This would, however, restrict the agent’s functionality and burdens the user with security decisions, effectively requiring the user to determine what is an appropriate (visual) instruction and what is data (Section 5.1). 

10 

|**essed**<br>**Dyn. Instr. Following**|✓<br>✓|–|✓<br>✓|✓<br>–<br>–<br>–|–|–|✓<br>✓<br>✓<br>–|–<br>✓|✓|✓<br>–|✓<br>✓|
|---|---|---|---|---|---|---|---|---|---|---|---|
|**ddr**<br>**Fuzzy Trust Boundary**|–<br>✓|✓|✓<br>✓|–<br>–<br>–<br>–|–|–|–<br>–<br>–<br>✓|–<br>–|–|–<br>–|–<br>–|
|**ges A**<br>**Dynamic Policy**|–<br>–|–|–<br>✓|–<br>✓<br>–<br>✓|✓|–|–<br>–<br>–<br>✓|–<br>–|✓|✓<br>✓|–<br>✓|
|**allen**<br><br>**Probabilistic TCB**|✓<br>✓|✓|✓<br>✓|✓<br>–<br>✓<br>✓|–|–|–<br><br>–<br>–<br>✓|✓<br>✓|✓|✓<br>✓|✓<br><br>✓|
|**Ch**<br>l,<br>**Instruction Following**<br>Mechanisms addressing prompt<br>injection as dynamic instructions to<br>the agent.|Monitor flters untrusted input<br>Data hiding, IFC labels|Execution isolation|Static IFC on structured plan<br>Plan from trusted data|Static policy<br>Prompting<br>Access control tokens<br>Policy verifcation via ASPM|Code-based guardrails|N/A (content moderation)|Adversarial training<br>Instruction format enforcement<br>Known-answer detection<br>Sandboxing blast radius|N/A (voice confusion)<br>Detection and attribution|Dependency screeners|Injection Isolator<br>Programmable rails|Manifest signing + vetting<br>Verifed policy + runtime check|
|**etails**<br>**Trust Boundary**<br>Where the security boundary is<br>placed: Model, Detector, Tool leve<br>IR/Plan level, App/System level,<br>Inter-agent level, Action level,<br>HTTP request layer, or Decision<br>level.|System level (IFC)<br>Tool level, IR|App level (spoke isolation)|Plan level (IR)<br>IR|Tool level<br>Tool level<br>Inter-agent level<br>Tool level (action-based)|Action level|Detector|Model<br>Model<br>Detector<br>HTTP request layer|Skill invocation level<br>Decision level (DDG)|Tool level (IFC)|Control + data level<br>Input/output/dialog rails|Tool descriptor level<br>Action level|
|**D**<br>**Policy Support**<br>Source or derivation mechanism for<br>task-time permissions and policies:<br>generated by an LLM, automated<br>via non-LLM heuristics or external<br>policy inputs, user-mediated via<br>interactive approvals, user-defned<br>via explicit confguration, or N/A<br>when policies are static/pre-defned.|Generated (task)<br>User-defned (IFC labels)|User-mediated (cross-app)|N/A (abstract/concrete<br>decoupling)<br>Generated (trusted query)|User-defned (JSON)<br>Generated (full context)<br>User-defned (access control)<br>Automated (policy documents)|Generated (task)|N/A|N/A<br>N/A<br>N/A<br>Automated + website policies|N/A<br>N/A (policy-agnostic)|Generated (task)|Generated (task)<br>User-defned (Colang)|N/A<br>Generated (task)|
|**TCB Assumption**<br>How probabilistic components are<br>handled, e.g., fne-tuning, external<br>deterministic monitors, isolation,<br>crypto/ACL primitives, or<br>attention-based analysis.|Security monitor,<br>planner/executor separation<br>Deterministic monitor, security<br>lbl|aes<br>Hub-and-spoke isolation, hub<br>|as kernel<br>Trusted abstract plan, static<br>analysis<br>Control fow isolation|Deterministic monitor<br>Prompting<br>Central Provider, crypto tokens<br>Predicate classifcation,<br>action-based safety policy<br>dl(ASPM)|moe <br>Guard agent (LLM + code<br>execution)|Fine-tuning for safety<br>classifcation|Fine-tuning (adversarial DPO)<br>Fine-tuning for instruction<br>format<br>Fine-tuning for instruction<br>detection<br>Browser extension, HTTP<br>mediation|Browser extension, phonetic<br>analysis<br>Attention-based DDG<br>|(non-invasive)<br>LM-as-judge + attention<br>|saliency<br>Secure Planner + Dynamic<br>Validator<br>Colang runtime, rail engine|RSA signing, LLM semantic<br>vetting<br>Formal verifcation, runtime<br>monitor|
||1]<br>]|[103]|]|4]<br>M [84]<br>t [19]|nt [105]|rd [43]|IH [18, 96]<br>el [52]<br>[54]|[41]<br>d [98]|13]|]<br>rdrails [61]|t al. [45]<br> [56]|
||[10<br> [23|GPT|8]<br> [25|t [8<br>t-LL<br> [90]<br>gen|Age|ua|n / <br>[16]<br>ntin<br>ate|nce <br>uar|[1|[49<br>Gua|di e<br>ard|
|**Work**|f-secure<br>FIDES|Isolate|ACE [4<br>CaMeL|Progen<br>Progen<br>SAGA <br>ShieldA|Guard|LlamaG|SecAlig<br>StruQ <br>DataSe<br>ceLLM|SkillFe<br>MindG|RTBAS|DRIFT<br>NeMo|Jamshi<br>VeriGu|



11 

## **4 Current Approaches** 

We provide an overview of existing efforts to secure agentic systems, with a concise summary in Table 2. 

### **4.1 General AI Security** 

In the past decade, there has been ample research on _formally_ and _rigorously_ verifying the correctness of AI-based systems in general, and neural networks in particular [1]. The various techniques define a property of interest, e.g., _is the AI classifier ϵ-robust to noise_ , and translates this check to a mathematical query that is then solved by off-the-shelf optimizers. On one hand, methods that are both _sound_ (always correct when they claim safety) and _complete_ (always find a violation, if it exists and resources permit) check if the required property holds for _every possible input_ within a domain of interest. Such methods include MILP [94], SAT [59], SMT [46, 47], and are typically geared towards AI models with piecewise-linear activation functions [14, 13, 46]. In some cases, these also include branch-and-bound (B&B) methods, e.g., [109, 97, 13]. Alternatively, some approaches sacrifice completeness (and hence, may not find existing counterexamples) but gain performance. Such techniques include IBP [57, 38], Zonotopes [57, 32], DeepZ [86], DeepPoly [87, 88]), convex relaxations [99], and SDP-based verification [69, 68]), as well as certificate-based techniques (Lyapunov/barrier functions [15, 67]). 

Finally, complementing methods are lightweight verification during runtime such as [2]. 

Robustness can also be assessed with gradient attacks [33, 53] and testing techniques [66, 11]. 

### **4.2 Agentic AI Security** 

Compared to standalone models, verifying the security of agentic AI systems is _substantially_ more challenging for multiple reasons. First, agents routinely invoke _external, third-party tools_ whose outputs are not under the developer’s control and may be adversarial. Second, interaction is typically _iterative_ : intermediate tool outputs are incorporated back into the agent’s context and can influence downstream planning and actions, creating long-range dependencies and compounding risk over time. Third, both the user interface and the tool interface are often mediated through _natural language_ (tool descriptions, user requests, and free-form tool results), making the “API surface” less structured and more susceptible to instruction smuggling and indirect prompt injection attacks [39, 51]. 

**Threat Landscape.** Recent work has systematically characterized the attack of LLM agents. Attacks can be broadly categorized as _agent-based_ , which manipulate internal components such as instructions [112], memory or knowledge bases [20, 116, 104, 22], as well as tool libraries [31, 107]. On the other hand, _environment-based_ attacks exploit vulnerabilities in the external environment the agent interacts with, such as injecting malicious HTML elements [106] or deceptive pop-ups [111]. These attacks can lead to severe consequences, including privacy breaches [50], financial losses [5], and life-threatening failures [20]. 

**Dynamic Monitor-Based Defenses.** One line of work preserves the expressive "plan-act-observereplan" loop but requires _continuous enforcement_ because tool results can modify the effective context seen by the planner. _f-secure_ uses a context-aware pipeline with structured executable plans and an explicit security monitor that filters untrusted inputs entering the planning process [101]. Similarly, _FIDES_ applies dynamic information-flow control to agent planning by tracking integrity/confidentiality labels and enforcing policies at each step [23]. _IsolateGPT_ introduces an architecture that isolates execution environments across applications, requiring user intervention for potentially dangerously cross-app communications [103]. In these architectures, sandboxing/isolation and runtime monitoring are naturally complementary: isolation limits the potential damage of using malicious tools, while monitoring constrains how untrusted data can steer subsequent decisions. Frameworks such as CAPSEM [35] and Invariant Guardrails [10] provide the enforcement mechanisms for applying a variety of security policies, from PII leakage detection to tool-call guardrails to dataflow controls, configurable via expressive policy languages [36]. 

**Planning-First (Static) Approaches.** An alternative paradigm intentionally reduces feedback from untrusted tool outputs into future control flow, enabling more principled ahead-of-time security reasoning. 

12 

_ACE_ [48] separates query processing into abstract plan-generation from trusted user input, concrete plan instantiation, and isolated execution, then statically checks information flow constraints over the resulting structured plan. _CaMeL_ [25] extracts control and data flows from trusted user queries and employs a custom interpreter to prevent untrusted data from affecting program flow. These approaches sacrifice some interactivity to minimize the need for monitoring the tool-response channel and strengthen enforceable security boundaries. 

**Privilege Control and Policy Languages.** Drawing inspiration from classical access control systems [28, 24] and cloud identity and access management (IAM) policies [3, 55, 37], recent work explores programmable privilege control for agents. _Progent_ [84] introduces a domain-specific language for expressing fine-grained, tool-call-level policies that specify which actions are permissible, under what conditions, and with what fallback behaviors. Policies can be manually specified for deterministic security guarantees or automatically generated and updated by LLMs to adapt to task-specific requirements. This approach enforces the principle of least privilege: blocking unnecessary and potentially malicious tool calls while permitting those essential for task completion. Evaluation on benchmarks including AgentDojo [26] and ASB [108] shows substantial reductions in attack success rate (e.g., from 41 _._ 2% to 2 _._ 2%) while maintaining utility. 

**Guardrail Agents and Policy Reasoning.** While traditional guardrails focus on content moderation for LLMs as models (e.g., LlamaGuard [43], LlavaGuard [40]), they fail to address the complexities of action sequences where vulnerabilities emerge over time [105]. _ShieldAgent_ [19] addresses this gap by introducing a guardrail _agent_ that shields other agents via verifiable safety policy reasoning. It constructs an action-based safety policy model (ASPM) by extracting verifiable rules from policy documents (e.g., EU AI Act, corporate handbooks) and organizing them into probabilistic rule circuits. During inference, ShieldAgent retrieves relevant circuits for the invoked action, generates verification plans using specialized tools, and performs formal verification via model checking before making probabilistic guardrail decisions. This approach achieves high accuracy while reducing computational overhead compared to naive rule traversal. 

**Model-Level Defenses.** Complementing system-level and user-level approaches, model-level defenses aim to make LLMs inherently more robust to prompt injection. These include fine-tuning approaches that train models to ignore injected prompts [16, 18, 96]. Detection-based defenses such as DataSentinel [52] use a secondary LLM to identify contaminated inputs via known-answer detection (KAD), achieving a near-perfect accuracy against existing attacks. However, KAD schemes contain a structural vulnerability [21]: since the detection instruction and secret key share the same context window as the potentially malicious input, adaptive attacks can extract and return the secret key while still executing the injected task, fundamentally undermining the defense. These defenses operate at a different level than system-level privilege control and can work in synergy model defenses protect the core reasoning while system defenses safeguard the execution boundary between the agent and the external tools. 

At a high level, these approaches represent recurring trade-offs: dynamic agent loops offer adaptivity but demand persistent monitoring of tool responses and context evolution; planning-first architectures sacrifice interactivity to strengthen enforceable security boundaries; privilege control policies require careful specification but enable deterministic guarantees; and guardrail agents add verification overhead but provide explicit policy compliance with interpretable explanations. 

## **5 Open Research Problems** 

We split the open problems into two categories. First we discuss three _specific mechanisms_ that, if reliable and trustworthy, can solve a significant number of security and privacy issues facing agentic deployments today. Second we discuss three _longer-term, fundamental topics_ that will allow stronger security and privacy guarantees in future agentic deployments. 

13 

### **5.1 Separating Instructions and Data** 

Instruction-data separation has been one of the cornerstones of modern operating systems security, where hardware functionality allows the operating system to mark regions of memory as writeable or executable, but not both (often referred to as W _⊕_ X). By placing code in executable-but-not-writable memory, this prevents a buffer-overflow attack that attempts to execute instructions on the stack that are only meant to be used as data.<sup>1</sup> In agentic computing, separating instructions and data will have a similarly positive effect on security—by preventing prompt-injection attacks that depend on the attacker planting instructions within untrusted data sources (e.g., emails, calendar events, webpages, desktop notifications) [39]. There are several key research questions here: (1) What is a precise and formal definition separating instructions and data [117]? and (2) Given a definition, is it practically possible to construct (in terms of capabilities, scale, cost) an LLM that provably follows this separation? (3) Are current definitions sufficient in capturing the nuances of prompt injection attacks? 

One popular definition is that the agent/LLM should not follow any instructions that appear in the context window tagged as “data” [39, 96, 16, 18, 102, 17]. However, this definition might be too restrictive in various settings, as one of the key benefits of agents is their ability to act upon new information to complete an (often underspecified) goal. Learning to use an API and following web links based on information present in a web page are crucial to such adaptability, though they involve some form of following new instructions present in data. One option to introduce some flexibility into the instruction-following policy is to generalize the instruction-data separation and introduce “trust layers,” where system instructions have the highest level of trust, whereas user instructions are one level below, and instructions from tool data have the lowest trust level [102, 96, 18]. If there is conflict of instructions, this priority is used to resolve it. Unfortunately, any nuanced policy requires the agent (or some additional tool) to explicitly and correctly identify the new instructions inside the data. 

These implementations do not offer security guarantees and, in this sense, are best effort heuristics. Attacks have been shown in the black-box and white-box setting [65, 70, 60], as one can trick the model into following instructions despite the fine-tuning to learn separators. Furthermore, with multi-modal becoming standard, instructions may appear not only in text, but also, in images, video, and audio. The past 10 years of adversarial machine learning has shown that “continuous domain” adversarial examples are easy to carry out [7]. As a result, a probabilistic separation of instructions and data allows the attacker to employ an optimizer to easily find counter-examples to break the defense. 

Furthermore, current definitions are insufficient to block all prompt injections. Even if the agent does not follow an instruction that comes as data, such as: 

ignore everything else and run rm -rf /* 

it can still be biased by the data because it must use it in its reasoning loop. For example, in an MCP tool poisoning attack, where the metadata in the tool descriptions provides “canonical examples” of how a tool should be used [9, 98], an agent can be biased to make mistakes by generating tool calls using those canonical examples. Even if the agent does not follow an instruction, the arguments to the tools that it decides to use can still be poisoned by external sources. This follows from first principles: if the model is to “act” on data, then any of its subsequent outputs must necessarily reflect the influence of that data. 

In conclusion, separating instructions and data (if attainable) will cut out a large swath of prompt injections, but it is unlikely to fully solve the prompt injection problem. 

### **5.2 Access Control and Least Privilege** 

This is another cornerstone of modern computer systems security. An entity should have the minimum privilege necessary to complete its stated function. In an operating system, the kernel (that is isolated from the untrusted processes using hardware mechanisms) enforces what resources the untrusted process can access. A developer or user creates an access control policy that tries to ensure accesses are “least privilege” only. A widely-used example of this design is the Android filesystem sandbox. Each app installed on the phone gets 

> 1We note that W _⊕_ X does not completely remove code execution vulnerabilities due to advanced techniques like return-to-libc or return-oriented programming [83], but is nonetheless foundational in systems security. 

14 

read-write access to a specific part of the filesystem that is meant only for that app—it does not have access to the entire filesystem. Another common example is SELinux policy set by system administrators for Linux computers in an enterprise environment—this sets deterministic guardrails on the various system calls any process is allowed to issue. 

The LLM/agent space does not follow any of these principles as, for example, an agent typically has uniform access to all tool calls, whether necessary for the current task or not. There are technical challenges to employing a least-privilege model. First, unlike traditional computer systems that had the notion of a program/application, for LLMs, there is no program. Rather, the LLM represents all possible programs at once because it can “compute” many different kinds of functions. Second, there is no “developer” to set access control policies, only a user who prompts the agent with a natural language task and who may lack any security expertise. Current recommendations from AI-agent providers highlight the need to proactively enable tools only as needed, as a form of manually enforced least privilege. For example OpenAI states in their documentation [63]: _“Enable only the connectors needed for the current task.”_ A related approach that Google Gemini takes is to disable some of the tools available to the agent under certain conditions, but this is bypassable by a determined attacker that injects multiple layers of instructions [72]. 

There are current efforts at addressing the policy enforcement challenge for discrete tool-using agents where tools have proper semantic definitions [25, 84, 48, 90]. These approaches provide a flexible way to express fine-grained access control, but there are AI agents (especially for computer-, browser-, phone-use tasks) that are not amenable to such system designs. Existing work also does not solve the policy specification problem. A complete access-control system also needs to provide tools for policy creation, maybe by inferring from the user’s prompt [95] or by requiring system administrators in an enterprise write a mandatory access control policy. An interesting research opportunity is to use the reasoning capabilities of modern language models to create policy assistants that can have conversations with users to clarify gaps in natural language task specifications or to automatically decide when a user should be prompted with a permission screen. 

In conclusion, least-privilege access control is going to be a necessary component for defending against prompt injections and needs to be layered with defenses that separate instructions and data. 

### **5.3 Information-Flow Control (IFC)** 

Access control as described above is a “gate” because it only decides a yes/no answer on whether the agent should have access to resources (one or more tools). There are many cases where an agent legitimately needs continued access to sensitive resources. For example, a coding agent might need access to API keys to perform operations like uploading a Docker container image to an endpoint. In such cases, the access-control policy will say that the agent has a legitimate reason to access the sensitive information. The least-privilege requirement is that the agent _must use_ that information in a very specific way—in our example, to only upload the Docker image to the endpoint and nothing else. Thus, there is a need to ensure that the only allowed flow of information (the API key) is from the agent to the deployment endpoint. IFC is a well-researched primitive in the computer security literature but applying it to the LLM/agent space is challenging. 

IFC works by labeling data, then tracking those labels, and enforcing label-based policies as the program operates on the data [92, 30, 27]. This labeling and tracking can be done at many granularities (e.g., processor-instruction level, program-variable level, process level, filesystem-level, cross-computer level), with various guarantees. However, the common assumption is that it is possible to track labels as the corresponding data makes its way through the system and updating the labels accordingly, through “flow arithmetic.” [27]. 

It is an open challenge to perform flow arithmetic on LLMs. Whatever multiple data values (and their corresponding labels) go into the model, currently we can only assume the union of those labels comes out. This immediately leads to the well-known problem of label explosion, where every piece of data is labeled as “everything” and thus defeats the purpose of tracking labels. 

Thus IFC is likely a great layer to add beyond least-privilege access control, but it requires solving the fundamental challenge of fine-grained and precise flow arithmetic in LLMs. 

### **5.4 Long-Term: Security Guarantees from Probabilistic TCBs** 

We mentioned the challenge of building on top of probabilistic TCBs in Section 2.1 and as we discussed earlier in this section, there are many proposals for such probabilistic TCBs (to distinguish instruction from data, 

15 

to create security policies, to perform information-flow tracking, etc.). Being probabilistic, such TCBs fall short of providing strong security guarantees, as determined and patient attackers can always find a bypass. Designing an approach to obtain guaranteed security from a probabilistic TCB is a hard foundational problem whose solutions would enable a variety of LLM uses in security tasks. The problem is further complicated by the requirement that the probabilistic TCB must be made secure _under Byzantine assumptions_ , meaning that worst-case attackers (adaptive, non-rational, not computationally bounded) 

are trying to abuse the system. Another particular complication, when using AI agents as part of the probabilistic TCB, is that agents may counterintuively try to evade the security policy due to their propensity to reward hacking [12]. 

### **5.5 Long-Term: Security-Aware ML Model Architectures** 

The common approaches discussed up to now either place security mechanisms outside the agent or train the agent to perform the security task themselves. Another alternative may be to “surgically enhance” an already trained agent to enforce some security policy. If a circuit in the model is found to address a security-relevant aspect of a task and the security policy blocks that aspect under some condition, it may be possible to enhance that circuit to discard its outputs when the condition holds [114, 42]. Such a model would necessarily have an architecture that can be inspected (e.g., via the means of mechanistic interpretability) and supplemented with security policy-specific constraints. While such an architecture may be more complex, it adds flexibility in allowing any security policy to be attached to the inference process, without having to train the model. 

### **5.6 Long Term: Designing Correct Security Principles for LLMs** 

We have seen so far that Large Language Models (LLMs) by their very nature present an interesting dilemma. As we saw in Section 5.4, they are not completely deterministic computer programs, and they cannot be treated as such. They are like humans in many ways—they are probabilistic, they make mistakes, and often the mistakes are human-like because their training data is primarily generated by humans. Yet, there are also many aspects where they are not quite like humans—an LLM has access to vast information that no single human could ever aspire to. The possibility of solutions of a different nature thus arises: given a task and a situation, the LLM could reason or look through its vast body of knowledge to see if completing this task could result in a security failure. 

All of this leads to an intriguing question: what are the right security principles while working with an LLM? What are some cases where we can treat it as a computer program (as in Section 5.4), where can we treat it as a human prone to mistakes, and where should we exploit its knowledge and reasoning ability to make better security decisions? Together with designing better probabilistic TCBs, this is yet another long-term question in building secure and effective agentic systems. 

## **6 Conclusion** 

Information security and cryptography are classic fields with several well investigated principles and techniques. Provable defenses generally work by having an invariant called the _security assumption_ . For example, in case of system security a TCB that the attacker cannot tamper with, and in case of cryptography, the hardness of a mathematical problem, such as factoring or discrete log. In the context of AI-agents it is unclear what the security assumption could be. Without precise security assumptions, it is very challenging to build provable defenses. Another important principle in the systems security approach is to have programmable and deterministic guardrails at different layers of abstraction (separate instructions/data at the lowest level, perform least privilege access control at the system call/tool level and monitor/enforce information flows at the program/agent level). 

Applying the above-mentioned principle to AI agents is challenging because the abstraction layers in agentic systems are not yet well defined. Traditional security principles and techniques still apply and can thwart many attacks on agentic systems, but some attack classes expose genuinely new problems that require new solutions. Encouragingly, these emerging challenges create a compelling research agenda for the community. 

16 

## **References** 

- [1] Aws Albarghouthi. Introduction to Neural Network Verification. _Found. Trends Program. Lang._ , 7(1–2):1––157, December 2021. doi:10.1561/2500000051. 

- [2] Mohammed Alshiekh, Roderick Bloem, Rüdiger Ehlers, Bettina Könighofer, Scott Niekum, and Ufuk Topcu. Safe reinforcement learning via shielding. In _Proceedings of the Thirty-Second AAAI Conference on Artificial Intelligence and Thirtieth Innovative Applications of Artificial Intelligence Conference and Eighth AAAI Symposium on Educational Advances in Artificial Intelligence_ , AAAI’18/IAAI’18/EAAI’18. AAAI Press, 2018. URL: https://dl.acm.org/doi/10.5555/3504035.3504361. 

- [3] Amazon Web Services. AWS Identity and Access Management (IAM). https://aws.amazon.com/iam/. Accessed: 2026. 

- [4] Ross J. Anderson. _Security Engineering: A Guide to Building Dependable Distributed Systems_ . John Wiley & Sons, Inc., USA, 1st edition, 2001. URL: https://www.wiley.com/Security+Engineering%3A+ A+Guide+to+Building+Dependable+Distributed+Systems%2C+3rd+Edition-p-9781119642787. 

- [5] Maksym Andriushchenko, Alexandra Souly, Mateusz Dziemian, Derek Duenas, Maxwell Lin, Justin Wang, Dan Hendrycks, Andy Zou, J Zico Kolter, Matt Fredrikson, Yarin Gal, and Xander Davies. AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents. In _The Thirteenth International Conference on Learning Representations_ , 2025. URL: https://openreview.net/forum?id=AC5n7xHuR1. 

- [6] Anthropic. Agent skills—Claude API docs, 2026. Accessed: 2026-02-05. URL: https://platform.claude. com/docs/en/agents-and-tools/agent-skills/overview. 

- [7] Anish Athalye, Nicholas Carlini, and David Wagner. Obfuscated Gradients Give a False Sense of Security: Circumventing Defenses to Adversarial Examples, 2018. URL: https://arxiv.org/abs/1802.00420, arXiv:1802.00420. 

- [8] Luca Beurer-Kellner, Beat Buesser, Ana-Maria Creţu, Edoardo Debenedetti, Daniel Dobos, Daniel Fabian, Marc Fischer, David Froelicher, Kathrin Grosse, Daniel Naeff, Ezinwanne Ozoani, Andrew Paverd, Florian Tramèr, and Václav Volhejn. Design Patterns for Securing LLM Agents against Prompt Injections, 2025. URL: https://arxiv.org/abs/2506.08837, arXiv:2506.08837. 

- [9] Luca Beurer-Kellner and Marc Fischer. MCP Security Notification: Tool Poisoning Attacks. https:// invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks, April 2025. Accessed: 2025-11-03. 

- [10] Luca Beurer-Kellner, Marc Fischer, Hemang Sarkar, Kristian Bonde Nielsen, Marco Milanta, and Aleksei Kudrinskii. Introducing Guardrails: The Contextual Security Layer for the Agentic Era. https://invariantlabs.ai/blog/guardrails, April 2025. Accessed: 2026-02-05. 

- [11] Leo Boisvert, Mihir Bansal, Chandra Kiran Reddy Evuru, Gabriel Huang, Abhay Puri, Avinandan Bose, Maryam Fazel, Quentin Cappart, Jason Stanley, Alexandre Lacoste, Alexandre Drouin, and Krishnamurthy Dvijotham. DoomArena: A framework for Testing AI Agents Against Evolving Security Threats, 2025. URL: https://arxiv.org/abs/2504.14064, arXiv:2504.14064. 

- [12] Alexander Bondarenko, Denis Volk, Dmitrii Volkov, and Jeffrey Ladish. Demonstrating Specification Gaming in Reasoning Models, 2025. URL: https://arxiv.org/abs/2502.13295, arXiv:2502.13295. 

- [13] Rudy Bunel, Jingyue Lu, Ilker Turkaslan, Philip H.S. Torr, Pushmeet Kohli, and M. Pawan Kumar. Branch and bound for piecewise linear neural network verification. _Journal of Machine Learning Research_ , 21(42):1–39, 2020. URL: http://jmlr.org/papers/v21/19-468.html. 

- [14] Rudy Bunel, Ilker Turkaslan, Philip H.S. Torr, Pushmeet Kohli, and M. Pawan Kumar. A unified view of piecewise linear neural network verification. In _Proceedings of the 32nd International Conference on Neural Information Processing Systems_ , NIPS’18, page 4795–4804, Red Hook, NY, USA, 2018. Curran Associates Inc. URL: https://dl.acm.org/doi/10.5555/3327345.3327388. 

17 

- [15] Ya-Chien Chang, Nima Roohi, and Sicun Gao. Neural Lyapunov control. In H. Wallach, H. Larochelle, A. Beygelzimer, F. d'Alché-Buc, E. Fox, and R. Garnett, editors, _Advances in Neural Information Processing Systems_ , volume 32. Curran Associates, Inc., 2019. URL: https://proceedings.neurips.cc/ paper_files/paper/2019/file/2647c1dba23bc0e0f9cdf75339e120d2-Paper.pdf. 

- [16] Sizhe Chen, Julien Piet, Chawin Sitawarin, and David Wagner. StruQ: Defending against prompt injection with structured queries. In _34th USENIX Security Symposium (USENIX Security 25)_ , pages 2383–2400, 2025. URL: https://www.usenix.org/conference/usenixsecurity25/presentation/chen-sizhe. 

- [17] Sizhe Chen, Yizhu Wang, Nicholas Carlini, Chawin Sitawarin, and David Wagner. Defending against prompt injection with a few defensive tokens, 2025. URL: https://arxiv.org/abs/2507.07974, arXiv: 2507.07974. 

- [18] Sizhe Chen, Arman Zharmagambetov, Saeed Mahloujifar, Kamalika Chaudhuri, David Wagner, and Chuan Guo. SecAlign: Defending Against Prompt Injection with Preference Optimization. In _Proceedings of the ACM Conference on Computer and Communications Security (CCS)_ , 2025. 

- [19] Zhaorun Chen, Mintong Kang, and Bo Li. ShieldAgent: Shielding Agents via Verifiable Safety Policy Reasoning, 2025. URL: https://arxiv.org/abs/2503.22738, arXiv:2503.22738. 

- [20] Zhaorun Chen, Zhen Xiang, Chaowei Xiao, Dawn Song, and Bo Li. AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases . _Advances in Neural Information Processing Systems_ , 37:130185–130213, 2024. 

- [21] Sarthak Choudhary, Divyam Anshumaan, Nils Palumbo, and Somesh Jha. How Not to Detect Prompt Injections with an LLM. In _Proceedings of the 18th ACM Workshop on Artificial Intelligence and Security_ , pages 218–229, 2025. 

- [22] Sarthak Choudhary, Nils Palumbo, Ashish Hooda, Krishnamurthy Dj Dvijotham, and Somesh Jha. Through the Stealth Lens: Rethinking Attacks and Defenses in RAG, 2025. URL: https://arxiv.org/ abs/2506.04390, arXiv:2506.04390. 

- [23] Manuel Costa, Boris Köpf, Aashish Kolluri, Andrew Paverd, Mark Russinovich, Ahmed Salem, Shruti Tople, Lukas Wutschitz, and Santiago Zanella-Béguelin. Securing AI Agents with Information-Flow Control, 2025. URL: https://arxiv.org/abs/2505.23643, arXiv:2505.23643. 

- [24] Joseph W. Cutler, Craig Disselkoen, Aaron Eline, Shaobo He, Kyle Headley, Michael Hicks, Kesha Hietala, Eleftherios Ioannidis, John Kastner, Anwar Mamat, Darin McAdams, Matt McCutchen, Neha Rungta, Emina Torlak, and Andrew M. Wells. Cedar: A new language for expressive, fast, safe, and analyzable authorization. _Proc. ACM Program. Lang._ , 8(OOPSLA1), April 2024. doi:10.1145/ 3649835. 

- [25] Edoardo Debenedetti, Ilia Shumailov, Tianqi Fan, Jamie Hayes, Nicholas Carlini, Daniel Fabian, Christoph Kern, Chongyang Shi, Andreas Terzis, and Florian Tramèr. Defeating Prompt Injections by Design, 2025. URL: https://arxiv.org/abs/2503.18813, arXiv:2503.18813. 

- [26] Edoardo Debenedetti, Jie Zhang, Mislav Balunovic, Luca Beurer-Kellner, Marc Fischer, and Florian Tramèr. AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents. _Advances in Neural Information Processing Systems (NeurIPS)_ , 37:82895–82920, 2024. 

- [27] Dorothy E. Denning. A Lattice Model of Secure Information Flow. _Commun. ACM_ , 19(5):236–243, May 1976. doi:10.1145/360051.360056. 

- [28] John DeTreville. Binder, a Logic-based Security Language. In _Proceedings 2002 IEEE Symposium on Security and Privacy_ , pages 105–113. IEEE, 2002. 

- [29] Brendan Dolan-Gavitt, Tim Leek, Michael Zhivich, Jonathon Giffin, and Wenke Lee. Virtuoso: Narrowing the Semantic Gap in Virtual Machine Introspection. In _2011 IEEE Symposium on Security and Privacy_ , pages 297–312, 2011. doi:10.1109/SP.2011.11. 

18 

- [30] William Enck, Peter Gilbert, Seungyeop Han, Vasant Tendulkar, Byung-Gon Chun, Landon P. Cox, Jaeyeon Jung, Patrick McDaniel, and Anmol N. Sheth. TaintDroid: An Information-Flow Tracking System for Realtime Privacy Monitoring on Smartphones. _ACM Trans. Comput. Syst._ , 32(2), June 2014. doi:10.1145/2619091. 

- [31] Xiaohan Fu, Shuheng Li, Zihan Wang, Yihao Liu, Rajesh K. Gupta, Taylor Berg-Kirkpatrick, and Earlence Fernandes. Imprompter: Tricking LLM agents into improper tool use, 2024. URL: https:// arxiv.org/abs/2410.14923, arXiv:2410.14923. 

- [32] Timon Gehr, Matthew Mirman, Dana Drachsler-Cohen, Petar Tsankov, Swarat Chaudhuri, and Martin Vechev. AI2: Safety and Robustness Certification of Neural Networks with Abstract Interpretation. In _2018 IEEE symposium on security and privacy (SP)_ , pages 3–18. IEEE, 2018. 

- [33] Ian J. Goodfellow, Jonathon Shlens, and Christian Szegedy. Explaining and Harnessing Adversarial Examples. In _3rd International Conference on Learning Representations (ICLR)_ , 2015. 

- [34] Google. Android Developers > Design & Plan > Security > Guides > Dynamic Code Loading, 2024. Last updated 2024-09-24 UTC. Accessed: 2026-02-05. URL: https://developer.android.com/ privacy-and-security/risks/dynamic-code-loading. 

- [35] Google. CAPSEM: Contextual Agent Privacy and Security Manager. https://capsem.org/, 2026. Accessed: 2026-02-05. 

- [36] Google. Common Expression Language (CEL). https://cel.dev/, 2026. Accessed: 2026-02-05. 

- [37] Google Cloud. Identity and Access Management (IAM). https://cloud.google.com/iam/. Accessed: 2026. 

- [38] Sven Gowal, Krishnamurthy Dvijotham, Robert Stanforth, Rudy Bunel, Chongli Qin, Jonathan Uesato, Relja Arandjelovic, Timothy Arthur Mann, and Pushmeet Kohli. Scalable verified training for provably robust image classification. In _2019 IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 4841–4850, 2019. doi:10.1109/ICCV.2019.00494. 

- [39] Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres, Thorsten Holz, and Mario Fritz. Not what You’ve Signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection, 2023. URL: https://arxiv.org/abs/2302.12173, arXiv:2302.12173. 

- [40] Lukas Helff, Felix Friedrich, Manuel Brack, Patrick Schramowski, and Kristian Kersting. LlavaGuard: An open VLM-based framework for safeguarding vision datasets and models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 8322–8326, 2024. URL: https://openreview.net/forum?id=YIO9ritzWV. 

- [41] Ashish Hooda, Matthew Wallace, Kushal Jhunjhunwalla, Earlence Fernandes, and Kassem Fawaz. SkillFence: A Systems Approach to Practically Mitigating Voice-Based Confusion Attacks. _Proc. ACM Interact. Mob. Wearable Ubiquitous Technol._ , 6(1), March 2022. doi:10.1145/3517232. 

- [42] Kuo-Han Hung, Ching-Yun Ko, Ambrish Rawat, I-Hsin Chung, Winston H. Hsu, and Pin-Yu Chen. Attention Tracker: Detecting Prompt Injection Attacks in LLMs, 2025. URL: https://arxiv.org/abs/ 2411.00348, arXiv:2411.00348. 

- [43] Hakan Inan, Kartikeya Upasani, Jianfeng Chi, Rashi Rungta, Krithika Iyer, Yuning Mao, Michael Tontchev, Qing Hu, Brian Fuller, Davide Testuggine, and Madian Khabsa. Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations, 2023. URL: https://arxiv.org/abs/2312.06674, arXiv:2312.06674. 

- [44] Bhushan Jain, Mirza Basim Baig, Dongli Zhang, Donald E. Porter, and Radu Sion. SoK: Introspections on Trust and the Semantic Gap. In _2014 IEEE Symposium on Security and Privacy_ , pages 605–620, 2014. doi:10.1109/SP.2014.45. 

19 

- [45] Saeid Jamshidi, Kawser Wazed Nafi, Arghavan Moradi Dakhel, Negar Shahabi, Foutse Khomh, and Naser Ezzati-Jivan. Securing the Model Context Protocol: Defending LLMs Against Tool Poisoning and Adversarial Attacks, 2025. Technical Report. http://arxiv.org/abs/2512.06556. 

- [46] Guy Katz, Clark Barrett, David L Dill, Kyle Julian, and Mykel J Kochenderfer. Reluplex: An Efficient SMT Solver for Verifying Deep Neural Networks. In _International Conference on Computer Aided Verification (CAV)_ , pages 97–117, 2017. doi:10.1007/978-3-319-63387-9_5. 

- [47] Guy Katz, Derek A. Huang, Duligur Ibeling, Kyle Julian, Christopher Lazarus, Rachel Lim, Parth Shah, Shantanu Thakoor, Haoze Wu, Aleksandar Zeljić, David L. Dill, Mykel J. Kochenderfer, and Clark Barrett. The Marabou framework for verification and analysis of deep neural networks. In Isil Dillig and Serdar Tasiran, editors, _Computer Aided Verification_ , pages 443–452, Cham, 2019. Springer International Publishing. doi:10.1007/978-3-030-25540-4_26. 

- [48] Evan Li, Tushin Mallick, Evan Rose, William Robertson, Alina Oprea, and Cristina Nita-Rotaru. ACE: A Security Architecture for LLM-Integrated App Systems. In _Proceedings of the Network and Distributed System Security Symposium (NDSS)_ , 2026. 

- [49] Hao Li, Xiaogeng Liu, CHIU Hung Chun, Dianqi Li, Ning Zhang, and Chaowei Xiao. DRIFT: Dynamic rule-based defense with injection isolation for securing LLM agents. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. URL: https://openreview.net/ forum?id=oY1Xnt83oJ. 

- [50] Zeyi Liao, Lingbo Mo, Chejian Xu, Mintong Kang, Jiawei Zhang, Chaowei Xiao, Yuan Tian, Bo Li, and Huan Sun. EIA: Environmental Injection Attack on Generalist Web Agents for Privacy Leakage, 2025. URL: https://arxiv.org/abs/2409.11295, arXiv:2409.11295. 

- [51] Yi Liu, Gelei Deng, Yuekang Li, Kailong Wang, Zihao Wang, Xiaofeng Wang, Tianwei Zhang, Yepang Liu, Haoyu Wang, Yan Zheng, Leo Yu Zhang, and Yang Liu. Prompt Injection Attack Against LLM-Integrated Applications, 2025. URL: https://arxiv.org/abs/2306.05499, arXiv:2306.05499. 

- [52] Yupei Liu, Yuqi Jia, Jinyuan Jia, Dawn Song, and Neil Zhenqiang Gong. DataSentinel: A GameTheoretic Detection of Prompt Injection Attacks. In _2025 IEEE Symposium on Security and Privacy (SP)_ , pages 2190–2208, 2025. doi:10.1109/SP61157.2025.00250. 

- [53] Aleksander Madry, Aleksandar Makelov, Ludwig Schmidt, Dimitris Tsipras, and Adrian Vladu. Towards Deep Learning Models Resistant to Adversarial Attacks. In _6th International Conference on Learning Representations (ICLR)_ , 2018. URL: https://openreview.net/forum?id=rJzIBfZAb. 

- [54] Luoxi Meng, Henry Feng, Ilia Shumailov, and Earlence Fernandes. ceLLMate: Sandboxing Browser AI Agents, 2025. URL: https://arxiv.org/abs/2512.12594, arXiv:2512.12594. 

- [55] Microsoft. Azure Policy Documentation. https://learn.microsoft.com/en-us/azure/governance/policy/. Accessed: 2026. 

- [56] Lesly Miculicich, Mihir Parmar, Hamid Palangi, Krishnamurthy Dj Dvijotham, Mirko Montanari, Tomas Pfister, and Long T. Le. VeriGuard: Enhancing LLM Agent Safety via Verified Code Generation, 2025. URL: https://arxiv.org/abs/2510.05156, arXiv:2510.05156. 

- [57] Matthew Mirman, Timon Gehr, and Martin Vechev. Differentiable abstract interpretation for provably robust neural networks. In Jennifer Dy and Andreas Krause, editors, _Proceedings of the 35th International Conference on Machine Learning_ , volume 80 of _Proceedings of Machine Learning Research_ , pages 3578– 3586. PMLR, 10–15 Jul 2018. URL: https://proceedings.mlr.press/v80/mirman18b.html. 

- [58] Model Context Protocol. Getting Started — Intro. https://modelcontextprotocol.io/docs/getting-started/ intro, 2025. Accessed 2025-10-31. 

20 

- [59] Nina Narodytska, Shiva Kasiviswanathan, Leonid Ryzhyk, Mooly Sagiv, and Toby Walsh. Verifying Properties of Binarized Deep Neural Networks. In _Proceedings of the Thirty-Second AAAI Conference on Artificial Intelligence and Thirtieth Innovative Applications of Artificial Intelligence Conference and Eighth AAAI Symposium on Educational Advances in Artificial Intelligence_ , AAAI’18/IAAI’18/EAAI’18. AAAI Press, 2018. URL: https://dl.acm.org/doi/abs/10.5555/3504035.3504845. 

- [60] Milad Nasr, Nicholas Carlini, Chawin Sitawarin, Sander V. Schulhoff, Jamie Hayes, Michael Ilie, Juliette Pluto, Shuang Song, Harsh Chaudhari, Ilia Shumailov, Abhradeep Thakurta, Kai Yuanqing Xiao, Andreas Terzis, and Florian Tramèr. The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against Llm Jailbreaks and Prompt Injections, 2025. URL: https://arxiv.org/abs/2510.09023, arXiv:2510.09023. 

- [61] NVIDIA. NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails. https://github.com/NVIDIA/NeMo-Guardrails, 2023. Accessed: 2026-02-03. URL: https:// github.com/NVIDIA/NeMo-Guardrails. 

- [62] OpenAI. How we think about safety and alignment. https://openai.com/safety/how-we-think-aboutsafety-alignment/, 2025. Accessed 2025-11-07. 

- [63] OpenAI. ChatGPT Agent, 2026. Accessed: 2026-01-28. URL: https://help.openai.com/en/articles/ 11752874-chatgpt-agent. 

- [64] OpenClaw. ClawHub, the skill dock for sharp agents, 2026. Accessed: 2026-02-05. URL: https:// clawhub.ai/. 

- [65] Nishit V. Pandya, Andrey Labunets, Sicun Gao, and Earlence Fernandes. May I have your Attention? Breaking Fine-Tuning based Prompt Injection Defenses using Architecture-Aware Attacks, 2025. URL: https://arxiv.org/abs/2507.07417, arXiv:2507.07417. 

- [66] Kexin Pei, Yinzhi Cao, Junfeng Yang, and Suman Jana. DeepXplore: Automated Whitebox Testing of Deep Learning Systems. In _Proceedings of the 26th Symposium on Operating Systems Principles (SOSP)_ , pages 1–18, 2017. 

- [67] Zengyi Qin, Kaiqing Zhang, Yuxiao Chen, Jingkai Chen, and Chuchu Fan. Learning Safe Multi-agent Control with Decentralized Neural Barrier Certificates. In _9th International Conference on Learning Representations (ICLR)_ , 2021. 

- [68] Aditi Raghunathan, Jacob Steinhardt, and Percy Liang. Certified Defenses against Adversarial Examples. In _Proceedings of the Sixth International Conference on Learning Representations (ICLR)_ , 2018. URL: https://openreview.net/forum?id=Bys4ob-Rb. 

- [69] Aditi Raghunathan, Jacob Steinhardt, and Percy Liang. Semidefinite Relaxations for Certifying Robustness to Adversarial Examples. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 31, pages 10900–10910, 2018. URL: https://dl.acm.org/doi/10.5555/3327546.3327746. 

- [70] J. Rehberger (wunderwuzzi). Breaking Instruction Hierarchy in OpenAI’s gpt-4o-mini. https:// embracethered.com/blog/posts/2024/chatgpt-gpt-4o-mini-instruction-hierarchie-bypasses/, July 2024. Accessed: 2025-11-03. 

- [71] J. Rehberger (wunderwuzzi). DeepSeek AI: From prompt injection to account takeover. https:// embracethered.com/blog/posts/2024/deepseek-ai-prompt-injection-to-xss-and-account-takeover/, 2024. Accessed on 2025-09-05. 

- [72] J. Rehberger (wunderwuzzi). Google Gemini: Planting Instructions For Delayed Automatic Tool Invocation, feb 2024. URL: https://embracethered.com/blog/posts/2024/llm-context-pollution-anddelayed-automated-tool-invocation/. 

- [73] J. Rehberger (wunderwuzzi). Microsoft Copilot: From Prompt Injection to Exfiltration of Personal Information. https://embracethered.com/blog/posts/2024/m365-copilot-prompt-injection-tool-invocationand-data-exfil-using-ascii-smuggling/, 2024. Accessed on 2025-09-05. 

21 

- [74] J. Rehberger (wunderwuzzi). Spyware Injection Into Your ChatGPT’s Long-Term Memory (SpAIware). https://embracethered.com/blog/posts/2024/chatgpt-macos-app-persistent-data-exfiltration/, 2024. Accessed on 2025-09-05. 

- [75] J. Rehberger (wunderwuzzi). Terminal DiLLMas—Prompt Injection in the Terminal via ANSI Sequences. https://embracethered.com/blog/posts/2024/terminal-dillmas-prompt-injection-ansi-sequences/, 2024. Accessed on 2025-09-05. 

- [76] J. Rehberger (wunderwuzzi). AI ClickFix: Hijacking Computer-Use Agents Using ClickFix. Blog post, May 2025. URL: https://embracethered.com/blog/posts/2025/ai-clickfix-ttp-claude/. 

- [77] J. Rehberger (wunderwuzzi). AMP–Agents that Modify System Configuration and Escape. https:// embracethered.com/blog/posts/2025/amp-agents-that-modify-system-configuration-and-escape/, 2025. Accessed on 2025-09-05. 

- [78] J. Rehberger (wunderwuzzi). ChatGPT Operator prompt injection exploits. https://embracethered.com/ blog/posts/2025/chatgpt-operator-prompt-injection-exploits/, 2025. Accessed on 2025-09-05. 

- [79] J. Rehberger (wunderwuzzi). Claude Code: Data Exfiltration with DNS (CVE-2025-55284). Blog post, August 2025. URL: https://embracethered.com/blog/posts/2025/claude-code-exfiltration-via-dnsrequests/. 

- [80] J. Rehberger (wunderwuzzi). Devin AI Kill Chain—Exposing Ports Leading to RCE and file Exfiltration. https://embracethered.com/blog/posts/2025/devin-ai-kill-chain-exposing-ports/, 2025. Accessed on 202509-05. 

- [81] J. Rehberger (wunderwuzzi). Devin can leak your secrets—Prompt Injection Leads to Exfiltration. https://embracethered.com/blog/posts/2025/devin-can-leak-your-secrets/, 2025. Accessed on 2025-09-05. 

- [82] J.H. Saltzer and M.D. Schroeder. The Protection of Information in Computer Systems. _Proceedings of the IEEE_ , 63(9):1278–1308, 1975. doi:10.1109/PROC.1975.9939. 

- [83] Hovav Shacham. The Geometry of Innocent Flesh on the Bone: Return-into-libc without Function Calls (on the x86). In _Proceedings of the 14th ACM Conference on Computer and Communications Security_ , CCS ’07, page 552–561, New York, NY, USA, 2007. Association for Computing Machinery. doi:10.1145/1315245.1315313. 

- [84] Tianneng Shi, Jingxuan He, Zhun Wang, Hongwei Li, Linyu Wu, Wenbo Guo, and Dawn Song. Progent: Programmable Privilege Control for LLM Agents, 2025. URL: https://arxiv.org/abs/2504.11703, arXiv:2504.11703. 

- [85] Marina Simakov. AgentFlayer: When a Jira Ticket Can Steal Your Secrets. https://labs.zenity.io/p/ when-a-jira-ticket-can-steal-your-secrets, August 2025. Accessed: 2025-09-17. 

- [86] Gagandeep Singh, Timon Gehr, Matthew Mirman, Markus Püschel, and Martin Vechev. Fast and Effective Robustness Certification. In S. Bengio, H. Wallach, H. Larochelle, K. Grauman, N. Cesa-Bianchi, and R. Garnett, editors, _Advances in Neural Information Processing Systems_ , volume 31. Curran Associates, Inc., 2018. URL: https://proceedings.neurips.cc/paper_files/paper/2018/ file/f2f446980d8e971ef3da97af089481c3-Paper.pdf. 

- [87] Gagandeep Singh, Timon Gehr, Markus Püschel, and Martin Vechev. An Abstract Domain for Certifying Neural Networks. _Proc. ACM Program. Lang._ , 3(POPL), January 2019. doi:10.1145/3290354. 

- [88] Gagandeep Singh, Timon Gehr, Markus Püschel, and Martin Vechev. Boosting Robustness Certification of Neural Networks. In _Proceedings of the Seventh International Conference on Learning Representations (ICLR)_ , 2019. URL: https://openreview.net/forum?id=HJgeEh09KQ. 

- [89] Robin Sommer and Vern Paxson. Outside the Closed World: On Using Machine Learning for Network Intrusion Detection. In _2010 IEEE Symposium on Security and Privacy_ , pages 305–316, 2010. doi:10.1109/SP.2010.25. 

22 

- [90] Georgios Syros, Anshuman Suri, Jacob Ginesin, Cristina Nita-Rotaru, and Alina Oprea. SAGA: A Security Architecture for Governing AI Agentic Systems. In _Network and Distributed System Security Symposium (NDSS)_ , 2026. 

- [91] Christian Szegedy, Wojciech Zaremba, Ilya Sutskever, Joan Bruna, Dumitru Erhan, Ian Goodfellow, and Rob Fergus. Intriguing Properties of Neural Networks, 2014. URL: https://arxiv.org/abs/1312.6199, arXiv:1312.6199. 

- [92] Trishita Tiwari, Suchin Gururangan, Chuan Guo, Weizhe Hua, Sanjay Kariyappa, Udit Gupta, Wenjie Xiong, Kiwan Maeng, Hsien-Hsin S. Lee, and G. Edward Suh. Information flow control in machine learning through modular model architecture. In _Proceedings of the 33rd USENIX Conference on Security Symposium_ , SEC’24, USA, 2024. USENIX Association. URL: https://www.usenix.org/ conference/usenixsecurity24/presentation/tiwari. 

- [93] Udbhav Tiwari and Meredith Whittaker. AI Agent, AI Spy. https://media.ccc.de/v/39c3-ai-agent-ai-spy. 39th Chaos Communication Congress, Congress Center Hamburg, Hamburg, Germany. URL: https:// media.ccc.de/v/39c3-ai-agent-ai-spy. 

- [94] Vincent Tjeng, Kai Xiao, and Russ Tedrake. Evaluating Robustness of Neural Networks with Mixed Integer Programming. In _Proceedings of the Seventh International Conference on Learning Representations (ICLR)_ , 2019. URL: https://openreview.net/forum?id=HyGIdiRqtm. 

- [95] Lillian Tsai and Eugene Bagdasarian. Contextual Agent Security: A Policy for Every Purpose. In _Proceedings of the 2025 Workshop on Hot Topics in Operating Systems_ , HotOS ’25, page 8–17, New York, NY, USA, 2025. Association for Computing Machinery. doi:10.1145/3713082.3730378. 

- [96] Eric Wallace, Kai Xiao, Reimar Leike, Lilian Weng, Johannes Heidecke, and Alex Beutel. The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions, 2024. URL: https:// arxiv.org/abs/2404.13208, arXiv:2404.13208. 

- [97] Shiqi Wang, Huan Zhang, Kaidi Xu, Xue Lin, Suman Jana, Cho-Jui Hsieh, and J Zico Kolter. Beta-CROWN: Efficient Bound Propagation with Per-neuron Split Constraints for Neural Network Robustness Verification. In _ICML 2021 Workshop on Adversarial Machine Learning_ , 2021. URL: https://openreview.net/forum?id=Mm3gxxTfT7A. 

- [98] Zhiqiang Wang, Junyang Zhang, Guanquan Shi, HaoRan Cheng, Yunhao Yao, Kaiwen Guo, Haohua Du, and Xiang-Yang Li. MindGuard: Tracking, Detecting, and Attributing MCP Tool Poisoning Attack via Decision Dependence Graph, 2025. URL: https://arxiv.org/abs/2508.20412, arXiv:2508.20412. 

- [99] Lily Weng, Huan Zhang, Hongge Chen, Zhao Song, Cho-Jui Hsieh, Luca Daniel, Duane Boning, and Inderjit Dhillon. Towards Fast Computation of Certified Robustness for ReLU Networks. In Jennifer Dy and Andreas Krause, editors, _Proceedings of the 35th International Conference on Machine Learning_ , volume 80 of _Proceedings of Machine Learning Research_ , pages 5276–5285. PMLR, 10–15 Jul 2018. URL: https://proceedings.mlr.press/v80/weng18a.html. 

- [100] Simon Willison. “I think ‘agent’ may Finally have a Widely Enough Agreed upon Definition to be useful Jargon now”. https://simonwillison.net/2025/Sep/18/agents/, 2025. Blog post, 18 September 2025. 

- [101] Fangzhou Wu, Ethan Cecchetti, and Chaowei Xiao. System-Level Defense against Indirect Prompt Injection Attacks: An Information Flow Control Perspective, 2024. URL: https://arxiv.org/abs/ 2409.19091, arXiv:2409.19091. 

- [102] Tong Wu, Shujian Zhang, Kaiqiang Song, Silei Xu, Sanqiang Zhao, Ravi Agrawal, Sathish Reddy Indurthi, Chong Xiang, Prateek Mittal, and Wenxuan Zhou. Instructional Segment Embedding: Improving LLM Safety with Instruction Hierarchy, 2025. URL: https://arxiv.org/abs/2410.09102, arXiv:2410.09102. 

23 

- [103] Yuhao Wu, Franziska Roesner, Tadayoshi Kohno, Ning Zhang, and Umar Iqbal. IsolateGPT: An Execution Isolation Architecture for LLM-Based Systems. In _Network and Distributed System Security Symposium (NDSS)_ , 2025. URL: https://www.ndss-symposium.org/ndss-paper/isolategpt-an-executionisolation-architecture-for-llm-based-agentic-systems/. 

- [104] Chong Xiang, Tong Wu, Zexuan Zhong, David Wagner, Danqi Chen, and Prateek Mittal. Certifiably Robust RAG against Retrieval Corruption, 2024. URL: https://arxiv.org/abs/2405.15556, arXiv: 2405.15556. 

- [105] Zhen Xiang, Linzhi Zheng, Yanjie Li, Junyuan Hong, Qinbin Li, Han Xie, Jiawei Zhang, Zidi Xiong, Chulin Xie, Carl Yang, Dawn Song, and Bo Li. GuardAgent: Safeguard LLM Agents by a Guard Agent via Knowledge-Enabled Reasoning, 2025. URL: https://arxiv.org/abs/2406.09187, arXiv:2406.09187. 

- [106] Chejian Xu, Mintong Kang, Jiawei Zhang, Zeyi Liao, Lingbo Mo, Mengqi Yuan, Huan Sun, and Bo Li. AdvAgent: Controllable Blackbox Red-teaming on Web Agents, 2025. URL: https://arxiv.org/abs/ 2410.17401, arXiv:2410.17401. 

- [107] Boyang Zhang, Yicong Tan, Yun Shen, Ahmed Salem, Michael Backes, Savvas Zannettou, and Yang Zhang. Breaking Agents: Compromising Autonomous LLM Agents through Malfunction Amplification. In _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ , pages 34952–34964, 2025. URL: https://aclanthology.org/2025.emnlp-main.1771/. 

- [108] Hanrong Zhang, Jingyuan Huang, Kai Mei, Yifei Yao, Zhenting Wang, Chenlu Zhan, Hongwei Wang, and Yongfeng Zhang. Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents, 2025. URL: https://arxiv.org/abs/2410.02644, arXiv:2410.02644. 

- [109] Huan Zhang, Tsui-Wei Weng, Pin-Yu Chen, Cho-Jui Hsieh, and Luca Daniel. Efficient Neural Network Robustness Certification with General Activation Functions. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 31, 2018. URL: https://proceedings.neurips.cc/paper_files/ paper/2018/file/d04863f100d59b3eb688a11f95b0ae60-Paper.pdf. 

- [110] Kaiyuan Zhang, Zian Su, Pin-Yu Chen, Elisa Bertino, Xiangyu Zhang, and Ninghui Li. LLM Agents Should Employ Security Principles, 2025. URL: https://arxiv.org/abs/2505.24019, arXiv:2505.24019. 

- [111] Yanzhe Zhang, Tao Yu, and Diyi Yang. Attacking Vision-Language Computer Agents via Pop-ups. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 8387–8401, 2025. URL: https://aclanthology.org/2025.acl-long.411/. 

- [112] Yuyang Zhang, Kangjie Chen, Jiaxin Gao, Ronghao Cui, Run Wang, Lina Wang, and Tianwei Zhang. Towards Action Hijacking of Large Language Model-based Agent, 2025. URL: https://arxiv.org/abs/ 2412.10807, arXiv:2412.10807. 

- [113] Peter Yong Zhong, Siyuan Chen, Ruiqi Wang, McKenna McCall, Ben L. Titzer, Heather Miller, and Phillip B. Gibbons. RTBAS: Defending LLM Agents Against Prompt Injection and Privacy Leakage, 2025. URL: https://arxiv.org/abs/2502.08966, arXiv:2502.08966. 

- [114] Andy Zou, Long Phan, Justin Wang, Derek Duenas, Maxwell Lin, Maksym Andriushchenko, Rowan Wang, Zico Kolter, Matt Fredrikson, and Dan Hendrycks. Improving Alignment and Robustness with Circuit Breakers, 2024. URL: https://arxiv.org/abs/2406.04313, arXiv:2406.04313. 

- [115] Andy Zou, Zifan Wang, Nicholas Carlini, Milad Nasr, J. Zico Kolter, and Matt Fredrikson. Universal and transferable adversarial attacks on aligned language models, 2023. URL: https://arxiv.org/abs/ 2307.15043, arXiv:2307.15043. 

- [116] Wei Zou, Runpeng Geng, Binghui Wang, and Jinyuan Jia. PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large :anguage Models. In _34th USENIX Security Symposium (USENIX Security 25)_ , pages 3827–3844, 2025. URL: https://www.usenix.org/conference/ usenixsecurity25/presentation/zou-poisonedrag. 

24 

- [117] Egor Zverev, Sahar Abdelnabi, Soroush Tabesh, Mario Fritz, and Christoph H. Lampert. Can LLMs Separate Instructions From Data? And What Do We Even Mean By That? In _The Thirteenth International Conference on Learning Representations (ICLR)_ , 2025. URL: https://iclr.cc/virtual/2024/ 23872. 

## **A Example: Claude Code Data Exfiltration** 


![](docs/paper-research/md-downloaded-paper-professor/images/10-systems-security-foundations-for-agentic-computing.pdf-0025-02.png)


Figure 2: CVE-2025-55284: Claude Code Data Exfiltration via DNS Lookup (Image Credit: Johann Rehberger/EmbraceTheRed). 

## **B Security Principles and Mechanisms** 

The standard security architecture consists of the trusted computing base (TCB), a security policy, the security boundary, and the untrusted system, as shown in Figure 3. The TCB consists of the functionality (code and data) whose integrity and confidentiality cannot be impacted by an attacker—in other words, the TCB defines the parts of the overall system that can be trusted to operate correctly under attack. The TCB typically contains the core functionality of the system (e.g., the kernel of the operating system) as well as a reference monitor that serves to approve or reject each request from the untrusted components to the TCB. The reference monitor is the part of the TCB that examines the security policy in order to make the approve/reject determination. The security policy is typically a declarative expression of the security goals—as an example, the security policy for stored files is given as a list of access control entries, each entry representing the operation(s) a given user is allowed to perform on a given file. The security boundary represents the interface through which the untrusted components interact with the TCB. In an OS, the security boundary between the OS kernel and the (untrusted) applications is the system-call interface. 

In layered system designs, the TCB crosses multiple layers, with each TCB layer providing some functionality that enables the TCB layers on top of it to create their own security guarantees. As an example, most contemporary hardware exposes memory-management functions, allowing the OS kernel to create isolated 

25 


![](docs/paper-research/md-downloaded-paper-professor/images/10-systems-security-foundations-for-agentic-computing.pdf-0026-00.png)


Figure 3: Standard security architecture. Requests and responses cross a security boundary between an untrusted system and the trusted computing base (TCB). The TCB consults the security policy to decide whether it is permitted to answer a given request. 

memory regions by managing the memory-access permissions carefully. In turn the OS kernel uses these isolated memory regions to separate applications from each other and exposes functions to enables applications to share code, data, files, and other resources. 

Within this context we define and describe the security principles referred to in the case studies of Section 3. 

**Principle of Least Privilege.** This principle dictates that the Security Policy should only grant the Untrusted System the _absolute minimum permissions_ it needs to function. For example, if the Untrusted System only needs to read a specific piece of data, the Security Policy should explicitly deny it permission to write, delete, or access any other data. The TCB is responsible for enforcing this minimal set of permissions, as specified by the Security Policy. For convenience most policies are written with the expectation of a _default-deny_ fallback, where access to a resource not explicitly listed in the policy is automatically rejected. 

**TCB Tamper Resistance.** This principle states that the TCB itself must be protected from modification by any outside influence. The Security Boundary must be designed to prevent the Untrusted System from altering the code or logic of the TCB or the Security Policy. If the TCB could be tampered with, an attacker could disable the “Check for permission” and bypass all security controls. 

**Complete Mediation.** This principle dictates that _every single_ request from the Untrusted System must be validated against the Security Policy. The system must not “remember” a previous authorization as users, trust levels, or other contextual conditions may have changed. Each time one of the requests crosses the Security Boundary, it must be intercepted by the TCB, which in turn must perform the “Check for permission to answer request” operation against the Security Policy. No request is allowed to bypass this check. 

**Secure Information Flow.** This principle governs the “Requests & Responses” channel, ensuring that sensitive information does not leak to untrusted areas. The Security Policy must define what kind of information is allowed to flow in which direction. For instance, even if a request is valid, the TCB must check the Security Policy to ensure that the resulting Response does not contain secret data that the Untrusted System is not authorized to see (this would constitute an unauthorized flow of data from high-trust components to low-trust components). 

**Human Weak Link.** This principle states that human operators can compromise this architecture in several ways, and thus the security mechanisms must be designed with this in mind. As a user, a human operating the Untrusted System could send malicious requests (e.g., SQL injection, prompt injection). As an administrator, a human could incorrectly configure the Security Policy, making it too permissive (violating 

26 

Least Privilege). As a developer, a human could accidentally introduce a bug into the TCB that fails to perform the _Check for permission_ operation correctly (violating Complete Mediation). 

A related principle, _Secure by Default_ , addresses some of the human weak-link concerns by ensuring that a newly deployed system comes with a default configuration that is secure, and that it becomes insecure only when the user changes that configuration. Secure by Default reduces the risk of damage at scale, as most users typically do not change the default configuration. While Human Weak Link is more general than Secure by Default (as it recommends hardening against inadvertent compromise even beyond the default configuration), for the purposes of this paper we use them interchangeably. 

This security architecture, together with the five principles above, ensures that the overall system is secure even when there are one or more untrusted components present. We note that security assessments performed in such a setting provide guarantees only for a given set of components (a certain version of the TCB, a certain set of request types and their semantics, and a security policy written with respect to these components). A change in the TCB or the Security Boundary requires a new assessment to determine whether the five principles still hold true. 

27 

