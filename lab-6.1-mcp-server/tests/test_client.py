import asyncio
import websockets
import json


async def main():
    async with websockets.connect("ws://localhost:9000/mcp") as ws:
        await ws.send(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "mcp.tools.list"}))
        print(await ws.recv())

        await ws.send(json.dumps({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "mcp.tools.call",
            "params": {"name": "k8s.list_pods", "args": {"namespace": "default"}}
        }))
        print(await ws.recv())


if __name__ == "__main__":
    asyncio.run(main())
