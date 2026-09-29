"""Place and temple guides written by hand in content/<lang>/<page>.html.

A content file starts with a header of "key: value" lines between two '---' lines, then the page text in HTML.
Header keys:
  title, desc, kicker, h1, lede      page title, Google description, heading texts
  hero       drone photo file for the top of the page, e.g. mahunag-214 (or 'band' for no photo)
  hero_alt   description of that photo;  hero_pos: which part of the photo to keep in view, e.g. 'center 40%'
  chips      short facts under the heading: 'pin: About 25 km from Karsog | calendar: Mela in mid-May'
  glance     'At a glance' box: 'Distance=About 25 km | Best time=April to November'
  geo        latitude,longitude for the Directions button
  bus        link to the bus timings for this place
  gallery    drone photo folder to show (usually the page name)
  videos     YouTube ids separated by spaces (titles come from data/videos.json)
  related    other guide pages, separated by spaces
  schema     schema.org type, e.g. HinduTemple or TouristAttraction
  crumb      breadcrumb: 'Temples=/temples/'
FAQ: write <faq><q>Question</q><a>Answer</a> ...</faq> anywhere in the text; it becomes a FAQ section for Google."""
import json, os, re
from urllib.parse import quote_plus
from layout import L, icon, img, section, shead, faq_block, faq_ld, comments, gallery, pcard, esc, href, ROOT
from data import BY_SLUG, PHOTOS, GUIDES, pbase, photo_label, photo_alt

CONTENT = os.path.join(ROOT, 'content')
VIDEOS = json.load(open(os.path.join(ROOT, 'data', 'videos.json'), encoding='utf-8'))


def read(lang, name):
    p = os.path.join(CONTENT, lang, name + '.html')
    s = open(p, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n(.*)$', s, re.S)
    meta = {}
    for line in m.group(1).split('\n'):
        if ':' in line and not line.startswith('#'):
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip()
    return meta, m.group(2)


def split_faq(body):
    faq = []
    for block in re.findall(r'<faq>(.*?)</faq>', body, re.S):
        # an answer runs to the </a> just before the next <q> (or the end), so it can hold links of its own
        faq += [(re.sub(r'\s+', ' ', q).strip(), a.strip())
                for q, a in re.findall(r'<q>(.*?)</q>\s*<a>(.*?)</a>\s*(?=<q>|$)', block.strip(), re.S)]
    return re.sub(r'<faq>.*?</faq>', '', body, flags=re.S), faq


def guide_card(name, lang):
    en, hi, photo, len_, lhi = GUIDES[name]
    title, line = L(lang, en, hi), L(lang, len_, lhi)
    if photo:
        return pcard(href('/' + name + '/', lang), pbase(photo), title, line, sizes='(max-width:700px) 80vw, 380px')
    return (f'<a class="card icard" href="{href("/" + name + "/", lang)}"><span class="i">{icon("mountain")}</span>'
            f'<span><b>{title}</b><span>{line}</span></span></a>')


def video_cards(ids, lang):
    out = []
    for v in ids:
        t = VIDEOS.get(v, {})
        title = t.get(lang) or t.get('en') or 'Karsog Miles'
        out.append(f'<a class="vcard" href="https://www.youtube.com/watch?v={v}" target="_blank" rel="noopener">'
                   f'<span class="th"><img src="https://i.ytimg.com/vi/{v}/mqdefault.jpg" width="320" height="180" loading="lazy" decoding="async" '
                   f'alt="{esc(title)}"></span><span class="bd"><b>{esc(title)}</b><small>Karsog Miles · YouTube</small></span></a>')
    return '<div class="ytg">' + ''.join(out) + '</div>'


def model(name, lang):
    meta, body = read(lang, name)
    body, faq = split_faq(body)
    path = '/' + name + '/'
    hero = meta.get('hero', 'band')
    chips = []
    for c in filter(None, [x.strip() for x in meta.get('chips', '').split('|')]):
        ic, tx = c.split(':', 1)
        chips.append((ic.strip(), tx.strip()))
    # --- aside: at a glance + directions + bus
    kv = ''
    for c in filter(None, [x.strip() for x in meta.get('glance', '').split('|')]):
        k, v = c.split('=', 1)
        kv += f'<dt>{k.strip()}</dt><dd>{v.strip()}</dd>'
    btns = ''
    dest = meta.get('geo') or quote_plus(meta.get('dest', ''))
    if dest:
        btns += (f'<a class="btn btn-p" href="https://www.google.com/maps/dir/?api=1&amp;destination={dest}" target="_blank" rel="noopener">'
                 f'{icon("nav")}{L(lang, "Directions", "रास्ता देखें")}</a>')
    if meta.get('bus'):
        btns += f'<a class="btn btn-o" href="{href(meta["bus"], lang)}">{icon("bus")}{L(lang, "Bus timings", "बसों का समय")}</a>'
    btns += f'<button type="button" class="btn btn-o" data-open="upd">{icon("msg")}{L(lang, "Suggest a correction", "सुधार सुझाएँ")}</button>'
    aside = (f'<aside class="aside-box"><div class="card"><h3>{L(lang, "At a glance", "एक नज़र में")}</h3><dl class="kv">{kv}</dl>'
             f'<div class="btns">{btns}</div></div></aside>')
    main = section(f'<div class="split"><div class="prose">{body}</div>{aside}</div>', '', 'guide')
    # --- photos, videos, related, comments, faq
    extra = ''
    g = meta.get('gallery')
    if g and BY_SLUG.get(g):
        ph = BY_SLUG[g]
        extra += section(shead(L(lang, 'From the air', 'आसमान से'), L(lang, f'{len(ph)} drone <em>photos</em>', f'{len(ph)} ड्रोन <em>फ़ोटो</em>'),
                               L(lang, 'Tap a photo to see it full size.', 'फ़ोटो को बड़ा देखने के लिए छुएँ।'))
                         + gallery(ph, lang, lambda p: photo_label(p, lang), lambda p: photo_alt(p, lang)), 'sec-alt', 'photos')
    if meta.get('videos'):
        extra += section(shead(L(lang, 'Watch the road', 'रास्ता देखें'), L(lang, 'Ride <em>videos</em>', 'राइड <em>वीडियो</em>'),
                               L(lang, 'Filmed on the way by Karsog Miles. They open on YouTube.', 'Karsog Miles के रास्ते के वीडियो। ये यूट्यूब पर खुलते हैं।'),
                               more=(L(lang, 'All ride videos', 'सभी राइड वीडियो'), href('/rides/', lang)))
                         + video_cards(meta['videos'].split(), lang), '', 'videos')
    if meta.get('related'):
        cards = ''.join(guide_card(r, lang) for r in meta['related'].split())
        extra += section(shead(L(lang, 'Nearby', 'आसपास'), L(lang, 'Make a day of <em>it</em>', 'साथ में <em>घूमें</em>')) +
                         f'<div class="grid g3">{cards}</div>', 'sec-alt', 'nearby')
    extra += comments(name, lang)
    extra += faq_block(faq, lang)
    crumbs = []
    if meta.get('crumb'):
        n, p = meta['crumb'].split('=')
        crumbs.append((n.strip(), p.strip()))
    crumbs.append((re.sub(r'<[^>]+>', '', meta.get('card', meta['h1'])), path))
    ld = []
    if meta.get('schema'):
        o = {'@context': 'https://schema.org', '@type': meta['schema'], 'name': re.sub(r'<[^>]+>', '', meta.get('card', meta['h1'])),
             'description': meta['desc'], 'url': 'https://karsog.com' + href(path, lang),
             'address': {'@type': 'PostalAddress', 'addressLocality': 'Karsog', 'addressRegion': 'Himachal Pradesh', 'addressCountry': 'IN'}}
        if meta.get('geo'):
            la, lo = meta['geo'].split(',')
            o['geo'] = {'@type': 'GeoCoordinates', 'latitude': float(la), 'longitude': float(lo)}
        if hero != 'band':
            o['image'] = f'https://karsog.com{pbase(hero)}-1600.webp'
        ld.append(o)
    if faq:
        ld.append(faq_ld(faq))
    acts = []
    if dest:
        acts.append((L(lang, 'Directions', 'रास्ता देखें'), f'https://www.google.com/maps/dir/?api=1&amp;destination={dest}', 'g', 'nav'))
    if meta.get('bus'):
        acts.append((L(lang, 'Bus timings', 'बसों का समय'), href(meta['bus'], lang), 'w', 'bus'))
    m = dict(path=path, lang=lang, kind='guide', actions=acts, title=meta['title'], desc=meta['desc'], kicker=meta.get('kicker', ''),
             h1=meta['h1'], lede=meta.get('lede', ''), chips=chips, crumbs=crumbs, body=main + extra, ld=ld)
    if hero != 'band':
        m['hero'] = 'photo'
        m['img'] = {'src': pbase(hero), 'alt': meta.get('hero_alt', ''), 'pos': meta.get('hero_pos')}
    else:
        m['hero'] = 'band'
    return m


def available(lang):
    d = os.path.join(CONTENT, lang)
    return sorted(f[:-5] for f in os.listdir(d) if f.endswith('.html')) if os.path.isdir(d) else []
