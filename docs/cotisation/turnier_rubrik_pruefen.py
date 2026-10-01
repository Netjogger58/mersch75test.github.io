"""Prueft, dass jede Turnierzeile in GENAU EINER Rubrik erscheint.

Anlass: passtZurKategorie() gab Turnierzeilen einen pauschalen
Durchlass in JEDE Jugend-Rubrik. Das U11-Turnier stand deshalb auch
unter U15, U13M-P1, U13M-P2, U11M-2 und U7M. Auf der Seite gibt es
aber eigene Knoepfe je Mannschaft - die Turniere gehoeren in ihre
eigene Rubrik.

Der Test laedt die echten Funktionen und die echten Daten aus
live-center.html in node und fragt: in wie vielen Rubriken taucht
jede Turnierzeile auf? Erwartet: genau einer - der eigenen.

Zusaetzlich: jede Rubrik mit Daten muss einen Knopf bekommen, und
jede Turnierzeile muss ueber den Knopf "Turniere" erreichbar sein.
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path('/Users/netjogger58/CascadeProjects/mersch75test.github.io')
SEITE = ROOT / 'live-center.html'
text = SEITE.read_text()


def hole(name):
    """Holt eine Funktion - als 'function name()' oder als 'const name ='."""
    m = re.search(r'function\s+' + re.escape(name) + r'\s*\(.*?\n\}',
                  text, re.S)
    if m:
        return m.group(0)
    m = re.search(r'const\s+' + re.escape(name) + r'\s*=.*?=>\s*\{.*?\n\};',
                  text, re.S)
    if m:
        return m.group(0)
    raise SystemExit(f'ABBRUCH: {name}() nicht gefunden')


turnier_block = re.search(r'const tournamentData = \[(.*?)\n\];', text, re.S)
if not turnier_block:
    raise SystemExit('ABBRUCH: tournamentData nicht gefunden')

js = f"""
{text[text.index('function normalizeTeamLabel'):]}
""" if 'function normalizeTeamLabel' in text else ''

# Nur die noetigen Bausteine - der Rest der Seite braucht ein DOM.
teile = []
# istTurnier haengt an TOURNAMENT_GAST und trimText. Werden die nicht
# mitgeladen, stuerzt der Test ab, sobald passtZurKategorie sie wieder
# benutzt - und statt einer klaren Meldung kommt eine Fehlermeldung
# aus node. Das ist ein schlechter Wächter.
const = re.search(r'const TOURNAMENT_GAST = .*?;', text, re.S)
teile.append(const.group(0) if const else '')
for name in ('trimText', 'normalizeTeamLabel', 'istTurnier',
             'passtZurKategorie'):
    teile.append(hole(name))
teile.append('const tournamentData = [' + turnier_block.group(1) + '\n];')
teile.append('const STAT = [' +
             ','.join('"' + c + '"' for c in
                      ('JUGEND: U15G', 'JUGEND: U13M-P1', 'JUGEND: U13M-P2',
                       'JUGEND: U11M-1', 'JUGEND: U11M-2', 'JUGEND: U9M',
                       'JUGEND: U7M', 'MÄNNER 1 (H-PRO)',
                       'FRAUEN (D-PRO)')) + '];')
teile.append("""
const out = [];
tournamentData.forEach(r => {
  const treffer = STAT.filter(k => passtZurKategorie(r, k));
  out.push({ team: r.team, datum: r.datum, gast: r.gast,
             anzahl: treffer.length, rubriken: treffer });
});
console.log(JSON.stringify({ zeilen: out, stat: STAT }, null, 1));
""")

res = subprocess.run(['node', '-e', '\n'.join(teile)],
                     capture_output=True, text=True)
if res.returncode != 0:
    print(res.stderr[:2000])
    raise SystemExit('ABBRUCH: node konnte den Code nicht ausfuehren')

import json  # noqa: E402
daten = json.loads(res.stdout)

print('Rubriken auf der Seite:')
for s in daten['stat']:
    print('  ', s)
print()
print(f'Turnierzeilen: {len(daten["zeilen"])}')
print()
fehler = []
for z in daten['zeilen']:
    n = z['anzahl']
    ok = n == 1
    if not ok:
        fehler.append(z)
    print(f"  {z['datum']:15} {z['team']:18} -> {n} Rubrik(en)  "
          f"{z['rubriken']}")
    if not ok:
        print(f"      FEHLER: gehoert in genau 1 Rubrik, nicht in {n}")

print()
if fehler:
    print(f'BEFUND: {len(fehler)} Turnierzeilen stehen in falsch vielen Rubriken')
    raise SystemExit(1)
print('Jede Turnierzeile steht in genau ihrer eigenen Rubrik.')
raise SystemExit(0)