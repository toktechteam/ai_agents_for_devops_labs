# Lab 4.1 PAID Setup Guide – Production Infrastructure Investigation Agent
## Enterprise Agent with Multi-Layer Memory and LLM Planning

---

## 🎯 What You Will Achieve

By completing this setup, you will:

### Learning Objectives

1. **Deploy Production Agent Stack** - Full enterprise architecture
2. **Implement Multi-Layer Memory** - Working + Episodic memory systems
3. **Configure Tool Governance** - Metadata-driven execution
4. **Integrate LLM Planning** - With intelligent fallback
5. **Test Complex Systems** - Validate all components
6. **Understand State Management** - Persistence and recovery

### Expected Outcomes

- ✅ Production-grade agent with full memory stack
- ✅ Tool registry with rich metadata (permissions, timeouts)
- ✅ Safe executor with sandboxing
- ✅ LLM client with deterministic fallback
- ✅ SQLite-based episodic memory (simulating Postgres)
- ✅ In-process working memory (simulating Redis)
- ✅ Plan execution engine with step tracking
- ✅ Comprehensive test coverage
- ✅ Understanding of production agent architecture

### Real-World Skills

**SREs** will learn:
- Building enterprise investigation systems
- Multi-layer memory architecture
- Tool governance patterns

**Platform Engineers** will learn:
- Production agent deployment
- State management strategies
- LLM integration patterns

**ML Engineers** will learn:
- Agent memory systems
- LLM abstraction layers
- Production AI deployment

---

## 📋 Prerequisites

### Required Software

**1. Docker (24+)**
```bash
docker --version
```

**2. kind**
```bash
kind version
```

**3. kubectl (1.29+)**
```bash
kubectl version --client
```

**4. Python (3.11+)**
```bash
python3 --version
```

**5. SQLite (usually pre-installed)**
```bash
sqlite3 --version
```

### Optional for LLM Features

**OpenAI API Key:**
```bash
# Check if set
echo $OPENAI_API_KEY

# Set if needed
export OPENAI_API_KEY="sk-your-key-here"
```

### Required Knowledge

- Completion of Lab 4.1 FREE version
- Understanding of database concepts
- Basic knowledge of caching systems
- Familiarity with LLM APIs

---

## 🏗️ Understanding Production Architecture

### Memory Layer Architecture

```
┌─────────────────────────────────────────────┐
│           InfrastructureAgent                │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │       Memory Manager                   │ │
│  │                                        │ │
│  │  ┌──────────────────────────────────┐ │ │
│  │  │  Working Memory (Fast/Temp)      │ │ │
│  │  │  Simulates: Redis                │ │ │
│  │  │  Storage: In-process dict        │ │ │
│  │  │  TTL: 1 hour                     │ │ │
│  │  │  Use: Current context            │ │ │
│  │  │                                  │ │ │
│  │  │  Examples:                       │ │ │
│  │  │  - Current alert                 │ │ │
│  │  │  - Active investigation          │ │ │
│  │  │  - Recent tool results           │ │ │
│  │  └──────────────────────────────────┘ │ │
│  │                                        │ │
│  │  ┌──────────────────────────────────┐ │ │
│  │  │  Episodic Memory (Permanent)     │ │ │
│  │  │  Simulates: PostgreSQL           │ │ │
│  │  │  Storage: SQLite file            │ │ │
│  │  │  Retention: Forever              │ │ │
│  │  │  Use: Historical analysis        │ │ │
│  │  │                                  │ │ │
│  │  │  Examples:                       │ │ │
│  │  │  - Past investigations           │ │ │
│  │  │  - Patterns detected             │ │ │
│  │  │  - Success/failure history       │ │ │
│  │  └──────────────────────────────────┘ │ │
│  └────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

### Tool Execution Pipeline

```
Alert Received
    ↓
1. Generate Plan (LLM or Fallback)
    ↓
2. For Each Tool in Plan:
    ↓
   ┌──────────────────────────┐
   │  SafeExecutor            │
   │  ┌────────────────────┐  │
   │  │ 1. Check Permissions│  │
   │  │ 2. Verify Rate Limit│  │
   │  │ 3. Set Timeout      │  │
   │  │ 4. Execute Tool     │  │
   │  │ 5. Handle Errors    │  │
   │  │ 6. Record Result    │  │
   │  └────────────────────┘  │
   └──────────────────────────┘
    ↓
3. Aggregate Results
    ↓
4. Store in Both Memory Layers
    ↓
5. Return Report
```

---

## 🚀 Step-by-Step Setup

### Step 1: Navigate to Lab Directory

```bash
cd lab-04.1-first-ai-agent-paid
```

Verify you're in the correct location:
```bash
ls
```

**Expected Output:**
```
Dockerfile  README.md  app/  k8s/  kind-mcp-cluster.yaml  setup.md
```

---

### Step 2: Examine Production Code Structure

**View agent orchestrator:**
```bash
cat app/agent.py | head -80
```

**Key production components:**

**1. Agent initialization with all layers:**
```python
class InfrastructureAgent:
    def __init__(self):
        self.llm_client = LLMClient()
        self.tools = ToolRegistry()
        self.executor = SafeExecutor(self.tools)
        self.memory = MemoryManager()
        self.planner = PlanExecutionEngine()
```

**2. Memory manager:**
```bash
cat app/memory.py | grep "class "
```

**Expected output:**
```python
class WorkingMemory:
class EpisodicMemory:
class MemoryManager:
```

**3. Tool registry with metadata:**
```bash
cat app/tools.py | grep -A10 "metadata"
```

**Understanding metadata:**
- `permissions`: What the tool can access
- `timeout_seconds`: Maximum execution time
- `retry_count`: How many retries on failure
- `rate_limit`: Requests per time period

---

### Step 3: Run Locally Without LLM (Fallback Mode)

**Navigate to app directory:**
```bash
cd app
```

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
Collecting fastapi==0.104.1
Collecting uvicorn[standard]==0.24.0
Collecting pydantic==2.5.0
Collecting sqlalchemy==2.0.23
...
Successfully installed fastapi uvicorn pydantic sqlalchemy ...
```

**Start the agent:**
```bash
uvicorn main:app --reload
```

**Expected Output:**
```
INFO:     Will watch for changes in these directories
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Started server process [12345]
INFO:     InfrastructureAgent initialized
INFO:     WorkingMemory created (simulating Redis)
INFO:     EpisodicMemory connected to episodic.db (simulating Postgres)
INFO:     ToolRegistry loaded 4 tools
INFO:     SafeExecutor initialized
INFO:     LLM client using fallback planner (no API key detected)
INFO:     Application startup complete
```

**What this validates:**
- ✅ All agent components initialized
- ✅ Memory systems created
- ✅ Tools registered
- ✅ Fallback planner active (no LLM needed)

---

### Step 4: Test Agent with First Alert

Open a new terminal (keep agent running).

**Test high memory alert:**
```bash
curl -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type": "high_memory", "service": "web-app"}'
```

**Expected Response:**
```json
{
  "alert": {
    "type": "high_memory",
    "service": "web-app",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "plan": {
    "source": "fallback_planner",
    "reasoning": "High memory alert requires checking pod status, metrics, and events",
    "steps": [
      {
        "step": 1,
        "tool": "check_pods",
        "reason": "Verify pod health and identify high memory pods"
      },
      {
        "step": 2,
        "tool": "get_metrics",
        "reason": "Analyze current memory usage patterns"
      },
      {
        "step": 3,
        "tool": "check_events",
        "reason": "Look for OOMKilled or memory-related events"
      }
    ]
  },
  "execution": {
    "steps": [
      {
        "step": 1,
        "tool": "check_pods",
        "status": "success",
        "result": "Found 5 pods for web-app: 4 healthy, 1 high memory (pod-456)",
        "duration_ms": 45,
        "metadata": {
          "permissions_checked": true,
          "rate_limit_ok": true,
          "timeout": 30
        }
      },
      {
        "step": 2,
        "tool": "get_metrics",
        "status": "success",
        "result": "web-app metrics - CPU: 45%, Memory: 92%, Requests: 200/s",
        "duration_ms": 32
      },
      {
        "step": 3,
        "tool": "check_events",
        "status": "success",
        "result": "Recent events: Warning: OOMKilled pod-456 5 minutes ago",
        "duration_ms": 28
      }
    ],
    "total_duration_ms": 105,
    "success_count": 3,
    "failure_count": 0
  },
  "episodic_id": "550e8400-e29b-41d4-a716-446655440000",
  "memory_snapshot": {
    "working_memory": {
      "current_alert": {
        "type": "high_memory",
        "service": "web-app"
      },
      "investigation_in_progress": false,
      "last_tool": "check_events",
      "tools_used": ["check_pods", "get_metrics", "check_events"]
    },
    "episodic_memory": {
      "total_investigations": 1,
      "investigations_for_service": 1,
      "similar_alerts": 0,
      "success_rate": 1.0
    }
  },
  "recommendations": [
    "Pod pod-456 is experiencing memory pressure",
    "OOMKilled event detected 5 minutes ago",
    "Consider increasing memory limits or investigating memory leaks",
    "Review application memory allocation patterns"
  ]
}
```

**What this validates:**
- ✅ Fallback planner generated appropriate plan
- ✅ All tools executed successfully
- ✅ Metadata tracked for each tool
- ✅ Episodic memory stored investigation
- ✅ Working memory updated
- ✅ Recommendations generated

---

### Step 5: Verify Memory Persistence

**Send second alert:**
```bash
curl -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type": "high_cpu", "service": "web-app"}'
```

**Check memory snapshot in response:**
```json
"episodic_memory": {
  "total_investigations": 2,
  "investigations_for_service": 2,
  "similar_alerts": 1,
  "success_rate": 1.0
}
```

**What this validates:**
- ✅ Investigation count incremented
- ✅ Service-specific investigations tracked
- ✅ Similar past alerts detected
- ✅ Success rate calculated

---

### Step 6: Inspect SQLite Database Directly

**Check database file was created:**
```bash
ls -la episodic.db
```

**Expected Output:**
```
-rw-r--r--  1 user  staff  12288 Jan 15 10:30 episodic.db
```

**Query investigations:**
```bash
sqlite3 episodic.db "SELECT id, alert_type, service, timestamp FROM investigations;"
```

**Expected Output:**
```
550e8400-e29b-41d4-a716-446655440000|high_memory|web-app|2024-01-15 10:30:00
660f9511-f39c-52e5-b827-557766551111|high_cpu|web-app|2024-01-15 10:31:00
```

**View full investigation details:**
```bash
sqlite3 episodic.db "SELECT plan FROM investigations WHERE alert_type='high_memory';"
```

**What this validates:**
- ✅ SQLite database created
- ✅ Investigations persisted
- ✅ Data can be queried
- ✅ Memory survives agent restarts

---

### Step 7: Test Different Alert Types

**CPU alert:**
```bash
curl -s -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type": "high_cpu", "service": "payment-api"}' | jq '.plan.steps[].tool'
```

**Expected Output:**
```
"check_pods"
"get_logs"
"get_metrics"
```

**Crash alert:**
```bash
curl -s -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type": "pod_crash", "service": "auth-service"}' | jq '.plan.steps[].tool'
```

**Expected Output:**
```
"check_pods"
"get_logs"
"check_events"
```

**What this validates:**
- ✅ Different alert types trigger different plans
- ✅ Agent adapts based on alert characteristics
- ✅ Tool selection is contextual

---

### Step 8: Test with LLM (Optional)

**Note:** This step requires OpenAI API key and is optional.

**Set API key:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

**Install OpenAI package:**
```bash
pip install openai
```

**Restart the agent:**
```bash
# Stop uvicorn (Ctrl+C)
uvicorn main:app --reload
```

**Expected startup message:**
```
INFO:     LLM client configured with OpenAI API
INFO:     Will use GPT-4 for planning
INFO:     Fallback planner available if LLM fails
```

**Send alert:**
```bash
curl -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type": "high_memory", "service": "payment-api"}'
```

**Expected: Plan source will be "llm" instead of "fallback_planner":**
```json
{
  "plan": {
    "source": "llm",
    "model": "gpt-4",
    "reasoning": "Given the high memory alert for payment-api, I need to investigate the root cause systematically. First, I'll check the pod status to identify which pods are affected. Then I'll examine the metrics to understand the memory usage pattern. Finally, I'll review events to see if there are any OOMKilled incidents or other memory-related issues.",
    "steps": [...]
  }
}
```

**What this validates:**
- ✅ LLM integration working
- ✅ Natural language reasoning
- ✅ More detailed plan explanations
- ✅ Fallback still available

**Test LLM fallback:**
```bash
# Use invalid API key
export OPENAI_API_KEY="sk-invalid"

# Restart agent
uvicorn main:app --reload

# Send alert - should use fallback
curl -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type": "high_cpu", "service": "test"}'
```

**Expected: Plan source will be "fallback_planner"**

---

### Step 9: Run Comprehensive Unit Tests

**Ensure in app directory:**
```bash
cd lab-04.1-first-ai-agent-paid/app
source .venv/bin/activate
```

**Run all tests:**
```bash
pytest -v
```

**Expected Output:**
```
================== test session starts ==================
platform linux -- Python 3.11.x, pytest-7.4.x
collected 15 items

tests/test_tools.py::test_tool_registry_initialization PASSED    [6%]
tests/test_tools.py::test_tool_metadata_validation PASSED        [13%]
tests/test_tools.py::test_tool_execution_success PASSED          [20%]
tests/test_memory.py::test_working_memory_set_get PASSED         [26%]
tests/test_memory.py::test_working_memory_expiration PASSED      [33%]
tests/test_memory.py::test_episodic_memory_storage PASSED        [40%]
tests/test_memory.py::test_episodic_memory_query PASSED          [46%]
tests/test_memory.py::test_memory_manager_integration PASSED     [53%]
tests/test_planning.py::test_fallback_planner PASSED             [60%]
tests/test_planning.py::test_plan_execution PASSED               [66%]
tests/test_planning.py::test_error_recovery PASSED               [73%]
tests/test_agent.py::test_agent_initialization PASSED            [80%]
tests/test_agent.py::test_full_investigation PASSED              [86%]
tests/test_main.py::test_health_endpoint PASSED                  [93%]
tests/test_main.py::test_alerts_endpoint PASSED                  [100%]

=================== 15 passed in 3.45s ===================
```

**Run specific test suites:**

**Test memory systems:**
```bash
pytest tests/test_memory.py -v
```

**Expected Output:**
```
tests/test_memory.py::test_working_memory_set_get PASSED
tests/test_memory.py::test_working_memory_expiration PASSED
tests/test_memory.py::test_episodic_memory_storage PASSED
tests/test_memory.py::test_episodic_memory_query PASSED
tests/test_memory.py::test_memory_manager_integration PASSED

Test details:
  Working Memory:
    ✓ Set and get values
    ✓ TTL expiration works
    ✓ Simulates Redis behavior

  Episodic Memory:
    ✓ Store investigations
    ✓ Query by service and type
    ✓ Simulates Postgres behavior

  Memory Manager:
    ✓ Coordinates both layers
    ✓ Provides unified interface
```

**Test tool execution:**
```bash
pytest tests/test_tools.py -v
```

**Test planning:**
```bash
pytest tests/test_planning.py -v
```

---

### Step 10: Deploy to Kubernetes

**Navigate to lab root:**
```bash
cd .. # Back to lab-04.1-first-ai-agent-paid/
```

**Create kind cluster:**
```bash
kind create cluster --config kind-mcp-cluster.yaml
```

**Verify cluster:**
```bash
kubectl get nodes
```

**Expected Output:**
```
NAME                      STATUS   ROLES           AGE   VERSION
mcp-cluster-control-plane Ready    control-plane   30s   v1.30.0
```

---

### Step 11: Build and Load Docker Image

**Build the image:**
```bash
docker build -t paid-agent-lab-4-1:v1 .
```

**Expected Output:**
```
[+] Building 42.8s (14/14) FINISHED
 => [internal] load build definition from Dockerfile
 => [1/8] FROM docker.io/library/python:3.11-slim
 => [2/8] WORKDIR /app
 => [3/8] COPY app/requirements.txt .
 => [4/8] RUN pip install --no-cache-dir -r requirements.txt
 => [5/8] COPY app/ .
 => [6/8] RUN useradd -m agentuser && chown -R agentuser:agentuser /app
 => [7/8] USER agentuser
 => exporting to image
 => => naming to docker.io/library/paid-agent-lab-4-1:v1
```

**Verify image:**
```bash
docker images | grep paid-agent-lab-4-1
```

**Expected Output:**
```
paid-agent-lab-4-1   v1      xyz789abc123   2 minutes ago   285MB
```

**Load into kind:**
```bash
kind load docker-image paid-agent-lab-4-1:v1 --name mcp-cluster
```

---

### Step 12: Deploy to Kubernetes

**Create namespace:**
```bash
kubectl apply -f k8s/namespace.yaml
```

**Expected Output:**
```
namespace/ai-ml-lab-4-1-paid created
```

**Deploy agent:**
```bash
kubectl apply -f k8s/deployment.yaml
```

**Expected Output:**
```
deployment.apps/paid-agent-lab-4-1 created
```

**Create service:**
```bash
kubectl apply -f k8s/service.yaml
```

**Expected Output:**
```
service/paid-agent-lab-4-1 created
```

**Wait for pod to be ready:**
```bash
kubectl wait --for=condition=available --timeout=60s deployment/paid-agent-lab-4-1 -n ai-ml-lab-4-1-paid
```

---

### Step 13: Verify Kubernetes Deployment

**Check pods:**
```bash
kubectl get pods -n ai-ml-lab-4-1-paid
```

**Expected Output:**
```
NAME                                 READY   STATUS    RESTARTS   AGE
paid-agent-lab-4-1-xxxxxxxxxx-xxxxx  1/1     Running   0          45s
```

**Check logs:**
```bash
kubectl logs -n ai-ml-lab-4-1-paid -l app=paid-agent --tail=30
```

**Expected Output:**
```
INFO:     Started server process [1]
INFO:     InfrastructureAgent initialized
INFO:     WorkingMemory created (simulating Redis)
INFO:     EpisodicMemory connected to /data/episodic.db
INFO:     ToolRegistry loaded 4 tools with metadata
INFO:     SafeExecutor initialized with permissions system
INFO:     PlanExecutionEngine ready
INFO:     LLM client using fallback planner
INFO:     Application startup complete
```

**Check service:**
```bash
kubectl get svc -n ai-ml-lab-4-1-paid
```

**Expected Output:**
```
NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
paid-agent-lab-4-1   ClusterIP   10.96.123.45    <none>        8000/TCP   50s
```

---

### Step 14: Test Agent in Kubernetes

**Port-forward:**
```bash
kubectl port-forward -n ai-ml-lab-4-1-paid svc/paid-agent-lab-4-1 8000:8000
```

**Test health endpoint:**
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "agent": "InfrastructureAgent",
  "components": {
    "working_memory": "active",
    "episodic_memory": "connected",
    "tool_registry": "4 tools loaded",
    "llm_client": "fallback_mode"
  },
  "memory_stats": {
    "working_memory_size": 0,
    "episodic_investigations": 0
  }
}
```

**Send test alert:**
```bash
curl -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type":"high_cpu","service":"payment-api"}'
```

**Expected:** Full investigation report

**Check agent logs:**
```bash
kubectl logs -n ai-ml-lab-4-1-paid -l app=paid-agent --tail=20
```

**Expected Output:**
```
INFO:     Alert received: high_cpu for payment-api
INFO:     Querying episodic memory for similar cases
INFO:     Found 0 similar investigations
INFO:     Generating plan with fallback planner
INFO:     Plan generated with 3 steps
INFO:     Executing step 1: check_pods
INFO:     Permissions verified for check_pods
INFO:     Tool check_pods executed successfully in 45ms
INFO:     Executing step 2: get_logs
INFO:     Tool get_logs executed successfully in 38ms
INFO:     Executing step 3: get_metrics
INFO:     Tool get_metrics executed successfully in 32ms
INFO:     Investigation complete, storing in episodic memory
INFO:     Episodic ID: 770g0622-g50d-63f6-c938-668877662222
INFO:     Investigation stored successfully
```

---

## ✅ Testing and Validation

### Test 1: Memory Layer Separation

**Working memory test (temporary):**
```bash
# Send alert
curl -s -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type":"high_cpu","service":"test"}' | jq '.memory_snapshot.working_memory'

# Working memory should show current context
```

**Episodic memory test (permanent):**
```bash
# Check pod for database file
kubectl exec -n ai-ml-lab-4-1-paid -l app=paid-agent -- ls -la /data/episodic.db

# Expected: File exists and grows with each investigation
```

### Test 2: Tool Metadata Enforcement

**Check tool execution includes metadata:**
```bash
curl -s -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type":"high_memory","service":"test"}' | jq '.execution.steps[0].metadata'
```

**Expected Output:**
```json
{
  "permissions_checked": true,
  "rate_limit_ok": true,
  "timeout": 30,
  "retry_count": 3
}
```

### Test 3: Plan Execution Tracking

**Verify step-by-step execution:**
```bash
curl -s -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type":"pod_crash","service":"test"}' | jq '.execution.steps[] | {step, tool, status, duration_ms}'
```

**Expected:** Each step has complete execution details

### Test 4: Historical Pattern Detection

**Send multiple alerts for same service:**
```bash
for i in {1..5}; do
  curl -s -X POST http://localhost:8000/alerts \
    -H "Content-Type: application/json" \
    -d '{"type":"high_cpu","service":"recurring-service"}' > /dev/null
  sleep 1
done

# Check if patterns detected
curl -s -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"type":"high_cpu","service":"recurring-service"}' | jq '.memory_snapshot.episodic_memory'
```

**Expected:**
```json
{
  "total_investigations": 6,
  "investigations_for_service": 6,
  "similar_alerts": 5,
  "detected_pattern": "recurring_cpu_issue"
}
```

### Test 5: Error Handling and Fallback

**Test with simulated tool failure:**
```bash
# This test is in the test suite
pytest tests/test_planning.py::test_error_recovery -v
```

**Expected:** Agent handles tool failures gracefully and continues

---

## 🎓 Understanding What You've Built

### Memory Layer Comparison

| Aspect | Working Memory | Episodic Memory |
|--------|---------------|-----------------|
| **Simulates** | Redis | PostgreSQL |
| **Implementation** | In-process dict | SQLite file |
| **Storage** | RAM | Disk |
| **TTL** | 1 hour | Permanent |
| **Use Case** | Current context | Historical analysis |
| **Speed** | Very fast | Fast |
| **Query** | Key-value | SQL queries |
| **Production** | Redis cluster | Postgres DB |

### Tool Execution Pipeline

```
Tool Request
    ↓
SafeExecutor.execute()
    ↓
├─ 1. Check permissions
│  ├─ Read permissions: ["read:pods", "read:logs"]
│  ├─ Write permissions: ["write:pods", "write:config"]
│  └─ Admin permissions: ["admin:*"]
    ↓
├─ 2. Verify rate limits
│  ├─ Track calls per tool
│  ├─ Enforce limits (e.g., 100/minute)
│  └─ Return error if exceeded
    ↓
├─ 3. Set timeout
│  ├─ Tool-specific timeout
│  ├─ Default: 30 seconds
│  └─ Maximum: 60 seconds
    ↓
├─ 4. Execute in sandbox
│  ├─ Isolated execution
│  ├─ Resource limits
│  └─ Error capturing
    ↓
├─ 5. Handle result
│  ├─ Success: Return result
│  ├─ Error: Retry if configured
│  └─ Timeout: Return timeout error
    ↓
├─ 6. Record metrics
│  ├─ Execution time
│  ├─ Success/failure
│  └─ Resource usage
    ↓
Result Returned
```

---

## 💰 Cost Analysis

### Running in KIND: $0/month

Free for development and learning.

### Production Deployment: $15-25/month

**With Real Services:**

```
Agent Pod:
  - 0.5 CPU × 730 hrs × $0.04/hr = $14.60

Redis (managed):
  - Small instance = $10-15/month
  - Or: 0.25 CPU self-hosted = $7.30

PostgreSQL (managed):
  - Small instance = $15-20/month
  - Or: 0.5 CPU self-hosted = $14.60

LLM Calls (optional):
  - 1000 calls/month × $0.01 = $10
  - Or use fallback: $0

Total with managed services: $39.60 + $10 (LLM) = $49.60
Total self-hosted + fallback: $36.50
With spot instances (60% off): $14.60-20

Target: $15-25/month achievable with:
- Self-hosted Redis/Postgres
- Fallback planner (no LLM)
- Spot/preemptible instances
```

---

## 🔧 Troubleshooting

### Issue: Database File Not Persisting

**Check volume mount:**
```bash
kubectl describe pod -n ai-ml-lab-4-1-paid -l app=paid-agent | grep -A5 "Volumes"
```

**Solution: Add persistent volume in deployment.yaml**

### Issue: Working Memory Not Expiring

**Check TTL logic:**
```python
# In app/memory.py
# Verify TTL is set correctly
def get(self, key):
    if time.time() - self.cache[key]["timestamp"] < self.ttl:
        return self.cache[key]["value"]
    return None  # Expired
```

### Issue: Tools Timing Out Frequently

**Check and adjust timeouts:**
```bash
# View current timeouts
grep -r "timeout_seconds" app/tools.py

# Increase if needed
"timeout_seconds": 60  # Increased from 30
```

---

## 🧹 Cleanup

### Remove Kubernetes Resources

```bash
kubectl delete namespace ai-ml-lab-4-1-paid
```

### Delete kind Cluster

```bash
kind delete cluster --name mcp-cluster
```

### Clean Local Files

```bash
cd lab-04.1-first-ai-agent-paid/app
rm -f episodic.db  # SQLite database
rm -rf .venv
rm -rf __pycache__
```

---

## 📊 Success Criteria Checklist

Your lab is complete when:

- [ ] Local agent runs successfully
- [ ] Both memory layers working
- [ ] SQLite database created and persisting
- [ ] Working memory provides current context
- [ ] Tool metadata enforced
- [ ] Safe executor validates permissions
- [ ] Plans execute with step tracking
- [ ] Fallback planner works offline
- [ ] (Optional) LLM integration works
- [ ] All unit tests pass (15/15)
- [ ] Agent deploys to Kubernetes
- [ ] Memory persists in K8s pod
- [ ] Can send alerts and receive reports
- [ ] Historical patterns detected
- [ ] You understand memory layer separation
- [ ] You understand tool governance
- [ ] You understand LLM integration patterns

---

## 📚 Next Steps

### Production Enhancements

**1. Real Database Integration:**
```python
# Redis for working memory
import redis
working_memory = redis.Redis(
    host='redis-service',
    port=6379,
    decode_responses=True
)

# PostgreSQL for episodic memory
from sqlalchemy import create_engine
engine = create_engine(
    "postgresql://user:pass@postgres-service:5432/agent_db"
)
```

**2. Advanced Tool Governance:**
```python
# Approval workflow
class ToolApprovalSystem:
    def requires_approval(self, tool_name):
        return tool_name in ["restart_pod", "delete_resource"]
    
    def request_approval(self, tool_name, context):
        # Send to Slack/PagerDuty
        # Wait for human approval
        pass
```

**3. Memory Optimization:**
```python
# Semantic search in episodic memory
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer('all-MiniLM-L6-v2')
embedding = embedder.encode(alert_description)
similar = vector_search(embedding, k=5)
```

---

## 🎉 Congratulations!

You've built a production-grade AI agent!

### What You've Mastered:

✅ **Multi-Layer Memory** - Working + Episodic architecture  
✅ **Tool Governance** - Metadata-driven execution  
✅ **Safe Execution** - Sandboxing and permissions  
✅ **LLM Integration** - With intelligent fallbacks  
✅ **State Management** - Persistence and recovery  
✅ **Production Patterns** - Enterprise-ready design  

You now have the skills to build and deploy production AI agents!

Happy learning! 🚀🤖🔧💾🧠