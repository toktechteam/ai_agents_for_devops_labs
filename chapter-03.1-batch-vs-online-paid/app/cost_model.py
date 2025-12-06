def estimate_batch_cost(total_predictions: int, cost_per_1k: float) -> float:
    """
    Returns estimated USD cost for batch inference.
    Example:
      2000 predictions at $0.002 per 1000 = 0.004 USD
    """
    units = total_predictions / 1000
    return round(units * cost_per_1k, 6)
