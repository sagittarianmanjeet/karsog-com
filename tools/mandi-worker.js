// karsog.com mandi rates — Cloudflare Worker "karsog-mandi" + D1 (binding: DB)
// Pulls daily APMC prices (Agmarknet via data.gov.in) on a schedule, stores history,
// and serves a small JSON API for karsog.com/mandi-rates/. Deployed separately from the site
// (Cloudflare dashboard → Workers → karsog-mandi → Edit code); this file is the source of truth.
//
// Bindings / settings (Cloudflare dashboard → Worker → Settings):
//   D1 binding       DB            → database "karsog-mandi"
//   Service binding  SELF          → this same Worker, "karsog-mandi"
//   Secret           DATA_GOV_KEY  → your data.gov.in API key
//   Secret           ADMIN_KEY     → optional; any long password, only for a manual refresh via /api/mandi/run
//   Variable         STATES        → optional, default "Himachal Pradesh" (comma-separated list)
//   Email binding    ALERT         → send_email to sagittarian.manjeet@gmail.com
//   Placement        Region: aws:ap-south-1 (Mumbai)
//   Route            karsog.com/api/mandi*   (includes /api/mandi/ingest, used by the PC script)
//   Cron             30 6,9,12 * * *   (12:00, 15:00, 18:00 IST)
//
// Why SELF and the Mumbai placement: since 26 Sep 2026 data.gov.in refuses connections from outside
// India (the Worker got HTTP 520/521/524 on every run, while the same API answers normally from an
// Indian connection). Cron runs execute wherever Cloudflare chooses and placement does not apply to
// them, so the scheduled handler calls this Worker's own fetch handler through the SELF binding;
// fetch handlers do follow the placement, so the data.gov.in request leaves from Mumbai.
//
// 8 Oct 2026: the Mumbai placement did NOT help, and a test from GitHub Actions (US) was refused too:
// data.gov.in refuses connections from data-centre/foreign networks. Prices now come from Manjeet's Ubuntu PC
// (tools/pc-mandi/), which fetches them ~10 min after it is switched on and POSTs them to /api/mandi/ingest.
// The Worker's own scheduled pull is kept: it costs nothing and resumes by itself if NIC lifts the block.
// The internal run is reachable only through SELF: public requests arrive with karsog.com or a
// workers.dev hostname, never the made-up host INTERNAL_HOST.

import { EmailMessage } from 'cloudflare:email';

// Same dataset, two addresses. Since 26 Sep 2026 api.data.gov.in refuses connections from everywhere (tested
// 8 Oct from a home connection in Himachal too). www.data.gov.in/backend/dataapi serves the same JSON and works from
// India, but its Akamai front returns "Access Denied" to US servers. Tried in this order.
const RESOURCES = [
  'https://www.data.gov.in/backend/dataapi/v1/resource/9ef84268-d588-465a-a308-a864a43d0070',
  'https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070'
];
const UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36 (karsog.com mandi rates; +https://karsog.com/mandi-rates/)';
const KEEP_DAYS_LATEST = 10;   // a market's last report older than this is dropped from "latest"
const HISTORY_DAYS = 90;
const INTERNAL_HOST = 'karsog-mandi.internal';

const J = (o, s = 200, cache = 'no-store') => new Response(JSON.stringify(o), {
  status: s,
  headers: { 'content-type': 'application/json;charset=utf-8', 'cache-control': cache }
});

function same(a, b) {
  a = String(a || ''); b = String(b || '');
  if (!a || !b || a.length !== b.length) return false;
  let r = 0; for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return r === 0;
}

// "25/09/2026" -> "2026-09-25"
function isoDate(s) {
  const m = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/.exec(String(s || '').trim());
  if (!m) return null;
  return `${m[3]}-${m[2].padStart(2, '0')}-${m[1].padStart(2, '0')}`;
}
function daysAgo(n) {
  const d = new Date(Date.now() + 5.5 * 3600e3 - n * 86400e3); // IST calendar day
  return d.toISOString().slice(0, 10);
}
const num = v => { const n = Math.round(Number(v)); return Number.isFinite(n) && n > 0 ? n : null; };
const txt = v => String(v ?? '').trim().slice(0, 80);

async function pullState(env, state, base) {
  const out = [];
  let offset = 0, total = Infinity;
  for (let page = 0; page < 40 && offset < total; page++) {
    const u = new URL(base);
    u.searchParams.set('api-key', env.DATA_GOV_KEY);
    u.searchParams.set('format', 'json');
    u.searchParams.set('limit', '1000');
    u.searchParams.set('offset', String(offset));
    u.searchParams.set('filters[state.keyword]', state);
    const r = await fetch(u, { headers: { accept: 'application/json', 'user-agent': UA, referer: 'https://www.data.gov.in/' } });
    if (!r.ok) throw new Error(`${new URL(base).hostname} HTTP ${r.status} for ${state}`);
    const j = await r.json();
    if (j.status && j.status !== 'ok') throw new Error(`data.gov.in: ${String(j.message || j.status).slice(0, 120)}`);
    const recs = Array.isArray(j.records) ? j.records : [];
    total = Number(j.total) || 0;
    out.push(...recs);
    if (!recs.length) break;
    offset += recs.length;
  }
  return out;
}

async function run(env, where = '') {
  const started = Date.now();
  try {
    if (!env.DATA_GOV_KEY) throw new Error('DATA_GOV_KEY secret is not set');
    const states = String(env.STATES || 'Himachal Pradesh').split(',').map(s => s.trim()).filter(Boolean);
    const errors = [];
    for (const base of RESOURCES) {
      try {
        const rows = [];
        for (const st of states) rows.push(...await pullState(env, st, base));
        return await save(env, rows, started, `${where} via ${new URL(base).hostname}`);
      } catch (e) { errors.push(String(e && e.message || e)); }
    }
    throw new Error(errors.join(' | '));
  } catch (e) {
    await log(env, 0, 0, (String(e && e.message || e) + where).slice(0, 300));
    return { ok: false, error: String(e && e.message || e) };
  }
}

// Store raw data.gov.in records (from this Worker's own pull or handed over by the PC script).
async function save(env, rows, started, where) {
  const stmt = env.DB.prepare(
    `INSERT INTO prices (d, state, district, market, commodity, variety, grade, min_p, max_p, modal_p, fetched)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
     ON CONFLICT (d, market, commodity, variety, grade) DO UPDATE SET
       min_p = excluded.min_p, max_p = excluded.max_p, modal_p = excluded.modal_p,
       district = excluded.district, state = excluded.state, fetched = excluded.fetched`
  );
  const batch = [];
  for (const r of rows) {
    if (!r || typeof r !== 'object') continue;
    const d = isoDate(r.arrival_date);
    const modal = num(r.modal_price);
    if (!d || !modal || !r.market || !r.commodity) continue;
    if (d > daysAgo(-1)) continue; // no future dates
    batch.push(stmt.bind(d, txt(r.state), txt(r.district), txt(r.market), txt(r.commodity),
      txt(r.variety), txt(r.grade), num(r.min_price), num(r.max_price), modal, started));
  }
  for (let i = 0; i < batch.length; i += 100) await env.DB.batch(batch.slice(i, i + 100));
  await buildSnapshot(env);
  await log(env, 1, batch.length, `ok: ${rows.length} fetched, ${batch.length} saved${where}`);
  return { ok: true, fetched: rows.length, saved: batch.length };
}

// Run the fetch from the Worker's placed location (Mumbai) when the SELF binding exists.
async function runPlaced(env) {
  if (!env.SELF) return run(env, ' (unplaced: SELF binding missing)');
  try {
    const r = await env.SELF.fetch(`https://${INTERNAL_HOST}/internal/run`, { method: 'POST' });
    return await r.json();
  } catch (e) {
    await log(env, 0, 0, ('SELF call failed: ' + String(e && e.message || e)).slice(0, 300));
    return { ok: false };
  }
}

async function log(env, ok, n, msg) {
  try {
    await env.DB.batch([
      env.DB.prepare('INSERT INTO runs (ts, ok, rows_in, msg) VALUES (?, ?, ?, ?)').bind(Date.now(), ok, n, msg),
      env.DB.prepare('DELETE FROM runs WHERE ts < ?').bind(Date.now() - 60 * 86400e3)
    ]);
  } catch { /* logging must never break a run */ }
}

// One pre-built JSON row → each page view costs a single D1 read.
async function buildSnapshot(env) {
  const { results } = await env.DB.prepare(
    `WITH latest AS (
       SELECT market, commodity, variety, grade, MAX(d) AS md
       FROM prices WHERE d >= ? GROUP BY market, commodity, variety, grade)
     SELECT p.d, p.state, p.district, p.market, p.commodity, p.variety, p.grade, p.min_p, p.max_p, p.modal_p,
       (SELECT q.modal_p FROM prices q WHERE q.market = p.market AND q.commodity = p.commodity
          AND q.variety = p.variety AND q.grade = p.grade AND q.d < p.d ORDER BY q.d DESC LIMIT 1) AS prev_p,
       (SELECT q.d FROM prices q WHERE q.market = p.market AND q.commodity = p.commodity
          AND q.variety = p.variety AND q.grade = p.grade AND q.d < p.d ORDER BY q.d DESC LIMIT 1) AS prev_d
     FROM prices p JOIN latest l
       ON p.market = l.market AND p.commodity = l.commodity AND p.variety = l.variety AND p.grade = l.grade AND p.d = l.md
     ORDER BY p.district, p.market, p.commodity`
  ).bind(daysAgo(KEEP_DAYS_LATEST)).all();

  const cols = ['d', 'state', 'district', 'market', 'commodity', 'variety', 'grade', 'min', 'max', 'modal', 'prev', 'prevD'];
  const rows = results.map(r => [r.d, r.state, r.district, r.market, r.commodity, r.variety, r.grade,
    r.min_p, r.max_p, r.modal_p, r.prev_p ?? null, r.prev_d ?? null]);
  const json = JSON.stringify({ built: Date.now(), cols, rows });
  await env.DB.prepare('INSERT INTO snapshot (id, built, json) VALUES (1, ?, ?) ON CONFLICT (id) DO UPDATE SET built = excluded.built, json = excluded.json')
    .bind(Date.now(), json).run();
}

async function cached(req, ctx, ttl, make) {
  const cache = caches.default;
  const key = new Request(new URL(req.url).toString(), { method: 'GET' });
  const hit = await cache.match(key);
  if (hit) return hit;
  const res = await make();
  if (res.status === 200) {
    res.headers.set('cache-control', `public, max-age=${ttl}`);
    ctx.waitUntil(cache.put(key, res.clone()));
  }
  return res;
}

const SAFE = /^[\p{L}\p{N} ().,&'\/-]{1,80}$/u;

export default {
  async scheduled(event, env, ctx) {
    ctx.waitUntil(runPlaced(env).then(() => new Date(event.scheduledTime).getUTCHours() === 12 ? healthCheck(env) : null));
  },

  async fetch(req, env, ctx) {
    const u = new URL(req.url);
    const path = u.pathname.replace(/\/+$/, '');

    // Internal: the scheduled handler's run, reached only through the SELF binding.
    if (u.hostname === INTERNAL_HOST && path === '/internal/run' && req.method === 'POST') {
      const colo = (req.cf && req.cf.colo) ? ` [${req.cf.colo}]` : '';
      return J(await run(env, colo));
    }

    // Latest price per market/commodity/variety/grade (+ previous report for change)
    if (path === '/api/mandi/latest' && req.method === 'GET') {
      return cached(req, ctx, 900, async () => {
        const row = await env.DB.prepare('SELECT json FROM snapshot WHERE id = 1').first();
        if (!row) return J({ built: 0, cols: [], rows: [] });
        return new Response(row.json, { headers: { 'content-type': 'application/json;charset=utf-8' } });
      });
    }

    // Price history for one line: ?market=&commodity=&variety=&grade=
    if (path === '/api/mandi/history' && req.method === 'GET') {
      const p = ['market', 'commodity', 'variety', 'grade'].map(k => (u.searchParams.get(k) || '').trim());
      if (!SAFE.test(p[0]) || !SAFE.test(p[1]) || (p[2] && !SAFE.test(p[2])) || (p[3] && !SAFE.test(p[3])))
        return J({ error: 'bad query' }, 400);
      return cached(req, ctx, 3600, async () => {
        const { results } = await env.DB.prepare(
          `SELECT d, min_p, max_p, modal_p FROM prices
           WHERE market = ? AND commodity = ? AND variety = ? AND grade = ? AND d >= ? ORDER BY d ASC`
        ).bind(p[0], p[1], p[2], p[3], daysAgo(HISTORY_DAYS)).all();
        return J({ points: results.map(r => [r.d, r.min_p, r.max_p, r.modal_p]) });
      });
    }

    if (path === '/api/mandi/alert-test' && req.method === 'GET') {
      const done = await env.DB.prepare("SELECT 1 AS x FROM runs WHERE msg = 'test alert sent'").first();
      if (done) return J({ error: 'Test email was already sent once.' }, 409);
      try {
        await sendAlert(env, 'karsog.com alerts are working', 'Test email. From now on you get an email here only if mandi rates stop updating or karsog.com pages stop loading (checked daily at 6 PM IST).');
        await log(env, 3, 0, 'test alert sent');
        return J({ ok: true, sent: true });
      } catch (e) { return J({ ok: false, error: String(e && e.message || e) }, 500); }
    }

    // Health check: last runs (no secrets)
    if (path === '/api/mandi/status' && req.method === 'GET') {
      const { results } = await env.DB.prepare('SELECT ts, ok, rows_in, msg FROM runs ORDER BY ts DESC LIMIT 10').all();
      const days = await env.DB.prepare('SELECT COUNT(DISTINCT d) AS days, MIN(d) AS first, MAX(d) AS last, COUNT(*) AS rows FROM prices').first();
      return J({ runs: results, stored: days, colo: (req.cf && req.cf.colo) || null });
    }

    // Hand-over from the PC script (tools/pc-mandi/): POST {"key":"<DATA_GOV_KEY>","records":[...]}
    // The PC fetches data.gov.in from an Indian home connection and sends the raw records here.
    if (path === '/api/mandi/ingest' && req.method === 'POST') {
      let d; try { d = await req.json(); } catch { return J({ error: 'Bad request.' }, 400); }
      if (!env.DATA_GOV_KEY || !same(d && d.key, env.DATA_GOV_KEY)) return J({ error: 'Wrong key.' }, 403);
      if (!Array.isArray(d.records) || d.records.length > 20000) return J({ error: 'records must be a list (max 20000).' }, 400);
      const from = txt(d.from || 'pc').replace(/[^\w .-]/g, '').slice(0, 30);
      try { return J(await save(env, d.records, Date.now(), ` (via ${from})`)); }
      catch (e) {
        await log(env, 0, 0, ('ingest failed: ' + String(e && e.message || e)).slice(0, 300));
        return J({ ok: false, error: 'save failed' }, 500);
      }
    }

    // Manual refresh: POST {"key":"<ADMIN_KEY>"} — runs from the placed location too
    if (path === '/api/mandi/run' && req.method === 'POST') {
      let d; try { d = await req.json(); } catch { return J({ error: 'Bad request.' }, 400); }
      if (!env.ADMIN_KEY || !same(d.key, env.ADMIN_KEY)) return J({ error: 'Wrong key.' }, 403);
      const colo = (req.cf && req.cf.colo) ? ` [${req.cf.colo}]` : '';
      return J(await run(env, colo));
    }

    return J({ error: 'Not found.' }, 404);
  }
};

// ---- Health alerts (email via Email Routing; binding: ALERT = send_email → sagittarian.manjeet@gmail.com) ----
// Runs after the 12:30 UTC cron (18:00 IST). At most one email per 20 hours.
// Alerts when: newest price older than 3 days, or karsog.com pages not loading.
const ALERT_TO = 'sagittarian.manjeet@gmail.com';
const ALERT_FROM = 'alerts@karsog.com';
const CHECK_PAGES = ['https://karsog.com/', 'https://karsog.com/karsog-bus-stand/', 'https://karsog.com/mandi-rates/'];

async function sendAlert(env, subject, body) {
  if (!env.ALERT) throw new Error('ALERT binding missing');
  const id = `<${Date.now()}.${Math.random().toString(36).slice(2)}@karsog.com>`;
  const raw = [
    `From: karsog.com alerts <${ALERT_FROM}>`,
    `To: <${ALERT_TO}>`,
    `Subject: ${subject}`,
    `Message-ID: ${id}`,
    `Date: ${new Date().toUTCString()}`,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=utf-8',
    'Content-Transfer-Encoding: 8bit',
    '',
    body
  ].join('\r\n');
  await env.ALERT.send(new EmailMessage(ALERT_FROM, ALERT_TO, raw));
}

async function healthCheck(env) {
  const problems = [];
  const now = Date.now();
  const newest = await env.DB.prepare('SELECT MAX(d) AS d FROM prices').first();
  if (!newest || !newest.d || newest.d < daysAgo(3)) {
    problems.push(`Mandi rates: newest price is dated ${newest && newest.d || 'never'} Is the Ubuntu PC being switched on? Its script hands the prices over (tools/pc-mandi/).`);
  }
  for (const p of CHECK_PAGES) {
    try {
      const r = await fetch(p, { headers: { 'user-agent': 'karsog-healthcheck' }, cf: { cacheTtl: 0 } });
      if (r.status !== 200) problems.push(`${p} returned HTTP ${r.status}`);
    } catch (e) { problems.push(`${p} failed to load: ${String(e && e.message || e).slice(0, 120)}`); }
  }
  if (!problems.length) return { ok: true };

  const recent = await env.DB.prepare('SELECT MAX(ts) AS t FROM runs WHERE ok = 2').first();
  if (recent && recent.t && now - recent.t < 20 * 3600e3) return { ok: false, problems, emailed: false };
  const body = 'Something on karsog.com needs a look:\n\n- ' + problems.join('\n- ') +
    '\n\nStatus: https://karsog.com/api/mandi/status\nThis email is sent at most once a day while a problem lasts.';
  try {
    await sendAlert(env, 'karsog.com: ' + problems.length + ' problem(s)', body);
    await log(env, 2, 0, 'alert sent: ' + problems.join(' | ').slice(0, 250));
    return { ok: false, problems, emailed: true };
  } catch (e) {
    await log(env, 0, 0, 'alert email failed: ' + String(e && e.message || e).slice(0, 200));
    return { ok: false, problems, emailed: false };
  }
}
