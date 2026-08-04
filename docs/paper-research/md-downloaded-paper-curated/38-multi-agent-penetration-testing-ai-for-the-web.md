# **Multi-Agent Penetration Testing AI for the Web** 

Isaac David Arthur Gervais _University College London University College London_ 

## **Abstract** 

AI-powered development platforms are making software creation accessible to a broader audience, but this democratization has triggered a scalability crisis in security auditing. With studies showing that up to 40% of AI-generated code contains vulnerabilities [21], the pace of development now vastly outstrips the capacity for thorough security assessment. 

We present MAPTA, a multi-agent system for autonomous web application security assessment that combines large language model orchestration with tool-grounded execution and end-to-end exploit validation. On the 104-challenge XBOW benchmark, MAPTA achieves 76.9% overall success with perfect performance on SSRF and misconfiguration vulnerabilities, 83% success on broken authorization, and strong results on injection attacks including server-side template injection (85%) and SQL injection (83%). Cross-site scripting (57%) and blind SQL injection (0%) remain challenging. Our comprehensive cost analysis across all challenges totals $21.38 with a median cost of $0.073 for successful attempts versus $0.357 for failures. Success correlates strongly with resource efficiency, enabling practical early-stopping thresholds at approximately 40 tool calls or $0.30 per challenge. 

MAPTA’s real-world findings are impactful given both the popularity of the respective scanned GitHub repositories (8K70K stars) and MAPTA’s low average operating cost of $3.67 per open-source assessment: MAPTA discovered critical vulnerabilities including RCEs, command injections, secret exposure, and arbitrary file write vulnerabilities. Findings are responsibly disclosed, 10 findings are under CVE review. 

## **1 Introduction** 

Web application security assessment faces a fundamental scalability crisis driven by AI-powered development acceleration. AI-assisted development platforms democratize application creation, enabling non-technical entrepreneurs and domain experts to build web services without traditional programming knowledge. However, this broader developer demographic 

lacks security expertise, creating applications with larger attack surfaces. The fastest-growing businesses today (from AI coding assistants to no-code platforms) accelerate application development, but security assessment remains constrained by manual processes and tools requiring human interpretation. 

The core challenge lies in the _semantic gap_ between patternbased vulnerability detection and contextual exploitation understanding. A SQL injection pattern in source code may be completely unexploitable due to prepared statements, input validation, or database permissions invisible to static analysis. Conversely, business logic vulnerabilities, particularly those involving multi-step attack chains, often evade detection by signature-based tools, as they exploit application-specific workflows rather than known patterns [1, 14]. Studies and industry reports emphasize that such flaws represent a significant share of real-world web application vulnerabilities, yet remain under-detected by automated scanners [23]. 

Recent advances in large language models (LLMs) and autonomous agent systems offer an approach to bridge this semantic gap. LLMs demonstrate reasoning capabilities about code semantics, security patterns, and exploitation strategies [4, 5]. However, applying these capabilities to penetration testing requires orchestration of tools and the meticulous verification of theoretical vulnerabilities through practical exploitation attempts, i.e. end-to-end proof-of-concept exploits. 

Pioneering research systems have demonstrated the viability of LLM-driven penetration testing. PentestGPT [8] established foundational multi-stage workflows for enumeration and exploitation, while PenHeal [13] advanced the field by coupling vulnerability discovery with automated remediation strategies. These systems validated the core premise that LLMs can reason about security assessment tasks and coordinate tool usage for autonomous testing. 

However, existing approaches face critical limitations: lack of rigorous cost-performance analysis along with insufficient vulnerability validation leading to false positives. While commercial systems like XBOW have emerged claiming competitive performance and contributing valuable benchmarks to the community, they lack scientific reproducibility in their core 

1 

methodologies, with only high-level descriptions available through blog posts rather than detailed system architectures or open-source implementations [10]. 

We present **MAPTA** (Multi-Agent Penetration Testing AI), to the best of our knowledge the first open-source multiagent penetration testing AI system for the web, enabling end-to-end, continuous penetration testing without human intervention. MAPTA’s approach fundamentally transforms security assessment from human-dependent pattern recognition to _adaptive adversarial execution_ , where AI agents autonomously reason about application behavior, adapt exploitation strategies, and validate vulnerabilities through concrete execution, matching the speed of AI-powered development. 

## **1.1 Key Insights and Contributions** 

Our work addresses the scalability-accuracy tradeoff in web application security through several key insights. Building on the foundational work of PentestGPT and PenHeal, MAPTA advances the state-of-the-art through rigorous costperformance measurement, mandatory proof-of-concept validation for all findings, and multi-agent orchestration that reduces the false positives and resource inefficiencies of prior approaches. Rather than a monolithic AI system, we employ a multi-agent architecture with a coordinator agent for strategic coordination and multiple sandbox agents for tactical execution. This separation enables high-level reasoning about attack strategies while maintaining secure, isolated execution of tools and exploits. LLMs require tools to conduct penetration testing, so our architecture integrates tools (nmap, python, ffuf) through orchestration, where agents reason about tool selection, parameter configuration, and result interpretation based on target application characteristics. We distinguish theoretical vulnerabilities from practical exploits through sandboxed proof-of-concept execution. This approach transforms vulnerability assessment from hypothesis generation to empirical validation, reducing false positives while providing actionable security intelligence. Our system adapts testing strategies based on discovered application characteristics, and importantly, partial exploitation results. This adaptation mimics human penetration tester reasoning while operating at machine scale and minutes of average assessment time. Our contributions include: 

- **Tool-grounded multi-agent architecture.** We design a three-agent-roles system where the Coordinator handles orchestration, Sandbox agents perform tactical execution within a shared per-job Docker container, and a Validation agent serves as end-to-end proof-of-concept oracles to eliminate theoretical findings and reduce false positives (Figure 1, Table 1, §2.1–2.3). 

- **Cost–performance accounting with actionable results.** We provide resource accounting across 104 XBOW challenges, tracking token-level I/O (3.2M regular input, 

- 50.5M cached, 1.10M output, 0.595M reasoning; $21.38 total) with a median cost of $0.117 per challenge. Our analysis reveals strong negative correlations between success and resource consumption (tools r = -0.661, cost -0.606, tokens -0.587, time -0.557), enabling practical early-stopping thresholds of approximately 40 tool calls, $0.30, or 300 seconds (§3.2–3.3, Table 2, Fig. 3–8). 

- **Black-box performance on modern web targets.** We achieve 76.9% success across 104 XBOW challenges, with perfect performance on SSRF and misconfiguration vulnerabilities and strong results on server-side template injection (85%), SQL injection (83%), and command injection (75%). We identify remaining performance gaps in areas such as blind SQL injection (0%) and cross-site scripting (57%) (§3.2, §3.4, Fig. 7, Table 2). 

- **Real-world white-box validation.** We demonstrate practical impact through testing ten popular open-source applications (8K–70K GitHub stars) across modern technology stacks including Next.js, React, Node.js, and Flask. This evaluation discovered 19 vulnerabilities, with 14 classified as high or critical severity and 10 pending CVE assignments, all accompanied by end-to-end proofof-concept exploits under responsible disclosure (§4.1). 

- **Open-science artifacts.** We provide the code, our evaluation results, and fixes for 43 out of 104 outdated XBOW Benchmark Docker images to enable reproducibility in autonomous security testing. 

## **2 Architecture** 

This section describes MAPTA’s multi-agent design that orchestrates specialized roles for autonomous penetration testing with mandatory proof-of-concept validation. 

## **2.1 Multi-Agent Architecture** 

MAPTA implements a three-role, tool-driven architecture that couples high-level planning with concrete exploit execution. A Coordinator agent performs strategy and delegation; Sandbox agents execute inside a single per-job Docker container; and a Validation agent converts candidate findings into verified, end-to-end PoCs. Orchestration is _dynamic_ —the Coordinator decides at runtime when to delegate to sandbox agents through the sandbox_agent tool versus acting directly—while resource handling uses thread-local isolation and per-scan accounting for elegant teardown, reproducibility, and concurrent safety. 

Within this work, an agent is an LLM-driven controller with (i) a goal (“obtain verified PoC for a target”), (ii) a bounded action space (security tools it may call and how to parameterize them), (iii) an observation stream (tool outputs, HTTP responses, code, telemetry), (iv) short-term memory/state (its 

2 


![](images/38-multi-agent-penetration-testing-ai-for-the-web.pdf-0003-00.png)


<!-- Start of picture text -->
CTF Mode:<br>Single agent Validation Legend:<br>Flag extraction Agent ToolCoordinationExecution<br>Real-World: PoC Validation<br>Multi-agent Data/Resource Flow<br>PoC validation<br>Candidate PoC<br>sandbox a gent<br>getlistsendgetsend r egistered a runrunccount ms essagelack s lack cp ommandythonsummary ma essages b lert e ymails i d Coordinator PoC Agent Storage Usage •••• ToolLLMWall-clockBudgetcallstokens Tracker: caps&time&latencycost<br>sandbox a gent delegate subtasks<br>Per-Job Docker Container<br>Sandbox Sandbox Sandbox<br>Agent 1 Agent 2 Agent N<br>run c ommand run c ommand run p ython<br>run p ython run p ython<br>via run c ommand via run c ommand via run p ython<br>Recon/Discovery: Web Testing: Python Script:<br>nmap, ffuf, nikto sqlmap, dirb import requests<br>amass, httpx jwt t ool, wafw00f r = requests.get(url)<br>if "admin" in r.text:<br>print("Found admin!")<br>ToolExecution<br>Target<br>Web App<br>(HTTP/HTTPS<br>or Source Code)<br><!-- End of picture text -->

Figure 1: **MAPTA multi-agent architecture** with singlepass controller with evidence-gated branching. Three roles: a _Coordinator_ (strategy and orchestration), one or more _Sandbox_ agents (tactical execution in an isolated per-job Docker environment), and a _Validation_ agent (concrete PoC execution and pass/fail evidence). The Coordinator dynamically decides whether to delegate to sandbox agents via the sandbox_agent tool or to execute commands directly; sandbox agents for the same job share a single virtual machine. 

working context and artifacts), and (v) termination/budget rules (stop on validated exploit or when cost/time/tool-call limits hit). In MAPTA this manifests concretely as rolespecialized agents—Coordinator (orchestrates), Sandbox (executes commands/code in an isolated per-job container), and Validation (turns a candidate into an end-to-end PoC and returns pass/fail evidence). 

**Coordinator Agent.** Responsible for attack-path reasoning, tool orchestration, and report synthesis. The coordinator operates with 8 tools: sandbox_agent (delegate to a sandbox agent), run_command, run_python, email workflow helpers get_registered_emails, list_account_messages, get_message_by_id, and alerting via send_slack_alert, send_slack_summary. 

**Sandbox Agents (1..N).** Execute tactical steps with _isolated LLM context_ for focus and to keep the Coordinator’s context clean. Each sandbox agent operates with 2 tools: run_command (shell) and run_python (Python). All sandbox agents spawned by the same Coordinator operate on the <u>same</u> per-job Docker container, enabling stateful reuse of filesystem artifacts, dependencies, credentials, and reconnaissance outputs across subtasks. 

**Validation Agent.** Consumes a candidate PoC artifact (HTTP request sequence, payload, or script) and _verifies exploitability by concrete execution_ on the per-job docker container, returning pass/fail with evidence (flag capture for CTF or side-effect evidence for real targets). The intent of this design is to reduce the reporting of theoretical findings. We understand that this could also potentially result in false negatives, where theoretical findings are valid and could materialize under a different state space. 

## **2.2 Threat Model** 

MAPTA operates under two distinct testing methodologies depending on the evaluation scenario, each representing different real-world penetration testing approaches. 

**Blackbox Local CTF Assessment.** For CTF challenges (XBOW benchmark evaluation), MAPTA operates under a pure _blackbox_ model from an _external attacker perspective_ . The system receives only (local) target URLs and challenge descriptions, without access to source code, database schemas, or internal configurations. Testing proceeds through behavioral analysis of application responses, error messages, timing characteristics, and other externally observable features to infer vulnerabilities and develop exploitation strategies. This approach mirrors real-world external penetration testing scenarios where attackers have no insider knowledge. 

**Whitebox Local Assessment.** For real-world application evaluation, MAPTA conducts _whitebox_ security assessments of locally cloned open-source repositories. This methodology provides complete source code access, enabling the agents to mimic static analysis, dependency vulnerability scanning, and code flow analysis to identify potential attack vectors. Applications are pulled, deployed and tested within virtual isolated local environments. 

Both methodologies operate within strict _ethical constraints_ , avoiding destructive operations, data exfiltration, or persistent system modifications. CTF testing targets purposebuilt vulnerable applications designed for security assessment, while whitebox testing occurs entirely within isolated local sandboxes to prevent any impact on production systems or third-party infrastructure. 

3 

Table 1: Agent Types and Tool Interfaces 

|**Agent Type**|**Tool Interface and Role**|
|---|---|
|**Coordinator**|Plans, orchestrates, synthesizes: sandbox_agent, run_command, run_python, get_registered_emails,|
||list_account_messages,get_message_by_id,send_slack_alert,send_slack_summary|
|**Sandbox (1..N)**|Executes tactics in isolated LLM context but shared container:run_command,run_python|
|**Validation**|Consumes and refnes candidate PoC; executes concretely; returns pass/fail with evidence|



## **2.3 Scope and Limitations** 

MAPTA targets web vulnerabilities that are (i) reachable over HTTP(S) and (ii) verifiable via concrete end-to-end PoCs, favoring classes where exploitability—not just pattern matches—can be demonstrated. In the evaluation we cover 13 categories spanning the majority of OWASP Top 10 (2021) and several OWASP API Top 10 (2023) families (Figure 7). 

Our primary focus encompasses access control vulnerabilities (A01), including insecure direct object references (IDOR), privilege escalation, and function-level authorization flaws that align with API security concerns such as BOLA and BFLA. These authorization weaknesses represented 29 challenges in our evaluation with 83% success rate, demonstrating MAPTA’s effectiveness in identifying access control bypasses through systematic privilege boundary testing. 

Injection vulnerabilities (A03) constitute another major evaluation category, spanning SQL injection, blind SQL injection, command injection, and server-side template injection (SSTI). We evaluate cross-site scripting (XSS) as a distinct injection vector due to its unique exploitation characteristics. MAPTA achieved strong performance on SSTI (85% success), standard SQL injection (83%), and command injection (75%), while showing challenges with XSS variants (57%) and complete difficulty with blind SQL injection scenarios (0% success), indicating areas for future improvement in timing-based attack detection. 

Security misconfigurations (A05) and server-side request forgery (A10) represent categories where MAPTA achieved perfect performance (100% success each). Misconfigurations include server configuration errors, CORS policy failures, and exposed administrative interfaces, while SSRF evaluation focuses on end-to-end exploitation demonstrating internal network access or cloud metadata extraction. Similarly, cryptographic failures and sensitive data exposure (A02) scenarios achieved 100% success where present in the dataset, covering weak randomness in secret generation and inadvertent credential leakage through client-side exposure. 

Authentication vulnerabilities (A07) encompass session management weaknesses, login bypass techniques, and broken authentication mechanisms, achieving 33% success rate in our evaluation. This lower performance indicates the complexity of authentication flow analysis and the need for enhanced session state reasoning. Business logic vulnerabilities classified under insecure design (A04) require multi-step rea- 

soning about application-specific workflows, while vulnerable and outdated components (A06) are detected through dependency analysis in white-box assessment mode with impact validation where feasible. 

**Limitations.** Our approach has several inherent limitations including the exclusion of network-level vulnerabilities such as SSL/TLS misconfigurations, network protocol vulnerabilities, or infrastructure security beyond what is discoverable through application-layer testing, and the inability to assess physical security controls, social engineering vulnerabilities, or human factors beyond what can be tested through technical means. We also do not evaluate OWASP A08 (Software & Data Integrity Failures) or A09 (Logging/Monitoring Failures). While our authorization testing results subsume key OWASP API Top 10 security issues such as the mentioned BOLA, BFLA, and related object-level authorization flaws, we do not target resource consumption, rate limiting, or API observability concerns in this work. 

While MAPTA reduces false positives through end-to-end proof-of-concept exploit generation and concrete execution with the validation agent within a virtual environment, we cannot guarantee zero false positives, particularly for complex business logic vulnerabilities. Business logic flaws often require a deeper understanding of application-specific workflows, user roles, and intended behaviors that may be difficult to distinguish from legitimate functionality through automated testing alone. For instance, a multi-step transaction that appears to bypass authorization controls may represent intended behavior under specific conditions not apparent to automated analysis. Future work may for example add automated canary placement systems that embed detectable markers throughout application workflows to provide additional exploitation validation. 

## **2.4 Orchestration Logic** 

MAPTA executes within a bounded loop. Each assessment progresses through four phases with explicit stop conditions (validated exploit, budget/time/tool-call caps). Figure 1 shows the roles and per-job container while Table 1 lists tool interfaces. As the orchestrator agent sees fit, the execution flow may begin with a _hypothesis synthesis_ , where the Coordinator derives likely attack surfaces and a prioritized set of probes with gating predicates (e.g., endpoint present, auth 

4 

state obtained) from the target description and early telemetry. This may then lead to _targeted dispatch_ , where probes are executed, either inline (run_command, run_python) or via sandbox_agent for focused sub-tasks such as payload crafting, enumeration bursts, or multi-step request sequences. Outputs are normalized into observations that feed the gating predicates with a global retry loop bounded by a maximum number of attempts. When preconditions for an exploit path are satisfied, the system may move to _PoC assembly_ , where the Coordinator constructs a minimal PoC artifact—whether a request sequence, payload, or script—together with an expected oracle or side-effect for verification. Finally, during _validation and finalization_ , the PoC is handed to the Validation agent for concrete execution or refinement, yielding a pass/fail result with evidence (flag in CTF scenarios; state change, data access, or RCE evidence in real-world assessments). The job terminates on a successful validation or when budget caps (time, tool calls, token/cost) are reached. CTF runs use a single agent and treat flag extraction as the oracle, while real-world runs employ the full Coordinator + Sandbox + Validation architecture with PoC-by-execution. Both operational modes share the same single-pass controller and per-job Docker isolation. 

## **2.5 Execution Environment and Isolation** 

Each assessment runs in _one_ Docker container per job, a virtual machine hosting a linux derivate, in our case Ubuntu. All agents attached to the same Coordinator share this container to amortize setup cost and retain state (installed toolchains, enumerations, downloaded artifacts). The container is ephemeral and terminated at job end. We distinguish _LLM context isolation_ (separate prompts/memory per sandbox agent to help agents to focus) from _system state sharing_ (single container), which reduces prompt bloat and cross-talk while preserving useful runtime state across sub-tasks. Only Docker is used as the isolation substrate in our deployment. 

**Job lifecycle and safety guarantees.** The job lifecycle follows three distinct phases: first, the system creates a fresh per-job container and injects only job-scoped credentials and configuration as needed; second, sandbox agents reuse the same container so that intermediate artifacts (auth cookies, wordlists, compiled helpers) persist across steps; and finally, on completion or failure, the system gracefully stops and removes the container, purges job-scoped secrets, and persists only evidence and minimal logs for reproducibility. This lifecycle yields predictable, low-overhead execution with isolation between concurrent jobs. 

## **2.6 Configurations: CTF vs Real-World** 

**CTF (blackbox).** In the CTF configuration, the system operates as a single agent (Coordinator only) where the Coor- 

dinator executes directly via run_command and run_python tools, and validation reduces to flag extraction as the groundtruth oracle. This configuration mirrors external attacker constraints and aligns to our knowledge with the XBOW evaluation methodology. Because the XBOW CTF challenges are blackbox based, they require less _context_ (no source) and have relatively simple web applications without extensive JavaScript code that we would expect in larger web applications. Hence, a single agent mode appears appropriate. 

**Real-World (whitebox).** For real-world assessments, we deploy the full multi-agent architecture comprising a Coordinator, one or more Sandbox agents, and a Validation agent. The Coordinator dynamically offloads tasks to sandbox agents (sharing the same per-job container) for targeted enumeration and exploit development, while the Validation agent executes proof-of-concept exploits end-to-end to confirm impact with concrete evidence such as state changes, data access, or remote code execution. 

## **2.7 Resource Handling and Observability** 

Each MAPTA sandbox agent runs in its own thread for parallelization, while we perform accounting with a per-scan UsageTracker: 

- **Tooling:** counts, latencies for run_command/run_python and delegation via sandbox_agent; 

- **LLM I/O:** input/output/cached/reasoning tokens and cost; 

- **Wall-clock:** end-to-end runtime. 

The tracker enables budget caps (cost/time/tool-call limits), early stopping when success likelihood drops, and graceful teardown on limit hit. Empirically, we observe negative correlations between success and resource use (tools, tokens, cost, and time) (see §3.3). 

Summarizing, MAPTA separates _orchestration_ (Coordinator) from _acting_ (Sandbox) and _verifying_ (Validation), maintains _context isolation_ for agent cognition while sharing a _single_ Docker runtime per job, and enforces _measure-first_ engineering through resource tracking and controlled teardown. 

## **3 CTF Evaluation** 

We evaluate MAPTA using the XBOW benchmark [25], a practical CTF benchmark for autonomous penetration testing evaluation. While we initially planned to include comparisons with the PentestGPT benchmark [8], the associated repository was unavailable at the time of evaluation. 

We therefore evaluate MAPTA using the XBOW benchmark, a collection of 104 web application security challenges designed for autonomous penetration testing evaluation. XBOW’s recognition as the #1 penetration testing 

5 

platform on HackerRank in 2025 underscores its industry relevance and challenge quality for evaluating autonomous security systems. Each challenge contains a specific security flaw with an associated flag that serves as proof of successful exploitation, creating a binary success metric that eliminates evaluation ambiguity—either the system finds the correct flag or it fails. 

Prior work has established that OpenAI’s models, particularly GPT-4, demonstrate superior performance compared to other publicly available LLMs on information security and penetration testing tasks [8, 13]. Industry practitioners, including XBOW’s commercial penetration testing platform, corroborate these findings through empirical deployment experience [26]. Given these established performance characteristics and to focus our limited financial resources, we focus our evaluation exclusively on GPT-5 under high-effort agent configurations throughout this work. 

The CTF evaluation operates under blackbox conditions where MAPTA receives only the _target URL and challenge description_ , matching real-world penetration testing scenarios. While the XBOW benchmark includes vulnerability type and category metadata in Docker readmes, we withheld these detailed classifications from MAPTA to ensure autonomous strategy determination based solely on observed application behavior. Challenge descriptions occasionally contained vulnerability hints, but this mirrors realistic penetration testing engagements where limited contextual information is available. Each challenge deploys as an isolated Docker container with standardized network configuration. 43 of the original 104 XBOW Docker images required manual fixes due to deprecated software versions—we completed extensive engineering efforts to restore functionality and plan to contribute these fixes back to the community via pull request to ensure continued dataset availability. We further have not found any online CTF solutions for this benchmark, and hence believe that MAPTAs solutions represent genuine discovery rather than model-trained regurgitation. 

## **3.1 Evaluation Metrics** 

We measure MAPTA’s performance using four objective metrics. First, we use a binary success metric for flag discovery: either MAPTA finds the correct flag (100% success) or fails (0% success). This eliminates false positive concerns since only correct exploitation yields the flag. Second, we measure time to solution as the total time from challenge start to flag discovery, measured in seconds, including reconnaissance, vulnerability analysis, and exploitation phases. Third, we track computational cost as the total cost in USD for LLM API calls, calculated using GPT-5 pricing at the time of writing ($1.25/1M input tokens, $10.00/1M output tokens, $0.125/1M cached tokens). Finally, we assess tool execution efficiency through the number of tool invocations required to reach the solution, measuring the efficiency of the agent’s 

exploration strategy. 


![](images/38-multi-agent-penetration-testing-ai-for-the-web.pdf-0006-06.png)


<!-- Start of picture text -->
Cumulative Distribution of Challenge Completion Times<br>100<br>All Challenges<br>Solved<br>Unsolved<br>80 Overall Median: 143.2s<br>Solved Median: 96.1s<br>Unsolved Median: 508.9s<br>60<br>40<br>20<br>0<br>0 200 400 600 800 1000 1200 1400<br>Total Time Spent on Challenge (seconds)<br>Cumulative Percentage (%)<br><!-- End of picture text -->

Figure 2: Cumulative distribution of challenge completion times showing the performance difference between solved and unsolved challenges. Solved challenges demonstrate faster completion with a median time of 96.1 seconds, while unsolved challenges show a median of 508.9 seconds. 

## **3.2 Results and Performance Analysis** 

MAPTA achieved a 76.9% success rate across the complete XBOW dataset, successfully solving 80 of 104 challenges. Table 2 presents performance metrics including timing, cost, and resource utilization characteristics. 

Our analysis reveals cost efficiency characteristics, as demonstrated in Figure 3. Challenges averaged $0.206 per attempt across the full dataset, with the cost breakdown revealing output tokens as the primary expense, reflecting the system’s analytical reasoning requirements. 

Examining _tool execution patterns_ , Figure 5 reveals adaptive tool selection with challenges averaging 25.1 tool calls per challenge. The distribution shows command execution heavily favored over Python runtime calls, indicating MAPTA’s preference for direct tool calling. Complex challenges demonstrate the system’s persistent approach to multi-step vulnerability analysis. Figure 6 shows curl as the dominant command across all challenges, reflecting the HTTP-centric nature of web application testing, while bash usage patterns indicate sophisticated exploitation scenarios requiring shell access. 

The _temporal performance characteristics_ illustrated in Figure 2 demonstrate efficient exploitation capabilities. The 275.0-second average solution time reflects the full dataset complexity, with a median solve time of 143.2 seconds indicating consistent performance for most challenges, while the maximum time of 1428.7 seconds represents the most complex failed challenges that reached timeout limits. 

Finally, our _token utilization analysis_ in Figure 4 reveals efficient usage patterns across different categories. Cached tokens comprise the largest portion of total token usage, contributing to cost reduction through context reuse. Also, higher 

6 

Table 2: MAPTA’s performance on the 104 XBOW Benchmark Challenge 

|**Metric**|**Value**|**Metric**|**Value**|
|---|---|---|---|
|Total Challenges|104|Success Rate|76.9%|
|Successful Challenges|80|Failed Challenges|24|
|Avg. Solve Time|275.0s|Median Solve Time|143.2s|
|Min Solve Time|26.3s|Max Solve Time|1428.7s|
|Total Regular Input Tokens|3,244,880|Total Output Tokens|1,100,790|
|Total Cached Tokens|50,524,032|Total Reasoning Tokens|594,880|
|Total Token Cost|$21.38|Avg. Cost per Challenge|$0.206|
|Total Commands|2613|Avg. Commands per Challenge|25.1|




![](images/38-multi-agent-penetration-testing-ai-for-the-web.pdf-0007-02.png)


<!-- Start of picture text -->
CDF of Total Costs Cost Breakdown by Challenge<br>100 Regular Input<br>Cached Input<br>Output<br>0.8<br>80<br>0.6<br>60<br>40 0.4<br>All Challenges<br>Solved<br>20 Unsolved 0.2<br>Overall Median: $0.117<br>Solved Median: $0.073<br>0 Unsolved Median: $0.357<br>0.0<br>0.0 0.2 0.4 0.6 0.8<br>Total Cost (USD)<br>Challenge<br>Ch1 Ch11 Ch21 Ch31 Ch41 Ch51 Ch61 Ch71 Ch81 Ch91 Ch101<br>Cost (USD)<br>Cumulative Percentage (%)<br><!-- End of picture text -->

Figure 3: CDF of total costs (left) and per-challenge cost by token type (right). Solved challenges maintain lower median costs ($0.073) compared to unsolved challenges ($0.357), with output tokens representing the largest cost component. 

reasoning token usage correlates with challenge complexity and multi-step exploitation scenarios. 

## **3.3 Resources and Success Correlations** 

- Our correlation analysis (point biserial, Pearson with binary outcome and N=104) across all challenge metrics reveals negative correlations between success and resource utilization, providing insights into agent behavior and efficiency patterns. All correlations are statistically significant (p<0.001). 

1. Tool Usage vs Success (r=-0.661). The negative correlation indicates that more tool calls correlate with lower success rates, suggesting that failed attempts involve more exploratory tool usage as the agent struggles to find viable attack vectors. 

2. Cost vs Success (r=-0.606). Higher computational costs associate with failures, indicating that failed challenges consume more expensive resources through extended reasoning cycles and repeated tool invocations. 

3. Token Usage vs Success (r=-0.587). More tokens used in unsuccessful attempts, possibly due to longer reasoning and exploration cycles as the agent attempts multiple approaches without finding successful exploitation paths. 

4. Time vs Success (r=-0.557). Longer time spent correlates with failure, showing a clear pattern of quick successes versus prolonged unsuccessful attempts. 

These correlations reveal a clear _efficiency pattern_ : successful challenges tend to be solved quickly with fewer resources, while failed challenges involve extensive exploration, more 

7 


![](images/38-multi-agent-penetration-testing-ai-for-the-web.pdf-0008-00.png)


<!-- Start of picture text -->
Cumulative Distribution of Token Usage by Type<br>100<br>Input Tokens<br>Output Tokens<br>Cached Tokens<br>Reasoning Tokens<br>80 Total Tokens<br>60<br>40<br>20<br>0<br>10 2 10 3 10 4 10 5 10 6<br>Number of Tokens<br>Cumulative Percentage (%)<br><!-- End of picture text -->

Figure 4: Cumulative distribution of token usage across token types. The analysis reveals a cached token utilization, which contributes to cost efficiency, while reasoning tokens demonstrate the system’s analytical processing requirements. 

tools, longer reasoning, and higher costs. The agent appears to recognize successful paths quickly but struggles with certain challenge types despite increased resource investment. This suggests challenges may have distinct "solvable" versus "unsolvable" categories for this agent configuration, indicating opportunities for implementing early stopping mechanisms to optimize resource utilization. 

**Statistical Interpretation and Limitations.** While these correlations are statistically significant with substantial effect sizes (r=-0.661 explains 44% of variance in success), several caveats merit consideration. The binary nature of our outcome variable (success/failure) somewhat limits correlation interpretation compared to continuous outcomes. More importantly, correlation does not imply causation—these relationships likely reflect underlying challenge difficulty rather than resource usage directly causing failure. Difficult challenges require more exploration attempts, leading to higher resource consumption regardless of the agent’s capability. 

**Practical Value.** Nevertheless, these patterns remain meaningful and actionable for system optimization. Specifically, _production deployments can implement early stopping_ when tool usage exceeds 40+ calls (95th percentile of successful challenges), cost surpasses $0.30 per target (indicating likely failure), or execution time reaches 300+ seconds without significant progress. For resource budgeting, organizations can allocate $0.073 per target for successful assessments versus $0.357 for exploration of difficult targets, enabling costpredictable security assessment workflows. 

## **3.4 Vulnerability Category Performance** 

Figure 7 presents MAPTA’s performance across 13 distinct vulnerability categories using the complete 104-challenge XBOW dataset. The Sankey flow visualization reveals both overall success patterns and category-specific performance characteristics that inform system optimization strategies. 

**Overall Performance.** MAPTA achieved a success rate of 76.9% (80/104 challenges), demonstrating performance across diverse vulnerability types. This performance approaches XBOW’s reported 84.6% coverage in July 2024, achieving within 7.7 percentage points of the commercial system’s claimed performance. Notably, XBOW has not published detailed methodology, system architecture, or reproducible evaluation protocols beyond high-level blog posts with sample prompts, making independent verification impossible. In contrast, MAPTA provides transparency with opensource implementation, detailed architectural descriptions, and evaluation methodology. To our knowledge, MAPTA represents the first open-source penetration testing AI system achieving competitive performance with commercial alternatives while maintaining scientific reproducibility. 

**Injection Vulnerability Performance.** The analysis reveals nuanced performance across injection vulnerability subtypes. Server-Side Template Injection (SSTI) shows exceptional performance with 85% success rate (11/13 challenges), indicating MAPTA’s capability in template injection analysis. SQL Injection maintains high success at 83% (5/6 challenges), while Command Injection achieves 75% success (6/8 challenges). However, Cross-Site Scripting (XSS) demonstrates lower success at 57% (13/23 challenges) despite being the largest category, and Blind SQL Injection shows 0% success rate (0/3 challenges), representing the most challenging category for the current system. 

**Authorization and Authentication.** Broken Authorization challenges achieve 83% success rate (24/29 challenges), demonstrating capability in identifying IDOR, path traversal, and privilege escalation vulnerabilities. However, Broken Authentication shows lower performance at 33% success (1/3 challenges), indicating areas for improvement in authentication bypass techniques. 

**High-Performance Categories.** Several categories demonstrate perfect or near-perfect success rates: Server-Side Request Forgery (100%, 3/3), Misconfiguration (100%, 3/3), Sensitive Data Exposure (100%, 2/2), and Cryptographic vulnerabilities (100%, 1/1). These results indicate MAPTA’s capability in network-based attacks. 

**Performance Insights.** The category-specific analysis reveals that MAPTA excels at vulnerabilities requiring systematic analysis and tool-based discovery (SSRF, misconfigurations, SQL injection) but struggles with vulnerabilities requiring complex payload crafting or timing-based analysis (Blind SQL injection, certain XSS variants). This performance pattern suggests optimization opportunities through enhanced payload generation and feedback-based exploration strategies. 

## **3.5 Failure Analysis** 

Analysis of the 24 failed challenges (23.1% of the dataset) reveals specific patterns and areas for improvement in autonomous penetration testing. Failed challenges consumed 

8 


![](images/38-multi-agent-penetration-testing-ai-for-the-web.pdf-0009-00.png)


<!-- Start of picture text -->
Distribution of Tool Usage per Challenge Total Tool Calls per Challenge<br>80 80<br>60 60<br>40 40<br>20<br>20<br>0<br>0<br>Figure 5: Tool usage patterns across challenges showing the distribution of command execution calls versus Python runtime calls<br>(left) and total tool invocations per challenge (right).<br>Command Usage by Challenge<br>Ch1<br>Ch6<br>Ch11<br>Ch16 60<br>Ch21<br>Ch26<br>Ch31 50<br>Ch36<br>Ch41<br>40<br>Ch46<br>Ch51<br>Ch56 30<br>Ch61<br>Ch66<br>20<br>Ch71<br>Ch76<br>Ch81 10<br>Ch86<br>Ch91<br>0<br>Ch96<br>Ch101<br>Command<br>Run Command Run Python Ch1 Ch11 Ch21 Ch31 Ch41 Ch51 Ch61 Ch71 Ch81 Ch91 Ch101<br>#(curl(echo/bin/bash/usr/bin/time/bin/shDISPLAY=:0START=$(datebash catcurldirsearchdirb feroxbusterecho ffuffindgobusterh2csmugglerfor lsmkdirmulti(){ ncnmapnodenodejsphantomjs pipprintfpythonpython3 qjs rm sedsmuggler.pyurls=("....//FLAG.php"sh sshpass wgetwhichwpscan<br>Total Calls<br>Number of Calls<br>Challenge<br>Command Usage Count<br><!-- End of picture text -->

Figure 5: Tool usage patterns across challenges showing the distribution of command execution calls versus Python runtime calls (left) and total tool invocations per challenge (right). 

Figure 6: Command usage heatmap across challenges showing the frequency of specific commands used. The curl command dominates, reflecting the HTTP-centric nature of web application testing, bash usage indicates complex exploitation scenarios. 

9 

XBOW Challenge Analysis: Outcomes and Vulnerability Types 


![](images/38-multi-agent-penetration-testing-ai-for-the-web.pdf-0010-01.png)


<!-- Start of picture text -->
Broken Authorization (29) Broken Authorization (29) Broken Authorization (29)Broken Authorization (29)<br><!-- End of picture text -->


![](images/38-multi-agent-penetration-testing-ai-for-the-web.pdf-0010-02.png)


<!-- Start of picture text -->
All Benchmarks (104) All Benchmarks (104) All Benchmarks (104)All Benchmarks (104)<br><!-- End of picture text -->


![](images/38-multi-agent-penetration-testing-ai-for-the-web.pdf-0010-03.png)


<!-- Start of picture text -->
Cross-Site Scripting (XSS) (23) Cross-Site Scripting (XSS) (23) Cross-Site Scripting (XSS) (23)Cross-Site Scripting (XSS) (23)<br>Succeeded (80) Succeeded (80) Succeeded (80)Succeeded (80)<br><!-- End of picture text -->


![](images/38-multi-agent-penetration-testing-ai-for-the-web.pdf-0010-04.png)


<!-- Start of picture text -->
Server-Side Template Injection (SSTI) (13) Server-Side Template Injection (SSTI) (13) Server-Side Template Injection (SSTI) (13)Server-Side Template Injection (SSTI) (13)<br><!-- End of picture text -->


![](images/38-multi-agent-penetration-testing-ai-for-the-web.pdf-0010-05.png)


<!-- Start of picture text -->
Command Injection (8) Command Injection (8) Command Injection (8)Command Injection (8)<br>SQL Injection (6) SQL Injection (6) SQL Injection (6)SQL Injection (6)<br>Insecure Design (7) Insecure Design (7) Insecure Design (7)Insecure Design (7)Insecure Design (7)<br>Broken Authentication (3) Broken Authentication (3) Broken Authentication (3)Broken Authentication (3)Broken Authentication (3)<br>Misconfiguration (3) Misconfiguration (3) Misconfiguration (3)Misconfiguration (3)Misconfiguration (3)<br><!-- End of picture text -->


![](images/38-multi-agent-penetration-testing-ai-for-the-web.pdf-0010-06.png)


<!-- Start of picture text -->
Insecure Design (7) Insecure Design (7) Insecure Design (7)Insecure Design (7)Insecure Design (7)<br>Broken Authentication (3) Broken Authentication (3) Broken Authentication (3)Broken Authentication (3)Broken Authentication (3)<br>Misconfiguration (3) Misconfiguration (3) Misconfiguration (3)Misconfiguration (3)Misconfiguration (3)<br>Server-Side Request Forgery (SSRF) (3) Server-Side Request Forgery (SSRF) (3) Server-Side Request Forgery (SSRF) (3)Server-Side Request Forgery (SSRF) (3)Failed (24) Failed (24) Failed (24)Failed (24)Sensitive Data Exposure (2) Sensitive Data Exposure (2) Sensitive Data Exposure (2)Sensitive Data Exposure (2)<br>Crypto (1) Crypto (1) Crypto (1)Crypto (1)Crypto (1)<br>Blind SQL Injection (3) Blind SQL Injection (3) Blind SQL Injection (3)Blind SQL Injection (3)Blind SQL Injection (3)<br>Vulnerable Component (3) Vulnerable Component (3) Vulnerable Component (3)Vulnerable Component (3)Vulnerable Component (3)<br><!-- End of picture text -->


![](images/38-multi-agent-penetration-testing-ai-for-the-web.pdf-0010-07.png)


<!-- Start of picture text -->
Crypto (1) Crypto (1) Crypto (1)Crypto (1)Crypto (1)<br>Blind SQL Injection (3) Blind SQL Injection (3) Blind SQL Injection (3)Blind SQL Injection (3)Blind SQL Injection (3)<br>Vulnerable Component (3) Vulnerable Component (3) Vulnerable Component (3)Vulnerable Component (3)Vulnerable Component (3)<br><!-- End of picture text -->

Figure 7: Vulnerability category distribution across 104 XBOW challenges. 13 categories spanning 8/10 OWASP Top-10 (2021) (A01–A07, A10); excluding A08/A09. 


![](images/38-multi-agent-penetration-testing-ai-for-the-web.pdf-0010-09.png)


<!-- Start of picture text -->
Time Distribution by Outcome Cost Distribution by Outcome<br>r = -0.557 r = -0.606<br>0.8<br>1000<br>0.6<br>0.4<br>500<br>0.2<br>0 0.0<br>Failed Solved Failed Solved<br>Token Distribution by Outcome Tool Usage Distribution by Outcome<br>r = -0.587 80 r = -0.661<br>10 6<br>60<br>10 5 40<br>20<br>10 4 0<br>Failed Solved Failed Solved<br>Total Cost (USD)<br>Total Time (seconds)<br>Total Tokens<br>Total Tool Calls<br><!-- End of picture text -->

Figure 8: Correlation analysis between challenge success and resource utilization metrics. Negative correlations indicate that successful challenges are solved efficiently, while failed attempts involve higher costs. 


![](images/38-multi-agent-penetration-testing-ai-for-the-web.pdf-0010-11.png)


<!-- Start of picture text -->
Vulnerability Distribution and Cost by Target Application<br>6<br>High/CriticalMedium Assessment Cost 8<br>Low/Info<br>5 7<br>4 6<br>3 5<br>4<br>2<br>3<br>1<br>2<br>0<br>Target Application<br>OSN-06 OSN-03 OSN-04 OSN-05 OSN-01 OSN-02appsmithorg/appsmithdirectus/directusgo-gitea/giteagrafana/grafana<br>Assessment Cost (USD)<br>Number of Vulnerabilities<br><!-- End of picture text -->

Figure 9: Vulnerability distribution and assessment costs across targets. The stacked bars show vulnerability severity levels, while the orange line indicates assessment costs. 

significantly higher computational resources, with maximum execution times reaching 1428.7 seconds and higher average costs per attempt. The correlation analysis confirms this pattern, showing that resource-intensive challenges typically indicate unsuccessful exploitation attempts. 

The failure distribution across vulnerability categories provides actionable insights: Blind SQL Injection represents the most challenging category with 0% success rate, indicating limitations in timing-based attack detection and payload refinement. XSS challenges show moderate success (57%) despite representing the largest category, suggesting opportunities for enhanced payload generation and DOM manipulation strategies. Broken Authentication failures (67% failure rate) highlight the need for improved credential analysis and session manipulation capabilities. 

## **4 Real-World Application Assessment** 

To evaluate MAPTA’s effectiveness beyond controlled environments, we conducted assessments on 10 production opensource web application code spanning 51K-1.3M lines of code with GitHub popularity ranging from 8K-70K stars. These applications represent diverse architectural patterns including React/Next.js frontends, Node.js/Python backends, and containerized microservice deployments. Each assessment followed a standardized protocol: (1) automated repository fetching, (2) dynamic application deployment in an isolated sandbox environment, followed by (4) a payload-guided vulnerability exploration using MAPTA’s multi-agent architecture. The main agent averaged 620K tokens for planning and coordination, while sandbox agents consumed 413K-7.3M tokens for hands-on security testing, reflecting the computational intensity of practical vulnerability discovery. 

10 

Table 3: Per-Target Vulnerability Assessment Results with Token Breakdown by Agent 

|**Target**|**GitHub**<br>_⋆_|**Mai**<br>**Regular**|**n Agent Tok**<br>**Cached**|**ens**<br>**Output**|**Sandb**<br>**Regular**|**ox Agent T**<br>**Cached**|**okens**<br>**Output**|**Vu**<br>**H**|**lnerabilities**<br>**M**<br>**L**|**Cost**<br>**($)**|
|---|---|---|---|---|---|---|---|---|---|---|
|OSN-06|21K|22K|270K|12K|322K|6.9M|70K|4|2<br>0|4.85|
|OSN-03|9K|9K|17K|11K|28K|372K|23K|5|1<br>0|1.57|
|OSN-04|18K|47K|834K|15K|176K|1.1M|117K|1|1<br>1|6.05|
|OSN-05|36K|40K|615K|20K|253K|1.7M|116K|2|0<br>0|6.55|
|OSN-01|26K|221K|3.8M|18K|182K|200K|180K|1|0<br>0|8.02|
|OSN-02|8K|8K|18K|8K|79K|657K|30K|1|0<br>0|1.97|
|appsmith|38K|12K|35K|9K|40K|339K|34K|0|0<br>0|2.11|
|directus|32K|11K|58K|11K|40K|536K|34K|0|0<br>0|1.97|
|gitea|50K|9K|18K|9K|131K|1.4M|27K|0|0<br>0|1.93|
|grafana|70K|7K|25K|10K|254K|432K|19K|0|0<br>0|1.73|




![](images/38-multi-agent-penetration-testing-ai-for-the-web.pdf-0011-02.png)


<!-- Start of picture text -->
Assessment Time vs Vulnerability Discovery<br>OSN-03: Other (+5) OSN-06: Other (+5)<br>6 r = 0.299<br>5<br>4<br>OSN-04: Other (+2)<br>3<br>OSN-05: Other, Other<br>2<br>1 OSN-02: Other OSN-01: Other<br>0<br>35 40 45 50 55 60 65 70<br>Assessment Time (minutes)<br>grafana/grafana directus/directus go-gitea/gitea appsmithorg/appsmith<br>Vulnerabilities Found<br><!-- End of picture text -->

Figure 10: Assessment time versus vulnerability discovery patterns. Labels indicate the types of vulnerabilities found. 

## **4.1 Vulnerability Discovery Results** 

**Responsible Disclosure Note:** In accordance with responsible disclosure practices, we have anonymized the identities of applications where vulnerabilities were discovered, using obfuscated names (OSN-XX) for these targets. Applications where no vulnerabilities were found (appsmithorg/appsmith, directus/directus, go-gitea/gitea, grafana/grafana) are identified by their repository names to demonstrate the breadth of our evaluation across diverse, production-grade codebases. 

MAPTA identified 19 vulnerabilities across 6 applications (60% discovery rate), with a severity distribution of 73.7% High/Critical, 21.1% Medium, and 5.3% Low/Informational. Assessment costs averaged $3.67 per application over 50.7 minutes, demonstrating practical feasibility for continuous security testing workflows. Figure 9 illustrates the relationship between vulnerability discovery and assessment costs across target applications, showing that cost does not directly correlate with findings—some of the most expensive assessments 

yielded no vulnerabilities while others discovered critical issues at lower computational cost. 

### **Example Critical Vulnerabilities Discovered:** 

- **Command Injection via Database Export** : Direct shell command construction enabling arbitrary code execution through PostgreSQL connection parameters (PGPASSWORD="$this.config.password" pg_dump -schema-only "$input") 

- **Client-Side Secret Exposure** : Server-side API keys delivered via JavaScript configuration endpoints (window.env = {OPENAI_API_KEY: "$OPENAI_API_KEY"}) 

- **postMessage RCE** : Arbitrary code execution through overly permissive cross-frame origin validation (case ’builder.evaluate’: new Function(text)) 

- **Unauthenticated Email Relay with SSRF** : Public API endpoints accepting arbitrary SMTP credentials and remote attachment URLs (fileUrls: "http://169.254.169.254/latest/meta-data/") 

- **Arbitrary File Write via Client-Controlled Tools** : Remote clients enabling dangerous file operations through tool merging (input.tools override enabling PatchTool) 

### **Example High Severity Patterns:** 

- **Unauthenticated API Integration Abuse** : Third-party service access using attacker-supplied credential IDs (Google Sheets, Stripe PaymentIntent creation) 

- **Insecure Cryptographic Implementation** : Noncryptographic RNG for API key generation (Math.random() for 64-character secret keys) 

- **Path Traversal via File Access APIs** : Unvalidated file path parameters enabling arbitrary file reads (File.read(path) without containment checks) 

11 

- **Unauthenticated Administrative Endpoints** : Critical system operations exposed without authorization (/share_delete_admin clearing Durable Objects) 

### **Example Medium Severity Patterns:** 

- **XSS via Environment Injection** : Unescaped serverside template rendering in configuration endpoints ("$OPENAI_API_ENDPOINT" string interpolation) 

- **CSRF Across REST APIs** : State-changing operations without Origin validation or CSRF tokens (API token creation, user invitations) 

- **SSRF via Integration APIs** : Server-side request forgery through legitimate webhook and file import functionality 

- **Open Redirect via Payment Flows** : Unchecked URL parameters in checkout processes (success_url, cancel_url) 

## **5 Related Work** 

## **5.1 Classical Automated Web Security Testing** 

Traditional automated security testing approaches have evolved significantly over the past two decades, yet fundamental limitations persist that motivate advanced AI-driven solutions like MAPTA. 

Dynamic scanners like OWASP ZAP [20] and Burp Suite [22] crawl web applications and fuzz HTTP parameters to identify common vulnerabilities. While valuable for baseline security assessment, traditional DAST approaches suffer from limitations when testing modern web applications. Single-page applications with dynamic JavaScript content may evade crawling, and business logic vulnerabilities requiring multi-step interactions remain largely undetectable due to scanners’ lack of contextual understanding for complex application workflows. 

Static analysis tools examine source code to identify potential vulnerabilities without execution. However, empirical evaluations reveal significant limitations: a study of seven Java SAST tools found only 12.7% of real-world vulnerabilities were detected, with the union of all tools missing 71% [16]. Poor detection rates stem from challenges in modeling complex data flows, handling dynamic language features, and reasoning about runtime exploitability conditions. SAST tools generate high false positive rates due to conservative assumptions, while struggling with vulnerability classes requiring runtime context. This gap between theoretical detection and practical exploitability directly motivates MAPTA’s verify-by-execution approach. 

Hybrid approaches combine static analysis with runtime instrumentation to reduce false positives by validating execution paths. However, deployment challenges limit adoption 

due to instrumentation requirements, performance overhead, and complexity across microservices and containers. 

API-driven architectures introduce vulnerability classes that traditional scanners struggle with. The OWASP API Security Top 10 (2023) [17] highlights business logic vulnerabilities like BOLA, BFLA, and IDOR requiring understanding of application-specific access controls. These vulnerabilities demand stateful interaction sequences and reasoning about intended versus actual behavior. 

## **5.2 Stateful REST/API Fuzzing** 

Traditional stateless fuzzing fails to detect business logic vulnerabilities, motivating stateful approaches that maintain application state across multi-step sequences. 

Microsoft Research’s RESTler [3] introduced request dependency graphs from OpenAPI specifications, analyzing relationships between API calls to construct meaningful multistep interaction sequences. RESTler’s success in discovering vulnerabilities in Azure and Office365 demonstrates the value of dependency-aware testing over naive parameter fuzzing. Extensions like Pythia [2] add coverage feedback and learning-based mutations for more targeted exploration. 

Specialized frameworks like Yelp’s fuzz-lightyear target specific vulnerability classes (IDOR/BOLA) through stateful Swagger-based fuzzing. These tools demonstrate that effective business logic detection requires understanding semantic relationships between data objects and authorization controls—the fundamental pattern MAPTA generalizes through statefulness, property checks, and oracle-backed validation. 

## **5.3 LLMs for Secure Code** 

Large Language Models show promise for cybersecurity tasks but have significant limitations that inform MAPTA’s design. 

GitHub Copilot generates code containing vulnerabilities in 40% of CWE-targeted scenarios [21], stemming from reproducing insecure patterns in training data. These AI-generated flaws often appear functionally correct but contain subtle security issues in input validation, authentication, or cryptographic implementation that evade traditional code review. 

Comprehensive surveys [6] show that while LLMs excel at security reasoning and hypothesis generation, they require external oracles and environment feedback to validate outputs and avoid hallucinations—a pattern MAPTA addresses through tool integration and concrete execution. 

Google’s Big Sleep project discovered a zero-day in SQLite (November 2024) and helped foil exploitation [11, 12]. However, it remains closed-source without technical details, preventing independent verification or scientific advancement. This opacity exemplifies the broader challenge in AI security research where commercial systems achieve results but fail to advance understanding due to proprietary constraints—motivating MAPTA’s open science approach. 

12 

## **5.4 LLM-Driven Autonomous Testing and Tool Orchestration** 

Autonomous penetration testing systems represent evolution from static detection toward dynamic, reasoning-based assessment enabled by sophisticated tool orchestration. Recent advances in agentic AI systems demonstrate that tool interaction fundamentals impact performance across complex domains. ReAct [28] and Toolformer [24] established that LLMs achieve superior performance through structured tool interaction and environmental feedback loops, while SWE-agent [27] demonstrates that interface design and tool abstractions determine success rates on complex technical tasks. 

PentestGPT [8] pioneered multi-stage LLM workflows for enumeration, exploitation, and privilege escalation with selfinteraction capabilities. PentestGPT operates through hardcoded interactive loops with optional human oversight, limiting scalability for continuous large scale assessment workflows. Additionally, the system lacks true agentic capabilities—the PentestGPT project explicitly states that “PentestGPT v2.0 agentic upgrade will be ready soon,” indicating current limitations in autonomous decision-making and tool orchestration. While contributing structured prompting techniques and evaluation metrics, the system revealed limitations in long-horizon state management and vulnerability validation. The system reports aggregate costs ($131.5 for 10 HTB machines; $5.1 average per picoMini attempt) and discusses token conservation strategies with GPT-4-32k context limits. 

Subsequent research addresses these limitations through complementary approaches: PenHeal [13] couples discovery with remediation using knapsack optimization but does not report token usage—the “cost” metric represents remediation scoring rather than LLM operational expenses. RefPentester [7] adds self-reflection and knowledge-guided planning, while browser-capable agents [15] enable direct web interaction for CSRF/SSRF testing. 

MAPTA advances autonomous security assessment through resource measurement and operational efficiency analysis that addresses fundamental gaps in prior work. Our evaluation provides complete token-level accounting across 104 XBOW challenges: 3.2M regular input, 1.10M output, 50.5M cached, and 0.595M reasoning tokens, totaling $21.38 overall cost with median $0.117 per challenge. This granular breakdown reveals output tokens as the primary cost driver, enabling resource optimization strategies unavailable prior. 

Beyond cost accounting, MAPTA quantifies negative correlations between resource utilization and success—tool calls (r=-0.661), dollar cost (r=-0.606), tokens (r=-0.587), and time (r=-0.557)—providing actionable early-stopping heuristics and budget allocation guidance for production deployments. Our multi-agent architecture employs a coordinator/sandbox design with dynamic tool use, combined with end-to-end proof-of-concept validation that eliminates the false positives inherent in theoretical detection approaches. While prior sys- 

tems discuss token pressure mitigation strategies, MAPTA measures and quantifies the complete operational profile, establishing the first rigorous cost-performance framework for autonomous penetration testing systems. 

## **5.5 Benchmarks and Testbeds** 

Traditional vulnerable applications (Juice Shop [18], WebGoat [19], DVWA [9]) focus on vulnerability types with implementations unsuitable for evaluating advanced systems. The XBOW benchmark dataset [25] represents significant advancement by providing modern web application challenges with REST APIs, complex business logic, and realistic authentication mechanisms. XBOW’s key innovation emphasizes exploit execution validation over theoretical detection—each challenge requires actual exploitation success, eliminating false positives and aligning with real-world penetration testing objectives. Our approach builds on the fundamental insight from related work that effective automated security assessment requires tool orchestration, stateful reasoning, and practical verification [3, 28]. MAPTA’s multi-agent architecture with sandboxed exploit validation directly addresses the limitations identified in single-agent systems like PentestGPT [8] and traditional scanners’ false-positive challenges [16]. 

## **6 Conclusion** 

MAPTA demonstrates that multi-agent architectures can achieve competitive autonomous web application security assessment at practical scale. Our evaluation across 104 XBOW challenges achieves 76.9% success with perfect performance on SSRF and misconfiguration vulnerabilities, while revealing systematic weaknesses in blind SQL injection (0%) and cross-site scripting (57%). The comprehensive cost accounting totaling $21.38 establishes the first rigorous resource model for autonomous penetration testing, with median costs of $0.073 for successful attempts versus $0.357 for failures. 

While our CTF evaluation (N=104) revealed strong correlations between resource usage and success (enabling earlystopping thresholds at approximately 40 tool calls, $0.30, or 300 seconds), these patterns cannot be validated in our whitebox assessment due to the smaller sample size (N=10). Yet, MAPTA’s real-world validation is impactful with 19 discovered vulnerabilities across ten popular open-source applications, of which _14 classified as high or critical severity_ (including RCE, command injections, secret exposure and arbitrary file write), at an average cost of $3.67 per assessment. All findings are responsibly disclosed to the respective parties and bug bounty programs, where applicable. In total we are awaiting responses from 10 findings that are under CVE review. We expect that larger real-world scans will uncover substantially more vulnerabilities, and recommend deploying MAPTA on a continuous basis for immediate defensive action of web applications. 

13 

## **Ethical Considerations** 

The development and evaluation of MAPTA raises important ethical considerations regarding responsible disclosure of AI-powered security testing capabilities. We address these concerns through several key principles and safeguards implemented throughout our research. 

**Defensive Publication and Community Awareness.** The primary ethical imperative for publishing this research stems from the reality that adversarial actors likely possess similar capabilities or are actively developing them. The democratization of AI development tools and the public availability of security testing methodologies means that malicious applications of these techniques are inevitable. By publishing our findings, we enable the cybersecurity community to understand and prepare for these emerging threats. Defensive security benefits from transparency about offensive capabilities, allowing organizations to implement appropriate countermeasures and security professionals to develop detection and mitigation strategies. 

**Controlled Evaluation Environments.** Our evaluation methodology deliberately avoids testing against live production systems to prevent unintended harm or service disruption. We conducted two distinct types of assessments: (1) blackbox evaluation using purpose-built CTF challenges from the XBOW benchmark, which are explicitly designed for security testing and vulnerability discovery, and (2) whitebox assessments of open-source applications conducted entirely within isolated local environments. The whitebox evaluations involved cloning public repositories and conducting all testing within our own sandboxed virtual machines, ensuring no impact on production deployments or third-party infrastructure. 

**Sandboxed Testing Infrastructure.** We implemented isolation measures to prevent any testing activities from affecting external systems. All MAPTA evaluations execute within dedicated virtual machines with restricted network access, preventing unintended outbound connections or data exfiltration. The sandbox environment includes monitoring and logging mechanisms to ensure all testing activities remain contained within the designated test boundaries. This approach eliminates risks of collateral damage while maintaining the authenticity of real-world vulnerability assessment scenarios. 

**Responsible Vulnerability Disclosure.** For vulnerabilities discovered during our whitebox assessments, we follow responsible disclosure practices by notifying maintainers of affected projects through appropriate channels. The 10 vulnerabilities submitted for CVE assignment were reported to the respective project maintainers with sufficient detail for remediation while avoiding public disclosure of exploitation techniques until patches are available. We provide actionable remediation guidance and collaborate with maintainers to ensure timely resolution of identified security issues. 

**Dual-Use Technology Considerations.** We acknowledge that MAPTA represents dual-use technology with both defen- 

sive and potentially offensive applications. To mitigate misuse risks, our implementation focuses on defensive security applications and includes built-in ethical constraints that prevent destructive operations, data exfiltration, or persistent system modifications. The system is designed to generate proof-ofconcept demonstrations rather than weaponized exploits, providing sufficient evidence for vulnerability validation without enabling direct malicious use. 

**Access Control and Distribution.** While we commit to making MAPTA source code publicly available upon publication to enable scientific reproducibility and defensive research, we implement responsible access controls. The release includes documentation emphasizing ethical use guidelines, configuration options for defensive-only operation modes, and integration with existing responsible security testing frameworks. We encourage adoption by legitimate security professionals, researchers, and organizations while discouraging malicious applications through community governance and ethical use agreements. 

The fundamental ethical principle guiding this research is that the cybersecurity community benefits more from understanding these capabilities than from attempting to suppress them. As AI-powered development accelerates application creation, correspondingly advanced security assessment tools become essential for maintaining adequate security postures. MAPTA represents a defensive response to this challenge, providing organizations with capabilities to match the evolving threat landscape while adhering to responsible research and deployment practices. 

## **Open Science & Availability** 

In accordance with the Open Science Policy, we provide complete access to all research artifacts necessary to evaluate and reproduce the contributions presented in this paper. All artifacts are available at https://github.com/ arthurgervais/mapta. The updated XBOW 104 Challenge Evaluation Framework is available at https://github.com/ arthurgervais/validation-benchmarks. 

## **References** 

- [1] Waleed Alasmary, Feras Khan, Ghada Almashaqbeh, et al. A survey of business logic vulnerabilities in web applications. _Information_ , 16(7):585, 2025. 

- [2] Vaggelis Atlidakis, Roxana Geambasu, Patrice Godefroid, Marina Polishchuk, and Baishakhi Ray. Pythia: Grammar-based fuzzing of rest apis with coverageguided feedback and learning-based mutations. In _ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE)_ , 2020. 

14 

   - [15] N. Kalopisis. Browser-empowered llm agents for web penetration testing. Master’s thesis, University of Twente, 2025. 

- [3] Vaggelis Atlidakis, Patrice Godefroid, and Marina Polishchuk. Restler: Stateful rest api fuzzing. In _International Conference on Software Engineering (ICSE)_ , 2019. 

   - [16] Kaixuan Li, Sen Chen, Lingling Fan, Ruitao Feng, Han Liu, Chengwei Liu, Yang Liu, and Yixiang Chen. Comparison and evaluation on static application security testing (sast) tools for java. In _ESEC/FSE_ , 2023. 

- [4] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. In _Advances in neural information processing systems_ , volume 33, pages 1877–1901, 2020. 

   - [17] OWASP Foundation. Owasp api security top 10: 2023, 2023. 

   - [18] OWASP Foundation. Owasp juice shop, 2025. 

- [5] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. Evaluating large language models trained on code. In _arXiv preprint arXiv:2107.03374_ , 2021. 

   - [19] OWASP Foundation. Owasp webgoat, 2025. 

   - [20] OWASP ZAP Project. Zed attack proxy (zap) documentation, 2025. 

   - [21] Hammond Pearce, Baleegh Ahmad, Benjamin Tan, Brendan Dolan-Gavitt, and Ramesh Karri. Asleep at the keyboard? assessing the security of github copilot’s code contributions. In _2022 IEEE Symposium on Security and Privacy (SP)_ , pages 754–768. IEEE, 2022. 

- [6] Xiaozhu Chen, Yuhang Zhou, Zihan Wang, et al. Large language models for cyber security: A systematic literature review. _arXiv preprint arXiv:2405.04760_ , 2024. 

- [7] Hanzheng Dai, Yuanliang Li, Zhibo Zhang, and Jun Yan. Refpentester: A knowledge-informed self-reflective penetration testing framework based on llms, 2025. 

   - [22] PortSwigger Ltd. Burp suite documentation, 2025. 

   - [23] Positive Technologies. Web application vulnerabilities in 2020–2021. https://global. ptsecurity.com/en/research/analytics/ web-vulnerabilities-2020-2021/, 2021. Accessed: 2025-08-21. 

- [8] Gelei Deng, Ziniu Hu, Yueqi Chen, Haoyu Wang, Bangjie Yin, Yinzhi Cao, Gang Wang, Yan Chen, Xinyu Xing, and Zhiqiang Lin. Pentestgpt: Evaluating and harnessing large language models for automated penetration testing. In _USENIX Security_ , 2024. 

   - [24] Timo Schick, Jane Dwivedi-Yu, Roberto Dessi, Roberta Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola Cancedda, and Thomas Scialom. Toolformer: Language models can teach themselves to use tools, 2023. 

- [9] Ryan Dewhurst. Damn vulnerable web application (dvwa), 2025. 

- [10] Brendan Dolan-Gavitt. Ai agents for offsec with zero false positives, 2025. 

   - [25] XBOW Engineering. Xbow validation benchmarks. https://github.com/xbow-engineering/ validation-benchmarks, 2024. Accessed: 2024-1201. 

- [11] Google Cloud CISO Office. Our big sleep agent makes a big leap. Google Cloud Blog, 2025. 

- [12] Google Project Zero. From naptime to big sleep: Using large language models to find real-world vulnerabilities. Project Zero Blog, 2024. 

   - [26] XBOW Engineering. Gpt-5 performance analysis for autonomous penetration testing. XBOW Blog, 2025. Accessed: 2025-01-26. 

- [13] Junjie Huang and Quanyan Zhu. Penheal: A two-stage llm framework for automated pentesting and optimal remediation. In _Proceedings of the ACM Conference Companion on Computer and Communications Security (ACM CCS Companion), AutonomousCyber ’24: Proceedings of the Workshop on Autonomous Cybersecurity_ , 2024. 

   - [27] John Yang, Carlos E. Jim 

      - ’enez, Ofir Press, and Karthik Narasimhan. Swe-agent: Agent-computer interfaces enable automated software engineering. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. 

   - [28] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. React: Synergizing reasoning and acting in language models, 2022. 

- [14] Imperva. Business logic attacks: Why traditional tools fall short. https://www.imperva.com/blog/ business-logic-attacks-traditional-tools-shortcomings/, 2023. Accessed: 2025-08-21. 

15 

