import re, glob
from collections import Counter
htmlkeys = set(); keyfiles = {}
for f in glob.glob('*.html'):
    t = open(f, encoding='utf-8', errors='ignore').read()
    ks = set(re.findall(r'data-i18n="([^"]+)"', t))
    for m in re.findall(r'data-i18n-attr="([^"]+)"', t):
        for b in m.split(';'):
            if ':' in b:
                ks.add(b.split(':')[1].strip())
    ks.update(re.findall(r'data-i18n-html="([^"]+)"', t))
    for k in ks:
        keyfiles.setdefault(k, []).append(f)
scr = open('script.js', encoding='utf-8').read()
missing = sorted([k for k in htmlkeys if k not in scr])
print('html keys:', len(htmlkeys), 'missing in script.js:', len(missing))
c = Counter()
for k in missing:
    for f in keyfiles[k]:
        c[f] += 1
print('missing per file:', dict(c.most_common()))
print('missing keys:')
for k in missing:
    print(' ', k, '<-', keyfiles[k])
