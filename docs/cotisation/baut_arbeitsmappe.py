#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
baut_arbeitsmappe.py - schreibt die Cotisation-Formeln in eine KOPIE der Mitgliederliste.

Das Original wird NICHT angefasst. Erzeugt wird
    GC 2026-09-24 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm

Eingebaut werden:
  * Blatt "Cotisation"  - alle Tarife, Schalter und Ausnahmen in Zellen
  * Blatt "Membres 2026_2027"
      - BW  = Sicherung der bisherigen Ergebnisse aus L (Saison 2025/26)
      - BN:BZ = Helferformeln
      - L   = die Ausgabeformel (reine Anzeige, alle Werte kommen aus den Helfern)

WARUM OHNE LET / XLOOKUP / MINIFS:
Das XLSX-Format speichert Funktionen neuerer Excel-Versionen mit Sonderpraefix
(_xlfn.LET, _xlfn.XLOOKUP, _xlfn.MINIFS). Ohne dieses Praefix zeigt Excel #NAME?.
Dieser Bausatz nutzt deshalb ausschliesslich klassische Funktionen
(IF, AND, OR, COUNTIFS, IFERROR, INDEX, MATCH, SUMPRODUCT, MIN, TEXT, ROW,
DATEVALUE, ISNUMBER) - damit die Datei in jeder Excel-Version, in LibreOffice
und in Google Sheets gleich laeuft.

Aufruf:
    python3 docs/cotisation/baut_arbeitsmappe.py
"""
from __future__ import annotations

import pathlib
import shutil
import sys

import openpyxl

DOCS = pathlib.Path("/Users/netjogger58/CascadeProjects/Vereins-OS/docs")
QUELLE = DOCS / "GC 2026-09-24 MEMBERSLESCHT 2026-2027.xlsm"
ZIEL = DOCS / "GC 2026-09-24 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm"

BLATT = "Membres 2026_2027"
ERSTE, LETZTE = 2, 773          # Datenzeilen (Blatt hat 773 Zeilen inkl. Kopf)

SP = dict(BN=66, BO=67, BP=68, BQ=69, BR=70, BS=71, BT=72, BU=73, BV=74,
          BW=75, BX=76, BY=77, BZ=78, CA=79, CB=80)

# Tarife und Schalter: Schluessel, Wert, Bedeutung (Zeile = Position in A/B)
TARIFE = [
    ("SEN", 300, "Einzelner Senior"),
    ("U25", 210, "Einzelner U25-Jugendspieler"),
    ("Familie", 384, "ab 2 aktiven Spielern oder gemischt SEN + U25"),
    ("Zusatz", 50, "Offizielle (AH/AI/AJ) oder Status N/R - freiwillig, Stimmrecht AG"),
    ("XSEUL", 300, "Fixbetrag, pro Zeile"),
    ("GAJGL", 0, "Fixbetrag, pro Zeile"),
    ("ZusatzBeiFamilie", "NEIN", "384 ist das Maximum -> kein +50 auf 384"),
    ("TraegerRegel", "Erste", "Erste = erste Zeile des Blocks | Aelteste = aeltestes Geburtsdatum"),
    ("ZusatzAuchOfficiel", "NEIN", "Rolle als Offizieller auch in Spalte BB werten"),
    ("ReservistenWert", "(0+50)", "Wert fuer Spieler mit Status R oder Code GAJGL, gilt auf der Zeile"),
    ("SaisonStichtag", "01.08.2026", "Saisonbeginn - das Alter wird an diesem Tag gemessen"),
    ("U25MaxAlter", 25, "Wer am Stichtag noch keine 25 Jahre alt ist, bleibt die ganze Saison U25"),
]

AUSNAHMEN = [
    ("Bourg", "Jeannot", "Don ? +(0 +50)"),
    ("Bourg-Thielen", "Gaby", "Don ? +(0 +50)"),
]

# Helfer: Spalte, Titel, Formelvorlage.  {r}=Zeile, {e}=erste, {l}=letzte
HELFER = [
    (SP["BN"], "FamID", '=IF($O{r}="","@"&ROW(),$O{r})'),
    (SP["BO"], "Schluessel",
     '=IF(ISNUMBER($J{r}),$J{r},IFERROR(DATEVALUE($J{r},"DD.MM.YYYY"),73415))-ROW()/1000000'),
    # kleinster Schluessel der Familie - SUMPRODUCT erzwingt die Array-Auswertung
    (SP["BP"], "Aeltester",
     '=SUMPRODUCT(MIN(($BN${e}:$BN${l}=$BN{r})*$BO${e}:$BO${l}'
     '+($BN${e}:$BN${l}<>$BN{r})*10^15))'),
    (SP["BQ"], "SpielerGes",
     '=COUNTIFS($BN${e}:$BN${l},$BN{r},$M${e}:$M${l},"J",$AG${e}:$AG${l},"<>")'),
    (SP["BR"], "SpielerSEN",
     '=COUNTIFS($BN${e}:$BN${l},$BN{r},$M${e}:$M${l},"J",$AG${e}:$AG${l},"<>",$K${e}:$K${l},"SEN")'),
    (SP["BS"], "SpielerU25",
     '=COUNTIFS($BN${e}:$BN${l},$BN{r},$M${e}:$M${l},"J",$AG${e}:$AG${l},"<>",$K${e}:$K${l},"U25")'),
    (SP["BT"], "Zusatz",
     "=" + "+".join('COUNTIFS($BN${e}:$BN${l},$BN{r},$AG${e}:$AG${l},"",$' + c
                    + '${e}:$' + c + '${l},"<>")' for c in ("AH", "AI", "AJ"))
     + "+" + "+".join('COUNTIFS($BN${e}:$BN${l},$BN{r},$AG${e}:$AG${l},"<>",$M${e}:$M${l},"'
                      + v + '")' for v in ("N", "R"))),
    # Traeger: TraegerRegel "Erste" = ERSTE Zeile des Familienblocks (Laufzaehler = 1),
    # "Aelteste" = kleinster Schluessel der Familie
    (SP["BU"], "Traeger",
     '=IF(Cotisation!$B$8="Aelteste",$BO{r}=$BP{r},'
     'COUNTIFS($BN${e}:$BN{r},$BN{r})=1)'),
    (SP["BX"], "Tarif",
     '=IF(OR($BQ{r}>=2,AND($BR{r}>=1,$BS{r}>=1)),Cotisation!$B$3,'
     'IF($BR{r}>=1,Cotisation!$B$1,IF($BS{r}>=1,Cotisation!$B$2,0)))'),
    (SP["BY"], "AusnahmeNr",
     '=IFERROR(MATCH($A{r}&"|"&$B{r},Cotisation!$G$2:$G$200,0),0)'),
    (SP["BZ"], "Zuschlag",
     '=IF(AND($BT{r}>=1,OR(Cotisation!$B$7="JA",$BX{r}<>Cotisation!$B$3)),Cotisation!$B$4,0)'),
    # Personenwert: Ausnahme (je Zeile) oder Spieler mit Status R / Code GAJGL
    (SP["CA"], "Personenwert",
     '=IF($BY{r}>0,INDEX(Cotisation!$F$2:$F$200,$BY{r}),'
     'IF(AND($AG{r}<>"",OR($M{r}="R",$O{r}="GAJGL")),Cotisation!$B$10,""))'),
    # Alterspruefung: U25 = am Saisonbeginn (Cotisation!B11) noch keine 25 Jahre alt
    # sein (Cotisation!B12). EDATE(J;12*Alter) ist der Geburtstag im Alter X: liegt
    # er nach dem Stichtag, ist die Person noch U25. Belegt: 0 Abweichungen ueber 329.
    (SP["CB"], "Alterspruefung",
     '=IFERROR(IF(IF(EDATE(IF(ISNUMBER($J{r}),$J{r},DATEVALUE($J{r},"DD.MM.YYYY")),'
     '12*Cotisation!$B$12)>DATEVALUE(Cotisation!$B$11;"DD.MM.YYYY"),"U25","SEN")'
     '<>$K{r},"PRUEFEN",""),"")'),
]

# Ausgabe in L - reine Anzeige, klassische Funktionen, keine Sonderpraefixe
FORMEL_L = (
    '=IF(AND($O{r}="",$M{r}=""),"",'
    'IF($BV{r}<>"",$BV{r}&"",'
    'IF($CA{r}<>"",$CA{r},'
    'IF($O{r}="XSEUL",TEXT(Cotisation!$B$5,"0"),'
    'IF($O{r}="GAJGL",TEXT(Cotisation!$B$6,"0"),'
    'IF(NOT($BU{r}),"",'
    'IF($BX{r}+$BZ{r}=0,"",'
    'IF($BX{r}=0,"(0+"&TEXT($BZ{r},"0")&")",'
    'TEXT($BX{r},"0")&IF($BZ{r}>0," (+0+"&TEXT($BZ{r},"0")&")","")))))))))'
)


def baue() -> int:
    if not QUELLE.exists():
        print(f"! Quelle fehlt: {QUELLE}", file=sys.stderr)
        return 2

    # Ergebnisse der alten Formel sichern (data_only liefert die berechneten Werte,
    # nicht die Formel-Objekte - die alte L ist eine Array-Formel mit _xlfn.LET)
    alt_wb = openpyxl.load_workbook(QUELLE, data_only=True)
    alt_ws = alt_wb[BLATT]
    alt_l = {r: alt_ws.cell(r, 12).value for r in range(ERSTE, LETZTE + 1)}
    alt_l = {r: v for r, v in alt_l.items() if v not in (None, "")}
    alt_wb.close()

    shutil.copy2(QUELLE, ZIEL)
    wb = openpyxl.load_workbook(ZIEL, keep_vba=True)
    ws = wb[BLATT]

    # 1) Blatt Cotisation (Tarife in A/B ab Zeile 1, Ausnahmen in D:F, Schluessel in G)
    if "Cotisation" in wb.sheetnames:
        del wb["Cotisation"]
    cfg = wb.create_sheet("Cotisation", 0)
    fett = openpyxl.styles.Font(bold=True)
    for i, (k, v, b) in enumerate(TARIFE, start=1):
        cfg.cell(i, 1, k).font = fett
        cfg.cell(i, 2, v)
        cfg.cell(i, 3, b)
    for j, t in enumerate(["Nom", "Prénom", "Ausgabe", "Schlüssel (automatisch)"], start=4):
        cfg.cell(1, j, t).font = fett
    for i, (nom, vorname, ausgabe) in enumerate(AUSNAHMEN, start=2):
        cfg.cell(i, 4, nom)
        cfg.cell(i, 5, vorname)
        cfg.cell(i, 6, ausgabe)
        cfg.cell(i, 7, f'=$D{i}&"|"&$E{i}').font = fett
    for i in range(len(AUSNAHMEN) + 2, 201):     # Schluesselbereich offen halten
        cfg.cell(i, 7, f'=$D{i}&"|"&$E{i}')
    for col, breite in (("A", 20), ("B", 10), ("C", 58), ("D", 18), ("E", 18), ("F", 18), ("G", 30)):
        cfg.column_dimensions[col].width = breite

    # 2) bisherige Ergebnisse aus L nach BW sichern
    ws.cell(1, SP["BW"], "L_alt_2025-26 (Ergebnis Sicherung)").font = fett
    for r, v in alt_l.items():
        ws.cell(r, SP["BW"], v)

    # 3) Helfer und Ausgabeformel
    for spalte, titel, _m in HELFER:
        ws.cell(1, spalte, titel).font = fett
    ws.cell(1, SP["BV"], "Manuell").font = fett
    for r in range(ERSTE, LETZTE + 1):
        fmt = dict(r=r, e=ERSTE, l=LETZTE)
        for spalte, _t, muster in HELFER:
            ws.cell(r, spalte, muster.format(**fmt))
        ws.cell(r, 12, FORMEL_L.format(**fmt))

    # 4) Excel soll beim Oeffnen einmal neu rechnen (openpyxl schreibt keine Werte)
    wb.calculation.fullCalcOnLoad = True
    wb.save(ZIEL)

    print(f"geschrieben : {ZIEL}")
    print(f"Blatt       : {BLATT}  Zeilen {ERSTE}-{LETZTE} ({LETZTE - ERSTE + 1})")
    print(f"gesichert   : {len(alt_l)} Ergebnisse der alten Formel nach Spalte BW")
    print(f"Formeln     : {len(HELFER)} Helfer + 1 Ausgabeformel je Zeile "
          f"= {(len(HELFER) + 1) * (LETZTE - ERSTE + 1)} Zellen")
    print(f"Tabellen    : Cotisation mit {len(TARIFE)} Eintraegen, {len(AUSNAHMEN)} Ausnahmen")
    return 0


if __name__ == "__main__":
    raise SystemExit(baue())
