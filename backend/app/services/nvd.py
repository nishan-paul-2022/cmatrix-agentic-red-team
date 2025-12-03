from typing import Any

import requests
from loguru import logger


def fetch_cves_from_nvd(keyword: str, limit: int = 10) -> list[dict[str, Any]]:
    """Helper to fetch CVEs from NVD API."""
    try:
        url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        params = {"keywordSearch": keyword, "resultsPerPage": limit}

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return data.get("vulnerabilities", [])
        return []
    except Exception as e:
        logger.error(f"NVD API error: {e}")
        return []
