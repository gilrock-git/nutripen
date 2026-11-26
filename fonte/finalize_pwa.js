// Gera os PNGs dos ícones e o sw.js com versão = hash dos arquivos.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path'); const crypto = require('crypto');
const out = process.argv[2];
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  const shots = [['icon.svg', 'icon-192.png', 192], ['icon.svg', 'icon-512.png', 512], ['maskable.svg', 'maskable-512.png', 512], ['maskable.svg', 'apple-touch-icon.png', 180]];
  for (const [svg, png, size] of shots) {
    await p.setViewportSize({ width: size, height: size });
    await p.setContent(`<html><body style="margin:0">${fs.readFileSync(path.join(out, 'icons', svg), 'utf8').replace('<svg ', `<svg width="${size}" height="${size}" `)}</body></html>`);
    await p.screenshot({ path: path.join(out, 'icons', png), omitBackground: true });
  }
  await b.close();
  const files = ['index.html', 'app.css', 'vendor/lucide.min.js', 'manifest.webmanifest', 'icons/icon.svg', 'icons/icon-192.png', 'icons/icon-512.png', 'icons/maskable-512.png', 'icons/apple-touch-icon.png'];
  const hash = crypto.createHash('sha256'); files.forEach(f => hash.update(fs.readFileSync(path.join(out, f))));
  const version = hash.digest('hex').slice(0, 10);
  const sw = fs.readFileSync(path.join(__dirname, 'sw.template.js'), 'utf8')
    .replace('__VERSION__', version).replace('__FILES__', JSON.stringify(['./', ...files], null, 2));
  fs.writeFileSync(path.join(out, 'sw.js'), sw);
  console.log('sw.js versão', version);
})();
