import requests
import json
from quantum_ledger import append_audit_entry

WP_URL = "https://deine-wordpress-domain.com/wp-json/wp/v2/posts"
WP_USER = "dein_wp_benutzer"
WP_APP_PASSWORD = "dein_wp_application_password"

def publish_content_to_wordpress(title, content_html, tags=[]):
    headers = {"Content-Type": "application/json"}
    payload = {
        "title": title,
        "content": content_html,
        "status": "draft",  # Sicherheitshalber als Entwurf speichern
        "tags": tags
    }
    
    try:
        response = requests.post(WP_URL, json=payload, auth=(WP_USER, WP_APP_PASSWORD))
        if response.status_code == 201:
            append_audit_entry(f"WordPress Beitrag als Entwurf erstellt: '{title}'", actor="Sky-CON Leader")
            return response.json()
        else:
            print(f"Fehler bei WordPress-Übertragung: {response.status_code}")
            return None
    except Exception as e:
        print(f"Verbindungsfehler zu WordPress: {e}")
        return None
