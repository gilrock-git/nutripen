// Gera capturas de tela (1080x1920) e a imagem de destaque (1024x500) para a Play Store.
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const OUT = process.argv[2], BASE = process.argv[3] || 'http://localhost:8767/';
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 360, height: 640 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true, locale: 'pt-BR' });
  await ctx.addInitScript(() => { try { localStorage.setItem('nutripen_aviso_aceito_v1', '1'); } catch (e) {} });
  const p = await ctx.newPage();
  await p.goto(BASE); await p.waitForTimeout(500);
  await p.evaluate(() => { appState.isDemo = false; renderAll(); document.getElementById('toast-container').innerHTML = ''; });
  const shots = [
    ['01-hoje.png', 'hoje', 0],
    ['02-metas.png', 'hoje', 'macro-cards-grid'],
    ['03-diario.png', 'caneta', 0],
    ['04-medidas.png', 'evolucao', 'chart-metric-tabs', 150],
    ['05-refeicoes.png', 'refeicoes', 0],
    ['06-relatorio.png', 'relatorio', 0]
  ];
  for (const [file, tab, anchor, extra = 0] of shots) {
    await p.evaluate(t => switchTab(t), tab);
    if (tab === 'refeicoes') { await p.selectOption('#opb-protein', 'f03'); await p.selectOption('#opb-carb', 'f32'); await p.selectOption('#opb-veg', 'f13'); }
    if (anchor) await p.evaluate(([id, ex]) => { const el = document.getElementById(id); window.scrollTo(0, el.getBoundingClientRect().top + scrollY - 70 - ex); }, [anchor, extra]);
    await p.waitForTimeout(400);
    await p.screenshot({ path: path.join(OUT, file) });
  }
  // Imagem de destaque 1024x500
  const fg = await b.newPage({ viewport: { width: 1024, height: 500 } });
  const icon = fs.readFileSync(path.join(__dirname, '..', 'assets', 'icon-only.png')).toString('base64');
  const font = n => fs.readFileSync(path.join(__dirname, '..', 'www', 'fonts', n)).toString('base64');
  const shot = fs.readFileSync(path.join(OUT, '01-hoje.png')).toString('base64');
  await fg.setContent(`<html><head><style>
    @font-face{font-family:J;font-weight:800;src:url(data:font/woff2;base64,${font('plus-jakarta-sans-latin-800-normal.woff2')})}
    @font-face{font-family:I;font-weight:500;src:url(data:font/woff2;base64,${font('inter-latin-500-normal.woff2')})}
    body{margin:0;width:1024px;height:500px;overflow:hidden;background:linear-gradient(135deg,#0f766e,#134e4a);font-family:I;color:#fff;position:relative}
    .t{position:absolute;left:64px;top:118px;width:520px}
    .logo{display:flex;align-items:center;gap:18px}.logo img{width:84px;height:84px;border-radius:20px;box-shadow:0 8px 24px #0004}
    h1{font-family:J;font-weight:800;font-size:64px;margin:0;letter-spacing:-1px}
    p{font-size:27px;line-height:1.35;margin:26px 0 0;color:#ccfbf1}
    .ph{position:absolute;right:70px;top:46px;width:250px;border-radius:30px;border:8px solid #0b1f1d;box-shadow:0 20px 50px #0006;transform:rotate(-4deg)}
  </style></head><body><div class="t"><div class="logo"><img src="data:image/png;base64,${icon}"><h1>NutriPen</h1></div>
  <p>Proteína, água, peso, glicemia e rodízio da caneta — no seu ritmo, sem cadastro.</p></div>
  <img class="ph" src="data:image/png;base64,${shot}"></body></html>`);
  await fg.evaluate(() => document.fonts.ready); await fg.waitForTimeout(300);
  await fg.screenshot({ path: path.join(OUT, 'destaque-1024x500.png') });
  await b.close(); console.log('imagens geradas em', OUT);
})();
