from typing import Any, Dict

from llm_client import LLMClient
from tools import ToolRegistry
from executor import SafeExecutor
from memory import MemoryManager
from planning import PlanExecutionEngine
from models import Alert


class InfrastructureAgent:
    """
    InfrastructureAgent corresponds to the Chapter 4 "Infrastructure Investigation Agent".

    Responsibilities:
    - Receive alerts
    - Build a plan using LLMClient (or deterministic logic)
    - Execute plan via PlanExecutionEngine + ToolRegistry + SafeExecutor
    - Store outcomes into MemoryManager (working + episodic)
    """

    def __init__(self) -> None:
        self.tools = ToolRegistry()
        self.executor = SafeExecutor()
        self.memory = MemoryManager()
        self.llm = LLMClient()
        self.engine = PlanExecutionEngine()

    def handle_alert(self, alert: Dict[str, Any]) -> Dict[str, Any]:
        # Working memory: store the current alert
        self.memory.remember_working("current_alert", alert)

        # Episodic memory: fetch some recent context
        recent = self.memory.recent_episodes(limit=3)

        # Build investigation plan
        plan = self.llm.create_investigation_plan(
            alert=alert,
            tools_metadata=self.tools.list_metadata(),
            recent_episodes=recent,
        )

        # Execute the plan
        summary = self.engine.execute(plan=plan, tools=self.tools, executor=self.executor)

        # Serialize outcome for episodic memory (simplified)
        outcome_str = f"success={summary.success}, steps={len(summary.steps)}"
        episode_id = self.memory.record_episode(alert, outcome_str)

        # Snapshot of working memory
        working_snapshot = self.memory.working_snapshot()

        return {
            "alert": alert,
            "plan": summary.plan.model_dump(),
            "steps": [s.model_dump() for s in summary.steps],
            "success": summary.success,
            "episodic_id": episode_id,
            "memory_snapshot": working_snapshot,
            "recent_episodes": recent,
        }
