# Lab 6.1 – Production-Ready MCP Server
## Building Agent-Native APIs with WebSocket + JSON-RPC 2.0

---

## 🎯 What You Will Learn

### Core Concepts

By completing this lab, you will master:

1. **Model Context Protocol (MCP)** - Next-generation agent APIs:
   - **Why REST APIs fail** for agents: Polling, discovery limitations, state management
   - **WebSocket transport**: Real-time bidirectional communication
   - **JSON-RPC 2.0**: Standard protocol for agent-server communication
   - **Dynamic tool discovery**: Self-describing APIs agents can explore
   - **Tool execution**: Safe, audited function calls from AI

2. **MCP Server Architecture** - Production components:
   - **Tool registry**: Dynamic tool registration and discovery
   - **Context management**: Redis-backed state storage
   - **Audit logging**: PostgreSQL compliance tracking
   - **RBAC enforcement**: Role-based tool access control
   - **Rate limiting**: Preventing abuse and runaway costs
   - **Caching layer**: Redis for frequently-accessed data

3. **Safe Tool Design** - Security-first agent tools:
   - **Read-only Kubernetes tools**: Safe cluster inspection
   - **Prometheus queries**: Cached metric access
   - **Log search**: Strict limits and filtering
   - **Runbook execution**: Approval-gated automation
   - **Input validation**: Preventing injection attacks
   - **Sandbox execution**: Isolated tool runtime

4. **Production Deployment** - Enterprise patterns:
   - **Kubernetes-native**: Deployed as K8s workload
   - **Multi-database**: Redis for cache, Postgres for audit
   - **Observability**: Prometheus metrics integration
   - **High availability**: Multi-replica deployment
   - **Resource management**: CPU/memory limits

### Practical Skills

You will be able to:

- ✅ Build WebSocket servers for AI agents
- ✅ Implement JSON-RPC 2.0 protocol handlers
- ✅ Create self-describing tool registries
- ✅ Design safe, audited agent tools
- ✅ Implement context management with Redis
- ✅ Add audit logging with PostgreSQL
- ✅ Deploy MCP servers on Kubernetes
- ✅ Enforce RBAC for agent operations
- ✅ Test agent-server communication

### Real-World Applications

**AI Platform Teams** will learn:
- Building agent-native APIs
- Tool discovery mechanisms
- Safe agent tool design
- Production MCP deployment

**SRE Teams** will learn:
- Enabling AI-powered automation
- Safe read-only operations for agents
- Audit trails for agent actions
- Agent observability patterns

**Security Teams** will learn:
- RBAC for AI agents
- Audit logging for compliance
- Sandboxed tool execution
- Input validation for agents

**Platform Engineers** will learn:
- WebSocket infrastructure
- Multi-database architecture
- Agent protocol implementation
- Production agent tooling

---

## 📋 Prerequisites

### Required Software
- **Docker:** Version 24+ with Docker Compose
- **kind:** Kubernetes in Docker
- **kubectl:** Version 1.29 or higher
- **Python:** Version 3.11 or higher
- **WebSocket client:** For testing (wscat or Python)

### Required Knowledge
- Understanding of REST API limitations for agents
- WebSocket and real-time communication concepts
- JSON-RPC protocol basics
- Kubernetes fundamentals
- Redis and PostgreSQL basics

### Verification Commands

```bash
# Check Docker and kind
docker --version
kind version

# Check kubectl
kubectl version --client

# Check Python
python3 --version

# Install wscat for testing (optional)
npm install -g wscat
```

---

## 🏗️ Architecture Overview

### Why MCP Instead of REST?

**REST API Limitations for Agents:**

```
Problem 1: No Dynamic Discovery
❌ Agent: "What can I do?"
   REST: Returns generic docs or 404

Problem 2: Polling for State
❌ Agent polls every 5 seconds for updates
   → Network overhead, latency, costs

Problem 3: Complex State Management
❌ Agent must track context across requests
   → Stateless HTTP breaks agent workflows

Problem 4: No Tool Metadata
❌ Agent can't know tool parameters dynamically
   → Hard-coded integrations, brittle
```

**MCP Solutions:**

```
✓ Tool Discovery: mcp.tools.list
  Agent queries available tools dynamically

✓ Persistent Connection: WebSocket
  Real-time updates, no polling

✓ Context Management: Built-in state
  Server maintains agent context

✓ Self-Describing Tools: Rich metadata
  Parameters, types, descriptions included
```

### What You're Building

```
┌─────────────────────────────────────────────────────────────────┐
│                    Production MCP Server                         │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  MCP Client (AI Agent / LLM Application)                   │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  LangChain Agent / AutoGen / Custom Agent           │  │ │
│  │  │  - Discovers available tools                         │  │ │
│  │  │  - Calls tools via JSON-RPC 2.0                     │  │ │
│  │  │  - Maintains context across calls                   │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────┬───────────────────────────────────┘ │
│                           │                                      │
│                           │ WebSocket                            │
│                           │ JSON-RPC 2.0                         │
│                           │                                      │
│                           ▼                                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  MCP Server (FastAPI + WebSocket Layer)                   │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  WebSocket Handler                                   │  │ │
│  │  │  - Accepts persistent connections                    │  │ │
│  │  │  - Maintains session state                           │  │ │
│  │  │  - Routes JSON-RPC requests                          │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │                                                              │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  JSON-RPC 2.0 Engine                                 │  │ │
│  │  │  - Parses JSON-RPC requests                          │  │ │
│  │  │  - Validates method and params                       │  │ │
│  │  │  - Routes to tool handlers                           │  │ │
│  │  │  - Formats JSON-RPC responses                        │  │ │
│  │  │  - Error handling and codes                          │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │                                                              │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  Tool Registry                                       │  │ │
│  │  │  ┌────────────────────────────────────────────────┐  │  │ │
│  │  │  │  Registered Tools:                             │  │  │ │
│  │  │  │                                                │  │  │ │
│  │  │  │  mcp.tools.list                                │  │  │ │
│  │  │  │  → Returns all available tools with metadata  │  │  │ │
│  │  │  │                                                │  │  │ │
│  │  │  │  ctx.get / ctx.set                             │  │  │ │
│  │  │  │  → Context management (Redis-backed)          │  │  │ │
│  │  │  │                                                │  │  │ │
│  │  │  │  k8s.list_pods                                 │  │  │ │
│  │  │  │  → Read-only Kubernetes queries               │  │  │ │
│  │  │  │                                                │  │  │ │
│  │  │  │  prom.query_simple                             │  │  │ │
│  │  │  │  → Prometheus metric queries (cached)         │  │  │ │
│  │  │  │                                                │  │  │ │
│  │  │  │  logs.search                                   │  │  │ │
│  │  │  │  → Log search with strict limits              │  │  │ │
│  │  │  │                                                │  │  │ │
│  │  │  │  runbook.preview                               │  │  │ │
│  │  │  │  → View runbook without execution             │  │  │ │
│  │  │  │                                                │  │  │ │
│  │  │  │  runbook.execute                               │  │  │ │
│  │  │  │  → Execute with approval + RBAC               │  │  │ │
│  │  │  └────────────────────────────────────────────────┘  │  │ │
│  │  │                                                        │  │ │
│  │  │  Each tool includes:                                  │  │ │
│  │  │  - Name and description                               │  │ │
│  │  │  - Parameters with types                              │  │ │
│  │  │  - Required permissions                               │  │ │
│  │  │  - Rate limits                                        │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │                                                              │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  RBAC Enforcement                                    │  │ │
│  │  │  - Validates caller permissions                      │  │ │
│  │  │  - Checks tool access rights                         │  │ │
│  │  │  - Enforces approval workflows                       │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │                                                              │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  Rate Limiter                                        │  │ │
│  │  │  - Per-tool rate limits                              │  │ │
│  │  │  - Per-user quotas                                   │  │ │
│  │  │  - Prevents runaway costs                            │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Storage Layer                                             │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  Redis (Context Store + Cache)                       │  │ │
│  │  │  - Agent context: Last queries, state                │  │ │
│  │  │  - Prometheus cache: Frequent metrics                │  │ │
│  │  │  - Rate limit counters                               │  │ │
│  │  │  - Session management                                │  │ │
│  │  │  TTL: 1 hour default                                 │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │                                                              │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  PostgreSQL (Audit Log)                              │  │ │
│  │  │  Schema: audit_logs table                            │  │ │
│  │  │  - Tool calls with parameters                        │  │ │
│  │  │  - Who called (agent/user)                           │  │ │
│  │  │  - What tool                                         │  │ │
│  │  │  - When (timestamp)                                  │  │ │
│  │  │  - Result (success/failure)                          │  │ │
│  │  │  - Duration                                          │  │ │
│  │  │  Retention: 90 days                                  │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  External Integrations                                     │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  Kubernetes API                                      │  │ │
│  │  │  - Read-only access                                  │  │ │
│  │  │  - Pod listing and status                            │  │ │
│  │  │  - No modifications allowed                          │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │                                                              │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  Prometheus API                                      │  │ │
│  │  │  - PromQL query execution                            │  │ │
│  │  │  - Metric retrieval                                  │  │ │
│  │  │  - Cached in Redis                                   │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### JSON-RPC 2.0 Communication Flow

```
Client Request:
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "mcp.tools.list"
}
    ↓
WebSocket Transport
    ↓
┌──────────────────────────────────┐
│  MCP Server Receives             │
│  - Parse JSON-RPC envelope       │
│  - Extract method                │
│  - Validate request structure    │
└─────────────┬────────────────────┘
              │
              ▼
┌──────────────────────────────────┐
│  Route to Tool Handler           │
│  - Look up "mcp.tools.list"      │
│  - Check permissions             │
│  - Check rate limits             │
└─────────────┬────────────────────┘
              │
              ▼
┌──────────────────────────────────┐
│  Execute Tool                    │
│  - Query tool registry           │
│  - Format tool metadata          │
│  - Return tool list              │
└─────────────┬────────────────────┘
              │
              ▼
┌──────────────────────────────────┐
│  Log to PostgreSQL               │
│  - Record tool call              │
│  - Store parameters              │
│  - Log result                    │
└─────────────┬────────────────────┘
              │
              ▼
Server Response:
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "k8s.list_pods",
        "description": "List pods in namespace",
        "parameters": {
          "namespace": {
            "type": "string",
            "required": true
          }
        }
      },
      ...
    ]
  }
}
    ↓
WebSocket Transport
    ↓
Client Receives and Processes
```

---

## 🔧 MCP Tools Reference

### Core Protocol Tools

**mcp.tools.list**
- **Description:** List all available tools with metadata
- **Parameters:** None
- **Returns:** Array of tool definitions
- **Permissions:** Public (no auth required)
- **Rate Limit:** 10 calls/minute

**Example:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "mcp.tools.list"
}

Response:
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "k8s.list_pods",
        "description": "List pods in a Kubernetes namespace",
        "parameters": {
          "namespace": {
            "type": "string",
            "required": true,
            "description": "Kubernetes namespace"
          }
        },
        "permissions": ["k8s:read"],
        "rate_limit": "20/minute"
      }
    ]
  }
}
```

### Context Management Tools

**ctx.get**
- **Description:** Retrieve context value by key
- **Parameters:**
  - `key` (string, required): Context key
- **Returns:** Context value
- **Storage:** Redis with 1-hour TTL

**ctx.set**
- **Description:** Store context value
- **Parameters:**
  - `key` (string, required): Context key
  - `value` (any, required): Value to store
- **Returns:** Success confirmation

### Kubernetes Tools

**k8s.list_pods**
- **Description:** List pods in namespace (read-only)
- **Parameters:**
  - `namespace` (string, required): Kubernetes namespace
  - `label_selector` (string, optional): Label filter
- **Returns:** Array of pod objects
- **Permissions:** `k8s:read`
- **Safety:** Read-only, no modifications

**Example:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "mcp.tools.call",
  "params": {
    "name": "k8s.list_pods",
    "args": {
      "namespace": "default"
    }
  }
}

Response:
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "pods": [
      {
        "name": "nginx-xyz",
        "status": "Running",
        "ready": "1/1",
        "restarts": 0
      }
    ]
  }
}
```

### Prometheus Tools

**prom.query_simple**
- **Description:** Execute PromQL query
- **Parameters:**
  - `query` (string, required): PromQL expression
  - `time` (string, optional): Query timestamp
- **Returns:** Query results
- **Caching:** Redis, 5-minute TTL
- **Permissions:** `prometheus:query`

**Example:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "mcp.tools.call",
  "params": {
    "name": "prom.query_simple",
    "args": {
      "query": "up{job='kubernetes-nodes'}"
    }
  }
}
```

### Log Search Tools

**logs.search**
- **Description:** Search logs with filters
- **Parameters:**
  - `namespace` (string, required): Namespace to search
  - `pod_pattern` (string, optional): Pod name pattern
  - `since` (string, optional): Time range (e.g., "1h")
  - `limit` (int, optional): Max results (default 100, max 1000)
- **Returns:** Log entries
- **Permissions:** `logs:read`
- **Safety:** Strict limits, filtered output

### Runbook Tools

**runbook.preview**
- **Description:** View runbook without executing
- **Parameters:**
  - `runbook_id` (string, required): Runbook identifier
- **Returns:** Runbook steps and metadata
- **Permissions:** `runbooks:read`

**runbook.execute**
- **Description:** Execute approved runbook
- **Parameters:**
  - `runbook_id` (string, required): Runbook identifier
  - `approval_token` (string, required): Human approval
- **Returns:** Execution results
- **Permissions:** `runbooks:execute`
- **Safety:** Requires approval, full audit logging

---

## 📁 Repository Structure

```
lab-06.1-mcp-server/
├── README.md                   ← This file
├── setup.md                    ← Detailed setup guide
├── docker-compose.yml          ← Local development stack
├── Dockerfile                  ← MCP server image
├── requirements.txt            ← Python dependencies
├── .env.example                ← Environment template
├── src/
│   ├── main.py                 ← FastAPI + WebSocket app
│   ├── mcp/
│   │   ├── server.py           ← MCP server implementation
│   │   ├── jsonrpc.py          ← JSON-RPC 2.0 handler
│   │   ├── registry.py         ← Tool registry
│   │   └── context.py          ← Context management
│   ├── tools/
│   │   ├── base.py             ← Tool base class
│   │   ├── kubernetes.py       ← K8s tools
│   │   ├── prometheus.py       ← Prom tools
│   │   ├── logs.py             ← Log search
│   │   └── runbooks.py         ← Runbook tools
│   ├── rbac/
│   │   ├── permissions.py      ← Permission definitions
│   │   └── enforcer.py         ← RBAC enforcement
│   ├── storage/
│   │   ├── redis_client.py     ← Redis connection
│   │   └── postgres_client.py  ← Postgres audit log
│   └── utils/
│       ├── config.py           ← Configuration
│       └── rate_limit.py       ← Rate limiting
├── infra/
│   └── k8s/
│       ├── namespace.yaml      ← Namespace
│       ├── redis.yaml          ← Redis StatefulSet
│       ├── postgres.yaml       ← Postgres StatefulSet
│       ├── mcp-deployment.yaml ← MCP server deployment
│       └── mcp-service.yaml    ← MCP service
├── tests/
│   ├── test_jsonrpc.py         ← JSON-RPC tests
│   ├── test_tools.py           ← Tool tests
│   ├── test_rbac.py            ← RBAC tests
│   └── test_integration.py     ← End-to-end tests
└── scripts/
    ├── test_client.py          ← WebSocket test client
    └── cleanup.sh              ← Cleanup script
```

---

## 🚀 Quick Start Guide

### Option 1: Docker Compose (Local Development)

**Step 1: Start stack**
```bash
docker compose up --build -d
```

**Step 2: Test WebSocket connection**
```bash
# Using Python test client
python scripts/test_client.py

# Or using wscat
wscat -c ws://localhost:8000/mcp
```

**Step 3: List available tools**
```json
{"jsonrpc": "2.0", "id": 1, "method": "mcp.tools.list"}
```

---

### Option 2: Kubernetes (Production)

**Step 1: Create cluster**
```bash
kind create cluster --name mcp-lab
```

**Step 2: Deploy stack**
```bash
kubectl apply -f infra/k8s/
```

**Step 3: Port-forward**
```bash
kubectl port-forward svc/mcp-server -n mcp-lab 8000:8000
```

**Step 4: Test**
```bash
python scripts/test_client.py --host localhost --port 8000
```

---

## 💰 Cost Analysis

### Development: $0/month

Free with local kind cluster and Docker Compose.

### Production: $30-50/month

**Infrastructure:**
```
MCP Server (3 replicas): $10
Redis: $10
PostgreSQL: $10
Total: $30/month
```

**No LLM costs** - MCP server is just the API layer, agents make the LLM calls.

---

## 🎓 Key Learning Outcomes

### Conceptual Understanding

After completing this lab, you understand:

✅ **MCP Protocol:**
- Why REST APIs are inadequate for agents
- WebSocket persistent connections
- JSON-RPC 2.0 request/response
- Dynamic tool discovery

✅ **Agent Tool Design:**
- Self-describing tools
- Safe, read-only operations
- Approval workflows
- Audit logging

✅ **Production Patterns:**
- Multi-database architecture
- RBAC enforcement
- Rate limiting
- Context management

### Technical Skills

You can now:

✅ **Build WebSocket servers** for real-time agent communication
✅ **Implement JSON-RPC 2.0** protocol handlers
✅ **Create tool registries** with dynamic discovery
✅ **Design safe agent tools** with proper validation
✅ **Deploy MCP servers** on Kubernetes
✅ **Implement audit logging** for compliance

---

## 🔧 Troubleshooting

### WebSocket Connection Failed

**Check server is running:**
```bash
curl http://localhost:8000/health
```

### Redis Connection Error

**Test Redis:**
```bash
docker exec -it redis redis-cli ping
```

### Postgres Audit Logging Failed

**Check Postgres:**
```bash
docker exec -it postgres psql -U mcp -d auditdb -c "SELECT 1;"
```

---

## 🧹 Cleanup

**Docker Compose:**
```bash
docker compose down -v
```

**Kubernetes:**
```bash
kubectl delete namespace mcp-lab
kind delete cluster --name mcp-lab
```

---

## 🎉 Congratulations!

You've built a production-ready MCP server!

### What You've Mastered:

✅ **MCP Protocol** - Agent-native APIs  
✅ **WebSocket + JSON-RPC** - Real-time communication  
✅ **Tool Discovery** - Self-describing interfaces  
✅ **Safe Execution** - Read-only, audited tools  
✅ **Production Deployment** - Kubernetes-ready  

You now understand the foundation of agent protocols!

Happy learning! 🚀🔌🤖📡