import time
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, conlist

from config import get_settings, Settings
from model import ResourceAwareModel

app = FastAPI(title="Lab 2.1 Paid - Resource-Aware Inference API")


class Features(BaseModel):
    features: conlist(float, min_items=1)


def cpu_burn(milliseconds: int) -> None:
    end = time.time() + (milliseconds / 1000.0)
    x = 0.0
    while time.time() < end:
        x += 1.0  # noqa: F841


def get_model() -> ResourceAwareModel:
    return ResourceAwareModel()


@app.get("/health")
def health(settings: Settings = Depends(get_settings)):
    return {
        "status": "ok",
        "env": settings.app_env,
        "cpu_burn_ms": settings.cpu_burn_ms,
    }


@app.post("/predict")
def predict(
    payload: Features,
    settings: Settings = Depends(get_settings),
    model: ResourceAwareModel = Depends(get_model),
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

    cpu_burn(settings.cpu_burn_ms)

    return {
        "prediction": prediction,
        "model_name": model.name,
        "cpu_burn_ms": settings.cpu_burn_ms,
    }
