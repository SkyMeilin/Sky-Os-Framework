# 🛡️ SkyOS – Sicherheitsrichtlinien & DevSecOps Control Center

> **SkyOS & Agency Level Up Core Security Infrastructure**
> *Zero-IP-Leakage | BSI § 8a BSIG Compliance | Gehärtete Agenten-Sandbox | Distroless Runtime*

---

## 📋 Übersicht & System-Profil

Das Repository **Sicherheitsrichtlinien** bildet das zentrale **Sicherheits-, Compliance- und Governance-Fundament** des **SkyOS / Agency Level Up** Ökosystems.

Es stellt sicher, dass alle autonomen KI-Agenten, lokale Inferenz-Engines (NPU / Ollama) und externe Schnittstellen (MCP Gateway) unter strikten Sicherheits-Leitplanken, vollständiger Datensouveränität (Zero-IP-Leakage) und auditierbarer Transparenz arbeiten.

---

## 📂 Repository-Struktur

```
Sicherheitsrichtlinien/
├── .github/
│   └── workflows/              # CI/CD pipelines (ci.yml, security_scan.yml, auto-assign.yml)
├── src/                        # Kern-Logik, Orchestrator & Agenten-Module
├── web-developer/              # Frontend Web-UI / Control Center Komponenten
├── papers/                     # Dokumente, Whitepaper & Spezifikationen (.gitkeep)
│   └── .gitkeep
├── node_modules/               # Automatisch generiert (in .gitignore)
├── app.py                      # Haupt-FastAPI Server & REST Gateway
├── mcp_server.py               # Model Context Protocol (MCP) Server
├── server.js                   # Node.js Integration Service
├── benchmark.py                # System-Performance & Inferenz-Benchmarking
├── update_readme.py            # Automatischer README-Updater
├── requirements.txt            # Python Dependencies
├── env.example                 # Vorlage für Umgebungsvariablen & Secrets
└── README.md                   # System-Dokumentation & Control Center Guide
```

---

## 🏛️ Die 5 Grundsäulen der Sicherheits-Architektur

### 1. 🛡️ Container-Härtung & Runtime Shield

* **Google Distroless Debian 12**: Minimale Angriffsfläche ohne Shells, Paketmanager oder unbewachte Binaries.
* **Non-Root Execution**: Strikter Betrieb unter der unprivilegierten **UID 65532**.
* **Schreibgeschütztes Dateisystem**: `read_only: true` mit dediziertem `tmpfs`-Volume für flüchtige Laufzeitdaten.
* **Kernel Capabilities**: Vollständiger Entzug aller Kernel-Rechte (`cap_drop: ALL`).

### 2. 📜 Revisionssicheres PostgreSQL WORM-Ledger

* **BSI § 8a BSIG & ISO/IEC 27037**: Unveränderliche Audit-Protokollierung aller Agenten-Transaktionen.
* **Kryptographische Verkettung**: SHA-256 Hashverkettung mit präzisen PTP-Zeitstempeln.
* **Tamper-Protection**: Der Datenbank-Trigger `fn_reject_audit_tampering` unterbindet jegliche nachträglichen `UPDATE`- oder `DELETE`-Operationen.

### 3. 🔒 3-Schichten IP-Schutz (Zero-IP-Leakage)

* **Layer 1 (Public Frontend)**: Interaktive Benutzeroberflächen und Log-Viewer.
* **Layer 2 (API Gateway)**: FastAPI & MCP Gateway zur Orchestrierung der Agenten-Workflows.
* **Layer 3 (Core IP Vault)**: Physisch isolierter Bereich für proprietäre Prompt-Logiken, API-Keys und Geschäftsgeheimnisse – ohne direkte externe Erreichbarkeit.

### 4. 🤖 Deterministisches Six-Verb-Protokoll

Alle KI-Agenten-Aktionen durchlaufen eine unumkehrbare Zustandsmaschine:

```
[SEARCH] → [RESOLVE] → [PREVIEW] → [HUMAN_GATE] → [EXECUTE] → [VERIFY]
```

* **Privacy-by-Design (DSGVO Art. 25)**: Automatische PII-Anonymisierung im `RESOLVE`-Schritt.
* **Manuelle Freigabe (`HUMAN_GATE`)**: Kritische System- oder Datenbankmutations-Schritte erfordern die explizite Bestätigung des Operators.

### 5. ⚡ Lokale NPU Inferenz & Datensouveränität

* **Bring Your Own Compute (BYOC)**: Vollständige Ausführung vertraulicher Modelle lokal auf dem Gerät (z. B. Copilot+ PC NPU / Ollama Port 11434).
* **Hybrid Workload Split**: Transformer-Blöcke laufen NPU-beschleunigt (ONNX QDQ int4/int16), Embeddings und LM-Head auf der CPU.

---

## 🚀 Quickstart & Inbetriebsetzung

```bash
# 1. Repository klonen
git clone https://github.com/Sky-Meilin-Coaperation/Sicherheitsrichtlinien.git
cd Sicherheitsrichtlinien

# 2. Umgebungsvariablen einrichten
cp env.example .env

# 3. Abhängigkeiten installieren
pip install -r requirements.txt

# 4. Gateway & MCP Server starten
python app.py
```

---

## ⚙️ CI/CD & Security Audits

In `.github/workflows/` sind automatisierte Qualitäts- und Sicherheitsprüfungen integriert:

* **`ci.yml`**: Syntaxtests (`app.py`, `mcp_server.py`, `server.js`), Flake8 & Black Linting, Pytest.
* **`security_scan.yml`**: SAST Code Scans, Code Integrity Audits und BSI Compliance Check.
* **`auto-assign.yml`**: Automatisches Reviewer-Assignment für PRs.

---

# Sky OS – Das Framework

**Sky OS – Das Framework** ist ein 100 % freies, lokales, quelloffenes und rechtlich sicheres Multi-Agenten-Betriebssystem, das auf lokaler Hardware läuft und kompromisslose Datensouveränität mit modernster Automatisierung verbindet.

---

## 🏛️ Die 15 Departments (Das organisatorische Rückgrat)
Das System ist in 15 spezialisierte Fachbereiche unterteilt, die jeweils von einem virtuellen "Sky-Leader" und integrierter MCP+CIP-Logik gesteuert werden:
1. **Executive Leadership** (Sky-EXE Leader) – Strategie & Ressourcen
2. **Account Management** (Sky-ACC Leader) – Kunden & Onboarding
3. **Strategy & Planning** (Sky-STR Leader) – Marktanalysen & Roadmaps
4. **Creative Department** (Sky-CRE Leader) – Design & visuelle Konsistenz
5. **Content Marketing** (Sky-CON Leader) – Inhalte & Funnel-Distribution
6. **SEO** (Sky-SEO Leader) – Suchmaschinenoptimierung
7. **Paid Media/PPC** (Sky-PAI Leader) – Kampagnen & ROAS
8. **Social Media Management** (Sky-SOC Leader) – Social-Präsenz & Cadence
9. **Email Marketing** (Sky-EMA Leader) – Sequenzen & Deliverability
10. **Analytics/BI** (Sky-ANA Leader) – KPIs & Predictive Modeling
11. **Development** (Sky-DEV Leader) – Code, Tests & Sicherheit
12. **Operations/Admin** (Sky-OPE Leader) – Buchhaltung & Compliance
13. **Media Buying** (Sky-MED Leader) – Verhandlungen & Budgetierung
14. **Community Management** (Sky-COM Leader) – Moderation & Member Journey
15. **Project Management** (Sky-PRO Leader) – Koordination & Zeitpläne

---

## 🛡️ Sicherheit & Architektur
* **Offline-First Digital Twin:** Keine ungewollten Cloud-Abhängigkeiten; alle Daten bleiben auf deiner Festplatte.
* **Quantensicheres Audit-Ledger (`quantum_ledger.py`):** Jede Transaktion, jeder Befehl und jedes Event wird per **SHA3-256** in einer unveränderbaren Hash-Kette mathematisch versiegelt.
* **Sovereign Payment Gateway:** Direkte, eigenständige Webhook-Anbindungen für **PayPal, Venmo und Revolut** ohne versteckte Zwischenhändler.
* **Dual-Interface:** Wahlfreiheit zwischen dem lokalen Web-Chat-Interface (Port `7860`) und der mobilen Anbindung per MCP-Brücke (Port `8001`).
* **Compliance & Zertifizierungen:** SkyOS basiert auf **GitHub Enterprise Cloud** mit **SOC 1/2 Type 2** und **PCI DSS 4.0.1** Zertifizierungen. Details siehe [COMPLIANCE.md](COMPLIANCE.md).

---

## 🚀 Schnellstart (Installation & Betrieb)

Voraussetzungen: Docker und Docker Compose auf deinem ThinkPad (WSL) installiert.

1. **Repository klonen / Ordner öffnen** im Terminal.
2. **Abhängigkeiten & Skripte prüfen**, dass alle `.py` und `.json` Dateien im Hauptverzeichnis liegen.
3. **Docker-Container starten:**
   ```bash
   docker compose up --build -d
   ```

---

## 🤖 Discord Support-Bot

SkyOS enthält einen integrierten Discord-Chatbot, der lokale Ollama-Modelle für Support-Anfragen nutzt.

### Einrichtung

1. **Discord Bot erstellen:**
   - Gehe zu [Discord Developer Portal](https://discord.com/developers/applications)
   - Erstelle eine neue Application und füge einen Bot hinzu
   - Kopiere den Bot-Token

2. **Token konfigurieren:**
   ```bash
   cp .env.example .env
   # Öffne .env und setze deinen Token:
   DISCORD_BOT_TOKEN=dein_token_hier
   ```

3. **Bot starten:**
   ```bash
   # Lokal
   npm run discord

   # Mit Docker (alle Dienste)
   docker compose up -d
   ```

### Features

- **System-Prompt:** Bot antwortet als SkyOS Support-Assistent
- **Konversationsgedächtnis:** Behält den Kontext pro Kanal (10 Nachrichten)
- **Embed-Antworten:** Formaterte Antworten mit Timestamp und Footer
- **Slash-Befehl:** `/help` zeigt Hilfe-Embed
- **DM-Support:** Bot antwortet auch auf Direktnachrichten

### Konfiguration

| Variable | Standard | Beschreibung |
|---|---|---|
| `DISCORD_BOT_TOKEN` | – | Erforderlich: Dein Discord Bot-Token |
| `OLLAMA_HOST` | `http://127.0.0.1:11434` | Ollama-Server-Adresse |
| `OLLAMA_MODEL` | `llama3` | Verwendetes LLM-Modell |

---

## 🔗 SkyOS Bridge (MCP + Ollama)

Die Bridge ist das Herzstück der SkyOS-Architektur und verbindet alle Komponenten:

### Endpunkte

| Endpoint | Methode | Beschreibung |
|---|---|---|
| `/api/command` | POST | Ollama-Chat (Befehl an LLM senden) |
| `/api/discord` | POST | Discord-Event-Relay (für Flutter-App) |
| `/api/mcp/tools` | GET | Verfügbare MCP-Tools auflisten |
| `/api/mcp/call` | POST | MCP-Tool ausführen |
| `/api/health` | GET | Health-Check |

### MCP-Tools

| Tool | Beschreibung |
|---|---|
| `sky_os_execute` | Führt Befehle in den 15 Departments aus |
| `discord_relay` | Sendet Events an Discord-Gateway |
| `vision_analysis` | Startet Vision-AI-Analyse (Mock) |

### Beispiel: MCP-Tool aufrufen

```bash
curl -X POST http://localhost:3000/api/mcp/call \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "sky_os_execute",
    "arguments": {
      "command": "Status aller Departments",
      "department": "Development",
      "model": "llama3"
    }
  }'
```

---

## 📱 Flutter-App Integration

Die Flutter-App (`skyos_overlay`) verbindet sich mit der Bridge über HTTP:

- **Discord-Relay:** `POST http://localhost:3000/api/discord`
- **MCP-Tools:** `POST http://localhost:3000/api/mcp/call`
- **Vision AI:** Wird über MCP-Tool `vision_analysis` aufgerufen

Die App unterstützt:
- **Spracherkennung** (Bluetooth-fähig, Deutsch)
- **Video-Import und -Player** mit Timeline-Trimming
- **Persona-Switch** (Sky Meilin / Molina Hill)
- **Jetpack Publish** (Social Media Broadcast)
- **Discord-Gateway** für Event-Sync

---

## 🐳 Docker-Dienste

| Dienst | Port | Beschreibung |
|---|---|---|
| `skyos-chat` | 7860 | Web-Chat-Interface |
| `skyos-mcp` | 8001 | MCP-Bridge (Python) |
| `skyos-payment` | 8002 | Payment-Gateway |
| `skyos-bridge` | 3000 | Express.js Bridge (Ollama + MCP) |
| `skyos-discord` | – | Discord Support-Bot |
| `skyos-security` | 8003 | Security Agent (Secret Scanning, WORM Audit) |
| `skyos-mcp-v2` | 8000 | MCP v2 (Streaming, NotebookLM Bridge, WordPress) |
| `skyos-mcp-v3` | 8004 | MCP v3 (v2 + SecurityAgent Integration) |

---

## 📝 WordPress.org Integration

Sky OS Framework unterstützt die automatische Veröffentlichung von Inhalten auf **WordPress.org**-basierten Blogs über die MCP-Bridge.

### Features
- **Automatisches Publishing:** Generierte Artikel und Clips werden direkt an deine WordPress-Instanz gesendet
- **Docker-Integration:** WordPress läuft als separater Container im selben Netzwerk
- **Offline-Queue:** Bei nicht erreichbarer WordPress-Instanz werden Beiträge lokal zwischengespeichert

### Endpunkte
| Endpoint | Methode | Beschreibung |
|---|---|---|
| `/publish/wordpress` | POST | Beitrag an WordPress senden |

### Konfiguration
```bash
# In docker-compose.yml oder .env
WORDPRESS_URL=http://localhost:8080/wp-json/wp/v2/posts
```

---

## 🔄 Git & Versionskontrolle

Sky OS Framework verwendet **Git** für die Versionskontrolle und folgt dem **Conventional Commits**-Standard.

### Branch-Strategie
- **`main`** – Produktive, stabile Version
- **`develop`** – Entwicklungsbranch für neue Features
- **`feature/*`** – Feature-Branches für neue Funktionen
- **`hotfix/*`** – Kritische Fehlerbehebungen

### Commit-Nachrichten
Folge dem Conventional Commits-Format:
```
type(scope): Beschreibung

- feat: Neue Funktion
- fix: Fehlerbehebung
- docs: Dokumentation
- chore: Wartungsaufgaben
- refactor: Code-Verbesserung ohne Funktionsänderung
```

### Beispiel
```bash
git checkout -b feature/wordpress-publish
git commit -m "feat(publish): WordPress-Publishing-Endpunkt hinzugefügt"
git push origin feature/wordpress-publish
```

---

## 🐙 GitHub & Open-Source-Entwicklung

Sky OS Framework wird als **Open-Source-Projekt** auf GitHub entwickelt und gepflegt.

### Repository-Struktur
- **[Issues](https://github.com/Sky-OS-Framework/Sky-Os-Framework/issues)** – Bug-Reports und Feature-Requests
- **[Pull Requests](https://github.com/Sky-OS-Framework/Sky-Os-Framework/pulls)** – Code-Beiträge und Reviews
- **[Discussions](https://github.com/Sky-OS-Framework/Sky-Os-Framework/discussions)** – Community-Diskussionen
- **[Wiki](https://github.com/Sky-OS-Framework/Sky-Os-Framework/wiki)** – Dokumentation und Anleitungen

### Mitwirken
1. **Fork** das Repository
2. **Erstelle einen Feature-Branch** (`git checkout -b feature/meine-funktion`)
3. **Commite deine Änderungen** (`git commit -m "feat: meine funktion"`)
4. **Push den Branch** (`git push origin feature/meine-funktion`)
5. **Erstelle einen Pull Request** auf GitHub

### Code of Conduct
Dieses Projekt folgt dem [Code of Conduct](CODE_OF_CONDUCT.md). Bitte lese und beachte ihn, bevor du beitragst.

---

## 💖 Open Source Funding

Sky OS Framework ist ein **100 % freies und quelloffenes** Projekt. Deine Unterstützung hilft, die Entwicklung und Wartung zu finanzieren.

### Unterstützen
| Plattform | Link | Beschreibung |
|---|---|---|
| **PayPal** | [paypal.me/SkyOS](https://paypal.me/SkyOS) | Einmalige oder monatliche Spenden |
| **Venmo** | `@Sky-OS` | Schnelle Unterstützung via Venmo |
| **Revolut** | [Revolut Link](https://revolut.com/pay/SkyOS) | Kryptos-freundliche Spenden |

### Enterprise-Support
Für Unternehmen, die Sky OS Framework in Produktion einsetzen, bieten wir:
- **Prioritäts-Support** – Direkter Zugang zum Entwicklungsteam
- **Custom Features** – Maßgeschneiderte Funktionen für deine Anforderungen
- **Schulungen** – Workshops und Onboarding für dein Team

Kontaktiere uns unter **support@sky-os.framework** für ein individuelles Angebot.

---

*Danke an alle Beitragenden, Unterstützer und die Community, die Sky OS Framework möglich machen.*
