from unittest.mock import AsyncMock, MagicMock

import pytest

from app.services.rag.cve_reranker import CVEScore, RankingStrategy, RerankingResult, ScoringWeights
from app.services.rag.self_correction import (
    CorrectionAction,
    EvaluationResult,
    SelfCorrectionService,
)


@pytest.fixture
def mock_llm():
    llm = MagicMock()
    llm.generate = AsyncMock()
    return llm


@pytest.fixture
def service(mock_llm):
    return SelfCorrectionService(mock_llm)


@pytest.mark.asyncio
async def test_evaluate_results_good(service):
    """Test evaluation of good results."""
    # Create a good result
    cve = CVEScore(
        cve_id="CVE-2021-44228",
        semantic_score=0.9,
        cvss_score=1.0,
        exploit_score=1.0,
        recency_score=0.5,
        final_score=0.85,
        explanation="High scores",
    )

    result = RerankingResult(
        query="log4j",
        strategy=RankingStrategy.BALANCED,
        weights=ScoringWeights(),
        ranked_cves=[cve] * 5,
        total_candidates=5,
        reranked_count=5,
        execution_time_ms=100,
        model_used="test",
    )

    eval_result = await service.evaluate_results("log4j", result)

    assert eval_result.is_satisfactory is True
    assert eval_result.suggested_action == CorrectionAction.NONE


@pytest.mark.asyncio
async def test_evaluate_results_no_results(service):
    """Test evaluation when no results found."""
    result = RerankingResult(
        query="unknown_thing",
        strategy=RankingStrategy.BALANCED,
        weights=ScoringWeights(),
        ranked_cves=[],
        total_candidates=0,
        reranked_count=0,
        execution_time_ms=10,
        model_used="test",
    )

    eval_result = await service.evaluate_results("unknown_thing", result)

    assert eval_result.is_satisfactory is False
    assert eval_result.suggested_action == CorrectionAction.BROADEN


@pytest.mark.asyncio
async def test_evaluate_results_low_score(service):
    """Test evaluation when top score is low."""
    cve = CVEScore(
        cve_id="CVE-2020-1234",
        semantic_score=0.2,
        cvss_score=0.5,
        exploit_score=0.0,
        recency_score=0.1,
        final_score=0.3,  # Below 0.6 threshold
        explanation="Low scores",
    )

    result = RerankingResult(
        query="complex query",
        strategy=RankingStrategy.BALANCED,
        weights=ScoringWeights(),
        ranked_cves=[cve] * 10,
        total_candidates=10,
        reranked_count=10,
        execution_time_ms=100,
        model_used="test",
    )

    eval_result = await service.evaluate_results("complex query", result)

    assert eval_result.is_satisfactory is False
    assert eval_result.suggested_action == CorrectionAction.REFORMULATE


@pytest.mark.asyncio
async def test_generate_correction(service, mock_llm):
    """Test query correction generation."""
    mock_llm.generate.return_value = "corrected query"

    evaluation = EvaluationResult(
        is_satisfactory=False,
        score=0.3,
        reason="Low score",
        suggested_action=CorrectionAction.REFORMULATE,
        feedback="Try synonyms",
    )

    new_query = await service.generate_correction("original", evaluation)

    assert new_query == "corrected query"
    mock_llm.generate.assert_called_once()

    # Verify prompt contains key info
    call_args = mock_llm.generate.call_args[0][0]
    assert "original" in call_args
    assert "REFORMULATE" in call_args
