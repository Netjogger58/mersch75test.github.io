"""Comité-Mitglieder: Spalte T=1 oder Spalte BI='Comite'.

Vorgabe: sie muessen mindestens 50 zahlen, also nicht (0+50).
METZLER Bernard (T=1) soll 50.- bekommen, CLEMENT Liliane bleibt (0+50).
"""
import collections
import pathlib
import sys

import openpyxl

D = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(D))
import pruef_cotisation as pr  # noqa: E402

MAPPE = ("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
         "GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm")
CSV = pathlib.Path("/Users/netjogger78/CascadeProjects/Vereins-OS/docs/"
                   "GC 2026-09-24 MEMBERSLESCHT 2026-2027.csv")
if not CSV.exists():
    CSV = pathlib.Path("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
                       "GC 2026-09-24 MEMBERSLESCHT 2026-2027.csv")

s = openpyxl.load_workbook(MAPPE)["Membres 2026_2027"]

print("Spalte BI (Comité) - Werteverteilung:")
cnt = collections.Counter()
for r in range(2, 904):
    v = s["BI" + str(r)].value
    cnt["" if v is None else str(v).strip()[:24]] += 1
print("  ", dict(cnt.most_common(10)))

zl = pr.lade_csv(CSV)
kopf = [c.strip() for c in zl[0]]


def sp(key):
    name = pr.SPALTEN[key]
    if name in kopf:
        return kopf.index(name)
    for alt in pr.SPALTEN_ALT.get(name, ()):
        if alt in kopf:
            return kopf.index(alt)
    raise SystemExit(f"Spalte {key!r} nicht gefunden")


T, ZB, REG, OF, RES = pr.lade_tarife(D / "tarife-cotisation.csv")
A, H = pr.lade_ausnahmen(D / "ausnahmen-cotisation.csv")
erg = pr.berechne(zl, A, T, ZB, REG, OF, RES, H)
by = {e["excel_zeile"]: e for e in erg}

comite = [r for r in range(2, 904)
          if str(s["T" + str(r)].value or "").strip() == "1"
          or "comit" in str(s["BI" + str(r)].value or "").lower()]
print(f"\nComité-Zeilen (T=1 oder BI='Comite'): {len(comite)}\n")
for r in sorted(comite):
    e = by.get(r, {})
    print(f"  Z{r:>3} {str(s['A'+str(r)].value or '')[:16]:<16} "
          f"{str(s['B'+str(r)].value or '')[:13]:<13} "
          f"St={str(s['O'+str(r)].value or '-'):<2} "
          f"T={str(s['T'+str(r)].value or '-'):<4} "
          f"BI={str(s['BI'+str(r)].value or '-')[:10]:<10} "
          f"Fam={str(s['Q'+str(r)].value or '-'):<7} "
          f"Tr={'J' if e.get('ist_traeger') else '-'} "
          f"-> {e.get('neu') or '(leer)':<8} {e.get('grund','')[:32]}")
