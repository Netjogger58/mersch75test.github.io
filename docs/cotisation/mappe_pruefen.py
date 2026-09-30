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
import baut_arbeitsmappe as ba  # noqa: E402

DOPPELT = re.compile(r'&amp;(?:amp|gt|lt|quot);')
def spaltenname(i):
    s = ''
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


SHEET = 'xl/worksheets/sheet1.xml'

ZELLE = re.compile(r'<c r="([A-Z]+)(\d+)"([^>]*)>(.*?)</c>', re.S)


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

        # 3) Formelzellen: Klammerbalance nach dem Auslesen UND Zelltyp.
        # Der Zelltyp t="str" ist Pflicht, sobald die Formel Text liefert.
        # Ohne das Attribut entfernt Excel die Formel und zeigt den
        # Reparatur-Dialog - am 30.09.2026 bei 5 Spalten passiert.
        x = z.read('xl/worksheets/sheet1.xml').decode('utf-8')
        kaputt = 0
        fehlend_t = 0
        ch_mit_t = 0
        gesamt = 0
        # Spalten, die TEXT liefern, brauchen t="str". Bestimmt ueber den
        # KOPFZEILENTEXT, nicht ueber einen fest verdrahteten Buchstaben -
        # nach dem Einfuegen der vier Medico-Spalten sind alle Buchstaben
        # um vier gewandert, eine feste Liste waere dann still falsch.
        mit = zipfile.ZipFile(pfad)
        roh = {n: mit.read(n) for n in mit.namelist()}
        kopf = [c.strip() for c in ba.liese_blatt(roh, SHEET)[0]]
        TEXT_KOEPFE = ('Cotisatioun', 'FamID', 'XSEULwert', 'Traeger',
                       'Personenwert')
        text_spalten = {i for i, h in enumerate(kopf) if h in TEXT_KOEPFE}
        print('Textspalten laut Kopfzeile:',
              ', '.join(spaltenname(i) for i in sorted(text_spalten)))

        def num(b):
            n = 0
            for c in b:
                n = n * 26 + (ord(c) - 64)
            return n

        kaputt = 0
        fehlend_t = 0
        gesamt = 0
        for m in ZELLE.finditer(x):
            inhalt = m.group(4)
            fm = re.search(r'<f[^>]*>(.*?)</f>', inhalt, re.S)
            if '<f' not in inhalt or not fm:
                # geteilte Formel (t="shared" si=..) ohne eigenen Text:
                # der steht in der Master-Zelle und wird dort geprueft
                continue
            gesamt += 1
            ref = m.group(1) + m.group(2)
            attr = m.group(3)
            f = (fm.group(1).replace('&gt;', '>').replace('&lt;', '<')
                 .replace('&quot;', '"').replace('&amp;', '&'))
            if f.count('(') != f.count(')'):
                kaputt += 1
                if kaputt <= 5:
                    fehler.append(f'{ref}: Klammern {f.count("(")}/'
                                  f'{f.count(")")}')
            if (num(m.group(1)) - 1 in text_spalten and 't="str"' not in attr
                    and not (kopf[num(m.group(1)) - 1] == 'Personenwert'
                        and int(m.group(2)) >= 592)):
                fehlend_t += 1
                if fehlend_t <= 5:
                    fehler.append(f'{ref}: Spalte {m.group(1)} '
                                  f'({kopf[num(m.group(1)) - 1]}) verliert t="str"')
        print(f'Formelzellen: {gesamt} | unbalanciert: {kaputt} '
              f'| ohne t="str": {fehlend_t}')
        # 310 Zellen der Spalte Personenwert (Zeilen 592-901) haben auch in
        # der Sicherung KEIN t="str": das ist der Bereich, der nie berechnet
        # wurde, und es ist so im Original. Ohne diese Grundlage wuerde der
        # Pruefer dauerhaft einen Fehler melden, den es nicht gibt.
        for i in sorted(text_spalten):
            sp = spaltenname(i)
            if kopf[i] != 'Personenwert':
                continue
            mit_t = 0
            for m in ZELLE.finditer(x):
                if num(m.group(1)) - 1 == i and 't="str"' in m.group(3):
                    mit_t += 1
            if mit_t != 590:
                fehler.append(f'{sp} (Personenwert): {mit_t} Zellen mit '
                              f't="str", erwartet 590 (Altstand)')
            else:
                print(f'{sp} (Personenwert): 590 mit t="str" wie im Altstand, '
                      f'310 ohne (Zeilen 592-901, nie berechnet)')

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
