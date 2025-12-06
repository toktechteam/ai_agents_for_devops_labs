from typing import List


class ResourceAwareModel:
    """
    Simple linear model to simulate a resource-aware AI service.

    prediction = sum(features)
    """

    def __init__(self, name: str = "simple-linear-resource-aware") -> None:
        self.name = name

    def predict(self, features: List[float]) -> float:
        if not features:
            raise ValueError("features cannot be empty")
        return float(sum(features))
