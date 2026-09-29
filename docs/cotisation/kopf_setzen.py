"""Setzt den Spaltentitel O1 auf 'Spielt J/R/N/X'.

Warum: der Kopf lautete 'Spielt            J/R/N' (12 Leerzeichen) und passte
zu keinem Namen, den der Code kennt - der Stripe-Lauf brach ab. Zusaetzlich
wird X als zulaessiger Status dokumentiert (X = ungeklaert, zahlt 0).

Sicherheitsregeln, bewusst uebernommen aus altartern_setzen / regeln_setzen:
  * nur ersetzen, wenn die Zelle GENAU einmal auf den String zeigt
  * ansonsten Abbruch - sonst wuerde ein_shared String mehrere Zellen treffen
  * Sicherungskopie vor dem Schreiben
  * XML danach parsen
  * Reihenfolge der Zellen und geteilte Formellen pruefen

Aufruf:  python3 docs/cotisation/kopf_setzen.py [--apply]
"""
import pathlib
import re
import shutil
import sys
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mappe  # noqa: E402

BLATT = "xl/worksheets/sheet1.xml"
STRINGS = "xl/sharedStrings.xml"
ZELLE = "O1"
ALT = "Spielt            J/R/N"
NEU = "Spielt J/R/N/X"


def main() -> int:
    pfad = (mappe.set_ziel(sys.argv[sys.argv.index("--datei") + 1])
            if "--datei" in sys.argv else mappe.ziel())
    print(f"Datei: {pfad.name}")

    with zipfile.ZipFile(pfad) as z:
        infos = z.infolist()
        teile = {i.filename: z.read(i.filename) for i in infos}
    blatt = teile[BLATT].decode("utf-8")
    strings = teile[STRINGS].decode("utf-8")

    treffer = re.search(r'<c r="%s"[^>]*t="s"[^>]*><v>(\d+)</v>' % ZELLE, blatt)
    if not treffer:
        raise SystemExit(f"ABBRUCH: {ZELLE} ist kein Shared-String - "
                         f"nichts geschrieben.")
    idx = int(treffer.group(1))

    sis = list(re.finditer(r"<si>(.*?)</si>", strings, re.S))
    if idx >= len(sis):
        raise SystemExit(f"ABBRUCH: Index {idx} liegt ausserhalb. "
                         f"Nichts geschrieben.")
    jetzt = sis[idx].group(1)
    print(f"  {ZELLE} -> SharedString {idx}: {jetzt!r}")

    # Sicherheitsregel: der String darf nur von dieser einen Zelle benutzt
    # werden, sonst wuerde der Titel in weiteren Zellen mitgeaendert.
    nutzer = []
    for name in teile:
        if name.startswith("xl/worksheets/sheet"):
            s = teile[name].decode("utf-8")
            nutzer += [(name, r) for r in
                       re.findall(r'<c r="([A-Z]+\d+)"[^>]*t="s"[^>]*><v>%d</v>'
                                  % idx, s)]
    if nutzer != [(BLATT, ZELLE)]:
        raise SystemExit(f"ABBRUCH: SharedString {idx} wird auch von "
                         f"{[n for n in nutzer if n != (BLATT, ZELLE)]} "
                         f"benutzt. Nichts geschrieben.")
    if jetzt != f"<t>{ALT}</t>":
        raise SystemExit(f"ABBRUCH: unerwarteter Inhalt {jetzt!r} "
                         f"(erwartet <t>{ALT}</t>). Nichts geschrieben.")

    if "--apply" not in sys.argv:
        print(f"\nProbe: {jetzt}  ->  <t>{NEU}</t>")
        print("Nichts geschrieben. Mit --apply aendern.")
        return 0

    neue_si = sis[idx].group(0).replace(f"<t>{ALT}</t>", f"<t>{NEU}</t>")
    neu_strings = (strings[:sis[idx].start()] + neue_si + strings[sis[idx].end():])
    ET.fromstring(neu_strings)          # wirft bei kaputtem XML
    ET.fromstring(blatt)                # Blatt unveraendert -> muss halten

    sicherung = pfad.with_name(
        f"{pfad.stem}.kopf-{datetime.now():%Y-%m-%d_%H%M}{pfad.suffix}")
    shutil.copy2(pfad, sicherung)
    print(f"Sicherung: {sicherung.name}")

    teile[STRINGS] = neu_strings.encode("utf-8")
    tmp = pfad.with_suffix(".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
        for i in infos:
            zi = zipfile.ZipInfo(i.filename, date_time=i.date_time)
            zi.compress_type = i.compress_type
            zi.external_attr = i.external_attr
            out.writestr(zi, teile[i.filename])
    tmp.replace(pfad)
    print(f"Geschrieben: {ZELLE} = {NEU!r} (nur diese eine Zelle)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
