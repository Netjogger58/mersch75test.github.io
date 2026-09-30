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


def buchstabe(i):
    s = ''
    n = i + 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def kopfzeile(blatt):
    kopf = ba.liese_blatt(teile, blatt)[0]
    return {buchstabe(i): h.replace('\n', ' ') for i, h in enumerate(kopf)
            if h}


# Die Anleitung beschreibt MEHRERE Blaetter: Teil 1 und 2 das Hauptblatt,
# Teil 3 das Blatt Stripe_Export. Gegen immer nur das Hauptblatt zu
# pruefen war falsch - jede Stripe-Spalte wurde als Abweichung gemeldet,
# obwohl sie voellig richtig ist.
#
# Geprueft wird darum gegen ALLE Blaetter. Eine Angabe gilt als
# bestaetigt, sobald der Name in einem Blatt an dieser Stelle steht.
# Ein Tippfehler, der in keinem Blatt vorkommt, faellt weiter auf.
BLATT = {
    'A': 'xl/worksheets/sheet1.xml',   # Membres 2026_2027
    'B': 'xl/worksheets/sheet3.xml',   # Stripe_Export
    'C': 'xl/worksheets/sheet2.xml',   # Cotisatiounen
}
koepfe = {k: kopfzeile(v) for k, v in BLATT.items()}
print('Kopfzeilen geladen:', ', '.join(koepfe))

text = P.read_text()
geprueft = 0
fehler = []
for nr, zeile in enumerate(text.split('\n'), start=1):
    # Tabellenzeilen: | **BX** | `Comite` | ... |
    for m in re.finditer(r'\| \*\*([A-Z]{1,2})\*\* \| `([^`]+)`', zeile):
        sp, name = m.group(1), m.group(2)
        geprueft += 1
        gefunden = [b for b, k in koepfe.items()
                    if name[:12].lower() in k.get(sp, '(leer)').lower()]
        if not gefunden:
            moeglich = {b: k.get(sp, '(leer)') for b, k in koepfe.items()}
            fehler.append(f'Zeile {nr}: {sp} heisst {moeglich}, '
                          f'nicht "{name}"')
        elif 'A' not in gefunden:
            print(f'  Zeile {nr}: {sp} = "{name}" stammt aus Blatt '
                  f'{gefunden} (nicht dem Hauptblatt)')

print(f'\nGeprueft: {geprueft} Spaltenangaben der Form "**XX** | `Name`"')
if fehler:
    print('ABWEICHUNGEN:')
    for f in fehler:
        print('  -', f)
else:
    print('alle stimmen mit einer echten Kopfzeile ueberein')

alt = 'GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm'
if alt in text:
    print('WARNUNG: veralteter Dateiname noch in der Anleitung')
    fehler.append('veralteter Dateiname')
elif 'GC 2026-10-01' in text:
    print('Dateiname: aktuell')

raise SystemExit(1 if fehler else 0)