from typing import Any, Dict, List

from config import get_settings
from models import Plan, PlanStep


class LLMClient:
    """
    A very small abstraction over "LLM as planner".

    For this lab:
    - If OPENAI_API_KEY is set and you add OpenAI client, you could call a real model.
    - By default, it uses a deterministic rule-based planner so the lab runs offline.
    """

    def __init__(self) -> None:
        self.settings = get_settings()

    def create_investigation_plan(
        self,
        alert: Dict[str, Any],
        tools_metadata: Dict[str, Dict[str, Any]],
        recent_episodes: List[Dict[str, Any]],
    ) -> Plan:
        """
        For now, plan is created deterministically based on alert type.
        This mimics "agent reasoning" without requiring a real LLM.
        """
        alert_type = alert.get("type", "unknown")
        service = alert.get("service", "unknown")

        goal = f"Investigate and respond to alert '{alert_type}' for service '{service}'"

        steps: List[PlanStep] = []

        # Basic patterns similar to Chapter 4 scenarios
        if alert_type == "high_cpu":
            steps.append(
                PlanStep(
                    step="1",
                    action="List pods for the service",
                    tool="get_pod_status",
                    params={"namespace": "default", "service": service},
                )
            )
            steps.append(
                PlanStep(
                    step="2",
                    action="Check service metrics",
                    tool="get_service_metrics",
                    params={"service": service},
                )
            )
        elif alert_type == "high_memory":
            steps.append(
                PlanStep(
                    step="1",
                    action="List pods for the service",
                    tool="get_pod_status",
                    params={"namespace": "default", "service": service},
                )
            )
            steps.append(
                PlanStep(
                    step="2",
                    action="Fetch logs from main pod",
                    tool="get_pod_logs",
                    params={"namespace": "default", "pod": f"{service}-pod"},
                )
            )
        else:
            steps.append(
                PlanStep(
                    step="1",
                    action="List pods for the service",
                    tool="get_pod_status",
                    params={"namespace": "default", "service": service},
                )
            )

        # In a real agent, recent episodes could influence the plan
        # For now, we just attach them to context if needed.

        return Plan(goal=goal, steps=steps)
