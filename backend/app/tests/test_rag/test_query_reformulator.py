"""
Unit tests for Query Reformulation Engine.

Tests cover:
- Synonym expansion
- CPE extraction
- LLM reformulation
- Caching behavior
- Fallback mechanisms
- Edge cases and error handling
"""

import json
from unittest.mock import MagicMock, Mock, patch

import pytest
from langchain_core.messages import AIMessage

from app.services.rag.query_reformulator import (
    QueryReformulator,
    ReformulatedQuery,
    get_query_reformulator,
)


@pytest.fixture
def mock_llm():
    """Create a mock LLM for testing."""
    llm = Mock()
    return llm


@pytest.fixture
def reformulator(mock_llm):
    """Create a QueryReformulator instance with mocked dependencies."""
    with patch("app.services.rag.query_reformulator.REDIS_AVAILABLE", False):
        return QueryReformulator(llm=mock_llm, enable_cache=False)


@pytest.fixture
def reformulator_with_cache(mock_llm):
    """Create a QueryReformulator with cache enabled."""
    with patch("app.services.rag.query_reformulator.REDIS_AVAILABLE", True):
        with patch("app.services.rag.query_reformulator.Redis") as mock_redis:
            mock_redis_instance = MagicMock()
            mock_redis.return_value = mock_redis_instance

            reformulator = QueryReformulator(llm=mock_llm, enable_cache=True)
            reformulator._cache = mock_redis_instance
            return reformulator


class TestKeywordExtraction:
    """Test security keyword extraction."""

    def test_extract_security_keywords(self, reformulator):
        """Test extraction of security-related keywords."""
        query = "apache vulnerability CVE exploit"
        keywords = reformulator._extract_keywords(query)

        assert "vulnerability" in keywords
        assert "CVE" in keywords
        assert "exploit" in keywords

    def test_extract_no_keywords(self, reformulator):
        """Test query with no security keywords."""
        query = "apache server"
        keywords = reformulator._extract_keywords(query)

        assert len(keywords) == 0

    def test_case_insensitive_extraction(self, reformulator):
        """Test case-insensitive keyword extraction."""
        query = "APACHE VULNERABILITY cve EXPLOIT"
        keywords = reformulator._extract_keywords(query)

        assert len(keywords) >= 2


class TestSynonymExpansion:
    """Test product name synonym expansion."""

    def test_expand_apache_synonyms(self, reformulator):
        """Test Apache product synonym expansion."""
        query = "apache bugs"
        synonyms = reformulator._expand_synonyms(query)

        assert "apache" in synonyms
        assert "Apache HTTP Server" in synonyms["apache"]
        assert "httpd" in synonyms["apache"]

    def test_expand_multiple_products(self, reformulator):
        """Test expansion of multiple product names."""
        query = "apache and nginx vulnerabilities"
        synonyms = reformulator._expand_synonyms(query)

        assert "apache" in synonyms
        assert "nginx" in synonyms

    def test_no_synonyms_found(self, reformulator):
        """Test query with no known products."""
        query = "unknown product vulnerability"
        synonyms = reformulator._expand_synonyms(query)

        assert len(synonyms) == 0


class TestCPEExtraction:
    """Test CPE (Common Platform Enumeration) extraction."""

    def test_extract_cpe_with_version(self, reformulator):
        """Test CPE extraction with version number."""
        query = "apache 2.4.49 vulnerability"
        cpe_candidates = reformulator._extract_cpe_candidates(query)

        assert len(cpe_candidates) > 0
        assert any("2.4.49" in cpe for cpe in cpe_candidates)
        assert any("apache" in cpe for cpe in cpe_candidates)

    def test_extract_cpe_without_version(self, reformulator):
        """Test CPE extraction without version."""
        query = "nginx vulnerability"
        cpe_candidates = reformulator._extract_cpe_candidates(query)

        assert len(cpe_candidates) > 0
        assert any("nginx" in cpe for cpe in cpe_candidates)

    def test_extract_multiple_versions(self, reformulator):
        """Test CPE extraction with multiple versions."""
        query = "apache 2.4.49 and 2.4.50 vulnerabilities"
        cpe_candidates = reformulator._extract_cpe_candidates(query)

        assert len(cpe_candidates) >= 2
        assert any("2.4.49" in cpe for cpe in cpe_candidates)
        assert any("2.4.50" in cpe for cpe in cpe_candidates)


class TestLLMReformulation:
    """Test LLM-based query reformulation."""

    def test_successful_llm_reformulation(self, reformulator, mock_llm):
        """Test successful LLM reformulation."""
        # Mock LLM response
        mock_response = AIMessage(
            content=json.dumps(
                {
                    "reformulated": "Apache HTTP Server vulnerabilities CVE",
                    "explanation": "Expanded 'apache' to full product name and added CVE context",
                    "confidence": 0.85,
                }
            )
        )
        mock_llm.invoke.return_value = mock_response

        reformulated, explanation, confidence = reformulator._llm_reformulate(
            query="apache bugs", keywords=[], synonyms={}, context=None
        )

        assert reformulated == "Apache HTTP Server vulnerabilities CVE"
        assert confidence == 0.85
        assert "Expanded" in explanation

    def test_llm_reformulation_with_markdown(self, reformulator, mock_llm):
        """Test LLM response with markdown code blocks."""
        # Mock LLM response with markdown
        mock_response = AIMessage(
            content="""```json
{
    "reformulated": "nginx 1.21 remote code execution CVE",
    "explanation": "Added security context",
    "confidence": 0.9
}
```"""
        )
        mock_llm.invoke.return_value = mock_response

        reformulated, explanation, confidence = reformulator._llm_reformulate(
            query="nginx 1.21 exploit", keywords=[], synonyms={}, context=None
        )

        assert reformulated == "nginx 1.21 remote code execution CVE"
        assert confidence == 0.9

    def test_llm_reformulation_fallback(self, reformulator, mock_llm):
        """Test fallback when LLM fails."""
        # Mock LLM to raise exception
        mock_llm.invoke.side_effect = Exception("LLM error")

        reformulated, explanation, confidence = reformulator._llm_reformulate(
            query="apache bugs",
            keywords=[],
            synonyms={"apache": ["Apache HTTP Server"]},
            context=None,
        )

        # Should use fallback
        assert "CVE" in reformulated or "vulnerability" in reformulated
        assert confidence < 0.5  # Fallback has lower confidence


class TestValidationAndEnhancement:
    """Test query validation and enhancement."""

    def test_add_cve_keyword(self, reformulator):
        """Test adding CVE keyword when missing."""
        query = "apache vulnerability"
        enhanced = reformulator._validate_and_enhance(query, ["vulnerability"])

        assert "CVE" in enhanced

    def test_remove_excessive_whitespace(self, reformulator):
        """Test whitespace normalization."""
        query = "apache    vulnerability   CVE"
        enhanced = reformulator._validate_and_enhance(query, [])

        assert "  " not in enhanced

    def test_truncate_long_query(self, reformulator):
        """Test truncation of excessively long queries."""
        query = " ".join(["word"] * 100)  # Very long query
        enhanced = reformulator._validate_and_enhance(query, [])

        assert len(enhanced) <= 200


class TestStrategyIdentification:
    """Test reformulation strategy identification."""

    def test_identify_llm_reformulation(self, reformulator):
        """Test identification of LLM reformulation strategy."""
        strategies = reformulator._identify_strategies(
            original="apache bugs",
            reformulated="Apache HTTP Server vulnerabilities CVE",
            cpe_candidates=[],
        )

        assert "llm_reformulation" in strategies

    def test_identify_cve_addition(self, reformulator):
        """Test identification of CVE keyword addition."""
        strategies = reformulator._identify_strategies(
            original="apache bugs", reformulated="apache bugs CVE", cpe_candidates=[]
        )

        assert "cve_keyword_addition" in strategies

    def test_identify_passthrough(self, reformulator):
        """Test identification of passthrough (no changes)."""
        strategies = reformulator._identify_strategies(
            original="apache CVE", reformulated="apache CVE", cpe_candidates=[]
        )

        assert "passthrough" in strategies


class TestCaching:
    """Test caching behavior."""

    def test_cache_miss(self, reformulator_with_cache, mock_llm):
        """Test cache miss scenario."""
        # Mock cache miss
        reformulator_with_cache._cache.get.return_value = None

        # Mock LLM response
        mock_response = AIMessage(
            content=json.dumps(
                {
                    "reformulated": "Apache HTTP Server CVE",
                    "explanation": "Enhanced query",
                    "confidence": 0.8,
                }
            )
        )
        mock_llm.invoke.return_value = mock_response

        result = reformulator_with_cache.reformulate("apache bugs")

        assert result.cached is False
        assert reformulator_with_cache._cache.setex.called

    def test_cache_hit(self, reformulator_with_cache):
        """Test cache hit scenario."""
        # Mock cache hit
        cached_data = {
            "original": "apache bugs",
            "reformulated": "Apache HTTP Server CVE",
            "strategies": ["llm_reformulation"],
            "confidence": 0.8,
            "cpe_candidates": [],
            "keywords": [],
            "synonyms": {},
            "explanation": "Cached result",
            "cached": False,
            "timestamp": "2025-11-27T00:00:00",
        }
        reformulator_with_cache._cache.get.return_value = json.dumps(cached_data)

        result = reformulator_with_cache.reformulate("apache bugs")

        assert result.cached is True
        assert result.reformulated == "Apache HTTP Server CVE"


class TestEndToEnd:
    """End-to-end integration tests."""

    def test_complete_reformulation_flow(self, reformulator, mock_llm):
        """Test complete reformulation flow."""
        # Mock LLM response
        mock_response = AIMessage(
            content=json.dumps(
                {
                    "reformulated": "Apache HTTP Server 2.4.49 remote code execution CVE",
                    "explanation": "Added full product name, security context, and CVE keyword",
                    "confidence": 0.95,
                }
            )
        )
        mock_llm.invoke.return_value = mock_response

        result = reformulator.reformulate("apache 2.4.49 exploit")

        assert isinstance(result, ReformulatedQuery)
        assert result.original == "apache 2.4.49 exploit"
        assert "Apache HTTP Server" in result.reformulated
        assert result.confidence > 0.9
        assert len(result.strategies) > 0
        assert len(result.cpe_candidates) > 0

    def test_reformulation_with_context(self, reformulator, mock_llm):
        """Test reformulation with additional context."""
        # Mock LLM response
        mock_response = AIMessage(
            content=json.dumps(
                {
                    "reformulated": "Apache HTTP Server CVE targeting Linux",
                    "explanation": "Added platform context",
                    "confidence": 0.85,
                }
            )
        )
        mock_llm.invoke.return_value = mock_response

        context = {"platform": "Linux", "target": "192.168.1.100"}
        result = reformulator.reformulate("apache bugs", context=context)

        assert result.confidence > 0.8
        assert mock_llm.invoke.called


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_query(self, reformulator, mock_llm):
        """Test handling of empty query."""
        mock_response = AIMessage(
            content=json.dumps(
                {"reformulated": "", "explanation": "Empty query", "confidence": 0.0}
            )
        )
        mock_llm.invoke.return_value = mock_response

        result = reformulator.reformulate("")

        assert isinstance(result, ReformulatedQuery)

    def test_very_long_query(self, reformulator, mock_llm):
        """Test handling of very long query."""
        long_query = " ".join(["apache"] * 100)

        mock_response = AIMessage(
            content=json.dumps(
                {
                    "reformulated": "Apache HTTP Server CVE",
                    "explanation": "Simplified long query",
                    "confidence": 0.7,
                }
            )
        )
        mock_llm.invoke.return_value = mock_response

        result = reformulator.reformulate(long_query)

        assert len(result.reformulated) <= 200

    def test_special_characters(self, reformulator, mock_llm):
        """Test handling of special characters."""
        query = "apache <script>alert('xss')</script> vulnerability"

        mock_response = AIMessage(
            content=json.dumps(
                {
                    "reformulated": "Apache HTTP Server XSS vulnerability CVE",
                    "explanation": "Cleaned and reformulated",
                    "confidence": 0.8,
                }
            )
        )
        mock_llm.invoke.return_value = mock_response

        result = reformulator.reformulate(query)

        assert isinstance(result, ReformulatedQuery)


class TestGlobalInstance:
    """Test global instance management."""

    def test_get_query_reformulator_singleton(self, mock_llm):
        """Test singleton pattern for global instance."""
        with patch("app.services.rag.query_reformulator.REDIS_AVAILABLE", False):
            instance1 = get_query_reformulator(mock_llm)
            instance2 = get_query_reformulator(mock_llm)

            assert instance1 is instance2
