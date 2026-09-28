#!/usr/bin/env python3
"""Builds the pages that answer what people search for on Google (Keyword Planner, 27 Sep 2026):

  /weather/    Karsog weather: live forecast, snow & rain alerts, air quality, nearby places, last 12 months
               (everything loads live from Open-Meteo, free, no key; nothing to update by hand)
  /distance/   Road distances from Karsog (OpenStreetMap routing, 27 Sep 2026)
  /hotels/     Hotels & stays in and around Karsog
  /contacts/   adds a "Karsog at a glance" block: PIN, STD code, vehicle code, bank IFSC codes, college, MLA

Run from the repo root:  python3 tools/extras.py   (safe to re-run; it rebuilds these pages)"""
import os, re, json, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagekit import *
# ------------------------------------------------------------------ weather
WX_CSS = ('<style>.wnow{display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));margin-top:1.25rem}'
          '.wbig{background:var(--forest);color:var(--cream);padding:1.4rem 1.5rem}.wbig .t{font-family:"Playfair Display",serif;font-size:3.4rem;line-height:1}'
          '.wbig .d{font-size:1.1rem;margin-top:.4rem}.wbig small{display:block;opacity:.8;margin-top:.6rem;line-height:1.6}'
          '.walert{padding:1rem 1.2rem;border-left:4px solid var(--gold);background:#fff;line-height:1.6}.walert.ok{border-color:var(--moss,#7aaa6a)}'
          '.whours{display:flex;gap:.5rem;overflow-x:auto;padding:.25rem 0 .75rem;margin-top:1rem;scrollbar-width:thin}'
          '.wh{flex:none;width:74px;text-align:center;background:#fff;border:1px solid var(--border);padding:.6rem .3rem;font-size:.82rem}'
          '.wh b{display:block;font-size:1.05rem;margin:.2rem 0;color:var(--forest)}.wh small{color:var(--muted)}'
          '.wdays .e{font-size:1.2rem}.xt td.hi{font-weight:700;color:var(--forest)}.xt td.lo{color:var(--muted)}'
          '.aq{display:inline-block;padding:.15rem .55rem;border-radius:999px;font-weight:700;color:#fff}'
          '.wload{color:var(--muted);font-style:italic}@media(max-width:600px){.wdays .sk{display:none}}</style>')
WX_JS = r'''<script>
(()=>{const LAT=31.3825,LON=77.2045,TZ='Asia%2FKolkata';
const W=c=>c===0?['☀️','Clear']:c<=2?['⛅','Partly cloudy']:c===3?['☁️','Cloudy']:c<=48?['🌫️','Fog']:c<=57?['🌦️','Drizzle']:c<=67?['🌧️','Rain']:c<=77?['❄️','Snow']:c<=82?['🌧️','Showers']:c<=86?['❄️','Snow showers']:['⛈️','Thunderstorm'];
const DAY=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const $=id=>document.getElementById(id),r0=x=>Math.round(x),f1=x=>(Math.round(x*10)/10);
const tm=s=>{const d=new Date(s);let h=d.getHours();const m=String(d.getMinutes()).padStart(2,'0');return (h%12||12)+':'+m+(h<12?' AM':' PM')};
fetch(`https://api.open-meteo.com/v1/forecast?latitude=${LAT}&longitude=${LON}&current=temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m,precipitation&hourly=temperature_2m,weather_code,precipitation_probability&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,snowfall_sum,precipitation_probability_max,sunrise,sunset&timezone=${TZ}&forecast_days=7`)
.then(r=>r.json()).then(d=>{const c=d.current,[e,t]=W(c.weather_code);
 $('now').innerHTML=`<div class="t">${e} ${r0(c.temperature_2m)}°C</div><div class="d">${t}</div><small>Feels like ${r0(c.apparent_temperature)}°C · Humidity ${c.relative_humidity_2m}% · Wind ${r0(c.wind_speed_10m)} km/h<br>Today ${r0(d.daily.temperature_2m_max[0])}° / ${r0(d.daily.temperature_2m_min[0])}° · Sunrise ${tm(d.daily.sunrise[0])} · Sunset ${tm(d.daily.sunset[0])}</small>`;
 const code=d.daily.weather_code[0],rain=d.daily.precipitation_sum[0]||0,snow=d.daily.snowfall_sum[0]||0;let msg='',ok=false;
 const snowDays=d.daily.snowfall_sum.map((s,i)=>s>0?DAY[new Date(d.daily.time[i]).getDay()]:null).filter(Boolean);
 if(snow>0||(code>=71&&code<=77)||code===85||code===86)msg='❄️ Snow forecast today. Upper roads (Shikari Devi, Chindi, Janjehli) can close. Check before you travel.';
 else if(rain>=20||[65,67,82,95,96,99].includes(code))msg='🌧️ Heavy rain forecast today. Landslides and slips are common on these hill roads. Check before you travel.';
 else if(rain>=7||[61,63,80,81].includes(code))msg='🌦️ Rain forecast today. Expect slow, slippery patches on the hill roads.';
 else{msg='✅ No heavy rain or snow forecast for Karsog today.';ok=true}
 if(snowDays.length)msg+=` Snow is in the forecast on: ${snowDays.join(', ')}.`;
 $('alert').className='walert'+(ok?' ok':'');$('alert').innerHTML=msg;
 const now=new Date(c.time),H=d.hourly;let hs='';for(let i=0;i<H.time.length&&hs.split('class="wh"').length<=24;i++){const ht=new Date(H.time[i]);if(ht<now-36e5)continue;const [he]=W(H.weather_code[i]);const h=ht.getHours();hs+=`<div class="wh"><small>${h%12||12} ${h<12?'AM':'PM'}</small><b>${he} ${r0(H.temperature_2m[i])}°</b><small>💧${H.precipitation_probability[i]??0}%</small></div>`}
 $('hours').innerHTML=hs;
 const D=d.daily;let rows='';for(let i=0;i<D.time.length;i++){const dt=new Date(D.time[i]);const [de,dtx]=W(D.weather_code[i]);rows+=`<tr><td>${i===0?'Today':DAY[dt.getDay()]+' '+dt.getDate()+' '+MON[dt.getMonth()]}</td><td><span class="e">${de}</span> <span class="sk">${dtx}</span></td><td class="hi">${r0(D.temperature_2m_max[i])}°</td><td class="lo">${r0(D.temperature_2m_min[i])}°</td><td>${D.precipitation_probability_max[i]??'–'}% · ${f1(D.precipitation_sum[i])} mm${D.snowfall_sum[i]>0?' · ❄️ '+f1(D.snowfall_sum[i])+' cm':''}</td></tr>`}
 $('days').innerHTML=rows;}).catch(()=>{$('now').innerHTML='Live weather could not load. Please refresh.'});
fetch(`https://air-quality-api.open-meteo.com/v1/air-quality?latitude=${LAT}&longitude=${LON}&current=us_aqi,pm2_5,pm10&timezone=${TZ}`).then(r=>r.json()).then(a=>{const v=a.current.us_aqi;const [c,l]=v<=50?['#3a8a3a','Good']:v<=100?['#b8932a','Moderate']:v<=150?['#d0702a','Unhealthy for sensitive groups']:v<=200?['#c0392b','Unhealthy']:['#7d3c98','Very unhealthy'];
 $('aqi').innerHTML=`<span class="aq" style="background:${c}">US AQI ${r0(v)}</span> ${l}<br><small>PM2.5 ${f1(a.current.pm2_5)} µg/m³ · PM10 ${f1(a.current.pm10)} µg/m³ (model estimate)</small>`}).catch(()=>{$('aqi').textContent='Air quality could not load.'});
const P=[['Shikari Devi','/shikari-devi/',31.4784,77.1657],['Janjehli','/janjehli/',31.5241,77.2209],['Kamru Nag','/kamru-nag/',31.4729,77.0497],['Tattapani','/tattapani/',31.2487,77.0879],['Pangna','/pangna-fort/',31.3855,77.1234]];
fetch(`https://api.open-meteo.com/v1/forecast?latitude=${P.map(p=>p[2])}&longitude=${P.map(p=>p[3])}&current=temperature_2m,weather_code&daily=temperature_2m_max,temperature_2m_min,snowfall_sum&timezone=${TZ}&forecast_days=1`).then(r=>r.json()).then(L=>{L=Array.isArray(L)?L:[L];
 $('near').innerHTML=L.map((x,i)=>{const [e,t]=W(x.current.weather_code);return `<tr><td><a href="${P[i][1]}">${P[i][0]}</a><br><small>${r0(x.elevation)} m</small></td><td>${e} ${t}</td><td class="hi">${r0(x.current.temperature_2m)}°C</td><td>${r0(x.daily.temperature_2m_max[0])}° / ${r0(x.daily.temperature_2m_min[0])}°${x.daily.snowfall_sum[0]>0?' · ❄️ snow':''}</td></tr>`}).join('')}).catch(()=>{});
const end=new Date(Date.now()-8*864e5),start=new Date(end.getTime()-364*864e5),iso=d=>d.toISOString().slice(0,10);
fetch(`https://archive-api.open-meteo.com/v1/archive?latitude=${LAT}&longitude=${LON}&start_date=${iso(start)}&end_date=${iso(end)}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,snowfall_sum&timezone=${TZ}`).then(r=>r.json()).then(h=>{const M={};h.daily.time.forEach((t,i)=>{const k=t.slice(0,7);(M[k]=M[k]||{mx:[],mn:[],p:0,s:0,sd:0});if(h.daily.temperature_2m_max[i]==null)return;M[k].mx.push(h.daily.temperature_2m_max[i]);M[k].mn.push(h.daily.temperature_2m_min[i]);M[k].p+=h.daily.precipitation_sum[i]||0;const s=h.daily.snowfall_sum[i]||0;M[k].s+=s;if(s>0.5)M[k].sd++});
 const avg=a=>a.reduce((x,y)=>x+y,0)/a.length;$('year').innerHTML=Object.keys(M).sort().filter(k=>M[k].mx.length>=25).map(k=>{const m=M[k],[y,mo]=k.split('-');return `<tr><td>${MON[+mo-1]} ${y}</td><td class="hi">${r0(avg(m.mx))}°</td><td class="lo">${r0(avg(m.mn))}°</td><td>${r0(m.p)} mm</td><td>${m.s>0.5?r0(m.s)+' cm ('+m.sd+' day'+(m.sd===1?'':'s')+')':'—'}</td></tr>`}).join('')}).catch(()=>{$('year').innerHTML='<tr><td colspan="5">Could not load past weather.</td></tr>'});
})();
</script>'''
wx_body = BOX + WX_CSS + f'''<section class="xs" id="now-sec"><div class="container">
<div class="wnow"><div class="wbig" id="now"><span class="wload">Loading live weather…</span></div>
<div><div class="walert" id="alert"><span class="wload">Checking today’s rain and snow…</span></div>
<div class="walert" style="margin-top:.75rem" id="aqi"><span class="wload">Loading air quality…</span></div></div></div>
<h2 style="margin-top:2.25rem">Next <em>24 hours</em></h2><div class="whours" id="hours"></div>
</div></section>
<section class="xs bg-secondary" id="forecast"><div class="container"><h2>7-day <em>forecast</em></h2>
<p class="sub">Karsog town, 1,404 m. Rain chance, total rain and snow for each day.</p>
<table class="xt wdays"><thead><tr><th>Day</th><th>Sky</th><th>High</th><th>Low</th><th>Rain / snow</th></tr></thead><tbody id="days"><tr><td colspan="5" class="wload">Loading…</td></tr></tbody></table>
</div></section>
<section class="xs" id="nearby"><div class="container"><h2>Weather at <em>nearby places</em></h2>
<p class="sub">Higher places are much colder than Karsog town and get snow first. Heights are from the forecast model.</p>
<table class="xt"><thead><tr><th>Place</th><th>Now</th><th>Temp</th><th>Today high / low</th></tr></thead><tbody id="near"><tr><td colspan="4" class="wload">Loading…</td></tr></tbody></table>
</div></section>
<section class="xs bg-secondary" id="snow"><div class="container"><h2>Snow in <em>Karsog</em></h2>
<p class="sub">Karsog town sits at about 1,404 m, so snow in town is occasional and usually light, in the coldest weeks of winter. Higher places such as Shikari Devi (about 3,359 m), Chindi and Janjehli get heavier snow, and their roads can close. The forecast above shows any snow expected in the next 7 days, and the table below shows how much fell in each of the last 12 months.</p>
</div></section>
<section class="xs" id="year"><div class="container"><h2>Last 12 months <em>month by month</em></h2>
<p class="sub">Average daily high and low, total rain and total snow at Karsog for each of the past 12 months, from weather records (ERA5 reanalysis). Useful for choosing when to visit.</p>
<table class="xt"><thead><tr><th>Month</th><th>Avg high</th><th>Avg low</th><th>Rain</th><th>Snow</th></tr></thead><tbody id="year"><tr><td colspan="5" class="wload">Loading…</td></tr></tbody></table>
<p class="xnote">Weather data: <a href="https://open-meteo.com/" target="_blank" rel="noopener">Open-Meteo</a> (forecast, air quality and past weather). Forecasts for mountain areas can be off; check again before a trip to the higher places.</p>
</div></section>
''' + WX_JS
# the months table needs a unique id
wx_body = wx_body.replace('<section class="xs" id="year">', '<section class="xs" id="months">')
page('/weather/', 'Karsog Weather Today — 7-Day Forecast, Rain, Snow & AQI (करसोग मौसम)',
     'Live Karsog weather: temperature now, next 24 hours, 7-day forecast, rain and snow alerts, air quality, weather at Shikari Devi, Janjehli and Tattapani, and the last 12 months.',
     'Weather', 'Live · updates itself', 'Karsog <em>weather</em>',
     'Today’s weather in Karsog town, the next 7 days, snow and rain alerts for the hill roads, air quality and the weather up at Shikari Devi and Janjehli.',
     wx_body, [('forecast', '7-day forecast'), ('nearby', 'Nearby places'), ('snow', 'Snow'), ('months', 'Last 12 months')],
     [('Does it snow in Karsog?', 'Karsog town is at about 1,404 m, so snow in town is occasional and usually light, in the coldest weeks of winter. Higher places such as Shikari Devi, Chindi and Janjehli get heavier snow and their roads can close. See the live 7-day forecast on this page.'),
      ('How high is Karsog?', 'Karsog town is at about 1,404 metres (4,606 feet) above sea level. Shikari Devi, the highest point nearby, is about 3,359 m.'),
      ('What is the weather in Karsog today?', 'This page shows the live temperature, today’s high and low, rain and snow alerts and the next 7 days for Karsog, updated automatically from Open-Meteo.')])

# ------------------------------------------------------------------ distances
# Road distance from Karsog bus stand along the shortest route, OpenStreetMap / OSRM, checked 27 Sep 2026.
DIST = [('Mamel (Mamleshwar Mahadev)', 1.2, '/mamleshwar/'), ('Kao (Kamaksha Devi)', 6, '/kao/'), ('Churag', 19, None),
        ('Pangna', 27, '/pangna-fort/'), ('Tattapani', 54, '/tattapani/'), ('Rohanda (start of the Kamru Nag trek)', 61, '/kamru-nag/'),
        ('Rampur Bushahr', 77, None), ('Janjehli', 88, '/janjehli/'), ('Sundernagar', 99, None), ('Shimla (ISBT Tutikandi)', 102, '/shimla-to-karsog-bus/'),
        ('Nerchowk', 103, None), ('Shikari Devi Temple', 103, '/shikari-devi/'), ('Mandi', 116, '/mandi-to-karsog-bus/'),
        ('Bhuntar Airport (Kullu)', 143, None), ('Solan', 143, None), ('Kullu', 155, None), ('Manali', 192, None),
        ('Chandigarh (ISBT Sector 43)', 213, None), ('Delhi (Kashmere Gate ISBT)', 451, '/bus/karsog-to-delhi/')]


def km(x):
    return f'{x:g} km'


drows = ''.join(
    f'<tr><td>{f"<a href={chr(34)}{u}{chr(34)}>{esc(n)}</a>" if u else esc(n)}</td><td class="n">{km(d)}</td>'
    f'<td><a href="https://www.google.com/maps/dir/Karsog,+Himachal+Pradesh/{esc(n.split(" (")[0].replace(" ", "+"))},+India" target="_blank" rel="noopener">Route &amp; time ↗</a></td></tr>'
    for n, d, u in DIST)
dist_body = BOX + f'''<section class="xs" id="table"><div class="container"><h2>Road distance <em>from Karsog</em></h2>
<p class="sub">From Karsog bus stand by the shortest road route. Hill roads are slow, so allow much more time than the distance suggests; tap “Route &amp; time” for live directions and today’s travel time.</p>
<table class="xt"><thead><tr><th>To</th><th>Distance</th><th>Directions</th></tr></thead><tbody>{drows}</tbody></table>
<p class="xnote">Distances measured on OpenStreetMap roads (OSRM routing) on 27 Sep 2026 and rounded. Other routes, such as Karsog–Shimla via Bagshad, can be longer. Buses: <a href="/karsog-bus-stand/">Karsog bus stand time table</a>.</p>
</div></section>
'''
page('/distance/', 'Distance from Karsog — Shimla, Mandi, Sundernagar, Rampur, Chandigarh, Delhi (km)',
     'Road distances from Karsog to Shimla (102 km), Mandi (116 km), Sundernagar (99 km), Rampur (77 km), Chandigarh, Delhi, Shikari Devi, Tattapani, Janjehli and more.',
     'Distances', 'Plan a trip', 'Distance from <em>Karsog</em>',
     'How far Karsog is from Shimla, Mandi, Sundernagar, Rampur, Chandigarh and Delhi, and from the temples and places nearby.',
     dist_body, (),
     [('How far is Karsog from Shimla?', 'About 102 km by road from Shimla ISBT (Tutikandi) to Karsog bus stand, via Tattapani. Buses take about 5 to 5½ hours.'),
      ('How far is Karsog from Mandi?', 'About 116 km by road from Mandi to Karsog.'),
      ('How far is Karsog from Sundernagar?', 'About 99 km by road from Sundernagar to Karsog.'),
      ('How far is Karsog from Rampur?', 'About 77 km by road from Rampur Bushahr to Karsog.'),
      ('How far is Karsog from Chandigarh?', 'About 213 km by road from Chandigarh ISBT Sector 43 to Karsog.'),
      ('How far is Shikari Devi from Karsog?', 'About 103 km by road from Karsog bus stand to Shikari Devi Temple, via Janjehli.')])

# ------------------------------------------------------------------ hotels
HOTELS = [('HPTDC Hotel Mamleshwar, Chindi', 'Government (HP Tourism) hotel at Chindi, about 15 km from Karsog, with a restaurant.', 'HPTDC Mamleshwar Chindi'),
          ('OMS Hotel', 'Karsog town.', 'OMS Hotel Karsog'), ('Hotel Mehta', 'Karsog town.', 'Mehta Hotel Karsog'),
          ('Hotel Tejas', 'Karsog town.', 'Hotel Tejas Karsog'), ('Hotel Sood', 'Karsog town.', 'Hotel Sood Karsog'),
          ('Hotel Mohan', 'Karsog town.', 'Mohan Hotel Karsog'), ('Hotel Tulsi', 'Karsog town.', 'Tulsi Hotel Karsog'),
          ('Divine Valley', 'Karsog town.', 'Divine Valley Karsog'), ('PWD Rest House, Karsog', 'Government rest house; booking through the PWD office.', 'PWD Rest House Karsog')]
hcards = ''.join(f'<div class="xcard"><b>{esc(n)}</b><small>{esc(d)}</small><a href="https://www.google.com/maps/search/{esc(q.replace(" ", "+"))}" target="_blank" rel="noopener">Location, photos &amp; phone ↗</a></div>'
                 for n, d, q in HOTELS)
hotel_body = BOX + f'''<section class="xs" id="list"><div class="container"><h2>Hotels in <em>Karsog</em></h2>
<p class="sub">Karsog is a small town with simple, family-run hotels, a government HPTDC hotel at Chindi, a PWD rest house and a few homestays. We don’t rate or take money from hotels. Tap a hotel for its location, photos, reviews and phone number, and call ahead in apple season (roughly July to October) and during big fairs.</p>
<div class="xcards">{hcards}</div>
<p class="xnote">Run a hotel or homestay in Karsog? Send your name, location and phone number with the “Submit an update” button and we’ll add it here.</p>
</div></section>
<section class="xs bg-secondary"><div class="container"><h2>Also useful</h2><p class="sub"><a href="/plan/#stay">Where to eat &amp; stay tips</a> · <a href="/plan/">Plan a trip</a> · <a href="/distance/">Distances</a> · <a href="/weather/">Weather</a></p></div></section>
'''
page('/hotels/', 'Hotels in Karsog, Himachal Pradesh — Where to Stay (HPTDC Chindi, Homestays)',
     'Hotels in Karsog, Himachal Pradesh: HPTDC Hotel Mamleshwar at Chindi, OMS, Mehta, Tejas, Sood, Mohan and Tulsi hotels, the PWD rest house and homestays, with maps and phone numbers.',
     'Hotels', 'Where to stay', 'Hotels in <em>Karsog</em>',
     'Places to stay in and around Karsog town, with a map link for each so you can see where it is and call.',
     hotel_body)

# ------------------------------------------------------------------ Karsog at a glance (on /contacts/)
GLANCE = [('PIN code (Karsog post office)', '175011'), ('STD / phone code', '01907'), ('Vehicle registration', 'HP-30'),
          ('District', 'Mandi, Himachal Pradesh'), ('Assembly constituency', '26 Karsog (SC)'),
          ('MLA', 'Deep Raj (BJP), elected 2022'), ('Lok Sabha constituency', 'Mandi'),
          ('Karsog tehsil', '534 villages, population 93,126 (Census 2011)'), ('Height of Karsog town', 'about 1,404 m')]
BANKS = [('State Bank of India, Karsog', 'SBIN0011884'), ('Punjab National Bank, Karsog', 'PUNB0074300'), ('HDFC Bank, Karsog', 'HDFC0008106')]
g_rows = ''.join(f'<div class="local-row"><span class="lbl">{esc(a)}</span><span class="val">{esc(b)}</span></div>' for a, b in GLANCE)
b_rows = ''.join(f'<div class="local-row"><span class="lbl">{esc(a)}</span><span class="val">{esc(b)}</span></div>' for a, b in BANKS)
glance = ('<!-- glance:start -->\n<section id="glance" class="bg-secondary"><div class="container"><div class="section-head"><span class="eyebrow">Codes &amp; facts</span>'
          '<h2>Karsog at a <em>glance</em></h2></div><div class="local-grid">'
          f'<div class="local"><div class="local-h"><span class="e">📮</span><h3>Codes &amp; facts</h3></div>{g_rows}</div>'
          f'<div class="local"><div class="local-h"><span class="e">🏦</span><h3>Bank IFSC codes</h3></div>{b_rows}'
          '<div class="local-row"><span class="lbl">Check any IFSC</span><a class="val" href="https://www.rbi.org.in/Scripts/IFSCMICRDetails.aspx" target="_blank" rel="noopener">RBI list ↗</a></div></div>'
          '<div class="local"><div class="local-h"><span class="e">🎓</span><h3>Education</h3></div>'
          '<div class="local-row"><span class="lbl">Government College Karsog</span><a class="val" href="tel:01907222116">01907-222116</a></div>'
          '<div class="local-row"><span class="lbl">College email</span><a class="val em" href="mailto:gckarsog-hp@nic.in">gckarsog-hp@nic.in</a></div>'
          '<div class="local-row"><span class="lbl">College website</span><a class="val" href="https://www.gckarsog.edu.in/" target="_blank" rel="noopener">gckarsog.edu.in ↗</a></div></div>'
          '</div><p class="xnote" style="margin-top:1.25rem">Checked 27 Sep 2026 against India Post, RBI/bank records, the college website and the Election Commission results. '
          'Spotted something out of date? Use the “Submit an update” button.</p></div></section>\n<!-- glance:end -->\n\n')
cp = os.path.join(PUB, 'contacts', 'index.html')
c = open(cp, encoding='utf-8').read()
c = re.sub(r'<!-- glance:start -->.*?<!-- glance:end -->\n\n', '', c, flags=re.S)
c = c.replace('<!-- Local Info -->', glance + '<!-- Local Info -->', 1)
if '<a href="#glance">' not in c:
    c = c.replace('<a href="#local">Offices & contacts</a>', '<a href="#glance">PIN, IFSC &amp; codes</a><a href="#local">Offices & contacts</a>', 1)
if '.xnote{' not in c:
    c = c.replace('</head>', '<style>.xnote{font-size:.85rem;color:var(--muted);line-height:1.6}</style>\n</head>', 1)
c = re.sub(r'(<meta name="description" content=")[^"]*',
           lambda m: m.group(1) + 'Karsog useful numbers: emergency, civil hospital, police, SDM and government offices, PIN code 175011, STD code 01907, bank IFSC codes (SBI, PNB, HDFC), college and MLA.', c)
c = re.sub(r'<title>.*?</title>', '<title>Karsog Useful Numbers — Emergency, Hospital, Police, PIN Code 175011 &amp; IFSC</title>', c)
open(cp, 'w', encoding='utf-8').write(c)

# ------------------------------------------------------------------ sitemap
sm_p = os.path.join(PUB, 'sitemap.xml')
sm = open(sm_p, encoding='utf-8').read()
sm = re.sub(r'<!-- extras -->.*?<!-- /extras -->\n?', '', sm, flags=re.S)
ent = ''.join(f'  <url><loc>https://karsog.com{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in ['/weather/', '/distance/', '/hotels/'])
sm = sm.replace('</urlset>', '<!-- extras -->\n' + ent + '<!-- /extras -->\n</urlset>')
open(sm_p, 'w', encoding='utf-8').write(sm)

import sitenav
sitenav.run()
print('weather, distance, hotels built; contacts updated')
