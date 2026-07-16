#!/bin/bash
# =============================================================================
# Rashid Dental AI Assistant — Deployment Script
# =============================================================================
# Usage:
#   ./deployment/scripts/deploy.sh               # Deploy using docker-compose
#   ./deployment/scripts/deploy.sh --build-only   # Only build images
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "============================================"
echo " Rashid Dental AI Assistant — Deploy"
echo "============================================"

cd "$PROJECT_DIR"

# Validate .env exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found. Copy .env.example to .env and configure."
    exit 1
fi

# Build Docker images
echo "[1/3] Building Docker images..."
docker-compose -f deployment/docker/docker-compose.yml build

if [ "${1:-}" = "--build-only" ]; then
    echo "Build complete. Exiting (--build-only flag detected)."
    exit 0
fi

# Start services
echo "[2/3] Starting services..."
docker-compose -f deployment/docker/docker-compose.yml up -d

# Health check
echo "[3/3] Waiting for service to be healthy..."
sleep 5
for i in {1..12}; do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/health 2>/dev/null || echo "000")
    if [ "$STATUS" = "200" ]; then
        echo "Service is healthy! (HTTP $STATUS)"
        echo ""
        echo "Website:  http://localhost:8000"
        echo "API Docs: http://localhost:8000/docs"
        echo ""
        exit 0
    fi
    echo "  Attempt $i/12 — HTTP $STATUS, retrying..."
    sleep 5
done

echo "WARNING: Service may not be healthy yet. Check with: docker-compose ps"
