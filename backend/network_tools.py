"""Network security scanning tools."""
from command_executor import command_executor

def port_scan(target, ports="1-1024"):
    """Perform a port scan on a target using nmap."""
    try:
        # Build nmap command
        command = f"nmap -p {ports} -T4 --open {target}"
        
        print(f"🔍 Executing: {command}")
        
        # Execute using command executor
        result = command_executor.execute(command, timeout=60)
        
        if not result["success"]:
            return f"Port scan failed: {result['stderr']}"
        
        output = result["stdout"]
        
        # Parse the output to extract open ports
        lines = output.split('\n')
        open_ports = []
        
        for line in lines:
            # Look for lines like "22/tcp open  ssh"
            if '/tcp' in line and 'open' in line:
                parts = line.split()
                if len(parts) >= 3:
                    port = parts[0].split('/')[0]
                    service = parts[2] if len(parts) > 2 else 'unknown'
                    open_ports.append(f"Port {port}: open ({service})")
        
        if open_ports:
            return f"Port scan results for {target}:\n" + "\n".join(open_ports)
        else:
            return f"No open ports found on {target} in range {ports}"
    
    except Exception as e:
        return f"Port scan failed: {str(e)}"

def vulnerability_assessment(target):
    """Perform basic vulnerability assessment on a target system."""
    try:
        # First, do a basic port scan to identify services
        command = f"nmap -p- --open -T4 {target}"
        
        print(f"🔍 Executing vulnerability scan: {command}")
        
        result = command_executor.execute(command, timeout=120)
        
        if not result["success"]:
            return f"Vulnerability assessment failed: {result['stderr']}"
        
        results = [f"Basic Vulnerability Assessment for {target}:"]
        open_ports = []
        
        # Parse open ports
        for line in result["stdout"].split('\n'):
            if '/tcp' in line and 'open' in line:
                parts = line.split()
                if len(parts) >= 3:
                    port = parts[0].split('/')[0]
                    service = parts[2] if len(parts) > 2 else 'unknown'
                    open_ports.append((port, service))
                    
                    # Basic vulnerability checks based on service
                    port_num = int(port)
                    if port_num == 21 and 'ftp' in service.lower():
                        results.append("⚠️  WARNING: FTP service detected on port 21 - consider using SFTP (secure)")
                    elif port_num == 23 and 'telnet' in service.lower():
                        results.append("🚨 CRITICAL: Telnet service detected on port 23 - insecure, use SSH")
                    elif port_num == 80 and 'http' in service.lower():
                        results.append("ℹ️  INFO: HTTP detected on port 80 - check for HTTPS support")
                    elif port_num == 445 and 'smb' in service.lower():
                        results.append("⚠️  WARNING: SMB service detected - check for known vulnerabilities")
                    elif port_num == 3389 and 'rdp' in service.lower():
                        results.append("⚠️  WARNING: RDP service detected - ensure NLA is enabled")
        
        # Check for common misconfigurations
        if open_ports:
            results.append(f"\nOpen ports found: {len(open_ports)}")
            for port, service in open_ports:
                results.append(f"  - Port {port}: {service}")
        else:
            results.append("No open ports detected")
        
        # Additional checks
        results.append("\nGeneral Recommendations:")
        results.append("• Ensure all services are up-to-date")
        results.append("• Use strong authentication mechanisms")
        results.append("• Implement proper firewall rules")
        results.append("• Regularly scan for vulnerabilities")
        
        return "\n".join(results)
    
    except Exception as e:
        return f"Vulnerability assessment failed: {str(e)}"