"""Echte Spalten AH..AN - was steht dort?"""
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


for j in range(30, 46):
    print(f"  {brief(j):<4} idx={j:<3} {kopf[j]!r}")
