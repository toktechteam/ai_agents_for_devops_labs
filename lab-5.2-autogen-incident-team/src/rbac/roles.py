import yaml
import os

RBAC_FILE = "configs/rbac.yaml"

with open(RBAC_FILE, "r") as f:
    RBAC_DATA = yaml.safe_load(f)


def check_permission(role: str, action: str):
    """
    Validates if an agent role is permitted to execute a given action.
    """

    role_data = RBAC_DATA["roles"].get(role)

    if not role_data:
        raise Exception(f"Unknown role: {role}")

    if action in role_data.get("deny", []):
        raise Exception(f"RBAC DENIED: {role} cannot perform '{action}'")

    if action not in role_data.get("allow", []):
        raise Exception(f"RBAC DENIED: '{action}' is not explicitly allowed for {role}")

    return True
