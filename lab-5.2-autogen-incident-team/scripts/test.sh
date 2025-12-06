#!/bin/bash
set -e

echo "🔥 Starting full Lab 5.2 test run..."

# 1) Run unit tests (no external services needed)
echo "🧪 Running pytest unit tests..."
pytest -q

# 2) Spin up full stack and hit the API once
echo "🐳 Starting docker-compose stack..."
docker-compose up -d --build

echo "⏳ Waiting for API to be ready..."
sleep 15

echo "📡 Hitting /health endpoint..."
curl -s http://localhost:8000/health || {
  echo "❌ Health check failed"
  docker-compose logs api
  exit 1
}

echo "📡 Running incident workflow for memory_leak..."
curl -s -X POST http://localhost:8000/incident/run \
  -H "Content-Type: application/json" \
  -d '{"scenario": "memory_leak", "auto_approve": false}' > incident_output.json || {
  echo "❌ Incident run failed"
  exit 1
}

echo "✅ Test script completed. See incident_output.json for full response."
