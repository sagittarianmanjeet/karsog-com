#!/usr/bin/env python3
"""One menu (tabs) for every page of karsog.com.

Run from the repo root after adding or regenerating pages:  python3 tools/sitenav.py
It replaces the <nav class="top"> block on every page in public/ with the shared tabs,
marks the current tab, and adds the tab styles. Safe to run any number of times.
To change the menu for the whole site, edit TABS below and run it again."""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, 'public')

# (key, English label, Hindi label, link)
TABS = [
    ('home', 'Home', 'होम', '/'),
    ('weather', 'Weather', 'मौसम', '/weather/'),
    ('bus', 'Buses', 'बसें', '/karsog-bus-stand/'),
    ('places', 'Places & Temples', 'स्थल व मंदिर', '/places/'),
    ('photos', 'Photos', 'फ़ोटो', '/photos/'),
    ('plan', 'Plan a Trip', 'यात्रा योजना', '/plan/'),
    ('mandi', 'Mandi Rates', 'मंडी भाव', '/mandi-rates/'),
    ('contacts', 'Useful Numbers', 'ज़रूरी नंबर', '/contacts/'),
    ('rti', 'RTI', 'RTI', '/rti/'),
]
# Temple and sightseeing guides sit under "Places & Temples"; other drone-photo place pages under "Photos".
PLACES = {'mahunag', 'mamleshwar', 'shikari-devi', 'kamru-nag', 'pangna-fort', 'chindi', 'tattapani', 'kao',
          'janjehli', 'jarli-mata'}
BUS = {'karsog-bus-stand', 'karsog-private-bus', 'mandi-to-karsog-bus', 'shimla-to-karsog-bus', 'bus'}
# Pages with a Hindi version: English path -> Hindi path
HINDI = {'/': '/hi/', '/rti/': '/hi/rti/'}

CSS = ('<style id="knav">'
       'nav.top.knav{position:sticky;top:0;z-index:40;background:rgba(250,248,244,.96);-webkit-backdrop-filter:blur(10px);'
       'backdrop-filter:blur(10px);border-bottom:1px solid #dcd5c8}'
       '.knav .kin{display:flex;align-items:center;gap:1rem;padding:.55rem 1.25rem;flex-wrap:nowrap}'
       '.knav .kbrand{font-family:"Playfair Display",Georgia,serif;font-size:1.25rem;font-weight:700;color:#1c3a1c;'
       'white-space:nowrap;text-decoration:none}.knav .kbrand em{color:#b8832a;margin-left:.25rem}'
       '.knav .ktabs{display:flex;gap:.15rem;list-style:none;margin:0 0 0 auto;padding:0;overflow-x:auto;'
       'scrollbar-width:none;-webkit-overflow-scrolling:touch}.knav .ktabs::-webkit-scrollbar{display:none}'
       '.knav .ktabs a{display:block;padding:.5rem .75rem;border-radius:999px;font-size:.74rem;font-weight:500;'
       'text-transform:uppercase;letter-spacing:.07em;color:#1a1a18b3;white-space:nowrap;text-decoration:none;transition:background .2s,color .2s}'
       '.knav .ktabs a:hover{color:#1c3a1c;background:#efe9dd}'
       '.knav .ktabs a[aria-current=page]{background:#1c3a1c;color:#f6f3ee}'
       '.knav .klang{flex:none;font-size:.78rem;padding:.35rem .65rem;border:1px solid #dcd5c8;color:#1c3a1c;'
       'border-radius:999px;white-space:nowrap;text-decoration:none}.knav .klang:hover{border-color:#1c3a1c}'
       '@media(max-width:1000px){.knav .kin{flex-wrap:wrap;gap:.1rem .75rem;padding:.5rem 1.25rem .35rem}'
       '.knav .klang{margin-left:auto}.knav .ktabs{order:3;flex-basis:100%;margin:0 -1.25rem;padding:0 1.25rem .15rem;'
       '-webkit-mask-image:linear-gradient(90deg,#000 88%,transparent);mask-image:linear-gradient(90deg,#000 88%,transparent)}'
       '.knav .ktabs a{padding:.45rem .7rem;font-size:.72rem}}'
       '</style>')


def url_of(path):
    rel = os.path.relpath(path, PUB).replace(os.sep, '/')
    if rel == 'index.html':
        return '/'
    if rel.endswith('/index.html'):
        return '/' + rel[:-len('index.html')]
    return '/' + rel


def tab_for(url):
    if url in ('/', '/hi/'):
        return 'home'
    first = url.strip('/').split('/')[0]
    if first == 'hi':
        first = url.strip('/').split('/')[1] if url.count('/') > 2 else ''
    if first in BUS:
        return 'bus'
    if first in PLACES or first == 'places':
        return 'places'
    if first in ('photos', 'rides'):
        return 'photos'
    if first in ('distance', 'hotels'):
        return 'plan'
    for key, _, _, link in TABS:
        if link.strip('/') == first:
            return key
    return 'photos' if os.path.exists(os.path.join(PUB, 'photos', first)) else None


def nav_html(url):
    hindi = url.startswith('/hi/')
    cur = tab_for(url)
    items = []
    for key, en, hi, link in TABS:
        if hindi and link in HINDI:
            link = HINDI[link]
        ac = ' aria-current="page"' if key == cur else ''
        items.append(f'<li><a href="{link}"{ac}>{hi if hindi else en}</a></li>')
    lang = ''
    if hindi:
        back = {v: k for k, v in HINDI.items()}.get(url)
        if back:
            lang = f'<a class="klang" href="{back}" hreflang="en" lang="en">English</a>'
    elif url in HINDI:
        lang = f'<a class="klang" href="{HINDI[url]}" hreflang="hi" lang="hi">हिंदी</a>'
    home = '/hi/' if hindi else '/'
    brand = 'करसोग<em>घाटी</em>' if hindi else 'Karsog<em>Valley</em>'
    return (f'<nav class="top knav" aria-label="{"मुख्य" if hindi else "Main"}">\n  <div class="container kin">\n'
            f'    <a href="{home}" class="kbrand">{brand}</a>\n    {lang}\n'
            f'    <ul class="ktabs">{"".join(items)}</ul>\n  </div>\n</nav>')


# The old homepage menu script assumed a hamburger menu; make it safe once the burger is gone.
OLD_JS = re.compile(r"const burger = document\.getElementById\('burger'\);.*?"
                    r"menu\.querySelectorAll\('a'\)\.forEach\(a => a\.addEventListener\('click', \(\) => toggleMenu\(false\)\)\);",
                    re.S)
NEW_JS = ("const burger = document.getElementById('burger');\nconst menu = document.getElementById('mobile-menu');\n"
          "function toggleMenu(open){ if (!menu || !burger) return; menu.classList.toggle('open', open); "
          "burger.classList.toggle('open', open); burger.setAttribute('aria-expanded', open); "
          "document.body.style.overflow = open ? 'hidden' : ''; }")


def fix(path):
    s = open(path, encoding='utf-8').read()
    o = s
    url = url_of(path)
    if '<nav' not in s:
        return False
    s = re.sub(r'<nav class="top[^"]*"[^>]*>.*?</nav>', lambda m: nav_html(url), s, count=1, flags=re.S)
    s = re.sub(r'\n?<!-- Mobile menu -->\n<div class="mobile-menu".*?</div>\n', '\n', s, count=1, flags=re.S)
    s = re.sub(r'<div class="mobile-menu" id="mobile-menu".*?</div>\n', '', s, count=1, flags=re.S)
    s = OLD_JS.sub(lambda m: NEW_JS, s)
    s = re.sub(r'<style id="knav">.*?</style>', lambda m: CSS, s, flags=re.S)
    if 'id="knav"' not in s:
        s = s.replace('</head>', CSS + '\n</head>', 1)
    if s != o:
        open(path, 'w', encoding='utf-8').write(s)
        return True
    return False


def run():
    files = sorted(glob.glob(os.path.join(PUB, '**', 'index.html'), recursive=True)) + [os.path.join(PUB, '404.html')]
    n = sum(fix(f) for f in files if os.path.exists(f))
    print(f'menu updated on {n} of {len(files)} pages')


if __name__ == '__main__':
    run()
