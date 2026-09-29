"""Strengere Pruefung ueber ALLE Blaetter - deckt Fehler auf, die mein
bisheriger Test (nur sheet1) nicht sieht.

Geprueft je Blatt:
  * Zellen aufsteigend, keine doppelt
  * r-Attribut passt zur tatsaechlichen Zeile und Spalte
  * Reihenfolge der Kindelemente in <c>:  <f> vor <v>/<is>
  * Reihenfolge der Kindelemente in <worksheet> laut OOXML-Schema
  * <dimension> deckt die benutzten Zellen ab
"""
import pathlib
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mappe

Z = str(mappe.ziel())
if len(sys.argv) > 1:
    Z = sys.argv[1]

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
REIHENFOLGE = ["sheetPr", "dimension", "sheetViews", "sheetFormatPr", "cols",
               "sheetData", "sheetCalcPr", "sheetProtection", "protectedRanges",
               "scenarios", "autoFilter", "sortState", "dataConsolidate",
               "customSheetViews", "mergeCells", "phoneticPr",
               "conditionalFormatting", "dataValidations", "hyperlinks",
               "printOptions", "pageMargins", "pageSetup", "headerFooter",
               "rowBreaks", "colBreaks", "customProperties", "cellWatches",
               "ignoredErrors", "smartTags", "drawing", "legacyDrawing",
               "picture", "oleObjects", "controls", "webPublishItems",
               "tableParts", "extLst"]
C_REIHENFOLGE = ["f", "v", "is"]


def kurz(tag):
    return tag.replace(NS, "")


def ci(name):
    n = 0
    for c in name:
        n = n * 26 + ord(c) - 64
    return n


def pruefe(pfad):
    z = zipfile.ZipFile(pfad)
    fehler = []
    for name in sorted(n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml$", n)):
        xml_raw = z.read(name).decode("utf-8")
        wurzel = ET.fromstring(xml_raw)

        # 1) Reihenfolge der Wurzelelemente
        gesehen = [kurz(k.tag) for k in wurzel]
        ordnung = [REIHENFOLGE.index(k) for k in gesehen if k in REIHENFOLGE]
        if ordnung != sorted(ordnung):
            fehler.append(f"{name}: Elemente ausser der Reihenfolge {gesehen}")

        # 2) <c>-Kindreihenfolge und r-Attribut
        maxcol = 0
        for row in wurzel.iter(f"{NS}row"):
            rnr = row.get("r")
            letztesignal, letzte_spalte = None, -1
            for c in row:
                if c.tag != f"{NS}c":
                    continue
                ref = c.get("r") or ""
                m = re.match(r"([A-Z]+)(\d+)$", ref)
                if not m:
                    fehler.append(f"{name} Zeile {rnr}: Zelle ohne gueltiges r='{ref}'")
                    continue
                if m.group(2) != rnr:
                    fehler.append(f"{name}: r='{ref}' steht in Zeile {rnr}")
                spalte = ci(m.group(1))
                if spalte <= letzte_spalte:
                    fehler.append(f"{name} Zeile {rnr}: Spalte {m.group(1)} nicht aufsteigend")
                letzte_spalte = spalte
                maxcol = max(maxcol, spalte)
                kinder = [kurz(k.tag) for k in c]
                if [C_REIHENFOLGE.index(k) for k in kinder if k in C_REIHENFOLGE] != \
                   sorted(C_REIHENFOLGE.index(k) for k in kinder if k in C_REIHENFOLGE):
                    fehler.append(f"{name} {ref}: <c>-Kinder falsch geordnet {kinder}")
                if "f" in kinder and "is" in kinder:
                    fehler.append(f"{name} {ref}: <f> und <is> zusammen")
                if c.get("t") == "inlineStr" and "is" not in kinder:
                    fehler.append(f"{name} {ref}: t='inlineStr' ohne <is>")
            if row.text and row.text.strip():
                fehler.append(f"{name} Zeile {rnr}: Text '{row.text.strip()[:30]}'")

        # 3) dimension deckt ab
        dim = wurzel.find(f"{NS}dimension")
        if dim is not None and dim.get("ref"):
            ende = dim.get("ref").split(":")[-1]
            m = re.match(r"([A-Z]+)(\d+)$", ende)
            if m and ci(m.group(1)) < maxcol:
                fehler.append(f"{name}: dimension {dim.get('ref')} zu klein, "
                              f"benutzt bis Spalte {maxcol}")

        # 4) Bereichs-Ungereimtheiten: dimension, autoFilter, sortState und
        #    mergeCells muessen zueinander passen. Excel prueft das.
        bereiche = {}
        for tag in ("dimension", "autoFilter", "sortState"):
            m = re.search(r'<' + tag + r'[^>]*ref="([^"]+)"', xml_raw)
            if m:
                bereiche[tag] = m.group(1)
        mc = re.search(r'<mergeCells[^>]*>(.*?)</mergeCells>', xml_raw, re.S)
        if mc:
            bereiche["mergeCells"] = ",".join(re.findall(r'ref="([^"]+)"', mc.group(1)))
        lz = [int(x) for x in re.findall(r"\$?[A-Z]{1,3}(\d+)", bereiche.get("dimension", ""))]
        for tag in ("autoFilter", "sortState"):
            if tag in bereiche:
                zeilen = [int(x) for x in re.findall(r"\d+", bereiche[tag])]
                if zeilen and lz and zeilen[-1] != lz[-1]:
                    fehler.append(f"{name}: {tag} endet in Zeile {zeilen[-1]}, "
                                  f"dimension in Zeile {lz[-1]}")
        blatt = name.split("/")[-1]
        rels = f"xl/worksheets/_rels/{blatt}.rels"
        z.close() if False else None
        if not any(n == rels for n in z.namelist()):
            fehler.append(f"{name}: keine _rels-Datei (nur fatal bei Kommentaren/VML)")
    return fehler


alle = pruefe(Z)
print("Geprueft:", Z.split("/")[-1])
if alle:
    print("FEHLER:", len(alle))
    seen = set()
    for f in alle:
        kurzform = re.sub(r"\d+", "#", f)
        if kurzform in seen:
            continue
        seen.add(kurzform)
        print("  -", f)
    print("  (Typen:", len(seen), ")")
else:
    print("keine Befunde")
