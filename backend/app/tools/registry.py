"""Tool registry for managing all available tools."""

from typing import Dict, Any, Callable


class ToolRegistry:
    """Central registry for all available tools."""
    
    def __init__(self):
        """Initialize the tool registry."""
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._register_all_tools()
    
    def _register_all_tools(self):
        """Register all tools from specialized agents."""
        # Lazy import to avoid circular dependencies
        from app.agents import (
            NETWORK_TOOLS,
            WEB_TOOLS,
            AUTH_TOOLS,
            CONFIG_TOOLS,
            VULN_INTEL_TOOLS,
            API_SECURITY_TOOLS,
            COMMAND_TOOLS,
        )
        from app.tools.memory import search_knowledge_base, save_to_knowledge_base
        
        all_tool_lists = [
            NETWORK_TOOLS,
            WEB_TOOLS,
            AUTH_TOOLS,
            CONFIG_TOOLS,
            VULN_INTEL_TOOLS,
            API_SECURITY_TOOLS,
            COMMAND_TOOLS,
            [search_knowledge_base, save_to_knowledge_base],  # Add memory tools
        ]
        
        for tool_list in all_tool_lists:
            for tool in tool_list:
                self._tools[tool.name] = {
                    "description": tool.description,
                    "parameters": list(tool.args.keys()),
                    "function": tool.func if hasattr(tool, "func") else tool
                }
    
    def get_tool(self, name: str) -> Dict[str, Any]:
        """
        Get a tool by name.
        
        Args:
            name: Tool name
            
        Returns:
            Tool information dictionary
            
        Raises:
            KeyError: If tool not found
        """
        return self._tools[name]
    
    def get_all_tools(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all registered tools.
        
        Returns:
            Dictionary of all tools
        """
        return self._tools.copy()
    
    def tool_exists(self, name: str) -> bool:
        """
        Check if a tool exists.
        
        Args:
            name: Tool name
            
        Returns:
            True if tool exists
        """
        return name in self._tools
    
    def get_tool_definitions(self) -> str:
        """
        Get formatted tool definitions for LLM prompt.
        
        Returns:
            Formatted string of tool definitions
        """
        definitions = []
        for name, tool_info in self._tools.items():
            params = ", ".join(tool_info["parameters"])
            definitions.append(f"- {name}({params}): {tool_info['description']}")
        return "\n".join(definitions)


# Global tool registry instance
_tool_registry: ToolRegistry = None


def get_tool_registry() -> ToolRegistry:
    """
    Get or create global tool registry instance.
    
    Returns:
        ToolRegistry instance
    """
    global _tool_registry
    if _tool_registry is None:
        _tool_registry = ToolRegistry()
    return _tool_registry
