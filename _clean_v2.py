import re

with open('index.html', 'r') as f:
    lines = f.readlines()

keep_lines = []
i = 0
in_track = False

while i < len(lines):
    line = lines[i]
    
    if 'data-news-track' in line and '<div class="news-carousel-track"' in line:
        in_track = True
        keep_lines.append(line)
        i += 1
        continue
    
    if in_track:
        m = re.match(r'\s*<article\s+class="([^"]*news-slide[^"]*)"', line)
        if m:
            article_class = m.group(1)
            article_lines = [line]
            i += 1
            depth = 1
            while i < len(lines) and depth > 0:
                l = lines[i]
                if '<article' in l and '</article>' not in l:
                    depth += 1
                if '</article>' in l:
                    depth -= 1
                article_lines.append(l)
                i += 1
            
            cls_name = None
            for cls in re.findall(r'news-slide-\S+', article_class):
                if cls in {'news-slide-coupe-fe', 'news-slide-floumaart', 'news-slide-ag'}:
                    cls_name = cls
                    break
            
            if cls_name:
                keep_lines.extend(article_lines)
                print('KEEP:', cls_name)
            else:
                print('REMOVE:', article_class)
            continue
        
        if '</div>' in line and 'news-arrow' in (lines[i+1] if i+1 < len(lines) else ''):
            keep_lines.append(line)
            i += 1
            continue
        
        i += 1
        continue
    
    keep_lines.append(line)
    i += 1

with open('index.html', 'w') as f:
    f.writelines(keep_lines)

print('Done!')