import subprocess


def safe_exec(cmd: list):
    """
    Executes kubectl in read-only mode.
    """
    allowed_cmds = ["kubectl", "get", "logs", "describe", "-n", "--namespace"]
    if any(c not in allowed_cmds for c in cmd):
        return "Command not allowed (read-only mode)."

    try:
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        return result
    except Exception as e:
        return str(e)


def get_pod_cpu(pod: str, namespace: str = "default"):
    cmd = ["kubectl", "top", "pod", pod, "-n", namespace]
    return safe_exec(cmd)


def get_pod_logs(pod: str, namespace: str = "default"):
    cmd = ["kubectl", "logs", pod, "-n", namespace, "--tail=50"]
    return safe_exec(cmd)
