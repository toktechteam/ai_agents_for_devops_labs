#!/bin/bash

set -e

echo "🧹 Cleaning up Kubernetes resources..."

kubectl delete ns ai-lab --ignore-not-found

echo "🧹 Removing Docker containers..."

docker rm -f langchain-api redis postgres 2>/dev/null || true

echo "🧹 Cleanup complete."
