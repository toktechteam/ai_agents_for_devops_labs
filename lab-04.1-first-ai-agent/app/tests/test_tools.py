from tools import ToolRegistry


def test_tool_registry_metadata_and_get():
    reg = ToolRegistry()
    meta = reg.list_metadata()
    assert "get_pod_status" in meta
    assert "restart_pod" in meta
    t = reg.get("get_pod_status")
    out = t.fn(namespace="default", service="web-app")
    assert "[FAKE]" in out
    assert "web-app" in out
