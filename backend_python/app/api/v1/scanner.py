"""
SkyOS Open Core - Scanner API
Agency Level Up 2025 (Pascal Weidermann, Hückelhoven)

API-Endpunkte für den OCR-Behördenbescheid-Parser.
Ermöglicht das Hochladen und Parsen von Behördenbescheiden.
"""

import sys
import os
from typing import List, Dict, Any, Optional
from pathlib import Path

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form, Depends
from pydantic import BaseModel

# Füge das Projekt-Root zum Path hinzu, um open-core Module zu importieren
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from open_core.ocr_scanner.bescheid_parser import BescheidParser, BescheidData
from open_core.telemetry.dsgvo_anonymizer import DSGVOAnonymizer
from app.core.security import get_current_user, User, check_rate_limit
from app.core.config import settings

router = APIRouter(prefix="/scanner", tags=["Scanner"])

# Globale Parser-Instanzen
bescheid_parser = BescheidParser(language=settings.tesseract_language)
dsgvo_anonymizer = DSGVOAnonymizer()


class ScannerRequest(BaseModel):
    """Anfrage für den OCR-Scanner."""
    ocr_text: str
    anonymize: bool = True


class ScannerResponse(BaseModel):
    """Antwort des OCR-Scanners."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    anonymized: bool = False
    document_type: Optional[str] = None


class BatchScannerRequest(BaseModel):
    """Batch-Anfrage für mehrere OCR-Texte."""
    ocr_texts: List[str]
    anonymize: bool = True


class BatchScannerResponse(BaseModel):
    """Batch-Antwort."""
    total: int
    successful: int
    failed: int
    results: List[Dict[str, Any]]


@router.post("/", response_model=ScannerResponse, summary="OCR-Scanner")
async def scan_bescheid(
    request: ScannerRequest,
    current_user: User = Depends(get_current_user),
    rate_check: None = Depends(check_rate_limit),
) -> ScannerResponse:
    """
    Parst einen Behördenbescheid aus OCR-Text.
    
    Erkennt automatisch den Dokumententyp und extrahiert strukturierte Daten.
    Optional werden personenbezogene Daten DSGVO-konform anonymisiert.
    """
    try:
        # Bescheid parsen
        data = bescheid_parser.parse(request.ocr_text)
        
        result_data = data.model_dump()
        anonymized = False
        
        # Optional anonymisieren
        if request.anonymize:
            result_data = dsgvo_anonymizer.anonymize_dict(result_data)
            anonymized = True
        
        return ScannerResponse(
            success=True,
            data=result_data,
            anonymized=anonymized,
            document_type=data.dokument_typ,
        )
    
    except ValueError as e:
        return ScannerResponse(
            success=False,
            error=str(e),
        )
    except Exception as e:
        return ScannerResponse(
            success=False,
            error=f"Interner Fehler: {str(e)}",
        )


@router.post("/batch", response_model=BatchScannerResponse, summary="Batch-Scanner")
async def scan_batch(
    request: BatchScannerRequest,
    current_user: User = Depends(get_current_user),
    rate_check: None = Depends(check_rate_limit),
) -> BatchScannerResponse:
    """
    Parst mehrere Behördenbescheide gleichzeitig.
    """
    results = bescheid_parser.batch_parse(request.ocr_texts)
    
    successful = sum(1 for r in results if r["status"] == "success")
    failed = len(results) - successful
    
    # Optional anonymisieren
    if request.anonymize:
        for result in results:
            if result["data"]:
                result["data"] = dsgvo_anonymizer.anonymize_dict(result["data"])
    
    return BatchScannerResponse(
        total=len(results),
        successful=successful,
        failed=failed,
        results=results,
    )


@router.post("/upload", response_model=ScannerResponse, summary="Datei-Upload & Scan")
async def upload_and_scan(
    file: UploadFile = File(..., description="Text- oder PDF-Datei mit Behördenbescheid"),
    anonymize: bool = Form(True, description="DSGVO-Anonymisierung anwenden"),
    current_user: User = Depends(get_current_user),
    rate_check: None = Depends(check_rate_limit),
) -> ScannerResponse:
    """
    Lädt eine Datei hoch und parst den Inhalt.
    
    Unterstützt aktuell nur Text-Dateien (.txt).
    PDF-Unterstützung kommt mit Tesseract-Integration.
    """
    # Datei-Typ prüfen
    if not file.filename.endswith(('.txt', '.text')):
        return ScannerResponse(
            success=False,
            error="Nur Text-Dateien (.txt) werden aktuell unterstützt.",
        )
    
    try:
        # Datei lesen
        content = await file.read()
        ocr_text = content.decode('utf-8')
        
        # Parsen
        data = bescheid_parser.parse(ocr_text)
        result_data = data.model_dump()
        anonymized = False
        
        if anonymize:
            result_data = dsgvo_anonymizer.anonymize_dict(result_data)
            anonymized = True
        
        return ScannerResponse(
            success=True,
            data=result_data,
            anonymized=anonymized,
            document_type=data.dokument_typ,
        )
    
    except UnicodeDecodeError:
        return ScannerResponse(
            success=False,
            error="Datei konnte nicht als UTF-8 decodiert werden.",
        )
    except ValueError as e:
        return ScannerResponse(
            success=False,
            error=str(e),
        )
    except Exception as e:
        return ScannerResponse(
            success=False,
            error=f"Interner Fehler: {str(e)}",
        )


@router.get("/types", summary="Unterstützte Dokumententypen")
async def get_document_types() -> Dict[str, List[str]]:
    """
    Gibt die unterstützten Dokumententypen und ihre Keywords zurück.
    """
    return {
        doc_type: keywords
        for doc_type, keywords in bescheid_parser.DOCUMENT_TYPE_KEYWORDS.items()
    }


@router.post("/detect-type", summary="Dokumententyp erkennen")
async def detect_document_type(
    request: ScannerRequest,
    current_user: User = Depends(get_current_user),
) -> Dict[str, str]:
    """
    Erkennt den Dokumententyp aus OCR-Text.
    """
    doc_type = bescheid_parser.detect_document_type(request.ocr_text)
    return {
        "document_type": doc_type,
        "confidence": "high" if doc_type != "Unbekannt" else "low",
    }
