from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any

from src.workflow.coordination import run_incident_workflow
from src.workflow.scenarios import get_scenario

app = FastAPI(title="AutoGen Incident Response Team", version="1.0.0")


class IncidentRequest(BaseModel):
    scenario: str
    auto_approve: Optional[bool] = False


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/scenarios")
def list_scenarios() -> Dict[str, Any]:
    available = ["memory_leak", "cascading_failure"]
    return {"available_scenarios": available}


@app.get("/scenarios/{name}")
def get_scenario_details(name: str) -> Dict[str, Any]:
    scenario = get_scenario(name)
    return {"scenario": scenario}


@app.post("/incident/run")
def run_incident(req: IncidentRequest) -> Dict[str, Any]:
    result = run_incident_workflow(
        scenario_name=req.scenario,
        auto_approve=bool(req.auto_approve),
    )
    return result
