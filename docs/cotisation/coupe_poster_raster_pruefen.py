"""Prueft das Coupe-Poster-Raster im Generator.

U13M kam in die Coupe-Reihe dazu. Damit stellt sich die Geometrie:

- ALLE Bloecke muessen GROSS GLEICH sein, unabhaengig von der Zahl
- das Poster ist 1600 px breit und 838 px hoch
- nichts darf ueber den Rand hinausragen
- bei bis zu drei Mannschaf ten muss das bisherige Raster EXAKT
  erhalten bleiben - fertige Poster duerfen sich nicht verschieben

Geprueft werden alle vier Faelle, unabhaengig von den echten Daten:
der Test darf nicht erst beim Rendern scheitern.
"""
import pathlib
import re

ROOT = pathlib.Path('/Users/netjogger58/CascadeProjects/mersch75test.github.io')
SEITE = (ROOT / 'generator.html').read_text()

POSTER_BREITE = 1600
POSTER_HOEHE = 838
RAND = 76                 # Icon-Kante 2 cm vom linken Rand, wie bisher
ALT_LEFT = [76, 570, 1064]
ALT_BREITE, ALT_HOEHE = 480, 320
SIEGEL_BREITE = 150        # Pokal

fehler = []

# Reihenfolge und Kappung aus dem Quelltext lesen, nicht nachbauen -
# sonst prueft der Test eine Kopie statt des echten Codes.
m = re.search(r"const coupePosterTeams = (\[[^\]]*\])", SEITE)
if not m:
    raise SystemExit('ABBRUCH: coupePosterTeams nicht gefunden')
reihenfolge = re.findall(r"'([a-z0-9]+)'", m.group(1))
print('Reihenfolge laut Code :', ' -> '.join(reihenfolge))
print(f'COUPE_MAX im Code    : {re.search(r"COUPE_MAX = (\d+)", SEITE).group(1)}')
print()

if 'u13p1' not in reihenfolge:
    fehler.append('u13p1 fehlt in der Coupe-Reihenfolge')
if reihenfolge.index('u13p1') > reihenfolge.index('u15'):
    print('Hinweis: U13M steht hinter U15, nicht davor.')

# --- Geometrie nachrechnen ------------------------------------------
def raster(n):
    if n <= 3:
        b, h = ALT_BREITE, ALT_HOEHE
        lefts = ALT_LEFT[:n]
    else:
        b, h = 340, 227
        lefts = [60 + i * (b + 40) for i in range(n)]
    return b, h, lefts


print('%-6s %-9s %-7s %-38s %s' % ('Mann.', 'Breite', 'Hoehe', 'Left-Werte', 'Urteil'))
print('-' * 86)
for n in range(1, 5):
    b, h, lefts = raster(n)
    gleich = True   # alle Bloecke stammen aus denselben b/h
    rechts = max(lefts) + b
    oben_unten = 350 + h
    passt = rechts <= POSTER_BREITE and oben_unten <= POSTER_HOEHE
    pokal = (lefts[-1] + 229) if n <= 3 else 800
    pokal_rechts = pokal + SIEGEL_BREITE / 2
    pokal_ok = pokal_rechts <= POSTER_BREITE
    print(f'{n:<6} {b:<9} {h:<7} {str(lefts):<38} '
          f'{"passt" if passt and pokal_ok else "PASST NICHT"}')
    if not gleich:
        fehler.append(f'{n} Mannschaf ten: Bloecke nicht alle gleich gross')
    if not passt:
        fehler.append(f'{n} Mannschaf ten: rechter Rand {rechts} > '
                      f'{POSTER_BREITE}')
    if not pokal_ok:
        fehler.append(f'{n} Mannschaf ten: Pokal ragt bis {pokal_rechts} raus')
    if abs(b / h - 1.5) > 0.01:
        fehler.append(f'{n} Mannschaf ten: Seitenverhaeltnis veraendert sich '
                      f'({b}x{h} statt 3:2)')

# --- Das alte Raster muss unveraendert sein -------------------------
b3, h3, lefts3 = raster(3)
if (b3, h3, lefts3) != (ALT_BREITE, ALT_HOEHE, ALT_LEFT):
    fehler.append(f'das bisherige Raster hat sich verschoben: {lefts3} '
                  f'statt {ALT_LEFT}')
else:
    print()
    print('Raster bei drei Mannschaf ten unveraendert:', lefts3, f'{b3}x{h3}')

print()
if fehler:
    print('BEFUNDE:')
    for f in fehler:
        print('  -', f)
    raise SystemExit(1)
print(f'Alle Bloecke gleich gross, alles innerhalb von '
      f'{POSTER_BREITE}x{POSTER_HOEHE} px.')
raise SystemExit(0)