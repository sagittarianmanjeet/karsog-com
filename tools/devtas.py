#!/usr/bin/env python3
"""Melas & Festivals (/melas/) and Devtas of Karsog (/devtas/), plus a "Fairs & festivals" block on each temple guide.

Sources: three years of local Facebook posts (Karsog Today TV, temple pages and groups), summarised in our own words
in data/devtas.json (one entry per devta) and the MELAS list below. Dates that follow the Hindu calendar move every year.
Run from the repo root:  python3 tools/devtas.py   (safe to re-run)"""
import os, re, json, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagekit import *

# month, name, hindi, place, usual, how the date is set, (2024, 2025, 2026), expected 2027, what happens, link
MELAS = [
 (1, 'Lohri & Makar Sankranti Mela', 'लोहड़ी व मकर संक्रांति मेला', 'Tattapani', '13–15 January', 'Fixed dates',
  ('13–14 Jan', '13–15 Jan', '13–15 Jan'), '~14–16 Jan', 'People take a holy dip in the hot springs beside the Sutlej. There are stalls, swings and cultural evenings on the river bank.', '/tattapani/'),
 (2, 'Mahashivratri', 'महाशिवरात्रि', 'Mamleshwar Mahadev, Mamel (Karsog)', 'February or March', 'Hindu calendar',
  ('8 Mar', '26 Feb', '15 Feb'), '6 Mar', 'Night-long worship and a community meal (bhandara) at Karsog’s ancient Shiva temple.', '/mamleshwar/'),
 (3, 'Chaitra Navratri', 'चैत्र नवरात्रि', 'Kamaksha Devi (Kao), Shikari Devi and other goddess temples', 'March–April, nine days', 'Hindu calendar',
  ('', '', ''), 'March–April', 'The busiest time at the valley’s goddess temples, with special worship every day.', '/devtas/#kamaksha'),
 (4, 'Nalwar Mela', 'नलवाड़ मेला', 'Karsog town', '5–11 April', 'Fixed dates, but not held every year',
  ('Not held', '5–11 Apr', '5–11 Apr'), '5–11 Apr, if held', 'Karsog’s biggest spring fair. It opens with a procession of Mamleshwar Mahadev, followed by a week of stalls, sports and cultural evenings. It was not held in 2024.', '/mamleshwar/'),
 (5, 'Chawasi Utsav', 'च्वासी उत्सव', 'Nahvindhar, Chawasi area', '12–15 May', 'Fixed dates',
  ('12–15 May', '12–15 May', 'from 14 May'), '12–15 May', 'A four-day fair of Nag Chawasi Siddh, with folk music and dance.', '/devtas/#chawasi'),
 (5, 'Mahunag Mela', 'माहूंनाग मेला', 'Mahunag (Bakhari Kothi)', 'Mid-May (about 14–19 May)', 'Starts around Jyeshtha Sankranti',
  ('from 14 May', '~15–19 May', '15–19 May'), '~14–19 May', 'The valley’s biggest fair: the devta’s procession to the fair ground, folk music and dance nights, stalls and a community meal.', '/mahunag/'),
 (6, 'Kamru Nag Mela', 'कमरूनाग मेला', 'Kamru Nag lake (trek from Rohanda)', 'Mid-June', 'Around the middle of June',
  ('', '', ''), 'Mid-June', 'The big annual gathering at the sacred lake, when the most pilgrims make the forest trek.', '/kamru-nag/'),
 (8, 'Chindi Mata Mela', 'चिंडी माता मेला', 'Chindi', '2–4 August', 'Fixed dates', ('2–4 Aug', '2–4 Aug', '2–4 Aug'), '2–4 Aug',
  'A three-day fair at the Chindi Mata temple, on the Karsog–Shimla road.', '/chindi/'),
 (9, 'Seri Bhanju Mela', 'सेरी भंजू मेला', 'Seri Bungalow', 'Late August or September, three days', 'Starts on Rishi Panchami',
  ('~8–10 Sep', 'from 28 Aug', '15–17 Sep'), '~5 Sep', 'A three-day fair of Nag Dhamuni at Seri Bungalow.', '/devtas/#dhamuni'),
 (9, 'Janmashtami', 'जन्माष्टमी', 'Laxmi Narayan temple, old bazaar, Karsog', 'August or September', 'Hindu calendar',
  ('', '', '4 Sep'), '~25 Aug', 'Krishna’s birthday celebrated in Karsog’s old bazaar.', '/devtas/#laxmi_narayan'),
 (10, 'Sharadiya Navratri', 'शारदीय नवरात्रि', 'Kamaksha Devi (Kao), Shikari Devi and other goddess temples', 'September–October, nine days', 'Hindu calendar',
  ('', '', ''), 'Sept–Oct', 'Autumn Navratri; Ashtami night is especially busy at Kamaksha Devi, Kao.', '/devtas/#kamaksha'),
 (12, 'Budhi Diwali', 'बूढ़ी दिवाली', 'Mamleshwar Mahadev (Mamel) and Mahog', 'About a month after Diwali', 'Hindu calendar',
  ('30 Nov–1 Dec', '19–20 Nov', 'expected early Dec'), '~28 Nov', 'The hill Diwali, celebrated a month after the main one with night-long festivities, a unique tradition of the hills.', '/mamleshwar/'),
]
MON = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

DEV = json.load(open(os.path.join(ROOT, 'data', 'devtas.json'), encoding='utf-8'))
GUIDE = {'mahunag': '/mahunag/', 'mamleshwar': '/mamleshwar/', 'kamaksha': '/kao/', 'shikari_devi': '/shikari-devi/',
         'kamrunag': '/kamru-nag/', 'chindi': '/chindi/', 'pangna': '/pangna-fort/'}
ORDER = ['mahunag', 'mamleshwar', 'kamaksha', 'shikari_devi', 'kamrunag', 'chindi', 'pangna', 'laxmi_narayan', 'chawasi', 'dhamuni']

CSS = ('<style>.mm{margin-top:2rem}.mm h3{font-family:"Playfair Display",serif;font-size:1.5rem;color:var(--forest);border-bottom:2px solid var(--gold);'
       'padding-bottom:.3rem;display:flex;align-items:center;gap:.6rem}.mm h3 .now{font-family:inherit;font-size:.7rem;background:var(--gold);color:#fff;'
       'padding:.2rem .55rem;border-radius:999px;letter-spacing:.05em;text-transform:uppercase}'
       '.mcard{background:#fff;border:1px solid var(--border);padding:1rem 1.15rem;margin-top:.75rem}.mcard b{font-family:"Playfair Display",serif;font-size:1.2rem;color:var(--forest)}'
       '.mcard .hi{color:var(--muted);margin-left:.4rem}.mcard .meta{display:flex;flex-wrap:wrap;gap:.35rem .9rem;margin:.45rem 0;font-size:.85rem;color:var(--muted)}'
       '.mcard .meta strong{color:var(--ink)}.mcard p{margin:.35rem 0 0;line-height:1.6}.mcard .yrs{font-size:.8rem;color:var(--muted);margin-top:.5rem}'
       '.mcard a.more{display:inline-block;margin-top:.5rem;color:var(--gold);font-weight:600;font-size:.9rem}'
       '.dgrid{display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(min(100%,420px),1fr));margin-top:1.25rem}'
       '.dcard{background:#fff;border:1px solid var(--border);padding:1.2rem 1.25rem;scroll-margin-top:7rem}.dcard h3{font-family:"Playfair Display",serif;font-size:1.35rem;color:var(--forest)}'
       '.dcard .hi{display:block;color:var(--muted);font-size:.95rem;margin-top:.1rem}.dcard .pl{font-size:.85rem;color:var(--gold);font-weight:600;margin-top:.4rem}'
       '.dcard p{line-height:1.65;margin-top:.6rem}.dcard h4{font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin-top:1rem}'
       '.dcard ul{margin:.35rem 0 0 1.1rem;line-height:1.6}.dcard li{margin:.2rem 0}.dcard a.more{display:inline-block;margin-top:.8rem;color:var(--gold);font-weight:600}'
       '.nowbox{background:var(--forest);color:var(--cream);padding:1.1rem 1.3rem;line-height:1.7}.nowbox b{color:var(--gold-light)}.nowbox a{color:#fff;text-decoration:underline}</style>')


# ------------------------------------------------------------------ /melas/
data = [{'m': m, 'n': n, 'u': u, 'l': l or ''} for m, n, _hi, _p, u, _r, _y, _e, _w, l in MELAS]
months_html = ''
for mi in range(1, 13):
    items = [x for x in MELAS if x[0] == mi]
    if not items:
        continue
    cards = ''
    for m, n, hi, place, usual, rule, yrs, exp, what, link in items:
        y = ' · '.join(f'{yr}: {d}' for yr, d in zip(('2024', '2025', '2026'), yrs) if d not in ('—', ''))
        cards += (f'<div class="mcard"><b>{esc(n)}</b><span class="hi" lang="hi">{esc(hi)}</span>'
                  f'<div class="meta"><span>📍 <strong>{esc(place)}</strong></span><span>📅 <strong>{esc(usual)}</strong></span></div>'
                  f'<p>{esc(what)}</p><div class="yrs">{("Past dates: " + esc(y) + " · ") if y else ""}2027: <strong>{esc(exp)}</strong></div>'
                  + (f'<a class="more" href="{link}">More →</a>' if link else '') + '</div>')
    months_html += f'<div class="mm" id="m{mi}" data-m="{mi}"><h3>{MON[mi - 1]}</h3>{cards}</div>'
NOW_JS = ('<script>(()=>{const M=' + json.dumps(data, ensure_ascii=False) + ';const d=new Date(Date.now()+(330+new Date().getTimezoneOffset())*6e4);'
          'const m=d.getMonth()+1,n=m%12+1,N=["January","February","March","April","May","June","July","August","September","October","November","December"];'
          'const a=M.filter(x=>x.m===m),b=M.filter(x=>x.m===n);const f=L=>L.map(x=>x.l?`<a href="${x.l}">${x.n}</a> (${x.u})`:`${x.n} (${x.u})`).join(" · ")||"no big fairs";'
          'const el=document.getElementById("now");if(el)el.innerHTML=`<b>This month (${N[m-1]}):</b> ${f(a)}<br><b>Next month (${N[n-1]}):</b> ${f(b)}`;'
          'const h=document.querySelector(`#m${m} h3`);if(h)h.insertAdjacentHTML("beforeend","<span class=now>This month</span>")})();</script>')
jumps = [(f'm{i}', MON[i - 1][:3]) for i in range(1, 13) if any(x[0] == i for x in MELAS)]
body = (BOX + CSS + '<section class="xs"><div class="container"><div class="nowbox" id="now">What’s on this month…</div>'
        '<p class="sub" style="margin-top:1.25rem">The biggest fairs (melas) and festivals of Karsog, month by month, for planning a visit. Many dates follow the Hindu calendar and move a little every year, and a few fairs are not held some years, so check locally before you travel. Visitors are welcome at all of them.</p>'
        + months_html + '<p class="xnote" style="margin-top:1.5rem">See also <a href="/devtas/">Temples of Karsog</a>. Know a date we’ve missed? Use the “Submit an update” button.</p></div></section>' + NOW_JS)
page('/melas/', 'Karsog Melas & Festivals — Fair Dates Month by Month (Nalwar, Mahunag, Budhi Diwali)',
     'Karsog fairs and festivals calendar for visitors: Lohri at Tattapani, Nalwar Mela, Mahunag Mela, Kamru Nag Mela, Chindi Mata Mela, Navratri and Budhi Diwali, with dates.',
     'Melas & Festivals', 'Karsog through the year', 'Melas &amp; <em>festivals</em>',
     'The fairs and festivals worth planning a trip around: where, when and what happens.',
     body, jumps,
     [('When is the Nalwar Mela in Karsog?', 'The Nalwar Mela is usually held on 5–11 April in Karsog town, in the years it takes place. It opens with a procession of Mamleshwar Mahadev. It was not held in 2024.'),
      ('When is the Mahunag Mela?', 'The Shri Mool Mahunag Mela is held in mid-May, usually about 14–19 May, at Mahunag (Bakhari Kothi).'),
      ('What is Budhi Diwali?', 'Budhi Diwali is the hill Diwali, celebrated about a month after the main Diwali. In Karsog it is held at Mamleshwar Mahadev and at Mahog. In 2027 it is expected around 28 November.')])

# ------------------------------------------------------------------ /devtas/ (Temples of Karsog)
def lis(xs, n=4):
    return ''.join(f'<li>{esc(x)}</li>' for x in xs[:n])


cards = ''
for slug in ORDER:
    d = DEV.get(slug)
    if not d:
        continue
    fairs = [f'{a}: {b}' for a, b in d.get('fairs', [])]
    cards += (f'<article class="dcard" id="{slug}"><h3>{esc(d["name_en"])}</h3><span class="hi" lang="hi">{esc(d.get("name_hi", ""))}</span>'
              f'<div class="pl">📍 {esc(d["place"])}</div><p>{esc(d["about"])}</p>'
              + (f'<p><i>{esc(d["story"])}</i></p>' if d.get('story') else '')
              + (f'<h4>When to go</h4><ul>{lis(d["when"])}</ul>' if d.get('when') else '')
              + (f'<h4>Fairs</h4><ul>{lis(fairs)}</ul>' if fairs else '')
              + (f'<h4>Tips</h4><ul>{lis(d["tips"])}</ul>' if d.get('tips') else '')
              + (f'<a class="more" href="{GUIDE[slug]}">Full guide →</a>' if slug in GUIDE else '') + '</article>')
body = (BOX + CSS + '<section class="xs"><div class="container"><p class="sub">Karsog is known as a valley of temples. Most are built in the old Himachali style of carved wood and stone, and each village has its own devta. These are the temples most worth visiting, with the story behind each, the best time to go and a few tips.</p>'
        f'<div class="dgrid">{cards}</div><p class="xnote" style="margin-top:1.5rem">Fair dates: <a href="/melas/">Melas &amp; festivals</a>. Something wrong or missing? Use the “Submit an update” button.</p></div></section>')
page('/devtas/', 'Temples of Karsog — Mahunag, Mamleshwar, Kamaksha, Shikari Devi & Kamru Nag',
     'The temples of Karsog worth visiting: Mahunag, Mamleshwar Mahadev, Kamaksha Devi, Shikari Devi, Kamru Nag, Chindi Mata and Pangna Mahamaya, with the story, best time to go and tips.',
     'Temples', 'Valley of temples', 'Temples of <em>Karsog</em>',
     'The temples most worth visiting in the valley: the story behind each, when to go and tips for your visit.',
     body)

# ------------------------------------------------------------------ "Good to know" block on each temple guide page
for slug, url in GUIDE.items():
    d = DEV.get(slug)
    p = os.path.join(PUB, url.strip('/'), 'index.html')
    if not d or not os.path.exists(p):
        continue
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<!-- devta:start -->.*?<!-- devta:end -->\n?', '', s, flags=re.S)
    fl = ''.join(f'<li><b>{esc(a)}</b>: {esc(b)}</li>' for a, b in d.get('fairs', []))
    block = ('<!-- devta:start -->\n<section class="container" id="devta" style="padding:2.5rem 1.25rem;max-width:880px">'
             '<h2 style="font-family:\'Playfair Display\',serif;color:#1c3a1c">Good to know</h2>'
             + (f'<p style="margin-top:.75rem;line-height:1.7"><i>{esc(d["story"])}</i></p>' if d.get('story') else '')
             + f'<h3 style="margin-top:1.25rem;color:#1c3a1c">When to go</h3><ul style="margin:.5rem 0 0 1.1rem;line-height:1.7">{lis(d["when"])}</ul>'
             + (f'<h3 style="margin-top:1.25rem;color:#1c3a1c">Fairs &amp; festivals</h3><ul style="margin:.5rem 0 0 1.1rem;line-height:1.7">{fl}</ul>' if fl else '')
             + f'<p style="margin-top:1rem"><a href="/melas/" style="color:#b8832a;font-weight:600">Karsog fair calendar →</a> · <a href="/devtas/#{slug}" style="color:#b8832a;font-weight:600">All temples of Karsog →</a></p>'
             '</section>\n<!-- devta:end -->\n')
    anchor = '<footer>' if 'class="cm container"' not in s else '<section class="cm container">'
    s = s.replace(anchor, block + anchor, 1)
    open(p, 'w', encoding='utf-8').write(s)

# ------------------------------------------------------------------ sitemap
sm_p = os.path.join(PUB, 'sitemap.xml')
sm = open(sm_p, encoding='utf-8').read()
sm = re.sub(r'<!-- devtas -->.*?<!-- /devtas -->\n?', '', sm, flags=re.S)
sm = sm.replace('</urlset>', '<!-- devtas -->\n' + ''.join(f'  <url><loc>https://karsog.com{u}</loc><lastmod>2026-09-28</lastmod></url>\n' for u in ['/melas/', '/devtas/']) + '<!-- /devtas -->\n</urlset>')
open(sm_p, 'w', encoding='utf-8').write(sm)

import sitenav
sitenav.run()
print('melas, devtas built')
