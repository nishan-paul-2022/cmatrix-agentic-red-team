# Supervisor Pattern: Complete Documentation

**Status:** ✅ Production Ready

---

## 1. Executive Summary

**Phase 2.2 Complete (Week 7 - Nov 2025)**

The Supervisor Pattern implements intelligent multi-agent coordination for CMatrix. It transforms the system from a single-threaded orchestrator into a hierarchical manager that delegates tasks to specialized agents (Network, Web, Vuln Intel). This architecture supports parallel execution, robust error handling, and state aggregation.

---

## 2. Quick Start

### Basic Usage

```python
from app.services.supervisor import get_supervisor_service

# Get supervisor instance
supervisor = get_supervisor_service()

# Analyze a task
analysis = supervisor.analyze_task("scan ports on localhost")
print(f"Agent: {analysis['primary_agent']}, Confidence: {analysis['confidence']}")

# Supervise execution
result = await supervisor.supervise(
    task="scan ports on localhost",
    context={},
    llm_provider=your_llm_provider
)

print(result["final_answer"])
```

### Delegation Strategies

| Strategy | Description | Example |
|----------|-------------|---------|
| **SINGLE** | One agent handles the task | "scan ports on localhost" |
| **SEQUENTIAL** | Multiple agents in sequence | "scan network then check web" |
| **PARALLEL** | Multiple agents simultaneously | "comprehensive security assessment" |

---

## 3. Architecture & Components

### High-Level Design

```
User Query
    ↓
Orchestrator Agent (LLM)
    ↓
_should_continue() routing
    ├─→ delegate (confidence >= 0.3)
    │       ↓
    │   Supervisor Service
    │       ├─→ Network Agent
    │       ├─→ Web Agent
    │       └─→ Vuln Intel Agent
    │       ↓
    │   Aggregate Results
    │       ↓
    │   Final Answer
    │
    └─→ tools (fallback)
```

### Key Components

1.  **Supervisor Service (`app/services/supervisor.py`)**:
    *   **Task Analysis**: Keyword-based matching with confidence scoring.
    *   **Delegation**: Manages Single, Sequential, and Parallel execution.
    *   **Aggregation**: Combines results into a unified response.
    *   **Error Handling**: Timeouts (default 300s) and graceful degradation.

2.  **Orchestrator Integration (`app/services/orchestrator.py`)**:
    *   **`delegate` Node**: New workflow node for agent delegation.
    *   **Routing Logic**: Automatically routes to agents if confidence is high.

---

## 4. Task Analysis & Agent Selection

The supervisor uses keyword matching to select the best agent.

| Agent | Keywords |
|-------|----------|
| **Network** | scan, port, network, nmap, host, ip, ping, tcp, udp |
| **Web** | web, http, https, ssl, tls, header, cookie, website, url |
| **Vuln Intel** | cve, vulnerability, exploit, nvd, threat, patch |

**Scoring Logic:**
*   Primary Agent: Highest keyword match score.
*   Secondary Agents: Score >= 30% of primary score.
*   Confidence: Normalized score (0.0 - 1.0).

---

## 5. Error Handling & Troubleshooting

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| **Agent Not Selected** | Confidence too low | Lower threshold in `supervisor.py` (default 0.3) |
| **Timeout** | Task too long | Increase timeout in `delegate_to_agent` (default 300s) |
| **Partial Results** | One agent failed | Check `result["status"] == "partial"` and use successful results |

### Monitoring

```python
result = await supervisor.supervise(...)
summary = result["execution_summary"]
print(f"Successful: {summary['successful']}, Failed: {summary['failed']}")
```

---

## 6. Testing & Verification

### Test Suite
*   **Location**: `app-backend/app/tests/test_supervisor.py`
*   **Coverage**: 21 unit tests covering analysis, delegation, and aggregation.

### Running Tests
```bash
pytest app-backend/app/tests/test_supervisor.py -v
```

### Demo Script
```bash
python3 -m app.examples.demo_supervisor
```

---

## 7. Future Roadmap (Phase 3)

*   **Agentic RAG**: For smarter CVE searching.
*   **Advanced Reasoning**: ReWOO and Tree of Thoughts patterns.
*   **Hierarchical Delegation**: Agents delegating to sub-agents.
