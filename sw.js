/* NutriPen — service worker (gerado automaticamente; não editar à mão) */
const VERSION = 'bd14a3805d';
const SHELL_CACHE = `nutripen-shell-${VERSION}`;
const FONT_CACHE = 'nutripen-fonts-v1';
const SHELL_FILES = [
  "./",
  "index.html",
  "app.css",
  "vendor/lucide.min.js",
  "manifest.webmanifest",
  "icons/icon.svg",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "icons/maskable-512.png",
  "icons/apple-touch-icon.png"
];

self.addEventListener('install', event => {
  event.waitUntil(caches.open(SHELL_CACHE).then(cache => cache.addAll(SHELL_FILES)));
  // Não chama skipWaiting aqui: a página oferece "Atualizar" ao usuário.
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k.startsWith('nutripen-shell-') && k !== SHELL_CACHE).map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

self.addEventListener('message', event => {
  if (event.data === 'SKIP_WAITING') self.skipWaiting();
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // IA (Gemini) e outros serviços externos: sempre direto na rede, nunca em cache.
  if (url.hostname === 'generativelanguage.googleapis.com') return;

  // Fontes do Google: usa o cache e atualiza em segundo plano.
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    event.respondWith((async () => {
      const cache = await caches.open(FONT_CACHE);
      const cached = await cache.match(req);
      const network = fetch(req).then(res => { if (res.ok || res.type === 'opaque') cache.put(req, res.clone()); return res; }).catch(() => cached);
      return cached || network;
    })());
    return;
  }

  if (url.origin !== self.location.origin) return;

  // Navegação para o app (raiz ou index.html): abre do cache (funciona offline), ignorando ?aba=/?acao=.
  // Outras páginas do site (ex.: privacidade, prévias) seguem pela rede normalmente.
  const scopePath = new URL(self.registration.scope).pathname;
  const isAppPage = url.pathname === scopePath || url.pathname === scopePath + 'index.html';
  if (req.mode === 'navigate' && !isAppPage) {
    event.respondWith(fetch(req).catch(() => caches.match(req)));
    return;
  }
  if (req.mode === 'navigate') {
    event.respondWith((async () => {
      const cache = await caches.open(SHELL_CACHE);
      return (await cache.match('./')) || (await cache.match('index.html')) || fetch(req);
    })());
    return;
  }

  // Demais arquivos do app: cache primeiro, rede como reserva.
  event.respondWith((async () => {
    const cached = await caches.match(req, { ignoreSearch: true });
    return cached || fetch(req);
  })());
});
