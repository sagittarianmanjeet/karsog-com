"""Drone photos: the /photos/ hub, one page per photographed place, and /rides/ (Karsog Miles ride videos).

Photos, places and captions come from public/photos/photos.json and places.json (made by tools/gallery-build.py on
the Mac); English/Hindi place names from data/photo-places.json, Hindi captions from data/photo-labels-hi.json.
Places that have a written guide (content/) show their photos on the guide page instead of a page of their own."""
import json, math, os, re
from collections import Counter
from layout import L, icon, img, section, shead, comments, esc, href, gallery, pcard, ROOT
from data import (PHOTOS, PLACES, BY_SLUG, PHOTO_PLACES, MON_EN, MON_HI, pbase, place_title, photo_label, photo_alt,
                  TOWN, km, centre, in_karsog)
from p_guide import VIDEOS, video_cards

DIRS = [('north', 'उत्तर'), ('north-east', 'उत्तर-पूर्व'), ('east', 'पूर्व'), ('south-east', 'दक्षिण-पूर्व'),
        ('south', 'दक्षिण'), ('south-west', 'दक्षिण-पश्चिम'), ('west', 'पश्चिम'), ('north-west', 'उत्तर-पश्चिम')]
CHANNEL = 'https://www.youtube.com/@KarsogMiles'


def guide_pages():
    return {f[:-5] for f in os.listdir(os.path.join(ROOT, 'content', 'en')) if f.endswith('.html')}


def where(g, lang):
    """'about 14 km east of Karsog town' — or 'in and around Karsog town'."""
    if not g or km(g, TOWN) < 1.5:
        return L(lang, 'in and around Karsog town', 'करसोग शहर में और आसपास')
    i = int((math.degrees(math.atan2((g[1] - TOWN[1]) * 95, (g[0] - TOWN[0]) * 111.2)) % 360 + 22.5) // 45) % 8
    d = round(km(g, TOWN))
    return L(lang, f'about {d} km {DIRS[i][0]} of Karsog town', f'करसोग शहर से लगभग {d} किमी {DIRS[i][1]} में')


def when(ps, lang, full=False):
    """'Jul 2026' or 'Jun 2026 – Sep 2026' (full=True: 'July 2026', for sentences)."""
    ds = sorted(p['date'] for p in ps)
    M = MON_EN if lang == 'en' else MON_HI
    f = lambda d: (M[int(d[5:7]) - 1][:None if full else 3] if lang == 'en' else M[int(d[5:7]) - 1]) + ' ' + d[:4]
    if ds[0][:7] == ds[-1][:7]:
        return f(ds[0])
    if ds[0][:4] == ds[-1][:4]:                  # same year: 'Jul – Sep 2026'
        return f'{f(ds[0])[:-5]} – {f(ds[-1])}'
    return f'{f(ds[0])} – {f(ds[-1])}'


def page_of(slug):
    return f'/{slug}/'


def cover(slug):
    ps = sorted(BY_SLUG[slug], key=lambda p: p['rank'])
    return ps[0]


def place_card(slug, lang, sizes='(max-width:700px) 50vw, 300px'):
    n = len(BY_SLUG.get(slug, []))
    c = cover(slug)
    return pcard(href(page_of(slug), lang), pbase(c['file']), esc(place_title(slug, lang)),
                 L(lang, f'{n} photo{"s" if n > 1 else ""}', f'{n} फ़ोटो'), sizes=sizes, alt=photo_alt(c, lang))


# ---------------------------------------------------------------- /photos/
def hub(lang):
    order = sorted([p['slug'] for p in PLACES if BY_SLUG.get(p['slug'])], key=lambda s: -len(BY_SLUG[s]))
    n_ph = sum(len(BY_SLUG[s]) for s in order)
    cards = ''.join(place_card(s, lang) for s in order)
    grid = section(shead(L(lang, 'Karsog from above', 'ऊपर से करसोग'),
                         L(lang, f'{n_ph} drone photos, <em>{len(order)} places</em>', f'{len(order)} जगहों की <em>{n_ph} ड्रोन फ़ोटो</em>'),
                         L(lang, 'Aerial photos of Karsog’s villages, temples, fairs and the Satluj valley, taken by Karsog Miles in 2026. Pick a place to see all its photos.',
                           'करसोग के गाँवों, मंदिरों, मेलों और सतलुज घाटी की हवाई फ़ोटो, जो Karsog Miles ने 2026 में लीं। किसी जगह की सभी फ़ोटो देखने के लिए उसे चुनें।'))
                   + f'<div class="grid g4 places-grid">{cards}</div>', '', 'places')
    vids = list(VIDEOS)[:6]
    rides = section(shead(L(lang, 'Karsog Miles', 'Karsog Miles'), L(lang, 'Ride the valley <em>on YouTube</em>', 'यूट्यूब पर <em>घाटी की सैर</em>'),
                          L(lang, 'No commentary, no music: just engine sound and real Himachal roads, filmed through Karsog, Shikari Devi, Janjehli, Tattapani and the hidden lanes in between.',
                            'न कमेंट्री, न संगीत: सिर्फ़ इंजन की आवाज़ और हिमाचल की असली सड़कें, करसोग, शिकारी देवी, जंजैहली, तत्तापानी और बीच की अनजानी गलियों से।'),
                          more=(L(lang, 'All ride videos', 'सभी राइड वीडियो'), href('/rides/', lang)))
                    + video_cards(vids, lang), 'sec-alt', 'videos')
    return dict(path='/photos/', lang=lang, kind='photos', hero='photo',
                title=L(lang, f'Karsog Photos — {n_ph} Drone Photos of {len(order)} Places & Ride Videos', f'करसोग की फ़ोटो — {len(order)} जगहों की {n_ph} ड्रोन फ़ोटो और राइड वीडियो'),
                desc=L(lang, f'{n_ph} aerial drone photos of {len(order)} places around Karsog, Mandi (HP): villages, temples, fairs and the Satluj valley, plus ride videos by Karsog Miles.',
                       f'करसोग (मंडी, हिमाचल) के आसपास {len(order)} जगहों की {n_ph} हवाई ड्रोन फ़ोटो: गाँव, मंदिर, मेले और सतलुज घाटी, साथ में Karsog Miles के राइड वीडियो।'),
                kicker=L(lang, 'Photos', 'फ़ोटो'), h1=L(lang, 'Karsog <em>from above</em>', 'आसमान से <em>करसोग</em>'),
                lede=L(lang, 'Villages, temples, fairs and rivers of the Karsog valley, photographed by drone.',
                       'करसोग घाटी के गाँव, मंदिर, मेले और नदियाँ, ड्रोन से ली गई फ़ोटो में।'),
                img={'src': pbase('karsog-town-001'), 'alt': photo_alt(cover('karsog-town'), lang), 'pos': 'center 50%'},
                chips=[('camera', L(lang, f'{n_ph} photos', f'{n_ph} फ़ोटो')), ('pin', L(lang, f'{len(order)} places', f'{len(order)} जगहें'))],
                crumbs=[(L(lang, 'Photos', 'फ़ोटो'), '/photos/')], body=grid + rides)


# ---------------------------------------------------------------- one page per photographed place
def place(slug, lang):
    meta = PHOTO_PLACES.get(slug, {})
    ps = sorted(BY_SLUG[slug], key=lambda p: p['rank'])
    n, g = len(ps), centre(slug)
    title = place_title(slug, lang)
    sub = L(lang, meta.get('sub', ''), meta.get('sub_hi', ''))
    desc = L(lang, meta.get('desc', ''), meta.get('desc_hi', ''))
    # --- about these photos
    cnt = Counter(photo_label(p, lang) for p in ps)
    name = lambda k: ('the area near ' + k[5:]) if lang == 'en' and k.startswith('Near ') else k
    count = lambda c: L(lang, f' ({c} photo{"s" if c > 1 else ""})', f' ({c} फ़ोटो)') if len(cnt) > 1 else ''
    parts = [name(k) + count(c) for k, c in cnt.most_common()]
    sep = '; ' if any(',' in k for k in cnt) else ', '       # captions like "Nanj - Tundal, Satluj" have commas of their own
    lst = (sep.join(parts[:-1]) + L(lang, ' and ', ' और ') + parts[-1]) if len(parts) > 1 else parts[0]
    about = (L(lang, f'<p>The {n} drone photos on this page show {esc(lst)}.</p>', f'<p>इस पेज की {n} ड्रोन फ़ोटो में {esc(lst)} दिखते हैं।</p>') if n > 1 else
             L(lang, f'<p>The drone photo on this page shows {esc(lst)}.</p>', f'<p>इस पेज पर एक ड्रोन फ़ोटो है: {esc(lst)}।</p>'))
    they = L(lang, 'They were' if n > 1 else 'It was', 'ये फ़ोटो' if n > 1 else 'यह फ़ोटो')
    took = 'लीं' if n > 1 else 'ली'
    by = f'<a href="{CHANNEL}" target="_blank" rel="noopener">Karsog Miles</a>'
    if g:
        about += L(lang, f'<p>{they} taken {where(g, lang)} in a straight line, in {when(ps, lang, True)}, by {by}. Distances are measured from where the drone flew, not by road.</p>',
                   f'<p>{they} {by} ने {when(ps, lang)} में {took}, {where(g, lang)} (सीधी रेखा में)। दूरी वहाँ से मापी गई है जहाँ ड्रोन उड़ा, सड़क से नहीं।</p>')
    else:
        about += L(lang, f'<p>{they} taken in {when(ps, lang, True)} by {by}. '
                         + ('These photos come from video frames' if n > 1 else 'It comes from a video frame') + ' without GPS, so no map location is given.</p>',
                   f'<p>{they} {by} ने {when(ps, lang)} में {took}। '
                   + ('ये वीडियो के फ़्रेम से हैं जिनमें' if n > 1 else 'यह वीडियो के फ़्रेम से है जिसमें') + ' जीपीएस नहीं था, इसलिए नक्शे पर जगह नहीं दी गई है।</p>')
    s_about = section(f'<div class="prose">{about}</div>', 'sec-tight', 'about', 'wrap wrap-n')
    s_gal = section(shead(L(lang, 'From the air', 'आसमान से'), L(lang, f'{n} drone <em>photo{"s" if n > 1 else ""}</em>', f'{n} ड्रोन <em>फ़ोटो</em>'),
                          L(lang, 'Tap a photo to see it full size.', 'फ़ोटो को बड़ा देखने के लिए छुएँ।'))
                    + gallery(ps, lang, lambda p: photo_label(p, lang), lambda p: photo_alt(p, lang)), 'sec-alt', 'photos')
    # --- nearby places (by where the drone flew)
    near = ''
    if g:
        others = sorted([(km(g, centre(s)), s) for s in BY_SLUG if s != slug and centre(s)])[:3]
        near = section(shead(L(lang, 'Nearby', 'आसपास'), L(lang, 'More places <em>from above</em>', 'ऊपर से <em>और जगहें</em>'))
                       + '<div class="grid g3">' + ''.join(place_card(s, lang, '(max-width:700px) 80vw, 380px') for d, s in others) + '</div>'
                       + f'<p class="mt1"><a class="more-link" href="{href("/photos/", lang)}">{L(lang, "All places", "सभी जगहें")} {icon("arrow")}</a></p>',
                       '', 'nearby')
    chips = [('camera', L(lang, f'{n} drone photo{"s" if n > 1 else ""}', f'{n} ड्रोन फ़ोटो')), ('calendar', when(ps, lang))]
    if g:
        chips.insert(1, ('pin', where(g, lang).replace('about ', '~').replace('लगभग ', '~')))
    acts = [(L(lang, 'Open map', 'नक्शा देखें'), f'https://www.google.com/maps?q={g[0]:.4f},{g[1]:.4f}', 'w', 'map')] if g else []
    names = list(dict.fromkeys(re.sub(r'^Near | के पास$', '', photo_label(p, lang)) for p in ps))
    labels = ('; ' if any(',' in x for x in names[:3]) else ', ').join(names[:3]) + (L(lang, ' and more', ' आदि') if len(names) > 3 else '')
    lede = ' '.join(x for x in [(sub[0].upper() + sub[1:] + '.') if sub and lang == 'en' else (sub + '।' if sub else ''), desc] if x)
    ld = [{'@context': 'https://schema.org', '@type': 'ImageGallery', 'name': L(lang, f'{place_title(slug)} — aerial photos', f'{title} — हवाई फ़ोटो'),
           'url': 'https://karsog.com' + href(page_of(slug), lang), 'inLanguage': L(lang, 'en-IN', 'hi-IN'),
           'image': [{'@type': 'ImageObject', 'contentUrl': f'https://karsog.com/photos/{slug}/{p["file"]}-1600.webp', 'caption': photo_alt(p, lang),
                      'creator': {'@type': 'Person', 'name': 'Karsog Miles'}, 'copyrightNotice': 'karsog.com'} for p in ps]}]
    if g:
        ld[0]['contentLocation'] = {'@type': 'Place', 'name': place_title(slug), 'geo': {'@type': 'GeoCoordinates', 'latitude': round(g[0], 4), 'longitude': round(g[1], 4)}}
    c = ps[0]
    return dict(path=page_of(slug), lang=lang, kind='place', hero='photo',
                title=L(lang, f'{title}, Karsog — Aerial Drone Photos', f'{title}, करसोग — ड्रोन से फ़ोटो'),
                desc=L(lang, f'{n} aerial drone photo{"s" if n > 1 else ""} of {labels} — '
                             + ('Karsog, Mandi district' if in_karsog(slug) else 'near Karsog') + f', Himachal Pradesh. Taken {when(ps, lang)}.',
                       f'{labels} की {n} हवाई ड्रोन फ़ोटो — ' + ('करसोग, ज़िला मंडी' if in_karsog(slug) else 'करसोग के पास')
                       + f', हिमाचल प्रदेश। {when(ps, lang)} में ली गईं।'),
                kicker=L(lang, 'Karsog from above', 'ऊपर से करसोग'), h1=esc(title), lede=lede or L(lang, f'Drone photos of {title}, Karsog.', f'{title}, करसोग की ड्रोन फ़ोटो।'),
                img={'src': pbase(c['file']), 'alt': photo_alt(c, lang), 'pos': 'center 50%'},
                chips=chips, actions=acts, crumbs=[(L(lang, 'Photos', 'फ़ोटो'), '/photos/'), (esc(title), page_of(slug))],
                body=s_about + s_gal + near + comments(slug, lang), ld=ld)


def places(lang):
    gp = guide_pages()
    return [place(p['slug'], lang) for p in PLACES if p['slug'] not in gp and BY_SLUG.get(p['slug'])]


# ---------------------------------------------------------------- /rides/
def rides(lang):
    ids = list(VIDEOS)
    top = section(f'<div class="btns"><a class="btn btn-p" href="{CHANNEL}?sub_confirmation=1" target="_blank" rel="noopener">{icon("play")}'
                  f'{L(lang, "Subscribe on YouTube", "यूट्यूब पर सब्सक्राइब करें")}</a>'
                  f'<a class="btn btn-o" href="{CHANNEL}" target="_blank" rel="noopener">{icon("ext")}{L(lang, "Visit the channel", "चैनल देखें")}</a></div>',
                  'sec-tight', 'channel')
    allv = section(shead(L(lang, 'All rides', 'सभी राइड'), L(lang, f'{len(ids)} ride <em>videos</em>', f'{len(ids)} राइड <em>वीडियो</em>'),
                         L(lang, 'Every ride on the Karsog Miles channel, newest first. Tap one to watch it on YouTube.',
                           'Karsog Miles चैनल की हर राइड, सबसे नई पहले। देखने के लिए किसी वीडियो को छुएँ, वह यूट्यूब पर खुलेगा।'))
                   + video_cards(ids, lang), 'sec-alt', 'all')
    return dict(path='/rides/', lang=lang, kind='rides', hero='band',
                title=L(lang, 'Karsog Ride Videos — Karsog Miles on YouTube', 'करसोग राइड वीडियो — यूट्यूब पर Karsog Miles'),
                desc=L(lang, 'Ride videos from the Karsog valley by Karsog Miles: Shikari Devi, Janjehli, Mahunag, Chindi, Tattapani and the hidden roads in between. No commentary, no music.',
                       'Karsog Miles के करसोग घाटी के राइड वीडियो: शिकारी देवी, जंजैहली, माहूँनाग, चिंडी, तत्तापानी और बीच की अनजानी सड़कें। न कमेंट्री, न संगीत।'),
                kicker=L(lang, 'Karsog Miles', 'Karsog Miles'), h1=L(lang, 'The valley, <em>as the road sees it</em>', 'सड़क की नज़र से <em>घाटी</em>'),
                lede=L(lang, 'No commentary, no music, no distractions: just engine sound, changing weather and real Himachal roads. Karsog Miles films the routes this site describes. New rides upload regularly.',
                       'न कमेंट्री, न संगीत, न कोई शोर: सिर्फ़ इंजन की आवाज़, बदलता मौसम और हिमाचल की असली सड़कें। Karsog Miles उन्हीं रास्तों को फ़िल्माता है जिनके बारे में यह साइट बताती है। नई राइड लगातार आती रहती हैं।'),
                chips=[('play', L(lang, f'{len(ids)} videos', f'{len(ids)} वीडियो'))],
                crumbs=[(L(lang, 'Photos', 'फ़ोटो'), '/photos/'), (L(lang, 'Ride videos', 'राइड वीडियो'), '/rides/')], body=top + allv)
