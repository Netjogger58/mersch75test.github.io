"""Vergleicht Excels TATSÄCHLICH berechnete Spalte L mit dem Python-Modell.

Das ist die einzige Pruefung, die aussagekraeftig ist. `pruefe_abgleich.py`
vergleicht zwei Python-Implementierungen miteinander und liest die Mappe
dafuer nicht - es kann eine falsche Excel-Formel nicht finden.

Dieses Skript liest die Werte, die EXCEL selbst berechnet und gespeichert hat.
Voraussetzung: die Mappe wurde in Excel geoeffnet, neu gerechnet und
gespeichert. Sonst sind die Werte leer.

    python3 docs/cotisation/pruefe_excel_gegen_python.py [mappe.xlsm]
"""
import pathlib
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import baut_arbeitsmappe as ba
import pruef_cotisation as pr

LIVE = pathlib.Path("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
                    "GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm")
P = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else LIVE
if not P.exists():
    raise SystemExit(f"ABBRUCH: {P} gibt es nicht.")
print(f"Geprueft wird: {P.name}")

teile = {}
with zipfile.ZipFile(P) as z:
    for n in z.namelist():
        teile[n] = z.read(n)
blatt = ba.finde_blatt(teile, ba.BLATT)
zeilen = ba.liese_blatt(teile, blatt)
kopf = [c.strip() for c in zeilen[0]]
iL = kopf.index("Cotisatioun")

CONFIG = pathlib.Path(__file__).parent


def cfg(name):
    return pr.liese_config(CONFIG / name)


tarife = pr.lade_tarife(CONFIG / "tarife-cotisation.csv")
ausnahmen = {(n.strip().upper(), p.strip().upper()): a.strip()
             for n, p, a in cfg("ausnahmen-cotisation.csv")}
haushalte = {pr.normalisiere_adresse(a.strip())
             for a, _b, *_rest in ((r + ["", ""])[:3]
                                   for r in cfg("haushalte-cotisation.csv"))
             if a.strip()}

modell = {x["excel_zeile"]: x["neu"] for x in
          pr.berechne(zeilen, ausnahmen, *tarife, haushalte)}

abw, geprueft = [], 0
for nr, z in enumerate(zeilen[1:], start=2):
    excel = z[iL] if iL < len(z) else ""
    soll = modell.get(nr, "")
    if not soll and not excel:
        continue
    geprueft += 1
    if excel != soll:
        abw.append((nr, z[0][:16], z[1][:12] if len(z) > 1 else "",
                    excel, soll))


def nur_schreibweise(a):
    """'210 (+0+50)' und '210' sind derselbe Betrag - Excel schreibt die
    Zuschlags-Notation mit, das Python-Modell nicht. Das ist kein Fehler."""
    return a[3].replace(" (+0+50)", "") == a[4]


echt = [a for a in abw if not nur_schreibweise(a)]
print(f"Geprueft: {geprueft} Zeilen mit Betrag")
print(f"Abweichungen gesamt          : {len(abw)}")
print(f"  davon nur Schreibweise     : {len(abw) - len(echt)}")
print(f"  davon echte Unterschiede   : {len(echt)}")
if echt:
    print()
    for a in echt:
        print(f"  Zeile {a[0]:<5} {a[1]:<17}{a[2]:<13}"
              f"Excel={a[3]!r:<18} Python={a[4]!r}")

    # BINGEN: Excel nimmt einen Spieler mehr an als Python. Zeige den
    # kompletten Haushalt mit Pass, Medico und dem Excel-Wert in CL.
    print("\n--- Haushalt von Zeile 58 im Detail ---")
    haus = zeilen[57]

    def g(z2, n):
        if n in kopf and kopf.index(n) < len(z2):
            return z2[kopf.index(n)]
        return "?"

    adr = g(haus, "Adresse")

    def norm(s):
        return " ".join(s.split())

    # Der Kopf enthaelt "Prochain \nMédico" mit Zeilenumbruch - der direkte
    # Vergleich findet die Spalte nicht, darum ueber den Leerraum.
    def gs(z2, teil):
        for i, k in enumerate(kopf):
            if norm(k) == norm(teil):
                return z2[i] if i < len(z2) else "?"
        return "?NICHT GEFUNDEN"

    for nr, z2 in enumerate(zeilen[1:], start=2):
        if g(z2, "Adresse") != adr:
            continue
        print(f"  Z{nr:<5} O={gs(z2,'Spielen J/R/N')!r:<4}"
              f"Pass={gs(z2,'Pass Nummer (Licences Joueurs / Joueuses)')!r:<12}"
              f"Medico={gs(z2,'Prochain \nMédico')!r:<10}"
              f"Kat={gs(z2,'Alterskategorie')!r:<7}"
              f"CL={gs(z2,'Spielberecht')!r}")




