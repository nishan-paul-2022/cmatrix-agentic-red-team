# **ARVO: Atlas of Reproducible Vulnerabilities for Open Source Software** 

Xiang Mei Arizona State University xmei5@asu.edu 

Pulkit Singh Singaria Arizona State University psingari@asu.edu 

Jordi Del Castillo New York University jordi.d@nyu.edu 

Abdelouahab (Habs) Benchikh Arizona State University abenchik@asu.edu 

Tiffany Bao Arizona State University tbao@asu.edu 

Haoran Xi 

New York University hx759@nyu.edu 

Yan Shoshitaishvili Arizona State University yans@asu.edu 

Adam Doupé Arizona State University doupe@asu.edu 

Ruoyu Wang Arizona State University fishw@asu.edu 

## Hammond Pearce 

Brendan Dolan-Gavitt New York University brendandg@nyu.edu 

University of New South Wales hammond.pearce@unsw.edu.au 

### **ABSTRACT** 

Vulnerability Database (NVD), 4,648 of which were classified as Critical severity (using CVSS V3 scores). Studying the nature of this growing world of vulnerabilities in software is critical, but doing so requires a _vulnerability dataset_ . 

High-quality datasets of real-world vulnerabilities are enormously valuable for downstream research in software security, but existing datasets are typically small, require extensive manual effort to update, and are missing crucial features that such research needs. In this paper, we introduce ARVO: an <u>Atlas of Reproducible Vulnerabilities in Open-source software. By sourcing vulnerabili-</u> ties from C/C++ projects that Google’s OSS-Fuzz discovered and implementing a reliable re-compilation system, we successfully reproduce more than 5,000 memory vulnerabilities across over 250 projects, each with a triggering input, the canonical developerwritten patch for fixing the vulnerability, and the ability to automatically rebuild the project from source and run it at its vulnerable and patched revisions. Moreover, our dataset can be automatically updated as OSS-Fuzz finds new vulnerabilities, allowing it to grow over time. We provide a thorough characterization of the ARVO dataset, show that it can locate fixes more accurately than Google’s own OSV reproduction effort, and demonstrate its value for future research through two case studies: firstly evaluating real-world LLM-based vulnerability repair, and secondly identifying over 300 falsely patched (still-active) zero-day vulnerabilities from projects improperly labeled by OSS-Fuzz. 

However, many existing vulnerability datasets, such as Common Vulnerabilities and Exposures (CVE) and the NVD, are designed to alert users about vulnerabilities in software so that system maintainers can verify affected versions and apply patches for known vulnerabilities in currently deployed software. Due to this focus, these datasets are not effective as a _research vulnerability dataset_ . 

A research vulnerability dataset must consist of real-world vulnerabilities. To be maximally useful, each vulnerability must contain metadata that includes: the input that triggers the vulnerability, the source-code patch that fixes the vulnerability, and the ability to compile the vulnerable and patched versions of the original source code. All of this must be reproducible into the future. 

Unfortunately, creating such a research vulnerability dataset manually is difficult. For example, despite over 3,600 hours of human work into reproducing publicly reported CVEs, Mu et al. [20] only succeeded in reproducing a total of 368 vulnerabilities. 

Another complexity is that, when used as an evaluation benchmark, research vulnerability datasets tend to become “stale” over time as researchers (perhaps unintentionally) tune their systems to achieve good benchmark scores on the research vulnerability dataset without necessarily improving their real-world performance. Therefore, a continuously updated research vulnerability dataset is critical. 

##### **ACM Reference Format:** 

Xiang Mei, Pulkit Singh Singaria, Jordi Del Castillo, Haoran Xi, Abdelouahab (Habs) Benchikh, Tiffany Bao, Ruoyu Wang, Yan Shoshitaishvili, Adam Doupé, Hammond Pearce, and Brendan Dolan-Gavitt. 2024. ARVO: Atlas of Reproducible Vulnerabilities for Open Source Software. In _Proceedings of ACM Conference (Conference’17)._ ACM, New York, NY, USA, 14 pages. https://doi.org/10.1145/nnnnnnn.nnnnnnn 

In this paper, we present ARVO, the ‘Atlas of Reproducible Vulnerabilities.’ ARVO is both a framework designed to address the shortage of research vulnerability dataset and a comprehensive bug dataset in its own right. Derived from Google’s OSS-Fuzz project, ARVO aims to achieve a high level of reproducibility across a large number of real-world projects and vulnerabilities, providing a robust set of real-world vulnerabilities for a research vulnerability dataset. We focus on C/C++ projects due to their widespread use and the significant impact of bugs in these languages. 

### **1 INTRODUCTION** 

Vulnerabilities in software are both common and damaging: in 2023 alone, more than 28,000 vulnerabilities were tracked by the National 

_Conference’17, July 2017, Washington, DC, USA_ 2024. ACM ISBN 978-x-xxxx-xxxx-x/YY/MM...$15.00 https://doi.org/10.1145/nnnnnnn.nnnnnnn 

1 

Xiang Mei, Pulkit Singh Singaria, Jordi Del Castillo, Haoran Xi, Abdelouahab (Habs) Benchikh, Tiffany Bao, Ruoyu Wang, Yan Shoshitaishvili, Adam Doupé, Hammond Pearce, Conference’17, July 2017, Washington, DC, USA and Brendan Dolan-Gavitt 

The ARVO dataset has the following key features: (1) _large-scale_ : 5,001 vulnerabilities across 273 projects at the time of this writing; (2) _recompilable_ : ARVO can rebuild the project at its vulnerable and patched versions for each vulnerability in the dataset; (3) _triggering inputs_ : Each vulnerability has a proof-of-concept “triggering” input that can be used to test for the presence of the vulnerability; (4) _precise fixes_ : For vulnerabilities in ARVO, we isolate and provide the precise developer patch that fixes the vulnerability; and (5) _usable_ : We provide prebuilt container images for each vulnerability, allowing issues to be reproduced with a single command such as docker run -it –rm n132/arvo:25402-vul arvo. 

These features, as well as the fact that it can be continuously updated with new vulnerabilities with minimal manual effort, make the ARVO dataset well-suited as an on-going evaluation dataset for many downstream tasks in software security research, such as vulnerability discovery, fault localization, patch reduction, and automated program repair. 

ARVO functions by ingesting bug reports from Google’s OSSFuzz bug tracker [25], which provides findings from the continuous fuzzing of over 1,000 open-source projects. Unfortunately, the reports by themselves are not enough to reproduce each vulnerability: while they do provide the revision and triggering input found by the fuzzer, reliably building the target software and its dependencies at the vulnerable version, as well as locating the precise patch that fixes the issue, require significant additional effort. 

Although OSS-Fuzz does provide a tool<sup>1</sup> for reproducing historical issues, it can only reproduce 13% of the issues we tested in OSS-Fuzz, particularly with older projects with many dependencies. As discussed in Section 4, ARVO achieves a much higher success rate (63%) by carefully tracking project dependencies and identifying the precise version needed, as well as mitigating the impact of missing assets (e.g., when a dependency or resource has been relocated or removed). With these reliable reproducing methods, ARVO located 5,001 patches over 5,651 vulnerabilities by bisection, and achieved 52.5% more cases than OSV-OSS-Fuzz [13], the current state-of-the-art approach. After rebuilding the project at the vulnerable version we also verified that the vulnerability can be reproduced and created public, pre-built Docker images for each issue, allowing it to be reproduced even if its dependencies succumb to bit rot. 

To evaluate the accuracy of ARVO’s patch identification, we conduct a comparison experiment in Section 5.3 between ARVO and Google’s own OSS-Fuzz reproduction effort, which attempts to identify the commits that introduced and fixed each vulnerability in OSS-Fuzz; this data is automatically published to the OSV database [13]. For each issue, we check if the commit ARVO identifies matches the one listed by OSV, and manually investigate any discrepancies to decide which is correct, finding that ARVO achieves much better results than OSV for the cases where the two systems disagree over the overlapped cases. 

Using ARVO, we uncovered several _hundred_ cases of “false positive fixes”, where issues marked as fixed by OSS-Fuzz could still be triggered on the most recent version of the project. This could allow malicious actors to harvest unfixed vulnerabilities, which the 

community does not realize are still extant, from OSS-Fuzz’s public issue tracker. 

Finally, in Section 6 we offer several use cases to demonstrate how ARVO dataset can benefit research in software security, by using it to conduct evaluations of LLM-based vulnerability repair and to characterize real-world vulnerability fixes based on the developers’ patches. 

In summary, this paper makes the following contributions: 

- (1) We identify the key challenges in improving reproducibility for research vulnerability datasets and describe our methods for addressing and mitigating these issues. 

- (2) We design a system called ARVO that automatically identifies the correct patch commit from OSS-Fuzz projects and automatically builds a reproducible environment for the vulnerable software system. 

- (3) We present the ARVO dataset, a reproducible, recompilable, and automatically updating dataset of over 5,000 real-world vulnerabilities in open source C/C++ projects. 

- (4) We make ARVO itself—the framework, evaluation infrastructure, images, and metadata— **open-source** , so that other researchers can build on our work. This includes more than 10,000 Docker images that can be used to reproduce each vulnerability and can re-compile after any valid modification of the source code. 

### **2 BACKGROUND** 

Before discussing ARVO, we must first cover existing research vulnerability datasets and the limitations of these techniques. 

### **2.1 Fuzzing and OSS-Fuzz** 

Fuzzing is one of the most widespread techniques for finding vulnerabilities in software, particularly software written in memory unsafe languages such as C and C++ [16, 19, 26]. Since the release of American Fuzzy Lop (AFL) in 2013 [28], fuzzing has attracted considerable attention from academic researchers and industry, and has been used to find vulnerabilities in a wide range of critical software. The most widely used fuzzing technique, _coverage-based greybox fuzzing_ , mutates inputs to a target program, runs the program on those inputs, and selects inputs that expose new _coverage_ for further mutation [24]. 

Meanwhile, open source software continues to gain prominence— as of November 2023 there were 284 million public repositories on GitHub [8]—and is part of the Internet’s “critical infrastructure” [6]. The vast scale of this open source ecosystem over the last decade has seen, with the boost of open-source software and version control systems, the realization and documentation of numerous security bugs. This has previously benefited the building of massive security bug datasets, such as OSV [13]. 

OSV uses the _Open Source Vulnerability Format_ [4] to describe bugs. OSV.dev [13] aggregates several bug datasets that expose data in the OSV format, and this includes more than 115,000 bugs. If we limit the scope to C/C++ projects and to reproducible bugs, OSS-Fuzz includes about 3,300 cases. 

Created by Google in 2016, OSS-Fuzz [25] is an open-source project that performs continuous fuzzing to detect and report security vulnerabilities in over 1,000 open-source projects. Each project 

1infra/build_specified_commit.py 

2 

Conference’17, July 2017, Washington, DC, USA 

ARVO: Atlas of Reproducible Vulnerabilities for Open Source Software 

is expected to provide a _fuzz harness_ that specifies API functions in the project to test. OSS-Fuzz then monitors the project repository, builds the software as new commits are made, fuzzes them with a variety of fuzzers and sanitizers (e.g., AddressSanitizer [11]), automatically reports crashes found by the fuzzers, and periodically checks whether the project has fixed the reported vulnerability. Google’s OSS-Fuzz cluster has helped find and fix more than 10,000 vulnerabilities, as of August 2023 (the last reported data). 

### **2.2 Patch Locating** 

For known vulnerabilities, the corresponding source-code fixes, called _patches_ , are vital to understand. Source code patches are used to detect the existence of patches without source code [7, 15, 29] and for hot-patch generation [1, 5]. Revision control software makes patches possible by recording all the historical changes. However, automatic identification of patches is an unsolved problem. 

The most well-known vulnerability dataset of CVE and NVD not not have patches as a required. Furthermore, for CVE entries with identified patches, there is no guarantee for accuracy and correctness. The purpose of the CVE and NVD datasets is to help alert system maintainers of vulnerabilities and identify vulnerable software versions, not identify the patch. 

Some automated methods such as CVEfixes [2] are designed to map each CVE vulnerability to its patch. These methods use keyword matching [22] and commit comment analysis [27]. However, these focused on the text document/code information that they can extract and analyze, and, therefore, have no guarantee of accuracy. Moreover not all developers will leave comments describing the bug especially when the bug does not have a CVE or the developer does not understand the details of the underlying vulnerability. 

### **2.3 OSV (Open Source Vulnerabilities) and OSS-Fuzz** 

OSS-Fuzz essentially contains a mostly text-based dataset that provides, for each vulnerability, the fuzzer-generated input as Proof of Concept (PoC) to trigger the vulnerability, the security sanitizer report, and the software components revision to ease reproducing. Google’s OSS-Fuzz fuzzing cluster compiles and runs the latest version of the software daily. For the found vulnerabilities, every 24 hours, OSS-Fuzz takes the known PoC as input to run the latest version of software to verify if the bug is fixed. 

While this method automates vulnerability discovery and can be used to build a research vulnerability dataset, the verification of the patch can have a 24-hour delay. Therefore, OSS-Fuzz vulnerability reports are coarse-grained and include a range of commits. 

OSV (Open Source Vulnerabilities) is a database that collects vulnerability reports from different software (called projects on OSV), including OSS-Fuzz, Linux, and Ubuntu. However, after checking all the ecosystems on OSV including more than 1,000 vulnerabilities, we found OSS-Fuzz is the only C/C++-focused ecosystem that provides patches for generic OSS projects. 

To generate OSV reports for OSS-Fuzz and identify the patch, OSS-Fuzz has a sub-project called OSS-Fuzz-Vulns [12], which performs automatic bisection search and repository analysis. Based on the PoC obtained from fuzzing, OSS-Fuzz-Vulns can tell if a version might be vulnerable or not by walking the revisions and decided 

which version is affected and which is not. Based on this method and from automating the pipeline earlier (since 2021) they have around 3,300 cases 

Surprisingly, the data from OSS-Fuzz is often unreliable and inaccurate. For instance, consider OSV-2020-1676<sup>2</sup> which identifies a specific commit as the patch for a heap buffer overflow vulnerability. Yet, upon inspection, this commit does not alter the source code at all; instead, it simply adds a text file for GitHub Actions configuration, which cannot fix the underlying vulnerability<sup>3</sup> . 

In Section 4 we evaluate OSS-Fuzz reproduction in detail, highlighting the limitations, and discuss our approach to improving the reproduction success rate from 13% to 63%. 

### **3 REPRODUCIBILITY** 

A significant contribution of ARVO is the focus on the reproducibility of the ARVO dataset. Unlike prior work, ARVO allows not only for replaying the PoCs for the vulnerable and fixed version of the system, but also for the _recompilation_ of each version of the software. To accomplish this goal, there are several challenges, which we highlight herein. 

In this paper, we judge the reproducibility of research vulnerability datasets on two criteria: the resources needed for reproduction and the reproduction pipelines. 

**Reproducing Resources** is all necessary metadata needed to reproduce a vulnerability, including vulnerability descriptions, source code of the related components, environment to reproduce, compile methods/scripts, an example of a vulnerable binary, the Proof of Concept (PoC) input that triggers the vulnerability, and the corresponding patch. 

**Reproducing Pipeline** allows the ability to easily reproduce the vulnerabilities. We focus on only the pipeline reproducing success rate and the required maintenance to measure the pipeline. This is a challenges because of the complexity of resolving missing resources (which we’ll discuss later in Section 3.2) and limited control on the upstream software. 

### **3.1 Why Recompilation?** 

Our definition of reproducibility requires recompilation, which is not a common feature supported by most datasets. The lack of recompilation limits the applicability of the datasets to several research directions. For example, novel methods, such as white-box fuzzing [3] and program repair [14, 17], require a dataset that supports recompilation to perform the evaluation. Moreover, recompilation ensures that the resulting binary is reliable and reproducible, which avoids incorrect vulnerabilities in the dataset. However, such a reproducible, recompilable, and scalable research vulnerability dataset is still missing. 

### **3.2 Challenges** 

Any large-scale research vulnerability dataset creation system must solve the following reproduction challenges, much of which stem from attempting to compile an old version of an open-source software system. 

2https://osv.dev/vulnerability/OSV-2020-1676 

3https://github.com/strukturag/libheif/commit/085531bd09a364deb759513204107bf8c99b0402 

3 

Xiang Mei, Pulkit Singh Singaria, Jordi Del Castillo, Haoran Xi, Abdelouahab (Habs) Benchikh, Tiffany Bao, Ruoyu Wang, Yan Shoshitaishvili, Adam Doupé, Hammond Pearce, Conference’17, July 2017, Washington, DC, USA and Brendan Dolan-Gavitt 

**Mismatched Dependencies.** While the source code is available in a revision control system, a key issue is the libraries and other dependencies that a specific version of the software depends on. Often, the exact version of the dependency is not directly specified in the revision control system. For instance, consider a system where the build process fetches the main branch of a dependency to build it. Clearly, this is not reproducible, as building a five-year-old version of this system will likely not compile against the current version of the dependency. Therefore, any reproducible and recompilable research vulnerability dataset creation system must handle dependencies, and Section 4.3 discusses how we solve this challenge. **Missing Resources.** A related issue to mismatched dependencies is missing resources, which is when the software system attempts to fetch the source of a dependency, however the dependency is no longer available. One example is that the website that hosted the dependency changed domain names. Another example is the PCRE library, which in 2021 switched from an FTP server hosting an SVN repository to a git repo hosted on GitHub. This issue becomes much more frequent as the number of dependencies of the software increases and as time increases. We discuss in Section 4.3 how ARVO handles this challenge. 

**Automated Pipeline.** Prior work [20] spent 1,600 man-hours reproducing 202 out of 368 vulnerabilities. This underscores the need for an automated system that can continuously expand the dataset with new entries. Therefore, we design ARVO specifically to be automated and run with minor manual analysis. 

### **3.3 Unsuitability of Prior Work** 

In light of the previously identified challenges, we now focus on current vulnerability datasets and demonstrate the need for ARVO. 

CVE and NVD only include a vulnerability description and sometimes a third-party URLs, which can be a report from another dataset, a commit of the patch, or a blog from the vulnerability discoverer. Therefore, there is not enough information to reproduction and requires manual effort of security professionals. 

OSS-Fuzz-Vuln (described in Section 2.3) aimed to solve the automation pipeline challenge by building a pipeline to fuzz opensource software. While this reduces manual analysis, significant manual effort is still needed to reproduce the vulnerability. 

This effort is because the reproducing pipeline on OSS-Fuzz is neither reliable nor strong. Most OSS-Fuzz reports only include the two-component revisions: (1) the version that found the bug and (2) the version when the crash stopped. These versions do not correspond to patches, as they are created daily (and can include many commits in a busy open-source project). 

Therefore, locating the vulnerability patches requires recompiling old versions of the targets, and to derive this data for OSSFuzz-Vuln, OSS-Fuzz performed bisection over commits that could include the fix. However, OSS-Fuzz only found the patches for about 3,300 cases out of more than 10,000 reported bugs. 

In addition, to measure reproducibility and recompilability, we selected 100 random cases (from the 10,000 reported bugs) and found only 13 cases that can reproduce the crash and the fix. Therefore, this motivates the need for a new system that can generate a research vulnerability dataset that is reproducible, recompilable, and scalable. 


![](docs/paper-research/md-downloaded-paper-professor/images/30-arvo-atlas-of-reproducible-vulnerabilities-for-open-source.pdf-0004-10.png)


<!-- Start of picture text -->
Existing<br>Databases DockerHub<br> Reproducer Patch Locator ARVO<br>Images<br>Database<br><!-- End of picture text -->

**Figure 1: Overview of ARVO.** 

### **4 ARVO** 

We designed ARVO with the goal of producing a reproducible and scalable vulnerability dataset and solving the challenges mentioned in Section 3.2. In detail, we aim to achieve: 

**Reproducibility.** Provide all the reproducing resources mentioned in Section 3.2 and a reliable pipeline to re-compile the (vulnerable/fixed) targets from the source code. 

**Scalability.** The dataset should contain a large number of vulnerabilities and automatically incorporate new vulnerabilities as they are found, to allow the dataset to expand and grow easily over time. 

**Quality and Diversity.** Each vulnerability in the dataset should be validated to ensure it is actually a bug with security impact. The vulnerabilities should be distributed across a large number of different projects, to ensure that evaluations using the dataset are representative. 

**Ease of Use.** The dataset should be easy for researchers and practitioners to use, without requiring them to have extensive security background or know how to build the projects in the dataset. 

In this section, we will describe the methods used in ARVO and the improvement the methods made compared to prior work; in Section 5 we characterize ARVO and demonstrate that it achieves these goals. Overall, it is able to successfully reproduce 5,651 out of 8,934 vulnerabilities sourced from OSS-Fuzz (63.3%), and identifies the precise fix for 5,001 (88.5%) of the reproduced cases. 

### **4.1 Overview** 

ARVO is an interactive framework to generate a research vulnerability dataset, designed to ingest source metadata from ‘bug’/project databases and augment this information with relevant source code, build steps, and binaries. Because we hope to support downstream uses such as analysis of security patches, evaluating vulnerability discovery systems, and automated vulnerability repair, the ARVO dataset also needs to include environments for re-compiling the code of each project so that modifications to the source code can be straightforwardly tested. To enable easy access, ARVO provides an online Dockerized dataset as well as infrastructure to build the dataset from scratch. 

ARVO consists of two major components, shown in Figure 1: (1) the reproducer and (2) the vulnerability patch locator, and ARVO outputs the ARVO dataset. 

The reproducer takes the provided metadata from the upstream bug database(s), compiles the project binary for the specified (vulnerable) version, and verifies that the provided triggering input causes a crash. It also checks whether the vulnerability was actually fixed by the fix commit listed in the metadata by compiling the project at the fixed version checking that the program no longer 

4 

Conference’17, July 2017, Washington, DC, USA 

ARVO: Atlas of Reproducible Vulnerabilities for Open Source Software 

crashes. If either of these steps fails, we consider the vulnerability unreproducible and exclude it from the dataset; we provide an analysis of the causes of such failures in Section 4. 

However, as previously discussed, the upstream metadata often does not provide the exact commit that fixes the issue, but rather a range of possible commits. ARVO’s vulnerability patch locator searches this commit range to find the earliest commit that resolves the issue; because we prepared reproducible project build environments, we can bisect the commit history to identify the exact changes that fix the vulnerability. 

### **4.2 Source Data** 

To obtain a large number of vulnerabilities and allow the dataset to grow over time, ARVO is designed to draw project and bug metadata from upstream sources (currently, OSS-Fuzz). We rely on some assumptions about the upstream data source (discussed in Section 3): 

- ∎ Version Information: To reproduce the issue and find the precise fix, we need version identifiers (e.g., git commit hashes) referencing the project’s revision control system that identify the vulnerable and non-vulnerable version of the project and its dependencies. If these are not available, however, we could (with some loss of precision) fall back to relying on timestamps to locate the appropriate versions. 

- ∎ Build Environment: This refers to a virtualized, interactive environment able to compile and execute the target programs and their dependencies. 

- ∎ Crash Information: At minimum, we need a triggering input and the command to execute the target program on that input. Additional information such as sanitizer output can also be used to validate that the crash we observe is the same one identified by the upstream source, but this is not strictly necessary. 

The current implementation of ARVO uses OSS-Fuzz as its upstream source. To identify security-relevant issues with metadata we need, we searched the issue tracker according to the labels OSS-Fuzz automatically applies to each issue: Type=Bug-Security (the crash is likely to be security-relevant, based on the sanitizer report and call stack), label:Reproducible (the crash occurs deterministically whenever the triggering input is provided), and status:Verified (OSS-Fuzz verified that the target no longer crashes<sup>4</sup> ). Combining these query elements, we obtain 8,934 issues in over 300 projects after filtering obvious false positives (the vulnerable version is the same as the fixed version), which serve as the starting point for our dataset. 

### **4.3 Reproducer** 

To reproduce an issue and locate its precise fix, ARVO must be able to build the project and its dependencies from source at different commits. However, this poses a number of challenges, particularly for older vulnerabilities where dependencies, resources, and toolchains may have been lost over time. Using the techniques described in this section, ARVO’s Reproducer component can successfully reproduce 5,651 vulnerabilities out of 8,934 vulnerabilities 

4We will see in Section 6.2 that this label is not always accurate; we found over 300 cases where the provided test case still crashes the most recent version of the project. 

(63.3%); this is a significant improvement over the 13% success rate achieved by OSS-Fuzz’s provided reproducer. 

We identify three key strategies that ARVO uses to improve the reproducibility of vulnerabilities: 1) revision control; 2) minimally intrusive build instrumentation; and 3) fixing missing resources. These strategies are implemented in the ARVO reproducer, as shown in Figure 2. 

### **Revision Control** 

Successfully reproducing a vulnerability requires precise information about the build environment and versions of the main project and its dependencies. We found that the information provided by OSS-Fuzz is generally sufficient: the build environments (the OSS-Fuzz base_builder Docker container images with the compiler toolchain used to build the project) are publicly archived, and a publicly-accessible Google Cloud Storage bucket stores a srcmap.json file for each build with the commit hashes for the project and dependencies<sup>5</sup> . 

### **Build Instrumentation** 

The build scripts used by OSS-Fuzz to compile the fuzz targets for each project are provided by the project developers in two parts: a Dockerfile (derived from base_builder) that downloads dependencies and external resources, and a build.sh script that actually compiles the fuzz targets. Because these build scripts can contain arbitrary commands, it is challenging to control the revisions of the project and its dependencies. The reproducer provided by OSS-Fuzz adjusts the main project to the correct commit, but it does not attempt to set dependencies to their corresponding versions. This leads to compatibility issues and build failures when dependencies have changed their APIs or build procedures. For instance, imagemagick relies on 15 separate components, each with frequently changing APIs and usage patterns, and attempting to reproduce a vulnerability in imagemagick without adjusting the dependencies to match the vulnerable version will likely result in a failed build. 

Figure 3 shows a simplified version of the workflow used to build OSS-Fuzz projects. First, the Dockerfile is used to download the resources needed before compiling (shown in blue on the left). This step not only runs commands such as git clone to download necessary resources but also executes some scripts such as git submodule init or custom initialization steps. Then, after all the components are initialized, in the red part, compile starts in the Docker container. 

When rolling back dependency versions, we attempt to be _minimally intrusive_ and make our changes only at the download stage. Starting with the dependency names and commit hashes provided in srcmap.json, we locate the point where the dependency is fetched in the Dockerfile by looking for git, Mercurial, or SVN commands referencing the dependency’s repository URL. We then add a command immediately after the download that rolls back the dependency to the correct commit. In some cases, where the provided version cannot be found (e.g., if the revision history for the project has been rewritten) we use the issue timestamp to identify the 

5The storage bucket also provides the original build artifacts (i.e., the actual binaries that were used during fuzzing), but ARVO does not use them. 

5 

Xiang Mei, Pulkit Singh Singaria, Jordi Del Castillo, Haoran Xi, Abdelouahab (Habs) Benchikh, Tiffany Bao, Ruoyu Wang, Yan Shoshitaishvili, Adam Doupé, Hammond Pearce, Conference’17, July 2017, Washington, DC, USA and Brendan Dolan-Gavitt 


![](docs/paper-research/md-downloaded-paper-professor/images/30-arvo-atlas-of-reproducible-vulnerabilities-for-open-source.pdf-0006-01.png)


<!-- Start of picture text -->
Revision Control<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/30-arvo-atlas-of-reproducible-vulnerabilities-for-open-source.pdf-0006-02.png)



![](docs/paper-research/md-downloaded-paper-professor/images/30-arvo-atlas-of-reproducible-vulnerabilities-for-open-source.pdf-0006-03.png)



![](docs/paper-research/md-downloaded-paper-professor/images/30-arvo-atlas-of-reproducible-vulnerabilities-for-open-source.pdf-0006-04.png)



![](docs/paper-research/md-downloaded-paper-professor/images/30-arvo-atlas-of-reproducible-vulnerabilities-for-open-source.pdf-0006-05.png)


<!-- Start of picture text -->
OSS-Fuzz Repo Revision Control Fetch Missing Resource<br>Fail<br>Version Build Docker Binary<br>Information Image<br>OSS-Fuzz Dataset Missing Resource<br>DB<br>Compile<br>Dockerfile and<br>Components and Revision Control<br>Dependencies Build Scripts Docker Image Fetch<br>Missing Resource<br>Success<br>Success Fail<br><!-- End of picture text -->

**Figure 2: ARVO Reproducer Structure** 

**Table 1: Successful Reproducing Count when Revision Control is Enabled and Disabled.** 

|**# Dependencies**|**Enabled**|**Disabled**|
|---|---|---|
|0|41|39|
|1|27|17|
|2-10|22|2|
|>10|10|0|




![](docs/paper-research/md-downloaded-paper-professor/images/30-arvo-atlas-of-reproducible-vulnerabilities-for-open-source.pdf-0006-09.png)


<!-- Start of picture text -->
Docker Build Docker Run<br>Download<br>Component<br>Prepare Base<br>Compile<br>Image Initialize<br>Component<br><!-- End of picture text -->

**Figure 3: Simplified Compiling Procedure** 

closest commit before the vulnerability was found. This approach minimizes the impact of our changes on the build process, reducing the likelihood of introducing new compatibility issues. 

By contrast, the original OSS-Fuzz reproducer attempts to adjust the version of the main project by preparing the project source outside the build container and mounting it in the container before running the build script. This requires parsing the Dockerfile and attempting to reproduce any necessary post-checkout initialization steps carried out during docker build, which is challenging and often fails in practice. ARVO sidesteps these issues by ensuring that dependencies are at the correct versions as soon as they are fetched and allowing all other build steps to proceed as normal. 

We found that correcting dependency versions is crucial for reproducing historical vulnerabilities. To demonstrate the impact of incorrect dependency versions, we performed an ablation test with 100 randomly selected issues that ARVO was able to reproduce. We then disabled the dependency revision control component and attempted to reproduce the issues; as seen in Table 1, the overall reproducing success rate decreased dramatically from 100% to 58%. We also note that vulnerabilities in projects with many dependencies are more likely to fail to reproduce without dependency revision control. When we disable the revision control, the successfully reproduced cases’ have 0.45 dependencies on average while the failed cases have 8.48 dependencies on average, which clearly 

shows the importance of revision control. Thus, if we do not account for dependency versions, the resulting dataset may be biased towards simpler projects with fewer dependencies. 

### **Broken Resource Fixing** 

Similar to “bit rot” in software, while reproducing old vulnerabilities, we encountered numerous dependencies where components were no longer accessible, particularly for projects from the 2017–2019 period. During this time, many projects migrated their repositories from Subversion to git, which breaks build scripts that reference the old repositories. Additionally, certain build scripts rely on tools and resources downloaded from the Internet, which may become unavailable over time. Because the failure of any step in the build process causes the entire process to fail, broken resources must be resolved to successfully reproduce the vulnerability. 

We divide missing resources into two categories: _core resources_ , which are necessary to compile the fuzz target, and _non-core resources_ , which are not necessary for compilation but are required for other parts of the build process. Core resources include software dependencies such as libraries as well as tools used by the build process that may be necessary to compile key components. Non-core resources include documentation generation tools, seed corpora used during the fuzzing process, and other resources that are not directly related to the fuzz target. 

6 

Conference’17, July 2017, Washington, DC, USA 

ARVO: Atlas of Reproducible Vulnerabilities for Open Source Software 


![](docs/paper-research/md-downloaded-paper-professor/images/30-arvo-atlas-of-reproducible-vulnerabilities-for-open-source.pdf-0007-02.png)


<!-- Start of picture text -->
Vulnerability<br>Found<br>6f6caf f3a481 51cbb7 fc3c6f 577566 57be67 893aea<br>7ff4ae 352a9a 9928af c27d49 0efff0 05b88b4 f939c2 a a668b<br>Fix<br>Vulnerability<br>Verified<br>Fixed<br><!-- End of picture text -->

**Figure 4: Vulnerability lifecycle for OSS-Fuzz issue 44851 on Imagemagick.** 

To identify missing resources we capture and log the error messages generated during the build process and look for errors related to failed URL downloads. We then manually classified these as core or non-core resources. For non-core resources, we simply modify the build script to remove the resource. For core resources, we manually locate the missing resource and replace it with a working URL. These resource fixups are stored as rules that can be applied to multiple vulnerabilities and projects. 

Although the manual effort required may seem daunting, we found that in fact many of the missing resources are shared by many vulnerabilities and projects, so that fixing a relatively small number of resources resolves a large number of issues. Our current dataset includes fixes for 66 missing resources identified from the past 8 years of vulnerabilities; thus, in the worst case, keeping ARVO’s fixes updated would only require updating about 8 records per year. This is a manageable amount of work, particularly given the benefits to reproducibility: applying these fixes allowed us to successfully reproduce an additional 1,568 vulnerabilities. 

### **4.4 Fix Locator** 

Pinpointing the patch that fixes a given vulnerability enables many different downstream uses of the vulnerability dataset, such as research into how developers fix vulnerabilities, benchmarking of localization and repair systems, etc. In this section we present ARVO’s fix locator and how it addresses limitations in OSS-Fuzz’s fix verification process. 

_OSS-Fuzz._ OSS-Fuzz builds each project once per day, and, if a crash is detected, it reports the issue to the project developers. The developers then identify the root cause and commit a fix for the issue, which can be time-consuming (vulnerabilities in our dataset averaged 68.89 days between the initial report and the fix). When OSS-Fuzz performs its daily build, it checks whether the most recent version at that time crashes on the triggering input; if it does not, the issue is marked as fixed. Particularly for highly active projects, the delay between the developers’ fix and OSS-Fuzz’s verification results in a range of possible candidate commits for the actual patch. Figure 4 illustrates the process through a concrete example: the vulnerability is first identified by OSS-Fuzz at 6f6caf; the developers commit a fix the next day at aa668b; finally, OSSFuzz verifies the fix at aa668b. Note that aa668b is not the actual fix, but rather a minor change to the ChangeLog file; to identify the actual fix, we must search over the 14 commits and 83 files that were changed between the initial report and the verification. 

|imagemagick|
|---|
|freetype2|
|libtiff|




![](docs/paper-research/md-downloaded-paper-professor/images/30-arvo-atlas-of-reproducible-vulnerabilities-for-open-source.pdf-0007-10.png)


**Figure 5: Revision Control on Locator.** 

To compile the blue/purple revision of Imagemagick, revision control is applied to get corresponding revisions over dependencies. Only 2 of 14 dependencies are included in the graph to avoid verbose demonstration. 

_ARVO._ Although bisection is conceptually simple, it is difficult to implement in practice due the difficulty of recompiling the project at each commit. ARVO’s fix locator also benefits from the techniques used for vulnerability reproduction: because we can precisely control dependency versions and account for missing resources, we can recompile the project not just at its vulnerable version, but also at other commits around the same time. This allows us to perform bisection on the range provided by OSS-Fuzz to locate the true fix. ARVO identified precise patches on the commit level for vulnerabilities in 88.5% of the reproducible cases from the reproducer. We believe these developer-written patches for vulnerabilities may also be of interest in their own right for future research such as work on vulnerability repair. 

As with reproducing the initial vulnerability, precise revision control for dependencies is crucial during bisection, because we cannot tell if a particular commit is before or after the fix was implemented unless we can build the project and run it on the triggering input. This means that as ARVO visits each commit during bisection, we must also identify the corresponding commit for each dependency to ensure that the build is compatible. Unlike the reproducer, the fix locator cannot rely on the dependency versions from srcmap.json, and so we instead use timestamps to find the appropriate commit. 

Figure 5 shows how revision control is applied for the Imagemagick issue previously discussed. For each revision of the main component, we used the timestamp to find the most recent version of the dependency at that time, improving the reliability of the build process. 

### **4.5 Database Access** 

A goal of our dataset is that it should be easy to use, even for researchers who do not have a security background; we hope that this will allow researchers in other fields (e.g., machine learning) to use it as an evaluation target. Based on ARVO, we have uploaded docker images for each vulnerability to Docker Hub, allowing each issue to be reproduced and recompiled with a single command: docker run n132/arvo:<localId>-<vul|fix> arvo [compile]. 

To support more advanced uses of the dataset (e.g., rebuilding the project with other instrumentation), we make ARVO itself opensource so researchers can rebuild the ARVO dataset from scratch with their desired changes. 

7 

Xiang Mei, Pulkit Singh Singaria, Jordi Del Castillo, Haoran Xi, Abdelouahab (Habs) Benchikh, Tiffany Bao, Ruoyu Wang, Yan Shoshitaishvili, Adam Doupé, Hammond Pearce, Conference’17, July 2017, Washington, DC, USA and Brendan Dolan-Gavitt 


![](docs/paper-research/md-downloaded-paper-professor/images/30-arvo-atlas-of-reproducible-vulnerabilities-for-open-source.pdf-0008-01.png)


<!-- Start of picture text -->
Vulnerabilities Over Time<br>All Vulnerabilities<br>7500<br>Reproducible<br>5000 Fix Located<br>2500<br>0<br>Timestamp<br>Reproduction and Fix Location Success by Month<br>60<br>40<br>20 Reproduced<br>Fix Located<br>0<br>0 20 40 60 80<br>Month (Since Aug 2016)<br>2016 2017 2018 2019 2020 2021 2022 2023 2024<br># Vulnerabilities<br>Success Rate (%)<br><!-- End of picture text -->

**Figure 6: Database growth over time.** 

### **5 DATASET** 

This section presents the details of the ARVO dataset constructed using the methods described in Section 4. 

### **5.1 Dataset Characteristics** 

_Dataset Size and Growth._ At the time of this writing, out of 8,934 vulnerabilities initially obtained from OSS-Fuzz, ARVO reproduced 5,651 vulnerabilities across 273 projects. From these, we could precisely locate the associated fix for 5,001 vulnerabilities. 

Figure 6 shows how these values grew over time against the proportion of OSS-Fuzz vulnerabilities that we could reproduce and fix. As can be seen, ARVO maintains a roughly constant rate of reproduction for cases after 2017. This means our mitigations for the missing resource challenge (discussed in Section 3.2) works. 

Prior to 2017 the OSS-Fuzz infrastructure changed more frequently. We hypothesize that this is why we have a lower success rate for those months, as we focus on a more generic approach suitable for the current OSS-Fuzz. 

The growth of the ARVO dataset over time is continuous as OSSFuzz also grows in popularity, includes more projects, and findes more bugs. As we leverage their success, ARVO is likewise suitable for scaling into the future—OSS-Fuzz’s continued fuzzing will keep the ARVO dataset growing and up-to-date. 

_Project and Language Distribution._ Table 2 shows the distribution of vulnerabilities among projects. This distribution is relatively even; the project with the most vulnerabilities represents 7.36% of the dataset, and the top 10 projects collectively account for only 31.13%. This indicates the comprehensive nature of the ARVO dataset: It does not contain a small number of projects, but instead a wide range of different C/C++ applications. 

_Patch Statistics._ Of the 5,001 vulnerabilities in the ARVO dataset for which we were able to identify the precise commit fixing the vulnerability, we first filter out duplicates (which can occur when a single patch fixes multiple vulnerabilities—this occurred in 1,246 

**Table 2: Project Distribution in ARVO.** 

|**Project**|**# Vulnerabilities**|**% of Dataset**|
|---|---|---|
|imagemagick|368|7.36|
|harfbuzz|147|2.94|
|binutils|146|2.92|
|ndpi|146|2.92|
|skia|143|2.86|
|ghostscript|136|2.72|
|fmpeg|129|2.58|
|opensc|121|2.42|
|gdal|111|2.22|
|graphicsmagick|110|2.22|
|Other Projects|3444|68.87|



cases) and then remove merge commits (as these contain many changes unrelated to the vulnerability—264 cases). The filtered set contains 3,491 patches. 

The large size of this dataset allows us to collect some interesting statistics on the nature of vulnerability patches. Prior research has found that security-related fixes are typically small and selfcontained [18]. Our data also supports this finding: In ARVO dataset we find that the average patch fixing a vulnerability affects 2.53 files (mean: 2.53, median: 1, std: 9.56); 2,216 patches (63.5%) affect just a single file. Looking at the number of lines added and removed by each patch, we find a median of 6 lines added and 2 lines removed; the means of both are significantly larger (131.0 added and 79.8 removed) due to a small number of outliers. 90% of the patches in our dataset have fewer than 60 lines added or removed. 

### **5.2 Dataset Comparison** 

Table 3 presents the ARVO dataset against several other state-ofthe-art bug databases. From this, we can see that ARVO dataset is the _only_ dataset to achieve reproducibility on a large scale— indeed, we believe ARVO is unique in its combination of size and bug reproducability. We have found no other public dataset which achieves bug incident and patch reproducibility with complete support for project recompilation for all bug cases at the scale we provide. Primarily this is because while small datasets can achieve reproducability through manual effort, this does not scale to larger datasets. This is seen, for instance, in the CGC dataset’s reproducible bugs, however the CGC dataset’s scale and custom setup (using DARPA’s custom DECREE operating system) limits its usage. 

Meanwhile, the ability to automatically update the dataset as its upstream data source reports new vulnerabilities (a feature shared with CVEFixes [2] and OSS-Fuzz-Vulns) means that ARVO will continue to grow over time, preventing any downstream users of the dataset from ‘overfitting’ to historical data. Moreover, larger datasets typically prioritize quantity over quality, which can compromise their utility. This is particularly critical in binary analysis, where despite the abundance of resources associated with each vulnerability, substantial effort is required to reproduce them. By providing the assets for reproducability directly, ARVO will substantially reduce this workload. 

8 

Conference’17, July 2017, Washington, DC, USA 

ARVO: Atlas of Reproducible Vulnerabilities for Open Source Software 

**Table 3: Comparison of ARVO with related datasets.** 

|**Dataset**|**# Vulns**|**# Projects**|**PoC**|**Automated**|**Reproducible**|**Patches**|**Real-World**|
|---|---|---|---|---|---|---|---|
|ExtractFix [10]|30|7|✗|✗|✗|✓|✓|
|CGC|276|249|✓|✗|✓|✓|✗|
|OSS-Fuzz-Vulns (OSV)|3,290|298|✓|✓|✗|✓|✓|
|Big-Vul [9]|3,754|348|✗|✗|✗|✗|✓|
|CVEFixes [2]|5,495|1,754|✗|✓|✗|✓|✓|
|ARVO|5,001|273|✓|✓|✓|✓|✓|



**Table 4: Cases where ARVO and OSV disagree on fix commits.** 

**Table 5: Cases where ARVO and OSV agree on fix commits.** 

|**Category**|**Number of Cases**|
|---|---|
|ARVO was correct|56|
|OSV was correct|15|
|Neither were correct|18|
|More in-depth analysis required|11|



|**Category**|**Number of Cases**|
|---|---|
|Patch manuallyverifed|48|
|Patch verifed bydevelopers|36|
|Total successfulpatches|84|
|Falsepatches|12|
|More in-depth analysis required|4|



### **5.3 Comparison between OSS-Fuzz-Vulns and ARVO** 

From a pure size-based perspective, the ARVO dataset consists of a database comprising 5,001 successfully identified patches for vulnerabilities compared to OSV’s OSS-Fuzz-Vulns subset at documented fixes for 3,280 cases. ARVO also provides information for reproducibility; OSV does not. However, only 1,906 bug cases actually overlap between ARVO and OSV. To evaluate the quality of the located patches, we first split the common cases (1906) between ARVO and OSV into two groups: agree (86%) and disagree (14%) cases. We then manually verified 100 cases from each group. In agree cases, 84% were confirmed as true positives, while 56% of ARVO’s results were true positives in disagree cases (OSV had only 15% true positives in disagree cases). Therefore, ARVO’s overall success rate of locating patches is more than 80%. 

In this comparison, we examined these overlapped cases to explore if the ARVO locates the patching commit correctly. This was broadly the case, but in total there were 270 cases for which ARVO and OSV disagreed on the fix commit. We randomly selected 100 cases and analyzed them manually to compare the results and present the results in Table 4. We found that there were four distinct categories of outcomes: firstly, cases where OSV provided correct results; secondly, cases where ARVO provided the correct results; thirdly, instances where neither OSV nor ARVO gave correct results (the bug patch was misidentified by both); and lastly, complex patches which require additional in-depth analysis to ascertain which patch fixes the bug more effectively. Another observation during this analysis was the identification of instances where the patches from OSV and ARVO were identical, with one being a merge commit having the other as its parent. In such cases, we deemed the original commit (parent commit) as the more accurate, given that merge commits typically consists of a large number of hunks with some not directly related to the fix. 

We also explored the 1,636 cases in which ARVO and OSV identified the same commit for the bug fixes. Here, we again randomly 

selected 100 cases to analyze their results (shown in Table 5). For the remaining 1,636 cases for which ARVO and OSV identified the same commit for the bug fixes, we randomly selected 100 cases to analyze their results. We found that there were three different categories of cases. Firstly, there is a distinction between cases where the commit message explicitly references the corresponding OSS-Fuzz issue (e.g., “Fix OSS-Fuzz issue 20493”), and no analysis is required; and cases where we had to manually analyze the patch and figure out if this patch fixes the bug or does it avoid the crash. Secondly, there is a distinction between patches which fix the bug and patches which do not actually address the bug at all, instead modifying files which do not affect the bug (e.g., Makefile, build.sh). These patches do not address the root cause of the bug and the bug may still be exploitable by attackers. Lastly, there were 4 cases where it was difficult to tell if the patch fixed the bug or not without doing a more in-depth analysis. 

Table 5 provides the best estimate of ARVO’s patch localisation accuracy at approximately 84%, and Table 4 provides a lower bound at approximately 56%. Still, this lower bound comes from the lessfrequent bugs where OSV and ARVO disagreed—i.e. these are the rarer, more complex cases. 

We now explore three interesting cases in more detail: _Issue 35566_ is an unknown address crash in Qt5 as reported by libfuzzer. Comparing ARVO’s fix commit with OSV’s provides a challenge. We found that ARVO’s fix commit was from the Qt5 project, but OSV’s was in qtbase project. In fact, Qtbase is a dependency of Qt5 and is a submodule in Qt5 repository. 

ARVO’s fix commit involved a submodule update to update all of Qt5’s submodules. In contrast, OSV’s fix commit correctly fixes the bug, which identified that the actual bug was not in Qt5 but in Qtbase. The fuzzer discovered an input that triggered a crash within Qtbase instead of Qt5. Because the way ARVO’s fix locator works, it identified submodule commit as the fix, because the submodule update commit also updates Qtbase from a vulnerable version to a fixed version, thus preventing the crash. 

9 

Xiang Mei, Pulkit Singh Singaria, Jordi Del Castillo, Haoran Xi, Abdelouahab (Habs) Benchikh, Tiffany Bao, Ruoyu Wang, Yan Shoshitaishvili, Adam Doupé, Hammond Pearce, Conference’17, July 2017, Washington, DC, USA and Brendan Dolan-Gavitt 


![](docs/paper-research/md-downloaded-paper-professor/images/30-arvo-atlas-of-reproducible-vulnerabilities-for-open-source.pdf-0010-01.png)


<!-- Start of picture text -->
master branch stable branch<br>Merge stable<br>Fix on master<br>Fix on stable<br>Bug found<br><!-- End of picture text -->

**Figure 7: Git Graph view of the fix commits in** **_Issue 23801_** 

This is a limitation of ARVO’s due to its reliance on the metadata from OSS-Fuzz. In this issue, OSS-Fuzz did not report that the crash happened in Qt5’s dependency rather than Qt5 itself—ergo, ARVO found the fix commit when the vulenrable dependency was updated to be the fixed version in Qt5. 

_Issue 23801_ is a double free bug in the mruby project. Upon reviewing the crash report and evaluating the fixes provided by OSV and ARVO, we noted that ARVO’s fix commit was implemented on the stable branch, whereas OSV’s fix commit occurred directly on the master branch where the bug was initially detected. Consequently, we contend that OSV’s fix is more suitable given that it addresses the vulnerability within the same branch in which it was discovered (the master branch). The stable branch, which was forked significantly prior to the discovery of the bug and later merged into master after an extended period, contains the ARVO fix. Given this timeline, the reliability of the fix implemented in the stable branch may be compromised. 

Figure 7 depicts the state of the mruby project when this bug was discovered and when it was fixed in the master and stable branches independently. The reason why ARVO found the fix on a different branch is because to perform the search it gets the range of commits using timestamps—however this method will also include commits from other branches. We did this to improve our chances of finding smaller and accurate patches, but this can lead to issues such as this, where ARVO found a patch which is on a different branch than the branch where the bug was discovered. 

_Issue 26952_ is also a double free bug detected by libFuzzer but in the wireshark project. After evaluating fixes provided by OSV and ARVO, we found that OSV’s fix commit is unrelated to the bug. We use the crash report to decide if the patch modifies a file or a function related to the crash. In this case OSV’s fix modifies the packet-nas_5gs.c but this file is not mentioned in the crash report. The crash report suggests that the object which was doublefree’d was allocated in dissect_rtps function of packet-rtps.c. OSV’s fix commit (561c560) has 324 additions and 24 deletions in a file which is unrelated to the bug. ARVO’s fix commit (29f2177), on the other hand, is very precise and contains only 1 addition and 2 deletions and is very relevant to the bug—being the function mentioned in the crash report. Figure 8 shows ARVO’s patch. 

--- a/epan/dissectors/packet-rtps.c 

+++ b/epan/dissectors/packet-rtps.c 

- **@@ -10544,8 +10544,7 @@ static gboolean dissect_rtps** * its changes. 

- */ 

- if (pinfo->private_table == NULL && pinfo->ptype == PT_TCP) { 

- pinfo->private_table = g_hash_table_new_full(g_str_hash, g_str_equal, 

- - g_free, g_free); 

- + pinfo->private_table = g_hash_table_new(g_str_hash, g_str_equal); ... 

#### **Figure 8: ARVO’s fix for 26952** 

### **6 CASE STUDIES** 

This section presents two case studies showing how ARVO can be used for research purposes. The first explores an application of Large Language Models (LLMs) for bug repair, and the second discusses how we found hundreds of current zero-day bugs from OSS-Fuzz’s bug reporting. 

### **6.1 Evaluation of LLMs for Bug Repair** 

Recent research has found that large language models (LLMs) may be effective at automatically repairing security vulnerabilities. However, existing work has only evaluated LLMs’ capabilities at this task on a handful of vulnerabilities (e.g., Pearce et al. [21] used a subset of the ExtractFix dataset containing just 12 CVEs). In this case study, we demonstrate ARVO’s potential for conducting much more extensive evaluations of vulnerability repair. 

We evaluate GPT-3.5 and GPT-4<sup>6</sup> on ARVO’s dataset. Because it is costly to operate the LLMs we evaluate their bug-fixing performance over 100 randomly-selected vulnerabilities, and because LLMs are currently limited in the size of the inputs they can handle we ensure these vulnerabilities have an official patch consisting of a single hunk (i.e. it changes only one location in the code). Similar to other work in vulnerability repair, we also assume the existence of a “localization oracle” that identifies the correct function to patch, and then prompt the model to rewrite the function to fix the vulnerability. 

The prompt provided to the LLM includes the source code of the whole vulnerable function and the sanitizer report for the corresponding vulnerability. In the crash sanitizer report, the crash type (e.g., heap buffer overflow) is provided. 

To validate the patches we use ARVO to first validate the project and dependencies for each issue, then apply the LLM-generated fix to the code before (re-)building the project. If the build succeeds, we then use the triggering input to test if the repair was successful. For this evaluation, we do not attempt to validate that the patched version keeps the functionality of the program intact (which would 

6 Specifically, gpt-3.5-turbo-1106 and gpt-4-1106-preview. 

**Table 6: LLMs Repair Evaluation** 

|**Results**|**GPT-3.5-Turbo**|**GPT-4-Turbo**|
|---|---|---|
|No Crash|13|20|
|Crash|32|38|
|Compile Failed|33|27|
|Too Long|22|15|



10 

Conference’17, July 2017, Washington, DC, USA 

ARVO: Atlas of Reproducible Vulnerabilities for Open Source Software 

--- a/src/lib/protocols/ori.c +++ b/src/lib/protocols/correct.c 

**@@ -115,12 +115,12 @@ static int thrift_validate_type** { if (thrift_validate_method(method, method_length) == 0) { ndpi_set_risk ...; flow->protos.thrift.method[0] = '\0'; 

} else { - strncpy(flow->protos.thrift.method, method, method_length); + strncpy(flow->protos.thrift.method, method, + ndpi_min(sizeof(flow->protos.thrift.method), method_length)); } } --- a/src/lib/protocols/ori.c +++ b/src/lib/protocols/gpt_fix.c **@@ -1,12 +1,14 @@ static int thrift_validate_type** { - if (thrift_validate_method(method, method_length) == 0) { + if (method_length >= sizeof(flow->protos.thrift.method)) { ndpi_set_risk ...; flow->protos.thrift.method[0] = '\0'; } else { strncpy(flow->protos.thrift.method, method, method_length); + flow->protos.thrift.method[method_length] = '\0'; } } 

#### **Figure 9: Correct Fix and GPT Fix** 

require, at minimum, the ability to run the project’s test suite, a feature ARVO currently lacks), nor do we verify that the patch fixes the root cause of the vulnerability (rather than simply preventing the test case from triggering); we leave a more thorough evaluation to future work. 

The results, shown in Table 6, indicate that GPT-4-Turbo generally produces better patches than GPT-3.5-Turbo (unsurprising given that GPT-4 is OpenAI’s flagship model). In the table, “No Crash” means the patched version no longer crashed on the PoC input, and “Crash” indicates the patched version was still vulnerable. “Compile Failed” denotes cases where the LLM-generated code did not compile, usually because the LLM attempted to call nonexistent functions. Finally, we found 37 cases where the provided repair prompt was too large to fit in the model’s context limit (“Too Long”). 

Among the apparently-successful repairs, we did find that there are cases that merely avoid the crash rather than fixing the bug. Figure 9, which depicts the official patch and the patch generated by GPT-3.5 on a heap buffer overflow, depicts one such case. As the modifications show, the developer fix performs a length check to fix the heap buffer overflow, while the LLM patch modifies an if statement. While the latter fix does prevent the PoC input from triggering the vulnerability, it also breaks the functionality of the original code. This case demonstrates the need for careful examination of apparent “fixes” when evaluating repair systems, echoing prior results in the program repair literature [23]. 

### **6.2 False Positives and Zero-day Bugs in OSS-Fuzz** 

After obtaining all source data from OSS-Fuzz, we were able to improve the original reproducing success rate from 13% to 63%. For the 37% cases that we failed to reproduce, 46.6% were due to two similar issues: "vulnerability can’t be reproduced" and "the fixed version still crashes". We investigated these cases and found that 57% of 

these cases were not our fault but rather OSS-Fuzz’s false positives, including non-reproducible crashes and non-verifiable fixes. Then, we confirmed these false positives on OSS-Fuzz, which resulted in not only polluted reports but leaked zero-day vulnerabilities. 

Given our pursuit of bug reproducibility, during the development of ARVO, we continuously and systematically analyzed cases where we were unable to reproduce bugs reported by OSS-Fuzz. In total, we found 46.6% of non-reproducible cases were due to either a failure to reproduce the intended crash or a failure to verify that the patch was correct. These mean that ARVO could successfully compile the intended version of the software, however, the PoCs given from OSS-Fuzz are not able to trigger the expected behaviors (i.e. crash/not crash). After investigating this further, we found there are large numbers of both false bugs and false patches found on OSS-Fuzz. The latter is particularly concerning because OSS-Fuzz automatically opens issues to the public once they are detected as fixed—these can be considered zero-day bugs, accompanied by triggering inputs, that attackers could use to develop working exploits. 

We first considered other potential causes, such as errors with the version control, but could not identify any reason other than errors in OSS-Fuzz’s provided metadata. In order to rule out issues with our own build environment, we downloaded the compiled binary OSS-Fuzz used to “verify” the fix; Google makes these artifacts publicly available via Google Cloud Storage. 

Concerningly, after downloading the OSS-Fuzz binaries and verifying these cases with their PoCs, out of the 1000 cases in which ARVO failed to verify the fixed version we found that **572 of these binaries were still crashing with the corresponding PoC** . 

Further investigation found that these cases fell into one of three categories: _(1) Zero-day Vulnerability:_ The vulnerability is present in the latest version, with a report on OSS-Fuzz labeling it as fixed. This potentially exposes information about unfixed vulnerabilities and how to trigger them to attackers. 

_(2) Broken OSS-Fuzz Vulnerability Reports:_ The bug is fixed correctly by the developers, but on a later commit than the one identified by OSS-Fuzz. These cases are less harmful, but are a source of noise when attempting to draw conclusions about vulnerability patches based on OSS-Fuzz data. 

_(3) Hidden Vulnerability:_ The bug is hidden because the code changes. Since OSS-Fuzz wrongly informs the project developers that the vulnerabilities were fixed, developers may not deeply investigate into the original crash to fix the vulnerability. After enough code changes, the original PoC may no longer trigger the vulnerability because of data/control flow changes. 

Of these options, the potential for zero-day vulnerabilities is the most concerning. Although we found them in the process of building the ARVO dataset, simpler techniques for extraction may also work—e.g., by collecting all PoCs on OSS-Fuzz and running them on the latest version software. 

For the other cases where the crash cannot be reproduced with the latest version of the software, we can leverage ARVO’s capability for project reproduction to perform a binary search between the commit when the crash is found to the latest commit. Because some commits may fail compilation (the bisection search could be downgraded to linear search) and given limited computational resources, we performed bisection with up to 10 linear steps from 

11 

Xiang Mei, Pulkit Singh Singaria, Jordi Del Castillo, Haoran Xi, Abdelouahab (Habs) Benchikh, Tiffany Bao, Ruoyu Wang, Yan Shoshitaishvili, Adam Doupé, Hammond Pearce, Conference’17, July 2017, Washington, DC, USA and Brendan Dolan-Gavitt 

a commit that fails to compile, which avoids spending too much time on one case. In this experiment, we automatically found 128 commits that stopped the crash over 297 false positives. Most of them are correct patches since these bugs were later rediscovered by OSS-Fuzz, letting project developers notice and fix them. 

_Examples:_ The open issue 25267<sup>7</sup> on OSS-Fuzz was claimed fixed. However, the OSS-Fuzz points to a commit<sup>8</sup> which modified a README file as the ‘fix’ of the heap buffer overflow vulnerability (obviously wrong). With ARVO, we located a potential patch<sup>9</sup> , which was applied two years later after the bug was found. In this patch 9, the commit message indicates that the patch fixes a wrong size passed to memcpy. According to the crash call stack we reproduced, the modified function is marked as the function that allocated the overflowed heap chunk. Furthermore, based on the deduplication feature supported on ARVO, we found that issue 39373 shares the same fix. Despite different fuzz engines (honggfuzz and afl) being applied, the crash reports are quite similar. Therefore, open issue 25267 was actually a leaked zero-day vulnerability for around **2 years** , with a report on OSS-Fuzz pointing the attackers to the PoC. 

_Disclosure:_ We reported **more than 300** of these potential leaked zero-day bug cases to OSS-Fuzz, and further responsible disclosure for the existing bugs is being processed. Thanks to the reliable reproducibility features of ARVO, these mistaken patch reports in OSS-Fuzz were caught. 

### **7 DISCUSSION** 

A key benefit of the idea behind ARVO is that it can be generally applicable to any upstream source data of vulnerabilities in a software system. While ARVO is targeted to OSS-Fuzz hosted projects, we believe that other vulnerability identification systems—including those run on closed-source software systems—can use the ideas and insights of ARVO to create research vulnerability datasets. 

One of the key challenging aspects when building ARVO that we faced was the lack of context captured by the upstream source data (discussed in Section 4.2). When OSS-Fuzz identifies a vulnerability, they capture the binary, however the _entire build environment_ is not captured. This lack of environment capture is why ARVO required the reproducer. While ARVO can continue to collect data, we believe that upstream data sources can benefit the entire ecosystem by capturing this context, which would greatly improve the ease of dataset creation. 

In a similar vein, it is clear that the open-source software ecosystem does not focus on long-term recompilability of specific software versions. While ARVO is able to build on the structure implemented by OSS-Fuzz, there are still significant challenges that remain. Clearly there is not enough structure and support to develop open-source software that can repeatably compile into the future. Perhaps a long-term goal would be improvements in the open-source ecosystem to help developers create reproducible and recompilable builds and combat bitrot. 

### **7.1 Limitations** 

Even though ARVO demonstrated significant improvement over prior datasets, the methodology does face certain limitations. 

_Source-Dependent._ ARVO takes sources from upstream datasets and trusts the metadata. Even though ARVO can detect some issues, broken metadata from the upstream dataset may lead to false positives. For example, there are cases when the vulnerability is in a project’s dependency, but the metadata implies the main component is vulnerable. 

_PoC-based Reproduction._ While reproducing vulnerabilities, we did not perform strict matches on the crash type and address, potentially affecting the accuracy of the ARVO dataset (i.e., it is possible that the crash we reproduce differs from the original vulnerability, despite sharing the same triggering input). Additional measurements could be used to improve the data quality. 

_Patch Quality._ ARVO’s reliance on bisection for identifying vulnerability fixes has limitations. Due to the possibility of multiple related commits, this approach might not always accurately pinpoint the exact fix, particularly when fixes involve a series of modifications. Also, while a commit may lead us to a presumed fix, an individual commit might encompass extensive modifications, complicating the identification of the precise change responsible for the fix. 

Another concern is our omission of functionality checks on the implemented fixes. Our observations suggest that most fixes, while mitigating the PoC vulnerability trigger, may not be functionally optimal—or might simply remove the vulnerable code block without addressing the underlying root cause of the vulnerability. 

_Duplicated Cases._ The ARVO dataset can include duplicated bugs from OSS-Fuzz, where OSS-Fuzz has reported two (or more) vulnerabilities that share a single underlying root cause. As these duplicate cases will trigger the bug from different paths (using different PoCs), to test the robustness of a patch we mark them instead of filtering them out. It is also not precise to check duplicated cases by a commit-level patching comparison if a single commit patches multiple bugs. In future work we hope to use ARVO to precisely detect duplicate bugs reported from OSS-Fuzz; assuming that we can identify patches for each issue that are precise and minimal (changing only what is necessary to fix the issue), then two bugs can be considered the same if the patch that fixes them is identical. 

_Time Consuming._ Even though we prepared all docker images, reproducing bugs via re-compiling projects is time-consuming. Even though there are only a few commands to run, re-building the ARVO dataset from scratch may take weeks for end-users depending on compute resources. Further, when patch locating, because certain ‘bad’ commits fail compilation, the bisection could be downgraded to linear search which is also time-consuming. We note, however, that this computational cost can be avoided for issues ARVO has already reproduced, because we make the resulting container images (which contain the build artifacts) publicly available. 

### **8 FUTURE WORK** 

> 7https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=25267 

> 8https://github.com/strukturag/libheif/commit/5f948947733b 

> 9https://github.com/strukturag/libheif/commit/11ffeffadd98 

We intend for ARVO to be a framework and dataset which continues to grow over time—at the very least via OSS-Fuzz reports which the system continues to ingest and process. We also hope to add 

12 

Conference’17, July 2017, Washington, DC, USA 

ARVO: Atlas of Reproducible Vulnerabilities for Open Source Software 

more sources, such as Linux Kernel vulnerabilities, as upstream data sources. 

Based on our original purpose, our future focus will include enhancing the reliability and automation of our compiling processes as well as facilitating the use of ARVO in further security research. 

In pursuit of these goals we also aim to improve the success rate of locating and reproducing vulnerabilities. A higher success rate would not only expand our database but also accelerate its growth, which is crucial for security research. More precise revision control could be implemented to expand the dataset. 

We plan to refine our methodologies as an open-source project. 

### **9 CONCLUSION** 

In this paper, we present ARVO—an Atlas of Reproducible Vulnerabilities in Open source software, established as a scalable and accessible benchmarking tool for binary security unique in its reproducibility. This paper outlines our approach for transforming document-centric vulnerability reports into a database of interactive and reproducible environments. Additionally, we identified and solved numerous challenges associated with building and reproducing historical vulnerabilities, despite the “bit rot” of their associated dependencies, resources, and toolchains. 

We justify the utility of ARVO through two case studies, one as a brief examination of LLMs for real-world vulnerability repair (showing that GPT-4 can ‘fix’ more issues than GPT-3.5-Turbo and 20% of issues overall), and the second which examined the reliability of OSS-Fuzz reports. This exploration yielded a startling discovery of over 300 active vulnerabilities in open-source projects previously identified by OSS-Fuzz but inaccurately flagged as fixed. 

Our dataset of reproducible vulnerabilities and the framework behind it are open-source, contain more than 5,000 vulnerabilities across 273 projects on more than 10,000 interactive build images on Dockerhub. We believe it is the most comprehensive offering to date in this area, especially as the framework has the facilities to add new vulnerabilities and projects automatically in the future. 

### **REFERENCES** 

- [1] Gautam Altekar, Ilya Bagrak, Paul Burstein, and Andrew Schultz. 2005. OPUS: Online Patches and Updates for Security. In _14th USENIX Security Symposium (USENIX Security 05)_ . USENIX Association, Baltimore, MD. https://www.usenix.org/conference/14th-usenix-security-symposium/ opus-online-patches-and-updates-security 

- [2] Guru Bhandari, Amara Naseer, and Leon Moonen. 2021. CVEfixes: automated collection of vulnerabilities and their fixes from open-source software. In _Proceedings of the 17th International Conference on Predictive Models and Data Analytics in Software Engineering (PROMISE 2021)_ . Association for Computing Machinery, New York, NY, USA, 30–39. https://doi.org/10.1145/3475960.3475985 

- [3] Marcel Böhme, Van-Thuan Pham, Manh-Dung Nguyen, and Abhik Roychoudhury. 2017. Directed Greybox Fuzzing. In _Proceedings of the 2017 ACM SIGSAC Conference on Computer and Communications Security (CCS)_ . 

- [4] Oliver Chang and Russ Cox. 2024. Open Source Vulnerability format. https: //ossf.github.io/osv-schema/. 

- [5] Yue Chen, Yulong Zhang, Zhi Wang, Liangzhao Xia, Chenfu Bao, and Tao Wei. 2017. Adaptive Android Kernel Live Patching. In _26th USENIX Security Symposium (USENIX Security 17)_ . USENIX Association, Vancouver, BC, 1253–1270. https://www.usenix.org/conference/usenixsecurity17/technicalsessions/presentation/chen 

- [6] CISA. 2023. CISA Open Source Software Security Roadmap. https://www.cisa. gov/resources-tools/resources/cisa-open-source-software-security-roadmap. 

- [7] Jiarun Dai, Yuan Zhang, Zheyue Jiang, Yingtian Zhou, Junyan Chen, Xinyu Xing, Xiaohan Zhang, Xin Tan, Min Yang, and Zhemin Yang. 2020. BScout: Direct Whole Patch Presence Test for Java Executables. In _29th USENIX Security Symposium (USENIX Security 20)_ . USENIX Association, 1147–1164. https://www. usenix.org/conference/usenixsecurity20/presentation/dai 

- [8] Kyle Daigle. 2023. Octoverse: The state of open source and rise of AI in 2023. https://github.blog/2023-11-08-the-state-of-open-source-and-ai/. 

- [9] Jiahao Fan, Yi Li, Shaohua Wang, and Tien N. Nguyen. 2020. A C/C++ Code Vulnerability Dataset with Code Changes and CVE Summaries. In _Proceedings of the 17th International Conference on Mining Software Repositories (MSR ’20)_ . Association for Computing Machinery, New York, NY, USA, 508–512. https: //doi.org/10.1145/3379597.3387501 

- [10] Xiang Gao, Bo Wang, Gregory J. Duck, Ruyi Ji, Yingfei Xiong, and Abhik Roychoudhury. 2021. Beyond Tests: Program Vulnerability Repair via Crash Constraint Extraction. _ACM Transactions on Software Engineering and Methodology_ 30, 2 (March 2021), 1–27. https://doi.org/10.1145/3418461 

- [11] Google. 2024. AddressSanitizer. https://github.com/google/sanitizers/wiki/ AddressSanitizer. 

- [12] Google. 2024. oss-fuzz-vulns. https://github.com/google/oss-fuzz-vulns/. 

- [13] Google. 2024. osv.dev. https://osv.dev/. 

- [14] Claire Le Goues, Michael Pradel, and Abhik Roychoudhury. 2019. Automated program repair. _Commun. ACM_ 62, 12 (2019), 56–65. 

- [15] Zheyue Jiang, Yuan Zhang, Jun Xu, Qi Wen, Zhenghe Wang, Xiaohan Zhang, Xinyu Xing, Min Yang, and Zhemin Yang. 2020. PDiff: Semantic-based Patch Presence Testing for Downstream Kernels. In _Proceedings of the 2020 ACM SIGSAC Conference on Computer and Communications Security_ (Virtual Event, USA) _(CCS ’20)_ . Association for Computing Machinery, New York, NY, USA, 1149–1163. https://doi.org/10.1145/3372297.3417240 

- [16] George Klees, Andrew Ruef, Benji Cooper, Shiyi Wei, and Michael Hicks. 2018. Evaluating fuzz testing. In _Proceedings of the 2018 ACM SIGSAC conference on computer and communications security_ . 2123–2138. 

- [17] Claire Le Goues, ThanhVu Nguyen, Stephanie Forrest, and Westley Weimer. 2012. GenProg: A Generic Method for Automatic Software Repair. _IEEE Transactions on Software Engineering_ 38, 1 (Jan. 2012), 54–72. https://doi.org/10.1109/TSE. 2011.104 

- [18] Frank Li and Vern Paxson. 2017. A Large-Scale Empirical Study of Security Patches. In _Proceedings of the 2017 ACM SIGSAC Conference on Computer and Communications Security (CCS ’17)_ . Association for Computing Machinery, New York, NY, USA, 2201–2215. https://doi.org/10.1145/3133956.3134072 

- [19] Barton P. Miller, Lars Fredriksen, and Bryan So. 1990. An empirical study of the reliability of UNIX utilities. _Commun. ACM_ 33, 12 (Dec. 1990), 32–44. https: //doi.org/10.1145/96267.96279 

- [20] Dongliang Mu, Alejandro Cuevas, Limin Yang, Hang Hu, Xinyu Xing, Bing Mao, and Gang Wang. 2018. Understanding the Reproducibility of Crowd-reported Security Vulnerabilities. In _27th USENIX Security Symposium (USENIX Security 18)_ . USENIX Association, Baltimore, MD, 919–936. https://www.usenix.org/ conference/usenixsecurity18/presentation/mu 

- [21] Hammond Pearce, Benjamin Tan, Baleegh Ahmad, Ramesh Karri, and Brendan Dolan-Gavitt. 2023. Examining Zero-Shot Vulnerability Repair with Large Language Models. In _2023 IEEE Symposium on Security and Privacy (SP)_ . 2339–2356. https://doi.org/10.1109/SP46215.2023.10179324 ISSN: 2375-1207. 

- [22] Henning Perl, Sergej Dechand, Matthew Smith, Daniel Arp, Fabian Yamaguchi, Konrad Rieck, Sascha Fahl, and Yasemin Acar. 2015. VCCFinder: Finding Potential Vulnerabilities in Open-Source Projects to Assist Code Audits. In _Proceedings of the 22nd ACM SIGSAC Conference on Computer and Communications Security_ (Denver, Colorado, USA) _(CCS ’15)_ . Association for Computing Machinery, New York, NY, USA, 426–437. https://doi.org/10.1145/2810103.2813604 

- [23] Zichao Qi, Fan Long, Sara Achour, and Martin Rinard. 2015. An analysis of patch plausibility and correctness for generate-and-validate patch generation systems. In _Proceedings of the 2015 International Symposium on Software Testing and Analysis_ . ACM, Baltimore MD USA, 24–36. https://doi.org/10.1145/2771783. 2771791 

- [24] Moritz Schloegel, Nils Bars, Nico Schiller, Lukas Bernhard, Tobias Scharnowski, Addison Crump, Arash Ale-Ebrahim, Nicolai Bissantz, Marius Muench, and Thorsten Holz. 2024. SoK: Prudent Evaluation Practices for Fuzzing. In _2024 IEEE Symposium on Security and Privacy (SP)_ . IEEE Computer Society, 137–137. 

- [25] Kostya Serebryany. 2017. OSS-Fuzz - Google’s continuous fuzzing service for open source software. USENIX Association, Vancouver, BC. https://www.usenix. org/conference/usenixsecurity17/technical-sessions/presentation/serebryany 

- [26] Ari Takanen, Jared D. Demott, Charles Miller, and Atte Kettunen. 2018. _Fuzzing for Software Security Testing and Quality Assurance, Second Edition_ . Artech House. Google-Books-ID: tKN5DwAAQBAJ. 

- [27] Xin Tan, Yuan Zhang, Chenyuan Mi, Jiajun Cao, Kun Sun, Yifan Lin, and Min Yang. 2021. Locating the Security Patches for Disclosed OSS Vulnerabilities with Vulnerability-Commit Correlation Ranking. In _Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security_ (Virtual Event, Republic of Korea) _(CCS ’21)_ . Association for Computing Machinery, New York, NY, USA, 3282–3299. https://doi.org/10.1145/3460120.3484593 

- [28] Michal Zalewski. 2013. AFL. https://lcamtuf.coredump.cx/afl/. 

- [29] Hang Zhang and Zhiyun Qian. 2018. Precise and Accurate Patch Presence Test for Binaries. In _27th USENIX Security Symposium (USENIX Security 18)_ . USENIX Association, Baltimore, MD, 887–902. https://www.usenix.org/conference/ usenixsecurity18/presentation/zhang-hang 

13 

Xiang Mei, Pulkit Singh Singaria, Jordi Del Castillo, Haoran Xi, Abdelouahab (Habs) Benchikh, Tiffany Bao, Ruoyu Wang, Yan Shoshitaishvili, Adam Doupé, Hammond Pearce, Conference’17, July 2017, Washington, DC, USA and Brendan Dolan-Gavitt 

### **APPENDIX A. LOCATED PATCH 25267** 

#### **Listing 1: Patch for Open Issue 25267** 

commit 11 ffeffadd980f9f96019fe180fc1e81827e3790 Author: Dirk Farin <dirk.farin@gmail.com > Date: Mon Apr 4 20:43:45 2022 +0200 fix wrong memcpy size diff --git a/libheif/heif_colorconversion.cc b/ libheif/heif_colorconversion.cc index 2b05068 ..5 a07ebb 100644 --- a/libheif/heif_colorconversion.cc +++ b/libheif/heif_colorconversion.cc @@ -526,7 +526 ,8 @@ Op_YCbCr_to_RGB <Pixel >:: convert_colorspace(const std::shared_ptr <const HeifPixel } if (has_alpha) { - memcpy (& out_a[y * out_a_stride], &in_a[y * in_a_stride], width * 2); + int copyWidth = (hdr ? width * 2 : width); + memcpy (& out_a[y * out_a_stride], &in_a[y * in_a_stride], copyWidth); } } 

14 

