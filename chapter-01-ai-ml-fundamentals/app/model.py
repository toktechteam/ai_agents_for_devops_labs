from typing import List


class SimpleLinearModel:
    """
    A tiny "fake" ML model that:

    prediction = sum(features)

    This is intentionally simple but gives DevOps engineers
    something concrete to test and reason about.
    """

    def __init__(self, name: str = "simple-linear-demo") -> None:
        self.name = name

    def predict(self, features: List[float]) -> float:
        if not features:
            raise ValueError("features list cannot be empty")
        return float(sum(features))
