import time
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, conlist

from config import get_settings, Settings
from model import SimpleLinearModel

app = FastAPI(title="AI Lab Paid - Configurable Inference API")


class Features(BaseModel):
    features: conlist(float, min_items=1)


def get_model() -> SimpleLinearModel:
    # In a real-world case, this might load a model from disk or remote storage
    return SimpleLinearModel()


@app.get("/health")
def health(settings: Settings = Depends(get_settings)):
    return {"status": "ok", "env": settings.app_env}


@app.post("/predict")
def predict(
    payload: Features,
    settings: Settings = Depends(get_settings),
    model: SimpleLinearModel = Depends(get_model),
):
    features: List[float] = payload.features

    if len(features) > settings.max_batch_size:
        raise HTTPException(
            status_code=400,
            detail=f"Too many features; max_batch_size={settings.max_batch_size}",
        )

    try:
        prediction = model.predict(features)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    simulated_latency_ms = settings.default_latency_ms
    time.sleep(simulated_latency_ms / 1000.0)

    return {
        "prediction": prediction,
        "model_name": model.name,
        "latency_ms": simulated_latency_ms,
    }
