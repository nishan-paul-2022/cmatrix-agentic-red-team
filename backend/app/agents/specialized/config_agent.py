"""Configuration Analysis Agent Subgraph."""

import subprocess
from typing import Any

from langchain_core.tools import tool
from loguru import logger

from app.agents.base.agent import BaseAgentSubgraph
from app.services.llm.providers.base import LLMProvider


@tool
def check_cloud_config(provider: str = "aws") -> str:
    """
    Check cloud configuration security (simulated - requires actual cloud credentials).

    Args:
        provider: Cloud provider (aws, gcp, azure)
    """
    # This is a placeholder - real implementation would use ScoutSuite or cloud SDKs
    results = []
    results.append(f"Cloud Configuration Analysis for {provider.upper()}")
    results.append(
        "\n⚠️  Note: This is a simulated check. Real implementation requires cloud credentials."
    )
    results.append("\nCommon Configuration Checks:")
    results.append("✅ IAM policies should follow least privilege")
    results.append("✅ S3 buckets should not be publicly accessible")
    results.append("✅ Security groups should restrict inbound traffic")
    results.append("✅ Encryption at rest should be enabled")
    results.append("✅ Logging and monitoring should be configured")
    results.append("\nRecommendation: Install ScoutSuite for comprehensive cloud security auditing")

    return "\n".join(results)


@tool
def check_system_hardening(target: str = "localhost") -> str:
    """
    Check system hardening configuration.

    Args:
        target: Target system to check
    """
    results = []
    results.append(f"System Hardening Check for {target}")

    try:
        # Check if running on localhost
        if target in ["localhost", "127.0.0.1"]:
            # Check some basic security configurations
            checks = []

            # Check firewall status
            try:
                fw_result = subprocess.run(
                    ["ufw", "status"], capture_output=True, text=True, timeout=5
                )
                if fw_result.returncode == 0:
                    if "active" in fw_result.stdout.lower():
                        checks.append("✅ Firewall is active")
                    else:
                        checks.append("⚠️  Firewall is not active")
                else:
                    checks.append("ℹ️  UFW firewall not found")
            except (FileNotFoundError, subprocess.TimeoutExpired):
                checks.append("ℹ️  Firewall check skipped (ufw not available)")

            # Check for automatic updates
            try:
                if (
                    subprocess.run(["which", "unattended-upgrades"], capture_output=True).returncode
                    == 0
                ):
                    checks.append("✅ Automatic security updates configured")
                else:
                    checks.append("⚠️  Automatic security updates not found")
            except:
                checks.append("ℹ️  Auto-update check skipped")

            results.append("\nSecurity Checks:")
            results.extend(checks)

            results.append("\nRecommendations:")
            results.append("• Enable firewall (ufw enable)")
            results.append("• Configure automatic security updates")
            results.append("• Disable unnecessary services")
            results.append("• Use strong password policies")
            results.append("• Enable SELinux/AppArmor")
            results.append("• Regular system updates")

        else:
            results.append("\n⚠️  Remote system hardening checks require SSH access")
            results.append(
                "Recommendation: Install Lynis for comprehensive system hardening audits"
            )

        return "\n".join(results)

    except Exception as e:
        return f"System hardening check failed: {str(e)}"


@tool
def check_compliance(standard: str = "CIS") -> str:
    """
    Check compliance with security standards.

    Args:
        standard: Security standard (CIS, PCI-DSS, HIPAA, SOC2)
    """
    results = []
    results.append(f"Compliance Check: {standard}")
    results.append(
        "\n⚠️  Note: This is a basic compliance overview. Full compliance requires OpenSCAP or similar tools."
    )

    compliance_checks = {
        "CIS": [
            "✅ Ensure filesystem integrity checking is enabled",
            "✅ Ensure permissions on bootloader config are configured",
            "✅ Ensure core dumps are restricted",
            "✅ Ensure address space layout randomization is enabled",
            "✅ Ensure SELinux/AppArmor is enabled",
        ],
        "PCI-DSS": [
            "✅ Install and maintain firewall configuration",
            "✅ Do not use vendor-supplied defaults",
            "✅ Protect stored cardholder data",
            "✅ Encrypt transmission of cardholder data",
            "✅ Use and regularly update anti-virus software",
        ],
        "HIPAA": [
            "✅ Access control - unique user identification",
            "✅ Audit controls - hardware, software, procedural",
            "✅ Integrity controls - data integrity",
            "✅ Transmission security - encryption",
            "✅ Person or entity authentication",
        ],
        "SOC2": [
            "✅ Security - protection against unauthorized access",
            "✅ Availability - system availability for operation",
            "✅ Processing Integrity - complete, valid, accurate processing",
            "✅ Confidentiality - confidential information protection",
            "✅ Privacy - personal information collection and use",
        ],
    }

    if standard in compliance_checks:
        results.append(f"\n{standard} Key Requirements:")
        results.extend(compliance_checks[standard])
    else:
        results.append(f"\nStandard '{standard}' not recognized")
        results.append(f"Supported standards: {', '.join(compliance_checks.keys())}")

    results.append("\nRecommendation: Use OpenSCAP for automated compliance scanning")

    return "\n".join(results)


# Legacy tool list for backward compatibility
CONFIG_TOOLS = [check_cloud_config, check_system_hardening, check_compliance]


class ConfigAgentSubgraph(BaseAgentSubgraph):
    """
    Configuration Analysis Agent Subgraph.

    This agent is responsible for:
    - Cloud configuration security (AWS, GCP, Azure)
    - System hardening checks (Linux, Windows)
    - Compliance auditing (CIS, PCI-DSS, HIPAA, SOC2)
    """

    def __init__(self, llm_provider: LLMProvider):
        """Initialize the Configuration Analysis Agent."""
        super().__init__(llm_provider, agent_name="ConfigAnalysisAgent")
        logger.info("Config Analysis Agent initialized with autonomous reasoning")

    def _register_tools(self) -> list[dict[str, Any]]:
        """Register configuration analysis tools."""
        return [
            {
                "name": "check_cloud_config",
                "function": check_cloud_config,
                "description": "Check cloud configuration security for providers like AWS, GCP, Azure.",
                "parameters": {"provider": "Cloud provider (aws, gcp, azure)"},
            },
            {
                "name": "check_system_hardening",
                "function": check_system_hardening,
                "description": "Check system hardening configuration for a target system.",
                "parameters": {"target": "Target system to check (e.g., 'localhost')"},
            },
            {
                "name": "check_compliance",
                "function": check_compliance,
                "description": "Check compliance with security standards like CIS, PCI-DSS, HIPAA, SOC2.",
                "parameters": {"standard": "Security standard (CIS, PCI-DSS, HIPAA, SOC2)"},
            },
        ]

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Config Analysis Agent."""
        return """You are the Configuration Analysis Agent, a specialized AI expert in system hardening and compliance.

Your core responsibilities:
1. **Cloud Security**: Audit cloud configurations (IAM, S3, Security Groups) for misconfigurations.
2. **System Hardening**: Verify system settings (Firewall, Updates, Services) against best practices.
3. **Compliance**: Check adherence to standards like CIS, PCI-DSS, HIPAA, and SOC2.

When analyzing configurations:
- Always recommend least privilege principles.
- Verify that encryption is enabled at rest and in transit.
- Check for default credentials and insecure default settings.
- Ensure logging and monitoring are active.
- Provide specific remediation steps for non-compliant items.

Communication style:
- Be precise and technical.
- Reference specific security controls (e.g., "CIS 1.1.1").
- Prioritize findings by risk and compliance impact.
"""


def create_config_agent(llm_provider: LLMProvider) -> ConfigAgentSubgraph:
    """Factory function to create a Config Analysis Agent instance."""
    return ConfigAgentSubgraph(llm_provider)
