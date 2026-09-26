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
      - BN:CC = Helferformeln
      - L   = die Ausgabeformel (reine Anzeige, alle Werte kommen aus den Helfern)

WARUM CHIRURGISCH UND NICHT MIT OPENPYXL:
Ein vollstaendiges Neuschreiben mit openpyxl erzeugte eine Datei, die Excel mit
"Problem bei einigen Inhalten erkannt" ablehnt. Zwei belegte Gruende:
  1. openpyxl setzt das neue Blatt an Position 0 - die 70 definierten Namen der
     Mappe (u. a. _FilterDatabase mit localSheetId 0/1/2/8) zeigen danach auf
     falsche Blaetter.
  2. openpyxl verliert xl/metadata.xml, auf die 1.842 Zellen per cm= verweisen.
Deshalb wird hier das Original-ZIP Teil fuer Teil uebernommen und nur veraendert:
  * xl/worksheets/sheet1.xml  (Membres 2026_2027): Spalte L + Helfer BN:CC
  * xl/worksheets/sheet13.xml: NEU, Blatt Cotisation, am ENDE angehaengt, damit
    die localSheetId der definierten Namen gueltig bleiben
  * xl/workbook.xml           : ein <sheet>-Eintrag am Ende, fullCalcOnLoad
  * xl/_rels/workbook.xml.rels: eine Beziehung, calcChain entfernt
  * [Content_Types].xml       : ein Override, calcChain-Override entfernt
  * xl/calcChain.xml          : geloescht (die Formeln haben sich geaendert)
Alles andere bleibt Byte fuer Byte erhalten: Kommentare, Metadaten, sharedStrings,
Formatvorlagen, VBA und alle uebrigen Blaetter.

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

import csv
import pathlib
import re
import zipfile
import sys


DOCS = pathlib.Path("/Users/netjogger58/CascadeProjects/Vereins-OS/docs")
QUELLE = DOCS / "GC 2026-09-24 MEMBERSLESCHT 2026-2027.xlsm"
ZIEL = DOCS / "GC 2026-09-24 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm"

BLATT = "Membres 2026_2027"
BLATT_XML = "xl/worksheets/sheet1.xml"       # das ist die Datei des Blattes oben
CONFIG_BLATT = "Cotisation"                  # neues Blatt, wird hinten angehaengt
CONFIG_XML = "xl/worksheets/sheet13.xml"     # das Original hat sheet1..sheet12
ERSTE, LETZTE = 2, 773          # Datenzeilen (Blatt hat 773 Zeilen inkl. Kopf)

SP = dict(BN=66, BO=67, BP=68, BQ=69, BR=70, BS=71, BT=72, BU=73, BV=74,
          BW=75, BX=76, BY=77, BZ=78, CA=79, CB=80, CC=81)

CONFIG = pathlib.Path("/Users/netjogger58/CascadeProjects/mersch75test.github.io/docs/cotisation")


def liese_config(datei: pathlib.Path) -> list[tuple[str, object, str]]:
    """Liest eine Config-CSV (Schluessel;Wert;Bemerkung) als Liste von Tripeln.
    Die CSV ist die einzige Quelle - der Bausatz pflegt keine eigene Liste mehr."""
    if not datei.exists():
        raise SystemExit(f"! Config fehlt: {datei}")
    with open(datei, encoding="utf-8-sig", newline="") as fh:
        zeilen = [r for r in csv.reader(fh, delimiter=";") if any(c.strip() for c in r)]
    out = []
    for row in zeilen[1:]:
        row = (row + ["", "", ""])[:3]          # auf 3 Spalten auffuellen
        k, w, b = (x.strip() for x in row)
        if w.lstrip("-").isdigit():
            w = int(w)
        out.append((k, w, b))
    return out

# Tarife, Schalter, Ausnahmen und Haushalte kommen aus den CSV-Dateien nebenan
TARIFE = liese_config(CONFIG / "tarife-cotisation.csv")
AUSNAHMEN = [(n.strip(), p.strip(), a.strip()) for n, p, a in
             liese_config(CONFIG / "ausnahmen-cotisation.csv")]
HAUSHALTE = [(n.strip(), str(p).strip()) for n, p, _b in
             liese_config(CONFIG / "haushalte-cotisation.csv")]

# Helfer: Spalte, Titel, Formelvorlage.  {r}=Zeile, {e}=erste, {l}=letzte
HELFER = [
    # Haushaltsschluessel: normalerweise der Familiencode O. Steht die Adresse in der
    # Haushaltsliste (Cotisation!I2:I50), ist der ganze Haushalt eine Einheit - auch
    # wenn die Mitglieder verschiedene Codes haben (z. B. ANSAY-Brueder, beide XSEUL).
    (SP["BN"], "FamID",
     '=IF($O{r}="","@"&ROW(),IF(SUMPRODUCT(--('
     'SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Cotisation!$I$2:$I$50)," ",""),".",""),"\'","")'
     '=SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER($G{r})," ",""),".",""),"\'","")))>0,'
     '"ADR:"&SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER($G{r})," ",""),".",""),"\'",""),$O{r}))'),
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
    # XSEUL 300 - aber nur, wenn der Haushalt nicht schon 2 aktive Spieler hat.
    # Sonst greift der Familientarif 384 (ANSAY-Brueder: 1x 384 statt 2x 300).
    (SP["CC"], "XSEULwert",
     '=IF($O{r}<>"XSEUL";"",IF(AND(LEFT($BN{r},4)="ADR:";$BQ{r}>=2);"",'
     'TEXT(Cotisation!$B$5;"0")))'),
]

# Ausgabe in L - reine Anzeige, klassische Funktionen, keine Sonderpraefixe
FORMEL_L = (
    '=IF(AND($O{r}="",$M{r}=""),"",'
    'IF($BV{r}<>"",$BV{r}&"",'
    'IF($CA{r}<>"",$CA{r},'
    'IF($CC{r}<>"",$CC{r},'
    'IF($O{r}="GAJGL",TEXT(Cotisation!$B$6,"0"),'
    'IF(NOT($BU{r}),"",'
    'IF($BX{r}+$BZ{r}=0,"",'
    'IF($BX{r}=0,"(0+"&TEXT($BZ{r},"0")&")",'
    'TEXT($BX{r},"0")&IF($BZ{r}>0," (+0+"&TEXT($BZ{r},"0")&")","")))))))))'
)


def esc(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def zelle_text(ref, text):
    return f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{esc(text)}</t></is></c>'


def zelle_formel(ref, formel):
    # Im XLSX wird die Formel OHNE fuehrendes = gespeichert (<f>IF(...)</f>).
    # Mit "=" wuerde Excel daraus ==IF(...) machen.
    return f'<c r="{ref}"><f>{esc(str(formel).lstrip("="))}</f></c>'


def zelle_leer(ref):
    return f'<c r="{ref}"/>'


def spalte_liste(i: int) -> str:
    """66 -> BN, 79 -> CA, 81 -> CC"""
    s = ""
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


# ---------------------------------------------------------------- neues Blatt
def baue_config_sheet() -> str:
    zeilen = {}
    for i, (k, v, b) in enumerate(TARIFE, start=1):
        teile = [zelle_text(f"A{i}", k), zelle_text(f"B{i}", v), zelle_text(f"C{i}", b)]
        if isinstance(v, int):
            teile[1] = f'<c r="B{i}"><v>{v}</v></c>'
        zeilen[i] = teile
    kopf = [zelle_text("A1", "Tarif"), zelle_text("B1", "Wert"), zelle_text("C1", "Bedeutung"),
            zelle_text("D1", "Nom"), zelle_text("E1", "Prénom"), zelle_text("F1", "Ausgabe"),
            zelle_text("G1", "Schlüssel (automatisch)"),
            zelle_text("I1", "Adresse gleicher Haushalt"), zelle_text("J1", "Bemerkung")]
    zeilen[1] = kopf
    for i, (nom, vorname, ausgabe) in enumerate(AUSNAHMEN, start=2):
        zeilen.setdefault(i, []).extend([zelle_text(f"D{i}", nom), zelle_text(f"E{i}", vorname),
                                         zelle_text(f"F{i}", ausgabe),
                                         zelle_formel(f"G{i}", f'=$D{i}&"|"&$E{i}')])
    for i in range(len(AUSNAHMEN) + 2, 60):        # Schluesselbereich offen halten
        zeilen.setdefault(i, []).append(zelle_formel(f"G{i}", f'=$D{i}&"|"&$E{i}'))
    for i, (adresse, bemerkung) in enumerate(HAUSHALTE, start=2):
        zeilen.setdefault(i, []).extend([zelle_text(f"I{i}", adresse), zelle_text(f"J{i}", bemerkung)])

    koerper = "".join(
        f'<row r="{i}">' + "".join(zeilen[i]) + "</row>" for i in sorted(zeilen))
    cols = "".join(
        f'<col min="{n}" max="{n}" width="{w}" customWidth="1"/>'
        for n, w in ((1, 20), (2, 10), (3, 58), (4, 18), (5, 18), (6, 18), (7, 30), (9, 28), (10, 60)))
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            f'<dimension ref="A1:J{max(zeilen)}"/><sheetViews><sheetView workbookViewId="0"/>'
            '</sheetViews><sheetFormatPr defaultRowHeight="15"/>'
            f'<cols>{cols}</cols><sheetData>{koerper}</sheetData></worksheet>')


# ------------------------------------------------------- Blatt Membres ändern
def col_index(buchstaben: str) -> int:
    n = 0
    for c in buchstaben:
        n = n * 26 + ord(c) - 64
    return n


def baue_membres_sheet(xml: str) -> tuple[str, int]:
    """Ersetzt Spalte L, ergänzt die Helfer BN:CC und die Sicherung BW.
    Alles andere (Kommentare, cm= Metadaten, Formatvorlagen) bleibt unangetastet."""
    gesichert = 0

    def zeile_ersetzen(m):
        nonlocal gesichert
        r = int(m.group(1))
        inhalt = m.group(3)
        alt_l = re.search(r'<c r="L%d"(?P<attr>[^>]*?)(?:/>|>(?P<inhalt>.*?)</c>)' % r, inhalt, re.S)
        bw = ""
        if alt_l:
            val = re.search(r"<v>(.*?)</v>", alt_l.group("inhalt") or "", re.S)
            if val and val.group(1).strip():
                # alten Wert unveraendert in BW spiegeln. t="str" ist nur fuer
                # Formelzellen gueltig, daher als Inline-Text uebernehmen
                # (der Wert ist im Quell-XML bereits escaped).
                bw = (f'<c r="BW{r}" t="inlineStr"><is>'
                      f'<t xml:space="preserve">{val.group(1)}</t></is></c>')
                gesichert += 1

        # alle vorhandenen Zellen der Zeile behalten, nur L ersetzen.
        # Innerhalb einer Zeile muessen die Zellen aufsteigend nach Spalte
        # sortiert sein - deshalb an der richtigen Stelle wieder einfuegen.
        zellen = re.findall(r'<c r="([A-Z]+)\d+"[^>]*?(?:/>|>.*?</c>)', inhalt, re.S)
        roh = re.findall(r'(<c r="[A-Z]+\d+"[^>]*?(?:/>|>.*?</c>))', inhalt, re.S)
        behalten = [(col_index(c), x) for c, x in zip(zellen, roh)
                    if not (c == "L") and col_index(c) not in (SP[k] for k in ("BV", "BW"))]

        fmt = dict(r=r, e=ERSTE, l=LETZTE)
        neu_l = [(12, zelle_formel(f"L{r}", FORMEL_L.format(**fmt)))]   # 12 = Spalte L
        for spalte, _t, muster in HELFER:
            neu_l.append((spalte, zelle_formel(f"{spalte_liste(spalte)}{r}", muster.format(**fmt))))
        if bw:
            neu_l.append((SP["BW"], bw))
        neu_l.append((SP["BV"], zelle_leer(f"BV{r}")))     # BV Manuell: Eingabefeld

        alle = sorted(behalten + neu_l, key=lambda kv: kv[0])
        return f'<row r="{r}"{m.group(2)}>' + "".join(x for _i, x in alle) + "</row>"

    xml = re.sub(r'<row r="(\d+)"([^>]*)>(.*?)</row>',
                 lambda m: zeile_ersetzen(m) if ERSTE <= int(m.group(1)) <= LETZTE else m.group(0),
                 xml, flags=re.S)

    kopf = {SP["BV"]: "Manuell", SP["BW"]: "L_alt_2025-26 (Ergebnis Sicherung)"}
    for spalte, titel, _m in HELFER:
        kopf[spalte] = titel
    m1 = re.search(r'<row r="1"([^>]*)>(.*?)</row>', xml, re.S)
    if m1:
        zusatz = "".join(zelle_text(f"{spalte_liste(s)}1", t)
                         for s, t in sorted(kopf.items(), key=lambda kv: kv[0]))
        xml = xml[:m1.start()] + f'<row r="1" spans="1:{max(kopf)}">' + m1.group(2) + zusatz \
            + "</row>" + xml[m1.end():]
    xml = re.sub(r'<dimension ref="A1:[A-Z]+\d+"/>',
                 f'<dimension ref="A1:{spalte_liste(max(kopf))}{LETZTE}"/>', xml, count=1)
    return xml, gesichert


# ------------------------------------------------------------------- Datei bauen
def baue() -> int:
    if not QUELLE.exists():
        print(f"! Quelle fehlt: {QUELLE}", file=sys.stderr)
        return 2

    with zipfile.ZipFile(QUELLE) as zin:
        teile = {n: zin.read(n) for n in zin.namelist()}
        reihenfolge = zin.namelist()

    if BLATT_XML not in teile:
        print(f"! {BLATT_XML} fehlt - falsche Quelle?", file=sys.stderr)
        return 2

    # 1) Blatt Membres: Spalte L + Helfer
    neues_membres, gesichert = baue_membres_sheet(teile[BLATT_XML].decode("utf-8"))
    teile[BLATT_XML] = neues_membres.encode("utf-8")

    # 2) Neues Blatt Cotisation - am ENDE, damit localSheetId gueltig bleibt
    teile[CONFIG_XML] = baue_config_sheet().encode("utf-8")
    reihenfolge.append(CONFIG_XML)

    rid = "rIdCotisation"
    wb = teile["xl/workbook.xml"].decode("utf-8")
    sheetids = [int(x) for x in re.findall(r'sheetId="(\d+)"', wb)] or [0]
    wb = wb.replace("</sheets>",
                    f'<sheet name="{CONFIG_BLATT}" sheetId="{max(sheetids) + 1}" r:id="{rid}"/>'
                    "</sheets>")
    wb = re.sub(r"<calcPr([^>]*?)/>",
                lambda m: "<calcPr" + re.sub(r'\sfullCalcOnLoad="[^"]*"', "", m.group(1))
                + ' fullCalcOnLoad="1"/>', wb, count=1)
    teile["xl/workbook.xml"] = wb.encode("utf-8")

    rels = teile["xl/_rels/workbook.xml.rels"].decode("utf-8")
    rels = re.sub(r'<Relationship[^>]*calcChain\.xml[^>]*/>', "", rels)
    rels = rels.replace("</Relationships>",
                        f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/'
                        'officeDocument/2006/relationships/worksheet" '
                        f'Target="worksheets/{CONFIG_XML.split("/")[-1]}"/></Relationships>')
    teile["xl/_rels/workbook.xml.rels"] = rels.encode("utf-8")

    ct = teile["[Content_Types].xml"].decode("utf-8")
    ct = re.sub(r'<Override[^>]*calcChain\.xml[^>]*/>', "", ct)
    ct = ct.replace("</Types>",
                    '<Override PartName="/xl/worksheets/'
                    f'{CONFIG_XML.split("/")[-1]}" ContentType="application/vnd.openxmlformats-'
                    'officedocument.spreadsheetml.worksheet+xml"/></Types>')
    teile["[Content_Types].xml"] = ct.encode("utf-8")

    # 3) calcChain loeschen: die Formeln haben sich geaendert, Excel baut sie neu auf
    teile.pop("xl/calcChain.xml", None)
    reihenfolge = [n for n in reihenfolge if n != "xl/calcChain.xml"]

    if ZIEL.exists():
        ZIEL.unlink()
    with zipfile.ZipFile(ZIEL, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in reihenfolge:
            zout.writestr(name, teile[name])

    print(f"geschrieben : {ZIEL}")
    print(f"Blatt       : {BLATT}  Zeilen {ERSTE}-{LETZTE} ({LETZTE - ERSTE + 1})")
    print(f"gesichert   : {gesichert} Ergebnisse der alten Formel nach Spalte BW")
    print(f"Formeln     : {len(HELFER)} Helfer + 1 Ausgabeformel je Zeile "
          f"= {(len(HELFER) + 1) * (LETZTE - ERSTE + 1)} Zellen")
    print(f"Tabelle     : Blatt {CONFIG_BLATT} mit {len(TARIFE)} Eintraegen, "
          f"{len(AUSNAHMEN)} Ausnahmen, {len(HAUSHALTE)} Haushalten")
    print("unveraendert: Kommentare, Metadaten, sharedStrings, VBA, alle anderen Blaetter")
    return 0


if __name__ == "__main__":
    raise SystemExit(baue())
