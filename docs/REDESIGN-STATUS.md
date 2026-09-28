# Redesign + Hindi version — status and how to resume

Last updated 28 Sep 2026. Work lives on the `redesign` branch. **Not merged**: the live site (main) is unchanged.
Some pages on this branch are in the new design and some are still old, so don't merge until everything below is done.

## Done

- **Design system**: `public/assets/site.css`, `site.js`, `icons.svg` (Lucide), self-hosted fonts in `assets/fonts/`, `weather.js`, `mandi.js`.
- **One builder for the whole site**: `python3 tools/build.py [home bus guides tools]`
  - `tools/layout.py` page shell (head, SEO, hreflang, header, phone bottom bar, menu sheet, footer, WhatsApp update form)
  - `tools/ui.py` menus and interface text (English + Hindi), `tools/data.py` buses, fairs, photos, distances, guide list
  - `p_home.py`, `p_bus.py`, `p_guide.py`, `p_tools.py` build the pages
- **Rebuilt in English and Hindi**: home, bus stand, private buses, Mandi ⇄ Karsog, Shimla ⇄ Karsog, 28 bus destination pages, weather, distance, hotels, mandi rates.
- **Guides rewritten (English only so far)** in `content/en/`: mahunag, mamleshwar, kao, shikari-devi, kamru-nag, tattapani, pangna-fort, chindi, janjehli.
- **Hindi glossary**: `docs/hindi-glossary.md` (local spellings counted from local posts).
- Preview screenshots of home, Hindi home, Mahunag guide sent to Manjeet on 28 Sep for approval.

## Facts checked and corrected

- **Distances** now come from Google Maps (fastest route from Karsog bus stand, 28 Sep 2026), in `tools/data.py` → `DIST`.
  The old OpenStreetMap figures were wrong because OSM is missing roads:
  - Shikari Devi was 103 km and is really 22 km, by the Shikari Temple road, which closes in winter.
  - Janjehli was 88 km and is really 27 km by the same road, or 84 km via Chhatri.
  - Other routes: Shimla 94 km, Mandi 99, Sundernagar 80, Rampur 75, Tattapani 46, Pangna 19, Mahunag 26, Chindi 7 (15 by the main road), Kao 7, Mamleshwar 2.3, Rohanda 52, Churag 13, Chhatri 48, Nerchowk 86, Solan 133, Bhuntar 150, Kullu 163, Manali 199, Chandigarh 217, Delhi 434.
- Mandi district site (hpmandi.nic.in):
  - Shikari Devi is at 3,359 m, 18 km from Janjehli by a jeepable road and 21 km from Karsog.
  - Kamru Nag is a 6 km trek from Rohanda (3–4 hours). Rohanda is 35 km from Sundernagar and 47 km from Mandi.
- Fixed old errors:
  - The Mahunag Mela is in mid-May, not April.
  - The Mamleshwar "7th century" claim is removed.
  - The Kamru Nag page said Rohanda was 30–35 km from Karsog. It is 52 km.
  - The Janjehli page said 40 km. The Chindi page said 15 km.
  - The "rhinoceros hide" and "6-foot" claims for Bhima's drum are removed.
- The board CSV's `note` column (covered / handwritten) is no longer shown to travellers.

## Still to do (in this order)

1. **Hindi guides**: write `content/hi/<name>.html` for the 9 guides.
   - Keep the same header keys (see the docstring in `p_guide.py`) and follow the glossary.
   - Change internal links to `/hi/…`.
2. **Hindi data**:
   - `data/devtas-hi.json`, the Hindi of `data/devtas.json`, for the temples page.
   - A `"hi"` title for every video in `data/videos.json`.
3. **Port the remaining pages** to the new builder, in both languages:
   - Pages to port:
     - `/melas/`
     - `/devtas/` → `/temples/`, adding `public/_redirects` with `/devtas/ /temples/ 301`
     - `/places/`, `/plan/`
     - `/contacts/`, including the "Karsog at a glance" block from `extras.py`
     - `/photos/` hub
     - the 19 drone place pages, built from `public/photos/photos.json` and `places.json`
     - `/rides/` (video order: newest first, as on the old page)
     - `/rti/` and `/hi/rti/`
     - `404.html`
   - Get the old page text with `python3 tools/dev/h2t.py <outdir> public/<page>/index.html`.
   - `gallery-build.py` (runs on the Mac) should then only update the photos and `photos.json`, and call `build.py`.
4. **Site plumbing**:
   - `build.py` writes `sitemap.xml` with hreflang, plus the new manifest and icons (`favicon.ico`, `apple-touch-icon.png`, `/assets/logo.svg`).
   - Share images `/og/*.jpg` (1200×630, from the hero photos). Pages already link to these, but they don't exist yet.
   - Bump the `sw.js` cache.
   - `comments.js`: add Hindi labels using `data-lang`. Pages already pass it.
5. **Remove the old generators** once everything is ported: `busgen.py`, `extras.py`, `devtas.py`, `sitenav.py`, `pagekit.py`, `restructure.py`.
6. **Checks**:
   - link check, Lighthouse, and English/Hindi screenshots on phone and desktop
   - write `docs/SITE-AUDIT.md`
   - open pull request(s) for Manjeet to merge from the GitHub app

## Audit of the old site (details in docs/audit/pages-before.json)

- Lighthouse (mobile): performance 95–99, SEO 100, accessibility 92–96.
- Problems (all solved by the new builder for the pages already ported):
  - Accessibility: low-contrast gold text, links shown only by colour, and a lightbox image with empty alt on every drone page.
  - Speed: images not sized, and Google Fonts blocking the page from showing.
  - Linking: 28 thin bus pages that only the bus stand page linked to.
  - Hindi: the old `/hi/` page was out of date and mixed कारसोग with करसोग.
  - Metadata: no structured data on mandi rates, and many titles and descriptions too long.
  - Guide pages had their sections in a confusing order.
  - Duplicate image-gallery structured data, up to 17 copies on /mahunag/, /janjehli/ and /shikari-devi/, because gallery-build.py appended a new copy each run.
  - Facts disagreed between pages: distances, the Mahunag Mela date and "7th century".

## Open questions for Manjeet

- Is the new design approved? (Screenshots sent on 28 Sep.)
- Hemant's access: option 1 (collaborator with main protected) or option 2 (a GitHub organization with the Triage role)?
- Should the site have a news section?
- Should we set up Search Console?
- Please verify:
  - HRTC Mandi bus stand 01905-222415
  - Shimla ISBT 0177-2658788
  - the hotel names
- Mandi → Karsog buses at 6:00, 8:30, 12:00 and 15:00 are shown as "reported locally" (they come from the old site). Keep them or drop them?
- Set up a yearly December reminder to update the mela dates?

## How to resume

- Code: `git clone` sagittarianmanjeet/karsog-com, then `git checkout redesign`.
- Preview: `cd public && python3 -m http.server 8766`.
- Screenshots: `node tools/dev/shot.js <outdir> / /hi/ /mahunag/`
  - needs Playwright, using `/opt/pw-browsers/chromium`
  - mocks the weather and mandi APIs with `tools/dev/mock.json`
  - then `python3 tools/dev/sheet.py <outdir> m_ 4 0.5` makes phone-screen sheets.
