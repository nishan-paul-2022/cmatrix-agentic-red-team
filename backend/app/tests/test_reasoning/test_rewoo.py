"""
Unit tests for ReWOO (Reasoning Without Observation) Planner.
"""

import json
from unittest.mock import Mock

import pytest

from app.services.reasoning.rewoo import Plan, PlanStatus, PlanStep, ReWOOPlanner, get_rewoo_planner


@pytest.fixture
def mock_llm():
    """Create a mock LLM for testing."""
    llm = Mock()

    # Mock successful plan generation
    mock_response = Mock()
    mock_response.content = json.dumps(
        {
            "steps": [
                {
                    "step_id": "#E1",
                    "tool_name": "scan_network",
                    "parameters": {"target": "192.168.1.0/24", "ports": "1-1000"},
                    "description": "Scan network for open ports",
                    "dependencies": [],
                    "expected_output": "List of open ports",
                },
                {
                    "step_id": "#E2",
                    "tool_name": "search_cve",
                    "parameters": {"keyword": "apache"},
                    "description": "Search for Apache CVEs",
                    "dependencies": ["#E1"],
                    "expected_output": "CVE list",
                },
            ],
            "estimated_duration": 30.0,
            "confidence": 0.9,
            "reasoning": "Systematic network scan followed by CVE search",
        }
    )
    llm.invoke.return_value = mock_response

    return llm


@pytest.fixture
def available_tools():
    """Create mock available tools."""
    return {
        "scan_network": {
            "description": "Scan network ports",
            "parameters": {"target": {"type": "string"}, "ports": {"type": "string"}},
        },
        "search_cve": {
            "description": "Search CVE database",
            "parameters": {"keyword": {"type": "string"}},
        },
        "check_service_version": {
            "description": "Check service versions",
            "parameters": {"target": {"type": "string"}},
        },
    }


@pytest.fixture
def planner(mock_llm, available_tools):
    """Create ReWOO planner instance."""
    return ReWOOPlanner(
        llm=mock_llm,
        available_tools=available_tools,
        enable_cache=False,  # Disable cache for testing
    )


class TestPlanStep:
    """Test PlanStep dataclass."""

    def test_plan_step_creation(self):
        """Test creating a plan step."""
        step = PlanStep(
            step_id="#E1",
            tool_name="scan_network",
            parameters={"target": "192.168.1.1"},
            description="Scan target",
        )

        assert step.step_id == "#E1"
        assert step.tool_name == "scan_network"
        assert step.status == PlanStatus.PENDING
        assert step.dependencies == []

    def test_plan_step_with_dependencies(self):
        """Test plan step with dependencies."""
        step = PlanStep(
            step_id="#E2",
            tool_name="search_cve",
            parameters={"keyword": "apache"},
            description="Search CVEs",
            dependencies=["#E1"],
        )

        assert step.dependencies == ["#E1"]


class TestPlan:
    """Test Plan dataclass."""

    def test_plan_creation(self):
        """Test creating a plan."""
        steps = [
            PlanStep(step_id="#E1", tool_name="scan_network", parameters={}, description="Step 1")
        ]

        plan = Plan(
            plan_id="test_plan",
            task_description="Test task",
            steps=steps,
            estimated_duration=10.0,
            confidence=0.8,
            reasoning="Test reasoning",
        )

        assert plan.plan_id == "test_plan"
        assert len(plan.steps) == 1
        assert plan.status == PlanStatus.PENDING

    def test_get_step(self):
        """Test getting a step by ID."""
        steps = [
            PlanStep(step_id="#E1", tool_name="tool1", parameters={}, description="Step 1"),
            PlanStep(step_id="#E2", tool_name="tool2", parameters={}, description="Step 2"),
        ]

        plan = Plan(
            plan_id="test",
            task_description="Test",
            steps=steps,
            estimated_duration=10.0,
            confidence=0.8,
            reasoning="Test",
        )

        step = plan.get_step("#E2")
        assert step is not None
        assert step.tool_name == "tool2"

        missing = plan.get_step("#E99")
        assert missing is None

    def test_get_executable_steps(self):
        """Test getting executable steps."""
        steps = [
            PlanStep(step_id="#E1", tool_name="tool1", parameters={}, description="Step 1"),
            PlanStep(
                step_id="#E2",
                tool_name="tool2",
                parameters={},
                description="Step 2",
                dependencies=["#E1"],
            ),
        ]

        plan = Plan(
            plan_id="test",
            task_description="Test",
            steps=steps,
            estimated_duration=10.0,
            confidence=0.8,
            reasoning="Test",
        )

        # Initially, only #E1 is executable
        executable = plan.get_executable_steps()
        assert len(executable) == 1
        assert executable[0].step_id == "#E1"

        # After #E1 completes, #E2 becomes executable
        steps[0].status = PlanStatus.COMPLETED
        executable = plan.get_executable_steps()
        assert len(executable) == 1
        assert executable[0].step_id == "#E2"

    def test_is_complete(self):
        """Test checking if plan is complete."""
        steps = [
            PlanStep(step_id="#E1", tool_name="tool1", parameters={}, description="Step 1"),
            PlanStep(step_id="#E2", tool_name="tool2", parameters={}, description="Step 2"),
        ]

        plan = Plan(
            plan_id="test",
            task_description="Test",
            steps=steps,
            estimated_duration=10.0,
            confidence=0.8,
            reasoning="Test",
        )

        assert not plan.is_complete()

        steps[0].status = PlanStatus.COMPLETED
        steps[1].status = PlanStatus.COMPLETED
        assert plan.is_complete()

    def test_has_failures(self):
        """Test checking for failures."""
        steps = [
            PlanStep(step_id="#E1", tool_name="tool1", parameters={}, description="Step 1"),
            PlanStep(step_id="#E2", tool_name="tool2", parameters={}, description="Step 2"),
        ]

        plan = Plan(
            plan_id="test",
            task_description="Test",
            steps=steps,
            estimated_duration=10.0,
            confidence=0.8,
            reasoning="Test",
        )

        assert not plan.has_failures()

        steps[1].status = PlanStatus.FAILED
        assert plan.has_failures()


class TestReWOOPlanner:
    """Test ReWOO Planner."""

    def test_planner_initialization(self, mock_llm, available_tools):
        """Test planner initialization."""
        planner = ReWOOPlanner(llm=mock_llm, available_tools=available_tools, enable_cache=False)

        assert planner.llm == mock_llm
        assert len(planner.available_tools) == 3
        assert not planner.enable_cache

    def test_generate_plan_llm(self, planner, mock_llm):
        """Test LLM-based plan generation."""
        plan = planner.generate_plan("Scan 192.168.1.0/24 for vulnerabilities")

        assert plan is not None
        assert len(plan.steps) == 2
        assert plan.steps[0].tool_name == "scan_network"
        assert plan.steps[1].tool_name == "search_cve"
        assert plan.confidence == 0.9
        assert plan.status == PlanStatus.VALIDATED

        # Verify LLM was called
        mock_llm.invoke.assert_called_once()

    def test_generate_plan_template(self, planner):
        """Test template-based plan generation."""
        # Enable templates
        planner.enable_templates = True

        plan = planner.generate_plan("scan network 192.168.1.0/24")

        assert plan is not None
        assert len(plan.steps) > 0
        # Template plans should have good confidence
        assert plan.confidence >= 0.8

    def test_extract_parameters_from_task(self, planner):
        """Test parameter extraction from task."""
        # Test IP extraction
        params = planner._extract_parameters_from_task("Scan 192.168.1.0/24", "scan_network")
        assert params["target"] == "192.168.1.0/24"

        # Test URL extraction
        params = planner._extract_parameters_from_task(
            "Check https://example.com", "validate_http_url"
        )
        assert params["url"] == "https://example.com"

        # Test CVE extraction
        params = planner._extract_parameters_from_task(
            "Get details for CVE-2024-1234", "get_cve_details"
        )
        assert params["cve_id"] == "CVE-2024-1234"

    def test_validate_plan_success(self, planner):
        """Test plan validation with valid tools."""
        steps = [
            PlanStep(step_id="#E1", tool_name="scan_network", parameters={}, description="Step 1")
        ]

        plan = Plan(
            plan_id="test",
            task_description="Test",
            steps=steps,
            estimated_duration=10.0,
            confidence=0.8,
            reasoning="Test",
        )

        validated = planner._validate_plan(plan)

        assert validated.status == PlanStatus.VALIDATED
        assert validated.steps[0].status == PlanStatus.VALIDATED

    def test_validate_plan_invalid_tool(self, planner):
        """Test plan validation with invalid tool."""
        steps = [
            PlanStep(
                step_id="#E1", tool_name="nonexistent_tool", parameters={}, description="Step 1"
            )
        ]

        plan = Plan(
            plan_id="test",
            task_description="Test",
            steps=steps,
            estimated_duration=10.0,
            confidence=0.8,
            reasoning="Test",
        )

        validated = planner._validate_plan(plan)

        assert validated.status == PlanStatus.FAILED
        assert validated.steps[0].status == PlanStatus.FAILED
        assert "not available" in validated.steps[0].error

    def test_validate_plan_invalid_dependency(self, planner):
        """Test plan validation with invalid dependency."""
        steps = [
            PlanStep(
                step_id="#E1",
                tool_name="scan_network",
                parameters={},
                description="Step 1",
                dependencies=["#E99"],  # Non-existent dependency
            )
        ]

        plan = Plan(
            plan_id="test",
            task_description="Test",
            steps=steps,
            estimated_duration=10.0,
            confidence=0.8,
            reasoning="Test",
        )

        validated = planner._validate_plan(plan)

        assert validated.steps[0].status == PlanStatus.FAILED
        assert "Dependency" in validated.steps[0].error

    def test_fallback_plan(self, planner, mock_llm):
        """Test fallback plan when LLM fails."""
        # Make LLM raise exception
        mock_llm.invoke.side_effect = Exception("LLM error")

        plan = planner.generate_plan("Test task")

        assert plan is not None
        assert len(plan.steps) >= 1
        assert plan.confidence < 0.5  # Fallback plans have low confidence
        assert "fallback" in plan.metadata


class TestGlobalInstance:
    """Test global instance management."""

    def test_get_rewoo_planner(self, mock_llm, available_tools):
        """Test getting global planner instance."""
        planner1 = get_rewoo_planner(mock_llm, available_tools)
        planner2 = get_rewoo_planner(mock_llm, available_tools)

        # Should return same instance
        assert planner1 is planner2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
