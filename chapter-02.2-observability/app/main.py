import time
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, conlist

from config import get_settings
from model import ObservabilityModel
from otel_setup import configure_otel

tracer, meter = configure_otel()

latency_hist = meter.create_histogram(
    name="inference_latency_ms", description="Latency of inference calls"
)

app = FastAPI(title="Lab 2.2 Paid - Observability API")


class Features(BaseModel):
    features: conlist(float, min_items=1)


@app.get("/health")
def health(settings=Depends(get_settings)):
    return settings.dict()


@app.post("/predict")
def predict(
    payload: Features,
    settings=Depends(get_settings),
):
    model = ObservabilityModel()

    with tracer.start_as_current_span("predict_span") as span:
        start = time.time()
        try:
            result = model.predict(payload.features)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        cpu_ms = settings.cpu_burn_ms
        end = time.time()

        latency_ms = (end - start) * 1000
        latency_hist.record(latency_ms)

        span.set_attribute("latency_ms", latency_ms)
        span.set_attribute("cpu_burn_ms", cpu_ms)

        return {
            "prediction": result,
            "latency_ms": round(latency_ms, 2),
            "cpu_burn_ms": cpu_ms,
        }
