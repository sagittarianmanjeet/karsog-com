/* karsog.com mandi rates: today's APMC prices from Agmarknet (via /api/mandi, stored daily by the site's Worker). */
(function () {
  'use strict';
  var HI = document.documentElement.lang === 'hi';
  var L = function (en, hi) { return HI ? hi : en; };
  var $ = function (id) { return document.getElementById(id); };
  var DIST_ORDER = ['Mandi', 'Shimla', 'Solan', 'Kullu'];
  var TOP = ['Apple', 'Tomato', 'Potato', 'Peas Wet', 'Cauliflower', 'Cabbage', 'Capsicum', 'Ginger(Green)', 'Pear(Marasebu)', 'Garlic', 'Onion'];
  var NAME_HI = { 'Apple': 'सेब', 'Tomato': 'टमाटर', 'Potato': 'आलू', 'Peas Wet': 'हरा मटर', 'Cauliflower': 'फूलगोभी', 'Cabbage': 'बंदगोभी',
    'Capsicum': 'शिमला मिर्च', 'Ginger(Green)': 'अदरक', 'Pear(Marasebu)': 'नाशपाती', 'Garlic': 'लहसुन', 'Onion': 'प्याज़', 'Plum': 'प्लम',
    'Peach': 'आड़ू', 'Apricot(Jardalu/Khumani)': 'खुमानी', 'Cucumbar(Kheera)': 'खीरा', 'Beans': 'बीन्स', 'Brinjal': 'बैंगन', 'Lemon': 'नींबू',
    'Green Chilli': 'हरी मिर्च', 'Bhindi(Ladies Finger)': 'भिंडी', 'Pumpkin': 'कद्दू', 'Radish': 'मूली', 'Carrot': 'गाजर', 'Spinach': 'पालक',
    'Coriander(Leaves)': 'हरा धनिया', 'Banana': 'केला', 'Mango': 'आम', 'Orange': 'संतरा', 'Kinnow': 'किन्नू', 'Pomegranate': 'अनार', 'Grapes': 'अंगूर' };
  var MON = HI ? ['जन', 'फ़र', 'मार्च', 'अप्रै', 'मई', 'जून', 'जुला', 'अग', 'सित', 'अक्टू', 'नव', 'दिस'] : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var data = [], cur = 'Apple', today = new Date(Date.now() + 5.5 * 3600e3).toISOString().slice(0, 10);

  function nm(c) { return HI && NAME_HI[c] ? NAME_HI[c] : c; }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function inr(n) { return n == null ? '—' : '₹' + Number(n).toLocaleString('en-IN'); }
  function fmtDate(d) { if (!d) return '—'; var p = d.split('-'); return (+p[2]) + ' ' + MON[+p[1] - 1]; }
  function ageDays(d) { return Math.round((Date.parse(today) - Date.parse(d)) / 864e5); }
  function cleanMarket(m) { var t = /^(PMY|SMY|TSMY)\s+/i.exec(m); return { name: t ? m.slice(t[0].length) : m, yard: t ? t[1].toUpperCase() : '' }; }
  function distRank(d) { var i = DIST_ORDER.indexOf(d); return i < 0 ? 99 : i; }

  function load() {
    fetch('/api/mandi/latest').then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (j) {
      var c = j.cols || [];
      data = (j.rows || []).map(function (r) { var o = {}; c.forEach(function (k, i) { o[k] = r[i]; }); return o; });
      if (!data.length) { $('mr-list').innerHTML = ''; $('mr-err').textContent = L('Prices will appear here after the first daily update.', 'पहले दैनिक अपडेट के बाद यहाँ भाव दिखेंगे।'); $('mr-err').hidden = false; return; }
      var dates = data.map(function (r) { return r.d; }).sort();
      $('mr-date').textContent = fmtDate(dates[dates.length - 1]);
      $('mr-mkts').textContent = new Set(data.map(function (r) { return r.market; })).size;
      $('mr-items').textContent = data.length;
      if (j.built) $('mr-built').textContent = L('Last updated ', 'आख़िरी अपडेट ') + new Date(j.built).toLocaleString(HI ? 'hi-IN' : 'en-IN', { dateStyle: 'medium', timeStyle: 'short' }) + '.';
      chips(); districts(); render();
    }).catch(function () { $('mr-list').innerHTML = ''; $('mr-err').hidden = false; });
  }

  function chips() {
    var counts = {}; data.forEach(function (r) { counts[r.commodity] = (counts[r.commodity] || 0) + 1; });
    var list = TOP.filter(function (c) { return counts[c]; });
    Object.keys(counts).sort(function (a, b) { return counts[b] - counts[a]; }).forEach(function (c) { if (list.length < 10 && list.indexOf(c) < 0) list.push(c); });
    if (!counts[cur]) cur = '';
    var box = $('mr-chips'); box.innerHTML = '';
    [''].concat(list).forEach(function (c) {
      var b = el('button', 'fchip', c ? nm(c) : L('All', 'सभी')); b.type = 'button';
      b.setAttribute('aria-pressed', String(c === cur));
      b.onclick = function () { cur = c; [].forEach.call(box.children, function (x) { x.setAttribute('aria-pressed', String(x === b)); }); render(); };
      box.appendChild(b);
    });
  }

  function districts() {
    var ds = Array.from(new Set(data.map(function (r) { return r.district; }))).sort(function (a, b) { return distRank(a) - distRank(b) || a.localeCompare(b); });
    ds.forEach(function (d) { var o = el('option', null, d); o.value = d; $('mr-dist').appendChild(o); });
  }

  function render() {
    var q = $('mr-q').value.trim().toLowerCase(), dist = $('mr-dist').value;
    var rows = data.filter(function (r) {
      if (cur && r.commodity !== cur) return false;
      if (dist && r.district !== dist) return false;
      if (q && (r.market + ' ' + r.commodity + ' ' + nm(r.commodity) + ' ' + r.variety + ' ' + r.district).toLowerCase().indexOf(q) < 0) return false;
      return true;
    });
    var groups = {};
    rows.forEach(function (r) { (groups[r.market] = groups[r.market] || []).push(r); });
    var keys = Object.keys(groups).sort(function (a, b) {
      var ra = groups[a][0], rb = groups[b][0];
      return distRank(ra.district) - distRank(rb.district) || ra.district.localeCompare(rb.district) || cleanMarket(a).name.localeCompare(cleanMarket(b).name);
    });
    var list = $('mr-list'); list.innerHTML = '';
    $('mr-none').hidden = keys.length > 0;
    keys.forEach(function (m) {
      var items = groups[m].sort(function (a, b) { return a.commodity.localeCompare(b.commodity) || b.modal - a.modal; });
      var last = items.map(function (r) { return r.d; }).sort().pop(), cm = cleanMarket(m);
      var card = el('section', 'mkt'), h = el('div', 'mkt-h'), left = el('div');
      left.appendChild(el('h3', null, cm.name));
      left.appendChild(el('div', 'sub', items[0].district + L(' district', ' ज़िला') + (cm.yard ? ' · ' + cm.yard : '')));
      var age = ageDays(last);
      var tag = el('span', 'mtag' + (age > 2 ? ' old' : ''), age <= 0 ? L('Today', 'आज') : age === 1 ? L('Yesterday', 'कल') : fmtDate(last));
      h.appendChild(left); h.appendChild(tag); card.appendChild(h);
      items.forEach(function (r) { card.appendChild(row(r)); });
      list.appendChild(card);
    });
  }

  function row(r) {
    var b = el('button', 'mrow'); b.type = 'button'; b.setAttribute('aria-expanded', 'false');
    var l = el('div');
    l.appendChild(el('div', 'c-name', nm(r.commodity)));
    var v = [r.variety, r.grade].filter(function (x) { return x && x !== r.commodity && x !== 'Other' && x !== 'FAQ'; }).join(' · ');
    l.appendChild(el('div', 'c-var', (v ? v + ' · ' : '') + L('range ', 'दायरा ') + inr(r.min) + '–' + inr(r.max)));
    var rt = el('div');
    rt.appendChild(el('div', 'c-price', inr(r.modal) + L('/qtl', '/क्विंटल')));
    var meta = el('div', 'c-meta', '≈ ₹' + (r.modal / 100).toLocaleString('en-IN', { maximumFractionDigits: 1 }) + L('/kg ', '/किलो '));
    if (r.prev) {
      var diff = r.modal - r.prev, pct = Math.round(diff / r.prev * 100);
      var s = el('span', 'chg ' + (diff > 0 ? 'up' : diff < 0 ? 'down' : 'flat'), (diff > 0 ? '▲ ' : diff < 0 ? '▼ ' : '• ') + (diff === 0 ? L('no change', 'कोई बदलाव नहीं') : Math.abs(pct) + '%'));
      s.title = L('vs ', 'पिछला: ') + inr(r.prev) + ' · ' + fmtDate(r.prevD);
      meta.appendChild(s);
    }
    rt.appendChild(meta); b.appendChild(l); b.appendChild(rt);
    var open = null;
    b.onclick = function () {
      if (open) { open.remove(); open = null; b.setAttribute('aria-expanded', 'false'); return; }
      open = el('div', 'hist'); open.appendChild(el('p', null, L('Loading price history…', 'भाव का इतिहास लोड हो रहा है…')));
      b.appendChild(open); b.setAttribute('aria-expanded', 'true');
      var target = open, qs = new URLSearchParams({ market: r.market, commodity: r.commodity, variety: r.variety || '', grade: r.grade || '' });
      fetch('/api/mandi/history?' + qs).then(function (x) { return x.json(); }).then(function (j) { hist(target, j.points || []); })
        .catch(function () { target.firstChild.textContent = L('History unavailable right now.', 'इतिहास अभी उपलब्ध नहीं है।'); });
    };
    return b;
  }

  function hist(box, pts) {
    box.innerHTML = '';
    if (pts.length < 2) { box.appendChild(el('p', null, L('The trend appears once this market has reported on at least two days.', 'इस मंडी के कम से कम दो दिन के भाव आने पर रुझान दिखेगा।'))); return; }
    var W = 600, H = 90, P = 6, vals = pts.map(function (p) { return p[3]; });
    var lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals); if (hi === lo) { hi += 1; lo -= 1; }
    var x = function (i) { return P + i * (W - 2 * P) / (pts.length - 1); }, y = function (v) { return H - P - (v - lo) * (H - 2 * P) / (hi - lo); };
    var d = vals.map(function (v, i) { return (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(v).toFixed(1); }).join(' ');
    var ns = 'http://www.w3.org/2000/svg', svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H); svg.setAttribute('preserveAspectRatio', 'none'); svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', L('Price trend from ', 'भाव का रुझान ') + fmtDate(pts[0][0]) + ' – ' + fmtDate(pts[pts.length - 1][0]));
    var path = document.createElementNS(ns, 'path'); path.setAttribute('d', d); path.setAttribute('fill', 'none');
    path.setAttribute('stroke', '#1f4e39'); path.setAttribute('stroke-width', '2'); path.setAttribute('vector-effect', 'non-scaling-stroke');
    svg.appendChild(path); box.appendChild(svg);
    box.appendChild(el('p', null, fmtDate(pts[0][0]) + ' → ' + fmtDate(pts[pts.length - 1][0]) + ' · ' + L('low ', 'न्यूनतम ') + inr(Math.min.apply(null, vals)) + ' · ' +
      L('high ', 'अधिकतम ') + inr(Math.max.apply(null, vals)) + ' (' + L('modal, ₹/quintal, ', 'मॉडल, ₹/क्विंटल, ') + pts.length + L(' reports)', ' रिपोर्ट)')));
  }

  $('mr-q').addEventListener('input', render);
  $('mr-dist').addEventListener('change', render);
  load();
})();
