"""
Supervisor Service for Multi-Agent Coordination.

This module implements the Supervisor Pattern for coordinating specialized
agent subgraphs. The supervisor intelligently routes tasks to the most
appropriate agent, aggregates results, and handles errors and timeouts.

Architecture:
    Supervisor (Orchestrator)
        ├─ Network Security Agent (port scanning, network analysis)
        ├─ Web Security Agent (HTTP/HTTPS, headers, SSL)
        └─ Vulnerability Intelligence Agent (CVE search, threat intel)

The supervisor uses keyword-based routing and can delegate to multiple
agents for complex tasks requiring multi-domain expertise.
"""

import asyncio
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from loguru import logger

from app.agents.registry import AgentRegistry, get_agent_registry
from app.services.llm.providers import LLMProvider


class DelegationStrategy(Enum):
    """Strategy for delegating tasks to agents."""

    SINGLE = "single"  # Delegate to a single best-match agent
    SEQUENTIAL = "sequential"  # Delegate to multiple agents in sequence
    PARALLEL = "parallel"  # Delegate to multiple agents in parallel
    HIERARCHICAL = "hierarchical"  # Delegate with sub-delegation


class SupervisorService:
    """
    Supervisor service for coordinating specialized agent subgraphs.

    This service implements intelligent task routing, state aggregation,
    error handling, and timeout management for multi-agent workflows.

    Key Features:
    - Intelligent agent selection based on task analysis
    - Multiple delegation strategies (single, sequential, parallel)
    - State aggregation from multiple agents
    - Comprehensive error handling and recovery
    - Timeout management for long-running tasks
    - Detailed execution metrics and logging
    """

    # Default timeout for agent execution (seconds)
    DEFAULT_AGENT_TIMEOUT = 300  # 5 minutes

    # Maximum number of agents to delegate to in parallel
    MAX_PARALLEL_AGENTS = 3

    def __init__(self, agent_registry: Optional[AgentRegistry] = None):
        """
        Initialize the supervisor service.

        Args:
            agent_registry: Optional agent registry instance (uses global if not provided)
        """
        self.agent_registry = agent_registry or get_agent_registry()
        logger.info("Supervisor service initialized for multi-agent coordination")

    def analyze_task(self, task: str) -> dict[str, Any]:
        """
        Analyze a task to determine which agents should handle it.

        This method performs intelligent task analysis to identify:
        - Primary agent (best match)
        - Secondary agents (supporting agents)
        - Task complexity
        - Recommended delegation strategy

        Args:
            task: Task description from user

        Returns:
            Dictionary with analysis results:
            {
                "primary_agent": str,
                "secondary_agents": List[str],
                "complexity": str,  # "simple", "moderate", "complex"
                "strategy": DelegationStrategy,
                "confidence": float  # 0.0 to 1.0
            }
        """
        task_lower = task.lower()

        # Keyword-based agent matching with confidence scores
        agent_scores = {}

        # Network agent keywords
        network_keywords = [
            "scan",
            "port",
            "network",
            "nmap",
            "host",
            "ip",
            "ping",
            "tcp",
            "udp",
            "service",
            "open ports",
            "network security",
        ]
        network_score = sum(1 for kw in network_keywords if kw in task_lower)
        if network_score > 0:
            agent_scores["network"] = network_score

        # Web agent keywords
        web_keywords = [
            "web",
            "http",
            "https",
            "ssl",
            "tls",
            "header",
            "cookie",
            "website",
            "url",
            "domain",
            "certificate",
            "cors",
            "csp",
        ]
        web_score = sum(1 for kw in web_keywords if kw in task_lower)
        if web_score > 0:
            agent_scores["web"] = web_score

        # Vulnerability intelligence agent keywords
        vuln_keywords = [
            "cve",
            "vulnerability",
            "exploit",
            "nvd",
            "threat",
            "security advisory",
            "patch",
            "weakness",
            "exposure",
        ]
        vuln_score = sum(1 for kw in vuln_keywords if kw in task_lower)
        if vuln_score > 0:
            agent_scores["vuln_intel"] = vuln_score

        # Auth agent keywords
        auth_keywords = [
            "auth",
            "login",
            "password",
            "session",
            "credential",
            "brute force",
            "rate limit",
            "mfa",
            "2fa",
            "token",
            "jwt",
        ]
        auth_score = sum(1 for kw in auth_keywords if kw in task_lower)
        if auth_score > 0:
            agent_scores["auth"] = auth_score

        # Config agent keywords
        config_keywords = [
            "config",
            "compliance",
            "hardening",
            "cis",
            "pci",
            "hipaa",
            "soc2",
            "cloud",
            "aws",
            "azure",
            "gcp",
            "iam",
            "policy",
        ]
        config_score = sum(1 for kw in config_keywords if kw in task_lower)
        if config_score > 0:
            agent_scores["config"] = config_score

        # Determine primary and secondary agents
        if not agent_scores:
            # No clear match - use general orchestrator
            return {
                "primary_agent": None,
                "secondary_agents": [],
                "complexity": "simple",
                "strategy": DelegationStrategy.SINGLE,
                "confidence": 0.0,
            }

        # Sort agents by score
        sorted_agents = sorted(agent_scores.items(), key=lambda x: x[1], reverse=True)
        primary_agent = sorted_agents[0][0]
        primary_score = sorted_agents[0][1]

        # Determine secondary agents (score >= 30% of primary for better multi-agent detection)
        secondary_agents = [
            agent for agent, score in sorted_agents[1:] if score >= primary_score * 0.3
        ]

        # Determine complexity
        total_keywords = sum(agent_scores.values())
        if total_keywords >= 5:
            complexity = "complex"
        elif total_keywords >= 3:
            complexity = "moderate"
        else:
            complexity = "simple"

        # Determine strategy
        if len(secondary_agents) >= 2:
            strategy = DelegationStrategy.PARALLEL
        elif len(secondary_agents) == 1:
            strategy = DelegationStrategy.SEQUENTIAL
        else:
            strategy = DelegationStrategy.SINGLE

        # Calculate confidence (normalized score)
        max_possible_score = max(
            len(network_keywords),
            len(web_keywords),
            len(vuln_keywords),
            len(auth_keywords),
            len(config_keywords),
        )
        confidence = min(primary_score / max_possible_score, 1.0)

        result = {
            "primary_agent": primary_agent,
            "secondary_agents": secondary_agents,
            "complexity": complexity,
            "strategy": strategy,
            "confidence": confidence,
        }

        logger.info(f"Task analysis: {result}")
        return result

    async def delegate_to_agent(
        self,
        agent_type: str,
        task: str,
        context: dict[str, Any],
        llm_provider: LLMProvider,
        timeout: Optional[int] = None,
    ) -> dict[str, Any]:
        """
        Delegate a task to a specific agent with timeout handling.

        Args:
            agent_type: Type of agent to delegate to
            task: Task description
            context: Additional context for the task
            llm_provider: LLM provider instance
            timeout: Timeout in seconds (uses default if not provided)

        Returns:
            Dictionary with execution results:
            {
                "agent": str,
                "status": str,  # "success", "error", "timeout"
                "result": Any,
                "error": Optional[str],
                "execution_time": float,
                "timestamp": str
            }
        """
        timeout = timeout or self.DEFAULT_AGENT_TIMEOUT
        start_time = datetime.now()

        logger.info(f"Delegating task to {agent_type} agent (timeout: {timeout}s)")
        logger.debug(f"Task: {task[:100]}...")

        try:
            # Register agent with the provided LLM provider
            agent = self.agent_registry.register_agent_sync(agent_type, llm_provider)

            # Execute with timeout
            result = await asyncio.wait_for(agent.ainvoke(task, context), timeout=timeout)

            execution_time = (datetime.now() - start_time).total_seconds()

            logger.info(f"✓ {agent_type} agent completed in {execution_time:.2f}s")

            return {
                "agent": agent_type,
                "status": "success",
                "result": result,
                "error": None,
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat(),
            }

        except asyncio.TimeoutError:
            execution_time = (datetime.now() - start_time).total_seconds()
            error_msg = f"Agent execution timed out after {timeout}s"
            logger.error(f"✗ {agent_type} agent timeout: {error_msg}")

            return {
                "agent": agent_type,
                "status": "timeout",
                "result": None,
                "error": error_msg,
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            error_msg = f"Agent execution failed: {str(e)}"
            logger.error(f"✗ {agent_type} agent error: {error_msg}", exc_info=True)

            return {
                "agent": agent_type,
                "status": "error",
                "result": None,
                "error": error_msg,
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat(),
            }

    async def delegate_sequential(
        self,
        agents: list[str],
        task: str,
        context: dict[str, Any],
        llm_provider: LLMProvider,
        timeout_per_agent: Optional[int] = None,
    ) -> list[dict[str, Any]]:
        """
        Delegate task to multiple agents sequentially.

        Each agent receives the results from previous agents in the context.

        Args:
            agents: List of agent types to delegate to
            task: Task description
            context: Initial context
            llm_provider: LLM provider instance
            timeout_per_agent: Timeout per agent in seconds

        Returns:
            List of execution results from each agent
        """
        logger.info(f"Sequential delegation to {len(agents)} agents: {agents}")

        results = []
        accumulated_context = context.copy()

        for agent_type in agents:
            result = await self.delegate_to_agent(
                agent_type, task, accumulated_context, llm_provider, timeout_per_agent
            )
            results.append(result)

            # Add result to context for next agent
            if result["status"] == "success":
                accumulated_context[f"{agent_type}_result"] = result["result"]

            # Stop if agent failed critically
            if result["status"] == "error":
                logger.warning(f"Stopping sequential delegation due to error in {agent_type}")
                break

        return results

    async def delegate_parallel(
        self,
        agents: list[str],
        task: str,
        context: dict[str, Any],
        llm_provider: LLMProvider,
        timeout_per_agent: Optional[int] = None,
    ) -> list[dict[str, Any]]:
        """
        Delegate task to multiple agents in parallel.

        All agents execute simultaneously with the same context.

        Args:
            agents: List of agent types to delegate to
            task: Task description
            context: Context for all agents
            llm_provider: LLM provider instance
            timeout_per_agent: Timeout per agent in seconds

        Returns:
            List of execution results from all agents
        """
        # Limit parallel execution
        agents = agents[: self.MAX_PARALLEL_AGENTS]
        logger.info(f"Parallel delegation to {len(agents)} agents: {agents}")

        # Create tasks for all agents
        tasks = [
            self.delegate_to_agent(agent_type, task, context, llm_provider, timeout_per_agent)
            for agent_type in agents
        ]

        # Execute all in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle any exceptions from gather
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(
                    {
                        "agent": agents[i],
                        "status": "error",
                        "result": None,
                        "error": str(result),
                        "execution_time": 0.0,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            else:
                processed_results.append(result)

        return processed_results

    def aggregate_results(
        self, results: list[dict[str, Any]], strategy: DelegationStrategy
    ) -> dict[str, Any]:
        """
        Aggregate results from multiple agents into a unified response.

        Args:
            results: List of agent execution results
            strategy: Delegation strategy used

        Returns:
            Aggregated result dictionary:
            {
                "status": str,  # "success", "partial", "failed"
                "primary_result": Any,
                "supporting_results": List[Any],
                "errors": List[str],
                "execution_summary": Dict[str, Any],
                "final_answer": str
            }
        """
        logger.info(f"Aggregating {len(results)} agent results (strategy: {strategy.value})")

        successful_results = [r for r in results if r["status"] == "success"]
        failed_results = [r for r in results if r["status"] in ["error", "timeout"]]

        # Determine overall status
        if len(successful_results) == len(results):
            status = "success"
        elif len(successful_results) > 0:
            status = "partial"
        else:
            status = "failed"

        # Extract primary and supporting results
        primary_result = None
        supporting_results = []

        if successful_results:
            primary_result = successful_results[0]["result"]
            supporting_results = [r["result"] for r in successful_results[1:]]

        # Collect errors
        errors = [r["error"] for r in failed_results if r["error"]]

        # Create execution summary
        execution_summary = {
            "total_agents": len(results),
            "successful": len(successful_results),
            "failed": len(failed_results),
            "total_time": sum(r["execution_time"] for r in results),
            "strategy": strategy.value,
            "agents_used": [r["agent"] for r in results],
        }

        # Generate final answer by combining results
        final_answer = self._synthesize_final_answer(successful_results, failed_results, strategy)

        aggregated = {
            "status": status,
            "primary_result": primary_result,
            "supporting_results": supporting_results,
            "errors": errors,
            "execution_summary": execution_summary,
            "final_answer": final_answer,
        }

        logger.info(
            f"Aggregation complete: {status} ({len(successful_results)}/{len(results)} agents succeeded)"
        )
        return aggregated

    def _synthesize_final_answer(
        self,
        successful_results: list[dict[str, Any]],
        failed_results: list[dict[str, Any]],
        strategy: DelegationStrategy,
    ) -> str:
        """
        Synthesize a final answer from agent results.

        Args:
            successful_results: List of successful agent results
            failed_results: List of failed agent results
            strategy: Delegation strategy used

        Returns:
            Synthesized final answer string
        """
        if not successful_results:
            # All agents failed
            error_summary = "\n".join([f"- {r['agent']}: {r['error']}" for r in failed_results])
            return f"❌ **All agents failed to complete the task**\n\n{error_summary}"

        # Build answer from successful results
        answer_parts = []

        for i, result in enumerate(successful_results):
            agent_name = result["agent"].replace("_", " ").title()
            agent_result = result["result"]

            # Extract the final answer from SubgraphState
            if isinstance(agent_result, dict) and "messages" in agent_result:
                messages = agent_result["messages"]
                if messages:
                    last_message = messages[-1]
                    content = (
                        last_message.content
                        if hasattr(last_message, "content")
                        else str(last_message)
                    )

                    if i == 0:
                        # Primary result
                        answer_parts.append(f"## {agent_name} Analysis\n\n{content}")
                    else:
                        # Supporting results
                        answer_parts.append(
                            f"### Additional Insights from {agent_name}\n\n{content}"
                        )

        # Add failure notices if partial success
        if failed_results:
            failure_notice = "\n\n---\n\n⚠️ **Note**: Some agents encountered issues:\n"
            for r in failed_results:
                failure_notice += f"- {r['agent']}: {r['error']}\n"
            answer_parts.append(failure_notice)

        return "\n\n".join(answer_parts)

    async def supervise(
        self,
        task: str,
        context: dict[str, Any],
        llm_provider: LLMProvider,
        force_strategy: Optional[DelegationStrategy] = None,
        timeout: Optional[int] = None,
    ) -> dict[str, Any]:
        """
        Main supervision method - analyzes task and delegates to appropriate agents.

        This is the primary entry point for the supervisor service.

        Args:
            task: Task description from user
            context: Additional context for the task
            llm_provider: LLM provider instance
            force_strategy: Optional strategy override
            timeout: Optional timeout override

        Returns:
            Aggregated results from agent delegation
        """
        logger.info(f"🎯 Supervisor analyzing task: {task[:100]}...")

        # Analyze task to determine delegation strategy
        analysis = self.analyze_task(task)

        # Use forced strategy if provided
        strategy = force_strategy or analysis["strategy"]

        # Determine which agents to use
        agents_to_use = []
        if analysis["primary_agent"]:
            agents_to_use.append(analysis["primary_agent"])
            agents_to_use.extend(analysis["secondary_agents"])

        # If no agents matched, return None (orchestrator will handle with tools)
        if not agents_to_use:
            logger.info("No specialized agents matched - using general orchestrator")
            return {
                "status": "no_delegation",
                "reason": "No specialized agents matched the task",
                "analysis": analysis,
            }

        # Delegate based on strategy
        if strategy == DelegationStrategy.SINGLE:
            # Single agent delegation
            results = [
                await self.delegate_to_agent(agents_to_use[0], task, context, llm_provider, timeout)
            ]

        elif strategy == DelegationStrategy.SEQUENTIAL:
            # Sequential delegation
            results = await self.delegate_sequential(
                agents_to_use, task, context, llm_provider, timeout
            )

        elif strategy == DelegationStrategy.PARALLEL:
            # Parallel delegation
            results = await self.delegate_parallel(
                agents_to_use, task, context, llm_provider, timeout
            )

        else:
            # Fallback to single
            results = [
                await self.delegate_to_agent(agents_to_use[0], task, context, llm_provider, timeout)
            ]

        # Aggregate results
        aggregated = self.aggregate_results(results, strategy)
        aggregated["analysis"] = analysis

        return aggregated


# Global supervisor instance
_supervisor_service: Optional[SupervisorService] = None


def get_supervisor_service() -> SupervisorService:
    """
    Get or create the global supervisor service instance.

    Returns:
        SupervisorService instance
    """
    global _supervisor_service
    if _supervisor_service is None:
        _supervisor_service = SupervisorService()
    return _supervisor_service
