"""Shared page shell for karsog.com generators (page(), BOX styles)."""
import os, re, json, html, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, 'public')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
esc = html.escape
TODAY = '2026-09-27'

SHELL = open(os.path.join(PUB, 'places', 'index.html'), encoding='utf-8').read()
PRE = SHELL[:SHELL.index('<header class="hub"')]
POST = SHELL[SHELL.index('<!-- Floating Submit Update button -->'):]


def page(path, title, desc, crumb, eyebrow, h1, lede, body, jumps=(), faq=None, extra_head=''):
    url = f'https://karsog.com{path}'
    h = PRE
    h = re.sub(r'<title>.*?</title>', f'<title>{esc(title)}</title>', h)
    h = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + esc(desc), h)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + esc(title), h)
    h = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + esc(desc), h)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, h)
    h = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, h)
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Karsog Valley", "item": "https://karsog.com/"},
        {"@type": "ListItem", "position": 2, "name": crumb, "item": url}]}
    ld = '<script type="application/ld+json">' + json.dumps(bc, ensure_ascii=False) + '</script>'
    if faq:
        ld += '\n<script type="application/ld+json">' + json.dumps(
            {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
            ensure_ascii=False) + '</script>'
    h = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: ld, h, count=1, flags=re.S)
    h = h.replace('</head>', extra_head + '\n</head>', 1)
    jl = ''.join(f'<a href="#{k}">{n}</a>' for k, n in jumps)
    top = (f'<header class="hub"><div class="container"><div class="crumbs"><a href="/">Karsog Valley</a> › {esc(crumb)}</div>'
           f'<span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p>{lede}</p>'
           + (f'<div class="jump">{jl}</div>' if jumps else '') + '</div></header>\n\n')
    faq_html = ''
    if faq:
        faq_html = ('<section id="faq" class="bg-secondary"><div class="container"><div class="section-head"><span class="eyebrow">FAQ</span>'
                    '<h2>Common <em>questions</em></h2></div><div class="faq-list">' +
                    ''.join(f'<details class="faq-item"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq) +
                    '</div></div></section>\n\n')
    out = (h + top + body + faq_html + POST).replace('href="#places"', 'href="/places/"')
    d = os.path.join(PUB, path.strip('/'))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(out)


BOX = ('<style>.xs{padding:3rem 0}.xs h2{font-family:"Playfair Display",serif;font-size:clamp(1.6rem,3.5vw,2.3rem);color:var(--forest);line-height:1.15}'
       '.xs h2 em{color:var(--gold)}.xs .sub{color:var(--muted);margin-top:.5rem;line-height:1.6;max-width:46rem}'
       '.xt{width:100%;border-collapse:collapse;margin-top:1.25rem;background:#fff;font-size:.95rem}'
       '.xt th,.xt td{text-align:left;padding:.7rem .8rem;border-bottom:1px solid var(--border);vertical-align:top}'
       '.xt th{font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);background:#faf8f4}'
       '.xt td.n{font-weight:700;white-space:nowrap;color:var(--forest)}.xt small{color:var(--muted)}'
       '.xt a{color:var(--gold);font-weight:600}.xnote{font-size:.85rem;color:var(--muted);margin-top:1rem;line-height:1.6}'
       '.xcards{display:grid;gap:.75rem;grid-template-columns:repeat(auto-fill,minmax(min(100%,260px),1fr));margin-top:1.25rem}'
       '.xcard{background:#fff;border:1px solid var(--border);padding:1rem 1.1rem}.xcard b{display:block;font-family:"Playfair Display",serif;'
       'font-size:1.15rem;color:var(--forest)}.xcard small{display:block;color:var(--muted);margin-top:.2rem;line-height:1.5}'
       '.xcard a{display:inline-block;margin-top:.6rem;color:var(--gold);font-weight:600;font-size:.9rem}'
       '@media(max-width:600px){.xt{font-size:.82rem}.xt th,.xt td{padding:.55rem .4rem}.xt th{letter-spacing:.04em}}</style>')

