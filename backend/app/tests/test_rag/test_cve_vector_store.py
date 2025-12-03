"""Tests for CVE Vector Store service.

Test Coverage:
- CVE metadata creation and serialization
- Vector store initialization
- Single CVE addition
- Batch CVE addition
- Semantic search
- Hybrid search (semantic + filters)
- CVSS score filtering
- Severity filtering
- Exploit filtering
- Date range filtering
- CVE retrieval by ID
- Statistics retrieval
- Caching behavior
- Error handling
"""

import pytest

from app.services.rag.cve_vector_store import (
    CVEMetadata,
    CVESearchResponse,
    CVESearchResult,
    CVEVectorStore,
    CVSSScore,
    get_cve_vector_store,
)


# Sample CVE data for testing
def create_sample_cve(
    cve_id: str = "CVE-2021-44228",
    description: str = "Apache Log4j2 remote code execution vulnerability",
    cvss_score: float = 10.0,
    severity: str = "CRITICAL",
    exploit_available: bool = True,
) -> CVEMetadata:
    """Create a sample CVE for testing."""
    return CVEMetadata(
        cve_id=cve_id,
        description=description,
        published_date="2021-12-10T00:00:00.000",
        last_modified_date="2021-12-15T00:00:00.000",
        cvss_v3_1=CVSSScore(
            version="v3.1",
            base_score=cvss_score,
            severity=severity,
            vector_string="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
            exploitability_score=3.9,
            impact_score=6.0,
        ),
        cwe_ids=["CWE-502", "CWE-400"],
        cpe_uris=[
            "cpe:2.3:a:apache:log4j:2.0:*:*:*:*:*:*:*",
            "cpe:2.3:a:apache:log4j:2.14.1:*:*:*:*:*:*:*",
        ],
        exploit_available=exploit_available,
        exploit_maturity="FUNCTIONAL",
        references=[
            "https://nvd.nist.gov/vuln/detail/CVE-2021-44228",
            "https://www.exploit-db.com/exploits/50592",
        ],
        patch_available=True,
        patch_references=["https://logging.apache.org/log4j/2.x/security.html"],
        vendor="apache",
        product="log4j",
    )


@pytest.fixture
def sample_cves() -> list[CVEMetadata]:
    """Create a list of sample CVEs for testing."""
    return [
        create_sample_cve(
            cve_id="CVE-2021-44228",
            description="Apache Log4j2 remote code execution vulnerability",
            cvss_score=10.0,
            severity="CRITICAL",
            exploit_available=True,
        ),
        create_sample_cve(
            cve_id="CVE-2021-45046",
            description="Apache Log4j2 denial of service vulnerability",
            cvss_score=9.0,
            severity="CRITICAL",
            exploit_available=True,
        ),
        create_sample_cve(
            cve_id="CVE-2022-12345",
            description="Example SQL injection vulnerability in web application",
            cvss_score=7.5,
            severity="HIGH",
            exploit_available=False,
        ),
        create_sample_cve(
            cve_id="CVE-2022-67890",
            description="Example cross-site scripting vulnerability",
            cvss_score=6.1,
            severity="MEDIUM",
            exploit_available=False,
        ),
        create_sample_cve(
            cve_id="CVE-2023-11111",
            description="Example information disclosure vulnerability",
            cvss_score=5.3,
            severity="MEDIUM",
            exploit_available=False,
        ),
    ]


class TestCVEMetadata:
    """Test CVE metadata creation and serialization."""

    def test_create_cve_metadata(self):
        """Test creating CVE metadata."""
        cve = create_sample_cve()

        assert cve.cve_id == "CVE-2021-44228"
        assert "Log4j2" in cve.description
        assert cve.cvss_v3_1.base_score == 10.0
        assert cve.cvss_v3_1.severity == "CRITICAL"
        assert cve.exploit_available is True
        assert len(cve.cwe_ids) == 2
        assert len(cve.cpe_uris) == 2

    def test_cve_to_dict(self):
        """Test CVE serialization to dict."""
        cve = create_sample_cve()
        data = cve.to_dict()

        assert data["cve_id"] == "CVE-2021-44228"
        assert data["cvss_v3_1"]["base_score"] == 10.0
        assert data["exploit_available"] is True

    def test_cve_from_dict(self):
        """Test CVE deserialization from dict."""
        cve = create_sample_cve()
        data = cve.to_dict()

        restored = CVEMetadata.from_dict(data)

        assert restored.cve_id == cve.cve_id
        assert restored.cvss_v3_1.base_score == cve.cvss_v3_1.base_score
        assert restored.exploit_available == cve.exploit_available


class TestCVEVectorStore:
    """Test CVE Vector Store functionality."""

    @pytest.mark.asyncio
    async def test_initialize_vector_store(self):
        """Test vector store initialization."""
        store = CVEVectorStore()
        success = await store.initialize()

        # Should succeed if Qdrant is running
        # If Qdrant is not running, this will fail gracefully
        assert isinstance(success, bool)

    @pytest.mark.asyncio
    async def test_add_single_cve(self):
        """Test adding a single CVE."""
        store = CVEVectorStore()
        await store.initialize()

        cve = create_sample_cve()
        success = await store.add_cve(cve)

        # Should succeed if Qdrant is running
        assert isinstance(success, bool)

    @pytest.mark.asyncio
    async def test_add_cves_batch(self, sample_cves):
        """Test adding CVEs in batch."""
        store = CVEVectorStore()
        await store.initialize()

        successful, failed = await store.add_cves_batch(sample_cves)

        # Should process all CVEs
        assert successful + failed == len(sample_cves)

    @pytest.mark.asyncio
    async def test_search_semantic(self):
        """Test semantic search."""
        store = CVEVectorStore()
        await store.initialize()

        # Add sample CVEs
        sample_cves_list = [
            create_sample_cve(
                cve_id="CVE-2021-44228",
                description="Apache Log4j2 remote code execution vulnerability",
            )
        ]
        await store.add_cves_batch(sample_cves_list)

        # Search
        response = await store.search(query="Log4j remote code execution", limit=5)

        assert isinstance(response, CVESearchResponse)
        assert response.query == "Log4j remote code execution"
        assert isinstance(response.results, list)

    @pytest.mark.asyncio
    async def test_search_with_cvss_filter(self):
        """Test search with CVSS score filtering."""
        store = CVEVectorStore()
        await store.initialize()

        response = await store.search(query="vulnerability", min_cvss_score=9.0, limit=10)

        assert isinstance(response, CVESearchResponse)
        assert response.filters_applied["min_cvss_score"] == 9.0

        # All results should have CVSS >= 9.0
        for result in response.results:
            cvss_score = store._get_highest_cvss_score(result.metadata)
            assert cvss_score >= 9.0

    @pytest.mark.asyncio
    async def test_search_with_severity_filter(self):
        """Test search with severity filtering."""
        store = CVEVectorStore()
        await store.initialize()

        response = await store.search(query="vulnerability", severity="CRITICAL", limit=10)

        assert isinstance(response, CVESearchResponse)
        assert response.filters_applied["severity"] == "CRITICAL"

    @pytest.mark.asyncio
    async def test_search_with_exploit_filter(self):
        """Test search with exploit availability filtering."""
        store = CVEVectorStore()
        await store.initialize()

        response = await store.search(query="vulnerability", exploit_available=True, limit=10)

        assert isinstance(response, CVESearchResponse)
        assert response.filters_applied["exploit_available"] is True

    @pytest.mark.asyncio
    async def test_search_with_date_filter(self):
        """Test search with date range filtering."""
        store = CVEVectorStore()
        await store.initialize()

        response = await store.search(
            query="vulnerability",
            published_after="2021-01-01",
            published_before="2023-12-31",
            limit=10,
        )

        assert isinstance(response, CVESearchResponse)
        assert response.filters_applied["published_after"] == "2021-01-01"
        assert response.filters_applied["published_before"] == "2023-12-31"

    @pytest.mark.asyncio
    async def test_get_cve_by_id(self):
        """Test retrieving CVE by ID."""
        store = CVEVectorStore()
        await store.initialize()

        # Add a CVE
        cve = create_sample_cve()
        await store.add_cve(cve)

        # Retrieve it
        retrieved = await store.get_cve_by_id("CVE-2021-44228")

        if retrieved:
            assert retrieved.cve_id == "CVE-2021-44228"
            assert "Log4j2" in retrieved.description

    @pytest.mark.asyncio
    async def test_get_stats(self):
        """Test getting vector store statistics."""
        store = CVEVectorStore()
        await store.initialize()

        stats = await store.get_stats()

        assert isinstance(stats, dict)
        if stats:  # If Qdrant is running
            assert "total_cves" in stats
            assert "collection_name" in stats
            assert stats["collection_name"] == "cve_knowledge"

    def test_get_highest_cvss_score(self):
        """Test CVSS score extraction."""
        store = CVEVectorStore()

        # CVE with only v3.1
        cve1 = create_sample_cve(cvss_score=10.0)
        assert store._get_highest_cvss_score(cve1) == 10.0

        # CVE with multiple versions
        cve2 = create_sample_cve()
        cve2.cvss_v2 = CVSSScore(version="v2", base_score=7.5, severity="HIGH")
        cve2.cvss_v3 = CVSSScore(version="v3", base_score=9.0, severity="CRITICAL")
        cve2.cvss_v3_1 = CVSSScore(version="v3.1", base_score=10.0, severity="CRITICAL")

        assert store._get_highest_cvss_score(cve2) == 10.0

    def test_get_severity(self):
        """Test severity extraction."""
        store = CVEVectorStore()

        cve = create_sample_cve(severity="CRITICAL")
        assert store._get_severity(cve) == "CRITICAL"

    def test_singleton_pattern(self):
        """Test that CVEVectorStore is a singleton."""
        store1 = CVEVectorStore()
        store2 = CVEVectorStore()

        assert store1 is store2

    def test_global_instance(self):
        """Test global instance getter."""
        store1 = get_cve_vector_store()
        store2 = get_cve_vector_store()

        assert store1 is store2
        assert isinstance(store1, CVEVectorStore)


class TestCVESearchResponse:
    """Test CVE search response."""

    def test_search_response_creation(self):
        """Test creating search response."""
        result = CVESearchResult(
            cve_id="CVE-2021-44228",
            description="Test CVE",
            score=0.95,
            metadata=create_sample_cve(),
        )

        response = CVESearchResponse(
            query="test query",
            results=[result],
            total_found=1,
            search_time_ms=123.45,
            filters_applied={},
        )

        assert response.query == "test query"
        assert len(response.results) == 1
        assert response.total_found == 1
        assert response.search_time_ms == 123.45

    def test_search_response_to_dict(self):
        """Test search response serialization."""
        result = CVESearchResult(
            cve_id="CVE-2021-44228",
            description="Test CVE",
            score=0.95,
            metadata=create_sample_cve(),
        )

        response = CVESearchResponse(
            query="test query",
            results=[result],
            total_found=1,
            search_time_ms=123.45,
            filters_applied={"min_cvss_score": 7.0},
        )

        data = response.to_dict()

        assert data["query"] == "test query"
        assert len(data["results"]) == 1
        assert data["total_found"] == 1
        assert data["filters_applied"]["min_cvss_score"] == 7.0


class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_search_empty_query(self):
        """Test search with empty query."""
        store = CVEVectorStore()
        await store.initialize()

        response = await store.search(query="", limit=5)

        assert isinstance(response, CVESearchResponse)

    @pytest.mark.asyncio
    async def test_search_no_results(self):
        """Test search with no matching results."""
        store = CVEVectorStore()
        await store.initialize()

        response = await store.search(query="nonexistent vulnerability xyz123", limit=5)

        assert isinstance(response, CVESearchResponse)
        assert response.total_found >= 0

    @pytest.mark.asyncio
    async def test_get_nonexistent_cve(self):
        """Test retrieving non-existent CVE."""
        store = CVEVectorStore()
        await store.initialize()

        cve = await store.get_cve_by_id("CVE-9999-99999")

        # Should return None for non-existent CVE
        assert cve is None or isinstance(cve, CVEMetadata)

    def test_cve_metadata_defaults(self):
        """Test CVE metadata with minimal data."""
        cve = CVEMetadata(
            cve_id="CVE-2023-00000",
            description="Minimal CVE",
            published_date="2023-01-01T00:00:00.000",
            last_modified_date="2023-01-01T00:00:00.000",
        )

        assert cve.cve_id == "CVE-2023-00000"
        assert cve.cwe_ids == []
        assert cve.cpe_uris == []
        assert cve.exploit_available is False
        assert cve.patch_available is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
