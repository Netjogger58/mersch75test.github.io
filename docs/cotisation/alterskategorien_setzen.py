"""Schreibt die Alterskategorie-Formeln in die Spalten Z..AM.

Warum ueberhaupt: in der Mappe standen bereits Formeln der Art
    =IF(AND(Q2="", J2>=2010, J2<=2011, C2="M"), "x", "")
Die zwei Fehler darin:
  1. J2>=2010 vergleicht ein DATUM (Excel-Serienzahl ~43000) mit der Zahl
     2010 -> J2<=2011 ist bei jedem echten Datum FALSCH, also kam nie ein
     "x" heraus.
  2. Q2="" verlangt einen LEEREN Haushaltscode. Q ist aber "Code Courrier
     neu" und bei 608 von 900 Zeilen gefuellt (F-Codes, XSEUL, GAJGL)
     -> auch damit kein "x".

Neu: YEAR() statt direktem Vergleich, IFERROR fuer "///"- und Textzeilen,
H/F-Trennung ueber Spalte C (Sexe) - so wie es schon angelegt war.

Spalte Q ("Code Courrier neu") wird NICHT mehr ausgewertet: sie enthaelt
neben GAJGL auch F-Codes und XSEUL, und der Wunsch war ausdruecklich, die
GAJGL-Regel fallen zu lassen. Damit bleiben alle 195 Jugendlichen aktiv.

  --variante 1  Q2<>""        (Q muss leer sein)                -> 0 x
  --variante 2  Q2<>"GAJGL"   (nur GAJGL-Zeilen ueberspringen)   -> 180 x
  --variante 3  keine Q-Bedingung                                -> 195 x

Aufruf:  python3 docs/cotisation/alterskategorien_setzen.py --variante 3 --apply
"""
import pathlib
import re
import shutil
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mappe  # noqa: E402

SHEET = "xl/worksheets/sheet1.xml"
ERSTE, LETZTE = 2, 900

# (Spalte, Jahr von, Jahr bis, Geschlecht in Spalte C)
SPALTEN = [
    ("Z", 2010, 2011, "M"), ("AA", 2010, 2011, "F"),
    ("AB", 2012, 2013, "M"), ("AC", 2012, 2013, "F"),
    ("AD", 2014, 2015, "M"), ("AE", 2014, 2015, "F"),
    ("AF", 2016, 2017, "M"), ("AG", 2016, 2017, "F"),
    ("AH", 2018, 2019, "M"), ("AI", 2018, 2019, "F"),
    ("AJ", 2020, 2022, "M"), ("AK", 2020, 2022, "F"),
    ("AL", 2023, 2024, "M"), ("AM", 2023, 2024, "F"),
]

# WICHTIG: In der XLSX-Datei werden Formeln IMMER englisch und mit Komma
# gespeichert - das ist Dateiformat, keine Benutzereinstellung. Ein deutsches
# Excel 365 uebersetzt beim Oeffnen automatisch nach WENN/UND/JAHR/... und
# Semikolon. Deutsche Namen in die Datei zu schreiben ergaebe #NAME?.
JAHR = "IFERROR(YEAR($J{r}),IFERROR(VALUE(LEFT($J{r},4)),0))"

ERSETZUNG = [("IFERROR", "WENNFEHLER"), ("YEAR", "JAHR"), ("VALUE", "WERT"),
             ("LEFT", "LINKS"), ("AND", "UND"), ("IF", "WENN")]


def nach_de(f: str) -> str:
    """Nur zur Anzeige/Erlaeuterung - wird nicht in die Datei geschrieben."""
    import re as _re
    for en, de in ERSETZUNG:
        f = _re.sub(rf"\b{en}\(", f"{de}(", f)
    return f.replace(",", ";")


def formel(r: int, lo: int, hi: int, sex: str, variante: int) -> str:
    jahr = f"{JAHR.format(r=r)}>={lo},{JAHR.format(r=r)}<={hi}"
    if variante == 3:                       # GAJGL-Regel faellt komplett weg
        return f'IF(AND({jahr},$C{r}="{sex}"),"x","")'
    sperre = '$Q{r}<>""' if variante == 1 else '$Q{r}<>"GAJGL"'
    return f'IF({sperre.format(r=r)},"",IF(AND({jahr},$C{r}="{sex}"),"x",""))'


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def colpos(sp: str) -> int:
    """Zellenbezug -> Spaltennummer. Ziffern werden ignoriert, sonst
    liefert colpos("Z776") statt 26 die Zahl 667 - und dann faellt jede
    Zelle aus der Schleife, die eine Zelle anlegen soll."""
    n = 0
    for c in sp:
        if c.isalpha():
            n = n * 26 + (ord(c.upper()) - 64)
    return n


def zellen_reihenfolge_ok(x: str) -> list[str]:
    """Zeilen, deren Zellen nicht aufsteigend nach Spalte sortiert sind.
    Excel verweigert solche Dateien mit dem Reparatur-Dialog."""
    kaputt = []
    for m in re.finditer(r'<row r="(\d+)"[^>]*>(.*?)</row>', x, re.S):
        refs = [c.group(1) for c in
                re.finditer(r'<c r="([A-Z]+)\d+"', m.group(2))]
        if refs != sorted(refs, key=colpos):
            kaputt.append(m.group(1))
    return kaputt


def partner(sp: str) -> str:
    """Z<->AA, AB<->AC ... die zweite Spalte eines Bereichs."""
    i = [s for s, *_ in SPALTEN].index(sp)
    return SPALTEN[i ^ 1][0]


def geteilte_formeln(x: str) -> tuple[set, set]:
    """Gibt (si-Gruppen mit Master, si-Gruppen der Follower) zurueck.

    Wird eine Master-Zelle entfernt, zeigen alle zugehoerigen Follower
    ins Leere und Excel repariert die Datei - daher diese Kontrolle.
    """
    master, follower = set(), set()
    for m in re.finditer(r"<c r=\"[A-Z]+\d+\"[^>]*>(.*?)</c>", x, re.S):
        f = re.search(r"<f([^>]*?)(?:/>|>(.*?)</f>)", m.group(1), re.S)
        if not f or 't="shared"' not in f.group(1):
            continue
        si = re.search(r'si="(\d+)"', f.group(1))
        if not si:
            continue
        if re.search(r'ref="', f.group(1)):
            master.add(si.group(1))
        else:
            follower.add(si.group(1))
    return master, follower


def zellen_doppelt(x: str) -> list[str]:
    """Zellen, die zweimal in derselben Zeile stehen - Excel meldet das
    ebenfalls als 'Problem bei einigen Inhalten'."""
    doppelt = []
    for m in re.finditer(r'<row r="(\d+)"[^>]*>(.*?)</row>', x, re.S):
        refs = [c.group(0) for c in
                re.finditer(r'<c r="[A-Z]+\d+"', m.group(2))]
        if len(refs) != len(set(refs)):
            doppelt.append(m.group(1))
    return doppelt


def zelle_einfuegen(inhalt: str, ref: str, xml: str) -> str:
    """Fehlende Zelle an der richtigen Stelle (nach Spaltenindex) einhaengen."""
    ziel = colpos(ref)
    for m in re.finditer(r'<c r="([A-Z]+)\d+"', inhalt):
        if colpos(m.group(1)) > ziel:
            return inhalt[:m.start()] + xml + inhalt[m.start():]
    return inhalt + xml


def main() -> int:
    variante = 3
    if "--variante" in sys.argv:
        variante = int(sys.argv[sys.argv.index("--variante") + 1])
    if "--datei" in sys.argv:
        pfad = mappe.set_ziel(sys.argv[sys.argv.index("--datei") + 1])
    else:
        pfad = mappe.ziel()
    von = (int(sys.argv[sys.argv.index("--zeilen-von") + 1])
           if "--zeilen-von" in sys.argv else ERSTE)
    bis = (int(sys.argv[sys.argv.index("--zeilen-bis") + 1])
           if "--zeilen-bis" in sys.argv else LETZTE)
    raeume = (int(sys.argv[sys.argv.index("--raeume-ab") + 1])
              if "--raeume-ab" in sys.argv else None)
    label = {1: "Q muss leer sein", 2: "nur GAJGL raus",
             3: "keine Q-Bedingung (GAJGL-Regel faellt weg)"}[variante]
    print(f"Datei: {pfad.name}   Variante {variante} ({label})")
    print(f"Formeln in Zeile(n) {von}-{bis}"
          + (f", Zellen ab Zeile {raeume} werden geleert" if raeume else ""))

    with zipfile.ZipFile(pfad) as z:
        infos = z.infolist()
        teile = {i.filename: z.read(i.filename) for i in infos}
    x = teile[SHEET].decode("utf-8")

    vorhanden = {int(m.group(1)) for m in re.finditer(r'<row r="(\d+)"', x)}
    fehlend = [r for r in range(ERSTE, LETZTE + 1) if r not in vorhanden]
    if fehlend:
        print(f"ABBRUCH: {len(fehlend)} Zeilen fehlen (z. B. {fehlend[:5]}) - "
              f"dort kann keine Formel stehen.")
        return 1

    if "--apply" not in sys.argv:
        print("\nProben (Zeile 2), so steht es in der Datei:")
        for sp, lo, hi, sex in SPALTEN[:2] + SPALTEN[-1:]:
            print(f"   {sp:<3} ={formel(2, lo, hi, sex, variante)}")
        print("\nSo zeigt es deutsches Excel 365 an:")
        for sp, lo, hi, sex in SPALTEN[:2] + SPALTEN[-1:]:
            print(f"   {sp:<3} ={nach_de(formel(2, lo, hi, sex, variante))}")
        print("\nNichts geschrieben. Mit --apply wirklich setzen.")
        return 0

    ersetzt = angelegt = geleert = 0

    def zeile_repl(m):
        nonlocal ersetzt, angelegt, geleert
        r = int(m.group(2))
        if r < 1:                              # Zeile 0 gibt es nicht
            return m.group(0)
        raeumen_ab = raeume is not None and r >= raeume
        if not (raeumen_ab or von <= r <= bis):
            return m.group(0)                  # Kopfzeile & Fremdzeilen unangetastet
        neu = m.group(3)
        for sp, lo, hi, sex in SPALTEN:
            alt = re.search(r'<c r="%s%d"([^>]*?)(?:/>|>.*?</c>)' % (sp, r),
                            neu, re.S)
            if raeumen_ab:                     # Formel entfernen, Zelle bleibt
                if not alt:
                    continue
                attr = re.sub(r'\s*(r|t)="[^"]*"', "", alt.group(1)).strip()
                zelle = f'<c r="{sp}{r}"{(" " + attr) if attr else ""}/>'
                neu = neu[:alt.start()] + zelle + neu[alt.end():]
                geleert += 1
                continue
            f = formel(r, lo, hi, sex, variante)
            if alt:
                attr = re.sub(r'\s*r="[^"]*"', "", alt.group(1)).strip()
                attr = re.sub(r'\s*t="[^"]*"', "", attr)
                zelle = (f'<c r="{sp}{r}"{(" " + attr) if attr else ""}>'
                         f'<f>{esc(f)}</f></c>')
                neu = neu[:alt.start()] + zelle + neu[alt.end():]
                ersetzt += 1
            else:
                # Zelle fehlt in der Zeile -> mit dem Stil der
                # Partner-Spalte (H/F) neu anlegen
                vor = re.search(r'<c r="%s%d"([^>]*?)(?:/>|>.*?</c>)'
                                % (partner(sp), r), neu, re.S)
                attr = ""
                if vor:
                    attr = re.sub(r'\s*(r|t)="[^"]*"', "", vor.group(1)).strip()
                zelle = (f'<c r="{sp}{r}"{(" " + attr) if attr else ""}>'
                         f'<f>{esc(f)}</f></c>')
                neu = zelle_einfuegen(neu, f"{sp}{r}", zelle)
                angelegt += 1
        return m.group(1) + neu + m.group(4)

    neu_x = re.sub(r'(<row r="(\d+)"[^>]*>)(.*?)(</row>)', zeile_repl, x, flags=re.S)
    try:
        ET.fromstring(neu_x)
    except ET.ParseError as e:
        raise SystemExit(f"ABBRUCH: XML kaputt ({e}). Es wurde nichts geschrieben.")

    kaputt = zellen_reihenfolge_ok(neu_x)
    if kaputt:
        raise SystemExit(
            f"ABBRUCH: {len(kaputt)} Zeile(n) haetten Zellen in falscher "
            f"Reihenfolge (z. B. {kaputt[:5]}). Excel wuerde die Datei "
            f"repararieren bzw. verweigern. Es wurde nichts geschrieben.")

    doppelt = zellen_doppelt(neu_x)
    if doppelt:
        raise SystemExit(f"ABBRUCH: {len(doppelt)} doppelte Zellen "
                         f"(z. B. {doppelt[:5]}). Es wurde nichts geschrieben.")

    # Geteilte Formeln: jeder Follower braucht seine Master-Zelle. Wird die
    # Master-Zelle entfernt, meldet Excel 'Problem bei einigen Inhalten'.
    master_vor, follower_vor = geteilte_formeln(x)
    master_nach, follower_nach = geteilte_formeln(neu_x)
    verwaist = follower_nach - master_nach
    if verwaist:
        raise SystemExit(
            f"ABBRUCH: {len(verwaist)} geteilte Formel-Gruppe(n) verlieren ihre "
            f"Master-Zelle (si={sorted(verwaist)[:5]}). Excel wuerde die Datei "
            f"reparieren. Es wurde nichts geschrieben.")
    if master_vor - master_nach:
        raise SystemExit(
            f"ABBRUCH: {len(master_vor - master_nach)} Master-Zelle(n) "
            f"geteilter Formeln wurden entfernt. Es wurde nichts geschrieben.")

    print(f"XML ok - {ersetzt} gesetzt, {angelegt} angelegt, {geleert} geleert")
    print(f"Pruefungen bestanden: Zellreihenfolge, Eindeutigkeit, "
          f"{len(master_nach)} geteilte Formel-Gruppen vollstaendig")

    sicherung = pfad.with_name(
        f"{pfad.stem}.alterskat-{datetime.now():%Y-%m-%d_%H%M}{pfad.suffix}")
    shutil.copy2(pfad, sicherung)
    print(f"Sicherung: {sicherung.name}")

    teile[SHEET] = neu_x.encode("utf-8")
    tmp = pfad.with_suffix(".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
        for i in infos:
            zi = zipfile.ZipInfo(i.filename, date_time=i.date_time)
            zi.compress_type = i.compress_type
            zi.external_attr = i.external_attr
            out.writestr(zi, teile[i.filename])
    tmp.replace(pfad)
    print(f"Geschrieben: {ersetzt} Zellen gesetzt, {angelegt} angelegt, "
          f"{geleert} geleert")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
