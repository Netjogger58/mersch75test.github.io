#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
baut_arbeitsmappe.py - schreibt die Cotisation-Formeln in eine KOPIE der Mitgliederliste.

Das Original wird NICHT angefasst. Erzeugt wird
    GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm

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
# Quelle ist die vom Benutzer bearbeitete Datei (Spieler J/R/N nach Spalte L verschoben,
# neue Spalte N "BEZAHLT J/N", Cotisatioun jetzt in M). Das Original vom 24.09. bleibt
# unangetastet, TEST1_nur-calcchain.xlsm ist die von Excel gespeicherte Arbeitsfassung.
QUELLE = DOCS / "TEST1_nur-calcchain.xlsm"
ZIEL = DOCS / "GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm"

BLATT = "Membres 2026_2027"
CONFIG_BLATT = "Cotisation"                  # neues Blatt, wird hinten angehaengt
ERSTE, LETZTE = 2, 773          # Datenzeilen (Blatt hat 773 Zeilen inkl. Kopf)

# ------------------------------------------------------ Spalten im Blatt "Membres"
# Kopfzeile (Stand 26.09.2026, nach dem Umbau durch den Benutzer):
#   J  Naissance      K  Alterskategorie   L  Spieler J/R/N
#   M  Cotisatioun  <- AUSGABE            N  BEZAHLT J/N   (Eingabe Kassierer)
#   P  Code Courrier neu = Haushaltscode   AH Spielerlizenz  AI/AJ/AK Offiziellenlizenz
# Helfer beginnen hinter der letzten Datenspalte BN (66).
SP = dict(BP=68, BQ=69, BR=70, BS=71, BT=72, BU=73, BV=74, BW=75, BX=76,
          BY=77, BZ=78, CA=79, CB=80, CC=81, CD=82, CE=83)
SP_ZIEL = "M"          # Spalte mit der Ausgabe
SP_SPIELT = "L"        # Spalte Spieler J/R/N (Eingabe)
SP_BEZAHLT = "N"       # Spalte BEZAHLT J/N (Eingabe Kassierer)
SP_FAM = "P"           # Code Courrier neu
SP_LIZ_SP = "AH"       # Spielerlizenz
SP_LIZ_OFF = ("AI", "AJ", "AK")
SP_MANUELL = "BX"      # Helfer: manuelle Vorgabe
SP_SICHER = "CE"       # Helfer: Sicherung des alten M-Wertes

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
    # Haushaltsschluessel: normalerweise der Familiencode P. Steht die Adresse in der
    # Haushaltsliste (Cotisation!I2:I50), ist der ganze Haushalt eine Einheit - auch
    # wenn die Mitglieder verschiedene Codes haben (z. B. ANSAY-Brueder, beide XSEUL).
    (SP["BP"], "FamID",
     '=IF($P{r}="","@"&ROW(),IF(SUMPRODUCT(--('
     'SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Cotisation!$I$2:$I$50)," ",""),".",""),"\'","")'
     '=SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER($G{r})," ",""),".",""),"\'","")))>0,'
     '"ADR:"&SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER($G{r})," ",""),".",""),"\'",""),$P{r}))'),
    # Schluessel = Geburtsdatum plus Zeilennummernanteil -> bei gleichem Datum
    # gewinnt die oberste Zeile (das Plus ist wichtig, siehe pruef_cotisation).
    (SP["BQ"], "Schluessel",
     '=IF(ISNUMBER($J{r}),$J{r},IFERROR(DATEVALUE($J{r}),73415))+ROW()/1000000'),
    # kleinster Schluessel der Familie - SUMPRODUCT erzwingt die Array-Auswertung
    (SP["BR"], "Aeltester",
     '=SUMPRODUCT(MIN(($BP${e}:$BP${l}=$BP{r})*$BQ${e}:$BQ${l}'
     '+($BP${e}:$BP${l}<>$BP{r})*10^15))'),
    (SP["BS"], "SpielerGes",
     '=COUNTIFS($BP${e}:$BP${l},$BP{r},$L${e}:$L${l},"J",$AH${e}:$AH${l},"<>")'),
    (SP["BT"], "SpielerSEN",
     '=COUNTIFS($BP${e}:$BP${l},$BP{r},$L${e}:$L${l},"J",$AH${e}:$AH${l},"<>",$K${e}:$K${l},"SEN")'),
    (SP["BU"], "SpielerU25",
     '=COUNTIFS($BP${e}:$BP${l},$BP{r},$L${e}:$L${l},"J",$AH${e}:$AH${l},"<>",$K${e}:$K${l},"U25")'),
    # Zusatzperson: Offizielle OHNE Spielerlizenz (AI/AJ/AK) oder Spieler mit Status N/R.
    # "///" gilt dabei als leer, sonst wuerde jede ungepflegte Zeile einen Zuschlag ausloesen.
    (SP["BV"], "Zusatz",
     "=" + "+".join('COUNTIFS($BP${e}:$BP${l},$BP{r},$AH${e}:$AH${l},"",'
                    + c + '${e}:' + c + '${l},"<>",' + c + '${e}:' + c + '${l},"<>///")'
                    for c in SP_LIZ_OFF)
     + "+" + "+".join('COUNTIFS($BP${e}:$BP${l},$BP{r},$AH${e}:$AH${l},"<>",$L${e}:$L${l},"'
                      + v + '")' for v in ("N", "R"))),
    # Traeger: TraegerRegel "Aelteste" = kleinster Schluessel der Familie (Standard).
    # Faellt der Ersatzwert 73415 als kleinster Schluessel an, hat niemand ein
    # Geburtsdatum - dann gewinnt die oberste Zeile des Familienblocks.
    # "Erste" = immer die oberste Zeile des Familienblocks.
    (SP["BW"], "Traeger",
     '=IF($BP{r}="","",IF(Cotisation!$B$8<>"Aelteste",'
     'IF(COUNTIFS($BP${e}:$BP{r},$BP{r})=1,"TRAEGER",""),'
     'IF($BR{r}>=73415,IF(COUNTIFS($BP${e}:$BP{r},$BP{r})=1,"TRAEGER",""),'
     'IF($BQ{r}=$BR{r},"TRAEGER",""))))'),
    (SP["BY"], "Tarif",
     '=IF(OR($BS{r}>=2,AND($BT{r}>=1,$BU{r}>=1)),Cotisation!$B$3,'
     'IF($BT{r}>=1,Cotisation!$B$1,IF($BU{r}>=1,Cotisation!$B$2,0)))'),
    (SP["BZ"], "AusnahmeNr",
     '=IFERROR(MATCH($A{r}&"|"&$B{r},Cotisation!$G$2:$G$200,0),0)'),
    (SP["CA"], "Zuschlag",
     '=IF(AND($BV{r}>=1,OR(Cotisation!$B$7="JA",$BY{r}<>Cotisation!$B$3)),Cotisation!$B$4,0)'),
    # Personenwert: namentliche Ausnahme (je Zeile) oder Spieler mit Status R / GAJGL
    # oder Spieler mit Lizenz, der bei den Frage-Spalten AW:AZ "FRAGEN" hat.
    # WICHTIG: auf Status R pruefen, NICHT auf "<>J und <>N". Die Variante
    # trifft auch X (und jeden Unsinn) und wuerde einem X-Spieler faelschlich
    # den Reservistenwert geben. Python testet ebenfalls auf "R".
    # Der Personenwert entfaellt, wenn der Haushalt den Familientarif 384 zahlt
    # (Maximum, analog zur Zuschlag-Regel in CA) - sonst wuerde ein Reservist
    # im Haushalt die ganze Familie auf 50 druecken (BISENIUS Z64).
    # Comite-Mitglieder ohne eigenen Spielertarif zahlen statt "(0+50)" die 50
    # direkt - aber nur wenn sie nicht selbst spielen (O <> "J", EPPS Z163).
    # Der Personenwert entfaellt, wenn der Haushalt den Familientarif 384 zahlt
    # (Maximum, analog zur Zuschlag-Regel in CA) - sonst wuerde ein Reservist
    # im Haushalt die ganze Familie auf 50 druecken (BISENIUS Z64).
    # XSEUL/GAJGL sind Sondercodes, keine Familientarife - dort bleibt es.
    (SP["CB"], "Personenwert",
     '=IF($BZ{r}>0,INDEX(Cotisation!$F$2:$F$200,$BZ{r}),'
     'IF(AND($BY{r}<>Cotisation!$B$3,OR($P{r}="XSEUL",$P{r}="GAJGL"),'
     'OR(AND($L{r}="R",$AH{r}<>""),'
     'AND($AH{r}<>"",COUNTIF($AW{r}:$AZ{r},"FRAGEN")>0),'
     '$P{r}="GAJGL")),Cotisation!$B$10,""))'),
    # Alterspruefung: U25 = am Saisonbeginn (Cotisation!B11) noch keine 25 Jahre alt
    # sein (Cotisation!B12). EDATE(J;12*Alter) ist der Geburtstag im Alter X: liegt
    # er nach dem Stichtag, ist die Person noch U25. Belegt: 0 Abweichungen ueber 329.
    (SP["CC"], "Alterspruefung",
     '=IFERROR(IF(IF(EDATE(IF(ISNUMBER($J{r}),$J{r},DATEVALUE($J{r})),'
     '12*Cotisation!$B$12)>DATEVALUE(Cotisation!$B$11),"U25","SEN")'
     '<>$K{r},"PRUEFEN",""),"")'),
    # XSEUL 300 - aber nur, wenn der Haushalt nicht schon 2 aktive Spieler hat.
    # Sonst greift der Familientarif 384 (ANSAY-Brueder: 1x 384 statt 2x 300).
    # XSEUL richtet sich nach dem Spielstatus (L), nicht nach der Lizenz:
    #   J -> 300 (Fixbetrag fuer Spieler), R oder N -> (0+50), sonst 0.
    # Die ADR-Ausnahme bleibt: ein echter Haushalt (gelistete Adresse) mit
    # mindestens 2 aktiven Spielern zahlt den Familientarif 384 statt 300
    # (ANSAY-Brueder, gleiche Adresse, beide XSEUL).
    # Kein Durchfallen bei "kein Status": sonst wuerde der Traeger der
    # 74-kopfigen XSEUL-Gruppe den Familientarif 384 bekommen.
    (SP["CD"], "XSEULwert",
     '=IF($P{r}<>"XSEUL","",IF(AND(LEFT($BP{r},4)="ADR:",$BS{r}>=2),"",'
     'IF($L{r}="J",TEXT(Cotisation!$B$5,"0"),'
     'IF(OR($L{r}="N",$L{r}="R"),"(0+"&TEXT(Cotisation!$B$4,"0")&")","0"))))'),
]

# Ausgabe in M - reine Anzeige, klassische Funktionen, keine Sonderpraefixe.
# Reihenfolge: leere Zeile -> manuelle Vorgabe -> Personenwert (aktive Spieler)
#              -> Rechnungstraeger (XSEUL 300, sonst Tarif + Zuschlag)
#              -> sonst der Haushaltscode Fxxxx, damit die Zugehoerigkeit sichtbar ist.
FORMEL_M = (
    '=IF($BP{r}="","",'
    'IF($BX{r}<>"",$BX{r}&"",'
    'IF($CB{r}<>"",$CB{r}&"",'
    'IF($CD{r}<>"",$CD{r}&"",'
    'IF($BW{r}="TRAEGER",'
    'IF($BY{r}=0,'
    'IF($CA{r}>0,"(0+"&TEXT($CA{r},"0")&")",""),'
    'TEXT($BY{r},"0")&IF($CA{r}>0," (+0+"&TEXT($CA{r},"0")&")",""))&"",'
    'IF(LEFT($BP{r},4)="ADR:",$P{r}&"",$BP{r}&""))))))'
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
    # Wichtig: Die Tarife stehen ab Zeile 1, weil die Formeln auf
    # Cotisation!$B$1 ... $B$12 verweisen. Die Ueberschriften fuer die
    # Ausnahmen stehen deshalb in derselben Zeile, in den Spalten D bis J.
    zeilen = {}
    for i, (k, v, b) in enumerate(TARIFE, start=1):
        wert = f'<c r="B{i}"><v>{v}</v></c>' if isinstance(v, int) else zelle_text(f"B{i}", v)
        zeilen[i] = [zelle_text(f"A{i}", k), wert, zelle_text(f"C{i}", b)]
    zeilen[1].extend([
        zelle_text("D1", "Nom"), zelle_text("E1", "Prénom"), zelle_text("F1", "Ausgabe"),
        zelle_text("G1", "Schlüssel (automatisch)"),
        zelle_text("I1", "Adresse gleicher Haushalt"), zelle_text("J1", "Bemerkung")])
    for i, (nom, vorname, ausgabe) in enumerate(AUSNAHMEN, start=2):
        zeilen.setdefault(i, []).extend([zelle_text(f"D{i}", nom), zelle_text(f"E{i}", vorname),
                                         zelle_text(f"F{i}", ausgabe),
                                         zelle_formel(f"G{i}", f'=$D{i}&"|"&$E{i}')])
    for i in range(max(len(AUSNAHMEN) + 2, len(TARIFE) + 2), 200):
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


def baue_membres_sheet(xml: str, werte: dict[int, str],
                       mit_m: bool = True, mit_helper: bool = True,
                       mit_kopf: bool = True) -> tuple[str, int]:
    """Setzt Spalte M, ergaenzt die Helfer BP:CE und die Sicherung CE.

    Die drei Schalter erlauben die Bisektion B1a/B1b/B1c: welcher der drei
    Teile der Blatt-1-Aenderung laesst Excel die Reparatur-Meldung zeigen?
    mit_m     -> nur die Zellen M ersetzen
    mit_helper-> nur die Helfer BP:CE hinten anhaengen
    mit_kopf  -> nur die Helfernamen in der Kopfzeile ergaenzen

    WICHTIG - so wenig wie moeglich am XML aendern:
    Die Zeilen werden NICHT neu aus ihren Zellen zusammengesetzt. Stattdessen wird
    in jeder Datenzeile genau die vorhandene Zelle M durch die neue ersetzt (reiner
    Textersatz an genau einer Stelle) und die Helferzellen direkt vor </row>
    angehaengt - sie stehen hinter BN, sind also bereits in aufsteigender
    Spaltenfolge. Kommentare, cm= Metadaten, Formatvorlagen, Array-Formeln und
    alle uebrigen Zellen bleiben Byte fuer Byte unangetastet.

    Genau dieses Minimum war der Grund fuer die Reparatur-Meldung von Excel:
    in der ersten Fassung wurden alle Zellen der Zeile per Regex neu ausgelesen
    und neu zusammengesetzt, wodurch Details wie t="array" ref="..." oder
    cm="1" verloren gingen.
    """
    gesichert = 0

    def zeile_ersetzen(m):
        nonlocal gesichert
        r = int(m.group(1))
        inhalt = m.group(3)

        # 1) vorhandene Zelle M durch die neue ersetzen (nur diese eine Stelle)
        alt_m = re.search(r'<c r="M%d"(?P<attr>[^>]*?)(?:/>|>(?P<inhalt>.*?)</c>)' % r,
                          inhalt, re.S)
        sicherung = ""
        if alt_m:
            wert = re.search(r"<v>(.*?)</v>", alt_m.group("inhalt") or "", re.S)
            if wert and wert.group(1).strip():
                # alten Wert unveraendert in CE spiegeln. t="str" ist nur fuer
                # Formelzellen gueltig, daher als Inline-Text uebernehmen
                # (der Wert ist im Quell-XML bereits escaped).
                sicherung = (f'<c r="CE{r}" t="inlineStr"><is>'
                             f'<t xml:space="preserve">{wert.group(1)}</t></is></c>')
                gesichert += 1
        # Stil der alten M-Zelle uebernehmen, damit die Optik der Spalte bleibt.
        stil = ""
        if alt_m and 's="' in (alt_m.group("attr") or ""):
            stil = ' s="%s"' % re.search(r's="(\d+)"', alt_m.group("attr")).group(1)

        fmt = dict(r=r, e=ERSTE, l=LETZTE)
        formel_m = esc(FORMEL_M.format(**fmt).lstrip("="))
        # Wert aus dem Python-Referenzmodell als <v> mitschreiben: die Datei zeigt
        # damit schon vor der ersten Neuberechnung durch Excel das richtige Ergebnis.
        # WICHTIG: t="str" nur, wenn der Wert wirklich ein Text ist - ein
        # numerischer Wert mit t="str" ist eine Typabweichung, die Excel als
        # reparaturwuerdig einstufen kann.
        wert_m = werte.get(r, "")
        zahl = wert_m.isdigit()
        if wert_m and zahl:
            neu_m = f'<c r="M{r}"{stil}><f>{formel_m}</f><v>{esc(wert_m)}</v></c>'
        elif wert_m:
            neu_m = (f'<c r="M{r}"{stil} t="str"><f>{formel_m}</f>'
                     f'<v>{esc(wert_m)}</v></c>')
        else:
            neu_m = f'<c r="M{r}"{stil}><f>{formel_m}</f></c>'
        zellen = []
        if mit_m:
            if alt_m:
                # Gezielter Textersatz: die alte M-Zelle wird an genau ihrer Stelle
                # durch die neue ersetzt. Der Rest der Zeile bleibt unberuehrt.
                inhalt = inhalt[:alt_m.start()] + neu_m + inhalt[alt_m.end():]
            else:
                # M fehlt in der Zeile: vor der ersten Zelle mit groesserer Spalte
                # einfuegen, damit die aufsteigende Reihenfolge gewahrt bleibt.
                pos = 0
                for treffer in re.finditer(r'<c r="([A-Z]+)\d+"', inhalt):
                    if col_index(treffer.group(1)) > col_index(SP_ZIEL):
                        pos = treffer.start()
                        break
                    pos = treffer.end()
                inhalt = inhalt[:pos] + neu_m + inhalt[pos:]

        # Helferzellen: alle hinter BN, deshalb in Spaltenfolge anhaengen.
        # Sortiert wird, damit die aufsteigende Reihenfolge in der Zeile stimmt.
        neu_helper = []
        if mit_helper:
            for spalte, _t, muster in HELFER:
                neu_helper.append((spalte, zelle_formel(
                    f"{spalte_liste(spalte)}{r}", muster.format(**fmt))))
            neu_helper.append((col_index(SP_MANUELL), zelle_leer(f"{SP_MANUELL}{r}")))
            if sicherung:
                neu_helper.append((SP["CE"], sicherung))
        zellen += [x for _c, x in sorted(neu_helper, key=lambda kv: kv[0])]

        return f'<row r="{r}"{m.group(2)}>' + inhalt + "".join(zellen) + "</row>"

    xml = re.sub(r'<row r="(\d+)"([^>]*)>(.*?)</row>',
                 lambda m: zeile_ersetzen(m) if ERSTE <= int(m.group(1)) <= LETZTE else m.group(0),
                 xml, flags=re.S)

    # Kopfzeile: nur die Helfernamen anhaengen. ACHTUNG - die Attribute der
    # Zeile (spans, ht, customHeight, ...) muessen erhalten bleiben. Sie stehen
    # in Gruppe 1, der Zellinhalt in Gruppe 2. Ein Verwechseln schreibt die
    # Attribute als Text in die Zeile - das ist schema-widrig und loest genau
    # die Meldung "Problem bei einigen Inhalten" aus.
    kopf = {SP["BX"]: "Manuell", SP["CE"]: "M_alt (Sicherung Wert 2025/26)"}
    for spalte, titel, _m in HELFER:
        kopf[spalte] = titel
    letzte_spalte = 83 if (mit_helper or mit_kopf) else 66
    letzter_name = spalte_liste(letzte_spalte)
    m1 = re.search(r'<row r="1"([^>]*)>(.*?)</row>', xml, re.S)
    if m1 and mit_kopf:
        attribute = re.sub(r'\sspans="[^"]*"', "", m1.group(1))
        zusatz = "".join(zelle_text(f"{spalte_liste(s)}1", t)
                         for s, t in sorted(kopf.items(), key=lambda kv: kv[0]))
        xml = (xml[:m1.start()]
               + f'<row r="1" spans="1:{letzte_spalte}"{attribute}>'
               + m1.group(2) + zusatz + "</row>" + xml[m1.end():])

    # spans JE Zeile aus den tatsaechlich vorhandenen Zellen berechnen - ein
    # pauschaler Wert wuerde auf Zeilen ohne Helferzellen falsch liegen.
    def spans_anpassen(m):
        rnr, attribute, koerper = m.group(1), m.group(2), m.group(3)
        spalten = [col_index(x) for x in re.findall(r'<c r="([A-Z]+)\d+"', koerper)]
        if not spalten:
            return m.group(0)
        maxsp = max(spalten)
        if "spans=" in attribute:
            attribute = re.sub(r'spans="[^"]*"', f'spans="1:{maxsp}"', attribute)
        else:
            attribute += f' spans="1:{maxsp}"'
        return f'<row r="{rnr}"{attribute}>{koerper}</row>'

    xml = re.sub(r'<row r="(\d+)"([^>]*)>(.*?)</row>',
                 lambda m: spans_anpassen(m) if ERSTE <= int(m.group(1)) <= LETZTE else m.group(0),
                 xml, flags=re.S)

    xml = re.sub(r'<dimension ref="A1:[A-Z]+\d+"/>',
                 f'<dimension ref="A1:{letzter_name}{LETZTE}"/>', xml, count=1)
    return xml, gesichert


# ------------------------------------------------- Daten aus dem Blatt auslesen
def liese_blatt(teile: dict, pfad: str) -> list[list[str]]:
    """Liest das Mitgliederblatt als Liste von Zeilen (Kopfzeile zuerst).
    noetig, weil der Benutzer die Zeilen in Excel umsortiert hat - der alte
    CSV-Export hat also eine andere Reihenfolge als das Blatt."""
    ss = re.findall(r"<si>(.*?)</si>", teile["xl/sharedStrings.xml"].decode("utf-8"), re.S)
    ss = ["".join(re.findall(r"<t[^>]*>(.*?)</t>", s, re.S)) for s in ss]
    xml = teile[pfad].decode("utf-8")

    def wert(m):
        zelle = m.group(0)
        # Inline-Text (t="inlineStr"): der Build schreibt die neuen Spalten-
        # kopfzeilen (N, O) und alle Texte so, damit die Shared-String-
        # Tabelle unangetastet bleibt. Ohne diesen Zweig kaeme fuer N/O/...
        # eine LEERE Kopfzeile - und das Modell fand die Spalte nicht.
        if 't="inlineStr"' in zelle:
            t = re.search(r"<is>.*?<t[^>]*>(.*?)</t>.*?</is>", zelle, re.S)
            if not t:
                return ""
            return (t.group(1).replace("&amp;", "&").replace("&lt;", "<")
                    .replace("&gt;", ">").replace("&quot;", '"').replace("&apos;", "'"))
        v = re.search(r"<v>(.*?)</v>", m.group(0), re.S)
        if not v:
            return ""
        roh = v.group(1)
        if 't="s"' in zelle:
            return ss[int(roh)]
        return (roh.replace("&amp;", "&").replace("&lt;", "<")
                .replace("&gt;", ">").replace("&quot;", '"').replace("&apos;", "'"))

    zeilen = {}
    for m in re.finditer(r'<row r="(\d+)"[^>]*>(.*?)</row>', xml, re.S):
        r = int(m.group(1))
        zellen = {}
        for c in re.finditer(r'<c r="([A-Z]+)\d+"[^>]*?(?:/>|>.*?</c>)', m.group(2), re.S):
            zellen[col_index(c.group(1))] = wert(c)
        zeilen[r] = [zellen.get(i, "") for i in range(1, max(zellen, default=0) + 1)]
    kopf = zeilen.get(1, [])
    breite = max((len(z) for z in zeilen.values()), default=0)
    kopf = (kopf + [""] * breite)[:breite]
    # Bis zur LETZTEN VORHANDENEN Zeile lesen, nicht nur bis LETZTE: die
    # Arbeitsmappe hat Reservezeilen bis 900. Wer dort ein neues Mitglied
    # eintragt, muss vom Modell gesehen werden - sonst fehlt es bei Stripe.
    letzte_vorhanden = max(zeilen) if zeilen else LETZTE
    return [kopf] + [(zeilen.get(r, []) + [""] * breite)[:breite]
                     for r in range(ERSTE, max(letzte_vorhanden, LETZTE) + 1)]


def rechne_werte(teile: dict, pfad: str) -> dict[int, str]:
    """Berechnet mit dem Python-Referenzmodell den Wert jeder Zeile (Spalte M).
    Der Wert wird als <v> in die Zelle geschrieben, damit die Mappe auch dann
    das Richtige anzeigt, wenn Excel beim Oeffnen noch nicht gerechnet hat."""
    sys.path.insert(0, str(CONFIG))
    import csv as _csv
    import pruef_cotisation as pr                                   # noqa: E402

    def cfg(name):
        """Liest die nebenliegende Config-CSV. Die Kopfzeile wird nur uebersprungen,
        wenn wirklich eine vorhanden ist - ausnahmen- und haushalte-cotisation.csv
        haben keine, ein blindes [1:] verliert sonst BOURG und den ANSAY-Haushalt."""
        sys.path.insert(0, str(CONFIG))
        import pruef_cotisation as pr                                   # noqa: E402
        return pr.liese_config(CONFIG / name)

    tarife = pr.lade_tarife(CONFIG / "tarife-cotisation.csv")
    ausnahmen = {(n.strip().upper(), p.strip().upper()): a.strip()
                 for n, p, a in cfg("ausnahmen-cotisation.csv")}
    haushalte = {pr.normalisiere_adresse(a.strip())
                 for a, _b, *_rest in ((r + ["", ""])[:3] for r in cfg("haushalte-cotisation.csv"))
                 if a.strip()}
    zeilen = liese_blatt(teile, pfad)
    ergebnis = pr.berechne(zeilen, ausnahmen, *tarife, haushalte)
    return {x["excel_zeile"]: x["neu"] for x in ergebnis}


# ------------------------------------------------------------------- Datei bauen
def finde_blatt(teile: dict, name: str) -> str:
    """Ermittelt den XML-Pfad des Blattes - er ist nach dem Speichern durch Excel
    nicht garantiert sheet1.xml (es haengt von der Reihenfolge der Blaetter ab)."""
    wb = teile["xl/workbook.xml"].decode("utf-8")
    rid = re.search(r'<sheet[^>]*name="%s"[^>]*r:id="([^"]+)"' % re.escape(name), wb)
    if not rid:
        raise SystemExit(f"! Blatt '{name}' nicht im Workbook gefunden")
    rels = teile["xl/_rels/workbook.xml.rels"].decode("utf-8")
    ziel = re.search(r'Id="%s"[^>]*Target="([^"]+)"' % re.escape(rid.group(1)), rels)
    if not ziel:
        raise SystemExit(f"! Beziehung {rid.group(1)} fehlt in workbook.xml.rels")
    return "xl/" + ziel.group(1).lstrip("/")


def baue() -> int:
    if not QUELLE.exists():
        print(f"! Quelle fehlt: {QUELLE}", file=sys.stderr)
        return 2

    with zipfile.ZipFile(QUELLE) as zin:
        teile = {n: zin.read(n) for n in zin.namelist()}
        reihenfolge = zin.namelist()

    try:
        BLATT_XML = finde_blatt(teile, BLATT)
    except SystemExit as err:
        print(err, file=sys.stderr)
        return 2
    # Name des neuen Blatts: erst ein freier, danach die naechste Nummer
    vorhanden = [int(m.group(1)) for m in
                 (re.match(r"xl/worksheets/sheet(\d+)\.xml$", n) for n in teile) if m]
    CONFIG_XML = f"xl/worksheets/sheet{max(vorhanden) + 1}.xml"

    # 1) Werte aus dem Python-Referenzmodell (liest das Blatt der Quelldatei)
    werte = rechne_werte(teile, BLATT_XML)

    # 2) Blatt Membres: Spalte M + Helfer
    neues_membres, gesichert = baue_membres_sheet(teile[BLATT_XML].decode("utf-8"), werte)
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

    # 3b) docProps/app.xml: Anzahl der Arbeitsblaetter und Titel nachziehen.
    #     Excel prueft diese Datei gegen das Workbook - ein alter Stand fuehrt zur
    #     Meldung "Problem bei einigen Inhalten erkannt".
    if "docProps/app.xml" in teile:
        app = teile["docProps/app.xml"].decode("utf-8")
        vorhandene_blaetter = re.findall(r'<sheet name="([^"]+)"', wb)
        alt = len(vorhandene_blaetter) - 1
        titel_liste = re.findall(r"<vt:lpstr>([^<]*)</vt:lpstr>",
                                 re.search(r"<TitlesOfParts>(.*?)</TitlesOfParts>", app, re.S).group(1))
        app = re.sub(r"(<vt:lpstr>Arbeitsblätter</vt:lpstr></vt:variant><vt:variant><vt:i4>)\d+(</vt:i4>)",
                     lambda m: m.group(1) + str(alt + 1) + m.group(2), app, count=1)
        app = re.sub(r'(<TitlesOfParts><vt:vector size=")(\d+)(")',
                     lambda m: m.group(1) + str(int(m.group(2)) + 1) + m.group(3), app, count=1)
        # Der neue Blattname muss direkt hinter dem LETZTEN Blatt stehen und
        # vor den benannten Bereichen - sonst meckert Excel ueber die Datei.
        letztes_blatt = None
        for name in reversed(titel_liste):
            if name in vorhandene_blaetter:
                letztes_blatt = name
                break
        app = app.replace(f"<vt:lpstr>{letztes_blatt}</vt:lpstr>",
                          f"<vt:lpstr>{letztes_blatt}</vt:lpstr><vt:lpstr>{CONFIG_BLATT}</vt:lpstr>", 1)
        teile["docProps/app.xml"] = app.encode("utf-8")

    # 4) calcChain loeschen: die Formeln haben sich geaendert, Excel baut sie neu auf
    teile.pop("xl/calcChain.xml", None)
    reihenfolge = [n for n in reihenfolge if n != "xl/calcChain.xml"]

    if ZIEL.exists():
        ZIEL.unlink()
    with zipfile.ZipFile(ZIEL, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in reihenfolge:
            zout.writestr(name, teile[name])

    print(f"geschrieben : {ZIEL}")
    print(f"Quelle      : {QUELLE.name}")
    print(f"Blatt       : {BLATT}  Zeilen {ERSTE}-{LETZTE} ({LETZTE - ERSTE + 1})")
    print(f"gesichert   : {gesichert} Ergebnisse der alten Formel nach Spalte CE")
    print(f"Formeln     : {len(HELFER)} Helfer + 1 Ausgabeformel je Zeile "
          f"= {(len(HELFER) + 1) * (LETZTE - ERSTE + 1)} Zellen")
    betraege = sum(1 for w in werte.values() if w and not w.startswith("F"))
    codes = sum(1 for w in werte.values() if w.startswith("F"))
    print(f"Ausgabe M   : {betraege} Betraege, {codes} Familiencodes, "
          f"{sum(1 for w in werte.values() if not w)} leer")
    print(f"Tabelle     : Blatt {CONFIG_BLATT} mit {len(TARIFE)} Eintraegen, "
          f"{len(AUSNAHMEN)} Ausnahmen, {len(HAUSHALTE)} Haushalten")
    print("unveraendert: Kommentare, sharedStrings, VBA, alle anderen Blaetter")
    return 0


if __name__ == "__main__":
    raise SystemExit(baue())
