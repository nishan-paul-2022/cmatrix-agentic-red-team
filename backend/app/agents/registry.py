"""
Agent Registry for Multi-Agent System.

This module provides a centralized registry for managing specialized agent
subgraphs, enabling dynamic agent selection and invocation.
"""

from typing import Optional

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.base.agent import BaseAgentSubgraph
from app.agents.specialized.auth_agent import create_auth_agent
from app.agents.specialized.config_agent import create_config_agent
from app.agents.specialized.network_agent import create_network_agent
from app.agents.specialized.vuln_intel_agent import create_vuln_intel_agent
from app.agents.specialized.web_agent import create_web_agent
from app.services.llm.pool import get_llm_pool
from app.services.llm.providers import LLMProvider


class AgentRegistry:
    """
    Registry for managing specialized agent subgraphs.

    This class provides:
    - Agent registration and lookup
    - Agent selection based on task type
    - Agent lifecycle management
    - Integration with LLM pool for resource management
    """

    # Agent type constants
    NETWORK_AGENT = "network_agent"
    WEB_AGENT = "web_agent"
    VULN_INTEL_AGENT = "vuln_intel_agent"
    AUTH_AGENT = "auth_agent"
    CONFIG_AGENT = "config_agent"

    # Keywords for agent selection
    AGENT_KEYWORDS = {
        NETWORK_AGENT: [
            "port",
            "scan",
            "network",
            "nmap",
            "service",
            "host",
            "tcp",
            "udp",
            "ping",
            "traceroute",
            "netstat",
            "firewall",
        ],
        WEB_AGENT: [
            "web",
            "http",
            "https",
            "ssl",
            "tls",
            "website",
            "url",
            "header",
            "cookie",
            "session",
            "xss",
            "csrf",
            "owasp",
        ],
        VULN_INTEL_AGENT: [
            "cve",
            "vulnerability",
            "exploit",
            "patch",
            "nvd",
            "security advisory",
            "threat",
            "zero-day",
            "cvss",
        ],
        AUTH_AGENT: [
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
        ],
        CONFIG_AGENT: [
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
        ],
    }

    def __init__(self):
        """Initialize the agent registry."""
        self.agents: dict[str, BaseAgentSubgraph] = {}
        self.llm_pool = get_llm_pool()
        logger.info("Agent Registry initialized")

    async def register_agent(
        self, agent_type: str, db: AsyncSession, user_id: int
    ) -> BaseAgentSubgraph:
        """
        Register and initialize an agent.

        Args:
            agent_type: Type of agent to register
            db: Database session
            user_id: User ID for LLM configuration

        Returns:
            Initialized agent subgraph

        Raises:
            ValueError: If agent type is unknown
        """
        cache_key = f"{agent_type}_{user_id}"

        if cache_key in self.agents:
            logger.debug(f"Using cached agent: {agent_type}")
            return self.agents[cache_key]

        # Get LLM provider for this agent
        llm_provider = await self.llm_pool.get_provider(agent_type, db, user_id)

        # Create agent based on type
        if agent_type == self.NETWORK_AGENT:
            agent = create_network_agent(llm_provider)
        elif agent_type == self.WEB_AGENT:
            agent = create_web_agent(llm_provider)
        elif agent_type == self.VULN_INTEL_AGENT:
            agent = create_vuln_intel_agent(llm_provider)
        elif agent_type == self.AUTH_AGENT:
            agent = create_auth_agent(llm_provider)
        elif agent_type == self.CONFIG_AGENT:
            agent = create_config_agent(llm_provider)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")

        self.agents[cache_key] = agent
        logger.info(f"Registered agent: {agent_type} for user {user_id}")

        return agent

    def register_agent_sync(self, agent_type: str, llm_provider: LLMProvider) -> BaseAgentSubgraph:
        """
        Register an agent synchronously with a pre-configured LLM provider.

        This is useful when the orchestrator already has a provider instance.

        Args:
            agent_type: Type of agent to register
            llm_provider: Pre-configured LLM provider

        Returns:
            Initialized agent subgraph

        Raises:
            ValueError: If agent type is unknown
        """
        cache_key = f"{agent_type}_shared"

        if cache_key in self.agents:
            return self.agents[cache_key]

        # Create agent based on type
        if agent_type == self.NETWORK_AGENT:
            agent = create_network_agent(llm_provider)
        elif agent_type == self.WEB_AGENT:
            agent = create_web_agent(llm_provider)
        elif agent_type == self.VULN_INTEL_AGENT:
            agent = create_vuln_intel_agent(llm_provider)
        elif agent_type == self.AUTH_AGENT:
            agent = create_auth_agent(llm_provider)
        elif agent_type == self.CONFIG_AGENT:
            agent = create_config_agent(llm_provider)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")

        self.agents[cache_key] = agent
        logger.info(f"Registered shared agent: {agent_type}")

        return agent

    def select_agent(self, user_message: str) -> Optional[str]:
        """
        Select the most appropriate agent based on user message.

        This method analyzes the user's message and selects the specialized
        agent best suited to handle the task.

        Args:
            user_message: The user's message/query

        Returns:
            Agent type string, or None if no specialized agent matches
        """
        message_lower = user_message.lower()

        # Score each agent based on keyword matches
        scores = {}
        for agent_type, keywords in self.AGENT_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                scores[agent_type] = score

        if not scores:
            logger.debug("No specialized agent matched, using general orchestrator")
            return None

        # Return agent with highest score
        selected_agent = max(scores, key=scores.get)
        logger.info(f"Selected agent: {selected_agent} (score: {scores[selected_agent]})")

        return selected_agent

    async def invoke_agent(
        self, agent_type: str, task: str, context: dict, db: AsyncSession, user_id: int
    ) -> dict:
        """
        Invoke a specialized agent to perform a task.

        Args:
            agent_type: Type of agent to invoke
            task: Task description
            context: Additional context for the task
            db: Database session
            user_id: User ID

        Returns:
            Agent execution results
        """
        # Register agent if not already registered
        agent = await self.register_agent(agent_type, db, user_id)

        # Invoke the agent
        logger.info(f"Invoking {agent_type} with task: {task[:100]}...")
        result = await agent.ainvoke(task, context)

        return result

    def get_available_agents(self) -> list[str]:
        """
        Get list of available agent types.

        Returns:
            List of agent type strings
        """
        return [
            self.NETWORK_AGENT,
            self.WEB_AGENT,
            self.VULN_INTEL_AGENT,
            self.AUTH_AGENT,
            self.CONFIG_AGENT,
        ]

    def get_agent_info(self, agent_type: str) -> dict:
        """
        Get information about an agent type.

        Args:
            agent_type: Type of agent

        Returns:
            Dictionary with agent information
        """
        info = {
            self.NETWORK_AGENT: {
                "name": "Network Security Agent",
                "description": "Specializes in network scanning, port analysis, and service enumeration",
                "capabilities": ["Port scanning", "Service detection", "Vulnerability assessment"],
                "keywords": self.AGENT_KEYWORDS[self.NETWORK_AGENT],
            },
            self.WEB_AGENT: {
                "name": "Web Security Agent",
                "description": "Specializes in web application security testing and SSL/TLS analysis",
                "capabilities": [
                    "Web app scanning",
                    "SSL/TLS testing",
                    "Security header validation",
                ],
                "keywords": self.AGENT_KEYWORDS[self.WEB_AGENT],
            },
            self.VULN_INTEL_AGENT: {
                "name": "Vulnerability Intelligence Agent",
                "description": "Specializes in CVE research and threat intelligence",
                "capabilities": ["CVE search", "Threat intelligence", "Vulnerability correlation"],
                "keywords": self.AGENT_KEYWORDS[self.VULN_INTEL_AGENT],
            },
            self.AUTH_AGENT: {
                "name": "Authentication Security Agent",
                "description": "Specializes in authentication security, session management, and password policies",
                "capabilities": [
                    "Login analysis",
                    "Session check",
                    "Rate limit testing",
                    "Password policy audit",
                ],
                "keywords": self.AGENT_KEYWORDS[self.AUTH_AGENT],
            },
            self.CONFIG_AGENT: {
                "name": "Configuration Analysis Agent",
                "description": "Specializes in cloud and system configuration security and compliance",
                "capabilities": [
                    "Cloud config check",
                    "System hardening",
                    "Compliance audit (CIS, PCI, etc.)",
                ],
                "keywords": self.AGENT_KEYWORDS[self.CONFIG_AGENT],
            },
        }

        return info.get(agent_type, {})

    def clear_cache(self, user_id: Optional[int] = None):
        """
        Clear cached agents.

        Args:
            user_id: If provided, only clear agents for this user
        """
        if user_id is not None:
            keys_to_remove = [key for key in self.agents if key.endswith(f"_{user_id}")]
            for key in keys_to_remove:
                del self.agents[key]
            logger.info(f"Cleared {len(keys_to_remove)} cached agents for user {user_id}")
        else:
            count = len(self.agents)
            self.agents.clear()
            logger.info(f"Cleared all {count} cached agents")

        # Also clear LLM pool cache
        self.llm_pool.clear_cache(user_id)


# Global agent registry instance
_agent_registry: Optional[AgentRegistry] = None


def get_agent_registry() -> AgentRegistry:
    """
    Get or create the global agent registry instance.

    Returns:
        AgentRegistry instance
    """
    global _agent_registry
    if _agent_registry is None:
        _agent_registry = AgentRegistry()
    return _agent_registry
