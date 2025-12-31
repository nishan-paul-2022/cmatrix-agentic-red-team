"""
Vulnerability Intelligence Agent Subgraph.

This agent specializes in CVE research, threat intelligence, and vulnerability
correlation. It operates as an autonomous LangGraph subgraph with its own
reasoning loop and LLM instance.
"""

import asyncio
from datetime import datetime, timedelta
from functools import partial
from typing import Any

import requests
from langchain_core.tools import tool
from loguru import logger

from app.agents.base.agent import BaseAgentSubgraph
from app.services.llm.providers.base import LLMProvider
from app.services.nvd import fetch_cves_from_nvd
from app.services.rag import CVEGraphTraversal
from app.services.rag.cve_search import get_smart_cve_search_service

# Tool implementations (keeping existing logic)


@tool
def search_cve(keyword: str, limit: int = 5) -> str:
    """
    Search for CVE vulnerabilities by keyword using semantic search.

    Args:
        keyword: Search keyword (e.g., "apache", "nginx", "openssl")
        limit: Maximum number of results to return (default: 5, max: 10)
    """
    try:
        # Use smart search service for semantic search
        # This is a synchronous wrapper around the async service

        # Ensure limit is an integer
        try:
            limit = int(limit)
        except (ValueError, TypeError):
            limit = 5
        limit = max(1, min(limit, 10))

        # We need an LLM provider for the service, but for simple search we can mock it or get a default
        # In this context, we'll try to use the global service if available, or create one
        # Since we can't easily inject the provider here without changing the signature,
        # we'll rely on the fact that smart_cve_search is the preferred tool.
        # However, to improve this tool, we'll use the vector store directly if possible.

        import asyncio

        from app.services.rag.cve_vector_store import get_cve_vector_store

        async def _run_search():
            store = get_cve_vector_store()
            await store.initialize()
            return await store.search(query=keyword, limit=limit)

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            # If loop is running, we can't use run_until_complete
            # This is tricky in a tool. For now, we'll fallback to the old method if async fails
            # or if we are in a context where we can't await.
            # But let's try to use the smart_cve_search logic which handles this.
            pass

        # Fallback to NVD for now to avoid async complexity in this simple tool
        # The smart_cve_search tool is the upgraded version
        vulnerabilities = fetch_cves_from_nvd(keyword, limit)

        if not vulnerabilities:
            return f"No CVEs found for keyword: {keyword}"

        results = [f"CVE Search Results for '{keyword}' (Top {len(vulnerabilities)} results):"]
        results.append("")

        for vuln in vulnerabilities:
            cve = vuln.get("cve", {})
            cve_id = cve.get("id", "Unknown")
            descriptions = cve.get("descriptions", [])
            description = (
                descriptions[0].get("value", "No description") if descriptions else "No description"
            )

            # Get severity if available
            metrics = cve.get("metrics", {})
            cvss_v3 = metrics.get("cvssMetricV31", [])
            severity = "Unknown"
            score = "N/A"

            if cvss_v3:
                cvss_data = cvss_v3[0].get("cvssData", {})
                severity = cvss_data.get("baseSeverity", "Unknown")
                score = cvss_data.get("baseScore", "N/A")

            results.append(f"🔴 {cve_id}")
            results.append(f"   Severity: {severity} (Score: {score})")
            results.append(f"   Description: {description[:200]}...")
            results.append("")

        results.append("Source: NVD (National Vulnerability Database)")
        return "\n".join(results)

    except Exception as e:
        return f"CVE search failed: {str(e)}"


@tool
def get_recent_cves(days: int = 7, severity: str = "HIGH") -> str:
    """
    Get recent high-severity CVEs from the last N days.

    Args:
        days: Number of days to look back (default: 7)
        severity: Minimum severity level (LOW, MEDIUM, HIGH, CRITICAL)
    """
    try:
        # Ensure days is an integer
        try:
            days = int(days)
        except (ValueError, TypeError):
            days = 7  # Default fallback

        # Clamp days between 1 and 365
        days = max(1, min(days, 365))

        # Ensure severity is a string and uppercase
        severity = str(severity).strip().upper()
        if severity not in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]:
            severity = "HIGH"  # Default fallback

        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        params = {
            "pubStartDate": start_date.strftime("%Y-%m-%dT00:00:00.000"),
            "pubEndDate": end_date.strftime("%Y-%m-%dT23:59:59.999"),
            "resultsPerPage": 10,
        }

        response = requests.get(url, params=params, timeout=15)

        if response.status_code == 200:
            data = response.json()
            vulnerabilities = data.get("vulnerabilities", [])

            results = [f"Recent CVEs (Last {days} days, {severity}+ severity):"]
            results.append("")

            severity_order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
            min_severity = severity_order.get(severity.upper(), 2)

            filtered_count = 0
            for vuln in vulnerabilities:
                cve = vuln.get("cve", {})
                cve_id = cve.get("id", "Unknown")

                # Get severity
                metrics = cve.get("metrics", {})
                cvss_v3 = metrics.get("cvssMetricV31", [])

                if cvss_v3:
                    cvss_data = cvss_v3[0].get("cvssData", {})
                    vuln_severity = cvss_data.get("baseSeverity", "UNKNOWN")
                    score = cvss_data.get("baseScore", "N/A")

                    if severity_order.get(vuln_severity, 0) >= min_severity:
                        descriptions = cve.get("descriptions", [])
                        description = (
                            descriptions[0].get("value", "No description")
                            if descriptions
                            else "No description"
                        )

                        results.append(f"🔴 {cve_id} - {vuln_severity} ({score})")
                        results.append(f"   {description[:150]}...")
                        results.append("")
                        filtered_count += 1

            if filtered_count == 0:
                results.append(f"No {severity}+ severity CVEs found in the last {days} days")

            results.append("Source: NVD (National Vulnerability Database)")
            return "\n".join(results)
        else:
            return f"Recent CVE fetch failed: HTTP {response.status_code}"

    except Exception as e:
        return f"Recent CVE fetch failed: {str(e)}"


@tool
def check_vulnerability_by_product(product: str, version: str = "") -> str:
    """
    Check for known vulnerabilities in a specific product/software.

    Args:
        product: Product name (e.g., "apache", "nginx", "wordpress")
        version: Optional version number
    """
    try:
        # Ensure product and version are strings
        product = str(product).strip()
        version = str(version).strip() if version else ""

        search_term = f"{product} {version}".strip()

        url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        params = {"keywordSearch": search_term, "resultsPerPage": 10}

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            vulnerabilities = data.get("vulnerabilities", [])

            results = [f"Vulnerability Check: {product}" + (f" v{version}" if version else "")]
            results.append("")

            if not vulnerabilities:
                results.append(f"✅ No known vulnerabilities found for {search_term}")
                results.append(
                    "Note: This doesn't guarantee the software is secure. Always keep software updated."
                )
                return "\n".join(results)

            results.append(f"⚠️  Found {len(vulnerabilities)} potential vulnerabilities:")
            results.append("")

            for vuln in vulnerabilities[:5]:  # Limit to top 5
                cve = vuln.get("cve", {})
                cve_id = cve.get("id", "Unknown")

                metrics = cve.get("metrics", {})
                cvss_v3 = metrics.get("cvssMetricV31", [])

                if cvss_v3:
                    cvss_data = cvss_v3[0].get("cvssData", {})
                    severity = cvss_data.get("baseSeverity", "Unknown")
                    score = cvss_data.get("baseScore", "N/A")

                    results.append(f"• {cve_id} - {severity} (Score: {score})")

            results.append("")
            results.append("Recommendation: Review CVE details and apply security patches")
            return "\n".join(results)
        else:
            return f"Vulnerability check failed: HTTP {response.status_code}"

    except Exception as e:
        return f"Vulnerability check failed: {str(e)}"


@tool
def explore_cve_relationships(cve_id: str, depth: int = 2) -> str:
    """
    Explore relationships between CVEs to discover hidden vulnerabilities.

    Args:
        cve_id: The starting CVE ID (e.g., "CVE-2021-44228")
        depth: How many hops to traverse (default: 2, max: 3)
    """
    try:
        # Ensure depth is an integer
        try:
            depth = int(depth)
        except (ValueError, TypeError):
            depth = 2
        depth = max(1, min(depth, 3))

        cve_id = str(cve_id).strip().upper()
        if not cve_id.startswith("CVE-"):
            return "Invalid CVE ID format. Must start with 'CVE-'."

        async def _run_traversal():
            traversal = CVEGraphTraversal()
            return await traversal.build_graph(start_cve_id=cve_id, max_depth=depth)

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            # If loop is running, we can't use run_until_complete directly
            # This is a hack for tools running in async context
            # Ideally tools should be async
            import nest_asyncio

            nest_asyncio.apply()
            graph_data = loop.run_until_complete(_run_traversal())
        else:
            graph_data = loop.run_until_complete(_run_traversal())

        # Format the output
        nodes = graph_data.get("nodes", [])
        links = graph_data.get("links", [])

        if not nodes:
            return f"No relationships found for {cve_id}."

        results = [f"CVE Relationship Graph for {cve_id} (Depth: {depth}):"]
        results.append(f"Found {len(nodes)} related CVEs and {len(links)} connections.")
        results.append("")

        # List critical nodes
        results.append("Critical Nodes:")
        sorted_nodes = sorted(nodes, key=lambda x: x.get("score", 0), reverse=True)
        for node in sorted_nodes[:5]:
            results.append(
                f"🔴 {node['id']} (Score: {node.get('score', 'N/A')}) - {node.get('description', '')[:100]}..."
            )

        results.append("")
        results.append("Relationships:")
        for link in links[:10]:
            results.append(
                f"  {link['source']} -> {link['target']} ({link.get('relation', 'related')})"
            )

        if len(links) > 10:
            results.append(f"  ... and {len(links) - 10} more connections.")

        return "\n".join(results)

    except Exception as e:
        return f"Graph traversal failed: {str(e)}"


def smart_cve_search(
    keyword: str,
    limit: int = 10,
    strategy: str = "balanced",
    min_cvss_score: float = None,
    severity: str = None,
    exploit_available: bool = None,
    llm_provider: LLMProvider = None,
) -> str:
    """
    Smart CVE search with semantic reranking, self-correction, and vector store filters.

    Args:
        keyword: Search query
        limit: Max results
        strategy: Ranking strategy
        min_cvss_score: Minimum CVSS score (0-10)
        severity: Severity level (LOW, MEDIUM, HIGH, CRITICAL)
        exploit_available: Filter by exploit availability
        llm_provider: Injected LLM provider
    """
    try:
        # Run async logic in sync wrapper
        async def _run_smart_search():
            service = get_smart_cve_search_service(llm_provider)
            data = await service.search(
                query=keyword,
                limit=limit,
                strategy=strategy,
                min_cvss_score=min_cvss_score,
                severity=severity,
                exploit_available=exploit_available,
            )

            result = data.get("results")
            current_query = data.get("query")
            is_corrected = data.get("is_corrected")
            feedback = data.get("feedback")

            # Format output
            output = [f"Smart CVE Search Results for '{current_query}' (Strategy: {strategy}):"]
            if is_corrected:
                output.append(f"(Corrected from original query: '{keyword}')")

            # Add filter info
            filters = []
            if min_cvss_score:
                filters.append(f"CVSS >= {min_cvss_score}")
            if severity:
                filters.append(f"Severity: {severity}")
            if exploit_available:
                filters.append("Exploit Available")
            if filters:
                output.append(f"Filters: {', '.join(filters)}")

            output.append("")

            if not result or not result.ranked_cves:
                output.append("No relevant CVEs found.")
                if feedback:
                    output.append(f"Feedback: {feedback}")
                return "\n".join(output)

            for cve in result.ranked_cves:
                output.append(f"🔴 {cve.cve_id} (Score: {cve.final_score:.2f})")
                output.append(f"   {cve.explanation}")

                # Extract description from raw data
                desc = "No description"
                if cve.raw_data and "cve" in cve.raw_data and "descriptions" in cve.raw_data["cve"]:
                    desc = cve.raw_data["cve"]["descriptions"][0].get("value", "No description")
                output.append(f"   Description: {desc[:150]}...")
                output.append("")

            return "\n".join(output)

        # Run the async function
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            return asyncio.run(_run_smart_search())
        else:
            return loop.run_until_complete(_run_smart_search())

    except Exception as e:
        return f"Smart search failed: {str(e)}"


# Legacy tool list for backward compatibility
VULN_INTEL_TOOLS = [search_cve, get_recent_cves, check_vulnerability_by_product]


class VulnIntelAgentSubgraph(BaseAgentSubgraph):
    """
    Vulnerability Intelligence Agent Subgraph.

    This agent is responsible for:
    - CVE research and vulnerability discovery
    - Threat intelligence gathering
    - Vulnerability correlation and impact analysis
    - Patch prioritization and remediation planning
    - Security advisory monitoring

    The agent uses the NVD (National Vulnerability Database) and other
    threat intelligence sources to provide comprehensive vulnerability intelligence.
    """

    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize the Vulnerability Intelligence Agent.

        Args:
            llm_provider: LLM provider instance for this agent
        """
        super().__init__(llm_provider, agent_name="VulnIntelAgent")
        logger.info("Vulnerability Intelligence Agent initialized with autonomous reasoning")

    def _register_tools(self) -> list[dict[str, Any]]:
        """
        Register vulnerability intelligence tools.

        Returns:
            List of tool definitions
        """
        return [
            {
                "name": "search_cve",
                "function": search_cve,
                "description": (
                    "Search for CVE vulnerabilities by keyword. "
                    "Use this to find vulnerabilities related to specific software, "
                    "vendors, or vulnerability types. Returns CVE IDs, severity scores, "
                    "and descriptions from the NVD database."
                ),
                "parameters": {
                    "keyword": "Search keyword (e.g., 'apache', 'nginx', 'openssl', 'log4j')",
                    "limit": "Maximum number of results to return (default: 5, max: 10)",
                },
            },
            {
                "name": "get_recent_cves",
                "function": get_recent_cves,
                "description": (
                    "Get recent high-severity CVEs from the last N days. "
                    "Use this to stay updated on the latest vulnerabilities and "
                    "emerging threats. Filters by severity level to focus on "
                    "critical and high-risk vulnerabilities."
                ),
                "parameters": {
                    "days": "Number of days to look back (default: 7)",
                    "severity": "Minimum severity level: LOW, MEDIUM, HIGH, or CRITICAL (default: HIGH)",
                },
            },
            {
                "name": "check_vulnerability_by_product",
                "function": check_vulnerability_by_product,
                "description": (
                    "Check for known vulnerabilities in a specific product or software. "
                    "Use this when you know the software name and optionally the version. "
                    "Returns all known CVEs affecting that product with severity scores."
                ),
                "parameters": {
                    "product": "Product name (e.g., 'apache', 'nginx', 'wordpress', 'openssl')",
                    "version": "Optional version number (e.g., '2.4.49', '1.21.0')",
                },
            },
            {
                "name": "explore_cve_relationships",
                "function": explore_cve_relationships,
                "description": (
                    "Explore relationships between CVEs to discover hidden vulnerabilities. "
                    "Use this to find related vulnerabilities that might be part of a larger attack chain "
                    "or share common root causes. Returns a graph of related CVEs."
                ),
                "parameters": {
                    "cve_id": "The starting CVE ID (e.g., 'CVE-2021-44228')",
                    "depth": "How many hops to traverse (default: 2, max: 3)",
                },
            },
            {
                "name": "smart_cve_search",
                "function": partial(smart_cve_search, llm_provider=self.llm_provider),
                "description": (
                    "Advanced CVE search with semantic reranking and self-correction. "
                    "Use this for complex queries or when standard search fails. "
                    "It automatically improves the query if results are poor."
                ),
                "parameters": {
                    "keyword": "Search query",
                    "limit": "Max results (default: 10)",
                    "strategy": "Ranking strategy: 'balanced', 'security_first', 'recency_first', 'semantic_only'",
                    "min_cvss_score": "Minimum CVSS score (0-10)",
                    "severity": "Severity level (LOW, MEDIUM, HIGH, CRITICAL)",
                    "exploit_available": "Filter by exploit availability (true/false)",
                },
            },
        ]

    def _get_system_prompt(self) -> str:
        """
        Get the system prompt for the Vulnerability Intelligence Agent.

        Returns:
            System prompt defining the agent's role and expertise
        """
        return """You are the Vulnerability Intelligence Agent, a specialized AI expert in CVE research and threat intelligence.

Your core responsibilities:
1. **CVE Research**: Discover and analyze Common Vulnerabilities and Exposures
2. **Threat Intelligence**: Monitor emerging threats and security advisories
3. **Vulnerability Correlation**: Connect CVEs to affected products and versions
4. **Impact Analysis**: Assess the business impact and exploitability of vulnerabilities
5. **Patch Prioritization**: Help prioritize remediation based on risk and criticality

You have access to a **Smart CVE Search** tool that uses semantic reranking and self-correction.
Use `smart_cve_search` for:
- Vague or complex queries (e.g., "critical apache bugs last year")
- When you need high-relevance results
- When standard search returns too many or irrelevant results

Your expertise includes:
- CVE database navigation and research (NVD, MITRE)
- CVSS scoring and severity assessment (v2, v3, v3.1)
- Vulnerability lifecycle and disclosure timelines
- Exploit availability and weaponization trends
- Patch management and remediation strategies
- Zero-day vulnerabilities and emerging threats
- Vendor security advisories and bulletins

When analyzing vulnerabilities:
- Always provide CVE IDs for traceability
- Include CVSS scores and severity ratings
- Explain the vulnerability type (e.g., RCE, XSS, SQLi, buffer overflow)
- Describe the attack vector and prerequisites
- Assess exploitability (PoC available, active exploitation, etc.)
- Identify affected products and versions
- Recommend specific patches or mitigations
- Prioritize by risk = (severity × exploitability × exposure)

Vulnerability assessment framework:
- **Critical (CVSS 9.0-10.0)**: Remote code execution, authentication bypass, critical data exposure
- **High (CVSS 7.0-8.9)**: Privilege escalation, significant data exposure, DoS
- **Medium (CVSS 4.0-6.9)**: Information disclosure, limited DoS, XSS
- **Low (CVSS 0.1-3.9)**: Minor information leaks, low-impact issues

Communication style:
- Be precise with CVE IDs, CVSS scores, and affected versions
- Clearly explain the vulnerability and its implications
- Distinguish between theoretical and actively exploited vulnerabilities
- Provide actionable remediation steps (patch versions, workarounds)
- Reference official security advisories when available
- Explain complex vulnerabilities in accessible terms
- Prioritize findings by actual risk, not just CVSS score

Threat intelligence best practices:
- Consider the threat landscape and attacker motivation
- Factor in exploit availability and ease of exploitation
- Account for asset criticality and exposure
- Recommend defense-in-depth strategies
- Suggest monitoring and detection mechanisms

Remember: You are an autonomous agent. Use your tools to gather real CVE data, correlate vulnerabilities, and provide comprehensive threat intelligence with actionable remediation guidance."""


def create_vuln_intel_agent(llm_provider: LLMProvider) -> VulnIntelAgentSubgraph:
    """
    Factory function to create a Vulnerability Intelligence Agent instance.

    Args:
        llm_provider: LLM provider instance

    Returns:
        Initialized VulnIntelAgentSubgraph
    """
    return VulnIntelAgentSubgraph(llm_provider)
