"""Generiert fehlende Card-IDs und traegt sie in Spalte D der Mappe ein.

Regelwerk (uebernommen aus .kilo/agent/memberslescht-sync.md):
  * Alphabet   : ABCDEFGHJKLMNPQRSTUVWXYZ23456789 (32 Zeichen, kein 0/1/I/O)
  * Laenge     : 8
  * Uniqueness : gegen ALLE bestehenden IDs aus xlsm + data.db + Sekretariat
  * NIEMALS ohne Backup schreiben

Sicherheitspruefungen VOR dem Schreiben: XML parsen, Zellreihenfolge je Zeile,
doppelte Zellen, geteilte Formeln.

Aufruf:
  python3 docs/cotisation/cardids_generieren.py            # Nur anzeigen
  python3 docs/cotisation/cardids_generieren.py --apply    # Wirklich schreiben
"""
import pathlib
import re
import secrets
import shutil
import sqlite3
import sys
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import baut_arbeitsmappe as ba                                             # noqa: E402
import mappe                                                              # noqa: E402
import cotisation_regeln_setzen as regeln                                  # noqa: E402

VOS = pathlib.Path("/Users/netjogger58/CascadeProjects/Vereins-OS")
BLATT = "xl/worksheets/sheet1.xml"
STRINGS = "xl/sharedStrings.xml"
ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
LAENGE = 8


def bestehende_ids(pfad: pathlib.Path) -> set[str]:
    """Alle Card-IDs aus xlsm und beiden Datenbanken."""
    ids: set[str] = set()

    teile = {}
    with zipfile.ZipFile(pfad) as z:
        for n in z.namelist():
            teile[n] = z.read(n)
    bl = ba.liese_blatt(teile, ba.finde_blatt(teile, ba.BLATT))
    iCard = [c.strip() for c in bl[0]].index("Card-ID")
    for r in bl[1:]:
        v = (r[iCard] if iCard < len(r) else "").strip()
        if v:
            ids.add(v)
    print(f"  xlsm           : {len(ids)}")

    for db, tab in (("data.db", "members"),
                    ("Sekretariat.db", "sekretariat_members")):
        p = VOS / db
        if not p.is_file():
            print(f"  {db:<14}: fehlt (uebersprungen)")
            continue
        try:
            con = sqlite3.connect(p)
            d = {x[0] for x in con.execute(f"SELECT card_id FROM {tab}")
                 if x[0]}
            con.close()
            ids |= d
            print(f"  {db:<14}: {len(d)}")
        except Exception as e:                                            # noqa: BLE001
            print(f"  {db:<14}: FEHLER {e}")
    return ids

ERE, LETZ = 2, 591          # echte Datenzeilen; ab 592 stehen Vorlagen

def main() -> int:
    anwenden = "--apply" in sys.argv
    pfad = mappe.ziel()
    print(f"Datei: {pfad.name}\n")

    print("Bestehende Card-IDs:")
    bekannt = bestehende_ids(pfad)
    print(f"  -> {len(bekannt)} eindeutig zu meiden\n")

    teile, infos = {}, []
    with zipfile.ZipFile(pfad) as z:
        infos = z.infolist()
        for i in infos:
            teile[i.filename] = z.read(i.filename)
    bl = ba.liese_blatt(teile, ba.finde_blatt(teile, ba.BLATT))
    kopf = [c.strip() for c in bl[0]]
    iCard = kopf.index("Card-ID")
    iSpielt = kopf.index("Spielt J/R/N/X")

    def g(r, j):
        return (r[j] if j < len(r) else "").strip()

    ziele = [nr for nr, r in enumerate(bl[1:], start=2)
             if ERE <= nr <= LETZ and g(r, 0) and not g(r, iCard)]
    print(f"Fehlende Card-ID in Zeile {ERE}..{LETZ}: {len(ziele)}")
    for nr in ziele:
        r = bl[nr - 1]
        print(f"  Z{nr:<4} D{nr:<4} {g(r, 0)[:14]:<15}"
              f"{g(r, 1)[:13]:<14}Spielt={g(r, iSpielt)!r}")
    if not ziele:
        print("Nichts zu tun.")
        return 0

    # IDs erzeugen - gegen alle bekannten und untereinander eindeutig
    neu: dict[int, str] = {}
    alle = set(bekannt)
    for nr in ziele:
        for _ in range(10_000):
            kand = "".join(secrets.choice(ALPHABET) for _ in range(LAENGE))
            if kand not in alle:
                break
        else:
            raise SystemExit("ABBRUCH: kein freier Kandidat gefunden.")
        neu[nr] = kand
        alle.add(kand)

    print("\nNeue Card-IDs:")
    for nr, wert in neu.items():
        print(f"  D{nr:<4} {wert}")

    if not anwenden:
        print("\nNur angezeigt. Mit --apply wird geschrieben.")
        return 0

    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    sicherung = pfad.with_name(f"{pfad.stem}.cardids-{stamp}{pfad.suffix}")
    shutil.copy2(pfad, sicherung)
    print(f"\nSicherung: {sicherung.name}")

    # Shared-Strings: neue Eintraege anhaengen, Zaehler anpassen
    strings = teile[STRINGS].decode("utf-8")
    vorhanden = len(re.findall(r"<si>", strings))
    index: dict[int, str] = {}
    neu_si = ""
    for nr, wert in neu.items():
        index[nr] = vorhanden + len(index)
        neu_si += f"<si><t>{wert}</t></si>"
    if not strings.rstrip().endswith("</sst>"):
        raise SystemExit("ABBRUCH: sharedStrings endet nicht mit </sst>.")
    strings = strings.rstrip()[:-len("</sst>")] + neu_si + "</sst>"
    anzahl = len(re.findall(r"<si>", strings))
    strings = re.sub(r'count="\d+"', f'count="{anzahl}"', strings, count=1)
    strings = re.sub(r'uniqueCount="\d+"', f'uniqueCount="{anzahl}"',
                     strings, count=1)
    teile[STRINGS] = strings.encode("utf-8")

    # Zellen fuellen
    blatt = teile[BLATT].decode("utf-8")
    geschrieben, probleme = [], []
    for nr, wert in neu.items():
        ref = f"D{nr}"
        treffer = re.search(r'<c r="%s"([^>]*?)(/>|>.*?</c>)' % ref,
                            blatt, re.S)
        if not treffer:
            probleme.append(f"{ref}: Zelle nicht gefunden")
            continue
        attr, rest = treffer.group(1), treffer.group(2)
        if rest != "/>" and re.search(r"<v>[^<]+</v>|<is>", rest):
            probleme.append(f"{ref}: nicht leer ({rest[:40]!r})")
            continue
        # vorhandenes t-Attribut entfernen, dann als Shared-String setzen
        attr = re.sub(r'\s+t="[^"]*"', "", attr)
        neu_xml = f'<c r="{ref}"{attr} t="s"><v>{index[nr]}</v></c>'
        blatt = blatt[:treffer.start()] + neu_xml + blatt[treffer.end():]
        geschrieben.append(f"{ref} = {wert}")
    teile[BLATT] = blatt.encode("utf-8")

    if probleme:
        print("ABBRUCH - nichts geschrieben:")
        for p in probleme:
            print("  " + p)
        shutil.copy2(sicherung, pfad)
        return 1

    # Validierung VOR dem Speichern
    ET.fromstring(teile[BLATT])
    ET.fromstring(teile[STRINGS])
    kaputt = regeln.zellen_reihenfolge_ok(blatt)
    doppelt = regeln.zellen_doppelt(blatt)
    vor = regeln.geteilte_formeln(
        zipfile.ZipFile(sicherung).read(BLATT).decode("utf-8"))
    nach = regeln.geteilte_formeln(blatt)
    if kaputt or doppelt or vor != nach:
        print("ABBRUCH - Validierung fehlgeschlagen, nichts geschrieben:")
        print(f"  Zellreihenfolge kaputt: {kaputt}")
        print(f"  doppelte Zellen       : {doppelt}")
        print(f"  geteilte Formeln      : vor={len(vor[0])}/{len(vor[1])} "
              f"nach={len(nach[0])}/{len(nach[1])}")
        shutil.copy2(sicherung, pfad)
        return 1

    with zipfile.ZipFile(pfad, "w", zipfile.ZIP_DEFLATED) as z:
        for i in infos:
            z.writestr(i.filename, teile[i.filename])

    print("Geschrieben:")
    for s in geschrieben:
        print("  " + s)
    print(f"\nZellreihenfolge ok, keine doppelten Zellen, "
          f"geteilte Formeln unveraendert ({len(nach[0])}/{len(nach[1])}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


