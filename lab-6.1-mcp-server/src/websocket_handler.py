import json
from fastapi import WebSocket
from src.rpc_engine import process_rpc
from src.audit.db import write_audit_log


async def handle_ws_connection(ws: WebSocket, tool_registry, redis_client, config):
    await ws.accept()

    while True:
        try:
            message = await ws.receive_text()
        except Exception:
            break

        try:
            request = json.loads(message)
        except json.JSONDecodeError:
            error = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"}
            }
            await ws.send_text(json.dumps(error))
            continue

        response = await process_rpc(
            request,
            tool_registry=tool_registry,
            redis_client=redis_client,
            config=config
        )

        # Audit log every request + result
        write_audit_log(request, response)

        await ws.send_text(json.dumps(response))
