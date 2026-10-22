# karsog.com — to-do list

Shared list for Manjeet and any AI working on the site. Last updated 22 Oct 2026. Tick items off here when done.
Background: `docs/REDESIGN-STATUS.md` (22 Oct sections cover the Gemini / ChatGPT / DeepSeek / Meta AI reviews).

## Manjeet (only he can do these)

- [ ] Search Console → Request indexing, ~9 pages a day (daily quota). 22 Oct done: /about/, /hi/about/, /places/, /hi/places/, /, /hi/, /photos/, /karsog-bus-stand/, /mahunag/. Next: /photos/license/, /temples/, /plan/, /mandi-to-karsog-bus/, /shimla-to-karsog-bus/, /mamleshwar/, /shikari-devi/, /kao/, /tattapani/.
- [ ] Each Karsog Miles YouTube video description: link to the matching karsog.com page (Shikari Devi ride → `/shikari-devi/`, etc.).
- [ ] karsog.com link in the YouTube channel, Instagram and Facebook bios.
- [ ] Add the site to Bing Webmaster Tools (can import from Search Console).
- [ ] Ask Himachal Tourism, the Mandi district office and local Hindi press to link to the site (offer drone photos / bus timetable).
- [ ] Link to karsog.com from toolninja.in and pinkyfancystore.com.
- [ ] Hotels: collect verified phone numbers and rough prices for the town hotels.
- [ ] Do not add karsog.com to Wikipedia/Wikidata/OpenStreetMap as Karsog's "official website" (it isn't; conflict of interest).

## Site work (Claude can do)

- [ ] Mandi rates: working again (22 Oct 2026: last 10 runs OK via api.data.gov.in, prices dated 22 Oct, 20 Himachal markets) — no code change was needed, data.gov.in came back. If it breaks again (the alert email says so), the ready fallback is branch `mandi-from-pc` (manual /mandi-update page + Ubuntu PC script); it needs the Worker redeployed from the Cloudflare dashboard and an ADMIN_KEY secret set by Manjeet. Put api.data.gov.in first in its RESOURCES list, since the Worker still runs from IAD (USA). `mandi-via-actions` was only a reachability test and can be deleted.
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
