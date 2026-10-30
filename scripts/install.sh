#!/bin/bash
# SkyOS Open Core - Installation Script
# Agency Level Up 2025 (Pascal Weidermann, Hückelhoven)

set -e

echo "🛡️ SkyOS Open Core - Installation"
echo "=================================="

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3.11+ ist erforderlich"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python Version: $PYTHON_VERSION"

# Create virtual environment
echo "📦 Virtuelle Umgebung erstellen..."
python3 -m venv venv
source venv/bin/activate

# Install backend dependencies
echo "📦 Backend-Abhängigkeiten installieren..."
pip install --upgrade pip
pip install -r backend_python/app/requirements.txt

# Setup .env file
if [ ! -f .env ]; then
    echo "📝 .env-Datei erstellen..."
    cp .env.example .env
    echo "✅ .env-Datei erstellt - bitte bearbeiten!"
fi

# Install frontend dependencies
if command -v npm &> /dev/null; then
    echo "📦 Frontend-Abhängigkeiten installieren..."
    cd frontend_web
    npm install
    cd ..
fi

echo ""
echo "✅ Installation abgeschlossen!"
echo ""
echo "Nächste Schritte:"
echo "  1. .env-Datei bearbeiten (GitHub OAuth Keys)"
echo "  2. Backend starten: source venv/bin/activate && cd backend_python && uvicorn app.main:app --reload"
echo "  3. Frontend starten: cd frontend_web && npm start"
echo ""
echo "🚀 SkyOS Open Core ist bereit!"
