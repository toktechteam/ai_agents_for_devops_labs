from typing import Any, Dict

from tools import Tool


class SafeExecutor:
    """
    A minimal "Tool Execution Sandbox" as per Chapter 4.

    - Validates permissions (simplified)
    - Simulates approval for dangerous tools
    - Captures errors and wraps them into a stable response
    """

    def __init__(self) -> None:
        # In a real system this would be RBAC, rate limiting, etc.
        self.auto_approve_write = False  # require approval in real setup

    def execute(self, tool: Tool, params: Dict[str, Any]) -> Dict[str, Any]:
        # Check permissions / approval
        if tool.requires_approval and not self.auto_approve_write:
            return {
                "ok": False,
                "error": f"Tool '{tool.name}' requires approval",
            }

        try:
            result = tool.fn(**params)
            return {
                "ok": True,
                "result": result,
            }
        except TypeError as e:
            return {
                "ok": False,
                "error": f"Parameter error: {e}",
            }
        except Exception as e:  # pragma: no cover - generic
            return {
                "ok": False,
                "error": f"Execution error: {e}",
            }
