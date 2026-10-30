"""
SkyOS Open Core - FastAPI Application Entry Point
Agency Level Up 2025 (Pascal Weidermann, Hückelhoven)

Hauptanwendung mit allen API-Routern, Middleware und Lifecycle-Events.
"""

import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Füge das Projekt-Root zum Path hinzu
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.core.config import settings
from app.core.security import add_cors_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application Lifecycle Manager.
    
    Wird beim Starten und Stoppen der Anwendung aufgerufen.
    """
    # Startup
    print(f"🚀 {settings.app_name} v{settings.app_version} starting...")
    print(f"   Environment: {settings.environment}")
    print(f"   Debug: {settings.debug}")
    
    if settings.github_client_id:
        print(f"   GitHub OAuth: configured")
    else:
        print(f"   GitHub OAuth: NOT configured (set GITHUB_CLIENT_ID)")
    
    if settings.database_url:
        print(f"   Database: configured")
    else:
        print(f"   Database: NOT configured (set DATABASE_URL)")
    
    yield
    
    # Shutdown
    print(f"👋 {settings.app_name} shutting down...")


# FastAPI App Instanz
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "SkyOS Open Core Backend API. "
        "Behördenbescheid-OCR-Parser, Notfall-Leitfäden und DSGVO-Anonymisierung. "
        "Open-Source-Komponente für das SkyOS Ökosystem."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS Middleware
add_cors_middleware(app)


# ==========================================
# API Routers
# ==========================================

from app.api.v1 import health, auth_github, scanner

app.include_router(health.router, prefix="/api/v1")
app.include_router(auth_github.router, prefix="/api/v1")
app.include_router(scanner.router, prefix="/api/v1")


# ==========================================
# Root Endpoint
# ==========================================

@app.get("/", summary="Root")
async def root():
    """
    Root Endpoint der SkyOS Open Core API.
    """
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/v1/health/",
    }


# ==========================================
# Run with Uvicorn
# ==========================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
    )
