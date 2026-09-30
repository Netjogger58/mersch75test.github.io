"""Prueft, ob FORMELN exakt dem entspricht, was in der Datei steht.

Der Vergleich laeuft gegen die AKTUELLE Arbeitsmappe - das ist die
einzige Masszahl, die zaehlt. Die Sicherung dient nur als Referenz, um
den Abstand zum Original auszugeben.

Anlass: Klammerbalance und XML-Wohlgeformtheit waren in Ordnung, Excel
lehnte die Datei trotzdem ab. Ursache war eine einzige zusaetzliche
Klammer in BV an Zeichen 189 (">0," wurde zu ">0),"). Dieser Test
faengt genau solche stillen Abweichungen.
"""
import re
import sys
import zipfile

SICH = ('/Users/netjogger58/CascadeProjects/Vereins-OS/docs/'
        'GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm')

sys.path.insert(0, '/Users/netjogger58/CascadeProjects/mersch75test.github.io/'
                   'docs/cotisation')
import cotisation_regeln_setzen as cr  # noqa: E402
import mappe  # noqa: E402


def zellen(pfad):
    x = zipfile.ZipFile(pfad).read('xl/worksheets/sheet1.xml').decode('utf-8')
    out = {}
    for m in re.finditer(r'<c r="([A-Z]+\d+)"[^>]*><f[^>]*>(.*?)</f>', x, re.S):
        out[m.group(1)] = (m.group(2).replace('&gt;', '>').replace('&lt;', '<')
                           .replace('&quot;', '"').replace('&amp;', '&'))
    return out


gut = zellen(SICH)
ist_datei = zellen(mappe.datenquelle())
formeln = {e[0]: e[-1] for e in cr.FORMELN}

fehler = []
print('%-5s %-10s %-10s %s' % ('SPALTE', 'in FORMELN', 'in Datei', 'Abstand zum Original'))
print('-' * 68)
for sp, formel in formeln.items():
    r = 10
    erwartet = formel.format(r=r, e=cr.ERSTE, l=cr.LETZTE).lstrip('=')
    in_datei = ist_datei.get(sp + str(r))
    alt = gut.get(sp + str(r))
    if in_datei is None:
        print('%-5s %-10s %-10s %s' % (sp, 'ok', 'FEHLT', '-'))
        fehler.append(f'{sp}: keine Formel in der Datei')
        continue
    gleich = erwartet == in_datei
    abstand = '-'
    if alt:
        abstand = 0 if gleich else sum(
            1 for x, y in zip(erwartet, alt) if x != y)
    print('%-5s %-10s %-10s %s' % (sp, 'ok' if gleich else 'ABWEICHUNG',
                                   'ok' if gleich else 'ABWEICHUNG', abstand))
    if not gleich:
        fehler.append(f'{sp}: FORMELN und Datei stimmen nicht überein')
        for i, (x, y) in enumerate(zip(erwartet, in_datei)):
            if x != y:
                fehler.append(f'   erste Abweichung bei Zeichen {i}')
                fehler.append(f'   FORMELN: ...{erwartet[max(0, i-40):i+40]}...')
                fehler.append(f'   DATEI  : ...{in_datei[max(0, i-40):i+40]}...')
                break

print()
print('Ergebnis:', 'FORMELN und Datei sind identisch' if not fehler
      else 'ABWEICHUNG')
for f in fehler:
    print(' -', f)
raise SystemExit(1 if fehler else 0)

print()
print('Ergebnis:', 'FORMELN und geprüfte Datei stimmen überein'
      if not fehler else 'ABWEICHUNG')
for f in fehler:
    print(' -', f)
raise SystemExit(1 if fehler else 0)
