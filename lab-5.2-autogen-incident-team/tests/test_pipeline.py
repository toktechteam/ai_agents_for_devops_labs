import pytest

from src.workflow.pipeline import IncidentPipeline


def test_pipeline_list_scenarios():
    pipeline = IncidentPipeline(default_scenarios=["memory_leak", "cascading_failure"])
    scenarios = pipeline.list_scenarios()
    assert "memory_leak" in scenarios
    assert "cascading_failure" in scenarios


def test_pipeline_invalid_scenario_raises():
    pipeline = IncidentPipeline(default_scenarios=["memory_leak"])

    with pytest.raises(ValueError):
        pipeline.run("unknown_scenario", auto_approve=False)
