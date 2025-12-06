from typing import Any, Dict, List

from models import Plan, PlanStep, StepExecutionResult, PlanExecutionSummary
from executor import SafeExecutor
from tools import ToolRegistry


class PlanExecutionEngine:
    """
    A simple engine that executes a Plan step-by-step.
    This models the "Plan Execution Engine with Checkpointing" from Chapter 4,
    in a simplified single-process way.
    """

    def __init__(self) -> None:
        # In a real system you'd have checkpoints, retries, etc.
        self.max_steps = 20

    def execute(self, plan: Plan, tools: ToolRegistry, executor: SafeExecutor) -> PlanExecutionSummary:
        step_results: List[StepExecutionResult] = []

        for i, step in enumerate(plan.steps):
            if i >= self.max_steps:
                step_results.append(
                    StepExecutionResult(
                        step=step.step,
                        tool=step.tool,
                        success=False,
                        result=None,
                        error="Max steps exceeded",
                    )
                )
                break

            tool = tools.get(step.tool)
            exec_result = executor.execute(tool, step.params)

            step_results.append(
                StepExecutionResult(
                    step=step.step,
                    tool=step.tool,
                    success=exec_result.get("ok", False),
                    result=exec_result.get("result"),
                    error=exec_result.get("error"),
                )
            )

        success = all(r.success for r in step_results if r.error is None or r.error == "")
        return PlanExecutionSummary(plan=plan, steps=step_results, success=success)
