/* Comments widget for karsog.com and toolninja.in — talks to /api/comments (Cloudflare Worker + D1).
   <div id="kc" data-page="…" data-sitekey="…" [data-placeholder="…"] [data-style="1"]></div>
   Clean comments go live at once; ones with numbers, links or emails wait for the owner. */
(function () {
  var el = document.getElementById('kc');
  if (!el) return;
  var page = el.getAttribute('data-page');
  var sitekey = el.getAttribute('data-sitekey');
  var ph = el.getAttribute('data-placeholder') || 'Your comment, question or correction.';
  var wid = null, tsLoaded = false;

  if (el.getAttribute('data-style') === '1' && !document.getElementById('kc-css')) {
    var st = document.createElement('style'); st.id = 'kc-css';
    st.textContent =
      '#kc .kc-list:empty{display:none}#kc .kc-list{margin:0 0 16px}' +
      '#kc .kc-c{border:1px solid var(--border,#2a2d3e);border-radius:10px;padding:10px 12px;margin:0 0 8px;background:var(--bg-card,transparent)}' +
      '#kc .kc-h{font-size:.8rem;color:var(--fg-muted,#8b8fa8)}#kc .kc-h b{color:var(--fg,inherit)}#kc .kc-c p{margin:4px 0 0;white-space:pre-wrap;word-break:break-word}' +
      '#kc form{display:grid;gap:10px}#kc label{display:grid;gap:4px;font-size:.8rem;font-weight:600;color:var(--fg-muted,#8b8fa8)}' +
      '#kc input,#kc textarea{font:inherit;font-size:.95rem;padding:10px 12px;border:1px solid var(--border,#2a2d3e);border-radius:8px;background:var(--bg,#fff);color:var(--fg,#111);width:100%;box-sizing:border-box}' +
      '#kc input:focus,#kc textarea:focus{outline:none;border-color:var(--primary,#f07525)}' +
      '#kc button{justify-self:start;font:inherit;font-weight:600;padding:10px 18px;border:0;border-radius:8px;background:var(--primary,#f07525);color:#fff;cursor:pointer}' +
      '#kc button:disabled{opacity:.6;cursor:default}#kc .kc-msg{margin:0;font-size:.85rem;min-height:1.2em}';
    document.head.appendChild(st);
  }

  el.innerHTML =
    '<div class="kc-list" aria-live="polite"></div>' +
    '<form class="kc-form" novalidate>' +
    '<label>Your name<input name="name" maxlength="60" autocomplete="name" required></label>' +
    '<label>Comment<textarea name="body" maxlength="2000" rows="4" required></textarea></label>' +
    '<div class="kc-ts"></div>' +
    '<button type="submit">Post comment</button>' +
    '<p class="kc-msg" role="status"></p>' +
    '</form>';

  var list = el.querySelector('.kc-list'), form = el.querySelector('form'),
      msg = el.querySelector('.kc-msg'), btn = form.querySelector('button');
  form.elements['body'].placeholder = ph;

  function fmt(t) {
    try { return new Date(t).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }); }
    catch (e) { return ''; }
  }
  function add(c) {
    var d = document.createElement('div'); d.className = 'kc-c';
    var h = document.createElement('div'); h.className = 'kc-h';
    var n = document.createElement('b'); n.textContent = c.name;
    var t = document.createElement('span'); t.textContent = ' · ' + fmt(c.created);
    h.appendChild(n); h.appendChild(t);
    var p = document.createElement('p'); p.textContent = c.body;
    d.appendChild(h); d.appendChild(p); list.appendChild(d);
  }
  fetch('/api/comments?page=' + encodeURIComponent(page), { cache: 'no-store' })
    .then(function (r) { if (!r.ok) throw 0; return r.json(); })
    .then(function (d) { (d.comments || []).forEach(add); })
    .catch(function () {});

  function loadTs() {
    if (tsLoaded) return; tsLoaded = true;
    window.kcTsReady = function () {
      wid = window.turnstile.render(el.querySelector('.kc-ts'), { sitekey: sitekey, size: 'flexible' });
    };
    var s = document.createElement('script');
    s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit&onload=kcTsReady';
    s.async = true; document.head.appendChild(s);
  }
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (e) { if (e[0].isIntersecting) { io.disconnect(); loadTs(); } }, { rootMargin: '400px' });
    io.observe(el);
  } else loadTs();
  form.addEventListener('focusin', loadTs);

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var name = form.elements['name'].value.trim(), body = form.elements['body'].value.trim();
    if (!name || body.length < 2) { msg.textContent = 'Please enter your name and a comment.'; return; }
    var token = wid !== null && window.turnstile ? window.turnstile.getResponse(wid) : '';
    if (!token) { msg.textContent = 'Please wait a moment for the security check, then try again.'; loadTs(); return; }
    btn.disabled = true; msg.textContent = 'Posting…';
    fetch('/api/comments', {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ page: page, name: name, body: body, token: token })
    })
      .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
      .then(function (x) {
        if (!x.ok) { msg.textContent = x.d.error || 'Something went wrong. Please try again.'; return; }
        form.reset();
        if (x.d.held) msg.textContent = 'Thank you! Your comment has a number, link or email in it, so it will appear after a quick check.';
        else { if (x.d.comment) add(x.d.comment); msg.textContent = 'Thank you! Your comment is live.'; }
      })
      .catch(function () { msg.textContent = 'Could not post. Please check your connection and try again.'; })
      .then(function () { btn.disabled = false; try { window.turnstile.reset(wid); } catch (e) {} });
  });
})();
