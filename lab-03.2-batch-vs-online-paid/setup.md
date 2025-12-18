# Lab 3.1 PAID Setup Guide – Production-Grade Batch Inference
## Enterprise Batch Inference with OpenTelemetry & Cost Intelligence

---

## 🎯 What You Will Achieve

By completing this setup, you will:

### Learning Objectives

1. **Deploy Production Batch Infrastructure** - Full observability stack for batch ML
2. **Implement OpenTelemetry in Batch Jobs** - Traces, metrics, and structured logging
3. **Build Cost-Aware ML Systems** - Track and optimize per-record inference costs
4. **Configure Resource Constraints** - Balance cost, speed, and reliability
5. **Export Telemetry at Scale** - Integration with observability backends
6. **Master Enterprise Patterns** - Production-ready batch inference architecture

### Expected Outcomes

- ✅ Production-grade batch inference job with full observability
- ✅ OpenTelemetry Collector receiving traces and metrics
- ✅ Per-record cost tracking and aggregation
- ✅ Resource-constrained jobs for cost optimization
- ✅ Scheduled CronJobs with enterprise monitoring
- ✅ Understanding of cost vs performance tradeoffs
- ✅ Export telemetry to external systems

### Real-World Skills

**ML Platform Engineers** will learn:
- How to standardize observability across ML pipelines
- Cost attribution patterns for ML workloads
- Production deployment architecture

**FinOps Professionals** will learn:
- ML cost tracking and optimization
- Resource utilization analysis
- Budget management for batch workloads

**SREs** will learn:
- Monitoring batch job health
- Performance troubleshooting with traces
- Setting up production alerting

**Data Scientists** will learn:
- How their batch models run in production
- Cost implications of model complexity
- Performance optimization opportunities

---

## 📋 Prerequisites

### Required Software

**1. Docker (24+)**
```bash
docker --version
```
Expected: `Docker version 24.x.x or higher`

**2. kind**
```bash
kind version
```
Expected: `kind v0.20.0 or higher`

**3. kubectl (1.29+)**
```bash
kubectl version --client
```
Expected: `v1.29.0 or higher`

**4. Python (3.11+)**
```bash
python3 --version
```
Expected: `Python 3.11.x or higher`

**5. Git**
```bash
git --version
```

### Required Knowledge

- Completion of Lab 3.1 FREE version (strongly recommended)
- Understanding of OpenTelemetry concepts (traces, metrics, spans)
- Kubernetes resource management (requests, limits)
- Basic cost optimization principles

### Recommended Preparation

- Review OpenTelemetry documentation
- Understand Kubernetes Jobs and CronJobs
- Familiarize with cloud cost models

---

## 🏗️ Understanding the Production Architecture

### Full Stack Components

```
┌─────────────────────────────────────────────────────────┐
│  Batch Inference Job (Pod)                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │                                                    │  │
│  │  Application Code                                  │  │
│  │  ├─ OpenTelemetry SDK                             │  │
│  │  ├─ Cost Calculation Logic                        │  │
│  │  ├─ Resource Constraints                          │  │
│  │  └─ Batch Processing                              │  │
│  │                                                    │  │
│  │  For Each Record:                                  │  │
│  │  1. Start trace span                              │  │
│  │  2. Process with timing                           │  │
│  │  3. Calculate cost                                │  │
│  │  4. Export metrics                                │  │
│  │  5. Log with trace ID                             │  │
│  │                                                    │  │
│  └─────────────────┬──────────────────────────────────┘  │
│                    │ OTLP (gRPC:4317)                    │
│                    ▼                                     │
│  ┌───────────────────────────────────────────────────┐  │
│  │  OpenTelemetry Collector                          │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │  Receivers:                                  │  │  │
│  │  │  - OTLP gRPC (port 4317)                    │  │  │
│  │  │  - OTLP HTTP (port 4318)                    │  │  │
│  │  │                                              │  │  │
│  │  │  Processors:                                 │  │  │
│  │  │  - Batch processor (optimize exports)       │  │  │
│  │  │  - Memory limiter (prevent OOM)             │  │  │
│  │  │  - Attributes processor (enrich data)       │  │  │
│  │  │                                              │  │  │
│  │  │  Exporters:                                  │  │  │
│  │  │  - Logging (stdout - this lab)              │  │  │
│  │  │  - Prometheus (production)                  │  │  │
│  │  │  - Jaeger (production)                      │  │  │
│  │  │  - Cloud providers (production)             │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
│  Resource Constraints Applied:                          │
│  - CPU: 250m (request) / 500m (limit)                  │
│  - Memory: 256Mi (request) / 512Mi (limit)             │
│  - Cost optimization through throttling                 │
└─────────────────────────────────────────────────────────┘
```

### Observability Data Types

**1. Traces:**
```
Batch Job Trace
├─ Span: batch_start
├─ Span: read_input_data
├─ Span: process_record (id=1)
│  ├─ Attributes: record_id, prediction, cost, latency
│  └─ Duration: 45ms
├─ Span: process_record (id=2)
│  ├─ Attributes: record_id, prediction, cost, latency
│  └─ Duration: 48ms
└─ Span: batch_complete
   └─ Attributes: total_records, total_cost, avg_latency
```

**2. Metrics:**
- `batch_total_records` - Count of records processed
- `record_latency_ms` - Histogram of per-record latency
- `batch_processing_ms` - Total batch execution time
- `batch_cost_usd` - Total batch cost
- `cost_per_record_usd` - Average cost per record
- `cpu_utilization` - CPU usage during processing

**3. Logs:**
```json
{
  "timestamp": "2024-01-15T10:30:00.123Z",
  "level": "INFO",
  "message": "Record processed",
  "record_id": 1,
  "prediction": 6.0,
  "latency_ms": 45,
  "cost_usd": 0.0001,
  "trace_id": "abc123...",
  "span_id": "def456..."
}
```

---

## 🚀 Step-by-Step Setup

### Step 1: Navigate to Lab Directory

```bash
cd lab-03.1-batch-vs-online-paid
```

Verify you're in the correct location:
```bash
ls
```

**Expected Output:**
```
Dockerfile  README.md  app/  k8s/  kind-mcp-cluster.yaml  setup.md  .env.example
```

---

### Step 2: Configure Environment

Copy the example environment file:
```bash
cp .env.example .env
```

View the configuration:
```bash
cat .env
```

**Expected Content:**
```bash
# Application Environment
APP_ENV=local

# OpenTelemetry Configuration
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector-paid:4317
OTEL_SERVICE_NAME=batch-inference-service
OTEL_TRACES_EXPORTER=otlp
OTEL_METRICS_EXPORTER=otlp

# Cost Model Parameters
COST_PER_CPU_HOUR=0.04        # $0.04 per CPU-hour (typical cloud cost)
COST_PER_MEMORY_GB_HOUR=0.005 # $0.005 per GB-hour
COST_PER_RECORD_TARGET=0.0001 # Target cost per record

# Resource Configuration
CPU_REQUEST=250m               # Guaranteed minimum
CPU_LIMIT=500m                 # Throttled maximum (cost control)
MEMORY_REQUEST=256Mi
MEMORY_LIMIT=512Mi

# Batch Processing
BATCH_SIZE=1000                # Records per batch
ENABLE_COST_TRACKING=true
ENABLE_TELEMETRY=true
```

**Understanding key settings:**

- **OTEL_EXPORTER_OTLP_ENDPOINT:** Where telemetry is sent
- **COST_PER_CPU_HOUR:** Based on cloud provider pricing (e.g., GCP, AWS)
- **CPU_LIMIT:** Throttling for cost optimization
- **ENABLE_COST_TRACKING:** Real-time cost calculation

**Optional: Customize for your needs:**
```bash
# For higher performance (higher cost)
echo "CPU_LIMIT=1000m" >> .env

# For lower cost (slower processing)
echo "CPU_LIMIT=250m" >> .env
```

---

### Step 3: Create kind Cluster

Create the cluster:
```bash
kind create cluster --config kind-mcp-cluster.yaml
```

**Expected Output:**
```
Creating cluster "mcp-cluster" ...
 ✓ Ensuring node image (kindest/node:v1.30.0) 🖼
 ✓ Preparing nodes 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
Set kubectl context to "kind-mcp-cluster"
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

### Step 4: Examine the Enhanced Batch Job Code

Before building, understand the production features:

**View the main batch job:**
```bash
cat app/batch_job.py | head -50
```

**Key production features:**

**1. OpenTelemetry Initialization:**
```python
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider

# Initialize tracer
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Initialize metrics
metrics.set_meter_provider(MeterProvider())
meter = metrics.get_meter(__name__)
```

**2. Cost Calculation Logic:**
```bash
cat app/cost_model.py
```

**3. Configuration Management:**
```bash
cat app/config.py
```

---

### Step 5: Build Docker Image

Build the production-grade image:
```bash
docker build -t ai-lab-3-1-paid:v1 .
```

**Expected Output:**
```
[+] Building 35.4s (15/15) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 567B
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/library/python:3.11-slim
 => [1/9] FROM docker.io/library/python:3.11-slim
 => [2/9] WORKDIR /app
 => [3/9] COPY app/requirements.txt .
 => [4/9] RUN pip install --no-cache-dir -r requirements.txt
 => [5/9] COPY app/ .
 => [6/9] COPY .env .
 => [7/9] RUN useradd -m appuser && chown -R appuser:appuser /app
 => [8/9] USER appuser
 => exporting to image
 => => exporting layers
 => => writing image sha256:pqr456...
 => => naming to docker.io/library/ai-lab-3-1-paid:v1
```

**Verify image:**
```bash
docker images | grep ai-lab-3-1-paid
```

**Expected Output:**
```
ai-lab-3-1-paid   v1      pqr456stu789   2 minutes ago   312MB
```

**Note:** Larger than FREE version due to OpenTelemetry dependencies.

---

### Step 6: Load Image into kind

```bash
kind load docker-image ai-lab-3-1-paid:v1 --name mcp-cluster
```

**Expected Output:**
```
Image: "ai-lab-3-1-paid:v1" with ID "sha256:pqr456..." not yet present on node "mcp-cluster-control-plane", loading...
```

**Verify:**
```bash
docker exec -it mcp-cluster-control-plane crictl images | grep ai-lab-3-1-paid
```

---

### Step 7: Create Namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

**Expected Output:**
```
namespace/ai-ml-lab-3-1-paid created
```

**Verify:**
```bash
kubectl get namespace ai-ml-lab-3-1-paid
```

**Expected Output:**
```
NAME                 STATUS   AGE
ai-ml-lab-3-1-paid   Active   10s
```

---

### Step 8: Deploy OpenTelemetry Collector Configuration

Deploy the ConfigMap:
```bash
kubectl apply -f k8s/otel-collector-config.yaml
```

**Expected Output:**
```
configmap/otel-collector-config created
```

**View the configuration:**
```bash
kubectl get configmap -n ai-ml-lab-3-1-paid otel-collector-config -o yaml
```

**Key sections in the config:**

**Receivers:**
```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
```

**Processors:**
```yaml
processors:
  batch:
    timeout: 10s
    send_batch_size: 1024
  memory_limiter:
    check_interval: 1s
    limit_mib: 512
```

**Exporters:**
```yaml
exporters:
  logging:
    loglevel: info
  debug:
    verbosity: detailed
```

---

### Step 9: Deploy OpenTelemetry Collector

```bash
kubectl apply -f k8s/otel-collector-deploy.yaml
```

**Expected Output:**
```
deployment.apps/otel-collector-paid created
service/otel-collector-paid created
```

**Wait for collector to be ready:**
```bash
kubectl wait --for=condition=available --timeout=60s deployment/otel-collector-paid -n ai-ml-lab-3-1-paid
```

**Expected Output:**
```
deployment.apps/otel-collector-paid condition met
```

**Verify collector is running:**
```bash
kubectl get pods -n ai-ml-lab-3-1-paid
```

**Expected Output:**
```
NAME                                  READY   STATUS    RESTARTS   AGE
otel-collector-paid-xxxxxxxxxx-xxxxx  1/1     Running   0          30s
```

**Check collector logs:**
```bash
kubectl logs -n ai-ml-lab-3-1-paid -l app=otel-collector-paid --tail=20
```

**Expected Output:**
```
2024-01-15T10:30:00.123Z info    service@v0.91.0/service.go:143  Starting otelcol...
2024-01-15T10:30:00.234Z info    service@v0.91.0/service.go:169  Everything is ready. Begin running and processing data.
2024-01-15T10:30:00.345Z info    otlpreceiver@v0.91.0/otlp.go:83 Starting GRPC server {"endpoint": "0.0.0.0:4317"}
2024-01-15T10:30:00.456Z info    otlpreceiver@v0.91.0/otlp.go:101 Starting HTTP server {"endpoint": "0.0.0.0:4318"}
```

**What this validates:**
- ✅ Collector started successfully
- ✅ OTLP receivers listening on ports 4317 (gRPC) and 4318 (HTTP)
- ✅ Ready to receive telemetry data

---

### Step 10: Deploy One-Time Batch Job

```bash
kubectl apply -f k8s/job-batch-once.yaml
```

**Expected Output:**
```
job.batch/batch-inference-paid-once created
```

**Check job status:**
```bash
kubectl get jobs -n ai-ml-lab-3-1-paid
```

**Expected Output (initial):**
```
NAME                        COMPLETIONS   DURATION   AGE
batch-inference-paid-once   0/1           5s         5s
```

**Watch pod status:**
```bash
kubectl get pods -n ai-ml-lab-3-1-paid -w
```

**Expected progression:**
```
NAME                              READY   STATUS    RESTARTS   AGE
otel-collector-paid-xxx-yyy       1/1     Running   0          2m
batch-inference-paid-once-zzz     0/1     Pending   0          2s
batch-inference-paid-once-zzz     0/1     ContainerCreating   0    3s
batch-inference-paid-once-zzz     1/1     Running   0          8s
batch-inference-paid-once-zzz     0/1     Completed   0        15s
```

Press `Ctrl+C` to stop watching.

**Wait for completion:**
```bash
kubectl wait --for=condition=complete --timeout=60s job/batch-inference-paid-once -n ai-ml-lab-3-1-paid
```

---

### Step 11: View Batch Job Output with Observability

Get the pod name:
```bash
POD_NAME=$(kubectl get pods -n ai-ml-lab-3-1-paid -l app=batch-inference-paid -o jsonpath='{.items[0].metadata.name}')
echo "Pod name: $POD_NAME"
```

**View the logs:**
```bash
kubectl logs -n ai-ml-lab-3-1-paid "$POD_NAME"
```

**Expected Output:**
```json
{"timestamp": "2024-01-15T10:32:00.123Z", "level": "INFO", "message": "Initializing OpenTelemetry", "service": "batch-inference-service"}
{"timestamp": "2024-01-15T10:32:00.234Z", "level": "INFO", "message": "Connected to OTLP collector", "endpoint": "http://otel-collector-paid:4317"}
{"timestamp": "2024-01-15T10:32:00.345Z", "level": "INFO", "message": "Starting batch inference job", "total_records": 2}

{"timestamp": "2024-01-15T10:32:00.456Z", "level": "INFO", "message": "Record processed", "id": 1, "prediction": 6.0, "latency_ms": 45, "cost_usd": 0.0001, "trace_id": "abc123def456", "span_id": "ghi789"}

{"timestamp": "2024-01-15T10:32:00.501Z", "level": "INFO", "message": "Record processed", "id": 2, "prediction": 15.0, "latency_ms": 48, "cost_usd": 0.0001, "trace_id": "jkl012mno345", "span_id": "pqr678"}

{"timestamp": "2024-01-15T10:32:00.567Z", "level": "INFO", "message": "Batch job completed", "summary": {
  "total_records": 2,
  "successful": 2,
  "failed": 0,
  "avg_prediction": 10.5,
  "total_latency_ms": 93,
  "avg_latency_ms": 46.5,
  "total_cost_usd": 0.0002,
  "cost_per_record_usd": 0.0001,
  "cpu_utilization": 0.45,
  "memory_used_mb": 128
}}
```

**What this validates:**
- ✅ OpenTelemetry initialized and connected
- ✅ Each record has unique trace ID
- ✅ Latency tracked per record
- ✅ Cost calculated per record
- ✅ Comprehensive summary with cost metrics
- ✅ Resource utilization tracked

---

### Step 12: View OpenTelemetry Collector Telemetry

**Check collector received the data:**
```bash
kubectl logs -n ai-ml-lab-3-1-paid -l app=otel-collector-paid --tail=100
```

**Expected Output:**
```
2024-01-15T10:32:00.600Z info    TracesExporter  {"kind": "exporter", "name": "logging", "traces_received": 2}

Trace 1:
  TraceID: abc123def456
  SpanID: ghi789
  ParentSpanID: 
  Name: process_record
  Kind: SPAN_KIND_INTERNAL
  Start: 2024-01-15T10:32:00.456Z
  End: 2024-01-15T10:32:00.501Z
  Duration: 45ms
  Attributes:
    service.name: batch-inference-service
    record.id: 1
    prediction: 6.0
    latency_ms: 45
    cost_usd: 0.0001
    cpu_cores: 0.5
    memory_mb: 512

Trace 2:
  TraceID: jkl012mno345
  SpanID: pqr678
  Name: process_record
  Duration: 48ms
  Attributes:
    record.id: 2
    prediction: 15.0
    cost_usd: 0.0001

2024-01-15T10:32:00.650Z info    MetricsExporter {"kind": "exporter", "name": "logging", "metrics_received": 6}

Metrics:
  batch_total_records:
    Value: 2
    Type: Counter
  
  record_latency_ms:
    Type: Histogram
    Buckets:
      [0-50ms]: 2 records
      [50-100ms]: 0 records
      [100-150ms]: 0 records
    Sum: 93ms
    Count: 2
    
  batch_processing_ms:
    Value: 93
    Type: Gauge
    
  batch_cost_usd:
    Value: 0.0002
    Type: Gauge
    
  cost_per_record_usd:
    Value: 0.0001
    Type: Gauge
    
  cpu_utilization:
    Value: 0.45
    Type: Gauge
```

**What this validates:**
- ✅ Traces received with full span details
- ✅ All attributes captured (record ID, cost, latency)
- ✅ Metrics exported (counters, histograms, gauges)
- ✅ Histogram shows latency distribution
- ✅ Cost metrics tracked
- ✅ Resource utilization recorded

---

### Step 13: Deploy CronJob

```bash
kubectl apply -f k8s/cronjob-batch.yaml
```

**Expected Output:**
```
cronjob.batch/batch-inference-paid-scheduled created
```

**Verify CronJob:**
```bash
kubectl get cronjobs -n ai-ml-lab-3-1-paid
```

**Expected Output:**
```
NAME                             SCHEDULE       SUSPEND   ACTIVE   LAST SCHEDULE   AGE
batch-inference-paid-scheduled   */10 * * * *   False     0        <none>          15s
```

**Understanding the schedule:**
- `*/10 * * * *` = Every 10 minutes
- `SUSPEND: False` = Active
- `LAST SCHEDULE: <none>` = Hasn't run yet

**View CronJob details:**
```bash
kubectl describe cronjob batch-inference-paid-scheduled -n ai-ml-lab-3-1-paid
```

---

### Step 14: Wait for CronJob Execution

**Wait for first scheduled run (up to 10 minutes):**
```bash
echo "Waiting for CronJob to trigger (this may take up to 10 minutes)..."
echo "You can check status with: kubectl get jobs -n ai-ml-lab-3-1-paid"
```

**Or manually trigger for testing:**
```bash
kubectl create job --from=cronjob/batch-inference-paid-scheduled manual-test -n ai-ml-lab-3-1-paid
```

**Check for created jobs:**
```bash
kubectl get jobs -n ai-ml-lab-3-1-paid
```

**Expected Output:**
```
NAME                                   COMPLETIONS   DURATION   AGE
batch-inference-paid-once              1/1           15s        5m
batch-inference-paid-scheduled-xxxxx1  1/1           14s        2m
manual-test                            1/1           13s        30s
```

---

### Step 15: Verify Telemetry from CronJob

**Get latest job's pod:**
```bash
LATEST_POD=$(kubectl get pods -n ai-ml-lab-3-1-paid --sort-by=.metadata.creationTimestamp -o jsonpath='{.items[-1].metadata.name}')
echo "Latest pod: $LATEST_POD"
```

**View its logs:**
```bash
kubectl logs -n ai-ml-lab-3-1-paid "$LATEST_POD"
```

**Check collector received data:**
```bash
kubectl logs -n ai-ml-lab-3-1-paid -l app=otel-collector-paid --tail=50 | grep -A5 "TracesExporter\|MetricsExporter"
```

**What this validates:**
- ✅ CronJob creates jobs on schedule
- ✅ Each job exports telemetry independently
- ✅ Collector aggregates data from all jobs
- ✅ Cost tracking works across multiple runs

---

## ✅ Testing and Validation

### Test 1: Verify Cost Calculation Accuracy

**Extract cost from logs:**
```bash
kubectl logs -n ai-ml-lab-3-1-paid "$POD_NAME" | grep "cost_usd"
```

**Manual verification:**
```
Record processing time: 45ms = 0.045 seconds
CPU limit: 0.5 cores
Cost per CPU-hour: $0.04

CPU cost = (0.5 cores × $0.04/hour × 0.045 seconds) / 3600 seconds
         = 0.00000025/second × 0.045
         = 0.00001125

Memory: 512Mi = 0.5 GB
Cost per GB-hour: $0.005

Memory cost = (0.5 GB × $0.005/hour × 0.045 seconds) / 3600
            = 0.00000003125

Total ≈ $0.0001 per record ✓
```

### Test 2: Verify Trace Context Propagation

**Get trace ID from job logs:**
```bash
TRACE_ID=$(kubectl logs -n ai-ml-lab-3-1-paid "$POD_NAME" | grep "trace_id" | head -1 | grep -oP 'trace_id": "\K[^"]+')
echo "Trace ID: $TRACE_ID"
```

**Find the same trace in collector:**
```bash
kubectl logs -n ai-ml-lab-3-1-paid -l app=otel-collector-paid | grep "$TRACE_ID"
```

**Expected:** Same trace ID appears in both places

### Test 3: Verify Resource Constraints

**Check resource usage:**
```bash
kubectl top pod -n ai-ml-lab-3-1-paid -l app=batch-inference-paid
```

**Expected Output:**
```
NAME                                CPU(cores)   MEMORY(bytes)
batch-inference-paid-once-xxxxx     450m         145Mi
```

**Verify it's within limits:**
- CPU: 450m < 500m limit ✓
- Memory: 145Mi < 512Mi limit ✓

### Test 4: Verify Metrics Export

**Count metric types in collector:**
```bash
kubectl logs -n ai-ml-lab-3-1-paid -l app=otel-collector-paid | grep -c "batch_total_records"
```

**Expected:** At least 1 (one per job execution)

### Test 5: Validate Histogram Buckets

**Check histogram distribution:**
```bash
kubectl logs -n ai-ml-lab-3-1-paid -l app=otel-collector-paid | grep -A10 "record_latency_ms"
```

**Expected:** Histogram with bucket counts showing latency distribution

---

## 🧪 Running Unit Tests

### Step 1: Navigate to App Directory

```bash
cd app
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed opentelemetry-api-1.x.x opentelemetry-sdk-1.x.x opentelemetry-exporter-otlp-1.x.x pytest-7.x.x ...
```

### Step 4: Run Tests

```bash
pytest -v
```

**Expected Output:**
```
================== test session starts ==================
collected 3 items

tests/test_batch_job.py::test_batch_inference PASSED     [33%]
tests/test_batch_job.py::test_cost_calculation PASSED    [66%]
tests/test_batch_job.py::test_telemetry_export PASSED    [100%]

=================== 3 passed in 0.25s ===================
```

### Step 5: Test Cost Model Separately

```bash
pytest -v tests/test_batch_job.py::test_cost_calculation
```

**Expected Output:**
```
tests/test_batch_job.py::test_cost_calculation PASSED

Cost calculation test details:
  CPU cost: $0.00001125
  Memory cost: $0.00000003125
  Total cost: $0.00001156
  Expected: $0.0001 (within tolerance) ✓
```

---

## 🎓 Understanding Production Features

### OpenTelemetry Integration Deep Dive

**Span Creation:**
```python
with tracer.start_as_current_span("process_record") as span:
    # Set attributes
    span.set_attribute("record.id", record_id)
    span.set_attribute("prediction", prediction)
    span.set_attribute("cost_usd", cost)
    
    # Span timing is automatic
    result = process_record(record)
    
    # Span ends automatically
```

**Metrics Collection:**
```python
# Counter
records_counter.add(1, {"status": "success"})

# Histogram
latency_histogram.record(latency_ms, {"record_id": record_id})

# Gauge
cost_gauge.set(total_cost)
```

### Cost Calculation Logic

**Per-Record Cost Formula:**
```
CPU Cost = (CPU_cores × CPU_rate_per_hour × duration_seconds) / 3600
Memory Cost = (Memory_GB × Memory_rate_per_hour × duration_seconds) / 3600
Total Cost = CPU Cost + Memory Cost
```

**Batch-Level Aggregation:**
```
Total Batch Cost = Σ(Per-Record Cost)
Average Cost = Total Cost / Record Count
Cost per 1M records = Average Cost × 1,000,000
```

### Resource Throttling Impact

| CPU Limit | Avg Latency | Cost/Record | Records/Hour | Monthly Cost |
|-----------|-------------|-------------|--------------|--------------|
| 250m | 90ms | $0.00005 | 40,000 | $1.20 |
| 500m | 45ms | $0.0001 | 80,000 | $2.40 |
| 1000m | 25ms | $0.0002 | 144,000 | $4.32 |

**Key Insight:** 2x CPU = 2x cost but only 1.8x throughput!

---

## 💰 Production Cost Analysis

### Monthly Cost Projection

**Scenario:** CronJob runs every hour (720 times/month)

**Job Specs:**
- Runtime: 2 min/job
- CPU: 0.5 cores
- Memory: 0.5 GB
- Records: 1,000/job

**Calculation:**
```
Monthly runtime: 720 jobs × 2 min = 1,440 min = 24 hours

Compute cost:
  CPU: 0.5 cores × 24 hrs × $0.04/hr = $0.48
  Memory: 0.5 GB × 24 hrs × $0.005/hr = $0.06
  Subtotal: $0.54

Collector overhead: $0.20/month
Storage (logs): $0.10/month

Total: $0.84/month

Per record cost: $0.84 / (720 × 1,000) = $0.0000012
Per 1M records: $1.20
```

### Cost Optimization Comparison

| Strategy | Monthly Cost | Savings |
|----------|-------------|---------|
| Baseline (500m CPU, hourly) | $0.84 | - |
| Reduce to 250m CPU | $0.54 | 36% |
| Run every 6 hours | $0.14 | 83% |
| Use spot instances | $0.17 | 80% |
| All optimizations | $0.04 | 95% |

---

## 🔧 Troubleshooting

### Issue: Collector Not Receiving Telemetry

**Symptoms:**
- Job completes successfully
- Collector logs show no traces/metrics

**Diagnosis:**
```bash
# Check job can reach collector
kubectl exec -n ai-ml-lab-3-1-paid "$POD_NAME" -- nc -zv otel-collector-paid 4317

# Check collector endpoints
kubectl get svc -n ai-ml-lab-3-1-paid otel-collector-paid

# Check job environment variables
kubectl describe pod -n ai-ml-lab-3-1-paid "$POD_NAME" | grep -A10 "Environment"
```

**Solution:**
```bash
# Verify OTEL_EXPORTER_OTLP_ENDPOINT is correct
kubectl get pod -n ai-ml-lab-3-1-paid "$POD_NAME" -o yaml | grep OTEL_EXPORTER

# Should be: http://otel-collector-paid:4317
```

---

### Issue: Cost Calculations Seem Incorrect

**Check cost parameters:**
```bash
kubectl logs -n ai-ml-lab-3-1-paid "$POD_NAME" | grep -E "COST_PER|CPU_LIMIT|MEMORY_LIMIT"
```

**Verify against cloud pricing:**
- GCP: https://cloud.google.com/products/calculator
- AWS: https://calculator.aws/
- Azure: https://azure.microsoft.com/en-us/pricing/calculator/

**Recalculate manually:**
```python
# Example
cpu_seconds = 0.045  # 45ms
cpu_cores = 0.5
cpu_rate = 0.04  # per hour

cost = (cpu_cores * cpu_rate * cpu_seconds) / 3600
print(f"Expected cost: ${cost:.6f}")
```

---

### Issue: High Resource Usage

**Symptoms:**
```bash
kubectl top pod -n ai-ml-lab-3-1-paid
# Shows CPU near or at limit
```

**Investigation:**
```bash
# Check for CPU throttling
kubectl describe pod -n ai-ml-lab-3-1-paid "$POD_NAME" | grep -i throttl

# View resource limits
kubectl describe pod -n ai-ml-lab-3-1-paid "$POD_NAME" | grep -A5 "Limits"
```

**Solutions:**

**Option 1: Increase limits (higher cost)**
```yaml
limits:
  cpu: "1000m"
  memory: "1Gi"
```

**Option 2: Optimize code**
- Reduce processing per record
- Use more efficient algorithms
- Batch operations

**Option 3: Accept slower processing**
- Keep limits low for cost control
- Increase schedule interval

---

## 🧹 Cleanup

### Step 1: Delete All Jobs

```bash
kubectl delete job --all -n ai-ml-lab-3-1-paid
```

### Step 2: Delete CronJob

```bash
kubectl delete -f k8s/cronjob-batch.yaml
```

### Step 3: Delete Remaining Resources

```bash
kubectl delete -f k8s/job-batch-once.yaml
kubectl delete -f k8s/otel-collector-deploy.yaml
kubectl delete -f k8s/otel-collector-config.yaml
kubectl delete -f k8s/namespace.yaml
```

**Or delete everything at once:**
```bash
kubectl delete namespace ai-ml-lab-3-1-paid
```

### Step 4: Delete kind Cluster

```bash
kind delete cluster --name mcp-cluster
```

**Verify:**
```bash
kind get clusters
kubectl config get-contexts
```

---

## 📊 Success Criteria Checklist

Your lab is complete when:

- [ ] kind cluster created and running
- [ ] Docker image built with production features
- [ ] Namespace created
- [ ] OpenTelemetry Collector deployed and running
- [ ] Collector receiving telemetry on ports 4317/4318
- [ ] One-time job completed successfully
- [ ] Job logs show per-record costs
- [ ] Job logs include trace IDs
- [ ] Collector logs show received traces
- [ ] Collector logs show received metrics
- [ ] Histogram metrics show latency distribution
- [ ] Cost metrics calculated correctly
- [ ] Resource usage within limits
- [ ] CronJob created and active
- [ ] CronJob created at least one scheduled job
- [ ] Manual job trigger works
- [ ] Unit tests pass
- [ ] You understand cost vs performance tradeoffs
- [ ] You can explain OpenTelemetry integration

---

## 📚 Next Steps

### Production Enhancements

**1. Export to Real Backends:**
- Prometheus for metrics
- Jaeger for traces
- CloudWatch/Stackdriver

**2. Add Alerting:**
- Cost per record > threshold
- Job failures
- Latency anomalies

**3. Implement Cost Budgets:**
- Daily/weekly spending limits
- Auto-scaling based on budget
- Cost forecasting

**4. Advanced Telemetry:**
- Exemplars linking metrics to traces
- Custom span events
- Baggage for context propagation

---

## 🎉 Congratulations!

You've completed Lab 3.1 PAID Setup!

### What You've Mastered:

✅ **Production Batch Observability** - Enterprise-grade monitoring  
✅ **Cost-Aware Engineering** - Financial intelligence in ML systems  
✅ **OpenTelemetry Integration** - Industry-standard telemetry  
✅ **Resource Optimization** - Balancing cost and performance  
✅ **Enterprise Patterns** - Production-ready batch inference  

You now have the skills to build and operate production ML batch systems!

Happy learning! 🚀💰📊🔍