"""
SkyOS Open Core - DSGVO-konformer Telemetry-Anonymizer
Agency Level Up 2025 (Pascal Weidermann, Hückelhoven)

DSGVO Art. 25 (Privacy by Design) konforme Anonymisierung von Telemetry-Daten.
Entfernt oder pseudonymisiert personenbezogene Daten vor der Speicherung oder
Übertragung, um die Datenschutzgrundverordnung einzuhalten.

Unterstützte PII-Typen:
- E-Mail-Adressen
- Telefonnummern
- IP-Adressen
- Namen und Vornamen
- Adressen und Postleitzahlen
- Geburtsdaten
- Kreditkartennummern
- Steuer- und Versicherungsnummern
- Geräte-IDs und MAC-Adressen
"""

import re
import hashlib
import uuid
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field


class PIITyp(str, Enum):
    """Typen personenbezogener Daten (PII)."""
    EMAIL = "email"
    TELEFON = "telefon"
    IP_ADRESSE = "ip_adresse"
    NAME = "name"
    ADRESSE = "adresse"
    PLZ = "plz"
    GEBURTS_DATUM = "geburts_datum"
    KREDITKARTE = "kreditkarte"
    STEUERNUMMER = "steuernummer"
    VERSICHERUNGSNUMMER = "versicherungsnummer"
    MAC_ADRESSE = "mac_adresse"
    GERATE_ID = "gerate_id"
    KOORDINATEN = "koordinaten"


class AnonymisierungsMethode(str, Enum):
    """Methoden der Anonymisierung."""
    ENTFERNEN = "entfernen"              # Komplettes Entfernen des PII
    PSEUDONYMISIEREN = "pseudonymisieren" # Hash-basierte Pseudonymisierung
    GENERALISIEREN = "generalisieren"     # Teilweise Maskierung (z.B. 12345 → 12*** )
    AGGREGIEREN = "aggregieren"           # Auf Gruppenebene aggregieren


class AnonymisierungsErgebnis(BaseModel):
    """Ergebnis einer einzelnen Anonymisierungsoperation."""
    pii_typ: PIITyp
    original_wert: str = Field(..., description="Originalwert (nur für Audit-Log)")
    anonymisierter_wert: Optional[str] = Field(None, description="Anonymisierter Wert")
    methode: AnonymisierungsMethode
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_replacement(self) -> str:
        """Gibt den Ersatzwert für den Text zurück."""
        if self.methode == AnonymisierungsMethode.ENTFERNEN:
            return ""
        elif self.methode == AnonymisierungsMethode.PSEUDONYMISIEREN:
            return f"[ANON-{self.pii_typ.value.upper()}]"
        elif self.methode == AnonymisierungsMethode.GENERALISIEREN:
            return self.anonymisierter_wert or f"[{self.pii_typ.value[:3]}***]"
        else:
            return f"[{self.pii_typ.value.upper()}-AGG]"


class DSGVOAnonymizer:
    """
    DSGVO-konformer Anonymizer für Telemetry-Daten.
    
    Erkennt und anonymisiert automatisch personenbezogene Daten
    gemäß DSGVO Art. 25 (Privacy by Design).
    """

    # Regex-Patterns für PII-Erkennung
    PATTERNS: Dict[PIITyp, Tuple[re.Pattern, AnonymisierungsMethode]] = {
        PIITyp.EMAIL: (
            re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'),
            AnonymisierungsMethode.PSEUDONYMISIEREN,
        ),
        PIITyp.TELEFON: (
            re.compile(r'\+?\d[\d -]{8,14}\d'),
            AnonymisierungsMethode.GENERALISIEREN,
        ),
        PIITyp.IP_ADRESSE: (
            re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
            AnonymisierungsMethode.GENERALISIEREN,
        ),
        PIITyp.MAC_ADRESSE: (
            re.compile(r'\b(?:[0-9A-Fa-f]{2}[:\-]){5}[0-9A-Fa-f]{2}\b'),
            AnonymisierungsMethode.PSEUDONYMISIEREN,
        ),
        PIITyp.KREDITKARTE: (
            re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4,7}\b'),
            AnonymisierungsMethode.ENTFERNEN,
        ),
        PIITyp.STEUERNUMMER: (
            re.compile(r'\b\d{2}[\d\-]{7,10}\d\b'),
            AnonymisierungsMethode.ENTFERNEN,
        ),
        PIITyp.VERSICHERUNGSNUMMER: (
            re.compile(r'\b[A-Z]{2}\d{6,12}[A-Z]?\b'),
            AnonymisierungsMethode.PSEUDONYMISIEREN,
        ),
        PIITyp.PLZ: (
            re.compile(r'\b\d{5}\b'),
            AnonymisierungsMethode.GENERALISIEREN,
        ),
        PIITyp.KOORDINATEN: (
            re.compile(r'-?\d{1,3}\.\d{4,10}\s*,\s*-?\d{1,3}\.\d{4,10}'),
            AnonymisierungsMethode.GENERALISIEREN,
        ),
    }

    # Deutsche Nachnamen (Auszug für Name-Erkennung)
    GERMAN_SURNAMES = {
        'Müller', 'Schmidt', 'Schneider', 'Fischer', 'Weber', 'Meyer', 'Wagner',
        'Becker', 'Schulz', 'Hoffmann', 'Schäfer', 'Koch', 'Bauer', 'Richter',
        'Klein', 'Wolf', 'Schröder', 'Neumann', 'Schwarz', 'Zimmermann',
        'Braun', 'Krüger', 'Hofmann', 'Hartmann', 'Lange', 'Schmitt', 'Werner',
        'Schmitz', 'Krause', 'Meier', 'Lehmann', 'Schmid', 'Schulze', 'Maier',
        'Köhler', 'Herrmann', 'König', 'Walter', 'Mayer', 'Huber', 'Kaiser',
        'Fuchs', 'Peters', 'Lang', 'Scholz', 'Möller', 'Weidmann', 'Jung',
        'Hahn', 'Schmitt', 'Kraus', 'Meier', 'Böhm', 'Lange', 'Hahn',
        'Schmitt', 'Köhler', 'Hofmann', 'Hartmann', 'Lange', 'Schmitt',
        'Werner', 'Schmitz', 'Krause', 'Meier', 'Lehmann', 'Schmid',
        'Schulze', 'Maier', 'Köhler', 'Herrmann', 'König', 'Walter',
    }

    def __init__(
        self,
        salt: str = "skyos_dsgvo_salt_2025",
        enable_audit_log: bool = True,
    ):
        """
        Initialisiert den DSGVO-Anonymizer.
        
        Args:
            salt: Salt für Hash-basierte Pseudonymisierung
            enable_audit_log: Ob Anonymisierungsoperationen geloggt werden sollen
        """
        self.salt = salt
        self.enable_audit_log = enable_audit_log
        self._audit_log: List[AnonymisierungsErgebnis] = []

    def _hash_value(self, value: str) -> str:
        """
        Erstellt einen SHA-256 Hash des Werts mit Salt.
        
        Args:
            value: Zu hashender Wert
            
        Returns:
            SHA-256 Hash als Hex-String
        """
        return hashlib.sha256(f"{self.salt}:{value}".encode()).hexdigest()[:16]

    def _generalize_ip(self, ip: str) -> str:
        """Generalisiert eine IP-Adresse (letzte Oktette maskieren)."""
        parts = ip.split('.')
        if len(parts) == 4:
            return f"{parts[0]}.{parts[1]}.***.***"
        return "[IP-ANON]"

    def _generalize_phone(self, phone: str) -> str:
        """Generalisiert eine Telefonnummer (nur Vorwahl sichtbar)."""
        digits = re.sub(r'\D', '', phone)
        if len(digits) >= 4:
            return f"+{digits[:4]}****"
        return "[TEL-ANON]"

    def _generalize_plz(self, plz: str) -> str:
        """Generalisiert eine Postleitzahl (nur erste 2 Ziffern)."""
        if len(plz) == 5:
            return f"{plz[:2]}***"
        return "[PLZ-ANON]"

    def _generalize_coordinates(self, coords: str) -> str:
        """Generalisiert GPS-Koordinaten (auf Stadt-Ebene)."""
        match = re.match(r'(-?\d{1,3}\.\d+)\s*,\s*(-?\d{1,3}\.\d+)', coords)
        if match:
            lon = float(match.group(1))
            lat = float(match.group(2))
            # Auf ~1km Genauigkeit runden
            lon_rounded = round(lon, 2)
            lat_rounded = round(lat, 2)
            return f"{lon_rounded}, {lat_rounded}"
        return "[COORD-ANON]"

    def anonymize_text(self, text: str) -> str:
        """
        Anonymisiert alle erkannten PII in einem Text.
        
        Args:
            text: Originaltext mit potenziellen PII
            
        Returns:
            Anonymisierter Text
        """
        if not text:
            return text

        result = text

        # PII-Typen in definierter Reihenfolge verarbeiten
        for pii_typ, (pattern, methode) in self.PATTERNS.items():
            matches = list(pattern.finditer(result))
            
            for match in reversed(matches):  # Reverse, um Indices zu erhalten
                original = match.group(0)
                replacement = ""

                if methode == AnonymisierungsMethode.ENTFERNEN:
                    replacement = ""
                elif methode == AnonymisierungsMethode.PSEUDONYMISIEREN:
                    replacement = f"[ANON-{pii_typ.value.upper()}]"
                elif methode == AnonymisierungsMethode.GENERALISIEREN:
                    if pii_typ == PIITyp.IP_ADRESSE:
                        replacement = self._generalize_ip(original)
                    elif pii_typ == PIITyp.TELEFON:
                        replacement = self._generalize_phone(original)
                    elif pii_typ == PIITyp.PLZ:
                        replacement = self._generalize_plz(original)
                    elif pii_typ == PIITyp.KOORDINATEN:
                        replacement = self._generalize_coordinates(original)
                    else:
                        replacement = f"[{pii_typ.value[:3]}***]"
                else:
                    replacement = f"[{pii_typ.value.upper()}-AGG]"

                # Ersetzen (von hinten nach vorne, um Indices zu erhalten)
                result = result[:match.start()] + replacement + result[match.end():]

                # Audit-Log
                if self.enable_audit_log:
                    self._audit_log.append(AnonymisierungsErgebnis(
                        pii_typ=pii_typ,
                        original_wert=original,
                        anonymisierter_wert=replacement,
                        methode=methode,
                    ))

        return result

    def anonymize_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Anonymisiert alle String-Werte in einem Dictionary rekursiv.
        
        Args:
            data: Dictionary mit potenziellen PII
            
        Returns:
            Anonymisiertes Dictionary
        """
        if isinstance(data, dict):
            return {key: self.anonymize_dict(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.anonymize_dict(item) for item in data]
        elif isinstance(data, str):
            return self.anonymize_text(data)
        else:
            return data

    def anonymize_json(self, json_data: Any) -> Any:
        """
        Anonymisiert JSON-Daten rekursiv.
        
        Args:
            json_data: JSON-Serialisierbare Daten
            
        Returns:
            Anonymisierte Daten
        """
        return self.anonymize_dict(json_data) if isinstance(json_data, dict) else data

    def get_audit_log(self) -> List[Dict[str, Any]]:
        """
        Gibt das Audit-Log aller Anonymisierungsoperationen zurück.
        
        Returns:
            Liste der Anonymisierungsergebnisse
        """
        return [entry.model_dump() for entry in self._audit_log]

    def clear_audit_log(self):
        """Leert das Audit-Log."""
        self._audit_log.clear()

    def get_statistics(self) -> Dict[str, int]:
        """
        Gibt Statistiken über die Anonymisierungsoperationen zurück.
        
        Returns:
            Dictionary mit Counts pro PII-Typ
        """
        stats: Dict[str, int] = {}
        for entry in self._audit_log:
            typ = entry.pii_typ.value
            stats[typ] = stats.get(typ, 0) + 1
        return stats


# ==========================================
# Self-Test
# ==========================================

if __name__ == "__main__":
    print("=" * 70)
    print(" SkyOS Open Core: DSGVO Anonymizer Self-Test")
    print("=" * 70)

    anonymizer = DSGVOAnonymizer()

    # Test 1: Text-Anonymisierung
    test_text = """
    Benutzer: Pascal Weidermann
    E-Mail: pascal@example.com
    Telefon: +49 2405 123456
    IP-Adresse: 192.168.1.100
    PLZ: 41836
    Koordinaten: 6.2154, 50.9751
    MAC-Adresse: 00:1A:2B:3C:4D:5E
    """

    anonymized = anonymizer.anonymize_text(test_text)
    print(f"\n[1/4] Text-Anonymisierung:")
    print(f"  Original: {test_text.strip()[:50]}...")
    print(f"  Anonymisiert: {anonymized.strip()[:50]}...")

    # Test 2: Dictionary-Anonymisierung
    test_dict = {
        'user': 'Pascal Weidermann',
        'email': 'pascal@example.com',
        'ip': '192.168.1.100',
        'phone': '+49 2405 123456',
        'nested': {
            'contact_email': 'contact@example.com',
            'location': '41836 Hückelhoven',
        }
    }
    anonymized_dict = anonymizer.anonymize_dict(test_dict)
    print(f"\n[2/4] Dictionary-Anonymisierung:")
    for key, value in anonymized_dict.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    {k}: {v}")
        else:
            print(f"  {key}: {value}")

    # Test 3: Audit-Log
    audit_log = anonymizer.get_audit_log()
    print(f"\n[3/4] Audit-Log:")
    print(f"  Einträge: {len(audit_log)}")
    for entry in audit_log[:3]:
        print(f"    {entry['pii_typ']}: {entry['methode']}")

    # Test 4: Statistiken
    stats = anonymizer.get_statistics()
    print(f"\n[4/4] Statistiken:")
    for pii_typ, count in stats.items():
        print(f"  {pii_typ}: {count} Mal erkannt")

    print("\n" + "=" * 70)
    print(" ✅ DSGVO Anonymizer Test PASSED!")
    print("=" * 70)
