import uuid
from src.sandbox.docker_api import run_code_in_docker
from src.sandbox.policies import validate_code


def run_in_sandbox(code: str) -> str:
    """
    Executes user-provided code in a restricted Docker sandbox.
    Full security workflow:
    1. Validate against denylist policy
    2. Assign correlation ID
    3. Execute in sandbox
    4. Return output
    """

    validate_code(code)

    correlation_id = str(uuid.uuid4())

    output = run_code_in_docker(code, correlation_id)

    return output
