# Security Policies

## Übersicht

SkyOS Open Core folgt strengen Sicherheitsrichtlinien, um die Vertraulichkeit, Integrität und Verfügbarkeit der Daten zu gewährleisten.

## DSGVO Art. 25 - Privacy by Design

- **DSGVO-Anonymizer**: Automatische Erkennung und Anonymisierung von PII (Personally Identifiable Information)
- **Supported PII Types**: E-Mail, Telefon, IP-Adresse, MAC-Adresse, Kreditkarte, Steuernummer, Versicherungsnummer, PLZ, GPS-Koordinaten
- **Anonymisierungsmethoden**: Entfernen, Pseudonymisieren (SHA-256 Hash), Generalisieren (Maskierung)

## Authentifizierung

- **GitHub OAuth 2.0**: Sichere Authentifizierung über GitHub-Accounts
- **JWT Tokens**: Short-lived Access Tokens (Standard: 60 Minuten)
- **Rate Limiting**: Schutz vor Brute-Force-Angriffen (100 Requests/Stunde)

## API-Sicherheit

- **CORS**: Konfigurierbare Cross-Origin Resource Sharing Richtlinien
- **HTTPS**: In Produktion ausschließlich verschlüsselte Kommunikation
- **Input Validation**: Pydantic-basierte Validierung aller API-Anfragen

## Datenschutz

- **Keine Telemetry**: SkyOS Open Core sendet keine Telemetry-Daten an externe Server
- **Lokale Speicherung**: Alle Daten werden lokal gespeichert
- **Audit-Log**: DSGVO-Anonymizer führt ein Audit-Log aller Anonymisierungsoperationen

## Empfehlungen für Produktion

1. **JWT_SECRET_KEY ändern**: Verwende einen sicheren, zufälligen Secret-Key
2. **HTTPS aktivieren**: Verwende ein Reverse Proxy (nginx, Traefik) mit TLS
3. **Rate Limiting anpassen**: Passe die Rate-Limits an deine Anforderungen an
4. **CORS einschränken**: Setze `CORS_ORIGINS` auf deine Produktions-Domains
5. **GitHub OAuth**: Verwende eine separate OAuth-App für Produktion
