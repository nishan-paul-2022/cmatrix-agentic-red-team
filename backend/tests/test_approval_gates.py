"""
Tests for HITL approval gates functionality.
"""

import pytest

from app.core.approval_config import (
    RiskLevel,
    check_auto_reject,
    get_tool_risk_info,
    requires_approval,
)


class TestApprovalConfig:
    """Test approval configuration and risk assessment."""

    def test_dangerous_tool_requires_approval(self):
        """Test that dangerous tools require approval."""
        assert requires_approval("execute_terminal_command", {"command": "ls"}) is True
        assert requires_approval("run_nmap_scan", {"target": "localhost"}) is True

    def test_safe_tool_no_approval(self):
        """Test that safe tools don't require approval."""
        assert requires_approval("search_cve", {"keyword": "apache"}) is False
        assert requires_approval("check_headers", {"url": "http://example.com"}) is False

    def test_auto_reject_dangerous_patterns(self):
        """Test auto-rejection of dangerous command patterns."""
        # Test rm -rf /
        result = check_auto_reject("execute_terminal_command", {"command": "rm -rf /"})
        assert result is not None
        assert "automatically rejected" in result.lower()

        # Test dd disk wipe
        result = check_auto_reject(
            "execute_terminal_command", {"command": "dd if=/dev/zero of=/dev/sda"}
        )
        assert result is not None

        # Test fork bomb
        result = check_auto_reject("execute_terminal_command", {"command": ":(){ :|:& };:"})
        assert result is not None

    def test_safe_commands_not_auto_rejected(self):
        """Test that safe commands are not auto-rejected."""
        result = check_auto_reject("execute_terminal_command", {"command": "ls -la"})
        assert result is None

        result = check_auto_reject("execute_terminal_command", {"command": "cat /etc/hosts"})
        assert result is None

    def test_risk_level_classification(self):
        """Test risk level classification for tools."""
        # CRITICAL
        risk_info = get_tool_risk_info("execute_terminal_command")
        assert risk_info.risk_level == RiskLevel.CRITICAL

        # HIGH
        risk_info = get_tool_risk_info("run_nmap_scan")
        assert risk_info.risk_level == RiskLevel.HIGH

        # MEDIUM
        risk_info = get_tool_risk_info("check_service_status")
        assert risk_info.risk_level == RiskLevel.MEDIUM

        # LOW (default for unknown tools)
        risk_info = get_tool_risk_info("unknown_tool")
        assert risk_info.risk_level == RiskLevel.LOW

    def test_risk_info_contains_required_fields(self):
        """Test that risk info contains all required fields."""
        risk_info = get_tool_risk_info("execute_terminal_command")

        assert hasattr(risk_info, "risk_level")
        assert hasattr(risk_info, "reason")
        assert hasattr(risk_info, "requires_approval")
        assert hasattr(risk_info, "estimated_duration")
        assert hasattr(risk_info, "reversible")

    def test_risk_info_to_dict(self):
        """Test conversion of risk info to dictionary."""
        risk_info = get_tool_risk_info("run_nmap_scan")
        risk_dict = risk_info.to_dict()

        assert isinstance(risk_dict, dict)
        assert "risk_level" in risk_dict
        assert "reason" in risk_dict
        assert "requires_approval" in risk_dict
        assert risk_dict["risk_level"] == "HIGH"


class TestOrchestratorApprovalGate:
    """Test orchestrator approval gate integration."""

    def test_should_continue_routes_to_approval_gate(self):
        """Test that dangerous tools route to approval gate."""
        from langchain_core.messages import AIMessage

        from app.services.orchestrator import OrchestratorService

        orchestrator = OrchestratorService()

        # Create state with dangerous tool call
        state = {
            "messages": [
                AIMessage(content="TOOL: execute_terminal_command(command='rm -rf /tmp/test')")
            ],
            "tool_calls": [],
            "animation_steps": [],
            "diagram_nodes": [],
            "diagram_edges": [],
        }

        # Should route to approval_gate
        next_node = orchestrator._should_continue(state)
        assert next_node == "approval_gate"
        assert "pending_approval" in state

    def test_should_continue_routes_to_tools_for_safe(self):
        """Test that safe tools route directly to tools."""
        from langchain_core.messages import AIMessage

        from app.services.orchestrator import OrchestratorService

        orchestrator = OrchestratorService()

        # Create state with safe tool call
        state = {
            "messages": [AIMessage(content="TOOL: search_cve(keyword='apache')")],
            "tool_calls": [],
            "animation_steps": [],
            "diagram_nodes": [],
            "diagram_edges": [],
        }

        # Should route to tools
        next_node = orchestrator._should_continue(state)
        assert next_node == "tools"
        assert "pending_approval" not in state

    def test_auto_reject_routes_to_end(self):
        """Test that auto-rejected tools route to end."""
        from langchain_core.messages import AIMessage

        from app.services.orchestrator import OrchestratorService

        orchestrator = OrchestratorService()

        # Create state with auto-rejected command
        state = {
            "messages": [AIMessage(content="TOOL: execute_terminal_command(command='rm -rf /')")],
            "tool_calls": [],
            "animation_steps": [],
            "diagram_nodes": [],
            "diagram_edges": [],
        }

        # Should route to end (auto-rejected)
        next_node = orchestrator._should_continue(state)
        assert next_node == "end"
        assert "auto_rejected" in state

    def test_approval_gate_creates_message(self):
        """Test that approval gate creates proper message."""
        from app.services.orchestrator import OrchestratorService

        orchestrator = OrchestratorService()

        # Create state with pending approval
        state = {
            "messages": [],
            "pending_approval": {
                "tool_name": "run_nmap_scan",
                "tool_args": {"target": "192.168.1.1"},
                "risk_info": {
                    "risk_level": "HIGH",
                    "reason": "Network scanning requires authorization",
                    "warning": "Ensure you have permission",
                },
            },
            "animation_steps": [],
            "diagram_nodes": [],
            "diagram_edges": [],
        }

        # Call approval gate
        result = orchestrator._approval_gate(state)

        assert "messages" in result
        assert len(result["messages"]) > 0
        assert "Approval Required" in result["messages"][0].content
        assert result["approval_status"] == "pending"


@pytest.mark.asyncio
class TestApprovalAPI:
    """Test approval API endpoints."""

    async def test_get_pending_approval_unauthorized(self, client):
        """Test that unauthorized requests are rejected."""
        response = await client.get("/api/v1/approvals/user_1_conv_1")
        assert response.status_code == 401

    async def test_get_pending_approval_wrong_user(
        self, client, auth_headers_user1, auth_headers_user2
    ):
        """Test that users can't access other users' approvals."""
        # User 1 tries to access user 2's approval
        response = await client.get("/api/v1/approvals/user_2_conv_1", headers=auth_headers_user1)
        assert response.status_code == 403

    async def test_approve_tool_unauthorized(self, client):
        """Test that unauthorized approval requests are rejected."""
        response = await client.post("/api/v1/approvals/user_1_conv_1", json={"action": "approve"})
        assert response.status_code == 401

    async def test_approve_tool_invalid_action(self, client, auth_headers_user1):
        """Test that invalid actions are rejected."""
        response = await client.post(
            "/api/v1/approvals/user_1_conv_1",
            headers=auth_headers_user1,
            json={"action": "invalid"},
        )
        assert response.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
