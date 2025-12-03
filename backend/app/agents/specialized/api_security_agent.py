"""API Security Agent - REST and GraphQL API security testing."""

import requests
from langchain_core.tools import tool


@tool
def test_api_endpoints(base_url: str, endpoints: str = "/api,/v1,/graphql") -> str:
    """
    Test common API endpoints for security issues.

    Args:
        base_url: Base URL of the API
        endpoints: Comma-separated list of endpoints to test
    """
    results = []
    results.append(f"API Security Test for {base_url}")
    results.append("")

    endpoint_list = [e.strip() for e in endpoints.split(",")]

    for endpoint in endpoint_list:
        full_url = base_url.rstrip("/") + "/" + endpoint.lstrip("/")
        results.append(f"Testing: {full_url}")

        try:
            # Test GET request
            response = requests.get(full_url, timeout=5, verify=False)
            results.append(f"  Status: {response.status_code}")

            # Check for common security headers
            headers_to_check = {
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "DENY or SAMEORIGIN",
                "Content-Security-Policy": "CSP policy",
                "Strict-Transport-Security": "HSTS",
                "X-API-Key": "Should not be exposed",
            }

            for header, _expected in headers_to_check.items():
                if header in response.headers:
                    if header == "X-API-Key":
                        results.append(f"  ⚠️  {header} header exposed!")
                    else:
                        results.append(f"  ✅ {header}: present")
                else:
                    if header != "X-API-Key":
                        results.append(f"  ❌ {header}: missing")

            # Check for error disclosure
            if response.status_code >= 400:
                if "stack" in response.text.lower() or "trace" in response.text.lower():
                    results.append("  ⚠️  Potential stack trace disclosure")

        except requests.Timeout:
            results.append("  ⚠️  Request timed out")
        except Exception as e:
            results.append(f"  ❌ Error: {str(e)}")

        results.append("")

    return "\n".join(results)


@tool
def check_api_authentication(api_url: str) -> str:
    """
    Check API authentication mechanisms.

    Args:
        api_url: API endpoint URL
    """
    results = []
    results.append(f"API Authentication Check: {api_url}")
    results.append("")

    try:
        # Test without authentication
        response_no_auth = requests.get(api_url, timeout=5, verify=False)
        results.append("Request without authentication:")
        results.append(f"  Status: {response_no_auth.status_code}")

        if response_no_auth.status_code == 200:
            results.append("  ⚠️  API accessible without authentication!")
        elif response_no_auth.status_code == 401:
            results.append("  ✅ Authentication required (401)")
        elif response_no_auth.status_code == 403:
            results.append("  ✅ Access forbidden (403)")

        # Check WWW-Authenticate header
        if "WWW-Authenticate" in response_no_auth.headers:
            auth_method = response_no_auth.headers["WWW-Authenticate"]
            results.append(f"  Authentication method: {auth_method}")

            if "Basic" in auth_method:
                results.append("  ⚠️  Basic authentication detected - ensure HTTPS is used")
            elif "Bearer" in auth_method:
                results.append("  ✅ Bearer token authentication")

        results.append("")
        results.append("Recommendations:")
        results.append("• Require authentication for all sensitive endpoints")
        results.append("• Use OAuth 2.0 or JWT for token-based authentication")
        results.append("• Implement rate limiting")
        results.append("• Use HTTPS for all API communications")
        results.append("• Implement proper CORS policies")

    except Exception as e:
        results.append(f"Authentication check failed: {str(e)}")

    return "\n".join(results)


@tool
def test_graphql_introspection(graphql_url: str) -> str:
    """
    Test GraphQL introspection and common security issues.

    Args:
        graphql_url: GraphQL endpoint URL
    """
    results = []
    results.append(f"GraphQL Security Test: {graphql_url}")
    results.append("")

    # Introspection query
    introspection_query = {
        "query": """
        {
            __schema {
                types {
                    name
                }
            }
        }
        """
    }

    try:
        response = requests.post(
            graphql_url,
            json=introspection_query,
            headers={"Content-Type": "application/json"},
            timeout=5,
            verify=False,
        )

        results.append("Introspection Query Test:")
        results.append(f"  Status: {response.status_code}")

        if response.status_code == 200:
            try:
                data = response.json()
                if "data" in data and "__schema" in data["data"]:
                    types = data["data"]["__schema"]["types"]
                    results.append("  ⚠️  Introspection is ENABLED")
                    results.append(f"  Found {len(types)} schema types")
                    results.append("  ⚠️  This exposes your entire API schema")
                else:
                    results.append("  ✅ Introspection appears to be disabled")
            except:
                results.append("  ℹ️  Could not parse response")
        else:
            results.append("  ✅ Introspection query rejected")

        results.append("")
        results.append("GraphQL Security Recommendations:")
        results.append("• Disable introspection in production")
        results.append("• Implement query depth limiting")
        results.append("• Implement query complexity analysis")
        results.append("• Use persisted queries")
        results.append("• Implement proper authentication and authorization")
        results.append("• Rate limit GraphQL endpoints")

    except Exception as e:
        results.append(f"GraphQL test failed: {str(e)}")

    return "\n".join(results)


@tool
def check_api_rate_limiting(api_url: str, requests_count: int = 10) -> str:
    """
    Test API rate limiting.

    Args:
        api_url: API endpoint URL
        requests_count: Number of rapid requests to send
    """
    results = []
    results.append(f"API Rate Limiting Test: {api_url}")
    results.append(f"Sending {requests_count} rapid requests...")
    results.append("")

    status_codes = []

    try:
        for i in range(requests_count):
            response = requests.get(api_url, timeout=2, verify=False)
            status_codes.append(response.status_code)

            if response.status_code == 429:
                results.append(f"✅ Rate limiting detected at request #{i+1}")
                break

        if 429 not in status_codes:
            results.append(f"⚠️  No rate limiting detected after {requests_count} requests")
            results.append(f"Status codes: {status_codes}")

        results.append("")
        results.append("Recommendations:")
        results.append("• Implement rate limiting (e.g., 100 requests per minute)")
        results.append("• Return 429 status code when limit exceeded")
        results.append("• Include Retry-After header")
        results.append("• Consider using API keys for tracking")

    except Exception as e:
        results.append(f"Rate limiting test failed: {str(e)}")

    return "\n".join(results)


API_SECURITY_TOOLS = [
    test_api_endpoints,
    check_api_authentication,
    test_graphql_introspection,
    check_api_rate_limiting,
]
