"""
Tests for Supervisor Service and Multi-Agent Coordination.

This module tests the supervisor pattern implementation, including:
- Task analysis and agent selection
- Delegation strategies (single, sequential, parallel)
- State aggregation from multiple agents
- Error handling and timeout management
- End-to-end multi-agent workflows
"""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest

from app.services.llm.providers import LLMProvider
from app.services.supervisor import DelegationStrategy, SupervisorService, get_supervisor_service


class TestSupervisorService:
    """Test suite for SupervisorService."""

    @pytest.fixture
    def mock_llm_provider(self):
        """Create a mock LLM provider."""
        provider = Mock(spec=LLMProvider)
        provider.invoke = Mock(return_value="Test response")
        return provider

    @pytest.fixture
    def supervisor(self):
        """Create a supervisor service instance."""
        return SupervisorService()

    def test_supervisor_initialization(self, supervisor):
        """Test supervisor service initialization."""
        assert supervisor is not None
        assert supervisor.agent_registry is not None
        assert supervisor.DEFAULT_AGENT_TIMEOUT == 300
        assert supervisor.MAX_PARALLEL_AGENTS == 3

    def test_analyze_task_network_keywords(self, supervisor):
        """Test task analysis with network-related keywords."""
        task = "scan ports on 192.168.1.1 and check for open services"
        analysis = supervisor.analyze_task(task)

        assert analysis["primary_agent"] == "network"
        assert analysis["confidence"] > 0.0
        assert analysis["complexity"] in ["simple", "moderate", "complex"]
        assert isinstance(analysis["strategy"], DelegationStrategy)

    def test_analyze_task_web_keywords(self, supervisor):
        """Test task analysis with web-related keywords."""
        task = "check SSL certificate and HTTP headers for https://example.com"
        analysis = supervisor.analyze_task(task)

        assert analysis["primary_agent"] == "web"
        assert analysis["confidence"] > 0.0

    def test_analyze_task_vuln_keywords(self, supervisor):
        """Test task analysis with vulnerability-related keywords."""
        task = "search for CVE-2024-1234 and find related vulnerabilities"
        analysis = supervisor.analyze_task(task)

        assert analysis["primary_agent"] == "vuln_intel"
        assert analysis["confidence"] > 0.0

    def test_analyze_task_multiple_agents(self, supervisor):
        """Test task analysis that matches multiple agents."""
        task = "scan network ports and check for web vulnerabilities with CVE search"
        analysis = supervisor.analyze_task(task)

        assert analysis["primary_agent"] is not None
        assert len(analysis["secondary_agents"]) > 0
        assert analysis["complexity"] in ["moderate", "complex"]
        assert analysis["strategy"] in [DelegationStrategy.SEQUENTIAL, DelegationStrategy.PARALLEL]

    def test_analyze_task_no_match(self, supervisor):
        """Test task analysis with no clear agent match."""
        task = "what is the weather today?"
        analysis = supervisor.analyze_task(task)

        assert analysis["primary_agent"] is None
        assert len(analysis["secondary_agents"]) == 0
        assert analysis["confidence"] == 0.0
        assert analysis["strategy"] == DelegationStrategy.SINGLE

    @pytest.mark.asyncio
    async def test_delegate_to_agent_success(self, supervisor, mock_llm_provider):
        """Test successful delegation to a single agent."""
        task = "scan localhost ports"
        context = {}

        # Mock the agent registry
        with patch.object(supervisor.agent_registry, "register_agent_sync") as mock_register:
            mock_agent = Mock()
            mock_agent.ainvoke = AsyncMock(
                return_value={"messages": [Mock(content="Scan complete: 3 open ports found")]}
            )
            mock_register.return_value = mock_agent

            result = await supervisor.delegate_to_agent("network", task, context, mock_llm_provider)

            assert result["status"] == "success"
            assert result["agent"] == "network"
            assert result["result"] is not None
            assert result["error"] is None
            assert result["execution_time"] > 0

    @pytest.mark.asyncio
    async def test_delegate_to_agent_timeout(self, supervisor, mock_llm_provider):
        """Test agent delegation with timeout."""
        task = "scan localhost ports"
        context = {}

        # Mock the agent registry with a slow agent
        with patch.object(supervisor.agent_registry, "register_agent_sync") as mock_register:
            mock_agent = Mock()

            async def slow_invoke(*args, **kwargs):
                await asyncio.sleep(10)  # Simulate slow execution
                return {"messages": []}

            mock_agent.ainvoke = slow_invoke
            mock_register.return_value = mock_agent

            result = await supervisor.delegate_to_agent(
                "network",
                task,
                context,
                mock_llm_provider,
                timeout=1,  # 1 second timeout
            )

            assert result["status"] == "timeout"
            assert result["agent"] == "network"
            assert result["result"] is None
            assert "timed out" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_delegate_to_agent_error(self, supervisor, mock_llm_provider):
        """Test agent delegation with error."""
        task = "scan localhost ports"
        context = {}

        # Mock the agent registry with a failing agent
        with patch.object(supervisor.agent_registry, "register_agent_sync") as mock_register:
            mock_agent = Mock()
            mock_agent.ainvoke = AsyncMock(side_effect=Exception("Agent execution failed"))
            mock_register.return_value = mock_agent

            result = await supervisor.delegate_to_agent("network", task, context, mock_llm_provider)

            assert result["status"] == "error"
            assert result["agent"] == "network"
            assert result["result"] is None
            assert "failed" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_delegate_sequential(self, supervisor, mock_llm_provider):
        """Test sequential delegation to multiple agents."""
        task = "scan network and check web security"
        context = {}
        agents = ["network", "web"]

        # Mock the agent registry
        with patch.object(supervisor.agent_registry, "register_agent_sync") as mock_register:
            mock_agent = Mock()
            mock_agent.ainvoke = AsyncMock(
                return_value={"messages": [Mock(content="Agent completed")]}
            )
            mock_register.return_value = mock_agent

            results = await supervisor.delegate_sequential(agents, task, context, mock_llm_provider)

            assert len(results) == 2
            assert all(r["status"] == "success" for r in results)
            assert results[0]["agent"] == "network"
            assert results[1]["agent"] == "web"

    @pytest.mark.asyncio
    async def test_delegate_parallel(self, supervisor, mock_llm_provider):
        """Test parallel delegation to multiple agents."""
        task = "comprehensive security assessment"
        context = {}
        agents = ["network", "web", "vuln_intel"]

        # Mock the agent registry
        with patch.object(supervisor.agent_registry, "register_agent_sync") as mock_register:
            mock_agent = Mock()
            mock_agent.ainvoke = AsyncMock(
                return_value={"messages": [Mock(content="Agent completed")]}
            )
            mock_register.return_value = mock_agent

            results = await supervisor.delegate_parallel(agents, task, context, mock_llm_provider)

            assert len(results) == 3
            assert all(r["status"] == "success" for r in results)

    def test_aggregate_results_all_success(self, supervisor):
        """Test result aggregation with all successful agents."""
        results = [
            {
                "agent": "network",
                "status": "success",
                "result": {"messages": [Mock(content="Network scan complete")]},
                "error": None,
                "execution_time": 2.5,
            },
            {
                "agent": "web",
                "status": "success",
                "result": {"messages": [Mock(content="Web security check complete")]},
                "error": None,
                "execution_time": 1.8,
            },
        ]

        aggregated = supervisor.aggregate_results(results, DelegationStrategy.SEQUENTIAL)

        assert aggregated["status"] == "success"
        assert aggregated["primary_result"] is not None
        assert len(aggregated["supporting_results"]) == 1
        assert len(aggregated["errors"]) == 0
        assert aggregated["execution_summary"]["successful"] == 2
        assert aggregated["execution_summary"]["failed"] == 0

    def test_aggregate_results_partial_success(self, supervisor):
        """Test result aggregation with partial success."""
        results = [
            {
                "agent": "network",
                "status": "success",
                "result": {"messages": [Mock(content="Network scan complete")]},
                "error": None,
                "execution_time": 2.5,
            },
            {
                "agent": "web",
                "status": "error",
                "result": None,
                "error": "Connection failed",
                "execution_time": 0.5,
            },
        ]

        aggregated = supervisor.aggregate_results(results, DelegationStrategy.PARALLEL)

        assert aggregated["status"] == "partial"
        assert aggregated["primary_result"] is not None
        assert len(aggregated["errors"]) == 1
        assert aggregated["execution_summary"]["successful"] == 1
        assert aggregated["execution_summary"]["failed"] == 1

    def test_aggregate_results_all_failed(self, supervisor):
        """Test result aggregation with all failed agents."""
        results = [
            {
                "agent": "network",
                "status": "error",
                "result": None,
                "error": "Network error",
                "execution_time": 0.5,
            },
            {
                "agent": "web",
                "status": "timeout",
                "result": None,
                "error": "Timeout after 300s",
                "execution_time": 300.0,
            },
        ]

        aggregated = supervisor.aggregate_results(results, DelegationStrategy.PARALLEL)

        assert aggregated["status"] == "failed"
        assert aggregated["primary_result"] is None
        assert len(aggregated["errors"]) == 2
        assert aggregated["execution_summary"]["successful"] == 0
        assert aggregated["execution_summary"]["failed"] == 2
        assert "All agents failed" in aggregated["final_answer"]

    @pytest.mark.asyncio
    async def test_supervise_single_agent(self, supervisor, mock_llm_provider):
        """Test end-to-end supervision with single agent."""
        task = "scan localhost ports"
        context = {}

        # Mock the agent registry
        with patch.object(supervisor.agent_registry, "register_agent_sync") as mock_register:
            mock_agent = Mock()
            mock_agent.ainvoke = AsyncMock(
                return_value={"messages": [Mock(content="Scan complete: 3 open ports found")]}
            )
            mock_register.return_value = mock_agent

            result = await supervisor.supervise(task, context, mock_llm_provider)

            assert result["status"] == "success"
            assert result["analysis"]["primary_agent"] == "network"
            assert "final_answer" in result

    @pytest.mark.asyncio
    async def test_supervise_no_delegation(self, supervisor, mock_llm_provider):
        """Test supervision when no agents match."""
        task = "what is the weather today?"
        context = {}

        result = await supervisor.supervise(task, context, mock_llm_provider)

        assert result["status"] == "no_delegation"
        assert "reason" in result
        assert result["analysis"]["primary_agent"] is None

    @pytest.mark.asyncio
    async def test_supervise_with_strategy_override(self, supervisor, mock_llm_provider):
        """Test supervision with forced delegation strategy."""
        task = "scan network and web"
        context = {}

        # Mock the agent registry
        with patch.object(supervisor.agent_registry, "register_agent_sync") as mock_register:
            mock_agent = Mock()
            mock_agent.ainvoke = AsyncMock(
                return_value={"messages": [Mock(content="Agent completed")]}
            )
            mock_register.return_value = mock_agent

            result = await supervisor.supervise(
                task, context, mock_llm_provider, force_strategy=DelegationStrategy.PARALLEL
            )

            # Should use parallel strategy even if analysis suggests otherwise
            assert result["execution_summary"]["strategy"] == "parallel"

    def test_get_supervisor_service(self):
        """Test global supervisor service getter."""
        supervisor1 = get_supervisor_service()
        supervisor2 = get_supervisor_service()

        # Should return the same instance
        assert supervisor1 is supervisor2


class TestSupervisorIntegration:
    """Integration tests for supervisor with orchestrator."""

    @pytest.mark.asyncio
    async def test_orchestrator_delegates_to_network_agent(self):
        """Test that orchestrator correctly delegates network tasks."""
        # This would require a full orchestrator setup
        # Placeholder for integration test
        pass

    @pytest.mark.asyncio
    async def test_orchestrator_delegates_to_multiple_agents(self):
        """Test that orchestrator handles multi-agent delegation."""
        # Placeholder for integration test
        pass

    @pytest.mark.asyncio
    async def test_orchestrator_fallback_to_tools(self):
        """Test that orchestrator falls back to tools when no agents match."""
        # Placeholder for integration test
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
