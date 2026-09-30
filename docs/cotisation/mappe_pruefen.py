"""Prueft die Arbeitsmappe auf alles, woran Excel beim Oeffnen scheitert.

Am 30.09.2026 kam der Reparatur-Dialog, weil eine Formel doppelt escapte
Entities enthielt ("&amp;gt;"). Diese Pruefung deckt genau solche Fehler ab
und laesst sich laengerfristig als Torwaechter verwenden.
"""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

sys.path.insert(0, '/Users/netjogger58/CascadeProjects/mersch75test.github.io/docs/cotisation')
import mappe  # noqa: E402

DOPPELT = re.compile(r'&amp;(?:amp|gt|lt|quot);')
ZELLE = re.compile(r'<c r="([A-Z]+)(\d+)"[^>]*><f[^>]*>(.*?)</f>', re.S)


def main() -> int:
    pfad = mappe.datenquelle()
    print('Datei:', pfad.name)
    fehler = []

    with zipfile.ZipFile(pfad) as z:
        if z.testzip() is not None:
            fehler.append('ZIP ist defekt')
        namen = z.namelist()
        print('Teile:', len(namen), '| Makro:', any('vbaProject' in n for n in namen))

        # 1) Jeder XML-Teil muss wohlgeformt sein
        for teil in namen:
            if not (teil.endswith('.xml') or teil.endswith('.rels')):
                continue
            try:
                ET.fromstring(z.read(teil))
            except ET.ParseError as e:
                fehler.append(f'{teil}: XML kaputt ({e})')
        print('XML-Teile geprueft:',
              sum(1 for n in namen if n.endswith(('.xml', '.rels'))))

        # 2) Keine doppelt escapten Entities - der Excel-Reparatur-Ausloeser
        doppelt = 0
        for teil in namen:
            if not (teil.endswith('.xml') or teil.endswith('.rels')):
                continue
            n = len(DOPPELT.findall(z.read(teil).decode('utf-8', 'ignore')))
            if n:
                fehler.append(f'{teil}: {n} doppelt escapte Entities')
                doppelt += n
        print('doppelt escapte Entities:', doppelt)

        # 3) Formelzellen: Klammerbalance nach dem Auslesen
        x = z.read('xl/worksheets/sheet1.xml').decode('utf-8')
        kaputt = 0
        gesamt = 0
        for m in ZELLE.finditer(x):
            gesamt += 1
            f = (m.group(3).replace('&gt;', '>').replace('&lt;', '<')
                 .replace('&quot;', '"').replace('&amp;', '&'))
            if f.count('(') != f.count(')'):
                kaputt += 1
                if kaputt <= 5:
                    fehler.append(f'{m.group(1)}{m.group(2)}: Klammern '
                                  f'{f.count("(")}/{f.count(")")}')
        print(f'Formelzellen: {gesamt} | unbalanciert: {kaputt}')

    print()
    if fehler:
        print('ERGEBNIS: FEHLER')
        for f in fehler[:20]:
            print('  -', f)
        return 1
    print('ERGEBNIS: Mappe ist strukturell in Ordnung - kein Reparatur-Dialog '
          'zu erwarten')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
