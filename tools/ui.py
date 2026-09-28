"""Site-wide navigation and interface text for karsog.com, in English and Hindi.

Every page is built in both languages: English at /path/, Hindi at /hi/path/.
To add or rename a menu item, edit NAV / MORE below and rebuild (python3 tools/build.py)."""

LANGS = ('en', 'hi')

# key, English, Hindi, path, icon
NAV = [
    ('buses', 'Buses', 'बसें', '/karsog-bus-stand/', 'bus'),
    ('weather', 'Weather', 'मौसम', '/weather/', 'weather'),
    ('places', 'Places', 'घूमने की जगहें', '/places/', 'pin'),
    ('temples', 'Temples', 'मंदिर', '/temples/', 'temple'),
    ('melas', 'Melas', 'मेले', '/melas/', 'party'),
    ('photos', 'Photos', 'फ़ोटो', '/photos/', 'camera'),
    ('plan', 'Plan a trip', 'यात्रा योजना', '/plan/', 'compass'),
]
MORE = [
    ('hotels', 'Hotels', 'होटल', '/hotels/', 'bed'),
    ('distance', 'Distances', 'दूरी', '/distance/', 'ruler'),
    ('mandi', 'Mandi rates', 'मंडी भाव', '/mandi-rates/', 'apple'),
    ('contacts', 'Useful numbers', 'ज़रूरी नंबर', '/contacts/', 'phone'),
    ('rti', 'RTI', 'आरटीआई', '/rti/', 'file'),
    ('rides', 'Ride videos', 'राइड वीडियो', '/rides/', 'play'),
]
BOTTOM = [('home', 'Home', 'होम', '/', 'home'), ('buses', 'Buses', 'बसें', '/karsog-bus-stand/', 'bus'),
          ('weather', 'Weather', 'मौसम', '/weather/', 'weather'), ('places', 'Places', 'जगहें', '/places/', 'pin')]

# second row of buttons shown on every page of a section
SUBNAV = {
    'buses': [('All buses', 'सभी बसें', '/karsog-bus-stand/'), ('Private buses', 'प्राइवेट बसें', '/karsog-private-bus/'),
              ('Mandi ⇄ Karsog', 'मंडी ⇄ करसोग', '/mandi-to-karsog-bus/'), ('Shimla ⇄ Karsog', 'शिमला ⇄ करसोग', '/shimla-to-karsog-bus/'),
              ('Distances', 'दूरी', '/distance/')],
}

# pages that belong to a menu section (first path segment -> nav key)
SECTION = {
    'karsog-bus-stand': 'buses', 'karsog-private-bus': 'buses', 'mandi-to-karsog-bus': 'buses', 'shimla-to-karsog-bus': 'buses', 'bus': 'buses',
    'weather': 'weather', 'places': 'places', 'temples': 'temples', 'melas': 'melas', 'photos': 'photos', 'rides': 'photos',
    'plan': 'plan', 'hotels': 'plan', 'distance': 'plan', 'mandi-rates': 'mandi', 'contacts': 'contacts', 'rti': 'rti',
    'mahunag': 'temples', 'mamleshwar': 'temples', 'kao': 'temples', 'chindi': 'temples', 'shikari-devi': 'places',
    'kamru-nag': 'places', 'tattapani': 'places', 'pangna-fort': 'places', 'janjehli': 'places',
}

T = {
    'skip': ('Skip to content', 'मुख्य सामग्री पर जाएँ'),
    'menu': ('Menu', 'मेन्यू'),
    'close': ('Close', 'बंद करें'),
    'more': ('More', 'और'),
    'switch': ('हिंदी', 'English'),
    'switch_label': ('पढ़ें हिंदी में', 'Read in English'),
    'home': ('Home', 'होम'),
    'send_update': ('Send an update', 'अपडेट भेजें'),
    'send_update_long': ('Seen a change? Send an update', 'कुछ बदला है? अपडेट भेजें'),
    'emergency': ('Emergency', 'आपातकाल'),
    'tagline': ('The complete guide to Karsog valley, Mandi, Himachal Pradesh — buses, weather, temples, fairs and photos.',
                'करसोग घाटी (मंडी, हिमाचल प्रदेश) की पूरी जानकारी — बसें, मौसम, मंदिर, मेले और फ़ोटो।'),
    'made_by': ('Made in Karsog by a local resident, for visitors and locals alike.',
                'करसोग के एक निवासी द्वारा, यात्रियों और स्थानीय लोगों के लिए।'),
    'f_travel': ('Travel', 'यात्रा'), 'f_explore': ('Explore', 'घूमें'), 'f_local': ('Local info', 'स्थानीय जानकारी'), 'f_more': ('More from us', 'हमारी और साइटें'),
    'copyright': ('Photos & videos © Karsog Miles', 'फ़ोटो व वीडियो © Karsog Miles'),
    'modal_title': ('Send an update', 'अपडेट भेजें'),
    'modal_sub': ('Bus timing changed? Road closed? New hotel? Tell us on WhatsApp and we’ll update the site.',
                  'बस का समय बदला? सड़क बंद है? नया होटल? व्हाट्सऐप पर बताइए, हम साइट अपडेट कर देंगे।'),
    'modal_type': ('What is it about?', 'किस बारे में?'),
    'modal_types': (['Bus timing', 'Road / weather', 'Temple / fair', 'Hotel / food', 'Phone number', 'Something else'],
                    ['बस का समय', 'सड़क / मौसम', 'मंदिर / मेला', 'होटल / खाना', 'फ़ोन नंबर', 'कुछ और']),
    'modal_text': ('Your update', 'आपका अपडेट'),
    'modal_name': ('Your name (optional)', 'आपका नाम (वैकल्पिक)'),
    'modal_send': ('Send on WhatsApp', 'व्हाट्सऐप पर भेजें'),
    'modal_empty': ('Please write your update first.', 'पहले अपना अपडेट लिखें।'),
    'crumb_root': ('karsog.com', 'karsog.com'),
    'now_title': ('Right now in Karsog', 'करसोग में अभी'),
    'updated': ('Checked', 'जाँचा गया'),
    'read_more': ('Read more', 'और पढ़ें'),
    'see_all': ('See all', 'सभी देखें'),
    'photos_n': ('photos', 'फ़ोटो'),
    'km_from': ('km from Karsog', 'किमी करसोग से'),
    'back_top': ('Back to top', 'ऊपर जाएँ'),
}


def t(key, lang):
    v = T[key]
    return v[0] if lang == 'en' else v[1]


def label(item, lang):
    return item[1] if lang == 'en' else item[2]


def section_of(path):
    """Menu key for a site path like /mahunag/ or /hi/mahunag/."""
    p = path
    if p.startswith('/hi/'):
        p = p[3:]
    seg = p.strip('/').split('/')[0] if p.strip('/') else ''
    if seg == '':
        return 'home'
    if seg in SECTION:
        return SECTION[seg]
    for k, *_rest in NAV + MORE:
        if _rest[2].strip('/') == seg:
            return k
    return 'photos'  # the drone-photo place pages


def lpath(path, lang):
    """Path of a page in the given language (English /x/, Hindi /hi/x/)."""
    base = path[3:] if path.startswith('/hi/') else path
    if lang == 'en':
        return base
    return '/hi' + base if base != '/' else '/hi/'
