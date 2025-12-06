import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

from src.chain import InvestigatorChain
from src.db import get_db_session
from src.models import AuditLog

app = FastAPI(title="LangChain Investigator API")

# Prometheus metrics
REQUEST_COUNT = Counter("request_count", "Total API requests")
INVESTIGATION_LATENCY = Histogram(
    "investigation_latency_seconds", "Time spent processing investigations"
)

class AlertRequest(BaseModel):
    alert: str


@app.get("/")
def root():
    return {"message": "LangChain Investigator API running"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/investigate")
def investigate(req: AlertRequest):
    REQUEST_COUNT.inc()
    start = time.time()

    try:
        chain = InvestigatorChain()
        result = chain.run(req.alert)
        duration = time.time() - start
        INVESTIGATION_LATENCY.observe(duration)

        # store in DB
        session = get_db_session()
        audit = AuditLog(
            alert=req.alert,
            result=result.get("analysis", ""),
            logs=result.get("logs", ""),
            metrics=result.get("metrics", ""),
            remediation=result.get("remediation", ""),
            cost=result.get("cost", 0.0),
        )
        session.add(audit)
        session.commit()

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
