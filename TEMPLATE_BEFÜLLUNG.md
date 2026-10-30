# Sky OS Framework – Template-Befüllungsanleitung

## Überblick

Dieses Dokument ist deine **Schritt-für-Schritt-Anleitung**, um das Sky OS Framework-Template mit echtem Code zu befüllen. Das Template ist ein Architektur-Gerüst, das die Struktur vordefiniert, aber die meisten Komponenten noch als Stubs (Platzhalter) enthält.

---

## Inhaltsverzeichnis

1. [Projektstruktur im Überblick](#1-projektstruktur-im-überblick)
2. [Was ist bereits funktional?](#2-was-ist-bereits-funktional)
3. [Was muss befüllt werden?](#3-was-muss-befüllt-werden)
4. [Schritt-für-Schritt: Befüllung nach Komponenten](#4-schritt-für-schritt-befüllung-nach-komponenten)
5. [Deinen verteilten Code identifizieren](#5-deinen-verteilten-code-identifizieren)
6. [15 Departments verstehen](#6-15-departments-verstehen)
7. [Testing und Validierung](#7-testing-und-validierung)
8. [GitHub CI/CD Pipeline](#8-github-cicd-pipeline)
9. [Checkliste: Wann ist das Template fertig?](#9-checkliste-wann-ist-das-template-fertig)

---

## 1. Projektstruktur im Überblick

```
Sky-Os-Framework/
├── .github/workflows/          # GitHub Actions CI/CD-Pipeline
│   └── ci.yml                  # Build, Lint, Test Workflow
├── src/                        # Next.js Frontend (React + TypeScript)
│   ├── app/                    # Seiten und API-Endpunkte
│   │   ├── page.tsx            # Hauptseite
│   │   └── api/oauth/          # OAuth-Endpunkte (Fanvue)
│   ├── lib/                    # Bibliothekscode
│   │   ├── fanvue.ts           # Fanvue-API-Integration
│   │   ├── oauth.ts            # OAuth/PKCE-Logik
│   │   └── session.ts          # Session-Management
│   └── env.ts                  # Umgebungsvariablen-Validierung
├── chat_interface.py           # Chat-Oberfläche (Port 7860)
├── mcp_server.py               # MCP-Bridge (Port 8001)
├── payment_gateway.py          # Payment-Gateway (Port 8002)
├── quantum_ledger.py           # Audit-Protokoll (SHA3-256)
├── publisher.py                # WordPress-Publisher
├── departments.json            # Definition der 15 Departments
├── docker-compose.yml          # Docker-Container-Konfiguration
├── requirements.txt            # Python-Abhängigkeiten
├── package.json                # Node.js-Abhängigkeiten
└── .env.example                # Beispiel-Umgebungsvariablen
```

### Die drei Schichten des Frameworks

| Schicht | Technologie | Zweck |
|---|---|---|
| **Frontend** | Next.js + React | Benutzeroberfläche, OAuth-Login |
| **Backend-Dienste** | Python + FastAPI | MCP-Bridge, Chat, Payment |
| **Infrastruktur** | Docker + Quantum Ledger | Container, Audit-Protokoll |

---

## 2. Was ist bereits funktional?

### ✅ Funktionale Komponenten (müssen nicht befüllt werden)

| Komponente | Datei | Status |
|---|---|---|
| **Quantum Ledger** | `quantum_ledger.py` | ✅ Voll funktional – SHA3-256 Hash-Kette für Audit-Protokolle |
| **Next.js OAuth** | `src/lib/oauth.ts`, `src/lib/fanvue.ts` | ✅ Fanvue OAuth-Flow funktioniert |
| **Session-Management** | `src/lib/session.ts` | ✅ JWT-basierte Sessions |
| **Docker-Compose** | `docker-compose.yml` | ✅ Startet 3 Container korrekt |
| **GitHub CI/CD** | `.github/workflows/ci.yml` | ✅ Build, Lint, Test Pipeline |

### ⚠️ Teilweise funktionale Komponenten (benötigen Ergänzungen)

| Komponente | Datei | Was fehlt |
|---|---|---|
| **Payment-Gateway** | `payment_gateway.py` | Webhook-Signatur-Verifikation, echte Zahlungsabwicklung |
| **WordPress Publisher** | `publisher.py` | Echte URL und Credentials (derzeit Platzhalter) |

### ❌ Nicht implementierte Komponenten (müssen befüllt werden)

| Komponente | Datei | Was zu tun ist |
|---|---|---|
| **MCP-Bridge** | `mcp_server.py` | Echte Tool-Ausführung statt Mock-Antwort |
| **Chat-Interface** | `chat_interface.py` | JavaScript-Logik, WebSocket, Befehlsverarbeitung |
| **15 Departments** | `departments.json` | Echte Implementierung der Department-Logik |
| **Circuit Breaker** | Nicht vorhanden | Implementierung des Fehlerbehandlungs-Musters |
| **Meta-Learning** | Nicht vorhanden | Implementierung der Re-Evaluationslogik |
| **Docker-Sandbox Freeze** | Nicht vorhanden | Implementierung der Sandbox-Freeze-Funktion |

---

## 3. Was muss befüllt werden?

### Priorität 1: Kernfunktionalität

Diese Komponenten sind grundlegend für den Betrieb des Frameworks:

1. **MCP-Bridge** – Die Brücke zwischen externen Aufrufen und den Departments
2. **Chat-Interface** – Die Benutzeroberfläche für Interaktion
3. **Payment-Gateway** – Vollständige Zahlungsverarbeitung

### Priorität 2: Departments

Jedes der 15 Departments in `departments.json` benötigt eine echte Implementierung. Die JSON-Datei definiert nur die Struktur, nicht die Logik.

### Priorität 3: Fortgeschrittene Features

- Circuit Breaker (Fehlerbehandlung)
- Meta-Learning-Re-Evaluation
- Docker-Sandbox-Freeze
- Agenten-Neubereitstellung

---

## 4. Schritt-für-Schritt: Befüllung nach Komponenten

### Schritt 1: MCP-Bridge befüllen (`mcp_server.py`)

**Aktueller Zustand:**
- Der Endpunkt `/mcp/call` akzeptiert nur `sky_os_execute`
- Die Antwort ist eine Mock-Nachricht: `"Aktion '{action}' erfolgreich durch das Framework ausgeführt."`
- Keine echte Code-Ausführung findet statt

**Was zu tun ist:**
1. Öffne `mcp_server.py`
2. Erweitere die Tool-Liste um alle Tools, die die 15 Departments bereitstellen
3. Ersetze die Mock-Antwort durch echte Aufrufe an die Department-Funktionen
4. Füge Error-Handling hinzu

**Beispiel-Struktur:**
```python
# Statt nur einer Mock-Antwort, sollte der Code so aussehen:
async def execute_tool(tool_name, parameters):
    if tool_name == "department_1_action":
        result = await department_1.execute(parameters)
    elif tool_name == "department_2_action":
        result = await department_2.execute(parameters)
    # ... usw. für alle Departments
    return result
```

**Deinen Code einfügen:**
- Suche in deinen Downloads und anderen Ordnern nach Code, der Department-Aktionen implementiert
- Kopiere die Logik in entsprechende Module im Projekt
- Verlinke sie in `mcp_server.py`

---

### Schritt 2: Chat-Interface befüllen (`chat_interface.py`)

**Aktueller Zustand:**
- Liefert eine statische HTML-Seite
- Der "Senden"-Button hat keine JavaScript-Logik
- Keine Verbindung zum Backend

**Was zu tun ist:**
1. Füge JavaScript hinzu, das den Button mit dem Backend verbindet
2. Implementiere WebSocket oder HTTP-Aufrufe an die MCP-Bridge
3. Zeige Antworten vom Backend im Chat-Fenster an

**Beispiel-Struktur:**
```javascript
// Im HTML-Teil der chat_interface.py sollte so etwas hinzugefügt werden:
document.getElementById('sendButton').addEventListener('click', async () => {
    const message = document.getElementById('messageInput').value;
    const response = await fetch('http://localhost:8001/mcp/call', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({tool: 'sky_os_execute', parameters: {action: message}})
    });
    const result = await response.json();
    displayMessage(result.response);
});
```

**Deinen Code einfügen:**
- Suche nach Chat-UI-Code oder WebSocket-Implementierungen
- Integriere die Logik in `chat_interface.py`

---

### Schritt 3: Payment-Gateway vervollständigen (`payment_gateway.py`)

**Aktueller Zustand:**
- Webhook-Endpunkte für PayPal und Revolut existieren
- **Keine Signatur-Verifikation** – Sicherheitsrisiko!
- Nur Protokollierung, keine echte Zahlungsabwicklung

**Was zu tun ist:**
1. Füge Webhook-Signatur-Verifikation hinzu (PayPal: `certify-signature`, Revolut: API-Key-Check)
2. Implementiere Status-Updates für Bestellungen
3. Füge Venmo-Webhook-Endpunkt hinzu (wird in README erwähnt, fehlt im Code)

**Beispiel-Struktur:**
```python
# PayPal Signatur-Verifikation
from paypalrestsdk import Webhook

def verify_paypal_signature(payload, headers):
    webhook = Webhook('YOUR_WEBHOOK_ID')
    return webhook.verify_signature({
        'transmission_id': headers['PAYPAL-TRANSMISSION-ID'],
        'transmission_time': headers['PAYPAL-TRANSMISSION-TIME'],
        'cert_url': headers['PAYPAL-CERT-URL'],
        'webhook_id': 'YOUR_WEBHOOK_ID',
        'webhook_event': payload
    })
```

**Deinen Code einfügen:**
- Suche nach Payment-Integration-Code
- Achte auf API-Keys und Secrets – diese gehören in `.env`, nicht in den Code

---

### Schritt 4: WordPress Publisher konfigurieren (`publisher.py`)

**Aktueller Zustand:**
- Code zum Erstellen von WordPress-Beiträgen als Entwurf existiert
- URL und Credentials sind Platzhalter (`deine-wordpress-domain.com`)

**Was zu tun ist:**
1. Ersetze die Platzhalter-URL durch deine echte WordPress-Domain
2. Füge die WordPress-API-Credentials in `.env` ein
3. Lade die Credentials aus `.env` statt aus dem Code

**Beispiel:**
```python
import os

WORDPRESS_URL = os.getenv('WORDPRESS_URL')  # Statt 'deine-wordpress-domain.com'
WORDPRESS_USER = os.getenv('WORDPRESS_USER')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD')
```

**.env-Einträge hinzufügen:**
```
WORDPRESS_URL=https://deine-domain.com
WORDPRESS_USER=dein-benutzername
WORDPRESS_PASSWORD=dein-passwort
```

---

### Schritt 5: Departments implementieren

**Aktueller Zustand:**
- `departments.json` listet 15 Departments mit Namen und Beschreibungen
- Keine Python- oder TypeScript-Implementierung existiert

**Was zu tun ist:**
1. Erstelle einen Ordner `departments/` im Projekt
2. Für jedes Department: Erstelle eine Python-Datei mit der Logik
3. Verlinke die Departments in `mcp_server.py`

**Beispiel-Struktur:**
```
departments/
├── __init__.py
├── department_1.py
├── department_2.py
└── ... (bis department_15)
```

**Jede Department-Datei sollte enthalten:**
```python
# departments/department_1.py
class Department1:
    async def execute(self, parameters):
        # Hier kommt die echte Logik hin
        result = ...
        return result
```

**Deinen Code einfügen:**
- Suche in deinen Downloads nach Code, der zu den Department-Beschreibungen passt
- Ordne den Code den richtigen Departments zu
- Kopiere und passe den Code in die entsprechenden Dateien ein

---

### Schritt 6: Fortgeschrittene Features

#### Circuit Breaker
Ein Circuit Breaker verhindert, dass das System bei wiederholten Fehlern weiter versucht, eine fehlerhafte Aktion auszuführen.

**Was zu tun ist:**
- Erstelle eine `circuit_breaker.py` Datei
- Implementiere das Circuit Breaker-Muster (Closed → Open → Half-Open Zustände)
- Wende es auf alle Department-Aufrufe an

#### Meta-Learning-Re-Evaluation
Ein System, das aus vergangenen Aktionen lernt und die Bewertung verbessert.

**Was zu tun ist:**
- Erstelle eine `meta_learning.py` Datei
- Implementiere eine Logik, die vergangene Ergebnisse analysiert
- Passe die Bewertungskriterien basierend auf den Ergebnissen an

#### Docker-Sandbox-Freeze
Ein Mechanismus, um den Zustand einer Docker-Sandbox zu speichern und wiederherzustellen.

**Was zu tun ist:**
- Erstelle eine `sandbox_manager.py` Datei
- Implementiere `freeze()` und `restore()` Funktionen
- Nutze Docker-API für Container-Snapshots

---

## 5. Deinen verteilten Code identifizieren

### Schritt 1: Code-Sammlung

Sammle alle Code-Dateien aus:
- Downloads-Ordner
- Andere Projekte und Ordner
- Externe Speicherorte

### Schritt 2: Code-Kategorisierung

Ordne jede Code-Datei einer Kategorie zu:

| Kategorie | Ziel-Datei im Template |
|---|---|
| MCP-Tool-Logik | `mcp_server.py` oder `departments/` |
| Chat-Funktionalität | `chat_interface.py` |
| Payment-Logik | `payment_gateway.py` |
| WordPress-Integration | `publisher.py` |
| Circuit Breaker | `circuit_breaker.py` (neu) |
| Meta-Learning | `meta_learning.py` (neu) |
| Sandbox-Management | `sandbox_manager.py` (neu) |
| Frontend-Komponenten | `src/app/` oder `src/components/` |
| Konfiguration | `.env` oder `config/` |

### Schritt 3: Code-Integration

Für jede Code-Datei:
1. **Prüfe die Abhängigkeiten** – Welche Bibliotheken werden importiert? Sind sie in `requirements.txt` (Python) oder `package.json` (Node.js) vorhanden?
2. **Passe die Pfade an** – Ändere Import-Pfade, um der neuen Projektstruktur zu entsprechen
3. **Füge Tests hinzu** – Wenn möglich, schreibe einfache Tests für die integrierte Logik
4. **Dokumentiere** – Füge Kommentare hinzu, die erklären, was der Code tut

---

## 6. 15 Departments verstehen

Die `departments.json` definiert 15 Departments. Jedes Department repräsentiert einen Bereich des Frameworks mit spezifischen Fähigkeiten.

### So findest du den passenden Code:

1. **Lies die Department-Beschreibung** in `departments.json`
2. **Suche in deinen Downloads** nach Code, der ähnliche Funktionen erfüllt
3. **Vergleiche die MCP+CIP-Protokolle** – Diese beschreiben, welche Tools und Aktionen das Department bereitstellen soll
4. **Ordne den Code dem Department zu** und integriere ihn

### Beispiel-Workflow:

Angenommen, Department 3 ist "Content-Erstellung":
- Suche nach Code, der Bilder, Videos oder Text generiert
- Prüfe, ob der Code die in der JSON beschriebenen Tools implementiert
- Integriere den Code in `departments/department_3.py`
- Verlinke die Tools in `mcp_server.py`

---

## 7. Testing und Validierung

### Python-Tests

Nach jeder Code-Integration:
```bash
# Tests ausführen
pytest

# Oder spezifische Tests
pytest test_mcp_server.py
pytest test_departments/
```

### Next.js-Tests

```bash
# Frontend-Tests ausführen
npm test

# Oder mit Coverage
npm run test:coverage
```

### Docker-Tests

```bash
# Alle Dienste starten
docker-compose up -d

# Logs prüfen
docker-compose logs -f

# Dienste stoppen
docker-compose down
```

### Manuelles Testing

1. **Chat-Interface**: Öffne `http://localhost:7860` und teste die Interaktion
2. **MCP-Bridge**: Sende einen POST-Anfrage an `http://localhost:8001/mcp/call`
3. **Payment-Gateway**: Simuliere einen Webhook an `http://localhost:8002/webhook/paypal`

---

## 8. GitHub CI/CD Pipeline

Die GitHub Actions Pipeline (`.github/workflows/ci.yml`) automatisiert Build, Lint und Test.

### Was die Pipeline macht:

1. **Trigger**: Bei jedem Push und Pull-Request
2. **Node.js Setup**: Installiert Node.js und cached Abhängigkeiten
3. **Python Setup**: Installiert Python und cached Abhängigkeiten
4. **Lint**: Prüft Code-Qualität (ESLint für TypeScript, flake8 für Python)
5. **Test**: Führt alle Tests aus (Jest für Frontend, pytest für Backend)
6. **Build**: Baut das Next.js-Frontend

### Wie du die Pipeline anpasst:

1. Öffne `.github/workflows/ci.yml`
2. Füge neue Test-Schritte hinzu, wenn du neue Tests schreibst
3. Passe die Python- oder Node.js-Version an, wenn nötig
4. Füge Deployment-Schritte hinzu, wenn du automatisches Deployment möchtest

---

## 9. Checkliste: Wann ist das Template fertig?

### Kernfunktionalität
- [ ] MCP-Bridge führt echte Aktionen aus (keine Mock-Antworten)
- [ ] Chat-Interface sendet und empfängt Nachrichten
- [ ] Payment-Gateway verifiziert Webhook-Signaturen
- [ ] WordPress-Publisher hat echte Credentials

### Departments
- [ ] Alle 15 Departments haben Implementierungsdateien
- [ ] Jedes Department ist in `mcp_server.py` verlinkt
- [ ] Departments können über die MCP-Bridge aufgerufen werden

### Fortgeschrittene Features
- [ ] Circuit Breaker ist implementiert
- [ ] Meta-Learning-Re-Evaluation funktioniert
- [ ] Docker-Sandbox-Freeze ist implementiert

### Qualität
- [ ] Alle Tests bestanden (Python + Next.js)
- [ ] GitHub CI/CD Pipeline ist grün
- [ ] Docker-Container starten ohne Fehler
- [ ] Dokumentation ist aktualisiert

### Sicherheit
- [ ] Keine Secrets im Code (nur in `.env`)
- [ ] Webhook-Signaturen werden verifiziert
- [ ] `.env` ist in `.gitignore`

---

## Häufige Fragen

### Wo finde ich meinen verteilten Code?
- Prüfe deinen Downloads-Ordner
- Suche nach Projekten mit ähnlichen Namen oder Funktionen
- Achte auf Code, der Department-Beschreibungen entspricht

### Was mache ich, wenn ich Code nicht zuordnen kann?
- Dokumentiere den Code in einem `unassigned/` Ordner
- Notiere, was der Code tut
- Suche später nach dem passenden Department

### Wie füge ich ein neues Department hinzu?
1. Füge das Department in `departments.json` hinzu
2. Erstelle eine Python-Datei in `departments/`
3. Verlinke die Tools in `mcp_server.py`
4. Schreibe Tests für die neue Funktionalität

### Was mache ich mit `.env.example`?
- Kopiere `.env.example` zu `.env`
- Fülle die echten Werte ein
- **Committe niemals `.env`** – es ist in `.gitignore`

---

## Nützliche Befehle

```bash
# Projekt starten
docker-compose up -d

# Frontend entwickeln
npm run dev

# Tests ausführen
npm test
pytest

# Linting
npm run lint

# Build
npm run build

# Docker-Logs
docker-compose logs -f

# GitHub Actions manuell auslösen
gh workflow run ci.yml
```

---

## Zusammenfassung

Dieses Template ist dein **Architektur-Skelett**. Es definiert die Struktur, aber die Muskeln (die Logik) musst du noch einfügen. Folge dieser Anleitung Schritt für Schritt, und du wirst das Template mit deinem verteilten Code befüllen können.

**Priorität:** Beginne mit den Kernkomponenten (MCP-Bridge, Chat, Payment), dann die Departments, dann die fortgeschrittenen Features.

**Geduld:** Da du keine Programmierkenntnisse hast, nimm dir Zeit für jeden Schritt. Die Anleitung erklärt, was zu tun ist – wenn du bei einem Schritt feststeckst, kann dir ein Entwickler oder KI-Assistent helfen.
