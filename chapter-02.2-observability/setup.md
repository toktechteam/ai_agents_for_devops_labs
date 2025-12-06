# Lab 2.2 PAID Version Setup Guide
## Production Observability for AI Inference with OpenTelemetry

---

## 🎯 What You Will Achieve

By completing this lab, you will:

### Learning Objectives
1. **Master OpenTelemetry Integration** - Implement industry-standard observability using OpenTelemetry SDK
2. **Build OTLP Pipelines** - Set up telemetry export to OpenTelemetry Collector
3. **Implement Distributed Tracing** - Track requests across services with trace IDs and spans
4. **Create Rich Metrics** - Use histogram buckets for accurate latency distribution analysis
5. **Deploy Production-Ready Architecture** - Use namespaces, resource limits, and proper configuration
6. **Understand Observability Costs** - Learn to reason about cloud costs for observability systems

### Expected Outcomes
- ✅ Production-grade AI inference service with OpenTelemetry
- ✅ OpenTelemetry Collector receiving traces and metrics
- ✅ Distributed tracing with unique trace IDs for each request
- ✅ Histogram-based latency metrics (not just averages)
- ✅ Namespace isolation and resource management
- ✅ Understanding of observability architecture for ML systems
- ✅ Cost-optimized deployment (<$10/month in cloud)

### Real-World Application
- **Production ML Teams** can use this pattern for real ML services
- **Platform Engineers** can standardize observability across microservices
- **SREs** can implement SLO monitoring and alerting
- **Cost-conscious organizations** can deploy observable systems affordably
- **Enterprise teams** can integrate with existing observability stacks (Prometheus, Jaeger, Datadog)

---

## 📋 Prerequisites

### Required Software
- **Operating System:** Ubuntu 22.04 (or similar Linux / WSL2 / macOS)
- **Docker:** Version 24 or higher
- **kind:** Kubernetes in Docker
- **kubectl:** Version 1.29 or higher
- **Python:** Version 3.11 or higher
- **Git:** For cloning repositories

### Required Knowledge
- **Intermediate Kubernetes:** Namespaces, ConfigMaps, resource limits
- **OpenTelemetry concepts:** Basic understanding of traces, spans, and metrics
- **Docker:** Multi-stage builds and container networking
- **Observability principles:** Logs, metrics, traces (the three pillars)

### Recommended Reading
- OpenTelemetry documentation: https://opentelemetry.io/docs/
- Kubernetes resource management: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
- Distributed tracing concepts

### Verification Commands

Check Docker:
```bash
docker --version
# Expected: Docker version 24.x.x or higher
```

Check kind:
```bash
kind --version
# Expected: kind v0.20.0 or higher
```

Check kubectl:
```bash
kubectl version --client
# Expected: v1.29.0 or higher
```

Check Python:
```bash
python3 --version
# Expected: Python 3.11.x or higher
```

---

## 🏗️ Architecture Overview

### What You're Building

```
┌─────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                    │
│  ┌───────────────────────────────────────────────────┐  │
│  │         Namespace: ai-ml-lab-2-2                  │  │
│  │                                                    │  │
│  │  ┌──────────────────┐      ┌──────────────────┐  │  │
│  │  │  AI Inference    │      │  OpenTelemetry   │  │  │
│  │  │  Service         │─────▶│  Collector       │  │  │
│  │  │                  │ OTLP │                  │  │  │
│  │  │  - FastAPI       │ 4317 │  - Receivers     │  │  │
│  │  │  - OTel SDK      │      │  - Processors    │  │  │
│  │  │  - Tracing       │      │  - Exporters     │  │  │
│  │  │  - Metrics       │      │                  │  │  │
│  │  └──────────────────┘      └──────────────────┘  │  │
│  │           │                         │             │  │
│  │           │                         │             │  │
│  │      Port 9000              Logs to stdout        │  │
│  └───────────┼─────────────────────────┼─────────────┘  │
│              │                         │                 │
│         Port Forward              kubectl logs           │
└──────────────┼─────────────────────────┼─────────────────┘
               │                         │
               ▼                         ▼
         Your Machine              Terminal Output
```

### Components

1. **AI Inference Service**
   - FastAPI application with OpenTelemetry instrumentation
   - Exports traces and metrics via OTLP protocol
   - Sends data to collector on port 4317

2. **OpenTelemetry Collector**
   - Receives telemetry data via OTLP
   - Processes and batches data
   - Exports to stdout (can be configured for Prometheus, Jaeger, etc.)

3. **Namespace Isolation**
   - Dedicated `ai-ml-lab-2-2` namespace
   - Resource quotas and limits
   - Clear separation from other workloads

---

## 🚀 Step-by-Step Setup

### Step 1: Create kind Cluster

Navigate to the lab directory:
```bash
cd lab-02.2-observability
```

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

**Verify the cluster:**
```bash
kubectl get nodes
```

**Expected Output:**
```
NAME                      STATUS   ROLES           AGE   VERSION
mcp-cluster-control-plane Ready    control-plane   45s   v1.30.0
```

---

### Step 2: Navigate to PAID Directory

```bash
cd paid
```

Verify you're in the correct directory:
```bash
ls
```

**Expected Output:**
```
Dockerfile  app/  k8s/  load-generator/  .env.example
```

---

### Step 3: Configure Environment

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
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
OTEL_SERVICE_NAME=ai-inference-service
OTEL_TRACES_EXPORTER=otlp
OTEL_METRICS_EXPORTER=otlp

# Model Configuration
DEFAULT_LATENCY_MS=100
MAX_BATCH_SIZE=32

# API Configuration
API_PORT=9000
```

**Understanding the configuration:**
- `APP_ENV` - Environment name (local, dev, staging, prod)
- `OTEL_EXPORTER_OTLP_ENDPOINT` - Where to send telemetry data
- `OTEL_SERVICE_NAME` - Service identifier in traces
- `DEFAULT_LATENCY_MS` - Simulated model latency
- `API_PORT` - Application listening port

---

### Step 4: Build Docker Image

Build the application image:
```bash
docker build -t ai-lab-2-2-paid:v1 .
```

**Expected Output:**
```
[+] Building 52.3s (14/14) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 456B
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/library/python:3.11-slim
 => [1/8] FROM docker.io/library/python:3.11-slim
 => [2/8] WORKDIR /app
 => [3/8] COPY app/requirements.txt .
 => [4/8] RUN pip install --no-cache-dir -r requirements.txt
 => [5/8] COPY app/ .
 => [6/8] COPY .env .
 => [7/8] RUN useradd -m appuser && chown -R appuser:appuser /app
 => [8/8] USER appuser
 => exporting to image
 => => exporting layers
 => => writing image sha256:def456...
 => => naming to docker.io/library/ai-lab-2-2-paid:v1
```

**Verify the image:**
```bash
docker images | grep ai-lab-2-2-paid
```

**Expected Output:**
```
ai-lab-2-2-paid   v1      def456abc789   2 minutes ago   298MB
```

---

### Step 5: Load Image into kind

```bash
kind load docker-image ai-lab-2-2-paid:v1 --name mcp-cluster
```

**Expected Output:**
```
Image: "ai-lab-2-2-paid:v1" with ID "sha256:def456..." not yet present on node "mcp-cluster-control-plane", loading...
```

**Verify image in kind:**
```bash
docker exec -it mcp-cluster-control-plane crictl images | grep ai-lab-2-2-paid
```

---

### Step 6: Create Namespace

Create the dedicated namespace:
```bash
kubectl apply -f k8s/namespace.yaml
```

**Expected Output:**
```
namespace/ai-ml-lab-2-2 created
```

**Verify namespace:**
```bash
kubectl get namespace ai-ml-lab-2-2
```

**Expected Output:**
```
NAME            STATUS   AGE
ai-ml-lab-2-2   Active   10s
```

---

### Step 7: Deploy OpenTelemetry Collector Configuration

Deploy the collector ConfigMap:
```bash
kubectl apply -f k8s/collector-config.yaml
```

**Expected Output:**
```
configmap/otel-collector-config created
```

**Verify ConfigMap:**
```bash
kubectl get configmap -n ai-ml-lab-2-2
```

**Expected Output:**
```
NAME                   DATA   AGE
otel-collector-config  1      15s
```

**View the configuration:**
```bash
kubectl get configmap otel-collector-config -n ai-ml-lab-2-2 -o yaml
```

This will show the OpenTelemetry Collector pipeline configuration.

---

### Step 8: Deploy OpenTelemetry Collector

Deploy the collector:
```bash
kubectl apply -f k8s/collector-deployment.yaml
```

**Expected Output:**
```
deployment.apps/otel-collector created
service/otel-collector created
```

**Wait for collector to be ready:**
```bash
kubectl wait --for=condition=available --timeout=60s deployment/otel-collector -n ai-ml-lab-2-2
```

**Expected Output:**
```
deployment.apps/otel-collector condition met
```

**Verify collector is running:**
```bash
kubectl get pods -n ai-ml-lab-2-2
```

**Expected Output:**
```
NAME                              READY   STATUS    RESTARTS   AGE
otel-collector-xxxxxxxxxx-xxxxx   1/1     Running   0          45s
```

**Check collector logs:**
```bash
kubectl logs -n ai-ml-lab-2-2 -l app=otel-collector --tail=20
```

**Expected Output:**
```
2024-01-15T10:30:00.123Z info    service@v0.91.0/service.go:143  Starting otelcol...
2024-01-15T10:30:00.234Z info    service@v0.91.0/service.go:169  Everything is ready. Begin running and processing data.
2024-01-15T10:30:00.345Z info    otlpreceiver@v0.91.0/otlp.go:83 Starting GRPC server {"kind": "receiver", "name": "otlp", "endpoint": "0.0.0.0:4317"}
2024-01-15T10:30:00.456Z info    otlpreceiver@v0.91.0/otlp.go:101 Starting HTTP server {"kind": "receiver", "name": "otlp", "endpoint": "0.0.0.0:4318"}
```

**What this validates:**
- ✅ Collector is running and healthy
- ✅ OTLP receivers are listening on ports 4317 (gRPC) and 4318 (HTTP)
- ✅ Configuration was loaded successfully

---

### Step 9: Deploy AI Inference Application

Deploy the application:
```bash
kubectl apply -f k8s/deployment.yaml
```

**Expected Output:**
```
deployment.apps/ai-lab-2-2-paid created
```

Deploy the service:
```bash
kubectl apply -f k8s/service.yaml
```

**Expected Output:**
```
service/ai-lab-2-2-paid created
```

**Wait for application to be ready:**
```bash
kubectl wait --for=condition=available --timeout=60s deployment/ai-lab-2-2-paid -n ai-ml-lab-2-2
```

**Expected Output:**
```
deployment.apps/ai-lab-2-2-paid condition met
```

---

### Step 10: Verify Complete Deployment

Check all pods in the namespace:
```bash
kubectl get pods -n ai-ml-lab-2-2
```

**Expected Output:**
```
NAME                              READY   STATUS    RESTARTS   AGE
otel-collector-xxxxxxxxxx-xxxxx   1/1     Running   0          3m
ai-lab-2-2-paid-yyyyyyyyyy-yyyyy  1/1     Running   0          45s
```

**Check all services:**
```bash
kubectl get svc -n ai-ml-lab-2-2
```

**Expected Output:**
```
NAME              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)             AGE
otel-collector    ClusterIP   10.96.111.222    <none>        4317/TCP,4318/TCP   3m
ai-lab-2-2-paid   ClusterIP   10.96.222.333    <none>        9000/TCP            45s
```

**Check resource usage:**
```bash
kubectl top pod -n ai-ml-lab-2-2
```

**Expected Output (may take a moment to populate):**
```
NAME                              CPU(cores)   MEMORY(bytes)
otel-collector-xxxxxxxxxx-xxxxx   5m           45Mi
ai-lab-2-2-paid-yyyyyyyyyy-yyyyy  8m           120Mi
```

---

### Step 11: View Application Startup Logs

Check that OpenTelemetry initialized correctly:
```bash
kubectl logs -n ai-ml-lab-2-2 -l app=ai-lab-2-2-paid --tail=30
```

**Expected Output:**
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     OpenTelemetry SDK initialized
INFO:     Exporter configured: otlp
INFO:     OTLP endpoint: http://otel-collector:4317
INFO:     Service name: ai-inference-service
INFO:     Tracing enabled: True
INFO:     Metrics enabled: True
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:9000 (Press CTRL+C to quit)
```

**What this validates:**
- ✅ Application started successfully
- ✅ OpenTelemetry SDK initialized
- ✅ Connected to collector at correct endpoint
- ✅ Both tracing and metrics are enabled

---

### Step 12: Set Up Port Forwarding

Forward the application port:
```bash
kubectl port-forward -n ai-ml-lab-2-2 svc/ai-lab-2-2-paid 9002:9000
```

**Expected Output:**
```
Forwarding from 127.0.0.1:9002 -> 9000
Forwarding from [::1]:9002 -> 9000
```

**Keep this terminal open!** Open a new terminal for testing.

---

## ✅ Testing and Validation

### Test 1: Health Check with Tracing Info

Test the health endpoint:
```bash
curl http://localhost:9002/health
```

**Expected Response:**
```json
{
  "status": "ok",
  "env": "local",
  "tracing_enabled": true,
  "collector_endpoint": "http://otel-collector:4317"
}
```

**What this validates:**
- ✅ Application is running and responding
- ✅ OpenTelemetry tracing is enabled
- ✅ Collector endpoint is configured correctly
- ✅ Environment configuration is loaded

---

### Test 2: Make First Prediction with Tracing

Make a prediction request:
```bash
curl -X POST http://localhost:9002/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [0.5, 1.5, 2.0]}'
```

**Expected Response:**
```json
{
  "prediction": 4.0,
  "model_name": "simple-linear-demo",
  "latency_ms": 100,
  "trace_id": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
}
```

**What this validates:**
- ✅ Prediction endpoint is working
- ✅ Model inference is functioning
- ✅ Trace ID is being generated for the request
- ✅ Latency is tracked and returned

**Important:** Note the `trace_id` - this uniquely identifies this request across all systems!

---

### Test 3: Verify Traces in Collector

Check collector logs to see the trace:
```bash
kubectl logs -n ai-ml-lab-2-2 -l app=otel-collector --tail=50 | grep -A10 "Trace"
```

**Expected Output:**
```
2024-01-15T10:35:12.345Z info    LogsExporter    {"kind": "exporter", "data_type": "traces", "name": "logging"}
Trace ID: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
Span ID: b2c3d4e5f6g7h8i9
Parent Span ID: 
Service: ai-inference-service
Operation: POST /predict
Start time: 2024-01-15T10:35:12.100Z
End time: 2024-01-15T10:35:12.200Z
Duration: 100ms
Attributes:
  http.method: POST
  http.route: /predict
  http.status_code: 200
```

**What this validates:**
- ✅ Traces are being sent to collector
- ✅ Collector is receiving and processing traces
- ✅ Span details include timing and attributes
- ✅ End-to-end tracing pipeline is working

---

### Test 4: Verify Metrics in Collector

Check collector logs for metrics:
```bash
kubectl logs -n ai-ml-lab-2-2 -l app=otel-collector --tail=100 | grep -A5 "Metric"
```

**Expected Output:**
```
2024-01-15T10:35:15.678Z info    MetricsExporter {"kind": "exporter", "data_type": "metrics", "name": "logging"}
Metric: http_requests_total
Type: Counter
Value: 1
Labels: {method="POST", endpoint="/predict", status="200"}

Metric: prediction_latency_ms
Type: Histogram
Bucket[0-50ms]: 0
Bucket[50-100ms]: 0
Bucket[100-150ms]: 1
Bucket[150-200ms]: 0
```

**What this validates:**
- ✅ Metrics are being exported
- ✅ Collector is receiving metrics
- ✅ Histogram buckets are working
- ✅ Latency distribution is being tracked

---

### Test 5: Multiple Predictions with Different Traces

Make several predictions and observe different trace IDs:
```bash
for i in {1..5}; do
  echo "Request $i:"
  curl -s -X POST http://localhost:9002/predict \
    -H "Content-Type: application/json" \
    -d "{\"features\": [$i.0, 2.0, 3.0]}" | jq '.trace_id'
  sleep 1
done
```

**Expected Output:**
```
Request 1:
"a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
Request 2:
"b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7"
Request 3:
"c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8"
Request 4:
"d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9"
Request 5:
"e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
```

**What this validates:**
- ✅ Each request gets a unique trace ID
- ✅ Distributed tracing is working correctly
- ✅ Trace context is being propagated
- ✅ Can track individual requests through the system

---

### Test 6: Stream Collector Telemetry in Real-Time

Open a new terminal and stream collector logs:
```bash
kubectl logs -f -n ai-ml-lab-2-2 -l app=otel-collector
```

In another terminal, make requests:
```bash
for i in {1..10}; do
  curl -s -X POST http://localhost:9002/predict \
    -H "Content-Type: application/json" \
    -d '{"features": [1.0, 2.0, 3.0]}' > /dev/null
  sleep 2
done
```

**Expected Output in collector stream:**
```
2024-01-15T10:40:01.123Z info    TracesExporter  {"traces": 1}
2024-01-15T10:40:02.234Z info    MetricsExporter {"metrics": 4}
2024-01-15T10:40:03.345Z info    TracesExporter  {"traces": 1}
2024-01-15T10:40:04.456Z info    MetricsExporter {"metrics": 4}
...
```

**What this validates:**
- ✅ Real-time telemetry streaming works
- ✅ Collector processes data as it arrives
- ✅ Both traces and metrics are being exported
- ✅ Batching is working (multiple metrics per export)

Press `Ctrl+C` to stop streaming.

---

### Test 7: Advanced Load Testing

Navigate to the load generator:
```bash
cd load-generator
```

Install dependencies:
```bash
pip install requests numpy
```

Run the advanced load generator:
```bash
python generate_load.py \
  --url http://localhost:9002 \
  --requests 500 \
  --concurrency 10 \
  --rate 50
```

**Expected Output:**
```
Starting load test...
========================================
Configuration:
  URL: http://localhost:9002/predict
  Total requests: 500
  Concurrency: 10 workers
  Target rate: 50 req/s per worker
  Total expected duration: ~10s
========================================

Progress: [####################] 500/500

Results:
========================================
Total requests:     500
Successful:         500
Failed:             0
Duration:           10.2s
Actual rate:        49.0 req/s

Latency Distribution:
========================================
  Min:              95ms
  Max:              156ms
  Mean:             102ms
  Median (p50):     100ms
  p90:              112ms
  p95:              125ms
  p99:              142ms

Histogram Buckets:
  0-50ms:     ████ 0%
  50-100ms:   ████████████████ 42%
  100-150ms:  ██████████████████████ 56%
  150-200ms:  ██ 2%
  200-250ms:   0%
  250+ms:      0%
========================================
```

**What this validates:**
- ✅ System handles concurrent load gracefully
- ✅ Latency distribution is consistent
- ✅ No errors under sustained load
- ✅ Performance is predictable and reliable

---

### Test 8: Verify Telemetry Under Load

Check application logs during/after load test:
```bash
cd ..
kubectl logs -n ai-ml-lab-2-2 -l app=ai-lab-2-2-paid --tail=20
```

**Expected Output:**
```
INFO:     Prediction request received
INFO:     Trace ID: abc123...
INFO:     Prediction completed - latency: 98ms
INFO:     Prediction request received
INFO:     Trace ID: def456...
INFO:     Prediction completed - latency: 103ms
...
```

Check collector received all the data:
```bash
kubectl logs -n ai-ml-lab-2-2 -l app=otel-collector --tail=50 | grep -E "(Trace|Metric)" | tail -20
```

**Expected Output:**
```
2024-01-15T10:45:10.123Z info    TracesExporter  {"traces": 10}
2024-01-15T10:45:11.234Z info    MetricsExporter {"metrics": 25}
2024-01-15T10:45:12.345Z info    TracesExporter  {"traces": 10}
2024-01-15T10:45:13.456Z info    MetricsExporter {"metrics": 25}
...
```

**What this validates:**
- ✅ All 500 requests were traced
- ✅ Telemetry pipeline handles high throughput
- ✅ No data loss under load
- ✅ Collector batching is efficient

---

### Test 9: Resource Usage Verification

Check resource consumption:
```bash
kubectl top pod -n ai-ml-lab-2-2
```

**Expected Output:**
```
NAME                              CPU(cores)   MEMORY(bytes)
otel-collector-xxxxxxxxxx-xxxxx   15m          62Mi
ai-lab-2-2-paid-yyyyyyyyyy-yyyyy  45m          145Mi
```

**What this validates:**
- ✅ Resource usage is within defined limits
- ✅ No memory leaks or CPU spikes
- ✅ Both services are running efficiently

Compare with resource limits:
```bash
kubectl describe pod -n ai-ml-lab-2-2 -l app=ai-lab-2-2-paid | grep -A5 "Limits"
```

**Expected Output:**
```
    Limits:
      cpu:     500m
      memory:  512Mi
    Requests:
      cpu:     250m
      memory:  256Mi
```

**Analysis:**
- Application using ~45m CPU (well under 500m limit)
- Application using ~145Mi RAM (well under 512Mi limit)
- Still room for traffic growth
- Resource allocation is appropriate

---

### Test 10: Trace Context Propagation

Verify trace context is properly propagated:
```bash
# Make a request and capture the trace ID
TRACE_ID=$(curl -s -X POST http://localhost:9002/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0]}' | jq -r '.trace_id')

echo "Trace ID: $TRACE_ID"

# Search for this trace in collector logs
kubectl logs -n ai-ml-lab-2-2 -l app=otel-collector | grep "$TRACE_ID"
```

**Expected Output:**
```
Trace ID: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
2024-01-15T10:50:00.123Z info    Trace ID: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

**What this validates:**
- ✅ Trace IDs are consistent between app and collector
- ✅ Trace context propagation works correctly
- ✅ Can correlate app responses with telemetry data

---

### Test 11: Error Handling and Tracing

Test error scenarios:
```bash
# Invalid input
curl -X POST http://localhost:9002/predict \
  -H "Content-Type: application/json" \
  -d '{"invalid": "data"}'
```

**Expected Response:**
```json
{
  "detail": [
    {
      "loc": ["body", "features"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

Check if errors are traced:
```bash
kubectl logs -n ai-ml-lab-2-2 -l app=otel-collector --tail=20 | grep -i error
```

**What this validates:**
- ✅ Errors are handled gracefully
- ✅ Error traces are captured
- ✅ Can debug issues using traces

---

### Test 12: Collector Health Check

Verify collector is healthy:
```bash
kubectl get pods -n ai-ml-lab-2-2 -l app=otel-collector
```

**Expected Output:**
```
NAME                              READY   STATUS    RESTARTS   AGE
otel-collector-xxxxxxxxxx-xxxxx   1/1     Running   0          15m
```

Check collector endpoints:
```bash
kubectl exec -n ai-ml-lab-2-2 -l app=otel-collector -- wget -q -O- http://localhost:13133
```

**Expected Output:**
```
{"status":"Server available","upSince":"2024-01-15T10:30:00.123Z","uptime":"15m"}
```

**What this validates:**
- ✅ Collector health endpoint is working
- ✅ Collector has been running stably
- ✅ No restarts or crashes

---

## 🎓 Understanding What You've Built

### OpenTelemetry Architecture

**1. Application Instrumentation:**
- FastAPI automatically instrumented with OpenTelemetry
- Custom spans for model inference
- Metrics for request counting and latency histograms
- Automatic trace context propagation

**2. OTLP Export:**
- Traces and metrics exported via OTLP protocol
- gRPC communication on port 4317
- Efficient binary format
- Batching for performance

**3. Collector Pipeline:**
```
Receivers → Processors → Exporters
   ↓            ↓            ↓
  OTLP       Batch       Logging
             Memory      (stdout)
                        [Future: Prometheus, Jaeger, etc.]
```

**4. Namespace Isolation:**
- Dedicated namespace for clear separation
- Resource quotas prevent resource exhaustion
- Network policies (can be added)
- RBAC for security (can be added)

### Production Observability Concepts

**Distributed Tracing:**
- Each request gets a unique trace ID
- Spans represent units of work
- Parent-child relationships show call hierarchy
- Latency attribution shows bottlenecks

**Metric Types:**
- **Counters:** Total requests, predictions
- **Histograms:** Latency distribution in buckets
- **Gauges:** Active connections, current load

**Why This Matters for AI/ML:**
- Model inference latency is variable
- Need percentiles (p50, p90, p99), not just averages
- Trace entire request from input to prediction
- Identify bottlenecks (preprocessing vs. model vs. postprocessing)
- Cost attribution per request

### Cloud Cost Analysis

**Running in Cloud (Estimated Monthly Cost):**

```
Application Pod (250m CPU, 256Mi RAM):
  - On-demand: $4-5/month
  - Spot/preemptible: $1-2/month

Collector Pod (100m CPU, 128Mi RAM):
  - On-demand: $2-3/month
  - Spot/preemptible: $0.50-1/month

Data Egress (minimal):
  - Collector logs: <$1/month
  
Load Balancer (optional):
  - $3-5/month

Total: $7-12/month (on-demand)
Total: $2-4/month (spot instances)
```

**Cost Optimization Tips:**
1. Use spot/preemptible instances (60-80% savings)
2. Right-size resources based on actual usage
3. Implement trace sampling (sample 10% of traces)
4. Use local storage instead of cloud storage
5. Batch metrics before export

**FREE in KIND:**
- This lab: $0/month
- Perfect for dev, testing, CI/CD
- Scale to cloud when needed

---

## 📊 Success Criteria Checklist

Your lab is complete when:

- [ ] kind cluster is running
- [ ] Namespace `ai-ml-lab-2-2` exists
- [ ] OpenTelemetry Collector pod is Running
- [ ] Application pod is Running
- [ ] Both services are accessible
- [ ] Health endpoint returns JSON with `tracing_enabled: true`
- [ ] Predictions return results with unique `trace_id`
- [ ] Collector logs show traces being received
- [ ] Collector logs show metrics being received
- [ ] Load test completes with 0 failures
- [ ] Resource usage is within limits
- [ ] Application logs show OpenTelemetry initialization
- [ ] Trace IDs match between app and collector
- [ ] You understand the observability architecture
- [ ] You can explain OTLP pipeline flow

---

## 🧹 Cleanup

### Delete All Resources

Quick cleanup (deletes everything):
```bash
kubectl delete namespace ai-ml-lab-2-2
```

**Expected Output:**
```
namespace "ai-ml-lab-2-2" deleted
```

Verify namespace is gone:
```bash
kubectl get namespace ai-ml-lab-2-2
```

**Expected Output:**
```
Error from server (NotFound): namespaces "ai-ml-lab-2-2" not found
```

### Alternative: Individual Deletion

If you prefer to delete resources individually:
```bash
kubectl delete -f k8s/service.yaml
kubectl delete -f k8s/deployment.yaml
kubectl delete -f k8s/collector-deployment.yaml
kubectl delete -f k8s/collector-config.yaml
kubectl delete -f k8s/namespace.yaml
```

### Delete kind Cluster

```bash
kind delete cluster --name mcp-cluster
```

**Expected Output:**
```
Deleting cluster "mcp-cluster" ...
Deleted nodes: ["mcp-cluster-control-plane"]
```

Verify:
```bash
kind get clusters
```

**Expected Output:**
```
No kind clusters found.
```

---

## 🔧 Troubleshooting

### Issue: Collector Pod Not Starting

**Symptom:**
```bash
kubectl get pods -n ai-ml-lab-2-2
# Shows: CrashLoopBackOff or Error
```

**Solution:**
```bash
# Check pod events
kubectl describe pod -n ai-ml-lab-2-2 -l app=otel-collector

# Check logs
kubectl logs -n ai-ml-lab-2-2 -l app=otel-collector

# Common fix: Verify ConfigMap exists
kubectl get configmap -n ai-ml-lab-2-2 otel-collector-config

# If missing, reapply:
kubectl apply -f k8s/collector-config.yaml
kubectl delete pod -n ai-ml-lab-2-2 -l app=otel-collector
```

---

### Issue: Application Not Sending Telemetry

**Symptom:**
Collector logs show no traces or metrics

**Solution:**
```bash
# Check application logs for OTel errors
kubectl logs -n ai-ml-lab-2-2 -l app=ai-lab-2-2-paid | grep -i otel

# Verify environment variables
kubectl describe pod -n ai-ml-lab-2-2 -l app=ai-lab-2-2-paid | grep -A10 "Environment"

# Test connectivity from app to collector
kubectl exec -n ai-ml-lab-2-2 -l app=ai-lab-2-2-paid -- nc -zv otel-collector 4317

# Expected: Connection to otel-collector 4317 port [tcp/*] succeeded!
```

---

### Issue: Traces Missing trace_id

**Symptom:**
Prediction response doesn't include trace_id

**Solution:**
```bash
# Check if tracing is enabled
curl http://localhost:9002/health | jq '.tracing_enabled'

# Should return: true

# If false, check .env file configuration
kubectl exec -n ai-ml-lab-2-2 -l app=ai-lab-2-2-paid -- cat .env | grep OTEL

# Rebuild and redeploy if needed
docker build -t ai-lab-2-2-paid:v1 .
kind load docker-image ai-lab-2-2-paid:v1 --name mcp-cluster
kubectl delete pod -n ai-ml-lab-2-2 -l app=ai-lab-2-2-paid
```

---

### Issue: High Resource Usage

**Symptom:**
```bash
kubectl top pod -n ai-ml-lab-2-2
# Shows CPU or Memory near limits
```

**Solution:**
```bash
# Check for resource throttling
kubectl describe pod -n ai-ml-lab-2-2 -l app=ai-lab-2-2-paid | grep -i throttl

# Increase limits if needed (edit k8s/deployment.yaml):
resources:
  limits:
    cpu: "1000m"
    memory: "1Gi"

# Reapply
kubectl apply -f k8s/deployment.yaml
```

---

### Issue: Port Forward Connection Refused

**Symptom:**
```bash
curl http://localhost:9002/health
# curl: (7) Failed to connect
```

**Solution:**
```bash
# Check if port-forward is running
ps aux | grep "port-forward"

# If not running, restart it
kubectl port-forward -n ai-ml-lab-2-2 svc/ai-lab-2-2-paid 9002:9000

# Try different port if 9002 is in use
kubectl port-forward -n ai-ml-lab-2-2 svc/ai-lab-2-2-paid 9003:9000
curl http://localhost:9003/health
```

---

### Issue: Collector Logs Too Verbose

**Symptom:**
Collector logs filling up with too much detail

**Solution:**
```bash
# Filter for important information only
kubectl logs -n ai-ml-lab-2-2 -l app=otel-collector | grep -E "(ERROR|WARN|Trace|Metric)"

# Or tail specific number of lines
kubectl logs -n ai-ml-lab-2-2 -l app=otel-collector --tail=50
```

---

## 📚 Next Steps

### Production Enhancements

**1. Export to Real Backends:**

Edit `k8s/collector-config.yaml` to add exporters:

```yaml
exporters:
  prometheus:
    endpoint: "0.0.0.0:8889"
  
  jaeger:
    endpoint: "jaeger-collector:14250"
    tls:
      insecure: true
  
  otlp/datadog:
    endpoint: "https://api.datadoghq.com"
    headers:
      DD-API-KEY: "${DD_API_KEY}"
```

**2. Add Trace Sampling:**

```yaml
processors:
  probabilistic_sampler:
    sampling_percentage: 10  # Sample 10% of traces
  
  tail_sampling:
    decision_wait: 10s
    policies:
      - name: errors
        type: status_code
        status_code: {status_codes: [ERROR]}
```

**3. Implement Alerting:**

Set up alerts based on metrics:
- Latency p99 > 200ms
- Error rate > 1%
- Request rate > 1000 req/s

**4. Add Custom Metrics:**

Instrument your code with custom metrics:
```python
from opentelemetry import metrics

meter = metrics.get_meter(__name__)
prediction_counter = meter.create_counter(
    "predictions.by_model",
    description="Predictions grouped by model"
)
```

### Advanced Topics

- **Service Mesh Integration** - Istio for automatic tracing
- **Multi-service Tracing** - Trace across microservices
- **Grafana Dashboards** - Visualize metrics
- **Jaeger UI** - Browse and analyze traces
- **Log Correlation** - Connect logs with trace IDs

---

## 🎉 Congratulations!

You've successfully completed the PAID version of Lab 2.2!

### What You've Mastered:

✅ **OpenTelemetry Integration** - Industry-standard observability  
✅ **Distributed Tracing** - Track requests with unique trace IDs  
✅ **OTLP Pipelines** - Export telemetry to collectors  
✅ **Production Architecture** - Namespaces, resources, configuration  
✅ **Histogram Metrics** - Accurate latency distribution analysis  
✅ **Cost Optimization** - Deploy affordably (<$10/month)  
✅ **Debugging Skills** - Use traces and metrics to find issues  

### Real-World Applications:

This architecture is used by companies like:
- Netflix (distributed tracing for microservices)
- Uber (request tracking across services)
- Airbnb (ML model performance monitoring)
- Spotify (observability for recommendation systems)

You're now equipped to implement production-grade observability for AI/ML systems!

Happy learning! 🚀📊🔍