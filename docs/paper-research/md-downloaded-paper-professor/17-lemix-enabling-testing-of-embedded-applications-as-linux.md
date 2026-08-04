# LEMIX **: Enabling Testing of Embedded Applications as Linux Applications** 

Sai Ritvik Tanksalkar _Purdue University_ 

Siddharth Muralee Srihari Danduri Paschal Amusuo _Purdue University Purdue University Purdue University_ James C Davis Aravind Kumar Machiry _Purdue University Purdue University_ 

Antonio Bianchi _Purdue University_ 

## **Abstract** 

Dynamic analysis, through rehosting, is an important capability for security assessment in embedded systems software. Existing rehosting techniques aim to provide high-fidelity execution by accurately emulating hardware and peripheral interactions. However, these techniques face challenges in adoption due to the increasing number of available peripherals and the complexities involved in designing emulation models for diverse hardware. Additionally, contrary to the prevailing belief that guides existing works, our analysis of reported bugs shows that high-fidelity execution is not required to expose most bugs in embedded software. Our key hypothesis is that security vulnerabilities are more likely to arise at higher abstraction levels. 

To substantiate our hypothesis, we introduce LEMIX, a framework enabling dynamic analysis of embedded applications by rehosting them as x86 Linux applications decoupled from hardware dependencies. Enabling embedded applications to run natively on Linux facilitates security analysis using available techniques and takes advantage of the powerful hardware available on the Linux platform for higher testing throughput. We develop various techniques to address the challenges involved in converting embedded applications to Linux applications. We evaluated LEMIX on 18 real-world embedded applications across four RTOSes and found 21 new bugs, in 12 of the applications and all 4 of the RTOS kernels. We report that LEMIX is superior to existing state-of-the-art techniques both in terms of code coverage ( _∼_ 2X more coverage) and bug detection (18 more bugs). 

## **1 Introduction** 

Society’s dependence on low-powered Microcontroller Unit (MCU) based devices ( _e.g.,_ IoT devices), has significantly increased, controlling various aspects of our daily lives, including homes [17], transportation [16], traffic management [90], and the distribution of vital resources like food [75] and power [72]. The adoption of these devices has seen rapid 

and extensive growth, with an estimated count of over 50 billion devices by the end of 2020 [15]. Vulnerabilities in the software controlling these devices have far-reaching consequences [18, 101] due to the pervasive and interconnected nature of these devices, as exemplified by the infamous Mirai botnet [66] and more recent URGENT/11 [11] vulnerabilities. It is important to detect such vulnerabilities proactively. Various works [102] show that dynamic analysis, especially fuzzing [64], is effective at vulnerability detection in web and desktop software. However, the dynamic analysis of embedded systems [41] is challenging [69, 99] because of the close interaction with hardware and the lack of Operating System (OS) abstractions. The lack of robust and readily available dynamic analysis tools (comparable to those for x86 systems) further imposes engineering challenges. 

To mitigate this, _rehosting_ [37] has emerged as an effective technique. By decoupling firmware from its hardware dependencies and enabling execution within an emulated environment, rehosting facilitates deeper exploration and analysis of embedded software without the constraints of physical hardware. Existing rehosting techniques mainly focus on achieving high-fidelity execution without hardware and focus on modeling peripheral interactions through manually created models [30], pattern-based model generation [39], or models built using machine learning techniques [44,91]. They depend on the availability of an MCU-specific Instruction Set Architecture (ISA) emulator and require considerable engineering effort [100] to configure different peripherals. _We hypothesize that this high-fidelity execution is not required for vulnerability detection, and a coarse approximation of program behavior is sufficient_ . We validate our hypothesis through a preliminary analysis of previously reported bugs (§ 3.2.2). We find that most bugs occur at higher software levels, and not within architecture-specific elements like inline assembly. 

Starting from this observation, in this paper, we present LEMIX, a novel approach to rehost embedded applications as Linux applications (for x86), which we call LEAPPs, with the goal of improving vulnerability detection capability in embed- 

1 

ded software with minimal engineering effort. LEMIX enables the use of dynamic analysis techniques readily available for Linux applications, such as sanitizers [84] on embedded applications. However, converting embedded applications to x86 Linux applications and enabling dynamic analysis poses challenges, _i.e.,_ preserving execution semantics, retargeting to different ISA, and handling peripheral interactions. We maintain execution semantics by leveraging the Linux Portable Layer, which comes as a part of most of the prevalent RTOSes (§ 4.1.1). We use an interactive refactoring approach (§ 4.1.2) to handle ISA retargeting. We tackle peripheral interactions (§ 4.1.4) by first identifying MMIO addresses through constant address analysis and using runtime instrumentation to feed peripheral data through standard input, thereby eliminating the need for precise peripheral models. We also weaken peripheral state-dependent conditions to improve code coverage, which is often limited by these conditions that are difficult for a fuzzer to bypass. To further improve testing, we apply a function-level fuzzing approach based on available research [59, 71] that directly invokes the target function with appropriate arguments generated from the input. Taken together, these design choices form a novel rehosting methodology that enables efficient bug discovery in embedded applications without sacrificing practical effectiveness, as demonstrated by our findings. 

We evaluated LEMIX on 18 real-world embedded applications ranging across four RTOSes, including FreeRTOS, Nuttx, Zephyr, and Threadx. These RTOSes support major semiconductor platforms like Qualcomm, NXP, Nordic [5, 8, 9,13] etc. We show that our approach can successfully convert applications to LEAPP with only a little manual effort. We tested LEAPPs by using whole-program fuzzing and functionlevel fuzzing and found 21 previously unknown bugs with 14 out of 18 applications effected by these bugs. Our ablation study shows that each of our techniques significantly contribute to the overall effectiveness of LEMIX. Finally, comparative evaluation against the state-of-the-art approaches shows that LEMIX is superior at improving code coverage ( _∼_ 2X more coverage) and bug detection (18 additional bugs). 

|**RTOS**|**Low Fidelity**|**High Fidelity**|
|---|---|---|
|FreeRTOS|20|2|
|Zephyr|26|7|
|RIOT|14|2|
|**Total**|**60 (85%)**|**11 (15%)**|



Table 1: Our analysis of the CVEs from the Rust4Embedded survey [6], [85] indicates that 60 out of 71 (85%) require lowfidelity execution. Table 11 (Appendix) has category-wise breakdown of the bugs. 

## **2 Background and Threat Model** 

We provide the necessary background of our target embedded systems (§ 2.1) and information about their software architecture (§ 2.2), along with our threat model (§ 2.3). 

## **2.1 Type-2 Embedded Systems** 

Embedded systems perform a designated task with customdesigned software and hardware. Following previous systematization works [37, 69], these systems can be categorized into three types: Type-1 systems use general purpose OSs retrofitted for embedded systems, _e.g.,_ Embedded Linux; Type-2 systems use an RTOS, a class of OS that provides timing guarantees, minimal hardware abstraction, and prioritizes tasks to meet strict timing constraints critical for real-time applications, and Type-3 systems use no OS abstractions. 

In this work, we focus on Type-2 systems, which consist of an RTOS combined with application code. Type-2 designs are common in safety-critical scenarios, supported by the availability of safety-certified RTOSes [7, 12, 96], which comply with guidelines like those set by MISRA [22] and provide real-time guarantees [94]. As shown in Figure 1, they have a layered design [88] and decouple the application components from the underlying RTOS kernel. Most RTOSes modularize their code base to capture all the hardware-specific functionalities within a portability layer specialized per MCU. 

In summary, the following are our contributions: 

- We propose LEMIX, an extensible framework to rehost embedded applications as x86 Linux applications ( _i.e.,_ LEAPPs) without emulation or physical devices. 

- We design various analysis techniques to tackle challenges in maintaining execution semantics, retargeting, and handling peripheral interactions. We also design techniques to improve the testing and code-coverage of LEAPPs. 

- We evaluated LEMIX on 18 embedded applications across four Real Time Operating Systems (RTOSes) and found 21 previously unknown bugs, most of which are confirmed and fixed by the corresponding vendors. 

- Our comparative evaluation against state-of-the-art approaches shows that LEMIX is superior in code coverage and bug detection. 

## **2.2 Portability Layers** 

As shown in Figure 1, RTOSes depend on a portable architecture to enable easy support for the diverse set of available CPU architectures and boards. Specifically, the portable layer provides header files that define interfaces between the hardware-agnostic kernel and the various MCU-specific ports. The RTOS kernel above the portable layer contains hardwareagnostic code. The hardware-specific implementations, containing interactions with specific MCU registers, memory regions, and peripherals, are contained in MCU ports, which are compiled and linked with the kernel. As a result of the portable architecture, an embedded application designed for a specific CPU architecture can run on a different CPU archi- 

2 


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0003-00.png)


<!-- Start of picture text -->
Task2<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0003-01.png)



![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0003-02.png)


<!-- Start of picture text -->
Task3<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0003-03.png)



![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0003-04.png)


<!-- Start of picture text -->
Third<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0003-05.png)



![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0003-06.png)



![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0003-07.png)



![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0003-08.png)


<!-- Start of picture text -->
Handler Invocation<br>Task2 Task3 Taskn<br>RTOS / Library Third<br>party<br>Linux Portable Layer SDK<br>(LPL)<br>Dispatcher Task<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0003-09.png)


<!-- Start of picture text -->
Handler Invocation<br>Task2 Task3 Taskn<br>RTOS / Library Third<br>party<br>Linux Portable Layer SDK<br>(LPL)<br>Dispatcher Task<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0003-10.png)


<!-- Start of picture text -->
Linux Portable Layer SDK<br>(LPL)<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0003-11.png)



![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0003-12.png)



![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0003-13.png)


<!-- Start of picture text -->
MMIO Accesses modeled as Reads from Standard Input<br><!-- End of picture text -->

Figure 1: Architecture of a Type-2 Embedded System and overview of LEMIX approach to convert it to a Linux Application. 

tecture by replacing the current MCU port with that of the new architecture [51]. 

To improve testability and aid embedded firmware development, many RTOSes also provide ports for various host operating systems such as Linux and Windows. We refer to these ports as the _Native Portable Layer (NPL)_ and this includes the _Linux Portable Layer (LPL)_ and the _Windows Portable Layer (WPL)_ . These native ports allow embedded applications built on these RTOSes to be run on respective desktop operating systems as native applications. Native ports use host-provided implementation to simulate various embedded functionalities. For example, the Linux Portable Layer (LPL) of the FreeRTOS [2] and Zephyr [14] operating systems use Linux _pthreads_ to simulate tasks, _signals_ to simulate interrupts, and _timers_ to simulate clocks in the application. We provide more details about NPL in Appendix B.0.2. 

## **2.3 Threat Model** 

Embedded applications receive inputs from a variety of sources, such as network interfaces, external storage devices ( _e.g.,_ SD cards, USB), user-provided inputs via buttons or screens, and peripherals accessed through Memory Mapped I/O (MMIO). In our threat model, we assume that _the attacker can control all inputs to the embedded application, including those coming from peripherals accessed via MMIO accesses_ . Specifically, all values through MMIO reads are fully controlled by the attacker. The goal of the attacker is to trigger vulnerabilities in the embedded application. 

This threat model is reasonable from the Defense in Depth perspective [70] and has been used in several other works [20, 53, 60]. Also, from a software resilience standpoint, it is important to reasonably validate data received from external entities (such as peripherals) to avoid arbitrary 

failures. For instance, in Listing 15 (Appendix), blindly trusting the data from MMIO GPIOx->LATCH (Line 2) could result in an infinite loop (Line 23), causing DoS. 

## **3 Motivation** 

Dynamic analysis, such as fuzzing, is shown to be an effective technique for vulnerability detection [64]. Scalable dynamic analysis of Type-2 embedded applications requires an instrumentation capability ( _e.g.,_ through an emulator) and hardware independence. One of the most popular approaches is _rehosting_ [37], where an unmodified embedded firmware will be executed or rehosted in a virtualized environment. One of the main challenges in rehosting is to achieve execution fidelity. The existing rehosting techniques can be categorized according to the developer/analyst effort and execution fidelity as shown in Figure 2. Ideally, we want to achieve _the highest execution fidelity with the least analyst effort in a hardware-independent manner_ — a known hard problem and the holy grail of rehosting [37]. Most of the recent rehosting techniques try to achieve high execution fidelity and mainly focus on automated techniques to precisely model peripheral interactions — which are hard to generalize across peripherals. Furthermore and more importantly, such high-fidelity execution may not be needed to detect most vulnerabilities. 

## **3.1 Execution Fidelity (EF)** 

Adapting<sup>1</sup> the categorization from Wright _et al.,_ [100], Execution Fidelity (EF) in embedded systems can be broadly grouped into four categories: 

> 1We build upon the broader categorization of Wright _et al.,_ by introducing more granular taxonomies, enabling a more detailed assessment of execution fidelity specifically in the context of embedded systems. 

3 


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0004-00.png)


<!-- Start of picture text -->
1 int32_t tud_msc_read10_cb( uint32_t lba, uint32_t offset,<br>2 void * buffer, uint32_t bufsize)<br>3 {<br>4 // out of ramdisk<br>5 if ( lba >= DISK_BLOCK_NUM ) {<br>6 return -1;<br>7 }<br>8 /* Attacker can offset to sensitive memory */<br>9 uint8_t const * addr = msc_disk[lba] + offset; �<br>10 /* Controlled write to known memory<br>11 may cause undefined behavior */<br>12 memcpy(buffer, addr, bufsize); �<br>13 return ( int32_t ) bufsize;<br>14 }<br><!-- End of picture text -->

Listing 1: Lack of bounds check on offset in tud_msc_read10_cb allows out-of-bounds read from msc_disk[lba], potentially leading to information disclosure or undefined behavior. 

**_Language Semantic Fidelity (S):_** The degree to which the execution preserves the high-level language ( _e.g.,_ C/C++) semantics intended by the programmer, including control flow, data types etc. 

**_Assembly Execution Fidelity (A):_** The correctness of executing assembly instructions which constitutes instruction-level behavior and any deviations due to instrumentation etc. In contrast to **S** , which focuses on high-level program behavior, **A** pertains to low-level execution behavior as specified by the processor’s instruction set architecture (ISA). 

**_Peripheral Handling Fidelity (P):_** The extent to which peripheral interactions ( _e.g.,_ memory-mapped I/O) are accurately modeled or handled during execution. While **A** ensures correct instruction behavior, P focuses on the correctness of effects on peripheral device interaction, requiring hardware modeling beyond the instruction level. 

**_Clock Fidelity (C):_** The accuracy of timing behavior with respect to real-time constraints such as instruction timing, interrupts, system clock behavior etc. 

For the sake of simplicity, we define Execution Fidelity (EF) as _< S, A, P,C >_ , where each component is categorized as **Low (L)** , **Medium (M)** or **High (H)** . While we adopt this discrete structure for clarity, finer gradations or even a continuous scale (Examples in Appendix § B.0.1) may offer further insights and are left for future work. This definition of EF also provides a way to categorize existing works. For instance, hardware-in-the-loop approaches, such as AVATAR [103], redirect all peripheral handling to the real board and execute the embedded firmware on the emulator. The split execution does not preserve the relative clock semantics between the emulator and actual hardware and only achieves partial clock fidelity, _i.e.,_ C = _M_ (Medium). The EF achieved by these approaches can be specified as _< H, H, H, M >_ . 

## **3.2 Bug Manifestation Fidelity (BMF)** 

_BMF_ is the minimum fidelity required to reach and observe the effects of the bugs of interest. BMF varies according to 

the type of bugs. For instance, to observe scheduling bugs, we need an accurate clock fidelity, _i.e.,_ C, in addition to the other components, depending on where the bug is. If scheduling bugs do not involve assembly, we do not need A. We therefore analyze known vulnerabilities in embedded software to understand the BMF required for memory corruption vulnerabilities (a common class of vulnerabilities). Specifically, which execution aspects out of **S, A, P, C** (§ 3.1) are required and which of them can be approximated. 

### **3.2.1 Empirical Data** 

We manually analyzed 84 publicly reported vulnerabilities in C/C++ software taken from the recent work by Sharma _et al.,_ [86] to identify what degree of fidelity is required to manifest them. This included CVEs with available patch information from open-source RTOSes, _i.e.,_ FreeRTOS, Zephyr, and RIOT. We considered only the common case of memory corruption vulnerabilities, omitting categories such as weak authentication and SQL injection. Memory corruption vulnerabilities comprised 71 out of the 84 vulnerabilities. 

For each CVE, we identified the target vulnerability and affected function by manually analyzing the CVE description and the corresponding patch. We then check if the vulnerability can be triggered with low-fidelity rehosting. Specifically, we target vulnerabilities characterized by an EF of _< H, L, M, M >_ , as defined in § 3.1. We consider those that meet all requirements to be triggerable with low-fidelity rehosting, else high fidelity is needed. Listing 16 (Appendix) shows an example of a CVE requiring high-fidelity rehosting and Listing 13 (Appendix) shows an example of a CVE requiring low-fidelity. We summarize our results in Table 1. More details can be found in Table 11 (Appendix). Our analysis is further confirmed by recent work [95], which detected various vulnerabilities through low-fidelity dynamic analysis. 

### **3.2.2 BMF For Embedded System Software** 

Based on our empirical study § 3.2.1, the BMF required for most of the memory corruption bugs is _< H, L, M, M >_ , which is what LEMIX targets. Following the definitions of Wright _et al.,_ [100], BMF for most memory corruption vulnerabilities can be approximated to module-level execution fidelity. Specifically, we should be able to execute a module ( _i.e.,_ a group of functions) with _enough fidelity_ to expose a bug. Listing 1 demonstrates a motivating example of a bug we discovered in TinyUSB. The tud_msc_read10_cb function lacks bounds checking on the offset parameter, allowing out-ofbounds reads from the msc_disk array (at line 9), which can cause potential information disclosure or even undefined behavior, depending on how the buffer is further used. We do not need a high-fidelity execution to detect the bug in Listing 1. We just need to execute the function tud_msc_read10_cb and pass a large number as offset. We also need the capability to 

4 


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0005-00.png)


<!-- Start of picture text -->
[48] [56]<br>[4] [93]<br>Abstract Model<br>of Application<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0005-01.png)


<!-- Start of picture text -->
[30] [91]<br>[26] [27]<br>SW Approaches<br>With Precise<br>Peripheral<br>Modeling<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0005-02.png)


<!-- Start of picture text -->
LEMIX<br>(BMF)<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0005-03.png)


<!-- Start of picture text -->
[39] [82]<br>[40] [105]<br>SW Approaches<br>With No<br>Peripheral<br>Modeling<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0005-04.png)


<!-- Start of picture text -->
[55] [68]<br>[32] [80]<br>[46] [43]<br>HW Dependent<br>Approaches<br><!-- End of picture text -->

Figure 2: Existing Rehosting Techniques v/s LEMIX 

detect out-of-bound memory access (at line 9), which is challenging in embedded systems because of the lack of memory protection mechanisms [69]. Although we do not require precise peripheral models to trigger the bug, achieving BMF or module-level execution fidelity without them is challenging. As mentioned in § 2.1, embedded applications are organized into a set of tasks and use a real-time scheduler to trigger the tasks. To execute the function tud_msc_read10_cb in Listing 1, we need to ensure the task containing the function gets executed, which further depends on the scheduler, which requires precise models for the clock peripheral. _Can we achieve BMF without explicitly providing precise peripheral models?_ In summary, we need the capability to execute embedded application, handle MMIO accesses ( _i.e.,_ provide data on reads and ignore writes), and detect memory safety violations. 

## **3.3 The Idea** 

Dynamic analysis challenges like execution environment and detectability have been well studied for Linux applications on standard ISAs (e.g., x86, x64), with many effective solutions [24, 34, 89]. Prior work, such as AoT [52], extracts components from complex systems (e.g., Linux kernel) into testable user-space applications. Our goal is to convert embedded applications into Linux applications to enable BMF and make existing dynamic analysis techniques [65] applicable. Srinivasan _et al.,_ [92] recently showed this is feasible by manually converting three simple FREERTOS applications. However, designing a generic technique involves tackling the following challenges. 

- **(Ch1) Preserving Execution Semantics.** Linux applications, by default, follow single-threaded execution. However, embedded applications (as explained in § 2.1) are engineered in terms of event-driven tasks and are multithreaded [45]. Simply replacing RTOS files with their POSIX equivalents (LPL) often leads to unintended er- 

rors during integration. Incorporating a POSIX-compatible RTOS requires a systematic and automated mechanism. This involves more than just file replacements; it necessitates careful adaptation to preserve the embedded system’s original task-based and event-driven execution semantics. 

- **(Ch2) Retargeting to different ISAs.** Though majorly developed in C, embedded applications use various nonstandard and embedded toolchain-specific C features not supported by traditional compilers for desktop ISAs, _e.g.,_ x86. The presence of inline ISA-specific assembly ( _e.g.,_ of ARM) further complicates retargeting ( _i.e.,_ compiling) for other ISAs. We need to have a mechanism to compile an embedded application for common desktop ISAs. 

- **(Ch3) Handling Peripheral Interactions.** Embedded systems directly interact with peripherals, mostly through a dedicated set of MMIO addresses [77]. It is crucial to distinguish these MMIO addresses from regular memory accesses because they correspond to physical hardware components, and improper handling can lead to incorrect behavior. 

## **4** LEMIX 

We design LEMIX, an interactive framework enabling effective dynamic analysis of embedded applications by converting them to Linux applications, which we call LEAPP. The novelty of LEMIX lies in recognizing and harnessing the BMF insight, _i.e.,_ rehosting with just enough execution fidelity to keep most security bugs triggerable, thereby significantly reducing the manual effort and complexity typically associated with generalizing full system emulation. The right side of Figure 1 shows the summary of our approach to tackling the challenges (§ 3.3) in converting to LEAPP. The LEMIX framework has two phases as illustrated in Figure 3. In Phase 1, we convert the given embedded application into LEAPP using static analysis techniques and compiler instrumentation. We use an interactive approach to tackle certain complex code idioms during retargeting. We also design instrumentation techniques for LEAPPs to improve the effectiveness of dynamic analysis, specifically random testing. In Phase 2, we focus on testing LEAPP. We support two modalities, whole-program, and function-level testing, providing a holistic testing infrastructure. 

## **4.1 Phase 1: Analysis Friendly** LEAPP 

This phase generates a dynamic analysis-friendly LEAPP from a given embedded application and the target RTOS configuration. This part tackles challenges (1-3) from § 3.3. 

### **4.1.1 Handling execution semantics using LPL (Ch 1)** 

As explained in § 2.1, embedded applications rely on RTOS functions for their execution semantics. For instance, an appli- 

5 


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0006-00.png)



![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0006-01.png)


<!-- Start of picture text -->
Runtime Interactive Automated<br>Interactive Library<br>Resolution<br>Whole<br>Sec. 4.1.1 Program<br>NPL Fuzzing<br>LLVM Bitcode LeApp with<br>Retargetting  for LeApp Peripheral HandlingMMIO DynamicAnalysis LeApp<br>Modeling and<br>Assistance<br>Application Instrumentation Instrumentation Function<br>Retargeting Sec. 4.1.3 Sec. 4.1.4 Sec. 4.1.5 Level<br>Sec. 4.1.2 Fuzzing<br>LeApp Generation<br>Phase 1: Generating Dynamic Analysis Friendly LeApp Phase 2: Testing<br>Sec. 4.2<br>RTOS<br>Configuration<br>Symbol<br>Oppurtunitic Resolution<br>Embedded Application source code<br><!-- End of picture text -->

Figure 3: Overview of our LEMIX framework. 

cation for FREERTOS uses xTaskCreate function to create a task and vTaskStartScheduler to start the scheduler. Similarly, xTimerCreate function is used to register for a timer event. 

Embedded systems use a portable layer enabling an RTOS to be used for different MCUs (Figure 1). As explained in § 2.2, most RTOSes maintain an NPL enabling them to run on top of regular OSes, _i.e.,_ Windows (WPL) or Linux (LPL). 

Given the source code of an embedded application, we identify the RTOS dependencies and re-configure them with corresponding LPL. To aid our process, we gather and maintain the LPL software packages of RTOSes apriori. This is not trivial as the build setup of the application may include MCUspecific configurations enabling certain HAL-specific APIs necessary for its functionality. For instance, in the FreeRTOS app TinyUSB, the configTIMER_QUEUE_LENGTH is set to 32, while the POSIX build sets it to 20, causing undefined behavior due to the application’s expectation that this value should not exceed its configuration. In few cases, peripheral models implemented in the original RTOS may not be available in the corresponding LPL. 

To address this, we designed a fully automated approach that selectively integrates configurations from the application that do not disrupt the LPL build. Each RTOS configuration from the application is iteratively toggled in the LPL build, retaining those that compile successfully. Once the LPL build successfully incorporates the necessary configurations, we replace the application’s RTOS object files with those from the successful LPL build. We term this process as **POSIX Swap** . This approach however can induce unexpected behaviors in the ported application since not every configuration was incorporated from the application’s config. But, we did not observe any false positive crashes due to misconfigured LPL build during our evaluation. 

### **4.1.2 Interactive Resolution for Retargeting (Ch 2)** 

As mentioned in § 3.3, our goal is to build LEAPP for common desktop ISAs, specifically x86, because of the availability of various testing tools. We want to use the CLANG compiler as 

the LLVM IR enables us to easily perform various analysis tasks, and also, several techniques ( _e.g.,_ loop analysis) already exist in the CLANG infrastructure. However, just replacing the compiler with CLANG and changing the target ISA to x86 does not work. Because (as mentioned in § 3.3) embedded applications use non-standard C language features and inline assembly of other ISAs, _e.g.,_ ARM. Handling this requires program semantic reasoning [57], a known hard problem. 

We use an _interactive human-in-the-loop refactoring approach to tackle this_ . We aim to automatically refactor the code to be CLANG and x86 friendly using a set of refactor patterns. However, for cases requiring semantic reasoning, we resort to developer assistance by providing precise guidance instructions. Our automation takes over after developer assistance, and the process continues with intermittent manual refactorings until the resulting code can be compiled using CLANG, _i.e.,_ able to generate LLVM Bitcode. The Table 12 (Appendix) summarizes automated and interactive refactorings. Further details of the build process tracing and streamlining the build system for x86-clang can be found in Appendix B.2. 

We classify the set of refactorings into the following two categories and present the techniques used to handle them: 

1. **Compiler Incompatibilities:** These are incompatibilities because of compilers (GCC v/s CLANG) and architecturedependent code, _e.g.,_ expecting **int** to be of 4 bytes. A significant portion of embedded software relies on GCC-based toolchains [98]. Hence, making the transition from a GCC build environment to CLANG is challenging, especially for embedded codebases [88]. Table 12 (Appendix) highlights the incompatibilities between GCC and CLANG affecting our embedded applications. Some of these, such as Variable-Sized Object initialization, are still not supported even in the latest version of LLVM at the time of writing (LLVM 18) [35]. Although several works [31, 62, 88] mention this problem, to the best of our knowledge, we are the first to highlight these issues, which have not yet received sufficient attention among embedded developers. 

6 

Addressing compiler incompatibilities requires semantically equivalent refactorings. We define a set of refactoring templates for automatically handling several of these issues and resort to developer assistance for others. We also provide guidance instructions to assist in the refactoring an example of which is shown in Listing 4 (Appendix). 

2. **Inline Assembly:** Embedded applications often use inline assembly for low-level operations, such as MCU-specific initialization [88]. LEAPP eliminates the need for such initialization by relying on LPL. As discussed in § 3.2.2, precise handling of assembly is unnecessary for manifesting most vulnerabilities. We automate source code rewriting to identify and comment out inline assembly regions. Commenting out assembly may lead to uninitialized or undefined variables ( _e.g.,_ Listing 5 Appendix). Most inline assembly reads architecture-specific registers for initialization checks. To address this, we randomly initialize variables defined by assembly to 0 or 1, allowing applications to bypass initialization routines over multiple runs. Our approach may not handle all cases, such as inline assembly within macros or machine code representations ( _e.g.,_ Listing 6 in Appendix). In such cases, we automatically detect issues and provide developers with precise instructions, such as resolving compilation errors like _expected closing parenthesis_ . LEMIX pinpoints problematic lines and suggests fixes, ensuring minimal manual intervention. 

### **4.1.3 Opportunistic Symbol Resolution** 

The final step in creating the LEAPP involves linking compiled LPL and application object files. However, directly linking RTOS object files often results in linker errors [23] because embedded applications may invoke MCU-specific functions [88] that are not present in LPL, causing undefined reference errors [81]. For example, in the FreeRTOS application _Infinitime_ , the function _xTimerGenericCommand_ is invoked but not available in LPL, leading to a linker error. 

LEMIX incrementally resolves linker errors by selectively linking only the required object files from the prebuilt LPL, resolving linker conflicts in an automated fashion. This is achieved using an opportunistic approach by identifying and linking MCU-specific RTOS object files (denoted as _Ou_ ) that define the missing symbols. However, this can cause multiple definition errors if symbols in _Ou_ overlap with those in LPL. For instance, resolving _xTimerGenericCommand_ by including the application kernel’s _timers.o_ introduces duplicate definitions, such as _prvInitialiseNewTimer_ , between the application kernel’s _timers.o_ and the LPL kernel’s _timers.o_ . We want to ensure that references are linked with the expected symbols. We use a two-phase approach to tackle this: 

1. **Creating Library Archives:** We observed that embedded applications and RTOSes use build procedures based on archiving [1], which prevents duplicate symbol errors 

across multiple components, _e.g.,_ an application can have a function (say _f_ ) with the same function as an RTOS function. Creating an archive of application-specific object files ensures that all references to _f_ within these object files are linked to the application-specific version. We trace the build process to identify which archives (and their order) were created and the corresponding object files. We follow the same order when creating and linking archive files to ensure that original references are intact. 

2. **Modifying Symbol in One of the Objects:** The remaining multiple references cannot be resolved by archiving; hence, the symbol name has to be modified in one of the object files. If the multiple reference is between an Application’s object file and LPL object file, we change the symbol name in the Application object file, which ensures that calls in the application to LPL functions are linked appropriately. 

**Handling Symbol Aliasing:** In the original application’s build procedure, the linker might create aliases for various symbols to maintain interoperability across different boards as guided by linker scripts. For instance, the symbol ___init_clock_ might be resolved to aliases like ___stm32_clock_init_ or ___nrf52_clock_init_ , depending on the target board. Additionally, multiple aliases can be created for the same symbol. Ignoring such aliases results in NULL-ptr deferences while executing the resulting LEAPP. To tackle this, we first extract the aliasing information using firmware debug symbols from the original embedded application (compiled for the target MCU) and identify symbol aliases with the help of GDB. Next, we instrument our LEAPP and link the symbol aliases to the appropriate references in LEAPP. 

### **4.1.4 Peripheral Modeling and Instrumentation (Tackling Ch 3)** 

As mentioned in § 2.3, our threat model includes malicious peripherals, _i.e.,_ we assume that all inputs from peripherals can be controlled by an attacker. As mentioned in § 2.1, applications interact with peripherals by accessing corresponding MMIO addresses and interrupts. 

**Handling MMIO Accesses:** Input from peripherals is received through reading MMIO addresses. We aim to model loads ( _i.e.,_ reads) from these addresses as reads from standard input and ignore stores ( _i.e.,_ writes) as we focus on vulnerability detection ( _i.e.,_ BMF as described in § 3.2.2). 

First, we determine MMIO address ranges. One of the common techniques is to find these address ranges from peripheral System View Description (SVD) files [10]. However, as we will show in § 5.3, oftentimes, SVD files are incomplete and do not contain all peripheral address ranges which is also a known problem [19]. We aim to create an automated technique that does not depend on SVD files. Peripherals have predefined MMIO address ranges, and applications access them through hardcoded addresses [39, 91]. We perform a 

7 

1 **uint32_t** HAL_RCC_GetSysClockFreq( **void** ) { 2 **uint32_t** pllm = 0U, pllvco = 0U, pllp = 0U; 3 **uint32_t** sysclockfreq = 0U; 4 **<mark>if</mark>** <mark>(isMMIO(RCC->PLLCFGR)) {</mark> 5 <mark>pllm = get_input_from_stdin() & RCC_PLLCFGR_PLLM;</mark> 6 <mark>}</mark> **<mark>else</mark>** <mark>{</mark> 7 pllm = RCC->PLLCFGR & RCC_PLLCFGR_PLLM; � 8 <mark>}</mark> 9 ... 10 sysclockfreq = pllvco / pllp; � ...} 

Listing 2: � shows original MMIO accesses that are instrumented in LEAPP. � shows a div-by-zero bug in STM32. 

constant address analysis to determine all hardcoded address values, _i.e.,_ constant values used as pointer operands in load and store instructions. The corresponding pages form the base MMIO pages ( _Pm_ ). For instance, if we found a constant address _x_ , then we will add the corresponding page [ _b, b_ + 4093] to _Pm_ , where _b_ = ( _x_ & _∼_ (0 _x_ 3 _FF_ )) is the base address of the corresponding page. We also perform additional coalescing and consider all pages within a range of ±2 KB from that boundary, also as MMIO addresses. This approach helps group related MMIO access and ensures that accesses within the same memory-mapped region are consistently recognized. 

Next, we will hook all loads and stores through compiletime instrumentation and link with our runtime library. At runtime, our hook will check if a load is within an MMIO address range; if yes, then it will read an appropriate number of bytes from input and return the corresponding value. Similarly, our hook will ignore all stores to MMIO address ranges. Listing 2 shows the example of our instrumentation (highlighted lines), where the memory access RCC->PLLCFGR is checked to see if it is an MMIO address; if yes, we will read a value of corresponding size ( _i.e.,_ 4 bytes) from input. **Handling Interrupts:** Interrupts are treated as peripheral inputs and triggered at random intervals. LEMIX identifies Interrupt Service Routines (ISRs) using RTOS-specific patterns, such as ISR vector tables in assembly files, while ignoring handlers implemented in assembly. Using RTOS-specific templates, we create a _Dispatcher Task_ to invoke ISRs at arbitrary intervals (Listing 7 in the Appendix). To prevent false crashes from ISRs requiring preconditions (e.g., valid global pointers), we use lightweight binary analysis and dynamic tracing to identify and disable them. 

### **4.1.5 Dynamic Analysis Assistance Instrumentation** 

Embedded applications have considerable peripheral statedependent code [82]. Specifically, they check for peripherals to be in a specific state before interacting with it or to perform some interesting function, _e.g.,_ as shown in Listing 3, at lines 3-4, the code busy-waits until the control register (accessed through MMIO read NRF_CLOCK->LFCLKSTAT) has any of the bits corresponding to CLOCK_LFCLKSTAT_STATE_Pos that are not set. 

Peripherals state is accessed through reading certain registers [54, 82], _e.g.,_ clock state is accessed through 


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0008-07.png)


<!-- Start of picture text -->
1 // Before Condition Weakening<br>2 while<br>3 ((NRF_CLOCK->LFCLKSTAT & CLOCK_LFCLKSTAT_STATE_Pos)�) {<br>4 // Busy Waiting<br>5 � };<br>6 interesting_function();<br>7 // After Condition Weakening<br>8 label:<br>9 bool cond = (NRF_CLOCK->LFCLKSTAT &<br>10 CLOCK_LFCLKSTAT_STATE_Pos); �<br>11 new_cond = cond;<br>12 if (isMMIO(NRF_CLOCK->LFCLKSTAT) && stdin_read() % 2) �<br>13 new_cond = !cond; �<br>14 while (new_cond) { goto label};<br>15 interesting_function();<br><!-- End of picture text -->

Listing 3: � indicates MMIO coverage blockers, � marks busy waiting due to unsolved constraints, � represents our instrumentation and � shows MMIO condition toggling. 

NRF_CLOCK->LFCLKSTAT (an MMIO address) in Listing 3. Since we model all peripheral reads (§ 4.1.4) as reads from standard input, the coverage of state-dependent code becomes the problem of constraint input generation. For instance, in Listing 3, the MMIO access, _i.e.,_ , NRF_CLOCK->LFCLKSTAT will be fetched from input. For the execution to reach out of the loop, an input generation technique ( _e.g.,_ AFL++) should provide an input that satisfies the constraint. Existing techniques handle this by providing precise peripheral models [82, 91] or symbolic execution [33], but they have scalability issues [37]. 

To tackle this, we perform _Weakening of Peripheral State Dependent conditions_ . Specifically, we instrument each conditional instruction to check whether it involves reading from an MMIO address; if yes, we weaken the condition such that any value can satisfy the constraint with 50% probability as shown in the lower part of Listing 3. Previous works [29, 74] show that such an approach improves the effectiveness of fuzzing. We will also show in § 5.5 that our approach greatly improves the coverage. We also perform instrumentation to collect additional metrics, such as coverage. 

## **4.2 Phase 2: Testing** 

This phase focuses on fuzzing of LEAPPs generated in Phase 1. We explore two modes of fuzzing: (i) Whole program and (ii) Function level. 

### **4.2.1 Whole Program Fuzzing** 

Here, we fuzz LEAPPs as a whole by providing inputs at appropriate locations ( _i.e.,_ MMIO accesses) until LEAPP terminates or crashes because of a bug. 

### **4.2.2 Function Level Fuzzing** 

In this mode, we directly fuzz individual functions by providing arguments of appropriate type [21, 104]. Given a function _f_ , we use a simple co-relation analysis [76] to determine the argument types and their size associations, _e.g.,_ 

8 

Table 2: Approximate Number of unique basic blocks discovered by various configurations of LEMIX in comparison to State Of The Art Tools (Discussed in § 5.4 and § 5.6). M1- M3 represents different configuration modes for LEMIX. Refer to Table 13 (Appendix) for a larger version. 

|**AppID**||||**Lx**||||**Fw**|||**Mf**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**M**|**1**|**M**|**2**|**M**|**3**|||||||
||Cov|Bug|Cov|Bug|Cov|Bug|Cov|Crash|Bug|Cov|Crash|Bug|
|f1|731|0|2.9k|1|�|1|500|1|0|1k|0|0|
|f2|456|1|2.8k|3|�|1|�|N/A|N/A|1.5k|1|1|
|f3|560|1|668|2|1.5k|3|�|N/A|N/A|�|N/A|N/A|
|f4|563|0|1k|1|6k|3|500|0|0|2k|41|0|
|f5|442|0|728|2|1.8k|2|700|0|0|1.8k|93|0|
|n1|105|0|301|1|13.5k|1|356|0|0|25.2k|148|0|
|n2|143|0|338|0|16.8k|1|405|0|0|300|0|0|
|n3|157|1|357|1|19.9k|1|60|1|1|100|1|0|
|n4|135|0|235|1|19.5k|1|388|3|0|2.4k|0|0|
|n5|823|0|1.5k|1|�|0|134|0|0|226|0|0|
|z1|76|0|86|2|3k|4|44|2|0|213|0|0|
|z2|�|0|�|2|12.3k|3|�|N/A|N/A|10.8k|483|1|
|z3|�|0|�|2|4.6k|6|�|N/A|N/A|�|N/A|N/A|
|t1|210|0|553|0|6.3k|0|670|0|0|750|0|0|
|t2|214|0|553|0|240|0|791|0|0|694|0|0|
|t3|�|0|�|0|3.1k|0|900|0|0|700|0|0|
|t4|310|0|455|1|188|1|749|0|0|659|10|1|
|t5|254|0|436|0|5.2k|0|748|0|0|658|0|0|
|Avg/Tot|345|3|860|20|7.5k|28|496|7|1|3.1k|777|3|
|Unique Bugs||3||10||11|||1|||3|



for a function that accepts two arguments, an integer array pointer, and its length; our co-relation analysis will produce: {arg1: {ARRAY, **int** , SIZE: arg2}, arg2: **int** }. Next, we automatically create generators for each of the argument types, _i.e.,_ functions that generate values of a specific type from the input. For instance, for the above example, the generator will create an integer array of an arbitrary size, populate it with random integer values, and return the pointer and size. Finally, we invoke _f_ with the pointer returned by the generator and the size as the second argument. Unlike whole program fuzzing (§ 4.2.1), each fuzzing run in function level fuzzing invokes the target function once and exits. 

## **5 Evaluation** 

We use a combination of Python scripts and CLANG/LLVM 10 toolchain passes to implement our framework. We provide more details in Appendix B.2. We evaluate LEMIX by answering the following questions: 

- **RQ1** ( _Converting to_ LEAPP _(§ 5.2)_ ): How effective is our approach (§ 4.1.2) in converting embedded applications to LEAPPs? How much manual effort does it require? 

- **RQ2** ( _Peripheral Handling (§ 5.3)_ ): How effective is our approach (§ 4.1.4) in identifying MMIO addresses? 

- **RQ3** ( _Testing_ LEAPP _Applications (§ 5.4)_ ): What is the effectiveness of testing LEAPPs through different fuzzing approaches, _i.e.,_ whole-program fuzzing and functionlevel fuzzing? 

- **RQ4** ( _Ablation Study (§ 5.5)_ ): What is the contribution of 

|**RTOS**|**ID**|**SRC**|**ASM**|**RTOS**|**SDK**|
|---|---|---|---|---|---|
||f1|88k|2.2k|105k|100k|
||f2|22k|2.6k|13.5k|2.16M|
|FreeRTOS|f3|32.4k|1k|10.3k|130k|
||f4|657k|1.5k|209k|65k|
||f5|656k|2k|209k||
||n1|429k|26k|1.7M||
||n2|428k|22k|1.6M|8k|
|Nuttx|n3|429k|23k|1.65M||
||n4|429k|25k|1.7M||
||n5|310k|600|1.5M|198k|
||z1|200|1k|19k|0|
|Zephyr|z2|5.6k|0|20k|3k|
||z3|14.2k|0|20k|2.4k|
||t1|413k|52.1k|351k||
||t2|236k|52.2k|351k||
|Threadx|t3|333k|51.3k|351k|335k|
||t4|185k|51.4k|351k||
||t5|310k|52k|351k||



Table 3: Breakdown of Source Lines of Code by source files, assembly (inline + standalone) , RTOS, and SDK (counted once per application). See Table 7 (Appendix) for descriptions of each application. 

   - our peripheral handling (§ 4.1.4) and dynamic analysis assistance (§ 4.1.5) on overall effectiveness? 

- **RQ5** ( _Comparative Evaluation (§ 5.6)_ ): What is the effectiveness of LEMIX compared to the existing state-of-the-art? 

- **RQ6** ( _False Positive Analysis (§ 5.7_ )): What false positives are introduced by low-fidelity execution, how do they compare against existing State-Of-The-Art, and how are they remediated? 

## **5.1 Dataset and Setup** 

**Dataset:** Table 3 gives details of our application set with percomponent SLOC, selected in 2 steps. 

First, to study Type-2 embedded systems, we ensured diversity at the RTOS level, choosing four popular RTOSes: FreeRTOS (widely used in resource-constrained systems), Zephyr (modularity and scalability), Nuttx (POSIX-compliant and versatile), and ThreadX (optimized for high-performance real-time applications). 

Second, we sampled applications for each RTOS from GitHub, including major, actively maintained projects (e.g., PX4 for drones, Infinitime for smartwatches) and smaller, peripheral-focused ones (e.g., TinyUSB for USB, Nrf_Pwm for PWM tasks). 

**Setup:** We have conducted our experiments on an AMD EPYC 7543P 32 Core Processor with 64 threads and 128 GB of RAM. In whole program mode, we fuzzed each application for 48 hours following suggested best practices [49]. 

9 

In function-level mode, we fuzzed each target function for 10 minutes, after which coverage plateaued for most functions. 

## **5.2 RQ1: Converting to Linux Applications** 

### **5.2.1 Methodology** 

We measure the ability of LEMIX to successfully convert the 18 embedded applications in our dataset to Linux applications and the amount of manual effort required. An application is successfully converted if it can be compiled and executed on a Linux operating system without crashing. Additionally, as described in § 4.1.2, LEMIX relies on human intervention to guide retargeting to desktop ISA. We categorize the required human effort into three categories as follows: (a) Setup (Identifying source files and build/compilation instructions), (b) Addressing errors due to compiler incompatibilities, and (c) Handling inline assembly. We measure the time spent in each category and the impact on the application’s source files. 

These conversions were performed by the authors, who are graduate students with intermediate expertise in C/C++ but with less experience with embedded codebases. The conversion time to LEAPP depends on familiarity with the embedded codebase, so the reported measurements represent an upper bound; engineers with embedded expertise should require significantly less time. 


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0010-05.png)


<!-- Start of picture text -->
80<br>60<br>40<br>20<br>0<br>FreeRTOS Nuttx Zephyr Threadx<br>RTOSes<br>Time (in mins)<br><!-- End of picture text -->

Figure 4: Comparison of manual effort time (y-axis) across RTOSes (x-axis), categorized into three categories: (a) - Preconfigurations and source modifications; (b) - Nonautomated compiler errors; (c) - Macro ASM adjustments. 

### **5.2.2 Results** 

Using LEMIX’s interactive approach, we successfully converted all the applications in our dataset to LEAPPs. As shown by the results in Table 2, we were able to execute and dynamically analyze all 18 applications. 

Figure 4 shows the box plot of time spent in each human effort category for applications across different RTOSes. In all RTOSes, setup time (category (a), median 40–60 min) is the largest contributor, mainly for identifying the build setup, dependencies, and toolchains. These times align with Shen _et al.,_ [87], who reported an average of 60 min for embedded 

build setup. Note that setup time is independent of LEMIX. As shown in Figure 4, our interactive steps (categories (b) and (c)) contribute minimally to the manual effort. 

Table 4 highlights SLoC affected for categories (b) and (c). Manual effort for (b) is relatively low (median 20–40 min) compared to the SLoC modified, demonstrating effective handling of compiler incompatibilities. For example, NuttX applications required no manual effort for (b) as they used standard C features supported by CLANG, larger FreeRTOS applications required more effort due to greater SLoC changes. 

Despite of a large number of ASM modifications, the amount of manual effort ( _i.e.,_ category (c) with a median of 20 - 30 min in Figure 4) is relatively less, demonstrating the effectiveness of our source code transformations to automatically handle inline assembly. 

RQ1 results demonstrate that LEMIX can successfully convert embedded applications to LEAPPs and requires minimal manual effort. 

## **5.3 RQ2: Peripheral Handling** 

### **5.3.1 Methodology** 

We assess the effectiveness of our constant address analysis in two ways. First, we validate discovered address ranges by checking for overlaps with the LEAPP’s actual memory map, ensuring MMIO ranges remain distinct. This validation leverages standardized memory boundaries documented in CMSIS-SVD files, which define peripheral registers and their address mappings. 

Second, we corroborate the results of LEMIX’s constant address analysis by comparing the discovered address ranges against those specified in CMSIS-SVD files [67]. Discrepancies are manually investigated through random sampling to understand gaps in identification. Both methods are necessary to ensure accuracy and to identify limitations of SVD-based documentation versus our constant address analysis approach. 

### **5.3.2 Results** 

The Table 5 shows the number of MMIO address ranges found across different applications. Upon investigation, we found that none of these address ranges conflict with the memory map of the corresponding LEAPP. Hence, instrumenting reads from these addresses should not affect LEAPP’s execution. 

When we compared the discovered address ranges with those in CMSIS-SVD files [67], we found that over 50% of our address ranges are missing in CMSIS-SVD files (last column of Table 5). Further analysis revealed that the missing address ranges represented valid MMIO addresses in the source code and corresponded with those used by valid core peripherals [19]. Listing 14 (Appendix) shows MMIO address ranges used in the codebase but missing from the corresponding peripheral’s SVD file. 

10 

Table 4: Detailed porting metrics for each application, including type of files modified, lines added or removed, and impact percentages (lines affected over total lines). The times are summarized in Figure 4. 

|**AppID**|**Tota**|**l Files**|**Total**|**Lines**|**Fi**|**les Modifed**||**Lines Added/R**|**emoved**|**Impact %**|
|---|---|---|---|---|---|---|---|---|---|---|
||**App**|**RTOS**|**App**|**RTOS**|**Sources**|**Headers**|**ASM**|**Sources + Headers**|**ASM**||
|||||||||**Category (b)**|**Category (c)**||
|f1|1.1k|612|184k|105k|2|8|6|2, -2|+505, -964|0.51|
|f2|5.8k|100|2.38M|13.5k|2|3|11|+218, -6|+410, -1483|0.09|
|f3|201|31|162.5k|10.3k|10|5|4|+502, -128|+539, -953|1.23|
|f4|232|584|724k|209k|3|2|4|+239, -2|+539, -1007|0.19|
|f5|230|584|723k|209k|2|1|4|+238, -2|+539, -1007|0.19|
|n1|400|14k|429k|1.7M|0|0|4|NIL|+133, -500|0.03|
|n2|378|13.9k|428k|1.6M|0|0|4|NIL|+133, -500|0.03|
|n3|355|13.8k|429k|1.65M|0|0|7|NIL|+147, -537|0.03|
|n4|400|14k|429k|1.7M|0|0|8|NIL|+148, -575|0.03|
|n5|455|12.9k|435k|1.5M|3|2|1|+6, -6|+152, -400|0.03|
|z1|50|6.2k|200|20k|7|3|0|+235, -171|NIL|1.27|
|z2|203|6.2k|8.6k|20k|7|3|0|+220, -180|NIL|1.40|
|z3|221|6.2k|16.6k|20k|7|3|0|+220, -180|NIL|1.09|
|t1|4.8k|1.3k|748k|351k|1|0|2|+3, 0|+568, -884|0.14|
|t2|3.8k|1.3k|571k|351k|0|0|2|NIL|+569, -879|0.16|
|t3|3.5k|1.3k|668k|351k|1|0|2|+4, 0|+568, -884|0.14|
|t4|3.3k|1.2k|520k|351k|0|0|1|NIL|+23, -167|0.02|
|t5|4.3k|1.2k|645k|351k|1|0|2|+3, 0|+568, -884|0.14|



RQ2 results show that our constant address analysis is effective at finding MMIO address ranges and provides more complete results than the commonly used approach of analyzing SVD files. 

## **5.4 RQ3: Testing** LEAPP **s** 

### **5.4.1 Methodology** 

In this RQ, we assess the effectiveness of the converted LEAPPs in supporting different fuzzing modes: Whole Program Fuzzing with MMIO instrumentation (M1), Whole Program Fuzzing with MMIO + Weakening State-Dependent Conditions (M2), and Function-Level fuzzing (M3) incorporating all optimizations from (M1) and (M2). We measure and report the code coverage (in terms of unique basic blocks covered) and the number of unique bugs detected through each mode, following crash triaging and manual confirmation according to our threat model. For whole-program fuzzing, we identified the MCU firmware ELF entrypoint and ensured the LEAPP’s entrypoint matched it (ignoring assembly-based entrypoints). This was necessary to initialize global structures for peripheral handling and avoid NULL-ptr dereferences in the LEAPP. To identify candidate functions for function-level fuzzing, we first filtered functions that take pointer arguments without a specified size. Next, we manually verified (5 minutes per function) whether these functions performed any interesting operations, such as pointer arithmetic or explicit casts, which are common in risky programming idioms. Previous work [36] indicates that these characteristics are strong 

|**AppID **|**Detected MMIOs **|**In SVD (% of Detected)**|
|---|---|---|
|f1<br>|45<br>|11 (24.44)<br>|
|f2<br>|33<br>|16 (48.48)<br>|
|f3|35|18 (51.43)|
|f4|15|11 (73.33)|
|f5|15|11 (73.33)|
|n1|8|4 (50.0)|
|n2|10|5 (50.0)|
|n3|9|4 (44.44)|
|n4<br>|9|4 (44.44)<br>|
|n5|60|9 (15.0)|
|z1|10|4 (40.0)|
|z2|10|5 (50.0)|
|z3|54|25 (46.3)|
|t1|16|6 (37.5)|
|t2|16|6 (37.5)|
|t3|3|1 (33.33)|
|t4<br>|16<br>|6 (37.5)<br>|
|t5|16|6 (37.5)|



Table 5: MMIO detection analysis highlights potential undocumented peripherals in SVD files. SVD Detection shows documented MMIOs, while Potential MMIOs indicates detected MMIOs that may represent undocumented peripherals. 

indicators of potentially buggy functions. Depending on the target, this process typically leaves us with roughly 100-150 functions per application for further fuzzing. 

### **5.4.2 Results** 

Table 2 shows the code coverage and bug detection results when conducting whole program ( _M_ 2) and function-level 

11 

( _M_ 3) fuzzing. Using LEMIX, we conducted whole program and function-level fuzzing on 15 applications each. We manually created the memory layout for z1 as a demonstration but did not perform whole-program fuzzing for z2, z3, and t3 due to their layout-dependent code, which is not automated (§ 6). We did not perform function-level fuzzing on f1, f2, and n5 as they were written in C++, and our current implementation of function-level fuzzing does not support C++ objects. 

**_Code Coverage:_** In whole program fuzzing, we triggered a considerable number of reachable functions ( _i.e.,_ those that can be reached through main) in each LEAPP. Figure 5 shows the percentage of triggered functions, with over 70% triggered on average, except for f2, f3, and z1. The Cumulative Distribution Function (CDF) in Figure 5 illustrates function coverage, where each point ( _x, y_ ) indicates that _x_ % of triggered functions have _y_ % or less code coverage. The consistent slope across LEAPPs confirms that LEMIX enables effective testing with reasonable coverage. For example, in FreeRTOS LEAPPs, 40% of triggered functions achieve 40% or more code coverage. Table 2 shows absolute coverage, with function-level fuzzing providing _∼_ 10x more coverage than whole-program fuzzing, as it targets individual functions. 

**_Bug Detection:_** Table 2 also shows the bugs detected by each approach. Overall, as expected, function level fuzzing ( _M_ 3) identified 11 additional unique bugs. This is due to its ability to directly exercise risky functions. As shown in Listing 1, function-level fuzzing ( _M_ 3) uncovered an out-of-bounds access in a deep function that whole-program fuzzing ( _M_ 2) missed, as the function was never triggered. 

As shown in the last row of Table 2, although total bugs are large ( _e.g.,_ 28), the number of unique bugs is small ( _e.g.,_ 11). This is because the same bugs (those in RTOS functions) could be present multiple in LEAPPs. More details can be found in § F.1 (Appendix). Table 8 (Appendix) summarizes the bug types, affected applications, bug descriptions, and developer responses. The Table 9 (Appendix) shows a detailed split of bugs and unique bugs. The Table 10 (Appendix) provides the categorization of unique bugs. We found several memory corruption bugs in addition to robustness bugs, such as Divide by zero (Listing 2). 

RQ3 results demonstrate that LEMIX facilitates wholeprogram and function-level fuzzing, leading to high code coverage and bug detection. 

## **5.5 RQ4: Ablation Study** 

### **5.5.1 Methodology** 

This RQ measures the contributions of our peripheral handling (§ 4.1.4) and condition weakening (§ 4.1.5) instrumentation in facilitating dynamic analysis. We disabled each of these instrumentations and report their impact on wholeprogram fuzzing. While function-level fuzzing performed 

better, whole-program fuzzing compensated for the limitations of function-level fuzzing on C++ applications and provided insights into how effectively a LEAPP can be tested as a standalone application. 

### **5.5.2 Results** 

**_Peripheral handling instrumentations:_** When the instrumentations on MMIO accesses are disabled, we observed that all LEAPPs crash immediately after they are started. As mentioned before, LEAPPs are fuzzed as regular Linux applications, in which MMIO addresses may not be mapped; consequently, any MMIO accesses will result in invalid memory access and segfault. This shows that _our peripheral handling instrumentation is necessary for testing_ LEAPP _s_ . 

**_Condition weakening instrumentation:_** When the instrumentations that weaken state-dependent conditions are disabled, we observe a remarkable drop in the number of covered basic blocks. The **M1** and **M2** columns in Table 2 shows the number of covered basic blocks and bugs found when conducting whole-program fuzzing without and with this instrumentation. On average, we see an improvement of _∼_ 2x in the number of basic blocks covered with M2 over M1. All bugs found by M1 were also detected by M2, with the addition of 7 more bugs. These results show that embedded applications greatly depend on the peripheral state for their execution, and ignoring them results in ineffective testing. 

RQ4 results show that our instrumentation-based techniques significantly improve the effectiveness of testing. 

## **5.6 RQ5: Comparative Evaluation** 

### **5.6.1 Methodology** 

In this RQ, we compare the code coverage and bug detection results of LEMIX with results from other recent dynamic analysis techniques that target embedded applications. We selected baselines that follow the LEMIX’s philosophy of being usable on applications without requiring low-level understanding of the application’s internal implementation. This led to three baselines: P2IM [39], Fuzzware ( _Fw_ ) [82] and MultiFuzz ( _M f_ ) [28], and the exclusion of three others: PMCU [56], Halucinator [30] and SAFIREFUZZ [83]. Notably, PMCU required a custom RTOS configuration for each application based on the application’s internal implementation. Halucinator and SAFIREFUZZ require creating handlers for each peripheral the application interacted with. 

We were unable to set up P2IM, despite following their instructions and attempting to contact the authors. Additionally, we encountered challenges setting up fuzzing for certain applications ( _e.g.,_ f3, z3) using Fuzzware and Multifuzz, primarily due to inaccurate memory modeling, resulting in applications crashing with unsupported or invalid instructions. 

12 


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0013-00.png)


<!-- Start of picture text -->
FreeRTOS Nuttx Zephyr Threadx<br>1 1 1 1<br>f1 (83.33%) n1 (84.42%) z1 (15.62%) t1 (77.78%)<br>0 . 8 f2 (30.62%) 0 . 8 n2 (95.24%) 0 . 8 0 . 8 t2 (78.95%)<br>f3 (22.02%) n3 (92.68%) t4 (78.95%)<br>f4 (62.50%) n4 (92.68%) t5 (66.67%)<br>0 . 6 f5 (76.25%) 0 . 6 n5 (93.34%) 0 . 6 0 . 6<br>0 . 4 0 . 4 0 . 4 0 . 4<br>0 . 2 0 . 2 0 . 2 0 . 2<br>0 0 0 0<br>0 20 40 60 80 100 0 20 40 60 80 100 0 20 40 60 80 100 0 20 40 60 80 100<br>Triggered Functions (%) Triggered Functions (%) Triggered Functions (%) Triggered Functions (%)<br>Function Coverage (%) Function Coverage (%) Function Coverage (%) Function Coverage (%)<br><!-- End of picture text -->

Figure 5: Cumulative Distribution Functions (CDFs) of function coverage across various applications. Each line represents an application’s coverage distribution in app-level fuzzing, illustrating the proportion of functions (x-axis) that achieve at most a given coverage percentage (y-axis). 

Consequently, we evaluated Fuzzware and Multifuzz on the remaining original, non-converted LEAPPs. 

### **5.6.2 Results** 

Table 2 shows the results of fuzzing each LEAPP with the selected baselines. We found that, on average, LEMIX configurations (M2/M3) detected 21 bugs, while Multifuzz ( _Mf_ ) and Fuzzware ( _Fw_ ) detected 1 and 3 bugs, respectively. From a code coverage perspective, _Mf_ outperformed _Fw_ for most applications. However, LEMIX configurations (M2/M3) outperformed _Mf_ for most applications except for n1 and z2. This was primarily due to _Mf_ ’s ability to trigger nested interrupts, which led to higher coverage. In contrast, LEMIX uses a simpler interrupt handling approach (§ 4.1.4) and does not support nested interrupts. We also observed that _Fw_ occasionally reported false positives, such as crashes in z1, caused by incorrect interrupt handling. From the bug detection perspective, LEMIX is even more effective by detecting 21 bugs, with Fuzzware and MultiFuzz detecting only 1 and 3 respectively. Furthermore, all bugs found by Fuzzware and MultiFuzz are also found by LEMIX. 

RQ5 results indicate that LEMIX has better bug-finding ability than existing techniques. 

## **5.7 RQ6: False Positive Analysis** 

### **5.7.1 Methodology** 

This RQ aims to analyze false positives that arise due to our low-fidelity approximations, how they compare with existing works, and provide remediation for each type of false positive. Our analysis covers the LEMIX components that introduce approximations, as these are the sources of false positives. 

### **5.7.2 Results** 

Table 6 summarizes the number and type of false positives encountered across various applications. 

|**AppID**|**Inline ASM**<br>**Interrupt Misfring**<br>**B**|**oard Layout**|
|---|---|---|
|f1|1<br>1|0|
|f2|1<br>3|0|
|z2|0<br>0|1|
|z3|0<br>0|1|
|t2|0<br>1|1|
|**Total**|**2**<br>**5**|**3**|



Table 6: False positives due to LEMIX approximations. 

**_POSIX Swap (§ 4.1.1):_** LEMIX replaces the board-specific RTOS layer with a POSIX-compatible one. While this can introduce false positives due to kernel misconfiguration, we observed none in our case. For example, incorrect task priorities could affect behavior, but we mitigated this by incorporating all relevant application kernel configurations. 

**_Inline ASM (§ 4.1.2):_** LEMIX removes all inline assembly and approximates expected values at runtime using random values of the same type This led to two false positives across all applications. For instance, Listing 5 (Appendix) shows how inline assembly was used for initialization, which we identified through debugger-inspected halts. We resolved this by manually patching the instruction to return the expected value. 

**_Symbol Modifications (§ 4.1.3):_** Our symbol modification strategy iteratively resolves linker errors and could, in principle, introduce false positives such as from incorrect renaming of indirect function calls. However, we observed none. 

**_Interrupt Misfiring (§ 4.1.4)_** : LEMIX attempts to trigger all interrupts from the _isr_vector_table_ , which can cause crashes if global structures containing callback routines are uninitialized. For example, Listing 9 (Appendix) shows a misfired interrupt caused by this dependency. We remediate using lightweight static analysis to trigger interrupts accurately. 

**_Board Layout (§ 6):_** Board-specific layout-dependent code is a limitation of our work, preventing analysis of two Zephyr and one ThreadX applications. An example of this issue is shown in Listing 8. We manually constructed the layout for one Zephyr application for our evaluation. 

13 

The existing tools used in our Comparative Evaluation (§ 5.6) also suffer from false positives due to misfired interrupts and emulation issues. In contrast to LEMIX, these tools had a greater number of false positive crashes, as indicated by the large numbers along the crash column of Table 2. Furthermore, triaging these crashes (especially in the case of Fuzzware ( _Fw_ )) is non-trivial, and has also been acknowledged by recent work [25]. LEMIX adopts an approximate but principled approach, enabling us to easily identify false positives and resolve them. 

RQ6 results indicate that the lower-fidelity execution model used by LEMIX does not lead to a large number of false positives, as evidenced by our comparative evaluation. 

## **6 Limitations and Future Work** 

We recognize the following limitations of LEMIX and plan to handle them as part of our future work. 

- **Dependency on LPL:** Our approach depends on the existence of LPL for RTOSes. As shown in Appendix B.0.3, most RTOSes already have LPL, we argue that it is fairly easy to create LPL based on existing implementations. 

- **Incomplete ISR coverage:** Our approach identifies ISRs via RTOS-specific pattern matching, which worked reliably in our experiments. However, we skip ISRs that depend on global state, leading to some coverage gaps. Recent works like AIM [38] improves ISR identification and invocation, and we plan to incorporate such techniques into LEMIX in future work. 

- **Unable to handle layout-specific code:** We found cases where embedded applications rely on specific memory layouts, hindering our efforts in further analysis. Listing 8 (Appendix) shows an example from a Zephyr RTOS application. As future work, we plan to automatically detect and refactor such code idioms. 

## **7 Related Work** 

Dynamic analysis techniques, especially automated random testing or fuzzing [42, 65], are demonstrated to be effective at vulnerability detection. _Rehosting_ is a necessary requirement for scalable dynamic analysis. This process is relatively easy for Type-1 systems [26, 58], _i.e.,_ those based on standard OSes such as Embedded Linux. Consequently, several techniques [37] exist for rehosting Type-1 systems. But, these cannot be applied to Type-2 systems because of lack of welldefined OS interface and tight coupling with hardware [37]. 

based approaches. The hardware-in-the-loop approaches [32, 43,46,47,50,55,68,80] achieve the highest level of fidelity and less manual effort. Given the diversity of hardware platforms, these techniques are hard to scale. 

The software-only approaches [39, 48, 82, 93, 106] provide low-fidelity execution unless there are precise peripheral models. Automated peripheral modeling techniques [30,39,44,91] are specific to certain peripherals and hard to generalize. Some techniques [32,82] use symbolic execution [3] to create peripheral models. As shown by the recent systematization work [37], these techniques are hard to extend for different peripherals and depend on the existence of emulators [4, 63] of the corresponding ISA. On the other hand, works such as METAEMU [27] attempt to rehost firmware in an architectureagnostic way by lifting firmware code to an Intermediate Representation as directed by Ghidra’s Language Specifications [79] enabling multi-target analysis. However, these techniques struggle with manual efforts required for specification creation, peripheral modeling, and limited support for specialized automotive protocols. 

One of the most closely related works is by Li _et al.,_ [56], who rehost MCU libraries for testing on Linux by implementing a portable MCU (PMCU) using the POSIX interface and abstracting hardware functions. However, their method relies on hand-written abstractions for specific libraries and does not handle unknown or undocumented peripherals, nor does it scale well across diverse firmware binaries. LEMIX side-steps the problem of precise peripheral emulation by using NPL, which relaxes the requirement of precise peripheral models without affecting the execution of the target embedded system. Unlike prior works that require accurate peripheral models or emulation for specific hardware targets, our approach generalizes across firmware by focusing on what is sufficient to trigger bugs, rather than replicating exact hardware behavior. As a result, dynamic analysis can be applied to embedded code in a more generalizable manner. 

## **8 Conclusion** 

We propose LEMIX, a novel approach to rehosting embedded applications as Linux applications by providing solutions to the associated challenges of retargeting to X86, preserving the execution semantics, and handling the peripheral interactions. We evaluated LEMIX on 18 embedded applications across four RTOSes and found 21 previously unknown bugs, most of which are confirmed and fixed by the corresponding developers. Our comparative evaluation shows that LEMIX outperforms existing state-of-the-art techniques in testing embedded applications. 

One of the most important challenges of Rehosting Type2 systems is the capability to handle peripheral interactions. Existing techniques to handle this can be categorized at a high level into hardware-in-the-loop [47] or software model [91] 

14 

_The call for papers states that an extra page is allotted to discuss ethics considerations and compliance with the open science policy. This page contains that content._ 

## **10 Open Science** 

We have released a raw development version of LEMIX along with the dataset and necessary documentation at : https: //zenodo.org/records/15611391. 

## **9 Ethics Considerations** 

This section describes the ethical considerations involved in designing, implementing, and evaluating our proposed system. We identify two relevant classes of stakeholders in this work. 

- Maintainers of the RTOSes and embedded applications on which we evaluated. 

- Users of the RTOSes and embedded applications on which we evaluated. 

These stakeholders share in the following risks and benefits: 

- _Risks and benefits from discovered bugs:_ To evaluate LEMIX, we applied it to 18 applications and uncovered 21 distinct defects in both the applications and the underlying RTOSes. Under our threat model, these defects could lead to malfunctions or crashes in the affected software. We reported all identified issues to the respective vendors and provided GitHub patches to facilitate their resolution. In our assessment, we did not perceive these defects posed a security threat, so we followed the projects’ standard defect disclosure processes (public issue reports) rather than their security vulnerability disclosure processes. Most of the _maintainers_ acknowledged the reported bugs, and our proposed patches were accepted and merged. In consequence, any _users_ who do not update to the latest versions may face a security risk if attackers can exploit these bugs. 

- _Risks and benefits from the existence of_ LEMIX _:_ Beyond our evaluation, LEMIX will be an open-source tool (see §10). Like any defect discovery tool, LEMIX can be used by maintainers and users in good faith, or abused by malicious actors seeking vulnerabilities to exploit. 

These stakeholders and risks/benefits are common to all defect detection systems, _e.g.,_ the fuzzing literature. The cybersecurity research community understands this risk-benefit tradeoff to fall within the scope of ethical practice for cybersecurity research. 

To further mitigate any potential risks, we submitted patches with each bug report, to help the developers fix the vulnerabilities promptly. None of the affected vendors assessed the reported issues as having significant security implications — our patches were typically merged but no CVEs were issued. 

## **11 Acknowledgments** 

We would like to thank the reviewers and our shepherd for their valuable comments and inputs to improve our paper. This research was supported by Rolls-Royce and the National Science Foundation (NSF) under Grant CNS-2340548. Any opinions, findings, conclusions, or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of Rolls-Royce and NSF. 

## **References** 

- [1] ar(1) - Linux man page. 

- [2] FreeRTOS. http://freertos.org. 

- [3] KLEE. 

- [4] Qemu. https://www.qemu.org/. 

- [5] Real Time Operating System (RTOS) | Microsoft Azure — azure.microsoft.com. https://azure. microsoft.com/en-us/products/rtos. [Accessed 07-02-2024]. 

- [6] Rust4embedded bug survey. https://docs.google. com/spreadsheets/d/e/2PACX-1vQndSwy_ CDJFeUCkc1PdUjF2j_q8eijUeRl8tjkM_ C4D7mkGAK-QJssO9j9JtIT8lSYfBNKg9-QUG7p/ pubhtml. 

- [7] SafeRTOS - an independently certified kernel for safety critical applications IEC61508 EN62304 and FDA 510(k) — freertos.org. https://www.freertos.org/FreeRTOS-Plus/ Safety_Critical_Certified/SafeRTOS.html. [Accessed 16-02-2024]. 

- [8] Semiconductor Partners - FreeRTOS — freertos.org. https://www.freertos.org/partners/ semiconductor.html. [Accessed 07-02-2024]. 

- [9] Supported platforms 2014; nuttx latest documentation — nuttx.apache.org. https://nuttx.apache. org/docs/10.0.1/introduction/supported_ platforms.html. [Accessed 07-02-2024]. 

- [10] SVD Description (*.svd) Format. 

- [11] URGENT/11. https://www.armis.com/research/ urgent11/. 

15 

- [12] VxWorks Safety Platforms — windriver.com. https://www.windriver.com/products/ vxworks/safety-platforms. [Accessed 1602-2024]. 

- [13] Zephyr Project | Ecosystem Vendors — zephyrproject.org. https://zephyrproject.org/ ecosystem-vendor-offerings/. [Accessed 07-02-2024]. 

- [14] ZephyrRTOS. https://zephyrproject.org/. 

- [15] Mohammed Ali Al-Garadi, Amr Mohamed, Abdulla Khalid Al-Ali, Xiaojiang Du, Ihsan Ali, and Mohsen Guizani. A Survey of Machine and Deep Learning Methods for Internet of Things (IoT) Security. _IEEE Communications Surveys & Tutorials_ , 2020. 

- [16] Fadi Al-Turjman and Joel Poncha Lemayian. Intelligence, security, and vehicular sensor networks in internet of things (iot)-enabled smart-cities: An overview. _Computers & Electrical Engineering_ , 2020. 

- [17] Omar Alrawi, Chaz Lever, Manos Antonakakis, and Fabian Monrose. SoK: Security Evaluation of HomeBased IoT Deployments. _2019 IEEE Symposium on Security and Privacy_ , 2019. 

- [18] Manos Antonakakis, Tim April, Michael Bailey, Matt Bernhard, Elie Bursztein, Jaime Cochran, Zakir Durumeric, J Alex Halderman, Luca Invernizzi, Michalis Kallitsis, et al. Understanding the mirai botnet. In _26th {USENIX} security symposium ({USENIX} Security 17)_ , 2017. 

- [19] ARM-software. Svd files: Missing the core peripherals · issue #844 · arm-software/cmsis_5. https://github.com/ARM-software/CMSIS_5/ issues/844. Accessed: 2025-01-20. 

- [20] Miguel A Arroyo. Bespoke security for resource constrained cyber-physical systems. In _ProQuest Dissertations and Theses_ , page 171. Columbia University, 2021. Accessed 15 Feb. 2023. 

- [21] Domagoj Babi´c, Stefan Bucur, Yaohui Chen, Franjo Ivanˇci´c, Tim King, Markus Kusano, Caroline Lemieux, László Szekeres, and Wei Wang. Fudge: Fuzz driver generation at scale. In _Proceedings of the 2019 27th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering_ , 2019. 

- [22] Roberto Bagnara, Abramo Bagnara, and Patricia M Hill. The misra c coding standard and its role in the development and analysis of safety-and security-critical embedded software. In _International Static Analysis Symposium_ , 2018. 

- [23] Katharina Bogad and Manuel Huber. Harzer roller: Linker-based instrumentation for enhanced embedded security testing. In _Proceedings of the 3rd Reversing and Offensive-Oriented Trends Symposium_ , 2020. 

- [24] Marcel Böhme, Cristian Cadar, and Abhik Roychoudhury. Fuzzing: Challenges and reflections. _IEEE Software_ , 38(3):79–86, 2021. 

- [25] Boyu Chang, Binbin Zhao, Qiao Zhang, Peiyu Liu, Yuan Tian, Raheem Beyah, and Shouling Ji. FirmRCA: Towards Post-Fuzzing Analysis on ARM Embedded Firmware with Efficient Event-based Fault Localization . In _2025 IEEE Symposium on Security and Privacy (SP)_ , 2025. 

- [26] Daming D. Chen, Maverick Woo, David Brumley, and Manuel Egele. Towards automated dynamic analysis for linux-based embedded firmware. In _23rd Annual Network and Distributed System Security Symposium, NDSS 2016, San Diego, California, USA, February 2124, 2016_ . The Internet Society, 2016. 

- [27] Zitai Chen, Sam L Thomas, and Flavio D Garcia. Metaemu: An architecture agnostic rehosting framework for automotive firmware. In _Proceedings of the 2022 ACM SIGSAC Conference on Computer and Communications Security_ , 2022. 

- [28] Michael Chesser, Surya Nepal, and Damith C. Ranasinghe. MultiFuzz: A Multi-Stream fuzzer for testing monolithic firmware. In _33rd USENIX Security Symposium (USENIX Security 24)_ , 2024. 

- [29] Jaeseung Choi, Joonun Jang, Choongwoo Han, and Sang Kil Cha. Grey-box concolic testing on binary code. In _2019 IEEE/ACM 41st International Conference on Software Engineering (ICSE)_ , 2019. 

- [30] Abraham A. Clements, Eric Gustafson, Tobias Scharnowski, Paul Grosen, David Fritz, Christopher Kruegel, Giovanni Vigna, Saurabh Bagchi, and Mathias Payer. HALucinator: firmware re-hosting through abstraction layer emulation. In _Proceedings of the 29th USENIX Conference on Security Symposium_ , 2020. 

- [31] Jake Corina, Aravind Machiry, Christopher Salls, Yan Shoshitaishvili, Shuang Hao, Christopher Kruegel, and Giovanni Vigna. Difuze: Interface aware fuzzing for kernel drivers. In _Proceedings of the 2017 ACM SIGSAC Conference on Computer and Communications Security_ , 2017. 

- [32] Nassim Corteggiani, Giovanni Camurati, and Aurélien Francillon. Inception: System-Wide security testing of Real-World embedded systems software. In _27th USENIX Security Symposium (USENIX Security 18)_ , 2018. 

16 

- [33] Drew Davidson, Benjamin Moench, Thomas Ristenpart, and Somesh Jha. _{_ FIE _}_ on firmware: Finding vulnerabilities in embedded systems using symbolic execution. In _22nd USENIX Security Symposium (USENIX Security 13)_ , 2013. 

- [34] Daniele Cono D’Elia, Emilio Coppa, Simone Nicchi, Federico Palmaro, and Lorenzo Cavallaro. Sok: Using dynamic binary instrumentation for security (and how you may get caught red handed). In _Proceedings of the 2019 ACM Asia Conference on Computer and Communications Security_ , 2019. 

- [35] dgookin. Not every compiler likes your code | c for dummies blog, Jan 2023. 

- [36] Xiaoning Du, Bihuan Chen, Yuekang Li, Jianmin Guo, Yaqin Zhou, Yang Liu, and Yu Jiang. Leopard: Identifying vulnerable code for vulnerability assessment through program metrics. In _2019 IEEE/ACM 41st International Conference on Software Engineering (ICSE)_ , 2019. 

- [37] Andrew Fasano, Tiemoko Ballo, Marius Muench, Tim Leek, Alexander Bulekov, Brendan Dolan-Gavitt, Manuel Egele, Aurélien Francillon, Long Lu, Nick Gregory, et al. Sok: Enabling security analyses of embedded systems via rehosting. In _Proceedings of the 2021 ACM Asia conference on computer and communications security (AsiaCCS)_ , 2021. 

- [38] Bo Feng, Meng Luo, Changming Liu, Long Lu, and Engin Kirda. Aim: Automatic interrupt modeling for dynamic firmware analysis. _IEEE Transactions on Dependable and Secure Computing_ , 2024. 

- [39] Bo Feng, Alejandro Mera, and Long Lu. P2IM: Scalable and hardware-independent firmware testing via automatic peripheral interface modeling. In _29th USENIX Security Symposium (USENIX Security 20)_ , 2020. 

- [40] Jian Gao, Yiwen Xu, Yu Jiang, Zhe Liu, Wanli Chang, Xun Jiao, and Jiaguang Sun. Em-fuzz: Augmented firmware fuzzing via memory checking. _IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems_ , 2020. 

- [41] Vahid Garousi, Michael Felderer, Ça˘grı Murat Karapıçak, and U˘gur Yılmaz. Testing embedded software: A survey of the literature. _Information and Software Technology_ , 2018. 

- [42] Patrice Godefroid. Fuzzing: Hack, art, and science. _Communications of the ACM_ , 2020. 

- [43] Zhijie Gui, Hui Shu, Fei Kang, and Xiaobing Xiong. Firmcorn: Vulnerability-oriented fuzzing of iot firmware via optimized virtual execution. _IEEE Access_ , 8:29826–29841, 2020. Publisher: IEEE. 

- [44] Eric Gustafson, Marius Muench, Chad Spensky, Nilo Redini, Aravind Machiry, Yanick Fratantonio, Davide Balzarotti, Aurélien Francillon, Yung Ryn Choe, Christophe Kruegel, and Giovanni Vigna. Toward the analysis of embedded firmware through automated rehosting. In _22nd International Symposium on Research in Attacks, Intrusions and Defenses (RAID 2019)_ , 2019. 

- [45] Thomas A Henzinger and Joseph Sifakis. The embedded systems design challenge. In _FM 2006: Formal Methods: 14th International Symposium on Formal Methods, Hamilton, Canada, August 21-27, 2006. Proceedings 14_ , 2006. 

- [46] Markus Kammerstetter, Daniel Burian, and Wolfgang Kastner. Embedded security testing with peripheral device caching and runtime program state approximation. In _10th International Conference on Emerging Security Information, Systems and Technologies (SECUWARE)_ , 2016. 

- [47] Markus Kammerstetter, Christian Platzer, and Wolfgang Kastner. Prospect: peripheral proxying supported embedded code testing. In _Proceedings of the 9th ACM symposium on Information, computer and communications security_ , 2014. 

- [48] Mingeun Kim, Dongkwan Kim, Eunsoo Kim, Suryeon Kim, Yeongjin Jang, and Yongdae Kim. Firmae: Towards large-scale emulation of iot firmware for dynamic analysis. _Annual Computer Security Applications Conference_ , 2020. 

- [49] George Klees, Andrew Ruef, Benji Cooper, Shiyi Wei, and Michael Hicks. Evaluating fuzz testing. In _Proceedings of the 2018 ACM SIGSAC conference on computer and communications security_ , 2018. 

- [50] Karl Koscher, Tadayoshi Kohno, and David Molnar. {SURROGATES}: Enabling {Near-Real-Time} Dynamic Analyses of Embedded Systems. In _9th USENIX Workshop on Offensive Technologies (WOOT 15)_ , 2015. 

- [51] Tamás Kovácsházy, Gábor Wacha, Tamás Dabóczi, Csanád Erd˝os, and Attila Szarvas. System architecture for internet of things with the extensive use of embedded virtualization. In _2013 IEEE 4th International Conference on Cognitive Infocommunications (CogInfoCom)_ , 2013. 

- [52] Tomasz Kuchta and Bartosz Zator. Auto off-target: Enabling thorough and scalable testing for complex software systems. In _Proceedings of the 37th IEEE/ACM International Conference on Automated Software Engineering_ , 2023. 

17 

- [53] Sekar Kulandaivel, Shalabh Jain, Jorge Guajardo, and Vyas Sekar. Cannon: Reliable and stealthy remote shutdown attacks via unaltered automotive microcontrollers. In _2021 IEEE Symposium on Security and Privacy (SP)_ , 2021. 

- [54] Chongqing Lei, Zhen Ling, Yue Zhang, Yan Yang, Junzhou Luo, and Xinwen Fu. A friend’s eye is a good mirror: Synthesizing _{_ MCU _}_ peripheral models from peripheral drivers. In _33rd USENIX Security Symposium (USENIX Security 24)_ , 2024. 

- [55] Hao Li, Dong Tong, Kan Huang, and Xu Cheng. FEMU: A firmware-based emulation framework for SoC verification. In _Proceedings of the eighth IEEE/ACM/IFIP international conference on Hardware/software codesign and system synthesis_ , 2010. 

- [56] Wenqiang Li, Le Guan, Jingqiang Lin, Jiameng Shi, and Fengjun Li. From library portability to pararehosting: Natively executing microcontroller software on commodity hardware. _arXiv preprint arXiv:2107.12867_ , 2021. 

- [57] Jay P Lim and Santosh Nagarakatte. Automatic equivalence checking for assembly implementations of cryptography libraries. In _2019 IEEE/ACM International Symposium on Code Generation and Optimization (CGO)_ , 2019. 

- [58] Qiang Liu, Cen Zhang, Lin Ma, Muhui Jiang, Yajin Zhou, Lei Wu, Wenbo Shen, Xiapu Luo, Yang Liu, and Kui Ren. Firmguide: Boosting the capability of rehosting embedded linux kernels through model-guided kernel execution. In _2021 36th IEEE/ACM International Conference on Automated Software Engineering (ASE)_ , 2021. 

- [59] Yuwei Liu, Yanhao Wang, Xiangkun Jia, Zheng Zhang, and Purui Su. Afgen: Whole-function fuzzing for applications and libraries. In _2024 IEEE Symposium on Security and Privacy (SP)_ , 2024. 

- [60] Zheyu Ma, Bodong Zhao, Letu Ren, Zheming Li, Siqi Ma, Xiapu Luo, and Chao Zhang. Printfuzz: Fuzzing linux drivers via automated virtual device simulation. In _Proceedings of the 31st ACM SIGSOFT International Symposium on Software Testing and Analysis_ , 2022. 

- [61] Aravind Machiry, John Kastner, Matt McCutchen, Aaron Eline, Kyle Headley, and Michael Hicks. C to checked c by 3c. _Proceedings of the ACM on Programming Languages_ , 2022. 

- [62] Aravind Machiry, Chad Spensky, Jake Corina, Nick Stephens, Christopher Kruegel, and Giovanni Vigna. 

   - Dr. checker: a soundy analysis for linux kernel drivers. In _Proceedings of the 26th USENIX Conference on Security Symposium_ , 2017. 

- [63] P.S. Magnusson, M. Christensson, J. Eskilson, D. Forsgren, G. Hallberg, J. Hogberg, F. Larsson, A. Moestedt, and B. Werner. Simics: A full system simulation platform. _Computer_ , 2002. 

- [64] Valentin JM Manès, HyungSeok Han, Choongwoo Han, Sang Kil Cha, Manuel Egele, Edward J Schwartz, and Maverick Woo. The art, science, and engineering of fuzzing: A survey. _IEEE Transactions on Software Engineering_ , 2019. 

- [65] Valentin J.M. Manès, HyungSeok Han, Choongwoo Han, Sang Kil Cha, Manuel Egele, Edward J. Schwartz, and Maverick Woo. The art, science, and engineering of fuzzing: A survey. _IEEE Transactions on Software Engineering_ , 2021. 

- [66] Joel Margolis, Tae Tom Oh, Suyash Jadhav, Young Ho Kim, and Jeong Neyo Kim. An in-depth analysis of the mirai botnet. In _2017 International Conference on Software Security and Assurance (ICSSA)_ , 2017. 

- [67] Trevor Martin. _The designer’s guide to the Cortex-M processor family_ . Newnes, 2016. 

- [68] Marius Muench, Dario Nisi, Aurélien Francillon, and Davide Balzarotti. Avatar 2: A multi-target orchestration platform. In _Proc. Workshop Binary Anal. Res.(Colocated NDSS Symp.)_ , volume 18, 2018. 

- [69] Marius Muench, Jan Stijohann, Frank Kargl, Aurélien Francillon, and Davide Balzarotti. What you corrupt is not what you crash: Challenges in fuzzing embedded devices. In _Network and Distributed System Security Symposium (NDSS)_ , 2018. 

- [70] Arif Ali Mughal. The art of cybersecurity: Defense in depth strategy for robust protection. _International Journal of Intelligent Automation and Computing_ , 1(1):1– 20, 2018. 

- [71] Aniruddhan Murali, Noble Mathews, Mahmoud Alfadel, Meiyappan Nagappan, and Meng Xu. Fuzzslice: Pruning false positives in static analysis warnings through function-level fuzzing. In _Proceedings of the 46th IEEE/ACM International Conference on Software Engineering_ , pages 1–13, 2024. 

- [72] Eoin O’driscoll and Garret E O’donnell. Industrial power and energy metering–a state-of-the-art review. _Journal of Cleaner Production_ , 2013. 

- [73] osrtos. List of open source real-time operating systems. https://www.osrtos.com/, 2023. 

18 

- [74] Hui Peng, Yan Shoshitaishvili, and Mathias Payer. T- fuzz: fuzzing by program transformation. In _2018 IEEE Symposium on Security and Privacy (SP)_ , 2018. 

- [75] Dipika Roy Prapti, Abdul Rashid Mohamed Shariff, Hasfalina Che Man, Norulhuda Mohamed Ramli, Thinagaran Perumal, and Mohamed Shariff. Internet of things (iot)-based aquaculture: An overview of iot application on water quality monitoring. _Reviews in Aquaculture_ , 2022. 

- [76] Polyvios Pratikakis, Jeffrey S. Foster, and Michael Hicks. Locksmith: context-sensitive correlation analysis for race detection. _SIGPLAN Not._ , June 2006. 

- [77] Edwin D Reilly. Memory-mapped i/o. In _Encyclopedia of Computer Science_ , pages 1152–1152. 2003. 

- [78] Rizsotto. GitHub - rizsotto/Bear: Bear is a tool that generates a compilation database for clang tooling. 

- [79] Roman Rohleder. Hands-on ghidra-a tutorial about the software reverse engineering framework. In _Proceedings of the 3rd ACM Workshop on Software Protection_ , 2019. 

- [80] Jan Ruge, Jiska Classen, Francesco Gringoli, and Matthias Hollick. Frankenstein: Advanced wireless fuzzing to exploit new bluetooth escalation targets. In _Proceedings of the 29th USENIX Conference on Security Symposium_ , 2020. 

- [81] Michael Rüegg and Peter Sommerlad. Refactoring towards seams in c++. In _2012 7th International Workshop on Automation of Software Test (AST)_ , 2012. 

- [82] Tobias Scharnowski, Nils Bars, Moritz Schloegel, Eric Gustafson, Marius Muench, Giovanni Vigna, Christopher Kruegel, Thorsten Holz, and Ali Abbasi. Fuzzware: Using precise MMIO modeling for effective firmware fuzzing. In _31st USENIX Security Symposium (USENIX Security 22)_ , 2022. 

- [83] Lukas Seidel, Dominik Christian Maier, and Marius Muench. Forming faster firmware fuzzers. In _USENIX Security Symposium_ , 2023. 

- [84] Konstantin Serebryany, Derek Bruening, Alexander Potapenko, and Dmitriy Vyukov. AddressSanitizer: A fast address sanity checker. In _2012 USENIX Annual Technical Conference (USENIX ATC 12)_ , 2012. 

- [85] Ayushi Sharma, Shashank Sharma, Santiago TorresArias, and Aravind Machiry. Rust for embedded systems: current state, challenges and open problems. _arXiv preprint arXiv:2311.05063_ , 2023. 

- [86] Ayushi Sharma, Shashank Sharma, Santiago TorresArias, and Aravind Machiry. Rust for embedded systems: Current state, challenges and open problems. In _Proceedings of the 31st ACM Conference on Computer and Communications Security (CCS)_ , 2024. 

- [87] Mingjie Shen. Finding 709 defects in 258 projects: An experience report on applying codeql to open-source embedded software (experience paper) (issta 2025 - research papers) - issta 2025. _ISSTA 2025_ , 2025. 

- [88] Mingjie Shen, James C. Davis, and Aravind Machiry. Towards automated identification of layering violations in embedded applications (wip). In _Proceedings of the 24th ACM SIGPLAN/SIGBED International Conference on Languages, Compilers, and Tools for Embedded Systems_ , 2023. 

- [89] Dokyung Song, Julian Lettner, Prabhu Rajasekaran, Yeoul Na, Stijn Volckaert, Per Larsen, and Michael Franz. SoK: Sanitizing for security. In _2019 IEEE Symposium on Security and Privacy (S&P)_ , 2019. 

- [90] NB Soni and Jaideep Saraswat. A review of iot devices for traffic management system. In _2017 international conference on intelligent sustainable systems (ICISS)_ , 2017. 

- [91] Chad Spensky, Aravind Machiry, Nilo Redini, Colin Unger, Graham Foster, Evan Blasband, Hamed Okhravi, Christopher Kruegel, and Giovanni Vigna. Conware: Automated modeling of hardware peripherals. In _Proceedings of the 2021 ACM Asia conference on computer and communications security (AsiaCCS)_ , 2021. 

- [92] Jayashree Srinivasan, Sai Ritvik Tanksalkar, Paschal C Amusuo, James C Davis, and Aravind Machiry. Towards rehosting embedded applications as linux applications. In _2023 53rd Annual IEEE/IFIP International Conference on Dependable Systems and NetworksSupplemental Volume (DSN-S)_ , 2023. 

- [93] Prashast Srivastava, Hui Peng, Jiahao Li, Hamed Okhravi, Howard E. Shrobe, and Mathias Payer. Firmfuzz: Automated iot firmware introspection and analysis. _Proceedings of the 2nd International ACM Workshop on Security and Privacy for the Internetof-Things_ , 2019. 

- [94] John A Stankovic and R Rajkumar. Real-time operating systems. _Real-Time Systems_ , 2004. 

- [95] Hui Jun Tay, Kyle Zeng, Jayakrishna Menon Vadayath, Arvind S Raj, Audrey Dutcher, Tejesh Reddy, Wil Gibbs, Zion Leonahenahe Basque, Fangzhou Dong, 

19 

Zack Smith, et al. Greenhouse: _{_ Single-Service _}_ rehosting of _{_ Linux-Based _}_ firmware binaries in _{_ UserSpace _}_ emulation. In _32nd USENIX Security Symposium (USENIX Security 23)_ , 2023. 

- [96] timlt. What is Microsoft Azure RTOS? — learn.microsoft.com. https://learn.microsoft. com/en-us/azure/rtos/overview-rtos. [Accessed 16-02-2024]. 

- [97] travitch. Whole Program LLVM. https://github. com/travitch/whole-program-llvm, 2015. 

- [98] William Von Hagen. _The definitive guide to GCC_ . Apress, 2011. 

- [99] Elecia White. _Making Embedded Systems: Design Patterns for Great Software_ . 2011. 

- [100] Christopher Wright, William A. Moeglein, Saurabh Bagchi, Milind Kulkarni, and Abraham A. Clements. Challenges in firmware re-hosting, emulation, and analysis. _ACM Comput. Surv._ , 2021. 

- [101] Guest Writer. The 5 Worst Examples of IoT Hacking and Vulnerabilities in Recorded History. https://www.iotforall.com/ 5-worst-iot-hacking-vulnerabilities, June 2020. 

- [102] Oualid Zaazaa and Hanan El Bakkali. Dynamic vulnerability detection approaches and tools: State of the art. In _2020 Fourth International Conference On Intelligent Computing in Data Sciences (ICDS)_ , 2020. 

- [103] Jonas Zaddach, Luca Bruno, Aurelien Francillon, Davide Balzarotti, et al. Avatar: A framework to support dynamic security analysis of embedded systems’ firmwares. In _NDSS_ , 2014. 

- [104] Mingrui Zhang, Jianzhong Liu, Fuchen Ma, Huafeng Zhang, and Yu Jiang. Intelligen: automatic driver synthesis for fuzz testing. In _Proceedings of the 43rd International Conference on Software Engineering: Software Engineering in Practice_ , 2021. 

- [105] Yaowen Zheng, Ali Davanian, Heng Yin, Chengyu Song, Hongsong Zhu, and Limin Sun. FIRM-AFL: High-Throughput greybox fuzzing of IoT firmware via augmented process emulation. In _28th USENIX Security Symposium (USENIX Security 19)_ , 2019. 

- [106] Wei Zhou, Le Guan, Peng Liu, and Yuqing Zhang. Automatic firmware emulation through invalidity-guided knowledge inference. In _30th USENIX Security Symposium (USENIX Security 21)_ , 2021. 

## **A Outline of Appendices** 

- Portable Layer and Implementation details – different phases of LEMIX (B Appendix) 

- Dataset details and bugs found by LEMIX (C Appendix) 

- Effects of removed inline assembly, instrumentation to handle interrupts, memory layout execution. (D Appendix) 

- Details of Compiler toolchain differences. (E Appendix) 

- Missing SVD Files and comparison against state of the art (F Appendix) 

## **B Appendix** 

### **B.0.1 Examples of Continuous Scale Gradations** 

- **S Fidelity:** Variable-length arrays are supported by embedded GCC-based compilers but lack support in clang. 

- **A Fidelity:** An emulator that implements all base instructions of ARMv7 but fails to emulate **SIMD** instructions or other processor extensions. 

- **P Fidelity:** An emulator that handles GPIO and UART correctly but approximates behavior for DMA. 

- **C Fidelity:** A simulation environment allows basic interrupt handling but does not handle nested interrupts. 

### **B.0.2 Native Portable Layer (NPL)** 

To improve testability and aid embedded firmware development, many RTOSes also provide ports for various host operating systems such as Linux and Windows. We refer to these ports as the _Native Portable Layer (NPL)_ and this includes the _Linux Portable Layer (LPL)_ and the _Windows Portable Layer (WPL)_ . These native ports allow embedded applications built on these RTOSes to be run on respective desktop operating systems as native applications. Native ports use host-provided implementation to simulate various embedded functionalities. For example, the Linux Portable Layer (LPL) of the FreeRTOS [2] and Zephyr [14] operating systems use Linux _pthreads_ to simulate tasks, _signals_ to simulate interrupts, and _timers_ to simulate clocks in the application. Some native ports contain only implementations for core RTOS functions such as task management, task context switching, interrupts, timers, and counters while other ports provide simulated implementations of various non-essential peripherals as well such as communication buses (SPI, I2C) and IO devices (USB, buttons, keyboard, LED, etc.). 

20 


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0021-00.png)


<!-- Start of picture text -->
1 � Effected Source file<br>2 struct foo {<br>3 int x;<br>4 int y[];<br>5 };<br>6 struct foo bar = {1, {2, 3, 4}};<br>7<br>8 � Compilation Fails<br>9 error: initialization of flexible array member is not allowed<br>10 struct foo bar = {1, {2, 3, 4}};<br>11<br>12 � Lemix Provides the Following Guidance Instruction<br>13<br>14 1. Search for the definition of the structure which has the<br>15 flexible member.<br>16 2. The member declaration will have a [], add a constant<br>17 value ex. [100] to the member.<br>18 3. Re-run the framework.<br><!-- End of picture text -->

Listing 4: � shows a sample code which causes compilation error indicated by �. LEMIX provides instructions to the developer to assist in fixing errors shown by �. 

### **B.0.3 Prevalence of NPL** 

A review of 23 actively maintained open-source RTOSes (as listed on the OSRTOS page [73]) shows that 14 (60%) RTOSes provide native ports. NPLs provided by 10 RTOSes only contain implementations of core RTOS functions, while 4 RTOSes also provide simulated implementations of nonessential peripherals also. Our review of the implementations of the available Native Portable Layer (NPL) also shows that while each native port is designed according to the architecture of their underlying RTOS, they have similar implementations as they rely on similar Linux or Windows features. 

## **B.2 Phase 1:** LEAPP **generation and Instrumentation** 

We implement our LEAPP generation as a Python tool. Given an embedded application, we first build for one of the supported targets and capture the compilation and linking steps using the Build EAR (Bear) tool [78] in a JSON file, _i.e.,_ compile_commands.json. We use WLLVM tool [97] to generate bitcode files for each of the source files. As mentioned in § 4.1.2 and Table 12, our tool uses an interactive technique to resolve compiler incompatibilities. Next, given the target RTOS for the embedded application, we identify the corresponding source files and replace them with the bitcode files of LPL layer to produce the final LEAPP We will tackle the linker issues (as mentioned in § 4.1.3), through a set of binary analysis scripts and LLVM passes. 

We also use LLVM transformation passes to implement our peripheral modeling and dynamic analysis assistance. We created a runtime library (one-time effort) implementing our hooks ( _e.g.,_ get_input_from_stdin() in Listing 2), which will be linked to produce the final fuzz-ready LEAPP. 

## **B.3 Phase 2: Testing** 

As mentioned in § 2.1, LEAPP runs indefinitely in an eventdriven mode. For whole program fuzzing, we use the persistent mode of AFL++ to provide inputs in a continuous manner and record coverage at specific intervals. We have also created auxiliary scripts to assist in crash reproducibility. 

For function level fuzzing, we use the recent 3C tool [61] for our co-relation analysis and implement our generator creation and LEAPP modification as LLVM passes. 

## **C Appendix** 

## **C.1 Dataset Details** 

Table 7 provides details of all applications used in our evaluation. 

## **C.2 Bugs Found By** LEMIX 

Table 9 shows bugs found by LEMIX across all the RTOSes and Table 10 shows the types of bugs found. Table 8 gives a detailed description and developer responses for each bug found. 

## **D Appendix** 

## **B.1 Implementation Details** 

We use a combination of Python scripts and CLANG/LLVM 10 toolchain passes to implement our framework. 

Listing 5 shows an example of inline ASM affecting program initialization where as Listing 6 shows an example of machine code embedded into the application as hex codes which is challenging to analyze on source level.Listing 7 

21 

|**RTOS**|**Application**|**ID**|**Description**|**SLOC**|
|---|---|---|---|---|
||FlipperZero|f1|Open source multi-tool device for researching and pentesting radio protocols, access control<br>systems, hardware, and more.|289k|
|FreeRTOS|Infnitime|f2|Firmware for the PineTime smartwatch|2.39M|
||SmartSpeaker|f3|Smart speaker based on cloud speech recognition running on FreeRTOS|172.8k|
||cdc_msc_freertos (TinyUSB)|f4|Example application to trigger a communication device class (cdc) task of tinyusb|933k|
||hid composite freertos (TinyUSB)|f5|Open-source cross-platform USB Host/Device stack for embedded systems. Example app to<br>trigger tinyusb hid (Human Interface Device) task|932k|
||nrf52840-dk pwm Application|n1|Demonstrates basic PWM support for the nRF52840-DK board.|2.1M|
||nrf52-feather i2c Application|n2|Demonstrates basic I2C support for the nRF52-Feather board.|2.02M|
|Nuttx|nsh (Nuttx-apps)|n3|Ships the entire nuttx kernel as a busybox application with several Unix-like utilities that<br>can be fashed to frmware to access nuttx features in a shell.|2.07M|
||posix spawn (Nuttx-apps)|n4|Demonstrates how to use the posix_spawn function to create a new process with more<br>control over attributes compared to fork.|2.1M|
||PX4-Autopilot|n5|PX4 fight control solution for drones running which has support for nuttx kernel|1.9M|
||Zephyr Blinky|z1|Demonstrates basic GPIO control and the core Zephyr kernel task creation.|20.2k|
|Zephyr|zmk|z2|Zephyr Mechanical Keyboard (ZMK) Firmware.|28.6k|
||ZSWatch|z3|Open Source Zephyr-based Smartwatch frmware.|36.6k|
||Tx_FreeRTOS_Wrapper|t1|Demonstrates how to develop an application using the FreeRTOS adaptation layer for<br>ThreadX.|1.09M|
|Threadx|Tx_LowPower|t2|Demonstrates how to develop an application using the ThreadX low power APIs when<br>coupled with STM32F4xx low power profles.|922k|
||Tx_Module|t3|Demonstrates how to load, start, and unload modules and use ThreadX memory protection<br>via the MPU.|1.01M|
||Tx_Thread_Creation|t4|Demonstrates how to create/destroy multiple threads using Azure RTOS ThreadX APIs,<br>including preemption thresholds and priority changes on-the-fy.|871k|
||Tx_Thread_MsgQueue|t5|Demonstrates how to send/receive messages between threads using ThreadX message queue<br>APIs with event chaining features.|996k|



Table 7: Dataset involving 18 applications across four prevalent RTOSes with application IDs added for clarity. SLOC represents combined sources from both the application and the underlying RTOS. 

22 

|**App ID**|**Bug**|**Description**|**Status of Bug**|
|---|---|---|---|
|f2|Assert Failure|Inconsistent use of confgASSERT FreeRTOS Kernel|�|
|f2|Assert Failure|Assert Failure in ble_event|�|
|f2|Build Related|Confict of min and max from stl_algo.h in HeartRateService.h|�|
|f3|Div By Zero|FPE in RCC_GetClocksFreq due to missing MMIO Checks|�|
|f3|Null Deref|Null Deref in ucFlash_Write|�|
|f3|OOB Write|Potential undefned behavior on overlapping copy in mem_cpy|�|
|f4|OOB Write|Potential OOB memcpy in tud_msc_read10_cb|�|
|f4|DoS|Infnite Loop in port_event_handle due to missing MMIO Checks|�|
|f5|OOB Read|Potential OOB Read & Null Deref due to missing MMIO Checks in board_get_unique_id|�|
|n1|Build Related|Buggy handling of unsigned long in vsprintf_internal|�|
|n3|Build Related|Compilation failure due to improper handling of CAN utils lely-core package|�|
|n4|OOB Write|Undefned behaviour on partial overlapping copy in sim_copyfullstate|�|
|n5|DoS|Infnite Loop in up_enable_dcache due to invalid MMIOs|�|
|z1|OOB Write|Stack Overfow in buf_char_out if CONFIG_PRINTK_BUFFER_SIZE is 0|�|
|z1|Null Deref|Null dereference in z_nrf_clock_control_lf_on|�|
|z2|OOB Write|The extract_conversion function in z_cbvprintf_impl can cause a potential 1 byte OOB<br>read when the format string ends with a % character|�|
|z2|OOB Write|If bpe points to a single byte, encode_uint may cause a 1-byte underfow write by<br>decrementing and dereferencing bp in the loop.|�|
|z2|OOB Write|Unchecked length can cause potential overfow|�|
|z3|OOB Read|OOB reads in lv_txt_utf8_next|�|
|z3|OOB Read|Reads past the buffer possible in u8_to_dec|�|
|z3|Div By Zero|Potential div by zero by passing 0 as data frame size|�|
|t4|Div By Zero|division by zero is possible given RCC->PLLCFGR is 0|�|



Table 8: Summary of all reported bugs and their statuses - � : acknowledged and PR merged, � : acknowledged, � : no response (issue open), � : not acknowledged as bug and closed. 

23 

Table 9: Bugs found by our technique in whole program (C2) and function level (C3) fuzzing modes. 

|**App**<br>**C2**|**C3**|**Unique Bugs**|
|---|---|---|
|f1<br>1|1||
|f2<br>3|1||
|f3<br>2|3||
|f4<br>1|3|9|
|f5<br>2|2||
|n1<br>1|1||
|n2<br>0|1||
|n3<br>1|1||
|n4<br>1|1|4|
|n5<br>1|0||
|z1<br>2|4||
|z2<br>2|3|7|
|z3<br>2|6||
|t4<br>1|1|1|
|**Total Bugs**<br>**20**|**28**|**21**|



1 __STATIC_FORCEINLINE **uint32_t** __get_IPSR( **void** ) 2 { 3 **uint32_t** result; 4 �__ASM **volatile** ("MRS %0, ipsr" : "=r" (result)); 5 � result = random() % 2; � 6 **return** result; 7 } 8 _#define FURI_IS_IRQ_MODE() ({__get_IPSR() != 0})_ � 9 10 **bool** furi_kernel_is_irq_or_masked( **void** ) { 11 **return** {FURI_IS_IRQ_MODE()};} 12 **int** main( **void** ) { 13 _// furi_check handles assertions_ 14 furi_check( 15 {!furi_kernel_is_irq_or_masked()} � 16 ); 17 **return** 0; 18 } 

Listing 5: An example of inline assembly effecting initialization code in Flipperzero. The � indicates inline assembly code removed by LEMIX and � indicates injected code to re-initialized with a random value. The highlighted checks (�) show how the IPSR value is verified in the initialization process to ensure we’re not in IRQ 

1 __ALIGN(16) 2 **static const uint16_t** delay_machine_code[] = { 3 _// SUBS r0, #loop_cycles_ 4 0x3800 + NRFX_COREDEP_DELAY_US_LOOP_CYCLES, 5 0xd8fd, _// BHI .-2_ 6 0x4770 _// BX LR_ 7 }; 8 9 **typedef void** (* delay_func_t)( **uint32_t** ); 10 **const** delay_func_t delay_cycles = 11 _// Set LSB to 1 to execute the code in the_ 12 _// Thumb mode._ 13 (delay_func_t)(delay_machine_code) | 1)); 14 **uint32_t** cycles = 15 time_us * NRFX_DELAY_CPU_FREQ_MHZ; 16 delay_cycles(cycles); 

Listing 6: An example of inline assembly masked inside hexadecimal machine code in Infinitime, one of our FreeRTOS applications. 

Table 10: Types of Bugs found by LEMIX in both Wp and Fl. 

|**Bug Type**|**Count**|
|---|---|
|OOB Read|2|
|OOB Write|7|
|Div By Zero|2|
|Null Dereference|3|
|DoS|2|
|Assert Failure|2|
|Build Related|3|



demonstrates how ISRs are modelled by LEMIX to run alongside other application tasks and Listing 8 gives an example of kernel initialization code from Zephyr RTOS application exhibiting memory layout dependent code which is currently not supported by LEMIX. 

## **E Appendix** 

## **E.1 GCC vs Clang Differences** 

Table 12 provides details on the compiler incompatibilities. Listings 12, 10 and 11 show examples of code that fails to compile with clang but is compatible with GCC. 

24 

|**RTOS**<br>**CATEGORY**|**Low Fidelity**|**High Fidelity**|
|---|---|---|
|BOF|3|0|
|OOB|5|0|
|UAF<br>FreeRTOS|4|0|
|Int Overfow|8|1|
|Privelege Escalation|0|1|
|BOF|10|2|
|OOB|5|1|
|Int Overfow<br>Zehr|3|1|
|DoS<br>py|4|1|
|Privelege Escalation|0|2|
|NULL Deref|4|0|
|BOF|2|1|
|OOB|3|0|
|NULL Deref<br>RIOT|5|0|
|DOS|2|1|
|logic|2|0|
|**Total**|**60**|**11**|



Table 11: Our analysis of the CVEs from the survey [6] conducted by Rust4Embedded (Extended Report) [85] indicates that only 11 out of 71 (15%) require high-fidelity execution (i.e precise hardware modeling). 

Table 12: Table depicting common GCC vs Clang incompatibilities found while porting applications across various RTOSes. 

|**Error Type**||**Compile**|**r Support**||**Error Fix**|**Automated**|
|---|---|---|---|---|---|---|
||**GCC Specifc**|**Arm-GCC**<br>**Specifc**|**Architecture**<br>**Specifc**|**Clang Support**|||
|Iiilii f fibl||||This initialization is|Mk h  b f||
|ntazaton o exe array<br>member is not allowed.|Yes (Example12)|No|No|not allowed in clang<br>(<15).|ae te array memer o a<br>fxed size.|No|
|Variable-sized object may not<br>be initialized.|Yes (Example10)|No|No|No|Declare the local variable with<br>a specifed length before<br>initializing it.|Yes|
|Member initializer ’X’ does<br>not name a non-static data<br>member or base class.|Yes (Example11)|No|No|No|Make the class inherit from<br>global namespace.|No|
|Static Assertion Failed.|No|No|This is due to<br>architecture specifc<br>size of types. Assert<br>failure is due to<br>compiling 32 bit<br>compatible types on<br>a 64 bit machine.|NA|Compile target on 32 bit<br>equivalent architecture.|Yes|
|Undeclared identifer example,<br>___assert_func_|No|Yes, The symbol<br>is specifc to<br>ARM’s internal<br>headers.|No|No|Get the symbol defnition from<br>the original source’s<br>preprocessor output.|Semi-<br>Automated|



25 


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0026-00.png)


<!-- Start of picture text -->
1 int main() {<br>2 /* RTOS specific task creation */<br>3 xTaskCreate(cdc_task, "cdc", CDC_STACK_SIZE, NULL,<br>4 configMAX_PRIORITIES - 2, NULL);<br>5 ...<br>6 /* Injecting isr_trigger function as a task<br>7 along with other tasks */<br>8 xTaskCreate(isr_trigger, "dispatcher_task", 1000, NULL,<br>9 configMAX_PRIORITIES - 1, NULL);<br>10 }<br>11<br>12 void dispatcher_task( void *parm) {<br>13 ( void )parm;<br>14 while (1) {<br>15 int size = sizeof (ivt) / sizeof (ivt[0]);<br>16 int random_isr = rand() % size;<br>17 switch (random_isr) {<br>18 case 0:<br>19 USBD_IRQHandler();<br>20 break ;<br>21 ...<br>22 case 4:<br>23 SPIM1_TWI1_IRQHandler();<br>24 break ;<br>25 default :<br>26 break ;<br>27 } } }<br><!-- End of picture text -->

Listing 7: Dispatcher Task instrumentation to handle interrupts. 


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0026-02.png)


<!-- Start of picture text -->
1 static void z_sys_init_run_level(<br>2 enum init_level level<br>3 )<br>4 {<br>5 static const struct init_entry *levels[] = {<br>6 __init_EARLY_start,<br>7 __init_PRE_KERNEL_1_start,<br>8 __init_PRE_KERNEL_2_start,<br>9 __init_POST_KERNEL_start,<br>10 __init_APPLICATION_start,<br>11 };<br>12 const struct init_entry *entry;<br>13 // The entries are function pointers that<br>14 // are expected to be placed in memory in<br>15 // the correct order. This ensures that<br>16 // the comparison between the current entry<br>17 // and the next one is valid.<br>18 for (entry = levels[level]; entry <<br>19 levels[level+1]; entry++) {<br>20 dev->state->initialized = true;<br>21 ( void )entry->init_fn.sys();<br>22 }<br>23 }<br>24 }<br><!-- End of picture text -->

Listing 8: Listing shows Layout Specific Execution found in one of Zephyr Kernel’s initialization routines. The kernel expects function pointers to be present in adjacent memory locations as directed by Board Specific Linker Scripts. 


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0026-04.png)


<!-- Start of picture text -->
1 void isr_trigger( void *parm) {<br>2 void isr_trigger( void *parm) {<br>3 ( void )parm;<br>4 while (1) {<br>5 int size = sizeof (ivt) / sizeof (ivt[0]);<br>6 int random_isr = rand() % size;<br>7 switch (random_isr) {<br>8 case ...<br>9 case 4:<br>10 /* ISR expecting a global state to be<br>11 initialized */<br>12 SPIM1_TWI1_IRQHandler(); �<br>13 break ;<br>14 default :<br>15 break ;<br>16 }<br>17 }<br>18 }<br>19<br>20 �<br>21 void SPIM1_TWI1_IRQHandler( void )<br>22 {<br>23 /* ISR expecting a global state m_cb<br>24 * to be initialized.<br>25 * /<br>26 irq_handler(((NRF_SPIM_Type*) 0x40004000UL),<br>27 &m_cb[NRFX_SPIM1_INST_IDX]);<br>28 }<br>29 �<br>30<br>31 �<br>32 void board_init( void ) {<br>33 /* Everything necessary gets initialized here */<br>34<br>35 #if CFG_TUH_ENABLED && defined(CFG_TUH_MAX3421) \<br>36 && CFG_TUH_MAX3421<br>37 /* SPIM1_TWI1_IRQHandler initialized only when<br>38 * any of these configs are selected.<br>39 * /<br>40<br>41 max3421_init(); �<br>42 #endif<br>43 }<br>44 �<br><!-- End of picture text -->

Listing 9: An example of a false positive interrupt misfiring in TinyUSB Application. 

- 1 **int** 2 doread( **uint8_t** addr, **uint8_t** *buf, **uint8_t** len) 3 { 4 **uint8_t** tx_buf[len + 1] = addr; 5 **return** -1; 6 } 

Listing 10: Listing shows variable sized object initialization which is not allowed even in the latest version of clang. 

26 


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0027-00.png)


<!-- Start of picture text -->
1 // Base class representing a generic object<br>2 class b {<br>3 public :<br>4 // Constructor accepting a config<br>5 b( const int config);<br>6 // Virtual destructor<br>7 virtual ~b() = default ;<br>8 };<br>9<br>10 namespace a :: b :: c {<br>11<br>12 class b_c : public b {<br>13 public :<br>14 // Constructor for b_c, initializes base class b<br>15 b_c( const int config);<br>16 };<br>17<br>18 // Constructor implementation for b_c<br>19 b_c::b_c( const int config) : b(config) {}<br>20<br>21 }<br><!-- End of picture text -->

Listing 11: Listing shows a sample code which errors because Clang expects the class b to inherit from the global namespace, but it cannot find it within the current scope. 

1 **uint8_t** ull_scan_rsp_set( **struct ll_adv_set** *adv, 2 **uint8_t** len, **void** *data) 3 { 4 **struct pdu_adv** *pdu; 5 pdu = lll_adv_scan_rsp_alloc(&adv->lll, &idx); 6 _/* update scan pdu fields. */_ 7 ... 8 _/* len is attacker controlled */_ 9 pdu->len = BDADDR_SIZE + len; � 10 _/* OOB write at scan_rsp.data[0] */_ 11 memcpy(&pdu->scan_rsp.data[0], data, len); � 12 ... 13 **return** 0; 14 } 

Listing 13: CVE-2021-3581: A low-fidelity vulnerability where unchecked length can cause OOB write if data and len are attacker controlled. 


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0027-04.png)


<!-- Start of picture text -->
1 struct foo {<br>2 int x;<br>3 int y[];<br>4 };<br>5<br>6 struct foo bar = {1, {2, 3, 4}};<br><!-- End of picture text -->

Listing 12: Listing shows flexible array member initialization which is not allowed in clang versions < 15. 

## **F Appendix** 

Listing 14 gives an example of a valid MMIO address range detected by LEMIX’s constant address analysis which was not found in the corresponding SVD files. Table 13 provides a more readable version of evaluation of LEMIX against existing state of the art tools.Figure 6 gives an idea of the coverage of total reachable functions in whole-program fuzzing. 

## **F.1 Bug Detected in Zephr RTOS** 

Listing 17 shows a buffer out-of-bounds write bug in Zephyr RTOS, where if _CONFIG_PRINTK_BUFFER_SIZE_ is not set by the application, it defaults to 0. At the _cbvprintf_ call site, the _buf_count_ member of _ctx_ is initialized to 0, leading to out-of-bounds access in the _buf_char_out_ function. This bug occurs in all applications of Zephr. 


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0027-10.png)


<!-- Start of picture text -->
1 � Identified Address ranges that are also in SVD:<br>2<br>3 (0x40000000, 0x40001000)<br>4 � (Peripheral: TIM2, Base: 0x40000000, End: 0x40000400)<br>5<br>6 (0x40008000, 0x40009000)<br>7 � (Peripheral: LPTIM1, Base: 0x40007c00, End: 0x40008000)<br>8<br>9 (0x40010000, 0x40011000)<br>10 � (Peripheral: SYSCFG_VREFBUF, Base: 0x40010000, End:<br>�→ 0x40010200)<br>11<br>12 (0x40020000, 0x40021000)<br>13 � (Peripheral: DMA1, Base: 0x40020000, End: 0x40020400)<br>14<br>15 � Identified Address ranges (and corresponding source lines)<br>�→ that are not in SVD files:<br>16<br>17 #define PERIPH_BASE (0x40000000UL)<br>18 #define APB1PERIPH_BASE PERIPH_BASE<br>19 #define TIM16_BASE (APB2PERIPH_BASE +<br>�→ 0x00004400UL)<br>20 (0x40020000, 0x40021000)<br>21<br>22 #define SAI1_BASE (APB2PERIPH_BASE +<br>�→ 0x00005400UL)<br>23 (0x40005000, 0x40006000)<br>24<br>25 #define LPTIM2_BASE (APB1PERIPH_BASE +<br>�→ 0x00009400UL)<br>26 (0x40009000, 0x4000a000)<br><!-- End of picture text -->

Listing 14: An example illustrating the cases where the detected MMIO address ranges are in SVD files (�) and those that are present in source files but missing (�) in SVD files. 

27 

Table 13: Approximate Number of unique basic blocks discovered by various configurations of LEMIX in comparison to State Of The Art Tools (Discussed in § 5.4 and § 5.6). M1- M3 represents different configuration modes for LEMIX. 

|**AppID**|||**L**|**x**||||**Fw**|||**Mf**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**M**|**1**|**M**|**2**|**M**|**3**|||||||
||Cov|Bug|Cov|Bug|Cov|Bug|Cov|Crash|Bug|Cov|Crash|Bug|
|f1|731|0|2.9k|1|�|1|500|1|0|1k|0|0|
|f2|456|1|2.8k|3|�|1|�|N/A|N/A|1.5k|1|1|
|f3|560|1|668|2|1.5k|3|�|N/A|N/A|�|N/A|N/A|
|f4|563|0|1k|1|6k|3|500|0|0|2k|41|0|
|f5|442|0|728|2|1.8k|2|700|0|0|1.8k|93|0|
|n1|105|0|301|1|13.5k|1|356|0|0|25.2k|148|0|
|n2|143|0|338|0|16.8k|1|405|0|0|300|0|0|
|n3|157|1|357|1|19.9k|1|60|1|1|100|1|0|
|n4|135|0|235|1|19.5k<br>|1|388|3|0|2.4k|0|0|
|n5|823|0|1.5k|1|�|0|134|0|0|226|0|0|
|z1|76<br>|0|86<br>|2|3k|4|44<br>|2|0|213|0|0|
|z2|�<br>|0|�<br>|2|12.3k|3|�<br>|N/A|N/A|10.8k<br>|483|1|
|z3|�|0|�|2|4.6k|6|�|N/A|N/A|�|N/A|N/A|
|t1|210|0|553|0|6.3k|0|670|0|0|750|0|0|
|t2|214|0|553|0|240|0|791|0|0|694|0|0|
|t3|�|0|�|0|3.1k|0|900|0|0|700|0|0|
|t4|310|0|455|1|188|1|749|0|0|659|10|1|
|t5|254|0|436|0|5.2k|0|748|0|0|658|0|0|
|Avg/Tot|345|3|860|20|7.5k|28|496|7|1|3.1k|777|3|
|Unique Bugs||3||10||11|||1|||3|



28 


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0029-00.png)


<!-- Start of picture text -->
100<br>n2<br>n3n4n5<br>f1 n1<br>t2 t4<br>80 f5 t1<br>t5<br>f4<br>60<br>40<br>f2<br>f3<br>20<br>z1<br>FreeRTOS Nuttx Zephyr ThreadX<br>RTOSes<br>Coverage Percentage (%)<br><!-- End of picture text -->

Figure 6: Each bar represents the percentage of functions hit amongst the total reachable functions for an application on a specific RTOS. Application IDs represent respective application from Table 7. 


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0029-02.png)


<!-- Start of picture text -->
1 bool latch_pending_read_and_check(latch, i) {<br>2 latch[i] = GPIOx->LATCH; �<br>3 if (latch[i])<br>4 {<br>5 /* If any latch bit is set, another edge was<br>6 captured -- repeat event processing. */<br>7 return true;<br>8 }<br>9 }<br>10 void port_event_handle(...)<br>11 {<br>12 uint32_t latch[GPIO_COUNT] = {0};<br>13 ...<br>14 do {<br>15 /* Attacker controlled gpio ports */<br>16 latch_pending_read_and_check(latch,<br>17 p_cb->available_gpio_ports);<br>18 /* The latch sent for processing */<br>19 nrfy_gpiote_events_process(p_gpiote, ...);<br>20<br>21 /* The latch_pending_read_and_check can always<br>22 return true leading to infinite loop */<br>23 } while (latch_pending_read_and_check(latch, �<br>24 p_cb->available_gpio_ports));<br>25 }<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/17-lemix-enabling-testing-of-embedded-applications-as-linux.pdf-0029-03.png)


<!-- Start of picture text -->
1 /* validate syscall limit */<br>2 ldr ip, =K_SYSCALL_LIMIT<br>3 cmp r6, ip<br>4 /* The supplied syscall_id must be lower than the<br>5 * limit (Requires unsigned integer comparison)<br>6 * /<br>7 blt valid_syscall_id �<br>8<br>9 /* bad syscall id. Set arg1 to bad id and set<br>10 call_id to SYSCALL_BAD */<br>11 str r6, [r0]<br>12 ldr r6, =K_SYSCALL_BAD<br><!-- End of picture text -->

Listing 16: CVE-2020-10027: A high-fidelity vulnerability where a signed comparison in ARM syscall validation (blt vs. blo) allows privilege escalation from user thread to kernel. 

Listing 15: If latch_pending_read_and_check() keeps returning true due to malicious GPIO peripheral, the do-while loop will never terminate, causing an infinite loop leading to DoS found in nrfx HAL library. 

29 

1 _#ifndef CONFIG_PRINTK_BUFFER_SIZE_ 2 _#define CONFIG_PRINTK_BUFFER_SIZE 0_ � 3 **struct buf_out_context** { 4 **char** buf[CONFIG_PRINTK_BUFFER_SIZE]; 5 **unsigned int** buf_count; 6 }; 7 8 **static int** buf_char_out( **int** c, **void** *ctx_p) { 9 **struct buf_out_context** *ctx = ctx_p; 10 ctx->buf[ctx->buf_count] = c; � 11 _// buf_count incremented before the check_ 12 ++ctx->buf_count; � 13 **if** (ctx->buf_count == CONFIG_PRINTK_BUFFER_SIZE) { 14 buf_flush(ctx); 15 } 16 **return** c; 17 } 

Listing 17: OOB write in Zephyr function _buf_char_out_ . 

30 

