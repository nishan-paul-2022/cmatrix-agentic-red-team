"""
Self-Correcting Loop for Agentic RAG.

This module implements the self-correction mechanism for the CVE search pipeline.
It evaluates the quality of search results and generates improved queries if
the results fall below a certain quality threshold.
"""

import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from loguru import logger

from app.services.llm.providers.base import LLMProvider, Message
from app.services.rag.cve_reranker import RerankingResult


class CorrectionAction(str, Enum):
    """Actions to take for self-correction."""

    NONE = "none"  # Results are good, no action needed
    REFORMULATE = "reformulate"  # Rewrite query with different keywords
    BROADEN = "broaden"  # Remove constraints (e.g., version, vendor)
    NARROW = "narrow"  # Add constraints (e.g., specific product)
    SPLIT = "split"  # Split complex query into sub-queries


@dataclass
class EvaluationResult:
    """Result of evaluating search quality."""

    is_satisfactory: bool
    score: float  # 0.0 to 1.0
    reason: str
    suggested_action: CorrectionAction
    feedback: str


class SelfCorrectionService:
    """
    Service for evaluating and correcting search results.

    Uses an LLM to analyze search results and suggest improvements
    when quality is low.
    """

    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider

    async def evaluate_results(
        self,
        query: str,
        result: RerankingResult,
        min_score_threshold: float = 0.6,
        min_count_threshold: int = 3,
    ) -> EvaluationResult:
        """
        Evaluate the quality of reranked results.

        Args:
            query: The original search query
            result: The reranking result containing ranked CVEs
            min_score_threshold: Minimum acceptable score for the top result
            min_count_threshold: Minimum number of results expected

        Returns:
            EvaluationResult with status and feedback
        """
        # 1. Check if we have any results
        if not result.ranked_cves:
            return EvaluationResult(
                is_satisfactory=False,
                score=0.0,
                reason="No results found",
                suggested_action=CorrectionAction.BROADEN,
                feedback="The search returned no results. Try removing specific versions or constraints.",
            )

        # 2. Analyze top result
        top_cve = result.ranked_cves[0]
        top_score = top_cve.final_score

        # 3. Analyze result count (with decent score)
        decent_results = [c for c in result.ranked_cves if c.final_score >= min_score_threshold]
        count_score = min(len(decent_results) / min_count_threshold, 1.0)

        # 4. Calculate overall quality score
        # Weighted: 70% top result quality, 30% quantity
        quality_score = (top_score * 0.7) + (count_score * 0.3)

        # 5. Determine if satisfactory
        is_satisfactory = top_score >= min_score_threshold

        if is_satisfactory:
            return EvaluationResult(
                is_satisfactory=True,
                score=quality_score,
                reason="Found relevant results",
                suggested_action=CorrectionAction.NONE,
                feedback="Search successful.",
            )

        # 6. If not satisfactory, determine action
        # This is a heuristic evaluation. For more complex cases, we could use LLM here too,
        # but heuristics are faster and cheaper for the initial check.

        action = CorrectionAction.REFORMULATE
        feedback = "Results have low relevance scores."

        if len(result.ranked_cves) < 3:
            action = CorrectionAction.BROADEN
            feedback = "Too few results found. The query might be too specific."
        elif len(result.ranked_cves) > 50 and top_score < 0.4:
            action = CorrectionAction.NARROW
            feedback = "Many results found but none are highly relevant. Query might be too vague."

        return EvaluationResult(
            is_satisfactory=False,
            score=quality_score,
            reason=f"Top score {top_score:.2f} below threshold {min_score_threshold}",
            suggested_action=action,
            feedback=feedback,
        )

    async def generate_correction(
        self, query: str, evaluation: EvaluationResult, history: list[str] = None
    ) -> str:
        """
        Generate a corrected query using LLM.

        Args:
            query: Original query
            evaluation: Evaluation result with feedback
            history: List of previously attempted queries (to avoid loops)

        Returns:
            New query string
        """
        if evaluation.suggested_action == CorrectionAction.NONE:
            return query

        history = history or []

        prompt = f"""You are a Search Query Optimizer for a CVE (Common Vulnerabilities and Exposures) database.

        Goal: Fix a failing search query to find relevant vulnerabilities.

        Original Query: "{query}"
        Problem: {evaluation.feedback}
        Suggested Strategy: {evaluation.suggested_action.value.upper()}
        Previous Attempts: {history}

        Task: Generate a SINGLE improved search query.

        Guidelines:
        - If BROADEN: Remove version numbers, specific vendors, or year constraints.
        - If NARROW: Add "vulnerability", "exploit", or specific product names.
        - If REFORMULATE: Use synonyms (e.g., "RCE" -> "remote code execution").
        - Do NOT output explanations, just the query.
        - Do NOT repeat previous attempts.

        New Query:"""

        try:
            messages = [Message(role="user", content=prompt)]
            response = await asyncio.to_thread(self.llm.invoke, messages)
            new_query = response.strip().strip('"')
            return new_query
        except Exception as e:
            logger.error(f"Failed to generate correction: {e}")
            return query  # Fallback to original


# Global instance factory
_self_correction_service: Optional[SelfCorrectionService] = None


def get_self_correction_service(llm_provider: LLMProvider) -> SelfCorrectionService:
    global _self_correction_service
    if _self_correction_service is None:
        _self_correction_service = SelfCorrectionService(llm_provider)
    return _self_correction_service
