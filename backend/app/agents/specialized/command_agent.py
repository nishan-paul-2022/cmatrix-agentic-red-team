"""General command execution agent - allows running terminal commands."""

from langchain_core.tools import tool

from app.core.security import auth_manager
from app.services.command_executor import command_executor


@tool
def execute_terminal_command(command: str, target: str = "localhost") -> str:
    """
    Execute a terminal command for security testing.

    Args:
        command: The command to execute (e.g., "nmap -p 80 localhost")
        target: The target being tested (for authorization check)

    Note: Only whitelisted commands are allowed for security.
    """
    # Check authorization for the target
    if not auth_manager.is_target_authorized(target):
        return f"❌ Target '{target}' is not authorized. Please authorize it first."

    # Execute the command
    result = command_executor.execute(command, timeout=60)

    if result["success"]:
        output = "✅ Command executed successfully:\n\n"
        output += f"Command: {command}\n"
        output += f"Exit code: {result['returncode']}\n\n"
        output += f"Output:\n{result['stdout']}"

        if result["stderr"]:
            output += f"\n\nErrors/Warnings:\n{result['stderr']}"

        return output
    else:
        return f"❌ Command failed:\n\nCommand: {command}\nError: {result['stderr']}"


@tool
def run_nmap_scan(target: str, ports: str = "1-1000", scan_type: str = "basic") -> str:
    """
    Run an nmap scan with predefined scan types.

    Args:
        target: Target IP or hostname
        ports: Port range (e.g., "1-1000", "80,443", "1-65535")
        scan_type: Type of scan (basic, fast, full, vuln)
    """
    # Check authorization
    if not auth_manager.is_target_authorized(target):
        return f"❌ Target '{target}' is not authorized. Please authorize it first."

    # Build nmap command based on scan type
    scan_commands = {
        "basic": f"nmap -p {ports} -T4 --open {target}",
        "fast": f"nmap -p {ports} -T5 --open {target}",
        "full": f"nmap -p {ports} -T4 -A --open {target}",
        "vuln": f"nmap -p {ports} -T4 --script vuln {target}",
        "service": f"nmap -p {ports} -T4 -sV --open {target}",
    }

    command = scan_commands.get(scan_type, scan_commands["basic"])

    print(f"🔍 Running {scan_type} nmap scan: {command}")

    result = command_executor.execute(command, timeout=120)

    if result["success"]:
        return f"Nmap {scan_type} scan results for {target}:\n\n{result['stdout']}"
    else:
        return f"Scan failed: {result['stderr']}"


@tool
def check_service_status(service_name: str) -> str:
    """
    Check the status of a system service.

    Args:
        service_name: Name of the service (e.g., "nginx", "apache2", "ssh")
    """
    command = f"systemctl status {service_name}"

    result = command_executor.execute(command, timeout=10)

    if result["success"]:
        # Parse the output for key information
        output = result["stdout"]
        lines = output.split("\n")

        status_info = []
        for line in lines[:10]:  # First 10 lines usually have the important info
            if any(
                keyword in line.lower()
                for keyword in ["active", "loaded", "main pid", "memory", "cpu"]
            ):
                status_info.append(line.strip())

        return f"Service status for '{service_name}':\n\n" + "\n".join(status_info)
    else:
        return f"Could not check service status: {result['stderr']}"


@tool
def run_curl_request(url: str, method: str = "GET", headers: str = "") -> str:
    """
    Make an HTTP request using curl to test web endpoints.

    Args:
        url: The URL to request
        method: HTTP method (GET, POST, HEAD, OPTIONS)
        headers: Additional headers (e.g., "Authorization: Bearer token")
    """
    # Build curl command
    command = f"curl -X {method} -i"

    if headers:
        for header in headers.split(";"):
            if header.strip():
                command += f" -H '{header.strip()}'"

    command += f" '{url}'"

    print(f"🌐 Executing: {command}")

    result = command_executor.execute(command, timeout=30)

    if result["success"]:
        return f"HTTP Response:\n\n{result['stdout']}"
    else:
        return f"Request failed: {result['stderr']}"


COMMAND_TOOLS = [execute_terminal_command, run_nmap_scan, check_service_status, run_curl_request]
