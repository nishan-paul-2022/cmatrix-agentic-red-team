"""Tool registry and management functions with backward compatibility imports."""

import re

# Import tool functions from specialized modules
from network_tools import port_scan, vulnerability_assessment
from web_security import web_app_security_test, check_https_hsts
from authentication_security import (
    analyze_login_form,
    check_session_security,
    test_rate_limiting,
    check_password_policy
)

TOOLS = {
    "security_scan": {
        "description": "Perform a security scan on a target system or application",
        "parameters": ["target"],
        "function": lambda target: f"Security scan completed for {target}. Found 3 medium-risk vulnerabilities: outdated dependencies, missing CORS headers, weak password policy."
    },
    "check_system_status": {
        "description": "Check the status of a system service or application",
        "parameters": ["service_name"],
        "function": lambda service_name: f"Service '{service_name}' is running. CPU: 45%, Memory: 2.3GB, Uptime: 7 days."
    },
    "analyze_logs": {
        "description": "Analyze logs from a specified source for errors or anomalies",
        "parameters": ["log_source"],
        "function": lambda log_source: f"Analyzed logs from {log_source}. Found 12 errors in the last hour, mostly connection timeouts to external API."
    },
    "deploy_config": {
        "description": "Deploy a configuration to a specified environment",
        "parameters": ["environment", "config_name"],
        "function": lambda environment, config_name: f"Configuration '{config_name}' successfully deployed to {environment} environment. Rollback available if needed."
    },
    "port_scan": {
        "description": "Perform a port scan on a target IP or hostname to discover open ports and services",
        "parameters": ["target", "ports"],
        "function": lambda target, ports="1-1024": port_scan(target, ports)
    },
    "vulnerability_assessment": {
        "description": "Perform vulnerability assessment on a target system using nmap scripts",
        "parameters": ["target"],
        "function": vulnerability_assessment
    },
    "web_app_security_test": {
        "description": "Perform basic web application security testing including header checks and common vulnerabilities",
        "parameters": ["url"],
        "function": web_app_security_test
    },
    "check_https_hsts": {
        "description": "Check if HTTPS is enforced and HSTS (HTTP Strict Transport Security) is enabled",
        "parameters": ["url"],
        "function": check_https_hsts
    },
    "analyze_login_form": {
        "description": "Analyze login forms for security best practices including method, HTTPS usage, and CSRF protection",
        "parameters": ["url"],
        "function": analyze_login_form
    },
    "check_session_security": {
        "description": "Check session management security including cookie flags and session handling",
        "parameters": ["url"],
        "function": check_session_security
    },
    "test_rate_limiting": {
        "description": "Test for rate limiting on authentication endpoints to prevent brute force attacks",
        "parameters": ["url", "endpoint"],
        "function": lambda url, endpoint="/login": test_rate_limiting(url, endpoint)
    },
    "check_password_policy": {
        "description": "Check password policy requirements and security features",
        "parameters": ["url"],
        "function": check_password_policy
    }
}
