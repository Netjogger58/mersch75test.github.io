#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Erzeugt eine Testserie, die den Grund der Excel-Reparatur eingrenzt.

Ausgangspunkt ist TEST1_nur-calcchain.xlsm, das nachweislich ohne Meldung
oeffnet. Jede Datei aendert GENAU EINEN der Schritte des Bausatzes:

  B0  nur calcChain entfernt                  (Kontrolle - bekannt gut)
  B1  + Blatt 1 geaendert (M, Helfer, Kopf)   -> ist die Werkzeugblatte schuld?
  B2  + neues Blatt "Cotisation"              -> ist das neue Blatt schuld?
  B3  + nur docProps/app.xml angepasst         -> ist app.xml schuld?
  B4  + nur workbook.xml fullCalcOnLoad        -> ist calcPr schuld?

Die erste Datei, bei der Excel die Reparatur-Meldung zeigt, benennt die
schuldige Aenderung.
"""
import pathlib
import re
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import baut_arbeitsmappe as ba                                    # noqa: E402

ZIEL = ba.DOCS / "_testbausteine"


def schreibe(name, teile, reihenfolge):
    pfad = ZIEL / name
    with zipfile.ZipFile(pfad, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in reihenfolge:
            if n in teile:
                zout.writestr(n, teile[n])
    return pfad


def basis():
    """TEST1 minus calcChain - dieser Stand oeffnet nachweislich sauber."""
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


def mit_blatt1(teile):
    blatt = ba.finde_blatt(teile, ba.BLATT)
    werte = ba.rechne_werte(teile, blatt)
    xml, _ = ba.baue_membres_sheet(teile[blatt].decode("utf-8"), werte)
    teile[blatt] = xml.encode("utf-8")


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
    rels = teile["xl/_rels/workbook.xml.rels"].decode("utf-8")
    rels = rels.replace("</Relationships>",
                        f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/'
                        f'officeDocument/2006/relationships/worksheet" '
                        f'Target="worksheets/{config.split("/")[-1]}"/></Relationships>')
    teile["xl/_rels/workbook.xml.rels"] = rels.encode("utf-8")
    ct = teile["[Content_Types].xml"].decode("utf-8")
    ct = ct.replace("</Types>",
                    f'<Override PartName="/{config}" ContentType="application/vnd.'
                    f'openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>')
    teile["[Content_Types].xml"] = ct.encode("utf-8")
    return teile, rei




def mit_app(teile):
    app = teile["docProps/app.xml"].decode("utf-8")
    app = re.sub(r"(Arbeitsblätter</vt:lpstr></vt:variant><vt:variant><vt:i4>)(\d+)(</vt:i4>)",
                 lambda m: m.group(1) + str(int(m.group(2)) + 1) + m.group(3), app, count=1)
    app = re.sub(r'(<TitlesOfParts><vt:vector size=")(\d+)(")',
                 lambda m: m.group(1) + str(int(m.group(2)) + 1) + m.group(3), app, count=1)
    wb = teile["xl/workbook.xml"].decode("utf-8")
    blaetter = re.findall(r'<sheet name="([^"]+)"', wb)
    titel = re.findall(r"<vt:lpstr>([^<]*)</vt:lpstr>",
                       re.search(r"<TitlesOfParts>(.*?)</TitlesOfParts>", app, re.S).group(1))
    letztes = [t for t in titel if t in blaetter][-1]
    app = app.replace(f"<vt:lpstr>{letztes}</vt:lpstr>",
                      f"<vt:lpstr>{letztes}</vt:lpstr>"
                      f"<vt:lpstr>{ba.CONFIG_BLATT}</vt:lpstr>", 1)
    teile["docProps/app.xml"] = app.encode("utf-8")


def mit_calcpr(teile):
    wb = teile["xl/workbook.xml"].decode("utf-8")
    wb = re.sub(r"<calcPr([^>]*?)/>",
                lambda m: "<calcPr" + re.sub(r'\sfullCalcOnLoad="[^"]*"', "", m.group(1))
                + ' fullCalcOnLoad="1"/>', wb, count=1)
    teile["xl/workbook.xml"] = wb.encode("utf-8")


def main():
    ZIEL.mkdir(exist_ok=True)
    gebaut = []

    t, r = basis()
    gebaut.append(schreibe("B0_kontrolle.xlsm", t, r))

    t, r = basis()
    mit_blatt1(t)
    gebaut.append(schreibe("B1_nur-blatt1.xlsm", t, r))

    t, r = basis()
    t, r = mit_configblatt(t, r)
    gebaut.append(schreibe("B2_nur-configblatt.xlsm", t, r))

    t, r = basis()
    mit_app(t)
    gebaut.append(schreibe("B3_nur-app-xml.xlsm", t, r))

    t, r = basis()
    mit_calcpr(t)
    gebaut.append(schreibe("B4_nur-fullcalconload.xlsm", t, r))

    # B5 = der vollstaendige Bausatz. Muss die Meldung zeigen, die du bisher
    # bekommen hast. Taucht sie erst hier auf, liegt sie an der Kombination.
    t, r = basis()
    mit_blatt1(t)
    t, r = mit_configblatt(t, r)
    mit_app(t)
    mit_calcpr(t)
    gebaut.append(schreibe("B5_vollstaendig.xlsm", t, r))

    print("Testserie in", ZIEL)
    for p in gebaut:
        print("  ", p.name, p.stat().st_size, "Bytes")
    print()
    print("Bitte JEDE Datei in Excel oeffnen und melden, welche die Meldung")
    print("'Problem bei einigen Inhalten' zeigt. Die erste fehlerhafte Datei")
    print("benennt die Ursache:")
    print("  B1 kaputt -> Blatt 1 (Formeln/Stile/Zellen)")
    print("  B2 kaputt -> neues Blatt Cotisation (workbook/rels/Content_Types)")
    print("  B3 kaputt -> docProps/app.xml")
    print("  B4 kaputt -> fullCalcOnLoad")
    print("  nur B5 kaputt -> erst die Kombination")
    print("Reparierte Dateien bitte NICHT speichern.")


if __name__ == "__main__":
    main()
