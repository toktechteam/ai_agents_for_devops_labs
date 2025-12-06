# Lab 6.1 Setup Guide – Production-Ready MCP Server
## Building Agent-Native APIs with WebSocket + JSON-RPC 2.0

---

## 🎯 What You Will Achieve

By completing this setup, you will:

### Learning Objectives

1. **Deploy Complete MCP Stack** - WebSocket + JSON-RPC + Redis + Postgres
2. **Understand Agent Protocols** - Why MCP beats REST for AI agents
3. **Build Tool Registries** - Dynamic discovery and self-describing tools
4. **Test WebSocket Communication** - Real-time agent-server interaction
5. **Validate Multi-Database Architecture** - Redis cache + Postgres audit

### Expected Outcomes

- ✅ Working MCP server with WebSocket endpoint
- ✅ Redis context store operational
- ✅ PostgreSQL audit logging active
- ✅ 7+ tools registered and callable
- ✅ JSON-RPC 2.0 protocol validated
- ✅ Web dashboard for testing
- ✅ Complete audit trail in database
- ✅ Understanding of MCP architecture

### Real-World Skills

**AI Platform Engineers** will learn:
- Deploying agent-native API servers
- WebSocket infrastructure setup
- Tool registry implementation

**DevOps Engineers** will learn:
- Multi-service Kubernetes deployment
- Redis and Postgres integration
- Real-time communication infrastructure

**Backend Engineers** will learn:
- WebSocket server implementation
- JSON-RPC protocol handling
- Multi-database architecture

---

## 📋 Prerequisites

### Required Software

| Tool | Required Version | Purpose |
|------|-----------------|---------|
| **Docker** | 24+ | Container runtime |
| **kind** | v0.20+ | Kubernetes in Docker |
| **kubectl** | 1.29+ | Kubernetes CLI |
| **Python** | 3.10+ | Testing and tools |
| **pip** | latest | Python package manager |

### Verification Commands

**Check Docker:**
```bash
docker --version
```
**Expected:** `Docker version 24.x.x` or higher

**Check kind:**
```bash
kind --version
```
**Expected:** `kind v0.20.0` or higher

**Check kubectl:**
```bash
kubectl version --client
```
**Expected:** `Client Version: v1.29.x` or higher

**Check Python:**
```bash
python3 --version
```
**Expected:** `Python 3.10.x` or higher

### Required Knowledge

- Understanding of WebSocket vs HTTP/REST
- JSON-RPC 2.0 protocol basics
- Kubernetes fundamentals
- Redis and PostgreSQL basics

---

## 🏗️ Understanding MCP Architecture Before Setup

### What You're Building

```
┌────────────────────────────────────────────┐
│  Kubernetes Cluster (kind)                 │
│  Namespace: mcp-lab                        │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │  MCP Server (3 replicas)             │ │
│  │  - WebSocket endpoint                │ │
│  │  - JSON-RPC 2.0 handler              │ │
│  │  - Tool registry                     │ │
│  │  - Port: 9000                        │ │
│  └──────────────────────────────────────┘ │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │  Redis StatefulSet                   │ │
│  │  - Context storage                   │ │
│  │  - Prometheus cache                  │ │
│  │  - Rate limit counters               │ │
│  └──────────────────────────────────────┘ │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │  PostgreSQL StatefulSet              │ │
│  │  - Audit log database                │ │
│  │  - Tool call tracking                │ │
│  │  - Compliance records                │ │
│  └──────────────────────────────────────┘ │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │  Prometheus (optional)               │ │
│  │  - Metrics collection                │ │
│  │  - MCP server monitoring             │ │
│  └──────────────────────────────────────┘ │
└────────────────────────────────────────────┘
```

### Communication Flow

```
Client (Agent/LLM)
    ↓ WebSocket Connection
MCP Server
    ↓ Context Lookup
Redis (ctx.get/set)
    ↓ Tool Execution
Kubernetes API / Prometheus
    ↓ Audit Logging
PostgreSQL (audit_logs table)
```

---

## 🚀 Step-by-Step Setup

### Step 1: Create Kubernetes Cluster

**Create kind cluster:**
```bash
kind create cluster --name mcp-lab
```

**Expected Output:**
```
Creating cluster "mcp-lab" ...
 ✓ Ensuring node image (kindest/node:v1.30.0) 🖼
 ✓ Preparing nodes 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
Set kubectl context to "kind-mcp-lab"
You can now use your cluster with:

kubectl cluster-info --context kind-mcp-lab
```

**Verify cluster:**
```bash
kubectl get nodes
```

**Expected Output:**
```
NAME                    STATUS   ROLES           AGE   VERSION
mcp-lab-control-plane   Ready    control-plane   30s   v1.30.0
```

**What this validates:**
- ✅ kind cluster created successfully
- ✅ Control plane node running
- ✅ kubectl context set correctly

---

### Step 2: Navigate to Lab Directory

**Change directory:**
```bash
cd labs/chapter-06/lab-6.1-mcp-server
```

**Verify you're in correct location:**
```bash
ls
```

**Expected Output:**
```
Dockerfile.api  README.md  docker-compose.yml  infra/  requirements.txt  
scripts/  setup.md  src/  tests/
```

---

### Step 3: Build MCP Server Docker Image

**Build the image:**
```bash
docker build -t mcp-server:latest -f Dockerfile.api .
```

**Expected Output:**
```
[+] Building 45.3s (15/15) FINISHED
 => [1/10] FROM docker.io/library/python:3.11-slim
 => [2/10] WORKDIR /app
 => [3/10] COPY requirements.txt .
 => [4/10] RUN pip install --no-cache-dir -r requirements.txt
 => [5/10] COPY src/ ./src/
 => exporting to image
 => => naming to docker.io/library/mcp-server:latest
```

**Verify image created:**
```bash
docker images | grep mcp-server
```

**Expected:**
```
mcp-server   latest   abc123def456   2 minutes ago   450MB
```

**Load image into kind cluster:**
```bash
kind load docker-image mcp-server:latest --name mcp-lab
```

**Expected Output:**
```
Image: "mcp-server:latest" with ID "sha256:abc123..." loaded into cluster
```

**Verify image in cluster:**
```bash
docker exec -it mcp-lab-control-plane crictl images | grep mcp-server
```

**What this validates:**
- ✅ Docker image built successfully
- ✅ Image loaded into kind cluster
- ✅ Image available for Kubernetes deployment

---

### Step 4: Deploy Namespace

**Create namespace:**
```bash
kubectl apply -f infra/k8s/namespace.yaml
```

**Expected Output:**
```
namespace/mcp-lab created
```

**Verify namespace:**
```bash
kubectl get ns mcp-lab
```

**Expected:**
```
NAME      STATUS   AGE
mcp-lab   Active   5s
```

---

### Step 5: Deploy Redis

**Deploy Redis StatefulSet:**
```bash
kubectl apply -f infra/k8s/redis.yaml
```

**Expected Output:**
```
statefulset.apps/redis-mcp created
service/redis-mcp created
```

**Wait for Redis to be ready:**
```bash
kubectl wait --for=condition=ready pod -l app=redis-mcp -n mcp-lab --timeout=60s
```

**Expected:**
```
pod/redis-mcp-0 condition met
```

**Verify Redis:**
```bash
kubectl get pods -n mcp-lab -l app=redis-mcp
```

**Expected:**
```
NAME          READY   STATUS    RESTARTS   AGE
redis-mcp-0   1/1     Running   0          30s
```

**Test Redis connection:**
```bash
kubectl exec -it redis-mcp-0 -n mcp-lab -- redis-cli ping
```

**Expected:** `PONG`

**What this validates:**
- ✅ Redis StatefulSet deployed
- ✅ Redis pod running
- ✅ Redis accepting connections

---

### Step 6: Deploy PostgreSQL

**Deploy Postgres StatefulSet:**
```bash
kubectl apply -f infra/k8s/postgres.yaml
```

**Expected Output:**
```
statefulset.apps/postgres-mcp created
service/postgres-mcp created
configmap/postgres-init created
```

**Wait for Postgres to be ready:**
```bash
kubectl wait --for=condition=ready pod -l app=postgres-mcp -n mcp-lab --timeout=90s
```

**Verify Postgres:**
```bash
kubectl get pods -n mcp-lab -l app=postgres-mcp
```

**Expected:**
```
NAME             READY   STATUS    RESTARTS   AGE
postgres-mcp-0   1/1     Running   0          45s
```

**Test Postgres connection:**
```bash
kubectl exec -it postgres-mcp-0 -n mcp-lab -- \
  psql -U aiagent -d mcpaudit -c "SELECT 1;"
```

**Expected Output:**
```
 ?column? 
----------
        1
(1 row)
```

**Verify audit_logs table exists:**
```bash
kubectl exec -it postgres-mcp-0 -n mcp-lab -- \
  psql -U aiagent -d mcpaudit -c "\dt"
```

**Expected:**
```
           List of relations
 Schema |    Name     | Type  |  Owner   
--------+-------------+-------+----------
 public | audit_logs  | table | aiagent
(1 row)
```

**What this validates:**
- ✅ PostgreSQL StatefulSet deployed
- ✅ Postgres pod running
- ✅ Database and tables created
- ✅ Postgres accepting connections

---

### Step 7: Deploy Prometheus (Optional)

**Deploy Prometheus:**
```bash
kubectl apply -f infra/k8s/prometheus.yaml
```

**Expected Output:**
```
deployment.apps/prometheus created
service/prometheus created
configmap/prometheus-config created
```

**Verify Prometheus:**
```bash
kubectl get pods -n mcp-lab -l app=prometheus
```

**Expected:**
```
NAME                          READY   STATUS    RESTARTS   AGE
prometheus-xxxxxxxxxx-xxxxx   1/1     Running   0          20s
```

---

### Step 8: Deploy MCP Server

**Deploy MCP server:**
```bash
kubectl apply -f infra/k8s/mcp-deployment.yaml
kubectl apply -f infra/k8s/mcp-service.yaml
```

**Expected Output:**
```
deployment.apps/mcp-server created
service/mcp-server created
```

**Wait for all MCP server pods:**
```bash
kubectl wait --for=condition=available --timeout=120s \
  deployment/mcp-server -n mcp-lab
```

**Expected:**
```
deployment.apps/mcp-server condition met
```

**Verify all pods running:**
```bash
kubectl get pods -n mcp-lab
```

**Expected Output:**
```
NAME                          READY   STATUS    RESTARTS   AGE
mcp-server-xxxxxxxxxx-aaaaa   1/1     Running   0          45s
mcp-server-xxxxxxxxxx-bbbbb   1/1     Running   0          45s
mcp-server-xxxxxxxxxx-ccccc   1/1     Running   0          45s
postgres-mcp-0                1/1     Running   0          2m
prometheus-xxxxxxxxxx-xxxxx   1/1     Running   0          1m
redis-mcp-0                   1/1     Running   0          3m
```

**Check MCP server logs:**
```bash
kubectl logs -n mcp-lab -l app=mcp-server --tail=20
```

**Expected to see:**
```
INFO: MCP Server starting...
INFO: Connected to Redis: redis-mcp:6379
INFO: Connected to Postgres: postgres-mcp:5432/mcpaudit
INFO: Registered 7 tools
INFO: WebSocket endpoint ready: /mcp
INFO: Dashboard available: /dashboard
INFO: Uvicorn running on 0.0.0.0:9000
```

**What this validates:**
- ✅ MCP server deployed with 3 replicas
- ✅ All pods running
- ✅ Redis connection successful
- ✅ Postgres connection successful
- ✅ Tools registered
- ✅ WebSocket ready

---

### Step 9: Port Forward MCP Server

**Forward port 9000:**
```bash
kubectl port-forward svc/mcp-server -n mcp-lab 9000:9000
```

**Expected Output:**
```
Forwarding from 127.0.0.1:9000 -> 9000
Forwarding from [::1]:9000 -> 9000
```

**Keep this terminal open** - it needs to stay running

**In a new terminal, test health endpoint:**
```bash
curl http://localhost:9000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "components": {
    "redis": "connected",
    "postgres": "connected",
    "websocket": "ready"
  },
  "registered_tools": 7
}
```

**What this validates:**
- ✅ Port forwarding working
- ✅ MCP server HTTP endpoints accessible
- ✅ Health check passing
- ✅ All components healthy

---

### Step 10: Install Python Dependencies for Testing

**Create virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Expected Output:**
```
Collecting websockets>=12.0
Collecting pytest>=7.4.0
Collecting requests>=2.31.0
...
Successfully installed websockets-12.0 pytest-7.4.3 requests-2.31.0 ...
```

**Verify installation:**
```bash
python -c "import websockets; print(websockets.__version__)"
```

**Expected:** `12.0` or higher

---

### Step 11: Run Automated Tests

**Run all tests:**
```bash
pytest -v
```

**Expected Output:**
```
==================== test session starts ====================
collected 8 items

tests/test_jsonrpc.py::test_jsonrpc_validation PASSED        [12%]
tests/test_jsonrpc.py::test_error_handling PASSED            [25%]
tests/test_tools.py::test_tool_discovery PASSED              [37%]
tests/test_tools.py::test_context_tools PASSED               [50%]
tests/test_tools.py::test_k8s_tools PASSED                   [62%]
tests/test_tools.py::test_prometheus_tools PASSED            [75%]
tests/test_integration.py::test_full_workflow PASSED         [87%]
tests/test_integration.py::test_audit_logging PASSED         [100%]

==================== 8 passed in 3.45s ====================
```

**What this validates:**
- ✅ JSON-RPC 2.0 protocol working
- ✅ Error handling correct
- ✅ Tool discovery functional
- ✅ Context tools (Redis) working
- ✅ Kubernetes tools operational
- ✅ Prometheus tools functional
- ✅ End-to-end workflow passing
- ✅ Audit logging to Postgres working

---

### Step 12: Test MCP Server via Python WebSocket Client

**Run test client:**
```bash
python tests/test_client.py
```

**Expected Output:**
```
🔌 Connecting to MCP Server...
✓ Connected to ws://localhost:9000/mcp

📋 Test 1: List All Tools
Request: {"jsonrpc": "2.0", "id": 1, "method": "mcp.tools.list"}
Response:
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "mcp.tools.list",
        "description": "List all available tools",
        "parameters": {}
      },
      {
        "name": "ctx.get",
        "description": "Get context value",
        "parameters": {"key": {"type": "string", "required": true}}
      },
      {
        "name": "ctx.set",
        "description": "Set context value",
        "parameters": {
          "key": {"type": "string", "required": true},
          "value": {"type": "any", "required": true}
        }
      },
      {
        "name": "k8s.list_pods",
        "description": "List Kubernetes pods",
        "parameters": {"namespace": {"type": "string", "required": true}}
      },
      {
        "name": "prom.query_simple",
        "description": "Execute Prometheus query",
        "parameters": {"query": {"type": "string", "required": true}}
      },
      {
        "name": "logs.search",
        "description": "Search logs",
        "parameters": {
          "namespace": {"type": "string", "required": true},
          "limit": {"type": "integer", "default": 100}
        }
      },
      {
        "name": "runbook.preview",
        "description": "Preview runbook",
        "parameters": {"runbook_id": {"type": "string", "required": true}}
      }
    ]
  }
}
✓ Test 1 PASSED

🔧 Test 2: List Kubernetes Pods
Request: {
  "jsonrpc": "2.0",
  "id": 2,
  "method": "mcp.tools.call",
  "params": {
    "name": "k8s.list_pods",
    "args": {"namespace": "mcp-lab"}
  }
}
Response:
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "pods": [
      {"name": "mcp-server-xxx", "status": "Running", "ready": "1/1"},
      {"name": "postgres-mcp-0", "status": "Running", "ready": "1/1"},
      {"name": "redis-mcp-0", "status": "Running", "ready": "1/1"}
    ]
  }
}
✓ Test 2 PASSED

📊 Test 3: Query Prometheus
Request: {
  "jsonrpc": "2.0",
  "id": 3,
  "method": "mcp.tools.call",
  "params": {
    "name": "prom.query_simple",
    "args": {"query": "up"}
  }
}
Response:
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "metric": "up",
    "values": [{"labels": {...}, "value": 1}]
  }
}
✓ Test 3 PASSED

All tests completed successfully! ✅
```

**What this validates:**
- ✅ WebSocket connection established
- ✅ JSON-RPC requests processed correctly
- ✅ Tool discovery working
- ✅ Kubernetes tool execution successful
- ✅ Prometheus tool execution successful
- ✅ All 7 tools registered and callable

---

### Step 13: Test via Web Dashboard

**Open web dashboard:**
```bash
open http://localhost:9000/dashboard
```

**Or visit in browser:** `http://localhost:9000/dashboard`

**Test 1: List all tools**

Paste into dashboard:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "mcp.tools.list"
}
```

**Click "Send"**

**Expected:** See list of 7 tools

**Test 2: Set context**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "mcp.tools.call",
  "params": {
    "name": "ctx.set",
    "args": {
      "key": "version",
      "value": "1.0.0"
    }
  }
}
```

**Expected:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "success": true,
    "key": "version",
    "value": "1.0.0"
  }
}
```

**Test 3: Get context**

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "mcp.tools.call",
  "params": {
    "name": "ctx.get",
    "args": {
      "key": "version"
    }
  }
}
```

**Expected:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "key": "version",
    "value": "1.0.0"
  }
}
```

**What this validates:**
- ✅ Web dashboard accessible
- ✅ Tool listing working
- ✅ Context set/get (Redis) working
- ✅ Real-time WebSocket communication

---

### Step 14: Validate Redis Context Store

**Check Redis keys:**
```bash
kubectl exec -it redis-mcp-0 -n mcp-lab -- redis-cli keys '*'
```

**Expected Output:**
```
1) "ctx:version"
2) "rate_limit:mcp.tools.list:default"
3) "cache:prom:up"
```

**Get specific context value:**
```bash
kubectl exec -it redis-mcp-0 -n mcp-lab -- redis-cli get "ctx:version"
```

**Expected:** `"1.0.0"`

**Check TTL:**
```bash
kubectl exec -it redis-mcp-0 -n mcp-lab -- redis-cli ttl "ctx:version"
```

**Expected:** Number of seconds remaining (e.g., `3540` for ~1 hour)

**What this validates:**
- ✅ Redis storing context correctly
- ✅ Keys prefixed properly
- ✅ TTL configured (1 hour)
- ✅ Rate limiting keys present
- ✅ Prometheus cache working

---

### Step 15: Validate PostgreSQL Audit Logs

**Query audit logs:**
```bash
kubectl exec -it postgres-mcp-0 -n mcp-lab -- \
  psql -U aiagent -d mcpaudit -c \
  "SELECT id, method, timestamp FROM audit_logs ORDER BY timestamp DESC LIMIT 10;"
```

**Expected Output:**
```
 id |      method       |        timestamp        
----+-------------------+-------------------------
  5 | mcp.tools.call    | 2024-01-15 10:35:23.456
  4 | mcp.tools.call    | 2024-01-15 10:35:15.234
  3 | mcp.tools.call    | 2024-01-15 10:35:10.123
  2 | mcp.tools.list    | 2024-01-15 10:35:05.678
  1 | mcp.tools.list    | 2024-01-15 10:35:00.123
(5 rows)
```

**View detailed audit entry:**
```bash
kubectl exec -it postgres-mcp-0 -n mcp-lab -- \
  psql -U aiagent -d mcpaudit -c \
  "SELECT * FROM audit_logs WHERE id = 1;"
```

**Expected:** Full record with method, params, result, duration, etc.

**Query by tool name:**
```bash
kubectl exec -it postgres-mcp-0 -n mcp-lab -- \
  psql -U aiagent -d mcpaudit -c \
  "SELECT method, tool_name, COUNT(*) as calls 
   FROM audit_logs 
   GROUP BY method, tool_name;"
```

**Expected:**
```
      method      |   tool_name    | calls 
------------------+----------------+-------
 mcp.tools.list   | NULL           |     2
 mcp.tools.call   | k8s.list_pods  |     1
 mcp.tools.call   | ctx.set        |     1
 mcp.tools.call   | ctx.get        |     1
(4 rows)
```

**What this validates:**
- ✅ PostgreSQL storing audit logs
- ✅ All tool calls logged
- ✅ Timestamps recorded
- ✅ Tool names tracked
- ✅ Query capabilities working

---

## ✅ Testing and Validation

### Test 1: Tool Discovery

**Verify all 7 tools registered:**
```bash
python -c "
import asyncio
import websockets
import json

async def test():
    uri = 'ws://localhost:9000/mcp'
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'mcp.tools.list'
        }))
        response = await ws.recv()
        data = json.loads(response)
        tools = data['result']['tools']
        print(f'Registered tools: {len(tools)}')
        for tool in tools:
            print(f'  - {tool[\"name\"]}')

asyncio.run(test())
"
```

**Expected:**
```
Registered tools: 7
  - mcp.tools.list
  - ctx.get
  - ctx.set
  - k8s.list_pods
  - prom.query_simple
  - logs.search
  - runbook.preview
```

### Test 2: Context Persistence

**Set multiple values:**
```bash
# Set value 1
curl -X POST http://localhost:9000/test/ctx \
  -H "Content-Type: application/json" \
  -d '{"key": "user", "value": "alice"}'

# Set value 2
curl -X POST http://localhost:9000/test/ctx \
  -H "Content-Type: application/json" \
  -d '{"key": "role", "value": "admin"}'
```

**Verify in Redis:**
```bash
kubectl exec -it redis-mcp-0 -n mcp-lab -- redis-cli keys 'ctx:*'
```

**Expected:**
```
1) "ctx:user"
2) "ctx:role"
3) "ctx:version"
```

### Test 3: Audit Trail Completeness

**Generate multiple tool calls:**
```bash
for i in {1..5}; do
  python tests/test_client.py --test k8s
  sleep 1
done
```

**Verify all logged:**
```bash
kubectl exec -it postgres-mcp-0 -n mcp-lab -- \
  psql -U aiagent -d mcpaudit -c \
  "SELECT COUNT(*) FROM audit_logs WHERE tool_name = 'k8s.list_pods';"
```

**Expected:** `5` or more

### Test 4: Error Handling

**Send invalid JSON-RPC:**
```bash
python -c "
import asyncio
import websockets
import json

async def test():
    uri = 'ws://localhost:9000/mcp'
    async with websockets.connect(uri) as ws:
        # Missing 'id' field
        await ws.send(json.dumps({
            'jsonrpc': '2.0',
            'method': 'invalid.tool'
        }))
        response = await ws.recv()
        print(response)

asyncio.run(test())
"
```

**Expected:**
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32600,
    "message": "Invalid Request"
  }
}
```

### Test 5: Rate Limiting

**Send rapid requests:**
```bash
for i in {1..15}; do
  curl -s http://localhost:9000/test/rate-limit > /dev/null
done
```

**Expected:** Some requests should be rate-limited (429 status)

---

## 🎓 Understanding What You've Built

### MCP vs REST API

**Why REST fails for agents:**

```
REST API Problem:
Agent: "What endpoints are available?"
REST: Returns OpenAPI spec (static, complex)
Agent: Must parse complex schema
Agent: Hard-coded integration

MCP Solution:
Agent: {"method": "mcp.tools.list"}
Server: Returns simple tool list with metadata
Agent: Dynamically discovers and calls tools
```

### JSON-RPC 2.0 Benefits

**Request/Response Pattern:**
```json
Request:
{
  "jsonrpc": "2.0",      ← Version
  "id": 1,               ← Request ID (for correlation)
  "method": "tool.name", ← Tool to call
  "params": {...}        ← Tool parameters
}

Response:
{
  "jsonrpc": "2.0",
  "id": 1,               ← Same ID as request
  "result": {...}        ← Tool output
}

Error:
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32600,
    "message": "Invalid Request"
  }
}
```

### Redis Context Store

**Use cases:**
```
1. Agent State:
   - Last query results
   - Conversation context
   - User preferences

2. Caching:
   - Prometheus metrics (5-min TTL)
   - Kubernetes pod lists (1-min TTL)
   - Expensive computations

3. Rate Limiting:
   - Per-tool counters
   - Per-user quotas
   - Time-window tracking
```

---

## 💰 Cost Analysis

### Development: $0/month

Free with kind cluster and Docker.

### Production: $30-50/month

**Infrastructure:**
```
MCP Server (3 replicas): $10
Redis: $10
PostgreSQL: $10
Total: $30/month

With monitoring: ~$40-50/month
```

**No LLM costs** - MCP server is infrastructure, not the agent itself.

---

## 🔧 Troubleshooting

### Issue: MCP Server Pod Not Starting

**Check logs:**
```bash
kubectl logs -n mcp-lab -l app=mcp-server --tail=50
```

**Common causes:**
- Redis connection failed
- Postgres connection failed
- Missing environment variables

**Solution:**
```bash
# Verify Redis
kubectl get pods -n mcp-lab -l app=redis-mcp

# Verify Postgres
kubectl get pods -n mcp-lab -l app=postgres-mcp

# Check service endpoints
kubectl get svc -n mcp-lab
```

### Issue: WebSocket Connection Refused

**Check port forward:**
```bash
# Kill existing port-forward
pkill -f "port-forward.*mcp-server"

# Start fresh
kubectl port-forward svc/mcp-server -n mcp-lab 9000:9000
```

### Issue: Redis Keys Not Persisting

**Check Redis:**
```bash
kubectl exec -it redis-mcp-0 -n mcp-lab -- redis-cli ping
```

**View Redis logs:**
```bash
kubectl logs redis-mcp-0 -n mcp-lab
```

### Issue: Audit Logs Not Appearing

**Check Postgres connection:**
```bash
kubectl exec -it postgres-mcp-0 -n mcp-lab -- \
  psql -U aiagent -d mcpaudit -c "SELECT 1;"
```

**Verify table exists:**
```bash
kubectl exec -it postgres-mcp-0 -n mcp-lab -- \
  psql -U aiagent -d mcpaudit -c "\dt"
```

---

## 🧹 Cleanup

### Automated Cleanup

```bash
bash scripts/cleanup.sh
```

### Manual Cleanup

**Delete namespace (removes all resources):**
```bash
kubectl delete namespace mcp-lab
```

**Delete kind cluster:**
```bash
kind delete cluster --name mcp-lab
```

**Clean Docker images:**
```bash
docker rmi mcp-server:latest
docker system prune -f
```

---

## 📊 Success Criteria Checklist

Your lab is complete when:

- [ ] kind cluster created and running
- [ ] MCP server image built and loaded
- [ ] All pods running (MCP server, Redis, Postgres)
- [ ] Port forwarding working
- [ ] Health endpoint returning healthy
- [ ] All 8 tests passing
- [ ] WebSocket client connecting successfully
- [ ] 7 tools registered and discoverable
- [ ] Context set/get working (Redis)
- [ ] Audit logs appearing (Postgres)
- [ ] Web dashboard accessible
- [ ] You understand MCP vs REST differences
- [ ] You understand JSON-RPC 2.0 protocol
- [ ] You understand tool registry concept

---

## 🎉 Congratulations!

You've deployed a production-ready MCP server!

### What You've Accomplished:

✅ **WebSocket Server** - Real-time agent communication  
✅ **JSON-RPC 2.0** - Standard protocol implementation  
✅ **Tool Registry** - Dynamic discovery system  
✅ **Redis Integration** - Context and caching  
✅ **PostgreSQL Audit** - Compliance logging  
✅ **Kubernetes Deployment** - Production-ready  

You now understand agent-native API protocols!

Happy learning! 🚀🔌📡🤖