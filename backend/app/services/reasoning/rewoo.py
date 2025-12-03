"""
ReWOO (Reasoning Without Observation) - Advanced Planning Pattern.

This module implements the ReWOO pattern for upfront planning of complex
security assessment workflows. Instead of iterative reasoning-acting cycles,
ReWOO generates a complete execution plan upfront, then executes it without
re-planning.

Key Benefits:
- 40%+ reduction in LLM calls (plan once, execute many)
- Faster execution (no reasoning overhead during execution)
- Better resource estimation (know full scope upfront)
- Cacheable plans for similar requests

Design Pattern:
1. Planner: Generate complete action plan using LLM
2. Validator: Verify tool availability and parameter validity
3. Executor: Execute plan steps sequentially
4. Cache: Store plans for reuse

References:
- ReWOO Paper: https://arxiv.org/abs/2305.18323
- LangChain ReWOO: https://python.langchain.com/docs/use_cases/more/agents/rewoo
"""

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger

# Try to import Redis for plan caching
try:
    from redis import Redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not available, ReWOO plan caching disabled")


class PlanStatus(str, Enum):
    """Status of a plan or plan step."""

    PENDING = "pending"
    VALIDATING = "validating"
    VALIDATED = "validated"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class PlanStep:
    """
    Represents a single step in an execution plan.

    Attributes:
        step_id: Unique identifier for this step (e.g., "#E1", "#E2")
        tool_name: Name of the tool to execute
        parameters: Parameters to pass to the tool
        description: Human-readable description of what this step does
        dependencies: List of step IDs this step depends on (e.g., ["#E1"])
        expected_output: Description of expected output
        status: Current execution status
        result: Actual execution result (populated after execution)
        error: Error message if execution failed
        execution_time: Time taken to execute (seconds)
    """

    step_id: str
    tool_name: str
    parameters: dict[str, Any]
    description: str
    dependencies: list[str] = field(default_factory=list)
    expected_output: str = ""
    status: PlanStatus = PlanStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None

    def __str__(self) -> str:
        deps = f" (depends on: {', '.join(self.dependencies)})" if self.dependencies else ""
        return f"{self.step_id}: {self.tool_name}({self.parameters}){deps} - {self.description}"


@dataclass
class Plan:
    """
    Represents a complete execution plan.

    Attributes:
        plan_id: Unique identifier for this plan
        task_description: Original task/query that generated this plan
        steps: List of execution steps
        estimated_duration: Estimated total execution time (seconds)
        confidence: Confidence score for plan quality (0.0-1.0)
        reasoning: LLM's reasoning for this plan
        created_at: Timestamp when plan was created
        status: Overall plan status
        cached: Whether this plan came from cache
        metadata: Additional metadata (e.g., user preferences, context)
    """

    plan_id: str
    task_description: str
    steps: list[PlanStep]
    estimated_duration: float
    confidence: float
    reasoning: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: PlanStatus = PlanStatus.PENDING
    cached: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def get_step(self, step_id: str) -> Optional[PlanStep]:
        """Get a step by its ID."""
        for step in self.steps:
            if step.step_id == step_id:
                return step
        return None

    def get_executable_steps(self) -> list[PlanStep]:
        """Get steps that are ready to execute (all dependencies completed)."""
        executable = []
        for step in self.steps:
            if step.status != PlanStatus.PENDING:
                continue

            # Check if all dependencies are completed
            all_deps_completed = all(
                self.get_step(dep_id).status == PlanStatus.COMPLETED
                for dep_id in step.dependencies
                if self.get_step(dep_id) is not None
            )

            if all_deps_completed:
                executable.append(step)

        return executable

    def is_complete(self) -> bool:
        """Check if all steps are completed or skipped."""
        return all(step.status in [PlanStatus.COMPLETED, PlanStatus.SKIPPED] for step in self.steps)

    def has_failures(self) -> bool:
        """Check if any steps failed."""
        return any(step.status == PlanStatus.FAILED for step in self.steps)

    def get_summary(self) -> dict[str, Any]:
        """Get a summary of plan execution."""
        total_steps = len(self.steps)
        completed = sum(1 for s in self.steps if s.status == PlanStatus.COMPLETED)
        failed = sum(1 for s in self.steps if s.status == PlanStatus.FAILED)
        skipped = sum(1 for s in self.steps if s.status == PlanStatus.SKIPPED)
        total_time = sum(s.execution_time or 0 for s in self.steps)

        return {
            "plan_id": self.plan_id,
            "task": self.task_description,
            "total_steps": total_steps,
            "completed": completed,
            "failed": failed,
            "skipped": skipped,
            "pending": total_steps - completed - failed - skipped,
            "total_execution_time": total_time,
            "estimated_duration": self.estimated_duration,
            "status": self.status.value,
            "confidence": self.confidence,
        }


class ReWOOPlanner:
    """
    ReWOO (Reasoning Without Observation) Planner.

    Generates complete execution plans upfront for complex security tasks,
    reducing LLM calls and improving execution efficiency.

    Example:
        >>> planner = ReWOOPlanner(llm, available_tools)
        >>> plan = planner.generate_plan("Scan 192.168.1.0/24 for vulnerabilities")
        >>> print(plan.steps)
        [
            PlanStep(#E1: scan_network(...)),
            PlanStep(#E2: check_service_version(...), depends on #E1),
            PlanStep(#E3: search_cve(...), depends on #E2)
        ]
    """

    # Plan templates for common scenarios (for faster generation)
    PLAN_TEMPLATES = {
        "network_scan": {
            "pattern": r"scan.*network|port.*scan|network.*discovery",
            "template": [
                {"tool": "scan_network", "description": "Discover hosts and open ports"},
                {"tool": "check_service_version", "description": "Identify service versions"},
                {"tool": "search_cve", "description": "Search for vulnerabilities"},
            ],
        },
        "web_assessment": {
            "pattern": r"web.*security|http.*scan|website.*test",
            "template": [
                {"tool": "validate_http_url", "description": "Validate target URL"},
                {"tool": "analyze_http_headers", "description": "Analyze security headers"},
                {"tool": "search_cve", "description": "Check for web vulnerabilities"},
            ],
        },
        "cve_research": {
            "pattern": r"cve.*search|vulnerability.*research|exploit.*lookup",
            "template": [
                {"tool": "search_cve", "description": "Search CVE database"},
                {"tool": "get_cve_details", "description": "Get detailed CVE information"},
            ],
        },
    }

    def __init__(
        self,
        llm: BaseChatModel,
        available_tools: dict[str, dict[str, Any]],
        cache_ttl: int = 7200,  # 2 hours
        enable_cache: bool = True,
        enable_templates: bool = True,
    ):
        """
        Initialize the ReWOO Planner.

        Args:
            llm: Language model for plan generation
            available_tools: Dictionary of available tools with their schemas
                Format: {tool_name: {description, parameters, ...}}
            cache_ttl: Cache time-to-live in seconds
            enable_cache: Whether to enable plan caching
            enable_templates: Whether to use plan templates for common scenarios
        """
        self.llm = llm
        self.available_tools = available_tools
        self.cache_ttl = cache_ttl
        self.enable_cache = enable_cache and REDIS_AVAILABLE
        self.enable_templates = enable_templates

        # Initialize cache
        if self.enable_cache:
            try:
                from app.core.config import settings

                self._cache = Redis(
                    host=settings.CELERY_BROKER_URL.split("//")[1].split(":")[0],
                    port=6379,
                    db=3,  # Use db 3 for reasoning caching
                    decode_responses=True,
                )
                logger.info("✅ Redis cache initialized for ReWOO planning")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize Redis cache: {e}")
                self._cache = None
                self.enable_cache = False
        else:
            self._cache = None

        logger.info(f"🧠 ReWOO Planner initialized with {len(available_tools)} tools")

    def generate_plan(
        self, task: str, context: Optional[dict[str, Any]] = None, max_steps: int = 10
    ) -> Plan:
        """
        Generate an execution plan for a given task.

        Args:
            task: Task description (e.g., "Scan 192.168.1.0/24 for vulnerabilities")
            context: Optional context (e.g., previous results, user preferences)
            max_steps: Maximum number of steps in the plan

        Returns:
            Complete execution plan
        """
        # Check cache first
        if self.enable_cache and self._cache:
            cached_plan = self._get_from_cache(task, context)
            if cached_plan:
                logger.info(f"📦 Cache hit for task: {task}")
                return cached_plan

        logger.info(f"🎯 Generating plan for: {task}")

        # Try template-based planning first (faster)
        if self.enable_templates:
            template_plan = self._try_template_planning(task, context)
            if template_plan:
                logger.info("⚡ Used template-based planning (fast path)")
                if self.enable_cache and self._cache:
                    self._save_to_cache(task, context, template_plan)
                return template_plan

        # Fall back to LLM-based planning
        plan = self._llm_generate_plan(task, context, max_steps)

        # Validate plan
        plan = self._validate_plan(plan)

        # Cache plan
        if self.enable_cache and self._cache:
            self._save_to_cache(task, context, plan)

        logger.info(
            f"✅ Generated plan with {len(plan.steps)} steps (confidence: {plan.confidence:.2f})"
        )
        return plan

    def _try_template_planning(
        self, task: str, context: Optional[dict[str, Any]]
    ) -> Optional[Plan]:
        """Try to generate a plan using templates."""
        task_lower = task.lower()

        for template_name, template_config in self.PLAN_TEMPLATES.items():
            pattern = template_config["pattern"]
            if re.search(pattern, task_lower):
                logger.debug(f"Matched template: {template_name}")

                # Build plan from template
                steps = []
                for i, step_template in enumerate(template_config["template"]):
                    step_id = f"#E{i+1}"
                    dependencies = [f"#E{i}"] if i > 0 else []

                    # Extract parameters from task (simplified)
                    parameters = self._extract_parameters_from_task(task, step_template["tool"])

                    step = PlanStep(
                        step_id=step_id,
                        tool_name=step_template["tool"],
                        parameters=parameters,
                        description=step_template["description"],
                        dependencies=dependencies,
                        expected_output=f"Results from {step_template['tool']}",
                    )
                    steps.append(step)

                plan_id = self._generate_plan_id(task)
                plan = Plan(
                    plan_id=plan_id,
                    task_description=task,
                    steps=steps,
                    estimated_duration=len(steps) * 5.0,  # 5s per step estimate
                    confidence=0.85,  # Template-based plans have good confidence
                    reasoning=f"Used template: {template_name}",
                    metadata={"template": template_name, "context": context or {}},
                )

                return plan

        return None

    def _extract_parameters_from_task(self, task: str, tool_name: str) -> dict[str, Any]:
        """Extract tool parameters from task description."""
        parameters = {}

        # Extract IP addresses/networks
        ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b"
        ips = re.findall(ip_pattern, task)
        if ips and tool_name in ["scan_network", "validate_http_url"]:
            parameters["target"] = ips[0]

        # Extract URLs
        url_pattern = r"https?://[^\s]+"
        urls = re.findall(url_pattern, task)
        if urls and tool_name == "validate_http_url":
            parameters["url"] = urls[0]

        # Extract port ranges
        port_pattern = r"\b(\d+)-(\d+)\b"
        ports = re.findall(port_pattern, task)
        if ports and tool_name == "scan_network":
            parameters["ports"] = f"{ports[0][0]}-{ports[0][1]}"

        # Extract CVE IDs
        cve_pattern = r"CVE-\d{4}-\d{4,7}"
        cves = re.findall(cve_pattern, task, re.IGNORECASE)
        if cves and tool_name in ["search_cve", "get_cve_details"]:
            parameters["cve_id"] = cves[0]

        # Extract keywords for CVE search
        if tool_name == "search_cve" and "keyword" not in parameters:
            # Use task as keyword if no specific CVE ID
            parameters["keyword"] = task

        return parameters

    def _llm_generate_plan(
        self, task: str, context: Optional[dict[str, Any]], max_steps: int
    ) -> Plan:
        """Generate plan using LLM."""
        system_prompt = f"""You are an expert security assessment planner.

Your task is to create a complete, executable plan for security assessment tasks.

Available Tools:
{self._format_tools_for_prompt()}

Planning Guidelines:
1. **Break down complex tasks** into sequential steps
2. **Use dependencies** when a step needs results from previous steps
3. **Be specific** with parameters (extract from task description)
4. **Estimate realistically** (network scans: 10-30s, CVE search: 2-5s, etc.)
5. **Plan completely** - include all necessary steps upfront
6. **Maximum {max_steps} steps** - be concise but thorough
7. **Use step references** like #E1, #E2 for dependencies

Output Format (JSON):
{{
    "steps": [
        {{
            "step_id": "#E1",
            "tool_name": "scan_network",
            "parameters": {{"target": "192.168.1.0/24", "ports": "1-1000"}},
            "description": "Discover hosts and open ports in network",
            "dependencies": [],
            "expected_output": "List of hosts with open ports"
        }},
        {{
            "step_id": "#E2",
            "tool_name": "check_service_version",
            "parameters": {{"target": "#E1.hosts", "port": "#E1.ports"}},
            "description": "Identify service versions on discovered ports",
            "dependencies": ["#E1"],
            "expected_output": "Service names and versions"
        }}
    ],
    "estimated_duration": 45.0,
    "confidence": 0.9,
    "reasoning": "This plan systematically scans the network, identifies services, and checks for vulnerabilities"
}}

Confidence Scoring:
- 0.9-1.0: Complete plan with all necessary steps
- 0.7-0.9: Good plan, may need minor adjustments
- 0.5-0.7: Moderate plan, some uncertainty
- 0.3-0.5: Basic plan, significant gaps
"""

        # Build context string
        context_str = ""
        if context:
            context_str = f"\n\nContext:\n{json.dumps(context, indent=2)}"

        user_prompt = f"""Create an execution plan for this task:

Task: "{task}"{context_str}

Provide your response as JSON with 'steps', 'estimated_duration', 'confidence', and 'reasoning' fields."""

        try:
            messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]

            response = self.llm.invoke(messages)
            content = response.content

            # Parse JSON response
            json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", content, re.DOTALL)
            if json_match:
                content = json_match.group(1)

            result = json.loads(content)

            # Build Plan object
            steps = [
                PlanStep(
                    step_id=s["step_id"],
                    tool_name=s["tool_name"],
                    parameters=s["parameters"],
                    description=s["description"],
                    dependencies=s.get("dependencies", []),
                    expected_output=s.get("expected_output", ""),
                )
                for s in result["steps"]
            ]

            plan_id = self._generate_plan_id(task)
            plan = Plan(
                plan_id=plan_id,
                task_description=task,
                steps=steps,
                estimated_duration=float(result.get("estimated_duration", len(steps) * 5.0)),
                confidence=float(result.get("confidence", 0.7)),
                reasoning=result.get("reasoning", "LLM-generated plan"),
                metadata={"context": context or {}},
            )

            return plan

        except Exception as e:
            logger.error(f"❌ LLM plan generation failed: {e}")
            # Return fallback plan
            return self._create_fallback_plan(task, context)

    def _create_fallback_plan(self, task: str, context: Optional[dict[str, Any]]) -> Plan:
        """Create a simple fallback plan when LLM fails."""
        # Extract basic parameters
        parameters = self._extract_parameters_from_task(task, "scan_network")

        # Create single-step plan
        step = PlanStep(
            step_id="#E1",
            tool_name="scan_network",
            parameters=parameters or {"target": "unknown"},
            description="Execute task (fallback plan)",
            dependencies=[],
            expected_output="Task results",
        )

        plan_id = self._generate_plan_id(task)
        plan = Plan(
            plan_id=plan_id,
            task_description=task,
            steps=[step],
            estimated_duration=10.0,
            confidence=0.3,
            reasoning="Fallback plan - LLM generation failed",
            metadata={"fallback": True, "context": context or {}},
        )

        return plan

    def _validate_plan(self, plan: Plan) -> Plan:
        """Validate plan steps and tool availability."""
        plan.status = PlanStatus.VALIDATING

        for step in plan.steps:
            # Check if tool exists
            if step.tool_name not in self.available_tools:
                logger.warning(f"⚠️ Tool not available: {step.tool_name}")
                step.status = PlanStatus.FAILED
                step.error = f"Tool '{step.tool_name}' not available"
                continue

            # Validate dependencies
            for dep_id in step.dependencies:
                if not plan.get_step(dep_id):
                    logger.warning(f"⚠️ Invalid dependency: {dep_id}")
                    step.status = PlanStatus.FAILED
                    step.error = f"Dependency '{dep_id}' not found"
                    continue

            # Mark as validated if no errors
            if step.status == PlanStatus.PENDING:
                step.status = PlanStatus.VALIDATED

        # Update overall plan status
        if plan.has_failures():
            plan.status = PlanStatus.FAILED
        else:
            plan.status = PlanStatus.VALIDATED

        return plan

    def _format_tools_for_prompt(self) -> str:
        """Format available tools for LLM prompt."""
        tool_descriptions = []
        for tool_name, tool_info in self.available_tools.items():
            desc = tool_info.get("description", "No description")
            params = tool_info.get("parameters", {})
            param_str = ", ".join(f"{k}: {v.get('type', 'any')}" for k, v in params.items())
            tool_descriptions.append(f"- {tool_name}({param_str}): {desc}")

        return "\n".join(tool_descriptions)

    def _generate_plan_id(self, task: str) -> str:
        """Generate unique plan ID."""
        timestamp = datetime.now(timezone.utc).isoformat()
        id_str = f"{task}:{timestamp}"
        return f"plan_{hashlib.md5(id_str.encode()).hexdigest()[:12]}"

    def _get_cache_key(self, task: str, context: Optional[dict[str, Any]]) -> str:
        """Generate cache key for task and context."""
        context_str = json.dumps(context or {}, sort_keys=True)
        key_str = f"{task}:{context_str}"
        return hashlib.md5(key_str.encode()).hexdigest()

    def _get_from_cache(self, task: str, context: Optional[dict[str, Any]]) -> Optional[Plan]:
        """Retrieve plan from cache."""
        if not self._cache:
            return None

        try:
            cache_key = self._get_cache_key(task, context)
            cached_json = self._cache.get(f"rewoo:plan:{cache_key}")

            if cached_json:
                data = json.loads(cached_json)
                # Reconstruct Plan object
                steps = [PlanStep(**s) for s in data["steps"]]
                plan = Plan(
                    plan_id=data["plan_id"],
                    task_description=data["task_description"],
                    steps=steps,
                    estimated_duration=data["estimated_duration"],
                    confidence=data["confidence"],
                    reasoning=data["reasoning"],
                    created_at=data["created_at"],
                    status=PlanStatus(data["status"]),
                    cached=True,
                    metadata=data.get("metadata", {}),
                )
                return plan
        except Exception as e:
            logger.warning(f"⚠️ Cache retrieval failed: {e}")

        return None

    def _save_to_cache(self, task: str, context: Optional[dict[str, Any]], plan: Plan):
        """Save plan to cache."""
        if not self._cache:
            return

        try:
            cache_key = self._get_cache_key(task, context)

            # Convert to dict
            plan_dict = {
                "plan_id": plan.plan_id,
                "task_description": plan.task_description,
                "steps": [asdict(s) for s in plan.steps],
                "estimated_duration": plan.estimated_duration,
                "confidence": plan.confidence,
                "reasoning": plan.reasoning,
                "created_at": plan.created_at,
                "status": plan.status.value,
                "metadata": plan.metadata,
            }

            plan_json = json.dumps(plan_dict)

            self._cache.setex(f"rewoo:plan:{cache_key}", self.cache_ttl, plan_json)
            logger.debug(f"💾 Cached plan: {plan.plan_id}")
        except Exception as e:
            logger.warning(f"⚠️ Cache save failed: {e}")


# Global instance
_rewoo_planner: Optional[ReWOOPlanner] = None


def get_rewoo_planner(
    llm: BaseChatModel, available_tools: dict[str, dict[str, Any]]
) -> ReWOOPlanner:
    """
    Get or create global ReWOO Planner instance.

    Args:
        llm: Language model for planning
        available_tools: Dictionary of available tools

    Returns:
        ReWOOPlanner instance
    """
    global _rewoo_planner
    if _rewoo_planner is None:
        _rewoo_planner = ReWOOPlanner(llm, available_tools)
    return _rewoo_planner
