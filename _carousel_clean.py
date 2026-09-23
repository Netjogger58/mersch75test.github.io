import re
import sys

with open('index.html', 'r') as f:
    html = f.read()

marker = 'data-news-track'
marker_pos = html.find(marker)

# Find the track div that contains the marker (not the viewport div)
# The track div is the one with data-news-track attribute
track_div_start = html.rfind('<div class="news-carousel-track"', 0, marker_pos)
if track_div_start == -1:
    print("ERROR: Could not find track div")
    sys.exit(1)

# Find the closing > of the track div
track_div_open_end = html.find('>', track_div_start)
if track_div_open_end == -1:
    print("ERROR: Could not find track div closing >")
    sys.exit(1)

track_content_start = track_div_open_end + 1

# Find the news-arrow button after the track
button_pos = html.find('<button class="news-arrow', track_content_start)
if button_pos == -1:
    print('ERROR: Could not find news-arrow button')
    sys.exit(1)

# Find the closing divs before the button
prev_div = html.rfind('</div>', 0, button_pos)
viewport_div = html.rfind('</div>', 0, prev_div - 1)
track_end_pos = viewport_div + 6

print('Track content:', track_content_start, 'to', track_end_pos)

track = html[track_content_start:track_end_pos]
articles = re.findall(r'<article\s+[^>]*class="[^"]*news-slide[^"]*"[^>]*>.*?</article>', track, re.DOTALL)
print('Found', len(articles), 'articles')

keep = {'news-slide-coupe-fe', 'news-slide-floumaart', 'news-slide-ag'}
kept = []
for a in articles:
    cls_matches = re.findall(r'news-slide-\S+', a)
    if cls_matches:
        for cls_name in cls_matches:
            if cls_name in keep:
                kept.append(a)
                break

removed = [a for a in articles if a not in kept]
print('Keeping:', len(kept), 'Removing:', len(removed))
for a in removed:
    m = re.search(r'class="[^"]*"', a)
    print('  REMOVE:', m.group(0) if m else 'unknown')

new_track = '\n' + '\n\n'.join(kept) + '\n                    '
new_html = html[:track_content_start] + new_track + html[track_end_pos:]

with open('index.html', 'w') as f:
    f.write(new_html)
print('Done! index.html updated.')
