from autogen import AssistantAgent
from src.rbac.roles import check_permission
from src.audit.logger import audit_log


class InvestigatorAgent(AssistantAgent):
    def __init__(self, api_key: str, model: str):
        super().__init__(
            name="sre_investigator",
            system_message=(
                "You are the SRE Investigator. Your responsibilities:\n"
                "- Analyze symptoms\n"
                "- Review logs\n"
                "- Identify root cause\n"
                "- Determine immediate operational risk\n"
                "Return short, clear answers ONLY."
            ),
            llm_config={"model": model, "api_key": api_key},
        )

    def investigate(self, alert: str, logs: str, correlation_id: str):
        check_permission("sre_investigator", "analyze_alerts")

        prompt = (
            f"ALERT:\n{alert}\n\nLOGS:\n{logs}\n\n"
            "Based on alert + logs:\n"
            "- Identify root cause\n"
            "- Summarize findings\n"
            "- Suggest immediate next steps"
        )

        audit_log("sre_investigator", "investigate", prompt, correlation_id)

        return self.complete(prompt)
