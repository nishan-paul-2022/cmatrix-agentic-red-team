"""
Unit tests for Self-Reflection Module.
"""

from unittest.mock import Mock

import pytest

from app.services.reasoning.reflection import (
    Gap,
    ImprovementAction,
    ImprovementPriority,
    ReflectionResult,
    ReflectionTrigger,
    SelfReflection,
    get_self_reflection,
)


@pytest.fixture
def mock_llm():
    """Create a mock LLM for testing."""
    llm = Mock()

    # Mock reflection response
    mock_response = Mock()
    mock_response.content = "The scan was incomplete. Critical ports were not checked, and no CVE search was performed. Recommend rescanning with full port range and searching for vulnerabilities."
    llm.invoke.return_value = mock_response

    return llm


@pytest.fixture
def reflection_service(mock_llm):
    """Create SelfReflection instance."""
    return SelfReflection(llm=mock_llm, enable_auto_reflection=True, quality_threshold=0.7)


class TestGap:
    """Test Gap dataclass."""

    def test_gap_creation(self):
        """Test creating a gap."""
        gap = Gap(
            category="missed_ports",
            description="Missed critical ports",
            severity=0.8,
            evidence=["Port 22 not scanned"],
            suggested_fix="Rescan with critical ports",
        )

        assert gap.category == "missed_ports"
        assert gap.severity == 0.8
        assert len(gap.evidence) == 1


class TestImprovementAction:
    """Test ImprovementAction dataclass."""

    def test_improvement_action_creation(self):
        """Test creating an improvement action."""
        action = ImprovementAction(
            action_id="improve_1",
            action_type="rescan",
            description="Rescan critical ports",
            tool_name="scan_network",
            parameters={"target": "192.168.1.1", "ports": "22,80,443"},
            priority=ImprovementPriority.HIGH,
            expected_benefit="Discover services on critical ports",
            estimated_time=15.0,
        )

        assert action.action_id == "improve_1"
        assert action.priority == ImprovementPriority.HIGH
        assert action.estimated_time == 15.0


class TestReflectionResult:
    """Test ReflectionResult dataclass."""

    def test_reflection_result_creation(self):
        """Test creating a reflection result."""
        gaps = [Gap(category="missed_ports", description="Missed ports", severity=0.9)]

        improvements = [
            ImprovementAction(
                action_id="improve_1",
                action_type="rescan",
                description="Rescan",
                tool_name="scan_network",
                parameters={},
                priority=ImprovementPriority.CRITICAL,
                expected_benefit="Better coverage",
            )
        ]

        result = ReflectionResult(
            reflection_id="test_reflection",
            task_description="Test task",
            execution_results={},
            quality_score=0.6,
            gaps=gaps,
            improvements=improvements,
            reasoning="Test reasoning",
            trigger=ReflectionTrigger.TASK_COMPLETION,
        )

        assert result.reflection_id == "test_reflection"
        assert result.quality_score == 0.6
        assert len(result.gaps) == 1
        assert len(result.improvements) == 1

    def test_has_critical_gaps(self):
        """Test checking for critical gaps."""
        gaps = [
            Gap(category="test", description="Test", severity=0.9),
            Gap(category="test2", description="Test2", severity=0.5),
        ]

        result = ReflectionResult(
            reflection_id="test",
            task_description="Test",
            execution_results={},
            quality_score=0.7,
            gaps=gaps,
            improvements=[],
            reasoning="Test",
            trigger=ReflectionTrigger.TASK_COMPLETION,
        )

        assert result.has_critical_gaps()

    def test_get_high_priority_actions(self):
        """Test getting high priority actions."""
        improvements = [
            ImprovementAction(
                action_id="1",
                action_type="test",
                description="Test",
                tool_name="test",
                parameters={},
                priority=ImprovementPriority.CRITICAL,
                expected_benefit="Test",
            ),
            ImprovementAction(
                action_id="2",
                action_type="test",
                description="Test",
                tool_name="test",
                parameters={},
                priority=ImprovementPriority.LOW,
                expected_benefit="Test",
            ),
            ImprovementAction(
                action_id="3",
                action_type="test",
                description="Test",
                tool_name="test",
                parameters={},
                priority=ImprovementPriority.HIGH,
                expected_benefit="Test",
            ),
        ]

        result = ReflectionResult(
            reflection_id="test",
            task_description="Test",
            execution_results={},
            quality_score=0.7,
            gaps=[],
            improvements=improvements,
            reasoning="Test",
            trigger=ReflectionTrigger.TASK_COMPLETION,
        )

        high_priority = result.get_high_priority_actions()
        assert len(high_priority) == 2
        assert all(
            a.priority in [ImprovementPriority.CRITICAL, ImprovementPriority.HIGH]
            for a in high_priority
        )


class TestSelfReflection:
    """Test SelfReflection service."""

    def test_initialization(self, mock_llm):
        """Test service initialization."""
        service = SelfReflection(llm=mock_llm, enable_auto_reflection=True, quality_threshold=0.75)

        assert service.llm == mock_llm
        assert service.enable_auto_reflection
        assert service.quality_threshold == 0.75

    def test_reflect_basic(self, reflection_service):
        """Test basic reflection."""
        result = reflection_service.reflect(
            task="Scan 192.168.1.5",
            execution_results={"open_ports": [80, 443]},
            trigger=ReflectionTrigger.TASK_COMPLETION,
        )

        assert result is not None
        assert result.task_description == "Scan 192.168.1.5"
        assert result.quality_score >= 0.0
        assert result.quality_score <= 1.0
        assert isinstance(result.gaps, list)
        assert isinstance(result.improvements, list)

    def test_assess_quality_good_scan(self, reflection_service):
        """Test quality assessment for good scan."""
        execution_results = {
            "open_ports": [22, 80, 443, 3306],
            "services": ["ssh", "http", "https", "mysql"],
            "cves": ["CVE-2024-1", "CVE-2024-2", "CVE-2024-3"],
        }

        score = reflection_service._assess_quality("Scan network", execution_results)

        # Good results should have high score
        assert score >= 0.7

    def test_assess_quality_poor_scan(self, reflection_service):
        """Test quality assessment for poor scan."""
        execution_results = {"error": "Scan failed"}

        score = reflection_service._assess_quality("Scan network", execution_results)

        # Error should significantly reduce score
        assert score <= 0.5

    def test_assess_quality_empty_results(self, reflection_service):
        """Test quality assessment for empty results."""
        execution_results = {}

        score = reflection_service._assess_quality("Scan network", execution_results)

        # Empty results should have low score
        assert score <= 0.7

    def test_detect_gaps_missed_ports(self, reflection_service):
        """Test gap detection for missed critical ports."""
        execution_results = {
            "open_ports": [8080]  # Missing critical ports
        }

        gaps = reflection_service._detect_gaps("scan network", execution_results, None)

        # Should detect missed critical ports
        missed_port_gaps = [g for g in gaps if g.category == "missed_ports"]
        assert len(missed_port_gaps) > 0

    def test_detect_gaps_missing_service_info(self, reflection_service):
        """Test gap detection for missing service info."""
        execution_results = {
            "open_ports": [80, 443],
            "services": [],  # No service info
        }

        gaps = reflection_service._detect_gaps("scan network", execution_results, None)

        # Should detect missing service info
        service_gaps = [g for g in gaps if g.category == "missing_service_info"]
        assert len(service_gaps) > 0

    def test_detect_gaps_no_vulnerability_check(self, reflection_service):
        """Test gap detection for missing CVE search."""
        execution_results = {
            "open_ports": [80],
            "services": ["apache"],
            "cves": [],  # No CVEs searched
        }

        gaps = reflection_service._detect_gaps("scan network", execution_results, None)

        # Should detect missing vulnerability check
        vuln_gaps = [g for g in gaps if g.category == "no_vulnerability_check"]
        assert len(vuln_gaps) > 0

    def test_generate_improvements_for_missed_ports(self, reflection_service):
        """Test improvement generation for missed ports."""
        gaps = [Gap(category="missed_ports", description="Missed critical ports", severity=0.8)]

        execution_results = {"target": "192.168.1.5"}

        improvements = reflection_service._generate_improvements(
            "scan network", execution_results, gaps, None
        )

        # Should generate rescan improvement
        assert len(improvements) > 0
        assert any(imp.action_type == "rescan" for imp in improvements)

    def test_generate_improvements_for_missing_cve(self, reflection_service):
        """Test improvement generation for missing CVE search."""
        gaps = [Gap(category="no_vulnerability_check", description="No CVE search", severity=0.9)]

        execution_results = {"services": ["apache", "nginx"]}

        improvements = reflection_service._generate_improvements(
            "scan network", execution_results, gaps, None
        )

        # Should generate CVE search improvements
        cve_improvements = [imp for imp in improvements if imp.action_type == "cve_search"]
        assert len(cve_improvements) > 0
        assert any(imp.priority == ImprovementPriority.CRITICAL for imp in cve_improvements)

    def test_reflection_history(self, reflection_service):
        """Test reflection history tracking."""
        # Perform multiple reflections
        for i in range(3):
            reflection_service.reflect(
                task=f"Task {i}", execution_results={}, trigger=ReflectionTrigger.TASK_COMPLETION
            )

        history = reflection_service.get_reflection_history(limit=5)
        assert len(history) == 3

    def test_get_common_gaps(self, reflection_service):
        """Test common gap pattern analysis."""
        # Create reflections with common gaps
        for _i in range(3):
            reflection_service.reflect(
                task="scan network",
                execution_results={"open_ports": [8080]},  # Will trigger missed_ports gap
                trigger=ReflectionTrigger.TASK_COMPLETION,
            )

        common_gaps = reflection_service.get_common_gaps()

        # missed_ports should be common
        assert "missed_ports" in common_gaps
        assert common_gaps["missed_ports"] >= 3

    def test_get_average_quality_score(self, reflection_service):
        """Test average quality score calculation."""
        # Perform reflections with different quality
        reflection_service.reflect(
            task="Good scan",
            execution_results={
                "open_ports": [22, 80, 443],
                "services": ["ssh", "http", "https"],
                "cves": ["CVE-1", "CVE-2"],
            },
            trigger=ReflectionTrigger.TASK_COMPLETION,
        )

        reflection_service.reflect(
            task="Poor scan",
            execution_results={"error": "Failed"},
            trigger=ReflectionTrigger.TASK_COMPLETION,
        )

        avg_score = reflection_service.get_average_quality_score()
        assert 0.0 <= avg_score <= 1.0


class TestGlobalInstance:
    """Test global instance management."""

    def test_get_self_reflection(self, mock_llm):
        """Test getting global reflection instance."""
        service1 = get_self_reflection(mock_llm)
        service2 = get_self_reflection(mock_llm)

        # Should return same instance
        assert service1 is service2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
