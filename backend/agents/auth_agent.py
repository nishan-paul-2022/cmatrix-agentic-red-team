from langchain_core.tools import tool
from authentication_security import (
    analyze_login_form,
    check_session_security,
    test_rate_limiting,
    check_password_policy
)

@tool
def analyze_auth_forms(url: str) -> str:
    """
    Analyze login and authentication forms for security issues.
    
    Args:
        url: The URL to analyze.
    """
    return analyze_login_form(url)

@tool
def check_sessions(url: str) -> str:
    """
    Check session management security (cookies, tokens).
    
    Args:
        url: The URL to check.
    """
    return check_session_security(url)

@tool
def test_auth_rate_limits(url: str, endpoint: str = "/login") -> str:
    """
    Test authentication endpoints for rate limiting.
    
    Args:
        url: The base URL.
        endpoint: The specific endpoint to test (default: "/login").
    """
    return test_rate_limiting(url, endpoint)

@tool
def audit_password_policy(url: str) -> str:
    """
    Audit the password policy and strength requirements.
    
    Args:
        url: The URL to check.
    """
    return check_password_policy(url)

AUTH_TOOLS = [analyze_auth_forms, check_sessions, test_auth_rate_limits, audit_password_policy]
