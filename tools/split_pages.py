# -*- coding: utf-8 -*-
"""Split the long homepage into multi-page HTML with shared CSS/JS."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "public"
INDEX = ROOT / "index.html"
CSS_DIR = ROOT / "css"
JS_DIR = ROOT / "js"

NAV_ITEMS = [
    ("Home", "/", "होम"),
    ("About", "/about/", "परिचय"),
    ("Places", "/places/", "स्थल"),
    ("Gallery", "/gallery/", "गैलरी"),
    ("Videos", "/videos/", "वीडियो"),
    ("Getting Here", "/getting-here/", "कैसे पहुँचें"),
    ("Plan", "/plan/", "यात्रा योजना"),
    ("FAQ", "/faq/", "सामान्य प्रश्न"),
    ("Contact", "/contact/", "संपर्क"),
]


def extract_between(text: str, start: str, end: str) -> str:
    i = text.find(start)
    j = text.find(end, i + len(start))
    if i < 0 or j < 0:
        raise ValueError(f"Could not find markers: {start!r} … {end!r}")
    return text[i + len(start) : j]


def extract_section(text: str, section_id: str) -> str:
    # Match <section ... id="id" ...> ... </section> with nested sections forbidden (flat)
    pattern = rf'(<section[^>]*\bid=["\']{re.escape(section_id)}["\'][^>]*>)(.*?)(</section>)'
    m = re.search(pattern, text, re.S)
    if not m:
        raise ValueError(f"Section not found: {section_id}")
    return m.group(0)


def extract_photos_block(text: str) -> str:
    return extract_between(text, "<!-- photos:start -->", "<!-- photos:end -->").strip()


def head_common(title: str, description: str, canonical: str, extra: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{description}" />
<link rel="canonical" href="{canonical}" />
<link rel="alternate" hreflang="en" href="{canonical}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{description}" />
<meta property="og:image" content="https://karsog.com/karsog-valley.jpg" />
<meta property="og:url" content="{canonical}" />
<meta property="og:type" content="website" />
<meta name="theme-color" content="#1c3a1c" />
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🏔️</text></svg>" />
<link rel="manifest" href="/manifest.webmanifest" />
<link rel="apple-touch-icon" href="/icon-192.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=DM+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/css/site.css" />
{extra}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def nav_html(active: str) -> str:
    links = []
    mobile = []
    for label, href, hi in NAV_ITEMS:
        cls = ' class="active"' if label == active else ""
        links.append(f'<li><a href="{href}"{cls} data-hi="{hi}">{label}</a></li>')
        mobile.append(f'<a href="{href}"{cls} data-hi="{hi}">{label}</a>')
    mobile.append('<a href="/rti/" data-hi="RTI व ऑडिट रिपोर्ट">RTI &amp; Audit Reports</a>')
    mobile.append('<a href="/mandi-rates/" data-hi="मंडी भाव">Mandi Rates</a>')
    mobile.append('<a href="tel:108" style="color:var(--gold-light);margin-top:1rem" data-hi="📞 108 एम्बुलेंस">📞 108 Ambulance</a>')
    mobile.append('<button class="lang-btn" id="lang-mobile" aria-label="Switch language">हिंदी</button>')
    return f"""
<div class="road" id="road" hidden></div>
<div class="wx" id="wx" hidden></div>
<nav class="top" aria-label="Primary">
  <div class="container inner">
    <a href="/" class="brand">Karsog<em>Valley</em></a>
    <ul class="nav-links">
      {"".join(links)}
    </ul>
    <button class="lang-btn" id="lang-desktop" aria-label="Switch language">हिंदी</button>
    <a href="tel:108" class="nav-cta" data-hi="📞 108 एम्बुलेंस">📞 108 Ambulance</a>
    <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>
<div class="mobile-menu" id="mobile-menu" role="dialog" aria-modal="true" aria-label="Navigation">
  <button class="close" id="close-menu" aria-label="Close menu">×</button>
  {"".join(mobile)}
</div>
"""


def footer_html() -> str:
    return """
<footer>
  <div class="container foot-grid">
    <div class="foot-brand">
      <h3>Karsog <em>Valley</em></h3>
      <p data-hi="कारसोग की संपूर्ण गाइड — पर्यटन, यात्रा, स्थानीय जानकारी और आपातकालीन संपर्क। एक कारसोग निवासी द्वारा, यात्रियों और स्थानीय लोगों के लिए।">A complete guide to Karsog — tourism, travel, local info and emergency contacts. Maintained by a Karsog resident, for visitors and locals alike.</p>
      <div class="hi">कारसोग घाटी, जिला मंडी, हिमाचल प्रदेश · PIN 175011</div>
    </div>
    <div class="foot-col">
      <h4 data-hi="पर्यटन">Explore</h4>
      <ul>
        <li><a href="/places/" data-hi="दर्शनीय स्थल">Places to Visit</a></li>
        <li><a href="/gallery/" data-hi="फ़ोटो गैलरी">Photo Gallery</a></li>
        <li><a href="/videos/" data-hi="वीडियो">Videos</a></li>
        <li><a href="/plan/" data-hi="यात्रा योजना">Plan Your Trip</a></li>
        <li><a href="/shikari-devi/">Shikari Devi</a></li>
        <li><a href="/kamru-nag/">Kamru Nag</a></li>
        <li><a href="/mamleshwar/">Mamleshwar</a></li>
        <li><a href="/mahunag/">Mahunag</a></li>
        <li><a href="/rides/" data-hi="राइड वीडियो">Ride Videos</a></li>
      </ul>
    </div>
    <div class="foot-col">
      <h4 data-hi="उपयोगी">Practical</h4>
      <ul>
        <li><a href="/getting-here/" data-hi="कैसे पहुँचें">Getting Here</a></li>
        <li><a href="/karsog-bus-stand/" data-hi="बस समय">Bus Stand Timings</a></li>
        <li><a href="/faq/" data-hi="सामान्य प्रश्न">FAQ</a></li>
        <li><a href="/contact/" data-hi="संपर्क व आपातकाल">Contact &amp; Emergency</a></li>
        <li><a href="/rti/" data-hi="RTI व ऑडिट रिपोर्ट">RTI &amp; Audit Reports</a></li>
        <li><a href="/mandi-rates/" data-hi="मंडी भाव">Mandi Rates</a></li>
        <li><a href="https://online.hrtchp.com/oprs-web/" target="_blank" rel="noopener">HRTC Online ↗</a></li>
      </ul>
    </div>
    <div class="foot-col">
      <h4 data-hi="हमारी अन्य साइटें">More From Us</h4>
      <ul>
        <li><a href="https://www.youtube.com/@KarsogMiles" target="_blank" rel="noopener">Karsog Miles · YouTube ↗</a></li>
        <li><a href="https://www.facebook.com/KarsogMiles/" target="_blank" rel="noopener">Karsog Miles · Facebook ↗</a></li>
        <li><a href="https://pinkyfancystore.com" target="_blank" rel="noopener">Pinky Fancy Store ↗</a></li>
        <li><a href="https://toolninja.in" target="_blank" rel="noopener">ToolNinja ↗</a></li>
      </ul>
    </div>
  </div>
  <div class="container foot-bot">
    <span>© <span id="y"></span> Karsog Valley Guide · Built &amp; maintained by a Karsog resident</span>
  </div>
</footer>

<button class="fab" id="fab" aria-label="Submit an update">
  <span class="fab-i">💬</span>
  <span data-hi="अपडेट भेजें">Submit an update</span>
</button>
<div class="modal" id="modal" role="dialog" aria-modal="true" aria-labelledby="mdl-title">
  <div class="modal-box">
    <button class="close" id="close-mdl" aria-label="Close">×</button>
    <h3 id="mdl-title" data-hi="Karsog.com को सटीक रखने में मदद करें">Help keep Karsog.com accurate</h3>
    <p class="mdl-sub" data-hi="ग़लत बस समय, बंद सड़क या नया संपर्क दिखा? भेजें — हम जाँचकर अपडेट करेंगे। संदेश WhatsApp में खुलेगा।">Noticed a wrong bus time, a closed road, or a new contact? Submit it — we'll verify and update. Message opens in WhatsApp.</p>
    <label for="s-type" data-hi="अपडेट का प्रकार">Type of update</label>
    <select id="s-type">
      <option value="bus" data-hi="बस समय बदलाव">Bus timing change</option>
      <option value="road" data-hi="सड़क / मौसम स्थिति">Road / weather condition</option>
      <option value="contact" data-hi="फ़ोन / ईमेल सुधार">Phone / email correction</option>
      <option value="taxi" data-hi="टैक्सी दर या ड्राइवर संपर्क">Taxi rate or driver contact</option>
      <option value="stay" data-hi="होटल / होमस्टे जानकारी">Hotel / homestay info</option>
      <option value="other" data-hi="अन्य">Other</option>
    </select>
    <label for="s-text" data-hi="विवरण *">Details *</label>
    <textarea id="s-text" placeholder="e.g. The 8:30 AM Mandi bus now departs at 9:00 AM (verified today)"></textarea>
    <label for="s-name" data-hi="आपका नाम (वैकल्पिक)">Your name (optional)</label>
    <input type="text" id="s-name" placeholder="Credited if published" />
    <button class="submit-btn" id="send" data-hi="📤 WhatsApp से भेजें">📤 Send via WhatsApp</button>
  </div>
</div>
<script src="/js/site.js" defer></script>
</body>
</html>
"""


def page_shell(
    *,
    title: str,
    description: str,
    canonical: str,
    active: str,
    main_html: str,
    extra_head: str = "",
) -> str:
    return (
        head_common(title, description, canonical, extra_head)
        + nav_html(active)
        + f'<main id="main">\n{main_html}\n</main>\n'
        + footer_html()
    )


def page_hero(eyebrow: str, title_html: str, lede: str, crumbs: list[tuple[str, str]] | None = None) -> str:
    crumb = ""
    if crumbs:
        parts = []
        for label, href in crumbs[:-1]:
            parts.append(f'<a href="{href}">{label}</a>')
        parts.append(f"<span>{crumbs[-1][0]}</span>")
        crumb = '<nav class="crumb" aria-label="Breadcrumb">' + " / ".join(parts) + "</nav>"
    return f"""
<header class="page-hero">
  <div class="container">
    {crumb}
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title_html}</h1>
    <p class="lede">{lede}</p>
  </div>
</header>
"""


def main() -> None:
    src = INDEX.read_text(encoding="utf-8")

    # CSS
    CSS_DIR.mkdir(exist_ok=True)
    css = extract_between(src, "<style>", "</style>")
    extras = """
/* Multi-page additions */
.skip{position:absolute;left:-999px;top:auto;width:1px;height:1px;overflow:hidden;z-index:100}
.skip:focus{left:1rem;top:1rem;width:auto;height:auto;padding:.6rem 1rem;background:var(--gold);color:var(--cream);outline:2px solid var(--forest)}
.nav-links a.active,.mobile-menu a.active{color:var(--forest);font-weight:600}
.mobile-menu a.active{color:var(--gold-light)}
.page-hero{padding:2.5rem 0 1rem;border-bottom:1px solid var(--border);background:linear-gradient(180deg,#efe9dd66,#faf8f4)}
.page-hero h1{font-size:clamp(2.2rem,5vw,3.4rem);color:var(--forest);margin-top:.75rem}
.page-hero .lede{margin-top:1rem}
.crumb{font-size:.78rem;color:var(--muted);margin-bottom:1rem}
.crumb a{color:var(--gold)}
.home-quick{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));margin:2.5rem 0 0}
.home-quick a{display:block;padding:1.25rem;background:#fff;border:1px solid var(--border);transition:all .3s}
.home-quick a:hover{transform:translateY(-2px);box-shadow:0 16px 32px -16px rgba(28,58,28,.15)}
.home-quick .k{font-size:.68rem;text-transform:uppercase;letter-spacing:.16em;color:var(--gold);font-weight:600}
.home-quick .t{font-family:'Playfair Display',serif;font-size:1.25rem;color:var(--forest);margin-top:.4rem}
.home-quick .d{font-size:.85rem;color:#1a1a18bf;margin-top:.45rem;line-height:1.55}
.cta-band{background:var(--forest);color:var(--cream);padding:3.5rem 0;margin-top:0}
.cta-band h2{color:var(--cream);font-size:clamp(1.8rem,4vw,2.6rem)}
.cta-band p{color:#f6f3eeb3;margin-top:1rem;max-width:36rem}
.cta-band .hero-actions{margin-top:1.5rem}
.feat-grid{margin-top:2.5rem;display:grid;gap:1.25rem;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
.about-prose{max-width:46rem;margin-top:1.5rem}
.about-prose p{margin-bottom:1rem;color:#1a1a18d9;font-size:1rem;line-height:1.75}
.gallery-more{margin-top:2rem}
"""
    (CSS_DIR / "site.css").write_text(css + extras, encoding="utf-8")

    # JS (from original, without GA)
    JS_DIR.mkdir(exist_ok=True)
    js = extract_between(src, '<script>\n// Year', "</script>")
    # The extract starts mid-script; prepend year comment area
    js_full = "// Year\n" + js
    # Fix: original had document.getElementById('y')... after // Year
    (JS_DIR / "site.js").write_text(js_full, encoding="utf-8")

    places = extract_section(src, "places")
    videos = extract_section(src, "videos")
    reach = extract_section(src, "reach")
    bus = extract_section(src, "bus")
    taxi = extract_section(src, "taxi")
    plan = extract_section(src, "plan")
    stay = extract_section(src, "stay")
    festivals = extract_section(src, "festivals")
    fmap = extract_section(src, "map")
    faq = extract_section(src, "faq")
    local = extract_section(src, "local")
    emergency = extract_section(src, "emergency")
    photos_block = extract_photos_block(src)

    # Featured places for home (first 3 articles from places grid)
    place_articles = re.findall(r"<article class=\"place\">.*?</article>", places, re.S)
    featured = "\n".join(place_articles[:3])

    # Photo preview: first 6 cards from pgrid
    pgrid_m = re.search(r'<div class="pgrid">(.*?)</div></div></section>', photos_block, re.S)
    photo_cards = re.findall(r'<a class="pc".*?</a>', pgrid_m.group(1) if pgrid_m else "", re.S)
    photo_preview = "".join(photo_cards[:6])

    marquee = """
<div class="marquee" aria-hidden="true">
  <div class="marquee-track">
    <span>Mahunag Temple <i>✦</i></span><span>Mamleshwar Mahadev <i>✦</i></span><span>Kamaksha Devi · Kao <i>✦</i></span><span>Kamru Nag Lake <i>✦</i></span><span>Pangna Fort · 1211 AD <i>✦</i></span><span>Shikari Devi · 3,359 m <i>✦</i></span><span>Apple Orchards <i>✦</i></span><span>Tattapani Hot Springs <i>✦</i></span><span>Janjehli Valley <i>✦</i></span><span>Chindi · HPTDC <i>✦</i></span>
    <span>Mahunag Temple <i>✦</i></span><span>Mamleshwar Mahadev <i>✦</i></span><span>Kamaksha Devi · Kao <i>✦</i></span><span>Kamru Nag Lake <i>✦</i></span><span>Pangna Fort · 1211 AD <i>✦</i></span><span>Shikari Devi · 3,359 m <i>✦</i></span><span>Apple Orchards <i>✦</i></span><span>Tattapani Hot Springs <i>✦</i></span><span>Janjehli Valley <i>✦</i></span><span>Chindi · HPTDC <i>✦</i></span>
  </div>
</div>
"""

    # --- HOME ---
    home_main = f"""
<section class="hero" id="top">
  <img srcset="/karsog-valley-900.webp 900w, /karsog-valley.webp 1600w" sizes="100vw" src="/karsog-valley.jpg" alt="Karsog Valley with traditional colourful houses on the hillside and the Himalayas behind" class="bg" width="1600" height="720" fetchpriority="high" decoding="async" />
  <div class="container inner">
    <div class="loc" data-hi="मंडी ज़िला · हिमाचल प्रदेश">Mandi District · Himachal Pradesh</div>
    <h1 data-hi="कारसोग <em>घाटी</em>">Karsog <em>Valley</em></h1>
    <p data-hi="हिमालय की गोद में बसी — प्राचीन मंदिर, सेब के बाग़ और ऐसी पहाड़ी हवा जो हमेशा के लिए रुक जाने का मन कर दे।">Tucked in the Himalayan foothills — ancient temples, apple orchards, and mountain air that makes you want to stay forever.</p>
    <div class="hero-actions">
      <a href="/places/" class="btn btn-gold" data-hi="स्थल देखें →">Explore places →</a>
      <a href="/getting-here/" class="btn btn-ghost" data-hi="कैसे पहुँचें">Getting here</a>
    </div>
    <div class="stats">
      <div class="stat"><div class="stat-v">1,404 m</div><div class="stat-l" data-hi="ऊँचाई">Elevation</div></div>
      <div class="stat"><div class="stat-v">120 km</div><div class="stat-l" data-hi="मंडी से दूरी">From Mandi</div></div>
      <div class="stat"><div class="stat-v">7th c.</div><div class="stat-l" data-hi="मामलेश्वर">Mamleshwar</div></div>
      <div class="stat"><div class="stat-v">HP 30</div><div class="stat-l" data-hi="RTO कोड">RTO Code</div></div>
    </div>
  </div>
</section>
{marquee}
<section>
  <div class="container">
    <div class="section-head">
      <span class="eyebrow" data-hi="शुरू करें">Start here</span>
      <h2 data-hi="कारसोग की गाइड,<br /><em>पृष्ठों में बाँटी।</em>">Your Karsog guide,<br /><em>in clear pages.</em></h2>
      <p class="lede" style="margin-top:1.25rem" data-hi="बस समय, मंदिर, ट्रेक, फ़ोटो और आपातकालीन नंबर — एक ही जगह, आसान नेविगेशन के साथ।">Bus timings, temples, treks, drone photos and emergency numbers — one local guide with easy navigation.</p>
    </div>
    <div class="home-quick">
      <a href="/places/"><div class="k">Attractions</div><div class="t" data-hi="दर्शनीय स्थल">Places to visit</div><div class="d" data-hi="मंदिर, झीलें, किले और ट्रेक।">Temples, lakes, forts and treks.</div></a>
      <a href="/gallery/"><div class="k">From above</div><div class="t" data-hi="ड्रोन फ़ोटो">Drone gallery</div><div class="d" data-hi="339 फ़ोटो · 27 जगहें।">339 photos · 27 places.</div></a>
      <a href="/getting-here/"><div class="k">Travel</div><div class="t" data-hi="बस व टैक्सी">Buses &amp; taxis</div><div class="d" data-hi="HRTC समय और स्थानीय किराए।">HRTC times and local fares.</div></a>
      <a href="/contact/"><div class="k">Help</div><div class="t" data-hi="संपर्क">Contacts</div><div class="d" data-hi="कार्यालय, अस्पताल, आपातकाल।">Offices, hospital, emergency.</div></a>
    </div>
  </div>
</section>
<section class="bg-secondary">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow" data-hi="क्या देखें">What to see</span>
      <h2 data-hi="घाटी के<br /><em>मुख्य स्थल</em>">Highlights of<br /><em>the valley</em></h2>
    </div>
    <div class="places-grid">{featured}</div>
    <div class="hero-actions" style="margin-top:2rem">
      <a href="/places/" class="btn btn-forest" data-hi="सभी स्थल →">All places →</a>
      <a href="/plan/" class="btn btn-outline" data-hi="यात्रा योजनाएँ">Itineraries</a>
    </div>
  </div>
</section>
<section>
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Karsog from above</span>
      <h2>Drone photos<br /><em>worth a look.</em></h2>
      <p class="lede" style="margin-top:1.25rem">Aerial photos by <a href="https://www.youtube.com/@KarsogMiles" target="_blank" rel="noopener">Karsog Miles</a> — pick a place for the full set.</p>
    </div>
    <div class="pgrid">{photo_preview}</div>
    <div class="gallery-more"><a href="/gallery/" class="btn btn-forest" data-hi="पूरी गैलरी →">Full gallery →</a></div>
  </div>
</section>
<section class="cta-band">
  <div class="container">
    <h2 data-hi="आज कारसोग कैसे पहुँचें?">How do you get to Karsog today?</h2>
    <p data-hi="मंडी और शिमला की HRTC बसें, टैक्सी दरें और सड़क सलाह — एक पेज पर।">HRTC buses from Mandi and Shimla, taxi rates and road advice — on one page.</p>
    <div class="hero-actions">
      <a href="/getting-here/" class="btn btn-gold" data-hi="कैसे पहुँचें →">Getting here →</a>
      <a href="/faq/" class="btn btn-ghost" data-hi="सामान्य प्रश्न">FAQ</a>
    </div>
  </div>
</section>
"""

    home_extra = """
<link rel="preload" as="image" fetchpriority="high" imagesrcset="/karsog-valley-900.webp 900w, /karsog-valley.webp 1600w" imagesizes="100vw" href="/karsog-valley.jpg" />
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"TouristDestination","name":"Karsog Valley","description":"Karsog Valley in Mandi district, Himachal Pradesh — ancient temples, apple orchards, Kath-Kuni heritage forts and a complete local guide.","url":"https://karsog.com/","image":"https://karsog.com/karsog-valley.jpg","address":{"@type":"PostalAddress","addressLocality":"Karsog","addressRegion":"Himachal Pradesh","postalCode":"175011","addressCountry":"IN"},"geo":{"@type":"GeoCoordinates","latitude":31.3825,"longitude":77.2045}}
</script>
"""

    INDEX.write_text(
        page_shell(
            title="Karsog Valley Guide — Bus Timings, Temples, Weather & Photos",
            description="Plan your Karsog trip: HRTC bus timings from Mandi and Shimla, temples, treks, taxi rates, weather, road advisories and emergency numbers.",
            canonical="https://karsog.com/",
            active="Home",
            main_html=home_main,
            extra_head=home_extra,
        ),
        encoding="utf-8",
    )

    def write_page(rel: str, **kwargs):
        path = ROOT / rel / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(page_shell(**kwargs), encoding="utf-8")
        print("wrote", path.relative_to(ROOT))

    # ABOUT
    about_main = page_hero(
        "About Karsog",
        "A Himalayan valley<br /><em>worth knowing.</em>",
        "Karsog sits at 1,404 m in southern Mandi district, Himachal Pradesh — roughly equidistant from Mandi and Shimla.",
        [("Home", "/"), ("About", "/about/")],
    ) + f"""
<section>
  <div class="container">
    <div class="about-prose">
      <p data-hi="हिमालय की गोद में बसी — प्राचीन मंदिर, सेब के बाग़ और ऐसी पहाड़ी हवा जो हमेशा के लिए रुक जाने का मन कर दे।">Tucked in the Himalayan foothills — ancient temples, apple orchards, and mountain air that makes you want to stay forever.</p>
      <p data-hi="7वीं सदी के शिव मंदिरों से लेकर ऊँचाई की झीलों और काठ-कुनी विरासत क़िलों तक — कारसोग घाटी में उम्मीद से कहीं ज़्यादा है।">From 7th-century Shiva shrines to high-altitude lakes and Kath-Kuni heritage forts — Karsog Valley holds far more than most travellers expect.</p>
      <p data-hi="यह साइट एक कारसोग निवासी द्वारा चलाई जाती है — पर्यटन, यात्रा, स्थानीय जानकारी और आपातकालीन संपर्क, यात्रियों और स्थानीय लोगों के लिए।">This site is maintained by a Karsog resident — tourism, travel, local information and emergency contacts for visitors and locals alike.</p>
      <p data-hi="हम वही प्रकाशित करते हैं जिसकी पुष्टि हो सके। ग़लत समय या नया संपर्क दिखे तो अपडेट भेजें।">We publish only what can be verified. If you spot a wrong timing or a new contact, submit an update.</p>
    </div>
    <div class="stats" style="margin-top:2.5rem;max-width:42rem;background:var(--border)">
      <div class="stat" style="background:#fff"><div class="stat-v" style="color:var(--forest)">1,404 m</div><div class="stat-l" style="color:var(--muted)">Elevation</div></div>
      <div class="stat" style="background:#fff"><div class="stat-v" style="color:var(--forest)">~114 km</div><div class="stat-l" style="color:var(--muted)">From Mandi</div></div>
      <div class="stat" style="background:#fff"><div class="stat-v" style="color:var(--forest)">~106 km</div><div class="stat-l" style="color:var(--muted)">From Shimla</div></div>
      <div class="stat" style="background:#fff"><div class="stat-v" style="color:var(--forest)">175011</div><div class="stat-l" style="color:var(--muted)">PIN code</div></div>
    </div>
    <div class="hero-actions" style="margin-top:2rem">
      <a href="/places/" class="btn btn-forest">Places to visit</a>
      <a href="/contact/" class="btn btn-outline">Local contacts</a>
      <a href="/rti/" class="btn btn-outline">RTI &amp; audits</a>
    </div>
  </div>
</section>
{fmap}
"""
    write_page(
        "about",
        title="About Karsog Valley — Mandi District, Himachal Pradesh",
        description="About Karsog Valley in Mandi district, Himachal Pradesh: elevation, location, temples, apple orchards and a locally maintained guide.",
        canonical="https://karsog.com/about/",
        active="About",
        main_html=about_main,
    )

    # PLACES
    places_main = page_hero(
        "What to see",
        "Sacred peaks, ancient<br /><em>temples, hidden trails.</em>",
        "From 7th-century Shiva shrines to high-altitude lakes and Kath-Kuni heritage forts.",
        [("Home", "/"), ("Places", "/places/")],
    ) + places
    write_page(
        "places",
        title="Places to Visit in Karsog — Temples, Treks & Heritage",
        description="Mahunag, Mamleshwar, Kamaksha Devi, Kamru Nag, Pangna Fort, Shikari Devi and more places to visit around Karsog Valley.",
        canonical="https://karsog.com/places/",
        active="Places",
        main_html=places_main,
    )

    # GALLERY
    gallery_main = page_hero(
        "Karsog from above",
        "339 drone photos,<br /><em>27 places.</em>",
        "Aerial photos of Karsog's villages, temples, fairs and the Satluj valley, shot by Karsog Miles in 2026.",
        [("Home", "/"), ("Gallery", "/gallery/")],
    ) + photos_block
    write_page(
        "gallery",
        title="Karsog Photo Gallery — 339 Drone Photos",
        description="Aerial drone photos of Karsog Valley villages, temples and the Satluj — 339 photos across 27 places by Karsog Miles.",
        canonical="https://karsog.com/gallery/",
        active="Gallery",
        main_html=gallery_main,
    )

    # VIDEOS
    videos_main = page_hero(
        "Karsog Miles",
        "Ride the valley<br /><em>on YouTube</em>",
        "No commentary, no music — just engine sound and real Himachal roads.",
        [("Home", "/"), ("Videos", "/videos/")],
    ) + videos
    write_page(
        "videos",
        title="Karsog Videos — Motorcycle Rides & Drone Views",
        description="Motorcycle journeys and drone views of Karsog, Shikari Devi, Janjehli, Tattapani and mountain routes from Karsog Miles on YouTube.",
        canonical="https://karsog.com/videos/",
        active="Videos",
        main_html=videos_main,
    )

    # GETTING HERE
    getting_main = page_hero(
        "Travel",
        "How to <em>reach</em><br />Karsog Valley",
        "Roads from Mandi and Shimla, HRTC bus timings, and local taxi rates.",
        [("Home", "/"), ("Getting Here", "/getting-here/")],
    ) + reach + bus + taxi
    write_page(
        "getting-here",
        title="How to Reach Karsog — Buses, Taxi & Routes",
        description="How to reach Karsog from Mandi and Shimla: HRTC bus timings, taxi rates, nearest airport and railway options.",
        canonical="https://karsog.com/getting-here/",
        active="Getting Here",
        main_html=getting_main,
    )

    # PLAN
    plan_main = page_hero(
        "Plan your trip",
        "Ready-made<br /><em>itineraries</em>",
        "Temple circuits, hot springs, big treks — plus where to stay, eat and which fairs to catch.",
        [("Home", "/"), ("Plan", "/plan/")],
    ) + plan + stay + festivals
    write_page(
        "plan",
        title="Plan a Trip to Karsog — Itineraries, Stay & Festivals",
        description="Karsog itineraries, stay and food options, and a year of valley fairs and festivals.",
        canonical="https://karsog.com/plan/",
        active="Plan",
        main_html=plan_main,
    )

    # FAQ
    faq_main = page_hero(
        "FAQ",
        "Questions travellers<br /><em>ask us</em>",
        "Buses, roads, best season, ATMs, network and where to stay — answered from local sources.",
        [("Home", "/"), ("FAQ", "/faq/")],
    ) + faq
    write_page(
        "faq",
        title="Karsog FAQ — Buses, Roads, Season & Stay",
        description="Frequently asked questions about visiting Karsog: bus timings, monsoon roads, ATMs, mobile network and stay options.",
        canonical="https://karsog.com/faq/",
        active="FAQ",
        main_html=faq_main,
    )

    # CONTACT
    contact_main = page_hero(
        "Contact & help",
        "Offices, hospital<br /><em>& emergency</em>",
        "Key government offices in and around Karsog, plus numbers to save before you travel.",
        [("Home", "/"), ("Contact", "/contact/")],
    ) + local + emergency + fmap
    write_page(
        "contact",
        title="Karsog Contact & Emergency Numbers",
        description="SDM office, civil hospital, police, control room and national emergency numbers for Karsog Valley, Mandi district.",
        canonical="https://karsog.com/contact/",
        active="Contact",
        main_html=contact_main,
    )

    print("Done. CSS/JS + pages written.")


if __name__ == "__main__":
    main()
