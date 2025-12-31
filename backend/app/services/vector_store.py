"""Vector store service for long-term memory using Qdrant."""

import hashlib
import json
import uuid
from datetime import datetime
from typing import Any, Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter
from loguru import logger
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import CrossEncoder, SentenceTransformer

from app.core.config import settings

# Try to import Redis for caching (optional)
try:
    from redis import Redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not available, caching disabled")


class VectorStoreService:
    """Service for managing vector embeddings and search in Qdrant."""

    _instance: Optional["VectorStoreService"] = None
    _client: Optional[QdrantClient] = None
    _model: Optional[SentenceTransformer] = None

    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize vector store service."""
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.collection_name = settings.QDRANT_COLLECTION_NAME
            self._setup_client()

            # Initialize text splitter for chunking
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1024,  # Optimal for BGE-large
                chunk_overlap=100,  # Preserve context
                separators=["\n\n", "\n", ". ", " ", ""],
            )

            # Initialize cache if Redis is available
            if REDIS_AVAILABLE:
                try:
                    self._cache = Redis(
                        host=settings.CELERY_BROKER_URL.split("//")[1].split(":")[0],
                        port=6379,
                        db=2,  # Use db 2 for vector cache
                        decode_responses=True,
                    )
                    logger.info("Redis cache initialized for vector store")
                except Exception as e:
                    logger.warning(f"Failed to initialize Redis cache: {e}")
                    self._cache = None
            else:
                self._cache = None

            # Lazy load model and reranker
            # self._setup_model()
            # self._setup_reranker()
            logger.info("Vector store service initialized")

    def _setup_client(self):
        """Initialize Qdrant client."""
        try:
            self._client = QdrantClient(url=settings.QDRANT_URL)
            logger.info(f"Connected to Qdrant at {settings.QDRANT_URL}")
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            self._client = None

    def _setup_model(self):
        """Initialize embedding model."""
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

    def _setup_reranker(self):
        """Initialize reranker model for improved precision."""
        if not hasattr(self, "_reranker") or self._reranker is None:
            try:
                logger.info("Loading reranker model: BAAI/bge-reranker-large")
                self._reranker = CrossEncoder(
                    "BAAI/bge-reranker-large", max_length=512, device=settings.EMBEDDING_DEVICE
                )
                logger.info("Reranker model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load reranker model: {e}")
                self._reranker = None

    def ensure_collection(self):
        """Ensure the vector collection exists."""
        if not self._client:
            return False

        try:
            # Check if collection exists
            collections = self._client.get_collections()
            exists = any(c.name == self.collection_name for c in collections.collections)

            if not exists:
                # Ensure model is loaded to get dimension
                self._setup_model()
                if not self._model:
                    raise RuntimeError("Cannot create collection without embedding model")

                dimension = self._model.get_sentence_embedding_dimension()

                logger.info(
                    f"Creating collection '{self.collection_name}' with dimension {dimension}"
                )
                self._client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=dimension, distance=models.Distance.COSINE
                    ),
                )
                logger.info("Collection created successfully")
            return True
        except Exception as e:
            logger.error(f"Error ensuring collection: {e}")
            return False

    def add_memory(self, text: str, metadata: dict[str, Any] = None) -> bool:
        """
        Add a text memory to the vector store.

        Args:
            text: The text content to store
            metadata: Optional metadata (e.g., user_id, conversation_id, type)

        Returns:
            bool: True if successful
        """
        if not self._client:
            logger.warning("Qdrant client not available, skipping memory storage")
            return False

        # Ensure collection exists before adding memory
        if not self.ensure_collection():
            logger.error("Failed to ensure collection exists")
            return False

        try:
            self._setup_model()
            if not self._model:
                return False

            # Generate embedding
            embedding = self._model.encode(text).tolist()

            # Prepare payload
            payload = {
                "content": text,
                "created_at": datetime.utcnow().isoformat(),
                **(metadata or {}),
            }

            # Upload to Qdrant
            self._client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(id=str(uuid.uuid4()), vector=embedding, payload=payload)
                ],
            )
            logger.debug(f"Stored memory: {text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Failed to add memory: {e}")
            return False

    def add_memory_with_chunking(self, text: str, metadata: dict[str, Any] = None) -> bool:
        """
        Add memory with automatic chunking for large content.

        Args:
            text: Content to store
            metadata: Optional metadata

        Returns:
            bool: True if successful
        """
        if not self._client:
            logger.warning("Qdrant client not available")
            return False

        # Ensure collection exists
        if not self.ensure_collection():
            return False

        try:
            self._setup_model()
            if not self._model:
                return False

            # Estimate tokens (rough: 1 token ≈ 4 characters)
            estimated_tokens = len(text) / 4

            if estimated_tokens > 800:  # Chunk if >800 tokens
                logger.info(f"Content is large ({estimated_tokens:.0f} tokens), chunking...")
                chunks = self.text_splitter.split_text(text)

                # Generate unique parent ID
                parent_id = str(uuid.uuid4())

                # Store each chunk
                for i, chunk in enumerate(chunks):
                    chunk_metadata = {
                        **(metadata or {}),
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                        "parent_id": parent_id,
                        "is_chunked": True,
                    }

                    # Generate embedding for chunk
                    embedding = self._model.encode(chunk).tolist()

                    # Prepare payload
                    payload = {
                        "content": chunk,
                        "created_at": datetime.utcnow().isoformat(),
                        **chunk_metadata,
                    }

                    # Upload chunk
                    self._client.upsert(
                        collection_name=self.collection_name,
                        points=[
                            models.PointStruct(
                                id=str(uuid.uuid4()), vector=embedding, payload=payload
                            )
                        ],
                    )

                logger.info(f"✅ Stored {len(chunks)} chunks for large content")
                return True
            else:
                # Use existing add_memory for small content
                return self.add_memory(text, metadata)

        except Exception as e:
            logger.error(f"Failed to add memory with chunking: {e}")
            return False

    def search_memory(
        self,
        query: str,
        limit: int = 5,
        score_threshold: float = 0.3,  # Lowered from 0.5 for better recall
        filter_metadata: dict[str, Any] = None,
        use_reranking: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Search for similar memories with optional reranking and caching.

        Args:
            query: Search query text
            limit: Maximum number of results
            score_threshold: Minimum similarity score (0-1)
            filter_metadata: Optional metadata filter (e.g., {"user_id": 1})
            use_reranking: Whether to use reranking (default: True)

        Returns:
            List of matches with content and metadata
        """
        if not self._client:
            return []

        # Check cache first
        cache_key = None
        if self._cache:
            cache_key = hashlib.md5(
                f"{query}:{limit}:{score_threshold}:{json.dumps(filter_metadata or {}, sort_keys=True)}".encode()
            ).hexdigest()

            try:
                cached = self._cache.get(f"search:{cache_key}")
                if cached:
                    logger.debug("Cache hit for search query")
                    return json.loads(cached)
            except Exception as e:
                logger.warning(f"Cache read failed: {e}")

        try:
            self._setup_model()
            if not self._model:
                return []

            # Generate query embedding
            query_vector = self._model.encode(query).tolist()

            # Build filter if provided
            query_filter = None
            if filter_metadata:
                must_conditions = []
                for key, value in filter_metadata.items():
                    must_conditions.append(
                        models.FieldCondition(key=key, match=models.MatchValue(value=value))
                    )
                if must_conditions:
                    query_filter = models.Filter(must=must_conditions)

            # Retrieve more candidates if reranking
            retrieve_limit = limit * 4 if use_reranking else limit

            # Search using query_points
            results = self._client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                query_filter=query_filter,
                limit=retrieve_limit,
                score_threshold=score_threshold,
            ).points

            # Format results
            memories = []
            for hit in results:
                memories.append(
                    {
                        "content": hit.payload.get("content", ""),
                        "score": hit.score,
                        "metadata": {k: v for k, v in hit.payload.items() if k != "content"},
                    }
                )

            # Apply reranking if enabled and we have results
            if use_reranking and memories and len(memories) > limit:
                try:
                    self._setup_reranker()
                    if self._reranker:
                        logger.debug(f"Reranking {len(memories)} candidates to top {limit}")

                        # Prepare pairs for reranking
                        pairs = [[query, mem["content"]] for mem in memories]

                        # Get reranking scores
                        rerank_scores = self._reranker.predict(pairs)

                        # Combine with original scores and sort
                        for i, mem in enumerate(memories):
                            mem["rerank_score"] = float(rerank_scores[i])

                        # Sort by rerank score and take top N
                        memories = sorted(memories, key=lambda x: x["rerank_score"], reverse=True)[
                            :limit
                        ]

                        logger.debug("Reranking complete")
                except Exception as e:
                    logger.warning(f"Reranking failed, using original results: {e}")
                    memories = memories[:limit]
            else:
                memories = memories[:limit]

            # Cache results
            if self._cache and cache_key:
                try:
                    self._cache.setex(
                        f"search:{cache_key}",
                        3600,  # 1 hour TTL
                        json.dumps(memories),
                    )
                except Exception as e:
                    logger.warning(f"Cache write failed: {e}")

            return memories
        except Exception as e:
            logger.error(f"Memory search failed: {e}")
            return []


# Global instance
_vector_store: Optional[VectorStoreService] = None


def get_vector_store() -> VectorStoreService:
    """Get global vector store service instance."""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStoreService()
    return _vector_store
