"""Prueft, ob Excel die geschriebenen Formeln parsen kann.

Excel repariert die Datei auch dann, wenn zwar das XML stimmt, eine Formel
aber syntaktisch kaputt ist (unbalancierte Klammer, unbekannte Funktion,
falsch gebildeter Zellbezug). Genau das war bisher nirgends geprueft.
"""
import collections
import pathlib
import re
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mappe

Z = str(mappe.ziel())
if len(sys.argv) > 1:
    Z = sys.argv[1]

FUNKTIONEN = set("""IF AND OR NOT COUNTIFS COUNTIF SUM SUMPRODUCT MIN MINIFS MAX MAXIFS
TEXT LEFT RIGHT MID LEN ROW ROWS COLUMN COLUMNS INDEX MATCH IFERROR IFNA
ISNUMBER ISBLANK ISERROR DATE DATEVALUE EDATE VLOOKUP HLOOKUP XLOOKUP LET
AVERAGEIFS SUMIFS CONCATENATE TRIM SUBSTITUTE UPPER LOWER YEAR MONTH DAY
ABS ROUND INDIRECT OFFSET CHOOSE ROWS N T HYPERLINK CLEAN REPT FIND
SEARCH MEDIAN STDEV VAR TRANSPOSE FREQUENCY CELL INFO TYPE VALUE
PMT RATE NPER FV PV""".split())


def unesc(s):
    return (s.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
            .replace("&apos;", "'").replace("&amp;", "&"))


def pruefe_formel(text, ref):
    fehler = []
    # Klammern innerhalb von Textliteralen herausrechnen
    ohne_literale = re.sub(r'"[^"]*"', '""', text)
    if ohne_literale.count("(") != ohne_literale.count(")"):
        fehler.append(f"unbalancierte Klammer: {ohne_literale.count('(')} ( gegen "
                      f"{ohne_literale.count(')')} )")
    if ohne_literale.count('"') % 2:
        fehler.append("ungerade Anzahl Anfuehrungszeichen")
    if text.startswith("="):
        fehler.append("Formel beginnt mit = (wird im XLSX weggelassen)")
    for name in set(re.findall(r"([A-ZÄÖÜ][A-ZÄÖÜa-zäöüß0-9_.]*)\s*\(", ohne_literale)):
        if name.upper() not in FUNKTIONEN and not name.upper().startswith("_XLFN"):
            fehler.append(f"unbekannte Funktion: {name}")
    # Bereichsbezuege: Spalte..Zeile..Spalte..Zeile
    for sprung in re.findall(r"\$[A-Z]{1,3}\$\d+:\$[A-Z]{1,3}\$\d+", ohne_literale):
        a, b = sprung.split(":")
        za, zb = int(re.search(r"\$(\d+)$", a).group(1)), int(re.search(r"\$(\d+)$", b).group(1))
        if za > zb:
            fehler.append(f"Bereich verkehrt herum: {sprung}")
    for bezug in re.findall(r"(?<![A-Z0-9_$!])\$?([A-Z]{1,3})\$?(\d{1,7})(?![0-9(])", ohne_literale):
        if int(bezug[1]) > 1048576:
            fehler.append(f"Zeilennummer zu gross: {bezug}")
    return fehler


z = zipfile.ZipFile(Z)
from xml.etree import ElementTree as ET                  # noqa: E402
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

geprueft = 0
muster = {}
fehler_gesamt = 0
for name in z.namelist():
    if not re.match(r"xl/worksheets/sheet\d+\.xml$", name):
        continue
    for c in ET.fromstring(z.read(name)).iter(f"{NS}c"):
        f = c.find(f"{NS}f")
        if f is None or not (f.text or "").strip():
            continue
        ref = c.get("r")
        text = f.text
        geprueft += 1
        # Zeilen- und Spaltennummern abstreichen, um gleiche Formeln zu buendeln
        schluessel = re.sub(r"(\$?)([A-Z]{1,3})(\$?)(\d+)", r"\1C\3N", text)
        schluessel = re.sub(r"\b\d{4,}\b", "N", schluessel)
        if schluessel in muster:
            continue
        muster[schluessel] = text
        fehler = pruefe_formel(text, ref)
        if fehler:
            fehler_gesamt += 1
            print(f"FEHLER {name} {ref}: {fehler[0]}")
            print(f"      {text[:160]}")

print()
print("Formelzellen geprueft:", geprueft)
print("verschiedene Formelmuster:", len(muster))
print("Muster mit Fehlern:", fehler_gesamt)
if not fehler_gesamt:
    print("Ergebnis: alle Formeln sind syntaktisch in Ordnung")
