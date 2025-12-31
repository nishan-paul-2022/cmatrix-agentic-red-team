"""Command execution module for CMatrix - allows agents to run terminal commands."""

import shlex
import subprocess
from typing import Any, Dict

from app.utils.audit_logger import audit_logger


class CommandExecutor:
    """Safely execute terminal commands with logging and validation."""

    # Whitelist of allowed commands for security
    ALLOWED_COMMANDS = {
        "nmap",
        "curl",
        "wget",
        "dig",
        "host",
        "ping",
        "netstat",
        "ss",
        "lsof",
        "ufw",
        "iptables",
        "openssl",
        "ssh",
        "telnet",
        "nc",
        "ncat",
        "python3",
        "python",
        "node",
        "npm",
        "git",
        "docker",
        "kubectl",
        "systemctl",
        "service",
        "ps",
        "top",
        "which",
        "whereis",
        "find",
        "grep",
        "awk",
        "sed",
        "sudo",  # Added for privileged scans
        "cat",
        "less",
        "tail",
        "head",  # File viewing
        "ls",
        "pwd",
        "whoami",  # Basic commands
    }

    def __init__(self, user_id: str = "system"):
        self.user_id = user_id

    def is_command_allowed(self, command: str) -> bool:
        """Check if a command is in the whitelist."""
        # Get the base command (first word)
        base_cmd = shlex.split(command)[0] if command else ""

        # Check if it's in allowed list
        return base_cmd in self.ALLOWED_COMMANDS

    def execute(
        self, command: str, timeout: int = 30, capture_output: bool = True, shell: bool = False
    ) -> dict[str, Any]:
        """
        Execute a terminal command safely.

        Args:
            command: Command to execute
            timeout: Maximum execution time in seconds
            capture_output: Whether to capture stdout/stderr
            shell: Whether to use shell (dangerous, use sparingly)

        Returns:
            Dict with 'success', 'stdout', 'stderr', 'returncode'
        """
        # Log the command execution attempt
        audit_logger.log_event(
            event_type="COMMAND_EXECUTION",
            user_id=self.user_id,
            action="execute_command",
            details={"command": command},
            severity="INFO",
        )

        # Validate command
        if not self.is_command_allowed(command):
            base_cmd = shlex.split(command)[0] if command else "unknown"
            audit_logger.log_event(
                event_type="COMMAND_BLOCKED",
                user_id=self.user_id,
                action="blocked_command",
                result="denied",
                details={"command": command, "reason": "not in whitelist"},
                severity="WARNING",
            )
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Command '{base_cmd}' is not allowed for security reasons",
                "returncode": -1,
                "command": command,
            }

        try:
            # Translate paths to use the mounted host filesystem at /host
            # This avoids permission issues with chroot/nsenter while still
            # providing access to the actual host filesystem

            # Translate common path patterns to /host equivalents
            import os
            import re

            # Get the host user's home directory from environment or default
            # Since we're in a container, we need to infer the host user
            # We'll use the first non-root user's home from /host/home
            host_home = "/host/home/nishan"  # Default, can be made configurable

            # Translate ~ to host home directory
            translated_cmd = command.replace("~/", f"{host_home}/")
            translated_cmd = re.sub(r"\s~/", f" {host_home}/", translated_cmd)
            translated_cmd = re.sub(r"^~/", f"{host_home}/", translated_cmd)

            # Translate absolute paths that should reference host
            # Only translate if not already prefixed with /host
            if not translated_cmd.startswith("/host"):
                # Common directories that should reference host
                for host_dir in ["/etc", "/var", "/usr", "/opt", "/tmp"]:
                    translated_cmd = re.sub(rf"\s{host_dir}/", f" /host{host_dir}/", translated_cmd)
                    if translated_cmd.startswith(f"{host_dir}/"):
                        translated_cmd = f"/host{translated_cmd}"

            # Set up environment to use host filesystem paths
            # Keep container's binaries but access host filesystem
            env = os.environ.copy()
            # Add host paths for accessing host-specific files/directories
            # But use container's own binaries (ps, ip, etc.) which are now installed

            # Execute the translated command
            if shell:
                result = subprocess.run(
                    translated_cmd,
                    shell=True,
                    capture_output=capture_output,
                    text=True,
                    timeout=timeout,
                    env=env,
                )
            else:
                result = subprocess.run(
                    shlex.split(translated_cmd),
                    capture_output=capture_output,
                    text=True,
                    timeout=timeout,
                    env=env,
                )

            # Log successful execution
            audit_logger.log_event(
                event_type="COMMAND_EXECUTED",
                user_id=self.user_id,
                action="command_completed",
                result="success",
                details={
                    "command": command,
                    "returncode": result.returncode,
                    "output_length": len(result.stdout) if result.stdout else 0,
                },
                severity="INFO",
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "command": command,
            }

        except subprocess.TimeoutExpired:
            audit_logger.log_event(
                event_type="COMMAND_TIMEOUT",
                user_id=self.user_id,
                action="command_timeout",
                result="timeout",
                details={"command": command, "timeout": timeout},
                severity="WARNING",
            )
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds",
                "returncode": -1,
                "command": command,
            }

        except FileNotFoundError:
            audit_logger.log_event(
                event_type="COMMAND_NOT_FOUND",
                user_id=self.user_id,
                action="command_not_found",
                result="error",
                details={"command": command},
                severity="ERROR",
            )
            return {
                "success": False,
                "stdout": "",
                "stderr": "Command not found. Please install the required tool.",
                "returncode": -1,
                "command": command,
            }

        except Exception as e:
            audit_logger.log_event(
                event_type="COMMAND_ERROR",
                user_id=self.user_id,
                action="command_error",
                result="error",
                details={"command": command, "error": str(e)},
                severity="ERROR",
            )
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Error executing command: {str(e)}",
                "returncode": -1,
                "command": command,
            }

    def execute_with_sudo(self, command: str, timeout: int = 30) -> dict[str, Any]:
        """
        Execute a command with sudo (requires passwordless sudo or user interaction).
        Use with extreme caution!
        """
        sudo_command = f"sudo {command}"

        audit_logger.log_event(
            event_type="SUDO_COMMAND",
            user_id=self.user_id,
            action="sudo_execution",
            details={"command": sudo_command},
            severity="WARNING",
        )

        return self.execute(sudo_command, timeout=timeout)


# Global command executor instance
command_executor = CommandExecutor()
