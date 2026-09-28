/* karsog.com — behaviour shared by every page: menus, the live "right now" strip, next-bus boards,
   photo lightbox and the WhatsApp update form. Plain JavaScript, no libraries. */
(function () {
  'use strict';
  var d = document, root = d.documentElement, HI = root.lang === 'hi';
  var $ = function (s, c) { return (c || d).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); };
  var L = function (en, hi) { return HI ? hi : en; };

  /* ---------- time in India (IST), whatever the visitor's phone is set to ---------- */
  function ist() { var n = new Date(); return new Date(n.getTime() + (n.getTimezoneOffset() + 330) * 60000); }
  function mins(t) { var p = t.split(':'); return +p[0] * 60 + +p[1]; }
  function clock(t) {           // '17:15' -> '5:15 PM' or 'शाम 5:15'
    var p = t.split(':'), h = +p[0], m = p[1], h12 = h % 12 || 12;
    if (!HI) return h12 + ':' + m + ' ' + (h < 12 ? 'AM' : 'PM');
    var part = h >= 4 && h < 12 ? 'सुबह' : h >= 12 && h < 16 ? 'दोपहर' : h >= 16 && h < 19 ? 'शाम' : 'रात';
    return part + ' ' + h12 + ':' + m;
  }
  function wait(n) {            // minutes -> 'in 1 h 5 min' / '1 घंटा 5 मिनट में'
    var h = Math.floor(n / 60), m = n % 60;
    if (HI) return (h ? h + ' घंटे ' : '') + (m || !h ? m + ' मिनट' : '') + ' में';
    return 'in ' + (h ? h + ' h ' : '') + (m || !h ? m + ' min' : '');
  }
  function json(id) { var el = d.getElementById(id); try { return el ? JSON.parse(el.textContent) : null; } catch (e) { return null; } }

  /* ---------- dialogs: menu sheet and update form ---------- */
  var last = null;
  function openDlg(id) {
    var el = d.getElementById(id); if (!el) return;
    closeAll(); last = d.activeElement;
    el.hidden = false; el.classList.add('open'); d.body.style.overflow = 'hidden';
    $$('[data-open="' + id + '"]').forEach(function (b) { b.setAttribute('aria-expanded', 'true'); });
    var f = el.querySelector('textarea, .sheet-grid a, button'); if (f) try { f.focus({ preventScroll: true }); } catch (e) {}
  }
  function closeDlg(el) {
    if (!el.classList.contains('open')) return;
    el.classList.remove('open'); el.hidden = true; d.body.style.overflow = '';
    $$('[data-open="' + el.id + '"]').forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
    if (last && last.focus) try { last.focus({ preventScroll: true }); } catch (e) {}
  }
  function closeAll() { $$('.sheet.open, .modal.open').forEach(closeDlg); }
  function closeMore(except) {
    $$('.more.open').forEach(function (m) { if (m !== except) { m.classList.remove('open'); m.firstElementChild.setAttribute('aria-expanded', 'false'); } });
  }
  d.addEventListener('click', function (e) {
    var t = e.target;
    var o = t.closest('[data-open]');
    if (o) { e.preventDefault(); openDlg(o.getAttribute('data-open')); return; }
    var c = t.closest('[data-close]');
    if (c) { var box = c.closest('.sheet, .modal'); if (box) closeDlg(box); return; }
    if (t.classList && t.classList.contains('modal')) { closeDlg(t); return; }
    var mb = t.closest('.more > button');
    if (mb) { var m = mb.parentNode, on = !m.classList.contains('open'); closeMore(m); m.classList.toggle('open', on); mb.setAttribute('aria-expanded', on); return; }
    if (!t.closest('.more')) closeMore();
  });
  d.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeAll(); closeMore(); } });

  /* ---------- header over the home photo turns solid on scroll ---------- */
  var hdr = $('.site-h.over');
  if (hdr) {
    var tick = false, set = function () { hdr.classList.toggle('solid', window.scrollY > 40); tick = false; };
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(set); } }, { passive: true });
    set();
  }

  /* ---------- gentle reveal of cards as they scroll into view ---------- */
  var rv = $$('.rv');
  if (rv.length) {
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } });
      }, { rootMargin: '0px 0px -8% 0px' });
      rv.forEach(function (el) { io.observe(el); });
    } else rv.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- next-bus boards: <div class="nextbus" data-src="bd" data-n="5"> + JSON [{t,to,hi,u}] ---------- */
  function upcoming(list, n) {
    var now = ist(), m = now.getHours() * 60 + now.getMinutes();
    var today = list.filter(function (b) { return mins(b.t) >= m; }).map(function (b) { return { b: b, w: mins(b.t) - m }; });
    var tmr = list.map(function (b) { return { b: b, w: mins(b.t) + 1440 - m, tmr: 1 }; });
    return today.concat(tmr).slice(0, n);
  }
  $$('.nextbus[data-src]').forEach(function (box) {
    var list = json(box.getAttribute('data-src')); if (!list || !list.length) return;
    var n = +box.getAttribute('data-n') || 5, ol = $('ol', box), when = $('.when', box);
    function draw() {
      var up = upcoming(list, n), now = ist();
      if (when) when.textContent = L('now ', 'अभी ') + clock(('0' + now.getHours()).slice(-2) + ':' + ('0' + now.getMinutes()).slice(-2));
      ol.innerHTML = up.map(function (x) {
        var to = HI && x.b.hi ? x.b.hi : x.b.to, dest = x.b.u ? '<a href="' + x.b.u + '">' + to + '</a>' : to;
        var tag = x.b.p ? ' <span class="pv">' + L('private', 'प्राइवेट') + '</span>' : '';
        return '<li><span class="tm">' + clock(x.b.t) + '</span><span class="to">' + dest + tag + '</span><span class="in">' +
          (x.tmr ? L('tomorrow', 'कल') : wait(x.w)) + '</span></li>';
      }).join('');
    }
    draw(); setInterval(draw, 30000);
  });

  /* ---------- home: live "right now" strip ---------- */
  var WX = { 0: ['Clear sky', 'साफ़ आसमान', 'sun'], 1: ['Mostly clear', 'ज़्यादातर साफ़', 'sun'], 2: ['Partly cloudy', 'हल्के बादल', 'cloud'],
    3: ['Cloudy', 'बादल', 'cloud'], 45: ['Fog', 'कोहरा', 'cloud'], 48: ['Fog', 'कोहरा', 'cloud'], 51: ['Light drizzle', 'हल्की बूँदाबाँदी', 'rain'],
    53: ['Drizzle', 'बूँदाबाँदी', 'rain'], 55: ['Heavy drizzle', 'तेज़ बूँदाबाँदी', 'rain'], 61: ['Light rain', 'हल्की बारिश', 'rain'],
    63: ['Rain', 'बारिश', 'rain'], 65: ['Heavy rain', 'तेज़ बारिश', 'rain'], 66: ['Freezing rain', 'जमने वाली बारिश', 'rain'],
    67: ['Freezing rain', 'जमने वाली बारिश', 'rain'], 71: ['Light snow', 'हल्की बर्फ़', 'snow'], 73: ['Snow', 'बर्फ़बारी', 'snow'],
    75: ['Heavy snow', 'भारी बर्फ़बारी', 'snow'], 77: ['Snow grains', 'बर्फ़ के कण', 'snow'], 80: ['Showers', 'बौछारें', 'rain'],
    81: ['Showers', 'बौछारें', 'rain'], 82: ['Heavy showers', 'तेज़ बौछारें', 'rain'], 85: ['Snow showers', 'बर्फ़ की बौछारें', 'snow'],
    86: ['Snow showers', 'बर्फ़ की बौछारें', 'snow'], 95: ['Thunderstorm', 'आँधी-तूफ़ान', 'rain'], 96: ['Thunderstorm, hail', 'तूफ़ान, ओले', 'rain'],
    99: ['Thunderstorm, hail', 'तूफ़ान, ओले', 'rain'] };
  window.KWX = WX;
  var nw = $('#now-w');
  if (nw) {
    fetch('https://api.open-meteo.com/v1/forecast?latitude=31.383&longitude=77.2&current=temperature_2m,weather_code&timezone=Asia%2FKolkata')
      .then(function (r) { return r.json(); })
      .then(function (j) {
        var c = j.current, w = WX[c.weather_code] || ['', '', 'cloud'];
        $('b', nw).textContent = Math.round(c.temperature_2m) + '°C · ' + (HI ? w[1] : w[0]);
        var u = $('use', nw); if (u) u.setAttribute('href', u.getAttribute('href').replace(/#i-[\w-]+/, '#i-' + w[2]));
      }).catch(function () {});
  }
  var nb = $('#now-b'), bl = json('j-bd');
  if (nb && bl && bl.length) {
    var draw1 = function () {
      var x = upcoming(bl, 1)[0]; if (!x) return;
      $('b', nb).textContent = clock(x.b.t) + ' → ' + (HI && x.b.hi ? x.b.hi : x.b.to) + (x.tmr ? L(' (tomorrow)', ' (कल)') : '');
    };
    draw1(); setInterval(draw1, 30000);
  }
  var nm = $('#now-m'), ml = json('j-melas');
  if (nm && ml && ml.length) {
    var mo = ist().getMonth() + 1, pick = null;
    for (var i = 0; i < 12 && !pick; i++) {
      var mm = (mo - 1 + i) % 12 + 1;
      ml.forEach(function (f) { if (!pick && f.m === mm) pick = f; });
    }
    if (pick) {
      $('b', nm).textContent = (HI ? pick.hi : pick.en) + ' · ' + (HI ? pick.wh : pick.we);
      if (pick.m !== mo) $('small', nm).textContent = L('Next fair', 'अगला मेला');
      if (pick.u) nm.setAttribute('href', pick.u);
    }
  }

  /* ---------- fair calendar: mark this month ---------- */
  var cm = ist().getMonth() + 1;
  $$('[data-m]').forEach(function (el) {
    if (+el.getAttribute('data-m') !== cm) return;
    el.classList.add('cur');
    var sc = el.parentNode;                       // on phones the calendar scrolls sideways: start at this month
    if (sc && sc.scrollWidth > sc.clientWidth + 4) sc.scrollLeft = el.offsetLeft - sc.firstElementChild.offsetLeft;
  });

  /* ---------- photo lightbox for .gallery ---------- */
  var gl = $$('.gallery a');
  if (gl.length) {
    var lb = d.createElement('div');
    lb.className = 'lb'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.hidden = true;
    lb.innerHTML = '<figure><img alt=""><figcaption></figcaption></figure>' +
      '<button type="button" class="x" aria-label="' + L('Close', 'बंद करें') + '">✕</button>' +
      '<button type="button" class="p" aria-label="' + L('Previous photo', 'पिछली फ़ोटो') + '">‹</button>' +
      '<button type="button" class="n" aria-label="' + L('Next photo', 'अगली फ़ोटो') + '">›</button>';
    d.body.appendChild(lb);
    var im = $('img', lb), fc = $('figcaption', lb), k = 0, x0 = null;
    var show = function (i) {
      k = (i + gl.length) % gl.length; var a = gl[k], th = $('img', a);
      im.src = a.href; im.alt = th ? th.alt : ''; fc.textContent = a.getAttribute('data-cap') + '  ·  ' + (k + 1) + ' / ' + gl.length;
      lb.hidden = false; lb.classList.add('open'); d.body.style.overflow = 'hidden';
    };
    var hide = function () { lb.classList.remove('open'); lb.hidden = true; d.body.style.overflow = ''; gl[k].focus(); };
    gl.forEach(function (a, i) { a.addEventListener('click', function (e) { e.preventDefault(); show(i); }); });
    $('.x', lb).onclick = hide; $('.p', lb).onclick = function () { show(k - 1); }; $('.n', lb).onclick = function () { show(k + 1); };
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.tagName === 'FIGURE') hide(); });
    d.addEventListener('keydown', function (e) {
      if (lb.hidden) return;
      if (e.key === 'Escape') hide(); else if (e.key === 'ArrowLeft') show(k - 1); else if (e.key === 'ArrowRight') show(k + 1);
    });
    lb.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) {
      if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 40) show(k + (dx < 0 ? 1 : -1)); x0 = null;
    });
  }

  /* ---------- "send an update" form -> WhatsApp ---------- */
  var fm = $('#upd form');
  if (fm) fm.addEventListener('submit', function (e) {
    e.preventDefault();
    var text = fm.elements.text.value.trim(), msg = $('.kc-msg', fm);
    if (!text) { msg.textContent = msg.getAttribute('data-empty'); fm.elements.text.focus(); return; }
    var name = fm.elements.name.value.trim();
    var body = '*karsog.com — ' + fm.elements.type.value + '*\n' + text + '\n\n' + L('Page: ', 'पेज: ') + location.href.split('#')[0] +
      (name ? '\n— ' + name : '');
    window.open('https://wa.me/' + fm.getAttribute('data-wa') + '?text=' + encodeURIComponent(body), '_blank', 'noopener');
    fm.reset(); msg.textContent = '';
    closeDlg($('#upd'));
  });

  /* ---------- works offline: cache pages already visited ---------- */
  if ('serviceWorker' in navigator) window.addEventListener('load', function () { navigator.serviceWorker.register('/sw.js').catch(function () {}); });
})();
