# PAID Version – Production-Ready AI Inference API Lab

This is the **PAID version** of the AI/ML Fundamentals lab for DevOps engineers. It includes production-leaning features like environment-based configuration, resource management, autoscaling, and CI/CD integration.

## What You'll Learn

- Production-ready configuration management with environment variables
- Setting resource requests and limits for AI workloads
- Implementing Horizontal Pod Autoscaler (HPA) for ML services
- Namespace isolation and best practices
- CI/CD pipeline integration with GitHub Actions
- Understanding why AI workloads need **tighter SLOs** and **autoscaling**

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
- Docker build/run commands
- Kubernetes deployments, services, and HPA
- Environment variable configuration
- Basic CI/CD concepts

---

## Repository Structure

```
chapter-02.1-inference-resources/
├── app/
│   ├── main.py              # FastAPI application
│   ├── model.py             # Separate model logic
│   ├── config.py            # Configuration management
│   ├── requirements.txt     # Python dependencies
│   └── tests/
│       └── test_app.py      # Unit tests
├── k8s/
│   ├── namespace.yaml       # Namespace isolation
│   ├── deployment.yaml      # Kubernetes deployment with resources
│   ├── service.yaml         # Kubernetes service
│   └── hpa.yaml             # Horizontal Pod Autoscaler
├── .env.example             # Example environment configuration
└── Dockerfile               # Container image definition
```

---

## Production Features

The PAID version includes:

✅ **Modular Code Structure** - Separate `model.py` and `config.py`  
✅ **Environment-Based Configuration** - `.env` file for different environments  
✅ **Resource Management** - CPU/Memory requests and limits  
✅ **Autoscaling** - Horizontal Pod Autoscaler (HPA) configuration  
✅ **Namespace Isolation** - Dedicated namespace for the application  
✅ **CI/CD Integration** - GitHub Actions workflow for tests and builds  

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

Edit `.env` to customize your configuration:

```bash
# Application environment
APP_ENV=local

# Model configuration
DEFAULT_LATENCY_MS=100
MAX_BATCH_SIZE=32

# API settings
API_PORT=9000
```

Available configuration options:

- `APP_ENV` - Environment name (local, dev, staging, prod)
- `DEFAULT_LATENCY_MS` - Simulated model inference latency
- `MAX_BATCH_SIZE` - Maximum batch size for predictions
- `API_PORT` - Port for the FastAPI application

### Step 3: Build Docker Image

```bash
docker build -t ai-lab-paid:v1 .
```

### Step 4: Load Image into kind

```bash
kind load docker-image ai-lab-paid:v1 --name mcp-cluster
```

### Step 5: Deploy to Kubernetes

Deploy all resources in order:

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Deploy application
kubectl apply -f k8s/deployment.yaml

# Create service
kubectl apply -f k8s/service.yaml

# Enable autoscaling
kubectl apply -f k8s/hpa.yaml
```

Check deployment status:

```bash
kubectl get pods -n ai-ml-lab
kubectl get svc -n ai-ml-lab
kubectl get hpa -n ai-ml-lab
```

---

## Testing the API

### Local Port Forward

To access the service locally:

```bash
kubectl port-forward -n ai-ml-lab deploy/ai-lab-paid 9000:9000
```

### Health Check

Test the health endpoint:

```bash
curl -s http://localhost:9000/health
```

Expected response:

```json
{"status": "ok", "env": "local"}
```

### Inference Test

Make a prediction request:

```bash
curl -s -X POST http://localhost:9000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [0.5, 1.5, 2]}'
```

Expected response:

```json
{
  "prediction": 4.0,
  "model_name": "simple-linear-demo",
  "latency_ms": 100
}
```

*Note: Values may differ slightly; the logic is deterministic for the given input.*

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
pytest
```

Expected output:

```
================== test session starts ==================
collected 3 items

tests/test_app.py ...                            [100%]

=================== 3 passed in X.XXs ===================
```

---

## Understanding Resource Configuration

### Deployment Resources

The deployment YAML includes resource requests and limits:

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

**Why this matters for AI/ML workloads:**
- AI inference can be CPU/memory intensive
- Proper resource allocation prevents pod eviction
- Ensures predictable performance and SLOs

### Horizontal Pod Autoscaler (HPA)

The HPA automatically scales pods based on CPU utilization:

```yaml
minReplicas: 1
maxReplicas: 5
targetCPUUtilizationPercentage: 70
```

**How it works:**
- Monitors CPU usage across all pods
- Scales up when CPU > 70%
- Scales down when CPU < 70%
- Ensures availability during traffic spikes

Check HPA status:

```bash
kubectl get hpa -n ai-ml-lab
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

The workflow at `.github/workflows/ci.yml` automatically:

1. Runs unit tests for the application
2. Builds Docker images
3. Validates Kubernetes manifests

### Triggering the Pipeline

**Automatic triggers:**
- Push to `main` branch
- Pull request creation

**Manual trigger:**
1. Go to GitHub Actions tab
2. Select the workflow
3. Click "Run workflow"

### Pipeline Steps

```yaml
1. Checkout code
2. Set up Python 3.11
3. Install dependencies
4. Run pytest
5. Build Docker image
6. Validate K8s manifests
```

---

## Local Development

To run the FastAPI app locally (without Kubernetes):

```bash
cd app

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (optional)
export APP_ENV=local
export DEFAULT_LATENCY_MS=100

# Run the application
uvicorn main:app --host 0.0.0.0 --port 9000
```

In another terminal:

```bash
curl -s http://localhost:9000/health
```

---

## Production Deployment Considerations

### Environment-Specific Configuration

For different environments, update the `.env` file:

**Development:**
```bash
APP_ENV=dev
DEFAULT_LATENCY_MS=50
```

**Staging:**
```bash
APP_ENV=staging
DEFAULT_LATENCY_MS=75
```

**Production:**
```bash
APP_ENV=prod
DEFAULT_LATENCY_MS=100
MAX_BATCH_SIZE=64
```

### Monitoring and Observability

Consider adding:
- Prometheus metrics for model latency
- Health check endpoints
- Structured logging
- Distributed tracing

### Security Best Practices

- Use namespace RBAC policies
- Implement network policies
- Scan Docker images for vulnerabilities
- Use secrets for sensitive configuration

---

## Cleanup

Remove all PAID lab resources:

```bash
# Delete in reverse order
kubectl delete -f k8s/hpa.yaml
kubectl delete -f k8s/service.yaml
kubectl delete -f k8s/deployment.yaml
kubectl delete -f k8s/namespace.yaml
```

Delete the kind cluster:

```bash
kind delete cluster --name mcp-cluster
```

---

## Troubleshooting

### Pods not starting / ImagePullBackOff

Ensure the image is loaded into kind:

```bash
kind load docker-image ai-lab-paid:v1 --name mcp-cluster
```

Check pod status in the namespace:

```bash
kubectl get pods -n ai-ml-lab
kubectl describe pod <pod-name> -n ai-ml-lab
```

### HPA not scaling

Verify metrics-server is running:

```bash
kubectl get deployment metrics-server -n kube-system
```

Check HPA status:

```bash
kubectl describe hpa ai-lab-paid -n ai-ml-lab
```

### Configuration not loading

Ensure `.env` file exists and is properly formatted:

```bash
cat .env
```

Check application logs:

```bash
kubectl logs <pod-name> -n ai-ml-lab
```

### Port-forward fails

Verify the deployment is running:

```bash
kubectl get deployments -n ai-ml-lab
kubectl get pods -n ai-ml-lab
```

### Tests failing

Ensure correct Python version and clean environment:

```bash
python --version  # Should be 3.11+
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pytest -v
```

---

## Comparison with FREE Version

| Feature | FREE Version | PAID Version |
|---------|-------------|--------------|
| Configuration | Hardcoded | Environment-based |
| Code Structure | Single file | Modular (model.py, config.py) |
| Resources | No limits | Requests & limits defined |
| Autoscaling | No HPA | HPA configured |
| Namespace | Default | Dedicated (ai-ml-lab) |
| CI/CD | Basic | GitHub Actions workflow |
| Production Ready | No | Yes |

---

## Next Steps

### Advanced Topics to Explore

- **Model Registry Integration** - Connect to MLflow or similar
- **A/B Testing** - Deploy multiple model versions
- **GPU Support** - Add GPU resources for intensive models
- **Service Mesh** - Implement Istio for advanced traffic management
- **Observability Stack** - Add Prometheus, Grafana, and Jaeger

### Production Checklist

- [ ] Configure resource requests/limits based on profiling
- [ ] Set up monitoring and alerting
- [ ] Implement proper logging
- [ ] Add authentication and authorization
- [ ] Configure network policies
- [ ] Set up backup and disaster recovery
- [ ] Document runbooks for common issues

---

## Questions or Issues?

Check the troubleshooting section above or review detailed logs:

```bash
# Pod logs
kubectl logs <pod-name> -n ai-ml-lab

# Deployment status
kubectl describe deployment ai-lab-paid -n ai-ml-lab

# HPA status
kubectl describe hpa ai-lab-paid -n ai-ml-lab
```

Happy learning and building production-ready AI services! 🚀