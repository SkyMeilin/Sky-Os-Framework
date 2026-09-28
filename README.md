# Sky OS – Das Framework

**Sky OS – Das Framework** ist ein 100 % freies, lokales, quelloffenes und rechtlich sicheres Multi-Agenten-Betriebssystem. Es läuft als isolierter Digital Twin auf lokaler Hardware (Lenovo ThinkPad unter WSL) und verbindet kompromisslose Datensouveränität mit modernster Automatisierung.

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

---

## 🚀 Schnellstart (Installation & Betrieb)

Voraussetzungen: Docker und Docker Compose auf deinem ThinkPad (WSL) installiert.

1. **Repository klonen / Ordner öffnen** im Terminal.
2. **Abhängigkeiten & Skripte prüfen**, dass alle `.py` und `.json` Dateien im Hauptverzeichnis liegen.
3. **Docker-Container starten:**
   ```bash
   docker compose up --build -d
