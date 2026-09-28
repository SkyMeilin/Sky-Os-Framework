import hashlib
import json
from datetime import datetime
from pathlib import Path

LEDGER_FILE = Path("audit_quantum_ledger.json")

def initialize_ledger():
    if not LEDGER_FILE.exists():
        genesis_block = {
            "index": 0,
            "timestamp": datetime.now().isoformat(),
            "event": "Genesis - Sky OS Framework Initialisierung",
            "previous_hash": "0" * 64,
            "hash": ""
        }
        genesis_block["hash"] = compute_hash(genesis_block)
        LEDGER_FILE.write_text(json.dumps([genesis_block], indent=4))

def compute_hash(block: dict) -> str:
    block_copy = block.copy()
    block_copy.pop("hash", None)
    block_string = json.dumps(block_copy, sort_keys=True).encode()
    return hashlib.sha3_256(block_string).hexdigest()

def append_audit_entry(event_description: str, actor: str = "Master_Core_A"):
    initialize_ledger()
    ledger = json.loads(LEDGER_FILE.read_text())
    last_block = ledger[-1]
    
    new_block = {
        "index": last_block["index"] + 1,
        "timestamp": datetime.now().isoformat(),
        "actor": actor,
        "event": event_description,
        "previous_hash": last_block["hash"]
    }
    new_block["hash"] = compute_hash(new_block)
    ledger.append(new_block)
    LEDGER_FILE.write_text(json.dumps(ledger, indent=4))
    print(f"[QUANTUM LEDGER] Block {new_block['index']} gesichert. Hash: {new_block['hash'][:16]}...")
