"""Add new drone photos to the site (runs on the Mac, where the original photos are).

What it does:
  1. finds new photos in the photo folders (Desktop/top-100 and Desktop/website-picks/<folder>/, file names like
     "123_Place name_2026-09-04.jpg"), works out which place page each belongs to,
  2. makes the web versions (-1600.webp and -800.webp, with the karsog.com mark) in public/photos/<place>/,
  3. updates public/photos/photos.json and places.json,
  4. runs tools/build.py, which makes every page from those files (place pages, /photos/, the home page, sitemap).

Place names -> place pages: tools/groups.py (G) if it exists on this computer; otherwise the places already in
photos.json. A photo whose place is not known is skipped with a message: add its place to data/photo-places.json and
to groups.py, then run again. Give a new photo a caption by adding a "label" to its entry in photos.json (and its Hindi
in data/photo-labels-hi.json); without one, the place name from the file name is used.

Folders (change with environment variables if yours differ):
  KARSOG_HOME   base folder that holds Desktop/ (default ~/mnt, as in the Cowork VM; on the Mac itself use ~)
  KARSOG_META   metadata files top100meta.json / picksmeta.json (default: KARSOG_HOME/..)"""
import os, re, json, sys, subprocess
from PIL import Image, ImageDraw, ImageFont

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
SITE = os.path.join(ROOT, 'public')
H = os.path.expanduser(os.environ.get('KARSOG_HOME', '~/mnt'))
DESK = os.path.join(H, 'Desktop')
TOP, PK = os.path.join(DESK, 'top-100'), os.path.join(DESK, 'website-picks')
META_DIR = os.path.expanduser(os.environ.get('KARSOG_META', '~'))


def load(p, default):
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else default


def font(size):
    for f in ['/usr/share/fonts/truetype/lato/Lato-Bold.ttf', '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
              '/Library/Fonts/Arial Bold.ttf']:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def wm(im):
    """The small 'karsog.com' mark in the bottom-right corner."""
    W, Hh = im.size
    f = font(max(14, W // 55))
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov); t = 'karsog.com'
    bw = d.textbbox((0, 0), t, font=f); w, h = bw[2] - bw[0], bw[3] - bw[1]; x, y = W - w - W // 60, Hh - h - Hh // 30
    d.text((x + 1, y + 1), t, font=f, fill=(0, 0, 0, 110)); d.text((x, y), t, font=f, fill=(255, 255, 255, 200))
    return Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')


# ---- which place page a photo belongs to
sys.path.insert(0, TOOLS)
try:
    from groups import G                      # (slug, title, sub, members, desc, has_guide)
    memb = {x: s for s, t, sub, mem, d, ex in G for x in mem}
except ImportError:
    G = None
    memb = {}
photos = load(os.path.join(SITE, 'photos', 'photos.json'), [])
for p in photos:
    memb.setdefault(p['place'], p['slug'])

META = {m['f'][:3]: m for m in load(os.path.join(META_DIR, 'top100meta.json'), [])}
PM = load(os.path.join(META_DIR, 'picksmeta.json'), {})


def srcpath(p):
    return os.path.join(DESK, p['source']) if '/' in p['source'] else os.path.join(TOP, p['source'])


# ---- collect new photos
known = {p['source'] for p in photos}
cand = [(f, f, int(f[:3])) for f in sorted(os.listdir(TOP)) if f.endswith('.jpg')] if os.path.isdir(TOP) else []
if os.path.isdir(PK):
    for d in sorted(os.listdir(PK)):
        if os.path.isdir(os.path.join(PK, d)) and not d.startswith('_'):
            cand += [(f'website-picks/{d}/{f}', f, 100 + int(f[:3])) for f in sorted(os.listdir(os.path.join(PK, d)))
                     if f.endswith('.jpg') and f[:3].isdigit()]
added = 0
for src, f, rank in cand:
    if src in known:
        continue
    raw = re.sub(r'^\d{3}_|_\d{4}-\d\d-\d\d\.jpg$', '', f); near = raw.startswith('near '); guess = raw.endswith('~')
    base = re.sub(r'^near ', '', raw.rstrip('~')); slug = memb.get(base)
    if not slug:
        print('SKIP (place not known yet):', src); continue
    g = META.get(f[:3], {}).get('g') if rank <= 100 else PM.get(f[:3], {}).get('g')
    dt = re.search(r'(\d{4})-(\d\d)-(\d\d)', f)
    photos.append(dict(source=src, rank=rank, slug=slug, place=base, near=near or guess, date=f'{dt[1]}-{dt[2]}-{dt[3]}', gps=g))
    added += 1

# ---- web versions
for s in sorted({p['slug'] for p in photos}):
    ps = sorted([p for p in photos if p['slug'] == s], key=lambda p: p['rank'])
    os.makedirs(f'{SITE}/photos/{s}', exist_ok=True)
    for p in ps:
        if 'file' not in p:
            p['file'] = f'{s}-{p["rank"]:03d}'
        big = f'{SITE}/photos/{s}/{p["file"]}-1600.webp'
        if not os.path.exists(big):
            if not os.path.exists(srcpath(p)):
                print('MISSING original for', p['file']); continue
            im = Image.open(srcpath(p)).convert('RGB')
            a = im.copy(); a.thumbnail((1600, 1600)); a = wm(a); a.save(big, 'WEBP', quality=80, method=5)
            b = im.copy(); b.thumbnail((800, 800)); b = wm(b); b.save(f'{SITE}/photos/{s}/{p["file"]}-800.webp', 'WEBP', quality=78, method=5)
            p['w'], p['h'] = a.size
json.dump(photos, open(os.path.join(SITE, 'photos', 'photos.json'), 'w'), indent=1)

# ---- places.json: one entry per place, most photos first
PP = load(os.path.join(ROOT, 'data', 'photo-places.json'), {})
titles = {s: t for s, t, *_ in G} if G else {}
old = {p['slug']: p for p in load(os.path.join(SITE, 'photos', 'places.json'), [])}
places = []
for s in {p['slug'] for p in photos}:
    ps = sorted([p for p in photos if p['slug'] == s], key=lambda p: p['rank'])
    title = (PP.get(s) or {}).get('title') or titles.get(s) or (old.get(s) or {}).get('title') or s
    places.append(dict(slug=s, title=title, n=len(ps), dist=(old.get(s) or {}).get('dist', ''), cover=f'/photos/{s}/{ps[0]["file"]}-800.webp'))
places.sort(key=lambda x: -x['n'])
json.dump(places, open(os.path.join(SITE, 'photos', 'places.json'), 'w'), indent=1)
print(f'{len(photos)} photos ({added} new), {len(places)} places')

# ---- every page, from the updated lists
subprocess.run([sys.executable, os.path.join(TOOLS, 'build.py')], cwd=ROOT, check=True)
