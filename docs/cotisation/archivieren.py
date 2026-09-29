"""Verschiebt Sicherungen/Testartefakte/Sperrdateien nach docs/_archiv/.

Sicherheitsgurt:
  1. Vor dem Umzug wird ermittelt, welche xlsm Skripte referenzieren.
  2. Keine davon darf in der Umzugsliste stehen -> sonst Abbruch.
  3. Nach dem Umzug wird der Pfadcheck erneut ausgefuehrt.

Aufruf:  python3 .../archivieren.py [--apply]
"""
import pathlib
import re
import shutil
import subprocess
import sys

DOCS = pathlib.Path("/Users/netjogger58/CascadeProjects/Vereins-OS/docs")
ZIEL = DOCS / "_archiv"
D = pathlib.Path(__file__).resolve().parent

# Diese Dateien duerfen NIEMALS umziehen: Live, Quelle, Test1 (13 Skripte)
# und TEST2_nur-blatt1 (check_backups.py liest es).
PFLICHT = {
    "GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm",
    "GC 2026-09-24 MEMBERSLESCHT 2026-2027.xlsm",
    "GC MEMBERSLESCHT 2026-2027.xlsm",
    "TEST1_nur-calcchain.xlsm",
    "TEST2_nur-blatt1.xlsm",
}

MUSTER = re.compile(r"^(.*\.(regeln|alterskat|kopf|benevole|backup|"
                    r"cardids|REPARIERT)-.*|TEST2.*|_temp_shifted)"
                    r"(\.xlsm)?$")


def referenziert() -> set[str]:
    """Namen aller xlsm, die in docs/cotisation/*.py GELESEN werden.

    Nennungen in schreibe()/print() sind Schreibziele bzw. Ausgabe und
    blockieren den Umzug zu Unrecht.
    """
    pat = re.compile(r'"([^"\n]*\.xlsm)"')
    ausgabe = re.compile(r"\b(schreibe|print)\s*\(")
    out = set()
    for py in D.glob("*.py"):
        for zeile in py.read_text(errors="replace").splitlines():
            if ausgabe.search(zeile):
                continue
            for roh in pat.findall(zeile):
                out.add(pathlib.Path(roh).name)
    return out


def main() -> int:
    anwenden = "--apply" in sys.argv
    alle = sorted(DOCS.glob("*.xlsm"))
    locker = sorted(DOCS.glob("~$*.xlsm"))
    # PFLICHT explizit aus der Umzugsliste nehmen - nicht nur indirekt
    kandidaten = [p for p in alle
                  if MUSTER.match(p.name) and p.name not in PFLICHT] + locker

    print(f"Vorhandene xlsm im Docs-Ordner: {len(alle)}")

    belegt = referenziert()
    print(f"Skripte referenzieren {len(belegt)} xlsm-Namen")

    gefahr = [p for p in kandidaten if p.name in belegt]
    if gefahr:
        print("\nABBRUCH - Umzugskandidaten werden von Skripten gebraucht:")
        for p in gefahr:
            print(f"  {p.name}")
        return 1

    fehlend = [n for n in PFLICHT if not (DOCS / n).exists()]
    if fehlend:
        print(f"\nABBRUCH - Pflichtdatei fehlt: {fehlend}")
        return 1

    bleibend = [p for p in alle if p not in kandidaten]
    print(f"\nUmzug ({len(kandidaten)}):")
    for p in kandidaten:
        print(f"  -> {p.name}")
    print(f"\nBleibt ({len(bleibend)}):")
    for p in bleibend:
        print(f"     {p.name}")

    if not anwenden:
        print("\nNur angezeigt. Mit --apply umziehen.")
        return 0

    ZIEL.mkdir(exist_ok=True)
    umgezogen = 0
    for p in kandidaten:
        z = ZIEL / p.name
        if z.exists():
            print(f"  UEBERSPRUNGEN (bereits da): {p.name}")
            continue
        shutil.move(str(p), str(z))
        umgezogen += 1
    print(f"\n{umgezogen} Dateien nach {ZIEL} verschoben.")

    print("\n--- Pfadcheck nach dem Umzug ---")
    r = subprocess.run([sys.executable, str(D / "pfadcheck.py")],
                       capture_output=True, text=True)
    zeile = [z for z in r.stdout.splitlines() if "KAPUTT" in z]
    print("  " + (zeile[0] if zeile else "kein Ergebnis"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

