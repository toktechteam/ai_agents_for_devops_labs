import json
from src.context_store import get_ctx, set_ctx
from src.rbac import check_rbac
from src.registry import TOOL_REGISTRY_GLOBAL
from src.tools.k8s_tools import list_pods
from src.tools.prom_tools import prom_query_simple
from src.tools.log_tools import log_search
from src.tools.runbook_tools import runbook_preview, runbook_execute


async def process_rpc(request, tool_registry, redis_client, config):
    if "jsonrpc" not in request or request["jsonrpc"] != "2.0":
        return _error(None, -32600, "Invalid Request")

    rpc_id = request.get("id")

    method = request.get("method")
    params = request.get("params", {})

    # ---- MCP Tool Discovery ----
    if method == "mcp.tools.list":
        tools = [{"name": t["name"], "description": t["description"]} for t in tool_registry]
        return {"jsonrpc": "2.0", "id": rpc_id, "result": tools}

    # ---- MCP Context Get ----
    if method == "mcp.context.get":
        key = params.get("key")
        value = get_ctx(redis_client, key)
        return {"jsonrpc": "2.0", "id": rpc_id, "result": value}

    # ---- MCP Context Set ----
    if method == "mcp.context.set":
        key = params.get("key")
        value = params.get("value")
        set_ctx(redis_client, key, value)
        return {"jsonrpc": "2.0", "id": rpc_id, "result": "ok"}

    # ---- MCP Tool Call ----
    if method == "mcp.tools.call":
        tool_name = params.get("name")
        args = params.get("args", {})

        tool_spec = TOOL_REGISTRY_GLOBAL.get(tool_name)
        if not tool_spec:
            return _error(rpc_id, -32601, "Tool not found")

        # RBAC check
        role = tool_spec["rbac_role"]
        check_rbac(role, tool_name)

        # Execute
        try:
            if tool_name == "k8s.list_pods":
                result = list_pods(config, args)
            elif tool_name == "prom.query_simple":
                result = prom_query_simple(config, redis_client, args)
            elif tool_name == "logs.search":
                result = log_search(args)
            elif tool_name == "runbook.preview":
                result = runbook_preview(args)
            elif tool_name == "runbook.execute":
                result = runbook_execute(args)
            else:
                return _error(rpc_id, -32601, "Unknown tool")
        except Exception as e:
            return _error(rpc_id, -32000, str(e))

        return {"jsonrpc": "2.0", "id": rpc_id, "result": result}

    return _error(rpc_id, -32601, "Method not found")


def _error(rpc_id, code, message):
    return {
        "jsonrpc": "2.0",
        "id": rpc_id,
        "error": {"code": code, "message": message}
    }
