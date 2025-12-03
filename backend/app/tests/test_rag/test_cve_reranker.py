"""
Unit tests for CVE Reranker.

Tests cover:
- Multi-factor scoring
- Ranking strategies
- Explainable AI
- Caching
- Edge cases
- Performance
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

from app.services.rag.cve_reranker import (
    CVEReranker,
    RankingStrategy,
    ScoringWeights,
    get_cve_reranker,
)


# Sample CVE data for testing
@pytest.fixture
def sample_cves():
    """Sample CVE candidates with varying characteristics."""
    now = datetime.now(timezone.utc)

    return [
        {
            "id": "CVE-2021-44228",  # Log4Shell - recent, high CVSS, exploited
            "descriptions": [{"value": "Apache Log4j2 remote code execution vulnerability"}],
            "published": (now - timedelta(days=15)).isoformat(),
            "metrics": {
                "cvssMetricV31": [{"cvssData": {"baseScore": 10.0, "baseSeverity": "CRITICAL"}}]
            },
            "references": [
                {"url": "https://www.exploit-db.com/exploits/50592", "tags": ["exploit"]},
                {"url": "https://nvd.nist.gov/vuln/detail/CVE-2021-44228"},
            ],
        },
        {
            "id": "CVE-2020-1234",  # Old, medium CVSS, no exploit
            "descriptions": [{"value": "Some old vulnerability in Apache software"}],
            "published": (now - timedelta(days=800)).isoformat(),
            "metrics": {
                "cvssMetricV31": [{"cvssData": {"baseScore": 5.5, "baseSeverity": "MEDIUM"}}]
            },
            "references": [{"url": "https://nvd.nist.gov/vuln/detail/CVE-2020-1234"}],
        },
        {
            "id": "CVE-2022-5678",  # Recent, low CVSS, POC available
            "descriptions": [{"value": "Apache HTTP Server information disclosure"}],
            "published": (now - timedelta(days=60)).isoformat(),
            "metrics": {"cvssMetricV31": [{"cvssData": {"baseScore": 3.7, "baseSeverity": "LOW"}}]},
            "references": [{"url": "https://github.com/user/poc", "tags": ["poc"]}],
        },
        {
            "id": "CVE-2023-9999",  # Very recent, high CVSS, no exploit yet
            "descriptions": [{"value": "Apache Tomcat authentication bypass vulnerability"}],
            "published": (now - timedelta(days=5)).isoformat(),
            "metrics": {
                "cvssMetricV31": [{"cvssData": {"baseScore": 9.1, "baseSeverity": "CRITICAL"}}]
            },
            "references": [{"url": "https://nvd.nist.gov/vuln/detail/CVE-2023-9999"}],
        },
    ]


@pytest.fixture
def reranker():
    """Create a CVEReranker instance for testing."""
    # Disable cache for testing
    return CVEReranker(enable_cache=False)


class TestScoringWeights:
    """Test ScoringWeights configuration."""

    def test_default_weights_sum_to_one(self):
        """Test that default weights sum to 1.0."""
        weights = ScoringWeights()
        total = weights.semantic + weights.cvss + weights.exploit + weights.recency
        assert abs(total - 1.0) < 0.01

    def test_invalid_weights_raise_error(self):
        """Test that invalid weights raise ValueError."""
        with pytest.raises(ValueError):
            ScoringWeights(semantic=0.5, cvss=0.3, exploit=0.1, recency=0.05)

    def test_strategy_presets(self):
        """Test predefined strategy weights."""
        # Semantic only
        weights = ScoringWeights.from_strategy(RankingStrategy.SEMANTIC_ONLY)
        assert weights.semantic == 1.0
        assert weights.cvss == 0.0

        # Security first
        weights = ScoringWeights.from_strategy(RankingStrategy.SECURITY_FIRST)
        assert weights.cvss > weights.semantic

        # Recency first
        weights = ScoringWeights.from_strategy(RankingStrategy.RECENCY_FIRST)
        assert weights.recency > weights.cvss


class TestCVEReranker:
    """Test CVEReranker functionality."""

    @pytest.mark.asyncio
    async def test_rerank_empty_candidates(self, reranker):
        """Test reranking with no candidates."""
        result = await reranker.rerank(
            query="Apache vulnerabilities", candidates=[], strategy=RankingStrategy.BALANCED
        )

        assert result.total_candidates == 0
        assert result.reranked_count == 0
        assert len(result.ranked_cves) == 0

    @pytest.mark.asyncio
    async def test_rerank_basic(self, reranker, sample_cves):
        """Test basic reranking functionality."""
        result = await reranker.rerank(
            query="Apache Log4j remote code execution",
            candidates=sample_cves,
            strategy=RankingStrategy.BALANCED,
        )

        assert result.total_candidates == 4
        assert result.reranked_count == 4
        assert len(result.ranked_cves) == 4

        # Check that CVEs are ranked
        for i, cve in enumerate(result.ranked_cves, start=1):
            assert cve.rank == i

        # Check that scores are in descending order
        scores = [cve.final_score for cve in result.ranked_cves]
        assert scores == sorted(scores, reverse=True)

    @pytest.mark.asyncio
    async def test_semantic_only_strategy(self, reranker, sample_cves):
        """Test semantic-only ranking strategy."""
        result = await reranker.rerank(
            query="Apache Log4j remote code execution",
            candidates=sample_cves,
            strategy=RankingStrategy.SEMANTIC_ONLY,
        )

        # Log4Shell should rank highest (best semantic match)
        assert result.ranked_cves[0].cve_id == "CVE-2021-44228"

        # Verify weights
        assert result.weights.semantic == 1.0
        assert result.weights.cvss == 0.0

    @pytest.mark.asyncio
    async def test_security_first_strategy(self, reranker, sample_cves):
        """Test security-first ranking strategy."""
        result = await reranker.rerank(
            query="Apache vulnerabilities",
            candidates=sample_cves,
            strategy=RankingStrategy.SECURITY_FIRST,
        )

        # High CVSS CVEs should rank higher
        top_cve = result.ranked_cves[0]
        assert top_cve.cve_id in ["CVE-2021-44228", "CVE-2023-9999"]
        assert top_cve.cvss_score >= 0.9  # CVSS 9.0+

    @pytest.mark.asyncio
    async def test_recency_first_strategy(self, reranker, sample_cves):
        """Test recency-first ranking strategy."""
        result = await reranker.rerank(
            query="Apache vulnerabilities",
            candidates=sample_cves,
            strategy=RankingStrategy.RECENCY_FIRST,
        )

        # Most recent CVE should rank highest
        assert result.ranked_cves[0].cve_id == "CVE-2023-9999"
        assert result.ranked_cves[0].recency_score >= 0.9

    @pytest.mark.asyncio
    async def test_custom_weights(self, reranker, sample_cves):
        """Test custom scoring weights."""
        custom_weights = ScoringWeights(
            semantic=0.1,
            cvss=0.1,
            exploit=0.7,  # Prioritize exploits
            recency=0.1,
        )

        result = await reranker.rerank(
            query="Apache vulnerabilities",
            candidates=sample_cves,
            strategy=RankingStrategy.CUSTOM,
            custom_weights=custom_weights,
        )

        # Log4Shell should rank highest (has exploit)
        assert result.ranked_cves[0].cve_id == "CVE-2021-44228"
        assert result.ranked_cves[0].exploit_score > 0.5

    @pytest.mark.asyncio
    async def test_top_k_filtering(self, reranker, sample_cves):
        """Test top-k result filtering."""
        result = await reranker.rerank(
            query="Apache vulnerabilities",
            candidates=sample_cves,
            strategy=RankingStrategy.BALANCED,
            top_k=2,
        )

        assert result.total_candidates == 4
        assert result.reranked_count == 2
        assert len(result.ranked_cves) == 2

    @pytest.mark.asyncio
    async def test_explainable_rankings(self, reranker, sample_cves):
        """Test that rankings include explanations."""
        result = await reranker.rerank(
            query="Apache Log4j", candidates=sample_cves, strategy=RankingStrategy.BALANCED
        )

        for cve in result.ranked_cves:
            assert cve.explanation != ""
            assert "Semantic:" in cve.explanation
            assert "CVSS:" in cve.explanation
            assert "Exploit:" in cve.explanation
            assert "Recency:" in cve.explanation

    def test_cvss_score_extraction(self, reranker, sample_cves):
        """Test CVSS score extraction."""
        scores = reranker._compute_cvss_scores(sample_cves)

        assert len(scores) == 4
        assert scores[0] == 1.0  # CVE-2021-44228 (CVSS 10.0)
        assert scores[1] == 0.55  # CVE-2020-1234 (CVSS 5.5)
        assert scores[2] == 0.37  # CVE-2022-5678 (CVSS 3.7)
        assert scores[3] == 0.91  # CVE-2023-9999 (CVSS 9.1)

    def test_exploit_score_computation(self, reranker, sample_cves):
        """Test exploit availability scoring."""
        scores = reranker._compute_exploit_scores(sample_cves)

        assert len(scores) == 4
        assert scores[0] >= 0.9  # CVE-2021-44228 (exploit-db)
        assert scores[1] == 0.0  # CVE-2020-1234 (no exploit)
        assert scores[2] >= 0.6  # CVE-2022-5678 (POC)
        assert scores[3] == 0.0  # CVE-2023-9999 (no exploit yet)

    def test_recency_score_computation(self, reranker, sample_cves):
        """Test recency scoring."""
        scores = reranker._compute_recency_scores(sample_cves)

        assert len(scores) == 4
        assert scores[0] >= 0.9  # CVE-2021-44228 (15 days old)
        assert scores[1] <= 0.1  # CVE-2020-1234 (800 days old)
        assert scores[2] >= 0.7  # CVE-2022-5678 (60 days old)
        assert scores[3] == 1.0  # CVE-2023-9999 (5 days old)

    @pytest.mark.asyncio
    async def test_fallback_semantic_scoring(self, reranker, sample_cves):
        """Test fallback semantic scoring when model fails."""
        # Mock model to raise exception
        with patch.object(reranker, "_load_model", side_effect=Exception("Model load failed")):
            scores = reranker._fallback_semantic_scores(
                "Apache Log4j remote code execution", sample_cves
            )

            assert len(scores) == 4
            assert all(0.0 <= score <= 1.0 for score in scores)

    @pytest.mark.asyncio
    async def test_max_candidates_limit(self, reranker):
        """Test that reranker limits number of candidates."""
        # Create 150 candidates
        many_candidates = [
            {
                "id": f"CVE-2023-{i:05d}",
                "descriptions": [{"value": f"Vulnerability {i}"}],
                "published": datetime.now(timezone.utc).isoformat(),
                "metrics": {"cvssMetricV31": [{"cvssData": {"baseScore": 5.0}}]},
                "references": [],
            }
            for i in range(150)
        ]

        result = await reranker.rerank(
            query="vulnerabilities", candidates=many_candidates, strategy=RankingStrategy.BALANCED
        )

        # Should be limited to MAX_CANDIDATES (100)
        assert result.total_candidates <= CVEReranker.MAX_CANDIDATES

    @pytest.mark.asyncio
    async def test_execution_time_tracking(self, reranker, sample_cves):
        """Test that execution time is tracked."""
        result = await reranker.rerank(
            query="Apache vulnerabilities",
            candidates=sample_cves,
            strategy=RankingStrategy.BALANCED,
        )

        assert result.execution_time_ms > 0
        assert result.execution_time_ms < 10000  # Should be under 10 seconds

    def test_description_extraction(self, reranker, sample_cves):
        """Test CVE description extraction."""
        desc = reranker._extract_description(sample_cves[0])
        assert "Apache Log4j2" in desc

        # Test fallback
        desc = reranker._extract_description({"id": "CVE-TEST"})
        assert desc == "No description"

    def test_cvss_extraction_fallback(self, reranker):
        """Test CVSS extraction with missing data."""
        cve_no_cvss = {"id": "CVE-TEST", "descriptions": [{"value": "Test"}], "metrics": {}}

        cvss = reranker._extract_cvss(cve_no_cvss)
        assert cvss == 0.0


class TestCaching:
    """Test caching functionality."""

    @pytest.mark.asyncio
    async def test_cache_disabled(self, sample_cves):
        """Test that caching can be disabled."""
        reranker = CVEReranker(enable_cache=False)

        result1 = await reranker.rerank(
            query="Apache Log4j", candidates=sample_cves, strategy=RankingStrategy.BALANCED
        )

        assert result1.cached is False

    @pytest.mark.asyncio
    async def test_cache_key_generation(self, reranker, sample_cves):
        """Test cache key generation."""
        key1 = reranker._get_cache_key("Apache Log4j", sample_cves, RankingStrategy.BALANCED)

        key2 = reranker._get_cache_key("Apache Log4j", sample_cves, RankingStrategy.BALANCED)

        # Same inputs should produce same key
        assert key1 == key2

        # Different strategy should produce different key
        key3 = reranker._get_cache_key("Apache Log4j", sample_cves, RankingStrategy.SEMANTIC_ONLY)
        assert key1 != key3


class TestGlobalInstance:
    """Test global instance management."""

    def test_get_cve_reranker_singleton(self):
        """Test that get_cve_reranker returns singleton."""
        reranker1 = get_cve_reranker()
        reranker2 = get_cve_reranker()

        assert reranker1 is reranker2

    def test_get_cve_reranker_with_params(self):
        """Test get_cve_reranker with custom parameters."""
        reranker = get_cve_reranker(model_name="BAAI/bge-reranker-base", enable_cache=False)

        assert reranker is not None
        assert reranker.model_name == "BAAI/bge-reranker-base"


class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_malformed_cve_data(self, reranker):
        """Test handling of malformed CVE data."""
        malformed = [
            {"id": "CVE-TEST-1"},  # Missing fields
            {"descriptions": [{"value": "Test"}]},  # Missing ID
            {},  # Empty
        ]

        result = await reranker.rerank(
            query="test", candidates=malformed, strategy=RankingStrategy.BALANCED
        )

        # Should not crash
        assert len(result.ranked_cves) == 3

    @pytest.mark.asyncio
    async def test_unicode_in_query(self, reranker, sample_cves):
        """Test handling of Unicode characters."""
        result = await reranker.rerank(
            query="Apache 日本語 vulnerability",
            candidates=sample_cves,
            strategy=RankingStrategy.BALANCED,
        )

        assert len(result.ranked_cves) > 0

    @pytest.mark.asyncio
    async def test_very_long_query(self, reranker, sample_cves):
        """Test handling of very long queries."""
        long_query = "Apache " * 100  # Very long query

        result = await reranker.rerank(
            query=long_query, candidates=sample_cves, strategy=RankingStrategy.BALANCED
        )

        assert len(result.ranked_cves) > 0


class TestResultSerialization:
    """Test result serialization."""

    @pytest.mark.asyncio
    async def test_result_to_dict(self, reranker, sample_cves):
        """Test RerankingResult serialization."""
        result = await reranker.rerank(
            query="Apache Log4j", candidates=sample_cves, strategy=RankingStrategy.BALANCED
        )

        result_dict = result.to_dict()

        assert "query" in result_dict
        assert "strategy" in result_dict
        assert "weights" in result_dict
        assert "ranked_cves" in result_dict
        assert "execution_time_ms" in result_dict

        # Check that it's JSON-serializable
        import json

        json_str = json.dumps(result_dict)
        assert len(json_str) > 0

    @pytest.mark.asyncio
    async def test_cve_score_to_dict(self, reranker, sample_cves):
        """Test CVEScore serialization."""
        result = await reranker.rerank(
            query="Apache Log4j", candidates=sample_cves, strategy=RankingStrategy.BALANCED
        )

        cve_dict = result.ranked_cves[0].to_dict()

        assert "cve_id" in cve_dict
        assert "semantic_score" in cve_dict
        assert "cvss_score" in cve_dict
        assert "exploit_score" in cve_dict
        assert "recency_score" in cve_dict
        assert "final_score" in cve_dict
        assert "rank" in cve_dict
        assert "explanation" in cve_dict


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
