"""Die 7 B-Halter mit aktivem Status + CSV-Export aller 258 zur Durchsicht."""
import csv
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


def col(b):
    j = 0
    for ch in b:
        j = j * 26 + (ord(ch) - 64)
    return j - 1


iAN, iO, iQ, iL = col("AN"), col("O"), col("Q"), col("L")
iG = col("G")
Z = range(2, 592)


def g(r, j):
    return (r[j] if j < len(r) else "").strip()


mit_b = [(nr, r) for nr, r in enumerate(bl[1:], 2)
         if nr in Z and g(r, 0) and g(r, iAN).upper() == "B"]

print("=== B-Halter mit aktivem Status (J/R/P) ===")
for nr, r in mit_b:
    if g(r, iO) != "N":
        print(f"  Z{nr} {g(r,0)[:14]:<16}{g(r,1)[:12]:<14}"
              f"O={g(r,iO)!r:<5}Q={g(r,iQ)!r:<9}L={g(r,iL)!r}")

print("\n=== B-Halter mit Betrag in L (ausser 0/leer) ===")
betrag = [(nr, r) for nr, r in mit_b if g(r, iL) not in ("", "0")]
print(f"  Anzahl: {len(betrag)}")
for nr, r in betrag:
    print(f"  Z{nr} {g(r,0)[:14]:<16}{g(r,1)[:12]:<14}"
          f"O={g(r,iO)!r:<5}L={g(r,iL)!r}")

out = pathlib.Path(__file__).parent / "Benevole-Durchsicht.csv"
with open(out, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Zeile", "Nom", "Prenom", "Status O", "Haushalt Q",
                "Betrag L", "BEHALTEN? (B loeschen = leer lassen)"])
    for nr, r in mit_b:
        w.writerow([nr, g(r, 0), g(r, 1), g(r, iO), g(r, iQ), g(r, iL), ""])
print(f"\nDurchsichtsliste: {out} ({len(mit_b)} Zeilen)")
