from typing import Dict, Any


def get_scenario(name: str) -> Dict[str, Any]:
    """
    Returns a predefined incident scenario.
    """
    scenarios: Dict[str, Dict[str, Any]] = {
        "memory_leak": {
            "name": "memory_leak",
            "description": "Pod memory usage growing steadily and OOMKilled frequently.",
            "alerts": [
                "ALERT KubePodMemoryHigh",
                "ALERT ContainerOOMKilled",
            ],
            "metrics": {
                "memory_rss_mb": [200, 400, 800, 1600],
                "restart_count": [1, 2, 3, 5],
            },
            "logs": [
                "ERROR java.lang.OutOfMemoryError: Java heap space",
                "GC overhead exceeded",
            ],
        },
        "cascading_failure": {
            "name": "cascading_failure",
            "description": "Upstream dependency latency causing 5xx errors downstream.",
            "alerts": [
                "ALERT Http5xxHigh",
                "ALERT ServiceLatencyHigh",
            ],
            "metrics": {
                "upstream_latency_ms": [80, 120, 250, 500],
                "downstream_5xx_rate": [0.02, 0.04, 0.11, 0.23],
            },
            "logs": [
                "ERROR upstream timeout after 2s",
                "WARN circuit breaker opened for upstream-api",
            ],
        },
    }

    if name not in scenarios:
        raise ValueError(f"Unknown scenario: {name}")

    return scenarios[name]
