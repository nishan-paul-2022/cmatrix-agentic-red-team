Title: PrediQL: Automated Testing of GraphQL APIs with LLMs

Source: https://arxiv.org/html/2510.10407v1

---

1. [1 INTRODUCTION](https://arxiv.org/html/2510.10407v1#S1)
2. 
[2 BACKGROUND & RELATED WORK](https://arxiv.org/html/2510.10407v1#S2)

[2.1 GraphQL Fundamentals](https://arxiv.org/html/2510.10407v1#S2.SS1)
[2.2 GraphQL Vulnerabilities](https://arxiv.org/html/2510.10407v1#S2.SS2)
[2.3 Related Work](https://arxiv.org/html/2510.10407v1#S2.SS3)


3. [2.1 GraphQL Fundamentals](https://arxiv.org/html/2510.10407v1#S2.SS1)
4. [2.2 GraphQL Vulnerabilities](https://arxiv.org/html/2510.10407v1#S2.SS2)
5. [2.3 Related Work](https://arxiv.org/html/2510.10407v1#S2.SS3)
6. 
[3 METHODOLOGY](https://arxiv.org/html/2510.10407v1#S3)

[3.1 Schema Modeling](https://arxiv.org/html/2510.10407v1#S3.SS1)
[3.2 Adaptive Query Generation](https://arxiv.org/html/2510.10407v1#S3.SS2)
[3.3 Execution and Feedback](https://arxiv.org/html/2510.10407v1#S3.SS3)
[3.4 Closed-Loop Integration](https://arxiv.org/html/2510.10407v1#S3.SS4)


7. [3.1 Schema Modeling](https://arxiv.org/html/2510.10407v1#S3.SS1)
8. [3.2 Adaptive Query Generation](https://arxiv.org/html/2510.10407v1#S3.SS2)
9. [3.3 Execution and Feedback](https://arxiv.org/html/2510.10407v1#S3.SS3)
10. [3.4 Closed-Loop Integration](https://arxiv.org/html/2510.10407v1#S3.SS4)
11. 
[4 EVALUATION](https://arxiv.org/html/2510.10407v1#S4)

[4.1 Experimental Setup](https://arxiv.org/html/2510.10407v1#S4.SS1)
[4.2 Schema Coverage (RQ1)](https://arxiv.org/html/2510.10407v1#S4.SS2)
[4.3 Prompt Engineering Impact (RQ2)](https://arxiv.org/html/2510.10407v1#S4.SS3)
[4.4 Vulnerability Detection (RQ3)](https://arxiv.org/html/2510.10407v1#S4.SS4)


12. [4.1 Experimental Setup](https://arxiv.org/html/2510.10407v1#S4.SS1)
13. [4.2 Schema Coverage (RQ1)](https://arxiv.org/html/2510.10407v1#S4.SS2)
14. [4.3 Prompt Engineering Impact (RQ2)](https://arxiv.org/html/2510.10407v1#S4.SS3)
15. [4.4 Vulnerability Detection (RQ3)](https://arxiv.org/html/2510.10407v1#S4.SS4)
16. [5 Discussion](https://arxiv.org/html/2510.10407v1#S5)
17. [6 Conclusion](https://arxiv.org/html/2510.10407v1#S6)
[1 INTRODUCTION](https://arxiv.org/html/2510.10407v1#S1)
[2 BACKGROUND & RELATED WORK](https://arxiv.org/html/2510.10407v1#S2)
1. [2.1 GraphQL Fundamentals](https://arxiv.org/html/2510.10407v1#S2.SS1)
2. [2.2 GraphQL Vulnerabilities](https://arxiv.org/html/2510.10407v1#S2.SS2)
3. [2.3 Related Work](https://arxiv.org/html/2510.10407v1#S2.SS3)
[2.1 GraphQL Fundamentals](https://arxiv.org/html/2510.10407v1#S2.SS1)
[2.2 GraphQL Vulnerabilities](https://arxiv.org/html/2510.10407v1#S2.SS2)
[2.3 Related Work](https://arxiv.org/html/2510.10407v1#S2.SS3)
[3 METHODOLOGY](https://arxiv.org/html/2510.10407v1#S3)
1. [3.1 Schema Modeling](https://arxiv.org/html/2510.10407v1#S3.SS1)
2. [3.2 Adaptive Query Generation](https://arxiv.org/html/2510.10407v1#S3.SS2)
3. [3.3 Execution and Feedback](https://arxiv.org/html/2510.10407v1#S3.SS3)
4. [3.4 Closed-Loop Integration](https://arxiv.org/html/2510.10407v1#S3.SS4)
[3.1 Schema Modeling](https://arxiv.org/html/2510.10407v1#S3.SS1)
[3.2 Adaptive Query Generation](https://arxiv.org/html/2510.10407v1#S3.SS2)
[3.3 Execution and Feedback](https://arxiv.org/html/2510.10407v1#S3.SS3)
[3.4 Closed-Loop Integration](https://arxiv.org/html/2510.10407v1#S3.SS4)
[4 EVALUATION](https://arxiv.org/html/2510.10407v1#S4)
1. [4.1 Experimental Setup](https://arxiv.org/html/2510.10407v1#S4.SS1)
2. [4.2 Schema Coverage (RQ1)](https://arxiv.org/html/2510.10407v1#S4.SS2)
3. [4.3 Prompt Engineering Impact (RQ2)](https://arxiv.org/html/2510.10407v1#S4.SS3)
4. [4.4 Vulnerability Detection (RQ3)](https://arxiv.org/html/2510.10407v1#S4.SS4)
[4.1 Experimental Setup](https://arxiv.org/html/2510.10407v1#S4.SS1)
[4.2 Schema Coverage (RQ1)](https://arxiv.org/html/2510.10407v1#S4.SS2)
[4.3 Prompt Engineering Impact (RQ2)](https://arxiv.org/html/2510.10407v1#S4.SS3)
[4.4 Vulnerability Detection (RQ3)](https://arxiv.org/html/2510.10407v1#S4.SS4)
[5 Discussion](https://arxiv.org/html/2510.10407v1#S5)
[6 Conclusion](https://arxiv.org/html/2510.10407v1#S6)

[shaolun.liu@sfu.ca, sina.marefat@kntu.ac.ir, omar@ztasecurity.com,](mailto:shaolun.liu@sfu.ca,%20sina.marefat@kntu.ac.ir,%20omar@ztasecurity.com,)
[yca518@sfu.ca, zda35@sfu.ca, jwa454@sfu.ca, tayebi@sfu.ca](mailto:%20yca518@sfu.ca,%20zda35@sfu.ca,%20jwa454@sfu.ca,%20tayebi@sfu.ca)

###### Abstract.
GraphQL’s flexible query model and nested data dependencies expose APIs to complex, context-dependent vulnerabilities that are difficult to uncover using conventional testing tools. Existing fuzzers either rely on random payload generation or rigid mutation heuristics, failing to adapt to the dynamic structures of GraphQL schemas and responses. We present PrediQL, the first retrieval-augmented, LLM-guided fuzzer for GraphQL APIs. PrediQL combines large language model reasoning with adaptive feedback loops to generate semantically valid and diverse queries. It models the choice of fuzzing strategy as a multi-armed bandit problem, balancing exploration of new query structures with exploitation of past successes. To enhance efficiency, PrediQL retrieves and reuses execution traces, schema fragments, and prior errors, enabling self-correction and progressive learning across test iterations. Beyond input generation, PrediQL integrates a context-aware vulnerability detector that uses LLM reasoning to analyze responses, interpreting data values, error messages, and status codes to identify issues such as injection flaws, access-control bypasses, and information disclosure. Our evaluation across open-source and benchmark GraphQL APIs shows that PrediQL achieves significantly higher coverage and vulnerability discovery rates compared to state-of-the-art baselines. These results demonstrate that combining retrieval-augmented reasoning with adaptive fuzzing can transform API security testing from reactive enumeration to intelligent exploration.

Modern software systems are often built from many independent microservices that communicate through well-defined APIs. Among contemporary API styles, GraphQL has gained significant adoption because it allows clients to request precisely the data they need through a single flexible endpoint. This design improves efficiency and mitigates the problem of over-fetching, common in REST ([aws_graphql_rest_2024,](https://arxiv.org/html/2510.10407v1#bib.bib8); [andersson2021rest_graphql_grpc,](https://arxiv.org/html/2510.10407v1#bib.bib16)) or gRPC ([aws_graphql_rest_2024,](https://arxiv.org/html/2510.10407v1#bib.bib8)) APIs.
According to a 2024 industry survey, approximately 61% of respondents reported using GraphQL in production, and about 10 % indicated that they were replacing REST with GraphQL in their systems ([techtarget2024graphql,](https://arxiv.org/html/2510.10407v1#bib.bib49); [hygraph2024survey,](https://arxiv.org/html/2510.10407v1#bib.bib34)). However, this widespread adoption has also exposed security weaknesses in many deployments. A recent study reported that roughly 69 % of the scanned public GraphQL API services suffered from unrestricted resource consumption vulnerabilities, making them susceptible to denial of service (DoS) attacks via deep-nested or costly queries ([escape2024security,](https://arxiv.org/html/2510.10407v1#bib.bib25); [ibm_dos_graphql_2023,](https://arxiv.org/html/2510.10407v1#bib.bib35); [fastly_graphql_security_2022,](https://arxiv.org/html/2510.10407v1#bib.bib27)). These issues highlight that GraphQL introduces unique security challenges, such as unbounded query depth, schema exposure, injection in nested arguments, and inconsistent access control across linked queries and mutations ([graphql_security_page_2025,](https://arxiv.org/html/2510.10407v1#bib.bib7)). Consequently, effective testing of GraphQL APIs requires more than traditional input fuzzing; it must incorporate contextual understanding of schema relationships and multistep interactions.
Existing testing tools fall into two main groups: black-box fuzzers and schema-aware fuzzers. Black-box fuzzers explore input space randomly, but do not respect GraphQL structure. Schema-aware tools, such as EvoMaster ([belhadi2023evomaster,](https://arxiv.org/html/2510.10407v1#bib.bib18); [arcuri2021evomaster,](https://arxiv.org/html/2510.10407v1#bib.bib17); [belhadi2023graphql,](https://arxiv.org/html/2510.10407v1#bib.bib19)), improve test coverage by using the schema; but rely on simple template mutations and ignore cross-field or cross-operation dependencies. Recent systems such as GraphQLer ([graphqler2025,](https://arxiv.org/html/2510.10407v1#bib.bib50)) take an important step by analyzing producer–consumer relationships between queries and mutations, discovering vulnerabilities missed by older tools. However, even these approaches remain static; their generation logic does not adapt to execution feedback or changing context. In short, current GraphQL fuzzers cannot yet reason adaptively about API behavior.

Recent advances in large language models (LLMs) offer a new direction on how to build intelligent, feedback-driven fuzzers. LLMs can reason about structured input formats, infer valid parameters from schema fragments, and generate meaningful queries ([ouyang2022instructgpt,](https://arxiv.org/html/2510.10407v1#bib.bib46); [madaan2023selfrefine,](https://arxiv.org/html/2510.10407v1#bib.bib43)). When combined with retrieval mechanisms that use past traces, schema segments, or error logs ([lewis2020rag,](https://arxiv.org/html/2510.10407v1#bib.bib41); [reimers2019sbert,](https://arxiv.org/html/2510.10407v1#bib.bib48); [johnson2019faiss,](https://arxiv.org/html/2510.10407v1#bib.bib37)), the fuzzer can refine future inputs based on what it has already learned. Recent LLM-assisted fuzzing solutions ([xia2023fuzz4all,](https://arxiv.org/html/2510.10407v1#bib.bib51); [fuzzgpt2024,](https://arxiv.org/html/2510.10407v1#bib.bib36); [deng2022titanfuzz,](https://arxiv.org/html/2510.10407v1#bib.bib22); [meng2024hyllfuzz,](https://arxiv.org/html/2510.10407v1#bib.bib45); [zhang2025dfuzz,](https://arxiv.org/html/2510.10407v1#bib.bib52); [surveyllmfuzz2024,](https://arxiv.org/html/2510.10407v1#bib.bib33)) show that generative reasoning improves coverage in binary and protocol fuzzing. Yet, no prior research has applied LLM-based fuzzing to GraphQL, whose nested queries and dependency-rich structure require contextual reasoning and adaptive feedback. Work such as WENDIGO ([ieee10579536,](https://arxiv.org/html/2510.10407v1#bib.bib44)) targets denial-of-service discovery in GraphQL using deep reinforcement learning, and Perera et al. ([perera2025enhancing,](https://arxiv.org/html/2510.10407v1#bib.bib47)) explore detecting malicious GraphQL queries with LLMs and neural classifiers, but neither focuses on adaptive fuzzing.
To close this gap, we present PrediQL, an automated GraphQL testing framework that joins schema introspection, retrieval-augmented LLM prompting ([lewis2020rag,](https://arxiv.org/html/2510.10407v1#bib.bib41)), multi-armed bandit learning ([lattimore2020bandit,](https://arxiv.org/html/2510.10407v1#bib.bib40); [agrawal2011ts,](https://arxiv.org/html/2510.10407v1#bib.bib15); [cavenaghi2021nonstationary,](https://arxiv.org/html/2510.10407v1#bib.bib20)) and self-correction into a single feedback loop. PrediQL treats the LLM as a guided component rather than an oracle. It first extracts schema information through introspection and then retrieves relevant examples and past errors to generate the query in real feedback. A bandit-based selector dynamically chooses between different prompting strategies, balancing exploration and exploitation. This design allows PrediQL to generate valid, diverse, and context-sensitive queries that explore deeper parts of the schema and reveal complex vulnerabilities.
We evaluated PrediQL using multiple large language models across a diverse set of open-source and benchmark GraphQL APIs. The results show that PrediQL consistently improves test coverage, by an average of 16% with a maximum improvement of 50%, and discovers more context-dependent vulnerabilities compared to established baselines. Among the tested configurations, the GPT-5 Mini achieved the highest coverage, while smaller models like Llama-3-8B offered competitive results with reduced computational cost. In addition to broader coverage, PrediQL demonstrates stronger vulnerability detection capabilities, accurately identifying injection flaws, access control bypasses, and information disclosure cases that existing tools often miss.
In summary, this paper makes three main contributions: (1) We present PrediQL, the first retrieval-augmented, LLM-guided GraphQL fuzzer with adaptive strategy selection, modeled as a multi-armed bandit problem ([lattimore2020bandit,](https://arxiv.org/html/2510.10407v1#bib.bib40); [agrawal2011ts,](https://arxiv.org/html/2510.10407v1#bib.bib15); [cavenaghi2021nonstationary,](https://arxiv.org/html/2510.10407v1#bib.bib20)) to improve efficiency and reduce redundant requests. (2) We design a context-aware vulnerability detector that leverages LLM reasoning to interpret responses and identify diverse vulnerability categories beyond static rule-based detection. (3) We conduct extensive experimental evaluation on open-source and benchmark GraphQL APIs, demonstrating that PrediQL achieves higher coverage and detects more context-dependent vulnerabilities than existing tools.

Modern web applications increasingly adopt GraphQL for its flexible and efficient data fetching model. While this paradigm simplifies client–server interaction, it also introduces a new class of security challenges that differ from those found in traditional REST APIs. In this section, we first review the fundamentals of GraphQL, then summarize its known vulnerability classes, and finally discuss prior work on API testing, GraphQL security analysis, large language model (LLM)–assisted fuzzing, prompt engineering, and adaptive test strategy selection.

GraphQL provides a structured and flexible alternative to traditional REST APIs, offering three key features ([graphql_security_page_2025,](https://arxiv.org/html/2510.10407v1#bib.bib7); [aws_graphql_rest_2024,](https://arxiv.org/html/2510.10407v1#bib.bib8); [andersson2021rest_graphql_grpc,](https://arxiv.org/html/2510.10407v1#bib.bib16)):
- 
⋄\diamond

Data as a graph: GraphQL organizes data as a graph of interconnected objects, allowing clients to retrieve all required information in a single request and mitigating both under-fetching and over-fetching.


- 
⋄\diamond

Strong typing: Each GraphQL API exposes a schema that defines data types (objects) and operations (queries and mutations). This strong type system ensures predictable responses, simplifies error handling, and requires clients to explicitly specify which fields to return.


- 
⋄\diamond

Single endpoint. All requests are processed through a unified endpoint, providing a consistent interface for both data retrieval and modification.


Data as a graph: GraphQL organizes data as a graph of interconnected objects, allowing clients to retrieve all required information in a single request and mitigating both under-fetching and over-fetching.
Strong typing: Each GraphQL API exposes a schema that defines data types (objects) and operations (queries and mutations). This strong type system ensures predictable responses, simplifies error handling, and requires clients to explicitly specify which fields to return.
Single endpoint. All requests are processed through a unified endpoint, providing a consistent interface for both data retrieval and modification.
A GraphQL schema defines two primary categories of data types: scalars and objects. Scalars represent atomic values such as Int, Float, String, Boolean, and ID. Objects, on the other hand, are user-defined entities composed of multiple fields, which may themselves be scalars, objects, or lists of other types. This nested composition creates a rich graph structure that captures relationships among entities and allows clients to traverse and query linked data seamlessly.
Clients interact with GraphQL APIs through two main operation types:
- 
⋄\diamond

Queries retrieve data from the server, functioning similarly to HTTP GET requests in REST APIs. A special form, the introspection query, allows clients to inspect the schema and obtain metadata about available types and operations.


- 
⋄\diamond

Mutations modify data on the server, corresponding to creation, update, or deletion actions.


Queries retrieve data from the server, functioning similarly to HTTP GET requests in REST APIs. A special form, the introspection query, allows clients to inspect the schema and obtain metadata about available types and operations.
Mutations modify data on the server, corresponding to creation, update, or deletion actions.
Both queries and mutations enable fine-grained field selection, ensuring clients request exactly the data they need. Each field may also take arguments, allowing deeply nested and parameterized requests. A GraphQL operation is first parsed and validated against the schema, then executed by resolving each field independently. This layered execution model, together with features like schema introspection, makes GraphQL powerful but also complex to test securely.

GraphQL provides powerful ways to query and manage data, but its flexibility also brings new types of security risks. Some of these problems are similar to common web application issues, such as broken access control, injection flaws, and misconfigurations, while others are specific to how GraphQL is designed. These GraphQL-specific issues expand the attack surface and need special attention. We group them into three main categories:
- 
⋄\diamond

Query Abuse Vulnerabilities. Because GraphQL allows users to send highly flexible queries, attackers can take advantage of this feature to overload or explore the system. A common example is misuse of the introspection query, which reveals the entire schema, including all types, fields, and relationships. This information helps attackers craft more targeted and harmful queries. GraphQL is also exposed to Denial of Service (DoS) attacks caused by deeply nested or repetitive queries that consume large amounts of server resources, leading to slowdowns or outages.


- 
⋄\diamond

Injection Vulnerabilities. GraphQL inputs can be an entry point for injection attacks if they are not properly checked or sanitized. The most serious case is SQL Injection, where unsafe user inputs are added to database queries, allowing data theft or manipulation. Other examples include Path Injection and Cross-Site Scripting (XSS). These can result in stolen sessions, leaked data, or malicious code running in the browser. Weak input handling in GraphQL therefore puts both the backend and users at risk.


- 
⋄\diamond

Access Control Vulnerabilities. Access control problems occur when a GraphQL API fails to properly restrict what data users can access. A typical example is Insecure Direct Object Reference (IDOR), where attackers change object identifiers to view or modify restricted data. Another example is batched attacks, where multiple operations are combined in one request to bypass individual security checks. Fixing such issues is difficult because GraphQL schemas often include many linked fields and relationships. Testing for these problems requires context-aware and dependency-based approaches that can understand how queries, mutations, and objects interact, helping to uncover access control flaws that traditional testing might miss.


Query Abuse Vulnerabilities. Because GraphQL allows users to send highly flexible queries, attackers can take advantage of this feature to overload or explore the system. A common example is misuse of the introspection query, which reveals the entire schema, including all types, fields, and relationships. This information helps attackers craft more targeted and harmful queries. GraphQL is also exposed to Denial of Service (DoS) attacks caused by deeply nested or repetitive queries that consume large amounts of server resources, leading to slowdowns or outages.
Injection Vulnerabilities. GraphQL inputs can be an entry point for injection attacks if they are not properly checked or sanitized. The most serious case is SQL Injection, where unsafe user inputs are added to database queries, allowing data theft or manipulation. Other examples include Path Injection and Cross-Site Scripting (XSS). These can result in stolen sessions, leaked data, or malicious code running in the browser. Weak input handling in GraphQL therefore puts both the backend and users at risk.
Access Control Vulnerabilities. Access control problems occur when a GraphQL API fails to properly restrict what data users can access. A typical example is Insecure Direct Object Reference (IDOR), where attackers change object identifiers to view or modify restricted data. Another example is batched attacks, where multiple operations are combined in one request to bypass individual security checks. Fixing such issues is difficult because GraphQL schemas often include many linked fields and relationships. Testing for these problems requires context-aware and dependency-based approaches that can understand how queries, mutations, and objects interact, helping to uncover access control flaws that traditional testing might miss.

GraphQL Security Testing. Security testing for GraphQL has evolved from basic black-box approaches to more sophisticated schema-aware methods. Early community tools such as GraphQL-Cop ([graphqlcop,](https://arxiv.org/html/2510.10407v1#bib.bib26)), GraphCrawler ([graphcrawler,](https://arxiv.org/html/2510.10407v1#bib.bib31)), CrackQL ([crackql,](https://arxiv.org/html/2510.10407v1#bib.bib24)), and Schemathesis ([hatfield_dodds_2021_schemathesis,](https://arxiv.org/html/2510.10407v1#bib.bib32)) rely on introspection to generate single-request mutations but lack systematic reasoning about dependencies between queries and mutations. EvoMaster extends evolutionary and random testing to GraphQL APIs, supporting both black-box and white-box modes to broaden coverage ([belhadi2023evomaster,](https://arxiv.org/html/2510.10407v1#bib.bib18); [arcuri2021evomaster,](https://arxiv.org/html/2510.10407v1#bib.bib17)). Industry-standard scanners such as OWASP ZAP ([zap2024,](https://arxiv.org/html/2510.10407v1#bib.bib14)) and BurpSuite ([burpsuite,](https://arxiv.org/html/2510.10407v1#bib.bib1)) include GraphQL modules (e.g., Burp’s Auto GQL Scanner) but primarily perform generic payload fuzzing and introspection-based attacks rather than exploring multi-step workflows. GraphQLer ([graphqler2025,](https://arxiv.org/html/2510.10407v1#bib.bib50)) introduced the first context-aware GraphQL security testing framework. It analyzes the schema to infer producer–consumer dependencies among queries and mutations, constructs a dependency graph, and generates realistic chained payloads. This approach improves schema coverage and discovers previously unknown vulnerabilities compared with earlier fuzzers, motivating the need for dependency reasoning in GraphQL security testing.
LLM-Assisted Fuzzing. In dynamic analysis, fuzzing remains one of the most effective ways to automatically find software bugs. Coverage-guided fuzzers such as AFL++ ([aflplusplus2020,](https://arxiv.org/html/2510.10407v1#bib.bib28)) and libFuzzer ([libfuzzer,](https://arxiv.org/html/2510.10407v1#bib.bib42)), along with large-scale efforts like OSS-Fuzz ([ossfuzz,](https://arxiv.org/html/2510.10407v1#bib.bib30)), have discovered thousands of vulnerabilities. However, these approaches often struggle with highly structured or constrained inputs and with reaching deep execution paths. To address these challenges, recent work combines LLMs with fuzzing and related dynamic techniques. Fuzz4All ([xia2023fuzz4all,](https://arxiv.org/html/2510.10407v1#bib.bib51)) uses LLMs for input generation and mutation across multiple formats, maintaining diversity through an autoprompting loop and achieving higher coverage than traditional fuzzers. ELFuzz ([chen2025elfuzz,](https://arxiv.org/html/2510.10407v1#bib.bib21)) enhances generation-based fuzzers through LLM-driven synthesis over input spaces, achieving higher coverage and revealing real-world bugs. Recent studies have explored machine learning–based detection of malicious GraphQL queries. For instance, one line of work applies deep reinforcement learning to identify denial-of-service patterns in GraphQL APIs ([ieee10579536,](https://arxiv.org/html/2510.10407v1#bib.bib44)), while another investigates the use of large language models, sentence transformers, and convolutional neural networks for malicious query detection ([perera2025enhancing,](https://arxiv.org/html/2510.10407v1#bib.bib47)). There has also been work to use LLMs in text-to-GraphQL queries ([graphqlquerygenerationkesarwani,](https://arxiv.org/html/2510.10407v1#bib.bib39)); however, the model does not target specific API schemas. To the best of our knowledge, no prior work has applied LLM-assisted fuzzing to GraphQL, whose schema-rich, multi-operation design introduces unique challenges. PrediQL is the first to address this gap by leveraging LLM reasoning to guide test generation and vulnerability detection in GraphQL APIs.

PrediQL is a modular LLM-driven GraphQL fuzzing framework organized around a closed-loop pipeline (Figure 1). At its core, PrediQL integrates an LLM-based query generator with schema introspection, semantic retrieval, adaptive arm selection, and self-correction modules. This architecture constrains the model’s generation space, maintaining validity and fuzzing relevance while adapting to feedback dynamically. The key contribution lies in coupling schema-aware reasoning with adaptive prompting to produce valid, diverse, and feedback-driven queries.
Rather than relying on static mutation operators, PrediQL refines prompts with schema fragments, retrieved traces, and error signals, making each generation guided by prior results and schema insights. The system runs as a closed-loop cycle: schema modeling constrains the search space, the bandit-based selector chooses a prompting strategy, retrieval grounds prompts in real execution history, and self-correction incorporates prior errors. Prompt construction then assembles these elements into an evidence-gated LLM input; executed queries update the schema, memory, and bandit posteriors, completing the loop and allowing iterative refinement of validity, diversity, and coverage.

The PrediQL pipeline begins with a standard GraphQL introspection query against the target API. Introspection reveals the complete schema, which includes queries, mutations, input parameters, and return types. PrediQL parses this output into a structured intermediate representation that organizes operations, argument specifications, and object definitions. To facilitate reuse and downstream automation, the schema is serialized into lightweight YAML files, separating queries, mutations, and type definitions. This schema map provides a blueprint of the API before any fuzzing or query generation takes place.
Unlike prior tools that treat introspection results as flat listings, PrediQL recursively follows links between objects to capture nested and cross-referenced types. This yields a graph-structured view of responses, enabling the system to reason about both top-level operations and the shape of deeply nested return values. Maintaining this normalized schema representation allows PrediQL to generate queries that are syntactically valid, semantically consistent, and structurally diverse, while avoiding common issues such as type mismatches or missing arguments.

Adaptive Arm Selection. Query generation is framed as a multi-armed bandit problem ([lattimore2020bandit,](https://arxiv.org/html/2510.10407v1#bib.bib40)), where each arm represents a distinct prompting strategy defined by four key parameters. The Schema parameter determines whether the full GraphQL schema is included in the LLM prompt to guide query construction. The Arg Mode parameter controls how arguments are generated: known reuses previously successful parameter values from the RAG context, real synthesizes realistic type-appropriate literals, and nulls tests optional fields with null values. The Depth parameter limits the nesting level of GraphQL selections to balance complexity and validity, while the top-k parameter specifies how many similar examples from the RAG system are retrieved as contextual grounding (see Section [4.1](https://arxiv.org/html/2510.10407v1#S4.SS1) for configuration details).
Since the effectiveness of each strategy depends on the endpoint’s evolving behavior, the bandit formulation enables PrediQL to dynamically allocate preference toward high-performing arms while still exploring alternatives. To balance exploration and exploitation, PrediQL employs Thompson Sampling ([agrawal2011ts,](https://arxiv.org/html/2510.10407v1#bib.bib15)), rewarding arms only when generated queries both (i) return HTTP 200 responses and (ii) expand coverage. To account for non-stationary environments, rewards are exponentially discounted so that outdated strategies are gradually down-weighted. This adaptive mechanism prevents over-commitment to a single strategy while progressively amplifying those that yield meaningful coverage.
Retrieval-Augmented Generation. To mitigate the problem of hallucinated or invalid query values, PrediQL integrates retrieval-augmented generation (RAG) ([lewis2020rag,](https://arxiv.org/html/2510.10407v1#bib.bib41)). All prior queries and responses are embedded into a FAISS index ([douze2024faiss,](https://arxiv.org/html/2510.10407v1#bib.bib23)). During generation, PrediQL retrieves the top-kk (where kk is equal to 0, 3, or 5, depending on the selected ARM) most semantically relevant traces and injects them into the prompt.
This retrieval memory grounds the LLM in real execution history, improving syntactic fidelity, reducing repetition, and promoting diversity by surfacing alternative query structures.
Prompt Engineering. Prompt design is key to guiding query generation. PrediQL adopts four design goals: prompts must be evidence-gated, deterministic, schema-constrained, and context-aware. At runtime, prompt PP is automatically assembled from five modular components: P=[B​‖S‖​R​‖E‖​D]P=[B\,\|\,S\,\|\,R\,\|\,E\,\|\,D]:
- 
⊳\triangleright

BB: Basic restricting header (evidence-gating).


- 
⊳\triangleright

SS: Schema fragments from introspection


- 
⊳\triangleright

RR: Retrieved execution examples (RAG)


- 
⊳\triangleright

EE: Prior error–query pairs (self-correction)


- 
⊳\triangleright

DD: Strategy-specific directives (bandit arm)


BB: Basic restricting header (evidence-gating).
SS: Schema fragments from introspection
RR: Retrieved execution examples (RAG)
EE: Prior error–query pairs (self-correction)
DD: Strategy-specific directives (bandit arm)
This modular structure ensures that exploration happens primarily through DD (arm choice), while SS, RR, and EE stabilize performance across strategies.
[userwallet_api,](https://arxiv.org/html/2510.10407v1#bib.bib13)
[countries_api,](https://arxiv.org/html/2510.10407v1#bib.bib2)
[rickmorty_api,](https://arxiv.org/html/2510.10407v1#bib.bib11)
[graphqlzero_api,](https://arxiv.org/html/2510.10407v1#bib.bib9)
[ehri_api,](https://arxiv.org/html/2510.10407v1#bib.bib4)
[tcgdex_api,](https://arxiv.org/html/2510.10407v1#bib.bib12)

### 3.3. Execution and Feedback
Self Correction. Failed queries are not discarded. Instead, PrediQL explicitly records schema errors and associates them with the queries that caused them. In subsequent generations, these error–query pairs are injected into the prompt as corrective signals.
This error-guided refinement turns schema violations into supervision, steering the model away from repeated mistakes and accelerating convergence toward valid, schema-compliant queries.
Context-Aware Vulnerability Detection. To assess security impact, PrediQL uses an LLM to analyze responses in context, rather than relying on predefined signatures or static rules. Each response, together with its execution metadata such as status codes and error messages, is transformed into a structured analysis prompt that directs the LLM to identify evidence of vulnerabilities, including injection flaws, access-control bypasses, and information disclosure. The resulting analyses are parsed into JSON records encoding vulnerability type, severity, confidence, and evidence. These records are stored and aggregated, yielding both granular findings and system-level trends. By conditioning on schema knowledge and execution context, PrediQL generalizes across diverse GraphQL APIs and uncovers subtle, context-dependent flaws that rule-based detectors overlook.

### 3.4. Closed-Loop Integration
Together, these phases form a closed-loop fuzzing cycle in which schema knowledge constrains the LLM, adaptive generation explores diverse query strategies, and execution feedback continuously refines both prompts and strategy selection. This iterative design enables PrediQL to expand coverage systematically while maintaining robustness and precision in vulnerability discovery.

We implement the design and experiments in an open-source repository***https://github.com/SLL288/prediql. Our experiment is structured to investigate the following research questions: RQ1. How can LLMs be guided to synthesize valid yet adversarial GraphQL queries that systematically expand schema coverage compared to schema-only or random fuzzing approaches? RQ2. How does prompt engineering and context enrichment contribute to improving schema coverage? RQ3. To what extent can this pipeline discover meaningful GraphQL vulnerabilities over existing rule-based methods?

API Selection. In our experimental evaluation, we employed a diverse spectrum of APIs, including open-source and openly hosted options. For open-source APIs, we obtained the backend code, established a self-hosted GraphQL server, and conducted tests. For openly hosted APIs, we utilized free-to-use reference APIs accessible on GitHub and conducted direct testing. The selected APIs are shown in Table [1](https://arxiv.org/html/2510.10407v1#S3.T1).
Baselines. We evaluate PrediQL against four representative baselines that include both general-purpose and GraphQL-specific testing frameworks.
- 
⋄\diamond

EvoMaster. The only prior academic framework supporting GraphQL testing in both white-box and black-box modes. We use its black-box configuration for fair comparison. EvoMaster generates and sends GraphQL queries and mutations automatically, but employs evolutionary heuristics to mutate payloads dynamically and explore a wider response space ([belhadi2023evomaster,](https://arxiv.org/html/2510.10407v1#bib.bib18); [arcuri2021evomaster,](https://arxiv.org/html/2510.10407v1#bib.bib17); [belhadi2023graphql,](https://arxiv.org/html/2510.10407v1#bib.bib19)).


- 
⋄\diamond

ZAP. An open source black-box vulnerability scanner maintained by the Open Web Application Security Project (OWASP) ([zap2024,](https://arxiv.org/html/2510.10407v1#bib.bib14)). Although originally designed for traditional web applications, it includes a module for GraphQL testing that performs introspection-based payload generation and common attack simulations.


- 
⋄\diamond

BurpSuite. A widely used commercial web security platform developed by PortSwigger ([burpsuite,](https://arxiv.org/html/2510.10407v1#bib.bib1)). For GraphQL testing, we enable the Auto GQL Scanner extension ([burpsuite_scanner,](https://arxiv.org/html/2510.10407v1#bib.bib29)), which automatically identifies GraphQL endpoints and injects predefined payloads to detect vulnerabilities such as injection and schema disclosure.


- 
⋄\diamond

GraphQLer. A recent context-aware GraphQL security testing framework ([graphqler2025,](https://arxiv.org/html/2510.10407v1#bib.bib50)). It constructs a dependency graph that captures producer–consumer relationships between queries and mutations, allowing the generation of realistic chained requests. GraphQLer demonstrates the benefit of dependency reasoning for GraphQL security testing and serves as the strongest baseline in our comparison.


EvoMaster. The only prior academic framework supporting GraphQL testing in both white-box and black-box modes. We use its black-box configuration for fair comparison. EvoMaster generates and sends GraphQL queries and mutations automatically, but employs evolutionary heuristics to mutate payloads dynamically and explore a wider response space ([belhadi2023evomaster,](https://arxiv.org/html/2510.10407v1#bib.bib18); [arcuri2021evomaster,](https://arxiv.org/html/2510.10407v1#bib.bib17); [belhadi2023graphql,](https://arxiv.org/html/2510.10407v1#bib.bib19)).
ZAP. An open source black-box vulnerability scanner maintained by the Open Web Application Security Project (OWASP) ([zap2024,](https://arxiv.org/html/2510.10407v1#bib.bib14)). Although originally designed for traditional web applications, it includes a module for GraphQL testing that performs introspection-based payload generation and common attack simulations.
BurpSuite. A widely used commercial web security platform developed by PortSwigger ([burpsuite,](https://arxiv.org/html/2510.10407v1#bib.bib1)). For GraphQL testing, we enable the Auto GQL Scanner extension ([burpsuite_scanner,](https://arxiv.org/html/2510.10407v1#bib.bib29)), which automatically identifies GraphQL endpoints and injects predefined payloads to detect vulnerabilities such as injection and schema disclosure.
GraphQLer. A recent context-aware GraphQL security testing framework ([graphqler2025,](https://arxiv.org/html/2510.10407v1#bib.bib50)). It constructs a dependency graph that captures producer–consumer relationships between queries and mutations, allowing the generation of realistic chained requests. GraphQLer demonstrates the benefit of dependency reasoning for GraphQL security testing and serves as the strongest baseline in our comparison.

### 4.1. Experimental Setup
Model Selection. For evaluation, we selected four LLMs spanning different developers, sizes, and design philosophies, as summarized in Table [2](https://arxiv.org/html/2510.10407v1#S3.T2). Specifically, we included LLaMA 3.1 from Meta ([meta_llama_3_1_8b,](https://arxiv.org/html/2510.10407v1#bib.bib10)) as a representative open source model, Gemini 2.5 from Google DeepMind ([deepmind_gemini_2_5_flash,](https://arxiv.org/html/2510.10407v1#bib.bib5)) as a lightweight and optimized variant of the Gemini family, GPT-5 Mini from OpenAI ([gpt5_mini_comparison,](https://arxiv.org/html/2510.10407v1#bib.bib6)) as a smaller yet efficient version of the GPT-5 series, and DeepSeek R1 from DeepSeek AI ([deepseek_r1_comparison,](https://arxiv.org/html/2510.10407v1#bib.bib3)), an open source model that emphasizes reasoning and efficiency. This diverse selection allows us to cover both open source and proprietary approaches, models optimized for speed as well as those focused on reasoning capabilities.
Bandit Configuration Details. For experimental evaluation, we instantiated eight distinct bandit arms, each representing a specific prompting strategy defined by four parameters: Schema, Arg Mode, Depth, and Top-k. Table [3](https://arxiv.org/html/2510.10407v1#S4.T3) summarizes these configurations.
Each configuration corresponds to a balance between reliability and exploration. Conservative arms (e.g., schema_min_known) prioritize syntactic validity by reusing known parameter values and shallow nesting. Aggressive arms (e.g., schema_deep_real) promote deeper traversal and the synthesis of new argument values. The non-schema variants probe the LLM’s ability to generalize without explicit schema guidance. The bandit dynamically reallocates probability mass toward arms that maximize successful, coverage-expanding executions.
Evaluation Metric. To address RQ1 and RQ2, we define the following coverage metric to evaluate GraphQL API testing:
where coverage is the fraction of schema nodes that return valid, error-free data rather than just an HTTP 200 status. This metric reflects how much of the GraphQL schema is actually exercised by successful queries, providing a more accurate view of the API’s reliability and robustness.

### 4.2. Schema Coverage (RQ1)
Table [4](https://arxiv.org/html/2510.10407v1#S4.T4.fig1) compares the API coverage achieved by PrediQL against four baseline tools: ZAP, BurpSuite, EvoMaster, and GraphQLer. Across all evaluated APIs, PrediQL consistently attains the highest or near-highest coverage, demonstrating its ability to exercise a larger portion of the GraphQL schema through valid, data-returning queries. Traditional black-box scanners such as ZAP and BurpSuite achieve limited coverage because they lack awareness of GraphQL’s hierarchical structure and query dependencies. EvoMaster performs better by generating dynamic requests, but still falls short on complex schemas. GraphQLer improves coverage by incorporating schema context, yet PrediQL surpasses it in nearly all cases by integrating retrieval-augmented reasoning and adaptive query generation. Note that the reported PrediQL results correspond to its configuration with the best-performing LLM.
Table [5](https://arxiv.org/html/2510.10407v1#S4.T5.fig1) presents the performance of tested large language models across different GraphQL APIs. Overall, all models achieve high coverage on simpler or well-structured APIs such as Countries, Rick & Morty, GraphQLZero, and TCGDex, indicating that these schemas are easier to navigate and query successfully. However, differences emerge on more complex or noisy schemas such as UserWallet and EHRI. GPT-5 Mini and Gemini 2.5 consistently produce the most stable and complete results, suggesting stronger schema understanding and query adaptation capabilities. LLaMA 3.1 performs comparably but occasionally misses certain paths. In contrast, DeepSeek R1 positions itself as the second-most proficient model on specific APIs, closely following GPT-5 Mini. These findings suggest that stronger reasoning models maintain high coverage under schema complexity, indicating better adaptability and understanding of GraphQL structures.

Prompt engineering is central to steering the reasoning capabilities of LLMs in improving schema coverage and discovering vulnerabilities in APIs. To address RQ2, we conduct an ablation study that isolates the contribution of each prompt enrichment component. This analysis quantifies how each module influences schema coverage and overall testing effectiveness. The corresponding configurations are detailed below.
- 
⋄\diamond

PrediQL-BASE. The baseline configuration provides only the minimal schema context and expected response format. It guides the model to produce syntactically valid GraphQL queries.


- 
⋄\diamond

PrediQL-AQG. Building on the baseline, the adaptive query generation configuration integrates both multi-armed bandit selection and retrieval-augmented generation, which is essential for known values ARM setting to enable adaptive and context-aware query synthesis.


- 
⋄\diamond

PrediQL-SCL. The self-correction feedback loop configuration enhances the baseline prompt, adding an error-aware refinement cycle. Failed or invalid queries are logged with their corresponding error messages and reinjected into subsequent prompts as a corrective context.


- 
⋄\diamond

PrediQL. The full pipeline, combining adaptive query generation, retrieval augmentation, and self-correction into a single closed-loop system.


PrediQL-BASE. The baseline configuration provides only the minimal schema context and expected response format. It guides the model to produce syntactically valid GraphQL queries.
PrediQL-AQG. Building on the baseline, the adaptive query generation configuration integrates both multi-armed bandit selection and retrieval-augmented generation, which is essential for known values ARM setting to enable adaptive and context-aware query synthesis.
PrediQL-SCL. The self-correction feedback loop configuration enhances the baseline prompt, adding an error-aware refinement cycle. Failed or invalid queries are logged with their corresponding error messages and reinjected into subsequent prompts as a corrective context.
PrediQL. The full pipeline, combining adaptive query generation, retrieval augmentation, and self-correction into a single closed-loop system.
Table [6](https://arxiv.org/html/2510.10407v1#S4.T6) evaluates the contribution of individual prompt engineering components: the base prompt (BASE), the self-correction loop (PrediQL-SCL), and adaptive query generation (PrediQL-AQG). Contributions are computed for models that experienced enhancements from PrediQL-Base to PrediQL. Across models and APIs, the incremental addition of these modules consistently improves schema coverage, confirming that each contributes complementary benefits. PrediQL-BASE alone often yields limited coverage, particularly in complex schemas such as UserWallet and EHRI, where naive prompting fails to satisfy nested or dependent field constraints. Introducing the self-correction loop (PrediQL-SCL) markedly reduces repeated schema violations, increasing coverage by 10–25% depending on the model capacity. Adaptive query generation (PrediQL-AQG) provides an additional boost to APIs that require realistic parameter inference, increasing coverage by as much as 26% on EHRI and 15% on GraphQLZero for Gemini 2.5. When both mechanisms are combined in PrediQL, coverage approaches or reaches 100% in almost all APIs and models.
Smaller open-source models such as LLaMA 3.1 follow the same pattern but exhibit slightly higher variance, reflecting reduced stability in long-context reasoning. Larger models (GPT-5 Mini, DeepSeek R1) demonstrate less sensitivity to prompt enrichment, suggesting that reasoning-oriented architectures benefit more from the feedback of retrieval and correction than from raw scale alone. In general, ablation confirms that the design gains of PrediQLstem from the synergy of retrieval grounding, adaptive prompting, and iterative self-correction, rather than from model size alone.

Table [7](https://arxiv.org/html/2510.10407v1#S4.T7) summarizes the vulnerability detection results across GraphQLer and the different configurations of PrediQL. Among existing GraphQL testing tools, only GraphQLer includes a built-in vulnerability detection module, while others, such as EvoMaster and ZAP, primarily focus on coverage measurement or payload fuzzing. Therefore, GraphQLer serves as the most relevant baseline for assessing the detection capacity.
Across all evaluated APIs, PrediQL consistently identifies a greater number and a wider range of vulnerabilities. While GraphQLer mainly exposes schema-level and input validation flaws, PrediQL leverages retrieval-augmented reasoning and adaptive arm selection to detect deeper logic- and context-dependent weaknesses such as HTML injection, SSRF, and OS command injection. The variants PrediQL -Gemini and PrediQL -GPT-5 achieve the highest detection counts, improving unique findings by 20-40% on complex benchmarks such as UserWallet and GraphQLZero. In general, these results confirm that LLM-guided reasoning substantially enhances vulnerability discovery beyond static or heuristic testing baselines.
Qualitative analysis shows that PrediQL detects a broader spectrum of vulnerability categories compared to GraphQLer, including deeper logic and context-dependent flaws. Its reasoning traces link each issue to its execution context (e.g., leaked variables or inconsistent authorization responses), enabling precise, evidence-based triaging.

Our evaluation demonstrates that PrediQL consistently outperforms all existing GraphQL testing frameworks. This section discusses key observations, broader implications, and open research directions.
Impact of Model Size. Larger models such as GPT-5 Mini and DeepSeek R1 achieved higher semantic coherence and reasoning stability, while smaller open-source models (e.g., LLaMA 3.1) remained competitive at a fraction of the computational cost. This highlights a practical trade-off between reasoning depth and efficiency. When equipped with retrieval memory and adaptive prompting, lightweight models can approximate the performance of proprietary ones. A promising direction is to adopt hybrid configurations, using larger models for seed generation and schema understanding, followed by smaller models for iterative fuzzing, to balance throughput, coverage, and cost.
Implications Beyond GraphQL. The introduced mechanisms in PrediQL, adaptive arm selection, self-corrective prompting, and retrieval-grounded reasoning, are not specific to GraphQL. These ideas extend naturally to other structured interface testing domains such as REST, gRPC, and JSON-RPC ([jsonrpc_specification,](https://arxiv.org/html/2510.10407v1#bib.bib38)). More broadly, PrediQL demonstrates that retrieval-augmented reasoning and bandit-driven exploration can complement traditional coverage-guided and evolutionary fuzzing. Integrating symbolic reasoning or static program analysis into such adaptive loops may bridge the gap between semantic understanding and execution-level precision, enabling more generalizable automated security testing frameworks.
Limitations. While effective, PrediQL is not without constraints:
- 
⊳\triangleright

Execution cost and rate limits. LLM-guided fuzzing remains computationally intensive, and API rate throttling can slow feedback cycles.


- 
⊳\triangleright

Context window constraints. Even with retrieval augmentation, large schemas can exceed model context limits, leading to partial prompt conditioning and missed relationships.


- 
⊳\triangleright

Response interpretation ambiguity. The context-aware detector can identify likely vulnerabilities, but some cases still require human validation to confirm exploitability.


- 
⊳\triangleright

Model bias and non-determinism. Variations in model architecture and decoding strategies lead to inconsistent results, motivating ensemble or calibration techniques for reproducibility.


Execution cost and rate limits. LLM-guided fuzzing remains computationally intensive, and API rate throttling can slow feedback cycles.
Context window constraints. Even with retrieval augmentation, large schemas can exceed model context limits, leading to partial prompt conditioning and missed relationships.
Response interpretation ambiguity. The context-aware detector can identify likely vulnerabilities, but some cases still require human validation to confirm exploitability.
Model bias and non-determinism. Variations in model architecture and decoding strategies lead to inconsistent results, motivating ensemble or calibration techniques for reproducibility.
Future Work. The growing ecosystem of agentic LLM frameworks offers a natural evolution path for PrediQL. A multi-agent design, with specialized agents for query generation, evaluation, and refinement, could enable continuous self-improvement and deeper exploit discovery. Another direction is the development of domain-specialized LLMs for API and schema reasoning, analogous to text-to-SQL models, which could reduce prompt overhead while improving precision and generalization. Finally, exploring hybrid systems that couple LLM reasoning with program analysis or formal verification could enable both semantic adaptability and provable assurance.

PrediQL shows that the combination of retrieval, reasoning, and adaptive learning can fundamentally improve the way GraphQL APIs are tested. By integrating large language models into the fuzzing loop, it transforms random exploration into guided reasoning, allowing the system to understand schemas, infer dependencies, and generate purposeful queries. Through multi-armed bandit strategy selection, PrediQL learns which testing behaviors yield the most valuable feedback, achieving higher coverage and uncovering vulnerabilities that existing tools consistently miss. Beyond its empirical gains, PrediQL reveals a deeper insight: LLMs can act not only as generators but as analysts that interpret system behavior. This ability to connect input, responses, and context enables the detection of complex logic-level flaws that evade rule-based or pattern-driven scanners. These results mark a step towards autonomous, self-improving security testing, where models learn from every execution to test smarter over time. Future extensions will explore collaborative, multi-agent setups and large-scale retrieval across heterogeneous APIs, paving the way for intelligent systems that continuously learn the structure and weaknesses of modern Web applications.

- 
(1)

Burp suite.


[https://portswigger.net/burp](https://portswigger.net/burp).


Accessed: 2025-10-03.



- 
(2)

Countries graphql api.


[https://countries.trevorblades.com/](https://countries.trevorblades.com/).


Accessed: October 2025.



- 
(3)

Deepseek r1 vs gpt-5 mini (model comparison).


[https://aimodels.fyi/compare/deepseek-r1-vs-gpt-5-mini](https://aimodels.fyi/compare/deepseek-r1-vs-gpt-5-mini).


Accessed 2025-10-07.



- 
(4)

European holocaust research infrastructure (ehri) graphql api.


[https://portal.ehri-project.eu/api/graphql](https://portal.ehri-project.eu/api/graphql).


Accessed: October 2025.



- 
(5)

Gemini 2.5 flash model.


[https://deepmind.google/models/gemini/flash/](https://deepmind.google/models/gemini/flash/).


Accessed 2025-10-07.



- 
(6)

Gpt-5 mini vs gemini 2.5 flash (model comparison).


[https://artificialanalysis.ai/models/comparisons/gpt-5-mini-vs-gemini-2-5-flash](https://artificialanalysis.ai/models/comparisons/gpt-5-mini-vs-gemini-2-5-flash).


Accessed 2025-10-07.



- 
(7)

Graphql security (official guide).


[https://graphql.org/learn/security/](https://graphql.org/learn/security/).


Accessed 2025-10-04.



- 
(8)

Graphql vs REST api — difference between api design styles.


[https://aws.amazon.com/compare/the-difference-between-graphql-and-rest/](https://aws.amazon.com/compare/the-difference-between-graphql-and-rest/).


Accessed 2025-10-04.



- 
(9)

Graphqlzero api.


[https://graphqlzero.almansi.me/](https://graphqlzero.almansi.me/).


Accessed: October 2025.



- 
(10)

Meta llama 3.1 8b.


[https://huggingface.co/meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B).


Accessed 2025-10-07.



- 
(11)

Rick and morty graphql api.


[https://rickandmortyapi.com/graphql](https://rickandmortyapi.com/graphql).


Accessed: October 2025.



- 
(12)

Tcgdex graphql api.


[https://api.tcgdex.net/v2/graphql](https://api.tcgdex.net/v2/graphql).


Accessed: October 2025.



- 
(13)

Userwallet graphql api.


[https://github.com/graphql-compose/graphql-compose-examples/tree/master/examples/user-wallet](https://github.com/graphql-compose/graphql-compose-examples/tree/master/examples/user-wallet).


Accessed: October 2025.



- 
(14)

Owasp zed attack proxy (zap).


[https://www.zaproxy.org/](https://www.zaproxy.org/), 2024.



- 
(15)

Agrawal, S., and Goyal, N.

Analysis of thompson sampling for the multi-armed bandit problem.


arXiv preprint arXiv:1111.1797 (2011).



- 
(16)

Andersson, T.

Rest api vs graphql — a literature and experimental study.


[https://www.diva-portal.org/smash/get/diva2:1571154/FULLTEXT01.pdf](https://www.diva-portal.org/smash/get/diva2:1571154/FULLTEXT01.pdf), 2021.



- 
(17)

Arcuri, A., Galeotti, J. P., Marculescu, B., and Zhang, M.

Evomaster: A search-based system test generation tool.


Journal of Open Source Software 6, 57 (2021), 2153.



- 
(18)

Belhadi, A., Zhang, M., and Arcuri, A.

Random testing and evolutionary testing for fuzzing graphql apis.


ACM Transactions on the Web (2023).



- 
(19)

Belhadi, Y., and Arcuri, A.

Evomaster for GraphQL: Black-box test generation for web APIs.


In Proceedings of the 38th IEEE/ACM International Conference on Automated Software Engineering (ASE) (2023), IEEE, pp. 1503–1507.



- 
(20)

Cavenaghi, E., et al.

Non-stationary multi-armed bandit: Empirical evaluation of f-discounted-sliding-window thompson sampling.


Entropy 23, 3 (2021), 380.



- 
(21)

Chen, C., Dolan-Gavitt, B., and Lin, Z.

Elfuzz: Efficient input generation via llm-driven synthesis over fuzzer space.


In Proceedings of the 34th USENIX Security Symposium (2025), USENIX Association.


to appear.



- 
(22)

Deng, Y., Xia, C. S., Peng, H., Yang, C., and Zhang, L.

Large language models are zero-shot fuzzers: Fuzzing deep-learning libraries via large language models.


arXiv preprint arXiv:2212.14834 (2022).



- 
(23)

Douze, M., Guzhva, A., Deng, C., Johnson, J., Szilvasy, G., Mazaré, P.-E., Lomeli, M., Hosseini, L., and Jégou, H.

The faiss library.



- 
(24)

Doyensec.


Crackql: Graphql security testing tool.


[https://github.com/doyensec/CrackQL](https://github.com/doyensec/CrackQL), 2021.


Accessed: 2025-10-04.



- 
(25)

Escape.


The state of graphql security 2024.


Tech. rep., Escape Technologies, 2024.


Accessed: October 2025.



- 
(26)

Escape Technologies.


Graphql-cop: Security scanner for graphql apis.

[https://github.com/escape-technologies/graphql-cop](https://github.com/escape-technologies/graphql-cop), 2023.


Accessed: 2025-10-04.



- 
(27)

Fastly.


Exploring the security implications of GraphQL.


[https://www.fastly.com/blog/exploring-the-security-implications-of-graphql](https://www.fastly.com/blog/exploring-the-security-implications-of-graphql), 2022.



- 
(28)

Fioraldi, A., Maier, D., Eißfeldt, H., and Heuse, M.

Afl++: Combining incremental steps of fuzzing research.


In 14th USENIX Workshop on Offensive Technologies (WOOT 20) (2020).



- 
(29)

Forward Security.


Autogql: Auto GraphQL scanner for burp suite.


[https://github.com/FWDSEC/burp-auto-gql](https://github.com/FWDSEC/burp-auto-gql), 2023.


Accessed: 2025-10-07.



- 
(30)

Google.


Oss-fuzz – continuous fuzzing for open source software.


[https://github.com/google/oss-fuzz](https://github.com/google/oss-fuzz), 2024.


Accessed: 2025-10-04.



- 
(31)

GraphCrawler Project.


Graphcrawler: Automated graphql introspection and fuzzing tool.


[https://github.com/gsmith257-cyber/GraphCrawler](https://github.com/gsmith257-cyber/GraphCrawler), 2022.


Accessed: 2025-10-04.



- 
(32)

Hatfield-Dodds, Z., et al.

Deriving semantics-aware fuzzers from web API schemas, 2021.



- 
(33)

Huang, L., Zhao, P., Chen, H., and Ma, L.

Large language models based fuzzing techniques: A survey.


arXiv preprint arXiv:2402.00350 (2024).



- 
(34)

Hygraph.


Graphql survey 2024, 2024.


Accessed: October 2025.



- 
(35)

IBM PTC Security.


Denial of service attacks with GraphQL.


[https://medium.com/@ibm_ptc_security/denial-of-service-attacks-with-graphql-77189a6ba85b](https://medium.com/@ibm_ptc_security/denial-of-service-attacks-with-graphql-77189a6ba85b), 2023.



- 
(36)

Jin, Y., et al.

Fuzzgpt: Harnessing large language models for effective api fuzzing.


In Proceedings of the 33rd USENIX Security Symposium (2024).



- 
(37)

Johnson, J., Douze, M., and Jégou, H.

Billion-scale similarity search with GPUs.


IEEE Transactions on Big Data (2019).



- 
(38)

JSON-RPC Working Group.


Json-rpc 2.0 specification.


[https://www.jsonrpc.org/specification](https://www.jsonrpc.org/specification), 2013.


Origin date 2010-03-26, updated 2013-01-04, accessed 2025-10-07.



- 
(39)

Kesarwani, M., Ghosh, S., Gupta, N., Chakraborty, S., Sindhgatta, R., Mehta, S., Eberhardt, C., and Debrunner, D.

Graphql query generation: A large training and benchmarking dataset.


pp. 1595–1607.



- 
(40)

Lattimore, T., and Szepesvári, C.

Bandit Algorithms.


Cambridge University Press, 2020.



- 
(41)

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W.-t., Rocktäschel, T., et al.

Retrieval-augmented generation for knowledge-intensive NLP tasks.


In Advances in Neural Information Processing Systems (2020), vol. 33, pp. 9459–9474.



- 
(42)

LLVM Project.


libfuzzer – a library for coverage-guided fuzzing.


[https://llvm.org/docs/LibFuzzer.html](https://llvm.org/docs/LibFuzzer.html), 2024.


Accessed: 2025-10-04.



- 
(43)

Madaan, A., Zhou, S., Alon, U., Sonkar, S., Gupta, P., Yang, Y., and Neubig, G.

Self-refine: Iterative refinement with self-feedback.


In Advances in Neural Information Processing Systems (NeurIPS) (2023).



- 
(44)

McFadden, S., Maugeri, M., Hicks, C., Mavroudis, V., and Pierazzi, F.

Wendigo: Deep reinforcement learning for denial-of-service query discovery in graphql.


In 2024 IEEE Security and Privacy Workshops (SPW) (2024), pp. 68–75.



- 
(45)

Meng, R., Duck, G. J., and Roychoudhury, A.

Large language model assisted hybrid fuzzing.


arXiv (2024).



- 
(46)

Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C. L., Mishkin, P., Zhang, C., Agarwal, S., Slama, K., Ray, A., Schulman, J., Hilton, J., Miller, L., Simens, M., Askell, A., Welinder, P., Christiano, P., Leike, J., and Lowe, R.

Training language models to follow instructions with human feedback.


arXiv preprint arXiv:2203.02155 (2022).



- 
(47)

Perera, I., Abeyrathne, H., Malalgoda, S., and Ifthikar, A.

Enhancing graphql security by detecting malicious queries using large language models, sentence transformers, and convolutional neural networks.


arXiv preprint arXiv:2508.11711 (2025).


arXiv:2508.11711v1 [cs.CR].



- 
(48)

Reimers, N., and Gurevych, I.

Sentence-bert: Sentence embeddings using siamese bert-networks.


In Proceedings of EMNLP (2019), pp. 3982–3992.



- 
(49)

TechTarget.


What’s next for apis? 4 api trends for 2025 and beyond, 2024.


Accessed: October 2025.



- 
(50)

Tsai, Y., Zhang, T., et al.

Graphqler: Enhancing graphql security with context-aware api testing.


arXiv preprint arXiv:2504.13358 (2025).



- 
(51)

Xia, C., Wang, R., Meng, Y., Tang, Z., Wang, Y., Xue, Y., Li, X., and Chen, X.

Fuzz4all: Universal fuzzing with large language models.


In Proceedings of the 46th International Conference on Software Engineering (ICSE) (2024), ACM, pp. 1–13.



- 
(52)

Zhang, T., et al.

Dfuzz: Large language models for deep api fuzzing with white-box guidance.


In Proceedings of the 47th International Conference on Software Engineering (ICSE) (2025), IEEE/ACM.



[https://portswigger.net/burp](https://portswigger.net/burp)
[https://countries.trevorblades.com/](https://countries.trevorblades.com/)
[https://aimodels.fyi/compare/deepseek-r1-vs-gpt-5-mini](https://aimodels.fyi/compare/deepseek-r1-vs-gpt-5-mini)
[https://portal.ehri-project.eu/api/graphql](https://portal.ehri-project.eu/api/graphql)
[https://deepmind.google/models/gemini/flash/](https://deepmind.google/models/gemini/flash/)
[https://artificialanalysis.ai/models/comparisons/gpt-5-mini-vs-gemini-2-5-flash](https://artificialanalysis.ai/models/comparisons/gpt-5-mini-vs-gemini-2-5-flash)
[https://graphql.org/learn/security/](https://graphql.org/learn/security/)
[https://aws.amazon.com/compare/the-difference-between-graphql-and-rest/](https://aws.amazon.com/compare/the-difference-between-graphql-and-rest/)
[https://graphqlzero.almansi.me/](https://graphqlzero.almansi.me/)
[https://huggingface.co/meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B)
[https://rickandmortyapi.com/graphql](https://rickandmortyapi.com/graphql)
[https://api.tcgdex.net/v2/graphql](https://api.tcgdex.net/v2/graphql)
[https://github.com/graphql-compose/graphql-compose-examples/tree/master/examples/user-wallet](https://github.com/graphql-compose/graphql-compose-examples/tree/master/examples/user-wallet)
[https://www.zaproxy.org/](https://www.zaproxy.org/)
[https://www.diva-portal.org/smash/get/diva2:1571154/FULLTEXT01.pdf](https://www.diva-portal.org/smash/get/diva2:1571154/FULLTEXT01.pdf)
[https://github.com/doyensec/CrackQL](https://github.com/doyensec/CrackQL)
[https://github.com/escape-technologies/graphql-cop](https://github.com/escape-technologies/graphql-cop)
[https://www.fastly.com/blog/exploring-the-security-implications-of-graphql](https://www.fastly.com/blog/exploring-the-security-implications-of-graphql)
[https://github.com/FWDSEC/burp-auto-gql](https://github.com/FWDSEC/burp-auto-gql)
[https://github.com/google/oss-fuzz](https://github.com/google/oss-fuzz)
[https://github.com/gsmith257-cyber/GraphCrawler](https://github.com/gsmith257-cyber/GraphCrawler)
[https://medium.com/@ibm_ptc_security/denial-of-service-attacks-with-graphql-77189a6ba85b](https://medium.com/@ibm_ptc_security/denial-of-service-attacks-with-graphql-77189a6ba85b)
[https://www.jsonrpc.org/specification](https://www.jsonrpc.org/specification)
[https://llvm.org/docs/LibFuzzer.html](https://llvm.org/docs/LibFuzzer.html)
[LaTeXML](http://dlmf.nist.gov/LaTeXML/)

