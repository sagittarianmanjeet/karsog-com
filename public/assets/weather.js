/* karsog.com weather page: live forecast, alerts, air quality, nearby places and the last 12 months.
   Data: Open-Meteo (free, no key). Every call runs in the visitor's browser, so there is nothing to update by hand. */
(function () {
  'use strict';
  var HI = document.documentElement.lang === 'hi';
  var L = function (en, hi) { return HI ? hi : en; };
  var $ = function (id) { return document.getElementById(id); };
  var LAT = 31.3825, LON = 77.2045, TZ = 'Asia%2FKolkata';
  var DAY = HI ? ['रवि', 'सोम', 'मंगल', 'बुध', 'गुरु', 'शुक्र', 'शनि'] : ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  var MON = HI ? ['जनवरी', 'फ़रवरी', 'मार्च', 'अप्रैल', 'मई', 'जून', 'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर']
               : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var WX = window.KWX || {};
  var r0 = function (x) { return Math.round(x); }, f1 = function (x) { return Math.round(x * 10) / 10; };
  var u0 = document.querySelector('svg use'), ICONS = u0 ? u0.getAttribute('href').split('#')[0] : '/assets/icons.svg';
  function ic(name, cls) { return '<svg class="' + (cls || 'ico') + '" aria-hidden="true"><use href="' + ICONS + '#i-' + name + '"/></svg>'; }
  function wx(code) { var w = WX[code] || ['Cloudy', 'बादल', 'cloud']; return { t: HI ? w[1] : w[0], i: w[2] }; }
  function hm(s) {                     // '2026-09-28T17:15' -> '5:15 PM' / 'शाम 5:15'
    var d = new Date(s), h = d.getHours(), m = ('0' + d.getMinutes()).slice(-2), h12 = h % 12 || 12;
    if (!HI) return h12 + ':' + m + (h < 12 ? ' AM' : ' PM');
    return (h >= 4 && h < 12 ? 'सुबह' : h < 16 && h >= 12 ? 'दोपहर' : h >= 16 && h < 19 ? 'शाम' : 'रात') + ' ' + h12 + ':' + m;
  }
  function hr(h) { var h12 = h % 12 || 12; return HI ? (h >= 4 && h < 12 ? 'सुबह ' : h >= 12 && h < 16 ? 'दोपहर ' : h >= 16 && h < 19 ? 'शाम ' : 'रात ') + h12 : h12 + (h < 12 ? ' AM' : ' PM'); }
  function fail(id, msg) { var e = $(id); if (e) e.innerHTML = '<p class="wx-load">' + msg + '</p>'; }

  fetch('https://api.open-meteo.com/v1/forecast?latitude=' + LAT + '&longitude=' + LON +
    '&current=temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m,precipitation' +
    '&hourly=temperature_2m,weather_code,precipitation_probability' +
    '&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,snowfall_sum,precipitation_probability_max,sunrise,sunset' +
    '&timezone=' + TZ + '&forecast_days=7')
    .then(function (r) { return r.json(); })
    .then(function (d) {
      var c = d.current, w = wx(c.weather_code), D = d.daily;
      $('wx-now').innerHTML = '<div class="wx-big">' + ic(w.i, 'ico wx-i') + '<b>' + r0(c.temperature_2m) + '°C</b></div>' +
        '<p class="wx-desc">' + w.t + '</p>' +
        '<dl class="wx-kv"><dt>' + L('Feels like', 'महसूस') + '</dt><dd>' + r0(c.apparent_temperature) + '°C</dd>' +
        '<dt>' + L('Humidity', 'नमी') + '</dt><dd>' + c.relative_humidity_2m + '%</dd>' +
        '<dt>' + L('Wind', 'हवा') + '</dt><dd>' + r0(c.wind_speed_10m) + ' ' + L('km/h', 'किमी/घंटा') + '</dd>' +
        '<dt>' + L('Today', 'आज') + '</dt><dd>' + r0(D.temperature_2m_max[0]) + '° / ' + r0(D.temperature_2m_min[0]) + '°</dd>' +
        '<dt>' + L('Sunrise', 'सूर्योदय') + '</dt><dd>' + hm(D.sunrise[0]) + '</dd>' +
        '<dt>' + L('Sunset', 'सूर्यास्त') + '</dt><dd>' + hm(D.sunset[0]) + '</dd></dl>';
      // road alert for today
      var code = D.weather_code[0], rain = D.precipitation_sum[0] || 0, snow = D.snowfall_sum[0] || 0, msg, kind = 'warn';
      var snowDays = D.snowfall_sum.map(function (s, i) { return s > 0 ? DAY[new Date(D.time[i]).getDay()] : null; }).filter(Boolean);
      if (snow > 0 || (code >= 71 && code <= 77) || code === 85 || code === 86)
        msg = L('<b>Snow forecast today.</b> The higher roads (Shikari Devi, Chindi, Janjehli) can close. Check before you travel.',
                '<b>आज बर्फ़ का पूर्वानुमान है।</b> ऊपर की सड़कें (शिकारी देवी, चिंडी, जंजैहली) बंद हो सकती हैं। निकलने से पहले पता कर लें।');
      else if (rain >= 20 || [65, 67, 82, 95, 96, 99].indexOf(code) >= 0)
        msg = L('<b>Heavy rain forecast today.</b> Landslides are common on these hill roads. Check before you travel.',
                '<b>आज तेज़ बारिश का पूर्वानुमान है।</b> इन पहाड़ी सड़कों पर भूस्खलन आम है। निकलने से पहले पता कर लें।');
      else if (rain >= 7 || [61, 63, 80, 81].indexOf(code) >= 0)
        msg = L('<b>Rain forecast today.</b> Expect slow, slippery stretches on the hill roads.', '<b>आज बारिश का पूर्वानुमान है।</b> पहाड़ी सड़कों पर फिसलन और धीमे रास्ते मिल सकते हैं।');
      else { msg = L('<b>No heavy rain or snow</b> forecast for Karsog today.', 'आज करसोग में <b>तेज़ बारिश या बर्फ़ का पूर्वानुमान नहीं</b> है।'); kind = 'ok'; }
      if (snowDays.length) msg += ' ' + L('Snow is forecast on: ', 'इन दिनों बर्फ़ का पूर्वानुमान है: ') + snowDays.join(', ') + '.';
      var a = $('wx-alert'); a.className = 'note ' + kind; a.innerHTML = '<p>' + msg + '</p>';
      // next 24 hours
      var now = new Date(c.time), H = d.hourly, out = [], n = 0;
      for (var i = 0; i < H.time.length && n < 24; i++) {
        var t = new Date(H.time[i]); if (t < now - 36e5) continue;
        var hw = wx(H.weather_code[i]);
        out.push('<div class="hour"><small>' + (n === 0 ? L('Now', 'अभी') : hr(t.getHours())) + '</small>' + ic(hw.i) + '<b>' + r0(H.temperature_2m[i]) + '°</b><small>' +
          ic('drop', 'ico drop') + (H.precipitation_probability[i] == null ? 0 : H.precipitation_probability[i]) + '%</small></div>');
        n++;
      }
      $('wx-hours').innerHTML = out.join('');
      // 7 days
      var rows = '';
      for (var k = 0; k < D.time.length; k++) {
        var dt = new Date(D.time[k]), dw = wx(D.weather_code[k]);
        rows += '<tr><td>' + (k === 0 ? L('Today', 'आज') : DAY[dt.getDay()] + ' ' + dt.getDate() + ' ' + MON[dt.getMonth()].slice(0, HI ? 10 : 3)) + '</td>' +
          '<td>' + ic(dw.i) + ' <span class="hide-s">' + dw.t + '</span></td><td class="t">' + r0(D.temperature_2m_max[k]) + '°</td><td>' + r0(D.temperature_2m_min[k]) + '°</td>' +
          '<td>' + (D.precipitation_probability_max[k] == null ? '–' : D.precipitation_probability_max[k]) + '% · ' + f1(D.precipitation_sum[k]) + ' ' + L('mm', 'मिमी') +
          (D.snowfall_sum[k] > 0 ? ' · ' + L('snow ', 'बर्फ़ ') + f1(D.snowfall_sum[k]) + ' ' + L('cm', 'सेमी') : '') + '</td></tr>';
      }
      $('wx-days').innerHTML = rows;
    })
    .catch(function () { fail('wx-now', L('Live weather could not load. Please refresh the page.', 'लाइव मौसम लोड नहीं हो पाया। कृपया पेज दोबारा खोलें।')); });

  // air quality
  fetch('https://air-quality-api.open-meteo.com/v1/air-quality?latitude=' + LAT + '&longitude=' + LON + '&current=us_aqi,pm2_5,pm10&timezone=' + TZ)
    .then(function (r) { return r.json(); })
    .then(function (a) {
      var v = a.current.us_aqi, lv = v <= 50 ? ['#2f7d3a', L('Good', 'अच्छी')] : v <= 100 ? ['#a4801f', L('Moderate', 'ठीक-ठाक')] :
        v <= 150 ? ['#c4631f', L('Unhealthy for sensitive groups', 'संवेदनशील लोगों के लिए हानिकारक')] : v <= 200 ? ['#b0372c', L('Unhealthy', 'हानिकारक')] : ['#6e3a8a', L('Very unhealthy', 'बहुत हानिकारक')];
      $('wx-aqi').innerHTML = '<p><span class="aqi" style="background:' + lv[0] + '">AQI ' + r0(v) + '</span> <b>' + lv[1] + '</b></p><p><small>PM2.5 ' + f1(a.current.pm2_5) +
        ' · PM10 ' + f1(a.current.pm10) + ' µg/m³ · ' + L('model estimate', 'मॉडल का अनुमान') + '</small></p>';
    }).catch(function () { fail('wx-aqi', L('Air quality could not load.', 'हवा की गुणवत्ता लोड नहीं हो पाई।')); });

  // nearby places
  var P = JSON.parse(($('j-near') || {}).textContent || '[]');
  if (P.length) fetch('https://api.open-meteo.com/v1/forecast?latitude=' + P.map(function (p) { return p[2]; }) + '&longitude=' + P.map(function (p) { return p[3]; }) +
    '&current=temperature_2m,weather_code&daily=temperature_2m_max,temperature_2m_min,snowfall_sum&timezone=' + TZ + '&forecast_days=1')
    .then(function (r) { return r.json(); })
    .then(function (Ls) {
      Ls = Array.isArray(Ls) ? Ls : [Ls];
      $('wx-near').innerHTML = Ls.map(function (x, i) {
        var w = wx(x.current.weather_code);
        return '<tr><td><a href="' + P[i][1] + '">' + P[i][0] + '</a><small>' + r0(x.elevation) + ' ' + L('m', 'मी') + '</small></td><td>' + ic(w.i) + ' <span class="hide-s">' + w.t + '</span></td>' +
          '<td class="t">' + r0(x.current.temperature_2m) + '°C</td><td>' + r0(x.daily.temperature_2m_max[0]) + '° / ' + r0(x.daily.temperature_2m_min[0]) + '°' +
          (x.daily.snowfall_sum[0] > 0 ? ' · ' + L('snow', 'बर्फ़') : '') + '</td></tr>';
      }).join('');
    }).catch(function () {});

  // the last 12 months
  var end = new Date(Date.now() - 8 * 864e5), start = new Date(end.getTime() - 364 * 864e5), iso = function (d) { return d.toISOString().slice(0, 10); };
  fetch('https://archive-api.open-meteo.com/v1/archive?latitude=' + LAT + '&longitude=' + LON + '&start_date=' + iso(start) + '&end_date=' + iso(end) +
    '&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,snowfall_sum&timezone=' + TZ)
    .then(function (r) { return r.json(); })
    .then(function (h) {
      var M = {};
      h.daily.time.forEach(function (t, i) {
        var k = t.slice(0, 7); M[k] = M[k] || { mx: [], mn: [], p: 0, s: 0, sd: 0 };
        if (h.daily.temperature_2m_max[i] == null) return;
        M[k].mx.push(h.daily.temperature_2m_max[i]); M[k].mn.push(h.daily.temperature_2m_min[i]); M[k].p += h.daily.precipitation_sum[i] || 0;
        var s = h.daily.snowfall_sum[i] || 0; M[k].s += s; if (s > 0.5) M[k].sd++;
      });
      var avg = function (a) { return a.reduce(function (x, y) { return x + y; }, 0) / a.length; };
      $('wx-year').innerHTML = Object.keys(M).sort().filter(function (k) { return M[k].mx.length >= 25; }).map(function (k) {
        var m = M[k], p = k.split('-');
        return '<tr><td>' + MON[+p[1] - 1] + ' ' + p[0] + '</td><td class="t">' + r0(avg(m.mx)) + '°</td><td>' + r0(avg(m.mn)) + '°</td><td>' + r0(m.p) + ' ' + L('mm', 'मिमी') + '</td><td>' +
          (m.s > 0.5 ? r0(m.s) + ' ' + L('cm', 'सेमी') + ' (' + m.sd + ' ' + L(m.sd === 1 ? 'day' : 'days', 'दिन') + ')' : '—') + '</td></tr>';
      }).join('');
    }).catch(function () { $('wx-year').innerHTML = '<tr><td colspan="5">' + L('Could not load past weather.', 'पिछला मौसम लोड नहीं हो पाया।') + '</td></tr>'; });
})();
