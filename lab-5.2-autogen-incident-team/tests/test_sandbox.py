import pytest

from src.sandbox.policies import validate_code


def test_sandbox_allows_simple_code():
    code = "print('hello world')"
    # Should not raise
    validate_code(code)


def test_sandbox_blocks_dangerous_import():
    code = "import os\nprint(os.listdir('.'))"
    with pytest.raises(Exception) as exc:
        validate_code(code)

    assert "Sandbox policy violation" in str(exc.value)
