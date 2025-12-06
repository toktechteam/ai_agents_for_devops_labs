from autogen import AssistantAgent
from src.rbac.roles import check_permission
from src.audit.logger import audit_log
from src.sandbox.execute import run_in_sandbox


class CodeAnalysisAgent(AssistantAgent):
    def __init__(self, api_key: str, model: str):
        super().__init__(
            name="code_analysis_agent",
            system_message=(
                "You are the Code Analysis Agent. Your responsibilities:\n"
                "- Perform static analysis\n"
                "- Identify anti-patterns\n"
                "- Validate logs vs code symptoms\n"
                "- Use the Sandbox for executing micro-tests safely\n"
                "You MUST NOT perform any destructive actions."
            ),
            llm_config={"model": model, "api_key": api_key},
        )

    def analyze(self, code_snippet: str, correlation_id: str):
        check_permission("code_analysis_agent", "static_analysis")

        prompt = (
            "Analyze the following code snippet:\n"
            f"{code_snippet}\n\n"
            "- Identify risky areas\n"
            "- Spot memory leaks, infinite loops, unbounded recursion\n"
            "- Suggest minimal safe changes"
        )

        audit_log("code_analysis_agent", "static_analysis", prompt, correlation_id)
        return self.complete(prompt)

    def execute_safely(self, code_snippet: str, correlation_id: str):
        check_permission("code_analysis_agent", "sandbox_execution")

        sandbox_output = run_in_sandbox(code_snippet)

        audit_log(
            "code_analysis_agent",
            "sandbox_execution",
            sandbox_output,
            correlation_id,
        )

        return sandbox_output
