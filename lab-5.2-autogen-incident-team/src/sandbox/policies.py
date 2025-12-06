DENYLIST = [
    "import os",
    "import sys",
    "open(",
    "subprocess",
    "socket",
    "shutil",
    "eval(",
    "exec(",
    "__import__",
]


def validate_code(code: str):
    """
    Enforces sandbox denylist rules.
    Any forbidden keyword immediately raises an exception.
    """

    for item in DENYLIST:
        if item in code:
            raise Exception(
                f"Sandbox policy violation: '{item}' is not allowed in sandboxed code."
            )
