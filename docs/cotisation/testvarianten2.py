#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
testvarianten2.py - grenzt den Fehler in den NEUEN Zellen ein.

TEST2a  nur Spalte L mit einer einfachen Formel, keine Helfer
TEST2b  L + Helfer, aber alle Helfer als Konstante 1 (keine Formeln)
TEST2c  L + Helfer wie geplant, aber mit rohen " statt &quot;

Blickrichtung:
  TEST2a warnt  -> das Ersetzen der L-Zelle selbst stoert
  TEST2b warnt -> die vielen neuen Zellen stoeren (Struktur/Sortierung)
  nur TEST2c/2b warnt -> es liegt an den Formeltexten bzw. am Escaping
"""
import pathlib
import re
import sys
import zipfile

sys.path.insert(0, "/Users/netjogger58/CascadeProjects/mersch75test.github.io/docs/cotisation")
import baut_arbeitsmappe as bau  # noqa: E402

D = pathlib.Path("/Users/netjogger58/CascadeProjects/Vereins-OS/docs")
Q = D / "GC 2026-09-24 MEMBERSLESCHT 2026-2027.xlsm"
EINFACH = 'IF($O{r}="","",IF($O{r}="XSEUL","300",""))'


def basis():
    with zipfile.ZipFile(Q) as zin:
        teile = {n: zin.read(n) for n in zin.namelist()}
        rei = [n for n in zin.namelist() if n != "xl/calcChain.xml"]
    teile.pop("xl/calcChain.xml", None)
    ct = re.sub(r'<Override[^>]*calcChain\.xml[^>]*/>', "",
                teile["[Content_Types].xml"].decode("utf-8"))
    teile["[Content_Types].xml"] = ct.encode("utf-8")
    rels = re.sub(r'<Relationship[^>]*calcChain\.xml[^>]*/>', "",
                  teile["xl/_rels/workbook.xml.rels"].decode("utf-8"))
    teile["xl/_rels/workbook.xml.rels"] = rels.encode("utf-8")
    return teile, rei


def rows_ohne_helfer(xml, l_formel):
    """Ersetzt nur die L-Zelle, laesst alle anderen Zellen unangetastet."""
    def repl(m):
        r = int(m.group(1))
        if not (bau.ERSTE <= r <= bau.LETZTE):
            return m.group(0)
        neu = re.sub(r'<c r="L%d"[^>]*?(?:/>|>.*?</c>)' % r, "", m.group(3), flags=re.S)
        zelle = f'<c r="L{r}"><f>{l_formel.format(r=r)}</f></c>'
        # L an der richtigen Stelle (Spalte 12) wieder einfuegen
        teile = CELL.finditer(neu)
        eingefuegt = False
        aus = []
        for c in teile:
            if not eingefuegt and bau.col_index(c.group(1)) > 12:
                aus.append(zelle)
                eingefuegt = True
            aus.append(c.group(0))
        if not eingefuegt:
            aus.append(zelle)
        return f'<row r="{r}"{m.group(2)}>' + "".join(aus) + "</row>"

    return re.sub(r'<row r="(\d+)"([^>]*)>(.*?)</row>', repl, xml, flags=re.S)


CELL = re.compile(r'<c r="([A-Z]+)\d+"[^>]*?(?:/>|>.*?</c>)', re.S)


def schreibe(ziel, teile, rei):
    if ziel.exists():
        ziel.unlink()
    with zipfile.ZipFile(ziel, "w", zipfile.ZIP_DEFLATED) as z:
        for n in rei:
            z.writestr(n, teile[n])
    print("geschrieben:", ziel.name)


def main():
    xml = zipfile.ZipFile(Q).read("xl/worksheets/sheet1.xml").decode("utf-8")

    # TEST2a: nur L, einfache Formel, keine Helfer
    t, r = basis()
    t["xl/worksheets/sheet1.xml"] = rows_ohne_helfer(xml, EINFACH).encode("utf-8")
    schreibe(D / "TEST2a_nur-L-einfach.xlsm", t, r)

    # TEST2b: L + Helfer als Konstanten
    t, r = basis()
    def mit_konstanten(m):
        rr = int(m.group(1))
        if not (bau.ERSTE <= rr <= bau.LETZTE):
            return m.group(0)
        neu = re.sub(r'<c r="L%d"[^>]*?(?:/>|>.*?</c>)' % rr, "", m.group(3), flags=re.S)
        neu = f'<c r="L{rr}"><f>{EINFACH.format(r=rr)}</f></c>'
        for spalte, _t, _m in bau.HELFER:
            neu += f'<c r="{bau.spalte_liste(spalte)}{rr}"><v>1</v></c>'
        aus, eingefuegt = [], False
        for c in CELL.finditer(neu):
            if not eingefuegt and bau.col_index(c.group(1)) > 12 and c.group(1) != "L":
                pass
            aus.append(c.group(0))
        # einsortieren
        paare = []
        for c in CELL.finditer(neu):
            paare.append((bau.col_index(c.group(1)), c.group(0)))
        paare.sort(key=lambda x: x[0])
        return f'<row r="{rr}"{m.group(2)}>' + "".join(x for _i, x in paare) + "</row>"

    t["xl/worksheets/sheet1.xml"] = re.sub(
        r'<row r="(\d+)"([^>]*)>(.*?)</row>', mit_konstanten, xml, flags=re.S).encode("utf-8")
    schreibe(D / "TEST2b_helfer-konstanten.xlsm", t, r)

    # TEST2c: volle Formeln, aber rohe Anfuehrungszeichen
    t, r = basis()
    neu, _ = bau.baue_membres_sheet(xml)
    neu = neu.replace("&quot;", '"')
    t["xl/worksheets/sheet1.xml"] = neu.encode("utf-8")
    schreibe(D / "TEST2c_roh-anfuehrungen.xlsm", t, r)


if __name__ == "__main__":
    main()
