"""The 404 page (public/404.html), shown by Cloudflare for any address that does not exist."""
from layout import L, icon, section, shead, href
from p_photos import place_card
from data import BY_SLUG, PLACES


def not_found(lang='en'):
    links = [('/', 'home', 'karsog.com home'), ('/karsog-bus-stand/', 'bus', 'Bus timings'), ('/mandi-to-karsog-bus/', 'bus', 'Mandi ⇄ Karsog bus'),
             ('/shimla-to-karsog-bus/', 'bus', 'Shimla ⇄ Karsog bus'), ('/places/', 'pin', 'Places to visit'), ('/weather/', 'weather', 'Weather'),
             ('/mandi-rates/', 'apple', 'Mandi rates'), ('/photos/', 'camera', 'Drone photos'), ('/hi/', 'lang', 'हिंदी में पढ़ें')]
    hi_attr = ' lang="hi"'
    btns = ''.join(f'<a class="btn {"btn-p" if u == "/" else "btn-o"}" href="{u}"{hi_attr if u == "/hi/" else ""}>{icon(ic)}{t}</a>'
                   for u, ic, t in links)
    top = [p['slug'] for p in sorted(PLACES, key=lambda p: -len(BY_SLUG.get(p['slug'], [])))][:6]
    body = (section(f'<div class="btns">{btns}</div>', 'sec-tight', 'links')
            + section(shead('Karsog from above', 'Places <em>from above</em>') + '<div class="grid g3">'
                      + ''.join(place_card(s, 'en', '(max-width:700px) 80vw, 380px') for s in top) + '</div>', 'sec-alt', 'places'))
    return dict(path='/404.html', lang='en', kind='page', hero='band', alt=False, noindex=True,
                title='Page not found — karsog.com', desc='This page isn’t here. Try the karsog.com home page, bus timings or places to visit.',
                kicker='404', h1='This page <em>isn’t here</em>',
                lede='The link may be old or mistyped. Try one of these, or use the menu. <span lang="hi">यह पेज नहीं मिला — ऊपर के मेन्यू से या हिंदी होम पेज से आगे बढ़ें।</span>',
                body=body)
