# Lab 5.1 PAID Setup Guide – Production LangChain Agent with Full Observability
## Enterprise LangChain with Redis, Postgres, Prometheus, and Grafana

---

## 🎯 What You Will Achieve

By completing this setup, you will:

### Learning Objectives

1. **Deploy Production LangChain Stack** - Full enterprise architecture
2. **Implement Multi-Database Architecture** - Redis + Postgres integration
3. **Configure Full Observability** - Prometheus + Grafana monitoring
4. **Secure Tool Execution** - Read-only kubectl sandbox
5. **Enable Audit Logging** - Database-backed investigation tracking
6. **Test at Scale** - Load testing and performance validation

### Expected Outcomes

- ✅ Production LangChain agent with real LLM integration
- ✅ Redis for conversation memory and caching
- ✅ Postgres for audit logs and decision history
- ✅ Prometheus metrics collection
- ✅ Grafana dashboards for visualization
- ✅ Secure tool execution with sandboxing
- ✅ Comprehensive audit trail
- ✅ Load testing validation
- ✅ Full Kubernetes deployment

### Real-World Skills

**ML Platform Engineers** will learn:
- Deploying production LangChain systems
- Multi-database architecture for ML agents
- Full-stack observability implementation

**SREs** will learn:
- Running LangChain in production
- Monitoring ML workloads
- Database integration patterns
- Secure tool execution

**DevOps Engineers** will learn:
- Container orchestration for ML
- Observability stack deployment
- Multi-service coordination

---

## 📋 Prerequisites

### Required Software

**1. Docker (24+) with Compose**
```bash
docker --version
docker compose version
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

**5. curl**
```bash
curl --version
```

### Optional Tools

**For load testing:**
```bash
# Install bombardier (optional)
go install github.com/codesenberg/bombardier@latest
```

### Required API Keys

**OpenAI API Key (required for LLM):**
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

### Required Knowledge

- Completion of Lab 5.1 FREE version
- Understanding of LangChain framework
- Docker Compose basics
- Kubernetes fundamentals
- Prometheus and Grafana basics

---

## 🏗️ Understanding Production Architecture

### Full Stack Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    Production Stack                              │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  FastAPI Application (Port 8000)                           │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  LangChain Agent                                     │  │ │
│  │  │  - Real OpenAI LLM                                   │  │ │
│  │  │  - Chain execution                                   │  │ │
│  │  │  - Tool orchestration                                │  │ │
│  │  │  - Memory management                                 │  │ │
│  │  └────────────────┬─────────────────────────────────────┘  │ │
│  │                   │                                          │ │
│  │         ┌─────────┴─────────┬────────────┬─────────────┐   │ │
│  │         │                   │            │             │   │ │
│  │         ▼                   ▼            ▼             ▼   │ │
│  │  ┌───────────┐      ┌──────────┐  ┌─────────┐  ┌─────────┐ │
│  │  │  Redis    │      │ Postgres │  │ kubectl │  │ Metrics │ │
│  │  │  (Cache)  │      │ (Audit)  │  │ (Tools) │  │ Export  │ │
│  │  └───────────┘      └──────────┘  └─────────┘  └─────────┘ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Redis (Port 6379)                                         │ │
│  │  - Conversation memory                                     │ │
│  │  - LangChain memory backend                                │ │
│  │  - Fast cache for frequent queries                         │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  PostgreSQL (Port 5432)                                    │ │
│  │  Database: auditdb                                         │ │
│  │  Table: audit_logs                                         │ │
│  │  - Investigation history                                   │ │
│  │  - Decision tracking                                       │ │
│  │  - Cost audit trail                                        │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Prometheus (Port 9090)                                    │ │
│  │  - Scrapes /metrics endpoint                               │ │
│  │  - Stores time-series data                                 │ │
│  │  - Provides query API                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Grafana (Port 3000)                                       │ │
│  │  - Visualizes metrics                                      │ │
│  │  - Custom dashboards                                       │ │
│  │  - Alerting rules                                          │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Investigation Flow with Full Stack

```
1. Investigation Request
   ↓
2. LangChain Agent (FastAPI)
   ↓
3. Check Redis Cache
   Cache hit? → Return cached result
   Cache miss? → Continue
   ↓
4. LLM Planning (OpenAI GPT-4)
   Generate investigation plan
   ↓
5. Tool Execution (Sandboxed kubectl)
   Execute tools with read-only access
   ↓
6. Store in Redis
   Cache result for future queries
   ↓
7. Log to Postgres
   Audit trail with full details
   ↓
8. Export Metrics
   Update Prometheus counters
   ↓
9. Return Response
   Complete investigation report
```

---

## 🚀 Step-by-Step Setup

### Part 1: Local Development with Docker Compose

### Step 1: Navigate to Lab Directory

```bash
cd lab-05.1-langchain-production-paid
```

Verify you're in the correct location:
```bash
ls
```

**Expected Output:**
```
docker-compose.yml  Dockerfile  README.md  app/  configs/  infra/  scripts/  setup.md
```

---

### Step 2: Configure Environment Variables

**Create .env file:**
```bash
cat > .env << 'EOF'
# OpenAI Configuration
OPENAI_API_KEY=sk-your-actual-key-here

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379

# Postgres Configuration
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=auditdb
POSTGRES_USER=aiagent
POSTGRES_PASSWORD=secure_password_change_in_production

# Application Configuration
API_PORT=8000
LOG_LEVEL=INFO
ENVIRONMENT=development
EOF
```

**Important:** Replace `sk-your-actual-key-here` with your real OpenAI API key.

**Verify environment:**
```bash
cat .env
```

---

### Step 3: Build Docker Images

**Build all services:**
```bash
docker compose build
```

**Expected Output:**
```
[+] Building 65.3s (18/18) FINISHED
 => [langchain-api internal] load build definition
 => [langchain-api 1/12] FROM docker.io/library/python:3.11-slim
 => [langchain-api 2/12] WORKDIR /app
 => [langchain-api 3/12] RUN apt-get update && apt-get install -y kubectl
 => [langchain-api 4/12] COPY requirements.txt .
 => [langchain-api 5/12] RUN pip install --no-cache-dir -r requirements.txt
 => [langchain-api 6/12] COPY src/ ./src/
 => [langchain-api 7/12] COPY configs/ ./configs/
 => exporting to image
 => => naming to docker.io/library/langchain-api:latest
```

**Verify images created:**
```bash
docker images | grep langchain
```

**Expected Output:**
```
langchain-api          latest    abc123def456   2 minutes ago   850MB
```

---

### Step 4: Start All Services

**Start the stack:**
```bash
docker compose up -d
```

**Expected Output:**
```
[+] Running 5/5
 ✔ Network langchain-production-paid_default    Created
 ✔ Container redis                              Started
 ✔ Container postgres                           Started
 ✔ Container langchain-api                      Started
 ✔ Container prometheus                         Started
 ✔ Container grafana                            Started
```

**Verify all containers running:**
```bash
docker compose ps
```

**Expected Output:**
```
NAME                STATUS              PORTS
langchain-api       Up 30 seconds       0.0.0.0:8000->8000/tcp
redis               Up 32 seconds       0.0.0.0:6379->6379/tcp
postgres            Up 32 seconds       0.0.0.0:5432->5432/tcp
prometheus          Up 30 seconds       0.0.0.0:9090->9090/tcp
grafana             Up 30 seconds       0.0.0.0:3000->3000/tcp
```

**What this validates:**
- ✅ All 5 services started
- ✅ Ports exposed correctly
- ✅ Network created
- ✅ Health checks passing

---

### Step 5: Verify API is Running

**Check API health:**
```bash
curl http://localhost:8000/
```

**Expected Response:**
```json
{
  "message": "LangChain Investigator API running",
  "version": "1.0.0",
  "status": "healthy",
  "components": {
    "langchain": "initialized",
    "redis": "connected",
    "postgres": "connected",
    "openai": "configured"
  }
}
```

**Check detailed health:**
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "redis": {
    "status": "connected",
    "ping": "PONG"
  },
  "postgres": {
    "status": "connected",
    "tables": ["audit_logs"]
  },
  "openai": {
    "status": "configured",
    "model": "gpt-4"
  },
  "uptime_seconds": 45
}
```

---

### Step 6: Initialize Database Tables

**Access API container:**
```bash
docker exec -it langchain-api bash
```

**Inside container, start Python:**
```bash
python
```

**Create database tables:**
```python
from src.models import Base
from src.db import engine

# Create all tables
Base.metadata.create_all(engine)

print("✓ Database tables created successfully")

# Verify tables exist
from src.db import get_db
db = next(get_db())
result = db.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
tables = [row[0] for row in result]
print(f"✓ Tables in database: {tables}")

# Exit Python
exit()
```

**Expected Output:**
```
✓ Database tables created successfully
✓ Tables in database: ['audit_logs']
```

**Exit container:**
```bash
exit
```

---

### Step 7: Test First Investigation

**Send investigation request:**
```bash
curl -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{
    "alert": "High CPU usage detected on pod payment-api-xyz",
    "service": "payment-api",
    "severity": "warning"
  }'
```

**Expected Response (formatted):**
```json
{
  "investigation_id": "inv_abc123xyz",
  "timestamp": "2024-01-15T10:30:00Z",
  "alert": {
    "alert": "High CPU usage detected on pod payment-api-xyz",
    "service": "payment-api",
    "severity": "warning"
  },
  "langchain_response": {
    "analysis": "The payment-api service is experiencing high CPU usage. Based on the alert, I will investigate the root cause by checking pod status, reviewing recent logs, and analyzing metrics.",
    "investigation_steps": [
      {
        "step": 1,
        "action": "check_pod_status",
        "result": "Pod payment-api-xyz is running with CPU at 95%. Container restart count: 0. Recent events: None."
      },
      {
        "step": 2,
        "action": "analyze_logs",
        "result": "Recent logs show increased request rate (500 req/s vs normal 200 req/s). No error patterns detected."
      },
      {
        "step": 3,
        "action": "review_metrics",
        "result": "CPU usage correlates with request spike. Memory usage normal at 60%."
      }
    ],
    "root_cause": "Traffic spike causing high CPU utilization",
    "recommendations": [
      "Scale horizontally to 5 replicas to handle increased load",
      "Implement rate limiting if traffic pattern is abnormal",
      "Review application profiling for CPU optimization opportunities",
      "Set up auto-scaling based on CPU metrics"
    ],
    "confidence": 0.92
  },
  "cost": {
    "tokens_used": 487,
    "input_tokens": 156,
    "output_tokens": 331,
    "cost_usd": 0.00974,
    "model": "gpt-4"
  },
  "execution_time_ms": 3450,
  "cached": false,
  "audit_log_id": 1
}
```

**What this validates:**
- ✅ LangChain agent working
- ✅ OpenAI API connected
- ✅ Real LLM reasoning
- ✅ Multi-step investigation
- ✅ Cost tracking active
- ✅ Audit log created

---

### Step 8: Verify Redis Caching

**Send same request again:**
```bash
curl -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{
    "alert": "High CPU usage detected on pod payment-api-xyz",
    "service": "payment-api",
    "severity": "warning"
  }'
```

**Expected in response:**
```json
{
  "cached": true,
  "execution_time_ms": 12,
  "cost": {
    "tokens_used": 0,
    "cost_usd": 0.00000,
    "note": "Result served from cache"
  }
}
```

**Verify in Redis:**
```bash
docker exec -it redis redis-cli

# Inside redis-cli
KEYS *
GET investigation:*

exit
```

**Expected:** Cache key exists with investigation data

---

### Step 9: Check Audit Logs in Postgres

**Query audit logs:**
```bash
docker exec -it postgres psql -U aiagent -d auditdb
```

**Inside psql:**
```sql
-- View all audit logs
SELECT id, timestamp, alert, service, cost_usd 
FROM audit_logs 
ORDER BY timestamp DESC 
LIMIT 5;

-- View detailed log
SELECT * FROM audit_logs WHERE id = 1;

-- View cost summary
SELECT 
  service,
  COUNT(*) as investigations,
  SUM(cost_usd) as total_cost,
  AVG(cost_usd) as avg_cost
FROM audit_logs
GROUP BY service;

-- Exit
\q
```

**Expected Output:**
```
 id |        timestamp        |              alert               |   service   | cost_usd 
----+-------------------------+----------------------------------+-------------+----------
  1 | 2024-01-15 10:30:00.123 | High CPU usage detected on po... | payment-api |  0.00974
(1 row)
```

---

### Step 10: View Prometheus Metrics

**Access metrics endpoint:**
```bash
curl http://localhost:8000/metrics
```

**Expected Output:**
```
# HELP langchain_requests_total Total investigation requests
# TYPE langchain_requests_total counter
langchain_requests_total 2

# HELP langchain_cached_requests_total Cached investigation requests
# TYPE langchain_cached_requests_total counter
langchain_cached_requests_total 1

# HELP langchain_tokens_total Total LLM tokens consumed
# TYPE langchain_tokens_total counter
langchain_tokens_total 487

# HELP langchain_cost_total Total cost in USD
# TYPE langchain_cost_total counter
langchain_cost_total 0.00974

# HELP langchain_latency_seconds Investigation latency
# TYPE langchain_latency_seconds histogram
langchain_latency_seconds_bucket{le="1.0"} 0
langchain_latency_seconds_bucket{le="5.0"} 2
langchain_latency_seconds_bucket{le="+Inf"} 2
langchain_latency_seconds_sum 3.462
langchain_latency_seconds_count 2

# HELP langchain_cache_hit_ratio Cache hit ratio
# TYPE langchain_cache_hit_ratio gauge
langchain_cache_hit_ratio 0.5
```

**Open Prometheus UI:**
```bash
# Open in browser
open http://localhost:9090
```

**Query examples:**
- `rate(langchain_requests_total[5m])` - Request rate
- `langchain_cost_total` - Total cost
- `langchain_cache_hit_ratio` - Cache effectiveness

---

### Step 11: Configure Grafana Dashboards

**Access Grafana:**
```bash
# Open in browser
open http://localhost:3000
```

**Login:**
```
Username: admin
Password: admin
```

**First login will prompt to change password - skip or set new password**

**Add Prometheus data source:**

1. Go to Configuration → Data Sources
2. Click "Add data source"
3. Select "Prometheus"
4. Set URL: `http://prometheus:9090`
5. Click "Save & Test"

**Expected:** "Data source is working"

**Import dashboard:**

1. Go to Dashboards → Import
2. Click "Upload JSON file"
3. Select `configs/grafana-dash.json` from host:
   ```bash
   # From your terminal, copy the dashboard config
   docker cp configs/grafana-dash.json grafana:/tmp/
   ```
4. Or paste JSON content directly
5. Select Prometheus data source
6. Click "Import"

**Expected dashboard panels:**
- Investigation Requests (rate)
- Total Cost (cumulative)
- Cache Hit Ratio
- Average Latency
- Token Usage
- Investigations by Service

---

### Step 12: Run Automated Tests

**Execute test script:**
```bash
bash scripts/test.sh
```

**Expected Output:**
```
🚀 LangChain Production Test Suite
===================================

📡 Test 1: Health Check
   ✓ API is healthy
   ✓ Redis connected
   ✓ Postgres connected
   ✓ OpenAI configured

📡 Test 2: Investigation Request
   ✓ Investigation completed
   ✓ LangChain response received
   ✓ Cost tracked: $0.00974
   ✓ Audit log created: ID 2

📡 Test 3: Cache Verification
   ✓ Second request served from cache
   ✓ Execution time: 12ms (99.7% faster)
   ✓ Cost: $0.00 (cached)

📡 Test 4: Metrics Check
   ✓ Prometheus metrics exposed
   ✓ Request counter: 3
   ✓ Cache hit ratio: 0.33

📊 Test Summary
   Total Tests: 4
   Passed: 4
   Failed: 0
   Duration: 8.5s

✅ All tests passed successfully!
```

---

### Part 2: Kubernetes Deployment

### Step 13: Create KIND Cluster

**Create cluster:**
```bash
kind create cluster --name langchain-lab
```

**Expected Output:**
```
Creating cluster "langchain-lab" ...
 ✓ Ensuring node image (kindest/node:v1.30.0) 🖼
 ✓ Preparing nodes 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
Set kubectl context to "kind-langchain-lab"
```

**Verify cluster:**
```bash
kubectl get nodes
```

**Expected:**
```
NAME                         STATUS   ROLES           AGE   VERSION
langchain-lab-control-plane  Ready    control-plane   30s   v1.30.0
```

---

### Step 14: Load Docker Image into KIND

**Load API image:**
```bash
kind load docker-image langchain-api:latest --name langchain-lab
```

**Expected:**
```
Image: "langchain-api:latest" with ID "sha256:abc123..." loaded into cluster
```

**Verify image in cluster:**
```bash
docker exec -it langchain-lab-control-plane crictl images | grep langchain-api
```

---

### Step 15: Deploy All Kubernetes Resources

**Apply all manifests:**
```bash
kubectl apply -f infra/k8s/
```

**Expected Output:**
```
namespace/ai-lab created
configmap/app-config created
secret/api-secrets created
deployment.apps/langchain-api created
deployment.apps/redis created
deployment.apps/postgres created
deployment.apps/prometheus created
deployment.apps/grafana created
service/langchain-api created
service/redis created
service/postgres created
service/prometheus created
service/grafana created
persistentvolumeclaim/postgres-pvc created
```

**Verify namespace:**
```bash
kubectl get ns
```

**Expected:**
```
NAME              STATUS   AGE
ai-lab            Active   15s
default           Active   2m
kube-system       Active   2m
kube-public       Active   2m
kube-node-lease   Active   2m
```

---

### Step 16: Verify All Pods Running

**Check pod status:**
```bash
kubectl get pods -n ai-lab
```

**Expected Output:**
```
NAME                             READY   STATUS    RESTARTS   AGE
langchain-api-xxxxxxxxxx-xxxxx   1/1     Running   0          45s
redis-xxxxxxxxxx-xxxxx           1/1     Running   0          45s
postgres-xxxxxxxxxx-xxxxx        1/1     Running   0          45s
prometheus-xxxxxxxxxx-xxxxx      1/1     Running   0          45s
grafana-xxxxxxxxxx-xxxxx         1/1     Running   0          45s
```

**Wait for all pods to be ready:**
```bash
kubectl wait --for=condition=ready pod --all -n ai-lab --timeout=120s
```

**Check logs of API pod:**
```bash
kubectl logs -n ai-lab -l app=langchain-api --tail=20
```

**Expected:**
```
INFO:     Started server process [1]
INFO:     LangChain agent initialized
INFO:     Connected to Redis: redis:6379
INFO:     Connected to Postgres: postgres:5432/auditdb
INFO:     OpenAI client configured with model: gpt-4
INFO:     Metrics exporter ready
INFO:     Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

### Step 17: Test API in Kubernetes

**Port-forward API service:**
```bash
kubectl port-forward svc/langchain-api -n ai-lab 8000:80
```

**In another terminal, test API:**
```bash
curl http://localhost:8000/
```

**Expected:**
```json
{
  "message": "LangChain Investigator API running",
  "environment": "kubernetes",
  "namespace": "ai-lab"
}
```

**Send investigation:**
```bash
curl -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{
    "alert": "Pod crash detected in production namespace",
    "service": "user-service",
    "severity": "critical"
  }'
```

**Expected:** Full investigation response with LangChain analysis

---

### Step 18: Access Prometheus in Kubernetes

**Port-forward Prometheus:**
```bash
kubectl port-forward svc/prometheus -n ai-lab 9090:9090
```

**Open Prometheus:**
```bash
open http://localhost:9090
```

**Verify targets:**
- Go to Status → Targets
- Should see `langchain-api` endpoint

**Run queries:**
- `langchain_requests_total`
- `rate(langchain_requests_total[5m])`
- `langchain_cost_total`

---

### Step 19: Access Grafana in Kubernetes

**Port-forward Grafana:**
```bash
kubectl port-forward svc/grafana -n ai-lab 3000:3000
```

**Access Grafana:**
```bash
open http://localhost:3000
```

**Login:** admin / admin

**Add Prometheus data source:**
- URL: `http://prometheus:9090`
- Save & Test

**Import dashboard:**
- Upload `configs/grafana-dash.json`

**Expected:** Dashboards showing live metrics from Kubernetes deployment

---

### Step 20: Load Testing (Optional)

**Simple load test:**
```bash
for i in {1..20}; do
  curl -s -X POST http://localhost:8000/investigate \
    -H "Content-Type: application/json" \
    -d "{\"alert\":\"Test alert $i\",\"service\":\"test-svc\"}" > /dev/null &
done
wait

echo "✓ Load test complete"
```

**Check Prometheus:**
```bash
curl http://localhost:8000/metrics | grep langchain_requests_total
```

**Expected:**
```
langchain_requests_total 20
```

**Advanced load test with bombardier (if installed):**
```bash
bombardier -c 10 -n 100 \
  -m POST \
  -H "Content-Type: application/json" \
  -b '{"alert":"Load test","service":"test"}' \
  http://localhost:8000/investigate
```

**Watch metrics in Grafana in real-time**

---

## ✅ Testing and Validation

### Test 1: Redis Caching Effectiveness

**Measure cache performance:**
```bash
# First request (cache miss)
time curl -s -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{"alert":"Cache test","service":"test"}' > /dev/null

# Second request (cache hit)
time curl -s -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{"alert":"Cache test","service":"test"}' > /dev/null
```

**Expected:**
- First request: ~3-5 seconds (LLM call)
- Second request: ~10-50ms (cached)
- **99% speedup!**

### Test 2: Postgres Audit Trail

**Verify audit logging:**
```bash
kubectl exec -it -n ai-lab deploy/postgres -- psql -U aiagent -d auditdb -c \
  "SELECT COUNT(*) as total_investigations, SUM(cost_usd) as total_cost FROM audit_logs;"
```

**Expected:**
```
 total_investigations | total_cost
----------------------+-----------
                   25 |   0.24350
```

### Test 3: Secure Tool Execution

**Test kubectl sandbox:**
```bash
kubectl exec -it -n ai-lab deploy/langchain-api -- kubectl get pods
```

**Expected:**
```
Command not allowed (read-only mode)
Error: kubectl execution blocked by security wrapper
```

**Verify read-only operations work:**
```bash
kubectl logs -n ai-lab deploy/langchain-api | grep "kubectl wrapper"
```

**Expected:** Log showing kubectl is wrapped with security layer

### Test 4: Metrics Accuracy

**Send 10 investigations:**
```bash
for i in {1..10}; do
  curl -s -X POST http://localhost:8000/investigate \
    -H "Content-Type: application/json" \
    -d "{\"alert\":\"Test $i\",\"service\":\"test\"}" > /dev/null
done
```

**Check Prometheus counter:**
```bash
curl -s http://localhost:8000/metrics | grep "^langchain_requests_total"
```

**Expected:** Counter increments by 10

### Test 5: End-to-End Flow

**Complete workflow test:**
```bash
# 1. Send investigation
RESPONSE=$(curl -s -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{"alert":"E2E test","service":"e2e-svc"}')

# 2. Extract audit log ID
AUDIT_ID=$(echo $RESPONSE | jq -r '.audit_log_id')

# 3. Verify in Postgres
kubectl exec -it -n ai-lab deploy/postgres -- psql -U aiagent -d auditdb -c \
  "SELECT * FROM audit_logs WHERE id = $AUDIT_ID;"

# 4. Check Redis cache
CACHE_KEY="investigation:$(echo $RESPONSE | jq -r '.investigation_id')"
docker exec redis redis-cli GET "$CACHE_KEY"

# 5. Verify metrics updated
curl http://localhost:8000/metrics | grep langchain_cost_total
```

**Expected:** All steps complete successfully showing full data flow

---

## 🎓 Understanding What You've Built

### Redis Caching Strategy

**Why caching matters:**
```
Without cache:
  10 investigations × 3s each = 30 seconds total
  10 investigations × $0.01 each = $0.10

With cache (80% hit rate):
  2 investigations × 3s = 6 seconds (cache miss)
  8 investigations × 0.01s = 0.08 seconds (cache hit)
  Total: 6.08 seconds (80% faster!)
  
  2 investigations × $0.01 = $0.02 (80% cost savings!)
```

### Audit Logging Benefits

**Production audit trail:**
- **Compliance**: Full investigation history
- **Debugging**: Trace decisions and outcomes
- **Cost attribution**: Per-service cost tracking
- **Analytics**: Pattern detection and optimization
- **Accountability**: Who requested what, when

### Secure Tool Execution

**kubectl wrapper prevents:**
```bash
# ❌ Dangerous operations blocked
kubectl delete deployment production-app
kubectl scale deployment --replicas=0
kubectl exec -it pod /bin/bash

# ✅ Read-only operations allowed
kubectl get pods
kubectl describe deployment
kubectl logs pod-name
```

---

## 💰 Cost Analysis

### Development (Docker Compose): $0.10-0.20/day

**LLM costs only:**
```
Testing: 50 investigations/day
Average: 300 tokens per investigation
Cost: 50 × 300 / 1000 × $0.002 = $0.03/day

With caching (80% hit rate):
Real LLM calls: 10/day
Cost: 10 × 300 / 1000 × $0.002 = $0.006/day
```

### Production (Kubernetes): $50-80/month

**Infrastructure:**
```
Agent pods (3 replicas): $15
Redis: $10
Postgres: $15
Prometheus: $5
Grafana: $5
Total infrastructure: $50/month
```

**LLM costs:**
```
1000 investigations/day × 30 days = 30,000/month
Cache hit rate: 75%
Real LLM calls: 7,500/month

Cost: 7,500 × 300 / 1000 × $0.002 = $4.50/month
```

**Total: ~$55/month** with good caching

### Cost Optimization

**1. Aggressive caching:**
- 90% hit rate → $1.50/month LLM (67% savings)

**2. Model selection:**
- GPT-3.5 for simple cases → $0.50/month (90% savings)

**3. Prompt optimization:**
- Reduce tokens by 30% → $3.15/month (30% savings)

---

## 🔧 Troubleshooting

### Issue: Pod CrashLoopBackOff

**Check logs:**
```bash
kubectl logs -n ai-lab deploy/langchain-api --previous
```

**Common causes:**
- Missing OpenAI API key
- Redis connection failed
- Postgres connection failed

**Solution:**
```bash
# Verify secrets
kubectl describe secret api-secrets -n ai-lab

# Check configmap
kubectl describe configmap app-config -n ai-lab
```

### Issue: Redis Not Reachable

**Test Redis connectivity:**
```bash
kubectl exec -it -n ai-lab deploy/redis -- redis-cli ping
```

**Expected:** `PONG`

**Check Redis service:**
```bash
kubectl get svc redis -n ai-lab
```

### Issue: Postgres Connection Refused

**Check Postgres logs:**
```bash
kubectl logs -n ai-lab deploy/postgres
```

**Test connection:**
```bash
kubectl exec -it -n ai-lab deploy/postgres -- psql -U aiagent -d auditdb -c "SELECT 1;"
```

### Issue: OpenAI API Key Missing

**Verify secret:**
```bash
kubectl get secret api-secrets -n ai-lab -o jsonpath='{.data.OPENAI_API_KEY}' | base64 -d
```

**Update secret:**
```bash
kubectl delete secret api-secrets -n ai-lab
kubectl create secret generic api-secrets -n ai-lab \
  --from-literal=OPENAI_API_KEY="sk-your-new-key"
kubectl rollout restart deployment/langchain-api -n ai-lab
```

### Issue: Metrics Not Showing in Grafana

**Check Prometheus targets:**
```bash
kubectl port-forward svc/prometheus -n ai-lab 9090:9090
# Open http://localhost:9090/targets
```

**Verify scrape config:**
```bash
kubectl logs -n ai-lab deploy/prometheus | grep langchain-api
```

---

## 🧹 Cleanup

### Cleanup Docker Compose

```bash
docker compose down -v
```

**Remove all data:**
```bash
docker compose down -v --remove-orphans
docker volume prune -f
```

### Cleanup Kubernetes

**Delete namespace (removes all resources):**
```bash
kubectl delete namespace ai-lab
```

**Delete KIND cluster:**
```bash
kind delete cluster --name langchain-lab
```

### Cleanup Docker Images

```bash
docker rmi langchain-api:latest
docker system prune -f
```

---

## 📊 Success Criteria Checklist

Your lab is complete when:

- [ ] Docker Compose stack running (5/5 services)
- [ ] API responding to health checks
- [ ] Database tables created
- [ ] First investigation successful
- [ ] Redis caching working (cache hit ratio > 0)
- [ ] Postgres audit logs storing data
- [ ] Prometheus metrics exposed
- [ ] Grafana dashboards visualizing data
- [ ] All unit tests passing
- [ ] KIND cluster created
- [ ] All K8s pods running (5/5)
- [ ] API accessible in Kubernetes
- [ ] Load testing successful
- [ ] kubectl sandbox enforced
- [ ] You understand full stack integration
- [ ] You understand caching strategy
- [ ] You understand audit logging

---

## 🎉 Congratulations!

You've deployed a production-grade LangChain system!

### What You've Mastered:

✅ **Production LangChain** - Real LLM integration  
✅ **Multi-Database Architecture** - Redis + Postgres  
✅ **Full Observability** - Prometheus + Grafana  
✅ **Secure Execution** - Sandboxed tools  
✅ **Audit Trail** - Complete investigation history  
✅ **Cost Optimization** - Caching and tracking  

You now have enterprise LangChain deployment skills!

Happy learning! 🚀🔗💾📊🔒