#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
testvarianten.py - baut drei Testdateien, um die Excel-Warnung einzugrenzen.

V1: Original + calcChain entfernt            (kein Blatt angefasst)
V2: Original + Blatt1-Zeilen umgeschrieben  (kein neues Blatt)
V3: vollstaendig, also die aktuelle Datei

Die Datei, die Excel ohne Warnung oeffnet, zeigt die Ursache:
  V1 warnt -> das Original selbst ist betroffen
  V2 warnt -> das Umschreiben der Zeilen ist die Ursache
  nur V3 warnt -> das neue Blatt ist die Ursache
"""
import pathlib
import sys
import zipfile

sys.path.insert(0, "/Users/netjogger58/CascadeProjects/mersch75test.github.io/docs/cotisation")
import baut_arbeitsmappe as bau  # noqa: E402

D = pathlib.Path("/Users/netjogger58/CascadeProjects/Vereins-OS/docs")
Q = D / "GC 2026-09-24 MEMBERSLESCHT 2026-2027.xlsm"


def schreibe(ziel: pathlib.Path, teile, reihenfolge) -> None:
    if ziel.exists():
        ziel.unlink()
    with zipfile.ZipFile(ziel, "w", zipfile.ZIP_DEFLATED) as z:
        for n in reihenfolge:
            z.writestr(n, teile[n])


def main() -> int:
    with zipfile.ZipFile(Q) as zin:
        teile = {n: zin.read(n) for n in zin.namelist()}
        rei = list(zin.namelist())

    # --- V1: nur calcChain raus
    t1 = dict(teile)
    t1.pop("xl/calcChain.xml", None)
    r1 = [n for n in rei if n != "xl/calcChain.xml"]
    ct = t1["[Content_Types].xml"].decode("utf-8")
    import re
    ct = re.sub(r'<Override[^>]*calcChain\.xml[^>]*/>', "", ct)
    t1["[Content_Types].xml"] = ct.encode("utf-8")
    rels = t1["xl/_rels/workbook.xml.rels"].decode("utf-8")
    rels = re.sub(r'<Relationship[^>]*calcChain\.xml[^>]*/>', "", rels)
    t1["xl/_rels/workbook.xml.rels"] = rels.encode("utf-8")
    schreibe(D / "TEST1_nur-calcchain.xlsm", t1, r1)
    print("TEST1_nur-calcchain.xlsm        (Original, calcChain entfernt)")

    # --- V2: nur Blatt1 umschreiben, KEIN neues Blatt
    t2 = dict(teile)
    t2.pop("xl/calcChain.xml", None)
    r2 = [n for n in rei if n != "xl/calcChain.xml"]
    t2["[Content_Types].xml"] = ct.encode("utf-8")
    t2["xl/_rels/workbook.xml.rels"] = rels.encode("utf-8")
    neues, _ = bau.baue_membres_sheet(teile["xl/worksheets/sheet1.xml"].decode("utf-8"))
    t2["xl/worksheets/sheet1.xml"] = neues.encode("utf-8")
    wb2 = teile["xl/workbook.xml"].decode("utf-8")
    wb2 = re.sub(r"<calcPr([^>]*?)/>", lambda m: "<calcPr" + m.group(1) + ' fullCalcOnLoad="1"/>',
                 wb2, count=1)
    t2["xl/workbook.xml"] = wb2.encode("utf-8")
    schreibe(D / "TEST2_nur-blatt1.xlsm", t2, r2)
    print("TEST2_nur-blatt1.xlsm          (Original + Spalte L/Helfer, ohne neues Blatt)")

    print()
    print("TEST3 ist die aktuelle Datei: GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
