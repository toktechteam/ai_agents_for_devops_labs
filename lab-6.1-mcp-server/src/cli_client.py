import asyncio
import json
import argparse
import websockets


async def send_rpc(request, ws_url: str):
    async with websockets.connect(ws_url) as ws:
        await ws.send(json.dumps(request))
        resp = await ws.recv()
        print(resp)


def main():
    parser = argparse.ArgumentParser(description="MCP Client CLI")
    parser.add_argument(
        "--ws-url",
        default="ws://localhost:9000/mcp",
        help="WebSocket URL of the MCP server (default: ws://localhost:9000/mcp)",
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list-tools", help="Call mcp.tools.list")

    pods_parser = subparsers.add_parser("list-pods", help="Call k8s.list_pods")
    pods_parser.add_argument("--namespace", default="default", help="Kubernetes namespace")

    prom_parser = subparsers.add_parser("prom-query", help="Call prom.query_simple")
    prom_parser.add_argument("query", help="PromQL query string (e.g. up)")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    if args.command == "list-tools":
        req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "mcp.tools.list",
        }
    elif args.command == "list-pods":
        req = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "mcp.tools.call",
            "params": {
                "name": "k8s.list_pods",
                "args": {"namespace": args.namespace},
            },
        }
    elif args.command == "prom-query":
        req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "mcp.tools.call",
            "params": {
                "name": "prom.query_simple",
                "args": {"query": args.query},
            },
        }
    else:
        parser.print_help()
        return

    asyncio.run(send_rpc(req, args.ws_url))


if __name__ == "__main__":
    main()
