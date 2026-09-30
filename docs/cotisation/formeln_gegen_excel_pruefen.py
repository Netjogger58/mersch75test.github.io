"""Vergleicht FORMELN mit dem, was in der Datei steht.

Excel hat die Formeln beim Einfuegen der vier Medico-Spalten selbst
angepasst. Damit liegt eine unabhaengige Referenz vor: stimmt unsere
Fassung mit dem ueberein, was Excel gemacht hat, ist der Spaltenwechsel
korrekt.

Zwei Spalten sind absichtlich NICHT gleich:

- Spielberecht (CP): wir haben die BA/BB-Sperre ergaenzt, die im
  Original noch nicht stand. Dort wird nur geprueft, dass die BA/BB-Bedingung
  drin ist und der Rest unveraendert blieb.
- Alle anderen: hier muessen sie zeichengenau uebereinstimmen.
"""
import re
import sys
import zipfile

sys.path.insert(0, '/Users/netjogger58/CascadeProjects/mersch75test.github.io/'
                   'docs/cotisation')
import cotisation_regeln_setzen as cr  # noqa: E402
import mappe  # noqa: E402

with zipfile.ZipFile(mappe.datenquelle()) as z:
    x = z.read('xl/worksheets/sheet1.xml').decode('utf-8')


def holen(ref):
    m = re.search(r'<c r="%s"[^>]*>(?:<f[^>]*>(.*?)</f>)?' % ref, x, re.S)
    if not m or not m.group(1):
        return None
    return (m.group(1).replace('&gt;', '>').replace('&lt;', '<')
            .replace('&quot;', '"').replace('&amp;', '&'))


fehler = 0
geprueft = 0
print('%-5s %-16s %s' % ('SPALTE', 'NAME', 'STIMMT MIT EXCEL'))
print('-' * 60)
for spalte, name, formel in cr.FORMELN:
    soll = formel.format(r=10, e=cr.ERSTE, l=cr.LETZTE).lstrip('=')
    ist = holen(spalte + '10')
    if ist is None:
        print('%-5s %-16s keine Formel in der Datei' % (spalte, name))
        continue
    geprueft += 1
    if name == 'Spielberecht':
        # BA/BB-Sperre ergaenzt: Bedingung muss drin sein
        hat_sperre = '$BA10=""' in ist and '$BB10=""' in ist
        print('%-5s %-16s %s' % (spalte, name,
                                  'ja, mit BA/BB-Sperre' if hat_sperre
                                  else 'NEIN - Sperre fehlt'))
        if not hat_sperre:
            fehler += 1
        continue
    ok = soll == ist
    if not ok:
        fehler += 1
    print('%-5s %-16s %s' % (spalte, name, 'ja' if ok else 'NEIN'))
    if not ok:
        for i, (a, b) in enumerate(zip(soll, ist)):
            if a != b:
                print('     erste Abweichung bei Zeichen', i)
                print('     FORMELN:', soll[max(0, i - 40):i + 40])
                print('     DATEI  :', ist[max(0, i - 40):i + 40])
                break

print()
print(f'Geprueft: {geprueft} | Abweichungen: {fehler}')
raise SystemExit(1 if fehler else 0)