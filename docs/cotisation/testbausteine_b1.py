#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unterspalten von B1: welcher TEIL der Blatt-1-Aenderung ist schuld?

B1 zeigt die Reparatur-Meldung, B0 (ohne Blatt-1-Aenderung) nicht.
Diese Serie spaltet B1 in seine drei Bestandteile auf:

  B1a  nur die Zellen M ersetzen        (kein Helfer, keine Kopfzellen)
  B1b  nur die Helfer BP:CE anhaengen   (M bleibt, Kopf bleibt)
  B1c  nur die Kopfzeile BP1:CE1        (M bleibt, Helfer fehlen)
  B1d  alles zusammen  = B1             (Kontrolle, muss die Meldung zeigen)

Erwartung: die erste kaputte Datei benennt die Ursache.
"""
import pathlib
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import baut_arbeitsmappe as ba                                    # noqa: E402

ZIEL = ba.DOCS / "_testbausteine_b1"


def basis():
    with zipfile.ZipFile(ba.QUELLE) as zin:
        teile = {n: zin.read(n) for n in zin.namelist()}
        rei = list(zin.namelist())
    teile.pop("xl/calcChain.xml", None)
    rei = [n for n in rei if n != "xl/calcChain.xml"]
    rels = teile["xl/_rels/workbook.xml.rels"].decode("utf-8")
    teile["xl/_rels/workbook.xml.rels"] = ba.re.sub(
        r'<Relationship[^>]*calcChain\.xml[^>]*/>', "", rels).encode("utf-8")
    ct = teile["[Content_Types].xml"].decode("utf-8")
    teile["[Content_Types].xml"] = ba.re.sub(
        r'<Override[^>]*calcChain\.xml[^>]*/>', "", ct).encode("utf-8")
    return teile, rei


def schreibe(name, teile, rei):
    pfad = ZIEL / name
    with zipfile.ZipFile(pfad, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in rei:
            if n in teile:
                zout.writestr(n, teile[n])
    return pfad


def variante(name, mit_m, mit_helper, mit_kopf):
    teile, rei = basis()
    blatt = ba.finde_blatt(teile, ba.BLATT)
    werte = ba.rechne_werte(teile, blatt)
    xml, _ = ba.baue_membres_sheet(teile[blatt].decode("utf-8"), werte,
                                   mit_m=mit_m, mit_helper=mit_helper,
                                   mit_kopf=mit_kopf)
    teile[blatt] = xml.encode("utf-8")
    return schreibe(name, teile, rei)


def main():
    ZIEL.mkdir(exist_ok=True)
    liste = [
        ("B1a_nur-M-Zellen.xlsm", True, False, False),
        ("B1b_nur-Helfer.xlsm", False, True, False),
        ("B1c_nur-Kopfzeile.xlsm", False, False, True),
        ("B1d_alles_B1.xlsm", True, True, True),
    ]
    gebaut = [variante(n, m, h, k) for n, m, h, k in liste]

    print("Testserie in", ZIEL)
    for p in gebaut:
        print("  ", p.name, p.stat().st_size, "Bytes")
    print()
    print("Bitte JEDE Datei oeffnen und sagen, welche die Reparatur-Meldung zeigt.")
    print("  B1a kaputt -> Ersatz der alten M-Formeln")
    print("  B1b kaputt -> die Helferspalten BP:CE")
    print("  B1c kaputt -> die Helfernamen in der Kopfzeile")
    print("  nur B1d kaputt -> erst die Kombination")
    print("Reparierte Dateien NICHT speichern.")


if __name__ == "__main__":
    main()
