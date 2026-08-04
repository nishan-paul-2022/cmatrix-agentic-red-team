# **Veritas: A Semantically Grounded Agentic Framework for Memory Corruption Vulnerability Detection in Binaries** 

Xinran Zheng University College London xinran.zheng.23@ucl.ac.uk 

Alfredo Pesoli Marco Valleri BynarIO BynarIO alfredo@bynar.io marco@bynar.io 

Lorenzo Cavallaro 

Suman Jana Columbia University suman@cs.columbia.edu 

University College London / BynarIO {l.cavallaro,lorenzo}@{ucl.ac.uk,bynar.io} 

## **Abstract** 

was confirmed and assigned a CVE. These results support semantic grounding as an operational design principle for practical binary vulnerability detection. 

Detecting memory corruption vulnerabilities in stripped binaries requires recovering object semantics, interprocedural propagation structure, and path-feasible triggering conditions from representations that are simultaneously low-level and semantically lossy. Recent LLM-based approaches improve code understanding and, when equipped with specialized tools, can assist vulnerability research; however, in stripped binaries, reliable detection still requires explicit grounding in memory-relevant program semantics and feasibility evidence beyond lossy lifted or decompiled representations. We present Veritas, a hybrid, semantically grounded framework for binary memory corruption vulnerability detection. Veritas combines a static slicer, _defuse_ , over RetDec-lifted LLVM IR; a dual-view LLM detector, _discovery_ , that performs step-wise reasoning over statically grounded candidate flows using RetDec-decompiled C and selectively instantiated LLVM IR; and a multi-agent _validator_ that grounds detector hypotheses in debugger-visible artifacts and concrete runtime evidence. The slicer reconstructs interprocedural value-flow relations from parser-derived LLVM-IR facts, including def-use, call, return, global access, and pointer operation relations, and emits compact witness-backed flow objects for downstream analysis. The detector uses these artifacts to reason about control flow, bounds, and object correspondence without rediscovering propagation from the whole binary. The validator then confirms or rejects candidate vulnerabilities via guided debugging, breakpoint inspection, and memory-checking oracles. We implement Veritas in a modular pipeline and evaluate it on a curated benchmark of repository-based binary vulnerability cases. Veritas achieves 90% recall. For false positive assessment, we exhaustively validate and manually verify 623 discovery candidate vulnerabilities via validator in tractable full-pipeline runs and audit additional candidate vulnerabilities from larger cases; the exhaustive subset produces no false positives, and the additional audit identifies two manually confirmed false positives. In a separate real-world case study, Veritas discovered a previously unknown Apple vulnerability (0day) that 

## **CCS Concepts** 

• **Security and privacy** → **Systems security** ; **Vulnerability management** ; **Vulnerability scanners** ; 

## **Keywords** 

Vulnerability Detection, Large Language Model 

#### **ACM Reference Format:** 

Xinran Zheng, Alfredo Pesoli, Marco Valleri, Suman Jana, and Lorenzo Cavallaro. 2018. Veritas: A Semantically Grounded Agentic Framework for Memory Corruption Vulnerability Detection in Binaries . In _Proceedings of Make sure to enter the correct conference title from your rights confirmation email (Conference acronym ’XX)._ ACM, New York, NY, USA, 15 pages. https: //doi.org/XXXXXXX.XXXXXXX 

## **1 Introduction** 

Memory corruption vulnerabilities (MCVs) enable attackers to subvert memory safety and seize control of program behavior, making them one of the most impactful classes of software defects [53]. In practice, security analysis is often performed directly on compiled binaries—the artifacts that are actually deployed and executed. Even when source code is available, it may be inaccessible (e.g., proprietary or legacy systems), mismatched with the analyzed build, or transformed by compilation and optimization in ways that erase memory-relevant structure, object boundaries, and high-level control flow [36, 54]. As a result, detecting MCVs in binaries becomes a problem of semantic reconstruction: the analysis must recover how memory objects are allocated, propagated, constrained, and accessed across functions from artifacts that no longer explicitly encode this information. While human experts can perform such reconstruction, it requires deep expertise and does not scale to the size and complexity of real-world binaries. 

Recent work applies large language models (LLMs) to code reasoning and vulnerability analysis, often within agentic frameworks that enable interaction with repositories, tools, and execution environments [3, 13, 20, 21, 28, 41, 56]. However, binary memory corruption vulnerability (BMCV) detection is fundamentally different from standard code comprehension. It requires tracking how attackercontrolled values propagate across functions and shared state to reach memory-sensitive operations, and determining whether the 

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org. _Conference acronym ’XX, Woodstock, NY_ 

© 2018 Copyright held by the owner/author(s). Publication rights licensed to ACM. ACM ISBN 978-1-4503-XXXX-X/2018/06 https://doi.org/XXXXXXX.XXXXXXX 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Xinran Zheng, Alfredo Pesoli, Marco Valleri, Suman Jana, and Lorenzo Cavallaro 

resulting access violates object safety under feasible path conditions. These requirements are challenging even for traditional static analysis, as pointer relations, aliasing, and object lifetimes often span multiple functions and levels of indirection [36, 54, 55]. They are even more problematic for LLM-based agents, whose reasoning is constrained by limited context and incomplete program facts. Evidence suggests that LLM-based vulnerability reasoning remains brittle when it lacks structured program-semantic support: current models often struggle to recover interprocedural dependencies and vulnerability-triggering semantic constraints when such evidence must be inferred from code context without sufficiently strong grounding [14, 44, 45, 50, 57]. At the same time, frontier models can discover real vulnerabilities at scale when embedded in systems with context selection, execution, and validation scaffolds [6–8, 16]. We do not argue that LLMs are intrinsically incapable of vulnerability discovery; rather, we observe that the effectiveness of such systems depends on how well the surrounding infrastructure recovers the semantic structure that reasoning requires. 

This dependence is especially consequential for BMCV detection, where the required semantic structure is partially absent by construction: compilation and stripping obscure interprocedural data flow, pointer relations, and path-sensitive conditions. Existing agentic approaches, developed primarily for source-level analysis, compensate through summarization, retrieval, or call-graph expansion [3, 19–21, 26]. However, these strategies do not directly solve the semantic-recovery problem posed by stripped binaries: call-graph expansion misses shared-state dependencies beyond direct caller–callee edges, summarization often discards the precise facts needed to assess whether a propagation path is vulnerabilityrelevant, and coverage-guided fuzzing explores broad input spaces with unguided seeds, making it unlikely to reach the specific path and memory state required to trigger a given corruption within a bounded budget. The core issue for BMCV is not model capability, but the absence of explicit static and executable grounding. 

We argue that BMCV detection requires _semantic grounding_ : constraining vulnerability reasoning to explicit memory-relevant program facts and validating conclusions against executable behavior. Without such grounding, LLM-based detectors rely on syntactic proxies rather than evidence of how attacker-controlled data propagates to memory-sensitive operations, leading to incomplete or incorrect vulnerability hypotheses. This issue is amplified in binaries, where compilation and stripping fragment semantic information across representations such as lifted IR and decompiled code. Semantic grounding has two components. _Static grounding_ constructs model context from interprocedural source-to-sink propagation evidence recovered from binary artifacts, exposing the memory lifecycle from input to access despite representation loss. _Runtime grounding_ validates each hypothesis through targeted execution aligned with the predicted path, rather than unguided exploration. Together, these components ensure that reasoning is anchored in both recovered program semantics and executable evidence. 

Based on this, we present Veritas, a semantically grounded agentic framework for detecting memory corruption vulnerabilities in stripped binaries. Veritas organizes analysis into three stages aligned with the grounding layers. A semantic-driven _Slicer_ extracts compact, witness-backed source-to-sink flows from lifted LLVM IR, capturing interprocedural propagation and memory-risk operations 


![](docs/paper-research/md-downloaded-paper-professor/images/04-veritas-semantically-grounded-agentic-framework-for.pdf-0002-06.png)


<!-- Start of picture text -->
ReadRankDims(mat_t *mat, matvar_t *matvar,...){<br>  for ( i = 0; i < matvar->rank; i++) {<br>     size_t readresult = fread(&buf, // Source<br>matvar->dims           sizeof(mat_uint32_t), 1, (FILE*)mat->fp);<br>     matvar->dims[i] = buf;...}<br>Mat_VarReadNextInfo5( mat_t *mat ) matvar->dims<br>ReadNextFunctionHandle(mat_t *mat, matvar_t *matvar){<br>  for ( j = 0; j < matvar->rank; j++ )<br>     nfunctions *= matvar->dims[j];<br>     matvar->data = malloc(nfunctions*sizeof(matvar_t *));<br>     matvar_t **functions = (matvar_t**)matvar->data;;<br>  for ( i = 0; i < nfunctions; i++ )<br>     functions[i] = Mat_VarReadNextInfo(mat);// OOB-write<br>Without Grounding (Claude Code on Source Code)<br>Step 1: Memory Object Localization<br>...`ReadRankDims()`  reads uint32 values from the<br>MAT file and stores them in `matvar->dims[]`...<br>Scan found ~140 consumption sites of dims and<br>narrowed to 6 candidates with<br>allocation/computation mismatch potential...<br>Step2: Allocation-Extent Binding<br>...`ReadNextFunctionHandle`: allocation and loop<br>both derive from `nfunctions`; they "wrap<br>identically"...<br>...Rejected. No vulnerability found.<br>With Grounding (Veritas on Stripped Binary)<br>Step 1: Slicer emits witness-backed flow<br>Mat_VarReadNextInfo5:fread@68 → ReadRankDims:%263<br>→ ReadNextFunctionHandle:pointer_offset@32,<br>carrying taint token %stack_var_-184 to sink %6.<br>Step 2: Dual-view Vulnerability Detection<br>Allocation computes `nfunctions * 8`, which wraps mod<br>2; loop iterates raw `nfunctions`. When `nfunctions`<br>is large, buffer size is insufficient.<br>Step 3: Runtime Validation<br>Valgrind: "Invalid write of size 8, 0 bytes after a<br>block of size 0 alloc'd." SIGSEGV confirmed.<br><!-- End of picture text -->

**Figure 1: Failure case showing the need for semantic grounding. Even on source code, a frontier agent (Claude Code) locates the sink, without tracing how the attacker-controlled value propagates through allocation and loop-bound computation, finally dismisses the mismatch. Veritas operates on the stripped binary, traces the tainted value from source to sink via a witness-backed flow, detects the allocation-extent mismatch, and confirms the out-of-bounds write at runtime.** 

across functions. A dual-view _Detector_ performs step-wise reasoning over these flows, combining decompiled control-flow structure with selectively instantiated IR to recover memory semantics lost during compilation. A _Validator_ translates candidate vulnerabilities into targeted execution checks, confirming or refuting each hypothesis using debugger-visible artifacts and concrete runtime evidence. Across all stages, Veritas constrains LLM reasoning to verifiable program semantics reconstructed from binary artifacts, enabling precise and executable vulnerability detection. This design closes the gap between LLM-based reasoning and validation grounded in static data-flow evidence and executable behavior in binary vulnerability analysis. 

In this paper, we make the following contributions: 

- We present Veritas, a semantically grounded framework for detecting memory corruption vulnerabilities in stripped binaries, unifying static program analysis and runtime validation as two grounding layers for controlled LLM reasoning. 

- We design a three-stage grounded architecture: a _Slicer_ that extracts witness-backed source-to-sink flows from lifted 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Veritas: A Semantically Grounded Agentic Framework for Memory Corruption Vulnerability Detection in Binaries 

- LLVM IR, a dual-view _Detector_ that performs step-wise reasoning over decompiled code with selective IR support, and a _Validator_ that confirms hypotheses using debugger-visible artifacts and concrete execution evidence. 

- We construct a fine-grained benchmark of real-world binary memory-corruption cases with trace-level ground truth, and show that Veritas clearly outperforms strong static, dynamic, binary-native, and agentic baselines end to end. 

## **2 Motivation** 

## **2.1 Challenges in Detecting BMCVs** 

To illustrate the underlying challenges of BMCV detection, we use CVE-2020-13790, an out-of-bounds read caused by inconsistent size assumptions about a shared lookup table, as a motivating example because it compactly captures key difficulties of BMCV. As shown in the source-code view of Figure 2, the vulnerability is not localized to a single block of code, but spans a disjoint lifecycle involving the global structure ppm_source_struct: jinit_read_ppm allocates the structure object, start_input_ppm initializes the rescale buffer according to the parsed maxval, and get_rgb_row later consumes this buffer, triggering an out-of-bounds access when an attackercontrolled input byte exceeds the maxval used to size the array. While a human expert may connect these functions through sourcelevel names and structure fields, automating the same reasoning in stripped binaries requires recovering such relations from lossy lifted and decompiled representations. The following subsections detail three challenges that motivate semantic grounding in Veritas. 

_2.1.1 Shared-State Tracking beyond Call Chains._ Many BMCV cases are not confined to a single function; instead, the erroneous memory access results from multiple functions operating on a shared memory region with inconsistent assumptions about its contents, layout, or bounds. Existing approaches typically rely on call-chain reasoning to approximate vulnerability propagation [20, 26, 28], but this is often insufficient because the relevant coupling may be defined by shared program state rather than direct control flow. As illustrated in Figure 2, jinit_read_ppm(), start_input_ppm(), and get_rgb_row() have no direct call edges between them, yet they all operate on the same global structure ppm_source_struct: allocation, bound initialization, and the eventual out-of-bounds read occur in disjoint locations. Connecting these operations requires resolving aliases and reconstructing field-level uses of memory objects, evidence that call-chain context alone does not capture. 

_2.1.2 Semantic Loss._ Accurately tracking shared program state across functions requires understanding how memory fields are allocated, populated, and consumed at different execution stages. In binaries, this evidence is fragmented across recovered representations. As Figure 2 illustrates, neither lifted IR nor decompiled code simultaneously provides precise memory semantics and highlevel program structure. LLVM IR preserves byte-level memory access patterns through instructions such as getelementptr, explicit loads and stores, and pointer arithmetic, but it is saturated with transient SSA variables, casts, and compiler-introduced bookkeeping that inflate code volume and obscure field-level relationships. Decompiled code provides a concise abstraction suitable for controlflow reasoning, but collapses memory operations into generic offset 

expressions (e.g., param_2 + 0x48), erasing the distinction between structure fields, array indices, and pointer dereferences. The result is a fundamental dilemma: the low-level facts needed to preserve object identity and sink semantics are more explicit in lifted IR, while the higher-level structure needed to interpret vulnerability logic is clearer in decompiled code. The evidence required for memory corruption reasoning is thus split across representations that are individually incomplete. 

_2.1.3 Constraint Verification._ Detecting BMCV vulnerabilities requires determining not only where memory is accessed, but whether a concrete execution can reach the vulnerable state. Even when static analysis identifies a suspicious access, it often cannot determine whether the required branch decisions, input values, and memory bounds can hold simultaneously. As illustrated in Figure 2, the out-of-bounds read is triggered only when the PPM parser selects the 8-bit decoding path and an input byte exceeds the parsed maxval, so reasoning about the relationship between the input value, the parsed bound, and the guarding branch conditions is essential. Due to the semantic loss discussed above, a bounds definition in start_input_ppm and the corresponding access in get_rgb_row may be obscured or disconnected in the recovered representation. A suspicious source-to-sink flow therefore remains only a hypothesis unless its triggering conditions can be tied to concrete execution behavior. 

## **2.2 Insights for Semantically Grounding Agentic Framework for BMCV Detection** 

The challenges above motivate _semantic grounding_ , which constrains vulnerability reasoning through two complementary layers: _static grounding_ restricts model context to compact, interprocedural source-to-sink flows backed by explicit propagation evidence, and _runtime grounding_ requires each candidate to be confirmed through concrete execution artifacts. This perspective leads to three design insights: Insight 1 : Ground context selection in memory flow evidence. The context exposed to the LLM should be constrained to source-to-sink flows supported by explicit program analysis evidence, preserving evidence needed to connect object allocation, bound definition, and unsafe consumption while excluding unrelated program logic. Insight 2 : Selectively fuse dual representations to overcome the precision-efficiency dilemma. The model should reason primarily over decompiled code, consulting lifted LLVM IR only at vulnerability-relevant loci identified by static slicing, focusing on candidate-relevant memory operations without the cost and noise of full IR exposure. Insight 3 : Ground feasibility confirmation in executable evidence. Rather than treating the model’s judgment as final, feasibility checking should be tied to runtime validation, letting the LLM focus on semantic inference while instrumentation confirms the vulnerability can be triggered. 

These insights lead to Veritas, a three-stage framework that grounds LLM-based BMCV detection in static context and dynamic evidence: a semantics-driven slicer extracts compact source-tosink flows from lifted binaries, a dual-view detector reasons over these flows with selective IR evidence, and a multi-agent validator confirms suspected vulnerabilities through concrete execution. The following section details each stage. 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Xinran Zheng, Alfredo Pesoli, Marco Valleri, Suman Jana, and Lorenzo Cavallaro 


![](docs/paper-research/md-downloaded-paper-professor/images/04-veritas-semantically-grounded-agentic-framework-for.pdf-0004-02.png)


<!-- Start of picture text -->
Attacker uploaded PPM file Reader Selection PPM Reader Object and Shared Structure Allocation<br>1: int main(int argc, char **argv){2:  ... 1: select_file_type(j_compress_ptr cinfo,     FILE*infile){  ... 1: jinit_read_ppm(j_compress_ptr cinfo){2:   ppm_source_ptr source;<br>3:  if ((input_file = fopen(argv[file_index],  2:    int c = getc(infile); 3:   source = (ppm_source_ptr)<br>READ_BINARY)) == NULL) ...  3:    if (c == 80) {   4:    (*cinfo->mem->alloc_small)((j_common_ptr)cinfo,<br>4:  src_mgr = select_file_type(&cinfo, input_file);} 4:      return jinit_read_ppm(cinfo); } ...       JPOOL_IMAGE, sizeof(ppm_source_struct));<br>5:   return (cjpeg_source_ptr)source;}<br>Malicious Data Reading and Memory Consumption No call chain Header Parsing and Rescale Array Memory Allocation<br>1: get_rgb_row(j_compress_ptr cinfo,  1: start_input_ppm(j_compress_ptr cinfo, cjpeg_source_ptr sinfo){<br>         cjpeg_source_ptr sinfo){ 1: typedef struct {   2:   ppm_source_ptr source = (ppm_source_ptr)sinfo;<br>4:   register JSAMPLE *rescale = source->rescale;register JSAMPLE *rescale = source->rescale; 3:  ...   3:   ...<br>5:   if (!ReadOK(source->pub.input_file,  4:  U_CHAR *iobuffer;    4:   maxval = read_pbm_integer(cinfo, source->pub.input_file, 65535);<br>          source->iobuffer, source->buffer_width)) 5:  JSAMPLE *rescale;JSAMPLE *rescale; 5:   source->rescale = (JSAMPLE *)<br>6:       ERREXIT(cinfo, JERR_INPUT_EOF); 6:  unsigned int maxval; 6:   (*cinfo->mem->alloc_small) ((j_common_ptr)cinfo, JPOOL_IMAGE,<br>7:   bufferptr = source->iobuffer; 7: } ppm_source_struct;ppm_source_struct;        (size_t)(((long)maxval + 1L) * sizeof(JSAMPLE)));<br>8:   ... 8: typedef ppm_source_struct ppm_source_struct  7:   ...<br>9:  //OOB-read: If file data UCH(*bufferptr++) is larger 9:          *ppm_source_ptr; 8:   // Initialize rescale array with maxval<br>10: than maxval, reads beyond allocated array.  9:   for (val = 0; val <= (long)maxval; val++) {<br>11:  RGB_READ_LOOP(rescale[UCH(*bufferptr++)], rescale[UCH(*bufferptr++)], [UCH(*bufferptr++)],  Shared the global structure  10:   source->rescale[val] = (JSAMPLE)((val * MAXJSAMPLE +<br>12:          ptr[aindex] = 0xFF;)} 11:           half_maxval) / maxval);}<br>ppm_source_struct<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/04-veritas-semantically-grounded-agentic-framework-for.pdf-0004-03.png)


<!-- Start of picture text -->
Malicious Data Reading and Memory Consumption No call chain<br>1: get_rgb_row(j_compress_ptr cinfo,<br>         cjpeg_source_ptr sinfo){ 1: typedef struct {<br>4:   register JSAMPLE *rescale = source->rescale;register JSAMPLE *rescale = source->rescale; 3:  ...<br>5:   if (!ReadOK(source->pub.input_file,  4:  U_CHAR *iobuffer;<br>          source->iobuffer, source->buffer_width)) 5:  JSAMPLE *rescale;JSAMPLE *rescale;<br>6:       ERREXIT(cinfo, JERR_INPUT_EOF); 6:  unsigned int maxval;<br>7:   bufferptr = source->iobuffer; 7: } ppm_source_struct;ppm_source_struct;<br>8:   ... 8: typedef ppm_source_struct ppm_source_struct<br>9:  //OOB-read: If file data UCH(*bufferptr++) is larger 9:          *ppm_source_ptr;<br>10: than maxval, reads beyond allocated array.<br>11:  RGB_READ_LOOP(rescale[UCH(*bufferptr++)], rescale[UCH(*bufferptr++)], [UCH(*bufferptr++)],  Shared the global structure<br>12:          ptr[aindex] = 0xFF;)}<br>ppm_source_struct<br><!-- End of picture text -->


![](docs/paper-research/md-downloaded-paper-professor/images/04-veritas-semantically-grounded-agentic-framework-for.pdf-0004-04.png)


<!-- Start of picture text -->
PPM Reader Object and Shared Structure Allocation ( jinit_read_ppm ) PPM Reader Object and Shared Structure Allocation<br>%9 = load ptr, ptr %2, align 8 //  load global pointer code ** jinit_read_ppm(long param_1) {<br>%10 = call ptr %8(ptr noundef %9, i32 noundef 1,  1: code **ppcVar1;<br>    i64 noundef 88) //  allocate shared structure ppm_source_struct // allocated ppm_source_struct<br>store ptr %10, ptr %3, align 8 //  store pointer to new object 2: ppcVar1 = (code **)(***(code ***)(param_1 + 8))(param_1,1,0x58);<br>Header Parsing and Rescale Array Memory Allocation<br>Header Parsing and Rescale Array Memory Allocation ( start_input_ppm ) 1: void start_input_ppm(long *param_1, long param_2){<br>%586 = call ptr %580(ptr noundef %581, i32 noundef 1,            i64 noundef %585) %588 =             ptr %587, i32 0, i32 4  store ptr %586, ptr %588, align 8getelementptr inbounds %struct.ppm_source_struct//  alloc rescale table // //  link rescale tableget &rescale field  ,  2:   uVar7 = read_pbm_integer(...); 3:   uVar8 = (**(code **)param_1[1])(param_1,1,(ulong)uVar7 + 1);4:   *(undefined8 *)(param_2 + 0x48) = uVar8; 5:   6:   for (local_40 = 0; local_40 <= (long)(ulong)uVar7; local_40 = local_40 + 1)  // assign size of rescale array// maxval //  allocate rescale<br>8:    {*(char *)(*(long *)(param_2 + 0x48) + local_40) =<br>Malicious Data Reading and Memory Consumption ( get_rgb_row ) 9:       (char)((long)(local_40 * 0xff + (ulong)(uVar7 >> 1)) /(long)(ulong)uVar7);}}<br>%18 = getelementptr inbounds<br>      %struct.ppm_source_struct, ptr %17, i32 0, i32 4 Malicious Data Reading and Memory Consumption<br>%184 = load ptr, ptr %8, align 8 //  load rescale table undefined8 get_rgb_row(long *param_1,long param_2){<br>%189 = sext i32 %188 to i64 ;  %188 is the controlled input 1: lVar7 = *(long *)(param_2 + 0x48);  // rescale<br>%190 = getelementptr inbounds i8, ptr %184, i64 %189   // user input loacl_28; OOB-read<br>%191 = load i8, ptr %190, align 1 //  OOB-read 2: *(undefined *)(local_20 + iVar2) = *(undefined *)(lVar7 + (int)(uint)*local_28);<br><!-- End of picture text -->

**Figure 2: Realistic program artifacts from CVE-2020-13790, an out-of-bounds read in the PPM reader. The vulnerability arises from a non-call-chain shared-memory dependence, where jinit_read_ppm() allocates a ppm_source_struct, start_input_ppm() populates its rescale array, and get_rgb_row() later consumes this array using an attacker-controlled index without checking the relationship between maxval and bufferptr. All functions are connected through the global structure ppm_source_struct, not by direct call edges.** 

## **2.3 Threat Model** 

We consider an adversary who controls program inputs to a binary through file, command-line, or network channels and seeks to trigger a memory-corruption condition. The vulnerabilities of interest are those in which attacker-controlled data, or values derived from it such as sizes, offsets, indices, or pointers, propagates interprocedurally to a memory-risk operation under feasible path conditions. Veritas assumes access to the target binary and an isolated execution environment for validation, but does not assume source code availability; the binary is stripped and may differ semantically from any available source build. The current evaluation focuses on outof-bounds reads and writes. Logic flaws, side channels, and severe lifting or decompilation failures that prevent analyzable LLVM-IR and decompiled artifacts are out of scope. 

## **3 Methodology** 

## **3.1 Overview of Framework** 

Building on the challenges and insights above, Veritas organizes its analysis into three stages around two grounding layers, as illustrated in Figure 3. Static program analysis constrains what the LLM 

reasons over, concrete runtime evidence determines what it may conclude, and each stage narrows the reasoning space for the next so that no stage must operate over unconstrained program context. 

The **Semantic-driven Context Slicer** provides the first grounding layer by lifting the binary with RetDec [9], constructing an interprocedural propagation graph over LLVM IR, and extracting taintverified candidate flows that connect attacker-controlled inputs to memory-risk operations. These witness-backed flows replace the full binary with a compact reasoning scope for all downstream analysis. The **Dual-view Vulnerability Detector** then reasons over each flow one function at a time, using decompiled C as the primary substrate and consulting LLVM IR at source and sink functions where taint alignment or sink semantics require disambiguation. Shared flow prefixes are reused through trie-based memoization, and a final consistency check verifies end-to-end taint propagation, bounds constraints, and sink conditions before a candidate is reported. The **Automatic Vulnerability Validator** provides the runtime grounding layer: it maps detector hypotheses to executable coordinates and orchestrates multiple agents to test them through debugger breakpoints, crafted PoCs, and memory-checking oracles. 

Veritas: A Semantically Grounded Agentic Framework for Memory Corruption Vulnerability Detection in Binaries Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 


![](docs/paper-research/md-downloaded-paper-professor/images/04-veritas-semantically-grounded-agentic-framework-for.pdf-0005-01.png)



![](docs/paper-research/md-downloaded-paper-professor/images/04-veritas-semantically-grounded-agentic-framework-for.pdf-0005-02.png)



![](docs/paper-research/md-downloaded-paper-professor/images/04-veritas-semantically-grounded-agentic-framework-for.pdf-0005-03.png)


<!-- Start of picture text -->
Static Grounding Controlled LLM Reasoning Runtime Grounding<br> Semantic-driven   Dual-view Vulnerability Detector  Automatic Vulnerability Validator<br>Context Slicer Trie-based Flow Memoization   Vulnerability / Benign  Detector   Stripped<br>Source Candidates Binary<br> Stripped Binary Cached  Sink Func Self Consistency<br>Prefix Reasoning State Checking Artifact Preparation & Docker Building<br>Intermediate Func Path-sensitive   Multi-agent Collaboration<br> Binary Lifting ... Verification<br>LLVM IR  Flow 2 Flow 3 Intermediate Func Final Reasoning  Strategist<br>State  • Identify instrumentation targets<br> Interprocedural   Flow 1 Sink Source Func • Set breakpoints & expressions<br>Propagation Graph • Determine triggering modality<br> Dual-view Input Representation<br>Taint-relevant Anchor Cue Binding Verifier Explorer<br>Flow Extraction & Anchoring struct _IO_FILE * file = fopen(... //Source %30 = call %_IO_FILE* @fopen(i8* %29, i8* getelementptr inbounds ... ••• PoC generation & executionAnalyze ExploitabilityDetect Latent Errors ••• Diagnose failure contextProbe alternative statesFeedback for refinement<br>long lVar7 = //Memory Access %ptr = getelementptr<br>Src Sink    *(long *)(param_2 + 0x48); %struct.ppm_source_struct i32 0, i32 4  PoC  Feedback<br> ... %190 = getelementptr inbounds i8,   Tools  Debugger (Radare2; Valgrind)<br>Src Sink *(undefined *)(lVar7 +         ptr %184, i64 %189<br>(int)(uint)local_28);//Sink %191 = load i8, ptr %190, align 1<br> Witness-backed Flows  Decompiled Function  LLVM IR Confirmed Vulnerability / False Positives<br><!-- End of picture text -->

**Figure 3: The workflow of Veritas, organized as static grounding, controlled LLM reasoning, and runtime grounding. (1) The** **_Semantic-driven Context Slicer_ extracts witness-backed flows with taint-relevant anchor cues from stripped binaries without LLMs. (2) The** **_Dual-view Vulnerability Detector_ reasons step-wise along these flows, consulting LLVM IR at anchored functions where decompiled code is ambiguous. (3) The** **_Automatic Vulnerability Validator_ confirms or rejects candidates through multi-agent debugger instrumentation and execution.** 

A candidate is confirmed only when concrete runtime evidence corroborates the reported sink, access pattern, and root cause. Across all stages, Veritas combines deterministic program analysis, controlled LLM reasoning, and executable validation, ensuring that conclusions are anchored in verifiable program semantics rather than unconstrained model speculation. 

## **3.2 Semantic-driven Context Slicer** 

A fundamental challenge in binary vulnerability detection lies in the extreme imbalance between program size and vulnerabilityrelevant semantics: only a small fraction of instructions participate in exploitable behaviors, while the majority constitute benign control logic. Directly feeding whole functions or binaries into LLMs, therefore, introduces substantial noise and quickly exceeds practical context budgets [27]. To address this challenge, we design a Semantic-driven Context Slicer that operates entirely without LLMs and extracts compact, vulnerability-relevant context from stripped binaries. The _Slicer_ takes as input a stripped binary B and produces a set of candidate vulnerability flows Π = { _𝜋_ 1 _, . . . , 𝜋𝑀_ }. Each flow object _𝜋_ contains an ordered sequence of recovered functions ( _𝑓_ 1 _, . . . , 𝑓𝑁_ ) connecting an attacker-controlled input to a securitysensitive memory operation, together with compact grounded labels derived from the underlying propagation of the taint. 

_3.2.1 Interprocedural Propagation Graph Construction._ Memory corruption vulnerabilities typically arise from the interprocedural propagation of memory-relevant values, such as pointers, offsets, 

lengths, allocation states, and aliases, whose interactions eventually lead to unsafe access or misuse. To capture these dependencies in a binary, the _Slicer_ first lifts B with RetDec [9] into LLVM IR. Rather than constructing a monolithic SVF-style sparse value-flow graph for the whole program, the current implementation extracts an inter-procedural fact base P directly from the lifted IR. This fact base includes per-function instructions, SSA def-use chains, call relations, actual-to-formal parameter mappings, return-value propagation, summaries of global accesses, pointer manipulation records, and sink-related facts. From P, the slicer materializes a typed interprocedural propagation graph GP = (F _,_ E _,𝜅, 𝜇_ ), where F is the set of recovered functions, E ⊆F × F is the set of interprocedural propagation edges, _𝜅_ : E →{call _,_ return _,_ global} assigns each edge a propagation kind, and _𝜇_ stores the metadata required to transfer taint across that edge, such as actual-to-formal mappings, return-value mappings, or the global object associated with a write-read dependency. This graph is more structured than a call graph because it encodes how taint-relevant values may propagate across calls, returns, and shared global state, while remaining lighter than a fully general whole-program memory model. 

RetDec also produces decompiled C for the same recovered functions. In Veritas, LLVM IR and decompiled code are heuristically paired at function granularity, supporting the subsequent _Detector_ , which uses IR to localize tokens and operations relevant to vulnerability, while performing most semantic reasoning over the body of the corresponding decompiled function. 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Xinran Zheng, Alfredo Pesoli, Marco Valleri, Suman Jana, and Lorenzo Cavallaro 

_3.2.2 Witness-based Flow Extraction._ The graph GP defines the interprocedural search space, but reachability alone is insufficient to establish a vulnerability-relevant flow. To avoid treating every reachable source-sink pair as meaningful, the _Slicer_ verifies whether taint propagates along a bounded interprocedural witness. Let F _𝑠𝑟𝑐_ ⊆F and F _𝑠𝑖𝑛𝑘_ ⊆F denote functions containing predefined sources and sinks, respectively. Sources include inputintroducing calls such as recv, fgets, and fread, while sinks are CWE-specific memory-risk patterns such as dangerous API arguments and memory-safety-relevant pointer operations. 

For source function _𝑓_ 0 ∈F _𝑠𝑟𝑐_ , the _Slicer_ initializes a set of tainted LLVM-IR tokens. A candidate witness is a bounded path _𝑒_ 0 _𝑒𝑘_ −1 _𝑤_ : _𝑓_ 0 −→ _𝑓_ 1 · · · −−−→ _𝑓𝑘_ , where _𝑓𝑘_ ∈F _𝑠𝑖𝑛𝑘_ . The witness is checked automatically at each function boundary. Within the current function _𝑓𝑖_ , the checker first expands the taint set through bounded local def-use chains, load/store links, argument aliases, pointer manipulation patterns, and lifted-IR memory-staging patterns. It then maps the expanded taint set across the outgoing edge _𝑒𝑖_ = ( _𝑓𝑖, 𝑓𝑖_ +1) ∈E using the edge kind _𝜅_ ( _𝑒𝑖_ ) and metadata _𝜇_ ( _𝑒𝑖_ ), such as parameter mappings for calls, return propagation for return edges, and global access summaries for global dependencies. If no tainted token can be transferred at any step, the candidate witness is rejected. A witness is accepted only when taint reaches a dangerous API argument or memory-safety-relevant pointer operation in _𝑓𝑘_ . 

Given an accepted witness _𝑤_ , the _Slicer_ constructs the candidate flow _𝜋_ = ( _𝑓_ 1 _, . . . , 𝑓𝑁_ ) from the ordered witness functions. It then performs a bounded enrichment step to retain helper frames that are locally necessary to interpret the flow, such as callees on the same branch that receive the same tainted SSA value, helper functions near the sink that prepare required inputs, or wrappers that forward return values based on local IR evidence. These additions must remain consistent with the witness through SSA provenance, field or global tags, and equivalent taint propagation; frames without such evidence are omitted. The resulting flow is therefore a compact context object containing the source, sink, ordered frames, perfunction taint-relevant tokens, and the underlying witness path, rather than a classical complete program slice. 

_3.2.3 Witness Slice Structure._ In the current implementation, anchoring is realized through the structure of the flow object itself. Each retained function carries a compact grounded label _ℓ𝑛_ , denoting the specific taint-relevant value, shared object tag, or sink-relevant operand to be tracked at that function; source and sink functions additionally receive endpoint annotations derived from verifier-supported tokens and callsite information. The _Slicer_ also assigns each retained function a provenance class: witness, global_proven, defuse_proven, or context_only, which indicates whether its presence is backed by the verified witness path, by global-state or local structural evidence, or retained solely for continuity. A compact witness slice that suppresses purely contextual functions is emitted alongside the full slice. 

Together, the propagation tokens, endpoint annotations, and provenance classes constitute the _anchor cues_ A( _𝑓𝑛_ ) attached to each retained function in the flow. These cues encode what the _Detector_ should track at each function and how strongly the function’s presence is evidentially grounded. A binary may yield multiple such 

flow objects, each passed to the _Detector_ for vulnerability reasoning and then to the _Validator_ for runtime confirmation. 

## **3.3 Dual-view Vulnerability Detector** 

Given the candidate flows Π produced by the _Slicer_ , the _Detector_ performs step-wise reasoning over statically grounded, witnessbacked traces. The LLM is not responsible for discovering taint propagation from the whole binary by itself; instead, propagation is precomputed by the _Slicer_ and provided as a fixed interprocedural context. The _Detector_ analyzes this context to recover the missing reasoning dimensions, including control-flow feasibility, object correspondence, and arithmetic bound constraints, to determine whether the flow is vulnerability-relevant. Flows judged as potentially vulnerable are then forwarded to the _Validator_ for dynamic confirmation. Algorithm 1 summarizes the procedure. 

_3.3.1 Dual-view Input Representation._ Let _𝐷_ ( _𝑓𝑡_ ) denote the decompiled code of function _𝑓𝑡_ , and let _𝐼_ ( _𝑓𝑡_ ) denote its lifted LLVM IR, both produced by RetDec. The _Detector_ adapts the input representation of each function according to its role in the flow, using the anchor cues A( _𝑓𝑡_ ) to identify the specific tokens and operations relevant at each step. This design is motivated by the semantic loss of decompilation (Section 2.1.2): decompiled code provides a concise representation for control-flow and constraint reasoning, but it often collapses memory operations into offset expressions, making object identity and sink semantics ambiguous. Lifted IR is therefore consulted at source and sink functions, where taint alignment or sink semantics require disambiguation. Formally, the function view is defined as: 


![](docs/paper-research/md-downloaded-paper-professor/images/04-veritas-semantically-grounded-agentic-framework-for.pdf-0006-11.png)


When dual-view is triggered, the prompt presents both representations together with the relevant endpoint annotations from A( _𝑓𝑡_ ). At intermediate functions, the _Detector_ reasons over _𝐷_ ( _𝑓𝑡_ ) alone; the propagation tokens in A( _𝑓𝑡_ ) identify which value to track, while the provenance class indicates the evidential strength of the function’s presence in the flow. 

_3.3.2 Step-wise Reasoning._ Analyzing an entire flow in a single LLM invocation is impractical: the combined IR and decompiled code of all functions can exceed context limits, and fine-grained semantic attention degrades with input length [27]. We therefore analyze each flow one function at a time, carrying forward the reasoning state through the accumulated prompt-response history of the current flow prefix and a running buffer and bounds inventory. This inventory records propagated values, memory-object aliases, and bound-related constraints needed for sink verification. 

For notation, we use S _𝑛_ as a conceptual abstraction of the _Detector_ ’s accumulated reasoning after processing the prefix ( _𝑓_ 1 _, . . . , 𝑓𝑛_ ), rather than as a separately materialized program-analysis object. At each step, the prompt asks the model to update this state only when the current function provides evidence that adds, refines, or invalidates prior facts. Let Φ _𝜃_ denote the step-wise LLM detector. The update at step _𝑛_ is written as: 


![](docs/paper-research/md-downloaded-paper-professor/images/04-veritas-semantically-grounded-agentic-framework-for.pdf-0006-15.png)


Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Veritas: A Semantically Grounded Agentic Framework for Memory Corruption Vulnerability Detection in Binaries 

where R( _𝑓𝑛_ ) is the role-dependent function representation and A( _𝑓𝑛_ ) is the anchor cues comprising the propagation token, provenance class, and, for source or sink functions, endpoint annotations. 

The prompts are specialized according to the function’s role in the flow. At the source step, the _Detector_ maps the IR taint label into the decompiled view and initializes the inventory of propagated values and bound-related facts. Intermediate steps incrementally update this inventory through assignments, arithmetic, and controlflow decisions that affect feasible propagation. At the sink step, the _Detector_ maps the sink label to the corresponding operation and performs end-to-end path-sensitive verification, including branch feasibility and bound consistency. 

_3.3.3 Trie-based Flow Memoization._ Many candidate flows share prefixes, especially when they originate from the same parsing logic or reach nearby sinks. Recomputing the reasoning state for each flow, therefore, causes redundant LLM invocations. However, reuse must distinguish flows that traverse the same recovered functions but track different vulnerability-relevant values or sink operands. Veritas memoizes prefixes using the compact representation passed from the _Slicer_ to the _Detector_ . Each retained function contributes a key element _𝑞𝑖_ = ( _𝑓_<sup>˜</sup> _𝑖, ℓ𝑖_ ), where _𝑓_<sup>˜</sup> _𝑖_ is the recovered function identifier in the emitted flow, and _ℓ𝑖_ is the compact grounded label attached to that function. In implementation, _𝑞𝑖_ is serialized as fn:@:data; the data field identifies the value or operand to track, but is not the full internal taint state maintained by the _Slicer_ . 

The cache C is a prefix trie over these key elements. A root-todepth path _𝑛_ represents: 


![](docs/paper-research/md-downloaded-paper-professor/images/04-veritas-semantically-grounded-agentic-framework-for.pdf-0007-06.png)


and stores the reasoning state S _𝑛_ after that prefix. For a new flow, the _Detector_ resumes from the longest exactly matched prefix and invokes the LLM only on the remaining suffix. Thus, reuse occurs only when two prefixes expose the same ordered function identifiers and grounded labels. 

_3.3.4 Consistency Checking and Decision._ After reaching the sink function _𝑓𝑁_ , the _Detector_ does not directly treat the final semantic state S _𝑁_ as the verdict. Instead, it performs a final path-sensitive verification over flow _𝜋_ = ( _𝑓_ 1 _, . . . , 𝑓𝑁_ ) based on the accumulated semantic-state sequence (S1 _, . . . ,_ S _𝑁_ ). It checks whether the tainted value remains vulnerability-relevant when propagated along _𝜋_ to the sink memory operation, rather than being sanitized, overwritten, or range-constrained to safety by intermediate steps. If the required branch conditions are infeasible, the flow is rejected. 

For the sink access under verification, the _Detector_ first checks whether the accessed value is still transitively derived from the root taint label along a feasible propagation chain. It then reconstructs the valid bounds of the accessed object from upstream code and compares them with the effective sink access. A flow is reported as vulnerable only when both conditions hold: the tainted propagation to the sink is feasible, and the reconstructed bound check shows that the sink access violates memory safety. This decision stage applies structured semantic and arithmetic checks while prioritizing recall, so that genuinely present vulnerabilities are not missed at discovery time; stricter confirmation and false-positive filtering are deferred to the downstream _Validator_ . If multiple tainted sink accesses within 

the same flow correspond to the same verified violation, they are merged into a single report entry before validation. 

## **3.4 Automatic Vulnerability Validator** 

The _Detector_ produces a vulnerability hypothesis over statically grounded flow objects, but this hypothesis still must be tied to executable program behavior. The _Validator_ , therefore, serves as a second grounding stage: it translates detector outputs into debuggervisible artifacts and tests them against concrete runtime observations. Rather than asking an LLM to decide whether a candidate is real in isolation, Veritas constrains validation to auditable tool interactions over the target binary. This design lets agents plan and diagnose validation attempts while requiring final confirmation to come from executable evidence. 

_3.4.1 Artifact Preparation._ Before validation, Veritas constructs an artifact layer that bridges static reasoning and runtime analysis. The goal is to align detector hypotheses expressed over RetDecrecovered functions and flow objects with the symbols, addresses, and code views used during debugging. To this end, the target binary is analyzed using Radare2 [37] and its decompiler backend to materialize structured pseudo-code representations (pddj) for the slice functions. RetDec-recovered function names and addresses are mapped to radare2 functions, and relative virtual addresses (RVAs) are computed for the reported functions and sink locations. 

This artifact layer ensures that validation operates on executable coordinates rather than only on decompiler-local descriptions. When necessary, explanations produced against the RetDec view are rewritten into the radare2/r2dec view so that breakpoints, watched expressions, and memory inspections refer to the same runtime objects. The resulting artifacts are serialized as structured JSON records containing the mapped functions, RVAs, pseudo-code, detector hypothesis, and relevant flow context, providing a consistent grounding interface for the validation agents. 

_3.4.2 Automatic Framework._ Building on the prepared artifacts, the validator orchestrates three agents: _Strategist_ , _Verifier_ , and _Explorer_ , to test each detector hypothesis against runtime evidence. The _Validator_ is not merely a downstream false-positive filter; it is a runtime grounding layer that constrains reasoning through executable artifacts, debugger observations, and memory-checking oracles. A candidate is validated only when evidence supports the reported sink, access pattern, and root cause. 

_Strategist:_ It is the planning component that converts the detector’s hypothesis into an executable validation plan. It takes as input a report of _Detector_ , the witness-backed flow object, the mapped artifact layer, and the target binary. From these inputs, it resolves the reported vulnerability into runtime-checkable targets, including the sink location, relevant symbol, memory region, and input channel. It then selects the functions and program points to instrument, translates them into breakpoints and symbolic observations, chooses the triggering modality (e.g., file, command line, network), and defines the observable conditions under which the hypothesis should be considered confirmed or refuted. When previous validation attempts fail, the _Strategist_ incorporates feedback from the _Verifier_ and _Explorer_ to revise the plan and avoid redundant probes. 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Xinran Zheng, Alfredo Pesoli, Marco Valleri, Suman Jana, and Lorenzo Cavallaro 

The output is a structured validation plan that specifies how to exercise the binary and what runtime evidence must be collected. 

_Verifier:_ It executes the validation plan and collects runtime evidence. Guided by the _Strategist_ ’s plan, it prepares the input channel, generates or adapts PoCs, and runs the target binary under debugging tools with controlled breakpoints. Its goal is not merely to trigger a crash, but to determine whether the observed runtime behavior supports the reported sink, access pattern, and root cause. If execution produces a segmentation fault, the _Verifier_ checks whether the crash location and trace match the detector hypothesis. When no explicit crash occurs, it invokes Valgrind [47] to inspect invalid accesses and object-lifetime violations. There are also cases where Valgrind reports no errors, e.g., stack-based off-by-one bugs; for these cases, the _Verifier_ relies on targeted breakpoints and memory inspection to check whether the relevant memory region is modified or accessed consistently with the predicted vulnerability. 

_Explorer:_ It is activated when the _Verifier_ cannot obtain sufficient evidence from the current plan. It does not change the vulnerability hypothesis under test; instead, it reruns the same PoC with supplementary breakpoints, symbols, and memory observations to search for nearby evidence. This may extend beyond the original slice to functions related to branch conditions, input sanitization, or intermediate states needed to trigger the bug. The results are returned to the _Strategist_ to refine the next validation plan. 

Together, the three agents operate a reasoning, execution and feedback loop, which repeats until either a vulnerability is confirmed, ruled out, or the system reaches the maximum iterations to control computational cost and prevent endless exploration. 

## **4 Evaluation** 

We conducted comprehensive experiments to evaluate Veritas and answer the following research questions: 

- **RQ1.** How effective is Veritas at detecting binary-level memory 

- corruption vulnerabilities compared to existing approaches? **RQ2.** What are Veritas’ cost-accuracy trade-off and bottlenecks? **RQ3.** How do components contribute to detection effectiveness? 

## **4.1 Experiment Setup** 

We implement Veritas as a modular analysis pipeline that combines deterministic static analysis with LLM-based reasoning and runtime validation. RetDec [9] is used to lift binaries into LLVM IR and decompiled C. The Slicer is implemented by defuse, a custom LLVMIR analysis framework that extracts program facts, materializes a typed interprocedural propagation graph over call, return, and global dependencies, and performs bounded witness verification using a Rust-backed CompactIR verifier. The Detector operates over the emitted witness-backed flow objects and uses GPT-5.4 [35] for step-wise dual-view reasoning with prefix reuse; it is not a multi-agent component. The Validator is implemented as a multiagent runtime-confirmation stage using AutoGen [52], Radare2 [37], and Valgrind [47] to translate detector hypotheses into executable validation plans and concrete evidence. 

**Table 1: Statistics of the evaluated projects. #IR Inst. and #Func report the size of LLVM IR instructions and source code functions of the analyzed binary; #Vuln_files is the number of source files in the vulnerability trace, and #Vuln is the number of ground-truth vulnerabilities in each commit.** 

|**ID**|**Project**|**Commit**|**Binary**|**#IR Inst.**|**#Func**|**#Vuln_fles**|**#Vuln**|
|---|---|---|---|---|---|---|---|
|P1|matio|64f7936|matdump|36,075|330|3|2|
||matio|55e506b|matdump|37,588|334|4|3|
|P2|libexif|a918830|exif|27,737|385|2|1|
||libexif|d0ebd6e|exif|19,988|380|3|1|
|P3|libsndfle|b0d7f5b|sndfle-info|126,238|1,608|4|1|
||libsndfle|1d928bf|sndfle-deinterleave|125,410|1,530|5|1|
|P4|gifib|52b62de|gif2rgb|11,370|133|2|2|
|P5|libheif|fd0c01d|heif-convert|78,396|2,141|5|1|
|P6|libtif|1bdbd03|tifcrop|107,603|1,601|1|1|
|P7|jhead|11e6e87|jhead|11,305|65|2|2|
|P8|ezxml|dcb1748|ezxml|6,876|33|1|2|
|P9|libredwg|5f99814|dwg2SVG|966,014|1,781|3|1|
||libredwg|93c2512|dwg2dxf|4,067,615|2,757|2|1|
|P10|faad2|1073aee|faad|77,227|609|1|1|



## **4.2 Dataset and Ground Truth** 

Existing vulnerability datasets [33, 38] typically label vulnerable commits, functions, or crashing inputs, but do not provide the interprocedural source-to-sink propagation and runtime feasibility evidence needed to evaluate grounded binary vulnerability detection. We therefore construct a fine-grained dataset of real-world out-of-bounds vulnerabilities with flow-level annotations. Samples are collected from SEC-Bench [24], ARVO [29], and official repositories of widely used open-source projects with CVE identifiers. Each sample must satisfy four criteria: (1) the PoC can be executed against the native binary via file, command-line, or network input; (2) the project compiles into a working executable; (3) the vulnerable function is preserved in the compiled binary; and (4) the vulnerability path remains recoverable in decompiled representations. The final dataset contains 20 samples from 10 projects across 14 commits, with statistics shown in Table 1. 

For each vulnerability, we reproduce the public PoC in a Docker environment and collect concrete failure evidence using AddressSanitizer and Valgrind. Based on crash reports, CVE descriptions, and code-level evidence, we annotate the vulnerability source, sink, triggering flow, and root cause. Each annotation is constructed by one author and independently checked by another, with all final annotations manually verified. LLMs are used only to assist candidate descriptions and intermediate reasoning artifacts. 

This process is inherently labor-intensive: constructing the current dataset required over 40 person-days of expert effort, excluding build and regression-test engineering overhead. This highlights a broader bottleneck: scaling high-quality vulnerability datasets requires substantial manual investment. To address this, we are working on releasing the dataset publicly and designing it to support incremental community contributions, enabling broader participation in dataset expansion. We emphasize that such curated, high-fidelity datasets are essential for advancing LLM-based vulnerability detection, where noisy or weakly-labeled data can both limit real progress and create misleading gains. 

We compile each project with -O0 optimization, stripping debugging symbols, and using the resulting binaries as inputs to Veritas. 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Veritas: A Semantically Grounded Agentic Framework for Memory Corruption Vulnerability Detection in Binaries 

## **4.3 Baseline** 

_4.3.1 Baseline Selection._ To evaluate Veritas comprehensively, we compare Veritas against seven representative baselines from four categories: source-code static analysis, binary analysis, dynamic fuzzing, and agent-driven auditing. Although Veritas operates exclusively on binaries, we deliberately include strong source-code-based baselines to provide a broader and more meaningful evaluation. This setting is inherently favorable to the baselines, since source code exposes richer semantic information than binaries, and thus serves as a stricter test of Veritas’ effectiveness. 

_Source-code static analysis._ We include two industry-standard analyzers. _Meta Infer_ [30] represents deep inter-procedural static reasoning based on separation logic, and _Semgrep_ [39], a lightweight rule-based analysis over AST patterns. We adopt the enhanced rules by experts [1] to strengthen Semgrep on memory corruptions. 

_Binary analysis._ We compare against _cwe_checker_ [17], a specialized and widely-used binary scanner based on data-flow analysis and symbolic execution with Ghidra [31] support. 

_Dynamic analysis._ We adopt _AFL++_ [4] as the representative fuzzing baseline, since fuzzing is a standard dynamic strategy for exposing memory-safety violations through concrete execution. All targets are recompiled with AFL++ instrumentation and sanitizers enabled; each sample is fuzzed for 8 hours on 3 parallel cores with 5 initial seeds in isolated Docker environments. 

_Agent-driven auditing methods_ We include three source-codebased Agentic baselines, since no public agent framework currently supports binary memory corruption detection. _RepoAudit_ [20] is a repository-level multi-agent auditing system with on-demand inter-procedural path construction; we use GPT-5.4 [35] as its base model. To keep the comparison practical and cost-bounded, and to separate vulnerability reasoning from repository-scale file localization, we run RepoAudit in a file-scoped upper-bound configuration: its search is restricted to files within the benchmark’s vulnerable region, following the file-scoping strategy used by BugScope [19]. We report this setting explicitly as favorable to RepoAudit rather than as a fully unconstrained repository audit. We also include _Codex_ [34] (GPT-5.4) and _Claude Code_ [5] (Opus 4.6) as frontier code agents. For both agents, we provide identical repository access, build/test permissions, and a two-hour audit budget. As their internal stopping criteria are not externally controllable, this serves as an upper-bound budget rather than a fixed runtime. 

_4.3.2 Evaluation Protocol._ We evaluate all methods against the curated ground truth. For source code-based methods, including static analyzers and agent-based approaches, GPT-5.4 [35] assists semantic matching between reported findings and benchmark vulnerabilities; all matches are then reviewed by four security experts. For binary-based methods, where exhaustive manual matching is prohibitively labor-intensive, we use an automated mapping pipeline that recovers binary base addresses, maps reports to the ELF layout, and resolves source-level function information with addr2line. A ground truth vulnerability is counted as a true positive (TP) if at least one reported finding matches its fine-grained annotation; otherwise, it is a false negative (FN). Multiple reports matching the same vulnerability are counted once. We report TP, FN, and Recall. For readability, detection results are aggregated by project ID when they share multiple vulnerable commits. 

Any baseline finding that does not match a ground-truth vulnerability is counted as a false positive (FP). For Veritas, FP accounting follows its two-stage pipeline: the _Detector_ first emits candidates, and the _Validator_ confirms or rejects them through runtime evidence. Since validation cost scales with the number of detector candidates, we select 7 project-commits covering 9 samples as the exhaustive validation subset and validate all candidates. For the remaining larger candidate sets, we validate a sampled subset and report the number of checked candidates and observed FPs. Unless otherwise stated, validation coverage uses non-deduplicated candidate, where each raw detector output is one validation task. Veritas’s FPR outside the exhaustive subset is reported as a sampled audit estimate over validated candidates rather than as an exact whole-population FPR, whereas TP, FN, and recall are computed against the ground truth for all the benchmark vulnerabilities. 

## **4.4 RQ1: Effectiveness on Detecting BMCVs** 

We apply Veritas and all baselines on our curated dataset. The detection results are shown in Table 2. Traditional static and dynamic tools are ineffective on BMCVs because they lack the semantic grounding needed to reconstruct memory object lifecycles across functions. All three static analyzers achieve zero recall: Meta Infer [30] over-approximates complex flows and yields 299 false positives in the exhaustively validated subset (Table 3), Semgrep [1] mainly matches syntactic patterns of unsafe code, and cwe_checker [17] is limited to narrowly defined binary CWE patterns. AFL++ [4] reaches only 10% recall (2/20) with zero false positives. While every AFL++ finding corresponds to a concrete crash, its low recall reflects the difficulty of reaching deep, pathsensitive triggering conditions through random seed mutation within a bounded fuzzing budget. 

The agentic baselines improve over traditional tools but remain limited by ungrounded candidate generation. RepoAudit [20] detects 6 of 20 vulnerabilities (30.00%) under the favorable file-scoped upper-bound configuration outlined in Section 4.3.1, mostly from P1, but its call-chain exploration still misses propagation through shared state or structure-mediated dependencies. Codex [34] and Claude Code [5] reach 25.00% and 35.00% recall, respectively. Despite their ability to inspect repositories, compile targets, and run validation, their main bottleneck is detection: they lack an explicit model of memory object lifecycles, constraining candidate generation around allocation, propagation, bounds, and unsafe consumption. As a result, they explore broadly and report surface-level suspicious patterns. Claude Code produces 186 FPs in the exhaustively validated subset (Table 3), indicating that execution capability alone cannot rescue incorrect vulnerability hypotheses. 

Veritas achieves 90.00% recall (18/20), substantially outperforming all baselines. For candidate-level precision, the _Validator_ exhaustively checks 623 _Detector_ candidates across 9 samples from 7 project-commits and reports zero false positives (Table 3). For the remaining larger projects, where exhaustive validation is prohibitively expensive (Table 4), we validate a 10% sample of 3,344 candidates and identify 2 false positives (Table 7). These results show that Veritas achieves high recall while keeping observed false positives low under both exhaustive and sampled validation. 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Xinran Zheng, Alfredo Pesoli, Marco Valleri, Suman Jana, and Lorenzo Cavallaro 

**Table 2: Ground-truth vulnerability detection results of Veritas and baseline methods. Each project-method cell reports TP/FN over the curated vulnerabilities in that project. The final rows report aggregate TP/FN and overall recall across all evaluated projects. “N/A” indicates that the method produced no applicable result for the target vulnerability class.** 

|ID|#Vuln|Meta Infer [30]|Semgrep [1]|cwe_checker [17]|AFL++ [4]|RepoAudit [20]|Codex [34]|Claude Code [5]|Veritas|
|---|---|---|---|---|---|---|---|---|---|
|||TP/FN|TP/FN|TP/FN|TP/FN|TP/FN|TP/FN|TP/FN|TP/FN|
|P1|5|0/5|0/5|0/5|1/4|5/0|1/4|1/4|3/2|
|P2|2|0/2|0/2|0/2|1/1|0/2|1/1|1/1|2/0|
|P3|2|0/2|0/2|0/2|0/2|0/2|0/2|0/2|2/0|
|P4|2|0/2|0/2|0/2|0/2|0/2|2/0|2/0|2/0|
|P5|1|0/1|0/1|N/A|0/1|0/1|0/1|0/1|1/0|
|P6|1|0/1|0/1|0/1|0/1|0/1|0/1|0/1|1/0|
|P7|2|0/2|0/2|0/2|0/2|0/2|0/2|0/2|2/0|
|P8|2|0/2|0/2|0/2|0/2|0/2|0/2|1/1|2/0|
|P9|2|0/2|0/2|N/A|0/2|0/2|0/2|1/1|2/0|
|P10|1|0/1|0/1|0/1|0/1|1/0|1/0|1/0|1/0|
|Total TP/FN|20|0/20|0/20|0/20|2/18|6/14|5/15|7/13|18/2|
|Recall (%)|-|0.00|0.00|0.00|10.00|30.00|25.00|35.00|90.00|



**Table 3: False Positives (FPs) in the Exhaustively Validated Subset.** 

|Project|Commit|#Vuln|Meta Infer[30]|Semgrep [1]|cwe_checker[17]|AFL++[4]|RepoAudit[20]|Codex[34]|Claude Code[5]|Veritas|
|---|---|---|---|---|---|---|---|---|---|---|
|libredwg|5f99814|1|144|15|N/A|0|2|3|8|0|
|libexif|d0ebd6e|1|0|4|0|0|0|4|12|0|
|libsndfle|b0d7f5b|1|41|8|30|0|5|3|7|0|
|libheif|fd0c01d|1|28|2|N/A|0|0|3|16|0|
|gifib|52b62de|2|7|3|10|0|13|2|131|0|
|jhead|11e6e87|2|10|21|2|0|1|2|5|0|
|faad2|1073aee|1|69|26|51|0|0|7|7|0|
|Tota|l FP|9|299|77|93|0|21|24|186|0|



**Table 4: Exhaustive Cost Extrapolation of Veritas.** 

|**Accounting choice**|**#defuse fows**|**#Detected Cand.**|**Discovery time @50 threads**|**Discovery API cost**|**Estimated Validator time**|**Estimated Validator cost**|
|---|---|---|---|---|---|---|
|no deduplication|11,901|3,967|33.40h|$1,190.10|12.67days|$7,140.60|
|deduplicated|7,898|2,633|22.16h|$789.80|8.41days|$4,738.80|



## **4.5 RQ2: Cost Analysis** 

RQ2 examines the cost distribution of Veritas and the practicality of exhaustive validation. Table 4 shows that runtime validation dominates the overall budget. Under non-deduplicated accounting, 11,901 defuse flows produce 3,967 detector candidates. Exhaustively validating them would require 33.40 hours of Discovery on 50 threads ($1,190.10) and an estimated 12.67 days of Validator time ($7,140.60). After Content-level deduplication, although the cost reduces roughly 30%, it still costs more than $5.5k. This cost is largely a consequence of binary-level analysis rather than a frameworkspecific inefficiency. Unlike source-code analysis, stripped binaries lack reliable types, symbols, object boundaries, and high-level control structures. As a result, Veritas must reconstruct propagation from lifted IR, align memory-level evidence with decompiled code, and validate hypotheses through low-level debugger-visible behavior. The _Slicer_ is deterministic and LLM-free, while the _Detector_ is parallelizable and benefits from trie-based prefix memoization. The _Validator_ remains the main bottleneck, costing roughly $1.80 per 

candidate, because each attempt may require PoC construction, debugger instrumentation, memory inspection, and retry loops. These results justify our mixed validation protocol: exhaustive validation for tractable projects, where Veritas reports zero false positives, and sampled validation for larger projects. Thus, the main scalability bottleneck is runtime confirmation, while static grounding and detection remain comparatively scalable. This cost-precision trade-off is characteristic of stripped-binary vulnerability detection: achieving high precision requires executable evidence that static reasoning alone cannot provide. Veritas prioritizes detection reliability over throughput, a design choice that reflects the high cost of missed vulnerabilities in security-critical binary analysis. 

## **4.6 RQ3: Component Effectiveness** 

In this section, we examine whether the three stages of Veritas contribute to the final detection pipeline in the intended way. 

The _Slicer_ constructs compact yet semantically complete contexts from stripped binaries. To test this, we compare its context construction with call-graph expansion under hop budgets from 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Veritas: A Semantically Grounded Agentic Framework for Memory Corruption Vulnerability Detection in Binaries 

**Table 5: Effect of** **_Slicer_ context construction. Sink Cov. and Flow Cov. denote sink and full-trace coverage, Func Con. denotes function connectivity along traces, and Avg. #Funcs is average context size.** 

|Context|Sink Cov.|Flow Cov.|Flow Con.|Avg. #Funcs|
|---|---|---|---|---|
|CG-1|4/20|3/20|3/20|7.2|
|CG-2|14/20|11/20|6/20|136.4|
|CG-3|18/20|17/20|6/20|269.1|
|CG-4|20/20|20/20|6/20|408.9|
|CG-5|20/20|20/20|6/20|446.1|
|_Slicer_|20/20|20/20|20/20|5.16|



**Table 6:** **_Detector_ on the exhaustive subset. #Flows are witnessbacked slicer outputs, #Cand. are** **_Detector_ candidates, and TP/FN are detected and missed ground-truth vulnerabilities.** 

|Project|Commit|#Flows|#Cand.|TP/FN|
|---|---|---|---|---|
|libredwg|5f99814|451|144|1/0|
|libexif|d0ebd6e|155|70|1/0|
|libsndfle|b0d7f5b|1,069|313|1/0|
|libheif|fd0c01d|146|47|1/0|
|gifib|52b62de|27|12|2/0|
|jhead|11e6e87|47|15|2/0|
|faad2|1073aee|80|22|1/0|
|Total||2,002|623|9/0|



**Table 7: False positive analysis of Veritas under nondeduplicated accounting. #Cand. are raw detector candidates, #Validated are validator-checked candidates, and Coverage denotes the validated fraction.** 

|Subset|#Vulns|#Cand.|#Validated|Coverage|FP|
|---|---|---|---|---|---|
|Exhaustive Validation|9|623|623|100%|0|
|Sampled Validation|11|3,344|334|10%|2|
|Total|20|3,967|957|24.12%|2|



This filtering is essential for downstream validation: without it, the _Validator_ would face over three times as many candidates under an already expensive per-candidate budget (Section 4.5). 

Table 7 then evaluates the _Validator_ ’s false positive filtering under non-deduplicated accounting. In the exhaustive subset, the _Validator_ checks all 623 detector candidates and produces zero false positives. In the partial-validation subset, it validates 334 of 3,344 candidates (10%) and identifies 2 manually confirmed false positives. Overall, Veritas validates 957 of 3,967 candidates (24.12%) with only 2 observed false positives, compared with 10-617 false positives from baselines on the same exhaustive subset (Table 3). These results confirm that removing any single stage would either inflate the candidate space beyond tractable validation, miss groundtruth vulnerabilities, or leave infeasible hypotheses unfiltered. 

## **4.7 Failure Case Analysis** 

Veritas missed two samples in P1, both share the same root cause: incomplete binary recovery by RetDec at the function preamble. In these samples, part of the local object initialization was absent from both the decompiled C and the lifted LLVM IR. The _Slicer_ recovered the correct source-to-sink flows, but the _Detector_ could not reconstruct the true extent of the destination object: it identified the correct vulnerability class and missing-boundary condition, but hypothesized a smaller object than actually existed. Under our ground-truth protocol, these are counted as false negatives because the reported triggering condition did not match the actual vulnerability semantics. These false negatives then produced two false positives: the _Validator_ confirmed that the program could perform the write length hypothesized by the Detector, but because the vulnerable object was embedded within a larger stack-allocated structure, the write fell within the true bounds and produced neither a crash nor a Valgrind-detectable violation, leaving the _Validator_ without a stronger oracle to reject the claim. We classify these as a coupled failure mode caused by representation loss in the recovered binary artifacts: an incorrect boundary hypothesis at detection time propagated through validation, yielding two false positives. 

## **4.8 Real-world Application** 

CG-1 to CG-5, measuring sink coverage, full-trace coverage, correct propagation connectivity, and average context size over all 20 ground-truth vulnerabilities. Table 5 shows that call-graph expansion requires at least 4 hops to cover all sinks. Still, even at CG-4 and CG-5, only 6 of 20 cases achieve correct propagation connectivity, because call-chain traversal cannot capture shared-state dependencies that bypass direct caller-callee edges. This coverage also comes at high context cost: CG-4 averages 408.9 functions per flow. In contrast, the _Slicer_ achieves 20/20 on all three coverage metrics with only 5.16 functions per flow, confirming that grounding context construction in memory-flow evidence yields both higher semantic completeness and substantially smaller inputs. 

The _Detector_ is expected to reduce this statically grounded search space to a tractable candidate set without losing ground-truth vulnerabilities. Table 6 shows this filtering on the exhaustive subset: the _Slicer_ emits 2,002 witness-backed flows across 7 project-commits, and the _Detector_ narrows these to 623 candidates, a 68.88% reduction, while retaining all 9 ground-truth vulnerabilities (9 TP, 0 FN). 

We apply Veritas to Apple macOS and discover a zero-day out-ofbounds read (CVE-2025-[REDACTED]) in Apple’s Universal Scene Description library (libusd_ms.dylib), which parses glTF assets. The simplified code is shown in Figure 4. 

The vulnerability arises because the glTF format does not enforce that a channel’s sampler index refers to a valid entry in the samplers array. During import, the channel.sampler value, which is attacker-controlled, is parsed by importNodeAnimations. At (1), piVar17 points to the current channel object. At (2), the code loads the sampler field from this channel object into iVar6, yielding an attacker-controlled sampler index. At (3), lVar16 is initialized to the base address of the contiguous buffer underlying the samplers vector. The vulnerability occurs at (4), where the unchecked sampler index is scaled by the sampler-object size and added to this base address. When the index is out of range, the computed pointer lies outside the allocated samplers buffer. This invalid pointer is then to FUN_269bde608 and dereferenced to read the 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Xinran Zheng, Alfredo Pesoli, Marco Valleri, Suman Jana, and Lorenzo Cavallaro 


![](docs/paper-research/md-downloaded-paper-professor/images/04-veritas-semantically-grounded-agentic-framework-for.pdf-0012-02.png)


<!-- Start of picture text -->
void adobe::usd::importNodeAnimations(ImportGltfContext<br> *param_1)<br>{ // ...<br>    lVar14 = *(long *)(*(long *)(param_1 + 8) + 0x18) + uVar19<br>* 0x108;<br>// (1) Point to the current channel entry<br>    piVar17 = *(int **)(lVar14 + 0x18);<br>// ...<br>    if (piVar17 != piVar2) {<br>        lVar13 = lVar13 + uVar19 * 0x40;<br>        do {<br>// (2) Load channel.sampler index<br>            iVar6 = *piVar17;<br>// (3) Load base address of the samplers buffer<br>            lVar16 = *(long *)(lVar14 + 0x30);<br>// (4) Compute sampler address: base + index * 0xe0<br>            lVar16 = lVar16 + (long)iVar6 * 0xe0;<br>// (5) Pass the computed sampler address to FUN_269bde608<br>            iVar7 =<br>FUN_269bde608(uVar18,piVar17,lVar16,&local_188,puVar20 +<br>10,lVar13 + 0x30, lVar13 + 0x34);<br>...<br>}<br>// ...<br>undefined8<br>FUN_269bde608(Model *param_1,long param_2,int<br>*param_3,undefined8 *param_4,long *param_5,<br>             float *param_6,float *param_7)<br>{<br>// (6) OOB read when *param_3 is used as an index<br>  uVar8 = adobe::usd::getAccessorElementCount(param_1,*param_3);<br>  // ...<br><!-- End of picture text -->

**Figure 4: The simplified code of CVE-2025-[REDACTED].** 

sampler’s input field before calling getAccessorElementCount, triggering an out-of-bounds read. 

Starting from UsdGltfFileFormat::Read, the file-loading entry point, the _Slicer_ extracts the glTF flow, tracking the attackercontrolled sampler index through importNodeAnimations into FUN_269bde608. Dual-view reasoning at the source and sink traces the attacker-controlled sampler index from the glTF input through the pointer arithmetic at (4) to the dereference at (6), relating the decompiled offset expression to the lifted-IR memory operation and identifying the missing bounds check. After detection, the _Validator_ constructs a proof-of-concept glTF file with an out-of-range sampler index (e.g., 0x1000000) and executes it under a debugger with a breakpoint at (4), confirming that the computed pointer exceeds the buffer boundary and triggers a crash. 

## **5 Related Work** 

_Memory Corruption Vulnerability Detection._ Memory-corruption vulnerability detection has long relied on static and dynamic analysis. Static techniques, ranging from range analysis to abstract interpretation [18, 48, 58], provide broad coverage but often overapproximate program behavior, yielding infeasible paths and false positives [15]. Dynamic techniques such as fuzzing and concolic execution [10, 12, 22, 40] validate bugs through concrete execution, but struggle with path explosion and deep program states [46]. For binaries, frameworks such as BAP and angr [11, 49] lift executables to intermediate representations for symbolic reasoning, while detectors such as cwe_checker and BinAbsInspector [17, 23] encode common MCV patterns through rule-based or abstractinterpretation-driven analyses. These methods are scalable, but their dependence on handcrafted memory models and vulnerability 

### predicates limits generalization and leaves substantial effort for result interpretation and false-positive reduction. 

_LLM- and Agentic-based Approaches._ Early LLM-based approaches identified vulnerability patterns through fine-tuning [14, 43, 51], but their effectiveness depends on training data quality and often does not transfer to real-world repositories. More recent work combines program analysis structure with LLM capabilities: LLMxCPG [25] uses code property graph slicing to preserve vulnerability-relevant context, while other systems use retrieval, call-graph expansion, or repository-level exploration [19, 21, 32]. Agentic frameworks further enable LLMs to interact with repositories and tools during analysis [57], with autonomous agents mimicking expert auditing via on-demand retrieval [2, 42] and tool-constrained agents bounding reasoning along call relationships [19, 20, 26]. On binaries, LATTE [28] and VulBinLLM [21] apply LLM reasoning over decompiled code for taint-style vulnerability detection, but primarily target injection or data-flow patterns rather than the interprocedural memory object lifecycle reasoning required for memory corruption. Further, they are largely evaluated on synthetic benchmarks. 

At the same time, the capability landscape is evolving rapidly. Industrial reports indicate that frontier models can discover real vulnerabilities in production software at meaningful scale [6–8, 16, 35]. We do not view these results as evidence that semantic grounding is becoming unnecessary; rather, they reinforce that practical vulnerability discovery depends on the architecture around the model, including how context is selected, how hypotheses are prioritized, and how findings are validated. This is consistent both with academic evidence that unconstrained vulnerability reasoning remains brittle when subtle semantic distinctions must be recovered from large code contexts [14, 44, 57], and with industrial systems that explicitly incorporate prioritization, triage, and validation workflows [6, 7, 16]. Veritas instantiates this principle in the binary setting: deterministic program-analysis evidence grounds reasoning before detection, and debugger-visible artifacts confirm hypotheses afterward. The architecture is modular, allowing individual grounding mechanisms to evolve as models improve. 

## **6 Discussion** 

_Dataset Scope._ Our evaluation uses 20 vulnerability instances from 10 projects. This scale is small relative to source-code benchmarks but reflects genuine constraints of binary-level evaluation: each sample must satisfy four criteria simultaneously (Section 4.2), and fine-grained ground-truth annotation demands roughly two person-days per case, however, such annotated binary vulnerability datasets remain scarce [24, 29, 33]. 

_Hybrid Grounding and Model Evolution._ Veritas is hybrid by design: the separation between deterministic analysis and LLM-driven reasoning reflects engineering and assurance constraints, not a claim that semantic recovery must always remain external to models. As frontier models improve [7, 16, 19, 28, 35], some tasks may migrate into learned components, but three requirements persist: selecting vulnerability-relevant context, preserving memory semantics, and validating hypotheses against executable evidence. We thus view semantic grounding as the central architectural principle. 

_Generalizability and Scope._ Our evaluation focuses on out-ofbounds vulnerabilities, but the architecture is more general: the 

Veritas: A Semantically Grounded Agentic Framework for Memory Corruption Vulnerability Detection in Binaries 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

modular design allows new source models, sink models, and validation procedures for other classes such as use-after-free or doublefree. Extending beyond the current scope may require different semantic recovery and runtime oracles, and remains a promising direction. Veritas is also complementary to fuzzing: it produces hypotheses precise enough to guide targeted dynamic confirmation, whereas coverage-guided fuzzing alone detected only 2 of 20 vulnerabilities within a bounded budget. Combining candidate generation with directed fuzzing is a natural extension. 

## **7 Conclusion** 

We presented Veritas, a framework for detecting memory-corruption vulnerabilities in stripped binaries, grounded in two layers: static evidence that constrains LLM reasoning to witness-backed propagation flows from lifted LLVM IR, and runtime evidence that confirms conclusions through concrete execution artifacts. Veritas implements this through a deterministic slicer, a dual-view step-wise LLM detector, and a multi-agent runtime validator. On 20 realworld binary vulnerability cases, Veritas achieves 90% recall with few FPs, outperforming all baselines, and identifies a confirmed Apple zero-day. We believe semantically grounded context selection and executable validation will remain core requirements for reliable binary vulnerability discovery. 

## **References** 

- [1] 0xdea. 2025. semgrep-rules. https://github.com/0xdea/semgrep-rules. [Online; accessed 29-Jan-2025]. 

- [2] Talor Abramovich, Meet Udeshi, Minghao Shao, Kilian Lieret, Haoran Xi, Kimberly Milner, Sofija Jancheska, John Yang, Carlos E Jimenez, Farshad Khorrami, et al. [n. d.]. EnIGMA: Interactive Tools Substantially Assist LM Agents in Finding Security Vulnerabilities. In _Forty-second International Conference on Machine Learning_ . 

- [3] Talor Abramovich, Meet Udeshi, Minghao Shao, Kilian Lieret, Haoran Xi, Kimberly Milner, Sofija Jancheska, John Yang, Carlos E Jimenez, Farshad Khorrami, et al. 2024. Interactive Tools Substantially Assist LM Agents in Finding Security Vulnerabilities. _arXiv preprint arXiv:2409.16165_ (2024). 

- [4] AFL++ Team. 2023. AFL++: Combining Incremental Steps of Fuzzing Research. https://github.com/AFLplusplus/AFLplusplus. Accessed: 2026-01-20. 

- [5] Anthropic. [n. d.]. Claude Code Overview. https://code.claude.com/docs/en/ overview. Claude Code Docs, accessed April 6, 2026. 

- [6] Anthropic. 2026. Partnering with Mozilla to Improve Firefox’s Security. https: //www.anthropic.com/news/mozilla-firefox-security. Accessed April 2026. 

- [7] Anthropic. 2026. Project Glasswing: Securing Critical Software for the AI Era. https://www.anthropic.com/project/glasswing. Accessed April 2026. 

- [8] Anthropic Frontier Red Team. 2026. Claude Mythos Preview. https://red. anthropic.com/2026/mythos-preview/. Accessed April 2026. 

- [9] Avast Software. 2015. RetDec: A Retargetable Machine-Code Decompiler. https: //github.com/avast/retdec. [Online; accessed 29-Jan-2025]. 

- [10] Thanassis Avgerinos, Sang Kil Cha, Alexandre Rebert, Edward J Schwartz, Maverick Woo, and David Brumley. 2014. Automatic exploit generation. _Commun. ACM_ 57, 2 (2014), 74–84. 

- [11] David Brumley, Ivan Jager, Thanassis Avgerinos, and Edward J Schwartz. 2011. BAP: A binary analysis platform. In _International Conference on Computer Aided Verification_ . Springer, 463–469. 

- [12] Cristian Cadar, Daniel Dunbar, Dawson R Engler, et al. 2008. Klee: unassisted and automatic generation of high-coverage tests for complex systems programs.. In _OSDI_ , Vol. 8. 209–224. 

- [13] Junkai Chen, Zhiyuan Pan, Xing Hu, Zhenhao Li, Ge Li, and Xin Xia. 2024. Reasoning runtime behavior of a program with llm: How far are we? _arXiv preprint arXiv:2403.16437_ (2024). 

- [14] Yangruibo Ding, Yanjun Fu, Omniyyah Ibrahim, Chawin Sitawarin, Xinyun Chen, Basel Alomair, David Wagner, Baishakhi Ray, and Yizheng Chen. 2024. Vulnerability detection with code language models: How far are we? _arXiv preprint arXiv:2403.18624_ (2024). 

- [15] Dawson Engler, David Yu Chen, Seth Hallem, Andy Chou, and Benjamin Chelf. 2001. Bugs as deviant behavior: A general approach to inferring errors in systems code. _ACM SIGOPS Operating Systems Review_ 35, 5 (2001), 57–72. 

- [16] Stanislav Fort. 2026. _System Over Model: Zero-Day Discovery at the Jagged Frontier_ . https://aisle.com/blog/system-over-model-zero-day-discovery-at-thejagged-frontier AISLE blog. 

- [17] Fraunhofer FKIE. 2025. cwe_checker: Static Binary Analysis for CWE Detection. https://github.com/fkie-cad/cwe_checker. [Online; accessed 29-Jan-2025]. 

- [18] Vinod Ganapathy, Somesh Jha, David Chandler, David Melski, and David Vitek. 2003. Buffer overrun detection using linear programming and static analysis. In _Proceedings of the 10th ACM conference on Computer and communications security_ . 345–354. 

- [19] Jinyao Guo, Chengpeng Wang, Dominic Deluca, Jinjie Liu, Zhuo Zhang, and Xiangyu Zhang. 2025. BugScope: Learn to Find Bugs Like Human. _arXiv preprint arXiv:2507.15671_ (2025). 

- [20] Jinyao Guo, Chengpeng Wang, Xiangzhe Xu, Zian Su, and Xiangyu Zhang. 2025. Repoaudit: An autonomous llm-agent for repository-level code auditing. _arXiv preprint arXiv:2501.18160_ (2025). 

- [21] Nasir Hussain, Haohan Chen, Chanh Tran, Philip Huang, Zhuohao Li, Pravir Chugh, William Chen, Ashish Kundu, and Yuan Tian. 2025. VulBinLLM: LLM-powered Vulnerability Detection for Stripped Binaries. _arXiv preprint arXiv:2505.22010_ (2025). 

- [22] Yu Jiang, Jie Liang, Fuchen Ma, Yuanliang Chen, Chijin Zhou, Yuheng Shen, Zhiyong Wu, Jingzhou Fu, Mingzhe Wang, Shanshan Li, et al. 2024. When fuzzing meets llms: Challenges and opportunities. In _Companion Proceedings of the 32nd ACM International Conference on the Foundations of Software Engineering_ . 492–496. 

- [23] Keen Security Lab. 2023. BinAbsInspector. https://github.com/KeenSecurityLab/ BinAbsInspector. GitHub repository. Retrieved May 1, 2023. 

- [24] Hwiwon Lee, Ziqi Zhang, Hanxiao Lu, and Lingming Zhang. 2025. SEC-bench: Automated Benchmarking of LLM Agents on Real-World Software Security Tasks. _arXiv preprint arXiv:2506.11791_ (2025). 

- [25] Ahmed Lekssays, Hamza Mouhcine, Khang Tran, Ting Yu, and Issa Khalil. 2025. {LLMxCPG}:{Context-Aware} vulnerability detection through code property 

   - {Graph-Guided} large language models. In _34th USENIX Security Symposium (USENIX Security 25)_ . 489–507. 

- [26] Ziyang Li, Saikat Dutta, and Mayur Naik. 2024. IRIS: LLM-assisted static analysis for detecting security vulnerabilities. _arXiv preprint arXiv:2405.17238_ (2024). 

- [27] Nelson F Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. 2024. Lost in the middle: How language models use long contexts. _Transactions of the Association for Computational Linguistics_ 12 (2024), 157–173. 

- [28] Puzhuo Liu, Chengnian Sun, Yaowen Zheng, Xuan Feng, Chuan Qin, Yuncheng Wang, Zhi Li, and Limin Sun. 2023. Harnessing the power of llm to support binary taint analysis. _arXiv preprint arXiv:2310.08275_ (2023). 

- [29] Xiang Mei, Pulkit Singh Singaria, Jordi Del Castillo, Haoran Xi, Tiffany Bao, Ruoyu Wang, Yan Shoshitaishvili, Adam Doupé, Hammond Pearce, Brendan Dolan-Gavitt, et al. 2024. Arvo: Atlas of reproducible vulnerabilities for open source software. _arXiv preprint arXiv:2408.02153_ (2024). 

- [30] Meta. 2025. Infer Static Analyzer. https://fbinfer.com/. [Online; accessed 29-Jan-2025]. 

- [31] National Security Agency. 2019. Ghidra Software Reverse Engineering Framework. https://ghidra-sre.org/. [Online; accessed 29-Jan-2025]. 

- [32] Yuzhou Nie, Hongwei Li, Chengquan Guo, Ruizhe Jiang, Zhun Wang, Bo Li, Dawn Song, and Wenbo Guo. 2025. VulnLLM-R: Specialized Reasoning LLM with Agent Scaffold for Vulnerability Detection. _arXiv preprint arXiv:2512.07533_ (2025). 

- [33] NSA Center for Assured Software. 2017. _Juliet C/C++ 1.3_ . https://samate.nist. gov/SARD/test-suites/112 

- [34] OpenAI. [n. d.]. Codex. https://openai.com/codex/. OpenAI Developers, accessed April 6, 2026. 

- [35] OpenAI. 2026. Introducing GPT-5.4. https://openai.com/index/introducing-gpt5-4/. Accessed: 2026-04-25. 

- [36] Chengbin Pang, Ruotong Yu, Yaohui Chen, Eric Koskinen, Georgios Portokalidis, Bing Mao, and Jun Xu. 2021. Sok: All you ever wanted to know about x86/x64 binary disassembly but were afraid to ask. In _2021 IEEE symposium on security and privacy (SP)_ . IEEE, 833–851. 

- [37] radareorg. 2025. radare2: Reverse Engineering Framework. https://github.com/ radareorg/radare2. [Online; accessed 29-Jan-2025]. 

- [38] Nilo Redini, Aravind Machiry, Ruoyu Wang, Chad Spensky, Andrea Continella, Yan Shoshitaishvili, Christopher Kruegel, and Giovanni Vigna. 2020. Karonte: Detecting insecure multi-binary interactions in embedded firmware. In _2020 IEEE Symposium on Security and Privacy (SP)_ . IEEE, 1544–1561. 

- [39] Semgrep. 2025. Semgrep: Lightweight Static Analysis for Many Languages. https://github.com/semgrep/semgrep. [Online; accessed 29-Jan-2025]. 

- [40] Konstantin Serebryany, Derek Bruening, Alexander Potapenko, and Dmitriy Vyukov. 2012. {AddressSanitizer}: A fast address sanity checker. In _2012 USENIX annual technical conference (USENIX ATC 12)_ . 309–318. 

- [41] Xiuwei Shang, Guoqiang Chen, Shaoyin Cheng, Benlong Wu, Li Hu, Gangyang Li, Weiming Zhang, and Nenghai Yu. 2025. BinMetric: A Comprehensive Binary Analysis Benchmark for Large Language Models. _arXiv preprint arXiv:2505.07360_ 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Xinran Zheng, Alfredo Pesoli, Marco Valleri, Suman Jana, and Lorenzo Cavallaro 

(2025). 

- [42] Minghao Shao, Haoran Xi, Nanda Rani, Meet Udeshi, Venkata Sai Charan Putrevu, Kimberly Milner, Brendan Dolan-Gavitt, Sandeep Kumar Shukla, Prashanth Krishnamurthy, Farshad Khorrami, et al. 2025. CRAKEN: Cybersecurity LLM Agent with Knowledge-Based Execution. _arXiv preprint arXiv:2505.17107_ (2025). 

- [43] Ze Sheng, Zhicheng Chen, Shuning Gu, Heqing Huang, Guofei Gu, and Jeff Huang. 2025. Llms in software security: A survey of vulnerability detection techniques and insights. _Comput. Surveys_ 58, 5 (2025), 1–35. 

- [44] Benjamin Steenhoek, Md Mahbubur Rahman, Monoshi Kumar Roy, Mirza Sanjida Alam, Hengbo Tong, Swarna Das, Earl T Barr, and Wei Le. 2024. To err is machine: Vulnerability detection challenges llm reasoning. _arXiv preprint arXiv:2403.17218_ (2024). 

- [45] Saad Ullah, Mingji Han, Saurabh Pujar, Hammond Pearce, Ayse Coskun, and Gianluca Stringhini. 2024. Llms cannot reliably identify and reason about security vulnerabilities (yet?): A comprehensive evaluation, framework, and benchmarks. In _2024 IEEE symposium on security and privacy (SP)_ . IEEE, 862–880. 

- [46] Jayakrishna Vadayath, Moritz Eckert, Kyle Zeng, Nicolaas Weideman, Gokulkrishna Praveen Menon, Yanick Fratantonio, Davide Balzarotti, Adam Doupé, Tiffany Bao, Ruoyu Wang, et al. 2022. Arbiter: Bridging the static and dynamic divide in vulnerability discovery on binary programs. In _31st USENIX Security Symposium (USENIX Security 22)_ . 413–430. 

- [47] Valgrind Developers. 2002. Valgrind: An Instrumentation Framework for Building Dynamic Analysis Tools. https://valgrind.org/. [Online; accessed 29-Jan-2025]. 

- [48] David A Wagner, Jeffrey S Foster, Eric A Brewer, and Alexander Aiken. 2000. A first step towards automated detection of buffer overrun vulnerabilities.. In _NDSS_ , Vol. 20. 0. 

- [49] Fish Wang and Yan Shoshitaishvili. 2017. Angr-the next generation of binary analysis. In _2017 IEEE Cybersecurity Development (SecDev)_ . IEEE, 8–9. 

- [50] Felix Weissberg, Lukas Pirch, Erik Imgrund, Jonas Möller, Thorsten Eisenhofer, and Konrad Rieck. 2025. LLM-based Vulnerability Discovery through the Lens of Code Metrics. _arXiv preprint arXiv:2509.19117_ (2025). 

- [51] Xin-Cheng Wen, Yijun Yang, Cuiyun Gao, Yang Xiao, and Deheng Ye. 2025. Boosting Vulnerability Detection of LLMs via Curriculum Preference Optimization with Synthetic Reasoning Data. _arXiv preprint arXiv:2506.07390_ (2025). 

- [52] Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shaokun Zhang, Jiale Liu, et al. 2024. Autogen: Enabling next-gen LLM applications via multi-agent conversations. In _First Conference on Language Modeling_ . 

- [53] Jun Xu, Dongliang Mu, Ping Chen, Xinyu Xing, Pei Wang, and Peng Liu. 2016. Credal: Towards locating a memory corruption vulnerability with your core dump. In _Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security_ . 529–540. 

- [54] Jun Xu, Peng Ning, Chongkyung Kil, Yan Zhai, and Chris Bookholt. 2005. Automatic diagnosis and response to memory corruption vulnerabilities. In _Proceedings of the 12th ACM conference on Computer and communications security_ . 223–234. 

- [55] Hua Yan, Yulei Sui, Shiping Chen, and Jingling Xue. 2018. Spatio-temporal context reduction: A pointer-analysis-based static approach for detecting use-after-free vulnerabilities. In _Proceedings of the 40th International Conference on Software Engineering_ . 327–337. 

- [56] Dayu Yang, Tianyang Liu, Daoan Zhang, Antoine Simoulin, Xiaoyi Liu, Yuwei Cao, Zhaopu Teng, Xin Qian, Grey Yang, Jiebo Luo, et al. 2025. Code to think, think to code: A survey on code-enhanced reasoning and reasoning-driven code intelligence in llms. _arXiv preprint arXiv:2502.19411_ (2025). 

- [57] Alperen Yildiz, Sin G Teo, Yiling Lou, Yebo Feng, Chong Wang, and Dinil Mon Divakaran. 2025. Benchmarking llms and llm-based agents in practical vulnerability detection for code repositories. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . 30848–30865. 

- [58] Hang Zhang, Jangha Kim, Chuhong Yuan, Zhiyun Qian, and Taesoo Kim. 2025. Statically discover cross-entry use-after-free vulnerabilities in the linux kernel. In _Network and Distributed System Security (NDSS) Symposium_ . 

## **Ethical Considerations** 

This work involves automated detection and validation of memory corruption vulnerabilities in binaries. Our benchmark uses exclusively previously-disclosed vulnerabilities with public CVE identifiers, and all experiments were conducted in isolated Docker environments. During real-world application, we discovered a zeroday vulnerability in Apple’s USD library and followed responsible disclosure: the vulnerability was reported to Apple through its official channel before any public disclosure, and was confirmed and assigned CVE-2025-[REDACTED]. We omit the full identifier in the submitted version to preserve double-blind review and will restore 

it in a de-anonymized version if the paper is accepted. While automated vulnerability detection tools carry inherent dual-use risks, Veritas is designed to assist defensive security analysis, targets wellstudied vulnerability classes, and does not generate weaponized exploits. This research does not involve human subjects or user data. 

## **Open Science** 

To support transparent evaluation of our core claims, we provide an anonymous artifact bundle for double-blind review at the following URL: 

• https://anonymous.4open.science/r/Veritas-2B46 

No credentials are required. The bundle contains the artifacts that underlie the benchmark construction, the static-to-LLM interface, and the detector prompts used in our experiments. Specifically, it includes: (1) the fine-grained ground-truth JSON annotations for the repository-level benchmark cases used in Section 4, including project and commit metadata together with the annotated vulnerability source, sink, triggering flow, and root-cause information; (2) the JSON outputs of slicer for the evaluated projects, corresponding to the witness-backed candidate flows produced from the stripped binaries and consumed by discovery; and (3) the prompt templates used by discovery, including the initial/source, intermediate, and final/sink prompts. These artifacts allow reviewers to inspect the benchmark structure, the form of the flow objects passed from the static-analysis stage to the detector, and the prompt interface used for step-wise reasoning. 

We cannot release the source code of defuse and the validator at submission time. These components are intellectual property of the industrial collaborator involved in this work and are currently undergoing internal clearance for a planned open-source release. Releasing them during review would violate existing intellectual property constraints. Accordingly, the artifact bundle does not support complete end-to-end re-execution of the full pipeline from binaries to validated findings. To partially mitigate this limitation, we release the derived analysis outputs and prompt artifacts that expose the benchmark annotations, the slicer outputs used by the detector, and the prompt-level interface underlying the reported methodology. 

Full reproduction of the reported runs also depends on thirdparty tools and commercial model APIs described in Section 4.1, including RetDec, radare2, Valgrind, and the LLM services used by the detector, validator, and agentic baselines. We do not redistribute these third-party components or model weights, and their use remains subject to the respective licenses and service terms. No private user data, human-subject data, or undisclosed benchmark vulnerabilities are included in the shared artifacts. 

## **A Appendix** 

## **A.1 Prompt Design** 

Prompting in Veritas is tailored to each stage rather than handled by a single template. The _Detector_ uses structured templates for each function and flow history to maintain taint, bounds, and control flow context along each candidate flow. The _Validator_ uses role-specific instructions and constrained tool interfaces to keep 

Veritas: A Semantically Grounded Agentic Framework for Memory Corruption Vulnerability Detection in Binaries Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

planning, execution, and failure diagnosis auditable. Thus, prompting reflects the distinct roles of the two LLM-facing components: semantic interpretation over precomputed flows and executable validation of concrete hypotheses. 

## **A.2 Algorithm of** **_Detector_** 

Algorithm 1 summarizes the Dual-view Vulnerability Detector. Given a flow object _𝜋_ = (( _𝑓_ 1 _, ℓ_ 1) _, . . . ,_ ( _𝑓𝑁 , ℓ𝑁_ )) with per-function grounded labels, anchor cues A( _𝑓𝑛_ ), decompiled code _𝐷_ ( _𝑓𝑛_ ), lifted IR _𝐼_ ( _𝑓𝑛_ ), and a prefix cache C, the _Detector_ first retrieves the longest cached prefix (Line 1). If no prefix is cached, the reasoning state is initialized as empty (Line 2). It then processes the remaining functions in flow order (Lines 3-11). Source and sink functions use a dual-view representation combining lifted IR and decompiled code (Line 5), while intermediate functions use only decompiled code (Line 7). At each step, the LLM Φ _𝜃_ updates the accumulated reasoning state _𝑆𝑛_ from the previous state, the current function representation, and its anchor cues (Line 9); the resulting state is stored in the prefix cache for later reuse by flows with the same prefix (Line 10). After all functions are processed, the _Detector_ performs path-sensitive verification over the complete flow using the final reasoning state _𝑆𝑁_ (Line 12), and deduplicates violations corresponding to the same memory-safety issue (Line 13). The flow is reported as vulnerable if any violation remains (Line 14), and benign otherwise (Line 15). The final output is the decision _𝑧𝜋_ ∈{0 _,_ 1} with a structured explanation derived from the violation set V _𝜋_ and the accumulated reasoning state _𝑆𝑁_ (Line 16). 

**Table 8: Cost (Time (s) and Finance ($)) of Agentic Baselines** 

|Method|RepoAu<br>Time|dit [20]<br>Finance|Claude<br>Time|Code [5]<br>Finance|Codex<br>Time|[34]<br>Finance|
|---|---|---|---|---|---|---|
|Avg.|7,957.50|11.36|2,846.85|20.64|5,846.23|27.62|



managed their own exploration and stopping criteria within this budget. RepoAudit was run on the specific files involved in each vulnerability trace, so its reported cost represents a lower bound on the resources needed to reach a detection. Although all three baselines complete faster and at lower cost than Veritas, this comparison is not direct: these methods operate on source code with access to type information, symbol names, structure definitions, and high-level control flow, whereas Veritas operates on stripped binaries where all such semantic structure must be reconstructed from lifted IR and decompiled code. As discussed in Section 4.5, the dominant cost in Veritas is runtime validation, which requires PoC construction, debugger instrumentation, and memory inspection against low-level binary artifacts, a cost that source-level methods largely avoid because richer program representations reduce the need for executable confirmation. 

|**Algorithm 1:**Dual-view Vulnerability Detector|
|---|



||**Input:**Flow object_𝜋_= ((_𝑓_1_, ℓ_1)_, ...,_(_𝑓𝑁, ℓ𝑁_)) with grounded<br>labels (_ℓ_1_, . . . , ℓ𝑁_); anchors A(_𝑓𝑛_); decompiled code<br>_𝐷_(_𝑓𝑛_); lifted IR_𝐼_(_𝑓𝑛_); prefx cache C|
|---|---|
||**Output:**Decision_𝑧𝜋_∈{0_,_1} and explanation<br><sup>∗</sup>|
|**1**|(_𝜋_<sup>(</sup><sup>_𝑛_)</sup>_,𝑆𝑛_∗) ←LongestCachedPrefix(_𝜋,_C);|
|**2 **|**if**_𝑛_<sup>∗</sup>=0**then**_𝑆_0 ←∅;|
|**3 **|**for**_𝑛_←_𝑛_<sup>∗</sup>+1**to**_𝑁_**do**|
|**4**|**if** _𝑓𝑛_∈F_𝑠𝑟𝑐_∪F_𝑠𝑖𝑛𝑘_**then**|
|**5**|R(_𝑓𝑛_) ←⟨_𝐼_(_𝑓𝑛_)_, 𝐷_(_𝑓𝑛_)⟩;|
|**6**|**else**<br>|
|**7**<br>**8**|R(_𝑓𝑛_) ←_𝐷_(_𝑓𝑛_);<br>**end**|
|**9**|_𝑆𝑛_←Φ_𝜃_(_𝑆𝑛_−1_,_R(_𝑓𝑛_)_,_A(_𝑓𝑛_));<br>|
|**10**|C[_𝜋_<sup>(</sup><sup>_𝑛_) </sup>] ←_𝑆𝑛_;|
|**11 **|**end**|
|**12**|V_𝜋_←PathSensitiveVerify(_𝜋,𝑆𝑁,_R(_𝑓𝑁_)_,_A(_𝑓𝑁_));|
|**13**|V_𝜋_←DeduplicateViolations(V_𝜋_);|
|**14 **|**if** V_𝜋_≠∅**then**_𝑧𝜋_←1;|
|**15 **|**else**_𝑧𝜋_←0;|
|**16 **|**return** (_𝑧𝜋,_GenerateExplanation(V_𝜋,𝑆𝑁_));|



## **A.3 Cost on Baselines** 

Table 8 reports the average per-sample time and financial cost of the three agentic baselines. Codex and Claude Code were each given a two-hour audit budget per sample with full repository access, build permissions, and execution capabilities; both agents 

