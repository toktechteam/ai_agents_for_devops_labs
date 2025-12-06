from agent import InfrastructureAgent


def test_infrastructure_agent_handle_alert():
    agent = InfrastructureAgent()
    alert = {"type": "high_memory", "service": "web-app"}

    result = agent.handle_alert(alert)

    assert result["alert"] == alert
    assert "plan" in result
    assert "steps" in result
    assert isinstance(result["episodic_id"], int)
    assert "memory_snapshot" in result
    assert result["memory_snapshot"]["current_alert"] == alert
