import time
from datetime import datetime, timedelta
from typing import Any, Optional

import requests
from loguru import logger

from app.services.rag.cve_vector_store import CVEMetadata, CVEVectorStore, CVSSScore


class NVDSyncService:
    """Service for syncing CVE data from NVD API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize NVD sync service.

        Args:
            api_key: Optional NVD API key for higher rate limits
        """
        self.base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.api_key = api_key
        self.headers = {}
        if api_key:
            self.headers["apiKey"] = api_key

        # Rate limiting
        self.requests_per_30s = 5 if not api_key else 50
        self.request_times: list[float] = []

    def _rate_limit(self):
        """Enforce rate limiting."""
        now = time.time()

        # Remove requests older than 30 seconds
        self.request_times = [t for t in self.request_times if now - t < 30]

        # If we've hit the limit, wait
        if len(self.request_times) >= self.requests_per_30s:
            sleep_time = 30 - (now - self.request_times[0])
            if sleep_time > 0:
                logger.info(f"Rate limit reached, sleeping for {sleep_time:.1f}s")
                time.sleep(sleep_time)
                self.request_times = []

        self.request_times.append(now)

    def fetch_cves(
        self,
        start_index: int = 0,
        results_per_page: int = 2000,
        pub_start_date: Optional[str] = None,
        pub_end_date: Optional[str] = None,
        mod_start_date: Optional[str] = None,
        mod_end_date: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Fetch CVEs from NVD API.

        Args:
            start_index: Starting index for pagination
            results_per_page: Number of results per page (max 2000)
            pub_start_date: Filter by published date (ISO format)
            pub_end_date: Filter by published date (ISO format)
            mod_start_date: Filter by modified date (ISO format)
            mod_end_date: Filter by modified date (ISO format)

        Returns:
            API response data
        """
        self._rate_limit()

        params = {"startIndex": start_index, "resultsPerPage": min(results_per_page, 2000)}

        if pub_start_date:
            params["pubStartDate"] = pub_start_date
        if pub_end_date:
            params["pubEndDate"] = pub_end_date
        if mod_start_date:
            params["modStartDate"] = mod_start_date
        if mod_end_date:
            params["modEndDate"] = mod_end_date

        try:
            response = requests.get(self.base_url, params=params, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch CVEs: {e}")
            return {}

    def parse_cve(self, cve_item: dict[str, Any]) -> Optional[CVEMetadata]:
        """
        Parse a CVE item from NVD API response.

        Args:
            cve_item: CVE item from API

        Returns:
            CVEMetadata or None if parsing fails
        """
        try:
            cve = cve_item.get("cve", {})
            cve_id = cve.get("id", "")

            # Get description
            descriptions = cve.get("descriptions", [])
            description = next((d["value"] for d in descriptions if d.get("lang") == "en"), "")

            # Get dates
            published = cve.get("published", "")
            modified = cve.get("lastModified", "")

            # Get CVSS scores
            metrics = cve.get("metrics", {})

            cvss_v2 = None
            if "cvssMetricV2" in metrics and metrics["cvssMetricV2"]:
                v2_data = metrics["cvssMetricV2"][0]["cvssData"]
                cvss_v2 = CVSSScore(
                    version="v2",
                    base_score=v2_data.get("baseScore", 0.0),
                    severity=v2_data.get("baseSeverity", "UNKNOWN"),
                    vector_string=v2_data.get("vectorString"),
                    exploitability_score=v2_data.get("exploitabilityScore"),
                    impact_score=v2_data.get("impactScore"),
                )

            cvss_v3 = None
            if "cvssMetricV30" in metrics and metrics["cvssMetricV30"]:
                v3_data = metrics["cvssMetricV30"][0]["cvssData"]
                cvss_v3 = CVSSScore(
                    version="v3",
                    base_score=v3_data.get("baseScore", 0.0),
                    severity=v3_data.get("baseSeverity", "UNKNOWN"),
                    vector_string=v3_data.get("vectorString"),
                    exploitability_score=v3_data.get("exploitabilityScore"),
                    impact_score=v3_data.get("impactScore"),
                )

            cvss_v3_1 = None
            if "cvssMetricV31" in metrics and metrics["cvssMetricV31"]:
                v31_data = metrics["cvssMetricV31"][0]["cvssData"]
                cvss_v3_1 = CVSSScore(
                    version="v3.1",
                    base_score=v31_data.get("baseScore", 0.0),
                    severity=v31_data.get("baseSeverity", "UNKNOWN"),
                    vector_string=v31_data.get("vectorString"),
                    exploitability_score=v31_data.get("exploitabilityScore"),
                    impact_score=v31_data.get("impactScore"),
                )

            # Get CWE IDs
            weaknesses = cve.get("weaknesses", [])
            cwe_ids = []
            for weakness in weaknesses:
                for desc in weakness.get("description", []):
                    if desc.get("lang") == "en":
                        cwe_ids.append(desc.get("value", ""))

            # Get CPE URIs
            configurations = cve.get("configurations", [])
            cpe_uris = []
            for config in configurations:
                for node in config.get("nodes", []):
                    for cpe_match in node.get("cpeMatch", []):
                        if cpe_match.get("vulnerable", True):
                            cpe_uris.append(cpe_match.get("criteria", ""))

            # Get references
            references = [ref.get("url", "") for ref in cve.get("references", [])]

            # Detect exploit availability (heuristic)
            exploit_keywords = ["exploit", "poc", "proof of concept", "metasploit", "exploit-db"]
            exploit_available = any(
                any(keyword in ref.lower() for keyword in exploit_keywords) for ref in references
            )

            # Detect patch availability (heuristic)
            patch_keywords = ["patch", "fix", "update", "advisory", "security bulletin"]
            patch_refs = [
                ref
                for ref in references
                if any(keyword in ref.lower() for keyword in patch_keywords)
            ]
            patch_available = len(patch_refs) > 0

            # Extract vendor/product from CPE (first one)
            vendor = None
            product = None
            if cpe_uris:
                # CPE format: cpe:2.3:part:vendor:product:version:...
                parts = cpe_uris[0].split(":")
                if len(parts) >= 5:
                    vendor = parts[3]
                    product = parts[4]

            return CVEMetadata(
                cve_id=cve_id,
                description=description,
                published_date=published,
                last_modified_date=modified,
                cvss_v2=cvss_v2,
                cvss_v3=cvss_v3,
                cvss_v3_1=cvss_v3_1,
                cwe_ids=cwe_ids,
                cpe_uris=cpe_uris,
                exploit_available=exploit_available,
                references=references,
                patch_available=patch_available,
                patch_references=patch_refs,
                vendor=vendor,
                product=product,
            )
        except Exception as e:
            logger.error(f"Failed to parse CVE: {e}")
            return None

    async def sync_full(self, vector_store: CVEVectorStore, max_cves: Optional[int] = None) -> int:
        """
        Perform full sync of all CVEs.

        Args:
            vector_store: CVE vector store instance
            max_cves: Maximum number of CVEs to sync (for testing)

        Returns:
            Number of CVEs synced
        """
        logger.info("🚀 Starting full CVE sync from NVD")

        start_index = 0
        results_per_page = 2000
        total_synced = 0

        while True:
            if max_cves and total_synced >= max_cves:
                logger.info(f"Reached max CVEs limit: {max_cves}")
                break

            logger.info(f"Fetching CVEs {start_index} to {start_index + results_per_page}")

            data = self.fetch_cves(start_index=start_index, results_per_page=results_per_page)

            if not data or "vulnerabilities" not in data:
                logger.warning("No more CVEs to fetch")
                break

            vulnerabilities = data["vulnerabilities"]
            if not vulnerabilities:
                logger.info("No more vulnerabilities in response")
                break

            # Parse CVEs
            cves = []
            for vuln in vulnerabilities:
                cve = self.parse_cve(vuln)
                if cve:
                    cves.append(cve)

            # Store in batches
            if cves:
                successful, failed = await vector_store.add_cves_batch(cves)
                total_synced += successful
                logger.info(
                    f"✅ Synced {successful} CVEs (failed: {failed}), total: {total_synced}"
                )

            # Check if we've reached the end
            total_results = data.get("totalResults", 0)
            if start_index + results_per_page >= total_results:
                logger.info(f"Reached end of results (total: {total_results})")
                break

            start_index += results_per_page

        logger.info(f"🎉 Full sync complete! Total CVEs synced: {total_synced}")
        return total_synced

    async def sync_incremental(self, vector_store: CVEVectorStore, days: int = 7) -> int:
        """
        Perform incremental sync of recent CVEs.

        Args:
            vector_store: CVE vector store instance
            days: Number of days to look back

        Returns:
            Number of CVEs synced
        """
        logger.info(f"🚀 Starting incremental CVE sync (last {days} days)")

        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        # Format dates for NVD API (ISO 8601)
        mod_start_date = start_date.strftime("%Y-%m-%dT%H:%M:%S.000")
        mod_end_date = end_date.strftime("%Y-%m-%dT%H:%M:%S.000")

        logger.info(f"Fetching CVEs modified between {mod_start_date} and {mod_end_date}")

        start_index = 0
        results_per_page = 2000
        total_synced = 0

        while True:
            data = self.fetch_cves(
                start_index=start_index,
                results_per_page=results_per_page,
                mod_start_date=mod_start_date,
                mod_end_date=mod_end_date,
            )

            if not data or "vulnerabilities" not in data:
                break

            vulnerabilities = data["vulnerabilities"]
            if not vulnerabilities:
                break

            # Parse CVEs
            cves = []
            for vuln in vulnerabilities:
                cve = self.parse_cve(vuln)
                if cve:
                    cves.append(cve)

            # Store in batches
            if cves:
                successful, failed = await vector_store.add_cves_batch(cves)
                total_synced += successful
                logger.info(
                    f"✅ Synced {successful} CVEs (failed: {failed}), total: {total_synced}"
                )

            # Check if we've reached the end
            total_results = data.get("totalResults", 0)
            if start_index + results_per_page >= total_results:
                break

            start_index += results_per_page

        logger.info(f"🎉 Incremental sync complete! Total CVEs synced: {total_synced}")
        return total_synced
