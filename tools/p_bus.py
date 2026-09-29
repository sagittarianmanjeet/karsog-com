"""Bus pages: Karsog bus stand timetable, one page per destination, private buses."""
from layout import L, icon, section, shead, faq_block, faq_ld, comments, note, esc, href
from data import (HRTC, PRIVATE, P_DEP, LINE, CHECKED, CHECKED_HI, P_CHECKED, P_CHECKED_HI, clock, bus_url, next_bus_json, PLACE_HI,
                  MISSING_HI)

BOARD = '/photos/bus-stand/karsog-bus-stand-board-2026'
GROUPS = [(0, 7, 'Night & early morning · before 7 AM', 'रात और तड़के · सुबह 7 बजे से पहले'),
          (7, 12, 'Morning · 7 AM to noon', 'सुबह · 7 से 12 बजे तक'),
          (12, 16, 'Afternoon · noon to 4 PM', 'दोपहर · 12 से 4 बजे तक'),
          (16, 24, 'Evening & night · after 4 PM', 'शाम और रात · 4 बजे के बाद')]


def dest_cell(b, lang, show_note=True):
    if b['slug']:
        name = L(lang, b['dest'], b['dest_hi'])
        d = f'<a href="{href(bus_url(b["slug"]), lang)}">{esc(name)}</a>'
    else:
        return L(lang, '<i>Not readable on the board</i>', '<i>बोर्ड पर पढ़ा नहीं जा सका</i>')
    n = L(lang, b['note'], b['note_hi'])
    return d + (f'<small>{esc(n)}</small>' if show_note and n else '')


def hrtc_table(rows, lang, show_dest=True, group=True):
    th = (f'<th>{L(lang, "Departs", "समय")}</th>' + (f'<th>{L(lang, "To", "कहाँ तक")}</th>' if show_dest else '') +
          f'<th class="hide-s">{L(lang, "Route on the board", "बोर्ड पर रूट")}</th>')
    ncol = 3 if show_dest else 2
    body = ''
    for lo, hi_, gen, ghi in (GROUPS if group else [(0, 24, '', '')]):
        rs = [b for b in rows if lo <= int(b['time'][:2]) < hi_]
        if not rs:
            continue
        if group:
            body += f'<tr class="grp"><th colspan="{ncol}">{L(lang, gen, ghi)}</th></tr>'
        for b in rs:
            route = (f'{esc(b["route_en"])}<small lang="hi">{esc(b["route_hi"])}</small>' if lang == 'en'
                     else f'{esc(b["route_hi"])}<small lang="en">{esc(b["route_en"])}</small>')
            body += (f'<tr><td class="t">{clock(b["time"], lang)}</td>' +
                     (f'<td>{dest_cell(b, lang)}</td>' if show_dest else '') +
                     f'<td class="hide-s">{route}<small>{L(lang, *LINE[b["line"]])}</small></td></tr>')
    return f'<div class="tbl"><div class="tbl-scroll"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div></div>'


def private_table(rows, lang):
    th = f'<th>{L(lang, "At Karsog", "करसोग में")}</th><th>{L(lang, "Route", "रूट")}</th><th class="hide-s">{L(lang, "Operator", "बस सेवा")}</th>'
    body = ''
    for r in rows:
        kind = L(lang, 'departs', 'चलती है') if r['karsog_kind'] == 'dep' else L(lang, 'reaches Karsog', 'करसोग पहुँचती है')
        t = f'{clock(r["karsog_time"], lang)}<small>{kind}</small>' if r['karsog_time'] else '—'
        body += (f'<tr><td class="t">{t}</td><td>{esc(r["route"])}<small class="show-s">{esc(r["op"])}</small></td>'
                 f'<td class="hide-s">{esc(r["op"])}</td></tr>')
    return f'<div class="tbl"><div class="tbl-scroll"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div></div>'


def nextbus(lang, src='j-bd', n=6, title=None, foot=None):
    title = title or L(lang, 'Next buses from Karsog', 'करसोग से अगली बसें')
    foot = foot or L(lang, 'By the time in India right now · confirm at the stand', 'भारत के अभी के समय के हिसाब से · बस अड्डे पर पुष्टि कर लें')
    return (f'<div class="nextbus" data-src="{src}" data-n="{n}"><h2 class="h"><span class="pulse"></span>{title}<span class="when"></span></h2>'
            f'<ol><li><span class="tm">—</span><span class="to">{L(lang, "Loading…", "लोड हो रहा है…")}</span></li></ol><p class="f">{foot}</p></div>')


def stand(lang):
    hl = lambda p: href(p, lang)
    n = len(HRTC)
    dests = {}
    for b in HRTC:
        if b['slug']:
            dests.setdefault(b['slug'], []).append(b)
    first, last = HRTC[0], HRTC[-1]
    # --- next bus + contacts
    aside = (f'<div class="aside-box"><div class="card"><h3>{L(lang, "At the bus stand", "बस अड्डे पर")}</h3>'
             f'<dl class="kv"><dt>{L(lang, "HRTC buses a day", "रोज़ एचआरटीसी बसें")}</dt><dd>{n}</dd>'
             f'<dt>{L(lang, "Private buses a day", "रोज़ प्राइवेट बसें")}</dt><dd>{len(P_DEP)}+</dd>'
             f'<dt>{L(lang, "Board photographed", "बोर्ड की फ़ोटो")}</dt><dd>{L(lang, CHECKED, CHECKED_HI)}</dd></dl>'
             f'<div class="btns"><a class="btn btn-p" href="https://online.hrtchp.com/oprs-web/" target="_blank" rel="noopener">{icon("ticket")}'
             f'{L(lang, "Book HRTC online", "एचआरटीसी ऑनलाइन बुकिंग")}</a>'
             f'<a class="btn btn-o" href="tel:01905222415">{icon("phone")}{L(lang, "HRTC Mandi 01905-222415", "एचआरटीसी मंडी 01905-222415")}</a></div></div>'
             f'<div class="card"><h3>{L(lang, "Timing changed?", "समय बदल गया?")}</h3><p>{L(lang, "Tell us on WhatsApp or in the comments, and we’ll update the page for everyone.", "व्हाट्सऐप पर या नीचे टिप्पणी में बताइए, हम सबके लिए पेज अपडेट कर देंगे।")}</p>'
             f'<button type="button" class="btn btn-g" data-open="upd">{icon("msg")}{L(lang, "Send an update", "अपडेट भेजें")}</button></div></div>')
    top = section(f'<div class="split"><div>{nextbus(lang, n=6)}'
                  + note(L(lang, f'<b>Please note:</b> HRTC times are from the timetable board at Karsog bus stand, photographed on {CHECKED}. '
                                 'Private bus times can change without notice. Always confirm at the stand or with the conductor before travelling.',
                           f'<b>ध्यान दें:</b> एचआरटीसी का समय करसोग बस अड्डे के टाइम-टेबल बोर्ड से है, जिसकी फ़ोटो {CHECKED_HI} को ली गई। '
                           'प्राइवेट बसों का समय बिना बताए बदल सकता है। निकलने से पहले बस अड्डे या कंडक्टर से पुष्टि ज़रूर कर लें।'))
                  + f'</div>{aside}</div>', 'sec-tight', 'next')
    # --- full timetable
    table = section(shead(L(lang, 'HRTC timetable', 'एचआरटीसी समय-सारणी'),
                          L(lang, f'All {n} departures from <em>Karsog</em>', f'करसोग से सभी <em>{n} बसें</em>'),
                          L(lang, f'In time order, exactly as on the board. First bus {clock(first["time"])}, last bus {clock(last["time"])}.',
                            f'समय के क्रम में, जैसे बोर्ड पर लिखा है। पहली बस {clock(first["time"], "hi")}, आख़िरी बस {clock(last["time"], "hi")}।'))
                    + hrtc_table(HRTC, lang), '', 'all')
    # --- by destination
    items = ''
    for s, bs in sorted(dests.items(), key=lambda x: (-len(x[1]), x[1][0]['dest'])):
        times = ', '.join(clock(b['time'], lang) for b in bs)
        cnt = L(lang, f'{len(bs)} bus{"es" if len(bs) > 1 else ""}', f'{len(bs)} बस')
        items += (f'<li><a href="{hl(bus_url(s))}"><b>{esc(L(lang, bs[0]["dest"], bs[0]["dest_hi"]))}<em>{cnt}</em></b>'
                  f'<span>{times}</span></a></li>')
    by_dest = section(shead(L(lang, 'By destination', 'मंज़िल के हिसाब से'), L(lang, 'Where do you want <em>to go?</em>', 'आपको <em>कहाँ जाना है?</em>'),
                            L(lang, 'Every destination on the board has its own page with its timings.', 'बोर्ड की हर मंज़िल का अपना पेज है, उसके समय के साथ।'))
                      + f'<ul class="dests">{items}</ul>', 'sec-alt', 'destinations')
    # --- private buses
    priv = section(shead(L(lang, 'Private buses', 'प्राइवेट बसें'), L(lang, 'Private buses at <em>Karsog</em>', 'करसोग की <em>प्राइवेट बसें</em>'),
                         L(lang, 'Private operators are not on the HRTC board. These are their departures from Karsog; the private bus page has arrivals and more routes.',
                           'प्राइवेट बसें एचआरटीसी बोर्ड पर नहीं होतीं। ये करसोग से उनकी रवानगी है; आने वाली बसें और दूसरे रूट प्राइवेट बस वाले पेज पर हैं।'),
                         more=(L(lang, 'All private buses', 'सभी प्राइवेट बसें'), hl('/karsog-private-bus/')))
                   + private_table(P_DEP, lang), '', 'private')
    # --- the board photo
    fig = (f'<figure class="board"><a href="{BOARD}.webp"><img src="{BOARD}-800.webp" srcset="{BOARD}-800.webp 800w, {BOARD}.webp 1600w" '
           f'sizes="(max-width:900px) 100vw, 820px" width="800" height="402" loading="lazy" decoding="async" '
           f'alt="{L(lang, "HRTC timetable board at Karsog bus stand, 25 September 2026", "करसोग बस अड्डे पर एचआरटीसी टाइम-टेबल बोर्ड, 25 सितंबर 2026")}"></a>'
           f'<figcaption>{L(lang, "Tap to open the full-size photo.", "पूरी फ़ोटो देखने के लिए छुएँ।")}</figcaption></figure>')
    board = section(shead(L(lang, 'The source', 'स्रोत'), L(lang, 'The timetable <em>board</em>', 'टाइम-टेबल <em>बोर्ड</em>'),
                          L(lang, 'The HRTC board at Karsog bus stand that this timetable is copied from.', 'करसोग बस अड्डे का एचआरटीसी बोर्ड, जिससे यह समय-सारणी ली गई है।'))
                    + fig, 'sec-alt', 'board', 'wrap wrap-n')
    to_k = section(shead(L(lang, 'Coming to Karsog?', 'करसोग आ रहे हैं?'), L(lang, 'Buses <em>to</em> Karsog', 'करसोग <em>आने वाली</em> बसें'),
                         L(lang, 'The board lists departures from Karsog only. For buses coming here:', 'बोर्ड पर सिर्फ़ करसोग से जाने वाली बसें हैं। यहाँ आने वाली बसों के लिए:'))
                   + '<div class="grid g2">'
                   + f'<a class="card icard" href="{hl("/mandi-to-karsog-bus/")}"><span class="i">{icon("bus")}</span><span><b>{L(lang, "Mandi ⇄ Karsog", "मंडी ⇄ करसोग")}</b>'
                     f'<span>{L(lang, "Buses both ways, first and last bus, fares", "दोनों तरफ़ की बसें, पहली और आख़िरी बस, किराया")}</span></span></a>'
                   + f'<a class="card icard" href="{hl("/shimla-to-karsog-bus/")}"><span class="i">{icon("bus")}</span><span><b>{L(lang, "Shimla ⇄ Karsog", "शिमला ⇄ करसोग")}</b>'
                     f'<span>{L(lang, "Buses both ways via Tattapani, fares", "तत्तापानी होकर दोनों तरफ़ की बसें, किराया")}</span></span></a></div>', 'sec-tight', 'to-karsog')
    fq = [(L(lang, 'What is the first bus from Karsog bus stand?', 'करसोग बस अड्डे से पहली बस कितने बजे है?'),
           L(lang, f'By the HRTC timetable board at Karsog bus stand (photographed {CHECKED}), the first departure is at {clock(first["time"])}. '
                   'Confirm at the stand, as the board may be out of date.',
             f'करसोग बस अड्डे के एचआरटीसी टाइम-टेबल बोर्ड ({CHECKED_HI} की फ़ोटो) के अनुसार पहली बस {clock(first["time"], "hi")} बजे है। '
             'बोर्ड पुराना हो सकता है, इसलिए बस अड्डे पर पुष्टि कर लें।')),
          (L(lang, 'How many buses leave Karsog bus stand every day?', 'करसोग बस अड्डे से रोज़ कितनी बसें चलती हैं?'),
           L(lang, f'The HRTC board lists {n} departures a day on three lines: Karsog–Churag–Tattapani, Karsog–Pangna–Mandi and Karsog–Kelodhar. '
                   f'Private operators add about {len(P_DEP)} more.',
             f'एचआरटीसी बोर्ड पर रोज़ {n} बसें हैं, तीन रूटों पर: करसोग–चुराग–तत्तापानी, करसोग–पांगणा–मंडी और करसोग–केलोधार। '
             f'प्राइवेट बसें लगभग {len(P_DEP)} और हैं।')),
          (L(lang, 'Is there a bus from Karsog to Delhi?', 'क्या करसोग से दिल्ली की बस है?'),
           L(lang, 'Yes. The HRTC board lists a Karsog–Delhi bus at 5:00 PM, and a Haridwar bus at 12:10 PM. Both can be booked on HRTC’s website.',
             'हाँ। एचआरटीसी बोर्ड पर करसोग–दिल्ली बस शाम 5:00 बजे और हरिद्वार की बस दोपहर 12:10 बजे है। दोनों की बुकिंग एचआरटीसी की वेबसाइट पर होती है।')),
          (L(lang, 'Can I book Karsog buses online?', 'क्या करसोग की बसें ऑनलाइन बुक हो सकती हैं?'),
           L(lang, 'Some long-distance HRTC buses (Shimla, Mandi, Haridwar, Delhi) can be booked at online.hrtchp.com. Most local buses cannot; buy the ticket on the bus.',
             'कुछ लंबी दूरी की एचआरटीसी बसें (शिमला, मंडी, हरिद्वार, दिल्ली) online.hrtchp.com पर बुक होती हैं। ज़्यादातर लोकल बसों का टिकट बस में ही मिलता है।'))]
    body = (top + table + by_dest + priv + board + to_k +
            comments('karsog-bus-stand', lang, L(lang, 'Is this timing still right?', 'क्या यह समय अब भी सही है?'),
                     L(lang, 'Seen a bus change time, stop running or get cancelled? Tell other travellers here.',
                       'कोई बस समय बदल गई, बंद हो गई या रद्द हुई? यहाँ दूसरे यात्रियों को बताइए।'),
                     L(lang, 'e.g. The 11:10 AM bus to Mandi now leaves at 11:30.', 'जैसे: मंडी की सुबह 11:10 वाली बस अब 11:30 बजे चलती है।')) +
            faq_block(fq, lang))
    return dict(
        path='/karsog-bus-stand/', lang=lang, kind='bus', hero='band',
        title=L(lang, 'Karsog Bus Timing — Bus Stand Time Table (HRTC & Private)', 'करसोग बस टाइमिंग — बस अड्डा समय-सारणी (एचआरटीसी व प्राइवेट)'),
        desc=L(lang, f'Karsog bus stand time table: all {n} HRTC departures to Shimla, Mandi, Rampur, Delhi, Haridwar and villages, private buses and a live next-bus board.',
               f'करसोग बस अड्डे की समय-सारणी: शिमला, मंडी, रामपुर, दिल्ली, हरिद्वार और गाँवों की सभी {n} एचआरटीसी बसें, प्राइवेट बसें और अगली बस का लाइव बोर्ड।'),
        kicker=L(lang, 'Karsog bus stand · HRTC & private', 'करसोग बस अड्डा · एचआरटीसी और प्राइवेट'),
        h1=L(lang, 'Karsog bus <em>timings</em>', 'करसोग बसों का <em>समय</em>'),
        lede=L(lang, f'All {n} HRTC departures from the timetable board at Karsog bus stand, private buses, and a live board of the next buses.',
               f'करसोग बस अड्डे के टाइम-टेबल बोर्ड की सभी {n} एचआरटीसी बसें, प्राइवेट बसें, और अगली बसों का लाइव बोर्ड।'),
        chips=[('clock', L(lang, f'Board checked {CHECKED}', f'बोर्ड {CHECKED_HI} को देखा गया')), ('bus', L(lang, f'{n} HRTC + {len(P_DEP)} private', f'{n} एचआरटीसी + {len(P_DEP)} प्राइवेट'))],
        hero_extra='<div class="jump">' + ''.join(f'<a href="#{k}">{L(lang, en, hi)}</a>' for k, en, hi in [
            ('next', 'Next buses', 'अगली बसें'), ('all', 'All departures', 'सभी बसें'), ('destinations', 'By destination', 'मंज़िल से'),
            ('private', 'Private buses', 'प्राइवेट बसें')]) + '</div>',
        crumbs=[(L(lang, 'Karsog bus timings', 'करसोग बस समय'), '/karsog-bus-stand/')], body=body, ld=[faq_ld(fq)], og='/og/bus.jpg',
        data={'j-bd': next_bus_json()})


# ---------------------------------------------------------------- one page per destination on the board
from data import DIST, GUIDES, hi_places
DEST_INFO = {   # short, safe descriptions of the bigger destinations
    'rampur': ('Rampur Bushahr is a town on the Sutlej, on the road to Kinnaur.', 'रामपुर बुशहर सतलुज किनारे बसा शहर है, किन्नौर के रास्ते पर।'),
    'reckong-peo': ('Reckong Peo is the headquarters of Kinnaur district. These buses come through Karsog on longer routes.', 'रिकांगपिओ किन्नौर ज़िले का मुख्यालय है। ये बसें लंबे रूट पर करसोग से होकर जाती हैं।'),
    'dharamshala': ('Dharamshala, in Kangra district, is a long overnight-style journey; these buses pass through Karsog on longer routes.', 'धर्मशाला (ज़िला कांगड़ा) का सफ़र लंबा है; ये बसें लंबे रूट पर करसोग से होकर जाती हैं।'),
    'delhi': ('The Delhi bus is HRTC’s long-distance service from Karsog, and it can be booked online.', 'दिल्ली वाली बस करसोग से एचआरटीसी की लंबी दूरी की सेवा है, और इसकी ऑनलाइन बुकिंग होती है।'),
    'haridwar': ('The Haridwar bus is HRTC’s long-distance service from Karsog, and it can be booked online.', 'हरिद्वार वाली बस करसोग से एचआरटीसी की लंबी दूरी की सेवा है, और इसकी ऑनलाइन बुकिंग होती है।'),
    'rewalsar': ('Rewalsar is a lake town near Mandi with Hindu, Buddhist and Sikh shrines.', 'रिवालसर मंडी के पास झील वाला क़स्बा है, जहाँ हिंदू, बौद्ध और सिख तीर्थ हैं।'),
    'mahunag': ('Shri Mool Mahunag is the valley’s most famous temple.', 'श्री मूल माहूनाग घाटी का सबसे प्रसिद्ध मंदिर है।'),
    'thunag': ('Thunag is the main town of the Seraj area, beyond Janjehli.', 'थुनाग सराज क्षेत्र का मुख्य क़स्बा है, जंजैहली से आगे।'),
    'gada-gushaini': ('Gada Gushaini is a village in the Seraj hills, known for its forests.', 'गाड़ागुशैणी सराज की पहाड़ियों का गाँव है, अपने जंगलों के लिए जाना जाता है।'),
}
PLACE_PAGE = {'pokhi': '/pokhi-mahog/', 'somakothi': '/pokhi-mahog/', 'dateha': '/kotlu-dateha/', 'gada-gushaini': '/gada-gushaini/',
              'mahunag': '/mahunag/', 'syanj': '/beludhar/', 'rampur': None}


def dest_pages(lang):
    hl = lambda p: href(p, lang)
    dests = {}
    for b in HRTC:
        if b['slug'] and b['slug'] not in ('shimla', 'mandi'):
            dests.setdefault(b['slug'], []).append(b)
    popular = ['shimla', 'mandi', 'rampur', 'reckong-peo', 'delhi', 'mahunag', 'dharamshala', 'haridwar']
    out = []
    for s, bs in dests.items():
        n, hi = bs[0]['dest'], bs[0]['dest_hi']
        name = L(lang, n, hi)
        times = ', '.join(clock(b['time'], lang) for b in bs)
        cnt = len(bs)
        path = f'/bus/karsog-to-{s}/'
        data = [{'t': b['time'], 'to': n, 'hi': hi, 'u': ''} for b in bs]
        info = DEST_INFO.get(s)
        about = f'<p>{L(lang, *info)}</p>' if info else ''
        pg = PLACE_PAGE.get(s)
        if pg:
            about += f'<p><a class="more-link" href="{hl(pg)}">{L(lang, f"About {n}: guide and drone photos", f"{hi}: जानकारी और ड्रोन फ़ोटो")} {icon("arrow")}</a></p>'
        dist = next((d for d in DIST if d[0].split(' (')[0] == n), None)
        facts_ = [(str(cnt), L(lang, 'buses a day from Karsog', 'बसें रोज़ करसोग से')), (clock(bs[0]['time'], lang), L(lang, 'first bus', 'पहली बस'))]
        if cnt > 1:
            facts_.append((clock(bs[-1]['time'], lang), L(lang, 'last bus', 'आख़िरी बस')))
        if dist:
            facts_.append((f'{dist[2]:g} ' + L(lang, 'km', 'किमी'), L(lang, 'by road', 'सड़क से')))
        fx = '<div class="facts">' + ''.join(f'<div><b>{v}</b><small>{k}</small></div>' for v, k in facts_) + '</div>'
        others = ''.join(f'<li><a href="{hl(bus_url(o))}"><b>{esc(L(lang, *next((x["dest"], x["dest_hi"]) for x in HRTC if x["slug"] == o)))}</b>'
                         f'<span>{L(lang, "Bus timings", "बसों का समय")}</span></a></li>' for o in popular if o != s)
        top = section('<div class="split"><div>' + nextbus(lang, n=min(3, cnt), title=L(lang, f'Next bus to {n}', f'{hi} की अगली बस')) +
                      note(L(lang, f'<b>Please note:</b> times are from the HRTC timetable board at Karsog bus stand, photographed on {CHECKED}. '
                                   'Confirm at the stand before travelling.',
                             f'<b>ध्यान दें:</b> समय करसोग बस अड्डे के एचआरटीसी टाइम-टेबल बोर्ड से है, जिसकी फ़ोटो {CHECKED_HI} को ली गई। '
                             'निकलने से पहले बस अड्डे पर पुष्टि कर लें।')) +
                      f'</div><div>{fx}{about}</div></div>', 'sec-tight', 'next')
        tbl = section(shead(L(lang, 'Timetable', 'समय-सारणी'), L(lang, f'Karsog to <em>{esc(n)}</em>', f'करसोग से <em>{esc(hi)}</em>')) +
                      hrtc_table(bs, lang, show_dest=False, group=False), '', 'times')
        more = section(shead(L(lang, 'More buses', 'और बसें'), L(lang, 'Other buses from <em>Karsog</em>', 'करसोग से <em>दूसरी बसें</em>'),
                             more=(L(lang, f'All {len(HRTC)} departures', f'सभी {len(HRTC)} बसें'), hl('/karsog-bus-stand/')))
                       + f'<ul class="dests">{others}</ul>', 'sec-alt', 'more')
        fq = [(L(lang, f'What time is the bus from Karsog to {n}?', f'करसोग से {hi} की बस कितने बजे है?'),
               L(lang, f'The HRTC timetable board at Karsog bus stand (photographed {CHECKED}) lists {cnt} bus{"es" if cnt > 1 else ""} to {n}: {times}. Confirm at the stand before travelling.',
                 f'करसोग बस अड्डे के एचआरटीसी टाइम-टेबल बोर्ड ({CHECKED_HI} की फ़ोटो) के अनुसार {hi} के लिए {cnt} बस है: {times}। निकलने से पहले बस अड्डे पर पुष्टि कर लें।'))]
        if dist:
            fq.append((L(lang, f'How far is {n} from Karsog?', f'करसोग से {hi} कितनी दूर है?'),
                       L(lang, f'About {dist[2]:g} km by road, around {dist[3]} by car.', f'सड़क से लगभग {dist[2]:g} किमी, गाड़ी से लगभग {dist[4]}।')))
        body = top + tbl + more + comments('bus/karsog-to-' + s, lang, L(lang, 'Is this timing still right?', 'क्या यह समय अब भी सही है?'),
                                           L(lang, 'Seen this bus change time or stop running? Tell other travellers here.',
                                             'यह बस समय बदल गई या बंद हो गई? यहाँ दूसरे यात्रियों को बताइए।')) + faq_block(fq, lang)
        out.append(dict(
            path=path, lang=lang, kind='bus', hero='band', subnav='buses',
            title=L(lang, f'Karsog to {n} Bus Timing — HRTC ({hi})', f'करसोग से {hi} बस का समय — एचआरटीसी'),
            desc=L(lang, f'Karsog to {n} bus timing: {times} (HRTC, from the timetable board at Karsog bus stand, {CHECKED}), with a live next-bus board.',
                   f'करसोग से {hi} बस का समय: {times} (एचआरटीसी, करसोग बस अड्डे के टाइम-टेबल बोर्ड से, {CHECKED_HI}), अगली बस के लाइव बोर्ड के साथ।'),
            kicker=L(lang, 'HRTC bus timing', 'एचआरटीसी बस का समय'),
            h1=L(lang, f'Karsog to {esc(n)} <em>bus</em>', f'करसोग से {esc(hi)} <em>बस</em>'),
            lede=L(lang, f'{"One bus" if cnt == 1 else f"{cnt} buses"} a day from Karsog bus stand to {esc(n)}: {times}.',
                   f'करसोग बस अड्डे से {esc(hi)} के लिए रोज़ {cnt} बस: {times}।'),
            chips=[('clock', L(lang, f'Board checked {CHECKED}', f'बोर्ड {CHECKED_HI} को देखा गया'))],
            crumbs=[(L(lang, 'Karsog bus timings', 'करसोग बस समय'), '/karsog-bus-stand/'), (L(lang, f'Karsog to {n}', f'करसोग से {hi}'), path)],
            body=body, ld=[faq_ld(fq)], og='/og/bus.jpg', data={'j-bd': data}))
    return out


# ---------------------------------------------------------------- private buses
# Operators seen on Karsog routes whose timings are not confirmed yet
P_ROUTES = [('Chetan Bus Service', 'Kamaksha – Karsog – Pangna – Jachh – Charkhari'), ('Shiv Shankar Express', 'Karsog – Syanj – Syanjali – Karsog'),
            ('NPT Bus Service', 'Karsog – Chhatri – Ani'), ('Anshika Bus Service', 'Karsog – Shri Mool Mahunag'),
            ('Hari Om Bus Service', 'Karsog – Shimla ISBT'), ('Radhika Bus Service', 'Somakothi – Karsog – Kelodhar – Syanj Bagra'),
            ('Radhika Bus Service', 'Ani – Karsog – Mahunag – Bagshad')]


def p_route(r, lang):
    return esc(r['route'] if lang == 'en' else hi_places(r['route']))


# Hindi for the notes in data/karsog-private-buses.csv (a new note with no Hindi here shows in English and is reported)
PRIVATE_NOTE_HI = {
    'Two Manohar buses run on this route': 'इस रूट पर मनोहर की दो बसें चलती हैं',
    'Arrival time from a separate Aug 2026 post': 'पहुँचने का समय अगस्त 2026 की एक अलग पोस्ट से',
    'Bus still carries the old Blue Line name': 'बस पर अब भी पुराना ब्लू लाइन नाम लिखा है',
    'Arrival is approximate': 'पहुँचने का समय अनुमानित है',
    'Runs via Bithri from 7 Sep 2025': '7 सितंबर 2025 से बिठरी होकर चलती है',
    'Service started 11 Dec 2025': 'यह सेवा 11 दिसंबर 2025 को शुरू हुई',
    'One commenter disputed these times': 'एक टिप्पणी में इन समयों पर सवाल उठाया गया है',
    'Runs via Pangna and Churag; does not enter Karsog town': 'पांगणा और चुराग होकर चलती है; करसोग शहर के अंदर नहीं आती',
    'Runs via Churag and Pangna; does not enter Karsog town': 'चुराग और पांगणा होकर चलती है; करसोग शहर के अंदर नहीं आती',
}


def private_note(r, lang):
    n = r.get('note', '')
    if not n or lang == 'en':
        return n
    if n not in PRIVATE_NOTE_HI:
        MISSING_HI.add(n)
    return PRIVATE_NOTE_HI.get(n, n)


def op_table(rows, lang):
    th = f'<th>{L(lang, "At Karsog", "करसोग में")}</th><th>{L(lang, "Route", "रूट")}</th><th class="hide-s">{L(lang, "Other stops", "दूसरे स्टॉप")}</th>'
    body = ''
    for r in rows:
        kind = L(lang, 'departs', 'चलती है') if r['karsog_kind'] == 'dep' else L(lang, 'reaches Karsog', 'करसोग पहुँचती है')
        t = f'{clock(r["karsog_time"], lang)}<small>{kind}</small>' if r['karsog_time'] else '—'
        stops = r['stops'] if lang == 'en' else hi_places(r['stops'])
        note_ = private_note(r, lang)
        body += (f'<tr><td class="t">{t}</td><td>{p_route(r, lang)}' + (f'<small>{esc(note_)}</small>' if note_ else '') +
                 (f'<small class="show-s">{esc(stops)}</small>' if stops else '') +
                 f'</td><td class="hide-s"><small>{esc(stops) or "—"}</small></td></tr>')
    return f'<div class="tbl"><div class="tbl-scroll"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div></div>'


def private(lang):
    hl = lambda p: href(p, lang)
    at_k = [r for r in PRIVATE if r['karsog_kind']]
    near = [r for r in PRIVATE if not r['karsog_kind']]
    ops = {}
    for r in at_k:
        ops.setdefault(r['op'], []).append(r)
    for v in ops.values():
        v.sort(key=lambda r: r['karsog_time'] or '99')
    pdata = sorted([{'t': r['karsog_time'], 'to': r['to'], 'hi': PLACE_HI.get(r['to'], r['to']), 'u': '', 'p': 1}
                    for r in at_k if r['karsog_kind'] == 'dep' and r['karsog_time']], key=lambda x: x['t'])
    blocks = ''.join(f'<h3 class="mt2">{esc(o)} <small class="pill">{len(rs)} {L(lang, "trips", "ट्रिप")}</small></h3>{op_table(rs, lang)}'
                     for o, rs in sorted(ops.items()))
    top = section('<div class="split"><div>' + nextbus(lang, n=5, title=L(lang, 'Next private buses from Karsog', 'करसोग से अगली प्राइवेट बसें')) +
                  note(L(lang, '<b>Please note:</b> private bus timings can change without notice, so confirm with the conductor or at the stand before travelling. '
                               'We try our best to keep this page updated. Spotted a wrong or changed time? Tell us in the comments below.',
                         '<b>ध्यान दें:</b> प्राइवेट बसों का समय बिना बताए बदल सकता है, इसलिए निकलने से पहले कंडक्टर या बस अड्डे पर पुष्टि कर लें। '
                         'हम इस पेज को अपडेट रखने की पूरी कोशिश करते हैं। कोई समय ग़लत या बदला हुआ दिखे तो नीचे टिप्पणी में बताइए।')) +
                  '</div><div class="aside-box"><div class="card">' +
                  f'<h3>{L(lang, "At a glance", "एक नज़र में")}</h3><dl class="kv"><dt>{L(lang, "Private trips at Karsog", "करसोग में प्राइवेट ट्रिप")}</dt><dd>{len(at_k)}</dd>'
                  f'<dt>{L(lang, "Operators", "बस सेवाएँ")}</dt><dd>{len(ops)}</dd><dt>{L(lang, "Last checked", "आख़िरी बार देखा")}</dt><dd>{L(lang, P_CHECKED, P_CHECKED_HI)}</dd></dl>'
                  f'<div class="btns"><a class="btn btn-o" href="{hl("/karsog-bus-stand/")}">{icon("bus")}{L(lang, "HRTC timetable", "एचआरटीसी समय-सारणी")}</a></div>'
                  '</div></div></div>', 'sec-tight', 'next')
    by_op = section(shead(L(lang, 'By operator', 'बस सेवा के हिसाब से'), L(lang, 'Private buses at <em>Karsog</em>', 'करसोग की <em>प्राइवेट बसें</em>'),
                          L(lang, f'{len(at_k)} trips by {len(ops)} private operators that start, end or stop at Karsog. Times marked “reaches Karsog” are arrivals.',
                            f'{len(ops)} प्राइवेट बस सेवाओं की {len(at_k)} ट्रिप जो करसोग से शुरू होती हैं, यहाँ ख़त्म होती हैं या यहाँ रुकती हैं। “करसोग पहुँचती है” वाला समय पहुँचने का है।'))
                    + blocks, '', 'operators')
    rl = ''.join(f'<li><b>{esc(o)}</b>: {esc(rt if lang == "en" else hi_places(rt))}</li>' for o, rt in P_ROUTES)
    unconf = section(shead('', L(lang, 'More routes <em>(times not confirmed)</em>', 'और रूट <em>(समय पक्का नहीं)</em>'),
                           L(lang, 'These operators also run on Karsog routes. If you know their timings, please tell us.',
                             'ये बसें भी करसोग के रूटों पर चलती हैं। अगर आपको इनका समय पता है, तो हमें ज़रूर बताइए।'))
                     + f'<ul class="cols2">{rl}</ul>', 'sec-alt', 'more-routes')
    nearby = section(shead('', L(lang, 'Private buses <em>nearby</em>', 'आसपास की <em>प्राइवेट बसें</em>'),
                           L(lang, 'These don’t enter Karsog town but serve Tattapani and Pangna.', 'ये करसोग शहर में नहीं आतीं, पर तत्तापानी और पांगणा की तरफ़ चलती हैं।'))
                     + op_table(near, lang), '', 'nearby')
    names = ', '.join(sorted(ops))
    fq = [(L(lang, 'Which private buses run from Karsog?', 'करसोग से कौन-सी प्राइवेट बसें चलती हैं?'),
           L(lang, f'Private operators on Karsog routes include {names}. They run to Shimla, Sundernagar, Mandi, Hamirpur, Rampur, Ani and nearby villages. Timings can change, so confirm before travelling.',
             f'करसोग के रूटों पर चलने वाली प्राइवेट बसों में {names} शामिल हैं। ये शिमला, सुंदरनगर, मंडी, हमीरपुर, रामपुर, आनी और आसपास के गाँवों तक जाती हैं। समय बदल सकता है, इसलिए पुष्टि कर लें।')),
          (L(lang, 'What is the first private bus from Karsog to Shimla?', 'करसोग से शिमला की पहली प्राइवेट बस कितने बजे है?'),
           L(lang, 'Manohar Bus Service leaves Karsog for Shimla ISBT at 4:40 AM, with a second bus at 7:30 AM. Timings can change, so confirm before travelling.',
             'मनोहर बस सर्विस करसोग से शिमला आईएसबीटी के लिए सुबह 4:40 बजे चलती है, और दूसरी बस सुबह 7:30 बजे। समय बदल सकता है, इसलिए पुष्टि कर लें।')),
          (L(lang, 'Is there a private bus from Karsog to Sundernagar or Mandi?', 'क्या करसोग से सुंदरनगर या मंडी की प्राइवेट बस है?'),
           L(lang, 'Yes. VIP Coach runs Karsog–Sundernagar–Mandi at 4:40 AM and 6:00 AM, and to Sundernagar at 7:10 AM; Sheetla and Chetan also run to Sundernagar. See the tables on this page.',
             'हाँ। वीआईपी कोच करसोग–सुंदरनगर–मंडी के लिए सुबह 4:40 और 6:00 बजे, और सुंदरनगर के लिए सुबह 7:10 बजे चलती है; शीतला और चेतन बसें भी सुंदरनगर जाती हैं। इस पेज की तालिकाएँ देखें।'))]
    body = (top + by_op + unconf + nearby +
            comments('karsog-private-bus', lang, L(lang, 'Is this timing still right?', 'क्या यह समय अब भी सही है?'),
                     L(lang, 'Seen a private bus change time or stop running? Tell other travellers here.', 'कोई प्राइवेट बस समय बदल गई या बंद हो गई? यहाँ दूसरे यात्रियों को बताइए।'),
                     L(lang, 'e.g. The 7:30 AM Manohar bus now leaves at 7:45.', 'जैसे: मनोहर की सुबह 7:30 वाली बस अब 7:45 बजे चलती है।')) + faq_block(fq, lang))
    return dict(path='/karsog-private-bus/', lang=lang, kind='bus', hero='band',
                title=L(lang, 'Karsog Private Bus Timings — Shimla, Sundernagar, Mandi', 'करसोग प्राइवेट बस का समय — शिमला, सुंदरनगर, मंडी'),
                desc=L(lang, f'Private bus timings at Karsog: {len(at_k)} trips by {names}, to Shimla, Sundernagar, Mandi, Hamirpur, Rampur and Ani.',
                       f'करसोग की प्राइवेट बसों का समय: {len(ops)} बस सेवाओं की {len(at_k)} ट्रिप, शिमला, सुंदरनगर, मंडी, हमीरपुर, रामपुर और आनी के लिए।'),
                kicker=L(lang, 'Private operators', 'प्राइवेट बसें'), h1=L(lang, 'Karsog private <em>buses</em>', 'करसोग की प्राइवेट <em>बसें</em>'),
                lede=L(lang, f'{len(at_k)} private bus trips at Karsog by {len(ops)} operators, with a live board of the next departures.',
                       f'करसोग में {len(ops)} बस सेवाओं की {len(at_k)} प्राइवेट ट्रिप, अगली बसों के लाइव बोर्ड के साथ।'),
                chips=[('clock', L(lang, f'Checked {P_CHECKED}', f'{P_CHECKED_HI} को देखा गया'))],
                crumbs=[(L(lang, 'Karsog bus timings', 'करसोग बस समय'), '/karsog-bus-stand/'), (L(lang, 'Private buses', 'प्राइवेट बसें'), '/karsog-private-bus/')],
                body=body, ld=[faq_ld(fq)], og='/og/bus.jpg', data={'j-bd': pdata})


# ---------------------------------------------------------------- Mandi and Shimla pages
def _rows_table(rows, lang, cols):
    """rows: [(time, what, note)] -> simple 3-column timetable"""
    th = ''.join(f'<th{" class=hide-s" if i == 2 else ""}>{c}</th>' for i, c in enumerate(cols))
    body = ''.join(f'<tr><td class="t">{clock(t, lang)}</td><td>{w}<small class="show-s">{n}</small></td><td class="hide-s"><small>{n}</small></td></tr>'
                   for t, w, n in rows)
    return f'<div class="tbl"><div class="tbl-scroll"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div></div>'


def _board(dest_slug):
    return [b for b in HRTC if b['slug'] == dest_slug]


def corridor(lang, city):
    """Mandi ⇄ Karsog or Shimla ⇄ Karsog."""
    hl = lambda p: href(p, lang)
    M = city == 'mandi'
    C, CH = ('Mandi', 'मंडी') if M else ('Shimla', 'शिमला')
    path = '/mandi-to-karsog-bus/' if M else '/shimla-to-karsog-bus/'
    cols = [L(lang, 'Time', 'समय'), L(lang, 'Bus', 'बस'), L(lang, 'Details', 'जानकारी')]
    hrtc = L(lang, 'HRTC', 'एचआरटीसी')
    # --- from Karsog
    out_rows = []
    for b in _board(city):
        extra = []
        if b['note']:
            extra.append(L(lang, b['note'], b['note_hi']))
        if M and b['time'] == '11:10':
            extra.append(L(lang, '₹256, also bookable online', '₹256, ऑनलाइन बुकिंग भी'))
        if not M and b['time'] == '05:00':
            extra.append(L(lang, '₹278, also bookable online', '₹278, ऑनलाइन बुकिंग भी'))
        extra.append(L(lang, 'Karsog bus stand board', 'करसोग बस अड्डे का बोर्ड'))
        out_rows.append((b['time'], hrtc, ' · '.join(extra)))
    if M:
        out_rows += [('04:40', 'VIP Coach', L(lang, 'Private, via Sundernagar', 'प्राइवेट, सुंदरनगर होकर')),
                     ('06:00', 'VIP Coach', L(lang, 'Private, via Sundernagar (Sundernagar 10:30, Mandi 11:30)', 'प्राइवेट, सुंदरनगर होकर (सुंदरनगर 10:30, मंडी 11:30)'))]
    else:
        out_rows += [('12:10', hrtc, L(lang, 'Haridwar bus via Shimla · ₹285 · bookable online · reaches Shimla ~6:40 PM', 'हरिद्वार वाली बस, शिमला होकर · ₹285 · ऑनलाइन बुकिंग · शिमला लगभग शाम 6:40')),
                     ('17:00', hrtc, L(lang, 'Delhi bus via Shimla · ₹285 · bookable online · reaches Shimla ~10:30 PM', 'दिल्ली वाली बस, शिमला होकर · ₹285 · ऑनलाइन बुकिंग · शिमला लगभग रात 10:30')),
                     ('04:40', 'Manohar Bus Service', L(lang, 'Private, to Shimla ISBT', 'प्राइवेट, शिमला आईएसबीटी तक')),
                     ('07:30', 'Manohar Bus Service', L(lang, 'Private, to Shimla ISBT', 'प्राइवेट, शिमला आईएसबीटी तक')),
                     ('13:00', 'Ayush Nipun Bus Service', L(lang, 'Private, to Shimla ISBT', 'प्राइवेट, शिमला आईएसबीटी तक'))]
    out_rows.sort(key=lambda r: r[0])
    # --- to Karsog
    if M:
        in_rows = [('04:30', hrtc, L(lang, 'On HRTC online booking (25 Sep 2026) · ₹285 · about 5¾ hours, reaches Karsog ~10:15 AM',
                                     'एचआरटीसी ऑनलाइन बुकिंग पर (25 सितंबर 2026) · ₹285 · लगभग 5¾ घंटे, करसोग लगभग सुबह 10:15')),
                   ('06:00', hrtc, L(lang, 'Reported locally · confirm at Mandi bus stand', 'स्थानीय जानकारी · मंडी बस अड्डे पर पुष्टि करें')),
                   ('07:45', hrtc, L(lang, 'Reported locally: Mandi depot bus to Mahunag via Karsog · confirm', 'स्थानीय जानकारी: मंडी डिपो की बस, करसोग होकर माहूँनाग · पुष्टि करें')),
                   ('08:30', hrtc, L(lang, 'Reported locally · confirm at Mandi bus stand', 'स्थानीय जानकारी · मंडी बस अड्डे पर पुष्टि करें')),
                   ('12:00', hrtc, L(lang, 'Reported locally · confirm at Mandi bus stand', 'स्थानीय जानकारी · मंडी बस अड्डे पर पुष्टि करें')),
                   ('15:00', hrtc, L(lang, 'Reported locally · confirm at Mandi bus stand', 'स्थानीय जानकारी · मंडी बस अड्डे पर पुष्टि करें')),
                   ('12:30', 'VIP Coach', L(lang, 'Private, via Sundernagar (13:40) · reaches Karsog ~7:00 PM', 'प्राइवेट, सुंदरनगर (13:40) होकर · करसोग लगभग शाम 7:00'))]
    else:
        in_rows = [('06:30', hrtc, L(lang, 'On HRTC online booking (25 Sep 2026) · ₹278 · reaches Karsog ~11:30 AM', 'एचआरटीसी ऑनलाइन बुकिंग पर (25 सितंबर 2026) · ₹278 · करसोग लगभग सुबह 11:30')),
                   ('14:40', hrtc, L(lang, 'On HRTC online booking (25 Sep 2026) · ₹278 · via Bagshad · reaches Karsog ~8:00 PM', 'एचआरटीसी ऑनलाइन बुकिंग पर (25 सितंबर 2026) · ₹278 · वाया बगशाड · करसोग लगभग रात 8:00')),
                   ('11:00', 'Manohar Bus Service', L(lang, 'Private · reaches Karsog ~4:40 PM', 'प्राइवेट · करसोग लगभग शाम 4:40')),
                   ('06:00', 'Ayush Nipun Bus Service', L(lang, 'Private · arrival time not confirmed', 'प्राइवेट · पहुँचने का समय पक्का नहीं'))]
    in_rows.sort(key=lambda r: r[0])
    km = 99 if M else 94
    drive = L(lang, 'about 3¾ hours', 'लगभग 3¾ घंटे')
    t_out = section(shead(L(lang, f'Karsog → {C}', f'करसोग → {CH}'), L(lang, f'From Karsog to <em>{C}</em>', f'करसोग से <em>{CH}</em>'),
                          L(lang, 'HRTC times are from the timetable board at Karsog bus stand (25 Sep 2026); private times can change.',
                            'एचआरटीसी का समय करसोग बस अड्डे के टाइम-टेबल बोर्ड से है (25 सितंबर 2026); प्राइवेट बसों का समय बदल सकता है।'))
                    + _rows_table(out_rows, lang, cols), '', 'from-karsog')
    t_in = section(shead(L(lang, f'{C} → Karsog', f'{CH} → करसोग'), L(lang, f'From {C} to <em>Karsog</em>', f'{CH} से <em>करसोग</em>'),
                         L(lang, f'Only some buses from {C} are on HRTC’s website. Confirm the others at the {C} bus stand the day before.',
                           f'{CH} से कुछ ही बसें एचआरटीसी की वेबसाइट पर हैं। बाक़ी की पुष्टि एक दिन पहले {CH} बस अड्डे पर कर लें।'))
                   + _rows_table(in_rows, lang, cols), 'sec-alt', 'to-karsog')
    phone = ('01905-222415', 'tel:01905222415', L(lang, 'HRTC Mandi bus stand', 'एचआरटीसी मंडी बस अड्डा')) if M else \
            ('0177-2658788', 'tel:01772658788', L(lang, 'Shimla ISBT enquiry', 'शिमला आईएसबीटी पूछताछ'))
    tips = section('<div class="grid g3">' +
                   f'<div class="card"><h3>{L(lang, "Distance", "दूरी")}</h3><p>{L(lang, f"About {km} km by road, {drive} by car. Buses take longer: about 5 to 6 hours.", f"सड़क से लगभग {km} किमी, गाड़ी से {drive}। बस में ज़्यादा समय लगता है: लगभग 5 से 6 घंटे।")}</p>'
                   f'<p><a class="more-link" href="{hl("/distance/")}">{L(lang, "All distances", "सभी दूरियाँ")} {icon("arrow")}</a></p></div>'
                   f'<div class="card"><h3>{L(lang, "Confirm before you go", "निकलने से पहले पुष्टि करें")}</h3><p>{phone[2]}: <a href="{phone[1]}"><b>{phone[0]}</b></a></p>'
                   f'<p>{L(lang, "Book some HRTC buses at", "कुछ एचआरटीसी बसों की बुकिंग")} <a href="https://online.hrtchp.com/oprs-web/" target="_blank" rel="noopener">online.hrtchp.com</a>{L(lang, ".", " पर।")}</p></div>'
                   f'<div class="card"><h3>{L(lang, "Missed the bus?", "बस छूट गई?")}</h3><p>{L(lang, "Shared taxis leave when full, and private taxis charge from about ₹9 per km. In the monsoon, check the weather and road conditions before setting out.", "शेयर्ड टैक्सी भरने पर चलती हैं, और प्राइवेट टैक्सी लगभग ₹9 प्रति किमी से। बरसात में निकलने से पहले मौसम और सड़क की हालत देख लें।")}</p></div>'
                   '</div>', '', 'tips')
    if M:
        fq = [(L(lang, 'What time is the first bus from Mandi to Karsog?', 'मंडी से करसोग की पहली बस कितने बजे है?'),
               L(lang, 'HRTC online booking lists a Mandi to Karsog bus at 4:30 AM (₹285, about 5¾ hours; checked 25 Sep 2026). Other morning buses are reported locally around 6:00 AM, 7:45 AM and 8:30 AM. Confirm at the Mandi bus stand.',
                 'एचआरटीसी ऑनलाइन बुकिंग में मंडी से करसोग की बस सुबह 4:30 बजे है (₹285, लगभग 5¾ घंटे; 25 सितंबर 2026 को देखा गया)। स्थानीय जानकारी के अनुसार सुबह लगभग 6:00, 7:45 और 8:30 बजे भी बसें चलती हैं। मंडी बस अड्डे पर पुष्टि कर लें।')),
              (L(lang, 'What time is the last bus from Karsog to Mandi?', 'करसोग से मंडी की आख़िरी बस कितने बजे है?'),
               L(lang, 'By the timetable board at Karsog bus stand (25 Sep 2026), the last direct HRTC bus to Mandi leaves at 5:15 PM. Earlier buses leave at 9:30 AM, 11:10 AM (via Sorta) and 2:00 PM (via Sorta).',
                 'करसोग बस अड्डे के टाइम-टेबल बोर्ड (25 सितंबर 2026) के अनुसार मंडी की आख़िरी सीधी एचआरटीसी बस शाम 5:15 बजे चलती है। इससे पहले सुबह 9:30, सुबह 11:10 (वाया सोरता) और दोपहर 2:00 बजे (वाया सोरता) बसें हैं।')),
              (L(lang, 'How far is Karsog from Mandi?', 'मंडी से करसोग कितनी दूर है?'),
               L(lang, 'About 99 km by road, about 3¾ hours by car. Buses take about 5 to 6 hours.', 'सड़क से लगभग 99 किमी, गाड़ी से लगभग 3¾ घंटे। बस में लगभग 5 से 6 घंटे लगते हैं।')),
              (L(lang, 'What is the bus fare from Mandi to Karsog?', 'मंडी से करसोग का बस किराया कितना है?'),
               L(lang, 'HRTC online booking showed ₹285 for the 4:30 AM Mandi–Karsog bus and ₹256 for the 11:10 AM Karsog–Mandi bus (25 Sep 2026). Fares change from time to time.',
                 'एचआरटीसी ऑनलाइन बुकिंग में मंडी–करसोग की सुबह 4:30 वाली बस का किराया ₹285 और करसोग–मंडी की सुबह 11:10 वाली बस का ₹256 था (25 सितंबर 2026)। किराया समय-समय पर बदलता है।'))]
    else:
        fq = [(L(lang, 'What time is the bus from Shimla to Karsog?', 'शिमला से करसोग की बस कितने बजे है?'),
               L(lang, 'HRTC online booking lists Shimla ISBT to Karsog buses at 6:30 AM and 2:40 PM (₹278; checked 25 Sep 2026). Manohar Bus Service (private) leaves Shimla ISBT at 11:00 AM.',
                 'एचआरटीसी ऑनलाइन बुकिंग में शिमला आईएसबीटी से करसोग की बसें सुबह 6:30 और दोपहर 2:40 बजे हैं (₹278; 25 सितंबर 2026 को देखा गया)। मनोहर बस सर्विस (प्राइवेट) शिमला आईएसबीटी से सुबह 11:00 बजे चलती है।')),
              (L(lang, 'What time is the first bus from Karsog to Shimla?', 'करसोग से शिमला की पहली बस कितने बजे है?'),
               L(lang, 'The private Manohar bus leaves at 4:40 AM, and the first HRTC bus on the Karsog board leaves at 5:00 AM (via Bagshad, also bookable online).',
                 'प्राइवेट मनोहर बस सुबह 4:40 बजे चलती है, और करसोग बोर्ड पर पहली एचआरटीसी बस सुबह 5:00 बजे है (वाया बगशाड, ऑनलाइन बुकिंग भी)।')),
              (L(lang, 'How far is Karsog from Shimla?', 'शिमला से करसोग कितनी दूर है?'),
               L(lang, 'About 94 km by road from Shimla ISBT via Tattapani, about 3¾ hours by car. Buses take about 5 to 5½ hours.', 'शिमला आईएसबीटी से तत्तापानी होकर सड़क से लगभग 94 किमी, गाड़ी से लगभग 3¾ घंटे। बस में लगभग 5 से 5½ घंटे लगते हैं।')),
              (L(lang, 'Can I break the journey at Tattapani?', 'क्या तत्तापानी में रुककर आगे जा सकते हैं?'),
               L(lang, 'Yes. Many travellers stop at Tattapani for the hot springs and continue on a later bus, but services are few, so check the onward time first.',
                 'हाँ। कई यात्री गर्म पानी के चश्मों के लिए तत्तापानी रुकते हैं और बाद की बस से आगे जाते हैं, पर बसें कम हैं, इसलिए पहले आगे की बस का समय देख लें।'))]
    vids = ''
    if not M:
        import p_guide
        vids = section(shead(L(lang, 'On the way', 'रास्ते में'), L(lang, 'Watch the <em>route</em>', 'रास्ता <em>देखें</em>'),
                             L(lang, 'The Sutlej valley stretch this bus takes, filmed by Karsog Miles. They open on YouTube.', 'यह बस जिस सतलुज घाटी से गुज़रती है, Karsog Miles के वीडियो में। ये यूट्यूब पर खुलते हैं।'))
                       + p_guide.video_cards(['m9gU9HxcJ3c', 'inAT7ixwamk'], lang), 'sec-alt', 'videos')
    body = (t_out + t_in + tips + vids + comments(path.strip('/'), lang, L(lang, 'Is this timing still right?', 'क्या यह समय अब भी सही है?'),
                                                 L(lang, 'Seen a bus change time, stop running or get cancelled? Tell other travellers here.',
                                                   'कोई बस समय बदल गई, बंद हो गई या रद्द हुई? यहाँ दूसरे यात्रियों को बताइए।')) + faq_block(fq, lang))
    nxt = [{'t': t, 'to': C, 'hi': CH, 'u': '', 'p': 0 if w == hrtc else 1} for t, w, n in out_rows]
    return dict(path=path, lang=lang, kind='bus', hero='band',
                title=L(lang, f'{C} to Karsog Bus Timing — HRTC & Private, Both Ways', f'{CH} से करसोग बस का समय — एचआरटीसी व प्राइवेट'),
                desc=L(lang, (f'Mandi ⇄ Karsog bus timings: Karsog to Mandi 9:30 AM, 11:10 AM, 2:00 PM, 5:15 PM; Mandi to Karsog 4:30 AM (online) and more. About 99 km.' if M else
                              f'Shimla ⇄ Karsog bus timings: Shimla to Karsog 6:30 AM, 2:40 PM (HRTC) and 11:00 AM (private); Karsog to Shimla from 4:40 AM. Fare ₹278. About 94 km.'),
                       (f'मंडी ⇄ करसोग बसों का समय: करसोग से मंडी सुबह 9:30, 11:10, दोपहर 2:00, शाम 5:15; मंडी से करसोग सुबह 4:30 (ऑनलाइन) और दूसरी बसें। लगभग 99 किमी।' if M else
                        f'शिमला ⇄ करसोग बसों का समय: शिमला से करसोग सुबह 6:30, दोपहर 2:40 (एचआरटीसी) और सुबह 11:00 (प्राइवेट); करसोग से शिमला सुबह 4:40 से। किराया ₹278। लगभग 94 किमी।')),
                kicker=L(lang, 'Bus timings, both ways', 'बसों का समय, दोनों तरफ़'),
                h1=L(lang, f'{C} ⇄ Karsog <em>buses</em>', f'{CH} ⇄ करसोग <em>बसें</em>'),
                lede=L(lang, f'Every bus between {C} and Karsog we know of: HRTC from the Karsog bus stand board and HRTC’s website, plus private buses.',
                       f'{CH} और करसोग के बीच की हर बस जिसकी हमें जानकारी है: करसोग बस अड्डे के बोर्ड और एचआरटीसी की वेबसाइट से एचआरटीसी बसें, और प्राइवेट बसें।'),
                chips=[('route', L(lang, f'About {km} km', f'लगभग {km} किमी')), ('clock', L(lang, 'Checked 25–27 Sep 2026', '25–27 सितंबर 2026 को देखा गया'))],
                hero_extra='<div class="jump">' + ''.join(f'<a href="#{k}">{v}</a>' for k, v in [
                    ('from-karsog', L(lang, f'Karsog → {C}', f'करसोग → {CH}')), ('to-karsog', L(lang, f'{C} → Karsog', f'{CH} → करसोग'))]) + '</div>',
                crumbs=[(L(lang, 'Karsog bus timings', 'करसोग बस समय'), '/karsog-bus-stand/'), (L(lang, f'{C} ⇄ Karsog', f'{CH} ⇄ करसोग'), path)],
                body=body, ld=[faq_ld(fq)], og='/og/bus.jpg')
