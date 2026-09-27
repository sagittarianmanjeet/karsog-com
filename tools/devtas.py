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
 (1, 'Lohri & Makar Sankranti Mela', 'लोहड़ी व मकर संक्रांति मेला', 'Tattapani', '13–15 January', 'Fixed: Lohri and Makar Sankranti',
  ('13–14 Jan', '13–15 Jan', '13–15 Jan'), '~14–16 Jan', 'Holy dip in the Sutlej-side hot springs, tuladan (giving grain and clothes), khichdi prasad, cultural evenings on the river bank.', '/tattapani/'),
 (2, 'Mahashivratri at Mamleshwar Mahadev', 'महाशिवरात्रि', 'Mamel, Karsog', 'February or March', 'Hindu calendar (Phalgun Krishna Chaturdashi)',
  ('8 Mar', '26 Feb', '15 Feb'), '6 Mar', 'Night-long worship in four pahars, special puja and bhandara at Mamleshwar Mahadev; jagran at the Shiv Gufa, Saraur (Tattapani).', '/mamleshwar/'),
 (3, 'Holi', 'होली', 'Karsog', 'February or March', 'Hindu calendar', ('—', '13–14 Mar', '2 Mar'), '22 Mar', 'Colours in the bazaar; a public rangotsav at Baral started in 2026.', None),
 (3, 'Karsog devtas go to the Suket Devta Mela', 'सुकेत देवता मेला (सुंदरनगर)', 'Sundernagar', 'March–April', 'Follows the Sundernagar fair dates',
  ('Mahunag left 6 Apr', 'Mahunag left 23 Mar', 'Mahunag left 15 Mar'), 'March', 'Shri Mool Mahunag walks with his rath from Bakhari Kothi to the state-level fair at Sundernagar, a tradition since 1902. Other Karsog devtas join in some years; in 2026 Nag Chawasi Siddh went for the first time in generations.', '/devtas/#mahunag'),
 (4, 'Nalwar Mela', 'नलवाड़ मेला', 'Karsog', '5–11 April', 'Fixed dates, but needs permission each year',
  ('Not held', '5–11 Apr', '5–11 Apr'), '5–11 Apr, if held', 'Karsog’s district-level fair. Opens with a bull puja and a procession of Shri Mamleshwar Mahadev; cattle fair, sports and cultural evenings. It was not held in 2024.', '/mamleshwar/'),
 (4, 'Lahaul Mela (Shiv–Parvati wedding)', 'लाहौल मेला', 'Karsog area', '18 April', 'Fixed', ('18 Apr', '18 Apr', '18 Apr'), '18 Apr',
  'Celebrates the wedding of Shiva and Parvati; Mamleshwar Mahadev and Maa Kamaksha take part.', '/devtas/#mamleshwar'),
 (4, 'Thirshu Mela', 'थिरशू मेला', 'Syanj Bagra and Somakothi', 'About 19–25 April', 'Around Baisakh', ('—', '~23–24 Apr', '19–25 Apr'), 'Late April',
  'Village fairs of the local devtas at Syanj Bagra and Somakothi around Baisakh.', None),
 (5, 'Nahvindhar Thirshu Mela (Chawasi Utsav)', 'नाहवींधार थिरशू मेला (च्वासी उत्सव)', 'Nahvindhar, Chawasi area', '12–15 May', 'Fixed, four days',
  ('12–15 May', '12–15 May', 'from 14 May'), '12–15 May', 'District-level fair of Gadhpati Shri Nag Chawasi Siddh.', '/devtas/#chawasi'),
 (5, 'Shri Mool Mahunag Mela', 'श्री मूल माहूंनाग मेला', 'Mahunag (Bakhari Kothi)', 'Mid-May (about 14–19 May)', 'Starts around Jyeshtha Sankranti',
  ('from 14 May', '~15–19 May', '15–19 May'), '~14–19 May', 'District-level fair with the devta’s shobha yatra to the fair ground, folk music and dance nights and a bhandara.', '/mahunag/'),
 (5, 'Kuthah Mela', 'कुठाह मेला', 'Janjehli (Seraj)', 'Late May', 'Varies', ('~20–24 May', '~29 May–1 Jun', '22–30 May'), 'Late May', 'Seraj-area fair near Janjehli.', '/janjehli/'),
 (6, 'Barshail Mela', 'बरशैल मेला', 'Lalag', '2–3 June', 'Fixed', ('—', '2–3 Jun', '2–3 Jun'), '2–3 Jun', 'Village fair in which Maa Kamaksha takes part.', '/devtas/#kamaksha'),
 (6, 'Katal Mela (Shri Gihn Nag)', 'कटाल मेला', 'Pangna', 'About 8–11 June', 'Early June', ('~8–11 Jun', 'early Jun', '9–11 Jun'), '~9–11 Jun', 'Fair of Shri Gihn Nag at Pangna.', '/devtas/#pangna'),
 (6, 'Ashadh Mela, Jachh (Chauridhar)', 'आषाढ़ मेला जाछ', 'Jachh, Chauridhar', '16–18 June', 'Starts on Ashadh Sankranti',
  ('ended 17 Jun', 'from 16 Jun', '16–18 Jun'), '16–18 Jun', 'Fair of Shri Nag Dhamuni.', '/devtas/#dhamuni'),
 (7, 'Shri Mool Mahunag birthday', 'श्री मूल माहूंनाग जन्मोत्सव', 'Mahunag (Bakhari Kothi)', '17–18 July', 'Fixed', ('—', '—', '17–18 Jul'), '17–18 Jul', 'Birthday celebrations of the devta at Bakhari Kothi.', '/mahunag/'),
 (7, 'Shravan Mondays', 'सावन सोमवार', 'Temples across Karsog', 'Every Monday of Shravan (July–August)', 'Hindu calendar', ('—', '—', 'Yes'), 'Jul–Aug',
  'Special puja, bhajans and bhandaras, especially at Shiva temples such as Mamleshwar Mahadev.', '/mamleshwar/'),
 (8, 'Chindi Mata Mela (Chakranth)', 'चिंडी माता मेला', 'Chindi', '2–4 August', 'Fixed', ('2–4 Aug', '2–4 Aug', '2–4 Aug'), '2–4 Aug', 'Annual fair of Mata Durga at Chindi.', '/chindi/'),
 (8, 'Kunho (Kunnu) Mela', 'कुन्हो मेला', 'Kunho', '7–9 August', 'Fixed', ('7–9 Aug', '7–9 Aug', '7–9 Aug'), '7–9 Aug', 'Village fair attended by Maa Kamaksha, Nag Dhamuni and Nag Pundri.', '/kunhoo/'),
 (9, 'Seri Bhanju Mela', 'सेरी भंजू मेला', 'Seri Bungalow', 'August–September', 'Starts on Rishi Panchami', ('~8–10 Sep', 'from 28 Aug', '15–17 Sep'), '~5 Sep',
  'Fair of Shri Nag Dhamuni at Seri Bungalow.', '/seri-bunglow/'),
 (9, 'Janmashtami & Nand Utsav', 'जन्माष्टमी व नंद उत्सव', 'Laxmi Narayan temple, Purana Bazaar, Karsog', 'August–September', 'Hindu calendar',
  ('—', '—', '4 Sep; Nand Utsav 14 Sep'), '~25 Aug', 'Janmashtami at the Laxmi Narayan temple in the old bazaar, followed by Nand Utsav.', '/devtas/#laxmi_narayan'),
 (10, 'Shri Mool Mahunag rath yatra (Chhatrale)', 'रथ यात्रा / छतराले', 'Villages around Karsog', 'October–November', 'Varies; hosting days are booked around Ashwin Sankranti',
  ('from 20 Oct', 'from 19 Nov', 'from 26 Oct'), 'Oct–Nov', 'The devta’s rath tours villages; families book a day (jatar) in advance at Bakhari Kothi to host it.', '/mahunag/'),
 (11, 'Chhatri Lavi Mela', 'छतरी लवी मेला', 'Chhatri (Seraj)', 'Late October–early November', 'Varies', ('—', '~30 Oct–3 Nov', '—'), 'Early Nov', 'Seraj-area fair at Chhatri.', '/chhatri/'),
 (11, 'Nag Tundal Mela', 'नाग टुंडल मेला', 'Nanj', '15–16 November', 'Fixed', ('15–16 Nov', '—', '—'), '15–16 Nov', 'Fair of Shri Nag Tundli at Tundal, Nanj.', '/nanj/'),
 (12, 'Budhi Diwali', 'बूढ़ी दिवाली', 'Mamleshwar Mahadev and Mahog', 'About a month after Diwali', 'Hindu calendar (Margashirsha Amavasya)',
  ('30 Nov–1 Dec', '19–20 Nov', 'expected early Dec'), '~28 Nov', 'The hill Diwali, a month after the main one, with night-long celebrations at Mamleshwar Mahadev and at Mahog.', '/mamleshwar/'),
]
MON = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

DEV = json.load(open(os.path.join(ROOT, 'data', 'devtas.json'), encoding='utf-8'))
GUIDE = {'mahunag': '/mahunag/', 'mamleshwar': '/mamleshwar/', 'kamaksha': '/kao/', 'shikari_devi': '/shikari-devi/',
         'kamrunag': '/kamru-nag/', 'chindi': '/chindi/', 'pangna': '/pangna-fort/'}
ORDER = ['mahunag', 'mamleshwar', 'kamaksha', 'shikari_devi', 'kamrunag', 'chawasi', 'chindi', 'dhamuni', 'pangna', 'mahasu',
         'laxmi_narayan', 'narsingh', 'shiv_gufa', 'dawahad', 'kajauni', 'pundri', 'tundli', 'sunani_kot', 'pali_nag', 'edhneshwar']

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
                  f'<div class="meta"><span>📍 <strong>{esc(place)}</strong></span><span>📅 <strong>{esc(usual)}</strong></span><span>🗓️ {esc(rule)}</span></div>'
                  f'<p>{esc(what)}</p><div class="yrs">{("Past dates — " + esc(y) + " · ") if y else ""}Expected 2027: <strong>{esc(exp)}</strong></div>'
                  + (f'<a class="more" href="{link}">More →</a>' if link else '') + '</div>')
    months_html += f'<div class="mm" id="m{mi}" data-m="{mi}"><h3>{MON[mi - 1]}</h3>{cards}</div>'
NOW_JS = ('<script>(()=>{const M=' + json.dumps(data, ensure_ascii=False) + ';const d=new Date(Date.now()+(330+new Date().getTimezoneOffset())*6e4);'
          'const m=d.getMonth()+1,n=m%12+1,N=["January","February","March","April","May","June","July","August","September","October","November","December"];'
          'const a=M.filter(x=>x.m===m),b=M.filter(x=>x.m===n);const f=L=>L.map(x=>x.l?`<a href="${x.l}">${x.n}</a> (${x.u})`:`${x.n} (${x.u})`).join(" · ")||"no big fairs";'
          'const el=document.getElementById("now");if(el)el.innerHTML=`<b>This month (${N[m-1]}):</b> ${f(a)}<br><b>Next month (${N[n-1]}):</b> ${f(b)}`;'
          'const h=document.querySelector(`#m${m} h3`);if(h)h.insertAdjacentHTML("beforeend","<span class=now>This month</span>")})();</script>')
jumps = [(f'm{i}', MON[i - 1][:3]) for i in range(1, 13) if any(x[0] == i for x in MELAS)]
body = (BOX + CSS + '<section class="xs"><div class="container"><div class="nowbox" id="now">What’s on this month…</div>'
        '<p class="sub" style="margin-top:1.25rem">The main fairs (melas) and festivals of Karsog, month by month. Many dates follow the Hindu calendar or the local devta committees and move a little every year, and a few fairs are not held some years. Confirm locally before you plan a trip around one. Know a date we’ve missed? Use the “Submit an update” button.</p>'
        + months_html + '<p class="xnote" style="margin-top:1.5rem">Put together from three years of local posts and announcements (2023–2026). See also <a href="/devtas/">Devtas of Karsog</a>.</p></div></section>' + NOW_JS)
page('/melas/', 'Karsog Melas & Festivals — Fair Dates Month by Month (Nalwar, Mahunag, Budhi Diwali)',
     'Karsog fairs and festivals calendar: Nalwar Mela, Mahunag Mela, Lahaul Mela, Chindi Mata Mela, Kunho Mela, Budhi Diwali and more, with usual dates, past dates and expected 2027 dates.',
     'Melas & Festivals', 'Karsog through the year', 'Melas &amp; <em>festivals</em>',
     'Karsog’s fairs and festivals month by month: where, when, how the date is set and what happens.',
     body, jumps,
     [('When is the Nalwar Mela in Karsog?', 'The Nalwar Mela is usually held on 5–11 April in Karsog, if permission is given that year. It opens with a procession of Shri Mamleshwar Mahadev. It was not held in 2024.'),
      ('When is the Mahunag Mela?', 'The district-level Shri Mool Mahunag Mela starts around Jyeshtha Sankranti, usually about 14–19 May, at Mahunag (Bakhari Kothi).'),
      ('When is Budhi Diwali in Karsog?', 'Budhi Diwali is celebrated about a month after Diwali, on Margashirsha Amavasya, at Mamleshwar Mahadev and Mahog. In 2027 it is expected around 28 November.')])

# ------------------------------------------------------------------ /devtas/
def lis(xs, n):
    return ''.join(f'<li>{esc(x)}</li>' for x in xs[:n])


cards = ''
for slug in ORDER:
    d = DEV.get(slug)
    if not d:
        continue
    fairs = [f'{f["name"]} — {f["when"]}' for f in d.get('fairs', [])]
    cards += (f'<article class="dcard" id="{slug}"><h3>{esc(d["name_en"])}</h3><span class="hi" lang="hi">{esc(d.get("name_hi", ""))}</span>'
              f'<div class="pl">📍 {esc(d.get("place", ""))}</div><p>{esc(d["summary"])}</p>'
              + (f'<h4>Beliefs &amp; stories</h4><ul>{lis(d.get("legend", []), 4)}</ul>' if d.get('legend') else '')
              + (f'<h4>Fairs</h4><ul>{lis(fairs, 5)}</ul>' if fairs else '')
              + (f'<h4>Customs</h4><ul>{lis(d.get("rituals_customs", []), 3)}</ul>' if d.get('rituals_customs') else '')
              + (f'<a class="more" href="{GUIDE[slug]}">Full guide →</a>' if slug in GUIDE else '') + '</article>')
body = (BOX + CSS + '<section class="xs"><div class="container"><p class="sub">Karsog is called a land of devtas: every area has its own devta, who travels in a rath or palki to fairs, visits other devtas and is consulted through the gur. Here are the main devtas and temples of the valley, what people believe about them and when their fairs are. Stories are given as local people tell them.</p>'
        f'<div class="dgrid">{cards}</div><p class="xnote" style="margin-top:1.5rem">Summarised in our own words from three years of local posts and announcements (2023–2026). Fair dates: <a href="/melas/">Melas &amp; festivals</a>. Something wrong or missing? Use the “Submit an update” button.</p></div></section>')
page('/devtas/', 'Devtas of Karsog — Mahunag, Mamleshwar, Kamaksha, Chawasi & Other Temples',
     'The devtas and temples of Karsog: Shri Mool Mahunag, Mamleshwar Mahadev, Maa Kamaksha, Shikari Devi, Kamrunag, Nag Chawasi Siddh, Chindi Mata, Nag Dhamuni and more — beliefs, stories and fairs.',
     'Devtas', 'Land of devtas', 'Devtas of <em>Karsog</em>',
     'The main devtas and temples of the valley, the stories people tell about them, and their fairs.',
     body)

# ------------------------------------------------------------------ fairs block on each temple guide page
for slug, url in GUIDE.items():
    d = DEV.get(slug)
    p = os.path.join(PUB, url.strip('/'), 'index.html')
    if not d or not os.path.exists(p):
        continue
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<!-- devta:start -->.*?<!-- devta:end -->\n?', '', s, flags=re.S)
    fl = ''.join(f'<li><b>{esc(f["name"])}</b> — {esc(f["when"])}. {esc(f.get("what_happens", ""))}</li>' for f in d.get('fairs', [])[:5])
    lg = lis(d.get('legend', []), 3)
    block = ('<!-- devta:start -->\n<section class="container" id="devta" style="padding:2.5rem 1.25rem;max-width:880px">'
             f'<h2 style="font-family:\'Playfair Display\',serif;color:#1c3a1c">Beliefs &amp; fairs</h2>'
             + (f'<ul style="margin:.75rem 0 0 1.1rem;line-height:1.7">{lg}</ul>' if lg else '')
             + (f'<h3 style="margin-top:1.25rem;color:#1c3a1c">Fairs &amp; festivals</h3><ul style="margin:.5rem 0 0 1.1rem;line-height:1.7">{fl}</ul>' if fl else '')
             + f'<p style="margin-top:1rem"><a href="/melas/" style="color:#b8832a;font-weight:600">Karsog fair calendar →</a> · <a href="/devtas/#{slug}" style="color:#b8832a;font-weight:600">Devtas of Karsog →</a></p>'
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
