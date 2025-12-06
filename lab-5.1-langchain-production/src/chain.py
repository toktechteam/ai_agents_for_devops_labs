import json
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

from src.kubernetes_tools import get_pod_cpu, get_pod_logs
from src.cost_tracker import CostTracker


class InvestigatorChain:
    def __init__(self):
        self.model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
        )
        self.cost_tracker = CostTracker()

    def run(self, alert: str):
        pod_name = self._extract_pod_name(alert)

        cpu = get_pod_cpu(pod_name)
        logs = get_pod_logs(pod_name)

        prompt = f"""
        You are an SRE investigation assistant.

        Alert: {alert}

        Pod CPU usage: {cpu}
        Pod Logs:
        {logs}

        Based on this, analyse:
        - Root cause
        - Summary of findings
        - Metrics impact
        - Suggest 1-2 safe remediation steps only
        """

        response = self.model([HumanMessage(content=prompt)])

        cost = self.cost_tracker.calculate_cost(response)

        return {
            "analysis": response.content,
            "logs": logs,
            "metrics": cpu,
            "remediation": "Restart deployment or scale out if CPU remains high.",
            "cost": cost,
        }

    def _extract_pod_name(self, alert: str):
        # very simple pod extraction logic for learning purposes
        if "pod" in alert.lower():
            parts = alert.lower().split("pod")
            return parts[1].strip().split()[0]
        return "default-pod"
