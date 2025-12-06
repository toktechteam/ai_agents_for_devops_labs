from dataclasses import dataclass
from typing import Any, Callable, Dict


@dataclass
class Tool:
    name: str
    fn: Callable[..., Any]
    description: str
    permissions: str = "read-only"
    requires_approval: bool = False
    timeout_seconds: int = 30


class ToolRegistry:
    """
    Tool Registry based on Chapter 4 "Tool Registry Pattern".
    In this lab tools are fake, but structure mirrors real production.
    """

    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}

        # Register builtin fake tools
        self.register(
            Tool(
                name="get_pod_status",
                fn=self.get_pod_status,
                description="Simulate 'kubectl get pods'",
                permissions="read-only",
            )
        )
        self.register(
            Tool(
                name="get_pod_logs",
                fn=self.get_pod_logs,
                description="Simulate 'kubectl logs'",
                permissions="read-only",
            )
        )
        self.register(
            Tool(
                name="get_service_metrics",
                fn=self.get_service_metrics,
                description="Simulate querying metrics backend",
                permissions="read-only",
            )
        )
        self.register(
            Tool(
                name="restart_pod",
                fn=self.restart_pod,
                description="Simulate restarting a pod (requires approval)",
                permissions="write",
                requires_approval=True,
            )
        )

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        return self._tools[name]

    def list_metadata(self) -> Dict[str, Dict[str, Any]]:
        return {
            name: {
                "description": tool.description,
                "permissions": tool.permissions,
                "requires_approval": tool.requires_approval,
                "timeout_seconds": tool.timeout_seconds,
            }
            for name, tool in self._tools.items()
        }

    # --- Fake tool implementations below ---

    def get_pod_status(self, namespace: str, service: str) -> str:
        return f"[FAKE] Pods for service '{service}' in ns '{namespace}': {service}-pod-abc, {service}-pod-def"

    def get_pod_logs(self, namespace: str, pod: str) -> str:
        return f"[FAKE] Last 100 log lines for pod '{pod}' in ns '{namespace}'"

    def get_service_metrics(self, service: str) -> str:
        return f"[FAKE] Metrics for service '{service}': latency_p95=230ms, error_rate=0.4%"

    def restart_pod(self, namespace: str, pod: str) -> str:
        return f"[FAKE] Restart requested for pod '{pod}' in ns '{namespace}'"
