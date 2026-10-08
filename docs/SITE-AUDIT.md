# karsog.com — audit of the live site, 6 Oct 2026

## 8 Oct 2026: mandi source found, PC backup added

- Mumbai placement did not help. Tests: GitHub Actions (US) could not connect to `api.data.gov.in`, and neither
  could Manjeet's home connection in Himachal, so that host is down for everyone, not blocking Cloudflare.
- The data.gov.in site itself reads the same dataset from `www.data.gov.in/backend/dataapi/v1/resource/<id>` (same
  JSON, same API key). It worked from the home connection (476 Himachal prices dated 8 Oct) but returned Akamai
  "Access Denied" to GitHub Actions.
- `tools/mandi-worker.js` now tries that address first, then the old one, and accepts records at
  `POST /api/mandi/ingest` (authorised by ADMIN_KEY). Alert emails now fire only when the newest
  price is older than 3 days (no more daily "no update in 24 h" mails).
- Manual fallback: karsog.com/mandi-update (`public/mandi-update.html`). Manjeet enters the ADMIN_KEY password; his
  browser fetches the prices from data.gov.in (CORS allows karsog.com, tested 8 Oct) and sends them to the Worker.
- `tools/pc-mandi/`: script + installer for the Ubuntu PC, using the same password and endpoints.

## Mandi rates stopped updating on 25 Sep 2026

- The Worker `karsog-mandi` ran on schedule (12:00, 15:00, 18:00 IST) but every run since 26 Sep failed:
  data.gov.in answered HTTP 520/502/503/504/524, and from 30 Sep only 521. Only 25 Sep is stored (526 price lines).
- The same API answers normally from an Indian connection (checked from Manjeet's computer on 6 Oct), and a US server
  could not connect at all. So data.gov.in is refusing traffic from outside India; Cloudflare runs cron jobs anywhere.
- Fix (`tools/mandi-worker.js`): the scheduled run now calls the Worker's own fetch handler through a `SELF` service
  binding, and the Worker gets the placement hint `aws:ap-south-1` (Mumbai), so the request leaves from India.
  Needs the dashboard steps listed at the top of that file. After deploying, `/api/mandi/status` shows each run's colo
  in brackets (`[BOM]` = Mumbai).
- The page said "Mandi rates today" with 11-day-old prices and no warning. It now shows a notice whenever the newest
  report is more than two days old (English and Hindi). Agmarknet's "Sirmore" is shown as Sirmaur.

## Other findings

| Check | Result |
|---|---|
| Live pages | all 146 sitemap addresses return 200; `/devtas/` redirects; robots.txt and sitemap fine; no `noindex` except 404 |
| Links | 0 broken internal links or images on 148 files |
| Build | reproducible: a fresh build matched what is live |
| Weather, next bus, comments | working (one comment so far, approved) |
| Google | Search Console (6 Oct): sitemap submitted 26 Sep and read 2 Oct (146 pages found), but only 2 pages indexed; the rest "Discovered – currently not indexed". 165 web clicks in the last 3 months. Indexing requested on 6 Oct for /, /karsog-bus-stand/, /shikari-devi/, /places/, /kamru-nag/, /mahunag/, /tattapani/ |
| Fairs | Sharadiya Navratri had no dates although it falls this month. Added 2024: 3–11 Oct, 2025: 22 Sep–1 Oct, 2026: 11–19 Oct (Dussehra 20 Oct 2026) |
| Bus board | 5 HRTC departures have no known destination (covered or handwritten on the board): 02:00, 04:20, 09:30, 11:00, 23:00. The next-bus boards said "see board"; now "ask at the stand" / "बस अड्डे पर पूछें". The board needs a fresh look |
| Long titles/descriptions | as listed under Known limits below, plus `/contacts/`, `/places/`, `/weather/` descriptions just over 165 characters |
| Old branches | `add-private-bus-timings`, `buses-brand`, `melas-devtas`, `site-tabs`, `redesign` are all superseded by `main` and can be deleted |

# karsog.com — site audit of the redesign

Checked on 29 Sep 2026, on the `redesign` branch as handed over for review (147 pages: 73 in English, 73 in Hindi, and
`404.html`). The earlier audit of the old site is summarised in `docs/REDESIGN-STATUS.md` and `docs/audit/`.

## Summary

| Check | Result |
|---|---|
| Build | `python3 tools/build.py` builds 147 pages; running it twice gives identical files |
| Links | 21,331 links, images and share images on 148 files: 0 missing targets |
| Old addresses | all 77 pages of the live site exist on the branch or redirect (`/devtas/` → `/temples/`, 301) |
| HTML | no unclosed or nested tags on any page |
| SEO basics | every page has a title, description and one h1; every indexable page has a canonical and an English/Hindi hreflang pair; all JSON-LD is valid; no duplicate titles or descriptions |
| Images | every image has alt text and width/height |
| Hindi | all 73 English/Hindi pairs have the same structure (lists, tables, FAQs, headings, images) and the same numbers; the only differences are the same value written two ways (1¼ hours = 1 घंटा 15 मिनट, 24/7 = 24 घंटे) |
| Scripts | no script errors on 26 pages; RTI filters and search, fair calendar "this month", jump links, photo lightbox (open, next, Esc) and comments (English and Hindi) work |
| Lighthouse | accessibility 100 and SEO 100 on all 20 pages tested (table below) |
| Screens | phone (390 px) and desktop (1440 px) screenshots of the new pages in English and Hindi; no sideways scrolling |

## Lighthouse (mobile)

Measured on a local test server **without compression** and with Google Analytics blocked, so performance on
Cloudflare (which compresses files) should be the same or better. "Best practices" is 96 only because of console
errors from the blocked analytics script and the comments API, which the local server doesn't have.

| Page | Performance | Accessibility | Best practices | SEO | LCP (s) | CLS |
|---|---|---|---|---|---|---|
| `/` | 94 | 100 | 96 | 100 | 3.2 | 0 |
| `/contacts/` | 98 | 100 | 96 | 100 | 2.4 | 0 |
| `/hi/` | 84 | 100 | 96 | 100 | 3.9 | 0.001 |
| `/hi/melas/` | 96 | 100 | 96 | 100 | 2.7 | 0.001 |
| `/hi/plan/` | 96 | 100 | 96 | 100 | 2.7 | 0.001 |
| `/hi/rti/` | 90 | 100 | 96 | 100 | 3.3 | 0.001 |
| `/hi/shikari-devi/` | 93 | 100 | 96 | 100 | 3.2 | 0.001 |
| `/hi/temples/` | 95 | 100 | 96 | 100 | 2.9 | 0.003 |
| `/karsog-bus-stand/` | 97 | 100 | 96 | 100 | 2.6 | 0.013 |
| `/karsog-private-bus/` | 96 | 100 | 96 | 100 | 2.4 | 0.085 |
| `/mandi-to-karsog-bus/` | 97 | 100 | 96 | 100 | 2.5 | 0 |
| `/melas/` | 98 | 100 | 96 | 100 | 2.4 | 0 |
| `/nanj/` | 94 | 100 | 96 | 100 | 3.2 | 0 |
| `/photos/` | 93 | 100 | 96 | 100 | 3.2 | 0 |
| `/plan/` | 98 | 100 | 96 | 100 | 2.4 | 0 |
| `/rides/` | 99 | 100 | 96 | 100 | 2.3 | 0 |
| `/rti/` | 97 | 100 | 96 | 100 | 2.6 | 0 |
| `/shikari-devi/` | 96 | 100 | 96 | 100 | 2.7 | 0 |
| `/temples/` | 98 | 100 | 96 | 100 | 2.4 | 0.0 |
| `/weather/` | 99 | 100 | 96 | 100 | 2.3 | 0 |

## Fixed during this check

- **Broken links in FAQ answers**: an answer that contained a link (Mahunag and Shikari Devi, both languages) was cut
  short, leaving an unclosed link over the rest of the page. The FAQ reader in `tools/p_guide.py` now allows links.
- **RTI page**: its list of findings used the class `facts`, which the new design also uses for the stats boxes, so
  every amount showed as a big heading. Renamed to `says`; the RTI script now only looks inside the RTI section.
- **Headings in order** (accessibility): `/temples/`, `/melas/`, the bus pages and `/weather/` jumped from h1 to h3.
  Added section headings; the "Next buses" title is now a heading.
- **Layout shift**: the italic heading font is now preloaded on English pages (every h1 has an italic word). Shift on
  the bus stand page went from 0.17 to 0.01, on `/temples/` from 0.11 to 0.
- **Honest photo alt text**: temple cards described every photo as "(temple name), from the air"; they now use the photo's
  own caption. The Chindi Mata card no longer uses a photo of the PWD rest house.
- **"near Karsog"**: alt text and descriptions of photo places more than 8 km from town now say "near Karsog" instead
  of "Karsog, Mandi district" (Anni and Luhri, for example, are in Kullu district).
- **Private buses in Hindi**: the notes under some trips ("Runs via Bithri from 7 Sep 2025", "Service started 11 Dec
  2025"…) were missing on the Hindi page. Added in Hindi.
- **Photo pages**: clearer sentence listing what the photos show; correct wording for pages with one photo;
  captions "Janjehli 1/2/3" (the photographer's file numbers) are now "Janjehli"; shorter descriptions.
- **Fair dates** labelled "Dates by year" instead of "Past dates" (the list also has dates still to come).
- **Useful numbers**: long values (district, census) no longer squeeze into a narrow column on phones.
- **404 page**: the menu no longer marks "Photos" as the current section; the Hindi line is marked as Hindi.
- **Manifest** colours match the new design; the icon stamp file moved out of `public/`.

## Known limits

- Four descriptions are 172–259 characters (Google shows about 155): `/karsog-private-bus/` (same as the live site),
  `/mandi-rates/`, `/karsog-town/` and the Hindi `/contacts/`.
- Ride-video thumbnails load from YouTube (`i.ytimg.com`).
- Both spellings Sutlej and Satluj appear: guides say Sutlej, photo captions (from the photographer's file names) say
  Satluj.
- The Hindi home page is the slowest page (performance 84 locally): the Hindi font is 99 KB and the hero photo is the
  largest element. Worth re-checking on the live site after the merge.

## Page titles that changed

With no Search Console data we can't tell which of these pages already earn clicks. If some do, the old title can be
put back in the page's source (see the README table) before merging.

| Page | Old title (live) | New title |
|---|---|---|
| `/` | karsog.com — Karsog Bus Timings, Weather, Temples & Photos | Karsog Valley Guide — Buses, Weather, Temples & Melas |
| `/chindi/` | Chindi, Karsog — Sunset Point, Orchards & HPTDC Resort | Chindi, Karsog — Chindi Mata Temple, HPTDC Hotel & Sunset Views |
| `/contacts/` | Karsog Useful Numbers — Emergency, Hospital, Police, PIN Code 175011 & IFSC | Karsog Useful Numbers — Emergency, Hospital, Police, PIN 175011 & IFSC |
| `/distance/` | Distance from Karsog — Shimla, Mandi, Sundernagar, Rampur, Chandigarh, Delhi (km) | Distance from Karsog — Shimla, Mandi, Chandigarh, Delhi (km) |
| `/hotels/` | Hotels in Karsog, Himachal Pradesh — Where to Stay (HPTDC Chindi, Homestays) | Hotels in Karsog — HPTDC Chindi, Town Hotels & Homestays |
| `/janjehli/` | Janjehli Valley — Base for the Shikari Devi Trek | Janjehli Valley — Road from Karsog, Shikari Devi, Stay & Best Time |
| `/kamru-nag/` | Kamrunag Temple & Lake (Kamru Nag) — Trek Route, Mela Dates & Best Time | Kamru Nag Temple & Lake — Trek from Rohanda, Mela & How to Reach |
| `/kao/` | Kamaksha Devi Temple, Kao (Karsog) — Photos & How to Reach | Kamaksha Devi Temple, Kao (Karsog) — Navratri & How to Reach |
| `/karsog-bus-stand/` | Karsog Bus Timing — Bus Stand Time Table, All HRTC Departures (2026) | Karsog Bus Timing — Bus Stand Time Table (HRTC & Private) |
| `/karsog-private-bus/` | Karsog Private Bus Timings — Shimla, Sundernagar, Mandi, Rampur (2026) | Karsog Private Bus Timings — Shimla, Sundernagar, Mandi |
| `/mahunag/` | Mahunag Temple, Karsog — Timings, Fair & How to Reach | Mahunag Temple, Karsog — Mela Dates, Legend & How to Reach |
| `/mamleshwar/` | Mamleshwar Mahadev Temple, Karsog — 7th Century Shiva Temple | Mamleshwar Mahadev Temple, Karsog — Legend, Festivals & How to Reach |
| `/mandi-rates/` | Apple Rate Today — Himachal Mandi Rates (Karsog, Mandi, Solan, Parwanoo) | Apple Rate Today — Himachal Mandi Rates (Mandi, Shimla, Solan) |
| `/mandi-to-karsog-bus/` | Mandi to Karsog Bus Timings — HRTC First & Last Bus | Mandi to Karsog Bus Timing — HRTC & Private, Both Ways |
| `/melas/` | Karsog Melas & Festivals — Fair Dates Month by Month (Nalwar, Mahunag, Budhi Diwali) | Karsog Melas & Festivals — Fair Dates Month by Month |
| `/pangna-fort/` | Pangna Fort, Karsog — Kath-Kuni Tower of the Suket Kings | Pangna Fort & Mahamaya Temple, Karsog — History & How to Reach |
| `/photos/` | Karsog Photos — Drone Photos of 27 Places & Ride Videos | Karsog Photos — 339 Drone Photos of 27 Places & Ride Videos |
| `/plan/` | Plan a Karsog Trip — How to Reach, Taxi Rates, Hotels & Festivals | Plan a Karsog Trip — How to Reach, Taxis, Day Plans & Stay |
| `/rides/` | Karsog Miles — Motorcycle Ride Videos from Karsog Valley | Karsog Ride Videos — Karsog Miles on YouTube |
| `/shikari-devi/` | Shikari Devi Temple — Trek Route, Distance, Weather & Best Time | Shikari Devi Temple — Road from Karsog, Janjehli, Weather & Best Time |
| `/shimla-to-karsog-bus/` | Shimla to Karsog Bus Timings — HRTC Schedule & Fare | Shimla to Karsog Bus Timing — HRTC & Private, Both Ways |
| `/tattapani/` | Tattapani Hot Spring — Distance, Best Time & Rafting (Karsog) | Tattapani Hot Springs — Distance from Karsog, Lohri Mela & Best Time |
| `/weather/` | Karsog Weather Today — 7-Day Forecast, Rain, Snow & AQI (करसोग मौसम) | Karsog Weather Today — 7-Day Forecast, Rain, Snow & AQI |
