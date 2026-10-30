"""
SkyOS Open Core - OCR Scanner Module
Agency Level Up 2025 (Pascal Weidermann, Hückelhoven)

Behördenbescheid-OCR-Parser mit Tesseract-Integration und strukturierter Datenextraktion.
Open-Source-Komponente für das SkyOS Open Core Paket.
"""

from .bescheid_parser import BescheidParser, BescheidData

__all__ = ["BescheidParser", "BescheidData"]
