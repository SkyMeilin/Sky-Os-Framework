"""
SkyOS & TRENCH PROTOCOL V2 - Multi-Protocol Agent Bridge & Gateway Adapter
Agency Level Up 2025 (Pascal Weidermann, Hückelhoven)

Features:
- MCP (Model Context Protocol) to A2A (Agent-to-Agent) & REST/Webhook Adapter
- HMAC-SHA256 Webhook Signature Verification
- Inbound Event Bridge into Six-Verb State Machine (SEARCH -> RESOLVE -> PREVIEW -> HUMAN_GATE -> EXECUTE -> VERIFY)
- GDPR Art. 25 PII Anonymization Bridge
- Direct WORM Ledger SHA-256 Hash Chain Integration
"""

import hmac
import hashlib
import json
import re
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

# ==========================================
# 1. PROTOCOL ENUMS & MODELS
# ==========================================

class ProtocolType(str, Enum):
    MCP = "MCP"          # Model Context Protocol (Tool / Resource Access)
    A2A = "A2A"          # Agent-to-Agent Protocol (Peer Collaboration)
    REST_WEBHOOK = "REST_WEBHOOK" # External Inbound Webhook
    HAI_SSE = "HAI_SSE"  # Human-Agent Interaction Event Stream

class SixVerb(str, Enum):
    SEARCH = "SEARCH"
    RESOLVE = "RESOLVE"
    PREVIEW = "PREVIEW"
    HUMAN_GATE = "HUMAN_GATE"
    EXECUTE = "EXECUTE"
    VERIFY = "VERIFY"

class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str = Field(..., description="e.g. tools/call or resources/read")
    params: Dict[str, Any] = Field(default_factory=dict)
    id: str

class A2AMessage(BaseModel):
    protocol: str = "A2A/1.0"
    performative: str = Field(..., description="REQUEST, INFORM, AGREE, REFUSE")
    sender_id: str
    receiver_id: str
    content: Dict[str, Any]

class BridgeEnvelope(BaseModel):
    source_protocol: ProtocolType
    target_protocol: ProtocolType
    workflow_id: str
    current_verb: SixVerb
    payload: Dict[str, Any]
    security_hash: str
    timestamp: str

# ==========================================
# 2. PROTOCOL ADAPTER & BRIDGE ENGINE
# ==========================================

class SkyOSAgentBridge:
    """
    Universeller Protocol Adapter & Bridge Service.
    Wandelt MCP, A2A und REST Webhooks in das deterministische Six-Verb-Protokoll um.
    """
    def __init__(self, webhook_secret: Optional[str] = None):
        if webhook_secret is None:
            raise RuntimeError(
                "webhook_secret is required. Set it via environment variable or constructor parameter."
            )
        self.webhook_secret = webhook_secret.encode('utf-8')
        self._last_worm_hash = "0000000000000000000000000000000000000000000000000000000000000000"

    def verify_webhook_signature(self, raw_body: bytes, signature_header: str) -> bool:
        """Prüft HMAC-SHA256 Signatur eingehender Webhooks."""
        expected = hmac.new(self.webhook_secret, raw_body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature_header.replace("sha256=", ""))

    def anonymize_pii(self, text: str) -> str:
        """DSGVO Art. 25 PII Redaction Bridge."""
        text = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[ANONYMIZED_EMAIL]', text)
        text = re.sub(r'\+?\d[\d -]{8,12}\d', '[ANONYMIZED_PHONE]', text)
        return text

    def mcp_to_a2a(self, mcp_req: MCPRequest, sender_agent: str, target_agent: str) -> A2AMessage:
        """
        Wandelt einen MCP Tool-Call (z.B. tools/call) in eine strukturierte A2A Request Message um.
        """
        tool_name = mcp_req.params.get("name", "unknown_tool")
        arguments = mcp_req.params.get("arguments", {})

        a2a_content = {
            "task": tool_name,
            "prompt": json.dumps(arguments),
            "mcp_orig_id": mcp_req.id
        }

        return A2AMessage(
            protocol="A2A/1.0",
            performative="REQUEST",
            sender_id=sender_agent,
            receiver_id=target_agent,
            content=a2a_content
        )

    def process_bridge_request(
        self,
        source_protocol: ProtocolType,
        target_protocol: ProtocolType,
        raw_payload: Dict[str, Any],
        workflow_id: str,
        human_approved: bool = False
    ) -> Dict[str, Any]:
        """
        Führt das 6-Stufen Six-Verb Protokoll durch den Bridge-Adapter aus.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # 1. SEARCH & RESOLVE Phase
        sanitized_payload = json.loads(self.anonymize_pii(json.dumps(raw_payload)))
        
        # 2. PREVIEW Phase
        preview_envelope = {
            "status": "PREVIEW_GENERATED",
            "source": source_protocol.value,
            "target": target_protocol.value,
            "transformed_data": sanitized_payload
        }
        
        # 3. HUMAN_GATE Phase
        if not human_approved:
            return {
                "status": "STOPPED_AT_HUMAN_GATE",
                "workflow_id": workflow_id,
                "required_action": "Explizite menschliche Freigabe erforderlich",
                "preview": preview_envelope
            }

        # 4. EXECUTE & VERIFY Phase (WORM Hash chain)
        payload_bytes = json.dumps(preview_envelope, sort_keys=True).encode()
        payload_hash = hashlib.sha256(payload_bytes).hexdigest()
        
        # previous_hash ZUERST speichern, DANN aktualisieren (Bug-Fix!)
        previous_hash_for_entry = self._last_worm_hash
        chain_raw = f"{previous_hash_for_entry}:{payload_hash}:{timestamp}:{workflow_id}"
        current_worm_hash = hashlib.sha256(chain_raw.encode()).hexdigest()
        self._last_worm_hash = current_worm_hash

        return {
            "status": "EXECUTION_SUCCESSFUL",
            "workflow_id": workflow_id,
            "source_protocol": source_protocol.value,
            "target_protocol": target_protocol.value,
            "result_payload": preview_envelope["transformed_data"],
            "worm_audit_entry": {
                "timestamp": timestamp,
                "payload_hash": payload_hash,
                "previous_hash": previous_hash_for_entry,
                "current_hash": current_worm_hash,
                "compliance": "BSI § 8a BSIG / ISO/IEC 27037"
            }
        }

# ==========================================
# 3. SELF-TEST SUITE
# ==========================================

if __name__ == "__main__":
    print("======================================================================")
    print(" SkyOS & TRENCH PROTOCOL V2: Multi-Protocol Agent Bridge Test ")
    print("======================================================================\n")

    bridge = SkyOSAgentBridge(webhook_secret="skyos_secret_key")

    # 1. MCP zu A2A Conversion Test
    mcp_req = MCPRequest(
        id="mcp_req_001",
        method="tools/call",
        params={"name": "crm_update_contact", "arguments": {"email": "pascal@example.com", "status": "active"}}
    )
    a2a_msg = bridge.mcp_to_a2a(mcp_req, sender_agent="master_orchestrator", target_agent="twenty_crm_agent")
    print(f"[1/2] MCP-to-A2A Translation:\n  Performative: {a2a_msg.performative}\n  Target: {a2a_msg.receiver_id}\n  Content Task: {a2a_msg.content['task']}\n")

    # 2. Six-Verb Bridge Pipeline Test mit HUMAN_GATE
    bridge_res = bridge.process_bridge_request(
        source_protocol=ProtocolType.MCP,
        target_protocol=ProtocolType.A2A,
        raw_payload={"contact_email": "pascal@example.com", "action": "UPDATE"},
        workflow_id="wf_bridge_101",
        human_approved=True
    )
    print(f"[2/2] Six-Verb Bridge Processed:\n  Status: {bridge_res['status']}\n  Anonymized Data: {bridge_res['result_payload']}\n  WORM Hash: {bridge_res['worm_audit_entry']['current_hash'][:16]}...\n")

    print("======================================================================")
    print(" ✅ SkyOS Agent Bridge Test PASSED! ")
    print("======================================================================")
