#!/usr/bin/env python3
"""Post-publish QA for a blog.quit9to5.in post. Read-only.
Usage: python3 live_qa.py <post-url> [source.md]
Ported from the box (blog/qa/live_qa.py). Needs beautifulsoup4 and google-chrome for screenshots.
Output dir: $BLOG_QA_DIR (default ./qa). Writes <slug>_live.html, _text.txt, _desktop.png, _mobile.png and prints a report."""
import sys, re, time, subprocess, urllib.request, unicodedata, os
from collections import Counter
from bs4 import BeautifulSoup
url = sys.argv[1].split('?')[0]; src = sys.argv[2] if len(sys.argv) > 2 else None
slug = url.rstrip('/').split('/')[-1]; here = os.environ.get('BLOG_QA_DIR', os.path.join(os.getcwd(), 'qa')); os.makedirs(here, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh) Chrome/130'}
def get(u):
    r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30); return r.status, r.read().decode('utf-8', 'replace')
nc = int(time.time()); st, html = get(f'{url}?nc={nc}')
open(f'{here}/{slug}_live.html', 'w').write(html)
s = BeautifulSoup(html, 'html.parser'); body = s.find(id='content-blocks')
fail = []
def chk(ok, msg):
    print(('PASS ' if ok else 'FAIL ') + msg)
    if not ok: fail.append(msg)
chk(st == 200, f'HTTP {st}')
title = s.title.string if s.title else ''
desc = (s.find('meta', attrs={'name': 'description'}) or {}).get('content', '')
og = {m['property']: m.get('content', '') for m in s.find_all('meta', property=re.compile('^og:'))}
print(f'title tag ({len(title)}): {title}\nmeta desc ({len(desc)}): {desc}\nog:title: {og.get("og:title")}\nog:description: {og.get("og:description")}\nog:image: {og.get("og:image")}')
chk(len(title.replace(" | Quit 9to5", "")) <= 60, 'title <= 60 chars (excluding " | Quit 9to5")')
chk(50 <= len(desc) <= 155, 'meta description 50-155 chars')
chk(bool(og.get('og:image')), 'og:image set (thumbnail)')
text = body.get_text('\n', strip=True); open(f'{here}/{slug}_live_text.txt', 'w').write(text)
bad = [b for b in ['â', 'Ã', 'Â', '€™', '�', 'ðŸ', '[PALLAV', 'PALLAV:', 'TODO', 'TK ', '{{', ']('] if b in text]
chk(not bad, f'no mojibake/placeholders/raw markdown {bad}')
print('non-ASCII chars:', {f'{c} {unicodedata.name(c, "?")}': n for c, n in Counter(c for c in text if ord(c) > 127).items()})
chk('—' not in text and '–' not in text, 'no em/en dashes in body text')
if src:
    n_src = open(src).read().count('₹'); chk(text.count('₹') == n_src, f'₹ count live {text.count("₹")} == source {n_src}')
heads = [(h.name, h.get_text(' ', strip=True)) for h in body.find_all(['h1', 'h2', 'h3', 'h4'])]
for h in heads: print('  ', h)
chk(not any(h[0] == 'h1' for h in heads), 'no H1 inside the body')
chk(not any(h.find_parent(class_=re.compile('blockquote|quote')) for h in body.find_all(['h2', 'h3'])), 'no heading inside a quote block')
qv = set(c for q in body.find_all(class_='dream-post-content-blockquoteFigure') for c in q.get('class', []) if c.startswith('yuqx'))
print('quote block style classes:', qv, '(older posts use yuqx91/yuqx94 = left-bar style)')
for a in body.find_all('a'):
    h = a.get('href', '')
    try: code = urllib.request.urlopen(urllib.request.Request(h, headers=UA), timeout=20).status
    except Exception as e: code = str(e)[:40]
    chk(code == 200, f'link {code}: "{a.get_text(strip=True)}" -> {h}')
print('words:', len(text.split()))
for name, size in [('desktop', '1280,2600'), ('mobile', '412,2600')]:
    subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', f'--user-data-dir=/tmp/qa-{name}',
                    f'--window-size={size}', '--virtual-time-budget=10000', f'--screenshot={here}/{slug}_{name}.png', f'{url}?nc={nc}'], capture_output=True, timeout=150)
print('screenshots:', f'{here}/{slug}_desktop.png', f'{here}/{slug}_mobile.png', '(open with Read; tall windows show a blank gap below the hero image, a headless artefact that also appears on older posts)')
print('\nRESULT:', 'ALL PASS' if not fail else f'{len(fail)} FAIL(S)')
