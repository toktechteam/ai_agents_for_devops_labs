# PAID Version – Production Observability for AI Inference Lab

This is the **PAID version** of Lab 2.2, teaching DevOps engineers how to implement production-grade observability for AI inference services using OpenTelemetry.

## What You'll Learn

- Implementing OpenTelemetry tracing and metrics
- Setting up an OTLP pipeline to OpenTelemetry Collector
- Creating rich metrics with histogram buckets for latency distribution
- Debugging latency issues in ML inference services
- Reasoning about observability costs in cloud environments
- Production-ready namespace isolation and resource management

---

## Prerequisites

**Operating System:**
- Ubuntu 22.04 (or similar Linux / WSL2 / macOS)

**Required Software:**
- Docker 24+
- kind (Kubernetes in Docker)
- kubectl ≥ 1.29
- Python 3.11+
- Git

**Basic Familiarity With:**
- OpenTelemetry concepts (traces, spans, metrics)
- Kubernetes ConfigMaps and namespaces
- Resource requests and limits
- Observability pipelines

---

## Repository Structure

```
paid/
├── app/
│   ├── main.py              # FastAPI app with OpenTelemetry
│   ├── config.py            # Configuration management
│   ├── requirements.txt     # Python dependencies
│   └── tests/
│       └── test_app.py      # Unit tests
├── k8s/
│   ├── namespace.yaml       # Dedicated namespace
│   ├── collector-config.yaml    # OTel Collector configuration
│   ├── collector-deployment.yaml # OTel Collector deployment
│   ├── deployment.yaml      # Application deployment
│   └── service.yaml         # Kubernetes service
├── load-generator/
│   └── generate_load.py     # Advanced load testing script
├── .env.example             # Example environment config
└── Dockerfile               # Container image definition
```

---

## Production Features

The PAID version includes:

✅ **OpenTelemetry Tracing** - Full distributed tracing support  
✅ **OpenTelemetry Metrics** - Rich metrics with histograms  
✅ **OTLP Pipeline** - Export to OpenTelemetry Collector  
✅ **Latency Histograms** - Bucket-based latency tracking  
✅ **Advanced Load Generator** - Realistic traffic patterns  
✅ **Namespace Isolation** - Dedicated `ai-ml-lab-2-2` namespace  
✅ **Resource Management** - Proper requests and limits  
✅ **Cost Optimization** - Designed for <$10/month in cloud  

---

## Quick Start Guide

### Step 1: Create kind Cluster

From the parent directory:

```bash
kind create cluster --config kind-mcp-cluster.yaml
```

Verify the cluster is running:

```bash
kubectl get nodes
```

### Step 2: Configure Environment

From the `paid/` directory:

```bash
cp .env.example .env
```

Edit `.env` to customize configuration:

```bash
# Application environment
APP_ENV=local

# OpenTelemetry settings
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
OTEL_SERVICE_NAME=ai-inference-service

# Model configuration
DEFAULT_LATENCY_MS=100
MAX_BATCH_SIZE=32
```

### Step 3: Build Docker Image

```bash
docker build -t ai-lab-2-2-paid:v1 .
```

### Step 4: Load Image into kind

```bash
kind load docker-image ai-lab-2-2-paid:v1 --name mcp-cluster
```

### Step 5: Deploy OpenTelemetry Collector

Deploy the namespace and collector first:

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Deploy collector configuration
kubectl apply -f k8s/collector-config.yaml

# Deploy collector
kubectl apply -f k8s/collector-deployment.yaml
```

Verify collector is running:

```bash
kubectl get pods -n ai-ml-lab-2-2
```

Expected output:

```
NAME                              READY   STATUS    RESTARTS   AGE
otel-collector-xxxxxxxxxx-xxxxx   1/1     Running   0          30s
```

### Step 6: Deploy Application

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Check deployment status:

```bash
kubectl get pods -n ai-ml-lab-2-2
kubectl get svc -n ai-ml-lab-2-2
```

---

## Testing Observability Features

### Access the Application

Port-forward the service:

```bash
kubectl port-forward -n ai-ml-lab-2-2 svc/ai-lab-2-2-paid 9002:9000
```

### Health Check

```bash
curl http://localhost:9002/health
```

Expected response:

```json
{
  "status": "ok",
  "env": "local",
  "tracing_enabled": true
}
```

### Make Prediction Requests

```bash
curl -X POST http://localhost:9002/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [0.5, 1.5, 2.0]}'
```

Expected response:

```json
{
  "prediction": 4.0,
  "model_name": "simple-linear-demo",
  "latency_ms": 100,
  "trace_id": "abc123..."
}
```

---

## Viewing Traces and Metrics

### View Collector Logs

Check what the OpenTelemetry Collector is receiving:

```bash
kubectl logs -n ai-ml-lab-2-2 deploy/otel-collector
```

You should see:

```
2024-01-15T10:30:45.123Z info    TracesExporter  {"kind": "exporter", "traces": 5}
2024-01-15T10:30:46.456Z info    MetricsExporter {"kind": "exporter", "metrics": 12}
```

### View Application Logs

```bash
kubectl logs -n ai-ml-lab-2-2 deploy/ai-lab-2-2-paid
```

Look for OpenTelemetry initialization:

```
INFO:     OpenTelemetry initialized
INFO:     Exporting to: http://otel-collector:4317
INFO:     Tracing enabled: true
```

### Stream Real-Time Logs

```bash
kubectl logs -f -n ai-ml-lab-2-2 deploy/ai-lab-2-2-paid
```

---

## Advanced Load Testing

### Using the Rich Load Generator

The PAID version includes an advanced load generator with:

- Configurable request rates
- Latency histogram tracking
- Concurrent request support
- Detailed statistics

From the `paid/load-generator/` directory:

```bash
# Install dependencies
pip install requests numpy

# Run load generator
python generate_load.py \
  --url http://localhost:9002 \
  --requests 500 \
  --concurrency 10 \
  --rate 50
```

Options:

- `--requests` - Total number of requests
- `--concurrency` - Number of concurrent workers
- `--rate` - Requests per second (per worker)

Expected output:

```
Starting load test...
URL: http://localhost:9002/predict
Total requests: 500
Concurrency: 10
Target rate: 50 req/s per worker

Progress: [####################] 500/500

Results:
========================================
Total requests:     500
Successful:         500
Failed:             0
Duration:           10.2s
Actual rate:        49.0 req/s

Latency Distribution:
  Min:              45ms
  Max:              156ms
  Mean:             98ms
  Median (p50):     95ms
  p90:              112ms
  p95:              125ms
  p99:              142ms

Histogram:
  0-50ms:     ████████ 12%
  50-100ms:   ████████████████████████ 62%
  100-150ms:  ████████████ 24%
  150-200ms:  ██ 2%
```

### Observe Metrics During Load Test

In another terminal, watch collector logs:

```bash
kubectl logs -f -n ai-ml-lab-2-2 deploy/otel-collector | grep -i metric
```

---

## Understanding OpenTelemetry Integration

### Tracing

Each prediction request creates a trace with spans:

```
Trace: abc123-def456-ghi789
├─ Span: HTTP POST /predict (120ms)
│  ├─ Span: validate_input (5ms)
│  ├─ Span: model_inference (100ms)
│  └─ Span: format_response (2ms)
```

### Metrics

The application exports:

**Counters:**
- `http_requests_total` - Total HTTP requests
- `predictions_total` - Total predictions made
- `errors_total` - Total errors

**Histograms:**
- `prediction_latency_ms` - Latency distribution with buckets
- `request_duration_ms` - Overall request duration

**Gauges:**
- `active_requests` - Currently processing requests

### OTLP Pipeline

```
Application → OTLP Exporter → OTel Collector → Logging Exporter
                                              → (Future: Prometheus, Jaeger, etc.)
```

---

## OpenTelemetry Collector Configuration

### Collector Components

The collector is configured with:

**Receivers:**
- `otlp` - Receives traces and metrics via gRPC (port 4317)

**Processors:**
- `batch` - Batches telemetry data for efficiency

**Exporters:**
- `logging` - Exports to stdout (visible in logs)
- `debug` - Detailed debugging output

### View Collector Config

```bash
kubectl get configmap -n ai-ml-lab-2-2 otel-collector-config -o yaml
```

### Collector Endpoints

| Port | Protocol | Purpose |
|------|----------|---------|
| 4317 | gRPC | OTLP receiver |
| 4318 | HTTP | OTLP/HTTP receiver (optional) |
| 8888 | HTTP | Collector metrics |
| 13133 | HTTP | Health check |

---

## Resource Management

### Application Resources

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Collector Resources

```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "200m"
```

### Why This Matters

- **AI inference is CPU-intensive** - Proper limits prevent throttling
- **Observability overhead** - Collector needs resources too
- **Cost optimization** - Right-sized resources reduce cloud costs

---

## Cost Analysis

### Cloud Deployment Cost Estimate

**Assumptions:**
- Running in managed Kubernetes (GKE, EKS, AKS)
- 2 pods (1 app + 1 collector)
- Low traffic staging environment

**Monthly costs:**

| Component | Cost |
|-----------|------|
| Application pod (0.25 CPU, 256Mi RAM) | $3-4 |
| Collector pod (0.1 CPU, 128Mi RAM) | $1-2 |
| Load balancer (optional) | $3-5 |
| Data egress (minimal) | <$1 |
| **Total** | **$7-12/month** |

### Cost Optimization Tips

1. **Use spot/preemptible instances** - Save 60-80%
2. **Right-size resources** - Monitor and adjust
3. **Batch telemetry data** - Reduce network costs
4. **Sample traces** - Not every request needs tracing
5. **Use local storage** - Avoid cloud storage costs

### FREE Alternative (KIND)

Running in KIND cluster: **$0/month**

Perfect for:
- Development and testing
- Learning and experimentation
- CI/CD pipelines
- Demos and POCs

---

## Running Unit Tests

From the `paid/app` directory:

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest -v
```

Expected output:

```
================== test session starts ==================
collected 5 items

tests/test_app.py::test_health_check PASSED         [ 20%]
tests/test_app.py::test_prediction PASSED           [ 40%]
tests/test_app.py::test_tracing PASSED              [ 60%]
tests/test_app.py::test_metrics PASSED              [ 80%]
tests/test_app.py::test_error_handling PASSED       [100%]

=================== 5 passed in X.XXs ===================
```

---

## Production Deployment Considerations

### Exporting to Real Backends

Modify `collector-config.yaml` to send data to production systems:

**Prometheus:**
```yaml
exporters:
  prometheus:
    endpoint: "0.0.0.0:8889"
```

**Jaeger:**
```yaml
exporters:
  jaeger:
    endpoint: "jaeger-collector:14250"
```

**Cloud Providers:**
```yaml
exporters:
  googlecloud:
    project: "my-project"
  awsxray:
    region: "us-east-1"
```

### Sampling Strategies

For high-traffic production, implement sampling:

```yaml
processors:
  probabilistic_sampler:
    sampling_percentage: 10  # Sample 10% of traces
```

### Security Considerations

- Use TLS for OTLP connections
- Implement authentication
- Restrict collector access
- Sanitize sensitive data in spans

---

## Troubleshooting

### Pod Not Starting

Check pod status and events:

```bash
kubectl get pods -n ai-ml-lab-2-2
kubectl describe pod <pod-name> -n ai-ml-lab-2-2
```

View logs:

```bash
kubectl logs <pod-name> -n ai-ml-lab-2-2
```

### Collector Not Receiving Data

Verify collector is running:

```bash
kubectl get pods -n ai-ml-lab-2-2 | grep collector
```

Check collector logs:

```bash
kubectl logs -n ai-ml-lab-2-2 deploy/otel-collector
```

Test connectivity from app pod:

```bash
kubectl exec -n ai-ml-lab-2-2 <app-pod> -- nc -zv otel-collector 4317
```

### Traces Not Appearing

Check application logs for OpenTelemetry errors:

```bash
kubectl logs -n ai-ml-lab-2-2 deploy/ai-lab-2-2-paid | grep -i otel
```

Verify environment variables:

```bash
kubectl describe pod -n ai-ml-lab-2-2 <pod-name> | grep -A5 "Environment"
```

### High Latency

Check resource usage:

```bash
kubectl top pod -n ai-ml-lab-2-2
```

Look for CPU throttling:

```bash
kubectl describe pod -n ai-ml-lab-2-2 <pod-name> | grep -i throttl
```

### Collector Crashing

Check resource limits:

```bash
kubectl describe pod -n ai-ml-lab-2-2 <collector-pod> | grep -A10 "Limits"
```

Increase resources if needed:

```yaml
resources:
  limits:
    memory: "512Mi"
    cpu: "500m"
```

---

## Cleanup

Remove all PAID lab resources:

```bash
# Delete application
kubectl delete -f k8s/service.yaml
kubectl delete -f k8s/deployment.yaml

# Delete collector
kubectl delete -f k8s/collector-deployment.yaml
kubectl delete -f k8s/collector-config.yaml

# Delete namespace
kubectl delete -f k8s/namespace.yaml
```

Or delete everything at once:

```bash
kubectl delete namespace ai-ml-lab-2-2
```

Delete the kind cluster:

```bash
kind delete cluster --name mcp-cluster
```

---

## Comparison with FREE Version

| Feature | FREE Version | PAID Version |
|---------|-------------|--------------|
| Logging | Stdout only | Stdout + structured logging |
| Metrics | Custom `/metrics-lite` | OpenTelemetry metrics |
| Tracing | None | Full distributed tracing |
| Collector | Not needed | OpenTelemetry Collector |
| Latency Tracking | Simple average | Histogram with buckets |
| Load Generator | Basic | Advanced with histograms |
| Namespace | Default | Dedicated isolation |
| Resources | No limits | Defined requests/limits |
| Production Ready | No | Yes |
| Cloud Cost | $0 (KIND only) | <$10/month |

---

## Next Steps

### Advanced Observability

- **Grafana Integration** - Visualize metrics dashboards
- **Jaeger UI** - View distributed traces
- **Prometheus** - Long-term metrics storage
- **Alerting** - Set up alerts on SLO violations

### Production Enhancements

- **Service Mesh** - Istio for automatic tracing
- **Log Aggregation** - ELK or Loki stack
- **APM Tools** - Datadog, New Relic integration
- **Custom Dashboards** - Build team-specific views

### Cost Optimization

- **Trace Sampling** - Reduce data volume
- **Metric Aggregation** - Pre-aggregate before export
- **Retention Policies** - Define data lifecycle
- **Resource Auto-scaling** - Scale based on load

---

## Key Takeaways

✅ **OpenTelemetry is standard** - Industry-standard observability  
✅ **Traces reveal bottlenecks** - See exactly where time is spent  
✅ **Histograms beat averages** - Understand latency distribution  
✅ **Collectors add flexibility** - Centralized telemetry pipeline  
✅ **Cost awareness matters** - Observability can get expensive  
✅ **Start in KIND** - Test everything locally first  

---

## Questions or Issues?

Check the troubleshooting section above or review detailed logs:

```bash
# Application logs
kubectl logs -n ai-ml-lab-2-2 deploy/ai-lab-2-2-paid

# Collector logs
kubectl logs -n ai-ml-lab-2-2 deploy/otel-collector

# Pod details
kubectl describe pod -n ai-ml-lab-2-2 <pod-name>
```

Happy building production-grade observability! 🚀📊🔍