import os,re,json,math,html,sys,shutil
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,os.path.dirname(__file__)); from groups import G
H=os.path.expanduser('~/mnt'); SITE=H+'/Desktop/github/karsog-com/public'; TOP=H+'/Desktop/top-100'
META={m['f'][:3]:m for m in json.load(open(os.path.expanduser('~/top100meta.json')))}
T=(31.3825,77.2045); KC_SITEKEY=os.environ.get('KC_SITEKEY','')
km=lambda a,b:math.hypot((a[0]-b[0])*111.2,(a[1]-b[1])*95)
def bearing(g): return ['north','north-east','east','south-east','south','south-west','west','north-west'][int((math.degrees(math.atan2((g[1]-T[1])*95,(g[0]-T[0])*111.2))%360+22.5)//45)%8]
esc=html.escape
MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
font=ImageFont.truetype('/usr/share/fonts/truetype/lato/Lato-Bold.ttf',10)
def wm(im):
    W,Hh=im.size; f=ImageFont.truetype('/usr/share/fonts/truetype/lato/Lato-Bold.ttf',max(14,W//55))
    ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov); t='karsog.com'
    bw=d.textbbox((0,0),t,font=f); w,h=bw[2]-bw[0],bw[3]-bw[1]; x,y=W-w-W//60,Hh-h-Hh//30
    d.text((x+1,y+1),t,font=f,fill=(0,0,0,110)); d.text((x,y),t,font=f,fill=(255,255,255,200))
    return Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB')
# ---- collect photos
memb={x:s for s,t,sub,mem,d,ex in G for x in mem}
photos=json.load(open(SITE+'/photos/photos.json')) if os.path.exists(SITE+'/photos/photos.json') and '--rebuild-list' not in sys.argv else []
DESK=H+'/Desktop'; PK=DESK+'/website-picks'
PM=json.load(open(os.path.expanduser('~/picksmeta.json')))
def srcpath(p): return os.path.join(DESK,p['source']) if '/' in p['source'] else os.path.join(TOP,p['source'])
photos=[p for p in photos if os.path.exists(srcpath(p))]
known={p['source'] for p in photos}
cand=[(f,f,int(f[:3])) for f in sorted(os.listdir(TOP)) if f.endswith('.jpg')]
for d in sorted(os.listdir(PK)):
    if os.path.isdir(os.path.join(PK,d)) and not d.startswith('_'):
        cand+=[(f'website-picks/{d}/{f}',f,100+int(f[:3])) for f in sorted(os.listdir(os.path.join(PK,d))) if f.endswith('.jpg') and f[:3].isdigit()]
for src,f,rank in cand:
    if src in known: continue
    raw=re.sub(r'^\d{3}_|_\d{4}-\d\d-\d\d\.jpg$','',f); near=raw.startswith('near '); guess=raw.endswith('~')
    base=re.sub(r'^near ','',raw.rstrip('~')); slug=memb.get(base)
    if not slug: print('SKIP unmapped',src); continue
    g=META.get(f[:3],{}).get('g') if rank<=100 else PM.get(f[:3],{}).get('g')
    dt=re.search(r'(\d{4})-(\d\d)-(\d\d)',f)
    photos.append(dict(source=src,rank=rank,slug=slug,place=base,near=near or guess,date=f'{dt[1]}-{dt[2]}-{dt[3]}',gps=g))
# ---- images
for s in {p['slug'] for p in photos}:
    ps=sorted([p for p in photos if p['slug']==s],key=lambda p:p['rank'])
    os.makedirs(f'{SITE}/photos/{s}',exist_ok=True)
    for i,p in enumerate(ps,1):
        if 'file' not in p: p['file']=f'{s}-{p["rank"]:03d}'
        big=f'{SITE}/photos/{s}/{p["file"]}-1600.webp'
        if not os.path.exists(big):
            im=Image.open(srcpath(p)).convert('RGB')
            a=im.copy(); a.thumbnail((1600,1600)); a=wm(a); a.save(big,'WEBP',quality=80,method=5)
            b=im.copy(); b.thumbnail((800,800)); b=wm(b); b.save(f'{SITE}/photos/{s}/{p["file"]}-800.webp','WEBP',quality=78,method=5)
            p['w'],p['h']=a.size
        if i==1 and not os.path.exists(f'{SITE}/photos/{s}/cover.jpg'):
            c=Image.open(srcpath(p)).convert('RGB'); c.thumbnail((1200,1200)); wm(c).save(f'{SITE}/photos/{s}/cover.jpg',quality=82)
json.dump(photos,open(SITE+'/photos/photos.json','w'),indent=1)
LABELS=json.load(open(os.path.expanduser('~/gal/labels.json'))) if os.path.exists(os.path.expanduser('~/gal/labels.json')) else {}
def cap(p):
    d=p['date']; when=f"{MON[int(d[5:7])-1]} {d[:4]}"
    lab=LABELS.get(p['file'])
    if lab: return lab, f"Aerial view of {lab}{'' if 'Karsog' in lab else ', Karsog'}, Himachal Pradesh", when
    pl=p['place']
    if pl.startswith('Laxmi Narayan Temple'): pl='Laxmi Narayan Temple, Karsog'+(' (Janmashtami)' if p['date']=='2026-09-04' else '')
    if pl=='Karsog town (night)': pl='Karsog town'
    nm=('Near ' if p['near'] else '')+pl
    return nm, f"Aerial view of {'the area near ' if p['near'] else ''}{pl}{'' if 'Karsog' in pl else ', Karsog'}, Himachal Pradesh", when
# ---- gallery html block
LB='''<div id="lb" class="lb" hidden><button class="lb-x" aria-label="Close">×</button><button class="lb-p" aria-label="Previous">‹</button><figure><img alt=""><figcaption></figcaption></figure><button class="lb-n" aria-label="Next">›</button></div>
<script>(()=>{const L=[...document.querySelectorAll('.gal a')],b=document.getElementById('lb');if(!L.length)return;const im=b.querySelector('img'),fc=b.querySelector('figcaption');let i=0;
const show=k=>{i=(k+L.length)%L.length;im.src=L[i].href;im.alt=L[i].querySelector('img').alt;fc.textContent=L[i].dataset.cap;b.hidden=false;document.body.style.overflow='hidden'};
const hide=()=>{b.hidden=true;document.body.style.overflow=''};
L.forEach((a,k)=>a.addEventListener('click',e=>{e.preventDefault();show(k)}));
b.querySelector('.lb-x').onclick=hide;b.querySelector('.lb-p').onclick=()=>show(i-1);b.querySelector('.lb-n').onclick=()=>show(i+1);
b.addEventListener('click',e=>{if(e.target===b)hide()});
document.addEventListener('keydown',e=>{if(b.hidden)return;if(e.key==='Escape')hide();if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1)});
let x0=null;b.addEventListener('touchstart',e=>x0=e.touches[0].clientX,{passive:true});b.addEventListener('touchend',e=>{if(x0===null)return;const dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>40)show(i+(dx<0?1:-1));x0=null});})();</script>'''
CSS='''.gal{display:grid;gap:.5rem;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));margin:1.25rem 0}
.gal a{display:block;background:#1a1a18;overflow:hidden;position:relative}
.gal img{width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;display:block;transition:transform .4s}
.gal a:hover img{transform:scale(1.04)}
.gal .c{position:absolute;left:0;right:0;bottom:0;padding:.5rem .6rem;font-size:.72rem;color:#fff;background:linear-gradient(transparent,#000a)}
.lb{position:fixed;inset:0;z-index:100;background:#000e;display:flex;align-items:center;justify-content:center}
.lb[hidden]{display:none}.lb figure{max-width:94vw;max-height:88vh;text-align:center}
.lb img{max-width:94vw;max-height:80vh;object-fit:contain}
.lb figcaption{color:#eee;font-size:.85rem;margin-top:.6rem}
.lb button{position:absolute;background:none;border:0;color:#fff;font-size:2.4rem;cursor:pointer;padding:1rem;line-height:1}
.lb-x{top:.2rem;right:.4rem}.lb-p{left:.2rem;top:50%;transform:translateY(-50%)}.lb-n{right:.2rem;top:50%;transform:translateY(-50%)}
.cm{margin-top:1.5rem}.kc-c{border-top:1px solid var(--border,#dcd5c8);padding:.7rem 0}.kc-h span{color:var(--muted,#6a6a5a);font-size:.85em}.kc-c p{margin:.25rem 0 0;white-space:pre-wrap;overflow-wrap:anywhere}.kc-form{display:grid;gap:.6rem;margin-top:1rem;max-width:560px}.kc-form label{display:grid;gap:.25rem;font-weight:600;font-size:.9rem}.kc-form input,.kc-form textarea{font:inherit;font-weight:400;padding:.6rem;border:1px solid var(--border,#dcd5c8);border-radius:8px;width:100%;background:#fff;box-sizing:border-box}.kc-form button{justify-self:start;font:inherit;font-weight:600;padding:.6rem 1.1rem;border:0;border-radius:8px;background:var(--forest,#1c3a1c);color:#fff;cursor:pointer}.kc-form button:disabled{opacity:.6}.kc-msg{margin:0;font-size:.9rem}'''
def gallery(s,ps,title):
    items=[]
    for p in ps:
        nm,alt,when=cap(p); c=f"{nm} · {when}"
        items.append(f'<a href="/photos/{s}/{p["file"]}-1600.webp" data-cap="{esc(c)}"><img src="/photos/{s}/{p["file"]}-800.webp" alt="{esc(alt)}" loading="lazy" width="800" height="533"><span class="c">{esc(nm)}</span></a>')
    cm=''
    if KC_SITEKEY:
        cm=f'''<section class="cm"><h2>Comments</h2><p>Know this place? Share a name, a story or a correction. Comments appear after approval.</p><div id="kc" data-page="{s}" data-sitekey="{KC_SITEKEY}"></div><script src="/comments.js?v=1" defer></script></section>'''
    return f'<!-- gallery:start -->\n<style>{CSS}</style>\n<section id="photos"><div class="container"><h2>Photos from above</h2><p>{len(ps)} drone photo{"s" if len(ps)>1 else ""} · tap a photo to view it full size.</p><div class="gal">{"".join(items)}</div>{cm}</div></section>\n{LB}\n<!-- gallery:end -->'
def ld(s,title,ps,g):
    imgs=[{"@type":"ImageObject","contentUrl":f"https://karsog.com/photos/{s}/{p['file']}-1600.webp","caption":cap(p)[1],"creator":{"@type":"Person","name":"Karsog Miles"},"copyrightNotice":"karsog.com"} for p in ps]
    d={"@context":"https://schema.org","@type":"ImageGallery","name":f"{title} — aerial photos","url":f"https://karsog.com/{s}/","image":imgs}
    if g: d["contentLocation"]={"@type":"Place","name":title,"geo":{"@type":"GeoCoordinates","latitude":round(g[0],4),"longitude":round(g[1],4)}}
    return '<script type="application/ld+json">'+json.dumps(d,ensure_ascii=False)+'</script>'
tpl=open(SITE+'/janjehli/index.html').read()
head_css=re.search(r'<style>.*?</style>',tpl,re.S)[0]
nav=re.search(r'<nav class="top">.*?</nav>',tpl,re.S)[0]; foot=re.search(r'<footer>.*</html>',tpl,re.S)[0]
fontlinks=re.search(r'<link rel="preconnect" href="https://fonts.googleapis.com" />.*?rel="stylesheet" />',tpl,re.S)[0]
CENT={}
TITLES={x[0]:x[1] for x in G}
for _s in TITLES:
    _gp=[p['gps'] for p in photos if p['slug']==_s and p['gps']]
    if _gp: CENT[_s]=(sum(x[0] for x in _gp)/len(_gp),sum(x[1] for x in _gp)/len(_gp))
def about(s,ps,g,rng,dist):
    from collections import Counter
    c=Counter(cap(p)[0] for p in ps)
    fx=lambda n:re.sub(r'^Near ','near ',n.replace(' (Janmashtami)',' at Janmashtami'))
    items=[f'{esc(fx(n))}{f" ({k} photos)" if k>1 and len(c)>1 else ""}' for n,k in c.most_common()]
    lst=', '.join(items[:-1])+(' and '+items[-1] if len(items)>1 else items[0])
    out=[f'<p>The {len(ps)} drone photo{"s" if len(ps)>1 else ""} on this page show {lst}.</p>']
    if g:
        where=f'about {km(g,T):.0f} km {bearing(g)} of Karsog town in a straight line' if km(g,T)>=1.5 else 'in and around Karsog town'
        out.append(f'<p>They were taken {where}, in {rng}, by <a href="https://www.youtube.com/@KarsogMiles" target="_blank" rel="noopener">Karsog Miles</a>. Distances are measured from where the drone flew, not by road.</p>')
        nb=sorted([(km(g,c2),s2) for s2,c2 in CENT.items() if s2!=s])[:3]
        out.append('<p>Nearby on this site: '+' · '.join(f'<a href="/{s2}/">{esc(TITLES[s2])}</a> (~{d:.0f} km)' for d,s2 in nb)+'.</p>')
    else:
        out.append(f'<p>They were taken in {rng} by <a href="https://www.youtube.com/@KarsogMiles" target="_blank" rel="noopener">Karsog Miles</a>. These photos come from video frames without GPS, so no map location is given.</p>')
    return '<section class="about"><div class="container"><h2>About these photos</h2>'+''.join(out)+'</div></section>'
cards=[]
for s,title,sub,mem,desc,exists in G:
    ps=sorted([p for p in photos if p['slug']==s],key=lambda p:p['rank'])
    if not ps: continue
    gp=[p['gps'] for p in ps if p['gps']]; g=(sum(x[0] for x in gp)/len(gp),sum(x[1] for x in gp)/len(gp)) if gp else None
    dates=sorted(p['date'] for p in ps); d0,d1=dates[0],dates[-1]
    rng=f"{MON[int(d0[5:7])-1]} {d0[:4]}"+("" if d0[:7]==d1[:7] else f" – {MON[int(d1[5:7])-1]} {d1[:4]}")
    dist=f"~{km(g,T):.0f} km {bearing(g)}" if g and km(g,T)>=1.5 else "Karsog town"
    names=sorted({re.sub(r' \((night|Janmashtami)\)','',p['place']).replace('Laxmi Narayan Temple','Laxmi Narayan Temple') for p in ps})
    cards.append((s,title,len(ps),ps[0],dist))
    blk=gallery(s,ps,title)
    if exists:
        pth=f'{SITE}/{s}/index.html'; h=open(pth).read()
        h=re.sub(r'<!-- gallery:start -->.*?<!-- gallery:end -->\n?','',h,flags=re.S)
        h=re.sub(r'<script type="application/ld\+json" id="galld">.*?</script>\n?','',h,flags=re.S)
        h=h.replace('</header>','</header>\n'+blk,1)
        h=h.replace('</head>',ld(s,title,ps,g).replace('<script ','<script id="galld" ')+'\n</head>',1)
        open(pth,'w').write(h); continue
    desc_html=f'<p class="lede">{esc(desc)}</p>' if desc else ''
    pl=', '.join(names)
    page=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(title)}, Karsog — Aerial Drone Photos</title>
<meta name="description" content="{esc(f'{len(ps)} aerial drone photos of {pl} — Karsog, Mandi district, Himachal Pradesh. Shot {rng}.')}" />
<link rel="canonical" href="https://karsog.com/{s}/" />
<meta property="og:title" content="{esc(title)} — aerial photos | Karsog Valley" />
<meta property="og:description" content="{esc(f'{len(ps)} drone photos of {pl}, Karsog.')}" />
<meta property="og:image" content="https://karsog.com/photos/{s}/cover.jpg" />
<meta property="og:url" content="https://karsog.com/{s}/" />
<meta property="og:type" content="article" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="theme-color" content="#1c3a1c" />
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🏔️</text></svg>" />
<link rel="manifest" href="/manifest.webmanifest" />
{fontlinks}
{ld(s,title,ps,g)}
<script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Karsog Valley','item':'https://karsog.com/'},{'@type':'ListItem','position':2,'name':title,'item':f'https://karsog.com/{s}/'}]},ensure_ascii=False)}</script>
{head_css}
<script async src="https://www.googletagmanager.com/gtag/js?id=G-P4GZFJ5XQG"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-P4GZFJ5XQG");</script>
</head>
<body>

{nav}

<div class="container crumb"><a href="/">Karsog Valley</a> › <a href="/#photos">Photos</a> › {esc(title)}</div>

<header class="page">
  <div class="container">
    <span class="eyebrow">Karsog from above</span>
    <h1>{esc(title)}{f' —<br /><em>{esc(sub)}</em>' if sub else ''}</h1>
    {desc_html}
    <div class="facts">
      <div class="fact"><div class="v">{len(ps)}</div><div class="l">Drone photos</div></div>
      <div class="fact"><div class="v">{dist}</div><div class="l">From Karsog town (straight line)</div></div>
      <div class="fact"><div class="v">{rng}</div><div class="l">Photographed</div></div>
      <div class="fact"><div class="v">{f'<a href="https://www.google.com/maps?q={g[0]:.4f},{g[1]:.4f}" target="_blank" rel="noopener">Open map ↗</a>' if g else '—'}</div><div class="l">Location</div></div>
    </div>
  </div>
</header>
{about(s,ps,g,rng,dist)}
{blk}
<section><div class="container"><h2>More places from above</h2><div class="related" id="rel"></div></div></section>
<script>fetch('/photos/places.json').then(r=>r.json()).then(L=>{{document.getElementById('rel').innerHTML=L.filter(p=>p.slug!=='{s}').slice(0,6).map(p=>`<a class="rel" href="/${{p.slug}}/"><h3>${{p.title}}</h3><p>${{p.n}} photos · ${{p.dist}}</p></a>`).join('')}})</script>
{foot}'''
    os.makedirs(f'{SITE}/{s}',exist_ok=True); open(f'{SITE}/{s}/index.html','w').write(page)
json.dump([dict(slug=s,title=t,n=n,dist=d,cover=f'/photos/{s}/{c["file"]}-800.webp') for s,t,n,c,d in cards],open(SITE+'/photos/places.json','w'),indent=1)
# ---- homepage section
cards.sort(key=lambda c:-c[2])
ch=''.join(f'<a class="pc" href="/{s}/"><img src="/photos/{s}/{c["file"]}-800.webp" alt="{esc(cap(c)[1])}" loading="lazy" width="800" height="533"><span class="pc-t"><b>{esc(t)}</b><i>{n} photos · {esc(d)}</i></span></a>' for s,t,n,c,d in cards)
home=f'''<!-- photos:start -->
<style>#photos{{padding:4rem 0 3rem}}.pgrid{{display:grid;gap:.6rem;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));margin-top:2rem}}.pc{{position:relative;display:block;overflow:hidden;background:#1a1a18}}.pc img{{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;display:block;transition:transform .5s}}.pc:hover img{{transform:scale(1.05)}}.pc-t{{position:absolute;left:0;right:0;bottom:0;padding:1rem .9rem .8rem;background:linear-gradient(transparent,#000c);color:#fff;display:flex;flex-direction:column}}.pc-t b{{font-family:'Playfair Display',serif;font-size:1.15rem}}.pc-t i{{font-style:normal;font-size:.72rem;opacity:.85;margin-top:.15rem}}</style>
<section id="photos"><div class="container"><div class="section-head"><span class="eyebrow">Karsog from above</span><h2>{sum(c[2] for c in cards)} drone photos,<br /><em>{len(cards)} places.</em></h2><p class="lede" style="margin-top:1.25rem">Aerial photos of Karsog's villages, temples, fairs and the Satluj valley, shot by <a href="https://www.youtube.com/@KarsogMiles" target="_blank" rel="noopener">Karsog Miles</a> in 2026. Pick a place to see all its photos.</p></div><div class="pgrid">{ch}</div></div></section>
<!-- photos:end -->'''
ip=SITE+'/index.html'; h=open(ip).read()
h=re.sub(r'<!-- photos:start -->.*?<!-- photos:end -->\n?','',h,flags=re.S)
h=h.replace('<!-- Marquee -->',home+'\n\n<!-- Marquee -->',1)
if 'href="#photos"' not in h:
    h=h.replace('<li><a href="#places" data-hi="स्थल">Places</a></li>','<li><a href="#photos" data-hi="फ़ोटो">Photos</a></li>\n      <li><a href="#places" data-hi="स्थल">Places</a></li>',1)
    h=h.replace('<a href="#places" data-hi="स्थल">Places</a>\n','<a href="#photos" data-hi="फ़ोटो">Photos</a>\n  <a href="#places" data-hi="स्थल">Places</a>\n',1)
    h=h.replace('<a href="#places" class="btn btn-gold" data-hi="घाटी देखें →">Explore the Valley →</a>','<a href="#photos" class="btn btn-gold" data-hi="फ़ोटो देखें →">See Karsog from above →</a>',1)
open(ip,'w').write(h)
# ---- sitemap
sm=open(SITE+'/sitemap.xml').read()
if 'xmlns:image' not in sm: sm=sm.replace('<urlset ','<urlset xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" ',1)
sm=re.sub(r'<!-- gal -->.*?<!-- /gal -->\n?','',sm,flags=re.S)
ent=''
EX={x[0] for x in G if x[5]}
for s,t,n,c,d in cards:
    if s in EX: continue
    ps=sorted([p for p in photos if p['slug']==s],key=lambda p:p['rank'])
    ent+=f'  <url><loc>https://karsog.com/{s}/</loc><lastmod>2026-09-24</lastmod>'+''.join(f'<image:image><image:loc>https://karsog.com/photos/{s}/{p["file"]}-1600.webp</image:loc></image:image>' for p in ps)+'</url>\n'
sm=sm.replace('</urlset>','<!-- gal -->\n'+ent+'<!-- /gal -->\n</urlset>')
open(SITE+'/sitemap.xml','w').write(sm)
print(len(photos),'photos',len(cards),'places')
