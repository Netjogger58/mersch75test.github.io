"""Welche Zeilen haben keine CH/CJ-Zelle, und was steht dort?"""
import re
import sys
import zipfile

P = sys.argv[1]
z = zipfile.ZipFile(P)
s = z.read("xl/worksheets/sheet1.xml").decode("utf-8")

for r in range(580, 595):
    m = re.search(r'<row r="%d"([^>]*)>(.*?)</row>' % r, s, re.S)
    if not m:
        print(f"  Zeile {r}: KEINE <row>")
        continue
    inhalt = m.group(2)
    refs = [c.group(1) for c in re.finditer(r'<c r="([A-Z]+)\d+"', inhalt)]
    hat_ch = "CH" in refs
    hat_cj = "CJ" in refs
    name = re.search(r'<c r="A%d"[^>]*>(.*?)</c>' % r, inhalt, re.S)
    nm = re.sub(r"<[^>]+>", "", name.group(1)) if name else ""
    print(f"  Zeile {r}: CH={'j' if hat_ch else '-'} CJ={'j' if hat_cj else '-'} "
          f"Zellen={len(refs):>3} A={nm[:24]!r}")

vorhanden = [r for r in range(2, 910)
             if re.search(r'<c r="CH%d"' % r, s) and re.search(r'<c r="CJ%d"' % r, s)]
print(f"\nZeilen 2-909 mit BEIDEN Zellen: {len(vorhanden)}")
print(f"  Luecken: {[r for r in range(min(vorhanden), max(vorhanden) + 1)
                   if r not in vorhanden]}")
print(f"  Bereich: {min(vorhanden)}..{max(vorhanden)}")

print("\n--- Fehlende Spalten in 584-586 (Vergleich zu 583) ---")
def refs_of(r):
    m = re.search(r'<row r="%d"[^>]*>(.*?)</row>' % r, s, re.S)
    return [c.group(1) for c in re.finditer(r'<c r="([A-Z]+)\d+"', m.group(1))]

voll = refs_of(583)
for r in (584, 585, 586):
    fehlt = [c for c in voll if c not in refs_of(r)]
    print(f"  Zeile {r}: fehlende Spalten {fehlt}")
