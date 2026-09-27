#!/usr/bin/env python3
"""One-off (27 Sep 2026): split the long homepage into tab pages.

  /           Home: hero, quick links to every tab, bus timings, photo teaser, FAQ, emergency numbers
  /places/    Places & Temples
  /photos/    Drone photos + ride videos
  /plan/      How to reach, taxi, itineraries, stay & eat, festivals, map
  /contacts/  Government offices & contacts + emergency numbers

Old links like /#plan or /#local are rewritten site-wide to their new pages.
Kept in the repo for reference; don't run it twice (the homepage sections will already be gone)."""
import os, re, json, glob, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, 'public')
IDX = os.path.join(PUB, 'index.html')
s = open(IDX, encoding='utf-8').read()
assert '<!-- Reach -->' in s, 'homepage already split'

# ---- cut the homepage into blocks at its <!-- Name --> comments
MARKS = ['<!-- photos:start -->', '<!-- Marquee -->', '<!-- Places -->', '<!-- Videos · Karsog Miles -->', '<!-- Reach -->',
         '<!-- Buses -->', '<!-- Taxi & Local Transport -->', '<!-- Itineraries -->', '<!-- Stay & Eat -->',
         '<!-- Festivals & Fairs -->', '<!-- Map -->', '<!-- FAQ -->', '<!-- Local Info -->', '<!-- Emergency -->',
         '<!-- Floating Submit Update button -->']
KEYS = ['photos', 'marquee', 'places', 'videos', 'reach', 'bus', 'taxi', 'plan', 'stay', 'festivals', 'map', 'faq',
        'local', 'emergency']
pos = [s.index(m) for m in MARKS]
assert pos == sorted(pos)
B = {k: s[pos[i]:pos[i + 1]].rstrip() + '\n\n' for i, k in enumerate(KEYS)}
pre = s[:pos[0]]              # head, weather strip, nav, hero
post = s[pos[-1]:]            # submit button, modal, footer, scripts

# ---- where each moved section now lives
MOVED = {'photos': '/photos/', 'videos': '/photos/#videos', 'places': '/places/', 'reach': '/plan/#reach',
         'taxi': '/plan/#taxi', 'plan': '/plan/', 'stay': '/plan/#stay', 'festivals': '/plan/#festivals',
         'map': '/plan/#map', 'local': '/contacts/'}
STAY = {'bus', 'faq', 'emergency', 'top'}   # still on the homepage


def relink(h, here):
    """Point #section and /#section links at the page that now holds the section."""
    def sub(m):
        q, key = m.group(1), m.group(2)
        if f'id="{key}"' in h:
            return f'href={q}#{key}{q}'
        if key in MOVED:
            tgt = MOVED[key]
            if tgt.split('#')[0] == here:
                tgt = '#' + (tgt.split('#')[1] if '#' in tgt else 'top')
            return f'href={q}{tgt}{q}'
        if key in STAY and here != '/':
            return f'href={q}/#{key}{q}'
        return m.group(0)
    return re.sub(r'href=(["\'])/?#([a-z-]+)\1', sub, h)


HUB_CSS = ('<style>.hub{background:var(--forest);color:var(--cream);padding:3.25rem 0 2.75rem}'
           '.hub .eyebrow{color:var(--gold-light)}.hub h1{font-family:"Playfair Display",serif;font-size:clamp(2.1rem,5vw,3.4rem);'
           'line-height:1.08;margin:.6rem 0 0;color:var(--cream)}.hub h1 em{color:var(--gold-light)}'
           '.hub p{max-width:44rem;margin-top:1rem;opacity:.85;line-height:1.65}'
           '.hub .jump{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1.5rem}.hub .jump a{border:1px solid #f6f3ee55;'
           'color:var(--cream);padding:.45rem .9rem;border-radius:999px;font-size:.8rem}.hub .jump a:hover{background:#f6f3ee1a}'
           '.crumbs{font-size:.75rem;opacity:.7}.crumbs a{color:var(--gold-light)}</style>')


def head_for(path, title, desc, crumb):
    h = pre[:pre.index('<body')]
    url = f'https://karsog.com{path}'
    h = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title)}</title>', h)
    h = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + html.escape(desc), h)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(title), h)
    h = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + html.escape(desc), h)
    h = h.replace('<meta property="og:url" content="https://karsog.com/" />', f'<meta property="og:url" content="{url}" />')
    h = h.replace('<link rel="canonical" href="https://karsog.com/" />', f'<link rel="canonical" href="{url}" />')
    h = h.replace('<meta property="og:type" content="website" />', '<meta property="og:type" content="article" />')
    h = re.sub(r'<link rel="alternate" hreflang[^>]*>\n?', '', h)
    h = re.sub(r'<link rel="preload" as="image"[^>]*>\n?', '', h)
    h = h.replace('href="manifest.webmanifest"', 'href="/manifest.webmanifest"').replace('href="icon-192.png"', 'href="/icon-192.png"')
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Karsog Valley", "item": "https://karsog.com/"},
        {"@type": "ListItem", "position": 2, "name": crumb, "item": url}]}
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', h, flags=re.S)
    h = h.replace('</head>', '<script type="application/ld+json">' + json.dumps(bc, ensure_ascii=False) + '</script>\n'
                  + HUB_CSS + '\n</head>')
    return h


body_top = pre[pre.index('<body'):pre.index('<section class="hero"')]
foot = post.replace("navigator.serviceWorker.register('sw.js')", "navigator.serviceWorker.register('/sw.js')")


def hub(path, title, desc, crumb, eyebrow, h1, lede, jumps, keys, extra=''):
    jl = ''.join(f'<a href="#{k}">{n}</a>' for k, n in jumps)
    top = (f'<header class="hub"><div class="container"><div class="crumbs"><a href="/">Karsog Valley</a> › {html.escape(crumb)}</div>'
           f'<span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p>{lede}</p>'
           + (f'<div class="jump">{jl}</div>' if jumps else '') + '</div></header>\n\n')
    body = ''.join(B[k] for k in keys) + extra
    page = head_for(path, title, desc, crumb) + body_top + top + body + foot
    page = relink(page, path)
    d = os.path.join(PUB, path.strip('/'))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(page)


# The places hub gets a list of every temple / sightseeing guide page too.
GUIDES = [('/mahunag/', 'Mahunag Temple'), ('/mamleshwar/', 'Mamleshwar Mahadev'), ('/kao/', 'Kamaksha Devi, Kao'),
          ('/shikari-devi/', 'Shikari Devi'), ('/kamru-nag/', 'Kamru Nag Lake'), ('/pangna-fort/', 'Pangna Fort'),
          ('/tattapani/', 'Tattapani hot springs'), ('/chindi/', 'Chindi'), ('/janjehli/', 'Janjehli'),
          ('/jarli-mata/', 'Jarli Mata')]
guides = ('<section id="guides" class="bg-secondary"><div class="container"><div class="section-head"><span class="eyebrow">Full guides</span>'
          '<h2>Temple & place<br /><em>guides</em></h2></div><ul class="glist">'
          + ''.join(f'<li><a href="{u}">{n} →</a></li>' for u, n in GUIDES) +
          '</ul><p style="margin-top:1.25rem">Villages and viewpoints from the air: <a href="/photos/" style="color:var(--gold);font-weight:600">drone photos of 27 places →</a></p>'
          '</div></section>\n<style>.glist{list-style:none;padding:0;margin-top:1.5rem;display:grid;gap:.5rem;'
          'grid-template-columns:repeat(auto-fill,minmax(220px,1fr))}.glist a{display:block;background:#fff;border:1px solid var(--border);'
          'padding:.9rem 1rem;font-weight:600;color:var(--forest)}.glist a:hover{border-color:var(--gold)}</style>\n\n')

hub('/places/', 'Places to Visit in Karsog — Temples, Treks, Forts & Hot Springs',
    'Places to visit in Karsog Valley: Mahunag, Mamleshwar Mahadev, Kamaksha Devi, Shikari Devi, Kamru Nag, Pangna Fort, Tattapani and Chindi, with full guides.',
    'Places & Temples', 'What to see', 'Places &amp; <em>temples</em>',
    'Temples, treks, forts and hot springs in and around Karsog Valley, with a full guide for each.',
    [], ['marquee', 'places'], guides)
hub('/photos/', 'Karsog Photos — Drone Photos of 27 Places & Ride Videos',
    'Aerial drone photos of Karsog Valley: villages, temples, fairs and the Satluj valley, plus Karsog Miles motorcycle ride videos.',
    'Photos', 'Karsog from above', 'Karsog <em>photos</em>',
    'Drone photos of Karsog’s villages, temples and fairs, and ride videos from the valley’s roads. Pick a place to see all its photos.',
    [('photos', 'Drone photos'), ('videos', 'Ride videos')], ['photos', 'videos'])
hub('/plan/', 'Plan a Karsog Trip — How to Reach, Taxi Rates, Hotels & Festivals',
    'How to reach Karsog from Mandi, Shimla and Chandigarh, taxi rates, ready-made itineraries, where to stay and eat, and the year’s fairs and festivals.',
    'Plan a Trip', 'Plan your trip', 'Plan a Karsog <em>trip</em>',
    'Getting here, getting around, where to stay and eat, and when the valley celebrates.',
    [('reach', 'How to reach'), ('taxi', 'Taxi rates'), ('plan', 'Itineraries'), ('stay', 'Stay & eat'),
     ('festivals', 'Festivals'), ('map', 'Map')], ['reach', 'taxi', 'plan', 'stay', 'festivals', 'map'],
    '<section class="container" style="padding:2rem 0 3rem"><p>Buses: <a href="/karsog-bus-stand/" style="color:var(--gold);font-weight:600">Karsog bus stand time table →</a> · '
    '<a href="/karsog-private-bus/" style="color:var(--gold);font-weight:600">private buses →</a></p></section>\n\n')
hub('/contacts/', 'Karsog Useful Numbers — Emergency, Hospital, Police & Government Offices',
    'Emergency numbers and contacts for Karsog: ambulance, police, fire, civil hospital, SDM office, HRTC depot and other government offices.',
    'Useful Numbers', 'Local information', 'Useful <em>numbers</em>',
    'Emergency numbers first, then government offices and local contacts in Karsog. Tap a number to call.',
    [('emergency', 'Emergency'), ('local', 'Offices & contacts')], ['emergency', 'local'])

# ---- homepage: hero, quick links, buses, photo teaser, FAQ, emergency
places = json.load(open(os.path.join(PUB, 'photos', 'places.json')))
places.sort(key=lambda p: -p['n'])
tease = ''.join(f'<a class="pc" href="/{p["slug"]}/"><img src="{p["cover"]}" alt="Aerial view of {html.escape(p["title"])}, Karsog" '
                f'loading="lazy" width="800" height="533"><span class="pc-t"><b>{html.escape(p["title"])}</b><i>{p["n"]} photos</i></span></a>'
                for p in places[:6])
m = re.search(r'<style>#photos\{.*?</style>', B['photos'], re.S)
teaser = ('<!-- photos-teaser:start -->\n' + (m.group(0) if m else '') +
          f'<section id="photos"><div class="container"><div class="section-head"><span class="eyebrow">Karsog from above</span>'
          f'<h2>{sum(p["n"] for p in places)} drone photos,<br /><em>{len(places)} places.</em></h2></div>'
          f'<div class="pgrid">{tease}</div><p style="margin-top:1.5rem"><a href="/photos/" class="btn btn-gold">See all photos →</a></p>'
          '</div></section>\n<!-- photos-teaser:end -->\n\n')
TILES = [('/karsog-bus-stand/', '🚌', 'Buses', 'बसें', 'Every departure from Karsog bus stand, private buses, Mandi & Shimla timings'),
         ('/places/', '🛕', 'Places & Temples', 'स्थल व मंदिर', 'Mahunag, Mamleshwar, Kamaksha, Shikari Devi, Kamru Nag and more'),
         ('/photos/', '📸', 'Photos', 'फ़ोटो', 'Drone photos of 27 places and ride videos'),
         ('/plan/', '🧭', 'Plan a Trip', 'यात्रा योजना', 'How to reach, taxi rates, stay & eat, festivals'),
         ('/mandi-rates/', '🍎', 'Mandi Rates', 'मंडी भाव', 'Today’s apple and vegetable rates'),
         ('/contacts/', '☎️', 'Useful Numbers', 'ज़रूरी नंबर', 'Emergency, hospital, police and government offices')]
tiles = ('<section id="explore"><div class="container"><div class="tiles">' + ''.join(
    f'<a class="tile" href="{u}"><span class="ti">{i}</span><b data-hi="{hi}">{n}</b><small>{d}</small></a>' for u, i, n, hi, d in TILES) +
    '</div></div></section>\n<style>#explore{padding:2.5rem 0 1rem}.tiles{display:grid;gap:.75rem;grid-template-columns:repeat(auto-fill,minmax(min(100%,340px),1fr))}'
    '.tile{display:flex;flex-direction:column;gap:.2rem;background:#fff;border:1px solid var(--border);padding:1.1rem 1.2rem;transition:border-color .2s,transform .2s}'
    '.tile:hover{border-color:var(--gold);transform:translateY(-2px)}.tile .ti{font-size:1.5rem}.tile b{font-family:"Playfair Display",serif;'
    'font-size:1.2rem;color:var(--forest)}.tile small{color:var(--muted);line-height:1.5}</style>\n\n')
home = pre + tiles + B['bus'] + teaser + B['faq'] + B['emergency'] + post
home = relink(home, '/')
home = home.replace('<a href="#photos" class="btn btn-gold" data-hi="फ़ोटो देखें →">See Karsog from above →</a>',
                    '<a href="/photos/" class="btn btn-gold" data-hi="फ़ोटो देखें →">See Karsog from above →</a>')
open(IDX, 'w', encoding='utf-8').write(home)

# ---- rewrite old /#section links on every other page
n = 0
for f in glob.glob(os.path.join(PUB, '**', '*.html'), recursive=True):
    if f == IDX:
        continue
    t = open(f, encoding='utf-8').read()
    here = '/' + os.path.relpath(os.path.dirname(f), PUB).replace(os.sep, '/').strip('.') + '/'
    here = here.replace('//', '/')
    u = re.sub(r'href=(["\'])/#([a-z-]+)\1',
               lambda m: f'href={m.group(1)}{MOVED[m.group(2)]}{m.group(1)}' if m.group(2) in MOVED else m.group(0), t)
    if u != t:
        open(f, 'w', encoding='utf-8').write(u)
        n += 1
print('links updated on', n, 'pages')

# ---- sitemap
sm_p = os.path.join(PUB, 'sitemap.xml')
sm = open(sm_p, encoding='utf-8').read()
sm = re.sub(r'<!-- tabs -->.*?<!-- /tabs -->\n?', '', sm, flags=re.S)
ent = ''.join(f'  <url><loc>https://karsog.com{u}</loc><lastmod>2026-09-27</lastmod></url>\n'
              for u in ['/places/', '/photos/', '/plan/', '/contacts/'])
sm = sm.replace('</urlset>', '<!-- tabs -->\n' + ent + '<!-- /tabs -->\n</urlset>')
open(sm_p, 'w', encoding='utf-8').write(sm)
