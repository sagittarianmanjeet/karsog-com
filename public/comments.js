/* karsog.com comments widget — talks to /api/comments (Cloudflare Worker + D1) */
(function () {
  var el = document.getElementById('kc');
  if (!el) return;
  var page = el.getAttribute('data-page');
  var sitekey = el.getAttribute('data-sitekey');
  var wid = null, tsLoaded = false;

  el.innerHTML =
    '<div class="kc-list" aria-live="polite">Loading comments…</div>' +
    '<form class="kc-form" novalidate>' +
    '<label>Your name<input name="name" maxlength="60" autocomplete="name" required></label>' +
    '<label>Comment<textarea name="body" maxlength="2000" rows="4" required placeholder="Know this place? Share its name, a story or a correction."></textarea></label>' +
    '<div class="kc-ts"></div>' +
    '<button type="submit">Post comment</button>' +
    '<p class="kc-msg" role="status"></p>' +
    '</form>';

  var list = el.querySelector('.kc-list'), form = el.querySelector('form'),
      msg = el.querySelector('.kc-msg'), btn = form.querySelector('button');

  function fmt(t) {
    try { return new Date(t).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }); }
    catch (e) { return ''; }
  }
  function render(cs) {
    list.innerHTML = '';
    if (!cs.length) { list.textContent = 'No comments yet — be the first.'; return; }
    cs.forEach(function (c) {
      var d = document.createElement('div'); d.className = 'kc-c';
      var h = document.createElement('div'); h.className = 'kc-h';
      var n = document.createElement('b'); n.textContent = c.name;
      var t = document.createElement('span'); t.textContent = ' · ' + fmt(c.created);
      h.appendChild(n); h.appendChild(t);
      var p = document.createElement('p'); p.textContent = c.body;
      d.appendChild(h); d.appendChild(p); list.appendChild(d);
    });
  }
  fetch('/api/comments?page=' + encodeURIComponent(page), { cache: 'no-store' })
    .then(function (r) { if (!r.ok) throw 0; return r.json(); })
    .then(function (d) { render(d.comments || []); })
    .catch(function () { list.textContent = 'Comments could not be loaded right now.'; });

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
        if (x.ok) { form.reset(); msg.textContent = 'Thank you! Your comment will appear after it is approved.'; }
        else msg.textContent = x.d.error || 'Something went wrong. Please try again.';
      })
      .catch(function () { msg.textContent = 'Could not post. Please check your connection and try again.'; })
      .then(function () { btn.disabled = false; try { window.turnstile.reset(wid); } catch (e) {} });
  });
})();
