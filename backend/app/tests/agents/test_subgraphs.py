"""
Tests for Agent Subgraphs.

This module contains unit tests for the specialized agent subgraphs
to ensure they function correctly as autonomous agents.
"""

from unittest.mock import Mock, patch

import pytest

from app.agents.specialized.network_agent import NetworkAgentSubgraph, create_network_agent
from app.agents.specialized.vuln_intel_agent import VulnIntelAgentSubgraph, create_vuln_intel_agent
from app.agents.specialized.web_agent import WebAgentSubgraph, create_web_agent
from app.services.llm.providers import LLMProvider


@pytest.fixture
def mock_llm_provider():
    """Create a mock LLM provider for testing."""
    provider = Mock(spec=LLMProvider)
    provider.invoke = Mock(return_value="Test response from LLM")
    return provider


class TestNetworkAgentSubgraph:
    """Tests for Network Security Agent Subgraph."""

    def test_initialization(self, mock_llm_provider):
        """Test agent initialization."""
        agent = create_network_agent(mock_llm_provider)

        assert isinstance(agent, NetworkAgentSubgraph)
        assert agent.agent_name == "NetworkSecurityAgent"
        assert len(agent.tools) == 2
        assert agent.llm_provider == mock_llm_provider

    def test_tool_registration(self, mock_llm_provider):
        """Test that tools are properly registered."""
        agent = create_network_agent(mock_llm_provider)

        tool_names = [tool["name"] for tool in agent.tools]
        assert "scan_network" in tool_names
        assert "assess_vulnerabilities" in tool_names

    def test_system_prompt(self, mock_llm_provider):
        """Test that system prompt is properly defined."""
        agent = create_network_agent(mock_llm_provider)

        system_prompt = agent._get_system_prompt()
        assert "Network Security Agent" in system_prompt
        assert "port scanning" in system_prompt.lower()
        assert "vulnerability" in system_prompt.lower()

    @patch("app.agents.specialized.network_agent.port_scan")
    def test_invoke_with_scan_task(self, mock_port_scan, mock_llm_provider):
        """Test agent invocation with a network scan task."""
        # Mock the port scan tool
        mock_port_scan.return_value = "Open ports: 22, 80, 443"

        # Mock LLM to request a tool call, then synthesize
        mock_llm_provider.invoke = Mock(
            side_effect=[
                "TOOL: scan_network(target='localhost', ports='1-1024')",
                "Based on the scan results, ports 22, 80, and 443 are open.",
            ]
        )

        agent = create_network_agent(mock_llm_provider)
        result = agent.invoke(task="Scan localhost for open ports", context={})

        assert result["completed"] is True
        assert len(result["results"]) > 0
        assert mock_port_scan.called


class TestWebAgentSubgraph:
    """Tests for Web Security Agent Subgraph."""

    def test_initialization(self, mock_llm_provider):
        """Test agent initialization."""
        agent = create_web_agent(mock_llm_provider)

        assert isinstance(agent, WebAgentSubgraph)
        assert agent.agent_name == "WebSecurityAgent"
        assert len(agent.tools) == 2

    def test_tool_registration(self, mock_llm_provider):
        """Test that tools are properly registered."""
        agent = create_web_agent(mock_llm_provider)

        tool_names = [tool["name"] for tool in agent.tools]
        assert "scan_web_app" in tool_names
        assert "check_ssl_security" in tool_names

    def test_system_prompt(self, mock_llm_provider):
        """Test that system prompt is properly defined."""
        agent = create_web_agent(mock_llm_provider)

        system_prompt = agent._get_system_prompt()
        assert "Web Security Agent" in system_prompt
        assert "OWASP" in system_prompt
        assert "SSL/TLS" in system_prompt


class TestVulnIntelAgentSubgraph:
    """Tests for Vulnerability Intelligence Agent Subgraph."""

    def test_initialization(self, mock_llm_provider):
        """Test agent initialization."""
        agent = create_vuln_intel_agent(mock_llm_provider)

        assert isinstance(agent, VulnIntelAgentSubgraph)
        assert agent.agent_name == "VulnIntelAgent"
        assert len(agent.tools) == 5

    def test_tool_registration(self, mock_llm_provider):
        """Test that tools are properly registered."""
        agent = create_vuln_intel_agent(mock_llm_provider)

        tool_names = [tool["name"] for tool in agent.tools]
        assert "search_cve" in tool_names
        assert "get_recent_cves" in tool_names
        assert "check_vulnerability_by_product" in tool_names

    def test_system_prompt(self, mock_llm_provider):
        """Test that system prompt is properly defined."""
        agent = create_vuln_intel_agent(mock_llm_provider)

        system_prompt = agent._get_system_prompt()
        assert "Vulnerability Intelligence Agent" in system_prompt
        assert "CVE" in system_prompt
        assert "CVSS" in system_prompt


class TestAgentWorkflow:
    """Tests for agent workflow execution."""

    def test_reasoning_to_synthesis_flow(self, mock_llm_provider):
        """Test the complete workflow from reasoning to synthesis."""
        # Mock LLM to not request tools (go straight to synthesis)
        mock_llm_provider.invoke = Mock(return_value="No tools needed, here's my analysis.")

        agent = create_network_agent(mock_llm_provider)
        result = agent.invoke(task="Explain what port scanning is", context={})

        assert result["completed"] is True
        assert len(result["messages"]) > 0

    def test_error_handling(self, mock_llm_provider):
        """Test error handling in agent execution."""
        # Mock LLM to raise an exception
        mock_llm_provider.invoke = Mock(side_effect=Exception("LLM error"))

        agent = create_network_agent(mock_llm_provider)
        result = agent.invoke(task="Test error handling", context={})

        assert result["completed"] is True
        assert "error" in result
        assert "LLM error" in result["error"]

    def test_max_iterations(self, mock_llm_provider):
        """Test that agent respects max iteration limit."""
        # Mock LLM to always request tools (would loop forever without limit)
        mock_llm_provider.invoke = Mock(
            return_value="TOOL: scan_network(target=localhost, ports=80)"
        )

        agent = create_network_agent(mock_llm_provider)

        # Mock tool to always succeed
        with patch("app.tools.network_tools.port_scan", return_value="Port 80 open"):
            result = agent.invoke(task="Keep scanning", context={})

        # Should complete even with infinite loop attempt
        assert result["completed"] is True
        # Should not exceed max iterations
        assert result["metadata"]["reasoning_iterations"] <= 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
