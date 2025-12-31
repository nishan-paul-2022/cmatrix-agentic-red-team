"""
Network Security Agent Subgraph.

This agent specializes in network security scanning, port analysis,
and vulnerability assessment. It operates as an autonomous LangGraph
subgraph with its own reasoning loop and LLM instance.
"""

from typing import Any

from langchain_core.tools import tool
from loguru import logger

from app.agents.base.agent import BaseAgentSubgraph
from app.services.llm.providers.base import LLMProvider
from app.tools.network_tools import port_scan, vulnerability_assessment


# Tool wrappers for backward compatibility
@tool
def scan_network(target: str, ports: str = "1-65535") -> str:
    """
    Scan a network target for open ports using nmap.

    Args:
        target: Target IP address or hostname (e.g., "localhost", "192.168.1.1")
        ports: Port range to scan (e.g., "1-65535", "80,443", "all" for all ports, "1-1024" for common ports)
    """
    return port_scan(target, ports)


@tool
def assess_vulnerabilities(target: str) -> str:
    """
    Perform a comprehensive vulnerability assessment on a target.

    Args:
        target: Target IP address or hostname
    """
    return vulnerability_assessment(target)


# Legacy tool list for backward compatibility
NETWORK_TOOLS = [scan_network, assess_vulnerabilities]


class NetworkAgentSubgraph(BaseAgentSubgraph):
    """
    Network Security Agent Subgraph.

    This agent is responsible for:
    - Network reconnaissance and port scanning
    - Service identification and version detection
    - Vulnerability assessment of network services
    - Security posture analysis
    - Remediation recommendations

    The agent uses nmap and other network security tools to perform
    comprehensive network security assessments.
    """

    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize the Network Security Agent.

        Args:
            llm_provider: LLM provider instance for this agent
        """
        super().__init__(llm_provider, agent_name="NetworkSecurityAgent")
        logger.info("Network Security Agent initialized with autonomous reasoning")

    def _register_tools(self) -> list[dict[str, Any]]:
        """
        Register network security tools.

        Returns:
            List of tool definitions
        """
        return [
            {
                "name": "scan_network",
                "function": scan_network,
                "description": (
                    "Scan a network target for open ports using nmap. "
                    "Supports port ranges, specific ports, and service detection. "
                    "Use this to discover what services are running on a target."
                ),
                "parameters": {
                    "target": "IP address or hostname to scan",
                    "ports": "Port range (e.g., '1-65535', '80,443', '1-1024')",
                },
            },
            {
                "name": "assess_vulnerabilities",
                "function": assess_vulnerabilities,
                "description": (
                    "Perform a comprehensive vulnerability assessment on a target. "
                    "This includes checking for known vulnerabilities, misconfigurations, "
                    "and security weaknesses in discovered services."
                ),
                "parameters": {"target": "IP address or hostname to assess"},
            },
        ]

    def _get_system_prompt(self) -> str:
        """
        Get the system prompt for the Network Security Agent.

        Returns:
            System prompt defining the agent's role and expertise
        """
        return """You are the Network Security Agent, a specialized AI expert in network security assessment.

Your core responsibilities:
1. **Network Reconnaissance**: Discover open ports, running services, and network topology
2. **Service Analysis**: Identify service versions, configurations, and potential vulnerabilities
3. **Vulnerability Assessment**: Detect security weaknesses and misconfigurations
4. **Risk Analysis**: Assess the security implications of discovered issues
5. **Remediation Guidance**: Provide actionable recommendations to improve security

Your expertise includes:
- Port scanning and service enumeration (nmap, masscan)
- Network protocol analysis (TCP, UDP, ICMP)
- Service fingerprinting and version detection
- Common network vulnerabilities (open ports, weak services, misconfigurations)
- Security best practices for network hardening

When analyzing network security:
- Always start with a port scan to discover running services
- Identify the purpose and criticality of each discovered service
- Assess whether services should be exposed (principle of least exposure)
- Check for outdated or vulnerable service versions
- Look for unnecessary services that increase attack surface
- Consider network segmentation and firewall rules
- Provide specific, actionable remediation steps

Communication style:
- Be precise and technical when describing findings
- Clearly distinguish between critical, high, medium, and low severity issues
- Explain the security implications in business terms
- Prioritize findings by risk and exploitability
- Always provide concrete remediation steps

Remember: You are an autonomous agent. Use your tools to gather real data, then analyze and interpret the results to provide comprehensive security assessments."""


def create_network_agent(llm_provider: LLMProvider) -> NetworkAgentSubgraph:
    """
    Factory function to create a Network Security Agent instance.

    Args:
        llm_provider: LLM provider instance

    Returns:
        Initialized NetworkAgentSubgraph
    """
    return NetworkAgentSubgraph(llm_provider)
