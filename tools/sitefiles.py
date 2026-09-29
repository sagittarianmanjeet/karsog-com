"""Site-wide files made after the pages: sitemap.xml (with the English/Hindi pairs), share images and app icons.

Called by build.py after a full build:
  sitemap.xml   every indexable page, its other-language twin (hreflang) and its drone photos (image sitemap)
  /og/*.jpg     1200x630 share images cut from the hero photos (made once; delete a file to remake it)
  icons         /favicon.ico, /apple-touch-icon.png, /icon-192.png, /icon-512.png and /assets/logo.svg, drawn from the logo"""
import os, re
from xml.sax.saxutils import escape as xesc
from layout import SITE, PUB, LOGO, lpath
from data import BY_SLUG, PHOTOS

# share image -> drone photo it is cut from (the others are named after their photo, e.g. /og/mahunag-214.jpg)
OG_SRC = {'home': 'nyara-004', 'karsog-valley': 'nyara-004', 'weather': 'karsog-town-013', 'mandi': 'nyara-015', 'rti': 'karsog-town-081', 'bus': 'karsog-town-048'}


def _photo_path(file):
    p = next((x for x in PHOTOS if x['file'] == file), None)
    return os.path.join(PUB, 'photos', p['slug'], p['file'] + '-1600.webp') if p else None


def og_images(models):
    from PIL import Image
    made, missing = [], []
    for m in models:
        og = m.get('og') or (m.get('img') or {}).get('src') and f'/og/{m["img"]["src"].split("/")[-1]}.jpg' or '/og/karsog-valley.jpg'
        name = og.split('/')[-1][:-4]
        out = os.path.join(PUB, 'og', name + '.jpg')
        if os.path.exists(out):
            continue
        src = _photo_path(OG_SRC.get(name, name))
        if not src or not os.path.exists(src):
            missing.append(og)
            continue
        im = Image.open(src).convert('RGB')
        w, h = im.size
        tw, th = 1200, 630
        k = max(tw / w, th / h)
        im = im.resize((round(w * k), round(h * k)), Image.LANCZOS)
        x, y = (im.width - tw) // 2, (im.height - th) // 2
        os.makedirs(os.path.dirname(out), exist_ok=True)
        im.crop((x, y, x + tw, y + th)).save(out, 'JPEG', quality=82, optimize=True, progressive=True)
        made.append(name)
    return made, sorted(set(missing))


def _draw_logo(size):
    """The karsog.com logo (see layout.LOGO) drawn with Pillow: green tile, gold sun, two ridges."""
    from PIL import Image, ImageDraw
    S = size * 4                      # draw big, then shrink for smooth edges
    k = S / 64
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=17 * k, fill='#15382a')
    d.ellipse([(45 - 6.5) * k, (20 - 6.5) * k, (45 + 6.5) * k, (20 + 6.5) * k], fill='#e0b453')
    pts = lambda p: [(x * k, y * k) for x, y in p]
    d.polygon(pts([(4, 52), (21, 27), (29, 37), (40, 21), (60, 52)]), fill='#2c6a4d')
    d.polygon(pts([(4, 52), (18, 38), (26, 45), (36, 34), (45, 43), (50, 39), (60, 52)]), fill='#f2ecdf')
    return im.resize((size, size), Image.LANCZOS)


def icons():
    made = []
    svg = os.path.join(PUB, 'assets', 'logo.svg')
    if not os.path.exists(svg):
        open(svg, 'w').write(LOGO.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ').replace(' aria-hidden="true"', '') + '\n')
        made.append('logo.svg')
    targets = {'apple-touch-icon.png': 180, 'icon-192.png': 192, 'icon-512.png': 512}
    stamp = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.icons-from-logo')   # kept out of public/
    if not os.path.exists(stamp):          # replace the old icons once; after that only missing files are made
        for f in targets:
            if os.path.exists(os.path.join(PUB, f)):
                os.remove(os.path.join(PUB, f))
    for f, s in targets.items():
        p = os.path.join(PUB, f)
        if not os.path.exists(p):
            im = _draw_logo(s)
            if f == 'apple-touch-icon.png':   # iOS shows transparent corners as black
                from PIL import Image
                bg = Image.new('RGB', im.size, '#15382a'); bg.paste(im, mask=im); im = bg
            im.save(p, optimize=True)
            made.append(f)
    ico = os.path.join(PUB, 'favicon.ico')
    if not os.path.exists(ico):
        _draw_logo(64).save(ico, sizes=[(16, 16), (32, 32), (48, 48)])
        made.append('favicon.ico')
    open(stamp, 'w').write('icons drawn from layout.LOGO by tools/sitefiles.py\n')
    return made


def sitemap(models):
    by_path = {}
    for m in models:
        if m.get('noindex'):
            continue
        by_path.setdefault(lpath(m['path'], 'en'), {})[m['lang']] = m
    rows = []
    for path, langs in sorted(by_path.items(), key=lambda x: (x[0] != '/', x[0])):
        both = 'en' in langs and 'hi' in langs and langs['en'].get('alt', True)
        for lang, m in sorted(langs.items()):
            url = SITE + lpath(path, lang)
            x = [f'  <url><loc>{xesc(url)}</loc>']
            if both:
                x += [f'    <xhtml:link rel="alternate" hreflang="en" href="{xesc(SITE + lpath(path, "en"))}"/>',
                      f'    <xhtml:link rel="alternate" hreflang="hi" href="{xesc(SITE + lpath(path, "hi"))}"/>',
                      f'    <xhtml:link rel="alternate" hreflang="x-default" href="{xesc(SITE + lpath(path, "en"))}"/>']
            slug = path.strip('/')
            if lang == 'en' and slug in BY_SLUG:          # drone photos of this place (English copy only, to avoid duplicates)
                x += [f'    <image:image><image:loc>{SITE}/photos/{slug}/{p["file"]}-1600.webp</image:loc></image:image>'
                      for p in sorted(BY_SLUG[slug], key=lambda p: p['rank'])]
            x.append('  </url>')
            rows.append('\n'.join(x))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" '
           'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + '\n'.join(rows) + '\n</urlset>\n')
    open(os.path.join(PUB, 'sitemap.xml'), 'w', encoding='utf-8').write(xml)
    return len(rows)


def finish(models):
    n = sitemap(models)
    made, missing = og_images(models)
    ic = icons()
    out = f'sitemap: {n} URLs'
    if made:
        out += f'; share images made: {len(made)}'
    if missing:
        out += f'; share images with no source photo: {", ".join(missing)}'
    if ic:
        out += f'; icons made: {", ".join(ic)}'
    return out
