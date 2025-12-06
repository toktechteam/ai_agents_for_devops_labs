from typing import Dict


class CostTracker:
    """
    Very small, approximate cost tracker.
    We approximate tokens by len(text) / 4 and charge $0.000001 per token.
    This keeps the whole lab well under the $10 cost ceiling for small tests.
    """

    def __init__(self) -> None:
        self.prompt_tokens = 0
        self.completion_tokens = 0

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        if not text:
            return 0
        return max(1, int(len(text) / 4))

    def add_prompt(self, content: str) -> None:
        self.prompt_tokens += self._estimate_tokens(content)

    def add_completion(self, content: str) -> None:
        self.completion_tokens += self._estimate_tokens(content)

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens

    @property
    def total_cost_usd(self) -> float:
        return self.total_tokens * 0.000001

    def to_dict(self) -> Dict[str, float]:
        return {
            "prompt_tokens": float(self.prompt_tokens),
            "completion_tokens": float(self.completion_tokens),
            "total_tokens": float(self.total_tokens),
            "estimated_cost_usd": float(round(self.total_cost_usd, 6)),
        }
