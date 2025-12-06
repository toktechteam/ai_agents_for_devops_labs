from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Alert(BaseModel):
    type: str
    service: str


class PlanStep(BaseModel):
    step: str
    action: str
    tool: str
    params: Dict[str, Any]


class Plan(BaseModel):
    goal: str
    steps: List[PlanStep]


class StepExecutionResult(BaseModel):
    step: str
    tool: str
    success: bool
    result: Any
    error: Optional[str] = None


class PlanExecutionSummary(BaseModel):
    plan: Plan
    steps: List[StepExecutionResult]
    success: bool
