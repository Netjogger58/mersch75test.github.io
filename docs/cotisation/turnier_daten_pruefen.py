"""Prueft die Turnierdaten in live-center.html auf Widersprueche.

Anlass: im Turnier-Array standen zwei Zeilen mit IDENTISCHEM Datum,
Uhrzeit und Ort fuer verschiedene Mannschaften (U9 und U11 am
10.11.26 9:30 in Mersch75). Zwei Mannschaften koennen nicht zur
selben Zeit am selben Ort spielen - es ist mit hoher Wahrscheinlichkeit
ein Altstand, der beim Ergaenzen neuer Daten liegen blieb.

Geprueft wird deshalb nicht, ob eine Zeile "richtig" aussieht, sondern
ob die Zeilen in sich zusammenpassen:

1. Keine zwei Mannschaften zur selben Zeit am selben Ort.
2. Die Liste ist nach Datum sortiert.
3. Keine Zeile ohne Datum.

Ein Altstand faellt dabei nicht auf, wenn er allein steht. Deshalb
werden die Zeilen auch ausgewiesen, damit man sie gegen die Meldung
des Secretaire pruefen kann.
"""
import collections
import pathlib
import re
import sys

ROOT = pathlib.Path('/Users/netjogger58/CascadeProjects/mersch75test.github.io')
SEITE = ROOT / 'live-center.html'

text = SEITE.read_text()

BLOCK = re.search(r'const tournamentData = \[(.*?)\n\];', text, re.S)
if not BLOCK:
    raise SystemExit('ABBRUCH: tournamentData nicht gefunden')

ZEILE = re.compile(
    r'\{ team: "([^"]*)", datum: "([^"]*)", heim: "([^"]*)", '
    r'gast: "([^"]*)"')

daten = []
for m in ZEILE.finditer(BLOCK.group(1)):
    daten.append({'team': m.group(1), 'datum': m.group(2),
                  'heim': m.group(3), 'gast': m.group(4)})

print(f'Turnierzeilen gefunden: {len(daten)}')
print()
for d in daten:
    print(f"  {d['datum']:15} {d['team']:18} {d['heim']:14} {d['gast']}")

fehler = []

# --- 1) gleiche Zeit, gleicher Ort, verschiedene Mannschaft -----------
print()
print('1) Zeitgleichheit am selben Ort:')
orte = collections.defaultdict(set)
for d in daten:
    orte[(d['datum'], d['heim'])].add(d['team'])
kollision = {k: v for k, v in orte.items() if len(v) > 1}
if not kollision:
    print('   keine - gut')
for (datum, heim), teams in sorted(kollision.items()):
    print(f'   KOLLISION am {datum} in {heim}: {sorted(teams)}')
    fehler.append(f'{len(teams)} Mannschaften am {datum} in {heim}: '
                  f'{sorted(teams)}')

# --- 2) Sortierung ---------------------------------------------------
def schluessel(datum):
    t, uhrzeit = datum.split(' ')
    tt, mm, jj = t.split('.')
    return (int(jj), int(mm), int(tt), uhrzeit)


unsortiert = []
for a, b in zip(daten, daten[1:]):
    if schluessel(a['datum']) > schluessel(b['datum']):
        unsortiert.append((a, b))
print()
print('2) Nach Datum sortiert:')
if not unsortiert:
    print('   ja')
for a, b in unsortiert:
    print(f'   {a["datum"]} vor {b["datum"]} - nicht sortiert')
    fehler.append(f'Sortierung: {a["datum"]} steht vor {b["datum"]}')

# --- 3) Vollstaendigkeit ---------------------------------------------
print()
print('3) Zeilen ohne Datum oder mit kaputtem Format:')
kaputt = [d for d in daten if not re.match(r'^\d{2}\.\d{2}\.\d{2} \d{1,2}:\d{2}$',
                                           d['datum'])]
if not kaputt:
    print('   keine')
for d in kaputt:
    fehler.append(f'unbrauchbares Datum: {d["datum"]!r}')
    print(f'   {d}')

# --- 4) Vollstaendige Dubletten --------------------------------------
print()
print('4) Wortgleiche Zeilen:')
doppelt = [t for t, n in collections.Counter(
    (d['team'], d['datum'], d['heim'], d['gast']) for d in daten).items()
    if n > 1]
if not doppelt:
    print('   keine')
for team, anzahl in doppelt:
    fehler.append(f'dieselbe Zeile {anzahl}x: {team}')
    print(f'   {anzahl}x {team}')

print()
if fehler:
    print('BEFUNDE:')
    for f in fehler:
        print('  -', f)
    raise SystemExit(1)
print('Turnierdaten sind in sich stimmig.')
raise SystemExit(0)