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


def _parse_params_string(params_str: str) -> dict:
    """Parse parameters string into dictionary, handling quotes and commas correctly."""
    params_dict = {}
    if not params_str.strip():
        return params_dict

    # Regex for keyword arguments: key="value" or key='value' or key=value
    # Handles commas inside quotes and escaped quotes
    # The pattern (?:[^"\\]|\\.)* matches any character that is not a quote or backslash, OR an escaped character
    kw_pattern = r"(\w+)\s*=\s*(?:\"((?:[^\"\\]|\\.)*)\"|'((?:[^'\\]|\\.)*)'|([^,]+))"

    if "=" in params_str:
        matches = re.finditer(kw_pattern, params_str, re.DOTALL)
        for match in matches:
            key = match.group(1)
            # Value is in group 2 (double quoted), 3 (single quoted), or 4 (unquoted)
            val = (
                match.group(2)
                if match.group(2) is not None
                else match.group(3)
                if match.group(3) is not None
                else match.group(4)
            )

            if val is not None:
                params_dict[key] = val.strip()
    else:
        # Positional arguments - try to handle quoted strings with commas
        # Pattern: "([^"]*)"|'([^']*)'|([^,]+)
        val_pattern = r"(?:\"((?:[^\"\\]|\\.)*)\"|'((?:[^'\\]|\\.)*)'|([^,]+))"
        matches = re.finditer(val_pattern, params_str, re.DOTALL)
        params = []
        for match in matches:
            val = (
                match.group(1)
                if match.group(1) is not None
                else match.group(2)
                if match.group(2) is not None
                else match.group(3)
            )

            # Filter out commas and empty strings that might be matched by the unquoted group
            if val and val.strip() and val.strip() != ",":
                params.append(val.strip())

        # Map positional args to known keys (legacy support)
        if len(params) > 0:
            params_dict["target"] = params[0]
        if len(params) > 1:
            params_dict["ports"] = params[1]

    return params_dict


def _find_balanced_parentheses(text: str, start_index: int) -> int:
    """
    Find the index of the closing parenthesis that balances the one at start_index.
    Handles nested parentheses and quotes.
    Returns -1 if not found.
    """
    count = 1
    in_quote = False
    quote_char = None
    i = start_index + 1

    while i < len(text):
        char = text[i]

        if in_quote:
            if char == quote_char:
                # Check for escaped quote
                bs_count = 0
                k = i - 1
                while k >= 0 and text[k] == "\\":
                    bs_count += 1
                    k -= 1

                if bs_count % 2 == 1:
                    pass  # Escaped
                else:
                    in_quote = False
                    quote_char = None
        else:
            if char == '"' or char == "'":
                in_quote = True
                quote_char = char
            elif char == "(":
                count += 1
            elif char == ")":
                count -= 1
                if count == 0:
                    return i
        i += 1

    return -1


def parse_tool_calls(text: str) -> list:
    """Parse tool calls from LLM response - handles multiple formats and nested parentheses."""
    tool_calls = []

    # Common tools list
    common_tools = [
        "scan_network",
        "assess_vulnerabilities",
        "scan_web_app",
        "check_ssl_security",
        "analyze_auth_forms",
        "check_sessions",
        "test_auth_rate_limits",
        "audit_password_policy",
        "check_cloud_config",
        "check_system_hardening",
        "check_compliance",
        "search_cve",
        "get_recent_cves",
        "check_vulnerability_by_product",
        "test_api_endpoints",
        "check_api_authentication",
        "test_graphql_introspection",
        "check_api_rate_limiting",
        "execute_terminal_command",
        "run_nmap_scan",
        "check_service_status",
        "run_curl_request",
        "search_knowledge_base",
        "save_to_knowledge_base",
    ]

    # Regex to find potential starts: matches "TOOL: name(" or "name("
    # Group 1: tool name
    start_pattern = re.compile(r"(?:TOOL(?:_CALL)?:\s*)?(\w+)\(", re.IGNORECASE)

    pos = 0
    while pos < len(text):
        match = start_pattern.search(text, pos)
        if not match:
            break

        tool_name = match.group(1)
        start_paren = match.end() - 1

        # Check validity
        is_explicit_tool = match.group(0).upper().lstrip().startswith("TOOL")
        is_common_tool = tool_name in common_tools

        if not (is_explicit_tool or is_common_tool):
            pos = match.end()
            continue

        end_paren = _find_balanced_parentheses(text, start_paren)

        if end_paren != -1:
            params_str = text[start_paren + 1 : end_paren]
            params_dict = _parse_params_string(params_str)
            tool_calls.append((tool_name, params_dict))
            pos = end_paren + 1
        else:
            # Malformed or incomplete, skip this match
            pos = match.end()

    return tool_calls


def execute_tools(tool_calls: list) -> str:
    """Execute tool calls and return results."""
    # Import TOOLS from tools.py to avoid circular imports
    from tools import TOOLS

    results = []
    for call in tool_calls:
        tool_name = call[0]  # Tuple is (name, params)
        params = call[1]

        if tool_name in TOOLS:
            try:
                # Check if tool expects specific arguments or **kwargs
                # For simplicity in this dynamic setup, we try to pass as kwargs
                # But some tools might be defined differently.
                # The registry.py approach uses .invoke(args) for LangChain tools
                # Here we are using direct function calls from TOOLS dict

                # Note: The original code used TOOLS[tool_name]["function"](*params)
                # But params is now a dict. We should use **params.

                func = TOOLS[tool_name]["function"]

                # Handle LangChain StructuredTool vs simple function
                if hasattr(func, "invoke"):
                    # For LangChain tools, invoke expects a dict
                    result = func.invoke(params)
                else:
                    # For regular functions, pass kwargs
                    result = func(**params)

                results.append(f"[{tool_name}] {result}")
            except Exception as e:
                results.append(f"[{tool_name}] Error: {str(e)}")
        else:
            results.append(f"[{tool_name}] Error: Tool not found")

    return "\n".join(results) if results else "No tools executed."
