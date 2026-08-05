# PrediQL: Automated Testing of GraphQL APIs with LLMs

**Shaolun Liu¹\*, Sina Marefat²\*, Omar Tsai¹, Yu Chen¹, Zecheng Deng¹, Jia Wang¹, Mohammad A. Tayebi¹**

¹ Simon Fraser University, Canada
² K. N. Toosi University of Technology, Iran

`shaolun.liu@sfu.ca` · `sina.marefat@email.kntu.ac.ir` · `omar@ztasecurity.com` · `yca518@sfu.ca` · `zda35@sfu.ca` · `jwa454@sfu.ca` · `tayebi@sfu.ca`

*\* Equal contribution.*

Source code: [github.com/SLL288/prediql](https://github.com/SLL288/prediql)

---

## Abstract

GraphQL's flexible query model and nested data dependencies expose APIs to complex, context-dependent vulnerabilities that are difficult to uncover using conventional testing tools. Existing fuzzers either rely on random payload generation or rigid mutation heuristics, failing to adapt to the dynamic structures of GraphQL schemas and responses. We present **PrediQL**, the first retrieval-augmented, LLM-guided fuzzer for GraphQL APIs. PrediQL combines large language model reasoning with adaptive feedback loops to generate semantically valid and diverse queries. It models the choice of fuzzing strategy as a multi-armed bandit problem, balancing exploration of new query structures with exploitation of past successes. To enhance efficiency, PrediQL retrieves and reuses execution traces, schema fragments, and prior errors, enabling self-correction and progressive learning across test iterations. Beyond input generation, PrediQL integrates a context-aware vulnerability detector that uses LLM reasoning to analyze responses, interpreting data values, error messages, and status codes to identify issues such as injection flaws, access-control bypasses, and information disclosure.

Our evaluation across open-source and benchmark GraphQL APIs shows that PrediQL achieves significantly higher coverage and vulnerability discovery rates compared to state-of-the-art baselines. These results demonstrate that combining retrieval-augmented reasoning with adaptive fuzzing can transform API security testing from reactive enumeration to intelligent exploration.

**Keywords:** GraphQL Security, API Fuzzing, Large Language Models, Retrieval-Augmented Generation, Multi-Armed Bandit Learning

---

## 1. Introduction

Modern software systems are often built from many independent microservices that communicate through well-defined APIs. Among contemporary API styles, GraphQL has gained significant adoption because it allows clients to request precisely the data they need through a single flexible endpoint. This design improves efficiency and mitigates the problem of over-fetching, common in REST or gRPC APIs [8, 16].

According to a 2024 industry survey, approximately 61% of respondents reported using GraphQL in production, and about 10% indicated that they were replacing REST with GraphQL in their systems [34, 49]. However, this widespread adoption has also exposed security weaknesses in many deployments. A recent study reported that roughly 69% of scanned public GraphQL API services suffered from unrestricted resource consumption vulnerabilities, making them susceptible to denial-of-service (DoS) attacks via deep-nested or costly queries [25, 27, 35]. These issues highlight that GraphQL introduces unique security challenges, such as unbounded query depth, schema exposure, injection in nested arguments, and inconsistent access control across linked queries and mutations [7]. Consequently, effective testing of GraphQL APIs requires more than traditional input fuzzing; it must incorporate a contextual understanding of schema relationships and multistep interactions.

Existing testing tools fall into two main groups: black-box fuzzers and schema-aware fuzzers.

- **Black-box fuzzers** explore input space randomly, but do not respect GraphQL structure.
- **Schema-aware tools**, such as EvoMaster [17–19], improve test coverage by using the schema, but rely on simple template mutations and ignore cross-field or cross-operation dependencies.

Recent systems such as GraphQLer [50] take an important step by analyzing producer–consumer relationships between queries and mutations, discovering vulnerabilities missed by older tools. However, even these approaches remain static; their generation logic does not adapt to execution feedback or changing context. In short, current GraphQL fuzzers cannot yet reason adaptively about API behavior.

Recent advances in large language models (LLMs) offer a new direction for building intelligent, feedback-driven fuzzers. LLMs can reason about structured input formats, infer valid parameters from schema fragments, and generate meaningful queries [43, 46]. When combined with retrieval mechanisms that use past traces, schema segments, or error logs [37, 41, 48], the fuzzer can refine future inputs based on what it has already learned. Recent LLM-assisted fuzzing solutions [22, 33, 36, 45, 51, 52] show that generative reasoning improves coverage in binary and protocol fuzzing. Yet, no prior research has applied LLM-based fuzzing to GraphQL, whose nested queries and dependency-rich structure require contextual reasoning and adaptive feedback. Work such as WENDIGO [44] targets denial-of-service discovery in GraphQL using deep reinforcement learning, and Perera et al. [47] explore detecting malicious GraphQL queries with LLMs and neural classifiers, but neither focuses on adaptive fuzzing.

To close this gap, we present **PrediQL**, an automated GraphQL testing framework that joins schema introspection, retrieval-augmented LLM prompting [41], multi-armed bandit learning [15, 20, 40], and self-correction into a single feedback loop. PrediQL treats the LLM as a guided component rather than an oracle. It first extracts schema information through introspection and then retrieves relevant examples and past errors to generate the query in real feedback. A bandit-based selector dynamically chooses between different prompting strategies, balancing exploration and exploitation. This design allows PrediQL to generate valid, diverse, and context-sensitive queries that explore deeper parts of the schema and reveal complex vulnerabilities.

We evaluated PrediQL using multiple large language models across a diverse set of open-source and benchmark GraphQL APIs. The results show that PrediQL consistently improves test coverage, by an average of 16% with a maximum improvement of 50%, and discovers more context-dependent vulnerabilities compared to established baselines. Among the tested configurations, GPT-5 Mini achieved the highest coverage, while smaller models like Llama-3-8B offered competitive results with reduced computational cost. In addition to broader coverage, PrediQL demonstrates stronger vulnerability detection capabilities, accurately identifying injection flaws, access-control bypasses, and information-disclosure cases that existing tools often miss.

In summary, this paper makes three main contributions:

1. We present PrediQL, the first retrieval-augmented, LLM-guided GraphQL fuzzer with adaptive strategy selection, modeled as a multi-armed bandit problem [15, 20, 40] to improve efficiency and reduce redundant requests.
2. We design a context-aware vulnerability detector that leverages LLM reasoning to interpret responses and identify diverse vulnerability categories beyond static rule-based detection.
3. We conduct extensive experimental evaluation on open-source and benchmark GraphQL APIs, demonstrating that PrediQL achieves higher coverage and detects more context-dependent vulnerabilities than existing tools.

---

## 2. Background & Related Work

Modern web applications increasingly adopt GraphQL for its flexible and efficient data-fetching model. While this paradigm simplifies client–server interaction, it also introduces a new class of security challenges that differ from those found in traditional REST APIs. In this section, we first review the fundamentals of GraphQL, then summarize its known vulnerability classes, and finally discuss prior work on API testing, GraphQL security analysis, LLM-assisted fuzzing, prompt engineering, and adaptive test-strategy selection.

### 2.1 GraphQL Fundamentals

GraphQL provides a structured and flexible alternative to traditional REST APIs, offering three key features [7, 8, 16]:

- **Data as a graph** — GraphQL organizes data as a graph of interconnected objects, allowing clients to retrieve all required information in a single request and mitigating both under-fetching and over-fetching.
- **Strong typing** — Each GraphQL API exposes a schema that defines data types (objects) and operations (queries and mutations). This strong type system ensures predictable responses, simplifies error handling, and requires clients to explicitly specify which fields to return.
- **Single endpoint** — All requests are processed through a unified endpoint, providing a consistent interface for both data retrieval and modification.

A GraphQL schema defines two primary categories of data types: **scalars** and **objects**. Scalars represent atomic values such as `Int`, `Float`, `String`, `Boolean`, and `ID`. Objects are user-defined entities composed of multiple fields, which may themselves be scalars, objects, or lists of other types. This nested composition creates a rich graph structure that captures relationships among entities and allows clients to traverse and query linked data seamlessly.

Clients interact with GraphQL APIs through two main operation types:

- **Queries** retrieve data from the server, functioning similarly to HTTP GET requests in REST APIs. A special form, the *introspection query*, allows clients to inspect the schema and obtain metadata about available types and operations.
- **Mutations** modify data on the server, corresponding to creation, update, or deletion actions.

Both queries and mutations enable fine-grained field selection, ensuring clients request exactly the data they need. Each field may also take arguments, allowing deeply nested and parameterized requests. A GraphQL operation is first parsed and validated against the schema, then executed by resolving each field independently. This layered execution model, together with features like schema introspection, makes GraphQL powerful but also complex to test securely.

### 2.2 GraphQL Vulnerabilities

GraphQL provides powerful ways to query and manage data, but its flexibility also brings new types of security risks. Some of these problems resemble common web-application issues, such as broken access control, injection flaws, and misconfigurations, while others are specific to how GraphQL is designed. These GraphQL-specific issues expand the attack surface and need special attention. They are grouped into three main categories:

- **Query Abuse Vulnerabilities.** Because GraphQL allows users to send highly flexible queries, attackers can exploit this feature to overload or explore the system. A common example is misuse of the introspection query, which reveals the entire schema, including all types, fields, and relationships — information that helps attackers craft more targeted and harmful queries. GraphQL is also exposed to Denial-of-Service (DoS) attacks caused by deeply nested or repetitive queries that consume large amounts of server resources, leading to slowdowns or outages.
- **Injection Vulnerabilities.** GraphQL inputs can be an entry point for injection attacks if they are not properly checked or sanitized. The most serious case is SQL Injection, where unsafe user inputs are added to database queries, allowing data theft or manipulation. Other examples include Path Injection and Cross-Site Scripting (XSS), which can result in stolen sessions, leaked data, or malicious code running in the browser. Weak input handling in GraphQL therefore puts both the backend and users at risk.
- **Access Control Vulnerabilities.** Access-control problems occur when a GraphQL API fails to properly restrict what data users can access. A typical example is Insecure Direct Object Reference (IDOR), where attackers change object identifiers to view or modify restricted data. Another example is batched attacks, where multiple operations are combined in one request to bypass individual security checks. Fixing such issues is difficult because GraphQL schemas often include many linked fields and relationships.

Testing for these problems requires context-aware and dependency-based approaches that can understand how queries, mutations, and objects interact, helping to uncover access-control flaws that traditional testing might miss.

### 2.3 Related Work

**GraphQL Security Testing.** Security testing for GraphQL has evolved from basic black-box approaches to more sophisticated schema-aware methods. Early community tools such as GraphQL-Cop [26], GraphCrawler [31], CrackQL [24], and Schemathesis [32] rely on introspection to generate single-request mutations but lack systematic reasoning about dependencies between queries and mutations. EvoMaster extends evolutionary and random testing to GraphQL APIs, supporting both black-box and white-box modes to broaden coverage [17, 18]. Industry-standard scanners such as OWASP ZAP [14] and BurpSuite [1] include GraphQL modules (e.g., Burp's Auto GQL Scanner) but primarily perform generic payload fuzzing and introspection-based attacks rather than exploring multistep workflows. GraphQLer [50] introduced the first context-aware GraphQL security testing framework: it analyzes the schema to infer producer–consumer dependencies among queries and mutations, constructs a dependency graph, and generates realistic chained payloads. This approach improves schema coverage and discovers previously unknown vulnerabilities compared with earlier fuzzers, motivating the need for dependency reasoning in GraphQL security testing.

**LLM-Assisted Fuzzing.** In dynamic analysis, fuzzing remains one of the most effective ways to automatically find software bugs. Coverage-guided fuzzers such as AFL++ [28] and libFuzzer [42], along with large-scale efforts like OSS-Fuzz [30], have discovered thousands of vulnerabilities. However, these approaches often struggle with highly structured or constrained inputs and with reaching deep execution paths. To address these challenges, recent work combines LLMs with fuzzing and related dynamic techniques. Fuzz4All [51] uses LLMs for input generation and mutation across multiple formats, maintaining diversity through an autoprompting loop and achieving higher coverage than traditional fuzzers. EL-Fuzz [21] enhances generation-based fuzzers through LLM-driven synthesis over input spaces, achieving higher coverage and revealing real-world bugs.

Recent studies have also explored machine-learning-based detection of malicious GraphQL queries. One line of work applies deep reinforcement learning to identify denial-of-service patterns in GraphQL APIs [44], while another investigates the use of large language models, sentence transformers, and convolutional neural networks for malicious query detection [47]. There has also been work using LLMs for text-to-GraphQL queries [39]; however, that model does not target specific API schemas. To the best of our knowledge, no prior work has applied LLM-assisted fuzzing to GraphQL, whose schema-rich, multi-operation design introduces unique challenges. PrediQL is the first to address this gap by leveraging LLM reasoning to guide test generation and vulnerability detection in GraphQL APIs.

---

## 3. Methodology

PrediQL is a modular LLM-driven GraphQL fuzzing framework organized around a closed-loop pipeline (Figure 1). At its core, PrediQL integrates an LLM-based query generator with schema introspection, semantic retrieval, adaptive arm selection, and self-correction modules. This architecture constrains the model's generation space, maintaining validity and fuzzing relevance while adapting to feedback dynamically. The key contribution lies in coupling schema-aware reasoning with adaptive prompting to produce valid, diverse, and feedback-driven queries.

Rather than relying on static mutation operators, PrediQL refines prompts with schema fragments, retrieved traces, and error signals, making each generation guided by prior results and schema insights. The system runs as a closed-loop cycle: schema modeling constrains the search space, the bandit-based selector chooses a prompting strategy, retrieval grounds prompts in real execution history, and self-correction incorporates prior errors. Prompt construction then assembles these elements into an evidence-gated LLM input; executed queries update the schema, memory, and bandit posteriors, completing the loop and allowing iterative refinement of validity, diversity, and coverage.

### Figure 1 — Workflow of PrediQL

The workflow is organized into three connected stages that run inside a closed loop, replicated across *N* parallel nodes, all backed by a shared index/store:

```mermaid
flowchart LR
    subgraph S1["Schema Retrieval & Modeling"]
        A["Introspection Query"] --> B["GraphQL API"]
        B --> C["Extracted Schema"]
    end

    subgraph S2["Memory Unit"]
        D["Object Schemas"]
        E["Retrieved Values"]
        F["Query / Response Pairs"]
    end

    subgraph S3["Adaptive Query Generation"]
        G["Multi-Arm Selection"] --> H["Prompt Enrichment"]
        H --> I["LLM"]
        I --> J["Send Payload"]
        J --> K["GraphQL API "]
        K --> L["Response"]
        L --> M["Self Correction"]
        L --> N["Log Failures"]
        L --> O["Vulnerability Detection"]
        M --> H
    end

    C --> S2
    S2 --> H
    O --> P[("Store in Index / Bandit Posterior / Schema")]
    N --> P
    P --> S2

    style S1 fill:#f8d7da,stroke:#c0392b
    style S2 fill:#d4edda,stroke:#27ae60
    style S3 fill:#fff3cd,stroke:#d4ac0d
```

**Figure 1: Workflow of PrediQL.** Schema retrieval and modeling extracts the API schema through introspection; the memory unit stores object schemas, retrieved values, and query/response pairs; adaptive query generation uses multi-arm selection and prompt enrichment to drive the LLM, send payloads to the GraphQL API, and analyze responses through self-correction, failure logging, and vulnerability detection. Results feed back into a shared index that updates the bandit posterior and schema knowledge, closing the loop across *N* parallel nodes.

### 3.1 Schema Modeling

The PrediQL pipeline begins with a standard GraphQL introspection query against the target API. Introspection reveals the complete schema, which includes queries, mutations, input parameters, and return types. PrediQL parses this output into a structured intermediate representation that organizes operations, argument specifications, and object definitions. To facilitate reuse and downstream automation, the schema is serialized into lightweight YAML files, separating queries, mutations, and type definitions. This schema map provides a blueprint of the API before any fuzzing or query generation takes place.

Unlike prior tools that treat introspection results as flat listings, PrediQL recursively follows links between objects to capture nested and cross-referenced types. This yields a graph-structured view of responses, enabling the system to reason about both top-level operations and the shape of deeply nested return values. Maintaining this normalized schema representation allows PrediQL to generate queries that are syntactically valid, semantically consistent, and structurally diverse, while avoiding common issues such as type mismatches or missing arguments.

The introspection query used follows the standard GraphQL introspection format:

```graphql
{
  __schema {
    queryType { name }
    mutationType { name }
    subscriptionType { name }
    types {
      ...FullType
    }
    directives {
      name
      description
      locations
      args {
        ...InputValue
      }
    }
  }
}
```

### 3.2 Adaptive Query Generation

**Adaptive Arm Selection.** Query generation is framed as a multi-armed bandit problem [40], where each arm represents a distinct prompting strategy defined by four key parameters:

- **Schema** — determines whether the full GraphQL schema is included in the LLM prompt to guide query construction.
- **Arg Mode** — controls how arguments are generated: `known` reuses previously successful parameter values from the RAG context, `real` synthesizes realistic type-appropriate literals, and `nulls` tests optional fields with null values.
- **Depth** — limits the nesting level of GraphQL selections to balance complexity and validity.
- **Top-k** — specifies how many similar examples from the RAG system are retrieved as contextual grounding (see Section 4.1 for configuration details).

Since the effectiveness of each strategy depends on the endpoint's evolving behavior, the bandit formulation enables PrediQL to dynamically allocate preference toward high-performing arms while still exploring alternatives. To balance exploration and exploitation, PrediQL employs Thompson Sampling [15], rewarding arms only when generated queries both *(i)* return HTTP 200 responses and *(ii)* expand coverage. To account for non-stationary environments, rewards are exponentially discounted so that outdated strategies are gradually down-weighted. This adaptive mechanism prevents over-commitment to a single strategy while progressively amplifying those that yield meaningful coverage.

**Retrieval-Augmented Generation.** To mitigate the problem of hallucinated or invalid query values, PrediQL integrates retrieval-augmented generation (RAG) [41]. All prior queries and responses are embedded into a FAISS index [23]. During generation, PrediQL retrieves the top-*k* (where *k* is equal to 0, 3, or 5, depending on the selected arm) most semantically relevant traces and injects them into the prompt.

This retrieval memory grounds the LLM in real execution history, improving syntactic fidelity, reducing repetition, and promoting diversity by surfacing alternative query structures.

**Prompt Engineering.** Prompt design is key to guiding query generation. PrediQL adopts four design goals: prompts must be evidence-gated, deterministic, schema-constrained, and context-aware. At runtime, prompt $P$ is automatically assembled from five modular components:

$$
P = \left[ B \parallel S \parallel R \parallel E \parallel D \right]
$$

where:

- $B$ — Basic restricting header (evidence-gating)
- $S$ — Schema fragments from introspection
- $R$ — Retrieved execution examples (RAG)
- $E$ — Prior error–query pairs (self-correction)
- $D$ — Strategy-specific directives (bandit arm)

This modular structure, illustrated in Figure 2, ensures that exploration happens primarily through $D$ (arm choice), while $S$, $R$, and $E$ stabilize performance across strategies.

#### Figure 2 — Structure of the curated prompt and enrichment sections

```mermaid
flowchart LR
    subgraph Template["Prompt Template"]
        direction TB
        H1["Header Block"]
        H2["Schema Block"]
        H3["Context Block"]
        H4["Format Block"]
    end

    subgraph Descriptions["Block Descriptions"]
        direction TB
        D1["Domain knowledge about GraphQL query generation based on targeted vulnerabilities and restricted reasoning"]
        D2["Include introspection query result based on selected ARM for the specific node"]
        D3["Include real values from previous responses (RAG) and previous query/error pairs"]
        D4["Response template description for bulk query generation with vulnerability label"]
    end

    H1 -.-> D1
    H2 -.-> D2
    H3 -.-> D3
    H4 -.-> D4

    style H1 fill:#d4edda,stroke:#27ae60
    style H2 fill:#cce5ff,stroke:#2e75b6
    style H3 fill:#e2d4f0,stroke:#8e44ad
    style H4 fill:#fde3cf,stroke:#d35400
```

**Figure 2: Structure of curated prompt and enrichment sections.** The prompt template is composed of four blocks — Header, Schema, Context, and Format — each contributing a distinct kind of information: domain knowledge and restricted reasoning guidance, introspection results for the selected arm, retrieved real values and prior error/query pairs, and the expected bulk-response format with vulnerability labeling.

### 3.3 Execution and Feedback

**Self-Correction.** Failed queries are not discarded. Instead, PrediQL explicitly records schema errors and associates them with the queries that caused them. In subsequent generations, these error–query pairs are injected into the prompt as corrective signals. This error-guided refinement turns schema violations into supervision, steering the model away from repeated mistakes and accelerating convergence toward valid, schema-compliant queries.

**Context-Aware Vulnerability Detection.** To assess security impact, PrediQL uses an LLM to analyze responses in context, rather than relying on predefined signatures or static rules. Each response, together with its execution metadata such as status codes and error messages, is transformed into a structured analysis prompt that directs the LLM to identify evidence of vulnerabilities, including injection flaws, access-control bypasses, and information disclosure. The resulting analyses are parsed into JSON records encoding vulnerability type, severity, confidence, and evidence. These records are stored and aggregated, yielding both granular findings and system-level trends. By conditioning on schema knowledge and execution context, PrediQL generalizes across diverse GraphQL APIs and uncovers subtle, context-dependent flaws that rule-based detectors overlook.

### 3.4 Closed-Loop Integration

Together, these phases form a closed-loop fuzzing cycle in which schema knowledge constrains the LLM, adaptive generation explores diverse query strategies, and execution feedback continuously refines both prompts and strategy selection. This iterative design enables PrediQL to expand coverage systematically while maintaining robustness and precision in vulnerability discovery.

---

## 4. Evaluation

We implement the design and experiments in an open-source repository.[^repo] Our experiment is structured to investigate the following research questions:

- **RQ1.** How can LLMs be guided to synthesize valid yet adversarial GraphQL queries that systematically expand schema coverage compared to schema-only or random fuzzing approaches?
- **RQ2.** How does prompt engineering and context enrichment contribute to improving schema coverage?
- **RQ3.** To what extent can this pipeline discover meaningful GraphQL vulnerabilities over existing rule-based methods?

[^repo]: https://github.com/SLL288/prediql

### 4.1 Experimental Setup

**API Selection.** In our experimental evaluation, we employed a diverse spectrum of APIs, including open-source and openly hosted options. For open-source APIs, we obtained the backend code, established a self-hosted GraphQL server, and conducted tests. For openly hosted APIs, we utilized free-to-use reference APIs accessible on GitHub and conducted direct testing. The selected APIs are shown in Table 1.

**Table 1: GraphQL APIs used in baseline testing.**

| API | #Queries | #Mutations | #Objects |
|---|---:|---:|---:|
| UserWallet [13] | 11 | 15 | 5 |
| Countries [2] | 6 | 0 | 5 |
| Rick & Morty [11] | 9 | 0 | 7 |
| GraphQLZero [9] | 13 | 19 | 18 |
| EHRI [4] | 19 | 0 | 46 |
| TCGDex [12] | 6 | 0 | 12 |

**Baselines.** We evaluate PrediQL against four representative baselines that include both general-purpose and GraphQL-specific testing frameworks.

- **EvoMaster** — The only prior academic framework supporting GraphQL testing in both white-box and black-box modes. We use its black-box configuration for fair comparison. EvoMaster generates and sends GraphQL queries and mutations automatically, but employs evolutionary heuristics to mutate payloads dynamically and explore a wider response space [17–19].
- **ZAP** — An open-source black-box vulnerability scanner maintained by the Open Web Application Security Project (OWASP) [14]. Although originally designed for traditional web applications, it includes a module for GraphQL testing that performs introspection-based payload generation and common attack simulations.
- **BurpSuite** — A widely used commercial web security platform developed by PortSwigger [1]. For GraphQL testing, we enable the Auto GQL Scanner extension [29], which automatically identifies GraphQL endpoints and injects predefined payloads to detect vulnerabilities such as injection and schema disclosure.
- **GraphQLer** — A recent context-aware GraphQL security testing framework [50]. It constructs a dependency graph that captures producer–consumer relationships between queries and mutations, allowing the generation of realistic chained requests. GraphQLer demonstrates the benefit of dependency reasoning for GraphQL security testing and serves as the strongest baseline in our comparison.

**Model Selection.** For evaluation, we selected four LLMs spanning different developers, sizes, and design philosophies, as summarized in Table 2. Specifically, we included LLaMA 3.1 from Meta [10] as a representative open-source model, Gemini 2.5 Flash from Google DeepMind [5] as a lightweight and optimized variant of the Gemini family, GPT-5 Mini from OpenAI [6] as a smaller yet efficient version of the GPT-5 series, and DeepSeek R1 from DeepSeek AI [3], an open-source model that emphasizes reasoning and efficiency. This diverse selection allows us to cover both open-source and proprietary approaches, models optimized for speed as well as those focused on reasoning capabilities.

**Table 2: Technical specifications of LLMs used for GraphQL testing.**

| Model | Developer | Year | Size | Focus |
|---|---|---:|---|---|
| LLaMA 3.1 | Meta | 2024 | 8B | Open-source, efficient inference |
| Gemini 2.5 Flash | Google DeepMind | 2025 | Undisclosed | Cost-efficient reasoning |
| GPT-5 Mini | OpenAI | 2025 | Undisclosed | Optimized for speed |
| DeepSeek R1 | DeepSeek AI | 2025 | 671B | Reasoning and efficiency |

**Bandit Configuration Details.** For experimental evaluation, we instantiated eight distinct bandit arms, each representing a specific prompting strategy defined by four parameters: Schema, Arg Mode, Depth, and Top-k. Table 3 summarizes these configurations.

Each configuration corresponds to a balance between reliability and exploration. Conservative arms (e.g., `schema_min_known`) prioritize syntactic validity by reusing known parameter values and shallow nesting. Aggressive arms (e.g., `schema_deep_real`) promote deeper traversal and the synthesis of new argument values. The non-schema variants probe the LLM's ability to generalize without explicit schema guidance. The bandit dynamically reallocates probability mass toward arms that maximize successful, coverage-expanding executions.

**Table 3: Parameters defining adaptive arms in PrediQL's prompt generation.**

| Arm Name | Schema | Arg Mode | Depth | Top-k |
|---|:---:|:---:|:---:|:---:|
| `schema_min_known` | True | known | 1 | 3 |
| `schema_min_real` | True | real | 1 | 3 |
| `schema_mod_known` | True | known | 2 | 5 |
| `noschema_min_known` | False | known | 1 | 3 |
| `noschema_min_real` | False | real | 1 | 0 |
| `schema_min_nulls` | True | nulls | 1 | 3 |
| `schema_deep_known` | True | known | 3 | 5 |
| `schema_deep_real` | True | real | 3 | 5 |

**Evaluation Metric.** To address RQ1 and RQ2, we define the following coverage metric to evaluate GraphQL API testing:

$$
\text{Coverage} = \frac{\#\text{Unique Successful Responses}}{\#\text{Unique Nodes}}
$$

where coverage is the fraction of schema nodes that return valid, error-free data rather than just an HTTP 200 status. This metric reflects how much of the GraphQL schema is actually exercised by successful queries, providing a more accurate view of the API's reliability and robustness.

### 4.2 Schema Coverage (RQ1)

Table 4 compares the API coverage achieved by PrediQL against four baseline tools: ZAP, BurpSuite, EvoMaster, and GraphQLer.

**Table 4: Comparison of PrediQL and baseline methods in terms of coverage performance. Tests that could not be executed are marked as FAILED.**

| API | ZAP | Burp | EvoMaster | GraphQLer | PrediQL |
|---|---:|---:|---:|---:|---:|
| UserWallet | 50.00% | 7.69% | 61.54% | 92.31% | **96.15%** (+3.84%) |
| Countries | 33.33% | 50.00% | 50.00% | 50.00% | **100%** (+50.00%) |
| Rick & Morty | 33.33% | 0.00% | 66.67% | 66.67% | **100%** (+33.33%) |
| GraphQLZero | 93.75% | 93.75% | 71.88% | 93.75% | **100%** (+6.25%) |
| EHRI | 10.53% | 0.00% | 84.21% | 94.74% | **100%** (+5.26%) |
| TCGDex | 66.67% | 33.33% | 100% | 100% | **100%** (+0.00%) |

Across all evaluated APIs, PrediQL consistently attains the highest or near-highest coverage, demonstrating its ability to exercise a larger portion of the GraphQL schema through valid, data-returning queries. Traditional black-box scanners such as ZAP and BurpSuite achieve limited coverage because they lack awareness of GraphQL's hierarchical structure and query dependencies. EvoMaster performs better by generating dynamic requests, but still falls short on complex schemas. GraphQLer improves coverage by incorporating schema context, yet PrediQL surpasses it in nearly all cases by integrating retrieval-augmented reasoning and adaptive query generation. Note that the reported PrediQL results correspond to its configuration with the best-performing LLM.

Table 5 presents the performance of tested large language models across different GraphQL APIs.

**Table 5: Coverage achieved by different language models across GraphQL APIs.**

| API | LLaMA 3.1 | Gemini 2.5 | GPT-5 Mini | DeepSeek R1 |
|---|---:|---:|---:|---:|
| UserWallet | 88.46% | 96.15% | 96.15% | 88.46% |
| Countries | 100% | 100% | 100% | 100% |
| Rick & Morty | 100% | 100% | 100% | 100% |
| GraphQLZero | 100% | 100% | 100% | 100% |
| EHRI | 78.94% | 100% | 100% | 100% |
| TCGDex | 100% | 83.33% | 100% | 100% |

Overall, all models achieve high coverage on simpler or well-structured APIs such as Countries, Rick & Morty, GraphQLZero, and TCGDex, indicating that these schemas are easier to navigate and query successfully. However, differences emerge on more complex or noisy schemas such as UserWallet and EHRI. GPT-5 Mini and Gemini 2.5 consistently produce the most stable and complete results, suggesting stronger schema understanding and query-adaptation capabilities. LLaMA 3.1 performs comparably but occasionally misses certain paths. In contrast, DeepSeek R1 positions itself as the second-most proficient model on specific APIs, closely following GPT-5 Mini. These findings suggest that stronger reasoning models maintain high coverage under schema complexity, indicating better adaptability and understanding of GraphQL structures.

> **Conclusion for RQ1.** PrediQL consistently outperforms all baseline tools in schema coverage across diverse APIs. Its context-aware input inference and semantic reasoning enable more accurate and comprehensive query generation. On average, PrediQL achieves a 16% improvement with a maximum improvement of 50% in schema coverage over the second-best model.

### 4.3 Prompt Engineering Impact (RQ2)

Prompt engineering is central to steering the reasoning capabilities of LLMs in improving schema coverage and discovering vulnerabilities in APIs. To address RQ2, we conduct an ablation study that isolates the contribution of each prompt-enrichment component. This analysis quantifies how each module influences schema coverage and overall testing effectiveness. The corresponding configurations are detailed below.

- **PrediQL-BASE.** The baseline configuration provides only the minimal schema context and expected response format. It guides the model to produce syntactically valid GraphQL queries.
- **PrediQL-AQG.** Building on the baseline, the adaptive query generation configuration integrates both multi-armed bandit selection and retrieval-augmented generation, which is essential for the known-values arm setting to enable adaptive and context-aware query synthesis.
- **PrediQL-SCL.** The self-correction feedback loop configuration enhances the baseline prompt, adding an error-aware refinement cycle. Failed or invalid queries are logged with their corresponding error messages and reinjected into subsequent prompts as corrective context.
- **PrediQL.** The full pipeline, combining adaptive query generation, retrieval augmentation, and self-correction into a single closed-loop system.

Table 6 evaluates the contribution of individual prompt-engineering components: the base prompt (BASE), the self-correction loop (SCL), and adaptive query generation (AQG). Contributions are computed for models that experienced enhancements from PrediQL-BASE to PrediQL.

**Table 6: Ablation study on prompt engineering components. BASE, AQG, and SCL denote PrediQL-BASE, PrediQL-AQG, and PrediQL-SCL, respectively.**

| API | GPT-5 Mini BASE | SCL | AQG | PrediQL | Gemini 2.5 BASE | SCL | AQG | PrediQL | DeepSeek R1 BASE | SCL | AQG | PrediQL | LLaMA 3.1 BASE | SCL | AQG | PrediQL |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| UserWallet | 19.23% | 38.46% | 61.53% | 96.15% | 19.23% | 26.92% | 65.38% | 96.15% | 19.23% | 30.76% | 65.38% | 96.15% | 38.46% | 42.30% | 84.61% | 88.46% |
| Countries | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| Rick & Morty | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| GraphQLZero | 81% | 100% | 87.5% | 100% | 81% | 100% | 91% | 100% | 100% | 100% | 100% | 100% | 90% | 100% | 96.87% | 100% |
| EHRI | 100% | 100% | 100% | 100% | 74% | 74% | 100% | 100% | 52.63% | 52.63% | 84.21% | 100% | 52% | 100% | 100% | 78.94% |
| TCGDex | 100% | 100% | 100% | 100% | 83% | 83% | 83% | 83% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |

Across models and APIs, the incremental addition of these modules consistently improves schema coverage, confirming that each contributes complementary benefits. PrediQL-BASE alone often yields limited coverage, particularly in complex schemas such as UserWallet and EHRI, where naive prompting fails to satisfy nested or dependent field constraints. Introducing the self-correction loop (PrediQL-SCL) markedly reduces repeated schema violations, increasing coverage by 10–25% depending on the model capacity. Adaptive query generation (PrediQL-AQG) provides an additional boost to APIs that require realistic parameter inference, increasing coverage by as much as 26% on EHRI and 15% on GraphQLZero for Gemini 2.5. When both mechanisms are combined in PrediQL, coverage approaches or reaches 100% in almost all APIs and models.

Smaller open-source models such as LLaMA 3.1 follow the same pattern but exhibit slightly higher variance, reflecting reduced stability in long-context reasoning. Larger models (GPT-5 Mini, DeepSeek R1) demonstrate less sensitivity to prompt enrichment, suggesting that reasoning-oriented architectures benefit more from the feedback of retrieval and correction than from raw scale alone. In general, ablation confirms that the design gains of PrediQL stem from the synergy of retrieval grounding, adaptive prompting, and iterative self-correction, rather than from model size alone.

> **Conclusion for RQ2.** Overall, prompt engineering significantly enhances PrediQL's ability to achieve broader and more accurate schema coverage. By integrating adaptive query generation and self-correction, the system effectively adapts, learns, and refines its queries over iterations. This synergy results in a more intelligent, reliable, and efficient API exploration process.

### 4.4 Vulnerability Detection (RQ3)

Table 7 summarizes the vulnerability detection results across GraphQLer and the different configurations of PrediQL. Among existing GraphQL testing tools, only GraphQLer includes a built-in vulnerability detection module, while others, such as EvoMaster and ZAP, primarily focus on coverage measurement or payload fuzzing. Therefore, GraphQLer serves as the most relevant baseline for assessing detection capacity.

**Table 7: Comparison of vulnerability detection performance between GraphQLer and PrediQL variants.**

| API | GraphQLer (Vuln.) | GraphQLer (Cat.) | LLaMA 3.1 (Vuln.) | LLaMA 3.1 (Cat.) | Gemini 2.5 (Vuln.) | Gemini 2.5 (Cat.) | GPT-5 Mini (Vuln.) | GPT-5 Mini (Cat.) | DeepSeek R1 (Vuln.) | DeepSeek R1 (Cat.) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| UserWallet | 26 | 7 | 31 | 11 | 41 | 7 | 20 | 6 | 34 | 8 |
| Countries | 6 | 2 | 7 | 3 | 9 | 2 | 9 | 4 | 7 | 3 |
| Rick & Morty | 12 | 3 | 10 | 10 | 13 | 4 | 11 | 4 | 14 | 6 |
| GraphQLZero | 37 | 8 | 35 | 7 | 37 | 7 | 44 | 6 | 34 | 7 |
| EHRI | 11 | 3 | 15 | 12 | 21 | 2 | 26 | 2 | 3 | 3 |
| TCGDex | 6 | 1 | 7 | 1 | 10 | 2 | 8 | 2 | 7 | 2 |

*Columns denote the number of unique vulnerabilities found ("Vuln.") and the number of distinct vulnerability categories ("Cat.") for each tool/model configuration.*

Across all evaluated APIs, PrediQL consistently identifies a greater number and a wider range of vulnerabilities. While GraphQLer mainly exposes schema-level and input-validation flaws, PrediQL leverages retrieval-augmented reasoning and adaptive arm selection to detect deeper logic- and context-dependent weaknesses such as HTML injection, SSRF, and OS command injection. The variants PrediQL-Gemini and PrediQL-GPT-5 achieve the highest detection counts, improving unique findings by 20–40% on complex benchmarks such as UserWallet and GraphQLZero. In general, these results confirm that LLM-guided reasoning substantially enhances vulnerability discovery beyond static or heuristic testing baselines.

Qualitative analysis shows that PrediQL detects a broader spectrum of vulnerability categories compared to GraphQLer, including deeper logic and context-dependent flaws. Its reasoning traces link each issue to its execution context (e.g., leaked variables or inconsistent authorization responses), enabling precise, evidence-based triaging.

> **Conclusion for RQ3.** PrediQL substantially advances vulnerability discovery beyond rule-based baselines. Its context-aware reasoning enables the LLM to correlate schema structure, response semantics, and execution traces, revealing logic and injection flaws that static or signature-driven tools overlook. Across all evaluated APIs, PrediQL achieves broader and deeper vulnerability coverage, demonstrating that adaptive, retrieval-guided analysis is essential to uncovering complex security weaknesses in GraphQL APIs.

---

## 5. Discussion

Our evaluation demonstrates that PrediQL consistently outperforms all existing GraphQL testing frameworks. This section discusses key observations, broader implications, and open research directions.

**Impact of Model Size.** Larger models such as GPT-5 Mini and DeepSeek R1 achieved higher semantic coherence and reasoning stability, while smaller open-source models (e.g., LLaMA 3.1) remained competitive at a fraction of the computational cost. This highlights a practical trade-off between reasoning depth and efficiency. When equipped with retrieval memory and adaptive prompting, lightweight models can approximate the performance of proprietary ones. A promising direction is to adopt hybrid configurations, using larger models for seed generation and schema understanding, followed by smaller models for iterative fuzzing, to balance throughput, coverage, and cost.

**Implications Beyond GraphQL.** The mechanisms introduced in PrediQL — adaptive arm selection, self-corrective prompting, and retrieval-grounded reasoning — are not specific to GraphQL. These ideas extend naturally to other structured interface testing domains such as REST, gRPC, and JSON-RPC [38]. More broadly, PrediQL demonstrates that retrieval-augmented reasoning and bandit-driven exploration can complement traditional coverage-guided and evolutionary fuzzing. Integrating symbolic reasoning or static program analysis into such adaptive loops may bridge the gap between semantic understanding and execution-level precision, enabling more generalizable automated security testing frameworks.

**Limitations.** While effective, PrediQL is not without constraints:

- **Execution cost and rate limits.** LLM-guided fuzzing remains computationally intensive, and API rate throttling can slow feedback cycles.
- **Context window constraints.** Even with retrieval augmentation, large schemas can exceed model context limits, leading to partial prompt conditioning and missed relationships.
- **Response interpretation ambiguity.** The context-aware detector can identify likely vulnerabilities, but some cases still require human validation to confirm exploitability.
- **Model bias and non-determinism.** Variations in model architecture and decoding strategies lead to inconsistent results, motivating ensemble or calibration techniques for reproducibility.

**Future Work.** The growing ecosystem of agentic LLM frameworks offers a natural evolution path for PrediQL. A multi-agent design, with specialized agents for query generation, evaluation, and refinement, could enable continuous self-improvement and deeper exploit discovery. Another direction is the development of domain-specialized LLMs for API and schema reasoning, analogous to text-to-SQL models, which could reduce prompt overhead while improving precision and generalization. Finally, exploring hybrid systems that couple LLM reasoning with program analysis or formal verification could enable both semantic adaptability and provable assurance.

---

## 6. Conclusion

PrediQL shows that the combination of retrieval, reasoning, and adaptive learning can fundamentally improve the way GraphQL APIs are tested. By integrating large language models into the fuzzing loop, it transforms random exploration into guided reasoning, allowing the system to understand schemas, infer dependencies, and generate purposeful queries. Through multi-armed bandit strategy selection, PrediQL learns which testing behaviors yield the most valuable feedback, achieving higher coverage and uncovering vulnerabilities that existing tools consistently miss.

Beyond its empirical gains, PrediQL reveals a deeper insight: LLMs can act not only as generators but as analysts that interpret system behavior. This ability to connect input, responses, and context enables the detection of complex logic-level flaws that evade rule-based or pattern-driven scanners. These results mark a step towards autonomous, self-improving security testing, where models learn from every execution to test smarter over time. Future extensions will explore collaborative, multi-agent setups and large-scale retrieval across heterogeneous APIs, paving the way for intelligent systems that continuously learn the structure and weaknesses of modern web applications.

---

## References

[1] Burp suite. https://portswigger.net/burp. Accessed: 2025-10-03.

[2] Countries graphql api. https://countries.trevorblades.com/. Accessed: October 2025.

[3] Deepseek r1 vs gpt-5 mini (model comparison). https://aimodels.fyi/compare/deepseek-r1-vs-gpt-5-mini. Accessed 2025-10-07.

[4] European holocaust research infrastructure (EHRI) graphql api. https://portal.ehri-project.eu/api/graphql. Accessed: October 2025.

[5] Gemini 2.5 flash model. https://deepmind.google/models/gemini/flash/. Accessed 2025-10-07.

[6] Gpt-5 mini vs gemini 2.5 flash (model comparison). https://artificialanalysis.ai/models/comparisons/gpt-5-mini-vs-gemini-2-5-flash. Accessed 2025-10-07.

[7] Graphql security (official guide). https://graphql.org/learn/security/. Accessed 2025-10-04.

[8] Graphql vs REST api — difference between api design styles. https://aws.amazon.com/compare/the-difference-between-graphql-and-rest/. Accessed 2025-10-04.

[9] Graphqlzero api. https://graphqlzero.almansi.me/. Accessed: October 2025.

[10] Meta llama 3.1 8b. https://huggingface.co/meta-llama/Llama-3.1-8B. Accessed 2025-10-07.

[11] Rick and morty graphql api. https://rickandmortyapi.com/graphql. Accessed: October 2025.

[12] Tcgdex graphql api. https://api.tcgdex.net/v2/graphql. Accessed: October 2025.

[13] Userwallet graphql api. https://github.com/graphql-compose/graphql-compose-examples/tree/master/examples/user-wallet. Accessed: October 2025.

[14] Owasp zed attack proxy (ZAP). https://www.zaproxy.org/, 2024.

[15] Agrawal, S., and Goyal, N. Analysis of thompson sampling for the multi-armed bandit problem. *arXiv preprint arXiv:1111.1797* (2011).

[16] Andersson, T. Rest api vs graphql — a literature and experimental study. https://www.diva-portal.org/smash/get/diva2:1571154/FULLTEXT01.pdf, 2021.

[17] Arcuri, A., Galeotti, J. P., Marculescu, B., and Zhang, M. Evomaster: A search-based system test generation tool. *Journal of Open Source Software* 6, 57 (2021), 2153.

[18] Belhadi, A., Zhang, M., and Arcuri, A. Random testing and evolutionary testing for fuzzing graphql apis. *ACM Transactions on the Web* (2023).

[19] Belhadi, Y., and Arcuri, A. Evomaster for GraphQL: Black-box test generation for web APIs. In *Proceedings of the 38th IEEE/ACM International Conference on Automated Software Engineering (ASE)* (2023), IEEE, pp. 1503–1507.

[20] Cavenaghi, E., et al. Non-stationary multi-armed bandit: Empirical evaluation of f-discounted-sliding-window thompson sampling. *Entropy* 23, 3 (2021), 380.

[21] Chen, C., Dolan-Gavitt, B., and Lin, Z. Elfuzz: Efficient input generation via llm-driven synthesis over fuzzer space. In *Proceedings of the 34th USENIX Security Symposium* (2025), USENIX Association. to appear.

[22] Deng, Y., Xia, C. S., Peng, H., Yang, C., and Zhang, L. Large language models are zero-shot fuzzers: Fuzzing deep-learning libraries via large language models. *arXiv preprint arXiv:2212.14834* (2022).

[23] Douze, M., Guzhva, A., Deng, C., Johnson, J., Szilvasy, G., Mazaré, P.-E., Lomeli, M., Hosseini, L., and Jégou, H. The faiss library.

[24] Doyensec. Crackql: Graphql security testing tool. https://github.com/doyensec/CrackQL, 2021. Accessed: 2025-10-04.

[25] Escape. The state of graphql security 2024. Tech. rep., Escape Technologies, 2024. Accessed: October 2025.

[26] Escape Technologies. Graphql-cop: Security scanner for graphql apis. https://github.com/escape-technologies/graphql-cop, 2023. Accessed: 2025-10-04.

[27] Fastly. Exploring the security implications of GraphQL. https://www.fastly.com/blog/exploring-the-security-implications-of-graphql, 2022.

[28] Fioraldi, A., Maier, D., Eissfeldt, H., and Heuse, M. Afl++: Combining incremental steps of fuzzing research. In *14th USENIX Workshop on Offensive Technologies (WOOT 20)* (2020).

[29] Forward Security. Autogql: Auto GraphQL scanner for burp suite. https://github.com/FWDSEC/burp-auto-gql, 2023. Accessed: 2025-10-07.

[30] Google. Oss-fuzz – continuous fuzzing for open source software. https://github.com/google/oss-fuzz, 2024. Accessed: 2025-10-04.

[31] GraphCrawler Project. Graphcrawler: Automated graphql introspection and fuzzing tool. https://github.com/gsmith257-cyber/GraphCrawler, 2022. Accessed: 2025-10-04.

[32] Hatfield-Dodds, Z., et al. Deriving semantics-aware fuzzers from web API schemas, 2021.

[33] Huang, L., Zhao, P., Chen, H., and Ma, L. Large language models based fuzzing techniques: A survey. *arXiv preprint arXiv:2402.00350* (2024).

[34] Hygraph. Graphql survey 2024, 2024. Accessed: October 2025.

[35] IBM PTC Security. Denial of service attacks with GraphQL. https://medium.com/@ibm_ptc_security/denial-of-service-attacks-with-graphql-77189a6ba85b, 2023.

[36] Jin, Y., et al. Fuzzgpt: Harnessing large language models for effective api fuzzing. In *Proceedings of the 33rd USENIX Security Symposium* (2024).

[37] Johnson, J., Douze, M., and Jégou, H. Billion-scale similarity search with GPUs. *IEEE Transactions on Big Data* (2019).

[38] JSON-RPC Working Group. Json-rpc 2.0 specification. https://www.jsonrpc.org/specification, 2013. Origin date 2010-03-26, updated 2013-01-04, accessed 2025-10-07.

[39] Kesarwani, M., Ghosh, S., Gupta, N., Chakraborty, S., Sindhgatta, R., Mehta, S., Eberhardt, C., and Debrunner, D. Graphql query generation: A large training and benchmarking dataset. pp. 1595–1607.

[40] Lattimore, T., and Szepesvári, C. *Bandit Algorithms.* Cambridge University Press, 2020.

[41] Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W.-t., Rocktäschel, T., et al. Retrieval-augmented generation for knowledge-intensive NLP tasks. In *Advances in Neural Information Processing Systems* (2020), vol. 33, pp. 9459–9474.

[42] LLVM Project. libfuzzer – a library for coverage-guided fuzzing. https://llvm.org/docs/LibFuzzer.html, 2024. Accessed: 2025-10-04.

[43] Madaan, A., Zhou, S., Alon, U., Sonkar, S., Gupta, P., Yang, Y., and Neubig, G. Self-refine: Iterative refinement with self-feedback. In *Advances in Neural Information Processing Systems (NeurIPS)* (2023).

[44] McFadden, S., Maugeri, M., Hicks, C., Mavroudis, V., and Pierazzi, F. Wendigo: Deep reinforcement learning for denial-of-service query discovery in graphql. In *2024 IEEE Security and Privacy Workshops (SPW)* (2024), pp. 68–75.

[45] Meng, R., Duck, G. J., and Roychoudhury, A. Large language model assisted hybrid fuzzing. *arXiv* (2024).

[46] Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C. L., Mishkin, P., Zhang, C., Agarwal, S., Slama, K., Ray, A., Schulman, J., Hilton, J., Miller, L., Simens, M., Askell, A., Welinder, P., Christiano, P., Leike, J., and Lowe, R. Training language models to follow instructions with human feedback. *arXiv preprint arXiv:2203.02155* (2022).

[47] Perera, I., Abeyrathne, H., Malalgoda, S., and Ifthikar, A. Enhancing graphql security by detecting malicious queries using large language models, sentence transformers, and convolutional neural networks. *arXiv preprint arXiv:2508.11711* (2025). arXiv:2508.11711v1 [cs.CR].

[48] Reimers, N., and Gurevych, I. Sentence-bert: Sentence embeddings using siamese bert-networks. In *Proceedings of EMNLP* (2019), pp. 3982–3992.

[49] TechTarget. What's next for apis? 4 api trends for 2025 and beyond, 2024. Accessed: October 2025.

[50] Tsai, Y., Zhang, T., et al. Graphqler: Enhancing graphql security with context-aware api testing. *arXiv preprint arXiv:2504.13358* (2025).

[51] Xia, C., Wang, R., Meng, Y., Tang, Z., Wang, Y., Xue, Y., Li, X., and Chen, X. Fuzz4all: Universal fuzzing with large language models. In *Proceedings of the 46th International Conference on Software Engineering (ICSE)* (2024), ACM, pp. 1–13.

[52] Zhang, T., et al. Dfuzz: Large language models for deep api fuzzing with white-box guidance. In *Proceedings of the 47th International Conference on Software Engineering (ICSE)* (2025), IEEE/ACM.
