#!/usr/bin/env python3
"""Build every page of karsog.com in English and Hindi, then the sitemap.

Run from the repo root:  python3 tools/build.py            (all pages + sitemap)
                          python3 tools/build.py home bus    (only some groups; the sitemap is rebuilt only on a full run)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout, p_home, p_bus, p_guide, p_tools, p_culture, p_info, p_photos, p_rti, p_misc, sitefiles
from data import MISSING_HI

GROUPS = {
    'home': lambda lang: [p_home.model(lang)],
    'bus': lambda lang: [p_bus.stand(lang), p_bus.private(lang), p_bus.corridor(lang, 'mandi'), p_bus.corridor(lang, 'shimla')] + p_bus.dest_pages(lang),
    'guides': lambda lang: [p_guide.model(n, lang) for n in p_guide.available(lang)],
    'tools': lambda lang: [p_tools.weather(lang), p_tools.distance(lang), p_tools.hotels(lang), p_tools.mandi_rates(lang)],
    'culture': lambda lang: [p_culture.melas(lang), p_culture.temples(lang)],
    'info': lambda lang: [p_info.places(lang), p_info.plan(lang), p_info.contacts(lang)],
    'photos': lambda lang: [p_photos.hub(lang), p_photos.rides(lang)] + p_photos.places(lang),
    'rti': lambda lang: [p_rti.model(lang)],
    'misc': lambda lang: [p_misc.not_found()] if lang == 'en' else [],
}


def main(args):
    groups = args or list(GROUPS)
    n, models = 0, []
    for g in groups:
        for lang in ('en', 'hi'):
            for m in GROUPS[g](lang):
                layout.write(m)
                models.append(m)
                n += 1
    print(f'built {n} pages')
    if not args:
        print(sitefiles.finish(models))
    if MISSING_HI:
        print('photo captions with no Hindi yet (add them to data/photo-labels-hi.json):', ', '.join(sorted(MISSING_HI)))


if __name__ == '__main__':
    main(sys.argv[1:])
