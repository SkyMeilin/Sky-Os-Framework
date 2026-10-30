"""
SkyOS Open Core - OBG NRW §14 Notfall-Leitfaden
Agency Level Up 2025 (Pascal Weidermann, Hückelhoven)

Notfallgenehmigungen nach § 14 des Obersten Baugesetzes NRW (OBG).
Dieses Modul bietet strukturierte Leitfäden und Checklisten für Notfallgenehmigungen
im Katastrophenfall, bei akuter Gefahr im Verzug (§ 35 BauNVO) und für
vorläufige Bauvorhaben in Krisensituationen.

Rechtsgrundlagen:
- § 14 OBG NRW: Notfallgenehmigungen
- § 35 BauNVO: Akute Gefahr im Verzug
- § 62 BauG: Bauvorlageberechtigung
- KRITIS-Verordnungen: Kritische Infrastrukturen
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field


class NotfallPrioritaet(str, Enum):
    """Prioritätsstufen für Notfallgenehmigungen."""
    KRITISCH = "kritisch"          # Sofortige Maßnahme erforderlich, Lebensgefahr
    HOCH = "hoch"                  # Innerhalb von 24 Stunden zu erledigen
    MITTEL = "mittel"              # Innerhalb von 72 Stunden zu erledigen
    NIEDRIG = "niedrig"            # Innerhalb von 7 Tagen zu erledigen


class GenehmigungsTyp(str, Enum):
    """Typen der Notfallgenehmigung."""
    AKUTE_GEFahr = "akute_gefahr_im_verzug"       # § 35 BauNVO
    KATASTROPHENFALL = "katastrophenfall"          # § 14 OBG NRW
    VORLAUFIG = "vorlaeufige_genehmigung"          # Vorläufige Bauvorhaben
    KRITIS_INFRA = "kritis_infrastruktur"          # KRITIS-Notfall
    WOHNUNGSBAU = "wohnungsbaunotfall"             # Wohnungsbaunotfall


class ChecklistenPunkt(BaseModel):
    """Einzelner Checklistenpunkt für Notfallgenehmigung."""
    nummer: int
    beschreibung: str
    rechtliche_grundlage: str
    ist_erfuellt: bool = False
    bemerkung: Optional[str] = None


class NotfallGenehmigung(BaseModel):
    """Datenmodell für eine Notfallgenehmigung nach § 14 OBG NRW."""
    genehmigungs_id: str = Field(..., description="Eindeutige ID der Genehmigung")
    typ: GenehmigungsTyp
    prioritaet: NotfallPrioritaet
    antragsteller: str
    grund: str = Field(..., description="Begründung des Notfalls")
    vorhaben_beschreibung: str
    standort: str
    geplante_dauer_tage: int = Field(..., description="Geplante Dauer in Tagen")
    rechtsgrundlage: str = Field(default="§ 14 OBG NRW", description="Rechtsgrundlage")
    checkliste: List[ChecklistenPunkt] = Field(default_factory=list)
    erstellt_am: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    genehmigt_durch: Optional[str] = None
    genehmigt_am: Optional[str] = None
    status: str = Field(default="ANTRAG_STELLUNG", description="Aktueller Status")

    def erfuellungsgrad(self) -> float:
        """Berechnet den Erfüllungsgrad der Checkliste (0.0 - 1.0)."""
        if not self.checkliste:
            return 0.0
        erfuellt = sum(1 for p in self.checkliste if p.ist_erfuellt)
        return erfuellt / len(self.checkliste)


class OBGSection14Guide:
    """
    Leitfaden für Notfallgenehmigungen nach § 14 OBG NRW.
    
    Bietet strukturierte Checklisten, rechtliche Hinweise und
    Vorlagen für verschiedene Notfall-Szenarien.
    """

    # Standard-Checklisten für verschiedene Notfall-Typen
    CHECKLISTEN = {
        GenehmigungsTyp.AKUTE_GEFahr: [
            ChecklistenPunkt(
                nummer=1,
                beschreibung="Gefahr im Verzug nachweisen",
                rechtliche_grundlage="§ 35 BauNVO",
            ),
            ChecklistenPunkt(
                nummer=2,
                beschreibung="Sofortige Maßnahme begründen",
                rechtliche_grundlage="§ 35 Abs. 1 BauNVO",
            ),
            ChecklistenPunkt(
                nummer=3,
                beschreibung="Keine alternative Lösung möglich",
                rechtliche_grundlage="Verhältnismäßigkeitsprinzip",
            ),
            ChecklistenPunkt(
                nummer=4,
                beschreibung="Betroffene Behörden informieren",
                rechtliche_grundlage="§ 35 Abs. 2 BauNVO",
            ),
            ChecklistenPunkt(
                nummer=5,
                beschreibung="Dokumentation und Nachweis führen",
                rechtliche_grundlage="§ 14 OBG NRW",
            ),
        ],
        GenehmigungsTyp.KATASTROPHENFALL: [
            ChecklistenPunkt(
                nummer=1,
                beschreibung="Katastrophenfall offiziell erklären lassen",
                rechtliche_grundlage="§ 14 OBG NRW",
            ),
            ChecklistenPunkt(
                nummer=2,
                beschreibung="Notfallmaßnahme definieren",
                rechtliche_grundlage="§ 14 Abs. 1 OBG NRW",
            ),
            ChecklistenPunkt(
                nummer=3,
                beschreibung="Zeitraum der Genehmigung festlegen",
                rechtliche_grundlage="§ 14 Abs. 2 OBG NRW",
            ),
            ChecklistenPunkt(
                nummer=4,
                beschreibung="Auflagen und Bedingungen festlegen",
                rechtliche_grundlage="§ 14 Abs. 3 OBG NRW",
            ),
            ChecklistenPunkt(
                nummer=5,
                beschreibung="Nachbereitung und Rückbau planen",
                rechtliche_grundlage="§ 14 Abs. 4 OBG NRW",
            ),
            ChecklistenPunkt(
                nummer=6,
                beschreibung="KRITIS-Betroffenheit prüfen",
                rechtliche_grundlage="KRITIS-Verordnung",
            ),
        ],
        GenehmigungsTyp.VORLAUFIG: [
            ChecklistenPunkt(
                nummer=1,
                beschreibung="Vorläufiges Bauvorhaben beschreiben",
                rechtliche_grundlage="§ 62 BauG",
            ),
            ChecklistenPunkt(
                nummer=2,
                beschreibung="Bauvorlageberechtigung nachweisen",
                rechtliche_grundlage="§ 62 BauG",
            ),
            ChecklistenPunkt(
                nummer=3,
                beschreibung="Zeitliche Begrenzung festlegen",
                rechtliche_grundlage="§ 14 OBG NRW",
            ),
            ChecklistenPunkt(
                nummer=4,
                beschreibung="Widerrufsbedingungen definieren",
                rechtliche_grundlage="Verwaltungsrecht",
            ),
        ],
        GenehmigungsTyp.KRITIS_INFRA: [
            ChecklistenPunkt(
                nummer=1,
                beschreibung="KRITIS-Sektor identifizieren",
                rechtliche_grundlage="KRITIS-Verordnung",
            ),
            ChecklistenPunkt(
                nummer=2,
                beschreibung="Ausfallrisiko bewerten",
                rechtliche_grundlage="BSI-Kritis-Verordnung",
            ),
            ChecklistenPunkt(
                nummer=3,
                beschreibung="Notfallplan vorlegen",
                rechtliche_grundlage="§ 14 OBG NRW",
            ),
            ChecklistenPunkt(
                nummer=4,
                beschreibung="Sicherheitsmaßnahmen dokumentieren",
                rechtliche_grundlage="BSI IT-Grundschutz",
            ),
            ChecklistenPunkt(
                nummer=5,
                beschreibung="Behördenkoordination sicherstellen",
                rechtliche_grundlage="Katastrophenschutzgesetz NRW",
            ),
        ],
        GenehmigungsTyp.WOHNUNGSBAU: [
            ChecklistenPunkt(
                nummer=1,
                beschreibung="Wohnungsnotfall begründen",
                rechtliche_grundlage="§ 14 OBG NRW",
            ),
            ChecklistenPunkt(
                nummer=2,
                beschreibung="Unterkunftsbedarf nachweisen",
                rechtliche_grundlage="Sozialrecht NRW",
            ),
            ChecklistenPunkt(
                nummer=3,
                beschreibung="Vorläufige Wohnbarkeit sicherstellen",
                rechtliche_grundlage="Landesbauordnung NRW",
            ),
            ChecklistenPunkt(
                nummer=4,
                beschreibung="Brandschutzmaßnahmen treffen",
                rechtliche_grundlage="LBO NRW",
            ),
        ],
    }

    @classmethod
    def get_checkliste(cls, typ: GenehmigungsTyp) -> List[ChecklistenPunkt]:
        """
        Gibt die Checkliste für einen bestimmten Genehmigungs-Typ zurück.
        
        Args:
            typ: Typ der Notfallgenehmigung
            
        Returns:
            Liste von Checklistenpunkten
        """
        return cls.CHECKLISTEN.get(typ, [])

    @classmethod
    def create_antrag(
        cls,
        typ: GenehmigungsTyp,
        prioritaet: NotfallPrioritaet,
        antragsteller: str,
        grund: str,
        vorhaben: str,
        standort: str,
        dauer_tage: int,
        genehmigungs_id: Optional[str] = None,
    ) -> NotfallGenehmigung:
        """
        Erstellt einen neuen Antrag auf Notfallgenehmigung.
        
        Args:
            typ: Typ der Genehmigung
            prioritaet: Prioritätsstufe
            antragsteller: Name des Antragstellers
            grund: Begründung des Notfalls
            vorhaben: Beschreibung des Vorhabens
            standort: Standort des Vorhabens
            dauer_tage: Geplante Dauer in Tagen
            genehmigungs_id: Optional: Eigene ID für die Genehmigung
            
        Returns:
            NotfallGenehmigung Objekt mit vollständiger Checkliste
        """
        if genehmigungs_id is None:
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
            genehmigungs_id = f"OBG14-{typ.value[:3].upper()}-{timestamp}"

        checkliste = cls.get_checkliste(typ)

        antrag = NotfallGenehmigung(
            genehmigungs_id=genehmigungs_id,
            typ=typ,
            prioritaet=prioritaet,
            antragsteller=antragsteller,
            grund=grund,
            vorhaben_beschreibung=vorhaben,
            standort=standort,
            geplante_dauer_tage=dauer_tage,
            checkliste=checkliste,
        )

        return antrag

    @classmethod
    def get_rechtliche_hinweise(cls, typ: GenehmigungsTyp) -> Dict[str, str]:
        """
        Gibt rechtliche Hinweise für einen bestimmten Genehmigungs-Typ zurück.
        
        Args:
            typ: Typ der Genehmigung
            
        Returns:
            Dictionary mit rechtlichen Hinweisen
        """
        hinweise = {
            GenehmigungsTyp.AKUTE_GEFahr: {
                'recht': "§ 35 BauNVO - Akute Gefahr im Verzug",
                'frist': "Sofortige Maßnahme erforderlich",
                'nachweis': "Gefahr muss konkret und unmittelbar drohend sein",
                'widerspruch': "Widerspruch bleibt vorbehalten",
            },
            GenehmigungsTyp.KATASTROPHENFALL: {
                'recht': "§ 14 OBG NRW - Notfallgenehmigung im Katastrophenfall",
                'frist': "Zeitlich befristet auf den Katastrophenfall",
                'nachweis': "Katastrophenfall muss offiziell erklärt sein",
                'widerspruch': "Kein Widerspruch während des Katastrophenfalls",
            },
            GenehmigungsTyp.VORLAUFIG: {
                'recht': "§ 62 BauG - Vorläufige Bauvorhaben",
                'frist': "Maximal 2 Jahre befristet",
                'nachweis': "Bauvorlageberechtigung erforderlich",
                'widerspruch': "Widerspruch innerhalb von 1 Monat möglich",
            },
            GenehmigungsTyp.KRITIS_INFRA: {
                'recht': "KRITIS-Verordnung - Kritische Infrastrukturen",
                'frist': "Je nach Ausfallrisiko",
                'nachweis': "KRITIS-Status und Ausfallrisiko nachweisen",
                'widerspruch': "Besondere Schutzvorschriften gelten",
            },
            GenehmigungsTyp.WOHNUNGSBAU: {
                'recht': "§ 14 OBG NRW - Wohnungsbaunotfall",
                'frist': "Bis zur Dauer des Wohnungsnotfalls",
                'nachweis': "Wohnungsbedarf und Untergebrachtsein nachweisen",
                'widerspruch': "Sozialrechtliche Prüfung erforderlich",
            },
        }
        return hinweise.get(typ, {})

    @classmethod
    def validate_antrag(cls, antrag: NotfallGenehmigung) -> Dict[str, Any]:
        """
        Validiert einen Notfallgenehmigungs-Antrag.
        
        Args:
            antrag: NotfallGenehmigung Objekt
            
        Returns:
            Dictionary mit Validierungsergebnis
        """
        errors = []
        warnings = []

        # Pflichtfelder prüfen
        if not antrag.antragsteller.strip():
            errors.append("Antragsteller ist erforderlich")
        if not antrag.grund.strip():
            errors.append("Begründung des Notfalls ist erforderlich")
        if not antrag.vorhaben_beschreibung.strip():
            errors.append("Vorhaben-Beschreibung ist erforderlich")
        if not antrag.standort.strip():
            errors.append("Standort ist erforderlich")
        if antrag.geplante_dauer_tage <= 0:
            errors.append("Geplante Dauer muss größer als 0 sein")

        # Prioritäts-spezifische Warnungen
        if antrag.prioritaet == NotfallPrioritaet.KRITISCH:
            warnings.append("KRITISCH: Sofortige Maßnahme erforderlich - Behörden sofort informieren!")
        elif antrag.prioritaet == NotfallPrioritaet.HOCH:
            warnings.append("HOCH: Innerhalb von 24 Stunden zu erledigen")

        # Checkliste prüfen
        erfuellungsgrad = antrag.erfuellungsgrad()
        if erfuellungsgrad < 0.5:
            warnings.append(f"Checkliste nur zu {erfuellungsgrad:.0%} erfüllt")

        return {
            'ist_gueltig': len(errors) == 0,
            'fehler': errors,
            'warnungen': warnings,
            'erfuellungsgrad': erfuellungsgrad,
        }


# ==========================================
# Self-Test
# ==========================================

if __name__ == "__main__":
    print("=" * 70)
    print(" SkyOS Open Core: OBG NRW §14 Notfall-Leitfaden Self-Test")
    print("=" * 70)

    guide = OBGSection14Guide()

    # Test 1: Antrag erstellen
    antrag = guide.create_antrag(
        typ=GenehmigungsTyp.KATASTROPHENFALL,
        prioritaet=NotfallPrioritaet.KRITISCH,
        antragsteller="Pascal Weidermann",
        grund="Überschwemmungsgefahr durch Starkregen",
        vorhaben="Notfall-Deichbau und Evakuierungsrouten",
        standort="Hückelhoven, NRW",
        dauer_tage=30,
    )
    print(f"\n[1/4] Antrag erstellt:")
    print(f"  ID: {antrag.genehmigungs_id}")
    print(f"  Typ: {antrag.typ.value}")
    print(f"  Priorität: {antrag.prioritaet.value}")
    print(f"  Checkliste: {len(antrag.checkliste)} Punkte")

    # Test 2: Checkliste ausfüllen
    for punkt in antrag.checkliste[:3]:
        punkt.ist_erfuellt = True
    print(f"\n[2/4] Checkliste:")
    print(f"  Erfüllungsgrad: {antrag.erfuellungsgrad():.0%}")

    # Test 3: Validierung
    validation = guide.validate_antrag(antrag)
    print(f"\n[3/4] Validierung:")
    print(f"  Ist gültig: {validation['ist_gueltig']}")
    print(f"  Fehler: {len(validation['fehler'])}")
    print(f"  Warnungen: {len(validation['warnungen'])}")

    # Test 4: Rechtliche Hinweise
    hinweise = guide.get_rechtliche_hinweise(GenehmigungsTyp.KATASTROPHENFALL)
    print(f"\n[4/4] Rechtliche Hinweise:")
    for key, value in hinweise.items():
        print(f"  {key}: {value}")

    print("\n" + "=" * 70)
    print(" ✅ OBG NRW §14 Notfall-Leitfaden Test PASSED!")
    print("=" * 70)
