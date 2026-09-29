"""Melas & festivals (/melas/) and the temples of Karsog (/temples/, which replaces the old /devtas/).

Fairs come from MELAS in data.py; temples from data/devtas.json (English) and data/devtas-hi.json (Hindi).
Dates that follow the Hindu calendar move every year, so each fair shows its usual time, its dates in
2024–2026 and the expected date in 2027. Beliefs and legends are always written as beliefs."""
import json, os
from layout import L, icon, img, section, shead, faq_block, faq_ld, comments, note, esc, href, ROOT
from data import MELAS, MON_EN, MON_HI, hi_date, GUIDES, pbase, photo, photo_alt

DEV = json.load(open(os.path.join(ROOT, 'data', 'devtas.json'), encoding='utf-8'))
DEV_HI = json.load(open(os.path.join(ROOT, 'data', 'devtas-hi.json'), encoding='utf-8'))
ORDER = ['mahunag', 'mamleshwar', 'kamaksha', 'shikari_devi', 'kamrunag', 'chindi', 'pangna', 'laxmi_narayan', 'chawasi', 'dhamuni']
GUIDE = {'mahunag': '/mahunag/', 'mamleshwar': '/mamleshwar/', 'kamaksha': '/kao/', 'shikari_devi': '/shikari-devi/',
         'kamrunag': '/kamru-nag/', 'chindi': '/chindi/', 'pangna': '/pangna-fort/'}
# drone photo for each temple card (None: no photo of that temple yet; the Chindi photos show the PWD rest house)
PHOTO = {'mahunag': 'mahunag-214', 'mamleshwar': 'mamleshwar-322', 'kamaksha': 'kao-326', 'shikari_devi': 'shikari-devi-005',
         'kamrunag': None, 'chindi': None, 'pangna': 'pangna-fort-244', 'laxmi_narayan': 'karsog-town-206',
         'chawasi': 'pokhi-mahog-212', 'dhamuni': 'seri-bunglow-034'}


# ---------------------------------------------------------------- /melas/
def _years(x, lang):
    past = [(y, d) for y, d in zip(('2024', '2025', '2026'), x['years']) if d]
    if lang == 'en':
        s = ('Dates by year: ' + ' · '.join(f'{y}: {esc(d)}' for y, d in past) + ' · ') if past else ''
        return s + f'2027: <b>{esc(x["next"])}</b>'
    s = ('हर साल की तारीख़ें: ' + ' · '.join(f'{y}: {esc(hi_date(d))}' for y, d in past) + ' · ') if past else ''
    return s + f'2027: <b>{esc(hi_date(x["next"]))}</b>'


def melas(lang):
    hl = lambda p: href(p, lang)
    months = [m for m in range(1, 13) if any(x['m'] == m for x in MELAS)]
    chips = ''.join(f'<a href="#m{m}" data-m="{m}">{L(lang, MON_EN[m - 1][:3], MON_HI[m - 1])}</a>' for m in months)
    tl = ''
    for m in months:
        evs = ''
        for x in [x for x in MELAS if x['m'] == m]:
            name, alt = L(lang, x['en'], x['hi']), L(lang, x['hi'], x['en'])
            more = (f'<p class="mt0"><a class="more-link" href="{hl(x["link"])}">{L(lang, "More about it", "पूरी जानकारी")} {icon("arrow")}</a></p>'
                    if x['link'] else '')
            evs += (f'<article class="ev"><h4>{esc(name)}<span class="alt" lang="{L(lang, "hi", "en")}">{esc(alt)}</span></h4>'
                    f'<div class="meta"><span>{icon("pin")}{esc(L(lang, x["place"], x["place_hi"]))}</span>'
                    f'<span>{icon("calendar")}{esc(L(lang, x["usual"], x["usual_hi"]))}</span>'
                    f'<span>{icon("clock")}{esc(L(lang, x["rule"], x["rule_hi"]))}</span></div>'
                    f'<p>{esc(L(lang, x["what"], x["what_hi"]))}</p><div class="yrs">{_years(x, lang)}</div>{more}</article>')
        tl += f'<div class="tl-m" id="m{m}" data-m="{m}"><h3>{L(lang, MON_EN[m - 1], MON_HI[m - 1])}</h3>{evs}</div>'
    cal = section(
        shead(L(lang, 'Fair calendar', 'मेलों का कैलेंडर'), L(lang, 'Month <em>by month</em>', 'महीने <em>दर महीने</em>'))
        + note(L(lang, 'Many dates follow the Hindu calendar and move a little every year, and a few fairs are not held every year, '
                     'so check locally before you travel. Visitors are welcome at all of them.',
               'कई तारीख़ें हिंदू पंचांग के हिसाब से हर साल थोड़ी आगे-पीछे होती हैं, और कुछ मेले हर साल नहीं होते, '
               'इसलिए जाने से पहले स्थानीय लोगों से पता कर लें। सभी मेलों में यात्रियों का स्वागत है।'))
        + f'<nav class="months mt2" aria-label="{L(lang, "Jump to a month", "महीना चुनें")}">{chips}</nav>'
        + f'<div class="tl mt1">{tl}</div>'
        + f'<p class="mt2">{L(lang, "See also", "यह भी देखें")}: <a href="{hl("/temples/")}">{L(lang, "Temples of Karsog", "करसोग के मंदिर")}</a>. '
          f'{L(lang, "Know a date we’ve missed?", "कोई तारीख़ छूट गई है?")} <a href="#update" data-open="upd">{L(lang, "Tell us", "हमें बताएँ")}</a>.</p>',
        '', 'calendar', 'wrap wrap-n')
    fq = [(L(lang, 'When is the Nalwar Mela in Karsog?', 'करसोग में नलवाड़ मेला कब लगता है?'),
           L(lang, 'The Nalwar Mela is usually held on 5–11 April in Karsog town, in the years it takes place. It opens with a procession of Mamleshwar Mahadev. It was not held in 2024.',
             'नलवाड़ मेला आम तौर पर करसोग शहर में 5–11 अप्रैल को लगता है, जिन सालों में यह होता है। इसकी शुरुआत ममलेश्वर महादेव की शोभायात्रा से होती है। 2024 में यह नहीं हुआ था।')),
          (L(lang, 'When is the Mahunag Mela?', 'माहूँनाग मेला कब लगता है?'),
           L(lang, 'The Shri Mool Mahunag Mela is held in mid-May, usually about 14–19 May, at Mahunag (Bakhari Kothi).',
             'श्री मूल माहूँनाग मेला मई के बीच में, आम तौर पर लगभग 14–19 मई को, माहूँनाग (बखारी कोठी) में लगता है।')),
          (L(lang, 'What is Budhi Diwali?', 'बूढ़ी दिवाली क्या है?'),
           L(lang, 'Budhi Diwali is the hill Diwali, celebrated about a month after the main Diwali. In Karsog it is held at Mamleshwar Mahadev and at Mahog. In 2027 it is expected around 28 November.',
             'बूढ़ी दिवाली पहाड़ों की दिवाली है, जो मुख्य दिवाली के लगभग एक महीने बाद मनाई जाती है। करसोग में यह ममलेश्वर महादेव और महोग में मनाई जाती है। 2027 में इसके लगभग 28 नवंबर को होने की उम्मीद है।'))]
    ld = [faq_ld(fq)]
    return dict(path='/melas/', lang=lang, kind='melas', hero='band',
                title=L(lang, 'Karsog Melas & Festivals — Fair Dates Month by Month', 'करसोग के मेले और त्योहार — महीने के हिसाब से तारीख़ें'),
                desc=L(lang, 'Karsog fairs and festivals calendar: Lohri at Tattapani, Nalwar Mela, Mahunag Mela, Kamru Nag Mela, Chindi Mata Mela, Navratri and Budhi Diwali, with dates.',
                       'करसोग के मेलों और त्योहारों का कैलेंडर: तत्तापानी की लोहड़ी, नलवाड़ मेला, माहूँनाग मेला, कमरूनाग मेला, चिंडी माता मेला, नवरात्रि और बूढ़ी दिवाली, तारीख़ों के साथ।'),
                kicker=L(lang, 'Karsog through the year', 'करसोग, पूरे साल'), h1=L(lang, 'Melas &amp; <em>festivals</em>', 'मेले और <em>त्योहार</em>'),
                lede=L(lang, 'The fairs and festivals worth planning a trip around: where, when and what happens.',
                       'वे मेले और त्योहार, जिनके हिसाब से यात्रा की योजना बनाई जा सकती है: कहाँ, कब और क्या होता है।'),
                chips=[('calendar', L(lang, f'{len(MELAS)} fairs through the year', f'साल भर में {len(MELAS)} मेले'))],
                crumbs=[(L(lang, 'Melas', 'मेले'), '/melas/')],
                body=cal + comments('melas', lang, None, L(lang, 'Been to one of these fairs? Share the dates for this year or a correction.',
                                                              'इनमें से किसी मेले में गए हैं? इस साल की तारीख़ें या कोई सुधार लिखें।')) + faq_block(fq, lang),
                ld=ld)


# ---------------------------------------------------------------- /temples/
def _lis(xs):
    return '<ul>' + ''.join(f'<li>{esc(x)}</li>' for x in xs) + '</ul>'


def temple_card(slug, lang):
    en, hi = DEV[slug], DEV_HI[slug]
    name, alt = L(lang, en['name_en'], hi['name']), L(lang, hi['name'], en['name_en'])
    d = en if lang == 'en' else hi
    ph = ''
    if PHOTO.get(slug):
        # alt text from the photo's own caption, so it says only what the photo shows
        ph = f'<div class="ph">{img(pbase(PHOTO[slug]), photo_alt(photo(PHOTO[slug]), lang), "(max-width:700px) 92vw, 460px")}</div>'
    story = f'<p class="story"><i>{esc(d["story"])}</i></p>' if d.get('story') else ''
    fairs = [f'{a}: {b}' for a, b in d.get('fairs', [])]
    guide = (f'<p class="mt0"><a class="more-link" href="{href(GUIDE[slug], lang)}">{L(lang, "Full guide", "पूरी गाइड")} {icon("arrow")}</a></p>'
             if slug in GUIDE else '')
    return (f'<article class="mcard temple" id="{slug}">{ph}<div class="bd">'
            f'<h3>{esc(name)}<small lang="{L(lang, "hi", "en")}">{esc(alt)}</small></h3>'
            f'<div class="meta"><span>{icon("pin")}{esc(d["place"])}</span></div>'
            f'<p>{esc(d["about"])}</p>{story}'
            + (f'<h4>{L(lang, "When to go", "कब जाएँ")}</h4>{_lis(d["when"])}' if d.get('when') else '')
            + (f'<h4>{L(lang, "Fairs", "मेले")}</h4>{_lis(fairs)}' if fairs else '')
            + (f'<h4>{L(lang, "Tips", "सुझाव")}</h4>{_lis(d["tips"])}' if d.get('tips') else '')
            + guide + '</div></article>')


def temples(lang):
    hl = lambda p: href(p, lang)
    chips = ''.join(f'<a href="#{s}">{esc(L(lang, DEV[s]["name_en"], DEV_HI[s]["name"]).split(",")[0].replace(" Temple", "").replace(" मंदिर", ""))}</a>'
                    for s in ORDER)
    intro = section(
        f'<p class="statement">{L(lang, "Karsog is known as a valley of temples. Most are built in the old Himachali style of carved wood and stone, and each village has its own <em>devta</em>.", "करसोग को मंदिरों की घाटी कहा जाता है। ज़्यादातर मंदिर नक्काशीदार लकड़ी और पत्थर की पुरानी हिमाचली शैली में बने हैं, और हर गाँव का अपना <em>देवता</em> है।")}</p>'
        f'<p class="mt1">{L(lang, "These are the temples most worth visiting, with the story behind each, the best time to go and a few tips. Stories and legends are told here as local people tell them.", "ये वे मंदिर हैं जहाँ जाना सबसे ज़्यादा सार्थक है, हर एक की कथा, जाने के सही समय और कुछ सुझावों के साथ। कथाएँ और मान्यताएँ यहाँ वैसे ही लिखी गई हैं, जैसे स्थानीय लोग सुनाते हैं।")}</p>'
        f'<nav class="months mt1" aria-label="{L(lang, "Jump to a temple", "मंदिर चुनें")}">{chips}</nav>', 'sec-tight', 'intro', 'wrap wrap-n')
    cards = ''.join(temple_card(s, lang) for s in ORDER if s in DEV)
    grid = section(shead(L(lang, 'Temple by temple', 'एक-एक मंदिर'), L(lang, f'{len(ORDER)} temples <em>to visit</em>', f'देखने लायक <em>{len(ORDER)} मंदिर</em>'))
                   + f'<div class="grid g2 temples">{cards}</div>'
                   + f'<p class="mt2">{L(lang, "Fair dates", "मेलों की तारीख़ें")}: <a href="{hl("/melas/")}">{L(lang, "melas &amp; festivals", "मेले और त्योहार")}</a>. '
                     f'{L(lang, "Something wrong or missing?", "कुछ ग़लत है या छूट गया है?")} <a href="#update" data-open="upd">{L(lang, "Tell us", "हमें बताएँ")}</a>.</p>',
                   'sec-alt', 'temples')
    fq = [(L(lang, 'Which is the most famous temple in Karsog?', 'करसोग का सबसे प्रसिद्ध मंदिर कौन-सा है?'),
           L(lang, 'The Shri Mool Mahunag temple at Bakhari Kothi, about 26 km from Karsog, where Mahunag is worshipped as Karna. It hosts the valley’s biggest fair in mid-May.',
             'बखारी कोठी का श्री मूल माहूँनाग मंदिर, करसोग से लगभग 26 किमी, जहाँ माहूँनाग की पूजा कर्ण के रूप में होती है। मई के बीच में यहाँ घाटी का सबसे बड़ा मेला लगता है।')),
          (L(lang, 'Which temples can I see in one day from Karsog?', 'करसोग से एक दिन में कौन-से मंदिर देख सकते हैं?'),
           L(lang, 'Mamleshwar Mahadev at Mamel, Kamaksha Devi at Kao and Mahunag make a good one-day temple circuit, back in Karsog by evening.',
             'ममेल में ममलेश्वर महादेव, काओ में कामाक्षा देवी और माहूँनाग मिलकर एक दिन का अच्छा मंदिर-सफ़र बनाते हैं, और शाम तक करसोग वापस।')),
          (L(lang, 'Why does the Shikari Devi temple have no roof?', 'शिकारी देवी मंदिर की छत क्यों नहीं है?'),
           L(lang, 'Local people believe the goddess does not want a roof and that every attempt to build one has failed.',
             'स्थानीय लोग मानते हैं कि देवी छत नहीं चाहतीं और छत बनाने की हर कोशिश नाकाम रही है।'))]
    return dict(path='/temples/', lang=lang, kind='temples', hero='band',
                title=L(lang, 'Temples of Karsog — Mahunag, Mamleshwar, Kamaksha, Shikari Devi', 'करसोग के मंदिर — माहूँनाग, ममलेश्वर, कामाक्षा, शिकारी देवी'),
                desc=L(lang, 'Karsog temples worth visiting: Mahunag, Mamleshwar Mahadev, Kamaksha Devi, Shikari Devi, Kamru Nag, Chindi Mata and Pangna Mahamaya — the story, when to go, tips.',
                       'करसोग के देखने लायक मंदिर: माहूँनाग, ममलेश्वर महादेव, कामाक्षा देवी, शिकारी देवी, कमरूनाग, चिंडी माता और पांगणा की महामाया, कथा, सही समय और सुझावों के साथ।'),
                kicker=L(lang, 'Valley of temples', 'मंदिरों की घाटी'), h1=L(lang, 'Temples of <em>Karsog</em>', 'करसोग के <em>मंदिर</em>'),
                lede=L(lang, 'The temples most worth visiting in the valley: the story behind each, when to go and tips for your visit.',
                       'घाटी के सबसे देखने लायक मंदिर: हर एक की कथा, कब जाएँ और दर्शन के लिए सुझाव।'),
                chips=[('temple', L(lang, f'{len(ORDER)} temples', f'{len(ORDER)} मंदिर')), ('calendar', L(lang, 'Fair dates on each', 'हर मंदिर के मेलों की तारीख़ें'))],
                crumbs=[(L(lang, 'Temples', 'मंदिर'), '/temples/')],
                body=intro + grid + comments('temples', lang) + faq_block(fq, lang), ld=[faq_ld(fq)])
