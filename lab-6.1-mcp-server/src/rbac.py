ALLOWED_ACTIONS = {
    "reader": [
        "k8s.list_pods",
        "prom.query_simple",
        "logs.search",
        "ctx.get"
    ],
    "operator": [
        "runbook.preview",
        "runbook.execute",
        "ctx.set"
    ]
}


def check_rbac(expected_role, tool_name):
    allowed = ALLOWED_ACTIONS.get(expected_role, [])
    if tool_name not in allowed:
        raise PermissionError(f"RBAC: role '{expected_role}' not allowed to call '{tool_name}'")
