"""Vulnerability Intelligence Agent - CVE and threat intelligence integration."""
from langchain_core.tools import tool
import requests
from datetime import datetime, timedelta

@tool
def search_cve(keyword: str, limit: int = 5) -> str:
    """
    Search for CVE vulnerabilities by keyword.
    
    Args:
        keyword: Search keyword (e.g., "apache", "nginx", "openssl")
        limit: Maximum number of results to return
    """
    try:
        # Use NVD API (requires no authentication for basic queries)
        url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        params = {
            "keywordSearch": keyword,
            "resultsPerPage": min(limit, 10)
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            vulnerabilities = data.get("vulnerabilities", [])
            
            if not vulnerabilities:
                return f"No CVEs found for keyword: {keyword}"
            
            results = [f"CVE Search Results for '{keyword}' (Top {len(vulnerabilities)} results):"]
            results.append("")
            
            for vuln in vulnerabilities:
                cve = vuln.get("cve", {})
                cve_id = cve.get("id", "Unknown")
                descriptions = cve.get("descriptions", [])
                description = descriptions[0].get("value", "No description") if descriptions else "No description"
                
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
            
            results.append(f"Source: NVD (National Vulnerability Database)")
            return "\n".join(results)
        else:
            return f"CVE search failed: HTTP {response.status_code}"
            
    except requests.Timeout:
        return "CVE search timed out. The NVD API may be slow."
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
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        params = {
            "pubStartDate": start_date.strftime("%Y-%m-%dT00:00:00.000"),
            "pubEndDate": end_date.strftime("%Y-%m-%dT23:59:59.999"),
            "resultsPerPage": 10
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
                        description = descriptions[0].get("value", "No description") if descriptions else "No description"
                        
                        results.append(f"🔴 {cve_id} - {vuln_severity} ({score})")
                        results.append(f"   {description[:150]}...")
                        results.append("")
                        filtered_count += 1
            
            if filtered_count == 0:
                results.append(f"No {severity}+ severity CVEs found in the last {days} days")
            
            results.append(f"Source: NVD (National Vulnerability Database)")
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
        search_term = f"{product} {version}".strip()
        
        url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        params = {
            "keywordSearch": search_term,
            "resultsPerPage": 10
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            vulnerabilities = data.get("vulnerabilities", [])
            
            results = [f"Vulnerability Check: {product}" + (f" v{version}" if version else "")]
            results.append("")
            
            if not vulnerabilities:
                results.append(f"✅ No known vulnerabilities found for {search_term}")
                results.append("Note: This doesn't guarantee the software is secure. Always keep software updated.")
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

VULN_INTEL_TOOLS = [search_cve, get_recent_cves, check_vulnerability_by_product]
