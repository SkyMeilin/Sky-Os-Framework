# Sicherheitsrichtlinie (Security Policy)

Vielen Dank, dass Sie zur Sicherheit von **Sky OS – Das Framework** beitragen. Da dieses System auf absolute Datensouveränität und lokale Ausführung ausgelegt ist, nehmen wir Sicherheit sehr ernst.

## 🛡️ Unterstützte Versionen
Da sich Sky OS in der aktiven Entwicklung befindet, wird Support und Sicherheitsupdates primär für den `main`-Branch bereitgestellt.

| Version | Unterstützt |
| ------- | ----------- |
| 4.x     | ✅ Ja       |
| < 4.0   | ❌ Nein     |

## 🚨 Meldung einer Sicherheitslücke (Vulnerability)
Wenn Sie eine Sicherheitslücke entdecken, möchten wir sicherstellen, dass sie verantwortungsvoll behoben werden kann, bevor sie öffentlich wird.

* **Bitte erstellen Sie KEINE öffentlichen GitHub-Issues** für sicherheitsrelevante Funde.
* Melten Sie Sicherheitslücken stattdessen direkt über einen privaten Kommunikationskanal oder per E-Mail an den Repository-Maintainer.
* Bitte fügen Sie eine detaillierte Beschreibung des Problems, Schritte zur Reproduktion sowie mögliche Lösungsvorschläge bei.

## 🔒 Lokales Sicherheitsmodell
* **Keine Cloud-Abhängigkeit:** Sky OS läuft lokal auf Ihrer Hardware (z. B. Lenovo ThinkPad unter WSL). Sensible Daten und das quantensichere Ledger (`audit_quantum_ledger.json`) bleiben isoliert auf Ihrem System.
* **Kryptografische Integrität:** Alle Systemereignisse und Transaktionen werden über SHA3-256 Hash-Ketten mathematisch versiegelt.

## 🤖 GitHub App: "sicherheitscontainer"

Sky OS nutzt die GitHub App **sicherheitscontainer** (App ID: `4827720`) für automatisierte Sicherheitsprüfungen und CI/CD-Integration.

### App-Details
* **Name:** sicherheitscontainer
* **App ID:** 4827720
* **Owner:** @SkyMeilin
* **Einstellungen:** [GitHub Apps Settings](https://github.com/settings/apps/sicherheitscontainer)

### Berechtigungen & Scopes
Die App verfügt über folgende Berechtigungen:
* **Repository-Zugriff:** Volle Kontrolle über private Repositories (für Security Scans und Code Analysis)
* **GitHub Actions:** Ausführen von Security-Workflows (Bandit, Gitleaks, Trivy)
* **WORM-Ledger:** Integritätsprüfung des PostgreSQL Audit-Ledgers via CI/CD

### Verwendung
Die App wird verwendet für:
1. **Automatisierte Security Scans** – SAST (Static Application Security Testing) bei jedem Push/PR
2. **Secret Detection** – Gitleaks-Scans verhindern das Commiten von API-Keys oder Tokens
3. **Container-Sicherheit** – Trivy-Scans für Docker-Images vor dem Deploy
4. **WORM-Ledger Validierung** – SHA-256 Hash-Kette wird in CI validiert

### Konfiguration
Die App-Credentials werden über Umgebungsvariablen verwaltet:
```env
GITHUB_OAUTH_APP_ID=4827720
GITHUB_OAUTH_CLIENT_ID=DEIN_CLIENT_ID_HIER
GITHUB_OAUTH_CLIENT_SECRET=DEIN_CLIENT_SECRET_HIER
```

### Sicherheitshinweise
* Die Client-ID und das Client-Secret sollten niemals öffentlich geteilt werden.
* Installation Tokens werden nur für die Dauer der CI/CD-Pipeline generiert.
* Die App folgt dem Principle of Least Privilege – nur notwendige Berechtigungen sind aktiviert.
