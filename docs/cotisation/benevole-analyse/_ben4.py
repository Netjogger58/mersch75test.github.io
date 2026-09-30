"""Bestandsaufnahme Benevole mit der RICHTIGEN Spalte AN (idx 39)."""
import collections
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


def brief(j):
    s = ""
    j += 1
    while j:
        j, r = divmod(j - 1, 26)
        s = chr(65 + r) + s
    return s


def col(b):
    j = 0
    for ch in b:
        j = j * 26 + (ord(ch) - 64)
    return j - 1


iAN, iO, iQ, iAO = col("AN"), col("O"), col("Q"), col("AO")
print(f"AN={kopf[iAN]!r}  O={kopf[iO]!r}  Q={kopf[iQ]!r}  AO={kopf[iAO]!r}")
Z = range(2, 592)


def g(r, j):
    return (r[j] if j < len(r) else "").strip()


alle = [(nr, r) for nr, r in enumerate(bl[1:], 2) if nr in Z and g(r, 0)]
mit_b = [(nr, r) for nr, r in alle if g(r, iAN).upper() == "B"]
print(f"\nZeilen mit B in AN (Benevole): {len(mit_b)} von {len(alle)}")
for v, c in sorted(collections.Counter(g(r, iO) for _n, r in mit_b).items()):
    print(f"  Status {v!r:<5} {c}x")

# Regelprobe: B + echter Pass in AO
mit_pass = [(nr, r) for nr, r in mit_b if g(r, iAO)]
print(f"\nB UND Pass in AO: {len(mit_pass)}")
for nr, r in mit_pass:
    print(f"  Z{nr} {g(r,0)[:14]:<16}{g(r,1)[:12]:<14}"
          f"O={g(r,iO)!r:<5}AO={g(r,iAO)!r:<9}Q={g(r,iQ)!r}")

# Benevole-Regel damals: AH..AN leer (alt) — dagegen halten, was heute stimmt
# Heute korrekt: keine ECHTE Lizenz in AO/AP/AQ/AR/AS?
liz_cols = [col(x) for x in ("AO", "AP", "AQ", "AR", "AS")]
print("\nB-Zeilen mit Inhalt in AO..AS (echte Lizenzspalten):")
treffer = 0
for nr, r in mit_b:
    voll = [brief(j) for j in liz_cols if g(r, j)]
    if voll:
        treffer += 1
        if treffer <= 15:
            print(f"  Z{nr} {g(r,0)[:14]:<16}{voll}")
print(f"  gesamt: {treffer} von {len(mit_b)}")
