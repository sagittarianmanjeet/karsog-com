"""Page layout for karsog.com: every page, in English and Hindi, is rendered by page() below.

A page is described by a small dict (the "model"). page() turns it into a complete HTML document
with the shared header, menus, footer, language switch, SEO tags and structured data.
Look: /assets/site.css   Behaviour: /assets/site.js   Icons: /assets/icons.svg (Lucide, ISC licence)

Model keys (only path, lang, title, desc, h1 and body are required):
  path      English path of the page, e.g. '/mahunag/' (the Hindi copy lives at '/hi/mahunag/')
  lang      'en' or 'hi'
  title     <title> text (aim for 60 characters or fewer)
  desc      meta description (aim for 150-160 characters)
  h1, kicker, lede          page heading, small line above it, paragraph below it (HTML allowed)
  hero      'home' | 'photo' | 'band' (default) | 'none'
  img       photo for a 'photo' hero or the share image: {'src': '/photos/x/x-001', 'alt': '...', 'pos': 'center 40%'}
  chips     [(icon, text)]            short facts under the heading
  actions   [(text, href, style, icon)]  buttons under the heading; style is g (gold), w (white), p, o
  crumbs    [(label, path)]           breadcrumb after Home; the last one is this page
  body      the page content (HTML)
  ld        extra structured data (list of dicts)
  og        share image path (1200x630 JPG), defaults to the hero photo
  kind      CSS hook on <body>, e.g. 'guide'
  data      {id: object} JSON embedded for site.js (next bus, weather ...)
  alt       False when the page has no copy in the other language
  noindex   True for pages Google should not list (404)
"""
import hashlib, html, json, os, re
from ui import NAV, MORE, BOTTOM, SUBNAV, t, label, section_of, lpath

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, 'public')
SITE = 'https://karsog.com'
GA = 'G-P4GZFJ5XQG'
WA = '917018485157'
TURNSTILE = '0x4AAAAAAFB76cvJ7UlhXYzU'
YEAR = '2026'
esc = html.escape


def _ver():
    """Short hash of the shared files, added to their links so browsers fetch new versions after a change."""
    h = hashlib.md5()
    d = os.path.join(PUB, 'assets')
    for f in sorted(os.listdir(d)):
        if f.endswith(('.css', '.js', '.svg')):
            h.update(open(os.path.join(d, f), 'rb').read())
    return h.hexdigest()[:8]


V = _ver()
ICONS = f'/assets/icons.svg?v={V}'


def icon(name, cls='ico'):
    return f'<svg class="{cls}" aria-hidden="true"><use href="{ICONS}#i-{name}"/></svg>'


def L(lang, en, hi):
    """Pick the English or Hindi text."""
    return en if lang == 'en' else hi


def href(path, lang):
    """Link to a page of this site in the current language (external links and #anchors pass through)."""
    if not path.startswith('/') or path.startswith('//') or path.startswith('/photos/') or path.startswith('/assets/') \
            or path.startswith('/rti/files/') or re.search(r'\.(webp|jpg|png|pdf|json|xml|js|css)$', path):
        return path
    return lpath(path, lang)


LOGO = ('<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="17" fill="#15382a"/>'
        '<circle cx="45" cy="20" r="6.5" fill="#e0b453"/>'
        '<path d="M4 52 21 27l8 10 11-16 20 31z" fill="#2c6a4d"/>'
        '<path d="M4 52l14-14 8 7 10-11 9 9 5-4 10 13z" fill="#f2ecdf"/></svg>')

RIDGE = ('<svg class="ridge" viewBox="0 0 1440 64" preserveAspectRatio="none" aria-hidden="true">'
         '<path fill="currentColor" opacity=".42" d="M0 34 60 26 120 34 200 14 270 30 340 20 420 34 500 10 570 26 640 18 720 32 '
         '800 8 880 28 950 20 1030 34 1110 12 1180 28 1250 18 1330 30 1400 20 1440 26V64H0Z"/>'
         '<path fill="currentColor" d="M0 50 90 40 170 48 260 34 340 46 430 38 520 50 610 36 700 46 790 40 880 52 970 38 '
         '1060 48 1150 36 1240 46 1330 40 1440 48V64H0Z"/></svg>')


# ---------------------------------------------------------------- images
def srcset(base):
    return f'{base}-800.webp 800w, {base}-1600.webp 1600w'


def img(base, alt, sizes='100vw', w=800, h=450, cls='', lazy=True, pos=None):
    """A responsive drone photo: base is '/photos/<place>/<file>' without the -800/-1600 ending."""
    extra = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    style = f' style="object-position:{pos}"' if pos else ''
    c = f' class="{cls}"' if cls else ''
    return (f'<img{c} src="{base}-800.webp" srcset="{srcset(base)}" sizes="{sizes}" width="{w}" height="{h}" '
            f'alt="{esc(alt)}" decoding="async"{extra}{style}>')


# ---------------------------------------------------------------- small components
def section(inner, cls='', id=None, wrap='wrap'):
    i = f' id="{id}"' if id else ''
    return f'<section class="sec {cls}"{i}><div class="{wrap}">{inner}</div></section>\n'


def shead(eyebrow, title, lede='', center=False, more=None):
    c = ' center' if center else ''
    ey = f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ''
    ld = f'<p class="lede">{lede}</p>' if lede else ''
    mo = f'<p class="mt1"><a class="more-link" href="{more[1]}">{more[0]} {icon("arrow")}</a></p>' if more else ''
    return f'<div class="head{c}">{ey}<h2>{title}</h2>{ld}{mo}</div>'


def note(inner, kind=''):
    return f'<div class="note {kind}">{inner}</div>'


def facts(items):
    return '<div class="facts">' + ''.join(f'<div><b>{v}</b><small>{k}</small></div>' for v, k in items) + '</div>'


def faq_block(items, lang, title=None, eyebrow=None, id='faq'):
    """FAQ section: items are (question, answer-HTML). Pair with faq_ld() for Google."""
    if not items:
        return ''
    title = title or L(lang, 'Common <em>questions</em>', 'अक्सर पूछे जाने वाले <em>सवाल</em>')
    rows = ''.join(f'<details><summary>{esc(q)}</summary><div>{a}</div></details>' for q, a in items)
    return section(shead(eyebrow or L(lang, 'FAQ', 'सवाल-जवाब'), title) + f'<div class="faq">{rows}</div>',
                   'sec-alt', id, 'wrap wrap-n')


def faq_ld(items):
    strip = lambda s: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': strip(a)}} for q, a in items]}


def comments(page_id, lang, title=None, text=None, placeholder=None):
    """Public comments (Cloudflare Worker + Turnstile, see /comments.js)."""
    title = title or L(lang, 'Comments', 'टिप्पणियाँ')
    text = text or L(lang, 'Know this place? Share a name, a story or a correction.',
                     'इस जगह के बारे में जानते हैं? नाम, कोई कहानी या सुधार लिखें।')
    ph = placeholder or L(lang, 'Your comment, question or correction.', 'आपकी टिप्पणी, सवाल या सुधार।')
    warn = L(lang, 'Comments are public. Please don’t share Aadhaar, PAN, phone numbers or other personal details.',
             'टिप्पणियाँ सबको दिखती हैं। आधार, पैन, फ़ोन नंबर या कोई निजी जानकारी न लिखें।')
    return section(f'<div class="head"><h2>{title}</h2><p class="lede">{text} <small>{warn}</small></p></div>'
                   f'<div id="kc" data-page="{page_id}" data-sitekey="{TURNSTILE}" data-lang="{lang}" '
                   f'data-placeholder="{esc(ph)}"></div><script src="/comments.js?v=3" defer></script>',
                   'sec-tight', 'comments', 'wrap wrap-n')


def gallery(photos, lang, caption=None):
    """Masonry of drone photos that open full size in a lightbox. photos: dicts from photos.json."""
    out = []
    for p in photos:
        base = f'/photos/{p["slug"]}/{p["file"]}'
        cap = caption(p) if caption else p['place']
        w, h = (p.get('w') or 1600) // 2, (p.get('h') or 900) // 2
        out.append(f'<a href="{base}-1600.webp" data-cap="{esc(cap)}">'
                   f'{img(base, cap, "(max-width:560px) 50vw, (max-width:980px) 33vw, 380px", w, h)}<span>{esc(cap)}</span></a>')
    return f'<div class="gallery">{"".join(out)}</div>'


def pcard(url, base, title, meta='', tag='', cls='', sizes='(max-width:700px) 80vw, 300px', alt=None):
    tg = f'<span class="tag">{tag}</span>' if tag else ''
    mt = f'<small>{meta}</small>' if meta else ''
    return (f'<a class="pcard {cls}" href="{url}">{img(base, alt or title, sizes)}{tg}'
            f'<span class="t"><b>{title}</b>{mt}</span></a>')


def icard(url, ic, title, text):
    return (f'<a class="card icard" href="{url}"><span class="i">{icon(ic)}</span>'
            f'<span><b>{title}</b><span>{text}</span></span></a>')


def ld_breadcrumb(crumbs, lang):
    items = [(L(lang, 'Home', 'होम'), lpath('/', lang))] + [(n, lpath(p, lang)) for n, p in crumbs if p]
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': re.sub(r'<[^>]+>', '', n), 'item': SITE + p}
        for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- page parts
FONT_PRELOAD = {
    'en': ['dm-sans-latin-wght-normal', 'playfair-display-latin-wght-normal'],
    'hi': ['dm-sans-latin-wght-normal', 'tiro-devanagari-hindi-devanagari-400-normal'],
}


def _head(m):
    lang, path = m['lang'], m['path']
    url = SITE + lpath(path, lang)
    alt = m.get('alt', True)
    title, desc = m['title'], m['desc']
    img_ = m.get('img') or {}
    og = m.get('og') or (img_.get('src') and f'/og/{img_["src"].split("/")[-1]}.jpg') or '/og/karsog-valley.jpg'
    og_alt = img_.get('alt') or L(lang, 'Karsog valley, Mandi, Himachal Pradesh', 'करसोग घाटी, मंडी, हिमाचल प्रदेश')
    h = ['<!DOCTYPE html>', f'<html lang="{lang}">', '<head>', '<meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
         f'<title>{esc(title)}</title>', f'<meta name="description" content="{esc(desc)}">']
    if m.get('noindex'):
        h.append('<meta name="robots" content="noindex">')
    else:
        h.append('<meta name="robots" content="max-image-preview:large">')
        h.append(f'<link rel="canonical" href="{url}">')
        if alt:
            h += [f'<link rel="alternate" hreflang="en" href="{SITE + lpath(path, "en")}">',
                  f'<link rel="alternate" hreflang="hi" href="{SITE + lpath(path, "hi")}">',
                  f'<link rel="alternate" hreflang="x-default" href="{SITE + lpath(path, "en")}">']
    h += ['<meta property="og:site_name" content="karsog.com">',
          f'<meta property="og:type" content="{"website" if path == "/" else "article"}">',
          f'<meta property="og:locale" content="{"en_IN" if lang == "en" else "hi_IN"}">',
          f'<meta property="og:title" content="{esc(m.get("og_title") or title)}">',
          f'<meta property="og:description" content="{esc(desc)}">',
          f'<meta property="og:url" content="{url}">',
          f'<meta property="og:image" content="{SITE}{og}">',
          '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
          f'<meta property="og:image:alt" content="{esc(og_alt)}">',
          '<meta name="twitter:card" content="summary_large_image">',
          '<meta name="theme-color" content="#15382a">',
          '<link rel="icon" href="/favicon.ico" sizes="32x32"><link rel="icon" href="/assets/logo.svg" type="image/svg+xml">',
          '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
          '<link rel="manifest" href="/manifest.webmanifest">']
    for f in FONT_PRELOAD[lang]:
        h.append(f'<link rel="preload" href="/assets/fonts/{f}.woff2" as="font" type="font/woff2" crossorigin>')
    if m.get('hero') in ('home', 'photo') and img_.get('src'):
        b = img_['src']
        h.append(f'<link rel="preload" as="image" href="{b}-1600.webp" imagesrcset="{srcset(b)}" imagesizes="100vw" fetchpriority="high">')
    h.append(f'<link rel="stylesheet" href="/assets/site.css?v={V}">')
    h.append('<script>document.documentElement.classList.add("js")</script>')
    lds = [ld_breadcrumb(m.get('crumbs', []), lang)] if path != '/' else []
    lds += m.get('ld', [])
    for x in lds:
        h.append('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False, separators=(',', ':')) + '</script>')
    h.append(f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>')
    h.append('<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
             f'gtag("js",new Date());gtag("config","{GA}");</script>')
    h.append('</head>')
    return '\n'.join(h)


def _cur(item_path, m):
    """aria-current for a menu link: 'page' on the page itself, 'true' for its section."""
    base = m['path']
    if item_path == base:
        return ' aria-current="page"'
    return ''


def _header(m):
    lang, path = m['lang'], m['path']
    sec = section_of(path)
    over = ' over' if m.get('hero') == 'home' else ''
    links = []
    for k, en, hi, p, ic in NAV:
        a = _cur(p, m) or (' aria-current="true"' if k == sec and path != p else '')
        links.append(f'<a href="{lpath(p, lang)}"{a}>{label((k, en, hi), lang)}</a>')
    more_on = any(p == path for k, en, hi, p, ic in MORE) or sec in [k for k, *_ in MORE]
    menu = ''.join(f'<a href="{lpath(p, lang)}"{_cur(p, m)}>{icon(ic)}{label((k, en, hi), lang)}</a>'
                   for k, en, hi, p, ic in MORE)
    other = 'hi' if lang == 'en' else 'en'
    sw = ''
    if m.get('alt', True):
        sw = (f'<a class="lang-sw" href="{lpath(path, other)}" hreflang="{other}" lang="{other}" '
              f'title="{t("switch_label", lang)}">{icon("lang")}<span>{t("switch", lang)}</span></a>')
    home = lpath('/', lang)
    return (f'<a class="skip" href="#main">{t("skip", lang)}</a>\n'
            f'<header class="site-h{over}" id="top"><div class="wrap bar">'
            f'<a class="logo" href="{home}" aria-label="karsog.com — {t("home", lang)}">{LOGO}<b>karsog<i>.com</i></b></a>'
            f'<nav class="nav" aria-label="{L(lang, "Main menu", "मुख्य मेन्यू")}">{"".join(links)}'
            f'<div class="more"><button type="button" class="{"on" if more_on else ""}" aria-expanded="false" aria-haspopup="true">'
            f'{t("more", lang)}{icon("chevd")}</button><div class="more-menu">{menu}</div></div></nav>'
            f'<div class="h-actions">{sw}</div></div></header>\n')


def _subnav(m):
    lang, path = m['lang'], m['path']
    key = m.get('subnav') or section_of(path)
    items = SUBNAV.get(key)
    if not items:
        return ''
    links = ''.join(f'<a href="{lpath(p, lang)}"{_cur(p, m)}>{en if lang == "en" else hi}</a>' for en, hi, p in items)
    return f'<nav class="subnav" aria-label="{L(lang, "In this section", "इस भाग में")}"><div class="wrap">{links}</div></nav>\n'


def _crumbs(m):
    lang = m['lang']
    cr = m.get('crumbs') or []
    if m['path'] == '/' or not cr:
        return ''
    parts = [f'<a href="{lpath("/", lang)}">{t("home", lang)}</a>']
    for i, (n, p) in enumerate(cr):
        if i == len(cr) - 1:
            parts.append(f'<span aria-current="page">{n}</span>')
        else:
            parts.append(f'<a href="{lpath(p, lang)}">{n}</a>')
    sep = '<span aria-hidden="true">/</span>'
    return f'<nav class="crumbs" aria-label="{L(lang, "Breadcrumb", "आप यहाँ हैं")}">{sep.join(parts)}</nav>'


def _chips(m, light=False):
    c = m.get('chips') or []
    if not c:
        return ''
    cl = ' chip-l' if light else ''
    return '<div class="chips">' + ''.join(f'<span class="chip{cl}">{icon(i)}{x}</span>' for i, x in c) + '</div>'


def _actions(m):
    a = m.get('actions') or []
    if not a:
        return ''
    out = []
    for x in a:
        text, url, style = x[0], x[1], x[2] if len(x) > 2 else 'g'
        ic = icon(x[3]) if len(x) > 3 and x[3] else ''
        ext = ' target="_blank" rel="noopener"' if url.startswith('http') else ''
        out.append(f'<a class="btn btn-{style}" href="{url}"{ext}>{ic}{text}</a>')
    return '<div class="hero-actions">' + ''.join(out) + '</div>'


def _hero(m):
    kind = m.get('hero', 'band')
    if kind == 'none':
        return ''
    kick = m.get('kicker', '')
    lede = f'<p class="lede">{m["lede"]}</p>' if m.get('lede') else ''
    if kind in ('home', 'photo'):
        im = m['img']
        k = f'<span class="kicker">{kick}</span>' if kick else ''
        credit = f'<span class="photo-credit">{im["credit"]}</span>' if im.get('credit') else ''
        cls = 'hero hero-home' if kind == 'home' else 'hero hero-photo'
        extra = m.get('hero_extra', '')
        return (f'<header class="{cls} on-photo">'
                f'{img(im["src"], im["alt"], "100vw", 1600, 900, "bg", lazy=False, pos=im.get("pos"))}'
                f'<div class="wrap in">{_crumbs(m)}{k}<h1>{m["h1"]}</h1>{lede}{_chips(m)}{_actions(m)}{extra}</div>'
                f'{credit}{RIDGE}</header>\n')
    ey = f'<span class="eyebrow">{kick}</span>' if kick else ''
    return (f'<header class="band"><div class="wrap">{_crumbs(m)}{ey}<h1>{m["h1"]}</h1>{lede}{_chips(m)}{_actions(m)}'
            f'{m.get("hero_extra", "")}</div>{RIDGE}</header>\n')


def _footer(m):
    lang = m['lang']
    lk = lambda p, en, hi: f'<li><a href="{lpath(p, lang)}">{L(lang, en, hi)}</a></li>'
    travel = ''.join([lk('/karsog-bus-stand/', 'Karsog bus timings', 'करसोग बस समय'),
                      lk('/karsog-private-bus/', 'Private buses', 'प्राइवेट बसें'),
                      lk('/mandi-to-karsog-bus/', 'Mandi ⇄ Karsog buses', 'मंडी ⇄ करसोग बसें'),
                      lk('/shimla-to-karsog-bus/', 'Shimla ⇄ Karsog buses', 'शिमला ⇄ करसोग बसें'),
                      lk('/distance/', 'Distances', 'दूरी'), lk('/weather/', 'Weather', 'मौसम'),
                      lk('/hotels/', 'Hotels', 'होटल'), lk('/plan/', 'Plan a trip', 'यात्रा योजना')])
    explore = ''.join([lk('/places/', 'Places to visit', 'घूमने की जगहें'), lk('/temples/', 'Temples', 'मंदिर'),
                       lk('/melas/', 'Melas & festivals', 'मेले और त्योहार'), lk('/photos/', 'Drone photos', 'ड्रोन फ़ोटो'),
                       lk('/rides/', 'Ride videos', 'राइड वीडियो'), lk('/shikari-devi/', 'Shikari Devi', 'शिकारी देवी'),
                       lk('/kamru-nag/', 'Kamru Nag', 'कमरूनाग'), lk('/tattapani/', 'Tattapani', 'तत्तापानी')])
    local = ''.join([lk('/contacts/', 'Useful numbers', 'ज़रूरी नंबर'), lk('/mandi-rates/', 'Mandi rates', 'मंडी भाव'),
                     lk('/rti/', 'RTI replies', 'आरटीआई जवाब'),
                     f'<li><a href="#update" data-open="upd">{t("send_update", lang)}</a></li>',
                     '<li><a href="https://www.youtube.com/@KarsogMiles" target="_blank" rel="noopener">Karsog Miles · YouTube</a></li>',
                     '<li><a href="https://www.facebook.com/KarsogMiles/" target="_blank" rel="noopener">Karsog Miles · Facebook</a></li>'])
    other = 'hi' if lang == 'en' else 'en'
    sw = ''
    if m.get('alt', True):
        sw = (f'<a class="lang-sw" href="{lpath(m["path"], other)}" hreflang="{other}" lang="{other}">'
              f'{icon("lang")}{t("switch_label", lang)}</a>')
    return (f'<footer class="site-f"><div class="wrap"><div class="f-top">'
            f'<div class="f-brand"><a class="logo" href="{lpath("/", lang)}">{LOGO}<b>karsog<i>.com</i></b></a>'
            f'<p>{t("tagline", lang)}</p><p><small>{t("made_by", lang)}</small></p></div>'
            f'<div class="f-col"><h3>{t("f_travel", lang)}</h3><ul>{travel}</ul></div>'
            f'<div class="f-col"><h3>{t("f_explore", lang)}</h3><ul>{explore}</ul></div>'
            f'<div class="f-col"><h3>{t("f_local", lang)}</h3><ul>{local}</ul></div></div>'
            f'<div class="f-bot"><span>© {YEAR} karsog.com · {t("copyright", lang)} · '
            f'<a href="https://pinkyfancystore.com" target="_blank" rel="noopener">Pinky Fancy Store</a> · '
            f'<a href="https://toolninja.in" target="_blank" rel="noopener">ToolNinja</a></span>{sw}</div>'
            f'</div></footer>\n')


def _bottom(m):
    lang, path = m['lang'], m['path']
    sec = section_of(path)
    out = []
    for k, en, hi, p, ic in BOTTOM:
        cur = ' aria-current="page"' if (p == path or (k == sec and k != 'home')) else ''
        out.append(f'<a href="{lpath(p, lang)}"{cur}>{icon(ic)}<span>{label((k, en, hi), lang)}</span></a>')
    out.append(f'<button type="button" data-open="sheet" aria-controls="sheet" aria-expanded="false">{icon("grid")}'
               f'<span>{t("menu", lang)}</span></button>')
    return f'<nav class="bottom" aria-label="{L(lang, "Quick links", "मुख्य लिंक")}">{"".join(out)}</nav>\n'


def _sheet(m):
    lang, path = m['lang'], m['path']
    items = [('home', 'Home', 'होम', '/', 'home')] + NAV + MORE
    grid = ''.join(f'<a href="{lpath(p, lang)}"{_cur(p, m)}>{icon(ic)}{label((k, en, hi), lang)}</a>'
                   for k, en, hi, p, ic in items)
    other = 'hi' if lang == 'en' else 'en'
    sw = ''
    if m.get('alt', True):
        sw = f'<a href="{lpath(path, other)}" hreflang="{other}" lang="{other}">{icon("lang")}{t("switch_label", lang)}</a>'
    return (f'<div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-label="{t("menu", lang)}" hidden>'
            f'<div class="sheet-bg" data-close></div><div class="sheet-p">'
            f'<div class="sheet-top"><b>karsog.com</b><button type="button" class="menu-btn" data-close aria-label="{t("close", lang)}">'
            f'{icon("x")}</button></div><div class="sheet-grid">{grid}</div>'
            f'<div class="sheet-foot">{sw}<button type="button" data-open="upd">{icon("msg")}{t("send_update", lang)}</button></div>'
            f'</div></div>\n')


def _modal(m):
    lang = m['lang']
    types = ''.join(f'<option>{x}</option>' for x in t('modal_types', lang))
    return (f'<button type="button" class="fab" data-open="upd" aria-label="{t("send_update", lang)}">{icon("msg")}'
            f'<span>{t("send_update", lang)}</span></button>\n'
            f'<div class="modal" id="upd" role="dialog" aria-modal="true" aria-labelledby="upd-t" hidden>'
            f'<div class="modal-box"><button type="button" class="x" data-close aria-label="{t("close", lang)}">{icon("x")}</button>'
            f'<h2 id="upd-t">{t("modal_title", lang)}</h2><p>{t("modal_sub", lang)}</p>'
            f'<form class="form" data-wa="{WA}"><label>{t("modal_type", lang)}<select name="type">{types}</select></label>'
            f'<label>{t("modal_text", lang)}<textarea name="text" required></textarea></label>'
            f'<label>{t("modal_name", lang)}<input name="name" autocomplete="name"></label>'
            f'<p class="kc-msg" role="status" data-empty="{esc(t("modal_empty", lang))}"></p>'
            f'<button class="btn btn-p" type="submit">{icon("msg")}{t("modal_send", lang)}</button></form></div></div>\n')


def page(m):
    """Complete HTML document for a page model."""
    m.setdefault('crumbs', [])
    data = ''.join(f'<script type="application/json" id="{k}">{json.dumps(v, ensure_ascii=False, separators=(",", ":"))}</script>'
                   for k, v in (m.get('data') or {}).items())
    kind = m.get('kind', 'page')
    body = m['body']
    return (_head(m) + f'\n<body class="k-{kind}">\n' + _header(m) + _subnav(m) +
            f'<main id="main">\n{_hero(m)}{body}</main>\n' + _footer(m) + _bottom(m) + _sheet(m) + _modal(m) +
            data + f'\n<script src="/assets/site.js?v={V}" defer></script>\n' +
            ''.join(f'<script src="{x}?v={V}" defer></script>\n' for x in m.get('scripts', [])) + '</body>\n</html>\n')


def out_path(path, lang):
    p = lpath(path, lang)
    if p.endswith('.html'):
        return os.path.join(PUB, p.lstrip('/'))
    return os.path.join(PUB, p.strip('/'), 'index.html') if p != '/' else os.path.join(PUB, 'index.html')


def write(m):
    f = out_path(m['path'], m['lang'])
    os.makedirs(os.path.dirname(f), exist_ok=True)
    s = page(m)
    open(f, 'w', encoding='utf-8').write(s)
    return f
