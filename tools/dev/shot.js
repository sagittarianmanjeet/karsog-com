// node shot.js <outdir> <path>...  -> screen-by-screen shots like a visitor scrolling (desktop d_*, phone m_*)
const { chromium } = require('/tmp/claude-0/node_modules/playwright');
const out = process.argv[2], paths = process.argv.slice(3);
const MOCK = JSON.parse(require('fs').readFileSync(__dirname + '/mock.json', 'utf8'));  // run: node tools/dev/shot.js <outdir> / /hi/ (local server on :8766)
const only = process.env.ONLY || 'dm';
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const [name, vp, dpr, mobile] of [['d', { width: 1440, height: 900 }, 1, false], ['m', { width: 390, height: 844 }, 2, true]]) {
    if (!only.includes(name)) continue;
    const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: dpr, isMobile: mobile, hasTouch: mobile, timezoneId: 'Asia/Kolkata' });
    await ctx.route(/open-meteo\.com/, r => { const u = r.request().url(); let b = MOCK.fc;
      if (u.includes('air-quality')) b = MOCK.aq; else if (u.includes('archive')) b = MOCK.arch; else if (u.includes('latitude=31.4784,')) b = MOCK.near;
      r.fulfill({ contentType: 'application/json', body: JSON.stringify(b) }); });
    await ctx.route(/\/api\/mandi\/latest/, r => r.fulfill({ contentType: 'application/json', body: JSON.stringify(MOCK.mandi) }));
    await ctx.route(/googletagmanager|google-analytics|challenges\.cloudflare/, r => r.abort());
    const pg = await ctx.newPage();
    const errs = [];
    pg.on('pageerror', e => errs.push(String(e)));
    for (const p of paths) {
      errs.length = 0;
      await pg.goto('http://localhost:8766' + p, { waitUntil: 'networkidle' }).catch(e => errs.push('goto ' + e));
      await pg.waitForTimeout(500);
      const H = await pg.evaluate(() => document.documentElement.scrollHeight);
      const slug = (p.replace(/\//g, '_') || '_');
      let i = 0;
      for (let y = 0; y < H; y += vp.height) {
        await pg.evaluate(y => window.scrollTo(0, y), y);
        await pg.waitForTimeout(450);
        await pg.screenshot({ path: `${out}/${name}${slug}${String(i).padStart(2, '0')}.png` });
        i++;
      }
      const ow = await pg.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      console.log(name, p, 'height', H, 'screens', i, 'overflowX', ow, errs.length ? 'ERR ' + errs.join(' | ').slice(0, 300) : '');
    }
    await ctx.close();
  }
  await b.close();
})();
