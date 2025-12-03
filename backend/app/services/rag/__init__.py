"""
Agentic RAG (Retrieval-Augmented Generation) services for CMatrix.

This package implements state-of-the-art RAG techniques for CVE intelligence:
- Query reformulation and expansion
- Multi-hop CVE graph traversal
- Semantic reranking with multi-factor scoring
- A/B testing for continuous optimization
- Self-correcting search loops
- CVE vector store management
"""

from app.services.rag.ab_testing import ABTestingFramework, ExperimentStatus, FeedbackType
from app.services.rag.cve_graph import CVEGraphTraversal
from app.services.rag.cve_reranker import (
    CVEReranker,
    CVEScore,
    RankingStrategy,
    RerankingResult,
    ScoringWeights,
    get_cve_reranker,
)
from app.services.rag.cve_vector_store import (
    CVEMetadata,
    CVESearchResponse,
    CVESearchResult,
    CVEVectorStore,
    CVSSScore,
    CVSSVersion,
    get_cve_vector_store,
)
from app.services.rag.query_reformulator import QueryReformulator, get_query_reformulator

__all__ = [
    # Query Reformulation
    "QueryReformulator",
    "get_query_reformulator",
    # Graph Traversal
    "CVEGraphTraversal",
    # Semantic Reranking
    "CVEReranker",
    "get_cve_reranker",
    "RankingStrategy",
    "ScoringWeights",
    "CVEScore",
    "RerankingResult",
    # A/B Testing
    "ABTestingFramework",
    "ExperimentStatus",
    "FeedbackType",
    # CVE Vector Store
    "CVEVectorStore",
    "CVEMetadata",
    "CVSSScore",
    "CVESearchResult",
    "CVESearchResponse",
    "CVSSVersion",
    "get_cve_vector_store",
]
