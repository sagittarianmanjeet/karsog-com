"""Home page (/ and /hi/)."""
from layout import L, icon, img, section, shead, faq_block, faq_ld, pcard, esc
from data import HRTC, P_DEP, MELAS, MON_EN, MON_HI, next_bus_json, melas_json, pbase, PHOTOS, PLACES, place_title

TILES = [
    ('/karsog-bus-stand/', 'bus', 'Buses', 'बसें', 'Every departure from Karsog, HRTC and private', 'करसोग से हर बस, एचआरटीसी और प्राइवेट'),
    ('/weather/', 'weather', 'Weather', 'मौसम', 'Live forecast, rain and snow alerts', 'लाइव मौसम, बारिश और बर्फ़ की चेतावनी'),
    ('/temples/', 'temple', 'Temples', 'मंदिर', 'Mahunag, Mamleshwar, Kamaksha and more', 'माहूँनाग, ममलेश्वर, कामाक्षा और दूसरे मंदिर'),
    ('/melas/', 'party', 'Melas', 'मेले', 'Every big fair, month by month', 'हर बड़ा मेला, महीने के हिसाब से'),
    ('/hotels/', 'bed', 'Hotels', 'होटल', 'Where to stay in and around Karsog', 'करसोग और आसपास कहाँ ठहरें'),
    ('/distance/', 'ruler', 'Distances', 'दूरी', 'Shimla, Mandi, Chandigarh, Delhi…', 'शिमला, मंडी, चंडीगढ़, दिल्ली…'),
    ('/contacts/', 'phone', 'Useful numbers', 'ज़रूरी नंबर', 'Hospital, police, offices, PIN, IFSC', 'अस्पताल, पुलिस, दफ़्तर, पिन कोड, IFSC'),
    ('/mandi-rates/', 'apple', 'Mandi rates', 'मंडी भाव', 'Today’s apple and vegetable prices', 'आज के सेब और सब्ज़ी के भाव'),
]

# (page, photo, English name, Hindi name, English line, Hindi line, tag en, tag hi)
PLACES_HOME = [
    ('/shikari-devi/', 'shikari-devi-005', 'Shikari Devi', 'शिकारी देवी', 'Roofless temple on a 3,359 m peak · 22 km', '3,359 मीटर की चोटी पर बिना छत का मंदिर · 22 किमी', 'Peak', 'चोटी'),
    ('/mahunag/', 'mahunag-214', 'Mahunag', 'माहूँनाग', 'The valley’s most famous temple · 26 km', 'घाटी का सबसे प्रसिद्ध मंदिर · 26 किमी', 'Temple', 'मंदिर'),
    ('/mamleshwar/', 'mamleshwar-322', 'Mamleshwar Mahadev', 'ममलेश्वर महादेव', 'Ancient Shiva temple · 2 km', 'प्राचीन शिव मंदिर · 2 किमी', '', ''),
    ('/tattapani/', 'tattapani-102', 'Tattapani', 'तत्तापानी', 'Hot springs on the Sutlej · 46 km', 'सतलुज किनारे गर्म पानी के चश्मे · 46 किमी', '', ''),
    ('/kao/', 'kao-326', 'Kamaksha Devi, Kao', 'कामाक्षा देवी, काओ', 'Goddess temple · 7 km', 'देवी का मंदिर · 7 किमी', '', ''),
    ('/pangna-fort/', 'pangna-fort-244', 'Pangna', 'पांगणा', 'Fort-temple of the Suket kings · 19 km', 'सुकेत राजाओं का क़िला-मंदिर · 19 किमी', '', ''),
    ('/chindi/', 'chindi-295', 'Chindi', 'चिंडी', 'Orchards, temple, sunsets · 7 km', 'बगीचे, मंदिर, सूर्यास्त · 7 किमी', '', ''),
    ('/janjehli/', 'janjehli-031', 'Janjehli', 'जंजैहली', 'Valley below Shikari Devi · 27 km', 'शिकारी देवी के नीचे की घाटी · 27 किमी', '', ''),
    ('/karsog-town/', 'karsog-town-001', 'Karsog town', 'करसोग शहर', 'Old bazaar & Laxmi Narayan temple', 'पुराना बाज़ार और लक्ष्मी नारायण मंदिर', '', ''),
]
MOSAIC = ['nanj-019', 'latheri-bhanthal-012', 'seri-bunglow-034', 'beludhar-006', 'luhri-anni-016']
DIST = [('Shimla', 'शिमला', 94), ('Mandi', 'मंडी', 99), ('Sundernagar', 'सुंदरनगर', 80), ('Rampur', 'रामपुर', 75),
        ('Bhuntar airport (Kullu)', 'भुंतर हवाई अड्डा (कुल्लू)', 150), ('Chandigarh', 'चंडीगढ़', 217), ('Delhi', 'दिल्ली', 434)]
DIAL = [('112', 'National emergency', 'राष्ट्रीय आपातकाल'), ('108', 'Ambulance', 'एम्बुलेंस'), ('100', 'Police', 'पुलिस'),
        ('01907-222218', 'Civil Hospital Karsog', 'सिविल अस्पताल करसोग'), ('01907-222221', 'Police Station Karsog', 'पुलिस थाना करसोग'),
        ('+91 93172-07043', 'Karsog Control Room', 'करसोग कंट्रोल रूम'), ('1077', 'Disaster / flood', 'आपदा / बाढ़'),
        ('1912', 'Power fault', 'बिजली की शिकायत')]


def tel(n):
    return 'tel:' + n.replace(' ', '').replace('-', '').replace('+91', '+91')


def faqs(lang):
    return [
        (L(lang, 'What is the first bus from Mandi to Karsog?', 'मंडी से करसोग की पहली बस कितने बजे है?'),
         L(lang, 'HRTC online booking lists one Mandi to Karsog service, at 4:30 AM (₹285, about 5¾ hours; checked 25 Sep 2026). '
                 'Local timings put the first ordinary bus around 6:00 AM, arriving about 9:00 AM. Confirm at the Mandi bus stand. '
                 '<a href="/mandi-to-karsog-bus/">All Mandi ⇄ Karsog buses</a>.',
           'एचआरटीसी की ऑनलाइन बुकिंग में मंडी से करसोग की एक बस सुबह 4:30 बजे की है (₹285, लगभग 5¾ घंटे; 25 सितंबर 2026 को देखा गया)। '
           'स्थानीय जानकारी के अनुसार पहली साधारण बस सुबह लगभग 6:00 बजे चलती है और लगभग 9:00 बजे पहुँचती है। मंडी बस अड्डे पर पुष्टि कर लें। '
           '<a href="/hi/mandi-to-karsog-bus/">मंडी ⇄ करसोग की सभी बसें</a>।')),
        (L(lang, 'What is the last bus from Karsog to Mandi?', 'करसोग से मंडी की आख़िरी बस कितने बजे है?'),
         L(lang, 'By the timetable board at Karsog bus stand (photographed 25 Sep 2026), the last direct bus to Mandi leaves at 5:15 PM. '
                 'Other Mandi buses leave at 9:30 AM, 11:10 AM (via Sorta, also bookable online) and 2:00 PM (the Reckong Peo bus, via Sorta). Confirm at the stand.',
           'करसोग बस अड्डे के टाइम-टेबल बोर्ड (25 सितंबर 2026 की फ़ोटो) के अनुसार मंडी की आख़िरी सीधी बस शाम 5:15 बजे चलती है। '
           'मंडी की दूसरी बसें सुबह 9:30, सुबह 11:10 (वाया सोरता, ऑनलाइन बुकिंग भी) और दोपहर 2:00 बजे (रिकांगपिओ वाली बस, वाया सोरता) चलती हैं। बस अड्डे पर पुष्टि कर लें।')),
        (L(lang, 'How far is Karsog from Shimla?', 'शिमला से करसोग कितनी दूर है?'),
         L(lang, 'About 95 km by road from Shimla ISBT (Tutikandi) to Karsog bus stand, via Tattapani: about 4 hours by car. HRTC buses take about 5 to 5½ hours. '
                 '<a href="/distance/">Distances to other places</a>.',
           'शिमला आईएसबीटी (टूटीकंडी) से करसोग बस अड्डा सड़क से लगभग 95 किमी है, तत्तापानी होकर: गाड़ी से लगभग 4 घंटे। एचआरटीसी बस लगभग 5 से 5½ घंटे लेती है। '
           '<a href="/hi/distance/">दूसरी जगहों की दूरी</a>।')),
        (L(lang, 'What is the best time to visit Karsog?', 'करसोग घूमने का सबसे अच्छा समय कौन-सा है?'),
         L(lang, 'March to November. May brings the Mahunag Mela, and the apple season (September–October) is especially beautiful. '
                 'In winter (December–February) the higher roads can close for snow.',
           'मार्च से नवंबर। मई में माहूँनाग मेला लगता है और सेब का मौसम (सितंबर–अक्टूबर) ख़ास तौर पर सुंदर होता है। '
           'सर्दियों (दिसंबर–फ़रवरी) में ऊँची सड़कें बर्फ़ से बंद हो सकती हैं।')),
        (L(lang, 'Does it snow in Karsog?', 'क्या करसोग में बर्फ़ गिरती है?'),
         L(lang, 'Karsog town is at about 1,404 m, so snow in town is occasional and usually light, in the coldest weeks of winter. '
                 'Shikari Devi, Chindi and Janjehli get heavier snow and their roads can close. <a href="/weather/">Live weather and snow forecast</a>.',
           'करसोग शहर लगभग 1,404 मीटर की ऊँचाई पर है, इसलिए शहर में बर्फ़ कभी-कभार और हल्की गिरती है, सर्दी के सबसे ठंडे हफ़्तों में। '
           'शिकारी देवी, चिंडी और जंजैहली में ज़्यादा बर्फ़ गिरती है और वहाँ की सड़कें बंद हो सकती हैं। <a href="/hi/weather/">लाइव मौसम और बर्फ़ का पूर्वानुमान</a>।')),
        (L(lang, 'Are the roads safe in the monsoon?', 'क्या बरसात में सड़कें ठीक रहती हैं?'),
         L(lang, 'From July to September landslides and slow patches are common, especially on the Shimla–Tattapani side. '
                 'In heavy rain, check the weather page and call the Karsog Control Room (+91 93172-07043) before you set out.',
           'जुलाई से सितंबर तक भूस्खलन और धीमे रास्ते आम हैं, ख़ासकर शिमला–तत्तापानी वाली तरफ़। '
           'तेज़ बारिश में निकलने से पहले मौसम देखें और करसोग कंट्रोल रूम (+91 93172-07043) पर फ़ोन कर लें।')),
        (L(lang, 'Are there ATMs and petrol pumps in Karsog?', 'क्या करसोग में एटीएम और पेट्रोल पंप हैं?'),
         L(lang, 'Yes, Karsog town has bank branches, ATMs and a petrol pump. Carry cash for villages and treks (Shikari Devi, Kamru Nag), which have neither.',
           'हाँ, करसोग शहर में बैंक, एटीएम और पेट्रोल पंप हैं। गाँवों और ट्रेक (शिकारी देवी, कमरूनाग) के लिए नक़द साथ रखें, वहाँ ये सुविधाएँ नहीं हैं।')),
        (L(lang, 'Is there mobile network in Karsog?', 'क्या करसोग में मोबाइल नेटवर्क आता है?'),
         L(lang, 'Jio, Airtel and BSNL generally work in town. Signal is weak or missing on the Shikari Devi and Kamru Nag trails, so download offline maps first.',
           'शहर में जियो, एयरटेल और बीएसएनएल आम तौर पर चलते हैं। शिकारी देवी और कमरूनाग के रास्तों पर सिग्नल कमज़ोर या बिल्कुल नहीं होता, इसलिए पहले से ऑफ़लाइन मैप डाउनलोड कर लें।')),
        (L(lang, 'Where can I stay in Karsog?', 'करसोग में कहाँ ठहरें?'),
         L(lang, 'The HPTDC Hotel Mamleshwar at Chindi (about 7 km), small hotels in Karsog town, the PWD rest house and a few homestays. '
                 'Book ahead in apple season and during big fairs. <a href="/hotels/">Hotels in Karsog</a>.',
           'चिंडी में एचपीटीडीसी का होटल ममलेश्वर (लगभग 7 किमी), करसोग शहर में छोटे होटल, पीडब्ल्यूडी रेस्ट हाउस और कुछ होमस्टे। '
           'सेब के मौसम और बड़े मेलों में पहले से बुकिंग कर लें। <a href="/hi/hotels/">करसोग के होटल</a>।')),
    ]


def model(lang):
    hl = lambda p: p if lang == 'en' else ('/hi' + p if p != '/' else '/hi/')
    n_dep = len(HRTC) + len(P_DEP)
    # --- hero with the live strip
    now = (f'<div class="now" aria-label="{L(lang, "Right now in Karsog", "करसोग में अभी")}">'
           f'<a href="{hl("/weather/")}" id="now-w">{icon("sun")}<span><small>{L(lang, "Weather now", "अभी का मौसम")}</small>'
           f'<b>{L(lang, "Karsog town, 1,404 m", "करसोग शहर, 1,404 मी")}</b></span></a>'
           f'<a href="{hl("/karsog-bus-stand/")}" id="now-b">{icon("bus")}<span><small>{L(lang, "Next bus", "अगली बस")}</small>'
           f'<b>{L(lang, "See the timetable", "समय-सारणी देखें")}</b></span></a>'
           f'<a href="{hl("/melas/")}" id="now-m">{icon("party")}<span><small>{L(lang, "Fairs this month", "इस महीने के मेले")}</small>'
           f'<b>{L(lang, "Fair calendar", "मेलों का कैलेंडर")}</b></span></a></div>')
    # --- quick tiles
    tiles = ''.join(f'<a class="tile" href="{hl(u)}"><span class="i">{icon(ic)}</span><b>{L(lang, en, hi)}</b>'
                    f'<span>{L(lang, den, dhi)}</span></a>' for u, ic, en, hi, den, dhi in TILES)
    s_tiles = section(f'<div class="tiles rv">{tiles}</div>', 'sec-tight', 'start')
    # --- intro
    facts = [('1,404 m' if lang == 'en' else '1,404 मी', L(lang, 'Height of Karsog town', 'करसोग शहर की ऊँचाई')),
             ('94 km' if lang == 'en' else '94 किमी', L(lang, 'From Shimla by road', 'शिमला से, सड़क से')),
             ('99 km' if lang == 'en' else '99 किमी', L(lang, 'From Mandi by road', 'मंडी से, सड़क से')),
             ('534', L(lang, 'Villages in Karsog tehsil', 'करसोग तहसील के गाँव'))]
    fx = '<div class="facts">' + ''.join(f'<div><b>{v}</b><small>{k}</small></div>' for v, k in facts) + '</div>'
    intro = (f'<div class="intro"><div><span class="eyebrow">{L(lang, "About Karsog", "करसोग के बारे में")}</span>'
             f'<p class="statement">{L(lang, "A valley of old wooden temples, terraced fields and apple orchards in the south of Mandi district, where every village has its own <em>devta</em>.", "मंडी ज़िले के दक्षिण में लकड़ी और पत्थर के पुराने मंदिरों, सीढ़ीदार खेतों और सेब के बगीचों की घाटी, जहाँ हर गाँव का अपना <em>देवता</em> है।")}</p></div>'
             f'<div><p>{L(lang, "This guide is made in Karsog, by a local. Bus times are copied from the timetable board at the bus stand, fair dates are checked against past years, and every photo on the site was taken over the valley by drone.", "यह गाइड करसोग में, यहीं के एक निवासी ने बनाई है। बसों का समय बस अड्डे के टाइम-टेबल बोर्ड से लिया गया है, मेलों की तारीख़ें पिछले सालों से मिलाकर देखी गई हैं, और साइट की हर फ़ोटो घाटी के ऊपर ड्रोन से ली गई है।")}</p>'
             f'<p>{L(lang, "Things change in the hills. If something here is out of date, please", "पहाड़ों में चीज़ें बदलती रहती हैं। अगर यहाँ कुछ पुराना हो गया हो, तो कृपया")} '
             f'<a href="#update" data-open="upd">{L(lang, "tell us", "हमें बताएँ")}</a>.</p>{fx}</div></div>')
    s_intro = section(intro, 'sec-alt', 'about')
    # --- places bento
    cards = ''
    for i, (u, f, en, hi, men, mhi, ten, thi) in enumerate(PLACES_HOME):
        sizes = '(max-width:900px) 76vw, 600px' if i == 0 else '(max-width:900px) 76vw, 300px'
        cards += pcard(hl(u), pbase(f), L(lang, en, hi), L(lang, men, mhi), L(lang, ten, thi), sizes=sizes,
                       alt=L(lang, f'{en}, Karsog, from the air', f'{hi}, करसोग, ऊपर से'))
    s_places = section(shead(L(lang, 'Places to visit', 'घूमने की जगहें'),
                             L(lang, 'Temples, peaks and <em>hot springs</em>', 'मंदिर, चोटियाँ और <em>गर्म चश्मे</em>'),
                             L(lang, 'From a Shiva temple at the edge of town to a goddess on the highest peak of Mandi district. Every place has a full guide.',
                               'शहर के किनारे बने शिव मंदिर से लेकर मंडी ज़िले की सबसे ऊँची चोटी पर देवी के मंदिर तक। हर जगह की पूरी जानकारी।'),
                             more=(L(lang, 'All places to visit', 'सभी घूमने की जगहें'), hl('/places/')))
                       + f'<div class="bento rv">{cards}</div>', '', 'places')
    # --- buses + distances
    board = (f'<div class="nextbus" data-src="j-bd" data-n="6"><div class="h"><span class="pulse"></span>'
             f'{L(lang, "Next buses from Karsog", "करसोग से अगली बसें")}<span class="when"></span></div>'
             f'<ol><li><span class="tm">—</span><span class="to">{L(lang, "Loading…", "लोड हो रहा है…")}</span></li></ol>'
             f'<p class="f">{L(lang, "HRTC and private · times from the stand’s timetable board · confirm at the stand", "एचआरटीसी और प्राइवेट · समय बस अड्डे के बोर्ड से · निकलने से पहले पुष्टि कर लें")}</p></div>')
    btns = ''.join(f'<a class="btn {c}" href="{hl(u)}">{L(lang, en, hi)}</a>' for u, en, hi, c in [
        ('/karsog-bus-stand/', 'All buses from Karsog', 'करसोग से सभी बसें', 'btn-p'),
        ('/mandi-to-karsog-bus/', 'Mandi ⇄ Karsog', 'मंडी ⇄ करसोग', 'btn-o'),
        ('/shimla-to-karsog-bus/', 'Shimla ⇄ Karsog', 'शिमला ⇄ करसोग', 'btn-o'),
        ('/karsog-private-bus/', 'Private buses', 'प्राइवेट बसें', 'btn-o')])
    dl = ''.join(f'<li><b>{L(lang, en, hi)}</b><span><strong>{km}</strong> {L(lang, "km", "किमी")}</span></li>' for en, hi, km in DIST)
    s_bus = section(
        '<div class="split split-l"><div>' +
        shead(L(lang, 'Getting here', 'कैसे पहुँचें'), L(lang, 'Buses from <em>Karsog</em>', 'करसोग से <em>बसें</em>'),
              L(lang, f'{n_dep} departures a day from Karsog bus stand, HRTC and private. The next ones, by the time in India right now:',
                f'करसोग बस अड्डे से रोज़ {n_dep} बसें, एचआरटीसी और प्राइवेट। अभी के समय के हिसाब से अगली बसें:')) +
        board + f'<div class="btns">{btns}</div></div>'
        f'<div><h3>{L(lang, "How far is Karsog?", "करसोग कितनी दूर है?")}</h3>'
        f'<p class="mt0">{L(lang, "By road, from Karsog bus stand.", "करसोग बस अड्डे से, सड़क के रास्ते।")}</p><ul class="dlist">{dl}</ul>'
        f'<p class="mt1"><a class="more-link" href="{hl("/distance/")}">{L(lang, "All distances", "सभी दूरियाँ")} {icon("arrow")}</a></p></div></div>',
        'sec-alt', 'buses')
    # --- melas year strip
    cells = ''
    for mi in range(1, 13):
        fs = [x for x in MELAS if x['m'] == mi]
        if not fs:
            continue
        first, rest = fs[0], fs[1:]
        more = (' + ' + ', '.join(L(lang, x['en'], x['hi']) for x in rest)) if rest else L(lang, first['place'], first['place_hi'])
        cells += (f'<a class="mo" href="{hl("/melas/")}#m{mi}" data-m="{mi}"><small>{L(lang, MON_EN[mi - 1], MON_HI[mi - 1])}</small>'
                  f'<b>{L(lang, first["en"], first["hi"])}</b><span>{more}</span></a>')
    s_melas = section(shead(L(lang, 'Melas & festivals', 'मेले और त्योहार'), L(lang, 'A year of <em>fairs</em>', 'पूरे साल <em>मेले</em>'),
                            L(lang, 'Every village has its devta, and every devta has a fair. These are the big ones; this month is marked.',
                              'हर गाँव का अपना देवता है और हर देवता का अपना मेला। ये हैं बड़े मेले; इस महीने वाला अलग रंग में है।'),
                            more=(L(lang, 'Dates and details', 'तारीख़ें और पूरी जानकारी'), hl('/melas/')))
                      + f'<div class="yr rv">{cells}</div>', '', 'melas')
    # --- from the air
    ms = ''
    for f in MOSAIC:
        p = next(x for x in PHOTOS if x['file'] == f)
        title = place_title(p['slug'], lang)
        ms += (f'<a href="{hl("/" + p["slug"] + "/")}">{img(pbase(f), L(lang, f"{title}, Karsog, from the air", f"{title}, करसोग, ऊपर से"), "(max-width:900px) 50vw, 25vw")}'
               f'<span>{esc(title)}</span></a>')
    s_air = section(shead(L(lang, 'From the air', 'आसमान से'),
                          L(lang, f'{len(PHOTOS)} drone photos of <em>{len(PLACES)} places</em>', f'{len(PLACES)} जगहों की <em>{len(PHOTOS)} ड्रोन फ़ोटो</em>'),
                          L(lang, 'Villages, temples and valleys of Karsog, photographed from above by Karsog Miles.',
                            'करसोग के गाँव, मंदिर और घाटियाँ, ऊपर से, Karsog Miles की ड्रोन फ़ोटो में।'),
                          more=(L(lang, 'See all photos', 'सभी फ़ोटो देखें'), hl('/photos/'))) + f'<div class="mosaic rv">{ms}</div>',
                    'sec-alt', 'photos')
    # --- emergency
    dial = ''.join(f'<a href="{tel(n)}"><b>{n}</b><span>{L(lang, en, hi)}</span></a>' for n, en, hi in DIAL)
    s_sos = section(shead(L(lang, 'Keep these handy', 'ये नंबर सेव रखें'), L(lang, 'Emergency <em>numbers</em>', 'आपातकालीन <em>नंबर</em>'),
                          L(lang, 'Tap to call. Mountain weather and roads can change quickly.', 'छूकर सीधे कॉल करें। पहाड़ों में मौसम और सड़कें जल्दी बदल जाती हैं।'),
                          more=(L(lang, 'All useful numbers', 'सभी ज़रूरी नंबर'), hl('/contacts/'))) + f'<div class="dial">{dial}</div>',
                    'sec-dark', 'emergency')
    fq = faqs(lang)
    body = s_tiles + s_intro + s_places + s_bus + s_melas + s_air + s_sos + faq_block(fq, lang, L(lang, 'Questions travellers <em>ask</em>', 'यात्रियों के <em>सवाल</em>'))
    ld = [{'@context': 'https://schema.org', '@type': 'WebSite', 'name': 'karsog.com', 'alternateName': ['Karsog', 'करसोग'],
           'url': 'https://karsog.com/', 'inLanguage': ['en-IN', 'hi-IN']},
          {'@context': 'https://schema.org', '@type': 'TouristDestination', 'name': L(lang, 'Karsog', 'करसोग'),
           'description': L(lang, 'Karsog valley in Mandi district, Himachal Pradesh: temples, fairs, apple orchards and treks.',
                            'करसोग घाटी, ज़िला मंडी, हिमाचल प्रदेश: मंदिर, मेले, सेब के बगीचे और ट्रेक।'),
           'geo': {'@type': 'GeoCoordinates', 'latitude': 31.383, 'longitude': 77.2},
           'containedInPlace': {'@type': 'AdministrativeArea', 'name': 'Mandi, Himachal Pradesh, India'}, 'url': 'https://karsog.com/'},
          faq_ld(fq)]
    return dict(
        path='/', lang=lang, kind='home', hero='home',
        title=L(lang, 'Karsog Valley Guide — Buses, Weather, Temples & Melas', 'करसोग घाटी गाइड — बसों का समय, मौसम, मंदिर और मेले'),
        desc=L(lang, 'Plan a trip to Karsog, Mandi (HP): live bus timings from Karsog bus stand, weather and snow, temples, fair dates, hotels and emergency numbers.',
               'करसोग (मंडी, हिमाचल) की पूरी जानकारी: करसोग बस अड्डे से बसों का समय, मौसम और बर्फ़, मंदिर, मेलों की तारीख़ें, होटल और ज़रूरी नंबर।'),
        kicker=f'{icon("pin")} ' + L(lang, 'Mandi district · Himachal Pradesh', 'ज़िला मंडी · हिमाचल प्रदेश'),
        h1=L(lang, 'Karsog <em>valley</em>', 'करसोग <em>घाटी</em>'),
        lede=L(lang, 'Ancient temples, apple orchards and deodar forests in the hills of Mandi, and everything you need for the trip: bus timings, weather, fairs and local numbers.',
               'मंडी की पहाड़ियों में प्राचीन मंदिर, सेब के बगीचे और देवदार के जंगल। और सफ़र की हर ज़रूरी जानकारी: बसों का समय, मौसम, मेले और ज़रूरी नंबर।'),
        img={'src': pbase('nyara-004'), 'alt': L(lang, 'Terraced green fields and a river at Sanarli, Karsog valley, from the air',
                                                   'सनारली, करसोग घाटी: सीढ़ीदार हरे खेत और नदी, ऊपर से'), 'pos': '45% 60%'},
        actions=[(L(lang, 'Bus timings', 'बसों का समय'), hl('/karsog-bus-stand/'), 'g', 'bus'),
                 (L(lang, 'Places to visit', 'घूमने की जगहें'), hl('/places/'), 'w', 'pin')],
        hero_extra=now, body=body, ld=ld, og='/og/home.jpg',
        data={'j-bd': next_bus_json(), 'j-melas': melas_json()})
