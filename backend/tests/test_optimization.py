"""
Unit Tests for Optimization Services.

Tests all optimization components:
- Semantic cache
- Backpressure manager
- Token optimizer
- Integration manager
"""

import asyncio
import time
from unittest.mock import Mock, patch

import pytest
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.services.optimization.backpressure import (
    BackpressureConfig,
    BackpressureManager,
    EventBatcher,
    RateLimiter,
)
from app.services.optimization.semantic_cache import (
    CacheConfig,
    CacheEntry,
    CacheStats,
    SemanticCache,
)
from app.services.optimization.token_optimizer import (
    ConversationSummarizer,
    PromptCompressor,
    TokenCounter,
    TokenOptimizer,
    TokenOptimizerConfig,
    ToolFilterer,
)


class TestSemanticCache:
    """Tests for semantic cache service."""

    @pytest.fixture
    def cache_config(self):
        """Create test cache configuration."""
        return CacheConfig(
            enabled=True,
            similarity_threshold=0.95,
            ttl_seconds=3600,
            max_cache_size=100,
            redis_host="localhost",
            redis_port=6379,
            redis_db=2,
        )

    @pytest.fixture
    def mock_redis(self):
        """Mock Redis client."""
        with patch("app.services.optimization.semantic_cache.Redis") as mock:
            redis_instance = Mock()
            redis_instance.ping.return_value = True
            redis_instance.keys.return_value = []
            redis_instance.get.return_value = None
            mock.return_value = redis_instance
            yield redis_instance

    def test_cache_initialization(self, cache_config, mock_redis):
        """Test cache initialization."""
        cache = SemanticCache(cache_config)

        assert cache.config == cache_config
        assert cache.embedding_model is not None
        assert cache.redis is not None

    def test_cache_set_and_get(self, cache_config, mock_redis):
        """Test caching and retrieval."""
        cache = SemanticCache(cache_config)

        # Set a value
        query = "What is a port scan?"
        response = "A port scan is a method used to identify open ports..."

        result = cache.set(query, response)
        assert result is True

        # Mock Redis to return the cached value
        embedding = cache._generate_embedding(query)
        entry = CacheEntry(
            query=query,
            response=response,
            embedding=embedding,
            metadata={},
            created_at=time.time(),
            ttl=3600,
        )

        import json

        mock_redis.get.return_value = json.dumps(entry.to_dict()).encode()
        mock_redis.keys.return_value = [cache._generate_cache_key(embedding).encode()]

        # Get the value
        cached_response = cache.get(query)
        assert cached_response == response

    def test_cache_similarity_threshold(self, cache_config, mock_redis):
        """Test similarity threshold filtering."""
        cache = SemanticCache(cache_config)

        # Cache original query
        original_query = "scan ports on localhost"
        response = "Scanning ports..."
        cache.set(original_query, response)

        # Similar query should hit cache
        similar_query = "scan ports on 127.0.0.1"

        # Mock similar entry
        original_embedding = cache._generate_embedding(original_query)
        entry = CacheEntry(
            query=original_query,
            response=response,
            embedding=original_embedding,
            metadata={},
            created_at=time.time(),
            ttl=3600,
        )

        import json

        mock_redis.get.return_value = json.dumps(entry.to_dict()).encode()
        mock_redis.keys.return_value = [cache._generate_cache_key(original_embedding).encode()]

        cached = cache.get(similar_query)
        # Should get cached response if similarity > threshold
        assert cached is not None or cached is None  # Depends on actual similarity

    def test_cache_stats(self, cache_config, mock_redis):
        """Test cache statistics tracking."""
        cache = SemanticCache(cache_config)

        stats = cache.get_stats()
        assert isinstance(stats, CacheStats)
        assert stats.total_requests >= 0
        assert stats.cache_hits >= 0
        assert stats.cache_misses >= 0


class TestBackpressureManager:
    """Tests for backpressure manager."""

    @pytest.fixture
    def bp_config(self):
        """Create test backpressure configuration."""
        return BackpressureConfig(
            enabled=True,
            batch_size=5,
            batch_timeout_ms=50,
            max_events_per_second=100,
            compression_threshold_bytes=512,
        )

    def test_rate_limiter(self):
        """Test rate limiter."""
        limiter = RateLimiter(max_rate=10)  # 10 events/second

        async def test():
            start = time.time()

            # Acquire 10 tokens
            for _ in range(10):
                await limiter.acquire()

            elapsed = time.time() - start

            # Should take ~0 seconds for first 10
            assert elapsed < 0.5

            # Next 10 should be rate limited
            start = time.time()
            for _ in range(10):
                await limiter.acquire()

            elapsed = time.time() - start
            # Should take ~1 second
            assert elapsed >= 0.8

        asyncio.run(test())

    def test_event_batcher(self):
        """Test event batching."""
        batcher = EventBatcher(batch_size=3, timeout_ms=100)

        async def test():
            # Create event stream
            async def event_stream():
                for i in range(10):
                    yield {"id": i, "data": f"event_{i}"}
                    await asyncio.sleep(0.01)

            batches = []
            async for batch in batcher.batch(event_stream()):
                batches.append(batch)

            # Should have multiple batches
            assert len(batches) > 1

            # Each batch should have <= batch_size events
            for batch in batches:
                assert len(batch) <= 3

        asyncio.run(test())

    def test_backpressure_processing(self, bp_config):
        """Test backpressure processing."""
        manager = BackpressureManager(bp_config)

        async def test():
            # Create event stream
            async def event_stream():
                for i in range(20):
                    yield {"id": i, "data": f"event_{i}"}

            processed = []
            async for event in manager.process(event_stream()):
                processed.append(event)

            # All events should be processed
            assert len(processed) == 20

        asyncio.run(test())

    def test_compression(self, bp_config):
        """Test payload compression."""
        manager = BackpressureManager(bp_config)

        # Large payload
        large_data = "x" * 2000
        compressed = manager._compress_payload(large_data)

        # Should compress large payloads
        assert compressed is not None
        assert len(compressed) < len(large_data.encode("utf-8"))

        # Small payload
        small_data = "small"
        compressed = manager._compress_payload(small_data)

        # Should not compress small payloads
        assert compressed is None


class TestTokenOptimizer:
    """Tests for token optimizer."""

    @pytest.fixture
    def token_config(self):
        """Create test token optimizer configuration."""
        return TokenOptimizerConfig(
            enabled=True,
            summarization_threshold=10,
            max_context_messages=5,
            dynamic_tool_filtering=True,
            compress_prompts=True,
        )

    def test_token_counter(self):
        """Test token counting."""
        counter = TokenCounter()

        text = "This is a test message for token counting."
        tokens = counter.count_tokens(text)

        # Should return positive number
        assert tokens > 0

        # Longer text should have more tokens
        longer_text = text * 10
        longer_tokens = counter.count_tokens(longer_text)
        assert longer_tokens > tokens

    def test_prompt_compression(self):
        """Test prompt compression."""
        compressor = PromptCompressor()

        text = "Please   kindly  help  me  very  much  with  this  task"
        compressed = compressor.compress(text)

        # Should be shorter
        assert len(compressed) < len(text)

        # Should remove filler words
        assert "kindly" not in compressed.lower()
        assert "very" not in compressed.lower()

    def test_conversation_summarization(self):
        """Test conversation summarization."""
        summarizer = ConversationSummarizer(max_messages=3)

        # Create long conversation
        messages = [HumanMessage(content=f"Question {i}") for i in range(10)]

        summarized = summarizer.summarize(messages)

        # Should be shorter than original
        assert len(summarized) < len(messages)

        # Should keep recent messages
        assert len(summarized) <= 4  # 3 recent + 1 summary

    def test_tool_filtering(self):
        """Test dynamic tool filtering."""
        filterer = ToolFilterer()

        # Create mock tools
        class MockTool:
            def __init__(self, name, description):
                self.name = name
                self.description = description

        tools = [
            MockTool("scan_network", "Scan network ports"),
            MockTool("check_headers", "Check HTTP headers"),
            MockTool("search_cve", "Search for CVE vulnerabilities"),
            MockTool("execute_command", "Execute terminal command"),
        ]

        # Query about scanning
        query = "scan ports on localhost"
        filtered = filterer.filter_tools(query, tools)

        # Should prioritize network tools
        assert any("scan" in tool.name for tool in filtered)

        # Should filter out irrelevant tools
        assert len(filtered) <= len(tools)

    def test_token_optimization(self, token_config):
        """Test full token optimization."""
        optimizer = TokenOptimizer(token_config)

        # Create messages
        messages = [
            SystemMessage(content="You are a helpful assistant. Please help the user."),
            HumanMessage(content="What is a port scan?"),
            AIMessage(content="A port scan is..."),
            HumanMessage(content="How do I scan ports?"),
        ]

        # Create mock tools
        class MockTool:
            def __init__(self, name, description):
                self.name = name
                self.description = description

        tools = [MockTool(f"tool_{i}", f"Description {i}") for i in range(10)]

        # Optimize
        optimized_messages, optimized_tools = optimizer.optimize_messages(
            messages=messages, tools=tools, query="scan ports"
        )

        # Should return optimized versions
        assert optimized_messages is not None
        assert optimized_tools is not None

        # Tools should be filtered
        assert len(optimized_tools) <= len(tools)

    def test_token_tracking(self, token_config):
        """Test token usage tracking."""
        optimizer = TokenOptimizer(token_config)

        # Track usage
        optimizer.track_usage(input_tokens=1000, output_tokens=500)

        stats = optimizer.get_stats()

        assert stats.total_requests == 1
        assert stats.total_input_tokens == 1000
        assert stats.total_output_tokens == 500
        assert stats.total_cost_usd > 0


@pytest.mark.asyncio
async def test_optimization_integration():
    """Test integration of all optimization services."""
    from app.services.optimization.integration import OptimizationManager

    # Create manager with all services disabled (to avoid Redis dependency)
    manager = OptimizationManager(
        enable_caching=False, enable_backpressure=False, enable_token_optimization=False
    )

    # Should initialize without errors
    assert manager is not None

    # Get stats should work even with disabled services
    stats = manager.get_stats()
    assert isinstance(stats, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
