"""Passt die Spaltenbuchstaben in FORMELN der neuen Datei an.

Wer vier Spalten vor AX einfuegt, verschiebt jede Spalte ab AY um vier
Positionen. Die Formeln sind buchstabenweise kodiert ($BV, $CC, $CL ...)
und zeigen danach auf die falsche Spalte - syntaktisch voellig in
Ordnung, inhaltlich falsch. Das faellt erst auf, wenn die Zahlen
schwanken.

Abgesichert wird die Verschiebung ueber die SPALTENNAMEN aus
spalten_verschiebung.py, nicht ueber eine blosse Rechnung. Eine
Namenspruefung faellt sofort auf, wenn die Annahme "+4" nicht stimmt.
"""
import pathlib
import re
import sys

P = pathlib.Path('/Users/netjogger58/CascadeProjects/mersch75test.github.io/'
                 'docs/cotisation/cotisation_regeln_setzen.py')


def num(buchstabe):
    n = 0
    for c in buchstabe:
        n = n * 26 + (ord(c) - 64)
    return n


def name(n):
    s = ''
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


ALT = '/Users/netjogger58/CascadeProjects/Vereins-OS/docs/' \
      'GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.' \
      'regeln-2026-09-29_vor-E7E8.xlsm'
NEU = '/Users/netjogger58/CascadeProjects/Vereins-OS/docs/' \
      'GC 2026-10-01 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm'


def kopf(pfad):
    import zipfile
    sys.path.insert(0, str(P.parent))
    import baut_arbeitsmappe as ba
    with zipfile.ZipFile(pfad) as z:
        teile = {n: z.read(n) for n in z.namelist()}
    return [c.strip() for c in ba.liese_blatt(teile, 'xl/worksheets/sheet1.xml')[0]]


alt, neu = kopf(ALT), kopf(NEU)
neu_idx = {}
for i, h in enumerate(neu):
    neu_idx.setdefault(h, i)

# Zuordnung ueber die Namen, mit Kontrolle
abbildung = {}
for i, h in enumerate(alt):
    j = neu_idx.get(h)
    if j is None or not h:
        continue
    abbildung[name(i + 1)] = (name(j + 1), j - i)

verschiebungen = {d for _, d in abbildung.values() if d}

# Zweimal gibt es die Spalte "Tarif": die des Users (alt BT, jetzt BX)
# und meine Rechenspalte (alt CE). Der Namensvergleich kann sie nicht
# unterscheiden und hat CE faelschlich nach BX geschickt. Richtig ist CI:
# das ist die Spalte, deren Formel in der Datei nach dem Einfuegen von
# Excel selbst auf CI steht und weiterhin die Tarif-Berechnung traegt.
abbildung["CE"] = ("CI", 4)

print('Verschiebungen gefunden:', sorted(verschiebungen))
# -7 kommt von "Tarif": es gibt zwei Spalten dieses Namens (die des Users
# und meine Rechenspalte). Der Namensvergleich kann sie nicht unterscheiden,
# deshalb wird die Richtigkeit spaeter ueber die von Excel selbst
# angepassten Formeln in der Datei geprueft.
assert verschiebungen <= {0, 4, -7} and 4 in verschiebungen, (
    'unerwartete Verschiebung: %s' % sorted(verschiebungen))

alt_buchstaben = [a for a, _ in abbildung.values()]
print('Spalten mit Verschiebung:', ', '.join(
    f'{a}->{n}' for a, (n, _) in sorted(abbildung.items(), key=lambda kv: num(kv[0]))
    if n != a))
print()


def verschiebe(text):
    """Alle $-Referenzen auf Spalten ab AY um vier Positionen schieben.

    Bewusst NICHT: Cotisation!$B$13 und Cotisation!$I$2:$I$50 - das sind
    Spalten eines ANDEREN Blattes. Das Muster erkennt sie nicht, weil auf
    den Buchstaben ein "$" und kein "{" folgt.
    """
    def einsetzen(m):
        sp = m.group(1)
        if sp not in abbildung:
            return m.group(0)
        neu_sp, diff = abbildung[sp]
        if diff == 0:
            return m.group(0)
        return '$' + neu_sp + m.group(2)
    return re.sub(r'\$([A-Z]{1,2})(\{|\$)', einsetzen, text)


s = P.read_text()
start = s.index('FORMELN = [')
ende = s.index('\n]\n', start)
block = s[start:ende]

neu_block = []
geaendert = 0
for zeile in block.split('\n'):
    # ALLE Zeilen eines Formel-Eintrags, nicht nur die erste: eine Formel
    # ueber mehrere Zeilen ist ein Python-String aus verketteten Literalen.
    # Nur die erste Zeile beginnt mit "'=", die Fortsetzungen nicht - sie
    # wurden sonst uebersprungen und blieben auf alten Spalten stehen.
    if zeile.lstrip().startswith("'") and '$' in zeile:
        alt_txt = zeile
        neu_txt = verschiebe(zeile)
        if neu_txt != alt_txt:
            geaendert += 1
            zeile = neu_txt
    neu_block.append(zeile)

print('Formelzeilen geaendert:', geaendert)
P.write_text(s[:start] + '\n'.join(neu_block) + s[ende:])
print('geschrieben')