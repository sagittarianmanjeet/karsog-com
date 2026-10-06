# Redesign + Hindi version — status

Last updated 29 Sep 2026.

**State: live.** The `redesign` branch was merged into `main` (fast-forward to `24d99ab`) and deployed on 29 Sep 2026,
by Claude from GitHub Desktop at Manjeet's request. Every page is built by the new builder in English and Hindi
(147 pages), every old address still works (`/devtas/` redirects to `/temples/`), and the checks in
`docs/SITE-AUDIT.md` pass. After the deploy, all 146 sitemap pages returned 200 on karsog.com with the new design,
`/devtas/` redirected, the 404 page, service worker `karsog-v21`, RTI PDFs, and the comments and mandi APIs worked.

## Done

- **Design system**: `public/assets/site.css`, `site.js`, `icons.svg` (Lucide), self-hosted fonts in `assets/fonts/`,
  `weather.js`, `mandi.js`, and `rti.css` / `rti.js` for the RTI page.
- **One builder for the whole site**: `python3 tools/build.py` (see the README for what comes from where).
  The old generators (`busgen.py`, `extras.py`, `devtas.py`, `sitenav.py`, `pagekit.py`, `restructure.py`, `k2x.py`)
  are removed.
- **Pages, in English and Hindi**:
  - home; bus stand, private buses, Mandi ⇄ Karsog, Shimla ⇄ Karsog and 28 bus destination pages
  - weather, distances, hotels, mandi rates
  - 9 guides: Mahunag, Mamleshwar, Kao, Shikari Devi, Kamru Nag, Tattapani, Pangna, Chindi, Janjehli
  - `/melas/` (fair calendar with "this month"), `/temples/` (new, replaces `/devtas/`)
  - `/places/`, `/plan/`, `/contacts/`
  - `/photos/`, 19 drone-photo place pages, `/rides/` (30 ride videos)
  - `/rti/`
  - `404.html` (English with a Hindi line)
- **Hindi data**: `data/devtas-hi.json`, a Hindi title for every video in `data/videos.json`, Hindi names for the photo
  places (`data/photo-places.json`) and captions (`data/photo-labels-hi.json`).
- **Photo captions**: every drone photo has a caption (`label` in `public/photos/photos.json`), taken from the old pages.
  Alt text says only what the caption says, plus "Karsog" for places within 8 km of town and "near Karsog" for the rest
  (Anni and Luhri, for example, are in Kullu district).
- **Site plumbing**: `sitemap.xml` with hreflang (146 addresses), share images in `public/og/` (1200×630), `favicon.ico`,
  `apple-touch-icon.png`, `assets/logo.svg`, `public/_redirects`, service-worker cache `karsog-v21`, Hindi labels in the
  comments box, manifest colours matching the new design.
- **`tools/gallery-build.py`** now only makes the web versions of new photos, updates `photos.json` / `places.json`, and
  runs `build.py`.
- **Docs**: README, `AGENTS.md` (notes for AI assistants), `docs/SITE-AUDIT.md`, the glossary's list of spellings to confirm.

## Facts checked and corrected

- **Distances** come from Google Maps (fastest route from Karsog bus stand, 28 Sep 2026), in `tools/data.py` → `DIST`.
  The old OpenStreetMap figures were wrong because OSM is missing roads:
  - Shikari Devi was 103 km and is really 22 km, by the Shikari Devi road, which closes in winter.
  - Janjehli was 88 km and is really 27 km by the same road, or 84 km via Chhatri.
  - Other routes: Shimla 94 km, Mandi 99, Sundernagar 80, Rampur 75, Tattapani 46, Pangna 19, Mahunag 26, Chindi 7
    (15 by the main road), Kao 7, Mamleshwar 2.3, Rohanda 52, Churag 13, Chhatri 48, Nerchowk 86, Solan 133,
    Bhuntar 150, Kullu 163, Manali 199, Chandigarh 217, Delhi 434.
  - `data/devtas.json` now uses the same figures (it still had old ones for Mahunag, Mamleshwar, Chindi and Pangna).
- Mandi district site (hpmandi.nic.in):
  - Shikari Devi is at 3,359 m, 18 km from Janjehli by a jeepable road and 21 km from Karsog.
  - Kamru Nag is a 6 km trek from Rohanda (3–4 hours). Rohanda is 35 km from Sundernagar and 47 km from Mandi.
- Fixed old errors:
  - The Mahunag Mela is in mid-May, not April.
  - The Mamleshwar "7th century" claim is removed.
  - The Kamru Nag page said Rohanda was 30–35 km from Karsog. It is 52 km.
  - The Janjehli page said 40 km. The Chindi page said 15 km.
  - The "rhinoceros hide" and "6-foot" claims for Bhima's drum are removed.
  - The Chindi Mata card on `/temples/` no longer shows a photo: the only Chindi drone photos show the PWD rest house.
  - Fair dates are labelled "Dates by year" (the old "Past dates" label also covered dates still to come).
- The board CSV's `note` column (covered / handwritten) is no longer shown to travellers.

## Still to do

0. Deploy the mandi Worker fix (`tools/mandi-worker.js`, steps at the top of the file). See `docs/SITE-AUDIT.md`, 6 Oct 2026.
1. Submit `https://karsog.com/sitemap.xml` in Google Search Console (Manjeet; account action).
2. The merged `redesign` branch on GitHub can be deleted (or kept; it is fully merged).
3. The open questions below.

## Open questions for Manjeet

- Is the new design approved? (Screenshots sent on 28 Sep.)
- 23 page titles changed with the redesign (listed in `docs/SITE-AUDIT.md`). With no Search Console data we can't see
  which pages already earn clicks. Keep the new titles, or put the old ones back on pages you know people find?
- Hemant's access: option 1 (collaborator with `main` protected) or option 2 (a GitHub organization with the Triage role)?
- Should the site have a news section?
- Search Console: the site already has a Google verification file (`public/google0f68a3e8b74ac0f2.html`), so a
  Search Console property for karsog.com may exist. Can you check? Its click data would also answer the titles question.
- Please verify:
  - HRTC Mandi bus stand 01905-222415
  - Shimla ISBT 0177-2658788
  - Karsog Control Room +91 93172-07043 and the other numbers on `/contacts/`
  - the hotel names on `/hotels/` and `/plan/`
- Mandi → Karsog buses at 6:00, 8:30, 12:00 and 15:00 are shown as "reported locally" (they come from the old site).
  Keep them or drop them?
- Set up a yearly December reminder to update the mela dates?
- The Hindi village spellings at the end of `docs/hindi-glossary.md`: can someone local check them?

## How to resume

- Code: `git clone` sagittarianmanjeet/karsog-com, then `git checkout redesign`.
- Build: `python3 tools/build.py`. Preview: `cd public && python3 -m http.server 8766`.
- Screenshots: `node tools/dev/shot.js <outdir> / /hi/ /mahunag/`
  - needs Playwright, using `/opt/pw-browsers/chromium`
  - mocks the weather and mandi APIs with `tools/dev/mock.json`
  - then `python3 tools/dev/sheet.py <outdir> m_ 4 0.5` makes phone-screen sheets.
