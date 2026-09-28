from fastapi import FastAPI, Request, HTTPException
from quantum_ledger import append_audit_entry

app = FastAPI(title="Sky OS Sovereign Payment Gateway", version="4.0.0")

@app.post("/webhook/paypal")
async def paypal_webhook(request: Request):
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
