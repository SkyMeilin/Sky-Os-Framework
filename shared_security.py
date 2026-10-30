"""
SkyOS Shared Security Module
Agency Level Up 2025 (Pascal Weidermann, Hückelhoven)

Zentrale Authentifizierung, CORS-Konfiguration und WORM-Audit-Hashing
für alle SkyOS Root-Server (mcp_server, app, payment_gateway, etc.).

Compliance: BSI § 8a BSIG, Zero-IP-Leakage, DSGVO Art. 25
"""

import os
import time
import hashlib
import hmac
from typing import Optional, List

from fastapi import HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware


# ------------------------------------------------------------------------------
# 1. API-Key Authentifizierung
# ------------------------------------------------------------------------------

def get_api_key() -> str:
    """
    Liest den API-Key aus der Umgebungsvariable SKYOS_API_KEY.
    Wirft HTTPException wenn der Key nicht gesetzt ist (kein Default-Fallback!).
    """
    key = os.getenv("SKYOS_API_KEY")
    if not key:
        raise RuntimeError(
            "SKYOS_API_KEY environment variable is not set. "
            "Set it in your .env file before starting the server."
        )
    return key


async def verify_api_key(
    x_api_key: Optional[str] = Header(None, alias="x-api-key")
) -> str:
    """
    Verifiziert den API-Key aus dem x-api-key Header.
    
    Returns:
        Der validierte API-Key.
        
    Raises:
        HTTPException 402: Wenn kein API-Key gesendet wurde.
        HTTPException 401: Wenn der API-Key ungültig ist.
    """
    expected_key = get_api_key()
    
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Payment Required: Active SaaS license or valid API Key required."
        )
    
    # Konstante Zeit-Vergleich um Timing Attacks zu verhindern
    if not hmac.compare_digest(x_api_key, expected_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Invalid API Key provided."
        )
    
    return x_api_key


# ------------------------------------------------------------------------------
# 2. CORS Middleware Konfiguration
# ------------------------------------------------------------------------------

ALLOWED_ORIGINS: List[str] = [
    "http://localhost:3000",   # Next.js Dev
    "http://localhost:4200",   # Angular Dev Server
    "http://localhost:8080",   # Flutter Web Dev
    "http://localhost:8000",   # FastAPI Dev
    "https://skyos.example.com",  # Production (anpassen!)
]


def add_cors_middleware(app):
    """
    Fügt CORS-Middleware mit expliziter Origin-Liste hinzu.
    Ersetzt allow_origins=["*"] durch sichere, explizite Origins.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "x-api-key"],
    )


# ------------------------------------------------------------------------------
# 3. WORM Audit Hash Generator
# ------------------------------------------------------------------------------

def generate_worm_hash(action: str, payload: str, previous_hash: str = "0" * 64) -> dict:
    """
    Generiert einen WORM-konformen Audit-Hash mit SHA-256 Chain-Verknüpfung.
    
    Args:
        action: Aktion-Name (z.B. "TRANSLATE", "AVATAR_PROD", "PAYMENT_WEBHOOK")
        payload: Payload-String (gekürzt auf relevante Teile)
        previous_hash: Hash des vorherigen Eintrags (Genesis = 64x'0')
        
    Returns:
        Dict mit timestamp, action, payload_hash, previous_hash, current_hash
    """
    timestamp = time.time()
    payload_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    
    # Chain-Hash: previous_hash + timestamp + action + payload_hash
    chain_data = f"{previous_hash}:{timestamp}:{action}:{payload_hash}"
    current_hash = hashlib.sha256(chain_data.encode("utf-8")).hexdigest()
    
    return {
        "timestamp": timestamp,
        "action": action,
        "payload_hash": payload_hash,
        "previous_hash": previous_hash,
        "current_hash": current_hash,
    }


# ------------------------------------------------------------------------------
# 4. Webhook HMAC Signatur Verifikation
# ------------------------------------------------------------------------------

def verify_webhook_signature(
    payload: bytes,
    signature_header: str,
    secret: str,
    algorithm: str = "sha256"
) -> bool:
    """
    Verifiziert die HMAC-Signatur eines Webhook-Payloads.
    
    Args:
        payload: Rohes Request-Payload (bytes)
        signature_header: Signatur aus dem Header (z.B. X-Webhook-Signature)
        secret: Webhook-Secret aus .env
        algorithm: Hash-Algorithmus (Standard: sha256)
        
    Returns:
        True wenn Signatur gültig ist.
    """
    if not secret:
        raise RuntimeError(
            "Webhook secret is not configured. "
            "Set the appropriate WEBHOOK_SECRET environment variable."
        )
    
    expected_signature = hmac.new(
        secret.encode("utf-8"),
        payload,
        getattr(hashlib, algorithm)
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature_header)


def get_webhook_secret(secret_name: str) -> str:
    """
    Liest einen Webhook-Secret aus der Umgebungsvariable.
    Wirft RuntimeError wenn nicht gesetzt.
    """
    secret = os.getenv(secret_name)
    if not secret:
        raise RuntimeError(
            f"{secret_name} environment variable is not set. "
            "Webhook signature verification is disabled without a secret."
        )
    return secret


# ------------------------------------------------------------------------------
# 5. Path Traversal Protection
# ------------------------------------------------------------------------------

def validate_path_against_root(requested_path: str, root_path: str) -> str:
    """
    Validiert, dass der angeforderte Pfad innerhalb des Root-Verzeichnisses liegt.
    
    Args:
        requested_path: Der vom Benutzer angeforderte Pfad
        root_path: Das erlaubte Root-Verzeichnis
        
    Returns:
        Der aufgelöste, validierte Pfad.
        
    Raises:
        HTTPException 403: Wenn Path-Traversal erkannt wird.
    """
    import pathlib
    
    requested = pathlib.Path(requested_path).resolve()
    root = pathlib.Path(root_path).resolve()
    
    if not str(requested).startswith(str(root)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Path traversal detected. Requested path is outside the allowed root directory."
        )
    
    return str(requested)
