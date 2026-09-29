"""Prueft alle in docs/cotisation/*.py hart kodierten xlsm-Pfade auf Existenz.

Nur Pfade, die EINGABEN sind, zaehlen. Dateien, die das Skript selbst
erzeugt (B0..B5, I1..I5, TEST2*), sind keine defekten Verweise.
"""
import pathlib
import re

D = pathlib.Path(__file__).resolve().parent
DOCS = pathlib.Path("/Users/netjogger58/CascadeProjects/Vereins-OS/docs")
MUSTER = re.compile(r'"([^"\n]*\.xlsm)"')
# erzeugt von testbausteine*.py / testvarianten*.py selbst
ERZEUGT = re.compile(r"^(B\d|I\d|E\d|H\d|D\d|TEST\d)")

treffer = {}
for py in sorted(D.glob("*.py")):
    for nr, zeile in enumerate(py.read_text(errors="replace").splitlines(), 1):
        for roh in MUSTER.findall(zeile):
            if "{" in roh or "*" in roh or roh.startswith("/tmp/"):
                continue
            p = pathlib.Path(roh)
            kandidaten = [p] if p.is_absolute() else [D / p, DOCS / p, p]
            existiert = any(k.exists() for k in kandidaten)
            erzeugt = bool(ERZEUGT.match(p.name))
            treffer.setdefault(roh, {"ok": existiert, "erzeugt": erzeugt,
                                     "t": []})
            treffer[roh]["t"].append(f"{py.name}:{nr}")

print("=== xlsm-Verweise in Skripten ===\n")

kategorie = {"ok": [], "erzeugt": [], "kaputt": []}
for roh, d in sorted(treffer.items()):
    if d["ok"]:
        kategorie["ok"].append(roh)
    elif d["erzeugt"]:
        kategorie["erzeugt"].append(roh)
    else:
        kategorie["kaputt"].append((roh, d["t"]))

print(f"-- OK, existiert ({len(kategorie['ok'])}) --")
for r in kategorie["ok"]:
    print(f"  {pathlib.Path(r).name}")

print(f"\n-- wird vom Skript selbst erzeugt ({len(kategorie['erzeugt'])}) --")
for r in kategorie["erzeugt"]:
    print(f"  {pathlib.Path(r).name}")

print(f"\n*** KAPUTT ({len(kategorie['kaputt'])}) ***")
for r, t in kategorie["kaputt"]:
    print(f"  {r}")
    for x in t:
        print(f"      {x}")
