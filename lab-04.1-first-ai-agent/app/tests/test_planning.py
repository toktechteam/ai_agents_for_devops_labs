from models import Plan, PlanStep
from planning import PlanExecutionEngine
from tools import ToolRegistry
from executor import SafeExecutor


def test_plan_execution_engine_runs_steps():
    plan = Plan(
        goal="Test plan",
        steps=[
            PlanStep(
                step="1",
                action="Check pods",
                tool="get_pod_status",
                params={"namespace": "default", "service": "web-app"},
            )
        ],
    )

    tools = ToolRegistry()
    executor = SafeExecutor()
    engine = PlanExecutionEngine()

    summary = engine.execute(plan, tools, executor)
    assert summary.success is True
    assert len(summary.steps) == 1
    assert summary.steps[0].success is True
    assert "[FAKE]" in str(summary.steps[0].result)
