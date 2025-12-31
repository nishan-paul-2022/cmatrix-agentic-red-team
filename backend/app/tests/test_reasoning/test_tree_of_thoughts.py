"""
Unit tests for Tree of Thoughts (ToT) Module.
"""

from unittest.mock import Mock

import pytest

from app.services.reasoning.tree_of_thoughts import (
    EvaluationCriterion,
    Strategy,
    StrategyEvaluation,
    StrategyScore,
    StrategyType,
    TreeOfThoughts,
    get_tree_of_thoughts,
)


@pytest.fixture
def mock_llm():
    """Create a mock LLM for testing."""
    llm = Mock()

    # Mock reasoning response
    mock_response = Mock()
    mock_response.content = "Selected Balanced Approach because it provides good coverage in reasonable time, suitable for most security assessment scenarios."
    llm.invoke.return_value = mock_response

    return llm


@pytest.fixture
def tot_service(mock_llm):
    """Create TreeOfThoughts instance."""
    return TreeOfThoughts(llm=mock_llm, default_num_strategies=3, enable_user_learning=True)


class TestStrategyScore:
    """Test StrategyScore dataclass."""

    def test_strategy_score_creation(self):
        """Test creating a strategy score."""
        score = StrategyScore(
            criterion=EvaluationCriterion.SPEED, score=0.85, reasoning="Fast execution"
        )

        assert score.criterion == EvaluationCriterion.SPEED
        assert score.score == 0.85
        assert "Fast" in score.reasoning


class TestStrategy:
    """Test Strategy dataclass."""

    def test_strategy_creation(self):
        """Test creating a strategy."""
        strategy = Strategy(
            strategy_id="strategy_1",
            strategy_type=StrategyType.FAST_SCAN,
            name="Fast Scan",
            description="Quick scan",
            steps=["Step 1", "Step 2"],
            pros=["Fast", "Efficient"],
            cons=["Limited coverage"],
            estimated_duration=300.0,
        )

        assert strategy.strategy_id == "strategy_1"
        assert strategy.strategy_type == StrategyType.FAST_SCAN
        assert len(strategy.steps) == 2
        assert len(strategy.pros) == 2

    def test_get_score(self):
        """Test getting score for criterion."""
        strategy = Strategy(
            strategy_id="test",
            strategy_type=StrategyType.FAST_SCAN,
            name="Test",
            description="Test",
            steps=[],
            pros=[],
            cons=[],
        )

        strategy.scores = [
            StrategyScore(EvaluationCriterion.SPEED, 0.9, "Fast"),
            StrategyScore(EvaluationCriterion.THOROUGHNESS, 0.5, "Limited"),
        ]

        speed_score = strategy.get_score(EvaluationCriterion.SPEED)
        assert speed_score == 0.9

        missing_score = strategy.get_score(EvaluationCriterion.STEALTH)
        assert missing_score is None

    def test_calculate_overall_score_equal_weights(self):
        """Test overall score calculation with equal weights."""
        strategy = Strategy(
            strategy_id="test",
            strategy_type=StrategyType.FAST_SCAN,
            name="Test",
            description="Test",
            steps=[],
            pros=[],
            cons=[],
        )

        strategy.scores = [
            StrategyScore(EvaluationCriterion.SPEED, 0.8, "Fast"),
            StrategyScore(EvaluationCriterion.THOROUGHNESS, 0.6, "Moderate"),
        ]

        overall = strategy.calculate_overall_score()

        # With equal weights: (0.8 + 0.6) / 2 = 0.7
        assert abs(overall - 0.7) < 0.01

    def test_calculate_overall_score_custom_weights(self):
        """Test overall score calculation with custom weights."""
        strategy = Strategy(
            strategy_id="test",
            strategy_type=StrategyType.FAST_SCAN,
            name="Test",
            description="Test",
            steps=[],
            pros=[],
            cons=[],
        )

        strategy.scores = [
            StrategyScore(EvaluationCriterion.SPEED, 0.8, "Fast"),
            StrategyScore(EvaluationCriterion.THOROUGHNESS, 0.6, "Moderate"),
        ]

        weights = {EvaluationCriterion.SPEED: 0.7, EvaluationCriterion.THOROUGHNESS: 0.3}

        overall = strategy.calculate_overall_score(weights)

        # (0.8 * 0.7 + 0.6 * 0.3) / 1.0 = 0.74
        assert abs(overall - 0.74) < 0.01


class TestStrategyEvaluation:
    """Test StrategyEvaluation dataclass."""

    def test_strategy_evaluation_creation(self):
        """Test creating a strategy evaluation."""
        strategies = [
            Strategy(
                strategy_id="1",
                strategy_type=StrategyType.FAST_SCAN,
                name="Fast",
                description="Fast scan",
                steps=[],
                pros=[],
                cons=[],
                overall_score=0.7,
            ),
            Strategy(
                strategy_id="2",
                strategy_type=StrategyType.COMPREHENSIVE,
                name="Comprehensive",
                description="Full scan",
                steps=[],
                pros=[],
                cons=[],
                overall_score=0.9,
            ),
        ]

        evaluation = StrategyEvaluation(
            evaluation_id="eval_1",
            task_description="Test task",
            strategies=strategies,
            selected_strategy=strategies[1],
            selection_reasoning="Best score",
            evaluation_criteria=[EvaluationCriterion.SPEED],
            criterion_weights={EvaluationCriterion.SPEED: 1.0},
        )

        assert evaluation.evaluation_id == "eval_1"
        assert len(evaluation.strategies) == 2
        assert evaluation.selected_strategy.name == "Comprehensive"

    def test_get_strategy_ranking(self):
        """Test getting strategy ranking."""
        strategies = [
            Strategy(
                strategy_id="1",
                strategy_type=StrategyType.FAST_SCAN,
                name="Fast",
                description="Fast",
                steps=[],
                pros=[],
                cons=[],
                overall_score=0.7,
            ),
            Strategy(
                strategy_id="2",
                strategy_type=StrategyType.COMPREHENSIVE,
                name="Comprehensive",
                description="Comprehensive",
                steps=[],
                pros=[],
                cons=[],
                overall_score=0.9,
            ),
            Strategy(
                strategy_id="3",
                strategy_type=StrategyType.BALANCED,
                name="Balanced",
                description="Balanced",
                steps=[],
                pros=[],
                cons=[],
                overall_score=0.8,
            ),
        ]

        evaluation = StrategyEvaluation(
            evaluation_id="test",
            task_description="Test",
            strategies=strategies,
            selected_strategy=strategies[1],
            selection_reasoning="Test",
            evaluation_criteria=[],
            criterion_weights={},
        )

        ranking = evaluation.get_strategy_ranking()

        # Should be sorted by score (descending)
        assert len(ranking) == 3
        assert ranking[0][0].name == "Comprehensive"  # 0.9
        assert ranking[1][0].name == "Balanced"  # 0.8
        assert ranking[2][0].name == "Fast"  # 0.7


class TestTreeOfThoughts:
    """Test TreeOfThoughts service."""

    def test_initialization(self, mock_llm):
        """Test service initialization."""
        service = TreeOfThoughts(llm=mock_llm, default_num_strategies=3, enable_user_learning=True)

        assert service.llm == mock_llm
        assert service.default_num_strategies == 3
        assert service.enable_user_learning

    def test_evaluate_strategies_basic(self, tot_service):
        """Test basic strategy evaluation."""
        evaluation = tot_service.evaluate_strategies(task="Scan network for vulnerabilities")

        assert evaluation is not None
        assert len(evaluation.strategies) > 0
        assert evaluation.selected_strategy is not None
        assert evaluation.selected_strategy.overall_score > 0

    def test_evaluate_strategies_with_preferences(self, tot_service):
        """Test strategy evaluation with user preferences."""
        evaluation = tot_service.evaluate_strategies(
            task="Scan network", user_preferences={"speed": "high"}
        )

        # With speed preference, weights should favor speed
        assert EvaluationCriterion.SPEED in evaluation.criterion_weights
        # Speed weight should be higher than default
        assert evaluation.criterion_weights[EvaluationCriterion.SPEED] > 0.2

    def test_evaluate_strategies_stealth_preference(self, tot_service):
        """Test strategy evaluation with stealth preference."""
        evaluation = tot_service.evaluate_strategies(
            task="Scan network", user_preferences={"stealth": "high"}
        )

        # With stealth preference, stealth weight should be higher
        assert EvaluationCriterion.STEALTH in evaluation.criterion_weights
        assert evaluation.criterion_weights[EvaluationCriterion.STEALTH] > 0.1

    def test_select_strategy_types_fast_task(self, tot_service):
        """Test strategy type selection for fast task."""
        types = tot_service._select_strategy_types("fast scan network", 3)

        # Should include FAST_SCAN
        assert StrategyType.FAST_SCAN in types
        # Should always include BALANCED
        assert StrategyType.BALANCED in types

    def test_select_strategy_types_stealth_task(self, tot_service):
        """Test strategy type selection for stealth task."""
        types = tot_service._select_strategy_types("stealth scan network", 3)

        # Should include STEALTH
        assert StrategyType.STEALTH in types

    def test_select_strategy_types_comprehensive_task(self, tot_service):
        """Test strategy type selection for comprehensive task."""
        types = tot_service._select_strategy_types("comprehensive scan", 3)

        # Should include COMPREHENSIVE
        assert StrategyType.COMPREHENSIVE in types

    def test_score_criterion_speed(self, tot_service):
        """Test scoring speed criterion."""
        fast_strategy = Strategy(
            strategy_id="1",
            strategy_type=StrategyType.FAST_SCAN,
            name="Fast",
            description="Fast",
            steps=[],
            pros=[],
            cons=[],
        )

        slow_strategy = Strategy(
            strategy_id="2",
            strategy_type=StrategyType.STEALTH,
            name="Stealth",
            description="Stealth",
            steps=[],
            pros=[],
            cons=[],
        )

        fast_score, _ = tot_service._score_criterion(
            fast_strategy, EvaluationCriterion.SPEED, "test", None
        )

        slow_score, _ = tot_service._score_criterion(
            slow_strategy, EvaluationCriterion.SPEED, "test", None
        )

        # Fast scan should score higher on speed
        assert fast_score > slow_score

    def test_score_criterion_thoroughness(self, tot_service):
        """Test scoring thoroughness criterion."""
        comprehensive_strategy = Strategy(
            strategy_id="1",
            strategy_type=StrategyType.COMPREHENSIVE,
            name="Comprehensive",
            description="Comprehensive",
            steps=[],
            pros=[],
            cons=[],
        )

        fast_strategy = Strategy(
            strategy_id="2",
            strategy_type=StrategyType.FAST_SCAN,
            name="Fast",
            description="Fast",
            steps=[],
            pros=[],
            cons=[],
        )

        comprehensive_score, _ = tot_service._score_criterion(
            comprehensive_strategy, EvaluationCriterion.THOROUGHNESS, "test", None
        )

        fast_score, _ = tot_service._score_criterion(
            fast_strategy, EvaluationCriterion.THOROUGHNESS, "test", None
        )

        # Comprehensive should score higher on thoroughness
        assert comprehensive_score > fast_score

    def test_score_criterion_stealth(self, tot_service):
        """Test scoring stealth criterion."""
        stealth_strategy = Strategy(
            strategy_id="1",
            strategy_type=StrategyType.STEALTH,
            name="Stealth",
            description="Stealth",
            steps=[],
            pros=[],
            cons=[],
        )

        comprehensive_strategy = Strategy(
            strategy_id="2",
            strategy_type=StrategyType.COMPREHENSIVE,
            name="Comprehensive",
            description="Comprehensive",
            steps=[],
            pros=[],
            cons=[],
        )

        stealth_score, _ = tot_service._score_criterion(
            stealth_strategy, EvaluationCriterion.STEALTH, "test", None
        )

        comprehensive_score, _ = tot_service._score_criterion(
            comprehensive_strategy, EvaluationCriterion.STEALTH, "test", None
        )

        # Stealth should score higher on stealth
        assert stealth_score > comprehensive_score

    def test_preference_learning(self, tot_service):
        """Test user preference learning."""
        # Perform multiple evaluations
        for i in range(3):
            tot_service.evaluate_strategies(
                task=f"Scan network {i}", user_preferences={"speed": "high"}
            )

        insights = tot_service.get_preference_insights()

        assert insights["total_evaluations"] == 3
        assert "strategy_preferences" in insights
        assert "most_preferred" in insights

    def test_get_preference_insights_empty(self, tot_service):
        """Test preference insights with no history."""
        insights = tot_service.get_preference_insights()

        assert "message" in insights


class TestGlobalInstance:
    """Test global instance management."""

    def test_get_tree_of_thoughts(self, mock_llm):
        """Test getting global ToT instance."""
        service1 = get_tree_of_thoughts(mock_llm)
        service2 = get_tree_of_thoughts(mock_llm)

        # Should return same instance
        assert service1 is service2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
