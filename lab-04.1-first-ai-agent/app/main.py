from fastapi import FastAPI
from models import Alert
from agent import InfrastructureAgent

app = FastAPI(
    title="Lab 4.1 Paid - Infrastructure Investigation Agent",
    version="1.0.0",
)

_agent = InfrastructureAgent()


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


@app.post("/alerts")
def receive_alert(alert: Alert):
    result = _agent.handle_alert(alert.model_dump())
    return result
