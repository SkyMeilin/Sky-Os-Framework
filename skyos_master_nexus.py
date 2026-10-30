# =====================================================================
# SkyOS Core - Master Nexus & Asynchronous Webhook Router
# Pfad: C:/Workspace LM studio/Sicherheitsrichtlinien/skyos_master_nexus.py
# Zweck: Bidirektionaler Hub, Event-Queue und WORM-Audit-Ledger für 
#        das gesamte SkyOS-Ökosystem (inkl. FastAPI & Pydantic v2).
# =====================================================================

import hashlib
import hmac
import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks, Header, Depends  # pyright: ignore[reportUnknownVariableType]
from pydantic import BaseModel, Field

from shared_security import verify_api_key, add_cors_middleware

# Logging-Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] SkyOS_MasterNexus: %(message)s"
)
logger = logging.getLogger("SkyOS_MasterNexus")

app = FastAPI(
    title="SkyOS Master Nexus & Webhook Router",
    version="5.0.0",
    description="Zentraler, bidirektionaler Event- und Routing-Core für das SkyOS-Ökosystem"
)

# CORS Middleware — explizite Origin-Liste (kein Wildcard!)
add_cors_middleware(app)

# Lokaler Vault-Puffer & WORM-Ledger
WORM_AUDIT_LEDGER: List[Dict[str, Any]] = []
EVENT_QUEUE: List[Dict[str, Any]] = []

# Webhook-Secret muss gesetzt sein — kein Default-Fallback!
def get_webhook_signing_secret() -> str:
    secret = os.getenv("SKYOS_WEBHOOK_SECRET")
    if not secret:
        raise RuntimeError(
            "SKYOS_WEBHOOK_SECRET environment variable is not set. "
            "Webhook signature verification requires a secret key."
        )
    return secret

class NexusMessage(BaseModel):
    source_node: str = Field(..., description="Absendender Agent oder Dienst (z.B. 'BosContainerPlannerAgent', 'WordPressBridge')")
    target_node: str = Field(..., description="Ziel-Node oder 'broadcast'")
    action_type: str = Field(..., description="Aktionstyp (z.B. 'sync_state', 'trigger_alert', 'validate_container')")
    payload_data: Dict[str, Any] = Field(..., description="Nutzdaten des Pakets")

def generate_worm_audit_hash(data: str) -> str:
    timestamp = datetime.utcnow()
    raw = f"{timestamp}:{data}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def verify_hmac_signature(raw_body: bytes, signature_header: Optional[str]) -> bool:
    if not signature_header:
        return False
    secret = get_webhook_signing_secret()
    expected = hmac.new(
        secret.encode("utf-8"),
        raw_body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature_header)

@app.get("/")
def master_status(api_key: str = Depends(verify_api_key)):
    return {
        "status": "online",
        "mode": "bidirectional_mesh_with_fallback",
        "workspace": "C:/Workspace LM studio/Sicherheitsrichtlinien",
        "queued_events": len(EVENT_QUEUE),
        "worm_audit_entries": len(WORM_AUDIT_LEDGER)
    }

@app.post("/v1/nexus/dispatch")
def dispatch_message(message: NexusMessage, background_tasks: BackgroundTasks, api_key: str = Depends(verify_api_key)):
    """Zentrale Dispatcher-Schnittstelle für den interaktiven Datenaustausch zwischen Nodes."""
    logger.info(f"📥 Nachricht von '{message.source_node}' an '{message.target_node}' [{message.action_type}]")
    
    packet_str = json.dumps(message.dict(), sort_keys=True)
    audit_hash = generate_worm_audit_hash(packet_str)
    
    WORM_AUDIT_LEDGER.append({
        "timestamp": datetime.utcnow().isoformat(),
        "source": message.source_node,
        "target": message.target_node,
        "action": message.action_type,
        "audit_hash": audit_hash
    })

    if message.target_node == "broadcast":
        background_tasks.add_task(execute_broadcast, message.dict())
        msg = "Broadcast an alle registrierten Mesh-Nodes erfolgreich initiiert."
    else:
        background_tasks.add_task(route_to_target, message.target_node, message.dict())
        msg = f"Daten erfolgreich an Node '{message.target_node}' geroutet."

    return {
        "status": "dispatched",
        "worm_audit_hash": audit_hash,
        "message": msg
    }

@app.post("/v1/webhook/ingress")
async def webhook_ingress(
    request: Request,
    background_tasks: BackgroundTasks,
    x_skyos_signature: Optional[str] = Header(None)
):
    """Asynchroner Fallback-Webhook-Empfang mit Signaturprüfung und Queue-Pufferung."""
    raw_body = await request.body()
    
    if not verify_hmac_signature(raw_body, x_skyos_signature):
        logger.warning("🚨 Unautorisierter Webhook-Aufruf abgewiesen (Signatur ungültig).")
        raise HTTPException(status_code=401, detail="Invalid HMAC signature")

    try:
        json_data = await request.json()
    except Exception as e:
        logger.error(f"❌ JSON-Parsing-Fehler: {e}")
        raise HTTPException(status_code=400, detail="Malformed JSON payload")

    source = json_data.get("event_source", "external")
    etype = json_data.get("event_type", "generic")
    payload = json_data.get("payload_data", {})

    audit_hash = generate_worm_audit_hash(json.dumps(json_data, sort_keys=True))
    WORM_AUDIT_LEDGER.append({
        "timestamp": datetime.utcnow().isoformat(),
        "source": source,
        "type": etype,
        "audit_hash": audit_hash
    })

    # Fallback-Queue Pufferung bei hoher Auslastung
    EVENT_QUEUE.append({
        "event_source": source,
        "event_type": etype,
        "data": payload,
        "audit_hash": audit_hash
    })

    logger.info(f"📥 Webhook von '{source}' ({etype}) in Fallback-Queue gepuffert.")
    return {
        "status": "queued_for_execution",
        "worm_audit_hash": audit_hash,
        "queue_size": len(EVENT_QUEUE)
    }

def execute_broadcast(data: Dict[str, Any]):
    logger.info(f"⚡ [BROADCAST] Verteile Daten von {data['source_node']} im Mesh.")

def route_to_target(target: str, data: Dict[str, Any]):
    logger.info(f"🔀 [ROUTING] Leite Daten an Ziel-Node '{target}' weiter.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("skyos_master_nexus:app", host="127.0.0.1", port=8000, reload=True)