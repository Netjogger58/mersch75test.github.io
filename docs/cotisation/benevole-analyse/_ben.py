"""Bestandsaufnahme Benevole: Wer hat wirklich das B in AI?"""
import pathlib
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import baut_arbeitsmappe as ba

XLSM = pathlib.Path("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
                    "GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm")
teile = {}
with zipfile.ZipFile(XLSM) as z:
    for n in z.namelist():
        teile[n] = z.read(n)
bl = ba.liese_blatt(teile, ba.finde_blatt(teile, ba.BLATT))
kopf = [" ".join(c.split()) for c in bl[0]]


def fand(tip):
    v = [j for j, c in enumerate(kopf) if c.lower().startswith(tip)]
    return v[0] if v else None


# Lizenzspalten (kommen im Code als AH..AN vor - hier pruefen)
lizenzen = []
for j, c in enumerate(kopf):
    if "licenc" in c.lower() or "lizenz" in c.lower():
        lizenzen.append((j, c))
print("=== Lizenzspalten (fuer die B-Regel relevant) ===")
for j, c in lizenzen:
    print(f"  {j:<4} {c}")

iAI = fand("bénévole") or fand("benevole")
iO = fand("spielt j/r/n")
print(f"\nAI-Spalte: {iAI} ({kopf[iAI]!r}), O-Spalte: {iO} ({kopf[iO]!r})")
Z = range(2, 592)


def g(r, j):
    return ("" if j is None else (r[j] if j < len(r) else "")).strip()


alle = [(nr, r) for nr, r in enumerate(bl[1:], 2) if nr in Z and g(r, 0)]
mit_b = [(nr, r) for nr, r in alle if g(r, iAI).upper() == "B"]
print(f"\n=== Zeilen mit B in AI: {len(mit_b)} ===")
for nr, r in mit_b:
    liz = [kopf[j][:12] for j, _c in lizenzen if g(r, j)]
    print(f"  Z{nr} {g(r,0)[:14]:<16}{g(r,1)[:12]:<14}O={g(r,iO)!r:<5}"
          f"Lizenzen={liz or 'KEINE'}")

iAO = fand("pass")
print(f"\n=== B-Zeilen mit Pass in AO? ===")
for nr, r in mit_b:
    print(f"  Z{nr} {g(r,0)[:14]:<16}AO={g(r,iAO)!r:<9}O={g(r,iO)!r}")
