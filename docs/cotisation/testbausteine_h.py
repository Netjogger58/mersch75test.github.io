#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Welche Helferformel ist ungueltig? Bisektion mit vorhandenem Cotisation-Blatt.

Aus den bisherigen Tests:
  E1 (1 Konstante)            sauber
  E2 (1 Formel BP)            nur VERKNUEPFUNGS-Warnung (Blatt fehlt) - keine Reparatur
  E3 (leere Zelle)            sauber
  E4 (alle als Konstanten)    sauber
  E5-E8 (alle als Formeln)    REPARATUR  (auch ohne AutoFilter)
=> Eine einzelne Formel ist in Ordnung, mindestens eine der 14 ist ungueltig.
=> Und: die Verknuepfungs-Warnung kommt vom fehlenden Blatt "Cotisation".

Deshalb enthalten ALLE Dateien dieser Serie das Blatt "Cotisation". Dann ist
jede Reparatur-Meldung eindeutig ein Formelfehler:

  H0  nur BP                          (muss sauber sein)
  H1  BP + BQ,BR,BS,BT,BU,BV,BW       (Gruppe A: ohne Cotisation-Bezug)
  H2  BP + BY,BZ,CA,CB,CC,CD          (Gruppe B: mit Cotisation-Bezug)
  H3  alle 14                         (Kontrolle - muss die Meldung zeigen)
"""
import pathlib
import re
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import baut_arbeitsmappe as ba                                    # noqa: E402

ZIEL = ba.DOCS / "_testbausteine_h"

GRUPPE_A = ["BQ", "BR", "BS", "BT", "BU", "BV", "BW"]
GRUPPE_B = ["BY", "BZ", "CA", "CB", "CC", "CD"]


def basis():
    with zipfile.ZipFile(ba.QUELLE) as zin:
        teile = {n: zin.read(n) for n in zin.namelist()}
        rei = list(zin.namelist())
    teile.pop("xl/calcChain.xml", None)
    rei = [n for n in rei if n != "xl/calcChain.xml"]
    rels = teile["xl/_rels/workbook.xml.rels"].decode("utf-8")
    teile["xl/_rels/workbook.xml.rels"] = re.sub(
        r'<Relationship[^>]*calcChain\.xml[^>]*/>', "", rels).encode("utf-8")
    ct = teile["[Content_Types].xml"].decode("utf-8")
    teile["[Content_Types].xml"] = re.sub(
        r'<Override[^>]*calcChain\.xml[^>]*/>', "", ct).encode("utf-8")
    return teile, rei


def mit_configblatt(teile, rei):
    vorhanden = [int(m.group(1)) for m in
                 (re.match(r"xl/worksheets/sheet(\d+)\.xml$", n) for n in teile) if m]
    config = f"xl/worksheets/sheet{max(vorhanden) + 1}.xml"
    teile[config] = ba.baue_config_sheet().encode("utf-8")
    rei = rei + [config]
    rid = "rIdCotisation"
    wb = teile["xl/workbook.xml"].decode("utf-8")
    ids = [int(x) for x in re.findall(r'sheetId="(\d+)"', wb)] or [0]
    wb = wb.replace("</sheets>",
                    f'<sheet name="{ba.CONFIG_BLATT}" sheetId="{max(ids) + 1}" '
                    f'r:id="{rid}"/></sheets>')
    teile["xl/workbook.xml"] = wb.encode("utf-8")
    regs = teile["xl/_rels/workbook.xml.rels"].decode("utf-8")
    regs = regs.replace("</Relationships>",
                        f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/'
                        f'officeDocument/2006/relationships/worksheet" '
                        f'Target="worksheets/{config.split("/")[-1]}"/></Relationships>')
    teile["xl/_rels/workbook.xml.rels"] = regs.encode("utf-8")
    ct = teile["[Content_Types].xml"].decode("utf-8")
    ct = ct.replace("</Types>",
                    f'<Override PartName="/{config}" ContentType="application/vnd.'
                    f'openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>')
    teile["[Content_Types].xml"] = ct.encode("utf-8")
    return teile, rei


def variante(name, spalten):
    teile, rei = basis()
    teile, rei = mit_configblatt(teile, rei)
    blatt = ba.finde_blatt(teile, ba.BLATT)
    xml = teile[blatt].decode("utf-8")
    gewaehlt = [h for h in ba.HELFER if ba.spalte_liste(h[0]) in (["BP"] + spalten)]

    def zeile(m):
        rnr = int(m.group(1))
        if not (ba.ERSTE <= rnr <= ba.LETZTE):
            return m.group(0)
        inhalt = m.group(3)
        fmt = dict(r=rnr, e=ba.ERSTE, l=ba.LETZTE)
        neu = [(s, ba.zelle_formel(f"{ba.spalte_liste(s)}{rnr}", muster.format(**fmt)))
               for s, _t, muster in gewaehlt]
        zusatz = "".join(x for _c, x in sorted(neu, key=lambda kv: kv[0]))
        sp = [ba.col_index(x) for x in re.findall(r'<c r="([A-Z]+)\d+"', inhalt)]
        sp += [c for c, _x in neu]
        attr = re.sub(r'\sspans="[^"]*"', "", m.group(2))
        if sp:
            attr += f' spans="1:{max(sp)}"'
        return f'<row r="{rnr}"{attr}>{inhalt}{zusatz}</row>'

    xml = re.sub(r'<row r="(\d+)"([^>]*)>(.*?)</row>', zeile, xml, flags=re.S)
    hoechste = max([66] + [s for s, _t, _m in gewaehlt])
    xml = re.sub(r'<dimension ref="A1:[A-Z]+\d+"/>',
                 f'<dimension ref="A1:{ba.spalte_liste(hoechste)}{ba.LETZTE}"/>', xml, count=1)
    teile[blatt] = xml.encode("utf-8")

    pfad = ZIEL / name
    with zipfile.ZipFile(pfad, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in rei:
            if n in teile:
                zout.writestr(n, teile[n])
    return pfad


def main():
    ZIEL.mkdir(exist_ok=True)
    liste = [("H0_nur-BP.xlsm", []),
             ("H1_Gruppe-A.xlsm", GRUPPE_A),
             ("H2_Gruppe-B.xlsm", GRUPPE_B),
             ("H3_alle.xlsm", GRUPPE_A + GRUPPE_B)]
    gebaut = [variante(n, s) for n, s in liste]
    print("Testserie in", ZIEL)
    for p in gebaut:
        print("  ", p.name, p.stat().st_size, "Bytes")
    print()
    print("Alle enthalten das Blatt Cotisation, damit keine Verknuepfungs-Warnung")
    print("mehr auftritt. Die ERSTE Datei mit Reparatur-Meldung benennt die Gruppe.")


if __name__ == "__main__":
    main()
