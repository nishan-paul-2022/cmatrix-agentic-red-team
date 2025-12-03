import asyncio
from typing import Any, Optional

import networkx as nx
import requests
from loguru import logger


class CVEGraphTraversal:
    """
    Service for traversing CVE relationships to discover hidden vulnerabilities.
    Builds a graph where nodes are CVEs and edges represent relationships
    (e.g., shared CPE, shared CWE, direct references).
    """

    def __init__(self, nvd_api_key: Optional[str] = None):
        self.graph = nx.DiGraph()
        self.nvd_api_key = nvd_api_key
        self.base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.headers = {"User-Agent": "CMatrix-Security-Agent/1.0"}
        if nvd_api_key:
            self.headers["apiKey"] = nvd_api_key

        # Cache to prevent redundant API calls during a single traversal session
        self._cache: dict[str, dict] = {}

    async def build_graph(self, start_cve_id: str, max_depth: int = 2) -> dict[str, Any]:
        """
        Build a graph of related CVEs starting from a given CVE ID.

        Args:
            start_cve_id: The CVE ID to start traversal from (e.g., "CVE-2021-44228")
            max_depth: Maximum number of hops to traverse (default: 2)

        Returns:
            Dictionary representation of the graph (nodes and links)
        """
        logger.info(f"Starting CVE graph traversal from {start_cve_id} with depth {max_depth}")
        self.graph.clear()
        self._cache.clear()

        # Queue for BFS: (cve_id, current_depth)
        queue = [(start_cve_id, 0)]
        visited = set()

        while queue:
            current_cve_id, depth = queue.pop(0)

            if current_cve_id in visited:
                continue

            visited.add(current_cve_id)

            # Fetch CVE details
            cve_data = await self._fetch_cve_details(current_cve_id)
            if not cve_data:
                logger.warning(f"Could not fetch details for {current_cve_id}")
                continue

            # Add node to graph
            self._add_cve_node(current_cve_id, cve_data)

            # Stop if we reached max depth
            if depth >= max_depth:
                continue

            # Find related CVEs
            related_cves = self._find_related_cves(cve_data)

            for related_id, relation_type in related_cves:
                if related_id not in visited:
                    self.graph.add_edge(current_cve_id, related_id, relation=relation_type)
                    queue.append((related_id, depth + 1))

        return nx.node_link_data(self.graph)

    async def _fetch_cve_details(self, cve_id: str) -> Optional[dict]:
        """Fetch CVE details from NVD API or cache."""
        if cve_id in self._cache:
            return self._cache[cve_id]

        try:
            # In a real async implementation, we'd use aiohttp.
            # For now, wrapping requests in asyncio.to_thread to avoid blocking
            params = {"cveId": cve_id}
            response = await asyncio.to_thread(
                requests.get, self.base_url, params=params, headers=self.headers, timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                vulnerabilities = data.get("vulnerabilities", [])
                if vulnerabilities:
                    cve_item = vulnerabilities[0].get("cve", {})
                    self._cache[cve_id] = cve_item
                    return cve_item
            elif response.status_code == 403 or response.status_code == 429:
                logger.warning(f"Rate limited by NVD API for {cve_id}")
                # Simple backoff could be added here

            return None
        except Exception as e:
            logger.error(f"Error fetching CVE {cve_id}: {str(e)}")
            return None

    def _add_cve_node(self, cve_id: str, data: dict):
        """Add a CVE node with metadata to the graph."""
        description = "No description"
        descriptions = data.get("descriptions", [])
        if descriptions:
            description = descriptions[0].get("value", "No description")

        metrics = data.get("metrics", {})
        cvss_score = 0.0
        severity = "UNKNOWN"

        # Try V3.1, then V3.0, then V2
        if "cvssMetricV31" in metrics:
            cvss_data = metrics["cvssMetricV31"][0].get("cvssData", {})
            cvss_score = cvss_data.get("baseScore", 0.0)
            severity = cvss_data.get("baseSeverity", "UNKNOWN")
        elif "cvssMetricV30" in metrics:
            cvss_data = metrics["cvssMetricV30"][0].get("cvssData", {})
            cvss_score = cvss_data.get("baseScore", 0.0)
            severity = cvss_data.get("baseSeverity", "UNKNOWN")
        elif "cvssMetricV2" in metrics:
            cvss_data = metrics["cvssMetricV2"][0].get("cvssData", {})
            cvss_score = cvss_data.get("baseScore", 0.0)
            severity = cvss_data.get("baseSeverity", "UNKNOWN")

        self.graph.add_node(
            cve_id,
            description=description[:100] + "..." if len(description) > 100 else description,
            score=cvss_score,
            severity=severity,
            published=data.get("published", ""),
            last_modified=data.get("lastModified", ""),
        )

    def _find_related_cves(self, cve_data: dict) -> list[tuple]:
        """
        Identify related CVEs based on:
        1. References (often link to other CVEs)
        2. Shared CWEs (weakness types) - *Optional, can be noisy*
        3. Shared CPEs (affected products) - *Optional, can be very noisy*

        For this implementation, we focus on direct references and explicit relationships.
        """
        related = []

        # 1. Check references for other CVE IDs
        references = cve_data.get("references", [])
        for ref in references:
            url = ref.get("url", "")
            # Simple heuristic to find CVEs in URLs
            if "CVE-" in url:
                # Extract CVE ID (simple regex-like logic)
                parts = url.split("CVE-")
                if len(parts) > 1:
                    potential_id = "CVE-" + parts[1].split("/")[0].split(".")[0]
                    # Basic validation of format CVE-YYYY-NNNN...
                    if len(potential_id) >= 13 and potential_id != cve_data.get("id"):
                        related.append((potential_id, "referenced_in_url"))

        # 2. Check for Weakness (CWE) relationships
        # Note: Traversing by CWE can lead to massive graphs (all SQLi bugs are related).
        # We might want to limit this or only use it for specific analysis.
        # For now, we'll skip implicit CWE traversal to keep the graph focused.

        return related

    def get_critical_path(self) -> list[str]:
        """
        Identify the most critical path in the graph based on CVSS scores.
        """
        if not self.graph:
            return []

        # Simple heuristic: find the node with highest score
        nodes_by_score = sorted(
            self.graph.nodes(data=True), key=lambda x: x[1].get("score", 0), reverse=True
        )

        return [n[0] for n in nodes_by_score[:5]]
