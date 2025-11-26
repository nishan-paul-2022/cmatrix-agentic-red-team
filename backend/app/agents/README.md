# Agent Subgraphs - Multi-Agent System

## Overview

This directory contains the implementation of autonomous agent subgraphs for the CMatrix cybersecurity platform. Each agent is a specialized LangGraph workflow with its own reasoning loop, tool execution capabilities, and LLM instance.

## Architecture

### Phase 2: True Multi-Agent System

```
┌─────────────────────────────────────────────────────────────┐
│                     Main Orchestrator                        │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Agent Registry                            │ │
│  │  • Agent Selection                                     │ │
│  │  • Lifecycle Management                                │ │
│  │  • Resource Optimization                               │ │
│  └────────────────────────────────────────────────────────┘ │
│                           │                                  │
│         ┌─────────────────┼─────────────────┐               │
│         │                 │                 │               │
│         ▼                 ▼                 ▼               │
│  ┌──────────┐      ┌──────────┐     ┌──────────┐           │
│  │ Network  │      │   Web    │     │  Vuln    │           │
│  │  Agent   │      │  Agent   │     │  Intel   │           │
│  │          │      │          │     │  Agent   │           │
│  │ ┌──────┐ │      │ ┌──────┐ │     │ ┌──────┐ │           │
│  │ │ LLM  │ │      │ │ LLM  │ │     │ │ LLM  │ │           │
│  │ └──────┘ │      │ └──────┘ │     │ └──────┘ │           │
│  │          │      │          │     │          │           │
│  │ Reason   │      │ Reason   │     │ Reason   │           │
│  │    ↓     │      │    ↓     │     │    ↓     │           │
│  │ Execute  │      │ Execute  │     │ Execute  │           │
│  │    ↓     │      │    ↓     │     │    ↓     │           │
│  │ Synthesize│     │ Synthesize│    │ Synthesize│          │
│  └──────────┘      └──────────┘     └──────────┘           │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
agents/
├── base/
│   ├── __init__.py           # Base package exports
│   ├── state.py              # SubgraphState TypedDict
│   └── subgraph.py           # BaseAgentSubgraph abstract class
├── specialized/
│   ├── network_agent.py      # Network Security Agent
│   ├── web_agent.py          # Web Security Agent
│   ├── vuln_intel_agent.py   # Vulnerability Intelligence Agent
│   ├── auth_agent.py         # Authentication Security Agent
│   ├── config_agent.py       # Configuration Analysis Agent
│   ├── api_security_agent.py # API Security Agent
│   └── command_agent.py      # Command Execution Agent
├── registry.py               # Agent Registry for management
└── README.md                 # This file
```

## Base Components

### SubgraphState

The state structure used by all agent subgraphs:

```python
class SubgraphState(TypedDict):
    messages: Sequence[BaseMessage]  # Conversation history
    task: str                        # Assigned task
    context: Dict[str, Any]          # Additional context
    results: List[Dict[str, Any]]    # Tool execution results
    metadata: Dict[str, Any]         # Agent metadata
    error: str                       # Error message if any
    completed: bool                  # Task completion status
    tool_calls: List[tuple]          # Pending tool calls
```

### BaseAgentSubgraph

Abstract base class for all specialized agents:

**Abstract Methods:**
- `_register_tools()`: Register agent-specific tools
- `_get_system_prompt()`: Define agent's expertise and role

**Workflow Nodes:**
- `_reason()`: Analyze task and decide on actions
- `_execute_tools()`: Run security tools
- `_synthesize()`: Analyze results and provide insights

**Features:**
- Autonomous reasoning loop (max 5 iterations)
- Error handling and recovery
- Sync and async invocation
- Comprehensive logging
- State management

## Specialized Agents

### 1. Network Security Agent

**File:** `specialized/network_agent.py`  
**Class:** `NetworkAgentSubgraph`

**Expertise:**
- Port scanning and service enumeration
- Network reconnaissance
- Vulnerability assessment
- Service fingerprinting

**Tools:**
- `scan_network(target, ports)`: Scan for open ports using nmap
- `assess_vulnerabilities(target)`: Comprehensive vulnerability assessment

**Use Cases:**
- Network security audits
- Service discovery
- Attack surface analysis
- Network hardening

**Example:**
```python
from app.agents.specialized.network_agent import create_network_agent

agent = create_network_agent(llm_provider)
result = await agent.ainvoke(
    task="Scan 192.168.1.1 for open ports",
    context={}
)
```

### 2. Web Security Agent

**File:** `specialized/web_agent.py`  
**Class:** `WebAgentSubgraph`

**Expertise:**
- OWASP Top 10 vulnerabilities
- SSL/TLS security
- HTTP security headers
- Web application security

**Tools:**
- `scan_web_app(url)`: Comprehensive web app security scan
- `check_ssl_security(url)`: SSL/TLS configuration analysis

**Use Cases:**
- Web application penetration testing
- SSL/TLS audits
- Security header validation
- OWASP compliance checking

**Example:**
```python
from app.agents.specialized.web_agent import create_web_agent

agent = create_web_agent(llm_provider)
result = await agent.ainvoke(
    task="Analyze https://example.com for security issues",
    context={}
)
```

### 3. Vulnerability Intelligence Agent

**File:** `specialized/vuln_intel_agent.py`  
**Class:** `VulnIntelAgentSubgraph`

**Expertise:**
- CVE research and analysis
- CVSS scoring
- Threat intelligence
- Patch prioritization

**Tools:**
- `search_cve(keyword, limit)`: Search CVE database
- `get_recent_cves(days, severity)`: Get recent high-severity CVEs
- `check_vulnerability_by_product(product, version)`: Check product vulnerabilities

**Use Cases:**
- CVE research
- Threat monitoring
- Vulnerability correlation
- Patch management

**Example:**
```python
from app.agents.specialized.vuln_intel_agent import create_vuln_intel_agent

agent = create_vuln_intel_agent(llm_provider)
result = await agent.ainvoke(
    task="Find recent critical CVEs for Apache",
    context={}
)
```

## Agent Registry

The `AgentRegistry` provides centralized management of all agents:

**Features:**
- Automatic agent selection based on keywords
- Agent lifecycle management
- LLM pool integration
- Caching and resource optimization

**Usage:**
```python
from app.agents.registry import get_agent_registry

registry = get_agent_registry()

# Automatic agent selection
agent_type = registry.select_agent("Scan localhost for open ports")
# Returns: "network_agent"

# Invoke agent
result = await registry.invoke_agent(
    agent_type=agent_type,
    task="Scan localhost for open ports",
    context={},
    db=db,
    user_id=user_id
)
```

## LLM Pool

The `AgentLLMPool` manages LLM instances for agents:

**Features:**
- Per-agent LLM instance caching
- Per-user configuration support
- Connection pooling
- Resource cleanup

**Usage:**
```python
from app.services.llm.pool import get_llm_pool

pool = get_llm_pool()
llm_provider = await pool.get_provider("network_agent", db, user_id)
```

## Creating a New Agent

To create a new specialized agent:

1. **Create the agent file** in `specialized/`:

```python
from app.agents.base.subgraph import BaseAgentSubgraph
from app.services.llm.providers import LLMProvider

class MyAgentSubgraph(BaseAgentSubgraph):
    def __init__(self, llm_provider: LLMProvider):
        super().__init__(llm_provider, agent_name="MyAgent")
    
    def _register_tools(self):
        return [
            {
                "name": "my_tool",
                "function": my_tool_function,
                "description": "Tool description",
                "parameters": {"param": "description"}
            }
        ]
    
    def _get_system_prompt(self):
        return """You are MyAgent, specialized in..."""

def create_my_agent(llm_provider: LLMProvider):
    return MyAgentSubgraph(llm_provider)
```

2. **Register in the Agent Registry** (`registry.py`):

```python
MY_AGENT = "my_agent"

AGENT_KEYWORDS = {
    MY_AGENT: ["keyword1", "keyword2", ...],
    # ...
}
```

3. **Add factory import** and registration logic

4. **Create tests** in `tests/agents/`

5. **Update documentation**

## Best Practices

### 1. System Prompts
- Be specific about agent expertise
- Include clear instructions for tool usage
- Define communication style
- Specify output format

### 2. Tool Registration
- Provide detailed descriptions
- Document all parameters
- Include usage examples
- Handle errors gracefully

### 3. Error Handling
- Always return completed state
- Set error field on failures
- Log errors with context
- Provide user-friendly messages

### 4. Performance
- Limit reasoning iterations (max 5)
- Cache LLM providers
- Use async invocation for I/O
- Clean up resources

### 5. Testing
- Test initialization
- Test tool registration
- Test workflow execution
- Test error scenarios
- Test max iterations

## Testing

Run agent tests:

```bash
# All agent tests
pytest app/tests/agents/test_subgraphs.py -v

# Specific agent
pytest app/tests/agents/test_subgraphs.py::TestNetworkAgentSubgraph -v

# With coverage
pytest app/tests/agents/ --cov=app.agents --cov-report=html
```

## Monitoring

Agents emit structured logs:

```python
logger.info(f"{self.agent_name}: Starting task execution")
logger.debug(f"{self.agent_name}: Routing to tool execution")
logger.error(f"{self.agent_name}: Error in reasoning", exc_info=True)
```

Monitor agent performance:

```python
result["metadata"]["reasoning_iterations"]  # Number of reasoning cycles
result["metadata"]["tools_executed"]        # Number of tools used
result["metadata"]["agent_name"]            # Agent identifier
```

## Examples

See `examples/agent_subgraph_usage.py` for comprehensive examples:

- Direct agent usage
- Registry-based usage
- Parallel multi-agent execution
- Agent capabilities discovery
- Error handling

## Migration from Phase 1

Phase 1 (Tool-based):
```python
from app.agents import NETWORK_TOOLS
# Tools are just functions, no reasoning
```

Phase 2 (Subgraph-based):
```python
from app.agents.specialized.network_agent import create_network_agent
# Agents are autonomous with reasoning loops
```

**Backward Compatibility:** Legacy `NETWORK_TOOLS`, `WEB_TOOLS`, etc. still work!

## Future Enhancements (Phase 3+)

- Agent collaboration (agents calling other agents)
- Shared memory and knowledge base
- Learning from past executions
- Multi-agent planning and coordination
- Agent specialization fine-tuning
- Custom agent creation via UI

## Resources

- **Implementation Plan:** `docs/phase2_implementation_plan.md`
- **Summary:** `docs/phase2_summary.md`
- **Checklist:** `docs/phase2_checklist.md`
- **Examples:** `examples/agent_subgraph_usage.py`
- **Tests:** `tests/agents/test_subgraphs.py`

## Support

For questions or issues:
1. Check the documentation in `docs/`
2. Review examples in `examples/`
3. Run tests to verify setup
4. Check logs for debugging

---

**Version:** Phase 2  
**Status:** Production Ready (Week 5-6 Complete)  
**Last Updated:** 2025-11-27
