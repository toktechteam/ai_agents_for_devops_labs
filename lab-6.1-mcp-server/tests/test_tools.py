from src.tools.runbook_tools import runbook_preview, runbook_execute
from src.tools.log_tools import log_search


def test_runbook_preview():
    result = runbook_preview({"runbook_id": "restart-api"})
    assert "steps" in result
    assert isinstance(result["steps"], list)


def test_runbook_execute_requires_approval():
    try:
        runbook_execute({"runbook_id": "restart-api"})
    except Exception as e:
        assert "approval" in str(e).lower()


def test_log_search_limit():
    # We only check that the function returns a list without errors
    result = log_search({"term": "root", "max_lines": 5})
    assert isinstance(result, list)
