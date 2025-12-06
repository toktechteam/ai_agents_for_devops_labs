from cost_estimator import estimate_cost


def test_estimate_cost_under_ten():
    cost = estimate_cost(node_hourly=0.01, nodes=1, hours=20)
    assert cost == 0.2
    assert cost < 10.0
