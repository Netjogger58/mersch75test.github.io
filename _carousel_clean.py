"""Remove news carousel articles that are not in the keep list.

Keeps exactly the target slides (coupe-fe, floumaart, ag) inside the
news-carousel-track of index.html and leaves every other line of the
file untouched (track/viewport closing divs, buttons, scripts, footer).

Usage: python3 _carousel_clean.py
"""

import re
import sys

KEEP = {'news-slide-coupe-fe', 'news-slide-ag'}
ARTICLE_START = re.compile(r'<article\s+class="([^"]*news-slide[^"]*)"')

with open('index.html', 'r') as f:
    lines = f.readlines()

out = []
i = 0
kept = 0
removed = 0

while i < len(lines):
    m = ARTICLE_START.search(lines[i])
    if m:
        start = i
        depth = 1 if '</article>' not in lines[i] else 0
        i += 1
        while i < len(lines) and depth > 0:
            if '<article' in lines[i] and '</article>' not in lines[i]:
                depth += 1
            if '</article>' in lines[i]:
                depth -= 1
            i += 1
        block = lines[start:i]
        classes = re.findall(r'news-slide-[A-Za-z0-9-]+', m.group(1))
        if any(c in KEEP for c in classes):
            out.extend(block)
            kept += 1
        else:
            removed += 1
            # Drop one trailing blank separator line after a removed article
            if i < len(lines) and lines[i].strip() == '':
                i += 1
        continue
    out.append(lines[i])
    i += 1

print('Keeping:', kept, 'Removing:', removed)

if kept != len(KEEP):
    print('ERROR: expected to keep %d articles, kept %d' % (len(KEEP), kept))
    sys.exit(1)

with open('index.html', 'w') as f:
    f.writelines(out)
print('Done! index.html updated.')
