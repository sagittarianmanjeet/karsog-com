// Karsog.com service worker — offline bus timings & emergency numbers
const CACHE = 'karsog-v18';
const CORE = ['/', '/index.html', '/karsog-valley.jpg', '/manifest.webmanifest', '/icon-192.png', '/icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);

  // Never intercept third-party requests (YouTube, Maps, fonts, weather API)
  if (url.origin !== self.location.origin) return;

  // Network-first for the page itself (freshest bus/road info), cache fallback offline
  if (e.request.mode === 'navigate' || url.pathname === '/' || url.pathname.endsWith('index.html')) {
    e.respondWith(
      fetch(e.request)
        .then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return r; })
        .catch(() => caches.match(e.request).then(m => m || caches.match('/index.html')))
    );
    return;
  }

  // Live comments API: never cache
  if (url.pathname.startsWith('/api/')) return;

  // RTI / audit PDFs are large: always fetch from network, never store in the offline cache
  if (url.pathname.startsWith('/rti/files/') || url.pathname.endsWith('.pdf')) return;


  // Cache-first for static assets
  e.respondWith(
    caches.match(e.request).then(m => m || fetch(e.request).then(r => {
      const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return r;
    }))
  );
});
