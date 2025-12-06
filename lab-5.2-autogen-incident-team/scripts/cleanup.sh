#!/bin/bash
set -e

echo "🧹 Stopping docker-compose stack..."
docker-compose down -v || true

echo "🧹 Removing temporary files..."
rm -f incident_output.json

echo "✅ Cleanup complete."
