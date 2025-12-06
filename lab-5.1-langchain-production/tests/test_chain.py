from src.chain import InvestigatorChain


def test_chain_execution():
    chain = InvestigatorChain()

    output = chain.run("High CPU on pod test-pod")

    assert "analysis" in output
    assert "logs" in output
    assert "metrics" in output
    assert "remediation" in output
    assert "cost" in output
    assert isinstance(output["cost"], float)
