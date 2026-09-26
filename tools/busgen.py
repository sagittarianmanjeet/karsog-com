#!/usr/bin/env python3
"""Generate Karsog bus pages from data/karsog-bus-stand-board.csv.
Run from repo root:  python3 tools/busgen.py
Outputs: public/karsog-bus-stand/, public/bus/karsog-to-<dest>/ pages, public/data/buses.json,
and adds URLs to public/sitemap.xml between <!-- bus --> markers."""
import csv, json, os, re, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, 'public')
SRC = 'Timetable board at Karsog bus stand (HRTC), photographed 25 Sep 2026'
CHECKED = '25 Sep 2026'
esc = html.escape

# Where each departure goes when leaving Karsog. key = (line, sr)
# value: (dest_name, dest_hindi, slug or None, note)
D = {}
def d(line, sr, name, hi, slug, note=''):
    D[(line, str(sr))] = (name, hi, slug, note)
L1, L2, L3 = 'Karsog-Churag-Tattapani', 'Karsog-Pangna-Mandi', 'Karsog-Kelodhar'
d(L1, 1, 'Shimla', 'शिमला', 'shimla', 'via Bagshad'); d(L1, 2, 'Shimla', 'शिमला', 'shimla'); d(L1, 3, 'Shimla', 'शिमला', 'shimla')
d(L1, 4, 'Shimla', 'शिमला', 'shimla', 'via Bagshad; bus starts at Janjehli'); d(L1, 5, 'Shri Mool Mahunag', 'श्री मूल माहूनाग', 'mahunag')
d(L1, 6, 'Haridwar', 'हरिद्वार', 'haridwar'); d(L1, 7, 'Salana', 'सलाणा', 'salana'); d(L1, 8, 'Shimla', 'शिमला', 'shimla')
d(L1, 9, 'Shimla', 'शिमला', 'shimla', 'via Bagshad'); d(L1, 10, 'Shri Mool Mahunag', 'श्री मूल माहूनाग', 'mahunag', 'Mandi-based bus')
d(L1, 11, 'Parlog', 'परलोग', 'parlog'); d(L1, 12, 'Rodidhar', 'रोड़ीधार', 'rodidhar'); d(L1, 13, 'Shalani', 'शलानी', 'shalani')
d(L1, 14, 'Delhi', 'दिल्ली', 'delhi'); d(L1, 15, 'Salana', 'सलाणा', 'salana')
d(L2, 1, None, None, None, 'destination covered on the board'); d(L2, 2, 'Gahidhar', 'गहीधार', 'gahidhar', 'via Sorta')
d(L2, 3, 'Mandi', 'मंडी', 'mandi'); d(L2, 4, 'Dharamshala', 'धर्मशाला', 'dharamshala', 'bus starts at Jyuri')
d(L2, 5, 'Mandi', 'मंडी', 'mandi', 'via Sorta; bus starts at Shri Mool Mahunag'); d(L2, 6, 'Rewalsar', 'रिवालसर', 'rewalsar', 'bus starts at Rampur')
d(L2, 7, 'Mandi', 'मंडी', 'mandi', 'via Sorta; bus starts at Reckong Peo'); d(L2, 8, 'Khaniudi', 'खनीऊडी', 'khaniudi')
d(L2, 9, 'Nihri', 'निहरी', 'nihri', 'via Sorta'); d(L2, 10, 'Sarcha', 'सरचा', 'sarcha'); d(L2, 11, 'Sarhi', 'सरही', 'sarhi', 'via Sorta')
d(L2, 12, 'Mandi', 'मंडी', 'mandi'); d(L2, 13, None, None, None, 'destination partly covered on the board')
d(L2, 14, 'Dharamshala', 'धर्मशाला', 'dharamshala', 'bus starts at Reckong Peo'); d(L2, 15, 'Jahalma', 'जाहलमा', 'jahalma', 'bus starts at Reckong Peo')
d(L3, 1, None, None, None, 'destination partly covered on the board'); d(L3, 2, 'Reckong Peo', 'रिकांगपिओ', 'reckong-peo', 'bus starts at Dharamshala')
d(L3, 3, 'Rampur', 'रामपुर', 'rampur'); d(L3, 4, 'Thunag', 'थुनाग', 'thunag'); d(L3, 5, None, None, None, 'destination covered on the board')
d(L3, 6, 'Reckong Peo', 'रिकांगपिओ', 'reckong-peo', 'bus starts at Mandi'); d(L3, 7, None, None, None, 'destination covered on the board')
d(L3, 8, 'Gada Gushaini', 'गाड़ागुशैणी', 'gada-gushaini'); d(L3, 9, 'Somakothi', 'सोमाकोठी', 'somakothi')
d(L3, 10, 'Rampur', 'रामपुर', 'rampur', 'bus starts at Rewalsar'); d(L3, 11, 'Syanj', 'स्यांज', 'syanj'); d(L3, 12, 'Tharmi', 'थर्मी', 'tharmi')
d(L3, 13, 'Mundu', 'मुंडू', 'mundu'); d(L3, 14, 'Dateha', 'दटेहा', 'dateha'); d(L3, 15, 'Shri Dev Dwahad', 'श्री देव दवाहड़', 'dev-dwahad')
d(L3, 16, 'Pokhi', 'पोखी', 'pokhi'); d(L3, 17, 'Syanjali', 'स्यांजली', 'syanjali'); d(L3, 18, 'Mahavan', 'महावन', 'mahavan')
d(L3, 19, 'Reckong Peo', 'रिकांगपिओ', 'reckong-peo', 'bus starts at Jahalma')
EXISTING = {'shimla': '/shimla-to-karsog-bus/', 'mandi': '/mandi-to-karsog-bus/'}
PLACE = {'pokhi': ('/pokhi-mahog/', 'Pokhi, Mahog & Somakothi drone photos'),
         'somakothi': ('/pokhi-mahog/', 'Pokhi, Mahog & Somakothi drone photos'),
         'dateha': ('/kotlu-dateha/', 'Kotlu & Dateha drone photos'),
         'gada-gushaini': ('/gada-gushaini/', 'Gada Gushaini drone photos'),
         'mahunag': ('/mahunag/', 'Mahunag Temple guide')}
LINE_EN = {L1: 'Karsog–Churag–Tattapani line', L2: 'Karsog–Pangna–Mandi line', L3: 'Karsog–Kelodhar line'}

rows = []
for r in csv.DictReader(open(os.path.join(ROOT, 'data', 'karsog-bus-stand-board.csv'), encoding='utf-8')):
    name, hi, slug, note = D[(r['line'], r['sr'])]
    rows.append(dict(line=r['line'], sr=int(r['sr']), time=r['departure'], route_hi=r['route_hindi'],
                     route_en=r['route_english'], unit=r['unit'], dest=name, dest_hi=hi, slug=slug,
                     note='; '.join(x for x in [note, r['note']] if x)))
rows.sort(key=lambda x: x['time'])


def t12(t):
    h, m = map(int, t.split(':'))
    return f'{h % 12 or 12}:{m:02d} {"AM" if h < 12 else "PM"}'


tpl = open(os.path.join(PUB, 'mandi-to-karsog-bus', 'index.html'), encoding='utf-8').read()
fonts = re.search(r'<link rel="preconnect" href="https://fonts.googleapis.com" />.*?rel="stylesheet" />', tpl, re.S)[0]
css = re.search(r'<style>.*?</style>', tpl, re.S)[0]
nav = re.search(r'<nav class="top">.*?</nav>', tpl, re.S)[0]
foot = re.search(r'<footer>.*</html>', tpl, re.S)[0]
EXTRA = ('<style>.bt{width:100%;border-collapse:collapse;font-size:.92rem;margin:1rem 0}'
         '.bt th,.bt td{text-align:left;padding:.55rem .6rem;border-bottom:1px solid var(--border,#dcd5c8);vertical-align:top}'
         '.bt th{font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted,#6a6a5a)}'
         '.bt td.t{font-weight:700;white-space:nowrap}.bt small{color:var(--muted,#6a6a5a)}'
         '.nb{background:var(--forest,#1c3a1c);color:#fff;padding:1rem 1.25rem;border-radius:8px;margin:1rem 0;line-height:1.7}'
         '.nb b{font-size:1.1rem}.nb small{opacity:.8}.dl{columns:2 14rem;padding-left:1.1rem}'
         '.board img{width:100%;height:auto;border-radius:6px}@media(max-width:600px){.bt td:last-child,.bt th:last-child{display:none}}</style>')
NEXT_JS = '''<script>(()=>{const B=JSON.parse(document.getElementById('bd').textContent);const now=new Date(Date.now()+(330+new Date().getTimezoneOffset())*6e4);const m=now.getHours()*60+now.getMinutes();const f=t=>{const[h,x]=t.split(':').map(Number);return h*60+x};const t12=t=>{let[h,x]=t.split(':').map(Number);const a=h<12?'AM':'PM';h=h%12||12;return h+':'+String(x).padStart(2,'0')+' '+a};const up=B.filter(b=>f(b.time)>=m).concat(B.filter(b=>f(b.time)<m).map(b=>Object.assign({},b,{tm:1}))).slice(0,NN);const el=document.getElementById('next');if(!el||!up.length)return;el.innerHTML='<div><small>Next from Karsog by the board (India time):</small></div>'+up.map(b=>{const d=f(b.time)-m+(b.tm?1440:0);const w=d<60?d+' min':Math.floor(d/60)+' h '+(d%60)+' min';return '<div><b>'+t12(b.time)+'</b> → '+(b.dest||'(see board)')+' <small>in '+w+(b.tm?', tomorrow':'')+'</small></div>'}).join('')})();</script>'''


def page(slug, title, desc, h1, sub, body, crumbs, faq=None):
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": "https://karsog.com" + u} for i, (n, u) in enumerate(crumbs)]}
    ld = '<script type="application/ld+json">' + json.dumps(bc, ensure_ascii=False) + '</script>'
    if faq:
        ld += '\n<script type="application/ld+json">' + json.dumps(faq, ensure_ascii=False) + '</script>'
    cr = ' › '.join(f'<a href="{u}">{esc(n)}</a>' for n, u in crumbs[:-1]) + ' › ' + esc(crumbs[-1][0])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<link rel="canonical" href="https://karsog.com/{slug}/" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(desc)}" />
<meta property="og:image" content="https://karsog.com/photos/bus-stand/karsog-bus-stand-board-2026.webp" />
<meta property="og:url" content="https://karsog.com/{slug}/" />
<meta property="og:type" content="article" />
<meta name="theme-color" content="#1c3a1c" />
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🏔️</text></svg>" />
<link rel="manifest" href="/manifest.webmanifest" />
{fonts}
{ld}
{css}
{EXTRA}
<script async src="https://www.googletagmanager.com/gtag/js?id=G-P4GZFJ5XQG"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-P4GZFJ5XQG");</script>
</head>
<body>

{nav}

<div class="container crumb">{cr}</div>

<header class="page">
  <div class="container">
    <span class="eyebrow">Karsog bus stand</span>
    <h1>{h1}</h1>
    <p class="lede">{sub}</p>
  </div>
</header>

<div class="container">
{body}
</div>

{foot}'''


def dest_link(b):
    if not b['slug']:
        return '<small>—</small>'
    u = EXISTING.get(b['slug'], f'/bus/karsog-to-{b["slug"]}/')
    return f'<a href="{u}">{esc(b["dest"])}</a>'


def table(rs, show_dest=True):
    h = ('<table class="bt"><thead><tr><th>Departs</th>' + ('<th>To</th>' if show_dest else '') +
         '<th>Route on the board</th><th>Line</th></tr></thead><tbody>')
    for b in rs:
        note = f'<br><small>{esc(b["note"])}</small>' if b['note'] else ''
        h += (f'<tr><td class="t">{t12(b["time"])}</td>' + (f'<td>{dest_link(b)}</td>' if show_dest else '') +
              f'<td>{esc(b["route_en"])} <small lang="hi">({esc(b["route_hi"])})</small>{note}</td>'
              f'<td><small>{esc(LINE_EN[b["line"]])}</small></td></tr>')
    return h + '</tbody></table>'


SOURCE_NOTE = (f'<div class="note"><b>Source:</b> {SRC}. The board may be out of date, so confirm at the bus stand '
               'before travelling. HRTC ordinary services; times are departures from Karsog.</div>')
BOARD = ('<figure class="board"><a href="/photos/bus-stand/karsog-bus-stand-board-2026.webp">'
         '<img src="/photos/bus-stand/karsog-bus-stand-board-2026-800.webp" alt="HRTC timetable board at Karsog bus stand, '
         'photographed 25 September 2026" width="800" height="402" loading="lazy"></a><figcaption><small>The HRTC '
         'timetable board at Karsog bus stand (25 Sep 2026). Tap to enlarge.</small></figcaption></figure>')

dests = {}
for b in rows:
    if b['slug']:
        dests.setdefault(b['slug'], []).append(b)

# ---- bus stand page
bdata = [{'time': b['time'], 'dest': b['dest']} for b in rows]
dlist = ''.join(
    f'<li><a href="{EXISTING.get(s, f"/bus/karsog-to-{s}/")}">{esc(v[0]["dest"])}</a> '
    f'<small>({len(v)} bus{"es" if len(v) > 1 else ""})</small></li>'
    for s, v in sorted(dests.items(), key=lambda x: x[1][0]['dest']))
body = f'''<section>
<div class="nb" id="next">Next buses from Karsog appear here.</div>
<script type="application/json" id="bd">{json.dumps(bdata, ensure_ascii=False)}</script>
{NEXT_JS.replace("NN", "5")}
{SOURCE_NOTE}
<h2>All {len(rows)} departures from Karsog, by time</h2>
{table(rows)}
<h2>Buses by destination</h2>
<ul class="dl">{dlist}</ul>
<h2>The timetable board</h2>
{BOARD}
<h2>Buses to Karsog</h2>
<p>The board lists departures from Karsog only. For buses coming to Karsog see <a href="/mandi-to-karsog-bus/">Mandi ⇄ Karsog</a> and <a href="/shimla-to-karsog-bus/">Shimla ⇄ Karsog</a>.</p>
</section>'''
faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": "What is the first bus from Karsog bus stand?", "acceptedAnswer": {"@type": "Answer",
     "text": f"By the timetable board at Karsog bus stand (photographed {CHECKED}), the first departure is {t12(rows[0]['time'])}. Confirm at the stand, as the board may be out of date."}},
    {"@type": "Question", "name": "How many buses leave Karsog bus stand every day?", "acceptedAnswer": {"@type": "Answer",
     "text": f"The HRTC board at Karsog bus stand lists {len(rows)} departures on three lines: Karsog–Churag–Tattapani, Karsog–Pangna–Mandi and Karsog–Kelodhar."}}]}
os.makedirs(os.path.join(PUB, 'karsog-bus-stand'), exist_ok=True)
open(os.path.join(PUB, 'karsog-bus-stand', 'index.html'), 'w', encoding='utf-8').write(page(
    'karsog-bus-stand', 'Karsog Bus Stand Time Table — All HRTC Departures (2026)',
    f'Full HRTC time table of Karsog bus stand: {len(rows)} daily departures to Shimla, Mandi, Rampur, Thunag, Delhi, Haridwar and villages, from the board at the stand ({CHECKED}).',
    'Karsog bus stand<br /><em>time table</em>',
    f'All {len(rows)} HRTC departures listed on the timetable board at Karsog bus stand, with a live "next bus" and a page for every destination.',
    body, [('Karsog Valley', '/'), ('Karsog Bus Stand Time Table', '/karsog-bus-stand/')], faq))

# ---- destination pages
urls = ['/karsog-bus-stand/']
for s, bs in dests.items():
    if s in EXISTING:
        continue
    n, hi = bs[0]['dest'], bs[0]['dest_hi']
    times = ', '.join(t12(b['time']) for b in bs)
    rel = f'<p>See also: <a href="{PLACE[s][0]}">{esc(PLACE[s][1])}</a>.</p>' if s in PLACE else ''
    bd = [{'time': b['time'], 'dest': n} for b in bs]
    body = f'''<section>
<div class="nb" id="next">Next bus to {esc(n)} appears here.</div>
<script type="application/json" id="bd">{json.dumps(bd, ensure_ascii=False)}</script>
{NEXT_JS.replace("NN", "1")}
{SOURCE_NOTE}
<h2>Karsog to {esc(n)} bus timings</h2>
{table(bs, show_dest=False)}
{rel}
<h2>Other buses from Karsog</h2>
<p>See the full <a href="/karsog-bus-stand/">Karsog bus stand time table</a> ({len(rows)} departures) and the photo of the timetable board.</p>
</section>'''
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f"What time is the bus from Karsog to {n}?", "acceptedAnswer": {"@type": "Answer",
         "text": f"The HRTC timetable board at Karsog bus stand (photographed {CHECKED}) lists {len(bs)} bus{'es' if len(bs) > 1 else ''} to {n}: {times}. Confirm at the stand before travelling."}}]}
    slug = f'bus/karsog-to-{s}'
    os.makedirs(os.path.join(PUB, slug), exist_ok=True)
    open(os.path.join(PUB, slug, 'index.html'), 'w', encoding='utf-8').write(page(
        slug, f'Karsog to {n} Bus Timing — HRTC ({hi})',
        f'Karsog to {n} bus timing: {times} (HRTC, from the Karsog bus stand timetable board, {CHECKED}).',
        f'Karsog to {esc(n)}<br /><em>bus timing</em>',
        f'{"One bus" if len(bs) == 1 else str(len(bs)) + " buses"} from Karsog to {esc(n)} <span lang="hi">({esc(hi)})</span>: {times}.',
        body, [('Karsog Valley', '/'), ('Karsog Bus Stand', '/karsog-bus-stand/'), (f'Karsog to {n}', f'/{slug}/')], faq))
    urls.append(f'/{slug}/')

os.makedirs(os.path.join(PUB, 'data'), exist_ok=True)
json.dump({'source': SRC, 'departures': rows}, open(os.path.join(PUB, 'data', 'buses.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
sm = open(os.path.join(PUB, 'sitemap.xml'), encoding='utf-8').read()
sm = re.sub(r'<!-- bus -->.*?<!-- /bus -->\n?', '', sm, flags=re.S)
ent = ''.join(f'  <url><loc>https://karsog.com{u}</loc><lastmod>2026-09-26</lastmod></url>\n' for u in urls)
sm = sm.replace('</urlset>', '<!-- bus -->\n' + ent + '<!-- /bus -->\n</urlset>')
open(os.path.join(PUB, 'sitemap.xml'), 'w', encoding='utf-8').write(sm)
print(len(rows), 'departures;', len(urls), 'pages')
