# karsog.com

Source of [karsog.com](https://karsog.com), a local guide to Karsog Valley, Mandi district, Himachal Pradesh: bus timings, mandi rates, temples, weather and drone photos.

## How it works

- Site files are in `public/`. Every change merged into `main` goes live automatically (Cloudflare Workers Builds, config in `wrangler.jsonc`).
- The menu (tabs) is the same on every page and lives in one place: `tools/sitenav.py`. To change it, edit `TABS` there and run `python3 tools/sitenav.py`.
- Tabs: Home · Buses · Places & Temples · Photos · Plan a Trip · Mandi Rates · Useful Numbers · RTI.
- `tools/busgen.py` rebuilds the bus stand, destination and private bus pages from `data/karsog-bus-stand-board.csv` and `data/karsog-private-buses.csv`.
- `tools/gallery-build.py` (run on the Mac) rebuilds the drone photo pages, the `/photos/` page and the homepage photo teaser.
- Both generators finish by running `tools/sitenav.py`.

## Contributing

1. Fork this repository and make your change on a branch in your fork.
2. Open a pull request. Say what you changed and, for any fact (a bus time, phone number, distance), where it can be verified.
3. Nothing goes live until the owner reviews and merges it.

We publish only what can be verified. Pull requests that add unsourced facts will not be merged.

## Copyright

Photos and drone footage © Karsog Miles. Not for reuse without permission.
Text and code © karsog.com.
