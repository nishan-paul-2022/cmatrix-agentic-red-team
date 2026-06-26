# [STEP 2b] — State-of-the-Art Search

## Summary
Performed a comprehensive search for the latest research (late 2024–2025) in LLM routing and autonomous security orchestration. Identified five major new papers that represent the current state-of-the-art (SOTA). The search reveals a shift from human-in-the-loop assistants to fully autonomous multi-agent systems using standardized protocols (MCP) and learned routing strategies.

## Full Output

### 1. New SOTA Papers (2024–2025)
| Paper | Venue | Core Contribution |
|-------|-------|-------------------|
| **PentestMCP** (2025) | ResearchGate | Uses Model Context Protocol (MCP) to standardize tool orchestration; features a "Penetration Task Graph" (PTG) to prevent context loss. |
| **PentestAgent** (2024/25) | arXiv | Achieves full-stage web penetration testing with online search augmentation and automated debugging. |
| **CurriculumPT** (2025) | MDPI | Introduces "curriculum learning" for LLM agents to progressively acquire and refine complex exploitation skills without fine-tuning. |
| **WorkflowLLM** (2025) | ICLR | Focuses on large-scale orchestration of complex task workflows using a data-centric framework (*WorkflowBench*). |
| **UniRoute** (2025) | arXiv | Proposes dynamic routing for "unobserved" LLMs by representing models as feature vectors, overcoming the "fixed pool" limitation of previous routers. |

### 2. Trending Methodologies
- **Model Context Protocol (MCP)**: An emerging standard for how agents interact with tools and data sources, pioneered by Anthropic and adopted in latest research (PentestMCP).
- **Task Graph Reasoning**: Moving beyond linear chains to DAG-based task graphs (PTG) to maintain long-term context in complex engagements.
- **Learned Semantic Routing**: Routers now use small, dedicated classifiers (BERT/small LLMs) to predict model suitability based on prompt embeddings rather than simple keyword matching.
- **Curriculum Learning**: Training agents through progressively difficult "security levels" to improve reasoning robustness.

### 3. Competitive Analysis
| Framework | Focus Area | Key Limitation |
|-----------|------------|----------------|
| **PentestGPT** | Human-in-the-loop guidance | High manual effort; context swamp. |
| **AutoAttacker** | Post-breach automation | Limited to specific attack stages; monolithic. |
| **PentestMCP** | Tool orchestration standards | Focuses on protocol rather than cost/latency optimization. |
| **LLMOrch-VAPT** (This Paper) | **Operational Infrastructure** | Needs to ground its cost/quality routing logic in real-world data. |

### 4. Identified Research Gap
While 2025 SOTA papers like **PentestMCP** and **PentestAgent** excel at "attack intelligence" (the *how* of exploitation), they largely ignore the **"operational economics and resilience"** of the system.
- **Gap 1**: None of the new papers explicitly address **Provider Failover** and resilience for security agents (critical for enterprise SOCs).
- **Gap 2**: Most assume access to a flagship model (GPT-4o/Claude 3.5) and do not formalize the **Cost-Reasoning-Latency tradeoff** specifically for security task tiers (Flash vs. Pro).
- **Gap 3**: There is a lack of research on **Heterogeneous Backend Pooling** where local models (Ollama) are blended with cloud APIs for privacy-preserving sub-tasks.

## Key Decisions Made
- Confirmed that LLMOrch-VAPT's focus on "Operational Infrastructure" and "Cost-Quality Routing" is a valid and distinct research niche.
- Decided to include "Semantic Caching" (found in Step 1a) as a key differentiator against PentestMCP.
- Decided to frame the "Unified Provider Protocol" as a precursor or alternative to MCP, focusing on resilience rather than just standardization.

## Open Questions
- Can we compare LLMOrch-VAPT's keyword-based complexity routing against the "learned classifiers" mentioned in UniRoute?
- Is there any publicly available code for PentestMCP to use as a baseline for comparison?

## Checklist Results
- [PASS] Fresh search for 2024–2025 papers performed
- [PASS] 3–5 brand-new papers identified
- [PASS] Methodology trends for 2025 are summarized
- [PASS] Competitive analysis against current paper is done
- [PASS] A clear research gap is identified
- [PASS] Artifact saved as `artifacts/step-2b-sota-search.md`
- [PASS] No outdated sources (pre-2023) treated as SOTA

## Input for Next Step
Synthesis of the literature (Step 2a) and SOTA (Step 2b) into a unified "Related Work Taxonomy" (Step 2c). This will categorize all research into logical clusters, setting the stage for the paper's Introduction and Background sections.
