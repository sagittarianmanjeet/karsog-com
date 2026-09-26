// Year

document.getElementById('y').textContent = new Date().getFullYear();

// Mobile menu
const burger = document.getElementById('burger');
const menu = document.getElementById('mobile-menu');
const closeMenu = document.getElementById('close-menu');
function toggleMenu(open){
  menu.classList.toggle('open', open);
  burger.classList.toggle('open', open);
  burger.setAttribute('aria-expanded', open);
  document.body.style.overflow = open ? 'hidden' : '';
}
burger.addEventListener('click', () => toggleMenu(!menu.classList.contains('open')));
closeMenu.addEventListener('click', () => toggleMenu(false));
menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => toggleMenu(false)));
document.addEventListener('keydown', e => { if (e.key === 'Escape') { toggleMenu(false); closeModal(); }});

// Language toggle (EN ↔ हिंदी)
function setLang(l){
  document.querySelectorAll('[data-hi]').forEach(el => {
    if (el.dataset.en === undefined) el.dataset.en = el.innerHTML;
    el.innerHTML = (l === 'hi') ? el.dataset.hi : el.dataset.en;
  });
  document.documentElement.lang = (l === 'hi') ? 'hi' : 'en';
  document.querySelectorAll('.lang-btn').forEach(b => b.textContent = (l === 'hi') ? 'English' : 'हिंदी');
  try { localStorage.setItem('karsog-lang', l); } catch(e){}
}
document.querySelectorAll('.lang-btn').forEach(b =>
  b.addEventListener('click', () => { window.location.href = '/hi/'; })
);

// Live weather — Open-Meteo (free, no key). Fails silently if offline.
(function(){
  const WMO = c =>
    c === 0 ? '☀️' : c <= 2 ? '⛅' : c === 3 ? '☁️' : c <= 48 ? '🌫️' :
    c <= 57 ? '🌦️' : c <= 67 ? '🌧️' : c <= 77 ? '❄️' : c <= 82 ? '🌧️' :
    c <= 86 ? '❄️' : '⛈️';
  fetch('https://api.open-meteo.com/v1/forecast?latitude=31.3825&longitude=77.2045&current=temperature_2m,weather_code&daily=temperature_2m_max,temperature_2m_min,weather_code,precipitation_sum,snowfall_sum&timezone=Asia%2FKolkata&forecast_days=4')
    .then(r => r.json())
    .then(d => {
      const el = document.getElementById('wx');
      const days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
      let html = `${WMO(d.current.weather_code)} <b>Karsog ${Math.round(d.current.temperature_2m)}°C</b>`;
      for (let i = 1; i < d.daily.time.length; i++) {
        const day = days[new Date(d.daily.time[i]).getDay()];
        html += `<span class="sep">·</span>${day} ${WMO(d.daily.weather_code[i])} ${Math.round(d.daily.temperature_2m_max[i])}°/${Math.round(d.daily.temperature_2m_min[i])}°`;
      }
      el.innerHTML = html;
      el.hidden = false;

      // Road advisory — derived from today's forecast only. Never claims a road is open or closed.
      try {
        const code = d.daily.weather_code[0];
        const rain = d.daily.precipitation_sum ? (d.daily.precipitation_sum[0] || 0) : 0;
        const snow = d.daily.snowfall_sum ? (d.daily.snowfall_sum[0] || 0) : 0;
        let msg = '';
        if (snow > 0 || (code >= 71 && code <= 77) || code === 85 || code === 86) msg = 'Snow forecast today — upper stretches (Shikari Devi, Chindi, Janjehli) can close. Check before you travel.';
        else if (rain >= 20 || [65, 67, 82, 95, 96, 99].indexOf(code) > -1) msg = 'Heavy rain forecast today — landslides and slips are common on these hill roads. Check before you travel.';
        else if (rain >= 7 || [61, 63, 80, 81].indexOf(code) > -1) msg = 'Rain forecast today — expect slow, slippery patches on the hill roads.';
        const road = document.getElementById('road');
        if (road && msg) { road.innerHTML = `<span class="dot"></span><span class="warn">${msg}</span>`; road.hidden = false; }
      } catch (e) {}
    })
    .catch(() => {});
})();


// Submit-update modal → WhatsApp
const fab = document.getElementById('fab');
const modal = document.getElementById('modal');
const closeMdl = document.getElementById('close-mdl');
const sendBtn = document.getElementById('send');
const WA_NUMBER = '917018485157'; // update this to the site owner's WhatsApp number

function openModal(){ modal.classList.add('open'); document.body.style.overflow = 'hidden'; }
function closeModal(){ modal.classList.remove('open'); document.body.style.overflow = ''; }
if (fab) fab.addEventListener('click', openModal);
if (closeMdl) closeMdl.addEventListener('click', closeModal);
if (modal) modal.addEventListener('click', e => { if (e.target === modal) closeModal(); });

if (sendBtn) sendBtn.addEventListener('click', () => {
  const type = document.getElementById('s-type').value;
  const text = document.getElementById('s-text').value.trim();
  const name = document.getElementById('s-name').value.trim();
  if (!text) { alert('Please add some details.'); return; }
  const msg = `*Karsog.com update*%0A%0A*Type:* ${encodeURIComponent(type)}%0A*Update:* ${encodeURIComponent(text)}${name ? '%0A*From:* ' + encodeURIComponent(name) : ''}`;
  window.open(`https://wa.me/${WA_NUMBER}?text=${msg}`, '_blank', 'noopener');
  closeModal();
});

// PWA — offline bus timings & emergency numbers
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => navigator.serviceWorker.register('/sw.js').catch(() => {}));
}
