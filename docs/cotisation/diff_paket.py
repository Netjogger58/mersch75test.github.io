"""Zeigt die Unterschiede in den Paket-Dateien zwischen Quelle und Ziel."""
import difflib
import re
import zipfile

Q = ("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
     "TEST1_nur-calcchain.xlsm")
Z = ("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
     "GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm")

TEILE = ["[Content_Types].xml", "xl/_rels/workbook.xml.rels", "xl/workbook.xml",
         "_rels/.rels", "docProps/app.xml"]


def haeufig(s):
    """XML auf eine Zeile pro Element bringt, damit der Diff lesbar wird."""
    s = re.sub(r"><", ">\n<", s)
    return [x for x in s.split("\n") if x.strip()]


with zipfile.ZipFile(Q) as a, zipfile.ZipFile(Z) as b:
    for teil in TEILE:
        if teil not in a.namelist() or teil not in b.namelist():
            print(f"### {teil}: fehlt (Q:{teil in a.namelist()} Z:{teil in b.namelist()})")
            continue
        alt = haeufig(a.read(teil).decode("utf-8"))
        neu = haeufig(b.read(teil).decode("utf-8"))
        print(f"### {teil}   Zeilen {len(alt)} -> {len(neu)}")
        for zeile in difflib.unified_diff(alt, neu, "Quelle", "Ziel", n=0, lineterm=""):
            if zeile.startswith(("---", "+++", "@@")):
                continue
            print("   ", zeile[:210])
        print()
