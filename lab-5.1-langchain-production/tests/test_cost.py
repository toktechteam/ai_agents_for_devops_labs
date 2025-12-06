from src.cost_tracker import CostTracker


class DummyResponse:
    class Usage:
        total_tokens = 1200

    usage = Usage()
    content = "test"


def test_cost_tracker():
    tracker = CostTracker()

    cost = tracker.calculate_cost(DummyResponse())

    # 1200 tokens → 1.2 * 0.002 = 0.0024
    assert round(cost, 4) == 0.0024
