import docker
import tempfile
import os
import uuid


def run_code_in_docker(code: str, correlation_id: str) -> str:
    """
    Executes Python code inside the sandbox container.
    The sandbox image is defined in docker-compose.
    """

    client = docker.from_env()

    # Temporary file to inject code
    temp_dir = tempfile.mkdtemp()
    script_path = os.path.join(temp_dir, "sandbox_code.py")

    with open(script_path, "w") as f:
        f.write(code)

    try:
        container = client.containers.run(
            image="autogen-sandbox",
            command=f"python sandbox_code.py",
            volumes={temp_dir: {"bind": "/sandbox", "mode": "ro"}},
            working_dir="/sandbox",
            network_disabled=True,
            mem_limit="128m",
            cpuset_cpus="0",
            stderr=True,
            stdout=True,
            detach=True,
            tty=False,
        )

        result = container.logs().decode("utf-8")

    except Exception as e:
        result = f"Sandbox execution error: {str(e)}"

    finally:
        try:
            container.remove(force=True)
        except:
            pass

    return result
