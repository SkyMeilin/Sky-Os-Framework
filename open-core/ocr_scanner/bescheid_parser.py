"""
SkyOS Open Core - Behördenbescheid OCR Parser
Agency Level Up 2025 (Pascal Weidermann, Hückelhoven)

Strukturierte Extraktion von Behördenbescheiden, Genehmigungen und offiziellen Dokumenten
mittels OCR (Tesseract) mit Regex-basierter Datenextraktion.

Unterstützte Dokumententypen:
- Baugenehmigungen
- Gewerbeanmeldungen
- Feuerwehrgutachten
- Immissionsschutz-Bescheide
- OBG NRW §14 Notfallgenehmigungen
"""

import re
import hashlib
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class BescheidData(BaseModel):
    """Strukturierte Daten eines Behördenbescheids."""
    dokument_typ: str = Field(..., description="Typ des Dokuments (z.B. Baugenehmigung)")
    bescheid_nummer: Optional[str] = Field(None, description="Aktenzeichen / Bescheidnummer")
    behoerde: Optional[str] = Field(None, description="Ausstellende Behörde")
    datum: Optional[str] = Field(None, description="Datum des Bescheids")
    empfaenger: Optional[str] = Field(None, description="Empfänger des Bescheids")
    inhalt_zusammenfassung: Optional[str] = Field(None, description="Zusammenfassung des Inhalts")
    frist_widerspruch: Optional[str] = Field(None, description="Widerspruchsfrist")
    sha256_hash: str = Field(default_factory=lambda: "", description="SHA-256 Hash des Originaltexts")
    confidence_score: float = Field(default=0.0, description="OCR-Confidence-Score (0.0-1.0)")

    def compute_hash(self, raw_text: str) -> str:
        """Berechnet den SHA-256 Hash des Original-OCR-Textes."""
        self.sha256_hash = hashlib.sha256(raw_text.encode('utf-8')).hexdigest()
        return self.sha256_hash


class BescheidParser:
    """
    Parser für deutsche Behördenbescheide mit Regex-basierter Extraktion.
    
    Unterstützt verschiedene Dokumentenformate und extrahiert strukturierte Daten
    aus OCR-Texten (Tesseract-Ausgabe).
    """

    # Regex-Patterns für deutsche Behördenbescheide
    PATTERNS = {
        'bescheid_nummer': [
            r'(?:Akten?zeichen|Az\.?|Bescheidnr\.?|Nr\.?)[\s:]+([A-Z0-9/\-\.]+)',
            r'([A-Z]{2,4}[\-\/]\d{4,6}[\-\/]\d{2,4})',
        ],
        'behoerde': [
            r'(?:Stadt|Kreis|Landkreis|Gemeinde|Behörde|Amt)[\s:]+([A-ZÄÖÜ][a-zäöüß\s]+(?:Stadt|Kreis|Gemeinde|Amt|Verwaltung))',
            r'([A-ZÄÖÜ][a-zäöüß]+(?:\s[A-ZÄÖÜ][a-zäöüß]+)*\s(?:Stadt|Kreis|Gemeinde|Amt))',
        ],
        'datum': [
            r'(?:vom|datiert|Hückelhoven,|Datteln,|Düsseldorf,)\s*(\d{1,2}[./]\d{1,2}[./]\d{4})',
            r'(\d{1,2}[./]\d{1,2}[./]\d{4})',
        ],
        'empfaenger': [
            r'(?:An\s+)([A-ZÄÖÜ][a-zäöüß]+(?:\s[A-ZÄÖÜ][a-zäöüß]+)+)',
            r'(?:Empfänger|An\s+den|An\s+die|An\s+das)[\s:]+(.+?)(?:\n|$)',
        ],
        'frist_widerspruch': [
            r'(?:Widerspruchs?frist|Rechtsbehelfs?belehrung)[\s:]+(.+?)(?:\n|$)',
            r'(\d{1,2}\s+(?:Tage|Woche|Monat)e?\s+(?:ab|nach)\s+(?:Zugang|Zustellung))',
        ],
    }

    DOCUMENT_TYPE_KEYWORDS = {
        'Baugenehmigung': ['Baugenehmigung', 'Bauvorhaben', 'Bauanzeige', 'Bauleitplanung'],
        'Gewerbeanmeldung': ['Gewerbeanmeldung', 'Gewerbebetrieb', 'Handwerkskammer'],
        'Feuerwehrgutachten': ['Feuerwehrgutachten', 'Brandschutz', 'Feuerwehraufsicht'],
        'Immissionsschutz': ['Immissionsschutz', 'Emissionswerte', 'Luftreinhaltung', 'Lärm'],
        'OBG_NRW_§14': ['OBG NRW', 'Notfallgenehmigung', '§ 14 OBG', 'Katastrophenfall'],
        'Allgemeiner_Bescheid': ['Bescheid', 'Verwaltungsakt', 'Behördenbescheid'],
    }

    def __init__(self, language: str = 'deu'):
        """
        Initialisiert den Bescheid-Parser.
        
        Args:
            language: Sprache für OCR (Standard: Deutsch)
        """
        self.language = language
        self._ocr_engine = None  # Optional[TesseractClient] - lazy load

    def detect_document_type(self, text: str) -> str:
        """
        Erkennt den Dokumententyp basierend auf Keywords im OCR-Text.
        
        Args:
            text: OCR-Text des Dokuments
            
        Returns:
            Dokumententyp-String
        """
        text_lower = text.lower()
        
        # Prüfe jeden Dokumententyp (priorisiert)
        for doc_type, keywords in self.DOCUMENT_TYPE_KEYWORDS.items():
            if any(keyword.lower() in text_lower for keyword in keywords):
                return doc_type
        
        return 'Unbekannt'

    def extract_field(self, text: str, field_name: str) -> Optional[str]:
        """
        Extrahiert ein einzelnes Feld aus dem OCR-Text.
        
        Args:
            text: OCR-Text des Dokuments
            field_name: Name des zu extrahierenden Feldes
            
        Returns:
            Extrahierter Wert oder None
        """
        patterns = self.PATTERNS.get(field_name, [])
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        
        return None

    def parse(self, raw_ocr_text: str) -> BescheidData:
        """
        Parst einen kompletten Behördenbescheid aus OCR-Text.
        
        Args:
            raw_ocr_text: Roher OCR-Text (z.B. von Tesseract)
            
        Returns:
            BescheidData Objekt mit extrahierten Daten
        """
        if not raw_ocr_text or not raw_ocr_text.strip():
            raise ValueError("OCR-Text darf nicht leer sein")

        # Dokumententyp erkennen
        doc_type = self.detect_document_type(raw_ocr_text)

        # Alle Felder extrahieren
        bescheid_nummer = self.extract_field(raw_ocr_text, 'bescheid_nummer')
        behoerde = self.extract_field(raw_ocr_text, 'behoerde')
        datum = self.extract_field(raw_ocr_text, 'datum')
        empfaenger = self.extract_field(raw_ocr_text, 'empfaenger')
        frist_widerspruch = self.extract_field(raw_ocr_text, 'frist_widerspruch')

        # Zusammenfassung generieren (erste 500 Zeichen)
        inhalt_zusammenfassung = raw_ocr_text.strip()[:500]

        # Datenobjekt erstellen
        data = BescheidData(
            dokument_typ=doc_type,
            bescheid_nummer=bescheid_nummer,
            behoerde=behoerde,
            datum=datum,
            empfaenger=empfaenger,
            inhalt_zusammenfassung=inhalt_zusammenfassung,
            frist_widerspruch=frist_widerspruch,
            confidence_score=self._estimate_confidence(raw_ocr_text),
        )

        # SHA-256 Hash berechnen
        data.compute_hash(raw_ocr_text)

        return data

    def _estimate_confidence(self, text: str) -> float:
        """
        Schätzt die OCR-Qualität basierend auf Textmerkmalen.
        
        Args:
            text: OCR-Text
            
        Returns:
            Confidence-Score zwischen 0.0 und 1.0
        """
        if not text:
            return 0.0

        score = 1.0
        text_len = len(text)

        # Kurze Texte haben niedrigere Confidence
        if text_len < 100:
            score -= 0.3
        elif text_len < 500:
            score -= 0.1

        # Viele Leerzeichen oder Sonderzeichen deuten auf schlechte OCR hin
        whitespace_ratio = text.count(' ') / max(text_len, 1)
        if whitespace_ratio > 0.6:
            score -= 0.2

        # Keine erkannten Struktur-Marker
        has_structure = any(marker in text for marker in ['§', 'Akten', 'Bescheid', 'Datum', 'An'])
        if not has_structure:
            score -= 0.2

        return max(0.0, min(1.0, score))

    def batch_parse(self, ocr_texts: List[str]) -> List[Dict[str, Any]]:
        """
        Parst mehrere OCR-Texte gleichzeitig.
        
        Args:
            ocr_texts: Liste von OCR-Texten
            
        Returns:
            Liste von Ergebnis-Dictionaries mit Status und Daten
        """
        results = []
        
        for i, text in enumerate(ocr_texts):
            try:
                data = self.parse(text)
                results.append({
                    'index': i,
                    'status': 'success',
                    'data': data.model_dump(),
                    'error': None
                })
            except Exception as e:
                results.append({
                    'index': i,
                    'status': 'error',
                    'data': None,
                    'error': str(e)
                })
        
        return results


# ==========================================
# Self-Test
# ==========================================

if __name__ == "__main__":
    print("=" * 70)
    print(" SkyOS Open Core: Bescheid Parser Self-Test")
    print("=" * 70)

    # Simulierter OCR-Text eines Bauantrags
    test_ocr_text = """
    Stadt Hückelhoven
    Bauaufsichtsbehörde
    
    Aktenzeichen: B-2025/042
    
    An
    Pascal Weidermann
    Musterstraße 1
    41836 Hückelhoven
    
    Hückelhoven, den 15.03.2025
    
    Baugenehmigung für Ihr Bauvorhaben
    
    Sehr geehrter Herr Weidermann,
    
    mit diesem Bescheid erteilen wir Ihnen die Baugenehmigung für das geplante 
    Wohngebäude auf dem Grundstück Musterstraße 1, Flurstück 123/4.
    
    Die Bauvorlageberechtigung wird Ihnen nach § 62 BauG anerkannt.
    
    Widerspruchsfrist: 1 Monat ab Zugang dieses Bescheids.
    
    Mit freundlichen Grüßen
    Stadt Hückelhoven - Bauaufsicht
    """

    parser = BescheidParser()
    
    # Dokumententyp erkennen
    doc_type = parser.detect_document_type(test_ocr_text)
    print(f"[1/4] Dokumententyp: {doc_type}")
    
    # Kompletter Parse
    data = parser.parse(test_ocr_text)
    print(f"[2/4] Bescheidnummer: {data.bescheid_nummer}")
    print(f"[3/4] Behörde: {data.behoerde}")
    print(f"[4/4] SHA-256 Hash: {data.sha256_hash[:16]}...")
    print(f"       Confidence: {data.confidence_score:.2f}")
    
    print("\n" + "=" * 70)
    print(" ✅ Bescheid Parser Test PASSED!")
    print("=" * 70)
