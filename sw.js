/**
 * Service worker — cache shell on install; cache media on visit.
 * Cache-first for same-origin assets.
 */

const CACHE_NAME = 'ghar-museum-v2';
const FONT_HOSTS = ['fonts.googleapis.com', 'fonts.gstatic.com'];
const SHELL = [
  './',
  './index.html',
  './styles.css',
  './app.js',
  './data.json',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  const sameOrigin = url.origin === self.location.origin;
  const isFontHost = FONT_HOSTS.includes(url.hostname);
  if (!sameOrigin && !isFontHost) return;

  event.respondWith(
    caches.match(req).then((cached) => {
      if (cached) return cached;
      return fetch(req)
        .then((res) => {
          if (!res) return res;
          const cacheable = res.status === 200 || (isFontHost && res.type === 'opaque');
          if (!cacheable) return res;
          const clone = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(req, clone));
          return res;
        })
        .catch(() => (sameOrigin ? caches.match('./index.html') : undefined));
    })
  );
});
