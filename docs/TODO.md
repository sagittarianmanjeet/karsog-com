# karsog.com — to-do list

Shared list for Manjeet and any AI working on the site. Last updated 22 Oct 2026. Tick items off here when done.
Background: `docs/REDESIGN-STATUS.md` (22 Oct sections cover the Gemini / ChatGPT / DeepSeek / Meta AI reviews).

## Manjeet (only he can do these)

- [ ] Search Console → URL Inspection → Request indexing: `/places/` and `/about/` first, then ~10 key pages every few days.
- [ ] Each Karsog Miles YouTube video description: link to the matching karsog.com page (Shikari Devi ride → `/shikari-devi/`, etc.).
- [ ] karsog.com link in the YouTube channel, Instagram and Facebook bios.
- [ ] Add the site to Bing Webmaster Tools (can import from Search Console).
- [ ] Ask Himachal Tourism, the Mandi district office and local Hindi press to link to the site (offer drone photos / bus timetable).
- [ ] Link to karsog.com from toolninja.in and pinkyfancystore.com.
- [ ] Hotels: collect verified phone numbers and rough prices for the town hotels.
- [ ] Do not add karsog.com to Wikipedia/Wikidata/OpenStreetMap as Karsog's "official website" (it isn't; conflict of interest).

## Site work (Claude can do)

- [ ] Mandi rates: no new data since 25 Sep 2026. Branches `mandi-from-pc` and `mandi-via-actions` are not merged. Finish one feed, or hide/noindex `/mandi-rates/` until data flows.
- [ ] Drone-photo place pages are thin (about 130–200 words) and don't link to their bus pages: add "How to get there" with the matching `/bus/karsog-to-*/` link.
- [ ] 28 `/bus/karsog-to-*/` pages are thin (about 200 words, one template): enrich or noindex.
- [ ] Apple season wording: "September–October" on most pages, "roughly July to October" on `/hotels/` — make consistent.
- [ ] Kunhoo / Dar Kunhoo guide — only after verifying name, location and access.
- [ ] New guides when facts can be sourced: Karsog in winter/snow, apple season, 2–3 day itinerary, Shimla → Karsog by road.
- [ ] Weather and mandi pages: useful text when the live data can't load (bus widget already done).

## Done 22 Oct 2026

- [x] `/photos/license/` + licence fields on drone-photo ImageObjects (Search Console image-metadata warning).
- [x] `/about/` page (who makes the site, sources, corrections), linked from the footer.
- [x] `/places/`: distance table for the 9 guides + links to all 19 other photographed places.
- [x] Next-bus widget links to the full timetable when JavaScript doesn't run.
- [x] Checked: Cloudflare is not blocking Google (Search Console live test on `/places/`: "URL is available to Google").
