"""Prueft die Anleitung gegen die tatsaechliche Kopfzeile.

Der Fehler, den man an einer Anleitung nicht sieht: ein Verweis, der auf
eine existierende, aber ANDERE Spalte zeigt. Er liest sich vollstaendig
korrekt und fuehrt trotzdem in die Irre - nach dem Einfuegen der vier
Medico-Spalten zeigen die alten Buchstaben genau dorthin.

Geprueft wird gegen die Kopfzeile, nicht gegen eine Liste, was "richtig"
sein sollte. Die Kopfzeile ist die Wahrheit.
"""
import pathlib
import re
import sys
import zipfile

sys.path.insert(0, '/Users/netjogger58/CascadeProjects/mersch75test.github.io/'
                   'docs/cotisation')
import mappe  # noqa: E402
import baut_arbeitsmappe as ba  # noqa: E402

P = pathlib.Path('/Users/netjogger58/CascadeProjects/Vereins-OS/docs/'
                 'ANLEITUNG-Cotisation-Tresorier.md')

with zipfile.ZipFile(mappe.datenquelle()) as z:
    teile = {n: z.read(n) for n in z.namelist()}
kopf = [c.strip() for c in ba.liese_blatt(teile, 'xl/worksheets/sheet1.xml')[0]]


def buchstabe(i):
    s = ''
    n = i + 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


inhalt = {buchstabe(i): h.replace('\n', ' ') for i, h in enumerate(kopf) if h}

text = P.read_text()
geprueft = 0
fehler = []
for nr, zeile in enumerate(text.split('\n'), start=1):
    # Tabellenzeilen der Hilfsspalten: | **BX** | `Comite` | ... |
    for m in re.finditer(r'\| \*\*([A-Z]{1,2})\*\* \| `([^`]+)`', zeile):
        sp, name = m.group(1), m.group(2)
        geprueft += 1
        ist = inhalt.get(sp, '(leer)')
        if name[:12].lower() not in ist.lower():
            fehler.append(f'Zeile {nr}: {sp} heisst "{ist}", '
                          f'nicht "{name}"')

print(f'Geprueft: {geprueft} Spaltenangaben der Form "**XX** | `Name`"')
if fehler:
    print('ABWEICHUNGEN:')
    for f in fehler:
        print('  -', f)
else:
    print('alle stimmen mit der Kopfzeile ueberein')

alt = 'GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm'
if alt in text:
    print('WARNUNG: veralteter Dateiname noch in der Anleitung')
    fehler.append('veralteter Dateiname')
elif 'GC 2026-10-01' in text:
    print('Dateiname: aktuell')

raise SystemExit(1 if fehler else 0)