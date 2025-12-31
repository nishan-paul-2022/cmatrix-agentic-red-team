"""
Tests for Auth and Config Agent Subgraphs.

This module contains unit tests for the new Auth and Config agent subgraphs.
"""

from unittest.mock import Mock

import pytest

from app.agents.specialized.auth_agent import AuthAgentSubgraph, create_auth_agent
from app.agents.specialized.config_agent import ConfigAgentSubgraph, create_config_agent
from app.services.llm.providers import LLMProvider


@pytest.fixture
def mock_llm_provider():
    """Create a mock LLM provider for testing."""
    provider = Mock(spec=LLMProvider)
    provider.invoke = Mock(return_value="Test response from LLM")
    return provider


class TestAuthAgentSubgraph:
    """Tests for Authentication Security Agent Subgraph."""

    def test_initialization(self, mock_llm_provider):
        """Test agent initialization."""
        agent = create_auth_agent(mock_llm_provider)

        assert isinstance(agent, AuthAgentSubgraph)
        assert agent.agent_name == "AuthSecurityAgent"
        assert len(agent.tools) == 4
        assert agent.llm_provider == mock_llm_provider

    def test_tool_registration(self, mock_llm_provider):
        """Test that tools are properly registered."""
        agent = create_auth_agent(mock_llm_provider)

        tool_names = [tool["name"] for tool in agent.tools]
        assert "analyze_auth_forms" in tool_names
        assert "check_sessions" in tool_names
        assert "test_auth_rate_limits" in tool_names
        assert "audit_password_policy" in tool_names

    def test_system_prompt(self, mock_llm_provider):
        """Test that system prompt is properly defined."""
        agent = create_auth_agent(mock_llm_provider)

        system_prompt = agent._get_system_prompt()
        assert "Authentication Security Agent" in system_prompt
        assert "Form Analysis" in system_prompt
        assert "Session Security" in system_prompt


class TestConfigAgentSubgraph:
    """Tests for Configuration Analysis Agent Subgraph."""

    def test_initialization(self, mock_llm_provider):
        """Test agent initialization."""
        agent = create_config_agent(mock_llm_provider)

        assert isinstance(agent, ConfigAgentSubgraph)
        assert agent.agent_name == "ConfigAnalysisAgent"
        assert len(agent.tools) == 3
        assert agent.llm_provider == mock_llm_provider

    def test_tool_registration(self, mock_llm_provider):
        """Test that tools are properly registered."""
        agent = create_config_agent(mock_llm_provider)

        tool_names = [tool["name"] for tool in agent.tools]
        assert "check_cloud_config" in tool_names
        assert "check_system_hardening" in tool_names
        assert "check_compliance" in tool_names

    def test_system_prompt(self, mock_llm_provider):
        """Test that system prompt is properly defined."""
        agent = create_config_agent(mock_llm_provider)

        system_prompt = agent._get_system_prompt()
        assert "Configuration Analysis Agent" in system_prompt
        assert "Cloud Security" in system_prompt
        assert "System Hardening" in system_prompt


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
