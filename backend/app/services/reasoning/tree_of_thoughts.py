"""
Tree of Thoughts (ToT) - Multi-Strategy Evaluation and Selection.

This module implements the Tree of Thoughts pattern for evaluating multiple
strategies before execution. Instead of committing to a single approach,
ToT generates multiple candidate strategies, evaluates each, and selects
the optimal one based on task requirements.

Key Benefits:
- Better decision making through multi-strategy comparison
- Explicit trade-off analysis (speed vs thoroughness, stealth vs noise)
- User preference learning and adaptation
- Explainable strategy selection

Design Pattern:
1. Generator: Create multiple candidate strategies
2. Evaluator: Score each strategy against criteria
3. Selector: Choose optimal strategy
4. Explainer: Justify the selection

References:
- Tree of Thoughts Paper: https://arxiv.org/abs/2305.10601
- LangChain ToT: https://python.langchain.com/docs/use_cases/more/agents/tree_of_thoughts
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger


class StrategyType(str, Enum):
    """Types of security assessment strategies."""

    FAST_SCAN = "fast_scan"  # Quick, top ports only
    COMPREHENSIVE = "comprehensive"  # Full coverage, all ports
    STEALTH = "stealth"  # Slow, evasive scanning
    TARGETED = "targeted"  # Focus on specific services/vulnerabilities
    BALANCED = "balanced"  # Balance between speed and coverage


class EvaluationCriterion(str, Enum):
    """Criteria for strategy evaluation."""

    SPEED = "speed"  # How fast will this complete?
    THOROUGHNESS = "thoroughness"  # How complete is the coverage?
    STEALTH = "stealth"  # How likely to avoid detection?
    RESOURCE_USAGE = "resource_usage"  # CPU, memory, network usage
    SUCCESS_PROBABILITY = "success_probability"  # Likelihood of finding issues
    NOISE_LEVEL = "noise_level"  # How much traffic/logs generated


@dataclass
class StrategyScore:
    """
    Score for a specific evaluation criterion.

    Attributes:
        criterion: What is being evaluated
        score: Score from 0.0 (poor) to 1.0 (excellent)
        reasoning: Why this score was given
    """

    criterion: EvaluationCriterion
    score: float
    reasoning: str

    def __str__(self) -> str:
        return f"{self.criterion.value}: {self.score:.2f} - {self.reasoning}"


@dataclass
class Strategy:
    """
    Represents a candidate strategy for task execution.

    Attributes:
        strategy_id: Unique identifier
        strategy_type: Type of strategy
        name: Human-readable name
        description: Detailed description
        steps: Execution steps for this strategy
        pros: Advantages of this strategy
        cons: Disadvantages of this strategy
        scores: Evaluation scores for different criteria
        overall_score: Weighted overall score (0.0-1.0)
        estimated_duration: Expected execution time (seconds)
        estimated_cost: Expected cost (LLM tokens, API calls, etc.)
        metadata: Additional context
    """

    strategy_id: str
    strategy_type: StrategyType
    name: str
    description: str
    steps: list[str]
    pros: list[str]
    cons: list[str]
    scores: list[StrategyScore] = field(default_factory=list)
    overall_score: float = 0.0
    estimated_duration: float = 0.0
    estimated_cost: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def get_score(self, criterion: EvaluationCriterion) -> Optional[float]:
        """Get score for a specific criterion."""
        for score in self.scores:
            if score.criterion == criterion:
                return score.score
        return None

    def calculate_overall_score(
        self, weights: Optional[dict[EvaluationCriterion, float]] = None
    ) -> float:
        """
        Calculate weighted overall score.

        Args:
            weights: Optional custom weights for criteria
                    (default: equal weights)
        """
        if not self.scores:
            return 0.0

        if weights is None:
            # Default equal weights
            weights = {score.criterion: 1.0 for score in self.scores}

        total_weight = sum(weights.values())
        if total_weight == 0:
            return 0.0

        weighted_sum = sum(score.score * weights.get(score.criterion, 0.0) for score in self.scores)

        self.overall_score = weighted_sum / total_weight
        return self.overall_score

    def __str__(self) -> str:
        return f"{self.name} ({self.strategy_type.value}) - Score: {self.overall_score:.2f}"


@dataclass
class StrategyEvaluation:
    """
    Result of strategy evaluation and selection.

    Attributes:
        evaluation_id: Unique identifier
        task_description: Original task
        strategies: All generated strategies
        selected_strategy: The chosen strategy
        selection_reasoning: Why this strategy was selected
        evaluation_criteria: Criteria used for evaluation
        criterion_weights: Weights applied to each criterion
        created_at: Timestamp
        metadata: Additional context
    """

    evaluation_id: str
    task_description: str
    strategies: list[Strategy]
    selected_strategy: Strategy
    selection_reasoning: str
    evaluation_criteria: list[EvaluationCriterion]
    criterion_weights: dict[EvaluationCriterion, float]
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)

    def get_strategy_ranking(self) -> list[tuple[Strategy, float]]:
        """Get strategies ranked by overall score."""
        return sorted(
            [(s, s.overall_score) for s in self.strategies], key=lambda x: x[1], reverse=True
        )

    def get_summary(self) -> dict[str, Any]:
        """Get evaluation summary."""
        ranking = self.get_strategy_ranking()
        return {
            "evaluation_id": self.evaluation_id,
            "task": self.task_description,
            "total_strategies": len(self.strategies),
            "selected": self.selected_strategy.name,
            "selected_score": self.selected_strategy.overall_score,
            "ranking": [{"name": s.name, "score": score} for s, score in ranking],
            "criteria": [c.value for c in self.evaluation_criteria],
        }


class TreeOfThoughts:
    """
    Tree of Thoughts service for multi-strategy evaluation.

    Generates multiple candidate strategies, evaluates each against
    relevant criteria, and selects the optimal strategy for the task.

    Example:
        >>> tot = TreeOfThoughts(llm)
        >>> evaluation = tot.evaluate_strategies(
        ...     task="Scan heavily firewalled network",
        ...     user_preferences={"stealth": "high", "speed": "low"}
        ... )
        >>> print(evaluation.selected_strategy.name)
        "Stealth Scan Strategy"
    """

    # Default evaluation criteria weights
    DEFAULT_WEIGHTS = {
        EvaluationCriterion.SPEED: 0.2,
        EvaluationCriterion.THOROUGHNESS: 0.3,
        EvaluationCriterion.STEALTH: 0.1,
        EvaluationCriterion.RESOURCE_USAGE: 0.1,
        EvaluationCriterion.SUCCESS_PROBABILITY: 0.3,
    }

    # Strategy templates for common scenarios
    STRATEGY_TEMPLATES = {
        StrategyType.FAST_SCAN: {
            "name": "Fast Scan",
            "description": "Quick reconnaissance scan of top ports",
            "steps": [
                "Scan top 100 ports",
                "Basic service detection",
                "Quick CVE lookup for detected services",
            ],
            "pros": ["Very fast (5-10 minutes)", "Low resource usage", "Minimal network noise"],
            "cons": [
                "May miss services on uncommon ports",
                "Limited service version details",
                "Incomplete vulnerability coverage",
            ],
            "estimated_duration": 300.0,  # 5 minutes
        },
        StrategyType.COMPREHENSIVE: {
            "name": "Comprehensive Scan",
            "description": "Full coverage scan of all ports and services",
            "steps": [
                "Scan all 65535 ports",
                "Detailed service version detection",
                "Comprehensive CVE search",
                "Security configuration analysis",
            ],
            "pros": [
                "Complete coverage",
                "Detailed service information",
                "Thorough vulnerability assessment",
            ],
            "cons": [
                "Very slow (30-60 minutes)",
                "High resource usage",
                "Generates significant network traffic",
            ],
            "estimated_duration": 2400.0,  # 40 minutes
        },
        StrategyType.STEALTH: {
            "name": "Stealth Scan",
            "description": "Evasive scanning to avoid detection",
            "steps": [
                "Slow, randomized port scanning",
                "Fragmented packets",
                "Delayed service detection",
                "Passive CVE research",
            ],
            "pros": [
                "Low detection probability",
                "Avoids IDS/IPS triggers",
                "Minimal log footprint",
            ],
            "cons": [
                "Extremely slow (2-4 hours)",
                "May still miss some services",
                "Complex to execute",
            ],
            "estimated_duration": 7200.0,  # 2 hours
        },
        StrategyType.TARGETED: {
            "name": "Targeted Assessment",
            "description": "Focus on specific services or vulnerabilities",
            "steps": [
                "Scan specific ports of interest",
                "Deep service analysis",
                "Targeted CVE research",
                "Exploit verification",
            ],
            "pros": [
                "Efficient use of time",
                "Deep analysis of targets",
                "High success rate for known targets",
            ],
            "cons": [
                "Requires prior knowledge",
                "May miss unexpected vulnerabilities",
                "Limited scope",
            ],
            "estimated_duration": 600.0,  # 10 minutes
        },
        StrategyType.BALANCED: {
            "name": "Balanced Approach",
            "description": "Balance between speed and thoroughness",
            "steps": [
                "Scan top 1000 ports",
                "Service version detection",
                "CVE search with reranking",
                "Priority-based analysis",
            ],
            "pros": [
                "Good coverage in reasonable time",
                "Balanced resource usage",
                "Suitable for most scenarios",
            ],
            "cons": ["Not optimal for any specific requirement", "May miss some edge cases"],
            "estimated_duration": 900.0,  # 15 minutes
        },
    }

    def __init__(
        self, llm: BaseChatModel, default_num_strategies: int = 3, enable_user_learning: bool = True
    ):
        """
        Initialize the Tree of Thoughts service.

        Args:
            llm: Language model for strategy generation and evaluation
            default_num_strategies: Default number of strategies to generate
            enable_user_learning: Whether to learn from user preferences
        """
        self.llm = llm
        self.default_num_strategies = default_num_strategies
        self.enable_user_learning = enable_user_learning

        # User preference history for learning
        self._preference_history: list[dict[str, Any]] = []

        logger.info(f"🌳 Tree of Thoughts initialized (strategies: {default_num_strategies})")

    def evaluate_strategies(
        self,
        task: str,
        num_strategies: Optional[int] = None,
        user_preferences: Optional[dict[str, Any]] = None,
        context: Optional[dict[str, Any]] = None,
    ) -> StrategyEvaluation:
        """
        Generate, evaluate, and select optimal strategy.

        Args:
            task: Task description
            num_strategies: Number of strategies to generate (default: 3)
            user_preferences: User preferences (e.g., {"speed": "high", "stealth": "low"})
            context: Additional context

        Returns:
            StrategyEvaluation with selected strategy
        """
        num_strategies = num_strategies or self.default_num_strategies

        logger.info(f"🌳 Evaluating {num_strategies} strategies for: {task}")

        # Step 1: Generate candidate strategies
        strategies = self._generate_strategies(task, num_strategies, context)

        # Step 2: Determine evaluation criteria and weights
        criteria, weights = self._determine_criteria_and_weights(task, user_preferences)

        # Step 3: Evaluate each strategy
        for strategy in strategies:
            self._evaluate_strategy(strategy, task, criteria, context)
            strategy.calculate_overall_score(weights)

        # Step 4: Select best strategy
        selected = self._select_strategy(strategies, user_preferences)

        # Step 5: Generate selection reasoning
        reasoning = self._generate_reasoning(task, strategies, selected, criteria, weights)

        # Create evaluation result
        evaluation_id = self._generate_evaluation_id(task)
        evaluation = StrategyEvaluation(
            evaluation_id=evaluation_id,
            task_description=task,
            strategies=strategies,
            selected_strategy=selected,
            selection_reasoning=reasoning,
            evaluation_criteria=criteria,
            criterion_weights=weights,
            metadata={"user_preferences": user_preferences or {}, "context": context or {}},
        )

        # Learn from this evaluation
        if self.enable_user_learning:
            self._record_preference(task, selected, user_preferences)

        logger.info(f"✅ Selected: {selected.name} (score: {selected.overall_score:.2f})")

        return evaluation

    def _generate_strategies(
        self, task: str, num_strategies: int, context: Optional[dict[str, Any]]
    ) -> list[Strategy]:
        """Generate candidate strategies."""
        strategies = []

        # Determine which strategy types to generate based on task
        strategy_types = self._select_strategy_types(task, num_strategies)

        for i, strategy_type in enumerate(strategy_types):
            template = self.STRATEGY_TEMPLATES[strategy_type]

            strategy_id = f"strategy_{i+1}"
            strategy = Strategy(
                strategy_id=strategy_id,
                strategy_type=strategy_type,
                name=template["name"],
                description=template["description"],
                steps=template["steps"],
                pros=template["pros"],
                cons=template["cons"],
                estimated_duration=template["estimated_duration"],
                metadata={"template": strategy_type.value},
            )

            strategies.append(strategy)

        return strategies

    def _select_strategy_types(self, task: str, num_strategies: int) -> list[StrategyType]:
        """Select which strategy types to generate based on task."""
        task_lower = task.lower()

        # Always include balanced
        types = [StrategyType.BALANCED]

        # Add task-specific strategies
        if "fast" in task_lower or "quick" in task_lower:
            types.append(StrategyType.FAST_SCAN)
        elif "stealth" in task_lower or "evasive" in task_lower:
            types.append(StrategyType.STEALTH)
        elif "comprehensive" in task_lower or "thorough" in task_lower:
            types.append(StrategyType.COMPREHENSIVE)
        elif "target" in task_lower or "specific" in task_lower:
            types.append(StrategyType.TARGETED)
        else:
            # Default: add fast and comprehensive
            types.extend([StrategyType.FAST_SCAN, StrategyType.COMPREHENSIVE])

        # Limit to requested number
        return types[:num_strategies]

    def _determine_criteria_and_weights(
        self, task: str, user_preferences: Optional[dict[str, Any]]
    ) -> tuple[list[EvaluationCriterion], dict[EvaluationCriterion, float]]:
        """Determine evaluation criteria and their weights."""
        # Start with default criteria
        criteria = list(self.DEFAULT_WEIGHTS.keys())
        weights = self.DEFAULT_WEIGHTS.copy()

        # Adjust weights based on user preferences
        if user_preferences:
            if user_preferences.get("speed") == "high":
                weights[EvaluationCriterion.SPEED] = 0.4
                weights[EvaluationCriterion.THOROUGHNESS] = 0.2
            elif user_preferences.get("thoroughness") == "high":
                weights[EvaluationCriterion.THOROUGHNESS] = 0.4
                weights[EvaluationCriterion.SPEED] = 0.1

            if user_preferences.get("stealth") == "high":
                weights[EvaluationCriterion.STEALTH] = 0.3
                weights[EvaluationCriterion.SPEED] = 0.1

        # Normalize weights to sum to 1.0
        total = sum(weights.values())
        weights = {k: v / total for k, v in weights.items()}

        return criteria, weights

    def _evaluate_strategy(
        self,
        strategy: Strategy,
        task: str,
        criteria: list[EvaluationCriterion],
        context: Optional[dict[str, Any]],
    ):
        """Evaluate a strategy against criteria."""
        for criterion in criteria:
            score, reasoning = self._score_criterion(strategy, criterion, task, context)
            strategy.scores.append(
                StrategyScore(criterion=criterion, score=score, reasoning=reasoning)
            )

    def _score_criterion(
        self,
        strategy: Strategy,
        criterion: EvaluationCriterion,
        task: str,
        context: Optional[dict[str, Any]],
    ) -> tuple[float, str]:
        """Score a strategy for a specific criterion."""
        # Heuristic scoring based on strategy type
        if criterion == EvaluationCriterion.SPEED:
            if strategy.strategy_type == StrategyType.FAST_SCAN:
                return 0.95, "Very fast execution"
            elif strategy.strategy_type == StrategyType.BALANCED:
                return 0.70, "Moderate speed"
            elif strategy.strategy_type == StrategyType.COMPREHENSIVE:
                return 0.30, "Slow due to full coverage"
            elif strategy.strategy_type == StrategyType.STEALTH:
                return 0.10, "Very slow for evasion"
            else:  # TARGETED
                return 0.80, "Fast for focused scope"

        elif criterion == EvaluationCriterion.THOROUGHNESS:
            if strategy.strategy_type == StrategyType.COMPREHENSIVE:
                return 0.95, "Complete coverage"
            elif strategy.strategy_type == StrategyType.BALANCED:
                return 0.75, "Good coverage"
            elif strategy.strategy_type == StrategyType.STEALTH:
                return 0.70, "Thorough but slow"
            elif strategy.strategy_type == StrategyType.TARGETED:
                return 0.60, "Deep but narrow scope"
            else:  # FAST_SCAN
                return 0.40, "Limited coverage"

        elif criterion == EvaluationCriterion.STEALTH:
            if strategy.strategy_type == StrategyType.STEALTH:
                return 0.95, "Designed for evasion"
            elif strategy.strategy_type == StrategyType.FAST_SCAN:
                return 0.60, "Minimal footprint"
            elif strategy.strategy_type == StrategyType.BALANCED:
                return 0.50, "Moderate stealth"
            elif strategy.strategy_type == StrategyType.TARGETED:
                return 0.55, "Focused traffic"
            else:  # COMPREHENSIVE
                return 0.20, "High visibility"

        elif criterion == EvaluationCriterion.SUCCESS_PROBABILITY:
            if strategy.strategy_type == StrategyType.COMPREHENSIVE:
                return 0.90, "Highest chance of finding issues"
            elif strategy.strategy_type == StrategyType.BALANCED:
                return 0.80, "Good success rate"
            elif strategy.strategy_type == StrategyType.STEALTH:
                return 0.75, "Reliable but slow"
            elif strategy.strategy_type == StrategyType.TARGETED:
                return 0.85, "High for known targets"
            else:  # FAST_SCAN
                return 0.60, "May miss some issues"

        elif criterion == EvaluationCriterion.RESOURCE_USAGE:
            if strategy.strategy_type == StrategyType.FAST_SCAN:
                return 0.90, "Minimal resources"
            elif strategy.strategy_type == StrategyType.BALANCED:
                return 0.70, "Moderate usage"
            elif strategy.strategy_type == StrategyType.TARGETED:
                return 0.80, "Efficient"
            elif strategy.strategy_type == StrategyType.STEALTH:
                return 0.85, "Low but sustained"
            else:  # COMPREHENSIVE
                return 0.30, "High resource usage"

        # Default
        return 0.5, "Moderate performance"

    def _select_strategy(
        self, strategies: list[Strategy], user_preferences: Optional[dict[str, Any]]
    ) -> Strategy:
        """Select the best strategy."""
        # Sort by overall score
        sorted_strategies = sorted(strategies, key=lambda s: s.overall_score, reverse=True)

        # Return highest scoring
        return sorted_strategies[0]

    def _generate_reasoning(
        self,
        task: str,
        strategies: list[Strategy],
        selected: Strategy,
        criteria: list[EvaluationCriterion],
        weights: dict[EvaluationCriterion, float],
    ) -> str:
        """Generate explanation for strategy selection."""
        system_prompt = """You are a security assessment strategist.

Explain why a particular strategy was selected for a task.

Focus on:
1. **Key strengths** of the selected strategy
2. **Trade-offs** compared to alternatives
3. **Alignment** with task requirements
4. **Expected outcomes**

Provide concise explanation in 2-3 sentences."""

        # Build strategy comparison
        ranking = sorted(strategies, key=lambda s: s.overall_score, reverse=True)
        comparison = "\n".join(
            f"{i+1}. {s.name}: {s.overall_score:.2f}" for i, s in enumerate(ranking)
        )

        user_prompt = f"""Explain this strategy selection:

Task: "{task}"

Strategies Evaluated:
{comparison}

Selected: {selected.name} (score: {selected.overall_score:.2f})

Key Strengths:
{chr(10).join(f'- {pro}' for pro in selected.pros)}

Provide selection reasoning."""

        try:
            messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]

            response = self.llm.invoke(messages)
            reasoning = response.content.strip()

            return reasoning

        except Exception as e:
            logger.warning(f"⚠️ LLM reasoning generation failed: {e}")
            return f"Selected {selected.name} based on highest overall score ({selected.overall_score:.2f})"

    def _generate_evaluation_id(self, task: str) -> str:
        """Generate unique evaluation ID."""
        import hashlib

        timestamp = datetime.now(timezone.utc).isoformat()
        id_str = f"{task}:{timestamp}"
        return f"eval_{hashlib.md5(id_str.encode()).hexdigest()[:12]}"

    def _record_preference(
        self, task: str, selected_strategy: Strategy, user_preferences: Optional[dict[str, Any]]
    ):
        """Record user preference for learning."""
        self._preference_history.append(
            {
                "task": task,
                "selected_type": selected_strategy.strategy_type.value,
                "preferences": user_preferences or {},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

        # Keep last 100 preferences
        if len(self._preference_history) > 100:
            self._preference_history = self._preference_history[-100:]

    def get_preference_insights(self) -> dict[str, Any]:
        """Analyze preference history for insights."""
        if not self._preference_history:
            return {"message": "No preference history available"}

        # Count strategy type preferences
        type_counts = {}
        for pref in self._preference_history:
            strategy_type = pref["selected_type"]
            type_counts[strategy_type] = type_counts.get(strategy_type, 0) + 1

        # Most common preference
        most_common = max(type_counts.items(), key=lambda x: x[1])

        return {
            "total_evaluations": len(self._preference_history),
            "strategy_preferences": type_counts,
            "most_preferred": most_common[0],
            "preference_rate": most_common[1] / len(self._preference_history),
        }


# Global instance
_tree_of_thoughts: Optional[TreeOfThoughts] = None


def get_tree_of_thoughts(llm: BaseChatModel) -> TreeOfThoughts:
    """
    Get or create global TreeOfThoughts instance.

    Args:
        llm: Language model for strategy evaluation

    Returns:
        TreeOfThoughts instance
    """
    global _tree_of_thoughts
    if _tree_of_thoughts is None:
        _tree_of_thoughts = TreeOfThoughts(llm)
    return _tree_of_thoughts
