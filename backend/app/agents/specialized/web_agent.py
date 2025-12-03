"""
Web Security Agent Subgraph.

This agent specializes in web application security testing, SSL/TLS analysis,
and HTTP security header validation. It operates as an autonomous LangGraph
subgraph with its own reasoning loop and LLM instance.
"""

from typing import Any

from langchain_core.tools import tool
from loguru import logger

from app.agents.base.agent import BaseAgentSubgraph
from app.services.llm.providers.base import LLMProvider
from app.tools.web_security import check_https_hsts, web_app_security_test


# Tool wrappers for backward compatibility
@tool
def scan_web_app(url: str) -> str:
    """
    Perform a comprehensive web application security scan.

    Args:
        url: The URL of the web application to scan.
    """
    return web_app_security_test(url)


@tool
def check_ssl_security(url: str) -> str:
    """
    Check SSL/TLS security configuration including HSTS.

    Args:
        url: The URL to check.
    """
    return check_https_hsts(url)


# Legacy tool list for backward compatibility
WEB_TOOLS = [scan_web_app, check_ssl_security]


class WebAgentSubgraph(BaseAgentSubgraph):
    """
    Web Security Agent Subgraph.

    This agent is responsible for:
    - Web application security scanning
    - SSL/TLS configuration analysis
    - HTTP security header validation
    - OWASP Top 10 vulnerability detection
    - Web security best practices assessment

    The agent uses various web security tools to perform comprehensive
    web application security assessments.
    """

    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize the Web Security Agent.

        Args:
            llm_provider: LLM provider instance for this agent
        """
        super().__init__(llm_provider, agent_name="WebSecurityAgent")
        logger.info("Web Security Agent initialized with autonomous reasoning")

    def _register_tools(self) -> list[dict[str, Any]]:
        """
        Register web security tools.

        Returns:
            List of tool definitions
        """
        return [
            {
                "name": "scan_web_app",
                "function": scan_web_app,
                "description": (
                    "Perform a comprehensive web application security scan. "
                    "Checks for common vulnerabilities including XSS, SQL injection, "
                    "CSRF, security misconfigurations, and OWASP Top 10 issues. "
                    "Use this to assess the overall security posture of a web application."
                ),
                "parameters": {
                    "url": "Full URL of the web application to scan (e.g., 'https://example.com')"
                },
            },
            {
                "name": "check_ssl_security",
                "function": check_ssl_security,
                "description": (
                    "Check SSL/TLS security configuration and HTTP security headers. "
                    "Validates certificate, protocol versions, cipher suites, HSTS, "
                    "and other security headers. Use this to assess transport security."
                ),
                "parameters": {"url": "URL to check (e.g., 'https://example.com')"},
            },
        ]

    def _get_system_prompt(self) -> str:
        """
        Get the system prompt for the Web Security Agent.

        Returns:
            System prompt defining the agent's role and expertise
        """
        return """You are the Web Security Agent, a specialized AI expert in web application security.

Your core responsibilities:
1. **Web Application Scanning**: Identify vulnerabilities in web applications
2. **SSL/TLS Analysis**: Assess transport layer security configurations
3. **Security Header Validation**: Check for proper HTTP security headers
4. **OWASP Top 10 Detection**: Identify common web vulnerabilities
5. **Remediation Guidance**: Provide actionable security recommendations

Your expertise includes:
- OWASP Top 10 vulnerabilities (XSS, SQL Injection, CSRF, etc.)
- HTTP security headers (CSP, HSTS, X-Frame-Options, etc.)
- SSL/TLS best practices and certificate validation
- Authentication and session management security
- Input validation and output encoding
- Security misconfigurations
- Modern web security standards (SameSite cookies, Subresource Integrity, etc.)

When analyzing web application security:
- Start with SSL/TLS configuration to ensure secure transport
- Check for critical security headers (HSTS, CSP, X-Frame-Options)
- Scan for common vulnerabilities (XSS, SQLi, CSRF)
- Assess authentication and session management
- Evaluate input validation and sanitization
- Check for security misconfigurations
- Review cookie security (HttpOnly, Secure, SameSite)
- Provide specific remediation steps with code examples when possible

Communication style:
- Be precise about vulnerability types and their CVSS scores
- Clearly explain the attack vector and potential impact
- Distinguish between critical, high, medium, and low severity issues
- Provide specific remediation steps (e.g., exact headers to add)
- Reference OWASP guidelines and industry standards
- Include code examples for fixes when applicable

Security assessment framework:
- **Critical**: Remote code execution, SQL injection, authentication bypass
- **High**: XSS, CSRF, sensitive data exposure, broken access control
- **Medium**: Security misconfigurations, missing security headers
- **Low**: Information disclosure, best practice violations

Remember: You are an autonomous agent. Use your tools to gather real data, analyze the findings, and provide comprehensive security assessments with actionable remediation steps."""


def create_web_agent(llm_provider: LLMProvider) -> WebAgentSubgraph:
    """
    Factory function to create a Web Security Agent instance.

    Args:
        llm_provider: LLM provider instance

    Returns:
        Initialized WebAgentSubgraph
    """
    return WebAgentSubgraph(llm_provider)
