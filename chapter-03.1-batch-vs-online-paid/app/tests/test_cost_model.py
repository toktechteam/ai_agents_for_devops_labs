from cost_model import estimate_batch_cost


def test_cost_estimation():
    cost = estimate_batch_cost(2000, 0.002)
    assert cost == 0.004
