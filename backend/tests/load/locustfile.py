"""
Load Testing Suite for CMatrix.

This module provides comprehensive load testing scenarios to validate
system performance, identify bottlenecks, and ensure production readiness.

Test Scenarios:
    1. Concurrent chat sessions
    2. Long-running scans
    3. Burst traffic patterns
    4. Cache performance
    5. Backpressure handling
    6. Token optimization effectiveness

Usage:
    # Run basic load test
    locust -f locustfile.py --users 50 --spawn-rate 5 --host http://localhost:8000

    # Run with web UI
    locust -f locustfile.py --host http://localhost:8000

    # Run headless with specific duration
    locust -f locustfile.py --users 100 --spawn-rate 10 --run-time 5m --headless --host http://localhost:8000
"""

import random
import time

from locust import between, events, task
from locust.contrib.fasthttp import FastHttpUser
from loguru import logger

# Test data
SCAN_TARGETS = ["192.168.1.1", "192.168.1.10", "10.0.0.1", "localhost", "scanme.nmap.org"]

CVE_QUERIES = [
    "Apache vulnerabilities",
    "OpenSSL CVE 2024",
    "Linux kernel exploits",
    "WordPress security issues",
    "MySQL vulnerabilities",
]

GENERAL_QUERIES = [
    "What security tools do you have?",
    "How do I scan a network?",
    "Explain CVE scoring",
    "What is a port scan?",
    "How to check SSL certificates?",
]


class CMatrixUser(FastHttpUser):
    """
    Simulates a CMatrix user performing various operations.

    This user class simulates realistic usage patterns including:
    - Chat conversations
    - Security scans
    - CVE searches
    - Knowledge base queries
    """

    # Wait time between tasks (1-3 seconds)
    wait_time = between(1, 3)

    def on_start(self):
        """Called when a user starts. Performs login."""
        # Login to get auth token
        response = self.client.post(
            "/api/v1/auth/login",
            json={
                "username": f"testuser_{self.environment.runner.user_count}",
                "password": "testpass123",
            },
            catch_response=True,
        )

        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access_token")
            self.headers = {"Authorization": f"Bearer {self.token}"}
            response.success()
        elif response.status_code == 404:
            # User doesn't exist, register first
            reg_response = self.client.post(
                "/api/v1/auth/register",
                json={
                    "username": f"testuser_{self.environment.runner.user_count}",
                    "email": f"test{self.environment.runner.user_count}@example.com",
                    "password": "testpass123",
                },
            )

            if reg_response.status_code == 200:
                # Now login
                login_response = self.client.post(
                    "/api/v1/auth/login",
                    json={
                        "username": f"testuser_{self.environment.runner.user_count}",
                        "password": "testpass123",
                    },
                )
                data = login_response.json()
                self.token = data.get("access_token")
                self.headers = {"Authorization": f"Bearer {self.token}"}
                response.success()
            else:
                response.failure(f"Registration failed: {reg_response.status_code}")
        else:
            response.failure(f"Login failed: {response.status_code}")

    @task(3)
    def chat_general_query(self):
        """Send a general chat query (most common operation)."""
        query = random.choice(GENERAL_QUERIES)

        with self.client.post(
            "/api/v1/chat/stream",
            json={"message": query},
            headers=self.headers,
            catch_response=True,
            stream=True,
        ) as response:
            if response.status_code == 200:
                # Read SSE stream
                chunks_received = 0
                for line in response.iter_lines():
                    if line:
                        chunks_received += 1

                if chunks_received > 0:
                    response.success()
                else:
                    response.failure("No SSE chunks received")
            else:
                response.failure(f"Chat failed: {response.status_code}")

    @task(2)
    def perform_scan(self):
        """Perform a network scan (resource-intensive operation)."""
        target = random.choice(SCAN_TARGETS)
        query = f"Scan ports on {target}"

        with self.client.post(
            "/api/v1/chat/stream",
            json={"message": query},
            headers=self.headers,
            catch_response=True,
            stream=True,
            timeout=30,  # Longer timeout for scans
        ) as response:
            if response.status_code == 200:
                chunks_received = 0
                for line in response.iter_lines():
                    if line:
                        chunks_received += 1

                if chunks_received > 0:
                    response.success()
                else:
                    response.failure("No scan results received")
            else:
                response.failure(f"Scan failed: {response.status_code}")

    @task(2)
    def search_cve(self):
        """Search for CVE information."""
        query = random.choice(CVE_QUERIES)

        with self.client.post(
            "/api/v1/chat/stream",
            json={"message": query},
            headers=self.headers,
            catch_response=True,
            stream=True,
        ) as response:
            if response.status_code == 200:
                chunks_received = 0
                for line in response.iter_lines():
                    if line:
                        chunks_received += 1

                if chunks_received > 0:
                    response.success()
                else:
                    response.failure("No CVE results received")
            else:
                response.failure(f"CVE search failed: {response.status_code}")

    @task(1)
    def check_optimization_stats(self):
        """Check optimization statistics (monitoring)."""
        with self.client.get(
            "/api/v1/optimization/stats", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code == 200:
                stats = response.json()
                # Validate stats structure
                if "cache" in stats or "token_optimization" in stats:
                    response.success()
                else:
                    response.failure("Invalid stats structure")
            else:
                response.failure(f"Stats check failed: {response.status_code}")


class BurstTrafficUser(FastHttpUser):
    """
    Simulates burst traffic patterns.

    This user sends rapid requests to test backpressure handling
    and rate limiting.
    """

    wait_time = between(0.1, 0.5)  # Very short wait time

    def on_start(self):
        """Login before starting."""
        response = self.client.post(
            "/api/v1/auth/login", json={"username": "burstuser", "password": "testpass123"}
        )

        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access_token")
            self.headers = {"Authorization": f"Bearer {self.token}"}

    @task
    def rapid_fire_queries(self):
        """Send rapid queries to test backpressure."""
        query = random.choice(GENERAL_QUERIES)

        self.client.post(
            "/api/v1/chat/stream", json={"message": query}, headers=self.headers, stream=True
        )


class CacheTestUser(FastHttpUser):
    """
    Tests semantic cache performance.

    Sends similar queries to test cache hit rates.
    """

    wait_time = between(1, 2)

    # Repeated queries to test caching
    CACHE_QUERIES = [
        "What is a port scan?",
        "What's a port scan?",
        "Explain port scanning",
        "How does port scanning work?",
        "Tell me about port scans",
    ]

    def on_start(self):
        """Login before starting."""
        response = self.client.post(
            "/api/v1/auth/login", json={"username": "cacheuser", "password": "testpass123"}
        )

        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access_token")
            self.headers = {"Authorization": f"Bearer {self.token}"}

    @task
    def test_cache_hits(self):
        """Send similar queries to test cache."""
        query = random.choice(self.CACHE_QUERIES)

        start_time = time.time()

        with self.client.post(
            "/api/v1/chat/stream",
            json={"message": query},
            headers=self.headers,
            catch_response=True,
            stream=True,
        ) as response:
            if response.status_code == 200:
                for _ in response.iter_lines():
                    pass

                response_time = time.time() - start_time

                # Cache hits should be < 200ms
                if response_time < 0.2:
                    response.success()
                    logger.info(f"Likely cache HIT: {response_time:.3f}s")
                else:
                    response.success()
                    logger.info(f"Likely cache MISS: {response_time:.3f}s")
            else:
                response.failure(f"Request failed: {response.status_code}")


# Event handlers for custom metrics
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Called when test starts."""
    logger.info("🚀 Load test starting...")
    logger.info(f"Target host: {environment.host}")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Called when test stops."""
    logger.info("🏁 Load test completed")

    # Print summary statistics
    stats = environment.stats
    logger.info(f"Total requests: {stats.total.num_requests}")
    logger.info(f"Total failures: {stats.total.num_failures}")
    logger.info(f"Average response time: {stats.total.avg_response_time:.2f}ms")
    logger.info(f"Requests per second: {stats.total.total_rps:.2f}")


@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    """Called on every request."""
    if exception:
        logger.error(f"Request failed: {name} - {exception}")
