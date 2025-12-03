"""Authorization and access control system for CMatrix."""

import hashlib
import json
import os
from datetime import datetime
from typing import Optional


class AuthorizationManager:
    """Manages target authorization and API key validation."""

    def __init__(self, config_path: str = "data/auth_config.json"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load authorization configuration."""
        if os.path.exists(self.config_path):
            with open(self.config_path) as f:
                return json.load(f)
        return {"authorized_targets": [], "api_keys": {}, "scope_limits": {}}

    def _save_config(self):
        """Save authorization configuration."""
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)

    def generate_api_key(self, user_id: str, description: str = "") -> str:
        """Generate a new API key for a user."""
        key = hashlib.sha256(f"{user_id}{datetime.now().isoformat()}".encode()).hexdigest()
        self.config["api_keys"][key] = {
            "user_id": user_id,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "active": True,
        }
        self._save_config()
        return key

    def validate_api_key(self, api_key: str) -> Optional[dict]:
        """Validate an API key and return user info."""
        if api_key in self.config["api_keys"]:
            key_info = self.config["api_keys"][api_key]
            if key_info.get("active", False):
                return key_info
        return None

    def authorize_target(self, target: str, user_id: str, scope: list[str] = None) -> bool:
        """Authorize a target for scanning."""
        # Check if target is already authorized
        for auth_target in self.config["authorized_targets"]:
            if auth_target["target"] == target:
                return True

        # Add new authorization
        self.config["authorized_targets"].append(
            {
                "target": target,
                "authorized_by": user_id,
                "authorized_at": datetime.now().isoformat(),
                "scope": scope or ["network", "web", "auth"],
            }
        )
        self._save_config()
        return True

    def is_target_authorized(self, target: str) -> bool:
        """Check if a target is authorized for scanning."""
        # Allow localhost, local, and local IPs by default
        if target in ["localhost", "local", "127.0.0.1", "::1"]:
            return True

        for auth_target in self.config["authorized_targets"]:
            if auth_target["target"] == target:
                return True

        return False

    def get_scope_limits(self, target: str) -> list[str]:
        """Get scope limits for a target."""
        for auth_target in self.config["authorized_targets"]:
            if auth_target["target"] == target:
                return auth_target.get("scope", ["network", "web", "auth"])

        return []

    def revoke_target_authorization(self, target: str) -> bool:
        """Revoke authorization for a target."""
        self.config["authorized_targets"] = [
            t for t in self.config["authorized_targets"] if t["target"] != target
        ]
        self._save_config()
        return True

    def revoke_api_key(self, api_key: str) -> bool:
        """Revoke an API key."""
        if api_key in self.config["api_keys"]:
            self.config["api_keys"][api_key]["active"] = False
            self._save_config()
            return True
        return False

    def list_authorized_targets(self) -> list[dict]:
        """List all authorized targets."""
        return self.config["authorized_targets"]

    def list_api_keys(self) -> list[dict]:
        """List all API keys."""
        return [
            {
                "key": key[:8] + "..." + key[-8:],
                "user_id": info["user_id"],
                "description": info.get("description", ""),
                "created_at": info["created_at"],
                "active": info["active"],
            }
            for key, info in self.config["api_keys"].items()
        ]


# Global authorization manager instance
auth_manager = AuthorizationManager()
