# [STEP 1a] — Codebase & Documentation Read

## Summary
Completed a comprehensive end-to-end audit of the CMatrix codebase and documentation. Identified the core components of the LLM orchestration layer, including the provider abstraction system, instance pooling mechanism, and per-user configuration management. Mapped the data flow from user input through the orchestrator and supervisor to specialized agents and tool execution.

## Full Output

### System Architecture Overview
The system follows a modular multi-agent architecture integrated into a modern web platform:
- **Frontend (Next.js)**: Provides the user interface for security assessments, LLM configuration, and real-time visualization of agent workflows.
- **Backend (FastAPI)**: Serves as the core orchestration engine, managing agent subgraphs, tool execution, and LLM provider integration.
- **Agent Layer (LangGraph)**: Implements a supervisor pattern to route tasks between 7 specialized security agents (Network, Web, Auth, Config, Intel, API, Command).
- **LLM Orchestration Layer**: A provider-agnostic abstraction layer that unified 6+ distinct LLM backends behind a common interface with pooling and multi-tenant config support.
- **Infrastructure**: PostgreSQL for persistent configuration/user data; Qdrant for semantic memory; Docker for containerized deployment.

### Key Modules
| Module | Purpose |
|--------|---------|
| `app/services/llm/providers/base.py` | Defines `LLMProvider` protocol and `LangChainAdapter` for framework compatibility. |
| `app/services/llm/pool.py` | Manages a pool of LLM provider instances to optimize resource usage during parallel agent execution. |
| `app/services/llm/db_factory.py` | Factory that instantiates specific providers based on database configuration. |
| `app/services/llm/config_profile_service.py` | Service layer for managing user-specific LLM configuration profiles. |
| `app/services/llm/api_provider_service.py` | Handles dynamic model discovery from various API providers. |
| `app/services/supervisor.py` | Analyzes task complexity and routes to specialized agents using a keyword-based scoring system. |
| `app/services/orchestrator.py` | Coordinates the main LangGraph workflow, integrating ToT, ReWOO, and HITL approval gates. |

### Data Flow
1. **Request Ingress**: User sends a task via the Next.js frontend to the FastAPI backend.
2. **Profile Resolution**: The system retrieves the user's active LLM configuration profile from PostgreSQL.
3. **Provider Instantiation**: The `AgentLLMPool` (via `DatabaseLLMProviderFactory`) gets or creates an `LLMProvider` instance for the session.
4. **Task Analysis**: The `SupervisorService` analyzes the user message to determine if specialized agents should be engaged.
5. **Execution Loop**:
    - If specialized: Supervisor delegates to specific subgraphs (e.g., Network Security Agent).
    - If general: Orchestrator calls the LLM provider to select tools.
6. **Tool Execution**: Tools call local commands or APIs, with results recorded in audit logs.
7. **Synthesis & Stream**: The orchestrator synthesizes the final result and streams it via SSE to the frontend.

### Technology Stack Summary
- **Languages**: Python (Backend), TypeScript (Frontend).
- **Frameworks**: FastAPI, Next.js, LangChain, LangGraph.
- **Storage**: PostgreSQL (SQL), Qdrant (Vector).
- **AI/LLM**: Google Gemini, Ollama, OpenRouter, HuggingFace, Cerebras.
- **Security Tools**: Nmap, Curl, etc. (wrapped as Python tools).

### Notable Implementation Details
- **LangChainAdapter**: A critical bridge that allows the custom `LLMProvider` ecosystem to work seamlessly with LangChain's standard agentic components.
- **Task Complexity Signaling**: The supervisor implicitly calculates task complexity (simple/moderate/complex), providing a foundation for future cost-aware routing.
- **Multi-Tenant LLM Support**: Unlike most AI systems that use a global API key, CMatrix enables per-user provider settings, which is essential for enterprise security environments.

## Key Decisions Made
- Focused on the `app/services/llm/` directory as the primary source for research claims related to model orchestration.
- Identified the `SupervisorService` as a secondary but important component for task-based routing research.

## Open Questions
- To what extent is the "complexity" signal in `SupervisorService` actually utilized for routing decisions currently? (Seems keyword-based for now).
- How does the `LangChainAdapter` handle streaming compared to the native `invoke_stream` method in providers?

## Checklist Results
- [PASS] `artifacts/research-area.md` has been read before starting
- [PASS] Every top-level directory and file has been read
- [PASS] Every module's purpose is documented
- [PASS] Data flow from input to output is fully mapped
- [PASS] All documentation files have been read
- [PASS] Technology stack is fully identified
- [PASS] Any discrepancies or unusual implementation choices are flagged
- [PASS] Artifact saved as `artifacts/step-1a-codebase-read.md`
- [PASS] `assets/ASSET-INDEX.md` created
- [PASS] No assumptions made — only what was actually found in the code

## Asset Files Created
- `assets/ASSET-INDEX.md`: Empty template for tracking paper assets.

## Input for Next Step
Comprehensive map of the CMatrix LLM orchestration codebase, including the provider interface, pooling mechanism, and multi-tenant configuration system. This will be used to cross-reference against the claims in the existing research paper draft.
