"""Setzt in Spalte AI ("Bénévole (B)") ein "B" nach der Vereinsregel.

Regel (vom 27.09.2026):
  1. In Spalte A steht ein Name,
  2. die Spalten AH, AI, AJ, AK, AL, AM, AN sind alle LEER,
  3. in P und Q steht kein GAJGL.
  -> dann bekommt die Zeile in AI ein "B".

Zu 3: GAJGL steht nachweislich in Q ("Code Courrier neu", 15 Zeilen), in P
("code courrier") kommt es kein einziges Mal vor. Die Sperre wird deshalb auf
BEIDE Spalten gelegt - so ist sie unabhaengig davon, welche der beiden Spalten
mal umbenannt wird.

Das Schreiben passiert chirurgisch im XML: es wird ausschliesslich der Inhalt
der AI-Zellen ersetzt, das Formatattribut "s" bleibt unangetastet. Formeln,
Rahmenlinien, Ausrichtung und alles Weitere bleiben, wie es war.

Aufruf:
  python3 docs/cotisation/benevole_setzen.py            # nur zaehlen
  python3 docs/cotisation/benevole_setzen.py --apply    # schreiben
"""
import pathlib
import re
import shutil
import sys
import zipfile
from datetime import datetime

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mappe  # noqa: E402

PRUEF = ["AH", "AI", "AJ", "AK", "AL", "AM", "AN"]
ZIEL_SPALTE = "AI"
SHEET = "xl/worksheets/sheet1.xml"


def colpos(spalte: str) -> int:
    return sum((ord(c) - 64) * 26 ** i for i, c in enumerate(reversed(spalte)))


def lade_strings(teile: dict) -> list:
    """Shared Strings auslesen. Excel legt eingetippten Text (Namen, Header)
    als Shared String ab - ohne diese Tabelle waere jede Zelle 'leer'."""
    roh = teile.get("xl/sharedStrings.xml")
    if not roh:
        return []
    x = roh.decode("utf-8")
    return ["".join(re.findall(r"<t[^>]*>(.*?)</t>", si, re.S))
            for si in re.findall(r"<si>(.*?)</si>", x, re.S)]


def zelle_wert(zelle: str, ss: list) -> str:
    if not zelle:
        return ""
    t = re.search(r"<is>.*?<t[^>]*>(.*?)</t>.*?</is>", zelle, re.S)   # Inline
    if t:
        return t.group(1)
    v = re.search(r"<v>(.*?)</v>", zelle, re.S)
    if not v:
        return ""
    if 't="s"' in zelle and ss:                                      # Shared
        i = int(v.group(1))
        return ss[i] if 0 <= i < len(ss) else ""
    return v.group(1)


def zellen_map(row_xml: str) -> dict:
    out = {}
    for c in re.finditer(r'<c r="([A-Z]+)\d+".*?(?:/>|>.*?</c>)', row_xml, re.S):
        out[c.group(1)] = c.group(0)
    return out


def main() -> int:
    # --datei muss hier EIGENS ausgewertet werden. mappe.ziel() alleine
    # liefert immer den Standardpfad - beim ersten Versuch hat das Skript
    # deshalb die echte Datei verändert, obwohl eine Kopie benannt war.
    if "--datei" in sys.argv:
        pfad = mappe.set_ziel(sys.argv[sys.argv.index("--datei") + 1])
        print(f"Arbeitsdatei (--datei): {pfad}")
    else:
        pfad = mappe.ziel()
        print(f"Arbeitsdatei (Standard): {pfad}")
    with zipfile.ZipFile(pfad) as z:
        infos = z.infolist()
        teile = {i.filename: z.read(i.filename) for i in infos}
    x = teile[SHEET].decode("utf-8")
    ss = lade_strings(teile)

    kopfzeile = zellen_map(re.search(r'<row r="1"[^>]*>(.*?)</row>', x, re.S).group(1))
    kopf = {s: zelle_wert(z, ss) for s, z in kopfzeile.items()}
    print(f"Datei      : {pfad.name}")
    print(f"Zielspalte : {ZIEL_SPALTE} = {kopf.get(ZIEL_SPALTE)!r}")
    print(f"Pruefspalten: " + ", ".join(
        f"{sp}={kopf.get(sp)!r}" for sp in PRUEF) + "\n")

    kandidaten, mit_name, gajgl_aus = [], 0, 0
    for m in re.finditer(r'<row r="(\d+)"[^>]*>(.*?)</row>', x, re.S):
        r = int(m.group(1))
        if r < 2:
            continue
        zellen = zellen_map(m.group(2))
        if not zelle_wert(zellen.get("A", ""), ss).strip():
            continue                                   # 1) Name noetig
        mit_name += 1
        if any(zelle_wert(zellen.get(sp, ""), ss).strip() for sp in PRUEF):
            continue                                   # 2) AH..AN muessen leer
        if any(zelle_wert(zellen.get(sp, ""), ss).strip().upper() == "GAJGL"
               for sp in ("P", "Q")):
            gajgl_aus += 1
            continue                                   # 3) kein GAJGL
        kandidaten.append(r)

    print(f"Zeilen mit Name (Spalte A)             : {mit_name}")
    print(f"davon AH..AN leer und kein GAJGL      : {len(kandidaten)}"
          f"   (GAJGL ausgeschlossen: {gajgl_aus})")
    print(f"erste Zielzeilen                       : {kandidaten[:8]}")

    if "--apply" not in sys.argv:
        print("\nNichts geschrieben. Mit --apply wirklich setzen.")
        return 0

    if not kandidaten:
        print("\nNichts zu tun - keine Zeile erfuellt die Regel.")
        return 0

    ziel = set(kandidaten)
    ersetzt = 0
    beispiel = []

    def zeile_repl(m):
        """m: 1 = <row ...>, 2 = Zeilennummer, 3 = Zellinhalt, 4 = </row>.

        WICHTIG: die Offsets von `alt` beziehen sich auf den ZELLINHALT
        (Gruppe 3), nicht auf den ganzen Treffer. Mit den falschen Offsets
        wurde jede bearbeitete Zeile vorn abgeschnitten -> kaputtes XML.
        """
        nonlocal ersetzt
        r = int(m.group(2))
        if r not in ziel:
            return m.group(0)
        inhalt = m.group(3)
        alt = re.search(r'<c r="%s%d"([^>]*?)(?:/>|>.*?</c>)'
                        % (ZIEL_SPALTE, r), inhalt, re.S)
        if not alt:
            return m.group(0)
        attr = re.sub(r'\s*r="[^"]*"', "", alt.group(1)).strip()
        attr = re.sub(r'\s*t="[^"]*"', "", attr)
        neu = (f'<c r="{ZIEL_SPALTE}{r}"{(" " + attr) if attr else ""} '
               f't="inlineStr"><is><t>B</t></is></c>')
        if len(beispiel) < 3:
            beispiel.append(alt.group(0) + "   ->   " + neu)
        ersetzt += 1
        return m.group(1) + inhalt[:alt.start()] + neu + inhalt[alt.end():] + m.group(4)

    neu_x = re.sub(r'(<row r="(\d+)"[^>]*>)(.*?)(</row>)', zeile_repl, x, flags=re.S)
    print("\nBeispiel-Zellen (alt -> neu):")
    for b in beispiel:
        print("   " + b)

    # SICHERHEITSNETZ: das Ergebnis muss gueltiges XML sein, BEVOR irgendetwas
    # geschrieben wird. Genau hier ist es beim ersten Versuch gescheitert.
    import xml.etree.ElementTree as ET
    try:
        ET.fromstring(neu_x)
    except ET.ParseError as e:
        raise SystemExit(f"ABBRUCH: erzeugtes XML ist kaputt ({e}). "
                         f"Es wurde nichts geschrieben.")
    print("XML-Pruefung: in Ordnung")

    sicherung = pfad.with_name(f"{pfad.stem}.benevole-{datetime.now():%Y-%m-%d_%H%M}{pfad.suffix}")
    shutil.copy2(pfad, sicherung)
    print(f"\nSicherung: {sicherung.name}")

    teile[SHEET] = neu_x.encode("utf-8")
    tmp = pfad.with_suffix(".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
        for i in infos:
            zi = zipfile.ZipInfo(i.filename, date_time=i.date_time)
            zi.compress_type = i.compress_type
            zi.external_attr = i.external_attr
            out.writestr(zi, teile[i.filename])
    tmp.replace(pfad)
    print(f"Ersetzt: {ersetzt} Zellen in {ZIEL_SPALTE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
