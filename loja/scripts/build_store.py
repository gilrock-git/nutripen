#!/usr/bin/env python3
"""Gera a versão do NutriPen para a Google Play (pasta www/ do Capacitor).

Diferenças em relação à versão web:
- nenhum acesso à internet: CSS do Tailwind compilado, ícones e fontes locais;
- sem análise por IA (Gemini) e sem service worker;
- backup e relatório usam o compartilhamento nativo do Android;
- botão "voltar" do Android fecha janelas e volta para a aba Hoje.

Uso (dentro de loja/): python3 scripts/build_store.py
"""
import json, re, shutil, subprocess, sys
from pathlib import Path

LOJA = Path(__file__).resolve().parent.parent
import os
SRC = Path(os.environ.get('NUTRIPEN_SRC') or (LOJA.parent / 'fonte' / 'nutripen.html'))
OUT = Path(os.environ.get('NUTRIPEN_WWW') or (LOJA / 'www'))
NODE = LOJA / 'node_modules'

html = SRC.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global html
    n = html.count(old)
    if n != count:
        sys.exit(f'[build_store] trecho encontrado {n}x (esperado {count}): {old[:80]!r}')
    html = html.replace(old, new)


def sub(pattern, new):
    global html
    html, n = re.subn(pattern, new, html, count=1, flags=re.S)
    if n != 1:
        sys.exit(f'[build_store] padrão não encontrado: {pattern[:80]!r}')


# ---------------------------------------------------------------- dependências externas
cfg = re.search(r'tailwind\.config = (\{.*?\});\s*</script>', html, re.S).group(1)
components = re.search(r'<style type="text/tailwindcss">(.*?)</style>', html, re.S).group(1)
sub(r'\s*<link rel="preconnect" href="https://fonts\.googleapis\.com" />\s*<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin />\s*<link href="https://fonts\.googleapis\.com/[^"]+" rel="stylesheet" />',
    '\n  <link rel="stylesheet" href="fonts/fonts.css" />')
sub(r'\s*<!-- Tailwind v3.*?</script>\s*<script>\s*tailwind\.config = .*?</script>', '\n  <link rel="stylesheet" href="app.css" />')
sub(r'\s*<style type="text/tailwindcss">.*?</style>', '')
sub(r'<script src="https://unpkg\.com/lucide@[^"]+"></script>', '<script src="vendor/lucide.min.js"></script>')
rep('<title>NutriPen — Diário da Caneta</title>', '<title>NutriPen</title>')
# Política de segurança de conteúdo: só arquivos do próprio app; nenhuma conexão externa
rep('<meta charset="UTF-8" />', '<meta charset="UTF-8" />\n  <meta http-equiv="Content-Security-Policy" content="default-src \'self\'; script-src \'self\' \'unsafe-inline\'; style-src \'self\' \'unsafe-inline\'; img-src \'self\' data: blob:; font-src \'self\'; connect-src \'self\'; object-src \'none\'; base-uri \'none\'; form-action \'none\'" />')
sub(r"\n\s*window\.addEventListener\('online',[^\n]*", '')
sub(r"\n\s*window\.addEventListener\('offline',[^\n]*", '')
rep('    body { font-family:', '    header.sticky { padding-top: env(safe-area-inset-top, 0px); }\n    body { font-family:')

# ---------------------------------------------------------------- Refeições: sem IA, montador sempre visível
sub(r'<span class="px-2\.5 py-0\.5 rounded-full[^>]*>☁️ IA Gemini \(requer chave e internet\)</span>\s*<h3[^>]*>.*?</h3>\s*<p[^>]*>.*?</p>',
    '<span class="eyebrow text-brand-700 dark:text-brand-400">Registro rápido</span>\n'
    '            <h3 class="text-base sm:text-lg font-bold text-slate-900 dark:text-white mt-1">Monte seu prato</h3>\n'
    '            <p class="text-xs text-slate-600 dark:text-slate-400">Escolha proteína, carboidrato, vegetal e fruta: o app soma os macros e confere seus tetos. Para outros alimentos, use a Tabela ou o formulário abaixo.</p>')
sub(r'\s*<button type="button" onclick="toggleOfflinePlateBuilder\(\)"[^>]*>🍱 Montador rápido</button>', '')
rep('<div class="grid grid-cols-1 lg:grid-cols-12 gap-4">\n          <!-- Foto -->', '<div class="hidden">\n          <!-- Foto -->')
rep('<div id="offline-plate-builder" class="hidden rounded-2xl bg-slate-50 dark:bg-slate-800/90 border-2 border-amber-400/70',
    '<div id="offline-plate-builder" class="rounded-2xl bg-slate-50 dark:bg-slate-800/90 border border-slate-200 dark:border-slate-700')
sub(r'\s*<div>\s*<span class="eyebrow text-amber-700 dark:text-amber-300">Não usa IA • funciona sem conexão</span>\s*<h4[^>]*>🍱 Montador rápido de prato</h4>\s*</div>\s*<button type="button" onclick="toggleOfflinePlateBuilder\(false\)"[^>]*>.*?</button>',
    '\n            <h4 class="text-sm font-extrabold text-slate-900 dark:text-white">🍱 Montador de prato</h4>')
sub(r'<div class="pt-1 space-y-1">\s*<label for="pm-gemini-key"', '<div class="hidden">\n          <label for="pm-gemini-key"')

# ---------------------------------------------------------------- menu, relatório, textos
sub(r'\s*<button role="menuitem" type="button" onclick="installApp\(\)".*?</button>', '')
rep('<i data-lucide="download" class="w-4 h-4"></i> Baixar backup (JSON)', '<i data-lucide="share-2" class="w-4 h-4"></i> Salvar backup')
rep('<i data-lucide="download" class="w-3.5 h-3.5"></i> Baixar backup antes', '<i data-lucide="share-2" class="w-3.5 h-3.5"></i> Salvar backup antes')
sub(r'<a id="wa-link"[^>]*>📲 WhatsApp</a>',
    '<button type="button" onclick="shareClinicalReport()" class="btn btn-md bg-[#16a34a] hover:bg-[#15803d] text-white shadow-sm">📤 Compartilhar</button>')
rep('            <button type="button" onclick="window.print()" class="btn btn-md btn-soft">🖨️ Imprimir / PDF</button>\n', '')
rep('<p class="text-xs font-bold text-amber-700 dark:text-amber-300">Versão de teste</p>',
    '<p class="text-xs font-bold text-brand-700 dark:text-brand-400">Diário da caneta</p>')
sub(r'<li class="flex gap-2\.5"><span aria-hidden="true">📱</span>.*?</li>',
    '<li class="flex gap-2.5"><span aria-hidden="true">🔒</span><span><strong>Seus dados ficam só neste celular.</strong> Sem cadastro e sem internet: o app não envia nada a servidores, nem ao criador do app. Se desinstalar, os dados são apagados — use ⋮ → "Salvar backup" de vez em quando.</span></li>')
sub(r'<li class="flex gap-2\.5"><span aria-hidden="true">📸</span>.*?</li>\s*<li class="flex gap-2\.5"><span aria-hidden="true">🧪</span>.*?</li>',
    '<li class="flex gap-2.5"><span aria-hidden="true">🧮</span><span><strong>Comece pelo seu perfil:</strong> idade, peso, medicação e condições clínicas. As metas de proteína, água, fibras e os tetos são calculados a partir dele.</span></li>')
rep('Sei que é uma ferramenta de apoio e que meus dados ficam neste aparelho.',
    'Sei que o NutriPen é uma ferramenta de apoio e que meus dados ficam neste aparelho.')

# ---------------------------------------------------------------- integração nativa (Capacitor)
native = r'''
<script>
  // ===== Versão Google Play: integração nativa via Capacitor =====
  const NativePlugins = (window.Capacitor && window.Capacitor.Plugins) || {};
  const isNative = !!(window.Capacitor && window.Capacitor.isNativePlatform && window.Capacitor.isNativePlatform());

  // Sem IA e sem instalação web nesta versão
  window.callGeminiNutritionAI = async () => {};
  window.installApp = () => {};
  window.registerServiceWorker = () => {};
  window.toggleOfflinePlateBuilder = () => { updateOfflinePlatePreview(); };

  async function shareText(title, text) {
    if (isNative && NativePlugins.Share) {
      try { await NativePlugins.Share.share({ title, text, dialogTitle: title }); return; } catch (e) { if (String(e && e.message).includes('cancel')) return; }
    }
    try { await navigator.clipboard.writeText(text); showToast('Copiado — cole onde quiser 📋'); }
    catch (e) { showToast('Não consegui compartilhar.', 'error'); }
  }

  window.shareClinicalReport = function () {
    renderClinicalReport();
    shareText('Relatório NutriPen', window.__nutripenReportText || '');
  };

  window.exportBackupJSON = async function () {
    const copy = JSON.parse(JSON.stringify(appState));
    copy.profile.customGeminiKey = '';
    copy.exportedAt = new Date().toISOString();
    const json = JSON.stringify(copy, null, 2);
    const fileName = `nutripen-backup-${getTodayISO()}.json`;
    if (isNative && NativePlugins.Filesystem && NativePlugins.Share) {
      try {
        const res = await NativePlugins.Filesystem.writeFile({ path: fileName, data: json, directory: 'CACHE', encoding: 'utf8' });
        await NativePlugins.Share.share({ title: 'Backup NutriPen', files: [res.uri], dialogTitle: 'Salvar backup em…' });
        return;
      } catch (e) {
        if (String(e && e.message).toLowerCase().includes('cancel')) return;
        console.warn('Backup nativo falhou', e);
      }
    }
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = fileName; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    showToast('Backup salvo.');
  };

  // Depois do aviso inicial, leva direto à criação do perfil
  window.acceptWelcome = (orig => function () {
    orig();
    if (appState && appState.isDemo) setTimeout(openResetModal, 250);
  })(window.acceptWelcome);

  // Botão "voltar" do Android
  if (isNative && NativePlugins.App) {
    NativePlugins.App.addListener('backButton', () => {
      const menu = document.getElementById('more-menu');
      if (menu && !menu.classList.contains('hidden')) { closeMoreMenu(); return; }
      const open = [...document.querySelectorAll('.modal.flex')].pop();
      if (open) { if (!open.dataset.required) closeModal(open.id); return; }
      if (currentTab !== 'hoje') { switchTab('hoje'); return; }
      NativePlugins.App.exitApp();
    });
  }
</script>
'''
rep('</body>\n</html>', native + '</body>\n</html>')

# ---------------------------------------------------------------- arquivos de saída
if OUT.exists():
    shutil.rmtree(OUT)
(OUT / 'vendor').mkdir(parents=True)
(OUT / 'fonts').mkdir()
(OUT / 'index.html').write_text(html, encoding='utf-8')

fonts = [('Inter', 'inter', w) for w in (400, 500, 600, 700)] + \
        [('Plus Jakarta Sans', 'plus-jakarta-sans', w) for w in (600, 700, 800)]
css = []
for family, pkg, w in fonts:
    name = f'{pkg}-latin-{w}-normal.woff2'
    shutil.copy(NODE / '@fontsource' / pkg / 'files' / name, OUT / 'fonts' / name)
    css.append(f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{w};font-display:swap;src:url('{name}') format('woff2')}}")
(OUT / 'fonts' / 'fonts.css').write_text('\n'.join(css) + '\n', encoding='utf-8')

shutil.copy(NODE / 'lucide' / 'dist' / 'umd' / 'lucide.min.js', OUT / 'vendor' / 'lucide.min.js')

work = LOJA / '.tw'
work.mkdir(exist_ok=True)
(work / 'in.css').write_text('@tailwind base;\n@tailwind components;\n@tailwind utilities;\n' + components, encoding='utf-8')
(work / 'tailwind.config.js').write_text(
    f"module.exports = Object.assign({cfg}, {{ content: [{json.dumps(str(OUT / 'index.html'))}] }});", encoding='utf-8')
subprocess.run([str(NODE / '.bin' / 'tailwindcss'), '-c', str(work / 'tailwind.config.js'), '-i', str(work / 'in.css'),
                '-o', str(OUT / 'app.css'), '--minify'], check=True, capture_output=True)
shutil.rmtree(work)

leftover = [u for u in re.findall(r'https?://[^\s"\'<>)]+', html) if 'wa.me' not in u and 'w3.org' not in u
            and 'generativelanguage' not in u]
print('[build_store] OK →', OUT)
if leftover:
    print('[build_store] URLs externas restantes (verifique):', sorted(set(leftover)))
