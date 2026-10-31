# Comprehensive Überblick: Lokale KI-Agenten, Software-Architekturen und Entwickler-Pipelines

## 1. Executive Summary (Kurzzusammenfassung)

### 1.1 Kernaussagen auf einen Blick

Der strategische Übergang von proprietären Cloud-APIs hin zu privaten, lokal gehosteten KI-Agenten markiert einen zentralen Paradigmenwechsel in der IT-Architektur moderner Unternehmen. Unkalkulierbare Token-Kosten bei kontinuierlicher Belastung, schwankende Latenzen und strikte datenschutzrechtliche Vorgaben zwingen Organisationen zunehmend dazu, auf hochleistungsfähige Open-Weight-Modelle auszuweichen. Die lokale Modellbereitstellung garantiert die uneingeschränkte Souveränität über sensible Unternehmensdaten, eliminiert exogene Vektoren für Datenabflüsse an Drittanbieter und beseitigt künstliche Ratenbeschränkungen sowie laufende Abonnementgebühren vollständig.

Aus operationaler Sicht bieten lokale Architekturen signifikante Performance-Vorteile: Durch die direkte Hardware-Ansteuerung – von modernsten Consumer-GPUs über Enterprise-Workstations bis hin zu Unified-Memory-Systemen der Apple-Silicon-Klasse – erreichen dedizierte Setups eine minimierte Time-To-First-Token (TTFT) sowie hohe Tokens-Per-Second (TPS) Durchsatzraten. Die vollständige Kontrolle über Modell-Updates, Prompt-Injektions-Schutzsysteme und dedizierte GPU-Speicherbereiche garantiert eine hochgradig deterministische und vorhersagbare Ausführungsumgebung für kritische Geschäftsprozesse.

Technologisch basiert dieses Paradigma auf einem integrierten Software-Stack: Inferenz-Engines wie Ollama und vLLM stellen quantisierte Modelle hochperformant bereit, während Frameworks wie LangGraph die zustandsbehaftete, mehrstufige Orchestrierung autonomer Agenten über gerichtete Graphen mit Schleifen, Verzweigungen und erweiterter Persistence übernehmen. Standardisierte Schnittstellen wie das Model Context Protocol (MCP) koppeln KI-Modelle nahtlos an Unternehmenswerkzeuge (z. B. Python-Laufzeitumgebungen, Firecrawl-Websuche oder GitHub-Schnittstellen). Visuelle Verarbeitungs-Engines wie ComfyUI erweitern dieses Ökosystem um komplexe, multimodale Pipelines.

Integriert in bestehende Entwickler-Pipelines lassen sich maßgeschneiderte Automatisierungen sicher ausführen. Die kostenfreie Bereitstellung privater GitHub Actions Marketplace Apps in Kombination mit einer gehärteten Event-Verarbeitung über HMAC-verifizierte Webhooks und Python-Backends ermöglicht hochgradig automatisierte, DSGVO-konforme CI/CD-Prozesse direkt innerhalb der eigenen Infrastrukturgrenzen.

### 1.2 Strategische Kernaussagen in Tabellenform

| Technologische Domäne | Haupterkenntnis / Nutzwert |
|------------------------|---------------------------|
| Lokale LLM-Inferenz | Beseitigt Cloud-Token-Kosten und Drittanbieter-Abhängigkeiten; garantiert 100 % DSGVO-Konformität und absolute Datensouveränität (Privacy by Design). |
| Agenten-Orchestrierung | LangGraph ermöglicht komplexe, zustandsbehaftete Multi-Actor-Workflows mit zyklischen Schleifen, bedingten Verzweigungen, Memory-Persistence und Human-in-the-Loop-Kontrollpunkten. |
| Tool-Integration (MCP) | Das Model Context Protocol standardisiert die sichere, entkoppelte Anbindung lokaler Sprachmodelle an externe Betriebssystem-Tools und Enterprise-Schnittstellen. |
| Multimodale 3-Server-Architektur | Spezialisiertes Zusammenspiel aus vLLM (Exekutiv-Inferenz), Ollama (Chat/Logik-Routing) und ComfyUI (Orchestrierung & visuelle Execution) zur optimalen VRAM-Auslastung. |
| CI/CD & DevSecOps | Private GitHub Actions Marketplace Apps in Verbindung mit HMAC-SHA256-signierten Webhooks ermöglichen kostenlose, datenschutzkonforme Workflow-Automatisierung. |

---

## 2. Strategische & Datenschutzrechtliche Treiber im Unternehmen

### 2.1 Datenschutz & DSGVO-Konformität (Bitkom-Kontext)

Empirische Erhebungen des Branchenverbands Bitkom belegen eine fortschreitende Adoption von Künstlicher Intelligenz im Unternehmenssektor: Bereits 57 % der Unternehmen ab 20 Beschäftigten setzen KI-Technologien aktiv ein. Dennoch offenbart die Datenlage massive regulatorische und administrative Vorbehalte, die eine breite Integration proprietärer Cloud-Dienste hemmen.

**Empirische Bitkom-Metrik (Unternehmensbefragung)**

| Messwert | Strategische Implikation für die IT-Architektur |
|----------|------------------------------------------------|
| KI-Nutzung im Mittelstand (Unternehmen ab 20 Beschäftigten): 57 % | KI ist im operativen Betrieb angekommen; der Bedarf an skalierbaren Architekturen steigt rasch. |
| Datenschutz-Hürden als primäres Einsatzhemmnis: 48 % | Strikte DSGVO-Vorgaben verhindern den Einsatz externer Cloud-Schnittstellen für Kernprozesse. |
| Sorge vor Datenabfluss an Dritte / Cyber-Risiken: 39 % | Bedenken hinsichtlich des Verlusts von IP, Geschäftsgeheimnissen und Personendaten dominieren. |

Der Betrieb einer lokalen On-Premise-KI-Infrastruktur löst diese regulatorischen Blockaden bauartbedingt (Privacy by Design). Da die Inferenz-Berechnungen vollständig auf eigenen physischen Servern oder lokalen Arbeitsplätzen durchgeführt werden, verlässt kein Dokument, kein Prompt und keine Kundenakte das interne Firmennetzwerk.

Infolgedessen entfällt die Notwendigkeit zur Aushandlung komplexer Auftragsverarbeitungsverträge (AVV) mit Cloud-Hyperscalern ebenso wie das Risiko eines ungewollten Modell-Trainings durch Drittanbieter auf proprietären Unternehmensdaten.

### 2.2 Wirtschaftlichkeit & Kostenstruktur

Der operative Betrieb proprietärer Cloud-APIs ist durch ein logarithmisches Kostenrisiko gekennzeichnet. Nutzungsabhängige Token-Abrechnungsmodelle in Kombination mit wiederkehrenden Lizenzgebühren (z. B. bis zu 200 $ pro Nutzer/Monat für Enterprise-Lizenzen) führen bei datenintensiven Agenten-Workflows, großen Kontextfenstern und hoher Frequenz zu unkalkulierbaren OpEx-Steigerungen.

**Cloud-API-Modell (OpEx):**
```
[Laufende Token-Kosten + Abos] ──> Exponentiell skalierende Betriebskosten
```

**Lokales Modell (CapEx):**
```
[Einmalige Hardware-Anschaffung] ──> 0 € Token-Kosten, unbegrenzte Inferenz
```

Die lokale Modell-Bereitstellung eliminiert variable Inferenzkosten und künstliche Rate-Limits vollständig. Nach der primären Investition in dedizierte Compute-Hardware fallen für die Ausführung der Inferenz keinerlei laufende Lizenz- oder API-Gebühren an. IT-Entscheider wandeln dadurch schwankende, unvorhersehbare Betriebsausgaben (OpEx) um in planbare Investitionsausgaben (CapEx), was insbesondere bei hochfrequenten, autonomen Agentenschleifen zu einer schnellen Amortisation führt.

---

## 3. Hardware-Dimensionierung und Modellauswahl

### 3.1 VRAM-Berechnungsformel & Speicherlehre

Bei der Konzeption lokaler KI-Hardware stellt der Grafikspeicher (VRAM) sowie dessen Speicherbandbreite den primären Systemengpass dar. Sprachmodelle müssen für eine effiziente Inferenz vollständig in den adressierbaren GPU-Speicher geladen werden.

Für standardmäßig quantisierte GGUF-Modelle (Standard-Quantisierung Q4_K_M mit ca. 4,9 Bit pro Gewicht bzw. ~0,6 GB pro 1 Milliarde Parameter) gilt folgende mathematische Berechnungsformel für den minimal erforderlichen VRAM:

```
VRAM_req = (N_Params × 0,7 GB) + 3 GB_Buffer
```

Der statische Aufschlag von 3 GB deckt den dynamischen Zwischenspeicher für den Key-Value-Cache (KV-Cache) bei erweiterten Kontextfenstern sowie die Overheads des Grafiktreibers und Betriebssystems ab.

**Architektonische Fehlannahme:** Die weitverbreitete Faustregel "1 GB VRAM pro 1 Milliarde Parameter" ist für quantisierte Produktionsmodelle falsch. Sie trifft ausschließlich auf unkomprimierte FP16-Präzisionen zu und veranlasst Systemarchitekten dazu, den Speicherbedarf von komprimierten GGUF-Modellen um mehr als 40 % zu überschätzen.

**Hybrid CPU/RAM-Offloading:**
Für budgetbeschränkte Setups oder Übergangsarchitekturen bietet sich das sogenannte Hybrid Offloading an. Hierbei werden Modellschichten (Layer Weights) primär im System-Arbeitsspeicher (CPU-RAM) vorgehalten, während rechenintensive Operationen oder der KV-Cache in den VRAM ausgelagert werden. Obwohl diese Methodik die Hardware-Anschaffungskosten drastisch senkt, führt die Begrenzung durch die PCIe-Bus-Transferrate und die im Vergleich zu VRAM deutlich geringere DDR4/DDR5-Speicherbandbreite zu signifikanten Einbußen bei der Token-Durchsatzrate (TPS).

### 3.2 Hardware-Klassen & Performance-Profil

**Consumer-GPUs (Arbeitsplatz & Edge-Setups):**
- **NVIDIA RTX 5060 Ti (16 GB VRAM):** Hocheffiziente Einsteigerkarte für komprimierte Modelle bis 8 Milliarden Parameter (z. B. Phi-4-Mini, Qwen3 4B) mit einem 32k-Kontextfenster.
- **NVIDIA RTX 3070 / RTX 3090:** Dual-RTX-3090-Setups (2x 24 GB = 48 GB VRAM, gebaucht ca. 1.500 $) bieten ein hervorragendes Preis-Leistungs-Verhältnis und ermöglichen das lokale Hostings von 70B-Modellen in Q4_K_M.
- **NVIDIA RTX 5090 (32 GB VRAM):** High-End-Consumer-Klasse (Stand September 2026 ab ca. 4.850 €), bewältigt anspruchsvolle 13B- bis 32B-Modelle mit maximalen Durchsatzraten.

**Enterprise & Workstation Hardware:**
- **NVIDIA RTX 6000 Ada (48 GB VRAM):** Professionelle Workstation-Karte (ca. 10.000 $+), ausgelegt für den unterbrechungsfreien 24/7-Dauerbetrieb von 70B-Modellen mit ECC-Speicherschutz.
- **Unified Memory Systems (Apple Silicon):** Apple MacBooks & Mac Studio (M3/M5 Architekturen): Nutzen eine Hochgeschwindigkeits-Architektur mit gemeinsam genutztem Arbeitsspeicher (Unified Memory) von bis zu 512 GB RAM. Ein Mac Studio mit M3 Max und 64 GB RAM führt ein DeepSeek-R1 70B (Q4_K_M) mit stabilen ~8 Token/s aus, während Systeme mit 512 GB RAM extrem große Parameterklassen ohne dedicated GPU-Cluster adressieren können.

### 3.3 Modellübersicht & Anwendungsbereiche

| Modell | Parametergröße | Kontextfenster | Lizenz / Besonderheit | Primärer Enterprise-Anwendungsbereich |
|--------|---------------|----------------|----------------------|--------------------------------------|
| Phi-4-Mini Instruct | 3,8B | 128.000 Token | Open Weight | Hochspezialisiert auf logisches Reasoning und mathematische Aufgaben; starkes synthetisches Training. |
| Qwen3 | 4B / 27B / 70B | 128.000 Token | Open Weight | Allgemeine Konversationslogik, funktionale Tool-Aufrufe und native Vision-Enkodierung. |
| Gemma 3 | 4B | 128.000 Token | Open Weight | Multimodale Text- und Bildverarbeitung mit robuster mehrsprachiger Abdeckung. |
| Gemma 4 | 12B / E4B (NVFP4) | Variabel | Apache 2.0 (Releases seit April 2026) | Exekutive Agenten-Tasks, hochperformante Code-Generierung und vLLM-Inferenz. |
| Mistral / Llama | 7B / 8B / 70B | Bis zu 128k | Permissiv / Open | Enterprise General-Purpose-Agenten, RAG-Pipelines und strukturierte Datenanalyse. |

---

## 4. Software-Stack & Agenten-Orchestrierung

### 4.1 Framework-Analyse: LangGraph vs. Visuelle Automatisierung

Im Zentrum robuster Agenten-Architekturen steht das Framework LangGraph. Im Gegensatz zu klassischen, sequenziellen Chaining-Bibliotheken modelliert LangGraph die Kontrolllogik als gerichteten Graphen (StateGraph).

```
┌───────────────────────────┐
│   Start / User Input      │
└─────────────┬─────────────┘
              ▼
┌─────────────────────────┐
│   LLM Agent (Node)      │
└────────────┬────────────┘
             │
Conditional Edge: Tool Call?
    ├──────────────────┤
   Ja                 Nein
    ▼                  ▼
┌───────────────────────────┐ ┌───────────────────┐
│ Execution: MCP Tool Node  │ │ Final Answer /    │
└────────────┬──────────────┘ │ State Completion  │
             │                └───────────────────┘
             └──────────────────────────┐
                                        ▼
                         (Loop Back to LLM Agent)
```

**Die Kernvorteile von LangGraph:**
- **Zyklen & Conditional Edges:** Die Unterstützung von nativen Schleifen und dynamischen Verzweigungen erlaubt es Agenten, Arbeitsergebnisse selbstständig zu evaluieren, Fehler zu korrigieren und iterative Lösungsansätze zu verfolgen.
- **State Persistence:** Der Gesamtzustand des Graphen wird nach jedem Ausführungsschritt in einem unterliegenden Checkpointer gespeichert. Dies ermöglicht lückenlose Audits, Time-Travel-Debugging sowie das Anhalten und Fortsetzen von Ausführungen.
- **Human-in-the-Loop:** Ermöglicht das deterministische Unterbrechen von Graph-Traversierungen an vordefinierten Knoten, um menschliche Freigaben (z. B. vor der Ausführung von Schreib-Aktionen) einzuholen.

**Architektonischer Ausschluss von Open-Core-Lösungen (n8n Anti-Pattern):**
In reinen Open-Source-Kernprojekten stellt der Einsatz von visuellem Low-Code-Werkzeugen wie n8n ein Anti-Pattern dar. n8n unterliegt einem Open-Core-Lizenzmodell (Sustainable Use License / Fair-Code) und erfüllt nicht die Kriterien permissiver Open-Source-Software. Um rechtliche Unsicherheiten, Lizenzkonflikte und proprietäre Abhängigkeiten im Enterprise-Stack vollständig auszuschließen, wird n8n explizit aus der Zielarchitektur ausgeschlossen. Die Orchestrierung verbleibt zu 100 % in quelloffenen Python-Bibliotheken wie LangGraph.

### 4.2 Inferenz-Engines & Benutzeroberflächen

- **Ollama:** Der Industriestandard für die lokale Bereitstellung und das Paketmanagement von LLMs unter Linux, macOS und Windows. Ollama abstrahiert das GPU-Layering, stellt CLI-Verwaltungstools bereit und bietet standardmäßig eine lokale API-Schnittstelle (http://localhost:11434).
- **vLLM:** Eine hochperformante Inferenz-Engine für Produktionsumgebungen. vLLM maximiert den Durchsatz via PagedAttention, unterstützt modernste Quantisierungsformate wie NVFP4 und bietet eine vollumfänglich OpenAI-kompatible REST-API.
- **Open WebUI:** Eine erweiterbare, selbstgehostete Benutzeroberfläche zur Replikation moderner Chat-Interfaces. Bietet rollenbasierte Zugriffskontrollen (RBAC), native RAG-Funktionen via Vektordatenbanken und visuelle Tool-Anbindungen.
- **ComfyUI:** Eine knotenbasierte (node-based) Ausführungsumgebung, die als visuelle Steuerungszentrale für multimodale Pipelines fungiert und eine präzise Steuerung komplexer Mediengenerierungs- und Agentenprozesse erlaubt.

### 4.3 Tool-Integration via Model Context Protocol (MCP)

Das von Anthropic initiierte und als Open-Source-Standard etablierte Model Context Protocol (MCP) entkoppelt Sprachmodelle von proprietären Systemintegrationen. Ein MCP-Server stellt ein einheitliches, typisiertes Schema bereit, welches dem LLM als Werkzeug zur Verfügung gestellt wird.

**In Produktionsumgebungen bewährte MCP-Tools:**
- **Python Calculator / REPL:** Ausführung mathematischer und logischer Berechnungen in einer isolierten Runtime zur Eliminierung von LLM-Halluzinationen.
- **Firecrawl Web Search API:** Bietet Agenten die Möglichkeit, strukturierte Echtzeit-Webdaten und Dokumenteninhalte datenschutzkonform zu extrahieren.
- **GitHub MCP Server:** Ermöglicht authentifizierte Schreib- und Lesezugriffe auf Repositories, Pull Requests und Issue-Tracker.
- **Sentry MCP:** Liest Produktions-Logs und Stack-Traces aus, um autonom Voranalysen bei Systemfehlern durchzuführen.

### 4.4 Multimodale 3-Server-Architekturen

Zur Maximierung der Hardware-Auslastung unter Linux/WSL2 wird eine entkoppelte 3-Server-Topologie eingesetzt, bei der Spezialaufgaben auf dedizierte Serverprozesse aufgeteilt werden:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   WSL2 / Linux Ausführungsumgebung                     │
│                                                                        │
│ ┌──────────────────┐    ┌──────────────────┐    ┌────────────────────┐ │
│ │  1. vLLM Server  │    │ 2. Ollama Server │    │ 3. ComfyUI Server  │ │
│ │  (Gemma 4 NVFP4) │    │  (Phi-4-Mini)    │    │  (Workflow Engine) │ │
│ └────────┬─────────┘    └────────┬─────────┘    └─────────┬──────────┘ │
└──────────┼───────────────────────┼────────────────────────┼────────────┘
           ▼                       ▼                        ▼
     [Exekutive KI]       [Brainstorming/Chat]      [Orchestrierung]
```

**Deterministische Startreihenfolge:**
Um Port-Konflikte und VRAM-Allokationsfehler zu vermeiden, muss die Startsequenz strikt eingehalten werden: **vLLM Server → ComfyUI → Ollama**.

**Produktions-Ausführungsbefehle:**

vLLM Server starten (Exekutives Modell):
```bash
python -m vllm.entrypoints.openai.api_server \
  --model /mnt/c/AI/Comfy/ComfyUI/models/LLM/cosmicproc/gemma-4-E4B-it-NVFP4 \
  --quantization nvfp4 \
  --gpu-memory-utilization 0.75 \
  --max-model-len 8192 \
  --trust-remote_code \
  --enforce-eager \
  --allowed-local-media-path /home/user/Nova-Lab/ComfyUI/input
```

ComfyUI Server starten (Workflow & Agentic UI):
```bash
python main.py --use-pytorch-cross-attention --disable-api-nodes
```

Ollama Server starten (Chat- & Logik-Modell):
```bash
ollama run phi4:q5
```

---

## 5. DevSecOps & Extensionen: Private GitHub Actions Marketplace Apps

### 5.1 Deployment-Architektur für private GitHub Apps

Unternehmen können maßgeschneiderte GitHub Actions als private Marketplace Apps innerhalb ihrer GitHub-Organisation bereitstellen. Dies erlaubt die sichere Wiederverwendbarkeit interner Entwickler-Tools ohne Exposition von geistigem Eigentum.

**Der 5-Schritte-Bereitstellungsleitfaden:**

1. **Action-Spezifikation (action.yml):** Definition der Aktionsschnittstelle im internen Repository
```yaml
name: "Enterprise Code Quality Checker"
description: "Führt statische Code-Analysen über lokale KI-Agenten aus"
inputs:
  files:
    description: "Zu analysierende Dateien"
    required: true
runs:
  using: "node12"
  steps:
    - run: "npm run lint"
      working-directory: ${{ github.workspace }}
```

2. **GitHub App Konfiguration:** Erstellung unter Settings → Developer Settings → GitHub Apps. Zuweisung minimaler OAuth-Berechtigungen (Principle of Least Privilege) und Umstellung der Sichtbarkeit auf Private.

3. **Marketplace-Registrierung:** In den App-Einstellungen "Add to Marketplace" wählen, die Sichtbarkeit auf Private beschränken, die eigene Organisation zuweisen und den privaten Schlüssel (Private Key) generieren und im Secret-Store hinterlegen.

4. **Private Installation:** Installation der App für spezifische Organisations-Repositories. Einbindung in CI/CD-Workflows via:
```yaml
steps:
  - uses: your-org/your-private-action@v1
    with:
      files: "src/**/*.js"
```

5. **Lifecycle & Versionierung:** Pflege über Git-Tags (@v1, @v1.2.0), um Abwärtskompatibilität in den Entwicklerteams zu garantieren.

### 5.2 Webhooks & Secure Event Handling

Die Anbindung externer GitHub-Ereignisse an interne Inferenz-Backends erfordert eine kryptografische Absicherung:

```
[GitHub Event] ──> Webhook (HTTP POST + X-Hub-Signature-256) ──> [Python Backend]
                                                                        │
                                                           HMAC-SHA256 Validierung
                                                                        │
[Runner Workflow Execution] <── repository_dispatch Event <─────────────┘
```

**HMAC-SHA256 Signaturprüfung:** Jeder von GitHub gesendete Webhook enthält im HTTP-Header `X-Hub-Signature-256` einen HMAC-Hash des Payloads. Das empfangende Python-Backend (FastAPI oder Flask) berechnet den Hash mit dem geteilten Webhook-Secret neu und verifiziert die Übereinstimmung, bevor Anfragen verarbeitet werden.

**Repository Dispatch Triggers:** Nach erfolgreicher HMAC-Validierung löst das Backend über die GitHub-API ein `repository_dispatch`-Ereignis aus. Dies trennt den Event-Empfänger strikt vom eigentlichen Action-Runner und schützt die interne Infrastruktur vor unautorisierten Aufrufen.

### 5.3 Pros & Cons Analysis

**Vorteile (Pros):**
- 🔐 **Maximale Datensicherheit:** Sämtliche Code-Analysen und KI-Prüfungen verbleiben innerhalb der eigenen Infrastruktur.
- 🆓 **Zero Licensing Costs:** Nutzung der bestehenden GitHub-Infrastruktur ohne Zusatzkosten für Dritte.
- 🚀 **Nahtlose CI/CD-Integration:** Direkte Einbindung in native Entwickler-Pipelines über vertraute GitHub-Action-Syntax.

**Nachteile (Cons):**
- ⚙ **Erhöhter Konfigurationsaufwand:** Komplexeres Initial-Setup im Vergleich zu öffentlichen Plug-and-Play-Marketplace-Actions.
- 🔒 **Governance-Verantwortung:** Private Keys, OAuth-Scopes und HMAC-Secrets müssen manuell verwaltet und rotiert werden.
- 🧑‍💻 **Wartungsaufwand:** Updates von Laufzeitumgebungen und API-Anpassungen obliegen dem internen DevOps-Team.

---

## 6. Practical Implementation Roadmap (Schritt-für-Schritt Leitfaden)

```
PHASE A: INFRASTRUKTUR & SYSTEMUMGEBUNG (Schritte 1 bis 3)
[Schritt 1: Tool-Wahl] ──> [Schritt 2: WSL2 / uv / Ollama] ──> [Schritt 3: Modelfile & Build]
                                                                            │
PHASE B: PRODUKTIVSETZUNG, RAG & HÄRTUNG (Schritte 4 bis 6)                 ▼
[Schritt 6: HTTPS / Endpoint] <── [Schritt 5: RAG & MCP] <── [Schritt 4: Prompting / LangGraph]
```

### 6.1 Phase A: Infrastruktur & Systemumgebung (Schritt 1 bis 3)

**Schritt 1: Auswahl der Laufzeitumgebung**
- Entwickler & Server-Betrieb: Ollama als schlanke CLI-Engine.
- Einsteiger & lokale Workstations: LM Studio für grafische Inspektion und Modell-Tests.

**Schritt 2: Systeminstallation & Paket-Setup**
- WSL2 auf Windows-Systemen bzw. Terminal unter Linux/macOS initialisieren.
- Installation von Komprimierungswerkzeugen:
```bash
sudo apt update && sudo apt install zstd -y
```
- Erstellen einer isolierten Python 3.11-Umgebung mittels Paketmanager uv:
```bash
uv venv --python 3.11
source .venv/bin/activate
```
- Ollama über das offizielle Shell-Skript installieren:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Schritt 3: Modell-Bereitstellung & Custom Modelfile Compilation**
- Modell ziehen: `ollama pull mistral`
- Erstellen einer maßgeschneiderten Modelfile-Konfiguration für strukturierte Chat-Modelle:
```dockerfile
FROM ./Phi-4-mini-instruct-Q5_K_M.gguf
PARAMETER num_ctx 32768
PARAMETER temperature 1.0

PARAMETER stop "<|end|>"
PARAMETER stop "## Conversation"

TEMPLATE """{{ if .System }}<|system|>
{{ .System }}<|end|>
{{ end }}{{ if .Prompt }}<|user|>
{{ .Prompt }}<|end|>
{{ end }}<|assistant|>
{{ .Response }}<|end|>"""
```
- Modell in Ollama kompilieren und testen:
```bash
ollama create phi4:q5 -f Modelfile
ollama run phi4:q5
```

### 6.2 Phase B: Produktivsetzung, RAG & Härtung (Schritt 4 bis 6)

**Schritt 4: System-Prompting & Agenten-Orchestrierung**
- Strukturierte System-Prompts zur Definition von Rolle, Markdown-Formatierungsvorgaben und Halluzinations-Schranken definieren.
- Einbinden des Modells in eine LangGraph-StateGraph-Pipeline mit persistentem Speicher.

**Schritt 5: Lokale Datenanbindung (RAG) & MCP-Tool-Binding**
- Anbindung interner Unternehmensdokumente über eine lokale Vektordatenbank (ChromaDB oder FAISS) zur Realisierung von Retrieval-Augmented Generation.
- Registrierung typisierter MCP-Tools (Python-REPL, Firecrawl) im LangGraph-Code.

**Schritt 6: Endpunkt-Bereitstellung, HTTPS & Absicherung**
- Netzwerk-Bindung von Ollama/vLLM auf interne Subnetze beschränken.
- Absicherung des Remote-Zugriffs über ein verschlüsseltes Mesh-VPN wie Tailscale.
- **HTTPS-Zertifikatsbindung:** Konfiguration von TLS/HTTPS-Zertifikaten an den Schnittstellen. Dies ist zwingend erforderlich, um Web-Browser-Sicherheitsrichtlinien für Funktionen wie lokale Mikrofoneingaben und Voice-Chat-APIs auf Client-Geräten zu erfüllen.

---

## Anhang: Digitales Gesundheitsleitsystem & Notfallreform

### Historische Entwicklung

Das Konzept des **digitalen Gesundheitsleitsystems** und der aktuellen **Notfallreform** entwickelte sich schrittweise aus mehreren Gutachten und Gesetzesinitiativen:

**2015 (Erste gesetzliche Weichenstellungen):**
- Das *GKV-Versorgungsstärkungsgesetz* verpflichtete Kassenärztliche Vereinigungen (KVs) erstmals zur Kooperation mit Rettungsleitstellen.
- Parallel beauftragte das *Krankenhausstrukturgesetz* den Gemeinsamen Bundesausschuss (G-BA), ein gestuftes System der Notfallversorgung an Kliniken (Stufen I bis III) zu definieren.

**2018 (Gutachten des Sachverständigenrats & Eckpunktepapier):**
- Der Sachverständigenrat Gesundheit legte 2018 Empfehlungen zur patientenorientierten Steuerung vor.
- Im Dezember 2018 veröffentlichte das Bundesgesundheitsministerium daraufhin das maßgebliche Eckpunktepapier für ein **Notfallgesetz**. Darin wurden die drei zentralen Säulen formuliert:
  1. Verankerung der medizinischen Notfallrettung als **dritte Säule** im Sozialgesetzbuch V (SGB V).
  2. Schaffung von **Integrierten Notfallzentren (INZ)** an ausgewählten Klinikstandorten.
  3. Aufbau eines **gemeinsamen Notfallleitsystems (GNL)** zur strukturierten Verbindung der Notrufnummern **112** und **116117**.

**2019 (Terminservicestellen-Gesetz & SmED):**
- Mit dem TSVG wurde die 116117 verpflichtet, Akutfälle rund um die Uhr zu vermitteln.
- In diesem Zuge entwickelte die Kassenärztliche Bundesvereinigung das standardisierte Ersteinschätzungsverfahren **SmED** (*Strukturierte medizinische Ersteinschätzung in Deutschland*).

**Aktueller Beschluss:**
Die verabschiedete Reform führt diese Bausteine zusammen, um über eine einheitliche, softwaregestützte Triage an den Leitstellen und gemeinsamen Tresen unnötige Transporte und Fehlsteuerungen zu vermeiden.
