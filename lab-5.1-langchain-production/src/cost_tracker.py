class CostTracker:
    """
    Simple cost estimator — counts tokens from response and applies fixed rate.
    """

    COST_PER_1K_TOKENS = 0.002  # cheap model rate assumption

    def calculate_cost(self, llm_response):
        usage = getattr(llm_response, "usage", None)

        if usage and hasattr(usage, "total_tokens"):
            tokens = usage.total_tokens
        else:
            tokens = 500  # fallback learning assumption

        cost = (tokens / 1000) * self.COST_PER_1K_TOKENS
        return round(cost, 6)
