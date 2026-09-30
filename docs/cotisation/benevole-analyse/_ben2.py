"""Benevole-Zusammenfassung: Anzahl, Regelverstoesse, Helfer ja/nein unklar."""
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


iAI = fand("bénévole")
iO = fand("spielt j/r/n")
iQ = fand("code courrier neu")
iAO = fand("pass")
lic = [j for j, c in enumerate(kopf)
       if c and ("licenc" in c.lower() or "lizenz" in c.lower())]
Z = range(2, 592)


def g(r, j):
    return ("" if j is None else (r[j] if j < len(r) else "")).strip()


alle = [(nr, r) for nr, r in enumerate(bl[1:], 2) if nr in Z and g(r, 0)]
mit_b = [(nr, r) for nr, r in alle if g(r, iAI).upper() == "B"]

print(f"Zeilen mit B in AI: {len(mit_b)} von {len(alle)} Mitgliedern")
print(f"Lizenzspalten gefunden: {[kopf[j] for j in lic]}")

# Regel aus benevole_setzen.py: AH..AN leer UND kein GAJGL in P/Q
regel_ok, regel_gebrochen = [], []
for nr, r in mit_b:
    liz_voll = [kopf[j] for j in lic if g(r, j)]
    if liz_voll or g(r, iQ) == "GAJGL":
        regel_gebrochen.append((nr, r, liz_voll))
    else:
        regel_ok.append((nr, r))

print(f"  entsprechen der B-Regel (keine Lizenz, kein GAJGL): {len(regel_ok)}")
print(f"  VERSTOSS gegen die B-Regel: {len(regel_gebrochen)}")
for nr, r, liz in regel_gebrochen[:20]:
    print(f"    Z{nr} {g(r,0)[:14]:<16}O={g(r,iO)!r:<5}"
          f"Q={g(r,iQ)!r:<9}hat:{liz or 'GAJGL'}")

print(f"\nStatus O der B-Halter:")
import collections
for v, c in sorted(collections.Counter(g(r, iO)
                                       for _n, r in mit_b).items()):
    print(f"  {v!r:<6} {c}x")
