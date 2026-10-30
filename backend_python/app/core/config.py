"""
SkyOS Open Core - Backend Configuration
Agency Level Up 2025 (Pascal Weidermann, Hückelhoven)

Zentralisierte Konfiguration via Pydantic Settings.
Unterstützt Umgebungsvariablen (.env) und Validierung.
"""

from typing import Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Zentrale Konfiguration für die SkyOS Open Core Backend-App.
    
    Liest Werte aus Umgebungsvariablen oder .env-Datei.
    """

    # Application
    app_name: str = "SkyOS Open Core"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "development"  # development, staging, production

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False

    # CORS
    cors_origins: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:8080"]
    )

    # GitHub OAuth
    github_client_id: Optional[str] = None
    github_client_secret: Optional[str] = None
    github_redirect_uri: str = "http://localhost:8000/api/v1/auth/github/callback"

    # JWT Authentication
    jwt_secret_key: str = "skyos-jwt-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    # Database (optional, for future WORM ledger)
    database_url: Optional[str] = None
    database_pool_size: int = 5
    database_max_overflow: int = 10

    # OCR / Tesseract
    tesseract_language: str = "deu"
    tesseract_timeout: int = 30

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"  # json, text

    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # seconds

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Globale Settings-Instanz
settings = Settings()
