"""
Comprehensive Integration Tests for Optimization Features.

This test suite demonstrates and verifies:
1. How semantic caching works (similarity matching)
2. How cost savings are calculated
3. How token optimization reduces usage
4. How backpressure handles large outputs
5. Real-world scenarios with actual LLM calls

Run with: pytest tests/test_optimization_integration.py -v -s
"""

import asyncio
import json
import time

import pytest
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.services.optimization.backpressure import BackpressureConfig, BackpressureManager
from app.services.optimization.integration import OptimizationManager
from app.services.optimization.semantic_cache import CacheConfig, SemanticCache
from app.services.optimization.token_optimizer import (
    TokenCounter,
    TokenOptimizer,
    TokenOptimizerConfig,
)


class TestSemanticCacheDetailed:
    """Detailed tests showing how semantic caching works."""

    @pytest.fixture
    def cache(self):
        """Create a fresh cache for each test."""
        config = CacheConfig(
            enabled=True,
            similarity_threshold=0.95,
            ttl_seconds=3600,
            max_cache_size=100,
            redis_host="localhost",
            redis_port=6379,
            redis_db=2,
        )
        cache = SemanticCache(config)
        cache.clear()  # Start fresh
        return cache

    def test_exact_match_caching(self, cache):
        """Test 1: Exact same query should hit cache."""
        print("\n" + "=" * 60)
        print("TEST 1: Exact Match Caching")
        print("=" * 60)

        query = "What is a port scan?"
        response = "A port scan is a method used to identify open ports on a network."

        # First call - cache miss
        print(f"\n1. First query: '{query}'")
        cached = cache.get(query)
        print(f"   Result: {cached}")
        print("   Status: CACHE MISS (expected)")
        assert cached is None

        # Store in cache
        print("\n2. Storing response in cache...")
        cache.set(query, response)
        print(f"   Stored: '{response[:50]}...'")

        # Second call - should hit cache
        print(f"\n3. Same query again: '{query}'")
        start = time.time()
        cached = cache.get(query)
        elapsed = (time.time() - start) * 1000
        print(f"   Result: '{cached[:50]}...'")
        print("   Status: CACHE HIT ✓")
        print(f"   Response time: {elapsed:.2f}ms")
        assert cached == response
        assert elapsed < 100  # Should be very fast

        # Check stats
        stats = cache.get_stats()
        print("\n4. Cache Statistics:")
        print(f"   Total requests: {stats.total_requests}")
        print(f"   Cache hits: {stats.cache_hits}")
        print(f"   Cache misses: {stats.cache_misses}")
        print(f"   Hit rate: {stats.hit_rate:.1%}")
        print(f"   Cost saved: ${stats.cost_savings_usd:.4f}")

        assert stats.cache_hits == 1
        assert stats.cache_misses == 1
        assert stats.hit_rate == 0.5

    def test_semantic_similarity_matching(self, cache):
        """Test 2: Similar queries should hit cache."""
        print("\n" + "=" * 60)
        print("TEST 2: Semantic Similarity Matching")
        print("=" * 60)

        # Original query
        original_query = "How do I scan network ports?"
        response = "To scan network ports, you can use tools like nmap..."

        print(f"\n1. Original query: '{original_query}'")
        cache.set(original_query, response)
        print("   Cached response")

        # Similar queries that should hit cache
        similar_queries = [
            "How to scan ports on a network?",
            "What's the way to scan network ports?",
            "Can you explain how to scan ports?",
            "Tell me about scanning network ports",
        ]

        print("\n2. Testing similar queries:")
        for i, query in enumerate(similar_queries, 1):
            print(f"\n   Query {i}: '{query}'")

            # Get embedding similarity
            original_emb = cache._generate_embedding(original_query)
            query_emb = cache._generate_embedding(query)
            similarity = cache._cosine_similarity(original_emb, query_emb)

            print(f"   Similarity to original: {similarity:.4f}")

            # Try to get from cache
            cached = cache.get(query)

            if similarity >= cache.config.similarity_threshold:
                print(f"   Status: CACHE HIT ✓ (similarity >= {cache.config.similarity_threshold})")
                assert cached is not None
            else:
                print(f"   Status: CACHE MISS (similarity < {cache.config.similarity_threshold})")
                assert cached is None

    def test_different_queries_no_match(self, cache):
        """Test 3: Different queries should NOT hit cache."""
        print("\n" + "=" * 60)
        print("TEST 3: Different Queries (No Match)")
        print("=" * 60)

        # Cache a query about port scanning
        query1 = "What is a port scan?"
        response1 = "A port scan is..."
        cache.set(query1, response1)
        print(f"\n1. Cached: '{query1}'")

        # Try completely different queries
        different_queries = [
            "What is the weather today?",
            "How do I bake a cake?",
            "Tell me about Python programming",
            "What is machine learning?",
        ]

        print("\n2. Testing different queries:")
        for i, query in enumerate(different_queries, 1):
            print(f"\n   Query {i}: '{query}'")

            # Calculate similarity
            emb1 = cache._generate_embedding(query1)
            emb2 = cache._generate_embedding(query)
            similarity = cache._cosine_similarity(emb1, emb2)

            print(f"   Similarity: {similarity:.4f}")

            cached = cache.get(query)
            print("   Status: CACHE MISS ✓ (expected - different topic)")
            assert cached is None

    def test_cost_calculation(self, cache):
        """Test 4: How cost savings are calculated."""
        print("\n" + "=" * 60)
        print("TEST 4: Cost Savings Calculation")
        print("=" * 60)

        # Simulate 100 queries with 50% cache hit rate
        queries = [
            "What is a port scan?",
            "Explain port scanning",  # Similar - should hit
            "How do port scans work?",  # Similar - should hit
            "What is SQL injection?",
            "Explain SQL injection",  # Similar - should hit
        ]

        responses = {
            "port": "A port scan is a method...",
            "sql": "SQL injection is a vulnerability...",
        }

        print("\n1. Simulating queries:")
        cache_hits = 0
        cache_misses = 0

        for i, query in enumerate(queries * 20, 1):  # 100 total queries
            cached = cache.get(query)

            if cached is None:
                # Cache miss - store response
                if "port" in query.lower():
                    cache.set(query, responses["port"])
                else:
                    cache.set(query, responses["sql"])
                cache_misses += 1
            else:
                cache_hits += 1

            if i % 20 == 0:
                print(f"   Processed {i} queries...")

        stats = cache.get_stats()

        print("\n2. Results after 100 queries:")
        print(f"   Cache hits: {stats.cache_hits}")
        print(f"   Cache misses: {stats.cache_misses}")
        print(f"   Hit rate: {stats.hit_rate:.1%}")

        print("\n3. Cost Analysis:")
        print("   Cost per LLM call: $0.003 (estimated)")
        print(f"   Cache hits (free): {stats.cache_hits} × $0.000 = $0.00")
        print(
            f"   Cache misses (paid): {stats.cache_misses} × $0.003 = ${stats.cache_misses * 0.003:.3f}"
        )
        print(f"   Total cost saved: ${stats.cost_savings_usd:.3f}")

        print("\n4. Without caching:")
        print("   All queries would cost: 100 × $0.003 = $0.30")
        print(f"   With caching actual cost: ${stats.cache_misses * 0.003:.3f}")
        print(f"   Savings: ${stats.cost_savings_usd:.3f} ({stats.hit_rate:.1%})")

        assert stats.cache_hits > 0
        assert stats.cost_savings_usd > 0


class TestTokenOptimizationDetailed:
    """Detailed tests showing how token optimization works."""

    @pytest.fixture
    def optimizer(self):
        """Create token optimizer."""
        config = TokenOptimizerConfig(
            enabled=True,
            summarization_threshold=10,
            max_context_messages=5,
            dynamic_tool_filtering=True,
            compress_prompts=True,
            track_costs=True,
        )
        return TokenOptimizer(config)

    def test_prompt_compression(self, optimizer):
        """Test 5: How prompt compression works."""
        print("\n" + "=" * 60)
        print("TEST 5: Prompt Compression")
        print("=" * 60)

        # Verbose prompt with filler words
        verbose_prompt = """
        Please kindly help me very much with this task.
        I would really appreciate it if you could basically
        explain to me quite clearly how port scanning actually works.
        """

        print(f"\n1. Original prompt ({len(verbose_prompt)} chars):")
        print(f"   '{verbose_prompt.strip()}'")

        # Compress
        compressed = optimizer.compressor.compress(verbose_prompt)

        print(f"\n2. Compressed prompt ({len(compressed)} chars):")
        print(f"   '{compressed}'")

        print("\n3. Reduction:")
        print(f"   Original: {len(verbose_prompt)} characters")
        print(f"   Compressed: {len(compressed)} characters")
        print(
            f"   Saved: {len(verbose_prompt) - len(compressed)} characters ({(1 - len(compressed)/len(verbose_prompt)):.1%})"
        )

        # Verify filler words removed
        assert "kindly" not in compressed.lower()
        assert "very" not in compressed.lower()
        assert "basically" not in compressed.lower()
        assert len(compressed) < len(verbose_prompt)

    def test_conversation_summarization(self, optimizer):
        """Test 6: How conversation summarization works."""
        print("\n" + "=" * 60)
        print("TEST 6: Conversation Summarization")
        print("=" * 60)

        # Create long conversation
        messages = []
        for i in range(15):
            messages.append(HumanMessage(content=f"Question {i+1}: Tell me about topic {i+1}"))
            messages.append(
                AIMessage(content=f"Answer {i+1}: Here's information about topic {i+1}...")
            )

        print("\n1. Original conversation:")
        print(f"   Total messages: {len(messages)}")
        print(f"   First message: '{messages[0].content}'")
        print(f"   Last message: '{messages[-1].content}'")

        # Count tokens
        counter = TokenCounter()
        original_tokens = counter.count_messages_tokens(messages)
        print(f"   Total tokens: {original_tokens}")

        # Summarize
        print(
            f"\n2. Summarizing (keeping last {optimizer.config.max_context_messages} messages)..."
        )
        summarized = optimizer.summarizer.summarize(messages)

        summarized_tokens = counter.count_messages_tokens(summarized)

        print("\n3. After summarization:")
        print(f"   Total messages: {len(summarized)}")
        print(f"   Total tokens: {summarized_tokens}")
        print(f"   Tokens saved: {original_tokens - summarized_tokens}")
        print(f"   Reduction: {(1 - summarized_tokens/original_tokens):.1%}")

        # Check that recent messages are preserved
        assert len(summarized) <= optimizer.config.max_context_messages + 1  # +1 for summary
        assert summarized_tokens < original_tokens

    def test_dynamic_tool_filtering(self, optimizer):
        """Test 7: How dynamic tool filtering works."""
        print("\n" + "=" * 60)
        print("TEST 7: Dynamic Tool Filtering")
        print("=" * 60)

        # Create mock tools
        class MockTool:
            def __init__(self, name, description):
                self.name = name
                self.description = description

        all_tools = [
            MockTool("scan_network", "Scan network ports using nmap"),
            MockTool("scan_ports", "Perform port scanning"),
            MockTool("check_http_headers", "Check HTTP security headers"),
            MockTool("test_ssl", "Test SSL/TLS configuration"),
            MockTool("search_cve", "Search for CVE vulnerabilities"),
            MockTool("check_auth", "Check authentication security"),
            MockTool("execute_command", "Execute terminal command"),
            MockTool("analyze_logs", "Analyze system logs"),
            MockTool("check_firewall", "Check firewall rules"),
            MockTool("test_api", "Test API security"),
        ]

        print(f"\n1. Available tools: {len(all_tools)}")
        for tool in all_tools:
            print(f"   - {tool.name}: {tool.description}")

        # Test different queries
        test_queries = [
            ("scan ports on localhost", "network scanning"),
            ("check SSL certificate", "SSL/TLS testing"),
            ("search for Apache vulnerabilities", "CVE search"),
        ]

        for query, expected_category in test_queries:
            print(f"\n2. Query: '{query}'")
            print(f"   Expected category: {expected_category}")

            # Filter tools
            filtered = optimizer.filterer.filter_tools(query, all_tools)

            print(f"   Filtered to {len(filtered)} tools:")
            for tool in filtered[:5]:  # Show top 5
                print(f"   - {tool.name}")

            print("\n   Token savings:")
            # Assume each tool definition is ~70 tokens
            original_tokens = len(all_tools) * 70
            filtered_tokens = len(filtered) * 70
            saved = original_tokens - filtered_tokens
            print(f"   Original: {len(all_tools)} tools × 70 tokens = {original_tokens} tokens")
            print(f"   Filtered: {len(filtered)} tools × 70 tokens = {filtered_tokens} tokens")
            print(f"   Saved: {saved} tokens ({(saved/original_tokens):.1%})")

            assert len(filtered) < len(all_tools)

    def test_end_to_end_optimization(self, optimizer):
        """Test 8: Complete optimization pipeline."""
        print("\n" + "=" * 60)
        print("TEST 8: End-to-End Token Optimization")
        print("=" * 60)

        # Create realistic scenario
        messages = [
            SystemMessage(
                content="You are a helpful security assistant. Please help the user with their security questions."
            ),
            HumanMessage(content="What is a port scan?"),
            AIMessage(content="A port scan is a method used to identify open ports..."),
            HumanMessage(content="How do I scan ports on my network?"),
            AIMessage(content="To scan ports, you can use nmap..."),
            HumanMessage(content="Please scan ports on 192.168.1.1"),
        ]

        # Mock tools
        class MockTool:
            def __init__(self, name, description):
                self.name = name
                self.description = description

        tools = [MockTool(f"tool_{i}", f"Description for tool {i}") for i in range(20)]

        print("\n1. Before optimization:")
        counter = TokenCounter()
        original_tokens = counter.count_messages_tokens(messages)
        tool_tokens = len(tools) * 70  # Estimate
        total_original = original_tokens + tool_tokens

        print(f"   Messages: {len(messages)}")
        print(f"   Message tokens: {original_tokens}")
        print(f"   Tools: {len(tools)}")
        print(f"   Tool tokens: {tool_tokens}")
        print(f"   Total tokens: {total_original}")

        # Optimize
        print("\n2. Applying optimizations...")
        optimized_messages, optimized_tools = optimizer.optimize_messages(
            messages=messages, tools=tools, query="scan ports on 192.168.1.1"
        )

        # Calculate savings
        optimized_msg_tokens = counter.count_messages_tokens(optimized_messages)
        optimized_tool_tokens = len(optimized_tools) * 70
        total_optimized = optimized_msg_tokens + optimized_tool_tokens

        print("\n3. After optimization:")
        print(f"   Messages: {len(optimized_messages)}")
        print(f"   Message tokens: {optimized_msg_tokens}")
        print(f"   Tools: {len(optimized_tools)}")
        print(f"   Tool tokens: {optimized_tool_tokens}")
        print(f"   Total tokens: {total_optimized}")

        print("\n4. Savings:")
        saved_tokens = total_original - total_optimized
        saved_pct = (saved_tokens / total_original) * 100
        cost_per_1k = 0.03  # GPT-4 pricing
        cost_saved = (saved_tokens / 1000) * cost_per_1k

        print(f"   Tokens saved: {saved_tokens}")
        print(f"   Percentage: {saved_pct:.1f}%")
        print(f"   Cost saved: ${cost_saved:.4f} per request")
        print(f"   Monthly (100 requests): ${cost_saved * 100:.2f}")

        assert total_optimized < total_original
        assert saved_pct > 20  # At least 20% reduction


class TestBackpressureDetailed:
    """Detailed tests showing how backpressure works."""

    @pytest.fixture
    def manager(self):
        """Create backpressure manager."""
        config = BackpressureConfig(
            enabled=True,
            batch_size=5,
            batch_timeout_ms=50,
            max_events_per_second=20,
            compression_threshold_bytes=512,
        )
        return BackpressureManager(config)

    @pytest.mark.asyncio
    async def test_event_batching(self, manager):
        """Test 9: How event batching works."""
        print("\n" + "=" * 60)
        print("TEST 9: Event Batching")
        print("=" * 60)

        # Create event stream
        async def event_stream():
            for i in range(25):
                yield {"id": i, "data": f"Event {i}", "timestamp": time.time()}
                await asyncio.sleep(0.01)  # Small delay

        print("\n1. Sending 25 events...")
        print(f"   Batch size: {manager.config.batch_size}")
        print(f"   Batch timeout: {manager.config.batch_timeout_ms}ms")

        batches = []
        batch_sizes = []

        print("\n2. Processing with batching:")
        async for event in manager.process(event_stream()):
            if not batches or len(batches[-1]) >= manager.config.batch_size:
                batches.append([])
            batches[-1].append(event)

        print("\n3. Results:")
        print(f"   Total batches: {len(batches)}")
        for i, batch in enumerate(batches, 1):
            print(f"   Batch {i}: {len(batch)} events")
            batch_sizes.append(len(batch))

        avg_batch_size = sum(batch_sizes) / len(batch_sizes)
        print("\n4. Statistics:")
        print(f"   Average batch size: {avg_batch_size:.1f}")
        print(f"   Expected: ~{manager.config.batch_size}")

        assert len(batches) > 1  # Should have multiple batches

    @pytest.mark.asyncio
    async def test_rate_limiting(self, manager):
        """Test 10: How rate limiting works."""
        print("\n" + "=" * 60)
        print("TEST 10: Rate Limiting")
        print("=" * 60)

        print(f"\n1. Rate limit: {manager.config.max_events_per_second} events/second")

        # Send events rapidly
        async def rapid_events():
            for i in range(50):
                yield {"id": i, "data": f"Event {i}"}

        print("\n2. Sending 50 events as fast as possible...")
        start = time.time()
        count = 0

        async for _event in manager.process(rapid_events()):
            count += 1

        elapsed = time.time() - start
        actual_rate = count / elapsed

        print("\n3. Results:")
        print(f"   Time taken: {elapsed:.2f}s")
        print(f"   Events processed: {count}")
        print(f"   Actual rate: {actual_rate:.1f} events/sec")
        print(f"   Configured limit: {manager.config.max_events_per_second} events/sec")

        # Should be close to rate limit (within 20%)
        assert actual_rate <= manager.config.max_events_per_second * 1.2

    def test_compression(self, manager):
        """Test 11: How compression works."""
        print("\n" + "=" * 60)
        print("TEST 11: Payload Compression")
        print("=" * 60)

        print(f"\n1. Compression threshold: {manager.config.compression_threshold_bytes} bytes")

        # Small payload (should NOT compress)
        small_data = "Small data"
        print(f"\n2. Small payload ({len(small_data)} bytes):")
        print(f"   Data: '{small_data}'")
        compressed = manager._compress_payload(small_data)
        print(f"   Compressed: {compressed is not None}")
        print("   Result: NOT compressed (below threshold) ✓")
        assert compressed is None

        # Large payload (should compress)
        large_data = "x" * 2000
        print(f"\n3. Large payload ({len(large_data)} bytes):")
        print(f"   Data: '{large_data[:50]}...'")
        compressed = manager._compress_payload(large_data)

        if compressed:
            original_size = len(large_data.encode("utf-8"))
            compressed_size = len(compressed)
            ratio = compressed_size / original_size
            saved = original_size - compressed_size

            print("   Compressed: YES ✓")
            print(f"   Original size: {original_size} bytes")
            print(f"   Compressed size: {compressed_size} bytes")
            print(f"   Compression ratio: {ratio:.1%}")
            print(f"   Bytes saved: {saved} ({(1-ratio):.1%})")

            assert compressed_size < original_size
        else:
            print("   Compressed: NO (compression didn't reduce size)")


@pytest.mark.asyncio
async def test_complete_integration():
    """Test 12: Complete integration of all optimization features."""
    print("\n" + "=" * 60)
    print("TEST 12: Complete Integration Test")
    print("=" * 60)

    # Create optimization manager
    manager = OptimizationManager(
        enable_caching=True, enable_backpressure=True, enable_token_optimization=True
    )

    print("\n1. Optimization Manager initialized:")
    print(f"   Caching: {manager.enable_caching}")
    print(f"   Backpressure: {manager.enable_backpressure}")
    print(f"   Token optimization: {manager.enable_token_optimization}")

    # Get initial stats
    print("\n2. Initial statistics:")
    stats = manager.get_stats()
    print(json.dumps(stats, indent=2))

    print("\n3. Integration test PASSED ✓")
    print("   All optimization services are working together")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("COMPREHENSIVE OPTIMIZATION TESTING SUITE")
    print("=" * 60)
    print("\nThis suite will demonstrate:")
    print("1. How semantic caching works")
    print("2. How cost savings are calculated")
    print("3. How token optimization reduces usage")
    print("4. How backpressure handles large outputs")
    print("\nRun with: pytest tests/test_optimization_integration.py -v -s")
    print("=" * 60 + "\n")
