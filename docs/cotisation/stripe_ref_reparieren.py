"""Repariert die beiden Zeilen mit #REF! im Blatt Stripe_Export.

Befund: in Zeile 206 und 590 sind saemtliche Verweise auf
'Membres 2026_2027' zu #REF! geworden. Die Zeilen ergeben damit
gar nichts - kein Haushalt, keinen Namen, keinen Betrag. Zwei
Posten fallen still aus der Rechnung, ohne dass irgendwo ein
Warnzeichen erscheint.

Die Formeln werden nicht erraten, sondern von einer gesunden Zeile
uebernommen und nur die Zeilennummer angepasst. Genau so, wie es
beim Kopieren einer Zeile in Excel passiert.

SICHER: ohne --apply wird nichts geschrieben.
"""
import argparse
import pathlib
import re
import sys
import zipfile

sys.path.insert(0, '/Users/netjogger58/CascadeProjects/mersch75test.github.io/'
                   'docs/cotisation')

DATEI = ('/Users/netjogger58/CascadeProjects/Vereins-OS/docs/'
         'GC 2026-10-01 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm')
BLATT = 'xl/worksheets/sheet3.xml'
KAPUTT = (206, 590)


def repariere(x: str, vorlage: dict) -> tuple:
    geaendert = 0
    for ziel in KAPUTT:
        for spalte, formel in vorlage.items():
            alt = re.search(r'<c r="%s%d"[^>]*>.*?</c>' % (spalte, ziel), x, re.S)
            neu = re.search(r'<c r="%s%d"[^>]*>.*?</c>' % (spalte, ziel), x, re.S)
            if not alt or not neu:
                continue
            neu_text = formel.replace('{z}', str(ziel))
            if neu_text != alt.group(0):
                x = x[:alt.start()] + neu_text + x[alt.end():]
                geaendert += 1
    return x, geaendert


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    with zipfile.ZipFile(DATEI) as z:
        teile = {n: z.read(n) for n in z.namelist()}
    x = teile[BLATT].decode('utf-8')

    vorlage = {}
    for ziel in KAPUTT:
        for m in re.finditer(r'<c r="([A-M])%d"([^>]*)>(.*?)</c>' % ziel, x, re.S):
            fm = re.search(r'<f[^>]*>(.*?)</f>', m.group(3), re.S)
            if not fm or '#REF!' not in fm.group(1):
                continue
            print(f'  kaputt  {m.group(1)}{ziel}: {fm.group(1)[:70]}...')
        break

    # Vorlage aus einer gesunden Zeile: 2 (oder die erste ohne #REF!)
    gesund = None
    for nr in range(2, 902):
        zellen = {}
        gut = True
        for m in re.finditer(r'<c r="([A-M])(\d+)"([^>]*)>(.*?)</c>', x, re.S):
            if int(m.group(2)) != nr:
                continue
            fm = re.search(r'<f[^>]*>(.*?)</f>', m.group(4), re.S)
            zellen[m.group(1)] = (m.group(3), fm.group(1) if fm else None)
            if fm and '#REF!' in fm.group(1):
                gut = False
        if gut and zellen.get('A', ('', None))[1]:
            gesund = (nr, zellen)
            break
    if gesund is None:
        raise SystemExit('ABBRUCH: keine gesunde Vorlagezeile gefunden')
    nr, zellen = gesund
    print(f'\nVorlage aus Zeile {nr}:')

    vorlage = {}
    for spalte, (attr, formel) in zellen.items():
        if not formel:
            continue
        vorlage[spalte] = (f'<c r="{spalte}{{z}}"{attr}>'
                           f'<f>{formel}</f><v>0</v></c>')
    print(f'  {len(vorlage)} Spalten: {" ".join(sorted(vorlage))}')

    xneu, n = repariere(x, vorlage)
    print(f'\nZellen ersetzt: {n}')
    if not args.apply:
        print('Nichts geschrieben. Mit --apply wirklich reparieren.')
        return 0

    # Schutz: keine other Formel darf dabei verloren gehen
    alt_n = len(re.findall(r'<f[^>]*>', x))
    neu_n = len(re.findall(r'<f[^>]*>', xneu))
    if alt_n != neu_n:
        raise SystemExit(f'ABBRUCH: Formelzahl {alt_n} -> {neu_n}')
    if '#REF!' in xneu:
        raise SystemExit('ABBRUCH: es sind noch #REF! uebrig')

    sicherung = pathlib.Path(DATEI).with_suffix('.vor-ref-2026-10-01.xlsm')
    sicherung.write_bytes(pathlib.Path(DATEI).read_bytes())
    with zipfile.ZipFile(DATEI, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, daten in teile.items():
            z.writestr(name, xneu.encode('utf-8') if name == BLATT else daten)
    print(f'Sicherung: {sicherung.name}')
    print(f'Geschrieben: {n} Zellen in den Zeilen {KAPUTT}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())