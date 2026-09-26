#!/usr/bin/env python3
"""One-off: update Karsog->Mandi and Karsog->Shimla tables from the bus stand board (25 Sep 2026)."""
import re, os, json, html
PUB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public')


def R(t, a, i, hi=None):
    h = f' data-hi="{hi}"' if hi else ''
    return f'<div class="row"><span class="time">{t}</span><span class="arr">{a}</span><span class="info"{h}>{i}</span></div>'


def RH(t, a, i):
    return f'<div class="row"><span class="time">{t}</span><span class="arr">{a}</span><span class="info">{i}</span></div>'


K2M = [R('9:30 AM', '—', 'Direct · stand board', 'सीधी · बस अड्डा बोर्ड'),
       R('11:10 AM', '~4:30 PM', 'Via Sorta · ₹256 · board + bookable online', 'सोरता होकर · ₹256 · बोर्ड + ऑनलाइन बुकिंग'),
       R('2:00 PM', '—', 'Reckong Peo bus, via Sorta · stand board', 'रिकांगपिओ बस, सोरता होकर · बोर्ड'),
       R('5:15 PM', '—', 'Direct · stand board', 'सीधी · बस अड्डा बोर्ड')]
K2Mh = [RH('9:30 AM', '—', 'सीधी · बस अड्डा बोर्ड'), RH('11:10 AM', '~4:30 PM', 'सोरता होकर · ₹256 · बोर्ड + ऑनलाइन बुकिंग'),
        RH('2:00 PM', '—', 'रिकांगपिओ बस, सोरता होकर · बोर्ड'), RH('5:15 PM', '—', 'सीधी · बस अड्डा बोर्ड')]
K2S = [R('5:00 AM', '~10:00 AM', 'Via Bagshad · ₹278 · board + bookable online', 'बगशाड़ होकर · ₹278 · बोर्ड + ऑनलाइन बुकिंग'),
       R('6:00 AM', '—', 'Stand board', 'बस अड्डा बोर्ड'),
       R('9:00 AM', '—', 'Stand board', 'बस अड्डा बोर्ड'),
       R('10:00 AM', '—', 'Via Bagshad · starts at Janjehli · board', 'बगशाड़ होकर · जंजैहली से · बोर्ड'),
       R('12:10 PM', '~6:40 PM', 'Haridwar bus · ₹285 · board + bookable online', 'हरिद्वार बस · ₹285 · बोर्ड + ऑनलाइन बुकिंग'),
       R('12:45 PM', '—', 'Stand board', 'बस अड्डा बोर्ड'),
       R('2:00 PM', '—', 'Via Bagshad · stand board', 'बगशाड़ होकर · बोर्ड'),
       R('5:00 PM', '~10:30 PM', 'Delhi bus · ₹285 · board + bookable online', 'दिल्ली बस · ₹285 · बोर्ड + ऑनलाइन बुकिंग')]
K2Sh = [RH('5:00 AM', '~10:00 AM', 'बगशाड़ होकर · ₹278 · बोर्ड + ऑनलाइन बुकिंग'), RH('6:00 AM', '—', 'बस अड्डा बोर्ड'),
        RH('9:00 AM', '—', 'बस अड्डा बोर्ड'), RH('10:00 AM', '—', 'बगशाड़ होकर · जंजैहली से · बोर्ड'),
        RH('12:10 PM', '~6:40 PM', 'हरिद्वार बस · ₹285 · बोर्ड + ऑनलाइन बुकिंग'), RH('12:45 PM', '—', 'बस अड्डा बोर्ड'),
        RH('2:00 PM', '—', 'बगशाड़ होकर · बोर्ड'), RH('5:00 PM', '~10:30 PM', 'दिल्ली बस · ₹285 · बोर्ड + ऑनलाइन बुकिंग')]
FOOT_EN = 'Karsog bus stand board (25 Sep 2026) + HRTC online booking · <a href="/karsog-bus-stand/">all 49 departures</a>'
FOOT_HI = 'करसोग बस अड्डा बोर्ड (25 सितंबर 2026) + HRTC ऑनलाइन बुकिंग · <a href="/karsog-bus-stand/">सभी 49 बसें</a>'


def block(s, title, rows, foot_html, foot_hi=None):
    pat = re.compile(r'(<h3[^>]*>🚌 ' + re.escape(title) + r'</h3>.*?<div class="head-row">.*?</div>\s*)((?:<div class="row">.*?</div>\s*)+)(<div class="foot"><span[^>]*>.*?</span>)?', re.S)
    n = 0

    def f(m):
        nonlocal n
        n += 1
        out = m.group(1) + '\n    '.join(rows) + '\n    '
        if m.group(3):
            span = f'<span data-hi="{html.escape(foot_hi, quote=True)}">' if foot_hi else '<span>'
            out += '<div class="foot">' + span + foot_html + '</span>'
        return out
    return pat.sub(f, s), n


FAQ = {
    "What is the last bus from Karsog to Mandi?": "By the timetable board at Karsog bus stand (photographed 25 Sep 2026), the last direct bus to Mandi leaves at 5:15 PM. Other Mandi buses: 9:30 AM, 11:10 AM (via Sorta, also bookable online) and 2:00 PM (Reckong Peo bus via Sorta). Confirm at the stand.",
    "What are the Karsog to Shimla bus timings?": "By the Karsog bus stand board (25 Sep 2026): 5:00 AM (via Bagshad), 6:00 AM, 9:00 AM, 10:00 AM (via Bagshad, from Janjehli), 12:10 PM (Haridwar bus), 12:45 PM, 2:00 PM (via Bagshad) and 5:00 PM (Delhi bus). The 5:00 AM, 12:10 PM and 5:00 PM are also bookable on HRTC online booking.",
}
FAQ_HI = {'स्थानीय जानकारी के अनुसार कारसोग से मंडी की आख़िरी बस लगभग दोपहर 2:30 बजे चलती है और ~5:30 बजे पहुँचती है। ऑनलाइन बुकिंग पर केवल सुबह 11:10 की बस (नेरचौक होकर, ₹256) दिखती है। बस अड्डे पर पुष्टि करें।':
          'करसोग बस अड्डे के बोर्ड (25 सितंबर 2026) के अनुसार मंडी की आख़िरी सीधी बस शाम 5:15 बजे चलती है। अन्य बसें: सुबह 9:30, 11:10 (सोरता होकर, ऑनलाइन बुकिंग भी) और दोपहर 2:00 (रिकांगपिओ बस)। बस अड्डे पर पुष्टि करें।'}

for fn in ['index.html', 'hi/index.html', 'mandi-to-karsog-bus/index.html', 'shimla-to-karsog-bus/index.html']:
    p = os.path.join(PUB, fn)
    s = open(p, encoding='utf-8').read()
    log = []
    if fn.startswith('hi/'):
        s, a = block(s, 'कारसोग → मंडी', K2Mh, FOOT_HI)
        s, b = block(s, 'कारसोग → शिमला', K2Sh, FOOT_HI)
        for x, y in FAQ_HI.items():
            s = s.replace(x, y)
    else:
        s, a = block(s, 'Karsog → Mandi', K2M, FOOT_EN, FOOT_HI if fn == 'index.html' else None)
        s, b = block(s, 'Karsog → Shimla', K2S, FOOT_EN, FOOT_HI if fn == 'index.html' else None)
        if fn == 'index.html':
            for x, y in FAQ_HI.items():
                s = s.replace(x, y)
    for q, ans in FAQ.items():
        s, n1 = re.subn(r'("name":"' + re.escape(q) + r'","acceptedAnswer":\{"@type":"Answer","text":")[^"]*(")', lambda m: m.group(1) + ans + m.group(2), s)
        s, n2 = re.subn(r'(<summary[^>]*>' + re.escape(q) + r'</summary>\s*<p[^>]*>).*?(</p>)', lambda m: m.group(1) + html.escape(ans, quote=False) + m.group(2), s, flags=re.S)
        log.append((q[:20], n1, n2))
    if fn == 'mandi-to-karsog-bus/index.html':
        d = 'Mandi ⇄ Karsog bus timings: Karsog to Mandi 9:30 AM, 11:10 AM, 2:00 PM, 5:15 PM (Karsog bus stand board); Mandi to Karsog 4:30 AM bookable online plus local timings. About 114 km.'
        s = re.sub(r'<meta name="description" content="[^"]*" />', f'<meta name="description" content="{d}" />', s, 1)
        s = re.sub(r'<meta property="og:description" content="[^"]*" />', f'<meta property="og:description" content="{d}" />', s, 1)
    for m in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', s, re.S):
        json.loads(m)
    open(p, 'w', encoding='utf-8').write(s)
    print(fn, 'K2M', a, 'K2S', b, log)
