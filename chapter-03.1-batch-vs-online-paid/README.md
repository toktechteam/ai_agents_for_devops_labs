# Lab 3.1 PAID Version – Production-Grade Batch Inference
## Enterprise Batch Inference with OpenTelemetry & Cost Insights

---

## 🎯 What You Will Learn

### Core Concepts

By completing this lab, you will master:

1. **Production Batch Inference Patterns** - How enterprise ML systems run batch workloads:
   - Full observability stack integration
   - Cost tracking and optimization
   - Resource constraint management
   - Performance monitoring at scale

2. **OpenTelemetry for Batch Workloads** - Industry-standard observability:
   - Distributed tracing for batch jobs
   - Metrics collection (records processed, latency, costs)
   - Integration with OpenTelemetry Collector
   - Exporting telemetry for analysis

3. **Cost Modeling for Batch AI** - Financial intelligence built-in:
   - Per-record cost calculation
   - Batch-level cost estimation
   - CPU utilization cost attribution
   - Cost optimization strategies

4. **Resource Management** - Production-grade controls:
   - CPU throttling configuration
   - Memory constraints
   - Execution time limits
   - Cost vs. speed tradeoffs

### Practical Skills

You will be able to:

- ✅ Build enterprise-grade batch inference pipelines
- ✅ Implement OpenTelemetry in batch workloads
- ✅ Track and optimize batch processing costs
- ✅ Monitor record-level and batch-level performance
- ✅ Configure resource constraints for cost control
- ✅ Deploy production-ready CronJobs with observability
- ✅ Export telemetry to observability backends
- ✅ Debug batch job performance issues

### Real-World Applications

**ML Platform Engineers** will learn:
- How to standardize observability across batch ML pipelines
- Cost attribution for ML workloads
- Production deployment patterns for batch inference

**FinOps Teams** will learn:
- How to track ML inference costs per record
- Resource optimization for batch workloads
- Cost modeling for capacity planning

**SREs** will learn:
- How to monitor batch job health
- Setting up alerts for batch failures
- Performance troubleshooting with traces

**Data Engineers** will learn:
- Integrating observability into data pipelines
- Batch processing performance optimization
- Cost-aware pipeline design

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
- Completion of Lab 3.1 FREE version (or equivalent batch job knowledge)
- Basic understanding of OpenTelemetry concepts
- Familiarity with Kubernetes Jobs and CronJobs
- Understanding of resource requests and limits

### Recommended Reading
- OpenTelemetry for batch processing
- Kubernetes resource management
- Cloud cost optimization for ML workloads

---

## 🏗️ Architecture Overview

### What You're Building

```
┌─────────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                            │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │         Namespace: ai-ml-lab-3-1-paid                     │  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────────────┐    │  │
│  │  │  Batch Inference Job                             │    │  │
│  │  │  ┌──────────────────────────────────────────┐   │    │  │
│  │  │  │  Pod: batch-inference-paid-xxxxx         │   │    │  │
│  │  │  │                                           │   │    │  │
│  │  │  │  1. Initialize OpenTelemetry SDK         │   │    │  │
│  │  │  │  2. Read input.jsonl                     │   │    │  │
│  │  │  │  3. For each record:                     │   │    │  │
│  │  │  │     ├─ Create trace span                 │   │    │  │
│  │  │  │     ├─ Compute prediction                │   │    │  │
│  │  │  │     ├─ Track latency                     │   │    │  │
│  │  │  │     ├─ Calculate cost                    │   │    │  │
│  │  │  │     └─ Export metrics                    │   │    │  │
│  │  │  │  4. Generate batch summary               │   │    │  │
│  │  │  │  5. Export telemetry to collector        │   │    │  │
│  │  │  │  6. Exit (Status: Completed)             │   │    │  │
│  │  │  │                                           │   │    │  │
│  │  │  │  Resource Limits:                        │   │    │  │
│  │  │  │  - CPU: 500m (throttled for cost)       │   │    │  │
│  │  │  │  - Memory: 512Mi                         │   │    │  │
│  │  │  └──────────────────────────────────────────┘   │    │  │
│  │  │                       │                          │    │  │
│  │  │                       │ OTLP                     │    │  │
│  │  │                       ▼                          │    │  │
│  │  │  ┌──────────────────────────────────────────┐   │    │  │
│  │  │  │  OpenTelemetry Collector                 │   │    │  │
│  │  │  │                                           │   │    │  │
│  │  │  │  Receivers:                               │   │    │  │
│  │  │  │  - OTLP (gRPC: 4317, HTTP: 4318)        │   │    │  │
│  │  │  │                                           │   │    │  │
│  │  │  │  Processors:                              │   │    │  │
│  │  │  │  - Batch (optimize exports)              │   │    │  │
│  │  │  │  - Memory limiter                        │   │    │  │
│  │  │  │                                           │   │    │  │
│  │  │  │  Exporters:                               │   │    │  │
│  │  │  │  - Logging (stdout)                      │   │    │  │
│  │  │  │  - [Future: Prometheus, Jaeger, etc.]   │   │    │  │
│  │  │  └──────────────────────────────────────────┘   │    │  │
│  │  └──────────────────────────────────────────────────┘    │  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────────────┐    │  │
│  │  │  CronJob (Scheduled Batch Processing)            │    │  │
│  │  │  Schedule: "*/10 * * * *" (every 10 minutes)    │    │  │
│  │  │  Creates Jobs → Same flow as above               │    │  │
│  │  └──────────────────────────────────────────────────┘    │  │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Observability Data Flow

```
Batch Job
    ↓
[Trace Spans] → Per-record processing spans with timing
[Metrics]     → Records processed, latency histogram, cost
[Logs]        → Structured logs with trace IDs
    ↓
OTLP Protocol (gRPC/HTTP)
    ↓
OpenTelemetry Collector
    ↓
Processors (Batch, Filter, Enrich)
    ↓
Exporters
    ├─ Stdout (for this lab)
    ├─ Prometheus (production)
    ├─ Jaeger (production)
    └─ Cloud providers (production)
```

---

## 🆚 FREE vs PAID Comparison

| Feature | FREE Version | PAID Version |
|---------|-------------|--------------|
| **Batch Inference** | ✅ Basic | ✅ Production-grade |
| **Kubernetes Jobs** | ✅ Simple | ✅ With resource limits |
| **CronJobs** | ✅ Basic schedule | ✅ With retry policies |
| **Logging** | ✅ Stdout only | ✅ Structured + trace IDs |
| **OpenTelemetry Traces** | ❌ | ✅ Per-record spans |
| **OpenTelemetry Metrics** | ❌ | ✅ Comprehensive metrics |
| **Cost Modeling** | ❌ | ✅ Per-record cost tracking |
| **CPU Throttling** | ❌ | ✅ Configurable limits |
| **OTel Collector** | ❌ | ✅ Included & configured |
| **Resource Management** | ❌ Basic | ✅ Requests & limits |
| **Observability Export** | ❌ | ✅ To collector |
| **Production Ready** | Learning only | ✅ Yes |

---

## 📁 Repository Structure

```
lab-03.1-batch-vs-online-paid/
├── README.md                       ← This file
├── setup.md                        ← Detailed setup guide
├── kind-mcp-cluster.yaml           ← Cluster configuration
├── Dockerfile                      ← Container image definition
├── .env.example                    ← Environment configuration
├── app/
│   ├── batch_job.py                ← Batch inference with OTel
│   ├── config.py                   ← Configuration management
│   ├── cost_model.py               ← Cost calculation logic
│   ├── requirements.txt            ← Python dependencies
│   ├── data/
│   │   └── input.jsonl             ← Sample dataset
│   └── tests/
│       └── test_batch_job.py       ← Unit tests
└── k8s/
    ├── namespace.yaml              ← Namespace isolation
    ├── otel-collector-config.yaml  ← Collector ConfigMap
    ├── otel-collector-deploy.yaml  ← Collector deployment
    ├── job-batch-once.yaml         ← One-time batch job
    └── cronjob-batch.yaml          ← Scheduled batch job
```

---

## 🚀 Quick Start Guide

### Step 1: Navigate to Lab Directory

```bash
cd lab-03.1-batch-vs-online-paid
```

### Step 2: Configure Environment

```bash
cp .env.example .env
```

Review configuration:
```bash
cat .env
```

**Key settings:**
```bash
# OpenTelemetry
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector-paid:4317
OTEL_SERVICE_NAME=batch-inference-service

# Cost modeling
COST_PER_CPU_HOUR=0.04        # $0.04 per CPU-hour
COST_PER_MEMORY_GB_HOUR=0.005 # $0.005 per GB-hour

# Resource throttling
CPU_LIMIT=500m                 # Throttle to 0.5 CPU
MEMORY_LIMIT=512Mi
```

### Step 3: Create kind Cluster

```bash
kind create cluster --config kind-mcp-cluster.yaml
kubectl get nodes
```

### Step 4: Build Docker Image

```bash
docker build -t ai-lab-3-1-paid:v1 .
```

### Step 5: Load Image into kind

```bash
kind load docker-image ai-lab-3-1-paid:v1 --name mcp-cluster
```

### Step 6: Deploy All Resources

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Deploy OpenTelemetry Collector
kubectl apply -f k8s/otel-collector-config.yaml
kubectl apply -f k8s/otel-collector-deploy.yaml

# Deploy batch jobs
kubectl apply -f k8s/job-batch-once.yaml
kubectl apply -f k8s/cronjob-batch.yaml
```

### Step 7: Verify Deployment

```bash
kubectl get all -n ai-ml-lab-3-1-paid
```

### Step 8: View Batch Job Output

```bash
kubectl logs -n ai-ml-lab-3-1-paid -l app=batch-inference-paid
```

**Expected Output:**
```json
{"level": "INFO", "message": "Starting batch inference job", "trace_id": "abc123..."}
{"id": 1, "prediction": 6.0, "latency_ms": 45, "cost_usd": 0.0001, "trace_id": "def456..."}
{"id": 2, "prediction": 15.0, "latency_ms": 48, "cost_usd": 0.0001, "trace_id": "ghi789..."}
{"summary": {
  "total_records": 2,
  "avg_prediction": 10.5,
  "total_latency_ms": 93,
  "avg_latency_ms": 46.5,
  "total_cost_usd": 0.0002,
  "cost_per_record_usd": 0.0001
}}
```

### Step 9: View OpenTelemetry Collector Logs

```bash
kubectl logs -n ai-ml-lab-3-1-paid deploy/otel-collector-paid
```

**Expected Output:**
```
2024-01-15T10:30:00.123Z info    TracesExporter  {"traces": 2}
2024-01-15T10:30:01.234Z info    MetricsExporter {"metrics": 6}

Trace details:
  Service: batch-inference-service
  Span: process_record
  Duration: 45ms
  Attributes:
    record_id: 1
    prediction: 6.0
    cost_usd: 0.0001

Metrics:
  batch_total_records: 2
  batch_processing_ms: 93
  record_latency_ms (histogram):
    - Bucket[0-50ms]: 2
    - Bucket[50-100ms]: 0
  batch_cost_usd: 0.0002
```

---

## 📊 Understanding Production Features

### OpenTelemetry Integration

**1. Trace Spans:**
Every record gets its own span:
```python
with tracer.start_as_current_span("process_record") as span:
    span.set_attribute("record.id", record_id)
    span.set_attribute("prediction", prediction)
    span.set_attribute("cost_usd", cost)
```

**2. Metrics Exported:**
- `batch_total_records` (Counter) - Total records processed
- `record_latency_ms` (Histogram) - Per-record latency distribution
- `batch_processing_ms` (Gauge) - Total batch processing time
- `batch_cost_usd` (Gauge) - Total batch cost
- `cost_per_record_usd` (Gauge) - Average cost per record

**3. Structured Logs:**
All logs include trace IDs for correlation:
```json
{
  "level": "INFO",
  "message": "Record processed",
  "record_id": 1,
  "trace_id": "abc123...",
  "span_id": "def456..."
}
```

### Cost Modeling

**Per-Record Cost Calculation:**
```python
# CPU cost
cpu_time_seconds = record_latency_ms / 1000
cpu_cost = (cpu_limit_cores * COST_PER_CPU_HOUR * cpu_time_seconds) / 3600

# Memory cost
memory_gb = memory_limit_bytes / (1024**3)
memory_cost = (memory_gb * COST_PER_MEMORY_GB_HOUR * cpu_time_seconds) / 3600

# Total cost per record
total_cost = cpu_cost + memory_cost
```

**Cost Tracking:**
- Real-time cost calculation per record
- Batch-level cost aggregation
- Cost exported as metrics
- Cost optimization recommendations

### Resource Management

**CPU Throttling:**
```yaml
resources:
  requests:
    cpu: "250m"      # Guaranteed minimum
    memory: "256Mi"
  limits:
    cpu: "500m"      # Throttled maximum (cost control)
    memory: "512Mi"   # OOM protection
```

**Why Throttle?**
- **Cost Control:** Lower CPU = lower cost
- **Predictability:** Consistent execution time
- **Fairness:** Share cluster resources
- **Optimization:** Force efficient code

---

## 🧪 Running Unit Tests

From the `app/` directory:

```bash
cd app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

**Expected Output:**
```
================== test session starts ==================
collected 3 items

tests/test_batch_job.py::test_batch_inference PASSED     [33%]
tests/test_batch_job.py::test_cost_calculation PASSED    [66%]
tests/test_batch_job.py::test_telemetry_export PASSED    [100%]

=================== 3 passed in 0.15s ===================
```

---

## 💰 Cost Analysis

### Running in KIND: $0/month

This lab runs locally with zero cloud costs.

### Cloud Deployment Cost Modeling

**Scenario:** CronJob runs every hour (24 times/day)

**Job Specifications:**
- Runtime: 2 minutes per execution
- CPU: 0.5 cores (throttled)
- Memory: 512Mi
- Records processed: 1,000 per run

**Monthly Calculation:**
```
Executions per month: 24/day × 30 days = 720 jobs
Total runtime: 720 × 2 min = 1,440 min = 24 hours

Compute cost:
  CPU: 0.5 cores × 24 hours × $0.04/core-hour = $0.48
  Memory: 0.5 GB × 24 hours × $0.005/GB-hour = $0.06
  Total compute: $0.54

Storage (logs, minimal): $0.10
Collector overhead: $0.20

Total: ~$0.84/month
```

**Per-Record Cost:**
```
Total records/month: 720 jobs × 1,000 records = 720,000 records
Cost per record: $0.84 / 720,000 = $0.0000012 per record
Cost per 1M records: $1.20
```

### Cost Optimization Strategies

**1. Adjust CPU Throttling:**
```yaml
# Slower but cheaper
cpu: "250m"  # Cost: ~$0.27/month (50% savings)

# Faster but more expensive
cpu: "1000m" # Cost: ~$0.96/month (80% increase)
```

**2. Optimize Schedule:**
```yaml
# Every hour (expensive)
schedule: "0 * * * *"  # 720 jobs/month

# Every 6 hours (75% savings)
schedule: "0 */6 * * *"  # 120 jobs/month

# Daily at 2 AM (97% savings)
schedule: "0 2 * * *"  # 30 jobs/month
```

**3. Batch More Records:**
```
1,000 records/job → $0.0000012 per record
10,000 records/job → $0.00000012 per record (90% savings!)
```

**4. Use Spot Instances:**
```
Regular: $0.84/month
Spot/Preemptible: $0.17/month (80% savings)
```

---

## 🎓 Key Learning Outcomes

### Conceptual Understanding

After completing this lab, you understand:

✅ **Enterprise Batch Observability:**
- How to instrument batch jobs with OpenTelemetry
- Difference between API and batch observability patterns
- Importance of per-record vs batch-level metrics

✅ **Cost Attribution for ML:**
- How to calculate per-record inference costs
- Impact of resource limits on costs
- Cost optimization strategies for batch workloads

✅ **Production Deployment Patterns:**
- Resource management for batch jobs
- Observability collector architecture
- Telemetry export and aggregation

✅ **Performance vs Cost Tradeoffs:**
- How CPU throttling affects cost and speed
- When to optimize for cost vs latency
- Right-sizing batch workloads

### Technical Skills

You can now:

✅ **Implement OpenTelemetry in batch jobs**
✅ **Calculate and track inference costs**
✅ **Configure resource constraints for cost control**
✅ **Export telemetry to collectors**
✅ **Monitor batch job performance**
✅ **Debug batch issues using traces**
✅ **Optimize batch workloads for cost**

### Production Patterns

You've learned:

✅ **Cost-aware engineering** - Building with cost as a first-class concern
✅ **Observability-driven development** - Using telemetry to optimize
✅ **Resource management** - Balancing cost, speed, and reliability
✅ **Enterprise monitoring** - Full-stack observability for batch jobs

---

## 🔧 Troubleshooting

### Issue: Collector Not Receiving Data

**Check collector status:**
```bash
kubectl logs -n ai-ml-lab-3-1-paid deploy/otel-collector-paid
```

**Test connectivity:**
```bash
kubectl exec -n ai-ml-lab-3-1-paid -l app=batch-inference-paid -- nc -zv otel-collector-paid 4317
```

**Verify configuration:**
```bash
kubectl get configmap -n ai-ml-lab-3-1-paid otel-collector-config -o yaml
```

### Issue: Cost Calculations Seem Wrong

**Check environment variables:**
```bash
kubectl describe pod -n ai-ml-lab-3-1-paid -l app=batch-inference-paid | grep -A10 "Environment"
```

**Verify cost parameters:**
- `COST_PER_CPU_HOUR` - Should match cloud pricing
- `COST_PER_MEMORY_GB_HOUR` - Should match cloud pricing
- `CPU_LIMIT` - Should match resource limits

### Issue: Job Runs Slower Than Expected

**Check if CPU throttled:**
```bash
kubectl top pod -n ai-ml-lab-3-1-paid
```

**Review resource limits:**
```bash
kubectl describe pod -n ai-ml-lab-3-1-paid -l app=batch-inference-paid | grep -A5 "Limits"
```

**Consider increasing CPU limit:**
```yaml
limits:
  cpu: "1000m"  # Double the CPU
```

---

## 🧹 Cleanup

### Remove All Resources

```bash
kubectl delete namespace ai-ml-lab-3-1-paid
```

### Delete kind Cluster

```bash
kind delete cluster --name mcp-cluster
```

---

## 📚 Next Steps

### Production Enhancements

**1. Export to Real Backends:**
```yaml
exporters:
  prometheus:
    endpoint: "prometheus:9090"
  jaeger:
    endpoint: "jaeger:14250"
  otlp/datadog:
    endpoint: "https://api.datadoghq.com"
```

**2. Add Cost Alerting:**
- Alert when cost per record exceeds threshold
- Daily/weekly cost reports
- Budget tracking and forecasting

**3. Implement Dynamic Scaling:**
- Adjust CPU based on workload size
- Scale horizontally for large batches
- Auto-tune resource limits

**4. Add Persistent Storage:**
- Save predictions to S3/GCS
- Database integration
- Data versioning

---

## 🎉 Congratulations!

You've completed Lab 3.1 PAID Version!

### What You've Mastered:

✅ **Production Batch Observability** - Enterprise-grade monitoring  
✅ **Cost-Aware ML Engineering** - Financial intelligence in code  
✅ **OpenTelemetry Integration** - Industry-standard telemetry  
✅ **Resource Optimization** - Cost vs performance tradeoffs  
✅ **Enterprise Patterns** - Real-world production deployments  

### Real-World Impact:

These skills are used by:
- **Major tech companies** for cost optimization
- **FinOps teams** for ML cost attribution
- **Platform teams** for standardized observability
- **ML engineers** for performance optimization

You now have production-grade batch ML skills!

Happy learning! 🚀💰📊