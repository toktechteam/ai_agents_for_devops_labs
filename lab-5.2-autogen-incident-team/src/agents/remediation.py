from autogen import AssistantAgent
from src.rbac.roles import check_permission
from src.audit.logger import audit_log


class RemediationAgent(AssistantAgent):
    def __init__(self, api_key: str, model: str):
        super().__init__(
            name="remediation_agent",
            system_message=(
                "You are the Remediation Agent. Your job:\n"
                "- Produce SAFE remediation plans\n"
                "- Suggest config changes, scaling, restarts\n"
                "- Suggest small code patches ONLY when approved\n"
                "Never deploy anything automatically."
            ),
            llm_config={"model": model, "api_key": api_key},
        )

    def propose_fix(self, findings: str, correlation_id: str):
        check_permission("remediation_agent", "propose_fix")

        prompt = (
            "Based on the findings, propose a safe remediation plan.\n"
            "NEVER deploy automatically.\n"
            "Findings:\n"
            f"{findings}"
        )

        audit_log("remediation_agent", "propose_fix", prompt, correlation_id)

        return self.complete(prompt)
