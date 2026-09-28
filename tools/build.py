#!/usr/bin/env python3
"""Build every page of karsog.com in English and Hindi.

Run from the repo root:  python3 tools/build.py            (all pages)
                          python3 tools/build.py home bus    (only some groups)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout, p_home, p_bus, p_guide, p_tools

GROUPS = {
    'home': lambda lang: [p_home.model(lang)],
    'bus': lambda lang: [p_bus.stand(lang), p_bus.private(lang), p_bus.corridor(lang, 'mandi'), p_bus.corridor(lang, 'shimla')] + p_bus.dest_pages(lang),
    'guides': lambda lang: [p_guide.model(n, lang) for n in p_guide.available(lang)],
    'tools': lambda lang: [p_tools.weather(lang), p_tools.distance(lang), p_tools.hotels(lang), p_tools.mandi_rates(lang)],
}


def main(args):
    groups = args or list(GROUPS)
    n = 0
    for g in groups:
        for lang in ('en', 'hi'):
            for m in GROUPS[g](lang):
                layout.write(m)
                n += 1
    print(f'built {n} pages')


if __name__ == '__main__':
    main(sys.argv[1:])
