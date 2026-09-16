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

const CACHE_NAME = 'ghar-museum-v47';
const SHELL = [
  './',
  './index.html',
  './styles.css?v=28',
  './app.js?v=35',
  './data.json',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './favicon.ico?v=4',
  './favicon-16x16.png?v=4',
  './favicon-32x32.png?v=4',
  './apple-touch-icon.png?v=4',
  './icons/logo-mark-simple.png?v=3',
  './icons/logo-mark-simple-light.png?v=3',
];

self.addEventListener('install', (event) => {
  /* cache.addAll() lets each request use default fetch semantics, which can
     be satisfied by the browser's own HTTP cache — so a stale disk-cached
     copy of index.html/app.js could get baked into a "fresh" install even
     right after bumping CACHE_NAME. Fetching with cache: 'reload' forces a
     real network round-trip for every shell file on install. */
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) =>
        Promise.all(SHELL.map((url) => fetch(url, { cache: 'reload' }).then((res) => cache.put(url, res))))
      )
      .then(() => self.skipWaiting())
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
