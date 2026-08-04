# **OSS-CRS: Liberating AIxCC Cyber Reasoning Systems for Real-World Open-Source Security** 

Andrew Chin<sup>_†_</sup> Dongkwan Kim<sup>_†_</sup> Yu-Fu Fu<sup>_†_</sup> Fabian Fleischer<sup>_†_</sup> Youngjoon Kim<sup>_†_</sup> HyungSeok Han<sup>_‡_</sup> Cen Zhang<sup>_†_</sup> Brian Junekyu Lee<sup>_†_</sup> Hanqing Zhao<sup>_†_</sup> Taesoo Kim<sup>_†‡_</sup> _† Georgia Institute of Technology_ , _‡ Microsoft_ 

**_Abstract_ —DARPA’s AI Cyber Challenge (AIxCC) showed that cyber reasoning systems (CRSs) can go beyond vulnerability discovery to autonomously confirm and patch bugs: seven teams built such systems and open-sourced them after the competition. Yet all seven open-sourced CRSs remain largely unusable outside their original teams, each bound to the competition cloud infrastructure that no longer exists. We present OSS-CRS, an open, locally deployable framework for running and combining CRS techniques against real-world open-source projects, with budget-aware resource management. We ported the first-place system (ATLANTIS) and discovered 10 previously unknown bugs (three of high severity) across 8 OSS-Fuzz projects. OSS-CRS is publicly available.** 

## **1. Introduction** 

AI-generated vulnerability reports [4, 18, 36, 47] are increasing the burden on open-source maintainers. The curl project shut down its bug bounty program after AI-written submissions overwhelmed reviewers with unconfirmed findings [45, 46]; FFmpeg maintainers criticized Google for reporting valid bugs without providing patches, calling the reports “CVE slop” [42]. In both cases, AI automation stops at discovery, leaving maintainers to validate findings and write fixes. 

DARPA’s AI Cyber Challenge (AIxCC, 2023–2025) [15] demonstrated that the gap between vulnerability discovery and validated remediation can be closed. Seven finalist teams built autonomous cyber reasoning systems (CRSs) that go beyond discovery: each CRS dynamically confirms a vulnerability with a proof of vulnerability (PoV) and synthesizes a patch validated against that PoV [14]. After the competition, all seven teams open-sourced their systems, in principle making it possible to deploy this capability against any open-source project. 

Yet over half a year later, these CRSs remain largely unusable outside their original teams: each system is bound to team-specific infrastructure and interfaces. This adoption gap blocks the communities that should benefit from these systems: researchers cannot run comparable cross-CRS experiments under consistent settings; CRS developers lack a stable integration contract; and security practitioners cannot adopt deployable, budget-aware workflows that produce actionable findings. 

To understand what prevents adoption, we analyzed the open-sourced codebases of all seven AIxCC finalists and identify three deployment barriers: 1 _Infrastructure duplication_ , each team independently rebuilt the same platform services; 2 _Cloud lock-in_ , every system targets the competition’s Azure and Kubernetes environment, which was decommissioned after the finals; and 3 _Monolithic design_ , analysis techniques are embedded in monolithic systems, preventing researchers from comparing or combining them across teams. Even ATLANTIS, the first-place system [24], requires over 20 Azure virtual machines and cannot target new projects without its original cloud environment. 

To address these barriers, we present OSS-CRS [37], an open framework for developing, running, and composing CRSs on real-world open-source projects. OSS-CRS provides a shared infrastructure layer including LLM budget management and cross-CRS artifact exchange, so that CRS developers can focus on analysis logic rather than platform engineering. It adopts the OSS-Fuzz [3] project format as its target interface, enabling any integrated CRS to target over 1,000 OSS-Fuzz projects without per-project customization. To validate the framework, we ported ATLANTIS and ran it against 8 OSS-Fuzz projects, discovering 10 previously unknown bugs, including three of high severity. OSS-CRS and all integrated CRSs are publicly available. 

This paper makes the following contributions: 

- An _empirical analysis_ of all seven AIxCC finalist CRS codebases, identifying three deployment barriers that prevent practical reuse: infrastructure duplication, cloud lock-in, and monolithic design (§2). 

- OSS-CRS, an open-source framework that addresses these barriers through a unified execution model and standard interface, budget-aware resource management across CPU, memory, and LLM usage, and support for combining CRS techniques across systems (§3). 

- _Real-world validation_ : porting ATLANTIS to OSS-CRS and discovering 10 previously unknown bugs (three of high severity) across 8 OSS-Fuzz projects, showing that competition-grade CRS techniques can be deployed without cloud infrastructure (§4, §5). 

## **2. Background and Motivation** 

### **2.1. Cyber Reasoning Systems** 

A _cyber reasoning system_ (CRS) is an autonomous agent that discovers and repairs software vulnerabilities without human intervention. The concept originated in DARPA’s Cyber Grand Challenge (CGC, 2014–2016) [13, 48], in which teams built systems to attack and defend custom binaries. AIxCC [15] extended the concept to real-world open-source software in C and Java, using challenge targets drawn from OSS-Fuzz projects [3]. 

**CRS capabilities.** Traditional security tools typically focus on a single stage of vulnerability management: fuzzers discover crashes, static analyzers flag potential flaws, and program repair systems synthesize patches, but integrated pipelines from discovery through a validated fix remain uncommon. 

A CRS unifies these stages. _Bug finding_ generates a proof of vulnerability (PoV), an input that triggers abnormal execution such as a crash or sanitizer violation. _Bug fixing_ synthesizes a patch and validates it by rebuilding the target and rerunning tests, confirming that the PoV no longer triggers while preserving the program’s original functionality. A CRS can accept a variety of inputs: an entire source tree, a commit-level code diff, a SARIF report [35] from a static analyzer, or a fuzzing seed corpus. 

**Practical scenarios.** This end-to-end capability supports several deployment settings. In CI/CD, a pipeline submits a pull-request diff and receives a PoV or confirmation of no bugs through a stable, machine-readable interface. For security practitioners, the system turns static-analysis findings into validated patches while enforcing spending limits. For research, multiple CRSs run on the same source tree with matched inputs, so results are reproducible and directly comparable. 

**Infrastructure requirements.** These scenarios create concrete system requirements. A CRS must coordinate multiple tools across stages, pass artifacts such as crash inputs, PoVs, candidate patches, and build outputs between them, and recover when a stage fails. LLM calls span bug finding, triage, and patch generation, thus token use must be budgeted and capped like CPU time and memory. AIxCC allocated $50,000 in LLM credits per team; without budget controls, a single CRS run can exceed $1,000 per hour [5]. Orchestration, artifact exchange, and budget-aware execution are therefore core design problems, not implementation details. 

**OSS-Fuzz.** The AIxCC competition drew its targets from Google’s OSS-Fuzz [3], which provides reproducible, containerized builds for over 1,000 open-source projects. Each project defines a Dockerfile and build script that compile the target project with sanitizer instrumentation, and supplies fuzz targets that consume fuzzer-generated inputs. For CRS deployment, this offers a standardized way to build and test many projects without per-project setup. However, OSS-Fuzz runs one fuzzer per container and 

**TABLE 1:** Deployment characteristics of the AIxCC finalist CRSs. “Local”: can run end-to-end on a single machine against a new target without cloud provisioning. “Composable”: analysis components can be extracted and recombined across systems. 

|**CRS**|**Comp.**|**Infra**|**Middleware**|**Local**|**Composable**|
|---|---|---|---|---|---|
|ATLANTIS [24]|9+|TF+K8s|Ka/PG+R<sup>_∗_</sup>|_×_|_×_|
|BUTTERCUP [9]|14+|TF+Helm|R/M|_◦_|_×_|
|ROBODUCK [5]|1|TF+VMs|–/S<sup>_∗_</sup>|_◦_|_×_|
|FUZZINGBRAIN [44]|4|TF+K8s|–/–<sup>_∗_</sup>|_◦_|_×_|
|ARTIPHISHELL [7]|53|TF+Helm|RMQ/PG+N<sup>_∗_</sup>|_△_|_×_|
|BUGBUSTER [8]|16|TF+Helm|RMQ/PG+R<sup>_∗_</sup>|_×_|_×_|
|LACROSSE [28]|3+|TF+VMs|RMQ/–|_×_|_×_|



TF = Terraform, K8s = Kubernetes, Ka = Kafka, RMQ = RabbitMQ. R = Redis, PG = PostgreSQL, M = MongoDB, S = SQLite, N = Neo4j. _∗_ Uses LiteLLM [6] for LLM proxy and routing. _◦_ Post-competition standalone version available. _△_ Post-competition local deployment guide available. 

does not provide multi-component orchestration, cross-stage artifact exchange, or budget management. 

### **2.2. From Competition to Deployment** 

To assess whether AIxCC CRSs can be deployed outside the competition, we analyzed the open-sourced repositories and deployment artifacts of all seven finalists [5, 7– 9, 24, 28, 44]. We find three recurring barriers: _infrastructure duplication_ , _cloud lock-in_ , and _monolithic design_ . These findings align with Zhang _et al_ . [54], who systematize the techniques of all seven AIxCC finalists and conclude that “the real bottleneck is not technique capability but robust integration into autonomous systems.” The next sections show where deployment breaks down in practice. 

### **2.3. Barrier 1: Infrastructure Duplication** 

Table 1 summarizes the deployment characteristics of each team, where _Comp._ denotes the number of independently built container images. The _Infra_ and _Middleware_ columns show that teams selected different tools yet converged on similar platform roles: container orchestration via Terraform with Kubernetes[26] or Helm[22], and coordination backends such as Kafka[2], RabbitMQ[40], Redis[41], and PostgreSQL[38]. Five of seven teams deployed LiteLLM [6] as their LLM gateway. 

The repositories reveal further overlap not visible in the table: each team independently built LLM budget tracking, cost enforcement, and model routing logic on top of its proxy, as well as test environments for applying patches, rebuilding targets, and validating PoVs. As noted in §2.1, LLM budget control is a shared requirement, yet each team built this logic independently. The barrier is not tool diversity itself, but the repeated integration effort: overlapping infrastructure roles reimplemented across all seven teams. This duplication extends beyond initial development: as LLM provider APIs and cloud platforms evolve, each team must independently update its proxy integration, cost-tracking logic, and deployment scripts. 

2 


![](docs/paper-research/md-downloaded-paper-professor/images/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf-0003-00.png)


<!-- Start of picture text -->
Bug
 Code<br>Cand. DIff<br>Optional<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf-0003-01.png)


<!-- Start of picture text -->
Target<br>Project<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf-0003-02.png)



![](docs/paper-research/md-downloaded-paper-professor/images/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf-0003-03.png)



![](docs/paper-research/md-downloaded-paper-professor/images/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf-0003-04.png)


<!-- Start of picture text -->
LLM Service<br>(§3.5)<br>LiteLLM<br>Budget mgmt<br>Per-CRS keys<br>Model routing<br>Model aliasing<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf-0003-05.png)


<!-- Start of picture text -->
CRS A<br>CPUPUU<br>Container 1ontainer 11 Container 2ontainer 22<br>Memoryemoryy<br>LLM<br>Budget Fuzzeruzzerzzerer Analyzeryzerer<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf-0003-06.png)


<!-- Start of picture text -->
CPUPUU<br>Container 1ontainer 11 Container 2ontainer 22<br>Memoryemoryy<br>LLM<br>Budget Fuzzeruzzerzzerer Analyzeryzerer<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf-0003-07.png)


<!-- Start of picture text -->
CRS B<br>CPUPUU<br>Container 1ontainer 11 Container 2ontainer 22<br>Memoryemoryy<br>LLM<br>Budget Fuzzeruzzerzzerer Builder Sidecar<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf-0003-08.png)


<!-- Start of picture text -->
CPUPUU<br>Container 1ontainer 11 Container 2ontainer 22<br>Memoryemoryy<br>LLM<br>Budget Fuzzeruzzerzzerer Builder Sidecar<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf-0003-09.png)



![](docs/paper-research/md-downloaded-paper-professor/images/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf-0003-10.png)


<!-- Start of picture text -->
File-based Storage<br>Build<br>Artifacts<br>Seeds<br>Bug-candidates<br>PoVs<br>Patches<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf-0003-11.png)



![](docs/paper-research/md-downloaded-paper-professor/images/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf-0003-12.png)



![](docs/paper-research/md-downloaded-paper-professor/images/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf-0003-13.png)


<!-- Start of picture text -->
Exchange Sidecar<br>(§3.6)<br>Artifact<br>deduplication<br><!-- End of picture text -->

**Figure 1:** Architecture overview of OSS-CRS. Users provide a target project and configuration (optionally with code diffs or bug candidates) and receive PoVs and patches as outputs through the three-phase interface ( _prepare_ , _build-target_ , _run_ ). CRSs run in resource-managed containers with isolated networks and interact with the platform through `libCRS` . All LLM calls are routed through the LiteLLM proxy, which handles model routing and per-CRS budget enforcement. The exchange sidecar deduplicates artifacts in file-based storage and synchronizes them across all CRSs. 

### **2.4. Barrier 2: Cloud Lock-in** 

The AIxCC competition provisioned each team with dedicated Azure virtual machines orchestrated by Kubernetes. That environment has since been shut down, and the released artifacts still target infrastructure that no longer exists. For example, ATLANTIS, the first-place system [24], requires 20+ Azure VMs, 42 TiB of cloud storage, and runtime Azure SDK calls to scale Kubernetes node pools, despite open-sourcing its full codebase. 

As the _Local_ column of Table 1 shows, only half the teams added local execution support through standalone releases or local deployment guides [5, 7, 9, 44]. These efforts show that cloud decoupling is possible. However, a local environment must still provide the resource controls and isolation that cloud platforms supply: CPU and memory quotas, network separation between CRSs, and LLM budget limits. Without these, multiple CRSs cannot run on a single machine without contention or cost overruns. 

### **2.5. Barrier 3: Monolithic Design** 

Beyond infrastructure and deployment, a structural obstacle remains: every CRS is a monolith with no modular internal interfaces. The seven finalist teams developed 

distinctive, often complementary techniques: LLM-based input mutation and hybrid fuzzing [24], LLM-first PoV generation [5], grammar-based fuzzing with LLM-generated grammars [7], expertise-driven multi-agent patching [9], diverse LLM strategy ensembles [44], traditional analysis with LLM-augmented patching [8], and multi-LLM workflow coordination [28]. Comparing and combining these techniques would reveal which approaches outperform others and whether ensembling improves overall results. 

Yet as the _Composable_ column of Table 1 confirms, no CRS exposes interfaces for component-level extraction. If ATLANTIS has a stronger fuzzer and BUTTERCUP has a stronger patcher, a researcher cannot combine them without reimplementing one inside the other. The AIxCC competition evaluated end-to-end system outputs but provided no way to attribute results to individual techniques; even Zhang _et al_ .’s survey [54] could describe each team’s methods but not compare them experimentally. As long as CRSs remain monolithic, techniques cannot be isolated, evaluated, or transferred beyond their original systems. A composable framework would let researchers mix the strongest components from different teams, run controlled ablation studies, and build on each other’s advances rather than rebuilding entire systems from scratch. 

3 

## **3. System Design** 

To address the barriers identified in §2, we propose OSSCRS, a locally deployable infrastructure for running and combining existing CRS techniques. OSS-CRS is not itself a CRS; it is the platform on which CRSs are developed, deployed, and composed. It provides three capabilities: 1) a unified three-phase execution model and standard interface ( `libCRS` ) that remove per-team infrastructure duplication; 2) local execution with resource controls and isolation across CPU, memory, network, and LLM budgets, removing cloud dependencies; and 3) cross-CRS artifact exchange that enables combining techniques from independently developed CRSs without requiring a single monolithic pipeline. The following subsections detail how OSS-CRS realizes these capabilities. 

### **3.1. Architecture Overview** 

Figure 1 illustrates the architecture of OSS-CRS. The OSS-CRS user interface defines a three-phase lifecycle ( _prepare_ , _build-target_ , _run_ ) that is driven by a single configuration file that deploys CRSs against target projects. CRSs run in isolated Docker containers with dedicated CPU, memory, and LLM budget allocations; separate networks prevent direct inter-CRS communication. Shared infrastructure provides common services: the _LiteLLM proxy_ handles model routing and budget enforcement, _file-based storage_ persists artifacts (seeds, PoVs, patches, bug-candidates), and the _exchange sidecar_ manages artifact flow between CRSs. CRSs interact with the platform through `libCRS` , which provides APIs for downloading targets, submitting findings, and validating patches. 

### **3.2. OSS-CRS Interface** 

From the user’s perspective, OSS-CRS only requires two inputs: a target project with source code and a single configuration file that specifies which CRSs to deploy along with their resource allocations. Optionally, users can also provide code diffs or bug candidates for targeted bug-finding in environments such as CI/CD pipelines. The user then sequentially runs three commands that set up CRSs, compile the target, and launch the analysis campaign. The main output artifacts are discovered bugs as PoVs and patches that fix them. 

**Three-phase lifecycle.** OSS-Fuzz combines building and running into a single workflow: build the fuzz target, then run it. OSS-CRS introduces a three-phase model ( _prepare_ , _build-target_ , _run_ ) that separates CRS setup from target compilation and running, enabling caching and modularity across diverse CRS architectures. The _prepare_ phase builds CRS container images and their dependencies. These images contain the CRS’s analysis tools but have no knowledge of the target project. A prepared CRS can analyze any compatible target without rebuilding, amortizing setup cost across multiple analysis campaigns. The _build-target_ phase 


![](docs/paper-research/md-downloaded-paper-professor/images/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf-0004-07.png)


<!-- Start of picture text -->
Prepare                        Build Target                          Ru<br>CRS Dependencie CRS Runne<br>Target Project<br>Docker Build
 (OSS-Fuzz<br>(images<br>CRS Builder<br>Docker Run  Instrumentatio CRS Runtim<br>(containers<br>Build Artifact<br>Inputs &<br>Artifacts (files Target Sourc Seeds,
 PoVs,
Patches,<br>PoVs,
 Seed<br>Report<br><!-- End of picture text -->

**Figure 2:** Docker workflow across the three operational phases, showing image construction (top), container execution (middle), and file artifact flow (bottom). 

constructs images for target compilation and compiles the target project. Separating this phase from _prepare_ allows CRSs to construct target-dependent containers while keeping targetindependent components cached. The _run_ phase launches all CRS containers and executes the analysis campaign. CRSs operate concurrently, exchanging artifacts through a shared directory and submitting and syncing findings via the `libCRS` interface. Users can specify a timeout or manually terminate the campaign. 

Figure 2 summarizes the Docker workflow across three layers. The top layer shows Docker images: _prepare_ builds CRS dependency images, _build-target_ adds the target project and CRS builder images, and _run_ produces the final CRS runner images. The middle layer shows containers: _buildtarget_ runs instrumentation containers that compile the target, and _run_ launches CRS runtime containers. The bottom layer tracks file artifacts: target source feeds into build artifacts and seed corpora during _build-target_ , and the _run_ phase produces PoVs, patches, and new seeds. 

**Single configuration.** Users only need to define a single configuration file ( `crs-compose.yaml` ; see Listings 4–7) that specifies CRSs, resource allocations, runtime environment, and LLM settings for all three phases. Adding or removing CRSs requires editing this one file, not coordinating multiple configurations. Users can also specify resource constraints without understanding CRS internals. The same file reproduces orchestration and resource settings across different machines. 

**Targeted analysis.** By default, CRSs analyze the entire target codebase. For focused analysis (checking whether a recent commit introduces vulnerabilities or fixing a specific reported bug), users can provide targeting metadata that constrains the analysis scope. OSS-CRS accepts targeted inputs through standard channels. A code diff specifies changed code regions, enabling delta analysis between versions; directed fuzzers can focus on changed functions, and patch generators can scope fixes to the modified code. Bug-candidate reports 

4 

**TABLE 2:** Representative `libCRS` commands used by CRS developers. 

|**Category**|**Command**|**Purpose**|
|---|---|---|
|Build outputs|`submit-build-output`|Publish build artifacts|
|Runtime setup|`register-shared-dir`|Share fles within CRS|
|Artifact exchange|`register-submit-dir`|Register for background submission|
|Artifact exchange|`register-fetch-dir`|Register for background fetching|
|Artifact exchange|`submit`|Submit artifact (PoV, seed, patch)|
|Artifact exchange|`fetch`|One-shot fetch of artifacts|
|Patch validation|`apply-patch-build`|Apply patch and rebuild|
|Patch validation|`run-pov`|Run PoV against patched build|
|Patch validation|`run-test`|Run regression tests|



identify specific issues for CRSs to address; OSS-CRS accepts SARIF reports [35] to align with the standard format of existing static analysis tools. Targeted analysis supports CI/CD integration, where CRSs check pull requests rather than the entire codebase. 

### **3.3.** `libCRS` 

> `libCRS` is a Python library automatically injected into every CRS container, providing the interface between a CRS’s analysis logic and the OSS-CRS infrastructure. A CRS uses the same `libCRS` interface regardless of deployment environment; only the OSS-CRS infrastructure layer changes, not the CRS itself. Table 2 lists the core commands across four categories: _build outputs_ ; _runtime setup_ ; _artifact exchange_ ; and _patch validation_ . 

**Build outputs.** The _build-target_ and _run_ phases execute in isolated containers, so build artifacts must be handed off across the phase boundary. Build outputs such as instrumented binaries, source snapshots, and coverage metadata, are published via `submit-build-output` during compilation and retrieved at run time. 

**Runtime setup.** A CRS may comprise multiple containers: a fuzzer generating inputs, an analyzer triaging crashes, a patcher synthesizing fixes. The `register-shared-dir` command provides intra-CRS file sharing for corpora, coverage data, and intermediate results, without passing through the inter-CRS exchange. 

**Artifact exchange.** CRSs receive external data via `register-fetch-dir` and `fetch` : initial inputs supplied by the operator (seed corpora, reference diffs, bug-candidate reports) and artifacts submitted by other CRSs during ensemble execution. Conversely, CRSs upload their findings (PoVs, seeds, patches) via `register-submit-dir` and `submit` , which flow to other CRSs’ fetch directories via the exchange sidecar. 

**Patch validation.** Bug-fixing CRSs require a tight editcompile-test loop to iterate on patch candidates. `libCRS` provides `apply-patch-build` , `run-pov` , and `run-test` for incremental project rebuilding and testing through the builder sidecar. 

Figure 3 shows the builder sidecar workflow. During the _build-target_ phase, OSS-CRS captures a Docker image snapshot of the fully compiled target along with its build 


![](docs/paper-research/md-downloaded-paper-professor/images/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf-0005-10.png)


<!-- Start of picture text -->
Instrumentatio<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf-0005-11.png)


<!-- Start of picture text -->
Project Build<br>Snapsho<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf-0005-12.png)


<!-- Start of picture text -->
CRS Runne<br>Builder<br>Patc Sideca<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf-0005-13.png)


<!-- Start of picture text -->
Builder<br>Patc Sideca<br>Build<br>Artifact<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/19-oss-crs-liberating-aixcc-cyber-reasoning-systems-for.pdf-0005-14.png)


<!-- Start of picture text -->
Builder<br>Patc Sideca<br>CRS Runtim Build<br>Artifact<br><!-- End of picture text -->

**Figure 3:** Builder sidecar workflow. The sidecar restores a snapshot of the compiled target, applies the patch diff, and performs an incremental rebuild. 

artifacts. In the _run_ phase, CRS runtime containers receive the build artifacts and begin analysis. When a CRS generates a candidate patch, it invokes `apply-patch-build` , which sends the diff to the builder sidecar; the sidecar restores the snapshot, applies the patch, and performs an incremental recompilation. The CRS then calls `run-pov` to re-execute the crash-triggering input against the patched binary, and `run-test` to run the project’s regression tests. Unlike shared infrastructure services, the builder sidecar runs within the CRS’s resource allocation ( `cpuset` and `memory_limit` ), ensuring that rebuild costs are accounted to the CRS, not the platform. 

### **3.4. Resource Management** 

Running multiple CRSs simultaneously demands coordinated allocation of heterogeneous resources: CPU cores for fuzzing and analysis, memory for program instrumentation, and LLM API budgets for AI-powered reasoning. 

**Compute and memory isolation.** Each CRS declares a `cpuset` string specifying its assigned CPU cores and a `memory` limit enforced via Docker cgroups ( `cpuset` , `mem_limit` ). Pinning CPUs prevents CRSs from contending for the same cores, while hard memory caps prevent a single CRS from destabilizing others. 

**LLM budget as a first-class resource.** Beyond compute resources, OSS-CRS manages LLM API costs as a firstclass resource. Each CRS may declare an `llm_budget` in US dollars; the LLM proxy tracks usage against this limit and rejects requests that would exceed it. This prevents cost overruns during long-running campaigns and enables fair comparison between CRSs with different cost profiles: a CRS that achieves the same results within a $50 budget is more efficient than one requiring $500. 

5 

**Network isolation.** A shared network introduces potential resource-management issues such as port conflicts between CRS containers and uncontrolled bandwidth consumption that could interfere with per-CRS resource guarantees. OSSCRS mitigates this by creating separate Docker networks per CRS and restricting all inter-CRS data exchange to the filesystem-based artifact mechanism. This also simplifies access control for shared services like the LLM proxy and ensures fair comparison when benchmarking multiple CRSs side by side. 

**Flat Docker architecture.** One approach to porting existing CRSs is to wrap them in Docker-in-Docker (DinD), running the entire system inside a single outer container. However, DinD complicates build performance, resource control, and debugging: Docker layer caches are harder to preserve across builds, host-level cgroup enforcement for individual inner containers is less direct, and debugging nested containers is substantially harder. OSS-CRS instead provides interfaces that let CRS developers build for a flat Docker architecture, where all containers are managed by the host Docker daemon. This enables straightforward per-container resource enforcement, preserves Docker layer caches, and simplifies debugging. 

### **3.5. LLM Services** 

CRSs rely on LLMs for code understanding, patch generation, and vulnerability reasoning. However, different CRSs may prefer different providers and models. OSS-CRS handles these differences with an LLM proxy layer based on LiteLLM [6], an open-source proxy that natively supports multiple provider APIs and model aliasing. 

**Unified endpoint.** All CRSs make standard OpenAIcompatible API calls to a single proxy that routes requests to the appropriate backend such as OpenAI, Anthropic, Google, or self-hosted inference servers. A CRS only needs to implement one API client, regardless of which provider the user ultimately configures. 

**Model aliasing.** CRSs reference models by logical names ( _e_ . _g_ ., `claude-sonnet` or `gpt-4o` ) rather than provider-specific identifiers. The proxy maps these aliases to concrete provider endpoints, so swapping providers requires only a configuration change, not CRS code modifications. Operators define model mappings in a YAML configuration file (see Listings 8 and 9). Each entry specifies a logical `model_name` (what CRSs request) and provider-specific parameters including the actual model identifier, API credentials, and optional custom endpoints for self-hosted or Azure deployments. At validation time, OSS-CRS checks that each CRS’s `required_llms` are available in the operator’s configured model list. 

**Per-CRS budget enforcement.** OSS-CRS generates a unique API key per CRS at campaign startup, each associated with its budget. The proxy tracks cumulative costs and rejects requests when the budget is exhausted. This per-CRS keying also enables fine-grained usage tracking such as which CRS made each request, what model was used, and how many tokens were consumed. When a CRS 

exhausts its budget, subsequent requests are rejected. The LiteLLM proxy is deployed as a service in the OSS-CRS infrastructure, and its lifetime is coupled with the run phase. 

**Deployment modes.** OSS-CRS supports three deployment modes. In _internal mode_ , OSS-CRS manages LiteLLM, and a key-generation sidecar; this is the default for standalone deployments. In _external mode_ , operators provide an existing LLM proxy endpoint and key, useful when an organization already runs centralized LLM infrastructure; per-CRS budget enforcement depends on the external proxy’s capabilities. In _disabled mode_ , OSS-CRS performs no LLM setup, for CRSs that do not use LLMs. 

### **3.6. Artifact Exchange** 

Running multiple CRSs simultaneously enables complementary workflows; a fuzzer can discover crashes while a separate patcher generates fixes. Our evaluation demonstrates that cross-CRS artifact flow works in practice (§4); quantifying performance gains over single-CRS runs remains future work. OSS-CRS enables this _ensemble execution_ (see Listing 7) through a filesystem-based exchange mechanism that requires no direct communication between CRSs. 

**Exchange model.** All inter-CRS coordination flows through a shared _exchange directory_ . Each CRS writes artifacts to its private submit directory, and reads from a shared fetch directory that mirrors the exchange. The exchange sidecar synchronizes per-CRS submit directories into a shared exchange exposed through each CRS’s fetch directory. The exchange organizes artifacts by type: `seeds` for fuzzing inputs, `povs` for crash-triggering inputs, `patches` for proposed fixes, and `bug-candidates` for triage reports. CRS-internal data (e.g. coverage maps, model weights, intermediate analysis state) remains private to each CRS and is not shared through the exchange. Artifacts are stored under content-hash filenames, ensuring that duplicate discoveries from multiple fuzzers appear exactly once. This hash-based deduplication is the baseline strategy. Because the exchange sidecar is a shared OSS-CRS service rather than library code launched in a CRS container, we can extend it with more advanced logic without modifying individual CRSs: coveragebased deduplication that keeps only seeds increasing overall coverage, or stack-trace-based deduplication that groups PoVs by crash signature to reduce redundant triage. 

**Coordination without direct communication.** CRSs coordinate implicitly through the artifacts they exchange, without direct messaging or task assignment. Each CRS polls for new artifacts at its own pace and decides independently what work to perform. This design provides fault isolation. If one CRS crashes, others continue operating on previously shared artifacts. Resource exhaustion in one CRS does not cascade to others, since each runs in an isolated container with independent resource allocations. This file sharingbased model also simplifies deployment: operators can add or remove CRSs across campaigns without reconfiguring communication channels within CRSs. 

6 

**TABLE 3:** CRSs integrated into OSS-CRS. 

|**CRS**|**Type**|**Languages**|**LLM**|
|---|---|---|---|
|CRS-LIBFUZZER|Bug-fnding|C/C++|None|
|ATLANTIS-C|Bug-fnding|C/C++|✓|
|ATLANTIS-JAVA|Bug-fnding|Java|✓|
|ATLANTIS-MULTILANG|Bug-fnding|C/C++/Java|✓|
|CLAUDECODE|Bug-fxing|C/C++/Java|✓|



**TABLE 4:** Environment variables injected into CRS containers. 

|**Variable**|**Purpose**|
|---|---|
|`OSS_CRS_TARGET`|Target project name|
|`OSS_CRS_TARGET_HARNESS`|Harness binary name|
|`OSS_CRS_NAME`|CRS name (for service discovery)|
|`OSS_CRS_CPUSET`|Allocated CPU cores (_e_._g_., `4-7`)|
|`OSS_CRS_MEMORY_LIMIT`|Memory limit (_e_._g_., `16G`)|
|`OSS_CRS_LLM_API_URL`|LLM proxy endpoint|
|`OSS_CRS_LLM_API_KEY`|Per-CRS API key for budget enforcement|



## **4. CRS Integration** 

The goal of OSS-CRS is to provide a modular framework where researchers can study, compare, and compose the distinctive techniques each team developed. As a first phase of validation, we integrated five CRSs that span the spectrum from traditional fuzzing to LLM-powered multi-language analysis (Table 3). The framework is open to the community to port additional systems. Our primary validation focuses on ATLANTIS for two reasons: 1 it is the best-performing AIxCC finalist, and 2 it provides no support for local execution outside the competition’s cloud infrastructure. The remaining CRSs validate interface usability and ensemble mechanics. 

### **4.1. Integration Requirements** 

CRS developers integrate their system into OSS-CRS through a `crs.yaml` manifest with three phase-aligned sections. 

> `prepare_phase` builds the CRS’s own container images ( _e_ . _g_ ., fuzzers, analyzers, LLM agents) that are target-independent and reusable across projects. 

`target_build_phase` declares build steps that require knowledge of the target: custom instrumentation passes, sanitizerspecific compilations, or snapshot captures for incremental patch validation. In the AIxCC competition, all seven teams independently implemented their own build and patchcompilation pipelines: ATLANTIS built a `cp_manager` with Docker-in-Docker, BUTTERCUP used a dedicated `build-bot` service, and ARTIPHISHELL deployed separate `patchery` and `patch-validation-testing` components [7, 9, 24]. With OSS-CRS, CRS developers extract these custom build passes into `target_build_phase` declarations. 

`crs_run_phase` defines the runtime modules as a set of named containers, each with its own Dockerfile. A multicomponent CRS ( _e_ . _g_ ., a fuzzer, an analyzer, and a builder sidecar) declares one entry per component, and OSS-CRS launches them together with shared networking and resource limits. 

OSS-CRS also injects environment variables into every CRS container at runtime (Table 4). These expose the target name, resource allocation, and LLM proxy credentials, so CRSs can adapt without hard-coded assumptions. For instance, a fuzzer can spawn one worker per core. 

1 _`#!/bin/bash`_ 2 `set -e` 3 `compile` 4 `libCRS submit-build-output $OUT build` 

**Figure 4:** Build script for CRS-LIBFUZZER. 

### **4.2. Baseline: CRS-LIBFUZZER** 

The simplest integrated CRS is a thin wrapper around libFuzzer [39], the coverage-guided fuzzer used by OSS-Fuzz. It serves as a baseline: it requires no LLM, uses a single container, and exercises the minimal OSS-CRS interface, _i_ . _e_ ., prepare, build-target, and run, with nothing beyond standard fuzzing. Its build script (Figure 4) is two lines: `compile` the target, then hand over artifacts to the run phase. This two-line pattern is the minimal build contract; CRSs can extend it freely by adding custom compiler passes, instrumenting with different sanitizers, or running static analyzers, while OSS-CRS handles container orchestration and artifact transfer. The complete `crs.yaml` and `crs-compose.yaml` for CRS-LIBFUZZER appear in Listing 1 and Listing 4. 

### **4.3. Porting ATLANTIS** 

ATLANTIS, the first-place AIxCC system [24], is among the most complex CRSs: it comprises multiple sub-systems (three independent bug-finding systems), uses multiple instrumentation passes (coverage, AddressSanitizer [43], and uninstrumented builds), and combines diverse fuzzing engines with multiple LLM agents. 

**Porting process.** Converting ATLANTIS to the OSS-CRS interface required four categories of changes. 1 _Manifest creation._ We wrote `crs.yaml` manifests for each subsystem, declaring its supported languages, required LLM models, capabilities, and prepare/build/run phase definitions. 2 _Artifact submission._ Competition-specific API usage ( _e_ . _g_ ., sending PoVs) was replaced with `libCRS` commands ( `register-submit-dir` , `submit` ). 3 _Project building._ Each ATLANTIS sub-system had its own way of adding CRS tooling to the target project image: ATLANTIS-MULTILANG rebuilt the project image with a custom base image and ATLANTIS-C mounted tooling into the project container and overwrote the compiler environment variable. Under OSSCRS, all sub-systems follow the same standard: providing a `builder.Dockerfile` that receives the target project base image as a build argument, unifying the build workflow. 

7 

4 _Image caching via prepare phase._ In the competition environment, CRS images are prebuilt into registries. However, for rapid local CRS development, OSS-CRS supports rebuilding CRS images through its infrastructure. As such, each ATLANTIS sub-system needed to optimize its build process by partitioning some images into the prepare phase. 

**Three sub-systems ported.** We ported three of ATLANTIS’s bug-finding sub-systems as independent CRSs. ATLANTIS-MULTILANG handles C/C++/Java targets using microservices-based fuzzing driven by directed fuzzing and LLM agents. ATLANTIS-JAVA targets Java projects with Jazzer [23] sinkpoint-based fuzzing, ATLANTIS-C targets C/C++ projects with a custom libAFL [17] fuzzer, and both ATLANTIS-JAVA and ATLANTIS-C use a highthroughput agentic seed generator. Each sub-system has its own `crs.yaml` manifest, its own target build process, and runs in its own containers. The configuration files for ATLANTIS-MULTILANG appear in Listing 2 and Listing 5. **What changed, what was preserved.** The original ATLANTIS requires over 20 Azure VMs across multiple Kubernetes node pools, three separate LiteLLM proxy instances, and dynamic node scaling via Azure SDK calls (§2.4). Porting replaced all Kubernetes orchestration with a flat Docker architecture, collapsed the three LiteLLM proxies into the single OSS-CRS proxy, and substituted the competition scoring API with `libCRS` ’s artifact submission. Each sub-system also shed auxiliary components: ATLANTIS-MULTILANG and ATLANTIS-JAVA dropped their concolic execution engines, and ATLANTIS-C dropped its backup fuzzing engines and harness scheduler. All primary bug-finding logic, including fuzzers, LLM agents, and analysis pipelines, was preserved with minimal modification, confirming that the core analysis techniques are independent of the deployment infrastructure. 

### **4.4. CLAUDECODE: LLM-Based Patch Generation** 

To demonstrate bug-fixing integration, we developed CLAUDECODE, a CRS that uses an LLM agent to analyze crash traces and source code for vulnerabilities discovered by other CRSs in order to generate patches. 

**Builder sidecar in action.** CLAUDECODE validates each candidate through `libCRS` ’s three-step patch validation pipeline: `apply-patch-build` sends the unified diff to a builder sidecar, which applies the patch and performs an incremental rebuild from a pre-captured build snapshot; `run-pov` re-executes the crash-triggering input against the patched binary to confirm the vulnerability is resolved; `run-test` runs the project’s regression tests to check for functional regressions. Because the builder sidecar handles all build-system complexity (such as Makefiles), CLAUDECODE’s implementation contains no build logic. The CRS focuses entirely on LLM-driven patch synthesis, delegating compilation and testing to the framework. 

## **5. Zero-day Results** 

To evaluate whether OSS-CRS enables practical, largescale vulnerability discovery and fixing on real-world soft- 

ware, we ran the ported ATLANTIS CRS against open-source projects. 

**Target selection.** We selected 8 OSS-Fuzz projects spanning C/C++ and Java, chosen to cover a range of project sizes (3 kLoC to 1,960 kLoC), application domains (databases, parsers, network servers, cryptographic libraries), and existing fuzzing maturity (from newly onboarded to heavily fuzzed for years). We did not cherry-pick projects based on expected vulnerability yield. 

**Running setup.** All experiments ran on a single machine with 32 CPU cores and 128 GB RAM, running Ubuntu 22.04 with Docker 27. Each campaign allocated 16 cores and 64 GB RAM to the bug-finding CRS, with a 24-hour timeout per target project. LLM budgets were set to $50 per campaign, using a mix of Claude and GPT-4o through the OSS-CRS LLM proxy. 

### **5.1. Zero-day Bugs Found** 

At the time of writing, three have been fixed by upstream maintainers, one confirmed, and six are pending review. The majority are memory-safety bugs in C, but the set also includes logic bugs and undefined-behavior flaws (CWE-476, CWE-674, CWE-681), demonstrating that the CRS finds nullpointer, schema-validation, and numeric-conversion issues, not only fuzzer-class crashes. 

We will release three cases in detail from two projects, following a 30-day window after the original fix was made available. 

### **5.2. Patches and Disclosure** 

**Patch generation and validation.** For each vulnerability, OSS-CRS feeds the crash trace, root-cause analysis, and surrounding source code to ATLANTIS, which uses an LLM to generate a minimal candidate patch as a unified diff. Each candidate is then validated automatically through the `libCRS` infrastructure (§3.3): the patch is applied and the project rebuilt, the original PoV is re-executed to confirm the crash no longer triggers, and the project’s test suite is run to check for regressions. We then manually reviewed all patches before submitting them to upstream maintainers. 

Three examples will be provided after a 30-day postfix window to illustrate the kinds of patches OSS-CRS produces. 

**Disclosure outcomes.** Of the 10 findings, three have been fixed by upstream maintainers, but have not passed a 30day period since being fixed. There is one confirmed by maintainers but not yet patched. The remaining six are pending initial response. We reported all vulnerabilities following each project’s preferred disclosure process, including GitHub Security Advisories and direct email. 

8 

## **6. Discussion** 

### **6.1. Challenges and Lessons** 

**Docker-in-Docker vs. flat Docker.** Our initial attempt at local portability wrapped each CRS in a Docker-in-Docker (DinD) container. As discussed in §3.4, DinD complicated resource control, build caching, and debugging, so OSSCRS adopted a flat Docker architecture instead. The practical lesson is that the flat model requires explicit network policies to prevent cross-CRS communication, a tradeoff we found acceptable given the gains in resource visibility and build performance. 

**Build-system diversity.** OSS-Fuzz projects use heterogeneous build systems (Make, CMake, Autoconf, Bazel, Meson, and more). During CRS integration, we found that build assumptions baked into the competition environment (preinstalled tool versions, fixed filesystem layouts) frequently broke on different target projects. OSS-CRS mitigates this by building targets through OSS-Fuzz’s official build flows, inheriting the build environment that each project’s maintainers already support. 

**Porting effort.** Adapting ATLANTIS to the OSS-CRS interface required understanding the system’s internal architecture and artifact flow without changing the core logic of the modules we ported. The changes fell into four categories: configuration (writing `crs.yaml` manifests), I/O adaptation (replacing competition-specific API calls with `libCRS` commands), build integration (replacing DinD-based patch compilation with `libCRS` ’s builder sidecar, which handles the apply-patch, rebuild, and test cycle), and image optimizations using the prepare phase. For the ATLANTIS-MULTILANG port, this integration work required approximately 3 persondays. For ATLANTIS-C, the port took over 4 person-days, as its tighter coupling to competition-specific build pipelines and container orchestration demanded more extensive I/O and build-integration changes. For ATLANTIS-JAVA and CLAUDECODE, integration required approximately 1 personday each. Across these ports, we modified configuration, orchestration logic, and artifact I/O boundaries, not the core analysis algorithms. In general, porting effort depends on the gap between a CRS’s original design and the four categories above: systems with hard-coded competition APIs, DinDbased build flows, non-standard configuration formats, or tightly coupled image assumptions require proportionally more adaptation work. 

### **6.2. Limitations and Threats to Validity** 

Our results demonstrate feasibility: CRS logic can be decoupled from competition infrastructure and applied to real OSS targets with actionable outputs. We note several limitations of OSS-CRS in its current state. 

**Single CRS ported.** We validated OSS-CRS by porting one AIxCC system (ATLANTIS). While ATLANTIS, the first-place system [24], is among the most infrastructure-heavy finalists, porting additional CRSs may reveal interface gaps or design 

assumptions that a single system does not exercise. We excluded `concolic` , ATLANTIS’s hybrid fuzzing component, from the current port because its instrumentation introduced compatibility issues across diverse target projects; in the original competition, this module contributed only 1.7% of ATLANTIS’s results [24], so we expect minimal impact on bug-finding capability. We are working on porting other finalist CRSs (§6.3). 

**Target format assumptions.** OSS-CRS currently targets projects compatible with OSS-Fuzz, which require a standardized build script, a containerized environment, language restrictions, and at least one fuzz harness. Projects not yet onboarded to OSS-Fuzz require harness development, which is outside the scope of the framework. 

**Target selection.** Our 8 target projects were selected from OSS-Fuzz’s project corpus based on adoption and security relevance. 

**LLM non-determinism.** LLM-based CRS components produce non-deterministic outputs, affecting both vulnerability discovery and patch generation. Our results reflect specific model versions and prompt configurations; different models or API versions may yield different findings. 

### **6.3. Community and Future Work** 

Our roadmap focuses on three directions: 

- _Cross-CRS technique analysis._ With ensemble execution and cross-CRS artifact exchange in place, we aim to answer two questions: which individual techniques are most effective, and which combinations yield the best results? Seed deduplication and PoV triage are prerequisites for meaningful cross-CRS comparison. 

- _CRS benchmarking._ To enable systematic evaluation, we are developing a benchmark suite that lets security practitioners and researchers evaluate and compare CRSs under controlled conditions, analogous to FuzzBench [34] for fuzzers. 

- _Broader target coverage._ We plan to apply integrated CRSs to a wider range of open-source projects to discover vulnerabilities at scale. 

## **7. Related Work** 

**Autonomous cyber reasoning.** The Cyber Grand Challenge (CGC) [13, 48] introduced autonomous systems that find and patch vulnerabilities in custom binaries on the DECREE OS. AIxCC [15] extended this to real-world open-source software, producing seven finalist CRSs whose techniques are analyzed by Zhang _et al_ . [54]. OSS-CRS differs from both competition platforms: CGC provided a fixed binary format and a scoring API; AIxCC provided Azure infrastructure with competition-specific endpoints. OSS-CRS provides a reusable framework that persists beyond any single competition, targeting OSS-Fuzz’s corpus of open-source projects. **Fuzzing infrastructure.** OSS-Fuzz [3] provides continuous fuzzing for open-source projects but supports only singlecontainer, single-fuzzer execution without bug-fixing or LLM 

9 

integration (§2.1). FuzzBench [34] evaluates fuzzer performance on standardized benchmarks but does not support multi-component CRS workloads. ARVO [32] reproduces historical OSS-Fuzz vulnerabilities for research but provides no execution framework. Magma [21] and UniFuzz [30] offer ground-truth benchmarks for evaluating fuzzers but focus on single-fuzzer comparison, not multi-technique composition. OSS-CRS complements these tools: it uses OSS-Fuzz project definitions as targets and could integrate with FuzzBench for CRS-level comparison. 

**Ensemble and collaborative fuzzing.** Collaborative fuzzing [12, 19, 20, 56] demonstrated that given fixed resources, distributing effort across multiple fuzzers outperforms focusing on any single fuzzer, motivating ensemble approaches. OSS-CRS generalizes this insight from fuzzer ensembles to CRS ensembles that combine heterogeneous techniques, including fuzzing, static analysis, LLM reasoning, and autonomous patching. It coordinates them via unified resource and LLM budget allocation and a filesystembased exchange mechanism that requires no modification to individual CRSs. 

**LLM-powered fuzzing.** LLMs are increasingly used to augment fuzzing. TitanFuzz [16] and Fuzz4All [50] use LLMs to generate test inputs, ChatAFL [33] applies them to protocol fuzzing, and ELFuzz [11] synthesizes entire fuzzers via LLM-driven evolution. HLPFuzz [51] and G<sup>2</sup> FUZZ [55] leverage LLMs for constraint solving and input generator synthesis, respectively. In a complementary direction, OSSFuzz-Gen [31] and SHERPA [27] use LLMs to synthesize fuzz harnesses, automating a key bottleneck in onboarding new targets. These works improve individual fuzzing components; OSS-CRS provides the orchestration layer to compose such LLM-augmented tools into complete CRS pipelines. 

**LLM-based vulnerability repair.** Several benchmarks evaluate LLM agents on security tasks: SEC-bench [29], Cybench [53], AutoPatchBench [10], and CVE-Bench [49]. On the technique side, San2Patch [25] automates vulnerability repair from sanitizer logs via tree-of-thought LLM reasoning, and PatchAgent [52] mimics human debugging expertise for practical program repair. The AIxCC competition demonstrated that integrating LLMs into full CRS pipelines, combining code reasoning with fuzzing and program analysis, yields stronger results than applying them in isolation [54]. OSSCRS provides the infrastructure to study this integration: its LLM proxy tracks per-CRS costs, enabling comparison of LLM-augmented versus traditional techniques under fixed budgets. 

## **8. Conclusion** 

DARPA’s AI Cyber Challenge produced seven autonomous CRSs for finding and fixing vulnerabilities, but left them entangled with competition-specific infrastructure. We analyzed all seven finalist CRSs and identified three categories of barriers (infrastructure duplication, cloud lockin, and monolithic design) that prevent real-world deployment. OSS-CRS addresses these barriers with a standardized 

CRS interface, resource isolation with LLM budget management, and cross-CRS artifact exchange for composing complementary techniques. By porting the AIxCC champion system and discovering 10 previously unknown bugs across 8 open-source projects, we provide feasibility evidence that competition CRS logic can be decoupled from its original infrastructure and applied to real-world OSS projects. OSSCRS is available as open source [37], a first step toward broader cross-CRS accessibility and evaluation. We invite the community, including researchers, CRS developers, and security practitioners, to actively develop, compose, and evaluate CRS techniques and help mature OSS-CRS into shared infrastructure for open-source software security. 

## **Ethical Considerations** 

OSS-CRS lowers the barrier to automated vulnerability discovery and patching in open-source software. This automation carries inherent dual-use risks, as the same techniques that help defenders find and fix bugs could also help attackers identify exploitable weaknesses. However, we believe the benefits outweigh these risks: our system produces not only proofs of vulnerability but also validated patches, shifting the balance toward defense. 

We ran OSS-CRS entirely in isolated Docker containers on local machines without transmitting any data to external services. Also, because OSS-CRS executes all analysis inside containerized environments and operates on fuzzing harnesses originally written for security testing, it poses no risk to running production systems. 

All vulnerabilities discovered in this work were reported to upstream maintainers following each project’s preferred disclosure process, including GitHub Security Advisories, SourceForge, and direct email. We withheld public disclosure of vulnerability details until maintainers acknowledged the reports. The proof-of-vulnerability inputs and patches are shared with maintainers to facilitate timely remediation. We are actively communicating with project maintainers and responsible parties to ensure all reported issues are addressed. 

## **Open Science** 

OSS-CRS, including the framework, all integrated CRSs, and evaluation artifacts, is publicly available at https://github. com/ossf/oss-crs. The repository includes the CRS interface specification, `libCRS` library, configuration templates, and documentation for porting new CRSs. 

## **Acknowledgments** 

We thank Younggi Park for the initial design and implementation of the bug-fixing infrastructure in OSSCRS. We thank Sin Liang Lee, Isaac Hung, Joshua Wang, and Jiho Kim for their contributions to the bug-finding campaign. We also thank Jeff Diecks and the Open Source Security Foundation (OpenSSF) for supporting OSS-CRS as an OpenSSF sandbox project and promoting community outreach. 

10 

## **References** 

- [1] _Proceedings of the 34th USENIX Security Symposium (Security)_ , Seattle, WA, Aug. 2025. 

- [2] Apache Software Foundation. Kafka, 2026. https://github.com/apache/ kafka. 

- [3] A. Arya, O. Chang, J. Metzman, K. Serebryany, and D. Liu. OSSFuzz: continuous fuzzing for open source software, 2016. https: //github.com/google/oss-fuzz. 

- [4] D. Bass. One of the Best Hackers in the Country Is an AI Bot. Bloomberg, 2025. https://www.bloomberg.com/news/articles/2025-0624/one-of-the-best-hackers-in-the-country-is-an-ai-bot. 

- [5] T. Becker, R. Goulden, Y. Kim, J. Kwon, S. Myung, T. Nighswander, and S. Seo. aixcc-afc-archive: Public source code release of theori’s aixcc afc submission, Aug. 2025. URL https://github.com/theoriio/aixcc-afc-archive/. 

- [6] BerriAI. LiteLLM: Call 100+ LLM APIs in OpenAI format, 2026. https://github.com/BerriAI/litellm. 

- [7] A. Bianchi, K. Borgolte, J. Corbetta, F. Disperati, A. Dutcher, J. Grosen, P. Grosen, A. Machiry, C. Salls, Y. Shoshitaishvili, N. Stephens, G. Vigna, and R. Wang. Cyber grand shellphish. _Phrack_ , 16(70), June 2017. URL https://sites.cs.ucsb.edu/~vigna/publications/2017_Phrack_ CyberGrandShellphish.pdf. 

- [8] BugBuster. 42-b3yond-6ug-crs: Bugbuster, our team’s submission to the ai cyber challenge final competition, Aug. 2025. URL https: //github.com/42-b3yond-6ug/42-b3yond-6ug-crs. 

- [9] Buttercup. Buttercup: finds and patches software vulnerabilities, Dec. 2024. URL https://github.com/trailofbits/buttercup. 

- [10] T. Byun, C. Aschermann, K. Y. Thng, W. Zhou, Y. Yang, L. Deason, and J. Saxe. Introducing AutoPatchBench: A Benchmark for AI-Powered Security Fixes, Apr. 2025. URL https://engineering.fb.com/2025/04/29/ai-research/autopatchbenchbenchmark-ai-powered-security-fixes/. 

- [11] C. Chen, B. Dolan-Gavitt, and Z. Lin. ELFuzz: Efficient Input Generation via LLM-driven Synthesis Over Fuzzer Space. In _Proceedings of the 34th USENIX Security Symposium (Security)_ SEC [1]. 

- [12] Y. Chen, Y. Jiang, F. Ma, J. Liang, M. Wang, C. Zhou, X. Jiao, and Z. Su. Enfuzz: Ensemble fuzzing with seed synchronization among diverse fuzzers. In _Proceedings of the 28th USENIX Security Symposium (Security)_ , Santa Clara, CA, Aug. 2019. 

- [13] DARPA. Cyber Grand Challenge, 2016. https://www.darpa.mil/ research/programs/cyber-grand-challenge. 

- [14] DARPA. AIxCC Archive, 2025. https://archive.aicyberchallenge.com/. [15] DARPA. AI Cyber Challenge (AIxCC), 2025. URL https:// aicyberchallenge.com/. Accessed: 2025-09-09. 

- [16] Y. Deng, C. S. Xia, H. Peng, C. Yang, and L. Zhang. Large Language Models Are Zero-Shot Fuzzers: Fuzzing Deep-Learning Libraries via Large Language Models. In _Proceedings of the 32nd ACM SIGSOFT International Symposium on Software Testing and Analysis_ , ISSTA 2023, pages 423–435. Association for Computing Machinery, 2023. doi: 10.1145/3597926.3598067. 

- [17] A. Fioraldi, D. Maier, D. Zhang, and D. Balzarotti. LibAFL: A Framework to Build Modular and Reusable Fuzzers. In _Proceedings of the 29th ACM conference on Computer and communications security (CCS)_ , CCS ’22. ACM, November 2022. 

- [18] L. Franceschi-Bicchierai. Google says its AI-based bug hunter found 20 security vulnerabilities. TechCrunch, 2025. https://techcrunch.com/2025/08/04/google-says-its-ai-based-bughunter-found-20-security-vulnerabilities/. 

- [19] Y.-F. Fu, J. Lee, and T. Kim. autofz: Automated Fuzzer Composition at Runtime. In _Proceedings of the 32nd USENIX Security Symposium (Security)_ , Anaheim, CA, Aug. 2023. 

- [20] E. Güler, P. Görz, E. Geretto, A. Jemmett, S. Österlund, H. Bos, C. Giuffrida, and T. Holz. Cupid : Automatic fuzzer selection for collaborative fuzzing. In _Proceedings of the Annual Computer Security_ 

_Applications Conference (ACSAC)_ , 2020. 

- [21] A. Hazimeh, A. Herrera, and M. Payer. Magma: A Ground-Truth Fuzzing Benchmark. _Proc. ACM Meas. Anal. Comput. Syst._ , 4(3): 49:1–49:29, Nov. 2020. doi: 10.1145/3428334. URL https://dl.acm. org/doi/10.1145/3428334. 

- [22] Helm. Helm: The Kubernetes Package Manager, 2026. https://github. com/helm/helm. 

- [23] C. Intelligence. Jazzer: Coverage-guided, in-process fuzzing for the jvm, 2025. https://github.com/CodeIntelligenceTesting/jazzer. 

- [24] T. Kim, H. Han, S. Park, D. R. Jeong, D. Kim, D. Kim, E. Kim, J. Kim, J. Wang, K. Kim, S. Ji, W. Song, H. Zhao, A. Chin, G. Lee, K. Stevens, M. Alharthi, Y. Zhai, C. Zhang, J. Jang, Y. Jang, A. Askar, D. Kim, F. Fleischer, J. Cho, J. Kim, K. Ko, I. Yun, S. Park, D. Baik, H. Lee, H. Heo, M. Gwon, M. Lee, M. Baek, S. Min, W. Kim, Y. Jin, Y. Park, Y. Choi, J. Jung, G. Lee, J. Jang, K. Kim, Y. Cha, and Y. Kim. ATLANTIS: AI-driven Threat Localization, Analysis, and Triage Intelligence System. _arXiv_ , Sept. 2025. doi: 10.48550/arXiv. 2509.14589. URL https://arxiv.org/abs/2509.14589. Cross-listed in cs.AI. 

- [25] Y. Kim, S. Shin, H. Kim, and J. Yoon. Logs In, Patches Out: Automated Vulnerability Repair via Tree-of-Thought LLM Analysis. In _34th USENIX Security Symposium (USENIX Security 25)_ , pages 4401– 4419, 2025. 

- [26] kubernetes. kubernetes: Production-Grade Container Scheduling and Management, 2026. https://github.com/kubernetes/kubernetes. 

- [27] Kudu Dynamics. SHERPA: Security Harness Engineering for Robust Program Analysis, 2025. URL https://github.com/AIxCyberChallenge/ sherpa.git. Developed as part of DARPA’s AI Cyber Challenge (AIxCC). 

- [28] Lacrosse. afc-crs-lacrosse: Aixcc finals 2025 crs submission, Aug. 2025. URL https://github.com/siftech/afc-crs-lacrosse. 

- [29] H. Lee, Z. Zhang, H. Lu, and L. Zhang. SEC-bench: Automated benchmarking of LLM agents on real-world software security tasks. In _The thirty-ninth annual conference on neural information processing systems_ , 2025. URL https://openreview.net/forum?id=QQhQIqons0. 

- [30] Y. Li, S. Ji, Y. Chen, S. Liang, W.-H. Lee, Y. Chen, C. Lyu, C. Wu, R. Beyah, P. Cheng, et al. UNIFUZZ: A holistic and pragmatic metrics-driven platform for evaluating fuzzers. In _Proceedings of the USENIX Security Symposium (Security)_ , pages 2777–2794. USENIX Association, Aug. 2021. 

- [31] D. Liu, O. Chang, J. Metzman, M. Sablotny, and M. Maruseac. OSSFuzz-Gen: LLM powered fuzzing via OSS-Fuzz, 2024. https://github. com/google/oss-fuzz-gen. 

- [32] X. Mei, P. S. Singaria, J. D. Castillo, H. Xi, Abdelouahab, Benchikh, T. Bao, R. Wang, Y. Shoshitaishvili, A. Doupé, H. Pearce, and B. Dolan-Gavitt. ARVO: Atlas of Reproducible Vulnerabilities for Open Source Software, Aug. 2024. URL http://arxiv.org/abs/2408. 02153. arXiv:2408.02153 [cs]. 

- [33] R. Meng, M. Mirchev, M. Böhme, and A. Roychoudhury. Large Language Model Guided Protocol Fuzzing. In _Proceedings of the 2024 Annual Network and Distributed System Security Symposium (NDSS)_ , San Diego, CA, Feb. 2024. 

- [34] J. Metzman, L. Szekeres, L. Simon, R. Sprabery, and A. Arya. FuzzBench: an open fuzzer benchmarking platform and service. In _Proceedings of the 29th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering_ , ESEC/FSE 2021, pages 1393–1403, New York, NY, USA, Aug. 2021. Association for Computing Machinery. ISBN 978-1-4503-8562-6. doi: 10.1145/3468264.3473932. URL https://dl.acm.org/doi/10.1145/3468264.3473932. 

- [35] OASIS. Static Analysis Results Interchange Format (SARIF) Version 2.1.0, 2023. https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0. html. 

- [36] OpenAI. Introducing Aardvark: OpenAI’s Agentic Security Researcher. OpenAI, 2025. https://openai.com/index/introducing-aardvark/. 

- [37] OSS-CRS, 2026. URL https://github.com/ossf/oss-crs. 

11 

- [38] PostgreSQL. Postgresql, 2026. https://github.com/postgres/postgres. 

- [39] T. L. Project. libfuzzer – a library for coverage-guided fuzz testing. https://llvm.org/docs/LibFuzzer.html, 2025. Accessed: 2025-12-09. 

- [40] RabbitMQ. Rabbitmq-server: core server and tier 1 (built-in) plugins, 2026. https://github.com/rabbitmq/rabbitmq-server. 

- [41] Redis. Redis: preferred, fastest, and most feature-rich cache, data structure server, and document and vector query engine, 2026. https: //github.com/redis/redis. 

- [42] S. Rudra. FFmpeg Calls Google’s AI Bug Reports “CVE Slop”. It’s FOSS, 2025. https://itsfoss.com/news/ffmpeg-google-fiasco/. 

https://arxiv.org/abs/2602.07666. Cross-listed in cs.AI. 

   - [55] K. Zhang, Z. Li, D. Wu, S. Wang, and X. Xia. Low-Cost and Comprehensive Non-textual Input Fuzzing with LLM-Synthesized Input Generators. In _Proceedings of the 34th USENIX Security Symposium (Security)_ SEC [1]. 

   - [56] S. Österlund, E. Geretto, A. Jemmett, E. Güler, P. Görz, T. Holz, C. Giuffrida, and H. Bos. Collabfuzz: A framework for collaborative fuzzing. In _Proceedings of the 14th European Workshop on Systems Security_ , EuroSec ’21, pages 1–7. Association for Computing Machinery, 2021. doi: 10.1145/3447852.3458720. URL https://doi.org/10.1145/3447852.3458720. 

- [43] K. Serebryany, D. Bruening, A. Potapenko, and D. Vyukov. AddressSanitizer: A Fast Address Sanity Checker. In _2012 USENIX Annual Technical Conference (USENIX ATC 12)_ , pages 309–318, 2012. 

- [44] Z. Sheng, Q. Xu, J. Huang, M. Woodcock, H. Huang, A. F. Donaldson, G. Gu, and J. Huang. All You Need Is A Fuzzing Brain: An LLMPowered System for Automated Vulnerability Detection and Patching, Sept. 2025. URL http://arxiv.org/abs/2509.07225. arXiv:2509.07225 [cs]. 

- [45] D. Stenberg. AI slop security reports submitted to curl. GitHub Gist, 2025. https://gist.github.com/bagder/ 07f7581f6e3d78ef37dfbfc81fd1d1cd. 

- [46] D. Stenberg. The end of the curl bug-bounty. Daniel Stenberg Blog, 2026. https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bugbounty/. 

- [47] the Big Sleep team. From Naptime to Big Sleep: Using Large Language Models To Catch Vulnerabilities In Real-World Code. Project Zero, 2024. https://projectzero.google/2024/10/from-naptimeto-big-sleep.html. 

- [48] M. Walker. Machine vs. Machine: Lessons from the First Year of Cyber Grand Challenge. In _24th USENIX Security Symposium (USENIX Security 15)_ , Washington, D.C., Aug. 2015. USENIX Association. 

- [49] P. Wang, X. Liu, and C. Xiao. CVE-Bench: Benchmarking LLMbased Software Engineering Agent’s Ability to Repair Real-World CVE Vulnerabilities. In L. Chiruzzo, A. Ritter, and L. Wang, editors, _Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)_ , pages 4207–4224, Albuquerque, New Mexico, Apr. 2025. Association for Computational Linguistics. ISBN 979-8-89176-189-6. doi: 10.18653/v1/2025.naacllong.212. URL https://aclanthology.org/2025.naacl-long.212/. 

- [50] C. S. Xia, M. Paltenghi, J. L. Tian, M. Pradel, and L. Zhang. Fuzz4ALL: Universal Fuzzing with Large Language Models. In _Proceedings of the IEEE/ACM 46th International Conference on Software Engineering_ , ICSE ’24, pages 126:1–126:13. Association for Computing Machinery, 2024. 

- [51] Y. Yang, S. Yao, J. Chen, and W. Lee. Hybrid Language Processor Fuzzing via LLM-Based Constraint Solving. In _Proceedings of the 34th USENIX Security Symposium (Security)_ SEC [1]. 

- [52] Z. Yu, Z. Guo, Y. Wu, J. Yu, M. Xu, D. Mu, Y. Chen, and X. Xing. PatchAgent: A Practical Program Repair Agent Mimicking Human Expertise. In _34th USENIX Security Symposium (USENIX Security 25)_ , pages 4381–4400, 2025. 

- [53] A. K. Zhang, N. Perry, R. Dulepet, J. Ji, C. Menders, J. W. Lin, E. Jones, G. Hussein, S. Liu, D. J. Jasper, P. Peetathawatchai, A. Glenn, V. Sivashankar, D. Zamoshchin, L. Glikbarg, D. Askaryar, H. Yang, A. Zhang, R. Alluri, N. Tran, R. Sangpisit, K. O. Oseleononmen, D. Boneh, D. E. Ho, and P. Liang. Cybench: A framework for evaluating cybersecurity capabilities and risks of language models. In _The Thirteenth International Conference on Learning Representations_ , 2025. URL https://openreview.net/forum?id=tc90LV0yRL. 

- [54] C. Zhang, Y. Park, F. Fleischer, Y.-F. Fu, J. Kim, D. Kim, Y. Kim, Q. Xu, A. Chin, Z. Sheng, H. Zhao, B. J. Lee, J. Wang, M. Pelican, D. J. Musliner, J. Huang, J. Silliman, M. Mcdaniel, J. Casavant, I. Goldthwaite, N. Vidovich, M. Lehman, and T. Kim. Sok: Darpa’s ai cyber challenge (aixcc): Competition design, architectures, and lessons learned. _arXiv_ , 2026. doi: 10.48550/arXiv.2602.07666. URL 

12 

## **Appendix** 

We present the complete `crs.yaml` and `crs-compose.yaml` configuration files for the three CRSs integrated in §4: CRS-LIBFUZZER (§4.2), ATLANTIS-MULTILANG (§4.3), and CLAUDECODE (§4.4). The `crs.yaml` manifest declares each CRS’s capabilities, supported languages, required LLM models, and build/run phase definitions, while `crs-compose.yaml` specifies resource allocations and runtime settings for a given deployment, including an ensemble example that combines multiple CRSs in a single run. We also include the LiteLLM proxy configurations used for multi-model routing (§3.5): one for ATLANTIS-MULTILANG, which routes directly to upstream providers, and one for CLAUDECODE, which proxies requests to an external LiteLLM instance. 

**Listing 1:** `crs.yaml` for CRS-LIBFUZZER 

1 `name: crs-libfuzzer` 2 `type:` 3 `- bug-finding` 4 `version: 1.0.0` 5 `docker_registry: ghcr.io/oss-crs/crs-libfuzzer` 6 7 `prepare_phase:` 8 `hcl: oss-crs/docker-bake.hcl` 9 10 `target_build_phase:` 11 `- name: build` 12 `dockerfile: oss-crs/dockerfiles/builder.Dockerfile` 13 `outputs:` 14 `- build` 15 16 `crs_run_phase:` 17 `fuzzer:` 18 `dockerfile: oss-crs/dockerfiles/runner.Dockerfile` 19 20 `supported_target:` 21 `mode:` 22 `- full` 23 `- delta` 24 `language:` 25 `- c` 26 `sanitizer:` 27 `- address` 28 `architecture:` 29 `- x86_64` 

13 

1 `name: atlantis-multilang-wo-concolic` 2 `type:` 3 `- bug-finding` 4 `version: 1.0.0` 5 `docker_registry: ghcr.io/oss-crs/atlantis-multilang-wo-concolic` 6 

7 `prepare_phase:` 8 `hcl: oss-crs/docker-bake.hcl` 9 10 `target_build_phase:` 11 `- name: uniafl-build` 12 `dockerfile: oss-crs/dockerfiles/builder.Dockerfile` 13 `additional_env:` 14 `BUILD_TYPE: uniafl` 15 `outputs:` 16 `- uniafl/build` 17 `- uniafl/src` 18 `- uniafl/project` 19 `- name: coverage-build` 20 `dockerfile: oss-crs/dockerfiles/builder.Dockerfile` 21 `additional_env:` 22 `BUILD_TYPE: coverage` 23 `outputs:` 24 `- coverage/build` 25 `- name: lsp-build` 26 `dockerfile: oss-crs/dockerfiles/lsp_builder.Dockerfile` 27 `outputs:` 28 `- lsp/compile_commands.json` 29 `- name: create-config` 30 `dockerfile: oss-crs/dockerfiles/multilang.Dockerfile` 31 `additional_env:` 32 `RUN_TYPE: CREATE_CONFIG` 33 `outputs:` 34 `- uniafl/config.yaml` 35 36 `crs_run_phase:` 37 `multilang:` 38 `dockerfile: oss-crs/dockerfiles/multilang.Dockerfile` 39 `additional_env:` 40 _`# Input generators for fuzzing (comma-separated)`_ 41 _`# Available options:`_ 42 _`# - given_fuzzer: Use provided seed corpus (default)`_ 43 _`# - testlang_input_gen: Test language-based input generation`_ 44 _`# - dict_input_gen: Dictionary-based input generation`_ 45 _`# - mlla: Multi-language LLM agent for input generation`_ 46 `CRS_INPUT_GENS: given_fuzzer,mlla,testlang_input_gen,dict_input_gen` 47 `redis:` 

48 `dockerfile: oss-crs/dockerfiles/redis.Dockerfile` 

49 `init_codeindexer:` 

50 `dockerfile: oss-crs/dockerfiles/multilang.Dockerfile` 51 `additional_env:` 

52 `RUN_TYPE: INIT_CODEINDEXER` 53 `joern:` 54 `dockerfile: oss-crs/dockerfiles/joern.Dockerfile` 55 `lsp:` 56 `dockerfile: oss-crs/dockerfiles/lsp.Dockerfile` 

57 58 `supported_target:` 59 `mode:` 60 `- full` 61 `- delta` 62 `language:` 63 `- c` 64 `sanitizer:` 65 `- address` 66 `architecture:` 67 `- x86_64` 68 69 `required_llms:` 70 `- o4-mini` 71 `- gpt-4o` 72 `- gpt-4o-mini` 73 `- gpt-4.1` 74 `- gpt-4.1-mini` 75 `- claude-sonnet-4-20250514` 76 `- claude-opus-4-20250514` 77 `- claude-3-7-sonnet-20250219` 78 `- claude-3-5-haiku-20241022` 79 `- gemini-2.5-pro` 

**Listing 2:** `crs.yaml` for ATLANTIS-MULTILANG 

14 

1 `name: crs-claude-code` 2 `type:` 3 `- bug-fixing` 4 `version: 1.0.0` 5 `docker_registry: ghcr.io/oss-crs/crs-claude-code` 6 7 `prepare_phase:` 8 `hcl: oss-crs/docker-bake.hcl` 9 10 `target_build_phase:` 11 `- name: default-build` 12 `dockerfile: oss-crs/builder.Dockerfile` 13 `outputs:` 14 `- build` 15 `- src` 16 `- name: inc-builder-asan` 17 `snapshot: true` 18 `dockerfile: oss-crs-infra:default-builder` 19 `additional_env:` 20 `SANITIZER: address` 21 22 `crs_run_phase:` 23 `patcher:` 24 `dockerfile: oss-crs/patcher.Dockerfile` 25 `additional_env:` 26 _`# Set via compose yaml additional_env.`_ 27 `CRS_AGENT: claude_code` 28 _`# ANTHROPIC_MODEL: claude-sonnet-4-5-20250929`_ 29 _`# CLAUDE_CODE_SUBAGENT_MODEL: claude-sonnet-4-5-20250929`_ 30 _`# ANTHROPIC_DEFAULT_OPUS_MODEL: claude-sonnet-4-5-20250929`_ 31 _`# ANTHROPIC_DEFAULT_SONNET_MODEL: claude-sonnet-4-5-20250929`_ 32 _`# ANTHROPIC_DEFAULT_HAIKU_MODEL: claude-sonnet-4-5-20250929`_ 33 _`# AGENT_TIMEOUT: "0" # seconds, 0 = no limit (default)`_ 34 `inc-builder-asan:` 35 `run_snapshot: true` 36 `dockerfile: oss-crs-infra:default-builder` 37 38 `supported_target:` 39 `mode:` 40 `- full` 41 `- delta` 42 `language:` _`# language-agnostic — agent edits source, builder sidecar handles compilation`_ 43 `- c` 44 `- c++` 45 `- jvm` 46 `sanitizer:` 47 `- address` 48 `- undefined` 49 `architecture:` 

50 `- x86_64` 

51 52 `required_llms:` 53 `- claude-opus-4-6` 54 `- claude-sonnet-4-6` 55 `- claude-haiku-4-5-20251001` 56 _`# - claude-opus-4-5-20251101`_ 57 _`# - claude-sonnet-4-5-20250929`_ 58 _`# - claude-haiku-4-5-20251001`_ 

**Listing 3:** `crs.yaml` for CLAUDECODE 

1 _`# --- General Settings -------------------------------------------------------`_ 

2 `run_env: local` 3 `docker_registry: local` 4 

5 _`# --- Infrastructure ---------------------------------------------------------`_ 6 `oss_crs_infra:` 7 `cpuset: "0-3"` 8 `memory: "16G"` 9 10 _`# --- CRS (crs-libfuzzer) ---------------------------------------------------`_ 

11 _`# Pure fuzzer — no LLM or builder sidecar needed.`_ 12 `crs-libfuzzer:` 13 `cpuset: "4-7"` 14 `memory: "16G"` 

**Listing 4:** `crs-compose.yaml` for CRS-LIBFUZZER 

15 

1 _`# --- General Settings -------------------------------------------------------`_ 2 `run_env: local` 3 `docker_registry: local` 4 5 _`# --- Infrastructure ---------------------------------------------------------`_ 6 `oss_crs_infra:` 7 `cpuset: "0-3"` 8 `memory: "16G"` 9 10 _`# --- CRS (atlantis-multilang-wo-concolic) -----------------------------------`_ 11 `atlantis-multilang-wo-concolic:` 12 `cpuset: "4-8"` 13 `memory: "16G"` 14 `llm_budget: 100` 15 16 _`# --- LLM Configuration -----------------------------------------------------`_ 17 `llm_config:` 18 `litellm:` 19 `mode: internal` 20 `internal:` 21 `config_path: ./example/atlantis-multilang-wo-concolic/litellm-config.yaml` 

**Listing 5:** `crs-compose.yaml` for ATLANTIS-MULTILANG 

1 _`# --- General Settings -------------------------------------------------------`_ 2 `run_env: local` 3 `docker_registry: local` 4 5 _`# --- Infrastructure ---------------------------------------------------------`_ 6 `oss_crs_infra:` 7 `cpuset: "0-1"` 8 `memory: "8G"` 9 10 _`# --- CRS (crs-claude-code) -------------------------------------------------`_ 11 _`# Builder sidecars are declared in crs.yaml (snapshot: true / run_snapshot: true)`_ 12 _`# and handled automatically by the framework — no separate entry needed.`_ 13 `crs-claude-code:` 14 `cpuset: "2-7"` 15 `memory: "16G"` 16 `llm_budget: 10` 17 `additional_env:` 18 _`# Override CRS defaults here. Available models:`_ 19 _`# claude-opus-4-6, claude-opus-4-5-20251101, claude-opus-4-1-20250805,`_ 20 _`# claude-sonnet-4-5-20250929, claude-sonnet-4-20250514, claude-haiku-4-5-20251001`_ 21 `CRS_AGENT: claude_code` 22 `ANTHROPIC_MODEL: claude-opus-4-6` 23 _`# CLAUDE_CODE_SUBAGENT_MODEL: claude-sonnet-4-5-20250929`_ 24 _`# ANTHROPIC_DEFAULT_OPUS_MODEL: claude-sonnet-4-5-20250929`_ 25 _`# ANTHROPIC_DEFAULT_SONNET_MODEL: claude-sonnet-4-5-20250929`_ 26 _`# ANTHROPIC_DEFAULT_HAIKU_MODEL: claude-sonnet-4-5-20250929`_ 27 _`# AGENT_TIMEOUT: "3600" # Optional: seconds, 0 = no limit (default)`_ 28 29 _`# --- LLM Configuration -----------------------------------------------------`_ 30 `llm_config:` 31 `litellm:` 32 `mode: internal` 33 `internal:` 34 `config_path: ./example/crs-claude-code/litellm-config.yaml` 

**Listing 6:** `crs-compose.yaml` for CLAUDECODE 

16 

|1|_`# --- General Settings -------------------------------------------------------`_|
|---|---|
|2 <br>3|`run_env: local`<br>`docker_registry: local`|
|4||
|5 <br>|_`# --- Infrastructure ---------------------------------------------------------`_<br>|
|6|`oss_crs_infra:`<br>|
|7|`cpuset: "0-3"`<br>|
|8|`memory: "16G"`|
|9||
|10 <br>|_`# --- CRS (crs-libfuzzer) ---------------------------------------------------`_<br>|
|11|`crs-libfuzzer:`<br>|
|12|`cpuset: "8-11"`<br>|
|13|`memory: "16G"`|
|14||
|15|_`# --- CRS (atlantis-multilang-wo-concolic) -----------------------------------`_|
|16|`atlantis-multilang-wo-concolic:`|
|17|`cpuset: "4-7"`|
|18|`memory: "16G"`|
|19|`llm_budget: 100`|
|20||
|21|_`# --- LLM Configuration -----------------------------------------------------`_|
|22|`llm_config:`|
|23|`litellm:`|
|24|`mode: internal`|
|25|`internal:`|
|26|`config_path: ./example/atlantis-multilang-wo-concolic/litellm-config.yaml`|



**Listing 7:** `crs-compose.yaml` for ensemble deployment 

17 

- 1 `model_list:` 2 _`#########################################`_ 3 _`# OPENAI API`_ 4 _`#########################################`_ 5 `- model_name: o4-mini` 6 `litellm_params:` 7 `model: openai/o4-mini` 8 `api_key: os.environ/OPENAI_API_KEY` 9 

- 10 `- model_name: gpt-4o` 11 `litellm_params:` 12 `model: openai/gpt-4o` 13 `api_key: os.environ/OPENAI_API_KEY` 14 15 `- model_name: gpt-4o-mini` 16 `litellm_params:` 17 `model: openai/gpt-4o-mini` 18 `api_key: os.environ/OPENAI_API_KEY` 19 

- 20 `- model_name: gpt-4.1` 21 `litellm_params:` 22 `model: openai/gpt-4.1` 23 `api_key: os.environ/OPENAI_API_KEY` 

- 24 25 `- model_name: gpt-4.1-mini` 26 `litellm_params:` 27 `model: openai/gpt-4.1-mini` 28 `api_key: os.environ/OPENAI_API_KEY` 29 30 _`#########################################`_ 

- 31 _`# ANTHROPIC API`_ 

- 32 _`#########################################`_ 

- 33 `- model_name: claude-3-7-sonnet-20250219` 34 `litellm_params:` 35 `model: anthropic/claude-3-7-sonnet-20250219` 36 `api_key: os.environ/ANTHROPIC_API_KEY` 

37 

- 38 `- model_name: claude-sonnet-4-20250514` 39 `litellm_params:` 40 `model: anthropic/claude-sonnet-4-20250514` 41 `api_key: os.environ/ANTHROPIC_API_KEY` 

42 

43 `- model_name: claude-opus-4-20250514` 44 `litellm_params:` 45 `model: anthropic/claude-opus-4-20250514` 46 `api_key: os.environ/ANTHROPIC_API_KEY` 47 48 `- model_name: claude-3-5-haiku-20241022` 49 `litellm_params:` 50 `model: anthropic/claude-3-5-haiku-20241022` 51 `api_key: os.environ/ANTHROPIC_API_KEY` 52 53 _`#########################################`_ 

54 _`# GEMINI API`_ 55 _`#########################################`_ 56 `- model_name: gemini-2.5-pro` 57 `litellm_params:` 58 `model: gemini/gemini-2.5-pro` 59 `api_key: os.environ/GEMINI_API_KEY` 

**Listing 8:** LiteLLM proxy configuration for ATLANTIS-MULTILANG (§3.5) 

18 

|1 `m`|`odel_list:`|
|---|---|
|2|_`#########################################`_|
|3|_`# ANTHROPIC API (via external LiteLLM)`_|
|4|_`# model_name = what Claude Code sends in API requests (bare names)`_|
|5|_`# litellm_params.model = how LiteLLM routes to the provider`_|
|6|_`#########################################`_|
|7|`- model_name: claude-opus-4-6`|
|8|`litellm_params:`<br>|
|9|`model: anthropic/claude-opus-4-6`|
|10|`api_base: os.environ/EXTERNAL_LITELLM_API_BASE`|
|11|`api_key: os.environ/EXTERNAL_LITELLM_API_KEY`|
|12||
|13|`- model_name: claude-sonnet-4-6`|
|14|`litellm_params:`|
|15|`model: anthropic/claude-sonnet-4-6`|
|16|`api_base: os.environ/EXTERNAL_LITELLM_API_BASE`|
|17|`api_key: os.environ/EXTERNAL_LITELLM_API_KEY`|
|18||
|19|`- model_name: claude-haiku-4-5-20251001`|
|20|`litellm_params:`|
|21|`model: anthropic/claude-haiku-4-5-20251001`|
|22|`api_base: os.environ/EXTERNAL_LITELLM_API_BASE`|
|23|`api_key: os.environ/EXTERNAL_LITELLM_API_KEY`|
|24||
|25|`- model_name: claude-opus-4-5-20251101`|
|26|`litellm_params:`|
|27|`model: anthropic/claude-opus-4-5-20251101`|
|28|`api_base: os.environ/EXTERNAL_LITELLM_API_BASE`|
|29|`api_key: os.environ/EXTERNAL_LITELLM_API_KEY`|
|30||
|31|`- model_name: claude-opus-4-1-20250805`|
|32|`litellm_params:`<br>|
|33|`model: anthropic/claude-opus-4-1-20250805`|
|34|`api_base: os.environ/EXTERNAL_LITELLM_API_BASE`|
|35|`api_key: os.environ/EXTERNAL_LITELLM_API_KEY`|
|36||
|37|`- model_name: claude-sonnet-4-5-20250929`|
|38|`litellm_params:`|
|39|`model: anthropic/claude-sonnet-4-5-20250929`|
|40|`api_base: os.environ/EXTERNAL_LITELLM_API_BASE`|
|41|`api_key: os.environ/EXTERNAL_LITELLM_API_KEY`|
|42||
|43|`- model_name: claude-sonnet-4-20250514`|
|44|`litellm_params:`|
|45|`model: anthropic/claude-sonnet-4-20250514`|
|46|`api_base: os.environ/EXTERNAL_LITELLM_API_BASE`|
|47|`api_key: os.environ/EXTERNAL_LITELLM_API_KEY`|



**Listing 9:** LiteLLM proxy configuration for CLAUDECODE, forwarding to an external LiteLLM instance (§3.5) 

19 

