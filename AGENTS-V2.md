# AGENTS.md — System- & Agenten-Architektur (v2)

Dieses Dokument definiert die Rollen, Workflows und Sicherheitsprotokolle für das autonome Multi-Agenten-System ("Sky Meilin" OS-Overlay, Sicherheitsagent & Publishing Pipeline).

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

### A. SicherheitsAgent (Ehemals PlannerAgent — Core Repository & Compliance Guard)

* **Framework**: Dart / Flutter (`SicherheitsAgent`) & Python Backend (`SecurityAgentService`).
* **Aufgaben**:
  * **Repository-Überwachung**: Überwacht aktiv das Git-Repository (z.B. `Sicherheitsrichtlinien` unter `/workspaces/Sicherheitsrichtlinien` oder `C:\Workspace LM studio`) auf Änderungen, unbefugte Commits und Dateiintegrität.
  * **WORM-Audit-Validierung**: Verifiziert fortlaufend alle SHA-256 Hashes der WORM-Protokolldateien (`worm_audit_log.jsonl`) auf Fälschungssicherheit.
  * **Secret & Leak Protection**: Scannt Repositories und Commits automatisiert auf versehentlich enthaltene `.env`-Dateien, API-Keys oder Passwörter.
  * **DIN- & KRITIS-Compliance**: Integriert die Bausteine zur Prüfung von Spezial-Containern nach **DIN 14505** und **DIN 30722-1** (Hakenhöhe 1,57 m, lichte Raumhöhe >= 2,10 m, CBRN-Überdruckkapselung) sowie allgemeine Bauakten-Normen.
  * **Build & Health Monitor**: Überwacht die Ausführung von Build-Skripten (`run.sh`, `dotnet build`, Flutter-Builds) und schlägt Alarm bei fehlerhaften Artefakten oder unterbrochenen Pipelines.

### B. NormenAgent (Premium Modul)

* **Status**: Kostenpflichtige Lizenzierung via `PremiumServicesController` (14,99 €).
* **Aufgaben**:
  * Tiefenprüfung von Bauakten, Raumhöhen und LBO-Compliance in Echtzeit.
  * Erweitertes Zertifizierungs-Modul für behördliche Abnahmen.

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

* **MCP-Schnittstelle (`mcp_server-v2.py`)**: Die Prozesskopplung zwischen Flutter-Frontend und Python-Backend erfolgt deterministisch über das Model Context Protocol via stdio-Transport.
* **WORM-Protokoll (Write Once, Read Many)**:
  * Revisionssichere und unveränderliche Speicherung aller Audit-Logs und Systementscheidungen durch den `SicherheitsAgent`.
  * Systemweit geschützt durch SHA-256 Integritäts-Hash (`7c8a9f2e3b1d4c5e6f7a8b9c0d1e2f3a4b5c6d7e`).
* **Secrets & Isolation**:
  * Strikter Ausschluss von `.env`-Dateien in `.gitignore` zur Sicherung lokaler API-Keys.
  * Kontinuierlicher Pre-Commit Scan durch den `SicherheitsAgent`.
  * Ausführung lokaler Sprachmodelle über isolierte Ollama-Container.
