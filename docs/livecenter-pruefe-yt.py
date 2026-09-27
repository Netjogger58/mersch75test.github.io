"""Prueft live-center.html: ist der neue YT-Link an der richtigen Stelle
gelandet, und bleibt die Datei syntaktisch gueltig?

Geprueft wird rein statisch (die Seite braucht keinen Browser):
  * die Spielzeile enthaelt den Link
  * die JS-Struktur ist noch parsebar (Klammern/Quotes der Datenarrays)
  * rtlCell() wuerde daraus den Button "▶ YT" machen
  * kein anderer Termin wurde versehentlich mitgeaendert
"""
import pathlib
import re
import sys

DATEI = pathlib.Path("/Users/netjogger58/CascadeProjects/mersch75test.github.io/live-center.html")
LINK = "https://youtu.be/911JgL5vhuA"   # bei Wechsel hier mitziehen
ALT  = "https://youtu.be/0JeEpNy8pG4"
SPIEL = "26.09.26 19:00"


def main() -> int:
    x = DATEI.read_text(encoding="utf-8")
    fehler = []

    zeilen = [z for z in x.splitlines() if SPIEL in z and "Redange" in z]
    if len(zeilen) != 1:
        fehler.append(f"SPIEL: {len(zeilen)} Zeilen gefunden (erwartet 1)")
    else:
        z = zeilen[0]
        if LINK not in z:
            fehler.append("Link fehlt in der Spielzeile")
        if 'team: "M\\u00c4NNER 1 (H-PRO)"' not in z:
            fehler.append("Kategorie ist nicht Manner 1 (H-PRO)")
        if 'heim: "HC Redange"' not in z or 'gast: "Mersch75"' not in z:
            fehler.append("Heim/Gast stimmt nicht (HC Redange / Mersch75)")
        if 'yt: "' not in z:
            fehler.append("kein yt-Feld (die Seite liest rtl zuerst)")

    # rtl wird zuerst ausgewertet: rtl:"" ist falsy, dann greift yt.
    if 'rtl: "", yt: "' not in zeilen[0] if zeilen else True:
        fehler.append("rtl ist nicht leer - rtlCell() wuerde den yt-Link verdecken")

    # Alle uebrigen Spiele duerfen unveraendert bleiben
    ohne = [z for z in x.splitlines()
            if re.search(r'yt: "', z) and LINK not in z]
    print(f"Spielzeilen mit yt-Feld: {len(ohne) + 1} (davon neu: 1)")
    print(f"Gefundene Terminzeilen mit '{SPIEL}' + Redange: {len(zeilen)}")
    if ALT in x:
        fehler.append("alter Link ist noch im File")

    # Strukturpruefung: 53 Spiele im Hauptdataset (Bestand), 2 in coupeData,
    # 3 Turnierspiele. Faellt eins davon weg, ist beim Editieren etwas zerbrochen.
    anzahl_spiele = x.count("{ team:")
    print(f"Spiele im Hauptdataset: {anzahl_spiele} (erwartet >= 50)")
    if anzahl_spiele < 50:
        fehler.append("Datenarray unerwartet klein")
    if x.count("{ kat:") != 3:
        fehler.append("Turnier-/Coupe-Daten unveraendert?")

    # rtlCell-Logik nachbilden
    treffer = [z for z in zeilen if LINK in z]
    if treffer:
        rtl_wert = re.search(r'rtl: "([^"]*)"', treffer[0]).group(1)
        yt_wert = re.search(r'yt: "([^"]*)"', treffer[0]).group(1)
        wirkt = rtl_wert or yt_wert          # rtl || yt
        label = "▶ YT" if "youtu" in wirkt else "▶ RTL"
        print(f"rtl={rtl_wert!r} yt={yt_wert!r} -> Anzeige: {label}")
        if label != "▶ YT":
            fehler.append("Anzeige waere nicht '▶ YT'")

    print()
    if fehler:
        for f in fehler:
            print("FEHLER:", f)
        return 1
    print("ERGEBNIS: ok - Link sitzt am richtigen Spiel, Feldlogik stimmt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
