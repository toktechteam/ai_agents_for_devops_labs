import pytest
from src.rpc_engine import process_rpc
from src.registry import load_tool_registry
from src.context_store import init_redis


@pytest.mark.asyncio
async def test_tool_list():
    registry = load_tool_registry("configs/tools.yaml")
    redis_client = init_redis({"host": "localhost", "port": 6379, "db": 0})
    config = {}

    request = {"jsonrpc": "2.0", "id": 1, "method": "mcp.tools.list"}
    resp = await process_rpc(request, registry, redis_client, config)

    assert resp["id"] == 1
    assert "result" in resp
    assert isinstance(resp["result"], list)


@pytest.mark.asyncio
async def test_invalid_method():
    registry = load_tool_registry("configs/tools.yaml")
    redis_client = init_redis({"host": "localhost", "port": 6379, "db": 0})

    request = {"jsonrpc": "2.0", "id": 99, "method": "unknown.method"}
    resp = await process_rpc(request, registry, redis_client, {})

    assert resp["error"]["code"] == -32601
