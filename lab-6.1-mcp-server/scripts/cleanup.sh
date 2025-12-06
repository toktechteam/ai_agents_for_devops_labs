#!/bin/bash
set -e

echo "Cleaning up cluster and namespace..."
kubectl delete namespace mcp-lab || true
kind delete cluster --name mcp-lab || true
echo "Cleanup complete."
