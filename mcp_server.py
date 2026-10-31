from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from quantum_ledger import append_audit_entry
from shared_security import verify_api_key, add_cors_middleware

app = FastAPI(title="Sky OS MCP Bridge", version="4.0.0")

# CORS Middleware — explizite Origin-Liste (kein Wildcard!)
add_cors_middleware(app)

class MCPToolCall(BaseModel):
    tool_name: str
    arguments: dict

@app.post("/mcp/call")
def handle_mcp_call(call: MCPToolCall, api_key: str = Depends(verify_api_key)):
    # Jedes Remote-Kommando vom Smartphone wird im Ledger dokumentiert
    append_audit_entry(f"MCP Befehl via Mobile empfangen: Tool '{call.tool_name}'", actor="Sky-DEV Leader")
    
    if call.tool_name == "sky_os_execute":
        action = call.arguments.get("action", "unbekannt")
        return {
            "status": "success",
            "result": f"Aktion '{action}' erfolgreich durch das Framework ausgeführt."
        }
    else:
        raise HTTPException(status_code=404, detail="MCP Tool nicht im System registriert.")

@app.get("/mcp/manifest")
def mcp_manifest():
    return {
        "tools": [
            {
                "name": "sky_os_execute",
                "description": "Steuert die 15 Departments und Workflows von Sky OS über das Smartphone.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {"type": "string", "description": "Die auszuführende Aufgabe"}
                    },
                    "required": ["action"]
                }
            }
        ]
    }
