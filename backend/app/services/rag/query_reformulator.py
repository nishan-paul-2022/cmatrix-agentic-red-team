"""
Query Reformulation Engine for Agentic RAG.

This module transforms vague user queries into precise, effective CVE search queries
using LLM-based reasoning, synonym expansion, and CPE extraction.

Design Principles:
- Semantic understanding over keyword matching
- Multi-strategy reformulation with confidence scoring
- Caching for performance (Redis)
- Graceful degradation (fallback to original query)
- Explainable transformations
"""

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Optional

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger

# Try to import Redis for caching
try:
    from redis import Redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not available, query reformulation caching disabled")


@dataclass
class ReformulatedQuery:
    """
    Represents a reformulated query with metadata.

    Attributes:
        original: Original user query
        reformulated: Enhanced query for CVE search
        strategies: List of strategies applied
        confidence: Confidence score (0.0-1.0)
        cpe_candidates: Extracted CPE strings
        keywords: Extracted security keywords
        synonyms: Expanded synonyms
        explanation: Human-readable explanation of changes
        cached: Whether this result came from cache
    """

    original: str
    reformulated: str
    strategies: list[str]
    confidence: float
    cpe_candidates: list[str]
    keywords: list[str]
    synonyms: dict[str, list[str]]
    explanation: str
    cached: bool = False
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            from datetime import timezone

            self.timestamp = datetime.now(timezone.utc).isoformat()


class QueryReformulator:
    """
    LLM-powered query reformulation engine for CVE search.

    This service enhances user queries through:
    1. Semantic understanding (LLM-based)
    2. Synonym expansion (product names, versions)
    3. CPE extraction and validation
    4. Security keyword identification
    5. Query validation and correction

    Example:
        >>> reformulator = QueryReformulator(llm)
        >>> result = reformulator.reformulate("apache bugs")
        >>> print(result.reformulated)
        "Apache HTTP Server vulnerabilities CVE"
    """

    # Common product name synonyms for CVE search
    PRODUCT_SYNONYMS = {
        "apache": ["Apache HTTP Server", "httpd", "Apache2"],
        "nginx": ["nginx", "nginx web server"],
        "mysql": ["MySQL", "MySQL Server", "MariaDB"],
        "postgres": ["PostgreSQL", "postgres"],
        "ssh": ["OpenSSH", "SSH", "Secure Shell"],
        "ssl": ["OpenSSL", "SSL", "TLS"],
        "java": ["Java", "JRE", "JDK", "OpenJDK"],
        "python": ["Python", "CPython"],
        "node": ["Node.js", "NodeJS"],
        "docker": ["Docker", "Docker Engine"],
        "kubernetes": ["Kubernetes", "k8s"],
        "wordpress": ["WordPress", "WP"],
        "log4j": ["Log4j", "Apache Log4j", "log4j2"],
        "spring": ["Spring Framework", "Spring Boot"],
        "tomcat": ["Apache Tomcat", "Tomcat"],
        "jenkins": ["Jenkins", "Jenkins CI"],
        "redis": ["Redis", "Redis Server"],
        "mongodb": ["MongoDB", "Mongo"],
        "elasticsearch": ["Elasticsearch", "Elastic"],
    }

    # Security-related keywords to emphasize
    SECURITY_KEYWORDS = [
        "vulnerability",
        "CVE",
        "exploit",
        "RCE",
        "XSS",
        "SQLi",
        "authentication bypass",
        "privilege escalation",
        "buffer overflow",
        "denial of service",
        "DoS",
        "information disclosure",
        "CSRF",
        "remote code execution",
        "arbitrary code execution",
        "security flaw",
        "zero-day",
        "patch",
        "security advisory",
        "CVSS",
    ]

    def __init__(self, llm: BaseChatModel, cache_ttl: int = 3600, enable_cache: bool = True):
        """
        Initialize the Query Reformulator.

        Args:
            llm: Language model for semantic reformulation
            cache_ttl: Cache time-to-live in seconds (default: 1 hour)
            enable_cache: Whether to enable Redis caching
        """
        self.llm = llm
        self.cache_ttl = cache_ttl
        self.enable_cache = enable_cache and REDIS_AVAILABLE

        # Initialize cache
        if self.enable_cache:
            try:
                from app.core.config import settings

                self._cache = Redis(
                    host=settings.CELERY_BROKER_URL.split("//")[1].split(":")[0],
                    port=6379,
                    db=3,  # Use db 3 for RAG caching
                    decode_responses=True,
                )
                logger.info("Redis cache initialized for query reformulation")
            except Exception as e:
                logger.warning(f"Failed to initialize Redis cache: {e}")
                self._cache = None
                self.enable_cache = False
        else:
            self._cache = None

        logger.info("Query Reformulator initialized")

    def reformulate(
        self, query: str, context: Optional[dict[str, Any]] = None
    ) -> ReformulatedQuery:
        """
        Reformulate a user query for optimal CVE search.

        Args:
            query: Original user query
            context: Optional context (e.g., previous scan results, target info)

        Returns:
            ReformulatedQuery with enhanced query and metadata
        """
        # Check cache first
        if self.enable_cache and self._cache:
            cached_result = self._get_from_cache(query, context)
            if cached_result:
                logger.debug(f"Cache hit for query: {query}")
                return cached_result

        logger.info(f"Reformulating query: {query}")

        # Step 1: Extract keywords and synonyms
        keywords = self._extract_keywords(query)
        synonyms = self._expand_synonyms(query)

        # Step 2: Extract CPE candidates
        cpe_candidates = self._extract_cpe_candidates(query)

        # Step 3: LLM-based semantic reformulation
        reformulated, explanation, confidence = self._llm_reformulate(
            query, keywords, synonyms, context
        )

        # Step 4: Validate and enhance
        reformulated = self._validate_and_enhance(reformulated, keywords)

        # Step 5: Determine strategies used
        strategies = self._identify_strategies(query, reformulated, cpe_candidates)

        # Create result
        result = ReformulatedQuery(
            original=query,
            reformulated=reformulated,
            strategies=strategies,
            confidence=confidence,
            cpe_candidates=cpe_candidates,
            keywords=keywords,
            synonyms=synonyms,
            explanation=explanation,
            cached=False,
        )

        # Cache result
        if self.enable_cache and self._cache:
            self._save_to_cache(query, context, result)

        logger.info(f"Reformulated: '{query}' → '{reformulated}' (confidence: {confidence:.2f})")
        return result

    def _extract_keywords(self, query: str) -> list[str]:
        """Extract security-related keywords from query."""
        query_lower = query.lower()
        found_keywords = []

        for keyword in self.SECURITY_KEYWORDS:
            if keyword.lower() in query_lower:
                found_keywords.append(keyword)

        return found_keywords

    def _expand_synonyms(self, query: str) -> dict[str, list[str]]:
        """Expand product names to include synonyms."""
        query_lower = query.lower()
        found_synonyms = {}

        for product, synonyms in self.PRODUCT_SYNONYMS.items():
            if product in query_lower:
                found_synonyms[product] = synonyms

        return found_synonyms

    def _extract_cpe_candidates(self, query: str) -> list[str]:
        """
        Extract potential CPE (Common Platform Enumeration) strings.

        CPE format: cpe:2.3:a:vendor:product:version:...
        """
        cpe_candidates = []

        # Look for version numbers (e.g., "2.4.49", "1.21.0")
        version_pattern = r"\b\d+\.\d+(?:\.\d+)*\b"
        versions = re.findall(version_pattern, query)

        # Look for product names
        query_lower = query.lower()
        for product, _synonyms in self.PRODUCT_SYNONYMS.items():
            if product in query_lower:
                # Generate CPE candidates for each version found
                for version in versions:
                    # Simplified CPE (real CPE generation would need vendor lookup)
                    cpe = f"cpe:2.3:a:*:{product}:{version}:*:*:*:*:*:*:*"
                    cpe_candidates.append(cpe)

                # Also add version-agnostic CPE
                if not versions:
                    cpe = f"cpe:2.3:a:*:{product}:*:*:*:*:*:*:*:*"
                    cpe_candidates.append(cpe)

        return cpe_candidates

    def _llm_reformulate(
        self,
        query: str,
        keywords: list[str],
        synonyms: dict[str, list[str]],
        context: Optional[dict[str, Any]],
    ) -> tuple[str, str, float]:
        """
        Use LLM to semantically reformulate the query.

        Returns:
            Tuple of (reformulated_query, explanation, confidence)
        """
        system_prompt = """You are a CVE (Common Vulnerabilities and Exposures) search expert.

Your task is to reformulate user queries into precise, effective CVE search queries.

Guidelines:
1. **Expand abbreviations**: "apache" → "Apache HTTP Server"
2. **Add security context**: "bugs" → "vulnerabilities CVE"
3. **Include product synonyms**: "httpd" → "Apache HTTP Server httpd"
4. **Preserve version numbers**: Keep exact version strings
5. **Add relevant keywords**: Include "CVE", "vulnerability", "security"
6. **Be specific**: Prefer full product names over abbreviations
7. **Keep it concise**: 5-10 words maximum

Examples:
- "apache bugs" → "Apache HTTP Server vulnerabilities CVE"
- "nginx 1.21 exploit" → "nginx 1.21 remote code execution CVE"
- "ssh vulnerability" → "OpenSSH vulnerability CVE security advisory"
- "log4j" → "Apache Log4j log4j2 vulnerability CVE"

Output format (JSON):
{
    "reformulated": "enhanced query here",
    "explanation": "why you made these changes",
    "confidence": 0.85
}

Confidence scoring:
- 0.9-1.0: Very specific query with product name and version
- 0.7-0.9: Good query with product name
- 0.5-0.7: Moderate query with some context
- 0.3-0.5: Vague query, minimal improvement
- 0.0-0.3: Unable to improve query
"""

        # Build context string
        context_str = ""
        if context:
            context_str = f"\n\nAdditional context:\n{json.dumps(context, indent=2)}"

        # Build keyword/synonym hints
        hints = ""
        if keywords:
            hints += f"\nSecurity keywords found: {', '.join(keywords)}"
        if synonyms:
            hints += f"\nProduct synonyms available: {json.dumps(synonyms, indent=2)}"

        user_prompt = f"""Reformulate this CVE search query:

Original query: "{query}"{hints}{context_str}

Provide your response as JSON with 'reformulated', 'explanation', and 'confidence' fields."""

        try:
            messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]

            response = self.llm.invoke(messages)
            content = response.content

            # Parse JSON response
            # Try to extract JSON from markdown code blocks if present
            json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", content, re.DOTALL)
            if json_match:
                content = json_match.group(1)

            result = json.loads(content)

            reformulated = result.get("reformulated", query)
            explanation = result.get("explanation", "LLM reformulation applied")
            confidence = float(result.get("confidence", 0.5))

            # Clamp confidence to [0, 1]
            confidence = max(0.0, min(1.0, confidence))

            return reformulated, explanation, confidence

        except Exception as e:
            logger.warning(f"LLM reformulation failed: {e}, using fallback")
            # Fallback: basic reformulation
            return self._fallback_reformulate(query, keywords, synonyms)

    def _fallback_reformulate(
        self, query: str, keywords: list[str], synonyms: dict[str, list[str]]
    ) -> tuple[str, str, float]:
        """Fallback reformulation without LLM."""
        reformulated = query

        # Add "CVE" if not present
        if "cve" not in query.lower():
            reformulated += " CVE"

        # Add "vulnerability" if no security keywords present
        if not keywords and "vulnerability" not in query.lower():
            reformulated += " vulnerability"

        # Expand first synonym found
        for product, syns in synonyms.items():
            if syns:
                reformulated = reformulated.replace(product, syns[0])
                break

        explanation = "Fallback reformulation: added CVE context"
        confidence = 0.4

        return reformulated, explanation, confidence

    def _validate_and_enhance(self, query: str, keywords: list[str]) -> str:
        """Validate and enhance the reformulated query."""
        # Remove excessive whitespace
        query = " ".join(query.split())

        # Ensure "CVE" is present for CVE searches
        if "cve" not in query.lower() and any(
            k in query.lower() for k in ["vulnerability", "exploit", "security"]
        ):
            query += " CVE"

        # Limit length (NVD API has query length limits)
        max_length = 200
        if len(query) > max_length:
            query = query[:max_length].rsplit(" ", 1)[0]  # Cut at word boundary

        return query.strip()

    def _identify_strategies(
        self, original: str, reformulated: str, cpe_candidates: list[str]
    ) -> list[str]:
        """Identify which reformulation strategies were applied."""
        strategies = []

        if original != reformulated:
            strategies.append("llm_reformulation")

        if "cve" in reformulated.lower() and "cve" not in original.lower():
            strategies.append("cve_keyword_addition")

        if any(syn in reformulated for syns in self.PRODUCT_SYNONYMS.values() for syn in syns):
            strategies.append("synonym_expansion")

        if cpe_candidates:
            strategies.append("cpe_extraction")

        if len(reformulated.split()) > len(original.split()):
            strategies.append("query_expansion")

        return strategies if strategies else ["passthrough"]

    def _get_cache_key(self, query: str, context: Optional[dict[str, Any]]) -> str:
        """Generate cache key for query and context."""
        context_str = json.dumps(context or {}, sort_keys=True)
        key_str = f"{query}:{context_str}"
        return hashlib.md5(key_str.encode()).hexdigest()

    def _get_from_cache(
        self, query: str, context: Optional[dict[str, Any]]
    ) -> Optional[ReformulatedQuery]:
        """Retrieve reformulated query from cache."""
        if not self._cache:
            return None

        try:
            cache_key = self._get_cache_key(query, context)
            cached_json = self._cache.get(f"reformulate:{cache_key}")

            if cached_json:
                data = json.loads(cached_json)
                result = ReformulatedQuery(**data)
                result.cached = True
                return result
        except Exception as e:
            logger.warning(f"Cache retrieval failed: {e}")

        return None

    def _save_to_cache(
        self, query: str, context: Optional[dict[str, Any]], result: ReformulatedQuery
    ):
        """Save reformulated query to cache."""
        if not self._cache:
            return

        try:
            cache_key = self._get_cache_key(query, context)
            result_dict = asdict(result)
            result_json = json.dumps(result_dict)

            self._cache.setex(f"reformulate:{cache_key}", self.cache_ttl, result_json)
        except Exception as e:
            logger.warning(f"Cache save failed: {e}")


# Global instance
_query_reformulator: Optional[QueryReformulator] = None


def get_query_reformulator(llm: BaseChatModel) -> QueryReformulator:
    """
    Get or create global QueryReformulator instance.

    Args:
        llm: Language model for reformulation

    Returns:
        QueryReformulator instance
    """
    global _query_reformulator
    if _query_reformulator is None:
        _query_reformulator = QueryReformulator(llm)
    return _query_reformulator
