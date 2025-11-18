"""Audit logging system for CMatrix."""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any

class AuditLogger:
    """Structured audit logging for security operations."""
    
    def __init__(self, log_dir: str = "audit_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup JSON file logger
        self.log_file = self.log_dir / f"audit_{datetime.now().strftime('%Y%m%d')}.jsonl"
        
        # Setup Python logger
        self.logger = logging.getLogger("cmatrix.audit")
        self.logger.setLevel(logging.INFO)
        
        # File handler for JSON logs
        handler = logging.FileHandler(self.log_file)
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)
        
        # Console handler for important events
        console = logging.StreamHandler()
        console.setLevel(logging.WARNING)
        formatter = logging.Formatter('%(asctime)s - AUDIT - %(levelname)s - %(message)s')
        console.setFormatter(formatter)
        self.logger.addHandler(console)
    
    def log_event(
        self,
        event_type: str,
        user_id: str,
        target: Optional[str] = None,
        action: Optional[str] = None,
        result: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        severity: str = "INFO"
    ):
        """Log an audit event."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "target": target,
            "action": action,
            "result": result,
            "severity": severity,
            "details": details or {}
        }
        
        # Write to JSON log file
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
        
        # Log to Python logger
        log_msg = f"{event_type} | User: {user_id} | Target: {target} | Action: {action} | Result: {result}"
        
        if severity == "ERROR":
            self.logger.error(log_msg)
        elif severity == "WARNING":
            self.logger.warning(log_msg)
        else:
            self.logger.info(log_msg)
    
    def log_scan_start(self, user_id: str, target: str, scan_type: str):
        """Log the start of a security scan."""
        self.log_event(
            event_type="SCAN_START",
            user_id=user_id,
            target=target,
            action=f"start_{scan_type}_scan",
            result="initiated",
            severity="INFO"
        )
    
    def log_scan_complete(self, user_id: str, target: str, scan_type: str, findings: int):
        """Log the completion of a security scan."""
        self.log_event(
            event_type="SCAN_COMPLETE",
            user_id=user_id,
            target=target,
            action=f"complete_{scan_type}_scan",
            result="success",
            details={"findings_count": findings},
            severity="INFO"
        )
    
    def log_scan_error(self, user_id: str, target: str, scan_type: str, error: str):
        """Log a scan error."""
        self.log_event(
            event_type="SCAN_ERROR",
            user_id=user_id,
            target=target,
            action=f"{scan_type}_scan",
            result="error",
            details={"error": error},
            severity="ERROR"
        )
    
    def log_authorization_check(self, user_id: str, target: str, authorized: bool):
        """Log an authorization check."""
        self.log_event(
            event_type="AUTH_CHECK",
            user_id=user_id,
            target=target,
            action="check_authorization",
            result="authorized" if authorized else "denied",
            severity="WARNING" if not authorized else "INFO"
        )
    
    def log_api_key_usage(self, api_key_prefix: str, user_id: str, endpoint: str):
        """Log API key usage."""
        self.log_event(
            event_type="API_KEY_USAGE",
            user_id=user_id,
            target=None,
            action=f"access_{endpoint}",
            result="success",
            details={"api_key_prefix": api_key_prefix},
            severity="INFO"
        )
    
    def log_unauthorized_attempt(self, user_id: str, target: str, reason: str):
        """Log an unauthorized access attempt."""
        self.log_event(
            event_type="UNAUTHORIZED_ATTEMPT",
            user_id=user_id,
            target=target,
            action="attempted_scan",
            result="blocked",
            details={"reason": reason},
            severity="WARNING"
        )
    
    def get_recent_logs(self, limit: int = 100) -> list:
        """Get recent audit logs."""
        logs = []
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
                for line in lines[-limit:]:
                    try:
                        logs.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return logs

# Global audit logger instance
audit_logger = AuditLogger()
