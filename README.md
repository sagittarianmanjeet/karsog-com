# karsog.com

Source of [karsog.com](https://karsog.com), a local guide to Karsog Valley, Mandi district, Himachal Pradesh: bus timings, mandi rates, temples, fairs, weather and drone photos, in English and Hindi (`/hi/…`).

## How it works

- Site files are in `public/`. Every change merged into `main` goes live automatically (Cloudflare Workers Builds, config in `wrangler.jsonc`).
- Every page is made by one builder, in English and Hindi. Don't edit the `.html` files in `public/` by hand: change the source and rebuild.

```
python3 tools/build.py             # every page, then sitemap, share images and icons
python3 tools/build.py bus guides  # only some groups (home bus guides tools culture info photos rti misc)
```

Where things come from:

| What | Source | Built by |
|---|---|---|
| Menu, footer, interface words (EN + HI) | `tools/ui.py` | `tools/layout.py` (page shell) |
| HRTC and private bus timings | `data/karsog-bus-stand-board.csv`, `data/karsog-private-buses.csv` | `tools/p_bus.py` |
| Temple and place guides | `content/en/<name>.html`, `content/hi/<name>.html` | `tools/p_guide.py` |
| Temples page | `data/devtas.json`, `data/devtas-hi.json` | `tools/p_culture.py` |
| Fair calendar | `MELAS` in `tools/data.py` | `tools/p_culture.py` |
| Distances (`DIST`), hotels (`HOTELS`) | `tools/data.py`, `tools/p_tools.py` | `tools/p_tools.py` |
| Weather, mandi rates (live, in the browser) | Open-Meteo; Agmarknet via `/api/mandi` | `tools/p_tools.py` + `public/assets/weather.js`, `mandi.js` |
| Places, plan a trip, useful numbers | `tools/p_info.py` | `tools/p_info.py` |
| Drone photos and ride videos | `public/photos/photos.json`, `data/photo-places.json`, `data/photo-labels-hi.json`, `data/videos.json` | `tools/p_photos.py` |
| RTI replies | `content/rti/en.html`, `content/rti/hi.html` | `tools/p_rti.py` |
| 404 page | `tools/p_misc.py` | |
| Sitemap, share images (`/og/`), icons | | `tools/sitefiles.py` |

- New drone photos: run `tools/gallery-build.py` on the Mac, where the original photos are. It makes the web versions, updates `photos.json` and `places.json`, and runs `build.py`.
- Old addresses that moved are redirected in `public/_redirects` (for example `/devtas/` → `/temples/`).
- Hindi follows `docs/hindi-glossary.md`: the same facts as the English page, nothing added and nothing left out.
- Preview locally: `cd public && python3 -m http.server 8766`. Screenshot helpers are in `tools/dev/`.
- Notes for AI assistants working on this repo: `AGENTS.md`. Current state of the redesign: `docs/REDESIGN-STATUS.md`. Latest checks: `docs/SITE-AUDIT.md`.

## Contributing

1. Fork this repository and make your change on a branch in your fork.
2. Open a pull request. Say what you changed and, for any fact (a bus time, phone number, distance), where it can be verified.
3. Nothing goes live until the owner reviews and merges it.

We publish only what can be verified. Pull requests that add unsourced facts will not be merged.

## Copyright

Photos and drone footage © Karsog Miles. Not for reuse without permission.
Text and code © karsog.com.
