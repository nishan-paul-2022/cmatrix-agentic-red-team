"""
Self-Reflection Module - Post-Execution Analysis and Improvement.

This module enables the agent to critique and improve its own work through
systematic self-reflection. After completing tasks, the agent analyzes its
performance, identifies gaps, and suggests improvements.

Key Capabilities:
- Quality assessment of scan results
- Gap detection (missed ports, services, vulnerabilities)
- Consistency checking across findings
- Improvement action generation
- Learning from past mistakes

Design Pattern:
1. Analyzer: Evaluate task execution quality
2. Critic: Identify gaps and inconsistencies
3. Improver: Generate actionable improvements
4. Tracker: Learn from reflection history

References:
- Reflexion Paper: https://arxiv.org/abs/2303.11366
- Self-Refine: https://arxiv.org/abs/2303.17651
"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger


class ReflectionTrigger(str, Enum):
    """Triggers for self-reflection."""

    TASK_COMPLETION = "task_completion"
    USER_REQUEST = "user_request"
    ANOMALY_DETECTED = "anomaly_detected"
    LOW_CONFIDENCE = "low_confidence"
    ERROR_OCCURRED = "error_occurred"


class ImprovementPriority(str, Enum):
    """Priority levels for improvement actions."""

    CRITICAL = "critical"  # Must fix immediately
    HIGH = "high"  # Should fix soon
    MEDIUM = "medium"  # Nice to have
    LOW = "low"  # Optional enhancement


@dataclass
class Gap:
    """
    Represents a detected gap or issue in execution.

    Attributes:
        category: Type of gap (e.g., "missed_ports", "incomplete_scan")
        description: Detailed description of the gap
        severity: How critical this gap is (0.0-1.0)
        evidence: Supporting evidence for this gap
        suggested_fix: How to address this gap
    """

    category: str
    description: str
    severity: float
    evidence: list[str] = field(default_factory=list)
    suggested_fix: str = ""

    def __str__(self) -> str:
        return f"[{self.category}] {self.description} (severity: {self.severity:.2f})"


@dataclass
class ImprovementAction:
    """
    Represents a suggested improvement action.

    Attributes:
        action_id: Unique identifier
        action_type: Type of action (e.g., "rescan", "additional_check")
        description: What to do
        tool_name: Tool to use for this action
        parameters: Parameters for the tool
        priority: How important this action is
        expected_benefit: What improvement this will bring
        estimated_time: Estimated execution time (seconds)
    """

    action_id: str
    action_type: str
    description: str
    tool_name: str
    parameters: dict[str, Any]
    priority: ImprovementPriority
    expected_benefit: str
    estimated_time: float = 5.0

    def __str__(self) -> str:
        return f"[{self.priority.value}] {self.description} (ETA: {self.estimated_time}s)"


@dataclass
class ReflectionResult:
    """
    Result of self-reflection analysis.

    Attributes:
        reflection_id: Unique identifier
        task_description: Original task that was executed
        execution_results: Results from task execution
        quality_score: Overall quality assessment (0.0-1.0)
        gaps: List of detected gaps
        improvements: List of suggested improvement actions
        reasoning: LLM's reasoning for this reflection
        trigger: What triggered this reflection
        created_at: Timestamp
        metadata: Additional context
    """

    reflection_id: str
    task_description: str
    execution_results: dict[str, Any]
    quality_score: float
    gaps: list[Gap]
    improvements: list[ImprovementAction]
    reasoning: str
    trigger: ReflectionTrigger
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)

    def has_critical_gaps(self) -> bool:
        """Check if there are any critical gaps."""
        return any(gap.severity >= 0.8 for gap in self.gaps)

    def get_high_priority_actions(self) -> list[ImprovementAction]:
        """Get high and critical priority improvement actions."""
        return [
            action
            for action in self.improvements
            if action.priority in [ImprovementPriority.CRITICAL, ImprovementPriority.HIGH]
        ]

    def get_summary(self) -> dict[str, Any]:
        """Get a summary of reflection results."""
        return {
            "reflection_id": self.reflection_id,
            "task": self.task_description,
            "quality_score": self.quality_score,
            "total_gaps": len(self.gaps),
            "critical_gaps": sum(1 for g in self.gaps if g.severity >= 0.8),
            "total_improvements": len(self.improvements),
            "high_priority_improvements": len(self.get_high_priority_actions()),
            "trigger": self.trigger.value,
        }


class SelfReflection:
    """
    Self-Reflection service for post-execution analysis.

    Enables the agent to critique its own work, identify gaps, and suggest
    improvements for better security assessment quality.

    Example:
        >>> reflection = SelfReflection(llm)
        >>> result = reflection.reflect(
        ...     task="Scan 192.168.1.5",
        ...     execution_results={"open_ports": [80, 443]},
        ...     trigger=ReflectionTrigger.TASK_COMPLETION
        ... )
        >>> print(result.quality_score)
        0.75
        >>> print(result.gaps)
        [Gap: Missed critical ports (22, 3389)]
    """

    # Critical ports that should always be checked
    CRITICAL_PORTS = [21, 22, 23, 25, 80, 443, 445, 3306, 3389, 5432, 8080, 8443]

    # Common security checks
    SECURITY_CHECKS = [
        "service_version_detection",
        "vulnerability_scanning",
        "ssl_certificate_validation",
        "security_header_analysis",
        "authentication_testing",
    ]

    def __init__(
        self,
        llm: BaseChatModel,
        enable_auto_reflection: bool = True,
        quality_threshold: float = 0.7,
    ):
        """
        Initialize the Self-Reflection service.

        Args:
            llm: Language model for reflection analysis
            enable_auto_reflection: Whether to automatically reflect after tasks
            quality_threshold: Minimum quality score to avoid triggering improvements
        """
        self.llm = llm
        self.enable_auto_reflection = enable_auto_reflection
        self.quality_threshold = quality_threshold

        # Reflection history for learning
        self._reflection_history: list[ReflectionResult] = []

        logger.info(
            f"🔍 Self-Reflection initialized (auto: {enable_auto_reflection}, threshold: {quality_threshold})"
        )

    def reflect(
        self,
        task: str,
        execution_results: dict[str, Any],
        trigger: ReflectionTrigger = ReflectionTrigger.TASK_COMPLETION,
        context: Optional[dict[str, Any]] = None,
    ) -> ReflectionResult:
        """
        Perform self-reflection on task execution.

        Args:
            task: Original task description
            execution_results: Results from task execution
            trigger: What triggered this reflection
            context: Optional additional context

        Returns:
            ReflectionResult with quality assessment and improvements
        """
        logger.info(f"🔍 Reflecting on task: {task} (trigger: {trigger.value})")

        # Step 1: Assess quality
        quality_score = self._assess_quality(task, execution_results)

        # Step 2: Detect gaps
        gaps = self._detect_gaps(task, execution_results, context)

        # Step 3: Generate improvements
        improvements = self._generate_improvements(task, execution_results, gaps, context)

        # Step 4: Get LLM reasoning
        reasoning = self._llm_reflect(task, execution_results, gaps, improvements, context)

        # Create reflection result
        reflection_id = self._generate_reflection_id(task)
        result = ReflectionResult(
            reflection_id=reflection_id,
            task_description=task,
            execution_results=execution_results,
            quality_score=quality_score,
            gaps=gaps,
            improvements=improvements,
            reasoning=reasoning,
            trigger=trigger,
            metadata={"context": context or {}},
        )

        # Store in history
        self._reflection_history.append(result)

        # Log summary
        logger.info(
            f"✅ Reflection complete: quality={quality_score:.2f}, "
            f"gaps={len(gaps)}, improvements={len(improvements)}"
        )

        if result.has_critical_gaps():
            logger.warning("⚠️ Critical gaps detected! Review recommended.")

        return result

    def _assess_quality(self, task: str, execution_results: dict[str, Any]) -> float:
        """
        Assess the quality of task execution.

        Returns quality score from 0.0 (poor) to 1.0 (excellent)
        """
        score = 1.0

        # Check for errors
        if execution_results.get("error"):
            score -= 0.5

        # Check for empty results
        if not execution_results or len(execution_results) == 0:
            score -= 0.3

        # Check for incomplete scans (network scanning)
        if "scan" in task.lower():
            open_ports = execution_results.get("open_ports", [])
            if not open_ports:
                score -= 0.2

            # Check if critical ports were scanned
            scanned_ports = set(open_ports)
            critical_ports_checked = sum(1 for port in self.CRITICAL_PORTS if port in scanned_ports)
            if critical_ports_checked < len(self.CRITICAL_PORTS) * 0.5:
                score -= 0.1

        # Check for CVE search quality
        if "cve" in task.lower() or "vulnerability" in task.lower():
            cves = execution_results.get("cves", [])
            if not cves:
                score -= 0.3
            elif len(cves) < 3:
                score -= 0.1

        # Clamp to [0, 1]
        return max(0.0, min(1.0, score))

    def _detect_gaps(
        self, task: str, execution_results: dict[str, Any], context: Optional[dict[str, Any]]
    ) -> list[Gap]:
        """Detect gaps and issues in execution."""
        gaps = []

        # Gap 1: Missed critical ports (for network scans)
        if "scan" in task.lower():
            open_ports = set(execution_results.get("open_ports", []))
            missed_critical = [port for port in self.CRITICAL_PORTS if port not in open_ports]

            if missed_critical:
                gaps.append(
                    Gap(
                        category="missed_ports",
                        description=f"Did not scan critical ports: {missed_critical}",
                        severity=0.7,
                        evidence=[f"Critical ports not in results: {missed_critical}"],
                        suggested_fix="Rescan with focus on critical ports",
                    )
                )

        # Gap 2: Missing service version information
        if "scan" in task.lower():
            services = execution_results.get("services", [])
            if not services:
                gaps.append(
                    Gap(
                        category="missing_service_info",
                        description="No service version information detected",
                        severity=0.6,
                        evidence=["'services' field is empty or missing"],
                        suggested_fix="Run service version detection",
                    )
                )

        # Gap 3: No CVE search performed
        if "scan" in task.lower() or "security" in task.lower():
            cves = execution_results.get("cves", [])
            if not cves:
                gaps.append(
                    Gap(
                        category="no_vulnerability_check",
                        description="No vulnerability/CVE search performed",
                        severity=0.8,
                        evidence=["No CVEs found in results"],
                        suggested_fix="Search for CVEs related to detected services",
                    )
                )

        # Gap 4: Inconsistent results
        if "open_ports" in execution_results and "services" in execution_results:
            num_ports = len(execution_results["open_ports"])
            num_services = len(execution_results["services"])
            if num_ports > 0 and num_services == 0:
                gaps.append(
                    Gap(
                        category="inconsistent_results",
                        description=f"Found {num_ports} open ports but no services identified",
                        severity=0.5,
                        evidence=[f"open_ports: {num_ports}, services: {num_services}"],
                        suggested_fix="Verify service detection on open ports",
                    )
                )

        # Gap 5: Low result count (for CVE searches)
        if "cve" in task.lower() or "vulnerability" in task.lower():
            cves = execution_results.get("cves", [])
            if 0 < len(cves) < 3:
                gaps.append(
                    Gap(
                        category="low_result_count",
                        description=f"Only {len(cves)} CVE(s) found, may be incomplete",
                        severity=0.4,
                        evidence=[f"CVE count: {len(cves)}"],
                        suggested_fix="Broaden search query or try alternative keywords",
                    )
                )

        return gaps

    def _generate_improvements(
        self,
        task: str,
        execution_results: dict[str, Any],
        gaps: list[Gap],
        context: Optional[dict[str, Any]],
    ) -> list[ImprovementAction]:
        """Generate actionable improvement suggestions."""
        improvements = []
        action_counter = 1

        for gap in gaps:
            # Map gaps to improvement actions
            if gap.category == "missed_ports":
                improvements.append(
                    ImprovementAction(
                        action_id=f"improve_{action_counter}",
                        action_type="rescan",
                        description="Rescan critical ports that were missed",
                        tool_name="scan_network",
                        parameters={
                            "target": execution_results.get("target", "unknown"),
                            "ports": ",".join(map(str, self.CRITICAL_PORTS)),
                        },
                        priority=ImprovementPriority.HIGH,
                        expected_benefit="Discover services on critical ports",
                        estimated_time=15.0,
                    )
                )
                action_counter += 1

            elif gap.category == "missing_service_info":
                improvements.append(
                    ImprovementAction(
                        action_id=f"improve_{action_counter}",
                        action_type="service_detection",
                        description="Detect service versions on open ports",
                        tool_name="check_service_version",
                        parameters={
                            "target": execution_results.get("target", "unknown"),
                            "ports": execution_results.get("open_ports", []),
                        },
                        priority=ImprovementPriority.HIGH,
                        expected_benefit="Identify vulnerable service versions",
                        estimated_time=10.0,
                    )
                )
                action_counter += 1

            elif gap.category == "no_vulnerability_check":
                # Extract service names from results
                services = execution_results.get("services", [])
                if services:
                    for service in services[:3]:  # Top 3 services
                        improvements.append(
                            ImprovementAction(
                                action_id=f"improve_{action_counter}",
                                action_type="cve_search",
                                description=f"Search for CVEs affecting {service}",
                                tool_name="search_cve",
                                parameters={"keyword": service},
                                priority=ImprovementPriority.CRITICAL,
                                expected_benefit=f"Discover vulnerabilities in {service}",
                                estimated_time=5.0,
                            )
                        )
                        action_counter += 1
                else:
                    improvements.append(
                        ImprovementAction(
                            action_id=f"improve_{action_counter}",
                            action_type="cve_search",
                            description="Search for general vulnerabilities",
                            tool_name="search_cve",
                            parameters={"keyword": task},
                            priority=ImprovementPriority.MEDIUM,
                            expected_benefit="Discover relevant vulnerabilities",
                            estimated_time=5.0,
                        )
                    )
                    action_counter += 1

            elif gap.category == "low_result_count":
                improvements.append(
                    ImprovementAction(
                        action_id=f"improve_{action_counter}",
                        action_type="query_expansion",
                        description="Broaden CVE search with alternative keywords",
                        tool_name="search_cve",
                        parameters={"keyword": task, "expand_query": True},
                        priority=ImprovementPriority.MEDIUM,
                        expected_benefit="Find additional related CVEs",
                        estimated_time=5.0,
                    )
                )
                action_counter += 1

        return improvements

    def _llm_reflect(
        self,
        task: str,
        execution_results: dict[str, Any],
        gaps: list[Gap],
        improvements: list[ImprovementAction],
        context: Optional[dict[str, Any]],
    ) -> str:
        """Use LLM to provide deeper reflection and reasoning."""
        system_prompt = """You are a security assessment expert performing self-reflection.

Your task is to analyze task execution and provide insightful critique.

Focus on:
1. **Completeness**: Were all necessary checks performed?
2. **Thoroughness**: Was the scan deep enough?
3. **Accuracy**: Are the results consistent and reliable?
4. **Coverage**: Were critical areas examined?
5. **Follow-up**: What additional steps would improve results?

Provide concise, actionable reflection in 2-3 sentences."""

        # Build context
        gaps_str = "\n".join(f"- {gap}" for gap in gaps) if gaps else "None detected"
        improvements_str = (
            "\n".join(f"- {imp}" for imp in improvements) if improvements else "None suggested"
        )

        user_prompt = f"""Reflect on this security assessment:

Task: "{task}"

Execution Results:
{json.dumps(execution_results, indent=2)}

Detected Gaps:
{gaps_str}

Suggested Improvements:
{improvements_str}

Provide your reflection and reasoning."""

        try:
            messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]

            response = self.llm.invoke(messages)
            reasoning = response.content.strip()

            return reasoning

        except Exception as e:
            logger.warning(f"⚠️ LLM reflection failed: {e}")
            return "Reflection analysis completed with detected gaps and improvement suggestions."

    def _generate_reflection_id(self, task: str) -> str:
        """Generate unique reflection ID."""
        import hashlib

        timestamp = datetime.now(timezone.utc).isoformat()
        id_str = f"{task}:{timestamp}"
        return f"reflect_{hashlib.md5(id_str.encode()).hexdigest()[:12]}"

    def get_reflection_history(self, limit: int = 10) -> list[ReflectionResult]:
        """Get recent reflection history."""
        return self._reflection_history[-limit:]

    def get_common_gaps(self) -> dict[str, int]:
        """Analyze reflection history to find common gap patterns."""
        gap_counts = {}
        for reflection in self._reflection_history:
            for gap in reflection.gaps:
                gap_counts[gap.category] = gap_counts.get(gap.category, 0) + 1

        # Sort by frequency
        return dict(sorted(gap_counts.items(), key=lambda x: x[1], reverse=True))

    def get_average_quality_score(self) -> float:
        """Get average quality score across all reflections."""
        if not self._reflection_history:
            return 0.0

        total = sum(r.quality_score for r in self._reflection_history)
        return total / len(self._reflection_history)


# Global instance
_self_reflection: Optional[SelfReflection] = None


def get_self_reflection(llm: BaseChatModel) -> SelfReflection:
    """
    Get or create global SelfReflection instance.

    Args:
        llm: Language model for reflection

    Returns:
        SelfReflection instance
    """
    global _self_reflection
    if _self_reflection is None:
        _self_reflection = SelfReflection(llm)
    return _self_reflection
