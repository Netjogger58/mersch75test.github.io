#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testserie I: Beseitigung des 2-Argument-DATEVALUE-Fehlers.

Befund:
  Excel DATEVALUE(date_text) akzeptiert laut OpenXML/Excel-Spezifikation genau 1 Argument.
  In BQ stand: DATEVALUE($J{r},"DD.MM.YYYY") -> 2 Argumente (Syntaxfehler beim Laden!)
  In CC stand: DATEVALUE($J{r},"DD.MM.YYYY") und DATEVALUE(Cotisation!$B$11,"DD.MM.YYYY") -> 2 Argumente!
  Genau deshalb meldeten BEIDE Gruppen H1 (enthält BQ) und H2 (enthält CC) Reparatur!

Diese Serie baut:
  I1_Gruppe-A_korrigiert.xlsm   (Gruppe A mit 1-Arg DATEVALUE)
  I2_Gruppe-B_korrigiert.xlsm   (Gruppe B mit 1-Arg DATEVALUE)
  I3_alle_korrigiert.xlsm       (alle 14 Helfer korrigiert)
  I4_nur-BQ-korrigiert.xlsm     (nur BP + BQ korrigiert)
  I5_nur-CC-korrigiert.xlsm     (nur BP + CC korrigiert)
"""
import pathlib
import re
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import baut_arbeitsmappe as ba                                    # noqa: E402
import testbausteine_h as th                                      # noqa: E402

ZIEL = ba.DOCS / "_testbausteine_i"


def korrigiere_formel(muster: str) -> str:
    m = muster.replace('DATEVALUE($J{r},"DD.MM.YYYY")', 'DATEVALUE($J{r})')
    m = m.replace('DATEVALUE(Cotisation!$B$11,"DD.MM.YYYY")', 'DATEVALUE(Cotisation!$B$11)')
    return m


def variante_i(name, spalten):
    teile, rei = th.basis()
    teile, rei = th.mit_configblatt(teile, rei)
    blatt = ba.finde_blatt(teile, ba.BLATT)
    xml = teile[blatt].decode("utf-8")

    helfer_korr = []
    for s, name_titel, f in ba.HELFER:
        helfer_korr.append((s, name_titel, korrigiere_formel(f)))

    gewaehlt = [h for h in helfer_korr if ba.spalte_liste(h[0]) in (["BP"] + spalten)]

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
    liste = [
        ("I1_Gruppe-A_korrigiert.xlsm", th.GRUPPE_A),
        ("I2_Gruppe-B_korrigiert.xlsm", th.GRUPPE_B),
        ("I3_alle_korrigiert.xlsm", th.GRUPPE_A + th.GRUPPE_B),
        ("I4_nur-BQ-korrigiert.xlsm", ["BQ"]),
        ("I5_nur-CC-korrigiert.xlsm", ["CC"]),
    ]
    print(f"Erzeuge Testserie I in {ZIEL}")
    for name, spalten in liste:
        p = variante_i(name, spalten)
        print(f"   {p.name:32s} {p.stat().st_size:8d} Bytes")


if __name__ == "__main__":
    main()
