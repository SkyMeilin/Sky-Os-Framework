"""
SkyOS Open Core - Health Check API
Agency Level Up 2025 (Pascal Weidermann, Hückelhoven)

Health Check und Readiness Endpunkte für Load Balancer und Monitoring.
"""

from datetime import datetime, timezone
from typing import Dict, Any

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", summary="Health Check")
async def health_check() -> Dict[str, Any]:
    """
    Basis-Health Check Endpoint.
    
    Gibt den aktuellen Status der Anwendung zurück.
    Wird von Load Balancern und Monitoring-Systemen verwendet.
    """
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/ready", summary="Readiness Check")
async def readiness_check() -> Dict[str, Any]:
    """
    Readiness Check Endpoint.
    
    Prüft, ob alle abhängigen Dienste verfügbar sind.
    """
    checks = {
        "app": "ok",
        "config": "ok" if settings.jwt_secret_key else "warning",
    }
    
    # Database Check (optional)
    if settings.database_url:
        checks["database"] = "configured"  # Future: actual connection check
    
    all_ok = all(v in ("ok", "configured") for v in checks.values())
    
    return {
        "status": "ready" if all_ok else "degraded",
        "checks": checks,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/info", summary="Application Info")
async def app_info() -> Dict[str, Any]:
    """
    Gibt Informationen über die Anwendung zurück.
    """
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "debug": settings.debug,
        "features": {
            "ocr_scanner": True,
            "emergency_guides": True,
            "dsgvo_anonymizer": True,
            "github_oauth": bool(settings.github_client_id),
            "database": bool(settings.database_url),
        },
    }
