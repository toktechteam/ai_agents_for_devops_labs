RUNBOOKS = {
    "restart-api": [
        "kubectl rollout restart deployment api-service",
        "kubectl get pods -l app=api-service"
    ]
}


def runbook_preview(args):
    rb = args["runbook_id"]
    steps = RUNBOOKS.get(rb)
    if not steps:
        raise ValueError("Unknown runbook")
    return {"runbook": rb, "steps": steps}


def runbook_execute(args):
    rb = args["runbook_id"]
    approver = args.get("approved_by")
    if not approver:
        raise PermissionError("Runbook execution requires human approval")

    steps = RUNBOOKS.get(rb)
    if not steps:
        raise ValueError("Unknown runbook")

    # NO REAL EXECUTION (Safety)
    return {"status": "approved", "executed_steps": steps, "approved_by": approver}
