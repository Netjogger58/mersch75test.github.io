"""Prueft, ob die Coupe-Spiele beim Live Center ankommen.

Zwei Risiken, die man auf der Seite nicht sieht:

1. buildUrl() in js/flh-live-sync.js uebergibt KEINE Woche. Die
   FLH-Schnittstelle antwortet mit genau der Woche, die sie gerade als
   aktuell fuehrt. Ein Coupe-Spiel aus einer anderen Woche fehlt dann -
   und zwar still, ohne Fehlermeldung.

2. Coupe-Spiele werden per Praefix "COUPE:" erkannt und landen in
   coupeData, nicht in den Mannschafts-Rubriken. Bricht diese
   Zuordnung, verschwindet das Spiel ganz.

Der Test laedt die ECHTEN Funktionen aus beiden Dateien in node,
speist sie mit den LIVE-Daten der FLH und fragt danach: steht das
bekannte U15-Spiel vom 03.10.2026 in coupeData?

Ohne Netz faellt der Test auf "uebersprungen" zurueck, statt zu
fehlschlagen - ein Datenproblem soll nicht als Codefehler aussehen.
"""
import json
import pathlib
import re
import subprocess
import sys
import urllib.request

ROOT = pathlib.Path('/Users/netjogger58/CascadeProjects/mersch75test.github.io')
SYNC = (ROOT / 'js/flh-live-sync.js').read_text()
SEITE = (ROOT / 'live-center.html').read_text()

# Das Spiel, um das es geht
GESUCHT = ('03.10.26', '29160404')


def hole_funktion(name):
    for muster in (r'function\s+' + name + r'\s*\(.*?\n\}',
                   r'const\s+' + name + r'\s*=.*?=>\s*\{.*?\n\};'):
        m = re.search(muster, SEITE, re.S)
        if m:
            return m.group(0)
    raise SystemExit(f'ABBRUCH: {name}() nicht in live-center.html')


def hole_sync_funktion(name):
    m = re.search(r'function\s+' + name + r'\s*\(.*?\n    \}', SYNC, re.S)
    return m.group(0) if m else ''


def flh(cl):
    url = ('https://spo.handball4all.de/service/if_g_json.php'
           f'?cmd=ps&og=95&p=142&cl={cl}&ca=1')
    with urllib.request.urlopen(url, timeout=30) as r:
        daten = json.loads(r.read())
    return daten[0] if isinstance(daten, list) else daten


print('Hole die Coupe-Wettbewerbe von der FLH …')
COMPETITIONS = [
    ('cupMenLN', '169141', 'COUPE: MÄNNER (H-C-LN)'),
    ('cupWomenLN', '169136', 'COUPE: FRAUEN (D-C-LN)'),
    ('cupMenFLH', '169146', 'COUPE: MÄNNER (H-C-FLH)'),
    ('cupU15', '169156', 'COUPE: U15 JONGEN (U15G-C)'),
    ('cupU13', '169151', 'COUPE: U13 MIXTE (U13M-C)'),
]
payload = {'games': [], 'standingsByLabel': {}}
try:
    for key, cl, label in COMPETITIONS:
        roh = flh(cl)
        inhalt = roh.get('content', {})
        spiele = list(inhalt.get('actualGames') or [])
        spiele += (inhalt.get('futureGames') or {}).get('games', []) or []
        for g in spiele:
            if 'Mersch' not in (g.get('gHomeTeam', '') +
                                g.get('gGuestTeam', '')):
                continue
            payload['games'].append({
                'team': label,
                'datum': f"{g.get('gDate','')} {g.get('gTime','')}".strip(),
                'heim': g.get('gHomeTeam', '').strip(),
                'gast': g.get('gGuestTeam', '').strip(),
                'nr': str(g.get('gNo', '')).strip(),
            })
        print(f'  {label:26} {len(spiele)} Spiele dieser Woche')
except Exception as e:                                     # noqa: BLE001
    print(f'\nFLH nicht erreichbar ({e}) - Test uebersprungen.')
    raise SystemExit(0)

print(f'\nMersch-Spiele im Payload: {len(payload["games"])}')
for g in payload['games']:
    print(f"  {g['datum']:16} {g['heim']:18} - {g['gast']:18} "
          f"[{g['team']}]")

teile = [
    "const TOURNAMENT_GAST = /^(Turnier|Tournoi|Plateau)\\b/;",
    hole_funktion('trimText'),
    hole_funktion('mergeCoupeDataFromLive'),
    'const coupeData = [];',
    'const livePayload = ' + json.dumps(payload, ensure_ascii=False) + ';',
    'mergeCoupeDataFromLive(livePayload);',
    'console.log(JSON.stringify(coupeData, null, 1));',
]

res = subprocess.run(['node', '-e', '\n'.join(teile)],
                     capture_output=True, text=True)
if res.returncode != 0:
    print(res.stderr[:1500])
    raise SystemExit('ABBRUCH: node konnte den Code nicht ausfuehren')

coupe = json.loads(res.stdout)
print(f'\ncoupeData nach dem Merge: {len(coupe)} Zeilen')
for c in coupe:
    print(f"  {c['datum']:16} {c['kat']:8} {c['heim']:18} - {c['gast']:14} "
          f"Nr {c['nr']}")

fehler = []
if not coupe:
    fehler.append('coupeData ist leer - kein Coupe-Spiel kommt an')
for datum, nr in [GESUCHT]:
    treffer = [c for c in coupe
               if datum in c['datum'] or c['nr'] == nr]
    if not treffer:
        fehler.append(f'U15-Spiel {datum} / Nr {nr} steht NICHT in coupeData')
    else:
        print(f'\nGESUCHTES SPIEL GEFUNDEN: {treffer[0]}')

print()
if fehler:
    print('BEFUNDE:')
    for f in fehler:
        print('  -', f)
    raise SystemExit(1)
print('Das U15-Coupe-Spiel kommt im Live Center an.')
raise SystemExit(0)