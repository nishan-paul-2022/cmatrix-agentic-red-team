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
    """Parse tool calls from LLM response."""
    # Import TOOLS from tools.py to avoid circular imports
    from tools import TOOLS

    tool_calls = []
    pattern = r'TOOL_CALL:\s*(\w+)\((.*?)\)'
    matches = re.findall(pattern, text, re.IGNORECASE)

    for tool_name, params_str in matches:
        if tool_name in TOOLS:
            # Parse parameters
            params = [p.strip().strip('"\'') for p in params_str.split(',') if p.strip()]
            tool_calls.append({"name": tool_name, "params": params})

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
