#!/bin/bash
set -e

echo "Running all tests..."
pytest -q
echo "All tests passed."
