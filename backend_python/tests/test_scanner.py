"""
SkyOS Open Core - Backend Tests
Agency Level Up 2025 (Pascal Weidermann, Hückelhoven)

Tests für den OCR-Bescheid-Parser und die Scanner-API.
"""

import pytest
import sys
from pathlib import Path

# Füge das Projekt-Root zum Path hinzu
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from open_core.ocr_scanner.bescheid_parser import BescheidParser, BescheidData
from open_core.telemetry.dsgvo_anonymizer import DSGVOAnonymizer


class TestBescheidParser:
    """Tests für den Bescheid-Parser."""

    def setup_method(self):
        self.parser = BescheidParser()

    def test_detect_baugenehmigung(self):
        """Test: Erkennung von Baugenehmigungen."""
        text = "Baugenehmigung für das geplante Wohngebäude"
        doc_type = self.parser.detect_document_type(text)
        assert doc_type == "Baugenehmigung"

    def test_detect_obg_nrw(self):
        """Test: Erkennung von OBG NRW §14 Dokumenten."""
        text = "Notfallgenehmigung nach § 14 OBG NRW"
        doc_type = self.parser.detect_document_type(text)
        assert doc_type == "OBG_NRW_§14"

    def test_detect_unknown(self):
        """Test: Unbekannter Dokumententyp."""
        text = "Dies ist ein normaler Text ohne Bescheid-Marker"
        doc_type = self.parser.detect_document_type(text)
        assert doc_type == "Unbekannt"

    def test_parse_bescheid(self):
        """Test: Komplettes Parsen eines Bescheids."""
        text = """
        Stadt Hückelhoven
        Aktenzeichen: B-2025/042
        Baugenehmigung für Ihr Bauvorhaben
        Hückelhoven, den 15.03.2025
        Widerspruchsfrist: 1 Monat ab Zugang
        """
        data = self.parser.parse(text)
        assert isinstance(data, BescheidData)
        assert data.dokument_typ == "Baugenehmigung"
        assert data.bescheid_nummer == "B-2025/042"
        assert data.sha256_hash  # Hash sollte berechnet sein

    def test_parse_empty_text(self):
        """Test: Leerer Text sollte ValueError werfen."""
        with pytest.raises(ValueError):
            self.parser.parse("")

    def test_batch_parse(self):
        """Test: Batch-Parsing mehrerer Texte."""
        texts = [
            "Baugenehmigung Az: B-001",
            "Feuerwehrgutachten Az: F-002",
        ]
        results = self.parser.batch_parse(texts)
        assert len(results) == 2
        assert results[0]["status"] == "success"
        assert results[1]["status"] == "success"


class TestDSGVOAnonymizer:
    """Tests für den DSGVO-Anonymizer."""

    def setup_method(self):
        self.anonymizer = DSGVOAnonymizer()

    def test_anonymize_email(self):
        """Test: E-Mail-Anonymisierung."""
        text = "Kontakt: pascal@example.com"
        result = self.anonymizer.anonymize_text(text)
        assert "pascal@example.com" not in result
        assert "ANON-EMAIL" in result

    def test_anonymize_phone(self):
        """Test: Telefonnummer-Anonymisierung."""
        text = "Telefon: +49 2405 123456"
        result = self.anonymizer.anonymize_text(text)
        assert "+49 2405 123456" not in result

    def test_anonymize_ip(self):
        """Test: IP-Adresse-Anonymisierung."""
        text = "IP: 192.168.1.100"
        result = self.anonymizer.anonymize_text(text)
        assert "192.168.1.100" not in result

    def test_anonymize_dict(self):
        """Test: Dictionary-Anonymisierung."""
        data = {
            "email": "test@example.com",
            "nested": {
                "phone": "+49 123 456789",
            }
        }
        result = self.anonymizer.anonymize_dict(data)
        assert "test@example.com" not in str(result)

    def test_audit_log(self):
        """Test: Audit-Log wird geführt."""
        text = "Email: test@example.com, IP: 192.168.1.1"
        self.anonymizer.anonymize_text(text)
        log = self.anonymizer.get_audit_log()
        assert len(log) > 0

    def test_statistics(self):
        """Test: Statistiken werden korrekt gezählt."""
        text = "Email: a@b.com, c@d.com"
        self.anonymizer.anonymize_text(text)
        stats = self.anonymizer.get_statistics()
        assert "email" in stats
        assert stats["email"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
