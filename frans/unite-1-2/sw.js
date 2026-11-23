// Service worker: eerst het netwerk (altijd de nieuwste versie), offline uit de cache.
// Bij installatie worden ook alle MP3's uit audio/lijst.json opgeslagen, zodat de hele toets offline werkt.
const CACHE = 'frans-unite-1-2-v2';
const FILES = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png', './icon-maskable-512.png', './apple-touch-icon-180.png'];

self.addEventListener('install', e => {
  e.waitUntil(
    fetch('audio/lijst.json')
      .then(res => res.json())
      .then(audio => caches.open(CACHE).then(c => c.addAll([...FILES, ...audio.map(name => `./audio/${name}`)])))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request)
      .then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, copy));
        return res;
      })
      .catch(() => caches.match(e.request, { ignoreSearch: true }))
  );
});
