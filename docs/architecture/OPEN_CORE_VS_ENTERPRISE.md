# SkyOS Open Core vs Enterprise

## Übersicht

SkyOS wird in zwei Editionen angeboten: **Open Core** (kostenlos, Open Source) und **Enterprise** (kommerziell, mit erweiterten Features).

## Open Core (MIT License)

Die Open Core Edition ist kostenlos und unter MIT-Lizenz verfügbar.

### Enthaltene Features

- ✅ **OCR-Bescheid-Scanner**: Behördenbescheide scannen und parsen
- ✅ **OBG NRW §14 Notfall-Leitfäden**: Strukturierte Checklisten für Notfallgenehmigungen
- ✅ **DSGVO-Anonymizer**: Privacy-by-Design Telemetry-Anonymisierung
- ✅ **GitHub OAuth Authentifizierung**: Login mit GitHub-Account
- ✅ **FastAPI Backend**: REST API mit Swagger/ReDoc Dokumentation
- ✅ **React Frontend**: Web-basierte Benutzerooberfläche
- ✅ **Flutter Mobile App**: Cross-Platform Mobile App
- ✅ **Docker Support**: Container-basiertes Deployment
- ✅ **CI/CD Pipelines**: Automatisierte Tests und Builds

### Nicht enthalten (Enterprise nur)

- ❌ PostgreSQL WORM-Ledger (revisionssicheres Audit-Logging)
- ❌ Six-Verb State Machine (deterministische Agenten-Orchestrierung)
- ❌ MCP Gateway (Model Context Protocol)
- ❌ 15 Spezial-Departments (Agency in a Box)
- ❌ KRITIS Facility Gateway (GeoJSON Export)
- ❌ Multi-Tenant Isolation
- ❌ Enterprise Support (SLA, Priority Support)
- ❌ Custom Integrations

## Enterprise (Kommerzielle Lizenz)

Die Enterprise Edition bietet erweiterte Features für Unternehmen und Behörden.

### Zusätzliche Features

- ✅ **PostgreSQL WORM-Ledger**: BSI § 8a BSIG konformes Audit-Logging
- ✅ **Six-Verb State Machine**: Deterministische Agenten-Orchestrierung
- ✅ **MCP Gateway**: Model Context Protocol für Agenten-Kommunikation
- ✅ **15 Spezial-Departments**: Vollständige Agency-in-a-Box Lösung
- ✅ **KRITIS Facility Gateway**: GeoJSON Export für Katastrophenschutz
- ✅ **Multi-Tenant Isolation**: Tenant-spezifische Datenisolierung
- ✅ **Enterprise Support**: 99.9% SLA, Priority Support
- ✅ **Custom Integrations**: Individuelle Anpassungen

## Upgrade-Pfad

Das Upgrade von Open Core auf Enterprise ist nahtlos möglich:

1. Open Core als Basis installieren
2. Enterprise-Lizenz-Key in `.env` setzen
3. Enterprise-Module aktivieren
4. WORM-Ledger initialisieren

## Lizenz

- **Open Core**: MIT License
- **Enterprise**: Kommerzielle Lizenz (kontaktieren Sie uns)
