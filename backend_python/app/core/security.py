"""
SkyOS Open Core - Security Module
Agency Level Up 2025 (Pascal Weidermann, Hückelhoven)

JWT-Authentifizierung, Rate Limiting und CORS-Konfiguration.
"""

import time
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from functools import wraps

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt, JWTError
from pydantic import BaseModel

from .config import settings

security = HTTPBearer()


class TokenPayload(BaseModel):
    """JWT Token Payload."""
    sub: str  # GitHub User ID
    username: str
    email: Optional[str] = None
    exp: datetime
    iat: datetime


class User(BaseModel):
    """Benutzermodell."""
    github_id: str
    username: str
    email: Optional[str] = None
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    is_authenticated: bool = True


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Erstellt einen JWT Access Token.
    
    Args:
        data: Daten, die im Token gespeichert werden sollen
        expires_delta: Gültigkeitsdauer (Standard: aus Config)
        
    Returns:
        JWT Token als String
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    })
    
    return jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


async def decode_access_token(token: str) -> Optional[TokenPayload]:
    """
    Dekodiert und validiert einen JWT Token.
    
    Args:
        token: JWT Token String
        
    Returns:
        TokenPayload oder None bei ungültigem Token
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return TokenPayload(
            sub=payload["sub"],
            username=payload["username"],
            email=payload.get("email"),
            exp=payload["exp"],
            iat=payload["iat"],
        )
    except JWTError:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Extrahiert und validiert den aktuellen Benutzer aus dem JWT Token.
    
    Args:
        credentials: HTTP Bearer Credentials
        
    Returns:
        User Objekt
        
    Raises:
        HTTPException: Wenn Token ungültig oder abgelaufen
    """
    payload = await decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ungültige oder abgelaufene Authentifizierung",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return User(
        github_id=payload.sub,
        username=payload.username,
        email=payload.email,
    )


async def get_optional_user(
    request: Request
) -> Optional[User]:
    """
    Extrahiert optional den aktuellen Benutzer (nicht erforderlich).
    
    Args:
        request: FastAPI Request
        
    Returns:
        User Objekt oder None wenn nicht authentifiziert
    """
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    
    token = auth_header.split("Bearer ")[1]
    payload = await decode_access_token(token)
    if payload is None:
        return None
    
    return User(
        github_id=payload.sub,
        username=payload.username,
        email=payload.email,
    )


def add_cors_middleware(app) -> None:
    """
    Fügt CORS-Middleware zur FastAPI App hinzu.
    
    Args:
        app: FastAPI App Instanz
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# ==========================================
# Rate Limiting
# ==========================================

class RateLimiter:
    """
    Einfacher in-memory Rate Limiter basierend auf IP-Adresse.
    
    Für Produktion: Redis-basierter Rate Limiter empfohlen.
    """
    
    def __init__(
        self,
        max_requests: int = None,
        window_seconds: int = None,
    ):
        self.max_requests = max_requests or settings.rate_limit_requests
        self.window_seconds = window_seconds or settings.rate_limit_window
        self._requests: Dict[str, list] = {}
    
    def _get_client_ip(self, request: Request) -> str:
        """Extrahiert die Client-IP aus dem Request."""
        # Prüfe X-Forwarded-For Header (bei Proxy/Load Balancer)
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.client.host if request.client else "unknown"
    
    def is_rate_limited(self, request: Request) -> bool:
        """
        Prüft, ob der Client das Rate Limit überschritten hat.
        
        Args:
            request: FastAPI Request
            
        Returns:
            True wenn Rate Limit überschritten
        """
        client_ip = self._get_client_ip(request)
        now = time.time()
        
        # Alte Einträge bereinigen
        if client_ip in self._requests:
            self._requests[client_ip] = [
                t for t in self._requests[client_ip]
                if now - t < self.window_seconds
            ]
        else:
            self._requests[client_ip] = []
        
        # Prüfen ob Limit überschritten
        if len(self._requests[client_ip]) >= self.max_requests:
            return True
        
        # Neuen Request registrieren
        self._requests[client_ip].append(now)
        return False


# Globaler Rate Limiter
rate_limiter = RateLimiter()


async def check_rate_limit(request: Request) -> None:
    """
    FastAPI Dependency für Rate Limiting.
    
    Args:
        request: FastAPI Request
        
    Raises:
        HTTPException: Wenn Rate Limit überschritten
    """
    if rate_limiter.is_rate_limited(request):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate Limit überschritten. Bitte warten Sie.",
        )


# ==========================================
# WORM Hash Utility
# ==========================================

def compute_worm_hash(payload: str, previous_hash: str = "0" * 64) -> Dict[str, str]:
    """
    Berechnet einen WORM-konformen SHA-256 Hash mit Hash-Chain.
    
    Args:
        payload: Zu hashender Payload
        previous_hash: Vorheriger Hash in der Kette
        
    Returns:
        Dictionary mit Hash-Informationen
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    payload_hash = hashlib.sha256(payload.encode()).hexdigest()
    chain_raw = f"{previous_hash}:{payload_hash}:{timestamp}"
    current_hash = hashlib.sha256(chain_raw.encode()).hexdigest()
    
    return {
        "timestamp": timestamp,
        "payload_hash": payload_hash,
        "previous_hash": previous_hash,
        "current_hash": current_hash,
    }
