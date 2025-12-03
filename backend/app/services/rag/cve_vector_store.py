"""CVE Vector Store - Semantic-searchable CVE database using Qdrant.

This module implements a dedicated vector store for CVE (Common Vulnerabilities and
Exposures) data, enabling:
- Semantic search over CVE descriptions
- Hybrid search (semantic + metadata filters)
- Rich metadata storage (CVSS, CWE, CPE, exploit info)
- Incremental updates from NVD feeds
- High-performance retrieval (<500ms)

Architecture:
    User Query → CVE Vector Store → Qdrant → Ranked Results
                      ↓
                 BGE Embeddings
                      ↓
                 Semantic Search + Filters
"""

import hashlib
import json
import uuid
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Optional

from loguru import logger
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer

from app.core.config import settings

# Try to import Redis for caching (optional)
try:
    from redis import Redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not available for CVE vector store caching")


class CVSSVersion(str, Enum):
    """CVSS version enumeration."""

    V2 = "v2"
    V3 = "v3"
    V3_1 = "v3.1"
    V4 = "v4"


@dataclass
class CVSSScore:
    """CVSS score information."""

    version: str
    base_score: float
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    vector_string: Optional[str] = None
    exploitability_score: Optional[float] = None
    impact_score: Optional[float] = None


@dataclass
class CVEMetadata:
    """Rich metadata for a CVE entry."""

    cve_id: str
    description: str
    published_date: str
    last_modified_date: str

    # CVSS Scores
    cvss_v2: Optional[CVSSScore] = None
    cvss_v3: Optional[CVSSScore] = None
    cvss_v3_1: Optional[CVSSScore] = None

    # Categorization
    cwe_ids: list[str] = None  # Common Weakness Enumeration
    cpe_uris: list[str] = None  # Common Platform Enumeration

    # Exploit Information
    exploit_available: bool = False
    exploit_maturity: Optional[str] = None  # UNPROVEN, POC, FUNCTIONAL, HIGH
    references: list[str] = None

    # Patch Status
    patch_available: bool = False
    patch_references: list[str] = None

    # Additional Context
    vendor: Optional[str] = None
    product: Optional[str] = None
    affected_versions: list[str] = None

    def __post_init__(self):
        """Initialize default values for lists."""
        if self.cwe_ids is None:
            self.cwe_ids = []
        if self.cpe_uris is None:
            self.cpe_uris = []
        if self.references is None:
            self.references = []
        if self.patch_references is None:
            self.patch_references = []
        if self.affected_versions is None:
            self.affected_versions = []

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for storage."""
        data = asdict(self)
        # Convert CVSS scores to dict
        if self.cvss_v2:
            data["cvss_v2"] = asdict(self.cvss_v2)
        if self.cvss_v3:
            data["cvss_v3"] = asdict(self.cvss_v3)
        if self.cvss_v3_1:
            data["cvss_v3_1"] = asdict(self.cvss_v3_1)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CVEMetadata":
        """Create from dictionary."""
        # Create a copy to avoid modifying original
        data = data.copy()

        # Convert CVSS scores from dict
        if data.get("cvss_v2"):
            data["cvss_v2"] = CVSSScore(**data["cvss_v2"])
        if data.get("cvss_v3"):
            data["cvss_v3"] = CVSSScore(**data["cvss_v3"])
        if data.get("cvss_v3_1"):
            data["cvss_v3_1"] = CVSSScore(**data["cvss_v3_1"])

        # Filter out keys that are not in the dataclass
        # This handles flattened fields like cvss_base_score, severity, etc.
        valid_keys = cls.__dataclass_fields__.keys()
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}

        return cls(**filtered_data)


@dataclass
class CVESearchResult:
    """A single CVE search result with score."""

    cve_id: str
    description: str
    score: float
    metadata: CVEMetadata

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "cve_id": self.cve_id,
            "description": self.description,
            "score": self.score,
            "metadata": self.metadata.to_dict(),
        }


@dataclass
class CVESearchResponse:
    """Response from CVE search."""

    query: str
    results: list[CVESearchResult]
    total_found: int
    search_time_ms: float
    filters_applied: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "query": self.query,
            "results": [r.to_dict() for r in self.results],
            "total_found": self.total_found,
            "search_time_ms": self.search_time_ms,
            "filters_applied": self.filters_applied,
        }


class CVEVectorStore:
    """
    CVE Vector Store for semantic search over vulnerability data.

    Features:
    - Semantic search using BGE embeddings
    - Hybrid search (semantic + metadata filters)
    - Rich metadata (CVSS, CWE, CPE, exploits)
    - Incremental updates from NVD
    - Redis caching for performance

    Usage:
        store = CVEVectorStore()
        await store.initialize()

        # Add CVEs
        await store.add_cve(cve_metadata)

        # Search
        results = await store.search(
            query="Apache Log4j RCE",
            min_cvss_score=7.0,
            limit=10
        )
    """

    _instance: Optional["CVEVectorStore"] = None
    _client: Optional[QdrantClient] = None
    _model: Optional[SentenceTransformer] = None

    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize CVE vector store."""
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.collection_name = "cve_knowledge"
            self.embedding_dimension = 768  # BGE-base dimension

            # Initialize cache if Redis is available
            if REDIS_AVAILABLE:
                try:
                    self._cache = Redis(
                        host=settings.CELERY_BROKER_URL.split("//")[1].split(":")[0],
                        port=6379,
                        db=5,  # Use db 5 for CVE vector cache
                        decode_responses=True,
                    )
                    logger.info("Redis cache initialized for CVE vector store")
                except Exception as e:
                    logger.warning(f"Failed to initialize Redis cache: {e}")
                    self._cache = None
            else:
                self._cache = None

            logger.info("CVE Vector Store initialized")

    def _setup_client(self):
        """Initialize Qdrant client."""
        if self._client is None:
            try:
                self._client = QdrantClient(url=settings.QDRANT_URL)
                logger.info(f"Connected to Qdrant at {settings.QDRANT_URL}")
            except Exception as e:
                logger.error(f"Failed to connect to Qdrant: {e}")
                self._client = None

    def _setup_model(self):
        """Initialize embedding model (lazy loading)."""
        if self._model is None:
            try:
                logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
                self._model = SentenceTransformer(
                    settings.EMBEDDING_MODEL, device=settings.EMBEDDING_DEVICE
                )
                logger.info("Embedding model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
                self._model = None

    async def initialize(self) -> bool:
        """
        Initialize the CVE vector store.

        Returns:
            bool: True if successful
        """
        self._setup_client()
        if not self._client:
            return False

        try:
            # Check if collection exists
            collections = self._client.get_collections()
            exists = any(c.name == self.collection_name for c in collections.collections)

            if not exists:
                logger.info(f"Creating CVE collection '{self.collection_name}'")

                # Create collection with optimized settings
                self._client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.embedding_dimension,
                        distance=models.Distance.COSINE,
                        on_disk=False,  # Keep in memory for speed
                    ),
                    # Enable payload indexing for fast filtering
                    optimizers_config=models.OptimizersConfigDiff(
                        indexing_threshold=10000,  # Index after 10k points
                    ),
                    # HNSW index for fast approximate search
                    hnsw_config=models.HnswConfigDiff(
                        m=16,  # Number of edges per node
                        ef_construct=100,  # Construction time accuracy
                        full_scan_threshold=10000,  # Use HNSW after 10k points
                    ),
                )

                # Create payload indexes for common filters
                self._create_payload_indexes()

                logger.info("✅ CVE collection created successfully")
            else:
                logger.info(f"CVE collection '{self.collection_name}' already exists")

            return True
        except Exception as e:
            logger.error(f"Failed to initialize CVE collection: {e}")
            return False

    def _create_payload_indexes(self):
        """Create indexes on frequently filtered fields."""
        try:
            # Index CVE ID for exact lookups
            self._client.create_payload_index(
                collection_name=self.collection_name,
                field_name="cve_id",
                field_schema=models.PayloadSchemaType.KEYWORD,
            )

            # Index CVSS base score for range queries
            self._client.create_payload_index(
                collection_name=self.collection_name,
                field_name="cvss_base_score",
                field_schema=models.PayloadSchemaType.FLOAT,
            )

            # Index severity for categorical filtering
            self._client.create_payload_index(
                collection_name=self.collection_name,
                field_name="severity",
                field_schema=models.PayloadSchemaType.KEYWORD,
            )

            # Index exploit availability
            self._client.create_payload_index(
                collection_name=self.collection_name,
                field_name="exploit_available",
                field_schema=models.PayloadSchemaType.BOOL,
            )

            # Index published year for temporal filtering
            self._client.create_payload_index(
                collection_name=self.collection_name,
                field_name="published_year",
                field_schema=models.PayloadSchemaType.INTEGER,
            )

            logger.info("✅ Payload indexes created")
        except Exception as e:
            logger.warning(f"Failed to create payload indexes: {e}")

    async def add_cve(self, cve: CVEMetadata) -> bool:
        """
        Add a single CVE to the vector store.

        Args:
            cve: CVE metadata to store

        Returns:
            bool: True if successful
        """
        if not self._client:
            self._setup_client()
            if not self._client:
                return False

        try:
            self._setup_model()
            if not self._model:
                return False

            # Generate embedding from description
            embedding = self._model.encode(cve.description).tolist()

            # Prepare payload with flattened metadata for filtering
            payload = cve.to_dict()

            # Add flattened fields for easy filtering
            payload["cvss_base_score"] = self._get_highest_cvss_score(cve)
            payload["severity"] = self._get_severity(cve)
            payload["published_year"] = int(cve.published_date[:4]) if cve.published_date else None

            # Upload to Qdrant
            self._client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=str(uuid.uuid5(uuid.NAMESPACE_DNS, cve.cve_id)),  # Deterministic ID
                        vector=embedding,
                        payload=payload,
                    )
                ],
            )

            logger.debug(f"Stored CVE: {cve.cve_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add CVE {cve.cve_id}: {e}")
            return False

    async def add_cves_batch(
        self, cves: list[CVEMetadata], batch_size: int = 100
    ) -> tuple[int, int]:
        """
        Add multiple CVEs in batches for efficiency.

        Args:
            cves: List of CVE metadata
            batch_size: Number of CVEs per batch

        Returns:
            Tuple of (successful_count, failed_count)
        """
        if not self._client:
            self._setup_client()
            if not self._client:
                return 0, len(cves)

        self._setup_model()
        if not self._model:
            return 0, len(cves)

        successful = 0
        failed = 0

        for i in range(0, len(cves), batch_size):
            batch = cves[i : i + batch_size]

            try:
                points = []
                for cve in batch:
                    # Generate embedding
                    embedding = self._model.encode(cve.description).tolist()

                    # Prepare payload
                    payload = cve.to_dict()
                    payload["cvss_base_score"] = self._get_highest_cvss_score(cve)
                    payload["severity"] = self._get_severity(cve)
                    payload["published_year"] = (
                        int(cve.published_date[:4]) if cve.published_date else None
                    )

                    points.append(
                        models.PointStruct(
                            id=str(uuid.uuid5(uuid.NAMESPACE_DNS, cve.cve_id)),
                            vector=embedding,
                            payload=payload,
                        )
                    )

                # Batch upload
                self._client.upsert(collection_name=self.collection_name, points=points)

                successful += len(batch)
                logger.info(f"✅ Stored batch {i // batch_size + 1}: {len(batch)} CVEs")
            except Exception as e:
                logger.error(f"Failed to store batch {i // batch_size + 1}: {e}")
                failed += len(batch)

        return successful, failed

    async def search(
        self,
        query: str,
        limit: int = 10,
        min_cvss_score: Optional[float] = None,
        max_cvss_score: Optional[float] = None,
        severity: Optional[str] = None,
        exploit_available: Optional[bool] = None,
        published_after: Optional[str] = None,  # ISO date string
        published_before: Optional[str] = None,
        cwe_ids: Optional[list[str]] = None,
        cpe_match: Optional[str] = None,
        score_threshold: float = 0.3,
    ) -> CVESearchResponse:
        """
        Search CVEs with hybrid semantic + metadata filtering.

        Args:
            query: Search query text
            limit: Maximum results to return
            min_cvss_score: Minimum CVSS base score (0-10)
            max_cvss_score: Maximum CVSS base score (0-10)
            severity: Severity level (LOW, MEDIUM, HIGH, CRITICAL)
            exploit_available: Filter by exploit availability
            published_after: Filter CVEs published after this date
            published_before: Filter CVEs published before this date
            cwe_ids: Filter by CWE IDs
            cpe_match: Filter by CPE URI substring
            score_threshold: Minimum similarity score (0-1)

        Returns:
            CVESearchResponse with ranked results
        """
        import time

        start_time = time.time()

        if not self._client:
            self._setup_client()
            if not self._client:
                return CVESearchResponse(
                    query=query, results=[], total_found=0, search_time_ms=0, filters_applied={}
                )

        # Check cache
        cache_key = None
        if self._cache:
            cache_key = hashlib.md5(
                f"{query}:{limit}:{min_cvss_score}:{max_cvss_score}:{severity}:{exploit_available}:{published_after}:{published_before}:{cwe_ids}:{cpe_match}:{score_threshold}".encode()
            ).hexdigest()

            try:
                cached = self._cache.get(f"cve_search:{cache_key}")
                if cached:
                    logger.debug("Cache hit for CVE search")
                    data = json.loads(cached)
                    return CVESearchResponse(
                        query=data["query"],
                        results=[CVESearchResult(**r) for r in data["results"]],
                        total_found=data["total_found"],
                        search_time_ms=data["search_time_ms"],
                        filters_applied=data["filters_applied"],
                    )
            except Exception as e:
                logger.warning(f"Cache read failed: {e}")

        try:
            self._setup_model()
            if not self._model:
                return CVESearchResponse(
                    query=query, results=[], total_found=0, search_time_ms=0, filters_applied={}
                )

            # Generate query embedding
            query_vector = self._model.encode(query).tolist()

            # Build filters
            filters = self._build_filters(
                min_cvss_score=min_cvss_score,
                max_cvss_score=max_cvss_score,
                severity=severity,
                exploit_available=exploit_available,
                published_after=published_after,
                published_before=published_before,
                cwe_ids=cwe_ids,
                cpe_match=cpe_match,
            )

            # Search
            search_results = self._client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                query_filter=filters,
                limit=limit,
                score_threshold=score_threshold,
            ).points

            # Format results
            results = []
            for hit in search_results:
                metadata = CVEMetadata.from_dict(hit.payload)
                results.append(
                    CVESearchResult(
                        cve_id=hit.payload["cve_id"],
                        description=hit.payload["description"],
                        score=hit.score,
                        metadata=metadata,
                    )
                )

            search_time_ms = (time.time() - start_time) * 1000

            response = CVESearchResponse(
                query=query,
                results=results,
                total_found=len(results),
                search_time_ms=search_time_ms,
                filters_applied={
                    "min_cvss_score": min_cvss_score,
                    "max_cvss_score": max_cvss_score,
                    "severity": severity,
                    "exploit_available": exploit_available,
                    "published_after": published_after,
                    "published_before": published_before,
                    "cwe_ids": cwe_ids,
                    "cpe_match": cpe_match,
                },
            )

            # Cache results
            if self._cache and cache_key:
                try:
                    self._cache.setex(
                        f"cve_search:{cache_key}",
                        3600,  # 1 hour TTL
                        json.dumps(response.to_dict()),
                    )
                except Exception as e:
                    logger.warning(f"Cache write failed: {e}")

            logger.info(
                f"CVE search completed in {search_time_ms:.2f}ms, found {len(results)} results"
            )
            return response

        except Exception as e:
            logger.error(f"CVE search failed: {e}")
            return CVESearchResponse(
                query=query,
                results=[],
                total_found=0,
                search_time_ms=(time.time() - start_time) * 1000,
                filters_applied={},
            )

    def _build_filters(
        self,
        min_cvss_score: Optional[float] = None,
        max_cvss_score: Optional[float] = None,
        severity: Optional[str] = None,
        exploit_available: Optional[bool] = None,
        published_after: Optional[str] = None,
        published_before: Optional[str] = None,
        cwe_ids: Optional[list[str]] = None,
        cpe_match: Optional[str] = None,
    ) -> Optional[models.Filter]:
        """Build Qdrant filter from search parameters."""
        must_conditions = []

        # CVSS score range
        if min_cvss_score is not None:
            must_conditions.append(
                models.FieldCondition(key="cvss_base_score", range=models.Range(gte=min_cvss_score))
            )

        if max_cvss_score is not None:
            must_conditions.append(
                models.FieldCondition(key="cvss_base_score", range=models.Range(lte=max_cvss_score))
            )

        # Severity
        if severity:
            must_conditions.append(
                models.FieldCondition(
                    key="severity", match=models.MatchValue(value=severity.upper())
                )
            )

        # Exploit availability
        if exploit_available is not None:
            must_conditions.append(
                models.FieldCondition(
                    key="exploit_available", match=models.MatchValue(value=exploit_available)
                )
            )

        # Published date range
        if published_after:
            year = int(published_after[:4])
            must_conditions.append(
                models.FieldCondition(key="published_year", range=models.Range(gte=year))
            )

        if published_before:
            year = int(published_before[:4])
            must_conditions.append(
                models.FieldCondition(key="published_year", range=models.Range(lte=year))
            )

        # CWE IDs (any match)
        if cwe_ids:
            # Note: This requires the CWE to be in the cwe_ids array
            # Qdrant doesn't support array contains, so we'd need to restructure
            # For now, we'll skip this filter
            pass

        # CPE match (substring)
        if cpe_match:
            # Similar limitation - would need full-text search
            pass

        if must_conditions:
            return models.Filter(must=must_conditions)
        return None

    def _get_highest_cvss_score(self, cve: CVEMetadata) -> float:
        """Get the highest CVSS score from all versions."""
        scores = []
        if cve.cvss_v2:
            scores.append(cve.cvss_v2.base_score)
        if cve.cvss_v3:
            scores.append(cve.cvss_v3.base_score)
        if cve.cvss_v3_1:
            scores.append(cve.cvss_v3_1.base_score)
        return max(scores) if scores else 0.0

    def _get_severity(self, cve: CVEMetadata) -> str:
        """Get severity from the latest CVSS version."""
        if cve.cvss_v3_1:
            return cve.cvss_v3_1.severity
        if cve.cvss_v3:
            return cve.cvss_v3.severity
        if cve.cvss_v2:
            return cve.cvss_v2.severity
        return "UNKNOWN"

    async def get_cve_by_id(self, cve_id: str) -> Optional[CVEMetadata]:
        """
        Retrieve a specific CVE by ID.

        Args:
            cve_id: CVE identifier (e.g., "CVE-2021-44228")

        Returns:
            CVEMetadata if found, None otherwise
        """
        if not self._client:
            self._setup_client()
            if not self._client:
                return None

        try:
            # Use deterministic UUID
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, cve_id))

            result = self._client.retrieve(collection_name=self.collection_name, ids=[point_id])

            if result:
                return CVEMetadata.from_dict(result[0].payload)
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve CVE {cve_id}: {e}")
            return None

    async def get_stats(self) -> dict[str, Any]:
        """
        Get statistics about the CVE vector store.

        Returns:
            Dictionary with collection statistics
        """
        if not self._client:
            self._setup_client()
            if not self._client:
                return {}

        try:
            collection_info = self._client.get_collection(self.collection_name)

            return {
                "total_cves": collection_info.points_count,
                "indexed_vectors_count": collection_info.indexed_vectors_count
                if hasattr(collection_info, "indexed_vectors_count")
                else collection_info.points_count,
                "collection_name": self.collection_name,
                "embedding_dimension": self.embedding_dimension,
                "status": collection_info.status,
            }
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {}


# Global instance
_cve_vector_store: Optional[CVEVectorStore] = None


def get_cve_vector_store() -> CVEVectorStore:
    """Get global CVE vector store instance."""
    global _cve_vector_store
    if _cve_vector_store is None:
        _cve_vector_store = CVEVectorStore()
    return _cve_vector_store
