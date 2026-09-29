"""Einziger Ort, an dem der Pfad zur fertigen Arbeitsmappe steht.

Wichtig fuer den Betrieb: der Tresorier benennt die Datei gelegentlich um
(z. B. neues Datum im Namen). Deshalb wird der Name NICHT ueberall hart
kodiert, sondern hier einmal aufgeloest:

  1. der konfigurierte Standardname, falls vorhanden
  2. sonst die neueste Datei `*_mit-Cotisation*.xlsm` im Docs-Ordner
  3. sonst Abbruch mit klarer Meldung

Ausgeschlossen werden Excel-Sperrdateien (`~$…`) und die Sicherungskopien
`….backup-<Zeitstempel>.xlsm`, die `build_perfect_workbook.py` vor jedem
Ueberschreiben anlegt.

Aufrufer: build_perfect_workbook.py, pruefe_formeln.py,
pruefe_alle_blaetter.py, ... (importiere `ziel()`).
"""
import os
import pathlib

DOCS = pathlib.Path(os.environ.get(
    "M75_COTISATION_DOCS", "/Users/netjogger58/CascadeProjects/Vereins-OS/docs"))
QUELLE_NAME = "GC 2026-09-24 MEMBERSLESCHT 2026-2027.xlsm"   # Original, nie anfassen
ZIEL_NAME = "GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm"
QUELLE = DOCS / QUELLE_NAME

# Explizit festgelegte Arbeitsdatei (z. B. --datei pfad.xlsx oder die aus
# Google Drive geladene Kopie). Ueberschreibt die Suche nach dem Standardnamen.
_FEST: pathlib.Path | None = None


def set_ziel(pfad) -> pathlib.Path:
    """Arbeitsdatei fest verankern - nuetzlich fuer die Drive-Kopie."""
    global _FEST
    _FEST = pathlib.Path(pfad).expanduser().resolve()
    return _FEST


def quelle() -> pathlib.Path:
    if not QUELLE.exists():
        raise SystemExit(f"! Quelle fehlt: {QUELLE}")
    return QUELLE


def datenquelle() -> pathlib.Path:
    """Die Datei, in der wirklich gearbeitet wird.

    Wichtig: Das Modell rechnet auf der ARBEITSDATEI, nicht auf dem Original.
    Sonst wuerden Mitglieder, die der Tresorier in der gebauten Mappe eintraegt
    (Zeilen 774-900), beim Stripe-Lauf einfach fehlen.

    Faellt auf das Original zurueck, wenn es keine Arbeitsdatei gibt.
    """
    try:
        z = ziel()
    except SystemExit:
        return quelle()
    if z.exists():
        return z
    print(f"! Keine Arbeitsdatei ({z}) - rechne mit dem Original {QUELLE.name}")
    return quelle()


def ziel() -> pathlib.Path:
    """Pfad der fertigen Mappe - rename-tolerant."""
    if _FEST is not None:
        return _FEST
    direkt = DOCS / ZIEL_NAME
    if direkt.exists():
        return direkt
    # Sicherungen tragen Suffixe wie .regeln-, .cardids-, .alterskat-,
    # .kopf-, .benevole-, .backup-, .REPARIERT-verdacht- (Zeitstempel).
    # Alle ausschliessen - sonst wuerde der Fallback eine Kopie als
    # Arbeitsdatei waehlen, wenn sie zufaellig das neueste mtime hat.
    def _ist_sicherung(p: pathlib.Path) -> bool:
        n = p.name
        return (n.startswith("~$")
                or p.name == ZIEL_NAME
                or any(f".{k}-" in n for k in (
                    "backup", "regeln", "cardids", "alterskat",
                    "kopf", "benevole", "REPARIERT")))

    kandidaten = [p for p in DOCS.glob("*_mit-Cotisation*.xlsm")
                  if not _ist_sicherung(p)]
    if not kandidaten:
        raise SystemExit(
            f"! Keine Arbeitsmappe gefunden.\n"
            f"  Erwartet: {DOCS / ZIEL_NAME}\n"
            f"  Auch kein '*_mit-Cotisation*.xlsm' im Ordner {DOCS}.")
    kandidaten.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    print(f"! '{ZIEL_NAME}' nicht gefunden -> arbeite weiter mit "
          f"'{kandidaten[0].name}' (Rename erkannt).")
    return kandidaten[0]
