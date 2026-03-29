# Human-in-the-Loop (HITL) Approval System

**Status:** ✅ Production Ready

---

## 1. Overview
The HITL system ensures that dangerous or sensitive operations (e.g., system commands, network scans) require explicit user approval before execution. It acts as a security layer for the autonomous agent, preventing unauthorized actions on the host system.

## 2. Architecture

### Workflow
1. **Tool Selection**: Agent selects a tool based on user request.
2. **Risk Assessment**: System checks the tool against the `DANGEROUS_TOOLS` registry.
3. **Approval Gate**:
   - If **Safe**: Tool executes immediately.
   - If **Dangerous**: Workflow pauses (LangGraph `interrupt_after`), state is checkpointed to PostgreSQL, and the user is prompted.
4. **User Action**: User approves (potentially with modified arguments) or rejects via the UI.
5. **Resumption**: Workflow resumes, executing the tool or handling the rejection.

### Components
- **Backend**:
  - **Orchestrator**: Manages the LangGraph workflow and interruption logic.
  - **Database**: PostgreSQL stores workflow state (checkpoints) and audit logs.
- **Frontend**:
  - **ApprovalCard**: Interactive UI component displaying risk level, warning, and parameters. Allows editing arguments before approval.

## 3. Configuration & Risk Levels

Tools are configured in `app-backend/app/core/approval_config.py`.

| Level | Color | Approval | Examples |
|-------|-------|----------|----------|
| **CRITICAL** | 🔴 Red | **Always** | `execute_terminal_command` (write/exec), `rm`, `dd` |
| **HIGH** | 🟠 Orange | **Always** | `run_nmap_scan`, `modify_config` |
| **MEDIUM** | 🟡 Yellow | Configurable | `check_service_status`, `read_logs` |
| **LOW** | 🟢 Green | Never | `search_cve`, `check_headers` |

### Adding a Dangerous Tool
```python
# app-backend/app/core/approval_config.py
DANGEROUS_TOOLS = {
    "your_tool_name": ToolRiskInfo(
        risk_level=RiskLevel.HIGH,
        reason="Potential system impact",
        requires_approval=True,
        warning="⚠️ Verify target before execution"
    )
}
```

## 4. API Reference

### Get Pending Approval
`GET /api/v1/approvals/{thread_id}`
Returns details of the paused workflow step, including tool name, arguments, and risk info.

### Submit Decision
`POST /api/v1/approvals/{thread_id}`
**Body:**
```json
{
  "action": "approve",  // or "reject"
  "modified_args": { "arg": "new_value" },  // Optional: override arguments
  "reason": "Audit trail note"              // Optional
}
```

## 5. Security Features

- **Auto-Rejection**: Regex patterns immediately block catastrophic commands (e.g., `rm -rf /`, fork bombs, disk wipes) without bothering the user.
- **Audit Logging**: All decisions are recorded in the `approval_logs` table with timestamp, user ID, tool args, and decision rationale.
- **State Integrity**: Checkpointing ensures the workflow resumes exactly where it left off; hash verification prevents state tampering.

## 6. Testing & Verification

### Unit Tests
Run backend tests to verify logic:
```bash
pytest app-backend/tests/test_approval_gates.py
```

### Manual Verification
1. **Trigger**: Ask the agent to "List files in /etc".
2. **Verify**:
   - "Approval Required" card appears with Red/Orange badge.
   - Buttons are interactive.
3. **Action**: Click "Approve".
4. **Result**: Spinner appears, then the command output is displayed.

---
*Status: Production Ready (Nov 26, 2025)*
