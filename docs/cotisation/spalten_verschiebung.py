"""Bildet ab, wohin die Spalten durch den Einfueg von vier Spalten
nach AX gewandert sind.

Der Kern: In den Formeln sind die Spalten buchstabenweise fest kodiert
(BV, CC, CL ...). Wer vier Spalten vor AX einfuegt, verschiebt damit
jede nachfolgende Spalte um vier. Wer die Formeln nicht anpasst, laeuft
in die falsche Spalte - und merkt es nicht, weil die Formel syntaktisch
voellig in Ordnung ist.

Verglichen wird die Kopfzeile der neuen Datei mit der Kopfzeile, die
vor dem Einfuegen existierte (festgehalten in der alten Sicherung).
"""
import sys
import zipfile

sys.path.insert(0, '/Users/netjogger58/CascadeProjects/mersch75test.github.io/'
                   'docs/cotisation')
import mappe  # noqa: E402
import baut_arbeitsmappe as ba  # noqa: E402

ALT = ('/Users/netjogger58/CascadeProjects/Vereins-OS/docs/'
       'GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.regeln-2026-09-29_vor-E7E8.xlsm')


def kopf(pfad):
    with zipfile.ZipFile(pfad) as z:
        teile = {n: z.read(n) for n in z.namelist()}
    return [c.strip() for c in ba.liese_blatt(teile, 'xl/worksheets/sheet1.xml')[0]]


def spaltenname(i):
    """0-basierter Index -> Excel-Buchstabe."""
    s = ''
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


neu = kopf(mappe.datenquelle())
alt = kopf(ALT)

print('ALT:', len(alt), 'Spalten | NEU:', len(neu), 'Spalten')
print()

position = {}
neu_idx = {}
for i, h in enumerate(neu):
    neu_idx.setdefault(h, i)

print('%-6s %-40s %-6s %s' % ('ALT', 'NAME', 'NEU', 'DIFF'))
print('-' * 72)
for i, h in enumerate(alt):
    j = neu_idx.get(h)
    if j is None:
        continue
    position[spaltenname(i)] = spaltenname(j)
    if j != i:
        print('%-6s %-40s %-6s %+d' % (spaltenname(i), h[:40],
                                      spaltenname(j), j - i))

print()
print('NEU eingefuegt (kein Gegenstueck in der alten Kopfzeile):')
alt_namen = set(alt)
for i, h in enumerate(neu):
    if h and h not in alt_namen:
        print('  %-6s %s' % (spaltenname(i), h))

print()
print('Nicht verschoben geblieben:')
unver = [spaltenname(i) for i, h in enumerate(alt)
         if neu_idx.get(h) == i and h]
print(' ', ', '.join(unver))
