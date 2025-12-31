"""
A/B Testing Framework for CVE Reranking.

This module enables data-driven optimization of reranking strategies through:
1. Experiment configuration and management
2. User feedback collection
3. Statistical analysis (t-tests, confidence intervals)
4. Automated winner selection
5. Performance metrics tracking

Design Principles:
- Scientific rigor (statistical significance)
- User-centric (real feedback)
- Automated decision making
- Transparent reporting
"""

import json
import random
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from loguru import logger

try:
    import numpy as np
    from scipy import stats

    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    logger.warning("scipy not available, statistical tests disabled")


class ExperimentStatus(str, Enum):
    """Experiment lifecycle status."""

    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class FeedbackType(str, Enum):
    """User feedback types."""

    THUMBS_UP = "thumbs_up"
    THUMBS_DOWN = "thumbs_down"
    CLICK = "click"  # User clicked on result
    SKIP = "skip"  # User skipped result
    CUSTOM = "custom"  # Custom metric


@dataclass
class ExperimentVariant:
    """A/B test variant configuration."""

    name: str
    description: str
    strategy: str  # RankingStrategy value
    custom_weights: Optional[dict[str, float]] = None
    traffic_allocation: float = 0.5  # 0.0-1.0

    # Metrics
    impressions: int = 0
    clicks: int = 0
    thumbs_up: int = 0
    thumbs_down: int = 0
    avg_position_clicked: float = 0.0

    def __post_init__(self):
        """Validate traffic allocation."""
        if not 0.0 <= self.traffic_allocation <= 1.0:
            raise ValueError("traffic_allocation must be between 0.0 and 1.0")


@dataclass
class Experiment:
    """A/B test experiment configuration."""

    id: str
    name: str
    description: str

    # Variants
    control: ExperimentVariant
    treatment: ExperimentVariant

    # Configuration
    status: ExperimentStatus = ExperimentStatus.DRAFT
    min_sample_size: int = 100  # Minimum samples before analysis
    confidence_level: float = 0.95  # Statistical confidence

    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    winner: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class FeedbackEvent:
    """User feedback event."""

    experiment_id: str
    variant_name: str
    query: str
    cve_id: str
    position: int
    feedback_type: FeedbackType
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)


class ABTestingFramework:
    """
    A/B testing framework for CVE reranking optimization.

    Features:
    - Experiment management (create, start, stop)
    - Traffic splitting
    - Feedback collection
    - Statistical analysis
    - Automated winner selection

    Example:
        >>> framework = ABTestingFramework()
        >>> exp = framework.create_experiment(
        ...     name="Semantic vs Security-First",
        ...     control_strategy="balanced",
        ...     treatment_strategy="security_first"
        ... )
        >>> framework.start_experiment(exp.id)
        >>> variant = framework.assign_variant(exp.id, user_id="user123")
        >>> framework.record_feedback(exp.id, variant, ...)
        >>> results = framework.analyze_experiment(exp.id)
    """

    def __init__(self, storage_backend: Optional[Any] = None):
        """
        Initialize A/B testing framework.

        Args:
            storage_backend: Optional storage backend (Redis, PostgreSQL, etc.)
        """
        self.storage = storage_backend
        self._experiments: dict[str, Experiment] = {}
        self._feedback: dict[str, list[FeedbackEvent]] = {}

        logger.info("A/B Testing Framework initialized")

    def create_experiment(
        self,
        name: str,
        description: str,
        control_strategy: str,
        treatment_strategy: str,
        control_weights: Optional[dict[str, float]] = None,
        treatment_weights: Optional[dict[str, float]] = None,
        traffic_split: float = 0.5,
        min_sample_size: int = 100,
    ) -> Experiment:
        """
        Create a new A/B test experiment.

        Args:
            name: Experiment name
            description: Experiment description
            control_strategy: Control variant strategy
            treatment_strategy: Treatment variant strategy
            control_weights: Optional custom weights for control
            treatment_weights: Optional custom weights for treatment
            traffic_split: Traffic allocation to treatment (0.0-1.0)
            min_sample_size: Minimum samples before analysis

        Returns:
            Created Experiment
        """
        experiment_id = self._generate_experiment_id(name)

        control = ExperimentVariant(
            name="control",
            description=f"Control: {control_strategy}",
            strategy=control_strategy,
            custom_weights=control_weights,
            traffic_allocation=1.0 - traffic_split,
        )

        treatment = ExperimentVariant(
            name="treatment",
            description=f"Treatment: {treatment_strategy}",
            strategy=treatment_strategy,
            custom_weights=treatment_weights,
            traffic_allocation=traffic_split,
        )

        experiment = Experiment(
            id=experiment_id,
            name=name,
            description=description,
            control=control,
            treatment=treatment,
            min_sample_size=min_sample_size,
        )

        self._experiments[experiment_id] = experiment
        self._feedback[experiment_id] = []

        logger.info(f"Created experiment: {experiment_id} ({name})")
        return experiment

    def start_experiment(self, experiment_id: str):
        """Start an experiment."""
        if experiment_id not in self._experiments:
            raise ValueError(f"Experiment {experiment_id} not found")

        experiment = self._experiments[experiment_id]
        experiment.status = ExperimentStatus.RUNNING
        experiment.started_at = datetime.now(timezone.utc).isoformat()

        logger.info(f"Started experiment: {experiment_id}")

    def stop_experiment(self, experiment_id: str):
        """Stop an experiment."""
        if experiment_id not in self._experiments:
            raise ValueError(f"Experiment {experiment_id} not found")

        experiment = self._experiments[experiment_id]
        experiment.status = ExperimentStatus.COMPLETED
        experiment.completed_at = datetime.now(timezone.utc).isoformat()

        logger.info(f"Stopped experiment: {experiment_id}")

    def assign_variant(
        self, experiment_id: str, user_id: Optional[str] = None
    ) -> ExperimentVariant:
        """
        Assign a variant to a user.

        Uses consistent hashing if user_id provided, otherwise random.

        Args:
            experiment_id: Experiment ID
            user_id: Optional user ID for consistent assignment

        Returns:
            Assigned ExperimentVariant
        """
        if experiment_id not in self._experiments:
            raise ValueError(f"Experiment {experiment_id} not found")

        experiment = self._experiments[experiment_id]

        if experiment.status != ExperimentStatus.RUNNING:
            # Default to control if experiment not running
            return experiment.control

        # Determine assignment
        if user_id:
            # Consistent hashing
            hash_val = hash(f"{experiment_id}:{user_id}")
            assignment = (hash_val % 100) / 100.0
        else:
            # Random assignment
            assignment = random.random()

        # Assign based on traffic allocation
        if assignment < experiment.treatment.traffic_allocation:
            return experiment.treatment
        else:
            return experiment.control

    def record_feedback(
        self,
        experiment_id: str,
        variant_name: str,
        query: str,
        cve_id: str,
        position: int,
        feedback_type: FeedbackType,
        metadata: Optional[dict[str, Any]] = None,
    ):
        """
        Record user feedback for a variant.

        Args:
            experiment_id: Experiment ID
            variant_name: Variant name ("control" or "treatment")
            query: Search query
            cve_id: CVE ID that received feedback
            position: Position in results (1-indexed)
            feedback_type: Type of feedback
            metadata: Optional additional metadata
        """
        if experiment_id not in self._experiments:
            raise ValueError(f"Experiment {experiment_id} not found")

        experiment = self._experiments[experiment_id]
        variant = experiment.control if variant_name == "control" else experiment.treatment

        # Update variant metrics
        variant.impressions += 1

        if feedback_type == FeedbackType.CLICK:
            variant.clicks += 1
            # Update average position clicked
            total_clicks = variant.clicks
            variant.avg_position_clicked = (
                variant.avg_position_clicked * (total_clicks - 1) + position
            ) / total_clicks
        elif feedback_type == FeedbackType.THUMBS_UP:
            variant.thumbs_up += 1
        elif feedback_type == FeedbackType.THUMBS_DOWN:
            variant.thumbs_down += 1

        # Record event
        event = FeedbackEvent(
            experiment_id=experiment_id,
            variant_name=variant_name,
            query=query,
            cve_id=cve_id,
            position=position,
            feedback_type=feedback_type,
            metadata=metadata or {},
        )

        self._feedback[experiment_id].append(event)

        logger.debug(f"Recorded feedback: {experiment_id}/{variant_name}/{feedback_type.value}")

    def analyze_experiment(self, experiment_id: str) -> dict[str, Any]:
        """
        Analyze experiment results with statistical tests.

        Args:
            experiment_id: Experiment ID

        Returns:
            Analysis results with metrics and statistical tests
        """
        if experiment_id not in self._experiments:
            raise ValueError(f"Experiment {experiment_id} not found")

        experiment = self._experiments[experiment_id]
        control = experiment.control
        treatment = experiment.treatment

        # Check minimum sample size
        if control.impressions < experiment.min_sample_size:
            logger.warning(
                f"Insufficient samples for control: {control.impressions}/{experiment.min_sample_size}"
            )
        if treatment.impressions < experiment.min_sample_size:
            logger.warning(
                f"Insufficient samples for treatment: {treatment.impressions}/{experiment.min_sample_size}"
            )

        # Calculate metrics
        control_ctr = control.clicks / control.impressions if control.impressions > 0 else 0.0
        treatment_ctr = (
            treatment.clicks / treatment.impressions if treatment.impressions > 0 else 0.0
        )

        control_satisfaction = (
            (control.thumbs_up - control.thumbs_down) / (control.thumbs_up + control.thumbs_down)
            if (control.thumbs_up + control.thumbs_down) > 0
            else 0.0
        )
        treatment_satisfaction = (
            (treatment.thumbs_up - treatment.thumbs_down)
            / (treatment.thumbs_up + treatment.thumbs_down)
            if (treatment.thumbs_up + treatment.thumbs_down) > 0
            else 0.0
        )

        # Statistical tests
        statistical_tests = {}

        if SCIPY_AVAILABLE:
            # Chi-square test for CTR
            if control.impressions > 0 and treatment.impressions > 0:
                contingency_table = [
                    [control.clicks, control.impressions - control.clicks],
                    [treatment.clicks, treatment.impressions - treatment.clicks],
                ]
                chi2, p_value = stats.chi2_contingency(contingency_table)[:2]

                statistical_tests["ctr_chi_square"] = {
                    "chi2": float(chi2),
                    "p_value": float(p_value),
                    "significant": p_value < (1 - experiment.confidence_level),
                }

            # T-test for position clicked
            control_positions = [
                e.position
                for e in self._feedback[experiment_id]
                if e.variant_name == "control" and e.feedback_type == FeedbackType.CLICK
            ]
            treatment_positions = [
                e.position
                for e in self._feedback[experiment_id]
                if e.variant_name == "treatment" and e.feedback_type == FeedbackType.CLICK
            ]

            if len(control_positions) > 1 and len(treatment_positions) > 1:
                t_stat, p_value = stats.ttest_ind(control_positions, treatment_positions)

                statistical_tests["position_t_test"] = {
                    "t_statistic": float(t_stat),
                    "p_value": float(p_value),
                    "significant": p_value < (1 - experiment.confidence_level),
                }

        # Determine winner
        winner = None
        if treatment_ctr > control_ctr * 1.05:  # 5% improvement threshold
            if not statistical_tests or statistical_tests.get("ctr_chi_square", {}).get(
                "significant", False
            ):
                winner = "treatment"
        elif control_ctr > treatment_ctr * 1.05:
            winner = "control"

        # Build results
        results = {
            "experiment_id": experiment_id,
            "name": experiment.name,
            "status": experiment.status.value,
            "control": {
                "strategy": control.strategy,
                "impressions": control.impressions,
                "clicks": control.clicks,
                "ctr": control_ctr,
                "avg_position_clicked": control.avg_position_clicked,
                "thumbs_up": control.thumbs_up,
                "thumbs_down": control.thumbs_down,
                "satisfaction": control_satisfaction,
            },
            "treatment": {
                "strategy": treatment.strategy,
                "impressions": treatment.impressions,
                "clicks": treatment.clicks,
                "ctr": treatment_ctr,
                "avg_position_clicked": treatment.avg_position_clicked,
                "thumbs_up": treatment.thumbs_up,
                "thumbs_down": treatment.thumbs_down,
                "satisfaction": treatment_satisfaction,
            },
            "comparison": {
                "ctr_lift": ((treatment_ctr - control_ctr) / control_ctr * 100)
                if control_ctr > 0
                else 0.0,
                "position_improvement": control.avg_position_clicked
                - treatment.avg_position_clicked,
                "satisfaction_lift": treatment_satisfaction - control_satisfaction,
            },
            "statistical_tests": statistical_tests,
            "winner": winner,
            "recommendation": self._generate_recommendation(
                control_ctr, treatment_ctr, winner, statistical_tests
            ),
        }

        return results

    def get_experiment(self, experiment_id: str) -> Optional[Experiment]:
        """Get experiment by ID."""
        return self._experiments.get(experiment_id)

    def list_experiments(self, status: Optional[ExperimentStatus] = None) -> list[Experiment]:
        """List all experiments, optionally filtered by status."""
        experiments = list(self._experiments.values())

        if status:
            experiments = [e for e in experiments if e.status == status]

        return experiments

    def _generate_experiment_id(self, name: str) -> str:
        """Generate unique experiment ID."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        name_slug = name.lower().replace(" ", "_")[:20]
        return f"exp_{name_slug}_{timestamp}"

    def _generate_recommendation(
        self,
        control_ctr: float,
        treatment_ctr: float,
        winner: Optional[str],
        statistical_tests: dict[str, Any],
    ) -> str:
        """Generate human-readable recommendation."""
        if not winner:
            return "No clear winner. Consider running experiment longer or increasing sample size."

        if winner == "treatment":
            improvement = (
                ((treatment_ctr - control_ctr) / control_ctr * 100) if control_ctr > 0 else 0
            )

            if statistical_tests and statistical_tests.get("ctr_chi_square", {}).get(
                "significant", False
            ):
                return f"✅ Treatment wins with {improvement:.1f}% CTR improvement (statistically significant). Recommend rolling out treatment strategy."
            else:
                return f"⚠️ Treatment shows {improvement:.1f}% CTR improvement, but not statistically significant. Consider longer test."
        else:
            return "❌ Treatment did not outperform control. Keep current strategy."


# Example usage and demo
def demo_ab_testing():
    """Demonstrate A/B testing framework."""
    framework = ABTestingFramework()

    # Create experiment
    exp = framework.create_experiment(
        name="Semantic vs Security-First",
        description="Test if security-first ranking improves user satisfaction",
        control_strategy="balanced",
        treatment_strategy="security_first",
        traffic_split=0.5,
        min_sample_size=50,
    )

    print(f"Created experiment: {exp.id}")

    # Start experiment
    framework.start_experiment(exp.id)

    # Simulate user interactions
    for i in range(100):
        user_id = f"user_{i}"
        variant = framework.assign_variant(exp.id, user_id)

        # Simulate feedback
        if random.random() < 0.3:  # 30% click rate
            framework.record_feedback(
                exp.id,
                variant.name,
                query="Apache vulnerabilities",
                cve_id=f"CVE-2023-{i:05d}",
                position=random.randint(1, 5),
                feedback_type=FeedbackType.CLICK,
            )

        if random.random() < 0.1:  # 10% thumbs up
            framework.record_feedback(
                exp.id,
                variant.name,
                query="Apache vulnerabilities",
                cve_id=f"CVE-2023-{i:05d}",
                position=1,
                feedback_type=FeedbackType.THUMBS_UP,
            )

    # Analyze results
    results = framework.analyze_experiment(exp.id)

    print("\n=== Experiment Results ===")
    print(json.dumps(results, indent=2))

    return framework, exp, results


if __name__ == "__main__":
    demo_ab_testing()
