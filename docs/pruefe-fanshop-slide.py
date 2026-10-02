"""Prueft die FANshop-Karussell-Slide: Bildverweise, Shop-Link, keine
verwaisten Pfade. Rein statisch, kein Browser noetig."""
import pathlib
import re
import urllib.parse

ROOT = pathlib.Path("/Users/netjogger58/CascadeProjects/mersch75test.github.io")
SHOP = "https://www.peterssportsfirveraeiner.com/store/hb-mersch/"

fehler = []
for seite in ("index.html", "wellkomm-mapp.html"):
    p = ROOT / seite
    x = p.read_text(encoding="utf-8")
    refs = sorted({r for r in re.findall(r'(?:src|srcset)="(assets/[^"?]+)', x)
                   if "FANshop" in r or "fanshop" in r})
    print(f"=== {seite}: {len(refs)} FANshop-Verweise")
    for r in refs:
        ok = (ROOT / urllib.parse.unquote(r)).exists()
        print(f"   {'ok  ' if ok else 'FEHLT'} {r}")
        if not ok:
            fehler.append(r)
    if seite == "index.html":
        print("   Slides im Karussell:", x.count("data-news-slide>"))
        print("   Shop-Link:", x.count(SHOP), "x")
        if SHOP not in x:
            fehler.append("Shop-Link fehlt")
        if "assets/pages/wellkomm-mapp/media/FANshop" in x:
            fehler.append("veralteter Pfad in index.html")

for p in ROOT.rglob("*.html"):
    s = str(p)
    if ".kilo" in s or "/backup/" in s or "/archive/" in s:
        continue
    if "assets/pages/wellkomm-mapp/media/FANshop" in p.read_text(
            encoding="utf-8", errors="replace"):
        print("VERWAIST:", p.relative_to(ROOT))
        fehler.append(f"verwaist in {p.name}")

print()
print("ERGEBNIS:", "ok - alle Verweise aufloesbar" if not fehler
      else f"{len(fehler)} Probleme: {fehler}")
