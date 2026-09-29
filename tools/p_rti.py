"""RTI replies & audit reports (/rti/ and /hi/rti/).

The text lives in content/rti/en.html and content/rti/hi.html: a header of "key: value" lines, then the page body
in HTML (document cards, filters, how to file, templates, FAQ). The PDFs are in public/rti/files/. Page-only styles
and behaviour: /assets/rti.css and /assets/rti.js. Applicants' phone numbers, emails and addresses stay blacked out
in the PDFs; names are kept."""
import json, os, re
from layout import L, section, facts, faq_ld, comments, ROOT


def read(lang):
    s = open(os.path.join(ROOT, 'content', 'rti', lang + '.html'), encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n(.*)$', s, re.S)
    meta = {}
    for line in m.group(1).split('\n'):
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()
    return meta, m.group(2)


def faq_items(body):
    """The FAQ at the bottom of the page, for Google: <details class="faq-item"><summary>Q</summary><p>A</p></details>."""
    return [(re.sub(r'<[^>]+>', '', q).strip(), a.strip())
            for q, a in re.findall(r'<details class="faq-item">\s*<summary>(.*?)</summary>\s*(.*?)</details>', body, re.S)]


def model(lang):
    meta, body = read(lang)
    stats = [x.split('=', 1) for x in meta['stats'].split(' | ')]
    top = section(facts([(b, s) for b, s in stats]) + f'<p class="mt1"><small>{meta["updated"]}</small></p>', 'sec-tight', 'stats', 'wrap wrap-n')
    ld = [x for x in json.loads(meta['ld']) if x.get('@type') != 'FAQPage']
    for x in ld:
        if isinstance(x.get('isPartOf'), dict):
            x['isPartOf']['name'] = 'karsog.com'
    fq = faq_items(body)
    if fq:
        ld.append(faq_ld(fq))
    return dict(path='/rti/', lang=lang, kind='rti', hero='band', title=meta['title'], desc=meta['desc'],
                kicker=meta['kicker'], h1=meta['h1'], lede=meta['lede'],
                crumbs=[(L(lang, 'RTI replies', 'आरटीआई जवाब'), '/rti/')],
                body=top + f'<div class="wrap wrap-n rti">{body}</div>\n'
                     + comments('rti', lang, None, L(lang, 'Filed an RTI about Karsog, or know what happened next? Share it here.',
                                                     'करसोग के बारे में आरटीआई लगाई है, या आगे क्या हुआ यह पता है? यहाँ बताइए।')),
                ld=ld, styles=['/assets/rti.css'], scripts=['/assets/rti.js'], og='/og/rti.jpg')
