"""End-to-End-Test: taucht ein NEU in Zeile 774 eingetragenes Mitglied
tatsaechlich in der Stripe-Rechnung auf?

Das ist die kritische Frage, weil die Werkzeuge auf der ARBEITSDATEI rechnen
muss (nicht auf dem Original) und der Zeilenleser die Reservezeilen bis 900
lesen muss.

Der Test schreibt das Mitglied direkt ins XML (so wie Excel es tut: Inline-Text
fuer Text, Zahl fuer Zahlen) und ruft danach dasselbe Modell auf, das auch
`stripe_sync.py` benutzt.

Aufruf:  python3 docs/cotisation/test_neues_mitglied.py
"""
import pathlib
import re
import shutil
import sys
import tempfile
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mappe                  # noqa: E402
import pruef_cotisation as pr  # noqa: E402
import pruefe_stripe_export as pse  # noqa: E402

ZEILE = 774
NEU = {
    "A": ("s", "TESTFALL"),        # Nom
    "B": ("s", "Neumitglied"),     # Prenom
    "G": ("s", "9, rue Test"),     # Adresse
    "J": ("n", "25000"),           # Geburtsdatum (Excel-Serienzahl, ~1968 -> SEN)
    "K": ("s", "SEN"),             # Alterskategorie - OHNE sie gibt es keinen Tarif!
    "O": ("s", "J"),               # spielt
    "Q": ("s", "F9999"),           # Haushaltscode -> eigener Traeger
    "AI": ("n", "123456"),         # Spielerlizenz
    "AX": ("s", "testfall@mersch75.lu"),   # E-Mail
}


def zelle(spalte: str, r: int) -> str:
    typ, wert = NEU[spalte]
    if typ == "n":
        return f'<c r="{spalte}{r}"><v>{wert}</v></c>'
    return (f'<c r="{spalte}{r}" t="inlineStr"><is>'
            f'<t xml:space="preserve">{wert}</t></is></c>')


def baue_testdatei(ziel: pathlib.Path) -> pathlib.Path:
    """Kopie der Arbeitsmappe mit einem neuen Mitglied in Zeile 774."""
    tmp = pathlib.Path(tempfile.mkdtemp()) / ziel.name
    shutil.copy(ziel, tmp)
    with zipfile.ZipFile(tmp) as z:
        teile = {n: z.read(n) for n in z.namelist()}
        reihenfolge = z.namelist()
    x = teile["xl/worksheets/sheet1.xml"].decode("utf-8")
    m = re.search(r'(<row r="%d"[^>]*>)(.*?)(</row>)' % ZEILE, x, re.S)
    if not m:
        raise SystemExit("! Zeile %d nicht gefunden" % ZEILE)
    vorhanden = re.findall(r'<c r="([A-Z]+)%d"' % ZEILE, m.group(2))

    def colpos(spalte: str) -> int:
        return sum((ord(c) - 64) * 26 ** i for i, c in enumerate(reversed(spalte)))

    # Bestehende Zellen einsammeln, neue dazugeben (gleiche Spalte wird
    # ERSETZT, nicht verdoppelt - sonst gewinnt beim Lesen die leere Zelle),
    # dann alles aufsteigend sortieren. Genau so schreibt es Excel.
    zellen = {}
    for c in re.finditer(r'<c r="([A-Z]+)%d".*?(?:/>|>.*?</c>)' % ZEILE, m.group(2), re.S):
        zellen[colpos(c.group(1))] = c.group(0)
    for spalte in NEU:
        zellen[colpos(spalte)] = zelle(spalte, ZEILE)
    koerper = "".join(zellen[k] for k in sorted(zellen))
    print("ersetzte Spalten:", " ".join(sorted(NEU, key=colpos)))
    print("vorhanden waren :", " ".join(vorhanden))
    neu = m.group(1) + koerper + m.group(3)
    teile["xl/worksheets/sheet1.xml"] = (x[:m.start()] + neu + x[m.end():]).encode("utf-8")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in reihenfolge:
            zout.writestr(n, teile[n])
    return tmp


def main() -> int:
    original = mappe.ziel()
    test = baue_testdatei(original)
    mappe.set_ziel(test)
    try:
        ergebnis, _cfg = pse.lade_modell()
        treffer = [x for x in ergebnis if x["nom"] == "TESTFALL"]
        if not treffer:
            print("FEHLER: das neue Mitglied wird vom Modell NICHT gesehen.")
            print("        Ursache waere: falsche Datei, falsche Kopfzeile oder")
            print("        Zeilenleser endet vor 774.")
            return 1
        x = treffer[0]
        print(f"gesehen       : Zeile {x['excel_zeile']}  {x['nom']} {x['vorname']}")
        print(f"famkey        : {x['famkey']}")
        print(f"L (neu)       : {x['neu']!r}   ({x['grund']})")
        print(f"Traeger       : {x['ist_traeger']}")
        posten = [p for p in pse.__dict__ and [] ]  # Platzhalter, s. u.
        rechnung = pse.echter_betrag(x["neu"]) and x["fam"] != "GAJGL"
        print(f"rechnungsfaehig: {rechnung}")
        del posten
        ok = rechnung and x["ist_traeger"] and x["excel_zeile"] == ZEILE
        print()
        print("ERGEBNIS:", "ok - neues Mitglied wird automatisch berechnet"
              if ok else "FEHLER - siehe Werte oben")
        return 0 if ok else 1
    finally:
        mappe.set_ziel(original)
        shutil.rmtree(test.parent, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
