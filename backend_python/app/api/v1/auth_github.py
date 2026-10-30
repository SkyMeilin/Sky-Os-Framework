"""
SkyOS Open Core - GitHub OAuth Authentication API
Agency Level Up 2025 (Pascal Weidermann, Hückelhoven)

GitHub OAuth 2.0 Authentifizierung für die SkyOS Open Core App.
Ermöglicht Login mit GitHub-Account und JWT-Token-Ausgabe.
"""

import httpx
from typing import Optional, Dict, Any
from urllib.parse import urlencode

from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel

from app.core.config import settings
from app.core.security import create_access_token, User, get_current_user

router = APIRouter(prefix="/auth/github", tags=["Authentication"])


class GitHubTokenResponse(BaseModel):
    """GitHub OAuth Token Response."""
    access_token: str
    token_type: str = "bearer"
    scope: Optional[str] = None


class GitHubUserResponse(BaseModel):
    """GitHub User API Response."""
    id: int
    login: str
    email: Optional[str] = None
    name: Optional[str] = None
    avatar_url: Optional[str] = None


class AuthResponse(BaseModel):
    """SkyOS Auth Response."""
    access_token: str
    token_type: str = "bearer"
    user: User


class TokenRefreshResponse(BaseModel):
    """Token Refresh Response."""
    access_token: str
    token_type: str = "bearer"


def get_github_authorization_url(state: str = "skyos_oauth") -> str:
    """
    Erstellt die GitHub OAuth Autorisierungs-URL.
    
    Args:
        state: CSRF-Protection State-Parameter
        
    Returns:
        GitHub Autorisierungs-URL
    """
    params = {
        "client_id": settings.github_client_id,
        "redirect_uri": settings.github_redirect_uri,
        "scope": "user:email read:user",
        "state": state,
    }
    return f"https://github.com/login/oauth/authorize?{urlencode(params)}"


async def exchange_code_for_token(code: str) -> str:
    """
    Tauscht den GitHub Authorization Code gegen ein Access Token.
    
    Args:
        code: GitHub Authorization Code
        
    Returns:
        GitHub Access Token
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": settings.github_client_id,
                "client_secret": settings.github_client_secret,
                "code": code,
                "redirect_uri": settings.github_redirect_uri,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["access_token"]


async def get_github_user(github_token: str) -> GitHubUserResponse:
    """
    Holt die Benutzerinformationen von GitHub.
    
    Args:
        github_token: GitHub Access Token
        
    Returns:
        GitHubUserResponse mit Benutzerdaten
    """
    async with httpx.AsyncClient() as client:
        # User-Info
        user_response = await client.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github.v3+json",
            },
        )
        user_response.raise_for_status()
        user_data = user_response.json()
        
        # Email (kann privat sein)
        email = user_data.get("email")
        if not email:
            try:
                emails_response = await client.get(
                    "https://api.github.com/user/emails",
                    headers={
                        "Authorization": f"token {github_token}",
                        "Accept": "application/vnd.github.v3+json",
                    },
                )
                emails_response.raise_for_status()
                emails = emails_response.json()
                # Primäre Email finden
                for email_obj in emails:
                    if email_obj.get("primary"):
                        email = email_obj["email"]
                        break
            except Exception:
                pass
        
        return GitHubUserResponse(
            id=user_data["id"],
            login=user_data["login"],
            email=email,
            name=user_data.get("name"),
            avatar_url=user_data.get("avatar_url"),
        )


@router.get("/login", summary="GitHub OAuth Login URL")
async def github_login(state: str = "skyos_oauth") -> Dict[str, str]:
    """
    Gibt die GitHub OAuth Autorisierungs-URL zurück.
    
    Der Client sollte den Benutzer zu dieser URL weiterleiten.
    """
    if not settings.github_client_id or not settings.github_client_secret:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="GitHub OAuth ist nicht konfiguriert. Setze GITHUB_CLIENT_ID und GITHUB_CLIENT_SECRET.",
        )
    
    auth_url = get_github_authorization_url(state)
    return {
        "authorization_url": auth_url,
        "state": state,
    }


@router.get("/callback", summary="GitHub OAuth Callback")
async def github_callback(
    code: str,
    state: Optional[str] = None,
) -> AuthResponse:
    """
    GitHub OAuth Callback Endpoint.
    
    Tauscht den Authorization Code gegen ein JWT-Token.
    """
    if not settings.github_client_id or not settings.github_client_secret:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="GitHub OAuth ist nicht konfiguriert.",
        )
    
    try:
        # Code gegen Token tauschen
        github_token = await exchange_code_for_token(code)
        
        # Benutzerinformationen holen
        github_user = await get_github_user(github_token)
        
        # JWT Token erstellen
        jwt_token = create_access_token(
            data={
                "sub": str(github_user.id),
                "username": github_user.login,
                "email": github_user.email,
            }
        )
        
        user = User(
            github_id=str(github_user.id),
            username=github_user.login,
            email=github_user.email,
            name=github_user.name,
            avatar_url=github_user.avatar_url,
        )
        
        return AuthResponse(
            access_token=jwt_token,
            user=user,
        )
    
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"GitHub OAuth Fehler: {e.response.text}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentifizierungsfehler: {str(e)}",
        )


@router.get("/me", summary="Aktueller Benutzer")
async def get_me(current_user: User = Depends(get_current_user)) -> User:
    """
    Gibt die Informationen des aktuell authentifizierten Benutzers zurück.
    
    Erfordert einen gültigen JWT Token im Authorization-Header.
    """
    return current_user


@router.post("/refresh", summary="Token Refresh")
async def refresh_token(
    current_user: User = Depends(get_current_user)
) -> TokenRefreshResponse:
    """
    Erzeugt ein neues JWT Token für den aktuell authentifizierten Benutzer.
    """
    new_token = create_access_token(
        data={
            "sub": current_user.github_id,
            "username": current_user.username,
            "email": current_user.email,
        }
    )
    
    return TokenRefreshResponse(access_token=new_token)
