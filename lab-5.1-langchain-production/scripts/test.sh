#!/bin/bash

set -e

echo "🔥 Running LangChain API Local Test"

API_URL="http://localhost:8000/investigate"

echo "📡 Sending test alert..."
response=$(curl -s -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{"alert": "High CPU on pod test-pod"}')

echo "📦 Response:"
echo "$response"

# Basic validation
if [[ "$response" == *"analysis"* ]]; then
  echo "✅ API test passed"
else
  echo "❌ API test failed"
  exit 1
fi
