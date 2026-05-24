# [STEP 4a] — Technical Methodology — OUTPUT ARTIFACT

## 1) Summary
This sub-step defined the formal technical methodology for CMatrix, describing the internal logic of the Composite Reasoning Pipeline. We provided modular descriptions and formal algorithms for the five core components: Tree of Thoughts (ToT), ReWOO Planner, Worker Execution, Reflexion Engine, and HITL Safety Gate. We created two major LaTeX assets: `figure-02-system-architecture.tex` (technical architecture) and `algorithm-01-composite-reasoning.tex` (formal orchestration flow).

## 2) Full Output

### 2.1 Core Components & Methodology

#### 1. Orchestrator (LangGraph StateGraph)
- **Input**: User Objective ($O$), Infrastructure Context ($C$).
- **Logic**: A directed acyclic graph (DAG) that manages the transition between reasoning nodes. It ensures state persistence and handles "interrupt-and-resume" for HITL events.
- **Output**: Final Attack Report ($R$).

#### 2. Tree of Thoughts (ToT) Strategy Selector
- **Input**: Objective ($O$).
- **Algorithm**: Generates $N=3$ strategic candidates (Fast, Stealth, Comprehensive). Evaluates each against 5 heuristics (Speed, Thoroughness, Stealth, Cost, Success). Selects the candidate with the highest weighted score.
- **Output**: Selected Strategy ($S$).

#### 3. ReWOO Planner
- **Input**: Objective ($O$), Selected Strategy ($S$).
- **Algorithm**: Generates a dependency-aware "Blueprint" ($B$) of tool calls. Each step is represented as a symbolic variable (e.g., `#E1`, `#E2`) to handle inter-task data dependencies.
- **Output**: Blueprint Plan ($B$).

#### 4. Worker & HITL Gate
- **Input**: Blueprint Plan ($B$), Risk Policy ($P$).
- **Algorithm**: Iterates through the blueprint. For each action $A$, calculates Risk Score $R(A)$. If $R(A) > \text{Threshold}$, intercepts for human approval. Otherwise, delegates task to a specialized agent via Celery.
- **Output**: Observation Stream ($Obs$).

#### 5. Reflexion Engine
- **Input**: Objective ($O$), Observation Stream ($Obs$).
- **Algorithm**: Performs a "Gap Analysis" on the observations. If vulnerabilities were missed (e.g., port 80 found but not probed), generates structured `ImprovementAction` objects ($I$).
- **Output**: Corrective Actions ($I$).

### 2.2 Composite Reasoning Pipeline
The novelty of CMatrix lies in the **composition** of these patterns:
1.  **ToT** provides the "Strategic Lookahead" (which approach to take).
2.  **ReWOO** provides the "Efficiency" (parallelizable/decoupled planning).
3.  **Reflexion** provides the "Quality Control" (identifying and fixing mistakes).
4.  **HITL Gate** provides the "Governance" (safe execution).

This sequence transforms a single, fallible LLM call into a robust, self-correcting system capable of navigating complex security environments.

## 3) Key Decisions Made
- **Symbolic Execution in ReWOO**: Explicitly mentioned the use of symbolic variables (`#E1`) to justify how the system handles complex data dependencies in attack chains.
- **Hierarchical Risk Model**: Defined the HITL Gate's role as a "Risk Interceptor," elevating it from a simple UI feature to a formal architectural component.
- **Graph-Based Orchestration**: Emphasized LangGraph's role in managing the state machine, which is critical for the "Reproducibility" section of the paper.

## 4) Open Questions
- **Complexity of ToT Heuristics**: Are 5 heuristics too many for the paper? Should we simplify to 3 (Speed, Stealth, Thoroughness)?
- **Algorithm Detail**: Is the pseudocode in `algorithm-01` detailed enough for a security conference, or does it need more "mathematical" rigor?

## 5) Checklist Results (PASS/FAIL)
- [PASS] Modular description of all 5 components provided
- [PASS] Inputs and outputs for each component specified
- [PASS] Algorithm pseudocode/logic provided for each
- [PASS] `figure-02-system-architecture.tex` created with technical depth
- [PASS] `algorithm-01-composite-reasoning.tex` created using formal LaTeX
- [PASS] `ASSET-INDEX.md` updated
- [PASS] Methodology is grounded in the Step 1 code audit

## 6) Input for Next Step (Step 4b)
- **Experimental Protocol**: Step 4b will define exactly how to *test* this methodology, including the datasets and metrics.
- **Ablation Setup**: Define the "disabled" states for the reasoning suite to measure the impact of each component.

## 7) Asset Files Created
- `paper-research/paper-04-agent-reasoning/assets/figure-02-system-architecture.tex`: Tech architecture.
- `paper-research/paper-04-agent-reasoning/assets/algorithm-01-composite-reasoning.tex`: Orchestration algorithm.
- `paper-research/paper-04-agent-reasoning/assets/ASSET-INDEX.md`: Updated index.
