"""Places to visit (/places/), plan a trip (/plan/) and useful numbers (/contacts/).

Only facts already checked elsewhere on the site are used here: distances from DIST in data.py (Google Maps,
28 Sep 2026), taxi fares and day plans as written in the guides, and the contact list from the old /contacts/ page
("Karsog at a glance" checked 27 Sep 2026)."""
from layout import L, icon, section, shead, faq_block, faq_ld, comments, note, esc, href
from data import DIST, DIST_CHECKED, DIST_CHECKED_HI, GUIDES
from p_guide import guide_card

ORDER = ['mahunag', 'shikari-devi', 'mamleshwar', 'kao', 'kamru-nag', 'tattapani', 'pangna-fort', 'chindi', 'janjehli']


def km(name):
    return next(x for x in DIST if x[0] == name)


def jump(lang, items):
    return '<div class="jump">' + ''.join(f'<a href="#{k}">{L(lang, en, hi)}</a>' for k, en, hi in items) + '</div>'


# ---------------------------------------------------------------- /places/
def places(lang):
    hl = lambda p: href(p, lang)
    cards = ''.join(guide_card(n, lang) for n in ORDER)
    grid = section(shead(L(lang, 'Full guides', 'पूरी गाइड'), L(lang, 'Temples, peaks and <em>hot springs</em>', 'मंदिर, चोटियाँ और <em>गर्म चश्मे</em>'),
                         L(lang, 'Each place has its own page: how to get there, when to go, the stories behind it and drone photos.',
                           'हर जगह का अपना पेज है: कैसे पहुँचें, कब जाएँ, उससे जुड़ी कथाएँ और ड्रोन फ़ोटो।'))
                   + f'<div class="grid g3">{cards}</div>', '', 'guides')
    more = section('<div class="grid g3">'
                   + f'<a class="card icard" href="{hl("/temples/")}"><span class="i">{icon("temple")}</span><span><b>{L(lang, "Temples of Karsog", "करसोग के मंदिर")}</b>'
                     f'<span>{L(lang, "Ten temples, the story behind each and when to go", "दस मंदिर, हर एक की कथा और कब जाएँ")}</span></span></a>'
                   + f'<a class="card icard" href="{hl("/melas/")}"><span class="i">{icon("party")}</span><span><b>{L(lang, "Melas &amp; festivals", "मेले और त्योहार")}</b>'
                     f'<span>{L(lang, "Every big fair, month by month", "हर बड़ा मेला, महीने के हिसाब से")}</span></span></a>'
                   + f'<a class="card icard" href="{hl("/photos/")}"><span class="i">{icon("camera")}</span><span><b>{L(lang, "Villages from the air", "आसमान से गाँव")}</b>'
                     f'<span>{L(lang, "Drone photos of 27 places around Karsog", "करसोग के आसपास की 27 जगहों की ड्रोन फ़ोटो")}</span></span></a>'
                   + '</div>', 'sec-alt', 'more')
    plan = section(shead(L(lang, 'Planning', 'योजना'), L(lang, 'Put it <em>together</em>', 'सफ़र की <em>तैयारी</em>'),
                         L(lang, 'Distances, buses, day plans, hotels and the weather in one place.', 'दूरी, बसें, एक दिन की योजनाएँ, होटल और मौसम, एक ही जगह।'))
                   + '<div class="btns">'
                   + f'<a class="btn btn-p" href="{hl("/plan/")}">{icon("compass")}{L(lang, "Plan a trip", "यात्रा योजना")}</a>'
                   + f'<a class="btn btn-o" href="{hl("/distance/")}">{icon("ruler")}{L(lang, "Distances", "दूरी")}</a>'
                   + f'<a class="btn btn-o" href="{hl("/karsog-bus-stand/")}">{icon("bus")}{L(lang, "Bus timings", "बसों का समय")}</a>'
                   + f'<a class="btn btn-o" href="{hl("/weather/")}">{icon("weather")}{L(lang, "Weather", "मौसम")}</a></div>', 'sec-tight', 'plan')
    fq = [(L(lang, 'What are the best places to visit in Karsog?', 'करसोग में घूमने की सबसे अच्छी जगहें कौन-सी हैं?'),
           L(lang, 'The Mahunag temple, Shikari Devi on the highest peak of Mandi district, Mamleshwar Mahadev at Mamel, Kamaksha Devi at Kao, the Kamru Nag lake trek, '
                   'the Tattapani hot springs, Pangna fort, Chindi and the Janjehli valley. Each has a full guide on this site.',
             'माहूँनाग मंदिर, मंडी ज़िले की सबसे ऊँची चोटी पर शिकारी देवी, ममेल में ममलेश्वर महादेव, काओ में कामाक्षा देवी, कमरूनाग झील का ट्रेक, '
             'तत्तापानी के गर्म चश्मे, पांगणा क़िला, चिंडी और जंजैहली घाटी। हर जगह की पूरी गाइड इस साइट पर है।')),
          (L(lang, 'Which places near Karsog can I see in one day?', 'करसोग के पास एक दिन में कौन-सी जगहें देख सकते हैं?'),
           L(lang, 'Mamleshwar Mahadev, Kamaksha Devi at Kao and Mahunag make a one-day temple circuit. Chindi and Tattapani also fit in a day. '
                   'Shikari Devi and Janjehli are best with a night in Janjehli.',
             'ममलेश्वर महादेव, काओ में कामाक्षा देवी और माहूँनाग एक दिन के मंदिर-सफ़र में देखे जा सकते हैं। चिंडी और तत्तापानी भी एक दिन में हो जाते हैं। '
             'शिकारी देवी और जंजैहली के लिए जंजैहली में एक रात रुकना सबसे अच्छा है।'))]
    return dict(path='/places/', lang=lang, kind='page', hero='band',
                title=L(lang, 'Places to Visit in Karsog — Temples, Treks, Forts & Hot Springs', 'करसोग में घूमने की जगहें — मंदिर, ट्रेक, क़िले और गर्म चश्मे'),
                desc=L(lang, 'Places to visit around Karsog: Mahunag, Shikari Devi, Mamleshwar Mahadev, Kamaksha Devi, Kamru Nag, Tattapani, Pangna, Chindi and Janjehli, with a full guide for each.',
                       'करसोग के आसपास घूमने की जगहें: माहूँनाग, शिकारी देवी, ममलेश्वर महादेव, कामाक्षा देवी, कमरूनाग, तत्तापानी, पांगणा, चिंडी और जंजैहली, हर एक की पूरी गाइड के साथ।'),
                kicker=L(lang, 'What to see', 'क्या देखें'), h1=L(lang, 'Places to <em>visit</em>', 'घूमने की <em>जगहें</em>'),
                lede=L(lang, 'Temples, treks, forts and hot springs in and around the Karsog valley, with a full guide for each.',
                       'करसोग घाटी और आसपास के मंदिर, ट्रेक, क़िले और गर्म चश्मे, हर एक की पूरी गाइड के साथ।'),
                chips=[('pin', L(lang, f'{len(ORDER)} full guides', f'{len(ORDER)} पूरी गाइड')), ('camera', L(lang, 'Drone photos of each', 'हर जगह की ड्रोन फ़ोटो'))],
                crumbs=[(L(lang, 'Places', 'घूमने की जगहें'), '/places/')],
                body=grid + more + plan + faq_block(fq, lang), ld=[faq_ld(fq)])


# ---------------------------------------------------------------- /plan/
def plan(lang):
    hl = lambda p: href(p, lang)
    sh, md, ch, dl, bh = km('Shimla (ISBT Tutikandi)'), km('Mandi'), km('Chandigarh (ISBT Sector 43)'), km('Delhi (Kashmere Gate ISBT)'), km('Bhuntar airport (Kullu)')
    card = lambda ic, t, txt, u=None, lk=None: (f'<div class="card icard"><span class="i">{icon(ic)}</span><span><b>{t}</b><span>{txt}'
                                             + (f' <a href="{hl(u)}">{lk}</a>' if u else '') + '</span></span></div>')
    reach = section(shead(L(lang, 'Getting here', 'कैसे पहुँचें'), L(lang, 'How to reach <em>Karsog</em>', 'करसोग <em>कैसे पहुँचें</em>'),
                          L(lang, f'Road distances from Karsog bus stand by the fastest route on Google Maps, checked on {DIST_CHECKED}. Hill roads are slow; buses take longer than cars.',
                            f'करसोग बस अड्डे से, गूगल मैप्स के सबसे तेज़ रास्ते से, {DIST_CHECKED_HI} को देखी गई दूरी। पहाड़ी सड़कों पर समय ज़्यादा लगता है; बसें कार से ज़्यादा समय लेती हैं।'))
                    + '<div class="grid g2">'
                    + card('bus', L(lang, 'From Shimla', 'शिमला से'),
                           L(lang, f'About {sh[2]:g} km from ISBT Tutikandi via Tattapani, around {sh[3]} by car. HRTC buses take about 5 to 5½ hours.',
                             f'आईएसबीटी टूटीकंडी से तत्तापानी होकर लगभग {sh[2]:g} किमी, कार से लगभग {sh[4]}। एचआरटीसी बसें लगभग 5 से 5½ घंटे लेती हैं।'),
                           '/shimla-to-karsog-bus/', L(lang, 'Shimla ⇄ Karsog buses', 'शिमला ⇄ करसोग बसें'))
                    + card('bus', L(lang, 'From Mandi', 'मंडी से'),
                           L(lang, f'About {md[2]:g} km, around {md[3]} by car.', f'लगभग {md[2]:g} किमी, कार से लगभग {md[4]}।'),
                           '/mandi-to-karsog-bus/', L(lang, 'Mandi ⇄ Karsog buses', 'मंडी ⇄ करसोग बसें'))
                    + card('car', L(lang, 'From Chandigarh and Delhi', 'चंडीगढ़ और दिल्ली से'),
                           L(lang, f'About {ch[2]:g} km from Chandigarh (ISBT Sector 43), around {ch[3]} by car; about {dl[2]:g} km from Delhi (Kashmere Gate ISBT), around {dl[3]}.',
                             f'चंडीगढ़ (आईएसबीटी सेक्टर 43) से लगभग {ch[2]:g} किमी, कार से लगभग {ch[4]}; दिल्ली (कश्मीरी गेट आईएसबीटी) से लगभग {dl[2]:g} किमी, लगभग {dl[4]}।'),
                           '/bus/karsog-to-delhi/', L(lang, 'Karsog ⇄ Delhi bus', 'करसोग ⇄ दिल्ली बस'))
                    + card('plane', L(lang, 'Nearest airport', 'सबसे पास का हवाई अड्डा'),
                           L(lang, f'Bhuntar (Kullu), about {bh[2]:g} km, around {bh[3]} by car.', f'भुंतर (कुल्लू), लगभग {bh[2]:g} किमी, कार से लगभग {bh[4]}।'),
                           '/distance/', L(lang, 'All distances', 'सभी दूरियाँ'))
                    + '</div>', '', 'reach')
    around = section(shead(L(lang, 'Getting around', 'आसपास घूमना'), L(lang, 'Taxis and <em>local buses</em>', 'टैक्सी और <em>स्थानीय बसें</em>'))
                     + '<div class="grid g2">'
                     + card('car', L(lang, 'Taxis', 'टैक्सी'),
                            L(lang, 'Taxis wait at the Karsog taxi stand in the main market. Short local trips cost about ₹250 an hour, including the first 10 km. Agree the fare before you start.',
                              'करसोग के मुख्य बाज़ार में टैक्सी स्टैंड पर टैक्सियाँ मिलती हैं। छोटे स्थानीय सफ़र का किराया लगभग ₹250 प्रति घंटा है, जिसमें पहले 10 किमी शामिल हैं। चलने से पहले किराया तय कर लें।'))
                     + card('bus', L(lang, 'Buses to the villages', 'गाँवों की बसें'),
                            L(lang, 'HRTC and private buses leave Karsog bus stand for many villages of the valley, and for Shimla, Mandi and beyond.',
                              'करसोग बस अड्डे से घाटी के कई गाँवों के लिए, और शिमला, मंडी व आगे के लिए एचआरटीसी और प्राइवेट बसें चलती हैं।'),
                            '/karsog-bus-stand/', L(lang, 'Every departure', 'सभी बसें'))
                     + '</div>', 'sec-alt', 'around')
    days = [('temple', L(lang, 'Temple day', 'मंदिरों का एक दिन'),
             L(lang, 'Mamleshwar Mahadev in the morning, then Kamaksha Devi at Kao, then Mahunag, back in Karsog by evening. A full day in a Dzire costs about ₹1,500–2,500.',
               'सुबह ममलेश्वर महादेव, फिर काओ में कामाक्षा देवी, फिर माहूँनाग, और शाम तक करसोग वापस। डिज़ायर गाड़ी से पूरे दिन का ख़र्च लगभग ₹1,500–2,500 आता है।'),
             [('/mamleshwar/', 'Mamleshwar', 'ममलेश्वर'), ('/kao/', 'Kao', 'काओ'), ('/mahunag/', 'Mahunag', 'माहूँनाग')]),
            ('sun', L(lang, 'Hot springs and orchards', 'गर्म चश्मे और बगीचे'),
             L(lang, 'Tattapani’s hot springs on the Sutlej (46 km) and the orchards and sunset views of Chindi on the way. Best from October to March.',
               'सतलुज किनारे तत्तापानी के गर्म चश्मे (46 किमी) और रास्ते में चिंडी के बगीचे और सूर्यास्त के नज़ारे। अक्टूबर से मार्च सबसे अच्छा।'),
             [('/tattapani/', 'Tattapani', 'तत्तापानी'), ('/chindi/', 'Chindi', 'चिंडी')]),
            ('mountain', L(lang, 'Shikari Devi and Janjehli', 'शिकारी देवी और जंजैहली'),
             L(lang, 'Over the Shikari Devi road to Janjehli (27 km, open about April to November), a night there, and the temple at first light, when the views are clearest.',
               'शिकारी देवी वाली सड़क से जंजैहली (27 किमी, लगभग अप्रैल से नवंबर तक खुली), वहाँ एक रात, और सुबह पहली रोशनी में मंदिर, जब नज़ारे सबसे साफ़ होते हैं।'),
             [('/shikari-devi/', 'Shikari Devi', 'शिकारी देवी'), ('/janjehli/', 'Janjehli', 'जंजैहली')]),
            ('footprints', L(lang, 'Kamru Nag trek', 'कमरूनाग ट्रेक'),
             L(lang, 'Drive to Rohanda (52 km), then a 6 km forest trail to the sacred lake: 3–4 hours up, about 2 down. Start early.',
               'रोहांडा तक गाड़ी से (52 किमी), फिर जंगल का 6 किमी का पैदल रास्ता पवित्र झील तक: चढ़ने में 3–4 घंटे, उतरने में लगभग 2 घंटे। जल्दी निकलें।'),
             [('/kamru-nag/', 'Kamru Nag', 'कमरूनाग')])]
    dcards = ''
    for ic, t, txt, links in days:
        lk = ' · '.join(f'<a href="{hl(u)}">{L(lang, en, hi)}</a>' for u, en, hi in links)
        dcards += f'<div class="card icard"><span class="i">{icon(ic)}</span><span><b>{t}</b><span>{txt}</span><span class="mt0">{lk}</span></span></div>'
    s_days = section(shead(L(lang, 'Ready-made days', 'एक दिन की योजनाएँ'), L(lang, 'Day <em>plans</em>', 'घूमने की <em>योजनाएँ</em>'),
                           L(lang, 'Simple plans using local taxis, from the guides on this site. Fares are indicative; agree them before you start.',
                             'स्थानीय टैक्सी से आसान योजनाएँ, इस साइट की गाइड से। किराया अनुमानित है; चलने से पहले तय कर लें।'))
                     + f'<div class="grid g2">{dcards}</div>', '', 'days')
    stay = section(shead(L(lang, 'Where to stay', 'कहाँ ठहरें'), L(lang, 'Hotels and <em>homestays</em>', 'होटल और <em>होमस्टे</em>'),
                         L(lang, 'Simple family-run hotels in Karsog town, the HPTDC Hotel Mamleshwar at Chindi (about 7 km), a PWD rest house and a few homestays. Book ahead in apple season and during big fairs.',
                           'करसोग शहर में परिवारों के चलाए सादे होटल, चिंडी में एचपीटीडीसी होटल ममलेश्वर (लगभग 7 किमी), एक पीडब्ल्यूडी रेस्ट हाउस और कुछ होमस्टे। सेब के मौसम और बड़े मेलों में पहले से बुकिंग कर लें।'),
                         more=(L(lang, 'All hotels, with maps', 'सभी होटल, नक्शे के साथ'), hl('/hotels/'))), 'sec-alt', 'stay')
    when = section(shead(L(lang, 'When to go', 'कब जाएँ'), L(lang, 'The best <em>season</em>', 'सबसे अच्छा <em>मौसम</em>'),
                         L(lang, 'March to November. May brings the Mahunag Mela, and the apple season (September–October) is especially beautiful. In winter (December–February) the higher roads can close for snow; July to September brings monsoon landslides.',
                           'मार्च से नवंबर। मई में माहूँनाग मेला लगता है और सेब का मौसम (सितंबर–अक्टूबर) ख़ास तौर पर सुंदर होता है। सर्दियों (दिसंबर–फ़रवरी) में ऊँची सड़कें बर्फ़ से बंद हो सकती हैं; जुलाई से सितंबर तक बरसात में भूस्खलन होते हैं।'))
                   + '<div class="btns">'
                   + f'<a class="btn btn-p" href="{hl("/weather/")}">{icon("weather")}{L(lang, "Live weather", "लाइव मौसम")}</a>'
                   + f'<a class="btn btn-o" href="{hl("/melas/")}">{icon("party")}{L(lang, "Fair calendar", "मेलों का कैलेंडर")}</a></div>', '', 'when')
    fq = [(L(lang, 'How do I reach Karsog?', 'करसोग कैसे पहुँचें?'),
           L(lang, f'By road. Karsog is about {sh[2]:g} km from Shimla via Tattapani and about {md[2]:g} km from Mandi, with HRTC and private buses from both. The nearest airport is Bhuntar (Kullu), about {bh[2]:g} km away.',
             f'सड़क से। करसोग शिमला से तत्तापानी होकर लगभग {sh[2]:g} किमी और मंडी से लगभग {md[2]:g} किमी है, और दोनों जगहों से एचआरटीसी और प्राइवेट बसें आती हैं। सबसे पास का हवाई अड्डा भुंतर (कुल्लू) है, लगभग {bh[2]:g} किमी दूर।')),
          (L(lang, 'What is the best time to visit Karsog?', 'करसोग घूमने का सबसे अच्छा समय कौन-सा है?'),
           L(lang, 'March to November. May brings the Mahunag Mela, and the apple season (September–October) is especially beautiful. In winter the higher roads can close for snow.',
             'मार्च से नवंबर। मई में माहूँनाग मेला लगता है और सेब का मौसम (सितंबर–अक्टूबर) ख़ास तौर पर सुंदर होता है। सर्दियों में ऊँची सड़कें बर्फ़ से बंद हो सकती हैं।')),
          (L(lang, 'How much does a taxi cost in Karsog?', 'करसोग में टैक्सी का किराया कितना है?'),
           L(lang, 'Short local trips cost about ₹250 an hour, including the first 10 km. A full day of temple visits in a Dzire costs about ₹1,500–2,500. Agree the fare before you start.',
             'छोटे स्थानीय सफ़र का किराया लगभग ₹250 प्रति घंटा है, जिसमें पहले 10 किमी शामिल हैं। डिज़ायर गाड़ी से मंदिरों के पूरे दिन का ख़र्च लगभग ₹1,500–2,500 आता है। चलने से पहले किराया तय कर लें।'))]
    return dict(path='/plan/', lang=lang, kind='page', hero='band',
                title=L(lang, 'Plan a Karsog Trip — How to Reach, Taxis, Day Plans & Stay', 'करसोग यात्रा योजना — कैसे पहुँचें, टैक्सी, एक दिन की योजनाएँ, ठहरना'),
                desc=L(lang, f'Plan a Karsog trip: getting there from Shimla ({sh[2]:g} km) or Mandi ({md[2]:g} km), taxis, day plans for temples, Tattapani, Shikari Devi and Kamru Nag, hotels, best season.',
                       f'करसोग यात्रा की योजना: शिमला ({sh[2]:g} किमी) या मंडी ({md[2]:g} किमी) से कैसे पहुँचें, टैक्सी, मंदिरों, तत्तापानी, शिकारी देवी और कमरूनाग के लिए एक दिन की योजनाएँ, होटल, सही मौसम।'),
                kicker=L(lang, 'Plan a trip', 'यात्रा योजना'), h1=L(lang, 'Plan a Karsog <em>trip</em>', 'करसोग यात्रा की <em>योजना</em>'),
                lede=L(lang, 'Getting here, getting around, where to stay and when the valley celebrates.',
                       'कैसे पहुँचें, आसपास कैसे घूमें, कहाँ ठहरें और घाटी में कब उत्सव होते हैं।'),
                hero_extra=jump(lang, [('reach', 'How to reach', 'कैसे पहुँचें'), ('around', 'Taxis & buses', 'टैक्सी और बसें'), ('days', 'Day plans', 'योजनाएँ'),
                                       ('stay', 'Where to stay', 'कहाँ ठहरें'), ('when', 'When to go', 'कब जाएँ')]),
                crumbs=[(L(lang, 'Plan a trip', 'यात्रा योजना'), '/plan/')],
                body=reach + around + s_days + stay + when + comments('plan', lang) + faq_block(fq, lang), ld=[faq_ld(fq)])


# ---------------------------------------------------------------- /contacts/
EMERGENCY = [('112', 'National emergency', 'राष्ट्रीय आपातकाल'), ('100', 'Police', 'पुलिस'), ('101', 'Fire', 'फ़ायर ब्रिगेड'),
             ('108', 'Ambulance', 'एम्बुलेंस'), ('1091', 'Women helpline', 'महिला हेल्पलाइन'), ('1098', 'Child helpline', 'चाइल्ड हेल्पलाइन'),
             ('104', 'Medical helpline', 'चिकित्सा हेल्पलाइन'), ('1077', 'Disaster / flood', 'आपदा / बाढ़'), ('1912', 'Power fault', 'बिजली की शिकायत'),
             ('01907-222218', 'Civil Hospital Karsog', 'सिविल अस्पताल करसोग'), ('01907-222221', 'Police Station Karsog', 'पुलिस थाना करसोग'),
             ('+91 93172-07043', 'Karsog Control Room', 'करसोग कंट्रोल रूम')]
GLANCE = [('PIN code (Karsog post office)', 'पिन कोड (करसोग डाकघर)', '175011', '175011'), ('STD / phone code', 'एसटीडी / फ़ोन कोड', '01907', '01907'),
          ('Vehicle registration', 'गाड़ियों का नंबर', 'HP-30', 'HP-30'), ('District', 'ज़िला', 'Mandi, Himachal Pradesh', 'मंडी, हिमाचल प्रदेश'),
          ('Assembly constituency', 'विधानसभा क्षेत्र', '26 Karsog (SC)', '26 करसोग (अनुसूचित जाति)'),
          ('MLA', 'विधायक', 'Deep Raj (BJP), elected 2022', 'दीप राज (भाजपा), 2022 में चुने गए'),
          ('Lok Sabha constituency', 'लोकसभा क्षेत्र', 'Mandi', 'मंडी'),
          ('Karsog tehsil', 'करसोग तहसील', '534 villages, population 93,126 (Census 2011)', '534 गाँव, आबादी 93,126 (जनगणना 2011)'),
          ('Height of Karsog town', 'करसोग शहर की ऊँचाई', 'about 1,404 m', 'लगभग 1,404 मीटर')]
BANKS = [('State Bank of India, Karsog', 'भारतीय स्टेट बैंक, करसोग', 'SBIN0011884'), ('Punjab National Bank, Karsog', 'पंजाब नेशनल बैंक, करसोग', 'PUNB0074300'),
         ('HDFC Bank, Karsog', 'एचडीएफ़सी बैंक, करसोग', 'HDFC0008106')]
# (English, Hindi, value, kind) kind: tel | mail | web | text
OFFICES = [
    ('users', 'Administrative offices', 'प्रशासनिक दफ़्तर', [
        ('SDM Office Karsog', 'एसडीएम दफ़्तर करसोग', '01907-222236', 'tel'), ('SDM email', 'एसडीएम ईमेल', 'sdmksg-man-hp@nic.in', 'mail'),
        ('Tehsildar Karsog', 'तहसीलदार करसोग', '01907-222228', 'tel'), ('Tehsildar email', 'तहसीलदार ईमेल', 'tdrmanksg@gmail.com', 'mail'),
        ('BDO Office', 'बीडीओ दफ़्तर', '01907-222222', 'tel'), ('BDO email', 'बीडीओ ईमेल', 'bdomanksg@gmail.com', 'mail'),
        ('DC Office Mandi', 'डीसी दफ़्तर मंडी', '01905-225201', 'tel'),
        ('Police Post Pangna', 'पुलिस चौकी पांगणा', '01907-225026', 'tel'), ('Police Post Nihri', 'पुलिस चौकी निहरी', '01907-233680', 'tel')]),
    ('hospital', 'Health & medical', 'स्वास्थ्य और इलाज', [
        ('Civil Hospital Karsog', 'सिविल अस्पताल करसोग', '01907-222218', 'tel'), ('Civil Hospital Janjehli', 'सिविल अस्पताल जंजैहली', '01907-256512', 'tel'),
        ('Civil Hospital Gohar', 'सिविल अस्पताल गोहर', '01907-250292', 'tel'),
        ('Himalaya Healthcare Dialysis', 'हिमालय हेल्थकेयर डायलिसिस', ('Sanarali Chowk · 24/7', 'सनारली चौक · 24 घंटे'), 'text'),
        ('Ultracare Radiodiagnostic', 'अल्ट्राकेयर रेडियोडायग्नोस्टिक', ('Near DFO Office', 'डीएफ़ओ दफ़्तर के पास'), 'text'),
        ('Ambulance (national)', 'एम्बुलेंस (राष्ट्रीय)', '108', 'tel'), ('Maternal health (JSSK)', 'मातृ स्वास्थ्य (जेएसएसके)', '102', 'tel'),
        ('Medical helpline', 'चिकित्सा हेल्पलाइन', '104', 'tel')]),
    ('shield', 'Police & safety', 'पुलिस और सुरक्षा', [
        ('Police Station Karsog', 'पुलिस थाना करसोग', '01907-222221', 'tel'), ('Karsog Control Room', 'करसोग कंट्रोल रूम', '+91 93172-07043', 'tel'),
        ('Police (national)', 'पुलिस (राष्ट्रीय)', '100', 'tel'), ('National emergency', 'राष्ट्रीय आपातकाल', '112', 'tel'),
        ('Women helpline', 'महिला हेल्पलाइन', '1091', 'tel'), ('Child helpline', 'चाइल्ड हेल्पलाइन', '1098', 'tel'), ('Fire', 'फ़ायर ब्रिगेड', '101', 'tel'),
        ('Flood / disaster', 'बाढ़ / आपदा', '1077', 'tel'), ('Power fault (HPSEBL)', 'बिजली की शिकायत (एचपीएसईबीएल)', '1912', 'tel')]),
]


def tel(n):
    return 'tel:' + n.replace(' ', '').replace('-', '')


def contacts(lang):
    hl = lambda p: href(p, lang)
    dial = ''.join(f'<a href="{tel(n)}"><b>{n}</b><span>{L(lang, en, hi)}</span></a>' for n, en, hi in EMERGENCY)
    s_sos = section(shead(L(lang, 'Emergency', 'आपातकाल'), L(lang, 'Save these <em>before you travel</em>', 'सफ़र से पहले ये <em>नंबर सेव करें</em>'),
                          L(lang, 'Tap to call. Mountain weather and roads can change without notice.', 'छूकर सीधे कॉल करें। पहाड़ों में मौसम और सड़कें बिना बताए बदल सकती हैं।'))
                    + f'<div class="dial">{dial}</div>', 'sec-dark', 'emergency')
    kv = lambda rows: '<dl class="kv">' + ''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in rows) + '</dl>'
    g_rows = [(esc(L(lang, en, hi)), esc(L(lang, ve, vh))) for en, hi, ve, vh in GLANCE]
    b_rows = [(esc(L(lang, en, hi)), code) for en, hi, code in BANKS] + [
        (L(lang, 'Check any IFSC', 'कोई भी IFSC जाँचें'), f'<a href="https://www.rbi.org.in/Scripts/IFSCMICRDetails.aspx" target="_blank" rel="noopener">{L(lang, "RBI list", "आरबीआई सूची")} {icon("ext")}</a>')]
    e_rows = [(L(lang, 'Government College Karsog', 'राजकीय महाविद्यालय करसोग'), f'<a href="tel:01907222116">01907-222116</a>'),
              (L(lang, 'College email', 'कॉलेज ईमेल'), '<a href="mailto:gckarsog-hp@nic.in">gckarsog-hp@nic.in</a>'),
              (L(lang, 'College website', 'कॉलेज वेबसाइट'), f'<a href="https://www.gckarsog.edu.in/" target="_blank" rel="noopener">gckarsog.edu.in {icon("ext")}</a>')]
    s_glance = section(shead(L(lang, 'Codes &amp; facts', 'कोड और जानकारी'), L(lang, 'Karsog at a <em>glance</em>', 'करसोग <em>एक नज़र में</em>'))
                       + '<div class="grid g3">'
                       + f'<div class="card"><h3>{icon("mail")} {L(lang, "Codes &amp; facts", "कोड और जानकारी")}</h3>{kv(g_rows)}</div>'
                       + f'<div class="card"><h3>{icon("bank")} {L(lang, "Bank IFSC codes", "बैंक IFSC कोड")}</h3>{kv(b_rows)}</div>'
                       + f'<div class="card"><h3>{icon("grad")} {L(lang, "Education", "शिक्षा")}</h3>{kv(e_rows)}</div></div>'
                       + note(L(lang, 'Checked 27 Sep 2026 against India Post, RBI and bank records, the college website and the Election Commission results. '
                                      'Spotted something out of date? <a href="#update" data-open="upd">Tell us</a>.',
                                '27 सितंबर 2026 को इंडिया पोस्ट, आरबीआई व बैंक रिकॉर्ड, कॉलेज की वेबसाइट और चुनाव आयोग के नतीजों से जाँचा गया। '
                                'कुछ पुराना हो गया है? <a href="#update" data-open="upd">हमें बताएँ</a>।'), '') , 'sec-alt', 'glance')
    groups = ''
    for ic, en, hi, rows in OFFICES:
        items = []
        for a, ah, v, kind in rows:
            if kind == 'tel':
                val = f'<a href="{tel(v)}">{v}</a>'
            elif kind == 'mail':
                val = f'<a href="mailto:{v}">{v}</a>'
            else:
                val = esc(L(lang, v[0], v[1]))
            items.append((esc(L(lang, a, ah)), val))
        groups += f'<div class="card"><h3>{icon(ic)} {L(lang, en, hi)}</h3>{kv(items)}</div>'
    s_off = section(shead(L(lang, 'Local information', 'स्थानीय जानकारी'), L(lang, 'Government offices <em>&amp; contacts</em>', 'सरकारी दफ़्तर <em>और संपर्क</em>'),
                          L(lang, 'Key offices in and around Karsog. Tap any number to call.', 'करसोग और आसपास के मुख्य दफ़्तर। कॉल करने के लिए नंबर को छुएँ।'))
                    + f'<div class="grid g3">{groups}</div>'
                    + '<div class="btns mt2">'
                    + f'<a class="btn btn-o" href="{hl("/rti/")}">{icon("file")}{L(lang, "RTI replies &amp; audit reports", "आरटीआई जवाब और ऑडिट रिपोर्ट")}</a>'
                    + f'<a class="btn btn-o" href="{hl("/mandi-rates/")}">{icon("apple")}{L(lang, "Today’s mandi rates", "आज के मंडी भाव")}</a></div>', '', 'offices')
    fq = [(L(lang, 'What is the PIN code of Karsog?', 'करसोग का पिन कोड क्या है?'),
           L(lang, '175011 (Karsog post office). The STD code is 01907 and vehicles are registered as HP-30.',
             '175011 (करसोग डाकघर)। एसटीडी कोड 01907 है और गाड़ियों का नंबर HP-30 से शुरू होता है।')),
          (L(lang, 'What is the phone number of Civil Hospital Karsog?', 'सिविल अस्पताल करसोग का फ़ोन नंबर क्या है?'),
           L(lang, '01907-222218. For an ambulance, call 108.', '01907-222218। एम्बुलेंस के लिए 108 पर कॉल करें।')),
          (L(lang, 'What is the IFSC code of SBI Karsog?', 'एसबीआई करसोग का IFSC कोड क्या है?'),
           L(lang, 'SBIN0011884. PNB Karsog is PUNB0074300 and HDFC Bank Karsog is HDFC0008106.',
             'SBIN0011884। पीएनबी करसोग का PUNB0074300 और एचडीएफ़सी बैंक करसोग का HDFC0008106 है।'))]
    return dict(path='/contacts/', lang=lang, kind='page', hero='band',
                title=L(lang, 'Karsog Useful Numbers — Emergency, Hospital, Police, PIN 175011 & IFSC', 'करसोग के ज़रूरी नंबर — आपातकाल, अस्पताल, पुलिस, पिन 175011, IFSC'),
                desc=L(lang, 'Karsog useful numbers: emergency, civil hospital, police, SDM and government offices, PIN code 175011, STD code 01907, bank IFSC codes (SBI, PNB, HDFC), college and MLA.',
                       'करसोग के ज़रूरी नंबर: आपातकाल, सिविल अस्पताल, पुलिस, एसडीएम और सरकारी दफ़्तर, पिन कोड 175011, एसटीडी कोड 01907, बैंकों के IFSC कोड (एसबीआई, पीएनबी, एचडीएफ़सी), कॉलेज और विधायक।'),
                kicker=L(lang, 'Local info', 'स्थानीय जानकारी'), h1=L(lang, 'Useful <em>numbers</em>', 'ज़रूरी <em>नंबर</em>'),
                lede=L(lang, 'Emergency numbers first, then government offices and local contacts in Karsog. Tap a number to call.',
                       'पहले आपातकालीन नंबर, फिर करसोग के सरकारी दफ़्तर और स्थानीय संपर्क। कॉल करने के लिए नंबर को छुएँ।'),
                hero_extra=jump(lang, [('emergency', 'Emergency', 'आपातकाल'), ('glance', 'PIN, IFSC & codes', 'पिन, IFSC और कोड'), ('offices', 'Offices', 'दफ़्तर')]),
                crumbs=[(L(lang, 'Useful numbers', 'ज़रूरी नंबर'), '/contacts/')],
                body=s_sos + s_glance + s_off + comments('contacts', lang, None,
                                                         L(lang, 'Number not working, or one missing? Tell others here.', 'कोई नंबर नहीं लग रहा, या कोई नंबर छूट गया है? यहाँ बताइए।')) + faq_block(fq, lang),
                ld=[faq_ld(fq)])
