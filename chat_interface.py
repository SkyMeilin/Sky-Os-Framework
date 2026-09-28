from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="Sky OS Web Chat UI")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Sky OS – Das Framework</title>
    <style>
        body { font-family: sans-serif; background: #121212; color: #e0e0e0; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .chat-container { width: 550px; background: #1e1e1e; padding: 20px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        h2 { text-align: center; color: #00adb5; }
        .chat-box { height: 320px; border: 1px solid #333; overflow-y: scroll; padding: 10px; margin-bottom: 10px; background: #252525; }
        input[type="text"] { width: 78%; padding: 10px; background: #333; border: 1px solid #444; color: white; border-radius: 4px; }
        button { width: 18%; padding: 10px; background: #00adb5; border: none; color: white; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="chat-container">
        <h2>Sky OS Terminal</h2>
        <div class="chat-box" id="chatBox">
            <div><strong>System:</strong> Alle 15 Departments geladen. Digital Twin aktiv.</div>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <input type="text" id="userInput" placeholder="Befehl eingeben...">
            <button>Senden</button>
        </div>
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def get_ui():
    return HTML_TEMPLATE

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
