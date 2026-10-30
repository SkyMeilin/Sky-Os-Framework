#!/bin/bash
# SkyOS Open Core - Deploy Agent Script
# Agency Level Up 2025 (Pascal Weidermann, Hückelhoven)

set -e

echo "🚀 SkyOS Open Core - Deployment"
echo "================================"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker ist erforderlich"
    exit 1
fi

# Build and run
echo "📦 Docker-Images bauen..."
cd docker
docker compose build

echo "🚀 Dienste starten..."
docker compose up -d

echo ""
echo "✅ Deployment abgeschlossen!"
echo ""
echo "Services:"
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:8080"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "Logs anzeigen: docker compose logs -f"
echo "Stoppen: docker compose down"
