"""
SkyOS Open Core - Environment Setup Script
Agency Level Up 2025 (Pascal Weidermann, Hückelhoven)

Erstellt und validiert die .env-Datei mit allen erforderlichen Variablen.
"""

import os
from pathlib import Path

ENV_TEMPLATE = """# SkyOS Open Core - Environment Variables
# Agency Level Up 2025 (Pascal Weidermann, Hückelhoven)

# Application
APP_NAME=SkyOS Open Core
APP_VERSION=0.1.0
DEBUG=false
ENVIRONMENT=development

# Server
HOST=0.0.0.0
PORT=8000
RELOAD=false

# CORS (comma-separated origins)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# GitHub OAuth (erforderlich für Authentifizierung)
# Siehe: docs/github-oauth-setup.md
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
GITHUB_REDIRECT_URI=http://localhost:8000/api/v1/auth/github/callback

# JWT Authentication
JWT_SECRET_KEY=skyos-jwt-secret-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

# Database (optional, für zukünftiges WORM-Ledger)
DATABASE_URL=

# OCR / Tesseract
TESSERACT_LANGUAGE=deu
TESSERACT_TIMEOUT=30

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600
"""


def setup_env():
    """Erstellt die .env-Datei, wenn sie noch nicht existiert."""
    env_path = Path(".env")
    
    if env_path.exists():
        print("✅ .env-Datei existiert bereits")
        return
    
    print("📝 .env-Datei erstellen...")
    env_path.write_text(ENV_TEMPLATE, encoding="utf-8")
    print("✅ .env-Datei erstellt!")
    print()
    print("⚠️  Bitte bearbeiten Sie die .env-Datei:")
    print("  1. GITHUB_CLIENT_ID und GITHUB_CLIENT_SECRET setzen")
    print("  2. JWT_SECRET_KEY ändern (für Produktion)")
    print("  3. CORS_ORIGINS anpassen")
    print()
    print("Siehe docs/github-oauth-setup.md für GitHub OAuth Einrichtung.")


def validate_env():
    """Validiert die .env-Datei auf erforderliche Variablen."""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env-Datei nicht gefunden. Führen Sie setup_env.py aus.")
        return False
    
    # Lade .env
    from dotenv import load_dotenv
    load_dotenv()
    
    errors = []
    warnings = []
    
    # Erforderliche Variablen
    if not os.getenv("JWT_SECRET_KEY") or os.getenv("JWT_SECRET_KEY") == "skyos-jwt-secret-change-in-production":
        warnings.append("JWT_SECRET_KEY sollte für Produktion geändert werden")
    
    # Optionale Variablen
    if not os.getenv("GITHUB_CLIENT_ID"):
        warnings.append("GITHUB_CLIENT_ID nicht gesetzt - GitHub OAuth wird nicht funktionieren")
    
    if not os.getenv("GITHUB_CLIENT_SECRET"):
        warnings.append("GITHUB_CLIENT_SECRET nicht gesetzt - GitHub OAuth wird nicht funktionieren")
    
    # Ausgabe
    if errors:
        print("❌ Fehler:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    if warnings:
        print("⚠️  Warnungen:")
        for warning in warnings:
            print(f"  - {warning}")
    
    print("✅ .env-Datei ist gültig")
    return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "validate":
        validate_env()
    else:
        setup_env()
