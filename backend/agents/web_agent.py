from langchain_core.tools import tool
from web_security import web_app_security_test, check_https_hsts

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

WEB_TOOLS = [scan_web_app, check_ssl_security]
