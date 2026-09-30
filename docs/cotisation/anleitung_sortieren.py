"""Sortiert die Abschnitte der Anleitung in die richtige Reihenfolge.

Beim schrittweisen Einfuegen mit Zeilennummern passiert es, dass ein
Abschnitt dann an anderer Stelle landet, weil sich die Zeilen davor
verschieben. Danach steht Kapitel 6 hinter Kapitel 9 - der Inhalt ist
richtig, die Reihenfolge nicht, und das sieht fuer den Leser wie ein
Fehler aus.

Das Skript verschiebt den Block an die richtige Stelle, statt ihn noch
einmal zu schreiben: geschrieben wurde er, falsch eingeordnet.
"""
import pathlib
import re

P = pathlib.Path('/Users/netjogger58/CascadeProjects/Vereins-OS/docs/'
                 'ANLEITUNG-Cotisation-Tresorier.md')
L = P.read_text().split('\n')

kapitel = [(i, m.group(1))
           for i, l in enumerate(L)
           for m in [re.match(r'^## (\d+)\. ', l)] if m]
print('gefunden:', ', '.join(f'{n}@Z{i + 1}' for i, n in kapitel))

# Ist die Reihenfolge schon 1,2,3...? Dann nichts tun. Das Skript soll
# wiederholbar laufen, ohne die Datei bei jedem Lauf zu verschieben.
nummern = [int(n) for _, n in kapitel]
if nummern == sorted(nummern):
    print('Reihenfolge stimmt bereits - nichts zu tun.')
    raise SystemExit(0)

# Abschnitt 6 samt Inhalt herausnehmen: von seiner Zeile bis vor die
# naechste Ueberschrift, die keine Kapitelnummer hat.
i6 = next(i for i, n in kapitel if n == '6')
ende = next(i for i in range(i6 + 1, len(L))
            if L[i].startswith('## ') and not re.match(r'^## \d+\. ', L[i]))
block = L[i6:ende]
rest = L[:i6] + L[ende:]

# Vor Kapitel 7 einfuegen
ziel = next(i for i, l in enumerate(rest)
            if re.match(r'^## 7\. ', l))
neu = rest[:ziel] + block + rest[ziel:]
P.write_text('\n'.join(neu))

print(f'Abschnitt 6 ({len(block)} Zeilen) vor Kapitel 7 verschoben')
print()
for i, l in enumerate(neu):
    m = re.match(r'^## (\d+)\. ', l)
    if m:
        print(f'  {m.group(1)}  Zeile {i + 1}')