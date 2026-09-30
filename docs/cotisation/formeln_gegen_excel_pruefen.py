"""Vergleicht die umgeschriebenen FORMELN mit dem, was in der Datei steht.

Excel hat die Formeln beim Einfuegen der vier Spalten selbst angepasst.
Damit liegt eine unabhaengige Referenz vor: stimmt meine Umschreibung mit
dem, was Excel gemacht hat, ist der Spaltenwechsel korrekt.
"""
import re
import sys
import zipfile

sys.path.insert(0, '/Users/netjogger58/CascadeProjects/mersch75test.github.io/'
                   'docs/cotisation')
import cotisation_regeln_setzen as cr  # noqa: E402
import mappe  # noqa: E402

PAARE = [('CL', 'CP'), ('BV', 'BZ'), ('CC', 'CG'), ('CE', 'CI'),
         ('CH', 'CL'), ('CJ', 'CN'), ('BY', 'CC'), ('BZ', 'CD'),
         ('CA', 'CE'), ('CB', 'CF'), ('CD', 'CH'), ('CG', 'CK'),
         ('CF', 'CJ')]

with zipfile.ZipFile(mappe.datenquelle()) as z:
    x = z.read('xl/worksheets/sheet1.xml').decode('utf-8')


def holen(ref):
    m = re.search(r'<c r="%s"[^>]*>(?:<f[^>]*>(.*?)</f>)?(?:<v|<is)' % ref,
                  x, re.S)
    if not m or not m.group(1):
        return None
    return (m.group(1).replace('&gt;', '>').replace('&lt;', '<')
            .replace('&quot;', '"').replace('&amp;', '&'))


schlecht = 0
print('%-5s %-6s %s' % ('ALT', 'NEU', 'STIMMT MIT EXCEL'))
print('-' * 58)
for alt, neu in PAARE:
    eintraege = [e[-1] for e in cr.FORMELN if e[0] == alt]
    if not eintraege:
        print('%-5s %-6s nicht in FORMELN' % (alt, neu))
        continue
    soll = eintraege[0].format(r=10, e=cr.ERSTE, l=cr.LETZTE).lstrip('=')
    ist = holen(neu + '10')
    if ist is None:
        print('%-5s %-6s keine Formel in der Datei' % (alt, neu))
        continue
    ok = soll == ist
    if not ok:
        schlecht += 1
    print('%-5s %-6s %s' % (alt, neu, 'ja' if ok else 'NEIN'))
    if not ok:
        for i, (a, b) in enumerate(zip(soll, ist)):
            if a != b:
                print('     erste Abweichung bei Zeichen', i)
                print('     FORMELN:', soll[max(0, i - 40):i + 40])
                print('     DATEI  :', ist[max(0, i - 40):i + 40])
                break

print()
print('Abweichungen:', schlecht)
raise SystemExit(1 if schlecht else 0)