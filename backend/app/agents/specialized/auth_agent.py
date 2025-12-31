"""Authentication Security Agent Subgraph."""

from typing import Any

from langchain_core.tools import tool
from loguru import logger

from app.agents.base.agent import BaseAgentSubgraph
from app.services.llm.providers.base import LLMProvider
from app.tools.authentication_security import (
    analyze_login_form,
    check_password_policy,
    check_session_security,
    test_rate_limiting,
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


# Legacy tool list for backward compatibility
AUTH_TOOLS = [analyze_auth_forms, check_sessions, test_auth_rate_limits, audit_password_policy]


class AuthAgentSubgraph(BaseAgentSubgraph):
    """
    Authentication Security Agent Subgraph.

    This agent is responsible for:
    - Analyzing login forms and authentication mechanisms
    - Testing session management security
    - Verifying rate limiting and brute force protection
    - Auditing password policies
    """

    def __init__(self, llm_provider: LLMProvider):
        """Initialize the Authentication Security Agent."""
        super().__init__(llm_provider, agent_name="AuthSecurityAgent")
        logger.info("Auth Security Agent initialized with autonomous reasoning")

    def _register_tools(self) -> list[dict[str, Any]]:
        """Register authentication security tools."""
        return [
            {
                "name": "analyze_auth_forms",
                "function": analyze_auth_forms,
                "description": "Analyze login and authentication forms for security issues like weak encryption, missing CSRF tokens, etc.",
                "parameters": {"url": "The URL to analyze"},
            },
            {
                "name": "check_sessions",
                "function": check_sessions,
                "description": "Check session management security, including cookie attributes (Secure, HttpOnly) and token handling.",
                "parameters": {"url": "The URL to check"},
            },
            {
                "name": "test_auth_rate_limits",
                "function": test_auth_rate_limits,
                "description": "Test authentication endpoints for rate limiting vulnerabilities to prevent brute force attacks.",
                "parameters": {
                    "url": "The base URL",
                    "endpoint": "The specific endpoint to test (default: '/login')",
                },
            },
            {
                "name": "audit_password_policy",
                "function": audit_password_policy,
                "description": "Audit the password policy and strength requirements of the application.",
                "parameters": {"url": "The URL to check"},
            },
        ]

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Auth Security Agent."""
        return """You are the Authentication Security Agent, a specialized AI expert in securing authentication mechanisms.

Your core responsibilities:
1. **Form Analysis**: Identify weaknesses in login forms (HTTP, missing CSRF, weak encryption).
2. **Session Security**: Validate cookie attributes (Secure, HttpOnly, SameSite) and token storage.
3. **Rate Limiting**: Verify protections against brute-force and credential stuffing attacks.
4. **Password Policy**: Ensure strong password requirements are enforced.

When analyzing authentication:
- Always check if login forms are served over HTTPS.
- Look for anti-automation mechanisms (CAPTCHA, rate limiting).
- Verify that session cookies are secure and not accessible via JavaScript.
- Assess the strength of password policies (length, complexity).
- Provide specific, actionable remediation steps for any findings.

Communication style:
- Be precise and technical.
- Clearly distinguish between critical, high, medium, and low severity issues.
- Prioritize findings by risk.
"""


def create_auth_agent(llm_provider: LLMProvider) -> AuthAgentSubgraph:
    """Factory function to create an Auth Security Agent instance."""
    return AuthAgentSubgraph(llm_provider)
