"""Tool execution and parsing functions."""

import re

def create_tool_prompt():
    """Create a prompt describing available tools."""
    # Import TOOLS from tools.py to avoid circular imports
    from tools import TOOLS

    tool_descriptions = []
    for name, info in TOOLS.items():
        params = ", ".join(info["parameters"])
        tool_descriptions.append(f"- {name}({params}): {info['description']}")

    return f"""You have access to the following tools:

{chr(10).join(tool_descriptions)}

To use a tool, respond with: TOOL_CALL: tool_name(param1, param2, ...)
You can call multiple tools by using multiple TOOL_CALL lines.
After tool results, provide your final answer to the user."""

def parse_tool_calls(text: str) -> list:
    """Parse tool calls from LLM response - handles multiple formats."""
    # Import ALL_TOOLS from orchestrator to get all available tools
    # We'll check against common tool names
    tool_calls = []
    
    # Pattern 1: TOOL_CALL: tool_name(params)
    pattern1 = r'TOOL_CALL:\s*(\w+)\((.*?)\)'
    matches1 = re.findall(pattern1, text, re.IGNORECASE)
    
    for tool_name, params_str in matches1:
        # Parse parameters - handle both positional and keyword args
        params_dict = {}
        if params_str.strip():
            # Try to parse keyword arguments like "target=localhost, ports=1-1024"
            if '=' in params_str:
                for param in params_str.split(','):
                    if '=' in param:
                        key, value = param.split('=', 1)
                        params_dict[key.strip()] = value.strip().strip('"\'')
            else:
                # Positional arguments
                params = [p.strip().strip('"\'') for p in params_str.split(',') if p.strip()]
                # For now, assume first param is 'target' and second is 'ports' for network tools
                if len(params) > 0:
                    params_dict['target'] = params[0]
                if len(params) > 1:
                    params_dict['ports'] = params[1]
        
        tool_calls.append((tool_name, params_dict))
    
    # Pattern 2: Direct function call like "scan_network(target=localhost, ports=1-1024)"
    # Look for common tool names
    common_tools = [
        'scan_network', 'assess_vulnerabilities', 'scan_web_app', 'check_ssl_security',
        'analyze_auth_forms', 'check_sessions', 'test_auth_rate_limits', 'audit_password_policy',
        'check_cloud_config', 'check_system_hardening', 'check_compliance',
        'search_cve', 'get_recent_cves', 'check_vulnerability_by_product',
        'test_api_endpoints', 'check_api_authentication', 'test_graphql_introspection', 'check_api_rate_limiting',
        'execute_terminal_command', 'run_nmap_scan', 'check_service_status', 'run_curl_request'
    ]
    
    for tool_name in common_tools:
        pattern2 = rf'{tool_name}\((.*?)\)'
        matches2 = re.findall(pattern2, text, re.IGNORECASE)
        
        for params_str in matches2:
            params_dict = {}
            if params_str.strip():
                # Parse keyword arguments
                if '=' in params_str:
                    for param in params_str.split(','):
                        if '=' in param:
                            key, value = param.split('=', 1)
                            params_dict[key.strip()] = value.strip().strip('"\'')
                else:
                    # Positional arguments
                    params = [p.strip().strip('"\'') for p in params_str.split(',') if p.strip()]
                    if len(params) > 0:
                        params_dict['target'] = params[0]
                    if len(params) > 1:
                        params_dict['ports'] = params[1]
            
            tool_calls.append((tool_name, params_dict))
    
    return tool_calls

def execute_tools(tool_calls: list) -> str:
    """Execute tool calls and return results."""
    # Import TOOLS from tools.py to avoid circular imports
    from tools import TOOLS

    results = []
    for call in tool_calls:
        tool_name = call["name"]
        params = call["params"]

        if tool_name in TOOLS:
            try:
                result = TOOLS[tool_name]["function"](*params)
                results.append(f"[{tool_name}] {result}")
            except Exception as e:
                results.append(f"[{tool_name}] Error: {str(e)}")

    return "\n".join(results) if results else "No tools executed."
