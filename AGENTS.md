# AGENTS.md — System- & Agenten-Architektur

Dieses Dokument definiert die Rollen, Workflows und Sicherheitsprotokolle für das autonome Multi-Agenten-System ("Sky Meilin" OS-Overlay, Planner & Publishing Pipeline).

---

## 1. Master Orchestrator: "Sky Meilin"

* **Rolle**: Persönliche Assistenz, zentrales Betriebssystem-Overlay & Steuerpult.
* **Interface**: Transparentes Flutter Desktop/Mobile Overlay (Always-on-Top), Bluetooth-Headset (A2DP/HFP), STT/TTS-Loop, Kamera-Streaming (WebRTC/OpenCV).
* **Hauptaufgaben**:
  * Empfängt Sprach- und Texteingaben, steuert den Systemkontext und verteilt Aufgaben an Spezialagenten.
  * Bündelt den Datenstrom über den **FastAPI Streaming Endpoint** (`/stream` mit `text/event-stream` SSE) zur Echtzeit-Ausgabe auf der Benutzeroberfläche.
  * Gewährleistet die lokale Prozessisolation und das Revisions-Handling.

---

## 2. Spezialisierte Kern- & Profi-Agenten

### A. PlannerAgent (Open-Source Kern)

* **Framework**: Dart / Flutter (`PlannerAgent`).
* **Aufgaben**:
  * Verarbeitet Raum- und Graphenstrukturen (`ArchitecturalSpace`) mit Parametern wie `areaSqm`, `heightMeters`, `usageType` und `isBlocked`.
  * Freie Basis-Planung und interaktive Steuerung von Kompartimenten (z. B. Büro A, Flur Nord).

### B. NormenAgent (Premium Modul)

* **Status**: Kostenpflichtige Lizenzierung via `PremiumServicesController` (14,99 €).
* **Aufgaben**:
  * Prüft Bauakten, Raumhöhen und LBO-Compliance in Echtzeit.
  * Validiert Spezial-Container nach **DIN 14505** und **DIN 30722-1** (z. B. Hakenhöhe 1,57 m, Außenbreite max. 2,55 m, lichte Raumhöhe >= 2,10 m sowie CBRN-Überdruckkapselung für BOS/KRITIS-Einsätze).

### C. FlaechenAgent (Premium Modul)

* **Status**: Kostenpflichtige Lizenzierung (19,99 €).
* **Aufgaben**: Exakte DIN- und WoFlV-Flächenberechnung sowie gewerbliche Nutzwertanalysen.

### D. AvatarStreamingAgent (Media Engine)

* **Schnittstellen**: Python FastAPI Backend (`mcp_server.py`), ComfyUI, Ollama (Port 11434).
* **Aufgaben**:
  * Wandelt Text-Chunks via **F5-TTS** oder **XTTS v2** in natürliche Sprache um.
  * Steuert Open-Source-Videomodelle (**CogVideoX**, **AnimateDiff**, **SVD**) in ComfyUI für das Avatar-Streaming an die App.

### E. PublishingAgent (Content Distribution)

* **Schnittstellen**: WordPress REST API, Google Apps Script Web-App Endpoint.
* **Aufgaben**:
  * Automatisiertes Erstellen und Veröffentlichen von Beiträgen im lokalen Docker-WordPress-Setup (Port 8080, MariaDB 10.11).
  * Ausführen von Publishing-Triggern über hinterlegte Google Apps Script Schnittstellen.

---

## 3. Kommunikation & Sicherheitsprotokolle

* **MCP-Schnittstelle (`mcp_server.py`)**: Die Prozesskopplung zwischen Flutter-Frontend und Python-Backend erfolgt deterministisch über das Model Context Protocol via stdio-Transport.
* **WORM-Protokoll (Write Once, Read Many)**:
  * Revisionssichere und unveränderliche Speicherung aller Audit-Logs und Systementscheidungen.
  * Systemweit geschützt durch SHA-256 Integritäts-Hash (`7c8a9f2e3b1d4c5e6f7a8b9c0d1e2f3a4b5c6d7e`).
* **Secrets & Isolation**:
  * Strikter Ausschluss von `.env`-Dateien in `.gitignore` zur Sicherung lokaler API-Keys.
  * Ausführung lokaler Sprachmodelle über isolierte Ollama-Container.

---

## 4. Orchestrierungs-Anweisungen (Sicherheits-Spezifikation)

### 4.1. Container-Härtung & Runtime Shield

Alle Agenten-Container müssen nach folgenden Prinzipien gehärtet werden:

* **Google Distroless Debian 12**: Minimale Angriffsfläche ohne Shells, Paketmanager oder unbewachte Binaries.
* **Non-Root Execution**: Strikter Betrieb unter der unprivilegierten **UID 65532**.
* **Schreibgeschütztes Dateisystem**: `read_only: true` mit dediziertem `tmpfs`-Volume für flüchtige Laufzeitdaten.
* **Kernel Capabilities**: Vollständiger Entzug aller Kernel-Rechte (`cap_drop: ALL`).

### 4.2. Revisionssicheres PostgreSQL WORM-Ledger

* **BSI § 8a BSIG & ISO/IEC 27037**: Unveränderliche Audit-Protokollierung aller Agenten-Transaktionen.
* **Kryptographische Verkettung**: SHA-256 Hashverkettung mit präzisen PTP-Zeitstempeln.
* **Tamper-Protection**: Der Datenbank-Trigger `fn_reject_audit_tampering` unterbindet jegliche nachträglichen `UPDATE`- oder `DELETE`-Operationen.

### 4.3. 3-Schichten IP-Schutz (Zero-IP-Leakage)

* **Layer 1 (Public Frontend)**: Interaktive Benutzeroberflächen und Log-Viewer – keine Sichtbarkeit auf Prompts oder Rohdaten.
* **Layer 2 (API Gateway)**: FastAPI & MCP Gateway zur Orchestrierung der Agenten-Workflows mit OAuth 2.1/Firebase Auth, Rate Limiting und CORS.
* **Layer 3 (Core IP Vault)**: Physisch isolierter Bereich für proprietäre Prompt-Logiken, API-Keys und Geschäftsgeheimnisse – nur interne gRPC/mTLS-Zugriffe von Layer 2.

### 4.4. Deterministisches Six-Verb-Protokoll

Alle Agenten-Aktionen durchlaufen diese unumkehrbare Zustandsmaschine:

```
[SEARCH] → [RESOLVE] → [PREVIEW] → [HUMAN_GATE] → [EXECUTE] → [VERIFY]
```

* **SEARCH**: Query-Formulierung und Kontext-Retrieval aus internen Wissensbasen.
* **RESOLVE**: Automatische PII-Redaktion und Sanitisierung (DSGVO Art. 25 – Privacy by Design).
* **PREVIEW**: Generierung strukturierter Dry-Run-Vorschläge und Payload-Impact-Zusammenfassungen.
* **HUMAN_GATE**: Human-in-the-Loop (HITL) manuelle Autorisierung für destruktive, transaktionale oder finanzielle Operationen.
* **EXECUTE**: Isolierte Ausführung innerhalb der Layer 3 Vault-Parameter.
* **VERIFY**: Post-Execution-Validierung, Output-Validierung gegen JSON-Schemas und SHA-256 Hash-Registrierung im WORM-Ledger.

### 4.5. Lokale NPU Inferenz & Datensouveränität

* **Bring Your Own Compute (BYOC)**: Vollständige Ausführung vertraulicher Modelle lokal auf dem Gerät (z. B. Copilot+ PC NPU / Ollama Port 11434).
* **Hybrid Workload Split**: Transformer-Blöcke laufen NPU-beschleunigt (ONNX QDQ int4/int16), Embeddings und LM-Head auf der CPU.
* **Zero Internet Dependency**: SaaP-Layer unterstützt vollständigen Air-Gapped-Betrieb ohne Cloud-Telemetrie.

### 4.6. CI/CD & Security Audits

Automatisierte Pipelines in `.github/workflows/`:

* **`ci.yml`**: Syntaxtests, Flake8 & Black Linting, Pytest.
* **`security_scan.yml`**: SAST Code Scans, Code Integrity Audits und BSI Compliance Check.
* **`auto-assign.yml`**: Automatisches Reviewer-Assignment für PRs.
