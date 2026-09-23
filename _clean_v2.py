import re

with open('index.html', 'r') as f:
    lines = f.readlines()

KEEP = {'news-slide-coupe-fe', 'news-slide-floumaart', 'news-slide-ag'}
ARTICLE_START = re.compile(r'<article\s+class="([^"]*news-slide[^"]*)"')

out = []
i = 0
removed = 0
kept = 0

while i < len(lines):
    m = ARTICLE_START.search(lines[i])
    if m:
        # Collect full article block
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
            # Drop a single trailing blank line that separated this article
            if i < len(lines) and lines[i].strip() == '':
                i += 1
        continue
    out.append(lines[i])
    i += 1

with open('index.html', 'w') as f:
    f.writelines(out)

print('Keeping:', kept, 'Removing:', removed)