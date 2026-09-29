#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""B1b zerlegen: was an den angehaengten Helferzellen stoert Excel?

B1a (nur M-Zellen ersetzen) ist sauber, B1b (nur Helfer anhaengen) nicht.
Diese Serie haengt Zellen mit steigendem Umfang an - jede Datei ein Aspekt:

  E1  1 Zelle BP als Konstante        (kleinstmoegliche Aenderung)
  E2  1 Zelle BP als Formel
  E3  nur die leere Zelle BX
  E4  alle Helfer als Konstanten      (ohne Formeln)
  E5  alle Helfer als Formeln         (= B1b, Kontrolle)

Die erste kaputte Datei benennt die Ursache:
  E1 kaputt -> das Anhaengen selbst (spans/dimension/Zellreihenfolge)
  E2 kaputt -> die Formel in der Zelle
  E3 kaputt -> eine leere Zelle <c r=".."/>
  E4 kaputt -> Zellstruktur/Stil; E5 kaputt -> Formelinhalte
"""
import pathlib
import re
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import baut_arbeitsmappe as ba                                    # noqa: E402

ZIEL = ba.DOCS / "_testbausteine_b1b"


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


def zellen_fuer(modus, r, fmt, spalten):
    """Liefert die anzuhängenden Zellen (Spaltennummer, XML) für einen Modus."""
    if modus == "nur_bp_konst":
        return [(ba.SP["BP"], '<c r="BP%d"><v>1</v></c>' % r)]
    if modus == "nur_bp_formel":
        muster = ba.HELFER[0][2]
        return [(ba.SP["BP"], ba.zelle_formel(f"BP{r}", muster.format(**fmt)))]
    if modus == "nur_leer":
        return [(ba.col_index(ba.SP_MANUELL), ba.zelle_leer(f"{ba.SP_MANUELL}{r}"))]
    if modus == "alle_konstanten":
        return [(s, '<c r="%s%d"><v>1</v></c>' % (ba.spalte_liste(s), r)) for s in spalten]
    # alle_formeln
    aus = []
    for spalte, _t, muster in ba.HELFER:
        aus.append((spalte, ba.zelle_formel(f"{ba.spalte_liste(spalte)}{r}",
                                            muster.format(**fmt))))
    aus.append((ba.col_index(ba.SP_MANUELL), ba.zelle_leer(f"{ba.SP_MANUELL}{r}")))
    return aus


def variante(name, modus, filter=None):
    teile, rei = basis()
    blatt = ba.finde_blatt(teile, ba.BLATT)
    xml = teile[blatt].decode("utf-8")
    spalten = [s for s, _t, _m in ba.HELFER]

    if filter == "weg":
        xml = re.sub(r'<autoFilter.*?</autoFilter>', "", xml, flags=re.S)

    def zeile(m):
        rnr = int(m.group(1))
        if not (ba.ERSTE <= rnr <= ba.LETZTE):
            return m.group(0)
        inhalt = m.group(3)
        fmt = dict(r=rnr, e=ba.ERSTE, l=ba.LETZTE)
        neu = zellen_fuer(modus, rnr, fmt, spalten)
        zusatz = "".join(x for _c, x in sorted(neu, key=lambda kv: kv[0]))
        sp = [ba.col_index(x) for x in re.findall(r'<c r="([A-Z]+)\d+"', inhalt)]
        sp += [c for c, _x in neu]
        attr = re.sub(r'\sspans="[^"]*"', "", m.group(2))
        if sp:
            attr += f' spans="1:{max(sp)}"'
        return f'<row r="{rnr}"{attr}>{inhalt}{zusatz}</row>'

    xml = re.sub(r'<row r="(\d+)"([^>]*)>(.*?)</row>', zeile, xml, flags=re.S)

    hoechste = max([66] + [s for s, _t, _m in ba.HELFER])
    letzte_sp = ba.spalte_liste(hoechste)
    # Zeile 773 liegt AUSSERHALB des AutoFilters (der endet bei 772)
    letzte_zeile = 772 if filter in ("bis_772", "bis_772_ce") else ba.LETZTE
    if filter in ("ce", "bis_772_ce"):
        xml = re.sub(r'autoFilter ref="A1:BN\d+"', f'autoFilter ref="A1:{letzte_sp}{letzte_zeile}"', xml)
        xml = re.sub(r'sortState ref="A2:BN\d+"', f'sortState ref="A2:{letzte_sp}{letzte_zeile}"', xml)
    xml = re.sub(r'<dimension ref="A1:[A-Z]+\d+"/>',
                 f'<dimension ref="A1:{letzte_sp}{letzte_zeile}"/>', xml, count=1)
    teile[blatt] = xml.encode("utf-8")

    pfad = ZIEL / name
    with zipfile.ZipFile(pfad, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in rei:
            if n in teile:
                zout.writestr(n, teile[n])
    return pfad


def main():
    ZIEL.mkdir(exist_ok=True)
    liste = [("E1_BP-als-Konstante.xlsm", "nur_bp_konst", None),
             ("E2_BP-als-Formel.xlsm", "nur_bp_formel", None),
             ("E3_nur-leere-Zelle.xlsm", "nur_leer", None),
             ("E4_alle-als-Konstanten.xlsm", "alle_konstanten", None),
             ("E5_alle-als-Formeln.xlsm", "alle_formeln", None),
             ("E6_Formeln-filter-auf-CE.xlsm", "alle_formeln", "ce"),
             ("E7_Formeln-ohne-AutoFilter.xlsm", "alle_formeln", "weg"),
             ("E8_Formeln-filter-CE-und-772.xlsm", "alle_formeln", "bis_772_ce")]
    gebaut = [variante(n, m, f) for n, m, f in liste]
    print("Testserie in", ZIEL)
    for p in gebaut:
        print("  ", p.name, p.stat().st_size, "Bytes")
    print()
    print("Bitte der Reihenfolge nach oeffnen und die ERSTE kaputte melden. NICHT speichern.")
    print("  E1/E2 kaputt -> das Anhaengen selbst bzw. die Formel")
    print("  E3 kaputt    -> leere Zelle <c r=\"..\"/>")
    print("  E4 sauber, E5 kaputt -> Formelinhalte")
    print("  E6/E7/E8 sauber, E5 kaputt -> AutoFilter/Sortierbereich ist die Ursache")


if __name__ == "__main__":
    main()
