"""Prueft die Zahlen im Tresorier-Teil (Teil 3) gegen die Datei.

Der Tresorier arbeitet nach festen Zahlen: 180 Posten, 39.168 Euro,
2 ohne E-Mail. Stimmen die nicht mehr, arbeitet jemand nach einer
veralteten Anleitung - und legt Links fuer Haushalte an, die es gar
nicht gibt.

Die Suche laeuft ueber die Zahl selbst, nicht ueber eine Wortliste:
wer den Satz umformuliert, soll die Pruefung nicht ausloesen, aber
auch nicht unbemerkt eine falsche Zahl durchschlupfen lassen.
"""
import pathlib
import re
import sys
import zipfile

sys.path.insert(0, '/Users/netjogger58/CascadeProjects/mersch75test.github.io/'
                   'docs/cotisation')
import baut_arbeitsmappe as ba  # noqa: E402

P = pathlib.Path('/Users/netjogger58/CascadeProjects/Vereins-OS/docs/'
                 'ANLEITUNG-Cotisation-Tresorier.md')
z = zipfile.ZipFile('/Users/netjogger58/CascadeProjects/Vereins-OS/docs/'
                    'GC 2026-10-01 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm')
t = {n: z.read(n) for n in z.namelist()}
doc = P.read_text()
fehler = []

teil3 = doc[doc.index('# TEIL 3'):] if '# TEIL 3' in doc else ''
if not teil3:
    print('FEHLER: Teil 3 nicht vorhanden')
    raise SystemExit(1)

r = ba.liese_blatt(t, 'xl/worksheets/sheet3.xml')
k = [c.strip() for c in r[0]]
i = {n: k.index(n) for n in k if k.count(n) == 1}
zeilen = [x for x in r[1:901] if (x[i['FamID']] or '').strip()]


def zahl(v):
    try:
        return float((v or '0').strip().replace(',', '.'))
    except ValueError:
        return None


mit_betrag = [x for x in zeilen if (zahl(x[i['Betrag_EUR']]) or 0) > 0]
summe = sum(zahl(x[i['Betrag_EUR']]) or 0 for x in mit_betrag)
ohne_mail = sum(1 for x in zeilen if not (x[i['Email']] or '').strip())
ohne_zahl = len(zeilen) - len(mit_betrag)

SOLL = {
    'Posten gesamt': str(len(zeilen)),
    'Posten mit Betrag': str(len(mit_betrag)),
    'Posten ohne Betrag': str(ohne_zahl),
    'Posten ohne E-Mail': str(ohne_mail),
    'Summe': f'{summe:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
}
print('Ist-Zustand aus der Datei:')
for name, wert in SOLL.items():
    print(f'  {name:22} {wert}')

# --- Jede Zahl pruefen: taucht sie irgendwo in Teil 3 auf? -------------
# Umgekehrt zaehlen: welche Zahlen nennt der Text ueberhaupt?
genannt = set(re.findall(r'(?<![\w.])\d{1,3}(?:[. ]\d{3})*(?:,\d+)?(?![\w])',
                         teil3))
erlaubt = {'1', '2', '3', '4', '5', '6', '10', '11', '12', '13', '14',
           '15', '16', '0', '50', '300', '384', '210', '20', '2026',
           '27', '2027', '2025', '2031', '2028', '900', '100', '0.00'}
print('\nZahlen aus der Datei, die im Text stehen muessen:')
for name, wert in SOLL.items():
    if name == 'Summe':
        # 39.168 darf auch als 39.168,00 geschrieben sein
        ok = ('39.168' in teil3) or wert in teil3
    else:
        ok = re.search(r'\b' + re.escape(wert) + r'\b', teil3) is not None
    print(f'  {name:22} {wert:10} {"ja" if ok else "NEIN"}')
    if not ok:
        fehler.append(f'{name} = {wert} kommt in Teil 3 nicht vor')

# --- Gegenprobe: nennt der Text eine Postenzahl, die es nicht gibt? ---
posten_texte = set()
for m in re.finditer(r'(\d+)\s+Posten', teil3):
    posten_texte.add(int(m.group(1)))
for m in re.finditer(r'(\d+)\s+Zeilen mit Betrag', teil3):
    posten_texte.add(int(m.group(1)))
print(f'\nIm Text genannte Postenzahlen: {sorted(posten_texte)}')
falsch = [p for p in posten_texte if p not in (len(zeilen), len(mit_betrag))]
if falsch:
    print('  ACHTUNG, nicht plausibel:', falsch)

# --- Kapitel 10-16 vorhanden? -----------------------------------------
fehl_kap = [n for n in range(10, 17)
            if not re.search(r'^## %d\. ' % n, teil3, re.M)]
if fehl_kap:
    fehler.append(f'Kapitel fehlen: {fehl_kap}')
else:
    print('Kapitel 10-16: alle vorhanden')

print()
if fehler:
    print('ABWEICHUNGEN:')
    for f in fehler:
        print('  -', f)
else:
    print('Teil 3 stimmt mit der Datei überein.')
raise SystemExit(1 if fehler else 0)