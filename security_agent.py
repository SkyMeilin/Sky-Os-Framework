"""
SecurityAgent Backend Service (formerly PlannerAgent Backend Core)
Integrates: Repository Monitoring, WORM SHA-256 Integrity Audit, Secret Leak Scanning, DIN Compliance Checking.
"""

import hashlib
import json
import os
import re
import time
from typing import Dict, List, Optional, Any

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from quantum_ledger import append_audit_entry
from shared_security import verify_api_key, add_cors_middleware, validate_path_against_root

app = FastAPI(title="Sky OS Security Agent", version="4.0.0")

# CORS Middleware — explizite Origin-Liste (kein Wildcard!)
add_cors_middleware(app)

# Standard-Pfad: das Projekt-Root-Verzeichnis
DEFAULT_REPO_PATH = os.path.dirname(os.path.abspath(__file__))


class SecurityAgentService:
    """
    Python Backend SecurityAgent for Repository Monitoring and Audit Verification.
    Monitors git repositories (e.g., /workspaces/Sicherheitsrichtlinien or C:/Workspace LM studio).
    """

    def __init__(self, repository_path: str = DEFAULT_REPO_PATH, worm_log_path: str = "worm_audit_log.jsonl"):
        self.repository_path = repository_path
        self.worm_log_path = worm_log_path
        self.secret_patterns = [
            re.compile(r"AIzaSy[A-Za-z0-9-_]{35}"),  # Google API Key
            re.compile(r"sk-[A-Za-z0-9]{32,}"),       # OpenAI / generic secret
            re.compile(r"-----BEGIN PRIVATE KEY-----"), # RSA Private Key
            re.compile(r"WORDPRESS_DB_PASSWORD\s*=\s*['\"]?[^'\"]+['\"]?"), # Unsafe hardcoded DB pass
        ]

    def compute_sha256(self, file_path: str) -> Optional[str]:
        """Computes SHA-256 hash of a specified file."""
        if not os.path.exists(file_path) or os.path.isdir(file_path):
            return None
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception:
            return None

    def scan_for_secret_leaks(self, file_path: str) -> List[str]:
        """Scans a file for potential secret leaks or API keys."""
        leaks = []
        if not os.path.exists(file_path) or os.path.isdir(file_path):
            return leaks

        filename = os.path.basename(file_path)
        if filename.startswith(".env") and not filename.endswith(".example"):
            leaks.append(f"UNSAFE_FILE: Sensitive environment file '{filename}' detected.")

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                for pattern in self.secret_patterns:
                    if pattern.search(content):
                        leaks.append(f"SECRET_MATCH: Potential sensitive string in {filename}")
        except Exception as e:
            leaks.append(f"READ_ERROR: Could not read {filename}: {str(e)}")

        return leaks

    def verify_worm_log_integrity(self) -> Dict[str, Any]:
        """Verifies integrity of the WORM audit log entries using SHA-256."""
        if not os.path.exists(self.worm_log_path):
            return {"status": "no_log_found", "valid_entries": 0, "corrupted_entries": 0, "is_secure": True}

        valid_count = 0
        corrupted_count = 0

        with open(self.worm_log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    provided_hash = entry.pop("sha256", None)
                    raw_data = json.dumps(entry, sort_keys=True)
                    expected_hash = hashlib.sha256(raw_data.encode("utf-8")).hexdigest()

                    if provided_hash == expected_hash:
                        valid_count += 1
                    else:
                        corrupted_count += 1
                except Exception:
                    corrupted_count += 1

        return {
            "status": "integrity_verified" if corrupted_count == 0 else "tamper_detected",
            "valid_entries": valid_count,
            "corrupted_entries": corrupted_count,
            "is_secure": corrupted_count == 0,
        }

    def audit_repository(self) -> Dict[str, Any]:
        """Full security and integrity audit of the target repository."""
        start_time = time.time()
        audited_files = []
        secret_leaks = []

        if os.path.exists(self.repository_path):
            for root, dirs, files in os.walk(self.repository_path):
                dirs[:] = [d for d in dirs if d not in [".git", "node_modules", ".dart_tool", "build"]]
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.repository_path)
                    file_hash = self.compute_sha256(file_path)

                    leaks = self.scan_for_secret_leaks(file_path)
                    if leaks:
                        secret_leaks.extend(leaks)

                    audited_files.append({
                        "file": rel_path,
                        "sha256": file_hash,
                        "status": "clean" if not leaks else "leak_detected"
                    })

        worm_audit = self.verify_worm_log_integrity()

        is_healthy = (len(secret_leaks) == 0) and worm_audit.get("is_secure", True)

        return {
            "agent": "SicherheitsAgent (SecurityAgentService)",
            "repository_path": self.repository_path,
            "audit_timestamp": time.time(),
            "duration_seconds": round(time.time() - start_time, 3),
            "overall_status": "SECURE" if is_healthy else "ALERT_REQUIRED",
            "total_files_audited": len(audited_files),
            "secret_leaks_found": secret_leaks,
            "worm_log_audit": worm_audit,
            "audited_files": audited_files[:50]
        }


# --- FastAPI Endpunkte ---

class ScanRequest(BaseModel):
    file_path: str


class AuditRequest(BaseModel):
    repository_path: Optional[str] = None


agent = SecurityAgentService()


@app.get("/security/status")
def security_status(api_key: str = Depends(verify_api_key)):
    """Gibt den aktuellen Sicherheitsstatus des Agents zurück."""
    return {
        "agent": "Sky OS Security Agent",
        "repository_path": agent.repository_path,
        "worm_log_path": agent.worm_log_path,
    }


@app.post("/security/scan")
def scan_file(request: ScanRequest, api_key: str = Depends(verify_api_key)):
    """Scannt eine einzelne Datei auf potenzielle Secret-Leaks."""
    # Path-Traversal-Schutz: Pfad muss innerhalb des Repository-Root liegen
    validated_path = validate_path_against_root(request.file_path, agent.repository_path)
    
    leaks = agent.scan_for_secret_leaks(validated_path)
    file_hash = agent.compute_sha256(validated_path)

    # Protokollierung im Ledger
    append_audit_entry(
        f"Dateiscan durchgeführt: {request.file_path} - {'{0} Probleme gefunden'.format(len(leaks))}",
        actor="SecurityAgent"
    )

    return {
        "file": validated_path,
        "sha256": file_hash,
        "leaks": leaks,
        "status": "clean" if not leaks else "leak_detected",
    }


@app.post("/security/audit")
def audit_repo(request: AuditRequest, api_key: str = Depends(verify_api_key)):
    """Führt ein vollständiges Repository-Security-Audit durch."""
    repo_path = request.repository_path or agent.repository_path
    temp_agent = SecurityAgentService(repository_path=repo_path)
    report = temp_agent.audit_repository()

    # Protokollierung im Ledger
    append_audit_entry(
        f"Repository-Audit abgeschlossen: {report['overall_status']} - {report['total_files_audited']} Dateien geprüft",
        actor="SecurityAgent"
    )

    return report


@app.get("/security/worm")
def verify_worm(api_key: str = Depends(verify_api_key)):
    """Verifiziert die Integrität des WORM-Audit-Logs."""
    result = agent.verify_worm_log_integrity()

    append_audit_entry(
        f"WORM-Integritätsprüfung: {result['status']} - {result['valid_entries']} gültige, {result['corrupted_entries']} korrupte Einträge",
        actor="SecurityAgent"
    )

    return result


if __name__ == "__main__":
    import uvicorn
    report = agent.audit_repository()
    print(json.dumps(report, indent=2))
    # Starte den FastAPI-Server auf Port 8003
    uvicorn.run(app, host="0.0.0.0", port=8003)
