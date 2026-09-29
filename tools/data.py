"""Shared data for every karsog.com page: buses, fairs, photos, distances.

The bus timetables come from data/*.csv; fairs are in MELAS below; photos in public/photos/photos.json.
Hindi spellings follow the ones people in Karsog use most (see docs/hindi-glossary.md)."""
import csv, json, math, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, 'public')
KARSOG = (31.3830, 77.2000)          # Karsog bus stand area
CHECKED = '25 Sep 2026'               # date the HRTC board was photographed
CHECKED_HI = '25 सितंबर 2026'
P_CHECKED = '27 Sep 2026'
P_CHECKED_HI = '27 सितंबर 2026'

MON_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
MON_HI = ['जनवरी', 'फ़रवरी', 'मार्च', 'अप्रैल', 'मई', 'जून', 'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर']


# ------------------------------------------------------------------ time formats
def clock(t, lang='en'):
    """'17:15' -> '5:15 PM' (English) or 'शाम 5:15' (Hindi)."""
    h, m = map(int, t.split(':'))
    h12 = h % 12 or 12
    if lang == 'en':
        return f'{h12}:{m:02d} {"AM" if h < 12 else "PM"}'
    part = 'सुबह' if 4 <= h < 12 else 'दोपहर' if 12 <= h < 16 else 'शाम' if 16 <= h < 19 else 'रात'
    return f'{part} {h12}:{m:02d}'


def hi_date(s):
    """Short English date strings used in MELAS ('13–15 Jan', 'from 14 May', '~5 Sep') in Hindi."""
    if not s:
        return s
    x = s
    for i, m in enumerate(MON_EN):
        x = re.sub(r'\b' + m[:3] + r'[a-z]*\b', MON_HI[i], x)
    x = x.replace('Not held', 'नहीं हुआ').replace(', if held', ', अगर हुआ तो').replace('expected early Dec', 'दिसंबर की शुरुआत में संभावित')
    x = x.replace('expected early दिसंबर', 'दिसंबर की शुरुआत में संभावित')
    x = re.sub(r'^from (.*)$', r'\1 से', x)
    x = x.replace('~', 'लगभग ').replace('Sept–Oct', 'सितंबर–अक्टूबर').replace('Mid-June', 'जून के बीच').replace('March–April', 'मार्च–अप्रैल')
    return x


# ------------------------------------------------------------------ HRTC departures (timetable board at Karsog bus stand)
# key = (line, sr) -> (destination, Hindi, page slug or None, note in English, note in Hindi)
L1, L2, L3 = 'Karsog-Churag-Tattapani', 'Karsog-Pangna-Mandi', 'Karsog-Kelodhar'
LINE = {L1: ('Karsog–Churag–Tattapani line', 'करसोग–चुराग–तत्तापानी रूट'),
        L2: ('Karsog–Pangna–Mandi line', 'करसोग–पांगणा–मंडी रूट'),
        L3: ('Karsog–Kelodhar line', 'करसोग–केलोधार रूट')}
D = {}


def _d(line, sr, name, hi, slug, note='', note_hi=''):
    D[(line, str(sr))] = (name, hi, slug, note, note_hi)


_d(L1, 1, 'Shimla', 'शिमला', 'shimla', 'via Bagshad', 'वाया बगशाड')
_d(L1, 2, 'Shimla', 'शिमला', 'shimla'); _d(L1, 3, 'Shimla', 'शिमला', 'shimla')
_d(L1, 4, 'Shimla', 'शिमला', 'shimla', 'via Bagshad; bus starts at Janjehli', 'वाया बगशाड; बस जंजैहली से आती है')
_d(L1, 5, 'Shri Mool Mahunag', 'श्री मूल माहूनाग', 'mahunag')
_d(L1, 6, 'Haridwar', 'हरिद्वार', 'haridwar'); _d(L1, 7, 'Salana', 'सलाणा', 'salana'); _d(L1, 8, 'Shimla', 'शिमला', 'shimla')
_d(L1, 9, 'Shimla', 'शिमला', 'shimla', 'via Bagshad', 'वाया बगशाड')
_d(L1, 10, 'Shri Mool Mahunag', 'श्री मूल माहूनाग', 'mahunag', 'Mandi-based bus', 'मंडी डिपो की बस')
_d(L1, 11, 'Parlog', 'परलोग', 'parlog'); _d(L1, 12, 'Rodidhar', 'रोड़ीधार', 'rodidhar'); _d(L1, 13, 'Shalani', 'शलानी', 'shalani')
_d(L1, 14, 'Delhi', 'दिल्ली', 'delhi'); _d(L1, 15, 'Salana', 'सलाणा', 'salana')
_d(L2, 1, None, None, None, 'destination covered on the board', 'बोर्ड पर मंज़िल ढकी हुई है')
_d(L2, 2, 'Gahidhar', 'गहीधार', 'gahidhar', 'via Sorta', 'वाया सोरता')
_d(L2, 3, 'Mandi', 'मंडी', 'mandi')
_d(L2, 4, 'Dharamshala', 'धर्मशाला', 'dharamshala', 'bus starts at Jyuri', 'बस ज्यूरी से आती है')
_d(L2, 5, 'Mandi', 'मंडी', 'mandi', 'via Sorta; bus starts at Shri Mool Mahunag', 'वाया सोरता; बस श्री मूल माहूनाग से आती है')
_d(L2, 6, 'Rewalsar', 'रिवालसर', 'rewalsar', 'bus starts at Rampur', 'बस रामपुर से आती है')
_d(L2, 7, 'Mandi', 'मंडी', 'mandi', 'via Sorta; bus starts at Reckong Peo', 'वाया सोरता; बस रिकांगपिओ से आती है')
_d(L2, 8, 'Khaniudi', 'खनीऊडी', 'khaniudi')
_d(L2, 9, 'Nihri', 'निहरी', 'nihri', 'via Sorta', 'वाया सोरता'); _d(L2, 10, 'Sarcha', 'सरचा', 'sarcha')
_d(L2, 11, 'Sarhi', 'सरही', 'sarhi', 'via Sorta', 'वाया सोरता'); _d(L2, 12, 'Mandi', 'मंडी', 'mandi')
_d(L2, 13, None, None, None, 'destination partly covered on the board', 'बोर्ड पर मंज़िल आधी ढकी है')
_d(L2, 14, 'Dharamshala', 'धर्मशाला', 'dharamshala', 'bus starts at Reckong Peo', 'बस रिकांगपिओ से आती है')
_d(L2, 15, 'Jahalma', 'जाहलमा', 'jahalma', 'bus starts at Reckong Peo', 'बस रिकांगपिओ से आती है')
_d(L3, 1, None, None, None, 'destination partly covered on the board', 'बोर्ड पर मंज़िल आधी ढकी है')
_d(L3, 2, 'Reckong Peo', 'रिकांगपिओ', 'reckong-peo', 'bus starts at Dharamshala', 'बस धर्मशाला से आती है')
_d(L3, 3, 'Rampur', 'रामपुर', 'rampur'); _d(L3, 4, 'Thunag', 'थुनाग', 'thunag')
_d(L3, 5, None, None, None, 'destination covered on the board', 'बोर्ड पर मंज़िल ढकी हुई है')
_d(L3, 6, 'Reckong Peo', 'रिकांगपिओ', 'reckong-peo', 'bus starts at Mandi', 'बस मंडी से आती है')
_d(L3, 7, None, None, None, 'destination covered on the board', 'बोर्ड पर मंज़िल ढकी हुई है')
_d(L3, 8, 'Gada Gushaini', 'गाड़ागुशैणी', 'gada-gushaini'); _d(L3, 9, 'Somakothi', 'सोमाकोठी', 'somakothi')
_d(L3, 10, 'Rampur', 'रामपुर', 'rampur', 'bus starts at Rewalsar', 'बस रिवालसर से आती है')
_d(L3, 11, 'Syanj', 'स्यांज', 'syanj'); _d(L3, 12, 'Tharmi', 'थर्मी', 'tharmi')
_d(L3, 13, 'Mundu', 'मुंडू', 'mundu'); _d(L3, 14, 'Dateha', 'दटेहा', 'dateha')
_d(L3, 15, 'Shri Dev Dwahad', 'श्री देव दवाहड़', 'dev-dwahad')
_d(L3, 16, 'Pokhi', 'पोखी', 'pokhi'); _d(L3, 17, 'Syanjali', 'स्यांजली', 'syanjali'); _d(L3, 18, 'Mahavan', 'महावन', 'mahavan')
_d(L3, 19, 'Reckong Peo', 'रिकांगपिओ', 'reckong-peo', 'bus starts at Jahalma', 'बस जाहलमा से आती है')
EXISTING = {'shimla': '/shimla-to-karsog-bus/', 'mandi': '/mandi-to-karsog-bus/'}


def bus_url(slug):
    return EXISTING.get(slug, f'/bus/karsog-to-{slug}/')


HRTC = []
for r in csv.DictReader(open(os.path.join(ROOT, 'data', 'karsog-bus-stand-board.csv'), encoding='utf-8')):
    name, hi, slug, note, note_hi = D[(r['line'], r['sr'])]
    extra = ''   # the CSV note describes the board itself (covered, handwritten); not shown to travellers
    HRTC.append(dict(line=r['line'], sr=int(r['sr']), time=r['departure'], route_hi=r['route_hindi'], route_en=r['route_english'],
                     unit=r['unit'], dest=name, dest_hi=hi, slug=slug,
                     note='; '.join(x for x in [note, extra] if x), note_hi='; '.join(x for x in [note_hi, extra] if x)))
HRTC.sort(key=lambda x: x['time'])

PRIVATE = list(csv.DictReader(open(os.path.join(ROOT, 'data', 'karsog-private-buses.csv'), encoding='utf-8')))
for r in PRIVATE:
    r['op'] = r['operator'].split(' (')[0]
P_DEP = sorted([r for r in PRIVATE if r['karsog_kind'] == 'dep' and r['karsog_time']], key=lambda r: r['karsog_time'])

# Hindi names for private-bus destinations and operators
PLACE_HI = {'Shimla ISBT': 'शिमला आईएसबीटी', 'Shimla': 'शिमला', 'Mandi': 'मंडी', 'Sundernagar': 'सुंदरनगर', 'Rampur': 'रामपुर',
            'Hamirpur': 'हमीरपुर', 'Syanj Bagra': 'स्यांज बगड़ा', 'Ani': 'आनी', 'Karsog': 'करसोग', 'Tattapani': 'तत्तापानी',
            'Pangna': 'पांगणा', 'Chindi': 'चिंडी', 'Churag': 'चुराग', 'Kelodhar': 'केलोधार', 'Mahunag': 'माहूँनाग',
            'Shri Mool Mahunag': 'श्री मूल माहूँनाग', 'Chandigarh': 'चंडीगढ़', 'Bilaspur': 'बिलासपुर', 'Solan': 'सोलन',
            'Nihri': 'निहरी', 'Sorta': 'सोरता', 'Jachh': 'जाच्छ', 'Charkhari': 'चरखड़ी', 'Kamaksha': 'कामाक्षा', 'Bagshad': 'बगशाड',
            'Somakothi': 'सोमाकोठी', 'Chhatri': 'छतरी', 'Luhri': 'लुहरी', 'Sainj': 'सैंज', 'Jyuri': 'ज्यूरी', 'Rohanda': 'रोहांडा',
            'Sanarli': 'सनारली', 'Kao': 'काओ', 'Mamel': 'ममेल', 'Bakhari Kothi': 'बखारी कोठी', 'Brahog': 'ब्राहोग', 'Karol': 'करोल',
            'Dogri': 'डोगरी', 'Mehandi': 'मेहंदी', 'Takrol': 'टकरोल', 'Jhungi': 'झुंगी', 'Arki': 'अर्की', 'Kamaksha Mata': 'कामाक्षा माता',
            'Dharmod': 'धरमोड़', 'Jahu': 'जाहू', 'Bithri': 'बिठरी', 'Sunni': 'सुन्नी', 'Nerchowk': 'नेरचौक', 'Katol': 'कटोल',
            'Chaira': 'चैरा', 'Shankardehra': 'शंकरदेहरा', 'Raigarh': 'रायगढ़', 'Lalag': 'लालग', 'Janjehli': 'जंजैहली', 'Delhi': 'दिल्ली',
            'Haridwar': 'हरिद्वार', 'Reckong Peo': 'रिकांगपिओ', 'Dharamshala': 'धर्मशाला', 'Rewalsar': 'रिवालसर', 'Thunag': 'थुनाग'}
for _v in D.values():
    if _v[0]:
        PLACE_HI.setdefault(_v[0], _v[1])
PLACE_HI.update({'Salana': 'सलाणा', 'Syanj': 'स्यांज', 'Kotlu': 'कोटलू', 'Nanj': 'नांज', 'Mahog': 'महोग', 'Pokhi': 'पोखी'})


def hi_places(text):
    """Translate place names inside a route or stops string ('Karsog – Shimla', 'Churag 16:25 · Pangna 17:25')."""
    for en in sorted(PLACE_HI, key=len, reverse=True):
        text = re.sub(r'\b' + re.escape(en) + r'\b', PLACE_HI[en], text)
    return re.sub(r'(\d{1,2}):(\d{2})', lambda m: m.group(0), text)


def next_bus_json(lang_rows='all'):
    """Departures for the live next-bus boards: [{t, to, hi, u, p}]."""
    out = [{'t': b['time'], 'to': b['dest'] or 'see board', 'hi': b['dest_hi'] or 'बोर्ड देखें',
            'u': bus_url(b['slug']) if b['slug'] else ''} for b in HRTC]
    if lang_rows == 'all':
        out += [{'t': r['karsog_time'], 'to': r['to'], 'hi': PLACE_HI.get(r['to'], r['to']), 'u': '/karsog-private-bus/', 'p': 1}
                for r in P_DEP]
    return sorted(out, key=lambda x: x['t'])


# ------------------------------------------------------------------ fairs and festivals
# m = month, en/hi = name, place, usual (when), rule, years = (2024, 2025, 2026), next = 2027, what, link
def _m(m, en, hi, place, place_hi, usual, usual_hi, rule, rule_hi, years, nxt, what, what_hi, link):
    return dict(m=m, en=en, hi=hi, place=place, place_hi=place_hi, usual=usual, usual_hi=usual_hi, rule=rule, rule_hi=rule_hi,
                years=years, next=nxt, what=what, what_hi=what_hi, link=link)


MELAS = [
    _m(1, 'Lohri & Makar Sankranti Mela', 'लोहड़ी व मकर संक्रांति मेला', 'Tattapani', 'तत्तापानी', '13–15 January', '13–15 जनवरी',
       'Fixed dates', 'तय तारीख़ें', ('13–14 Jan', '13–15 Jan', '13–15 Jan'), '~14–16 Jan',
       'People take a holy dip in the hot springs beside the Sutlej. There are stalls, swings and cultural evenings on the river bank.',
       'लोग सतलुज किनारे गर्म पानी के चश्मों में पवित्र स्नान करते हैं। नदी किनारे दुकानें, झूले और सांस्कृतिक संध्याएँ होती हैं।', '/tattapani/'),
    _m(2, 'Mahashivratri', 'महाशिवरात्रि', 'Mamleshwar Mahadev, Mamel (Karsog)', 'ममलेश्वर महादेव, ममेल (करसोग)', 'February or March',
       'फ़रवरी या मार्च', 'Hindu calendar', 'हिंदू पंचांग के अनुसार', ('8 Mar', '26 Feb', '15 Feb'), '6 Mar',
       'Night-long worship and a community meal (bhandara) at Karsog’s ancient Shiva temple.',
       'करसोग के प्राचीन शिव मंदिर में रात भर पूजा और भंडारा।', '/mamleshwar/'),
    _m(3, 'Chaitra Navratri', 'चैत्र नवरात्रि', 'Kamaksha Devi (Kao), Shikari Devi and other goddess temples',
       'कामाक्षा देवी (काओ), शिकारी देवी और देवी के दूसरे मंदिर', 'March–April, nine days', 'मार्च–अप्रैल, नौ दिन',
       'Hindu calendar', 'हिंदू पंचांग के अनुसार', ('', '', ''), 'March–April',
       'The busiest time at the valley’s goddess temples, with special worship every day.',
       'घाटी के देवी मंदिरों में सबसे ज़्यादा रौनक का समय, हर दिन विशेष पूजा।', '/temples/#kamaksha'),
    _m(4, 'Nalwar Mela', 'नलवाड़ मेला', 'Karsog town', 'करसोग शहर', '5–11 April', '5–11 अप्रैल',
       'Fixed dates, but not held every year', 'तय तारीख़ें, पर हर साल नहीं होता', ('Not held', '5–11 Apr', '5–11 Apr'), '5–11 Apr, if held',
       'Karsog’s biggest spring fair. It opens with a procession of Mamleshwar Mahadev, followed by a week of stalls, sports and cultural evenings. It was not held in 2024.',
       'करसोग का वसंत का सबसे बड़ा मेला। शुरुआत ममलेश्वर महादेव की शोभायात्रा से होती है, फिर एक हफ़्ते तक दुकानें, खेल और सांस्कृतिक संध्याएँ। 2024 में यह मेला नहीं हुआ था।',
       '/mamleshwar/'),
    _m(5, 'Chawasi Utsav', 'च्वासी उत्सव', 'Nahvindhar, Chawasi area', 'नाहवींधार, च्वासी क्षेत्र', '12–15 May', '12–15 मई',
       'Fixed dates', 'तय तारीख़ें', ('12–15 May', '12–15 May', 'from 14 May'), '12–15 May',
       'A four-day fair of Nag Chawasi Siddh, with folk music and dance.', 'नाग च्वासी सिद्ध का चार दिन का मेला, लोक संगीत और नाटी के साथ।',
       '/temples/#chawasi'),
    _m(5, 'Mahunag Mela', 'माहूँनाग मेला', 'Mahunag (Bakhari Kothi)', 'माहूँनाग (बखारी कोठी)', 'Mid-May (about 14–19 May)',
       'मई के बीच (लगभग 14–19 मई)', 'Starts around Jyeshtha Sankranti', 'ज्येष्ठ संक्रांति के आसपास शुरू',
       ('from 14 May', '~15–19 May', '15–19 May'), '~14–19 May',
       'The valley’s biggest fair: the devta’s procession to the fair ground, folk music and dance nights, stalls and a community meal.',
       'घाटी का सबसे बड़ा मेला: देवता की शोभायात्रा, लोक संगीत और नाटी की रातें, दुकानें और भंडारा।', '/mahunag/'),
    _m(6, 'Kamru Nag Mela', 'कमरूनाग मेला', 'Kamru Nag lake (trek from Rohanda)', 'कमरूनाग झील (रोहांडा से पैदल)', 'Mid-June',
       'जून के बीच', 'Around the middle of June', 'जून के बीच के आसपास', ('', '', ''), 'Mid-June',
       'The big annual gathering at the sacred lake, when the most pilgrims make the forest trek.',
       'पवित्र झील पर साल का बड़ा मेला, जब सबसे ज़्यादा श्रद्धालु जंगल के रास्ते पैदल पहुँचते हैं।', '/kamru-nag/'),
    _m(8, 'Chindi Mata Mela', 'चिंडी माता मेला', 'Chindi', 'चिंडी', '2–4 August', '2–4 अगस्त', 'Fixed dates', 'तय तारीख़ें',
       ('2–4 Aug', '2–4 Aug', '2–4 Aug'), '2–4 Aug', 'A three-day fair at the Chindi Mata temple, on the Karsog–Shimla road.',
       'करसोग–शिमला सड़क पर चिंडी माता मंदिर में तीन दिन का मेला।', '/chindi/'),
    _m(9, 'Seri Bhanju Mela', 'सेरी भणजू मेला', 'Seri Bungalow', 'सेरी बंगलो', 'Late August or September, three days',
       'अगस्त के आख़िर या सितंबर में, तीन दिन', 'Starts on Rishi Panchami', 'ऋषि पंचमी से शुरू', ('~8–10 Sep', 'from 28 Aug', '15–17 Sep'),
       '~5 Sep', 'A three-day fair of Nag Dhamuni at Seri Bungalow.', 'सेरी बंगलो में नाग धमूनी का तीन दिन का मेला।', '/temples/#dhamuni'),
    _m(9, 'Janmashtami', 'जन्माष्टमी', 'Laxmi Narayan temple, old bazaar, Karsog', 'लक्ष्मी नारायण मंदिर, पुराना बाज़ार, करसोग',
       'August or September', 'अगस्त या सितंबर', 'Hindu calendar', 'हिंदू पंचांग के अनुसार', ('', '', '4 Sep'), '~25 Aug',
       'Krishna’s birthday celebrated in Karsog’s old bazaar.', 'करसोग के पुराने बाज़ार में श्रीकृष्ण जन्मोत्सव।', '/temples/#laxmi_narayan'),
    _m(10, 'Sharadiya Navratri', 'शारदीय नवरात्रि', 'Kamaksha Devi (Kao), Shikari Devi and other goddess temples',
       'कामाक्षा देवी (काओ), शिकारी देवी और देवी के दूसरे मंदिर', 'September–October, nine days', 'सितंबर–अक्टूबर, नौ दिन',
       'Hindu calendar', 'हिंदू पंचांग के अनुसार', ('', '', ''), 'Sept–Oct',
       'Autumn Navratri; Ashtami night is especially busy at Kamaksha Devi, Kao.',
       'शरद ऋतु की नवरात्रि; अष्टमी की रात काओ के कामाक्षा देवी मंदिर में ख़ास भीड़ रहती है।', '/temples/#kamaksha'),
    _m(12, 'Budhi Diwali', 'बूढ़ी दिवाली', 'Mamleshwar Mahadev (Mamel) and Mahog', 'ममलेश्वर महादेव (ममेल) और महोग',
       'About a month after Diwali', 'दिवाली के लगभग एक महीने बाद', 'Hindu calendar', 'हिंदू पंचांग के अनुसार',
       ('30 Nov–1 Dec', '19–20 Nov', 'expected early Dec'), '~28 Nov',
       'The hill Diwali, celebrated a month after the main one with night-long festivities, a unique tradition of the hills.',
       'पहाड़ों की दिवाली, जो मुख्य दिवाली के एक महीने बाद रात भर के उत्सव के साथ मनाई जाती है।', '/mamleshwar/'),
]


def melas_json():
    """Compact fair list for the home page's live strip."""
    return [{'m': x['m'], 'en': x['en'], 'hi': x['hi'], 'we': x['usual'], 'wh': x['usual_hi'], 'u': '/melas/#m%d' % x['m']}
            for x in MELAS]


# ------------------------------------------------------------------ drone photos
PHOTOS = json.load(open(os.path.join(PUB, 'photos', 'photos.json'), encoding='utf-8'))
PLACES = json.load(open(os.path.join(PUB, 'photos', 'places.json'), encoding='utf-8'))
BY_SLUG = {}
for _p in PHOTOS:
    BY_SLUG.setdefault(_p['slug'], []).append(_p)


TOWN = (31.3825, 77.2045)     # Karsog town centre, for "how far from town" (straight line, as the drone flew)


def km(a, b):
    """Straight-line distance in km between two (lat, lon) points (good enough at this size)."""
    return math.hypot((a[0] - b[0]) * 111.2, (a[1] - b[1]) * 95)


def centre(slug):
    """Middle of the GPS points of a place's photos, or None when its photos have no GPS."""
    g = [p['gps'] for p in BY_SLUG.get(slug, []) if p.get('gps')]
    return (sum(x[0] for x in g) / len(g), sum(x[1] for x in g) / len(g)) if g else None


def in_karsog(slug):
    """True when a photo place is within 8 km of Karsog town. Farther places (Janjehli, Anni, Luhri...) are
    described as 'near Karsog', because some are in other tehsils or districts."""
    c = centre(slug)
    return c is not None and km(c, TOWN) < 8


PHOTO_PLACES = {k: v for k, v in json.load(open(os.path.join(ROOT, 'data', 'photo-places.json'), encoding='utf-8')).items()
                if not k.startswith('_')}
LABEL_HI = {k: v for k, v in json.load(open(os.path.join(ROOT, 'data', 'photo-labels-hi.json'), encoding='utf-8')).items()
            if not k.startswith('_')}
MISSING_HI = set()   # captions with no Hindi yet (build.py reports them)


def place_title(slug, lang='en'):
    """Name of a drone-photo place ('Nanj & Tundal' / 'नांज और टुंडल')."""
    p = PHOTO_PLACES.get(slug) or {}
    t = p.get('title') or next((x['title'] for x in PLACES if x['slug'] == slug), slug)
    return p.get('title_hi', t) if lang == 'hi' else t


def label_hi(label):
    if label in LABEL_HI:
        return LABEL_HI[label]
    if label.startswith('Near ') and label[5:] in LABEL_HI:
        return LABEL_HI[label[5:]] + ' के पास'
    MISSING_HI.add(label)
    return label


def photo_label(p, lang='en'):
    """Caption of a drone photo, e.g. 'Nanj bridge' / 'नांज पुल'."""
    lab = p.get('label') or (('Near ' if p.get('near') else '') + p['place'])
    return lab if lang == 'en' else label_hi(lab)


def photo_alt(p, lang='en'):
    """'Aerial view of Nanj bridge, near Karsog, Himachal Pradesh' — only what the caption says, plus where."""
    lab = photo_label(p, 'en')
    home = in_karsog(p['slug'])
    if lang == 'en':
        near = lab.startswith('Near ')
        x = lab[5:] if near else lab
        return f"Aerial view of {'the area near ' if near else ''}{x}{'' if 'Karsog' in x else (', Karsog' if home else ', near Karsog')}, Himachal Pradesh"
    h = label_hi(lab)
    return f"{h}{'' if 'करसोग' in h else (', करसोग' if home else ', करसोग के पास')}, हिमाचल प्रदेश, आसमान से"


def photo(file):
    """Photo record by file name, e.g. 'nyara-004'."""
    for p in PHOTOS:
        if p['file'] == file:
            return p
    raise KeyError(file)


def pbase(file):
    p = photo(file)
    return f'/photos/{p["slug"]}/{p["file"]}'


# ------------------------------------------------------------------ guide pages (for cards and lists across the site)
# page: (English name, Hindi name, photo, English line, Hindi line)
GUIDES = {
    'mahunag': ('Mahunag Temple', 'माहूँनाग मंदिर', 'mahunag-214', 'The valley’s most famous temple · 26 km', 'घाटी का सबसे प्रसिद्ध मंदिर · 26 किमी'),
    'mamleshwar': ('Mamleshwar Mahadev', 'ममलेश्वर महादेव', 'mamleshwar-322', 'Ancient Shiva temple · 2 km', 'प्राचीन शिव मंदिर · 2 किमी'),
    'kao': ('Kamaksha Devi, Kao', 'कामाक्षा देवी, काओ', 'kao-326', 'Goddess temple of the Suket kings · 7 km', 'सुकेत राजाओं की कुलदेवी का मंदिर · 7 किमी'),
    'shikari-devi': ('Shikari Devi', 'शिकारी देवी', 'shikari-devi-005', 'Roofless temple on a 3,359 m peak · 22 km', '3,359 मीटर की चोटी पर बिना छत का मंदिर · 22 किमी'),
    'kamru-nag': ('Kamru Nag Lake', 'कमरूनाग झील', None, 'Sacred lake of the rain god, reached on foot', 'वर्षा देवता की पवित्र झील, पैदल रास्ता'),
    'tattapani': ('Tattapani', 'तत्तापानी', 'tattapani-102', 'Hot springs on the Sutlej · 46 km', 'सतलुज किनारे गर्म पानी के चश्मे · 46 किमी'),
    'pangna-fort': ('Pangna', 'पांगणा', 'pangna-fort-244', 'Fort-temple of the Suket kings · 19 km', 'सुकेत राजाओं का क़िला-मंदिर · 19 किमी'),
    'chindi': ('Chindi', 'चिंडी', 'chindi-295', 'Orchards, temple and sunsets · 7 km', 'बगीचे, मंदिर और सूर्यास्त · 7 किमी'),
    'janjehli': ('Janjehli', 'जंजैहली', 'janjehli-031', 'Valley below Shikari Devi · 27 km', 'शिकारी देवी के नीचे की घाटी · 27 किमी'),
}

# Road distances from Karsog bus stand, fastest route on Google Maps, checked 28 Sep 2026.
# (English, Hindi, km, driving time English, driving time Hindi, guide page, note English, note Hindi)
DIST_CHECKED, DIST_CHECKED_HI = '28 Sep 2026', '28 सितंबर 2026'
DIST = [
    ('Mamleshwar Mahadev, Mamel', 'ममलेश्वर महादेव, ममेल', 2.3, '10 min', '10 मिनट', '/mamleshwar/', '', ''),
    ('Chindi', 'चिंडी', 7, '25 min', '25 मिनट', '/chindi/', 'steep short road; 15 km by the main road', 'छोटी पर चढ़ाई वाली सड़क से; मुख्य सड़क से 15 किमी'),
    ('Kamaksha Devi, Kao', 'कामाक्षा देवी, काओ', 7, '20 min', '20 मिनट', '/kao/', '', ''),
    ('Churag', 'चुराग', 13, '40 min', '40 मिनट', None, '', ''),
    ('Pangna', 'पांगणा', 19, '50 min', '50 मिनट', '/pangna-fort/', '', ''),
    ('Shikari Devi temple', 'शिकारी देवी मंदिर', 22, '1 h 15 min', '1 घंटा 15 मिनट', '/shikari-devi/', 'road usually closed by snow in winter', 'सर्दियों में सड़क अक्सर बर्फ़ से बंद'),
    ('Mahunag temple', 'माहूँनाग मंदिर', 26, '1 h 15 min', '1 घंटा 15 मिनट', '/mahunag/', '', ''),
    ('Janjehli', 'जंजैहली', 27, '1 h 25 min', '1 घंटा 25 मिनट', '/janjehli/', 'over the Shikari Devi road; 84 km via Chhatri when it is closed', 'शिकारी देवी वाली सड़क से; वह बंद हो तो छतरी होकर 84 किमी'),
    ('Tattapani', 'तत्तापानी', 46, '1 h 45 min', '1 घंटा 45 मिनट', '/tattapani/', '', ''),
    ('Chhatri', 'छतरी', 48, '2 h 20 min', '2 घंटे 20 मिनट', '/chhatri/', '', ''),
    ('Rohanda (start of the Kamru Nag trek)', 'रोहांडा (कमरूनाग ट्रेक की शुरुआत)', 52, '2 h 15 min', '2 घंटे 15 मिनट', '/kamru-nag/', '', ''),
    ('Rampur Bushahr', 'रामपुर बुशहर', 75, '2 h 35 min', '2 घंटे 35 मिनट', '/bus/karsog-to-rampur/', '', ''),
    ('Sundernagar', 'सुंदरनगर', 80, '3 h 15 min', '3 घंटे 15 मिनट', None, '', ''),
    ('Nerchowk', 'नेरचौक', 86, '3 h 25 min', '3 घंटे 25 मिनट', None, '', ''),
    ('Shimla (ISBT Tutikandi)', 'शिमला (आईएसबीटी टूटीकंडी)', 94, '3 h 40 min', '3 घंटे 40 मिनट', '/shimla-to-karsog-bus/', '', ''),
    ('Mandi', 'मंडी', 99, '3 h 40 min', '3 घंटे 40 मिनट', '/mandi-to-karsog-bus/', '', ''),
    ('Solan', 'सोलन', 133, '4 h 35 min', '4 घंटे 35 मिनट', None, '', ''),
    ('Bhuntar airport (Kullu)', 'भुंतर हवाई अड्डा (कुल्लू)', 150, '4 h 45 min', '4 घंटे 45 मिनट', None, '', ''),
    ('Kullu', 'कुल्लू', 163, '5 h', '5 घंटे', None, '', ''),
    ('Manali', 'मनाली', 199, '6 h', '6 घंटे', None, '', ''),
    ('Chandigarh (ISBT Sector 43)', 'चंडीगढ़ (आईएसबीटी सेक्टर 43)', 217, '6 h', '6 घंटे', None, '', ''),
    ('Delhi (Kashmere Gate ISBT)', 'दिल्ली (कश्मीरी गेट आईएसबीटी)', 434, '10 h', '10 घंटे', '/bus/karsog-to-delhi/', '', ''),
]
