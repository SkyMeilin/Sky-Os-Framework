import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from quantum_ledger import append_audit_entry
from shared_security import verify_api_key, add_cors_middleware, verify_webhook_signature, get_webhook_secret

app = FastAPI(title="Sky OS Sovereign Payment Gateway", version="4.0.0")

# CORS Middleware — explizite Origin-Liste (kein Wildcard!)
add_cors_middleware(app)


def verify_paypal_signature(payload: bytes, signature_header: str) -> bool:
    """Verifiziert die PayPal Webhook-Signatur."""
    secret = get_webhook_secret("PAYPAL_WEBHOOK_SECRET")
    return verify_webhook_signature(payload, signature_header, secret)


def verify_revolut_signature(payload: bytes, signature_header: str) -> bool:
    """Verifiziert die Revolut Webhook-Signatur."""
    secret = get_webhook_secret("REVOLUT_WEBHOOK_SECRET")
    return verify_webhook_signature(payload, signature_header, secret)


@app.post("/webhook/paypal")
async def paypal_webhook(request: Request):
    # 1. Rohes Payload für Signatur-Verifikation lesen
    raw_body = await request.body()
    
    # 2. Signatur-Verifikation (kritisch — verhindert gefälschte Webhooks!)
    signature = request.headers.get("paypal-transmission-id")
    transmission_sig = request.headers.get("paypal-transmission-sig")
    
    if transmission_sig:
        if not verify_paypal_signature(raw_body, transmission_sig):
            raise HTTPException(
                status_code=401,
                detail="Unauthorized: Invalid PayPal webhook signature."
            )
    else:
        # Fallback: API-Key Auth wenn keine Signatur vorhanden
        await verify_api_key(request.headers.get("x-api-key"))
    
    try:
        body = await request.json()
        event_type = body.get("event_type")
        
        if event_type == "CHECKOUT.ORDER.APPROVED":
            resource = body.get("resource", {})
            order_id = resource.get("id", "unknown")
            amount = resource.get("purchase_units", [{}])[0].get("amount", {}).get("value", "0.00")
            
            # Protokollierung im quantensicheren Ledger durch die Buchhaltung (Sky-OPE Leader)
            append_audit_entry(f"Zahlung eingegangen (PayPal/Venmo): Bestellung {order_id} über {amount} EUR", actor="Sky-OPE Leader")
            return {"status": "success", "processed": True, "order_id": order_id}
            
        return {"status": "ignored_event"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/webhook/revolut")
async def revolut_webhook(request: Request):
    # 1. Rohes Payload für Signatur-Verifikation lesen
    raw_body = await request.body()
    
    # 2. Signatur-Verifikation (kritisch — verhindert gefälschte Webhooks!)
    signature = request.headers.get("x-revolut-webhook-signature")
    
    if signature:
        if not verify_revolut_signature(raw_body, signature):
            raise HTTPException(
                status_code=401,
                detail="Unauthorized: Invalid Revolut webhook signature."
            )
    else:
        # Fallback: API-Key Auth wenn keine Signatur vorhanden
        await verify_api_key(request.headers.get("x-api-key"))
    
    try:
        body = await request.json()
        event = body.get("event")
        
        if event == "ORDER_COMPLETED":
            data = body.get("data", {})
            order_id = data.get("id", "unknown")
            amount_data = data.get("order_amount", {})
            amount = str(amount_data.get("value", "0"))
            
            # Protokollierung im Ledger
            append_audit_entry(f"Zahlung eingegangen (Revolut): Bestellung {order_id} über {amount}", actor="Sky-OPE Leader")
            return {"status": "success", "processed": True, "order_id": order_id}
            
        return {"status": "ignored_event"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
