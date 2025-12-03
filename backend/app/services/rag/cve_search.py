import asyncio
from typing import Any, Optional

from loguru import logger

from app.services.llm.providers import LLMProvider
from app.services.nvd import fetch_cves_from_nvd
from app.services.rag.cve_reranker import RankingStrategy, get_cve_reranker
from app.services.rag.cve_vector_store import get_cve_vector_store
from app.services.rag.self_correction import get_self_correction_service


class SmartCVESearchService:
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider
        self.reranker = get_cve_reranker()
        self.corrector = get_self_correction_service(llm_provider)
        self.vector_store = get_cve_vector_store()
        self.use_vector_store = True  # Flag to enable/disable vector store

    async def search(
        self,
        query: str,
        limit: int = 10,
        strategy: str = "balanced",
        min_cvss_score: Optional[float] = None,
        severity: Optional[str] = None,
        exploit_available: Optional[bool] = None,
    ) -> dict[str, Any]:
        """
        Execute smart CVE search with self-correction.

        Args:
            query: Search query
            limit: Max results to return
            strategy: Ranking strategy (balanced, semantic_only, security_first, recency_first)
            min_cvss_score: Minimum CVSS score filter
            severity: Severity filter (LOW, MEDIUM, HIGH, CRITICAL)
            exploit_available: Filter by exploit availability

        Returns:
            Dict containing results, metadata, and correction history.
        """
        current_query = query
        query_history = []
        max_retries = 2

        for attempt in range(max_retries + 1):
            # 1. Fetch candidates from vector store or NVD API
            fetch_limit = max(limit * 2, 20)

            if self.use_vector_store:
                try:
                    # Use vector store for fast semantic search
                    vector_response = await self.vector_store.search(
                        query=current_query,
                        limit=fetch_limit,
                        min_cvss_score=min_cvss_score,
                        severity=severity,
                        exploit_available=exploit_available,
                        score_threshold=0.3,
                    )

                    # Convert vector store results to NVD format for compatibility
                    candidates = []
                    for result in vector_response.results:
                        cve_data = {
                            "cve": {
                                "id": result.metadata.cve_id,
                                "descriptions": [
                                    {"lang": "en", "value": result.metadata.description}
                                ],
                                "published": result.metadata.published_date,
                                "lastModified": result.metadata.last_modified_date,
                                "metrics": {},
                                "weaknesses": [],
                                "configurations": [],
                                "references": [{"url": ref} for ref in result.metadata.references],
                            }
                        }

                        # Add CVSS metrics
                        if result.metadata.cvss_v3_1:
                            cve_data["cve"]["metrics"]["cvssMetricV31"] = [
                                {
                                    "cvssData": {
                                        "baseScore": result.metadata.cvss_v3_1.base_score,
                                        "baseSeverity": result.metadata.cvss_v3_1.severity,
                                        "vectorString": result.metadata.cvss_v3_1.vector_string,
                                    }
                                }
                            ]

                        candidates.append(cve_data)

                    logger.info(
                        f"Vector store search: {len(candidates)} candidates in {vector_response.search_time_ms:.2f}ms"
                    )

                except Exception as e:
                    logger.warning(f"Vector store search failed, falling back to NVD API: {e}")
                    candidates = await asyncio.to_thread(
                        fetch_cves_from_nvd, current_query, fetch_limit
                    )
            else:
                # Fallback to NVD API
                candidates = await asyncio.to_thread(
                    fetch_cves_from_nvd, current_query, fetch_limit
                )

            # 2. Rerank
            try:
                strat_enum = RankingStrategy(strategy.lower())
            except ValueError:
                strat_enum = RankingStrategy.BALANCED

            result = await self.reranker.rerank(
                query=current_query, candidates=candidates, strategy=strat_enum, top_k=limit
            )

            # 3. Evaluate
            evaluation = await self.corrector.evaluate_results(current_query, result)

            if evaluation.is_satisfactory or attempt == max_retries:
                return {
                    "query": current_query,
                    "original_query": query,
                    "results": result,
                    "history": query_history,
                    "feedback": evaluation.feedback,
                    "is_corrected": len(query_history) > 0,
                }

            # 4. Correct
            query_history.append(current_query)
            current_query = await self.corrector.generate_correction(
                current_query, evaluation, history=query_history
            )
            logger.info(f"Self-correction: '{query_history[-1]}' -> '{current_query}'")

        return {
            "query": current_query,
            "original_query": query,
            "results": None,
            "history": query_history,
            "feedback": "Max retries exceeded",
            "is_corrected": True,
        }


# Global instance factory
_smart_search_service: Optional[SmartCVESearchService] = None


def get_smart_cve_search_service(llm_provider: LLMProvider) -> SmartCVESearchService:
    global _smart_search_service
    # Note: In a real app, we might want to handle the llm_provider dependency better
    # ensuring we don't overwrite with a different provider if already initialized,
    # or just creating a new one if needed. For now, simple singleton.
    if _smart_search_service is None:
        _smart_search_service = SmartCVESearchService(llm_provider)
    return _smart_search_service
