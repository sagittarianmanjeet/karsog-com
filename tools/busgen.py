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


KCSS = '.cm{margin-top:1.5rem}.kc-c{border-top:1px solid var(--border,#dcd5c8);padding:.7rem 0}.kc-h span{color:var(--muted,#6a6a5a);font-size:.85em}.kc-c p{margin:.25rem 0 0;white-space:pre-wrap;overflow-wrap:anywhere}.kc-form{display:grid;gap:.6rem;margin-top:1rem;max-width:560px}.kc-form label{display:grid;gap:.25rem;font-weight:600;font-size:.9rem}.kc-form input,.kc-form textarea{font:inherit;font-weight:400;padding:.6rem;border:1px solid var(--border,#dcd5c8);border-radius:8px;width:100%;background:#fff;box-sizing:border-box}.kc-form button{justify-self:start;font:inherit;font-weight:600;padding:.6rem 1.1rem;border:0;border-radius:8px;background:var(--forest,#1c3a1c);color:#fff;cursor:pointer}.kc-form button:disabled{opacity:.6}.kc-msg{margin:0;font-size:.9rem}'
KC_NOTE = 'Comments are public. Please don’t share Aadhaar, PAN, phone numbers or other personal details.'
def kc_block(slug):
    return (f'<section class="cm container"><style>{KCSS}</style><h2>Is this timing still right?</h2>'
            f'<p>Seen a bus change time, stop running or get cancelled? Tell other travellers here. {KC_NOTE}</p>'
            f'<div id="kc" data-page="{slug}" data-sitekey="0x4AAAAAAFB76cvJ7UlhXYzU" data-placeholder="e.g. The 11:10 AM bus to Mandi now leaves at 11:30."></div>'
            f'<script src="/comments.js?v=2" defer></script></section>')

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
{kc_block(slug)}

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
<h2>Private buses</h2>
<p>Private operators (Manohar, VIP Coach, Sheetla, Chetan, Lajhari, Sharma, Radhika and others) are not on the HRTC board. See <a href="/karsog-private-bus/">Karsog private bus timings</a>.</p>
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

# ---- private buses page (from data/karsog-private-buses.csv, private operators)
P_CHECKED = '27 Sep 2026'
prv = list(csv.DictReader(open(os.path.join(ROOT, 'data', 'karsog-private-buses.csv'), encoding='utf-8')))
# Operators seen on Karsog routes with no reliable timings yet: (operator, route, as_of, source)
P_ROUTES = [
    ('Chetan Bus Service', 'Kamaksha – Karsog – Pangna – Jachh – Charkhari', 'Sep 2026', 'https://www.facebook.com/photo/?fbid=122348689436229581'),
    ('Shiv Shankar Express', 'Karsog – Syanj – Syanjali – Karsog', 'Aug 2026', 'https://www.facebook.com/reel/2080647785879851/'),
    ('NPT Bus Service', 'Karsog – Chhatri – Ani', 'Sep 2026', 'https://www.facebook.com/photo/?fbid=122184756272616859'),
    ('Anshika Bus Service', 'Karsog – Shri Mool Mahunag', 'Sep 2026', 'https://www.facebook.com/photo/?fbid=1815075229625233'),
    ('Hari Om Bus Service', 'Karsog – Shimla ISBT', 'Sep 2026', 'https://www.facebook.com/photo/?fbid=1815075229625233'),
    ('Radhika Bus Service', 'Somakothi – Karsog – Kelodhar – Syanj Bagra', 'Sep 2026', 'https://www.facebook.com/photo/?fbid=1809882586811164'),
    ('Radhika Bus Service', 'Ani – Karsog – Mahunag – Bagshad', 'Jan 2026', 'https://www.facebook.com/photo/?fbid=2117835829052163'),
]
PCSS = '<style>.op{margin:1.75rem 0 .25rem}.op small{font-weight:400;color:var(--muted,#6a6a5a)}.src{font-size:.8rem}.ms{display:none}@media(max-width:600px){.pv td:nth-child(3),.pv th:nth-child(3){display:none}.ms{display:block}}</style>'


def p_time(r):
    if not r['karsog_time']:
        return '<small>—</small>'
    return f'{t12(r["karsog_time"])}<br><small>{"departs" if r["karsog_kind"] == "dep" else "reaches"} Karsog</small>'


def p_table(rs):
    h = ('<table class="bt pv"><thead><tr><th>At Karsog</th><th>Route</th><th>Other stops</th></tr></thead><tbody>')
    for r in rs:
        note = f'<br><small>{esc(r["note"])}</small>' if r['note'] else ''
        ms = f'<small class="ms">{esc(r["stops"])}</small>' if r['stops'] else ''
        h += (f'<tr><td class="t">{p_time(r)}</td><td>{esc(r["route"])}{note}{ms}</td><td><small>{esc(r["stops"]) or "—"}</small></td></tr>')
    return h + '</tbody></table>'


karsog_rows = [r for r in prv if r['karsog_kind']]
near_rows = [r for r in prv if not r['karsog_kind']]
ops = {}
for r in karsog_rows:
    ops.setdefault(r['operator'].split(' (')[0], []).append(r)
for v in ops.values():
    v.sort(key=lambda r: r['karsog_time'] or '99')
pdeps = sorted([{'time': r['karsog_time'], 'dest': f'{r["to"]} ({r["operator"].split(" (")[0]})'}
                for r in karsog_rows if r['karsog_kind'] == 'dep' and r['karsog_time']], key=lambda x: x['time'])
op_html = ''.join(f'<h3 class="op">{esc(o)} <small>({len(rs)} trip{"s" if len(rs) > 1 else ""})</small></h3>{p_table(rs)}'
                  for o, rs in sorted(ops.items()))
routes_html = ''.join(f'<li><b>{esc(o)}</b>: {esc(rt)}</li>'
                      for o, rt, d, s in P_ROUTES)
body = f'''{PCSS}<section>
<div class="nb" id="next">Next private buses from Karsog appear here.</div>
<script type="application/json" id="bd">{json.dumps(pdeps, ensure_ascii=False)}</script>
{NEXT_JS.replace("NN", "4").replace("Next from Karsog by the board", "Next private buses from Karsog")}
<div class="note"><b>Please note:</b> private bus timings can change without notice, so confirm with the conductor or at the bus stand before travelling. We try our best to keep this page updated. Spotted a wrong or changed time? Tell us in the comments below. Times marked “reaches Karsog” are arrivals.</div>
<h2>Private buses at Karsog, by operator</h2>
<p>{len(karsog_rows)} trips by {len(ops)} private operators that start, end or stop at Karsog. HRTC buses are on the <a href="/karsog-bus-stand/">Karsog bus stand time table</a>.</p>
{op_html}
<h2>More private routes (timings not confirmed)</h2>
<p>These operators also run on Karsog routes. If you know their timings, tell us in the comments below.</p>
<ul>{routes_html}</ul>
<h2>Private buses nearby (Tattapani, Pangna)</h2>
<p>These don’t enter Karsog town but serve the valley’s edges.</p>
{p_table(near_rows)}
</section>'''
faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": "Which private buses run from Karsog?", "acceptedAnswer": {"@type": "Answer",
     "text": f"Private operators on Karsog routes include {', '.join(sorted(ops))}. They run to Shimla, Sundernagar, Mandi, Hamirpur, Rampur, Ani and nearby villages. Timings can change, so confirm before travelling."}},
    {"@type": "Question", "name": "What is the first private bus from Karsog to Shimla?", "acceptedAnswer": {"@type": "Answer",
     "text": "Manohar Bus Service leaves Karsog for Shimla ISBT at 4:40 AM, with a second bus at 7:30 AM Timings can change, so confirm before travelling."}}]}
os.makedirs(os.path.join(PUB, 'karsog-private-bus'), exist_ok=True)
open(os.path.join(PUB, 'karsog-private-bus', 'index.html'), 'w', encoding='utf-8').write(page(
    'karsog-private-bus', 'Karsog Private Bus Timings — Shimla, Sundernagar, Mandi, Rampur (2026)',
    f'Private bus timings at Karsog: {len(karsog_rows)} trips by {", ".join(sorted(ops))}, to Shimla, Sundernagar, Mandi, Hamirpur, Rampur and Ani.',
    'Karsog private bus<br /><em>timings</em>',
    f'{len(karsog_rows)} private bus trips at Karsog by {len(ops)} operators, with a live next-bus finder.',
    body, [('Karsog Valley', '/'), ('Karsog Bus Stand', '/karsog-bus-stand/'), ('Private buses', '/karsog-private-bus/')], faq))
urls.append('/karsog-private-bus/')

os.makedirs(os.path.join(PUB, 'data'), exist_ok=True)
json.dump({'source': SRC, 'departures': rows}, open(os.path.join(PUB, 'data', 'buses.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
sm = open(os.path.join(PUB, 'sitemap.xml'), encoding='utf-8').read()
sm = re.sub(r'<!-- bus -->.*?<!-- /bus -->\n?', '', sm, flags=re.S)
ent = ''.join(f'  <url><loc>https://karsog.com{u}</loc><lastmod>2026-09-26</lastmod></url>\n' for u in urls)
sm = sm.replace('</urlset>', '<!-- bus -->\n' + ent + '<!-- /bus -->\n</urlset>')
open(os.path.join(PUB, 'sitemap.xml'), 'w', encoding='utf-8').write(sm)
print(len(rows), 'departures;', len(urls), 'pages')
