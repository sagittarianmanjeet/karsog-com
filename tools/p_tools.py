"""Practical pages: weather, distances, hotels, mandi rates."""
import json
from urllib.parse import quote_plus
from layout import L, icon, section, shead, faq_block, faq_ld, comments, note, esc, href
from data import DIST, DIST_CHECKED, DIST_CHECKED_HI


# ---------------------------------------------------------------- weather
NEAR = [('Shikari Devi', 'शिकारी देवी', '/shikari-devi/', 31.4784, 77.1657), ('Janjehli', 'जंजैहली', '/janjehli/', 31.5241, 77.2209),
        ('Kamru Nag', 'कमरूनाग', '/kamru-nag/', 31.4729, 77.0497),
        ('Tattapani', 'तत्तापानी', '/tattapani/', 31.2487, 77.0879), ('Pangna', 'पांगणा', '/pangna-fort/', 31.3863, 77.1230)]


def weather(lang):
    hl = lambda p: href(p, lang)
    load = L(lang, 'Loading…', 'लोड हो रहा है…')
    top = section(
        f'<h2 class="vh">{L(lang, "Karsog weather now", "करसोग का मौसम अभी")}</h2><div class="split"><div>'
        f'<div class="wx-card" id="wx-now" aria-live="polite"><p class="wx-load">{L(lang, "Loading live weather…", "लाइव मौसम लोड हो रहा है…")}</p></div></div>'
        f'<div class="stack"><div class="note" id="wx-alert"><p>{L(lang, "Checking today’s rain and snow…", "आज की बारिश और बर्फ़ देखी जा रही है…")}</p></div>'
        f'<div class="card"><h3>{L(lang, "Air quality", "हवा की गुणवत्ता")}</h3><div id="wx-aqi"><p>{load}</p></div></div></div></div>'
        f'<h2 class="mt2">{L(lang, "Next <em>24 hours</em>", "अगले <em>24 घंटे</em>")}</h2><div class="hours" id="wx-hours"></div>', 'sec-tight', 'now')
    days = section(shead(L(lang, 'Forecast', 'पूर्वानुमान'), L(lang, '7-day <em>forecast</em>', '7 दिन का <em>पूर्वानुमान</em>'),
                         L(lang, 'Karsog town, 1,404 m. Chance of rain, total rain and snow for each day.', 'करसोग शहर, 1,404 मीटर। हर दिन बारिश की संभावना, कुल बारिश और बर्फ़।'))
                   + f'<div class="tbl"><div class="tbl-scroll"><table><thead><tr><th>{L(lang, "Day", "दिन")}</th><th>{L(lang, "Sky", "आसमान")}</th>'
                     f'<th>{L(lang, "High", "अधिकतम")}</th><th>{L(lang, "Low", "न्यूनतम")}</th><th>{L(lang, "Rain / snow", "बारिश / बर्फ़")}</th></tr></thead>'
                     f'<tbody id="wx-days"><tr><td colspan="5">{load}</td></tr></tbody></table></div></div>', 'sec-alt', 'forecast')
    near = section(shead(L(lang, 'Up in the hills', 'ऊँची जगहें'), L(lang, 'Weather at <em>nearby places</em>', 'आसपास की जगहों का <em>मौसम</em>'),
                         L(lang, 'Higher places are much colder than Karsog town and get snow first. Heights are from the forecast model.',
                           'ऊँची जगहें करसोग शहर से कहीं ज़्यादा ठंडी होती हैं और वहाँ बर्फ़ पहले गिरती है। ऊँचाई पूर्वानुमान मॉडल से है।'))
                   + f'<div class="tbl"><div class="tbl-scroll"><table><thead><tr><th>{L(lang, "Place", "जगह")}</th><th>{L(lang, "Now", "अभी")}</th>'
                     f'<th>{L(lang, "Temp", "तापमान")}</th><th>{L(lang, "Today high / low", "आज अधिकतम / न्यूनतम")}</th></tr></thead>'
                     f'<tbody id="wx-near"><tr><td colspan="4">{load}</td></tr></tbody></table></div></div>', '', 'nearby')
    snow = section('<div class="split"><div class="prose">' +
                   f'<h2>{L(lang, "Snow in <em>Karsog</em>", "करसोग में <em>बर्फ़</em>")}</h2>' +
                   L(lang, '<p>Karsog town sits at about 1,404 m, so snow in town is occasional and usually light, in the coldest weeks of winter. '
                           'Higher places such as <a href="/shikari-devi/">Shikari Devi</a> (about 3,359 m), <a href="/chindi/">Chindi</a> and '
                           '<a href="/janjehli/">Janjehli</a> get heavier snow, and the road over Shikari Devi usually closes for the winter.</p>'
                           '<p>The 7-day forecast above shows any snow expected this week, and the table shows how much fell in each of the last 12 months.</p>',
                     '<p>करसोग शहर लगभग 1,404 मीटर की ऊँचाई पर है, इसलिए शहर में बर्फ़ कभी-कभार और हल्की गिरती है, सर्दी के सबसे ठंडे हफ़्तों में। '
                     '<a href="/hi/shikari-devi/">शिकारी देवी</a> (लगभग 3,359 मीटर), <a href="/hi/chindi/">चिंडी</a> और <a href="/hi/janjehli/">जंजैहली</a> जैसी ऊँची जगहों पर '
                     'ज़्यादा बर्फ़ गिरती है, और शिकारी देवी वाली सड़क आम तौर पर पूरी सर्दी बंद रहती है।</p>'
                     '<p>ऊपर 7 दिन का पूर्वानुमान इस हफ़्ते की संभावित बर्फ़ दिखाता है, और नीचे की तालिका पिछले 12 महीनों में हर महीने गिरी बर्फ़।</p>') +
                   '</div><div>' +
                   f'<div class="tbl"><div class="tbl-h"><b>{L(lang, "The last 12 months", "पिछले 12 महीने")}</b></div><div class="tbl-scroll"><table><thead><tr>'
                   f'<th>{L(lang, "Month", "महीना")}</th><th>{L(lang, "Avg high", "औसत अधिकतम")}</th><th>{L(lang, "Avg low", "औसत न्यूनतम")}</th>'
                   f'<th>{L(lang, "Rain", "बारिश")}</th><th>{L(lang, "Snow", "बर्फ़")}</th></tr></thead><tbody id="wx-year"><tr><td colspan="5">{load}</td></tr></tbody></table></div>'
                   f'<div class="tbl-f">{L(lang, "Weather records (ERA5 reanalysis) via Open-Meteo.", "मौसम रिकॉर्ड (ERA5) Open-Meteo से।")}</div></div></div></div>', 'sec-alt', 'snow')
    src = section(note(L(lang, 'Weather data: <a href="https://open-meteo.com/" target="_blank" rel="noopener">Open-Meteo</a> (forecast, air quality and past weather). '
                               'Forecasts for mountain areas can be off; check again before a trip to the higher places.',
                         'मौसम का डेटा: <a href="https://open-meteo.com/" target="_blank" rel="noopener">Open-Meteo</a> (पूर्वानुमान, हवा की गुणवत्ता और पिछला मौसम)। '
                         'पहाड़ों का पूर्वानुमान ग़लत भी हो सकता है; ऊँची जगहों पर जाने से पहले दोबारा देख लें।')), 'sec-tight')
    fq = [(L(lang, 'Does it snow in Karsog?', 'क्या करसोग में बर्फ़ गिरती है?'),
           L(lang, 'Karsog town is at about 1,404 m, so snow in town is occasional and usually light, in the coldest weeks of winter. Shikari Devi, Chindi and Janjehli get heavier snow and their roads can close.',
             'करसोग शहर लगभग 1,404 मीटर पर है, इसलिए शहर में बर्फ़ कभी-कभार और हल्की गिरती है, सर्दी के सबसे ठंडे हफ़्तों में। शिकारी देवी, चिंडी और जंजैहली में ज़्यादा बर्फ़ गिरती है और सड़कें बंद हो सकती हैं।')),
          (L(lang, 'How high is Karsog?', 'करसोग कितनी ऊँचाई पर है?'),
           L(lang, 'Karsog town is about 1,404 metres (4,606 feet) above sea level. Shikari Devi, the highest point nearby, is about 3,359 m.',
             'करसोग शहर समुद्र तल से लगभग 1,404 मीटर (4,606 फ़ुट) की ऊँचाई पर है। पास की सबसे ऊँची जगह, शिकारी देवी, लगभग 3,359 मीटर पर है।')),
          (L(lang, 'What is the best weather to visit Karsog?', 'करसोग घूमने के लिए सबसे अच्छा मौसम कब है?'),
           L(lang, 'Spring (March–May) and autumn (September–November) are mild and clear. July and August bring heavy monsoon rain, and winters are cold with snow higher up.',
             'वसंत (मार्च–मई) और पतझड़ (सितंबर–नवंबर) में मौसम सुहावना और साफ़ रहता है। जुलाई–अगस्त में तेज़ बरसात होती है, और सर्दियाँ ठंडी होती हैं, ऊपर बर्फ़ के साथ।'))]
    near_j = [[L(lang, en, hi), href(u, lang), la, lo] for en, hi, u, la, lo in NEAR]
    return dict(path='/weather/', lang=lang, kind='weather', hero='band',
                title=L(lang, 'Karsog Weather Today — 7-Day Forecast, Rain, Snow & AQI', 'करसोग का मौसम आज — 7 दिन का पूर्वानुमान, बारिश, बर्फ़'),
                desc=L(lang, 'Live Karsog weather: temperature now, next 24 hours, 7-day forecast, rain and snow alerts for the hill roads, air quality, and the weather at Shikari Devi and Janjehli.',
                       'करसोग का लाइव मौसम: अभी का तापमान, अगले 24 घंटे, 7 दिन का पूर्वानुमान, पहाड़ी सड़कों के लिए बारिश और बर्फ़ की चेतावनी, हवा की गुणवत्ता, और शिकारी देवी व जंजैहली का मौसम।'),
                kicker=L(lang, 'Live · updates by itself', 'लाइव · अपने-आप अपडेट'), h1=L(lang, 'Karsog <em>weather</em>', 'करसोग का <em>मौसम</em>'),
                lede=L(lang, 'Today’s weather in Karsog town, the next 7 days, snow and rain alerts for the hill roads, and the weather up at Shikari Devi and Janjehli.',
                       'करसोग शहर का आज का मौसम, अगले 7 दिन, पहाड़ी सड़कों के लिए बर्फ़ और बारिश की चेतावनी, और ऊपर शिकारी देवी व जंजैहली का मौसम।'),
                chips=[('mountain', L(lang, 'Karsog town, 1,404 m', 'करसोग शहर, 1,404 मी')), ('clock', L(lang, 'Live forecast', 'लाइव पूर्वानुमान'))],
                hero_extra='<div class="jump">' + ''.join(f'<a href="#{k}">{L(lang, en, hi)}</a>' for k, en, hi in [
                    ('forecast', '7 days', '7 दिन'), ('nearby', 'Nearby places', 'आसपास'), ('snow', 'Snow & past year', 'बर्फ़ और पिछला साल')]) + '</div>',
                crumbs=[(L(lang, 'Weather', 'मौसम'), '/weather/')], body=top + days + near + snow + src + faq_block(fq, lang),
                ld=[faq_ld(fq)], data={'j-near': near_j}, scripts=['/assets/weather.js'], og='/og/weather.jpg')


# ---------------------------------------------------------------- distances
def distance(lang):
    hl = lambda p: href(p, lang)
    rows = ''
    for en, hi, km, ten, thi, page, nen, nhi in DIST:
        name = L(lang, en, hi)
        nm = f'<a href="{hl(page)}">{esc(name)}</a>' if page else esc(name)
        n = L(lang, nen, nhi)
        dest = quote_plus(en.split(' (')[0] + ', Himachal Pradesh') if 'Delhi' not in en and 'Chandigarh' not in en else quote_plus(en)
        go = f'https://www.google.com/maps/dir/?api=1&amp;origin=Karsog+Bus+Stand&amp;destination={dest}'
        rows += (f'<tr><td>{nm}' + (f'<small>{esc(n)}</small>' if n else '') + f'</td><td class="t">{km:g} {L(lang, "km", "किमी")}</td>'
                 f'<td class="hide-s">{L(lang, ten, thi)}</td><td><a href="{go}" target="_blank" rel="noopener">{icon("nav")}<span class="sr">{L(lang, "Directions to ", "रास्ता: ")}{esc(name)}</span></a></td></tr>')
    table = section(shead(L(lang, 'By road', 'सड़क से'), L(lang, 'Distance <em>from Karsog</em>', 'करसोग से <em>दूरी</em>'),
                          L(lang, f'From Karsog bus stand by the fastest road route on Google Maps, checked on {DIST_CHECKED}. Hill roads are slow; tap the arrow for live directions and today’s travel time.',
                            f'करसोग बस अड्डे से, गूगल मैप्स के सबसे तेज़ सड़क रास्ते से, {DIST_CHECKED_HI} को देखी गई। पहाड़ी सड़कों पर समय ज़्यादा लगता है; आज का सही समय और रास्ता देखने के लिए तीर को छुएँ।'))
                    + f'<div class="tbl"><div class="tbl-scroll"><table><thead><tr><th>{L(lang, "To", "कहाँ तक")}</th><th>{L(lang, "Distance", "दूरी")}</th>'
                      f'<th class="hide-s">{L(lang, "By car", "गाड़ी से")}</th><th><span class="sr">{L(lang, "Directions", "रास्ता")}</span></th></tr></thead><tbody>{rows}</tbody></table></div></div>'
                    + note(L(lang, 'Driving times are Google’s estimates for a car. Buses take longer. In the monsoon and in winter, some hill roads close; check the <a href="/weather/">weather</a> first.',
                             'गाड़ी का समय गूगल का अनुमान है। बस में ज़्यादा समय लगता है। बरसात और सर्दियों में कुछ पहाड़ी सड़कें बंद हो जाती हैं; पहले <a href="/hi/weather/">मौसम</a> देख लें।')), '', 'table')
    fq = []
    for key in ['Shimla (ISBT Tutikandi)', 'Mandi', 'Sundernagar', 'Rampur Bushahr', 'Chandigarh (ISBT Sector 43)', 'Shikari Devi temple', 'Tattapani']:
        d = next(x for x in DIST if x[0] == key)
        en, hi = d[0].split(' (')[0], d[1].split(' (')[0]
        fq.append((L(lang, f'How far is Karsog from {en}?', f'{hi} से करसोग कितनी दूर है?'),
                   L(lang, f'About {d[2]:g} km by road from Karsog bus stand, around {d[3]} by car (Google Maps, {DIST_CHECKED}).',
                     f'करसोग बस अड्डे से सड़क से लगभग {d[2]:g} किमी, गाड़ी से लगभग {d[4]} (गूगल मैप्स, {DIST_CHECKED_HI})।')))
    return dict(path='/distance/', lang=lang, kind='tool', hero='band',
                title=L(lang, 'Distance from Karsog — Shimla, Mandi, Chandigarh, Delhi (km)', 'करसोग से दूरी — शिमला, मंडी, चंडीगढ़, दिल्ली (किमी)'),
                desc=L(lang, 'Road distances and driving times from Karsog to Shimla (94 km), Mandi (99 km), Sundernagar, Rampur, Chandigarh, Delhi, Shikari Devi, Tattapani and more.',
                       'करसोग से शिमला (94 किमी), मंडी (99 किमी), सुंदरनगर, रामपुर, चंडीगढ़, दिल्ली, शिकारी देवी, तत्तापानी और दूसरी जगहों की सड़क दूरी और समय।'),
                kicker=L(lang, 'Plan a trip', 'यात्रा योजना'), h1=L(lang, 'Distance from <em>Karsog</em>', 'करसोग से <em>दूरी</em>'),
                lede=L(lang, 'How far Karsog is from Shimla, Mandi, Chandigarh and Delhi, and from the temples and places around it, with driving times.',
                       'करसोग से शिमला, मंडी, चंडीगढ़ और दिल्ली, और आसपास के मंदिरों और जगहों की दूरी, गाड़ी के समय के साथ।'),
                chips=[('route', L(lang, f'Checked {DIST_CHECKED}', f'{DIST_CHECKED_HI} को देखा गया'))],
                crumbs=[(L(lang, 'Distances', 'दूरी'), '/distance/')], body=table + faq_block(fq, lang), ld=[faq_ld(fq)])


# ---------------------------------------------------------------- hotels
HOTELS = [('HPTDC Hotel Mamleshwar, Chindi', 'एचपीटीडीसी होटल ममलेश्वर, चिंडी', 'Government (HP Tourism) hotel at Chindi, about 7 km from Karsog, with a restaurant and valley views.',
           'चिंडी में सरकारी (हिमाचल पर्यटन) होटल, करसोग से लगभग 7 किमी, रेस्टोरेंट और घाटी के नज़ारों के साथ।', 'HPTDC Hotel Mamleshwar Chindi'),
          ('OMS Hotel', 'ओएमएस होटल', 'Karsog town.', 'करसोग शहर।', 'OMS Hotel Karsog'),
          ('Hotel Mehta', 'होटल मेहता', 'Karsog town.', 'करसोग शहर।', 'Mehta Hotel Karsog'),
          ('Hotel Tejas', 'होटल तेजस', 'Karsog town.', 'करसोग शहर।', 'Hotel Tejas Karsog'),
          ('Hotel Sood', 'होटल सूद', 'Karsog town.', 'करसोग शहर।', 'Hotel Sood Karsog'),
          ('Hotel Mohan', 'होटल मोहन', 'Karsog town.', 'करसोग शहर।', 'Mohan Hotel Karsog'),
          ('Hotel Tulsi', 'होटल तुलसी', 'Karsog town.', 'करसोग शहर।', 'Tulsi Hotel Karsog'),
          ('Divine Valley', 'डिवाइन वैली', 'Karsog town.', 'करसोग शहर।', 'Divine Valley Karsog'),
          ('PWD Rest House, Karsog', 'पीडब्ल्यूडी रेस्ट हाउस, करसोग', 'Government rest house; booking through the PWD office, subject to availability.',
           'सरकारी रेस्ट हाउस; बुकिंग पीडब्ल्यूडी दफ़्तर से, जगह मिलने पर।', 'PWD Rest House Karsog')]


def hotels(lang):
    hl = lambda p: href(p, lang)
    cards = ''.join(f'<div class="card"><h3>{esc(L(lang, en, hi))}</h3><p>{esc(L(lang, den, dhi))}</p>'
                    f'<p><a class="more-link" href="https://www.google.com/maps/search/{quote_plus(q)}" target="_blank" rel="noopener">'
                    f'{L(lang, "Map, photos & phone", "नक्शा, फ़ोटो और फ़ोन")} {icon("ext")}</a></p></div>'
                    for en, hi, den, dhi, q in HOTELS)
    lst = section(shead(L(lang, 'Where to stay', 'कहाँ ठहरें'), L(lang, 'Hotels in <em>Karsog</em>', 'करसोग के <em>होटल</em>'),
                        L(lang, 'Karsog is a small town with simple, family-run hotels, a government HPTDC hotel at Chindi, a PWD rest house and a few homestays. '
                                'We don’t rate hotels or take money from them. Tap a hotel for its location, photos, reviews and phone number.',
                          'करसोग एक छोटा शहर है, जहाँ परिवारों के चलाए सादे होटल, चिंडी में सरकारी एचपीटीडीसी होटल, एक पीडब्ल्यूडी रेस्ट हाउस और कुछ होमस्टे हैं। '
                          'हम होटलों की रेटिंग नहीं करते और न ही उनसे पैसे लेते हैं। जगह, फ़ोटो, समीक्षाएँ और फ़ोन नंबर देखने के लिए होटल के लिंक को छुएँ।'))
                  + f'<div class="grid g3">{cards}</div>', '', 'list')
    tips = section('<div class="grid g3">' +
                   f'<div class="card icard"><span class="i">{icon("calendar")}</span><span><b>{L(lang, "Book ahead", "पहले से बुक करें")}</b>'
                   f'<span>{L(lang, "In apple season (roughly July to October) and during big fairs like the Mahunag Mela in May.", "सेब के मौसम (लगभग जुलाई से अक्टूबर) और माहूँनाग मेले (मई) जैसे बड़े मेलों के दौरान।")}</span></span></div>'
                   f'<div class="card icard"><span class="i">{icon("home")}</span><span><b>{L(lang, "Homestays", "होमस्टे")}</b>'
                   f'<span>{L(lang, "Villages around Karsog, Pangna and Janjehli have homestays with home-cooked Himachali food. Ask locally.", "करसोग, पांगणा और जंजैहली के आसपास के गाँवों में घर का बना हिमाचली खाना देने वाले होमस्टे हैं। स्थानीय लोगों से पूछें।")}</span></span></div>'
                   f'<div class="card icard"><span class="i">{icon("pin")}</span><span><b>{L(lang, "Nearby", "आसपास")}</b>'
                   f'<span>{L(lang, "Tattapani and Janjehli also have guesthouses, handy for the hot springs or Shikari Devi.", "तत्तापानी और जंजैहली में भी गेस्टहाउस हैं, गर्म चश्मों या शिकारी देवी के लिए सुविधाजनक।")}</span></span></div></div>'
                   + note(L(lang, 'Run a hotel or homestay in Karsog? <a href="#update" data-open="upd">Send us</a> its name, place and phone number and we’ll add it here.',
                            'करसोग में होटल या होमस्टे चलाते हैं? उसका नाम, जगह और फ़ोन नंबर <a href="#update" data-open="upd">हमें भेजें</a>, हम उसे यहाँ जोड़ देंगे।')), 'sec-alt', 'tips')
    fq = [(L(lang, 'Where can I stay in Karsog?', 'करसोग में कहाँ ठहरें?'),
           L(lang, 'In one of the small hotels in Karsog town, at the HPTDC Hotel Mamleshwar at Chindi (about 7 km away), at the PWD rest house or in a homestay.',
             'करसोग शहर के छोटे होटलों में, चिंडी के एचपीटीडीसी होटल ममलेश्वर में (लगभग 7 किमी दूर), पीडब्ल्यूडी रेस्ट हाउस में या किसी होमस्टे में।')),
          (L(lang, 'Is there a government hotel in Karsog?', 'क्या करसोग में सरकारी होटल है?'),
           L(lang, 'Yes, Himachal Tourism (HPTDC) runs the Hotel Mamleshwar at Chindi, about 7 km from Karsog. There is also a PWD rest house in Karsog.',
             'हाँ, हिमाचल पर्यटन (एचपीटीडीसी) चिंडी में होटल ममलेश्वर चलाता है, करसोग से लगभग 7 किमी। करसोग में एक पीडब्ल्यूडी रेस्ट हाउस भी है।'))]
    return dict(path='/hotels/', lang=lang, kind='tool', hero='band',
                title=L(lang, 'Hotels in Karsog — HPTDC Chindi, Town Hotels & Homestays', 'करसोग के होटल — एचपीटीडीसी चिंडी, शहर के होटल और होमस्टे'),
                desc=L(lang, 'Hotels in Karsog, Himachal Pradesh: HPTDC Hotel Mamleshwar at Chindi, OMS, Mehta, Tejas, Sood, Mohan and Tulsi hotels, the PWD rest house and homestays, with maps.',
                       'करसोग (हिमाचल प्रदेश) के होटल: चिंडी में एचपीटीडीसी होटल ममलेश्वर, ओएमएस, मेहता, तेजस, सूद, मोहन और तुलसी होटल, पीडब्ल्यूडी रेस्ट हाउस और होमस्टे, नक्शे के साथ।'),
                kicker=L(lang, 'Plan a trip', 'यात्रा योजना'), h1=L(lang, 'Hotels in <em>Karsog</em>', 'करसोग के <em>होटल</em>'),
                lede=L(lang, 'Places to stay in and around Karsog town, each with a map link so you can see where it is and call ahead.',
                       'करसोग शहर और आसपास ठहरने की जगहें, हर एक के नक्शे के लिंक के साथ, ताकि आप जगह देख सकें और पहले फ़ोन कर सकें।'),
                crumbs=[(L(lang, 'Plan a trip', 'यात्रा योजना'), '/plan/'), (L(lang, 'Hotels', 'होटल'), '/hotels/')],
                body=lst + tips + faq_block(fq, lang), ld=[faq_ld(fq)])


# ---------------------------------------------------------------- mandi rates
def mandi_rates(lang):
    stats = (f'<div class="facts" aria-live="polite"><div><b id="mr-date">—</b><small>{L(lang, "Latest report", "ताज़ा रिपोर्ट")}</small></div>'
             f'<div><b id="mr-mkts">—</b><small>{L(lang, "Markets", "मंडियाँ")}</small></div>'
             f'<div><b id="mr-items">—</b><small>{L(lang, "Price lines", "भाव")}</small></div></div>')
    tool = section(
        '<p id="mr-stale" class="note" role="status" hidden></p>' +
        note(L(lang, '<b>Karsog has no reporting APMC yard.</b> The nearest official prices are from the Mandi district yards (Kangni, Takoli, Dhanotu, Jogindernagar, Chail Chowk) '
                     'and from Shimla and Solan. Prices are <b>₹ per quintal (100 kg)</b>; ₹ per kg is shown for convenience.',
               '<b>करसोग में भाव भेजने वाली एपीएमसी मंडी नहीं है।</b> सबसे पास के सरकारी भाव मंडी ज़िले की मंडियों (कांगणी, टकोली, धनोटू, जोगिंदरनगर, चैलचौक) '
               'और शिमला व सोलन से हैं। भाव <b>₹ प्रति क्विंटल (100 किलो)</b> में हैं; सुविधा के लिए ₹ प्रति किलो भी दिखाया गया है।')) +
        f'<h2 class="mt2">{L(lang, "Rates by <em>market</em>", "मंडी के हिसाब से <em>भाव</em>")}</h2>'
        f'<div class="fchips" id="mr-chips" role="group" aria-label="{L(lang, "Filter by crop", "फ़सल चुनें")}"></div>'
        f'<div class="mr-tools"><input id="mr-q" type="search" placeholder="{L(lang, "Search market or crop (e.g. Parwanoo, tomato)", "मंडी या फ़सल खोजें (जैसे परवाणू, टमाटर)")}" '
        f'aria-label="{L(lang, "Search", "खोजें")}"><select id="mr-dist" aria-label="{L(lang, "District", "ज़िला")}"><option value="">{L(lang, "All districts", "सभी ज़िले")}</option></select></div>'
        f'<div id="mr-list"><p class="msg-box">{L(lang, "Loading today’s rates…", "आज के भाव लोड हो रहे हैं…")}</p></div>'
        f'<p id="mr-none" class="msg-box" hidden>{L(lang, "No prices match this filter. Try “All” or clear the search.", "इस चुनाव में कोई भाव नहीं मिला। “सभी” चुनें या खोज हटाएँ।")}</p>'
        f'<p id="mr-err" class="msg-box" hidden>{L(lang, "Couldn’t load prices right now. Please try again in a few minutes.", "अभी भाव लोड नहीं हो पाए। कुछ मिनट बाद फिर कोशिश करें।")}</p>'
        f'<noscript><p class="note">{L(lang, "Please turn on JavaScript to see the live price table.", "लाइव भाव देखने के लिए जावास्क्रिप्ट चालू करें।")}</p></noscript>'
        f'<p class="mt1"><small>{L(lang, "Prices are indicative and may contain reporting errors; confirm with the market before you buy or sell. Source: Agmarknet, Ministry of Agriculture &amp; Farmers Welfare, via", "भाव अनुमानित हैं और इनमें ग़लती हो सकती है; ख़रीदने या बेचने से पहले मंडी से पुष्टि कर लें। स्रोत: एगमार्कनेट, कृषि एवं किसान कल्याण मंत्रालय,")} '
        f'<a href="https://data.gov.in/" rel="noopener">data.gov.in</a> (Government Open Data License – India). <span id="mr-built"></span></small></p>', '', 'rates', 'wrap wrap-n')
    fq = [(L(lang, 'Where do these prices come from?', 'ये भाव कहाँ से आते हैं?'),
           L(lang, 'From the Government of India’s Agmarknet system, published on data.gov.in. Each APMC market reports the minimum, maximum and most common (“modal”) price for the day. This page stores every day’s report, so trends build up over time.',
             'भारत सरकार के एगमार्कनेट सिस्टम से, जो data.gov.in पर प्रकाशित होता है। हर एपीएमसी मंडी दिन का न्यूनतम, अधिकतम और सबसे आम (“मॉडल”) भाव भेजती है। यह पेज हर दिन की रिपोर्ट सहेजता है, इसलिए समय के साथ रुझान दिखने लगता है।')),
          (L(lang, 'Why doesn’t the apple price match what my aadhti quotes per box?', 'सेब का भाव मेरे आढ़ती के पेटी वाले भाव से क्यों नहीं मिलता?'),
           L(lang, 'Official figures are averages per quintal across all lots of a variety and grade that day. Box rates depend on size, colour, packing and the buyer. Use these numbers to see which way the market is moving, not as the price of a particular box.',
             'सरकारी आँकड़े उस दिन किसी किस्म और ग्रेड के सभी लॉट का प्रति क्विंटल औसत हैं। पेटी का भाव आकार, रंग, पैकिंग और ख़रीदार पर निर्भर करता है। इन आँकड़ों से बाज़ार का रुख़ देखें, किसी ख़ास पेटी का भाव नहीं।')),
          (L(lang, 'Why is a market missing today?', 'आज कोई मंडी क्यों नहीं दिख रही?'),
           L(lang, 'Markets report only on the days they trade, and some report late. Each market card shows the date of its last report; cards older than two days are marked.',
             'मंडियाँ सिर्फ़ उन्हीं दिनों भाव भेजती हैं जब वहाँ कारोबार होता है, और कुछ देर से भेजती हैं। हर मंडी के कार्ड पर आख़िरी रिपोर्ट की तारीख़ दिखती है; दो दिन से पुराने कार्ड अलग रंग में हैं।')),
          (L(lang, 'What do PMY, SMY and TSMY mean?', 'पीएमवाई, एसएमवाई और टीएसएमवाई का क्या मतलब है?'),
           L(lang, 'Principal Market Yard, Sub Market Yard and Tertiary Sub Market Yard: the three levels of APMC market yards in Himachal.',
             'प्रिंसिपल मार्केट यार्ड, सब मार्केट यार्ड और टर्शियरी सब मार्केट यार्ड: हिमाचल में एपीएमसी मंडियों के तीन स्तर।'))]
    ld = [faq_ld(fq), {'@context': 'https://schema.org', '@type': 'Dataset', 'name': L(lang, 'Himachal Pradesh mandi (APMC) prices', 'हिमाचल प्रदेश मंडी (एपीएमसी) भाव'),
                       'description': L(lang, 'Daily apple, vegetable and fruit prices reported by Himachal Pradesh APMC markets, from Agmarknet.',
                                        'हिमाचल प्रदेश की एपीएमसी मंडियों के सेब, सब्ज़ी और फलों के दैनिक भाव, एगमार्कनेट से।'),
                       'url': 'https://karsog.com' + href('/mandi-rates/', lang), 'isAccessibleForFree': True,
                       'license': 'https://data.gov.in/government-open-data-license-india',
                       'creator': {'@type': 'Organization', 'name': 'Agmarknet, Ministry of Agriculture & Farmers Welfare, Government of India'}}]
    return dict(path='/mandi-rates/', lang=lang, kind='tool', hero='band',
                title=L(lang, 'Apple Rate Today — Himachal Mandi Rates (Mandi, Shimla, Solan)', 'सेब का भाव आज — हिमाचल मंडी भाव (मंडी, शिमला, सोलन)'),
                desc=L(lang, 'Daily apple, vegetable and fruit rates from Himachal APMC markets: Parwanoo, Solan, Shimla and the Mandi district yards. Updated automatically from official Agmarknet data.',
                       'हिमाचल की एपीएमसी मंडियों के सेब, सब्ज़ी और फलों के रोज़ के भाव: परवाणू, सोलन, शिमला और मंडी ज़िले की मंडियाँ। सरकारी एगमार्कनेट डेटा से अपने-आप अपडेट।'),
                kicker=L(lang, 'Daily APMC prices', 'रोज़ के एपीएमसी भाव'), h1=L(lang, 'Mandi rates <em>today</em>', 'आज के <em>मंडी भाव</em>'),
                lede=L(lang, 'Apple, vegetable and fruit prices reported by Himachal’s APMC markets, updated several times a day from official Agmarknet data.',
                       'हिमाचल की एपीएमसी मंडियों से आए सेब, सब्ज़ी और फलों के भाव, सरकारी एगमार्कनेट डेटा से दिन में कई बार अपडेट।'),
                hero_extra=stats, crumbs=[(L(lang, 'Mandi rates', 'मंडी भाव'), '/mandi-rates/')],
                body=tool + comments('mandi-rates', lang, L(lang, 'Comments', 'टिप्पणियाँ'),
                                     L(lang, 'Rate at your mandi different from what is shown? Tell others here.', 'आपकी मंडी का भाव यहाँ से अलग है? दूसरों को यहाँ बताइए।'),
                                     L(lang, 'e.g. Tomato at Karsog sold for ₹30/kg today.', 'जैसे: आज करसोग में टमाटर ₹30 किलो बिका।')) + faq_block(fq, lang),
                ld=ld, scripts=['/assets/mandi.js'], og='/og/mandi.jpg')
