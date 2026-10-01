"""Prueft den Coupe-Weg im Generator gegen die Live-Daten der FLH.

Der Generator hat den Knopf "Coupe dieses Wochenende laden". Er sammelt
die Spiele aus einem Zeitraum Freitag bis Sonntag und schreibt sie in
das Textfeld fuer den Postergenerator.

Die Zuordnung Coupe -> Mannschaft steckt in getGeneratorCoupeTeamKey().
Sie entscheidet, in welches Poster ein Coupe-Spiel wandert - und sie
ist der Punkt, um den es hier geht: der Coupe U13 wird auf "u13p1"
abgebildet. Ob das stimmt, ist eine ANNAHME des Codes, keine Aussage
der FLH; die FLH fuehrt den Wettbewerb als "U13 MIXTE (U13M-C)". Der
Test kann das nicht entscheiden, nur sichtbar machen.

Geprueft wird mit den ECHTEN Funktionen des Generators und den
Live-Daten, ob das bekannte U15-Spiel vom 03.10.2026 im Coupe-Weg
ankommt und welcher Mannschaft es zugeordnet wird.
"""
import json
import pathlib
import re
import subprocess
import sys
import urllib.request

ROOT = pathlib.Path('/Users/netjogger58/CascadeProjects/mersch75test.github.io')
SEITE = (ROOT / 'generator.html').read_text()

WETTBEWERBE = [('169141', 'COUPE: MÄNNER (H-C-LN)'),
               ('169136', 'COUPE: FRAUEN (D-C-LN)'),
               ('169146', 'COUPE: MÄNNER (H-C-FLH)'),
               ('169156', 'COUPE: U15 JONGEN (U15G-C)'),
               ('169151', 'COUPE: U13 MIXTE (U13M-C)')]


def hole(name):
    """Klammerbewusst - dieselbe Begruendung wie im Live-Center-Test."""
    start = None
    for mstr in (r'function\s+' + name + r'\s*\(', r'const\s+' + name + r'\s*='):
        m = re.search(mstr, SEITE)
        if m:
            start = m.start()
            break
    if start is None:
        raise SystemExit(f'ABBRUCH: {name} nicht im Generator')
    tiefe = 0
    i, n, zustand = start, len(SEITE), None
    while i < n:
        c = SEITE[i]
        nxt = SEITE[i + 1] if i + 1 < n else ''
        if zustand == '//':
            if c == '\n':
                zustand = None
        elif zustand == '/*':
            if c == '*' and nxt == '/':
                zustand = None
                i += 1
        elif zustand in ("'", '"', '`'):
            if c == '\\':
                i += 1
            elif c == zustand:
                zustand = None
        else:
            if c == '/' and nxt == '/':
                zustand = '//'
                i += 1
            elif c == '/' and nxt == '*':
                zustand = '/*'
                i += 1
            elif c in ("'", '"', '`'):
                zustand = c
            elif c == '{':
                tiefe += 1
            elif c == '}':
                tiefe -= 1
                if tiefe == 0:
                    return SEITE[start:i + 1]
        i += 1
    raise SystemExit(f'ABBRUCH: {name} nicht geschlossen')


payload = []
try:
    for cl, label in WETTBEWERBE:
        url = ('https://spo.handball4all.de/service/if_g_json.php'
               f'?cmd=ps&og=95&p=142&cl={cl}&ca=1')
        with urllib.request.urlopen(url, timeout=30) as r:
            roh = json.loads(r.read())
        roh = roh[0] if isinstance(roh, list) else roh
        inhalt = roh.get('content', {})
        spiele = list(inhalt.get('actualGames') or [])
        spiele += (inhalt.get('futureGames') or {}).get('games', []) or []
        for g in spiele:
            if 'Mersch' not in g.get('gHomeTeam', '') + g.get('gGuestTeam', ''):
                continue
            payload.append({
                'team': label,
                'datum': f"{g.get('gDate','')} {g.get('gTime','')}".strip(),
                'heim': g.get('gHomeTeam', '').strip(),
                'gast': g.get('gGuestTeam', '').strip(),
                'halle': str(g.get('gGymnasiumNo', '') or '').strip(),
            })
except Exception as e:                                     # noqa: BLE001
    print(f'FLH nicht erreichbar ({e}) - Test uebersprungen.')
    raise SystemExit(0)

print(f'Live-Coupe-Spiele mit Mersch-Bezug: {len(payload)}')

teile = [
    hole('isGeneratorCoupeGame'),
    hole('getGeneratorCoupeTeamKey'),
    hole('buildCoupeRawScheduleText'),
    'const spiele = ' + json.dumps(payload, ensure_ascii=False) + ';',
    """
const nurCoupe = spiele.filter(isGeneratorCoupeGame);
const out = {
  gesamt: spiele.length,
  nurCoupe: nurCoupe.length,
  ohneCoupe: spiele.filter(g => !isGeneratorCoupeGame(g)).length,
  zuordnung: nurCoupe.map(g => ({
    team: g.team, datum: g.datum, key: getGeneratorCoupeTeamKey(g)
  })),
  text: buildCoupeRawScheduleText(nurCoupe)
};
console.log(JSON.stringify(out, null, 1));
""",
]

res = subprocess.run(['node', '-e', '\n'.join(teile)],
                     capture_output=True, text=True)
if res.returncode != 0:
    print(res.stderr[:1500])
    raise SystemExit('ABBRUCH: node konnte den Code nicht ausfuehren')

out = json.loads(res.stdout)
print()
print(f"Alle Spiele         : {out['gesamt']}")
print(f"davon Coupe         : {out['nurCoupe']}")
print(f"Ohne COUPE:-Praefix : {out['ohneCoupe']}")
print()
print('Zuordnung Coupe -> Mannschaft:')
for z in out['zuordnung']:
    print(f"  {z['datum']:16} {z['team']:26} -> {z['key']}")
print()
print('Text fuer den Postergenerator:')
for zeile in out['text'].split('\n'):
    print('   ', zeile)

fehler = []
if out['nurCoupe'] != out['gesamt']:
    fehler.append('nicht alle Spiele tragen das COUPE:-Praefix')
if not out['text'].strip():
    fehler.append('der Coupe-Text ist leer')

u15 = [z for z in out['zuordnung']
       if '03.10.26' in z['datum'] and 'U15' in z['team']]
if u15 and u15[0]['key'] != 'u15':
    fehler.append(f"das U15-Spiel vom 03.10.26 landet auf {u15[0]['key']!r} "
                  f"statt auf 'u15'")

print()
if fehler:
    print('BEFUNDE:')
    for f in fehler:
        print('  -', f)
    raise SystemExit(1)

print('Hinweis zur Zuordnung - nicht automatisch pruefbar:')
print('  Coupe U13 -> "u13p1" ist eine ANNAHME des Codes. Die FLH fuehrt')
print('  den Wettbewerb als "U13 MIXTE (U13M-C)". Ob ein Coupe-Spiel in')
print('  das P1-Poster gehoert, muss das Secretariat entscheiden.')
raise SystemExit(0)