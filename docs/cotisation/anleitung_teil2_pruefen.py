"""Prueft die Behauptungen in TEIL 2 der Anleitung gegen die Datei.

Nicht nur die Spaltenbuchstaben, sondern auch die Zahlen: Blattnamen,
Regelwerte B1:B13, belegte Werte in Spalte O, Blattgroessen. Wer eine
Anleitung schreibt, erfindet sonst leicht eine Zahl, die plausibel klingt
und falsch ist.
"""
import pathlib
import re
import sys
import zipfile
from collections import Counter

sys.path.insert(0, '/Users/netjogger58/CascadeProjects/mersch75test.github.io/'
                   'docs/cotisation')
import baut_arbeitsmappe as ba  # noqa: E402

P = pathlib.Path('/Users/netjogger58/CascadeProjects/Vereins-OS/docs/'
                 'ANLEITUNG-Cotisation-Tresorier.md')
F = ('/Users/netjogger58/CascadeProjects/Vereins-OS/docs/'
     'GC 2026-10-01 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm')

z = zipfile.ZipFile(F)
t = {n: z.read(n) for n in z.namelist()}
doc = P.read_text()
fehler = []
Hinweis = []

# --- Blaetter ---------------------------------------------------------
wb = z.read('xl/workbook.xml').decode()
echt = re.findall(r'<sheet name="([^"]+)"', wb)
print(f'Blätter in der Datei: {len(echt)}')
fehlend = [b for b in echt if b not in doc]
if fehlend:
    fehler.append(f'Blätter nicht erwähnt: {fehlend}')
else:
    print('  alle im Text erwähnt')

# --- Blattgroessen -------------------------------------------------

# --- Regelwerte B1:B13 ------------------------------------------------
cfg = ba.liese_blatt(t, 'xl/worksheets/sheet12.xml')
print('Regelwerte B1:B13:')
for i in range(13):
    name = (cfg[i][0] or '').strip()
    wert = (cfg[i][1] or '').strip()
    zeile = [l for l in doc.split('\n') if l.startswith(f'| `B{i + 1}`')]
    ok = bool(zeile) and wert in zeile[0]
    if not ok:
        fehler.append(f'B{i + 1} {name}={wert!r} steht nicht so im Text')
    print(f'  B{i + 1:<3} {name:<20} {wert:<12} {"ja" if ok else "NEIN"}')

# --- Spalte O: die behaupteten Haeufigkeiten -------------------------
rows = ba.liese_blatt(t, 'xl/worksheets/sheet1.xml')
k = [c.strip() for c in rows[0]]
cnt = Counter((r[k.index('Spielt J/R/N/P')] or '(leer)').strip()
              for r in rows[1:901])
behauptet = re.search(r'(\d+) × `N`, (\d+) × `J`, (\d+) × `P`, (\d+) × `R`, '
                      r'(\d+) leer', doc)
print('\nSpalte O — Häufigkeiten:')
if behauptet:
    n, j, p, rr, leer = (int(x) for x in behauptet.groups())
    for wert, soll in (('N', n), ('J', j), ('P', p), ('R', rr),
                       ('(leer)', leer)):
        ist = cnt.get(wert, 0)
        ok = ist == soll
        if not ok:
            fehler.append(f'Spalte O: {wert} ist {ist}x, Text sagt {soll}x')
        print(f'  {wert:<7} Text {soll:<5} Datei {ist:<5} {"ja" if ok else "NEIN"}')
else:
    fehler.append('Haeufigkeitsangabe zu Spalte O nicht gefunden')

# --- Anzahl Inapte-Markierungen ---------------------------------------
n_in = sum(1 for r in rows[1:901]
           if (r[k.index('Inapte')] or '').strip()
           or (r[k.index('Inapte temporaire (Date)')] or '').strip())
beh = re.search(r'trägt genau \*\*eine\*\* Person', doc)
print(f'\nInapte-Markierungen: {n_in}')
if beh and n_in != 1:
    fehler.append(f'Text sagt "genau eine" Inapte-Markierung, Datei hat {n_in}')
else:
    print('  stimmt mit dem Text überein')

print()
if fehler:
    print('FEHLER:')
    for f in fehler:
        print('  -', f)
else:
    print('Alle Angaben in Teil 2 stimmen mit der Datei überein.')
for h in Hinweis:
    print('Hinweis:', h)
raise SystemExit(1 if fehler else 0)