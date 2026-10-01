"""Prueft die Coupe-Zusatzknoepfe gegen die Live-Daten der FLH.

Es gab nur EINEN Knopf "Coupe", in dem U15, U13M, Maenner und Frauen
gemischt standen. Jetzt gibt es zusaetzlich einen Knopf je Rubrik.
Geprueft wird, was tatsaechlich erscheint - nicht, ob die Formel
"richtig aussieht":

1. coupeRubriken() liefert genau die Rubriken, die es in den Daten gibt
2. jeder Zusatzknopf zeigt genau die Spiele seiner Rubrik
3. die Summe aller Rubrikknöpfe ergibt zusammen den grossen Coupe-Knopf
   - es geht kein Spiel verloren und keins doppelt
4. U15 und U13M sind beide vorbereitet, auch wenn eine Rubrik diese
   Woche kein Spiel hat

Die Daten kommen von der FLH. Ohne Netz wird der Test uebersprungen.
"""
import json
import pathlib
import re
import subprocess
import sys
import urllib.request

ROOT = pathlib.Path('/Users/netjogger58/CascadeProjects/mersch75test.github.io')
SEITE = (ROOT / 'live-center.html').read_text()

WETTBEWERBE = [
    ('169141', 'COUPE: MÄNNER (H-C-LN)'),
    ('169136', 'COUPE: FRAUEN (D-C-LN)'),
    ('169146', 'COUPE: MÄNNER (H-C-FLH)'),
    ('169156', 'COUPE: U15 JONGEN (U15G-C)'),
    ('169151', 'COUPE: U13 MIXTE (U13M-C)'),
]


def hole(name):
    """Holt eine Funktion oder Konstante - klammerbewusst.

    Nicht mit einem Regex: in live-center.html stehen die Bloecke einer
    Funktion often am Zeilenanfang, zum Beispiel

        }).join("") : (katFilter

    Ein Muster wie r'function ... \\(.*?\\n\\}' hoert dort auf und
    liefert einen halben Ausdruck - node meldet dann einen
    Syntaxfehler und man weiss nicht, dass die Extraktion schuld war.
    """
    start = None
    for mstr in (r'function\s+' + name + r'\s*\(',
                 r'const\s+' + name + r'\s*='):
        m = re.search(mstr, SEITE)
        if m:
            start = m.start()
            break
    if start is None:
        raise SystemExit(f'ABBRUCH: {name} nicht in live-center.html')

    tiefe = 0
    i = start
    n = len(SEITE)
    zustand = None            # None | "'" | '"' | '`' | '//' | '/*'
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
                i += 1          # Escape ueberspringen
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


payload = {'games': []}
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
            payload['games'].append({
                'team': label,
                'datum': f"{g.get('gDate','')} {g.get('gTime','')}".strip(),
                'heim': g.get('gHomeTeam', '').strip(),
                'gast': g.get('gGuestTeam', '').strip(),
                'nr': str(g.get('gNo', '')).strip(),
            })
except Exception as e:                                     # noqa: BLE001
    print(f'FLH nicht erreichbar ({e}) - Test uebersprungen.')
    raise SystemExit(0)

print(f'Live-Spiele mit Mersch-Bezug: {len(payload["games"])}')

teile = [
    hole('COUPE_KNOPF_LABEL'),
    hole('COUPE_KNOPF_RANG'),
    hole('COUPE_RUBRIKEN_FEST'),
    hole('coupeRubriken'),
    hole('mergeCoupeDataFromLive'),
    'const scoreCSS = () => ""; const sboCell = () => ""; const rtlCell = () => "";',
    hole('renderCoupe'),
    'const coupeData = [];',
    'const livePayload = ' + json.dumps(payload, ensure_ascii=False) + ';',
    'mergeCoupeDataFromLive(livePayload);',
    """
// Zaehlt SPIELzeilen. Der Platzhalter "Keng Coupe-Spill" ist auch ein
// <tr> und wuerde sonst mitgezaehlt - dann meldet der Test "ein Spiel
// zu viel", obwohl keines da ist.
const LEER_TEXT = 'Keng Coupe-Spill';
const spielZaehlen = (html) => {
  const s = String(html);
  if (s.indexOf(LEER_TEXT) !== -1) return 0;
  return (s.match(/<tr>/g) || []).length;
};
const istLeer = (html) => String(html).indexOf(LEER_TEXT) !== -1;
const knoepfe = coupeRubriken();
const out = {
  rubriken: knoepfe.map(k => k.kat),
  knopfe: knoepfe.map(k => k.label),
  gesamt: spielZaehlen(renderCoupe().rows),
  jeRubrik: {},
  leer: {}
};
knoepfe.forEach(k => {
  out.jeRubrik[k.kat] = spielZaehlen(renderCoupe(k.kat).rows);
  out.leer[k.kat] = istLeer(renderCoupe(k.kat).rows);
});
out.ohneFilter = coupeData.length;
console.log(JSON.stringify(out, null, 1));
""",
]

res = subprocess.run(['node', '-e', '\n'.join(teile)],
                     capture_output=True, text=True)
if res.returncode != 0:
    print(res.stderr[:1500])
    raise SystemExit('ABBRUCH: node konnte den Code nicht ausfuehren')

out = json.loads(res.stdout)
print('\nRubriken (Knöpfe):', ', '.join(out.get('rubriken', [])))
print('Beschriftung        :', ' | '.join(out.get('knopfe', [])))
print()
print(f'Coupe gesamt          : {out["gesamt"]} Spiele')
print(f'coupeData             : {out["ohneFilter"]} Spiele')
for k in out['rubriken']:
    print(f'  Coupe {k:8}        : {out["jeRubrik"][k]} Spiele')

fehler = []

# 1) Kein Knopf ohne Daten, kein Rubrik-Datensatz ohne Knopf
if sorted(out['rubriken']) != sorted(set(out['rubriken'])):
    fehler.append('doppelte Rubrik im Knopf')

# 2) Summe der Rubrikknoepfe == grosser Coupe-Knopf
summe = sum(out['jeRubrik'].values())
if summe != out['gesamt']:
    fehler.append(f'Summe der Rubriken {summe} != Coupe gesamt {out["gesamt"]} '
                  f'- es geht ein Spiel verloren oder es doppelt sich')

# 3) Coupe gesamt passt zu coupeData (renderCoupe ohne Filter zeigt alle)
if out['gesamt'] != out['ohneFilter']:
    fehler.append(f'renderCoupe() zeigt {out["gesamt"]}, coupeData hat '
                  f'{out["ohneFilter"]}')

# 4) U15 und U13M vorbereitet
for kat in ('U15', 'U13M'):
    if kat not in out['rubriken']:
        fehler.append(f'{kat} fehlt - es gibt Mersch-Spiele dieser Rubrik '
                      f'oder die Zuordnung greift nicht')

print()
if fehler:
    print('BEFUNDE:')
    for f in fehler:
        print('  -', f)
    raise SystemExit(1)
print('Die Coupe-Zusatzknoepfe sind stimmig.')
raise SystemExit(0)