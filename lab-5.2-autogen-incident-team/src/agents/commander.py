from autogen import AssistantAgent
from src.rbac.roles import check_permission
from src.audit.logger import audit_log


class CommanderAgent(AssistantAgent):
    def __init__(self, api_key: str, model: str):
        super().__init__(
            name="incident_commander",
            system_message=(
                "You are the Incident Commander. You coordinate the entire IR workflow. "
                "Your job is to:\n"
                "- Interpret alerts\n"
                - "Assign tasks to SRE Investigator\n"
                "- Request code review from Code Analysis Agent\n"
                "- Approve remediation actions\n"
                "You DO NOT perform technical investigations directly."
            ),
            llm_config={"model": model, "api_key": api_key},
        )

    def delegate_investigation(self, investigator, alert: str, correlation_id: str):
        check_permission("incident_commander", "orchestrate_workflow")

        msg = (
            f"New alert raised:\n{alert}\n"
            "Please investigate symptoms, metrics, and logs."
        )

        audit_log("incident_commander", "delegate_investigation", msg, correlation_id)

        return investigator.complete(msg)

    def request_code_review(self, code_agent, scenario_code: str, correlation_id: str):
        check_permission("incident_commander", "orchestrate_workflow")

        prompt = (
            "The SRE investigator suspects code-level issues.\n"
            "Review the following snippet for problems:\n"
            f"{scenario_code}"
        )

        audit_log("incident_commander", "request_code_review", prompt, correlation_id)

        return code_agent.complete(prompt)

    def approve_remediation(self, remediation_agent, findings: str, correlation_id: str):
        check_permission("incident_commander", "approve_actions")

        prompt = (
            "Based on the findings, generate a safe remediation plan that does not "
            "deploy code directly but suggests safe operational steps.\n"
            f"Findings:\n{findings}"
        )

        audit_log("incident_commander", "approve_remediation", prompt, correlation_id)

        return remediation_agent.complete(prompt)
