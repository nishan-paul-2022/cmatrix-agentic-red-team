"""
Approval configuration for dangerous tools.

This module defines which tools require human approval before execution,
categorized by risk level.
"""

import re
from enum import Enum
from typing import Any, Optional


class RiskLevel(str, Enum):
    """Risk levels for tool execution."""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ToolRiskInfo:
    """Information about a tool's risk level and approval requirements."""

    def __init__(
        self,
        risk_level: RiskLevel,
        reason: str,
        requires_approval: bool,
        warning: Optional[str] = None,
        auto_reject_patterns: Optional[list[str]] = None,
        estimated_duration: str = "< 1 minute",
        reversible: bool = True,
    ):
        self.risk_level = risk_level
        self.reason = reason
        self.requires_approval = requires_approval
        self.warning = warning
        self.auto_reject_patterns = auto_reject_patterns or []
        self.estimated_duration = estimated_duration
        self.reversible = reversible

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            "risk_level": self.risk_level.value,
            "reason": self.reason,
            "requires_approval": self.requires_approval,
            "warning": self.warning,
            "auto_reject_patterns": self.auto_reject_patterns,
            "estimated_duration": self.estimated_duration,
            "reversible": self.reversible,
        }


# Dangerous tools registry with risk classification
DANGEROUS_TOOLS: dict[str, ToolRiskInfo] = {
    # CRITICAL RISK - Can cause system damage, data loss, or security breaches
    "execute_terminal_command": ToolRiskInfo(
        risk_level=RiskLevel.CRITICAL,
        reason="Can execute arbitrary system commands with potential for system damage",
        requires_approval=True,
        warning="⚠️ This command can permanently damage your system or expose sensitive data!",
        auto_reject_patterns=[
            r"rm\s+-rf\s+/",  # Delete root filesystem
            r"dd\s+if=.*\s+of=/dev/",  # Disk wipe
            r"mkfs\.",  # Format filesystem
            r":\(\)\{.*\}",  # Fork bomb
            r"chmod\s+-R\s+777\s+/",  # Dangerous permissions on root
            r">\s*/dev/sd[a-z]",  # Direct write to disk
            r"curl.*\|\s*bash",  # Pipe to bash (common malware vector)
            r"wget.*\|\s*sh",  # Pipe to shell
        ],
        estimated_duration="Varies",
        reversible=False,
    ),
    # HIGH RISK - Can modify system state or expose sensitive data
    "run_nmap_scan": ToolRiskInfo(
        risk_level=RiskLevel.HIGH,
        reason="Network scanning may trigger IDS/IPS alerts and requires authorization",
        requires_approval=True,
        warning="⚠️ Ensure you have explicit authorization to scan this target!",
        estimated_duration="2-10 minutes (depending on port range)",
        reversible=True,
    ),
    "run_exploit": ToolRiskInfo(
        risk_level=RiskLevel.CRITICAL,
        reason="Exploit execution can compromise target systems",
        requires_approval=True,
        warning="⚠️ CRITICAL: Only run exploits on authorized test systems!",
        estimated_duration="Varies",
        reversible=False,
    ),
    "modify_config": ToolRiskInfo(
        risk_level=RiskLevel.HIGH,
        reason="Configuration changes can affect system behavior",
        requires_approval=True,
        warning="⚠️ Configuration changes may require system restart",
        estimated_duration="< 1 minute",
        reversible=True,
    ),
    "deploy_config": ToolRiskInfo(
        risk_level=RiskLevel.HIGH,
        reason="Deploying configuration can affect running services",
        requires_approval=True,
        warning="⚠️ Deployment may cause service interruption",
        estimated_duration="1-5 minutes",
        reversible=True,
    ),
    # MEDIUM RISK - Read-only operations on sensitive resources
    "check_service_status": ToolRiskInfo(
        risk_level=RiskLevel.MEDIUM,
        reason="Accesses system service information",
        requires_approval=False,  # Can be configured to require approval
        estimated_duration="< 10 seconds",
        reversible=True,
    ),
    "analyze_logs": ToolRiskInfo(
        risk_level=RiskLevel.MEDIUM,
        reason="May expose sensitive information in logs",
        requires_approval=False,
        estimated_duration="< 30 seconds",
        reversible=True,
    ),
    "run_curl_request": ToolRiskInfo(
        risk_level=RiskLevel.MEDIUM,
        reason="Makes external HTTP requests",
        requires_approval=False,
        warning="Ensure the target URL is trusted",
        estimated_duration="< 30 seconds",
        reversible=True,
    ),
}


# Auto-reject patterns that apply globally
GLOBAL_AUTO_REJECT_PATTERNS = [
    r"rm\s+-rf\s+/",  # Delete root filesystem
    r"dd\s+if=.*\s+of=/dev/",  # Disk wipe
    r"mkfs\.",  # Format filesystem
    r":\(\)\{.*\}",  # Fork bomb
    r"chmod\s+-R\s+777\s+/",  # Dangerous permissions on root
]


def get_tool_risk_info(tool_name: str) -> ToolRiskInfo:
    """
    Get risk information for a tool.

    Args:
        tool_name: Name of the tool

    Returns:
        ToolRiskInfo object (defaults to LOW risk if not found)
    """
    return DANGEROUS_TOOLS.get(
        tool_name,
        ToolRiskInfo(
            risk_level=RiskLevel.LOW,
            reason="Standard tool operation",
            requires_approval=False,
            estimated_duration="< 1 minute",
            reversible=True,
        ),
    )


def check_auto_reject(tool_name: str, tool_args: dict[str, Any]) -> Optional[str]:
    """
    Check if tool execution should be automatically rejected.

    Args:
        tool_name: Name of the tool
        tool_args: Tool arguments

    Returns:
        Rejection reason if should be rejected, None otherwise
    """
    risk_info = get_tool_risk_info(tool_name)

    # Check tool-specific patterns
    for pattern in risk_info.auto_reject_patterns:
        # Check all string arguments
        for arg_value in tool_args.values():
            if isinstance(arg_value, str):
                if re.search(pattern, arg_value, re.IGNORECASE):
                    return (
                        f"⛔ Operation automatically rejected: "
                        f"Command matches dangerous pattern '{pattern}'. "
                        f"This operation is not allowed for safety reasons."
                    )

    # Check global patterns
    for pattern in GLOBAL_AUTO_REJECT_PATTERNS:
        for arg_value in tool_args.values():
            if isinstance(arg_value, str):
                if re.search(pattern, arg_value, re.IGNORECASE):
                    return (
                        "⛔ Operation automatically rejected: "
                        "Command matches globally banned pattern. "
                        "This operation is not allowed for safety reasons."
                    )

    return None


def requires_approval(tool_name: str, tool_args: dict[str, Any]) -> bool:
    """
    Check if a tool requires approval before execution.

    Args:
        tool_name: Name of the tool
        tool_args: Tool arguments

    Returns:
        True if approval is required, False otherwise
    """
    # First check if it should be auto-rejected
    if check_auto_reject(tool_name, tool_args):
        return True  # Requires approval (which will be auto-rejected)

    # Check tool's approval requirement
    risk_info = get_tool_risk_info(tool_name)
    return risk_info.requires_approval


def get_all_dangerous_tools() -> list[str]:
    """
    Get list of all tools that require approval.

    Returns:
        List of tool names
    """
    return [
        tool_name for tool_name, risk_info in DANGEROUS_TOOLS.items() if risk_info.requires_approval
    ]
