#!/usr/bin/env python3
"""
Auto PR Description Generator
Analyзирует PR-Änderungen und generiert Titel und Beschreibung.
"""

import os
import subprocess
import sys
import re
from pathlib import Path


def run_command(cmd: str) -> str:
    """Führt einen Shell-Befehl aus und gibt die Ausgabe zurück."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()


def count_files(changed_files: list, pattern: str) -> int:
    """Zählt Dateien, die einem Muster entsprechen."""
    count = 0
    pattern_re = re.compile(pattern)
    for f in changed_files:
        if pattern_re.search(f):
            count += 1
    return count


def get_pr_type(branch_name: str) -> tuple:
    """Bestimmt den PR-Typ basierend auf dem Branch-Namen."""
    branch_lower = branch_name.lower()
    
    if any(kw in branch_lower for kw in ['fix', 'bug', 'repair']):
        return 'Bugfix', '🐛'
    elif any(kw in branch_lower for kw in ['refactor', 'refactoring']):
        return 'Refactoring', '🔄'
    elif any(kw in branch_lower for kw in ['docs', 'documentation']):
        return 'Dokumentation', '📚'
    elif any(kw in branch_lower for kw in ['ci', 'cd', 'pipeline', 'workflow']):
        return 'CI/CD', '🚀'
    elif 'test' in branch_lower:
        return 'Tests', '🧪'
    elif any(kw in branch_lower for kw in ['security', 'sec', 'audit']):
        return 'Sicherheit', '🔒'
    else:
        return 'Feature', '✨'


def clean_branch_name(branch_name: str) -> str:
    """Entfernt Prefixe wie 'feature/', 'fix/', etc. vom Branch-Namen."""
    return re.sub(r'^(feature|fix|bug|refactor|docs|ci|test|security)[/-]+', '', branch_name, flags=re.IGNORECASE)


def generate_change_summary(changed_files: list) -> str:
    """Generiert eine Zusammenfassung der Änderungen nach Kategorie."""
    summaries = []
    
    python_count = count_files(changed_files, r'\.py$')
    if python_count > 0:
        summaries.append(f"- 🐍 **Python Backend**: {python_count} Datei(en) geändert")
    
    ts_count = count_files(changed_files, r'\.(tsx?|ts)$')
    if ts_count > 0:
        summaries.append(f"- ⚛️ **Frontend (TypeScript/React)**: {ts_count} Datei(en) geändert")
    
    js_count = count_files(changed_files, r'\.js$')
    if js_count > 0:
        summaries.append(f"- 📜 **JavaScript**: {js_count} Datei(en) geändert")
    
    dart_count = count_files(changed_files, r'\.dart$')
    if dart_count > 0:
        summaries.append(f"- 📱 **Flutter App**: {dart_count} Datei(en) geändert")
    
    docker_count = count_files(changed_files, r'docker|Dockerfile')
    if docker_count > 0:
        summaries.append(f"- 🐳 **Docker/Infrastruktur**: {docker_count} Datei(en) geändert")
    
    md_count = count_files(changed_files, r'\.md$')
    if md_count > 0:
        summaries.append(f"- 📝 **Dokumentation**: {md_count} Datei(en) geändert")
    
    json_count = count_files(changed_files, r'\.json$')
    if json_count > 0:
        summaries.append(f"- 📋 **Konfiguration (JSON)**: {json_count} Datei(en) geändert")
    
    yaml_count = count_files(changed_files, r'\.(yml|yaml)$')
    if yaml_count > 0:
        summaries.append(f"- ⚙️ **CI/CD (YAML)**: {yaml_count} Datei(en) geändert")
    
    config_count = count_files(changed_files, r'\.env|\.gitignore|package\.json|requirements\.txt|tsconfig')
    if config_count > 0:
        summaries.append(f"- 🔧 **Projektkonfiguration**: {config_count} Datei(en) geändert")
    
    return '\n'.join(summaries)


def generate_description(branch_name: str, pr_type: str, emoji: str, changed_files: list) -> str:
    """Generiert die vollständige PR-Beschreibung."""
    change_summary = generate_change_summary(changed_files)
    files_list = '\n'.join(changed_files)
    
    description = f"""## Was ändert dieser Pull Request?

{emoji} **{pr_type}** – Änderungen aus dem Branch `{branch_name}`

---

### 📊 Zusammenfassung der Änderungen

{change_summary}

---

### 📁 Geänderte Dateien

```
{files_list}
```

---

### Typ der Änderung

- [ ] Bugfix
- [ ] Neue Feature
- [ ] Refactoring
- [ ] Dokumentation
- [ ] CI/CD
- [ ] Tests
- [ ] Sicherheit

---

### Tests

- [ ] Unit-Tests sind hinzugefügt/aktualisiert
- [ ] Alle Tests bestehen lokal

---

### Checkliste

- [ ] Code folgt dem Style-Guide
- [ ] Dokumentation ist aktualisiert
- [ ] Selbst-Review durchgeführt

---

*🤖 Diese Beschreibung wurde automatisch von der GitHub Action generiert.*
"""
    return description


def main():
    """Hauptfunktion zum Generieren von PR-Titel und -Beschreibung."""
    # Hole Umgebungsvariablen von GitHub Actions
    branch_name = os.environ.get('BRANCH_NAME', 'unknown')
    base_sha = os.environ.get('BASE_SHA', '')
    head_sha = os.environ.get('HEAD_SHA', '')
    
    # Hole die Liste der geänderten Dateien
    if base_sha and head_sha:
        changed_files_output = run_command(f'git diff --name-only {base_sha}...{head_sha}')
        changed_files = [f for f in changed_files_output.split('\n') if f.strip()]
    else:
        # Fallback: zeige alle geänderten Dateien seit dem letzten Commit
        changed_files_output = run_command('git diff --name-only HEAD~1 HEAD')
        changed_files = [f for f in changed_files_output.split('\n') if f.strip()]
    
    # Bestimme PR-Typ und Emoji
    pr_type, emoji = get_pr_type(branch_name)
    
    # Generiere Titel
    clean_name = clean_branch_name(branch_name)
    title = f"{emoji} [{pr_type}] {clean_name}"
    
    # Generiere Beschreibung
    description = generate_description(branch_name, pr_type, emoji, changed_files)
    
    # Ausgabe als JSON für GitHub Actions
    output_file = os.environ.get('OUTPUT_FILE', '/tmp/pr-output.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f'TITLE={title}\n')
        f.write('DESCRIPTION_START\n')
        f.write(description)
        f.write('\nDESCRIPTION_END\n')
    
    print(f"Title: {title}")
    print(f"Description written to: {output_file}")


if __name__ == '__main__':
    main()
