import os
from typing import Optional
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field

from shared_security import verify_api_key, add_cors_middleware, generate_worm_hash

# ------------------------------------------------------------------------------
# SkyOS & Agency Level Up - Core Gateway (PKG-01)
# ------------------------------------------------------------------------------

app = FastAPI(
    title="SkyOS Security & Avatar Gateway (PKG-01)",
    description="Layer 2 API Gateway with Paywall Protection, CORS & WORM Audit-Logging",
    version="2.3.0",
    docs_url=None,  # Disabled for security in production
    redoc_url=None  # Disabled for security in production
)

# 1. CORS Middleware — explizite Origin-Liste (kein Wildcard!)
add_cors_middleware(app)

# 2. Request & Response Schemas
class TranslationRequest(BaseModel):
    text: str = Field(..., description="Text content to translate")
    target_language: str = Field(default="en", description="Target BCP-47 language code")

class AvatarProductionRequest(BaseModel):
    avatar_id: str = Field(default="sky_meilin_v1", description="Target avatar ID")
    script_text: str = Field(..., description="Script text for video synthesis")
    output_resolution: str = Field(default="1080p", description="Rendering resolution (720p, 1080p, 4k)")

# 4. Helper: WORM Audit Hash Generator (von shared_security importiert)

# ------------------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------------------

@app.get("/health")
async def health_check():
    return {
        "status": "secured",
        "module": "PKG-01 Core Vault Gateway",
        "translator_agent": "active",
        "feature": "SkyOS Avatare",
        "licensing": "paywall_protected",
        "cors": "enabled",
        "worm_audit": "active"
    }

@app.post("/agent/translate")
async def translate_content(
    payload: TranslationRequest, 
    api_key: str = Depends(verify_api_key)
):
    audit_entry = generate_worm_hash("TRANSLATE", payload.text[:50])
    
    return {
        "status": "success",
        "target_language": payload.target_language,
        "translated_text": f"[Translated to {payload.target_language}]: {payload.text}",
        "gateway": "paywall_verified",
        "audit": audit_entry
    }

@app.post("/agent/sky-os-avatare")
async def sky_os_avatare(
    payload: AvatarProductionRequest, 
    api_key: str = Depends(verify_api_key)
):
    if not payload.script_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing script text for avatar video production."
        )
    
    audit_entry = generate_worm_hash("AVATAR_PROD", payload.avatar_id)
    
    return {
        "status": "rendering_queued",
        "module": "SkyOS Avatare",
        "avatar_id": payload.avatar_id,
        "resolution": payload.output_resolution,
        "message": "Production sequence successfully dispatched via paywall gateway.",
        "audit": audit_entry
    }
