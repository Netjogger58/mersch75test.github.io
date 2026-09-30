"""Belegt, dass die Inapte-Sperre wirklich greift.

Zwei Wege:

1. Ist in den Daten bereits jemand markiert, wird gezeigt, was die
   Sperre bei ihm bewirkt.
2. Fuellt der erste Weg nichts - und das ist der Regelfall, denn aktuell
   traegt KNABBEN Joost zwar ein "x" in BA, hat aber gar kein Medico-Jahr
   in AX und waere also auch ohne die Markierung nicht berechtigt -, dann
   wird ein BEWIESENERMAESSEN BERECHTIGTER Spieler testweise markiert.
   Nur wenn er danach nicht mehr berechtigt ist, greift die Regel wirklich.

Der zweite Weg ist der eigentliche Nachweis: eine Regel, die niemanden
aendert, ist von einer, die nicht greift, nicht zu unterscheiden.
"""
import pathlib
import sys
import zipfile

sys.path.insert(0, '/Users/netjogger58/CascadeProjects/mersch75test.github.io/'
                   'docs/cotisation')
import mappe  # noqa: E402
import baut_arbeitsmappe as ba  # noqa: E402
import pruef_cotisation as pr  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent

with zipfile.ZipFile(mappe.datenquelle()) as z:
    teile = {n: z.read(n) for n in z.namelist()}
roh = ba.liese_blatt(teile, 'xl/worksheets/sheet1.xml')
kopf = [c.strip() for c in roh[0]]

i_in = kopf.index('Inapte')
i_tmp = kopf.index('Inapte temporaire (Date)')
i_sp = kopf.index('Spielt J/R/N/P')
i_vn = kopf.index('Nom(s)')
i_n = kopf.index('Prénom(s)')

tarife = pr.lade_tarife(HERE / 'tarife-cotisation.csv')[0]


def berechne(zeilen):
    erg = pr.berechne(zeilen, {}, tarife, False, 'Aelteste', False,
                      '(0+50)', [])
    return {x['excel_zeile']: x for x in erg}


basis = berechne(roh)
fehler = []

# --- 1) Bereits markierte Personen -------------------------------------
markiert = [n for n, z in enumerate(roh[1:], start=2)
            if (z[i_in] or '').strip() or (z[i_tmp] or '').strip()]
print('Bereits markiert:', len(markiert))
for n in markiert:
    print(f'  Z{n} {roh[n - 1][i_vn]} {roh[n - 1][i_n]} '
          f'-> {basis[n]["neu"]!r} ({basis[n]["grund"]})')

# --- 2) Nachweis an einem wirklich berechtigten Spieler -----------------
kandidaten = [n for n, z in enumerate(roh[1:], start=2)
              if (z[i_sp] or '').strip() == 'J'
              and not (z[i_in] or '').strip()
              and not (z[i_tmp] or '').strip()
              and basis[n]['ist_traeger']
              and basis[n]['neu'] not in ('', '0')]
print()
print('Berechtigte Spieler zur Gegenprobe:',
      len(kandidaten))
if not kandidaten:
    raise SystemExit('ABBRUCH: kein berechtigter Spieler zum Testen')

test_zeile = kandidaten[0]
print(f'Gegentest mit Z{test_zeile} {roh[test_zeile - 1][i_vn]} '
      f'{roh[test_zeile - 1][i_n]}: vorher {basis[test_zeile]["neu"]!r}')

kopie = list(roh)
k = list(roh[test_zeile - 1])
k[i_in] = 'x'
kopie[test_zeile - 1] = k
nachher = berechne(kopie)

vor = basis[test_zeile]['neu']
nach = nachher[test_zeile]['neu']
print(f'   nach dem Setzen von BA="x": {nach!r} '
      f'({nachher[test_zeile]["grund"]})')
if vor == nach:
    fehler.append('Die Sperre aendert nichts - sie greift nicht')
if nach not in ('', '0', None):
    fehler.append(f'Nach der Sperre weiterhin ein Betrag: {nach!r}')

print()
print('Ergebnis:', 'Sperre greift nachweislich' if not fehler else 'PROBLEM')
for f in fehler:
    print(' -', f)
raise SystemExit(1 if fehler else 0)