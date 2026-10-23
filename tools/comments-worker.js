// Comments and up/down votes for karsog.com, toolninja.in and kheloaurseekho.in — one Cloudflare Worker + D1 (binding: DB)
// Secrets: TURNSTILE_SECRET, ADMIN_KEY. Email binding: ALERT (send_email, via karsog.com Email Routing).
// Routes: karsog.com/api/comments*, toolninja.in/api/comments*, kheloaurseekho.in/api/comments*, and the same three with /api/votes*
// Votes: one per connection per page (up, down or none), no names, no Turnstile. Table `votes` is created on first use.
// kheloaurseekho.in is a children's site: every comment there waits for the owner's approval (moderate: true).
//
// Rules: a clean comment goes live at once. A comment containing a link, email, phone number,
// Aadhaar-like or PAN-like number (or any long number) is held until the owner approves it.
// The owner gets an email for every new comment, with a review link.
import { EmailMessage } from 'cloudflare:email';

const SITES = {
  'karsog.com': { id: 'karsog', name: 'karsog.com', url: p => `https://karsog.com/${p}/` },
  'www.karsog.com': { id: 'karsog', name: 'karsog.com', url: p => `https://karsog.com/${p}/` },
  'toolninja.in': { id: 'toolninja', name: 'ToolNinja', url: p => `https://toolninja.in/tools/${p}` },
  'www.toolninja.in': { id: 'toolninja', name: 'ToolNinja', url: p => `https://toolninja.in/tools/${p}` },
  'kheloaurseekho.in': { id: 'khelo', name: 'Khelo aur Seekho', url: p => `https://kheloaurseekho.in/${p === 'home' ? '' : p + '/'}`, moderate: true },
  'www.kheloaurseekho.in': { id: 'khelo', name: 'Khelo aur Seekho', url: p => `https://kheloaurseekho.in/${p === 'home' ? '' : p + '/'}`, moderate: true },
};
const SITE_BY_ID = { karsog: SITES['karsog.com'], toolninja: SITES['toolninja.in'], khelo: SITES['kheloaurseekho.in'] };
const ORIGINS = ['https://karsog.com', 'https://www.karsog.com', 'https://toolninja.in', 'https://www.toolninja.in', 'https://kheloaurseekho.in', 'https://www.kheloaurseekho.in'];
const PAGE = /^[a-z0-9-]{1,60}(?:\/[a-z0-9-]{1,60}){0,3}$/; // e.g. kamru-nag, bus/karsog-to-thunag, pdf-compressor, worksheets/class-1-maths/shapes
const ALERT_FROM = 'alerts@karsog.com';
const ALERT_TO = 'sagittarian.manjeet@gmail.com';

// Anything that looks like personal data or a link is held for approval.
const FLAGS = [
  [/https?:\/\/|www\.|\b[a-z0-9-]+\.(?:com|in|net|org|co|info|xyz|online|site|shop|app|io|me|link|ly|biz|top)\b/i, 'a link'],
  [/[\w.+-]+@[\w-]+\.[\w.]+/, 'an email address'],
  [/(?<!\d)\d{4}[\s-]?\d{4}[\s-]?\d{4}(?!\d)/, 'an Aadhaar-like number'],
  [/\b[a-z]{5}\d{4}[a-z]\b/i, 'a PAN-like code'],
  [/(?<!\d)(?:\+?91[\s-]?|0)?[6-9]\d{4}[\s-]?\d{5}(?!\d)/, 'a phone number'],
  [/\d[\d\s-]{8,}\d/, 'a long number'],
];
function flagged(text) {
  for (const [re, why] of FLAGS) if (re.test(text)) return why;
  return '';
}

const votesTable = { ready: false };
async function ensureVotes(env) {
  if (votesTable.ready) return;
  await env.DB.prepare('CREATE TABLE IF NOT EXISTS votes (site TEXT NOT NULL, page TEXT NOT NULL, iphash TEXT NOT NULL, v INTEGER NOT NULL, created INTEGER NOT NULL, PRIMARY KEY (site, page, iphash))').run();
  votesTable.ready = true;
}
async function tally(env, site, page) {
  const r = await env.DB.prepare('SELECT COALESCE(SUM(v = 1), 0) AS up, COALESCE(SUM(v = -1), 0) AS down FROM votes WHERE site = ? AND page = ?').bind(site, page).first();
  return { up: (r && r.up) || 0, down: (r && r.down) || 0 };
}

const J = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { 'content-type': 'application/json;charset=utf-8', 'cache-control': 'no-store' } });
const H = (html, s = 200) => new Response(html, { status: s, headers: { 'content-type': 'text/html;charset=utf-8', 'cache-control': 'no-store', 'x-robots-tag': 'noindex' } });
const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

async function sha(s) {
  const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
  return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join('');
}
async function hmac(key, msg) {
  const k = await crypto.subtle.importKey('raw', new TextEncoder().encode(key), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', k, new TextEncoder().encode(msg));
  return [...new Uint8Array(sig)].slice(0, 16).map(x => x.toString(16).padStart(2, '0')).join('');
}
function same(a, b) {
  a = String(a || ''); b = String(b || '');
  if (!a || !b || a.length !== b.length) return false;
  let r = 0; for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return r === 0;
}
const token = (env, id) => hmac(env.ADMIN_KEY || '', 'comment:' + id);

async function notify(env, host, c, why) {
  if (!env.ALERT) return;
  const site = SITE_BY_ID[c.site];
  const t = await token(env, c.id);
  const review = `https://${host}/api/comments/review?id=${c.id}&t=${t}`;
  const subject = (why ? `[${site.name}] Held for approval` : `[${site.name}] New comment`) + ` — ${c.page}`;
  const body = [
    why ? `This comment is waiting for your approval (${why}).` : 'This comment is live on the site.',
    '',
    `Page: ${site.url(c.page)}`,
    `Name: ${c.name}`,
    '',
    c.body,
    '',
    why ? `Approve or delete it here: ${review}` : `To hide or delete it: ${review}`,
  ].join('\n');
  const raw = [
    `From: ${site.name} comments <${ALERT_FROM}>`,
    `To: <${ALERT_TO}>`,
    `Subject: =?UTF-8?B?${btoa(unescape(encodeURIComponent(subject)))}?=`,
    `Message-ID: <c${c.id}.${Date.now()}@karsog.com>`,
    `Date: ${new Date().toUTCString()}`,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=utf-8',
    'Content-Transfer-Encoding: base64',
    '',
    btoa(unescape(encodeURIComponent(body))).replace(/.{76}/g, '$&\r\n'),
  ].join('\r\n');
  await env.ALERT.send(new EmailMessage(ALERT_FROM, ALERT_TO, raw));
}

export default {
  async fetch(req, env, ctx) {
    const u = new URL(req.url);
    const path = u.pathname.replace(/\/+$/, '');
    const site = SITES[u.hostname] || SITES['karsog.com'];

    // Public: approved comments for one page
    if (path === '/api/comments' && req.method === 'GET') {
      const page = u.searchParams.get('page') || '';
      if (!PAGE.test(page)) return J({ error: 'bad page' }, 400);
      const { results } = await env.DB.prepare(
        'SELECT id, name, body, created FROM comments WHERE site = ? AND page = ? AND approved = 1 ORDER BY created ASC LIMIT 500'
      ).bind(site.id, page).all();
      return J({ comments: results });
    }

    // Public: post a comment
    if (path === '/api/comments' && req.method === 'POST') {
      const origin = req.headers.get('origin');
      if (origin && !ORIGINS.includes(origin) && origin !== env.DEV_ORIGIN) return J({ error: 'Not allowed.' }, 403);
      let d; try { d = await req.json(); } catch { return J({ error: 'Bad request.' }, 400); }
      const page = String(d.page || '');
      const name = String(d.name || '').trim().slice(0, 60);
      const body = String(d.body || '').trim();
      if (!PAGE.test(page) || !name || body.length < 2 || body.length > 2000)
        return J({ error: 'Please enter your name and a comment (up to 2000 characters).' }, 400);

      const ip = req.headers.get('cf-connecting-ip') || '';
      const fd = new FormData();
      fd.append('secret', env.TURNSTILE_SECRET);
      fd.append('response', String(d.token || ''));
      if (ip) fd.append('remoteip', ip);
      let v = {};
      try { v = await (await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body: fd })).json(); }
      catch { return J({ error: 'Security check unavailable. Please try again in a minute.' }, 503); }
      if (!v.success) return J({ error: 'Verification failed. Please try again.' }, 403);

      const h = (await sha('kc|' + ip)).slice(0, 24);
      const r = await env.DB.prepare('SELECT COUNT(*) AS n FROM comments WHERE iphash = ? AND created > ?').bind(h, Date.now() - 3600000).first();
      if (r && r.n >= 10) return J({ error: 'Too many comments from this connection. Please try again later.' }, 429);

      const f = flagged(name + '\n' + body);
      const why = f ? 'it contains ' + f : (site.moderate ? 'every comment on this site is checked first' : '');
      const created = Date.now();
      const res = await env.DB.prepare('INSERT INTO comments (site, page, name, body, created, approved, iphash) VALUES (?, ?, ?, ?, ?, ?, ?)')
        .bind(site.id, page, name, body, created, why ? 0 : 1, h).run();
      const id = res.meta && res.meta.last_row_id;
      const c = { id, site: site.id, page, name, body, created };
      ctx.waitUntil(notify(env, u.hostname, c, why).catch(e => console.log('notify failed', String(e))));
      return why ? J({ ok: true, held: true }) : J({ ok: true, held: false, comment: { id, name, body, created } });
    }

    // Public: vote counts for one page, and this connection's own vote
    if (path === '/api/votes' && req.method === 'GET') {
      const page = u.searchParams.get('page') || '';
      if (!PAGE.test(page)) return J({ error: 'bad page' }, 400);
      await ensureVotes(env);
      const t = await tally(env, site.id, page);
      const h = (await sha('kc|' + (req.headers.get('cf-connecting-ip') || ''))).slice(0, 24);
      const mine = await env.DB.prepare('SELECT v FROM votes WHERE site = ? AND page = ? AND iphash = ?').bind(site.id, page, h).first();
      return J({ ...t, mine: mine ? mine.v : 0 });
    }

    // Public: vote up (1), down (-1) or take the vote back (0)
    if (path === '/api/votes' && req.method === 'POST') {
      const origin = req.headers.get('origin');
      if (origin && !ORIGINS.includes(origin) && origin !== env.DEV_ORIGIN) return J({ error: 'Not allowed.' }, 403);
      let d; try { d = await req.json(); } catch { return J({ error: 'Bad request.' }, 400); }
      const page = String(d.page || ''), v = Number(d.v);
      if (!PAGE.test(page) || ![1, -1, 0].includes(v)) return J({ error: 'Bad request.' }, 400);
      await ensureVotes(env);
      const h = (await sha('kc|' + (req.headers.get('cf-connecting-ip') || ''))).slice(0, 24);
      const r = await env.DB.prepare('SELECT COUNT(*) AS n FROM votes WHERE iphash = ? AND created > ?').bind(h, Date.now() - 3600000).first();
      if (r && r.n >= 60) return J({ error: 'Too many votes from this connection. Please try again later.' }, 429);
      if (v === 0) await env.DB.prepare('DELETE FROM votes WHERE site = ? AND page = ? AND iphash = ?').bind(site.id, page, h).run();
      else await env.DB.prepare('INSERT INTO votes (site, page, iphash, v, created) VALUES (?, ?, ?, ?, ?) ON CONFLICT (site, page, iphash) DO UPDATE SET v = excluded.v, created = excluded.created')
        .bind(site.id, page, h, v, Date.now()).run();
      return J({ ok: true, ...(await tally(env, site.id, page)), mine: v });
    }

    // Owner: review one comment from the email link (buttons POST back; nothing changes on GET)
    if (path === '/api/comments/review') {
      if (!env.ADMIN_KEY) return H('<p>Not configured.</p>', 500);
      let id, t, action = '';
      if (req.method === 'POST') {
        const f = await req.formData().catch(() => null);
        if (!f) return H('<p>Bad request.</p>', 400);
        id = parseInt(f.get('id'), 10); t = String(f.get('t') || ''); action = String(f.get('action') || '');
      } else { id = parseInt(u.searchParams.get('id'), 10); t = u.searchParams.get('t') || ''; }
      if (!id || !same(t, await token(env, id))) return H('<p>This link is not valid.</p>', 403);
      let done = '';
      if (action === 'approve') { await env.DB.prepare('UPDATE comments SET approved = 1 WHERE id = ?').bind(id).run(); done = 'Approved — it is now live.'; }
      else if (action === 'hide') { await env.DB.prepare('UPDATE comments SET approved = 0 WHERE id = ?').bind(id).run(); done = 'Hidden from the site.'; }
      else if (action === 'delete') { await env.DB.prepare('DELETE FROM comments WHERE id = ?').bind(id).run(); return H(page_('Deleted', '<p><b>Deleted.</b> The comment is gone.</p>')); }
      const c = await env.DB.prepare('SELECT id, site, page, name, body, created, approved FROM comments WHERE id = ?').bind(id).first();
      if (!c) return H(page_('Not found', '<p>This comment no longer exists.</p>'), 404);
      const s = SITE_BY_ID[c.site] || SITE_BY_ID.karsog;
      const btn = (a, label, cls) => `<form method="post"><input type="hidden" name="id" value="${c.id}"><input type="hidden" name="t" value="${esc(t)}"><input type="hidden" name="action" value="${a}"><button class="${cls || ''}"${a === 'delete' ? ' onclick="return confirm(\'Delete this comment for good?\')"' : ''}>${label}</button></form>`;
      return H(page_('Review comment', `${done ? `<p class="done">${esc(done)}</p>` : ''}
<p class="m">${esc(s.name)} · <a href="${esc(s.url(c.page))}" target="_blank" rel="noopener">${esc(c.page)}</a> · ${new Date(c.created).toISOString().slice(0, 16).replace('T', ' ')} UTC · <b>${c.approved ? 'Live' : 'Waiting for approval'}</b></p>
<div class="c"><b>${esc(c.name)}</b><div class="b">${esc(c.body)}</div></div>
<div class="row">${c.approved ? btn('hide', 'Hide') : btn('approve', 'Approve', 'ok')}${btn('delete', 'Delete')}</div>`));
    }

    // Owner: full admin page (both sites)
    if (path === '/api/comments/admin' && req.method === 'GET') return H(ADMIN);
    if (path === '/api/comments/admin' && req.method === 'POST') {
      let d; try { d = await req.json(); } catch { return J({ error: 'Bad request.' }, 400); }
      if (!env.ADMIN_KEY || !same(d.key, env.ADMIN_KEY)) return J({ error: 'Wrong key.' }, 403);
      const id = parseInt(d.id, 10);
      if (d.action === 'approve') await env.DB.prepare('UPDATE comments SET approved = 1 WHERE id = ?').bind(id).run();
      else if (d.action === 'hide') await env.DB.prepare('UPDATE comments SET approved = 0 WHERE id = ?').bind(id).run();
      else if (d.action === 'delete') await env.DB.prepare('DELETE FROM comments WHERE id = ?').bind(id).run();
      const q = 'SELECT id, site, page, name, body, created FROM comments WHERE approved = ? ORDER BY created DESC LIMIT ';
      const pending = (await env.DB.prepare(q + '200').bind(0).all()).results;
      const live = (await env.DB.prepare(q + '100').bind(1).all()).results;
      await ensureVotes(env);
      const votes = (await env.DB.prepare('SELECT site, page, SUM(v = 1) AS up, SUM(v = -1) AS down FROM votes GROUP BY site, page ORDER BY down DESC, up DESC LIMIT 200').all()).results;
      return J({ pending, live, votes });
    }

    return J({ error: 'Not found.' }, 404);
  }
};

function page_(title, inner) {
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>${esc(title)}</title>
<style>body{font:16px/1.5 system-ui,sans-serif;max-width:640px;margin:0 auto;padding:16px;background:#f6f5f1;color:#222}.c{background:#fff;border:1px solid #ddd;border-radius:8px;padding:12px;margin:10px 0}.b{white-space:pre-wrap;margin-top:6px}.m{color:#555;font-size:14px}
.row{display:flex;gap:8px}button{font:inherit;padding:8px 16px;border-radius:6px;border:1px solid #888;background:#fff;cursor:pointer}.ok{background:#1d6b3a;color:#fff;border-color:#1d6b3a}.done{background:#e6f4ea;border:1px solid #1d6b3a;padding:8px 12px;border-radius:6px}</style></head><body><h1 style="font-size:20px">${esc(title)}</h1>${inner}</body></html>`;
}

const ADMIN = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Comments admin</title>
<style>body{font:15px/1.5 system-ui,sans-serif;max-width:760px;margin:0 auto;padding:16px;background:#f6f5f1;color:#222}h1{font-size:20px}h2{font-size:17px;margin-top:28px}
.c{background:#fff;border:1px solid #ddd;border-radius:8px;padding:10px 12px;margin:8px 0}.m{color:#666;font-size:13px}.b{white-space:pre-wrap;margin:6px 0}
button{font:inherit;padding:6px 12px;margin-right:6px;border-radius:6px;border:1px solid #888;background:#fff;cursor:pointer}.ok{background:#1d6b3a;color:#fff;border-color:#1d6b3a}
input{font:inherit;padding:8px;width:100%;box-sizing:border-box;border:1px solid #aaa;border-radius:6px}#msg{color:#a00}</style></head><body>
<h1>Comments and votes — karsog.com, ToolNinja, Khelo aur Seekho</h1>
<div id="login"><p>Enter your admin key:</p><input id="k" type="password" autocomplete="current-password"><p><button class="ok" id="go">Open</button></p></div>
<p id="msg"></p><div id="app" hidden><h2>Waiting for approval (<span id="np">0</span>)</h2><div id="pending"></div><h2>Votes by page (most down-votes first)</h2><div id="votes"></div><h2>Live on the sites</h2><div id="live"></div></div>
<script>
let key='';try{key=localStorage.getItem('kck')||''}catch(e){}
const $=id=>document.getElementById(id);
const url=c=>c.site==='toolninja'?'https://toolninja.in/tools/'+c.page:c.site==='khelo'?'https://kheloaurseekho.in/'+(c.page==='home'?'':c.page+'/'):'https://karsog.com/'+c.page+'/';
const SN={toolninja:'ToolNinja ',khelo:'Khelo aur Seekho ',karsog:'karsog.com '};
function card(c,live){const d=document.createElement('div');d.className='c';
 const m=document.createElement('div');m.className='m';const a=document.createElement('a');a.href=url(c);a.textContent=(SN[c.site]||'')+c.page;a.target='_blank';
 m.append(new Date(c.created).toLocaleString('en-IN')+' · ',a);
 const n=document.createElement('b');n.textContent=c.name;const b=document.createElement('div');b.className='b';b.textContent=c.body;
 const btns=document.createElement('div');
 const mk=(t,act,cls)=>{const x=document.createElement('button');x.textContent=t;if(cls)x.className=cls;x.onclick=()=>{if(act==='delete'&&!confirm('Delete this comment for good?'))return;call(act,c.id)};btns.append(x)};
 if(live)mk('Hide','hide');else mk('Approve','approve','ok');mk('Delete','delete');
 d.append(m,n,b,btns);return d}
async function call(action,id){const r=await fetch(location.pathname,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({key,action,id})});const d=await r.json();
 if(!r.ok){$('msg').textContent=d.error||'Error';$('app').hidden=true;$('login').hidden=false;return}
 try{localStorage.setItem('kck',key)}catch(e){}
 $('msg').textContent='';$('login').hidden=true;$('app').hidden=false;$('np').textContent=d.pending.length;
 $('pending').replaceChildren(...(d.pending.length?d.pending.map(c=>card(c,false)):[Object.assign(document.createElement('p'),{textContent:'Nothing waiting.'})]));
 $('live').replaceChildren(...d.live.map(c=>card(c,true)));
 $('votes').replaceChildren(...((d.votes||[]).length?d.votes.map(x=>{const p=document.createElement('div');p.className='c';const a=document.createElement('a');a.href=url(x);a.target='_blank';a.textContent=(SN[x.site]||'')+x.page;p.append(a,' — up '+x.up+' · down '+x.down);return p}):[Object.assign(document.createElement('p'),{textContent:'No votes yet.'})]))}
$('go').onclick=()=>{key=$('k').value.trim();call('list')};
if(key)call('list');
</script></body></html>`;
