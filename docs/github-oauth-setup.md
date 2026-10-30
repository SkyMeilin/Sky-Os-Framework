# GitHub OAuth Setup Guide

## Übersicht

SkyOS Open Core verwendet GitHub OAuth 2.0 für die Authentifizierung. Dieser Guide beschreibt die Einrichtung.

## Schritt 1: GitHub OAuth App erstellen

1. Gehe zu [GitHub Settings → Developer settings → OAuth Apps](https://github.com/settings/developers)
2. Klicke auf **"New OAuth App"**
3. Fülle die Felder aus:
   - **Application name**: `SkyOS Open Core`
   - **Homepage URL**: `http://localhost:8080`
   - **Authorization callback URL**: `http://localhost:8000/api/v1/auth/github/callback`
4. Klicke auf **"Register application"**

## Schritt 2: Client ID und Secret kopieren

Nach der Erstellung der App:

1. Kopiere die **Client ID**
2. Klicke auf **"Generate a new client secret"** und kopiere das Secret
3. Speichere beide Werte sicher

## Schritt 3: .env konfigurieren

Trage die Werte in der `.env`-Datei ein:

```env
GITHUB_CLIENT_ID=deine_client_id_hier
GITHUB_CLIENT_SECRET=dein_client_secret_hier
GITHUB_REDIRECT_URI=http://localhost:8000/api/v1/auth/github/callback
```

## Schritt 4: Testen

1. Starte das Backend:
   ```bash
   cd backend_python
   uvicorn app.main:app --reload
   ```

2. Öffne `http://localhost:8000/docs`
3. Teste den `/api/v1/auth/github/login` Endpoint
4. Du solltest zur GitHub-Autorisierungsseite weitergeleitet werden

## Produktion

Für die Produktion:

1. Erstelle eine neue OAuth App oder aktualisiere die bestehende
2. Setze die korrekten URLs:
   ```env
   GITHUB_REDIRECT_URI=https://deine-domain.de/api/v1/auth/github/callback
   ```
3. Ändere den `JWT_SECRET_KEY`:
   ```env
   JWT_SECRET_KEY=dein-sicherer-secret-key
   ```

## Fehlerbehebung

### "Bad request" beim Callback
- Prüfe, ob die `GITHUB_REDIRECT_URI` exakt mit der in GitHub konfigurierten URL übereinstimmt

### "Unauthorized client"
- Prüfe, ob `GITHUB_CLIENT_ID` und `GITHUB_CLIENT_SECRET` korrekt gesetzt sind

### Token funktioniert nicht
- Prüfe, ob `JWT_SECRET_KEY` gesetzt ist
- Prüfe die Token-Gültigkeit (Standard: 60 Minuten)
