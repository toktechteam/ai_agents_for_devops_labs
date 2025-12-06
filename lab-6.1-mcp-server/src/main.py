import os
import yaml
from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse, HTMLResponse
from src.websocket_handler import handle_ws_connection
from src.registry import load_tool_registry
from src.context_store import init_redis
from src.audit.db import init_db

app = FastAPI()

CONFIG_PATH = os.getenv("APP_CONFIG_PATH", "/app/configs/app_config.yaml")

with open(CONFIG_PATH, "r") as f:
    APP_CONFIG = yaml.safe_load(f)

TOOL_REGISTRY = load_tool_registry("/app/configs/tools.yaml")
REDIS_CLIENT = init_redis(APP_CONFIG["redis"])
init_db(APP_CONFIG["database"])


@app.get("/health")
async def health():
    return JSONResponse({"status": "ok", "app": APP_CONFIG["app"]["name"]})


@app.get("/")
async def root():
    return JSONResponse({"message": "MCP Server running", "websocket": "/mcp", "dashboard": "/dashboard"})


@app.get("/dashboard")
async def dashboard():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MCP Server Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            #log { border: 1px solid #ccc; padding: 10px; height: 300px; overflow-y: scroll; background: #f9f9f9; }
            input, select, button, textarea { margin: 5px 0; width: 100%; }
            .row { margin-bottom: 15px; }
        </style>
    </head>
    <body>
        <h1>MCP Server Dashboard</h1>
        <p>Use this dashboard to send JSON-RPC requests over WebSocket to the MCP server.</p>

        <div class="row">
            <label>Request JSON:</label>
            <textarea id="request" rows="8">
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "mcp.tools.list"
}
            </textarea>
            <button onclick="sendRequest()">Send Request</button>
        </div>

        <h3>Quick Actions</h3>
        <div class="row">
            <button onclick="setListTools()">mcp.tools.list</button>
            <button onclick="setListPods()">k8s.list_pods (default namespace)</button>
            <button onclick="setPromQuery()">prom.query_simple (up)</button>
        </div>

        <h3>Responses</h3>
        <div id="log"></div>

        <script>
            let ws = null;

            function log(msg) {
                const logDiv = document.getElementById('log');
                const line = document.createElement('div');
                line.textContent = msg;
                logDiv.appendChild(line);
                logDiv.scrollTop = logDiv.scrollHeight;
            }

            function connect() {
                const proto = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
                const url = proto + window.location.host + '/mcp';
                ws = new WebSocket(url);

                ws.onopen = () => log('WebSocket connected: ' + url);
                ws.onmessage = (event) => log('← ' + event.data);
                ws.onclose = () => log('WebSocket closed');
                ws.onerror = (err) => log('WebSocket error: ' + err);
            }

            function sendRequest() {
                if (!ws || ws.readyState !== WebSocket.OPEN) {
                    log('WebSocket not connected.');
                    return;
                }
                const text = document.getElementById('request').value;
                try {
                    JSON.parse(text);
                } catch (e) {
                    log('Invalid JSON: ' + e);
                    return;
                }
                log('→ ' + text);
                ws.send(text);
            }

            function setListTools() {
                document.getElementById('request').value = JSON.stringify({
                    jsonrpc: "2.0",
                    id: 1,
                    method: "mcp.tools.list"
                }, null, 2);
            }

            function setListPods() {
                document.getElementById('request').value = JSON.stringify({
                    jsonrpc: "2.0",
                    id: 2,
                    method: "mcp.tools.call",
                    params: {
                        name: "k8s.list_pods",
                        args: { namespace: "default" }
                    }
                }, null, 2);
            }

            function setPromQuery() {
                document.getElementById('request').value = JSON.stringify({
                    jsonrpc: "2.0",
                    id: 3,
                    method: "mcp.tools.call",
                    params: {
                        name: "prom.query_simple",
                        args: { query: "up" }
                    }
                }, null, 2);
            }

            window.onload = connect;
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html)


@app.websocket("/mcp")
async def websocket_endpoint(ws: WebSocket):
    await handle_ws_connection(ws, TOOL_REGISTRY, REDIS_CLIENT, APP_CONFIG)
