from typing import Dict, Any

from src.workflow.coordination import run_incident_workflow
from src.utils.constants import DEFAULT_SCENARIOS


class IncidentPipeline:
    """
    High-level pipeline wrapper around the incident workflow.

    This keeps a clean abstraction:
    - API, CLI, and tests call this pipeline
    - Internal orchestration lives in run_incident_workflow(...)
    """

    def __init__(self, default_scenarios=None) -> None:
        self.default_scenarios = default_scenarios or DEFAULT_SCENARIOS

    def list_scenarios(self):
        """
        Return the list of supported scenarios.
        """
        return list(self.default_scenarios)

    def run(self, scenario: str, auto_approve: bool = False) -> Dict[str, Any]:
        """
        Run a full incident workflow for a given scenario name.

        :param scenario: scenario identifier (e.g. "memory_leak")
        :param auto_approve: whether to auto-run sandbox validation
        """
        if scenario not in self.default_scenarios:
            raise ValueError(
                f"Unsupported scenario '{scenario}'. "
                f"Supported scenarios: {', '.join(self.default_scenarios)}"
            )

        return run_incident_workflow(scenario_name=scenario, auto_approve=auto_approve)
