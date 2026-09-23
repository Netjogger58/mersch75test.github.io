import re
with open('index.html', 'r') as f:
    html = f.read()

# Find the data-news-track marker
marker = 'data-news-track'
marker_pos = html.find(marker)
print('marker_pos:', marker_pos)

# Find opening <div> tag for the track
div_open = html.rfind('<div', 0, marker_pos)
div_close = html.find('>', div_open)
if div_open == -1 or div_close == -1:
    print('ERROR: Could not find track div')
    exit(1)
content_start = div_close + 1
print('content_start:', content_start)

# Find the end of the track content
end_marker = '</div>\n                </div>\n                <button class="news-arrow"'
content_end = html.find(end_marker, content_start)
print('content_end:', content_end)

if content_end == -1:
    # Try alternative
    alt_end = '</div>\n                        </div>'
    content_end = html.find(alt_end, content_start)
    print('alt content_end:', content_end)

# Extract track content
track = html[content_start:content_end] if content_end > content_start else ''
print('track length:', len(track))

# Find all news-slide articles
articles = re.findall(r'<article\s+[^>]*class="[^"]*news-slide[^"]*"[^>]*>.*?</article>', track, re.DOTALL)
print('Found articles:', len(articles))
for a in articles:
    cls = re.search(r'class="([^"]+)"', a)
    if cls:
        print('  Class:', cls.group(1))
        matches = re.findall(r'news-slide-\S+', cls.group(1))
        print('  Matches:', matches)