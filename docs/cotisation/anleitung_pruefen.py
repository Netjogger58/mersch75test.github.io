import pathlib, re, urllib.parse

p = pathlib.Path('/Users/netjogger58/CascadeProjects/Vereins-OS/docs/'
                 'ANLEITUNG-Cotisation-Tresorier.md')
s = p.read_text()

print('Zeilen :', len(s.splitlines()))
print('Wörter :', len(s.split()))

# 1) Kapitel vs Inhaltsverzeichnis
kap = re.findall(r'^## (\d+)\. (.+)$', s, re.M)
iv = re.findall(r'^(\d+)\. \[(.+?)\]\(#', s, re.M)
print(f'\nKapitel im Referenzteil : {len(kap)}')
print(f'Einträge im Inhaltsverzeichnis: {len(iv)}')
print('Kapitel ohne IV-Eintrag :', [n for n, _ in kap if n not in [i for i, _ in iv]])
print('IV ohne Kapitel        :', [i for i, _ in iv if i not in [n for n, _ in kap]])

# 2) Anker pruefen (GitHub-Regel: Kleinbuchstaben, Leerzeichen -> '-',
#    Sonderzeichen weg, Umlaute bleiben)
def anker(t):
    t = t.strip().lower()
    t = re.sub(r'[`*]', '', t)
    t = re.sub(r'[^\w\sÀ-ÿ-]', '', t, flags=re.U)
    return t.replace(' ', '-') if '%' not in t else t.replace(' ', '-')

links = {urllib.parse.unquote(a) for a in re.findall(r'\]\(#([^)]+)\)', s)}
fehlend = [a for a in links if a not in {anker(f'{n}. {t}') for n, t in kap}]
print('\nLinks ohne Ziel        :', fehlend or 'keine')

# 3) Tabellen: jede Zeile gleich viele Spalten wie die Kopfzeile
print('\nUnvollstaendige Tabellenzeilen:')
bad = 0
zeilen = s.splitlines()
i = 0
while i < len(zeilen):
    if zeilen[i].startswith('|') and i + 1 < len(zeilen) and re.match(r'^\|[\s:|-]+\|$', zeilen[i + 1]):
        n = zeilen[i].count('|')
        j = i + 2
        while j < len(zeilen) and zeilen[j].startswith('|'):
            if zeilen[j].count('|') != n:
                print(f'   Z{j + 1}: {zeilen[j][:70]}')
                bad += 1
            j += 1
        i = j
    else:
        i += 1
print('   ', bad, 'auffaellig' if bad else 'keine')

# 4) Rubrik steht vor dem Referenzteil?
print('\nRubrik vor Referenzteil :',
      s.index('# 🔴 Rubrik') < s.index('# 📘 Referenz'))
