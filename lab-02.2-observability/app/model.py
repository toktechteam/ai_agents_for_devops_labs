from typing import List


class ObservabilityModel:
    def __init__(self, name: str = "obs-linear-model"):
        self.name = name

    def predict(self, features: List[float]) -> float:
        if not features:
            raise ValueError("Empty features")
        return float(sum(features))
