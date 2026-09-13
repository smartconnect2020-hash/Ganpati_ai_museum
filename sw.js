/**
 * Service worker — cache shell on install; cache media on visit.
 * Cache-first for same-origin assets. No external hosts (site uses system fonts only).
 *
 * IMPORTANT: media/item-XXX/*.png (symbol badges, gallery images) have no
 * ?v=N query string, so cache-first means a returning visitor's cached copy
 * never refreshes on its own even after the file changes on the server.
 * Any time a media file changes, bump CACHE_NAME (and the ?v=N on
 * styles.css/app.js below, if those also changed) so the old cache gets
 * dropped in 'activate' and everything re-fetches fresh.
 */

const CACHE_NAME = 'ghar-museum-v10';
const SHELL = [
  './',
  './index.html',
  './styles.css?v=10',
  './app.js?v=10',
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
  if (url.origin !== self.location.origin) return;

  event.respondWith(
    caches.match(req).then((cached) => {
      if (cached) return cached;
      return fetch(req)
        .then((res) => {
          if (!res || res.status !== 200 || res.type === 'opaque') return res;
          const clone = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(req, clone));
          return res;
        })
        .catch(() => caches.match('./index.html'));
    })
  );
});
