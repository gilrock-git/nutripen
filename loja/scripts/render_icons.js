// Gera os PNGs-fonte dos ícones (assets/) a partir do desenho vetorial da caneta.
const { chromium } = require('playwright'); const path = require('path');
const PEN = '<path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/><path d="m15 5 4 4"/><path d="M9.5 11.5c1.5-1.5 3.5-1.5 5 0"/>';
const GRAD = '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#14b8a6"/><stop offset="1" stop-color="#115e59"/></linearGradient></defs>';
const pen = (size, scale, color) => { const s = size * scale / 24; const t = (size - 24 * s) / 2;
  return `<g transform="translate(${t} ${t}) scale(${s})" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${PEN}</g>`; };
const files = {
  'icon-only.png': [1024, `${GRAD}<rect width="1024" height="1024" fill="url(#g)"/>${pen(1024, 0.56, '#fff')}`],
  'icon-foreground.png': [1024, pen(1024, 0.38, '#fff')],
  'icon-background.png': [1024, `${GRAD}<rect width="1024" height="1024" fill="url(#g)"/>`],
  'splash.png': [2732, `<rect width="2732" height="2732" fill="#f8fafc"/>${GRAD}<rect x="1066" y="1066" width="600" height="600" rx="132" fill="url(#g)"/>${pen(2732, 0.12, '#fff')}`],
  'splash-dark.png': [2732, `<rect width="2732" height="2732" fill="#020617"/>${GRAD}<rect x="1066" y="1066" width="600" height="600" rx="132" fill="url(#g)"/>${pen(2732, 0.12, '#fff')}`],
};
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  for (const [name, [size, body]] of Object.entries(files)) {
    await p.setViewportSize({ width: size, height: size });
    await p.setContent(`<html><body style="margin:0;background:transparent"><svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">${body}</svg></body></html>`);
    await p.screenshot({ path: path.join(__dirname, '..', 'assets', name), omitBackground: true });
  }
  await b.close(); console.log('ícones-fonte gerados'); })();
