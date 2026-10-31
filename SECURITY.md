# SkyOS Security Policy & Audit Richtlinie

Vielen Dank, dass Sie zur Sicherheit von **Sky OS – Das Framework** beitragen. Da dieses System auf absolute Datensouveränität, lokale Ausführung und WORM-Compliance ausgelegt ist, nehmen wir Sicherheit sehr ernst.

## 🛡️ Unterstützte Versionen

SkyOS verwendet strikte Sicherheits- und Audit-Standards. Sicherheitspatches und WORM-Compliance-Updates werden ausschließlich für die aktiven Produktions- und Hauptversionen bereitgestellt.

| Version | Core Architecture | Supported | Audit & WORM |
| ------- | ---------------- | --------- | ------------ |
| 4.x.x   | SkyOS Core (FastAPI / Flutter / Discord / MCP) | :white_check_mark: | Full Audit Support |
| < 4.0   | Legacy / Prototype Phase | :x: | Non-Compliant / Deprecated |

---

## Sicherheitsarchitektur & Compliance Guidelines

1. **Workspace Isolation:**
   - Der primäre Ausführungspfad ist isoliert. Direkte Pfad-Skripte oder uneingeschränkte Dateizugriffe außerhalb des deklarierten Workspaces sind strikt untersagt.

2. **WORM-Audit-Logging (Write Once, Read Many):**
   - Alle sicherheits- und systemrelevanten Ereignisse werden unveränderbar protokolliert (`quantum_ledger.py`, Ledger unter `audit_quantum_ledger.json`).
   - Manipulationen an Protokolldateien lösen automatische Guard-Alerts aus.
   - Hash-Integrität wird per **SHA3-256** in der CI-Pipeline validiert.

3. **Messenger & API Isolation:**
   - Externe Steuerung erfolgt ausschließlich über die verifizierte Discord-Bot-API (`discord-bot.js`) und MCP-Server (`mcp_server.py`).
   - Veraltete oder unverschlüsselte Messenger-Schnittstellen sind deaktiviert.

4. **Secrets & API-Key Management:**
   - API-Schlüssel dürfen niemals in Repositories eingecheckt werden.
   - Es müssen ausschließlich `.env`-Dateien oder Umgebungsvariablen verwendet werden.
   - `.env` und `*.pem`/`*.key` Dateien sind in `.gitignore` geschützt.

5. **Keine Cloud-Abhängigkeit:**
   - Sky OS läuft lokal auf Ihrer Hardware. Sensible Daten und das quantensichere Ledger bleiben isoliert auf Ihrem System.

---

## 🚨 Meldung von Sicherheitslücken (Reporting a Vulnerability)

Sicherheitslücken, unbefugte Zugriffsmöglichkeiten oder Compliance-Abweichungen müssen umgehend gemeldet werden.

1. **Meldeweg:**
   - Bitte melde potenzielle Schwachstellen per privatem Ticket an den System-Architekten (Sky Meilin / Pascal) oder direkt über das interne Discord Security-Audit-Overlay.
   - **Bitte erstelle keine öffentlichen Issues auf GitHub** für nicht gepatchte Sicherheitslücken.

2. **Reaktionszeiten:**
   - **Erstbestätigung:** Innerhalb von 24 Stunden.
   - **Bewertung & Triage:** Innerhalb von 48 Stunden.
   - **Fix & Patch-Deployment:** Je nach Schweregrad (Kritisch: < 24h, Mittel: < 7 Tage).

3. **Inhalt der Meldung:**
   - Betroffene Komponente / Pfad (z. B. API, MCP Server, Discord Bot).
   - Schritte zur Reproduktion der Schwachstelle (Proof of Concept).
   - Mögliche Auswirkungen auf das WORM-Audit-System oder gespeicherte Daten.

---

## Automatisierte Sicherheitsprüfungen

Vor jedem Commit oder Deployment greifen automatische Guard-Checks in der CI/CD-Pipeline:

- **Dependency Scan:** Prüfung aller Python (`pip-audit`) und Node.js Dependencies auf bekannte Lücken.
- **SAST (Static Analysis):** Bandit-Scan für Python-Code-Schwachstellen.
- **Secret Scanning:** Gitleaks scannt auf versehentlich eingecheckte API-Keys und Secrets.
- **Container Scan:** Trivy prüft Docker-Images auf Vulnerabilities.
- **WORM Log Integrity Check:** SHA3-256 Hash-Verifizierung des Audit-Ledgers.
- **Path Isolation Check:** Strikte Validierung der Systemgrenzen.

---

*Letzte Aktualisierung: Oktober 2026*
*Autor: Sky Meilin Agent (Security Department)*
